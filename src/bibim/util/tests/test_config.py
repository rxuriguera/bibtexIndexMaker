
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

from bibim.util.config import configuration

class TestBibimConfig(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_get_database(self):
        self.failUnless(configuration.database == 'sqlite:///bibim.db')

    def test_search_engine(self):
        self.failUnless(configuration.search_engine >= 0)

    def test_search_properties(self):
        properties = configuration._get_search_properties()
        self.failUnless(properties['min_query_length'] == 6)

    def test_black_list(self):
        black_list = configuration.black_list
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
