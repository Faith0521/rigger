# -*- coding: utf-8 -*-
from maya import cmds as cmds
from maya.api import OpenMaya as om2
from cgrig.libs.maya import zapi
from cgrig.libs.maya.cmds.meta import metajointscurve, metasplinejointscurve
from cgrig.libs.maya.cmds.objutils import filtertypes, namehandling, joints
from cgrig.libs.maya.cmds.rig.splines import objectsAlongSplineDuplicate
from cgrig.libs.maya.cmds.objutils import curves
from cgrig.libs.maya.cmds.rig import axis
from cgrig.libs.maya.meta import base

"""
Joints Along A Spline
"""


def jointsAlongACurve(splineCurve, jointCount=30, jointName="joint", spacingWeight=0.0, spacingStart=0.0,
                      spacingEnd=1.0, secondaryAxisOrient="yup", fractionMode=True, numberPadding=2, suffix=True,
                      buildMetaNode=False, reverseDirection=False, hideCurve=False, message=True):
    """Given a spline curve build joints along the curve, parent and orient them into an FK chain.

    :param splineCurve: The name of the transform node of the curve
    :type splineCurve: str
    :param jointCount: The number of joints to build in the chain
    :type jointCount: int
    :param jointName: The base name of the joints to be created
    :type jointName: str
    :param spacingWeight: The weighting of the spacing, causes more joints to be sqashed to one end or another 0.0 - 1.0
    :type spacingWeight: float
    :param spacingStart: The start of the curve where the joint chain will start usually 0.0 (start)
    :type spacingStart: float
    :param spacingEnd: The end of the curve where the joint chain will start usually 1.0 (end)
    :type spacingEnd: float
    :param secondaryAxisOrient: this axis of the joints orients in what direction?  Default is "yup"
    :type secondaryAxisOrient: str
    :param fractionMode: calculates in real world coords based on the curve, is affected by the spacing on the CVs.
    :type fractionMode: bool
    :param numberPadding: Pad the joint names with numbers and this padding.  ie 2 is 01, 02, 03
    :type numberPadding: int
    :param suffix: Add a joint suffix "jnt" to the end of the joint names ie "joint_01_jnt"
    :type suffix: bool
    :param buildMetaNode: builds the meta node for tracking and altering the joints later
    :type buildMetaNode: bool
    :param reverseDirection: reverses the curve while building, the reverses it back after build
    :type reverseDirection: bool
    :param hideCurve: hides the incoming curve splineCurve
    :type hideCurve: bool
    :param message: return any messages to the user?
    :type message: bool

    :return jointList: A list of joint string names
    :rtype jointList: list(str)
    """
    if secondaryAxisOrient == joints.AUTO_UP_VECTOR_WORDS_LIST[0]:  # is "Auto"
        upAxis = axis.autoAxisBBoxObj(splineCurve, secondaryAxis=True)  # Result will be "+y" or "+z"
        index = joints.AUTO_UP_VECTOR_POSNEG_LIST.index(upAxis)
        secondaryAxisOrient = joints.AUTO_UP_VECTOR_WORDS_LIST[index]  # now fixed to "yup" or "zup"
    if jointCount < 1:
        jointCount = 1
    jointList = list()
    if fractionMode:  # Normalize values
        if spacingStart < 0.0:
            spacingStart = 0.0
        if spacingEnd > 1.0:
            spacingEnd = 1.0
    buildCurve = splineCurve
    if reverseDirection:  # Reverse the direction of the curve
        buildCurve = cmds.reverseCurve(splineCurve, replaceOriginal=False)[0]
    for n in range(jointCount):  # create joints
        cmds.select(deselect=True)
        if suffix:
            n = "_".join([jointName, str(n + 1).zfill(numberPadding), filtertypes.JOINT_SX])
        else:
            n = "_".join([jointName, str(n + 1).zfill(numberPadding)])
        jointList.append(cmds.joint(name=namehandling.nonUniqueNameNumber(n)))
    # Place joints on the curve
    objectsAlongSplineDuplicate(jointList, buildCurve, multiplyObjects=0, deleteMotionPaths=True,
                                spacingWeight=spacingWeight, spacingStart=spacingStart, spacingEnd=spacingEnd,
                                follow=False, group=False, fractionMode=fractionMode, weightPosition=True,
                                weightRotation=False, weightScale=False, autoWorldUpV=False, message=False)
    # Parent the joints to each other
    jntDagList = list(zapi.nodesByNames(jointList))  # objects to api dag objects for names
    for n in range(1, len(jointList)):
        cmds.parent(jointList[n], jointList[n - 1])
    jointList = zapi.fullNames(jntDagList)  # back to long names
    # Orient joints
    if len(jointList) > 1:
        joints.alignJoint(jointList, secondaryAxisOrient=secondaryAxisOrient, children=False, freezeJnt=True,
                          message=False)
        joints.alignJointToParent(jointList[-1])  # orient last joint to parent
    if reverseDirection:  # Delete reverse direction curve
        cmds.delete(buildCurve)
    if buildMetaNode:  # Builds the network meta node on all joints and the curve
        name = namehandling.nonUniqueNameNumber("{}_joints_meta".format(splineCurve))
        metaNode = metajointscurve.CgRigJointsCurve(name=name)
        metaNode.connectAttributes(list(zapi.nodesByNames(jointList)),
                                   zapi.nodeByName(splineCurve))
        metaNode.setMetaAttributes(jointCount, jointName, spacingWeight, spacingStart, spacingEnd, secondaryAxisOrient,
                                   fractionMode, numberPadding, suffix, reverseDirection)
    if hideCurve:
        cmds.hide(splineCurve)
    if message:
        om2.MGlobal.displayInfo("Success: Joints created and oriented along `{}`.".format(splineCurve))
    return jointList


