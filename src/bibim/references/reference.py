
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
 

class ReferenceField(object):
    def __init__(self, name, value, valid=True):
        self.name = name
        self.value = value
        self.valid = valid

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def is_valid(self):
        return self.__valid

    def set_name(self, value):
        self.__name = value

    def set_value(self, value):
        self.__value = value

    def set_valid(self, value):
        self.__valid = value

    name = property(get_name, set_name)
    value = property(get_value, set_value)
    valid = property(is_valid, set_valid)

class Reference(object):
    """
    This class represents a bibliographic reference.
    """
    def __init__(self, fields={}, format=None, entry=''):
        """
        Constructs an empty Reference
        """
        self.fields = fields
        self.format = format
        self.entry = entry
        self.validity = 0.0

    def get_fields(self):
        """
        Returns a list of available keys
        """
        return self.__fields.keys()
    
    def set_fields(self, fields={}):
        self.__fields = {}
        for field in fields.keys():
            self.set_field(field, fields[field])
        
    def get_field(self, field_name):
        return self.__fields.get(field_name)
    
    def set_field(self, field_name, value, valid=True):
        if not value:
            valid = False
        self.__fields[field_name] = ReferenceField(field_name, value, valid)
    
    def set_entry(self, entry):
        self.__entry = entry
        
    def get_entry(self):
        return self.__entry
    
    def get_format(self):
        return self.__format

    def set_format(self, value):
        self.__format = value
   
    def set_validity(self, value):
        self.__validity = value
   
    def get_validity(self):
        """
        Returns a float representing the confidence that its fields are correct
        """
        #self.validity = 0.0
        #inc = 1 / len(self.fields)
        #for field in self.fields:
        #    if self.get_field(field).valid:
        #        self.validity += inc
        return self.__validity
        
    fields = property(get_fields, set_fields)    
    entry = property(get_entry, set_entry)
    format = property(get_format, set_format)
    validity = property(get_validity, set_validity)
        
    def has_format(self):
        return self.format is not None

    def has_non_empty_fields(self):
        """
        Checks if there is any field with a value (not None).
        """
        filled = False
        for field in self.fields:
            if self.get_field(field).value:
                filled = True
                break
        return filled

    def __repr__(self):
        return 'format: %s\nentry:\n%s' % (self.format, self.entry)
