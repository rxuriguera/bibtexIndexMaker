
# Copyright 2010 Ramon Xuriguera
# 
# This file is part of BibtexIndexMaker IR. The code in this file is 
# largely based on Peteris Krumins' python library for google search 
# wich is licensed under MIT license.
# 
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
# http://www.catonmat.net/blog/python-library-for-google-search/
#  
# BibtexIndexMaker IR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BibtexIndexMaker IR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker IR.  If not, see <http://www.gnu.org/licenses/>.


import re
import urllib #@UnresolvedImport

from htmlentitydefs import name2codepoint #@UnresolvedImport

from bibim.beautifulsoup import BeautifulSoup
from bibim.ir.browser import Browser, BrowserError


class SearchError(Exception):
    
    """
    Base class for search exceptions.
    """


class ParseError(SearchError):
    
    """
    Parse error in search results.
    self.msg attribute contains explanation why parsing failed
    self.tag attribute contains BeautifulSoup object with the most relevant tag
    that failed to parse
    Thrown only in debug mode
    """
     
    def __init__(self, msg, tag):
        self.msg = msg
        self.tag = tag

    def __str__(self):
        return self.msg

    def html(self):
        return self.tag.prettify()


class SearchResult(object):
    
    """
    """
    
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return 'Search Result: "%s"' % self.title


class GoogleSearchResult(SearchResult):
    
    """
    """
    
    def __init__(self, title, url, desc):
        super(GoogleSearchResult, self).__init__(title, url)
        self.desc = desc


class ScholarSearchResult(SearchResult):
    
    """
    """
    
    def __init__(self, title, url, desc, authors=[], year=None):
        super(ScholarSearchResult, self).__init__(title, url)
        self.desc = desc
        self.authors = authors
        self.year = year
    

class Searcher(object):
    
    """
    Base class for searching with a search engine
    """
    
    def __init__(self, query, random_agent=False, debug=False):
        self.query = query
        self.debug = debug
        self.browser = Browser(debug=debug)
        self.results_info = None
        self.eor = False # end of results
        self._page = 0
        self._results_per_page = 10
        self._last_from = 0

        if random_agent:
            self.browser.set_random_user_agent() 
            
    @property
    def num_results(self):
        if not self.results_info:
            page = self._get_results_page()
            self.results_info = self._extract_info(page)
            if self.results_info['total'] == 0:
                self.eor = True
        return self.results_info['total']

    @property
    def search_engine_url(self):
        raise NotImplementedError()    

    def _get_page(self):
        return self._page

    def _set_page(self, page):
        self._page = page

    page = property(_get_page, _set_page)

    def _get_results_per_page(self):
        return self._results_per_page

    def _set_results_par_page(self, rpp):
        self._results_per_page = rpp

    results_per_page = property(_get_results_per_page, _set_results_par_page)

    def get_results(self):
        """ Gets a page of results """
        if self.eor:
            return []

        page = self._get_results_page()
        search_info = self._extract_info(page)
        if not self.results_info:
            self.results_info = search_info
            if self.num_results == 0:
                self.eor = True
                return []
        results = self._extract_results(page)
        if not results:
            self.eor = True
            return []
        if self._page > 0 and search_info['from'] == self._last_from:
            self.eor = True
            return []
        if search_info['to'] == search_info['total']:
            self.eor = True
        self._page += 1
        self._last_from = search_info['from']
        return results

    def _maybe_raise(self, cls, *arg):
        if self.debug:
            raise cls(*arg)

    def _get_safe_url(self):
        raise NotImplementedError()

    def _get_results_page(self):
        safe_url = self._get_safe_url() 
        try:
            page = self.browser.get_page(safe_url)
        except BrowserError, e:
            raise SearchError, "Failed getting %s: %s" % (e.url, e.error)
        return BeautifulSoup(page)

    def _extract_info(self, soup):
        raise NotImplementedError()

    def _extract_raw_results_list(self, soup):
        raise NotImplementedError()

    def _extract_results(self, soup):
        results = self._extract_raw_results_list(soup)
        ret_res = []
        for result in results:
            eres = self._extract_result(result)
            if eres:
                ret_res.append(eres)
        return ret_res
    
    def _extract_result(self, result):
        raise NotImplementedError()

    def _html_unescape(self, str):
        def entity_replacer(m):
            entity = m.group(1)
            if entity in name2codepoint:
                return unichr(name2codepoint[entity])
            else:
                return m.group(0)

        def ascii_replacer(m):
            cp = int(m.group(1))
            if cp <= 255:
                return unichr(cp)
            else:
                return m.group(0)

        s = re.sub(r'&#(\d+);', ascii_replacer, str, re.U)
        return re.sub(r'&([^;]+);', entity_replacer, s, re.U)


