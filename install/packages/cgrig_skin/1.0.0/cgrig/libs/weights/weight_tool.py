# -*- coding: utf-8 -*-
# coding:utf-8
import json
import re
import stat
import os
from maya.api.OpenMaya import *
from .api_lib import weight_tool_api
from .common import *


def _copy_weight(src, dst):
    if not is_shape(src, Shape.mesh):
        return
    if not is_shape(dst, Shape.mesh):
        return
    skin_cluster = get_skin_cluster(src)
    if not skin_cluster:
        return cmds.warning(u"please select two skin polygon")
    if get_skin_cluster(dst):
        return cmds.CopySkinWeights()
    joints = cmds.skinCluster(skin_cluster, q=1, influence=1)
    cmds.skinCluster(joints, dst, tsb=1)
    cmds.select(src, dst)
    cmds.CopySkinWeights()


def get_short_long_polygons(group_name):
    polygons = set()
    for mesh in cmds.ls(cmds.listRelatives(group_name, ad=1, f=1), type="mesh"):
        polygons.update(cmds.listRelatives(mesh, p=1, f=1))
    short_long_name = dict()
    for long_name in polygons:
        short_name = long_name.split("|")[-1]
        short_long_name[short_name] = long_name
    return short_long_name


def copy_weights():
    selected = cmds.ls(sl=1, o=1)
    count = len(selected)
    if count < 2:
        return
    elif count == 2:
        src, dst = selected
        _copy_weight(src, dst)
        src_map = get_short_long_polygons(src)
        dst_map = get_short_long_polygons(dst)
        for src_key, src_value in src_map.items():
            dst_value = dst_map.get(src_key)
            if dst_value is None:
                continue
            _copy_weight(src_value, dst_value)
    elif len(selected) > 2:
        src = selected[0]
        for dst in selected[1:]:
            _copy_weight(src, dst)


def copy_unlock_skin_polygon():
    polygon = get_selected_geometry(Shape.mesh)
    sk = get_skin_cluster(polygon)
    influences = cmds.skinCluster(sk, q=1, influence=1)
    joints = [joint for joint in influences if not cmds.getAttr(joint+'.liw')]
    dup_polygon = cmds.duplicate(polygon)[0]
    new_name = "_".join([joint.split("|")[-1].split(":")[-1] for joint in joints[:3]])
    dup_polygon = cmds.rename(dup_polygon, new_name)
    cmds.skinCluster(joints, dup_polygon, mi=1, tsb=1)
    cmds.select(polygon, dup_polygon)
    cmds.CopySkinWeights()
    cmds.select(dup_polygon)


def get_logical_index(attr):
    str_i = attr.split("[")[-1].split("]")[0]
    if str_i.isdigit():
        return int(str_i)
    else:
        return str_i


def re_skin():
    polygons = get_selected_geometries(Shape.mesh)
    skin_cluster_list = [sk for sk in map(get_skin_cluster, polygons) if sk]
    for sk in skin_cluster_list:
        attrs = cmds.listConnections(sk+'.matrix', s=1, d=0, c=1,  p=1, type="joint")
        for i in range(0, len(attrs), 2):
            src, dst = attrs[i+1], attrs[i]
            index = get_logical_index(dst)
            joint = src.split(".")[0]
            matrix = cmds.xform(joint, q=1, ws=1, m=1)
            inverse = list(MMatrix(matrix).inverse())
            cmds.setAttr("{sk}.bindPreMatrix[{index}]".format(**locals()), inverse, type="matrix")
    joints = cmds.ls(sl=1, type="joint")
    for joint in joints:
        matrix = cmds.xform(joint, q=1, ws=1, m=1)
        inverse = list(MMatrix(matrix).inverse())
        for attr in cmds.listConnections(joint+'.worldMatrix[0]', s=0, d=1, type="skinCluster", p=1):
            index = get_logical_index(attr)
            sk = attr.split(".")[0]
            cmds.setAttr("{sk}.bindPreMatrix[{index}]".format(**locals()), inverse, type="matrix")


