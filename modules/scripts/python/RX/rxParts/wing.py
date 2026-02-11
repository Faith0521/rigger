# -*- coding: utf-8 -*-
from maya import cmds
from typing import List
from operator import itemgetter
import pymaya as pm
import re
import templateTools
import pointOnCrv
import cluster
import rivet
import maya.mel as mel
import controlTools
import tagTools
from Faith.maya_utils import attribute_utils
from rxCore import aboutName
from rxCore import aboutLock
from rxCore import aboutPublic
from typing import Dict, List, Union
from maya.api.OpenMaya import *


def template(side='lf', prefix='', parent='lf_shoulder', connetParent=[""], numFeatherJoints=4,
             numArmJoints=6, numElbowJoints=6, numWristJoints=4, numFingerJoints=2, featherStretch=True):
    args = dict()
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['connetParent'] = connetParent
    args['numArmJoints'] = numArmJoints
    args['numElbowJoints'] = numElbowJoints
    args['numWristJoints'] = numWristJoints
    args['numFingerJoints'] = numFingerJoints
    args['numFeatherJoints'] = numFeatherJoints
    args['featherStretch'] = featherStretch

    # Args to lock once part is built
    lockArgs = ['connetParent', 'control', 'numFeatherJoints', 'numArmJoints',
                'numElbowJoints', 'numWristJoints', 'numFingerJoints', 'featherStretch']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('wing', args, lockArgs)

    if not info:
        print('Exiting... ')
        return

    if not len(connetParent) == 4:
        cmds.warning(u"请选择四个翅膀身体骨骼!")
        return

    topnode = info[0]
    prefix = info[1]

    # 获取连接的父级的名字
    connetParentPosNode = []

    for connect in connetParent:
        if cmds.objExists(f"{connect}_pos") and 'templateJoint' in cmds.getAttr(f"{connect}_pos.tag"):
            connetParentPosNode.append(connect + "_pos")
        else:
            connetParentPosNode.append(connect)

    # 获取距离数值
    differences = [aboutPublic.getDistance2(pm.PyNode(a), pm.PyNode(b)) for a, b in
                   zip(connetParentPosNode[:-1], connetParentPosNode[1:])]
    average_diff = sum(differences) / len(differences) if differences else 0

    numPartsList = [numArmJoints, numElbowJoints, numWristJoints, numFingerJoints]
    numFeathers = sum(numPartsList) + len(connetParent)
    colors = ['blue'] * numFeathers

    mirror = 1
    if side == 'rt':
        colors = ['red'] * numFeathers
        mirror = -1
    prefixes = [prefix + "shoulder", prefix + "elbow", prefix + "wrist", prefix + "finger"]

    secFingerNames = group_with_prefixes([numArmJoints + 1, numElbowJoints + 1, numWristJoints + 1, numWristJoints+1], prefixes)

    if cmds.objExists(parent):
        cmds.delete(cmds.parentConstraint(parent, topnode))

    sec_pos_dict = insert_joints_sequentially(connetParent, numPartsList, average_diff*0.1)

    createJointsByPosDict(sec_pos_dict, secFingerNames, topnode, colors, numFeatherJoints, mirror, connetParent, average_diff)

    tagTools.tagIfRestorePos(topnode, prefix)

    return True


def group_with_prefixes(group_sizes, prefixes):
    if len(group_sizes) != len(prefixes):
        raise ValueError(u"分组尺寸和前缀数量必须一致")

    data = []
    for num, prefix in zip(group_sizes, prefixes):
        for i in range(num):
            name = prefix + '_secFeather' + aboutName.letter(i)
            data.append(name)

    return data


def split_list_by_sizes(data, group_sizes):
    result = []
    index = 0
    for size in group_sizes:
        if index + size > len(data):
            raise ValueError
        result.append(data[index: index + size])
        index += size
    return result


def createFeather(name, topnode, numFingerJoints, color, numSecJnts, mirror=1, distance=1.0, radius=1.0):
    # Create joints
    joints = []
    for i in range(2):
        if i == 0:
            # the first finger named "Base"
            ltr = 'Base'
        elif i == numFingerJoints:
            # the last finger named "End"
            ltr = 'End'
        else:
            ltr = aboutName.letter(i - 1)

        joint = templateTools.createJoint(name + ltr, topnode, color, makeGroups=True, ctrlOnly=False, pc=1, oc=0)
        cmds.move(0, 0, (-1 * i * distance), joint[0], r=1, os=1, wd=1)
        # cmds.setAttr(joint[0] + '.tz', i * distance)
        joints.append(joint[-1])

    [cmds.setAttr(jnt + '.radius', radius) for jnt in joints]
    cmds.parent(joints[0] + '_pos_grp', topnode + 'Ctrls')

    for i in range(1, len(joints)):
        cmds.parent(joints[i], joints[i - 1])

        # base
        #   --A : axisCrv
        #       --B
        #       --C
        #       --End

        # if i == 1:
        cmds.parent(joints[i] + '_pos_grp', joints[0] + '_pos')
        # elif i > 1:
        #     cmds.parent(joints[i] + '_pos_grp', joints[1] + '_pos')

        cmds.aimConstraint(joints[i] + '_pos', joints[i - 1], n=joints[i - 1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, 1],
                           wu=[0, 0, 1], wut='objectRotation', wuo=joints[i - 1] + '_pos')

        aboutLock.lock([joints[i] + '_pos_grp', joints[i] + '_pos_con', joints[i] + '_pos_sdk', joints[i] + '_pos'])
        aboutLock.unlock(joints[i] + '_pos', 't r')

        # Create ctrl
        ctrl = controlTools.create(joints[i - 1] + '_ctrl', shape='D07_circle', color=color, scale=1, jointCtrl=True)
        cmds.parent(ctrl[0], topnode + 'Ctrls')
        controlTools.rollCtrlShape(ctrl[-1], axis='z')
        cmds.parentConstraint(joints[i - 1], ctrl[0], n=ctrl[0] + '_prc')
        aboutLock.lock(ctrl)
        aboutLock.unlock(ctrl[-1], 't r s')

    aboutLock.lock([joints[0] + '_pos_con', joints[0] + '_pos_sdk', joints[0] + '_pos'])
    aboutLock.unlock(joints[0] + '_pos', 't r')

    # finger upper axis displate curve.
    axisCrv = mel.eval('curve -d 1 -p 0 -1 0 -p 0 0 0 -p 0 1 0 -k 0 -k 1 -k 2 ;')
    axisCrv = cmds.rename(axisCrv, joints[1] + '_axis')
    cmds.parentConstraint(joints[1], axisCrv, mo=False, n=axisCrv + '_prc')
    cmds.parent(axisCrv, topnode + 'Ctrls')
    cmds.select(axisCrv)
    aboutPublic.displaySet([axisCrv], 'reference')

    secJnts = createFeatherLimbGuide(name, topnode, [joints[0], joints[-1]], numSecJnts)

    return [joint + '_pos_grp' for joint in joints], joints, secJnts


