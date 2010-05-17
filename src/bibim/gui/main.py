import sys

from PyQt4 import QtCore, QtGui #@UnresolvedImport

from bibim import log
from bibim.gui.ui.ui_main_window import Ui_MainWindow
from bibim.gui.reference_extraction import ReferenceExtractionWizard
from bibim.gui.reference_manager import ReferenceManagerWizard
from bibim.gui.reference_importer import ReferenceImporterWizard
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

        self.last_selected = self.populate_menu()

        # Signal connection
        self.mw.menu.itemSelectionChanged.connect(self.change_content)
        self.mw.menu.setItemSelected(self.last_selected, True)

    def change_content(self):
        """
        Changes the widget in the content area
        """
        items = self.mw.menu.selectedItems()
        if not items:
            return
        selected = items[0]
        self.last_selected.widget_element.hide()
        self.last_selected = selected
        self.last_selected.widget_element.show()
    
    def populate_menu(self):
        item_0 = QtGui.QTreeWidgetItem(self.mw.menu)
        item_0.setFlags(QtCore.Qt.ItemIsEnabled)
        item_0.setText(0, QtGui.QApplication.translate("MainWindow",
            "References", None, QtGui.QApplication.UnicodeUTF8))
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Extract", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Extract References'
        item_1.widget_element = ReferenceExtractionWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)
        default = item_1
                
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
             "Manage", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Manage References'
        item_1.widget_element = ReferenceManagerWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)

        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
             "Import", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Import References'
        item_1.widget_element = ReferenceImporterWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
             "Export", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Export References'
        item_1.widget_element = ReferenceExporterWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)

        item_0 = QtGui.QTreeWidgetItem(self.mw.menu)
        item_0.setFlags(QtCore.Qt.ItemIsEnabled)
        item_0.setText(0, QtGui.QApplication.translate("MainWindow",
            "Wrappers", None, QtGui.QApplication.UnicodeUTF8))
    
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Train", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Train Wrappers'
        item_1.widget_element = WrapperTrainingWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)
        
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_1.setText(0, QtGui.QApplication.translate("MainWindow",
            "Manage", None, QtGui.QApplication.UnicodeUTF8))
        item_1.title = 'Manage Wrappers'
        item_1.widget_element = WrapperManagerWizard()
        item_1.widget_element.hide()
        self.mw.contentLayout.addWidget(item_1.widget_element)
        
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


