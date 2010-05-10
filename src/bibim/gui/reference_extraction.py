
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
            
        
class PathChoosePage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(PathChoosePage, self).__init__(parent)
        self.setTitle(title)
        self.setCommitPage(True)
        self.setButtonText(QtGui.QWizard.CommitButton, "Extract References")
        
        # Create Widgets
        label = QtGui.QLabel("Choose a directory:")
        file_chooser = FileChooser()
        
        self.registerField('filePath*', file_chooser)
        
        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(file_chooser)
        self.setLayout(layout)


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
        self.parent.index_maker.set_path(str(path))
        
        n_files = self.parent.index_maker.get_n_files()
        
        self.progressBar.setMaximum(n_files)
        self.progressBar.setValue(0)
        
        # This thread will update the GUI
        self.thread = ReferenceExtractionThread(self, self.parent.index_maker,
                                                n_files)
        
        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self.next)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self.next)
        self.connect(self.thread, QtCore.SIGNAL("output(int)"),
                     self.updateProgressBar)
        
        self.thread.start()
        
        # Start making the index
        self.parent.index_maker.make_index()
        
    def updateProgressBar(self, value=0):
        log.debug("Updating progress bar. New value: %d" % value) #@UndefinedVariable
        self.progressBar.setValue(value)

    def next(self):
        log.debug("Stopping thread and jumping to next page") #@UndefinedVariable
        # Stop the thread before jumping to next page
        self.thread.exiting = True
        self.parent.next()


class FinishedPage(QtGui.QWizardPage):
    def __init__(self, title, parent=None):
        super(FinishedPage, self).__init__(parent)
        self.setTitle(title)
        self.parent = parent
        
        self.label01 = QtGui.QLabel("Extraction finished")
        self.label02 = QtGui.QLabel("You can see the extracted references in the 'Manage' page")

        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label01)
        layout.addWidget(self.label02)
        self.setLayout(layout)
        
        
class ReferenceExtractionWizard(QtGui.QWizard):
    
    def __init__(self):
        super(ReferenceExtractionWizard, self).__init__()
        self.setDefaultProperty('FileChooser', 'path', QtCore.SIGNAL('pathChanged()'))
        self.setDefaultProperty('QProgressBar', 'value', QtCore.SIGNAL('valueChanged(int)'))
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        
        #self.setOption(QtGui.QWizard.HaveHelpButton, True)
        self.wizard_title = 'Extract References'
        self.page01 = PathChoosePage(self.wizard_title, self)
        self.page02 = ProgressPage(self.wizard_title, self)
        self.page03 = FinishedPage(self.wizard_title, self) 
        self.addPage(self.page01)
        self.addPage(self.page02)
        self.addPage(self.page03)
        self.index_maker = IndexMaker()
        

