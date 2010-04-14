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

from bibim.db.session import create_session
from bibim.ie.rules import Rule
from bibim.ie.wrappers import (RuledWrapper, RuledWrapperManager)
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
    

class TestRuledWrapperManager(unittest.TestCase):
    
    def setUp(self):
        #self.wm = RuledWrapperManager()
        self.wm = RuledWrapperManager(create_session(
            sql_uri='sqlite:///:memory:', debug=True))
    
    def test_get_unavailable_wrapper(self):
        wrapper = self.wm.get_wrapper(u'non_existent_url')
        self.failUnless(wrapper == None)

    def test_persist_wrapper_with_incorrect_rules(self):
        wrapper = RuledWrapper()
        wrapper.add_rule(u'field01', MockRule01(MockRule02(33)))
        self.failUnlessRaises(TypeError, self.wm.persist_wrapper,
                              'some_url', wrapper)
    
    def test_persist_and_get_wrapper(self):
        wrapper = RuledWrapper()
        wrapper.add_rule(u'field01', MockRule01(33))
        wrapper.add_rule(u'field01', MockRule01(55))
        wrapper.add_rule(u'field01', MockRule01(66))
        wrapper.add_rule(u'field02', MockRule02([1, [2, 3, 4, 5], 6]))

        self.wm.persist_wrapper(u'some_url', wrapper)
    
        # Get the wrapper that we've just saved
        wrapper = self.wm.get_wrapper(u'some_url')
        self.failUnless(len(wrapper.rules) == 2)
        self.failUnless('field01' in wrapper.rules)
        self.failUnless('field02' in wrapper.rules)
        self.failUnless(len(wrapper.rules['field01']) == 3)
        self.failUnless(len(wrapper.rules['field02']) == 1)

        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


