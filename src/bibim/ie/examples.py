
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

from bibim import log
from bibim.db.session import create_session
from bibim.db import mappers
from bibim.util.browser import (Browser, BrowserError)
from bibim.util.beautifulsoup import BeautifulSoup

class Example(object):
    """
    Represents an example
    """
    
    def __init__(self, url='', source=None, info={}, positive=True):
        self.url = url
        self.source = source
        self.info = info
        self.positive = positive

    def get_url(self):
        return self.__url

    def set_url(self, value):
        self.__url = value

    def get_source(self):
        # Lazy load to prevent too many requests to the server
        if not self.__source:
            self._get_example_source()
        return self.__source

    def get_info(self):
        return self.__info

    def get_positive(self):
        return self.__positive

    def set_source(self, value):
        self.__source = value

    def set_info(self, value):
        self.__info = value

    def set_positive(self, value):
        self.__positive = value
    
    def _get_example_source(self):
        try:
            page = Browser().get_page(self.url)
        except BrowserError as e:
            log.error('Error retrieving page %s: %s' % (self.url,
                                                        e.error))
            return
        self.source = BeautifulSoup(page)

    url = property(get_url, set_url)
    source = property(get_source, set_source)
    info = property(get_info, set_info)
    positive = property(get_positive, set_positive)
        
    
class ExampleManager(object):
    """
    Retrieves examples from the database and organizes in different sets 
    depending on some parameters.
    """
    def __init__(self, session=create_session()):
        self.session = session

    def get_examples(self, url): 
        examples = []
        query_results = (self.session.query(mappers.Reference).
                         join(mappers.Result).
                         filter(mappers.Result.url.like(url + '%')).
                         filter(mappers.Result.used == True))
        
        for reference in query_results:
            append = False
            
            example = Example()
            example.url = reference.search_result.url
            
            for field in reference.fields:
                if field.valid:
                    append = True
                    example.info[field.name] = field.value
                
            # Only append if the reference has valid fields    
            if append:
                examples.append(example)
    
        return examples
