
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
from bibim.db import mappers
from bibim.db.session import create_session
from bibim.ie.types import (Example,
                            Wrapper,
                            Extraction)
from bibim.ie.rules import RuleFactory
from bibim.ir.search import SearchResult

# TODO: move to config file
MAX_EXAMPLES_FROM_DB = 15

class Gateway(object):
    def __init__(self, session=None):
        if not session:
            session = create_session()
        self.session = session
        
    def commit(self):
        self.session.commit()


class ReferenceGateway(Gateway):
    """
    This class allows to store and retrieve references from the database
    """
    
    def find_reference_by_id(self, id):
        pass
    
    def persist_references(self, references):
        references = list(references)
        m_references = []
        for reference in references:
            m_references.append(self.persist_reference(reference))
        return m_references

    def persist_reference(self, reference):
        m_reference = mappers.Reference()
        self.session.add(m_reference)
        
        m_reference.validity = reference.validity
                
        for field in reference.get_fields():
            field = reference.get_field(field)
            
            if not field.value:
                continue
            
            # Authors and editors are special cases as they are not 
            # represented as simple strings but dictionaries
            if field.name == 'author':
                self.persist_authors(field.value, m_reference)
            
            elif field.name == 'editor':
                self.persist_editors(field.value, m_reference)
                
            else:
                m_reference.add_field(field.name, field.value, field.valid)
        return m_reference
        
    def persist_authors(self, authors, reference):
        """
        Adds an author to the authors database table.
        """
        for author in authors:
            author = self.get_person(author)
            reference.add_author(mappers.Author(author))
            
    def persist_editors(self, editors, reference):
        """
        Adds an editor to the editors database table.
        """
        for editor in editors:
            editor = self.get_person(editor)
            reference.add_editor(mappers.Editor(editor))
    
    def get_person(self, person):
        # Check if person already exists in the database.
        new_person = self.session.query(mappers.Person).filter_by(
                        first_name=person['first_name'],
                        middle_name=person['middle_name'],
                        last_name=person['last_name']).first()
        
        if not new_person:
            new_person = mappers.Person(person['first_name'],
                                        person['middle_name'],
                                        person['last_name'])
        return new_person


class ExtractionGateway(Gateway):
    """
    This class allows to store and retrieve extractions from the database
    """
    def persist_extraction(self, extraction):
        """
        Adds new extractions to the database.
        """
        m_extraction = mappers.Extraction()
        self.session.add(m_extraction)
            
        m_extraction.file_path = unicode(extraction.file_path)
        m_extraction.query_string = unicode(extraction.used_query)
        if extraction.used_result:
            m_extraction.result = unicode(extraction.used_result.url)

        ReferenceGateway(self.session).persist_references(extraction.references)
        
        return m_extraction
    
    def find_extraction_by_id(self, e_id):
        m_extraction = self.session.query(mappers.Extraction).filter_by(id=e_id).one()
        extraction = Extraction()
        
        extraction.id = m_extraction.id
        extraction.used_query = m_extraction.query_string
        extraction.used_result = SearchResult("", m_extraction.result)
        return extraction


class ExampleGateway(Gateway):
    """
    """
    def get_examples(self, url, min_validity):
        """
        Retrieves mappers from the database that will be used to create
        the examples
        """
        url = unicode(url)
        
        examples = {}
        
        """
        
        m_results = (self.session.query(mappers.Reference).
                     filter(mappers.Reference.validity == 0.2)#@UndefinedVariable
                     #join(mappers.Reference).
                        #filter(mappers.Reference.validity >= min_validity).
                        #filter(mappers.Extraction.result_url.like(url + '%')). #@UndefinedVariable
                        #order_by(mappers.Reference.validity).all()
                        [:MAX_EXAMPLES_FROM_DB])
        """
        m_results = (self.session.query(mappers.Extraction).
                    filter(mappers.Extraction.result_url.like('aaa'))); #@UndefinedVariable
         
         
        for m_result in m_results:
            fields = [field for field in m_result.fields if field.valid]
            for field in fields:
                examples.setdefault(field.name, [])
                example = Example(field.value, None, m_result.url)
                examples[field.name].append(example)
                
        return examples
    

class WrapperGateway(Gateway):
    """
    This class allows to store and retrieve ruled wrappers from the database
    """
    def __init__(self, session=None, max_wrappers=50):
        super(WrapperGateway, self).__init__(session)
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
        
        return m_wrapper

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
        url = unicode(url)
        field = unicode(field)
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field))) #@UndefinedVariable
        return collection

    def find_wrapper_collection(self, url, field=u'%', create=False):
        url = unicode(url)
        field = unicode(field)
        collection = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field)). #@UndefinedVariable
                      first())
        if not collection and create and field != u'%':
            collection = mappers.WrapperCollection(url, field)
            self.session.add(collection)
        return collection

    def get_wrappers(self, url=u'%', field=u'%'):
        """
        Gets all the wrappers from a given collection.
        """
        url = unicode(url)
        field = unicode(field)
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
    
