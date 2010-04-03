
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
from bibim.main.files import FileManager
from bibim.main.threads import ThreadRunner, ReferenceMakerThread
from bibim.main.persistence import Persistor

class IndexMaker(object):
    def __init__(self):
        self._in_queue = Queue.Queue(0)
        self._out_queue = Queue.Queue(0)
    
    def make_index(self, path, source_format='pdf', target_format='bibtex'):
        log.debug("Start making index")
        files = FileManager().get_files_list(path)        
        for file in files:
            self._in_queue.put(file)
        
        thread_runner = ThreadRunner(ReferenceMakerThread,
                                     self._in_queue, self._out_queue)
        thread_runner.run()
        
        # TODO: Add results to database
        # TODO: Remove printing from this class
        num_refs = 0
        content_extract = 0
        found_resutls = 0
        valid = 0
        invalid = 0
        while not self._out_queue.empty():
            entry = self._out_queue.get()
            
            try:
                persistor = Persistor()
                persistor.persist_dto(entry)
                persistor.commit()
            except Exception, e:
                log.error('Exception while storing to db:\n%s' % e)
                
            print "File: %s" % entry.file
            if entry.used_query:
                print "Query: %s" % entry.used_query
                content_extract += 1
            if entry.used_result:
                print "Result: %s" % entry.used_result.url
                found_resutls += 1
            for ref in entry.entries:
                num_refs += 1
                print "Ref: \n%s" % ref.get_entry()
                if ref.validity >= 0.5:
                    print 'Valid'
                    valid += 1
                else:
                    print 'Not Valid'
                    invalid += 1 
            print "\n\n\n"
        
        
        print 'Total files: %d' % len(files)
        print 'Could extract content: %d' % content_extract
        print 'Could find results: %d' % found_resutls
        print 'Total references: %d' % num_refs
        print 'Total valid references: %d' % valid
        print 'Total invalid references: %d' % invalid    
        
        
