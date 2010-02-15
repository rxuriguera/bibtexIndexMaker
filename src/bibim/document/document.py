# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker. 
#
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


class Document(object):
    """
    """

    def __init__(self):
        """
        """
        self._metadata = {}
        self._content = None
        
    def set_metadata_field(self, field, value):
        self._metadata[field] = value
    
    def get_metadata_field(self, field):
        if field not in self._metadata.keys():
            return None
        return self._metadata[field]
    
    @property
    def available_metadata(self):
        return self._metadata.keys()
    
    def _set_content(self, cnt):
        self._content = cnt
    
    def _get_content(self):
        return self._content
    
    content = property(_get_content, _set_content)
