# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_user_login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class User_login_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(395, 258)
        Dialog.setStyleSheet("QDialog{\n"
"    background-color:#E0B9E7;\n"
" background-position: center;\n"
"  background-size: cover;\n"
"}\n"
"")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 160, 151, 31))
        self.pushButton.setStyleSheet("QPushButton{\n"
"border-radius: 50px;\n"
"background:#c68ad1;\n"
"opacity: 0.6;\n"
"}\n"
"QPushButton:hover {background-color: #a56baf; }")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(208, 160, 131, 31))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"border-radius: 50px;\n"
"background:#c68ad1;\n"
"opacity: 0.6;\n"
"}\n"
"QPushButton:hover {background-color: #a56baf; }")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 291, 41))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Create"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "There is no user with this name."))
        self.label_2.setText(_translate("Dialog", "You can add a new user or try again."))

