# -*- coding: utf-8 -*-
import json
import os
import os.path
import re
import sys
from functools import partial, reduce
from imp import reload

import maya.cmds as cmds
import maya.mel as mel

from ...tools import FacsTool as tool
from ...tools.FacsTool import ctrl as ctrl_

try:
    import cPickle
except:
    import _pickle as cPickle

# 导入ui
from ...tools.FacsTool.UI import DigitalFaceUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtCore, QtWidgets, QtGui
from ...maya_utils import ui_utils, decorator_utils, deformer_utils, attribute_utils
from pymel.core import *


reload(DigitalFaceUI)
reload(deformer_utils)
reload(tool)


class ImportWeightsError(Exception):
    """This is user's Exception for import weights """


class DigitalGUI(QtWidgets.QMainWindow, DigitalFaceUI.Ui_MainWindow):
    """
    main ui window
    """

    def __init__(self, parent=None):
        super(DigitalGUI, self).__init__(parent)
        self.setupUi(self)


class DockableDigitalFaceMainUI(MayaQWidgetDockableMixin, QtWidgets.QDialog, ctrl_.ctrlData):

    def __init__(self, parent=None):
        self.ctrlValues = None
        self.ctrlAttrs = None
        self.ctrlNames = None
        self.itemList = None
        self.itemList_reduce = None
        self.itemWidgetList = None
        self.baseFaceList = None
        self.isDoubleClicked = None
        self.skin_Imfile_name = None
        self.gmc_layout = None
        self.uiName = "DigitalFacial"
        super(DockableDigitalFaceMainUI, self).__init__(parent=parent)
        self.blendShapeName = ""
        self.attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        self.weightDataPathDict = {
            "Meta": [tool.scriptPath + "\\faceDataV1", tool.scriptPath + "\\RealFacsData\\meta_template.0013.ma"],
            "Snapper": [tool.scriptPath + "\\faceDataV2", tool.scriptPath + "\\RealFacsData\\hanli_template.ma"]
        }
        self.matchDict = {
            "Meta": {
                "base": [4292, 1221],
                "jaw": [4459, 1388],
                "upTeeth": [5325, 2254],
                "dnTeeth": [10500, 16503],
                "jawEnd": [23432, 20419],
                "L_secCtrlvtxs": [5116, 5120, 10028, 8727, 22249, 22251, 3951, 3934, 7628, 6221, 21253, 3169],
                "m_sec_ctrlvtxs": [12207, 12177]
            },
            "Snapper": {
                "base": [2798, 5857],
                "jaw": [3584, 5103],
                "upTeeth": [1933, 5541],
                "dnTeeth": [1881, 5545],
                "jawEnd": [1018, 4392],
                "L_secCtrlvtxs": [1494, 1699, 2225, 71, 18, 8, 55, 42, 39, 8441, 8421, 8553],
                "m_sec_ctrlvtxs": [8862, 7573]
            }
        }
        self.mainUI = DigitalGUI()

        self.create_window()
        self.create_layout()
        self.init_widget()
        self.create_connections()

    def create_window(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("RealFacs Facial v0.0.1")
        self.resize(400, 550)
        self.setStyleSheet(ui_utils.qss)

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRoundedRect(pixmap.rect(), 8, 8)
        painter.end()

        self.setMask(pixmap.mask())

    def create_layout(self):
        """
        create layouts
        :return:
        """
        self.gmc_layout = QtWidgets.QVBoxLayout()
        self.gmc_layout.addWidget(self.mainUI)
        self.gmc_layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.gmc_layout)

    def init_widget(self):
        self.mainUI.create_btn.setHidden(True)
        self.mainUI.autoMirror_cb.setHidden(True)
        self.mainUI.meshName_le.setHidden(True)
        self.mainUI.export_btn.setHidden(True)
        self.mainUI.create_btn.setHidden(True)
        self.mainUI.weightPath_le.setText(self.weightDataPathDict[self.mainUI.typeCombo.currentText()][0])
        self.baseFaceList = ["Brows", "Eyelid", "Eyelid Follow",
                             "Cheek", "Nose", "lip1", "lip2",
                             "lip3", "lip4", "lip5", "neck"]
        self.itemWidgetList = []
        self.itemList = [[name for data in tool.configData["facePoseList"][item] for name, info in data.items()] for
                         item in self.baseFaceList]
        self.itemList_reduce = reduce(lambda x, y: x + y, self.itemList)  # 将每个表情列表中的表情加到一起变成一个整的列表，用来给每个表情加上序号
        self.itemList = [["%s: %s" % (self.itemList_reduce.index(item) + 1, item) for i, item in enumerate(itemList) if
                          item in self.itemList_reduce] for itemList in self.itemList]
        self.TreeViewModelCreate(self.baseFaceList, self.itemList, self.mainUI.treeViewBase)
        self.TreeViewModelCreate([list(tool.configData["CombinFacePoseList"][i].keys())[0]
                                  for i in range(len(tool.configData["CombinFacePoseList"]))],
                                 treeView=self.mainUI.comBineViewBase)

    def create_connections(self):
        self.mainUI.treeViewBase.clicked.connect(
            partial(self.editfacePose, self.mainUI.treeViewBase))
        self.mainUI.comBineViewBase.clicked.connect(
            partial(self.editfacePose, self.mainUI.comBineViewBase))
        self.mainUI.treeViewBase.selectionModel().selectionChanged.connect(
            partial(self.editfacePose, self.mainUI.treeViewBase))
        self.mainUI.comBineViewBase.selectionModel().selectionChanged.connect(
            partial(self.editfacePose, self.mainUI.comBineViewBase))
        self.mainUI.value_dp.valueChanged.connect(self.SpinValChange)
        self.mainUI.value_slider.valueChanged.connect(self.SliderValueChange)

        self.mainUI.select_btn.clicked.connect(self.selectCurrentCtrl)

        self.mainUI.value_dp2.valueChanged.connect(self.SpinValChange2)
        self.mainUI.value_slider2.valueChanged.connect(self.SliderValueChange2)

        self.mainUI.changeShape_btn.clicked.connect(self.faceCtrlShapeEdit)
        self.mainUI.follicleScl_btn.clicked.connect(self.con_all_filloc)
        self.mainUI.createSec_btn.clicked.connect(self.facesecCtrl)
        self.mainUI.splitAll_btn.clicked.connect(self.faceSplit_all)
        self.mainUI.ImpWeight_btn.clicked.connect(self.import_skin_weights)
        self.mainUI.rUplash_btn.clicked.connect(partial(self.create_eyelash, 'R_eyelash_up'))
        self.mainUI.lUplash_btn.clicked.connect(partial(self.create_eyelash, 'L_eyelash_up'))
        self.mainUI.rDnlash_btn.clicked.connect(partial(self.create_eyelash_dn, 'R_eyelash_dn'))
        self.mainUI.lDnlash_btn.clicked.connect(partial(self.create_eyelash_dn, 'L_eyelash_dn'))
        self.mainUI.lBr_btn.clicked.connect(partial(self.create_browJnt, 'L'))
        self.mainUI.rBr_btn.clicked.connect(partial(self.create_browJnt, 'R'))

        self.mainUI.lUpshadow_btn.clicked.connect(partial(self.create_eyelash_dn, 'L_eyeshadow_up'))
        self.mainUI.lDnshadow_btn.clicked.connect(partial(self.create_eyelash_dn, 'L_eyeshadow_dn'))
        self.mainUI.rUpshadow_btn.clicked.connect(partial(self.create_eyelash_dn, 'R_eyeshadow_up'))
        self.mainUI.rDnshadow_btn.clicked.connect(partial(self.create_eyelash_dn, 'R_eyeshadow_dn'))

        self.mainUI.exp_btn.clicked.connect(self.face_secCtrl_Constraints)
        self.mainUI.ShowLoc_btn.clicked.connect(partial(self.locVis, 1))
        self.mainUI.HideLoc_btn.clicked.connect(partial(self.locVis, 0))
        # self.mainUI.actionFaceUpdate.triggered.connect(self.face_updata)

        self.mainUI.weightPath_btn.clicked.connect(self.changePath)
        self.mainUI.typeCombo.currentTextChanged.connect(self.changeWeightPath)
        self.mainUI.export_btn.clicked.connect(self.Export_bsWeight)
        self.mainUI.faceMdl_btn.clicked.connect(partial(self.loadMesh, self.mainUI.faceMdl_le))
        self.mainUI.origMdl_btn.clicked.connect(partial(self.loadMesh, self.mainUI.origMdl_le))
        self.mainUI.create_btn.clicked.connect(self.createBsMesh)

        self.mainUI.ctrl_freezBtn.clicked.connect(self.faceCtrlReturnsDefault)
        self.mainUI.split_btn.clicked.connect(self.faceSplit)
        self.mainUI.mirrorBtn.clicked.connect(self.mirrorMesh)
        self.mainUI.autoMirror_cb.toggled.connect(self.autoMirror)

        self.mainUI.shaderPath_btn.clicked.connect(self.loadDX11)
        self.mainUI.diffuse_mapBtn.clicked.connect(
            partial(self.importFilePath, "face_dx11_diffuse_map", self.mainUI.diffuse_mapLe))
        self.mainUI.normal_mapBtn.clicked.connect(
            partial(self.importFilePath, "face_dx11_normal_map", self.mainUI.normal_mapLe))
        self.mainUI.wrinkleColor_btn.clicked.connect(
            partial(self.importFilePath, "face_dx11_wrinkle_color", self.mainUI.wrinkleColor_le))
        self.mainUI.wrinkleNormal_btn.clicked.connect(
            partial(self.importFilePath, "face_dx11_wrinkle_normal", self.mainUI.wrinkleNormal_le))
        self.mainUI.mask_btn.clicked.connect(self.face_control_to_Mask_expression)
        self.mainUI.anim_btn.clicked.connect(self.face_control_to_MaskAniAttr_expression)

        self.mainUI.temp_list.itemDoubleClicked.connect(partial(self.loadGeometry, self.mainUI.temp_list))
        self.mainUI.replace_list.itemDoubleClicked.connect(partial(self.loadGeometry, self.mainUI.replace_list))
        self.mainUI.ImportBtn.clicked.connect(self.importFile)
        self.mainUI.match_btn.clicked.connect(self.autoMatch)
        self.mainUI.replace_btn.clicked.connect(self.replace)
        self.mainUI.mirrorLR.clicked.connect(partial(self.mirrorType2, 1))
        self.mainUI.mirrorRL.clicked.connect(partial(self.mirrorType2, 2))
        self.mainUI.addBs_btn.clicked.connect(self.addBsNode)
        self.mainUI.ExpBs_btn.clicked.connect(self.Export_bsWeight)
        self.mainUI.ImBs_btn.clicked.connect(self.Import_bsWeight2)

    @decorator_utils.one_undo
    def faceCtrlShapeEdit(self, *args):  # 表情控制器mesh形态换成crv
        mel.eval('''reflectionSetMode none;''')

        for ctrl in tool.face_ctrls:
            if cmds.listRelatives(ctrl, s=True):
                cmds.delete(cmds.listRelatives(ctrl, s=True)[0])
            if ctrl == 'Jaw_cntr':
                ctrColor = 17
            elif ctrl == 'Mouth_cntr':
                ctrColor = 13
            else:
                ctrColor = 6
            if ctrl in ['BrowIn_L_cntr', 'BrowIn_R_cntr']:
                offsetTs = [0, 0, 0.5]
            elif ctrl in ['BrowOut_L_cntr']:
                offsetTs = [0.3, 0, 0.5]
            elif ctrl in ['BrowOut_R_cntr']:
                offsetTs = [-0.3, 0, 0.5]

            elif ctrl in ['UprLid_L_cntr', 'UprLid_R_cntr']:
                offsetTs = [0, 0.3, 0.2]
            elif ctrl in ['LwrLid_L_cntr', 'LwrLid_R_cntr']:
                offsetTs = [0, -0.3, 0.1]

            elif ctrl in ['Jaw_cntr']:
                offsetTs = [0, -0.3, 0.3]
            elif ctrl in ['Cheek_L_2_cntr']:
                offsetTs = [0.3, 0, 0]
            elif ctrl in ['Cheek_R_2_cntr']:
                offsetTs = [-0.3, 0, 0]
            else:
                offsetTs = [0, 0, 0.2]
            ctrl = self.ctrlCreate(ctrl, 'C00_sphere', 'Add', ctrColor, offsetTs, [0, 0, 0], 0.15)
        cmds.select(cl=True)

    @decorator_utils.one_undo
    def create_eyelash(self, jntPrefix, *args):
        crv = selected()[0]
        jnts = self.crvToJnt(crv, jntPrefix)
        setAttr(jnts[-1] + '.jointOrient', 0, 0, 0)

        ctrl_grp = jntPrefix + 'ctrl_grp'
        if cmds.objExists(ctrl_grp) != True:
            ctrl_grp = cmds.group(name=ctrl_grp, em=True)
        for jnt in jnts:
            jnt = jnt.name()
            ctrl = self.ctrlCreate(jnt.replace('_jnt', '_ctrl'), 'C00_sphere', 'Create', 18, [0, -0.05, 0], [0, 0, 0],
                                   0.03)
            ctrl_sdk = cmds.group(ctrl, name=ctrl + '_sdk', em=True)
            ctrl_con = cmds.group(ctrl_sdk, name=ctrl + '_con')
            ctrl_zero = cmds.group(ctrl_con, name=ctrl + '_zero')
            for attr in ['sx', 'sy', 'sz', 'v']:
                cmds.setAttr(ctrl + '.' + attr, lock=1, keyable=0)
            cmds.parent(ctrl, ctrl_sdk)
            cmds.delete(cmds.parentConstraint(jnt, ctrl_zero, mo=0))
            cmds.parentConstraint(ctrl, jnt, mo=1)
            cmds.parent(ctrl_zero, ctrl_grp)

    def create_eyelash_dn(self, jntPrefix):
        crv = selected()[0]
        jnts = self.crvToJnt(crv, jntPrefix)
        # cmds.joint(jnts[0],e = True,oj = 'xyz',secondaryAxisOrient = 'yup',ch = True,zso = True)
        setAttr(jnts[-1] + '.jointOrient', 0, 0, 0)
        select(jnts[0])

    def crvToJnt(self, crv, jntPrefix):
        # crvs = cmds.ls(sl = True)
        # crv = crvs[0]
        select(cl=True)
        crvep = crv.ep
        jnts = []
        for i in range(len(crvep)):
            ep = crvep[i]
            cv_num_world = xform(ep, ws=1, q=1, t=1)  # 获取cv点得空间位置
            jnt = joint(n=jntPrefix + '_0' + str(i + 1) + '_jnt', p=(cv_num_world))  # 创建骨骼
            jnt.radius.set(0.03)
            jnts.append(jnt)
        return jnts

    def import_skin_weights(self, *args):
        """
        导出权重
        @param args:
        @return:
        """
        self.skin_Imfile_name = self.mainUI.weightPath_le.text() + "\\head.skin"
        # tool.scriptPath + "\\head.skin"
        cmds.file(self.skin_Imfile_name, i=1, type="skin", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False,
                  rpr="head", pr=1, importTimeRange="combine")

    @decorator_utils.one_undo
    def create_browJnt(self, side='L', *args):
        """
        创建眉毛骨骼
        @param side:
        @param args:
        @return:
        """
        sel = selected()[0]
        sel.visibility.set(0)
        jntPrefix = side + '_brow'
        if objectType(sel) == 'joint':
            jnts = self.jntTojnt(sel, jntPrefix)
        elif objectType(listRelatives(sel, s=True)[0]) == 'nurbsCurve':
            jnts = self.crvToJnt(sel, jntPrefix)
        self.jntToLowmodel_1(jnts)
        # cmds.joint(jnts[0],e = True,oj = 'xyz',secondaryAxisOrient = 'yup',ch = True,zso = True)
        setAttr(jnts[-1] + '.jointOrient', 0, 0, 0)

    def jntTojnt(self, seljnt, jntPrefix):
        select(cl=True)
        jnts = []
        if objectType(seljnt) == 'joint':
            jnts1 = listRelatives(seljnt, ad=True, f=True)
            jnts1.append(seljnt)
            jnts1 = jnts1[::-1]
            for i in range(len(jnts1)):
                jnt = jnts1[i]
                jnt_t = xform(jnt, q=True, ws=True, t=True)
                jnt = joint(name=jntPrefix + '_0' + str(i + 1) + '_jnt', p=jnt_t)
                jnts.append(jnt)
                cmds.setAttr(jnt + '.radius', 0.03)
        return jnts

    def jntToLowmodel_1(self, jnts):
        """

        @param jnts:
        @return:
        """
        parent(jnts[1:], w=True)
        jntwsList = []
        for jnt in jnts:
            jntws = xform(jnt, q=True, ws=True, t=True)
            jntwsList.append(jntws)
        model_low = polyCreateFacet(ch=1, tx=1, s=1, p=jntwsList)[0]
        mel.eval('DeleteHistory;')
        skinCluster(jnts, model_low, mi=1, rui=False, tsb=True)
        [parent(jnts[i], jnts[i - 1]) for i in range(len(jnts)) if i > 0]

        return model_low

    @decorator_utils.one_undo
    def face_secCtrl_Constraints(self, *args):
        """

        @param args:
        @return:
        """
        face_secCtrl_Constraints_exprName = ls('face_secCtrl_Constraints', type='expression')
        if face_secCtrl_Constraints_exprName:
            delete(face_secCtrl_Constraints_exprName)

        secCtrl_Constraints_expressionStr = ''
        for face_sec_ctrl in tool.face_sec_ctrls:
            if objExists(face_sec_ctrl):
                secCtrl_Constraints_expressionStr += face_sec_ctrl + '_con.translateX = - ' + face_sec_ctrl + '.translateX;\n'
                secCtrl_Constraints_expressionStr += face_sec_ctrl + '_con.translateY = - ' + face_sec_ctrl + '.translateY;\n'
                secCtrl_Constraints_expressionStr += face_sec_ctrl + '_con.translateZ = - ' + face_sec_ctrl + '.translateZ;\n'
        expression(s=secCtrl_Constraints_expressionStr, name='face_secCtrl_Constraints', ae=True, uc=all)

    @decorator_utils.one_undo
    def faceSplit_all(self, *args):
        """

        :param args:
        :return:
        """
        origModel = self.mainUI.origMdl_le.text()
        bsweightPath = self.mainUI.weightPath_le.text()
        self.blendShapeName = self.blendShapeNode(PyNode(self.mainUI.faceMdl_le.text()))[0]
        BlendShape = self.blendShapeName
        tars = listAttr(BlendShape + '.weight', multi=True)

        # 运行前判断-----------------------------------------------------------------------------
        if objExists(origModel) != True:
            cmds.warning(u'org模型不存在: ' + origModel)
            return
        #
        if os.path.exists(bsweightPath) != True:
            cmds.warning(u'{0}权重路径不存在'.format(bsweightPath))
            return

        # 获取表情信息
        # print(self.itemList_reduce)
        self.splitSingleFace("brows_up", origModel, bsweightPath)
        self.splitSingleFace("brows_dn", origModel, bsweightPath)
        self.splitSingleFace("brows_squez", origModel, bsweightPath)
        self.splitSingleFace("brows_squez_up", origModel, bsweightPath)
        self.splitSingleFace("eye_blink_b", origModel, bsweightPath)
        self.splitSingleFace("eye_blink_a", origModel, bsweightPath)
        self.splitSingleFace("upr_lid_dn_b", origModel, bsweightPath)
        self.splitSingleFace("upr_lid_dn_a", origModel, bsweightPath)
        self.splitSingleFace("upr_lid_up", origModel, bsweightPath)
        self.splitSingleFace("lwr_lid_dn", origModel, bsweightPath)
        self.splitSingleFace("lwr_lid_up", origModel, bsweightPath)
        self.splitSingleFace("lwr_lid_out", origModel, bsweightPath)
        self.splitSingleFace("double_eyelid_up", origModel, bsweightPath)
        self.splitSingleFace("double_eyelid_dn", origModel, bsweightPath)
        self.splitSingleFace("blink_brs_up", origModel, bsweightPath)
        self.splitSingleFace("blink_brs_dn", origModel, bsweightPath)
        self.splitSingleFace("eye_squint", origModel, bsweightPath)
        self.splitSingleFace("eye_sqz", origModel, bsweightPath)
        self.splitSingleFace("eye_squint_blink", origModel, bsweightPath)
        self.splitSingleFace("eye_look_up", origModel, bsweightPath)
        self.splitSingleFace("eye_look_dn_b", origModel, bsweightPath)
        self.splitSingleFace("eye_look_dn_a", origModel, bsweightPath)
        self.splitSingleFace("eye_look_out", origModel, bsweightPath)
        self.splitSingleFace("eye_look_out_mid", origModel, bsweightPath)
        self.splitSingleFace("eye_look_in", origModel, bsweightPath)
        self.splitSingleFace("eye_look_in_mid", origModel, bsweightPath)
        self.splitSingleFace("cheek_raise", origModel, bsweightPath)
        self.splitSingleFace("puff", origModel, bsweightPath)
        self.splitSingleFace("suck", origModel, bsweightPath)
        self.splitSingleFace("puff_up", origModel, bsweightPath)
        self.splitSingleFace("puff_dn", origModel, bsweightPath)
        self.splitSingleFace("cheekRaise_Eblink", origModel, bsweightPath)
        self.splitSingleFace("nose_open", origModel, bsweightPath)
        self.splitSingleFace("nose_close", origModel, bsweightPath)
        self.splitSingleFace("nose_dn", origModel, bsweightPath)
        self.splitSingleFace("sneer_only", origModel, bsweightPath)
        self.splitSingleFace("nasolabial_deep", origModel, bsweightPath)
        self.splitSingleFace("funel", origModel, bsweightPath)
        self.splitSingleFace("disgust", origModel, bsweightPath)
        self.splitSingleFace("disgust_close", origModel, bsweightPath)
        self.splitSingleFace("grin", origModel, bsweightPath)
        self.splitSingleFace("pull", origModel, bsweightPath)
        self.splitSingleFace("grin_pull", origModel, bsweightPath)
        self.splitSingleFace("pull_close", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_up", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_dn", origModel, bsweightPath)
        self.splitSingleFace("sneer_close", origModel, bsweightPath)
        self.splitSingleFace("jaw_drop", origModel, bsweightPath)
        self.splitSingleFace("jaw_drop_mid", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_drop_mid", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_drop", origModel, bsweightPath)
        self.splitSingleFace("smile", origModel, bsweightPath)
        self.splitSingleFace("smile_open", origModel, bsweightPath)
        self.splitSingleFace("smile_close", origModel, bsweightPath)
        self.splitSingleFace("dimple", origModel, bsweightPath)
        self.splitSingleFace("stretch", origModel, bsweightPath)
        self.splitSingleFace("tight", origModel, bsweightPath)
        self.splitSingleFace("corners_close", origModel, bsweightPath)
        self.splitSingleFace("smile_drop", origModel, bsweightPath)
        self.splitSingleFace("grin_pull_drop", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_up_drop", origModel, bsweightPath)
        self.splitSingleFace("frown", origModel, bsweightPath)
        # self.splitSingleFace("sticky_lips", origModel, bsweightPath)
        self.splitSingleFace("jaw_l", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_mov_l", origModel, bsweightPath)
        self.splitSingleFace("jaw_r", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_mov_r", origModel, bsweightPath)
        self.splitSingleFace("jaw_fwd", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_fwd", origModel, bsweightPath)
        self.splitSingleFace("jaw_back", origModel, bsweightPath)
        self.splitSingleFace("lip_lk_back", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_tension", origModel, bsweightPath)
        self.splitSingleFace("mouth_tension", origModel, bsweightPath)
        self.splitSingleFace("mouth_press", origModel, bsweightPath)
        self.splitSingleFace("m_1", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_funl_l", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_funl_r", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_mov_l", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_mov_r", origModel, bsweightPath)
        self.splitSingleFace("mouth_mov_up", origModel, bsweightPath)
        self.splitSingleFace("mouth_mov_up_2", origModel, bsweightPath)
        self.splitSingleFace("mouth_mov_up_3", origModel, bsweightPath)
        self.splitSingleFace("mouth_dn", origModel, bsweightPath)
        self.splitSingleFace("mouth_mov_l", origModel, bsweightPath)
        self.splitSingleFace("mouth_mov_r", origModel, bsweightPath)
        self.splitSingleFace("h", origModel, bsweightPath)
        self.splitSingleFace("h_wide", origModel, bsweightPath)
        self.splitSingleFace("h_close", origModel, bsweightPath)
        self.splitSingleFace("o", origModel, bsweightPath)
        self.splitSingleFace("o_wide", origModel, bsweightPath)
        self.splitSingleFace("kiss", origModel, bsweightPath)
        self.splitSingleFace("h_drop", origModel, bsweightPath)
        self.splitSingleFace("upr_lip_in", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_in", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_in_drop", origModel, bsweightPath)
        self.splitSingleFace("chin_up", origModel, bsweightPath)
        self.splitSingleFace("chin_dn", origModel, bsweightPath)
        self.splitSingleFace("jaw_clench", origModel, bsweightPath)
        self.splitSingleFace("lip_back", origModel, bsweightPath)
        self.splitSingleFace("lwr_lip_out", origModel, bsweightPath)
        self.splitSingleFace("lip_volume", origModel, bsweightPath)
        self.splitSingleFace("neck_tension", origModel, bsweightPath)
        self.splitSingleFace("neck_blow", origModel, bsweightPath)
        self.splitSingleFace("neck_slide", origModel, bsweightPath)
        self.splitSingleFace("neck_muscle", origModel, bsweightPath)
        self.splitSingleFace("tension_drop", origModel, bsweightPath)

    def splitSingleFace(self, fasePose, origModel, bsweightPath):
        poseData = self.getPoseInformation(fasePose)
        [setAttr(poseData["ctrlNames"][i] + poseData["ctrlAttrs"][i], poseData["ctrlValues"][i]) for i in
         range(len(poseData["ctrlNames"]))]
        if objExists(fasePose):
            select(fasePose)
            cmds.warning(u'有物体和整体表情重命名，无法拆分：{0}'.format(fasePose))
            return

        notExistsSubFace = [subFace for subFace in poseData["subFaces"] if not objExists(subFace)]

        if notExistsSubFace:
            cmds.warning(u'组合反减表情模型不存在，无法拆分:---' + str(notExistsSubFace))
            return

        splitTargetExistsList = []
        faceSplitNum = len(poseData["weightDataSplitList"])
        for i in range(faceSplitNum):  # 循环方位['l-r','out_l-in_l','out_r-in_r']
            weightDataSplit = poseData["weightDataSplitList"][i]
            Splitweight = poseData["weightDataSplitList"][i]
            weightUDLRs = weightDataSplit.split('-')  # ['l','r']#拆分方位
            for weightUDLR in weightUDLRs:
                if objExists(weightUDLR):
                    splitTargetExistsList.append(weightUDLR)
        if splitTargetExistsList:
            select(splitTargetExistsList)
            cmds.warning(u'有物体和拆分表情重命名，无法拆分:---' + str(splitTargetExistsList))
            return
        # ------------------------------------------------------------------------------------------
        origModelVisValue = getAttr(origModel + '.v')
        if origModelVisValue == 0:  # 显示org模型
            setAttr(origModel + '.v', 1)
        face_bs_grp = 'IMM_face_bs_grp'
        if objExists(face_bs_grp) != True:
            group(name=face_bs_grp, em=True)
        faceAreas = []
        faceArea_grp = fasePose + '_face_bs_grp'
        if objExists(faceArea_grp) != True:
            faceArea_grp = group(name=faceArea_grp, em=True)
            parent(faceArea_grp, face_bs_grp)
        else:
            setAttr(faceArea_grp + '.tx', 0)
        copy_model = self.copyFaceModel(True, fasePose)
        if objExists(fasePose) != True:  # 整体表情
            combinFace = duplicate(origModel, name=fasePose)[0]
            self.createBlendShape3(copy_model, combinFace, 1)
            setAttr(combinFace + '.t', 0, 0, 0)
            parent(combinFace, faceArea_grp)
            if poseData["subFaces"] != []:
                setAttr(combinFace + '.tx', 15)
                addcombinFace = duplicate(origModel, name=fasePose + '_add')[0]
                setAttr(addcombinFace + '.t', 0, 0, 0)
                parent(addcombinFace, faceArea_grp)
                self.createBlendShape(addcombinFace, PyNode(fasePose), 1)
                for i in range(len(poseData["subFaces"])):
                    subFace = poseData["subFaces"][i]
                    subFaceValue = poseData["subFaceValues"][i]
                    self.createBlendShape(subFace, PyNode(fasePose), subFaceValue)
        if poseData["weightDataSplitList"]:  # 判断是否需要拆分
            faceSplitNum = len(poseData["weightDataSplitList"])
            for i in range(faceSplitNum):  # 循环方位['l-r','out_l-in_l','out_r-in_r']
                weightDataSplit = poseData["weightDataSplitList"][i]
                Splitweight = poseData["SplitweightList"][i]
                weightUDLRs = weightDataSplit.split('-')  # ['l','r']#拆分方位
                weightData = Splitweight  # 拆分权重

                face1 = weightUDLRs[0]  # 刷权重的模型
                face2 = weightUDLRs[1]  # 反减出来的模型
                faceSplitNum = i
                if i == 0:
                    faceAreas.append(face1)
                    faceAreas.append(face2)
                if i == 1:
                    fasePose = faceAreas[0]
                if i == 2:
                    fasePose = faceAreas[1]
                self.splitFace_edit(fasePose, origModel, bsweightPath, weightData, face1, face2, faceSplitNum,
                                    faceArea_grp)

        else:
            weightData = ''
            face1 = ''
            face2 = ''
            faceSplitNum = 0
            self.splitFace_edit(fasePose, origModel, bsweightPath, weightData, face1, face2, faceSplitNum,
                                faceArea_grp)

        setAttr(faceArea_grp + '.tx', 65)
        setAttr(origModel + '.v', origModelVisValue)
        parent(copy_model, faceArea_grp)
        self.freezeFacePose()

    def sel_ad_type(self, objs, selTypes):
        # objs = cmds.ls(sl = True)
        grp_ads = []
        for grp in objs:
            for selType in selTypes:
                selTypeObjs = cmds.listRelatives(grp, ad=True, type=selType, f=True)
                if selTypeObjs != None:
                    grp_ads = grp_ads + selTypeObjs
        return grp_ads

    @decorator_utils.one_undo
    def con_all_filloc(self):
        """
        约束所有毛囊
        @return:
        """
        self.locVis(1)
        if not cmds.objExists('face_head_global'):
            cmds.error(u'face_head_global------不存在，无法运行')
        follicShapes = cmds.ls(type='follicle')
        ExistsScaleFolics = []
        newConFollic = []
        follics = []
        for follicShape in follicShapes:
            follic = cmds.listRelatives(follicShape, p=True)[0]
            scaleNode = self.sel_ad_type([follic], ['scaleConstraint'])
            follics.append(follic)
            if not scaleNode:
                cmds.scaleConstraint('face_head_global', follic)
                newConFollic.append(follic)
            else:
                ExistsScaleFolics.append(follic)
        if ExistsScaleFolics:
            cmds.warning(u'以下毛囊之前已经存在缩放约束------\ncmds.select(' + str(ExistsScaleFolics) + ')')
        if ExistsScaleFolics:
            cmds.warning(u'已经被约束过的----\ncmds.select(' + str(ExistsScaleFolics) + ')')
        if newConFollic:
            cmds.warning(u'新约束的毛囊------' + str(newConFollic))
            cmds.select(newConFollic)
        else:
            cmds.warning(u'所有毛囊都已经被约束过，没有需要约束的毛囊')
            cmds.warning(u'所有毛囊---\ncmds.select(' + str(follics) + ')')

    @staticmethod
    def getPoseInformation(pose):
        """

        :param pose:
        :return:
        """
        poseInfoDict = dict()
        splitface_grp = pose + '_face_bs_grp'
        if objExists(splitface_grp):
            setAttr(splitface_grp + '.v', 0)

        data = [info for key, value in tool.configData["facePoseList"].items()
                for info in value if pose in info]
        poseData = tool.getPoseData(data[0], pose)

        poseInfoDict["ctrlNames"] = poseData[0]  # 控制器
        poseInfoDict["ctrlAttrs"] = poseData[1]  # 控制器属性
        poseInfoDict["ctrlValues"] = poseData[2]  # 控制器数值
        poseInfoDict["weightDataSplitList"] = poseData[3]  # 拆分列表
        poseInfoDict["SplitweightList"] = poseData[4]  # 拆分权重
        poseInfoDict["subFaces"] = poseData[5]  # 反减表情
        poseInfoDict["subFaceValues"] = poseData[6]  # 反减数值
        poseInfoDict["doc"] = poseData[7]

        return poseInfoDict

    def createFaceSecCtrl(self, secCtrl, ws):

        cmds.select(cl=True)
        jntName = secCtrl[:-4] + 'jnt'
        facejnt = cmds.joint(name=jntName)
        # ctrl = self.Ctrl(secCtrl,'C00_sphere',0.13,18,[0,0,0],[0,0,0.3])
        if secCtrl in ['L_Brow_1_sec_ctrl', 'L_Brow_2_sec_ctrl', 'R_Brow_1_sec_ctrl', 'R_Brow_2_sec_ctrl']:
            offsetTs = [0, 0, 0.5]
        elif secCtrl in ['L_Brow_3_sec_ctrl']:
            offsetTs = [0.3, 0, 0.5]
        elif secCtrl in ['R_Brow_3_sec_ctrl']:
            offsetTs = [-0.3, 0, 0.5]
        elif secCtrl in ['L_UprLid_1_sec_ctrl', 'L_UprLid_2_sec_ctrl', 'L_UprLid_3_sec_ctrl', 'R_UprLid_1_sec_ctrl',
                         'R_UprLid_2_sec_ctrl', 'R_UprLid_3_sec_ctrl']:
            offsetTs = [0, 0.3, 0.3]
        elif secCtrl in ['L_LwrLid_1_sec_ctrl', 'L_LwrLid_2_sec_ctrl', 'L_LwrLid_3_sec_ctrl', 'R_LwrLid_1_sec_ctrl',
                         'R_LwrLid_2_sec_ctrl', 'R_LwrLid_3_sec_ctrl']:
            offsetTs = [0, -0.3, 0.3]
        else:
            offsetTs = [0, 0, 0.3]

        ctrl = self.ctrlCreate(secCtrl, 'C00_sphere', 'Create', 18, offsetTs, [0, 0, 0], 0.13)
        ctrl_sdk = cmds.group(ctrl, name=ctrl + '_sdk', em=True)
        ctrl_con = cmds.group(ctrl_sdk, name=ctrl + '_con')
        ctrl_zero = cmds.group(ctrl_con, name=ctrl + '_zero')
        cmds.parent(ctrl, ctrl_sdk)

        con_jnt_grp = cmds.group(name='con_' + jntName, em=True)
        con_jnt_grp_zero = cmds.group(con_jnt_grp, name=con_jnt_grp + '_zero')

        cmds.parentConstraint(con_jnt_grp, facejnt, mo=0)
        cmds.connectAttr(ctrl + '.t', con_jnt_grp + '.t')

        cmds.setAttr(ctrl_zero + '.t', ws[0], ws[1], ws[2])
        cmds.setAttr(con_jnt_grp_zero + '.t', ws[0], ws[1], ws[2])

        for attr in ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
            cmds.setAttr(ctrl + '.' + attr, lock=1, keyable=0)

        cmds.setAttr(facejnt + '.radius', 0.2)
        return ctrl_zero, facejnt, con_jnt_grp_zero

    @decorator_utils.one_undo
    def facesecCtrl(self, *args):
        L_secCtrls = ['L_Brow_1_sec_ctrl', 'L_Brow_2_sec_ctrl', 'L_Brow_3_sec_ctrl', 'L_UprLid_1_sec_ctrl',
                      'L_UprLid_2_sec_ctrl', 'L_UprLid_3_sec_ctrl', 'L_LwrLid_1_sec_ctrl', 'L_LwrLid_2_sec_ctrl',
                      'L_LwrLid_3_sec_ctrl', 'L_UprLip_sec_ctrl', 'L_LwrLip_sec_ctrl',
                      'L_Corner_sec_ctrl']
        m_sec_ctrls = ['UprLip_sec_ctrl', 'LwrLip_sec_ctrl']
        L_secCtrlvtxs = self.matchDict[self.mainUI.typeCombo.currentText()]["L_secCtrlvtxs"]
        m_sec_ctrlvtxs = self.matchDict[self.mainUI.typeCombo.currentText()]["m_sec_ctrlvtxs"]

        # faceModel = cmds.textFieldGrp('real_face_model_TF',q = True,text=True )
        faceModel = cmds.ls(sl=True)[0]
        if cmds.objExists(faceModel) != True:
            cmds.error(u'------表情模型不存在------' + faceModel)
        face_sec_ctrl_grp = 'face_sec_ctrl_grp'
        if cmds.objExists(face_sec_ctrl_grp) != True:
            cmds.group(em=True, name=face_sec_ctrl_grp)

        face_sec_jnt_grp = 'face_sec_jnt_grp'
        if cmds.objExists(face_sec_jnt_grp) != True:
            cmds.group(em=True, name=face_sec_jnt_grp)

        ctrl_zero = []
        con_jnt_grp_zero = []
        facejnt = []
        for i in range(len(L_secCtrls)):
            L_secCtrl = L_secCtrls[i]
            R_secCtrl = 'R_' + L_secCtrls[i][2:]
            if cmds.objExists(L_secCtrl) != True:
                L_secCtrlvtx = L_secCtrlvtxs[i]
                L_faceCtrlws = cmds.xform(faceModel + '.vtx[' + str(L_secCtrlvtx) + ']', q=True, ws=True, t=True)
                R_faceCtrlws = [-L_faceCtrlws[0], L_faceCtrlws[1], L_faceCtrlws[2]]

                L_faceSecData = self.createFaceSecCtrl(L_secCtrl, L_faceCtrlws)
                R_faceSecData = self.createFaceSecCtrl(R_secCtrl, R_faceCtrlws)
                L_ctrl_zero = L_faceSecData[0]
                R_ctrl_zero = R_faceSecData[0]

                L_facejnt = L_faceSecData[1]
                R_facejnt = R_faceSecData[1]
                L_con_jnt_grp_zero = L_faceSecData[2]
                R_con_jnt_grp_zero = R_faceSecData[2]
                ctrl_zero.append(L_ctrl_zero)
                ctrl_zero.append(R_ctrl_zero)
                facejnt.append(L_facejnt)
                facejnt.append(R_facejnt)
                con_jnt_grp_zero.append(L_con_jnt_grp_zero)
                con_jnt_grp_zero.append(R_con_jnt_grp_zero)

        for i in range(len(m_sec_ctrls)):
            m_sec_ctrl = m_sec_ctrls[i]
            if cmds.objExists(m_sec_ctrl) != True:
                m_sec_ctrlvtx = m_sec_ctrlvtxs[i]
                m_faceCtrlws = cmds.xform(faceModel + '.vtx[' + str(m_sec_ctrlvtx) + ']', q=True, ws=True, t=True)
                m_faceCtrlws = [0, m_faceCtrlws[1], m_faceCtrlws[2]]

                m_faceSecData = self.createFaceSecCtrl(m_sec_ctrl, m_faceCtrlws)
                m_ctrl_zero = m_faceSecData[0]
                m_facejnt = m_faceSecData[1]
                m_con_jnt_grp_zero = m_faceSecData[2]

                ctrl_zero.append(m_ctrl_zero)
                facejnt.append(m_facejnt)
                con_jnt_grp_zero.append(m_con_jnt_grp_zero)

        if ctrl_zero != [] and con_jnt_grp_zero != []:
            cmds.parent(ctrl_zero, con_jnt_grp_zero, face_sec_ctrl_grp)
        if facejnt != []:
            cmds.parent(facejnt, face_sec_jnt_grp)
            if cmds.objExists(self.mainUI.faceMdl_le.text()):
                cmds.skinCluster(facejnt, self.mainUI.faceMdl_le.text(), tsb=True, nw=1, mi=2, dropoffRate=3.0,
                                 rui=False)
        self.face_secCtrl_Constraints()

    @decorator_utils.one_undo
    def freezeFacePose(self, *args):
        self.isDoubleClicked = True
        [delete(PyNode(ctrl).inputs(type="animCurve")) for ctrl in tool.face_ctrls if objExists(ctrl)]
        self.faceCtrlReturnsDefault()
        select(clear=True)

    def autoMirror(self, show, *args):
        if not self.mainUI.treeViewBase.selectedIndexes():
            cmds.warning("Please select ui.")
            return
        # else:
        item_name = self.mainUI.treeViewBase.selectedIndexes()[0].data()
        selMesh = re.findall(r'\d: (.*)', item_name)[0] + "_edit_model"

        objList = cmds.ls(type="transform")
        mirrorMesh = [obj for obj in objList if cmds.objExists("%s.%s_mirrorMesh" % (obj, selMesh))]

        if show:
            if not mirrorMesh and cmds.objExists(selMesh):
                self.mirrorMesh(False)
        else:
            if mirrorMesh:
                cmds.delete(mirrorMesh)

    @decorator_utils.one_undo
    def mirrorMesh(self, delOut=True, *args):
        """
        镜像模型
        @param args:
        @return:
        :param delOut:
        """
        mirrorDict = {}
        if not self.mainUI.treeViewBase.selectedIndexes():
            cmds.warning("Please select ui.")
            return
        # else:
        item_name = self.mainUI.treeViewBase.selectedIndexes()[0].data()
        selMesh = re.findall(r'\d: (.*)', item_name)[0] + "_edit_model"
        if not cmds.objExists(selMesh): return

        orgMesh = self.mainUI.origMdl_le.text()

        polySymNode = cmds.createNode("polySymmetryEx")
        cmds.setAttr(polySymNode + ".mirrorType", 1)
        cmds.setAttr(polySymNode + ".symCompose", self.mainUI.typeCombo.currentIndex())

        if cmds.objExists("mirror_mesh_geo_grp.mirrorSetting"):
            mirrorDict = eval(cmds.getAttr("mirror_mesh_geo_grp.mirrorSetting"))

        if not cmds.objExists(mirrorDict[selMesh.replace("_edit_model", "")]["orgMesh"]):
            cmds.warning("Org Mesh : %s does not exists." % orgMesh)
            return

        orgBase = mirrorDict[selMesh.replace("_edit_model", "")]["orgMesh"]

        outMesh = self.copymodel([orgMesh])[0]
        cmds.setAttr(outMesh + ".translateX", -50)
        cmds.connectAttr(orgBase + ".outMesh", polySymNode + ".baseMesh", f=True)

        cmds.setAttr(outMesh + ".v", 1)
        cmds.connectAttr(selMesh + ".outMesh", polySymNode + ".inMesh", f=True)
        cmds.connectAttr(polySymNode + ".outMesh", outMesh + ".inMesh", f=True)
        attribute_utils.addAttributes(outMesh, selMesh + "_mirrorMesh", "bool", 1, keyable=False)
        if delOut:
            cmds.select(outMesh)
            cmds.DeleteHistory()
            bsNode = cmds.blendShape(outMesh, selMesh, exclusive='deformPartition#', frontOfChain=True)[0]
            cmds.setAttr(bsNode + "." + outMesh, 1)
            cmds.delete(outMesh)
            cmds.select(selMesh)
            cmds.DeleteHistory()
        else:
            outMesh = cmds.rename(outMesh, selMesh + "_mirrorMesh")

        if selMesh.replace("_edit_model", "") in mirrorDict:
            mirrorDict[selMesh.replace("_edit_model", "")]["isMirror"] = True
        cmds.setAttr("mirror_mesh_geo_grp.mirrorSetting", str(mirrorDict), type="string")

        if cmds.objExists(orgBase):
            if delOut:
                cmds.delete(orgBase)
                orgBase = cmds.rename(self.copymodel([selMesh])[0], orgBase)
                cmds.parent(orgBase, "mirror_mesh_geo_grp")
                cmds.setAttr(orgBase + ".v", 0)

        return outMesh

    @decorator_utils.one_undo
    def mirrorType2(self, type=0, *args):
        mirrorDict = {}

        selMesh = cmds.ls(sl=True)[0]
        if not selMesh: return

        orgMesh = self.mainUI.origMdl_le.text()

        polySymNode = cmds.createNode("polySymmetryEx")
        cmds.setAttr(polySymNode + ".mirrorType", 1)
        cmds.setAttr(polySymNode + ".mirrorSpace", type)
        cmds.setAttr(polySymNode + ".symCompose", self.mainUI.typeCombo.currentIndex())

        if cmds.objExists("mirror_mesh_geo_grp.mirrorSetting"):
            mirrorDict = eval(cmds.getAttr("mirror_mesh_geo_grp.mirrorSetting"))

        orgBase = self.mainUI.origMdl_le.text()

        outMesh = self.copymodel([orgMesh])[0]
        cmds.setAttr(outMesh + ".translateX", -50)
        cmds.connectAttr(orgBase + ".outMesh", polySymNode + ".baseMesh", f=True)

        cmds.setAttr(outMesh + ".v", 1)
        cmds.connectAttr(selMesh + ".outMesh", polySymNode + ".inMesh", f=True)
        cmds.connectAttr(polySymNode + ".outMesh", outMesh + ".inMesh", f=True)
        attribute_utils.addAttributes(outMesh, selMesh + "_mirrorMesh", "bool", 1, keyable=False)

        cmds.select(outMesh)
        cmds.DeleteHistory()
        bsNode = cmds.blendShape(outMesh, selMesh, exclusive='deformPartition#', frontOfChain=True)[0]
        cmds.setAttr(bsNode + "." + outMesh, 1)
        cmds.delete(outMesh)
        cmds.select(selMesh)
        cmds.DeleteHistory()

        if selMesh.replace("_edit_model", "") in mirrorDict:
            mirrorDict[selMesh.replace("_edit_model", "")]["isMirror"] = True
        cmds.setAttr("mirror_mesh_geo_grp.mirrorSetting", str(mirrorDict), type="string")

        return outMesh

    def locVis(self, type=0, *args):
        """
        locator显示隐藏
        @param hide:
        @param args:
        @return:
        """
        [setAttr(loc + '.v', type, lock=0) for loc in ls(type='locator')]

    def Export_bsWeight(self, *args):
        """

        @param args:
        @return:
        """
        selection = selected()
        if not selection:
            return
        # objShape = self.mainUI.faceMdl_le.text()
        objBlendShape = self.blendShapeNode(selection[0])
        if not objBlendShape:
            error('no bs')
            return
        objBlendShape = PyNode(objBlendShape[0])
        vtxs = PyNode(selection[0]).getPoints(space="world")
        weights = {"weights": [getAttr('%s.it[0].bw[%d]' % (objBlendShape, int(x))) for x in range(len(vtxs))]}

        filePath, type = QtWidgets.QFileDialog.getSaveFileName(self, "save", "/", "json(*.json)")
        with open(filePath, 'w') as f:
            json.dump(weights, f, indent=4)

    @decorator_utils.one_undo
    def face_updata(self, *args):  # 表情层级更新

        faceModel = selected()[0]
        cheeckExistObjs = ['head_offset', 'donotTouch', u'face_ChestMid', u'face_LeftShoulder', u'face_RightShoulder',
                           u'face_Neck1', u'face_Neck2', u'face_Neck3', u'face_Head']

        existsObjs = [cheeckExistObj for cheeckExistObj in cheeckExistObjs if objExists(cheeckExistObj) == 0]

        if existsObjs:
            cmds.error(u'以下物体不存在，无法升级------', str(existsObjs))
        jaw_01_joint_zero = 'jaw_01_joint_zero'

        rename('head_offset', 'face_head_offset')
        rename('donotTouch', 'face_donotTouch')
        rename('L_eye_ctrl_rotate45|L_eye_ctrl_sdk', 'L_eye_ctrl_sdk_2')
        rename('R_eye_ctrl_rotate45|R_eye_ctrl_sdk', 'R_eye_ctrl_sdk_2')

        head_offset_grp = listRelatives('teeth_ctrl_all', p=True)[0]
        # 创建口腔loc
        jaw_zero_loc = spaceLocator(name='jaw_zero_loc')
        delete(parentConstraint(jaw_01_joint_zero, jaw_zero_loc, mo=0))
        parentConstraint(jaw_zero_loc, jaw_01_joint_zero, mo=1)
        parent(jaw_zero_loc, head_offset_grp)
        parent('up_teeth_ctrl_zero', jaw_zero_loc)
        # 创建上牙01 Loc
        upTeeth_01_loc = spaceLocator(name='upTeeth_01_loc')
        delete(parentConstraint('up_teeth_ctrl', upTeeth_01_loc, mo=0))
        parent(upTeeth_01_loc, 'up_teeth_ctrl_zero')
        parent('up_teeth_ctrl', upTeeth_01_loc)
        # 创建下牙01 Loc
        upTeeth_02_loc = spaceLocator(name='upTeeth_02_loc')
        delete(pointConstraint('upTeeth_02_joint', upTeeth_02_loc, mo=0))
        parentConstraint(upTeeth_02_loc, 'upTeeth_02_joint', mo=1)
        parent(upTeeth_02_loc, 'up_teeth_ctrl')
        # 创建下巴组
        face_jaw_con = group(em=True, name='face_jaw_con')
        delete(parentConstraint('jaw_01_joint', face_jaw_con, mo=0))
        parent(face_jaw_con, jaw_zero_loc)
        parent('lw_teeth_ctrl_zero', face_jaw_con)
        connectAttr('jaw_01_joint.t', face_jaw_con + '.t')
        connectAttr('jaw_01_joint.r', face_jaw_con + '.r')
        # 创建下巴02 Loc
        jaw_02_loc = spaceLocator(name='jaw_02_loc')
        delete(parentConstraint('jaw_02_joint', jaw_02_loc, mo=0))
        parentConstraint(jaw_02_loc, 'jaw_02_joint', mo=1)
        parent(jaw_02_loc, face_jaw_con)

        # 创建下牙01 Loc
        lwTeeth_01_loc = spaceLocator(name='lwTeeth_01_loc')
        delete(parentConstraint('lw_teeth_ctrl', lwTeeth_01_loc, mo=0))
        parent(lwTeeth_01_loc, 'lw_teeth_ctrl_zero')
        parent('lw_teeth_ctrl', lwTeeth_01_loc)
        # 创建下牙02 Loc
        lwTeeth_02_loc = spaceLocator(name='lwTeeth_02_loc')
        delete(parentConstraint('lwTeeth_02_joint', lwTeeth_02_loc, mo=0))
        parentConstraint(lwTeeth_02_loc, 'lwTeeth_02_joint', mo=1)
        parent(lwTeeth_02_loc, 'lw_teeth_ctrl')
        # 创建base 骨骼
        face_sec_base_jnt = 'face_Head_base_jnt'
        if objExists(face_sec_base_jnt) != True:
            select(cl=True)
            face_sec_base_jnt = joint(name=face_sec_base_jnt)
            delete(pointConstraint('face_Head', face_sec_base_jnt))
            setAttr(face_sec_base_jnt + '.radius', 1)
        else:
            cmds.warning(face_sec_base_jnt + u'------已经存在')
        # 创建头部Loc
        face_Head_base_loc = spaceLocator(name='face_Head_base_loc')
        delete(parentConstraint(face_sec_base_jnt, face_Head_base_loc, mo=0))
        parentConstraint(face_Head_base_loc, face_sec_base_jnt, mo=1)
        parent(face_Head_base_loc, head_offset_grp)
        parent(jaw_zero_loc, face_Head_base_loc)
        # 骨骼层级修改
        parent('L_eye_skin_01_jnt', 'R_eye_skin_01_jnt', 'jaw_01_joint_zero', 'face_Head_base_jnt')
        parent(face_sec_base_jnt, head_offset_grp)
        # 骨骼命名修改
        jnts = [u'face_ChestMid', u'face_LeftShoulder', u'face_RightShoulder', u'face_Neck1', u'face_Neck2',
                u'face_Neck3', u'face_Head']
        setAttr(jnts[0] + '.v', 0)
        for jnt in jnts:
            rename(jnt, jnt + '_old')
        # cmds.select(face_sec_base_jnt)
        # 添加一个缩放组
        face_head_global = group(em=True, name='face_head_global')
        parent(head_offset_grp, face_head_global)
        # 删除无用的约束
        delete('up_teeth_ctrl_zero_parentConstraint1', 'lw_teeth_ctrl_zero_parentConstraint1',
               'L_eye_loc_zero_parentConstraint1', 'R_eye_loc_zero_parentConstraint1')
        # 创建一些放毛囊的组
        self.create_follic_grp()
        # 骨骼大小修改
        jnts = [u'face_Head_base_jnt', u'L_eye_skin_01_jnt', u'R_eye_skin_01_jnt', u'jaw_01_joint_zero',
                u'upTeeth_01_joint', u'upTeeth_02_joint', u'jaw_01_joint', u'jaw_02_joint', u'lwTeeth_01_joint',
                u'lwTeeth_02_joint']
        for jnt in jnts:
            setAttr(jnt + '.radius', 0.2)
        setAttr('jaw_01_joint_zero' + '.radius', 0.25)

    def create_follic_grp(self):
        follicgrps = ['L_face_brow_follic_grp', 'R_face_brow_follic_grp',
                      'L_face_eyelash_up_follic_grp', 'R_face_eyelash_up_follic_grp',
                      'L_face_eyelash_dn_follic_grp', 'R_face_eyelash_dn_follic_grp',
                      'L_face_shadows_follic_grp', 'R_face_shadows_follic_grp',
                      'huzi_lip_up_follic_grp', 'huzi_jaw_follic_grp', 'huzi_cheek_follic_grp',
                      'face_sec_ctrl_follic_grp']
        for follicgrp in follicgrps:
            if not objExists(follicgrp):
                grp = group(em=True, name=follicgrp)
                if objExists('face_donotTouch'):
                    parent(grp, 'face_donotTouch')
                elif objExists('donotTouch'):
                    parent(grp, 'donotTouch')
                else:
                    pass

    def exportMouthBs(self, Datastr):
        filePath = self.mainUI.weightPath_le.text() + '/mouth_up.json'

        with open(filePath, 'w') as f:
            json.dump(Datastr, f, indent=4)

        self.bsweight_filePath = filePath[:-(len(filePath.split('/')[-1]))]

    @decorator_utils.one_undo
    def faceSplit(self, *args):
        """

        :param args:
        :return:
        """
        origModel = self.mainUI.origMdl_le.text()
        bsweightPath = self.mainUI.weightPath_le.text()
        self.blendShapeName = self.blendShapeNode(PyNode(self.mainUI.faceMdl_le.text()))[0]
        BlendShape = self.blendShapeName
        tars = listAttr(BlendShape + '.weight', multi=True)

        # 运行前判断-----------------------------------------------------------------------------
        if not objExists(origModel):
            return
        #
        if not os.path.exists(bsweightPath):
            return
        #
        if objExists(self.CombinFace):
            select(self.CombinFace)
            return
        #
        notExistsSubFace = []
        for subFace in self.subFaces:
            if not objExists(subFace):
                notExistsSubFace.append(subFace)
        if notExistsSubFace:
            return

        splitTargetExistsList = []
        faceSplitNum = len(self.weightDataSplitList)
        for i in range(faceSplitNum):  # 循环方位['l-r','out_l-in_l','out_r-in_r']
            weightDataSplit = self.weightDataSplitList[i]
            Splitweight = self.weightDataSplitList[i]
            weightUDLRs = weightDataSplit.split('-')  # ['l','r']#拆分方位
            for weightUDLR in weightUDLRs:
                if objExists(weightUDLR) == True:
                    splitTargetExistsList.append(weightUDLR)
        if splitTargetExistsList != []:
            select(splitTargetExistsList)
            return
        # ------------------------------------------------------------------------------------------
        origModelVisValue = getAttr(origModel + '.v')
        if origModelVisValue == 0:  # 显示org模型
            setAttr(origModel + '.v', 1)
        face_bs_grp = 'IMM_face_bs_grp'
        if not objExists(face_bs_grp):
            group(name=face_bs_grp, em=True)
        faceAreas = []
        faceArea_grp = self.CombinFace + '_face_bs_grp'
        if not objExists(faceArea_grp):
            faceArea_grp = group(name=faceArea_grp, em=True)
            parent(faceArea_grp, face_bs_grp)
        else:
            setAttr(faceArea_grp + '.tx', 0)
        copy_model = self.copyFaceModel(True, self.CombinFace)

        if not objExists(self.CombinFace):  # 整体表情
            combinFace = duplicate(origModel, name=self.CombinFace)[0]
            self.createBlendShape3(copy_model, combinFace, 1)
            setAttr(combinFace + '.t', 0, 0, 0)
            parent(combinFace, faceArea_grp)
            if self.subFaces:
                setAttr(combinFace + '.tx', 15)
                addcombinFace = duplicate(origModel, name=self.CombinFace + '_add')[0]
                setAttr(addcombinFace + '.t', 0, 0, 0)
                parent(addcombinFace, faceArea_grp)
                self.createBlendShape(addcombinFace, PyNode(self.CombinFace), 1)
                for i in range(len(self.subFaces)):
                    subFace = self.subFaces[i]
                    subFaceValue = self.subFaceValues[i]
                    self.createBlendShape(subFace, PyNode(self.CombinFace), subFaceValue)
        if self.weightDataSplitList:  # 判断是否需要拆分
            faceSplitNum = len(self.weightDataSplitList)
            for i in range(faceSplitNum):  # 循环方位['l-r','out_l-in_l','out_r-in_r']
                weightDataSplit = self.weightDataSplitList[i]
                Splitweight = self.SplitweightList[i]
                weightUDLRs = weightDataSplit.split('-')  # ['l','r']#拆分方位
                weightData = Splitweight  # 拆分权重

                face1 = weightUDLRs[0]  # 刷权重的模型
                face2 = weightUDLRs[1]  # 反减出来的模型
                faceSplitNum = i
                if i == 0:
                    faceAreas.append(face1)
                    faceAreas.append(face2)
                if i == 1:
                    self.CombinFace = faceAreas[0]
                if i == 2:
                    self.CombinFace = faceAreas[1]
                self.splitFace_edit(self.CombinFace, origModel, bsweightPath, weightData, face1, face2, faceSplitNum,
                                    faceArea_grp)

        else:
            weightData = ''
            face1 = ''
            face2 = ''
            faceSplitNum = 0
            self.splitFace_edit(self.CombinFace, origModel, bsweightPath, weightData, face1, face2, faceSplitNum,
                                faceArea_grp)

        setAttr(faceArea_grp + '.tx', 65)
        setAttr(origModel + '.v', origModelVisValue)
        parent(copy_model, faceArea_grp)

    def splitFace_edit(self, CombinFace, origModel, bsweightPath, weightData, face1, face2, faceSplitNum, faceArea_grp):
        """

        @param CombinFace:
        @param origModel: 原始头部
        @param bsweightPath:
        @param weightData:
        @param face1:
        @param face2:
        @param faceSplitNum:
        @param faceArea_grp:
        @return:
        """
        BlendShape = self.blendShapeName

        tars = listAttr(BlendShape + '.weight', multi=True)

        if faceSplitNum == 0:
            face1ws = (15, 25, 0)
            face2ws = (-15, 25, 0)
        elif faceSplitNum == 1:
            face1ws = (22.5, 50, 0)
            face2ws = (7.5, 50, 0)
        elif faceSplitNum == 2:
            face1ws = (-22.5, 50, 0)
            face2ws = (-7.5, 50, 0)
        if weightData != '':
            # 拆分整体表情
            if objExists(face1) != True:
                face1 = duplicate(origModel, name=face1)[0]
                setAttr(face1 + '.t', face1ws[0], face1ws[1], face1ws[2])
                face1bsNode = self.createBlendShape(CombinFace, face1, 1)
                face2 = duplicate(origModel, name=face2)[0]
                setAttr(face2 + '.t', face2ws[0], face2ws[1], face2ws[2])
                face2bsNode = self.createBlendShape2([CombinFace, face1], face2)
                parent(face1, face2, faceArea_grp)

                if face1 in tars:
                    tar1 = self.GainTarget_All(BlendShape, face1)[0]  # 从bs节点提取tar形态
                    setAttr(tar1 + '.t', face1ws[0], face1ws[1] + 25, face1ws[2])
                    face1_tar = rename(face1, face1 + '_tar')
                    self.createBlendShape(face1_tar, PyNode(tar1), 1)
                    parent(tar1, faceArea_grp)
                if face2 in tars:
                    tar2 = self.GainTarget_All(BlendShape, face2)[0]  # 从bs节点提取tar形态
                    setAttr(tar2 + '.t', face2ws[0], face2ws[1] + 25, face2ws[2])
                    face2_tar = rename(face2, face2 + '_tar')
                    self.createBlendShape(face2_tar, PyNode(tar2), 1)
                    parent(tar2, faceArea_grp)
                refresh()
                self.Import_bsWeight(face1, face1bsNode, weightData)
        elif weightData == '':
            faceArea_tar = rename(CombinFace, CombinFace + '_tar')
            tar = self.GainTarget_All(BlendShape, CombinFace)[0]  # 从bs节点提取tar形态
            setAttr(tar + '.t', 0, 25, 0)
            self.createBlendShape(faceArea_tar, PyNode(tar), 1)
            parent(tar, faceArea_grp)

    def createBlendShape(self, targetModel, addblendShapeModel, Targetvalue):
        SourceGeo = addblendShapeModel
        ToName = targetModel
        SourceBlendShape = self.blendShapeNode(SourceGeo)  # 查询被copy修型模型blendShape节点
        if SourceBlendShape != []:  # bs节点只有一个，在此基础上添加Target
            SourceBlendShape = SourceBlendShape[0]
            SourceBsAttrs = listAttr(SourceBlendShape + '.weight', multi=True)  # 查询bs属性
            if SourceBsAttrs != None:
                xi = self.GetWeightIndex(SourceBlendShape, SourceBsAttrs[-1])
                origSourceBsAttrsNum = len(SourceBsAttrs)
                xi += 1
            else:
                xi = 0

        elif len(SourceBlendShape) > 1:  # bs节点不止1个，报错，结束程序
            return
        elif SourceBlendShape == []:  # 没有bs节点，就创建
            SourceBlendShape = SourceGeo + '_blendShape'
            SourceBlendShape = \
                blendShape(SourceGeo, exclusive='deformPartition#', frontOfChain=True, name=SourceBlendShape)[0]
            xi = 0
            origSourceBsAttrsNum = 0
        blendShape(SourceBlendShape, edit=True, tc=False, target=(SourceGeo, xi, ToName, 1.0))
        setAttr(SourceBlendShape + "." + ToName, Targetvalue)
        return SourceBlendShape

    def createBlendShape2(self, targetModels, addblendShapeModel):
        bsNode = blendShape(targetModels, addblendShapeModel)[0]
        for i in range(len(targetModels)):
            targetModel = targetModels[i]
            if i == 0:
                setAttr(bsNode + '.' + targetModel, 1)
            else:
                setAttr(bsNode + '.' + targetModel, -1)
        return bsNode

    def createBlendShape3(self, targetModel, addblendShapeModel, Targetvalue):  # 先删除原先的bs，再创建一个新的
        """

        @param targetModel:
        @param addblendShapeModel:
        @param Targetvalue:
        @return:
        """
        SourceBlendShape = self.blendShapeNode(addblendShapeModel)  # 查询被copy修型模型blendShape节点
        if SourceBlendShape != []:
            delete(SourceBlendShape)
        SourceBlendShape = addblendShapeModel + '_blendShape'
        SourceBlendShape = \
            blendShape(addblendShapeModel, exclusive='deformPartition#', frontOfChain=True, name=SourceBlendShape)[0]
        blendShape(SourceBlendShape, edit=True, tc=False, target=(addblendShapeModel, 0, targetModel, 1.0))
        setAttr(SourceBlendShape + '.' + targetModel, Targetvalue)
        addblendShapeModelPar = listRelatives(addblendShapeModel, p=True)
        targetModelPar = listRelatives(targetModel, p=True)
        if targetModelPar != addblendShapeModelPar and addblendShapeModelPar != None:
            parent(targetModel, addblendShapeModelPar)

    def GainTarget_All(self, BlendShape, tragetBlendShape):  # 提取出traget并连接到bs
        """

        @param BlendShape:
        @param tragetBlendShape:
        @return:
        """
        if isinstance(tragetBlendShape, PyNode):
            tragetBlendShape = tragetBlendShape.nodeName()
        tragetIndexItem = self.InputTargetGroup(BlendShape, tragetBlendShape)
        tars = self.creativeTarget(BlendShape, [tragetBlendShape])

        for i in tars:
            get = getAttr(i + '.' + tragetBlendShape) * 1000.0 + 5000
            shape = listHistory(i)
            connectAttr(shape[0] + '.worldMesh[0]',
                        BlendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (
                            tragetIndexItem, get), f=True)
        return tars

    def InputTargetGroup(self, blendShapeNode, target):  # 查询bs 某个target的序号
        """

        @param blendShapeNode:
        @param target:
        @return:
        """
        tragetIndexItem = self.GetWeightIndex(blendShapeNode, target)
        return tragetIndexItem

    def creativeTarget(self, blendShape, target=[], prefix=None):  # 提取target
        """

        @param blendShape:
        @param target:
        @param prefix:
        @return:
        """
        listConnect = []
        listConnect_target = []
        listLock_target = []
        listValue_target = []
        listConnect_Name = []
        MeshOrigList = []
        listTargetBlendShape = listAttr(blendShape + '.weight', multi=True)
        if objExists(blendShape + '_Grp') != 1:
            blendShapeGrp = createNode('transform', name=blendShape + '_Grp')

        for i in listTargetBlendShape:
            if getAttr(blendShape + '.' + i, l=1):
                setAttr(blendShape + '.' + i, l=0)
                listLock_target.append(i)
            get = getAttr(blendShape + '.' + i)
            listValue_target.append(get)

            targetConnect = listConnections(blendShape + '.' + i, p=True, s=True, d=False)
            if targetConnect is not None:
                for m in targetConnect:
                    disconnectAttr(m, blendShape + '.' + i)
                    listConnect.append(m)
                listConnect_target.append(i)
            setAttr(blendShape + "." + i, 0)

        MeshOrigList = self.meshOrig(blendShape.nodeName())

        for x in target:
            if listTargetBlendShape.__contains__(x) != 1 or 'weight[' in x:
                continue

            tragetIndexItem = self.InputTargetGroup(blendShape, x)
            inputTargetItem = getAttr(
                blendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
            for c in inputTargetItem:
                indexInt = (int(c) - 5000) / 1000.0

                Mesh = createNode('mesh', name=x + '_Shape')
                MeshMianShape = createNode('mesh', name=x + '_MianShape')

                cmds.sets(Mesh.name(), edit=True, forceElement='initialShadingGroup')
                listRel = listRelatives(Mesh, p=True)
                MianlistRel = listRelatives(MeshMianShape, p=True)

                setAttr(blendShape + '.' + x, float(indexInt))
                connectAttr(blendShape + '.outputGeometry[0]', MeshMianShape + '' + '.inMesh')

                connectAttr(MeshOrigList[0] + '.outMesh', Mesh + '' + '.inMesh')
                copyMesh = duplicate(MianlistRel)

                #########################################
                count = str(indexInt).split(".")
                if count[0] == '-0':
                    ne = 'm'
                else:
                    ne = 'p'

                if float(indexInt) == 1:
                    targetName = x
                else:
                    targetName = x + '_' + ne + count[1]
                parent(copyMesh, blendShape + '_Grp')
                if prefix == 1:
                    targetName = '_' + targetName
                ToName = rename(copyMesh, targetName)
                addAttr(ToName, ln=x, at='double', k=0)
                setAttr(ToName + '.' + x, float(indexInt))

                setAttr(blendShape + '.' + x, 0)
                delete(listRel, MianlistRel)
                listConnect_Name.append(ToName)
        ##############setAttr value
        for i in range(len(listTargetBlendShape)):
            val = listValue_target[i]
            setAttr(blendShape + '.' + listTargetBlendShape[i], val)
        ##############setAttr value
        ##############lock Node
        for i in listLock_target:
            setAttr(blendShape + '.' + i, l=1)
        ##############connection Node
        for i in range(len(listConnect)):
            connectAttr(listConnect[i], blendShape + '.' + listConnect_target[i])

        return listConnect_Name

    def meshOrig(self, meshNode):  # 获取Orig Shape
        """

        @param meshNode:
        @return:
        """
        MeshOrigList = []
        Mesh_Orig = cmds.listHistory(meshNode)
        for i in range(len(Mesh_Orig)):
            if cmds.nodeType(Mesh_Orig[i]) == 'mesh':
                if 'Orig' in Mesh_Orig[i]:
                    if Mesh_Orig[i] != None:
                        if cmds.listConnections(Mesh_Orig[i] + '.worldMesh[0]', source=True):
                            MeshOrigList.append(PyNode(Mesh_Orig[i]))
        return MeshOrigList

    def GetWeightIndex(self, blendShapeNode, target):  # 查询target的序号
        """

        @param blendShapeNode:
        @param target:
        @return:
        """
        aliases = aliasAttr(blendShapeNode, q=True)
        a = aliases.index(target)
        weight = aliases[a + 1]
        index = weight.split('[')[-1][:-1]
        return int(index)

    def meshExists(self, mesh):
        """
        判断物体shape是否是mesh
        @param mesh:
        @return:
        """
        try:
            listMesh = listRelatives(mesh, s=True, f=1)
            if nodeType(listMesh[0]) == 'mesh':
                return True
            else:
                return False
        except TypeError:
            pass

    def copyFaceModel(self, uiHost=True, item=None):
        """
        复制模型
        @param select: 是否选择物体
        @return:
        """
        if uiHost:
            modelName = item + "_edit_model"
        else:
            modelName = self.mainUI.faceMdl_le.text() + "_bs"
        sel = self.mainUI.faceMdl_le.text()

        attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

        copysel = duplicate(sel, name=modelName)[0]
        conObjAttrName = listConnections(copysel + '.drawOverride', p=True)
        if conObjAttrName:
            disconnectAttr(conObjAttrName[0], copysel + '.drawOverride')

        shapes = copysel.getShapes()
        for shape in shapes:
            if shape.intermediateObject.get() == 1:
                delete(shape)
        for at in attrs:
            copysel.attr(at).set(lock=0)
        copysel.tx.set(25)

        if uiHost:
            if objExists(copysel.replace('edit', 'fix')):
                bs = blendShape(copysel.replace('edit', 'fix'), copysel)[0]
                setAttr(bs + "." + copysel.replace('edit', 'fix'), 1)

        select(copysel)

        return copysel

    def createBsMesh(self, *args):
        """
        创建bs权重模型
        @return:
        """
        if objExists(self.mainUI.faceMdl_le.text()):
            self.bsMesh = self.copyFaceModel(False)
            bsNode = self.addNewBlendShape(self.mainUI.faceMdl_le.text(), self.bsMesh, 1.0)
            self.mainUI.meshName_le.setText(bsNode.name())
            select(self.bsMesh, r=True)
            mel.eval("ArtPaintBlendShapeWeightsTool;")

    def loadMesh(self, widget):
        """
        #加载模型
        @param widget:
        @return:
        """
        sel = selected(type="transform")
        if len(sel) > 0 and self.meshExists(sel):
            widget.setText(sel[0].name())
        else:
            warning('No transform objects selected.')

    def changePath(self, *args):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, "select path",
                                                               tool.scriptPath)
        self.mainUI.weightPath_le.setText(file_name)

    def changeWeightPath(self, *args):
        self.mainUI.weightPath_le.setText(self.weightDataPathDict[self.mainUI.typeCombo.currentText()][0])

    def addNewBlendShape(self, targetModel, addblendShapeModel, Targetvalue):
        """
        创建一个新的blendShape
        @param targetModel:
        @param addblendShapeModel:
        @param Targetvalue:
        @return:
        """
        SourceBlendShape = self.blendShapeNode(addblendShapeModel)  # 查询被copy修型模型blendShape节点
        if SourceBlendShape != []:
            delete(SourceBlendShape)
        SourceBlendShape = addblendShapeModel + '_blendShape'
        SourceBlendShape = \
            blendShape(addblendShapeModel, exclusive='deformPartition#', frontOfChain=True, name=SourceBlendShape)[0]
        blendShape(SourceBlendShape, edit=True, tc=False, target=(addblendShapeModel, 0, targetModel, 1.0))
        setAttr(SourceBlendShape + '.' + targetModel, Targetvalue)
        addblendShapeModelPar = listRelatives(addblendShapeModel, p=True)
        targetModelPar = listRelatives(targetModel, p=True)
        if targetModelPar != addblendShapeModelPar and addblendShapeModelPar is not None:
            parent(targetModel, addblendShapeModelPar)
        return SourceBlendShape

    def copymodel(self, meshList, *args):
        """copy model"""
        attrs = ['tx',
                 'ty',
                 'tz',
                 'rx',
                 'ry',
                 'rz',
                 'sx',
                 'sy',
                 'sz']
        copysels = []
        for sel in meshList:
            copysel = cmds.duplicate(sel, name=sel + '_duplicate')[0]
            copysels.append(copysel)
            shapes = cmds.listRelatives(copysel, s=True, f=True)
            for shape in shapes:
                if cmds.getAttr(shape + '.intermediateObject') == 1:
                    cmds.delete(shape)

            for attr in attrs:
                cmds.setAttr(copysel + '.' + attr, lock=0)

        return copysels

    def createMirrorOrgModel(self, name):
        orgCopyModel = self.copymodel([self.mainUI.faceMdl_le.text()])
        orgCopyModel = cmds.rename(orgCopyModel, name + "_org")
        cmds.parent(orgCopyModel, 'mirror_mesh_geo_grp')
        cmds.setAttr(orgCopyModel + ".v", 0)

    def selectCurrentCtrl(self, *args):
        cmds.select(self.ctrlNames, r=1)

    @decorator_utils.one_undo
    def editfacePose(self, widget, *args):
        """

        :param item:
        :return:
        """

        if widget.selectedIndexes():
            item_name = widget.selectedIndexes()[0].data()
            index = widget.currentIndex().row()
            try:
                self.CombinFace = re.findall(r'\d: (.*)', item_name)[0]
            except:
                self.CombinFace = item_name
            for face in self.itemList_reduce:
                splitface_grp = face + '_face_bs_grp'
                if objExists(splitface_grp) == True:
                    setAttr(splitface_grp + '.v', 0)
            if objExists(self.CombinFace + '_face_bs_grp') == True:
                setAttr(self.CombinFace + '_face_bs_grp.v', 1)

            self.mainUI.value_dp.setValue(1.0)
            data = dict()
            self.facePoseData = []

            for i, lst in enumerate(self.itemList):
                for item in lst:
                    if re.findall(r'\d: (.*)', item)[0] == self.CombinFace:
                        data = tool.configData["facePoseList"][self.baseFaceList[i]][index]
                        self.facePoseData = tool.configData["facePoseList"][self.baseFaceList[i]]

            if not data:
                data = tool.configData["CombinFacePoseList"][index]  # 获取表情数据

            if not self.facePoseData:
                self.facePoseData = tool.configData["CombinFacePoseList"]

            self.poseData = tool.getPoseData(data, self.CombinFace)
            self.ctrlNames = self.poseData[0]  # 控制器
            self.ctrlAttrs = self.poseData[1]  # 控制器属性
            self.ctrlValues = self.poseData[2]  # 控制器数值
            self.weightDataSplitList = self.poseData[3]  # 拆分列表
            self.SplitweightList = self.poseData[4]  # 拆分权重
            self.subFaces = self.poseData[5]  # 反减表情
            self.subFaceValues = self.poseData[6]  # 反减数值
            self.doc = self.poseData[7]

            self.mainUI.doc_edit.setText(self.doc)

            for face in self.itemList_reduce:
                splitface_grp = face + '_face_bs_grp'
                if objExists(splitface_grp) == True:
                    setAttr(splitface_grp + '.v', 0)
            if objExists(self.CombinFace + '_face_bs_grp') == True:
                setAttr(self.CombinFace + '_face_bs_grp.v', 1)

            for ctrl in tool.face_ctrls:
                if objExists(ctrl) == True:
                    for attr in self.attrs:
                        if getAttr('%s.%s' % (ctrl, attr), lock=True) == False:
                            setAttr('%s.%s' % (ctrl, attr), 0)

            self.ctrlNames = [ctrl for i, dic in enumerate(self.facePoseData) if self.CombinFace in dic for ctrl in
                              dic[self.CombinFace]['ctrlNames']]  # 控制器
            self.ctrlAttrs = [ctrl for i, dic in enumerate(self.facePoseData) if self.CombinFace in dic for ctrl in
                              dic[self.CombinFace]['ctrlAttrs']]  # 控制器属性
            self.ctrlValues = [ctrl for i, dic in enumerate(self.facePoseData) if self.CombinFace in dic for ctrl in
                               dic[self.CombinFace]['ctrlValues']]  # 控制器数值

            [cmds.setAttr(self.ctrlNames[i] + self.ctrlAttrs[i], self.ctrlValues[i]) for i in
             range(len(self.ctrlNames))]
            self.deleteKeyFrame()
            self.keyPose()
            cmds.currentTime(50)
            if objExists('mirror_mesh_geo_grp'):
                mirrorDict = eval(cmds.getAttr("mirror_mesh_geo_grp.mirrorSetting"))
                if mirrorDict[self.CombinFace]["isMirror"]:
                    if objExists(mirrorDict[self.CombinFace]["orgMesh"]):
                        delete(mirrorDict[self.CombinFace]["orgMesh"])
                    self.createMirrorOrgModel(self.CombinFace)
                else:
                    if not objExists(mirrorDict[self.CombinFace]["orgMesh"]):
                        self.createMirrorOrgModel(self.CombinFace)
                mirrorDict[self.CombinFace]["isMirror"] = False
                cmds.setAttr("mirror_mesh_geo_grp.mirrorSetting", str(mirrorDict), type="string")
            cmds.select(d=1)

    @decorator_utils.one_undo
    def faceCtrlReturnsDefault(self, *args):  # 控制器恢复默认
        self.deleteKeyFrame()
        try:
            [PyNode(ctrl).attr(at).set(0) for ctrl in tool.face_ctrls if objExists(ctrl) == True for at in self.attrs if
             PyNode(ctrl).attr(at).get(lock=True) == False]
        except MayaObjectError:
            warning(u"控制器物体不存在.")

    def blendShapeNode(self, MeshNode):
        """
        查询blenShape节点
        @param MeshNode:
        @return:
        """
        BlendShapeNode = []
        try:
            BlendShapeNode = MeshNode.history(type='blendShape')
        except TypeError:
            pass
        return BlendShapeNode

    @decorator_utils.one_undo
    def Import_bsWeight2(self, *args):
        """
        Import bs weights from select file path.
        :param args:
        :return:
        """
        selection = selected()
        if not selection:
            cmds.warning("Please select one mesh object with bs node!")
            return

        fileName, type = QtWidgets.QFileDialog.getOpenFileName(self, "Open", "/", "json(*.json)")

        DataWeights = None

        with open(fileName, "r") as f:
            DataWeights = json.load(f)["weights"]

        refresh()

        if len(selection[0].vtx) != len(DataWeights):
            raise ImportWeightsError("Selected object vert number is not the same.")

        bsNode = self.blendShapeNode(selection[0])
        if not bsNode:
            cmds.error("Selected object has no bs node!")
            return

        [setAttr('%s.it[0].bw[%d]' % (bsNode[0].name(), int(x)), DataWeights[x]) for x in range(len(selection[0].vtx))]
        print(
            "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Import Successfully!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def Import_bsWeight(self, obj, bsNode, fileName):
        self.rampSettingPath = self.mainUI.weightPath_le.text() + "/rampWeightsSettings.json"
        # tool.scriptPath + "/faceWeightData/rampWeightsSettings.json"
        if "mouth" in fileName:
            filePath = self.mainUI.weightPath_le.text() + "/mouth_up.json"
            with open(filePath, 'r') as f:
                Datastr = json.load(f)["weights"]
            refresh()
            if len(obj.vtx) != len(Datastr):
                return False
            [setAttr('%s.it[0].bw[%d]' % (bsNode.name(), int(x)), Datastr[x]) for x in range(len(obj.vtx))]
        else:
            with open(self.rampSettingPath, 'r') as f:
                settingsData = json.load(f)[fileName]
            bsNode = PyNode(bsNode)
            deformerObj = bsNode.outputs(type="mesh")[0]

            shapes = listRelatives(deformerObj, s=True, f=True)
            orgShape = ""
            for shape in shapes:
                if getAttr(shape + '.intermediateObject') == 1:
                    orgShape = shape

            rampWeightsNode = createNode("rampWeights", name=bsNode + "_rampWeights")
            deformerObj.worldMatrix[0] >> rampWeightsNode.matrixList[0]
            orgShape.worldMesh[0] >> rampWeightsNode.mesh[0]

            connectAttr(rampWeightsNode + ".weightList[0].weights",
                        bsNode + ".inputTarget[0].inputTargetGroup[0].targetWeights")

            srcAttr = bsNode.attr("inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputComponentsTarget")
            destAttr = rampWeightsNode.attr("inputComponentsList[0].inputComponents")

            srcAttr >> destAttr
            refresh()

            disconnectAttr(srcAttr, destAttr)

            for attr, value in settingsData.items():
                setAttr(rampWeightsNode + "." + attr, value)

    def SpinValChange(self, *args):
        """

        @param args:
        @return:
        """
        if objExists(self.mainUI.faceMdl_le.text()):
            self.blendShapeName = self.blendShapeNode(PyNode(self.mainUI.faceMdl_le.text()))[0]
        self.mainUI.value_slider.setValue(self.mainUI.value_dp.value() * 100.0)
        if self.mainUI.treeViewBase.selectedIndexes():
            [cmds.setAttr(self.ctrlNames[i] + self.ctrlAttrs[i], self.ctrlValues[i] * self.mainUI.value_dp.value()) for
             i in
             range(len(self.ctrlNames))]

    def SliderValueChange(self, *args):
        """

        @param args:
        @return:
        """
        self.mainUI.value_dp.setValue(self.mainUI.value_slider.value() / 100.0)

    def deleteKeyFrame(self):
        removeNodes = []
        for i, x in enumerate(cmds.ls(type="animCurve")):
            if cmds.objExists(x):
                hasInput = cmds.listConnections(x, s=True, d=False, scn=True)
                hasOutput = cmds.listConnections(x, s=False, d=True, scn=True)
                if 'hyperLayout' in str(hasOutput) and len(hasOutput) == 1:
                    hasOutput = None
                isLocked = cmds.lockNode(x, q=1, l=1)[0]
                if isLocked:
                    cmds.lockNode(x, l=False)
                if (not hasInput) or (not hasOutput):
                    if "scalePower" not in x:
                        removeNodes.append(x)
        [cmds.delete(node) for node in removeNodes if cmds.objExists(node)]

    @decorator_utils.one_undo
    def keyPose(self, *args):
        value = self.mainUI.value_dp.value()
        if self.mainUI.treeViewBase.selectedIndexes():
            for i in range(len(self.ctrlNames)):
                cmds.setKeyframe(self.ctrlNames[i], v=0, attribute=self.ctrlAttrs[i].split('.')[-1], t=0)
                cmds.setKeyframe(self.ctrlNames[i], v=self.ctrlValues[i] * value,
                                 attribute=self.ctrlAttrs[i].split('.')[-1], t=50)

    def SpinValChange2(self, *args):
        """

        @param args:
        @return:
        """
        if objExists(self.mainUI.faceMdl_le.text()):
            self.blendShapeName = self.blendShapeNode(PyNode(self.mainUI.faceMdl_le.text()))[0]
        self.mainUI.value_slider2.setValue(self.mainUI.value_dp2.value() * 100.0)
        if self.mainUI.comBineViewBase.selectedIndexes():
            [setAttr(self.ctrlNames[i] + self.ctrlAttrs[i], self.ctrlValues[i] * self.mainUI.value_dp2.value()) for i in
             range(len(self.ctrlNames))]

    def SliderValueChange2(self, *args):
        """

        @param args:
        @return:
        """
        self.mainUI.value_dp2.setValue(self.mainUI.value_slider2.value() / 100.0)

    def TreeViewModelCreate(self, titleList, chList=None, treeView=None):
        model_base = QtGui.QStandardItemModel()
        for i, item in enumerate(titleList):
            itemChild = QtGui.QStandardItem(item)
            itemChild.setEditable(False)
            if chList:
                itemChild.setEnabled(False)
                for ch in chList[i]:
                    chItem = QtGui.QStandardItem(ch)
                    itemChild.appendRow(chItem)
                    chItem.setEditable(False)
            model_base.appendRow(itemChild)
        treeView.setModel(model_base)
        treeView.setHeaderHidden(True)
        treeView.setStyleSheet("font: 12pt 'Consolas';")

    @decorator_utils.one_undo
    def loadDX11(self, *args):
        SkinShaders = ls('SkinShader*')
        if SkinShaders != []:
            select(SkinShaders)
            cmds.warning(u'已经存在 SkinShader ,如果无用请删除后再导入---' + str(SkinShaders))
            return
        os.startfile(tool.scriptPath + '\\DX11')

    def importFilePath(self, fileNode, lineEdit, *args):
        """

        @param fileNode:
        @param lineEdit:
        @param args:
        @return:
        """
        self.dx11_filePath = r'R:\\rigToolset\\JunCmds\\JueJiFaceTool_2\\DX11\\'
        filePath = fileDialog(dm=self.dx11_filePath + '*.*', m=0)
        if filePath != '':
            if objExists(fileNode) == True and objectType(fileNode) == 'file':
                setAttr(fileNode + '.fileTextureName', filePath, type="string")
                select(fileNode)
            else:
                cmds.warning(u'运行失败，没有找到名字为---' + fileNode + '---的材质节点(file)')
            self.dx11_filePath = filePath[:-(len(filePath.split('/')[-1]))]
            lineEdit.setText(self.dx11_filePath)

    @decorator_utils.one_undo
    def face_control_to_Mask_expression(self, *args):  # DX11材质表达式
        face_control_to_MaskName = ls('face_control_to_Mask', type='expression')
        if face_control_to_MaskName:
            delete(face_control_to_MaskName)
        dx11s = ls(type='dx11Shader')
        SkinShader = ""
        if len(dx11s) == 1:
            SkinShader = dx11s[0]
        elif not dx11s:
            cmds.warning(u'失败,不存在dx11材质球,请先导入DX11材质球')
            return
        elif len(dx11s) > 1:
            select(dx11s)
            cmds.warning(u'失败,发现多个DX11材质球')
            return
        face_control_to_Mask_expressionStr = '''{0}.Mask1 = face_control.BrowOut_TY_L;
{0}.Mask2 = face_control.BrowIn_TY_L;
{0}.Mask3 = face_control.BrowIn_TY_R;
{0}.Mask4 = face_control.BrowOut_TY_R;
{0}.Mask5 = max(face_control.eye_look_dn_L,max(max(face_control.UprLid_TX_neg_L,(face_control.BrowOut_TY_L*0.5 + face_control.BrowIn_TY_L*0.5)),face_control.UprLid_TY_neg_L));
{0}.Mask6 = max(face_control.eye_look_dn_R,max(max(face_control.UprLid_TX_neg_R,(face_control.BrowOut_TY_R*0.5 + face_control.BrowIn_TY_R*0.5)),face_control.UprLid_TY_neg_R));

{0}.Mask7 =max(face_control.Crnr_TX_neg_L,max(face_control.Crnr_TX_neg_L,face_control.Mouth_TZ));
{0}.Mask8 =max(face_control.Crnr_TX_neg_R,max(face_control.Crnr_TX_neg_R,face_control.Mouth_TZ));
{0}.Mask9 =max(face_control.Jaw_TY_neg,face_control.Jaw_TY_neg * max(face_control.LwrLip_TX_neg_L,face_control.LwrLip_TX_neg_R));
//mask2 chanel 13-24
{0}.Mask13 = face_control.BrowIn_TY_neg_L*face_control.BrowIn_TX_neg_L;
{0}.Mask14 = face_control.BrowIn_TY_neg_R*face_control.BrowIn_TX_neg_R;

{0}.Mask15 = face_control.Nose_TY_L;
{0}.Mask16 = face_control.Nose_TY_R;
{0}.Mask17 = max(face_control.UprLip_2_TX_L,face_control.Nose_TY_L);
{0}.Mask18 = max(face_control.UprLip_2_TX_R,face_control.Nose_TY_R);
{0}.Mask19 = face_control.Chin_TY_neg_L;
{0}.Mask20 = face_control.Chin_TY_neg_R;
{0}.Mask21 = face_control.Chin_TX_L;
{0}.Mask22 = face_control.Chin_TX_R;

//mask3 chanel 25-36
{0}.Mask25 = face_control.BrowIn_TX_neg_L;
{0}.Mask26 = face_control.BrowIn_TX_neg_R;
{0}.Mask27 = face_control.EyeSqz_TY_neg_L;
{0}.Mask28 = face_control.EyeSqz_TY_neg_R;
{0}.Mask29 = face_control.EyeSqz_TY_neg_L*face_control.BrowIn_TY_neg_L*face_control.UprLid_TX_neg_L;
{0}.Mask30 = face_control.EyeSqz_TY_neg_R*face_control.BrowIn_TY_neg_R*face_control.UprLid_TX_neg_R;

{0}.Mask31 = face_control.Cheek_TY_L;
{0}.Mask32 = face_control.Cheek_TY_R;
{0}.Mask33 = max(face_control.Crnr_2_TX_L,face_control.Mouth_TX);
{0}.Mask34 = max(face_control.Crnr_2_TX_R,face_control.Mouth_TX_neg);
//mask3 chanel 37-48
//{0}.Mask37 = max(face_control.BrowIn_TX_neg_L,face_control.BrowIn_TX_neg_R)+face_control.Brow_TY;
{0}.Mask37 = face_control.Brow_TY;
{0}.Mask38 = face_control.Crnr_2_TY_neg_L;
{0}.Mask39 = face_control.Crnr_2_TY_neg_R;
{0}.Mask40 =max(face_control.LwrLip_TZ_L*0.2+face_control.LwrLip_TZ_R*0.2,max(face_control.UprLip_TY_neg*0.75,max(max((max((max(face_control.Mouth_TY,face_control.Jaw_TY)),face_control.LwrLip_TY)),face_control.Chin_TY),(face_control.LwrLip_TY_L*0.4+face_control.LwrLip_TY_R*0.4))));
'''.format(SkinShader)
        expression(s=face_control_to_Mask_expressionStr, name='face_control_to_Mask', ae=True, uc=all)
        cmds.warning(SkinShader + u'---褶皱驱动---is ok')

    def face_control_to_MaskAniAttr_expression(self, *args):  # 控制器关联mske属性，用于UE产生mske动画，继承到UE
        face_control_to_MaskAniAttr_exprName = ls('face_control_to_MaskAniAttr_expr', type='expression')
        if face_control_to_MaskAniAttr_exprName != []:
            delete(face_control_to_MaskAniAttr_exprName)
        maskAttrs = []
        if objExists('face_Head_base_jnt') != True:
            cmds.error(u'添加 WrinkleMask 属性的物体不存在------' + 'face_Head_base_jnt')
        allAttr = listAttr('face_Head_base_jnt')
        for i in range(48):
            attrName = 'WrinkleMask' + str('%.2d' % (i + 1))
            if attrName not in allAttr:
                addAttr('face_Head_base_jnt', ln='WrinkleMask' + str('%.2d' % (i + 1)),
                        at='double', dv=0, keyable=1)
        face_control_to_MaskAniAttr_expressionStr = '''face_Head_base_jnt.WrinkleMask01 = face_control.BrowOut_TY_L;
    face_Head_base_jnt.WrinkleMask02 = face_control.BrowIn_TY_L;
    face_Head_base_jnt.WrinkleMask03 = face_control.BrowIn_TY_R;
    face_Head_base_jnt.WrinkleMask04 = face_control.BrowOut_TY_R;
    face_Head_base_jnt.WrinkleMask05 = max(face_control.eye_look_dn_L,max(max(face_control.UprLid_TX_neg_L,(face_control.BrowOut_TY_L*0.5 + face_control.BrowIn_TY_L*0.5)),face_control.UprLid_TY_neg_L));
    face_Head_base_jnt.WrinkleMask06 = max(face_control.eye_look_dn_R,max(max(face_control.UprLid_TX_neg_R,(face_control.BrowOut_TY_R*0.5 + face_control.BrowIn_TY_R*0.5)),face_control.UprLid_TY_neg_R));

    face_Head_base_jnt.WrinkleMask07 =max(face_control.Crnr_TX_neg_L,max(face_control.Crnr_TX_neg_L,face_control.Mouth_TZ));
    face_Head_base_jnt.WrinkleMask08 =max(face_control.Crnr_TX_neg_R,max(face_control.Crnr_TX_neg_R,face_control.Mouth_TZ));
    face_Head_base_jnt.WrinkleMask09 =max(face_control.Jaw_TY_neg,face_control.Jaw_TY_neg * max(face_control.LwrLip_TX_neg_L,face_control.LwrLip_TX_neg_R));
    face_Head_base_jnt.WrinkleMask10 = 0;
    face_Head_base_jnt.WrinkleMask11 = 0;
    face_Head_base_jnt.WrinkleMask12 = 0;
    //mask2 chanel 13-24
    face_Head_base_jnt.WrinkleMask13 = face_control.BrowIn_TY_neg_L*face_control.BrowIn_TX_neg_L;
    face_Head_base_jnt.WrinkleMask14 = face_control.BrowIn_TY_neg_R*face_control.BrowIn_TX_neg_R;

    face_Head_base_jnt.WrinkleMask15 = face_control.Nose_TY_L;
    face_Head_base_jnt.WrinkleMask16 = face_control.Nose_TY_R;
    face_Head_base_jnt.WrinkleMask17 = max(face_control.UprLip_2_TX_L,face_control.Nose_TY_L);
    face_Head_base_jnt.WrinkleMask18 = max(face_control.UprLip_2_TX_R,face_control.Nose_TY_R);
    face_Head_base_jnt.WrinkleMask19 = face_control.Chin_TY_neg_L;
    face_Head_base_jnt.WrinkleMask20 = face_control.Chin_TY_neg_R;
    face_Head_base_jnt.WrinkleMask21 = face_control.Chin_TX_L;
    face_Head_base_jnt.WrinkleMask22 = face_control.Chin_TX_R;

    face_Head_base_jnt.WrinkleMask23 = 0;
    face_Head_base_jnt.WrinkleMask24 = 0;

    //mask3 chanel 25-36
    face_Head_base_jnt.WrinkleMask25 = face_control.BrowIn_TX_neg_L;
    face_Head_base_jnt.WrinkleMask26 = face_control.BrowIn_TX_neg_R;
    face_Head_base_jnt.WrinkleMask27 = face_control.EyeSqz_TY_neg_L;
    face_Head_base_jnt.WrinkleMask28 = face_control.EyeSqz_TY_neg_R;
    face_Head_base_jnt.WrinkleMask29 = face_control.EyeSqz_TY_neg_L*face_control.BrowIn_TY_neg_L*face_control.UprLid_TX_neg_L;
    face_Head_base_jnt.WrinkleMask30 = face_control.EyeSqz_TY_neg_R*face_control.BrowIn_TY_neg_R*face_control.UprLid_TX_neg_R;

    face_Head_base_jnt.WrinkleMask31 = face_control.Cheek_TY_L;
    face_Head_base_jnt.WrinkleMask32 = face_control.Cheek_TY_R;
    face_Head_base_jnt.WrinkleMask33 = max(face_control.Crnr_2_TX_L,face_control.Mouth_TX);
    face_Head_base_jnt.WrinkleMask34 = max(face_control.Crnr_2_TX_R,face_control.Mouth_TX_neg);

    face_Head_base_jnt.WrinkleMask35 = 0;
    face_Head_base_jnt.WrinkleMask36 = 0;

    //mask3 chanel 37-48
    //face_Head_base_jnt.WrinkleMask37 = max(face_control.BrowIn_TX_neg_L,face_control.BrowIn_TX_neg_R)+face_control.Brow_TY;
    face_Head_base_jnt.WrinkleMask37 = face_control.Brow_TY;
    face_Head_base_jnt.WrinkleMask38 = face_control.Crnr_2_TY_neg_L;
    face_Head_base_jnt.WrinkleMask39 = face_control.Crnr_2_TY_neg_R;
    face_Head_base_jnt.WrinkleMask40 =max(face_control.LwrLip_TZ_L*0.2+face_control.LwrLip_TZ_R*0.2,max(face_control.UprLip_TY_neg*0.75,max(max((max((max(face_control.Mouth_TY,face_control.Jaw_TY)),face_control.LwrLip_TY)),face_control.Chin_TY),(face_control.LwrLip_TY_L*0.4+face_control.LwrLip_TY_R*0.4))));

    face_Head_base_jnt.WrinkleMask41 = 0;
    face_Head_base_jnt.WrinkleMask42 = 0;
    face_Head_base_jnt.WrinkleMask43 = 0;
    face_Head_base_jnt.WrinkleMask44 = 0;
    face_Head_base_jnt.WrinkleMask45 = 0;
    face_Head_base_jnt.WrinkleMask46 = 0;
    face_Head_base_jnt.WrinkleMask47 = 0;
    face_Head_base_jnt.WrinkleMask48 = 0;
    '''
        expression(s=face_control_to_MaskAniAttr_expressionStr, name='face_control_to_MaskAniAttr_expr',
                   ae=True, uc=all)
        select('face_Head_base_jnt')
        cmds.warning(u'添加褶皱属性，用于继承动画褶皱动画---is ok')

    def loadGeometry(self, widget, *args):
        selection = cmds.ls(sl=True)
        if len(selection) > 1:
            return
        if widget.selectedIndexes():
            if selection:
                if "  --->  " in widget.selectedIndexes()[0].data():
                    widget.selectedItems()[0].setText(
                        widget.selectedIndexes()[0].data().split("  --->  ")[0] + "  --->  " + selection[0])
                else:
                    widget.selectedItems()[0].setText(widget.selectedIndexes()[0].data() + "  --->  " + selection[0])
            else:
                widget.selectedItems()[0].setText(widget.selectedIndexes()[0].data().split("  --->  ")[0])

    def importFile(self, *args):
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        templateFilePath = self.weightDataPathDict[self.mainUI.typeCombo.currentText()][1]
        filePath = cmds.fileDialog2(fm=1, okc='import', fileFilter=multipleFilters, dir=templateFilePath)[0]
        # filePath = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, dir=templateFilePath, okc='import')[0]
        cmds.file(filePath, i=True)

    def getReplaceInfo(self):
        self.oldMeshList = [''] * 4
        self.newMeshList = [''] * 4
        for i in range(self.mainUI.temp_list.count()):
            self.oldMeshList[i] = self.mainUI.temp_list.item(i).text().split("  --->  ")[-1]
        for i in range(self.mainUI.replace_list.count()):
            self.newMeshList[i] = self.mainUI.replace_list.item(i).text().split("  --->  ")[-1]
        # print([self.mainUI.temp_list.item(i).text().split("  --->  ")[-1] for i in range(self.mainUI.temp_list.count())])
        self.oldHead = self.oldMeshList[0]
        self.oldLEye = self.oldMeshList[1]
        self.oldREye = self.oldMeshList[2]
        self.oldTeeth = self.oldMeshList[3]

        self.newHead = self.newMeshList[0]
        self.newLEye = self.newMeshList[1]
        self.newREye = self.newMeshList[2]
        self.newTeeth = self.newMeshList[3]
        return self.oldMeshList, self.newMeshList

    def getLocPosition(self, vtx1, vtx2):
        if cmds.objExists(vtx1) and cmds.objExists(vtx2):
            pos1 = cmds.xform(vtx1, q=True, ws=True, t=True)
            pos2 = cmds.xform(vtx2, q=True, ws=True, t=True)
            pos = [0, (pos1[1] + pos2[1]) / 2, (pos1[2] + pos2[2]) / 2]
            return pos
        else:
            return []

    @decorator_utils.one_undo
    def autoMatch(self, *args):
        self.oldMeshList, self.newMeshList = self.getReplaceInfo()
        if self.newMeshList[0] == "Head_mdl": return
        topologyType = self.mainUI.typeCombo.currentText()
        basePos = self.getLocPosition("%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["base"][0]),
                                      "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["base"][1]))
        jawPos = self.getLocPosition("%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["jaw"][0]),
                                     "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["jaw"][1]))
        upTeethPos = self.getLocPosition(
            "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["upTeeth"][0]),
            "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["upTeeth"][1]))
        dnTeethPos = self.getLocPosition(
            "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["dnTeeth"][0]),
            "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["dnTeeth"][1]))
        jawEndPos = self.getLocPosition("%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["jawEnd"][0]),
                                        "%s.vtx[%d]" % (self.newMeshList[0], self.matchDict[topologyType]["jawEnd"][1]))
        if basePos and cmds.objExists("face_Head_base_loc"): cmds.xform("face_Head_base_loc", ws=True, t=basePos)
        if jawPos and cmds.objExists("jaw_zero_loc"): cmds.xform("jaw_zero_loc", ws=True, t=jawPos)
        if upTeethPos and cmds.objExists("upTeeth_01_loc"): cmds.xform("upTeeth_01_loc", ws=True, t=upTeethPos)
        if dnTeethPos and cmds.objExists("lwTeeth_01_loc"): cmds.xform("lwTeeth_01_loc", ws=True, t=dnTeethPos)
        if jawEndPos and cmds.objExists("jaw_02_loc"): cmds.xform("jaw_02_loc", ws=True, t=jawEndPos)
        self.matchEyeballPosition(self.newMeshList[1], "L_")
        self.matchEyeballPosition(self.newMeshList[2], "R_")

    @decorator_utils.one_undo
    def addBsNode(self, *args):
        selection = cmds.ls(sl=True)
        if not selection:
            return
        if selection.__len__() != 2:
            cmds.warning("Selected object number is not 2!")
            return
        targetModel, addblendShapeModel = selection
        SourceBlendShape = self.blendShapeNode(PyNode(addblendShapeModel))
        if SourceBlendShape:
            cmds.blendShape(SourceBlendShape[0].name(), edit=True, tc=False, target=(addblendShapeModel, len(cmds.aliasAttr(SourceBlendShape[0].name(), q=1)) + 1, targetModel, 1.0))
            cmds.setAttr(SourceBlendShape[0].name() + '.' + targetModel, 1)
        else:
            SourceBlendShape = addblendShapeModel + '_blendShape'
            SourceBlendShape = cmds.blendShape(addblendShapeModel, exclusive='deformPartition#', frontOfChain=True, name=SourceBlendShape)[0]
            cmds.blendShape(SourceBlendShape, edit=True, tc=False, target=(addblendShapeModel, 0, targetModel, 1.0))
            cmds.setAttr(SourceBlendShape + '.' + targetModel, 1)
        addblendShapeModelPar = cmds.listRelatives(addblendShapeModel, p=True)
        targetModelPar = cmds.listRelatives(targetModel, p=True)
        if targetModelPar != addblendShapeModelPar and addblendShapeModelPar is not None:
            cmds.parent(targetModel, addblendShapeModelPar)

    @decorator_utils.one_undo
    def replace(self, *args):
        self.oldMeshList, self.newMeshList = self.getReplaceInfo()
        self.oldHead = self.oldMeshList[0]
        self.oldLEye = self.oldMeshList[1]
        self.oldREye = self.oldMeshList[2]
        self.oldTeeth = self.oldMeshList[3]

        self.newHead = self.newMeshList[0]
        self.newLEye = self.newMeshList[1]
        self.newREye = self.newMeshList[2]
        self.newTeeth = self.newMeshList[3]

        self.replaceCorrectiveMesh(self.oldHead, self.newHead)
        self.replaceCorrectiveMesh(self.oldTeeth, self.newTeeth)
        if self.newHead != "Head_mdl":
            self.addFollicMeshBs(self.newHead, "facial_head_follic_model")
        if self.newTeeth != "Teeth":
            self.addFollicMeshBs(self.newTeeth, "facial_teeth_follic_model")
        if self.newLEye != "L_Eyeball":
            self.replaceEyeballMesh(self.newLEye, side="L_")
        if self.newREye != "R_Eyeball":
            self.replaceEyeballMesh(self.newREye, side="R_")

    def addFollicMeshBs(self, addObj, attrName):
        objList = cmds.ls(type="transform")
        for obj in objList:
            if cmds.objExists(obj + "." + attrName):
                cmds.select(obj, r=True)
                cmds.DeleteHistory()
                bsNode = cmds.blendShape(addObj, obj, exclusive='deformPartition#', frontOfChain=True)[0]
                cmds.setAttr(bsNode + "." + addObj, 1)

    def matchEyeballPosition(self, mesh, side="L_"):
        if mesh == "L_Eyeball" or mesh == "R_Eyeball":
            return
        cmds.select(mesh + ".vtx[*]", r=True)
        clust = cmds.cluster()
        if cmds.objExists(side + "eye_loc"):
            cmds.delete(cmds.pointConstraint(clust[-1], side + "eye_loc"))
        cmds.delete(clust)

    def replaceEyeballMesh(self, mesh, side="L_"):
        if mesh == "L_Eyeball" or mesh == "R_Eyeball":
            return
        objList = cmds.ls(type="transform")
        for obj in objList:
            if cmds.objExists("%s.%seye_skin_01_jnt" % (obj, side)):
                cmds.skinCluster(obj, mesh, tsb=True, nw=1, mi=2, dropoffRate=3.0, rui=False)

    def replaceCorrectiveMesh(self, old, new):
        if old == "Head_mdl" or new == "Head_mdl":
            return
        if old == "Teeth" or new == "Teeth":
            return
        old_sculpt = cmds.duplicate(old, name=old + "_sculpt")[0]
        cmds.select([old, old_sculpt], r=True)
        invertMesh = deformer_utils.invert()

        bsNode = cmds.blendShape(new, old_sculpt, exclusive='deformPartition#', frontOfChain=True)[0]
        cmds.setAttr(bsNode + "." + new, 1)

        bsNode_ = self.blendShapeNode(PyNode(old))
        if bsNode_:
            bsNode_ = bsNode_[0]
            weightList = cmds.listAttr(bsNode_ + '.weight', multi=True)
            cmds.blendShape(bsNode_.name(), edit=True, tc=False, target=(old, len(weightList), invertMesh, 1.0))

            cmds.setAttr(bsNode_ + ".weight[%d]" % len(weightList), 1)
            cmds.DeleteHistory(invertMesh)
            cmds.delete([invertMesh, old_sculpt])

        copyWeightObjSkin = mel.eval('findRelatedSkinCluster' + '("' + old + '")')
        copyWeightObjJnts = []
        if copyWeightObjSkin != '' and cmds.nodeType(copyWeightObjSkin) == 'skinCluster':
            copyWeightObjJnts = cmds.skinCluster(copyWeightObjSkin, q=True, inf=copyWeightObjSkin)
            cmds.skinCluster(copyWeightObjJnts, new, mi=10, rui=False, tsb=True)
            cmds.copySkinWeights(old, new, noMirror=True, surfaceAssociation='closestPoint',
                                 influenceAssociation=["closestJoint", "oneToOne"])

        cmds.refresh()
        cmds.select(d=1)

        if bsNode_:
            cmds.select([new, old], r=True)
            self.seekOutBs()

    def getBlendShapeWeight(self, bsNode):
        """#Get blendshape weights and return a list."""

        weightAttrPath = bsNode + '.weight'
        weightList = cmds.listAttr(weightAttrPath, multi=True)
        return weightList

    def seekOutBs(self, skipLock=True, replaceConnect=True):
        """seek out blendshape targt with original connection """

        meshList = cmds.ls(sl=True)
        length = len(meshList)

        if length == 2:
            pass
        else:
            cmds.error('please select aimMesh(1st) and orgMesh(2st)')

        aimObject = meshList[0]
        orgObject = meshList[1]

        # get org blendShape node
        bsNode = self.blendShapeNode(PyNode(orgObject))

        if bsNode is not None:
            bsList = self.getBlendShapeWeight(bsNode[0].name())[:-1]
            if bsList is not None:
                targtGrp = cmds.createNode('transform', name=orgObject + '_targt_grp')
                if aimObject is not None:

                    for bs in bsList:
                        if skipLock:
                            result = cmds.getAttr(bsNode[0] + '.' + bs, lock=True)
                            if result:
                                pass
                            else:
                                cmds.select(aimObject)
                                cmds.select(orgObject, add=True)
                                warpNode = mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0"}')[0]
                                cmds.select(cl=True)
                                cmds.setAttr(bsNode[0] + '.' + bs, 1)
                                cmds.duplicate(aimObject, name=bs)
                                cmds.delete(warpNode)
                                cmds.setAttr(bsNode[0] + '.' + bs, 0)

                        elif not skipLock:
                            cmds.select(aimObject)
                            cmds.select(orgObject, add=True)
                            warpNode = mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0"}')[0]
                            cmds.select(cl=True)
                            cmds.setAttr(bsNode[0] + '.' + bs, 1)
                            cmds.duplicate(aimObject, name=bs)
                            cmds.delete(warpNode)
                            cmds.setAttr(orgObject + '.' + bs, 0)

                            # clean
                        if cmds.objExists(orgObject + 'Base'):
                            cmds.delete(orgObject + 'Base')
                        if cmds.objExists(bs):
                            cmds.parent(bs, targtGrp)
                    # cmds.setAttr(bsNode[0] + '.' + bsList[-1], 1)
                    # create aimObject blendShape
                    targetList = cmds.listRelatives(targtGrp)
                    newBsNode = cmds.blendShape(targetList, aimObject, tc=True, name=aimObject + '_blendShape')[0]

                    # rebuild connection
                    if replaceConnect:
                        for bs in targetList:
                            attrSource = cmds.connectionInfo(bsNode[0] + '.' + bs, sfd=1)
                            if attrSource != '':
                                cmds.connectAttr(attrSource, newBsNode + '.' + bs)
                    cmds.delete(targtGrp)


def show_guide_component_manager(*args):
    ui_utils.showDialog(DockableDigitalFaceMainUI, dockable=True)
