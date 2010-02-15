
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

from bibim.references.format import BibtexGenerator
from bibim.references.util import split_name

class TestBibtexGenerator(unittest.TestCase):
    
    def setUp(self):
        self.bg = BibtexGenerator()
        self.bg.setup_new_reference()
        self.refend = os.linesep + '}' + os.linesep
        
    def tearDown(self):
        pass

    def test_header(self):
        self.bg.generate_header()
        self.failUnless(self.bg.get_generated_reference() == 
            '@article{refid' + self.refend)

    def test_header_with_type_and_id(self):
        self.bg.generate_reference_type('inproceedings')
        self.bg.generate_reference_id('Sol04')
        self.failUnless(self.bg.get_generated_reference() == 
            '@inproceedings{Sol04' + self.refend)

    def test_title(self):
        self.bg.generate_title('This is a title')
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'title = {This is a title}' + self.refend
            ))
        
    def test_single_author(self):
        author = [split_name('Jack Jr. Brown Jovovic')]
        self.bg.generate_author(author)
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'author = {Jovovic, Jr. Brown, Jack}' + 
            self.refend
            ))

    def test_multiple_authors(self):
        author = [split_name('Jack Jr. Brown'), split_name('von Hammer, Hans')]
        self.bg.generate_author(author)
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'author = {Brown, Jr., Jack and von Hammer, Hans}' + 
            self.refend
            ))
        
    def test_year(self):
        self.bg.generate_year('1993')
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'year = 1993' + 
            self.refend
            ))
 
    def test_journal(self):
        self.bg.generate_journal('This is the name of a journal')
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'journal = {This is the name of a journal}' + self.refend
            ))        
                
    def test_pages(self):
        self.bg.generate_pages('33--44')
        self.failUnless(self.bg.get_generated_reference() == (
            '@article{refid,' + os.linesep + 
            'pages = {33--44}' + self.refend
            ))           
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
