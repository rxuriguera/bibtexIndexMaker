
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
                            ElementsRegexRuler,
                            SeparatorsRegexRuler,
                            PathRuler,
                            MultiValuePathRuler,
                            Rule,
                            RegexRule,
                            SeparatorsRegexRule,
                            MultiValueRegexRule,
                            PathRule)
from bibim.ie.types import Example
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


class TestRegexRule(object):#(unittest.TestCase):
    def test_apply(self):
        text = 'The event was held in Belgrade from 1883 to 1993'
        rule = RegexRule('.*(\d{4}).*(\d{4}).*')
        result = rule.apply(text)
        self.failUnless(result == '1883')
        
        rule.pattern = '.*(\d{4}).*(?:\d{4}).*'
        result = rule.apply(text)
        self.failUnless(result == '1883')


class TestMultiValueRegexRule(unittest.TestCase):
    def setUp(self):
        self.rule = MultiValueRegexRule('(.*)')

    def test_apply(self):
        input = [u'L. Cabre, ', u'J. Mancebo, ', u'F. Solsona']
        result = self.rule.apply(input)
        self.failUnless(input == result)


class TestSeparatorsRegexRule(unittest.TestCase):
    def setUp(self):
        self.rule = SeparatorsRegexRule([u'1, ', u'2, ', u'2 and '])

    def test_apply(self):
        input = (u'L. Cabre1, J. Mancebo2, J. F. Solsona3, and the Bioethics '
                 'Working Group of the SEMICYUC')
        result = self.rule.apply(input)
        self.failUnless(len(result) == 3)     


class TestPathRule(object):#(unittest.TestCase):
    def setUp(self):
        self.rule = PathRule()
        
    def test_apply_single_path(self):
        html = get_soup('acm01.html')
        
        path = [[u'td', {u'colspan': u'2', u'class': u'small-text'}, 1],
                    [u'span', {u'class': u'small-text'}, 5]]
        self.rule.pattern = path
        
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result.startswith(' Volume 70'))
        
    def test_apply_no_sibling(self):
        html = BeautifulSoup('<html><body><div id="01" class="div01"><span>'
                             'Some text</span><p>Paragraph</p></div>'
                             '</body></html>')
        
        path = [[u'div', {u'class': u'div01'}, 1],
                [u'p', {}, None]]
               
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result == "Paragraph")
    
    def test_apply_no_tag(self):
        html = BeautifulSoup('<html><body><div id="01" class="div01"><span>'
                             'Some text</span><p>Paragraph</p></div>'
                             '</body></html>')
        
        path = [[True, {u'class': u'div01'}, 1]]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(not result)
        self.failUnless(result == "Some text")
    
    def test_apply_multiple_root(self):
        html = BeautifulSoup('<html><body>'
                             '<div class="div01"/>'
                             '<div class="div01"/>'
                             '</body></html>')
        
        path = [[True, {u'class': u'div01'}, None]]
        
        self.rule.pattern = path
        result = self.rule.apply(html)
        self.failIf(result)
                
                
class TestRuler(unittest.TestCase):
    def setUp(self):
        self.soup01 = get_soup('acm01.html')
        self.soup02 = get_soup('acm02.html')
        self.soup03 = get_soup('springer01.html')
        self.element01 = self.soup01.find(True, text='Neurocomputing ').parent
        self.element02 = self.soup01.find('td', {'class':'small-text'}).parent
        self.element03 = self.soup01.find('col', {'width':'91%'})
        self.text01 = '2007'
        self.text02 = '2668-2678'
        self.text03 = '2008'
        self.text04 = '1459-1460'
        self.text05 = '149-154'
        self.element_text = self.soup01.find(True,
                                             text=re.compile(self.text01))
        self.example01 = Example(self.text01, self.soup01, 'http://some_url')
        self.example02 = Example(self.text02, self.soup01)
        self.example03 = Example(self.text03, self.soup02, 'http://some_url')
        self.example04 = Example(self.text04, self.soup02, 'http://some_url')      
        self.example05 = Example(self.text05, self.soup03, 'http://some_url')
        
        
class TestPathRuler(object):#(TestRuler):
        
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
        
        elements = self.ruler._get_content_elements(self.example05)
        expected = [u'149-154']
        self.failUnless(len(elements) == 1)
        self.failUnless(elements == expected)
        
    def test_get_invalid_content_element(self):
        example = Example(value='random text', content=BeautifulSoup(''))
        elements = self.ruler._get_content_elements(example)
        self.failIf(elements)
        
    def test_apply(self):
        rule = PathRule([[u'td', {u'colspan': u'2',
                                  u'class': u'small-text'}, 1],
                         [u'span', {u'class': u'small-text'}, 5]
                        ])
        result = rule.apply(self.example01.content)
        self.failUnless(result == u' Volume 70 ,&nbsp; Issue 16-18 &nbsp;(October 2007)')


