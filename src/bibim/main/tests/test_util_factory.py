
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

from bibim.main.factory import UtilFactory, UtilCreationError
from bibim.util.helpers import FileFormat

class TestUtilFactory(unittest.TestCase):

    def setUp(self):
        self.uf = UtilFactory()

    def tearDown(self):
        pass

    def test_create_extractor(self):
        extractor = self.uf.create_extractor(FileFormat.PDF, FileFormat.TXT) #@UnusedVariable
        self.assertRaises(UtilCreationError,
            self.uf.create_extractor, FileFormat.TXT, FileFormat.PDF)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
