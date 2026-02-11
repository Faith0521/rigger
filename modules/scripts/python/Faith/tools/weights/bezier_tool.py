# coding:utf-8
import functools
from maya.api.OpenMaya import *
from .common import *
from .api_lib import bezier_api


def convert_p(p):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(cmds.currentUnit(q=1, l=1))
    return [p[i]*unit for i in range(3)]


def convert_length(l):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(cmds.currentUnit(q=1, l=1))
    return l*unit


def convert_y(y):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(cmds.currentUnit(q=1, l=1))
    return y/unit


def ik_x(v, p):
    u"""
    :param v: 向量
    :param p: 点坐标
    :return: 点p在向量v轴上的坐标值。或理解为点p到向量v所在直线的最近点与远点的距离
    """
    return sum(v[i] * p[i] for i in range(3)) / sum(v[i] ** 2 for i in range(3))


def vp_to_vx(v, p):
    return [v[0], v[1], v[2], ik_x(v, p)]


def ik_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if len(unlock_joints) == 0 or paint_joint is None:
        return
    vx = spine_vx(unlock_joints[0], paint_joint)
    bezier_api.ik_init(polygon, sk, vx)
    return True


def soft_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if sk is None:
        return
    cmds.softSelect(sse=1)
    cmds.softSelect(ssc="0,1,1,1,0,1")
    radius = cmds.softSelect(q=1, ssd=1)
    cmds.softSelect(ssd=radius * 2)
    up_cmd = "move -r -os -wd 0 %.6f 0 ;" % convert_y(1)
    dn_cmd = "move -r -os -wd 0 %.6f 0 ;" % -convert_y(1)
    bezier_api.soft_init(polygon, sk, up_cmd, dn_cmd)
    cmds.softSelect(ssd=radius)
    # sk.ptw.get(cmds.getAttr(sk+'.ptw'))
    cmds.dgdirty(sk)
    cmds.refresh()
    return True


def ik_solve(xs, ys, r):
    r = cmds.softSelect(q=1, ssd=1) * r * 2
    bezier_api.solve("ik", xs, ys, r)


def soft_solve(xs, ys, r):
    ys = [1 - y for y in ys]
    bezier_api.solve("soft", xs, ys, r)


def locator_vx(fun):
    def _fun(joint1, joint2):
        vx_nodes = cmds.ls(joint2+"LushBezierVX", type="transform")
        if len(vx_nodes) == 1:
            vx_node = vx_nodes[0]
            p = convert_p(cmds.xform(joint2, q=1, ws=1, t=1))
            v = cmds.xform(vx_node, q=1, m=1, ws=1)[:3]
            return vp_to_vx(v, p)
        else:
            return fun(joint1, joint2)
    return _fun


@locator_vx
def spine_vx(joint1, joint2):
    v1 = cmds.xform(joint1, q=1, m=1, ws=1)[:3]
    v2 = cmds.xform(joint2, q=1, m=1, ws=1)[:3]
    v = [(e1+e2)/2 for e1, e2 in zip(v1, v2)]
    p = convert_p(cmds.xform(joint2, q=1, ws=1, t=1))
    point = MPoint(p)*MMatrix(cmds.xform(joint1, q=1, ws=1, m=1)).inverse()
    if point[0] < 0:
        v = [-i for i in v]
    return vp_to_vx(v, p)


@locator_vx
def brow_vx(joint1, joint2):
    p1, p2 = cmds.xform(joint1, q=1, ws=1, t=1), cmds.xform(joint2, ws=1, q=1, t=1)
    p1, p2 = MVector(p1), MVector(p2)
    p2[1] = p1[1]
    p2[2] = p1[2]
    p = (p1 + p2) / 2
    v = (p2 - p1).normal()
    v, p = list(v)[:3], list(p)[:3]
    p = convert_p(p)
    return vp_to_vx(v, p)


@locator_vx
def belt_vx(joint1, joint2):
    p1, p2 = cmds.xform(joint1, q=1, ws=1, t=1), cmds.xform(joint2, q=1, ws=1, t=1)
    p1, p2 = MVector(p1), MVector(p2)
    p = (p1 + p2) / 2
    v = (p2 - p1).normal()
    v, p = list(v)[:3], list(p)[:3]
    p = convert_p(p)
    return vp_to_vx(v, p)


