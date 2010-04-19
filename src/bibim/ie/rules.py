
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

import re
import difflib #@UnresolvedImport
import simplejson #@UnresolvedImport

from bibim import log

# TODO: Load these values from the configuration file
MINIMUM_RATIO = 0.5 
SIMILARITY_THRESHOLD = 0.8

class Rule(object):
    """
    Specifies how some information can be extracted from a document.
    """
    
    def __init__(self, pattern=None):
        self.pattern = pattern

    def __eq__(self, other):
        return self.pattern == other.pattern

    def get_pattern(self):
        return self.__pattern

    def set_pattern(self, value):
        self.__pattern = value

    def apply(self, input):
        pass

    def __repr__(self):
        return "Pattern: %s" % repr(self.pattern)

    pattern = property(get_pattern, set_pattern)


class RegexRule(Rule):
    """
    Defines how to apply a regex rule. The input must be a string and it will
    output a tuple with all the matching groups 
    """
    def apply(self, input):
        regex = re.compile(self.pattern)
        matches = re.search(regex, input)
        if matches:
            return matches.groups()
        else: 
            return ()
    

class PathRule(Rule):
    """
    Defines how to apply a path rule.
    The input of this rule must be a BeautifulSoup element and it will output
    a string.
    """
    def apply(self, input):
        element = ''
        for path in self.pattern:
            element = self._get_path_element(list(path), input)
            if element: 
                break
        if element:
            return element.find(True, text=True)
        else:
            return ''
    
    def _get_path_element(self, path, input):
        current = input
        tag, attrs, sibling = path.pop(0)
        
        # First element from the path must be unique
        elements = current.findAll(tag, attrs)
        if len(elements) != 1:
            return None
        current = elements[0]
        
        for tag, attrs, sibling in path:
            if sibling >= 0:
                try:
                    current = current.contents[sibling]
                except IndexError:
                    current = None
                    break
            else:
                current = current.find(tag, attrs)
        return current


class RuleFactory(object):
    def create_rule(self, rule_type, pattern):
        try:
            return globals()[rule_type](pattern)
        except KeyError:
            return Rule(pattern)

        
class Ruler(object):
    """
    Creates rules given a set of examples
    """
    def rule(self, training):
        """
        Given a set of examples, induces a rule that conforms them
        """
        rules = self._rule_example(training.pop())
        for example in training:
            example_rules = self._rule_example(example)
            self._merge_rules(rules, example_rules)
        return rules
 
    def _rule_example(self, example):
        """
        It creates a rule that works for a specific example 
        """
        return []
    
    def _merge_rules(self, generalized_rules, rules):
        """
        Given a list of rules, it finds their common with a list of some other
        rules. The result is a generalization covering the two collections. 
        """
        for rule in rules:
            self._merge_single_rule(generalized_rules, rule)
            
    def _merge_single_rule(self, g_rules, s_rule):
        """
        Given a rule and a list of rules, it generalizes the rules on the list
        so they cover the new case.
        """
        append_rule = True
        for g_rule, index in zip(g_rules, range(len(g_rules))):
            if self._should_merge(g_rule, s_rule):
                g_rule.pattern = self._merge_patterns(g_rule.pattern,
                                                      s_rule.pattern)
                append_rule = False
                break
        if append_rule:
            g_rules.append(s_rule)
    
    
