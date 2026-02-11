# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\templateUI.ui'
#
# Created: Thu Apr 17 13:04:43 2025
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TemplateUI(object):
    def setupUi(self, TemplateUI):
        TemplateUI.setObjectName("TemplateUI")
        TemplateUI.resize(665, 890)
        self.gridLayout = QtWidgets.QGridLayout(TemplateUI)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(TemplateUI)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addBtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.addBtn.setStyleSheet("QPushButton{ \n"
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
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout.addWidget(self.addBtn)
        self.partsList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.partsList.setStyleSheet("QScrollBar{\n"
"                    border: 1px solid grey;\n"
"                    background:rgb(55,55,55);\n"
"                    width: 8px;}")
        self.partsList.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.partsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.partsList.setObjectName("partsList")
        self.verticalLayout.addWidget(self.partsList)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setContentsMargins(-1, 6, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.optionsGrid = QtWidgets.QGridLayout()
        self.optionsGrid.setContentsMargins(0, 0, 0, 0)
        self.optionsGrid.setObjectName("optionsGrid")
        self.gridLayout_2.addLayout(self.optionsGrid, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.widget)
        self.buildBtn = QtWidgets.QPushButton(self.groupBox)
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
        self.verticalLayout_3.addWidget(self.buildBtn)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadBtn = QtWidgets.QPushButton(TemplateUI)
        self.loadBtn.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.loadBtn.setStyleSheet("QPushButton{ \n"
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
        self.loadBtn.setObjectName("loadBtn")
        self.horizontalLayout.addWidget(self.loadBtn)
        self.saveBtn = QtWidgets.QPushButton(TemplateUI)
        self.saveBtn.setStyleSheet("QPushButton{ \n"
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
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout.addWidget(self.saveBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(TemplateUI)
        QtCore.QMetaObject.connectSlotsByName(TemplateUI)

    def retranslateUi(self, TemplateUI):
        TemplateUI.setWindowTitle(QtWidgets.QApplication.translate("TemplateUI", "Rig Build Template", None, -1))
        self.addBtn.setToolTip(QtWidgets.QApplication.translate("TemplateUI", "Mirror selected parts.", None, -1))
        self.addBtn.setText(QtWidgets.QApplication.translate("TemplateUI", "+ P a r t +", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("TemplateUI", "Part Options", None, -1))
        self.buildBtn.setText(QtWidgets.QApplication.translate("TemplateUI", "* B u i l d *", None, -1))
        self.loadBtn.setToolTip(QtWidgets.QApplication.translate("TemplateUI", "Load existing rig layout.", None, -1))
        self.loadBtn.setText(QtWidgets.QApplication.translate("TemplateUI", "Load Template", None, -1))
        self.saveBtn.setToolTip(QtWidgets.QApplication.translate("TemplateUI", "Save current rig layout.", None, -1))
        self.saveBtn.setText(QtWidgets.QApplication.translate("TemplateUI", "Save Template", None, -1))

