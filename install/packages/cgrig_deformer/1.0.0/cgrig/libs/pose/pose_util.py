import maya.cmds as mc
import math
import traceback
from cgrig.libs.api_lib import bs_api
from cgrig.libs.naming import naming
from cgrig.libs import sdk_io
from cgrig.libs.maya.api import generic
from cgrig.libs.maya.cmds.rig import follicles
from cgrig.libs.maya.cmds.mesh import mesh, shape
from maya import OpenMaya, cmds
import pymel.core as pm
from cgrig.libs.pose import pose_exceptions as exceptions
from maya.api import OpenMaya as om2
from maya.api import OpenMayaAnim as oma2


class LEditTargetJob(object):

    def __init__(self, src, dst, target):
        self.del_job()
        self.bs = get_bs(dst)
        self.index = get_index(self.bs, target)
        self.src = src
        bs_api.cache_target(self.bs, self.index, dst, get_orig(dst))
        mc.scriptJob(attributeChange=[mc.listRelatives(src, s=1)[0] + ".outMesh", self])

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self):
        bs_api.set_target(self.bs, self.index, self.src)

    def add_job(self):
        self.del_job()

    @classmethod
    def del_job(cls):
        for job in mc.scriptJob(listJobs=True):
            if repr(cls.__name__) in job:
                mc.scriptJob(kill=int(job.split(":")[0]))


def get_index(node, alias_name):
    if node is None:
        return
    parent_attr = mc.attributeQuery(alias_name, node=node, ln=1)
    parent_name = "{node}.{parent_attr}".format(**locals())
    elem_names = mc.listAttr(parent_name, m=1)
    elem_indexes = mc.getAttr(parent_name, mi=1)
    if alias_name in elem_names:
        return elem_indexes[elem_names.index(alias_name)]


def getBaseIndex(blendshape: str, base: str) -> str:
    """
    Get the index for a given base geometry

    :param blendshape: blendshape node
    :param base: base node
    :return:
    """
    # get the blendshape as a geometry filter
    deformerObj = generic.asMObject(blendshape)
    deformFn = oma2.MFnGeometryFilter(deformerObj)

    # get the deforming shape and an mObject for it.
    deformingShape = follicles.getDeformShape(base)
    deformingShapeMObj = generic.asMObject(deformingShape)

    return deformFn.indexForOutputShape(deformingShapeMObj)


def get_orig(polygon):
    orig_list = [shape for shape in mc.listRelatives(polygon, s=1) if mc.getAttr(shape+'.io')]
    orig_list.sort(key=lambda x: len(set(mc.listConnections(x, s=0, d=1, ) or [])))
    if orig_list:
        return orig_list[-1]
    else:
        return mc.listRelatives(polygon, s=1)[0]


def getOrigShape(node):
    """
    Get an orig shape from the given geometry node

    :param node:  geometry or deformer name to get the orig shape for
    :return: orig shape or orig shape output plug
    """
    deformShape = follicles.getDeformShape(node)
    origShape = naming.getFirst(cmds.deformableShape(deformShape, originalGeometry=True))

    origShape = origShape.split(".")[0]
    return origShape


def check_bs(fun):
    def check_fun(bs, *args, **kwargs):
        if not bs:
            return
        if is_shape(bs):
            bs = get_bs(bs)
        return fun(bs, *args, **kwargs)
    return check_fun


def check_target(fun):
    def check_fun(bs, target, *args, **kwargs):
        if not mc.objExists(get_bs_attr(bs, target)):
            return
        fun(bs, target, *args, **kwargs)
    return check_fun


def get_bs(polygon):
    bs = find_bs(polygon)
    if bs is None:
        bs = mc.blendShape(polygon, automatic=True, n=polygon.split("|")[-1] + "_bs")[0]
    return bs


def getPlugAttrs(nodes, attrType="keyable"):
    """Get a list of attributes to display to the user

    Args:
        nodes (str): name of node to attr query
        keyable (bool, optional): should the list only be kayable attrs

    Returns:
        list: list of attrplugs
    """
    plugAttrs = []
    if len(nodes) >= 2:
        print("the number of node is more than two")

    for node in nodes:
        if attrType == "all":
            attrs = mc.listAttr(node, se=True, u=False)
            aliasAttrs = mc.aliasAttr(node, q=True)
            if aliasAttrs is not None:
                try:
                    attrs.extend(aliasAttrs[0::2])
                except Exception:
                    pass
        elif attrType == "cb":
            attrs = mc.listAttr(node, se=True, u=False, cb=True)
        elif attrType == "keyable":
            attrs = mc.listAttr(node, se=True, u=False, keyable=True)
        if attrs is None:
            continue
        [plugAttrs.append("{}.{}".format(node, a)) for a in attrs]
    return plugAttrs


def is_shape(polygon_name, typ="mesh"):
    # 判断物体是否存在
    if not mc.objExists(polygon_name):
        return False
    # 判断类型是否为transform
    if mc.objectType(polygon_name) != "transform":
        return False
    # 判断是否有形节点
    shapes = mc.listRelatives(polygon_name, s=1, f=1)
    if not shapes:
        return False
    # 判断形节点类型是否时typ
    if mc.objectType(shapes[0]) != typ:
        return False
    return True


