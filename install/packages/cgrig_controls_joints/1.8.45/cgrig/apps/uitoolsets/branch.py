# -*- coding: utf-8 -*-
""" ---------- Toolset Boiler Plate (Single Mode) -------------
The following code is a template (boiler plate) for building Zoo Toolset GUIs that have a single mode.

A single mode means there is no compact and medium or advanced modes.

"""
from functools import partial
from cgrigvendor.Qt import QtWidgets, QtCore, QtGui
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt.widgets.elements import (hBoxLayout, vBoxLayout, LineEdit,
                                              CheckBox, ComboBoxRegular, IntLineEdit,
                                              styledButton, FloatEdit, Label)
from cgrig.libs import iconlib
from cgrig.libs.naming import naming
from cgrig.libs.pyqt.extended import treeviewplus
from cgrig.libs.pyqt.models import treemodel
from cgrig.libs.maya.cmds.objutils import attributes
from cgrig.libs.maya.api import plugs
from cgrig.libs.maya.cmds.objutils import filtertypes
from cgrig.libs.maya.cmds.objutils import namehandling as names
from cgrig.libs.pyqt.models import datasources
from cgrig.libs.maya.cmds.objutils import matrix
from cgrig.libs.maya.cmds.objutils import matching
from cgrig.libs.maya.cmds.rig import controls, controlconstants
# from cgrig.libs import branch_api
from maya import cmds
import string


class BranchNameDataSource(datasources.BaseDataSource):

    def __init__(self, label, headerText=None, model=None, parent=None):
        super(BranchNameDataSource, self).__init__(headerText, model, parent)
        self._name = label

    def data(self, index):
        return self._name

    def isEditable(self, index):
        return False