class GoogleSearch(Searcher):
    
    """
    """
    
    @property
    def search_engine_url(self):
        return ('http://www.google.com/search?hl=en&q=%(query)s&num=%(num)d&st'
                'art=%(start)d')    

    def _get_safe_url(self):
        return self.search_engine_url % {'query':urllib.quote_plus(self.query),
                                'start':self._page * self._results_per_page,
                                'num'  :self._results_per_page }

    def _extract_info(self, soup):
        empty_info = {'from': 0, 'to': 0, 'total': 0}
        div_ssb = soup.find('div', id='ssb')
        if not div_ssb:
            self._maybe_raise(ParseError, ('Div with number of results was not'
                ' found on Google search page'), soup)
            return empty_info
        p = div_ssb.find('p')
        if not p:
            self._maybe_raise(ParseError, ('<p> tag within <div id="ssb"> was'
                ' not found on Google search page'), soup)
            return empty_info
        txt = ''.join(p.findAll(text=True))
        txt = txt.replace(',', '')
        matches = re.search(r'Results (\d+) - (\d+) of (?:about )?(\d+)',
                            txt, re.U)
        if not matches:
            return empty_info
        return {'from': int(matches.group(1)),
                'to': int(matches.group(2)),
                'total': int(matches.group(3))}
    
    def _extract_raw_results_list(self, soup):
        return soup.findAll('li', {'class': 'g'})

    def _extract_result(self, result):
        """
        This method will extract the title, url and description from a result.
        """
        title, url = self._extract_title_url(result)
        desc = self._extract_description(result)
        if not title or not url or not desc:
            return None
        return GoogleSearchResult(title, url, desc)

    def _extract_title_url(self, result):
        #title_a = result.find('a', {'class': re.compile(r'\bl\b')})
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(ParseError, ('Title tag in Google search result '
                                           'was not found'), result)
            return None, None
        title = ''.join(title_a.findAll(text=True))
        title = self._html_unescape(title)
        url = title_a['href']
        match = re.match(r'/url\?q=(http[^&]+)&', url)
        if match:
            url = urllib.unquote(match.group(1))
        return title, url

    def _extract_description(self, result):
        desc_div = result.find('div', {'class': re.compile(r'\bs\b')})
        if not desc_div:
            self._maybe_raise(ParseError, ('Description tag in Google search '
                                           'result was not found'), result)
            return None

        desc_strs = []
        def looper(tag):
            if not tag: return
            for t in tag:
                try:
                    if t.name == 'br': break
                except AttributeError:
                    pass

                try:
                    desc_strs.append(t.string)
                except AttributeError:
                    desc_strs.append(t)

        looper(desc_div)
        looper(desc_div.find('wbr')) # BeautifulSoup does not self-close <wbr>

        desc = ''.join(s for s in desc_strs if s)
        return self._html_unescape(desc)


