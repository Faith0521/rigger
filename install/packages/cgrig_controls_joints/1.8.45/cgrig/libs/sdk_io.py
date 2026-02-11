# -*- coding: utf-8 -*-
import json
import os
import re
from maya import cmds
from maya.api import OpenMaya as om2
import maya.api.OpenMayaAnim as oman2

mirror_config = {
    # 基本镜像设置
    0: {
        "mirror_axis": "x",
        "attribute_rules": {
            "translateX": {
                "x": 1,  # invert/keep/pair
                "y": 1,
                "z": 1
            },
            "rotate": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            }
        }
    },
    1: {
        "mirror_axis": "x",
        "attribute_rules": {
            "translate": {
                "x": -1,  # invert/keep/pair
                "y": -1,
                "z": -1
            },
            "rotate": {
                "x": 1,
                "y": 1,
                "z": 1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            }
        }
    },
    2: {
        "mirror_axis": "x",
        "attribute_rules": {
            "translate": {
                "x": -1,  # invert/keep/pair
                "y": 1,
                "z": 1
            },
            "rotate": {
                "x": 1,
                "y": -1,
                "z": -1
            },
            "scale": {
                "x": 1,
                "y": 1,
                "z": 1
            }
        }
    }
}
# 切线类型映射
tangent_type_map = {
    0: "auto",
    1: "fixed",
    2: "linear",
    3: "flat",
    4: "smooth",
    5: "step",
    6: "slow",
    7: "fast",
    8: "clamped",
    9: "plateau",
    10: "stepnext"
}
reverse_tangent_type_map = {v: k for k, v in tangent_type_map.items()}


def get_valid_animation_curves():
    """
    使用API 2.0获取所有有效连接的动画曲线
    :return: (MObject列表, 曲线名称列表)
    """
    valid_mobjs = []
    valid_names = []

    # for curve_type in curve_types:
    iter = om2.MItDependencyNodes(om2.MFn.kAnimCurve)

    while not iter.isDone():
        mobj = iter.thisNode()
        dep_node = om2.MFnDependencyNode(mobj)

        # 检查输入连接
        input_plug = dep_node.findPlug("input", False)
        input_connected = input_plug.isConnected

        # 检查输出连接
        output_plug = dep_node.findPlug("output", False)
        output_connected = output_plug.isConnected

        # 只有同时有输入和输出连接才算有效
        if input_connected and output_connected:
            valid_mobjs.append(mobj)
            valid_names.append(dep_node.name())

        iter.next()

    return valid_mobjs, valid_names


def get_curve_data(mobj):
    """
    使用API 2.0获取动画曲线数据
    :param mobj: 动画曲线MObject
    :return: 包含曲线数据的字典
    """
    curve_fn = oman2.MFnAnimCurve(mobj)
    dep_node = om2.MFnDependencyNode(mobj)
    curve_name = dep_node.name()

    input_plug = dep_node.findPlug("input", False)

    output_plug = dep_node.findPlug("output", False)
    # 获取连接信息
    input_conns = removeEXnodes(input_plug.name().split('.')[0], True)
    output_conns = removeEXnodes(output_plug.name().split('.')[0], False)

    # 获取关键帧数据
    times = []
    values = []
    itt_list = []
    ott_list = []
    in_angles = []
    out_angles = []
    for i in range(curve_fn.numKeys):
        times.append(curve_fn.input(i))
        # value = curve_fn.value(i)
        ia, iv = curve_fn.getTangentAngleWeight(i, True)
        oa, ov = curve_fn.getTangentAngleWeight(i, False)
        value = cmds.getAttr("{0}.keyTimeValue[{1}]".format(curve_name, i))
        values.append(value[0][-1])
        in_angles.append(ia.asRadians())
        out_angles.append(oa.asRadians())
        itt_list.append(curve_fn.inTangentType(i))
        ott_list.append(curve_fn.outTangentType(i))

    return {
        'type': curve_fn.typeName,
        'input_connections': input_conns,
        'output_connections': output_conns,
        'times': times,
        'values': values,
        'in_tangent_types': itt_list,
        'out_tangent_types': ott_list,
        'in_angles': in_angles,
        'out_angles': out_angles,
        'pre_infinity': cmds.getAttr(curve_name + ".preInfinity"),
        'post_infinity': cmds.getAttr(curve_name + ".postInfinity"),
        'is_weighted': curve_fn.isWeighted,
        'is_static': curve_fn.isStatic
    }


