#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/10/11 17:10
# @Author : yinyufei
# @File : splitBs.py
# @Project : TeamCode

from functools import partial
from maya import cmds
import maya.mel as mel
from Qt import QtWidgets, QtCore
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.maya.cmds.rig import deformers


class SplitBsToolUI(toolsetwidget.ToolsetWidget):
    id = "splitBsTool"
    uiData = {"label": "Split Bs Window",
              "icon": "split",
              "tooltip": "Split BlendShape By Skin",
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
        self.compactWidget = CompactLayout(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiConnections()

    def defaultAction(self):
        """Double Click"""
        pass

    # ------------------
    # PROPERTIES
    # ------------------
    def loadMesh(self, widget):
        selection = cmds.ls(selection=True)
        result = None
        if not selection:
            result = ''
        else:
            result = selection[0]
        widget.setText(result)

    @staticmethod
    def listSkinCluster(inputMesh=''):
        obj = inputMesh
        skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + obj + "\")")
        if skinNode != '':
            return skinNode
        else:
            return False

    @toolsetwidget.ToolsetWidget.undoDecorator
    def apply(self):
        orgMesh = self.compactWidget.orgLine.text()
        skinMesh = self.compactWidget.skinLine.text()
        selection = cmds.ls(selection=True)
        skinNode = self.listSkinCluster(inputMesh=skinMesh)
        jnts = cmds.skinCluster(skinNode, q=True, inf=True)
        if not selection: return
        for sel in selection:
            deformers.splitBlendshape(inputBSMesh=sel, orgMesh=orgMesh, skinMesh=skinMesh, jointInputs=jnts)

    # ------------------
    # CALLBACKS
    # ------------------

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        # handles the coPlanar close event
        self.compactWidget.orgBtn.clicked.connect(partial(self.loadMesh, self.compactWidget.orgLine))
        self.compactWidget.skinBtn.clicked.connect(partial(self.loadMesh, self.compactWidget.skinLine))
        self.compactWidget.applyBtn.clicked.connect(self.apply)


class GuiWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc
        """
        super(GuiWidgets, self).__init__(parent=parent)

        self.toolsetWidget = toolsetWidget
        self.properties = properties

        self.orgLb = elements.Label("Org Mesh", parent=parent, bold=True)
        self.orgLine = elements.LineEdit(parent=self)
        self.orgBtn = elements.styledButton(text="Load", parent=self)
        self.skinLb = elements.Label("Skin Mesh", parent=parent, bold=True)
        self.skinLine = elements.LineEdit(parent=self)
        self.skinBtn = elements.styledButton(text="Load", parent=self)
        self.applyBtn = elements.styledButton(text="Apply", parent=self)


class CompactLayout(GuiWidgets):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Adds the layout building the compact version of the GUI:

            default uiMode - 0 is advanced (UI_MODE_COMPACT)

        :param parent: the parent of this widget
        :type parent: qtObject
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: list[dict]
        """
        super(CompactLayout, self).__init__(parent=parent, properties=properties,
                                            toolsetWidget=toolsetWidget)
        # Main Layout ------------------------------------
        contentsLayout = elements.vBoxLayout(self,
                                             margins=(uic.WINSIDEPAD,
                                                      uic.WINBOTPAD,
                                                      uic.WINSIDEPAD,
                                                      uic.WINBOTPAD),
                                             spacing=5)
        orgLayout = elements.hBoxLayout(self)
        orgLayout.addWidget(self.orgLb)
        orgLayout.addWidget(self.orgLine)
        orgLayout.addWidget(self.orgBtn)

        skinLayout = elements.hBoxLayout(self)
        skinLayout.addWidget(self.skinLb)
        skinLayout.addWidget(self.skinLine)
        skinLayout.addWidget(self.skinBtn)

        contentsLayout.addLayout(orgLayout)
        contentsLayout.addLayout(skinLayout)
        contentsLayout.addWidget(self.applyBtn)
        contentsLayout.addStretch(1)
