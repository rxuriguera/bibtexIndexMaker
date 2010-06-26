
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

from bibim.ie.context import ContextResolver
from bibim.util.beautifulsoup import BeautifulSoup
from bibim.util.helpers import ContentCleaner

html = """
       <html>
       <head></head>
       <body>
           <table>
               <tr>
                   <td>Field 01:</td>
                   <td>Value 01</td>
               </tr>
               <tr>
                   <td>Field 02:</td>
                   <td>Value 02</td>
               </tr>
               <tr>
                   <td>Field 03 <sup>33</sup</td>
                   <td>Value 03</td>
               </tr>               
           </table>
       </body>
       </html> 
       """


class ContextResolverTest(unittest.TestCase):
    def setUp(self):
        self.cr = ContextResolver()
        self.soup = ContentCleaner().clean_content(html)
        self.element01 = self.soup.find('td', text='Value 01').parent
        self.element02 = self.soup.find('td', text='Value 03').parent
        
    def tearDown(self):
        pass

    def test_get_context(self):
        context = self.cr.get_context(self.element01)
        self.failUnless(context[u'Field 01:'] == 1)
        
    def test_get_tree_context(self):
        context = self.cr.get_context(self.element02)
        self.failUnless(context[u'Field 03'] == 1)
        self.failUnless(context[u'33'] == 1)

    def test_merge_contexts(self):
        context01 = {u'Field 01:':1}
        context02 = {u'Field 01:':3, u'Field 02:':1, u'Field 03:':4}
        merged = self.cr.merge_context(context01, context02)
        self.failUnless(merged == {u'Field 02:': 1, u'Field 01:': 4,
                                   u'Field 03:': 4})
    
    def test_clean_context(self):
        context = {'a':2, 'b':3, 'c':1,
                   'this string is quite long. yes indeed':4}
        result = self.cr.clean_context(context)
        self.failUnless(result == {'a':2, 'b':3})
        
    def test_get_top_words(self):
        context = {u'a':3, 'b':5, 'c':1, u'd':2, 'e':4}
        expected = ['b', 'e', u'a']
        result = self.cr.get_top_strings(context, 3)
        self.failUnless(result == expected)
        
    def test_check_context(self):
        context01 = {'a':3, 'b':5, 'c':1, 'd':2, 'e':4}
        context02 = {'a':1, 'x':3}
        result = self.cr.check_context(context01, context02)
        self.failUnless(result)
        
        context02 = {'x':3}
        result = self.cr.check_context(context01, context02)
        self.failIf(result)
        
        context01 = {}
        result = self.cr.check_context(context01, context02)
        self.failUnless(result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