def is_on_duplicate_edit():
    return mc.objExists("cgrig_duplicate_edit")


def find_bs(polygon):
    # 查找 模型 blend shape
    shapes = set(mc.listRelatives(polygon, s=1))
    for bs in mc.ls(mc.listHistory(polygon), type="blendShape"):
        if mc.blendShape(bs, q=1, g=1)[0] in shapes:
            return bs


def get_selected_polygons():
    return list(filter(is_shape, mc.ls(sl=1, o=1)))


def get_selected_blend_shapes():
    return list(filter(bool, map(find_bs, get_selected_polygons())))


def duplicate_polygon_by_target(target, polygon):
    root = "cgrig_duplicate_edit"
    parent = "edit_"+ target
    # bs_name = get_bs(polygon)
    name = target + "_" + polygon.split("|")[-1]
    if not mc.objExists(root):
        mc.group(em=1, n=root)
    if not mc.objExists("|cgrig_duplicate_edit|"+parent):
        mc.group(em=1, n=parent, p=root)
    if mc.objExists(name):
        return name
    dup = mc.duplicate(polygon, n=name)[0]
    for shape in mc.listRelatives(dup, s=1):
        if mc.getAttr(shape + '.io'):
            mc.delete(shape)
    mc.parent(dup, parent)
    for shape in mc.listRelatives(dup, s=1):
        mc.setAttr(shape + '.overrideEnabled', True)
        mc.setAttr(shape + '.overrideColor', 13)
    return dup


def finish_duplicate_edit():
    LEditTargetJob.del_job()
    root = "|cgrig_duplicate_edit"
    if not mc.objExists(root):
        return
    for target_group in mc.listRelatives(root):
        if target_group[:5] != "edit_":
            continue
        target = target_group[5:]
        for src in mc.listRelatives(target_group):
            if not is_shape(src):
                continue
            dst = src[len(target)+1:]
            if not is_shape(dst):
                continue
            edit_target(src, dst, target)
    mc.delete(root)


def driver_polygon_vis(attr, polygon, dup):
    mc.setDrivenKeyframe(polygon + ".v", cd=attr, dv=0.0, v=1, itt="linear", ott="linear")
    mc.setDrivenKeyframe(polygon + ".v", cd=attr, dv=0.99, v=1, itt="linear", ott="linear")
    mc.setDrivenKeyframe(polygon + ".v", cd=attr, dv=1.0, v=0, itt="linear", ott="linear")
    mc.setDrivenKeyframe(dup + ".v", cd=attr, dv=0.0, v=0, itt="linear", ott="linear")
    mc.setDrivenKeyframe(dup + ".v", cd=attr, dv=0.99, v=0, itt="linear", ott="linear")
    mc.setDrivenKeyframe(dup + ".v", cd=attr, dv=1.0, v=1, itt="linear", ott="linear")


def duplicate_polygon(attr, polygon, target):
    dup = duplicate_polygon_by_target(target, polygon)
    return dup


def get_bs_attr(bs, target):
    return bs + "." + target


def edit_target(src, dst, target):
    bs = find_bs(dst)
    add_target(bs, target)
    index = get_index(bs, target)
    bs_api.edit_target(bs, index, src, dst, get_orig(dst))


def get_target(attr):
    return attr.replace('.', '_')


def check_connect_attr(src, dst):
    animCurves = sdk_io.getAnimCurve(src, dst)
    if not animCurves:
        mc.setDrivenKeyframe(dst, cd=src, dv=0.0, v=0.0, itt="linear", ott="linear")
        mc.setDrivenKeyframe(dst, cd=src, dv=cmds.getAttr(src), v=1.0, itt="linear", ott="linear")


@check_bs
def connect_target(bs, attr, target):
    # target = get_target(attr)
    add_target(bs, target)
    check_connect_attr(attr, bs + '.' + target)


@check_bs
@check_target
def delete_target(bs, target):
    index = get_index(bs, target)
    mc.aliasAttr(get_bs_attr(bs, target), rm=1)
    mc.removeMultiInstance(bs + ".weight[%i]" % index, b=1)
    mc.removeMultiInstance(bs + ".it[0].itg[%i]" % index, b=1)


@check_bs
@check_target
def mirror_target(bs, src, dst):
    src_id = get_index(bs, src)
    add_target(bs, dst)
    dst_id = get_index(bs, dst)
    symmetric_cache = {key: mc.symmetricModelling(q=1, **{key: True}) for key in ["s", "t", "ax", "a"]}
    if src_id != dst_id:
        mc.blendShape(bs, e=1, rtd=[0, dst_id])
        mc.blendShape(bs, e=1, cd=[0, src_id, dst_id])
        mc.blendShape(bs, e=1, ft=[0, dst_id], sa="X", ss=1)
    else:
        mc.blendShape(bs, e=1, md=0, mt=[0, dst_id], sa="X", ss=1)
    for key, value in symmetric_cache.items():
        mc.symmetricModelling(**{key: value})


def mirror_by_targets(targets, polygons):
    target_mirrors = targets_to_mirror(targets)
    if not target_mirrors:
        return
    # add_by_targets([m for _, m in target_mirrors], polygons)
    for polygon in polygons:
        mirror_targets(polygon, target_mirrors)


def mirror_targets(polygon, names):
    bs = get_bs(polygon)
    for src, dst in names:
        mirror_target(bs, src, dst)


