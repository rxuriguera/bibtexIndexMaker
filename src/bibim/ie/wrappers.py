
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

import simplejson #@UnresolvedImport

from bibim.db.session import create_session
from bibim.db import mappers
from bibim.ie.rules import RuleFactory


class Wrapper(object):
    """
    Defines base methods that must be implemented by Wrappers. This is an
    abstract class.
    """
       
    def extract_info(self, source, page):
        """
        Given a source and a page, searches in the page for relevant
        information. This method must be implemented by a subclass.
        """
        raise NotImplementedError()

    def _extract_text(self, tag=None):
        """
        Returns the concatenation of all the text from a given tag or None if
        not applicable. 
        """
        text = None
        if tag:
            text = tag.findAll(text=True)
        if text:
            text = ''.join(text).strip()
        return text
    
    def _find_in(self, tag, soup_list=None, attrs={}):
        """
        Finds a specific tag in a list of other tags. Returns a BeautifulSoup
        object.
        """
        tag_soup = None
        for soup in soup_list:
            tag_soup = soup.find(tag, attrs)
            if tag_soup:
                break        
        return tag_soup
            
        
class FieldWrapper(Wrapper):
    """
    Allows concrete field extraction from semi-structured 
    """
    _shortcuts = {}
    
    def extract_info(self, source, page):
        """
        Extracts a field from the given page. Strategy: if the source is
        defined in the shortcuts list, it tries to extract relevant
        information with the given strategy.
        Otherwise, it tries with all available strategies. 
        """
        info = self._extract_with_shortcut(source, page)
        if info:
            return info
        
        strategies = [method for method in dir(self) if method.startswith('_do_')]
        for strategy in strategies:
            strategy = getattr(self, strategy)
            info = strategy(page)
            if info:
                break
        return info
 
    def _extract_with_shortcut(self, source, page):
        """
        Checks if there is a strategy defined for the given source. If so, it
        tries to extract information with it.
        """
        info = None
        if source in self._shortcuts.keys():
            x = self._shortcuts[source]
            strategy = getattr(self, x)
            info = strategy(page)
        return info


class RuledWrapper(Wrapper):
    """
    This kind of wrapper is intended to extract information using a set of
    rules. For each field there will be a list of rules that will be applied
    in the given order. The result of a rule will be processed with the 
    following rule in the list.
    """
    def __init__(self):
        self.rules = {}

    def get_rules(self):
        return self.__rules
    
    def set_rules(self, value):
        self.__rules = value

    def add_rule(self, field, rule):
        self.__rules.setdefault(field, [])
        self.__rules[field].append(rule)
    
    def add_field_rules(self, field, rules):
        self.__rules[field] = rules
    
    def extract_info(self):    
        pass
    
    rules = property(get_rules, set_rules)
    

class RuledWrapperManager(object):
    """
    This class allows to store and retrieve ruled wrappers from the database
    as well as computing some statistics about the available wrappers.
    RuledWrappers used by this class must have a pattern that only consists
    of python built-in classes (i.e. strings, ints, lists, tuples, 
    dictionaries, etc.)
    """
    def __init__(self, session=None):
        if not session:
            session = create_session()
        self.session = session
    
    def persist_wrapper(self, url, wrapper):
        m_wrapper = mappers.Wrapper(url)
        self.session.add(m_wrapper)
        for field in wrapper.rules:
            m_field = mappers.WrapperField(field)
            m_wrapper.fields.append(m_field)
            
            rules = wrapper.rules[field]
            for rule, order in zip(rules, range(len(rules))):
                m_rule = mappers.WrapperRule(rule.__class__.__name__,
                                             simplejson.dumps(rule.pattern),
                                             order)
                m_field.rules.append(m_rule)
        self.session.commit()
        
    def get_wrapper(self, url):
        mapper = self._get_wrapper_mapper(url)
        if not mapper:
            return None
        
        rule_factory = RuleFactory()
        wrapper = RuledWrapper()
        for field in mapper.fields:
            for rule in field.rules:
                rule_type = rule.rule_type
                pattern = simplejson.loads(str(rule.pattern))
                r_rule = rule_factory.create_rule(rule_type, pattern)
                if r_rule:
                    wrapper.add_rule(field.name, r_rule)
                
        return wrapper
            
    def _get_wrapper_mapper(self, url):
        """
        Retrieves mappers from the database that will be used to create
        the examples
        """
        examples = {}
        query_results = (self.session.query(mappers.Wrapper).
                         filter(mappers.Wrapper.url.like(url + '%'))[0:1]) #@UndefinedVariable
        
        if query_results:
            return query_results.pop(0)
        else:
            return None
    
    def check_obsolete_wrappers(self):
        pass
