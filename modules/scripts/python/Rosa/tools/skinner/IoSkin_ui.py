# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\IoSkinUI.ui'
#
# Created: Thu Jul 20 15:03:37 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_IoSkinUI(object):
    def setupUi(self, IoSkinUI):
        IoSkinUI.setObjectName("IoSkinUI")
        IoSkinUI.resize(293, 168)
        self.centralwidget = QtWidgets.QWidget(IoSkinUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.io_gb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.io_gb.sizePolicy().hasHeightForWidth())
        self.io_gb.setSizePolicy(sizePolicy)
        self.io_gb.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.io_gb.setObjectName("io_gb")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.io_gb)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.selectSkinJnts_btn = QtWidgets.QPushButton(self.io_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectSkinJnts_btn.sizePolicy().hasHeightForWidth())
        self.selectSkinJnts_btn.setSizePolicy(sizePolicy)
        self.selectSkinJnts_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectSkinJnts_btn.setFont(font)
        self.selectSkinJnts_btn.setStyleSheet("QPushButton{ \n"
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
        self.selectSkinJnts_btn.setObjectName("selectSkinJnts_btn")
        self.verticalLayout_5.addWidget(self.selectSkinJnts_btn)
        self.injectionMode_layout = QtWidgets.QHBoxLayout()
        self.injectionMode_layout.setObjectName("injectionMode_layout")
        self.injectionMode_label = QtWidgets.QLabel(self.io_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.injectionMode_label.sizePolicy().hasHeightForWidth())
        self.injectionMode_label.setSizePolicy(sizePolicy)
        self.injectionMode_label.setMinimumSize(QtCore.QSize(0, 0))
        self.injectionMode_label.setObjectName("injectionMode_label")
        self.injectionMode_layout.addWidget(self.injectionMode_label)
        self.injectionMode_cb = QtWidgets.QComboBox(self.io_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.injectionMode_cb.sizePolicy().hasHeightForWidth())
        self.injectionMode_cb.setSizePolicy(sizePolicy)
        self.injectionMode_cb.setObjectName("injectionMode_cb")
        self.injectionMode_cb.addItem("")
        self.injectionMode_cb.addItem("")
        self.injectionMode_cb.addItem("")
        self.injectionMode_layout.addWidget(self.injectionMode_cb)
        self.verticalLayout_5.addLayout(self.injectionMode_layout)
        self.exportSkin_btn = QtWidgets.QPushButton(self.io_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportSkin_btn.sizePolicy().hasHeightForWidth())
        self.exportSkin_btn.setSizePolicy(sizePolicy)
        self.exportSkin_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.exportSkin_btn.setFont(font)
        self.exportSkin_btn.setStyleSheet("QPushButton{ \n"
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
        self.exportSkin_btn.setObjectName("exportSkin_btn")
        self.verticalLayout_5.addWidget(self.exportSkin_btn)
        self.importSkin_btn = QtWidgets.QPushButton(self.io_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importSkin_btn.sizePolicy().hasHeightForWidth())
        self.importSkin_btn.setSizePolicy(sizePolicy)
        self.importSkin_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.importSkin_btn.setFont(font)
        self.importSkin_btn.setStyleSheet("QPushButton{ \n"
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
        self.importSkin_btn.setObjectName("importSkin_btn")
        self.verticalLayout_5.addWidget(self.importSkin_btn)
        self.horizontalLayout.addWidget(self.io_gb)
        IoSkinUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(IoSkinUI)
        QtCore.QMetaObject.connectSlotsByName(IoSkinUI)

    def retranslateUi(self, IoSkinUI):
        IoSkinUI.setWindowTitle(QtWidgets.QApplication.translate("IoSkinUI", "IoSkin_v01", None, -1))
        self.io_gb.setTitle(QtWidgets.QApplication.translate("IoSkinUI", "IO", None, -1))
        self.selectSkinJnts_btn.setToolTip(QtWidgets.QApplication.translate("IoSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.selectSkinJnts_btn.setText(QtWidgets.QApplication.translate("IoSkinUI", "Select Skin Joints", None, -1))
        self.injectionMode_label.setText(QtWidgets.QApplication.translate("IoSkinUI", "Injection Mode:", None, -1))
        self.injectionMode_cb.setItemText(0, QtWidgets.QApplication.translate("IoSkinUI", "alembicIO", None, -1))
        self.injectionMode_cb.setItemText(1, QtWidgets.QApplication.translate("IoSkinUI", "mayaAscii", None, -1))
        self.injectionMode_cb.setItemText(2, QtWidgets.QApplication.translate("IoSkinUI", "mayaBinary", None, -1))
        self.exportSkin_btn.setToolTip(QtWidgets.QApplication.translate("IoSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.exportSkin_btn.setText(QtWidgets.QApplication.translate("IoSkinUI", "Export Skin Weights", None, -1))
        self.importSkin_btn.setToolTip(QtWidgets.QApplication.translate("IoSkinUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.importSkin_btn.setText(QtWidgets.QApplication.translate("IoSkinUI", "Import Skin Weights", None, -1))