def removeEXnodes(nodeName, is_source):
    connections = []
    results = []
    if is_source:
        connections = cmds.listConnections(nodeName + ".input", source=True, destination=False, plugs=True) or []
    else:
        connections = cmds.listConnections(nodeName + ".output", source=False, destination=True, plugs=True) or []

    for conn in connections:
        # 获取连接的节点（去掉属性部分）
        connected_node = conn.split('.')[0]

        # 检查节点类型
        node_type = cmds.objectType(connected_node)

        if node_type in ['unitConversion', 'blendWeighted', 'unitToTimeConversion']:
            # 如果是转换节点，继续递归查找
            connections = removeEXnodes(connected_node, is_source)
        else:
            results.append(conn)

    return list(set(connections + results))


def export_animation_curves(file_path):
    """
    使用API 2.0导出动画曲线数据到JSON文件
    :param file_path: 导出文件路径
    """
    mobjs, names = get_valid_animation_curves()
    export_data = {}

    for mobj, name in zip(mobjs, names):
        export_data[name] = get_curve_data(mobj)

    # 写入JSON文件
    with open(file_path, 'w') as f:
        json.dump(export_data, f, indent=4)

    print(u"成功导出 {0} 条动画曲线到 {1}".format(len(export_data), file_path))
    return True


def exportSdks(export_data, file_path):
    # 写入JSON文件
    with open(file_path, 'w') as f:
        json.dump(export_data, f, indent=4)

    print(u"成功导出 {0} 条动画曲线到 {1}".format(len(export_data), file_path))
    return True


def import_animation_curves(file_path):
    """
    使用API 2.0从JSON文件导入动画曲线数据
    :param file_path: 导入文件路径
    """
    if not os.path.exists(file_path):
        print("错误: 文件 {file_path} 不存在".format(file_path=file_path))
        return False

    with open(file_path, 'r') as f:
        import_data = json.load(f)
    # 重建连接关系
    for old_curve, curve_data in import_data.items():
        for i, output_conn in enumerate(curve_data['output_connections']):
            if cmds.objExists(curve_data['input_connections'][0]) and cmds.objExists(output_conn):
                for i, output_conn in enumerate(curve_data['output_connections']):
                    animCurrentCrv = getAnimCurve(curve_data['input_connections'][0], output_conn)
                    if not cmds.objExists(output_conn.split('.')[0]) or not cmds.objExists(curve_data['input_connections'][0]):
                        continue
                    if not animCurrentCrv:
                        for k in range(len(curve_data["times"])):
                            cmds.setDrivenKeyframe(output_conn.split('.')[0], at=output_conn.split('.')[1],
                                                   cd=curve_data['input_connections'][0],
                                                   dv=curve_data["times"][k], v=curve_data["values"][k])
                    else:
                        for animCurve in animCurrentCrv:
                            if not checkAnimCurveInput(animCurve):
                                cmds.delete(animCurve)
                        for k in range(len(curve_data["times"])):
                            cmds.setDrivenKeyframe(output_conn.split('.')[0], at=output_conn.split('.')[1],
                                                   cd=curve_data['input_connections'][0],
                                                   dv=curve_data["times"][k], v=curve_data["values"][k])
                    animCurrentCrv = getAnimCurve(curve_data['input_connections'][0], output_conn)
                    if animCurrentCrv:
                        for animCurve in animCurrentCrv:
                            setAnimCurve(animCurve, curve_data)


