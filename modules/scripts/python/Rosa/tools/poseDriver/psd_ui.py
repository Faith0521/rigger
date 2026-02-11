# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\psdUI.ui'
#
# Created: Tue Sep  5 14:19:28 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PsdUI(object):
    def setupUi(self, PsdUI):
        PsdUI.setObjectName("PsdUI")
        PsdUI.resize(366, 156)
        self.centralwidget = QtWidgets.QWidget(PsdUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.parentObj_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parentObj_btn.setFont(font)
        self.parentObj_btn.setStyleSheet("QPushButton{ \n"
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
        self.parentObj_btn.setObjectName("parentObj_btn")
        self.horizontalLayout.addWidget(self.parentObj_btn)
        self.parentObj_line = QtWidgets.QLineEdit(self.centralwidget)
        self.parentObj_line.setObjectName("parentObj_line")
        self.horizontalLayout.addWidget(self.parentObj_line)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.followObj_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.followObj_btn.setFont(font)
        self.followObj_btn.setStyleSheet("QPushButton{ \n"
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
        self.followObj_btn.setObjectName("followObj_btn")
        self.horizontalLayout_2.addWidget(self.followObj_btn)
        self.followObj_line = QtWidgets.QLineEdit(self.centralwidget)
        self.followObj_line.setObjectName("followObj_line")
        self.horizontalLayout_2.addWidget(self.followObj_line)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lside_rb = QtWidgets.QRadioButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lside_rb.sizePolicy().hasHeightForWidth())
        self.lside_rb.setSizePolicy(sizePolicy)
        self.lside_rb.setObjectName("lside_rb")
        self.horizontalLayout_5.addWidget(self.lside_rb)
        self.rside_rb = QtWidgets.QRadioButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rside_rb.sizePolicy().hasHeightForWidth())
        self.rside_rb.setSizePolicy(sizePolicy)
        self.rside_rb.setObjectName("rside_rb")
        self.horizontalLayout_5.addWidget(self.rside_rb)
        self.mside_rb = QtWidgets.QRadioButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mside_rb.sizePolicy().hasHeightForWidth())
        self.mside_rb.setSizePolicy(sizePolicy)
        self.mside_rb.setObjectName("mside_rb")
        self.horizontalLayout_5.addWidget(self.mside_rb)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_6.addWidget(self.line_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.axis_lb = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axis_lb.sizePolicy().hasHeightForWidth())
        self.axis_lb.setSizePolicy(sizePolicy)
        self.axis_lb.setObjectName("axis_lb")
        self.horizontalLayout_4.addWidget(self.axis_lb)
        self.axis_cb = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axis_cb.sizePolicy().hasHeightForWidth())
        self.axis_cb.setSizePolicy(sizePolicy)
        self.axis_cb.setObjectName("axis_cb")
        self.axis_cb.addItem("")
        self.axis_cb.addItem("")
        self.axis_cb.addItem("")
        self.axis_cb.addItem("")
        self.axis_cb.addItem("")
        self.axis_cb.addItem("")
        self.horizontalLayout_4.addWidget(self.axis_cb)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_6.addWidget(self.line_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.scale_lb = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scale_lb.sizePolicy().hasHeightForWidth())
        self.scale_lb.setSizePolicy(sizePolicy)
        self.scale_lb.setObjectName("scale_lb")
        self.horizontalLayout_3.addWidget(self.scale_lb)
        self.scalePSD_dsb = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scalePSD_dsb.sizePolicy().hasHeightForWidth())
        self.scalePSD_dsb.setSizePolicy(sizePolicy)
        self.scalePSD_dsb.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.scalePSD_dsb.setWrapping(False)
        self.scalePSD_dsb.setFrame(False)
        self.scalePSD_dsb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.scalePSD_dsb.setKeyboardTracking(True)
        self.scalePSD_dsb.setSuffix("")
        self.scalePSD_dsb.setProperty("value", 0.05)
        self.scalePSD_dsb.setObjectName("scalePSD_dsb")
        self.horizontalLayout_3.addWidget(self.scalePSD_dsb)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.createPsd_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createPsd_btn.setFont(font)
        self.createPsd_btn.setStyleSheet("QPushButton{ \n"
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
        self.createPsd_btn.setObjectName("createPsd_btn")
        self.verticalLayout_2.addWidget(self.createPsd_btn)
        PsdUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(PsdUI)
        QtCore.QMetaObject.connectSlotsByName(PsdUI)

    def retranslateUi(self, PsdUI):
        PsdUI.setWindowTitle(QtWidgets.QApplication.translate("PsdUI", "PoseDriver_v2.0", None, -1))
        self.parentObj_btn.setText(QtWidgets.QApplication.translate("PsdUI", "Parent Obj >>", None, -1))
        self.followObj_btn.setText(QtWidgets.QApplication.translate("PsdUI", "Follow Obj >>", None, -1))
        self.lside_rb.setText(QtWidgets.QApplication.translate("PsdUI", "L", None, -1))
        self.rside_rb.setText(QtWidgets.QApplication.translate("PsdUI", "R", None, -1))
        self.mside_rb.setText(QtWidgets.QApplication.translate("PsdUI", "M", None, -1))
        self.axis_lb.setText(QtWidgets.QApplication.translate("PsdUI", "Axis", None, -1))
        self.axis_cb.setItemText(0, QtWidgets.QApplication.translate("PsdUI", "+x", None, -1))
        self.axis_cb.setItemText(1, QtWidgets.QApplication.translate("PsdUI", "+y", None, -1))
        self.axis_cb.setItemText(2, QtWidgets.QApplication.translate("PsdUI", "+z", None, -1))
        self.axis_cb.setItemText(3, QtWidgets.QApplication.translate("PsdUI", "-x", None, -1))
        self.axis_cb.setItemText(4, QtWidgets.QApplication.translate("PsdUI", "-y", None, -1))
        self.axis_cb.setItemText(5, QtWidgets.QApplication.translate("PsdUI", "-z", None, -1))
        self.scale_lb.setText(QtWidgets.QApplication.translate("PsdUI", "Scale:", None, -1))
        self.createPsd_btn.setText(QtWidgets.QApplication.translate("PsdUI", "create", None, -1))

