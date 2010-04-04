
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
                            RegexRuler,
                            PathRuler,
                            Rule)
from bibim.ie.examples import HTMLExample
from bibim.util.beautifulsoup import BeautifulSoup


class TestRuler(unittest.TestCase):
    def setUp(self):
        self.soup01 = self._get_soup('acm01.html')
        self.soup02 = self._get_soup('acm02.html')
        self.element01 = self.soup01.find(True, text='Neurocomputing ').parent
        self.element02 = self.soup01.find('td', {'class':'small-text'}).parent
        self.element03 = self.soup01.find('col', {'width':'91%'})
        self.text01 = '2007'
        self.text02 = '2668-2678'
        self.text03 = '2008'
        self.text04 = '1459-1460'
        self.element_text = self.soup01.find(True,
                                             text=re.compile(self.text01))
        
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


class TestHTMLRuler(TestRuler):    
    def setUp(self):
        super(TestHTMLRuler, self).setUp()
        self.example01 = HTMLExample('http://some_url', self.text01,
                                     self.soup01)
        self.example02 = HTMLExample('http://some_url', self.text02,
                                     self.soup01)
        self.example03 = HTMLExample('http://some_url', self.text03,
                                     self.soup02)
        self.example04 = HTMLExample('http://some_url', self.text04,
                                     self.soup02)
                
        
class TestPathRuler(TestHTMLRuler):
    def setUp(self):
        super(TestPathRuler, self).setUp()
        self.ruler = PathRuler()
        
    def test_get_element_attrs(self):
        attrs = self.ruler._get_element_attrs(self.element01)
        self.failUnless(len(attrs) == 1)
        self.failUnless(attrs['class'] == 'mediumb-text')

    def test_is_unique(self):
        description01 = self.ruler._get_element_description(self.element01)
        self.failUnless(self.ruler._is_unique(self.soup01, description01))

        description02 = self.ruler._get_element_description(self.element02)
        self.failIf(self.ruler._is_unique(self.soup01, description02))
    
    def test_get_sibling_number(self):
        number = self.ruler._get_sibling_number(self.element03)
        self.failUnless(number == 2)
        pass

    def test_get_element_path(self):
        path = self.ruler._get_element_path(self.soup01, self.element02)
        self.failUnless(len(path) == 3)
        
    def test_rule_example(self):
        rule = self.ruler._rule_example(self.example01)
        pattern = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, 5]] 
        self.failUnless(rule.pattern == pattern)        
    
    def test_merge_patterns(self):
        general = [[[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                    [u'span', {u'class': u'small-text'}, 5]]] 

        # Merge patterns with different attributes list
        pattern = [[u'td', {u'class': u'small-text'}, 1],
                  [u'span', {u'class': u'small-text'}, 5]]         
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[u'td', {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, 5]]]
        self.failUnless(general == result, "Different attributes")
        
        # Merge patterns with different element names
        pattern = [[u'div', {u'class': u'small-text'}, 1],
                  [u'span', {u'class': u'small-text'}, 5]]          
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[None, {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, 5]]]
        self.failUnless(general == result, "Different element names")

        # Merge patterns with different sibling number
        pattern = [[u'div', {u'class': u'small-text'}, 1],
                  [u'span', {u'class': u'small-text'}, 3]]          
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[None, {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, None]]]
        self.failUnless(general == result, "Different element sibling number")
        
        # Merge patters with different attribute values
        pattern = [[u'td', {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'big-text'}, 5]] 
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[None, {u'class': u'small-text'}, 1],
                   [u'span', {}, None]]]
        self.failUnless(general == result, "Different attribute values")
        
        # Merge patterns with different length paths
        pattern = [[u'span', {u'class': u'big-text'}, 5]] 
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[None, {u'class': u'small-text'}, 1],
                   [u'span', {}, None]],
                  [[u'span', {u'class': u'big-text'}, 5]]]
        self.failUnless(general == result, "Different length")

    def test_merge_rules(self):
        rule01 = self.ruler._rule_example(self.example01)
        rule02 = self.ruler._rule_example(self.example03)
        result = self.ruler._merge_rules([rule01, rule02])
        expected = [[[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                     [u'span', {u'class': u'small-text'}, 5]]]
        self.failUnless(result.pattern == expected)
    
    def test_rule(self):
        result = self.ruler.rule(set([self.example01, self.example03]))
        expected = [[[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                     [u'span', {u'class': u'small-text'}, 5]]]
        self.failUnless(result.pattern == expected)

    def test_get_content_element(self):
        element_text = self.ruler._get_content_element(self.example01) 
        expected = ' Volume 70 ,&nbsp; Issue 16-18 &nbsp;(October 2007)'
        self.failUnless(element_text == expected)
        
    def test_get_invalid_content_element(self):
        example = HTMLExample(value='random text', content=BeautifulSoup(''))
        get_it = self.ruler._get_content_element
        self.failUnlessRaises(ValueError, get_it, example)


class TestRegexRuler(TestHTMLRuler):

    def setUp(self):
        self.ruler = RegexRuler()
        super(TestRegexRuler, self).setUp()

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

    def test_rule_example(self):
        rule = self.ruler._rule_example(self.example01)
        self.failUnless(rule.pattern == (u'\\ Volume\\ 70\\ \\,\\&nbsp\\;\\ '
            'Issue\\ 16\\-18\\ \\&nbsp\\;\\(October\\ (.*)\\)'))
    

    def test_merge_patterns(self):
        general = ['aaaaxxxx\(\)', 'bbbbxxxx\(\)']
        pattern = 'aaaaxxxx\(\)'
        result = self.ruler._merge_patterns(general, pattern)
        self.failUnless(result == general)
        

#    def test_rule(self):
#        rule = self.ruler.rule(self.soup, self.text02)
#        pattern = "\\:\\ (.*)\\&n"
#        self.failUnless(rule.pattern == pattern)

#    def test_rule_raises_exception(self):
#        self.failUnlessRaises(ValueError, self.ruler.rule, self.soup, 'some random text')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
