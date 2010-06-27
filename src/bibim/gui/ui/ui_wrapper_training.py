# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_wrapper_training.ui'
#
# Created: Sun Jun 27 13:50:22 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_WrapperTrainingPage(object):
    def setupUi(self, WrapperTrainingPage):
        WrapperTrainingPage.setObjectName("WrapperTrainingPage")
        WrapperTrainingPage.resize(640, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WrapperTrainingPage.sizePolicy().hasHeightForWidth())
        WrapperTrainingPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(WrapperTrainingPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(WrapperTrainingPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.wrapperTrainingLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.wrapperTrainingLayout.setSpacing(6)
        self.wrapperTrainingLayout.setObjectName("wrapperTrainingLayout")
        self.urlLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.urlLabel.setObjectName("urlLabel")
        self.wrapperTrainingLayout.addWidget(self.urlLabel)
        self.urlLine = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.urlLine.setObjectName("urlLine")
        self.wrapperTrainingLayout.addWidget(self.urlLine)
        self.instructionsLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.instructionsLabel.setObjectName("instructionsLabel")
        self.wrapperTrainingLayout.addWidget(self.instructionsLabel)
        self.urls = QtGui.QTreeWidget(self.verticalLayoutWidget)
        self.urls.setIndentation(0)
        self.urls.setItemsExpandable(False)
        self.urls.setObjectName("urls")
        self.urls.header().setVisible(True)
        self.wrapperTrainingLayout.addWidget(self.urls)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(WrapperTrainingPage)
        QtCore.QMetaObject.connectSlotsByName(WrapperTrainingPage)

    def retranslateUi(self, WrapperTrainingPage):
        WrapperTrainingPage.setWindowTitle(QtGui.QApplication.translate("WrapperTrainingPage", "Reference Manager", None, QtGui.QApplication.UnicodeUTF8))
        WrapperTrainingPage.setTitle(QtGui.QApplication.translate("WrapperTrainingPage", "Wrapper Training", None, QtGui.QApplication.UnicodeUTF8))
        self.urlLabel.setText(QtGui.QApplication.translate("WrapperTrainingPage", "Write a URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.instructionsLabel.setText(QtGui.QApplication.translate("WrapperTrainingPage", "Or select one below:", None, QtGui.QApplication.UnicodeUTF8))
        self.urls.headerItem().setText(0, QtGui.QApplication.translate("WrapperTrainingPage", "Available URLs", None, QtGui.QApplication.UnicodeUTF8))

