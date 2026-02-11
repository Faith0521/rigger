#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/12/4 17:17
# @Author : yinyufei
# @File : combineMetaFace.py
# @Project : TeamCode
from functools import partial
from cgrigvendor.Qt import QtWidgets, QtCore, QtGui
from maya import cmds, mel
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.maya.cmds.rig import blendshape
from cgrig.libs.maya.cmds.rig import skin
from cgrig.libs.maya.cmds.skin import skinreplacejoints
import ngSkinTools2.api as ng2
from ngSkinTools2 import api as ngst_api
from ngSkinTools2.api import InfluenceMappingConfig, VertexTransferMode
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict


UI_MODE_COMPACT = 0
UI_MODE_ADVANCED = 1


class CombineMetaFace(toolsetwidget.ToolsetWidget):
    id = "combineMetaFace"
    info = "Auto Combine Meta Tool."
    uiData = {"label": "Combine Meta Face",
              "icon": "nodeTools",
              "defaultActionDoubleClick": False}

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        plugin_name = "ngSkinTools2"

        # 检查插件是否已加载
        if cmds.pluginInfo(plugin_name, query=True, loaded=True):
            print("\n// Result:{} 插件已加载.".format(plugin_name))
        else:
            print("\n// Result:{} 插件未加载.".format(plugin_name))

            # 如果未加载，则尝试手动加载插件
        if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
            try:
                cmds.loadPlugin(plugin_name)
                print("\n// Result:{plugin_name} 插件已成功加载.".format(plugin_name))
            except Exception as e:
                print("\n// Result:加载 {} 插件时出现错误: {}".format(plugin_name, e))

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]  # self.initAdvancedWidget()

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
        return super(CombineMetaFace, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[GuiAdvanced or GuiCompact]
        """
        return super(CombineMetaFace, self).widgets()

    # ------------------
    # LOGIC
    # ------------------
    def del_ngSkinNode(self):
        nodes_to_delete = []
        if cmds.pluginInfo('ngSkinTools2', query=True, loaded=True):
            nodes_to_delete = cmds.ls(type='ngst2SkinLayerData')
        if cmds.pluginInfo('ngSkinTools', query=True, loaded=True):
            nodes_to_delete += cmds.ls(type='ngSkinLayerData')

        if nodes_to_delete:
            cmds.delete(nodes_to_delete)

        mel.eval(u'print "// Result: ngSkinTools nodes have been cleared from the scene."')
        cmds.select(cl=True)
        cmds.setToolTo('selectSuperContext')

    def load(self, widget):
        selection = cmds.ls(selection=True)
        if not selection: return

        shapes = cmds.listRelatives(selection[0], s=1, noIntermediate=True)
        if not shapes:
            cmds.warning(u"选择的物体: {} 没有shape节点.".format(selection[0]))
            return

        nodeType = cmds.nodeType(shapes[0], api=True)
        if nodeType == 'kMesh':
            skinNode = mel.eval( 'findRelatedSkinCluster("{}")'.format(shapes[0]))
            if not skinNode:
                cmds.warning(u"选择的物体: {} 没有蒙皮节点.".format(shapes[0]))
                return
        widget.setText(selection[0])

    def copymodel(self, model):
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
        copysel = cmds.duplicate(model, name=model + '_duplicate')[0]
        shapes = cmds.listRelatives(copysel, s=True, f=True)
        for shape in shapes:
            if cmds.getAttr(shape + '.intermediateObject') == 1:
                cmds.delete(shape)

        for attr in attrs:
            cmds.setAttr(copysel + '.' + attr, lock=0)

        return copysel

    def base_layer_info(self, layers, layer_obj):
        # 使用缓存
        if hasattr(self, '_cached_base_layer_influences_od'):
            return self._cached_base_layer_influences_od

        influences_info = layers.list_influences()

        # 预提取路径和索引
        paths = [inf.path for inf in influences_info]
        indices = [inf.logicalIndex for inf in influences_info]

        # 并行获取权重
        with ThreadPoolExecutor(max_workers=4) as executor:
            weights = list(executor.map(layer_obj.get_weights, indices))

        # 使用生成器表达式创建字典
        self._cached_base_layer_influences_od = OrderedDict(
            sorted(
                ((path, [idx, weight]) for path, idx, weight in zip(paths, indices, weights)),
                key=lambda x: len(x[0])
            )
        )
        return self._cached_base_layer_influences_od

    def get_fit_inf(self, fit_jnt, layers, layer_obj):
        fit_inf = None
        fit_index = None
        fit_weights = None
        for long in self.base_layer_info(layers, layer_obj).keys():
            if long == cmds.ls(fit_jnt, long=True)[0]:
                fit_inf = long
                fit_index, fit_weights = self.base_layer_info[fit_inf]
        return (fit_inf, fit_index)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def apply(self):
        start_time = time.time()
        body_hi_name = self.compactWidget.loadBodyLe.text()
        head_mdl_name = self.compactWidget.loadHeadLe.text()
        if body_hi_name == "" or head_mdl_name == "":
            return

        body_hi_dup = self.copymodel(body_hi_name)
        head_mdl_dup = self.copymodel(head_mdl_name)

        blendshape.copyBs(head_mdl_name, body_hi_dup, skipLock=True, replaceConnect=True)

        verts = cmds.ls(cmds.polyListComponentConversion(body_hi_dup, toVertex=True), fl=True)

        skin_body = skin.copySkin(body_hi_name, body_hi_dup, "closestJoint", "closestJoint")
        skin_head = skin.copySkin(head_mdl_name, head_mdl_dup, "closestJoint", "closestJoint")

        if not cmds.objExists("FACIAL_C_Neck1Root") or not cmds.objExists("FACIAL_C_Neck2Root") or not cmds.objExists("FACIAL_C_FacialRoot"):
            cmds.warning(u"//检查场景内是否存在以下名称的骨骼: {} /n {} /n {}".format("FACIAL_C_Neck1Root", "FACIAL_C_Neck2Root", "FACIAL_C_FacialRoot"))
        try:
            cmds.parent("FACIAL_C_Neck1Root", "Neck2")
            cmds.parent("FACIAL_C_Neck2Root", "Neck3")
            cmds.parent("FACIAL_C_FacialRoot", "Head")
        except:
            RuntimeWarning(u"//处理骨骼层级时出错")

        # 处理head模型
        cmds.skinCluster(skin_head, e=1, dr=4, lw=1, wt=0, ai=["ChestMid", "Head"])
        skinreplacejoints.replaceSkinJoint('head', 'Head', unbindSource=True, skipSkinClusters=(), skin_name=skin_head)
        del_joints = ['spine_04', 'clavicle_pec_l', 'clavicle_pec_r', 'spine_04_latissimus_l', 'spine_04_latissimus_r', 'clavicle_l', 'clavicle_out_l',
                      'clavicle_scap_l', 'upperarm_out_l', 'upperarm_fwd_l', 'upperarm_in_l', 'upperarm_bck_l', 'clavicle_r',
                      'clavicle_out_r', 'clavicle_scap_r', 'upperarm_out_r', 'upperarm_fwd_r', 'upperarm_in_r', 'upperarm_bck_r']
        skinreplacejoints.replaceSkinJointsToOne(del_joints, 'ChestMid',
                                                 moveWithJoints=False, unbindSource=False, skipSkinClusters=(), skin_name=skin_head)
        cmds.refresh()

        # 处理身体
        meta_skin_jnts = ['FACIAL_C_NeckB',
 'FACIAL_L_NeckB1',
 'FACIAL_R_NeckB1',
 'FACIAL_L_NeckB2',
 'FACIAL_R_NeckB2',
 'FACIAL_C_12IPV_NeckB1',
 'FACIAL_C_12IPV_NeckB2',
 'FACIAL_L_12IPV_NeckB3',
 'FACIAL_R_12IPV_NeckB3',
 'FACIAL_L_12IPV_NeckB4',
 'FACIAL_R_12IPV_NeckB4',
 'FACIAL_L_12IPV_NeckB5',
 'FACIAL_R_12IPV_NeckB5',
 'FACIAL_L_12IPV_NeckB6',
 'FACIAL_R_12IPV_NeckB6',
 'FACIAL_L_12IPV_NeckB7',
 'FACIAL_R_12IPV_NeckB7',
 'FACIAL_C_NeckBackB',
 'FACIAL_L_NeckBackB',
 'FACIAL_R_NeckBackB',
 'FACIAL_C_12IPV_NeckBackB1',
 'FACIAL_C_12IPV_NeckBackB2',
 'FACIAL_L_12IPV_NeckBackB1',
 'FACIAL_R_12IPV_NeckBackB1',
 'FACIAL_L_12IPV_NeckBackB2',
 'FACIAL_R_12IPV_NeckBackB2',
 'FACIAL_C_Neck1Root',
 'FACIAL_C_AdamsApple',
 'FACIAL_C_12IPV_AdamsA1',
 'FACIAL_C_12IPV_AdamsA2',
 'FACIAL_L_NeckA1',
 'FACIAL_R_NeckA1',
 'FACIAL_L_NeckA2',
 'FACIAL_R_NeckA2',
 'FACIAL_L_NeckA3',
 'FACIAL_R_NeckA3',
 'FACIAL_L_12IPV_NeckA1',
 'FACIAL_R_12IPV_NeckA1',
 'FACIAL_L_12IPV_NeckA2',
 'FACIAL_R_12IPV_NeckA2',
 'FACIAL_L_12IPV_NeckA3',
 'FACIAL_R_12IPV_NeckA3',
 'FACIAL_L_12IPV_NeckA4',
 'FACIAL_R_12IPV_NeckA4',
 'FACIAL_L_12IPV_NeckA5',
 'FACIAL_R_12IPV_NeckA5',
 'FACIAL_L_12IPV_NeckA6',
 'FACIAL_R_12IPV_NeckA6',
 'FACIAL_C_NeckBackA',
 'FACIAL_L_NeckBackA',
 'FACIAL_R_NeckBackA',
 'FACIAL_C_12IPV_NeckBackA1',
 'FACIAL_C_12IPV_NeckBackA2',
 'FACIAL_L_12IPV_NeckBackA1',
 'FACIAL_R_12IPV_NeckBackA1',
 'FACIAL_L_12IPV_NeckBackA2',
 'FACIAL_R_12IPV_NeckBackA2',
 'FACIAL_C_Neck2Root',
 'FACIAL_C_Hair1',
 'FACIAL_L_12IPV_Hair1',
 'FACIAL_R_12IPV_Hair1',
 'FACIAL_C_Hair2',
 'FACIAL_C_Hair3',
 'FACIAL_C_Hair4',
 'FACIAL_C_Hair5',
 'FACIAL_C_Hair6',
 'FACIAL_L_HairA1',
 'FACIAL_R_HairA1',
 'FACIAL_L_HairA2',
 'FACIAL_R_HairA2',
 'FACIAL_L_HairA3',
 'FACIAL_R_HairA3',
 'FACIAL_L_HairA4',
 'FACIAL_R_HairA4',
 'FACIAL_L_HairA5',
 'FACIAL_R_HairA5',
 'FACIAL_L_HairA6',
 'FACIAL_R_HairA6',
 'FACIAL_L_HairB1',
 'FACIAL_R_HairB1',
 'FACIAL_L_HairB2',
 'FACIAL_R_HairB2',
 'FACIAL_L_HairB3',
 'FACIAL_R_HairB3',
 'FACIAL_L_HairB4',
 'FACIAL_R_HairB4',
 'FACIAL_L_HairB5',
 'FACIAL_R_HairB5',
 'FACIAL_L_Temple',
 'FACIAL_R_Temple',
 'FACIAL_L_12IPV_Temple1',
 'FACIAL_R_12IPV_Temple1',
 'FACIAL_L_12IPV_Temple2',
 'FACIAL_R_12IPV_Temple2',
 'FACIAL_L_12IPV_Temple3',
 'FACIAL_R_12IPV_Temple3',
 'FACIAL_L_12IPV_Temple4',
 'FACIAL_R_12IPV_Temple4',
 'FACIAL_L_HairC1',
 'FACIAL_R_HairC1',
 'FACIAL_L_HairC2',
 'FACIAL_R_HairC2',
 'FACIAL_L_HairC3',
 'FACIAL_R_HairC3',
 'FACIAL_L_HairC4',
 'FACIAL_R_HairC4',
 'FACIAL_L_Sideburn1',
 'FACIAL_R_Sideburn1',
 'FACIAL_L_Sideburn2',
 'FACIAL_R_Sideburn2',
 'FACIAL_L_Sideburn3',
 'FACIAL_R_Sideburn3',
 'FACIAL_L_Sideburn4',
 'FACIAL_R_Sideburn4',
 'FACIAL_L_Sideburn5',
 'FACIAL_R_Sideburn5',
 'FACIAL_L_Sideburn6',
 'FACIAL_R_Sideburn6',
 'FACIAL_C_ForeheadSkin',
 'FACIAL_L_ForeheadInSkin',
 'FACIAL_R_ForeheadInSkin',
 'FACIAL_L_12IPV_ForeheadSkin1',
 'FACIAL_R_12IPV_ForeheadSkin1',
 'FACIAL_L_12IPV_ForeheadSkin2',
 'FACIAL_R_12IPV_ForeheadSkin2',
 'FACIAL_L_12IPV_ForeheadSkin3',
 'FACIAL_R_12IPV_ForeheadSkin3',
 'FACIAL_L_12IPV_ForeheadSkin4',
 'FACIAL_R_12IPV_ForeheadSkin4',
 'FACIAL_L_12IPV_ForeheadSkin5',
 'FACIAL_R_12IPV_ForeheadSkin5',
 'FACIAL_L_12IPV_ForeheadSkin6',
 'FACIAL_R_12IPV_ForeheadSkin6',
 'FACIAL_L_ForeheadMidSkin',
 'FACIAL_R_ForeheadMidSkin',
 'FACIAL_L_ForeheadOutSkin',
 'FACIAL_R_ForeheadOutSkin',
 'FACIAL_C_Skull',
 'FACIAL_C_Forehead1',
 'FACIAL_L_Forehead1',
 'FACIAL_R_Forehead1',
 'FACIAL_C_Forehead2',
 'FACIAL_L_Forehead2',
 'FACIAL_R_Forehead2',
 'FACIAL_C_Forehead3',
 'FACIAL_L_Forehead3',
 'FACIAL_R_Forehead3',
 'FACIAL_C_12IPV_Forehead1',
 'FACIAL_L_12IPV_Forehead1',
 'FACIAL_R_12IPV_Forehead1',
 'FACIAL_C_12IPV_Forehead2',
 'FACIAL_L_12IPV_Forehead2',
 'FACIAL_R_12IPV_Forehead2',
 'FACIAL_C_12IPV_Forehead3',
 'FACIAL_L_12IPV_Forehead3',
 'FACIAL_R_12IPV_Forehead3',
 'FACIAL_C_12IPV_Forehead4',
 'FACIAL_L_12IPV_Forehead4',
 'FACIAL_R_12IPV_Forehead4',
 'FACIAL_C_12IPV_Forehead5',
 'FACIAL_L_12IPV_Forehead5',
 'FACIAL_R_12IPV_Forehead5',
 'FACIAL_C_12IPV_Forehead6',
 'FACIAL_L_12IPV_Forehead6',
 'FACIAL_R_12IPV_Forehead6',
 'FACIAL_C_Forehead',
 'FACIAL_L_ForeheadInA1',
 'FACIAL_L_ForeheadInA2',
 'FACIAL_L_ForeheadInA3',
 'FACIAL_L_ForeheadInB1',
 'FACIAL_L_ForeheadInB2',
 'FACIAL_L_12IPV_ForeheadIn1',
 'FACIAL_L_12IPV_ForeheadIn2',
 'FACIAL_L_12IPV_ForeheadIn3',
 'FACIAL_L_12IPV_ForeheadIn4',
 'FACIAL_L_12IPV_ForeheadIn5',
 'FACIAL_L_12IPV_ForeheadIn6',
 'FACIAL_L_12IPV_ForeheadIn7',
 'FACIAL_L_12IPV_ForeheadIn8',
 'FACIAL_L_12IPV_ForeheadIn9',
 'FACIAL_L_12IPV_ForeheadIn10',
 'FACIAL_L_12IPV_ForeheadIn11',
 'FACIAL_L_12IPV_ForeheadIn12',
 'FACIAL_L_12IPV_ForeheadIn13',
 'FACIAL_L_12IPV_ForeheadIn14',
 'FACIAL_L_ForeheadIn',
 'FACIAL_R_ForeheadInA1',
 'FACIAL_R_ForeheadInA2',
 'FACIAL_R_ForeheadInA3',
 'FACIAL_R_ForeheadInB1',
 'FACIAL_R_ForeheadInB2',
 'FACIAL_R_12IPV_ForeheadIn1',
 'FACIAL_R_12IPV_ForeheadIn2',
 'FACIAL_R_12IPV_ForeheadIn3',
 'FACIAL_R_12IPV_ForeheadIn5',
 'FACIAL_R_12IPV_ForeheadIn4',
 'FACIAL_R_12IPV_ForeheadIn6',
 'FACIAL_R_12IPV_ForeheadIn7',
 'FACIAL_R_12IPV_ForeheadIn8',
 'FACIAL_R_12IPV_ForeheadIn9',
 'FACIAL_R_12IPV_ForeheadIn10',
 'FACIAL_R_12IPV_ForeheadIn12',
 'FACIAL_R_12IPV_ForeheadIn11',
 'FACIAL_R_12IPV_ForeheadIn13',
 'FACIAL_R_12IPV_ForeheadIn14',
 'FACIAL_R_ForeheadIn',
 'FACIAL_L_ForeheadMid1',
 'FACIAL_L_ForeheadMid2',
 'FACIAL_L_12IPV_ForeheadMid15',
 'FACIAL_L_12IPV_ForeheadMid16',
 'FACIAL_L_12IPV_ForeheadMid17',
 'FACIAL_L_12IPV_ForeheadMid18',
 'FACIAL_L_12IPV_ForeheadMid19',
 'FACIAL_L_12IPV_ForeheadMid20',
 'FACIAL_L_12IPV_ForeheadMid21',
 'FACIAL_L_12IPV_ForeheadMid22',
 'FACIAL_L_ForeheadMid',
 'FACIAL_R_ForeheadMid1',
 'FACIAL_R_ForeheadMid2',
 'FACIAL_R_12IPV_ForeheadMid15',
 'FACIAL_R_12IPV_ForeheadMid16',
 'FACIAL_R_12IPV_ForeheadMid17',
 'FACIAL_R_12IPV_ForeheadMid18',
 'FACIAL_R_12IPV_ForeheadMid19',
 'FACIAL_R_12IPV_ForeheadMid20',
 'FACIAL_R_12IPV_ForeheadMid21',
 'FACIAL_R_12IPV_ForeheadMid22',
 'FACIAL_R_ForeheadMid',
 'FACIAL_L_ForeheadOutA1',
 'FACIAL_L_ForeheadOutA2',
 'FACIAL_L_ForeheadOutB1',
 'FACIAL_L_ForeheadOutB2',
 'FACIAL_L_12IPV_ForeheadOut23',
 'FACIAL_L_12IPV_ForeheadOut24',
 'FACIAL_L_12IPV_ForeheadOut25',
 'FACIAL_L_12IPV_ForeheadOut26',
 'FACIAL_L_12IPV_ForeheadOut27',
 'FACIAL_L_12IPV_ForeheadOut28',
 'FACIAL_L_12IPV_ForeheadOut29',
 'FACIAL_L_12IPV_ForeheadOut30',
 'FACIAL_L_12IPV_ForeheadOut31',
 'FACIAL_L_12IPV_ForeheadOut32',
 'FACIAL_L_ForeheadOut',
 'FACIAL_R_ForeheadOutA1',
 'FACIAL_R_ForeheadOutA2',
 'FACIAL_R_ForeheadOutB1',
 'FACIAL_R_ForeheadOutB2',
 'FACIAL_R_12IPV_ForeheadOut23',
 'FACIAL_R_12IPV_ForeheadOut24',
 'FACIAL_R_12IPV_ForeheadOut25',
 'FACIAL_R_12IPV_ForeheadOut26',
 'FACIAL_R_12IPV_ForeheadOut27',
 'FACIAL_R_12IPV_ForeheadOut28',
 'FACIAL_R_12IPV_ForeheadOut29',
 'FACIAL_R_12IPV_ForeheadOut30',
 'FACIAL_R_12IPV_ForeheadOut31',
 'FACIAL_R_12IPV_ForeheadOut32',
 'FACIAL_R_ForeheadOut',
 'FACIAL_L_12IPV_EyesackU0',
 'FACIAL_R_12IPV_EyesackU0',
 'FACIAL_L_EyesackUpper1',
 'FACIAL_L_EyesackUpper2',
 'FACIAL_L_EyesackUpper3',
 'FACIAL_L_EyesackUpper',
 'FACIAL_R_EyesackUpper1',
 'FACIAL_R_EyesackUpper2',
 'FACIAL_R_EyesackUpper3',
 'FACIAL_R_EyesackUpper',
 'FACIAL_L_EyesackUpper4',
 'FACIAL_R_EyesackUpper4',
 'FACIAL_L_EyelidUpperFurrow1',
 'FACIAL_L_EyelidUpperFurrow2',
 'FACIAL_L_EyelidUpperFurrow3',
 'FACIAL_L_EyelidUpperFurrow',
 'FACIAL_R_EyelidUpperFurrow1',
 'FACIAL_R_EyelidUpperFurrow2',
 'FACIAL_R_EyelidUpperFurrow3',
 'FACIAL_R_EyelidUpperFurrow',
 'FACIAL_L_EyelidUpperB1',
 'FACIAL_L_EyelidUpperB2',
 'FACIAL_L_EyelidUpperB3',
 'FACIAL_L_EyelidUpperB',
 'FACIAL_R_EyelidUpperB1',
 'FACIAL_R_EyelidUpperB2',
 'FACIAL_R_EyelidUpperB3',
 'FACIAL_R_EyelidUpperB',
 'FACIAL_L_EyelashesUpperA1',
 'FACIAL_L_EyelidUpperA1',
 'FACIAL_L_EyelashesUpperA2',
 'FACIAL_L_EyelidUpperA2',
 'FACIAL_L_EyelashesUpperA3',
 'FACIAL_L_EyelidUpperA3',
 'FACIAL_L_EyelidUpperA',
 'FACIAL_R_EyelashesUpperA1',
 'FACIAL_R_EyelidUpperA1',
 'FACIAL_R_EyelashesUpperA2',
 'FACIAL_R_EyelidUpperA2',
 'FACIAL_R_EyelashesUpperA3',
 'FACIAL_R_EyelidUpperA3',
 'FACIAL_R_EyelidUpperA',
 'FACIAL_L_Pupil',
 'FACIAL_L_EyeParallel',
 'FACIAL_L_Eye',
 'FACIAL_R_Pupil',
 'FACIAL_R_EyeParallel',
 'FACIAL_R_Eye',
 'FACIAL_L_EyelidLowerA1',
 'FACIAL_L_EyelidLowerA2',
 'FACIAL_L_EyelidLowerA3',
 'FACIAL_L_EyelidLowerA',
 'FACIAL_R_EyelidLowerA1',
 'FACIAL_R_EyelidLowerA2',
 'FACIAL_R_EyelidLowerA3',
 'FACIAL_R_EyelidLowerA',
 'FACIAL_L_EyelidLowerB1',
 'FACIAL_L_EyelidLowerB2',
 'FACIAL_L_EyelidLowerB3',
 'FACIAL_L_EyelidLowerB',
 'FACIAL_R_EyelidLowerB1',
 'FACIAL_R_EyelidLowerB2',
 'FACIAL_R_EyelidLowerB3',
 'FACIAL_R_EyelidLowerB',
 'FACIAL_L_EyeCornerInner1',
 'FACIAL_L_EyeCornerInner2',
 'FACIAL_L_EyeCornerInner',
 'FACIAL_R_EyeCornerInner1',
 'FACIAL_R_EyeCornerInner2',
 'FACIAL_R_EyeCornerInner',
 'FACIAL_L_EyelashesCornerOuter1',
 'FACIAL_L_EyeCornerOuter1',
 'FACIAL_L_EyeCornerOuter2',
 'FACIAL_L_EyeCornerOuter',
 'FACIAL_R_EyelashesCornerOuter1',
 'FACIAL_R_EyeCornerOuter1',
 'FACIAL_R_EyeCornerOuter2',
 'FACIAL_R_EyeCornerOuter',
 'FACIAL_L_12IPV_EyeCornerO1',
 'FACIAL_R_12IPV_EyeCornerO1',
 'FACIAL_L_12IPV_EyeCornerO2',
 'FACIAL_R_12IPV_EyeCornerO2',
 'FACIAL_L_EyesackLower1',
 'FACIAL_L_EyesackLower2',
 'FACIAL_L_12IPV_EyesackL1',
 'FACIAL_L_12IPV_EyesackL2',
 'FACIAL_L_12IPV_EyesackL3',
 'FACIAL_L_12IPV_EyesackL4',
 'FACIAL_L_12IPV_EyesackL5',
 'FACIAL_L_12IPV_EyesackL6',
 'FACIAL_L_12IPV_EyesackL7',
 'FACIAL_L_12IPV_EyesackL8',
 'FACIAL_L_EyesackLower',
 'FACIAL_R_EyesackLower1',
 'FACIAL_R_EyesackLower2',
 'FACIAL_R_12IPV_EyesackL1',
 'FACIAL_R_12IPV_EyesackL2',
 'FACIAL_R_12IPV_EyesackL3',
 'FACIAL_R_12IPV_EyesackL4',
 'FACIAL_R_12IPV_EyesackL5',
 'FACIAL_R_12IPV_EyesackL6',
 'FACIAL_R_12IPV_EyesackL7',
 'FACIAL_R_12IPV_EyesackL8',
 'FACIAL_R_EyesackLower',
 'FACIAL_L_CheekInner1',
 'FACIAL_L_CheekInner2',
 'FACIAL_L_CheekInner3',
 'FACIAL_L_CheekInner4',
 'FACIAL_L_CheekInner',
 'FACIAL_R_CheekInner1',
 'FACIAL_R_CheekInner2',
 'FACIAL_R_CheekInner3',
 'FACIAL_R_CheekInner4',
 'FACIAL_R_CheekInner',
 'FACIAL_L_CheekOuter1',
 'FACIAL_L_CheekOuter2',
 'FACIAL_L_CheekOuter3',
 'FACIAL_L_CheekOuter',
 'FACIAL_R_CheekOuter1',
 'FACIAL_R_CheekOuter2',
 'FACIAL_R_CheekOuter3',
 'FACIAL_R_CheekOuter',
 'FACIAL_L_CheekOuter4',
 'FACIAL_R_CheekOuter4',
 'FACIAL_L_12IPV_CheekOuter1',
 'FACIAL_R_12IPV_CheekOuter1',
 'FACIAL_L_12IPV_CheekOuter2',
 'FACIAL_R_12IPV_CheekOuter2',
 'FACIAL_L_12IPV_CheekOuter3',
 'FACIAL_R_12IPV_CheekOuter3',
 'FACIAL_L_12IPV_CheekOuter4',
 'FACIAL_R_12IPV_CheekOuter4',
 'FACIAL_C_NoseBridge',
 'FACIAL_C_12IPV_NoseBridge1',
 'FACIAL_L_12IPV_NoseBridge1',
 'FACIAL_R_12IPV_NoseBridge1',
 'FACIAL_C_12IPV_NoseBridge2',
 'FACIAL_L_12IPV_NoseBridge2',
 'FACIAL_R_12IPV_NoseBridge2',
 'FACIAL_L_NoseBridge',
 'FACIAL_R_NoseBridge',
 'FACIAL_C_NoseUpper',
 'FACIAL_L_NoseUpper',
 'FACIAL_R_NoseUpper',
 'FACIAL_C_12IPV_NoseUpper1',
 'FACIAL_C_12IPV_NoseUpper2',
 'FACIAL_L_12IPV_NoseUpper1',
 'FACIAL_R_12IPV_NoseUpper1',
 'FACIAL_L_12IPV_NoseUpper2',
 'FACIAL_R_12IPV_NoseUpper2',
 'FACIAL_L_12IPV_NoseUpper3',
 'FACIAL_R_12IPV_NoseUpper3',
 'FACIAL_L_12IPV_NoseUpper4',
 'FACIAL_R_12IPV_NoseUpper4',
 'FACIAL_L_12IPV_NoseUpper5',
 'FACIAL_R_12IPV_NoseUpper5',
 'FACIAL_L_12IPV_NoseUpper6',
 'FACIAL_R_12IPV_NoseUpper6',
 'FACIAL_L_NasolabialBulge1',
 'FACIAL_R_NasolabialBulge1',
 'FACIAL_L_12IPV_NasolabialB13',
 'FACIAL_R_12IPV_NasolabialB13',
 'FACIAL_L_12IPV_NasolabialB14',
 'FACIAL_R_12IPV_NasolabialB14',
 'FACIAL_L_12IPV_NasolabialB15',
 'FACIAL_R_12IPV_NasolabialB15',
 'FACIAL_L_NasolabialBulge2',
 'FACIAL_L_NasolabialBulge3',
 'FACIAL_L_12IPV_NasolabialB1',
 'FACIAL_L_12IPV_NasolabialB2',
 'FACIAL_L_12IPV_NasolabialB3',
 'FACIAL_L_12IPV_NasolabialB4',
 'FACIAL_L_12IPV_NasolabialB5',
 'FACIAL_L_12IPV_NasolabialB6',
 'FACIAL_L_12IPV_NasolabialB7',
 'FACIAL_L_12IPV_NasolabialB8',
 'FACIAL_L_12IPV_NasolabialB9',
 'FACIAL_L_12IPV_NasolabialB10',
 'FACIAL_L_12IPV_NasolabialB11',
 'FACIAL_L_12IPV_NasolabialB12',
 'FACIAL_L_NasolabialBulge',
 'FACIAL_R_NasolabialBulge2',
 'FACIAL_R_NasolabialBulge3',
 'FACIAL_R_12IPV_NasolabialB1',
 'FACIAL_R_12IPV_NasolabialB2',
 'FACIAL_R_12IPV_NasolabialB3',
 'FACIAL_R_12IPV_NasolabialB4',
 'FACIAL_R_12IPV_NasolabialB5',
 'FACIAL_R_12IPV_NasolabialB6',
 'FACIAL_R_12IPV_NasolabialB7',
 'FACIAL_R_12IPV_NasolabialB8',
 'FACIAL_R_12IPV_NasolabialB9',
 'FACIAL_R_12IPV_NasolabialB10',
 'FACIAL_R_12IPV_NasolabialB11',
 'FACIAL_R_12IPV_NasolabialB12',
 'FACIAL_R_NasolabialBulge',
 'FACIAL_L_NasolabialFurrow',
 'FACIAL_R_NasolabialFurrow',
 'FACIAL_L_12IPV_NasolabialF1',
 'FACIAL_R_12IPV_NasolabialF1',
 'FACIAL_L_12IPV_NasolabialF2',
 'FACIAL_R_12IPV_NasolabialF2',
 'FACIAL_L_12IPV_NasolabialF3',
 'FACIAL_R_12IPV_NasolabialF3',
 'FACIAL_L_12IPV_NasolabialF4',
 'FACIAL_R_12IPV_NasolabialF4',
 'FACIAL_L_12IPV_NasolabialF5',
 'FACIAL_R_12IPV_NasolabialF5',
 'FACIAL_L_12IPV_NasolabialF6',
 'FACIAL_R_12IPV_NasolabialF6',
 'FACIAL_L_12IPV_NasolabialF7',
 'FACIAL_R_12IPV_NasolabialF7',
 'FACIAL_L_12IPV_NasolabialF8',
 'FACIAL_R_12IPV_NasolabialF8',
 'FACIAL_L_12IPV_NasolabialF9',
 'FACIAL_R_12IPV_NasolabialF9',
 'FACIAL_L_CheekLower1',
 'FACIAL_L_CheekLower2',
 'FACIAL_L_12IPV_CheekL1',
 'FACIAL_L_12IPV_CheekL2',
 'FACIAL_L_12IPV_CheekL3',
 'FACIAL_L_12IPV_CheekL4',
 'FACIAL_L_CheekLower',
 'FACIAL_R_CheekLower1',
 'FACIAL_R_CheekLower2',
 'FACIAL_R_12IPV_CheekL1',
 'FACIAL_R_12IPV_CheekL2',
 'FACIAL_R_12IPV_CheekL3',
 'FACIAL_R_12IPV_CheekL4',
 'FACIAL_R_CheekLower',
 'FACIAL_L_Ear1',
 'FACIAL_L_Ear2',
 'FACIAL_L_Ear3',
 'FACIAL_L_Ear4',
 'FACIAL_L_Ear',
 'FACIAL_R_Ear1',
 'FACIAL_R_Ear2',
 'FACIAL_R_Ear3',
 'FACIAL_R_Ear4',
 'FACIAL_R_Ear',
 'FACIAL_L_NostrilThickness3',
 'FACIAL_R_NostrilThickness3',
 'FACIAL_C_12IPV_NoseL1',
 'FACIAL_C_12IPV_NoseL2',
 'FACIAL_C_NoseLower',
 'FACIAL_C_12IPV_NoseTip1',
 'FACIAL_C_12IPV_NoseTip2',
 'FACIAL_C_12IPV_NoseTip3',
 'FACIAL_L_12IPV_NoseTip1',
 'FACIAL_R_12IPV_NoseTip1',
 'FACIAL_L_12IPV_NoseTip2',
 'FACIAL_R_12IPV_NoseTip2',
 'FACIAL_L_12IPV_NoseTip3',
 'FACIAL_R_12IPV_NoseTip3',
 'FACIAL_C_NoseTip',
 'FACIAL_L_NostrilThickness1',
 'FACIAL_L_NostrilThickness2',
 'FACIAL_L_12IPV_Nostril1',
 'FACIAL_L_12IPV_Nostril2',
 'FACIAL_L_12IPV_Nostril3',
 'FACIAL_L_12IPV_Nostril4',
 'FACIAL_L_12IPV_Nostril5',
 'FACIAL_L_12IPV_Nostril6',
 'FACIAL_L_12IPV_Nostril7',
 'FACIAL_L_12IPV_Nostril8',
 'FACIAL_L_12IPV_Nostril9',
 'FACIAL_L_12IPV_Nostril10',
 'FACIAL_L_12IPV_Nostril11',
 'FACIAL_L_12IPV_Nostril12',
 'FACIAL_L_12IPV_Nostril13',
 'FACIAL_L_12IPV_Nostril14',
 'FACIAL_L_Nostril',
 'FACIAL_R_NostrilThickness1',
 'FACIAL_R_NostrilThickness2',
 'FACIAL_R_12IPV_Nostril1',
 'FACIAL_R_12IPV_Nostril2',
 'FACIAL_R_12IPV_Nostril3',
 'FACIAL_R_12IPV_Nostril4',
 'FACIAL_R_12IPV_Nostril5',
 'FACIAL_R_12IPV_Nostril6',
 'FACIAL_R_12IPV_Nostril7',
 'FACIAL_R_12IPV_Nostril8',
 'FACIAL_R_12IPV_Nostril9',
 'FACIAL_R_12IPV_Nostril10',
 'FACIAL_R_12IPV_Nostril11',
 'FACIAL_R_12IPV_Nostril12',
 'FACIAL_R_12IPV_Nostril13',
 'FACIAL_R_12IPV_Nostril14',
 'FACIAL_R_Nostril',
 'FACIAL_C_Nose',
 'FACIAL_C_LipUpperSkin',
 'FACIAL_L_LipUpperSkin',
 'FACIAL_R_LipUpperSkin',
 'FACIAL_L_LipUpperOuterSkin',
 'FACIAL_R_LipUpperOuterSkin',
 'FACIAL_C_12IPV_LipUpperSkin1',
 'FACIAL_C_12IPV_LipUpperSkin2',
 'FACIAL_L_12IPV_LipUpperSkin',
 'FACIAL_R_12IPV_LipUpperSkin',
 'FACIAL_L_12IPV_LipUpperOuterSkin1',
 'FACIAL_R_12IPV_LipUpperOuterSkin1',
 'FACIAL_L_12IPV_LipUpperOuterSkin2',
 'FACIAL_R_12IPV_LipUpperOuterSkin2',
 'FACIAL_L_12IPV_MouthInteriorUpper1',
 'FACIAL_R_12IPV_MouthInteriorUpper1',
 'FACIAL_L_12IPV_MouthInteriorUpper2',
 'FACIAL_R_12IPV_MouthInteriorUpper2',
 'FACIAL_C_LipUpper1',
 'FACIAL_C_LipUpper2',
 'FACIAL_C_LipUpper3',
 'FACIAL_L_12IPV_LipUpper1',
 'FACIAL_R_12IPV_LipUpper1',
 'FACIAL_L_12IPV_LipUpper2',
 'FACIAL_R_12IPV_LipUpper2',
 'FACIAL_L_12IPV_LipUpper3',
 'FACIAL_R_12IPV_LipUpper3',
 'FACIAL_L_12IPV_LipUpper4',
 'FACIAL_R_12IPV_LipUpper4',
 'FACIAL_L_12IPV_LipUpper5',
 'FACIAL_R_12IPV_LipUpper5',
 'FACIAL_C_LipUpper',
 'FACIAL_L_LipUpper1',
 'FACIAL_L_LipUpper2',
 'FACIAL_L_LipUpper3',
 'FACIAL_L_12IPV_LipUpper6',
 'FACIAL_L_12IPV_LipUpper7',
 'FACIAL_L_12IPV_LipUpper8',
 'FACIAL_L_12IPV_LipUpper9',
 'FACIAL_L_12IPV_LipUpper10',
 'FACIAL_L_12IPV_LipUpper11',
 'FACIAL_L_12IPV_LipUpper12',
 'FACIAL_L_12IPV_LipUpper13',
 'FACIAL_L_12IPV_LipUpper14',
 'FACIAL_L_12IPV_LipUpper15',
 'FACIAL_L_LipUpper',
 'FACIAL_R_LipUpper1',
 'FACIAL_R_LipUpper2',
 'FACIAL_R_LipUpper3',
 'FACIAL_R_12IPV_LipUpper6',
 'FACIAL_R_12IPV_LipUpper7',
 'FACIAL_R_12IPV_LipUpper8',
 'FACIAL_R_12IPV_LipUpper9',
 'FACIAL_R_12IPV_LipUpper10',
 'FACIAL_R_12IPV_LipUpper11',
 'FACIAL_R_12IPV_LipUpper12',
 'FACIAL_R_12IPV_LipUpper13',
 'FACIAL_R_12IPV_LipUpper14',
 'FACIAL_R_12IPV_LipUpper15',
 'FACIAL_R_LipUpper',
 'FACIAL_L_LipUpperOuter1',
 'FACIAL_L_LipUpperOuter2',
 'FACIAL_L_LipUpperOuter3',
 'FACIAL_L_12IPV_LipUpper16',
 'FACIAL_L_12IPV_LipUpper17',
 'FACIAL_L_12IPV_LipUpper18',
 'FACIAL_L_12IPV_LipUpper19',
 'FACIAL_L_12IPV_LipUpper20',
 'FACIAL_L_12IPV_LipUpper21',
 'FACIAL_L_12IPV_LipUpper22',
 'FACIAL_L_12IPV_LipUpper23',
 'FACIAL_L_12IPV_LipUpper24',
 'FACIAL_L_LipUpperOuter',
 'FACIAL_R_LipUpperOuter1',
 'FACIAL_R_LipUpperOuter2',
 'FACIAL_R_LipUpperOuter3',
 'FACIAL_R_12IPV_LipUpper16',
 'FACIAL_R_12IPV_LipUpper17',
 'FACIAL_R_12IPV_LipUpper18',
 'FACIAL_R_12IPV_LipUpper19',
 'FACIAL_R_12IPV_LipUpper20',
 'FACIAL_R_12IPV_LipUpper21',
 'FACIAL_R_12IPV_LipUpper22',
 'FACIAL_R_12IPV_LipUpper23',
 'FACIAL_R_12IPV_LipUpper24',
 'FACIAL_R_LipUpperOuter',
 'FACIAL_L_LipCorner1',
 'FACIAL_L_LipCorner2',
 'FACIAL_L_LipCorner3',
 'FACIAL_L_12IPV_LipCorner1',
 'FACIAL_L_12IPV_LipCorner2',
 'FACIAL_L_12IPV_LipCorner3',
 'FACIAL_L_LipCorner',
 'FACIAL_R_LipCorner1',
 'FACIAL_R_LipCorner2',
 'FACIAL_R_LipCorner3',
 'FACIAL_R_12IPV_LipCorner1',
 'FACIAL_R_12IPV_LipCorner2',
 'FACIAL_R_12IPV_LipCorner3',
 'FACIAL_R_LipCorner',
 'FACIAL_C_MouthUpper',
 'FACIAL_L_JawBulge',
 'FACIAL_R_JawBulge',
 'FACIAL_L_JawRecess',
 'FACIAL_R_JawRecess',
 'FACIAL_L_Masseter',
 'FACIAL_R_Masseter',
 'FACIAL_C_UnderChin',
 'FACIAL_L_12IPV_UnderChin1',
 'FACIAL_R_12IPV_UnderChin1',
 'FACIAL_L_12IPV_UnderChin2',
 'FACIAL_R_12IPV_UnderChin2',
 'FACIAL_L_UnderChin',
 'FACIAL_R_UnderChin',
 'FACIAL_L_12IPV_UnderChin3',
 'FACIAL_R_12IPV_UnderChin3',
 'FACIAL_L_12IPV_UnderChin4',
 'FACIAL_R_12IPV_UnderChin4',
 'FACIAL_L_12IPV_UnderChin5',
 'FACIAL_R_12IPV_UnderChin5',
 'FACIAL_L_12IPV_UnderChin6',
 'FACIAL_R_12IPV_UnderChin6',
 'FACIAL_C_TeethUpper',
 'FACIAL_C_LipLowerSkin',
 'FACIAL_L_LipLowerSkin',
 'FACIAL_R_LipLowerSkin',
 'FACIAL_L_LipLowerOuterSkin',
 'FACIAL_R_LipLowerOuterSkin',
 'FACIAL_C_12IPV_LipLowerSkin1',
 'FACIAL_C_12IPV_LipLowerSkin2',
 'FACIAL_L_12IPV_LipLowerSkin',
 'FACIAL_R_12IPV_LipLowerSkin',
 'FACIAL_L_12IPV_LipLowerOuterSkin1',
 'FACIAL_R_12IPV_LipLowerOuterSkin1',
 'FACIAL_L_12IPV_LipLowerOuterSkin2',
 'FACIAL_R_12IPV_LipLowerOuterSkin2',
 'FACIAL_L_12IPV_LipLowerOuterSkin3',
 'FACIAL_R_12IPV_LipLowerOuterSkin3',
 'FACIAL_L_12IPV_MouthInteriorLower1',
 'FACIAL_R_12IPV_MouthInteriorLower1',
 'FACIAL_L_12IPV_MouthInteriorLower2',
 'FACIAL_R_12IPV_MouthInteriorLower2',
 'FACIAL_C_LipLower1',
 'FACIAL_C_LipLower2',
 'FACIAL_C_LipLower3',
 'FACIAL_L_12IPV_LipLower1',
 'FACIAL_R_12IPV_LipLower1',
 'FACIAL_L_12IPV_LipLower2',
 'FACIAL_R_12IPV_LipLower2',
 'FACIAL_L_12IPV_LipLower3',
 'FACIAL_R_12IPV_LipLower3',
 'FACIAL_L_12IPV_LipLower4',
 'FACIAL_R_12IPV_LipLower4',
 'FACIAL_L_12IPV_LipLower5',
 'FACIAL_R_12IPV_LipLower5',
 'FACIAL_C_LipLower',
 'FACIAL_L_LipLower1',
 'FACIAL_L_LipLower2',
 'FACIAL_L_LipLower3',
 'FACIAL_L_12IPV_LipLower6',
 'FACIAL_L_12IPV_LipLower7',
 'FACIAL_L_12IPV_LipLower8',
 'FACIAL_L_12IPV_LipLower9',
 'FACIAL_L_12IPV_LipLower10',
 'FACIAL_L_12IPV_LipLower11',
 'FACIAL_L_12IPV_LipLower12',
 'FACIAL_L_12IPV_LipLower13',
 'FACIAL_L_12IPV_LipLower14',
 'FACIAL_L_12IPV_LipLower15',
 'FACIAL_L_LipLower',
 'FACIAL_R_LipLower1',
 'FACIAL_R_LipLower2',
 'FACIAL_R_LipLower3',
 'FACIAL_R_12IPV_LipLower6',
 'FACIAL_R_12IPV_LipLower7',
 'FACIAL_R_12IPV_LipLower8',
 'FACIAL_R_12IPV_LipLower9',
 'FACIAL_R_12IPV_LipLower10',
 'FACIAL_R_12IPV_LipLower11',
 'FACIAL_R_12IPV_LipLower12',
 'FACIAL_R_12IPV_LipLower13',
 'FACIAL_R_12IPV_LipLower14',
 'FACIAL_R_12IPV_LipLower15',
 'FACIAL_R_LipLower',
 'FACIAL_L_LipLowerOuter1',
 'FACIAL_L_LipLowerOuter2',
 'FACIAL_L_LipLowerOuter3',
 'FACIAL_L_12IPV_LipLower16',
 'FACIAL_L_12IPV_LipLower17',
 'FACIAL_L_12IPV_LipLower18',
 'FACIAL_L_12IPV_LipLower19',
 'FACIAL_L_12IPV_LipLower20',
 'FACIAL_L_12IPV_LipLower21',
 'FACIAL_L_12IPV_LipLower22',
 'FACIAL_L_12IPV_LipLower23',
 'FACIAL_L_12IPV_LipLower24',
 'FACIAL_L_LipLowerOuter',
 'FACIAL_R_LipLowerOuter1',
 'FACIAL_R_LipLowerOuter2',
 'FACIAL_R_LipLowerOuter3',
 'FACIAL_R_12IPV_LipLower16',
 'FACIAL_R_12IPV_LipLower17',
 'FACIAL_R_12IPV_LipLower18',
 'FACIAL_R_12IPV_LipLower19',
 'FACIAL_R_12IPV_LipLower20',
 'FACIAL_R_12IPV_LipLower21',
 'FACIAL_R_12IPV_LipLower22',
 'FACIAL_R_12IPV_LipLower23',
 'FACIAL_R_12IPV_LipLower24',
 'FACIAL_R_LipLowerOuter',
 'FACIAL_C_MouthLower',
 'FACIAL_C_TongueUpper2',
 'FACIAL_L_TongueSide2',
 'FACIAL_R_TongueSide2',
 'FACIAL_C_TongueUpper3',
 'FACIAL_C_TongueLower3',
 'FACIAL_L_TongueSide3',
 'FACIAL_R_TongueSide3',
 'FACIAL_C_Tongue4',
 'FACIAL_C_Tongue3',
 'FACIAL_C_Tongue2',
 'FACIAL_C_Tongue1',
 'FACIAL_C_TeethLower',
 'FACIAL_C_LowerLipRotation',
 'FACIAL_C_Jawline',
 'FACIAL_L_12IPV_Jawline1',
 'FACIAL_R_12IPV_Jawline1',
 'FACIAL_L_12IPV_Jawline2',
 'FACIAL_R_12IPV_Jawline2',
 'FACIAL_L_Jawline1',
 'FACIAL_L_Jawline2',
 'FACIAL_L_12IPV_Jawline3',
 'FACIAL_L_12IPV_Jawline4',
 'FACIAL_L_12IPV_Jawline5',
 'FACIAL_L_12IPV_Jawline6',
 'FACIAL_L_Jawline',
 'FACIAL_R_Jawline1',
 'FACIAL_R_Jawline2',
 'FACIAL_R_12IPV_Jawline3',
 'FACIAL_R_12IPV_Jawline4',
 'FACIAL_R_12IPV_Jawline5',
 'FACIAL_R_12IPV_Jawline6',
 'FACIAL_R_Jawline',
 'FACIAL_L_ChinSide',
 'FACIAL_R_ChinSide',
 'FACIAL_L_12IPV_ChinS1',
 'FACIAL_R_12IPV_ChinS1',
 'FACIAL_L_12IPV_ChinS2',
 'FACIAL_R_12IPV_ChinS2',
 'FACIAL_L_12IPV_ChinS3',
 'FACIAL_R_12IPV_ChinS3',
 'FACIAL_L_12IPV_ChinS4',
 'FACIAL_R_12IPV_ChinS4',
 'FACIAL_C_Chin1',
 'FACIAL_L_Chin1',
 'FACIAL_R_Chin1',
 'FACIAL_C_Chin2',
 'FACIAL_L_Chin2',
 'FACIAL_R_Chin2',
 'FACIAL_C_Chin3',
 'FACIAL_L_Chin3',
 'FACIAL_R_Chin3',
 'FACIAL_L_12IPV_Chin1',
 'FACIAL_R_12IPV_Chin1',
 'FACIAL_L_12IPV_Chin2',
 'FACIAL_R_12IPV_Chin2',
 'FACIAL_C_12IPV_Chin3',
 'FACIAL_C_12IPV_Chin4',
 'FACIAL_L_12IPV_Chin5',
 'FACIAL_R_12IPV_Chin5',
 'FACIAL_L_12IPV_Chin6',
 'FACIAL_R_12IPV_Chin6',
 'FACIAL_L_12IPV_Chin7',
 'FACIAL_R_12IPV_Chin7',
 'FACIAL_L_12IPV_Chin8',
 'FACIAL_R_12IPV_Chin8',
 'FACIAL_L_12IPV_Chin9',
 'FACIAL_R_12IPV_Chin9',
 'FACIAL_L_12IPV_Chin10',
 'FACIAL_R_12IPV_Chin10',
 'FACIAL_L_12IPV_Chin11',
 'FACIAL_R_12IPV_Chin11',
 'FACIAL_L_12IPV_Chin12',
 'FACIAL_R_12IPV_Chin12',
 'FACIAL_L_12IPV_Chin13',
 'FACIAL_R_12IPV_Chin13',
 'FACIAL_L_12IPV_Chin14',
 'FACIAL_R_12IPV_Chin14',
 'FACIAL_C_Chin',
 'FACIAL_C_Jaw',
 'FACIAL_C_FacialRoot',
 'head',
 'neck_02']
        del_body_jnts = ["Neck1", "Neck2", "Neck3", "Head"]
        skinreplacejoints.replaceSkinJointsToOne(del_body_jnts, 'ChestMid',
                                                 moveWithJoints=False, unbindSource=False, skipSkinClusters=(), skin_name=skin_body)
        cmds.skinCluster(skin_body, e=1, dr=4, lw=1, wt=0, ai=meta_skin_jnts)
        cmds.refresh()

        head_layers = ng2.layers.init_layers(head_mdl_dup)
        head_layers_list = head_layers.list()
        layer_obj = next((l for l in head_layers_list if l.name == "Base Weights"), None)

        if not layer_obj:
            head_layers.add("Base Weights")

        layers = ng2.layers.init_layers(body_hi_dup)
        layers_list = layers.list()
        layer_body_obj = next((l for l in layers_list if l.name == "Base Body Weights"), None)

        if not layer_body_obj:
            layers.add("Base Body Weights")

        config = InfluenceMappingConfig()
        config.use_distance_matching = True
        config.use_name_matching = True
        config.use_label_matching = True
        config.distance_threshold = True
        config.use_dg_link_matching = True

        ngst_api.transfer_layers(head_mdl_dup, body_hi_dup, vertex_transfer_mode=VertexTransferMode.vertexId, influences_mapping_config=config)

        top_layer = layers.list()[-1]
        influences_info = layers.list_influences()
        fit_index = 0
        for info in influences_info:
            if info.path_name().split('|')[-1] == "ChestMid":
                fit_index = info.logicalIndex
        top_layer.set_weights(fit_index, np.zeros(len(verts), dtype=np.float32).tolist())

        skin.del_ngSkinNode()

        end_time = time.time()
        print("//Spend {} seconds.".format(end_time - start_time))

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.compactWidget.loadBodyBtn.clicked.connect(partial(self.load, self.compactWidget.loadBodyLe))
        self.compactWidget.loadHeadBtn.clicked.connect(partial(self.load, self.compactWidget.loadHeadLe))
        self.compactWidget.applyButton.clicked.connect(self.apply)


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
        self.loadBodyBtn = elements.styledButton(text="Load Body Rig Mesh")
        self.loadBodyLe = elements.LineEdit()
        self.loadHeadBtn = elements.styledButton(text="Load Head Rig Mesh")
        self.loadHeadLe = elements.LineEdit()
        self.applyButton = elements.styledButton(text="Apply")


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
                                         spacing=5)
        loadBodyLay = elements.hBoxLayout()
        loadBodyLay.addWidget(self.loadBodyBtn)
        loadBodyLay.addWidget(self.loadBodyLe)
        mainLayout.addLayout(loadBodyLay)

        loadHeadLay = elements.hBoxLayout()
        loadHeadLay.addWidget(self.loadHeadBtn)
        loadHeadLay.addWidget(self.loadHeadLe)
        mainLayout.addLayout(loadHeadLay)
        mainLayout.addWidget(self.applyButton)
        # mainLayout.addWidget(self.parameterCollapsable)
        mainLayout.addStretch()


if __name__ == '__main__':
    selection = cmds.ls(selection=True)
    source = selection[0]
    target = selection[1]
    target_bs_list = blendshape.getBlendshapeNodes(target)
    if target_bs_list:
        target_bs = target_bs_list[0]
        cmds.blendShape(source, edit=True, tc=False,
                        target=(target, len(cmds.aliasAttr(target_bs, q=1)) + 1,
                                target, 0.0))
    else:
        cmds.blendShape(source, target, frontOfChain=True, name="{}_blendShape".format(target))