def jointsAlongACurveSelected(jointCount=30, jointName="joint", spacingWeight=0.0, spacingStart=0.0,
                              spacingEnd=1.0, secondaryAxisOrient="yup", fractionMode=True, numberPadding=2,
                              suffix=True, buildMetaNode=True, reverseDirection=False):
    """Given a selected spline curve build joints along the curve, parent and orient them into an FK chain.

    :param jointCount: The number of joints to build in the chain
    :type jointCount: int
    :param jointName: The base name of the joints to be created
    :type jointName: str
    :param spacingWeight: The weighting of the spacing, causes more joints to be sqashed to one end or another 0.0 - 1.0
    :type spacingWeight: float
    :param spacingStart: The start of the curve where the joint chain will start usually 0.0 (start)
    :type spacingStart: float
    :param spacingEnd: The end of the curve where the joint chain will start usually 1.0 (end)
    :type spacingEnd: float
    :param secondaryAxisOrient: this axis of the joints orients in what direction?  Default is "yup"
    :type secondaryAxisOrient: str
    :param fractionMode: calculates in real world coords based on the curve, is affected by the spacing on the CVs.
    :type fractionMode: bool
    :param numberPadding: Pad the joint names with numbers and this padding.  ie 2 is 01, 02, 03
    :type numberPadding: int
    :param suffix: Add a joint suffix "jnt" to the end of the joint names ie "joint_01_jnt"
    :type suffix: bool
    :param buildMetaNode: builds the meta node for tracking and altering the joints later
    :type buildMetaNode: bool
    :param reverseDirection: reverses the curve while building, the reverses it back after build
    :type reverseDirection: bool

    :return jointListList: A list of a list of joint string names
    :rtype jointListList: list(list(str))
    """
    selObjs = cmds.ls(selection=True)
    curveTransforms = filtertypes.filterTypeReturnTransforms(selObjs, children=False, shapeType="nurbsCurve")
    if not curveTransforms:
        om2.MGlobal.displayWarning("Selection incorrect.  Please a curve type object.")
        return
    if len(curveTransforms) > 1:  # multiple curves found build a joint chain on each curve, names are different
        jointListList = list()
        uniqueName = namehandling.nonUniqueNameNumber(jointName)
        for i, curve in enumerate(curveTransforms):
            jointName = "_".join([uniqueName, str(i + 1).zfill(numberPadding)])
            jointList = jointsAlongACurve(curve, jointCount=jointCount, jointName=jointName,
                                          spacingWeight=spacingWeight,
                                          spacingStart=spacingStart, spacingEnd=spacingEnd,
                                          secondaryAxisOrient=secondaryAxisOrient,
                                          fractionMode=fractionMode, numberPadding=numberPadding,
                                          buildMetaNode=buildMetaNode, reverseDirection=reverseDirection)
            jointListList.append(jointList)
        return jointListList
    # Else only one curve found
    jointList = jointsAlongACurve(curveTransforms[0], jointCount=jointCount, jointName=jointName,
                                  spacingWeight=spacingWeight,
                                  spacingStart=spacingStart, spacingEnd=spacingEnd,
                                  secondaryAxisOrient=secondaryAxisOrient,
                                  fractionMode=fractionMode, numberPadding=numberPadding, suffix=suffix,
                                  buildMetaNode=buildMetaNode, reverseDirection=reverseDirection)
    return [jointList]