def calculate_pos_between_selected(selected_joints, num_joints_per_gap_list: list):
    """
    在选中的骨骼之间平均生成指定数量的骨骼
    :param num_joints_per_gap_list: 每对骨骼之间生成的骨骼数量列表
    """
    if len(selected_joints) < 2:
        cmds.warning(u"请至少有两个物体！")
        return

    posList = []  # 存储所有骨骼（原始 + 新生成的）

    for i in range(len(selected_joints)):
        current_joint = selected_joints[i]
        posList.append(cmds.xform(current_joint, query=True, worldSpace=True, translation=True))  # 添加原始骨骼

        # 如果不是最后一根骨骼，计算中间骨骼
        if i < len(selected_joints) - 1:
            next_joint = selected_joints[i + 1]

            # 获取起始和结束骨骼的世界坐标位置
            pos_start = cmds.xform(current_joint, query=True, worldSpace=True, translation=True)
            pos_end = cmds.xform(next_joint, query=True, worldSpace=True, translation=True)

            # 在每对骨骼之间生成 num_joints_per_gap 个骨骼
            for j in range(1, num_joints_per_gap_list[i] + 1):
                # 计算插值比例 (0~1)
                t = float(j) / (num_joints_per_gap_list[i] + 1)

                # 线性插值位置
                new_pos = [
                    pos_start[0] + (pos_end[0] - pos_start[0]) * t,
                    pos_start[1] + (pos_end[1] - pos_start[1]) * t,
                    pos_start[2] + (pos_end[2] - pos_start[2]) * t
                ]

                posList.append(new_pos)

    return posList


def insert_joints_sequentially(
        joint_chain: List[str],
        insert_counts: Union[int, List[int]] = 1,
        scale: float = 1.0,
) -> Dict[str, List[float]]:
    """
    严格按照两两连续顺序插入骨骼，确保不跨顺序
    支持在最后一根骨骼之后也插入骨骼

    Args:
        joint_chain: 按顺序连接的骨骼链
        insert_counts: 每对相邻骨骼间要插入的数量，整数或列表
                      列表最后一个数字用于在最后一根骨骼之后插入

    Returns:
        字典 {骨骼名: 位置}，包含原始骨骼和插入骨骼

    Example:
        >>> insert_joints_sequentially(['jnt1','jnt2','jnt3'], [1,2,3])
        {
            'jnt1': [0,0,0],
            'jnt1_insert1': [1,0,0],  # jnt1和jnt2之间插入1个
            'jnt2': [2,0,0],
            'jnt2_insert1': [2.5,0,0], # jnt2和jnt3之间插入2个
            'jnt2_insert2': [3,0,0],
            'jnt3': [4,0,0],
            'jnt3_insert1': [5,0,0],   # jnt3之后插入3个
            'jnt3_insert2': [6,0,0],
            'jnt3_insert3': [7,0,0]
        }
    """
    # 参数验证
    if len(joint_chain) < 2:
        cmds.warning("需要至少2个骨骼组成链条")
        return {}

    # 处理insert_counts参数
    if isinstance(insert_counts, int):
        insert_counts = [insert_counts] * len(joint_chain)  # 包含末尾插入
    elif len(insert_counts) < len(joint_chain):
        # 如果数量不足，用最后一个值填充剩余
        last_count = insert_counts[-1]
        insert_counts = insert_counts + [last_count] * (len(joint_chain) - len(insert_counts))

    joint_data = {}
    prev_joint = joint_chain[0]
    joint_data[prev_joint] = cmds.xform(prev_joint, q=True, ws=True, t=True)

    # 处理骨骼之间的插入
    for i in range(1, len(joint_chain)):
        next_joint = joint_chain[i]
        start_pos = joint_data[prev_joint]
        end_pos = cmds.xform(next_joint, q=True, ws=True, t=True)

        # 当前对骨骼的插入处理
        count = insert_counts[i - 1]
        for j in range(1, count + 1):
            t = j / (count + 1)
            new_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * t,
                start_pos[1] + (end_pos[1] - start_pos[1]) * t,
                start_pos[2] + (end_pos[2] - start_pos[2]) * t
            ]
            insert_name = f"{prev_joint}_insert{j}"
            joint_data[insert_name] = new_pos

        # 添加当前原始骨骼
        joint_data[next_joint] = end_pos
        prev_joint = next_joint

    # 处理最后一根骨骼之后的插入
    last_joint = joint_chain[-1]
    last_count = insert_counts[-1] if len(insert_counts) >= len(joint_chain) else insert_counts[-1]

    if last_count > 0:
        start_pos = joint_data[last_joint]
        # 假设沿最后骨骼的朝向延伸(这里简单沿X轴延伸)
        for j in range(1, last_count + 1):
            new_pos = [
                start_pos[0] + j * scale,  # 每个间隔1单位
                start_pos[1],
                start_pos[2]
            ]
            insert_name = f"{last_joint}_insert{j}"
            joint_data[insert_name] = new_pos

    return joint_data


def createJointsByPosDict(posDict, names, parent, colors, numJoints, mirror, connectParent, scale=1.0):
    for partName, pos in posDict.items():
        id = list(posDict.keys()).index(partName)
        sec_feathers, sec_con_jnts, secJnts = createFeather(names[id], parent, 1, colors[id], numJoints,
                                                            mirror=mirror,
                                                            distance=scale * 1.1, radius=0.5)
        cmds.xform(sec_feathers[0], ws=1,
                   t=[pos[0], pos[1], pos[2] - (scale * 0.1)])
        if partName in connectParent:
            [cmds.setAttr(joint + ".radius", 1.5) for joint in secJnts]


