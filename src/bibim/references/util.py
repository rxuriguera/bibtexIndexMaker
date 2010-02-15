
# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker. Some functions are largely based on
# ITB's (Humboldt-University Berlin) Bibliograph.parsing, written 
# by Raphael Ritz (r.ritz@biologie.hu-berlin.de) and released under the
# Zope License v.2.1
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


def split_name(name):
    """
    Splits a name into its different parts.
    These are the valid input formats:
        first_name [middle_name] last_name
        last_name, [middle_name,] first_name
    Returns a dictionary with three values: first_name, last_name and
    middle_name.
    """
    name_representation = {'first_name' : '',
                           'middle_name' : '',
                           'last_name' : '' }
    
    comma_split = name.split(',', 2)
    if len(comma_split) == 1: 
        full_name = comma_split[0].split()
    elif len(comma_split) == 2:
        full_name = comma_split[1].split()
        full_name.append(comma_split[0])
    else:
        full_name = comma_split[2].split()
        full_name.append(comma_split[1])
        full_name.append(comma_split[0])
    
    
    if len(full_name) == 1:
        name_representation['last_name'] = full_name[0].strip()
    else:
        name_representation['first_name'] = full_name[0].strip()
        name_representation['last_name'] = full_name[-1].strip()
        for middle_part in full_name[1:-1]:
            name_representation['middle_name'] += middle_part.strip() + ' '
        name_representation['middle_name'] = (
            name_representation['middle_name'].strip()) 
        
    return name_representation
