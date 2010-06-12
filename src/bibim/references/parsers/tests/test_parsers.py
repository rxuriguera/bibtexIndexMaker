
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

from os.path import join, dirname, normpath
import unittest #@UnresolvedImport

from bibim.references.parsers.bibtex import BibtexParser


class TestBibtexParser(unittest.TestCase):

    def setUp(self):
        self.parser = BibtexParser()
        self.single = self._get_reference('single.bib')
        self.multiple = self._get_reference('multiple.bib')
        self.macros = self._get_reference('macros.bib')
        self.wrong01 = self._get_reference('wrong_format01.bib')
        self.wrong02 = self._get_reference('wrong_format02.bib')

    def tearDown(self):
        pass

    def test_check_format(self):
        self.failUnless(self.parser.check_format(self.single))
        self.failUnless(not self.parser.check_format(self.wrong01))
        self.failUnless(not self.parser.check_format(self.wrong02))
        pass
    
    def test_expand_macros(self):
        ref = self.parser.preprocess(self.macros)
        self.failUnless(self.parser.parse_entry(ref)['title'] == 
            ('Performance Analysis of Bayes Classification, Support Vector '
             'Machines'))
    
    def test_parse_single_entry(self):
        ref = self.parser.preprocess(self.single)
        parsed = self.parser.parse_entry(ref)
        self.failUnless(parsed['title'] == ('MaltParser: A Language-'
            'Independent System for Data-Driven Dependency Parsing'))
        self.failUnless(parsed['journal'] == ('Natural Language Engineering '
            'Journal'))
    
    def test_parse_multiple_entries(self):
        ref = self.parser.preprocess(self.multiple)
        ref = self.parser.split_source(ref)
        self.failUnless(len(ref) == 2, 'The file contains two entries')
        parsed01 = self.parser.parse_entry(ref[0])
        self.failUnless(parsed01['title'] == ('Improvements to Penalty-Based'))
        parsed02 = self.parser.parse_entry(ref[1])
        self.failUnless(parsed02['title'] == ('Na\\"ive Bayes Techniques'))
        pass
    
    def _get_reference(self, file_name):
        ref_path = '../../../../../tests/fixtures/references/bibtex/'
        file_path = normpath(join(dirname(__file__), (ref_path + file_name)))
        file = open(file_path)
        ref = file.read()
        file.close()
        return ref

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
