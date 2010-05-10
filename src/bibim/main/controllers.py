
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

from bibim import log
from bibim.db.gateways import (WrapperGateway,
                               ExampleGateway)
from bibim.ie.reference_wrappers import ReferenceWrapper
from bibim.ie.rules import (PathRuler,
                            RegexRuler)
from bibim.ie.trainers import WrapperTrainer
from bibim.ir.types import SearchError
from bibim.main.factory import UtilCreationError                  
from bibim.main.validation import ValidatorFactory
from bibim.rce import ExtractionError
from bibim.references.reference import Reference
from bibim.references.format.formatter import ReferenceFormatter
from bibim.util import (Browser,
                        BrowserError,
                        BeautifulSoup)
from bibim.util.config import configuration
from bibim.util.helpers import (FileFormat,
                                ReferenceFormat)

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
        pattern = re.compile("([\w()?!]+[ ]+){%d,%d}" % (MIN_WORDS, MAX_WORDS))
        strings = []
        matches = re.finditer(pattern, text)
        for i in range(MAX_QUERIES + SKIP_QUERIES): #@UnusedVariable
            try:
                match = matches.next()
                strings.append('"%s"' % match.group().strip())
            except StopIteration:
                break
        return strings[SKIP_QUERIES:]
    
    
class IRController(Controller):
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
                log.debug('Searching query %s with engine %d' % (query, engine)) #@UndefinedVariable
                results = searcher.get_results()
            except SearchError, e:
                log.error(e.error) #@UndefinedVariable
                break
        
            if searcher.num_results >= TOO_MANY_RESULTS:
                log.debug('Search with query %s yielded too many results ' #@UndefinedVariable
                          '(%d or more)' % (query, TOO_MANY_RESULTS)) 
                continue
            
            if results:
                break
        return (self._sort_results(results), query)
    
    def _sort_results(self, results):
        """
        Sorts the results depending on the available wrappers. 
        Returns a list with the results that have a wrapper available on top
        of it. If two or more results have a wrapper available, the order 
        from the search engine is preserved.
        """
        # TODO: Refactor this method an extend it to sort depending on the
        # ruled wrappers as well.
        has_wrapper = []
        doesnt_have_wrapper = []
    
        log.debug('Sorting %d results' % len(results)) #@UndefinedVariable
    
        available_wrappers = ReferenceWrapper().get_available_wrappers()
        for result in results:
            if result.base_url in available_wrappers:
                has_wrapper.append(result)
            elif result.base_url in configuration.black_list:
                continue
            else:
                doesnt_have_wrapper.append(result)
        has_wrapper.extend(doesnt_have_wrapper)
        return has_wrapper


class IEController(Controller):
    def __init__(self, factory, target_format=ReferenceFormat.BIBTEX):
        self.browser = Browser()
        self.format = target_format
        self.field_validation = {}
        self._set_field_validation()
        Controller.__init__(self, factory)
        
    def extract_reference(self, top_results, raw_text):
        """
        Returns a list of References if they can be extracted or an empty 
        list otherwise.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        
        log.debug('Extracting reference from %d ' % len(top_results)) #@UndefinedVariable
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
            
            page = self._clean_content(page)
            page = BeautifulSoup(page)
            
            references = self._use_reference_wrappers(result.base_url, page,
                                                      raw_text)
            if not references:
                references = self._use_rule_wrappers(result.base_url, page,
                                                     raw_text)
                
            #if not references:
            #references = self._use_field_wrappers(result.base_url, page)
            if references:
                break
        
        # Convert to target format, if necessary
        for reference in references:
            self._format_reference(reference)
        
        # Return the extracted reference and the result that has been used
        return (references, result)
    
    def _clean_content(self, content):
        """
        Removes blank spaces from the retrieved page
        """
        if not content:
            return None
        content = content.replace('\n', '')
        content = content.replace('\r', '')
        content = content.replace('\t', '')
        return content
    
    def _use_rule_wrappers(self, source, page, raw_text):
        """
        Look if there is any wrapper in the database for the given source.
        """
        log.debug('Attempting to extract reference with ruled wrappers') #@UndefinedVariable
        fields = {}
        reference = Reference()
        wrapper_manager = WrapperGateway(max_wrappers=MAX_WRAPPERS)
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
                if not (type(info) == str or type(info) == unicode):
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
            return [reference]
        else:
            return []
    
    def _use_reference_wrappers(self, source, page, raw_text):
        """
        Use a reference wrapper to get the reference from a given page.
        Returns a list of References with the full entry, format and a 
        structure with the different fields.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        log.debug('Attempting to extract reference with a reference wrapper') #@UndefinedVariable
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
        entries = parser.split_source(entry)
        for entry in entries:
            fields = parser.parse_entry(entry)
            reference = Reference(fields, format, entry)
            self._validate_reference_fields(reference, raw_text)
            references.append(reference)

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
     
    def generate_wrappers(self, url):
        wrapper_manager = WrapperGateway()
        example_manager = ExampleGateway(max_examples_from_db=
                                        MAX_EXAMPLES_FROM_DB,
                                        seconds_between_requests=
                                        SECONDS_BETWEEN_REQUESTS)
        example_sets = example_manager.get_examples(WRAPPER_GEN_EXAMPLES, url,
                                                    MIN_VALIDITY)
        
        rulers = []
        for set in example_sets:
            if set == 'authors' or set == 'editors':
                pass
            else:
                rulers = [PathRuler(), RegexRuler()] 
        
            trainer = WrapperTrainer(rulers, WRAPPER_GEN_EXAMPLES)
            wrappers = trainer.train(example_sets[set])
            wrapper_manager.persist_wrappers(url, set, wrappers)
