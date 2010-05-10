import sys

from PyQt4 import QtCore, QtGui #@UnresolvedImport

from bibim import log
from bibim.gui.ui.ui_main_window import Ui_MainWindow
from bibim.gui.reference_extraction import ReferenceExtractionWizard
from bibim.gui.reference_manager import ReferenceManagerWizard
from bibim.gui.reference_exporter import ReferenceExporterWizard
from bibim.gui.wrapper_manager import WrapperManagerWizard
from bibim.gui.wrapper_training import WrapperTrainingWizard


# Menu actions
menu_actions = {'ref:extract':ReferenceExtractionWizard,
                'ref:manage':ReferenceManagerWizard,
                'ref:export':ReferenceExporterWizard,
                'wrap:train':WrapperTrainingWizard,
                'wrap:manage':WrapperManagerWizard}


class BibimMain(QtGui.QMainWindow):
    
    def __init__(self):
        super(BibimMain, self).__init__()

        # This is always the same
        self.mw = Ui_MainWindow()
        self.mw.setupUi(self)
        self.default_selected = self.populate_menu()

        # Signal connection
        self.mw.menu.itemSelectionChanged.connect(self.change_content)
        self.mw.menu.setItemSelected(self.default_selected, True)

    def change_content(self):
        """
        Changes the widget in the content area
        """
        items = self.mw.menu.selectedItems()
        if not items:
            return
        
        selected = items[0]
        try:
            content_widget = menu_actions[selected.action_command]
        except KeyError:
            return
        #print self.mw.contentLayout.count()
        if self.mw.contentLayout.count() > 0:
            try:
                self.mw.contentLayout.takeAt(0).widget().done(0)
            except:
                log.warn('Widget has no done method') #@UndefinedVariable

        self.mw.contentLayout.addWidget(content_widget())
    
    def populate_menu(self):
        item_0 = QtGui.QTreeWidgetItem(self.mw.menu)
        item_0.setFlags(QtCore.Qt.ItemIsEnabled)
        item_0.setText(0, QtGui.QApplication.translate("MainWindow",
            "References", None, QtGui.QApplication.UnicodeUTF8))
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Extract", None, QtGui.QApplication.UnicodeUTF8))
        item_1.action_command = 'ref:extract'
        default = item_1
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
             "Manage", None, QtGui.QApplication.UnicodeUTF8))
        item_1.action_command = 'ref:manage'
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
             "Export", None, QtGui.QApplication.UnicodeUTF8))
        item_1.action_command = 'ref:export'        
        
        item_0 = QtGui.QTreeWidgetItem(self.mw.menu)
        item_0.setFlags(QtCore.Qt.ItemIsEnabled)
        item_0.setText(0, QtGui.QApplication.translate("MainWindow",
            "Wrappers", None, QtGui.QApplication.UnicodeUTF8))
    
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Train", None, QtGui.QApplication.UnicodeUTF8))
        item_1.action_command = 'wrap:train'
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Manage", None, QtGui.QApplication.UnicodeUTF8))
        item_1.action_command = 'wrap:manage'
        
        self.mw.menu.expandAll()

        return default
        
def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window = BibimMain()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


