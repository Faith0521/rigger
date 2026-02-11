#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/11/19 09:31
# @Author : yinyufei
# @File : dynamicjoint.py
# @Project : TeamCode
# -*- coding: utf-8 -*-
from cgrigvendor.Qt import QtWidgets, QtCore, QtGui
from maya import cmds
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.maya.cmds.rig import riggingmisc
from cgrig.libs.maya.cmds.objutils import attributes
from cgrig.libs.iconlib import iconlib
from cgrig.libs.pyqt.extended import listviewplus
from cgrig.libs.pyqt.models import datasources, listmodel, constants


UI_MODE_COMPACT = 0
UI_MODE_ADVANCED = 1


class DynamicJoint(toolsetwidget.ToolsetWidget):
    id = "dynamicJoint"
    info = "Dynamic rigging tool."
    uiData = {"label": "Dynamic Joint",
              "icon": "robotArm",
              "defaultActionDoubleClick": False}

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        self.nodes = []
        if not cmds.pluginInfo("boneDynamicsNode.mll", q=True, loaded=True):
            try:
                cmds.loadPlugin("boneDynamicsNode.mll")
            except RuntimeError:
                cmds.error("You need the boneDynamicsNode plugins!")

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]  # self.initAdvancedWidget()

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = GuiCompact(parent=self, properties=self.properties, toolsetWidget=self)
        dynamic_nodes = self.getDynamicNodes
        if dynamic_nodes:
            self.refresh_(dynamic_nodes)
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
        return super(DynamicJoint, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[GuiAdvanced or GuiCompact]
        """
        return super(DynamicJoint, self).widgets()

    # ------------------
    # LOGIC
    # ------------------
    import maya.cmds as cmds

    def create_joint_chain_from_selected(self, nodes):
        joints = []

        # 2. 按顺序创建骨骼
        for i, obj in enumerate(nodes):

            # 创建骨骼
            joint_name = "{}_dynamic_jnt".format(obj)
            new_joint = cmds.createNode(
                "joint",
                name=joint_name
            )
            cmds.delete(cmds.parentConstraint(obj, new_joint))
            cmds.makeIdentity(new_joint, r=1, apply=1)

            joints.append(new_joint)

        # 3. 建立父子关系
        for i in range(1, len(joints)):
            cmds.parent(joints[i], joints[i - 1])

        return joints

    def create_dynamics_node(
            self,
            bone,
            end,
            scalable=False,
            target_bone=None,
            offset_node=None,
            colliders=[],
            visualize=True,
            additional_force_node=None,
            additional_force_init_vec=[0, 0, -1]
    ):

        if not bone in cmds.listRelatives(end, p=True):
            print("Exit: {} is not {}'s parent.".format(bone, end))
            return

        boneDynamicsNode = cmds.createNode("boneDynamicsNode")

        cmds.connectAttr('time1.outTime', boneDynamicsNode + '.time', force=True)
        cmds.connectAttr(bone + '.translate', boneDynamicsNode + '.boneTranslate', f=True)
        cmds.connectAttr(bone + '.parentMatrix[0]', boneDynamicsNode + '.boneParentMatrix', f=True)
        cmds.connectAttr(bone + '.parentInverseMatrix[0]', boneDynamicsNode + '.boneParentInverseMatrix', f=True)
        cmds.connectAttr(bone + '.jointOrient', boneDynamicsNode + '.boneJointOrient', f=True)
        cmds.connectAttr(end + '.translate', boneDynamicsNode + '.endTranslate', f=True)

        cmds.connectAttr(boneDynamicsNode + '.outputRotate', bone + '.rotate', f=True)

        if scalable:
            cmds.connectAttr(bone + '.scale', boneDynamicsNode + '.boneScale', f=True)
            cmds.connectAttr(bone + '.inverseScale', boneDynamicsNode + '.boneInverseScale', f=True)
            cmds.connectAttr(end + '.scale', boneDynamicsNode + '.endScale', f=True)

        if target_bone:
            if cmds.objExists(target_bone):
                cmds.connectAttr(target_bone + '.rotate', boneDynamicsNode + '.rotationOffset', f=True)

        if offset_node:
            if cmds.objExists(offset_node):
                cmds.connectAttr(offset_node + '.worldMatrix[0]', boneDynamicsNode + '.offsetMatrix', f=True)

        if additional_force_node:
            if cmds.objExists(additional_force_node):
                vp = cmds.listConnections(additional_force_node + '.worldMatrix[0]', s=False, d=True,
                                          type='vectorProduct')
                if vp:
                    vp = vp[0]
                else:
                    vp = cmds.createNode('vectorProduct')
                    cmds.setAttr(vp + '.operation', 3)
                    cmds.setAttr(vp + '.input1', additional_force_init_vec[0], additional_force_init_vec[1],
                                 additional_force_init_vec[2], type='double3')
                    cmds.setAttr(vp + '.normalizeOutput', 1)
                    cmds.connectAttr(additional_force_node + '.worldMatrix[0]', vp + '.matrix', f=True)
                cmds.connectAttr(vp + '.output', boneDynamicsNode + '.additionalForce', f=True)

        if visualize:
            # angle limit
            angle_cone = cmds.createNode("implicitCone")
            angle_cone_tm = cmds.listRelatives(angle_cone, p=True)[0]
            angle_cone_ro = cmds.createNode("transform", n="{}_cone_ro".format(bone))
            angle_cone_root = cmds.createNode("transform", n="{}_cone_root".format(bone))
            cmds.setAttr(angle_cone_tm + '.ry', -90)
            cmds.parent(angle_cone_tm, angle_cone_ro, r=True)
            cmds.parent(angle_cone_ro, angle_cone_root, r=True)
            bone_parent = cmds.listRelatives(bone, p=True)
            if bone_parent:
                cmds.parent(angle_cone_root, bone_parent[0], r=True)
            cmds.connectAttr(boneDynamicsNode + '.boneTranslate', angle_cone_root + '.translate', f=True)
            cmds.connectAttr(boneDynamicsNode + '.boneJointOrient', angle_cone_root + '.rotate', f=True)
            cmds.connectAttr(boneDynamicsNode + '.rotationOffset', angle_cone_ro + '.rotate', f=True)
            cmds.connectAttr(boneDynamicsNode + '.enableAngleLimit', angle_cone_root + '.v', f=True)
            cmds.connectAttr(boneDynamicsNode + '.angleLimit', angle_cone + '.coneAngle', f=True)
            cmds.setAttr(angle_cone + '.coneCap', 2)
            cmds.setAttr(angle_cone_tm + '.overrideEnabled', 1)
            cmds.setAttr(angle_cone_tm + '.overrideDisplayType', 2)

            # collision radius
            radius_sphere = cmds.createNode("implicitSphere")
            cmds.connectAttr(boneDynamicsNode + '.radius', radius_sphere + '.radius', f=True)
            radius_sphere_tm = cmds.listRelatives(radius_sphere, p=True)[0]
            cmds.parent(radius_sphere_tm, end, r=True)
            cmds.setAttr(radius_sphere_tm + '.overrideEnabled', 1)
            cmds.setAttr(radius_sphere_tm + '.overrideDisplayType', 2)
            cmds.connectAttr(boneDynamicsNode + '.iterations', radius_sphere_tm + '.v', f=True)

        sphere_col_idx = 0
        capsule_col_idx = 0
        iplane_col_idx = 0
        mesh_col_idx = 0

        for col in colliders:

            if not cmds.objExists(col):
                print("Skip: {} is not found.".format(col))
                continue

            if not cmds.attributeQuery('colliderType', n=col, ex=True):
                col_shape = cmds.listRelatives(col, s=True, f=True)
                if col_shape:
                    if cmds.nodeType(col_shape[0]) == 'mesh':
                        cmds.connectAttr(col_shape[0] + '.worldMesh[0]',
                                         boneDynamicsNode + '.meshCollider[{}]'.format(mesh_col_idx), f=True)
                        mesh_col_idx += 1
                        continue
                print("Skip: {} has no 'colliderType' attribute.".format(col))
                continue

            colliderType = cmds.getAttr(col + '.colliderType')

            if colliderType == 'sphere':
                cmds.connectAttr(col + ".worldMatrix[0]",
                                 boneDynamicsNode + ".sphereCollider[{}].sphereColMatrix".format(sphere_col_idx),
                                 f=True)
                cmds.connectAttr(col + ".radius",
                                 boneDynamicsNode + ".sphereCollider[{}].sphereColRadius".format(sphere_col_idx),
                                 f=True)
                sphere_col_idx += 1

            elif colliderType in ['capsule', 'capsule2']:
                radius_attr_a = ".radius" if colliderType == 'capsule' else ".radiusA"
                radius_attr_b = ".radius" if colliderType == 'capsule' else ".radiusB"
                a = cmds.listConnections(col + '.sphereA', d=0)[0]
                b = cmds.listConnections(col + '.sphereB', d=0)[0]
                cmds.connectAttr(a + ".worldMatrix[0]",
                                 boneDynamicsNode + ".capsuleCollider[{}].capsuleColMatrixA".format(capsule_col_idx),
                                 f=True)
                cmds.connectAttr(b + ".worldMatrix[0]",
                                 boneDynamicsNode + ".capsuleCollider[{}].capsuleColMatrixB".format(capsule_col_idx),
                                 f=True)
                cmds.connectAttr(col + radius_attr_a,
                                 boneDynamicsNode + ".capsuleCollider[{}].capsuleColRadiusA".format(capsule_col_idx),
                                 f=True)
                cmds.connectAttr(col + radius_attr_b,
                                 boneDynamicsNode + ".capsuleCollider[{}].capsuleColRadiusB".format(capsule_col_idx),
                                 f=True)
                capsule_col_idx += 1

            elif colliderType == 'infinitePlane':
                cmds.connectAttr(col + ".worldMatrix[0]",
                                 boneDynamicsNode + ".infinitePlaneCollider[{}].infinitePlaneColMatrix".format(
                                     iplane_col_idx), f=True)
                iplane_col_idx += 1

        return boneDynamicsNode

    def load(self):
        selections = cmds.ls(selection=True)
        if not selections:
            self.compactWidget.loadObj.setText("")
            return
        else:
            self.compactWidget.loadObj.setText(str(selections))
            self.nodes = selections

    @property
    def getDynamicNodes(self):
        dynamic_nodes = cmds.ls(type="boneDynamicsNode") or []

        return dynamic_nodes

    @toolsetwidget.ToolsetWidget.undoDecorator
    def add(self):
        # Enable per-section scaling.
        scalable = True

        # Place the collider created by expcol as a child of 'collider_grp'.
        colliders = []
        if cmds.objExists("collider_grp"):
            colliders = cmds.ls(cmds.listRelatives("collider_grp", c=True), tr=True)

        # Duplicate the joint-chain to be simulated and add '_target' to the postfix.
        target_bone_postfix = "_target"

        # Name of the node to offset the transform.
        offset_node_name = "offset"

        # Node name that controls the direction of additional force
        additional_force_node_name = "wind"

        # ---------------------------------------------------

        set_name = "boneDynamicsNodeSet"
        if not cmds.objExists(set_name):
            cmds.select(cl=True)
            cmds.sets(name=set_name)

        nodes = self.create_joint_chain_from_selected(self.nodes)
        nodes_up_zero = cmds.createNode("transform", name=nodes[0]+"_up_zero")
        nodes_up = cmds.createNode("transform", name=nodes[0] + "_up_ctrl", p=nodes_up_zero)
        cmds.delete(cmds.parentConstraint(nodes[0], nodes_up_zero))
        cmds.parent(nodes[0], nodes_up)

        boneDynamicsNodes = []
        for bone, end in zip(nodes[:-1], nodes[1:]):
            boneDynamicsNode = self.create_dynamics_node(
                bone,
                end,
                scalable=scalable,
                target_bone=bone + target_bone_postfix,
                offset_node=offset_node_name,
                colliders=colliders,
                visualize=True,
                additional_force_node=additional_force_node_name,
                additional_force_init_vec=[0, 0, -1]
            )

            boneDynamicsNodes.append(boneDynamicsNode)
            if boneDynamicsNode:
                cmds.sets(boneDynamicsNode, addElement=set_name)

        controls = []
        for j,joint in enumerate(nodes[1:]):
            parent = cmds.listRelatives(joint, parent=True, ad=True)[0]
            zero = cmds.createNode("transform", name="{}_ctrl_zero".format(joint))
            control = cmds.createNode("transform", name="{}_ctrl".format(joint), p=zero)
            cmds.delete(cmds.parentConstraint(joint, zero))
            cmds.parent(zero, parent)
            cmds.makeIdentity(zero, apply=True, t=1, r=1, s=1)
            cmds.parent(joint, control)
            controls.append(control)

        [cmds.parentConstraint(control, self.nodes[j], mo=1) for j,control in enumerate([nodes_up]+controls)]


        attributes.createEnumAttrList(nodes_up, "_____", ["switch"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "enable", nodes_up, "bool", "switch", defaultValue=1)
        attributes.createEnumAttrList(nodes_up, "____", ["FPS"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "fps", nodes_up, "float", "fps", defaultValue=24, minValue=1)
        attributes.createEnumAttrList(nodes_up, "___", ["damping"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "damping", nodes_up, "float", "damping", defaultValue=0.1, minValue=0)
        attributes.createEnumAttrList(nodes_up, "__", ["elasticity"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "elasticity", nodes_up, "float", "elasticity", defaultValue=30, minValue=0)
        attributes.createEnumAttrList(nodes_up, "_", ["stiffness"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "stiffness", nodes_up, "float", "stiffness", defaultValue=0, minValue=0)
        attributes.createEnumAttrList(nodes_up, "_______", ["mass"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "mass", nodes_up, "float", "mass", defaultValue=1, minValue=0.01)
        attributes.createEnumAttrList(nodes_up, "______", ["angle"], channelBox=True, nonKeyable=True)
        self.addListAttr(boneDynamicsNodes, "enableAngleLimit", nodes_up, "bool", "enableAngleLimit", defaultValue=0)
        self.addListAttr(boneDynamicsNodes, "angleLimit", nodes_up, "float", "angleLimit", defaultValue=60, minValue=0)

        self.refresh_(boneDynamicsNodes)

    def addListAttr(self, dynamic_nodes, dynamic_attr, node, attr_type, attr_prefix, defaultValue=0, minValue=None, maxValue=None):
        for i,dyn in enumerate(dynamic_nodes):
            attributes.createAttribute(
                node, "{}0{}".format(attr_prefix, i), attributeType=attr_type, minValue=minValue, maxValue=maxValue, defaultValue=defaultValue
            )
            cmds.connectAttr("{}.{}0{}".format(node, attr_prefix, i), "{}.{}".format(dyn, dynamic_attr), f=1)


    def refresh_(self, nodes):
        self.compactWidget.objModel.clear()
        for node in nodes:
            item = QtGui.QStandardItem(node)
            item.setSelectable(True)
            self.compactWidget.objModel.appendRow(item)

    def selectNode(self, index):
        row = index.row()
        item_text = index.data()
        if cmds.objExists(item_text):
            cmds.select(item_text, r=1)

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.compactWidget.loadBtn.clicked.connect(self.load)
        self.compactWidget.add.clicked.connect(self.add)
        self.compactWidget.objView.clicked.connect(self.selectNode)


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
        self.properties = properties
        self.loadObj = elements.StringEdit(label="Load Objects",
                                           editPlaceholder="selected objects to load.",
                                           labelRatio=3,
                                           editRatio=6,
                                           parent=parent)
        self.loadBtn = elements.styledButton(text="Load Objects")
        self.objView = QtWidgets.QListView(self)
        self.objModel = QtGui.QStandardItemModel()
        self.objView.setModel(self.objModel)
        self.add = elements.styledButton(text="add")


class GuiCompact(GuiWidgets):
    def __init__(self, parent=None, properties=None, uiMode=UI_MODE_COMPACT, toolsetWidget=None):
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
                                         spacing=uic.SPACING)
        loadHLayout = elements.hBoxLayout(self)
        loadHLayout.addWidget(self.loadObj)
        loadHLayout.addWidget(self.loadBtn)

        # Add To Main Layout ---------------------------------------
        mainLayout.addLayout(loadHLayout)
        mainLayout.addWidget(self.objView)
        mainLayout.addWidget(self.add)
        # mainLayout.addWidget(self.parameterCollapsable)
        mainLayout.addStretch()



