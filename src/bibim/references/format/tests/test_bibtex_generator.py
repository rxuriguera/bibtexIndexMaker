
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
import re

from bibim.references.format.generator import BibtexGenerator
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
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*',
                            self.refend])  
        self.failUnless(re.search(expected, result))
        
    def test_header_with_type_and_id(self):
        self.bg.generate_reference_type('inproceedings')
        self.bg.generate_reference_id('Sol04')
        self.failUnless(self.bg.get_generated_reference() == 
            '@inproceedings{Sol04' + self.refend)

    def test_title(self):
        self.bg.generate_title('This is a title')
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                            'title = {This is a title}',
                            self.refend])  
        self.failUnless(re.search(expected, result))

    def test_single_author(self):
        author = [split_name('Jack Jr. Brown Jovovic')]
        self.bg.generate_author(author)
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                            'author = {Jovovic, Jr. Brown, Jack}',
                            self.refend])  
        self.failUnless(re.search(expected, result))

    def test_multiple_authors(self):
        author = [split_name('Jack Jr. Brown'), split_name('von Hammer, Hans')]
        self.bg.generate_author(author)
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                            'author = {Brown, Jr., Jack and von Hammer, Hans}',
                            self.refend])  
        self.failUnless(re.search(expected, result))
        
    def test_year(self):
        self.bg.generate_year('1993')
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                             'year = 1993',
                             self.refend])  
        self.failUnless(re.search(expected, result))        

    def test_journal(self):
        self.bg.generate_journal('This is the name of a journal')
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                             'journal = {This is the name of a journal}',
                             self.refend])  
        self.failUnless(re.search(expected, result))    
 
    def test_pages(self):
        self.bg.generate_pages('33--44')
        result = self.bg.get_generated_reference()
        expected = ''.join(['@article{.*,', os.linesep,
                             'pages = {33--44}',
                             self.refend])  
        self.failUnless(re.search(expected, result))           
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
