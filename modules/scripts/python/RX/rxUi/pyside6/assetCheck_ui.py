# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetCheckUI.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QPushButton,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_assetCheckUI(object):
    def setupUi(self, assetCheckUI):
        if not assetCheckUI.objectName():
            assetCheckUI.setObjectName(u"assetCheckUI")
        assetCheckUI.resize(556, 1060)
        self.gridLayout = QGridLayout(assetCheckUI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkTree = QTreeWidget(assetCheckUI)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(2, u"3");
        __qtreewidgetitem.setText(1, u"2");
        __qtreewidgetitem.setText(0, u"1");
        self.checkTree.setHeaderItem(__qtreewidgetitem)
        self.checkTree.setObjectName(u"checkTree")
        self.checkTree.setEnabled(True)
        self.checkTree.setUniformRowHeights(True)
        self.checkTree.setAllColumnsShowFocus(True)
        self.checkTree.setHeaderHidden(True)
        self.checkTree.setColumnCount(3)
        self.checkTree.header().setMinimumSectionSize(60)
        self.checkTree.header().setDefaultSectionSize(60)
        self.checkTree.header().setStretchLastSection(False)

        self.gridLayout.addWidget(self.checkTree, 1, 0, 1, 2)

        self.ExportBtn = QPushButton(assetCheckUI)
        self.ExportBtn.setObjectName(u"ExportBtn")
        self.ExportBtn.setEnabled(True)
        self.ExportBtn.setMinimumSize(QSize(0, 35))
        self.ExportBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.gridLayout.addWidget(self.ExportBtn, 3, 0, 1, 2)

        self.fixBtn = QPushButton(assetCheckUI)
        self.fixBtn.setObjectName(u"fixBtn")
        self.fixBtn.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.fixBtn, 2, 1, 1, 1)

        self.checkBtn = QPushButton(assetCheckUI)
        self.checkBtn.setObjectName(u"checkBtn")
        self.checkBtn.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.checkBtn, 2, 0, 1, 1)

        self.checkTypeBtn = QPushButton(assetCheckUI)
        self.checkTypeBtn.setObjectName(u"checkTypeBtn")
        self.checkTypeBtn.setMinimumSize(QSize(0, 0))
        self.checkTypeBtn.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.checkTypeBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.gridLayout.addWidget(self.checkTypeBtn, 0, 0, 1, 2)


        self.retranslateUi(assetCheckUI)

        QMetaObject.connectSlotsByName(assetCheckUI)
    # setupUi

    def retranslateUi(self, assetCheckUI):
        assetCheckUI.setWindowTitle(QCoreApplication.translate("assetCheckUI", u"Asset Checker V1.0", None))
        self.ExportBtn.setText(QCoreApplication.translate("assetCheckUI", u"Publish model", None))
        self.fixBtn.setText(QCoreApplication.translate("assetCheckUI", u"Run Auto Fix", None))
        self.checkBtn.setText(QCoreApplication.translate("assetCheckUI", u"Run Checks", None))
        self.checkTypeBtn.setText(QCoreApplication.translate("assetCheckUI", u"model", None))
    # retranslateUi

