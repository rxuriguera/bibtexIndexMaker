
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
 

import unittest #@UnresolvedImport

from bibim.db.session import create_session
from bibim.db.mappers import (Publication,
                              QueryString,
                              Result,
                              Reference,
                              ReferenceField)
from bibim import references
from bibim.main.refmaker import ReferenceMakerDTO
from bibim.ir.search import SearchResult

from bibim.main.persistence import persist_dto

class TestDB(unittest.TestCase):

    def setUp(self):
        #self.session = create_session(sql_uri='sqlite:///:memory:')
        self.session = create_session()

        self.reference = references.Reference()
        self.reference.set_field('reference_id', 'Lmadsen99')
        self.reference.set_field('title', 'Some article title')
        self.reference.set_field('pages', '133--144')
        self.reference.set_field('journal', 'Some journal')
        self.reference.set_field('year', '1999')

        self.result1 = 'http://someurl1.com'
        self.result2 = 'http://someurl2.com'
        self.result3 = 'http://someurl3.com'
        
        self.dto = ReferenceMakerDTO()
        self.dto.used_result = SearchResult('resulta', 'http://resulta')
        self.dto.top_results = [SearchResult('resultb', 'http://resultb'),
                                SearchResult('resultc', 'http://resultc'), ]
        self.dto.query_strings = ['querya', 'queryb']
        self.dto.used_query = 'queryc'
        self.dto.entries = [self.reference]
        
        self.queries = [u'string1', u'string2', u'string3']
        pass

    def tearDown(self):
        pass

    def test_add_publication(self):
        publication = Publication(u'file.pdf')
        publication.query_strings = [QueryString(u'some query string'),
                                     QueryString(u'some other query')]
        publication.search_results = [Result('http://firsturl'),
                                      Result('http://secondurl')]
        ref = Reference()
        ref.set_result(Result(self.result3))
        publication.references = [ref]
        publication.references[0].fields = [ReferenceField('f1', u'v1', True),
                                            ReferenceField('f2', u'v2', False)]
        self.session.add(publication)
        self.session.commit()

    def test_add_publication_from_objects(self):
        publication = Publication('file.pdf')
        publication.add_query_strings([QueryString(string) for string in self.queries])
        publication.add_search_results([Result(self.result1),
                                        Result(self.result2),
                                        Result(self.result3)])
        self.session.commit()
    
    def test_query_db(self):
        all = self.session.query(Publication).all()
        self.failUnless(len(all) != 0)
        publication = all[0]
        self.failUnless(len(publication.query_strings) == 2)
        self.failUnless(len(publication.search_results) == 2)
        self.failUnless(len(publication.references) == 1)
        reference = publication.references[0]
        self.failUnless(len(reference.fields) == 5)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
