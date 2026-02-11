# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pruneSkinUI.ui'
#
# Created: Thu Jul 20 13:48:18 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_pruneSkinUI(object):
    def setupUi(self, pruneSkinUI):
        pruneSkinUI.setObjectName("pruneSkinUI")
        pruneSkinUI.resize(297, 172)
        self.centralwidget = QtWidgets.QWidget(pruneSkinUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prune_gb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prune_gb.sizePolicy().hasHeightForWidth())
        self.prune_gb.setSizePolicy(sizePolicy)
        self.prune_gb.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.prune_gb.setObjectName("prune_gb")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.prune_gb)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.sp_gb_ht1_a = QtWidgets.QHBoxLayout()
        self.sp_gb_ht1_a.setObjectName("sp_gb_ht1_a")
        self.limit_lb = QtWidgets.QLabel(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.limit_lb.sizePolicy().hasHeightForWidth())
        self.limit_lb.setSizePolicy(sizePolicy)
        self.limit_lb.setMinimumSize(QtCore.QSize(0, 0))
        self.limit_lb.setObjectName("limit_lb")
        self.sp_gb_ht1_a.addWidget(self.limit_lb)
        self.limit_sb = QtWidgets.QSpinBox(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.limit_sb.sizePolicy().hasHeightForWidth())
        self.limit_sb.setSizePolicy(sizePolicy)
        self.limit_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.limit_sb.setProperty("value", 8)
        self.limit_sb.setObjectName("limit_sb")
        self.sp_gb_ht1_a.addWidget(self.limit_sb)
        self.decimal_lb = QtWidgets.QLabel(self.prune_gb)
        self.decimal_lb.setObjectName("decimal_lb")
        self.sp_gb_ht1_a.addWidget(self.decimal_lb)
        self.decimal_sb = QtWidgets.QSpinBox(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.decimal_sb.sizePolicy().hasHeightForWidth())
        self.decimal_sb.setSizePolicy(sizePolicy)
        self.decimal_sb.setFrame(True)
        self.decimal_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.decimal_sb.setKeyboardTracking(True)
        self.decimal_sb.setProperty("value", 3)
        self.decimal_sb.setObjectName("decimal_sb")
        self.sp_gb_ht1_a.addWidget(self.decimal_sb)
        self.verticalLayout_4.addLayout(self.sp_gb_ht1_a)
        self.horizontalLayout_a = QtWidgets.QHBoxLayout()
        self.horizontalLayout_a.setObjectName("horizontalLayout_a")
        self.greater_btn = QtWidgets.QPushButton(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.greater_btn.sizePolicy().hasHeightForWidth())
        self.greater_btn.setSizePolicy(sizePolicy)
        self.greater_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.greater_btn.setFont(font)
        self.greater_btn.setStyleSheet("QPushButton{ \n"
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
        self.greater_btn.setObjectName("greater_btn")
        self.horizontalLayout_a.addWidget(self.greater_btn)
        self.equal_btn = QtWidgets.QPushButton(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.equal_btn.sizePolicy().hasHeightForWidth())
        self.equal_btn.setSizePolicy(sizePolicy)
        self.equal_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.equal_btn.setFont(font)
        self.equal_btn.setStyleSheet("QPushButton{ \n"
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
        self.equal_btn.setObjectName("equal_btn")
        self.horizontalLayout_a.addWidget(self.equal_btn)
        self.less_btn = QtWidgets.QPushButton(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.less_btn.sizePolicy().hasHeightForWidth())
        self.less_btn.setSizePolicy(sizePolicy)
        self.less_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.less_btn.setFont(font)
        self.less_btn.setStyleSheet("QPushButton{ \n"
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
        self.less_btn.setObjectName("less_btn")
        self.horizontalLayout_a.addWidget(self.less_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_a)
        self.setSkinLimit_btn = QtWidgets.QPushButton(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setSkinLimit_btn.sizePolicy().hasHeightForWidth())
        self.setSkinLimit_btn.setSizePolicy(sizePolicy)
        self.setSkinLimit_btn.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setSkinLimit_btn.setFont(font)
        self.setSkinLimit_btn.setStyleSheet("QPushButton{ \n"
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
        self.setSkinLimit_btn.setObjectName("setSkinLimit_btn")
        self.verticalLayout_4.addWidget(self.setSkinLimit_btn)
        self.prune_gb_ht1_a = QtWidgets.QHBoxLayout()
        self.prune_gb_ht1_a.setObjectName("prune_gb_ht1_a")
        self.smallWeight_sp = QtWidgets.QDoubleSpinBox(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smallWeight_sp.sizePolicy().hasHeightForWidth())
        self.smallWeight_sp.setSizePolicy(sizePolicy)
        self.smallWeight_sp.setDecimals(3)
        self.smallWeight_sp.setMaximum(1.0)
        self.smallWeight_sp.setSingleStep(0.05)
        self.smallWeight_sp.setProperty("value", 0.001)
        self.smallWeight_sp.setObjectName("smallWeight_sp")
        self.prune_gb_ht1_a.addWidget(self.smallWeight_sp)
        self.pruneSmall_btn = QtWidgets.QPushButton(self.prune_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pruneSmall_btn.sizePolicy().hasHeightForWidth())
        self.pruneSmall_btn.setSizePolicy(sizePolicy)
        self.pruneSmall_btn.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pruneSmall_btn.setFont(font)
        self.pruneSmall_btn.setStyleSheet("QPushButton{ \n"
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
        self.pruneSmall_btn.setObjectName("pruneSmall_btn")
        self.prune_gb_ht1_a.addWidget(self.pruneSmall_btn)
        self.verticalLayout_4.addLayout(self.prune_gb_ht1_a)
        self.horizontalLayout_2.addWidget(self.prune_gb)
        pruneSkinUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(pruneSkinUI)
        QtCore.QMetaObject.connectSlotsByName(pruneSkinUI)

    def retranslateUi(self, pruneSkinUI):
        pruneSkinUI.setWindowTitle(QtWidgets.QApplication.translate("pruneSkinUI", "PruneSkin_v01", None, -1))
        self.prune_gb.setTitle(QtWidgets.QApplication.translate("pruneSkinUI", "Prune", None, -1))
        self.limit_lb.setText(QtWidgets.QApplication.translate("pruneSkinUI", " Limit:", None, -1))
        self.decimal_lb.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Decimal:", None, -1))
        self.greater_btn.setToolTip(QtWidgets.QApplication.translate("pruneSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.greater_btn.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Greater", None, -1))
        self.equal_btn.setToolTip(QtWidgets.QApplication.translate("pruneSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.equal_btn.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Equal", None, -1))
        self.less_btn.setToolTip(QtWidgets.QApplication.translate("pruneSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.less_btn.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Less", None, -1))
        self.setSkinLimit_btn.setToolTip(QtWidgets.QApplication.translate("pruneSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.setSkinLimit_btn.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Set Skin Limit", None, -1))
        self.pruneSmall_btn.setToolTip(QtWidgets.QApplication.translate("pruneSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.pruneSmall_btn.setText(QtWidgets.QApplication.translate("pruneSkinUI", "Prune Small", None, -1))

