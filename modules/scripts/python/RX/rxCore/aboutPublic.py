#!/usr/bin/python
# -*- coding: utf-8 -*-
# --------------------------------------------<<<<<This script can solve a series of problems>>>>>--------------------------------------------------#
# Author: rosa.w
# Mail: wrx1844@qq.com
# Computer language: Python.3.2.2
# scriptName : rosa_PublicClass.py
# Note: this is my global class
# add in git 2014/03/06
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import maya.cmds as mc
import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymaya as pm
from rxCore import aboutApi

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GET FUNCTION

def getSpace(obj, spaceType='both'):
    """
    #get one object's worldSpace value.
    #Date:2013/5/13_v01. Have a attribute named 'type', is used for get your desired data type.
    :param obj:
    :param spaceType:
    :return:
    """
    if spaceType == 'both':
        objT = mc.xform(obj, q=1, t=1, ws=1)
        objR = mc.xform(obj, q=1, ro=1, ws=1)
        aboutObjDate = objT + objR
        return aboutObjDate

    elif spaceType == 'tr':
        objT = mc.xform(obj, q=1, t=1, ws=1)
        return objT

    elif spaceType == 'r':
        objR = mc.xform(obj, q=1, ro=1, ws=1)
        return objR


def getObjType(objCheck):
    """
    #kMesh
    #kNurbsCurve
    #kNurbsSurface
    :param objCheck:
    :return:
    """

    # noinspection PyBroadException
    try:
        childobj = mc.listRelatives(objCheck, c=True)[0]
        typelist = mc.nodeType(childobj, api=True)
        return typelist
    except:
        mc.error('Node Error')


def getChannelBox():
    # channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    channelBox = 'mainChannelBox'
    attrs = mc.channelBox(channelBox, q=True, sma=True)
    attrs2 = mc.channelBox(channelBox, q=True, sha=True)
    if not attrs:
        attrs = []
    if not attrs2:
        attrs2 = []
    return attrs + attrs2


def getClosestParameterOnMesh(modelShape, obj):
    closest_Point = []
    modelShapeType = getObjType(modelShape)

    temp = mc.createNode('transform', name=obj + '_point_temp')
    mc.parentConstraint(obj, temp, mo=False)

    # model type data
    if modelShapeType == 'kNurbsSurface':
        closest_Point = ['closestPointOnSurface', temp + '_cpos', 'local', 'inputSurface']
    elif modelShapeType == 'kMesh':
        closest_Point = ['closestPointOnMesh', temp + '_cpom', 'outMesh', 'inMesh']

    # create getUV Node
    closest_PointNode = mc.createNode(closest_Point[0], name=closest_Point[1])
    mc.connectAttr(temp + '.translate', closest_PointNode + '.inPosition')
    mc.connectAttr(modelShape + '.' + closest_Point[2], closest_PointNode + '.' + closest_Point[3])

    # get UV
    U = mc.getAttr(closest_PointNode + '.result.parameterU')
    V = mc.getAttr(closest_PointNode + '.result.parameterV')
    mc.delete(closest_PointNode, temp)

    return {'u': U, 'v': V}


def getAxisTwistValue(orgObj, aimObj, axis='y'):
    axis = axis.upper()
    needPlugin = ['matrixNodes.mll', 'quatNodes.mll']
    for plugin in needPlugin:
        if not mc.pluginInfo(plugin, query=True, loaded=True):
            mc.loadPlugin(plugin)

    # create node 
    multMatrixNode = mc.createNode('multMatrix', n='{0}_{1}_multMatrix_node'.format(orgObj, aimObj))
    decomposeMatrixNode = mc.createNode('decomposeMatrix', n='{0}_{1}_decomposeMatrix_node'.format(orgObj, aimObj))
    quatToEulerNode = mc.createNode('quatToEuler', n='{0}_{1}_quatToEuler_node'.format(orgObj, aimObj))

    # connect node ....
    mc.connectAttr(orgObj + '.worldMatrix[0]', multMatrixNode + '.matrixIn[0]')
    mc.connectAttr(aimObj + '.worldMatrix[0]', multMatrixNode + '.matrixIn[1]')
    mc.connectAttr(multMatrixNode + '.matrixSum', decomposeMatrixNode + '.inputMatrix')
    # outputQuatY
    mc.connectAttr(decomposeMatrixNode + '.outputQuat' + axis, quatToEulerNode + '.inputQuat' + axis)
    mc.connectAttr(decomposeMatrixNode + '.outputQuatW', quatToEulerNode + '.inputQuatW')
    value = mc.getAttr(quatToEulerNode + '.outputRotate' + axis)

    # cleaner
    needDelete = [multMatrixNode, decomposeMatrixNode, quatToEulerNode]
    mc.delete(needDelete)

    return value


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CREATE FUNCTION

