# coding=utf-8
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


def get_selected_geometries(typ):
    shapes = cmds.ls(sl=1, o=1, type=typ)
    polygons = [cmds.listRelatives(shape, p=1)[0] for shape in shapes]
    polygons += cmds.ls(sl=1, o=1, type="transform")
    return list(filter(lambda x: is_shape(x, typ), polygons))


def get_selected_geometry(typ):
    for geo in get_selected_geometries(typ):
        return geo


def get_selected_object_matrix():
    # 获取所有选择物体的子物体
    return [[top] + list(reversed(cmds.listRelatives(top, ad=1, f=1))) for top in cmds.ls(sl=1, o=1, l=1)]


def get_skin_cluster(polygon_name):
    if not is_shape(polygon_name, "mesh"):
        return
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    for skin_cluster in cmds.ls(cmds.listHistory(polygon_name), type="skinCluster"):
        for shape in cmds.skinCluster(skin_cluster, q=1, geometry=1):
            for long_shape in cmds.ls(shape, l=1):
                if long_shape in shapes:
                    return skin_cluster


class Shape(object):
    mesh = "mesh"
    nurbsSurface = "nurbsSurface"
    nurbsCurve = "nurbsCurve"


def get_orig(polygon_name, clear=False):
    shapes = cmds.listRelatives(polygon_name, s=1, f=1)
    if shapes is None:
        return
    shapes = [shape for shape in shapes if cmds.getAttr(shape+'.io')]
    shapes.sort(key=lambda x: len(set(cmds.listConnections(x, s=0, d=1))))
    if clear:
        cmds.delete(shapes[1:])
    return shapes[0]


def get_short_name(name):
    return name.split(":")[-1].split("|")[-1]


def convert_p(p):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(cmds.currentUnit(q=1, l=1))
    return [p[i]*unit for i in range(3)]


def get_paint_joint(sk):
    if sk is None:
        return
    paint_joints = [joint for joint in cmds.listConnections(sk+'.paintTrans', s=1, d=0, )
                    if cmds.nodeType(joint) == "joint"]
    if len(paint_joints) != 1:
        return cmds.warning("\nyou need a paint joint")
    return paint_joints[0]


def default_init_var():
    polygon = get_selected_geometry(Shape.mesh)
    sk = get_skin_cluster(polygon)
    if sk is None:
        return polygon, sk, None, None, None
    paint_joint = get_paint_joint(sk)
    joints = cmds.skinCluster(sk, q=1, influence=1)
    unlock_joints = [joint for joint in joints if cmds.nodeType(joint) == "joint" and not cmds.getAttr(joint+'.liw')]
    return polygon, sk, joints, unlock_joints, paint_joint
