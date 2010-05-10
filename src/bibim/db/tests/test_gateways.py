
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

from bibim.db.gateways import (ExampleGateway,
                               ReferenceGateway)
from bibim.references.reference import Reference

class TestExampleGateway(unittest.TestCase):
    def setUp(self):
        self.eg = ExampleGateway()

    def tearDown(self):
        pass

    def xtestGetExamples(self):
        examples = self.eg.get_examples(2, "http://zetcode.com", 0.5)
        self.eg.session.flush()
        self.eg.session.close()
        

class TestReferenceGateway(unittest.TestCase):
    def setUp(self):
        self.eg = ReferenceGateway()

    def test_find_by_id(self):
        reference = self.eg.find_reference_by_id(2)
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
