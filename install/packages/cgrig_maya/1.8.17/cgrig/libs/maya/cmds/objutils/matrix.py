# -*- coding: utf-8 -*-
"""cmds functions related to Offset Parent Matrix in Maya 2020 and above.

Example use:

.. code-block:: python

    from cgrig.libs.maya.cmds.objutils import matrix

Author: Andrew Silke

"""
from maya import cmds

from cgrig.libs.maya import zapi
from cgrig.libs.maya.api import nodes
from cgrig.libs.maya.cmds.objutils import attributes
from cgrig.libs.utils import output
from cgrig.libs.maya.utils import mayaenv
from cgrig.libs.maya.api import nodes
from cgrig.libs.utils import general
from maya.api import OpenMaya as om2


MAYA_VERSION = float(mayaenv.mayaVersionNiceName())
DEFAULT_MATRIX = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def hasMatrixOffset(transform):
    """Checks to see if a transforms Offset Parent Matrix (Composition) has been modified at all.

    Attribute: offsetParentMatrix

    :param transform: A maya transform node
    :type transform: str
    :return hasOffset: True if there is an offset, False if no offset
    :rtype hasOffset: bool
    """
    if cmds.getAttr("{}.offsetParentMatrix".format(transform)) == DEFAULT_MATRIX:  # no need to do anything
        return False
    return True


def selectionMatrixCheck(message=True):
    if MAYA_VERSION <= 2020.0:
        if message:
            output.displayWarning("The Offset Matrix settings are only in Maya 2020 and above. \n"
                                  "You will need to upgrade to use this tool.")
        return list()
    selObjs = cmds.ls(selection=True, type="transform")
    if not selObjs:
        if message:
            output.displayWarning("No transform objects are selected, please select an object/s")
        return list()
    return selObjs


# -----------------------
# Zero/Reset Matrix Offset
# -----------------------


def zeroMatrixOffset(transform, unlockAttrs=True):
    """Resets/zeros the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr of a single object.
    Maintains the current position/rotation/scale.

    :param transform: A maya transform node
    :type transform: str
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """
    if not hasMatrixOffset(transform):
        return
    if unlockAttrs:  # Unlocks/del keys/disconnects any connected SRT attributes
        attributes.unlockDisconnectSRT(transform)
    matrixTRS = cmds.xform(transform, q=True, matrix=True, worldSpace=True)
    cmds.setAttr("{}.offsetParentMatrix".format(transform), DEFAULT_MATRIX, type="matrix")
    cmds.xform(transform, matrix=matrixTRS, worldSpace=True)


def resetMatrixOffsetList(transformList, unlockAttrs=True):
    """Resets/zeros the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr of a list of objects.
    Maintains the current position/rotation/scale.

    :param transformList: A list of A maya transform node names
    :type transformList: list(str)
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """
    for transform in transformList:
        zeroMatrixOffset(transform, unlockAttrs=unlockAttrs)


def zeroMatrixOffsetSel(unlockAttrs=True, children=False, nodeType=None, message=True):
    """Resets/zeros the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr of the selected objects.
    Maintains the current position/rotation/scale.

    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    :param children: If True will also reset the children of the selected objects
    :type children: bool
    :param nodeType: If children is True will only reset the children of the selected objects of this nodeType
    :type nodeType: str
    :param message: report a message to the user?
    :type message: bool
    """
    selObjs = selectionMatrixCheck(message=message)
    if not selObjs:  # message already given
        return
    if children:
        selObjs = childrenByNodeType(selObjs, nodeType=nodeType)
    resetMatrixOffsetList(selObjs, unlockAttrs=unlockAttrs)
    if message:
        output.displayInfo("The Offset Matrix of the selected objects has been reset to zero.")


# -----------------------
# SRT to Matrix Offset And Back
# -----------------------
def childrenByNodeType(objList, nodeType="transform"):
    """retrieves all objs under the obj list in the hierarchy, all child joints

    :param objList: a list of Maya objects DAG nodes
    :type objList: list(str)
    :return allObjs: an obj list now including children
    :rtype allObjs: list(str)
    """
    allJoints = list()
    for obj in objList:
        allJoints.append(obj)
        if type:
            tempJntList = cmds.listRelatives(obj, allDescendents=True, type=nodeType, fullPath=True)
        else:
            tempJntList = cmds.listRelatives(obj, allDescendents=True, fullPath=True)
        if tempJntList:
            allJoints += tempJntList
    return list(set(allJoints))  # remove duplicates