def jointsSplineAlongACurve(selected=None, jointCount=10, axis="x", secondaryAxisOrient="+y", jointName='control', numberPadding=2, suffix=True,
                            reverseDirection=False, buildMetaNode=True):
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
    joints = filtertypes.filterTypeObjList(['joint', 'transform'], selected)
    matrix_list = [cmds.xform(joint, q=1, ws=1, m=1) for joint in joints]

    selection = filtertypes.filterTypeReturnTransforms([selected[-1].fullPathName()], children=False,
                                                       shapeType="nurbsCurve")

    if selection:
        # 如果选择了曲线，则获取cv点坐
        curve = joints[0]
        if reverseDirection:
            curve = cmds.reverseCurve(curve, replaceOriginal=True)[0]
        points = cmds.xform(joints[0] + ".cv[*]", q=1, ws=1, t=1)
        points = [points[i:i + 3] for i in range(0, len(points), 3)]
    else:
        # 如果选择了骨骼，获取选择骨骼的坐
        points = [cmds.xform(joint, q=1, ws=1, t=1) for joint in joints]
        curve = curves.create_curve_by_joints(points)
        if reverseDirection:
            curve = cmds.reverseCurve(curve, replaceOriginal=True)[0]
        cmds.delete(joints)

    # 按骨骼长度，创建等长骨骼
    length = cmds.arclen(curve, ch=0)
    step = length / (jointCount - 1)
    joint = None
    joints = []
    for i in range(jointCount):
        if suffix:
            name = "_".join([jointName, str(i + 1).zfill(numberPadding), filtertypes.JOINT_SX])
        else:
            name = "_".join([jointName, str(i + 1).zfill(numberPadding)])
        if cmds.objExists(name):
            cmds.delete(name)
        joint = cmds.joint(joint, name=name)

        cmds.setAttr(joint + ".tx", step)
        joints.append(joint)
    cmds.xform(joints[0], ws=1, t=points[0])

    # 创建样条IK
    ik = cmds.ikHandle(sol="ikSplineSolver", ccv=0, sj=joints[0], ee=joints[-1], curve=curve)[0]

    for _ in range(3):
        # 在倒数第二个骨骼出，放止一个临时组，位置设置为points[-1]
        temp = cmds.group(em=1, p=joints[-2])
        cmds.xform(temp, ws=1, t=points[-1])
        # 此时，最后以跟x轴的坐标与临时组x轴坐标的差，越为线段长度与曲线长度的
        err = (cmds.getAttr(joints[-1] + ".tx") - cmds.getAttr(temp + ".tx")) / (jointCount - 1)
        # 缩小tx的值，减少误差，让最后一根骨骼落地在曲线末短
        for joint in joints[1:]:
            cmds.setAttr(joint + ".tx", cmds.getAttr(joint + ".tx") - err)
        cmds.delete(temp)

    # 设置骨骼第二轴朝
    if axis == "y":
        cmds.setAttr(ik + ".dWorldUpAxis", 0)
    elif axis == "z":
        cmds.setAttr(ik + ".dWorldUpAxis", 3)

    up_map = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]

    if isinstance(secondaryAxisOrient, int):
        # 设置up为世界正方向
        up1, up2 = up_map[secondaryAxisOrient], up_map[secondaryAxisOrient]
    else:
        # 设置up为首尾骨骼的y/z轴朝
        axis_index = slice(4, 7) if axis == "y" else slice(8, 11)
        joint_index = -1 if secondaryAxisOrient == u"首尾骨骼" else 0
        up1, up2 = matrix_list[0][axis_index], matrix_list[joint_index][axis_index]

    # 设置ik高级旋转
    cmds.setAttr(ik + ".dTwistControlEnable", True)
    cmds.setAttr(ik + ".dWorldUpType", 4)
    cmds.setAttr(ik + ".dWorldUpAxis", 0 if axis == "y" else 3)
    cmds.setAttr(ik + ".dWorldUpVector", *up1)
    cmds.setAttr(ik + ".dWorldUpVectorEnd", *up2)
    # 获取骨骼矩阵，触发ik计算更新
    cmds.xform(joints[0], q=1, ws=1, m=1)
    cmds.delete(ik)
    # cmds.toggle(joints, la=1)
    cmds.makeIdentity(joints, apply=1, r=1)
    jntDagList = list(zapi.nodesByNames(joints))
    jointList = zapi.fullNames(jntDagList)

    if buildMetaNode:  # Builds the network meta node on all joints and the curve
        name = namehandling.nonUniqueNameNumber("{}_joints_meta".format(curve))
        metaNode = metasplinejointscurve.CgRigSplineJointsCurve(name=name)
        metaNode.connectAttributes(list(zapi.nodesByNames(jointList)),
                                   zapi.nodeByName(curve))
        metaNode.setMetaAttributes(jointCount, jointName, secondaryAxisOrient, numberPadding, suffix, reverseDirection)

    return jointList


