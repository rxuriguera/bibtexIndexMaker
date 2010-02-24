
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

class ReferenceMaker(object):
    def __init__(self):
        self.factory = UtilFactory()
    
    def make_reference(self, file, target_format):
        """
        Uses the controllers to extract the content of a file, get some query
        strings, retrieve results from a search engine, and extract the
        reference.
        """
        entries = []
        
        rce = RCEController(self.factory)
        content = rce.extract_content(file, FileFormat.TXT)
        if not content:
            return entries
        
        query_strings = rce.get_query_strings(content)
        if not query_strings:
            return entries
        
        ir = IRController(self.factory)
        top_results = ir.get_top_results(query_strings)
        if not top_results:
            return entries
        
        ie = IEController(self.factory, target_format)
        entries = ie.extract_reference(top_results)
        return entries
        
        
