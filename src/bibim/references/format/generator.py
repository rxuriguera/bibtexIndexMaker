
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

import os
import random #@UnresolvedImport

from bibim.util.helpers import ReferenceFormat

class ReferenceFormatGenerator(object):
    
    _key_order = []
    
    def __init__(self):
        self._format = None
        pass

    def get_format(self):
        return self._format
    
    format = property(get_format)

    def setup_new_reference(self):
        pass
    
    def get_generated_reference(self):
        pass
    
    def generate_header(self):
        pass
    
    def generate_footer(self):
        pass
    
    def generate_reference_type(self):
        pass

    def generate_reference_id(self):
        pass
    
    def generate_title(self):
        pass
    
    def generate_author(self):
        pass
    
    def generate_year(self):
        pass
    
    def generate_journal(self):
        pass

    def generate_pages(self):
        pass
    
    def generate_default(self):
        pass
    
    format = property(get_format, None, None, None)


class BibtexGenerator(ReferenceFormatGenerator):
    """
    Defines the methods for generating a bibtex reference. It only overrides
    the methods that are applicable.
    """
    
    _format = ReferenceFormat.BIBTEX
    
    # In some formats, the order of the fields matters
    _key_order = ['title',
                  'author',
                  'year',
                  'journal',
                  'pages']
    
    def __init__(self):
        """
        Constructs a BibtexGenerator and sets up the template for a new 
        reference.
        """
        self._type = 'article'
        self._id = self._random_refid()
        self.setup_new_reference()     

    def _get_id(self):
        return self._id

    def _set_id(self, value):
        self._id = value
    
    def _set_type(self, atype):
        self._type = atype
        
    def _get_type(self):
        return self._type
    
    id = property(_get_id, _set_id)
    type = property(_get_type, _set_type)
   
    def _random_refid(self):
        refid = ''
        for i in range(5): #@UnusedVariable
            refid = ''.join([refid, random.choice('0123456789ABCDEF')])
        return refid

    def setup_new_reference(self):
        self.run_key_order = list(self._key_order)
        self._temp_ref = {'header':'@article{%s,' % self._random_refid(),
                          'footer':'}'}
        
    def get_generated_reference(self):
        reference = self._temp_ref['header'] + os.linesep
        
        for key in self.run_key_order:
            if self._temp_ref.has_key(key):
                reference += self._temp_ref[key] + os.linesep
        reference = reference.rstrip(' ,' + os.linesep)
        reference += os.linesep + self._temp_ref['footer'] + os.linesep
        return reference

    def generate_header(self):
        self._temp_ref['header'] = ('@' + self.type.lower() + '{' + self.id + 
            ',')

    def generate_reference_type(self, reference_type='article'):
        self.type = reference_type
        # In Bibtex, the header depends on the type, so we have to generate it
        self.generate_header()

    def generate_reference_id(self, reference_id=''):
        if not reference_id:
            reference_id = self._random_refid()
            
        self.id = reference_id
        # In Bibtes, the header depends on the reference id, so we have to 
        # generate it again.
        self.generate_header()
    
    def generate_title(self, title=''):
        self._in_braces_value('title', title)
        
    def generate_author(self, authors={}):
        auth_ref = 'author = {'
        for author in authors:
            auth_ref += author['last_name']
            if author['middle_name']:
                auth_ref += ', '
            auth_ref += author['middle_name']
            if author['first_name']:
                auth_ref += ', '
            auth_ref += author['first_name']
            auth_ref += ' and '
        
        # Remove the last ' and '
        auth_ref = auth_ref[0:-5]
        auth_ref += '},'
        self._temp_ref['author'] = auth_ref

    def generate_year(self, year=''):
        self._temp_ref['year'] = 'year = ' + year + ','

    def generate_journal(self, journal=''):
        self._in_braces_value('journal', journal)
    
    def generate_pages(self, pages=''):
        self._in_braces_value('pages', pages)
    
    def _in_braces_value(self, key, value):
        self._temp_ref[key] = key + ' = {' + value + '},'
    
    def generate_default(self, field_name='', value=''):
        self.run_key_order.append(field_name)
        self._in_braces_value(field_name, value)
