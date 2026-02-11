#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/2/10 17:48
# @Author : yinyufei
# @File : selectui.py
# @Project : TeamCode
from cgrigvendor.Qt import QtWidgets, QtGui, QtCore
from cgrigvendor.Qt.QtWidgets import QWidget
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt.widgets.frameless.widgets import Dialog



class SelectDialogBodyWidget(QWidget):
    def __init__(self, options, dialog):
        self.dialog = dialog
        self.result = None

        super(SelectDialogBodyWidget, self).__init__()

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)
        if len(options) == 0:
            label = elements.Label(text='No Options')
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.addWidget(label)
            return

        self.list_widget = elements.ListWidget()
        self.list_widget.updateItems([(key, name, icon, None) for key, name, icon in options])
        self.list_widget.setSelectItem(options[0][0])

        self.main_layout.addWidget(self.list_widget)

        h_layout = QtWidgets.QHBoxLayout(self)
        h_layout.setContentsMargins(5, 5, 5, 5)
        h_layout.setSpacing(2)

        h_layout.addStretch(0)

        self.ok_button = elements.styledButton(text=u"确认", icon="cursorSelect")
        self.cancel_button = elements.styledButton(text=u"取消", icon="close")
        self.ok_button.clicked.connect(self.okClick)
        self.cancel_button.clicked.connect(self.cancelClick)

        h_layout.addWidget(self.ok_button)
        h_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(h_layout)

    def okClick(self):
        self.result = self.list_widget.nowSelectItem()
        self.dialog.close()

    def cancelClick(self):
        self.dialog.close()


class SelectDialog(Dialog):
    def __init__(self, options, icon_path=None, parent=None):
        """

        :param options: [(key, name, icon_path)]
        :param parent:
        """
        self.body_widget = SelectDialogBodyWidget(options, self)
        super(SelectDialog, self).__init__(self.body_widget, icon_path=icon_path, parent=parent)
        self.resize(375, 205)

    @staticmethod
    def select(options, icon_path=None, parent=None):
        dialog = SelectDialog(options, icon_path=icon_path, parent=parent)
        dialog.exec_()
        return dialog.body_widget.result