def create_vx():
    for joint in cmds.ls(sl=1, type="joint"):
        loc = cmds.spaceLocator(n=joint+"LushBezierVX")
        cmds.xform(loc, ws=1, m=cmds.xform(joint, q=1, m=1, ws=1))


def create_y_vx():
    selected_joints = cmds.ls(selection=True, type='joint')
    if not selected_joints:
        cmds.warning('No joints selected.')
        return
    for joint in selected_joints:
        loc_name = joint + 'LushBezierVX'
        loc = cmds.spaceLocator(name=loc_name)[0]
        cmds.parent(loc, joint)
        cmds.setAttr(loc + '.translate', 0, 0, 0)
        cmds.setAttr(loc + '.rotate', 0, 0, 90)
        cmds.parent(loc, w=1)


def create_z_vx():
    selected_joints = cmds.ls(selection=True, type='joint')
    if not selected_joints:
        cmds.warning('No joints selected.')
        return
    for joint in selected_joints:
        loc_name = joint + 'LushBezierVX'
        loc = cmds.spaceLocator(name=loc_name)[0]
        cmds.parent(loc, joint)
        cmds.setAttr(loc + '.translate', 0, 0, 0)
        cmds.setAttr(loc + '.rotate', 0, -90, 0)
        cmds.parent(loc, w=1)


def paint_eye():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if not unlock_joints:
        return
    joint_points = [convert_p(cmds.xform(joint, q=1, t=1, ws=1)) for joint in unlock_joints]
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    weight_tool_api.paint_eye(polygon, sk, indices, joint_points)


def get_json_kwargs(fun):
    path = os.path.abspath("%s/../data/kwargs/%s.json" % (__file__, fun.__name__)).replace("\\", "/")
    if os.path.isfile(path):
        with open(path, "r") as fp:
            return json.load(fp)
    return dict()


def cache_kwargs(fun):
    def new_fun(**kwargs):
        if len(kwargs.keys()) == 0:
            fun(**get_json_kwargs(fun))
        else:
            path = os.path.abspath("%s/../data/kwargs/%s.json" % (__file__, fun.__name__)).replace("\\", "/")
            dir_path = os.path.dirname(path)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            if os.path.isfile(path):
                os.chmod(path, stat.S_IWRITE)
            with open(path, "w") as fp:
                json.dump(kwargs, fp)
            fun(**kwargs)
    new_fun.__name__ = fun.__name__
    return new_fun


@cache_kwargs
def limit_max_influence(max_influence=4):
    polygon = get_selected_geometry(Shape.mesh)
    sk = get_skin_cluster(polygon)
    indexes = list(range(len(cmds.skinCluster(sk, q=1, influence=1))))
    weight_tool_api.limit_max_influence(polygon, sk, indexes, max_influence)


def selected_vertices():
    vertices = "".join(cmds.ls(sl=1, fl=11))
    vertices = re.findall("\.vtx\[(\d+)\]", vertices)
    vertices = list(set(map(int, vertices)))
    return vertices


@cache_kwargs
def lock_influence_smooth(smooth_count=1, smooth_step=0.2):
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if sk is None:
        return
    vtx_ids = selected_vertices()
    indexes = list(range(len(cmds.skinCluster(sk, q=1, influence=1))))
    if not len(vtx_ids):
        return
    weight_tool_api.lock_influence_smooth(polygon, sk, indexes, vtx_ids, smooth_step, smooth_count)


def copy_joint_weight():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if not unlock_joints:
        return
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    joint_names = [unlock_joint for unlock_joint in unlock_joints]
    weight_tool_api.copy_joint_weight(polygon, sk, indices, joint_names)


def paste_joint_weight():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if not unlock_joints:
        return
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    joint_names = [unlock_joint for unlock_joint in unlock_joints]
    weight_tool_api.paste_joint_weight(polygon, sk, indices, joint_names)




