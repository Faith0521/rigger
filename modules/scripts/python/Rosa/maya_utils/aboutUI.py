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
import weakref
import shiboken2
from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def get_maya_window():
    """
    return maya window by Qt object..
    """
    maya_window = om.MQtUtil.mainWindow()
    if maya_window:
        return shiboken2.wrapInstance(int(maya_window), QtWidgets.QWidget)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_workspace_control(control):
    if mc.workspaceControl(control, q=True, exists=True):
        mc.workspaceControl(control, e=True, close=True)
        mc.deleteUI(control, control=True)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def window_exists(name):
    """
    get named window, if window exists, return true; if not, return false..
    """
    widget = om.MQtUtil.findControl(name)
    if not widget:
        return False

    wnd = shiboken2.wrapInstance(int(widget), QtWidgets.QWidget)#QMainWindow
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

def confirmDialogWin(title, message, button=['Yes','No']):
    result = mc.confirmDialog(title=title,
                              message=message,
                              button=button,
                              defaultButton='Yes', cancelButton='No', dismissString='No')
    if result == button[0]:
        return True
    else:
        return False

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

def dockWin(widget, width=200, show=True):
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
                                        label=label,
                                        rs=True
                                      )

    dockPtr = om.MQtUtil.findControl(dockControl)
    dockWidget = shiboken2.wrapInstance(int(dockPtr), QtWidgets.QWidget)

    child = widget(dockWidget)
    dockWidget.layout().addWidget(child)
    dockWidget.layout().setContentsMargins(2, 2, 2, 2)

    if show:
        mc.evalDeferred( lambda *args: mc.workspaceControl(dockControl, edit=True, restore=True) )
    return child

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UI_Dockable(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    title_name = 'no name window'  # Window display name
    control_name = 'no_name_window'  # Window unique object name
    instances = list()

    def __init__(self, parent=None):
        super(UI_Dockable, self).__init__(parent)
        self.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        if mc.workspaceControl(self.control_name + "WorkspaceControl", q=True, exists=True):
            mc.deleteUI(self.control_name + "WorkspaceControl")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName(self.control_name)
        self.setWindowTitle(self.title_name)

        self.build_ui()

    @staticmethod
    def delete_instances():
        for ins in UI_Dockable.instances:
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass
            try:
                UI_Dockable.instances.remove(ins)
                del ins
            except:
                # Supress error
                pass

    def build_ui(self):
        """
        This function is called at the end of window initialization and creates your actual UI.
        Override it with your UI.
        """
        pass