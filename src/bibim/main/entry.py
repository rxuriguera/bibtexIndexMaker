
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

from bibim import log
from bibim.db.session import flush_changes
from bibim.main.files import FileManager
from bibim.main.threads import ThreadRunner, ReferenceMakerThread

class IndexMaker(object):
    def __init__(self):
        self._in_queue = Queue.Queue(0)
        self._out_queue = Queue.Queue(0)
    
    def make_index(self, path, source_format='pdf', target_format='bibtex'):
        log.debug("Start making index") #@UndefinedVariable
        
        # Read all the files from the given path and put them in a queue
        files = FileManager().get_files_list(path)        
        for file in files:
            self._in_queue.put(file)
        
        # Run threads to extract references
        thread_runner = ThreadRunner(ReferenceMakerThread,
                                     self._in_queue, self._out_queue)
        thread_runner.run()
        
        # TODO: Remove printing from this class
        num_refs = 0
        content_extract = 0
        found_resutls = 0
        valid = 0
        invalid = 0
        while not self._out_queue.empty():
            extraction = self._out_queue.get()
            
            print "File: %s" % extraction.file_path
            if extraction.used_query:
                print "Query: %s" % extraction.used_query
                content_extract += 1
            if extraction.used_result:
                print "Result: %s" % extraction.used_result.url
                found_resutls += 1
            for ref in extraction.entries:
                num_refs += 1
                print "Ref: \n%s" % ref.get_entry()
                if ref.validity >= 0.5:
                    print 'Valid'
                    valid += 1
                else:
                    print 'Not Valid'
                    invalid += 1 
            print "\n\n\n"
        
        # Commit changes to the database
        flush_changes()
        
        
        print 'Total files: %d' % len(files)
        print 'Could extract content: %d' % content_extract
        print 'Could find results: %d' % found_resutls
        print 'Total references: %d' % num_refs
        print 'Total valid references: %d' % valid
        print 'Total invalid references: %d' % invalid    
    
    def generate_wrappers(self):
        pass
        