def create_joint_chain_from_dict(joint_data: Dict[str, List[float]]) -> List[str]:
    """从位置字典创建实际的骨骼链"""
    created_joints = []
    parent = None

    for name, pos in joint_data.items():
        jnt = cmds.joint(n=name, p=pos)
        if parent:
            cmds.parent(jnt, parent)
        parent = jnt
        created_joints.append(jnt)

    return created_joints


def createFeatherLimbGuide(prefix, topnode, jnts, numJoints):
    nodes = []
    # create snap object
    for i in range(numJoints):
        l = cmds.createNode('transform')
        cmds.pointConstraint(jnts[0], l)
        cmds.orientConstraint(jnts[0], l)
        nodes.append(l)

    # create joints
    # jnts
    bendyJnts = []
    bendyJntsGrp = []

    for i in range(numJoints):
        upjnt = templateTools.createJoint(prefix + '_ub' + aboutName.letter(i), topnode, color='yellow', pc=1, oc=1)
        cmds.hide(upjnt[-2])

        cmds.setAttr(upjnt[-1] + '.radius', 0.5)

        bendyJnts.append(upjnt[-1])

        bendyJntsGrp.append(upjnt[0])

    # set position
    upStartPoint = cmds.xform(jnts[0], q=1, t=1, ws=1)
    upEndPoint = cmds.xform(jnts[1], q=1, t=1, ws=1)

    upCrv = cmds.curve(n=prefix + '_ub_temp_crv', p=[upStartPoint, upEndPoint], d=1, k=(0, 1))
    cluster.create([upCrv + '.cv[0]', jnts[0] + '_pos'])
    cluster.create([upCrv + '.cv[1]', jnts[1] + '_pos'])

    upPoslist = pointOnCrv.posListOnCrv(upCrv, numJoints - 1, ev=0, start=0, end=1)

    for i in range(numJoints):
        if i != numJoints - 1:
            cmds.parent(bendyJnts[i + 1], bendyJnts[i])

        cmds.xform(bendyJntsGrp[i], t=upPoslist[i], ws=1)
        cmds.orientConstraint(jnts[0], bendyJntsGrp[i])

    rivet.curve(bendyJntsGrp, upCrv, con=True, mo=True, wuo=None, mpnode=topnode + 'Nox')
    # clean
    cmds.parent(bendyJntsGrp, bendyJntsGrp, topnode + 'Nox')
    cmds.parent(upCrv, topnode + 'Nox')
    cmds.hide(upCrv)
    cmds.delete(nodes)
    return bendyJnts


def snap_shape_to_target_cmds(ctrl_name, target_name, offset_list):
    """
    使用 maya.cmds 将控制器的 Shape 吸附到目标物体位置
    """
    # 获取目标物体的世界坐标
    target_pos = cmds.xform(target_name, q=True, ws=True, t=True)

    # 获取控制器的世界坐标
    ctrl_pos = cmds.xform(ctrl_name, q=True, ws=True, t=True)

    # 计算偏移量
    offset = [
        target_pos[0] - ctrl_pos[0] + offset_list[0],
        target_pos[1] - ctrl_pos[1] + offset_list[1],
        target_pos[2] - ctrl_pos[2] + offset_list[2]
    ]

    # 获取控制器的 Shape 节点
    shapes = cmds.listRelatives(ctrl_name, shapes=True, fullPath=True)
    if not shapes:
        raise RuntimeError(f"{ctrl_name} 没有 Shape 节点")

    shape = shapes[0]
    shape_type = cmds.objectType(shape)

    # 根据 Shape 类型移动 CV 或顶点
    if shape_type == "nurbsCurve":
        # Nurbs 曲线：移动 CV 点
        cvs = cmds.ls(f"{shape}.cv[*]", flatten=True)
        for cv in cvs:
            cmds.move(offset[0], offset[1], offset[2], cv, r=True, ws=True, wd=True)
    elif shape_type == "mesh":
        # Mesh：移动顶点
        vertices = cmds.ls(f"{shape}.vtx[*]", flatten=True)
        for vtx in vertices:
            cmds.move(offset[0], offset[1], offset[2], vtx, r=True, os=True)
    else:
        raise RuntimeError(f"不支持的 Shape 类型: {shape_type}")


def distribute_shapes_symmetrically(controllers, total_width=None, spacing=None, axis="z"):
    """
    将控制器的 Shape 节点左右对称排列（不移动 Transform）
    :param controllers: 控制器列表（如 ["ctrl1", "ctrl2"]）
    :param total_width: 总分布宽度（与 spacing 二选一）
    :param spacing: 控制器间距（与 total_width 二选一）
    :param axis: 对称轴方向（"x"/"y"/"z"）
    """
    if not controllers:
        raise RuntimeError(u"控制器列表不能为空")

    num_ctrls = len(controllers)
    if num_ctrls < 2:
        cmds.warning(u"至少需要2个控制器")
        return

    # 计算间距或总宽度
    if total_width is not None:
        spacing = total_width / (num_ctrls - 1)
    elif spacing is not None:
        total_width = spacing * (num_ctrls - 1)
    else:
        spacing = 2.0  # 默认间距
        total_width = spacing * (num_ctrls - 1)

    # 确定对称轴（0=x, 1=y, 2=z）
    axis_index = {"x": 0, "y": 1, "z": 2}.get(axis.lower(), 0)
    start_pos = -total_width / 2
    offsets = [start_pos + i * spacing for i in range(num_ctrls)]

    # 遍历每个控制器
    for i, ctrl in enumerate(controllers):
        shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
        if not shapes:
            cmds.warning(f"控制器 {ctrl} 没有 Shape 节点")
            continue

        shape = shapes[0]

        cvs = cmds.ls(f"{shape}.cv[*]", flatten=True)
        for cv in cvs:
            current_pos = cmds.xform(cv, q=True, translation=True, objectSpace=True)
            current_pos[axis_index] += offsets[i]
            cmds.xform(cv, translation=current_pos, objectSpace=True)


