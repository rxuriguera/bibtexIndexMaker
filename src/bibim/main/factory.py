
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

from __future__ import absolute_import #@UnresolvedImport

from bibim.util import FileFormat #@UnresolvedImport
from bibim.rce import Extractor, TextExtractor, PDFTextExtractor #@UnresolvedImport

class UtilCreationError(Exception):
    pass

class UtilFactory(object):
    
    _extractors = {FileFormat.TXT:{FileFormat.PDF:PDFTextExtractor}}
    
    def create_extractor(self, source_format, target_format):
        if target_format in self._extractors.keys():
            if source_format in self._extractors[target_format].keys():
                return self._extractors[target_format][source_format]()
        raise UtilCreationError('Converter from %s to %s is not available' % 
                                (source_format, target_format))
