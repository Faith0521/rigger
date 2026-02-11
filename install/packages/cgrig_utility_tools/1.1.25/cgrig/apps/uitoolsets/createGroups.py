# -*- coding: utf-8 -*-
"""
@Author: Faith
@Date: 2025/10/8
@Time: 10:47
@Description:
@FilePath: createGroups.py
"""
from functools import partial
from Qt import QtWidgets
from maya import cmds
import cgrig.libs.pyqt.extended.lineedit
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.maya import zapi
from cgrig.libs.maya.cmds.animation import resetattrs
from cgrig.libs.pyqt.widgets import elements


class CgRigAddGroup(toolsetwidget.ToolsetWidget):
    id = "cgrigAddGroup"
    uiData = {"label": "CgRig AddGroup",
              "icon": "addThumbnail",
              "tooltip": "Tools For Group Objects",
              "defaultActionDoubleClick": False
              }
    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run"""
        self.widgets_all = []
        self.add_names = []

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = AddGroupCompactWidget(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def currentWidget(self):
        """ Current active widget

        :return:
        :rtype:  :class:`AddGroupWidgets`
        """
        return super(CgRigAddGroup, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[:class:`AddGroupCompactWidget` or :class:`AddGroupAdvancedWidget`]
        """
        return super(CgRigAddGroup, self).widgets()

    def postContentSetup(self):
        self.setFixedHeight(400)
        self.connectionsAddGroup()

    # ------------------
    # CORE LOGIC
    # ------------------
    def get_all_widgets_in_layout(self, layout):
        """
        获取布局中所有的QWidget（包括子布局中的部件）

        参数:
            layout: 要遍历的布局

        返回:
            包含所有QWidget的列表
        """
        widgets = []

        if layout is None:
            return widgets

        # 遍历布局中的所有项目
        for i in range(layout.count()):
            item = layout.itemAt(i)

            # 如果是Widget项
            if item.widget():
                if type(item.widget()) == cgrig.libs.pyqt.extended.lineedit.LineEdit:
                    widgets.append(item.widget())

        return widgets

    def addLabelText(self, mode=0):
        self.widgets_all = self.get_all_widgets_in_layout(self.compactWidget.labelLayout)
        if mode == 0:
            if self.widgets_all:
                self.widgets_all[-1].deleteLater()
        else:
            forceRenameTxt = elements.LineEdit(text="",
                                                placeholder="Force Name",
                                                parent=self)
            forceRenameTxt.setFixedHeight(30)
            self.compactWidget.labelLayout.addWidget(forceRenameTxt)

    def GrpAdd(self, Obj, GrpNames, addgrpRelativeTier):
        """
        添加层级组结构

        :param Obj: 目标对象
        :param GrpNames: 组名称列表
        :param addgrpRelativeTier: 组添加方向 ('Up' 向上层级, 'Dn' 向下层级)
        :return: 新建的组列表
        """
        # 获取对象父级
        obj_parent = cmds.listRelatives(Obj, p=True, f=True)

        # 反转组名称列表以便从内向外创建
        reversed_grp_names = GrpNames[::-1]
        created_groups = []

        # 创建组结构
        for idx, grp_name in enumerate(reversed_grp_names):
            # 检查组是否已存在
            if cmds.objExists(grp_name):
                cmds.warning("{} ------ 已存在".format(grp_name))

            # 创建空组或普通组
            if idx == 0:
                new_group = cmds.group(em=True)
            else:
                new_group = cmds.group()

            created_groups.append(new_group)

        # 调整组顺序并获取顶层和底层组
        created_groups = created_groups[::-1]
        top_group = created_groups[0]
        end_group = created_groups[-1]

        # 设置组的父子关系
        cmds.parent(top_group, Obj)
        resetattrs.resetNodes([top_group])  # 假设resetNodes是已定义的函数

        # 根据方向参数处理层级关系
        if addgrpRelativeTier == 'Up':
            # 向上层级: 将顶层组移至世界空间或原父级下
            cmds.parent(top_group, w=True)
            if obj_parent:
                cmds.parent(top_group, obj_parent[0])
            # 将原始对象移至最底层组
            cmds.parent(Obj, end_group)
        elif addgrpRelativeTier == 'Dn':
            # 向下层级: 可在此添加具体逻辑
            pass

        # 重命名组并调整选择顺序
        created_groups = created_groups
        cmds.select(created_groups, add=True)

        # 应用用户指定的组名称
        for group, name in zip(created_groups, GrpNames):
            cmds.rename(group, name)

        # 返回重命名后的组列表
        return cmds.ls(sl=True)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def createGroup(self):
        self.add_names = []
        if not zapi.selected():
            return
        self.widgets_all = self.get_all_widgets_in_layout(self.compactWidget.labelLayout)
        mode = self.compactWidget.optionsRadio.checked().text()
        if self.widgets_all:
            for widget in self.widgets_all:
                self.add_names.append(widget.value())

        for sel in zapi.selected():
            grps = ["{}{}".format(sel.name(), name) for name in self.add_names]
            self.GrpAdd(sel.name(), grps, mode)
        cmds.select(clear=True)
    # ------------------
    # CONNECTIONS
    # ------------------

    def connectionsAddGroup(self):
        """Connects up the buttons to the CgRig AddGroup logic """
        self.compactWidget.removeGrpBtn.clicked.connect(partial(self.addLabelText, mode=0))
        self.compactWidget.addGrpBtn.clicked.connect(partial(self.addLabelText, mode=1))
        self.compactWidget.createBtn.clicked.connect(self.createGroup)


class AddGroupWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc

        :param parent: the parent of this widget
        :type parent: CgRigAddGroup
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: object
        :param uiMode: 0 is compact ui mode, 1 is advanced ui mode
        :type uiMode: int
        """
        super(AddGroupWidgets, self).__init__(parent=parent)

        self.toolsetWidget = toolsetWidget
        self.properties = properties
        # Top Radio Buttons ------------------------------------
        radioNameList = ["Up", "Dn"]
        radioToolTipList = ["Create groups upward based on the selected objects.",
                            "Create groups downward  based on the selected objects."]
        self.optionsRadio = elements.RadioButtonGroup(radioList=radioNameList, toolTipList=radioToolTipList,
                                                      default=0, parent=parent)
        add_toolTip = ""
        remove_toolTip = ""
        self.addGrpBtn = elements.styledButton("",
                                               "boxAdd",
                                               toolTip=add_toolTip,
                                               parent=self,
                                               minWidth=uic.BTN_W_ICN_MED)
        self.removeGrpBtn = elements.styledButton("",
                                               "boxRemove",
                                               toolTip=remove_toolTip,
                                               parent=self,
                                               minWidth=uic.BTN_W_ICN_MED)
        self.addGrpBtn.setFixedWidth(uic.BTN_W_ICN_MED)
        self.removeGrpBtn.setFixedWidth(uic.BTN_W_ICN_MED)
        self.labelDriver = elements.LabelDivider("Group Suffix Name")
        self.forceRenameTxt1 = elements.LineEdit(text="_zero",
                                                placeholder="Force Name",
                                                parent=parent)
        self.forceRenameTxt1.setFixedHeight(30)
        self.forceRenameTxt2 = elements.LineEdit(text="_sdk",
                                                 placeholder="Force Name",
                                                 parent=parent)
        self.forceRenameTxt2.setFixedHeight(30)
        self.createBtn = QtWidgets.QPushButton("Create",self)


class AddGroupCompactWidget(AddGroupWidgets):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Adds the layout building the advanced version of the directional light UI:

            default uiMode - 1 is advanced (UI_MODE_ADVANCED)

        :param parent: the parent of this widget
        :type parent: qtObject
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: list[dict]
        """
        super(AddGroupCompactWidget, self).__init__(parent=parent, properties=properties,
                                                   toolsetWidget=toolsetWidget)
        # Main Layout ------------------------------------
        contentsLayout = elements.vBoxLayout(self,
                                             margins=(uic.WINSIDEPAD,
                                                      0,
                                                      uic.WINSIDEPAD,
                                                      uic.WINBOTPAD),
                                             spacing=uic.SREG)
        self.typeLayout = elements.hBoxLayout(spacing=0)
        self.typeLayout.addWidget(self.addGrpBtn)
        self.typeLayout.addItem(elements.Spacer(uic.SREG, uic.SREG))
        self.typeLayout.addWidget(self.removeGrpBtn)
        self.typeLayout.addItem(elements.Spacer(1, uic.SREG))
        self.typeLayout.addWidget(self.optionsRadio)
        self.labelLayout = elements.vBoxLayout(spacing=5)
        self.labelLayout.addWidget(self.labelDriver)
        self.labelLayout.addWidget(self.forceRenameTxt1)
        self.labelLayout.addWidget(self.forceRenameTxt2)
        contentsLayout.addLayout(self.typeLayout)
        contentsLayout.addLayout(self.labelLayout)
        contentsLayout.addWidget(self.createBtn)
        contentsLayout.addStretch(1)