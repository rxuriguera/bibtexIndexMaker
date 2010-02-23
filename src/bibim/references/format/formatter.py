
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

from bibim.references import Reference, ReferenceField

class ReferenceFormatter(object):

    def __init__(self):
        pass
    
    def format_reference(self, reference, format_generator):
        """
        Sets the 'entry' attribute of 'reference' 
        """
        format_generator.setup_new_reference()
        format_generator.generate_header()
        
        fields = reference.get_fields()
        for field in fields:
            field = reference.get_field(field)
            generate_method = 'generate_' + field.name
            generate_method = getattr(format_generator, generate_method)
            if field.value:
                generate_method(field.value)
        
        format_generator.generate_footer()
        reference.entry = format_generator.get_generated_reference()
        
        reference.format = format_generator.format
