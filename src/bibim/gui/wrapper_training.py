
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
from bibim.db.gateways import WrapperGateway
from bibim.gui.custom_widgets import LogsTextEdit
from bibim.gui.outlog import GUIHandler
from bibim.gui.ui.ui_wrapper_training import Ui_WrapperTrainingPage
from bibim.main.entry import WrapperGenerator



class WrapperTrainingThread(QtCore.QThread):
    def __init__(self, parent=None, url=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.url = url
        self.wrapper_generator = WrapperGenerator(url)
         
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        self.wrapper_generator.start()
        self.wrapper_generator.join()


class URLChoosePage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(URLChoosePage, self).__init__(parent)
        self.parent = parent
        self.last_selected = None
        
        self.ui = Ui_WrapperTrainingPage()
        self.ui.setupUi(self)

        self.setCommitPage(True)
        self.setButtonText(QtGui.QWizard.CommitButton, "Train")
        
        self.registerField('url*', self.ui.urlLine)
        
        self.ui.urls.itemSelectionChanged.connect(self.update_url_line)
    
    def initializePage(self):
        urls_list = []
        
        # Populate available URLs
        for collection in self.parent.wrapper_gw.find_wrapper_collections():
            if collection.url in urls_list:
                continue
            item = QtGui.QTreeWidgetItem(self.ui.urls)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setText(0, QtGui.QApplication.translate("", collection.url,
                None, QtGui.QApplication.UnicodeUTF8))
            urls_list.append(collection.url)
    
    def update_url_line(self):
        items = self.ui.urls.selectedItems()
        if not items:
            return
        selected = items[0]
        self.ui.urlLine.setText(selected.text(0))


class ProgressPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ProgressPage, self).__init__(parent)
        self.parent = parent
        
        self.label = QtGui.QLabel("Training wrappers...")

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
        
        self.guihandler = GUIHandler(omit_levels=['WARNING'])
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
                
        url = self.field('url').toPyObject()
        log.info("Starting training for URL: %s" % url) #@UndefinedVariable
        
        self.thread = WrapperTrainingThread(self, url)
        # Connect thread signals
        self.connect(self.thread, QtCore.SIGNAL("finished()"),
                     self.finish)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"),
                     self.finish)
        self.thread.start()

    def finish(self):
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(1)
        log.info('Finished training. Results can be found in the Manage page') #@UndefinedVariable
        log.removeHandler(self.guihandler) #@UndefinedVariable
        self.empty_edit.setText('Done!')

        
        
class FinishedPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(FinishedPage, self).__init__(parent)
        self.parent = parent
        
        self.label01 = QtGui.QLabel("Finished training wrappers")
        self.label02 = QtGui.QLabel("You can see the extracted trainers in the 'Manage' page")

        # Add Widgets to layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label01)
        layout.addWidget(self.label02)
        self.setLayout(layout)
        
     
class WrapperTrainingWizard(QtGui.QWizard):
    
    def __init__(self):
        super(WrapperTrainingWizard, self).__init__()
        self.initialize()

    def initialize(self):
        self.setDefaultProperty('FileChooser', 'path', QtCore.SIGNAL('pathChanged()'))
        self.setDefaultProperty('QProgressBar', 'value', QtCore.SIGNAL('valueChanged(int)'))
        
        self.setOption(QtGui.QWizard.NoCancelButton, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QtGui.QWizard.NoBackButtonOnLastPage, True)
        
        self.wrapper_gw = WrapperGateway()
        
        self.page01 = URLChoosePage(self)
        self.page02 = ProgressPage(self)
        #self.page03 = FinishedPage(self) 
        self.addPage(self.page01)
        self.addPage(self.page02)
        #self.addPage(self.page03)
        
    def done(self, status):
        self.removePage(0)
        self.removePage(1)
        #self.removePage(2)
        self.initialize()
        self.restart()        
