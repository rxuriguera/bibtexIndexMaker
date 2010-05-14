
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
from bibim.gui.ui.ui_new_collection_dialog import Ui_NewWrapperCollection

class FileChooser(QtGui.QWidget):
    DIR = 0
    FILE = 1
    pathChanged = QtCore.pyqtSignal()
    
    def __init__(self):
        super(FileChooser, self).__init__()
        
        # Setup ui
        self.ui = Ui_FileChooser()
        self.ui.setupUi(self)
        
        self.path = QtCore.QString()
        
        self.mode = self.DIR
        
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
        if self.mode == self.DIR:
            self.path = QtGui.QFileDialog.getExistingDirectory(self)
        else:
            self.path = QtGui.QFileDialog.getOpenFileName(self)
        
        if self.path:
            self.ui.pathLine.setText(self.path)


class WrapperCollectionBox(QtGui.QDialog):
    def __init__(self, parent=None):
        super(WrapperCollectionBox, self).__init__()
        self.ui = Ui_NewWrapperCollection()
        self.ui.setupUi(self)
        self.setModal(True)
        
        # OK Button disabled until both url and field are not empty
        self.ok_button = self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        
        self.ui.urlLine.textChanged.connect(self._enable_ok_button)
        self.ui.fieldLine.textChanged.connect(self._enable_ok_button)
        
    def _enable_ok_button(self):
        if not (self.ui.urlLine.text() and self.ui.fieldLine.text()):
            self.ok_button.setEnabled(False)
        else:
            self.ok_button.setEnabled(True)
        
        
class ConfirmMessageBox(QtGui.QMessageBox):
    def __init__(self, parent=None):
        super(ConfirmMessageBox, self).__init__(parent)
        self.setModal(True)
        self.setStandardButtons(QtGui.QMessageBox.Ok | 
                                QtGui.QMessageBox.Cancel)
        self.setDefaultButton(QtGui.QMessageBox.Cancel)
        self.setIcon(QtGui.QMessageBox.Question)