def srtToMatrixOffset(transform, unlockAttrs=True):
    """Sets the transforms translate, rotate to be zero and the scale to be one and passes the information into \
    the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr
    For a single transform
    Maintains the current position/rotation/scale.

    # TODO could possibly be done by simple math on the scale/rot/trans values not sure

    :param transform: A maya transform node
    :type transform: str
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """
    if attributes.srtIsZeroed(transform):  # already frozen so bail
        return
    if unlockAttrs:  # Unlocks/del keys/disconnects any connected SRT attributes
        attributes.unlockDisconnectSRT(transform)
    if hasMatrixOffset(transform):  # if offset already then zero offsetParentMatrix values
        matrixTRS = cmds.xform(transform, q=True, matrix=True, worldSpace=True)
        cmds.setAttr("{}.offsetParentMatrix".format(transform), DEFAULT_MATRIX, type="matrix")
        cmds.xform(transform, matrix=matrixTRS, worldSpace=True)
    # Now switch vales back to the offsetParentMatrix
    matrixTRS = cmds.xform(transform, q=True, matrix=True, worldSpace=False)
    attributes.resetTransformAttributes(transform)  # zero SRT
    cmds.setAttr("{}.offsetParentMatrix".format(transform), matrixTRS, type="matrix")
    if cmds.objectType(transform) == "joint":
        cmds.setAttr("{}.jointOrient".format(transform), 0.0, 0.0, 0.0, type="float3")


def srtToMatrixOffsetList(transformList, unlockAttrs=True):
    """Sets the transforms translate, rotate to be zero and the scale to be one and passes the information into \
    the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr
    For a list of tranforms
    Maintains the current position/rotation/scale.

    :param transformList: A list of A maya transform node names
    :type transformList: list(str)
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """
    for transform in transformList:
        srtToMatrixOffset(transform, unlockAttrs=unlockAttrs)


def srtToMatrixOffsetSel(unlockAttrs=True, children=False, nodeType=None, message=True):
    """Sets the transforms translate, rotate to be zero and the scale to be one and passes the information into \
    the Offset Parent Matrix (Composition) ".offsetParentMatrix" attr
    For a the selected transforms
    Maintains the current position/rotation/scale.


    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    :param children: If True will also reset the children of the selected objects
    :type children: bool
    :param nodeType: If children is True will only reset the children of the selected objects of this nodeType
    :type nodeType: str
    :param message: report a message to the user?
    :type message: bool
    """
    selObjs = selectionMatrixCheck(message=message)
    if not selObjs:  # message already given
        return
    if children:
        selObjs = childrenByNodeType(selObjs, nodeType=nodeType)
    srtToMatrixOffsetList(selObjs, unlockAttrs=unlockAttrs)
    if message:
        output.displayInfo("The Offset Matrix is now handling the selected objects offsets. "
                           "Translate, rotate and scale have been zeroed")


# -----------------------
# Zero SRT Model Matrix Offset
# -----------------------


def zeroSrtModelMatrix(transform, unlockAttrs=True):
    """Modeller Matrix Zero SRT, this will zero SRT and move offsets to the offsetParentMatrix but will freeze \
    transforms for scale so the object can be rotated nicely.

    # TODO record the scale values so the freeze can be undone?

    :param transform: A maya transform node name
    :type transform: str
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """

    if attributes.srtIsZeroed(transform):  # already frozen so bail
        return
    if unlockAttrs:  # Unlocks/del keys/disconnects any connected SRT attributes
        attributes.unlockDisconnectSRT(transform)

    matrixTRS = cmds.xform(transform, q=True, matrix=True, worldSpace=True)

    # Zero the scale of the matrix ------------------
    node = zapi.nodeByName(transform)
    offsetTransform = zapi.TransformationMatrix(node.offsetParentMatrix.value())
    offsetTransform.setScale((1.0, 1.0, 1.0), zapi.kWorldSpace)
    cmds.setAttr("{}.offsetParentMatrix".format(transform), offsetTransform.asMatrix(), type="matrix")

    # return object to original position.
    cmds.xform(transform, matrix=matrixTRS, worldSpace=True)

    curScale = cmds.getAttr("{}.scale".format(transform))[0]
    cmds.setAttr("{}.scale".format(transform), 1.0, 1.0, 1.0, type="float3")

    # now move all values to the offset matrix
    srtToMatrixOffset(transform)

    # return the scale values and freeze scale
    cmds.setAttr("{}.scale".format(transform), curScale[0], curScale[1], curScale[2], type="float3")
    cmds.makeIdentity(transform, apply=True, translate=False, rotate=False, scale=True, normal=2)  # freeze scale


