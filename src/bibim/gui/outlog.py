
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

from PyQt4 import QtCore #@UnresolvedImport
import logging #@UnresolvedImport


class GUIHandler(logging.Handler, QtCore.QObject):
    
    messageLogged = QtCore.pyqtSignal(QtCore.QString, QtCore.QString)
    
    def __init__(self, parent=None, level=logging.INFO, omit_levels=[]):
        QtCore.QString.__init__(self, parent)
        logging.Handler.__init__(self)        
        
        self.setLevel(level)
        self.omit_levels = omit_levels
        
        self.setFormatter(logging.Formatter('%(threadName)-10s\t - %(message)s'))

    def emit(self, record):
        if record.levelname in self.omit_levels:
            return
        
        message = self.format(record)
        if not message:
            return
        self.messageLogged.emit(message, record.levelname)