def anim():
    parts = templateTools.getParts('wing')
    for part in parts:
        # > get parts data
        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        connetParent = templateTools.getArgs(part, 'connetParent')
        numArmJoints = templateTools.getArgs(part, 'numArmJoints')
        numElbowJoints = templateTools.getArgs(part, 'numElbowJoints')
        numWristJoints = templateTools.getArgs(part, 'numWristJoints')
        # numLayeredFeathers = templateTools.getArgs(part, 'numLayeredFeathers')
        numFeatherJoints = templateTools.getArgs(part, 'numFeatherJoints')
        # createSecondaryControls = templateTools.getArgs(part, 'createSecondaryControls')
        stretch = templateTools.getArgs(part, 'featherStretch')
        prefix = templateTools.getPrefix(side, prefix)

        color = "blue"
        mirror = 1
        if side == "rt":
            color = "red"
            mirror = -1

        # 计算距离
        connetParentPosNode = {
            "shoulder": connetParent[0] + "_drv",
            "elbow": connetParent[1] + "_drv",
            "wrist": connetParent[2] + "_drv",
            "wristEnd": connetParent[3] + "_drv"
        }
        connetParentPosNodeList = list(connetParentPosNode.values())
        differences = [aboutPublic.getDistance2(pm.PyNode(a), pm.PyNode(b)) for a, b in
                       zip(connetParentPosNodeList[:-1], connetParentPosNodeList[1:])]
        average_diff = sum(differences) / len(differences) if differences else 0

        # 创建大组
        mpNode = '{0}mod'.format(prefix + 'wing_')
        wing_mod = cmds.createNode("transform", name=mpNode, p="controls")
        wing_jnt = cmds.createNode("transform", name=prefix + "wing_jnt_grp", p=mpNode)
        wing_curve_jnt_grp = cmds.createNode("transform", name=prefix + "wing_curve_jnt_grp", p=wing_jnt)
        wing_ctrl_grp = cmds.createNode("transform", name=prefix + "wing_ctrl_grp", p=mpNode)
        ikCrvGrp = cmds.createNode("transform", name=f"{prefix}wing_sec_ik_curve_grp", p="crvsPrep")
        wing_ikh_grp = cmds.createNode("transform", name=f"{prefix}wing_ikHandle_noTrans", p="noTransform")
        # wing_loc_noTrans = cmds.createNode("transform", name=f"{prefix}wing_loc_noTrans", p="noTransform")
        wing_transform_noTrans = cmds.createNode("transform", name=f"{prefix}wing_transform_noTrans", p="noTransform")

        # > create jnts
        # ------------------------------------------------------------------------------------------------------------------
        # >> org jnts
        shoulder_jnt = connetParentPosNode["shoulder"]
        elbow_jnt = connetParentPosNode["elbow"]
        wrist_jnt = connetParentPosNode["wrist"]
        wristEnd_jnt = connetParentPosNode["wristEnd"]

        pattern_dict = getCompilePattern(prefix)

        all_jnts = pm.listRelatives("controls", c=1, ad=1, type="joint")
        shoulder_ub_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['shoulder_ub'].match(obj.nodeName())]
        elbow_ub_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['elbow_ub'].match(obj.nodeName())]
        wrist_ub_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['wrist_ub'].match(obj.nodeName())]
        finger_ub_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['finger_ub'].match(obj.nodeName())]
        feather_sec_ub_jnts = shoulder_ub_jnts + elbow_ub_jnts + wrist_ub_jnts + finger_ub_jnts
        feather_base_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['feather_base'].match(obj.nodeName())]
        # feather_end_jnts = [obj.nodeName() for obj in all_jnts if pattern_dict['feather_sec_ub'].match(obj.nodeName())]
        mainConJointList = [shoulder_ub_jnts[0], elbow_ub_jnts[0], wrist_ub_jnts[0], finger_ub_jnts[0]]

        [cmds.delete(jnt) for jnt in feather_base_jnts if cmds.objExists(jnt)]

        [cmds.parent(l[0], shoulder_jnt) for l in list(zip(*[iter(shoulder_ub_jnts)] * numFeatherJoints))]
        [cmds.parent(l[0], elbow_jnt) for l in list(zip(*[iter(elbow_ub_jnts)] * numFeatherJoints))]
        [cmds.parent(l[0], wrist_jnt) for l in list(zip(*[iter(wrist_ub_jnts)] * numFeatherJoints))]
        [cmds.parent(l[0], wristEnd_jnt) for l in list(zip(*[iter(finger_ub_jnts)] * numFeatherJoints))]

        # 创建half joint
        elbow_half_jnt = f'{elbow_jnt}_half_jnt'
        if not cmds.objExists(elbow_half_jnt):
            elbow_half_jnt = cmds.createNode("joint", name=f'{elbow_jnt}_half_jnt', p=elbow_jnt)
            cmds.parent(elbow_half_jnt, mpNode)
            cmds.setAttr(f"{elbow_half_jnt}.rotateOrder", 1)
            aboutPublic.createHalfConstraint(elbow_half_jnt, shoulder_jnt, elbow_jnt, type="parent")

        wrist_half_jnt = f'{wrist_jnt}_half_jnt'
        if not cmds.objExists(wrist_half_jnt):
            wrist_half_jnt = cmds.createNode("joint", name=f'{wrist_jnt}_half_jnt', p=wrist_jnt)
            cmds.parent(wrist_half_jnt, mpNode)
            cmds.setAttr(f"{wrist_half_jnt}.rotateOrder", 1)
            aboutPublic.createHalfConstraint(wrist_half_jnt, elbow_jnt, wrist_jnt, type="parent")

        cmds.addAttr(wing_mod, ln="stretch", min=0, max=1, dv=0)
        cmds.setAttr(wing_mod + ".stretch", e=1, k=1)
        cmds.addAttr(wing_mod, ln="bend", dv=0)
        cmds.setAttr(wing_mod + ".bend", e=1, k=1)

        # # do sec feather
        grouped_feather_sec_ub_jnt_list = list(zip(*[iter(feather_sec_ub_jnts)] * numFeatherJoints))
        grouped_feather_sec_ub_first_jnt_list = [jntChain[0] for jntChain in grouped_feather_sec_ub_jnt_list]
        # print(grouped_feather_sec_ub_first_jnt_list)
        initScale = 'worldA_ctrl.globalScale'

        result_ctrl = aboutPublic.create_hierarchy_groups_from_joint(grouped_feather_sec_ub_first_jnt_list, suffix="_ctrl")

        result_cns = aboutPublic.create_hierarchy_groups_from_joint(grouped_feather_sec_ub_first_jnt_list, suffix="_cns")

        joint_counts = [0, numArmJoints, numElbowJoints, numWristJoints]
        numPartList = [sum(joint_counts[:i + 1]) + i for i in range(4)]

        grouped_result_ctrl_list = [ctrlList for joint, ctrlList in result_ctrl.items()]
        grouped_result_cns_list = [cnsList for joint, cnsList in result_cns.items()]
        grouped_result_con_list = []

        [cmds.parent(ctrlList[0], wing_jnt) for joint, ctrlList in result_ctrl.items()]
        [cmds.parent(cnsList[0], wing_jnt) for joint, cnsList in result_cns.items()]

        for index, childs in enumerate(grouped_result_ctrl_list):
            featherCrvJnts = []
            groupList = aboutPublic.create_nested_groups_with_hierarchy(childs, ['sec_con', 'offset', 'con', 'sdk'], rotateOrder=0)
            conGrpList = []
            for i,child in enumerate(childs):
                conGrpList.append(groupList[i]['con']) if index in numPartList else conGrpList
                cmds.connectAttr(f"{grouped_result_cns_list[index][i]}.translate", f"{groupList[i]['sec_con']}.translate")
                cmds.connectAttr(f"{grouped_result_cns_list[index][i]}.rotate", f"{groupList[i]['sec_con']}.rotate")

                shape_name = "jack" if index in numPartList else "C01_cube"
                scale_value = 1.2 if index in numPartList else average_diff * 0.1

                skin_joint = cmds.createNode("joint", name=groupList[i]["sdk"].replace("sdk", "skin_jnt"), p=child)
                featherCrvJnts.append(skin_joint)
                ctrl_temp = controlTools.create(groupList[i]["sdk"].replace("sdk", "ctrl_temp"), shape=shape_name,
                                           makeGroups=0, color=color,
                                           snapTo=child,
                                           scale=[scale_value]*3)[0]
                shape = cmds.listRelatives(ctrl_temp, s=1, ad=1, ni=1)[0]
                cmds.parent(shape, child, r=1, s=1)
                cmds.delete(ctrl_temp)
            grouped_result_con_list.append(conGrpList)
            pos = [cmds.xform(c, query=True, worldSpace=True, translation=True) for c in childs]
            ikCrv = cmds.curve(degree=3, p=pos, name=f"{childs[0]}_ikCrv")  # 创建ikHandle曲线

            cmds.select([grouped_feather_sec_ub_jnt_list[index][0], grouped_feather_sec_ub_jnt_list[index][-1], ikCrv], r=1)
            ikHandle = cmds.ikHandle(
                name=f"{grouped_feather_sec_ub_jnt_list[index][0]}_ikh",
                startJoint=grouped_feather_sec_ub_jnt_list[index][0],
                endEffector=grouped_feather_sec_ub_jnt_list[index][-1],
                solver="ikSplineSolver",
                createCurve=0,
                c=ikCrv,
                simplifyCurve=False
            )[0]
            cmds.setAttr(f"{ikHandle}.visibility", 0)
            cmds.parent(ikHandle, wing_ikh_grp)

            # ik stretch
            scale_mult = cmds.createNode("multiplyDivide", name=grouped_feather_sec_ub_jnt_list[index][0] + "_global_scale_md")
            scale_devision = cmds.createNode("multiplyDivide", name=grouped_feather_sec_ub_jnt_list[index][0] + "_global_scale_devision")
            cmds.setAttr(f"{scale_devision}.operation", 2)
            crvInfo = cmds.createNode("curveInfo", name=ikCrv + "_info")
            cmds.connectAttr(f"{ikCrv}.worldSpace[0]", f"{crvInfo}.inputCurve")
            crv_length = cmds.getAttr(f"{crvInfo}.arcLength")
            cmds.connectAttr(initScale, f"{scale_mult}.input1X")
            cmds.setAttr(f"{scale_mult}.input2X", crv_length)
            cmds.connectAttr(f"{crvInfo}.arcLength", f"{scale_devision}.input1X")
            cmds.connectAttr(f"{scale_mult}.outputX", f"{scale_devision}.input2X")

            cmds.parent(ikCrv, ikCrvGrp)

            for joint_name in grouped_feather_sec_ub_jnt_list[index]:
                ik_jnt_tx_value = cmds.getAttr(joint_name + ".tx")
                stretch_md = cmds.createNode("multiplyDivide", name=joint_name + "_stretch_md")
                cmds.connectAttr(f"{scale_devision}.outputX", f"{stretch_md}.input1X")
                cmds.setAttr(stretch_md + ".input2X", ik_jnt_tx_value)
                blendColor = cmds.createNode("blendColors", name=f"{joint_name}_blend")
                cmds.connectAttr(f"{wing_mod}.stretch", f"{blendColor}.blender")
                cmds.connectAttr(f"{stretch_md}.outputX", f"{blendColor}.color1R")
                cmds.setAttr(blendColor + ".color2R", ik_jnt_tx_value)
                condition = cmds.createNode("condition", name=f"{joint_name}_condition")
                cmds.setAttr(f"{condition}.operation", 4)
                if side == 'rt':
                    cmds.setAttr(f"{condition}.operation", 2)
                cmds.connectAttr(f"{blendColor}.outputR", f"{condition}.colorIfFalseR")
                cmds.connectAttr(f"{blendColor}.color1R", f"{condition}.colorIfTrueR")
                cmds.connectAttr(f"{blendColor}.color1R", f"{condition}.firstTerm")
                cmds.setAttr(f"{condition}.secondTerm", ik_jnt_tx_value)
                cmds.connectAttr(f"{condition}.outColorR", f"{joint_name}.translateX")

            cmds.skinCluster(featherCrvJnts, ikCrv, maximumInfluences=1)

            cmds.setAttr(f"{ikHandle}.dTwistControlEnable", 1)
            cmds.setAttr(f"{ikHandle}.dWorldUpType", 4)

            cmds.connectAttr(f"{childs[0]}.worldMatrix[0]", f"{ikHandle}.dWorldUpMatrix")
            cmds.connectAttr(f"{childs[-1]}.worldMatrix[0]", f"{ikHandle}.dWorldUpMatrixEnd")

        [cmds.connectAttr(f"{wing_mod}.bend", f"{child}.rotateZ") for index, childs in enumerate(grouped_result_con_list) for child in childs]

        MainCnsInfo = getMainCnsInfo(grouped_result_cns_list, numPartList)
        MainCtrlssInfo = getMainCnsInfo(grouped_result_ctrl_list, numPartList)

        # aboutPublic.matrixConstraint([shoulder_jnt], MainCnsInfo[0][0], maintainOffset=True, prefix=MainCnsInfo[0][0], skipTranslate=['x', 'y', 'z'])
        # aboutPublic.matrixConstraint([elbow_half_jnt], MainCnsInfo[1][0], maintainOffset=True, prefix=MainCnsInfo[1][0], skipTranslate=['x', 'y', 'z'])
        # aboutPublic.matrixConstraint([wrist_half_jnt], MainCnsInfo[2][0], maintainOffset=True, prefix=MainCnsInfo[2][0], skipTranslate=['x', 'y', 'z'])
        # aboutPublic.matrixConstraint([wristEnd_jnt], MainCnsInfo[3][0], maintainOffset=True, prefix=MainCnsInfo[3][0], skipTranslate=['x', 'y', 'z'])

        shoulder_apply_cns = []
        elbow_apply_cns = []
        wrist_apply_cns = []

        for index, cns in enumerate(grouped_result_cns_list):
            if index != numPartList[0] and index < numPartList[1]:
                shoulder_apply_cns.append(cns)
            elif index != numPartList[1] and (numPartList[1] < index < numPartList[2]):
                elbow_apply_cns.append(cns)
            elif index != numPartList[2] and (numPartList[2] < index < numPartList[3]):
                wrist_apply_cns.append(cns)
        shoulder_apply_cns = [list(map(itemgetter(i), shoulder_apply_cns)) for i in range(numFeatherJoints)]
        elbow_apply_cns = [list(map(itemgetter(i), elbow_apply_cns)) for i in range(numFeatherJoints)]
        wrist_apply_cns = [list(map(itemgetter(i), wrist_apply_cns)) for i in range(numFeatherJoints)]

        for i in range(numFeatherJoints):
            assign_smooth_rotation_constraints(MainCtrlssInfo[0][i], MainCtrlssInfo[1][i], shoulder_apply_cns[i])
            assign_smooth_rotation_constraints(MainCtrlssInfo[1][i], MainCtrlssInfo[2][i], elbow_apply_cns[i])
            assign_smooth_rotation_constraints(MainCtrlssInfo[2][i], MainCtrlssInfo[3][i], wrist_apply_cns[i])

        # # clean
        # """drawStyle"""
        # [cmds.setAttr(f"{joint}.drawStyle", 2) for joint in list(set(feather_ub_jnts+feather_sec_ub_jnts+feather_end_jnts+feather_base_jnts+con_jnts+sec_jnts))]

    return


