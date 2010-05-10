
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

"""
Entry points to the application
"""

import Queue #@UnresolvedImport
import threading #@UnresolvedImport

from bibim import log
from bibim.db.session import flush_changes
from bibim.main.files import FileManager
from bibim.main.threads import ThreadRunner, ReferenceMakerThread
from bibim.main.controllers import IEController
from bibim.main.factory import UtilFactory

class IndexMaker(threading.Thread):
    def __init__(self):
        super(IndexMaker, self).__init__()
        self.__path = ''
        self._in_queue = Queue.Queue(0)
        self._out_queue = Queue.Queue(0)
        self.processed = []
        self.thread_runner = None
        self.trhead_class = ReferenceMakerThread

    def get_processed(self):
        return self.__processed

    def set_processed(self, value):
        self.__processed = value

    def set_path(self, path):
        self.__path = path
        
        # Read all the files from the given path and put them in a queue
        self.files = FileManager().get_files_list(path)        
        for file in self.files:
            self._in_queue.put(file)
    
    def get_n_files(self):
        return self._in_queue.qsize()
        
    def make_index(self):
        self.trhead_class = ReferenceMakerThread
        self.start()
        
    def run(self):
        log.debug("Start running index maker") #@UndefinedVariable

        # Run threads
        self.thread_runner = ThreadRunner(self.trhead_class,
                                          self._in_queue, self._out_queue)
        self.thread_runner.run()
        
        while not self._out_queue.empty():
            self.processed.append(self._out_queue.get())

        # Commit changes to the database
        flush_changes()
        log.debug("Total processed: %d" % len(self.processed)) #@UndefinedVariable

    processed = property(get_processed, set_processed)


class WrapperGenerator(threading.Thread):               
    def __init__(self, url):
        super(WrapperGenerator, self).__init__()
        self.url = url
        self.factory = UtilFactory()
        self.ie_controller = IEController(self.factory)

    def run(self):
        self.generate_wrappers()

    def generate_wrappers(self):
        self.ie_controller.generate_wrappers(self.url)
    
    

        
