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

from bibim.document import Document


class TestPDFTextExtractor(unittest.TestCase):

    def setUp(self):
        self.document = Document()
        
    def tearDown(self):
        pass

    def test_metadata_fields(self):
        self.document.set_metadata_field('Name', 'Document name')
        self.failUnless(self.document.get_metadata_field('Name') == 
                        'Document name')
    
    def test_available_metadata(self):
        self.document.set_metadata_field('Name', 'Document name')
        self.document.set_metadata_field('CreationDate', 'Today')
        fields = self.document.available_metadata
        self.failUnless(len(fields) == 2)
        self.failUnless(fields.count('Name') == 1)
        self.failUnless(fields.count('CreationDate') == 1)

    def test_content(self):
        self.document.content = "Some text content"
        self.failUnless(self.document.content == "Some text content")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
