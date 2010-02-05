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

from bibim.rce.extraction import PDFTextExtractor

class TestPDFTextExtractor(unittest.TestCase):


    def setUp(self):
        self.extractor = PDFTextExtractor()
        self.article01 = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/001.pdf')))
        self.article02 = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/002.pdf')))
        self.article03 = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/003.pdf')))
        self.scanned = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/scanned.pdf')))
        self.corrupt = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/extraction/corrupt.pdf')))

    def tearDown(self):
        pass

    def test_extract_non_existent_file(self):
        self.failUnlessRaises(IOError, self.extractor.extract, 'some_file.pdf')

    def test_extract(self):
        content = self.extractor.extract(self.article01)
        print content


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
