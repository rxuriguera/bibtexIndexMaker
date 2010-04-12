
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

from bibim import log

# TODO: Load these values from the configuration file
MINIMUM_RATIO = 0.5 

class Rule(object):
    """
    Specifies how some information can be extracted from a document.
    """
    
    def __init__(self, pattern=None):
        self.pattern = pattern

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
        
        
class Ruler(object):
    """
    Creates rules given a set of examples
    """
    
    def rule(self, training):
        """
        Given a set of examples, induces a rule that conforms them
        """
        rules = []
        for example in training:
            rules.append(self._rule_example(example))
        
        return self._merge_rules(rules) 
    
    def _rule_example(self, example):
        """
        It creates a rule that works for a specific example 
        """
        pass
    
    def _merge_rules(self, rules):
        """
        Given a set of rules, it finds their common factor to create a new 
        rule that works for all of them.
        """
        pass


class HTMLRuler(Ruler):
    """
    Creates rules that can be used with HTML documents
    """
    def _get_content_element(self, example):
        """
        Looks in the content of the example to find the element that contains
        the desired value. Raises a ValueError exception if the example's
        content does not contain the value.
        """
        try:
            element_text = example.content.find(True,
                                                text=re.compile(example.value))
        except NameError, e:
            log.error("Example's content is not an HTML document: %s" % e) #@UndefinedVariable
            
        if not element_text:
            raise ValueError
        
        return element_text
    
    def _merge_rules(self, rules):
        if not rules:
            raise ValueError
        
        # In order to have OR rules, we use a list with all the possibilities
        general_pattern = [rules.pop(0).pattern]
        
        for rule in rules:
            general_pattern = self._merge_patterns(general_pattern,
                                                   rule.pattern)
        return Rule(general_pattern)
    
    def _merge_patterns(self, general, pattern):
        pass


class RegexRuler(HTMLRuler):
    """
    Creates rules conisting of a regular expression and that define how a piece
    of informacion can be extracted from an HTML element.
    """
    
    def _rule_example(self, example):
        text = re.escape(self._get_content_element(example))
        pattern = text.replace(re.escape(example.value), '(.*)')
        return Rule(pattern)
    
    def _merge_patterns(self, general, pattern):     
        # Get the pattern from the general patterns that has the maximum 
        # ressemblance to the current pattern
        smc = difflib.SequenceMatcher
        ratios = map(lambda p: smc(None, p, pattern).quick_ratio(), general)
        g_pattern_ratio = max(ratios)
        g_pattern_index = ratios.index(g_pattern_ratio)
        g_pattern = general[g_pattern_index]
        
        if g_pattern_ratio < MINIMUM_RATIO:
            # In this case, we don't generalize the pattern and add it as 
            # another possibility.
            general.append(pattern)
            
        elif g_pattern_ratio < 1.0:
            # In this case, we generalize the general pattern to match the 
            # current one  
            general[g_pattern_index] = self._non_matching_to_regex(g_pattern,
                                                                   pattern) 
        return general
        
    def _non_matching_to_regex(self, g_pattern, pattern):
        sm = difflib.SequenceMatcher(None, g_pattern, pattern)
        while not sm.quick_ratio() == 1.0:
            matching_blocks = sm.get_matching_blocks()
            
            matching_blocks = self._apply_heuristics(g_pattern,
                                                     list(matching_blocks))
            
            g_pattern = self._replace_non_matching_block(g_pattern,
                                                         matching_blocks,
                                                         0)
            pattern = self._replace_non_matching_block(pattern,
                                                       matching_blocks,
                                                       1)
            sm.set_seqs(g_pattern, pattern)
        return g_pattern    
    
    def _replace_non_matching_block(self, str, blocks, seq=0, block=0,
                                    rep='(?:.*)'):
        # Check that the sequence is a or b
        if not ((seq in [0, 1]) and (len(blocks) > block + 2)):
            return None
        
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
        
    #def _get_within_pattern_candidate(self, element_text, text, padding=1):
    #    """
    #    Finds a pattern that matches with the given text. It does not guarantee
    #    that a search will return the same text. Padding needs to be adjusted
    #    to get the desired results.
    #    """
    #    start_index = element_text.find(text)
    #    if start_index == -1:
    #        print "Value: '%s' not found" % text
    #        return None
    #
    #    # Extend with characters from the right
    #    end_index = start_index + len(text)
    #    max_right_padding = len(element_text) - end_index 
    #    right_padding = (padding if padding <= max_right_padding 
    #                     else max_right_padding)
    #    end_index += right_padding
    #    
    #    # Extend with elements from the left
    #    max_left_padding = start_index
    #    left_padding = (padding if padding <= max_left_padding 
    #                    else max_left_padding)
    #    start_index -= left_padding            
    #    
    #    # Compile pattern
    #    pattern = element_text[start_index:end_index]
    #    pattern = re.escape(pattern)
    #    pattern = pattern.replace(re.escape(text), '(.*)')
    #    return pattern

    #def _get_within_pattern(self, element_text, text):
    #    pattern = 'some_initial_pattern'
    #    previous_pattern = 'some_other_pattern'
    #    matches = None
    #    padding = 2 # Start at padding = 2 to avoid spaces
    #    while (pattern != previous_pattern) and (not matches):
    #        previous_pattern = pattern
    #        pattern = self._get_within_pattern_candidate(element_text,
    #                                                     text, padding)
    #        matches = re.search(pattern, element_text)
    #    
    #    return pattern
        

class PathRuler(HTMLRuler):
    """
    Creates a rule described by the path to locate some piece of information 
    in an HTML document
    """ 

    def _rule_example(self, example):
        rule = Rule()
        element_text = self._get_content_element(example)
        element = element_text.parent
        rule.pattern = self._get_element_path(example.content, element)
        return rule
    
    def _merge_patterns(self, general_pattern, path):
        # All paths from the general_pattern with the same length
        same_length_path = filter(lambda p: len(p) == len(path),
                                  general_pattern)
        
        if not same_length_path:
            general_pattern.append(path)
            return general_pattern
            
        same_length_path = same_length_path.pop(0)
        
        for element01, element02 in zip(same_length_path, path):
            # Element type
            element01[0] = (element01[0] 
                            if element01[0] == element02[0] else True)
            
            # Element attributes
            fields = {}
            for field in element01[1]:
                if ((field in element02[1]) and 
                    (element01[1][field] == element02[1][field])):
                    fields[field] = element01[1][field] 
            element01[1] = fields
            
            # Number of sibbling
            element01[2] = (element01[2] 
                            if element01[2] == element02[2] else None)
        return general_pattern
    
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
  