def targets_to_mirror(targets):
    target_mirrors = []
    for target in targets:
        other_side_target = naming.convertRLName(target)
        if other_side_target == target:
            continue
        target_mirrors.append([target, other_side_target])
    return target_mirrors


def add_target(bs, target):
    if mc.objExists(get_bs_attr(bs, target)):
        return
    elem_indexes = mc.getAttr(bs+".weight", mi=1) or []
    index = len(elem_indexes)
    for i in range(index):
        if i == elem_indexes[i]:
            continue
        index = i
        break
    bs_attr = bs+'.weight[%i]' % index
    mc.setAttr(bs+'.weight[%i]' % index, 1)
    mc.aliasAttr(target, bs_attr)
    bs_api.init_target(bs, index)


def connect_polygons(attr, polygons, target):
    for polygon in polygons:
        connect_target(polygon, attr, target)


def wireframe_planes():
    panels = mc.getPanel(all=True)
    for panel in panels:
        if mc.modelPanel(panel, ex=1):
            try:
                mc.modelEditor(panel, e=1, wireframeOnShaded=True)
            except RuntimeError:
                pass
    mc.select(cl=1)


def duplicate_edit_polygon(attr, polygon, target):
    dup = duplicate_polygon(attr, polygon, target)
    if attr:
        connect_target(polygon, attr, target)
        LEditTargetJob(dup, polygon, target)
    wireframe_planes()


def duplicate_edit_selected_polygons2(target_names, attr):
    polygons = get_selected_polygons()
    if len(polygons) == 0:
        return
    if len(target_names) == 0:
        return
    all_dup_polygons = []
    for target_name in target_names:
        # set_pose_by_target(target_name)
        dup_polygons = []
        for polygon in polygons:
            dup = duplicate_polygon_by_target(target_name, polygon)
            dup_polygons.append(dup)
        all_dup_polygons.append(dup_polygons)

    if attr:
        connect_polygons(attr, polygons, target_names[0])
    duplicate_edit_polygon(attr, polygons[0], target_names[0])
    if attr:
        LEditTargetJob(all_dup_polygons[0][0], polygons[0], target_names[0])
    wireframe_planes()


# ======================================================================================
# NOTE: MTransformationMatrix & MEulerRotation have different values for the same axis.
XFORM_ROTATION_ORDER = {
    'xyz': OpenMaya.MTransformationMatrix.kXYZ,
    'yzx': OpenMaya.MTransformationMatrix.kYZX,
    'zxy': OpenMaya.MTransformationMatrix.kZXY,
    'xzy': OpenMaya.MTransformationMatrix.kXZY,
    'yxz': OpenMaya.MTransformationMatrix.kYXZ,
    'zyx': OpenMaya.MTransformationMatrix.kZYX
}

EULER_ROTATION_ORDER = {
    'xyz': OpenMaya.MEulerRotation.kXYZ,
    'yzx': OpenMaya.MEulerRotation.kYZX,
    'zxy': OpenMaya.MEulerRotation.kZXY,
    'xzy': OpenMaya.MEulerRotation.kXZY,
    'yxz': OpenMaya.MEulerRotation.kYXZ,
    'zyx': OpenMaya.MEulerRotation.kZYX
}


def compose_matrix(position, rotation, scale, rotation_order='xyz'):
    """
    Compose a 4x4 matrix with given transformation.

    >>> compose_matrix((0.0, 0.0, 0.0), (90.0, 0.0, 0.0), (1.0, 1.0, 1.0))
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    """

    # create rotation ptr
    rot_script_util = OpenMaya.MScriptUtil()
    rot_script_util.createFromDouble(*[deg * math.pi / 180.0 for deg in rotation])
    rot_double_ptr = rot_script_util.asDoublePtr()

    # construct transformation matrix
    xform_matrix = OpenMaya.MTransformationMatrix()
    xform_matrix.setTranslation(OpenMaya.MVector(*position), OpenMaya.MSpace.kTransform)
    xform_matrix.setRotation(rot_double_ptr, XFORM_ROTATION_ORDER[rotation_order], OpenMaya.MSpace.kTransform)

    util = OpenMaya.MScriptUtil()
    util.createFromList(scale, 3)
    scale_pointer = util.asDoublePtr()
    xform_matrix.setScale(scale_pointer, OpenMaya.MSpace.kTransform)

    matrix = xform_matrix.asMatrix()
    return [matrix(m, n) for m in range(4) for n in range(4)]


