
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
from bibim.gui.ui.ui_reference_editor import Ui_ReferenceEditor

class ReferenceEditor(QtGui.QWidget):

    filePathChanged = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self, parent=None):
        super(ReferenceEditor, self).__init__(parent)
        self.editor = Ui_ReferenceEditor()
        self.editor.setupUi(self)
        
        self.extraction = None
        self.populating = False
        self.for_update = False
        
        # Connect signals to update the reference if changed
        self.editor.filePathLine.textChanged.connect(self._mark_for_update)
        self.editor.filePathLine.textChanged.connect(self.filePathChanged)
        
        self.editor.resultLine.textChanged.connect(self._mark_for_update)
        self.editor.queryLine.textChanged.connect(self._mark_for_update)
        self.editor.validitySpin.valueChanged.connect(self._mark_for_update)
        self.connect(self.editor.fields, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._mark_for_update)
        self.connect(self.editor.authors, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._mark_for_update)
        self.connect(self.editor.editors, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._mark_for_update)
        
        # Add new row if last one is not empty
        self.connect(self.editor.fields, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self.add_fields_last_row)
        self.connect(self.editor.authors, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self.add_authors_last_row)
        self.connect(self.editor.editors, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self.add_editors_last_row)
    
    def set_extraction(self, extraction):
        self.load(extraction)
    
    def clear(self):
        """
        Clears all the information of the reference editor
        """
        self.editor.filePathLine.setText('')
        self.editor.resultLine.setText('')
        self.editor.queryLine.setText('')
        self.editor.validitySpin.setValue(0.0)
        
        self.editor.fields.clear()
        self.editor.authors.clear()
        self.editor.editors.clear()
        
    def create_last_rows(self):
        """
        Adds empty rows at the end of the lists for fields, authors and editors
        """
        item = QtGui.QTreeWidgetItem(self.editor.fields)
        item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        
        item = QtGui.QTreeWidgetItem(self.editor.authors)
        item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        
        item = QtGui.QTreeWidgetItem(self.editor.editors)
        item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
        
    def _mark_for_update(self):
        """
        Marks the current reference for update
        """
        if not self.populating:
            self.for_update = True
            log.debug("Reference marked for update") #@UndefinedVariable
    
    def update(self):
        """
        If needed, it updates the current extraction with all the changes made
        by the user.
        Changes won't be flushed to the database until 'Save changes' is
        clicked.
        """
        if not (self.extraction and self.for_update):
            return
        
        self.for_update = True
        self.extraction.file_path = unicode(self.editor.filePathLine.text())
        self.extraction.query_string = unicode(self.editor.queryLine.text())
        self.extraction.result_url = unicode(self.editor.resultLine.text())
   
        if not self.extraction.references:
            self.extraction.add_reference()
            
        reference = self.extraction.references[0]
        reference.validity = float(self.editor.validitySpin.value())
    
        self._update_fields(reference)
        self._update_people(self.editor.authors, reference.authors,
                           reference.add_author_by_name)
        self._update_people(self.editor.editors, reference.editors,
                           reference.add_editor_by_name)
    
    def _update_fields(self, reference):
        """
        Updates the fields of a reference
        """
        log.debug('Updating reference') #@UndefinedVariable
        for index in range(self.editor.fields.topLevelItemCount()):
            item = self.editor.fields.topLevelItem(index)
            
            # Remove empty items
            if ((len(reference.fields) > index) and 
                not (item.text(0) and item.text(1) and (item.text(2)))):
                reference.fields.pop(index) 
            
            # Skip non-empty items that have an invalid status
            if not ((item.text(2) == 'True' or item.text(2) == 'False')):
                continue
            
            log.debug('Index: %d Number of fields %d' % (index , len(reference.fields))) #@UndefinedVariable
            
            try:
                name = unicode(item.text(0))
                value = unicode(item.text(1))
                valid = True if str(item.text(2)) == "True" else False
            except TypeError, e:
                log.error('Type error when casting to store to database %s' % str(e)) #@UndefinedVariable
                continue
            
            if(len(reference.fields) > index):
                reference.fields[index].name = name
                reference.fields[index].value = value
                reference.fields[index].valid = valid
            else:
                reference.add_field(name, value, valid)
    
    def _update_people(self, tree, people, add_method):
        """
        Updates the lists of authors or editors from a reference. The one
        that gets updated is decided depending on the people and add_method
        parameteres.
        """
        for index in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(index)
            
            if not (item.text(0) or item.text(1) or item.text(2)):
                if(len(people) > index):
                    people.pop(index)
                continue
            
            log.debug("Index: %d Number of fields %d" % (index , len(people))) #@UndefinedVariable
            
            try:
                first_name = unicode(item.text(0))
                middle_name = unicode(item.text(1))
                last_name = unicode(item.text(2))
            except TypeError, e:
                log.error("Type error when casting to store to database %s" % str(e)) #@UndefinedVariable
                continue
            
            if(len(people) > index):
                people[index].name = first_name
                people[index].value = middle_name
                people[index].valid = last_name
            else:
                add_method(first_name, middle_name, last_name)

    def add_fields_last_row(self):
        self._add_last_row(self.editor.fields)
        
    def add_authors_last_row(self):
        self._add_last_row(self.editor.authors)
        
    def add_editors_last_row(self):
        self._add_last_row(self.editor.editors)
        
    def _add_last_row(self, tree):
        """
        Adds an empty row at the end of the qtreewidget, if there isn't one
        already
        """
        if self.populating:
            return
        
        n_items = tree.topLevelItemCount()
        columns = tree.columnCount()
        
        last_item = tree.topLevelItem(n_items - 1)
        empty = True
        for i in range(columns):
            if last_item.text(i):
                empty = False
            
        # Add a new row if the last field is not empty
        if not empty:
            item = QtGui.QTreeWidgetItem(tree)
            item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            
        log.debug("List contains %d items" % n_items) #@UndefinedVariable


    def enter_populating(self):
        self.populating = True
        
    def exit_populating(self):
        self.create_last_rows()
        self.for_update = False
        self.populating = False;

    def populate(self, extraction):
        if not extraction:
            return
        
        self.enter_populating()
        self.clear()
        self.extraction = extraction
        log.debug("Loading extraction for: %s" % extraction.file_path) #@UndefinedVariable
        
        self.editor.filePathLine.setText(extraction.file_path)
        self.editor.queryLine.setText(extraction.query_string)
        self.editor.resultLine.setText(extraction.result_url)

        if not extraction.references:
            self.exit_populating()
            return

        reference = extraction.references[0]
        self.editor.validitySpin.setValue(reference.validity)
        
        # Add fields
        for field in reference.fields:
            item = QtGui.QTreeWidgetItem(self.editor.fields)
            item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            item.setText(0, field.name)
            item.setText(1, field.value)
            item.setText(2, repr(field.valid))

        self.populate_people(self.editor.authors, reference.authors)
        self.populate_people(self.editor.editors, reference.editors)

        self.exit_populating()
        
        
    def populate_people(self, tree, people):    
        for person in people:
            item = QtGui.QTreeWidgetItem(tree)
            item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            if(person.person.first_name):
                item.setText(0, person.person.first_name)
            if(person.person.middle_name):    
                item.setText(1, person.person.middle_name)
            if(person.person.last_name):
                item.setText(2, person.person.last_name)
            
