# -*- coding: utf-8 -*-

from imp import reload
from maya import cmds
import pymel.core as pm
from pymel.core import *
from pymel.core import datatypes
from . import api_utils as api
from . import function_utils as func
from . import vector_utils as vector
from . import controller_utils as ctrl
from . import attribute_utils as attribute
from maya.api import OpenMaya
from pymel import util
import re
import os

reload(api)
reload(func)


def setMatrixPosition(in_m, pos):
    """Set the position for a given matrix

    Arguments:
        in_m (matrix): The input Matrix.
        pos (list of float): The position values for xyz

    Returns:
        matrix: The matrix with the new position

    >>> tnpo = tra.setMatrixPosition(tOld, tra.getPositionFromMatrix(t))

    >>> t = tra.setMatrixPosition(t, self.guide.apos[-1])

    """
    m = datatypes.Matrix()
    m[0] = in_m[0]
    m[1] = in_m[1]
    m[2] = in_m[2]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def getTransformLookingAt(pos, lookat, normal, axis, negate=False):
    normal.normalize()

    if negate:
        a = pos - lookat
    else:
        a = lookat - pos

    a.normalize()
    c = util.cross(a, normal)
    c.normalize()
    b = util.cross(c, a)
    b.normalize()

    if axis == "xy":
        X = a
        Y = b
        Z = c
    elif axis == "xz":
        X = a
        Z = b
        Y = -c
    elif axis == "x-z":
        X = a
        Z = -b
        Y = c
    elif axis == "x-y":
        X = a
        Y = -b
        Z = -c
    elif axis == "-xy":
        X = -a
        Y = b
        Z = -c
    elif axis == "-xz":
        X = -a
        Z = b
        Y = c
    elif axis == "-x-y":
        X = -a
        Y = -b
        Z = c
    elif axis == "-x-z":
        X = -a
        Z = -b
        Y = -c
    elif axis == "yx":
        Y = a
        X = b
        Z = -c
    elif axis == "yz":
        Y = a
        Z = b
        X = c
    elif axis == "y-x":
        Y = a
        X = -b
        Z = c
    elif axis == "y-z":
        Y = a
        Z = -b
        X = -c
    elif axis == "-yx":
        Y = -a
        X = b
        Z = c
    elif axis == "-yz":
        Y = -a
        Z = b
        X = -c
    elif axis == "-y-x":
        Y = -a
        X = -b
        Z = -c
    elif axis == "-y-z":
        Y = -a
        Z = -b
        X = c
    elif axis == "zx":
        Z = a
        X = b
        Y = c
    elif axis == "z-x":
        Z = a
        X = -b
        Y = -c
    elif axis == "zy":
        Z = a
        Y = b
        X = -c
    elif axis == "z-y":
        Z = a
        Y = -b
        X = c
    elif axis == "-zx":
        Z = -a
        X = b
        Y = -c
    elif axis == "-z-x":
        Z = -a
        X = -b
        Y = c
    elif axis == "-zy":
        Z = -a
        Y = b
        X = c
    elif axis == "-z-y":
        Z = -a
        Y = -b
        X = -c

    m = datatypes.Matrix()
    m[0] = [X[0], X[1], X[2], 0.0]
    m[1] = [Y[0], Y[1], Y[2], 0.0]
    m[2] = [Z[0], Z[1], Z[2], 0.0]
    m[3] = [pos[0], pos[1], pos[2], 1.0]

    return m


def getChainTransform(positions, normal, axis, negate=False):
    transforms = []
    for i in range(len(positions) - 1):
        v0 = positions[i - 1]
        v1 = positions[i]
        v2 = positions[i + 1]

        # Normal Offset
        if i > 0:
            normal = vector.getTransposedVector(
                normal, [v0, v1], [v1, v2])

        t = getTransformLookingAt(v1, v2, normal, axis, negate)
        transforms.append(t)

    return transforms


def matrixConstraint(drivers,
                     driven,
                     maintainOffset=True,
                     prefix="",
                     skipRotate=None,
                     skipTranslate=None,
                     skipScale=None,
                     source_parent_cutoff=None,
                     weightList=None,
                     **short_arguments
                     ):
    """
    Create a Matrix Constraint.
    :param drivers: Parent Node(s)
    :param driven: Child Node
    :param maintainOffset: Maintain offset
    :param prefix: Prefix for the nodes names which will be created
    :param skipRotate: "xyz" or ["x", "y", "z"]
    :param skipTranslate: "xyz" or ["x", "y", "z"]
    :param skipScale: "xyz" or ["x", "y", "z"]
    :param source_parent_cutoff: The transformation matrices above
    this node won't affect to the child
    :param short_arguments:
    :return: (Tuple) mult_matrix, decompose_matrix, wtAddMatrix
    """
    # match the long names to the short ones if used
    for key, value in short_arguments:
        if key == "mo":
            maintainOffset = key
        elif key == "sr":
            skipRotate = value
        elif key == "st":
            skipTranslate = value
        elif key == "ss":
            skipScale = value
        elif key == "spc":
            source_parent_cutoff = value

    is_multi = bool(isinstance(drivers, list))
    is_joint = bool(cmds.objectType(driven) == "joint")
    if is_multi and source_parent_cutoff:
        source_parent_cutoff = None
    parents = cmds.listRelatives(driven, parent=True)
    parent_of_driven = parents[0] if parents else None
    next_index = -1

    mult_matrix = cmds.createNode("multMatrix", name="{}_multMatrix".format(prefix))
    decompose_matrix = cmds.createNode(
        "decomposeMatrix", name="{}_decomposeMatrix".format(prefix))

    # if there are multiple targets, average them first separately
    if is_multi:
        driver_matrix_plugs = ["{}.worldMatrix[0]".format(x) for x in drivers]
        if not weightList:
            average_node = average_matrix(driver_matrix_plugs,
                                          return_plug=False)
            out_plug = "{}.matrixSum".format(average_node)
        else:
            average_node = average_matrix_by_weight_list(driver_matrix_plugs, weightList, return_plug=False)
            out_plug = "{}.matrixSum".format(average_node)
    else:
        out_plug = "{}.worldMatrix[0]".format(drivers)
        average_node = None

    if maintainOffset:
        driven_world_matrix = api.get_mdag_path(driven).inclusiveMatrix()
        if is_multi:
            driver_world_matrix = OpenMaya.MMatrix(cmds.getAttr(out_plug))
        else:
            driver_world_matrix = api.get_mdag_path(drivers).inclusiveMatrix()
        local_offset = driven_world_matrix * driver_world_matrix.inverse()
        next_index += 1
        cmds.setAttr("{0}.matrixIn[{1}]".format(mult_matrix, next_index),
                     local_offset, type="matrix")

    next_index += 1
    cmds.connectAttr(out_plug, "{0}.matrixIn[{1}]".format(mult_matrix, next_index))

    cmds.connectAttr("{}.matrixSum".format(mult_matrix),
                     "{}.inputMatrix".format(decompose_matrix))

    if source_parent_cutoff:
        next_index += 1
        cmds.connectAttr("{}.worldInverseMatrix".format(source_parent_cutoff),
                         "{0}.matrixIn[{1}]".format(mult_matrix, next_index))

    if parent_of_driven:
        next_index += 1
        cmds.connectAttr("{}.worldInverseMatrix[0]".format(parent_of_driven),
                         "{0}.matrixIn[{1}]".format(mult_matrix, next_index))

    if not skipTranslate:
        cmds.connectAttr("{}.outputTranslate".format(decompose_matrix),
                         "{}.translate".format(driven))
    else:
        for attr in "XYZ":
            if attr.lower() not in skipTranslate and attr.upper() not in skipTranslate:
                cmds.connectAttr(
                    "{0}.outputTranslate{1}".format(
                        decompose_matrix, attr),
                    "{0}.translate{1}".format(driven, attr))

    # if the driven is a joint, the rotations needs to be handled differently
    # is there any rotation attribute to connect?
    if not skipRotate or len(skipRotate) != 3:
        if is_joint:
            # store the orientation values
            rot_index = 0
            second_index = 0
            joint_orientation = cmds.getAttr("{}.jointOrient".format(driven))[0]

            # create the compensation node strand
            rotation_compose = cmds.createNode(
                "composeMatrix", name="{}_rotateComposeMatrix".format(prefix))
            rotation_first_mult_matrix = cmds.createNode(
                "multMatrix", name="{}_firstRotateMultMatrix".format(prefix))
            rotation_inverse_matrix = cmds.createNode(
                "inverseMatrix", name="{}_rotateInverseMatrix".format(prefix))
            rotation_sec_mult_matrix = cmds.createNode(
                "multMatrix", name="{}_secRotateMultMatrix".format(prefix))
            rotation_decompose_matrix = cmds.createNode(
                "decomposeMatrix", name="{}_rotateDecomposeMatrix".format(prefix))

            # set values and make connections for rotation strand
            cmds.setAttr("{}.inputRotate".format(rotation_compose),
                         *joint_orientation)
            cmds.connectAttr("{}.outputMatrix".format(rotation_compose),
                             "{0}.matrixIn[{1}]".format(
                                 rotation_first_mult_matrix, rot_index))

            if parent_of_driven:
                rot_index += 1
                cmds.connectAttr("{}.worldMatrix[0]".format(parent_of_driven),
                                 "{0}.matrixIn[{1}]".format(
                                     rotation_first_mult_matrix,
                                     rot_index))
            cmds.connectAttr("{}.matrixSum".format(rotation_first_mult_matrix),
                             "{}.inputMatrix".format(rotation_inverse_matrix))

            cmds.connectAttr(out_plug, "{0}.matrixIn[{1}]".format(
                rotation_sec_mult_matrix, second_index))

            if source_parent_cutoff:
                second_index += 1
                cmds.connectAttr("{}.worldInverseMatrix".format(
                    source_parent_cutoff),
                    "{0}.matrixIn[{1}]".format(rotation_sec_mult_matrix, second_index))

            second_index += 1
            cmds.connectAttr("{}.outputMatrix".format(
                rotation_inverse_matrix),
                "{0}.matrixIn[{1}]".format(rotation_sec_mult_matrix, second_index))
            cmds.connectAttr("{}.matrixSum".format(
                rotation_sec_mult_matrix),
                "{}.inputMatrix".format(rotation_decompose_matrix))
            rotation_output_plug = "{}.outputRotate".format(rotation_decompose_matrix)
        else:
            rotation_output_plug = "{}.outputRotate".format(decompose_matrix)

        # it All rotation attrs will be connected?
        if not skipRotate:
            cmds.connectAttr(rotation_output_plug, "{}.rotate".format(driven))
        else:
            for attr in "XYZ":
                if attr.lower() not in skipRotate and attr.upper() not in skipRotate:
                    cmds.connectAttr(
                        "{0}{1}".format(
                            rotation_output_plug, attr),
                        "{0}.rotate{1}".format(driven, attr))

    if not skipScale:
        cmds.connectAttr("{}.outputScale".format(decompose_matrix),
                         "{}.scale".format(driven))
    else:
        for attr in "XYZ":
            if attr.lower() not in skipScale and attr.upper() not in skipScale:
                cmds.connectAttr("{0}.outputScale{1}".format(
                    decompose_matrix, attr),
                    "{0}.scale{1}".format(driven, attr))

    return mult_matrix, decompose_matrix, average_node


def average_matrix(matrices_list, return_plug=True, name="averageMatrix"):
    """
	Average a list of matrices.
	:param matrices_list: List of matrices to average
	:param return_plug: Return the output plug or the node (optional)
	:param name: Name of the node (optional)
	:return: String: Output plug or node
	"""
    average_matrix_node = cmds.createNode("wtAddMatrix", name=name)
    average_value = 1.0 / len(matrices_list)
    for index, matrix in enumerate(matrices_list):
        cmds.connectAttr(matrix, "{0}.wtMatrix[{1}].matrixIn".format(
            average_matrix_node, index))
        cmds.setAttr("{0}.wtMatrix[{1}].weightIn".format(
            average_matrix_node, index), average_value)
    if return_plug:
        return "{}.matrixSum".format(average_matrix_node)
    else:
        return average_matrix_node


def average_matrix_by_weight_list(matrices_list, weightList, return_plug=True, name="averageMatrix"):
    average_matrix_node = cmds.createNode("wtAddMatrix", name=name)
    for index, matrix in enumerate(matrices_list):
        cmds.connectAttr(matrix, "{0}.wtMatrix[{1}].matrixIn".format(
            average_matrix_node, index))
        cmds.setAttr("{0}.wtMatrix[{1}].weightIn".format(
            average_matrix_node, index), weightList[index])
    if return_plug:
        return "{}.matrixSum".format(average_matrix_node)
    else:
        return average_matrix_node


def AttrSet(ObjattrDatadic):
    """
	attrDatadic = {obj.Attr:data,obj.Attr:data}
	"""
    for objattr in ObjattrDatadic:
        Data = ObjattrDatadic.get(objattr)
        cmds.setAttr(objattr, Data)


def GrpAdd(Obj, GrpNames, addgrpRelativeTier):
    """
	Ass Groups
	:param self:
	:param Obj:
	:param GrpNames:
	:param addgrpRelativeTier:
	:return:
	"""
    objParent = cmds.listRelatives(Obj, p=True, f=True)
    GrpNames = GrpNames[::-1]
    Grps = []
    for grp in GrpNames:
        if cmds.objExists(grp):
            cmds.warning(grp + '------ is exists')
        if grp == GrpNames[0]:
            grp = cmds.group(em=True)
            Grps.append(grp)
        else:
            grp = cmds.group()
            Grps.append(grp)

    Grps = Grps[::-1]
    topGrp = Grps[0]
    EndGrp = Grps[-1]
    cmds.parent(topGrp, Obj)
    AttrSet({topGrp + '.rx': 0,
             topGrp + '.ry': 0,
             topGrp + '.rz': 0,
             topGrp + '.tx': 0,
             topGrp + '.ty': 0,
             topGrp + '.tz': 0,
             topGrp + '.sx': 1,
             topGrp + '.sy': 1,
             topGrp + '.sz': 1})
    if addgrpRelativeTier == 'Up':
        cmds.parent(topGrp, w=True)
        if objParent:
            cmds.parent(topGrp, objParent)
        cmds.parent(Obj, EndGrp)
    elif addgrpRelativeTier == 'Dn':
        pass
    Grps = Grps[::-1]
    cmds.select(Grps, add=True)
    for i in range(len(Grps)):
        cmds.rename(Grps[i], GrpNames[i])
    reGrps = cmds.ls(sl=True)[::-1]

    return reGrps


