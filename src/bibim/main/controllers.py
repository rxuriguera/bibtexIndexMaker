
# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker.
#
# BibtexIndexMaker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BibtexIndexMaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker. If not, see <http://www.gnu.org/licenses/>.


import re
import heapq #@UnresolvedImport

from bibim import log
from bibim.db.gateways import (WrapperGateway,
                               ExampleGateway,
                               ExtractionGateway)
from bibim.ie.reference_wrappers import ReferenceWrapper
from bibim.ie.rules import (PathRuler,
                            RegexRuler,
                            MultiValuePathRuler,
                            ElementsRegexRuler,
                            SeparatorsRegexRuler,
                            PersonRuler)
from bibim.ie.trainers import WrapperTrainer
from bibim.ie.types import Extraction
from bibim.ir.types import (SearchError,
                            SearchResult)
from bibim.main.factory import UtilCreationError                  
from bibim.main.validation import ValidatorFactory
from bibim.rce.extraction import ExtractionError
from bibim.references.reference import Reference
from bibim.references.format.formatter import ReferenceFormatter
from bibim.util.browser import (Browser,
                                BrowserError)
from bibim.util.config import configuration
from bibim.util.helpers import (FileFormat,
                                ReferenceFormat,
                                ContentCleaner)

# Retrieve constants' value from the configuration file
MIN_WORDS = configuration.search_properties['min_query_length']         
MAX_WORDS = configuration.search_properties['max_query_length']           
SKIP_QUERIES = configuration.search_properties['queries_to_skip']                          
MAX_QUERIES = configuration.search_properties['max_queries_to_try']
TOO_MANY_RESULTS = configuration.search_properties['too_many_results']
ENGINE = configuration.search_engine

MAX_WRAPPERS = configuration.wrapper_properties['max_wrappers']
MIN_VALIDITY = configuration.wrapper_properties['min_validity']
WRAPPER_GEN_EXAMPLES = configuration.wrapper_properties['wrapper_gen_examples']
MAX_EXAMPLES_FROM_DB = configuration.wrapper_properties['max_examples_from_db']
MAX_EXAMPLES = configuration.wrapper_properties['max_examples']
SECONDS_BETWEEN_REQUESTS = configuration.wrapper_properties['seconds_between_requests']


class Controller(object):
    def __init__(self, factory):
        self.util_factory = factory
    

class RCEController(Controller):
    def __init__(self, factory, min_words=MIN_WORDS, max_words=MAX_WORDS,
                 max_queries=MAX_QUERIES, skip_queries=SKIP_QUERIES):
        super(RCEController, self).__init__(factory)
        self.min_words = min_words
        self.max_words = max_words
        self.max_queries = max_queries
        self.skip_queries = skip_queries

    def get_min_words(self):
        return self.__min_words

    def get_max_words(self):
        return self.__max_words

    def get_max_queries(self):
        return self.__max_queries

    def get_skip_queries(self):
        return self.__skip_queries

    def set_min_words(self, value):
        self.__min_words = value

    def set_max_words(self, value):
        self.__max_words = value

    def set_max_queries(self, value):
        self.__max_queries = value
        
    def set_skip_queries(self, value):
        self.__skip_queries = value
        
    min_words = property(get_min_words, set_min_words)
    max_words = property(get_max_words, set_max_words)
    max_queries = property(get_max_queries, set_max_queries)
    skip_queries = property(get_skip_queries, set_skip_queries)
    
    def extract_content(self, file, target_format):
        content = None
        source_format = FileFormat().get_format(file)
        
        # Get an extractor
        try:
            extractor = self.util_factory.create_extractor(source_format,
                                                           target_format)
        except UtilCreationError as e:
            log.error('Could not create an extractor: %s' % e.args) #@UndefinedVariable
            return content

        # Extract content
        try:
            content = extractor.extract(file).content
        except ExtractionError:
            log.error('Could not extract content for file: %s' % file) #@UndefinedVariable
        except IOError as e:
            log.error('Error extracting file content: %s' % e.args) #@UndefinedVariable
        return content
    
    def get_query_strings(self, text):
        """
        Extracts query strings from a text and returns a list containing them.
        The list's size is MAX_QUERIES at most.
        """
        pattern = re.compile("([\w()?!]+[ ]){%d,%d}" % (self.min_words,
                                                        self.max_words))
        strings = []
        matches = re.finditer(pattern, text)
        for i in range(self.max_queries + self.skip_queries): #@UnusedVariable
            try:
                match = matches.next()
                strings.append('"%s"' % match.group().strip())
            except StopIteration:
                break
        return strings[self.skip_queries:]
 
 
