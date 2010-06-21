
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

from bibim.ie.tests import TestWrapper
from bibim.ie.reference_wrappers import ReferenceWrapper

class TestReferenceWrappers(TestWrapper):

    def setUp(self):
        self.rw = ReferenceWrapper()
        self.acm = ('http://portal.acm.org', self._get_soup('acm01.html'))
        self.citeseerx = ('http://citeseerx.ist.psu.edu', self._get_soup('citeseer01.html'))
        
    def tearDown(self):
        pass

    def test_invalid_source(self):
        self.failUnless(not self.rw.extract_info('some_source', None)[0])

    def test_portal_acm_wrapper(self):
        reference = self.rw.extract_info(self.acm[0], self.acm[1])
        self.failUnless(reference[0].startswith('@article{1316105,'))
        self.failUnless(reference[0].endswith('}'))

    def test_citeseerx_wrapper(self):
        reference = self.rw.extract_info(self.citeseerx[0], self.citeseerx[1])
        self.failUnless(reference[0].startswith('@INPROCEEDINGS{Johnson96dynamicsource'))
        self.failUnless(reference[0].endswith('}'))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
