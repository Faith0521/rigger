# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assetCheckUI.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_assetCheckUI(object):
    def setupUi(self, assetCheckUI):
        assetCheckUI.setObjectName("assetCheckUI")
        assetCheckUI.resize(486, 428)
        self.gridLayout = QtWidgets.QGridLayout(assetCheckUI)
        self.gridLayout.setObjectName("gridLayout")
        self.checkTree = QtWidgets.QTreeWidget(assetCheckUI)
        self.checkTree.setEnabled(True)
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
        self.checkTypeBtn = QtWidgets.QPushButton(assetCheckUI)
        self.checkTypeBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.checkTypeBtn.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.checkTypeBtn.setStyleSheet("QPushButton{ \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #116776, stop:0 #116776);\n"
"padding: 5px;\n"
"border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"background-color: #1d8ba3;\n"
"border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: #1d1d1d;\n"
"border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: #4b4b4b;\n"
"border-radius: 2px;\n"
"}")
        self.checkTypeBtn.setObjectName("checkTypeBtn")
        self.gridLayout.addWidget(self.checkTypeBtn, 0, 0, 1, 2)
        self.fixBtn = QtWidgets.QPushButton(assetCheckUI)
        self.fixBtn.setMinimumSize(QtCore.QSize(0, 35))
        self.fixBtn.setObjectName("fixBtn")
        self.gridLayout.addWidget(self.fixBtn, 2, 1, 1, 1)
        self.checkBtn = QtWidgets.QPushButton(assetCheckUI)
        self.checkBtn.setMinimumSize(QtCore.QSize(0, 35))
        self.checkBtn.setObjectName("checkBtn")
        self.gridLayout.addWidget(self.checkBtn, 2, 0, 1, 1)

        self.retranslateUi(assetCheckUI)
        QtCore.QMetaObject.connectSlotsByName(assetCheckUI)

    def retranslateUi(self, assetCheckUI):
        _translate = QtCore.QCoreApplication.translate
        assetCheckUI.setWindowTitle(_translate("assetCheckUI", "Asset Checker V1.0"))
        self.checkTypeBtn.setText(_translate("assetCheckUI", "Elo_film_rig"))
        self.fixBtn.setText(_translate("assetCheckUI", "Run Auto Fix"))
        self.checkBtn.setText(_translate("assetCheckUI", "Run Checks"))