class IRController(Controller):
    def __init__(self, factory, too_many_results=TOO_MANY_RESULTS):
        super(IRController, self).__init__(factory)
        self.too_many_results = too_many_results

    def get_too_many_results(self):
        return self.__too_many_results

    def set_too_many_results(self, value):
        self.__too_many_results = value
        
    too_many_results = property(get_too_many_results, set_too_many_results)
    
    def get_top_results(self, query_strings, engine=ENGINE):
        """
        Returns a list of search results.
        """
        results = []
        
        # Get a searcher
        try:
            searcher = self.util_factory.create_searcher(engine)
        except UtilCreationError as e:
            log.error('Could not create a searcher: %s' % e.args) #@UndefinedVariable
            return results
    
        # Search the query strings       
        for query in query_strings:
            searcher.set_query(query)
            try:
                log.debug('Searching query %s' % (query)) #@UndefinedVariable
                results = searcher.get_results()
            except SearchError, e:
                log.error(e.error) #@UndefinedVariable
                break
            
            if searcher.num_results >= self.too_many_results:
                log.debug('Search with query %s yielded too many results ' #@UndefinedVariable
                          '(%d or more)' % (query, self.too_many_results)) 
                results = []
                continue
            
            if results:
                log.info('Searcher yielded the following results using ' #@UndefinedVariable
                         'query %s' % (query)) 
                for result in results:
                    log.info('    %s' % result.url[:120]) #@UndefinedVariable
                results = self._sort_results(results)
                
            if results:
                break
            
        return (results, query)
    
    def _sort_results(self, results):
        """
        Sorts the results depending on the available wrappers. 
        Returns a list with the results that have a wrapper available on top
        of it, and those with no wrapper are discarded.
        The list is ordered depending on the quality of the wrappers.
        """

        # Create a list with all the available wrappers ordered by priority
        # Reference wrapper will be at the very beginning of the priority queue
        reference_wrappers = ReferenceWrapper().get_available_wrappers()
        available_wrappers = list(reference_wrappers)
         
        field_wrappers = WrapperGateway().get_available_wrappers()
        available_wrappers.extend(list(field_wrappers))
        
        wrappers_heap = [] 
        for result in results:
            base_url = result.base_url
            if self._in_black_list(result.url):
                continue
            elif not base_url in available_wrappers:
                continue
            else:
                # TODO: Remove this conditional
                if base_url.startswith('http://citeseerx'):
                    wrapper_index = len(results) + 5
                else:
                    wrapper_index = available_wrappers.index(base_url)
                heapq.heappush(wrappers_heap, (wrapper_index, result))
        results = heapq.nsmallest(len(results), wrappers_heap)
        return [result[1] for result in results] 
         
    def _in_black_list(self, url):
        is_in_it = False
        for element in configuration.black_list:
            if url.startswith(element):
                is_in_it = True
                break
        return is_in_it
    
        
