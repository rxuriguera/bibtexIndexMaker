
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
import os

from bibim.references import Reference
from bibim.references.format import ReferenceFormatter
from bibim.references.format import ReferenceFormatGenerator, BibtexGenerator

class TestReferenceFormatter(unittest.TestCase):

    def setUp(self):
        self.ref = Reference()
        self.ref.set_field('reference_id', 'Lmadsen99')
        self.ref.set_field('author', [{'first_name':'Lars',
                                 'last_name':'Madsen',
                                 'middle_name':'Lithen'}])
        self.ref.set_field('title', 'Some article title')
        self.ref.set_field('pages', '133--144')
        self.ref.set_field('journal', 'Some journal')
        self.ref.set_field('year', '1999')

        self.ref_formatter = ReferenceFormatter()
        self.format_generator = BibtexGenerator()
        

    def tearDown(self):
        pass

    def test_formatter(self):
        self.ref_formatter.format_reference(self.ref, self.format_generator)
        entry = self.ref.get_entry()
        self.failUnless(entry == ('@article{Lmadsen99,' + os.linesep + 
                                   'title = {Some article title},' + os.linesep + 
                                   'author = {Madsen, Lithen, Lars},' + os.linesep + 
                                   'year = 1999,' + os.linesep + 
                                   'journal = {Some journal},' + os.linesep + 
                                   'pages = {133--144}' + os.linesep + 
                                    '}' + os.linesep))
        
        self.failUnless(self.ref.format == self.format_generator.format)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
