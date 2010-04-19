
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


from bibim.ie.rules import (RegexRuler,
                            PathRuler,
                            Rule,
                            RegexRule,
                            PathRule)
from bibim.ie.examples import Example, HTMLExample
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
        self.example01 = HTMLExample('http://some_url', self.text01,
                                     self.soup01)
        self.example02 = HTMLExample('http://some_url', self.text02,
                                     self.soup01)
        self.example03 = HTMLExample('http://some_url', self.text03,
                                     self.soup02)
        self.example04 = HTMLExample('http://some_url', self.text04,
                                     self.soup02)      

        
class TestPathRuler(TestRuler):
        
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

    def test_rule_element(self):
        elements = self.example01.content.findAll('span', {u'class':u'small-text'})
        rule = self.ruler._rule_element(self.example01, elements[1])
        expected = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1]]
        self.failUnless(rule.pattern == expected)
    
    def test_should_merge(self):
        rule01 = Rule([[u'a', {u'a01':u'x'}, 0], [u'b', {}, 1]])
        rule02 = Rule([[u'a', {}, 1], [u'b', {u'b02':'x'}, 2]])
        should_merge = self.ruler._should_merge(rule01, rule02)
        self.failUnless(should_merge == True)
        
        rule01 = Rule([[u'a', {u'a01':u'x'}, 0], [u'b', {}, 1], [u'c', {}, 2]])
        rule02 = Rule([[u'a', {}, 1], [u'b', {u'b02':'x'}, 2]])
        should_merge = self.ruler._should_merge(rule01, rule02)
        self.failUnless(should_merge == False)
    
    def xtest_rule_example(self):
        rules = self.ruler._rule_example(self.example01)
        pattern01 = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                     [u'span', {u'class': u'small-text'}, 5]]
        pattern02 = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                     [u'div', {u'class': u'small-text'}, 15]]
        self.failUnless(len(rules) == 2) 
        self.failUnless(rules[0].pattern == pattern01)
        self.failUnless(rules[1].pattern == pattern02)           
    
    def test_merge_patterns(self):
        general = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                    [u'span', {u'class': u'small-text'}, 5]]

        # Merge patterns with different length paths
        pattern = [[u'span', {u'class': u'big-text'}, 5]] 
        self.failUnlessRaises(ValueError, self.ruler._merge_patterns, general,
                              pattern)

        # Merge patterns with different attributes list
        pattern = [[u'td', {u'class': u'small-text'}, 1],
                  [u'span', {u'class': u'small-text'}, 5]]         
        result = self.ruler._merge_patterns(general, pattern)
        expected = [[u'td', {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'small-text'}, 5]]
        self.failUnless(result == expected, "Different attributes")
        
        # Merge patters with different attribute values
        pattern = [[u'td', {u'class': u'small-text'}, 1],
                   [u'span', {u'class': u'big-text'}, 5]] 
        result = self.ruler._merge_patterns(general, pattern)
        expected = [['td', {u'class': u'small-text'}, 1],
                   [u'span', {}, 5]]
        self.failUnless(result == expected, "Different attribute values")
        
    def test_merge_rules(self):
        g_rules = [Rule([['a', {'j':'k'}, 0], ['b', {'m':'n'}, 1]]),
                   Rule([['c', {}, 0], ['d', {}, 1]])]
        s_rules = [Rule([['a', {'x':'y', 'j':'k'}, 0], ['b', {'m':'o'}, 1]]),
                   Rule([['e', {}, 5]])]
        expected = [Rule([['a', {'j':'k'}, 0], ['b', {}, 1]]),
                    Rule([['c', {}, 0], ['d', {}, 1]]),
                    Rule([['e', {}, 5]])]
        self.ruler._merge_rules(g_rules, s_rules)
        self.failUnless(len(g_rules) == 3)
        self.failUnless(g_rules == expected)
    
    def test_rule(self):
        rules = self.ruler.rule(set([self.example01, self.example03]))
        expected = [PathRule([[u'td', {u'colspan': u'2',
                                       u'class': u'small-text'}, 1],
                              [u'span', {u'class': u'small-text'}, 5]]),
                    PathRule([[u'td', {u'colspan': u'2',
                                       u'class': u'small-text'}, 1],
                              [u'div', {u'class': u'small-text'}, 15]])]
        self.failUnless(rules == expected)

    def test_get_content_elements(self):
        elements = self.ruler._get_content_elements(self.example01) 
        expected = [u' Volume 70 ,&nbsp; Issue 16-18 &nbsp;(October 2007)',
                    u'Year of Publication:&nbsp;2007']
        self.failUnless(len(elements) == 2)
        self.failUnless(elements == expected)
        
    def test_get_invalid_content_element(self):
        example = HTMLExample(value='random text', content=BeautifulSoup(''))
        elements = self.ruler._get_content_elements(example)
        self.failIf(elements)


