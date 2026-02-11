# coding=utf-8
'''
Created on: 2023-12-31
Description: 这个插件是为了利用ngSkinTools为骨骼添加一个遮罩层,硬化一端的权重,这个插件解决的痛点是常规流程下
使用加减笔刷会破坏区域内多个骨骼之间的过渡关系,借助于ngSkinTools对层级内过渡关系的保护和自动分配,这样就可以专注于绘制一个方向的衰减.
'''
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.mel as mel
import ngSkinTools2.api as ng2
import numpy as np

from collections import OrderedDict
import sys

from Faith.tools.small_tools import jointHierarchy
from concurrent.futures import ThreadPoolExecutor


def check_ngSkinTools2_plugin():
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


def del_ngSkinNode():
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


def filter_objects():
    # 获取当前选择的所有物体
    selected_objects = cmds.ls(selection=True)

    # 初始化变量
    joints = []
    mesh_objects = []

    # 筛选骨骼和网格物体
    for obj in selected_objects:
        if cmds.objectType(obj) == 'joint':
            joints.append(obj)
        elif cmds.objectType(obj) == 'transform':
            # 对于 transform 类型，检查其子物体是否为 mesh 类型
            meshes = cmds.listRelatives(obj, shapes=True, type='mesh')
            if meshes:
                mesh_objects.append(obj)
    return joints, mesh_objects


def get_all_nodes_in_hierarchy(parent_node):
    # 获取直接子节点
    children = cmds.listRelatives(parent_node, children=True, fullPath=True) or []
    # 递归获取所有子节点
    all_nodes = []
    for child in children:
        all_nodes.append(child)
        all_nodes.extend(get_all_nodes_in_hierarchy(child))
    return all_nodes


