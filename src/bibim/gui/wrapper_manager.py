
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

import simplejson #@UnresolvedImport

from bibim import log
from bibim.db.gateways import WrapperGateway
from bibim.gui.ui.ui_wrapper_manager import Ui_WrapperManagerPage
from bibim.gui.bibim_manager import BibimManagerWizard
from bibim.gui.custom_widgets import (WrapperCollectionBox,
                                      ConfirmMessageBox)
from bibim.ie.rating import AverageRater


class WrapperManagerPage(QtGui.QWizardPage, BibimManagerWizard):
    
    def __init__(self, title, parent=None):
        super(WrapperManagerPage, self).__init__(parent)
        self.parent = parent
        
        self.last_selected_collection = None
        self.last_selected_wrapper = None
        
        self.collection_for_update = False
        self.wrapper_for_update = False
        
        self.collections_top_level = []
        
        self.setButtonText(QtGui.QWizard.FinishButton, "Save changes")
        
        self.ui = Ui_WrapperManagerPage()
        self.ui.setupUi(self)
        self.setTitle(title)
        self.set_collections_context_menu()
        self.set_wrappers_context_menu()
        
        self.ui.collections.itemSelectionChanged.connect(self._populate_collection_wrappers)
        self.ui.wrappers.itemSelectionChanged.connect(self._populate_wrapper_editor)
        
        self.ui.upvotesSpin.valueChanged.connect(self._refresh_score_value)
        self.ui.downvotesSpin.valueChanged.connect(self._refresh_score_value)
        
        self.connect(self.ui.rules, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._mark_wrapper_for_update)
        self.connect(self.ui.rules, QtCore.SIGNAL("itemChanged(QTreeWidgetItem *,int)"), self._add_rules_last_row)
        
    def initializePage(self):
        self._populate_collections()

    def set_collections_context_menu(self):
        self.ui.new_collection = QtGui.QAction("New Collection",
                                               self.ui.collections)
        self.ui.new_collection.triggered.connect(self._create_new_collection)
        self.ui.collections.addAction(self.ui.new_collection)
        
        self.ui.delete_collection = QtGui.QAction("Delete Collection",
                                                  self.ui.collections)
        self.ui.delete_collection.triggered.connect(
                                            self._delete_selected_collection)
        self.ui.collections.addAction(self.ui.delete_collection)

    def set_wrappers_context_menu(self):
        self.ui.new_wrapper = QtGui.QAction("New Wrapper",
                                               self.ui.wrappers)
        self.ui.new_wrapper.triggered.connect(self._create_new_wrapper)
        self.ui.wrappers.addAction(self.ui.new_wrapper)
        
        self.ui.delete_wrapper = QtGui.QAction("Delete Wrapper",
                                                  self.ui.wrappers)
        self.ui.delete_wrapper.triggered.connect(
                                            self._delete_selected_wrapper)
        self.ui.wrappers.addAction(self.ui.delete_wrapper)

    def _create_new_collection(self):
        """
        Creates, if possible, a new collection of wrappers for a url and field
        name
        """
        collection_box = WrapperCollectionBox(self)
        result = collection_box.exec_()
        
        if result == QtGui.QDialog.Rejected:
            log.debug('Collection creation aborted') #@UndefinedVariable
            return
        
        log.debug('Creating new collection %s %s' % (collection_box.ui.urlLine.text(), collection_box.ui.fieldLine.text())) #@UndefinedVariable
        
        url = unicode(collection_box.ui.urlLine.text())
        field = unicode(collection_box.ui.fieldLine.text())
    
        collection = self.parent.wrapper_gw.new_wrapper_collection()
        collection.url = url
        collection.field = field
        item = self._add_collection(collection)
        self.ui.collections.setItemExpanded(item.parent(), True)
        self.ui.collections.setItemSelected(item, True)

    def _delete_selected_collection(self):
        if not self.last_selected_collection:
            return
        
        # Confirmation message
        item_text = '%s:%s' % (self.last_selected_collection.collection.url,
                               self.last_selected_collection.collection.field)
        
        msg_box = ConfirmMessageBox(self)
        msg_box.setText('Are you sure you want to delete collection %s?' % 
                        item_text)
        result = msg_box.exec_()
        
        if result == QtGui.QMessageBox.Cancel:
            log.debug('Deletion of %s aborted' % item_text) #@UndefinedVariable
            return
        
        # Reference deletion
        log.debug('Deleting collection %s' % item_text) #@UndefinedVariable
        self._clear_wrappers()
        self.parent.wrapper_gw.delete(self.last_selected_collection.collection)
        self.ui.collections.setItemSelected(self.last_selected_collection,
                                            False)
        self.ui.collections.removeItemWidget(self.last_selected_collection, 0)
        
        item_parent = self.last_selected_collection.parent()
        if item_parent.childCount() == 1:
            log.debug('Removing top level item') #@UndefinedVariable
            self.ui.collections.removeItemWidget(item_parent, 0)
        self.last_selected_collection = None

    def _create_new_wrapper(self):
        """
        Creates a new wrapper
        """
        if not self.last_selected_collection:
            return
        
        # A new wrapper has been requested by the user
        self._mark_collection_for_update()
        self._mark_wrapper_for_update()
        
        item = QtGui.QTreeWidgetItem(self.ui.wrappers)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item.setText(0, 'New Wrapper')
        item.wrapper = self.parent.wrapper_gw.new_wrapper()
        self.last_selected_collection.collection.wrappers.append(item.wrapper)
        log.debug('Generated new wrapper') #@UndefinedVariable
        
        log.debug('Changing selection') #@UndefinedVariable
        # Change selection to current wrapper
        try:
            self.ui.wrappers.setItemSelected(self.last_selected_wrapper, False)
        except:
            log.debug('Error unselecting wrapper') #@UndefinedVariable
        self.ui.wrappers.setItemSelected(item, True)
        
        
    def _delete_selected_wrapper(self):
        if not self.last_selected_wrapper:
            return
        
        # Confirmation message
        item_text = self.last_selected_wrapper.text(0)
        msg_box = ConfirmMessageBox(self)
        msg_box.setText('Are you sure you want to delete wrapper %s?' % 
                        item_text)
        result = msg_box.exec_()
        
        if result == QtGui.QMessageBox.Cancel:
            log.debug('Deletion of %s aborted' % item_text) #@UndefinedVariable
            return
        
        # Reference deletion
        log.debug('Deleting wrapper %s' % item_text) #@UndefinedVariable
        self._clear_wrapper_editor()
        self.parent.wrapper_gw.delete(self.last_selected_wrapper.wrapper)
        self.ui.wrappers.setItemSelected(self.last_selected_wrapper, False)
        self.ui.wrappers.removeItemWidget(self.last_selected_wrapper, 0)
        self.last_selected_wrapper = None
        
    def _add_rules_last_row(self):
        self.add_last_row(self.ui.rules)                
                
    def _populate_collections(self):
        """
        Adds all the collections from the database to the collections list,
        grouped by url.
        """
        log.debug("Populating collections list") #@UndefinedVariable    
        self.enter_populating()
        for collection in self.parent.wrapper_gw.find_wrapper_collections():
            self._add_collection(collection)
        self.exit_populating()
    
    def _add_collection(self, collection):
        """
        Adds a collection to the list widget.
        """
        if collection.url in self.collections_top_level:
            item0 = self.ui.collections.topLevelItem(self.collections_top_level.index(collection.url))
        else:
            self.collections_top_level.append(collection.url)
            item0 = QtGui.QTreeWidgetItem(self.ui.collections)
            item0.setFlags(QtCore.Qt.ItemIsEnabled)
            item0.setText(0, QtGui.QApplication.translate("", collection.url,
                        None, QtGui.QApplication.UnicodeUTF8))
            
        # Add sub item
        item1 = QtGui.QTreeWidgetItem(item0)
        item1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item1.setText(0, QtGui.QApplication.translate("", collection.field,
            None, QtGui.QApplication.UnicodeUTF8)) 
        item1.collection = collection
        return item1
        
    def _populate_collection_wrappers(self):
        """
        Populates the list of wrappers with all the wrappers of the current
        selected collection
        """
        log.debug("Populating wrappers list") #@UndefinedVariable
        
        # Before changing to the new collection, update the last selected one
        self._update_wrapper()
        self._update_collection()
        
        # Change to the new selected collection
        items = self.ui.collections.selectedItems()
        if not items:
            return
        self.last_selected_collection = items[0]
        collection = items[0].collection   
        
        # Reset marked for update flags
        self.collection_for_update = False
        self.wrapper_for_update = False 
        
        # Start populating the list of wrappers
        self.enter_populating()
        self._clear_wrappers()
        for wrapper in collection.wrappers:
            item = QtGui.QTreeWidgetItem(self.ui.wrappers)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
            if wrapper.id:
                show_string = 'Wrapper %d' % wrapper.id
            else:
                show_string = 'New wrapper'
            show_string = ''.join([show_string, ', Score %.2f' % (wrapper.score)])
            item.setText(0, QtGui.QApplication.translate("", show_string,
                            None, QtGui.QApplication.UnicodeUTF8))
            item.wrapper = wrapper
        self.exit_populating()
    
    def _populate_wrapper_editor(self):
        """
        Populate the wrapper editor with the current selected wrapper
        """
        log.debug("Populating wrapper editor") #@UndefinedVariable
        
        # Before changing to the new wrapper, update the last selected one
        self._update_wrapper()
        
        # Change to the new selected wrapper    
        log.debug('Move to selected item') #@UndefinedVariable
        items = self.ui.wrappers.selectedItems()
        if not items:
            return
        self.last_selected_wrapper = items[0]
        wrapper = items[0].wrapper  
        
        self.enter_populating()
        self._clear_wrapper_editor()
        
        self.wrapper_for_update = False
        
        self.ui.upvotesSpin.setValue(wrapper.upvotes)
        self.ui.downvotesSpin.setValue(wrapper.downvotes)
        self.ui.scoreSpin.setValue(wrapper.score)
        
        for rule in wrapper.rules:
            item = QtGui.QTreeWidgetItem(self.ui.rules)
            item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            item.setText(0, rule.rule_type)
            item.setText(1, rule.pattern)
            item.setText(2, str(rule.order))
            item.rule = rule
        self.add_last_row(self.ui.rules, False)
        
        log.debug("Wrapper editor populated") #@UndefinedVariable
        
        self.exit_populating()
    
    def _clear_collections(self):
        self.ui.collections.clear()
    
    def _clear_wrappers(self):
        """
        Clears the wrappers list and the wrapper editor
        """
        self.ui.wrappers.clear()
        self._clear_wrapper_editor()
    
    def _clear_wrapper_editor(self):
        """
        Clears all the data from the wrapper editor
        """
        self.ui.rules.clear()
        self.ui.upvotesSpin.setValue(0)
        self.ui.downvotesSpin.setValue(0)
        self.ui.scoreSpin.setValue(0.0)
        
    def _refresh_score_value(self):
        """
        Refreshes the value of the score spin box depending on the upvotes and
        downvotes
        """
        self._mark_wrapper_for_update()
        upvotes = int(self.ui.upvotesSpin.value())
        downvotes = int(self.ui.downvotesSpin.value()) 
        score = AverageRater().rate(upvotes, downvotes)
        self.ui.scoreSpin.setValue(score)

    def _mark_collection_for_update(self):
        """
        Marks a collection for update if there have been changes to it and
        needs to be updated.
        Changes made to the collection while populating fields are discarded.
        """
        if not self.populating:
            self.collection_for_update = True
            log.debug('Marked collection for update') #@UndefinedVariable
            
    def _mark_wrapper_for_update(self):
        """
        Marks a wrapper for update if there have been changes to it and
        needs to be updated.
        Changes made to the collection while populating fields are discarded.
        """
        if not self.populating:
            self.wrapper_for_update = True
            log.debug('Marked wrapper for update') #@UndefinedVariable
    
    def _update_collection(self):
        """
        Updates last selected collection adding more wrappers to it if 
        necessary.
        """
        if not (self.collection_for_update and self.last_selected_collection):
            return
        log.debug('Updating last selected collection') #@UndefinedVariable
        
        collection = self.last_selected_collection.collection

        for index in range(self.ui.wrappers.topLevelItemCount()):
            item = self.ui.wrappers.topLevelItem(index)
            if item not in collection.wrappers:
                #item.wrapper.collection_id = collection.id
                log.debug('Adding new wrapper to collection') #@UndefinedVariable
                collection.wrappers.append(item.wrapper)
    
    def _update_wrapper(self):
        """
        Updates last selected wrapper with any changed values of new rules
        """
        if not (self.wrapper_for_update and self.last_selected_wrapper):
            return
        log.debug('Updating last selected wrapper') #@UndefinedVariable
        
        wrapper = self.last_selected_wrapper.wrapper

        self._update_score(wrapper)
        self._update_rules(wrapper)
    
    def _update_score(self, wrapper):
        """
        Updates the score of a wrapper. To do it, it uses an AverageRater, to 
        establish the score depending on the upvotes and downvotes
        """
        # No need to try/except, spins only allow int and floats
        upvotes = int(self.ui.upvotesSpin.value())
        downvotes = int(self.ui.downvotesSpin.value()) 
        score = float(self.ui.scoreSpin.value())
        
        wrapper.upvotes = upvotes
        wrapper.downvotes = downvotes
        wrapper.score = score
        
    def _update_rules(self, wrapper):
        for index in range(self.ui.rules.topLevelItemCount() - 1):
            item = self.ui.rules.topLevelItem(index)
            
            log.debug('Updating rule %d' % index) #@UndefinedVariable
            
            # Remove empty items
            if ((len(wrapper.rules) > index) and 
                not (item.text(0) and item.text(1) and item.text(2))):
                wrapper.rules.pop(index)
                continue
            
            # Skip non-empty items that have an invalid status
            try:
                rule_type = str(item.text(0))
                pattern = str(item.text(1))
                order = int(str(item.text(2)))
            except (TypeError, ValueError):
                log.error('Error when casting to store to database') #@UndefinedVariable
                continue
            
            # Check that the pattern can be converted to a python object
            try:
                pattern_py = simplejson.loads(pattern) #@UnusedVariable
            except ValueError:
                log.debug('Cannot convert pattern %s to Python objects' % pattern) #@UndefinedVariable
                continue
            
            # Update or append the rules
            if(len(wrapper.rules) > index):
                wrapper.rules[index].rule_type = rule_type
                wrapper.rules[index].pattern = pattern
                wrapper.rules[index].order = order
            else:
                wrapper.add_rule_by_info(rule_type, pattern, order)

        
class WrapperManagerWizard(QtGui.QWizard):
    
    def __init__(self):
        super(WrapperManagerWizard, self).__init__()
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        
        self.wrapper_gw = WrapperGateway()
        
        wizard_title = 'Manage Wrappers'
        self.page01 = WrapperManagerPage(wizard_title, self)
        self.addPage(self.page01)

    def done(self, status):
        self.page01._update_collection()
        self.page01._update_wrapper()
        self.wrapper_gw.flush()