class IEController(Controller):
    def __init__(self, factory, target_format=ReferenceFormat.BIBTEX,
                 max_wrappers=MAX_WRAPPERS,
                 max_examples=MAX_EXAMPLES,
                 max_examples_from_db=MAX_EXAMPLES_FROM_DB,
                 min_validity=MIN_VALIDITY,
                 secs_between_reqs=SECONDS_BETWEEN_REQUESTS,
                 wrapper_gen_examples=WRAPPER_GEN_EXAMPLES):
        super(IEController, self).__init__(factory)
        self.browser = Browser()
        self.format = target_format
        self.field_validation = {}
        self._set_field_validation()
        self.value_guides = configuration.wrapper_properties['value_guide']
        
        self.max_wrappers = max_wrappers
        self.max_examples = max_examples
        self.max_examples_from_db = max_examples_from_db
        self.min_validity = min_validity
        self.secs_between_reqs = secs_between_reqs
        self.wrapper_gen_examples = wrapper_gen_examples
        
    def extract_reference(self, top_results, raw_text):
        """
        Returns a list of References if they can be extracted or an empty 
        list otherwise.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        
        log.info('Using %d top results' % len(top_results)) #@UndefinedVariable
        page = None
        references = []
        for result in top_results:
            try:
                log.debug('Retrieving page for result %s' % result.url) #@UndefinedVariable
                page = self.browser.get_page(result.url)
            except BrowserError as e:
                log.error('Error retrieving page %s: %s' % (result.url, #@UndefinedVariable
                                                            e.error))
                continue
            
            page = ContentCleaner().clean_content(page)
            
            references = self._use_reference_wrappers(result.base_url, page,
                                                      raw_text)
            if not references:
                references = self._use_rule_wrappers(result.base_url, page,
                                                     raw_text)
                
            if references:
                break
        
        # Convert to target format, if necessary
        for reference in references:
            self._format_reference(reference)
        
        # Return the extracted reference and the result that has been used
        return (references, result)
    
    def _use_rule_wrappers(self, source, page, raw_text):
        """
        Look if there is any wrapper in the database for the given source.
        """
        log.info('Attempting to extract reference with ruled wrappers') #@UndefinedVariable
        fields = {}
        reference = Reference()
        wrapper_manager = WrapperGateway(max_wrappers=self.max_wrappers)
        wrapper_field_collections = wrapper_manager.find_wrapper_collections(source)
        
        for collection in wrapper_field_collections:
            # Get the wrappers for the current collection
            url, field = collection.url, collection.field
            wrappers = wrapper_manager.get_wrappers(url, field)
            log.debug('Collection %s:%s has %d wrappers' % (url, field, #@UndefinedVariable
                                                            len(wrappers)))
            
            # Get field validator
            try:
                validator = self.field_validation[collection.field][1]
            except KeyError:
                validator = None
            
            # Extract information using the wrappers we have
            for wrapper in wrappers:
                info = wrapper.extract_info(page)
                # we expect 'info' to be a string
                if type(info) == list and not (collection.field == 'author' 
                     or collection.field == 'editor'):
                    continue 
                log.debug('Info extracted by wrapper: %s' % info) #@UndefinedVariable
                
                valid = validator.validate(info, raw_text) if validator else True
                # Save the extracted info even if it's not correct. It will
                # be overwritten afterwards if necessary
                reference.set_field(field, info, valid)
                
                if not valid: 
                    log.debug('The extracted information is not valid. ' #@UndefinedVariable
                              'Downvoting wrapper.') 
                    wrapper.downvotes += 1
                    wrapper_manager.update_wrapper(wrapper)
                else:
                    log.debug('The extracted information is valid. ' #@UndefinedVariable
                              'Upvoting wrapper') 
                    wrapper.upvotes += 1
                    wrapper_manager.update_wrapper(wrapper)
                    fields[field] = info
                    break
                
        if len(reference.fields) > 0:
            log.info('Extracted reference')  #@UndefinedVariable
            return [reference]
        else:
            log.info('Could not extract reference using ruled wrappers')  #@UndefinedVariable
            return []
    
    def _use_reference_wrappers(self, source, page, raw_text):
        """
        Use a reference wrapper to get the reference from a given page.
        Returns a list of References with the full entry, format and a 
        structure with the different fields.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        log.info('Attempting to extract reference with a reference wrapper') #@UndefinedVariable
        references = []
        entry, format = ReferenceWrapper().extract_info(source, page)
        if not entry:
            log.debug('Could not find any entry using a reference wrapper') #@UndefinedVariable
            return references
        
        # Create a parser for the given reference format
        try:
            parser = self.util_factory.create_parser(format)
        except UtilCreationError as e:
            log.error('Could not create a parser for %s: %s' % (format, #@UndefinedVariable
                                                                e.args))
            return references
        
        if not parser.check_format(entry):
            log.error('Given entry is not in %s' % format) #@UndefinedVariable
            return references
        
        # There may be more than one entry for the same file.
        log.debug('Parsing extracted entries') #@UndefinedVariable
        try:
            entries = parser.split_source(entry)
            for entry in entries:
                fields = parser.parse_entry(entry)
                reference = Reference(fields, format, entry)
                self._validate_reference_fields(reference, raw_text)
                references.append(reference)
        except Exception, e:
            log.error('Error parsing extracted entry: %s ' % e) #@UndefinedVariable

        return references
    
    def _validate_reference_fields(self, reference, raw_text):
        """
        This method is a complement for _use_reference_wrappers 
        """
        log.debug('Validating reference fields') #@UndefinedVariable
        for field_name in reference.fields:
            field = reference.get_field(field_name)
            try:
                validator = self.field_validation[field_name][1]
            except KeyError:
                validator = None
                
            valid = validator.validate(field.value, raw_text) if validator else True
            field.valid = valid
        
    def _format_reference(self, reference):
        """
        Formats a reference with the target format.
        """
        if reference.format == self.format:
            return
        
        # Create a formatter and a generator
        formatter = ReferenceFormatter()
        try:
            generator = self.util_factory.create_generator(self.format)
        except UtilCreationError as e:
            log.error('Could not create a formatter for %s: %s' % #@UndefinedVariable
                      (self.format, e.args))
            return
        
        formatter.format_reference(reference, generator)
        
    
    def _set_field_validation(self):
        fields = configuration.wrapper_properties['field_validation']
        
        for field in fields.keys():
            values = list(fields[field])
            new_values = [values[0]]
            new_values.append(ValidatorFactory.create_validator(values[1], *values[2:]))
            self.field_validation[field] = new_values
    
    def _prune_wrappers(self, wrappers):
        log.debug('Prunning %d wrappers.' % len(wrappers)) #@UndefinedVariable
        max = self.max_wrappers
        prunned = []
        for wrapper in wrappers:
            max -= 1
            mv = self.min_validity / 2.0
            if wrapper.score > mv or max >= 0:
                prunned.append(wrapper)
        log.debug('After prunning: %d wrappers' % len(prunned)) #@UndefinedVariable
        return prunned
    
    def generate_wrappers(self, url):
        wrapper_manager = WrapperGateway()
        example_manager = ExampleGateway(max_examples=self.max_examples,
                                         max_examples_from_db=
                                         self.max_examples_from_db,
                                         seconds_between_requests=
                                         self.secs_between_reqs)
        example_sets = example_manager.get_examples(self.wrapper_gen_examples,
                                                    url, self.min_validity)
        
        rulers = []
        for set in example_sets:
            log.info('Starting wrapper training for set "%s"' % set) #@UndefinedVariable
            
            if set == 'author' or set == 'editor':
                rulers = [MultiValuePathRuler(),
                          SeparatorsRegexRuler(),
                          ElementsRegexRuler(),
                          PersonRuler()]
            else:
                try:
                    value_guide = self.value_guides[set]
                    pass
                except KeyError:
                    value_guide = '.*'
                rulers = [PathRuler(value_guide), RegexRuler()] 
        
            trainer = WrapperTrainer(rulers, self.wrapper_gen_examples)
            try:
                wrappers = trainer.train(example_sets[set])
                wrappers = self._prune_wrappers(wrappers)
                wrapper_manager.persist_wrappers(url, set, wrappers)
                log.info('Trainer generated %d wrappers' % len(wrappers)) #@UndefinedVariable
            except Exception, e:
                log.error('Error training wrapper for set "%s": %s' % (set, e)) #@UndefinedVariable


