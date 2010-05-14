
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
from bibim.gui.custom_widgets import FileChooser
from bibim.main.entry import ReferenceImporter


class ReferenceImporterThread(QtCore.QThread):
    def __init__(self, path, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.path = path
        self.reference_importer = ReferenceImporter()
        self.imported = 0
         
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        self.imported = self.reference_importer.import_references(self.path)
        
        
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

        # Register an empty label so next button is disabled
        self.empty_label = QtGui.QLabel("")
        self.registerField('completed*', self.empty_label)
        
        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

    def initializePage(self):
        path = self.field('filePath').toPyObject()
        log.debug("Starting importing references from: %s" % path) #@UndefinedVariable
        
        self.thread = ReferenceImporterThread(str(path), self)
        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self.next)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self.next)
        self.thread.start()

    def next(self):
        log.debug("Stopping thread and jumping to next page") #@UndefinedVariable
        self.parent.next()
        

class FinishedPage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(FinishedPage, self).__init__(parent)
        self.setTitle(title)
        self.parent = parent
        
        self.label01 = QtGui.QLabel("Import finished")
        self.label02 = QtGui.QLabel("You can see the imported references in the 'Manage' page")

        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label01)
        layout.addWidget(self.label02)
        self.setLayout(layout)

        
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
        self.page03 = FinishedPage(self.wizard_title, self) 
        self.addPage(self.page01)
        self.addPage(self.page02)
        self.addPage(self.page03)
        self.reference_importer = ReferenceImporter()
    
    def done(self, status):
        self.removePage(0)
        self.removePage(1)
        self.removePage(2)
        self.initialize()
        self.restart()
