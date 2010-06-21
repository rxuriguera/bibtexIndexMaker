# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_file_chooser.ui'
#
# Created: Mon May  3 12:01:39 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FileChooser(object):
    def setupUi(self, FileChooser):
        FileChooser.setObjectName("FileChooser")
        FileChooser.resize(457, 183)
        self.horizontalLayout = QtGui.QHBoxLayout(FileChooser)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathLine = QtGui.QLineEdit(FileChooser)
        self.pathLine.setEnabled(True)
        self.pathLine.setObjectName("pathLine")
        self.horizontalLayout.addWidget(self.pathLine)
        self.browseButton = QtGui.QPushButton(FileChooser)
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout.addWidget(self.browseButton)

        self.retranslateUi(FileChooser)
        QtCore.QMetaObject.connectSlotsByName(FileChooser)

    def retranslateUi(self, FileChooser):
        FileChooser.setWindowTitle(QtGui.QApplication.translate("FileChooser", "File Chooser", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("FileChooser", "Browse...", None, QtGui.QApplication.UnicodeUTF8))

