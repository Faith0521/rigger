#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/2/10 18:24
# @Author : yinyufei
# @File : core.py
# @Project : TeamCode
import json
from typing import *
from cgrig.libs.protocol import node_types, shape_types, NodeProtocol, find_node_type, ShapeProtocol


_node_list = []  # type: List[NodeProtocol]
_node_to_shape = {}  # type: Dict[NodeProtocol, List[ShapeProtocol]]

IkuraPoseSetName = "FixShapeSet"


def save_all_data():
    import maya.cmds as cmds
    pose_data_list = [[i.type_name, i.dump()] for i in _node_list]
    shape_data_dict = {
        str(_node_list.index(pose)): [[shape.type_name, shape.dump()] for shape in shape_list]
        for pose, shape_list in _node_to_shape.items()
    }
    all_data = {
        'pose_list': pose_data_list,
        'pose_to_shape': shape_data_dict
    }

    cmds.select(clear=True)
    if not cmds.objExists(IkuraPoseSetName):
        cmds.sets(name=IkuraPoseSetName)
    if not cmds.objExists(IkuraPoseSetName + '.IkuraShapeData'):
        cmds.addAttr(IkuraPoseSetName, ln='FixShapeData', dt='string')
    cmds.setAttr(IkuraPoseSetName + '.FixShapeData', json.dumps(all_data), type='string')


def add_node(pose_type_name):
    # type: (str) -> NodeProtocol
    node_type = find_node_type(pose_type_name)
    node = node_type.create()
    _node_list.append(node)
    save_all_data()
    return node