def decompose_matrix(matrix, rotation_order='xyz'):
    """
    Decomposes a 4x4 matrix into translation and rotation.

    >>> decompose_matrix([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    ((0.0, 0.0, 0.0), (90.0, 0.0, 0.0))
    """
    if isinstance(matrix, (list, tuple)):
        mmatrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(matrix, mmatrix)
    else:
        mmatrix = matrix

    # create transformation matrix
    xform_matrix = OpenMaya.MTransformationMatrix(mmatrix)

    # get translation
    translation = xform_matrix.getTranslation(OpenMaya.MSpace.kTransform)

    # get rotation
    # @ref: https://github.com/LumaPictures/pymel/blob/master/pymel/core/datatypes.py
    # The apicls getRotation needs a "RotationOrder &" object, which is impossible to make in python...
    euler_rotation = xform_matrix.eulerRotation()
    euler_rotation.reorderIt(EULER_ROTATION_ORDER[rotation_order])
    rotation = euler_rotation.asVector()

    util = OpenMaya.MScriptUtil()
    util.createFromList([1.0, 1.0, 1.0], 3)
    scale_pointer = util.asDoublePtr()

    xform_matrix.getScale(scale_pointer, OpenMaya.MSpace.kTransform)

    scale_x = OpenMaya.MScriptUtil().getDoubleArrayItem(scale_pointer, 0)
    scale_y = OpenMaya.MScriptUtil().getDoubleArrayItem(scale_pointer, 1)
    scale_z = OpenMaya.MScriptUtil().getDoubleArrayItem(scale_pointer, 2)

    return (
        (translation.x, translation.y, translation.z),
        (rotation.x * 180.0 / math.pi, rotation.y * 180.0 / math.pi, rotation.z * 180.0 / math.pi),
        (scale_x, scale_y, scale_z)
    )


def euler_to_quaternion(rotation, rotation_order='xyz'):
    """
    Returns Euler Rotation as Quaternion

    >>> euler_to_quaternion((90, 0, 0))
    (0.7071, 0.0, 0.0, 0.70710))
    """
    euler_rotation = OpenMaya.MEulerRotation(
        rotation[0] * math.pi / 180.0,
        rotation[1] * math.pi / 180.0,
        rotation[2] * math.pi / 180.0
    )
    euler_rotation.reorderIt(EULER_ROTATION_ORDER[rotation_order])

    quat = euler_rotation.asQuaternion()
    return quat.x, quat.y, quat.z, quat.w


def quaternion_to_euler(rotation, rotation_order='xyz'):
    """
    Returns Quaternion Rotation as Euler

    quaternion_to_euler((0.7071, 0.0, 0.0, 0.70710))
    (90, 0, 0)
    """
    quat = OpenMaya.MQuaternion(*rotation)
    euler_rotation = quat.asEulerRotation()
    euler_rotation.reorderIt(EULER_ROTATION_ORDER[rotation_order])

    return euler_rotation.x * 180.0 / math.pi, euler_rotation.y * 180.0 / math.pi, euler_rotation.z * 180.0 / math.pi


def get_local_matrix_without_joint_orient(transform_name):
    """
    Removes the joint orient from the local matrix if the transform is a joint
    """
    if cmds.objectType(transform_name) == 'joint':
        joint_orient_matrix_list = compose_matrix(
            position=(0.0, 0.0, 0.0),
            rotation=cmds.getAttr("{joint}.jointOrient".format(
                joint=transform_name))[0]
            ,
            scale=(1.0, 1.0, 1.0)
        )
        joint_orient_matrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(joint_orient_matrix_list, joint_orient_matrix)
        inverse_joint_orient_matrix = joint_orient_matrix.inverse()

        object_space_matrix_list = cmds.xform(transform_name, query=True, matrix=True, objectSpace=True)
        object_space_matrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(object_space_matrix_list, object_space_matrix)

        m = object_space_matrix * inverse_joint_orient_matrix
        _, rotation, _ = decompose_matrix(m)
        translation, _, scale = decompose_matrix(object_space_matrix_list)

        return list(compose_matrix(translation, rotation, scale))

    return cmds.xform(transform_name, query=True, matrix=True, objectSpace=True)


def is_connected_to_array(attribute, array_attr):
    """
    Check if the attribute is connected to the specified array
    :param attribute :type str: attribute
    :param array_attr :type str array attribute
    :return :type int or None: int of index in the array or None
    """
    try:
        indices = cmds.getAttr(array_attr, multiIndices=True) or []
    except ValueError:
        return None
    for i in indices:
        attr = '{from_attr}[{index}]'.format(from_attr=array_attr, index=i)
        if attribute in (cmds.listConnections(attr, plugs=True) or []):
            return i
    return None


def get_next_available_index_in_array(attribute):
    # Get the next available index
    indices = cmds.getAttr(attribute, multiIndices=True) or []
    i = 0
    for index in indices:
        if index != i and i not in indices:
            indices.append(i)
        i += 1
    indices.sort()
    attrs = ['{from_attr}[{index}]'.format(from_attr=attribute, index=i) for i in indices]
    connections = [cmds.listConnections(attr, plugs=True) or [] for attr in attrs]
    target_index = len(indices)
    for index, conn in enumerate(connections):
        if not conn:
            target_index = index
            break
    return target_index


