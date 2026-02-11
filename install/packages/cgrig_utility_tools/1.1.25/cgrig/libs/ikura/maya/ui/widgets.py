#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 16:59
# @Author : yinyufei
# @File : widgets.py
# @Project : TeamCode
import traceback
import webbrowser
from functools import partial
from six.moves import range
from six import string_types

import maya.cmds as mc
from cgrigvendor.Qt import QtCore, QtWidgets, QtCompat
from cgrigvendor.Qt.QtCore import Qt
from cgrigvendor.Qt.QtGui import QSyntaxHighlighter
from cgrigvendor.Qt.QtWidgets import QMainWindow, QDockWidget, QVBoxLayout, QWidget, QDialog, QTextEdit


class OptVarSettings(object):
    """选项变量设置类

    用于管理Maya选项变量，提供获取和设置选项变量的方法。
    """

    def __init__(self, *args, **kw):
        """初始化选项变量设置

        参数:
            *args: 位置参数
            **kw: 关键字参数
        """
        pass

    def optvar_id(self):
        """获取选项变量ID

        返回值:
            选项变量的ID，通常是类名或对象名称
        """
        opt = self.__class__.__name__
        try:
            opt = self.objectName() or opt
        except:
            pass
        return opt

    def get_optvar(self, name, default=None):
        """获取选项变量

        参数:
            name: 选项变量名称
            default: 默认值，当选项变量不存在时返回

        返回值:
            选项变量的值，或默认值
        """
        opt_var = '{object}::{name}'.format(object=self.optvar_id(), name=name)
        opt_vars = list(filter(partial(lambda x: x.startswith(opt_var)), mc.optionVar(list=1)))

        if opt_vars:
            opt_var = opt_vars[0]
            if mc.optionVar(exists=opt_var):
                v = mc.optionVar(q=opt_var)
                if opt_var.endswith('.bool'):
                    return bool(v)
                elif opt_var.endswith('.point'):
                    return QtCore.QPoint(*v)
                elif opt_var.endswith('.geo'):
                    return QtCore.QRect(*v)
                elif opt_var.endswith('.area'):
                    return getattr(Qt, v)
                return v
        return default

    def set_optvar(self, name, v):
        """设置选项变量

        参数:
            name: 选项变量名称
            v: 选项变量值
        """
        opt_var = '{object}::{name}'.format(object=self.optvar_id(), name=name) + '{}'

        if isinstance(v, bool):
            mc.optionVar(intValue=(opt_var.format('.bool'), int(v)))
        elif isinstance(v, int):
            mc.optionVar(intValue=(opt_var.format(''), v))
        elif isinstance(v, float):
            mc.optionVar(floatValue=(opt_var.format(''), v))
        elif isinstance(v, string_types):
            mc.optionVar(stringValue=(opt_var.format(''), str(v)))

        elif isinstance(v, Qt.DockWidgetArea):
            mc.optionVar(stringValue=(opt_var.format('.area'), v.name))

        elif isinstance(v, QtCore.QPoint):
            opt_var = opt_var.format('.point')
            if mc.optionVar(exists=opt_var):
                mc.optionVar(remove=opt_var)
            mc.optionVar(intValueAppend=[
                (opt_var, v.x()),
                (opt_var, v.y())
            ])

        elif isinstance(v, QtCore.QRect):
            opt_var = opt_var.format('.geo')
            if mc.optionVar(exists=opt_var):
                mc.optionVar(remove=opt_var)
            mc.optionVar(intValueAppend=[
                (opt_var, v.x()),
                (opt_var, v.y()),
                (opt_var, v.width()),
                (opt_var, v.height())
            ])
