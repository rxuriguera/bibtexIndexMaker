# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_reference_manager.ui'
#
# Created: Fri May 14 12:36:26 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ReferenceManagerPage(object):
    def setupUi(self, ReferenceManagerPage):
        ReferenceManagerPage.setObjectName("ReferenceManagerPage")
        ReferenceManagerPage.resize(640, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReferenceManagerPage.sizePolicy().hasHeightForWidth())
        ReferenceManagerPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ReferenceManagerPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(ReferenceManagerPage)
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
        self.references = QtGui.QTreeWidget(self.layoutWidget)
        self.references.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.references.setIndentation(0)
        self.references.setItemsExpandable(False)
        self.references.setObjectName("references")
        self.references.header().setVisible(True)
        self.verticalLayout.addWidget(self.references)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.referenceEditorLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.referenceEditorLayout.setSpacing(0)
        self.referenceEditorLayout.setObjectName("referenceEditorLayout")
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(ReferenceManagerPage)
        QtCore.QMetaObject.connectSlotsByName(ReferenceManagerPage)

    def retranslateUi(self, ReferenceManagerPage):
        ReferenceManagerPage.setWindowTitle(QtGui.QApplication.translate("ReferenceManagerPage", "Reference Manager", None, QtGui.QApplication.UnicodeUTF8))
        ReferenceManagerPage.setTitle(QtGui.QApplication.translate("ReferenceManagerPage", "Reference Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.references.headerItem().setText(0, QtGui.QApplication.translate("ReferenceManagerPage", "Available References", None, QtGui.QApplication.UnicodeUTF8))

