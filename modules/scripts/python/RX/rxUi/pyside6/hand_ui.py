# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'handUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_handUI(object):
    def setupUi(self, handUI):
        if not handUI.objectName():
            handUI.setObjectName(u"handUI")
        handUI.resize(273, 228)
        handUI.setMinimumSize(QSize(0, 228))
        handUI.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(handUI)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(6)
        self.frame = QFrame(handUI)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setStyleSheet(u"background-color:rgb(42,42,42);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 2, 8, 2)
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        font = QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(u"color:lightGrey")
        self.label_7.setIndent(10)

        self.horizontalLayout_3.addWidget(self.label_7)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 2)

        self.groupBox_2 = QGroupBox(handUI)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buildBtn = QPushButton(self.groupBox_2)
        self.buildBtn.setObjectName(u"buildBtn")

        self.verticalLayout.addWidget(self.buildBtn)

        self.rebuildBtn = QPushButton(self.groupBox_2)
        self.rebuildBtn.setObjectName(u"rebuildBtn")

        self.verticalLayout.addWidget(self.rebuildBtn)

        self.mirrorBtn = QPushButton(self.groupBox_2)
        self.mirrorBtn.setObjectName(u"mirrorBtn")

        self.verticalLayout.addWidget(self.mirrorBtn)

        self.exportBtn = QPushButton(self.groupBox_2)
        self.exportBtn.setObjectName(u"exportBtn")

        self.verticalLayout.addWidget(self.exportBtn)


        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 8, 0, 1, 1)


        self.retranslateUi(handUI)

        QMetaObject.connectSlotsByName(handUI)
    # setupUi

    def retranslateUi(self, handUI):
        handUI.setWindowTitle(QCoreApplication.translate("handUI", u"Hand Poses", None))
        self.label_7.setText(QCoreApplication.translate("handUI", u"Hand Pose Set", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("handUI", u"Set Pose", None))
        self.buildBtn.setText(QCoreApplication.translate("handUI", u"Build Pose", None))
        self.rebuildBtn.setText(QCoreApplication.translate("handUI", u"Rebuild Pose", None))
        self.mirrorBtn.setText(QCoreApplication.translate("handUI", u"Mirror / Copy Poses", None))
        self.exportBtn.setText(QCoreApplication.translate("handUI", u"Export Poses", None))
    # retranslateUi

