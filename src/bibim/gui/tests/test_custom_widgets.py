
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

import sys
import unittest #@UnresolvedImport

from PyQt4 import QtGui #@UnresolvedImport
from bibim.gui.custom_widgets import FileChooser


from bibim.gui.reference_extraction import ReferenceExtractionWizard


class TestFileChooser(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def xtestFileChooser(self):
        self.app = QtGui.QApplication(sys.argv)
        window = FileChooser()
        window.show()
        sys.exit(self.app.exec_())
        # It's exec_ because exec is a reserved word in Python
    
    def testMakeIndex(self):
        self.app = QtGui.QApplication(sys.argv)
        window = ReferenceExtractionWizard()
        window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