def get_prefix_type(s, pattern, prefix="lf_Up"):
    result = None
    match = re.fullmatch(pattern, s)
    if match:
        result = match.group(0)
    return result


def getCompilePattern(prefix):
    patternDict = {}
    shoulder_ub_comp = prefix + r"shoulder_secFeather.*_ub.*_drv(?:_\d+)?$"
    shoulder_ub_pattern = re.compile(shoulder_ub_comp)
    patternDict["shoulder_ub"] = shoulder_ub_pattern

    shoulder_sec_grp_comp = prefix + r"shoulder_secFeather.*_ub.*_sec_con_grp$"
    shoulder_sec_grp_pattern = re.compile(shoulder_sec_grp_comp)
    patternDict["shoulder_sec_grp"] = shoulder_sec_grp_pattern

    elbow_ub_comp = prefix + r"elbow_secFeather.*_ub.*_drv(?:_\d+)?$"
    elbow_ub_pattern = re.compile(elbow_ub_comp)
    patternDict["elbow_ub"] = elbow_ub_pattern

    elbow_sec_grp_comp = prefix + r"elbow_secFeather.*_ub.*_sec_con_grp$"
    elbow_sec_grp_pattern = re.compile(elbow_sec_grp_comp)
    patternDict["elbow_sec_grp"] = elbow_sec_grp_pattern

    wrist_ub_comp = prefix + r"wrist_secFeather.*_ub.*_drv(?:_\d+)?$"
    wrist_ub_pattern = re.compile(wrist_ub_comp)
    patternDict["wrist_ub"] = wrist_ub_pattern

    wrist_sec_grp_comp = prefix + r"wrist_secFeather.*_ub.*_sec_con_grp$"
    wrist_sec_grp_pattern = re.compile(wrist_sec_grp_comp)
    patternDict["wrist_sec_grp"] = wrist_sec_grp_pattern

    finger_ub_comp = prefix + r"finger_secFeather.*_ub.*_drv(?:_\d+)?$"
    finger_ub_pattern = re.compile(finger_ub_comp)
    patternDict["finger_ub"] = finger_ub_pattern

    finger_sec_grp_comp = prefix + r"finger_secFeather.*_ub.*_sec_con_grp$"
    finger_sec_grp_pattern = re.compile(finger_sec_grp_comp)
    patternDict["finger_sec_grp"] = finger_sec_grp_pattern

    feather_base_comp = prefix + r".*secFeather.*Base_drv(?:_\d+)?$"
    feather_base_pattern = re.compile(feather_base_comp)
    patternDict["feather_base"] = feather_base_pattern

    return patternDict


