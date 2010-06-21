
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
from os.path import normpath, join, dirname

from bibim.util.beautifulsoup import BeautifulSoup
from bibim.util.helpers import ReferenceFormat

from bibim.main.factory import UtilFactory
from bibim.main.controllers import IEController
from bibim.ir.types import SearchResult
from bibim.references.reference import Reference


class TestIEController(unittest.TestCase):
        
    def setUp(self):
        factory = UtilFactory()
        self.iec = IEController(factory, ReferenceFormat.BIBTEX)
        self.top_results = [
            SearchResult('result01',
                'http://portal.acm.org/citation.cfm?id=507338.507355'),
            SearchResult('result01',
                'http://www.springerlink.com/index/D7X7KX6772HQ2135.pdf')]        
        self.empty_page = BeautifulSoup("<html><head/><body/></html>")
        self.page = self._get_soup('acm01.html')
        self.text = 'ss';
        
    def tearDown(self):
        pass

    def test_use_reference_wrappers_page_with_no_wrapper(self):
        references = self.iec._use_reference_wrappers('some_source',
                                                      self.empty_page,
                                                      self.text)
        self.failUnless(len(references) == 0)
    
    def xtest_use_reference_wrappers_page_with_wrapper(self):
        references = self.iec._use_reference_wrappers('http://portal.acm.org',
                                                      self.page,
                                                      self.text)
        self.failUnless(len(references) == 1)
    
    def test_format_reference_same_format(self):
        ref = Reference(format=ReferenceFormat.BIBTEX, entry='formatted entry')
        self.iec._format_reference(ref)
        self.failUnless(ref.get_entry() == 'formatted entry')
        
    def test_format_reference_different_format(self):
        ref = Reference()
        ref.set_field('reference_id', 'Lmadsen99')
        ref.set_field('title', 'Some article title')
        
        self.iec._format_reference(ref)
        
        self.failUnless(ref.get_entry().startswith('@article{Lmadsen99,'))
        self.failUnless(ref.get_format() == self.iec.format)

    def xtest_use_rule_wrappers(self):
        references = self.iec._use_rule_wrappers(u'some_source', 'test 2007 content', '')
        self.failUnless(len(references) == 1)
        self.failUnless(len(references[0].fields) == 3)
    
    def test_validate_reference_fields(self):
        ref = Reference()
        ref.set_field('title', 'Some article title')
        ref.set_field('year', '32')
        raw_text = "Some article title and something else"
        self.iec._validate_reference_fields(ref, raw_text)
        self.failUnless(ref.get_field('title').valid == True)
        self.failUnless(ref.get_field('year').valid == False)
    
    def _get_soup(self, file_name):
        file_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/wrappers/' + file_name)))
        file = open(file_path)
        soup = BeautifulSoup(file.read())
        file.close()
        return soup
    
    def test_set_value_guides(self):
        value_guides = self.iec.value_guides
        self.failUnless(len(value_guides) == 5)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
