# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created: Fri May 14 12:51:05 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(769, 529)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.menuLayout = QtGui.QHBoxLayout(self.verticalLayoutWidget)
        self.menuLayout.setSpacing(0)
        self.menuLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.menuLayout.setMargin(0)
        self.menuLayout.setObjectName("menuLayout")
        self.menu = QtGui.QTreeWidget(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMinimumSize(QtCore.QSize(150, 0))
        self.menu.setMaximumSize(QtCore.QSize(150, 16777215))
        self.menu.setFrameShape(QtGui.QFrame.Box)
        self.menu.setFrameShadow(QtGui.QFrame.Plain)
        self.menu.setLineWidth(0)
        self.menu.setAnimated(True)
        self.menu.setHeaderHidden(True)
        self.menu.setObjectName("menu")
        self.menu.header().setVisible(False)
        self.menu.header().setDefaultSectionSize(27)
        self.menuLayout.addWidget(self.menu)
        self.vline = QtGui.QFrame(self.verticalLayoutWidget)
        self.vline.setFrameShape(QtGui.QFrame.VLine)
        self.vline.setFrameShadow(QtGui.QFrame.Sunken)
        self.vline.setObjectName("vline")
        self.menuLayout.addWidget(self.vline)
        self.horizontalLayoutWidget = QtGui.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.contentLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setObjectName("contentLayout")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bibtex Index Maker", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))

