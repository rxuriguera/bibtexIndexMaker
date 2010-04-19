
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
from sqlalchemy import (Table, #@UnresolvedImport
                        DateTime, #@UnresolvedImport
                        Column, #@UnresolvedImport
                        Integer, #@UnresolvedImport
                        Float, #@UnresolvedImport
                        Boolean, #@UnresolvedImport
                        String, #@UnresolvedImport
                        Unicode, #@UnresolvedImport
                        MetaData, #@UnresolvedImport
                        ForeignKey, #@UnresolvedImport
                        Text)#@UnresolvedImport

from sqlalchemy.orm import (relation, #@UnresolvedImport
                            mapper, #@UnresolvedImport
                            relation,
                            backref)#@UnresolvedImport

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
    
    def add_rule(self, rule):
        self.rules.append(rule)


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
    
    def __repr__(self):
        return "<Person('%s','%s','%s')>" % (self.first_name,
                                             self.middle_name,
                                             self.last_name)    


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    refefence_id = Column(Integer, ForeignKey('extracted_references.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relation(Person, order_by=Person.id)
    
    def __init__(self, person):
        self.person = person

    def __repr__(self):
        return "<Author>"    
    
    
class Editor(Base):
    __tablename__ = 'editors'
    
    id = Column(Integer, primary_key=True)
    refefence_id = Column(Integer, ForeignKey('extracted_references.id'))
    person_id = Column(Integer, ForeignKey('people.id'))    
    person = relation(Person, order_by=Person.id)
    
    def __init__(self, person):
        self.person = person

    def __repr__(self):
        return "<Editor>"    


class ReferenceField(Base):
    __tablename__ = 'reference_fields'    
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    value = Column(Unicode, nullable=False)
    valid = Column(Boolean, default=True)
    reference_id = Column(Integer, ForeignKey('extracted_references.id'))
    
    def __init__(self, name, value, valid):
        self.name = name
        self.value = value
        self.valid = valid

    def __repr__(self):
        return "<ReferenceField('%s','%s','%s')>" % (self.name, self.value,
                                                     self.valid)         
     
     
class ExtractedReference(Base):
    __tablename__ = 'extracted_references'
    
    id = Column(Integer, primary_key=True)
    fields = relation(ReferenceField, order_by=ReferenceField.id,
                      backref='reference')
    validity = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.now())
    file_id = Column(Integer, ForeignKey('files.id'))
    authors = relation(Author, order_by=Author.id)
    editors = relation(Editor, order_by=Editor.id)
    result = Column(String, nullable=False)
    query_string = Column(Unicode, nullable=False)
    
    def add_field(self, name, value, valid):
        self.fields.append(ReferenceField(name, value,
                                          valid))

    def add_author(self, author):
        self.authors.append(author)        

    def add_editor(self, editor):
        self.editors.append(editor)            
            
    def __repr__(self):
        return "<ExtractedReference('%s','%s')>" % (self.query_string, self.result)
    
    
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    file_path = Column(Unicode, nullable=True)
    references = relation(ExtractedReference, order_by=ExtractedReference.id,
                          backref='file')
    
    def __init__(self, file_path=''):
        self.file_path = file_path

    def add_reference(self, reference):
        self.references.append(reference)
        
    def __repr__(self):
        return "<File('%s')>" % self.file        

