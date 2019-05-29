# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Login_error_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 261)
        Dialog.setStyleSheet("QDialog{\n"
"    background-color:#E0B9E7;\n"
" background-position: center;\n"
"  background-size: cover;\n"
"}\n"
"")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 120, 181, 31))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"border-radius: 50px;\n"
"background:#c68ad1;\n"
"opacity: 0.6;\n"
"}\n"
"QPushButton:hover {background-color: #a56baf; }")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 10, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 80, 181, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "Try again."))
        self.label.setText(_translate("Dialog", "Error!"))
        self.label_2.setText(_translate("Dialog", "Wrong password."))

