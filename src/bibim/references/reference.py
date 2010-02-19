
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
    def __init__(self):
        """
        Constructs an empty Reference
        """
        self.fields = {}
        self.format = None
        self.entry = ""

    def get_fields(self):
        """
        Returns a list of available keys
        """
        return self.__fields.keys()
    
    def _set_fields(self, fields={}):
        self.__fields = fields
        
    def get_field(self, field_name):
        return self.__fields.get(field_name)
    
    def set_field(self, field_name, value, valid=True):
        self.__fields[field_name] = ReferenceField(field_name, value)
        pass
    
    def set_entry(self, entry):
        self.__entry = entry
        
    def get_entry(self):
        return self.__entry
    
    def get_format(self):
        return self.__format

    def set_format(self, value):
        self.__format = value
        
    fields = property(get_fields, _set_fields)    
    entry = property(get_entry, set_entry)
    format = property(get_format, set_format)
        
    def has_format(self):
        return self.format is not None

    def is_valid(self):
        """
        Checks if there is any field that is not valid
        """
        valid = True
        for field in self.fields:
            if not self.fields[field].valid:
                valid = False
                break;
        return valid
