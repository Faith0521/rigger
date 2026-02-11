# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'buildUI.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_buildUI(object):
    def setupUi(self, buildUI):
        if not buildUI.objectName():
            buildUI.setObjectName(u"buildUI")
        buildUI.resize(379, 572)
        buildUI.setAcceptDrops(False)
        self.verticalLayout = QVBoxLayout(buildUI)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rigTypeBtn = QPushButton(buildUI)
        self.rigTypeBtn.setObjectName(u"rigTypeBtn")
        self.rigTypeBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.verticalLayout.addWidget(self.rigTypeBtn)

        self.buildList = QListWidget(buildUI)
        self.buildList.setObjectName(u"buildList")
        self.buildList.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.buildList.setStyleSheet(u"QScrollBar{\n"
"                    border: 1px solid grey;\n"
"                    background:rgb(55,55,55);\n"
"                    width: 8px;}")

        self.verticalLayout.addWidget(self.buildList)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(6)
        self.nextBtn = QPushButton(buildUI)
        self.nextBtn.setObjectName(u"nextBtn")
        self.nextBtn.setMinimumSize(QSize(0, 37))
        font = QFont()
        font.setPointSize(12)
        self.nextBtn.setFont(font)
        self.nextBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.gridLayout_3.addWidget(self.nextBtn, 0, 0, 1, 1)

        self.selBtn = QPushButton(buildUI)
        self.selBtn.setObjectName(u"selBtn")
        self.selBtn.setMinimumSize(QSize(0, 37))
        self.selBtn.setFont(font)
        self.selBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.gridLayout_3.addWidget(self.selBtn, 0, 1, 1, 1)

        self.buildBtn = QPushButton(buildUI)
        self.buildBtn.setObjectName(u"buildBtn")
        self.buildBtn.setMinimumSize(QSize(0, 37))
        self.buildBtn.setFont(font)
        self.buildBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.gridLayout_3.addWidget(self.buildBtn, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.groupBox = QGroupBox(buildUI)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 1))
        self.groupBox.setFlat(True)

        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loadBtn_2 = QPushButton(buildUI)
        self.loadBtn_2.setObjectName(u"loadBtn_2")

        self.horizontalLayout_3.addWidget(self.loadBtn_2)

        self.saveBtn_2 = QPushButton(buildUI)
        self.saveBtn_2.setObjectName(u"saveBtn_2")

        self.horizontalLayout_3.addWidget(self.saveBtn_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(buildUI)

        QMetaObject.connectSlotsByName(buildUI)
    # setupUi

    def retranslateUi(self, buildUI):
        buildUI.setWindowTitle(QCoreApplication.translate("buildUI", u"Rig Build", None))
        self.rigTypeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.nextBtn.setToolTip(QCoreApplication.translate("buildUI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.nextBtn.setText(QCoreApplication.translate("buildUI", u"Build Next", None))
#if QT_CONFIG(tooltip)
        self.selBtn.setToolTip(QCoreApplication.translate("buildUI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.selBtn.setText(QCoreApplication.translate("buildUI", u"To Selected", None))
#if QT_CONFIG(tooltip)
        self.buildBtn.setToolTip(QCoreApplication.translate("buildUI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the entire rig.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.buildBtn.setText(QCoreApplication.translate("buildUI", u"Build All", None))
        self.groupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.loadBtn_2.setToolTip(QCoreApplication.translate("buildUI", u"Load existing rig scene.", None))
#endif // QT_CONFIG(tooltip)
        self.loadBtn_2.setText(QCoreApplication.translate("buildUI", u"Load Work Scene", None))
#if QT_CONFIG(tooltip)
        self.saveBtn_2.setToolTip(QCoreApplication.translate("buildUI", u"Save current rig scene.", None))
#endif // QT_CONFIG(tooltip)
        self.saveBtn_2.setText(QCoreApplication.translate("buildUI", u"Save Work Scene", None))
    # retranslateUi

