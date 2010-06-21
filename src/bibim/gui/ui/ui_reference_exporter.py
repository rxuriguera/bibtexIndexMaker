# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_reference_exporter.ui'
#
# Created: Fri May 14 16:20:28 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ReferenceExporterPage(object):
    def setupUi(self, ReferenceExporterPage):
        ReferenceExporterPage.setObjectName("ReferenceExporterPage")
        ReferenceExporterPage.resize(640, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReferenceExporterPage.sizePolicy().hasHeightForWidth())
        ReferenceExporterPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ReferenceExporterPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(ReferenceExporterPage)
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
        self.referenceListLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.referenceListLayout.setSpacing(0)
        self.referenceListLayout.setObjectName("referenceListLayout")
        self.references = QtGui.QTreeWidget(self.layoutWidget)
        self.references.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.references.setIndentation(0)
        self.references.setItemsExpandable(False)
        self.references.setObjectName("references")
        self.references.header().setVisible(True)
        self.referenceListLayout.addWidget(self.references)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.exportLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.exportLayout.setSpacing(6)
        self.exportLayout.setObjectName("exportLayout")
        self.entriesEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.entriesEdit.setObjectName("entriesEdit")
        self.exportLayout.addWidget(self.entriesEdit)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(ReferenceExporterPage)
        QtCore.QMetaObject.connectSlotsByName(ReferenceExporterPage)

    def retranslateUi(self, ReferenceExporterPage):
        ReferenceExporterPage.setWindowTitle(QtGui.QApplication.translate("ReferenceExporterPage", "Export References", None, QtGui.QApplication.UnicodeUTF8))
        ReferenceExporterPage.setTitle(QtGui.QApplication.translate("ReferenceExporterPage", "Export References", None, QtGui.QApplication.UnicodeUTF8))
        self.references.headerItem().setText(0, QtGui.QApplication.translate("ReferenceExporterPage", "Available References", None, QtGui.QApplication.UnicodeUTF8))

