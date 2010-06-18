
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
from bibim.db.gateways import (ReferenceGateway,
                               ExtractionGateway)
from bibim.main.files import FileManager
from bibim.main.threads import ThreadRunner, ReferenceMakerThread
from bibim.main.controllers import (IEController,
                                    ReferencesController)
from bibim.main.factory import (UtilFactory,
                                UtilCreationError)
from bibim.references.format.formatter import ReferenceFormatter
from bibim.util.helpers import ReferenceFormat


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
            extraction = self._out_queue.get()
            # Persist the extraction
            ExtractionGateway().persist_extraction(extraction)
            
            self.processed.append(extraction)

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

    def set_wrapper_gen_examples(self, num_examples):
        self.ie_controller.wrapper_gen_examples = num_examples

    def generate_wrappers(self):
        self.ie_controller.generate_wrappers(self.url)


class ReferenceEntryFormatter(object):
    def __init__(self, format=ReferenceFormat.BIBTEX):
        self.reference_gw = ReferenceGateway()
        self.format = format
        self.util_factory = UtilFactory()
        
    def format_reference(self, reference_id):
        log.debug('Retrieving reference from the database') #@UndefinedVariable
        reference = self.reference_gw.find_reference_by_id(reference_id)
        if not reference:
            log.error('Reference with id %d could not be retrieved'  #@UndefinedVariable
                      % reference_id)
            return None
        
        formatter = ReferenceFormatter()
        try:
            generator = self.util_factory.create_generator(self.format)
        except UtilCreationError as e:
            log.error('Could not create a formatter for %s: %s' % #@UndefinedVariable
                      (self.format, e.args))
            return None
        
        log.debug('Starting to format') #@UndefinedVariable
        formatter.format_reference(reference, generator)
        
        return reference.entry


class ReferenceImporter(object):
    def __init__(self, format=ReferenceFormat.BIBTEX):
        self.format = format
        self.util_factory = UtilFactory()
        self.ref_controller = ReferencesController(self.util_factory,
                                                   self.format)
    
    def import_references(self, path):
        references = self.ref_controller.persist_file_references(path)
        return len(references)
