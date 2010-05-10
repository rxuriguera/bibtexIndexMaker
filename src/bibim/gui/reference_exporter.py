
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
from bibim.main.entry import ReferenceEntryFormatter
from bibim.gui.ui.ui_reference_exporter import Ui_ReferenceExporterPage


class ReferenceFormatterThread(QtCore.QThread):
    def __init__(self, parent=None, reference_formatter=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.reference_formatter = reference_formatter 
        self.items = []
        self.formatted_references = []
        
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        self.formatted_references = []
        for item in self.items:
            if not item.extraction.references:
                log.warn('Item has no references') #@UndefinedVariable
                continue
            
            if item.reference_entry:
                self.formatted_references.append(item.reference_entry)
                continue
        
            id = item.extraction.references[0].id
            log.debug('Formatting reference with id %d' % id) #@UndefinedVariable
            entry = self.reference_formatter.format_reference(id)
            if(entry):
                log.debug('Reference with id %d formatted' % id) #@UndefinedVariable
                self.formatted_references.append(entry)
                item.reference_entry = entry


class ReferenceExporterpage(QtGui.QWizardPage):
    
    def __init__(self, title, parent=None):
        super(ReferenceExporterpage, self).__init__(parent)
        self.parent = parent
        
        self.populating = False
        self.reference_formatter = ReferenceEntryFormatter()
        
        self.setButtonText(QtGui.QWizard.FinishButton, "Save changes")
        
        self.ui = Ui_ReferenceExporterPage()
        self.ui.setupUi(self)
        self.setTitle(title)
        
        self.connect(self.ui.references, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._format_references)
        
    def initializePage(self):
        log.debug("Initializing references list.")  #@UndefinedVariable

        self.enter_populating()
        extractions = self.parent.extraction_gw.find_extractions()
        for extraction in extractions:
            self._add_extraction(extraction)
        self.exit_populating()
        
        self.thread = ReferenceFormatterThread(self, self.reference_formatter)
        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self._update_export_edit)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self._update_export_edit)
    
    def enter_populating(self):
        self.populating = True
        
    def exit_populating(self):
        self.populating = False
    
    def _add_extraction(self, extraction):
        item = QtGui.QTreeWidgetItem(self.ui.references)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        
        item.extraction = extraction
        item.show_path = self._get_show_string(extraction.file_path)
        
        item.setText(0, QtGui.QApplication.translate("", item.show_path,
            None, QtGui.QApplication.UnicodeUTF8))
        item.setCheckState(0, QtCore.Qt.Unchecked)
        item.reference_entry = None
        return item
    
    def _format_references(self):
        if self.populating:
            return
        
        log.debug('Item checked/unchecked') #@UndefinedVariable
        self.ui.entriesEdit.setText('Updating...')
        
        items = self._get_checked_items()
        log.debug('Items selected: %d' % len(items)) #@UndefinedVariable
        
        self.thread.items = items
        self.thread.start()
    
    def _get_checked_items(self):
        items = []
        for index in range(self.ui.references.topLevelItemCount()):
            item = self.ui.references.topLevelItem(index)
            if item.checkState(0) == QtCore.Qt.Checked:
                items.append(item)
        return items
    
    def _update_export_edit(self):
        log.debug('Finished formatting: %d formatted references' % #@UndefinedVariable 
                  len(self.thread.formatted_references))
        formatted_references = self.thread.formatted_references
        
        text = ''
        for reference in formatted_references:
            text = ''.join([text, reference, '\n\n'])
        
        self.ui.entriesEdit.setText(text)
        
    def _get_show_string(self, string):
        split_string = string.rsplit('/', 1) 
        if len(split_string) == 2:
            return split_string[1]
        else:
            return split_string[0]


class ReferenceExporterWizard(QtGui.QWizard):

    def __init__(self):
        super(ReferenceExporterWizard, self).__init__()
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        
        self.extraction_gw = ExtractionGateway()
        
        wizard_title = 'Export References'
        self.page01 = ReferenceExporterpage(wizard_title, self)
        self.addPage(self.page01)


        