# 比较复杂的情况下,Ng的层级权重效果和Maya默认权重效果之间并不能进行完美的转换,在使用此脚本过程中请保持谨慎.
class SkinLayer:
    def __init__(self, mesh_short):
        self.mesh_short = mesh_short
        # API创建选择列表容器,把物体短名放进容器
        selection_list = OpenMaya.MSelectionList()
        selection_list.add(self.mesh_short)

        # 根据短名确定场景根部到物体的路径
        dag_path = selection_list.getDagPath(0)
        self.mesh = OpenMaya.MFnMesh(dag_path)

        # 获取物体长名
        self.mesh_long = self.mesh.fullPathName()
        # 获取物体点的数量
        self.mesh_numVertices = self.mesh.numVertices

        self.maskSkinInfo = dict()
        self.skinInfluencesInfo = dict()

        # del_ngSkinNode()
        # self.clear()

        self.base_layer = None
        self.init_base_layer()

    @property
    def layers(self):
        # ngSkin节点中所有关于层的数据
        layers = ng2.layers.init_layers(self.mesh_long)
        return layers

    def clear(self):
        self.layers.clear()

        # 从 self.layers.list() 中定位 Base weights 这个层的数据更新到变量 self.base_layer

    def init_base_layer(self):
        ls_base_layers = [layer for layer in self.layers.list() if layer.name == 'Base weights']
        if not ls_base_layers:
            self.base_layer = self.layers.add("Base weights")
        else:
            self.base_layer = ls_base_layers[0]
        self.base_layer.set_weights('mask', [1.000] * self.mesh.numVertices)
        return

    @property
    def base_layer_info(self):
        # 使用缓存
        if hasattr(self, '_cached_base_layer_influences_od'):
            return self._cached_base_layer_influences_od

        influences_info = self.layers.list_influences()

        # 预提取路径和索引
        paths = [inf.path for inf in influences_info]
        indices = [inf.logicalIndex for inf in influences_info]

        # 并行获取权重
        with ThreadPoolExecutor(max_workers=4) as executor:
            weights = list(executor.map(self.base_layer.get_weights, indices))

        # 使用生成器表达式创建字典
        self._cached_base_layer_influences_od = OrderedDict(
            sorted(
                ((path, [idx, weight]) for path, idx, weight in zip(paths, indices, weights)),
                key=lambda x: len(x[0])
            )
        )
        return self._cached_base_layer_influences_od

    @property
    def influences_names(self):
        base_layer_info = self.base_layer_info
        influences_short_names = base_layer_info.keys()
        influences_long_names = [cmds.ls(short_name, long=True)[0] for short_name in influences_short_names]

        if cmds.objExists(jointHierarchy.Group):
            nodes = get_all_nodes_in_hierarchy(jointHierarchy.Group)
            nodes = [node.split('|')[-1] for node in nodes]
            nodes = [node.replace('__', '|') for node in nodes]
            influences_long_names = nodes
            influences_short_names = [node.split('|')[-1] for node in nodes]
        return (influences_short_names, influences_long_names)

    # 找到目标骨骼的上一级蒙皮骨骼(未必是父物体,所以要写一个逻辑筛选)
    def find_matching_bone(self, long_name, influences_long_names):
        max_pipe_count = -1
        matching_bone = None
        for inf_name in influences_long_names:
            if inf_name in long_name and inf_name != long_name:
                pipe_count = inf_name.count('|')
                if pipe_count > max_pipe_count:
                    max_pipe_count = pipe_count
                    matching_bone = inf_name
        return matching_bone

        # 获取支链根关节

    def get_fit_inf(self, fit_jnt):
        fit_inf = None
        fit_index = None
        fit_weights = None
        for long in self.base_layer_info.keys():
            if long == cmds.ls(fit_jnt, long=True)[0]:
                fit_inf = long
                fit_index, fit_weights = self.base_layer_info[fit_inf]
        return (fit_inf, fit_index)

        # 获取骨架末端关节

    def get_last_inf(self, fit_jnt):
        fit_inf = self.get_fit_inf(fit_jnt)[0]
        long = cmds.ls(fit_jnt, long=True)[0]
        last_inf = self.find_matching_bone(long, self.influences_names[1])
        if cmds.objExists(jointHierarchy.Group):
            index = self.influences_names[1].index(fit_inf)
            last_inf = self.influences_names[1][index - 1]
        last_index = None
        if last_inf in self.base_layer_info.keys():
            last_index, _ = self.base_layer_info[last_inf]
        return (last_inf, last_index)

    def get_fit_chain(self, fit_jnt):
        chain = list()
        fit_inf = self.get_fit_inf(fit_jnt)[0]
        if cmds.objExists(jointHierarchy.Group):
            fit_inf = fit_inf.replace('|', '__')
            nodes = get_all_nodes_in_hierarchy(fit_inf)
            for long in nodes:
                if fit_inf in long:
                    chain.append(long.split('|')[-1].replace('__', '|'))
        else:
            chain = get_all_nodes_in_hierarchy(fit_inf)
        chain = [node for node in chain if node in self.base_layer_info.keys()]
        return chain

    def build(self, fit_jnt):
        cmds.undoInfo(stateWithoutFlush=True)
        cmds.undoInfo(openChunk=True)
        fit_inf, fit_index = self.get_fit_inf(fit_jnt)
        if fit_inf == None:
            OpenMaya.MGlobal.displayWarning("{} is not a influence.".format(fit_jnt))
            return

        last_inf, last_index = self.get_last_inf(fit_jnt)


        base_info = self.base_layer_info

        # 检查并创建必要的图层
        bottom_weights_layers = [layer for layer in self.layers.list() if layer.name == 'Trunk weights']

        if not bottom_weights_layers:
            if not last_inf:
                # 创建Trunk weights层
                bottom_layer = self.layers.add('Trunk weights')
                bottom_layer.set_weights('mask', np.ones(self.mesh.numVertices, dtype=np.float32).tolist())
            else:
                # 创建两个新图层
                bottom_layer = self.layers.add('Trunk weights')
                bottom_layer.set_weights('mask', np.ones(self.mesh.numVertices, dtype=np.float32).tolist())

                paint_layer = self.layers.add(fit_jnt)

                inf_index, inf_weights = base_info[fit_inf]
                weights_arr = np.array(inf_weights, dtype=np.float32)
                fit_weights = np.round(weights_arr, 6)

                paint_layer.set_weights(fit_index, np.ones(self.mesh.numVertices, dtype=np.float32).tolist())
                paint_layer.set_weights('mask', np.clip(fit_weights, 0, 1).tolist())
        else:
            layers = self.layers.list()
            last_layer = layers[-1]
            if last_layer.name == fit_jnt:
                return

            paint_layer = self.layers.add(fit_jnt)

            inf_index, inf_weights = base_info[fit_inf]
            weights_arr = np.array(inf_weights, dtype=np.float32)
            fit_weights = np.round(weights_arr, 6)

            paint_layer.set_weights(fit_index, np.ones(self.mesh.numVertices, dtype=np.float32).tolist())
            paint_layer.set_weights('mask', np.clip(fit_weights, 0, 1).tolist())

        cmds.undoInfo(closeChunk=True)

        try:
            exec("import ngSkinTools2; ngSkinTools2.open_ui()")
        except:
            pass
        finally:
            cmds.select(cl=True)
            mel.eval(u'print "// Result: Layer data has been created!    (蒙皮模型 - {} | 目标绘制关节 - {})"'.format(self.mesh_short, fit_jnt))
