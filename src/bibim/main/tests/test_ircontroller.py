
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

from bibim.db.session import create_session
from bibim.db.gateways import WrapperGateway

from bibim.main.factory import UtilFactory
from bibim.main.controllers import IRController

from bibim.ir.types import SearchResult


class TestIRController(unittest.TestCase):
        
    def setUp(self):
        factory = UtilFactory()
        self.session = create_session('sqlite:///:memory:', True)
        self.irc = IRController(factory)
        self.queries = ['"We view these methods as tools which can be used"',
                        '"believe that the information thus extracted"',
                        '"can be used to extract useful information"']
        
    def _populate_db(self):
        wg = WrapperGateway(self.session)
        collection01 = wg.new_wrapper_collection()
        collection01.field = u'a'
        collection01.url = u'url01'
        
        collection02 = wg.new_wrapper_collection()
        collection02.field = u'b'
        collection02.url = u'url01'
        
        collection03 = wg.new_wrapper_collection()
        collection03.field = u'a'
        collection03.url = u'url02'
        
        collection04 = wg.new_wrapper_collection()
        collection04.field = u'b'
        collection04.url = u'url02'
        
        collection05 = wg.new_wrapper_collection()
        collection05.field = u'a'
        collection05.url = u'url03'

        wrapper01 = wg.new_wrapper()
        wrapper01.downvotes = 0
        wrapper01.upvotes = 3
        wrapper01.score = 1.0
        collection01.wrappers.append(wrapper01)
        
        wrapper02 = wg.new_wrapper()
        wrapper02.downvotes = 0
        wrapper02.upvotes = 2
        wrapper02.score = 1.0
        collection01.wrappers.append(wrapper02)

        wrapper03 = wg.new_wrapper()
        wrapper03.downvotes = 1
        wrapper03.upvotes = 1
        wrapper03.score = 0.5
        collection02.wrappers.append(wrapper03)        
 
        wrapper04 = wg.new_wrapper()
        wrapper04.downvotes = 0
        wrapper04.upvotes = 3
        wrapper04.score = 1.0
        collection04.wrappers.append(wrapper04)
        
        wrapper05 = wg.new_wrapper()
        wrapper05.downvotes = 0
        wrapper05.upvotes = 2
        wrapper05.score = 1.0
        collection05.wrappers.append(wrapper05)

        wrapper06 = wg.new_wrapper()
        wrapper06.downvotes = 1
        wrapper06.upvotes = 1
        wrapper06.score = 0.8
        collection05.wrappers.append(wrapper06)     
        
        
        wrapper07 = wg.new_wrapper()
        wrapper07.downvotes = 0
        wrapper07.upvotes = 3
        wrapper07.score = 1.0
        collection05.wrappers.append(wrapper07)

        wrapper08 = wg.new_wrapper()
        wrapper08.downvotes = 1
        wrapper08.upvotes = 1
        wrapper08.score = 0.2
        collection05.wrappers.append(wrapper08)     
        
        self.session.flush()
        
    def tearDown(self):
        pass

    def xtest_get_top_results_wrong_search_engine(self):
        results = self.irc.get_top_results(self.queries, -1)
        self.failUnless(not results)
    
    def xtest_get_top_results(self):
        results = self.irc.get_top_results(self.queries)
        self.failUnless(results)    
  
    def test_sort_results(self):
        self._populate_db()
        results = [SearchResult('', u'url01/dir'), SearchResult('', u'url05/someotherdir'), SearchResult('', u'http://portal.acm.org')]
        results = self.irc._sort_results(results)
        self.failUnless(results == [u'http://portal.acm.org', u'url01'])
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
