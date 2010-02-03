
# Copyright 2010 Ramon Xuriguera
# 
# BibtexIndexMaker IR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BibtexIndexMaker IR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker IR.  If not, see <http://www.gnu.org/licenses/>.


import unittest #@UnresolvedImport
from os.path import join, dirname, normpath

from bibim.ir.beautifulSoup import BeautifulSoup
from bibim.ir.search import GoogleSearch, ScholarSearch


class TestGoogleSearch(unittest.TestCase):

    def setUp(self):
        self.gs = GoogleSearch('query text')
        fixture_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/search/googleSearch.html')))
        self.fixture = open(fixture_path)
        self.page = BeautifulSoup(self.fixture.read())

    def tearDown(self):
        self.fixture.close()

    def test_extract_info(self):
        search_info = self.gs._extract_info(self.page)
        self.failUnless(search_info['to'] == 30, 'Wrong "to" field')
        self.failUnless(search_info['from'] == 21, 'Wrong "from" field')
        self.failUnless(search_info['total'] == 136000, 'Wrong "total" field')


class TestScholarSearch(unittest.TestCase):
    
    def setUp(self):
        self.ss = ScholarSearch('query text')
        fixture_path = normpath(join(dirname(__file__), ('../../../../tests/'
            'fixtures/search/scholarSearch.html')))
        self.fixture = open(fixture_path)
        self.page = BeautifulSoup(self.fixture.read())
        self.results = self.ss._extract_raw_results_list(self.page)

    def tearDown(self):
        self.fixture.close()

    def test_extract_info(self):
        search_info = self.ss._extract_info(self.page)
        self.failUnless(search_info['to'] == 10, 'Wrong "to" field')
        self.failUnless(search_info['from'] == 1, 'Wrong "from" field')
        self.failUnless(search_info['total'] == 1470000, 'Wrong "total" field')
    
    def test_extract_desc(self):
        desc = self.ss._extract_description(self.results[0])
        self.failUnless(desc.startswith('Witten and Frank\'s textbook'),
                        'Description does not start were it should')
        self.failUnless(desc.endswith('representation that can  ...'),
                        'Description does not end were it should')

    def test_extract_authors(self):
        authors = self.ss._extract_authors(self.results[0])
        self.failUnless(authors == ['IH Witten', 'E Frank'])
        
    def test_extract_authors_ellipsis_removal(self):
        authors = self.ss._extract_authors(self.results[1])
        self.failUnless(authors == ['T Hastie', 'R Tibshirani', 'J Friedman'])

    def test_extract_year(self):
        year = self.ss._extract_year(self.results[0])
        self.failUnless(year == '2002')
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
