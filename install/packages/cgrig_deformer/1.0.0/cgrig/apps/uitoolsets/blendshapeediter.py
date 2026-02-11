#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/28 11:05
# @Author : yinyufei
# @File : blendshapeediter.py
# @Project : TeamCode
import os
import json
import collections
import re
from functools import partial
from Qt import QtWidgets, QtCore, QtGui
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements


class ShapeEditor(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ShapeEditor, self).__init__(parent)
        self.setWindowTitle("Shape Editor")
        self.setMinimumSize(500, 450)
        self._setup_ui()
        # 记录鼠标点击时的按键状态
        self.ctrl_pressed = False
        # 标记是否正在批量更新复选框（防止递归触发）
        self._batch_updating = False

    def _setup_ui(self):
        # 主布局（保留原有逻辑）
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. 菜单栏
        menu_bar = self.menuBar()
        for menu_name in ["File", "Edit", "Create", "Shapes", "Options", "Help"]:
            menu_bar.addMenu(menu_name)

        # 2. 工具栏
        tool_bar = QtWidgets.QToolBar()
        self.addToolBar(tool_bar)

        search_widget = QtWidgets.QWidget()
        search_layout = QtWidgets.QHBoxLayout(search_widget)
        search_layout.setContentsMargins(5, 5, 5, 5)
        create_bs_btn = elements.styledButton("Create BlendShape")
        add_target_btn = elements.styledButton("Add Target")

        search_field = QtWidgets.QLineEdit()
        search_field.setPlaceholderText("Search...")
        load_mesh_button = elements.styledButton("Load Mesh")
        search_layout.addWidget(search_field)
        search_layout.addWidget(load_mesh_button)
        tool_bar.addWidget(create_bs_btn)
        tool_bar.addWidget(add_target_btn)
        tool_bar.addWidget(search_widget)

        # 3. 树形表格区域
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(["Name", "Weight/Slider", "Edit"])

        # 设置多选模式（关键：ExtendedSelection支持Ctrl/Shift多选）
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # 监听复选框点击事件（通过itemChanged信号）
        self.tree_widget.itemChanged.connect(self.on_item_check_state_changed)
        # 监听键盘按键事件（空格批量勾选）
        self.tree_widget.keyPressEvent = self.on_key_press
        self.tree_widget.keyReleaseEvent = self.on_key_release

        # 表头列宽
        header = self.tree_widget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        header.resizeSection(0, 200)
        header.resizeSection(1, 350)
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        main_layout.addWidget(self.tree_widget)

        # # 构建树形结构
        # root_item = QtWidgets.QTreeWidgetItem(self.tree_widget, ["blendShape1"])
        # root_item.setCheckState(0, QtCore.Qt.Checked)
        # self._add_weight_slider_widget(root_item, 1, "1.000")
        #
        # # 添加子项
        # for name in ["pTorus2", "pTorus3", "pTorus4", "pTorus5"]:
        #     child_item = QtWidgets.QTreeWidgetItem(root_item, [name])
        #     child_item.setCheckState(0, QtCore.Qt.Checked)
        #     self._add_weight_slider_widget(child_item, 1, "0.000")
        #     self._add_edit_button_to_item(child_item, 2)
        #     if name == "pTorus5":
        #         child_item.setSelected(True)

    def _add_weight_slider_widget(self, item, column, initial_value):
        """数值+滑块合并控件"""
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)

        weight_label = QtWidgets.QLabel(initial_value)
        weight_label.setFixedWidth(60)
        weight_label.setAlignment(QtCore.Qt.AlignCenter)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 1000)
        slider.setValue(int(float(initial_value) * 1000))
        slider.valueChanged.connect(lambda val, label=weight_label: self._update_weight_label(label, val))

        layout.addWidget(weight_label)
        layout.addWidget(slider)
        self.tree_widget.setItemWidget(item, column, container)

    def _update_weight_label(self, label, slider_value):
        """更新数值标签"""
        weight_value = slider_value / 1000.0
        label.setText(f"{weight_value:.3f}")

    def _add_edit_button_to_item(self, item, column):
        """添加Edit按钮"""
        btn = QtWidgets.QPushButton("Edit")
        self.tree_widget.setItemWidget(item, column, btn)

    def on_item_check_state_changed(self, item, column):
        """复选框状态变化时，批量同步所有选中Item的状态"""
        # 避免递归触发（批量更新时跳过）
        if self._batch_updating or column != 0:
            return

        # 获取当前所有选中的Item
        selected_items = self.tree_widget.selectedItems()
        if len(selected_items) <= 1:
            return  # 只有1个选中，无需批量处理

        # 获取当前修改的状态
        target_state = item.checkState(0)
        # 标记批量更新中
        self._batch_updating = True
        # 同步所有选中Item的复选框状态
        for selected_item in selected_items:
            if selected_item != item:  # 跳过触发的那个Item
                selected_item.setCheckState(0, target_state)
        # 取消批量更新标记
        self._batch_updating = False

    def on_key_press(self, event):
        """键盘事件：Ctrl键状态记录 + 空格键批量勾选/取消勾选"""
        if event.key() == QtCore.Qt.Key_Control:
            self.ctrl_pressed = True

        # 空格键触发批量勾选/取消勾选
        if event.key() == QtCore.Qt.Key_Space:
            selected_items = self.tree_widget.selectedItems()
            if not selected_items:
                return

            # 取第一个Item的状态作为目标状态（反向切换）
            first_state = selected_items[0].checkState(0)
            target_state = QtCore.Qt.Unchecked if first_state == QtCore.Qt.Checked else QtCore.Qt.Checked

            # 批量更新
            self._batch_updating = True
            for item in selected_items:
                item.setCheckState(0, target_state)
            self._batch_updating = False
            return  # 阻止空格的默认行为

        # 保留原键盘事件
        QtWidgets.QTreeWidget.keyPressEvent(self.tree_widget, event)

    def on_key_release(self, event):
        """释放Ctrl键"""
        if event.key() == QtCore.Qt.Key_Control:
            self.ctrl_pressed = False
        QtWidgets.QTreeWidget.keyReleaseEvent(self.tree_widget, event)

class BsToolUI(toolsetwidget.ToolsetWidget):
    id = "BsTool"
    uiData = {"label": "BlendShape Editer Window",
              "icon": "split",
              "tooltip": "Edit BlendShape Tool",
              "defaultActionDoubleClick": False
              }

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run"""
        pass

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        parent = QtWidgets.QWidget(parent=self)
        self.widgetsAll(parent)
        self.allLayouts(parent)
        return parent

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiConnections()

    def defaultAction(self):
        """Double Click"""
        pass

    # ------------------
    # PROPERTIES
    # ------------------
    def widgetsAll(self, parent):
        """Create all widgets for the GUI here

        See elements.py for all available widgets in the Zoo PySide framework.
        cgrig_pyside repo then cgrig.libs.pyqt.widgets.elements

        :param parent: The parent widget
        :type parent: obj
        """
        self.mainui = ShapeEditor()

    # ------------------
    # UI Layouts
    # ------------------

    def allLayouts(self, parent):
        """Builds the layout for the GUI.  Builds all qt layouts and adds all widgets

        :param parent: the parent widget
        :type parent: obj
        """
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(parent, margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)
        # Add To Main Layout ---------------------------------------
        mainLayout.addWidget(self.mainui)
    # ------------------
    # CALLBACKS
    # ------------------

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        # handles the coPlanar close event
        pass

