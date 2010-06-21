# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ref_extraction_results.ui'
#
# Created: Tue May  4 01:04:01 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RefExtractionResultsPage(object):
    def setupUi(self, RefExtractionResultsPage):
        RefExtractionResultsPage.setObjectName("RefExtractionResultsPage")
        RefExtractionResultsPage.resize(640, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RefExtractionResultsPage.sizePolicy().hasHeightForWidth())
        RefExtractionResultsPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(RefExtractionResultsPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(RefExtractionResultsPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.files = QtGui.QTreeWidget(self.layoutWidget)
        self.files.setIndentation(0)
        self.files.setItemsExpandable(False)
        self.files.setObjectName("files")
        self.files.header().setVisible(True)
        self.verticalLayout.addWidget(self.files)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.referenceEditorLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.referenceEditorLayout.setSpacing(0)
        self.referenceEditorLayout.setObjectName("referenceEditorLayout")
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(RefExtractionResultsPage)
        QtCore.QMetaObject.connectSlotsByName(RefExtractionResultsPage)

    def retranslateUi(self, RefExtractionResultsPage):
        RefExtractionResultsPage.setWindowTitle(QtGui.QApplication.translate("RefExtractionResultsPage", "Extraction Results", None, QtGui.QApplication.UnicodeUTF8))
        RefExtractionResultsPage.setTitle(QtGui.QApplication.translate("RefExtractionResultsPage", "Extract References", None, QtGui.QApplication.UnicodeUTF8))
        self.files.headerItem().setText(0, QtGui.QApplication.translate("RefExtractionResultsPage", "Files", None, QtGui.QApplication.UnicodeUTF8))

