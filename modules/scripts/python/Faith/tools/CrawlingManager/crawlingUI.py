# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crawlingUI.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 184)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_btn = QtWidgets.QPushButton(Form)
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout.addWidget(self.load_btn)
        self.load_le = QtWidgets.QLineEdit(Form)
        self.load_le.setReadOnly(True)
        self.load_le.setObjectName("load_le")
        self.horizontalLayout.addWidget(self.load_le)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ctrl_btn = QtWidgets.QPushButton(Form)
        self.ctrl_btn.setObjectName("ctrl_btn")
        self.horizontalLayout_4.addWidget(self.ctrl_btn)
        self.ctrl_le = QtWidgets.QLineEdit(Form)
        self.ctrl_le.setObjectName("ctrl_le")
        self.horizontalLayout_4.addWidget(self.ctrl_le)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.count_spin = QtWidgets.QSpinBox(Form)
        self.count_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.count_spin.setMinimum(5)
        self.count_spin.setMaximum(9999)
        self.count_spin.setObjectName("count_spin")
        self.horizontalLayout_2.addWidget(self.count_spin)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.ctrlSize_dp = QtWidgets.QDoubleSpinBox(Form)
        self.ctrlSize_dp.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ctrlSize_dp.setMinimum(1.0)
        self.ctrlSize_dp.setMaximum(999.99)
        self.ctrlSize_dp.setSingleStep(0.01)
        self.ctrlSize_dp.setObjectName("ctrlSize_dp")
        self.horizontalLayout_2.addWidget(self.ctrlSize_dp)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.name_le = QtWidgets.QLineEdit(Form)
        self.name_le.setObjectName("name_le")
        self.horizontalLayout_3.addWidget(self.name_le)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.create_btn = QtWidgets.QPushButton(Form)
        self.create_btn.setObjectName("create_btn")
        self.verticalLayout.addWidget(self.create_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Crwling Tool"))
        self.load_btn.setText(_translate("Form", "Load Curves"))
        self.ctrl_btn.setText(_translate("Form", "Add Ctrl"))
        self.label.setText(_translate("Form", "count"))
        self.label_3.setText(_translate("Form", "ctrl size"))
        self.label_2.setText(_translate("Form", "Prefix Name"))
        self.create_btn.setText(_translate("Form", "Create"))


