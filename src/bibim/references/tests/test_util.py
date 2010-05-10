'''
Created on 16/04/2010

@author: rxuriguera
'''
import unittest #@UnresolvedImport


from bibim.references.util import split_name

class TestUtil(unittest.TestCase):

    def test_split_name(self):
        name = "Last, J."
        result = split_name(name)
        self.failUnless(result['first_name'] == 'J.')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == '')
        
        name = "Last, Middle, First"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == 'Middle')
        
        name = "First Middle Last"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == 'Middle')
        
        name = "First Last"
        result = split_name(name)
        self.failUnless(result['first_name'] == 'First')
        self.failUnless(result['last_name'] == 'Last')
        self.failUnless(result['middle_name'] == '')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