def zeroSrtModelMatrixList(transformList, unlockAttrs=True):
    """Modeller Matrix Zero SRT, this will zero SRT and move offsets to the offsetParentMatrix but will freeze \
    transforms for any scale so the object can be rotated nicely.

    Works on a list of transforms.

    :param transformList: A list of A maya transform node names
    :type transformList: list(str)
    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    """
    for transform in transformList:
        zeroSrtModelMatrix(transform, unlockAttrs=unlockAttrs)


def zeroSrtModelMatrixSel(unlockAttrs=True, children=False, nodeType=None, message=True):
    """Modeller Matrix Zero SRT, this will zero SRT and move offsets to the offsetParentMatrix but will freeze \
    transforms for any scale so the object can be rotated nicely.

    Works on selected transform objects.

    :param unlockAttrs: If True will unlock/del keys/disconnect any connected SRT attributes
    :type unlockAttrs: str
    :param children: If True will also reset the children of the selected objects
    :type children: bool
    :param nodeType: If children is True will only reset the children of the selected objects of this nodeType
    :type nodeType: str
    :param message: report a message to the user?
    :type message: bool
    """
    selObjs = selectionMatrixCheck(message=message)
    if not selObjs:  # message already given
        return
    if children:
        selObjs = childrenByNodeType(selObjs, nodeType=nodeType)
    zeroSrtModelMatrixList(selObjs, unlockAttrs=unlockAttrs)
    if message:
        output.displayInfo("The Offset Matrix is now handling the selected objects translation and rotation offsets. "
                           "Translate, rotate have been zeroed and scale has been frozen.")


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


