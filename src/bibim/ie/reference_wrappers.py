
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


import re

from bibim import log
from bibim.ie.types import Wrapper
from bibim.util.beautifulsoup import BeautifulSoup
from bibim.util.browser import (Browser,
                                BrowserError)
from bibim.util.helpers import ReferenceFormat


class ReferenceWrapper(Wrapper):
    """
    Offers methods to extract complete references from som webpages
    """
    _available_wrappers = {'http://portal.acm.org':'portal_acm'}
    _browser = Browser()
    
    def extract_info(self, source, page):
        """
        Extracts a reference from the given page.
        """
        if source not in self._available_wrappers.keys():
            log.debug('No reference wrapper available for source %s' % source) #@UndefinedVariable
            return (None, None)
        
        wrapper_method = getattr(self,
                                 '_do_' + self._available_wrappers[source])
        
        return wrapper_method(source, page) 

    def get_available_wrappers(self):
        return self._available_wrappers.keys()

    def _do_portal_acm(self, source, page):
        """
        Searches the page for a link to the reference, and then retrieves the
        reference.
        Returns a tuple with the full reference and its format.
        """ 
        log.debug('Using ACM Portal reference wrapper') #@UndefinedVariable
        ref = (None, None)
        anchor = page.find('a', {'onclick':re.compile('popBibTex.cfm')})
        if not anchor:
            return ref
        jscript = anchor['onclick'].replace('window.open', '').strip('\(\)')
        ref_url = jscript.split(',')[0].strip('\'')
        ref_url = source + '/' + ref_url
        
        try:
            page = BeautifulSoup(self._browser.get_page(ref_url))
        except BrowserError:
            log.error('Browse error while retrieving entry page') #@UndefinedVariable
            return ref
        
        pre = page.find('pre')
        if not pre:
            return ref
        
        # As the wrapper has been hardcoded, we already know what will be the
        # format of the reference
        return (pre.find(text=True).strip(), ReferenceFormat.BIBTEX)
       
