# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tagTools.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_tagToolsUI(object):
    def setupUi(self, tagToolsUI):
        if not tagToolsUI.objectName():
            tagToolsUI.setObjectName(u"tagToolsUI")
        tagToolsUI.resize(500, 866)
        self.verticalLayout_4 = QVBoxLayout(tagToolsUI)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pathHBox = QHBoxLayout()
        self.pathHBox.setSpacing(6)
        self.pathHBox.setObjectName(u"pathHBox")
        self.pathLabel = QLabel(tagToolsUI)
        self.pathLabel.setObjectName(u"pathLabel")

        self.pathHBox.addWidget(self.pathLabel)

        self.pathLine = QLineEdit(tagToolsUI)
        self.pathLine.setObjectName(u"pathLine")
        self.pathLine.setStyleSheet(u"background-color:#555555\n"
"\n"
"")
        self.pathLine.setFrame(False)
        self.pathLine.setReadOnly(True)

        self.pathHBox.addWidget(self.pathLine)

        self.browseBtn = QPushButton(tagToolsUI)
        self.browseBtn.setObjectName(u"browseBtn")
        self.browseBtn.setMaximumSize(QSize(30, 24))
        self.browseBtn.setStyleSheet(u"background-color:gray")
        self.browseBtn.setAutoDefault(True)
        self.browseBtn.setFlat(False)

        self.pathHBox.addWidget(self.browseBtn)

        self.reloadBtn = QPushButton(tagToolsUI)
        self.reloadBtn.setObjectName(u"reloadBtn")
        self.reloadBtn.setMaximumSize(QSize(30, 24))
        self.reloadBtn.setStyleSheet(u"background-color:gray")
        icon = QIcon()
        icon.addFile(u"icons/reloadSmall.png", QSize(), QIcon.Normal, QIcon.Off)
        self.reloadBtn.setIcon(icon)
        self.reloadBtn.setAutoDefault(True)
        self.reloadBtn.setFlat(False)

        self.pathHBox.addWidget(self.reloadBtn)


        self.verticalLayout_4.addLayout(self.pathHBox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.tagKeyBtn = QPushButton(tagToolsUI)
        self.tagKeyBtn.setObjectName(u"tagKeyBtn")
        self.tagKeyBtn.setMinimumSize(QSize(100, 0))
        self.tagKeyBtn.setMaximumSize(QSize(100, 16777215))
        self.tagKeyBtn.setContextMenuPolicy(Qt.NoContextMenu)
        self.tagKeyBtn.setStyleSheet(u"QPushButton {background-color:#5B5B5B;}\n"
"QPushButton:disabled {background-color:grey; color:rgb(246, 246, 246);}\n"
"")
        self.tagKeyBtn.setCheckable(True)
        self.tagKeyBtn.setChecked(True)

        self.horizontalLayout_5.addWidget(self.tagKeyBtn)

        self.tagSpaceBtn = QPushButton(tagToolsUI)
        self.tagSpaceBtn.setObjectName(u"tagSpaceBtn")
        self.tagSpaceBtn.setMinimumSize(QSize(100, 0))
        self.tagSpaceBtn.setMaximumSize(QSize(100, 16777215))
        self.tagSpaceBtn.setContextMenuPolicy(Qt.NoContextMenu)
        self.tagSpaceBtn.setStyleSheet(u"QPushButton {background-color:#5B5B5B;}\n"
"QPushButton:disabled {background-color:grey; color:rgb(246, 246, 246);}\n"
"")
        self.tagSpaceBtn.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.tagSpaceBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.widget_2 = QWidget(tagToolsUI)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(9)
        self.groupBox_2 = QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font = QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.splitter = QSplitter(self.groupBox_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setStyleSheet(u"background-color: rgb(55, 55, 55);")
        self.splitter.setFrameShape(QFrame.StyledPanel)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        self.frame_4 = QFrame(self.splitter)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.ctrlList_6 = QListWidget(self.frame_4)
        self.ctrlList_6.setObjectName(u"ctrlList_6")
        self.ctrlList_6.setMinimumSize(QSize(0, 0))
        self.ctrlList_6.setMaximumSize(QSize(16777215, 16777215))
        self.ctrlList_6.setLayoutDirection(Qt.LeftToRight)
        self.ctrlList_6.setStyleSheet(u"background-color:rgb(42,42,42)\n"
"")
        self.ctrlList_6.setFrameShape(QFrame.NoFrame)
        self.ctrlList_6.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ctrlList_6.setUniformItemSizes(True)

        self.verticalLayout_6.addWidget(self.ctrlList_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 2, 4)
        self.addCtrlBtn_4 = QPushButton(self.frame_4)
        self.addCtrlBtn_4.setObjectName(u"addCtrlBtn_4")
        self.addCtrlBtn_4.setMinimumSize(QSize(0, 0))
        self.addCtrlBtn_4.setMaximumSize(QSize(16777215, 20))
        font1 = QFont()
        font1.setPointSize(9)
        self.addCtrlBtn_4.setFont(font1)
        self.addCtrlBtn_4.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_3.addWidget(self.addCtrlBtn_4)

        self.rmCtrlBtn_4 = QPushButton(self.frame_4)
        self.rmCtrlBtn_4.setObjectName(u"rmCtrlBtn_4")
        self.rmCtrlBtn_4.setMinimumSize(QSize(0, 0))
        self.rmCtrlBtn_4.setMaximumSize(QSize(16777215, 20))
        self.rmCtrlBtn_4.setFont(font1)
        self.rmCtrlBtn_4.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_3.addWidget(self.rmCtrlBtn_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.splitter.addWidget(self.frame_4)
        self.frame_5 = QFrame(self.splitter)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listWidget = QListWidget(self.frame_5)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(50, 0))
        self.listWidget.setStyleSheet(u"background-color:rgb(42,42,42)\n"
"")
        self.listWidget.setFrameShape(QFrame.NoFrame)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_5.addWidget(self.listWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 4, 4, 4)
        self.CBBtn_2 = QPushButton(self.frame_5)
        self.CBBtn_2.setObjectName(u"CBBtn_2")
        self.CBBtn_2.setMaximumSize(QSize(16777215, 20))
        self.CBBtn_2.setFont(font1)
        self.CBBtn_2.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_4.addWidget(self.CBBtn_2)

        self.saveBtn_5 = QPushButton(self.frame_5)
        self.saveBtn_5.setObjectName(u"saveBtn_5")
        self.saveBtn_5.setMaximumSize(QSize(16777215, 20))
        self.saveBtn_5.setFont(font1)
        self.saveBtn_5.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_4.addWidget(self.saveBtn_5)

        self.saveBtn_4 = QPushButton(self.frame_5)
        self.saveBtn_4.setObjectName(u"saveBtn_4")
        self.saveBtn_4.setMaximumSize(QSize(16777215, 20))
        self.saveBtn_4.setFont(font1)
        self.saveBtn_4.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_4.addWidget(self.saveBtn_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.splitter.addWidget(self.frame_5)

        self.verticalLayout_2.addWidget(self.splitter)


        self.gridLayout_3.addWidget(self.groupBox_2, 2, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.widget = QWidget(tagToolsUI)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(9)
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 0)
        self.splitter_2 = QSplitter(self.groupBox_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setStyleSheet(u"background-color: rgb(55, 55, 55);")
        self.splitter_2.setFrameShape(QFrame.StyledPanel)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setHandleWidth(1)
        self.splitter_2.setChildrenCollapsible(False)
        self.frame_2 = QFrame(self.splitter_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ctrlList_5 = QListWidget(self.frame_2)
        self.ctrlList_5.setObjectName(u"ctrlList_5")
        self.ctrlList_5.setMinimumSize(QSize(0, 0))
        self.ctrlList_5.setMaximumSize(QSize(16777215, 16777215))
        self.ctrlList_5.setLayoutDirection(Qt.LeftToRight)
        self.ctrlList_5.setStyleSheet(u"background-color:rgb(42,42,42)\n"
"")
        self.ctrlList_5.setFrameShape(QFrame.NoFrame)
        self.ctrlList_5.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ctrlList_5.setUniformItemSizes(True)

        self.gridLayout.addWidget(self.ctrlList_5, 0, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 4, 2, 4)
        self.addCtrlBtn_3 = QPushButton(self.frame_2)
        self.addCtrlBtn_3.setObjectName(u"addCtrlBtn_3")
        self.addCtrlBtn_3.setMinimumSize(QSize(0, 0))
        self.addCtrlBtn_3.setMaximumSize(QSize(16777215, 20))
        self.addCtrlBtn_3.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_2.addWidget(self.addCtrlBtn_3)

        self.rmCtrlBtn_3 = QPushButton(self.frame_2)
        self.rmCtrlBtn_3.setObjectName(u"rmCtrlBtn_3")
        self.rmCtrlBtn_3.setMinimumSize(QSize(0, 0))
        self.rmCtrlBtn_3.setMaximumSize(QSize(16777215, 20))
        self.rmCtrlBtn_3.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout_2.addWidget(self.rmCtrlBtn_3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)

        self.splitter_2.addWidget(self.frame_2)
        self.frame_3 = QFrame(self.splitter_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"color:rgb(180, 180, 180)")

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)

        self.conBtn = QPushButton(self.frame_3)
        self.conBtn.setObjectName(u"conBtn")
        self.conBtn.setMinimumSize(QSize(75, 0))
        self.conBtn.setMaximumSize(QSize(16777215, 20))
        self.conBtn.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.gridLayout_4.addWidget(self.conBtn, 0, 2, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"color:rgb(180, 180, 180)")

        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)

        self.conLine = QLineEdit(self.frame_3)
        self.conLine.setObjectName(u"conLine")
        self.conLine.setMaximumSize(QSize(16777215, 20))
        self.conLine.setStyleSheet(u"background-color:rgb(42,42,42)\n"
"")
        self.conLine.setReadOnly(True)

        self.gridLayout_4.addWidget(self.conLine, 0, 1, 1, 1)

        self.defaultCmb = QComboBox(self.frame_3)
        self.defaultCmb.setObjectName(u"defaultCmb")
        self.defaultCmb.setMaximumSize(QSize(16777215, 20))
        self.defaultCmb.setStyleSheet(u"background-color:rgb(42,42,42)\n"
"")

        self.gridLayout_4.addWidget(self.defaultCmb, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"color:rgb(180, 180, 180)")

        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)

        self.checkBox = QCheckBox(self.frame_3)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setStyleSheet(u"")
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)

        self.gridLayout_4.addWidget(self.checkBox, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.spaceTree_3 = QTreeWidget(self.frame_3)
        self.spaceTree_3.headerItem().setText(2, "")
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Space Node");
        __qtreewidgetitem.setText(0, u"  Label");
        self.spaceTree_3.setHeaderItem(__qtreewidgetitem)
        self.spaceTree_3.setObjectName(u"spaceTree_3")
        self.spaceTree_3.setStyleSheet(u"background-color:rgb(42,42,42);\n"
"QPushButton {background-color:rgb(80,80,80);}\n"
"")
        self.spaceTree_3.setFrameShape(QFrame.NoFrame)
        self.spaceTree_3.setDragEnabled(False)
        self.spaceTree_3.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.spaceTree_3.setDefaultDropAction(Qt.IgnoreAction)
        self.spaceTree_3.setAlternatingRowColors(True)
        self.spaceTree_3.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.spaceTree_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.spaceTree_3.setUniformRowHeights(True)
        self.spaceTree_3.setAllColumnsShowFocus(True)
        self.spaceTree_3.setColumnCount(3)
        self.spaceTree_3.header().setVisible(True)
        self.spaceTree_3.header().setCascadingSectionResizes(True)
        self.spaceTree_3.header().setMinimumSectionSize(50)
        self.spaceTree_3.header().setDefaultSectionSize(50)
        self.spaceTree_3.header().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.spaceTree_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 4, 4, 4)
        self.addSpaceBtgn_3 = QPushButton(self.frame_3)
        self.addSpaceBtgn_3.setObjectName(u"addSpaceBtgn_3")
        self.addSpaceBtgn_3.setMaximumSize(QSize(16777215, 20))
        self.addSpaceBtgn_3.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout.addWidget(self.addSpaceBtgn_3)

        self.rmSpaceBtn_3 = QPushButton(self.frame_3)
        self.rmSpaceBtn_3.setObjectName(u"rmSpaceBtn_3")
        self.rmSpaceBtn_3.setMaximumSize(QSize(16777215, 20))
        self.rmSpaceBtn_3.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout.addWidget(self.rmSpaceBtn_3)

        self.rmSpaceBtn_4 = QPushButton(self.frame_3)
        self.rmSpaceBtn_4.setObjectName(u"rmSpaceBtn_4")
        self.rmSpaceBtn_4.setMaximumSize(QSize(35, 20))
        self.rmSpaceBtn_4.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout.addWidget(self.rmSpaceBtn_4)

        self.rmSpaceBtn_6 = QPushButton(self.frame_3)
        self.rmSpaceBtn_6.setObjectName(u"rmSpaceBtn_6")
        self.rmSpaceBtn_6.setMaximumSize(QSize(35, 20))
        self.rmSpaceBtn_6.setStyleSheet(u"QPushButton {background-color:rgb(80,80,80);}\n"
"")

        self.horizontalLayout.addWidget(self.rmSpaceBtn_6)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter_2.addWidget(self.frame_3)

        self.verticalLayout_3.addWidget(self.splitter_2)


        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.widget)

        self.exportDeformersBtn = QPushButton(tagToolsUI)
        self.exportDeformersBtn.setObjectName(u"exportDeformersBtn")
        self.exportDeformersBtn.setMinimumSize(QSize(0, 35))
        font2 = QFont()
        font2.setPointSize(12)
        self.exportDeformersBtn.setFont(font2)
        self.exportDeformersBtn.setStyleSheet(u"background-color:rgb(128,128,128)")

        self.verticalLayout_4.addWidget(self.exportDeformersBtn)

        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)

        self.retranslateUi(tagToolsUI)
        self.tagSpaceBtn.clicked.connect(self.tagKeyBtn.toggle)
        self.tagKeyBtn.clicked.connect(self.tagSpaceBtn.toggle)
        self.tagSpaceBtn.clicked.connect(self.widget.show)
        self.tagKeyBtn.clicked.connect(self.widget.hide)
        self.tagKeyBtn.clicked.connect(self.widget_2.show)
        self.tagSpaceBtn.clicked.connect(self.widget_2.hide)

        self.browseBtn.setDefault(False)
        self.reloadBtn.setDefault(False)


        QMetaObject.connectSlotsByName(tagToolsUI)
    # setupUi

    def retranslateUi(self, tagToolsUI):
        tagToolsUI.setWindowTitle(QCoreApplication.translate("tagToolsUI", u"Tag Tools", None))
        self.pathLabel.setText(QCoreApplication.translate("tagToolsUI", u"Export Path", None))
        self.browseBtn.setText(QCoreApplication.translate("tagToolsUI", u"...", None))
        self.tagKeyBtn.setText(QCoreApplication.translate("tagToolsUI", u"Attributes", None))
        self.tagSpaceBtn.setText(QCoreApplication.translate("tagToolsUI", u"Spaces", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("tagToolsUI", u"Tag Keyable Attributes    ", None))
        self.addCtrlBtn_4.setText(QCoreApplication.translate("tagToolsUI", u"+", None))
        self.rmCtrlBtn_4.setText(QCoreApplication.translate("tagToolsUI", u"-", None))
        self.CBBtn_2.setText(QCoreApplication.translate("tagToolsUI", u"Set From CB", None))
        self.saveBtn_5.setText(QCoreApplication.translate("tagToolsUI", u"Add From CB", None))
        self.saveBtn_4.setText(QCoreApplication.translate("tagToolsUI", u"Remove", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("tagToolsUI", u"Tag Spaces    ", None))
        self.addCtrlBtn_3.setText(QCoreApplication.translate("tagToolsUI", u"+", None))
        self.rmCtrlBtn_3.setText(QCoreApplication.translate("tagToolsUI", u"-", None))
        self.label_4.setText(QCoreApplication.translate("tagToolsUI", u"  Parent Node", None))
        self.conBtn.setText(QCoreApplication.translate("tagToolsUI", u"Get", None))
        self.label_5.setText(QCoreApplication.translate("tagToolsUI", u"  Default Space", None))
        self.label_6.setText(QCoreApplication.translate("tagToolsUI", u"  Rotation Only", None))
        self.checkBox.setText("")
        self.addSpaceBtgn_3.setText(QCoreApplication.translate("tagToolsUI", u"Add", None))
        self.rmSpaceBtn_3.setText(QCoreApplication.translate("tagToolsUI", u"Remove", None))
        self.rmSpaceBtn_4.setText(QCoreApplication.translate("tagToolsUI", u"\u2191", None))
        self.rmSpaceBtn_6.setText(QCoreApplication.translate("tagToolsUI", u"\u2193", None))
        self.exportDeformersBtn.setText(QCoreApplication.translate("tagToolsUI", u"Export Tags", None))
    # retranslateUi

