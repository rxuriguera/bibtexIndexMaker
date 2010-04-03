
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

from bibim.main.validation import ReferenceValidator
from bibim.references import Reference

class TestReferenceValidator(unittest.TestCase):

    def setUp(self):
        self.rv = ReferenceValidator(fields={'title':0.75, 'author':0.25})
        self.text = """
        Neurocomputing 35 (2000) 3}26

        Class separability estimation and incremental learning using 
        boundary methods Jose-Luis Sancho *, William E. Pierson , 
        Batu Ulug , H AnmH bal R. Figueiras-Vidal , Stanley C. Ahalt 
        ATSC-DI, Escuela Politecnica Superior. Universidad Carlos III 
        Leganes-Madrid, Spain & & Department of Electrical Engineering, 
        he Ohio State University Columbus, OH 43210, USA Received 7 
        January 1999; revised 5 April 1999; accepted 10 April 2000

        Abstract In this paper we discuss the use of boundary methods 
        (BMs) for distribution analysis. We view these methods as tools 
        which can be used to extract useful information from sample 
        distributions. We believe that the information thus extracted has 
        utility for a number of applications, but in particular we discuss 
        the use of BMs as a mechanism for class separability estimation and 
        as an aid to constructing robust and e$cient neural networks (NNs) 
        to solve classi"cation problems. In the "rst case, BMs can 
        establish the utili...
        """


    def tearDown(self):
        pass

    def test_validate_correct_reference(self):
        correct_ref = Reference()
        correct_ref.set_field('author', [{'first_name':'Jose-Luis',
                                          'last_name':'Sancho',
                                          'middle_name':''}])
        correct_ref.set_field('title', ('Class separability estimation and '
            'incremental learning using boundary methods'))        
        
        self.rv.validate_reference(correct_ref, self.text)
        x = correct_ref.validity
        self.failUnless(correct_ref.validity)
    
    def test_validate_missing_fields_reference(self):
        missing_field_ref = Reference()
        missing_field_ref.set_field('title', ('Class separability estimation '
            ' and incremental learning using boundary methods'))
        
        self.rv.validate_reference(missing_field_ref, self.text)
        x = missing_field_ref.validity
        self.failUnless(missing_field_ref.validity == 0.0)

    def test_validate_incorrect_reference(self):
        incorrect_ref = Reference()
        incorrect_ref.set_field('title', ('some arbitrary text'))
        incorrect_ref.set_field('author', [{'first_name':'Jose-Luis',
                                            'last_name':'Sancho',
                                            'middle_name':''}])
        self.rv.validate_reference(incorrect_ref, self.text)
        x = incorrect_ref.validity
        self.failUnless(incorrect_ref.validity < 0.5)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