class RegexRuler(Ruler):
    """
    Creates rules consisting of a regular expression that can be used to
    extract a piece of information from a text.
    """
    
    def _rule_example(self, example):
        text = re.escape(example.content)
        pattern = text.replace(re.escape(example.value), '(.*)')
        # In this case, only one rule is possible.
        return [RegexRule(pattern)]
    
    def _should_merge(self, g_rule, s_rule):
        sm = difflib.SequenceMatcher(None, g_rule.pattern, s_rule.pattern)
        return sm.quick_ratio() > SIMILARITY_THRESHOLD
    
    def _merge_patterns(self, g_pattern, s_pattern):     
        sm = difflib.SequenceMatcher(None, g_pattern, s_pattern)
        while not sm.quick_ratio() == 1.0:
            matching_blocks = sm.get_matching_blocks()
            
            matching_blocks = self._apply_heuristics(g_pattern,
                                                     list(matching_blocks))
            
            g_pattern = self._replace_non_matching_block(g_pattern,
                                                         matching_blocks,
                                                         0)
            s_pattern = self._replace_non_matching_block(s_pattern,
                                                       matching_blocks,
                                                       1)
            sm.set_seqs(g_pattern, s_pattern)
        return g_pattern
    
    def _replace_non_matching_block(self, str, blocks, seq=0, block=0,
                                    rep='(?:.*)'):
        # Check that the sequence is a or b
        if not ((seq in [0, 1]) and (len(blocks) > block)): 
            return ""
        
        if len(blocks) == block + 2:
            # Remove non-matching block
            start = blocks[block][seq]
            length = blocks[block][2]
            return str[start:start + length]
        else:
            start = blocks[block][seq] + blocks[block][2]
            length = blocks[block + 1][seq] - start
            return str[:start] + rep + str[start + length:]

    def _apply_heuristics(self, str, matching_blocks, seq=0):
        """
        This function applies an heuristic to remove matching blocks of length
        1 that are characters or numbers.
        It might be extended in the future
        """
        
        regex = re.compile("(\w{1})")
        length1 = [block for block in matching_blocks if block[2] == 1]
        
        for block in length1:
            char = str[block[seq]]
            matches = re.search(regex, char)
            if matches:
                matching_blocks.remove(block)
                
        return matching_blocks


class PathRuler(Ruler):
    """
    Creates a rule described by the path to locate some piece of information 
    in an HTML document
    """ 

    
    def _rule_example(self, example):
        rules = []
        element_rules = []
        for element in self._get_content_elements(example):
            element_rules.append(self._rule_element(example, element))
        self._merge_rules(rules, element_rules)
        return rules
    
    def _rule_element(self, example, element):
        pattern = self._get_element_path(example.content, element.parent)
        return PathRule(pattern)
    
    def _get_content_elements(self, example):
        """
        Looks in the content of the example to find the elements that contain
        the desired value. Raises a ValueError exception if the example's
        content does not contain the value.
        """
        try:
            elements = example.content.findAll(True,
                                               text=re.compile(example.value))
        except NameError, e:
            log.error("Example's content is not an HTML document: %s" % e) #@UndefinedVariable
            elements = []
        return elements

    def _should_merge(self, g_rule, s_rule):
        """
        Checks if the two patterns should be merged. In this case, two patterns
        will be merged if they have the same length with the same elements,
        i.e. they only differ in their attributes.
        """
        g_pattern, s_pattern = g_rule.pattern, s_rule.pattern
        should_merge = True
        if len(g_pattern) != len(s_pattern):
            should_merge = False
        
        for g_element, s_element in zip(g_pattern, s_pattern):
            if g_element[0] != s_element[0]:
                should_merge = False
                break
        
        return should_merge
    
    def _merge_patterns(self, g_pattern, s_pattern):
        """
        Merges two patterns (i.e. paths) of the same length and element names.
        """
        g_pattern = list(g_pattern)
        if not len(g_pattern) == len(s_pattern):
            raise ValueError
        
        for element01, element02 in zip(g_pattern, s_pattern):
            # Element attributes
            fields = {}
            for field in element01[1]:
                if ((field in element02[1]) and 
                    (element01[1][field] == element02[1][field])):
                    fields[field] = element01[1][field] 
            element01[1] = fields
        return g_pattern

    def _is_unique(self, document, description):
        """
        Test if there is more than one element with the given description 
        """
        elements = document.findAll(description[0], description[1])
        return (len(elements) == 1)

    def _get_element_attrs(self, element):
        """
        Returns the attributes of an element after doing some filtering.
        """
        forbidden_attrs = ['onclick', 'href', 'src']
        attrs = {}
        for name, value in element.attrs:
            if name not in forbidden_attrs:
                attrs[name] = value 
        return attrs
      
    def _get_sibling_number(self, element):
        parent = element.parent
        
        if not parent:
            return 0
        
        return parent.contents.index(element)
                
    def _get_element_description(self, element):
        return [element.name, self._get_element_attrs(element),
                self._get_sibling_number(element)]
        
    def _get_element_path(self, document, element):
        """
        Returns a unique path to the element. The path is composed by all the 
        necessary parent elements to make it unique. For each element it
        specifies: name, attributes and sibling number.
        Example:
            [[u'table', {u'width': u'100%'}, 7], [u'tr', {}, 0]]
        """
        path = []
        
        description = self._get_element_description(element)
        path.append(description)
        
        while not self._is_unique(document, description) and element:
            element = element.parent
    
            description = self._get_element_description(element)
            path.append(description)
        
        path.reverse()
        return path
  
