
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
from bibim.main.entry import ReferenceImporter


class ReferenceImporterThread(QtCore.QThread):
    def __init__(self, path, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.reference_importer = ReferenceImporter()
        self.reference_importer.set_path(path)
        self.imported = 0
         
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        self.reference_importer.start()
        self.reference_importer.join()
        
        
class PathChoosePage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(PathChoosePage, self).__init__(parent)
        self.setTitle(title)
        self.setCommitPage(True)
        self.setButtonText(QtGui.QWizard.CommitButton, "Import References")
        
        # Create Widgets
        self.label = QtGui.QLabel("Choose a file:")
        self.file_chooser = FileChooser()
        self.file_chooser.mode = FileChooser.FILE
        
        self.registerField('filePath*', self.file_chooser)
        
        # Add Widgets to layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_chooser)
        self.setLayout(self.layout)
        

class ProgressPage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(ProgressPage, self).__init__(parent)
        self.parent = parent
        self.setTitle(title)
        
        self.label = QtGui.QLabel("Importing references...")

        # Set progress bar
        self.max = 0
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setMaximum(self.max)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setTextVisible(False)

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
        log.debug("Starting importing references from: %s" % path) #@UndefinedVariable
        
        self.thread = ReferenceImporterThread(str(path), self)
        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self.finish)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self.finish)
        self.thread.start()
    
    def finish(self):
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(1)
        log.info('Finished importing. Results can be found in the Manage page') #@UndefinedVariable
        log.removeHandler(self.guihandler) #@UndefinedVariable
        self.empty_edit.setText('Done!')

        
class ReferenceImporterWizard(QtGui.QWizard):
    
    def __init__(self):
        super(ReferenceImporterWizard, self).__init__()
        self.initialize()
        #self.setOption(QtGui.QWizard.HaveHelpButton, True)
    
    def initialize(self):
        self.setDefaultProperty('FileChooser', 'path', QtCore.SIGNAL('pathChanged()'))
        self.setDefaultProperty('QProgressBar', 'value', QtCore.SIGNAL('valueChanged(int)'))
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnLastPage, True)

        self.wizard_title = 'Import References'
        self.page01 = PathChoosePage(self.wizard_title, self)
        self.page02 = ProgressPage(self.wizard_title, self)
        self.addPage(self.page01)
        self.addPage(self.page02)
        self.reference_importer = ReferenceImporter()
    
    def done(self, status):
        self.removePage(0)
        self.removePage(1)
        self.initialize()
        self.restart()
