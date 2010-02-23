# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker RCE. 
#
#
# BibtexIndexMaker RCE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BibtexIndexMaker RCE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BibtexIndexMaker RCE. If not, see <http://www.gnu.org/licenses/>.


import platform #@UnresolvedImport
import subprocess #@UnresolvedImport
from os import path

from bibim import log
from bibim.document import Document
from bibim.util import BeautifulSoup

class ExtractionError(Exception):
    
    """
    Raised when the content of the file cannot be extracted or the file is
    corrupted.
    """

class Extractor(object):
    
    """
    Extractor provides methods for content extraction.
    """
    
    def __init__(self):
        pass

    def _check_input_file(self, input_file):
        """
        Checks file existence and normalizes its path.
        """
        if not path.isfile(input_file):
            raise IOError('%s does not exist or is not a file.' % input_file)
        return path.normpath(input_file)
        
    def extract(self, input_file):
        raise NotImplementedError()
    

class TextExtractor(Extractor):
    
    """
    TextExtractor provides methods to extract text from other kind of 
    documents.  
    """


class PDFTextExtractor(TextExtractor):
    """
    This class allows text extraction from PDF documents.
    """

    _tool_path = {
        'Darwin':'../../../tools/xpdf/linux/pdftotext', # MAC OS 
        'Linux':'../../../tools/xpdf/linux/pdftotext',
        'Windows':'../../../tools/xpdf/windows/pdftotext.exe'
    }
    
    @property
    def _pdf_extraction_tool(self):
        """
        Extraction tools normalised URL depending on the platform on which
        the method is invoked.
        """
        plat = platform.system()
        if plat not in self._tool_path.keys():
            plat = 'Linux'
        return path.normpath(path.join(path.dirname(__file__),
            (self._tool_path[plat])))
    
    def extract(self, input_file):
        input_file = self._check_input_file(input_file)
        # Extraction command and its options. They may be parametrized in the
        # future
        command = [self._pdf_extraction_tool, '-q', '-f', '1', '-l', '1',
                   '-enc', 'ASCII7', '-htmlmeta', input_file, '-']
        try:
            pop = subprocess.Popen(command, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as cpe:
            log.error ('Error executing PDF text extraction tool. Return code: ' #@UndefinedVariable
                   + repr(cpe.returncode))
        except OSError:
            log.error ('PDF extraction tool not found') #@UndefinedVariable
        
        stdout = pop.communicate()[0]
        if not stdout:
            raise ExtractionError('Corrupted file')
        
        parser = BeautifulSoup(stdout)
        document = Document()
        self._extract_metadata(parser, document)
        self._extract_content(parser, document)

        return document
    
    def _extract_metadata(self, parser, document):
        # Title
        title = parser.find('title')
        if title:
            document.set_metadata_field('Title', title.find(text=True))
        # Rest of metadata
        metas = parser.findAll('meta')
        for meta in metas:
            document.set_metadata_field(meta['name'], meta['content'])
    
    def _extract_content(self, parser, document):
        pre = parser.find('pre')
        raw_content = pre.find(text=True).strip()
        if not raw_content:
            raise ExtractionError('Could not extract content') 
        document.content = raw_content
        
