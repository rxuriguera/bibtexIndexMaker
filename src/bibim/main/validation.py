
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

class Validator(object):
    """
    Superclass that defines the basic methods that validators must implement.
    """
    def validate(self, value, *kwargs):
        raise NotImplementedError


class FieldValidator(Validator):
    pass


class RegexValidator(FieldValidator):
    """
    Validates information using a regular expression.
    """
    def __init__(self, pattern=''):
        self.pattern = pattern

    def get_pattern(self):
        return self.__pattern

    def set_pattern(self, value):
        self.__pattern = value

    pattern = property(get_pattern, set_pattern, None, None)
    
    def validate(self, value, *kwargs):
        """
        Checks if there are matches when searching the regular expression in
        in the given text value
        """
        if self.pattern and re.search(self.pattern, value):
            return True
        else:
            return False


class WithinTextValidator(FieldValidator):
    """
    Validates that a piece of information appears in a given text
    """
    def validate(self, value, *kwargs):
        """
        Checks if the value appears in the first parameter in kwargs
        """
        if len(kwargs) and re.search(value, kwargs[0]):
            return True
        return False


class PersonValidator(FieldValidator):
    """
    Validates that the values are a list of people
    """
    def validate(self, value, *kwargs):
        # TODO: For each name field, check with a WithinTextValidator
        return True
    

class ReferenceValidator(Validator):
    """
    Checks if the information from a reference is valid. Only those pieces of
    information that are available in the text can be checked (e.g. we can
    try to check if the title of a publication is correct, but not its number 
    of pages.
    """
    def __init__(self, weights={'title':0.75, 'authors':0.25}):
        """
        Creates a ReferenceValidator. The parameters that have to be checked
        can be passed as a parameter.
        """
        self.field_weights = weights 
        
    def validate(self, reference, *kwargs):
        """
        Searches the value of the fields of the reference in the full text.
        """
        validity = 0.0
        for field in reference.fields:
            weight = self.field_weights.get(field, 0.0)
            if reference.get_field(field).valid:
                validity += weight
            
        reference.validity = validity
            
        
class ValidatorFactory(object):
    @staticmethod
    def create_validator(type, *kwargs):
        try:
            return globals()[type](*kwargs)
        except KeyError:
            return Validator()
