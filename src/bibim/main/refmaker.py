
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

from bibim import log
from bibim.ie.types import Extraction
from bibim.main.controllers import (RCEController,
                                    IRController,
                                    IEController)
from bibim.main.factory import UtilFactory
from bibim.main.validation import ReferenceValidator
from bibim.util.config import configuration
from bibim.util.helpers import FileFormat

FIELD_WEIGHTS = configuration._get_validation_weights()

class ReferenceMaker(object):
    def __init__(self):
        self.factory = UtilFactory()
    
    def make_reference(self, file, target_format):
        """
        Uses the controllers to extract the content of a file, get some query
        strings, retrieve results from a search engine, and extract the
        reference.
        """
        extraction = Extraction()
        
        extraction.file_path = file
        extraction.target_format = target_format
        
        log.info("Making reference for file: %s" % file) #@UndefinedVariable

        rce = RCEController(self.factory)
        raw_text = rce.extract_content(file, FileFormat.TXT)
        if not raw_text:
            return extraction
        
        extraction.query_strings = rce.get_query_strings(raw_text)
        if not extraction.query_strings:
            log.error('No query strings extracted') #@UndefinedVariable
            return extraction
        log.debug("Query strings %s" % str(extraction.query_strings)) #@UndefinedVariable
        
        ir = IRController(self.factory)
        extraction.top_results, extraction.used_query = (
            ir.get_top_results(extraction.query_strings))
        if not extraction.top_results:
            log.error('No top results to use with the available wrappers ' #@UndefinedVariable
                      'after trying %d queries' % 
                      len(extraction.query_strings))
            return extraction
        extraction.query_strings.remove(extraction.used_query)
        
        log.debug("Used query %s" % str(extraction.used_query)) #@UndefinedVariable
        log.debug("Query returned %d top results" % len(extraction.top_results)) #@UndefinedVariable
        
        ie = IEController(self.factory, target_format)
        extraction.entries, extraction.used_result = (
            ie.extract_reference(extraction.top_results, raw_text))
        extraction.top_results.remove(extraction.used_result)
        log.info("Used result: %s" % str(extraction.used_result)) #@UndefinedVariable
        
        validator = ReferenceValidator(FIELD_WEIGHTS)
        for entry in extraction.entries:
            validator.validate(entry, raw_text)
        
        return extraction
        