def mirror_obj_with_matrix(source=None, target=None):
    mirrored_matrix = zapi.Matrix([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    dag_path_obj = nodes.asDagPath(source)
    original_matrix_obj = dag_path_obj.inclusiveMatrix()

    mirror_ma = original_matrix_obj * mirrored_matrix

    dag_path = nodes.asDagPath(target)

    # 创建 MFnTransform
    fn_transform = om2.MFnTransform(dag_path)

    # 将 MMatrix 转换为 MTransformationMatrix
    transform = om2.MTransformationMatrix(mirror_ma)

    # 设置物体的变换矩阵
    fn_transform.setTransformation(transform)


def getMirrorMatrix(source=None):
    mirrored_matrix = zapi.Matrix([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    dag_path_obj = nodes.asDagPath(source)
    original_matrix_obj = dag_path_obj.inclusiveMatrix()

    mirror_ma = original_matrix_obj * mirrored_matrix
    return mirror_ma


def isAttr(plug):
    """
    Check if the node is a valid Container

    :param str plug: Node to check
    :return: True if Valid. False is invalid.
    :rtype: bool
    """
    node = plug.split(".")[0]
    attr = plug.replace(node + ".", "")
    attrNoCompound = attr.split("[")[0]

    if cmds.attributeQuery(attrNoCompound, node=node, exists=True):
        return True
    return False


def offsetMatrix(node1, node2):
    """
    Calculate an offset matrix between two nodes.
    Returns the matrix of node2 relative to node 1

    :param node1: first node
    :param node2: second node
    :return: relative offset matrix between node1 and node2
    :rtype: MMatrix
    """

    node1Attr = node1 if isAttr(node1) else f"{node1}.worldMatrix"
    node2Attr = node2 if isAttr(node2) else f"{node2}.worldMatrix"

    node1Matrix = om2.MMatrix(cmds.getAttr(node1Attr))
    node2Matrix = om2.MMatrix(cmds.getAttr(node2Attr))

    # invert the parent matrix
    node1Inverted = om2.MTransformationMatrix(node1Matrix).asMatrixInverse()
    offset = node2Matrix * node1Inverted

    return offset


def resetTransformations(nodes):
    """
    Reset the channel box transformations of a given node.

    :param nodes: list of nodes to reset the transformations
    """
    nodes = general.toList(nodes)
    for node in nodes:
        for attr in ["jo", "ra"]:
            if cmds.objExists("{}.{}".format(node, attr)):
                cmds.setAttr("{}.{}".format(node, attr), 0, 0, 0)
        for attr in ["{}{}".format(x, y) for x in "trs" for y in "xyz"]:
            isLocked = cmds.getAttr("{}.{}".format(node, attr), lock=True)
            connection = (
                cmds.listConnections(
                    "{}.{}".format(node, attr), s=True, d=False, plugs=True
                )
                or []
            )
            isConnected = len(connection)
            if isLocked:
                cmds.setAttr("{}.{}".format(node, attr), lock=False)
            if isConnected:
                cmds.disconnectAttr(connection[0], "{}.{}".format(node, attr))

            value = 1.0 if attr.startswith("s") else 0.0
            cmds.setAttr("{}.{}".format(node, attr), value)
            if isConnected:
                cmds.connectAttr(connection[0], "{}.{}".format(node, attr), f=True)
            if isLocked:
                cmds.setAttr("{}.{}".format(node, attr), lock=True)


def connectOffsetParentMatrix(
    driver, driven, mo=False, t=True, r=True, s=True, sh=True
):
    """
    Create a connection between a driver and driven node using the offset parent matrix.
    the maintain offset option creates a transform node to store the offset.
    the t, r, s, sh attributes can be used to select only some transformations to affect the driven using a pickMatrix node.

    :param str driver: driver node
    :param str driven: driven node(s)
    :param bool mo: add a transform node to store the offset between the driver and driven nodes
    :param bool t: Apply translation transformations
    :param bool r: Apply rotation transformations
    :param bool s: Apply scale transformations
    :param bool sh: Apply shear transformations
    :return: multmatrix,  pickmatrix
    :rtype: list
    """

    if cmds.about(api=True) < 20200000:
        raise RuntimeError(
            "OffsetParentMatrix is only available in Maya 2020 and beyond"
        )
    drivens = general.toList(driven)

    driverIsAttr = True if isAttr(driver) else False

    if not driverIsAttr:
        driverAttr = "{}.{}".format(driver, "worldMatrix")
    else:
        driverAttr = driver
        driver = driver.split(".")[0]

    for driven in drivens:
        offset = list()
        if mo:
            offset = offsetMatrix(driverAttr, driven)

        parentList = cmds.listRelatives(driven, parent=True, path=True)
        parent = parentList[0] if parentList else None

        if not parent and not mo:
            outputPlug = "{}.{}".format(driver, "worldMatrix")
        else:
            multMatrix = cmds.createNode(
                "multMatrix", name="{}_{}_mm".format(driver, driven)
            )
            if offset:
                cmds.setAttr(
                    "{}.{}".format(multMatrix, "matrixIn[0]"), offset, type="matrix"
                )

            cmds.connectAttr(
                driverAttr, "{}.{}".format(multMatrix, "matrixIn[1]"), f=True
            )

            if parent:
                cmds.connectAttr(
                    "{}.{}".format(parent, "worldInverseMatrix"),
                    "{}.{}".format(multMatrix, "matrixIn[2]"),
                    f=True,
                )
            outputPlug = "{}.{}".format(multMatrix, "matrixSum")

        pickMat = None
        if not t or not r or not s or not sh:
            # connect the output into a pick matrix node
            pickMat = cmds.createNode(
                "pickMatrix", name="{}_{}_pickMatrix".format(driver, driven)
            )
            cmds.connectAttr(outputPlug, "{}.inputMatrix".format(pickMat))
            cmds.setAttr(pickMat + ".useTranslate", t)
            cmds.setAttr(pickMat + ".useRotate", r)
            cmds.setAttr(pickMat + ".useScale", s)
            cmds.setAttr(pickMat + ".useShear", sh)
            outputPlug = pickMat + ".outputMatrix"

        cmds.connectAttr(
            outputPlug, "{}.{}".format(driven, "offsetParentMatrix"), f=True
        )

        # now we need to reset the trs
        resetTransformations(driven)

    return multMatrix, pickMat


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
        driven_world_matrix = nodes.asDagPath(driven).inclusiveMatrix()
        if is_multi:
            driver_world_matrix = zapi.Matrix(cmds.getAttr(out_plug))
        else:
            driver_world_matrix = nodes.asDagPath(drivers).inclusiveMatrix()
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