def mirrorObj(obj, freez=True):
    """

    :param obj:
    :param freez:
    :return:
    """
    mirrorGrp = createNode("transform", name=obj + "_mirror")
    parent(obj, mirrorGrp)
    setAttr(mirrorGrp + ".sx", -1)
    parent(obj, w=True)
    delete(mirrorGrp)
    if freez:
        makeIdentity(obj, apply=True, t=True, r=True, s=True)


def getNodeByMessage(attrName, node=None, *args):
    """ Get connected node in the given attribute searching as message.
		If there isn't a given node, try to use All_Grp.
		Return the found node name or False if it wasn't found.
	"""
    result = False
    if not node:
        # try to find All_Grp
        allTransformList = cmds.ls(selection=False, type="transform")
        if allTransformList:
            for transform in allTransformList:
                if cmds.objExists(transform + ".masterGrp"):
                    if cmds.getAttr(transform + ".masterGrp") == 1:
                        node = transform  # All_Grp found
                        break
    if node:
        if cmds.objExists(node + "." + attrName):
            foundNodeList = cmds.listConnections(node + "." + attrName, source=True, destination=False)
            if foundNodeList:
                result = foundNodeList[0]
    return result


def matrixOnCurve(count=4,
                  pCountList=[],
                  degree=3):
    """
	Creates an example curve with the given cv and point counts.
	:param count: The amount of ctrls.
	:param pCountList: Node List.
	:param degree: The degree of the curve.
	:return:
	"""
    cvMatrices = []


def connections(node,
                exclude_nodes=None,
                exclude_types=None,
                return_mode="all"
                ):
    """
	Return the connections for the given node as a dictionary
	result_dict = {
		"incoming": [
			{
				"plug_out": "someNode.outputX",
				"plug_in": "node.inputX"
			}
		]
		"outgoing": [
			{
				"plug_out": "node.outputX",
				"plug_in": "someOtherNode.inputZ
			}
		]
		}
	Args:
		node (str): Node to get connections
		exclude_nodes (List): nodes in this list will be excluded
		exclude_types (List): nodes types in this list will be excluded
		return_mode (str): modifies return value:
			"all" : returns a dictionary with incoming and outgoing keys
			"incoming": returns a list of dictionaries for incoming connections
			"outgoing": returns a list of dictionaries for outgoing connections
			defaults to "all"
	Returns: (Dictionary) or (List)
	"""

    raw_inputs = cmds.listConnections(node,
                                      plugs=True,
                                      source=True,
                                      destination=False,
                                      connections=True)
    raw_outputs = cmds.listConnections(node,
                                       plugs=True,
                                       source=False,
                                       destination=True,
                                       connections=True)
    input_plugs = raw_inputs[::2] if raw_inputs else []
    output_plugs = raw_outputs[::2] if raw_outputs else []
    result_dict = {"incoming": [], "outgoing": []}

    # filter input plug lists
    if exclude_nodes:
        input_plugs = [
            plug for plug in input_plugs
            if plug.split(".")[0] not in exclude_nodes]
    if exclude_types:
        input_plugs = [
            plug for plug in input_plugs if cmds.objectType(
                plug.split(".")[0]) not in exclude_types]

    for in_plug in input_plugs:
        conn = {
            "plug_out": cmds.listConnections(in_plug,
                                             plugs=True,
                                             source=True,
                                             destination=False,
                                             connections=True)[0],
            "plug_in": cmds.listConnections(in_plug,
                                            plugs=True,
                                            source=True,
                                            destination=False,
                                            connections=True)[1]
        }
        result_dict["incoming"].append(conn)

    for out_plug in output_plugs:
        out_connections = cmds.listConnections(out_plug,
                                               plugs=True,
                                               source=False,
                                               destination=True,
                                               connections=False)
        for out_c in out_connections:
            if exclude_nodes:
                if out_c.split(".")[0] in exclude_nodes:
                    continue
            if exclude_types:
                if cmds.objectType(out_c.split(".")[0]) in exclude_types:
                    continue
            conn = {
                "plug_out": out_plug,
                "plug_in": out_c
            }
            result_dict["outgoing"].append(conn)

    if return_mode == "all":
        return result_dict
    elif return_mode == "incoming":
        return result_dict["incoming"]
    elif return_mode == "outgoing":
        return result_dict["outgoing"]
    else:
        raise Exception("Not valid return_mode argument."
                        "Valid values are 'all', 'incoming', 'outgoing'")


def disconnect_attr(node=None, attr=None, suppress_warnings=False):
    """Disconnects all INCOMING connections to the attribute"""
    if len(node.split(".")) < 2:
        if not attr:
            cmds.error("You need to provide node=<node> and attr=<attr> or node=<node>.<attr>")
            return
        attr_path = "%s.%s" % (node, attr)
    else:
        attr_path = node
    plug = cmds.listConnections(attr_path, source=True, plugs=True)

    if plug:
        cmds.disconnectAttr(plug[0], attr_path)
    else:
        if not suppress_warnings:
            cmds.warning("Nothing connected to this attribute => %s" % attr_path)
        else:
            pass


def uvPin_generate(deformed_mesh, original_mesh, coordinates, follicList, type="mesh", uv_pin=None):
    """

    :param follicList:
    :param type:
    :param deformed_mesh:
    :param original_mesh:
    :param coordinates:
    :param uv_pin:
    :return:
    """

    if uv_pin:
        uv_pin_node = uv_pin
        out_matrix_list = cmds.listAttr(uv_pin + ".outputMatrix", m=1)

        numberList = [int(re.search(r'\d+', s).group()) for s in out_matrix_list if
                      cmds.listConnections("%s.%s" % (uv_pin, s), s=0, d=1) if out_matrix_list]

        max_num = max(numberList)
        [cmds.setAttr("%s.coordinate[%d]" % (uv_pin_node, i + max_num + 1), *coordinates[i]) for i in
         range(len(coordinates))]

        for i, follic in enumerate(follicList):
            print("%s.outputMatrix[%d]" % (uv_pin_node, i + max_num + 1), "%s.offsetParentMatrix" % follic)
        [cmds.connectAttr("%s.outputMatrix[%d]" % (uv_pin_node, i + max_num + 1), "%s.offsetParentMatrix" % follic) for
         i, follic in enumerate(follicList)]

    else:
        uv_pin_node = cmds.createNode("uvPin")

        if type == "mesh":
            cmds.connectAttr("{}.worldMesh".format(deformed_mesh),
                             "{}.deformedGeometry".format(uv_pin_node))
            cmds.connectAttr("{}.outMesh".format(original_mesh),
                             "{}.originalGeometry".format(uv_pin_node))
        elif type == "nurbsSurface":
            cmds.connectAttr("{}.worldSpace[0]".format(deformed_mesh),
                             "{}.deformedGeometry".format(uv_pin_node))
            cmds.connectAttr("{}.local".format(original_mesh),
                             "{}.originalGeometry".format(uv_pin_node))

        [cmds.setAttr("%s.coordinate[%d]" % (uv_pin_node, i), *coordinates[i]) for i in range(len(coordinates))]

        [cmds.connectAttr("%s.outputMatrix[%d]" % (uv_pin_node, i), "%s.offsetParentMatrix" % follic) for i, follic in
         enumerate(follicList)]

    return uv_pin_node


def create_and_process_planes(rivet_mesh, rivets):
    created_planes = []
    merged = None
    try:
        # 1. 在每个选中物体的位置创建polyPlane
        for obj in rivets:
            # 获取物体的世界空间位置
            pos = cmds.xform(obj, query=True, translation=True, worldSpace=True)

            # 创建平面（默认大小1x1，可根据需要调整）
            plane = cmds.polyPlane(width=0.1, height=0.1, ax=(0, 0, 1), subdivisionsX=1, subdivisionsY=1)[0]

            # 将平面移动到选中物体的位置
            cmds.xform(plane, translation=pos, worldSpace=True)

            created_planes.append(plane)

        # 2. 合并所有创建的平面
        if len(created_planes) > 1:
            merged = cmds.polyUnite(created_planes, ch=False)[0]
        else:
            merged = created_planes[0]

        # 3. 自动分UV
        cmds.polyAutoProjection(merged, ch=False)

        # 4. 删除历史记录
        cmds.delete(merged, constructionHistory=True)

        # 5. 冻结变换（重置坐标）
        cmds.makeIdentity(merged, apply=True, translate=True, rotate=True, scale=True)

    except Exception as e:
        cmds.warning(u"操作失败: {}".format(e))
    if merged:
        version = int(cmds.about(version=True))
        if version >= 2023:
            merged = cmds.rename(merged, "{}_rivet_plane".format(rivet_mesh))
            proxy_wrap = cmds.proximityWrap([merged])[0]
            cmds.proximityWrap(proxy_wrap, edit=True, addDrivers=[rivet_mesh])
    return merged


def uvPin(mesh_transform, coordinates, follicList, type="mesh"):
    """

    :param follicList:
    :param mesh_transform:
    :param coordinates:
    :param type:
    :return:
    """
    assert cmds.about(api=True) >= 20200000, "uv_pin requires Maya 2020 and later!"

    all_shapes = cmds.listRelatives(mesh_transform,
                                    shapes=True,
                                    children=True,
                                    parent=False)
    # separate intermediates
    intermediates = [x for x in all_shapes
                     if cmds.getAttr("{}.intermediateObject".format(x)) == 1]
    non_intermediates = [x for x in all_shapes if x not in intermediates]
    deformed_mesh = non_intermediates[0]
    if not intermediates:
        # create original / deformed mesh hiearchy
        dup = cmds.duplicate(mesh_transform,
                             name="{}_ORIG".format(mesh_transform))[0]
        original_mesh = cmds.listRelatives(dup, children=True)[0]
        cmds.parent(original_mesh, mesh_transform, shape=True, r=True)
        cmds.delete(dup)
        incoming_connections = connections(deformed_mesh)["incoming"]
        for connection in incoming_connections:
            disconnect_attr(connection["plug_out"])
            cmds.connectAttr(connection["plug_in"],
                             connection["plug_out"].replace(
                                 deformed_mesh, original_mesh))
        # hide/intermediate original mesh
        cmds.setAttr("%s.hiddenInOutliner" % original_mesh, 1)
        cmds.setAttr("%s.intermediateObject" % original_mesh, 1)
        refresh_outliner()
    else:
        original_mesh = intermediates[0]

    connection_nodes = None
    uv_pin_node = None

    if type == "mesh":
        connection_nodes = cmds.listConnections(deformed_mesh + ".worldMesh[0]", s=0, d=1)
    elif type == "nurbsSurface":
        connection_nodes = cmds.listConnections(deformed_mesh + ".worldSpace[0]", s=0, d=1)

    # find exists uvPin nodes
    if connection_nodes:
        for node in connection_nodes:
            if cmds.objectType(node) == "uvPin":
                uv_pin_node = uvPin_generate(deformed_mesh, original_mesh, coordinates, follicList, type, uv_pin=node)
                return uv_pin_node
            else:
                uv_pin_node = uvPin_generate(deformed_mesh, original_mesh, coordinates, follicList, type, uv_pin=None)
    else:
        uv_pin_node = uvPin_generate(deformed_mesh, original_mesh, coordinates, follicList, type, uv_pin=None)

    return uv_pin_node


def get_uv_at_point(position, dest_node):
    """Get a tuple of u, v values for a point on a given mesh.

	Args:
		position (vector3): The world space position to get the uvs of.
		dest_node (str): The mesh with uvs.

	Returns:
		tuple: (float, float) The U and V values.
	"""
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(dest_node)
    dag_path = selection_list.getDagPath(0)

    mfn_mesh = OpenMaya.MFnMesh(dag_path)

    point = OpenMaya.MPoint(position)
    space = OpenMaya.MSpace.kWorld

    u_val, v_val, _ = mfn_mesh.getUVAtPoint(point, space)

    return u_val, v_val


def get_uv_at_surface(node, dest_node):
    """

    :param node:
    :param dest_node:
    :return:
    """
    grp = cmds.group(em=True)
    parentConstraint(node, grp, mo=False)
    closest_PointNode = cmds.createNode("closestPointOnSurface")
    cmds.connectAttr(grp + '.translateX', closest_PointNode + '.inPosition.inPositionX')
    cmds.connectAttr(grp + '.translateY', closest_PointNode + '.inPosition.inPositionY')
    cmds.connectAttr(grp + '.translateZ', closest_PointNode + '.inPosition.inPositionZ')
    cmds.connectAttr(dest_node + ".local", closest_PointNode + ".inputSurface")
    minMaxRangeU = int(cmds.getAttr(dest_node + '.minMaxRangeU')[0][1])
    minMaxRangeV = int(cmds.getAttr(dest_node + '.minMaxRangeV')[0][1])
    U = cmds.getAttr(closest_PointNode + '.result.parameterU') / minMaxRangeU
    V = cmds.getAttr(closest_PointNode + '.result.parameterV') / minMaxRangeV
    cmds.delete([closest_PointNode, grp])
    return U, V


def pin_to_surface(node, surface, sr="", st="", ss="xyz"):
    """

    :param node:
    :param surface:
    :param sr:
    :param st:
    :param ss:
    :return:
    """
    uv_coordinates = get_uv_at_surface(node, surface)
    _uv_pin = uvPin(surface, [uv_coordinates], follicList=[node], type="nurbsSurface")
    # decompose_matrix_node = cmds.createNode("decomposeMatrix",
    #                                         name="decompose_pinMatrix")
    # cmds.connectAttr("{}.outputMatrix[0]".format(_uv_pin),
    #                  "{}.inputMatrix".format(decompose_matrix_node))
    #
    # for attr in "XYZ":
    #     if attr.lower() not in sr and attr.upper() not in sr:
    #         cmds.connectAttr("{0}.outputRotate{1}".format(
    #             decompose_matrix_node, attr),
    #             "{0}.rotate{1}".format(node, attr))
    #
    # for attr in "XYZ":
    #     if attr.lower() not in st and attr.upper() not in st:
    #         cmds.connectAttr("{0}.outputTranslate{1}".format(
    #             decompose_matrix_node, attr),
    #             "{0}.translate{1}".format(node, attr))
    #
    # for attr in "XYZ":
    #     if attr.lower() not in ss and attr.upper() not in ss:
    #         cmds.connectAttr("{0}.outputScale{1}".format(
    #             decompose_matrix_node, attr),
    #             "{0}.scale{1}".format(node, attr))

    return _uv_pin


