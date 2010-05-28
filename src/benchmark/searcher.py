
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

import numpy as nps
import matplotlib.pyplot as plt #@UnresolvedImport


from bibim.ir.search import (Browser,
                             BrowserError)
from bibim.main import controllers
from bibim.main.factory import UtilFactory
from bibim.util.helpers import FileFormat
from bibim.util.beautifulsoup import BeautifulSoup



class SearcherBenchmark(object):
    engines = ['Google', 'Scholar', 'Bing', 'Yahoo']
    colors = ['#666666', '#60a63a', '#999999', '#BBBBBB']

    updated = [False, False, False, False]
    good_results_files = [0, 0, 0, 0]
    info = []
    
    # 'file':[{},[first_query_with_good_results,0,0,0]]
    #                 google      bing       yahoo
    # 'query_string':[[total results, good results, first good result] , [], []]
    
    
    def __init__(self):
        self.factory = UtilFactory()
        self.rce = controllers.RCEController(self.factory, 10, 10)
        self.ir = controllers.IRController(self.factory)
        self.results_cache_filename = 'customHeaders_cache_file.txt'
        self.results_cache = {}
        self.browser = Browser()
        self.basepath = '/home/rxuriguera/benchmark/pdfsets/random/'
        self.basename = 'random'
        self.len_range = range(4, 15)

    def _load_results_cache(self):
        results_cache_file = open(self.results_cache_filename, 'r')
        contents = results_cache_file.read()
        results_cache_file.close()
        if contents != '': 
            self.results_cache = simplejson.loads(contents)
    
    def _save_results_cache(self):
        results_cache_file = open(self.results_cache_filename, 'w')
        simplejson.dump(self.results_cache, results_cache_file)
        results_cache_file.close()
    
    def run(self):
        self._load_results_cache()
        self.results_file = open(''.join([self.basepath,
                                          ''.join([self.basename,
                                                   '.csv'])]), 'w')

        files = open(''.join([self.basepath, 'filelist.txt']), 'r')
        
        for length in self.len_range:
            print '$$$$$$$$$$$$$$$$$$$ Word Length %d $$$$$$$$$$$$$$$$$$$' % length
            word_length_info = [{}, [0, 0, 0, 0]] # files info and file coverage
            self.info.append(word_length_info)
            
            self.rce = controllers.RCEController(self.factory, length, length)
            
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
                
                self.updated = [False, False, False, False]
                file_info = word_length_info[0].setdefault(file, [{}, [0, 0, 0, 0]])
                
                queries = self.rce.get_query_strings(file_text)
                self.save_msg('File:; %s' % file)
    
                for query, pos in zip(queries, range(len(queries))):
                    file_covered = self.search_query(query, pos, check_string, file_info)
                    word_length_info[1] = [i + j for i, j in 
                                           zip(word_length_info[1], file_covered)]

            files.seek(0)
            self._save_results_cache()
            
        print self.info

        self.save_charts()

        self._save_results_cache()
        files.close()
        self.results_file.close()

    def save_cvs(self, query_length):    
        self.save_msg('')
        self.save_msg('')
        self.save_msg('')
        self.save_msg('Query length:;%s' % query_length)
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
            
        self.save_msg('First good result for query:')
        self.save_msg('Query;Google;Scholar;Bing;Yahoo')

    def save_charts(self):
        self._save_coverage_chart()
        self._save_first_query_chart()
        #self._save_first_result_chart()
        pass
    
    def _save_first_result_chart(self):
        """
        This chart shows the average number of bad results that have been tried 
        before getting good results
        """
        data = [[], [], [], []]
        for word_length_info in self.info:
            total_files = float(len(word_length_info[0]))
            for i in range(len(data)):
                try:
                    s = sum([sum([query_info[i][2] for query_info in file_info[0].values()]) / sum([query_info[i][0] for query_info in file_info[0].values()]) for file_info in word_length_info[0].values()]) / total_files
                except ZeroDivisionError:
                    s = 0    
                data[i].append(12)
        
        self._save_chart(data, 'Resultats',
                 'Primer bon resultat',
                 'Llargada de la consulta (paraules)',
                 '-firstresult.pdf',
                 self.len_range,
                 [self.len_range[0] - 1, self.len_range[-1] + 1, 0, 10],
                 self.len_range,
                 range(0, 10, 1))
        
        
    def _save_first_query_chart(self):
        """
        This chart shows the average number of queries necessary to start
        getting good results
        """
        data = [[], [], [], []]
        for word_length_info in self.info:
            total_files = float(len(word_length_info[0]))
            for i in range(len(data)):
                s = sum([file[1][i] for file in word_length_info[0].values()])
                data[i].append(s / total_files)
                
        self._save_chart(data, 'Consultes',
                 'Primera consulta amb bons resultats',
                 'Llargada de la consulta (paraules)',
                 '-firstquery.pdf',
                 self.len_range,
                 [self.len_range[0] - 1, self.len_range[-1] + 1, 0, 10],
                 self.len_range,
                 range(0, 10, 1))
        
        
    def _save_coverage_chart(self):
        """
        This chart shows the percentage of files for which each browser 
        returned good results
        """
        data = [[], [], [], []]
        total_files = len(self.info[0][0])
        percentage = 100.0 / total_files
        for word_length_info in self.info:
            file_coverage = word_length_info[1]
            
            for i in range(len(file_coverage)):
                data[i].append(file_coverage[i] * percentage)
        
        self._save_chart(data, 'Cobertura',
                         'Fitxers coberts (%)',
                         'Llargada de la consulta (paraules)',
                         '-coverage.pdf',
                         self.len_range,
                         [self.len_range[0] - 1, self.len_range[-1] + 1, 0, 110],
                         self.len_range,
                         range(0, 101, 10))
        
    def _save_chart(self, data, title, ylabel, xlabel, name, xvalues=[],
                    axis_info=[0, 100, 0, 100], xticks=None, yticks=None):
        width = 4.5
        height = 2.0
        #plt.rc("figure.subplot", left=(22 / 72.27) / width)
        #plt.rc("figure.subplot", right=(width - 10 / 72.27) / width)
        #plt.rc("figure.subplot", bottom=(14 / 72.27) / height)
        #plt.rc("figure.subplot", top=(height - 7 / 72.27) / height)
        plt.figure(figsize=(width + 1, height + 1))
        plt.subplots_adjust(left=0.125, bottom=0.15, right=0.95, top=0.9)
        
        #plt.figure()
        
        plt.rc("font", family="cmr10")
        plt.rc("font", size=10)
        
        plt.subplot(111)
        lines = []
        for i in range(len(data)):
            # Skip scholar
            if i == 1:
                continue
            print data[i]
            line = plt.plot(xvalues, data[i])[0]
            line.set_color(self.colors[i])
            line.set_label(self.engines[i])
            line.set_linewidth(2.0)
            lines.append(line)
            
        plt.axis(axis_info)
                
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
            
        if xticks:
            plt.xticks(xticks)
        
        if yticks:
            plt.yticks(yticks)
        

        plt.grid(True, color='#666666')
        
        plt.savefig(''.join([self.basepath, self.basename, name ]))
        
        
    def save_msg(self, msg):
        print msg
        self.results_file.write(''.join([msg, '\n']))

    def search_query(self, query, query_pos, check_string, file_info):
        self.save_msg('Query;%s' % (query))
        
        query_info = file_info[0].setdefault(query, [[0, 0, 0],
                                                     [0, 0, 0],
                                                     [0, 0, 0],
                                                     [0, 0, 0]])
        
        max_results = 0
        min_results = 50
        top_engine = ''
        worst_engine = ''
        covered = [0, 0, 0, 0]
        
        for engine in range(4):
            # Skip google scholar
            if engine == 1:
                continue
            engine_name = self.engines[engine]
            results, query = self.ir.get_top_results([query], engine)
            nresults = len(results)
            self.save_msg('Engine:,%s,,Results:,%d' % (engine_name, nresults))
            
            query_info[engine][0] = nresults
            
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
            
            for result, index in zip(results, range(len(results))):
                valid = self.check_result_url(result.url, check_string)
                self.save_msg(''.join([engine_name, ';', result.url, ';', str(valid)]))
                
                if valid:
                    # Update number of good results
                    query_info[engine][1] += 1
                    
                    # Update first good results for this query
                    if not query_info[engine]:
                        query_info[engine][2] = index
                    
                    # Set first query with good result
                    if not file_info[1][engine]:
                        file_info[1][engine] = query_pos
                    
                    if not self.updated[engine]:
                        self.updated[engine] = True
                        covered[engine] = 1
                                        
                
        if max_results:
            self.save_msg('Max Results (%s):;%d ' % (top_engine, max_results))
            self.save_msg('Min Results (%s):;%d' % (worst_engine, min_results))
            pass
        else:
            self.save_msg('None of the searchers got results')
            pass
        self.save_msg('')
        
        return covered
        
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
