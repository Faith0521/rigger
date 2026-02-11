# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newAssetUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_newAssetUI(object):
    def setupUi(self, newAssetUI):
        if not newAssetUI.objectName():
            newAssetUI.setObjectName(u"newAssetUI")
        newAssetUI.resize(310, 269)
        newAssetUI.setMinimumSize(QSize(310, 269))
        newAssetUI.setMaximumSize(QSize(310, 269))
        self.gridLayout = QGridLayout(newAssetUI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(newAssetUI)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 40))
        self.label.setMaximumSize(QSize(16777215, 40))
        self.label.setSizeIncrement(QSize(0, 50))
        font = QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color:rgb(35,35,35)")
        self.label.setMargin(3)
        self.label.setIndent(5)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.cancelBtn = QPushButton(newAssetUI)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.gridLayout.addWidget(self.cancelBtn, 3, 1, 1, 1)

        self.groupBox = QGroupBox(newAssetUI)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.animChx = QCheckBox(self.groupBox)
        self.animChx.setObjectName(u"animChx")
        self.animChx.setChecked(True)

        self.verticalLayout.addWidget(self.animChx)

        self.gameChx = QCheckBox(self.groupBox)
        self.gameChx.setObjectName(u"gameChx")
        self.gameChx.setChecked(False)

        self.verticalLayout.addWidget(self.gameChx)

        self.mocapChx = QCheckBox(self.groupBox)
        self.mocapChx.setObjectName(u"mocapChx")

        self.verticalLayout.addWidget(self.mocapChx)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.otherChx = QCheckBox(self.groupBox)
        self.otherChx.setObjectName(u"otherChx")

        self.horizontalLayout.addWidget(self.otherChx)

        self.otherLine = QLineEdit(self.groupBox)
        self.otherLine.setObjectName(u"otherLine")
        self.otherLine.setEnabled(False)

        self.horizontalLayout.addWidget(self.otherLine)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)

        self.createBtn = QPushButton(newAssetUI)
        self.createBtn.setObjectName(u"createBtn")

        self.gridLayout.addWidget(self.createBtn, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(newAssetUI)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.nameLine = QLineEdit(newAssetUI)
        self.nameLine.setObjectName(u"nameLine")

        self.horizontalLayout_2.addWidget(self.nameLine)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)


        self.retranslateUi(newAssetUI)
        self.otherChx.toggled.connect(self.otherLine.setDisabled)
        self.otherChx.toggled.connect(self.otherLine.setEnabled)

        QMetaObject.connectSlotsByName(newAssetUI)
    # setupUi

    def retranslateUi(self, newAssetUI):
        newAssetUI.setWindowTitle(QCoreApplication.translate("newAssetUI", u"New Asset", None))
        self.label.setText(QCoreApplication.translate("newAssetUI", u"Create New Asset", None))
        self.cancelBtn.setText(QCoreApplication.translate("newAssetUI", u"Cancel", None))
        self.groupBox.setTitle(QCoreApplication.translate("newAssetUI", u"Rig Types", None))
        self.animChx.setText(QCoreApplication.translate("newAssetUI", u"Rig", None))
        self.gameChx.setText(QCoreApplication.translate("newAssetUI", u"Game Rig", None))
        self.mocapChx.setText(QCoreApplication.translate("newAssetUI", u"Mocap Rig", None))
        self.otherChx.setText(QCoreApplication.translate("newAssetUI", u"Other", None))
        self.createBtn.setText(QCoreApplication.translate("newAssetUI", u"Create", None))
        self.label_2.setText(QCoreApplication.translate("newAssetUI", u"Asset Name", None))
    # retranslateUi

