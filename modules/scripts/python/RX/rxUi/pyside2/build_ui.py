# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\buildUI.ui'
#
# Created: Thu Apr 17 13:02:49 2025
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_buildUI(object):
    def setupUi(self, buildUI):
        buildUI.setObjectName("buildUI")
        buildUI.resize(379, 572)
        buildUI.setAcceptDrops(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(buildUI)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rigTypeBtn = QtWidgets.QPushButton(buildUI)
        self.rigTypeBtn.setStyleSheet("QPushButton{ \n"
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
        self.rigTypeBtn.setText("")
        self.rigTypeBtn.setObjectName("rigTypeBtn")
        self.verticalLayout.addWidget(self.rigTypeBtn)
        self.buildList = QtWidgets.QListWidget(buildUI)
        self.buildList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.buildList.setStyleSheet("QScrollBar{\n"
"                    border: 1px solid grey;\n"
"                    background:rgb(55,55,55);\n"
"                    width: 8px;}")
        self.buildList.setObjectName("buildList")
        self.verticalLayout.addWidget(self.buildList)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.nextBtn = QtWidgets.QPushButton(buildUI)
        self.nextBtn.setMinimumSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nextBtn.setFont(font)
        self.nextBtn.setStyleSheet("QPushButton{ \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #116776, stop:0 #116776);\n"
"padding: 5px;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"background-color: #1d8ba3;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: #1d1d1d;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: #4b4b4b;\n"
"border-radius: 5px;\n"
"}")
        self.nextBtn.setObjectName("nextBtn")
        self.gridLayout_3.addWidget(self.nextBtn, 0, 0, 1, 1)
        self.selBtn = QtWidgets.QPushButton(buildUI)
        self.selBtn.setMinimumSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selBtn.setFont(font)
        self.selBtn.setStyleSheet("QPushButton{ \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #116776, stop:0 #116776);\n"
"padding: 5px;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"background-color: #1d8ba3;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: #1d1d1d;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: #4b4b4b;\n"
"border-radius: 5px;\n"
"}")
        self.selBtn.setObjectName("selBtn")
        self.gridLayout_3.addWidget(self.selBtn, 0, 1, 1, 1)
        self.buildBtn = QtWidgets.QPushButton(buildUI)
        self.buildBtn.setMinimumSize(QtCore.QSize(0, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buildBtn.setFont(font)
        self.buildBtn.setStyleSheet("QPushButton{ \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #116776, stop:0 #116776);\n"
"padding: 5px;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"background-color: #1d8ba3;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"background-color: #1d1d1d;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"background-color: #4b4b4b;\n"
"border-radius: 5px;\n"
"}")
        self.buildBtn.setObjectName("buildBtn")
        self.gridLayout_3.addWidget(self.buildBtn, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.groupBox = QtWidgets.QGroupBox(buildUI)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 1))
        self.groupBox.setTitle("")
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loadBtn_2 = QtWidgets.QPushButton(buildUI)
        self.loadBtn_2.setObjectName("loadBtn_2")
        self.horizontalLayout_3.addWidget(self.loadBtn_2)
        self.saveBtn_2 = QtWidgets.QPushButton(buildUI)
        self.saveBtn_2.setObjectName("saveBtn_2")
        self.horizontalLayout_3.addWidget(self.saveBtn_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(buildUI)
        QtCore.QMetaObject.connectSlotsByName(buildUI)

    def retranslateUi(self, buildUI):
        buildUI.setWindowTitle(QtWidgets.QApplication.translate("buildUI", "Rig Build", None, -1))
        self.nextBtn.setToolTip(QtWidgets.QApplication.translate("buildUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.nextBtn.setText(QtWidgets.QApplication.translate("buildUI", "Build Next", None, -1))
        self.selBtn.setToolTip(QtWidgets.QApplication.translate("buildUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.selBtn.setText(QtWidgets.QApplication.translate("buildUI", "To Selected", None, -1))
        self.buildBtn.setToolTip(QtWidgets.QApplication.translate("buildUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the entire rig.</p></body></html>", None, -1))
        self.buildBtn.setText(QtWidgets.QApplication.translate("buildUI", "Build All", None, -1))
        self.loadBtn_2.setToolTip(QtWidgets.QApplication.translate("buildUI", "Load existing rig scene.", None, -1))
        self.loadBtn_2.setText(QtWidgets.QApplication.translate("buildUI", "Load Work Scene", None, -1))
        self.saveBtn_2.setToolTip(QtWidgets.QApplication.translate("buildUI", "Save current rig scene.", None, -1))
        self.saveBtn_2.setText(QtWidgets.QApplication.translate("buildUI", "Save Work Scene", None, -1))

