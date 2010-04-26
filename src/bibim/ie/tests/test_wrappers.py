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
from os.path import join, dirname, normpath

from bibim.db import mappers
from bibim.db.session import create_session
from bibim.ie.rules import Rule
from bibim.ie.wrappers import (Wrapper, WrapperManager)
from bibim.util import BeautifulSoup


class MockRule01(Rule):
    pass


class MockRule02(Rule):
    pass


class TestWrapper(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_soup(self, file_name):
        file_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/wrappers/' + file_name)))
        file = open(file_path)
        soup = BeautifulSoup(file.read())
        file.close()
        return soup
    

class TestWrapperManager(unittest.TestCase):
    
    def setUp(self):
        #self.wm = RuledWrapperManager()
        self.wm = WrapperManager(create_session(
            sql_uri='sqlite:///:memory:', debug=True))
    
    def test_find_collection(self):
        # Do not create
        collection1 = self.wm.find_wrapper_collection(u'some_url',
                                                     u'some_field')
        self.failIf(collection1)
        
        # New collection
        collection1 = self.wm.find_wrapper_collection(u'some_url',
                                                     u'some_field', True)
        self.failUnless(collection1)
        self.failUnless(type(collection1) == mappers.WrapperCollection)
        
        # Existent collection
        collection2 = self.wm.find_wrapper_collection(u'some_url',
                                                     u'some_field')
        self.failUnless(collection2)
        self.failUnless(collection1 is collection2)
    
    def test_find_collections(self):
        collection11 = self.wm.find_wrapper_collection(u'c01', u'f01', True)
        collection12 = self.wm.find_wrapper_collection(u'c01', u'f02', True)
        collection21 = self.wm.find_wrapper_collection(u'c02', u'f01', True)
        collection22 = self.wm.find_wrapper_collection(u'c02', u'f02', True)
        
        collections = self.wm.find_wrapper_collections()
        self.failUnless(collections.count() >= 4)
        
        collections = self.wm.find_wrapper_collections(url=u'c02')
        self.failUnless(collections.count() == 2)
    
        collections = self.wm.find_wrapper_collections(field=u'f02')
        self.failUnless(collections.count() == 2)
            
    def test_get_unavailable_wrappers(self):
        wrappers = self.wm.get_wrappers(u'non_existent_url', u'no_field')
        self.failUnless(wrappers == [])

    def xtest_persist_wrapper_with_incorrect_rules(self):
        wrapper = Wrapper()
        wrapper.add_rule(MockRule01(MockRule02(33)))
        self.failUnlessRaises(TypeError, self.wm.persist_wrapper,
                              u'some_url', u'some_field', wrapper)
    
    def xtest_persist_and_get_wrapper(self):
        wrapper = Wrapper()
        wrapper.add_rule(MockRule01(33))
        wrapper.add_rule(MockRule01(55))
        wrapper.add_rule(MockRule02([1, [2, 3, 4, 5], 6]))
        self.wm.persist_wrapper(u'some_url', u'some_field', wrapper)

        wrapper = Wrapper()
        wrapper.add_rule(MockRule01(66))
        wrapper.add_rule(MockRule01(77))
        wrapper.add_rule(MockRule02([[2, 3, 4, 5], 4]))
        self.wm.persist_wrapper(u'some_url', u'some_field', wrapper)

        wrapper = Wrapper()
        wrapper.add_rule(MockRule01(11))
        wrapper.add_rule(MockRule01(22))
        wrapper.add_rule(MockRule01(33))
        self.wm.persist_wrapper(u'some_url', u'some_other_field', wrapper)
    
        # Get non-existent wrapper
        wrappers = self.wm.get_wrappers(u'some_url', u'non_existent_field')
        self.failIf(wrappers, 'Get non-existent wrapper')
        
        # Get wrappers
        wrappers = self.wm.get_wrappers(u'some_url', u'some_field')
        self.failUnless(len(wrappers) == 2)
        wrappers = self.wm.get_wrappers(u'some_url', u'some_other_field')
        self.failUnless(len(wrappers) == 1)
        
    def test_persist_and_update_wrapper(self):
        wrapper = Wrapper()
        wrapper.add_rule(MockRule01(33))
        wrapper.add_rule(MockRule01(55))
        wrapper.add_rule(MockRule02([1, [2, 3, 4, 5], 6]))
        self.wm.persist_wrapper(u'concrete_url', u'concrete_field', wrapper)
        
        # Get wrappers
        wrappers = self.wm.get_wrappers(u'concrete_url', u'concrete_field')
        self.failUnless(len(wrappers) == 1)
        
        # Update wrapper
        wrapper = wrappers[0]
        wrapper.upvotes += 1
        wrapper.downvotes -= 1
        self.wm.update_wrapper(wrapper)
        
        # Get the wrapper again
        wrappers = self.wm.get_wrappers(u'concrete_url', u'concrete_field')
        self.failUnless(len(wrappers) == 1)
        self.failUnless(wrappers[0].upvotes == 1)
        self.failUnless(wrappers[0].downvotes == -1)
        
        # Update wrapper rules
        wrapper = wrappers[0]
        wrapper.rules[0].pattern = 223
        wrapper.rules[2].pattern = [1, 6]
        self.wm.update_wrapper(wrapper)
        
        # Get the wrapper again
        wrappers = self.wm.get_wrappers(u'concrete_url', u'concrete_field')
        self.failUnless(len(wrappers) == 1)
        self.failUnless(wrappers[0].rules[0].pattern == 223)
        self.failUnless(wrappers[0].rules[2].pattern == [1, 6])
        
        # Add another wrapper rule
        wrapper = wrappers[0]
        wrapper.rules.append(MockRule02([2, 3, 4, 5]))
        self.wm.update_wrapper(wrapper)
        
        # Get the wrapper again
        wrappers = self.wm.get_wrappers(u'concrete_url', u'concrete_field')
        self.failUnless(len(wrappers) == 1)
        self.failUnless(len(wrappers[0].rules) == 4)
        self.failUnless(wrappers[0].rules[3].pattern == [2, 3, 4, 5])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


