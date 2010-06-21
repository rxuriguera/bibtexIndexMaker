
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


class BibimManagerWizard(object):
    
    def __init__(self):
        self.populating = False
    
    def enter_populating(self):
        self.populating = True
        
    def exit_populating(self):
        self.populating = False

    def add_last_row(self, tree, check_populating=True):
        if check_populating and self.populating:
            return
        
        log.debug('Adding empty row to list') #@UndefinedVariable
        
        n_items = tree.topLevelItemCount()
        cols = tree.columnCount()
        
        if n_items == 0:
            add_row = True 
        else:
            last = tree.topLevelItem(n_items - 1)
            add_row = len([i for i in range(cols) if not last.text(i)]) != cols
            
        if add_row:
            item = QtGui.QTreeWidgetItem(tree)
            item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            
        
