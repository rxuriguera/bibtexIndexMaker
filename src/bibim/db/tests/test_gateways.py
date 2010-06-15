
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
from bibim.db.gateways import (ExampleGateway,
                               ReferenceGateway,
                               WrapperGateway)

class TestExampleGateway(unittest.TestCase):
    def setUp(self):
        self.eg = ExampleGateway()

    def tearDown(self):
        pass

    def xtestGetExamples(self):
        examples = self.eg.get_examples(2, "http://zetcode.com", 0.5) #@UnusedVariable
        self.eg.session.flush()
        self.eg.session.close()
        

class TestWrapperGateway(unittest.TestCase):
    def setUp(self):
        self.session = create_session('sqlite:///:memory:', True)
        self.wg = WrapperGateway(session=self.session)
        
    def _populate_db(self):
        collection01 = self.wg.new_wrapper_collection()
        collection01.field = u'a'
        collection01.url = u'url01'
        
        collection02 = self.wg.new_wrapper_collection()
        collection02.field = u'b'
        collection02.url = u'url01'
        
        collection03 = self.wg.new_wrapper_collection()
        collection03.field = u'a'
        collection03.url = u'url02'
        
        collection04 = self.wg.new_wrapper_collection()
        collection04.field = u'b'
        collection04.url = u'url02'
        
        collection05 = self.wg.new_wrapper_collection()
        collection05.field = u'a'
        collection05.url = u'url03'

        wrapper01 = self.wg.new_wrapper()
        wrapper01.downvotes = 0
        wrapper01.upvotes = 3
        wrapper01.score = 1.0
        collection01.wrappers.append(wrapper01)
        
        wrapper02 = self.wg.new_wrapper()
        wrapper02.downvotes = 0
        wrapper02.upvotes = 2
        wrapper02.score = 1.0
        collection01.wrappers.append(wrapper02)

        wrapper03 = self.wg.new_wrapper()
        wrapper03.downvotes = 1
        wrapper03.upvotes = 1
        wrapper03.score = 0.5
        collection02.wrappers.append(wrapper03)        
 
        wrapper04 = self.wg.new_wrapper()
        wrapper04.downvotes = 0
        wrapper04.upvotes = 3
        wrapper04.score = 1.0
        collection04.wrappers.append(wrapper04)
        
        wrapper05 = self.wg.new_wrapper()
        wrapper05.downvotes = 0
        wrapper05.upvotes = 2
        wrapper05.score = 1.0
        collection05.wrappers.append(wrapper05)

        wrapper06 = self.wg.new_wrapper()
        wrapper06.downvotes = 1
        wrapper06.upvotes = 1
        wrapper06.score = 0.8
        collection05.wrappers.append(wrapper06)     
        
        
        wrapper07 = self.wg.new_wrapper()
        wrapper07.downvotes = 0
        wrapper07.upvotes = 3
        wrapper07.score = 1.0
        collection05.wrappers.append(wrapper07)

        wrapper08 = self.wg.new_wrapper()
        wrapper08.downvotes = 1
        wrapper08.upvotes = 1
        wrapper08.score = 0.2
        collection05.wrappers.append(wrapper08)     
        
        self.session.flush()
        
    def test_get_available_wrappers(self):
        self._populate_db()
        wrappers = self.wg.get_available_wrappers()
        self.failUnless(wrappers == [u'url03', u'url01', u'url02'])
                                                           

class TestReferenceGateway(unittest.TestCase):
    def setUp(self):
        self.eg = ReferenceGateway()

    def xtest_find_by_id(self):
        reference = self.eg.find_reference_by_id(2) #@UnusedVariable
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
