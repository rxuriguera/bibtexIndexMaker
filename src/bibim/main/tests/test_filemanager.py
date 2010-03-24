
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
from os.path import join, dirname, normpath

from bibim.main.files import FileManager

class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.fm = FileManager()
        self.dir = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/main/filemanager')))
        self.file = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'fixtures/main/filemanager/a.bib')))
        
    def tearDown(self):
        pass

    def test_get_files_dir_path(self):
        files = self.fm.get_files_list(self.dir, 'bib')
        self.failUnless(len(files) == 2)
        files = self.fm.get_files_list(self.dir, 'pdf')
        self.failUnless(len(files) == 2)
        files = self.fm.get_files_list(self.dir)
        self.failUnless(len(files) == 4)
    
    def test_get_files_file_path(self):
        files = self.fm.get_files_list(self.file)
        self.failUnless(len(files) == 1)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
