
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

from bibim.references import Reference

class TestReference(unittest.TestCase):

    def setUp(self):
        self.ref = Reference()

    def tearDown(self):
        pass

    def test_set_and_get_field(self):
        self.ref.set_field('random_field', 'random_value')
        self.failUnless(self.ref.get_field('random_field').value == 'random_value')

    def test_get_fields(self):
        self.ref.set_field('rf01', 'rv01')
        self.ref.set_field('rf02', 'rv02')
        self.ref.set_field('rf03', 'rv04')
        self.failUnless(len(self.ref.get_fields()) == 3)
        self.failUnless(self.ref.get_fields() == ['rf01', 'rf02', 'rf03'])

    def test_set_and_get_entry(self):
        self.ref.set_entry('This is an entry')
        self.failUnless(self.ref.get_entry() == 'This is an entry')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
