# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nurbs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(654, 959)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(5, 5))
        MainWindow.setStyleSheet(u"")
        self.actionExport_Weights = QAction(MainWindow)
        self.actionExport_Weights.setObjectName(u"actionExport_Weights")
        self.actionImport_Weights = QAction(MainWindow)
        self.actionImport_Weights.setObjectName(u"actionImport_Weights")
        self.actionExport_Settings = QAction(MainWindow)
        self.actionExport_Settings.setObjectName(u"actionExport_Settings")
        self.actionImport_Settings = QAction(MainWindow)
        self.actionImport_Settings.setObjectName(u"actionImport_Settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"border: 0px;")
        self.horizontalLayout_12 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.custom_rb = QRadioButton(self.groupBox_4)
        self.custom_rb.setObjectName(u"custom_rb")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.custom_rb.sizePolicy().hasHeightForWidth())
        self.custom_rb.setSizePolicy(sizePolicy2)
        self.custom_rb.setChecked(True)

        self.horizontalLayout_12.addWidget(self.custom_rb)

        self.snake_rb = QRadioButton(self.groupBox_4)
        self.snake_rb.setObjectName(u"snake_rb")
        sizePolicy2.setHeightForWidth(self.snake_rb.sizePolicy().hasHeightForWidth())
        self.snake_rb.setSizePolicy(sizePolicy2)

        self.horizontalLayout_12.addWidget(self.snake_rb)

        self.mirror_cb = QCheckBox(self.groupBox_4)
        self.mirror_cb.setObjectName(u"mirror_cb")

        self.horizontalLayout_12.addWidget(self.mirror_cb)


        self.horizontalLayout_2.addWidget(self.groupBox_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.setting_wdgt = QWidget()
        self.setting_wdgt.setObjectName(u"setting_wdgt")
        self.verticalLayout_3 = QVBoxLayout(self.setting_wdgt)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(self.setting_wdgt)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(5, 5))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 620, 805))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(5, 0))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.custom_widget = QWidget(self.scrollAreaWidgetContents)
        self.custom_widget.setObjectName(u"custom_widget")
        sizePolicy.setHeightForWidth(self.custom_widget.sizePolicy().hasHeightForWidth())
        self.custom_widget.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.custom_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_20 = QLabel(self.custom_widget)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_5.addWidget(self.label_20)

        self.rigName_le = QLineEdit(self.custom_widget)
        self.rigName_le.setObjectName(u"rigName_le")

        self.horizontalLayout_5.addWidget(self.rigName_le)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.label_17 = QLabel(self.custom_widget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet(u"QLabel {\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius:5px;\n"
"}")
        self.label_17.setTextFormat(Qt.AutoText)

        self.verticalLayout_4.addWidget(self.label_17)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.custom_widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.jntNum_spin_2 = QSpinBox(self.custom_widget)
        self.jntNum_spin_2.setObjectName(u"jntNum_spin_2")
        self.jntNum_spin_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.jntNum_spin_2.setMinimum(1)
        self.jntNum_spin_2.setMaximum(999999)
        self.jntNum_spin_2.setValue(5)

        self.horizontalLayout.addWidget(self.jntNum_spin_2)

        self.label_4 = QLabel(self.custom_widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.sec_axis_cb = QComboBox(self.custom_widget)
        self.sec_axis_cb.addItem("")
        self.sec_axis_cb.addItem("")
        self.sec_axis_cb.setObjectName(u"sec_axis_cb")

        self.horizontalLayout.addWidget(self.sec_axis_cb)

        self.label_6 = QLabel(self.custom_widget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.type_cb = QComboBox(self.custom_widget)
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.addItem("")
        self.type_cb.setObjectName(u"type_cb")

        self.horizontalLayout.addWidget(self.type_cb)

        self.world_cb = QCheckBox(self.custom_widget)
        self.world_cb.setObjectName(u"world_cb")

        self.horizontalLayout.addWidget(self.world_cb)

        self.create_jnt_btn = QPushButton(self.custom_widget)
        self.create_jnt_btn.setObjectName(u"create_jnt_btn")

        self.horizontalLayout.addWidget(self.create_jnt_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line = QFrame(self.custom_widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.label_5 = QLabel(self.custom_widget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"QLabel {\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius:5px;\n"
"}")

        self.verticalLayout_4.addWidget(self.label_5)

        self.line_4 = QFrame(self.custom_widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_7 = QLabel(self.custom_widget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_10.addWidget(self.label_7)

        self.custom_spin = QDoubleSpinBox(self.custom_widget)
        self.custom_spin.setObjectName(u"custom_spin")
        self.custom_spin.setMaximum(9999.000000000000000)
        self.custom_spin.setValue(1.000000000000000)

        self.horizontalLayout_10.addWidget(self.custom_spin)

        self.groupBox_3 = QGroupBox(self.custom_widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setStyleSheet(u"border: 0px;")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.ikfkType = QRadioButton(self.groupBox_3)
        self.ikfkType.setObjectName(u"ikfkType")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ikfkType.sizePolicy().hasHeightForWidth())
        self.ikfkType.setSizePolicy(sizePolicy4)
        self.ikfkType.setChecked(True)

        self.horizontalLayout_11.addWidget(self.ikfkType)

        self.ikType = QRadioButton(self.groupBox_3)
        self.ikType.setObjectName(u"ikType")
        sizePolicy4.setHeightForWidth(self.ikType.sizePolicy().hasHeightForWidth())
        self.ikType.setSizePolicy(sizePolicy4)

        self.horizontalLayout_11.addWidget(self.ikType)

        self.fkType = QRadioButton(self.groupBox_3)
        self.fkType.setObjectName(u"fkType")
        sizePolicy4.setHeightForWidth(self.fkType.sizePolicy().hasHeightForWidth())
        self.fkType.setSizePolicy(sizePolicy4)

        self.horizontalLayout_11.addWidget(self.fkType)

        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy5)

        self.horizontalLayout_11.addWidget(self.label_13)

        self.jntNum_spin = QSpinBox(self.groupBox_3)
        self.jntNum_spin.setObjectName(u"jntNum_spin")
        sizePolicy1.setHeightForWidth(self.jntNum_spin.sizePolicy().hasHeightForWidth())
        self.jntNum_spin.setSizePolicy(sizePolicy1)
        self.jntNum_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.jntNum_spin.setMinimum(4)
        self.jntNum_spin.setMaximum(99999)
        self.jntNum_spin.setValue(9)

        self.horizontalLayout_11.addWidget(self.jntNum_spin)


        self.horizontalLayout_10.addWidget(self.groupBox_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)


        self.verticalLayout_2.addWidget(self.custom_widget)

        self.upper_widget = QWidget(self.scrollAreaWidgetContents)
        self.upper_widget.setObjectName(u"upper_widget")
        self.verticalLayout_6 = QVBoxLayout(self.upper_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 0, 5, 5)
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, 5, -1, 5)
        self.addUpperCb = QCheckBox(self.upper_widget)
        self.addUpperCb.setObjectName(u"addUpperCb")
        sizePolicy4.setHeightForWidth(self.addUpperCb.sizePolicy().hasHeightForWidth())
        self.addUpperCb.setSizePolicy(sizePolicy4)
        self.addUpperCb.setChecked(True)

        self.horizontalLayout_19.addWidget(self.addUpperCb)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_2)

        self.label_16 = QLabel(self.upper_widget)
        self.label_16.setObjectName(u"label_16")
        sizePolicy4.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy4)

        self.horizontalLayout_19.addWidget(self.label_16)

        self.upperNum_spin = QSpinBox(self.upper_widget)
        self.upperNum_spin.setObjectName(u"upperNum_spin")
        sizePolicy4.setHeightForWidth(self.upperNum_spin.sizePolicy().hasHeightForWidth())
        self.upperNum_spin.setSizePolicy(sizePolicy4)
        self.upperNum_spin.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.upperNum_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.upperNum_spin.setMinimum(2)
        self.upperNum_spin.setMaximum(999999)
        self.upperNum_spin.setValue(3)

        self.horizontalLayout_19.addWidget(self.upperNum_spin)

        self.stretch_cb = QCheckBox(self.upper_widget)
        self.stretch_cb.setObjectName(u"stretch_cb")
        sizePolicy4.setHeightForWidth(self.stretch_cb.sizePolicy().hasHeightForWidth())
        self.stretch_cb.setSizePolicy(sizePolicy4)

        self.horizontalLayout_19.addWidget(self.stretch_cb)

        self.reverse_cb = QCheckBox(self.upper_widget)
        self.reverse_cb.setObjectName(u"reverse_cb")
        sizePolicy4.setHeightForWidth(self.reverse_cb.sizePolicy().hasHeightForWidth())
        self.reverse_cb.setSizePolicy(sizePolicy4)

        self.horizontalLayout_19.addWidget(self.reverse_cb)

        self.upperType_cb = QComboBox(self.upper_widget)
        self.upperType_cb.addItem("")
        self.upperType_cb.addItem("")
        self.upperType_cb.addItem("")
        self.upperType_cb.setObjectName(u"upperType_cb")

        self.horizontalLayout_19.addWidget(self.upperType_cb)


        self.verticalLayout_6.addLayout(self.horizontalLayout_19)

        self.line_5 = QFrame(self.upper_widget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.upper_widget)

        self.snake_widget = QWidget(self.scrollAreaWidgetContents)
        self.snake_widget.setObjectName(u"snake_widget")
        self.verticalLayout_10 = QVBoxLayout(self.snake_widget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.sinCos_cb = QCheckBox(self.snake_widget)
        self.sinCos_cb.setObjectName(u"sinCos_cb")
        self.sinCos_cb.setChecked(True)

        self.verticalLayout_10.addWidget(self.sinCos_cb)

        self.rotate_cb = QCheckBox(self.snake_widget)
        self.rotate_cb.setObjectName(u"rotate_cb")
        self.rotate_cb.setChecked(True)

        self.verticalLayout_10.addWidget(self.rotate_cb)

        self.curly_cb = QCheckBox(self.snake_widget)
        self.curly_cb.setObjectName(u"curly_cb")
        self.curly_cb.setChecked(True)

        self.verticalLayout_10.addWidget(self.curly_cb)

        self.drum_cb = QCheckBox(self.snake_widget)
        self.drum_cb.setObjectName(u"drum_cb")
        self.drum_cb.setChecked(False)

        self.verticalLayout_10.addWidget(self.drum_cb)

        self.slider_cb = QCheckBox(self.snake_widget)
        self.slider_cb.setObjectName(u"slider_cb")
        sizePolicy2.setHeightForWidth(self.slider_cb.sizePolicy().hasHeightForWidth())
        self.slider_cb.setSizePolicy(sizePolicy2)
        self.slider_cb.setChecked(True)

        self.verticalLayout_10.addWidget(self.slider_cb)


        self.verticalLayout_2.addWidget(self.snake_widget)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.rig_btn = QPushButton(self.scrollAreaWidgetContents)
        self.rig_btn.setObjectName(u"rig_btn")
        font1 = QFont()
        font1.setPointSize(13)
        self.rig_btn.setFont(font1)

        self.horizontalLayout_6.addWidget(self.rig_btn)

        self.delete_btn = QPushButton(self.scrollAreaWidgetContents)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setFont(font1)

        self.horizontalLayout_6.addWidget(self.delete_btn)

        self.motion_btn = QPushButton(self.scrollAreaWidgetContents)
        self.motion_btn.setObjectName(u"motion_btn")
        self.motion_btn.setFont(font1)

        self.horizontalLayout_6.addWidget(self.motion_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.setting_wdgt, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_11 = QVBoxLayout(self.tab)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_21 = QLabel(self.tab)
        self.label_21.setObjectName(u"label_21")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy6)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet(u"QLabel {\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius:5px;\n"
"}")
        self.label_21.setTextFormat(Qt.AutoText)

        self.verticalLayout_5.addWidget(self.label_21)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_17.addWidget(self.label)

        self.prefix_le = QLineEdit(self.tab)
        self.prefix_le.setObjectName(u"prefix_le")

        self.horizontalLayout_17.addWidget(self.prefix_le)


        self.verticalLayout_5.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.attrCtrl_btn = QPushButton(self.tab)
        self.attrCtrl_btn.setObjectName(u"attrCtrl_btn")

        self.horizontalLayout_7.addWidget(self.attrCtrl_btn)

        self.attrCtrl_le = QLineEdit(self.tab)
        self.attrCtrl_le.setObjectName(u"attrCtrl_le")

        self.horizontalLayout_7.addWidget(self.attrCtrl_le)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.obj_btn = QPushButton(self.tab)
        self.obj_btn.setObjectName(u"obj_btn")

        self.horizontalLayout_8.addWidget(self.obj_btn)

        self.obj_le = QLineEdit(self.tab)
        self.obj_le.setObjectName(u"obj_le")

        self.horizontalLayout_8.addWidget(self.obj_le)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.setup_btn = QPushButton(self.tab)
        self.setup_btn.setObjectName(u"setup_btn")

        self.verticalLayout_5.addWidget(self.setup_btn)


        self.verticalLayout_11.addLayout(self.verticalLayout_5)

        self.line_6 = QFrame(self.tab)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_6)

        self.line_3 = QFrame(self.tab)
        self.line_3.setObjectName(u"line_3")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy7)
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_3)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 654, 26))
        self.menubar.setDefaultUp(False)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.upperType_cb.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExport_Weights.setText(QCoreApplication.translate("MainWindow", u"Export Weights", None))
        self.actionImport_Weights.setText(QCoreApplication.translate("MainWindow", u"Import Weights", None))
        self.actionExport_Settings.setText(QCoreApplication.translate("MainWindow", u"Export Settings", None))
        self.actionImport_Settings.setText(QCoreApplication.translate("MainWindow", u"Import Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7ed1\u5b9a\u7c7b\u578b", None))
        self.groupBox_4.setTitle("")
        self.custom_rb.setText(QCoreApplication.translate("MainWindow", u"\u666e\u901a", None))
        self.snake_rb.setText(QCoreApplication.translate("MainWindow", u"\u86c7\u7c7b", None))
        self.mirror_cb.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u7ed1\u5b9a\u524d\u7f00\u540d", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Step1: \u751f\u6210\u9aa8\u9abc,\u786e\u5b9a\u8f74\u5411", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u9aa8\u9abc\u6570\u91cf", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7b2c\u4e8c\u8f74\u5411", None))
        self.sec_axis_cb.setItemText(0, QCoreApplication.translate("MainWindow", u"y", None))
        self.sec_axis_cb.setItemText(1, QCoreApplication.translate("MainWindow", u"z", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8f74\u5411\u7c7b\u578b", None))
        self.type_cb.setItemText(0, QCoreApplication.translate("MainWindow", u"+x", None))
        self.type_cb.setItemText(1, QCoreApplication.translate("MainWindow", u"-x", None))
        self.type_cb.setItemText(2, QCoreApplication.translate("MainWindow", u"+y", None))
        self.type_cb.setItemText(3, QCoreApplication.translate("MainWindow", u"-y", None))
        self.type_cb.setItemText(4, QCoreApplication.translate("MainWindow", u"+z", None))
        self.type_cb.setItemText(5, QCoreApplication.translate("MainWindow", u"-z", None))
        self.type_cb.setItemText(6, QCoreApplication.translate("MainWindow", u"\u9996\u9aa8\u9abc", None))
        self.type_cb.setItemText(7, QCoreApplication.translate("MainWindow", u"\u9996\u5c3e\u9aa8\u9abc", None))

        self.world_cb.setText(QCoreApplication.translate("MainWindow", u"\u4e16\u754c\u5750\u6807", None))
        self.create_jnt_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Step2: \u751f\u6210\u8bbe\u7f6e", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u63a7\u5236\u5668\u5927\u5c0f", None))
        self.groupBox_3.setTitle("")
        self.ikfkType.setText(QCoreApplication.translate("MainWindow", u"IKFK", None))
        self.ikType.setText(QCoreApplication.translate("MainWindow", u"IK", None))
        self.fkType.setText(QCoreApplication.translate("MainWindow", u"FK", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u9aa8\u9abc\u6570\u91cf", None))
        self.addUpperCb.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u4e0a\u5c42\u63a7\u5236", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u63a7\u5236\u5668\u6570\u91cf", None))
        self.stretch_cb.setText(QCoreApplication.translate("MainWindow", u"\u62c9\u4f38", None))
        self.reverse_cb.setText(QCoreApplication.translate("MainWindow", u"\u53cd\u8f6c", None))
        self.upperType_cb.setItemText(0, QCoreApplication.translate("MainWindow", u"IKFK", None))
        self.upperType_cb.setItemText(1, QCoreApplication.translate("MainWindow", u"IK", None))
        self.upperType_cb.setItemText(2, QCoreApplication.translate("MainWindow", u"FK", None))

        self.sinCos_cb.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa Sin/Cos \u504f\u79fb", None))
        self.rotate_cb.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u6574\u4f53\u65cb\u8f6c\u63a7\u5236", None))
        self.curly_cb.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u6e10\u53d8\u65cb\u8f6c\u6548\u679c", None))
        self.drum_cb.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u7f29\u653eSin/Cos\u6548\u679c", None))
        self.slider_cb.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u6ed1\u52a8\u63a7\u5236", None))
        self.rig_btn.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.motion_btn.setText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u52a8\u753b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setting_wdgt), QCoreApplication.translate("MainWindow", u"\u57fa\u7840\u8bbe\u7f6e", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Dynamics", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u524d\u7f00\u540d", None))
        self.attrCtrl_btn.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u5c5e\u6027\u63a7\u5236\u5668", None))
        self.obj_btn.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u7269\u4f53", None))
        self.setup_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u6a21\u62df\u52a8\u529b\u5b66(\u9700\u8981mgear)", None))
    # retranslateUi

