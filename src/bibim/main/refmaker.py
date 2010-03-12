
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

from bibim.util.helpers import FileFormat
from bibim.main.factory import UtilFactory
from bibim.main.controllers import (RCEController,
                                    IRController,
                                    IEController)
from bibim.main.validation import ReferenceValidator

class ReferenceMakerDTO(object):
    def __init__(self, file='', target_format='',
                 query_strings=[], top_results=[], entries=[]):
        self.file = file
        self.target_format = target_format
        self.query_strings = query_strings
        self.top_results = top_results
        self.entries = entries
        self.used_query = ''
        self.used_result = None
        

class ReferenceMaker(object):
    def __init__(self):
        self.factory = UtilFactory()
    
    def make_reference(self, file, target_format):
        """
        Uses the controllers to extract the content of a file, get some query
        strings, retrieve results from a search engine, and extract the
        reference.
        """
        dto = ReferenceMakerDTO(file, target_format)
        
        rce = RCEController(self.factory)
        content = rce.extract_content(file, FileFormat.TXT)
        if not content:
            return dto
        
        dto.query_strings = rce.get_query_strings(content)
        if not dto.query_strings:
            return dto
        
        ir = IRController(self.factory)
        dto.top_results, dto.used_query = ir.get_top_results(dto.query_strings)
        if not dto.top_results:
            return dto
        dto.query_strings.remove(dto.used_query)
        
        ie = IEController(self.factory, target_format)
        dto.entries, dto.used_result = ie.extract_reference(dto.top_results)
        dto.top_results.remove(dto.used_result)
        
        validator = ReferenceValidator(['title'])
        for entry in dto.entries:
            validator.validate_reference(entry, content)
            
        return dto
        
        