def create_hierarchy_groups_from_joint(selected_joints, suffix="_grp"):
    """
    根据选中的骨骼创建匹配的层级组结构
    返回: {选中骨骼短名称: [创建的组列表]}
    """
    # 获取选择的骨骼（只取第一个选中的骨骼）

    if not selected_joints:
        cmds.warning("请先选择一个关节！")
        return {}

    result = {}
    for jnt in selected_joints:
        root_joint = jnt

        # 获取该骨骼下的完整层级（包括自身和所有子级）
        all_joints = [root_joint]
        all_joints.extend(cmds.listRelatives(root_joint, allDescendents=True, type="joint") or [])

        # 按层级深度排序（确保先父后子）
        # all_joints.sort(key=lambda x: x.count("|"))

        created_groups = []  # 存储所有创建的组
        parent_dict = {}  # 临时存储父子关系 {短名称: 组}


        for joint in all_joints:
            # 获取关节短名称
            joint_name = joint
            group_name = joint_name + suffix
            # 获取父关节短名称
            parent_joint = cmds.listRelatives(joint, parent=True)
            parent_name = parent_joint[0] if parent_joint else None

            # 创建新组
            new_group = cmds.group(empty=True, name=group_name)
            created_groups.append(new_group)

            # 建立父子关系
            if parent_name and parent_name in parent_dict:
                cmds.parent(new_group, parent_dict[parent_name])

            # 复制变换属性
            cmds.matchTransform(new_group, joint)

            # 存储关系
            parent_dict[joint_name] = new_group

        result[jnt] = created_groups
    # 返回结果字典
    return result


