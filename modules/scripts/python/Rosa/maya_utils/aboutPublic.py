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
    multMatrixNode = mc.createNode( 'multMatrix', n='{0}_{1}_multMatrix_node'.format(orgObj, aimObj) )
    decomposeMatrixNode = mc.createNode( 'decomposeMatrix', n='{0}_{1}_decomposeMatrix_node'.format(orgObj, aimObj) )
    quatToEulerNode = mc.createNode( 'quatToEuler', n='{0}_{1}_quatToEuler_node'.format(orgObj, aimObj) )

    # connect node ....
    mc.connectAttr(orgObj+'.worldMatrix[0]', multMatrixNode+'.matrixIn[0]')
    mc.connectAttr(aimObj+'.worldMatrix[0]', multMatrixNode+'.matrixIn[1]')
    mc.connectAttr(multMatrixNode+'.matrixSum', decomposeMatrixNode+'.inputMatrix')
    # outputQuatY
    mc.connectAttr(decomposeMatrixNode+'.outputQuat'+axis, quatToEulerNode+'.inputQuat'+axis)
    mc.connectAttr(decomposeMatrixNode+'.outputQuatW', quatToEulerNode+'.inputQuatW')
    value = mc.getAttr(quatToEulerNode+'.outputRotate'+axis)

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

    objP = mc.listRelatives(obj, p=True)
    if objP:
        objP = objP[0]

    objGrp = ''
    #---------------------------------------------------------------------------
    if nodeType == 'joint':
        objGrp = mc.duplicate(obj ,n='%s_%s'%(obj, grpName), po=1)[0]
        mc.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0)
        mc.setAttr(objGrp+'.rx',0)
        mc.setAttr(objGrp+'.ry',0)
        mc.setAttr(objGrp+'.rz',0)

    elif nodeType == 'group':
        objGrp = mc.createNode('transform', name='%s_%s' %(obj, grpName))
    #---------------------------------------------------------------------------

    if worldOrient:
        point = mc.xform(obj, q=1, t=1, ws=1)
        mc.xform(objGrp, ws=1, t=point)
        scale = mc.xform(obj, q=1, s=1, ws=1)
        mc.xform(objGrp, ws=1, s=scale)

    elif not worldOrient:
        point = mc.xform(obj, q=1, t=1, ws=1)
        mc.xform(objGrp, ws=1, t=point)
        rotate = mc.xform(obj, q=1, ro=1, ws=1)
        mc.xform(objGrp, ws=1, ro=rotate)
        scale = mc.xform(obj, q=1, s=1, ws=1)
        mc.xform(objGrp, ws=1, s=scale)

    #---------------------------------------------------------------------------
    if objP is None:
        mc.parent(obj, objGrp)
    else:
        mc.parent(objGrp, objP)
        mc.parent(obj, objGrp)
    return objGrp


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
    elif snapType == 's':
        mc.delete(mc.scaleConstraint(b, a, mo=False))
    elif snapType == 'both':
        mc.delete(mc.parentConstraint(b, a, mo=False))
        mc.delete(mc.scaleConstraint(b, a, mo=False))

def snapLoc(node=None, name=None):
    # create a locator snap to assign object.

    if node:
        sel=mc.ls(node)
    else:
        sel=mc.ls(sl=1)

    # get bounding box
    nodeType=mc.nodeType(sel[0])
    if nodeType=='joint':
        bb= mc.xform(sel, q=1, bb=1, ws=1)
    else:
        bb=mc.exactWorldBoundingBox(sel, ii=1)

    # set object pos
    x=(bb[3]+bb[0])/2
    y=(bb[4]+bb[1])/2
    z=(bb[5]+bb[2])/2

    mc.spaceLocator(p=(0,0,0))
    mc.xform(ws=1, t=[x, y, z])
    loc=mc.ls(sl=1)[0]

    if nodeType=='joint':
        mc.delete( mc.pointConstraint(sel ,loc) )
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

    orgaxisValue = [(1, 0, 0),(0, 1, 0),(0, 0, 1)]
    axisKey = ['X', 'Y', 'Z', 'X-', 'Y-', 'Z-']
    symaxisValue = [(1, 0, 0),(0, 1, 0),(0, 0, 1),
                   (-1, 0, 0),(0, -1, 0),(0, 0, -1)]

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
        incriment = 1.0 /(objNum - 1)

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
                mc.setAttr('%s.interpType' %(constraintNode[0]), 2)
            elif constraintType == 'rotate':
                constraintNode = mc.orientConstraint(alocator, aimObjs[num], weight=aw, mo=True)
                mc.orientConstraint(blocator, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' %(constraintNode[0]), 2)
            elif constraintType == 'scale':
                mc.scaleConstraint(alocator, aimObjs[num], weight=aw, mo=True)
                mc.scaleConstraint(blocator, aimObjs[num], weight=bw, mo=True)

        elif not correctAxis:
            if constraintType == 'parent':
                constraintNode = mc.parentConstraint(objectA, aimObjs[num], weight=aw, mo=True)
                mc.parentConstraint(objectB, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' %(constraintNode[0]), 2)
            elif constraintType == 'rotate':
                constraintNode = mc.orientConstraint(objectA, aimObjs[num], weight=aw, mo=True)
                mc.orientConstraint(objectB, aimObjs[num], weight=bw, mo=True)
                mc.setAttr('%s.interpType' %(constraintNode[0]), 2)
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
        incriment = 1.0 /(objNum - 1)

    while num < objNum:

        parentRoll = mc.listRelatives(aimObjs[num], p=True)

        # create bridge group.
        if parentRoll is None:
            rollGrp = fastGrp('On', ['%s_roll' %(attrA.split('.')[0]), '%s_roll' %(attrB.split('.')[0])],
                                   aimObjs[num])
        else:
            if 'roll' in parentRoll[0]:
                rollGrp = ['%s_%s_roll' %(aimObjs[num], attrA.split('.')[0]),
                           '%s_%s_roll' %(aimObjs[num], attrB.split('.')[0])]
            else:
                rollGrp = fastGrp('On', ['%s_roll' %(attrA.split('.')[0]), '%s_roll' %(attrB.split('.')[0])],
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
                'multiplyDivide', name='%s_%s_md_node' %(aimObjs[num], rollAixs))

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
        nodes=mc.ls(sl=1, l=1)

    for n in nodes:

        cn=mc.listConnections(n+'.overrideEnabled')
        cnb=mc.listConnections(n+'.overrideDisplayType')
        if cn is None and cnb is None:
            mc.setAttr(n+'.overrideEnabled',l=0)
            mc.setAttr(n+'.overrideDisplayType',l=0)

            if display=='off':
                mc.setAttr(n+'.overrideEnabled', 0)
            else:
                mc.setAttr(n+'.overrideEnabled', 1)

            if display=='off' or display=='normal':
                mc.setAttr(n+'.overrideDisplayType', 0)
            elif display=='template':
                mc.setAttr(n+'.overrideDisplayType', 1)
            elif display=='reference':
                mc.setAttr(n+'.overrideDisplayType', 2)

            if shape:
                shapenode=mc.listRelatives(n, s=1, f=1)
                if shapenode is not None:
                    for sh in shapenode:
                        scn=mc.listConnections(sh+'.overrideEnabled')
                        scnb=mc.listConnections(sh+'.overrideDisplayType')

                        if scn is None and scnb is None:
                            mc.setAttr(sh+'.overrideEnabled',l=0)
                            mc.setAttr(sh+'.overrideEnabled', 0)

                            mc.setAttr(sh+'.overrideDisplayType',l=0)
                            mc.setAttr(sh+'.overrideDisplayType', 0)