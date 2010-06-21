
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

from bibim.util.beautifulsoup import BeautifulSoup 

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_soup_from_None(self):
        self.failUnlessRaises(TypeError, BeautifulSoup, None)

    def test_create_soup_from_empty_string(self):
        try:
            soup = BeautifulSoup('')
            self.failIf(soup is None)
        except:
            self.fail("Soup of empty string shouldn't raise an exception")
    
    def test_get_text_from_non_leaf(self):
        soup = BeautifulSoup('<html><body>'
                             '<div>'
                             '<span>Text 01</span>'
                             '<span>Text 02</span>'
                             '</div>'
                             '</html></body>')
        text = soup.findAll('div', text=True)
        self.failUnless(len(text) == 2)
        self.failUnless(text[0] == u'Text 01')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