def getMainCnsInfo(cnsList, numPartList):
    MainCnsInfo = [[]]*4
    for index, childs in enumerate(cnsList):
        if index == numPartList[0]:
            MainCnsInfo[0] = childs
        elif index == numPartList[1]:
            MainCnsInfo[1] = childs
        elif index == numPartList[2]:
            MainCnsInfo[2] = childs
        elif index == numPartList[3]:
            MainCnsInfo[3] = childs
    return MainCnsInfo


def createConstraintGrp(parentJoint, parentGrp, prefix='con'):
    zero_grp = cmds.createNode("transform", name=f"{parentJoint}_{prefix}_zero",
                               p=parentGrp)
    con_grp = cmds.createNode("transform", name=f"{parentJoint}_{prefix}",
                              p=zero_grp)
    cmds.delete(cmds.parentConstraint(parentJoint, zero_grp))
    aboutPublic.matrixConstraint([parentJoint], con_grp, maintainOffset=False,
                                 prefix=con_grp)
    return zero_grp, con_grp


def smoothstep(min_val, max_val, value):
    """Smoothstep插值函数"""
    x = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
    return x * x * (3 - 2 * x)


def assign_smooth_rotation_constraints(mainA, mainB, apply_ctrls):

    # 计算平滑权重
    weight_list = []
    num_controls = len(apply_ctrls) + 2

    for i in range(num_controls):
        # 计算归一化位置(0到1之间)
        t = float(i) / (num_controls - 1)
        # 应用smoothstep函数
        smooth_t = smoothstep(0.0, 1.0, t)
        weight_A = 1.0 - smooth_t
        weight_B = smooth_t
        weight_list.append((weight_A, weight_B))
    weight_list = weight_list[1:-1]
    # 为每个小控制器创建约束
    for i, small_ctrl in enumerate(apply_ctrls):
        # 创建跟随节点
        follow_A = cmds.createNode("transform",
                                   name=f"{small_ctrl}_follow1",
                                   parent=mainA)
        follow_B = cmds.createNode("transform",
                                   name=f"{small_ctrl}_follow2",
                                   parent=mainB)

        # 创建父约束
        constraint_name = cmds.parentConstraint(
            follow_A, follow_B, small_ctrl,
            skipTranslate=['x', 'y', 'z'],  # 只影响旋转
            weight=1.0,
            maintainOffset=True
        )[0]

        # 设置平滑权重
        cmds.setAttr(f"{constraint_name}.{follow_A}W0", weight_list[i][0])
        cmds.setAttr(f"{constraint_name}.{follow_B}W1", weight_list[i][1])


def createHalfJointCns(joint, con, parent):
    half_follow_con = cmds.createNode("transform", name=f"{con}_follow_con")
    half_noMove_con = cmds.createNode("transform", name=f"{con}_noMove_con")
    cmds.delete(cmds.parentConstraint(joint, half_follow_con))

    OneToOneCreateParentMatrix(parent, half_noMove_con)
    OneToOneCreateParentMatrix(con, half_follow_con)
    orig = cmds.orientConstraint(half_follow_con, half_noMove_con, joint, mo=True, skip=['x', 'z'])[0]
    cmds.setAttr(f"{orig}.interpType", 2)
    return half_follow_con, half_noMove_con


def OneToOneCreateParentMatrix(targetObj, aimObj, T=True, R=True, S=True, bridge=None, name=""):
    """
    矩阵一对一连接
    """
    nodeList = []
    parentMult = cmds.createNode("multMatrix", n="%s_parentMM" % aimObj)
    nodeList.append(parentMult)
    father_ma = cmds.getAttr(aimObj + ".worldMatrix[0]")
    parent_RevMatrix = cmds.getAttr(targetObj + ".worldInverseMatrix[0]")
    cmds.setAttr(parentMult + ".matrixIn[0]", aboutPublic.multiply_matrices(father_ma, parent_RevMatrix), type="matrix")
    if bridge:
        if not cmds.isConnected(targetObj + ".worldMatrix[0]", bridge):
            cmds.connectAttr(targetObj + ".worldMatrix[0]", bridge, f=True)
        cmds.connectAttr(bridge, parentMult + ".matrixIn[1]", f=True)
    else:
        cmds.connectAttr(targetObj + ".worldMatrix[0]", parentMult + ".matrixIn[1]")
    cmds.connectAttr(aimObj + ".parentInverseMatrix[0]", parentMult + ".matrixIn[2]")
    parentDecomp = cmds.createNode("decomposeMatrix", n="%s_parentDPM" % aimObj)
    nodeList.append(parentMult)
    cmds.connectAttr(parentMult + ".matrixSum", parentDecomp + ".inputMatrix")

    if T:
        cmds.connectAttr(parentDecomp + ".outputTranslate", aimObj + ".translate")

    if S:
        cmds.connectAttr(parentDecomp + ".outputScale", aimObj + ".scale")

    if R:
        fa_quatPr = cmds.createNode("quatProd", n="%s_quatPr" % aimObj)
        nodeList.append(fa_quatPr)
        cmds.connectAttr(parentDecomp + ".outputQuat", fa_quatPr + ".input1Quat")
        cmds.setAttr(fa_quatPr + ".input2QuatW", 1)

        fa_quatEu = cmds.createNode("quatToEuler", n="%s_quatEu" % aimObj)
        nodeList.append(fa_quatEu)
        cmds.connectAttr(fa_quatPr + ".outputQuat", fa_quatEu + ".inputQuat")
        cmds.connectAttr(aimObj + ".rotateOrder", fa_quatEu + ".inputRotateOrder")
        cmds.connectAttr(fa_quatEu + ".outputRotate", aimObj + ".rotate")

    return nodeList


def createPciNodeFromCurve(obj, curve, posNode):
    pci_node = cmds.createNode('pointOnCurveInfo', name=f"{obj}_pci")
    param = aboutPublic.getParamFromCurveAPI(posNode, curve)
    cmds.setAttr(f"{pci_node}.parameter", param)
    cmds.connectAttr(f"{curve}.worldSpace[0]", f"{pci_node}.inputCurve")
    cmds.connectAttr(f"{pci_node}.result.position", f"{obj}.translate")

    return pci_node


