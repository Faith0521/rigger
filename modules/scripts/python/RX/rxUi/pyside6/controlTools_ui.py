# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controlToolsUI.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_ctrl_win(object):
    def setupUi(self, ctrl_win):
        if not ctrl_win.objectName():
            ctrl_win.setObjectName(u"ctrl_win")
        ctrl_win.resize(342, 759)
        ctrl_win.setMinimumSize(QSize(342, 715))
        self.gridLayout = QGridLayout(ctrl_win)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(ctrl_win)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 45))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setStyleSheet(u"background-color:rgb(42,42,42);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 2, 8, 2)
        self.controlTools_label = QLabel(self.frame)
        self.controlTools_label.setObjectName(u"controlTools_label")
        self.controlTools_label.setMinimumSize(QSize(0, 36))
        font = QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.controlTools_label.setFont(font)
        self.controlTools_label.setStyleSheet(u"color:lightGrey")
        self.controlTools_label.setIndent(10)

        self.horizontalLayout_3.addWidget(self.controlTools_label)

        self.controlTools_help = QPushButton(self.frame)
        self.controlTools_help.setObjectName(u"controlTools_help")
        self.controlTools_help.setMaximumSize(QSize(30, 16777215))
        icon = QIcon()
        icon.addFile(u"rigBuild/icons/helpMeduim.png", QSize(), QIcon.Normal, QIcon.Off)
        self.controlTools_help.setIcon(icon)
        self.controlTools_help.setFlat(True)

        self.horizontalLayout_3.addWidget(self.controlTools_help)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.create_gb = QGroupBox(ctrl_win)
        self.create_gb.setObjectName(u"create_gb")
        self.create_gb.setMinimumSize(QSize(0, 100))
        self.create_gb.setMaximumSize(QSize(16777215, 80))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setItalic(True)
        self.create_gb.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.create_gb)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.snap_lb = QLabel(self.create_gb)
        self.snap_lb.setObjectName(u"snap_lb")
        self.snap_lb.setMinimumSize(QSize(0, 19))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.snap_lb.setFont(font2)

        self.gridLayout_2.addWidget(self.snap_lb, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.snap_line = QLineEdit(self.create_gb)
        self.snap_line.setObjectName(u"snap_line")
        self.snap_line.setFont(font2)

        self.horizontalLayout_5.addWidget(self.snap_line)

        self.snap_btn = QPushButton(self.create_gb)
        self.snap_btn.setObjectName(u"snap_btn")
        self.snap_btn.setMinimumSize(QSize(60, 0))
        self.snap_btn.setMaximumSize(QSize(16777215, 16777215))
        self.snap_btn.setFont(font2)
        self.snap_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_5.addWidget(self.snap_btn)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 2)

        self.name_lb = QLabel(self.create_gb)
        self.name_lb.setObjectName(u"name_lb")
        self.name_lb.setFont(font2)

        self.gridLayout_2.addWidget(self.name_lb, 0, 0, 1, 1)

        self.nameLine = QLineEdit(self.create_gb)
        self.nameLine.setObjectName(u"nameLine")
        self.nameLine.setFont(font2)

        self.gridLayout_2.addWidget(self.nameLine, 0, 1, 1, 2)


        self.gridLayout.addWidget(self.create_gb, 1, 0, 1, 1)

        self.shape_gb = QGroupBox(ctrl_win)
        self.shape_gb.setObjectName(u"shape_gb")
        self.shape_gb.setMinimumSize(QSize(292, 345))
        self.shape_gb.setFont(font1)
        self.shape_gb.setFlat(False)
        self.shape_gb.setCheckable(False)
        self.gridLayout_6 = QGridLayout(self.shape_gb)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ctrl_listWidget = QListWidget(self.shape_gb)
        self.ctrl_listWidget.setObjectName(u"ctrl_listWidget")
        self.ctrl_listWidget.setBaseSize(QSize(272, 0))
        self.ctrl_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ctrl_listWidget.setIconSize(QSize(70, 70))
        self.ctrl_listWidget.setMovement(QListView.Static)
        self.ctrl_listWidget.setResizeMode(QListView.Adjust)
        self.ctrl_listWidget.setGridSize(QSize(80, 80))
        self.ctrl_listWidget.setViewMode(QListView.IconMode)
        self.ctrl_listWidget.setUniformItemSizes(False)

        self.gridLayout_6.addWidget(self.ctrl_listWidget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.shape_gb, 2, 0, 1, 1)

        self.modify_gb = QGroupBox(ctrl_win)
        self.modify_gb.setObjectName(u"modify_gb")
        self.modify_gb.setMinimumSize(QSize(0, 210))
        self.modify_gb.setMaximumSize(QSize(16777215, 190))
        self.modify_gb.setFont(font1)
        self.gridLayout_3 = QGridLayout(self.modify_gb)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.green_color_btn = QPushButton(self.modify_gb)
        self.green_color_btn.setObjectName(u"green_color_btn")
        palette = QPalette()
        brush = QBrush(QColor(0, 255, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.green_color_btn.setPalette(palette)
        font3 = QFont()
        font3.setBold(True)
        font3.setItalic(False)
        self.green_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.green_color_btn)

        self.violet_color_btn = QPushButton(self.modify_gb)
        self.violet_color_btn.setObjectName(u"violet_color_btn")
        palette1 = QPalette()
        brush2 = QBrush(QColor(255, 0, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.violet_color_btn.setPalette(palette1)
        self.violet_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.violet_color_btn)

        self.red_color_btn = QPushButton(self.modify_gb)
        self.red_color_btn.setObjectName(u"red_color_btn")
        palette2 = QPalette()
        brush3 = QBrush(QColor(255, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.red_color_btn.setPalette(palette2)
        self.red_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.red_color_btn)

        self.yellow_color_btn = QPushButton(self.modify_gb)
        self.yellow_color_btn.setObjectName(u"yellow_color_btn")
        palette3 = QPalette()
        brush4 = QBrush(QColor(255, 255, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.yellow_color_btn.setPalette(palette3)
        self.yellow_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.yellow_color_btn)

        self.blue_color_btn = QPushButton(self.modify_gb)
        self.blue_color_btn.setObjectName(u"blue_color_btn")
        palette4 = QPalette()
        brush5 = QBrush(QColor(0, 0, 255, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.blue_color_btn.setPalette(palette4)
        self.blue_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.blue_color_btn)

        self.cobalt_color_btn = QPushButton(self.modify_gb)
        self.cobalt_color_btn.setObjectName(u"cobalt_color_btn")
        palette5 = QPalette()
        brush6 = QBrush(QColor(66, 110, 212, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.cobalt_color_btn.setPalette(palette5)
        self.cobalt_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.cobalt_color_btn)

        self.turquoise_color_btn = QPushButton(self.modify_gb)
        self.turquoise_color_btn.setObjectName(u"turquoise_color_btn")
        palette6 = QPalette()
        brush7 = QBrush(QColor(85, 170, 127, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette6.setBrush(QPalette.Active, QPalette.ButtonText, brush7)
        palette6.setBrush(QPalette.Inactive, QPalette.ButtonText, brush7)
        palette6.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.turquoise_color_btn.setPalette(palette6)
        self.turquoise_color_btn.setFont(font3)

        self.horizontalLayout.addWidget(self.turquoise_color_btn)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.seprate_line_3 = QFrame(self.modify_gb)
        self.seprate_line_3.setObjectName(u"seprate_line_3")
        self.seprate_line_3.setFrameShape(QFrame.HLine)
        self.seprate_line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.seprate_line_3, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scale_add_btn = QPushButton(self.modify_gb)
        self.scale_add_btn.setObjectName(u"scale_add_btn")
        self.scale_add_btn.setMinimumSize(QSize(60, 23))
        self.scale_add_btn.setMaximumSize(QSize(16777215, 16777215))
        self.scale_add_btn.setFont(font2)
        self.scale_add_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_2.addWidget(self.scale_add_btn)

        self.scale_reduce_btn = QPushButton(self.modify_gb)
        self.scale_reduce_btn.setObjectName(u"scale_reduce_btn")
        self.scale_reduce_btn.setMinimumSize(QSize(60, 23))
        self.scale_reduce_btn.setMaximumSize(QSize(16777215, 16777215))
        self.scale_reduce_btn.setFont(font2)
        self.scale_reduce_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_2.addWidget(self.scale_reduce_btn)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.rox_btn = QPushButton(self.modify_gb)
        self.rox_btn.setObjectName(u"rox_btn")
        self.rox_btn.setMinimumSize(QSize(60, 23))
        self.rox_btn.setMaximumSize(QSize(16777215, 16777215))
        self.rox_btn.setFont(font2)
        self.rox_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_10.addWidget(self.rox_btn)

        self.roy_btn = QPushButton(self.modify_gb)
        self.roy_btn.setObjectName(u"roy_btn")
        self.roy_btn.setMinimumSize(QSize(60, 23))
        self.roy_btn.setMaximumSize(QSize(16777215, 16777215))
        self.roy_btn.setFont(font2)
        self.roy_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_10.addWidget(self.roy_btn)

        self.roz_btn = QPushButton(self.modify_gb)
        self.roz_btn.setObjectName(u"roz_btn")
        self.roz_btn.setMinimumSize(QSize(60, 23))
        self.roz_btn.setMaximumSize(QSize(16777215, 16777215))
        self.roz_btn.setFont(font2)
        self.roz_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_10.addWidget(self.roz_btn)


        self.gridLayout_3.addLayout(self.horizontalLayout_10, 3, 0, 1, 1)

        self.seprate_line = QFrame(self.modify_gb)
        self.seprate_line.setObjectName(u"seprate_line")
        self.seprate_line.setFrameShape(QFrame.HLine)
        self.seprate_line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.seprate_line, 4, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.mirrorControl_btn = QPushButton(self.modify_gb)
        self.mirrorControl_btn.setObjectName(u"mirrorControl_btn")
        self.mirrorControl_btn.setMinimumSize(QSize(60, 23))
        self.mirrorControl_btn.setMaximumSize(QSize(16777215, 16777215))
        self.mirrorControl_btn.setFont(font2)
        self.mirrorControl_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_8.addWidget(self.mirrorControl_btn)

        self.mirrorShapel_btn = QPushButton(self.modify_gb)
        self.mirrorShapel_btn.setObjectName(u"mirrorShapel_btn")
        self.mirrorShapel_btn.setMinimumSize(QSize(60, 23))
        self.mirrorShapel_btn.setMaximumSize(QSize(16777215, 16777215))
        self.mirrorShapel_btn.setFont(font2)
        self.mirrorShapel_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_8.addWidget(self.mirrorShapel_btn)


        self.gridLayout_3.addLayout(self.horizontalLayout_8, 5, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.exportShape_btn = QPushButton(self.modify_gb)
        self.exportShape_btn.setObjectName(u"exportShape_btn")
        self.exportShape_btn.setMinimumSize(QSize(60, 23))
        self.exportShape_btn.setMaximumSize(QSize(16777215, 16777215))
        self.exportShape_btn.setFont(font2)
        self.exportShape_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_6.addWidget(self.exportShape_btn)

        self.importShape_btn = QPushButton(self.modify_gb)
        self.importShape_btn.setObjectName(u"importShape_btn")
        self.importShape_btn.setMinimumSize(QSize(60, 23))
        self.importShape_btn.setMaximumSize(QSize(16777215, 16777215))
        self.importShape_btn.setFont(font2)
        self.importShape_btn.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout_6.addWidget(self.importShape_btn)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)


        self.gridLayout.addWidget(self.modify_gb, 3, 0, 1, 1)


        self.retranslateUi(ctrl_win)

        QMetaObject.connectSlotsByName(ctrl_win)
    # setupUi

    def retranslateUi(self, ctrl_win):
        ctrl_win.setWindowTitle(QCoreApplication.translate("ctrl_win", u"ControlTools", None))
        self.controlTools_label.setText(QCoreApplication.translate("ctrl_win", u"Control Tools", None))
        self.create_gb.setTitle(QCoreApplication.translate("ctrl_win", u"Name", None))
        self.snap_lb.setText(QCoreApplication.translate("ctrl_win", u"Snap To", None))
        self.snap_btn.setText(QCoreApplication.translate("ctrl_win", u"   Get   ", None))
        self.name_lb.setText(QCoreApplication.translate("ctrl_win", u"Name", None))
        self.nameLine.setText("")
        self.shape_gb.setTitle(QCoreApplication.translate("ctrl_win", u"Create", None))
        self.modify_gb.setTitle(QCoreApplication.translate("ctrl_win", u"Modify", None))
        self.green_color_btn.setText(QCoreApplication.translate("ctrl_win", u"G", None))
        self.violet_color_btn.setText(QCoreApplication.translate("ctrl_win", u"V", None))
        self.red_color_btn.setText(QCoreApplication.translate("ctrl_win", u"R", None))
        self.yellow_color_btn.setText(QCoreApplication.translate("ctrl_win", u"Y", None))
        self.blue_color_btn.setText(QCoreApplication.translate("ctrl_win", u"B", None))
        self.cobalt_color_btn.setText(QCoreApplication.translate("ctrl_win", u"C", None))
        self.turquoise_color_btn.setText(QCoreApplication.translate("ctrl_win", u"T", None))
        self.scale_add_btn.setText(QCoreApplication.translate("ctrl_win", u"Scale +", None))
        self.scale_reduce_btn.setText(QCoreApplication.translate("ctrl_win", u"Scale -", None))
        self.rox_btn.setText(QCoreApplication.translate("ctrl_win", u"Ro-X", None))
        self.roy_btn.setText(QCoreApplication.translate("ctrl_win", u"Ro-Y", None))
        self.roz_btn.setText(QCoreApplication.translate("ctrl_win", u"Ro-Z", None))
        self.mirrorControl_btn.setText(QCoreApplication.translate("ctrl_win", u"Mirror Control", None))
        self.mirrorShapel_btn.setText(QCoreApplication.translate("ctrl_win", u"Mirror Shape", None))
        self.exportShape_btn.setText(QCoreApplication.translate("ctrl_win", u"Export Shape", None))
        self.importShape_btn.setText(QCoreApplication.translate("ctrl_win", u"Import Shape", None))
    # retranslateUi

