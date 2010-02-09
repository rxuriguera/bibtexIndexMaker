
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


import unittest #@UnresolvedImport

from bibim.beautifulsoup import BeautifulSoup
from bibim.ie.tests import TestWrapper
from bibim.ie import AuthorFieldWrapper


class TestAuthorWrapper(TestWrapper):

    def setUp(self):
        self.afw = AuthorFieldWrapper()
        self.ieee = ('ieeexplore.ieee.org',
                     self._get_soup('ieee01.html'))
        self.citeseer = ('citeseerx.ist.psu.edu',
                         self._get_soup('citeseer01.html'))
        self.acm = ('portal.acm.org', self._get_soup('acm01.html'))
        self.springer = ('www.springerlink.com',
                         self._get_soup('springer01.html'))
        self.scienced = ('www.sciencedirect.com',
                         self._get_soup('sciencedirect01.html'))
        
    def tearDown(self):
        pass

    def test_extract_(self):
        pass
    
