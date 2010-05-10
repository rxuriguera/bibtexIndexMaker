
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
from sqlalchemy import (DateTime, #@UnresolvedImport
                        Column, #@UnresolvedImport
                        Integer, #@UnresolvedImport
                        Float, #@UnresolvedImport
                        Boolean, #@UnresolvedImport
                        String, #@UnresolvedImport
                        Unicode, #@UnresolvedImport
                        ForeignKey) #@UnresolvedImport

from sqlalchemy.orm import relation #@UnresolvedImport

from sqlalchemy.ext.declarative import declarative_base #@UnresolvedImport

Base = declarative_base()

class WrapperRule(Base):
    __tablename__ = 'wrapper_rules'
    
    id = Column(Integer, primary_key=True)
    rule_type = Column(String, nullable=False)
    pattern = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    wrapper_id = Column(Integer, ForeignKey('wrappers.id'))

    def __init__(self, rule_type, pattern, order=0):
        self.rule_type = rule_type
        self.pattern = pattern
        self.order = order
    
    def __repr__(self):
        return 'WrapperRule(type: %s,pattern: %s,order: %d)' % (self.rule_type,
                                                                self.pattern,
                                                                self.order)


class Wrapper(Base):
    __tablename__ = 'wrappers'
    
    id = Column(Integer, primary_key=True)
    rules = relation(WrapperRule, order_by=WrapperRule.order)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    collection_id = Column(Integer, ForeignKey('wrapper_collections.id'))

    def __init__(self, rules=[]):
        self.rules = rules
        self.upvotes = 0
        self.downvotes = 0
        self.score = 0.0
    
    def add_rule_by_info(self, rule_type='', pattern='', order=0):
        rule = WrapperRule(rule_type, pattern, order)
        rule.wrapper_id = self.id
        self.rules.append(rule)
    
    def add_rule(self, rule):
        self.rules.append(rule)
        
    def upvote(self, vote=1):
        self.upvotes += vote
        self._compute_score()
    
    def downvote(self, vote=1):
        self.downvotes += vote
        self._compute_score()
    
    def _compute_score(self):
        self.score = self.upvotes - self.downvotes
    
    def __repr__(self):
        return 'Wrapper(upvotes: %d,downvotes: %d,rules: %d)' % (self.upvotes,
            self.downvotes,
            len(self.rules))


class WrapperCollection(Base):
    """
    Groups wrappers depending on the URL and fields for which they can be used
    """
    __tablename__ = 'wrapper_collections'
    
    id = Column(Integer, primary_key=True)
    url = Column(Unicode, nullable=False)
    field = Column(Unicode, nullable=False)
    wrappers = relation(Wrapper, order_by=Wrapper.score.desc())

    def __init__(self, url='', field=''):
        self.url = url
        self.field = field
        self.wrappers = []
        
    def __repr__(self):
        return 'WrapperCollection(url: %s,field: %s)' % (self.url, self.field)


class Person(Base):
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode, nullable=True)
    middle_name = Column(Unicode, nullable=True)
    last_name = Column(Unicode, nullable=True)
    
    def __init__(self, first_name='', middle_name='', last_name=''):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def to_name_dict(self):
        return {'first_name':self.first_name, 'middle_name':self.middle_name,
                'last_name':self.last_name}
    
    def __repr__(self):
        return "Person(first: %s,middle: %s,last: %s)" % (self.first_name,
                                                          self.middle_name,
                                                          self.last_name)    


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    refefence_id = Column(Integer, ForeignKey('references.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relation(Person, order_by=Person.id)
    
    def __init__(self, person):
        self.person = person

    def to_name_dict(self):
        return self.person.to_name_dict()

    def __repr__(self):
        return "Author"    
    
    
class Editor(Base):
    __tablename__ = 'editors'
    
    id = Column(Integer, primary_key=True)
    refefence_id = Column(Integer, ForeignKey('references.id'))
    person_id = Column(Integer, ForeignKey('people.id'))    
    person = relation(Person, order_by=Person.id)
    
    def __init__(self, person):
        self.person = person

    def to_name_dict(self):
        return self.person.to_name_dict()

    def __repr__(self):
        return "Editor"    


class ReferenceField(Base):
    __tablename__ = 'reference_fields'    
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    value = Column(Unicode, nullable=False)
    valid = Column(Boolean, default=True)
    reference_id = Column(Integer, ForeignKey('references.id'))
    
    def __init__(self, name, value, valid):
        self.name = name
        self.value = value
        self.valid = valid

    def __repr__(self):
        return "ReferenceField(name: %s, value: %s, valid: %s)" % (self.name,
                                                                   self.value,
                                                                   self.valid)         
     
     
class Reference(Base):
    __tablename__ = 'references'
    
    id = Column(Integer, primary_key=True)
    fields = relation(ReferenceField, order_by=ReferenceField.id,
                      backref='reference')
    validity = Column(Float, default=0.0)
    authors = relation(Author, order_by=Author.id)
    editors = relation(Editor, order_by=Editor.id)

    extraction_id = Column(Integer, ForeignKey('extractions.id'))
    
    def __init__(self, fields=[], validity=0.0, authors=[], editors=[], extraction_id=0):
        self.fields = fields
        self.validity = validity
        self.authors = authors
        self.editors = editors
        self.extraction_id = extraction_id
    
    def add_field(self, name, value, valid):
        self.fields.append(ReferenceField(name, value,
                                          valid))

    def add_author_by_name(self, first_name, middle_name, last_name):
        self.authors.append(Author(Person(first_name, middle_name, last_name)))

    def add_editor_by_name(self, first_name, middle_name, last_name):
        self.editors.append(Editor(Person(first_name, middle_name, last_name)))
        
    def add_author(self, author):
        self.authors.append(author)        

    def add_editor(self, editor):
        self.editors.append(editor)            
            
    def __repr__(self):
        return ("Reference(fields: %d, authors: %d, editors: %d, validity: %f)" 
                % (len(self.fields), len(self.authors), len(self.editors),
                   self.validity))


class Extraction(Base):
    __tablename__ = 'extractions'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now())
    file_path = Column(Unicode, default=u'')
    result_url = Column(Unicode, default=u'')
    query_string = Column(Unicode, default=u'')
    
    references = relation(Reference, order_by=Reference.id,
                          backref='extraction')

    def __init__(self, file_path=u'', result_url=u'', query_string=u''):
        self.file_path = file_path
        self.result_url = result_url
        self.query_string = query_string
    
    def add_reference(self):
        self.references.append(Reference(extraction_id=self.id))
    
    def __repr__(self):
        return ('Extraction(file_path: %s, result_url: %s, query_string: %s, '
                'timestamp: %s)' % (self.file_path, self.result_url,
                                    self.query_string, self.timestamp))
