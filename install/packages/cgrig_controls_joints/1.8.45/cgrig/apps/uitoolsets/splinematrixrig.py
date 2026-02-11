#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/10/30 13:36
# @Author : yinyufei
# @File : splinematrixrig.py
# @Project : TeamCode
# -*- coding: utf-8 -*-
from functools import partial
from cgrigvendor.Qt import QtWidgets
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.maya.mayacommand import mayaexecutor as executor
from cgrig.libs.pyqt import uiconstants as uic, utils
from cgrig.core.util import zlogging
from cgrig.libs.utils import output
from cgrig.preferences.core import preference
from maya import cmds
import maya.api.OpenMaya as om2
from cgrig.libs.maya.cmds.meta import metaadditivefk
from cgrig.libs.maya import zapi
from cgrig.libs.maya.cmds.meta import metasplinerig
from cgrig.libs.maya.cmds.meta.metasplinerig import HIERARCHY_SWITCH
from cgrig.libs.maya.meta import base
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.maya.cmds.rig import splinebuilder
from cgrig.libs.maya.cmds.objutils import namehandling, joints, curves, filtertypes, scaleutils
from cgrig.libs.maya.triggers import blockSelectionCallbackDecorator


UP_AXIS_LIST = ["Auto", "+Y", "-Y", "+X", "-X", "+Z", "-Z"]
NEW_SPLINE_RIG = "<New Spline Rig>"


logger = zlogging.getLogger(__name__)


class DotsItems:
    SelectJoints = "Select Joints"
    SelectMeta = "Select Meta Node"
    Separator = "---"
    RebuildBaked = "Rebuild Current Pos"
    Duplicate = "Duplicate Rig"
    DeleteAll = "Delete All"
    ResetSettings = "Reset Settings"
    TogglePublish = "Rig Published"


class SplineMatrixRig(toolsetwidget.ToolsetWidget):
    id = "splineMatrixRig"
    info = "Builds a spline rig with various options"
    uiData = {"label": "Spline Matrix Rig",
              "icon": "splineRig",
              "tooltip": "Builds a spline rig with various options.",
              "defaultActionDoubleClick": False
              }

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        pass
    
    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """

        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = GuiCompact(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def postContentSetup(self):
        """Last of the initialize code"""
        # self.startSelectionCallback()  # start selection callback
        self.uiConnections()

    def currentWidget(self):
        """Returns the current widget class eg. self.compactWidget or self.advancedWidget

        Overridden class

        :return:
        :rtype:  GuiCompact
        """
        return super(SplineMatrixRig, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[GuiCompact]
        """
        return super(SplineMatrixRig, self).widgets()

    # ------------------
    # LOGIC
    # ------------------
    def propertiesToMetaAttr(self):
        """ Convert properties to meta attributes
        """
        self.properties.jointsSplineEdit.data = self.properties.jointsSplineEdit.get("data")

        propText = self.properties.splineCombo.currentText
        text = propText if propText != NEW_SPLINE_RIG else "splineRig"
        specialChars = ['<', '>']
        if any([s in text for s in specialChars]):
            text = "splineRig"  # use default if any special characters found

        return {'name': text,
                'curve': self.properties.jointsSplineEdit.value,
                'rigName': self.properties.jointsSplineEdit.value,
                'controlCount': self.properties.jointCountInt.value,
                'secondaryOrient': self.properties.upAxisCombo.value,
                'world': self.properties.worldCheckbox.value,
                'reverse': self.properties.reverseJointsCheckbox.value,
                'size': self.properties.controlSizeFloat.value,
                'rigType': self.properties.baseRigMode.value,
                'controlSpacing': self.properties.controlSpacingInt.value,
                'addUp': self.properties.addUpCheckbox.value,
                'controlSpacingUp': self.properties.upControlSpacingInt.value,
                'stretch': self.properties.upStretchCheckbox.value,
                'reverseUp': self.properties.upReverseCheckbox.value,
                'rigUpType': self.properties.upMode.value,
                'sinCos': self.properties.ropeSinRotCheckbox.value,
                'rotateAll': self.properties.rotateAllCheckbox.value,
                'rotateGradient': self.properties.gradientRotateCheckbox.value,
                'slide': self.properties.slideCheckbox.value,
                }

    def inputSplineJoints(self):
        """ Input the spline curve so we can generate the joints

        :return:
        :rtype:
        """

        curve = self.selectedCurve()
        if curve:
            self.setJointsCurve(curve)

    def setJointsCurve(self, curve):
        """ Set the curve for the joints on curve mode

        :param curve:
        :type curve:
        :return:
        :rtype:
        """
        self.properties.jointsSplineEdit.value = curve.name()
        self.properties.jointsSplineEdit.data = curve
        self.updateFromProperties()

    def selectedCurve(self, finishedOnly=True):
        """ Get selected curve

        :param finishedOnly: Returns curve only if its finished, if false it may return even if its not finished
        :type finishedOnly:
        :return:
        :rtype:
        """
        selected = list(zapi.selected())
        if len(selected) < 1:
            return
        selection = filtertypes.filterTypeReturnTransforms([selected[-1].fullPathName()], children=False,
                                                           shapeType="nurbsCurve")

        if len(selection) > 0:
            curve = zapi.nodeByName(selection[0])

            numPoints = len(curve.children()[0].attribute('controlPoints'))

            # Always returns if theres a curve and finishedOnly is false or only if the curve is finished
            if finishedOnly and numPoints > 1 or not finishedOnly:
                return curve

    def createCurveContext(self):
        """Enters the create curve context (user draws cvs).  Uses mel hardcoded 3 bezier curve."""
        curves.createCurveContext(degrees=3)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def createCurveChain(self):
        metaAttrs = self.propertiesToMetaAttr()
        self._joints_metaNode = executor.execute("cgrig.maya.jointsOnCurve",
                                                 selected=[zapi.nodeByName(metaAttrs['curve'])],
                                                 jointCount=metaAttrs['controlCount'],
                                                 axis="x",
                                                 secondaryAxisOrient=metaAttrs['secondaryOrient'],
                                                 jointName=metaAttrs['curve'],
                                                 numberPadding=2,
                                                 suffix=True,
                                                 reverseDirection=metaAttrs['reverse'],
                                                 buildMetaNode=True)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def buildRig(self):
        metaAttrs = self.propertiesToMetaAttr()
        self._metaNode = executor.execute("cgrig.maya.roperig.build", metaAttrs=metaAttrs)

    # ------------------
    # CONNECTIONS
    # ------------------
    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.compactWidget.inputJointsSplineBtn.clicked.connect(self.inputSplineJoints)
        self.compactWidget.curveCvBtn.clicked.connect(self.createCurveContext)
        self.compactWidget.createControlChainBtn.clicked.connect(self.createCurveChain)
        self.compactWidget.buildBtn.clicked.connect(self.buildRig)


class GuiWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, uiMode=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc

        :param parent: the parent of this widget
        :type parent: qtObject
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: object
        :param uiMode: 0 is compact ui mode, 1 is advanced ui mode
        :type uiMode: int
        """
        super(GuiWidgets, self).__init__(parent=parent)
        self.properties = properties
        # Titles Dividers ---------------------------------------
        self.controlRigsTitle = elements.LabelDivider(text="Spline Rig Control Sets")
        self.splineControlsTitle = elements.LabelDivider(text="Spline Rig Options")
        self.additiveFkTitle = elements.LabelDivider(text="Additive FK Controls")
        tooltip = "为绑定命名，或重命名已有绑定"
        self.splineCombo = elements.ComboEditRename(label="Spline绑定", labelStretch=5, mainStretch=21,
                                                    primaryTooltip="选择一个现有的Spline绑定",
                                                    toolTip=tooltip)


        self.splineCombo.comboEdit.edit.setAlphanumericValidator()
        toolsetWidget.addExtraProperties(self.splineCombo, ["currentData", "currentText"])
        self.splineCombo.addItem(NEW_SPLINE_RIG)

        tooltip = "控制器大小"
        self.controlSizeFloat = elements.FloatEdit(label="大小",
                                                   editText=1.0,
                                                   toolTip=tooltip,
                                                   editRatio=11,
                                                   labelRatio=6)

        tooltip = ("绑定模式 \n"
                   "分为: ik/fk/ikfk")
        self.baseRigMode = elements.ComboBoxRegular(label="绑定模式",
                                                    items=["IK", "FK", "IK/FK"],
                                                    setIndex=2,
                                                    toolTip=tooltip,
                                                    boxRatio=2,
                                                    labelRatio=1)

        tooltip = "仅为叠加式FK，在每隔N个关节处创建一个控制器。\n" \
                  "示例：值设为3时，将在每第三个关节处创建控制器。"
        self.controlSpacingInt = elements.IntEdit(label="控制器间隔",
                                                  editText=1,
                                                  toolTip=tooltip,
                                                  editRatio=7,
                                                  labelRatio=10)

        self.ropeSinRotCheckbox = elements.CheckBox(label="Sin/Cos Rot",
                                                 toolTip=tooltip,
                                                 checked=False,
                                                 right=True,
                                                 boxRatio=2,
                                                 labelRatio=1)
        self.rotateAllCheckbox = elements.CheckBox(label="整体旋转",
                                                 toolTip=tooltip,
                                                 checked=False,
                                                 right=True,
                                                 boxRatio=2,
                                                 labelRatio=1)
        self.gradientRotateCheckbox = elements.CheckBox(label="渐变旋转",
                                                   toolTip=tooltip,
                                                   checked=False,
                                                   right=True,
                                                   boxRatio=2,
                                                   labelRatio=1)
        self.slideCheckbox = elements.CheckBox(label="滑动控制",
                                                   toolTip=tooltip,
                                                   checked=False,
                                                   right=True,
                                                   boxRatio=2,
                                                   labelRatio=1)

        self.addUpCheckbox = elements.CheckBox(label="添加上层控制",
                                               toolTip=tooltip,
                                               checked=False,
                                               right=True,
                                               boxRatio=2,
                                               labelRatio=1)

        self.upControlSpacingInt = elements.IntEdit(label="控制器间隔",
                                                  editText=1,
                                                  toolTip=tooltip,
                                                  editRatio=7,
                                                  labelRatio=10)
        self.upStretchCheckbox = elements.CheckBox(label="拉伸",
                                                   toolTip=tooltip,
                                                   checked=False,
                                                   right=True,
                                                   boxRatio=2,
                                                   labelRatio=1)
        self.upReverseCheckbox = elements.CheckBox(label="反转",
                                                   toolTip=tooltip,
                                                   checked=False,
                                                   right=True,
                                                   boxRatio=2,
                                                   labelRatio=1)
        self.upMode = elements.ComboBoxRegular(label="上层级模式",
                                               items=["IK", "FK", "IK/FK"],
                                               setIndex=0,
                                               toolTip=tooltip,
                                               boxRatio=2,
                                               labelRatio=1)
        # Build Button ---------------------------------------
        self.buildBtn = elements.styledButton("Build Spline Rig",
                                              icon="splineRig",
                                              style=uic.BTN_DEFAULT)

        # Delete Button ------------------------------------
        self.deleteBtn = elements.styledButton("",
                                               "trash",
                                               parent=self,
                                               minWidth=uic.BTN_W_ICN_MED)

        # Allow the widgets to update for these two when updateFromProperties is run
        self._jointsOnCurveWidgets()

    def _dotsMenuWidget(self):
        THEME_PREFS = preference.interface("core_interface")
        iconColor = THEME_PREFS.ICON_PRIMARY_COLOR
        self.dotsMenu = elements.IconMenuButton(parent=self)
        self.dotsMenu.setIconByName("menudots", size=16, colors=iconColor)
        self.dotsMenu.addAction(DotsItems.SelectJoints, icon="cursorSelect")
        self.dotsMenu.addAction(DotsItems.SelectMeta, icon="cube")
        self.dotsMenu.addSeparator()
        self.dotsMenu.addAction(DotsItems.RebuildBaked, icon="refresh")
        self.dotsMenu.addAction(DotsItems.Duplicate, icon="duplicate")
        self.dotsMenu.addSeparator()
        self.dotsMenu.addAction(DotsItems.DeleteAll, icon="trash")
        self.dotsMenu.addAction(DotsItems.ResetSettings, icon="reload2")
        publishAction = self.dotsMenu.addAction(DotsItems.TogglePublish, icon="reload2", checkable=True, checked=False)
        self.dotsMenu.setProperty("publishAction", publishAction)

    def _jointsOnCurveWidgets(self):
        """ Initialise the start end joints widgets

        :return:
        :rtype:
        """
        tooltip = "该轴为所有关节的次要轴向（关节Y轴朝上）\n" \
                  "主要轴向始终为+X轴（指向相邻的下一个关节）\n\n" \
                  " 「首骨骼」模式会根据第一根骨骼确定次要轴向\n" \
                  " 「首尾骨骼」模式会根据第一根和末根骨骼确定次要轴向"
        self.upAxisCombo = elements.ComboBoxRegular(label="上方向",
                                                    items=joints.UP_VECTOR_POSNEG_LIST + [u"首骨骼", u"首尾骨骼"],
                                                    setIndex=2,
                                                    toolTip=tooltip,
                                                    boxRatio=2,
                                                    labelRatio=1)

        # Joint Count Int ---------------------------------------
        tooltip = "沿该曲线生成的控制器的数量。"
        self.jointCountInt = elements.IntEdit(label="数量",
                                              editText=5,
                                              toolTip=tooltip,
                                              editRatio=11,
                                              labelRatio=6)
        tooltip = "指定一条已存在的曲线"
        self.jointsSplineEdit = elements.StringEdit(label="曲线",
                                                    editPlaceholder="创建曲线并添加到这里",
                                                    editText="",
                                                    toolTip=tooltip,
                                                    editRatio=26,
                                                    labelRatio=7)
        tooltip = "选择一条场景内的曲线"
        self.inputJointsSplineBtn = elements.styledButton("",
                                                          "arrowLeft",
                                                          self,
                                                          toolTip=tooltip,
                                                          style=uic.BTN_TRANSPARENT_BG,
                                                          minWidth=15)
        # Create CV Curve Button ------------------------------------
        toolTip = "创建一条曲线 (模式: 3 Cubic)"
        self.curveCvBtn = elements.styledButton("",
                                                "curveCv",
                                                toolTip=toolTip,
                                                parent=self,
                                                minWidth=uic.BTN_W_ICN_MED)
        # Reverse Direction Checkbox ---------------------------------------
        tooltip = "反转关节的创建方向\n" \
                  "注意：此操作会临时反转曲线方向\n" \
                  "若曲线带有历史记录，请勿启用此选项"
        self.reverseJointsCheckbox = elements.CheckBox(label="反转",
                                                       toolTip=tooltip,
                                                       checked=False,
                                                       right=True,
                                                       boxRatio=2,
                                                       labelRatio=1)
        tooltip = "创建的骨骼轴向是否为世界坐标"
        self.worldCheckbox = elements.CheckBox(label="世界坐标",
                                               toolTip=tooltip,
                                               checked=False,
                                               right=True,
                                               boxRatio=2,
                                               labelRatio=1)
        toolTip = "创建控制器骨骼"
        self.createControlChainBtn = elements.styledButton("创建",
                                                           "",
                                                          toolTip=toolTip,
                                                          parent=self,
                                                          minWidth=uic.BTN_W_REG_SML)


class GuiCompact(GuiWidgets):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Adds the layout building the compact version of the GUI:

        :param parent: the parent of this widget
        :type parent: qtObject
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: list[dict]
        """
        super(GuiCompact, self).__init__(parent=parent, properties=properties,
                                         toolsetWidget=toolsetWidget)
        self.themePref = preference.interface("core_interface")
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(self, margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)

        topLayout = elements.hBoxLayout()
        topLayout.addWidget(self.splineCombo)

        upLayout= elements.hBoxLayout()
        upLayout.addWidget(self.addUpCheckbox)
        upLayout.addWidget(self.upControlSpacingInt)
        upLayout.addWidget(self.upStretchCheckbox)
        upLayout.addWidget(self.upReverseCheckbox)
        upLayout.addWidget(self.upMode)

        snakeLayout = elements.GridLayout()
        r = 0
        snakeLayout.addWidget(self.ropeSinRotCheckbox, r, 0)
        snakeLayout.addWidget(self.rotateAllCheckbox, r, 1)
        r += 1
        snakeLayout.addWidget(self.gradientRotateCheckbox, r, 0)
        snakeLayout.addWidget(self.slideCheckbox, r, 1)


        # Main Layout --------------------------------------
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(elements.Divider())
        mainLayout.addWidget(self._jointsOnCurveWidget())
        mainLayout.addWidget(self.controlRigsTitle)

        settingLayout = elements.hBoxLayout(self)
        settingLayout.addWidget(self.controlSizeFloat)
        settingLayout.addWidget(self.baseRigMode)
        settingLayout.addWidget(self.controlSpacingInt)

        mainLayout.addLayout(settingLayout)
        mainLayout.addLayout(upLayout)
        mainLayout.addLayout(snakeLayout)

        buildLayout = elements.hBoxLayout()
        buildLayout.addWidget(self.buildBtn)
        buildLayout.addWidget(self.deleteBtn)
        mainLayout.addLayout(buildLayout)


    def _jointsOnCurveWidget(self):
        jointsOnCurveWidget = QtWidgets.QWidget(parent=self)
        curveModeLayout = elements.vBoxLayout()
        editLayout = elements.hBoxLayout()
        editLayout.addWidget(self.jointsSplineEdit)
        editLayout.addWidget(self.inputJointsSplineBtn)
        editLayout.addWidget(self.curveCvBtn)
        # Name Layout ---------------------------------------
        nameLayout = elements.hBoxLayout()
        nameLayout.addWidget(self.worldCheckbox, 1)
        nameLayout.addWidget(self.reverseJointsCheckbox, 1)
        nameLayout.addWidget(self.createControlChainBtn)
        # Count Layout ---------------------------------------
        countLayout = elements.hBoxLayout()
        countLayout.addWidget(self.jointCountInt, 1)
        countLayout.addWidget(self.upAxisCombo, 1)
        # Button Layout ---------------------------------------
        curveModeLayout.addLayout(editLayout)
        curveModeLayout.addLayout(countLayout)
        curveModeLayout.addLayout(nameLayout)
        jointsOnCurveWidget.setLayout(curveModeLayout)
        return jointsOnCurveWidget
