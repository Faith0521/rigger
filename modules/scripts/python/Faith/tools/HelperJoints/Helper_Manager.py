import os.path
from imp import reload
from functools import partial
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from Faith.vendor.Qt import QtCore, QtWidgets, QtGui
from maya import cmds
from pymel.core import *
from maya.api import OpenMaya
from Faith.maya_utils import controller_utils as ctrl
from Faith.maya_utils import ui_utils as UI
from Faith.maya_utils import rigging_utils as rig
from Faith.maya_utils import decorator_utils as decorator
from Faith.maya_utils import attribute_utils as attr
from Faith.maya_utils import sdk_utils as sdk
from Faith.maya_utils import vector_utils as vec
from Faith.maya_utils.naming_utils import *
from . import helperUI as ui
import string, json

reload(ui)
reload(ctrl)
reload(UI)
reload(rig)
reload(decorator)
reload(attr)
reload(vec)


class MainUI(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)


class HelperManager(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    """
    主窗口
    """

    def __init__(self, parent=None):
        super(HelperManager, self).__init__(parent=parent)

        self.icon = ctrl.Icon()
        self.mainCorrectiveNetList = []
        self.uiName = "Helper_Manager"
        self.correctiveCtrlsGrp = "BranchSystem"
        self.uiDict = dict()
        self.axisList = ["x", "y", "z"]
        self.start_dir = cmds.workspace(q=True, rootDirectory=True)

        # item ui
        self.mainUI = MainUI()

        # initialize
        self.create_widgets()
        self.create_connections()
        self.refreshList()

    def create_widgets(self):
        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Helper Manager v0.0.2")
        self.resize(325, 492)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.mainUI)
        self.setStyleSheet(UI.qss)

        self.mainUI.NetView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        item = QtWidgets.QAction(self)
        item.setText('Delete')
        item.triggered.connect(self.deleteHelper)
        self.mainUI.NetView.addAction(item)

    def create_connections(self, *args):
        self.mainUI.LoadPb.clicked.connect(partial(self.loadJoint, self.mainUI.LoadLe))
        self.mainUI.ParentPb.clicked.connect(partial(self.loadJoint, self.mainUI.ParentLe))
        self.mainUI.ApplyPb.clicked.connect(self.Generate)  # 生成函数
        self.mainUI.addBtn.clicked.connect(partial(self.Generate, True))
        self.mainUI.NetView.clicked.connect(self.viewItemClick)
        self.mainUI.MirrorPb.clicked.connect(partial(self.mirrorHelperJoint, type="LR"))  # 左 >> 右
        self.mainUI.MirrorPb1.clicked.connect(partial(self.mirrorHelperJoint, type="RL"))  # 右 >> 左
        self.mainUI.RefreshPb.clicked.connect(self.refreshList)  # 刷新列表
        self.mainUI.actionExport_All_Settings.triggered.connect(self.exportSettings)  # 导出所有设置
        self.mainUI.actionImport_Settings.triggered.connect(self.importSettings)  # 导入所有设置
        self.mainUI.actionCreate_TimelineSettings.triggered.connect(partial(self.createAllSettings, type="timeline"))  # 导出所有设置
        self.mainUI.actionCreate_AdvSettings.triggered.connect(partial(self.createAllSettings, type="adv"))  # 导出所有设置

    @decorator.one_undo
    def createAllSettings(self, type="timeline", *args):
        json_file_path = os.path.abspath(__file__ + "/../settings.json")
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            if type in data:
                for joint, ref in data[type].items():
                    if cmds.objExists(joint) and cmds.objExists(ref['parent']):
                        size = ref["distance"]*0.3
                        side = ref['side']
                        primaryAxis = 'x'
                        translate_axis = 'y'
                        if type == "timeline":
                            size = ref["distance"] * 0.1
                            if 'Foot' in joint:
                                primaryAxis = 'y'
                                translate_axis = 'z'
                            elif 'Toe' in joint:
                                size *= 0.7
                                primaryAxis = 'z'
                                translate_axis = 'y'
                        if side != "M" and not ref['isFinger']:
                            root, baseZero, zero = self.addHelperJoint(joint, ref['parent'], primaryAxis=primaryAxis,
                                                    size=size, side=side,
                                                    translate_axis=translate_axis,
                                                    isJointChain=True, add=False)


                        self.refreshList()

    @decorator.one_undo
    def deleteHelper(self, *args):
        if self.mainUI.NetView.selectedIndexes():
            for index in self.mainUI.NetView.selectedIndexes():
                item_name = index.data()
                nodeList = []
                if "_bridge" in item_name:
                    roots = cmds.listConnections(item_name + ".roots", s=1, d=0)
                    nodeList.append(item_name.replace("_bridge", "_HelperGrp"))
                    for root in roots:
                        rootBranchList = cmds.ls("*." + root + "_branchNode")
                        for branch in rootBranchList:
                            nodeList.append(branch.split(".")[0])
                elif "_root" in item_name:
                    rootBranchList = cmds.ls("*." + item_name + "_branchNode")
                    for branch in rootBranchList:
                        nodeList.append(branch.split(".")[0])

                [cmds.delete(node) for node in nodeList if node and cmds.objExists(node)]

        self.refreshList()

    @decorator.one_undo
    def exportSettings(self, *args):
        multipleFilters = "Json Files (*.json);;All Files (*.*)"
        filePath = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=1)[0]
        if not cmds.objExists("BranchSystem"):
            return
        export_dict = {}
        for ch in cmds.listRelatives("BranchSystem", c=1, ad=1):
            if cmds.objExists(ch + ".helperGrp"):
                bridge = ch
                rootInfo = {}

                add_joint = cmds.getAttr(bridge + ".addJoint")
                parent_joint = cmds.getAttr(bridge + ".parentJoint")
                axis = cmds.getAttr(bridge + ".axis")
                tr_axis = cmds.getAttr(bridge + ".translate_axis")
                size = cmds.getAttr(bridge + ".size")
                isJntChain = cmds.getAttr(bridge + ".jointChain")
                rootNodes = cmds.listConnections(bridge + ".roots")

                export_dict[bridge] = {"name": bridge,
                                       "addJoint": add_joint,
                                       "parent_joint": parent_joint,
                                       "axis": axis,
                                       "translate_axis": tr_axis,
                                       "size": size,
                                       "isJointChain": isJntChain,
                                       "rootsInfo": rootInfo}

                for root in rootNodes:
                    rootInfo[root] = {}
                    zero = root.replace("_root", "_zero")
                    base_zero = root.replace("_root", "_base_zero")

                    base_zero_ma = cmds.getAttr(base_zero + ".worldMatrix[0]")
                    zero_ma = cmds.getAttr(zero + ".worldMatrix[0]")

                    rootInfo[root]["base_zero"] = {"name": base_zero, "matrix": base_zero_ma}
                    rootInfo[root]["zero"] = {"name": zero, "matrix": zero_ma}
                    rootInfo[root]["side"] = cmds.getAttr(root + ".side")
                    rootInfo[root]["mirrorMatrix"] = None
                    if cmds.objExists(root + ".isMirror"):
                        rootInfo[root]["mirrorMatrix"] = cmds.getAttr(root + ".worldMatrix[0]")
        with open(filePath, 'w') as json_file:
            json.dump(export_dict, json_file, indent=4)

    @decorator.one_undo
    def importSettings(self, *args):
        if cmds.objExists("BranchSystem"):
            cmds.warning("Object BranchSystem is existing.")
            return

        Mesh = "body"
        selection = cmds.ls(sl=1)
        if selection:
            Mesh = selection[0]

        multipleFilters = "Json Files (*.json);;All Files (*.*)"
        filePath = cmds.fileDialog2(fileFilter=multipleFilters, fileMode=1, dialogStyle=1)[0]

        with open(filePath, 'r') as json_file:
            importData = json.load(json_file)
            for bridge, dictInfo in importData.items():
                addJoint = dictInfo["addJoint"]
                parent_joint = dictInfo["parent_joint"]
                axis = dictInfo["axis"]
                size = dictInfo["size"]
                translate_axis = dictInfo["translate_axis"]
                isJointChain = dictInfo["isJointChain"]
                rootsInfo = dictInfo["rootsInfo"]
                for root, zeroInfo in rootsInfo.items():
                    mirrorMatrix = zeroInfo["mirrorMatrix"]
                    side = zeroInfo["side"]

                    baseZero_ma = zeroInfo["base_zero"]["matrix"]
                    Zero_ma = zeroInfo["zero"]["matrix"]

                    root, baseZero, zero = self.addHelperJoint(addJoint, parent_joint, primaryAxis=axis,
                                                               translate_axis=translate_axis,
                                                               size=size, side=side,
                                                               add=True, isJointChain=isJointChain,
                                                               mirrorRoot=mirrorMatrix, name=root.split("_root")[0])

                    cmds.xform(baseZero, matrix=baseZero_ma, ws=1)
                    cmds.xform(zero, matrix=Zero_ma, ws=1)


        try:
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
        except:
            pass

    def matchPosition(self, Mesh):
        branchDict = {
            "L_ArmA_01_anim_A_zero": 18174,
            "L_ArmA_01_anim_B_zero": 18137,
            "L_ArmA_01_anim_C_zero": 22651,
            "L_ArmA_01_anim_D_zero": 22496,

            "L_ArmB_01_anim_A_zero": 22091,
            "L_ArmB_01_anim_B_zero": 22085,
            "L_ArmB_01_anim_C_zero": 22078,
            "L_ArmB_01_anim_D_zero": 21711,

            "L_Hand_anim_A_zero": 17228,
            "L_Hand_anim_B_zero": 17220,
            "L_Hand_anim_C_zero": 17191,
            "L_Hand_anim_D_zero": 17243,

            "L_LegA_01_anim_A_zero": 20903,
            "L_LegA_01_anim_B_zero": 20457,
            "L_LegA_01_anim_C_zero": 20471,
            "L_LegA_01_anim_D_zero": 20505,

            "L_LegB_01_anim_B_zero": 19512,
            "L_LegB_01_anim_D_zero": 19748,

            "L_Foot_anim_A_zero": 20105,
            "L_Foot_anim_B_zero": 20132,
            "L_Foot_anim_C_zero": 20099,
            "L_Foot_anim_D_zero": 20008,

            "L_Index01_anim_A_zero": 15808,
            "L_Index01_anim_C_zero": 16804,

            "L_Middle01_anim_A_zero": 15777,
            "L_Middle01_anim_C_zero": 16783,

            "L_Ring01_anim_A_zero": 15830,
            "L_Ring01_anim_C_zero": 17059,

            "L_Pinky01_anim_A_zero": 15791,
            "L_Pinky01_anim_C_zero": 17039,

            "L_Thumb02_anim_A_zero": 17864,
            "L_Thumb02_anim_C_zero": 17869,

            "R_ArmA_01_anim_A_zero": 8247,
            "R_ArmA_01_anim_B_zero": 8210,
            "R_ArmA_01_anim_C_zero": 12738,
            "R_ArmA_01_anim_D_zero": 12574,

            "R_ArmB_01_anim_A_zero": 12164,
            "R_ArmB_01_anim_B_zero": 12158,
            "R_ArmB_01_anim_C_zero": 12151,
            "R_ArmB_01_anim_D_zero": 11784,

            "R_Hand_anim_A_zero": 14627,
            "R_Hand_anim_B_zero": 14619,
            "R_Hand_anim_C_zero": 14592,
            "R_Hand_anim_D_zero": 14639,

            "R_LegA_01_anim_A_zero": 10976,
            "R_LegA_01_anim_B_zero": 10530,
            "R_LegA_01_anim_C_zero": 10544,
            "R_LegA_01_anim_D_zero": 10578,

            "R_LegB_01_anim_B_zero": 9585,
            "R_LegB_01_anim_D_zero": 9821,

            "R_Foot_anim_A_zero": 10178,
            "R_Foot_anim_B_zero": 10205,
            "R_Foot_anim_C_zero": 10172,
            "R_Foot_anim_D_zero": 10081,

            "R_Index01_anim_A_zero": 13215,
            "R_Index01_anim_C_zero": 14211,

            "R_Middle01_anim_A_zero": 13184,
            "R_Middle01_anim_C_zero": 14190,

            "R_Ring01_anim_A_zero": 13237,
            "R_Ring01_anim_C_zero": 14466,

            "R_Pinky01_anim_A_zero": 13198,
            "R_Pinky01_anim_C_zero": 14446,

            "R_Thumb02_anim_A_zero": 15253,
            "R_Thumb02_anim_C_zero": 15258
        }

        branchDict_A = {
            "L_ArmA_01_jnt_A_zero": 18174,
            "L_ArmA_01_jnt_B_zero": 18137,
            "L_ArmA_01_jnt_C_zero": 22651,
            "L_ArmA_01_jnt_D_zero": 22496,

            "L_ArmB_01_jnt_A_zero": 22091,
            "L_ArmB_01_jnt_B_zero": 22085,
            "L_ArmB_01_jnt_C_zero": 22078,
            "L_ArmB_01_jnt_D_zero": 21711,

            "L_Hand_jnt_A_zero": 17228,
            "L_Hand_jnt_B_zero": 17220,
            "L_Hand_jnt_C_zero": 17191,
            "L_Hand_jnt_D_zero": 17243,

            "L_LegA_01_jnt_A_zero": 20903,
            "L_LegA_01_jnt_B_zero": 20457,
            "L_LegA_01_jnt_C_zero": 20471,
            "L_LegA_01_jnt_D_zero": 20505,

            "L_LegB_01_jnt_B_zero": 19512,
            "L_LegB_01_jnt_D_zero": 19748,

            "L_Foot_jnt_A_zero": 20105,
            "L_Foot_jnt_B_zero": 20132,
            "L_Foot_jnt_C_zero": 20099,
            "L_Foot_jnt_D_zero": 20008,

            "L_Index01_jnt_A_zero": 15808,
            "L_Index01_jnt_C_zero": 16804,

            "L_Middle01_jnt_A_zero": 15777,
            "L_Middle01_jnt_C_zero": 16783,

            "L_Ring01_jnt_A_zero": 15830,
            "L_Ring01_jnt_C_zero": 17059,

            "L_Pinky01_jnt_A_zero": 15791,
            "L_Pinky01_jnt_C_zero": 17039,

            "L_Thumb02_jnt_A_zero": 17864,
            "L_Thumb02_jnt_C_zero": 17869,

            "R_ArmA_01_jnt_A_zero": 8247,
            "R_ArmA_01_jnt_B_zero": 8210,
            "R_ArmA_01_jnt_C_zero": 12738,
            "R_ArmA_01_jnt_D_zero": 12574,

            "R_ArmB_01_jnt_A_zero": 12164,
            "R_ArmB_01_jnt_B_zero": 12158,
            "R_ArmB_01_jnt_C_zero": 12151,
            "R_ArmB_01_jnt_D_zero": 11784,

            "R_Hand_jnt_A_zero": 14627,
            "R_Hand_jnt_B_zero": 14619,
            "R_Hand_jnt_C_zero": 14592,
            "R_Hand_jnt_D_zero": 14639,

            "R_LegA_01_jnt_A_zero": 10976,
            "R_LegA_01_jnt_B_zero": 10530,
            "R_LegA_01_jnt_C_zero": 10544,
            "R_LegA_01_jnt_D_zero": 10578,

            "R_LegB_01_jnt_B_zero": 9585,
            "R_LegB_01_jnt_D_zero": 9821,

            "R_Foot_jnt_A_zero": 10178,
            "R_Foot_jnt_B_zero": 10205,
            "R_Foot_jnt_C_zero": 10172,
            "R_Foot_jnt_D_zero": 10081,

            "R_Index01_jnt_A_zero": 13215,
            "R_Index01_jnt_C_zero": 14211,

            "R_Middle01_jnt_A_zero": 13184,
            "R_Middle01_jnt_C_zero": 14190,

            "R_Ring01_jnt_A_zero": 13237,
            "R_Ring01_jnt_C_zero": 14466,

            "R_Pinky01_jnt_A_zero": 13198,
            "R_Pinky01_jnt_C_zero": 14446,

            "R_Thumb02_jnt_A_zero": 15253,
            "R_Thumb02_jnt_C_zero": 15258
        }

        branchDict_elo = {
            "L_ArmA_01_jnt_A_zero": 22158,
            "L_ArmA_01_jnt_B_zero": 21863,
            "L_ArmA_01_jnt_C_zero": 12513,
            "L_ArmA_01_jnt_D_zero": 11703,

            "L_ArmB_01_jnt_A_zero": 12548,
            "L_ArmB_01_jnt_B_zero": 12565,
            "L_ArmB_01_jnt_C_zero": 24219,
            "L_ArmB_01_jnt_D_zero": 24307,

            "L_Hand_jnt_A_zero": 12311,
            "L_Hand_jnt_B_zero": 25454,
            "L_Hand_jnt_C_zero": 20544,
            "L_Hand_jnt_D_zero": 21230,

            "L_LegA_01_jnt_A_zero": 14053,
            "L_LegA_01_jnt_B_zero": 14033,
            "L_LegA_01_jnt_C_zero": 14088,
            "L_LegA_01_jnt_D_zero": 13791,

            "L_LegB_01_jnt_B_zero": 13268,
            "L_LegB_01_jnt_D_zero": 13318,

            "L_Foot_jnt_A_zero": 12910,
            "L_Foot_jnt_B_zero": 23030,
            "L_Foot_jnt_C_zero": 13659,
            "L_Foot_jnt_D_zero": 12897,

            "L_Index01_jnt_A_zero": 20227,
            "L_Index01_jnt_C_zero": 12040,

            "L_Middle01_jnt_A_zero": 20167,
            "L_Middle01_jnt_C_zero": 12036,

            "L_Ring01_jnt_A_zero": 20086,
            "L_Ring01_jnt_C_zero": 11860,

            "L_Pinky01_jnt_A_zero": 19958,
            "L_Pinky01_jnt_C_zero": 11837,

            "L_Thumb02_jnt_A_zero": 20738,
            "L_Thumb02_jnt_C_zero": 20652,

            "R_ArmA_01_jnt_A_zero": 17137,
            "R_ArmA_01_jnt_B_zero": 17137,
            "R_ArmA_01_jnt_C_zero": 10789,
            "R_ArmA_01_jnt_D_zero": 10769,

            "R_ArmB_01_jnt_A_zero": 11627,
            "R_ArmB_01_jnt_B_zero": 11656,
            "R_ArmB_01_jnt_C_zero": 19333,
            "R_ArmB_01_jnt_D_zero": 19286,

            "R_Hand_jnt_A_zero": 10618,
            "R_Hand_jnt_B_zero": 24608,
            "R_Hand_jnt_C_zero": 16218,
            "R_Hand_jnt_D_zero": 16161,

            "R_LegA_01_jnt_A_zero": 13906,
            "R_LegA_01_jnt_B_zero": 14176,
            "R_LegA_01_jnt_C_zero": 14195,
            "R_LegA_01_jnt_D_zero": 13860,

            "R_LegB_01_jnt_B_zero": 11549,
            "R_LegB_01_jnt_D_zero": 11540,

            "R_Foot_jnt_A_zero": 11197,
            "R_Foot_jnt_B_zero": 17579,
            "R_Foot_jnt_C_zero": 11238,
            "R_Foot_jnt_D_zero": 11212,

            "R_Index01_jnt_A_zero": 14852,
            "R_Index01_jnt_C_zero": 10119,

            "R_Middle01_jnt_A_zero": 14844,
            "R_Middle01_jnt_C_zero": 10232,

            "R_Ring01_jnt_A_zero": 15090,
            "R_Ring01_jnt_C_zero": 10074,

            "R_Pinky01_jnt_A_zero": 14711,
            "R_Pinky01_jnt_C_zero": 10059,

            "R_Thumb02_jnt_A_zero": 15246,
            "R_Thumb02_jnt_C_zero": 15324
        }
        if cmds.objExists("move_origin_ctrl"):
            for zero, vtxId in branchDict_elo.items():
                vtxPosition = cmds.xform("%s.vtx[%d]" % (Mesh, vtxId), q=1, t=1, ws=1)
                if cmds.objExists(zero):
                    cmds.xform(zero, t=vtxPosition, ws=1)

        else:
            for zero, vtxId in branchDict.items():
                vtxPosition = cmds.xform("%s.vtx[%d]" % (Mesh, vtxId), q=1, t=1, ws=1)
                if cmds.objExists(zero):
                    cmds.xform(zero, t=vtxPosition, ws=1)

            for zero, vtxId in branchDict_A.items():
                vtxPosition = cmds.xform("%s.vtx[%d]" % (Mesh, vtxId), q=1, t=1, ws=1)
                if cmds.objExists(zero):
                    cmds.xform(zero, t=vtxPosition, ws=1)

    def viewItemClick(self, *args):
        if self.mainUI.NetView.selectedIndexes():
            itemName = self.mainUI.NetView.selectedIndexes()[0].data()
            if cmds.objExists(itemName):
                cmds.select(itemName, r=True)

    def refreshList(self):
        objectList = cmds.ls(type="transform")
        helperGrpList = [obj for obj in objectList if cmds.objExists(obj + ".helperGrp")]

        model_base = QtGui.QStandardItemModel(self)

        for grp in helperGrpList:
            itemChild = QtGui.QStandardItem(grp)
            itemChild.setEditable(False)

            rootList = cmds.listConnections(grp + ".roots", s=True, d=False)
            if rootList:
                for ch in rootList:
                    chItem = QtGui.QStandardItem(ch)
                    itemChild.appendRow(chItem)
                    chItem.setEditable(False)
            model_base.appendRow(itemChild)

        self.mainUI.NetView.setModel(model_base)
        self.mainUI.NetView.setHeaderHidden(True)

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

    def UIDict(self):
        self.uiDict = {
            "loadJoint": self.mainUI.LoadLe.text(),
            "parentJoint": self.mainUI.ParentLe.text(),
            "axis": self.mainUI.RoCombo.currentText(),
            "translate_axis": self.mainUI.moveAx_cb.currentText(),
            "size": self.mainUI.SizeSp.value(),
            "side": self.mainUI.side_cb.currentText(),
            "isJointChain": self.mainUI.jntChain_rb.isChecked(),
        }
        return self.uiDict

    @decorator.one_undo
    def Generate(self, add=False, *args):
        # ui info-----------------------------
        uiDict = self.UIDict()
        self.addHelperJoint(uiDict["loadJoint"], uiDict["parentJoint"], primaryAxis=uiDict["axis"],
                            size=uiDict["size"], side=uiDict["side"], translate_axis=uiDict["translate_axis"],
                            isJointChain=uiDict["isJointChain"], add=add)
        self.refreshList()

    def OneToOneCreateParentMatrix(self, targetObj, aimObj, T=True, R=True, S=True, bridge=None, name=""):
        """
        矩阵一对一连接
        :param targetObj:
        :param aimObj:
        :param T:
        :param R:
        :param S:
        :param bridge:
        :param name:
        :return:
        """
        nodeList = []
        parentMult = cmds.createNode("multMatrix", n="%s_parentMM" % aimObj)
        attr.addAttributes(parentMult, name + "_branchNode", "bool", 1, keyable=0)
        nodeList.append(parentMult)
        father_ma = cmds.getAttr(aimObj + ".worldMatrix[0]")
        parent_RevMatrix = cmds.getAttr(targetObj + ".worldInverseMatrix[0]")
        cmds.setAttr(parentMult + ".matrixIn[0]", rig.multiply_matrices(father_ma, parent_RevMatrix), type="matrix")
        if bridge:
            if not cmds.isConnected(targetObj + ".worldMatrix[0]", bridge):
                cmds.connectAttr(targetObj + ".worldMatrix[0]", bridge, f=True)
            cmds.connectAttr(bridge, parentMult + ".matrixIn[1]", f=True)
        else:
            cmds.connectAttr(targetObj + ".worldMatrix[0]", parentMult + ".matrixIn[1]")
        cmds.connectAttr(aimObj + ".parentInverseMatrix[0]", parentMult + ".matrixIn[2]")
        parentDecomp = cmds.createNode("decomposeMatrix", n="%s_parentDPM" % aimObj)
        attr.addAttributes(parentDecomp, name + "_branchNode", "bool", 1, keyable=0)
        nodeList.append(parentMult)
        cmds.connectAttr(parentMult + ".matrixSum", parentDecomp + ".inputMatrix")

        if T:
            cmds.connectAttr(parentDecomp + ".outputTranslate", aimObj + ".translate")

        if S:
            cmds.connectAttr(parentDecomp + ".outputScale", aimObj + ".scale")

        if R:
            fa_quatPr = cmds.createNode("quatProd", n="%s_quatPr" % aimObj)
            attr.addAttributes(fa_quatPr, name + "_branchNode", "bool", 1, keyable=0)
            nodeList.append(fa_quatPr)
            cmds.connectAttr(parentDecomp + ".outputQuat", fa_quatPr + ".input1Quat")
            cmds.setAttr(fa_quatPr + ".input2QuatW", 1)

            fa_quatEu = cmds.createNode("quatToEuler", n="%s_quatEu" % aimObj)
            attr.addAttributes(fa_quatEu, name + "_branchNode", "bool", 1, keyable=0)
            nodeList.append(fa_quatEu)
            cmds.connectAttr(fa_quatPr + ".outputQuat", fa_quatEu + ".inputQuat")
            cmds.connectAttr(aimObj + ".rotateOrder", fa_quatEu + ".inputRotateOrder")
            cmds.connectAttr(fa_quatEu + ".outputRotate", aimObj + ".rotate")

        return nodeList

    def addHelperJoint(self, AddJoint, ParentJoint, primaryAxis='x', translate_axis='y', size=1.0, side="L", add=False,
                       isJointChain=False, mirrorRoot=False,
                       mirror=None, name=None):
        """
        Create helper joints by ui settings.
        :param AddJoint:
        :param ParentJoint:
        :param primaryAxis:
        :param size:
        :param side:
        :param add:
        :param isJointChain:
        :param mirror:
        :param name:
        :return:
        """
        # 创建辅助骨骼设置大组
        if not cmds.objExists("BranchSystem"):
            BranchSystem = cmds.createNode("transform", n="BranchSystem")
            BranchController = cmds.createNode("transform", n="BranchController", p=BranchSystem)
            attr.addAttributes(BranchSystem, "branchNode", "bool", 1, keyable=0)
            attr.addAttributes(BranchController, "branchNode", "bool", 1, keyable=0)

        helperGrp = AddJoint + "_HelperGrp"
        bridge = AddJoint + "_bridge"

        # 创建helper的grp,给bridge组创建属性,记录信息
        if not cmds.objExists(helperGrp):
            helperGrp = cmds.createNode("transform", name=helperGrp, p="BranchController")
            attr.addAttributes(helperGrp, "branchNode", "bool", 1, keyable=0)
        if not cmds.objExists(bridge):
            bridge = cmds.createNode("transform", name=bridge, p=helperGrp)
            attr.addAttributes(bridge, "branchNode", "bool", 1, keyable=0)
            attr.addAttributes(bridge, "rootMatrix", "matrix")
            attr.addAttributes(bridge, "fatherMatrix", "matrix")
            attr.addAttributes(bridge, "jointChain", "bool", False, keyable=0)
            attr.addAttributes(bridge, "helperJoints", 'message', multi=1)
            attr.addAttributes(bridge, "controls", 'message', multi=1)
            attr.addAttributes(bridge, "roots", 'message', multi=1)
            attr.addAttributes(bridge, "addJoint", "string", AddJoint, keyable=False)
            attr.addAttributes(bridge, "parentJoint", "string", ParentJoint, keyable=False)
            attr.addAttributes(bridge, "axis", "string", primaryAxis, keyable=False)
            attr.addAttributes(bridge, "translate_axis", "string", translate_axis, keyable=False)
            attr.addAttributes(bridge, "size", "double", size, keyable=False)
            attr.addAttributes(bridge, "helperGrp", "bool", 1, keyable=False)

        NumberDict = string.ascii_uppercase

        # 检查是否有已经创建的root组, 判断后缀序号
        rootNodes = []
        if cmds.objExists(AddJoint + "*.rootNode"):
            rootNodes = cmds.ls(AddJoint + "*.rootNode")
        index = 0
        if not rootNodes:
            index = 0
        else:
            index = NumberDict.index(rootNodes[0].split(".")[0][-6]) + 1

        cmds.refresh()
        cmds.setAttr(bridge + '.jointChain', isJointChain)
        dis = vec.getDistance2(AddJoint, ParentJoint)
        prefixName = "%s_%s" % (AddJoint, NumberDict[index])

        root, baseZero, zero = "", "", ""

        if add:
            rootNodes = cmds.listConnections(bridge + ".roots") or []
            if name:
                root, baseZero, zero = self.createRootSettings(AddJoint, ParentJoint, helperGrp, rootNodes,
                                                               name, bridge, size, side, jntChain=isJointChain,
                                                               mirror=mirror, mirrorRoot=mirrorRoot)
            else:
                text = ""
                result = cmds.promptDialog(title="Enter Prefix Name", text=prefixName, message='Enter New Name:',
                                           button=['OK', 'Cancel'],
                                           defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
                if result == 'OK':
                    text = cmds.promptDialog(query=True, text=True)
                    root, baseZero, zero = self.createRootSettings(AddJoint, ParentJoint, helperGrp, rootNodes,
                                                                   text, bridge, size, side,
                                                                   jntChain=isJointChain,
                                                                   mirror=mirror, mirrorRoot=mirrorRoot)
                elif result == 'Cancel':
                    text = ''
                    return

        else:
            for i in range(4):
                root, baseZero, zero = self.createRootSettings(AddJoint, ParentJoint, helperGrp, rootNodes,
                                                               "%s_%s" % (AddJoint, NumberDict[index + i]), bridge,
                                                               size, side, index=i,
                                                               jntChain=isJointChain, mirrorRoot=mirrorRoot)
                cmds.setAttr("%s.r%s" % (baseZero, primaryAxis), i * 90)
                cmds.setAttr("%s.t%s" % (zero, translate_axis), size * dis * 0.6)
        return root, baseZero, zero

    def createRootSettings(self, AddJoint, ParentJoint, helperGrp, rootNodes,
                           prefixName, bridge, size, side, index=0, jntChain=False, mirror=None, mirrorRoot=False):
        """
        创建root设置
        :param AddJoint:
        :param ParentJoint:
        :param rootNodes:
        :param helperGrp:
        :param prefixName:
        :param bridge:
        :param size:
        :return:
        """
        root = cmds.createNode("transform", n="%s_root" % prefixName)
        attr.addAttributes(root, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(root, "side", "string", side, keyable=False)
        attr.addAttributes(root, "rootNode", "bool", 1, keyable=False)
        cmds.connectAttr(root + ".message", bridge + ".roots[%d]" % (len(rootNodes) + index), f=True)

        cmds.delete(cmds.parentConstraint(AddJoint, root))
        cmds.parent(root, "BranchController")

        father = cmds.createNode("transform", n="%s_father" % prefixName, p=root)
        origin = cmds.createNode("transform", n="%s_origin" % prefixName, p=root)
        attr.addAttributes(father, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(origin, root + "_branchNode", "bool", 1, keyable=0)

        ctrlSdk2Zero = cmds.createNode("transform", n="%s_base_zero" % prefixName)
        ctrlSdk2 = cmds.createNode("transform", n="%s_base_sdk" % prefixName,
                                   p=ctrlSdk2Zero)
        ctrlZero = cmds.createNode("transform", n="%s_zero" % prefixName, p=ctrlSdk2)

        ctrlSdk = cmds.createNode("transform", n="%s_sdk" % prefixName, p=ctrlZero)
        Ctrl = ctrl.Icon().create_icon("Sphere", icon_name="%s_ctrl" % prefixName,
                                       icon_color=17, scale=(size * 0.5, size * 0.5, size * 0.5))[0]

        attr.addAttributes(ctrlSdk2Zero, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(ctrlSdk2, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(ctrlZero, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(ctrlSdk, root + "_branchNode", "bool", 1, keyable=0)
        attr.addAttributes(Ctrl, root + "_branchNode", "bool", 1, keyable=0)

        cmds.connectAttr(Ctrl + ".message", bridge + ".controls[%d]" % len(rootNodes), f=True)
        attr.addAttributes(Ctrl, "follow", "double", min=0, max=10, value=5, keyable=True)

        # 创建骨骼
        jnt = cmds.createNode("joint", n="%s_Helper" % prefixName, p=Ctrl)
        attr.addAttributes(jnt, root + "_branchNode", "bool", 1)

        if jntChain:  # 是否要P到骨骼里
            cmds.setAttr(jnt + ".visibility", 0)
            skin_jnt = cmds.createNode("joint", name=jnt.replace("_Helper", "_Skin"))
            attr.addAttributes(skin_jnt, root + "_branchNode", "bool", 1, keyable=0)
            cmds.delete(cmds.parentConstraint(jnt, skin_jnt))
            cmds.makeIdentity(skin_jnt, t=1, r=1, apply=1)
            cmds.parent(skin_jnt, AddJoint)
            prc = cmds.parentConstraint(jnt, skin_jnt, mo=True)[0]
            sc = cmds.scaleConstraint(jnt, skin_jnt, mo=True)[0]
            attr.addAttributes(prc, root + "_branchNode", "bool", 1, keyable=0)
            attr.addAttributes(sc, root + "_branchNode", "bool", 1, keyable=0)

        cmds.connectAttr(jnt + ".message", bridge + ".helperJoints[%d]" % (len(rootNodes) + index), f=True)

        cmds.parent(Ctrl, ctrlSdk)
        cmds.delete(cmds.parentConstraint(origin, ctrlSdk2Zero))
        cmds.parent(ctrlSdk2Zero, origin)

        if mirror:
            attrList = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY",
                        "scaleZ"]
            rig.mirror_all_obj(mirror, root)
            attr.addAttributes(root, "isMirror", "bool", 1, keyable=0)
            for at in attrList:
                mirror_base_zero_value = cmds.getAttr(mirror.replace("_root", "_base_zero") + "." + at)
                zero_value = cmds.getAttr(mirror.replace("_root", "_zero") + "." + at)
                cmds.setAttr(ctrlSdk2Zero + "." + at, mirror_base_zero_value)
                cmds.setAttr(ctrlZero + "." + at, zero_value)
        if mirrorRoot:
            cmds.xform(root, matrix=mirrorRoot, worldSpace=True)

        # root/father cnt
        self.OneToOneCreateParentMatrix(AddJoint, root, bridge=bridge + ".rootMatrix", name=root)
        self.OneToOneCreateParentMatrix(ParentJoint, father, bridge=bridge + ".fatherMatrix", name=root)

        multDiv = cmds.createNode("multDoubleLinear", n="%s_offset_mult" % Ctrl)
        attr.addAttributes(multDiv, root + "_branchNode", "bool", 1, keyable=0)
        cmds.connectAttr(Ctrl + ".follow", multDiv + ".input1", f=True)
        cmds.setAttr(multDiv + ".input2", 0.1)

        offset_plus = cmds.createNode("plusMinusAverage", n="%s_offset_plus" % Ctrl)
        attr.addAttributes(offset_plus, root + "_branchNode", "bool", 1, keyable=0)
        cmds.setAttr(offset_plus + ".operation", 2)
        cmds.setAttr(offset_plus + ".input1D[0]", 1)
        cmds.connectAttr(multDiv + ".output", offset_plus + ".input1D[1]", f=True)

        # 旋转约束跟随一半
        orig = cmds.parentConstraint(father, root, origin, mo=True)[0]
        orig = cmds.rename(orig, "%s_prc" % origin)
        attr.addAttributes(orig, root + "_branchNode", "bool", 1, keyable=0)
        cmds.setAttr(orig + ".interpType", 2)
        cmds.connectAttr(multDiv + ".output", orig + ".w0", f=True)
        cmds.connectAttr(offset_plus + ".output1D", orig + ".w1", f=True)

        cmds.refresh()  # 刷新

        cmds.parent(root, helperGrp)

        return root, ctrlSdk2Zero, ctrlZero

    @staticmethod
    def findOherSideObj(obj, key, oppositeKey, find=True):
        i = 0
        keyNum = len(key)
        rightObj = ""
        while i < keyNum:
            if key[i] in obj:
                if find:
                    rightObj = (sdk.checkSymObj(orgObj=[obj], searchFor=key[i],
                                                replaceWith=oppositeKey[i]))
                else:
                    rightObj = obj.replace(key[i], oppositeKey[i])
                break
            else:
                i = i + 1
                if i == keyNum:
                    rightObj = obj
                    break
        return rightObj

    def mirrorInfo(self, obj, LeftKey, RightKey, type="LR", find=True):
        """

        :param type:
        :return:
        """
        oppoObj = None
        if type == "LR":
            oppoObj = self.findOherSideObj(obj, LeftKey, RightKey, find=find)
        elif type == "RL":
            oppoObj = self.findOherSideObj(obj, RightKey, LeftKey, find=find)
        return oppoObj

    def mirrorCenter(self):
        return

    def mirrorSettings(self, obj, type="LR"):
        LeftKey = ['L_', 'lf_', '_L', 'facial_L_', 'left_', 'Left_', '_L_', 'Left', 'L']
        RightKey = ['R_', 'rt_', '_R', 'facial_R_', 'right_', 'Right_', '_R_', 'Right', 'R']

        addJoint = cmds.getAttr(obj + ".addJoint")
        parentJoint = cmds.getAttr(obj + ".parentJoint")

        oppoAddJoint = self.mirrorInfo(addJoint, LeftKey, RightKey, type)
        oppoParentJoint = self.mirrorInfo(parentJoint, LeftKey, RightKey, type)

        axis = cmds.getAttr(obj + ".axis")
        tr_axis = cmds.getAttr(obj + ".translate_axis")
        size = cmds.getAttr(obj + ".size")

        roots = cmds.listConnections(obj + ".roots", s=1, d=0)
        isJointChain = cmds.getAttr(obj + ".jointChain")
        if not roots:
            return

        for root in roots:
            side = cmds.getAttr(root + ".side")
            oppoSideName = self.mirrorInfo(side, LeftKey, RightKey, type, find=False)
            oppoRootName = self.mirrorInfo(root, LeftKey, RightKey, type, find=False)
            if not cmds.objExists(oppoRootName):
                if side != "M":
                    self.addHelperJoint(oppoAddJoint, oppoParentJoint, primaryAxis=axis, translate_axis=tr_axis,
                                        size=size, side=oppoSideName,
                                        add=True, isJointChain=isJointChain,
                                        mirror=root, name=oppoRootName.split("_root")[0])
            else:
                oppoBaseZero = oppoRootName.replace("_root", "_base_zero")
                oppoZero = oppoRootName.replace("_root", "_zero")
                baseZero = root.replace("_root", "_base_zero")
                zero = root.replace("_root", "_zero")

                base_pos = cmds.xform(baseZero, q=1, t=1, os=1)
                base_ro = cmds.xform(baseZero, q=1, rotation=1, os=1)

                zero_pos = cmds.xform(zero, q=1, t=1, os=1)
                zero_ro = cmds.xform(zero, q=1, rotation=1, os=1)

                cmds.xform(oppoBaseZero, t=base_pos, os=1)
                cmds.xform(oppoBaseZero, rotation=base_ro, os=1)
                cmds.xform(oppoZero, t=zero_pos, os=1)
                cmds.xform(oppoZero, rotation=zero_ro, os=1)

    @decorator.one_undo
    def mirrorHelperJoint(self, type="LR", *args):
        if self.mainUI.NetView.selectedIndexes():
            for index in self.mainUI.NetView.selectedIndexes():
                item_name = index.data()
                if not cmds.objExists("%s.helperGrp" % item_name):
                    OpenMaya.MGlobal.displayWarning("Please select bridge to mirror.")
                    return
                self.mirrorSettings(item_name, type)
        self.refreshList()


def show(*args):
    UI.showDialog(HelperManager, dockable=True)