def message_connect(from_attribute, to_attribute, in_array=False, out_array=False):
    """
    Create and connect a message attribute between two nodes
    """
    # Generate the object and attr names
    from_object, from_attribute_name = from_attribute.split('.', 1)
    to_object, to_attribute_name = to_attribute.split('.', 1)

    # If the attributes don't exist, create them
    if not cmds.attributeQuery(from_attribute_name, node=from_object, exists=True):
        cmds.addAttr(from_object, longName=from_attribute_name, attributeType='message', multi=in_array)
    if not cmds.attributeQuery(to_attribute_name, node=to_object, exists=True):
        cmds.addAttr(to_object, longName=to_attribute_name, attributeType='message', multi=out_array)
    # Check that both attributes, if existing are message attributes
    for a in (from_attribute, to_attribute):
        if cmds.getAttr(a, type=1) != 'message':
            raise exceptions.MessageConnectionError(
                'Message Connect: Attribute {attr} is not a message attribute. CONNECTION ABORTED.'.format(
                    attr=a
                )
            )
    # Connect up the attributes
    try:
        if in_array:
            from_attribute = "{from_attribute}[{index}]".format(
                from_attribute=from_attribute,
                index=get_next_available_index_in_array(from_attribute)
            )

        if out_array:
            to_attribute = "{to_attribute}[{index}]".format(
                to_attribute=to_attribute,
                index=get_next_available_index_in_array(to_attribute)
            )

        return cmds.connectAttr(from_attribute, to_attribute, force=True)
    except Exception as e:
        cmds.error(traceback.format_exc())
        return False


def connect_attr(from_attr, to_attr):
    if not cmds.isConnected(from_attr, to_attr):
        cmds.connectAttr(from_attr, to_attr)


def get_attr(attr_name, as_value=True):
    """
    Get the specified attribute
    :param attr_name :type str: attribute name i.e node.translate
    :param as_value :type bool: return as value or connected plug name
    :return :type list or any: either returns a list of connections or the value of the attribute
    """
    # Check if the attribute is connected
    connections = cmds.listConnections(attr_name, plugs=True)
    if connections and not as_value:
        # If the attribute is connected and we don't want the value, return the connections
        return connections
    elif as_value:
        # Return the value
        return cmds.getAttr(attr_name)


def get_attr_array(attr_name, as_value=True):
    """
    Get the specified array attr
    :param attr_name :type str: attribute name i.e node.translate
    :param as_value :type bool: return as value or connected plug name
    :return :type list or any: either returns a list of connections or the value of the attribute
    """
    # Get the number of indices in the array
    indices = cmds.getAttr(attr_name, multiIndices=True) or []
    # Empty list to store the connected plugs
    connected_plugs = []
    # Empty list to store values
    values = []
    # Iterate through the indices
    for i in indices:
        # Get all the connected plugs for this index
        connections = cmds.listConnections('{attr_name}[{index}]'.format(attr_name=attr_name, index=i), plugs=True)
        # If we want the plugs and not values, store connections
        if connections and not as_value:
            connected_plugs.extend(connections)
        # If we want values, get the value at the index
        elif as_value:
            values.append(cmds.getAttr('{attr_name}[{index}]'.format(attr_name=attr_name, index=i)))
    # Return plugs or values, depending on which one has data
    return connected_plugs or values


def set_attr_or_connect(source_attr_name, value=None, attr_type=None, output=False):
    """
    Set an attribute or connect it to another attribute
    :param source_attr_name :type str: attribute name
    :param value : type any: value to set the attribute to
    :param attr_type :type str: name of the attribute type i.e matrix
    :param output :type bool: is this plug an output (True) or input (False)
    """
    # Type conversion from maya: python
    attr_types = {
        'matrix': list
    }
    # Check if we have a matching type
    matching_type = attr_types.get(attr_type, None)
    # If we have a matching type and the value matches that type, set the attr
    if matching_type is not None and isinstance(value, matching_type):
        cmds.setAttr(source_attr_name, value, type=attr_type)
    # If the value is a string and no type is matched, we want to connect the attributes
    elif isinstance(value, str):
        try:
            # Connect from left->right depending on if the source is output or input
            if output:
                if not cmds.isConnected(source_attr_name, value):
                    cmds.connectAttr(source_attr_name, value)
            else:
                if not cmds.isConnected(value, source_attr_name):
                    cmds.connectAttr(value, source_attr_name)
        except Exception as e:
            raise exceptions.PoseWranglerAttributeError(
                "Unable to {direction} {input} to '{output}'".format(
                    direction="connect" if value else "disconnect",
                    input=source_attr_name if output else value,
                    output=value if output else source_attr_name
                )
            )
    else:
        cmds.setAttr(source_attr_name, value)


def disconnect_attr(attr_name, array=False):
    """
    Disconnect the specified attribute
    :param attr_name :type str: attribute name to disconnect
    :param array :type bool: is this attribute an array?
    """
    attrs = []
    # If we are disconnecting an array, get the names of all the attributes
    if array:
        attrs.extend(cmds.getAttr(attr_name, multiIndices=True) or [])
    # Otherwise append the attr name specified
    else:
        attrs.append(attr_name)
    # Iterate through all the attrs listed
    for attr in attrs:
        # Find their connections and disconnect them
        for plug in cmds.listConnections(attr, plugs=True) or []:
            cmds.disconnectAttr(attr, plug)


def get_selection(_type=""):
    """
    Returns the current selection
    """
    return cmds.ls(selection=True, type=_type)


def set_selection(selection_list):
    """
    Sets the active selection
    """
    cmds.select(selection_list, replace=True)


class PoseWranglerContext(object):
    def __init__(self, current_solver, solvers):
        self._current_solver = current_solver
        self._solvers = solvers

    @property
    def current_solver(self):
        return self._current_solver

    @property
    def solvers(self):
        return self._solvers


class EditSolverContextManager(object):
    def __init__(self, api, current_solver):
        self._api = api
        self._current_solver = current_solver

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._api.edit_solver(edit=False, solver=self._current_solver)


