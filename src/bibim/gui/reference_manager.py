
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

from bibim import log
from bibim.db.gateways import ExtractionGateway
from bibim.gui.reference_editor import ReferenceEditor
from bibim.gui.ui.ui_reference_manager import Ui_ReferenceManagerPage
from bibim.gui.custom_widgets import ConfirmMessageBox

class ReferenceManagerPage(QtGui.QWizardPage):
    
    def __init__(self, title, parent=None):
        super(ReferenceManagerPage, self).__init__(parent)
        self.parent = parent
        self.last_selected = None
        
        self.setButtonText(QtGui.QWizard.FinishButton, "Save changes")
        
        self.ui = Ui_ReferenceManagerPage()
        self.ui.setupUi(self)
        self.setTitle(title)
        self.set_references_context_menu()
                
        self.editor = ReferenceEditor(self)
        self.ui.referenceEditorLayout.addWidget(self.editor)
        
        self.editor.filePathChanged.connect(self._change_show_string)
        
        self.ui.references.itemSelectionChanged.connect(self.update_extraction_editor)

    def set_references_context_menu(self):
        self.ui.new_reference = QtGui.QAction("New Reference", self.ui.references)
        self.ui.new_reference.triggered.connect(self._create_new_reference)
        self.ui.references.addAction(self.ui.new_reference)
        
        self.ui.delete_action = QtGui.QAction("Delete Selected", self.ui.references)
        self.ui.delete_action.triggered.connect(self._delete_selected_reference)
        self.ui.references.addAction(self.ui.delete_action)

    def initializePage(self):
        log.debug("Initializing references page.")  #@UndefinedVariable

        extractions = self.parent.extraction_gw.find_extractions()
        for extraction in extractions:
            self._add_extraction(extraction)
    
    def _change_show_string(self, new):
        log.debug('Changing show string for current item') #@UndefinedVariable
        
        if self.last_selected:
            show_path = self._get_show_string(str(new))
            self.last_selected.show_path = show_path
            self.last_selected.setText(0, show_path) 
    
    def _add_extraction(self, extraction):
        item = QtGui.QTreeWidgetItem(self.ui.references)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        
        item.extraction = extraction
        item.show_path = self._get_show_string(extraction.file_path)
        
        item.setText(0, QtGui.QApplication.translate("", item.show_path,
            None, QtGui.QApplication.UnicodeUTF8))
        
        return item

    def _create_new_reference(self):
        extraction = self.parent.extraction_gw.new_extraction()
        item = self._add_extraction(extraction)
        
        log.debug('Changing selection to the new item') #@UndefinedVariable
        # Change selection to current wrapper
        try:
            self.ui.references.setItemSelected(self.last_selected, False)
        except:
            log.debug('Error unselecting extraction') #@UndefinedVariable
        self.ui.references.setItemSelected(item, True)
        
    def _delete_selected_reference(self):
        if not self.last_selected:
            return
        
        # Confirmation message
        item_text = '"%s..."' % self.last_selected.text(0)[:20]
        msg_box = ConfirmMessageBox(self)
        msg_box.setText('Are you sure you want to delete reference %s?' % 
                        item_text)
        result = msg_box.exec_()
        
        if result == QtGui.QMessageBox.Cancel:
            log.debug('Deletion of %s aborted' % item_text) #@UndefinedVariable
            return
        
        # Reference deletion
        log.debug('Deleting reference %s' % item_text) #@UndefinedVariable
        self.parent.extraction_gw.delete(self.last_selected.extraction)
        self.ui.references.setItemSelected(self.last_selected, False)
        self.ui.references.removeItemWidget(self.last_selected, 0)
        self.last_selected = None

    def update_extraction_editor(self):
        # Save current changes
        if self.last_selected: 
            self.editor.update()
        items = self.ui.references.selectedItems()
        if not items:
            return
        self.last_selected = items[0]
        self.editor.populate(self.last_selected.extraction)

    def _get_show_string(self, string):
        split_string = string.rsplit('/', 1) 
        if len(split_string) == 2:
            return split_string[1]
        else:
            return split_string[0]


class ReferenceManagerWizard(QtGui.QWizard):

    def __init__(self):
        super(ReferenceManagerWizard, self).__init__()
        self.initialize()

    def initialize(self):
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        
        self.extraction_gw = ExtractionGateway()
        
        wizard_title = 'Manage References'
        self.page01 = ReferenceManagerPage(wizard_title, self)
        self.addPage(self.page01)

    def show(self):
        self.removePage(0)
        self.initialize()
        self.restart()
        super(ReferenceManagerWizard, self).show()

    def done(self, status):
        self.extraction_gw.flush()