def increaseDecreaseAttr(bridgeList, attrList, addList):
    """
    attrList={}
    :param bridgeList:
    :param addAttrObjList:
    :param attrList:
    :param prefix:
    :return:
    """
    bridgeNetList = []
    for attr in attrList:
        for i, br in enumerate(bridgeList):
            bridge_net = cmds.createNode('network', name=f"{br}_{attr}_bridge_net")
            bridgeNetList.append(bridge_net)
            cmds.addAttr(bridge_net, ln='current_closest', at='double', dv=0)
            cmds.addAttr(bridge_net, ln='offset', at='double', dv=0)
            cmds.addAttr(bridge_net, ln='range', at='double', min=1, dv=1)
            cmds.addAttr(bridge_net, ln='closet_ratio', at='double', dv=0)

            cmds.addAttr(br, ln=f'{attr}_offset', at='double', dv=0)
            cmds.setAttr(f"{br}.{attr}_offset", e=1, k=1)

            cmds.addAttr(br, ln=f'{attr}_positionoffset', at='double', dv=0)
            cmds.setAttr(f"{br}.{attr}_positionoffset", e=1, k=1)

            cmds.addAttr(br, ln=f'{attr}_range', at='double', min=1, dv=1)
            cmds.setAttr(f"{br}.{attr}_range", e=1, k=1)

            pma = cmds.createNode("plusMinusAverage", n=f"{bridge_net}_pma")
            cmds.setAttr(f"{pma}.input3D[0]", 0, 0, 5)
            cmds.connectAttr(f"{br}.{attr}_offset", f"{pma}.input3D[1].input3Dx")
            cmds.connectAttr(f"{br}.{attr}_positionoffset", f"{pma}.input3D[1].input3Dy")
            cmds.connectAttr(f"{br}.{attr}_range", f"{pma}.input3D[1].input3Dz")
            cmds.setAttr(f"{pma}.input3D[2]", 0, 5 * i, -5)

            cmds.connectAttr(f"{pma}.output3Dx", f"{bridge_net}.offset")
            cmds.connectAttr(f"{pma}.output3Dy", f"{bridge_net}.current_closest")
            cmds.connectAttr(f"{pma}.output3Dz", f"{bridge_net}.range")

    for k,add in enumerate(addList):
        value_pma = cmds.createNode("plusMinusAverage", n=f"{add}_value_pma")

        for j,bridge in enumerate(bridgeNetList):
            diff_num_pma = cmds.createNode("plusMinusAverage", n=f"{bridge}_{add}_diff_num_pma")
            cmds.setAttr(f"{diff_num_pma}.operation", 2)
            cmds.connectAttr(f"{bridge}.current_closest", f"{diff_num_pma}.input3D[0].input3Dx")
            cmds.setAttr(f"{diff_num_pma}.input3D[1].input3Dx", k)

            posNeg_md = cmds.createNode("multDoubleLinear", n=f"{bridge}_{add}_posNeg_md")
            cmds.setAttr(f"{posNeg_md}.input2", -1)
            cmds.connectAttr(f"{diff_num_pma}.output3Dx", f"{posNeg_md}.input1")

            posNeg_condition = cmds.createNode("condition", n=f"{bridge}_{add}_posNeg_condition")
            cmds.setAttr(f"{posNeg_condition}.operation", 4)
            cmds.setAttr(f"{posNeg_condition}.secondTerm", 0)
            cmds.connectAttr(f"{diff_num_pma}.output3Dx", f"{posNeg_condition}.colorIfFalseR")
            cmds.connectAttr(f"{posNeg_md}.output", f"{posNeg_condition}.colorIfTrueR")
            cmds.connectAttr(f"{diff_num_pma}.output3Dx", f"{posNeg_condition}.firstTerm")

            action_num_pma = cmds.createNode("plusMinusAverage", n=f"{bridge}_{add}_action_num_pma")
            cmds.setAttr(f"{action_num_pma}.operation", 2)
            cmds.connectAttr(f"{bridge}.range", f"{action_num_pma}.input3D[0].input3Dx")
            cmds.connectAttr(f"{posNeg_condition}.outColorR", f"{action_num_pma}.input3D[1].input3Dx")

            diff_inversevalue_pma = cmds.createNode('plusMinusAverage', n=f"{bridge}_{add}_diff_inversevalue_pma")
            cmds.setAttr(f"{diff_inversevalue_pma}.operation", 2)
            cmds.setAttr(f"{diff_inversevalue_pma}.input3D[0].input3Dx", 1)
            cmds.connectAttr(f"{bridge}.closet_ratio", f"{diff_inversevalue_pma}.input3D[1].input3Dx")

            diff_value_adl = cmds.createNode("addDoubleLinear", n=f"{bridge}_{add}_diff_value_adl")
            cmds.connectAttr(f"{action_num_pma}.output3Dx", f"{diff_value_adl}.input1")
            cmds.connectAttr(f"{diff_inversevalue_pma}.output3Dx", f"{diff_value_adl}.input2")

            value_ratio_condition = cmds.createNode("condition", n=f"{bridge}_{add}_value_ratio_condition")
            cmds.setAttr(f"{value_ratio_condition}.operation", 3)
            cmds.setAttr(f"{value_ratio_condition}.colorIfFalseR", 0)
            cmds.connectAttr(f"{diff_value_adl}.output", f"{value_ratio_condition}.firstTerm")
            cmds.connectAttr(f"{diff_value_adl}.output", f"{value_ratio_condition}.colorIfTrueR")

            bridge_range_md = cmds.createNode("multiplyDivide", n=f"{bridge}_{add}_bridge_range_md")
            cmds.setAttr(f"{bridge_range_md}.operation", 2)
            cmds.connectAttr(f"{bridge}.offset", f"{bridge_range_md}.input1X")
            cmds.connectAttr(f"{bridge}.range", f"{bridge_range_md}.input2X")

            rotationV_md = cmds.createNode("multDoubleLinear", n=f"{bridge}_{add}_rotationV_md")
            cmds.connectAttr(f"{value_ratio_condition}.outColorR", f"{rotationV_md}.input1")
            cmds.connectAttr(f"{bridge_range_md}.outputX", f"{rotationV_md}.input2")
            cmds.connectAttr(f"{rotationV_md}.output", f"{value_pma}.input3D[{j}].input3Dx")

        cmds.connectAttr(f"{value_pma}.output3Dx", f"{add}.rotateX")

    return bridgeNetList


