def multiplyCombine(attrA='', attrB='', toAttr=''):
    """
    attrA * attrB to AttrC
    :param attrA:
    :param attrB:
    :param toAttr:
    :return:
    """
    combineNode = pm.createNode('multDoubleLinear', n='%s_combine_mdl' % (toAttr.replace('.', '_')), ss=1)
    mc.connectAttr(attrA, combineNode + '.input1', f=True)
    mc.connectAttr(attrB, combineNode + '.input2', f=True)
    mc.connectAttr(combineNode + '.output', toAttr, f=True)

    # return
    returnDict = {
        'input1': combineNode.i1.inputs(p=True)[0].name(),
        'input2': combineNode.i2.inputs(p=True)[0].name(),
        'output': toAttr
    }
    return returnDict

def constraintBridge(parentObj='', followObj='', parentHandle='', followHandle=''):
    """
    constraint bridge
    :param parentObj:
    :param followObj:
    :param parentHandle:
    :param followHandle:
    :return:
    """
    mc.pointConstraint(followObj, parentHandle, n=parentHandle + '_pc')
    constraintNode = mc.orientConstraint(followObj, parentHandle, n=parentHandle + '_oc', mo=True)[0]

    # rotateOffset
    offsetX = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetX'))
    offsetY = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetY'))
    offsetZ = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetZ'))
    rotateOffset = [offsetX, offsetY, offsetZ]

    # normalize
    normalizeRotate = [round(rE / 90.0) * 90 for rE in rotateOffset]
    mc.setAttr('{0}.{1}'.format(constraintNode, 'offset'), *normalizeRotate)
    mc.delete(constraintNode)

    # final constraint
    mc.orientConstraint(parentObj, parentHandle, n=parentHandle + '_oc', mo=True)
    mc.parentConstraint(followObj, followHandle, n=followHandle + '_prc', mo=True)


def scaleBridge(prefix='', value=0.5):
    """
    scale pose driver
    :param prefix:
    :param value:
    :return:
    """

    # init data
    parentHandle = '{0}_psd_parent_handle'.format(prefix)
    followHandle = '{0}_psd_follow_handle'.format(prefix)

    # if not find Parent handle, return.
    if not mc.objExists(parentHandle) or not mc.objExists(followHandle):
        return
    mc.scale(value, value, value, '{0}.cv[*]'.format(parentHandle), '{0}.cv[*]'.format(followHandle))

    # scale tranlate
    constrainNode = mc.parentConstraint(followHandle, q=True)

    if constrainNode:
        attrStr = '{0}.tg[0].tot'.format(constrainNode)
    else:
        attrStr = '{0}.t'.format(followHandle)

    for axisE in 'xyz':
        fullAttrStr = '{0}{1}'.format(attrStr, axisE)
        mc.setAttr(fullAttrStr, mc.getAttr(fullAttrStr) * value)

def remapSDK(toAttr='', dv=0.0, v=0.0, cd=''):
    """
    use remapValue node instance setDrivenKey node
    :param toAttr:
    :param dv:
    :param v:
    :param cd:
    :return:
    """

    # createNode
    rvNode = '{0}_rv'.format(toAttr.replace('.', '_'))

    if not mc.objExists(rvNode):
        mc.createNode('remapValue', n=rvNode)
        mc.removeMultiInstance('{0}.value[1]'.format(rvNode), b=True)
        mc.removeMultiInstance('{0}.value[0]'.format(rvNode), b=True)

        # connect
        mc.connectAttr(cd, '{0}.inputValue'.format(rvNode))
        mc.connectAttr('{0}.outValue'.format(rvNode), toAttr)

    # get Index
    index = 0
    attrList = mc.listAttr(rvNode + '.value', m=True)
    if attrList:
        index = len(attrList) // 4

    # setValue
    mc.setAttr('{0}.value[{1}].value_Position'.format(rvNode, index), dv)
    mc.setAttr('{0}.value[{1}].value_FloatValue'.format(rvNode, index), v)
    mc.setAttr('{0}.value[{1}].value_Interp'.format(rvNode, index), 1)


def getBaseGeometry(blendshape):
    """
    Get a list of blendshape geometry

    :param str blendshape: blendshape name to get the base geometry from
    """
    deformerObj = generic.asMObject(blendshape)
    deformFn = oma2.MFnGeometryFilter(deformerObj)

    baseObject = deformFn.getOutputGeometry()
    outputNode = om2.MFnDagNode(baseObject[0])

    return outputNode.partialPathName()


def inbetweenToIti(inbetween) -> int:
    """Convert the inbetween float an inputTargetItem index"""
    return int((float(inbetween) * 1000) + 5000)


def getInputTargetItemAttr(blendshape: str, baseIndex: int, targetIndex: int, inputTargetItem: int = None):
    """
    Get the input target item attribute for a blendshape

    :param blendshape: blendshape node
    :param baseIndex: base index of the blendshape
    :param targetIndex: blendshape target index
    :param inputTargetItem: unique identifier for each target index (index = wt * 1000 + 5000)
    :return:
    """
    targetItemAttr = f"{blendshape}.inputTarget[{baseIndex}].inputTargetGroup[{targetIndex}].inputTargetItem"
    if inputTargetItem:
        targetItemAttr += f"[{inputTargetItem}]"
    return targetItemAttr