def refresh_outliner():
    """Refresh the Maya outliner"""
    eds = cmds.lsUI(editors=True)
    for ed in eds:
        if cmds.outlinerEditor(ed, exists=True):
            cmds.outlinerEditor(ed, e=True, refresh=True)


def createJointChainByCurve(curve, jntPrefix, rigPrefix, jointNumber):
    """
    :param jointNumber:
    :param curve:
    :param jntPrefix:
    :param jntPrefix:
    :param rigPrefix:
    :return:
    """
    jointChainList = []
    cvPosList = [pm.xform(cv, q=1, t=1, ws=1) for cv in curve.cv]
    param = curve.getParamAtPoint(cvPosList[-1])

    for i in range(jointNumber):
        # 计算当前距离
        current_param = i * (param / (jointNumber - 1))
        # 计算当前距离在曲线上的位置
        current_pos = curve.getPointAtParam(current_param, space='world')
        jnt = joint(p=current_pos, name="%s_0%d_%s_jnt" % (rigPrefix, i, jntPrefix))
        jointChainList.append(jnt)
    return jointChainList


def calculateJointAxis(jntList, aimAxis, upAxis, plane=False):
    """
    骨骼校轴
    :param plane:
    :param jntList: joint list
    :param aimAxis: aim Axis of the chain
    :param upAxis: upAxis of the chain
    :return:
    """
    # 先把每个骨骼p出来
    [parent(jnt, w=True) for jnt in jntList]
    upVecs = []
    if plane:
        for i, jnt in enumerate(jntList):
            position = jnt.getTranslation(space="world")
            u, v = plane.getParamAtPoint(position)
            uTang, vTang = plane.getTangents(u, v, space="world")
            upVecs.append(vTang ^ uTang)
    for i in range(len(jntList) - 1):
        # do the aimConstraint
        if plane:
            delete(aimConstraint(jntList[i + 1], jntList[i], aimVector=aimAxis, upVector=upAxis,
                                 worldUpType="vector", worldUpVector=upVecs[i]))
        else:
            delete(aimConstraint(jntList[i + 1], jntList[i], aimVector=aimAxis, upVector=upAxis,
                                 worldUpType="objectrotation", worldUpObject=jntList[i + 1]))
        makeIdentity(jntList[i], apply=True, r=True)
    # 再p回去
    [parent(jntList[i + 1], jntList[i]) for i in range(len(jntList) - 1)]
    jntList[-1].jointOrient.set(0, 0, 0)


def spineStretchSoftCmd(bridge, crv, prefix, count):
    if not objExists(bridge):
        return False

    crv_info = cmds.shadingNode("curveInfo", asUtility=True, name=crv + "_crvInfo")
    cmds.connectAttr(crv + ".worldSpace[0]", crv_info + ".inputCurve")
    # crv.worldSpace[0] >> crv_info.inputCurve

    # soft val
    # soft_val_condition = node.if_else(bridge + ".softness",
    #                                   0,
    #                                   second_term,
    #                                   if_true,
    #                                   if_false,
    #                                   return_plug=True,
    #                                   name="condition", )
    soft_val_condition = shadingNode("condition", asUtility=True, name=prefix + "_soft_val_condition")
    soft_val_condition.operation.set(0)
    bridge.softness >> soft_val_condition.firstTerm
    soft_val_condition.colorIfTrueR.set(0.001)
    bridge.softness >> soft_val_condition.colorIfFalseR

    # stretch ==================================================================================
    sl_stretch_mult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sl_stretch_mult")
    bridge.slave_length >> sl_stretch_mult.input1
    bridge.maxstretch >> sl_stretch_mult.input2

    activeLengthMinus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_activeLengthMinus")
    activeLengthMinus.operation.set(2)
    crv_info.arcLength >> activeLengthMinus.input1D[0]
    bridge.master_length >> activeLengthMinus.input1D[1]

    stretch = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_stretch")
    stretch.operation.set(2)
    activeLengthMinus.output1D >> stretch.input1X
    sl_stretch_mult.output >> stretch.input2X

    neg_stretch = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_neg_stretch")
    neg_stretch.input1.set(-1)
    stretch.outputX >> neg_stretch.input2

    stretch_soft_div = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_stretch_soft_div")
    stretch_soft_div.operation.set(2)
    neg_stretch.output >> stretch_soft_div.input1X
    soft_val_condition.outColorR >> stretch_soft_div.input2X

    stretch_soft_pow = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_stretch_soft_pow")
    stretch_soft_pow.operation.set(3)
    stretch_soft_pow.input1X.set(2.718)
    stretch_soft_div.outputX >> stretch_soft_pow.input2X

    expo_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_expo_minus")
    expo_minus.operation.set(2)
    expo_minus.input1D[0].set(1)
    stretch_soft_pow.outputX >> expo_minus.input1D[1]

    stretch_expo_condition = shadingNode("condition", asUtility=True, name=prefix + "_stretch_expo_condition")
    stretch_expo_condition.operation.set(0)
    soft_val_condition.outColorR >> stretch_expo_condition.firstTerm
    expo_minus.output1D >> stretch_expo_condition.colorIfFalseR
    stretch_expo_condition.colorIfTrueR.set(1.0)

    stretch_val = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_stretch_val")
    stretch_val.operation.set(2)
    bridge.maxstretch >> stretch_val.input1D[0]
    stretch_val.input1D[1].set(1)

    sl_stretch_mult_a = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sl_stretch_mult_a")
    bridge.slave_length >> sl_stretch_mult_a.input1
    stretch_val.output1D >> sl_stretch_mult_a.input2

    sl_val_after = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sl_val_after")
    sl_stretch_mult_a.output >> sl_val_after.input1
    stretch_expo_condition.outColorR >> sl_val_after.input2

    st_ext_condition = shadingNode("condition", asUtility=True, name=prefix + "_st_ext_condition")
    st_ext_condition.operation.set(4)
    sl_val_after.output >> st_ext_condition.firstTerm
    activeLengthMinus.output1D >> st_ext_condition.secondTerm
    sl_val_after.output >> st_ext_condition.colorIfTrueR
    activeLengthMinus.output1D >> st_ext_condition.colorIfFalseR

    in_sl_stretch = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_in_sl_stretch")
    st_ext_condition.outColorR >> in_sl_stretch.input1D[0]
    bridge.slave_length >> in_sl_stretch.input1D[1]

    # squash ==================================================================================
    negtiveLengthMinus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_negtiveLengthMinus")
    negtiveLengthMinus.operation.set(2)
    bridge.master_length >> negtiveLengthMinus.input1D[0]
    crv_info.arcLength >> negtiveLengthMinus.input1D[1]

    sl_squash_mult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sl_squash_mult")
    bridge.slave_length >> sl_squash_mult.input1
    bridge.maxsquash >> sl_squash_mult.input2

    squash = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_squash")
    squash.operation.set(2)
    negtiveLengthMinus.output1D >> squash.input1X
    sl_squash_mult.output >> squash.input2X

    neg_squash = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_neg_squash")
    neg_squash.input1.set(-1)
    squash.outputX >> neg_squash.input2

    squash_soft_div = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_squash_soft_div")
    squash_soft_div.operation.set(2)
    neg_squash.output >> squash_soft_div.input1X
    soft_val_condition.outColorR >> squash_soft_div.input2X

    squash_soft_pow = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_squash_soft_pow")
    squash_soft_pow.operation.set(3)
    squash_soft_pow.input1X.set(2.718)
    squash_soft_div.outputX >> squash_soft_pow.input2X

    expo_minus1 = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_expo_minus1")
    expo_minus1.operation.set(2)
    expo_minus1.input1D[0].set(1)
    squash_soft_pow.outputX >> expo_minus1.input1D[1]

    squash_expo_condition = shadingNode("condition", asUtility=True, name=prefix + "_squash_expo_condition")
    squash_expo_condition.operation.set(0)
    squash_expo_condition.colorIfTrueR.set(1.0)
    bridge.softness >> squash_expo_condition.firstTerm
    expo_minus1.output1D >> squash_expo_condition.colorIfFalseR

    squash_val = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_squash_val")
    squash_val.operation.set(2)
    squash_val.input1D[0].set(1)
    bridge.maxsquash >> squash_val.input1D[1]

    sl_squash_mult_a = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sl_squash_mult_a")
    bridge.slave_length >> sl_squash_mult_a.input1
    squash_val.output1D >> sl_squash_mult_a.input2

    squash_sl_val_after = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_squash_sl_val_after")
    squash_expo_condition.outColorR >> squash_sl_val_after.input1
    sl_squash_mult_a.output >> squash_sl_val_after.input2

    sq_ext_condition = shadingNode("condition", asUtility=True, name=prefix + "_sq_ext_condition")
    sq_ext_condition.operation.set(4)
    squash_sl_val_after.output >> sq_ext_condition.firstTerm
    negtiveLengthMinus.output1D >> sq_ext_condition.secondTerm
    negtiveLengthMinus.output1D >> sq_ext_condition.colorIfFalseR
    squash_sl_val_after.output >> sq_ext_condition.colorIfTrueR

    in_sl_squash = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_in_sl_squash")
    in_sl_squash.operation.set(2)
    bridge.slave_length >> in_sl_squash.input1D[0]
    sq_ext_condition.outColorR >> in_sl_squash.input1D[1]

    # **************************************************************************************************
    in_sl_condition = shadingNode("condition", asUtility=True, name=prefix + "_in_sl_condition")
    in_sl_condition.operation.set(3)
    crv_info.arcLength >> in_sl_condition.firstTerm
    bridge.master_length >> in_sl_condition.secondTerm
    in_sl_squash.output1D >> in_sl_condition.colorIfFalseR
    in_sl_stretch.output1D >> in_sl_condition.colorIfTrueR

    size = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_size")
    size.operation.set(2)
    in_sl_condition.outColorR >> size.input1X
    crv_info.arcLength >> size.input2X

    size_plus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_size_plus")
    size_plus.operation.set(2)
    size_plus.input1D[0].set(1)
    size.outputX >> size_plus.input1D[1]

    start = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_start")
    bridge.position >> start.input1
    size_plus.output1D >> start.input2

    end = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_end")
    start.output >> end.input1D[0]
    size.outputX >> end.input1D[1]

    start_end_length = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_start_end_length")
    start_end_length.operation.set(2)
    end.output1D >> start_end_length.input1D[0]
    start.output >> start_end_length.input1D[1]

    step = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_step")
    step.operation.set(2)
    start_end_length.output1D >> step.input1X
    step.input2X.set(int(count - 1))

    pciList = []
    for i in range(count):
        step_mult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_step_mult" + str(i))
        step_mult.input1.set(i)
        step.outputX >> step_mult.input2

        perc = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_per" + str(i))
        start.output >> perc.input1D[0]
        step_mult.output >> perc.input1D[1]

        perc_clamp = shadingNode("clamp", asUtility=True, name=prefix + "_perc_clamp" + str(i))
        perc_clamp.maxR.set(1)
        perc.output1D >> perc_clamp.inputR

        pci = createNode("pointOnCurveInfo", name=prefix + "_pci" + str(i))
        crv.worldSpace[0] >> pci.inputCurve
        perc_clamp.outputR >> pci.parameter
        pci.turnOnPercentage.set(1)
        pciList.append(pci)

    return pciList


