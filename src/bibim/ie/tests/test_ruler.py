
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

import re
from os.path import normpath, join, dirname

from bibim.ie.rules import (HTMLRuler,
                            HTMLRule)
from bibim.util.beautifulsoup import BeautifulSoup

class TestHTMLRuler(unittest.TestCase):

    def setUp(self):
        self.ruler = HTMLRuler()
        self.soup = self._get_soup('acm01.html')
        self.element01 = self.soup.find(True, text='Neurocomputing ').parent
        self.element02 = self.soup.find('td', {'class':'small-text'}).parent
        self.element03 = self.soup.find('col', {'width':'91%'})
        self.text01 = '2007'
        self.text02 = '2668-2678'
        self.element_text = self.soup.find(True, text=re.compile(self.text01))
        
    def tearDown(self):
        pass

    def test_get_element_attrs(self):
        attrs = self.ruler._get_element_attrs(self.element01)
        self.failUnless(len(attrs) == 1)
        self.failUnless(attrs['class'] == 'mediumb-text')

    def test_is_unique(self):
        description01 = self.ruler._get_element_description(self.element01)
        self.failUnless(self.ruler._is_unique(self.soup, description01))

        description02 = self.ruler._get_element_description(self.element02)
        self.failIf(self.ruler._is_unique(self.soup, description02))
        pass
    
    def test_get_sibling_number(self):
        number = self.ruler._get_sibling_number(self.element03)
        self.failUnless(number == 2)
        pass

    def test_get_element_path(self):
        path = self.ruler._get_element_path(self.soup, self.element02)
        self.failUnless(len(path) == 3)

    def test_get_within_pattern_candidate_incorrect_result(self):
        pattern = self.ruler._get_within_pattern_candidate(self.element_text,
                                                           self.text01)
        pattern = re.compile(pattern)
        matches = re.search(pattern, self.element_text)
        self.failUnless(matches)
        groups = matches.groups()
        self.failUnless(len(groups) == 1)
        # The text should not be extracted properly
        self.failIf(groups[0] == self.text01)
        
    def test_get_within_pattern__candidate_too_much_padding(self):
        pattern = self.ruler._get_within_pattern_candidate(self.element_text,
                                                           self.text01, 10)
        pattern = re.compile(pattern)
        matches = re.search(pattern, self.element_text)
        self.failUnless(matches)
        groups = matches.groups()
        self.failUnless(len(groups) == 1)
        self.failUnless(groups[0] == self.text01)

    def test_rule(self):
        rule = self.ruler.rule(self.soup, self.text02)
        path = [(u'td', {u'colspan': u'2', u'class': u'small-text'}, 1), (u'div', {u'class': u'small-text'}, 14)]
        pattern = "\\:\\ (.*)\\&n"
        self.failUnless(rule.element_path == path)
        self.failUnless(rule.within_pattern == pattern)

    def test_rule_raises_exception(self):
        self.failUnlessRaises(ValueError, self.ruler.rule, self.soup, 'some random text')
            
    def _get_soup(self, file_name):
        file_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/wrappers/' + file_name)))
        file = open(file_path)
        contents = file.read()
        contents = contents.replace('\n', '')
        contents = contents.replace('\r', '')
        contents = contents.replace('\t', '')
        soup = BeautifulSoup(contents)
        #soup = BeautifulSoup(file.read())
        file.close()
        return soup

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