class ScholarSearch(Searcher):
    
    """
    """
    
    @property
    def search_engine_url(self):
        return ('http://scholar.google.com/scholar?hl=en&q=%(query)s&num=%'
                '(num)d&start=%(start)d')
    
    def _get_safe_url(self):
        return self.search_engine_url % {'query':urllib.quote_plus(self.query),
                                'start':self._page * self._results_per_page,
                                'num'  :self._results_per_page }
        
    def _extract_info(self, soup):
        empty_info = {'from': 0, 'to': 0, 'total': 0}
        td_cell = soup.find('td', bgcolor='#dcf6db', align='right')
        if not td_cell:
            self._maybe_raise(ParseError, ('Cell with number of results was '
                'not found on Google Scholar search page'), soup)
            return empty_info
        font = td_cell.find('font')     
        if not font:
            self._maybe_raise(ParseError, ('<font> tag within <td> was not '
                'found on Google Scholar search page'), soup)
            return empty_info
        txt = ''.join(font.findAll(text=True))
        txt = txt.replace(',', '').split('.')[0]
        matches = re.search(r'Results (\d+) - (\d+) of (?:about )?(\d+)',
                            txt, re.U)
        if not matches:
            return empty_info
                
        return {'from': int(matches.group(1)),
                'to': int(matches.group(2)),
                'total': int(matches.group(3))}
  
    def _extract_raw_results_list(self, soup):
        return soup.findAll('div', {'class': 'gs_r'})    
  
    def _extract_result(self, result):
        title, url = self._extract_title_url(result)
        # Warning: _extract_description removes some elements from the tree, 
        # so authors and year have to be extracted in advance
        authors = self._extract_authors(result)
        desc = self._extract_description(result)
        if not title or not url or not desc:
            return None
        return ScholarSearchResult(title, url, desc, authors=authors) 

    def _extract_title_url(self, result):
        #title_a = result.find('a', {'class': re.compile(r'\bl\b')})
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(ParseError, ('Title tag in Google Scholar search'
                                           ' result was not found'), result)
            return None, None
        title = ''.join(title_a.findAll(text=True))
        title = self._html_unescape(title)
        url = title_a['href']
        match = re.match(r'/url\?q=(http[^&]+)&', url)
        if match:
            url = urllib.unquote(match.group(1))
        return title, url

    def _get_result_text(self, result):
        """
        This method returns all the text associated to a result. 
        Both the description and any other additional
        information that it may contain.
        """
        return result.find('font', size='-1')

    def _get_results_additional_info(self, result):
        """
        This method returns the information that appears on the first line of 
        a result's text.
        This information usually includes authors' names, year of publication, 
        etc.
        """
        result_text = self._get_result_text(result)
        if not result_text:
            return None
        return result_text.find('span', {'class': 'gs_a'})        

    def _extract_authors(self, result):
        """
        Google Scholar provides author names by each search result. This 
        method will return a list of names (if applicable).
        For results with a long list of authors, Google will truncate the 
        list and add an ellipsis. In such cases, this method will return
        a list containing only those complete names enclosed in the result.
        """
        add_info = self._get_results_additional_info(result)
        if not add_info:
            self._maybe_raise(ParseError, ('Additional information in Google '
                'Scholar search result was not found'), result)
            return []
        authors_info = ''.join(add_info.findAll(text=True)).split(' - ')[0]
        
        # Remove last author if it contains an ellipsis "..."
        authors = [self._html_unescape(author.strip()) for author in 
                   authors_info.split(',') if author.count(' &hellip') == 0]
        return authors
    
    def _extract_year(self, result):
        """
        Google Scholar usually provides result's year of publication. This
        method will search for a 4-digit number and return it.
        """
        add_info = self._get_results_additional_info(result)
        if not add_info:
            self._maybe_raise(ParseError, ('Additional information in Google '
                'Scholar search result was not found'), result)
            return None
        add_info_text = ''.join(add_info.findAll(text=True))
        matches = re.search(r"(\d{4})", add_info_text)
        if not matches:
            return None
        return matches.group(1)
  
    def _extract_description(self, result):
        """
        Given a result, it returns its description. Please note that 
        this method will remove some of the tree elements.
        """
        result_text = self._get_result_text(result) 
        if not result_text:
            self._maybe_raise(ParseError, ('Description tag in Google Scholar '
                'search result was not found'), result)
            return None
        
        # Remove irrelevant information.
        other_info = result_text.findAll('span')
        for info in other_info: info.extract()
         
        desc = ''.join(result_text.findAll(text=True))
        return self._html_unescape(desc.replace('\n', '')).strip()
