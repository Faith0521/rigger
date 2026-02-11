# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\handUI.ui'
#
# Created: Thu Apr 17 13:03:53 2025
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_handUI(object):
    def setupUi(self, handUI):
        handUI.setObjectName("handUI")
        handUI.resize(273, 228)
        handUI.setMinimumSize(QtCore.QSize(0, 228))
        handUI.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_2 = QtWidgets.QGridLayout(handUI)
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(handUI)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setStyleSheet("background-color:rgb(42,42,42);")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(4, 2, 8, 2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:lightGrey")
        self.label_7.setIndent(10)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(handUI)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buildBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.buildBtn.setObjectName("buildBtn")
        self.verticalLayout.addWidget(self.buildBtn)
        self.rebuildBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.rebuildBtn.setObjectName("rebuildBtn")
        self.verticalLayout.addWidget(self.rebuildBtn)
        self.mirrorBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.mirrorBtn.setObjectName("mirrorBtn")
        self.verticalLayout.addWidget(self.mirrorBtn)
        self.exportBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.exportBtn.setObjectName("exportBtn")
        self.verticalLayout.addWidget(self.exportBtn)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 8, 0, 1, 1)

        self.retranslateUi(handUI)
        QtCore.QMetaObject.connectSlotsByName(handUI)

    def retranslateUi(self, handUI):
        handUI.setWindowTitle(QtWidgets.QApplication.translate("handUI", "Hand Poses", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("handUI", "Hand Pose Set", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("handUI", "Set Pose", None, -1))
        self.buildBtn.setText(QtWidgets.QApplication.translate("handUI", "Build Pose", None, -1))
        self.rebuildBtn.setText(QtWidgets.QApplication.translate("handUI", "Rebuild Pose", None, -1))
        self.mirrorBtn.setText(QtWidgets.QApplication.translate("handUI", "Mirror / Copy Poses", None, -1))
        self.exportBtn.setText(QtWidgets.QApplication.translate("handUI", "Export Poses", None, -1))