class TestRegexRuler(TestRuler):

    def setUp(self):
        self.ruler = RegexRuler()
        super(TestRegexRuler, self).setUp()
        
    def test_rule_example(self):
        example = Example('2007', 'Volume 31, Number 7 / July, 2007')
        rules = self.ruler._rule_example(example)
        expected = 'Volume\ 31\,\ Number\ 7\ \/\ July\,\ (.*)'
        self.failUnless(rules[0].pattern == expected)

    def test_should_merge(self):
        rule01 = Rule('Volume\ 31\,\ Number\ 7\ \/\ July\,\ (.*)')
        rule02 = Rule('Wednesday\,\ November\ 03\,\ (.*)')
        should_merge = self.ruler._should_merge(rule01, rule02)
        self.failUnless(should_merge == False)
        
        rule01 = Rule(u'\\ Volume\\ 70\\ \\,\\&nbsp\\;\\ '
                      'Issue\\ 16\\-18\\ \\&nbsp\\;\\(October\\ (.*)\\)')
        rule02 = Rule(u'\\ Volume\\ 22\\ \\,\\&nbsp\\;\\ '
                      'Issue\\ 21\\-23\\ \\&nbsp\\;\\(January\\ (.*)\\)')
        should_merge = self.ruler._should_merge(rule01, rule02)
        self.failUnless(should_merge == True)

    def test_merge_patterns(self):
        general = 'aa3aaxxxx\(\)'
        pattern = 'aa1aaxxxx\(\)'
        result = self.ruler._merge_patterns(general, pattern)
        expected = 'aa(?:.*)aaxxxx\(\)'
        self.failUnless(result == expected)
  
        general = (u'\\ Volume\\ 70\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 16\\-18\\ \\&nbsp\\;\\(October\\ (.*)\\)')
        pattern = (u'\\ Volume\\ 22\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 21\\-23\\ \\&nbsp\\;\\(January\\ (.*)\\)')
        result = self.ruler._merge_patterns(general, pattern)
        expected = (u'\\ Volume\\ (?:.*)\\ \\,\\&nbsp\\;\\ '
                     'Issue\\ (?:.*)\\-(?:.*)\\ \\&nb'
                     'sp\\;\\((?:.*)\\ (.*)\\)')
        self.failUnless(result == expected)
        
        pattern = (u'\\ Volume\\ 22\\ \\,\\&nbsp\\;\\ '
                    'Issue\\ 22\\-23\\ \\&nbsp\\;\\(May\\ (.*)\\)')
        result = self.ruler._merge_patterns(general, pattern)
        expected = (u'\\ Volume\\ (?:.*)\\ \\,\\&nbsp\\;\\ '
                     'Issue\\ (?:.*)\\-(?:.*)\\ \\&nbsp\\;'
                     '\\((?:.*)\\ (.*)\\)')
        self.failUnless(result == expected)
        
    def test_rule(self):
        example01 = Example(u'2007', u' Volume 22 ,&nbsp; '
                    'Issue 22-23 &nbsp;(May 2007)')
        example02 = Example(u'2009', u' Volume 11 ,&nbsp; '
                    'Issue 16-25 &nbsp;(May 2009)')
        example03 = Example(u'2008', u' Year of publication:&nbsp;2008')

        results = self.ruler.rule([example01, example02])
        self.failUnless(results[0].pattern == u'\\ Volume\\ (?:.*)\\ \\,\\&nb'
            'sp\\;\\ Issue\\ (?:.*)\\-2(?:.*)\\ \\&nbsp\\;\\(May\\ (.*)\\)')        

        results = self.ruler.rule([example01, example02, example03])
        self.failUnless(len(results) == 2)
        self.failUnless(results[0].pattern == u'\\ Year\\ of\\ publication\\:'
                        '\\&nbsp\\;(.*)')

    def test_apply_heuristics(self):
        sm = difflib.SequenceMatcher(None, 'The 35th house', 'The 3rd House')
        result = self.ruler._apply_heuristics('The 35th house',
                                              sm.get_matching_blocks())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
