# coding=utf-8
from imp import reload
from maya import cmds
from Faith.maya_utils import attribute_utils as attribute
from Faith.maya_utils import naming_utils as naming
reload(naming)


def get_selected_object_matrix():
    # 获取所有选择物体的子物体
    return [[top] + list(reversed(cmds.listRelatives(top, ad=1, f=1))) for top in cmds.ls(sl=1, o=1, l=1)]


def get_selected_objects():
    # 获取选择物体列表，若选择物体只有一个，则返回所有子物体
    selected = cmds.ls(sl=1, o=1, l=1)
    if len(selected) == 1:
        return get_selected_object_matrix()[0]
    else:
        return selected


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


def create_curve_by_joints(points):
    # 创建经过点points的曲
    # 创建多个线段，移至points
    curves = []
    for p in points:
        curve = cmds.curve(p=[[1, 0, 0], [-1, 0, 0]], d=1)
        cmds.xform(curve, ws=1, t=p)
        curves.append(curve)
    # 将线段放样成曲面
    surface = cmds.loft(curves, ch=1, u=1)[0]
    # 从曲面上复制曲线
    curve = cmds.duplicateCurve(surface+".v[0.5]", ch=0, rn=0, local=0)[0]
    cmds.delete(curves, surface)
    return curve


def re_joints(joints, count, axis, typ, prefix='control_', mirror=False, surface=None, world=False, add=True):
    """
    重建骨骼
    :param joints: 骨骼或曲线
    :param count: 新骨骼个
    :param axis: 第二轴轴
    :param typ: 第二轴朝向类
    :param prefix: 前缀名
    :param mirror: 是否镜像骨骼
    :param surface: 根据曲面创建骨骼
    :param world: 世界轴
    :param add: 添加属性
    :return:
    """
    # 获取骨骼矩阵，避免骨骼删掉后无法获取
    joints = [joint for joint in joints if cmds.objectType(joint) in ["joint", "transform"]]
    matrix_list = [cmds.xform(joint, q=1, ws=1, m=1) for joint in joints]
    if is_shape(joints[0], "nurbsCurve"):
        # 如果选择了曲线，则获取ep点坐
        points = cmds.xform(joints[0]+".cv[*]", q=1, ws=1, t=1)
        points = [points[i:i+3] for i in range(0, len(points), 3)]
    else:
        # 如果选择了骨骼，获取选择骨骼的坐
        points = [cmds.xform(joint, q=1, ws=1, t=1) for joint in joints]
        cmds.delete(joints)
    normals = []
    if surface:
        normals = get_joint_normals_by_surface(surface, count)

    # 创建经过points的曲
    curve = create_curve_by_joints(points)
    # 按骨骼长度，创建等长骨骼
    length = cmds.arclen(curve, ch=0)
    step = length/(count-1)
    joint = None
    joints = []
    for i in range(count):
        name = "{prefix}0{index}_jnt".format(prefix=prefix, index=i)
        if cmds.objExists(name):
            cmds.delete(name)
        joint = cmds.joint(joint, name="{prefix}0{index}_jnt".format(prefix=prefix, index=i))
        if add:
            attribute.addAttributes(joint, "rope_control_joint", "bool", value=True, keyable=False)
            attribute.addAttributes(joint, "rigName", "string", value=prefix, keyable=False)
            attribute.addAttributes(joint, "axis", "string", value=typ, keyable=False)
        cmds.setAttr(joint+".tx", step)
        joints.append(joint)
    cmds.xform(joints[0], ws=1, t=points[0])

    # 创建样条IK
    ik = cmds.ikHandle(sol="ikSplineSolver", ccv=0, sj=joints[0], ee=joints[-1], curve=curve)[0]

    for _ in range(3):
        # 在倒数第二个骨骼出，放止一个临时组，位置设置为points[-1]
        temp = cmds.group(em=1, p=joints[-2])
        cmds.xform(temp, ws=1, t=points[-1])
        # 此时，最后以跟x轴的坐标与临时组x轴坐标的差，越为线段长度与曲线长度的
        err = (cmds.getAttr(joints[-1]+".tx") - cmds.getAttr(temp+".tx"))/(count-1)
        # 缩小tx的值，减少误差，让最后一根骨骼落地在曲线末短
        for joint in joints[1:]:
            cmds.setAttr(joint + ".tx", cmds.getAttr(joint + ".tx")-err)
        cmds.delete(temp)

    # 设置骨骼第二轴朝
    if axis == "y":
        cmds.setAttr(ik + ".dWorldUpAxis", 0)
    elif axis == "z":
        cmds.setAttr(ik + ".dWorldUpAxis", 3)
    up_map = {
        "+x": [1, 0, 0],
        "-x": [-1, 0, 0],
        "+y": [0, 1, 0],
        "-y": [0, -1, 0],
        "+z": [0, 0, 1],
        "-z": [0, 0, -1]
    }
    if typ in up_map:
        # 设置up为世界正方向
        up1, up2 = up_map[typ], up_map[typ]
    else:
        # 设置up为首尾骨骼的y/z轴朝
        axis_index = slice(4, 7) if axis == "y" else slice(8, 11)
        joint_index = -1 if typ == u"首尾骨骼" else 0
        up1, up2 = matrix_list[0][axis_index], matrix_list[joint_index][axis_index]
    if normals:
        up1, up2 = normals[0], normals[-1]
    # 设置ik高级旋转
    cmds.setAttr(ik + ".dTwistControlEnable", True)
    cmds.setAttr(ik + ".dWorldUpType", 4)
    cmds.setAttr(ik + ".dWorldUpAxis", 0 if axis == "y" else 3)
    cmds.setAttr(ik + ".dWorldUpVector", *up1)
    cmds.setAttr(ik + ".dWorldUpVectorEnd", *up2)
    # 获取骨骼矩阵，触发ik计算更新
    cmds.xform(joints[0], q=1, ws=1, m=1)
    cmds.delete(ik, curve)
    # 显示轴向，冻结旋
    # cmds.toggle(joints, la=1)
    cmds.makeIdentity(joints, apply=1, r=1)
    if world:
        clear_rotation_keep_position(joints)
    if mirror:
        for joint in joints:
            mirror_joint = naming.convertRLName(joint)
            if cmds.objExists(mirror_joint):
                cmds.delete(mirror_joint)
        mirror_joints = cmds.mirrorJoint(joints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=["L_", "R_"])
        if add:
            [attribute.addAttributes(jnt, "rope_control_joint", "bool", value=True, keyable=False) for jnt in mirror_joints]
            [cmds.setAttr("{}.rigName".format(jnt), naming.convertRLName(prefix), type='string') for jnt in mirror_joints]
        joints += mirror_joints

    return joints


