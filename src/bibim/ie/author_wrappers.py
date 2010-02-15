
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


from bibim.ie.wrappers import FieldWrapper


class AuthorFieldWrapper(FieldWrapper):
    """
    The methods of this class try to extract the authors of a given article
    page.
    """
    
    _shortcuts = {
        'portal.acm.org':'',
        'www.springerlink.com':'',
        'www.sciencedirect.com':'',
        'ieeexplore.ieee.org':'',
        'citeseerx.ist.psu.edu':''
    }
