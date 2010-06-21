
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

from bibim.util.helpers import FileFormat
from bibim.main.factory import UtilFactory
from bibim.main.controllers import RCEController


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
        self.failUnless(len(strings) > 0)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
