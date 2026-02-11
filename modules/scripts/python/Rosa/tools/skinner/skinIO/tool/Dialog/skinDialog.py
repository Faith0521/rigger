import maya.OpenMayaUI as OpenMayaUI
import maya.cmds 
from importlib import reload

import inspect
import os
import posixpath 

from PySide2 import QtGui, QtCore, QtWidgets
from shiboken2 import wrapInstance

from skinIO.tool.Widgets import exportWidget
from skinIO.tool.Widgets import importWidget

reload(exportWidget)
reload(importWidget)

class mayaTool(QtWidgets.QMainWindow):
    def __init__(self,
                 title):
        super(mayaTool, self).__init__(self.getMainWindow())

        windowName = '{}_windowTool'.format(title.replace(' ', ''))

        self.removePreviousWindow(windowName)

        self.setWindowTitle(title)
        self.setObjectName(windowName)

    def removePreviousWindow(self,
                             windowName):
        widgetLink = OpenMayaUI.MQtUtil.findControl(windowName)

        if widgetLink is not None:
            guiFullName = OpenMayaUI.MQtUtil.fullName(int(widgetLink))
            maya.cmds.deleteUI(guiFullName)

    def getMainWindow(self):
        """
            Return the Maya main window widget as a Python object
         
            return: Maya Main Window.
        """
        mainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()

        return wrapInstance(int(mainWindowPtr),
                            QtWidgets.QWidget)


class SkinTool(mayaTool):
    def __init__(self):
        self.width = 680

        super(SkinTool, self).__init__('Skin Tool')

        self.setupUi()

    def setupUi(self):
        self.mainFrame = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.exporterWidget = exportWidget.SkinExportWidget(self)
        
        self.importerWidget = importWidget.SkinImportWidget(self)

        self.tabWidget = QtWidgets.QTabWidget()

        self.tabWidget.addTab(self.exporterWidget, "Export")

        self.tabWidget.addTab(self.importerWidget, 'Import')

        self.mainLayout.addWidget(self.tabWidget)

        self.mainFrame.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainFrame)


def Run():
    skinUI = SkinTool()

    skinUI.show()