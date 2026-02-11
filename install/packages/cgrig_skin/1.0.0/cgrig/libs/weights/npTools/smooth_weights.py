# coding=utf-8
try:
    import numpy as np
except ImportError:
    np = None

from maya.api.OpenMaya import *
from maya.api.OpenMayaAnim import *
from maya import cmds


def is_shape(polygon_name, typ="mesh"):
    # 判断物体是否存在
    if not cmds.objExists(polygon_name):
        return False
    # 判断类型是否为transform
    if cmds.objectType(polygon_name) != "transform":
        return False
    # 判断是否有形节点
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    if not shapes:
        return False
    # 判断形节点类型是否时typ
    if cmds.objectType(shapes[0]) != typ:
        return False
    return True


def get_skin_cluster(polygon_name):
    if not is_shape(polygon_name, "mesh"):
        return
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    for skin_cluster in cmds.ls(cmds.listHistory(polygon_name), type="skinCluster"):
        for shape in cmds.skinCluster(skin_cluster, q=1, geometry=1):
            for long_shape in cmds.ls(shape, l=1):
                if long_shape in shapes:
                    return skin_cluster


def api_ls(*names):
    selection_list = MSelectionList()
    for name in names:
        selection_list.add(name)
    return selection_list


def get_weights_args(polygon_name):
    shape, components = api_ls(polygon_name + ".vtx[*]").getComponent(0)
    fn_skin = MFnSkinCluster(api_ls(get_skin_cluster(polygon_name)).getDependNode(0))
    influences = MIntArray(range(len(fn_skin.influenceObjects())))
    return fn_skin, shape, components, influences


def get_weights(polygon_name):
    fn_skin, shape, components, influences = get_weights_args(polygon_name)
    return fn_skin.getWeights(shape, components, influences)


def set_weights(polygon_name, weights):
    cmds.dgdirty(get_skin_cluster(polygon_name))
    fn_skin, shape, components, influences = get_weights_args(polygon_name)
    fn_skin.setWeights(shape, components, influences, MDoubleArray(weights))


def get_orig(polygon_name, clear=False):
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    if shapes is None:
        return
    shapes = [shape for shape in shapes if cmds.getAttr(shape+'.io')]
    shapes.sort(key=lambda x: len(set(cmds.listConnections(x, s=0, d=1))))
    if clear:
        cmds.delete(shapes[1:])
    return shapes[0]


def get_vv_data():
    sel = MGlobal.getActiveSelectionList()
    assert isinstance(sel, MSelectionList)
    path, component = sel.getComponent(0)
    if component.apiTypeStr == "kMeshVertComponent":
        mit_vtx = MItMeshVertex(path, component)
        path.pop()
    else:
        mit_vtx = MItMeshVertex(path)
    data = {}
    for vtx in mit_vtx:
        links = list(vtx.getConnectedVertices())
        count = len(links)
        data.setdefault(count, dict(ids=[], links=[]))
        data[count]["ids"].append(vtx.index())
        data[count]["links"].append(links)
    polygon = path.fullPathName()
    return polygon, data


def normal_weights(weights):
    max_weights = np.sum(weights, axis=1)
    max_weights[max_weights < 0.0001] = 1
    weights = weights / max_weights[:, None]
    return weights


def solve_link_power(points, ids, links):
    link_points = points[links]
    vtx_points = points[ids]
    distance_matrix = np.linalg.norm(link_points[:, :, None, :] - link_points[:, None, :, :], axis=3)
    distance_inv = np.linalg.inv(distance_matrix)
    vtx_distance = np.linalg.norm(vtx_points[:, None] - link_points, axis=2)
    rbf_weights = np.sum(vtx_distance[:, None] * distance_inv, axis=2)
    rbf_weights[rbf_weights < 0] = 0
    rbf_weights = normal_weights(rbf_weights)
    soft_max_weights = normal_weights(np.exp(-vtx_distance))
    return rbf_weights*0.8+soft_max_weights*0.2


def smooth_current_weights(smooth_weights, weights, ids, links, power):
    smooth_weights[ids] = np.sum(weights[links]*power[:, :, None], axis=1)


def smooth_iter_weights(weights, count, step, data):
    for i in range(count):
        smooth_weights = weights.copy()
        for row in data.values():
            smooth_current_weights(smooth_weights, weights, **row)
        weights = weights*(1-step) + smooth_weights*step
    return weights


def smooth_selected(count=2, step=0.3):
    polygon, data = get_vv_data()
    points = np.array(MFnMesh(api_ls(get_orig(polygon)).getDagPath(0)).getPoints())[:, :3]
    for row in data.values():
        row["power"] = solve_link_power(points, **row)
    weights = np.array(get_weights(polygon))
    vtx_count = points.shape[0]
    joint_count = weights.shape[0]//vtx_count
    weights = weights.reshape(vtx_count, joint_count)
    weights = smooth_iter_weights(weights, count, step, data)
    set_weights(polygon, weights.reshape(vtx_count*joint_count).tolist())


def smooth_weights_by_polygon(polygon, weights, count, step):
    cmds.select(polygon)
    polygon, data = get_vv_data()
    points = np.array(MFnMesh(api_ls(get_orig(polygon)).getDagPath(0)).getPoints())[:, :3]
    for row in data.values():
        row["power"] = solve_link_power(points, **row)
    weights = smooth_iter_weights(weights, count, step, data)
    return weights


def doit():
    smooth_selected()

