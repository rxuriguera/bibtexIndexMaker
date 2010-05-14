
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


from bibim import log
from bibim.ie.rating import AverageRater

"""
This module defines the basic types used for the information extraction
package
"""

class Extraction(object):
    """
    Helper class that encapsulates all the information generated during the
    extraction.
    """
    def __init__(self):
        self.id = None
        self.file_path = u''
        self.target_format = u''
        self.entries = []
        self.query_strings = []
        self.__top_results = []
        self.used_query = ''
        self.used_result = None
        self.added = u''


class Rule(object):
    """
    Specifies how some information can be extracted from a document.
    """
    
    def __init__(self, pattern=None, id=None):
        self.id = id
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
        return "Rule(%s)" % repr(self.pattern)

    pattern = property(get_pattern, set_pattern)


class Example(object):
    """
    Represents an example defining a piece of information to be extracted. 
    """
    def __init__(self, value=None, content=None, url=u'', valid=True, ref_id=None):
        self.ref_id = ref_id
        self.value = value
        self.content = content
        self.valid = valid
        self.url = url

    def get_ref_id(self):
        return self.__ref_id

    def set_ref_id(self, value):
        self.__ref_id = value

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
    
    def get_content(self):
        return self.__content
    
    def set_content(self, value):
        self.__content = value
   
    def get_valid(self):
        return self.__valid

    def set_valid(self, value):
        self.__valid = value
   
    def get_url(self):
        return self.__url
    
    def set_url(self, value):
        self.__url = value

    value = property(get_value, set_value)
    content = property(get_content, set_content)
    url = property(get_url, set_url)
    valid = property(get_valid, set_valid)
    ref_id = property(get_ref_id, set_ref_id)
    
    def __repr__(self):
        return "Example(value: %s,content: %s)" % (str(self.value),
                                                   str(self.content))    


class Wrapper(object):
    """
    Defines methods to extract information using a set of
    rules. Each wrapper will have a list of rules that will be applied
    in the given order. Rules used by this class must have a pattern that only 
    consist of python built-in classes (i.e. string, int, list, tuple, 
    dictionary, etc.)
    """
    def __init__(self, rules=[], upvotes=0, downvotes=0,
                 rater=AverageRater(), id=None):
        self.id = id
        self.rules = list(rules)
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.rater = rater

    def get_rules(self):
        return self.__rules

    def set_rules(self, value):
        self.__rules = value

    def add_rule(self, rule):
        self.__rules.append(rule)

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_upvotes(self):
        return self.__upvotes

    def get_downvotes(self):
        return self.__downvotes

    def set_upvotes(self, value):
        self.__upvotes = value

    def set_downvotes(self, value):
        self.__downvotes = value

    def get_rater(self):
        return self.__rater

    def set_rater(self, value):
        self.__rater = value
        
    def get_score(self):
        return self.rater.rate(self.upvotes, self.downvotes)

    rules = property(get_rules, set_rules)
    id = property(get_id, set_id)
    upvotes = property(get_upvotes, set_upvotes)
    downvotes = property(get_downvotes, set_downvotes)
    rater = property(get_rater, set_rater)
    score = property(get_score)
    
    def extract_info(self, input):
        """
        Applies the rules' chain to extract the piece of information.
        """
        log.debug('Applying ruled wrapper') #@UndefinedVariable
        result = input
        for rule in self.rules:
            result = rule.apply(result)
        return result
    
    def __repr__(self):
        return 'Wrapper(upvotes:%d, downvotes:%d, rules:%d)' % (self.upvotes,
                self.downvotes, len(self.rules))