def getAnimCurve(driverAttr, drivenAttr):
    setdrivenCrv = []
    connections = cmds.listConnections(driverAttr, source=False, destination=True, type="animCurve", scn=True) or []
    if connections:
        for anim in connections:
            driven = removeEXnodes(anim, 0)
            if driven:
                driven = driven[0]
                if driven == drivenAttr:
                    setdrivenCrv.append(anim)
    return setdrivenCrv


def setAnimCurve(new_curve, curve_data, value_multi=1.0):
    # 设置曲线属性
    selectionList = om2.MSelectionList()
    selectionList.add(new_curve)
    curve_node = selectionList.getDependNode(0)

    curve_fn = oman2.MFnAnimCurve(curve_node)
    curve_fn.setPreInfinityType(curve_data['pre_infinity'])
    curve_fn.setPostInfinityType(curve_data['post_infinity'])

    times = curve_data['times']
    values = curve_data['values']
    in_tangent_types = curve_data['in_tangent_types']
    out_tangent_types = curve_data['out_tangent_types']
    in_angles = curve_data['in_angles']
    out_angles = curve_data['out_angles']

    if len(times) == curve_fn.numKeys:
        for i, time in enumerate(times):
            curve_fn.setInTangentType(i, in_tangent_types[i])
            curve_fn.setOutTangentType(i, out_tangent_types[i])

        for i, time in enumerate(times):
            if in_tangent_types[i] == 1 or out_tangent_types[i] == 1:
                curve_fn.setAngle(i, om2.MAngle(in_angles[i], om2.MAngle.kRadians), True)
                curve_fn.setAngle(i, om2.MAngle(out_angles[i], om2.MAngle.kRadians), False)


def is_valid_sdk_connection(target_plug, source_plug):
    """
    验证两个属性之间是否存在有效的SDK驱动关系

    :param target_plug: 目标属性（动画曲线输入端）
    :param source_plug: 源属性（驱动属性）
    :return: bool
    """
    attr_name = target_plug.partialName(
        includeNodeName=False,
        includeNonMandatoryIndices=False,
        useLongNames=True
    ).lower()

    return attr_name.startswith('input')


def find_sdk_connections(node, is_source, visited=None):
    if visited is None:
        visited = set()

    if node in visited:
        return {'all_nodes': [], 'sdk_nodes': []}

    visited.add(node)

    connections = []
    if is_source:
        connections = cmds.listConnections(node, source=True, destination=False, plugs=False) or []
    else:
        connections = cmds.listConnections(node, source=False, destination=True, plugs=False) or []

    all_nodes = []
    sdk_nodes = []

    for n in connections:
        if 'animCurve' in cmds.objectType(n):
            sdk_nodes.append(n)
        else:
            result = find_sdk_connections(n, is_source, visited)
            all_nodes.extend(result['all_nodes'])
            sdk_nodes.extend(result['sdk_nodes'])

        all_nodes.append(n)
    return {
        'all_nodes': list(set(all_nodes)),  # 去重
        'sdk_nodes': list(set(sdk_nodes))  # 去重
    }