def addNewAttr(objects=None, attrName=None, lock=False, **kwargs):
    """
    # Add different attributes to the objects in the scene.
    #if you attrType is not bool ,you must give editAttr some values!

    #Date : 2013/5/16_v01
    #     : 2020/4/12_v02 objects=[] / attrName=[]
    :param objects:
    :param attrName:
    :param lock:
    :param kwargs:
    :return:
    """

    # for each obj
    if attrName is None:
        attrName = []
    if objects is None:
        objects = []
    for obj in objects:
        #for each attr
        for x in range(0, len(attrName)):
            #If the attribute does not exists
            if not mc.attributeQuery(attrName[x], node=obj, exists=True):
                #Add the attribute
                mc.addAttr(obj, longName=attrName[x], **kwargs)
                #If lock was set to True
                mc.setAttr((obj + '.' + attrName[x]), lock=1) if lock else mc.setAttr((obj + '.' + attrName[x]), lock=0)


def createParentGrp(obj, grpName, nodeType='group', worldOrient=False):
    """
    #This Function can make object zero
    #Note: if you want create control type is joint or you wang create sdk group on objects , you can use this script.
    #FN: makeObjZero(sel,type,rotation)

    #Date:      2012/07/13_v1.0       Just support one type('joint')
    #           2012/07/20_v1.1       Add new type(transform) / user can modify orient.
    #           2012/12/24_v1.2       Add new flag '*obj', Now it can return group name.
    #           2020/03/30_v1.3       Rewrite
    :param obj:
    :param grpName:
    :param nodeType:
    :param worldOrient:
    :return:
    """
    if not obj:
        obj = mc.ls(sl=1)[0]

    if not mc.objExists(obj):
        return
    #---------------------------------------------------------------------------

    parent = mc.listRelatives(obj, p=True)
    if parent:
        parent = parent[0]

    parentGrp = ''
    #---------------------------------------------------------------------------
    if nodeType == 'joint':
        parentGrp = mc.duplicate(obj, n='%s_%s' % (obj, grpName), po=1)[0]
        mc.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)
        mc.setAttr(parentGrp + '.rx', 0)
        mc.setAttr(parentGrp + '.ry', 0)
        mc.setAttr(parentGrp + '.rz', 0)

    elif nodeType == 'group':
        parentGrp = mc.createNode('transform', name='%s_%s' % (obj, grpName))
    #---------------------------------------------------------------------------

    if worldOrient:
        mc.delete(mc.pointConstraint(obj, parentGrp, mo=False))
    elif not worldOrient:
        mc.delete(mc.parentConstraint(obj, parentGrp, mo=False))

    #---------------------------------------------------------------------------

    if parent is None:
        mc.parent(obj, parentGrp)
    else:
        orgParent = mc.listRelatives(parentGrp, p=True)

        if orgParent:
            if orgParent[0] != parent:
                mc.parent(parentGrp, parent)
        else:
            mc.parent(parentGrp, parent)

        mc.parent(obj, parentGrp)

    return parentGrp