def spineVolumeCmd(bridge, prefix, outObj):  # todo: 创建脊椎拉伸
    # in st----------------------------------------------------------------------------------------
    driver_ctrl_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_dc_minus")
    driver_ctrl_minus.operation.set(2)
    bridge.driver >> driver_ctrl_minus.input1D[0]
    bridge.driver_ctr >> driver_ctrl_minus.input1D[1]

    driver_ctrl_max = shadingNode("condition", asUtility=True, name=prefix + "_dc_max")
    driver_ctrl_minus.output1D >> driver_ctrl_max.firstTerm
    driver_ctrl_max.operation.set(2)
    driver_ctrl_max.colorIfFalseR.set(0)
    driver_ctrl_minus.output1D >> driver_ctrl_max.colorIfTrueR

    max_ctrl_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_mc_minus")
    max_ctrl_minus.operation.set(2)
    bridge.driver_max >> max_ctrl_minus.input1D[0]
    bridge.driver_ctr >> max_ctrl_minus.input1D[1]

    max_ctrl_max = shadingNode("condition", asUtility=True, name=prefix + "_mc_max")
    max_ctrl_minus.output1D >> max_ctrl_max.firstTerm
    max_ctrl_max.operation.set(2)
    max_ctrl_max.secondTerm.set(0.001)
    max_ctrl_max.colorIfFalseR.set(0.001)
    max_ctrl_minus.output1D >> max_ctrl_max.colorIfTrueR

    ctrl_max_div = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_cm_div")
    ctrl_max_div.operation.set(2)
    driver_ctrl_max.outColorR >> ctrl_max_div.input1X
    max_ctrl_max.outColorR >> ctrl_max_div.input2X

    cm_clamp = shadingNode("clamp", asUtility=True, name=prefix + "_cm_clamp")
    cm_clamp.maxR.set(1)
    ctrl_max_div.outputX >> cm_clamp.inputR

    in_st = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_in_st")
    bridge.stretch >> in_st.input1
    cm_clamp.outputR >> in_st.input2

    # in sq---------------------------------------------------------------------------------------------
    ctrl_driver_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_cd_minus")
    ctrl_driver_minus.operation.set(2)
    bridge.driver_ctr >> ctrl_driver_minus.input1D[0]
    bridge.driver >> ctrl_driver_minus.input1D[1]

    ctrl_driver_max = shadingNode("condition", asUtility=True, name=prefix + "_cd_max")
    ctrl_driver_minus.output1D >> ctrl_driver_max.firstTerm
    ctrl_driver_max.operation.set(2)
    ctrl_driver_max.colorIfFalseR.set(0.001)
    ctrl_driver_minus.output1D >> ctrl_driver_max.colorIfTrueR

    ctrl_min_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_cm_minus")
    ctrl_min_minus.operation.set(2)
    bridge.driver_ctr >> ctrl_min_minus.input1D[0]
    bridge.driver_min >> ctrl_min_minus.input1D[1]

    min_ctrl_max = shadingNode("condition", asUtility=True, name=prefix + "_mic_max")
    ctrl_min_minus.output1D >> min_ctrl_max.firstTerm
    min_ctrl_max.operation.set(2)
    min_ctrl_max.secondTerm.set(0.001)
    min_ctrl_max.colorIfFalseR.set(0.001)
    ctrl_min_minus.output1D >> min_ctrl_max.colorIfTrueR

    ctrl_min_div = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_cmi_div")
    ctrl_min_div.operation.set(2)
    ctrl_driver_max.outColorR >> ctrl_min_div.input1X
    min_ctrl_max.outColorR >> ctrl_min_div.input2X

    cmi_clamp = shadingNode("clamp", asUtility=True, name=prefix + "_cmi_clamp")
    cmi_clamp.maxR.set(1)
    ctrl_min_div.outputX >> cmi_clamp.inputR

    in_sq = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_in_sq")
    cmi_clamp.outputR >> in_sq.input1
    bridge.squash >> in_sq.input2

    qt_plus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_sqst_plus")
    qt_plus.input1D[0].set(1)
    in_st.output >> qt_plus.input1D[1]
    in_sq.output >> qt_plus.input1D[2]

    scale_condition = shadingNode("condition", asUtility=True, name=prefix + "_scale_condition")
    scale_condition.operation.set(2)
    qt_plus.output1D >> scale_condition.firstTerm
    qt_plus.output1D >> scale_condition.colorIfTrueR

    sxMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sx_mult")
    bridge.global_scaleX >> sxMult.input1
    scale_condition.outColorR >> sxMult.input2

    syMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sy_mult")
    bridge.global_scaleY >> syMult.input1
    scale_condition.outColorR >> syMult.input2

    szMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_sz_mult")
    bridge.global_scaleZ >> szMult.input1
    scale_condition.outColorR >> szMult.input2

    x_condition = shadingNode("condition", asUtility=True, name=prefix + "_x_condition")
    x_condition.operation.set(1)
    bridge.axis >> x_condition.firstTerm
    sxMult.output >> x_condition.colorIfTrueR
    bridge.global_scaleX >> x_condition.colorIfFalseR

    y_condition = shadingNode("condition", asUtility=True, name=prefix + "_y_condition")
    y_condition.operation.set(1)
    y_condition.secondTerm.set(1)
    bridge.axis >> y_condition.firstTerm
    syMult.output >> y_condition.colorIfTrueR
    bridge.global_scaleY >> y_condition.colorIfFalseR

    z_condition = shadingNode("condition", asUtility=True, name=prefix + "_z_condition")
    z_condition.operation.set(1)
    z_condition.secondTerm.set(2)
    bridge.axis >> z_condition.firstTerm
    szMult.output >> z_condition.colorIfTrueR
    bridge.global_scaleY >> z_condition.colorIfFalseR

    x_blendMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_x_blendMult")
    x_condition.outColorR >> x_blendMult.input1
    bridge.blend >> x_blendMult.input2

    y_blendMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_y_blendMult")
    y_condition.outColorR >> y_blendMult.input1
    bridge.blend >> y_blendMult.input2

    z_blendMult = shadingNode("multDoubleLinear", asUtility=True, name=prefix + "_z_blendMult")
    z_condition.outColorR >> z_blendMult.input1
    bridge.blend >> z_blendMult.input2

    blend_minus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_blend_minus")
    blend_minus.operation.set(2)
    blend_minus.input1D[0].set(1)
    bridge.blend >> blend_minus.input1D[1]

    blendScl_mult = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_blendScl_mult")
    bridge.global_scaleX >> blendScl_mult.input1X
    bridge.global_scaleY >> blendScl_mult.input1Y
    bridge.global_scaleZ >> blendScl_mult.input1Z

    blend_minus.output1D >> blendScl_mult.input2X
    blend_minus.output1D >> blendScl_mult.input2Y
    blend_minus.output1D >> blendScl_mult.input2Z

    scale_plus = shadingNode("plusMinusAverage", asUtility=True, name=prefix + "_scale_plus")
    x_blendMult.output >> scale_plus.input3D[0].input3Dx
    y_blendMult.output >> scale_plus.input3D[0].input3Dy
    z_blendMult.output >> scale_plus.input3D[0].input3Dz
    blendScl_mult.outputX >> scale_plus.input3D[1].input3Dx
    blendScl_mult.outputY >> scale_plus.input3D[1].input3Dy
    blendScl_mult.outputZ >> scale_plus.input3D[1].input3Dz

    global_div = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_global_div")
    global_div.operation.set(2)
    global_div.input1X.set(1)
    global_div.input1Y.set(1)
    global_div.input1Z.set(1)
    bridge.global_scaleX >> global_div.input1X
    bridge.global_scaleY >> global_div.input1Y
    bridge.global_scaleZ >> global_div.input1Z

    scale_out = shadingNode("multiplyDivide", asUtility=True, name=prefix + "_scl_out")
    scale_plus.output3D >> scale_out.input1
    global_div.output >> scale_out.input2

    scale_out.output >> outObj.scale

    scaleValue = scale_out.output.get()
    return scaleValue


def AttrSet(ObjattrDatadic):
    """
    attrDatadic = {obj.Attr:data,obj.Attr:data}
    """
    for objattr in ObjattrDatadic:
        Data = ObjattrDatadic.get(objattr)
        cmds.setAttr(objattr, Data)


def GrpAdd(Obj, GrpNames, addgrpRelativeTier):
    """
    Add Grp
    :param Obj:
    :param GrpNames:
    :param addgrpRelativeTier:
    :return:
    """
    objParent = cmds.listRelatives(Obj, p=True, f=True)
    GrpNames = GrpNames[::-1]
    Grps = []
    GrpDict = dict()
    for grp in GrpNames:
        if cmds.objExists(grp):
            cmds.warning(grp + '------ is exists')
        if grp == GrpNames[0]:
            grp = cmds.group(em=True)
            Grps.append(grp)
        else:
            grp = cmds.group()
            Grps.append(grp)

    Grps = Grps[::-1]
    topGrp = Grps[0]
    EndGrp = Grps[-1]
    cmds.parent(topGrp, Obj)
    AttrSet({topGrp + '.rx': 0,
             topGrp + '.ry': 0,
             topGrp + '.rz': 0,
             topGrp + '.tx': 0,
             topGrp + '.ty': 0,
             topGrp + '.tz': 0,
             topGrp + '.sx': 1,
             topGrp + '.sy': 1,
             topGrp + '.sz': 1})
    if addgrpRelativeTier == 'Up':
        cmds.parent(topGrp, w=True)
        if objParent:
            cmds.parent(topGrp, objParent[0])
        cmds.parent(Obj, EndGrp)
    elif addgrpRelativeTier == 'Dn':
        pass
    Grps = list(reversed(Grps))
    cmds.select(Grps, add=True)
    reGrps = list(reversed([cmds.rename(Grps[i], GrpNames[i]) for i in range(len(Grps))]))

    for i, grp in enumerate(list(reversed(reGrps))):
        GrpDict[GrpNames[i].split("_")[-1]] = grp

    return GrpDict, topGrp, EndGrp


def setDrivenKey(driver, driven, driverNums, drivenNums, itt, ott):
    """
    set driven key
    :param driver:
    :param driven:
    :param driverNums:
    :param drivenNums:
    :param itt:
    :param ott:
    :return:
    """
    driverSplit = driver.split('.')
    driverAttr = ''
    for x, Attr in enumerate(driverSplit[1:]):
        if x == 0:
            driverAttr = Attr
        else:
            driverAttr = driverAttr + '.' + Attr

    drivenSplit = driven.split('.')
    drivenAttr = ''
    for x, Attr in enumerate(drivenSplit[1:]):
        if x == 0:
            drivenAttr = Attr
        else:
            drivenAttr = drivenAttr + '.' + Attr

    [setDrivenKeyframe(driven, currentDriver=driver, driverValue=driverNums[i], v=drivenNums[i],
                       itt=itt, ott=ott) for i in range(len(driverNums))]


def createSinCosAttr(objList, name, addAttrObj, Axis):
    """

    :param objList:
    :param name:
    :param addAttrObj:
    :param Axis:
    :return:
    """
    maya_version = int(cmds.about(version=True))
    nodeList = []
    ObjNumber = len(objList)
    AttrPrefix = Axis[0] + Axis[-1]

    waveAttName = '____________' + AttrPrefix
    EnumName = AttrPrefix + '_wave'
    attribute.addEnumAttribute(addAttrObj, waveAttName, 0, [EnumName], keyable=True, lock=True)

    EnvelopeAttName = AttrPrefix + '_Envelope'
    attribute.addAttributes(addAttrObj, EnvelopeAttName, "double", value=0, min=0, max=1, keyable=True)
    Envelope = PyNode(addAttrObj + "." + EnvelopeAttName)

    AmplitudeAttName = AttrPrefix + '_Amplitude'
    attribute.addAttributes(addAttrObj, AmplitudeAttName, "double", value=5, keyable=True)
    Amplitude = PyNode(addAttrObj + "." + AmplitudeAttName)

    WavelengthAttName = AttrPrefix + '_Wavelength'
    attribute.addAttributes(addAttrObj, WavelengthAttName, "double", value=10, keyable=True)
    Wavelength = PyNode(addAttrObj + "." + WavelengthAttName)

    WaveFollowAttName = AttrPrefix + '_WaveFollow'
    attribute.addAttributes(addAttrObj, WaveFollowAttName, "double", value=0, keyable=True)
    WaveFollow = PyNode(addAttrObj + "." + WaveFollowAttName)

    StartingPositionAttName = AttrPrefix + '_StartingPosition'
    attribute.addAttributes(addAttrObj, StartingPositionAttName, "double", value=0, min=0, max=ObjNumber, keyable=True)
    StartingPosition = PyNode(addAttrObj + "." + StartingPositionAttName)

    StartingreversalAttName = AttrPrefix + '_reversal'
    attribute.addAttributes(addAttrObj, StartingreversalAttName, "double", value=1, min=-1, max=1, keyable=True)
    Startingreversal = PyNode(addAttrObj + "." + StartingreversalAttName)

    if ObjNumber == 1:
        averageNum = 1
    else:
        averageNum = 1.0 / (ObjNumber - 1)
    expressionStr = ''
    for x in range(ObjNumber):
        StartingPosition_PMA01 = shadingNode('plusMinusAverage', asUtility=True,
                                             name=name + '_' + Axis + '_StartingPosition0' + str(x) + '_PMA01')
        nodeList.append(StartingPosition_PMA01)
        StartingPosition_PMA01.operation.set(1)
        StartingPosition_PMA01.input2D[0].input2Dx.set(ObjNumber - 1 - x)
        StartingPosition >> StartingPosition_PMA01.input2D[1].input2Dx

        setDrivenKey(Startingreversal, StartingPosition_PMA01 + '.input2D[0].input2Dx', [1, -1], [ObjNumber - 1 - x, x],
                     'linear', 'linear')

        StartingPosition_SR = shadingNode('setRange', asUtility=True,
                                          name=name + '_' + Axis + '_StartingPosition0' + str(
                                              x) + '_setRange')
        nodeList.append(StartingPosition_SR)
        StartingPosition_SR.maxX.set(1)
        StartingPosition_SR.oldMaxX.set(ObjNumber)
        StartingPosition_PMA01.output2Dx >> StartingPosition_SR.valueX

        StartingPosition_PMA02 = shadingNode('plusMinusAverage', asUtility=True,
                                             name=name + '_' + Axis + '_StartingPosition0' + str(
                                                 x) + '_PMA02')
        nodeList.append(StartingPosition_PMA02)
        StartingPosition_PMA02.operation.set(2)
        StartingPosition_PMA02.input2D[0].input2Dx.set(1)
        StartingPosition_SR.outValueX >> StartingPosition_PMA02.input2D[1].input2Dx

        Envelope_MD = shadingNode('multiplyDivide', asUtility=True,
                                  name=name + '_' + Axis + '_Envelope0' + str(x) + '_MD')
        nodeList.append(Envelope_MD)
        Envelope >> Envelope_MD.input1X
        StartingPosition_PMA02.output2Dx >> Envelope_MD.input2X

        Amplitude_MD = shadingNode('multiplyDivide', asUtility=True,
                                   name=name + '_' + Axis + '_Amplitude0' + str(x) + '_MD')
        nodeList.append(Amplitude_MD)
        Amplitude >> Amplitude_MD.input1X
        Envelope_MD.outputX >> Amplitude_MD.input2X

        result_MD = shadingNode('multiplyDivide', asUtility=True,
                                name=name + '_' + Axis + '_result0' + str(x) + '_MD')
        nodeList.append(result_MD)
        Amplitude_MD.outputX >> result_MD.input1X
        connectAttr(result_MD.outputX, objList[x] + '.' + Axis)

        Wavelength_MD = shadingNode('multiplyDivide', asUtility=True,
                                    name=name + '_' + Axis + '_Wavelength0' + str(x) + '_MD')
        nodeList.append(Wavelength_MD)
        Wavelength >> Wavelength_MD.input1.input1X
        Wavelength_MD.input2X.set(averageNum * x)
        WaveFollow_MD = shadingNode('multiplyDivide', asUtility=True,
                                    name=name + '_' + Axis + '_WaveFollow0' + str(x) + '_MD')
        nodeList.append(WaveFollow_MD)
        WaveFollow >> WaveFollow_MD.input1.input1X
        WaveFollow_MD.input2X.set(-1)

        sine_PMA = shadingNode('plusMinusAverage', asUtility=True,
                               name=name + '_' + Axis + '_sine0' + str(x) + '_PMA')
        nodeList.append(sine_PMA)
        Wavelength_MD.outputX >> sine_PMA.input2D[0].input2Dx
        WaveFollow_MD.outputX >> sine_PMA.input2D[1].input2Dx

        if maya_version >= 2024:
            unit_conversion = cmds.createNode('unitConversion', n='{}_unit'.format(sine_PMA))
            sin_node = cmds.createNode('sin', n='{}_sin'.format(sine_PMA))
            cmds.connectAttr('{}.output2Dx'.format(sine_PMA), '{}.input'.format(unit_conversion))
            cmds.connectAttr('{}.output'.format(unit_conversion), '{}.input'.format(sin_node))
            cmds.connectAttr('{}.output'.format(sin_node), '{}.input2X'.format(result_MD))
        else:
            expressionStr01 = result_MD + '.input2X' + ' = ' + 'sin(' + sine_PMA + '.output2Dx);' + '\n'
            expressionStr = expressionStr + expressionStr01
    if maya_version >= 2024:
        expression(s=expressionStr, name='sine_' + Axis, ae=True, uc=all)
    return nodeList