def deleteSplineJoints(relatedObjs, message=False):
    """Deletes all joints and the meta node setup related to the selection

    :param relatedObjs: any maya nodes by name, should be joints or curves related to joint setup
    :type relatedObjs: str
    :param message: report the message to the user
    :type message: bool
    """
    metajointscurve.deleteSplineJoints(list(zapi.nodesByNames(relatedObjs)), message=message)


def deleteSplineJointsSelected(message=True):
    """Deletes all joints and the meta node setup related to the selection

    :param message: report the message to the user
    :type message: bool
    """
    selObjs = cmds.ls(selection=True)
    if not selObjs:
        om2.MGlobal.displayWarning("Please select a joint or curve related to the spline joint setup")
        return
    metajointscurve.deleteSplineJoints(list(zapi.nodesByNames(selObjs)), message=message)


def rebuildSplineJointsSelected(jointCount=30, jointName="joint", spacingWeight=0.0, spacingStart=0.0,
                                spacingEnd=1.0, secondaryAxisOrient="yup", fractionMode=True, numberPadding=2,
                                suffix=True, buildMetaNode=True, reverseDirection=False, message=True,
                                renameMode=False):
    """Deletes all joints and the meta node setup related to the selection and then rebuilds it as per the kwargs

    See jointsAlongACurve() for documentation

    :param renameMode: If True will use the incoming name to build the new setup.  If False will use the existing name
    :type renameMode: bool
    """
    lastJointList = list()
    selNodes = zapi.selected()
    if not selNodes:
        if message:
            om2.MGlobal.displayWarning("Please select a joint or curve related to the spline joint setup")
        return
    metaNodes = base.findRelatedMetaNodesByClassType(selNodes, metajointscurve.CgRigJointsCurve.__name__)
    if not metaNodes:
        if message:
            om2.MGlobal.displayWarning("No `{}` related setups found connected to "
                                       "objects".format(metajointscurve.META_TYPE))
        return

    for metaNode in metaNodes:
        curve = metaNode.getCurveStr()
        if not curve:  # no curve so bail
            continue
        jointList = metaNode.getJointsStr()
        if not renameMode:  # get the previous name
            jointName = metaNode.getMetaJointName()
        if jointList:
            metaNode.deleteJoints()
            metaNode.delete()
        jointList = jointsAlongACurve(curve, jointCount=jointCount, jointName=jointName, spacingWeight=spacingWeight,
                                      spacingStart=spacingStart, spacingEnd=spacingEnd,
                                      secondaryAxisOrient=secondaryAxisOrient,
                                      fractionMode=fractionMode, numberPadding=numberPadding, suffix=suffix,
                                      buildMetaNode=buildMetaNode, reverseDirection=reverseDirection, message=message)
        lastJointList.append(jointList[-1])
        if message:
            om2.MGlobal.displayInfo("Success: Joints rebuilt on `{}`".format(curve))
    if len(metaNodes) > 1:  # select all last joints
        cmds.select(lastJointList, add=True)

    return lastJointList


def splineJointsAttrValues(message=True):
    """Returns all the attribute (usually related to the UI) settings from the jointsOnCurve meta node

    Finds related meta node from selected objects either the joints or curves

    :param message: report messages to the user
    :type message: bool
    """
    selNodes = zapi.selected()
    if not selNodes:
        if message:
            om2.MGlobal.displayWarning("Please select a joint or curve related to the spline joint setup")
        return dict()
    metaNodes = base.findRelatedMetaNodesByClassType(selNodes, metajointscurve.CgRigJointsCurve.__name__)
    if not metaNodes:
        if message:
            om2.MGlobal.displayWarning("No `{}` related setups found connected to "
                                       "objects".format(metajointscurve.META_TYPE))
        return dict()
    return metaNodes[-1].getMetaAttributes()
