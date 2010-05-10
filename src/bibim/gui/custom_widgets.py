
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

from PyQt4 import QtCore, QtGui #@UnresolvedImport

from bibim.gui.ui.ui_file_chooser import Ui_FileChooser

class FileChooser(QtGui.QWidget):
    pathChanged = QtCore.pyqtSignal()
    
    def __init__(self):
        super(FileChooser, self).__init__()
        
        # Setup ui
        self.ui = Ui_FileChooser()
        self.ui.setupUi(self)
        
        self.path = QtCore.QString()
        
        # Connect signals and slots
        #self.connect(self.ui.browseButton, QtCore.SIGNAL('clicked()'), self.chooseFile)
        self.ui.browseButton.clicked.connect(self.chooseFile)

    def get_path(self):
        return self.__path

    def set_path(self, value):
        self.__path = value
        self.pathChanged.emit()

    path = QtCore.pyqtProperty(QtCore.QString, get_path, set_path)

    @QtCore.pyqtSlot()
    def chooseFile(self):
        self.path = QtGui.QFileDialog.getExistingDirectory(self)
        if self.path:
            self.ui.pathLine.setText(self.path)

            
