
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


from bibim.util.helpers import (FileFormat,
                                ReferenceFormat)
from bibim.rce import PDFTextExtractor
from bibim.ir.search import (Searcher,
                             ScholarSearch,
                             BingSearch,
                             YahooSearch,
                             GoogleJSONSearch)
from bibim.references.parsers.bibtex import BibtexParser
from bibim.references.format.generator import BibtexGenerator


class UtilCreationError(Exception):
    pass


class UtilFactory(object):
    
    _extractors = {FileFormat.TXT:{FileFormat.PDF:PDFTextExtractor}}
    
    def create_extractor(self, source_format, target_format):
        if target_format in self._extractors.keys():
            if source_format in self._extractors[target_format].keys():
                return self._extractors[target_format][source_format]()
        raise UtilCreationError('Converter from %s to %s is not available' % 
                                (source_format, target_format))

    def create_searcher(self, engine):
        if engine == Searcher.GOOGLE:
            return GoogleJSONSearch()
        elif engine == Searcher.SCHOLAR:
            return ScholarSearch()
        elif engine == Searcher.BING:
            return BingSearch()
        elif engine == Searcher.YAHOO:
            return YahooSearch()
        else:
            raise UtilCreationError('Requested searcher is not available')

    def create_parser(self, format):
        if format == ReferenceFormat.BIBTEX:
            return BibtexParser()
        else:
            raise UtilCreationError('Parser for %s is not available' % format)

    def create_generator(self, format):
        if format == ReferenceFormat.BIBTEX:
            return BibtexGenerator()
        else:
            raise UtilCreationError('Generator for %s is not available' 
                                    % format)
