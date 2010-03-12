
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

from sqlalchemy import (Table, #@UnresolvedImport
                        DateTime, #@UnresolvedImport
                        Column, #@UnresolvedImport
                        Integer, #@UnresolvedImport
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

class QueryString(Base):
    __tablename__ = 'query_strings'

    id = Column(Integer, primary_key=True)
    query = Column(Unicode, nullable=False)
    publication_id = Column(Integer, ForeignKey('publications.id'))
    
    def __init__(self, query):
        self.query = query

    def __repr__(self):
        return "<QueryString('%s')>" % self.query         


class Result(Base):
    __tablename__ = 'search_results'
    
    id = Column(Integer, primary_key=True)
    url = Column(String , nullable=False)
    publication_id = Column(Integer, ForeignKey('publications.id'))
    
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<WebResult('%s')>" % self.url         

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
    refefence_id = Column(Integer, ForeignKey('publication_references.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relation(Person, order_by=Person.id)
    
    def __init__(self, person):
        self.person = person

    def __repr__(self):
        return "<Author>"    
    
    
class Editor(Base):
    __tablename__ = 'editors'
    
    id = Column(Integer, primary_key=True)
    refefence_id = Column(Integer, ForeignKey('publication_references.id'))
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
    reference_id = Column(Integer, ForeignKey('publication_references.id'))
    
    def __init__(self, name, value, valid):
        self.name = name
        self.value = value
        self.valid = valid

    def __repr__(self):
        return "<ReferenceField('%s','%s','%s')>" % (self.name, self.value,
                                                     self.valid)         
     
     
class Reference(Base):
    __tablename__ = 'publication_references'
    
    id = Column(Integer, primary_key=True)
    fields = relation(ReferenceField, order_by=ReferenceField.id,
                      backref='reference')
    # The url of the page from which the reference was extracted
    result_id = Column(Integer, ForeignKey('search_results.id'))
    publication_id = Column(Integer, ForeignKey('publications.id'))
    authors = relation(Author, order_by=Author.id)
    editors = relation(Editor, order_by=Editor.id)
    search_result = relation(Result)
    
    def set_result(self, result):
        if type(result) is str:
            result = Result(result)
        self.search_result = result
        self.search_result.publication = self.publication
        
    def add_field(self, name, value, valid):
        self.fields.append(ReferenceField(name, value,
                                          valid))

    def add_author(self, author):
        self.authors.append(author)        

    def add_editor(self, editor):
        self.editors.append(editor)            
            
    def __repr__(self):
        return "<Reference>"
    
    
class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    file = Column(Unicode, nullable=True)
    search_results = relation(Result, order_by=Result.id,
                           backref='publication')
    query_strings = relation(QueryString, order_by=QueryString.id,
                             backref='publication')
    references = relation(Reference, order_by=Reference.id,
                          backref='publication')
    
    def __init__(self, file=''):
        self.file = file

    def add_search_results(self, results):
        if type(results) is not list:
            results = [results]
            
        for result in results:
            self.search_results.append(result)

    def add_query_strings(self, query_strings):
        if type(query_strings) is not list:
            query_strings = [query_strings]
            
        for query_string in query_strings:
            self.query_strings.append(query_string)
        
    def add_reference(self, reference):
        self.references.append(reference)
        
    def __repr__(self):
        return "<Publication('%s')>" % self.file        
