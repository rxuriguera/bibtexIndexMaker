
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


class SearchError(Exception):
    """
    Base class for search exceptions.
    """
    def __init__(self, error):
        self.error = error


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
    def __init__(self, title="", url=""):
        self.title = title
        self.url = url

    def __repr__(self):
        return ('Search Result(title: "%s..., url: %s...)"' % 
                (self.title[0:20], self.url[0:20]))
    
    @property
    def base_url(self):
        if self.url.startswith('http://'):
            return 'http://' + self.url.split('/')[2]
        else:
            return self.url.rsplit('/', 1)[0]
          

class DescSearchResult(SearchResult):
    """
    """
    def __init__(self, title, url, desc):
        super(DescSearchResult, self).__init__(title, url)
        self.desc = desc


class ScholarSearchResult(SearchResult):
    """
    """
    def __init__(self, title, url, desc, authors=[], year=None, base=None):
        super(ScholarSearchResult, self).__init__(title, url)
        self.desc = desc
        self.authors = authors
        self.year = year
