# Copyright 2010 Ramon Xuriguera
#
# BibtexIndexMaker RCE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BibtexIndexMaker RCE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker RCE. If not, see <http://www.gnu.org/licenses/>.

import unittest #@UnresolvedImport
from os.path import join, dirname, normpath
import subprocess #@UnresolvedImport

from bibim.rce.extraction import ExtractionError, PDFTextExtractor

class TestPDFTextExtractor(unittest.TestCase):


    def setUp(self):
        self.extractor = PDFTextExtractor()
        self.scanned = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/scanned.pdf')))
        self.corrupt = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/corrupt.pdf')))
        self.article = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/article.pdf')))
        self.document = self.extractor.extract(self.article)

    def tearDown(self):
        pass

    def test_extract_non_existent_file(self):
        self.failUnlessRaises(IOError, self.extractor.extract, 'some_file.pdf')

    def test_extract_scanned_file(self):
        self.failUnlessRaises(ExtractionError, self.extractor.extract,
                              self.scanned)
        
    def test_extract_corrupt_file(self):
        self.failUnlessRaises(ExtractionError, self.extractor.extract,
                              self.corrupt)

    def test_metadata_extraction(self):
        self.failUnless(self.document.get_metadata_field('Title') == ('PII: '
            'S0925-2312(00)00293-9'))
        self.failUnless(self.document.get_metadata_field('CreationDate') == 
            '20001019095743')

    def test_content_extraction(self):
        self.failUnless(self.document.content.count(('In this paper we discuss'
            ' the use of boundary methods')) == 1)
        self.failUnless(self.document.content.count(('Army Research Lab '
            'Programming Environment and Training program')) == 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
