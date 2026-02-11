# coding=utf-8

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


def api_ls(*names):
    selection_list = MSelectionList()
    for name in names:
        selection_list.add(name)
    return selection_list


def get_skin_cluster(polygon_name):
    if not is_shape(polygon_name, "mesh"):
        return
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    for skin_cluster in cmds.ls(cmds.listHistory(polygon_name), type="skinCluster"):
        for shape in cmds.skinCluster(skin_cluster, q=1, geometry=1):
            for long_shape in cmds.ls(shape, l=1):
                if long_shape in shapes:
                    return skin_cluster


def get_weights_args(polygon_name):
    shape, components = api_ls(polygon_name + ".vtx[*]").getComponent(0)
    fn_skin = MFnSkinCluster(api_ls(get_skin_cluster(polygon_name)).getDependNode(0))
    influences = MIntArray(range(len(fn_skin.influenceObjects())))
    return fn_skin, shape, components, influences


def get_weights(polygon_name):
    fn_skin, shape, components, influences = get_weights_args(polygon_name)
    return list(fn_skin.getWeights(shape, components, influences))


def set_weights(polygon_name, weights):
    cmds.dgdirty(get_skin_cluster(polygon_name))
    fn_skin, shape, components, influences = get_weights_args(polygon_name)
    fn_skin.setWeights(shape, components, influences, MDoubleArray(weights))
    cmds.dgdirty(get_skin_cluster(polygon_name))


def get_skin_joints(polygon_name):
    sk = get_skin_cluster(polygon_name)
    return cmds.skinCluster(sk, q=1, influence=1)


def get_vv_data(mit_vtx):
    data = {}
    vtx = mit_vtx
    for i in range(mit_vtx.count()):
        vtx.setIndex(i)
        links = list(vtx.getConnectedVertices())
        count = len(links)
        data.setdefault(count, dict(ids=[], links=[]))
        data[count]["ids"].append(i)
        data[count]["links"].append(links)
    return data


def get_polygon_vv_data(polygon_name):
    return get_vv_data(MItMeshVertex(api_ls(polygon_name).getDagPath(0)))


def get_near_vtx_ids(polygon_name, points):
    fn_mesh = MFnMesh(api_ls(polygon_name).getDagPath(0))
    vtx_ids = []
    for point in points:
        p = MPoint(point)
        p, f = fn_mesh.getClosestPoint(p, MSpace.kWorld)
        ids = fn_mesh.getPolygonVertices(f)
        ids = sorted(ids, key=lambda x: MVector(fn_mesh.getPoint(x, MSpace.kWorld)-p).length())
        vtx_ids.append(ids[0])
    return vtx_ids


def get_tri_mesh_data(polygon):
    temp_polygon = cmds.duplicate(polygon)[0]
    cmds.polyTriangulate(temp_polygon)
    fn_mesh = MFnMesh(api_ls(temp_polygon).getDagPath(0))
    points = fn_mesh.getPoints(MSpace.kWorld)
    points = [list(p) for p in points]
    faces = []
    for f in MItMeshPolygon(fn_mesh.dagPath()):
        faces.append(list(f.getVertices()))
    cmds.delete(temp_polygon)
    return points, faces


def get_polygon_data(polygon):
    sk = get_skin_cluster(polygon)
    joints = cmds.skinCluster(sk, q=1, inf=1)
    indexes = [i for i, joint in enumerate(joints) if not cmds.getAttr(joint+".liw")]
    points = [cmds.xform(joints[i], q=1, ws=1, t=1) for i in indexes]
    ids = get_near_vtx_ids(polygon, points)
    points, faces = get_tri_mesh_data(polygon)
    vv = get_polygon_vv_data(polygon)
    weights = get_weights(polygon)
    return dict(
        polygon=polygon,
        points=points,
        faces=faces,
        vv=vv,
        weights=weights,
        indexes=indexes,
        ids=ids
    )


def get_distance_data(polygon):
    sk = get_skin_cluster(polygon)
    joints = cmds.skinCluster(sk, q=1, inf=1)
    indexes = [i for i, joint in enumerate(joints) if not cmds.getAttr(joint+".liw")]
    vtx_points = MFnMesh(api_ls(polygon).getDagPath(0)).getPoints(MSpace.kWorld)
    vtx_points = [list(p) for p in vtx_points]
    joint_points = [cmds.xform(joints[i], q=1, ws=1, t=1) for i in indexes]
    vv = get_polygon_vv_data(polygon)
    weights = get_weights(polygon)
    return dict(
        vtx_points=vtx_points,
        joint_points=joint_points,
        vv=vv,
        weights=weights,
        indexes=indexes,
    )