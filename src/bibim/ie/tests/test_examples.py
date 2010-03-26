
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

from bibim.ie.examples import (Example, ExampleManager)

class TestExampleManager(unittest.TestCase):
    
    def setUp(self):
        self.example_manager = ExampleManager()
        self.url = 'http://portal.acm.org'

    def tearDown(self):
        pass

    def test_get_examples(self):
        examples = self.example_manager.get_examples(self.url)
        self.failUnless(len(examples) == 1)
        pass

class TestExample(unittest.TestCase):
    
    def xtest_get_source(self):
        example = Example(url="http://www.google.com")
        source01 = example.source
        source02 = example.source
        self.failUnless(source01)
        self.failUnless(id(source01) == id(source01))
