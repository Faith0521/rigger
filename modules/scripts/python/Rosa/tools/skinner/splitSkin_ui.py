# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\splitSkinUI.ui'
#
# Created: Thu Jul 20 14:37:52 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_splitSkinUI(object):
    def setupUi(self, splitSkinUI):
        splitSkinUI.setObjectName("splitSkinUI")
        splitSkinUI.resize(296, 138)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(splitSkinUI.sizePolicy().hasHeightForWidth())
        splitSkinUI.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(splitSkinUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sp_gb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sp_gb.sizePolicy().hasHeightForWidth())
        self.sp_gb.setSizePolicy(sizePolicy)
        self.sp_gb.setCheckable(False)
        self.sp_gb.setObjectName("sp_gb")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sp_gb)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sp_gb_ht1 = QtWidgets.QHBoxLayout()
        self.sp_gb_ht1.setObjectName("sp_gb_ht1")
        self.split_type_label = QtWidgets.QLabel(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.split_type_label.sizePolicy().hasHeightForWidth())
        self.split_type_label.setSizePolicy(sizePolicy)
        self.split_type_label.setMinimumSize(QtCore.QSize(0, 0))
        self.split_type_label.setObjectName("split_type_label")
        self.sp_gb_ht1.addWidget(self.split_type_label)
        self.splite_type_cb = QtWidgets.QComboBox(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splite_type_cb.sizePolicy().hasHeightForWidth())
        self.splite_type_cb.setSizePolicy(sizePolicy)
        self.splite_type_cb.setObjectName("splite_type_cb")
        self.splite_type_cb.addItem("")
        self.splite_type_cb.addItem("")
        self.splite_type_cb.addItem("")
        self.splite_type_cb.addItem("")
        self.splite_type_cb.addItem("")
        self.splite_type_cb.addItem("")
        self.sp_gb_ht1.addWidget(self.splite_type_cb)
        self.split_softness_label = QtWidgets.QLabel(self.sp_gb)
        self.split_softness_label.setObjectName("split_softness_label")
        self.sp_gb_ht1.addWidget(self.split_softness_label)
        self.split_softness_dsb = QtWidgets.QDoubleSpinBox(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.split_softness_dsb.sizePolicy().hasHeightForWidth())
        self.split_softness_dsb.setSizePolicy(sizePolicy)
        self.split_softness_dsb.setDecimals(1)
        self.split_softness_dsb.setProperty("value", 2.0)
        self.split_softness_dsb.setObjectName("split_softness_dsb")
        self.sp_gb_ht1.addWidget(self.split_softness_dsb)
        self.verticalLayout.addLayout(self.sp_gb_ht1)
        self.sp_gb_ht2 = QtWidgets.QHBoxLayout()
        self.sp_gb_ht2.setObjectName("sp_gb_ht2")
        self.loadMesh_btn = QtWidgets.QPushButton(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadMesh_btn.sizePolicy().hasHeightForWidth())
        self.loadMesh_btn.setSizePolicy(sizePolicy)
        self.loadMesh_btn.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.loadMesh_btn.setFont(font)
        self.loadMesh_btn.setStyleSheet("QPushButton{ \n"
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
        self.loadMesh_btn.setObjectName("loadMesh_btn")
        self.sp_gb_ht2.addWidget(self.loadMesh_btn)
        self.loadMesh_line = QtWidgets.QLineEdit(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadMesh_line.sizePolicy().hasHeightForWidth())
        self.loadMesh_line.setSizePolicy(sizePolicy)
        self.loadMesh_line.setMinimumSize(QtCore.QSize(20, 0))
        self.loadMesh_line.setObjectName("loadMesh_line")
        self.sp_gb_ht2.addWidget(self.loadMesh_line)
        self.sp_gb_ht2.setStretch(1, 1)
        self.verticalLayout.addLayout(self.sp_gb_ht2)
        self.splitSkin_btn = QtWidgets.QPushButton(self.sp_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitSkin_btn.sizePolicy().hasHeightForWidth())
        self.splitSkin_btn.setSizePolicy(sizePolicy)
        self.splitSkin_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.splitSkin_btn.setFont(font)
        self.splitSkin_btn.setStyleSheet("QPushButton{ \n"
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
        self.splitSkin_btn.setObjectName("splitSkin_btn")
        self.verticalLayout.addWidget(self.splitSkin_btn)
        self.horizontalLayout.addWidget(self.sp_gb)
        splitSkinUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(splitSkinUI)
        QtCore.QMetaObject.connectSlotsByName(splitSkinUI)

    def retranslateUi(self, splitSkinUI):
        splitSkinUI.setWindowTitle(QtWidgets.QApplication.translate("splitSkinUI", "splitSkin_v01", None, -1))
        self.sp_gb.setTitle(QtWidgets.QApplication.translate("splitSkinUI", "Split", None, -1))
        self.split_type_label.setText(QtWidgets.QApplication.translate("splitSkinUI", " Type:", None, -1))
        self.splite_type_cb.setItemText(0, QtWidgets.QApplication.translate("splitSkinUI", "spine", None, -1))
        self.splite_type_cb.setItemText(1, QtWidgets.QApplication.translate("splitSkinUI", "belt", None, -1))
        self.splite_type_cb.setItemText(2, QtWidgets.QApplication.translate("splitSkinUI", "brow", None, -1))
        self.splite_type_cb.setItemText(3, QtWidgets.QApplication.translate("splitSkinUI", "transverse", None, -1))
        self.splite_type_cb.setItemText(4, QtWidgets.QApplication.translate("splitSkinUI", "cloth", None, -1))
        self.splite_type_cb.setItemText(5, QtWidgets.QApplication.translate("splitSkinUI", "eyes", None, -1))
        self.split_softness_label.setText(QtWidgets.QApplication.translate("splitSkinUI", "Softness:", None, -1))
        self.loadMesh_btn.setToolTip(QtWidgets.QApplication.translate("splitSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.loadMesh_btn.setText(QtWidgets.QApplication.translate("splitSkinUI", "mesh", None, -1))
        self.splitSkin_btn.setToolTip(QtWidgets.QApplication.translate("splitSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.splitSkin_btn.setText(QtWidgets.QApplication.translate("splitSkinUI", "Split Skin Weights", None, -1))

