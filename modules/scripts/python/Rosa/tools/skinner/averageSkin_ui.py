# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\averageSkinUI.ui'
#
# Created: Thu Jul 20 11:16:16 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_averageSkinUI(object):
    def setupUi(self, averageSkinUI):
        averageSkinUI.setObjectName("averageSkinUI")
        averageSkinUI.resize(295, 174)
        self.centralwidget = QtWidgets.QWidget(averageSkinUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.av_gb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.av_gb.sizePolicy().hasHeightForWidth())
        self.av_gb.setSizePolicy(sizePolicy)
        self.av_gb.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.av_gb.setObjectName("av_gb")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.av_gb)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_a = QtWidgets.QHBoxLayout()
        self.horizontalLayout_a.setObjectName("horizontalLayout_a")
        self.jnt_a_btn = QtWidgets.QPushButton(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jnt_a_btn.sizePolicy().hasHeightForWidth())
        self.jnt_a_btn.setSizePolicy(sizePolicy)
        self.jnt_a_btn.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.jnt_a_btn.setFont(font)
        self.jnt_a_btn.setStyleSheet("QPushButton{ \n"
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
        self.jnt_a_btn.setObjectName("jnt_a_btn")
        self.horizontalLayout_a.addWidget(self.jnt_a_btn)
        self.jnt_a_line = QtWidgets.QLineEdit(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jnt_a_line.sizePolicy().hasHeightForWidth())
        self.jnt_a_line.setSizePolicy(sizePolicy)
        self.jnt_a_line.setMinimumSize(QtCore.QSize(20, 0))
        self.jnt_a_line.setObjectName("jnt_a_line")
        self.horizontalLayout_a.addWidget(self.jnt_a_line)
        self.horizontalLayout_a.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_a)
        self.horizontalLayout_b = QtWidgets.QHBoxLayout()
        self.horizontalLayout_b.setObjectName("horizontalLayout_b")
        self.jnt_b_btn = QtWidgets.QPushButton(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jnt_b_btn.sizePolicy().hasHeightForWidth())
        self.jnt_b_btn.setSizePolicy(sizePolicy)
        self.jnt_b_btn.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.jnt_b_btn.setFont(font)
        self.jnt_b_btn.setStyleSheet("QPushButton{ \n"
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
        self.jnt_b_btn.setObjectName("jnt_b_btn")
        self.horizontalLayout_b.addWidget(self.jnt_b_btn)
        self.jnt_b_line = QtWidgets.QLineEdit(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jnt_b_line.sizePolicy().hasHeightForWidth())
        self.jnt_b_line.setSizePolicy(sizePolicy)
        self.jnt_b_line.setMinimumSize(QtCore.QSize(20, 0))
        self.jnt_b_line.setObjectName("jnt_b_line")
        self.horizontalLayout_b.addWidget(self.jnt_b_line)
        self.horizontalLayout_b.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_b)
        self.horizontalLayout_c = QtWidgets.QHBoxLayout()
        self.horizontalLayout_c.setObjectName("horizontalLayout_c")
        self.skinPer_sp = QtWidgets.QDoubleSpinBox(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skinPer_sp.sizePolicy().hasHeightForWidth())
        self.skinPer_sp.setSizePolicy(sizePolicy)
        self.skinPer_sp.setMaximum(1.0)
        self.skinPer_sp.setSingleStep(0.05)
        self.skinPer_sp.setProperty("value", 0.5)
        self.skinPer_sp.setObjectName("skinPer_sp")
        self.horizontalLayout_c.addWidget(self.skinPer_sp)
        self.skinPer_sd = QtWidgets.QSlider(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.skinPer_sd.sizePolicy().hasHeightForWidth())
        self.skinPer_sd.setSizePolicy(sizePolicy)
        self.skinPer_sd.setMaximum(10)
        self.skinPer_sd.setSingleStep(20)
        self.skinPer_sd.setProperty("value", 5)
        self.skinPer_sd.setSliderPosition(5)
        self.skinPer_sd.setOrientation(QtCore.Qt.Horizontal)
        self.skinPer_sd.setTickInterval(0)
        self.skinPer_sd.setObjectName("skinPer_sd")
        self.horizontalLayout_c.addWidget(self.skinPer_sd)
        self.verticalLayout_3.addLayout(self.horizontalLayout_c)
        self.avSkin_btn = QtWidgets.QPushButton(self.av_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.avSkin_btn.sizePolicy().hasHeightForWidth())
        self.avSkin_btn.setSizePolicy(sizePolicy)
        self.avSkin_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.avSkin_btn.setFont(font)
        self.avSkin_btn.setStyleSheet("QPushButton{ \n"
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
        self.avSkin_btn.setObjectName("avSkin_btn")
        self.verticalLayout_3.addWidget(self.avSkin_btn)
        self.horizontalLayout.addWidget(self.av_gb)
        averageSkinUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(averageSkinUI)
        QtCore.QMetaObject.connectSlotsByName(averageSkinUI)

    def retranslateUi(self, averageSkinUI):
        averageSkinUI.setWindowTitle(QtWidgets.QApplication.translate("averageSkinUI", "AverageSkin_v01", None, -1))
        self.av_gb.setTitle(QtWidgets.QApplication.translate("averageSkinUI", "Average", None, -1))
        self.jnt_a_btn.setToolTip(QtWidgets.QApplication.translate("averageSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.jnt_a_btn.setText(QtWidgets.QApplication.translate("averageSkinUI", "jointA", None, -1))
        self.jnt_b_btn.setToolTip(QtWidgets.QApplication.translate("averageSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.jnt_b_btn.setText(QtWidgets.QApplication.translate("averageSkinUI", "jointB", None, -1))
        self.avSkin_btn.setToolTip(QtWidgets.QApplication.translate("averageSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.avSkin_btn.setText(QtWidgets.QApplication.translate("averageSkinUI", "Average Skin Weights", None, -1))

