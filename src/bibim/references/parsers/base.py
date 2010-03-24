
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
BibliographyParser main class
"""

import re
import os

class BibliographyParser(object):
    """
    Base class for the input parser of the bibliography tool.
    """
    delimiter = os.linesep + os.linesep
    # The Medline pattern as default
    pattern = r'(^.{0,4}- )' 

    def __init__(self):
        pass

    def get_delimiter(self):
        """
        Returns the delimiter used to split a list of entries into pieces
        """
        return self.delimiter

    def get_pattern(self):
        """
        Returns the pattern used to parse a single entry
        """
        return self.pattern

    def set_delimiter(self, delimiter=os.linesep + '{2,}', flags=None):
        """
        Sets the delimiter used to split a list of entries into pieces
        the 'delimiter' argument and the flags are passed to 're.compile'
        """
        if flags:
            self.delimiter = re.compile(delimiter, flags)
        else:
            self.delimiter = re.compile(delimiter)
        return None

    def set_pattern(self, pattern="\n", flags=None):
        """
        Sets the pattern used to parse a single entry
        the 'pattern' argument is passed to 're.compile')
        """
        if flags:
            self.pattern = re.compile(pattern, flags)
        else:
            self.pattern = re.compile(pattern)
        return None

    def check_format(self, source):
        """
        Checks whether source has the right format
        Returns True if so and False otherwise
        """
        pass # needs to be provided by the individual parsers

    def split_source(self, source):
        """
        Splits a (text) file with several entries
        Returns a list of those entries
        """
        source = self.preprocess(source)
        return self.delimiter.split(source)

    def parse_entry(self, entry):
        """
        Parses a single entry
        Returns a dictionary
        """
        pass  # needs to be overwriten by the individual parser

    def preprocess(self, source):
        """
        The behavior of this method will vary for each subclass. Basically, it
        will include anything related to expanding macros, stripping comments, 
        etc.
        """
        pass

    def get_entries(self, source):
        """
        Splits a (text) file with several entries
        Parses the entries
        Returns a list of the parsed entries
        """
        source = self.check_encoding(source)
        return [self.parse_entry(entry) \
                for entry in self.split_source(source)]

    def check_encoding(self, source):
        """
        Make sure we have utf encoded text
        """
        try:
            source = unicode(source, 'utf-8')
        except UnicodeDecodeError:
            source = unicode(source, 'iso-8859-15')
        return source.encode('utf-8')


class EntryParseError(Exception):
    """
    Parsers can return instances of this class when the parsing
    of an entry fails for whatever reason.
    """
    pass

