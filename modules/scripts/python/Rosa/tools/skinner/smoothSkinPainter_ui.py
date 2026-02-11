# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\smoothSkinPainterUI.ui'
#
# Created: Thu Jul 20 15:38:03 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_smoothSkinPainterUI(object):
    def setupUi(self, smoothSkinPainterUI):
        smoothSkinPainterUI.setObjectName("smoothSkinPainterUI")
        smoothSkinPainterUI.resize(240, 76)
        self.centralwidget = QtWidgets.QWidget(smoothSkinPainterUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Paint_gb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Paint_gb.sizePolicy().hasHeightForWidth())
        self.Paint_gb.setSizePolicy(sizePolicy)
        self.Paint_gb.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Paint_gb.setObjectName("Paint_gb")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.Paint_gb)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.smoothBrush_btn = QtWidgets.QPushButton(self.Paint_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smoothBrush_btn.sizePolicy().hasHeightForWidth())
        self.smoothBrush_btn.setSizePolicy(sizePolicy)
        self.smoothBrush_btn.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.smoothBrush_btn.setFont(font)
        self.smoothBrush_btn.setStyleSheet("QPushButton{ \n"
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
        self.smoothBrush_btn.setObjectName("smoothBrush_btn")
        self.verticalLayout_6.addWidget(self.smoothBrush_btn)
        self.horizontalLayout.addWidget(self.Paint_gb)
        smoothSkinPainterUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(smoothSkinPainterUI)
        QtCore.QMetaObject.connectSlotsByName(smoothSkinPainterUI)

    def retranslateUi(self, smoothSkinPainterUI):
        smoothSkinPainterUI.setWindowTitle(QtWidgets.QApplication.translate("smoothSkinPainterUI", "smoothSkinPainter_v01", None, -1))
        self.Paint_gb.setTitle(QtWidgets.QApplication.translate("smoothSkinPainterUI", "Paint", None, -1))
        self.smoothBrush_btn.setToolTip(QtWidgets.QApplication.translate("smoothSkinPainterUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.smoothBrush_btn.setText(QtWidgets.QApplication.translate("smoothSkinPainterUI", "Smooth Painter Brush", None, -1))

