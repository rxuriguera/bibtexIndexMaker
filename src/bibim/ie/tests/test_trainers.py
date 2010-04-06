
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

from bibim.ie.trainers import (HTMLWrapperTrainer,
                               TooFewExamplesError)

from bibim.ie.examples import ExampleManager                                
from bibim.ie.rules import Rule, Ruler
from bibim.ie.validation import WrapperValidator

class MockExampleManager(ExampleManager):
    def get_examples(self, url, nexamples):
        sets = {}
        for i in 'abcde':
            sets[i] = set(range(random.randint(3, 50)))
        return sets

class MockRuler(Ruler):
    def rule(self, training):
        return Rule(random.randint(0, 10))     

class MockTrueValidator(WrapperValidator):
    def validate(self):
        return True

class MockFalseValidator(WrapperValidator):
    def validate(self):
        return False

class TestHTMLWrapperTrainer(unittest.TestCase):

    def setUp(self):
        self.htmlwt = HTMLWrapperTrainer(tp=0.8, vp=0.2, min=3)
        self.htmlwt.set_example_manager(MockExampleManager())

    def test_split_examples(self):
        examples = range(50)
        sets = self.htmlwt._split_examples(examples)
        self.failIf(not sets)
        self.failUnless(len(sets[0]) == 40)
        self.failUnless(len(sets[1]) == 10)

    def test_split_examples_too_few_examples(self):
        examples = range(10)
        self.htmlwt.set_min_examples(20)
        self.failUnlessRaises(TooFewExamplesError, self.htmlwt._split_examples,
                              examples)

    def test_train(self):
        self.htmlwt.set_rulers([MockRuler()])
        wrapper = self.htmlwt.train('some_url')
        pass
              
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

