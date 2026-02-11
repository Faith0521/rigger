# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\checkUI.ui'
#
# Created: Tue Jul 20 16:53:46 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CheckUI(object):
    def setupUi(self, CheckUI):
        CheckUI.setObjectName("CheckUI")
        CheckUI.resize(525, 1060)
        self.gridLayout = QtWidgets.QGridLayout(CheckUI)
        self.gridLayout.setObjectName("gridLayout")
        self.checkTree = QtWidgets.QTreeWidget(CheckUI)
        self.checkTree.setUniformRowHeights(True)
        self.checkTree.setAllColumnsShowFocus(True)
        self.checkTree.setHeaderHidden(True)
        self.checkTree.setColumnCount(3)
        self.checkTree.setObjectName("checkTree")
        self.checkTree.headerItem().setText(0, "1")
        self.checkTree.headerItem().setText(1, "2")
        self.checkTree.headerItem().setText(2, "3")
        self.checkTree.header().setDefaultSectionSize(60)
        self.checkTree.header().setMinimumSectionSize(60)
        self.checkTree.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.checkTree, 1, 0, 1, 2)
        self.ExportBtn = QtWidgets.QPushButton(CheckUI)
        self.ExportBtn.setMinimumSize(QtCore.QSize(0, 35))
        self.ExportBtn.setStyleSheet("QPushButton{ \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #0072bc, stop:0 #0054a6);\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: #1d1d1d;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: #4b4b4b;\n"
"border-radius: 0px;\n"
"}")
        self.ExportBtn.setObjectName("ExportBtn")
        self.gridLayout.addWidget(self.ExportBtn, 3, 0, 1, 2)
        self.fixBtn = QtWidgets.QPushButton(CheckUI)
        self.fixBtn.setMinimumSize(QtCore.QSize(0, 35))
        self.fixBtn.setObjectName("fixBtn")
        self.gridLayout.addWidget(self.fixBtn, 2, 1, 1, 1)
        self.checkBtn = QtWidgets.QPushButton(CheckUI)
        self.checkBtn.setMinimumSize(QtCore.QSize(0, 35))
        self.checkBtn.setObjectName("checkBtn")
        self.gridLayout.addWidget(self.checkBtn, 2, 0, 1, 1)
        self.lodBtn = QtWidgets.QPushButton(CheckUI)
        self.lodBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.lodBtn.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.lodBtn.setObjectName("lodBtn")
        self.gridLayout.addWidget(self.lodBtn, 0, 0, 1, 2)

        self.retranslateUi(CheckUI)
        QtCore.QMetaObject.connectSlotsByName(CheckUI)

    def retranslateUi(self, CheckUI):
        CheckUI.setWindowTitle(QtWidgets.QApplication.translate("CheckUI", "Checker", None, -1))
        self.ExportBtn.setText(QtWidgets.QApplication.translate("CheckUI", "Export Rig", None, -1))
        self.fixBtn.setText(QtWidgets.QApplication.translate("CheckUI", "Run Auto Fix", None, -1))
        self.checkBtn.setText(QtWidgets.QApplication.translate("CheckUI", "Run Checks", None, -1))
        self.lodBtn.setText(QtWidgets.QApplication.translate("CheckUI", "Rig Type", None, -1))

