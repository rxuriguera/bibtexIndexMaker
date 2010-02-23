
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

from bibim.main.files import FileManager
from bibim.main.threads import ThreadRunner

'''                        
pdf_extractor = PDFTextExtractor()
ref_wrapper = ReferenceWrapper()
pattern = re.compile("([\w]+[ .,;:()?!]){8,10}")

# Extract text
print 'RCE' 
self.file_content = pdf_extractor.extract(file).content

# Get Query String
search_string = re.search(pattern, self.file_content)
search_string = '"' + search_string.group().strip() + '"'
print 'Search string %s' % search_string

# Search
print 'IR'
searcher = ScholarSearch(search_string)
results = searcher.get_results()
results = [result for result in results if not result.url.endswith('.pdf')]
if not results:
    return

# Get page
print 'Get page'
browser = Browser()
page = browser.get_page(results[0].url)
page = BeautifulSoup(page)

# Extract reference
print 'IE'
id = 'http://' + results[0].url.split('/')[2]
raw_ref = ref_wrapper.extract_info(id, page)

# Parse reference
ref = Reference()
ref.set_entry(raw_ref)
ref.set_format(ReferenceFormat.BIBTEX)
parser = BibtexParser()
parsed = parser.parse_entry(raw_ref)

# Validation
print 'Validate'
title = parsed.get('title')
valid = re.search(title, self.file_content)
Qout.put(ref)        
'''

class IndexMaker(object):
    def __init__(self):
        
        self._in_queue = Queue.Queue(0)
        self._out_queue = Queue.Queue(0)
    
    def make_index(self, path, source_format='pdf', target_format='bibtex'):
        files = FileManager().get_files_list(path)
        for file in files:
            self._in_queue.put(file)
        
        thread_runner = ThreadRunner(self._in_queue, self._out_queue)
        thread_runner.run()
        
