
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
from bibim.gui.custom_widgets import (FileChooser,
                                      LogsTextEdit)
from bibim.gui.outlog import GUIHandler
from bibim.main.entry import IndexMaker

import time

class ReferenceExtractionThread(QtCore.QThread):
    def __init__(self, parent=None, index_maker=None, maximum=0):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.index_maker = index_maker
        self.maximum = maximum

    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        extracted = 0
        log.debug("Reference extraction thread running") #@UndefinedVariable
        while extracted < self.maximum:
            extracted = len(self.index_maker.processed)
            self.emit(QtCore.SIGNAL("output(int)"), extracted)
            time.sleep(0.5)
        log.debug("Exiting extraction thread") #@UndefinedVariable
        self.exit(0)
        
        
class PathChoosePage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(PathChoosePage, self).__init__(parent)
        self.setTitle(title)
        self.setCommitPage(True)
        self.setButtonText(QtGui.QWizard.CommitButton, "Extract References")
        
        # Create Widgets
        self.label = QtGui.QLabel("Choose a directory:")
        self.file_chooser = FileChooser()
        
        self.registerField('filePath*', self.file_chooser)
        
        # Add Widgets to layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_chooser)
        self.setLayout(self.layout)
        

class ProgressPage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(ProgressPage, self).__init__(parent)
        self.setTitle(title)
        self.parent = parent
        
        self.label = QtGui.QLabel("Extracting references...")

        # Set progress bar
        self.max = 30
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setFormat('%v/%m')
        self.progressBar.setMaximum(self.max)
        self.progressBar.setProperty("value", 30)
        self.progressBar.setObjectName("progressBar")

        # Show logs
        self.logsLabel = QtGui.QLabel(self)
        self.logsLabel.setText('Status:')
        
        self.guihandler = GUIHandler()
        self.logs = LogsTextEdit(self)
        self.guihandler.messageLogged.connect(self.logs.updateText)

        # Register an empty label so next button is disabled
        self.empty_edit = QtGui.QLineEdit(self)
        self.empty_edit.setVisible(False)
        self.registerField('completed*', self.empty_edit)

        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.logsLabel)
        layout.addWidget(self.logs)
        self.setLayout(layout)
        
    def initializePage(self):
        log.addHandler(self.guihandler) #@UndefinedVariable

        path = self.field('filePath').toPyObject()
        self.parent.index_maker.set_path(str(path))
        
        self.logs.setText('')
        
        n_files = self.parent.index_maker.get_n_files()
        
        self.progressBar.setMaximum(n_files)
        self.progressBar.setValue(0)
        
        # This thread will update the GUI
        self.thread = ReferenceExtractionThread(self, self.parent.index_maker,
                                                n_files)

        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self.finish)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self.finish)
        self.connect(self.thread, QtCore.SIGNAL("output(int)"),
                     self.updateProgressBar)
        
        self.thread.start()
        
        # Start making the index
        self.parent.index_maker.make_index()
        
    def updateProgressBar(self, value=0):
        self.progressBar.setValue(value)

    def finish(self):
        log.info('Finished extracting. Results can be found in the Manage ' #@UndefinedVariable
                 'page') 
        # Stop the thread before jumping to next page
        self.thread.exiting = True        
        log.removeHandler(self.guihandler) #@UndefinedVariable
        self.empty_edit.setText('Done!')
        

class ReferenceExtractionWizard(QtGui.QWizard):
    
    def __init__(self):
        super(ReferenceExtractionWizard, self).__init__()
        self.initialize()
    
    def initialize(self):
        self.setDefaultProperty('FileChooser', 'path', QtCore.SIGNAL('pathChanged()'))
        self.setDefaultProperty('QProgressBar', 'value', QtCore.SIGNAL('valueChanged(int)'))
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnLastPage, True)

        self.wizard_title = 'Extract References'
        self.page01 = PathChoosePage(self.wizard_title, self)
        self.page02 = ProgressPage(self.wizard_title, self)
        self.addPage(self.page01)
        self.addPage(self.page02)
        self.index_maker = IndexMaker()
    
    def done(self, status):
        self.removePage(0)
        self.removePage(1)
        self.initialize()
        self.restart()
