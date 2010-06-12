
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

from bibim.references.util import split_name


class TestUtil(unittest.TestCase):

    def test_split_name(self):
        name = "Last, J."
        result = split_name(name)
        self.failUnless(result['first_name'] == 'J.')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == '')
        
        name = "Last, Middle, First"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == 'Middle')
        
        name = "First Middle Last"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == 'Middle')
        
        name = "First Last"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == '')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
