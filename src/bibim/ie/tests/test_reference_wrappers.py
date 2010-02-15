'''
Created on 15/02/2010

@author: rxuriguera
'''
import unittest #@UnresolvedImport

from bibim.ie.tests import TestWrapper
from bibim.ie import ReferenceWrapper

class TestReferenceWrappers(TestWrapper):

    def setUp(self):
        self.rw = ReferenceWrapper()
        self.acm = ('http://portal.acm.org', self._get_soup('acm01.html'))

    def tearDown(self):
        pass

    def test_invalid_source(self):
        self.failUnless(not self.rw.extract_info('some_source', None))

    def test_portal_acm_wrapper(self):
        reference = self.rw.extract_info(self.acm[0], self.acm[1])
        self.failUnless(reference.startswith('@article{1316105,'))
        self.failUnless(reference.endswith('}'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
