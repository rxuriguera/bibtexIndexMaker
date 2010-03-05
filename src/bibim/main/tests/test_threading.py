
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
import Queue #@UnresolvedImport
import threading #@UnresolvedImport

from bibim.main.threads import ThreadRunner

class TestThread(threading.Thread):
    """
    This is just a test thread that 
    """
    def __init__(self, in_queue, out_queue, **kwargs):
        self.stop_event = threading.Event()
        self.in_queue = in_queue
        self.out_queue = out_queue
        threading.Thread.__init__(self)
        
    def run(self):
        while not self.stop_event.isSet():
            object = None
            if not self.in_queue.empty():
                try:
                    object = self.in_queue.get(False)
                except Queue.Empty:
                    continue
            if object:
                self.out_queue.put(self.getName())
                
    def join(self, timeout=None):
        self.stop_event.set()
        threading.Thread.join(self, timeout)                

class TestThreading(unittest.TestCase):

    def setUp(self):
        self.thread_type = TestThread
        self.in_queue = Queue.Queue(0)
        self.out_queue = Queue.Queue(0)
        self.tr = ThreadRunner(self.thread_type, self.in_queue,
                               self.out_queue)

    def tearDown(self):
        pass

    def test_set_pool_size(self):
        for i in range(2):
            self.in_queue.put(i)
        self.tr._set_pool_size()
        self.failUnless(self.tr.get_pool_size() == 1)
        
        # Let's add two more items
        for i in range(2):
            self.in_queue.put(i)
        self.tr._set_pool_size()
        self.failUnless(self.tr.get_pool_size() == 2)
        
        # Let's add 25 items
        for i in range(25):
            self.in_queue.put(i)
        self.tr._set_pool_size()
        self.failUnless(self.tr.get_pool_size() == 5)
    
    def test_run(self):
        for i in range(50):
            self.in_queue.put('somet_object')
        self.tr.run()
        self.failUnless(self.out_queue.qsize() == 50)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
