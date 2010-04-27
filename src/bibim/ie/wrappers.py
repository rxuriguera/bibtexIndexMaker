
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

from bibim.ie.rating import AverageRater


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
        result = input
        for rule in self.rules:
            result = rule.apply(result)
        return result
    
    def __repr__(self):
        return 'Wrapper(upvotes=%d,downvotes=%d,rules=%d)' % (self.upvotes,
                                                              self.downvotes,
                                                              len(self.rules))


class WrapperManager(object):
    """
    This class allows to store and retrieve ruled wrappers from the database
    as well as computing some statistics about the available wrappers.
    """
    def __init__(self, session=None, max_wrappers=50):
        if not session:
            session = create_session()
        self.session = session
        self.max_wrappers = max_wrappers

    def get_max_wrappers(self):
        return self.__max_wrappers

    def set_max_wrappers(self, value):
        self.__max_wrappers = value
        
    max_wrappers = property(get_max_wrappers, set_max_wrappers)

    def persist_wrapper(self, url, field, wrapper):
        """
        Adds the given wrapper to the wrapper collection described by the url
        and field
        """
        collection = self.find_wrapper_collection(url, field, True)
        m_wrapper = mappers.Wrapper()
        collection.wrappers.append(m_wrapper)
        
        for rule, order in zip(wrapper.rules, range(len(wrapper.rules))):
            m_wrapper.rules.append(self._persist_rule(rule, order))

    def _persist_rule(self, rule, order):
        return mappers.WrapperRule(rule.__class__.__name__,
                                   simplejson.dumps(rule.pattern),
                                   order) 

    def update_wrapper(self, wrapper):
        if not wrapper.id:
            raise ValueError 
        
        m_wrapper = self.find_wrapper_by_id(wrapper.id)
        if not m_wrapper:
            raise ValueError
        
        m_wrapper.upvotes = wrapper.upvotes
        m_wrapper.downvotes = wrapper.downvotes
        m_wrapper.score = wrapper.score
        
        for rule, order in zip(wrapper.rules, range(len(wrapper.rules))):
            try:
                m_rule = m_wrapper.rules[order]
                m_rule.type = rule.__class__.__name__
                m_rule.pattern = simplejson.dumps(rule.pattern)
            except IndexError:
                m_wrapper.rules.append(self._persist_rule(rule, order))
        
    def find_wrapper_by_id(self, w_id):
        return self.session.query(mappers.Wrapper).filter_by(id=w_id).one()
        
    def find_wrapper_collections(self, url=u'%', field=u'%'):
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field))) #@UndefinedVariable
        return collection
       
    def find_wrapper_collection(self, url, field=u'%', create=False):
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field)). #@UndefinedVariable
                      first())
        if not collection and create and field != u'%':
            collection = mappers.WrapperCollection(url, field)
            self.session.add(collection)
        return collection
     
    def get_wrappers(self, url='%', field='%'):
        """
        Gets all the wrappers from a given collection.
        """
        collection = self.find_wrapper_collection(url, field)
        if not collection:
            return []
        
        rule_factory = RuleFactory()
        wrappers = []
        for m_wrapper in collection.wrappers:
            wrapper = Wrapper()
            
            wrapper.id = m_wrapper.id
            wrapper.upvotes = m_wrapper.upvotes
            wrapper.downvotes = m_wrapper.downvotes
            
            for rule in m_wrapper.rules:
                pattern = simplejson.loads(str(rule.pattern))
                r_rule = rule_factory.create_rule(rule.rule_type, pattern)
                if r_rule:
                    wrapper.add_rule(r_rule)
            wrappers.append(wrapper)
        return wrappers
            
    def _get_wrapper_mappers(self, url):
        """
        Retrieves the mappers from the database that will be used to create
        the wrappers
        """
        query_results = (self.session.query(mappers.WrapperCollection).
                         filter(mappers.WrapperCollection.url.like(url + '%')) #@UndefinedVariable
                         [:self.max_wrappers])
        
        self.wrapper_mappers = query_results
    
    def check_obsolete_wrapper_collections(self):
        pass
    
