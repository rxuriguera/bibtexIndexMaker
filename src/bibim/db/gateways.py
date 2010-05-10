
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

from datetime import datetime
from time import sleep
import re
import simplejson #@UnresolvedImport
from sqlalchemy import desc #@UnresolvedImport

from bibim import log
from bibim.db import mappers
from bibim.db.session import create_session
from bibim.ie.types import (Example,
                            Wrapper,
                            Extraction)
from bibim.ie.rules import RuleFactory
from bibim.ir.types import SearchResult
from bibim.references.reference import Reference
from bibim.util.browser import (Browser,
                                BrowserError)
from bibim.util.beautifulsoup import BeautifulSoup

class Gateway(object):
    def __init__(self, session=None):
        if not session:
            session = create_session()
        self.session = session
        
    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()

class ReferenceGateway(Gateway):
    """
    This class allows to store and retrieve references from the database
    """
    
    def find_reference_by_id(self, id):
        if not id:
            raise ValueError
        
        log.debug('Querying the database. Reference with id %s' % str(id)) #@UndefinedVariable
        m_reference = (self.session.query(mappers.Reference).
                       filter(mappers.Reference.id == id).one())
        
        if not m_reference:
            return None
        
        log.debug('Creating new reference') #@UndefinedVariable
        reference = Reference()
        reference.id = m_reference.id
        reference.validity = m_reference.validity
        
        log.debug('Adding fields') #@UndefinedVariable
        for m_field in m_reference.fields:
            reference.set_field(m_field.name, m_field.value, m_field.valid)
        
        log.debug('Adding authors') #@UndefinedVariable
        authors = []
        for m_author in m_reference.authors:
            authors.append(m_author.to_name_dict())
        if authors:
            reference.set_field(u'author', authors, True)
        
        log.debug('Adding editors') #@UndefinedVariable
        editors = []
        for m_editor in m_reference.editors:
            editors.append(m_editor.to_name_dict())
        if editors:
            reference.set_field(u'editor', editors, True)
        
        return reference
    
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

    def new_reference(self):
        reference = mappers.Reference()
        self.session.add(reference)
        return reference


class ExtractionGateway(Gateway):
    """
    This class allows to store and retrieve extractions from the database
    """
    def persist_extraction(self, extraction):
        """
        Adds new extractions to the database.
        """
        log.debug("Persisting extraction") #@UndefinedVariable
        m_extraction = mappers.Extraction()
        self.session.add(m_extraction)
            
        m_extraction.file_path = unicode(extraction.file_path)
        m_extraction.query_string = unicode(extraction.used_query)
        if extraction.used_result:
            m_extraction.result_url = unicode(extraction.used_result.url)

        m_references = ReferenceGateway(self.session).persist_references(extraction.entries)
        for m_reference in m_references:
            m_extraction.references.append(m_reference)
        
        return m_extraction
    
    def find_extraction_by_id(self, e_id):
        m_extraction = self.session.query(mappers.Extraction).filter_by(id=e_id).one()
        extraction = Extraction()
        
        extraction.id = m_extraction.id
        extraction.used_query = m_extraction.query_string
        extraction.used_result = SearchResult("", m_extraction.result)
        return extraction

    def find_extractions(self):
        m_extractions = (self.session.query(mappers.Extraction).
                         order_by(desc(mappers.Extraction.timestamp))[:1000])
        return m_extractions
    
    def new_extraction(self):
        extraction = mappers.Extraction()
        self.session.add(extraction)
        return extraction
    

