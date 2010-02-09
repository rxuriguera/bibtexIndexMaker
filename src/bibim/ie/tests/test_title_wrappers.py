
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

from bibim.beautifulsoup import BeautifulSoup
from bibim.ie.tests import TestWrapper
from bibim.ie import TitleFieldWrapper


class TestTitleWrapper(TestWrapper):

    def setUp(self):
        self.tfw = TitleFieldWrapper()
        self.ieee = ('ieeexplore.ieee.org',
                     self._get_soup('ieee01.html'))
        self.citeseer = ('citeseerx.ist.psu.edu',
                         self._get_soup('citeseer01.html'))
        self.acm = ('portal.acm.org', self._get_soup('acm01.html'))
        self.springer = ('www.springerlink.com',
                         self._get_soup('springer01.html'))
        self.scienced = ('www.sciencedirect.com',
                         self._get_soup('sciencedirect01.html'))
        
    def tearDown(self):
        pass

    def test_extract_title_tag(self):
        self.failUnless(self.tfw._do_title_tag(self.acm[1]) == 
            ('Estimation of rotor angles of synchronous machines using '
            'artificial neural networks and local PMU-based quantities'))
    
    def test_extract_title_tag_with_text_removal(self):
        self.failUnless(self.tfw._do_title_tag(self.ieee[1]) == 
            ('A nonlinear reduced order observer for permanent magnet '
             'synchronousmotors'))
        self.failUnless(self.tfw._do_title_tag(self.citeseer[1]) == 
            ('Dynamic source routing in ad hoc wireless networks'))        

    def test_extract_strong_in_colspan_td(self):
        self.failUnless(self.tfw._do_strong_in_colspan_td(self.acm[1]) == 
            ('Estimation of rotor angles of synchronous machines using '
            'artificial neural networks and local PMU-based quantities'))

    def test_extract_h2_in_td(self):
        self.failUnless(self.tfw._do_h2_in_td(self.springer[1]) == 
            ('Selective Oxidation of Propane to Acrylic Acid on MoVNbTe Mixed '
             'Oxides Catalysts Prepared by Hydrothermal Synthesis'))

    def test_extract_div_with_class(self):
        self.failUnless(self.tfw._do_div_with_class(self.scienced[1]) == 
            ('Rigid-layer lattice vibrations and van der waals bonding in '
             'hexagonal MoS2'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
