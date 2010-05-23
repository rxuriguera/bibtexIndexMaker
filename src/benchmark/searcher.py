
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

import simplejson #@UnresolvedImport
import time
import re

from bibim.ir.search import (Browser,
                             BrowserError)
from bibim.main import controllers
from bibim.main.factory import UtilFactory
from bibim.util.helpers import FileFormat
from bibim.util.beautifulsoup import BeautifulSoup



class SearcherBenchmark(object):
    engines = ['Google', 'Scholar', 'Bing', 'Yahoo']
    good_results = [0, 0, 0, 0]
    
    bad_results = [0, 0, 0, 0]
    first_query_with_good = {}
    
    updated = [False, False, False, False]
    good_results_files = [0, 0, 0, 0]
    
    def __init__(self):
        self.factory = UtilFactory()
        self.rce = controllers.RCEController(self.factory)
        self.ir = controllers.IRController(self.factory)
        self.results_cache = {}
        self.browser = Browser()
        
    def print_parameters(self):
        self.save_msg('Parameters:')
        self.save_msg('Too many results;Min words;Max words;Skip queries')
        self.save_msg(''.join([str(controllers.TOO_MANY_RESULTS), ';',
                               str(controllers.MIN_WORDS), ';',
                               str(controllers.MAX_WORDS), ';',
                               str(controllers.SKIP_QUERIES)]))

    def run(self):
        results_cache_filename = 'customHeaders_cache_file.txt'
        results_cache_file = open(results_cache_filename, 'r')
        contents = results_cache_file.read()
        results_cache_file.close()
        if contents != '': 
            self.results_cache = simplejson.loads(contents)
        basepath = '/home/rxuriguera/benchmark/pdfsets/customHeader/'
        self.results_file = open(''.join([basepath, 'results-15-7-12.csv']), 'w')
        
        self.print_parameters()     
        files = open(''.join([basepath, 'filelist.txt']), 'r')
        for line in files.readlines():
            split_line = line.split(' ', 1)
            if len(split_line) != 2:
                print 'Incorrect line!'
                continue
            file = split_line[0].strip()
            check_string = split_line[1].strip()
            
            file_text = self.rce.extract_content(file, FileFormat.TXT)
            if not file_text:
                print 'Skipping file %s' % file
                continue
            
            queries = self.rce.get_query_strings(file_text)
            self.save_msg('File:; %s' % file)
            
            self.updated = [False, False, False, False]
            file_first_queries = self.first_query_with_good.setdefault(file, [0, 0, 0, 0])
            for query, pos in zip(queries, range(len(queries))):
                self.search_query(query, pos, check_string, file_first_queries)
        
        self.save_msg('')
        self.save_msg('')
        self.save_msg('')

            
        self.save_msg('Good results by engine:')
        self.save_msg('Google;Scholar;Bing;Yahoo')
        self.save_msg('%d;%d;%d;%d' % tuple(self.good_results))
        self.save_msg('')
        
        self.save_msg('Bad results by engine:')
        self.save_msg('Google;Scholar;Bing;Yahoo')
        self.save_msg('%d;%d;%d;%d' % tuple(self.bad_results))
        self.save_msg('')
        
        self.save_msg('Files with good results:')
        self.save_msg('Google;Scholar;Bing;Yahoo')
        self.save_msg('%d;%d;%d;%d' % tuple(self.good_results_files))
        self.save_msg('')
        
        self.save_msg('First query with good results:')
        self.save_msg('File;Google;Scholar;Bing;Yahoo')
        for item in self.first_query_with_good.items():
            self.save_msg('%s;%d;%d;%d;%d' % ((item[0],) + tuple(item[1])))
        
        results_cache_file = open(results_cache_filename, 'w')
        simplejson.dump(self.results_cache, results_cache_file)
        results_cache_file.close()
        
        files.close()
        self.results_file.close()

    def save_msg(self, msg):
        print msg
        self.results_file.write(''.join([msg, '\n']))

    def search_query(self, query, query_pos, check_string, file_first_queries):
        self.save_msg('Query;%s' % (query))
        max_results = 0
        min_results = 50
        top_engine = ''
        worst_engine = ''
        
        for engine in range(4):
            # Skip google scholar
            if engine == 1:
                continue
            engine_name = self.engines[engine]
            results, query = self.ir.get_top_results([query], engine)
            nresults = len(results)
            #self.save_msg('Engine:,%s,,Results:,%d' % (engine_name, nresults))
            
            too_many = False
            if nresults > controllers.TOO_MANY_RESULTS:
                too_many = True
                results = results[:controllers.TOO_MANY_RESULTS]
            
            if too_many:
                self.save_msg('%s;Query with too many results' % engine_name)
                continue
            
            # Check max number of results
            if nresults > max_results:
                max_results = len(results)
                top_engine = engine_name
            elif nresults == max_results:
                top_engine = ''.join([top_engine, ', ', engine_name])
            
            # Check min number of results
            if nresults == min_results:
                worst_engine = ''.join([worst_engine, ', ', engine_name])
            elif nresults < min_results:
                min_results = nresults
                worst_engine = engine_name
            
            for result in results:
                valid = self.check_result_url(result.url, check_string)
                self.save_msg(''.join([engine_name, ';', result.url, ';', str(valid)]))
                
                if valid:
                    # Update number of good results
                    self.good_results[engine] += 1
                    
                    # Update first query with good results
                    if file_first_queries[engine] == 0:
                        file_first_queries[engine] = query_pos
                    
                    # Update number of files with good results
                    if not self.updated[engine]:
                        self.updated[engine] = True 
                        self.good_results_files[engine] += 1
                else:
                    self.bad_results[engine] += 1
                    
            
                
        if max_results:
            self.save_msg('Max Results (%s):;%d ' % (top_engine, max_results))
            self.save_msg('Min Results (%s):;%d' % (worst_engine, min_results))
        else:
            self.save_msg('None of the searchers got results')
            
        self.save_msg('')
        
    def check_result_url(self, url, check_string):
        if url in self.results_cache.keys():
            return self.results_cache[url]
        else:
            elements = None
            try:
                time.sleep(5)
                page = self.browser.get_page(url)
                page = self._clean_content(page)
                page = BeautifulSoup(page)
                elements = page.findAll(True,
                                        text=re.compile(check_string.lower()))
            except BrowserError, e:
                print 'ERROR: Browser error: %s' % e
            except Exception, e:
                print 'ERROR: Error checking error: %s' % e
            
            if elements:
                valid = 1
            else:
                valid = 0
            self.results_cache[url] = valid
            return valid
        
    def _clean_content(self, content):
        """
        Removes blank spaces from the retrieved page
        """
        if not content:
            return None
        content = content.lower()
        content = content.replace('\n', ' ')
        content = content.replace('\r', '')
        content = content.replace('\t', '')
        content = content.replace('&nbsp;', ' ')
        return content
                
if __name__ == '__main__':
    benchmark = SearcherBenchmark()
    benchmark.run()
    
    #browser = Browser()
    #page = browser.get_page('')
    #page = _clean_content(page)
    #page = BeautifulSoup(page)
    #elements = page.findAll(True,
    #                        text=re.compile(''.lower()))
