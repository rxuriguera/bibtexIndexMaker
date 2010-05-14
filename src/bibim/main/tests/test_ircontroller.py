
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

from bibim.main.factory import UtilFactory
from bibim.main.controllers import IRController


class TestIRController(unittest.TestCase):
        
    def setUp(self):
        factory = UtilFactory()
        self.irc = IRController(factory)
        self.queries = ['"We view these methods as tools which can be used"',
                        '"believe that the information thus extracted"',
                        '"can be used to extract useful information"']

    def tearDown(self):
        pass

    def test_get_top_results_wrong_search_engine(self):
        results = self.irc.get_top_results(self.queries, -1)
        self.failUnless(not results)
    
    def test_get_top_results(self):
        results = self.irc.get_top_results(self.queries)
        self.failUnless(results)    
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
