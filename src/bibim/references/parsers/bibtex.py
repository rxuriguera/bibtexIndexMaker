
# Copyright 2010 Ramon Xuriguera
#
# This file is an adaptation of ITB's (Humboldt-University Berlin)
# Bibliograph.parsing, written by Raphael Ritz (r.ritz@biologie.hu-berlin.de) 
# and released under the Zope License v.2.1
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
BibtexParser class
"""

import re
import os

from bibim.references.parsers.base import BibliographyParser, EntryParseError
from bibim.references.util import split_name
from bibim.references.parsers.util import (_encode, _decode,
                                    _latex2utf8enc_mapping,
                                    _latex2utf8enc_mapping_simple)


class BibtexParser(BibliographyParser):
    """
    A specific parser to process input in BiBTeX-format.
    """

    def __init__(self,
                 delimiter='}\s*@',
                 pattern='(,\s*[\w\-]{2,}\s*=)'):
        """
        Initializes including the regular expression patterns
        """
        self.set_delimiter(delimiter)
        self.set_pattern(pattern)

    def check_format(self, source):
        """
        Check if source is formatted in BibTeX
        """
        pattern = re.compile('^@[A-Z|a-z]*{', re.M)
        all_tags = re.findall(pattern, source)

        if all_tags:
            for t in all_tags:
                type = t.strip('@{').lower()
                if type not in ('article', 'book', 'booklet', 'conference',
                                'inbook', 'incollection', 'inproceedings',
                                'manual', 'mastersthesis', 'misc', 'phdthesis',
                                'proceedings', 'techreport', 'unpublished',
                                'collection', 'patent', 'webpublished'):
                    return False
            return True
        else:
            return False

    def preprocess(self, source):
        """
        Expands LaTeX macros
        Removes LaTeX commands and special formating
        Converts special characters to their ASCII equivalents
        """
        source = self._expand_macros(source)
        source = self._strip_comments(source)
        source = self._convert_chars(source)
        # it is important to _convert_chars before stripping off commands!!!
        # thus, whatever command will be replaced by a unicode value... the
        # remaining LaTeX commands will vanish here...
        source = self._strip_commands(source)
        return source

    def _expand_macros(self, source):
        lines = source.split(os.linesep)
        macros = [line for line in lines if line.count('@string') > 0]
        sourcelns = [line for line in lines if line.count('@string') == 0]
        source = '\n'.join(sourcelns)
        for macro in macros:
            split_on = re.compile('[{=}]+')
            matches = [m for m in split_on.split(macro) if m not in ['', ' ', '\r']]
            short = matches[1].strip()
            long = matches[-1].strip()
            old = re.compile("\\b" + short + "\\b")
            source = old.sub(long, source)
        return source

    def _strip_commands(self, source):
        oldstyle_cmd = re.compile(r'{\\[a-zA-Z]{2,}')
        newstyle_cmd = re.compile(r'\\[a-zA-Z]+{')
        source = oldstyle_cmd.sub('{', source)
        source = newstyle_cmd.sub('{', source)
        return source

    def _strip_comments(self, source):
        inside_entry = False
        waiting_for_first_brace = False
        newsource = ''

        for idx in range(len(source)):
            char = source[idx]
            last_char = (idx > 0) and source[idx - 1] or '\n'

            if char == '@' and not inside_entry:
                inside_entry = True
                waiting_for_first_brace = True
                braces_nesting_level = 0

            if inside_entry:
                newsource = newsource + char
                if char == '{' and last_char != "\\":
                    braces_nesting_level += 1

                if char == '}' and last_char != "\\":
                    braces_nesting_level -= 1

                if waiting_for_first_brace and (braces_nesting_level == 1):
                    waiting_for_first_brace = False

                if (braces_nesting_level == 0) and not waiting_for_first_brace and (char == '}'):
                    inside_entry = False
                    newsource = newsource + "\n"
        return newsource

    def _convert_chars(self, source):
        source = self._convert_latex_2_unicode(source)
        source = self._fix_white_space(source)
        return self._explicit_replacements(source)

    def _convert_latex_2_unicode(self, source):
        for latex_entity in _latex2utf8enc_mapping_simple.keys():
            source = _encode(_decode(source).replace(latex_entity,
                _latex2utf8enc_mapping_simple[latex_entity]))
        for latex_entity in _latex2utf8enc_mapping.keys():
            source = _encode(_decode(source).replace(latex_entity,
                _latex2utf8enc_mapping[latex_entity]))
        return source

    def _fix_white_space(self, source):
        ttable = [(r'\ ', ' '),
                  (r'\!', ' ')
                  ]
        for src_str, dst_str in ttable:
            source = source.replace(src_str, dst_str)
        wsp_tilde = re.compile(r'[^/\\]~')
        return wsp_tilde.sub(self._tilde_2_wsp, source).replace('\~', '~')

    def _tilde_2_wsp(self, hit): 
        return hit.group(0)[0] + ' '

    def _explicit_replacements(self, source):
        ttable = [(r'\/', ''),
                  (r'\&', '&'),
                  (r'\~', '~')
                  ]
        for src_str, dst_str in ttable:
            source = source.replace(src_str, dst_str)
        return source
    
    def parse_entry(self, entry):
        """
        Parses a single entry
        Returns a dictionary
        """
        result = {}

        # Remove newlines and <CR>s, and remove the last '}'
        blanks = re.compile('[\t\r\n]+')
        dspace = re.compile('[ ]{2,}')
        entry = blanks.sub(' ', entry).rstrip(' }')
        entry = dspace.sub(' ', entry)
        tokens = self.pattern.split(entry)

        try:
            type, id = tokens[0].strip(' @,').split('{')
            type = type.lower()
            result['reference_type'] = type
            result['reference_id'] = id
        except (ValueError, IndexError):
            raise EntryParseError() 
    
        for key, value in self._group(tokens[1:], 2):
            key = key.strip(' ,=').lower()

            # INBOOKs mapping: title -> booktitle, chapter -> chapter and title
            if type == 'inbook':
                if key == 'title':
                    key = 'booktitle'

                if key == 'chapter':
                    result['title'] = self._clean_line(value)

            # BibTex field "type" maps to CMFBAT field "publication_type"
            if key == 'type':
                key = 'publication_type'
                result[key] = self._clean_line(value)

            # special procedure for authors and editors
            elif key == 'author':
                if result.has_key('author'):
                    result[key].append(self._clean_line(value))
                else:
                    result[key] = [ self._clean_line(value) ]
                    
            elif (key == 'editor'):
                if result.has_key('editor'):
                    result[key].append(self._clean_line(value)) 
                else:
                    result[key] = [ self._clean_line(value) ]
                    
            elif key == 'keywords':
                if not result.has_key(key):
                    result[key] = self._split_comma_separated(value) 
                else:
                    result[key].append(self._clean_line(value))
            else:
                value = self._clean_line(value)
                result[key] = value
                
        if result.get('author'):
            result['author'] = self._format_names(result, 'author')
        
        if result.get('editor'):
            result['editor'] = self._format_names(result, 'editor')

        return result

    def _format_names(self, result, key='author'):
        """
        Formats a list of author/editor names
        """
        name_list = []
        newn_list = []

        if result.has_key(key):
            for each in result[key]:
                each = each.replace(' AND ', ' and ')
                name_list.extend(each.split(' and '))

        if name_list:
            name_list = [x for x in name_list if x]
            for name in name_list:
                newn_list.append(split_name(name))
        return newn_list

    def _split_separated_values(self, value, delim=','):
        """
        Splits multiple values separated by 'delim'. By default, delim is a 
        comma.
        """
        value = self.clean(value)
        result = []
        for item in value.split(delim):
            item = item.strip()
            if item:
                result.append(item)
        return result

    def _clean(self, value):
        """
        This method removes braces and quotes from the beginning and the ending
        of the value.
        """
        value = value.replace('{', '').replace('}', '').strip()
        if value and value[0] == '"' and len(value) > 1:
            value = value[1:-1]
        return value

    def _clean_line(self, value):
        return self._clean(value.rstrip(' ,'))

    def _group(self, p, n):
        """ Group a sequence p into a list of n tuples."""
        mlen, lft = divmod(len(p), n)
        if lft != 0: 
            mlen += 1

        # initialize a list of suitable length
        lst = [[None] * n for i in range(mlen)]

        # Loop over all items in the input sequence
        for i in range(len(p)):
            j, k = divmod(i, n)
            lst[j][k] = p[i]

        return map(tuple, lst)
