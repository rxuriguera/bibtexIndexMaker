
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

from datetime import datetime
from time import sleep
import re

from bibim import log
from bibim.db.session import create_session
from bibim.db.mappers import (ExtractedReference)
from bibim.util.browser import (Browser, BrowserError)
from bibim.util.beautifulsoup import BeautifulSoup


MAX_EXAMPLES = 5
MAX_EXAMPLES_FROM_DB = 15
MIN_VALIDITY = 0.75
SECONDS_BETWEEN_REQUESTS = 0.5

class Example(object):
    """
    Represents an example defining a piece of information to be extracted. 
    """
    
    def __init__(self, value=None, content=None):
        self.value = value
        self.content = content

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
    
    def get_content(self):
        return self.__content
    
    def set_content(self, value):
        self.__content = value
   
    value = property(get_value, set_value)
    content = property(get_content, set_content)    


class HTMLExample(Example):
    
    def __init__(self, url='', value=None, content=None):
        self.url = url
        super(HTMLExample, self).__init__(value, content)
    
    def get_url(self):
        return self.__url

    def set_url(self, value):
        self.__url = value

    url = property(get_url, set_url)


class ExampleManager(object):
    def __init__(self, session=create_session()):
        self.session = session
        
    def get_examples(self): 
        """
        Creates examples from the database and organizes them in different sets
        depending on some parameters.
        """
        raise NotImplementedError
        
    def _get_example_mappers(self):
        """
        Retrieves mappers from the database. A mapper will later be used to 
        create examples that share some data. 
        """
        raise NotImplementedError
    
    def _check_still_valid(self):
        """
        Checks if an example is valid. This method attempts to detect positive
        examples that are no longer working. It should be overridden by 
        subclasses.
        """
        raise NotImplementedError


class HTMLExampleManager(ExampleManager):
    """
    This subclass implements methods to retrieve the examples from the database
    and to check if they are still valid. It is intended to work with
    HTMLExample objects.
    """
    last_request = datetime.now()
    
    def get_examples(self, url, nexamples):
        """
        Retrieves information from the database and creates instances of 
        HTMLExample with the url and the value that has to be extracted.
        It organizes all the examples in sets depending on the field that
        has to be extracted.
        """
        
        # This is to prevent the system from doing too many requests to the
        # same server
        if nexamples > MAX_EXAMPLES:
            nexamples = MAX_EXAMPLES
            
        examples = {}
        example_mappers = self._get_example_mappers(url)
         
        for mapper in example_mappers:
            url = mapper.result
            content = self._get_content(url)

            # Check if the contents of the database are still valid
            if not self._check_still_valid(mapper, content):
                continue 
            
            fields = [field for field in mapper.fields if field.valid]
            for field in fields:
                examples.setdefault(field.name, set())
                example = HTMLExample(url, field.value, content)
                examples[field.name].add(example)
                
            # Break if we already have enought examples for all of the fields
            if min(map(len, examples.values())) >= nexamples:
                break
    
        self.session.commit()
        return examples
    
    def _get_example_mappers(self, url):
        """
        Retrieves mappers from the database that will be used to create
        the examples
        """
        examples = {}
        query_results = (self.session.query(ExtractedReference).
                         filter(ExtractedReference.validity >= MIN_VALIDITY).
                         filter(ExtractedReference.result.like(url + '%')). #@UndefinedVariable
                         order_by(ExtractedReference.validity).
                         order_by(ExtractedReference.timestamp)
                         [:MAX_EXAMPLES_FROM_DB])
        
        return query_results
    
    def _get_content(self, url):
        """
        This method looks for the content of an example's URL. In order not to
        overload the server, it sleeps for some time between multiple calls. 
        """
        time_to_sleep = (SECONDS_BETWEEN_REQUESTS - 
                        (datetime.now() - self.last_request).seconds)
        if time_to_sleep > 0:
            sleep(time_to_sleep)
        
        content = None
        try:
            content = Browser().get_page(url)
            content = BeautifulSoup(content) if content else None
        except BrowserError as e:
            log.error('Error retrieving page %s: %s' % (url, #@UndefinedVariable
                                                        e.error))
        self.last_request = datetime.now()
        return content
    
    def _check_still_valid(self, mapper, content):
        """
        It checks if the information to be extracted is really present within
        the contents. If it doesn't, then it updates the database so the
        corresponding records won't be used again.
        """
        
        # In case the content could not be extracted, don't update the database
        if not content:
            return False
        
        # For each piece of information, check if it exists in the contents.
        # At this point, we don't care about its location, but if it
        # can be found.
        not_found = 0.0
        for field in mapper.fields:
            found = content.find(text=re.compile(field.value))
            if not found:
                log.info('Field %s with value %s cannot be found anymore in %s' #@UndefinedVariable
                         % (field.name, field.value, mapper.result))
                field.valid = False
                not_found += 1
        
        validity = 1 - (not_found / len(mapper.fields)) 
        if validity < MIN_VALIDITY:
            log.info('Example with url "%s" marked as invalid from now on.' % #@UndefinedVariable
                      mapper.result)
            mapper.validity = validity
            return False
    
        return  True
    
