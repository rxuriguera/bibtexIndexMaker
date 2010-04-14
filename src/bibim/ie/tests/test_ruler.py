
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
import difflib #@UnresolvedImport
from os.path import normpath, join, dirname

from bibim.ie.rules import (HTMLRuler,
                            RegexRuler,
                            PathRuler,
                            Rule,
                            RegexRule,
                            PathRule)
from bibim.ie.examples import HTMLExample
from bibim.util.beautifulsoup import BeautifulSoup

        
def get_soup(file_name):
    file_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                 'fixtures/wrappers/' + file_name)))
    file = open(file_path)
    contents = file.read()
    contents = contents.replace('\n', '')
    contents = contents.replace('\r', '')
    contents = contents.replace('\t', '')
    soup = BeautifulSoup(contents)
    file.close()
    return soup


class TestRegexRule(unittest.TestCase):
    def test_apply(self):
        text = 'The event was held in Belgrade from 1883 to 1993'
        rule = RegexRule('.*(\d{4}).*(\d{4}).*')
        result = rule.apply(text)
        self.failUnless(result == ('1883', '1993'))
        
        rule.pattern = '.*(\d{4}).*(?:\d{4}).*'
        result = rule.apply(text)
        self.failUnless(result == ('1883',))


class TestPathRule(unittest.TestCase):
    def setUp(self):
        self.rule = PathRule()
        
    def test_apply_single_path(self):
        html = get_soup('acm01.html')
        
        path = [[[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                    [u'span', {u'class': u'small-text'}, 5]]]
        self.rule.pattern = path
        
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result.startswith(' Volume 70'))

    def test_apply_multiple_paths(self):
        html = BeautifulSoup('<html><body><div id="01" class="div01"><span>'
                             'Some text</span><p>Paragraph</p></div>'
                             '</body></html>')
        
        path = [[[u'div', {u'class': u'div01'}, 1],
                 [u'span', {u'class': u'small-text'}, 5]],
                [[u'div', {u'class': u'div01'}, 1],
                 [u'span', {}, 0]]
               ]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result == "Some text")
        
    def test_apply_no_sibling(self):
        html = BeautifulSoup('<html><body><div id="01" class="div01"><span>'
                             'Some text</span><p>Paragraph</p></div>'
                             '</body></html>')
        
        path = [[[u'div', {u'class': u'div01'}, 1],
                 [u'p', {}, None]],
                [[u'div', {u'class': u'div01'}, 1],
                 [u'span', {}, 0]]
               ]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result == "Paragraph")
    
    def test_apply_no_tag(self):
        html = BeautifulSoup('<html><body><div id="01" class="div01"><span>'
                             'Some text</span><p>Paragraph</p></div>'
                             '</body></html>')
        
        path = [[[True, {u'class': u'div01'}, 1]]]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result == "Some text")
    
    def test_apply_multiple_root(self):
        html = BeautifulSoup('<html><body>'
                             '<div class="div01"/>'
                             '<div class="div01"/>'
                             '</body></html>')
        
        path = [[[True, {u'class': u'div01'}, None]]]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(result)
                
                
