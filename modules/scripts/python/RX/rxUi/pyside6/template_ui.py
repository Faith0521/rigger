# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'templateUI.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_TemplateUI(object):
    def setupUi(self, TemplateUI):
        if not TemplateUI.objectName():
            TemplateUI.setObjectName(u"TemplateUI")
        TemplateUI.resize(665, 890)
        self.gridLayout = QGridLayout(TemplateUI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(TemplateUI)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.addBtn = QPushButton(self.verticalLayoutWidget)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMaximumSize(QSize(16777215, 16777215))
        self.addBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.verticalLayout.addWidget(self.addBtn)

        self.partsList = QListWidget(self.verticalLayoutWidget)
        self.partsList.setObjectName(u"partsList")
        self.partsList.setStyleSheet(u"QScrollBar{\n"
"                    border: 1px solid grey;\n"
"                    background:rgb(55,55,55);\n"
"                    width: 8px;}")
        self.partsList.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.partsList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.partsList)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 6, -1, -1)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(Qt.NoContextMenu)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 9)
        self.optionsGrid = QGridLayout()
        self.optionsGrid.setObjectName(u"optionsGrid")

        self.gridLayout_2.addLayout(self.optionsGrid, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.widget)

        self.buildBtn = QPushButton(self.groupBox)
        self.buildBtn.setObjectName(u"buildBtn")
        self.buildBtn.setMinimumSize(QSize(0, 37))
        font1 = QFont()
        font1.setPointSize(12)
        self.buildBtn.setFont(font1)
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

        self.verticalLayout_3.addWidget(self.buildBtn)

        self.verticalLayout_3.setStretch(2, 1)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loadBtn = QPushButton(TemplateUI)
        self.loadBtn.setObjectName(u"loadBtn")
        self.loadBtn.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.loadBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.horizontalLayout.addWidget(self.loadBtn)

        self.saveBtn = QPushButton(TemplateUI)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setStyleSheet(u"QPushButton{ \n"
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

        self.horizontalLayout.addWidget(self.saveBtn)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(TemplateUI)

        QMetaObject.connectSlotsByName(TemplateUI)
    # setupUi

    def retranslateUi(self, TemplateUI):
        TemplateUI.setWindowTitle(QCoreApplication.translate("TemplateUI", u"Rig Build Template", None))
#if QT_CONFIG(tooltip)
        self.addBtn.setToolTip(QCoreApplication.translate("TemplateUI", u"Mirror selected parts.", None))
#endif // QT_CONFIG(tooltip)
        self.addBtn.setText(QCoreApplication.translate("TemplateUI", u"+ P a r t +", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("TemplateUI", u"Part Options", None))
        self.buildBtn.setText(QCoreApplication.translate("TemplateUI", u"* B u i l d *", None))
#if QT_CONFIG(tooltip)
        self.loadBtn.setToolTip(QCoreApplication.translate("TemplateUI", u"Load existing rig layout.", None))
#endif // QT_CONFIG(tooltip)
        self.loadBtn.setText(QCoreApplication.translate("TemplateUI", u"Load Template", None))
#if QT_CONFIG(tooltip)
        self.saveBtn.setToolTip(QCoreApplication.translate("TemplateUI", u"Save current rig layout.", None))
#endif // QT_CONFIG(tooltip)
        self.saveBtn.setText(QCoreApplication.translate("TemplateUI", u"Save Template", None))
    # retranslateUi