def find_symmetric_attribute(attr_name):
    obj, attribute = attr_name.split('.')[0], attr_name.split('.')[1]

    # 常见的对称命名模式
    symmetry_patterns = [
        (r'_L(\D|$)', r'_R\1'),  # _L 和 _R 后缀
        (r'_R(\D|$)', r'_L\1'),
        (r'L_(\D|$)', r'R_\1'),
        (r'R_(\D|$)', r'L_\1'),
        (r'lf_(\D|$)', r'rt_\1'),
        (r'_left(\D|$)', r'_right\1'),  # _left 和 _right 后缀
        (r'_right(\D|$)', r'_left\1'),
        (r'Left(\D|$)', r'Right\1'),  # Left 和 Right 驼峰式
        (r'Right(\D|$)', r'Left\1'),
    ]

    # 检查属性是否存在
    if 'output' not in attribute:
        if not cmds.attributeQuery(attribute, node=obj, exists=True):
            return {
                'status': 'error',
                'message': '属性 {attribute} 在物体 {obj} 上不存在'.format(attribute=attr_name, obj=obj)
            }

    # 尝试找到对称物体
    symmetric_obj = None
    if cmds.objectType(obj) == "blendShape":
        symmetric_obj = obj
    else:
        for pattern, replacement in symmetry_patterns:
            symmetric_name = re.sub(pattern, replacement, obj)
            if symmetric_name != obj and cmds.objExists(symmetric_name):
                symmetric_obj = symmetric_name
                break

    if not symmetric_obj:
        symmetric_obj = obj

    # 尝试找到对称属性
    symmetric_attr = None
    for pattern, replacement in symmetry_patterns:
        symmetric_attr_name = re.sub(pattern, replacement, attribute)
        if symmetric_attr_name != attribute and cmds.attributeQuery(symmetric_attr_name, node=symmetric_obj,
                                                                    exists=True):
            symmetric_attr = symmetric_attr_name
            break

    if not symmetric_attr:
        if cmds.objExists("{symmetric_obj}.{attribute}".format(symmetric_obj=symmetric_obj, attribute=attribute)):
            symmetric_attr = attribute
        else:
            return {
                'status': 'attr_not_found',
                'message': '在对称物体 {symmetric_obj} 上未找到 {attribute} 的对称属性'.format(symmetric_obj=symmetric_obj, attribute=attribute),
                'symmetric_object': symmetric_obj
            }

    return {
        'status': 'success',
        'original_object': obj,
        'original_attribute': attribute,
        'symmetric_object': symmetric_obj,
        'symmetric_attribute': symmetric_attr
    }


def getSdkConnections(node, is_source):
    sdkNodes = find_sdk_connections(node, is_source)["sdk_nodes"]
    sdkConnections = {}
    for animCurve in sdkNodes:
        selectionList = om2.MSelectionList()
        selectionList.add(animCurve)
        anim_obj = selectionList.getDependNode(0)

        dep_node = om2.MFnDependencyNode(anim_obj)

        input_plug = dep_node.findPlug("input", False)
        input_connected = input_plug.isConnected

        # 检查输出连接
        output_plug = dep_node.findPlug("output", False)
        output_connected = output_plug.isConnected

        # 只有同时有输入和输出连接才算有效
        if (not input_connected) or (not output_connected):
            continue

        anim_data = get_curve_data(anim_obj)

        if is_source:
            for out in anim_data["output_connections"]:
                if node in out:
                    sdkConnections[animCurve] = anim_data
        else:
            if node in anim_data["input_connections"][0]:
                sdkConnections[animCurve] = anim_data

    return sdkConnections


def checkAnimCurveInput(animCurve):
    isValid = True
    selectionList = om2.MSelectionList()
    selectionList.add(animCurve)
    curve_node = selectionList.getDependNode(0)

    curve_fn = oman2.MFnAnimCurve(curve_node)
    if curve_fn.numKeys <= 1:
        isValid = False
    return isValid


