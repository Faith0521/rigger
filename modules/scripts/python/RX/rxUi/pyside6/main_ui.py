# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_rs_win(object):
    def setupUi(self, rs_win):
        if not rs_win.objectName():
            rs_win.setObjectName(u"rs_win")
        rs_win.resize(380, 790)
        rs_win.setMinimumSize(QSize(380, 0))
        self.verticalLayout = QVBoxLayout(rs_win)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.assetInfoHBox = QHBoxLayout()
        self.assetInfoHBox.setObjectName(u"assetInfoHBox")
        self.assetInfoFrame = QFrame(rs_win)
        self.assetInfoFrame.setObjectName(u"assetInfoFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assetInfoFrame.sizePolicy().hasHeightForWidth())
        self.assetInfoFrame.setSizePolicy(sizePolicy)
        self.assetInfoFrame.setSizeIncrement(QSize(0, 100))
        self.assetInfoFrame.setStyleSheet(u"background-color: rgb(60,60,60);\n"
"")
        self.assetInfoFrame.setFrameShape(QFrame.NoFrame)
        self.assetInfoFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.assetInfoFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.assetsInfoHBox = QHBoxLayout()
        self.assetsInfoHBox.setObjectName(u"assetsInfoHBox")
        self.idLb = QLabel(self.assetInfoFrame)
        self.idLb.setObjectName(u"idLb")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.idLb.sizePolicy().hasHeightForWidth())
        self.idLb.setSizePolicy(sizePolicy1)
        self.idLb.setMinimumSize(QSize(120, 120))

        self.assetsInfoHBox.addWidget(self.idLb)

        self.assetsInfo01Line = QFrame(self.assetInfoFrame)
        self.assetsInfo01Line.setObjectName(u"assetsInfo01Line")
        self.assetsInfo01Line.setFrameShape(QFrame.VLine)
        self.assetsInfo01Line.setFrameShadow(QFrame.Sunken)

        self.assetsInfoHBox.addWidget(self.assetsInfo01Line)

        self.assetsInfoVBox = QVBoxLayout()
        self.assetsInfoVBox.setObjectName(u"assetsInfoVBox")
        self.assetsNameHBox = QHBoxLayout()
        self.assetsNameHBox.setObjectName(u"assetsNameHBox")
        self.assetNameLabel = QLabel(self.assetInfoFrame)
        self.assetNameLabel.setObjectName(u"assetNameLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.assetNameLabel.sizePolicy().hasHeightForWidth())
        self.assetNameLabel.setSizePolicy(sizePolicy2)
        self.assetNameLabel.setMinimumSize(QSize(0, 0))
        self.assetNameLabel.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setBold(False)
        self.assetNameLabel.setFont(font)

        self.assetsNameHBox.addWidget(self.assetNameLabel)

        self.assetNameDate = QLabel(self.assetInfoFrame)
        self.assetNameDate.setObjectName(u"assetNameDate")
        sizePolicy2.setHeightForWidth(self.assetNameDate.sizePolicy().hasHeightForWidth())
        self.assetNameDate.setSizePolicy(sizePolicy2)
        self.assetNameDate.setMinimumSize(QSize(0, 20))
        font1 = QFont()
        font1.setPointSize(10)
        self.assetNameDate.setFont(font1)
        self.assetNameDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.assetsNameHBox.addWidget(self.assetNameDate)


        self.assetsInfoVBox.addLayout(self.assetsNameHBox)

        self.assetsDateHBox = QHBoxLayout()
        self.assetsDateHBox.setObjectName(u"assetsDateHBox")
        self.createdLabel = QLabel(self.assetInfoFrame)
        self.createdLabel.setObjectName(u"createdLabel")
        sizePolicy2.setHeightForWidth(self.createdLabel.sizePolicy().hasHeightForWidth())
        self.createdLabel.setSizePolicy(sizePolicy2)
        self.createdLabel.setMinimumSize(QSize(0, 0))
        self.createdLabel.setSizeIncrement(QSize(0, 0))
        self.createdLabel.setFont(font)

        self.assetsDateHBox.addWidget(self.createdLabel)

        self.createdDate = QLabel(self.assetInfoFrame)
        self.createdDate.setObjectName(u"createdDate")
        sizePolicy2.setHeightForWidth(self.createdDate.sizePolicy().hasHeightForWidth())
        self.createdDate.setSizePolicy(sizePolicy2)
        self.createdDate.setMinimumSize(QSize(0, 20))
        self.createdDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.assetsDateHBox.addWidget(self.createdDate)


        self.assetsInfoVBox.addLayout(self.assetsDateHBox)

        self.assetsAuthorHBox = QHBoxLayout()
        self.assetsAuthorHBox.setObjectName(u"assetsAuthorHBox")
        self.modLabel = QLabel(self.assetInfoFrame)
        self.modLabel.setObjectName(u"modLabel")
        sizePolicy2.setHeightForWidth(self.modLabel.sizePolicy().hasHeightForWidth())
        self.modLabel.setSizePolicy(sizePolicy2)
        self.modLabel.setMinimumSize(QSize(0, 0))
        self.modLabel.setSizeIncrement(QSize(0, 0))
        self.modLabel.setFont(font)

        self.assetsAuthorHBox.addWidget(self.modLabel)

        self.modDate = QLabel(self.assetInfoFrame)
        self.modDate.setObjectName(u"modDate")
        sizePolicy2.setHeightForWidth(self.modDate.sizePolicy().hasHeightForWidth())
        self.modDate.setSizePolicy(sizePolicy2)
        self.modDate.setMinimumSize(QSize(0, 20))
        self.modDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.assetsAuthorHBox.addWidget(self.modDate)


        self.assetsInfoVBox.addLayout(self.assetsAuthorHBox)

        self.assetsInfo02Line = QFrame(self.assetInfoFrame)
        self.assetsInfo02Line.setObjectName(u"assetsInfo02Line")
        self.assetsInfo02Line.setFrameShape(QFrame.HLine)
        self.assetsInfo02Line.setFrameShadow(QFrame.Sunken)

        self.assetsInfoVBox.addWidget(self.assetsInfo02Line)

        self.assetsEditHBox = QHBoxLayout()
        self.assetsEditHBox.setObjectName(u"assetsEditHBox")
        self.setBtn = QPushButton(self.assetInfoFrame)
        self.setBtn.setObjectName(u"setBtn")
        sizePolicy2.setHeightForWidth(self.setBtn.sizePolicy().hasHeightForWidth())
        self.setBtn.setSizePolicy(sizePolicy2)
        self.setBtn.setMinimumSize(QSize(25, 25))
        self.setBtn.setMaximumSize(QSize(25, 25))
        self.setBtn.setFont(font1)
        self.setBtn.setCheckable(True)
        self.setBtn.setFlat(True)

        self.assetsEditHBox.addWidget(self.setBtn)

        self.rigTypeDate = QLabel(self.assetInfoFrame)
        self.rigTypeDate.setObjectName(u"rigTypeDate")
        sizePolicy2.setHeightForWidth(self.rigTypeDate.sizePolicy().hasHeightForWidth())
        self.rigTypeDate.setSizePolicy(sizePolicy2)
        self.rigTypeDate.setMinimumSize(QSize(0, 20))
        self.rigTypeDate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.assetsEditHBox.addWidget(self.rigTypeDate)

        self.newRigBtn = QPushButton(self.assetInfoFrame)
        self.newRigBtn.setObjectName(u"newRigBtn")
        sizePolicy2.setHeightForWidth(self.newRigBtn.sizePolicy().hasHeightForWidth())
        self.newRigBtn.setSizePolicy(sizePolicy2)
        self.newRigBtn.setMinimumSize(QSize(25, 25))
        self.newRigBtn.setMaximumSize(QSize(25, 25))
        self.newRigBtn.setFont(font1)
        self.newRigBtn.setFlat(True)

        self.assetsEditHBox.addWidget(self.newRigBtn)


        self.assetsInfoVBox.addLayout(self.assetsEditHBox)


        self.assetsInfoHBox.addLayout(self.assetsInfoVBox)


        self.verticalLayout_4.addLayout(self.assetsInfoHBox)

        self.stratInfoLb = QLabel(self.assetInfoFrame)
        self.stratInfoLb.setObjectName(u"stratInfoLb")

        self.verticalLayout_4.addWidget(self.stratInfoLb)


        self.assetInfoHBox.addWidget(self.assetInfoFrame)


        self.verticalLayout.addLayout(self.assetInfoHBox)

        self.envWdg = QWidget(rs_win)
        self.envWdg.setObjectName(u"envWdg")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.envWdg.sizePolicy().hasHeightForWidth())
        self.envWdg.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.envWdg)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.assetFrame = QFrame(self.envWdg)
        self.assetFrame.setObjectName(u"assetFrame")
        sizePolicy2.setHeightForWidth(self.assetFrame.sizePolicy().hasHeightForWidth())
        self.assetFrame.setSizePolicy(sizePolicy2)
        self.assetFrame.setStyleSheet(u"")
        self.assetFrame.setFrameShape(QFrame.StyledPanel)
        self.assetFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.assetFrame)
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.assetList = QListWidget(self.assetFrame)
        self.assetList.setObjectName(u"assetList")
        self.assetList.setFrameShape(QFrame.NoFrame)
        self.assetList.setLineWidth(1)
        self.assetList.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.assetList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.assetList.setIconSize(QSize(40, 40))
        self.assetList.setMovement(QListView.Static)
        self.assetList.setFlow(QListView.LeftToRight)
        self.assetList.setProperty("isWrapping", False)
        self.assetList.setResizeMode(QListView.Fixed)
        self.assetList.setGridSize(QSize(70, 70))
        self.assetList.setViewMode(QListView.IconMode)
        self.assetList.setSelectionRectVisible(False)

        self.horizontalLayout_4.addWidget(self.assetList)


        self.verticalLayout_2.addWidget(self.assetFrame)

        self.searchHbl = QHBoxLayout()
        self.searchHbl.setObjectName(u"searchHbl")
        self.seartch_lb = QLabel(self.envWdg)
        self.seartch_lb.setObjectName(u"seartch_lb")

        self.searchHbl.addWidget(self.seartch_lb)

        self.searchLine = QLineEdit(self.envWdg)
        self.searchLine.setObjectName(u"searchLine")

        self.searchHbl.addWidget(self.searchLine)


        self.verticalLayout_2.addLayout(self.searchHbl)

        self.assetCmdHBox = QHBoxLayout()
        self.assetCmdHBox.setObjectName(u"assetCmdHBox")
        self.newAssetBtn = QPushButton(self.envWdg)
        self.newAssetBtn.setObjectName(u"newAssetBtn")
        self.newAssetBtn.setMinimumSize(QSize(0, 40))
        font2 = QFont()
        font2.setBold(False)
        font2.setItalic(False)
        self.newAssetBtn.setFont(font2)
        self.newAssetBtn.setStyleSheet(u"QPushButton{ \n"
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
        self.newAssetBtn.setFlat(False)

        self.assetCmdHBox.addWidget(self.newAssetBtn)


        self.verticalLayout_2.addLayout(self.assetCmdHBox)

        self.rootHBox = QHBoxLayout()
        self.rootHBox.setSpacing(10)
        self.rootHBox.setObjectName(u"rootHBox")
        self.rootHBox.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.rootHBox.setContentsMargins(-1, -1, -1, 0)
        self.rootLine = QLineEdit(self.envWdg)
        self.rootLine.setObjectName(u"rootLine")
        self.rootLine.setMaximumSize(QSize(16777215, 25))
        self.rootLine.setStyleSheet(u"QLineEdit{color:grey;\n"
"background-color:rgb(60,60,60);}\n"
"")
        self.rootLine.setFrame(False)
        self.rootLine.setReadOnly(True)

        self.rootHBox.addWidget(self.rootLine)

        self.rootBtn = QPushButton(self.envWdg)
        self.rootBtn.setObjectName(u"rootBtn")
        self.rootBtn.setMaximumSize(QSize(50, 25))
        self.rootBtn.setFont(font1)
        self.rootBtn.setStyleSheet(u"QPushButton{color:grey;\n"
"background-color:rgb(60,60,60);}\n"
"")
        self.rootBtn.setIconSize(QSize(0, 0))
        self.rootBtn.setFlat(True)

        self.rootHBox.addWidget(self.rootBtn)

        self.rootHBox.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.rootHBox)


        self.verticalLayout.addWidget(self.envWdg)

        self.tabsWdg = QTabWidget(rs_win)
        self.tabsWdg.setObjectName(u"tabsWdg")
        sizePolicy3.setHeightForWidth(self.tabsWdg.sizePolicy().hasHeightForWidth())
        self.tabsWdg.setSizePolicy(sizePolicy3)
        self.tabsWdg.setTabPosition(QTabWidget.North)
        self.tabsWdg.setUsesScrollButtons(True)
        self.tabsWdg.setTabsClosable(False)
        self.tabsWdg.setMovable(False)

        self.verticalLayout.addWidget(self.tabsWdg)

        self.assetPathHBox = QHBoxLayout()
        self.assetPathHBox.setSpacing(10)
        self.assetPathHBox.setObjectName(u"assetPathHBox")
        self.assetPathLine = QLineEdit(rs_win)
        self.assetPathLine.setObjectName(u"assetPathLine")
        self.assetPathLine.setMaximumSize(QSize(16777215, 25))
        self.assetPathLine.setStyleSheet(u"QLineEdit{color:grey;\n"
"background-color:rgb(60,60,60);}\n"
"")
        self.assetPathLine.setFrame(False)
        self.assetPathLine.setReadOnly(True)

        self.assetPathHBox.addWidget(self.assetPathLine)

        self.openPathBtn = QPushButton(rs_win)
        self.openPathBtn.setObjectName(u"openPathBtn")
        self.openPathBtn.setMaximumSize(QSize(50, 25))
        self.openPathBtn.setFont(font1)
        self.openPathBtn.setStyleSheet(u"QPushButton{color:grey;\n"
"background-color:rgb(60,60,60);}\n"
"")
        self.openPathBtn.setIconSize(QSize(30, 30))
        self.openPathBtn.setFlat(True)

        self.assetPathHBox.addWidget(self.openPathBtn)

        self.assetPathHBox.setStretch(0, 1)

        self.verticalLayout.addLayout(self.assetPathHBox)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(rs_win)

        self.tabsWdg.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(rs_win)
    # setupUi

    def retranslateUi(self, rs_win):
        rs_win.setWindowTitle(QCoreApplication.translate("rs_win", u"Rig Build", None))
        self.idLb.setText("")
        self.assetNameLabel.setText(QCoreApplication.translate("rs_win", u"NAME:", None))
        self.assetNameDate.setText("")
        self.createdLabel.setText(QCoreApplication.translate("rs_win", u"DATE:", None))
        self.createdDate.setText("")
        self.modLabel.setText(QCoreApplication.translate("rs_win", u"AUTHOR:", None))
        self.modDate.setText("")
        self.setBtn.setText("")
        self.rigTypeDate.setText("")
        self.newRigBtn.setText("")
        self.stratInfoLb.setText("")
        self.seartch_lb.setText(QCoreApplication.translate("rs_win", u"Search", None))
        self.searchLine.setText("")
        self.newAssetBtn.setText(QCoreApplication.translate("rs_win", u"+ A S S E T +", None))
        self.rootBtn.setText(QCoreApplication.translate("rs_win", u">>", None))
        self.openPathBtn.setText("")
    # retranslateUi

