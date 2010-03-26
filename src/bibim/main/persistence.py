
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


from bibim.db.session import create_session
from bibim.db import mappers

class Persistor(object):
    def __init__(self, session=create_session()):
        self.session = session

    def get_session(self):
        return self.__session

    def set_session(self, value):
        self.__session = value

    session = property(get_session, set_session)

    def commit(self):
        self.session.commit()
        
    def persist_dto(self, dto):
        """
        Stores all the information of a processed file to the database.
        """
        publication = mappers.Publication(file=unicode(dto.file))
        self.session.add(publication)
    
        publication.add_query_strings([mappers.QueryString(query) for query in dto.query_strings])
        publication.add_search_results([mappers.Result(result.url) for result in dto.top_results])
        
        if dto.used_query:
            publication.add_query_strings(mappers.QueryString(dto.used_query,
                                                              True))
        
        if dto.used_result:
            publication.add_search_results(mappers.Result(dto.used_result.url,
                                                          True))
        
        # One single publication can have more than one entry (e.g. inbook + book)
        for entry in dto.entries:
            reference = mappers.Reference()
            for field in entry.get_fields():
                field = entry.get_field(field)
                
                # Authors and editors are special cases as they are not represented
                # as simple strings but dictionaries
                if field.name == 'author':
                    self.persist_authors(field.value, reference)
                
                elif field.name == 'editor':
                    self.persist_editors(field.value, reference)
                    
                else:
                    reference.add_field(field.name, field.value, field.valid)
                    
            publication.add_reference(reference)


    def persist_authors(self, authors, reference):
        """
        Adds an author to the authors db table.
        """
        for author in authors:
            author = self.get_person(author)
            reference.add_author(mappers.Author(author))
            
    def persist_editors(self, editors, reference):
        """
        Adds an editor to the editors db table.
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
