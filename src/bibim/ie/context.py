
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

import heapq #@UnresolvedImport

MIN_OCURRENCES = 2
PARENT_RECURS = 2
TOP_STRINGS = 3

class ContextResolver(object):
    
    def get_context(self, element, parent_recurs=PARENT_RECURS):
        """
        Gets a beautiful soup element and retrieves its context. 
        
        Context is defined as the strings that precede the current element but
        are not part of it.
        We don't consider the strings that go after the element in order to
        avoid context overlapping.  
        
        Context is represented as dictionary where the value is the number
        of appearances of the word.
        """
        context = {}
        
        if not element:
            return context
        
        # First, try with element's previous sibling
        context_element = element.previousSibling
        if not context_element:
            if parent_recurs:
                # TODO: As of this version, we only consider direct siblings. In
                # future versions we might look for parent's previous sibling.
                parent = element.parent
                return self.get_context(parent, parent_recurs - 1)
            else:
                return context

        strings = context_element.findAll(text=True)
        for string in strings:
            string = string.strip()
            value = context.setdefault(string, 0)
            value += 1
            context[string] = value 
        return context
    
    def merge_context(self, previous, current):
        """
        Merges two contexts by adding the string appearance indexs.
        """
        previous = dict(previous)
        for string in current:
            value = previous.setdefault(string, 0)
            value += current[string]
            previous[string] = value
        return previous

    def get_top_strings(self, context, top_strings=TOP_STRINGS):
        tuple_list = [(context[string], string) for string in context 
                      if context[string] >= MIN_OCURRENCES]
        heap = []
        for item in tuple_list:
            heapq.heappush(heap, item)
            
        return [string[1] for string in heapq.nlargest(top_strings, heap)]
         
            
    def check_context(self, control, to_check):
        """
        Checks if two contexts share any of the top words
        """
        control_top = self.get_top_strings(control)        
        if not control_top:
            return True

        valid = False
        for string in to_check:
            if string in control_top:
                valid = True
                break
        return valid
            

