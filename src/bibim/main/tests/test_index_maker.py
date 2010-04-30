
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
from datetime import datetime

from bibim.main.entry import IndexMaker
from bibim.references import Reference

class TestIndexMaker(unittest.TestCase):


    def setUp(self):
        self.bim = IndexMaker()
        self.file = normpath(join(dirname(__file__), ('../../../../tests/'
                                     'articles/009.pdf')))
        self.path = normpath('/home/rxuriguera/Escriptori/lattice')

    def tearDown(self):
        pass

    def test_index_maker(self):
        start = datetime.now() 
        ref = self.bim.make_index(self.file)
        now = datetime.now() 
        print 'Temps: ', now - start


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
