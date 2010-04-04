
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

from bibim import log

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

    def __repr__(self):
        return "Pattern: %s" % repr(self.pattern)

    pattern = property(get_pattern, set_pattern)


#class HTMLRule(Rule):
#    """
#    Specifies how some information can be extracted from an HTML document.
#    """
#    def __init__(self, element_path=[], within_pattern=''):
#        self.element_path = element_path
#        self.within_pattern = within_pattern
#
#    def get_element_path(self):
#        return self.__element_path
#
#    def get_within_pattern(self):
#        return self.__within_pattern
#
#    def set_element_path(self, value):
#        self.__element_path = value
#
#    def set_within_pattern(self, value):
#        self.__within_pattern = value
#
#    element_path = property(get_element_path, set_element_path)
#    within_pattern = property(get_within_pattern, set_within_pattern)


class Ruler(object):
    """
    Creates rules given a set of examples
    """
    
    def rule(self, training_set):
        """
        Given a set of examples, induces a rule that conforms them
        """
        # We actually use lists instead of sets for flexibility issues. As 
        # far as we know, set elements must be hashable.
        rules = []
        for example in training_set:
            rules.append(self._rule_example(example))
        
        return self._merge_rules(rules) 
    
    def _rule_example(self, example):
        """
        It creates a rule that works for a specific example 
        """
        raise NotImplementedError
    
    def _merge_rules(self, rules):
        """
        Given a set of rules, it finds their common factor to create a new 
        rule that works for all of them.
        """
        raise NotImplementedError
        

class HTMLRuler(Ruler):
    """
    Creates rules that can be used with HTML documents
    """
    
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
        raise NotImplementedError


class RegexRuler(HTMLRuler):
    """
    Creates rules conisting of a regular expression and that define how a piece
    of informacion can be extracted from an HTML element.
    """
    
    def _rule_example(self, example):
        pass
    
    def _get_within_pattern_candidate(self, element_text, text, padding=1):
        """
        Finds a pattern that matches with the given text. It does not guarantee
        that a search will return the same text. Padding needs to be adjusted
        to get the desired results.
        """
        start_index = element_text.find(text)
        if start_index == -1:
            print "Value: '%s' not found" % text
            return None
    
        # Extend with characters from the right
        end_index = start_index + len(text)
        max_right_padding = len(element_text) - end_index 
        right_padding = (padding if padding <= max_right_padding 
                         else max_right_padding)
        end_index += right_padding
        
        # Extend with elements from the left
        max_left_padding = start_index
        left_padding = (padding if padding <= max_left_padding 
                        else max_left_padding)
        start_index -= left_padding            
        
        # Compile pattern
        pattern = element_text[start_index:end_index]
        pattern = re.escape(pattern)
        pattern = pattern.replace(re.escape(text), '(.*)')
        return pattern

    def _get_within_pattern(self, element_text, text):
        pattern = 'some_initial_pattern'
        previous_pattern = 'some_other_pattern'
        matches = None
        padding = 2 # Start at padding = 2 to avoid spaces
        while (pattern != previous_pattern) and (not matches):
            previous_pattern = pattern
            pattern = self._get_within_pattern_candidate(element_text,
                                                         text, padding)
            matches = re.search(pattern, element_text)
        
        return pattern
        

class PathRuler(HTMLRuler):
    """
    Creates a rule described by the path to locate some piece of information 
    in an HTML document
    """ 
    
    def _rule_example(self, example):
        rule = Rule()
        try:
            element_text = example.content.find(True,
                                                text=re.compile(example.value))
        except NameError, e:
            log.error("Example's content is not an HTML document: %s" % e) #@UndefinedVariable
            
        if not element_text:
            raise ValueError
        
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
                            if element01[0] == element02[0] else None)
            
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
  
