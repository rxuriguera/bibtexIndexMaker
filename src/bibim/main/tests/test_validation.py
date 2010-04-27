
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

from bibim.main.validation import (ReferenceValidator,
                                   ValidatorFactory,
                                   WithinTextValidator,
                                   RegexValidator)
from bibim.references import Reference

class TestReferenceValidator(unittest.TestCase):

    def setUp(self):
        self.rv = ReferenceValidator(weights={'title':0.75, 'author':0.25})

    def tearDown(self):
        pass

    def test_validate_correct_reference(self):
        correct_ref = Reference()
        correct_ref.set_field('author', [{'first_name':'Jose-Luis',
                                          'last_name':'Sancho',
                                          'middle_name':''}], True)
        correct_ref.set_field('title', ('Class separability estimation and '
            'incremental learning using boundary methods'), True)        
        
        self.rv.validate(correct_ref)
        x = correct_ref.validity
        self.failUnless(correct_ref.validity == 1.0)

    def test_validate_incorrect_reference(self):
        incorrect_ref = Reference()
        incorrect_ref.set_field('title', ('some arbitrary text'), False)
        incorrect_ref.set_field('author', [{'first_name':'Jose-Luis',
                                            'last_name':'Sancho',
                                            'middle_name':''}], True)
        self.rv.validate(incorrect_ref)
        x = incorrect_ref.validity
        self.failUnless(incorrect_ref.validity < 0.5)


class TestRegexValidator(unittest.TestCase):
    def setUp(self):
        self.validator = RegexValidator('(\d{4})')
    
    def test_validate(self):
        result = self.validator.validate('2003')
        self.failUnless(result)
        
        result = self.validator.validate('abcd')
        self.failIf(result)


class TestWithinTextValidator(unittest.TestCase):
    def setUp(self):
        self.validator = WithinTextValidator()
        
    def test_validate(self):
        result = self.validator.validate('apple', 'I like apples')
        self.failUnless(result)
        
        result = self.validator.validate('apple', 'I am a PC')
        self.failIf(result)

class TestValidatorFactory(unittest.TestCase):
    
    def test_create_validator(self):
        validator = ValidatorFactory.create_validator('WithinTextValidator')
        self.failUnless(validator.__class__.__name__ == 'WithinTextValidator')
        
        validator = ValidatorFactory.create_validator('RegexValidator', 'ptrn')
        self.failUnless(validator.__class__.__name__ == 'RegexValidator')
        self.failUnless(validator.pattern == 'ptrn')
        
        validator = ValidatorFactory.create_validator('RegexValidator',
                                                      *['ptrn2'])
        self.failUnless(validator.__class__.__name__ == 'RegexValidator')
        self.failUnless(validator.pattern == 'ptrn2')
        
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
