
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

import threading #@UnresolvedImport
import Queue #@UnresolvedImport

from bibim import log
from bibim.main.refmaker import ReferenceMaker
from bibim.util.helpers import ReferenceFormat
from bibim.ie.types import Extraction

MAX_THREADS = 5
MIN_CLIENTS_PER_THREAD = 2


class ThreadRunner(threading.Thread):
    """
    This class will create a thread pool and run tasks on its threads. 
    It is extremely important that the thread removes objects from the 
    'input_queue' as it runs. This is because the runner waits for the 
    'input_queue' to be empty before asking the threads to stop.
    Threads should put their results (if any) in the 'output_queue'.
    """
    def __init__(self, thread_class, in_queue, out_queue, **kwargs):
        """
        It creates a ThreadRunner that will run multiple threads of
        thread_class.
        'kwargs' allows us to pass a variable number of keyworded parameters
        to the threads. 
        """
        threading.Thread.__init__(self)
        self.name = 'Runner'
        self.thread_class = thread_class
        self.in_queue = in_queue
        self.out_queue = out_queue
        self._thread_pool = []
        self._pool_size = 0
        self._thread_args = kwargs
        self.finished = False

    def get_thread_class(self):
        return self.__thread_class

    def set_thread_class(self, value):
        self.__thread_class = value

    def get_pool_size(self):
        return self._pool_size

    def _set_pool_size(self):
        """
        This method determines the number of threads that will be necessary
        to execute the queue in a timely manner.
        It uses the constants 'MAX_THREADS' and 'MIN_CLIENTS_PER_THREAD' to 
        limit the number of threads.
        """
        queue_size = self.in_queue.qsize()
        estimated_pool_size = max(1, queue_size / MIN_CLIENTS_PER_THREAD)
        self._pool_size = min(estimated_pool_size, MAX_THREADS)
    
    def get_in_queue(self):
        return self.__in_queue

    def get_out_queue(self):
        return self.__out_queue

    def set_in_queue(self, value):
        self.__in_queue = value

    def set_out_queue(self, value):
        self.__out_queue = value

    def get_finished(self):
        return self.__finished

    def set_finished(self, value):
        self.__finished = value

    thread_class = property(get_thread_class, set_thread_class)
    in_queue = property(get_in_queue, set_in_queue)
    out_queue = property(get_out_queue, set_out_queue)
    pool_size = property(get_pool_size)
    finished = property(get_finished, set_finished)
    
    def run(self):
        """
        This method creates a pool of threads, starts them, and waits for the
        'input_queue' to be empty before asking them to stop.
        Results, if any, will be available in the 'output_queue'.
        """
        self._set_pool_size()
        
        log.debug('Active threads: %d' % threading.active_count()) #@UndefinedVariable
        
        # Create threads and add them to the pool
        for i in range(self.pool_size): #@UnusedVariable
            thread = self.thread_class(self.in_queue, self.out_queue,
                                       **self._thread_args)
            thread.name = 'Worker-%02d' % i
            self._thread_pool.append(thread)
            thread.start()
        
        log.debug('Active threads: %d' % threading.active_count()) #@UndefinedVariable
        
        # Wait for the threads to process all the clients in the queue
        while not self.in_queue.empty():
            pass

        # Ask threads to stop
        for thread in self._thread_pool:
            thread.join()
        self.finished = True
            

class ReferenceMakerThread(threading.Thread):
    """
    This class has the logic to create the reference for a file in a separate
    thread.
    """
    def __init__(self, in_queue, out_queue, **kwargs):
        self.stop_event = threading.Event()
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.parse_args(**kwargs)
        threading.Thread.__init__(self)

    def get_in_queue(self):
        return self.__in_queue

    def get_out_queue(self):
        return self.__out_queue

    def get_target_format(self):
        return self.__target_format

    def set_in_queue(self, value):
        self.__in_queue = value

    def set_out_queue(self, value):
        self.__out_queue = value
        
    def set_target_format(self, value):
        self.__target_format = value

    in_queue = property(get_in_queue, set_in_queue)
    out_queue = property(get_out_queue, set_out_queue)
    target_format = property(get_target_format, set_target_format)

    def parse_args(self, **kwargs):
        self.target_format = (kwargs['target_format'] if 'target_format' in 
                              kwargs.keys() else ReferenceFormat.BIBTEX)

    def join(self, timeout=None):
        """
        Kindly asks the thread to finish.
        """
        self.stop_event.set()
        threading.Thread.join(self, timeout)            

    def run(self):
        """
        Runs indefinitely until it is asked to finish.
        Processes files from the 'input_queue' and supplies them to a 
        'ReferenceMaker' object.
        Once the ReferenceMaker is done, it stores the results in tuples
        (file, reference) to the output queue.
        """
        log.debug("Running thread", extra={'threadname':self.getName()}) #@UndefinedVariable
        while not self.stop_event.isSet():
            file = None
            if not self.in_queue.empty():
                try:
                    file = self.in_queue.get(False)
                except Queue.Empty:
                    continue
            if file:
                log.debug("Processing file %s" % file) #@UndefinedVariable
                try:
                    reference = ReferenceMaker().make_reference(file,
                                                            self.target_format)
                    self.out_queue.put(reference)
                except Exception, e:
                    log.error('Unexpected exception while extracting reference' #@UndefinedVariable
                              ' for file %s: %s' % (file, str(e)))
                    self.out_queue.put(Extraction())
                    continue
    