def CvNearestPoint(obj, cv):
    obj = pm.general.PyNode(obj)
    cv = pm.general.PyNode(cv)
    cv_Shape = pm.listRelatives(cv, s=1)[0]
    cv_NP = pm.createNode('nearestPointOnCurve', n=cv + '_nearestPoint')
    cv_Shape.worldSpace.connect(cv_NP.inputCurve)
    obj_pos = pm.xform(obj, q=1, ws=1, t=1)
    cv_NP.ip.set(obj_pos)
    out = [cv_NP.p.get(), cv_NP.pr.get()]
    pm.delete(cv_NP)
    return out


# todo: 替换控制器形态
def replace_curve(orig_curve, new_curve, snap=True, transfer_color=True):  # noqa
    """Replace orig_curve with new_curve.

    Args:
        orig_curve (str): nurbsCurve to replace.
        new_curve (str): nurbsCurve to replace with.
    """
    if snap:
        new_curve = cmds.duplicate(new_curve, rc=1)[0]
        cmds.parentConstraint(orig_curve, new_curve)

    if cmds.objectType(orig_curve) == 'transform' or cmds.objectType(orig_curve) == "joint":
        orig_shapes = cmds.listRelatives(orig_curve, shapes=True, type="nurbsCurve")
    else:
        raise Exception("Cant find the shape of the orig_curve")

    if cmds.objectType(new_curve) == 'transform' or cmds.objectType(new_curve) == "joint":
        new_shapes = cmds.listRelatives(new_curve, shapes=True, type="nurbsCurve")
    else:
        raise Exception("Cant find the shape of the new_curve")

    color = None
    if transfer_color:
        if cmds.getAttr(new_curve + ".overrideEnabled"):
            color = cmds.getAttr(new_curve + ".overrideColor")

    # Make amount of shapes equal
    shape_dif = len(orig_shapes) - len(new_shapes)
    if shape_dif != 0:
        # If original curve has fewer shapes, create new nulls until equal
        if shape_dif < 0:
            for shape in range(0, shape_dif * -1):
                dupe_curve = cmds.duplicate(orig_shapes, rc=1)[0]
                dupe_shape = cmds.listRelatives(dupe_curve, s=1)[0]

                orig_shapes.append(dupe_shape)
                cmds.select(dupe_shape, orig_curve)
                cmds.parent(r=1, s=1)
                cmds.delete(dupe_curve)
        # If original curve has more shapes, delete shapes until equal
        if shape_dif > 0:
            for shape in range(0, shape_dif):
                cmds.delete(orig_shapes[shape])

    orig_shapes = cmds.listRelatives(orig_curve, s=1)
    # For each shape, transfer from original to new.
    for new_shape, orig_shape in zip(new_shapes, orig_shapes):
        if color:
            cmds.setAttr("{}.overrideEnabled".format(new_shape), 1)
            cmds.setAttr("{}.overrideColor".format(new_shape), color)
        cmds.connectAttr("{}.worldSpace".format(new_shape), "{}.create".format(orig_shape))

        cmds.dgeval("{}.worldSpace".format(orig_shape))
        cmds.disconnectAttr("{}.worldSpace".format(new_shape), "{}.create".format(orig_shape))

        spans = cmds.getAttr('{}.degree'.format(orig_shape))
        degree = cmds.getAttr('{}.spans'.format(orig_shape))
        for i in range(0, spans + degree):
            cmds.xform(orig_shape + '.cv[' + str(i) + ']', t=cmds.pointPosition(new_shape + '.cv[' + str(i) + ']'),
                       ws=1)

    if snap:
        cmds.delete(new_curve)


def mirror_controller(axis="x", node_list=None, side_flags=("L_", "R_"), side_bias="start", continue_on_fail=True):
    if not node_list:
        node_list = cmds.ls(sl=True)

    warnings = []

    bias_dict = {"start": "'{0}'.startswith('{1}')", "end": "'{0}'.endswith('{1}')", "include": "'{1}' in '{0}'"}
    # print(bias_dict)
    if side_bias not in bias_dict.keys():
        cmds.error("Invalid argument: {0}".format(side_bias))
    for node in node_list:
        if eval(bias_dict[side_bias].format(node, side_flags[0])):
            other_side = node.replace(side_flags[0], side_flags[1])
        elif eval(bias_dict[side_bias].format(node, side_flags[1])):
            other_side = node.replace(side_flags[1], side_flags[0])
        else:
            if continue_on_fail:
                msg = "Cannot find side flags for %s. Skipping" % node
                cmds.warning(msg)
                warnings.append(msg)
                continue
            else:
                return -1
        if not cmds.objExists(other_side):
            if continue_on_fail:
                msg = "Cannot find the other side controller %s. Skipping" % other_side
                cmds.warning(msg)
                warnings.append(msg)
                continue
            else:
                return False

        tmp_cont = cmds.duplicate(node, name="tmp_{0}".format(node), rr=True, renameChildren=True)
        # delete nodes below it
        cmds.transformLimits(tmp_cont, etx=(0, 0), ety=(0, 0), etz=(0, 0), erx=(0, 0), ery=(0, 0), erz=(0, 0),
                             esx=(0, 0), esy=(0, 0), esz=(0, 0))
        attribute.unlock(tmp_cont[0])
        if cmds.listRelatives(tmp_cont, type="transform"):
            cmds.delete(cmds.listRelatives(tmp_cont, type="transform"))

        # create a group for the selected controller
        node_grp = cmds.group(name="tmpGrp", em=True)
        cmds.parent(tmp_cont, node_grp)
        # get rid of the limits
        # ## mirror it on the given axis
        cmds.setAttr("%s.s%s" % (node_grp, axis), -1)
        # ungroup it
        cmds.ungroup(node_grp)
        # cmds.makeIdentity(tmp_cont[0], a=True, r=False, t=False, s=True)
        replace_curve(other_side, tmp_cont[0], snap=False)
        cmds.delete(tmp_cont)


def addTransform(parent, name, m=[]):
    """Create a transform dagNode.

    Arguments:
        parent (dagNode): The parent for the node.
        name (str): The Node name.
        m (matrix): The matrix for the node transformation (optional).

    Returns:
        dagNode: The newly created node.

    """
    node = cmds.createNode("transform", n=name)
    cmds.xform(node, matrix=m)

    if parent is not None:
        cmds.parent(node, parent)

    return node


def getTransformFromPos(pos):
    """Create a transformation Matrix from a given position.

    Arguments:
        pos (vector): Position for the transformation matrix

    Returns:
        matrix: The newly created transformation matrix

    """
    m = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, pos[0], pos[1], pos[2], 1.0]

    return m


# @deco.one_undo
def deleteNamespaces():
    nss = cmds.namespaceInfo(lon=1, r=1)
    if 'UI' in nss:
        nss.remove('UI')
    if 'shared' in nss:
        nss.remove('shared')
    [cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True) for ns in nss if ns != ":"]


def openCurrentSceneFolder():
    """
    Open Current File Folder
    :return:
    """
    path1 = cmds.file(q=1, sn=1)
    full = path1.replace('/', '\\')
    a = -len(full.split('\\')[-1])
    full1 = full[0:a - 1]
    os.system('explorer.exe %s' % full1)


