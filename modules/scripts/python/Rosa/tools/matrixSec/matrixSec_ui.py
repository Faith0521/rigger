# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\matrixSecUI.ui'
#
# Created: Mon Dec 18 13:40:03 2023
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_matrixSecUI(object):
    def setupUi(self, matrixSecUI):
        matrixSecUI.setObjectName("matrixSecUI")
        matrixSecUI.resize(435, 611)
        self.centralwidget = QtWidgets.QWidget(matrixSecUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.splitter01 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter01.setOrientation(QtCore.Qt.Horizontal)
        self.splitter01.setObjectName("splitter01")
        self.layoutWidget = QtWidgets.QWidget(self.splitter01)
        self.layoutWidget.setObjectName("layoutWidget")
        self.right_layout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setObjectName("right_layout")
        self.create_gb = QtWidgets.QGroupBox(self.layoutWidget)
        self.create_gb.setAutoFillBackground(False)
        self.create_gb.setObjectName("create_gb")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.create_gb)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.initMesh_btn = QtWidgets.QPushButton(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initMesh_btn.sizePolicy().hasHeightForWidth())
        self.initMesh_btn.setSizePolicy(sizePolicy)
        self.initMesh_btn.setMinimumSize(QtCore.QSize(50, 0))
        self.initMesh_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.initMesh_btn.setObjectName("initMesh_btn")
        self.horizontalLayout_3.addWidget(self.initMesh_btn)
        self.initMesh_line = QtWidgets.QLineEdit(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initMesh_line.sizePolicy().hasHeightForWidth())
        self.initMesh_line.setSizePolicy(sizePolicy)
        self.initMesh_line.setObjectName("initMesh_line")
        self.horizontalLayout_3.addWidget(self.initMesh_line)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.orgVtxs_btn = QtWidgets.QPushButton(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orgVtxs_btn.sizePolicy().hasHeightForWidth())
        self.orgVtxs_btn.setSizePolicy(sizePolicy)
        self.orgVtxs_btn.setMinimumSize(QtCore.QSize(50, 0))
        self.orgVtxs_btn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.orgVtxs_btn.setObjectName("orgVtxs_btn")
        self.horizontalLayout_6.addWidget(self.orgVtxs_btn)
        self.orgVtxs_line = QtWidgets.QLineEdit(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orgVtxs_line.sizePolicy().hasHeightForWidth())
        self.orgVtxs_line.setSizePolicy(sizePolicy)
        self.orgVtxs_line.setObjectName("orgVtxs_line")
        self.horizontalLayout_6.addWidget(self.orgVtxs_line)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.prefix_lb = QtWidgets.QLabel(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prefix_lb.sizePolicy().hasHeightForWidth())
        self.prefix_lb.setSizePolicy(sizePolicy)
        self.prefix_lb.setMinimumSize(QtCore.QSize(50, 0))
        self.prefix_lb.setObjectName("prefix_lb")
        self.horizontalLayout_10.addWidget(self.prefix_lb)
        self.prefix_line = QtWidgets.QLineEdit(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prefix_line.sizePolicy().hasHeightForWidth())
        self.prefix_line.setSizePolicy(sizePolicy)
        self.prefix_line.setObjectName("prefix_line")
        self.horizontalLayout_10.addWidget(self.prefix_line)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.line = QtWidgets.QFrame(self.create_gb)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.sec_sys_btn = QtWidgets.QPushButton(self.create_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sec_sys_btn.sizePolicy().hasHeightForWidth())
        self.sec_sys_btn.setSizePolicy(sizePolicy)
        self.sec_sys_btn.setMinimumSize(QtCore.QSize(120, 0))
        self.sec_sys_btn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sec_sys_btn.setBaseSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sec_sys_btn.setFont(font)
        self.sec_sys_btn.setStyleSheet("QPushButton{ \n"
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
        self.sec_sys_btn.setObjectName("sec_sys_btn")
        self.verticalLayout_2.addWidget(self.sec_sys_btn)
        self.right_layout.addWidget(self.create_gb)
        self.splitter02 = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter02.setOrientation(QtCore.Qt.Vertical)
        self.splitter02.setObjectName("splitter02")
        self.system_gb = QtWidgets.QGroupBox(self.splitter02)
        self.system_gb.setObjectName("system_gb")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.system_gb)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sec_sys_lv = QtWidgets.QListWidget(self.system_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sec_sys_lv.sizePolicy().hasHeightForWidth())
        self.sec_sys_lv.setSizePolicy(sizePolicy)
        self.sec_sys_lv.setMinimumSize(QtCore.QSize(120, 0))
        self.sec_sys_lv.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sec_sys_lv.setBaseSize(QtCore.QSize(10, 0))
        self.sec_sys_lv.setObjectName("sec_sys_lv")
        self.horizontalLayout_7.addWidget(self.sec_sys_lv)
        self.mesh_gb = QtWidgets.QGroupBox(self.splitter02)
        self.mesh_gb.setObjectName("mesh_gb")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.mesh_gb)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.mesh_add_btn = QtWidgets.QPushButton(self.mesh_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mesh_add_btn.sizePolicy().hasHeightForWidth())
        self.mesh_add_btn.setSizePolicy(sizePolicy)
        self.mesh_add_btn.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mesh_add_btn.setFont(font)
        self.mesh_add_btn.setStyleSheet("QPushButton{ \n"
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
        self.mesh_add_btn.setObjectName("mesh_add_btn")
        self.horizontalLayout_4.addWidget(self.mesh_add_btn)
        self.mesh_remove_btn = QtWidgets.QPushButton(self.mesh_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mesh_remove_btn.sizePolicy().hasHeightForWidth())
        self.mesh_remove_btn.setSizePolicy(sizePolicy)
        self.mesh_remove_btn.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mesh_remove_btn.setFont(font)
        self.mesh_remove_btn.setStyleSheet("QPushButton{ \n"
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
        self.mesh_remove_btn.setObjectName("mesh_remove_btn")
        self.horizontalLayout_4.addWidget(self.mesh_remove_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mesh_lv = QtWidgets.QListWidget(self.mesh_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mesh_lv.sizePolicy().hasHeightForWidth())
        self.mesh_lv.setSizePolicy(sizePolicy)
        self.mesh_lv.setMinimumSize(QtCore.QSize(0, 0))
        self.mesh_lv.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.mesh_lv.setTextElideMode(QtCore.Qt.ElideRight)
        self.mesh_lv.setObjectName("mesh_lv")
        self.horizontalLayout.addWidget(self.mesh_lv)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.right_layout.addWidget(self.splitter02)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter01)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.left_layout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setObjectName("left_layout")
        self.modify_gb = QtWidgets.QGroupBox(self.layoutWidget1)
        self.modify_gb.setObjectName("modify_gb")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.modify_gb)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.md_hl1_2 = QtWidgets.QHBoxLayout()
        self.md_hl1_2.setObjectName("md_hl1_2")
        self.md_prefix_lb = QtWidgets.QLabel(self.modify_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md_prefix_lb.sizePolicy().hasHeightForWidth())
        self.md_prefix_lb.setSizePolicy(sizePolicy)
        self.md_prefix_lb.setObjectName("md_prefix_lb")
        self.md_hl1_2.addWidget(self.md_prefix_lb)
        self.md_prefix_line = QtWidgets.QLineEdit(self.modify_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md_prefix_line.sizePolicy().hasHeightForWidth())
        self.md_prefix_line.setSizePolicy(sizePolicy)
        self.md_prefix_line.setObjectName("md_prefix_line")
        self.md_hl1_2.addWidget(self.md_prefix_line)
        self.verticalLayout_8.addLayout(self.md_hl1_2)
        self.md_hl2_2 = QtWidgets.QHBoxLayout()
        self.md_hl2_2.setObjectName("md_hl2_2")
        self.md_initMesh_lb = QtWidgets.QLabel(self.modify_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md_initMesh_lb.sizePolicy().hasHeightForWidth())
        self.md_initMesh_lb.setSizePolicy(sizePolicy)
        self.md_initMesh_lb.setObjectName("md_initMesh_lb")
        self.md_hl2_2.addWidget(self.md_initMesh_lb)
        self.md_initMesh_line = QtWidgets.QLineEdit(self.modify_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md_initMesh_line.sizePolicy().hasHeightForWidth())
        self.md_initMesh_line.setSizePolicy(sizePolicy)
        self.md_initMesh_line.setObjectName("md_initMesh_line")
        self.md_hl2_2.addWidget(self.md_initMesh_line)
        self.verticalLayout_8.addLayout(self.md_hl2_2)
        self.md_line = QtWidgets.QFrame(self.modify_gb)
        self.md_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.md_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.md_line.setObjectName("md_line")
        self.verticalLayout_8.addWidget(self.md_line)
        self.meshs_gb = QtWidgets.QWidget(self.modify_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meshs_gb.sizePolicy().hasHeightForWidth())
        self.meshs_gb.setSizePolicy(sizePolicy)
        self.meshs_gb.setObjectName("meshs_gb")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.meshs_gb)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.md_mesh_grid = QtWidgets.QGridLayout()
        self.md_mesh_grid.setObjectName("md_mesh_grid")
        self.horizontalLayout_9.addLayout(self.md_mesh_grid)
        self.verticalLayout_8.addWidget(self.meshs_gb)
        self.genarate_btn = QtWidgets.QPushButton(self.modify_gb)
        self.genarate_btn.setStyleSheet("QPushButton{ \n"
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
        self.genarate_btn.setObjectName("genarate_btn")
        self.verticalLayout_8.addWidget(self.genarate_btn)
        self.exit_btn = QtWidgets.QPushButton(self.modify_gb)
        self.exit_btn.setStyleSheet("QPushButton{ \n"
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
        self.exit_btn.setObjectName("exit_btn")
        self.verticalLayout_8.addWidget(self.exit_btn)
        self.horizontalLayout_12.addLayout(self.verticalLayout_8)
        self.left_layout.addWidget(self.modify_gb)
        self.ctrl_gb = QtWidgets.QGroupBox(self.layoutWidget1)
        self.ctrl_gb.setObjectName("ctrl_gb")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ctrl_gb)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ctrl_add_btn = QtWidgets.QPushButton(self.ctrl_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ctrl_add_btn.sizePolicy().hasHeightForWidth())
        self.ctrl_add_btn.setSizePolicy(sizePolicy)
        self.ctrl_add_btn.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ctrl_add_btn.setFont(font)
        self.ctrl_add_btn.setStyleSheet("QPushButton{ \n"
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
        self.ctrl_add_btn.setObjectName("ctrl_add_btn")
        self.horizontalLayout_5.addWidget(self.ctrl_add_btn)
        self.ctrl_remove_btn = QtWidgets.QPushButton(self.ctrl_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ctrl_remove_btn.sizePolicy().hasHeightForWidth())
        self.ctrl_remove_btn.setSizePolicy(sizePolicy)
        self.ctrl_remove_btn.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ctrl_remove_btn.setFont(font)
        self.ctrl_remove_btn.setStyleSheet("QPushButton{ \n"
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
        self.ctrl_remove_btn.setObjectName("ctrl_remove_btn")
        self.horizontalLayout_5.addWidget(self.ctrl_remove_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ctrl_lv = QtWidgets.QTreeWidget(self.ctrl_gb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ctrl_lv.sizePolicy().hasHeightForWidth())
        self.ctrl_lv.setSizePolicy(sizePolicy)
        self.ctrl_lv.setMinimumSize(QtCore.QSize(0, 0))
        self.ctrl_lv.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ctrl_lv.setObjectName("ctrl_lv")
        self.ctrl_lv.header().setVisible(False)
        self.horizontalLayout_2.addWidget(self.ctrl_lv)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.left_layout.addWidget(self.ctrl_gb)
        self.verticalLayout_9.addWidget(self.splitter01)
        matrixSecUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(matrixSecUI)
        QtCore.QMetaObject.connectSlotsByName(matrixSecUI)

    def retranslateUi(self, matrixSecUI):
        matrixSecUI.setWindowTitle(QtWidgets.QApplication.translate("matrixSecUI", "matrixSec_v1.1", None, -1))
        self.create_gb.setTitle(QtWidgets.QApplication.translate("matrixSecUI", "Creat", None, -1))
        self.initMesh_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "Mesh >", None, -1))
        self.orgVtxs_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "Vtxs >", None, -1))
        self.prefix_lb.setText(QtWidgets.QApplication.translate("matrixSecUI", "Prefix:", None, -1))
        self.sec_sys_btn.setToolTip(QtWidgets.QApplication.translate("matrixSecUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.sec_sys_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "+ Sec System", None, -1))
        self.system_gb.setTitle(QtWidgets.QApplication.translate("matrixSecUI", "System", None, -1))
        self.mesh_gb.setTitle(QtWidgets.QApplication.translate("matrixSecUI", "Meshs", None, -1))
        self.mesh_add_btn.setToolTip(QtWidgets.QApplication.translate("matrixSecUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.mesh_add_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "+", None, -1))
        self.mesh_remove_btn.setToolTip(QtWidgets.QApplication.translate("matrixSecUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.mesh_remove_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "-", None, -1))
        self.modify_gb.setTitle(QtWidgets.QApplication.translate("matrixSecUI", "Modify", None, -1))
        self.md_prefix_lb.setText(QtWidgets.QApplication.translate("matrixSecUI", "Prefix:", None, -1))
        self.md_initMesh_lb.setText(QtWidgets.QApplication.translate("matrixSecUI", "InitMesh:", None, -1))
        self.genarate_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "Genarate", None, -1))
        self.exit_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "Exit", None, -1))
        self.ctrl_gb.setTitle(QtWidgets.QApplication.translate("matrixSecUI", "Controls", None, -1))
        self.ctrl_add_btn.setToolTip(QtWidgets.QApplication.translate("matrixSecUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.ctrl_add_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "+", None, -1))
        self.ctrl_remove_btn.setToolTip(QtWidgets.QApplication.translate("matrixSecUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Build the next step in the list.</p></body></html>", None, -1))
        self.ctrl_remove_btn.setText(QtWidgets.QApplication.translate("matrixSecUI", "-", None, -1))
        self.ctrl_lv.headerItem().setText(0, QtWidgets.QApplication.translate("matrixSecUI", "ghdfgh", None, -1))

