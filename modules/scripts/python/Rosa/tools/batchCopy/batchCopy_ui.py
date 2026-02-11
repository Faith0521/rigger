# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\batchCopyUI.ui'
#
# Created: Wed Jul  5 10:39:03 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_batchCopyUI(object):
    def setupUi(self, batchCopyUI):
        batchCopyUI.setObjectName("batchCopyUI")
        batchCopyUI.resize(319, 524)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(batchCopyUI.sizePolicy().hasHeightForWidth())
        batchCopyUI.setSizePolicy(sizePolicy)
        batchCopyUI.setMinimumSize(QtCore.QSize(100, 0))
        batchCopyUI.setAcceptDrops(False)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(batchCopyUI)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.inf1_layout = QtWidgets.QHBoxLayout()
        self.inf1_layout.setObjectName("inf1_layout")
        self.inf1_label = QtWidgets.QLabel(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inf1_label.sizePolicy().hasHeightForWidth())
        self.inf1_label.setSizePolicy(sizePolicy)
        self.inf1_label.setMinimumSize(QtCore.QSize(10, 0))
        self.inf1_label.setObjectName("inf1_label")
        self.inf1_layout.addWidget(self.inf1_label)
        self.inf1_cb = QtWidgets.QComboBox(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inf1_cb.sizePolicy().hasHeightForWidth())
        self.inf1_cb.setSizePolicy(sizePolicy)
        self.inf1_cb.setObjectName("inf1_cb")
        self.inf1_cb.addItem("")
        self.inf1_cb.addItem("")
        self.inf1_cb.addItem("")
        self.inf1_cb.addItem("")
        self.inf1_cb.addItem("")
        self.inf1_layout.addWidget(self.inf1_cb)
        self.verticalLayout_3.addLayout(self.inf1_layout)
        self.inf2_layout = QtWidgets.QHBoxLayout()
        self.inf2_layout.setObjectName("inf2_layout")
        self.inf2_label = QtWidgets.QLabel(batchCopyUI)
        self.inf2_label.setObjectName("inf2_label")
        self.inf2_layout.addWidget(self.inf2_label)
        self.inf2_cb = QtWidgets.QComboBox(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inf2_cb.sizePolicy().hasHeightForWidth())
        self.inf2_cb.setSizePolicy(sizePolicy)
        self.inf2_cb.setObjectName("inf2_cb")
        self.inf2_cb.addItem("")
        self.inf2_cb.addItem("")
        self.inf2_cb.addItem("")
        self.inf2_cb.addItem("")
        self.inf2_cb.addItem("")
        self.inf2_layout.addWidget(self.inf2_cb)
        self.verticalLayout_3.addLayout(self.inf2_layout)
        self.cm_layout = QtWidgets.QHBoxLayout()
        self.cm_layout.setObjectName("cm_layout")
        self.cm_label = QtWidgets.QLabel(batchCopyUI)
        self.cm_label.setObjectName("cm_label")
        self.cm_layout.addWidget(self.cm_label)
        self.cm_cb = QtWidgets.QComboBox(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cm_cb.sizePolicy().hasHeightForWidth())
        self.cm_cb.setSizePolicy(sizePolicy)
        self.cm_cb.setObjectName("cm_cb")
        self.cm_cb.addItem("")
        self.cm_cb.addItem("")
        self.cm_cb.addItem("")
        self.cm_cb.addItem("")
        self.cm_layout.addWidget(self.cm_cb)
        self.verticalLayout_3.addLayout(self.cm_layout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.line = QtWidgets.QFrame(batchCopyUI)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.splitter = QtWidgets.QSplitter(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.old_mode_view = QtWidgets.QListWidget(self.layoutWidget)
        self.old_mode_view.setLineWidth(1)
        self.old_mode_view.setMidLineWidth(0)
        self.old_mode_view.setObjectName("old_mode_view")
        self.verticalLayout.addWidget(self.old_mode_view)
        self.old_mode_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.old_mode_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.old_mode_btn.setFont(font)
        self.old_mode_btn.setStyleSheet("QPushButton{ \n"
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
        self.old_mode_btn.setObjectName("old_mode_btn")
        self.verticalLayout.addWidget(self.old_mode_btn)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.new_mode_view = QtWidgets.QListWidget(self.layoutWidget1)
        self.new_mode_view.setLineWidth(1)
        self.new_mode_view.setMidLineWidth(0)
        self.new_mode_view.setObjectName("new_mode_view")
        self.verticalLayout_2.addWidget(self.new_mode_view)
        self.new_mode_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.new_mode_btn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.new_mode_btn.setFont(font)
        self.new_mode_btn.setStyleSheet("QPushButton{ \n"
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
        self.new_mode_btn.setObjectName("new_mode_btn")
        self.verticalLayout_2.addWidget(self.new_mode_btn)
        self.verticalLayout_4.addWidget(self.splitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.copySkin_btn = QtWidgets.QPushButton(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copySkin_btn.sizePolicy().hasHeightForWidth())
        self.copySkin_btn.setSizePolicy(sizePolicy)
        self.copySkin_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.copySkin_btn.setFont(font)
        self.copySkin_btn.setStyleSheet("QPushButton{ \n"
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
        self.copySkin_btn.setObjectName("copySkin_btn")
        self.verticalLayout_4.addWidget(self.copySkin_btn)
        self.copyBs_btn = QtWidgets.QPushButton(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyBs_btn.sizePolicy().hasHeightForWidth())
        self.copyBs_btn.setSizePolicy(sizePolicy)
        self.copyBs_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.copyBs_btn.setFont(font)
        self.copyBs_btn.setStyleSheet("QPushButton{ \n"
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
        self.copyBs_btn.setObjectName("copyBs_btn")
        self.verticalLayout_4.addWidget(self.copyBs_btn)
        self.replace_hierachy_btn = QtWidgets.QPushButton(batchCopyUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replace_hierachy_btn.sizePolicy().hasHeightForWidth())
        self.replace_hierachy_btn.setSizePolicy(sizePolicy)
        self.replace_hierachy_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.replace_hierachy_btn.setFont(font)
        self.replace_hierachy_btn.setStyleSheet("QPushButton{ \n"
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
        self.replace_hierachy_btn.setObjectName("replace_hierachy_btn")
        self.verticalLayout_4.addWidget(self.replace_hierachy_btn)

        self.retranslateUi(batchCopyUI)
        QtCore.QMetaObject.connectSlotsByName(batchCopyUI)

    def retranslateUi(self, batchCopyUI):
        batchCopyUI.setWindowTitle(QtWidgets.QApplication.translate("batchCopyUI", "batchCopy", None, -1))
        self.inf1_label.setText(QtWidgets.QApplication.translate("batchCopyUI", "Inf Association 1:", None, -1))
        self.inf1_cb.setItemText(0, QtWidgets.QApplication.translate("batchCopyUI", "closestJoint", None, -1))
        self.inf1_cb.setItemText(1, QtWidgets.QApplication.translate("batchCopyUI", "closestBone", None, -1))
        self.inf1_cb.setItemText(2, QtWidgets.QApplication.translate("batchCopyUI", "oneToOne", None, -1))
        self.inf1_cb.setItemText(3, QtWidgets.QApplication.translate("batchCopyUI", "label", None, -1))
        self.inf1_cb.setItemText(4, QtWidgets.QApplication.translate("batchCopyUI", "name", None, -1))
        self.inf2_label.setText(QtWidgets.QApplication.translate("batchCopyUI", "Inf Association 2:", None, -1))
        self.inf2_cb.setItemText(0, QtWidgets.QApplication.translate("batchCopyUI", "closestJoint", None, -1))
        self.inf2_cb.setItemText(1, QtWidgets.QApplication.translate("batchCopyUI", "closestBone", None, -1))
        self.inf2_cb.setItemText(2, QtWidgets.QApplication.translate("batchCopyUI", "oneToOne", None, -1))
        self.inf2_cb.setItemText(3, QtWidgets.QApplication.translate("batchCopyUI", "label", None, -1))
        self.inf2_cb.setItemText(4, QtWidgets.QApplication.translate("batchCopyUI", "name", None, -1))
        self.cm_label.setText(QtWidgets.QApplication.translate("batchCopyUI", "Copy Type", None, -1))
        self.cm_cb.setItemText(0, QtWidgets.QApplication.translate("batchCopyUI", "* to *", None, -1))
        self.cm_cb.setItemText(1, QtWidgets.QApplication.translate("batchCopyUI", "One to *", None, -1))
        self.cm_cb.setItemText(2, QtWidgets.QApplication.translate("batchCopyUI", "* to One", None, -1))
        self.cm_cb.setItemText(3, QtWidgets.QApplication.translate("batchCopyUI", "Custom", None, -1))
        self.old_mode_btn.setToolTip(QtWidgets.QApplication.translate("batchCopyUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.old_mode_btn.setText(QtWidgets.QApplication.translate("batchCopyUI", "Load Old Mesh", None, -1))
        self.new_mode_btn.setToolTip(QtWidgets.QApplication.translate("batchCopyUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.new_mode_btn.setText(QtWidgets.QApplication.translate("batchCopyUI", "Load New Mesh", None, -1))
        self.copySkin_btn.setToolTip(QtWidgets.QApplication.translate("batchCopyUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.copySkin_btn.setText(QtWidgets.QApplication.translate("batchCopyUI", "Copy Skin", None, -1))
        self.copyBs_btn.setToolTip(QtWidgets.QApplication.translate("batchCopyUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.copyBs_btn.setText(QtWidgets.QApplication.translate("batchCopyUI", "Copy BS", None, -1))
        self.replace_hierachy_btn.setToolTip(QtWidgets.QApplication.translate("batchCopyUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.replace_hierachy_btn.setText(QtWidgets.QApplication.translate("batchCopyUI", "Replace Hierachy", None, -1))