def re_all_joints(count, axis, typ, prefix='control_', mirror=False, surface=None, world=False, add=True):
    selected = []
    joints = re_joints(get_selected_objects(), count, axis, typ, prefix, mirror, surface, world, add)
    selected.append(joints[0])
    cmds.select(selected)
    return joints


def createCurveByJoints(joints, value, axis="y", name="", d=3):
    """
    通过关节创建两条沿指定轴偏移的曲线
    :param joints: 关节列表（需为场景中存在的关节）
    :param value: 偏移距离（基础值）
    :param axis: 偏移轴，支持"x"/"y"/"z"，默认"y"
    :param name: 曲线名称前缀，默认自动命名
    :return: 创建的两条曲线列表
    """
    curves = []
    move_values = [0, 0, 0]
    if not isinstance(joints, (list, tuple, set)):
        return []
    if axis == "y":
        move_values[1] = value
    elif axis == "z":
        move_values[2] = value
    for index,i in enumerate([0.5, -0.5]):
        pointList = []
        temp_transform_list = []
        for joint in joints:
            temp_transform = cmds.createNode("transform")
            cmds.delete(cmds.parentConstraint(joint, temp_transform))
            cmds.move(*[value*i for value in move_values], temp_transform, r=1, os=1, wd=1)
            pointList.append(cmds.xform(temp_transform, q=True, ws=True, t=True))
            temp_transform_list.append(temp_transform)
        curve = cmds.curve(d=d, p=pointList, name="{name}_{index}".format(name=name, index=index))
        curves.append(curve)
        cmds.delete(temp_transform_list)
    return curves


def get_joint_normals_by_surface(surface, num_joint):
    normals = []

    # 沿曲面的U方向创建骨骼
    for i in range(num_joint):
        # 计算当前位置的参数值 (0到1之间)
        u_param = float(i) / (num_joint - 1) if num_joint > 1 else 0.5
        v_param = 0.5  # 沿V方向中间位置

        # 获取该点的法向量（垂直于曲面）
        normal = cmds.pointOnSurface(surface, u=u_param, v=v_param, normal=True)
        normals.append(normal)
    return normals


import maya.cmds as cmds
import math


def clear_rotation_keep_position(selected):
    """
    获取物体的矩阵，清零旋转部分，同时保持位置不变

    参数:
        obj: 物体名称
    """
    matrixList = []
    for obj in selected:
        # 获取物体的世界空间矩阵
        world_matrix = cmds.xform(obj, query=True, matrix=True, worldSpace=True)

        # 提取位置信息（矩阵的第12、13、14元素对应x、y、z位置）
        pos_x, pos_y, pos_z = world_matrix[12], world_matrix[13], world_matrix[14]

        # 创建一个新的矩阵：单位矩阵（无旋转）+ 原始位置
        new_matrix = [
            1.0, 0.0, 0.0, 0.0,  # 第一列 - X轴方向
            0.0, 1.0, 0.0, 0.0,  # 第二列 - Y轴方向
            0.0, 0.0, 1.0, 0.0,  # 第三列 - Z轴方向
            pos_x, pos_y, pos_z, 1.0  # 第四列 - 位置
        ]

        # 应用新矩阵到物体
        matrixList.append(new_matrix)
    for i, matrix in enumerate(matrixList):
        cmds.setAttr(selected[i] + ".rotate", 0, 0, 0)
        cmds.setAttr(selected[i] + ".jointOrient", 0, 0, 0)
        cmds.xform(selected[i], matrix=matrix, worldSpace=True)



