#!/usr/bin/python
# -*- coding: utf-8 -*-
#=============================================
#   author: ruixi.wang
#   mail: wrx1844@qq.com
#   date: Thu, 03 Jul 2019 16:35:02
#=============================================
import re
import maya.cmds as mc
import maya.OpenMayaUI as om

def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from shiboken2 import wrapInstance
        return QtCore, QtGui, QtWidgets, wrapInstance
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from shiboken6 import wrapInstance
            return QtCore, QtGui, QtWidgets, wrapInstance
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets, wrapInstance= get_pyside_module()
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def get_maya_window():
    """
    return maya window by Qt object..
    """
    maya_window = om.MQtUtil.mainWindow()
    if maya_window:
        return wrapInstance(int(maya_window), QtWidgets.QWidget)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def window_exists(name):
    """
    get named window, if window exists, return true; if not, return false..
    """
    widget = om.MQtUtil.findControl(name)
    if not widget:
        return False

    wnd = wrapInstance(int(widget), QtWidgets.QWidget)#QMainWindow
    wnd.showNormal()
    wnd.activateWindow()
    return True

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getChildrenWindows(parent):
    """
    get object's children windows..
    """
    windows = []
    if not parent:return windows

    for child in parent.children():
        if not hasattr(child, 'isWindow'):
            continue
        if not child.isWindow():
            continue
        windows.append(child)
    return windows

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def cleanChildrenWindows(parent, delete=True):
    """
    delete window's child window...
    """
    if not parent:return
    for child in getChildrenWindows(parent):
        if not re.match('RootUI|Plugcmds', child.__module__):
            continue
        child.close()
        if not delete:continue
        child.deleteLater()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def promptDialogWin(titleDialog='None', instrunctions='Default', buttons=['OK', 'Cancel'], text=None):
    """dialog window to get input imformation"""

    dialog = mc.promptDialog(title=titleDialog,
                             message=instrunctions,
                             tx=text,
                             button=buttons,
                             defaultButton=buttons[0],
                             cancelButton=buttons[1],
                             dismissString=buttons[1])

    if dialog == 'OK':
        text = mc.promptDialog(query=True, text=True)
    else:
        text = None
    return text

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def dockWin(widget, width=390, show=True):
    """Dock `Widget` into Maya"""

    name = widget.DOCK_NAME
    label = widget.DOCK_LABEL

    try:
        mc.deleteUI(name, control=True)

    except RuntimeError:
        pass

    dockControl = mc.workspaceControl(  name,
                                        tabToControl=["Outliner", -1],
                                        initialWidth=width,
                                        minimumWidth=True,
                                        widthProperty="preferred",
                                        label=label
                                      )

    dockPtr = om.MQtUtil.findControl(dockControl)
    dockWidget = wrapInstance(int(dockPtr), QtWidgets.QWidget)

    child = widget(dockWidget)
    dockWidget.layout().addWidget(child)
    dockWidget.layout().setContentsMargins(2, 2, 2, 2)

    if show:
        mc.evalDeferred( lambda *args: mc.workspaceControl(dockControl, edit=True, restore=True) )
    return child

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def hide_layout_items(layout):
    for i in range(layout.count()):
        item = layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            widget.hide()
        else:
            # 如果item是一个布局，则递归调用
            sub_layout = item.layout()
            if sub_layout is not None:
                hide_layout_items(sub_layout)

def show_layout_items(layout):
    for i in range(layout.count()):
        item = layout.itemAt(i)
        widget = item.widget()
        if widget is not None:
            widget.show()
        else:
            # 如果item是一个布局，则递归调用
            sub_layout = item.layout()
            if sub_layout is not None:
                show_layout_items(sub_layout)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