def split_init(typ):
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if paint_joint is None or unlock_joints is None:
        return
    if typ == "brow":
        unlock_joints.sort(key=lambda x: cmds.xform(x, q=1, ws=1, t=1)[0])
    else:
        unlock_joints.sort(key=lambda x: x)
        unlock_joints.sort(key=lambda x: cmds.ls(x, l=1)[0].count("|"))
    vxs = [globals()[typ+"_vx"](unlock_joints[i], joint) for i, joint in enumerate(unlock_joints[1:])]
    vxs = sum(vxs, [])
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    bezier_api.split_init(polygon, sk, indices, vxs)
    return True


def split_solve(xs, ys, r):
    r = cmds.softSelect(q=1, ssd=1) * r * 2
    bezier_api.solve("split", xs, ys, r)


brow_init = functools.partial(split_init, "brow")
spine_init = functools.partial(split_init, "spine")
belt_init = functools.partial(split_init, "belt")
brow_solve = split_solve
spine_solve = split_solve
belt_solve = split_solve


def points_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if unlock_joints is None:
        return
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    joint_points = [convert_p(cmds.xform(joint, q=1, ws=1, t=1)) for joint in unlock_joints]
    bezier_api.points_init(polygon, sk, indices, joint_points)
    return True


def points_solve(xs, ys, r):
    r = cmds.softSelect(q=1, ssd=1) * r
    ys = [1 - y for y in ys]
    bezier_api.solve("points", xs, ys, r)


def full_path(name):
    return cmds.ls(name, l=1)[0]


def get_joint_chains(unlock_joints):
    joint_length = len(unlock_joints)
    un_use_joints = sorted(unlock_joints, key=lambda x: len(full_path(x)))
    joint_chains = []
    for i in range(joint_length):
        joint_chain = [un_use_joints.pop(0)]
        joint_chain += [joint for joint in un_use_joints if full_path(joint).startswith(full_path(joint_chain[0]))]
        un_use_joints = [joint for joint in un_use_joints if joint not in joint_chain]
        joint_chains.append(joint_chain)
        if len(un_use_joints) == 0:
            break
    return joint_chains


def chains_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if paint_joint is None or unlock_joints is None:
        return
    joint_chains = get_joint_chains(unlock_joints)
    indices = [joints.index(unlock_joint) for unlock_joint in unlock_joints]
    top_indices = [joints.index(joint_chain[0]) for joint_chain in joint_chains]
    point_data = [[convert_p(cmds.xform(joint, q=1, ws=1, t=1))
                   for joint in joint_chain] for joint_chain in joint_chains]
    chin_lengths = [len(joint_chain) for joint_chain in joint_chains]
    joint_points = sum(point_data, [])
    bezier_api.chains_init(polygon, sk, indices, joint_points, chin_lengths, top_indices)
    return True


def lines_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if paint_joint is None or unlock_joints is None:
        return
    joint_chains = get_joint_chains(unlock_joints)
    joint_points = []
    indices = []
    for joint_chain in joint_chains:
        for i, joint in enumerate(joint_chain[1:]):
            indices.append(joints.index(joint_chain[i]))
            p1 = convert_p(cmds.xform(joint_chain[i], q=1, t=1, ws=1))
            p2 = cmds.xform(joint, q=1, ws=1, t=1)
            p1, p2 = MVector(p1), MVector(p2)
            p = (p1+p2)/2
            p = list(p)
            joint_points.append(convert_p(p))
    bezier_api.points_init(polygon, sk, indices, joint_points)
    return True


chains_solve = points_solve
lines_solve = points_solve


def finger_init():
    polygon, sk, joints, unlock_joints, paint_joint = default_init_var()
    if paint_joint is None or unlock_joints is None:
        return
    joint_chains = get_joint_chains(unlock_joints)
    indices = []
    vxs = []
    for joint_chain in joint_chains:
        for joint in joint_chain:
            indices.append(joints.index(joint))
        for i, joint in enumerate(joint_chain[1:]):
            vxs.append(spine_vx(joint_chain[i], joint))
    vxs = sum(vxs, [])
    chin_lengths = [len(joint_chain) for joint_chain in joint_chains]
    bezier_api.finger_init(polygon, sk, indices, vxs, chin_lengths)
    return True


def finger_solve(xs, ys, r):
    r = cmds.softSelect(q=1, ssd=1) * r * 2
    bezier_api.solve("finger", xs, ys, r)


def paint(typ, xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    if globals()[typ+"_init"]():
        globals()[typ+"_solve"](xs, ys, r)


def init(typ):
    return globals()[typ+"_init"]()


def solve(typ, xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    globals()[typ + "_solve"](xs, ys, r)

