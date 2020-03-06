# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(1114, 695)
        self.widget = QtWidgets.QWidget(main)
        self.widget.setGeometry(QtCore.QRect(140, 240, 241, 381))
        self.widget.setObjectName("widget")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 30, 93, 131))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 190, 93, 141))
        self.pushButton_2.setObjectName("pushButton_2")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(10, 370, 91, 19))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Form"))
        self.pushButton.setText(_translate("main", "PushButton"))
        self.pushButton_2.setText(_translate("main", "PushButton"))
        self.checkBox.setText(_translate("main", "CheckBox"))
