# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_wrapper_manager.ui'
#
# Created: Fri May 14 14:00:58 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_WrapperManagerPage(object):
    def setupUi(self, WrapperManagerPage):
        WrapperManagerPage.setObjectName("WrapperManagerPage")
        WrapperManagerPage.resize(590, 545)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WrapperManagerPage.sizePolicy().hasHeightForWidth())
        WrapperManagerPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(WrapperManagerPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(WrapperManagerPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(6)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.collectionsLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.collectionsLayout.setSpacing(6)
        self.collectionsLayout.setContentsMargins(-1, -1, 0, -1)
        self.collectionsLayout.setObjectName("collectionsLayout")
        self.collections = QtGui.QTreeWidget(self.layoutWidget)
        self.collections.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.collections.setObjectName("collections")
        self.collections.header().setVisible(True)
        self.collectionsLayout.addWidget(self.collections)
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.wrappersLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.wrappersLayout.setSpacing(6)
        self.wrappersLayout.setContentsMargins(-1, -1, 0, -1)
        self.wrappersLayout.setObjectName("wrappersLayout")
        self.wrappers = QtGui.QTreeWidget(self.verticalLayoutWidget)
        self.wrappers.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.wrappers.setIndentation(0)
        self.wrappers.setItemsExpandable(False)
        self.wrappers.setObjectName("wrappers")
        self.wrappersLayout.addWidget(self.wrappers)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.wrapperEditorLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.wrapperEditorLayout.setObjectName("wrapperEditorLayout")
        self.wrapperForm = QtGui.QFormLayout()
        self.wrapperForm.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.wrapperForm.setObjectName("wrapperForm")
        self.upvotesLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.upvotesLabel.setObjectName("upvotesLabel")
        self.wrapperForm.setWidget(0, QtGui.QFormLayout.LabelRole, self.upvotesLabel)
        self.upvotesSpin = QtGui.QSpinBox(self.verticalLayoutWidget_2)
        self.upvotesSpin.setObjectName("upvotesSpin")
        self.wrapperForm.setWidget(0, QtGui.QFormLayout.FieldRole, self.upvotesSpin)
        self.downvotesLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.downvotesLabel.setObjectName("downvotesLabel")
        self.wrapperForm.setWidget(1, QtGui.QFormLayout.LabelRole, self.downvotesLabel)
        self.downvotesSpin = QtGui.QSpinBox(self.verticalLayoutWidget_2)
        self.downvotesSpin.setObjectName("downvotesSpin")
        self.wrapperForm.setWidget(1, QtGui.QFormLayout.FieldRole, self.downvotesSpin)
        self.scoreLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.scoreLabel.setObjectName("scoreLabel")
        self.wrapperForm.setWidget(2, QtGui.QFormLayout.LabelRole, self.scoreLabel)
        self.scoreSpin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.scoreSpin.setReadOnly(True)
        self.scoreSpin.setObjectName("scoreSpin")
        self.wrapperForm.setWidget(2, QtGui.QFormLayout.FieldRole, self.scoreSpin)
        self.wrapperEditorLayout.addLayout(self.wrapperForm)
        self.line = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.wrapperEditorLayout.addWidget(self.line)
        self.rulesLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.rulesLabel.setObjectName("rulesLabel")
        self.wrapperEditorLayout.addWidget(self.rulesLabel)
        self.rules = QtGui.QTreeWidget(self.verticalLayoutWidget_2)
        self.rules.setIndentation(0)
        self.rules.setItemsExpandable(False)
        self.rules.setObjectName("rules")
        self.wrapperEditorLayout.addWidget(self.rules)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(WrapperManagerPage)
        QtCore.QMetaObject.connectSlotsByName(WrapperManagerPage)

    def retranslateUi(self, WrapperManagerPage):
        WrapperManagerPage.setWindowTitle(QtGui.QApplication.translate("WrapperManagerPage", "Reference Manager", None, QtGui.QApplication.UnicodeUTF8))
        WrapperManagerPage.setTitle(QtGui.QApplication.translate("WrapperManagerPage", "Wrapper Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.collections.headerItem().setText(0, QtGui.QApplication.translate("WrapperManagerPage", "Wrapper Collections", None, QtGui.QApplication.UnicodeUTF8))
        self.wrappers.headerItem().setText(0, QtGui.QApplication.translate("WrapperManagerPage", "Available Wrappers", None, QtGui.QApplication.UnicodeUTF8))
        self.upvotesLabel.setText(QtGui.QApplication.translate("WrapperManagerPage", "Upvotes", None, QtGui.QApplication.UnicodeUTF8))
        self.downvotesLabel.setText(QtGui.QApplication.translate("WrapperManagerPage", "Downvotes", None, QtGui.QApplication.UnicodeUTF8))
        self.scoreLabel.setText(QtGui.QApplication.translate("WrapperManagerPage", "Score", None, QtGui.QApplication.UnicodeUTF8))
        self.rulesLabel.setText(QtGui.QApplication.translate("WrapperManagerPage", "Rules", None, QtGui.QApplication.UnicodeUTF8))
        self.rules.headerItem().setText(0, QtGui.QApplication.translate("WrapperManagerPage", "Rule Type", None, QtGui.QApplication.UnicodeUTF8))
        self.rules.headerItem().setText(1, QtGui.QApplication.translate("WrapperManagerPage", "Pattern", None, QtGui.QApplication.UnicodeUTF8))
        self.rules.headerItem().setText(2, QtGui.QApplication.translate("WrapperManagerPage", "Order", None, QtGui.QApplication.UnicodeUTF8))

