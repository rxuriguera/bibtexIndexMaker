# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_new_collection_dialog.ui'
#
# Created: Fri May 14 14:24:38 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewWrapperCollection(object):
    def setupUi(self, NewWrapperCollection):
        NewWrapperCollection.setObjectName("NewWrapperCollection")
        NewWrapperCollection.resize(373, 148)
        self.verticalLayout = QtGui.QVBoxLayout(NewWrapperCollection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoLabel = QtGui.QLabel(NewWrapperCollection)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(NewWrapperCollection)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.urlLine = QtGui.QLineEdit(NewWrapperCollection)
        self.urlLine.setObjectName("urlLine")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.urlLine)
        self.label_2 = QtGui.QLabel(NewWrapperCollection)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.fieldLine = QtGui.QLineEdit(NewWrapperCollection)
        self.fieldLine.setObjectName("fieldLine")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.fieldLine)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(NewWrapperCollection)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewWrapperCollection)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewWrapperCollection.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewWrapperCollection.reject)
        QtCore.QMetaObject.connectSlotsByName(NewWrapperCollection)

    def retranslateUi(self, NewWrapperCollection):
        NewWrapperCollection.setWindowTitle(QtGui.QApplication.translate("NewWrapperCollection", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("NewWrapperCollection", "New Wrapper Collection:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewWrapperCollection", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewWrapperCollection", "Field", None, QtGui.QApplication.UnicodeUTF8))