class TestMultiValuePathRuler(object):#(TestRuler):
    def setUp(self):
        self.ruler = MultiValuePathRuler()
        super(TestMultiValuePathRuler, self).setUp()
        
        self.example06 = Example(['.*(Botella.*P\.|P\..*Botella).*',
                                  '.*(Solona.*B\.|B\..*Solsona).*'],
                                  self.soup03)
        
        self.example07 = Example(['.*(Alberto.*Angel|Angel.*Alberto).*',
                                  '.*(Geurts.*Pierre|Pierre.*Geurts).*'],
                                  self.soup01)
        self.example08 = Example(['.*(Michael.*Sweredoski|Sweredoski.*Michael).*',
                                  '.*(Pierre.*Baldi|Baldi.*Pierre).*'],
                                  self.soup02)
    
    def test_rule_example(self):
        rules = self.ruler._rule_example(self.example06)
        self.failUnless(len(rules) == 1)
        
        rules = self.ruler._rule_example(self.example07)
        self.failUnless(len(rules) == 2)
    
    def test_rule(self):
        rules = self.ruler.rule([self.example07, self.example08])
        self.failUnless(len(rules) == 2)
    
        result = rules[0].apply(self.soup01)
        self.failUnless(len(result) == 5)


class TestRegexRuler(object):#(TestRuler):

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


class TestElementsRegexRuler(TestRuler):
    def setUp(self):
        self.ruler = ElementsRegexRuler()
        super(TestElementsRegexRuler, self).setUp()
        
        self.example06 = Example(['(Alberto.*Angel|Angel.*Alberto)',
                                  '(Geurts.*Pierre|Pierre.*Geurts)',
                                  '(Damien.*Ernst|Ernst.*Damien)'],
                                 ['The author Alberto Del Angel',
                                  'Pierre Geurts The author',
                                  'Damien Ernst'])

        self.example07 = Example(['(Alberto.*Angel|Angel.*Alberto)',
                                  '(Geurts.*Pierre|Pierre.*Geurts)',
                                  '(Damien.*Ernst|Ernst.*Damien)'],
                                 ['Alberto Del Angel',
                                  'Pierre Geurts',
                                  'Damien Ernst'])
        
    def test_rule_example(self):
        result = self.ruler._rule_example(self.example06)
        self.failUnless(result.pattern == u'The author (.*)')

    def test_rule(self):
        rules = self.ruler.rule([self.example06, self.example07])
        self.failUnless(len(rules) == 2)
         

class TestSeparatorsRegexRuler(TestRuler):
    def setUp(self):
        self.ruler = SeparatorsRegexRuler()
        super(TestSeparatorsRegexRuler, self).setUp()
        
        self.example06 = Example(['(Botella.*P\.|P\..*Botella)',
                          '(Solona.*B\.|B\..*Solsona)',
                          '(A\..*Martinez-Arias|Martinez-Arias.*A\.)',
                          '(J\.M\..*Nieto|Nieto.*J\.M\.)'],
                          [u'P. Botella1, B. Solsona1, '
                           'A. Martinez-Arias2 and J.M. '
                           'Lopez Nieto1'])     

        self.example07 = Example(['(Cabre.*L\.|L\..*Cabre)',
                          '(Mancebo.*J\.|J\..*Mancebo)',
                          '(J\..*Solsona|Solsona.*J\.)'],
                          u'L. Cabre1, J. Mancebo2, J. F. Solsona3, '
                          ' and the Bioethics Working '
                           'Group of the SEMICYUC')             

        
    def test_find_separators(self):
        pattern = '(.*)1, (.*)1, (.*)2 and (.*)1 '
        separators = self.ruler._find_separators(pattern)
        self.failUnless(separators == ['1, ', '2 and '])
    
    def test_merge_separators(self):
        sep01 = [u'1, ', u'2, ', u'2 and ']
        sep02 = [u'1, ', u'3, ', u'2 and ']
        expected = [u'1, ', '2, ', u'2 and ', u'3, ']
        result = self.ruler._merge_separators(sep01, sep02)
        self.failUnless(result == expected)
    
    def test_rule_example(self):
        rules = self.ruler._rule_example(self.example06)
        self.failUnless(len(rules) == 1)
        self.failUnless(len(rules[0].pattern) == 2)
    
    def test_rule(self):
        rules = self.ruler.rule([self.example06, self.example07])
        pass
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