def getInputTargetItemList(blendshape, target, base=None):
    """
    Get the input targetItem attribute from a blendshape node and a target.
    This is handy if we want to rebuild the targets from deltas
    or just check if nodes are connected to the targets already

    :param blendshape: name of the blendshape node to get the target item plug
    :param target: name of the blendshape target to check
    :param base: Optional pass in a specific base to query from.
    :return:
    """

    targetIndex = get_index(blendshape, target)

    if not base:
        base = getBaseGeometry(blendshape)
    baseIndex = getBaseIndex(blendshape, base)
    targetItemAttr = getInputTargetItemAttr(blendshape, baseIndex, targetIndex)

    indices = cmds.getAttr(targetItemAttr, multiIndices=True)
    return indices


def getDelta(
    blendshape: str, target: str, inbetween: float = None, prune: int = 5
):
    """
    Gather the deltas for each vertex in a blendshape node.

    To optimize the dictonary prune any deltas with a magnitude below 0.0001.
    This returns a dictonary containing only the deltas of vertices that have been modified

    :param blendshape: name of the blendshape to gather blendshape data from.
    :param target: name of the target to gather the delta information for
    :param inbetween: inbetween weight value Specify to get the delta of a specific target
    :param prune: number of decimal places to prune from position delta
    :return: a dictionary containing the vertex ID as the key, and a tuple representing the delta
    """
    targetIndex = get_index(blendshape, target)

    base = getBaseGeometry(blendshape)
    baseIndex = getBaseIndex(blendshape, base)

    inputTargetItem = 6000 if not inbetween else inbetweenToIti(inbetween)

    inputTargetItemPlug = getInputTargetItemAttr(blendshape, baseIndex, targetIndex, inputTargetItem)
    geoTargetPlug = "{}.igt".format(inputTargetItemPlug)

    deltaPointList = dict()

    if len(cmds.listConnections(geoTargetPlug, source=True, destination=False) or list()) > 0:
        inputShape = cmds.listConnections(geoTargetPlug, source=True, destination=False, plugs=True)
        inputShape = inputShape[0].split(".")[0]
        origShape = getOrigShape(base)
         # TODO: add a check to support live connections to nurbs curves as well.
        targetPoints = mesh.getVertPositions(inputShape, world=False)
        origPoints = mesh.getVertPositions(origShape, world=False)

        deltaPointList = dict()
        for i in range(len(targetPoints)):
            offset = om2.MVector(targetPoints[i]) - om2.MVector(origPoints[i])

            # check if the magnitude is within a very small vector before adding it.
            # This will help us cut down on file sizes.
            if offset.length() >= 0.0001:
                deltaPointList[str(i)] = (
                    round(offset.x, prune),
                    round(offset.y, prune),
                    round(offset.z, prune),
                )

    else:
        pointsTarget = cmds.getAttr("{}.ipt".format(inputTargetItemPlug))
        componentsTarget = naming.flattenList(cmds.getAttr("{}.ict".format(inputTargetItemPlug)))

        for point, componentTarget in zip(pointsTarget, componentsTarget):
            vertexId = componentTarget.split("[")[-1].split("]")[0]

            prunedPoint = (
                round(point[0], prune),
                round(point[1], prune),
                round(point[2], prune),
            )
            deltaPointList[vertexId] = prunedPoint

    return deltaPointList


def createCleanMesh(dupGeo, origShape) -> str:
    """Create a clean version of geo for a mesh"""
    shapes = cmds.listRelatives(dupGeo, s=True)

    # get the point positions of the orig shape
    origPoints = mesh.getVertPositions(origShape, world=False)

    # delete all intermediate shapes
    for eachShape in shapes:
        if cmds.getAttr("{}.intermediateObject".format(eachShape)):
            cmds.delete(eachShape)

    # set the point positions the ones from the orig shape
    mesh.setVertPositions(dupGeo, vertList=origPoints, world=False)

    return dupGeo


def createCleanGeo(geo, name=None):
    """
    create a completely clean version of the given geo. To do this we will revert the mesh to the shape of the orig shape

    :param geo: name of the geometry to create a clean shape for
    :param name: name for the newly created clean geometery
    :return:
    """
    dupGeo = cmds.duplicate(geo)[0]
    if not name:
        name = "{}_clean".format(geo)

    dupGeo = cmds.rename(dupGeo, name)
    origShape = getOrigShape(geo)

    if shape.getType(dupGeo) == shape.MESH:
        return createCleanMesh(dupGeo, origShape)
    else:
        raise NotImplementedError(f"Shape types are not currently supported")


def reconstructTargetFromDelta(blendshape, deltaDict, name=None):
    """
    Reconstruct a blendshape target from a given delta dictionary.
    The deltaDict contains a vertex ID and a delta position per item.
    If no delta exists for the given vertex ID default to the position from the orig shape

    :param blendshape: blendshape node to reconstruct the delta for. This is used for gathering the orig shape.
    :param deltaDict: delta data dictionary of deltas for vertex IDs
    :param name: name the newly created target
    :return: New blendshape target mesh from delta
    """
    base = getBaseGeometry(blendshape)
    origShape = getOrigShape(base)
    origShapePoints = mesh.getVertPositions(origShape, world=False)

    targetGeo = createCleanGeo(base, name=name)

    for vertexId in list(deltaDict.keys()):
        origPoint = om2.MPoint(origShapePoints[int(vertexId)])
        delta = om2.MVector(deltaDict[vertexId])

        absPoint = origPoint + delta
        absPoint = [absPoint.x, absPoint.y, absPoint.z]

        cmds.xform(
            "{}.vtx[{}]".format(targetGeo, vertexId),
            objectSpace=True,
            translation=absPoint,
        )

    return targetGeo


