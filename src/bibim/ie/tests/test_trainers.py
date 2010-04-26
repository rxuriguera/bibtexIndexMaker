
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
                               TooFewExamplesError)

from bibim.db.session import create_session
from bibim.ie.examples import (Example, ExampleManager, HTMLExampleManager)                                
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
            sets[field] = set([Example('v_%d' % i, 'c_%d' % i) for i in 
                               range(random.randint(min, max))])
        return sets   


class MockRule(Rule):
    def apply(self, input):  
        return str(input) + '_r' + self.pattern


class MockRuler(Ruler):
    def rule(self, training):
        return [MockRule(str(random.randint(0, 10))),
                MockRule(str(random.randint(10, 20)))]     
    
    
class TestWrapperTrainer(unittest.TestCase):
    def setUp(self):
        self.wt = WrapperTrainer([MockRuler()], min=3)
        self.nsets = 5
        
        self.example_sets = MockExampleManager()._get_examples(self.nsets,
                                                               5, 10)
        
    def test_train_too_few_examples(self):
        self.wt.set_min_examples(20)
        self.failUnlessRaises(TooFewExamplesError, self.wt.train,
                              self.example_sets)

    def test_train(self):
        self.wt.rulers = [MockRuler(), MockRuler()]
        wrappers = self.wt.train(self.example_sets['a'])
        self.failUnless(len(wrappers) == 4)
        self.failUnless(len(wrappers[0].rules) == 2)
    
    def test_get_new_example_set(self):
        example_set = [Example('v01', 'c01'),
                       Example('v02', 'c02'),
                       Example('v03', 'c03')]
        example_set = self.wt._get_new_example_set(MockRule('xx'), example_set)
        self.failUnless(len(example_set) == 3)
        self.failUnless(example_set[0].content == 'c01_rxx')

    def test_get_rule_sets(self):
        example_set = [Example('v01', 'c01'),
                       Example('v02', 'c02'),
                       Example('v03', 'c03')]
        rules = self.wt._get_rule_sets([MockRuler(), MockRuler()],
                                       example_set)
        self.failUnless(len(rules) == 4)
        length_bools = map(lambda x: len(x) == 2, rules)
        self.failUnless(length_bools.count(False) == 0)

              
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