class BranchGUI(toolsetwidget.ToolsetWidget):
    id = "branchTool"
    info = "Create Helper Joint Settings GUI."
    uiData = {"label": "Branch Joint Tool",
              "icon": "jointA",
              "tooltip": "Create Branch Joint Settings GUI.",
              "defaultActionDoubleClick": False}

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        self.toolsetWidget = self
        self.scale_fraction = 1.0

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced, in this case we are only building one UI mode """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        parent = QtWidgets.QWidget(parent=self)
        self.widgetsAll(parent)
        self.allLayouts(parent)
        self.refreshList()
        return parent

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiConnections()

    def defaultAction(self):
        """Double Click
        Double clicking the tools toolset icon will run this method
        Be sure "defaultActionDoubleClick": True is set inside self.uiData (meta data of this class)"""
        pass

    # ------------------
    # UI WIDGETS
    # ------------------

    def widgetsAll(self, parent):
        """Create all widgets for the GUI here

        See elements.py for all available widgets in the Zoo PySide framework.
        cgrig_pyside repo then cgrig.libs.pyqt.widgets.elements

        :param parent: The parent widget
        :type parent: obj
        """
        self.centralwidget = QtWidgets.QWidget()
        self.LoadPb = styledButton(u"加载骨骼",
                                   style=uic.BTN_DEFAULT,
                                   parent=self)
        self.LoadPb.setEnabled(True)
        self.LoadLe = LineEdit(parent=self)
        self.LoadLe.setReadOnly(True)
        self.ParentPb = styledButton(u"父骨骼",
                                     style=uic.BTN_DEFAULT,
                                     parent=self)
        self.ParentLe = LineEdit(parent=self)
        self.ParentLe.setReadOnly(True)
        self.RoCombo = ComboBoxRegular(label=u"骨骼轴向",
                                      items=["x", "y", "z"],
                                      setIndex=0,
                                      boxRatio=2,
                                      labelRatio=1)
        self.RoCombo.setEditable(False)
        self.moveAx_cb = ComboBoxRegular(label="位移轴向",
                                      items=["x", "y", "z"],
                                      setIndex=0,
                                      boxRatio=2,
                                      labelRatio=1)
        self.moveAx_cb.setEditable(False)
        self.moveAx_cb.setCurrentText('y')
        self.SizeSp = FloatEdit(label=u"大小",
                               editText=1.0,
                               editRatio=2,
                               labelRatio=1)
        self.DisSp = FloatEdit(label=u"距离",
                                editText=6.0,
                                editRatio=2,
                                labelRatio=1)
        self.numLabel = Label(u"数量")
        self.NumSp = IntLineEdit(text=u"4", editWidth=60)
        self.jntChain_cb = CheckBox(label="骨骼链",
                                    checked=False)
        self.NetView = treeviewplus.TreeViewPlus(parent=self, title='Existing')
        self.NetView.treeView.setHeaderHidden(True)
        self.rootSource = BranchNameDataSource("")
        self.NetView_model = treemodel.TreeModel(self.rootSource, parent=self)
        self.NetView.setModel(self.NetView_model)
        self.NetView.setSearchable(False)
        self.NetView.setMinimumHeight(400)

        self.RefreshPb = styledButton(u"刷新",
                                      style=uic.BTN_DEFAULT,
                                      icon="refresh",
                                      parent=self)
        self.ApplyPb = styledButton(u"创建",
                                      style=uic.BTN_DEFAULT,
                                      icon="plus",
                                      parent=self)
        self.MirrorPb = styledButton(u"镜像",
                                      style=uic.BTN_DEFAULT,
                                      icon="mirrorComponent",
                                      parent=self)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menuTool = self.menubar.addMenu(u'工具')
        self.actionExport_All_Settings = QtWidgets.QAction(u'导出所有')
        self.actionImport_Settings = QtWidgets.QAction(u'导入')
        self.actionCreate_AdvSettings = QtWidgets.QAction(u'创建adv设置')
        self.actionCreate_TimelineSettings = QtWidgets.QAction(u'创建timeline设置')
        self.menuTool.addAction(self.actionExport_All_Settings)
        self.menuTool.addAction(self.actionImport_Settings)
        self.menuTool.addAction(self.actionCreate_AdvSettings)
        self.menuTool.addAction(self.actionCreate_TimelineSettings)
        # self.menubar.addAction(self.menuTool.menuAction())

    # ------------------
    # UI Layouts
    # ------------------

    def allLayouts(self, parent):
        """Builds the layout for the GUI.  Builds all qt layouts and adds all widgets

        :param parent: the parent widget
        :type parent: obj
        """
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(parent, margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)
        mainLayout.addWidget(self.centralwidget)
        self.verticalLayout = vBoxLayout()

        self.LoadHz = hBoxLayout()
        self.LoadHz.addWidget(self.LoadPb)
        self.LoadHz.addWidget(self.LoadLe)
        self.LoadHz.addWidget(self.ParentPb)
        self.LoadHz.addWidget(self.ParentLe)
        self.verticalLayout.addLayout(self.LoadHz)

        self.AxisHz = hBoxLayout()
        self.AxisHz.addWidget(self.RoCombo)
        self.AxisHz.addWidget(self.moveAx_cb)
        self.AxisHz.addWidget(self.SizeSp)
        self.AxisHz.addWidget(self.DisSp)
        self.AxisHz.addWidget(self.numLabel)
        self.AxisHz.addWidget(self.NumSp)
        self.AxisHz.addWidget(self.jntChain_cb)
        self.verticalLayout.addLayout(self.AxisHz)

        self.verticalLayout.addWidget(self.NetView)

        self.CreateHz = hBoxLayout()
        self.CreateHz.addWidget(self.RefreshPb)
        self.CreateHz.addWidget(self.ApplyPb)
        self.CreateHz.addWidget(self.MirrorPb)
        self.verticalLayout.addLayout(self.CreateHz)

        self.verticalLayout.setMenuBar(self.menubar)
        self.centralwidget.setLayout(self.verticalLayout)

    # ------------------
    # LOGIC
    # ------------------
    @property
    def UIDict(self):
        uiDict = {
            "loadJoint": self.LoadLe.text(),
            "parentJoint": self.ParentLe.text(),
            "axis": self.RoCombo.currentIndex(),
            "translate_axis": self.moveAx_cb.currentIndex(),
            "translate_distance": self.DisSp.value(),
            "size": self.SizeSp.value(),
            "isJointChain": self.jntChain_cb.isChecked(),
            "number": self.NumSp.value(),
        }
        return uiDict
    
    
    def loadJoint(self, ui, *args):
        """
        Load Selected Joint.
        :param ui: ui to setText.
        :param args:
        :return:
        """
        selection = cmds.ls(selection=True)
        if not selection or len(selection) > 1:
            cmds.warning("Please select one joint to add corrective network.")
            return
        if cmds.objectType(selection[0]) != "joint":
            raise TypeError("Select object type is not the joint.")
        ui.setText(selection[0])

    def addHelperJoint(self, AddJoint, ParentJoint, primaryAxis=0, translate_axis=1, size=1.0, distance=6.0, names=None, isJointChain=False, mirror=False):
        """
        Create helper joints by ui settings.
        :param AddJoint:
        :param ParentJoint:
        :param primaryAxis:
        :param size:
        :param number:
        :param isJointChain:
        :param mirror:
        :param name:
        :return:
        """
        if names is None:
            names = list()
        BranchSystem = "BranchSystem"
        helperGrp = "{}_HelperGrp".format(AddJoint)
        net_node = "{}_net".format(AddJoint)
        self.scale_fraction = 1.0

        # 创建辅助骨骼设置大组
        if not cmds.objExists(BranchSystem):
            BranchSystem = cmds.createNode("transform", n=BranchSystem)
            BranchController = cmds.createNode("transform", n="BranchController", p=BranchSystem)

        # 创建helper的grp,给bridge组创建属性,记录信息
        if not cmds.objExists(helperGrp):
            helperGrp = cmds.createNode("transform", name=helperGrp)
            if cmds.objExists("BranchController"): cmds.parent(helperGrp, "BranchController")

        if not cmds.objExists(net_node):
            net_node = cmds.createNode("network", name=net_node)
            attributes.createAttribute(net_node, "branchNode", attributeType="bool", channelBox=True, nonKeyable=True,
                                       defaultValue=1)
            attributes.createAttribute(net_node, "helperGroup", attributeType="message", channelBox=True, nonKeyable=True)
            attributes.createAttribute(net_node, "rootMatrix", attributeType="matrix", channelBox=True, nonKeyable=True)
            attributes.createAttribute(net_node, "fatherMatrix", attributeType="matrix", channelBox=True,
                                       nonKeyable=True)
            attributes.createAttribute(net_node, "jointChain", attributeType="bool", channelBox=True, defaultValue=isJointChain,
                                       nonKeyable=True)
            attributes.createAttribute(net_node, "branchSkinJoints", attributeType="message", channelBox=True, nonKeyable=True,
                                       multi=1)
            attributes.createAttribute(net_node, "controls", attributeType="message", channelBox=True, nonKeyable=True,
                                       multi=1)
            attributes.createAttribute(net_node, "roots", attributeType="message", channelBox=True, nonKeyable=True,
                                       multi=1)
            attributes.createEnumAttrList(net_node, "axis", ["x", "y", "z"], channelBox=True, nonKeyable=True,
                                          defaultValue=primaryAxis)
            attributes.createEnumAttrList(net_node, "translate_axis", ["x", "y", "z"], channelBox=True, nonKeyable=True,
                                          defaultValue=translate_axis)
            attributes.createAttribute(net_node, "distance", attributeType="double", channelBox=True, nonKeyable=True,
                                       defaultValue=distance)
            attributes.createAttribute(net_node, "size", attributeType="double", channelBox=True, nonKeyable=True,
                                       defaultValue=self.scale_fraction*size)

            cmds.connectAttr("{}.message".format(helperGrp), "{}.helperGroup".format(net_node), f=True)
            cmds.connectAttr("{}.worldMatrix[0]".format(AddJoint), "{}.rootMatrix".format(net_node), f=True)
            cmds.connectAttr("{}.worldMatrix[0]".format(ParentJoint), "{}.fatherMatrix".format(net_node), f=True)

        # 查找所有连接的root组
        add_roots = []
        roots = cmds.listConnections("{}.roots".format(net_node), source=True, destination=False) or []
        for i,name in enumerate(names):
            if not mirror:
                for root in roots:
                    if name in root:
                        name += "_{}".format(i)
            root_settings = self.createRootSettings(net_node, name)
            add_roots.append(root_settings["root"])
            if not root_settings:
                return
            cmds.parent(root_settings["root"], helperGrp)
            rotate_value = i*(360.0/len(names))
            cmds.setAttr("%s.r%s" % (root_settings["ctrlSdk2Zero"], cmds.getAttr("{}.axis".format(net_node), asString=True)), rotate_value)
            cmds.setAttr("%s.t%s" % (root_settings["ctrlZero"], cmds.getAttr("{}.translate_axis".format(net_node), asString=True)), distance)

            if isJointChain:  # p骨骼链
                branch_jnts = cmds.listConnections("{}.branchSkinJoints".format(net_node), source=True,
                                                   destination=False) or []
                skin_jnt_name = "{}_skin_jnt".format(name)
                if not cmds.objExists(skin_jnt_name):
                    skin_jnt = cmds.createNode("joint", name=skin_jnt_name, p=root_settings["joint"])
                    cmds.parent(skin_jnt, AddJoint)
                    cmds.parentConstraint(root_settings["joint"], skin_jnt, mo=True)
                    cmds.scaleConstraint(root_settings["joint"], skin_jnt, mo=True)
                    cmds.connectAttr("{}.message".format(skin_jnt),
                                     "{0}.branchSkinJoints[{1}]".format(net_node, len(branch_jnts)), f=True)

                cmds.connectAttr("{}.message".format(skin_jnt_name), "{}.branch_jnt".format(root_settings["root"]),
                                 f=True)
            else:
                cmds.connectAttr("{}.message".format(root_settings["joint"]), "{}.branch_jnt".format(root_settings["root"]),
                                 f=True)
        return add_roots

    def createRootSettings(self, net_node, name):
        addJoint = cmds.listConnections("{}.rootMatrix".format(net_node), source=True, destination=False)[0]
        Controls = cmds.listConnections("{}.controls".format(net_node), source=True, destination=False) or []
        current_size = cmds.getAttr("{}.size".format(net_node))
        control_scale = current_size * 0.5

        root_name = "{}_root".format(name)
        if cmds.objExists(root_name):
            return {}
        root = cmds.createNode("transform", n="{}_root".format(name))
        attributes.createAttribute(root, "zeroGrp", attributeType="message", channelBox=True, nonKeyable=True)
        attributes.createAttribute(root, "baseZeroGrp", attributeType="message", channelBox=True, nonKeyable=True)
        attributes.createAttribute(root, "control", attributeType="message", channelBox=True, nonKeyable=True)
        attributes.createAttribute(root, "branch_jnt", attributeType="message", channelBox=True, nonKeyable=True)
        cmds.parent(root, "BranchController")

        # 把创建的root组连接到network节点上
        plug = plugs._getPlug("{}.roots".format(net_node))  # 需提前定义plugs模块，用于属性操作
        # 2. 找到"coordinate"数组的下一个可用索引（避免覆盖已有元素）
        nextIndex = plugs.getNextAvailableElement(plug)
        cmds.connectAttr(root + ".message", nextIndex, f=True)
        matching.matchCgRigAlSimpErrConstrain(addJoint, root)  # 匹配骨骼位置

        father = cmds.createNode("transform", n="{}_father".format(name), p=root)  # 最外层链接的组
        origin = cmds.createNode("transform", n="{}_origin".format(name), p=root)  # 用来做旋转约束跟随的组

        # 创建控制器和上层组
        ctrlSdk2Zero = cmds.createNode("transform", n="{}_base_zero".format(name))
        ctrlSdk2 = cmds.createNode("transform", n="{}_base_sdk".format(name), p=ctrlSdk2Zero)
        ctrlZero = cmds.createNode("transform", n="{}_zero".format(name), p=ctrlSdk2)
        ctrlSdk = cmds.createNode("transform", n="{}_sdk".format(name), p=ctrlZero)
        Control = controls.createControlCurve(folderpath="",
                                              ctrlName="{}_ctrl".format(name),
                                              curveScale=[control_scale]*3,
                                              designName=controlconstants.CTRL_SPHERE,
                                              addSuffix=False,
                                              shapeParent=None,
                                              rotateOffset=(0.0, 0.0, 0.0),
                                              trackScale=True,
                                              lineWidth=-1,
                                              rgbColor=[0.1, 0.3, 1.0],
                                              addToUndo=True)[0]
        cmds.connectAttr("{}.message".format(ctrlSdk2Zero), "{}.baseZeroGrp".format(root), f=True)
        cmds.connectAttr("{}.message".format(ctrlZero), "{}.zeroGrp".format(root), f=True)
        cmds.connectAttr("{}.message".format(Control), "{}.control".format(root), f=True)
        Control = Control.split('|')[-1]
        cmds.connectAttr("{}.message".format(Control), "{0}.controls[{1}]".format(net_node, len(Controls)), f=True)
        attributes.createAttribute(Control, "follow", attributeType="double", channelBox=True,
                                   nonKeyable=False, minValue=0, maxValue=10, defaultValue=5)
        cmds.parent(Control, ctrlSdk)

        # 创建骨骼
        jnt = cmds.createNode("joint", n="{}_jnt".format(name), p=Control)
        matching.matchCgRigAlSimpErrConstrain(origin, ctrlSdk2Zero)
        cmds.parent(ctrlSdk2Zero, origin)

        # 矩阵约束
        self.buildConstraint("{}.rootMatrix".format(net_node), root)
        self.buildConstraint("{}.fatherMatrix".format(net_node), father)

        multDiv = cmds.createNode("multDoubleLinear", n="{0}_offset_mult".format(Control))
        cmds.connectAttr("{0}.follow".format(Control), "{0}.input1".format(multDiv), f=True)
        cmds.setAttr("{0}.input2".format(multDiv), 0.1)

        offset_plus = cmds.createNode("plusMinusAverage", n="{0}_offset_plus".format(Control))
        cmds.setAttr("{0}.operation".format(offset_plus), 2)
        cmds.setAttr("{0}.input1D[0]".format(offset_plus), 1)
        cmds.connectAttr("{0}.output".format(multDiv), "{0}.input1D[1]".format(offset_plus), f=True)

        # 旋转约束跟随一半
        orc = cmds.parentConstraint(father, root, origin, mo=True)[0]
        orc = cmds.rename(orc, "{0}_orc".format(origin))
        cmds.setAttr("{0}.interpType".format(orc), 2)
        cmds.connectAttr("{0}.output".format(multDiv), "{0}.w0".format(orc), f=True)
        cmds.connectAttr("{0}.output1D".format(offset_plus), "{0}.w1".format(orc), f=True)

        return {"joint": jnt,
                "root": root,
                "father": father,
                "origin": origin,
                "ctrlSdk2Zero": ctrlSdk2Zero,
                "control": Control,
                "ctrlZero": ctrlZero}


    def buildConstraint(self, target_attr, aim, T=True, R=True, S=True):
        target = cmds.listConnections(target_attr, source=True, destination=False) or []
        if not target:
            return False
        parentMult = cmds.createNode("multMatrix", n="{}_parentMM".format(aim))
        father_ma = cmds.getAttr(target_attr)
        parent_RevMatrix = cmds.getAttr("{0}.worldInverseMatrix[0]".format(target[0]))
        cmds.setAttr(parentMult + ".matrixIn[0]", matrix.multiply_matrices(father_ma, parent_RevMatrix), type="matrix")

        cmds.connectAttr(target_attr, parentMult + ".matrixIn[1]", f=True)
        cmds.connectAttr("{}.parentInverseMatrix[0]".format(aim), "{}.matrixIn[2]".format(parentMult))
        parentDecomp = cmds.createNode("decomposeMatrix", n="{}_parentDPM".format(aim))
        cmds.connectAttr(parentMult + ".matrixSum", parentDecomp + ".inputMatrix")
        if T:
            cmds.connectAttr("{}.outputTranslate".format(parentDecomp), "{}.translate".format(aim))

        if S:
            cmds.connectAttr("{}.outputScale".format(parentDecomp), "{}.scale".format(aim))

        if R:
            fa_quatPr = cmds.createNode("quatProd", n="{}_quatPr".format(aim))
            cmds.connectAttr("{}.outputQuat".format(parentDecomp), "{}.input1Quat".format(fa_quatPr))
            cmds.setAttr("{}.input2QuatW".format(fa_quatPr), 1)

            fa_quatEu = cmds.createNode("quatToEuler", n="{}_quatEu".format(aim))
            cmds.connectAttr("{}.outputQuat".format(fa_quatPr), "{}.inputQuat".format(fa_quatEu))
            cmds.connectAttr("{}.rotateOrder".format(aim), "{}.inputRotateOrder".format(fa_quatEu))
            cmds.connectAttr("{}.outputRotate".format(fa_quatEu), "{}.rotate".format(aim))

    @toolsetwidget.ToolsetWidget.undoDecorator
    def Generate(self, add=False, *args):
        # ui info-----------------------------
        uiDict = self.UIDict
        destinations = cmds.listConnections("{}.worldMatrix[0]".format(uiDict["loadJoint"]), source=True, destination=True, type="network")
        roots = []
        if destinations:
            roots = cmds.listConnections("{}.roots".format(destinations[0]), source=True, destination=False) or []
        prefix_names = []
        if uiDict['number'] == 1:
            prefix_names = [elements.MessageBox.inputDialog(title="Name",
                                                         text="{}_{}_branch".format(uiDict["loadJoint"], string.ascii_uppercase[len(roots)]),
                                                         parent=None, message='Set Name')]
            distance = 0
        else:
            for i in range(uiDict['number']):
                prefix_names.append("{}_{}_branch".format(uiDict["loadJoint"], string.ascii_uppercase[len(roots) + i]))
            distance = uiDict['translate_distance']

        # branch_net = branch_api.BranchNode.create(name=uiDict["loadJoint"] + "_net")
        self.addHelperJoint(uiDict["loadJoint"], uiDict["parentJoint"], primaryAxis=uiDict["axis"],
                            size=uiDict["size"], translate_axis=uiDict["translate_axis"], distance=distance,
                            isJointChain=uiDict["isJointChain"], names=prefix_names)
        # cmds.select(branch_net)
        self.refreshList()

    def refreshList(self):
        self.NetView_model.beginResetModel()
        if self.NetView_model.root.rowCount() > 0:
            self.NetView_model.root.removeRowDataSources(0, self.NetView_model.root.rowCount())
        self.NetView_model.endResetModel()
        branchNetList = [obj for obj in cmds.ls(type="network") if cmds.objExists(obj + ".branchNode")]
        if not branchNetList: return
        parentItem = self.NetView_model.root
        for i,net in enumerate(branchNetList):
            rootList = cmds.listConnections("{}.roots".format(net), s=True, d=False) or []
            netItem = BranchNameDataSource(label=net, model=self.NetView_model, parent=parentItem)
            parentItem.addChild(netItem)
            for root in rootList:
                rootSource = BranchNameDataSource(label=root, model=self.NetView_model, parent=parentItem)
                netItem.addChild(rootSource)
        self.NetView_model.reload()
        # self.NetView.expandAll()

    def viewItemClick(self, *args):
        if self.NetView.treeView.selectedIndexes():
            cmds.select(d=1)
            for i in range(len(self.NetView.treeView.selectedIndexes())):
                itemName = self.NetView.treeView.selectedIndexes()[i].data()
                if cmds.objExists(itemName):
                    cmds.select(itemName, add=True)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def deleteSetting(self, *args):
        if not self.NetView.selectedItems():
            return
        for i in range(len(self.NetView.selectedItems())):
            selected_node = self.NetView.selectedItems()[i].data(0)
            if cmds.objExists(selected_node) and cmds.objectType(selected_node) == "network":
                helper_grp = cmds.listConnections("{}.helperGroup".format(selected_node)) or []
                net_data = self.getNodeData(selected_node)
                for root in net_data["roots"]:
                    joints = cmds.listConnections("{}.branch_jnt".format(root), source=True, destination=False,
                                                  type="joint") or []
                    cmds.delete(joints)
                cmds.delete(helper_grp[0]) if cmds.objExists(helper_grp[0]) else None
            else:
                joints = cmds.listConnections("{}.branch_jnt".format(selected_node), source=True, destination=False, type="joint") or []
                cmds.delete(joints)
                cmds.delete(selected_node) if cmds.objExists(selected_node) else None
        self.refreshList()

    @toolsetwidget.ToolsetWidget.undoDecorator
    def mirrorSetting(self, *args):
        net_nodes = []
        mirror_roots = []
        for i in range(len(self.NetView.selectedItems())):
            selected_node = self.NetView.selectedItems()[i].data(0)
            if cmds.objExists(selected_node) and cmds.objectType(selected_node) == "network":
                net_nodes.append(selected_node)
            else:
                cmds.warning(u"请选择network节点来镜像")
                return False
        if not net_nodes:
            return
        for net in net_nodes:
            data = self.getNodeData(net)
            mirror_add_joint = naming.convertRLName(data['addJoint'])
            mirror_parent_joint = naming.convertRLName(data['parentJoint'])
            if data['addJoint'] != mirror_add_joint:
                if not cmds.objExists(mirror_add_joint) or not cmds.objExists(mirror_parent_joint):
                    continue
                mirror_names = []
                for root in data['roots']:
                    mirror_name = naming.convertRLName(root)
                    mirror_names.append(mirror_name[:mirror_name.rfind("_")])
                mirror_roots = self.addHelperJoint(mirror_add_joint, mirror_parent_joint, primaryAxis=data["axis"],
                                                   size=data["size"], translate_axis=data["translate_axis"], distance=data["distance"],
                                                   isJointChain=data["isJointChain"], names=mirror_names, mirror=True)
                self.mirror_root(data["roots"], mirror_roots)
            else:
                mirrors = []
                roots = []
                for root in data['roots']:
                    mirror_name = naming.convertRLName(root)
                    if root == mirror_name or cmds.objExists(mirror_name):
                        continue
                    roots.append(root)
                    mirrors.append(mirror_name[:mirror_name.rfind("_")])
                mirror_roots = self.addHelperJoint(mirror_add_joint, mirror_parent_joint, primaryAxis=data["axis"],
                                                   size=data["size"], translate_axis=data["translate_axis"],
                                                   isJointChain=data["isJointChain"], names=mirrors,
                                                   mirror=True)
                self.mirror_root(roots, mirror_roots)
        self.refreshList()

    def mirror_root(self, roots, mirror_roots):
        for root, mirror_root in zip(roots, mirror_roots):
            number_root = root.split("_")[-3]
            mirror_number_root = mirror_root.split("_")[-3]
            if number_root != mirror_number_root:
                childs = cmds.listRelatives(mirror_root, c=True, ad=True)
                for c in childs + [mirror_root]:
                    if mirror_number_root in c:
                        new_name = c.replace(mirror_number_root, number_root)
                        cmds.rename(c, new_name)
            base_zero = cmds.listConnections("{}.baseZeroGrp".format(root), source=True, destination=False) or []
            zero = cmds.listConnections("{}.zeroGrp".format(root), source=True, destination=False) or []
            ctrl = cmds.listConnections("{}.control".format(root), source=True, destination=False) or []
            if not base_zero or not zero or not ctrl:
                return
            mirror_base_zero = naming.convertRLName(base_zero[0])
            mirror_zero = naming.convertRLName(zero[0])
            mirror_ctrl = naming.convertRLName(ctrl[0])
            if not cmds.objExists(mirror_zero) or not cmds.objExists(mirror_base_zero) or not cmds.objExists(mirror_ctrl):
                return

            mirror_matrix = matrix.getMirrorMatrix(base_zero[0])
            cmds.xform(mirror_base_zero, matrix=mirror_matrix, worldSpace=True)
            cmds.setAttr(mirror_zero+".translate", *cmds.getAttr(zero[0]+".translate")[0])
            cmds.setAttr(mirror_zero + ".rotate", *cmds.getAttr(zero[0] + ".rotate")[0])
            controls.mirrorControl(ctrl[0], mirror_ctrl)

    def getNodeData(self, net):
        addJoint = cmds.listConnections("{}.rootMatrix".format(net), source=True, destination=False, type="joint")[0]
        parentJoint = cmds.listConnections("{}.fatherMatrix".format(net), source=True, destination=False, type="joint")[0]
        ctrls = cmds.listConnections("{}.controls".format(net), source=True, destination=False)
        skinJnts = cmds.listConnections("{}.branchSkinJoints".format(net), source=True, destination=False)
        roots = cmds.listConnections("{}.roots".format(net), source=True, destination=False)
        isJointChain = cmds.getAttr("{}.jointChain".format(net))
        size = cmds.getAttr("{}.size".format(net))
        axis = cmds.getAttr("{}.axis".format(net))
        translate_axis = cmds.getAttr("{}.translate_axis".format(net))
        return {
            "addJoint": addJoint,
            "parentJoint": parentJoint,
            "ctrls": ctrls,
            "skinJnts": skinJnts,
            "roots": roots,
            "isJointChain": isJointChain,
            "size": size,
            "distance": cmds.getAttr("{}.distance".format(net)),
            "axis": axis,
            "translate_axis": translate_axis
        }


    @toolsetwidget.ToolsetWidget.undoDecorator
    def rename(self, *args):
        if not self.NetView.selectedItems():
            return
        selected_node = self.NetView.selectedItems()[0].data(0)
        if cmds.objExists(selected_node) and cmds.objectType(selected_node) == "network": return
        search_text = selected_node[:selected_node.rfind("_")]
        replace_text = elements.MessageBox.inputDialog(title="Rename",
                                        text=search_text,
                                        parent=None, message='Replace Name')
        names.searchReplaceFilteredType(search_text,
                                        replace_text,
                                        filtertypes.ALL,
                                        renameShape=True,
                                        searchHierarchy=True,
                                        selectionOnly=False,
                                        dag=False,
                                        removeMayaDefaults=True,
                                        transformsOnly=True,
                                        message=True)
        self.refreshList()

    def onContextMenu(self, selection, menu):
        menu.setSearchVisible(False)
        menu.addActionExtended(
            "Rename",
            connect=self.rename
        )
        menu.addActionExtended(
            "Delete",
            connect=self.deleteSetting,
            icon=iconlib.iconColorized("deleteHiveRig"),
        )
        menu.addSeparator()

    @toolsetwidget.ToolsetWidget.undoDecorator
    def createAllSettings(self, type='timeline'):
        # json_file_path = os.path.abspath(__file__ + "/../settings.json")
        # with open(json_file_path, 'r') as json_file:
        #     data = json.load(json_file)
        #     if type in data:
        #         for joint, ref in data[type].items():
        #             if cmds.objExists(joint) and cmds.objExists(ref['parent']):
        #                 size = ref["distance"] * 0.3
        #                 side = ref['side']
        #                 primaryAxis = 'x'
        #                 translate_axis = 'y'
        #                 if type == "timeline":
        #                     size = ref["distance"] * 0.1
        #                     if 'Foot' in joint:
        #                         primaryAxis = 'y'
        #                         translate_axis = 'z'
        #                     elif 'Toe' in joint:
        #                         size *= 0.7
        #                         primaryAxis = 'z'
        #                         translate_axis = 'y'
        #                 if side != "M" and not ref['isFinger']:
        #                     root, baseZero, zero = self.addHelperJoint(joint, ref['parent'], primaryAxis=primaryAxis,
        #                                                                size=size, side=side,
        #                                                                translate_axis=translate_axis,
        #                                                                isJointChain=True, add=False)
        #
        #                 self.refreshList()
        pass


    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.LoadPb.clicked.connect(partial(self.loadJoint, self.LoadLe))
        self.ParentPb.clicked.connect(partial(self.loadJoint, self.ParentLe))
        self.ApplyPb.clicked.connect(self.Generate)  # 生成函数
        self.NetView.treeView.clicked.connect(self.viewItemClick)
        self.NetView.contextMenuRequested.connect(self.onContextMenu)
        self.RefreshPb.clicked.connect(self.refreshList)  # 刷新列表
        self.MirrorPb.clicked.connect(self.mirrorSetting)
        # self.actionExport_All_Settings.triggered.connect(self.exportSettings)  # 导出所有设置
        # self.actionImport_Settings.triggered.connect(self.importSettings)  # 导入所有设置
        self.actionCreate_TimelineSettings.triggered.connect(partial(self.createAllSettings, type="timeline"))
        # self.actionCreate_AdvSettings.triggered.connect(partial(self.createAllSettings, type="adv"))

