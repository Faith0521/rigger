#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/2/10 17:59
# @Author : yinyufei
# @File : listwidget.py
# @Project : TeamCode
from cgrigvendor.Qt.QtWidgets import QScrollArea, QWidget, QMenu
from cgrigvendor.Qt.QtCore import Signal, Qt
from cgrigvendor.Qt.QtGui import QPainter, QColor, QPixmap, QCursor
from cgrig.libs.pyqt.widgets import elements
import os

from mgear.shifter_epic_components.EPIC_arm_01.settingsUI import QtWidgets


class _ListViewWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('#3D3D3D'))
        painter.drawRect(self.rect())
        painter.end()


class _ListItemWidget(QWidget):
    click = Signal()

    def __init__(self, text, icon_path=None, function_table=None, parent=None):
        self.function_table = function_table

        super(_ListItemWidget, self).__init__(parent)
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)
        self.main_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if icon_path:
            if not os.path.isfile(icon_path):
                raise LookupError('icon_path not found: {}'.format(icon_path))

            icon = elements.Label(parent=self)
            icon_pix = QPixmap(icon_path)
            icon_pix = icon_pix.scaled(20, 20)
            icon.setPixmap(icon_pix)
            self.main_layout.addWidget(icon)

        label = elements.Label(text=text)
        self.main_layout.addWidget(label)

        self.is_left_press = False
        self.is_right_press = False
        self.selected = False

    def setSelectState(self, state):
        self.selected = state
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_left_press = True
            self.update()
        if event.button() == Qt.RightButton:
            self.is_right_press = True
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_left_press:
            self.click.emit()
            self.is_left_press = False
            self.update()
        if event.button() == Qt.RightButton and self.is_right_press:
            self.is_right_press = False
            self.update()
            self.showRightMenu()

    def showRightMenu(self):
        if self.function_table is None or len(self.function_table) == 0:
            return
        menu = QMenu(self)
        for text, callback in self.function_table:
            action = menu.addAction(text)
            action.triggered.connect(callback)

        pos = QCursor.pos()
        menu.exec_(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        if self.selected:
            painter.setBrush(QColor('#48AAB5'))
        elif self.is_left_press or self.is_right_press:
            painter.setBrush(QColor('#4F4F4F'))
        else:
            painter.setBrush(QColor('#333333'))
        painter.drawRect(self.rect())
        painter.end()


class ListWidget(QScrollArea):
    item_click = Signal(str)

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setWidgetResizable(True)

        self.main_widget = _ListViewWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)

        self.setWidget(self.main_widget)

        self._items = []
        self._key_to_item_table = dict()

    def addItem(self, key, name, icon_path=None, function_table=None):
        # type: (str, str, str) -> None
        item = _ListItemWidget(name, icon_path, function_table)
        self._items.append(item)
        self._key_to_item_table[key] = item
        item.click.connect(lambda: self.item_click.emit(key))
        item.click.connect(self.clearAllSelect)
        item.click.connect(lambda: item.setSelectState(True))
        self.main_layout.addWidget(item)

    def clearAllSelect(self):
        for i in self._items:
            i.setSelectState(False)

    def updateItems(self, items):
        # type: (List[Tuple[str, str, str|None, List[Tuple[str, Callable]]|None]]) -> None

        self.clear()
        for key, name, icon_path, function_table in items:
            self.addItem(key, name, icon_path, function_table)

    def clear(self):
        self._items = []
        self._key_to_item_table = dict()
        for i in range(self.main_layout.count()):
            self.main_layout.itemAt(i).widget().deleteLater()

    def nowSelectItem(self):
        for i_key, i in self._key_to_item_table.items():
            if i.selected:
                return i_key
        return None

    def findItem(self, key):
        return self._key_to_item_table.get(key, None)

    def setSelectItem(self, key):
        for i_key, i in self._key_to_item_table.items():
            if i_key == key:
                i.setSelectState(True)
            else:
                i.setSelectState(False)


class ListEditWidget(QWidget):
    item_click = Signal(str)
    plus_click = Signal()
    trash_click = Signal(str)

    def __init__(self, object_type_name, parent=None):
        super(ListEditWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景透明：避免圆角外的区域显示白色底色
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(2)
        self.main_layout.setAlignment(Qt.AlignCenter)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(elements.Label(text=object_type_name))
        h_layout.addStretch(0)

        self._refresh_button = elements.IconMenuButton(iconName="refresh", parent=self)
        self._plus_button = elements.IconMenuButton(iconName="plus", parent=self)
        self._trash_button = elements.IconMenuButton(iconName="deletePreset", parent=self)
        self._plus_button.clicked.connect(self.plus_click.emit)
        self._trash_button.clicked.connect(self._sendTrashClick)

        h_layout.addWidget(self._refresh_button)
        h_layout.addWidget(self._plus_button)
        h_layout.addWidget(self._trash_button)

        self.main_layout.addLayout(h_layout)
        self.search_line_edit = elements.LineEdit(placeholder="search")
        self.search_line_edit.setAlignment(Qt.AlignCenter)
        self.search_line_edit.textModified.connect(self.refreshList)

        self._now_item_key = None
        self.list_widget = ListWidget()
        self.list_widget.item_click.connect(self._setNowItemKey)
        self.list_widget.item_click.connect(self.item_click.emit)

        self.main_layout.addWidget(self.search_line_edit)
        self.main_layout.addWidget(self.list_widget)

        self._items = []

    def _setNowItemKey(self, key):
        self._now_item_key = key

    def _sendTrashClick(self):
        self.trash_click.emit(self._now_item_key)
        self._now_item_key = None

    def updateItems(self, items):
        # type: (Iterator[Tuple[str, str, str|None, List[Tuple[str, Callable]]|None]]) -> None
        self._items = list(items)
        self.refreshList()

    def refreshList(self):
        print('refresh_list')
        print('search_line_edit.text():', self.search_line_edit.text())
        items = [
            (key, name, icon_path, function_table)
            for key, name, icon_path, function_table in self._items
            if self.search_line_edit.text() in name
        ]
        self.list_widget.updateItems(items)

    def setSelectItem(self, key):
        if self.list_widget.findItem(key) is None:
            self.search_line_edit.setText('')
            self.refreshList()
        self.list_widget.setSelectItem(key)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('#3D3D3D'))
        painter.drawRoundedRect(self.rect(),10,10)
        painter.end()


