def fastGrp(obj, grpNameList, worldOrient=False):
    """
    #This Function can quickly create three group with one object, the three group named  'sdk','pos','zero'.
    #Note: pass
    #FN: fastGrp(obj)
    #Date: 2012/09/28_v1.0
    #      2013/01/05_v1.1
    #      2020/03/30_v1.2
    :param obj:
    :param grpNameList:
    :param worldOrient:
    :return:
    """
    zeroGrp = []

    for i in range(len(grpNameList)):
        grp = createParentGrp(obj, grpNameList[i], nodeType='group', worldOrient=worldOrient)
        zeroGrp.append(grp)

    return zeroGrp


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def snapAtoB(a, b, snapType='both'):
    """
    #This Function can from A to B.
    #Note: none
    #FN: snapAtoB():
    #Date: 2020/04/22 v1.0
    :param a:
    :param b: 
    :param snapType:
    :return:
    """
    if snapType == 't':
        mc.delete(mc.pointConstraint(b, a, mo=False))

    elif snapType == 'r':
        mc.delete(mc.orientConstraint(b, a, mo=False))

    elif snapType == 'both':
        mc.delete(mc.parentConstraint(b, a, mo=False))


def snapLoc(node=None, name=None):
    # create a locator snap to assign object.

    if node:
        sel = mc.ls(node)
    else:
        sel = mc.ls(sl=1)

    # get bounding box
    nodeType = mc.nodeType(sel[0])
    if nodeType == 'joint':
        bb = mc.xform(sel, q=1, bb=1, ws=1)
    else:
        bb = mc.exactWorldBoundingBox(sel, ii=1)

    # set object pos
    x = (bb[3] + bb[0]) / 2
    y = (bb[4] + bb[1]) / 2
    z = (bb[5] + bb[2]) / 2

    mc.spaceLocator(p=(0, 0, 0))
    mc.xform(ws=1, t=[x, y, z])
    loc = mc.ls(sl=1)[0]

    if nodeType == 'joint':
        mc.delete(mc.pointConstraint(sel, loc))
    # rename
    if name:
        loc = mc.rename(loc, name)
    return loc


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CHECK FUNCTION

def checkSymObj(orgObj=None, searchFor='L_', replaceWith='R_'):
    # --------------------------------------------------------
    # Check the symmetry of objects and attributes.
    # --------------------------------------------------------

    # ------------------------------
    if orgObj is None:
        orgObj = []
    symObj = []
    keyword = [searchFor]
    # ------------------------------
    if not orgObj:
        selobjs = mc.ls(sl=1)
    else:
        selobjs = orgObj

    for x in selobjs:
        for n in keyword:
            if n not in x:
                symObj.append(x)
            else:
                theOtherSideobj = x.replace(searchFor, replaceWith)
                if mc.objExists(theOtherSideobj):
                    symObj.append(theOtherSideobj)
                else:
                    mc.warning('can not find the sysmmetry : %s' % theOtherSideobj)

        symObj = sorted(set(symObj), key=symObj.index)

    if len(symObj) == 1:
        return symObj[0]
    else:
        return symObj


