
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

class ReferenceValidator(object):
    """
    Checks if the information from a reference is valid. Only those pieces of
    information that are available in the text can be checked (e.g. we can
    try to check if the title of a publication is correct, but not its number 
    of pages.
    """
    def __init__(self, fields=['title', 'authors',
                                        'year', 'journal']):
        """
        Creates a ReferenceValidator. The parameters that have to be checked
        can be passed as a parameter.
        """
        self.fields_to_check = fields
        
    def validate_reference(self, reference, text):
        """
        Searches the value of the fields of the reference in the full text.
        """
        for field in self.fields_to_check:
            ref_field = reference.get_field(field)
            if not ref_field:
                reference.set_field(field, None)
                continue
            
            # Check depends on the field
            if field == 'author':
                self._validate_author(ref_field, text)
            else:
                self._validate_string(ref_field, text)
    
    def _validate_string(self, ref_field, text):
        """
        Check if a field appears in the text. The value of the field may be 
        separated in different lines in the text.
        """
        str = ref_field.value.replace(' ', '[\s]+')
        pattern = re.compile(str,
                             re.I | re.M)
        occurrence = re.search(pattern, text)
        
        if not occurrence:
            ref_field.valid = False

        
    def _validate_author(self, ref_field, text):
        # TODO: implement author validation
        pass
        
