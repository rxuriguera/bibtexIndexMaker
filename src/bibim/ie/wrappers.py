
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

# TODO: Load from config file
MAX_WRAPPERS = 50

class Wrapper(object):
    """
    Defines methods to extract information using a set of
    rules. Each wrapper will have a list of rules that will be applied
    in the given order. Rules used by this class mu   st have a pattern that only 
    consist of python built-in classes (i.e. string, int, list, tuple, 
    dictionary, etc.)
    """
    def __init__(self):
        self.rules = []

    def get_rules(self):
        return self.__rules
    
    def set_rules(self, value):
        self.__rules = value

    def add_rule(self, rule):
        self.__rules.append(rule)

    rules = property(get_rules, set_rules)
    
    def extract_info(self, input):
        """
        Applies the rules' chain to extract the piece of information.
        """
        result = input
        for rule in self.rules:
            result = rule.apply(result)
        return result


class RatedWrapper(Wrapper):
    def __init__(self, upvotes=0, downvotes=0, rater=None):
        super(RatedWrapper, self).__init__()
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.rater = rater

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

    upvotes = property(get_upvotes, set_upvotes)
    downvotes = property(get_downvotes, set_downvotes)
    rater = property(get_rater, set_rater)

    def get_score(self):
        return self.rater.rate(self.upvotes, self.downvotes)
        

class WrapperManager(object):
    """
    This class allows to store and retrieve ruled wrappers from the database
    as well as computing some statistics about the available wrappers.
    """
    def __init__(self, session=None):
        if not session:
            session = create_session()
        self.session = session
        
    def commit(self):
        self.session.commit()
    
    def persist_wrapper(self, url, field, wrapper):
        """
        Adds the given wrapper to the wrapper collection described by the url
        and field
        """
        # Get the given collection
        m_collection = self.get_wrapper_collection(url, field, True)
        m_wrapper = mappers.Wrapper()
        m_collection.wrappers.append(m_wrapper)
        
        for rule, order in zip(wrapper.rules, range(len(wrapper.rules))):
            m_rule = mappers.WrapperRule(rule.__class__.__name__,
                                        simplejson.dumps(rule.pattern),
                                        order)
            m_wrapper.rules.append(m_rule)
        self.session.commit()

    def get_wrapper_collections(self, url=u'%', field=u'%'):
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field))) #@UndefinedVariable
        return collection
       
    def get_wrapper_collection(self, url, field=u'%', create=False):
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field)). #@UndefinedVariable
                      first())
        if not collection and create and field != u'%':
            collection = mappers.WrapperCollection(url, field)
            self.session.add(collection)
        return collection
     
    def get_wrappers(self, url, field):
        collection = self.get_wrapper_collection(url, field)
        if not collection:
            return []
        
        rule_factory = RuleFactory()
        wrappers = []
        for m_wrapper in collection.wrappers:
            wrapper = Wrapper()
            for rule in m_wrapper.rules:
                rule_type = rule.rule_type
                pattern = simplejson.loads(str(rule.pattern))
                r_rule = rule_factory.create_rule(rule_type, pattern)
                if r_rule:
                    wrapper.add_rule(r_rule)
            wrappers.append(wrapper)
        return wrappers
            
    def _get_wrapper_mappers(self, url):
        """
        Retrieves the mappers from the database that will be used to create
        the examples
        """
        query_results = (self.session.query(mappers.WrapperCollection).
                         filter(mappers.WrapperCollection.url.like(url + '%')) #@UndefinedVariable
                         [:MAX_WRAPPERS])
        
        self.wrapper_mappers = query_results
    
    def check_obsolete_wrappers(self):
        pass
