# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_logo_conv.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(709, 240)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/file_xml-512.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(100.0)
        Form.setStyleSheet("background-color: rgb(0, 83, 113);")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(13, 213, 301, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(305, 213, 391, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(10, -10, 200, 200))
        self.label_1.setMinimumSize(QtCore.QSize(200, 200))
        self.label_1.setMaximumSize(QtCore.QSize(200, 200))
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap(":/logo/vniims_logo_2.jpg"))
        self.label_1.setScaledContents(True)
        self.label_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_1.setWordWrap(False)
        self.label_1.setIndent(1)
        self.label_1.setObjectName("label_1")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(13, 191, 461, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(0, 163, 709, 4))
        self.progressBar.setMinimumSize(QtCore.QSize(709, 4))
        self.progressBar.setMaximumSize(QtCore.QSize(709, 4))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    border: 0px solid rgb(8, 20, 53);\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(255, 255, 255)\n"
"}")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(250, 50, 391, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 180, 711, 16))
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_1.raise_()
        self.progressBar.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.line.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "LOGO"))
        self.label_4.setStyleSheet(_translate("Form", "color: rgb(255, 255, 255)"))
        self.label_4.setText(_translate("Form", "Программа распространяется бесплатно"))
        self.label_2.setText(_translate("Form", "Версия программы: 2.0"))
        self.label_3.setText(_translate("Form", "© Разработка и сопровождение ФГУП \"ВНИИМС\". 2021."))
        self.label_5.setText(_translate("Form", "Конвертер файлов из формата CSV в XML"))

import res_rc
