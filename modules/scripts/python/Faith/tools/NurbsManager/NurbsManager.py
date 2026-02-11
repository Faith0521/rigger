# coding:utf-8
from functools import partial
from imp import reload
# maya import
from pymel.core import *
from pymel.core.datatypes import *
from Faith.vendor.Qt import QtCore, QtWidgets
from maya import cmds
from maya.api import OpenMaya as om
# ui import
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from ...maya_utils import ui_utils, decorator_utils, controller_utils, rigging_utils, attribute_utils, function_utils, api_utils, node_utils
from . import nurbs as ui
from . import nurbsIKFK_motionPath as motion
from . import rope_utils
import re
from cgrig.libs.maya.cmds.rig import skeleton

reload(rigging_utils)
reload(attribute_utils)
reload(api_utils)
reload(ui)
reload(function_utils)
reload(motion)
reload(rope_utils)


class CurveException(BaseException):
    """ Raised to indicate invalid curve parameters. """


class DeleteException(BaseException):
    """ Raised to invalid delete objects. """


class MainGUI(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    """
    main ui window
    """

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.installEventFilter(self)


class DockableNurbsMainUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(DockableNurbsMainUI, self).__init__(parent=parent)
        self._rigName = None
        self.joints = None
        self.skinJntGrp = None
        self.follicgrp = None
        self.NurbsRigGlobal = None
        self.spring_con = None
        self.spring_cns = []
        self.spring_aim = []
        self.spring_target = []
        self.gmc_layout = None
        self.uiName = "NurbsManager"
        self.mainUI = MainGUI()
        self.axis = {"+X": (1, 0, 0), "+Y": (0, 1, 0), "+Z": (0, 0, 1),
                     "-X": (-1, 0, 0), "-Y": (0, -1, 0), "-Z": (0, 0, -1)}
        self.rigData = {"side": [""], "fkColor": (1, 1, 0.5), "ikColor": (1, 0, 0)}
        self.addStretchAttrObj = None
        self.hiddenWidget = [self.mainUI.upper_widget, self.mainUI.snake_widget]
        self.ctrlTypes = list(controller_utils.Icon().iconDictionary.keys())
        self.create_window()
        self.create_layout()
        self.init_widget()
        self.create_connections()

    def create_window(self):
        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Nurbs Tool v0.0.3")
        self.resize(220, 250)
        # self.setStyleSheet(ui_utils.qss)

    def init_widget(self):
        self.mainUI.snake_widget.setHidden(True)
        self.mainUI.sec_axis_cb.setHidden(True)
        self.mainUI.label_4.setHidden(True)

    def create_layout(self):
        """
        create layouts
        :return:
        """
        self.gmc_layout = QtWidgets.QVBoxLayout()
        self.gmc_layout.addWidget(self.mainUI)
        self.gmc_layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.gmc_layout)

    def create_connections(self):
        self.mainUI.create_jnt_btn.clicked.connect(self.create_joint)
        self.mainUI.custom_rb.toggled.connect(self.hideSnakeWidget)
        self.mainUI.addUpperCb.toggled.connect(self.enableUpperUI)
        self.mainUI.rig_btn.clicked.connect(self.generate)
        self.mainUI.delete_btn.clicked.connect(self.deleteRig)

        self.mainUI.attrCtrl_btn.clicked.connect(self.loadAttrCtrl)
        self.mainUI.obj_btn.clicked.connect(self.loadSetObjects)
        self.mainUI.setup_btn.clicked.connect(self.setupDynamics)
        self.mainUI.motion_btn.clicked.connect(lambda x: motion.mwnd().show())

    @decorator_utils.one_undo
    def create_joint(self):
        self.getRigData()
        count = self.mainUI.jntNum_spin_2.value()
        axis = self.mainUI.sec_axis_cb.currentText()
        typ = self.mainUI.type_cb.currentText()
        mirror = False if self.rigData["side"][0] == "" else True
        self.joints = [joint for joint in cmds.ls(rope_utils.re_all_joints(count, axis, typ,
                                                  self.rigData["side"][0] + self.rigData["rigName"], mirror, world=self.rigData["world"]), long=1)]

    @decorator_utils.one_undo
    def deleteRig(self, *args):
        all_trans = api_utils.get_all_objects_by_type(om.MFn.kTransform)
        for node in all_trans:
            if cmds.objExists(node + ".rig_group"):
                cmds.delete(node)

    def loadObj(self, widget, *args):
        selection = selected(type="transform")
        if selection:
            if len(selection) > 1:
                widget.setText(str([sel.nodeName() for sel in selection]))
            else:
                widget.setText(selection[0].nodeName())

    def loadSkinJnts(self, *args):
        selection = selected(type="joint")
        if selection: self.mainUI.stretch_skinJnts_le.setText(str([sel.nodeName() for sel in selection]))

    @decorator_utils.one_undo
    def createMotionPath_old(self, *args):
        self.getRigData()
        selection = eval(self.rigData["animCurves"])
        selection = [PyNode(sel) for sel in selection if objExists(sel)]
        selection = [selection[i:i + 2] for i in range(0, len(selection), 2)]
        objList = ls(type="transform")
        for obj in objList:
            if objExists(obj + ".global_grp"):
                self.NurbsRigGlobal = obj.nodeName()
            if objExists(obj + ".show_grp"):
                self.NurbsRigShow = obj.nodeName()
            if objExists(obj + ".hidden_grp"):
                self.NurbsRigHidden = obj.nodeName()
            if objExists(obj + ".follic_grp"):
                self.follicgrp = obj
            if objExists(obj + ".skin_grp"):
                self.skinJntGrp = obj
        returnDict = self.createNurbsIKFKRig(selection, self.rigData["motionNumber"], self.rigData["motionNumber"],
                                             self.rigData["aimAxis"], self.rigData["upAxis"],
                                             self.rigData["motionType"],
                                             self.rigData["motionSize"], prefix="Motion")
        # create path joints
        ctrlJnts = []
        confkgrps = []
        if objExists(self.NurbsRigGlobal + ".custom_ctrlJnts"):
            ctrlJnts = eval(getAttr(self.NurbsRigGlobal + ".custom_ctrlJnts"))
        if objExists(self.NurbsRigGlobal + ".custom_confkgrps"):
            confkgrps = eval(getAttr(self.NurbsRigGlobal + ".custom_confkgrps"))

        for i in range(len(ctrlJnts)):
            size = 0
            pathJointList = list()
            for jnt in ctrlJnts[i][::-1]:
                jin = joint(p=xform(jnt, q=True, t=True, ws=True),  # NOQA
                            n=self.rigData["rigName"] + str(i) + "_pathikHandleJnt_" + str(size))
                pathJointList.append(jin)
                size += 1
            select((pathJointList[0], pathJointList[-1], returnDict["wireCrvs"][i]), r=1)
            IkHandle = ikHandle(sol='ikSplineSolver', ccv=False, pcv=False, roc=True)[0]
            IkHandle.dTwistControlEnable.set(1)
            IkHandle.dWorldUpType.set(3)
            connectAttr(self.NurbsRigGlobal + ".worldMatrix[0]", IkHandle + ".dWorldUpMatrix")

            parents = [parentConstraint(joint, conGrp, mo=True) for joint, conGrp in
                       zip(pathJointList, confkgrps[i][::-1])]

            PathCurveRigDoMoveGrp = group(pathJointList[0],
                                          n=self.rigData["rigName"] + str(i) + 'PathCurveRigDoMoveGrp')
            PathCurveRigDoMoveGrp.v.set(0)
            PathCurveRigDoMoveGrp.v.set(lock=1)
            PathCurveRigDoMoveGrp.inheritsTransform.set(0)
            parent(IkHandle, PathCurveRigDoMoveGrp)
            parCon = parentConstraint(self.NurbsRigGlobal, PathCurveRigDoMoveGrp)
            scleCon = scaleConstraint(self.NurbsRigGlobal, PathCurveRigDoMoveGrp)
            IkHandle.v.set(0, lock=1)

            attribute_utils.addAttributes(self.NurbsRigGlobal, "Go", "double", 0, min=0, max=1, keyable=True)
            connectAttr(self.NurbsRigGlobal + ".Go", IkHandle + ".offset")

            # 移动组
            parent(PathCurveRigDoMoveGrp, self.NurbsRigHidden)

    @decorator_utils.one_undo
    def sizeValueChange(self, widget, *args):
        CtrlList = []
        nodeList = ls(type="transform")
        for node in nodeList:
            if objExists("%s.%s_Controller" % (node, widget.objectName()[:2])): CtrlList.append(node)
        value = float(widget.currentText())
        [scale(ctrl.cv, value, value, value, r=True) for
         ctrl in CtrlList]

    def enableUpperUI(self, typ, *args):
        enableWidgets = [self.mainUI.upperNum_spin, self.mainUI.stretch_cb, self.mainUI.reverse_cb]
        [widget.setEnabled(typ) for widget in enableWidgets]

    def hideSnakeWidget(self, typ, *args):
        self.mainUI.snake_widget.setHidden(typ)

    @decorator_utils.one_undo
    def generate(self, *args):
        self.getRigData()
        self.rigName = self.rigData["rigName"]
        self.joints = self.control_joints
        if not self.joints: return

        self.joints = self.get_selected_joint_chains(self.joints)

        # if not cmds.ls(sl=1):
        #     cmds.warning("Please select one curve.")
        #     return
        # selection = cmds.ls(sl=1)
        # count = len(cmds.ls(selection[0] + ".cv[*]", fl=1))
        # axis = self.mainUI.sec_axis_cb.currentText()
        # typ = self.mainUI.type_cb.currentText()
        # mirror = False if self.rigData["side"][0] == "" else True
        #
        # tempjoints = [joint for joint in cmds.ls(rope_utils.re_all_joints(count, axis, typ,"temp", mirror, world=False), long=1)]

        for i, joints in enumerate(self.joints):
            rig_name = cmds.getAttr("{}.rigName".format(joints[0]))
            rig_group = rig_name + "rope_rig_grp"
            scale_group = rig_name + "rope_scale"
            show_group = rig_name + "rope_show"
            hidden_group = rig_name + "rope_hidden"
            rivets_group = rig_name + "rope_rivets"
            skin_joints_group = rig_name + "rope_skin_joints"
            if cmds.objExists(rig_group):
                continue
            cmds.createNode('transform', name=rig_group)
            cmds.createNode('transform', name=scale_group, p=rig_group)
            cmds.createNode('transform', name=show_group, p=rig_group)
            cmds.createNode('transform', name=hidden_group, p=rig_group)
            cmds.createNode('transform', name=rivets_group, p=hidden_group)
            cmds.createNode('transform', name=skin_joints_group, p=hidden_group)
            attribute_utils.addAttributes(rig_group, 'rig_group', 'bool', value=1, keyable=False)

            return_dict = self.createNurbsIKFKRig(joints, self.rigData["rigTypes"], self.rigData["jointNumber"], self.rigData["customSize"], world=self.rigData["world"])

            self.doConstraint(scale_group, show_group, hidden_group, rivets_group, skin_joints_group, return_dict, snake=self.rigData["snakeType"])

            if self.rigData["addUpperCtrl"]:
                count = self.rigData["upperCtrlNumber"]
                axis = cmds.getAttr("{}.axis".format(joints[0]))
                cmds.select(return_dict["wireCrvs"], r=1)
                temp_joints = rope_utils.re_all_joints(count, axis, u'首尾骨骼', rig_name + "up_", False, surface=return_dict['planes'][0], world=False)

                d=3
                if len(temp_joints) <= 3:
                    d=1

                return_up_dict = self.createNurbsIKFKRig(temp_joints, self.rigData["upperRigTypes"], len(joints),
                                                         self.rigData["customSize"]*2.0, prefix='', reverse=self.rigData["upperReverse"], world=False)
                self.doConstraint(scale_group, show_group, hidden_group, rivets_group, skin_joints_group, return_up_dict, snake=self.rigData["snakeType"])
                [cmds.setAttr(plane + ".v", 0) for plane in return_up_dict['planes']]
                [cmds.setAttr(jnt + ".v", 0) for jnt in return_up_dict['skinJointList']]
                if count > 2:
                    cmds.delete(temp_joints)

                if 'fk' in self.rigData["rigTypes"]:
                    if self.rigData["upperReverse"]: return_dict["confkgrps"].reverse()
                    for i in range(len(return_dict["confkgrps"])):
                        cmds.parentConstraint(return_up_dict["skinJointList"][i], return_dict["confkgrps"][i], mo=1)

                if self.rigData["rigTypes"] == ["ik"]:
                    if self.rigData["upperReverse"]: return_dict["ikctrlZeros"].reverse()
                    for i in range(len(return_dict["ikctrlZeros"])):
                        cmds.parentConstraint(return_up_dict["skinJointList"][i], return_dict["ikctrlZeros"][i], mo=1)

                if self.rigData["addUpperStretch"]:
                    if not objExists("%s.%s" % (scale_group, "up_stretch")):
                        attribute_utils.addAttributes(scale_group, "up_stretch", "float", value=0, min=0, max=1, keyable=True)
                    self.addStretch(return_up_dict["follicTransforms"], return_up_dict["ctrlJnts"], len(joints), show_group, hidden_group, scale_group)

            if self.rigData["snakeType"]:
                for i in range(len(return_dict["planes"])):
                    axisList = ["Y", "Z"]
                    side_bridge = return_dict["planes"][i].replace("_nurbSurface", "") + "_bridge"

                    side_bridge = controller_utils.Icon().create_icon("Diamond",
                                                                      icon_name=side_bridge,
                                                                      icon_color=17,
                                                                      scale=[self.rigData["customSize"]]*3)[0]
                    attribute_utils.lock_and_hide(side_bridge)

                    rigging_utils.GrpAdd(side_bridge, [side_bridge + "_zero", side_bridge + "_con"], "Up")
                    cmds.parent(side_bridge + "_zero", scale_group)

                    rigging_utils.Snake().addSnakeAttrs(side_bridge, addDrum=self.rigData["createDrum"],
                                                        addRot=self.rigData["createRot"],
                                                        addCurly=self.rigData["createCurly"])

                    curlyGrpList = []
                    boodyCurlyGrpList = []
                    ReverseCurlyGrpList = []
                    rootGrpList = []
                    grpList = []
                    DrumBagGrpList = []
                    GrpLStrList = ["_control"]
                    if self.rigData["createRot"]:
                        GrpLStrList += ["_reverseRoot", "_root"]
                    if self.rigData["createCurly"]:
                        GrpLStrList += ["_reverseCurly", "_boodyCurly", "_curly"]
                    # add Grp
                    for k, grp in enumerate(return_dict["confkgrps"]):
                        zeroGrp = grp.split('|')[-1][4:].replace('_offset', '_con')
                        Grps = rigging_utils.GrpAdd(zeroGrp, [zeroGrp[:-4] + name for name in GrpLStrList], "Up")[0]
                        if self.rigData["createRot"]:
                            rootGrpList.append(Grps["root"])
                        if self.rigData["createCurly"]:
                            curlyGrpList.append(Grps["curly"])
                            boodyCurlyGrpList.append(Grps["boodyCurly"])
                            ReverseCurlyGrpList.append(Grps["reverseCurly"])
                        grpList.append(Grps["control"])

                    if self.rigData["createRot"]:
                        [cmds.connectAttr(side_bridge + ".rootX", grp + ".rx") for grp in rootGrpList]
                        [cmds.connectAttr(side_bridge + ".rootY", grp + ".ry") for grp in rootGrpList]
                        [cmds.connectAttr(side_bridge + ".rootZ", grp + ".rz") for grp in rootGrpList]

                    grpList = [PyNode(node) for node in grpList]
                    ReverseCurlyGrpList = [PyNode(node) for node in ReverseCurlyGrpList]
                    curlyGrpList = [PyNode(node) for node in curlyGrpList]
                    boodyCurlyGrpList = [PyNode(node) for node in boodyCurlyGrpList]

                    if self.rigData["createCurly"]:
                        CurlyNodes = rigging_utils.Snake().addSnakeCurly(PyNode(side_bridge), grpList[1:],
                                                                         ReverseCurlyGrpList[1:],
                                                                         curlyGrpList[1:], "curly", "")
                        BoodyCurlyNodes = rigging_utils.Snake().addSnakeCurly(PyNode(side_bridge), grpList[1:][::-1],
                                                                              ReverseCurlyGrpList[1:][::-1],
                                                                              boodyCurlyGrpList[1:][::-1], "boodyCurly",
                                                                              "boody")

                    if self.rigData["createSinCos"]:
                        [rigging_utils.createSinCosAttr(grpList,
                                                        return_dict["planes"][i].replace("_nurbSurface",
                                                                                        ""),
                                                        side_bridge,
                                                        'translate' + axis) for axis in axisList]

                    if self.rigData["createDrum"]:
                        drumGrp = cmds.createNode("transform",
                                             n=return_dict["planes"][i].replace("_nurbSurface", "") + "_DrumBag",
                                             p=show_group)
                        drumList = rigging_utils.Snake().addSnakeDrum((return_dict["skinJointList"]), side_bridge)
                        DrumBagGrpList.append(drumList)
                        cmds.parent(drumList, drumGrp)
                        cmds.scaleConstraint(scale_group, drumGrp, mo=True)

                    if self.rigData["createSlider"]:
                        sliderGrp, remapValueList, nodeList = rigging_utils.Snake().addSnakeSlider([PyNode(ctrl) for ctrl in return_dict["ikctrls"][i]],
                                                                                                   3,
                                                                                                   return_dict["planes"][
                                                                                                       i].replace(
                                                                                                       "_nurbSurface", ""),
                                                                                                   'Z',
                                                                                                   [PyNode(jnt) for jnt in return_dict["ctrlJnts"]],
                                                                                                   PyNode(scale_group),
                                                                                                   self.rigData["customSize"])

            cmds.select(cl=True)

    def getRigData(self):
        """
        get uI data for rigging prepare.
        :return:
        """
        self.rigData["rigName"] = self.mainUI.rigName_le.text()
        if self.rigData["rigName"] == "":
            self.rigData["rigName"] = "Nurbs_"
        if bool(self.mainUI.mirror_cb.isChecked()):
            self.rigData["side"] = ["L_", "R_"]
        else:
            self.rigData["side"] = [""]

        if self.mainUI.ikfkType.isChecked():
            self.rigData["rigTypes"] = ['ik', 'fk']
        elif self.mainUI.ikType.isChecked():
            self.rigData["rigTypes"] = ['ik']
        elif self.mainUI.fkType.isChecked():
            self.rigData["rigTypes"] = ['fk']

        self.rigData["world"] = bool(self.mainUI.world_cb.isChecked())
        self.rigData["second_axis"] = self.mainUI.sec_axis_cb.currentText()
        self.rigData["controlJointNumber"] = self.mainUI.jntNum_spin_2.value()
        self.rigData["joint_type"] = self.mainUI.type_cb.currentText()
        self.rigData["jointNumber"] = self.mainUI.jntNum_spin.value()
        self.rigData["customSize"] = self.mainUI.custom_spin.value()
        self.rigData["addUpperCtrl"] = bool(self.mainUI.addUpperCb.isChecked())
        self.rigData["upperCtrlNumber"] = self.mainUI.upperNum_spin.value()
        self.rigData["addUpperStretch"] = bool(self.mainUI.stretch_cb.isChecked())
        self.rigData["upperReverse"] = bool(self.mainUI.reverse_cb.isChecked())
        if self.mainUI.upperType_cb.currentIndex() == 0: self.rigData["upperRigTypes"] = ['ik', 'fk']
        if self.mainUI.upperType_cb.currentIndex() == 1: self.rigData["upperRigTypes"] = ['ik']
        if self.mainUI.upperType_cb.currentIndex() == 2: self.rigData["upperRigTypes"] = ['fk']

        # snake setting
        self.rigData["snakeType"] = bool(self.mainUI.snake_rb.isChecked())
        self.rigData["createSinCos"] = bool(self.mainUI.sinCos_cb.isChecked())
        self.rigData["createRot"] = bool(self.mainUI.rotate_cb.isChecked())
        self.rigData["createCurly"] = bool(self.mainUI.curly_cb.isChecked())
        self.rigData["createDrum"] = bool(self.mainUI.drum_cb.isChecked())
        self.rigData["createSlider"] = bool(self.mainUI.slider_cb.isChecked())

    def doConstraint(self, scale_group, show_group, hidden_group, rivets_group, skin_joints_group, data, snake=False):
        """
        给生成的绑定做约束
        """
        [cmds.setAttr(jnt + ".v", 0) for jnt in data['ctrlJnts']]
        cmds.parent(data['wireCrvs'], data['planes'], hidden_group)
        cmds.parent(data['ctrlGrp'], show_group)
        cmds.parent(data['follicTransforms'], rivets_group)
        cmds.parent(data['skinJointList'], skin_joints_group)
        cmds.parentConstraint(scale_group, data['ctrlGrp'], mo=1)
        cmds.scaleConstraint(scale_group, data['ctrlGrp'], mo=1)
        [cmds.scaleConstraint(scale_group, rivet, mo=1) for rivet in data['follicTransforms']]
        [cmds.scaleConstraint(scale_group, rivet, mo=1) for rivet in data['skinJointList'] if not snake]

    def createCtrl(self, rig_name, joints, rig_types, prefix='', size=1.0, world=False):
        """
        根据绑定类型和骨骼创建绑定
        :param rig_name: 绑定命名
        :param joints: 控制器骨骼
        :param rig_types: 绑定类型
        :param prefix: 前缀名
        :param size: 控制器大小
        :param world: 世界轴
        :return:
        """
        control_dict = {"fkctrlZeros": [], "ikctrlZeros": [],
                        "fkctrls": [], "ikctrls": [], "conJnts": [], "ctrlGrp": ""}
        control_joints = []
        for joint in joints:
            rig_name = cmds.getAttr("{}.rigName".format(joint))
            control_joint_name = joint.split('|')[-1].replace(rig_name, rig_name + prefix)
            control_joint = cmds.createNode("joint", name=control_joint_name.replace('jnt', 'rope_con_jnt'), p=joint)
            control_joints.append(control_joint)

        for j in range(len(rig_types)):
            color = 17 if rig_types[j] == 'fk' else 20
            ctrlShape = 'Circle' if rig_types[j] == 'fk' else 'Square'
            rig_type = rig_types[j]
            scale_size = [size]*3 if rig_type == 'ik' else [size*1.8]*3
            for i in range(len(control_joints)):
                con_joint = control_joints[i]
                normal = (1, 0, 0)
                if world:
                    normal = (0, 1, 0)
                # create control
                ctrl = controller_utils.Icon().create_icon(ctrlShape,
                                                           icon_name=con_joint.replace('jnt', rig_type + '_ctrl'),
                                                           icon_color=color,
                                                           scale=scale_size,
                                                           normal=normal)[0]
                attribute_utils.lock_and_hide(ctrl, channelArray = ["sx", "sy", "sz", "v"])
                group_dict, top, end = rigging_utils.GrpAdd(ctrl, [ctrl+"_offset", ctrl+"_con", ctrl+"_sdk"], 'Up')
                if world:
                    cmds.delete(cmds.pointConstraint(con_joint, group_dict['offset']))
                else:
                    cmds.delete(cmds.parentConstraint(con_joint, group_dict['offset']))
                if rig_type == 'fk':
                    if rig_types == ['fk']:
                        cmds.parentConstraint(ctrl, con_joint, mo=True, w=True)
                    control_dict["fkctrlZeros"].append(group_dict['offset'])
                    control_dict["fkctrls"].append(ctrl)
                    if i != 0:
                        parent(group_dict['offset'], control_dict["fkctrls"][-2])
                if rig_type == 'ik':
                    control_dict["ikctrlZeros"].append(group_dict['offset'])
                    control_dict["ikctrls"].append(ctrl)
        if rig_types == ['ik', 'fk']:
            [cmds.parent(control_dict["ikctrlZeros"][k], control_dict["fkctrls"][k]) for k in
             range(len(control_dict["ikctrlZeros"]))]

        control_dict["ctrlGrp"] = rig_name + prefix + 'ctrl_grp'
        if not objExists(control_dict["ctrlGrp"]):
            control_dict["ctrlGrp"] = cmds.createNode('transform', name=control_dict["ctrlGrp"])
        control_dict['conJnts'] = control_joints
        cmds.parent(control_joints, control_dict["ctrlGrp"])

        if 'fk' in rig_types:
            if 'ik' not in rig_types:
                [cmds.parent(joint, fk_ctrl) for fk_ctrl, joint in zip(control_dict["fkctrls"], control_joints)]
            else:
                [cmds.parent(joint, ik_ctrl) for ik_ctrl, joint in zip(control_dict["ikctrls"], control_joints)]
            cmds.parent(control_dict["fkctrlZeros"][0], control_dict["ctrlGrp"])
        else:
            [cmds.parent(joint, ik_ctrl) for ik_ctrl, joint in
             zip(control_dict["ikctrls"], control_joints)]
            cmds.parent(control_dict["ikctrlZeros"], control_dict["ctrlGrp"])

        return control_dict

    def createNurbsIKFKRig(self, joints, rigTypes, skin_joint_count, size=1.0, prefix='', reverse=False, world=False):
        """
        不创建曲面绑定
        :param joints: 骨骼链
        :param rigTypes: 绑定类型
        :param skin_joint_count: 蒙皮骨骼数量
        :param size: 绑定大小
        :param prefix: 前缀名
        :param reverse: 是否反转方向
        :param world: 世界轴
        :return: 字典
        """
        return_dict = {"skinJointList": [], "planes": [], "follicTransforms": [], "ikctrlZeros": [], "confkgrps": [],
                       "ikctrls": [], "fkctrls": [], "ctrlJnts": [], "uvPins": [], "wireCrvs": []}
        rig_name = cmds.getAttr(joints[0] + ".rigName") + prefix
        if reverse:
            joints.reverse()
        Plane = skeleton.loftSurfaceFromJointList(joints, "z")

        wireCrv, wireHis = cmds.duplicateCurve(Plane + ".u[0]", ch=1, rn=0, local=0, n="%sWireCrv" % rig_name)
        cmds.setAttr(wireCrv + ".visibility", 0)
        cmds.setAttr(wireHis + ".isoparmValue", 0.5)
        return_dict["wireCrvs"].append(wireCrv)

        ctrl_dict = self.createCtrl(rig_name, joints, rigTypes, size=size, prefix=prefix, world=world)
        return_dict["ikctrlZeros"] = ctrl_dict["ikctrlZeros"]
        return_dict["ikctrls"].append(ctrl_dict["ikctrls"])
        return_dict["fkctrls"].append(ctrl_dict["fkctrls"])
        return_dict["ctrlJnts"]= ctrl_dict["conJnts"]
        return_dict["ctrlGrp"] = ctrl_dict['ctrlGrp']

        [attribute_utils.addAttributes(node, "IK_Controller", "bool", value=True, keyable=False) for node in ctrl_dict["ikctrls"]]
        [attribute_utils.addAttributes(node, "FK_Controller", "bool", value=True, keyable=False) for node in ctrl_dict["fkctrls"]]

        confkgrps = []
        if 'fk' in rigTypes:
            confkgrps = self.conFKGrp(ctrl_dict["fkctrlZeros"], ctrl_dict["ctrlGrp"])
        return_dict["confkgrps"] = confkgrps

        axis = cmds.getAttr(joints[0] + ".axis")
        cmds.select(return_dict["wireCrvs"], r=1)
        skin_joints = rope_utils.re_all_joints(skin_joint_count, axis, u'首尾骨骼', rig_name +"skin_" + prefix, False, surface=Plane, world=False, add=False)
        return_dict["skinJointList"] = skin_joints
        rivets = []
        uvs = []
        for i, jnt in enumerate(skin_joints):
            rivet_transform = cmds.createNode("transform", name=jnt.replace("jnt", "rivet"))
            rivets.append(rivet_transform)
            uv_coordinates = rigging_utils.get_uv_at_surface(jnt, Plane)
            uvs.append(uv_coordinates)

        uv_pin = rigging_utils.uvPin(Plane, uvs, follicList=rivets, type="nurbsSurface")
        [cmds.parentConstraint(rivet_transform, jnt, mo=True) for rivet_transform, jnt in zip(rivets, skin_joints)]
        cmds.skinCluster(ctrl_dict["conJnts"], Plane, tsb=True, nw=1, mi=2, dropoffRate=3.0, rui=False)
        return_dict["follicTransforms"] = rivets
        return_dict["uvPins"].append(uv_pin)
        return_dict["planes"].append(Plane)

        return return_dict

    # def unitConvertAndReverse(self, name, driver):
    #     unit = createNode("unitConversion", n=name + "UnitConversion")
    #     unit.conversionFactor.set(0.1)
    #     driver >> unit.input
    #     reverse = node_utils.reverse(unit + ".output", return_plug=False, name=name + "Reverse")
    #     return unit, reverse

    def conFKGrp(self, fkgrps, ctrlGrp):
        """

        :param fkgrps:
        :param ctrlGrp:
        :return:
        """
        confkgrps = []
        for i in range(len(fkgrps)):
            fkgrp = fkgrps[i]
            confkgrp = cmds.createNode("transform", name='con_' + fkgrp, p=fkgrp)
            if i > 0:
                cmds.parent(confkgrp, confkgrps[-1])
            else:
                cmds.parent(confkgrp, ctrlGrp)
            confkgrps.append(confkgrp)
            cmds.connectAttr(confkgrp + '.t', fkgrp + '.t')
            cmds.connectAttr(confkgrp + '.r', fkgrp + '.r')
            cmds.connectAttr(confkgrp + '.s', fkgrp + '.s')

        return confkgrps

    def addStretch(self, follics, ctrlJnts, point_count, show, hidden, scale_group):
        returnNodes = []
        jnts = []
        locs = []
        for j, follic in enumerate(follics):
            confollicUVjnt = cmds.createNode('joint', name='con_' + follic + '_UV_jnt', p=follic)
            cmds.parent(confollicUVjnt, w=True)
            jnts.append(confollicUVjnt)
            loc = cmds.spaceLocator(n='con_' + follic + '_UV_loc')[0]
            cmds.parentConstraint(confollicUVjnt, loc, mo=0)
            locs.append(loc)
        conUVloc_grp = cmds.group(locs, name=locs[0] + '_grp')
        [cmds.parent(jnts[i + 1], jnts[i]) for i in range(len(jnts) - 1)]

        con_follicUV = 'con_' + follics[0].replace('_01_follic', '') + '_ikHandle'
        ikHandleNode = con_follicUV + '_ikHandle'
        cmds.select(jnts[0], jnts[-1], r=True)
        ikHaneldGrp = cmds.ikHandle(sol='ikSplineSolver', scv=False, ns=3, name=con_follicUV + '_ikHandle')
        ikHaneld_crv = ikHaneldGrp[2]
        cmds.rebuildCurve(ikHaneld_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=point_count - 1, d=3, tol=0.01)
        ikHaneld_crv = cmds.rename(ikHaneld_crv, con_follicUV + '_crv')
        ikspline_grp = cmds.group(name=con_follicUV + '_jnt_grp', em=True)
        cmds.parent(jnts[0], ikHandleNode, ikspline_grp)
        cmds.parent(ikHaneld_crv, hidden)
        cmds.parent(ikspline_grp, show)
        cmds.parent(conUVloc_grp, show)
        cmds.parentConstraint(scale_group, ikspline_grp, mo=True)
        cmds.scaleConstraint(scale_group, ikspline_grp, mo=True)
        cmds.setAttr(conUVloc_grp + '.v', 0)

        for i in range(len(follics)):
            follic = follics[i]
            uvPinPlug = cmds.listConnections(follic + '.offsetParentMatrix', scn=True, destination=False, p=True)[0]
            uvPin = uvPinPlug.split('.')[0]
            result = re.search(r"\[(\d+)\]", uvPinPlug).group(1)
            nurbs_Plane = cmds.listConnections(uvPin + '.deformedGeometry', scn=True, destination=False)[0]
            loc = locs[i]
            conUV_prefix = 'con_'
            CPOSF = cmds.createNode('closestPointOnSurface', name=conUV_prefix + follic + 'closestPOSf')
            cmds.connectAttr(nurbs_Plane + '.worldSpace[0]', CPOSF + '.inputSurface')
            cmds.connectAttr(loc + '.translate', CPOSF + '.inPosition')
            blendColorsNode = cmds.createNode('blendColors',
                                              name=conUV_prefix + follic + 'blendColors')
            cmds.setAttr(blendColorsNode + '.blender', 1)
            cmds.connectAttr(CPOSF + '.result.parameterU', blendColorsNode + '.color1.color1R')
            cmds.connectAttr(blendColorsNode + '.output.outputR', "%s.coordinate[%s].coordinateU" % (uvPin, result))

        cmds.skinCluster(ctrlJnts, ikHaneld_crv, tsb=True, nw=1, mi=2, dropoffRate=3.0, rui=False)
        cmds.setAttr(ikspline_grp + ".v", 0)
        cmds.setAttr(ikHaneld_crv + ".v", 0)

        cv_shape = cmds.listRelatives(ikHaneld_crv, ad=True)[0]
        arclenNode = cmds.arclen(ikHaneld_crv, ch=1)
        cv_Info_length = arclenNode + '.arcLength'
        cv_length = cmds.getAttr(cv_Info_length)
        MD01_Node = cmds.createNode('multiplyDivide')
        cmds.setAttr(MD01_Node + '.operation', 2)
        cmds.connectAttr(cv_Info_length, MD01_Node + '.input1.input1X')
        Global_mdNode = cmds.createNode('multiplyDivide', name=scale_group + '_Global_multiplyDivide')
        cmds.setAttr(Global_mdNode + '.input2X', cv_length)
        cmds.connectAttr(scale_group + '.scaleY', Global_mdNode + '.input1.input1X')
        cmds.connectAttr(Global_mdNode + '.outputX', MD01_Node + '.input2X')
        stretchJnts = jnts[1:]
        for i in range(len(stretchJnts)):
            stretchJnt = stretchJnts[i]
            tail_jnt_multiplyDivideName = stretchJnt.split('|')[-1] + '_multiplyDivide'
            jnt_tX_number = cmds.getAttr(stretchJnt + '.translateZ')
            tail_jnt_multiplyDivide = cmds.createNode('multiplyDivide', name=tail_jnt_multiplyDivideName)
            cmds.setAttr(tail_jnt_multiplyDivide + '.input2X', jnt_tX_number)
            cmds.connectAttr(MD01_Node + '.outputX', tail_jnt_multiplyDivide + '.input1.input1X')
            blendNode = cmds.createNode('blendColors', name=stretchJnt.split('|')[-1] + 'blendColors')
            cmds.connectAttr(scale_group + ".up_stretch", blendNode + '.blender')
            cmds.connectAttr(tail_jnt_multiplyDivide + '.outputX', blendNode + '.color1.color1R')
            cmds.setAttr(blendNode + '.color2.color2R', jnt_tX_number)
            baseCondition = cmds.createNode('condition', name=stretchJnt + '_condition0' + str(i + 2))
            cmds.setAttr(baseCondition + '.secondTerm', jnt_tX_number)
            cmds.setAttr(baseCondition + '.operation', 2)
            cmds.connectAttr(blendNode + '.color1.color1R', baseCondition + '.firstTerm')
            cmds.connectAttr(blendNode + '.output.outputR', baseCondition + '.colorIfTrueR')
            cmds.connectAttr(blendNode + '.color1.color1R', baseCondition + '.colorIfFalseR')
            cmds.connectAttr(baseCondition + '.outColorR', stretchJnt + '.translateZ')

        return returnNodes

    def loadAttrCtrl(self, *args):
        selection = cmds.ls(sl=True)
        if selection.__len__() > 1:
            cmds.warning("Select too more objects add attributes!")
            return
        if not selection:
            self.mainUI.attrCtrl_le.setText("")

        self.mainUI.attrCtrl_le.setText(selection[0])

    def loadSetObjects(self, *args):
        selection = cmds.ls(sl=True)
        if not selection:
            self.mainUI.obj_le.setText("")
            return
        self.mainUI.obj_le.setText(str(selection))

    @decorator_utils.one_undo
    def setupDynamics(self, *args):
        prefixName = self.mainUI.prefix_le.text()
        AttrControl = self.mainUI.attrCtrl_le.text()

        if not cmds.objExists(AttrControl): return
        setObjectList = eval(self.mainUI.obj_le.text())
        if not isinstance(setObjectList, list): return

        positionList = [cmds.xform(obj, q=True, t=True, ws=True) for obj in setObjectList]
        aposList = [cmds.xform(obj, q=True, matrix=True, ws=1) for obj in setObjectList]
        self.spring_con = []
        self.spring_aim = []
        self.spring_target = []
        self.spring_cns = []

        for i, obj in enumerate(setObjectList[:-1]):
            spring_addList = rigging_utils.GrpAdd(obj, [obj + "_spring_con", obj + "_spring_cns"], "Up")[0]
            spring_con = spring_addList["con"]
            spring_cns = spring_addList["cns"]
            self.spring_cns.append(spring_cns)
            self.spring_con.append(spring_con)

            spring_aim = rigging_utils.addTransform(spring_con, obj + "_spring_aim" + str(i), aposList[i])
            self.spring_aim.append(spring_aim)

        if cmds.objExists(prefixName + "spring_npo*"):
            cmds.warning("Prefix name object is already exists.")
            return

        for i, v in enumerate(positionList[1:]):
            t = rigging_utils.getTransformFromPos(v)
            if i == 0:
                spring_npo = rigging_utils.addTransform(AttrControl, prefixName + "spring_npo0", t)
            else:
                spring_npo = rigging_utils.addTransform(setObjectList[i - 1], prefixName + "spring_npo" + str(i), t)
            spring_target = rigging_utils.addTransform(spring_npo, prefixName + "spring_target" + str(i), t)
            self.spring_target.append(spring_target)

        attribute_utils.addAttributes(AttrControl, longName=prefixName + "spring_intensity",
                                      niceName=prefixName + "Spring chain intensity", type="double", value=0, min=0,
                                      max=1)

        for i, tar in enumerate(self.spring_target):
            attribute_utils.addAttributes(AttrControl, longName=prefixName + "damping_%s" % i,
                                          niceName=prefixName + "damping_%s" % i,
                                          type="double", value=0.5, min=0, max=1)
        for i, tar in enumerate(self.spring_target):
            attribute_utils.addAttributes(AttrControl, longName=prefixName + "stiffness_%s" % i,
                                          niceName=prefixName + "stiffness_%s" % i,
                                          type="double", value=0.5, min=0, max=1)

        for i, tranCns in enumerate(self.spring_aim):

            aim = cmds.aimConstraint(self.spring_target[i],
                                     tranCns,
                                     worldUpType=2,
                                     worldUpVector=[0, 1, 0],
                                     worldUpObject=self.spring_con[i],
                                     maintainOffset=False)[0]
            a = [1, 0, 0, 0, 1, 0]
            for j, name in enumerate(["aimVectorX",
                                      "aimVectorY",
                                      "aimVectorZ",
                                      "upVectorX",
                                      "upVectorY",
                                      "upVectorZ"]):
                cmds.setAttr(aim + "." + name, a[j])

            oriCns = cmds.orientConstraint(tranCns, self.spring_cns[i], maintainOffset=False)[0]
            for axis in "XYZ":
                cmds.disconnectAttr(oriCns + ".constraintRotate" + axis,
                                    self.spring_cns[i] + ".rotate" + axis)
            cmds.connectAttr(oriCns + ".constraintRotate", self.spring_cns[i] + ".rotate", f=True)

            node = cmds.createNode("mgear_springNode")

            cmds.connectAttr("time1.outTime", node + ".time")
            dm_node = cmds.createNode("decomposeMatrix")
            cmds.connectAttr(self.spring_target[i] + ".parentMatrix", dm_node + ".inputMatrix")
            cmds.connectAttr(dm_node + ".outputTranslate", node + ".goal")

            cm_node = cmds.createNode("composeMatrix")
            cmds.connectAttr(node + ".output", cm_node + ".inputTranslate")

            mm_node = cmds.createNode("multMatrix")

            cmds.connectAttr(cm_node + ".outputMatrix", mm_node + ".matrixIn[0]")
            cmds.connectAttr(self.spring_target[i] + ".parentInverseMatrix", mm_node + ".matrixIn[1]")

            dm_node2 = cmds.createNode("decomposeMatrix")
            cmds.connectAttr(mm_node + ".matrixSum", dm_node2 + ".inputMatrix")
            cmds.connectAttr(dm_node2 + ".outputTranslate", self.spring_target[i] + ".translate")

            cmds.setAttr(node + ".stiffness", 0.5)
            cmds.setAttr(node + ".damping", 0.5)

            blend_node = cmds.createNode("pairBlend")

            cmds.connectAttr(oriCns + ".constraintRotate", blend_node + ".inRotate2")
            cmds.connectAttr(AttrControl + "." + prefixName + "spring_intensity", blend_node + ".weight")

            cmds.disconnectAttr(oriCns + ".constraintRotate",
                                self.spring_cns[i] + ".rotate")

            cmds.connectAttr(blend_node + ".outRotateX", self.spring_cns[i] + ".rotateX")
            cmds.connectAttr(blend_node + ".outRotateY", self.spring_cns[i] + ".rotateY")
            cmds.connectAttr(blend_node + ".outRotateZ", self.spring_cns[i] + ".rotateZ")

            cmds.connectAttr("%s.%sspring_intensity" % (AttrControl, prefixName), node + ".intensity")
            cmds.connectAttr("%s.%sdamping_%s" % (AttrControl, prefixName, i), node + ".damping")
            cmds.connectAttr("%s.%sstiffness_%s" % (AttrControl, prefixName, i), node + ".stiffness")

    def get_selected_joint_chains(self, joints):
        if not joints:
            return 0

        # 筛选根节点（父骨骼不在选中集合中）
        roots = [j for j in joints
                 if not cmds.listRelatives(j, parent=True, type='joint', fullPath=True)
                 or cmds.listRelatives(j, parent=True, fullPath=True)[0] not in joints]

        # 追踪每条骨骼链
        chains = []
        for root in roots:
            chain = []
            queue = [root]
            while queue:
                current = queue.pop(0)
                if current in joints and current not in chain:
                    chain.append(current)
                    # 添加选中的子骨骼
                    queue.extend(
                        [c for c in cmds.listRelatives(current, children=True, type='joint', fullPath=True) or []
                         if c in joints])
            chains.append(chain)

        return chains

    @property
    def rigName(self):
        return self._rigName

    @rigName.setter
    def rigName(self, name):
        self._rigName = name

    @property
    def control_joints(self):
        all_joints = api_utils.get_all_objects_by_type(om.MFn.kJoint)
        control_joints = [joint for joint in all_joints if cmds.attributeQuery("rope_control_joint", node=joint, exists=True)]
        return control_joints

    # @decorator_utils.one_undo
    # def createMotionPath(self, *args):
    #     self.getRigData()
    #     selection = eval(self.rigData["animCurves"])
    #     selection = [PyNode(sel) for sel in selection if objExists(sel)]
    #     selection = [selection[i:i + 2] for i in range(0, len(selection), 2)]
    #     objList = ls(type="transform")
    #     for obj in objList:
    #         if objExists(obj + ".global_grp"):
    #             self.NurbsRigGlobal = obj.nodeName()
    #         if objExists(obj + ".show_grp"):
    #             self.NurbsRigShow = obj.nodeName()
    #         if objExists(obj + ".hidden_grp"):
    #             self.NurbsRigHidden = obj.nodeName()
    #         if objExists(obj + ".follic_grp"):
    #             self.follicgrp = obj
    #         if objExists(obj + ".skin_grp"):
    #             self.skinJntGrp = obj
    #     returnDict = self.createNurbsIKFKRig(selection, self.rigData["motionNumber"], self.rigData["motionNumber"],
    #                                          self.rigData["aimAxis"], self.rigData["upAxis"],
    #                                          self.rigData["motionType"],
    #                                          self.rigData["motionSize"], prefix="Motion")
    #     # create path joints
    #
    #     ctrlJnts = []
    #     confkgrps = []
    #     if objExists(self.NurbsRigGlobal + ".custom_ctrlJnts"):
    #         ctrlJnts = eval(getAttr(self.NurbsRigGlobal + ".custom_ctrlJnts"))
    #     if objExists(self.NurbsRigGlobal + ".custom_confkgrps"):
    #         confkgrps = eval(getAttr(self.NurbsRigGlobal + ".custom_confkgrps"))
    #
    #     for i in range(len(ctrlJnts)):
    #         size = 0
    #         pathJointList = list()
    #         for jnt in ctrlJnts[i][::-1]:
    #             jin = joint(p=xform(jnt, q=True, t=True, ws=True),  # NOQA
    #                         n=self.rigData["rigName"] + str(i) + "_pathikHandleJnt_" + str(size))
    #             pathJointList.append(jin)
    #             size += 1
    #         select((pathJointList[0], pathJointList[-1], returnDict["wireCrvs"][i]), r=1)
    #         IkHandle = ikHandle(sol='ikSplineSolver', ccv=False, pcv=False, roc=True)[0]
    #         IkHandle.dTwistControlEnable.set(1)
    #         IkHandle.dWorldUpType.set(3)
    #         connectAttr(self.NurbsRigGlobal + ".worldMatrix[0]", IkHandle + ".dWorldUpMatrix")
    #
    #         parents = [parentConstraint(joint, conGrp, mo=True) for joint, conGrp in
    #                    zip(pathJointList, confkgrps[i][::-1])]
    #         self.rigNodes.append(parents)
    #
    #         PathCurveRigDoMoveGrp = group(pathJointList[0],
    #                                       n=self.rigData["rigName"] + str(i) + 'PathCurveRigDoMoveGrp')
    #         PathCurveRigDoMoveGrp.v.set(0)
    #         PathCurveRigDoMoveGrp.v.set(lock=1)
    #         PathCurveRigDoMoveGrp.inheritsTransform.set(0)
    #         parent(IkHandle, PathCurveRigDoMoveGrp)
    #         parCon = parentConstraint(self.NurbsRigGlobal, PathCurveRigDoMoveGrp)
    #         scleCon = scaleConstraint(self.NurbsRigGlobal, PathCurveRigDoMoveGrp)
    #         self.rigNodes.append(scleCon)
    #         self.rigNodes.append(parCon)
    #         IkHandle.v.set(0, lock=1)
    #
    #
    #         # 移动组
    #         parent(PathCurveRigDoMoveGrp, self.NurbsRigHidden)


def show_guide_component_manager(*args):
    ui_utils.showDialog(DockableNurbsMainUI, dockable=True)