class ReferencesController(Controller):
    def __init__(self, factory, format=ReferenceFormat.BIBTEX):
        super(ReferencesController, self).__init__(factory)
        self.format = format

    def get_format(self):
        return self.__format

    def set_format(self, value):
        self.__format = value
        
    format = property(get_format, set_format)
    
    def _parse_entries_file(self, file_path):
        """
        Reads the file described by 'file_path' and parses all the references
        that it may contain.
        Returns a list of Reference instances with the extracted instances.
        """
        references = []
        try:
            self.parser = self.util_factory.create_parser(self.format)
        except UtilCreationError, e:
            log.error('Error creating parser for format %s: %s' % #@UndefinedVariable 
                      (str(self.format), str(e)))
            return references
        
        try:
            file = open(file_path, 'r')
            content = file.read()
        except Exception, e:
            log.error('Error reading entries file %s: %s' % #@UndefinedVariable
                      (file_path, str(e)))
            return references
        
        if not content:
            log.info('Empty entries file') #@UndefinedVariable
            return references
        
        
        if not self.parser.check_format(content):
            log.error('Given entry is not in %s' % format) #@UndefinedVariable
            return references
        
        # There may be more than one entry for the same file.
        log.debug('Parsing entries') #@UndefinedVariable
        
        entries = self.parser.split_source(content)
        for entry in entries:
            fields = self.parser.parse_entry(entry)
            reference = Reference(fields, format, entry)
            reference.validity = 1.0
            references.append(reference)
        return references
        
    def persist_file_references(self, file_path):
        """
        Parses references from a file and stores them to the database
        """
        extraction_gw = ExtractionGateway()
        references = self._parse_entries_file(file_path)
        extractions = []
        
        for reference, index in zip(references, range(len(references))):
            
            extraction = Extraction()
            
            # Clean fields that we don't want
            reference.remove_field('reference_id')
            reference.remove_field('abstract')
            reference.remove_field('reference_type')
            
            url = reference.remove_field('url')
            if not url:
                url = file_path
            else:
                url = url.value
            
            extraction.used_result = SearchResult('', url)
            text = unicode('Reference %d from %s' % (index,
                                file_path.rsplit('/', 1)[-1]))
            extraction.file_path = text
            extraction.entries.append(reference)
            extractions.append(extraction)
            extraction_gw.persist_extraction(extraction)
            log.info(''.join(['Imported ', text.lower()])) #@UndefinedVariable
        
        return extractions

