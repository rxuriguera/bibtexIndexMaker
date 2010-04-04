
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
from os.path import join, dirname, normpath

from bibim.ie.examples import (Example,
                               ExampleManager,
                               HTMLExample,
                               HTMLExampleManager)


class TestHTMLExampleManager(unittest.TestCase):
    
    def setUp(self):
        self.example_manager = HTMLExampleManager()
        self.url = (u'file://' + normpath(join(dirname(__file__),
                    ('../../../../tests/fixtures/wrappers/'))))
        
    def tearDown(self):
        pass

    def test_get_examples(self):
        examples = self.example_manager.get_examples(self.url, 1)
        self.failIf(not examples)
    
    def test_get_content(self):
        content = self.example_manager._get_content(self.url + '/acm01.html')
        self.failIf(not content)
    
