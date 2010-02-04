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
import os.path

from bibim.rce.document import Document


class Extractor(object):
    """
    Extractor provides methods for content extraction.
    """
    
    def __init__(self):
        pass

    def _get_input_file(self):
        return self._input_file

    def _set_input_file(self, file_name):
        if not os.path.isfile(file_name):
            raise IOError
        self._input_file = file_name
    
    _input_file = property(_get_input_file, _set_input_file)
    
    def extract(self):
        raise NotImplementedError()
    


class TextExtractor(Extractor):
    """
    TextExtractor provides methods to extract text from other kind of documents.  
    """

    def __init__(self):
        """
        Constructor
        """
        pass
        
class PDFTextExtractor(TextExtractor):
    """
    This class allows text extraction from PDF documents.
    """

    _pdf_extration_tool = {'darwin':'../../../xpdf/linux/pdftotext', # MAC OS uses same binaries as linux
                           'linux':'../../../xpdf/linux/pdftotext',
                           'windows':'../../../xpdf/windows/pdftotext.exe'}

    def __init__(self):
        """
        """
        pass
    
    def _get_pdf_tool(self):
        platform = platform.system()
        
        if platform not in self._pdf_extration_tool.keys():
            raise
        
        return self._pdf_extration_tool[platform]
    
    def extract(self):
        command = [self._get_pdf_tool(), '-f', '1', '-l', '1', '-enc', 'UTF-8', '-htmlmeta', self._input_file, '-']
        try:
            pop = subprocess.Popen(command, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print 'Error executing PDF text extraction tool. Return code: ' + repr(e.returncode)
        
        return pop.communicate()[0]