def regenerateTarget(blendshape, target, inbetween=None, connect=True):
    """
    为指定的混合变形目标（target）重新生成一个可编辑的实时目标网格。
    核心功能：通过读取混合变形节点的delta（差值）数据重建目标网格，并可选连接到混合变形节点的输入几何目标接口，
    支持基础目标和中间目标（inbetween）的重建。

    :param blendshape: str，混合变形节点（blendShape node）的名称或路径，是操作的核心节点
    :param target: str，要重新生成的目标（target）名称（即混合变形中的单个目标权重对应的形状）
    :param inbetween: float/int，可选参数，中间目标（inbetween target）的权重值。
                     若为None，重建基础目标；若指定具体值，重建对应权重的中间目标
    :param connect: bool，可选参数，默认True。是否将重建的目标网格连接到混合变形节点的输入几何目标接口（igt）
    :return: str，新创建的重建目标网格（transform节点）的名称
    """
    # 获取目标（target）在混合变形节点中的索引（用于定位该目标的相关数据）
    targetIndex = get_index(blendshape, target)
    # 获取混合变形的基础几何体（base geometry）——即变形前的原始模型
    base = getBaseGeometry(blendshape)
    # 获取基础几何体在混合变形节点中的索引（用于定位基础几何对应的目标数据）
    baseIndex = getBaseIndex(blendshape, base)

    # 计算输入目标项索引（inputTargetItem/iti）：
    # - 基础目标（无inbetween）固定使用6000作为iti索引
    # - 中间目标通过inbetweenToIti函数将权重值转换为对应的iti索引（Maya内部映射规则）
    inputTargetItem = 6000 if not inbetween else inbetweenToIti(inbetween)

    # 构造混合变形节点中输入目标项的属性插头（plug）路径：
    # 格式：blendshape.it[基础几何索引].itg[目标索引].iti[输入目标项索引]
    # 其中：
    # - it: inputTarget（输入目标）
    # - itg: inputTargetGroup（输入目标组）
    # - iti: inputTargetItem（输入目标项，对应基础/中间目标）
    inputTargetItemPlug = "{}.it[{}].itg[{}].iti[{}]".format(
        blendshape, baseIndex, targetIndex, inputTargetItem
    )

    # 检查指定的中间目标（inbetween）是否存在于该混合变形目标中
    if inputTargetItem not in getInputTargetItemList(blendshape, target):
        # 若不存在，抛出值错误，提示具体的混合变形节点、目标名称和中间目标权重
        raise ValueError(
            "No inbetween exists for '{}.{}' at the inbetween {}".format(
                blendshape, target, inbetween
            )
        )

    # 检查当前输入目标项的igt（inputGeometryTarget）属性是否已连接到几何体：
    # cmds.listConnections查询该插头的源连接（source=True表示查输入连接），仅返回插头（plugs=True）
    if cmds.listConnections(
        "{}.igt".format(inputTargetItemPlug),  # 完整的igt属性路径
        source=True, destination=False, plugs=True
    ):
        # 若已连接，打印提示信息并直接返回（无需重复重建）
        print("{}.{} is already connected to input geometry".format(blendshape, target))
        return

    # 若未连接，则执行目标重建流程
    else:
        # 构建中间目标的名称：
        # - 基础目标直接使用原始target名称
        # - 中间目标命名规则：目标名_ib[权重值]（权重中的.替换为_，-替换为neg避免非法字符）
        ibName = "{}_ib{}".format(
            target, str(inbetween).replace(".", "_").replace("-", "neg")
        )
        targetGeoName = target if not inbetween else ibName

        # 从混合变形节点中获取目标的delta数据（delta：目标形状与基础形状的顶点差值信息）
        deltaDict = getDelta(blendshape, target, inbetween=inbetween)

        # 利用delta差值数据重建目标网格：
        # 基于基础几何体，应用delta差值得到目标形状，命名为targetGeoName
        targetGeo = reconstructTargetFromDelta(
            blendshape, deltaDict=deltaDict, name=targetGeoName
        )

        # 获取重建目标网格的形状节点（shape node）：
        # cmds.listRelatives(shapes=True)返回transform节点下的所有形状节点，取第一个（通常仅一个）
        targetGeoShape = cmds.listRelatives(targetGeo, shapes=True)[0]

        # 若connect参数为True（默认），将重建的目标形状连接到混合变形的igt属性
        if connect:
            cmds.connectAttr(
                "{}.worldMesh[0]".format(targetGeoShape),  # 形状节点的世界网格属性（输出几何）
                "{}.igt".format(inputTargetItemPlug),       # 混合变形的输入几何目标属性（输入接口）
                force=True,  # 强制连接（若有旧连接则替换，确保连接生效）
            )

        # 返回重建的目标网格（transform节点）名称
        return targetGeo