class ExampleGateway(Gateway):
    """
    """
    
    last_request = datetime.now()
    
    def __init__(self, session=None, max_examples=5, max_examples_from_db=15, seconds_between_requests=5):
        super(ExampleGateway, self).__init__(session)
        self.max_examples = max_examples
        self.max_examples_from_db = max_examples_from_db
        self.seconds_between_requests = seconds_between_requests
    
    def get_examples(self, nexamples, url=u'', min_validity='0.5'):
        """
        Creates examples from the available references in the database. The
        references to use can be filtered depending on the validity and the 
        url.
        
        This method returns a dictionary of fields whose value is a list of
        examples with values for that field.
        """
        
        nexamples = nexamples if nexamples <= self.max_examples else self.max_examples
        
        url = unicode(url)
        examples = {}
        m_results = (self.session.query(mappers.Extraction, mappers.Reference).
                     filter(mappers.Extraction.id == mappers.Reference.extraction_id).
                     filter(mappers.Reference.validity >= min_validity).
                     filter(mappers.Extraction.result_url.like(url + '%')). #@UndefinedVariable
                     order_by(desc(mappers.Reference.validity)).all()
                     [:self.max_examples_from_db])

        for m_extraction, m_result in m_results:
            content = self._get_content(m_extraction.result_url)

            # Check if the contents of the database are still valid
            if not self._check_still_valid(m_result, content, min_validity):
                continue
            
            fields = [field for field in m_result.fields if field.valid]
            for field in fields:
                examples.setdefault(field.name, [])
                example = Example(field.value, content, m_extraction.result_url,
                                  field.valid, m_result.id)
                examples[field.name].append(example)
        
            # Break if we already have enough examples for all of the fields
            if min(map(len, examples.values())) >= nexamples:
                break    
           
        return examples

    def _get_content(self, url):
        """
        This method looks for the content of an example's URL. In order not to
        overload the server, it sleeps for some time between multiple calls. 
        """
        time_to_sleep = (self.seconds_between_requests - 
                        (datetime.now() - self.last_request).seconds)
        if time_to_sleep > 0:
            sleep(time_to_sleep)
        
        content = None
        try:
            content = Browser().get_page(url)
            content = self._clean_content(content)
            content = BeautifulSoup(content) if content else None
        except BrowserError as e:
            log.error('Error retrieving page %s: %s' % (url, #@UndefinedVariable
                                                        e.error))
        self.last_request = datetime.now()
        return content

    def _clean_content(self, content):
        if not content:
            return None
        content = content.replace('\n', '')
        content = content.replace('\r', '')
        content = content.replace('\t', '')
        return content
    
    def _check_still_valid(self, mapper, content, min_validity):
        """
        It checks if the information to be extracted is really present within
        the contents. If it doesn't, then it updates the database so the
        corresponding records won't be used again.
        """
        
        # In case the content could not be extracted, don't update the database
        if not content:
            return False
        
        # For each piece of information, check if it exists in the contents.
        # At this point, we don't care about its location, but if it
        # can be found.
        not_found = 0.0
        for field in mapper.fields:
            found = content.find(text=re.compile(field.value))
            if not found:
                log.info('Field %s with value %s cannot be found anymore in %d' #@UndefinedVariable
                         % (field.name, field.value, mapper.id))
                field.valid = False
                not_found += 1
        
        # Recompute validity
        validity = 1 - (not_found / len(mapper.fields)) 
        if validity < min_validity:
            log.info('Reference "%d" marked as invalid from now on.' % #@UndefinedVariable
                      mapper.id)
            mapper.validity = validity
            return False
    
        return  True   
    
    
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

    def persist_wrappers(self, url, field, wrappers):
        wrappers = list(wrappers)
        m_wrappers = []
        for wrapper in wrappers:
            m_wrappers.append(self.persist_wrapper(url, field, wrapper))
        return m_wrappers

    def persist_wrapper(self, url, field, wrapper):
        """
        Adds the given wrapper to the wrapper collection described by the url
        and field
        """
        collection = self.find_wrapper_collection(url, field, True)
        m_wrapper = mappers.Wrapper()
        collection.wrappers.append(m_wrapper)
        
        m_wrapper.upvotes = wrapper.upvotes
        m_wrapper.downvotes = wrapper.downvotes
        m_wrapper.score = wrapper.score
        
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
        m_wrapper.score = wrapper.get_score()
        
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
        collections = (self.session.query(mappers.WrapperCollection).
                      filter(mappers.WrapperCollection.url.like(url + '%')). #@UndefinedVariable
                      filter(mappers.WrapperCollection.field.like(field)). #@UndefinedVariable
                      order_by(mappers.WrapperCollection.field))
        return collections

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

    def new_wrapper_collection(self):
        collection = mappers.WrapperCollection()
        self.session.add(collection)
        return collection

    def new_wrapper(self):
        """
        Returns a new wrapper mapper
        """
        wrapper = mappers.Wrapper()
        self.session.add(wrapper)
        return wrapper

    def check_obsolete_wrapper_collections(self):
        pass
    
