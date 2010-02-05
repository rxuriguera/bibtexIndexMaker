# Copyright 2010 Ramon Xuriguera
#
# This file is part of BibtexIndexMaker RCE. 
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net -- good coders code, great reuse
# http://www.catonmat.net/blog/python-library-for-google-search/
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
            raise IOError
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
        'Darwin':'../../../xpdf/linux/pdftotext', #MAC OS 
        'Linux':'../../../xpdf/linux/pdftotext',
        'Windows':'../../../xpdf/windows/pdftotext.exe'
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
        
        command = [self._pdf_extraction_tool, '-f', '1', '-l', '1', '-enc',
                   'UTF-8', '-htmlmeta', input_file, '-']
        try:
            pop = subprocess.Popen(command, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as cpe:
            log.error ('Error executing PDF text extraction tool. Return code: ' 
                   + repr(cpe.returncode))
        except OSError:
            log.error ('PDF extraction tool not found')
        else:
            return pop.communicate()[0]

        
