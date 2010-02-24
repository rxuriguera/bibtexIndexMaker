
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
from bibim.util.helpers import (FileFormat,
                                ReferenceFormat)

from bibim.main.factory import UtilFactory
from bibim.main.controllers import (RCEController,
                                    IRController,
                                    IEController)
from bibim.ir.search import SearchResult
from bibim.references import Reference


class TestRCEController(unittest.TestCase):
    some_text = """Neurocomputing 35 (2000) 3}26

        Class separability estimation and incremental learning using 
        boundary methods Jose-Luis Sancho *, William E. Pierson , 
        Batu Ulug , H AnmH bal R. Figueiras-Vidal , Stanley C. Ahalt 
        ATSC-DI, Escuela Politecnica Superior. Universidad Carlos III 
        Leganes-Madrid, Spain & & Department of Electrical Engineering, 
        he Ohio State University Columbus, OH 43210, USA Received 7 
        January 1999; revised 5 April 1999; accepted 10 April 2000

        Abstract In this paper we discuss the use of boundary methods 
        (BMs) for distribution analysis. We view these methods as tools 
        which can be used to extract useful information from sample 
        distributions. We believe that the information thus extracted has 
        utility for a number of applications, but in particular we discuss 
        the use of BMs as a mechanism for class separability estimation and 
        as an aid to constructing robust and e$cient neural networks (NNs) 
        to solve classi"cation problems. In the "rst case, BMs can 
        establish the utili...
    """
        
    def setUp(self):
        factory = UtilFactory()
        self.rcec = RCEController(factory)
        self.pdf = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/article.pdf')))

    def tearDown(self):
        pass

    def test_extract_content_from_non_existent_file(self):
        content = self.rcec.extract_content('somefile.pdf', FileFormat.TXT)
        self.failUnless(content is None)
    
    def test_extract_content_to_invalid_target_format(self):
        content = self.rcec.extract_content(self.pdf, 'invalid format')
        self.failUnless(content is None)
            
    def test_extract_content_from_pdf(self):
        content = self.rcec.extract_content(self.pdf, FileFormat.TXT)
        self.failUnless(content is not None)
    
    def test_get_query_strings(self):
        strings = self.rcec.get_query_strings(self.some_text)
        self.failUnless(len(strings) == 5)


class TestIRController(unittest.TestCase):
        
    def setUp(self):
        factory = UtilFactory()
        self.irc = IRController(factory)
        self.queries = ['"We view these methods as tools which can be used"',
                        '"believe that the information thus extracted"',
                        '"can be used to extract useful information"']

    def tearDown(self):
        pass

    def test_get_top_results_wrong_search_engine(self):
        results = self.irc.get_top_results(self.queries, -1)
        self.failUnless(not results)
    
    def test_get_top_results(self):
        results = self.irc.get_top_results(self.queries)
        self.failUnless(results)    
    
    
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
        
    def tearDown(self):
        pass

    def test_extract_reference(self):
        #self.iec.extract_reference(self.top_results)
        pass
    
    def test_use_reference_wrappers_page_with_no_wrapper(self):
        references = self.iec._use_reference_wrappers('some_source',
                                                      self.empty_page)
        self.failUnless(len(references) == 0)
    
    def test_use_reference_wrappers_page_with_wrappter(self):
        references = self.iec._use_reference_wrappers('http://portal.acm.org',
                                                      self.page)
        self.failUnless(len(references) == 1)
    
    def test_use_field_wrappers_no_wrapper_available(self):
        references = self.iec._use_field_wrappers('some_source',
                                                  self.empty_page)
        self.failUnless(len(references) == 0)

    def test_use_field_wrappers_wrapper_available(self):
        references = self.iec._use_field_wrappers('some_source',
                                                  self.page)
        self.failUnless(len(references) == 1)
        self.failUnless(references[0].get_field('title').
            value.startswith('Estimation of rotor angles'))
            
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

    def _get_soup(self, file_name):
        file_path = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/wrappers/' + file_name)))
        file = open(file_path)
        soup = BeautifulSoup(file.read())
        file.close()
        return soup
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