class TestRuler(unittest.TestCase):
    def setUp(self):
        self.soup01 = get_soup('acm01.html')
        self.soup02 = get_soup('acm02.html')
        self.element01 = self.soup01.find(True, text='Neurocomputing ').parent
        self.element02 = self.soup01.find('td', {'class':'small-text'}).parent
        self.element03 = self.soup01.find('col', {'width':'91%'})
        self.text01 = '2007'
        self.text02 = '2668-2678'
        self.text03 = '2008'
        self.text04 = '1459-1460'
        self.element_text = self.soup01.find(True,
                                             text=re.compile(self.text01))


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
        result = [[[True, {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, 5]]]
        self.failUnless(general == result, "Different element names")

        # Merge patterns with different sibling number
        pattern = [[u'div', {u'class': u'small-text'}, 1],
                  [u'span', {u'class': u'small-text'}, 3]]          
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[True, {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, None]]]
        self.failUnless(general == result, "Different element sibling number")
        
        # Merge patters with different attribute values
        pattern = [[u'td', {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'big-text'}, 5]] 
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[True, {u'class': u'small-text'}, 1],
                   [u'span', {}, None]]]
        self.failUnless(general == result, "Different attribute values")
        
        # Merge patterns with different length paths
        pattern = [[u'span', {u'class': u'big-text'}, 5]] 
        general = self.ruler._merge_patterns(general, pattern)
        result = [[[True, {u'class': u'small-text'}, 1],
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

    def test_non_matching_to_regex_different(self):
        pattern01 = 'Volume\ 31\,\ Number\ 7\ \/\ July\,\ (.*)'
        pattern02 = 'Wednesday\,\ November\ 03\,\ (.*)'
        result = self.ruler._non_matching_to_regex(pattern01, pattern02)
        self.failUnless(result == '\,\ N(?:.*)mber\ (?:.*)\,\ (.*)')
        
        pattern01 = 'July\,\ (.*)Some'
        pattern02 = '\ (.*)More'
        result = self.ruler._non_matching_to_regex(pattern01, pattern02)
        self.failUnless(result == '\ (.*)')
        
    def xtest_rule_example(self):
        rule = self.ruler._rule_example(self.example01)
        self.failUnless(rule.pattern == (u'\\ Volume\\ 70\\ \\,\\&nbsp\\;\\ '
            'Issue\\ 16\\-18\\ \\&nbsp\\;\\(October\\ (.*)\\)'))

    def test_merge_patterns(self):
        general = ['aaaaxxxx\(\)', 'bbbbxxxx\(\)']
        pattern = 'aaaaxxxx\(\)'
        result = self.ruler._merge_patterns(general, pattern)
        self.failUnless(result == general)
  
    def test_merge_patterns_02(self):
        general = [u'\\ Volume\\ 70\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 16\\-18\\ \\&nbsp\\;\\(October\\ (.*)\\)'] 
        pattern = (u'\\ Volume\\ 22\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 21\\-23\\ \\&nbsp\\;\\(January\\ (.*)\\)')
        result = self.ruler._merge_patterns(general, pattern)
        expected = [u'\\ Volume\\ (?:.*)\\ \\,\\&nbsp\\;\\ '
                     'Issue\\ (?:.*)\\-(?:.*)\\ \\&nb'
                     'sp\\;\\((?:.*)\\ (.*)\\)']
        self.failUnless(result == expected)
        

        pattern = (u'\\ Volume\\ 22\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 22\\-23\\ \\&nbsp\\;\\(May\\ (.*)\\)')
        result = self.ruler._merge_patterns(general, pattern)
        expected = [u'\\ Volume\\ (?:.*)\\ \\,\\&nbsp\\;\\ '
                     'Issue\\ (?:.*)\\-(?:.*)\\ \\&nbsp\\;'
                     '\\((?:.*)\\ (.*)\\)']
        self.failUnless(result == expected)
        

    def test_rule(self):
        result = self.ruler.rule([self.example01, self.example03])
        self.failUnless(result.pattern == [u'\\ Volume\\ (?:.*)\\ \\,\\&nbsp\\'
                                            ';\\ Issue\\ 1(?:.*)\\ \\&nbsp\\;'
                                            '\\((?:.*)\\ (.*)\\)'])        
        result = self.ruler.rule([self.example02, self.example04])
        self.failUnless(result.pattern == [u'\\ Pages\\:\\ (.*)\\&nbsp\\'
                                            ';\\&nbsp\\;'])

    def test_apply_heuristics(self):
        sm = difflib.SequenceMatcher(None, 'The 35th house', 'The 3rd House')
        result = self.ruler._apply_heuristics('The 35th house',
                                              sm.get_matching_blocks())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
