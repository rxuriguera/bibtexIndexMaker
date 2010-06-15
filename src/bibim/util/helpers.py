
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

from bibim.util.beautifulsoup import (BeautifulSoup,
                                      Comment)

class Format(object):
    
    def get_format(self, path):
        format = None
        elements = path.split('.')
        if elements:
            format = elements[-1]
        return format


class FileFormat(Format):
    TXT = 'txt'
    PDF = 'pdf'


class ReferenceFormat(Format):
    BIBTEX = 'bibtex'

class ContentCleaner(object):
    def __init__(self):
        pass
    
    def clean_content(self, content):
        if not content:
            return None
        
        to_replace = {'\n':' ',
                      '\r':'',
                      '\t':'',
                      '<br>':' ',
                      '<br/>':' ',
                      '&amp;':'&',
                      '&#38;':'&',
                      '&#34;':'"',
                      '&quot;':'"',
                      '&rsquo;':"'",
                      '&#39;':"'",
                      '&apos;':"'",
                      '&#x2013;':'-',
                      '&nbsp;':' '}
        for key in to_replace:
            content = content.replace(key, to_replace[key])

        # Remove consecutive whitespaces
        content = re.sub(' {2,}', ' ', content)
        content = re.sub('>( *)<', '><', content)

        content = BeautifulSoup(content)
        
        # Remove comments
        comments = content.findAll(text=lambda text:isinstance(text, Comment))
        [element.extract() for element in comments]
        
        # Remove unnecessary HTML elements
        for tag in ['meta', 'link', 'style', 'script']:
            elements = content.findAll(tag)
            [element.extract() for element in elements]

        return content
    
