# -*- coding: utf-8 -*-
from functools import reduce
from maya import cmds
from maya.api import OpenMaya
from . import api_utils as api
from pymel import core as pm


def get_shapes(node, full_path=False):
    """Return shapes of the given node."""
    return cmds.listRelatives(node, c=True, shapes=True, path=True, fullPath=full_path)


def get_parent(node, full_path=False):
    """Return the parent of the given node."""
    parent_list = cmds.listRelatives(node, parent=True, path=True, fullPath=full_path)
    return parent_list[0] if parent_list else None


def align_to_normal(node, normal_vector):
    """
    Aligns the object according to the given normal vector
    Args:
        node: The node to be aligned
        normal_vector: Alignment vector

    Returns: None

    """
    # create a temporary alignment locator
    temp_target = cmds.spaceLocator(name="tempAlignTarget")[0]
    align_to(temp_target, node)
    cmds.makeIdentity(temp_target, a=True)
    cmds.move(normal_vector[0], normal_vector[1], normal_vector[2], temp_target)
    cmds.delete(cmds.aimConstraint(temp_target, node, aim=(0, 1, 0), mo=False))
    cmds.delete(temp_target)


def align_to_alter(node1, node2, mode=0, offset=(0, 0, 0)):
    """
    Aligns the first node to the second. Alternative method to alignTo
    Args:
        node1: (String) Node to be aligned.
        node2: (String) Target Node.
        mode: (int) the alignment Mode. Valid Values: 0=position only, 1=Rotation Only, 2=Position and Rotation
        offset: (Tuple or List) Offset Value. Default: (0,0,0)

    Returns:None

    """
    if mode == 0:
        # Position Only
        cmds.delete(cmds.pointConstraint(node2, node1, mo=False))
    elif mode == 1:
        # Rotation Only
        cmds.delete(cmds.orientConstraint(node2, node1, o=offset, mo=False))
    elif mode == 2:
        # Position and Rotation
        cmds.delete(cmds.parentConstraint(node2, node1, mo=False))


def align_to(node, target, position=True, rotation=False):
    """
    This is the fastest align method. May not work in all cases
    www.rihamtoulan.com/blog/2017/12/21/matching-transformation-in-maya-and-mfntransform-pitfalls

    Args:
        node: (String) Node to be aligned
        target: (String) Align target
        position: (Bool) Match world position. Default True
        rotation: (Bool) Match rotation. Defaults to False

    Returns: None

    """

    node_m_transform = OpenMaya.MFnTransform(api.get_mdag_path(node))
    target_m_transform = OpenMaya.MFnTransform(api.get_mdag_path(target))
    if position:
        target_rotate_pivot = OpenMaya.MVector(target_m_transform.rotatePivot(OpenMaya.MSpace.kWorld))
        node_m_transform.setTranslation(target_rotate_pivot, OpenMaya.MSpace.kWorld)
    if rotation:
        target_mt_matrix = OpenMaya.MTransformationMatrix(
            OpenMaya.MMatrix(cmds.xform(target, matrix=True, ws=1, q=True)))
        # using the target matrix decomposition
        # Worked on all cases tested
        node_m_transform.setRotation(target_mt_matrix.rotation(True), OpenMaya.MSpace.kWorld)


def checkResult(**kw):
    """

    :param kw:
    :return:
    """
    d = {'allowPublish': None,
         'msg': '',
         'nodes': [],
         'warning': False}
    d.update(kw)
    raise d['allowPublish'] is True or d['allowPublish'] is False or AssertionError
    raise isinstance(d['msg'], str) or AssertionError
    raise type(d['nodes']) is list or AssertionError
    raise d['warning'] is True or d['warning'] is False or AssertionError
    return d


def listStorableAttrs(node, shortName=True, noCompound=True):
    """
    @brief List every attributes of a node who can go trough the pipeline and whose value will be stored.
    @return : List

    @param node - String - Node to get the attributes of.
    @param shortName - Bool - If True, return attributes short name.
    @param noCompound - Bool - If True, exclude compound attributes.
    """

    def __getShortName(node, attr, shortName):
        result = attr
        if shortName:
            names = attr.split('.')
            snames = []
            for name in names:
                if name.endswith(']'):
                    snames.append(name)
                else:
                    snames.append(pm.attributeQuery(name, node=node, shortName=True))

            result = '.'.join(snames)
        return result

    result = []

    if not pm.listAnimatable(node):
        return result
    for s in pm.listAnimatable(node):
        if noCompound:
            if len(s.split('.')) > 2:
                continue
        nodeName = s.split('.')[0]
        attr = '.'.join(s.split('.')[1:])
        if pm.nodeType(node) == pm.nodeType(nodeName):
            attr = __getShortName(node, attr, shortName)
            result.append(str(attr))

    attrs = pm.listAttr(node, cb=True)
    if attrs:
        for attr in attrs:
            attr = __getShortName(node, attr, shortName)
            result.append(str(attr))

    if pm.listAttr(node, userDefined=True):
        extra = [str(x) for x in pm.listAttr(node, userDefined=True) if
                 pm.getAttr('%s.%s' % (node, x), type=True) == 'string' if not x.startswith('rnkInit_') if
                 not pm.getAttr('%s.%s' % (node, x), lock=True)]
        if extra:
            result.extend(extra)
    return result


def SearchType(iList, Type):
    return [i for i in iList if type(i) == Type]


def listCompleteBreakDown(iList, limit):
    """
    递归
    :param iList:
    :param limit:
    :return:
    """
    if limit <= 0:
        return [None]
    o = []
    if type(iList) != type([]):
        o.append(iList)
    else:
        [o.append(i) if type(i) != type([]) else o.extend(listCompleteBreakDown(i, limit - 1)) for i in iList]
    return o


def listBreakDown(iList):
    o = []
    [o.append(i) if type(i) != type([]) else o.extend(i) for i in iList]
    return o


def Deduplication(iList):
    return list(set(iList))


def listCombine(iList):
    return reduce(lambda x, y: x if y in x else x + [y], [[], ] + iList)


def refresh_outliner():  # noqa
    """Refresh the Maya outliner"""
    eds = cmds.lsUI(editors=True)
    for ed in eds:
        if cmds.outlinerEditor(ed, exists=True):
            cmds.outlinerEditor(ed, e=True, refresh=True)


# TODO:拆分列表
def list_of_groups(list_info, per_list_len):
    """
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    """
    list_of_group = zip(*(iter(list_info),) * per_list_len)
    end_list = [list(i) for i in list_of_group]  # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list
