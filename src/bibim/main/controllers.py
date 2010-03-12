
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
from bibim.util.helpers import (FileFormat,
                                ReferenceFormat)
from bibim.util import (Browser,
                        BrowserError,
                        BeautifulSoup)
from bibim.util.config import BibimConfig
from bibim.rce import ExtractionError
from bibim.ir.search import (Searcher,
                             SearchError)
from bibim.ie import (ReferenceWrapper,
                      TitleFieldWrapper,
                      AuthorFieldWrapper)
from bibim.references import Reference
from bibim.references.format import ReferenceFormatter
from bibim.main.factory import UtilCreationError                  


# Retrieve constants' value from the configuration file
configuration = BibimConfig()
MIN_WORDS = configuration.search_properties['min_query_length']         
MAX_WORDS = configuration.search_properties['max_query_length']           
SKIP_QUERIES = configuration.search_properties['queries_to_skip']                          
MAX_QUERIES = configuration.search_properties['max_queries_to_try']
TOO_MANY_RESULTS = configuration.search_properties['too_many_results']
ENGINE = configuration.search_engine

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
            log.error('Could not create an extractor: %s' % e.args)
            return content

        # Extract content
        try:
            content = extractor.extract(file).content
        except ExtractionError:
            log.error('Could not extract content for file: %s' % file)
        except IOError as e:
            log.error('Error extracting file content: %s' % e.args)
        return content
    
    def get_query_strings(self, text):
        """
        Extracts query strings from a text and returns a list containing them.
        The list's size is MAX_QUERIES at most.
        """
        pattern = re.compile("([\w()?!]+[ ]+){%d,%d}" % (MIN_WORDS, MAX_WORDS))
        strings = []
        matches = re.finditer(pattern, text)
        for i in range(MAX_QUERIES + SKIP_QUERIES):
            try:
                match = matches.next()
                strings.append('"%s"' % match.group().strip())
            except StopIteration:
                break
        return strings[SKIP_QUERIES:]
    
    
class IRController(Controller):
    # Forbidden pages are webs that appear on the results, but are of no
    # interest for our application.
    forbidden_pages = ['http://academic.research.microsoft.com']
    
    def get_top_results(self, query_strings, engine=ENGINE):
        """
        Returns a list of search results.
        """
        results = []
        
        # Get a searcher
        try:
            searcher = self.util_factory.create_searcher(engine)
        except UtilCreationError as e:
            log.error('Could not create a searcher: %s' % e.args)
            return results
    
        # Search the query strings       
        for query in query_strings:
            searcher.set_query(query)
            try:
                results = searcher.get_results()
            except SearchError, e:
                log.error(e.error)
                break
        
            if searcher.num_results >= TOO_MANY_RESULTS:
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
        # field wrappers as well.
        has_wrapper = []
        doesnt_have_wrapper = []
    
        available_wrappers = ReferenceWrapper().get_available_wrappers()
        for result in results:
            if result.base_url in available_wrappers:
                has_wrapper.append(result)
            elif result.base_url in self.forbidden_pages:
                continue
            else:
                doesnt_have_wrapper.append(result)
        has_wrapper.extend(doesnt_have_wrapper)
        return has_wrapper


class IEController(Controller):
    def __init__(self, factory, target_format=ReferenceFormat.BIBTEX):
        self.brower = Browser()
        self.format = target_format
        Controller.__init__(self, factory)
        
    def extract_reference(self, top_results):
        """
        Returns a list of References if they can be extracted or an empty 
        list otherwise.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        page = None
        references = []
        for result in top_results:
            try:
                page = self.brower.get_page(result.url)
            except BrowserError as e:
                log.error('Error retrieving page %s: %s' % (result.url,
                                                            e.error))
                continue
            
            page = BeautifulSoup(page)
            
            references = self._use_reference_wrappers(result.base_url, page)
            if not references:
                references = self._use_field_wrappers(result.base_url, page)
            if references:
                break
        
        # Convert to target format, if necessary
        for reference in references:
            self._format_reference(reference)
        
        # Return the extracted reference and the result that has been used
        return (references, result)
        
    def _use_reference_wrappers(self, source, page):
        """
        Use a reference wrapper to get the reference from a given page.
        Returns a list of References with the full entry, format and a 
        structure with the different fields.
        A single publication may need more than a reference (e.g: inproceedings
        and its proceedings)
        """
        references = []
        entry, format = ReferenceWrapper().extract_info(source, page)
        if not entry:
            return references
        
        # Create a parser for the given reference format
        try:
            parser = self.util_factory.create_parser(format)
        except UtilCreationError as e:
            log.error('Could not create a parser for %s: %s' % (format,
                                                                e.args))
            return references
        
        if not parser.check_format(entry):
            log.error('Given entry is not in %s' % format)
            return references
        
        # There may be more than one entry for the same file.
        entries = parser.split_source(entry)
        for entry in entries:
            fields = parser.parse_entry(entry)
            references.append(Reference(fields, format, entry))
        return references
    
    def _use_field_wrappers(self, source, page):
        """
        Returns a list with a Reference for the publication.
        It returns a list for consistency, but it will only contain one single
        entry.
        """
        # Try to extract info
        title = TitleFieldWrapper().extract_info(source, page)
        #author = AuthorFieldWrapper().extract_info(source, page)
        # TODO: add more field wrappers
        
        #fields = {'title':title,
        #          'author':author}
        fields = {'title':title}
                  
        reference = Reference(fields=fields) 
        return [reference] if reference.has_non_empty_fields() else []

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
            log.error('Could not create a formatter for %s: %s' % 
                      (self.format, e.args))
            return
        
        formatter.format_reference(reference, generator)
        
        
    
        
        
        