def mirror_all_obj(source=None, target=None):
    mirrored_matrix = OpenMaya.MMatrix([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    if source:
        sel = OpenMaya.MSelectionList()
        sel.add(source)
    else:
        sel = OpenMaya.MSelectionList()
        sel.add(target)
    dag_path_obj = sel.getDagPath(0)
    original_matrix_obj = dag_path_obj.inclusiveMatrix()

    mirror_ma = original_matrix_obj * mirrored_matrix

    sel = OpenMaya.MSelectionList()
    sel.add(target)
    dag_path = sel.getDagPath(0)

    # 创建 MFnTransform
    fn_transform = OpenMaya.MFnTransform(dag_path)

    # 将 MMatrix 转换为 MTransformationMatrix
    transform = OpenMaya.MTransformationMatrix(mirror_ma)

    # 设置物体的变换矩阵
    fn_transform.setTransformation(transform)


def multiply_matrices(matrix1, matrix2):
    """
    实现两个矩阵的相乘
    :param matrix1: 第一个矩阵（4x4 列表）
    :param matrix2: 第二个矩阵（4x4 列表）
    :return: 相乘结果矩阵（4x4 列表）
    """
    # 创建 multMatrix 节点
    mult_matrix_node = cmds.createNode('multMatrix', name='matrixMult')

    # 设置矩阵值
    cmds.setAttr("{}.matrixIn[0]".format(mult_matrix_node), matrix1, type="matrix")
    cmds.setAttr("{}.matrixIn[1]".format(mult_matrix_node), matrix2, type="matrix")

    # 获取相乘结果
    result_matrix = cmds.getAttr("{}.matrixSum".format(mult_matrix_node))
    cmds.delete(mult_matrix_node)
    return result_matrix


def replace_controller(
        old_controller,
        new_controller,
        mirror=True,
        mirror_axis="X",
        keep_old_shape=False,
        keep_copy=False,
        align_to_center=False,
):
    """Replace old_controller with new_controller.

    Args:
        old_controller (str): The controller with the old shape
        new_controller (str): The new shape for the old controller
        mirror (bool): If True mirrors the controller shape
        mirror_axis (str): Mirror axis direction. Only valid if mirror set to True.
                            Defaults to "X"
        keep_old_shape (bool): If True does not delete the old controller shape
        keep_copy (bool): If True, duplicates the new controller, keeping a copy of it intact
        align_to_center (bool): If True aligns to the center

    Returns:

    """

    # get the current transform
    try_channels = ["tx", "ty", "tz", "rx", "ry", "rz"]
    transform_dict = {}
    for attr in try_channels:
        kept_data = cmds.getAttr("%s.%s" % (old_controller, attr))
        transform_dict[attr] = kept_data
        try:
            cmds.setAttr("%s.%s" % (old_controller, attr), 0)
        except RuntimeError:
            pass

    new_cont_dup = cmds.duplicate(new_controller)[0] if keep_copy else new_controller
    # make a nested loop for all channels
    for attr in [(x, y) for x in "trs" for y in "xyz"]:
        cmds.setAttr(
            "{0}.{1}{2}".format(new_cont_dup, attr[0], attr[1]), e=True, k=True, l=False
        )

    cmds.makeIdentity(new_cont_dup, a=True)

    # Make sure the new controllers transform are zeroed at the (0,0,0)
    offset = cmds.xform(new_cont_dup, q=True, ws=True, rp=True)
    rv_offset = [x * -1 for x in offset]
    cmds.xform(new_cont_dup, ws=True, t=rv_offset)

    cmds.makeIdentity(
        new_cont_dup, apply=True, t=True, r=False, s=True, n=False, pn=True
    )

    # get the same color code
    cmds.setAttr(
        "%s.overrideEnabled" % func.get_shapes(new_cont_dup)[0],
        cmds.getAttr("%s.overrideEnabled" % func.get_shapes(old_controller)[0]),
    )

    cmds.setAttr(
        "%s.overrideColor" % func.get_shapes(new_cont_dup)[0],
        cmds.getAttr("%s.overrideColor" % func.get_shapes(old_controller)[0]),
    )

    # move the new controller to the old controllers place
    if align_to_center:
        func.align_to(new_cont_dup, old_controller, position=True, rotation=True)
    else:
        func.align_to_alter(new_cont_dup, old_controller, mode=2)

    # put the new controller shape under the same parent with the old first (if there is a parent)
    if func.get_parent(old_controller):
        cmds.parent(new_cont_dup, func.get_parent(old_controller))
    cmds.makeIdentity(new_cont_dup, apply=True)

    if not keep_old_shape:
        cmds.delete(cmds.listRelatives(old_controller, shapes=True, children=True))

    cmds.parent(func.get_shapes(new_cont_dup)[0], old_controller, r=True, s=True)

    if mirror:
        # find the mirror of the oldController
        if old_controller.startswith("L_"):
            mirror_name = old_controller.replace("L_", "R_")
        elif old_controller.startswith("R_"):
            mirror_name = old_controller.replace("R_", "L_")
        else:
            cmds.warning("Cannot find the mirror controller, skipping mirror part")
            if not keep_old_shape:
                cmds.delete(func.get_shapes(old_controller))
            return
        old_cont_mirror = mirror_name
        # get the current transform
        transform_dict_mirror = {}
        for attr in try_channels:
            kept_data_mirror = cmds.getAttr("{0}.{1}".format(old_cont_mirror, attr))
            transform_dict_mirror[attr] = kept_data_mirror
            try:
                cmds.setAttr("%s.%s" % (old_cont_mirror, attr), 0)
            except RuntimeError:
                pass

        new_cont_dup_mirror = cmds.duplicate(new_controller)[0]
        cmds.makeIdentity(new_cont_dup_mirror, a=True)
        # Make sure the new controllers transform are zeroed at the (0,0,0)
        offset = cmds.xform(new_cont_dup_mirror, q=True, ws=True, rp=True)
        rv_offset = [x * -1 for x in offset]
        cmds.xform(new_cont_dup_mirror, ws=True, t=rv_offset)
        cmds.makeIdentity(
            new_cont_dup_mirror, apply=True, t=True, r=True, s=True, n=False, pn=True
        )
        cmds.setAttr("{0}.scale{1}".format(new_cont_dup_mirror, mirror_axis), -1)
        cmds.makeIdentity(new_cont_dup_mirror, apply=True, s=True)

        # get the same color code
        cmds.setAttr(
            "%s.overrideEnabled" % func.get_shapes(new_cont_dup_mirror)[0],
            cmds.getAttr("%s.overrideEnabled")
            % func.get_shapes(old_cont_mirror)[0],
        )
        cmds.setAttr(
            "%s.overrideColor" % func.get_shapes(new_cont_dup_mirror)[0],
            cmds.getAttr("%s.overrideColor" % func.get_shapes(old_cont_mirror)[0]),
        )

        # move the new controller to the old controllers place
        func.align_to_alter(new_cont_dup_mirror, old_cont_mirror, mode=0)

        if not keep_old_shape:
            cmds.delete(cmds.listRelatives(old_cont_mirror, shapes=True, children=True))

        for attr in try_channels:
            try:
                cmds.setAttr(
                    "{0}.{1}".format(old_cont_mirror, attr), transform_dict_mirror[attr]
                )
            except RuntimeError:
                pass

    for attr in try_channels:
        try:
            cmds.setAttr("{0}.{1}".format(old_controller, attr), transform_dict[attr])
        except RuntimeError:
            pass


def create_hierarchy_groups_from_joint(selected_joints, prefix="", suffix="_grp"):
    """
    根据选中的骨骼创建匹配的层级组结构
    返回: {选中骨骼短名称: [创建的组列表]}
    """
    # 获取选择的骨骼（只取第一个选中的骨骼）
    if not selected_joints:
        cmds.warning("请先选择一个关节！")
        return {}

    result = {}
    for i,jnt in enumerate(selected_joints):
        root_joint = jnt

        # 获取该骨骼下的完整层级（包括自身和所有子级）
        all_joints = [root_joint]
        all_joints.extend(cmds.listRelatives(root_joint, allDescendents=True, fullPath=True, type="joint") or [])

        # 按层级深度排序（确保先父后子）
        all_joints.sort(key=lambda x: x.count("|"))

        created_groups = []  # 存储所有创建的组
        parent_dict = {}  # 临时存储父子关系 {短名称: 组}

        for joint in all_joints:
            # 获取关节短名称
            joint_name = joint.split("|")[-1]
            group_name = prefix + joint_name + suffix

            # 获取父关节短名称
            parent_joint = cmds.listRelatives(joint, parent=True, fullPath=True)
            parent_name = parent_joint[0].split("|")[-1] if parent_joint else None

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


class Snake(ctrl.Icon):

    @staticmethod
    def addSnakeAttrs(rigObj, addDrum=True, addRot=True, addCurly=True, prefix=""):
        if addDrum:
            attribute.addAttributes(rigObj, 'Drumbag', "bool", keyable=True, lock=True)
            attribute.addAttributes(rigObj, 'DrumBagSpeed', "double", value=1, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'DrumBagStrength', "double", value=0, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'DrumBagOffset', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'DrumBagReduction', "double", value=1, keyable=True)

        if addRot:
            attribute.addAttributes(rigObj, 'FK', "bool", keyable=True, lock=True)
            attribute.addAttributes(rigObj, 'rootX', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'rootY', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'rootZ', "double", value=0, keyable=True)

        if addCurly:
            attribute.addAttributes(rigObj, 'Curly', "bool", keyable=True, lock=True)
            attribute.addAttributes(rigObj, 'curlyX', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'curlyY', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'curlyZ', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'Clamp', "double", value=30, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'Strength', "double", value=1, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'Increment', "double", value=3, min=0, keyable=True)

            attribute.addAttributes(rigObj, 'boodyCurlyX', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'boodyCurlyY', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'boodyCurlyZ', "double", value=0, keyable=True)
            attribute.addAttributes(rigObj, 'boodyClamp', "double", value=30, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'boodyStrength', "double", value=1, min=0, keyable=True)
            attribute.addAttributes(rigObj, 'boodyIncrement', "double", value=3, min=0, keyable=True)

    @staticmethod
    def dupConCurve(joints, **kwargs):
        Curve = curve(d=3, p=[xform(i, q=1, t=1, ws=1) for i in ls(joints, dag=1)])
        if 'n' in kwargs:
            if type(kwargs['n']) == str:
                rename(Curve, 'ConCurve' + kwargs['n'])
        if 'name' in kwargs:
            if type(kwargs['name']) == str:
                rename(Curve, 'ConCurve' + kwargs['name'])
        parent(Curve, w=1)
        return Curve

    def createRemapValue(self, name):
        remapValue = pm.createNode('remapValue', n=name + 'remapValue')

        remapValue.value[0].value_Position.set(0)
        remapValue.value[0].value_FloatValue.set(1)
        remapValue.value[0].value_Interp.set(1)

        remapValue.value[1].value_Position.set(0.5)
        remapValue.value[1].value_FloatValue.set(0)
        remapValue.value[1].value_Interp.set(1)

        remapValue.value[2].value_Position.set(1)
        remapValue.value[2].value_FloatValue.set(1)
        remapValue.value[2].value_Interp.set(1)

        remapValue.inputMin.set(-1)
        remapValue.inputMax.set(1)

        remapValue.outputMin.set(0)
        remapValue.outputMax.set(1)
        return remapValue

    def addSnakeIK(self, ctrlJnts, side, nurbs, parentObj, aimAxis):
        transformPointList = []
        ikGrp = createNode("transform", name="%sikGrp" % side, p=parentObj)
        for i in ctrlJnts:
            transformPoint = spaceLocator(n=i.split('|')[-1] + '_transformPoint')
            delete(parentConstraint(i, transformPoint))
            transformPointList.append(transformPoint)
        ikPointTransformGrp = group(transformPointList, n=side + 'ikPointTransformGrp')  # 位置定位器组
        ikPointTransformGrp.inheritsTransform.set(0)
        parent(ikPointTransformGrp, ikGrp)

        ikOtherGrp = createNode('transform', n=side + 'ikOtherGrp', p=ikGrp)

        Curve = self.dupConCurve(ctrlJnts, n=side + 'ikCurveStart')  # 位置曲线
        # 缩放曲线
        CurveCgRigm = self.dupConCurve(ctrlJnts, n=side + 'ikCurveCgRigm')
        CurveCgRigmY = self.dupConCurve(ctrlJnts, n=side + 'ikCurveCgRigmY')
        CurveCgRigmZ = self.dupConCurve(ctrlJnts, n=side + 'ikCurveCgRigmZ')
        # 相对缩放曲线
        CurveCgRigmYBase = self.dupConCurve(ctrlJnts, n=side + 'ikCurveCgRigmYBase')
        CurveCgRigmZBase = self.dupConCurve(ctrlJnts, n=side + 'ikCurveCgRigmZBase')
        parent(Curve, CurveCgRigm, CurveCgRigmY, CurveCgRigmZ, CurveCgRigmYBase, CurveCgRigmZBase, ikOtherGrp)
        move(CurveCgRigmY.cv, (0, 1, 0), r=1)
        move(CurveCgRigmYBase.cv, (0, 1, 0), r=1)
        if aimAxis[0] == 1 or aimAxis[0] == -1:
            move(CurveCgRigmZ.cv, (1, 0, 0), r=1)
            move(CurveCgRigmZBase.cv, (1, 0, 0), r=1)
        else:
            move(CurveCgRigmZ.cv, (0, 0, 1), r=1)
            move(CurveCgRigmZBase.cv, (0, 0, 1), r=1)

        ikCgRigmJinList = []

        for i in range(len(ctrlJnts)):
            cvPos = ctrlJnts[i].getTranslation(space='world')
            select(cl=1)

            scaleJoint = joint(p=cvPos, n=side + 'ikScaleJoint' + str(i))
            scaleJoint.v.set(0)
            scaleJoint.v.set(lock=1)

            delete(parentConstraint(ctrlJnts[i], scaleJoint))
            select(scaleJoint, r=1)
            makeIdentity(apply=True, t=0, r=1, s=0, n=0, pn=1)

            scaleConstraint(ctrlJnts[i], scaleJoint)
            ikCgRigmJinList.append(scaleJoint)
            refresh()

        skinCluster(ctrlJnts, Curve, tsb=1, nw=1)

        skinCluster(ikCgRigmJinList, CurveCgRigm, tsb=1, nw=1, mi=1)
        skinCluster(ikCgRigmJinList, CurveCgRigmY, tsb=1, nw=1, mi=1)
        skinCluster(ikCgRigmJinList, CurveCgRigmZ, tsb=1, nw=1, mi=1)

        CgRigmJointGrp = createNode('transform', n=side + 'ikCgRigmJointGrp', p=ikGrp)  # 缩放控制关节
        [parent(i, CgRigmJointGrp) for i in ikCgRigmJinList]

        # 控制曲线形态
        cv_Shape = listRelatives(Curve, s=1)[0]
        # 缩放曲线形态
        CurveCgRigmShape = listRelatives(CurveCgRigm, s=1)[0]
        CurveCgRigmYShape = listRelatives(CurveCgRigmY, s=1)[0]
        CurveCgRigmZShape = listRelatives(CurveCgRigmZ, s=1)[0]
        # 相对缩放曲线形态
        CurveCgRigmYBaseShape = listRelatives(CurveCgRigmYBase, s=1)[0]
        CurveCgRigmZBaseShape = listRelatives(CurveCgRigmZBase, s=1)[0]
        nurbsUpShape = listRelatives(nurbs, s=1)[0]
        outS = []
        for i in range(len(transformPointList)):
            spa = transformPointList[i]
            spaShape = listRelatives(spa, s=1)[0]

            cv_NP = createNode('nearestPointOnCurve', n=Curve + 'nearestPointOnCurve' + str(i))
            cv_Shape.worldSpace.connect(cv_NP.inputCurve)
            spaShape.wp.connect(cv_NP.ip)

            nu_NP = createNode('closestPointOnSurface', n=Curve + 'closestPointOnSurface' + str(i))
            nurbsUpShape.worldSpace.connect(nu_NP.inputSurface)
            spaShape.wp.connect(nu_NP.ip)

            # 缩放曲线点节点
            # 原始
            pointOnCurveInfo = createNode('pointOnCurveInfo', n=CurveCgRigmShape + 'pointOnCurveInfo' + str(i))
            cv_NP.pr.connect(pointOnCurveInfo.parameter)
            CurveCgRigmShape.ws.connect(pointOnCurveInfo.ic)
            # Y
            pointOnCurveInfoY = createNode('pointOnCurveInfo',
                                           n=CurveCgRigmShape + 'pointOnCurveInfoY' + str(i))
            cv_NP.pr.connect(pointOnCurveInfoY.parameter)
            CurveCgRigmYShape.ws.connect(pointOnCurveInfoY.ic)
            # Z
            pointOnCurveInfoZ = createNode('pointOnCurveInfo',
                                           n=CurveCgRigmShape + 'pointOnCurveInfoZ' + str(i))
            cv_NP.pr.connect(pointOnCurveInfoZ.parameter)
            CurveCgRigmZShape.ws.connect(pointOnCurveInfoZ.ic)
            # 相对曲线点节点
            # Y
            pointOnCurveInfoBaseY = createNode('pointOnCurveInfo',
                                               n=CurveCgRigmShape + 'pointOnCurveInfoBaseY' + str(i))
            cv_NP.pr.connect(pointOnCurveInfoBaseY.parameter)
            CurveCgRigmYBaseShape.ws.connect(pointOnCurveInfoBaseY.ic)
            # Z
            pointOnCurveInfoBaseZ = createNode('pointOnCurveInfo',
                                               n=CurveCgRigmShape + 'pointOnCurveInfoBaseZ' + str(i))
            cv_NP.pr.connect(pointOnCurveInfoBaseZ.parameter)
            CurveCgRigmZBaseShape.ws.connect(pointOnCurveInfoBaseZ.ic)
            # 距离计算缩放
            MultiplyDividefollicleCgRigm = shadingNode('multiplyDivide', asUtility=1,
                                                     n='MultiplyDividefollicleCgRigm' + str(i))
            MultiplyDividefollicleCgRigm.operation.set(2)
            # Y
            distanceBetweenY = shadingNode('distanceBetween', asUtility=1, n='distanceBetweenY' + str(i))
            pointOnCurveInfo.p.connect(distanceBetweenY.p1)
            pointOnCurveInfoY.p.connect(distanceBetweenY.p2)

            distanceBetweenBaseY = shadingNode('distanceBetween', asUtility=1,
                                               n='distanceBetweenBaseY' + str(i))
            pointOnCurveInfo.p.connect(distanceBetweenBaseY.p1)
            pointOnCurveInfoBaseY.p.connect(distanceBetweenBaseY.p2)

            distanceBetweenY.d.connect(MultiplyDividefollicleCgRigm.i1x)
            distanceBetweenBaseY.d.connect(MultiplyDividefollicleCgRigm.i2x)
            # Z
            distanceBetweenZ = shadingNode('distanceBetween', asUtility=1, n='distanceBetweenZ' + str(i))
            pointOnCurveInfo.p.connect(distanceBetweenZ.p1)
            pointOnCurveInfoZ.p.connect(distanceBetweenZ.p2)

            distanceBetweenBaseZ = shadingNode('distanceBetween', asUtility=1,
                                               n='distanceBetweenBaseZ' + str(i))
            pointOnCurveInfo.p.connect(distanceBetweenBaseZ.p1)
            pointOnCurveInfoBaseZ.p.connect(distanceBetweenBaseZ.p2)

            distanceBetweenZ.d.connect(MultiplyDividefollicleCgRigm.i1y)
            distanceBetweenBaseZ.d.connect(MultiplyDividefollicleCgRigm.i2y)

            # 输出缩放
            outS.append((MultiplyDividefollicleCgRigm.ox, MultiplyDividefollicleCgRigm.oy))

            refresh()

        ikOtherGrp.visibility.set(0, lock=True)
        ikPointTransformGrp.visibility.set(0, lock=True)

        return transformPointList, ikCgRigmJinList, outS

    def addSnakeCurly(self, attrObj, ikJoint, ReverseJoint, rootJoint, type="curly", strIncClPrefix=""):
        # 创建旋转强度绑定
        strengthMD = createNode('multiplyDivide', n=attrObj + '_Multiply')  # 旋转强度乘除节点
        connectAttr("%s.%sX" % (attrObj, type), strengthMD.i1x)
        connectAttr("%s.%sY" % (attrObj, type), strengthMD.i1y)
        connectAttr("%s.%sZ" % (attrObj, type), strengthMD.i1z)

        connectAttr("%s.%sStrength" % (attrObj, strIncClPrefix), strengthMD.i2x)
        connectAttr("%s.%sStrength" % (attrObj, strIncClPrefix), strengthMD.i2y)
        connectAttr("%s.%sStrength" % (attrObj, strIncClPrefix), strengthMD.i2z)

        attrRootX = strengthMD.ox  # 旋转控制属性
        attrRootY = strengthMD.oy
        attrRootZ = strengthMD.oz
        # 创建反向旋转强度绑定
        ReverseMD = createNode('multiplyDivide', n=attrObj + '_MultiplyReverse')  # 旋转强度乘除节点
        attrRootX.connect(ReverseMD.i1x)
        attrRootY.connect(ReverseMD.i1y)
        attrRootZ.connect(ReverseMD.i1z)
        ReverseMD.i2.set((-1, -1, -1))

        ReverseRootX = ReverseMD.ox  # 旋转控制属性
        ReverseRootY = ReverseMD.oy
        ReverseRootZ = ReverseMD.oz

        # 创建旋转递增强度绑定
        IncrementMD = createNode('multiplyDivide',
                                 n=attrObj.split('|')[-1] + '_Increment_Multiply')  # 旋转强度乘除节点
        connectAttr(attrObj + ".%sIncrement" % strIncClPrefix, IncrementMD.i1x)

        IncrementMD.i2x.set(0.01)

        IncrementAdd = createNode('plusMinusAverage',
                                  n=attrObj.split('|')[-1] + '_Increment_MultiplyAdd')
        IncrementMD.ox >> IncrementAdd.i1[0]
        IncrementAdd.i1[1].set(1)

        attrIncrement = IncrementAdd.o1  # 旋转递增强度

        IncrementIt = multiplyDivideLinkedList(len(rootJoint), n=attrObj + '_Increment')

        IncrementIt.con(attrIncrement, 'i2x')
        IncrementIt.con(attrIncrement, 'i2y')
        IncrementIt.con(attrIncrement, 'i2z')

        IncrementIt.initIt()
        connectAttr("%s.%sClamp" % (attrObj, strIncClPrefix), IncrementIt.currentDG.i1x)
        connectAttr("%s.%sClamp" % (attrObj, strIncClPrefix), IncrementIt.currentDG.i1y)
        connectAttr("%s.%sClamp" % (attrObj, strIncClPrefix), IncrementIt.currentDG.i1z)

        # 创建之后减去绑定节点
        addIt = addLinkedList(len(rootJoint), 3, n=attrObj + '_minus')
        addIt.set(1, 'operation')
        addIt.Reverse()
        addIt.initIt()
        # 建立限制节点
        Ikclamp = [createNode('clamp', n=i.split('|')[-1] + '_Ikclamp') for i in
                   rootJoint]  # 限制节点功能为限制每个关节最大最小值以产生卷曲效果
        [i.mn.set((-1, -1, -1)) for i in Ikclamp]
        [i.mx.set((1, 1, 1)) for i in Ikclamp]
        # 创建减去连接
        addIt.initIt()
        for i in Ikclamp:
            addIt.inCon(i.op)
            addIt.it()
        # 创建减去绑定
        Less = [createNode('plusMinusAverage', n=i.split('|')[-1] + '_Less') for i in rootJoint]
        [i.operation.set(2) for i in Less]
        [attrRootX.connect(i.i3[0].i3x) for i in Less]
        [attrRootY.connect(i.i3[0].i3y) for i in Less]
        [attrRootZ.connect(i.i3[0].i3z) for i in Less]

        addIt.initIt()
        for i in Less[0:-1]:
            addIt.it()
            addIt.outCon(i.i3[1])
        # 建立限制绑定
        It = Iteration(Less, Ikclamp)
        for i in Ikclamp:
            It.it[0].o3 >> It.it[1].ip
            It.next()

        # 创建衰减最终连接绑定
        attenuation = [createNode('multiplyDivide', n=i.split('|')[-1] + '_multiplyDivideAttenuation') for i
                       in rootJoint]

        It = Iteration(IncrementIt.DG, Ikclamp, attenuation)
        for i in It.init():
            It.it[0].o >> It.it[2].i1
            It.it[1].op >> It.it[2].i2
            It.next()
        # 创建Ik减去矩阵
        decomposeMatrix = []
        It = Iteration(ikJoint, rootJoint)
        for i in It.init():
            Node = createNode('decomposeMatrix')
            It.it[0].inverseMatrix >> Node.inputMatrix
            decomposeMatrix.append(Node)
            It.next()
        # 创建Ik减去绑定
        AddplusMinusRemapList = []
        It = Iteration(Ikclamp, decomposeMatrix, ReverseJoint)
        for i in It.init():
            RemapValueX = self.createRemapValue(It.it[1].split('|')[-1] + '_LessRemapValueX')
            AddplusMinusRemapList.append(RemapValueX)
            It.it[0].opr >> RemapValueX.inputValue

            RemapValueY = self.createRemapValue(It.it[1].split('|')[-1] + '_LessRemapValueY')
            AddplusMinusRemapList.append(RemapValueY)
            It.it[0].opg >> RemapValueY.inputValue

            RemapValueZ = self.createRemapValue(It.it[1].split('|')[-1] + '_LessRemapValueZ')
            AddplusMinusRemapList.append(RemapValueZ)
            It.it[0].opb >> RemapValueZ.inputValue

            AddplusMinusAverage = createNode('plusMinusAverage',
                                             n=It.it[1].split('|')[-1] + 'AddplusMinusAverage')

            RemapValueX.outValue >> AddplusMinusAverage.input1D[0]
            RemapValueY.outValue >> AddplusMinusAverage.input1D[1]
            RemapValueZ.outValue >> AddplusMinusAverage.input1D[2]

            setRangedrive = createNode('setRange', n=It.it[1].split('|')[-1] + 'setRangedrive')
            AddplusMinusRemapList.append(setRangedrive)
            setRangedrive.oldMin.set((0, 0, 0))
            setRangedrive.oldMax.set((1, 1, 1))
            setRangedrive.min.set((0, 0, 0))

            AddplusMinusAverage.output1D >> setRangedrive.valueX
            AddplusMinusAverage.output1D >> setRangedrive.valueY
            AddplusMinusAverage.output1D >> setRangedrive.valueZ

            It.it[1].outputRotate >> setRangedrive.max

            setRangedrive.o >> It.it[2].r
            AddplusMinusRemapList.append(AddplusMinusAverage)
            It.next()
        # 最终连接
        It = Iteration(attenuation, rootJoint)
        for i in It.init():
            It.it[0].o >> It.it[1].r
            It.next()
        return [strengthMD, ReverseMD, IncrementMD, addIt.DG, Ikclamp, decomposeMatrix, Less, AddplusMinusRemapList]

    def addSnakeDrum(self, skinJntList, attrObj):
        DrumBagGrpList = [cmds.group(i, n=i.split('|')[-1] + 'DrumBagGrp', em=True) for i in skinJntList]
        [attribute.addAttributes(jnt, "DrumBagStrength", "float", value=1, keyable=True) for jnt in skinJntList]

        exp = 'float $time = time*' + attrObj + '.DrumBagSpeed+' + attrObj + '.DrumBagOffset;\n'
        exp = exp + 'float $Strength = ' + attrObj + '.DrumBagStrength;\n'
        exp = exp + 'float $Reduction = ' + attrObj + '.DrumBagReduction;\n'
        for i in range(len(DrumBagGrpList)):
            exp = exp + DrumBagGrpList[i] + '.scaleX=1+((1+sin($time))*0.5*$Strength*' + skinJntList[
                i] + '.DrumBagStrength);\n'
            exp = exp + DrumBagGrpList[i] + '.scaleY=1+((1+sin($time))*0.5*$Strength*' + skinJntList[
                i] + '.DrumBagStrength);\n'
            exp = exp + DrumBagGrpList[i] + '.scaleZ=1+((1+sin($time))*0.5*$Strength*' + skinJntList[
                i] + '.DrumBagStrength);\n'
            exp = exp + '$time-=$Reduction;\n'
        cmds.expression(s=exp, ae=1, name=attrObj + '_DrumBagExp', uc='all')
        [cmds.scaleConstraint(grp, jnt) for grp, jnt in zip(DrumBagGrpList, skinJntList)]
        return DrumBagGrpList

    def addSnakeSlider(self, ikCons, sliderNumber, name, axis, ctrlJnts, scaleObj, size):
        """

        :param ikCons:
        :param sliderNumber:
        :param name:
        :param axis:
        :param ctrlJnts:
        :return:
        """
        nodeList = []
        sliderGrp = createNode("transform", name=name + "sliderGrp")
        Curve = curve(d=1, p=[pm.xform(i, q=1, t=1, ws=1) for i in ikCons],
                      n=name + 'SlidingPositioningCurve')
        Curve.inheritsTransform.set(0)

        UpCurve = curve(d=1, p=[pm.xform(i, q=1, t=1, ws=1) for i in ikCons],
                        n=name + 'SlidingPositioningCurveUp')
        UpCurve.inheritsTransform.set(0)
        setAttr(UpCurve + '.translate' + axis, 1)

        Nurbs = loft(Curve, UpCurve, ch=0, u=1, c=0, ar=1, d=1, ss=1, rn=0, po=0, rsn=True,
                     n=name + 'SlidingPositioningNurbs')[0]

        delete(UpCurve)
        slideLocList = list()  # 位置定位器列表
        UpslideLocList = list()  # 位置定位器列表
        pointer = 0

        for i in range(len(ikCons)):
            refresh()
            loc = spaceLocator(n=ikCons[i].split('|')[-1] + '_SlideLoc')
            loc.v.set(0, lock=1)
            delete(pm.pointConstraint(ikCons[i], loc))
            parent(loc, ikCons[i])
            listRelatives(loc, s=1)[0].worldPosition.connect(listRelatives(Curve, s=1)[0].controlPoints[i])
            listRelatives(loc, s=1)[0].worldPosition.connect(listRelatives(Nurbs, s=1)[0].controlPoints[pointer])
            pointer = pointer + 1

            Uploc = spaceLocator(n=ikCons[i].split('|')[-1] + '_SlideLocUp')
            Uploc.v.set(0, lock=1)
            delete(pointConstraint(ikCons[i], Uploc))

            parent(Uploc, ikCons[i])
            listRelatives(Uploc, s=1)[0].worldPosition.connect(listRelatives(Nurbs, s=1)[0].controlPoints[pointer])
            pointer = pointer + 1
            setAttr(Uploc + ".translate" + axis, 0.5)
            slideLocList.append(loc)
            UpslideLocList.append(Uploc)

        # 创建滑动控制器
        CurveShape = listRelatives(Curve, s=1)[0]
        nurbsShape = listRelatives(Nurbs, s=1)[0]
        follicleList = []
        ConGrpList = []
        ConList = []
        ConPathLocList = []
        ConPathLocShapeList = []
        select(d=True)
        jointList = createJointChainByCurve(Curve, "", "", sliderNumber)

        for i, jnt in enumerate(jointList):
            loc = spaceLocator(n=name + 'motionPathLoc_' + str(i))
            locShape = listRelatives(loc, s=1)[0]
            ConPathLocList.append(loc)
            ConPathLocShapeList.append(locShape)

            follicle = pm.createNode('follicle', n=Nurbs.split('|')[-1] + 'follicle' + str(i))
            follicleTransform = pm.listRelatives(follicle, p=1)[0]
            follicle.ot.connect(follicleTransform.t)
            follicle.outRotate.connect(follicleTransform.r)
            follicle.parameterU.set(0)
            follicle.parameterV.set(0)
            nurbsShape.ws.connect(follicleTransform.inputSurface)

            pm.delete(pm.parentConstraint(ikCons[0], loc))
            pm.delete(pm.pointConstraint(follicleTransform, loc))

            pm.parent(loc, follicleTransform)
            # 创建控制器
            Con = PyNode(
                self.create_icon("Sphere", name + 'slideCon_' + str(i), icon_color=17, scale=(size, size, size))[0])

            grp = group(em=1, n=name + 'slideConGrp')
            parent(Con, grp)
            parentConstraint(loc, grp)

            addAttr(Con, ln='U', at=float, k=1, dv=0, min=0, max=10)
            addAttr(Con, ln='range', at=float, k=1, dv=1, min=0.01)
            addAttr(Con, ln='Curve', at='enum', k=1, dv=2, en='no:Linear:smooth:Spline:')

            md = createNode('multiplyDivide', n=name + '_multiplyDivide_PathU')
            Con.U.connect(md.input1X)
            md.input2X.set(0.1)
            md.ox.connect(follicle.parameterU)

            ConList.append(Con)
            ConGrpList.append(grp)
            follicleList.append(follicle)

        # 创建临时曲线
        temporaryCurve = \
            rebuildCurve(curve(d=1, p=[pm.xform(i, q=1, t=1, ws=1) for i in ikCons]), ch=0, rpo=1, rt=0,
                         end=1, kr=0, kcp=0, kep=1, kt=0, s=4, d=2, tol=0.01)[0]
        # 设置控制器U位置
        [ConList[i].U.set(CvNearestPoint(jointList[i], temporaryCurve)[1] * 10) for i in range(len(ConList))]
        # 删除临时曲线
        delete(temporaryCurve)
        # 创建控制器定位器
        ConLocList = []
        for i in ConList:
            ConLoc = spaceLocator(n=i.split('|')[-1] + 'Loc')
            ConLoc.v.set(0, lock=1)
            delete(parentConstraint(i, ConLoc))
            parent(ConLoc, i)
            ConLocList.append(ConLoc)
        # 创建曲线最近点节点每个ik控制器下定位器一个
        posNearestPointList = []
        for i in listRelatives(slideLocList, s=1):
            cv_NP = createNode('nearestPointOnCurve', n=Curve.split('|')[-1] + '_conLoc_nearestPoint')
            CurveShape.worldSpace.connect(cv_NP.inputCurve)
            i.worldPosition.connect(cv_NP.ip)
            posNearestPointList.append(cv_NP.p)
        # 计算距离
        DisList = []

        for i in posNearestPointList:
            DisListA = []
            Md = ''
            size = 0
            for t in range(len(ConList)):
                dis = shadingNode('distanceBetween', asUtility=1,
                                  n=i.split('.')[0] + "To" + str(size) + 'Dis')
                scMult = shadingNode("multDoubleLinear", asUtility=1)
                scaleObj.sx.connect(scMult.input1)
                ConList[t].range.connect(scMult.input2)
                ConPathLocShapeList[t].wp.connect(dis.p1)
                i.connect(dis.p2)
                if size % 3 == 0:
                    Md = shadingNode('multiplyDivide', asUtility=1,
                                     n=i.split('.')[0] + "To" + str(size) + 'multiplyDivide')
                    Md.operation.set(2)
                    dis.d >> Md.i1x
                    scMult.output >> Md.i2x
                    DisListA.append(Md.ox)
                elif size % 3 == 1:
                    dis.d >> Md.i1y
                    scMult.output >> Md.i2y
                    DisListA.append(Md.oy)
                else:
                    dis.d >> Md.i1z
                    scMult.output >> Md.i2z
                    DisListA.append(Md.oz)
                size = size + 1
            nodeList.append(Md)
            DisList.append(DisListA)
        # 建立对应控制组
        slideConGrp = []
        for i in ctrlJnts:
            grp = group(em=1, n=i.split('|')[-1] + '_slide')
            delete(parentConstraint(i, grp))
            parent(grp, i.getParent())
            parent(i, grp)
            slideConGrp.append(grp)
        # 创建映射
        remapValueList = []
        for t in DisList:
            remapValueListA = []
            size = 0
            for i in t:
                remapValue = shadingNode('remapValue', asUtility=1, n='remapValueDis' + str(size))
                remapValueListA.append(remapValue)
                [ConList[size].Curve.connect(remapValue.value[t].value_Interp) for t in range(2)]
                remapValue.value[0].value_FloatValue.set(1)
                remapValue.value[0].value_Position.set(0)

                remapValue.value[1].value_FloatValue.set(0)
                remapValue.value[1].value_Position.set(1)

                remapValue.inputMin.set(0)
                remapValue.inputMax.set(1)

                remapValue.outputMin.set(0)
                remapValue.outputMax.set(1)

                i.connect(remapValue.inputValue)
                size = size + 1
            remapValueList.append(remapValueListA)
        ###########################
        # 建立滑动控制
        size = 0

        for i in slideConGrp:
            plusMinusAverage = shadingNode('plusMinusAverage', asUtility=1,
                                           n=i.split('|')[-1] + 'plusMinusAverageOutT')
            nodeList.append(plusMinusAverage)
            plusMinusAverage.operation.set(1)
            for t in range(len(remapValueList[size])):
                md = shadingNode('multiplyDivide', asUtility=1,
                                 n=i.split('|')[-1] + "Id" + str(t) + 'multiplyDivideT')
                nodeList.append(md)
                ConList[t].t >> md.i1
                remapValueList[size][t].ov >> md.i2x
                remapValueList[size][t].ov >> md.i2y
                remapValueList[size][t].ov >> md.i2z
                md.o >> plusMinusAverage.i3[t]
            if 'R_' in i.nodeName() or '_R' in i.nodeName():
                sideMd = shadingNode('multiplyDivide', asUtility=1, n=i.split('|')[-1] + "sideMult")
                sideMd.input2.set(-1, -1, -1)
                plusMinusAverage.o3 >> sideMd.input1
                sideMd.output >> i.t
            else:
                plusMinusAverage.o3 >> i.t

            plusMinusAverage = shadingNode('plusMinusAverage', asUtility=1,
                                           n=i.split('|')[-1] + 'plusMinusAverageOutR')
            nodeList.append(plusMinusAverage)
            plusMinusAverage.operation.set(1)
            for t in range(len(remapValueList[size])):
                md = shadingNode('multiplyDivide', asUtility=1,
                                 n=i.split('|')[-1] + "Id" + str(t) + 'multiplyDivideR')
                nodeList.append(md)
                ConList[t].r >> md.i1
                remapValueList[size][t].ov >> md.i2x
                remapValueList[size][t].ov >> md.i2y
                remapValueList[size][t].ov >> md.i2z
                md.o >> plusMinusAverage.i3[t]
            plusMinusAverage.o3 >> i.r

            plusMinusAverageOut = shadingNode('plusMinusAverage', asUtility=1,
                                              n=i.split('|')[-1] + 'plusMinusAverageOutS')
            nodeList.append(plusMinusAverageOut)
            for t in range(len(remapValueList[size])):
                plusMinusAverage = shadingNode('plusMinusAverage', asUtility=1,
                                               n=i.split('|')[-1] + "Id" + str(t) + 'plusMinusAverageInS')
                nodeList.append(plusMinusAverage)
                ConList[t].s >> plusMinusAverage.i3[0]
                plusMinusAverage.i3[1].set((1, 1, 1))
                plusMinusAverage.operation.set(2)
                md = shadingNode('multiplyDivide', asUtility=1,
                                 n=i.split('|')[-1] + "Id" + str(t) + 'multiplyDivideS')
                nodeList.append(md)
                plusMinusAverage.o3 >> md.i1
                remapValueList[size][t].ov >> md.i2x
                remapValueList[size][t].ov >> md.i2y
                remapValueList[size][t].ov >> md.i2z
                md.o >> plusMinusAverageOut.i3[t]
            plusMinusAverageOut.i3[len(remapValueList[size])].set((1, 1, 1))
            plusMinusAverageOut.operation.set(1)
            plusMinusAverageOut.o3 >> i.s
            size = size + 1

        for con in ConList:
            UVal = con.U.get()
            rangeVal = con.range.get()
            if UVal != 0:
                addAttr(con.U, e=1, dv=UVal)
                addAttr(con.range, e=1, dv=UVal)
            # select(con.cv, r=1)
            # move(0, 2.0*size, 0, r=1, ws=1)

        doMoveGrp = group((Curve, Nurbs, follicleList), n=name + 'SlideDoMoveGrp')
        doMoveGrp.inheritsTransform.set(0)
        doMoveGrp.v.set(0, lock=1)
        parent(doMoveGrp, ConGrpList, sliderGrp)
        delete(jointList)
        parent(sliderGrp, scaleObj)
        return sliderGrp, remapValueList, nodeList


# 本类实现了加减节点的列表初始化输入为链表节点数、链表维度。可选参数链表名称
class addLinkedList:
    # 初始化
    def __init__(self, size, Dimension, **Inname):
        sel = selected()
        name = 'plusMinusAverage'
        Dimension = str(Dimension)
        if 'n' in Inname:
            name = Inname['n']
        if 'name' in Inname:
            name = Inname['name']
        out = [createNode('plusMinusAverage', n=name + str(i + 1)) for i in range(size)]
        for i in range(len(out) - 1):
            outAttr = general.PyNode(out[i] + '.o' + Dimension)
            inAttr = general.PyNode(out[i + 1] + '.i' + Dimension)
            outAttr >> inAttr[0]
        self.Dimension = Dimension  # 维度
        self.name = name  # 链表名称
        self.size = size  # DG节点数
        self.DG = out  # DG节点列表
        self.ID = [0] + [1 for i in range(1, size)]  # ID列表
        self.currentDG = self.DG[0]  # 当前DG节点
        self.current = 0  # 当前节点号
        select(sel, r=1)

    # 设置链表属性数值
    def set(self, value, attr):
        for i in self.DG:
            Attr = general.PyNode(i + '.' + attr)
            Attr.set(value)
        return 0

    # 获得链表属性数值
    def get(self, attr):
        out = []
        for i in self.DG:
            Attr = general.PyNode(i + '.' + attr)
            out.append(Attr.get())
        return out

    # 连接链表节点
    def con(self, outattr, inattr):
        outattr = general.PyNode(outattr)
        for i in self.DG:
            Attr = general.PyNode(i + '.' + inattr)
            outattr >> Attr
        return 0

    # 删除链表
    def delete(self):
        delete(self.DG)
        self.DG = []
        self.ID = []
        self.size = 0

    # 添加链表数
    def add(self):
        sel = selected()
        self.DG.append(createNode('plusMinusAverage', n=self.name + str(self.size)))
        outAttr = general.PyNode(self.DG[-2] + '.o' + self.Dimension)
        inAttr = general.PyNode(self.DG[-1] + '.i' + self.Dimension)
        outAttr >> inAttr[0]
        self.size = self.size + 1
        select(sel, r=1)
        return 0

    # 获得链表每属性列表
    def getattr(self, attr):
        return [general.PyNode(i + '.' + attr) for i in self.DG]

    # 迭代器
    def it(self):
        if self.current < self.size - 1:
            self.current = self.current + 1
            self.currentDG = self.DG[self.current]
        else:
            return 1
        return 0

    # 当前DG节点
    def getItDG(self):
        if self.currentDG == None:
            error('迭代未开始')
        return self.currentDG

    # 输入连接
    def inCon(self, inAttr):
        inAttr = general.PyNode(inAttr)
        Attr = general.PyNode(self.currentDG + '.i' + str(self.Dimension))
        inAttr >> Attr[self.ID[self.current]]
        self.ID[self.current] = self.ID[self.current] + 1
        return 0

    # 输出连接
    def outCon(self, inAttr):
        inAttr = general.PyNode(inAttr)
        Attr = general.PyNode(self.currentDG + '.o' + str(self.Dimension))
        Attr >> inAttr
        return 0

    # 初始化
    def initIt(self):
        self.current = 0
        self.currentDG = self.DG[self.current]
        return 0

    # 反转
    def Reverse(self):
        self.DG = self.DG[::-1]
        self.ID = self.ID[::-1]
        return 0


# 本类实现了乘除节点的列表初始化输入为链表节点数。可选参数链表名称
class multiplyDivideLinkedList():
    # 初始化
    def __init__(self, size, **Inname):
        sel = selected()
        name = 'multiplyDivide'
        if 'n' in Inname:
            name = Inname['n']
        if 'name' in Inname:
            name = Inname['name']
        out = [createNode('multiplyDivide', n=name + str(i + 1)) for i in range(size)]
        for i in range(len(out) - 1):
            outAttr = general.PyNode(out[i] + '.o')
            inAttr = general.PyNode(out[i + 1] + '.i1')
            outAttr >> inAttr
        self.name = name  # 链表名称
        self.size = size  # DG节点数
        self.DG = out  # DG节点列表
        self.DgIf = [0 for i in range(0, size)]  # 连接判断列表
        self.currentDG = self.DG[0]  # 当前DG节点
        self.current = 0  # 当前节点号
        select(sel, r=1)

    # 设置链表属性数值
    def set(self, value, attr):
        for i in self.DG:
            Attr = general.PyNode(i + '.' + attr)
            Attr.set(value)
        return 0

    # 获得链表属性数值
    def get(self, attr):
        out = []
        for i in self.DG:
            Attr = general.PyNode(i + '.' + attr)
            out.append(Attr.get())
        return out

    # 连接链表节点
    def con(self, outattr, inattr):
        outattr = general.PyNode(outattr)
        for i in self.DG:
            Attr = general.PyNode(i + '.' + inattr)
            outattr >> Attr
        return 0

    # 删除链表
    def delete(self):
        delete(self.DG)
        self.DG = []
        self.DgIf = []
        self.size = 0

    # 添加链表数
    def add(self):
        sel = selected()
        self.DG.append(createNode('multiplyDivide', n=self.name + str(self.size)))
        outAttr = general.PyNode(self.DG[-2] + '.o')
        inAttr = general.PyNode(self.DG[-1] + '.i1')
        outAttr >> inAttr
        self.size = self.size + 1
        select(sel, r=1)
        return 0

    # 获得链表每属性列表
    def getattr(self, attr):
        return [general.PyNode(i + '.' + attr) for i in self.DG]

    # 迭代器
    def it(self):
        if self.current < self.size - 1:
            self.current = self.current + 1
            self.currentDG = self.DG[self.current]
        else:
            return 1
        return 0

    # 当前DG节点
    def getItDG(self):
        if self.currentDG == None:
            error('迭代未开始')
        return self.currentDG

    # 输入连接
    def inCon(self, inAttr):
        inAttr = general.PyNode(inAttr)
        Attr = general.PyNode(self.currentDG + '.i2')
        if self.DgIf[self.current] != 0:
            warning('警告节点已被连接自动跳过')
            return 1
        inAttr >> Attr
        self.DgIf[self.current] = 1
        return 0

    # 输出连接
    def outCon(self, inAttr):
        inAttr = general.PyNode(inAttr)
        Attr = general.PyNode(self.currentDG + '.o')
        Attr >> inAttr
        return 0

    # 初始化
    def initIt(self):
        self.current = 0
        self.currentDG = self.DG[self.current]
        return 0

    # 反转
    def Reverse(self):
        self.DG = self.DG[::-1]
        self.DgIf = self.DgIf[::-1]
        return 0


# 迭代器类输入多个列表
class Iteration:
    def __init__(self, *inlist):
        self.it = None
        self.itList = None

        self.itList = inlist
        self.ID = 0
        self.it = [i[self.ID] for i in self.itList]
        self.max = min([len(i) for i in self.itList])

        if self.it is None:
            error('初始化失败')
        if self.itList is None:
            error('初始化失败')

    # 初始化当前迭代器
    def init(self, *inlist):
        return range(0, self.max)

    # 确定当前参数并将指针指向下一个
    def next(self):
        if self.ID < self.max - 1:
            self.ID = self.ID + 1
            self.it = [i[self.ID] for i in self.itList]
        else:
            return 1
        return 0


# todo: 适用于Python的迭代器
class ItPy:
    def __init__(self, *inList):
        self.C = Iteration(*inList)
        self.list = inList
        self.max = min([len(i) for i in inList])

    # 获得输入列表
    def getList(self):
        return self.list

    # 获得反转行列后的列表
    def getReverseRow(self):
        return [[t[i] for t in self.list] for i in range(self.max)]

    # 获得去除重复的列表
    def Deduplication(self):
        return [list(set(i)) for i in self.list]

    # 获得查找列表元素类型后的列表
    def SearchType(self, Type):
        return [[t for t in i if type(t) == Type] for i in self.list]

    # 获得展开列表
    def BreakDown(self):
        o = []
        [o.append(i) if type(i) != type([]) else o.extend(i) for i in self.list]
        return o

    # 获得反转行列后的展开列表
    def reverseRowBreakDown(self):
        o = []
        [o.append(i) if type(i) != type([]) else o.extend(i) for i in self.getReverseRow()]
        return o
