# -*- coding: utf-8 -*-
"""Module for assorted rigging related functions

Examples:

Example use:

.. code-block:: python

    # Unlock and unhide all nodes in a hierarchy.
    from cgrig.libs.maya.cmds.rig import riggingmisc
    riggingmisc.markCenterPivot(name="")

    # Unlock and unhide all nodes in a hierarchy.
    from cgrig.libs.maya.cmds.rig import riggingmisc
    riggingmisc.unlockUnhideAll()

 Author: Andrew Silke

"""

from maya import cmds

from cgrig.libs.utils import output
from cgrig.libs.maya.cmds.objutils import namehandling, locators, attributes
from cgrig.libs.maya.cmds.animation import resetattrs

TEMP_PIVOT_PREFIX = "tempPivot_loc"


def markCenterPivot(name=""):
    """Creates a locator with display handles on at the center pivot of the selection.

    Uses a cluster to mark the center point and then deletes it.

    :return locator:  The newly created locator
    :rtype locator: str
    """
    if not name:
        name = "{}_01".format(TEMP_PIVOT_PREFIX)
    return locators.createLocatorAndMatch(name=name, handle=True, locatorSize=0.1, message=True)


def deleteAllCenterPivots():
    """Deletes all the pivot locators in the scene named "tempPivot_loc"
    """
    pivots = cmds.ls("{}*".format(TEMP_PIVOT_PREFIX))
    pivLocators = list()
    for pivot in pivots:
        shapes = cmds.listRelatives(pivot, shapes=True)
        if not shapes:
            continue
        if cmds.nodeType(shapes[0]) == "locator":
            pivLocators.append(pivot)
    if pivLocators:
        cmds.delete(pivLocators)
        output.displayInfo("Success: Pivot locators deleted `{}`".format(pivLocators))


def bakeNamespaces():
    """replaces a namespace `:` character with `_` on an object selection list:

        ["rig:polyCube1", "rig:polyCube2"] becomes ["rig_polyCube1", "rig_polyCube2"]
    """
    namehandling.bakeNamespacesSel()


def selectionHighlightList(objs, highlight=True, message=True):
    """Turns on or off selection highlight for an object list.  Attribute selectionChildHighlighting

    If True then highlighting is on, if False then children are not highlighted when selected.

    Maya preferences must be set to "Use Object Highlight Setting":

        Windows > Settings Preferences > preferences > Settings > Selection > Selection Child Highlighting

    :param objs: A list of Maya objects transforms or shapes.
    :type objs: list(str)
    :param highlight: If True then highlighting is on, if False then children are not highlighted when selected.
    :type highlight: bool
    :param message: report a message to the user
    :type message: bool
    """
    for obj in objs:
        cmds.setAttr('{}.selectionChildHighlighting'.format(obj), highlight)
    if message:
        state = "off"
        if highlight:
            state = "on"
        output.displayInfo("Success: Selection highlighting {} `{}`".format(state, objs))


def selectionHighlightSelected(highlight=True):
    """Turns on or off selection highlight for an object list.  Attribute selectionChildHighlighting

    If True then highlighting is on, if False then children are not highlighted when selected.

    See selectionHighlightList() for more information.

    :param highlight: If True then highlighting is on, if False then children are not highlighted when selected.
    :type highlight: bool
    """
    selObjs = cmds.ls(selection=True)
    if not selObjs:
        output.displayWarning("Nothing selected, please select object/s.")
        return
    selectionHighlightList(selObjs, highlight=highlight)


def unlockUnhideAll():
    """Unlocks and unhides everything selected"""
    cmds.select(hierarchy=True, replace=True)
    nodes = cmds.ls(selection=True, long=True)
    cmds.lockNode(nodes, lock=False)
    for node in nodes:
        try:
            cmds.setAttr('{0}.hiddenInOutliner'.format(node), False)
        except:
            pass
        try:
            cmds.setAttr('{0}.visibility'.format(node), True)
        except:
            pass
    for node in cmds.ls(long=True, type='transform'):
        try:
            cmds.setAttr('{0}.intermediateObject'.format(node), False)
        except:
            pass
        try:
            cmds.setAttr('{0}.visibility'.format(node), True)
        except:
            attributes.breakAttr(('{0}.visibility'.format(node)))
    for node in cmds.ls(long=True, type='joint'):
        try:
            cmds.setAttr('{0}.drawStyle'.format(node), 0)
        except:
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


def GrpAdd(Obj, GrpNames, addgrpRelativeTier):
    """
    添加层级组结构

    :param Obj: 目标对象
    :param GrpNames: 组名称列表
    :param addgrpRelativeTier: 组添加方向 ('Up' 向上层级, 'Dn' 向下层级)
    :return: 新建的组列表
    """
    # 获取对象父级
    obj_parent = cmds.listRelatives(Obj, p=True, f=True)

    # 反转组名称列表以便从内向外创建
    reversed_grp_names = GrpNames[::-1]
    created_groups = []

    # 创建组结构
    for idx, grp_name in enumerate(reversed_grp_names):
        # 检查组是否已存在
        if cmds.objExists(grp_name):
            cmds.warning("{} ------ 已存在".format(grp_name))

        # 创建空组或普通组
        if idx == 0:
            new_group = cmds.group(em=True)
        else:
            new_group = cmds.group()

        created_groups.append(new_group)

    # 调整组顺序并获取顶层和底层组
    created_groups = created_groups[::-1]
    top_group = created_groups[0]
    end_group = created_groups[-1]

    # 设置组的父子关系
    cmds.parent(top_group, Obj)
    resetattrs.resetNodes([top_group])  # 假设resetNodes是已定义的函数

    # 根据方向参数处理层级关系
    if addgrpRelativeTier == 'Up':
        # 向上层级: 将顶层组移至世界空间或原父级下
        cmds.parent(top_group, w=True)
        if obj_parent:
            cmds.parent(top_group, obj_parent[0])
        # 将原始对象移至最底层组
        cmds.parent(Obj, end_group)
    elif addgrpRelativeTier == 'Dn':
        # 向下层级: 可在此添加具体逻辑
        pass

    # 重命名组并调整选择顺序
    created_groups = created_groups
    cmds.select(created_groups, add=True)

    # 应用用户指定的组名称
    for group, name in zip(created_groups, GrpNames):
        cmds.rename(group, name)

    # 返回重命名后的组列表
    return cmds.ls(sl=True)


