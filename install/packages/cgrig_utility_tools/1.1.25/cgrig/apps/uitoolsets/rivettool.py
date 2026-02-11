#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/11/3 18:26
# @Author : yinyufei
# @File : rivettool.py
# @Project : TeamCode
from cgrigvendor.Qt import QtWidgets
from maya import cmds
from maya.api import OpenMaya as om2
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.maya.cmds.rig import follicles


class RivetTool(toolsetwidget.ToolsetWidget):
    id = "rivetTool"
    info = "rivet tools for Maya objects."
    uiData = {"label": "Rivet Tool",
              "icon": "matrix",
              "tooltip": "Rivet tools for Maya objects.",
              "defaultActionDoubleClick": False}

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        self.constraint_type = None
        self.rivet_type = None
        self.create_mid = True
        self.create_plane = False

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = GuiCompact(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiConnections()

    def defaultAction(self):
        """Double Click
        Double clicking the tools toolset icon will run this method
        Be sure "defaultActionDoubleClick": True is set inside self.uiData (meta data of this class)"""
        pass

    def currentWidget(self):
        """ Currently active widget

        :return:
        :rtype: GuiAdvanced or GuiCompact
        """
        return super(RivetTool, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[GuiAdvanced or GuiCompact]
        """
        return super(RivetTool, self).widgets()

    # ------------------
    # LOGIC
    # ------------------
    def createPlane(self, nodes):
        created_planes = []
        merged = None
        try:
            # 1. 在每个选中物体的位置创建polyPlane
            for obj in nodes:
                # 获取物体的世界空间位置
                pos = cmds.xform(obj, query=True, translation=True, worldSpace=True)

                # 创建平面（默认大小1x1，可根据需要调整）
                plane = cmds.polyPlane(width=0.1, height=0.1, ax=(0, 0, 1), subdivisionsX=1, subdivisionsY=1)[0]

                # 将平面移动到选中物体的位置
                cmds.xform(plane, translation=pos, worldSpace=True)

                created_planes.append(plane)

            # 2. 合并所有创建的平面
            if len(created_planes) > 1:
                merged = cmds.polyUnite(created_planes, ch=False)[0]
            else:
                merged = created_planes[0]

            # 3. 自动分UV
            cmds.polyAutoProjection(merged, ch=False)

            # 4. 删除历史记录
            cmds.delete(merged, constructionHistory=True)

            # 5. 冻结变换（重置坐标）
            cmds.makeIdentity(merged, apply=True, translate=True, rotate=True, scale=True)
            cmds.select(clear=True)

        except Exception as e:
            cmds.warning(u"Failed: {}".format(e))

        return merged

    @toolsetwidget.ToolsetWidget.undoDecorator
    def createRivets(self, *args):
        selection = cmds.ls(selection=True)
        if not selection:
            return
        self.constraint_type = self.compactWidget.con_radioBtnGrp.checked().text()
        self.rivet_type = self.compactWidget.typ_radioBtnGrp.checked().text()
        self.create_mid = self.compactWidget.midCheck._checkBox.isChecked()
        self.create_plane = self.compactWidget.planeCheck._checkBox.isChecked()

        rivet_mesh = selection[-1]

        if self.create_plane:
            rivet_mesh = self.createPlane(selection[:-1])
        for obj in selection[:-1]:
            if self.rivet_type == "uvPin":
                follicles.uvPinConstraint(obj, rivet_mesh, constraint=self.constraint_type, createMid=self.create_mid)
            elif self.rivet_type == "follicle":
                follicles.follicleConstraint(obj, rivet_mesh, constraint=self.constraint_type, createMid=self.create_mid)

    def loadVertex(self):
        selection = cmds.ls(selection=True, flatten=True)
        if not selection:
            return
        verticies = []
        for obj in selection:
            sel = om2.MSelectionList()
            sel.add(obj)
            path, component = sel.getComponent(0)
            if not om2.MFnComponent(component).componentType == om2.MFn.kMeshVertComponent:
                continue
            verticies.append(obj)
        if verticies:
            self.compactWidget.loadVertexLe.setText(str(verticies))

    @toolsetwidget.ToolsetWidget.undoDecorator
    def createByVertex(self):
        self.constraint_type = self.compactWidget.con_radioBtnGrp.checked().text()
        self.rivet_type = self.compactWidget.typ_radioBtnGrp.checked().text()
        self.create_mid = self.compactWidget.midCheck._checkBox.isChecked()
        self.create_plane = self.compactWidget.planeCheck._checkBox.isChecked()
        if self.compactWidget.loadVertexLe.text() == "":
            return
        verticies = eval(self.compactWidget.loadVertexLe.text())

        rivet_mesh = verticies[0].split('.')[0]

        if self.create_plane:
            rivet_mesh = self.createPlane(verticies)

        for i,obj in enumerate(verticies):
            pos = cmds.xform(obj, query=True, translation=True, worldSpace=True)
            vert_node = cmds.createNode("transform", name="{}_vert_transform{}".format(rivet_mesh, i))
            cmds.xform(vert_node, translation=pos, worldSpace=True)
            if self.rivet_type == "uvPin":
                follicles.uvPinConstraint(vert_node, rivet_mesh, False, constraint=self.constraint_type,
                                          createMid=self.create_mid)
            elif self.rivet_type == "follicle":
                follicles.follicleConstraint(vert_node, rivet_mesh, constraint=self.constraint_type,
                                             createMid=self.create_mid)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def replaceRivetModel(self):
        follicles.replaceFollicModel()

    # ------------------
    # CONNECTIONS
    # ------------------
    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.compactWidget.createBtn.clicked.connect(self.createRivets)
        self.compactWidget.loadVertexBtn.clicked.connect(self.loadVertex)
        self.compactWidget.vertexBtn.clicked.connect(self.createByVertex)
        self.compactWidget.replaceBtn.clicked.connect(self.replaceRivetModel)


class GuiWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, uiMode=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc

        :param parent: the parent of this widget
        :type parent: QtWidgets.QWidget
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: cgrig.apps.toolsetsui.widgets.toolsetwidget.PropertiesDict
        :param uiMode: 0 is compact ui mode, 1 is advanced ui mode
        :type uiMode: int
        """
        super(GuiWidgets, self).__init__(parent=parent)
        self.con_radioBtnGrp = elements.RadioButtonGroup(radioList=["parent", "point", "orient"],
                                                         default=0,
                                                         margins=(uic.REGPAD, 0, uic.REGPAD, uic.SMLPAD))
        self.typ_radioBtnGrp = elements.RadioButtonGroup(radioList=["follicle", "uvPin"],
                                                         default=1,
                                                         margins=(uic.REGPAD, 0, uic.REGPAD, uic.SMLPAD))
        self.midCheck = elements.CheckBox(label="create mid group", checked=True)
        self.planeCheck = elements.CheckBox(label="create plane", checked=False)
        self.createBtn = elements.styledButton(text="Create", toolTip="Please select objects and rivet mesh.")
        self.replaceBtn = elements.styledButton(text="Replace Rivet Mesh", toolTip="Please select uvPin or follicles and one rivet mesh.")
        self.loadVertexBtn = elements.styledButton(text="Load Mesh Vertices")
        self.loadVertexLe = elements.LineEdit(placeholder="Mesh Vertices")
        self.vertexBtn = elements.styledButton(text="Create",
                                               toolTip="Please select objects and rivet mesh.")

class GuiCompact(GuiWidgets):
    def __init__(self, parent=None, properties=None, uiMode=0, toolsetWidget=None):
        """Adds the layout building the compact version of the GUI:

            default uiMode - 0 is advanced (UI_MODE_COMPACT)

        :param parent: the parent of this widget
        :type parent: QtWidgets.QWidget
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: cgrig.apps.toolsetsui.widgets.toolsetwidget.PropertiesDict
        """
        super(GuiCompact, self).__init__(parent=parent, properties=properties, uiMode=uiMode,
                                         toolsetWidget=toolsetWidget)
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(self, margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)
        conTypeLay = elements.hBoxLayout()
        conTypeLay.addWidget(self.con_radioBtnGrp)
        rivetTypeLay = elements.hBoxLayout()
        rivetTypeLay.addWidget(self.typ_radioBtnGrp)
        rivetTypeLay.addWidget(self.midCheck)
        rivetTypeLay.addWidget(self.planeCheck)
        vertexLay = elements.hBoxLayout()
        vertexLay.addWidget(self.loadVertexBtn)
        vertexLay.addWidget(self.loadVertexLe)
        vertexLay.addWidget(self.vertexBtn)
        # Add To Main Layout ---------------------------------------
        mainLayout.addWidget(elements.LabelDivider("Constraint Type"))
        mainLayout.addLayout(conTypeLay)
        mainLayout.addWidget(elements.LabelDivider("Rivet Type"))
        mainLayout.addLayout(rivetTypeLay)
        mainLayout.addWidget(self.createBtn)
        mainLayout.addWidget(elements.LabelDivider("Select Vertex"))
        mainLayout.addLayout(vertexLay)
        mainLayout.addWidget(self.replaceBtn)