def mirrorNodeSdk(node, is_source, mirror_type):
    sdkConnectionData = getSdkConnections(node, is_source)
    for animCurve, data in sdkConnectionData.items():
        input_node = data["input_connections"][0]
        if cmds.objectType(node) == 'blendShape':
            output_nodes = []
            for output_node in data["output_connections"]:
                if output_node.split('.')[0] == node:
                    output_nodes.append(output_node)
        else:
            output_nodes = data["output_connections"]

        sym_input_info = find_symmetric_attribute(input_node)
        sym_outputs_info = [find_symmetric_attribute(out) for out in output_nodes]
        sym_input_node = '{}.{}'.format(sym_input_info["symmetric_object"], sym_input_info["symmetric_attribute"]) if \
            sym_input_info["status"] == "success" else ""
        sym_outputs_nodes = []
        if sym_input_node == "":
            continue
        for sym_output in sym_outputs_info:
            sym_output_node = '{}.{}'.format(sym_output["symmetric_object"], sym_output["symmetric_attribute"]) if \
                sym_output["status"] == "success" else ""
            if sym_output_node == "":
                continue
            sym_outputs_nodes.append(sym_output_node)

        # 如果获取到的对称的驱动物体名字，被驱动物体名字和现在的一样，则不需要镜像
        for output, sym_output in zip(output_nodes, sym_outputs_nodes):
            if output == sym_output:
                sym_outputs_nodes.remove(sym_output)

        for i, out in enumerate(sym_outputs_nodes):
            existsAnimCurves = getAnimCurve(sym_input_node, out)
            outNode, outAttr = output_nodes[i].split('.')[0], output_nodes[i].split('.')[-1]
            symOutNode, symOutAttr = out.split('.')[0], out.split('.')[-1]
            value_scale = 1

            if mirror_type == 1:
                if 'translate' in symOutAttr:
                    value_scale = -1
            elif mirror_type == 2:
                if 'translateX' in symOutAttr or 'rotateY' in symOutAttr or 'rotateZ' in symOutAttr:
                    value_scale = -1

            if existsAnimCurves:
                cmds.delete(existsAnimCurves[0])
                for k in range(len(data["times"])):
                    cmds.setDrivenKeyframe(symOutNode, at=symOutAttr,
                                           cd=sym_input_node,
                                           dv=data["times"][k], v=data["values"][k] * value_scale)

                animCurrentCrv = getAnimCurve(sym_input_node, out)
                if animCurrentCrv:
                    setAnimCurve(animCurrentCrv[0], data, value_scale)
            else:
                for k in range(len(data["times"])):
                    cmds.setDrivenKeyframe(symOutNode, at=symOutAttr,
                                           cd=sym_input_node,
                                           dv=data["times"][k], v=data["values"][k] * value_scale)

                animCurrentCrv = getAnimCurve(sym_input_node, out)
                if animCurrentCrv:
                    setAnimCurve(animCurrentCrv[0], data, value_scale)


def set_driven_key(driver, driven, attr_list=None, default_values=None, value=1.0):
    """
    设置驱动关键帧,前后设置无限,模拟约束

    参数:
        driver (str): 驱动对象名称
        driven (str): 被驱动对象名称
        attr_list (list): 属性列表，默认为['tx', 'ty', 'tz']
        default_values (list): 包含默认值的列表，格式为[(驱动值1, 被驱动值1, 入切线1, 出切线1), ...]
                             默认为[(0, 0, 'linear', 'linear'),
                                   (-1, -1, 'clamped', 'linear'),
                                   (1, 1, 'linear', 'clamped')]
    """
    # 设置默认属性列表
    if attr_list is None:
        attr_list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']

    # 设置默认值
    if default_values is None:
        default_values = [
            (0, 0, 'linear', 'linear'),
            (-1, -1*value, 'clamped', 'linear'),
            (1, value, 'linear', 'clamped')
        ]

    # 为每个属性设置驱动关键帧
    for attr in attr_list:
        driven_attr = "{driven}.{attr}".format(driven=driven, attr=attr)
        driver_attr = "{driver}.{attr}".format(driver=driver, attr=attr)

        for dv, v, itt, ott in default_values:
            cmds.setDrivenKeyframe(
                driven_attr,
                cd=driver_attr,
                dv=dv,
                v=v,
                itt=itt,
                ott=ott
            )

        anim_curve = getAnimCurve(driver_attr, driven_attr)[0]
        cmds.setAttr("{}.preInfinity".format(anim_curve), 1)
        cmds.setAttr("{}.postInfinity".format(anim_curve), 1)


