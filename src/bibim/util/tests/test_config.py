
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

from bibim.util.config import BibimConfig

class TestBibimConfig(unittest.TestCase):

    def setUp(self):
        self.config = BibimConfig()

    def tearDown(self):
        pass

    def test_get_database(self):
        self.failUnless(self.config.database == 'sqlite:///bibim.db')

    def test_searcher(self):
        self.failUnless(self.config.search_engine >= 0)

    def test_get_search_properties(self):
        properties = self.config._get_search_properties()
        self.failUnless(properties['min_query_length'] == 6)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