def checkSymAxis(orgobj, symobj):
    # ------------------------------------------------------------
    # Check the symmetry axis of objects and attributes.
    # ------------------------------------------------------------

    symAxis = []

    orghelploc = mc.spaceLocator(p=(0, 0, 0), name=str(orgobj) + '_help_loc')[0]
    symhelploc = mc.spaceLocator(p=(0, 0, 0), name=str(symobj) + '_help_loc')[0]

    orghelplocGrp = createParentGrp(orghelploc, 'zero', nodeType='group', worldOrient=False)
    symhelplocGrp = createParentGrp(symhelploc, 'zero', nodeType='group', worldOrient=False)

    # update date 2017/03/16 >>
    # set zero value in object space
    mc.parent(orghelplocGrp, orgobj)
    mc.parent(symhelplocGrp, symobj)

    defaultAttr = ['.tx', '.ty', '.tz', '.rx',
                   '.ry', '.rz', '.sx', '.sy', '.sz']
    for attr in defaultAttr:
        if 's' in attr:
            mc.setAttr(orghelplocGrp + attr, 1)
            mc.setAttr(symhelplocGrp + attr, 1)
        else:
            mc.setAttr(orghelplocGrp + attr, 0)
            mc.setAttr(symhelplocGrp + attr, 0)

    # set zero value in world space
    mc.parent(orghelplocGrp, w=1)
    mc.parent(symhelplocGrp, w=1)

    zeroValue = ['.tx', '.ty', '.tz']
    for x in zeroValue:
        mc.setAttr(orghelplocGrp + x, 0)
        mc.setAttr(symhelplocGrp + x, 0)

    orgaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    axisKey = ['X', 'Y', 'Z', 'X-', 'Y-', 'Z-']
    symaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                    (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

    i = 0
    while i < len(orgaxisValue):
        j = 0

        mc.setAttr(orghelploc + '.tx', orgaxisValue[i][0])
        mc.setAttr(orghelploc + '.ty', orgaxisValue[i][1])
        mc.setAttr(orghelploc + '.tz', orgaxisValue[i][2])

        orgcurrentPos = mc.xform(orghelploc, q=1, t=1, ws=1)

        orgcurrentPos[0] = round(orgcurrentPos[0], 1)
        orgcurrentPos[1] = round(orgcurrentPos[1], 1)
        orgcurrentPos[2] = round(orgcurrentPos[2], 1)

        mc.setAttr(orghelploc + '.tx', 0)
        mc.setAttr(orghelploc + '.ty', 0)
        mc.setAttr(orghelploc + '.tz', 0)

        while j < len(symaxisValue):

            mc.setAttr(symhelploc + '.tx', symaxisValue[j][0])
            mc.setAttr(symhelploc + '.ty', symaxisValue[j][1])
            mc.setAttr(symhelploc + '.tz', symaxisValue[j][2])

            symcurrentPos = mc.xform(symhelploc, q=1, t=1, ws=1)

            symcurrentPos[0] = round(symcurrentPos[0], 1)
            symcurrentPos[1] = round(symcurrentPos[1], 1)
            symcurrentPos[2] = round(symcurrentPos[2], 1)

            mc.setAttr(symhelploc + '.tx', 0)
            mc.setAttr(symhelploc + '.ty', 0)
            mc.setAttr(symhelploc + '.tz', 0)

            if symcurrentPos[0] * -1 == orgcurrentPos[0] and symcurrentPos[1] == orgcurrentPos[1] and symcurrentPos[
                2] == orgcurrentPos[2]:

                symAxis.append(orgobj + '.translate' + axisKey[i])
                symAxis.append(symobj + '.translate' + axisKey[j])

                # check rotate
                # create rotate help locator
                orgRollLoc = mc.spaceLocator(
                    p=(0, 0, 0), name=str(orgobj) + '_roll_loc')[0]
                symRollLoc = mc.spaceLocator(
                    p=(0, 0, 0), name=str(symobj) + '_roll_loc')[0]

                # sym help loc
                mc.setAttr(orgRollLoc + '.tx', 1)
                mc.setAttr(symRollLoc + '.tx', -1)
                mc.setAttr(orgRollLoc + '.ty', 1)
                mc.setAttr(symRollLoc + '.ty', 1)

                mc.parentConstraint(orghelploc, orgRollLoc, mo=True)
                mc.parentConstraint(symhelploc, symRollLoc, mo=True)

                # give help loc rotate
                mc.setAttr(orghelploc + '.rotate' + axisKey[i], 10)

                # check rotate at two type
                if '-' in axisKey[j]:
                    mc.setAttr(symhelploc + '.rotate' +
                               axisKey[j][:-1], -10)
                    orgRollLocPos = mc.xform(orgRollLoc, q=1, t=1, ws=1)
                    symRollLocPos = mc.xform(symRollLoc, q=1, t=1, ws=1)

                    orgRollLocPos[0] = round(orgRollLocPos[0], 1)
                    orgRollLocPos[1] = round(orgRollLocPos[1], 1)
                    orgRollLocPos[2] = round(orgRollLocPos[2], 1)

                    symRollLocPos[0] = round(symRollLocPos[0], 1)
                    symRollLocPos[1] = round(symRollLocPos[1], 1)
                    symRollLocPos[2] = round(symRollLocPos[2], 1)

                    if symRollLocPos[0] * -1 == orgRollLocPos[0] and symRollLocPos[1] == orgRollLocPos[1] and \
                            symRollLocPos[2] == orgRollLocPos[2]:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(symobj + '.rotate' + axisKey[j])
                    else:
                        # print 'test'
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(
                            symobj + '.rotate' + axisKey[j][:-1])

                elif '-' not in axisKey[j]:
                    mc.setAttr(symhelploc + '.rotate' + axisKey[j], 10)
                    orgRollLocPos = mc.xform(orgRollLoc, q=1, t=1, ws=1)
                    symRollLocPos = mc.xform(symRollLoc, q=1, t=1, ws=1)

                    orgRollLocPos[0] = round(orgRollLocPos[0], 1)
                    orgRollLocPos[1] = round(orgRollLocPos[1], 1)
                    orgRollLocPos[2] = round(orgRollLocPos[2], 1)

                    symRollLocPos[0] = round(symRollLocPos[0], 1)
                    symRollLocPos[1] = round(symRollLocPos[1], 1)
                    symRollLocPos[2] = round(symRollLocPos[2], 1)

                    if symRollLocPos[0] * -1 == orgRollLocPos[0] and symRollLocPos[1] == orgRollLocPos[1] and \
                            symRollLocPos[2] == orgRollLocPos[2]:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(symobj + '.rotate' + axisKey[j])
                    else:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(
                            symobj + '.rotate' + axisKey[j] + '-')

                # clean
                mc.delete(orgRollLoc)
                mc.delete(symRollLoc)
            j += 1
        i += 1

    mc.delete(orghelplocGrp, symhelplocGrp)
    axisNote = {}
    for i in range(0, len(symAxis), 2):
        axisNote[symAxis[i]] = symAxis[i + 1]
    return axisNote


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ATTENUATION FUNCTION

def attenuationConstraint(constraintType, objectA, objectB, aimObjs, correctAxis=True):
    # a and b constraint c that in aimObjs at the same time.
    # if correctAxis is none, use default loc to constraint
    num = 0
    aw = 1.0
    bw = 0.0
    objNum = len(aimObjs)
    incriment = 0

    if objNum == 0:
        mc.error('Has no aim object')
    else:
        incriment = 1.0 / (objNum - 1)

    while num < objNum:

        if correctAxis:
            if mc.objExists(aimObjs[num] + '_' + objectA + '_loc'):
                alocator = aimObjs[num] + '_' + objectA + '_loc'
            else:
                alocator = mc.spaceLocator(p=(0, 0, 0), name=aimObjs[num] + '_' + objectA + '_loc')[0]
                mc.delete(mc.pointConstraint(aimObjs[num], alocator))
                mc.delete(mc.pointConstraint(objectA, alocator))
                mc.parent(alocator, objectA)
                mc.setAttr(alocator + '.visibility', 0)

            if mc.objExists(aimObjs[num] + '_' + objectB + '_loc'):
                blocator = aimObjs[num] + '_' + objectB + '_loc'
            else:
                blocator = mc.spaceLocator(p=(0, 0, 0), name=aimObjs[num] + '_' + objectB + '_loc')[0]
                mc.delete(mc.orientConstraint(aimObjs[num], blocator))
                mc.delete(mc.pointConstraint(objectB, blocator))
                mc.parent(blocator, objectB)
                mc.setAttr(blocator + '.visibility', 0)

            if constraintType == 'parent':
                constraintNode = mc.parentConstraint(alocator, aimObjs[num], weight=aw, mo=True)
                mc.parentConstraint(blocator, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' % (constraintNode[0]), 2)
            elif constraintType == 'rotate':
                constraintNode = mc.orientConstraint(alocator, aimObjs[num], weight=aw, mo=True)
                mc.orientConstraint(blocator, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' % (constraintNode[0]), 2)
            elif constraintType == 'scale':
                mc.scaleConstraint(alocator, aimObjs[num], weight=aw, mo=True)
                mc.scaleConstraint(blocator, aimObjs[num], weight=bw, mo=True)

        elif not correctAxis:
            if constraintType == 'parent':
                constraintNode = mc.parentConstraint(objectA, aimObjs[num], weight=aw, mo=True)
                mc.parentConstraint(objectB, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' % (constraintNode[0]), 2)
            elif constraintType == 'rotate':
                constraintNode = mc.orientConstraint(objectA, aimObjs[num], weight=aw, mo=True)
                mc.orientConstraint(objectB, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' % (constraintNode[0]), 2)
            elif constraintType == 'scale':
                mc.scaleConstraint(objectA, aimObjs[num], weight=aw, mo=True)
                mc.scaleConstraint(objectB, aimObjs[num], weight=bw, mo=True)

        aw = aw - incriment
        bw = bw + incriment
        num += 1


def attenuationRotate(attrA, attrB, aimObjs, rollAixs):
    num = 0
    aw = 1.0
    bw = 0.0
    objNum = len(aimObjs)
    incriment = 0

    if objNum == 0:
        mc.error('Has no aim object')
    else:
        incriment = 1.0 / (objNum - 1)

    while num < objNum:

        parentRoll = mc.listRelatives(aimObjs[num], p=True)

        # create bridge group.
        if parentRoll is None:
            rollGrp = fastGrp('On', ['%s_roll' % (attrA.split('.')[0]), '%s_roll' % (attrB.split('.')[0])],
                              aimObjs[num])
        else:
            if 'roll' in parentRoll[0]:
                rollGrp = ['%s_%s_roll' % (aimObjs[num], attrA.split('.')[0]),
                           '%s_%s_roll' % (aimObjs[num], attrB.split('.')[0])]
            else:
                rollGrp = fastGrp('On', ['%s_roll' % (attrA.split('.')[0]), '%s_roll' % (attrB.split('.')[0])],
                                  aimObjs[num])

        # connect with bridge group.
        if aw == 1:
            if mc.listConnections(rollGrp[0] + '.' + rollAixs) is not None:
                pass
            else:
                mc.connectAttr(attrA, rollGrp[0] + '.' + rollAixs)

        elif bw == 1:
            if mc.listConnections(rollGrp[0] + '.' + rollAixs) is not None:
                pass
            else:
                mc.connectAttr(attrB, rollGrp[0] + '.' + rollAixs)

        else:
            multiplyDrivideNode = mc.createNode(
                'multiplyDivide', name='%s_%s_md_node' % (aimObjs[num], rollAixs))

            mc.connectAttr(attrA, multiplyDrivideNode + '.input1X')
            mc.setAttr(multiplyDrivideNode + '.input2X', aw)
            mc.connectAttr(multiplyDrivideNode +
                           '.output.outputX', rollGrp[0] + '.' + rollAixs)

            mc.connectAttr(attrB, multiplyDrivideNode + '.input1Y')
            mc.setAttr(multiplyDrivideNode + '.input2Y', bw)
            mc.connectAttr(multiplyDrivideNode +
                           '.output.outputY', rollGrp[1] + '.' + rollAixs)

        aw = aw - incriment
        bw = bw + incriment

        num += 1


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# BATCH FUNCTION

def batchModify(outputs, inputs, modifyType='connection', outputAttr='', inputAttr=''):
    outputsNum = len(outputs)
    inputsNum = len(inputs)

    if outputsNum != 0 and inputsNum != 0:

        if outputsNum == 1 and outputsNum != inputsNum:

            for i in range(inputsNum):
                if modifyType == 'connection':
                    mc.connectAttr(outputs[0] + '.' + outputAttr, inputs[i] + '.' + inputAttr)
                if modifyType == 'pointConstraint':
                    mc.pointConstraint(outputs[0], inputs[i], mo=True)
                if modifyType == 'orientConstraint':
                    mc.orientConstraint(outputs[0], inputs[i], mo=True)
                if modifyType == 'parentConstraint':
                    mc.parentConstraint(outputs[0], inputs[i], mo=True)
                if modifyType == 'aimConstraint':
                    mc.aimConstraint(outputs[0], inputs[i], mo=True)

        if outputsNum == inputsNum:
            for i in range(inputsNum):
                if modifyType == 'connection':
                    mc.connectAttr(outputs[i] + '.' + outputAttr, inputs[i] + '.' + inputAttr)
                if modifyType == 'pointConstraint':
                    mc.pointConstraint(outputs[i], inputs[i], mo=True)
                if modifyType == 'orientConstraint':
                    mc.orientConstraint(outputs[i], inputs[i], mo=True)
                if modifyType == 'parentConstraint':
                    mc.parentConstraint(outputs[i], inputs[i], mo=True)
                if modifyType == 'aimConstraint':
                    mc.aimConstraint(outputs[i], inputs[i], mo=True)
                if modifyType == 'parent':
                    mc.parent(outputs[i], inputs[i])

    else:
        mc.error('outputs or inputs is null !')


# Options: 'normal' 'template' 'reference' 'off'
def displaySet(nodes=None, display='reference', shape=False):
    if nodes is None:
        nodes = mc.ls(sl=1, l=1)

    for n in nodes:

        cn = mc.listConnections(n + '.overrideEnabled')
        cnb = mc.listConnections(n + '.overrideDisplayType')
        if cn is None and cnb is None:
            mc.setAttr(n + '.overrideEnabled', l=0)
            mc.setAttr(n + '.overrideDisplayType', l=0)

            if display == 'off':
                mc.setAttr(n + '.overrideEnabled', 0)
            else:
                mc.setAttr(n + '.overrideEnabled', 1)

            if display == 'off' or display == 'normal':
                mc.setAttr(n + '.overrideDisplayType', 0)
            elif display == 'template':
                mc.setAttr(n + '.overrideDisplayType', 1)
            elif display == 'reference':
                mc.setAttr(n + '.overrideDisplayType', 2)

            if shape:
                shapenode = mc.listRelatives(n, s=1, f=1)
                if shapenode is not None:
                    for sh in shapenode:
                        scn = mc.listConnections(sh + '.overrideEnabled')
                        scnb = mc.listConnections(sh + '.overrideDisplayType')

                        if scn is None and scnb is None:
                            mc.setAttr(sh + '.overrideEnabled', l=0)
                            mc.setAttr(sh + '.overrideEnabled', 0)

                            mc.setAttr(sh + '.overrideDisplayType', l=0)
                            mc.setAttr(sh + '.overrideDisplayType', 0)


def getDistance2(obj0: pm.node, obj1: pm.node):
    """Get the distance between 2 objects.

    Arguments:
        obj0 (dagNode): Object A
        obj1 (dagNode): Object B

    Returns:
        float: Distance length

    """
    v0 = obj0.getTranslation(space="world")
    v1 = obj1.getTranslation(space="world")

    v = v1 - v0

    return v.length()


def get_joint_chain_details(start_joint=None):
    """
    获取骨骼链的详细信息

    返回:
        包含每个骨骼详细信息的列表，每个元素为字典格式：
        {
            'name': 骨骼名称,
            'parent': 父骨骼,
            'children': 子骨骼列表,
            'position': 世界坐标位置,
            'rotation': 旋转值,
            'jointOrient': 关节方向
        }
    """
    if start_joint is None:
        return []

    # 向上查找根关节
    root = start_joint

    details = []

    def collect_details(joint):
        parent = cmds.listRelatives(joint, parent=True, type='transform')
        children = cmds.listRelatives(joint, children=True, type='transform') or []

        details.append({
            'name': joint,
            'parent': parent[0] if parent else None,
            'children': children
        })

        for child in children:
            collect_details(child)

    collect_details(root)
    return details


def matrixConstraint(drivers,
                     driven,
                     maintainOffset=True,
                     prefix="",
                     skipRotate=None,
                     skipTranslate=None,
                     skipScale=None,
                     source_parent_cutoff=None,
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
        average_node = average_matrix(driver_matrix_plugs,
                                      return_plug=False)
        out_plug = "{}.matrixSum".format(average_node)
    else:
        out_plug = "{}.worldMatrix[0]".format(drivers)
        average_node = None

    if maintainOffset:
        driven_world_matrix = aboutApi.toMDagPath(driven).inclusiveMatrix()
        if is_multi:
            driver_world_matrix = om.MMatrix(cmds.getAttr(out_plug))
        else:
            driver_world_matrix = aboutApi.toMDagPath(drivers).inclusiveMatrix()
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
    cmds.setAttr(f"{mult_matrix_node}.matrixIn[0]", matrix1, type="matrix")
    cmds.setAttr(f"{mult_matrix_node}.matrixIn[1]", matrix2, type="matrix")

    # 获取相乘结果
    result_matrix = cmds.getAttr(f"{mult_matrix_node}.matrixSum")
    cmds.delete(mult_matrix_node)
    return result_matrix


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


def create_nested_groups_with_hierarchy(objects, suffixes, rotateOrder=0):
    """
    为所选物体按后缀列表打组，继承原始层级关系
    :param objects: 物体列表
    :param suffixes: 后缀列表（如 ["_grp", "_ctrl"]）
    """
    if not suffixes:
        raise RuntimeError(u"后缀列表不能为空")
    goupList = []
    for obj in objects:
        # 获取物体的短名称（不含父级路径）
        short_name = obj.split("|")[-1]

        # 获取当前父级（保留原始层级）
        original_parent = cmds.listRelatives(obj, parent=True, fullPath=True)
        original_parent = original_parent[0] if original_parent else None

        # 获取物体的世界变换
        pos = cmds.xform(obj, q=True, translation=True, worldSpace=True)
        rot = cmds.xform(obj, q=True, rotation=True, worldSpace=True)
        scale = cmds.xform(obj, q=True, scale=True, worldSpace=True)

        current_parent = obj  # 初始父级为物体本身

        sufficGrps = {'object': obj}
        # 从内到外逐层打组
        for suffix in reversed(suffixes):
            group_name = f"{short_name}_{suffix}"
            group = cmds.group(empty=True, name=group_name)
            cmds.setAttr(f"{group}.ro", rotateOrder)
            # 匹配原始变换
            cmds.xform(group, translation=pos, rotation=rot, scale=scale, worldSpace=True)

            # 将当前父级物体放入新组
            cmds.parent(current_parent, group)
            current_parent = group  # 更新父级
            sufficGrps[suffix] = group

        goupList.append(sufficGrps)

        # 将最外层的组重新链接到原始父级
        if original_parent:
            cmds.parent(current_parent, original_parent)

    return goupList


def getParamFromCurveAPI(obj, curve):
    sel_list = om.MSelectionList()

    # 将物体和曲线添加到选择列表
    sel_list.add(obj)
    sel_list.add(curve)

    # 获取物体的Dag路径和世界位置
    obj_dag = sel_list.getDagPath(0)
    obj_pos = om.MPoint(om.MFnTransform(obj_dag).translation(om.MSpace.kWorld))

    # 获取曲线的Dag路径
    curve_dag = sel_list.getDagPath(1)
    # 创建NURBS曲线函数集
    curve_fn = om.MFnNurbsCurve(curve_dag)
    max_param = curve_fn.findParamFromLength(curve_fn.length())
    clostPt, _ = curve_fn.closestPoint(obj_pos, tolerance=0.01, space=om.MSpace.kWorld)

    param = curve_fn.getParamAtPoint(
        clostPt,
        0.01,
        om.MSpace.kObject
    )
    return param


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
    for jnt in selected_joints:
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


def createHalfConstraint(node, parent1, parent2, type="orient", skipTranslate=[], skipRotate=[]):
    follow1 = cmds.createNode("transform", name=f"{node}_follow1", p=node)
    follow2 = cmds.createNode("transform", name=f"{node}_follow2", p=node)
    cmds.parent(follow1, parent1)
    cmds.parent(follow2, parent2)
    constraint = None
    if type == "orient":
        constraint = cmds.orientConstraint(follow1, follow2, node, mo=True)[0]
    elif type == "parent":
        constraint = cmds.parentConstraint(follow1, follow2, node, sr=skipRotate, st=skipTranslate, mo=True)[0]
    cmds.setAttr(constraint + ".interpType", 2)
    return follow1, follow2