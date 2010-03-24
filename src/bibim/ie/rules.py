
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

from bibim.util.beautifulsoup import BeautifulSoup
from bibim.ie.examples import (ExampleManager,
                               Example)

class Rule(object):
    """
    Specifies how some information can be extracted from a document.
    """
    pass

class HTMLRule(object):
    """
    Specifies how some information can be extracted from an HTML document.
    """
    def __init__(self, element_path=[], within_pattern=''):
        self.element_path = element_path
        self.within_pattern = within_pattern

    def get_element_path(self):
        return self.__element_path

    def get_within_pattern(self):
        return self.__within_pattern

    def set_element_path(self, value):
        self.__element_path = value

    def set_within_pattern(self, value):
        self.__within_pattern = value

    element_path = property(get_element_path, set_element_path)
    within_pattern = property(get_within_pattern, set_within_pattern)


class Ruler(object):
    """
    Induces a rule to locate a pice of information in a document.
    """
    
    def rule(self, document, info):
        raise NotImplementedError
        

class HTMLRuler(Ruler):
    """
    Induces a rule to locate a piece of information in an HTML document
    """ 
    
    def rule(self, document, info):
        rule = HTMLRule()
        
        element_text = document.find(True, text=re.compile(info))
        element = element_text.parent

        rule.element_path = self._get_element_path(document, element)
        rule.within_pattern = self._get_within_pattern(element_text, info)
        
        return rule
    
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
        return (element.name, self._get_element_attrs(element),
                self._get_sibling_number(element))
        
    def _get_element_path(self, document, element):
        """
        Returns a unique path to the element. The path is composed by all the 
        necessary parent elements to make it unique. For each element it
        specifies: name, attributes and sibling number.
        Example:
            [(u'table', {u'width': u'100%'}, 7), (u'tr', {}, 0)]
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
        padding = 1
        while (pattern != previous_pattern) and (not matches):
            previous_pattern = pattern
            pattern = self._get_within_pattern_candidate(element_text,
                                                         text, padding)
            matches = re.search(pattern, element_text)
        
        return pattern
        
