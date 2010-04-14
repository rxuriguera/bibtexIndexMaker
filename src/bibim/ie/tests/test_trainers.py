
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
import random #@UnresolvedImport

from os.path import join, dirname, normpath

from bibim.util.config import BibimConfig
from bibim.ie.trainers import (WrapperTrainer,
                               HTMLWrapperTrainer,
                               TooFewExamplesError)

from bibim.db.session import create_session
from bibim.ie.examples import (ExampleManager, HTMLExampleManager)                                
from bibim.ie.rules import Rule, Ruler


class MockExampleManager(ExampleManager):
    def get_examples(self, url, nexamples):
        return self._get_examples(5, nexamples, nexamples + 15)
    
    def _get_examples(self, nsets, min, max):
        sets = {}
        fields = 'abcdefghijklmnopqrstuvwxyz'
        nsets = nsets if nsets < len(fields) else len(fields) - 1
        for i in range(nsets):
            field = fields[i]
            sets[field] = set(range(random.randint(min, max)))
        return sets   
    

class MockRuler(Ruler):
    def rule(self, training):
        return Rule(str(random.randint(0, 10)))     


class TestWrapperTrainer(unittest.TestCase):
    def setUp(self):
        self.wt = WrapperTrainer(MockExampleManager(), [MockRuler()], min=3)
        self.nsets = 5
        
        self.example_sets = MockExampleManager()._get_examples(self.nsets,
                                                               5, 10)
        
    def test_train_too_few_examples(self):
        self.wt.set_min_examples(20)
        self.failUnlessRaises(TooFewExamplesError, self.wt.train,
                              self.example_sets)

    def test_train(self):
        wrapper = self.wt.train(self.example_sets)
        self.failUnless(len(wrapper.rules) == self.nsets)
              
              
class TestHTMLWrapperTrainer(unittest.TestCase):
    def setUp(self):
        self.wt = HTMLWrapperTrainer(min=2)
        self.wt.example_manager = HTMLExampleManager(create_session(
            sql_uri='sqlite:///../../../../tests/fixtures/wrappers/test_db.db',
            debug=True))
        #self.wt.example_manager = MockExampleManager()
        #self.wt.rulers = [MockRuler()]
        self.nsets = 3

    def test_train(self):
        wrapper01 = self.wt.train('file:///home/rxuriguera/enlistments/bibtexIndexMaker/tests/fixtures/wrappers/acm')
        self.failUnless(len(wrapper01.rules) == self.nsets)
        
        wrapper02 = self.wt.train('file:///home/rxuriguera/enlistments/bibtexIndexMaker/tests/fixtures/wrappers/springer')
        self.failUnless(len(wrapper02.rules) == self.nsets)
        
        wrapper03 = self.wt.train('file:///home/rxuriguera/enlistments/bibtexIndexMaker/tests/fixtures/wrappers/sciencedirect')
        self.failUnless(len(wrapper03.rules) == self.nsets)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

