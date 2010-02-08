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
from bibim.ie import TitleFieldWrapper


class TestTitleWrapper(TestWrapper):

    def setUp(self):
        self.tfw = TitleFieldWrapper()
        self.acm01 = ('portal.acm.org', self._get_soup('acm01.html'))

    def tearDown(self):
        pass

    def test_extract_strong_in_td(self):
        self.failUnless(self.tfw.extract_info(self.acm01[0], self.acm01[1]) == 
            ('Estimation of rotor angles of synchronous machines using '
            'artificial neural networks and local PMU-based quantities'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
