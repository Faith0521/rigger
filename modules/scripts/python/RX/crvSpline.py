#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.11.20
#========================================
from importlib import reload

import maya.cmds as mc
import maya.mel as mel

from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutPublic
from rxCore import aboutApi

import controlTools
import templateTools
import pointOnCrv
import cluster
import rivet
import squeezeTools

reload(pointOnCrv)
#  Create template reference rig for a ikSpline Rig
def crvSplineTemplate(prefix, name, part, numJoints=7, numControls=4, aim=1):
    """
    :param prefix:
    :param name:
    :param part:
    :param numJoints:
    :param numControls:
    :param aim:
    :return:
    """
    # Create Joints.
    color = 'teal'

    joints = []
    for i in range(numJoints):
        jname = prefix + name + aboutName.letter(i)
        jnt = templateTools.createJoint(jname, part, color, pc=1, oc=0)

        mc.xform(jnt[0], ws=1, t=[0, i, 0])
        joints.append(jnt[-1])

    # Orient Joints.
    for i in range(1, numJoints):
        mc.aimConstraint(joints[i] + '_pos', joints[i - 1], n=joints[i - 1] + '_ac', aim=[0, aim, 0],
                         u=[0, 0, 1], wut='objectRotation', wuo=joints[i - 1] + '_pos', wu=[0, 0, 1])
        # fixed pos jnt right axis to next one.
        mc.delete(mc.aimConstraint(joints[i] + '_pos_grp', joints[i - 1] + '_pos_grp',
                                   aim=[0, aim, 0], u=[0, 0, aim], wut='vector', wu=[0, 0, 1]))
        mc.parent(joints[i], joints[i - 1])

    # fixed end pos jnt axis.
    mc.delete(mc.orientConstraint(joints[-2] + '_pos_grp', joints[-1] + '_pos_grp'))

    # create controls
    div = float(numJoints - 1) / float(numControls - 1)
    crv = '{0}{1}_crv_org'.format(prefix, name)
    arg = 'curve -d 1 -n " '+ crv +' " '

    ctrls = []
    for i in range(numControls):
        # controls
        ctrl = controlTools.create(prefix + name + aboutName.letter(i) + '_crvPos',
                                   shape='C02_pole', color='yellow', scale=.8, jointCtrl=True, tag='splineTemp')

        mc.setAttr(ctrl[-1] + '.drawStyle', 0)
        mc.setAttr(ctrl[-1] + '.radi', 1.5)

        # set pos
        mc.xform(ctrl[0], ws=1, t=[0, i * div, 0])
        ctrls.append(ctrl[-1])
        arg += '-p 0 {0} 0 '.format(i * div)

    # create base curve
    crv = mel.eval(arg)
    shape = mc.listRelatives(crv, s=1)[0]
    mc.rename(shape, '{0}Shape'.format(crv))
    mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 1 -kep 1 -kt 0 -s {0} -d 3 -tol 0.01 "{1}";'.format(numControls - 1, crv))

    # create stretch ikSpine system
    strechType = 1
    ikSys = ikSplineByCurve(prefix + name, crv, numJoints, strechType, strechAxis='ty', twistFix=True, volume=False, mpNode=None)
    ikjoints = ikSys['jointList']
    ikRootGrp = ikSys['rootGrp']

    # connect template joints
    groupNodes = []
    tempConnectNode = []
    for j in joints:
        groupNodes.append(j + '_pos_grp')
        tempConnectNode.append(j + '_pos_sdk')

    for i, node in enumerate(tempConnectNode):
        mc.parentConstraint(ikjoints[i], node, n='{0}_prc'.format(node))

    # cluster curve
    for i in range(len(ctrls)):
        cluster.create(['{0}.cv[{1}]'.format(crv, i), ctrls[i]])
    
    # Cleanup
    mc.hide(ikjoints[0])
    mc.parent(groupNodes, part + 'Ctrls')
    mc.parent(ikjoints[0], part + 'Nox')
    mc.parent(ikRootGrp, part + 'Nox')

    for i in range(len(ctrls)):
        mc.parent(ctrls[i] + '_grp', part + 'Ctrls')
        aboutLock.lock([ctrls[i] + '_grp', ctrls[i] + '_con', ctrls[i] + '_sdk', ctrls[i]])
        aboutLock.unlock(ctrls[i] + '_grp', 't r')
        aboutLock.unlock(ctrls[i], 't')

    for i in range(len(joints)):
        aboutLock.lock([joints[i] + '_pos_grp', joints[i] + '_pos_con', joints[i] + '_pos_sdk', joints[i] + '_pos'])

    result = {'jointList':joints, 'ctrls':ctrls, 'crv':crv}
    return result
    

def ikSplineByCurve(prefix, crv, numJoints, strechType, strechAxis='ty', twistFix=False, volume=False, mpNode=None):
    """
    |---------------------------------------------------|
    |Create ikSpline / Thanks for my teacher ZhaoChunHai
    |---------------------------------------------------|
    args:
    prefix  string  the ikSpline name
    crv         string  curve name
    numJoints    int     how many joint build
    strechType  1 2     1 by curveInfo 2 by distanceBetween
    keepVolume  0 1     wiht keep volume ?
    axis default is 'ty'
    """
    # init
    result = {}
    jointList = []
    stretchInfo = []

    # get input crv
    crvShapes = mc.listRelatives(crv, shapes=True)
    if crvShapes is None or mc.objectType(crvShapes[0], isType='nurbsCurve') == 0:
        mc.error('crv type error')
        return
    crvShape = crvShapes[0]
    crvFn = aboutApi.asMFnNurbsCurve(crv)
    # create joint by poci node.
    # -------------------------------------------------------------------------------------------------#
    pociNode = mc.createNode('pointOnCurveInfo', n='{0}pociNode{1}_poci'.format(prefix, crvShape))
    mc.connectAttr(crvShape + '.worldSpace[0]',  pociNode + '.inputCurve', f=True)

    # >> everage
    length = crvFn.length()
    orgLen = 0
    averageLen = length / (numJoints - 1)

    for i in range(0, int(numJoints), 1):
        divide = crvFn.findParamFromLength(orgLen)
        orgLen = orgLen + averageLen

        # >> build joint at everage postion.
        # >> if you crv cv point not everage, please rebuild it.
        mc.setAttr(pociNode + '.parameter', divide)
        locPos = mc.getAttr(pociNode + '.position')[0]
        jnt = mc.joint(p=locPos, n='{0}{1}_jnt'.format(prefix, aboutName.letter(i)))
        jointList.append(jnt)

    mc.delete(pociNode)

    # >> edit joint orient
    mc.joint(jointList[0], e=True, oj='yxz', secondaryAxisOrient='xup', ch=True, zso=True)
    mc.joint(jointList[-1], e=True, oj='none', secondaryAxisOrient='xup', ch=True, zso=True)

    # fixed spline joints advanced twist.
    # need add a new joint at last.
    # thanks for my brother -- Lin lingWei
    if twistFix:
        twistAxis = strechAxis
        twistFixJnt = mc.duplicate(jointList[-1], po=1, n='{0}_twistFix'.format(prefix))[0]
        mc.parent(twistFixJnt, jointList[-1])
        mc.setAttr(twistFixJnt + '.' + twistAxis, mc.getAttr(jointList[-1] + '.' +  twistAxis) * 0.01)
        mc.setAttr(twistFixJnt+'.drawStyle', 2)
        jointList.append(twistFixJnt)

    # create ikh
    ikSys =mc.ikHandle(sol='ikSplineSolver',
                        ccv=False, pcv=False,
                        startJoint=jointList[0], endEffector=jointList[-1],
                        curve=crvShape, n='{0}_spline_ikh'.format(prefix))
    mc.rename(ikSys[1], '{0}_spline_ikh_eff'.format(prefix))

    ikh = ikSys[0]
    mc.hide(ikh)
    mc.select(cl=True)

    # create stretch
    if twistFix:
        joints = jointList[:-1]
    else:
        joints = jointList

    if strechType == 1 or strechType == 2:
        if strechType == 1:
            stretchInfo = stretchByCrvInfo(prefix, crv, joints, axis=strechAxis, volume=volume, mpNode=None)
        else:
            stretchInfo = stretchByPointOnCurve(prefix, crv, joints, axis=strechAxis, volume=volume, mpNode=None)

    # clean
    mpExists = False  # type: bool
    if not mpNode:
        mpNode = '{0}_ikSys_noTrans'.format(prefix)
        mc.createNode('transform', n=mpNode)
        mpExists = True
    elif mc.objExists(mpNode):
        mpExists = True

    if mpExists:
        mc.parent(ikh, mpNode)
        mc.parent(crv, mpNode)
        if strechType != 0:
            mc.parent(stretchInfo['rootGrp'], mpNode)
        aboutLock.lock(mpNode)

    # output
    result['rootGrp'] = mpNode
    result['jointList'] = jointList
    result['ikh'] = ikh

    if strechType != 0:
        result['cmd'] = stretchInfo['cmd']

    return result


def ikSplineByJoints(prefix, crv, jointList, strechType, strechAxis='ty', twistFix=False, volume=False, mpNode=None):
    """
    |---------------------------------------------|
    |make a stretchy ikSpline form selected joints|
    |---------------------------------------------|
    args: 
    prefix  string  the ikSpline name 
    jointStart  string  joint chain root joint.
    jointEnd    string  joint chain tip joint.
    strechType  0 1 2   0 without stretch 1 by curveInfo 2 by distanceBetween     
    keepVolume  0 1     wiht keep volume ?
    """

    # init
    result = {}
    stretchInfo = []

    # get input crv
    crvShapes = mc.listRelatives(crv, shapes=True, f=True)
    if crvShapes is None or mc.objectType(crvShapes[0], isType='nurbsCurve') == 0:
        mc.error('crv type error')
        return
    crvShape = crvShapes[0]

    # fixed spline joints advanced twist.
    # need add a new joint at last.
    # thanks for my brother -- Lin lingWei
    if twistFix:
        twistAxis = strechAxis
        twistFixJnt = mc.duplicate(jointList[-1], po=1, n='{0}_twistFix'.format(prefix))[0]
        mc.parent(twistFixJnt, jointList[-1])
        mc.setAttr(twistFixJnt + '.' + twistAxis, mc.getAttr(jointList[-1] + '.' + twistAxis) * 0.01)
        mc.setAttr(twistFixJnt+'.drawStyle', 2)
        jointList.append(twistFixJnt)

    # create ikh
    ikSys = mc.ikHandle(sol='ikSplineSolver',
                        ccv=False, pcv=False,
                        startJoint=jointList[0], endEffector=jointList[-1],
                        curve=crvShape, n='{0}_spline_ikh'.format(prefix))

    mc.rename(ikSys[1], '{0}_spline_ikh_eff'.format(prefix))
    
    ikh = ikSys[0]
    mc.hide(ikh)
    mc.select(cl=True)
    
    # create stretch
    if twistFix:
        joints = jointList[:-1]
    else:
        joints = jointList

    if strechType == 1 or strechType == 2:
        if strechType == 1:
            stretchInfo = stretchByCrvInfo(prefix, crv, joints, axis=strechAxis, volume=volume, mpNode=None)
        else:
            stretchInfo = stretchByPointOnCurve(prefix, crv, joints, axis=strechAxis, volume=volume, mpNode=None)

    # clean
    mpExists = False
    if not mpNode:
        mpNode = '{0}_iksys_noTrans'.format(prefix)
        mc.createNode('transform', n=mpNode)
        mpExists = True
    elif mc.objExists(mpNode):
        mpExists = True

    if mpExists:
        mc.parent(ikh, mpNode)
        mc.parent(crv, mpNode)
        if strechType != 0:
            mc.parent(stretchInfo['rootGrp'], mpNode)
        mc.hide(mpNode)
        aboutLock.lock(mpNode)

    # output
    result['rootGrp'] = mpNode
    result['jointList'] = jointList
    result['ikh'] = ikh

    if strechType != 0:
        result['cmd'] = stretchInfo['cmd']

    return result


def stretchByCrvInfo(prefix, crv, jointList, axis='ty', volume=False, mpNode=None):
    """
    |---------------------------------------------|
    |you can make a in existence ikSpline stretchy|
    |---------------------------------------------|
    make ikspline stretchy by curveInfo node.
    stretch by translateX.
    all the joints must X axis point at its child
    -----------------------------------------------
    args: 
    prefix  string  the ikSpline name 
    crv  string  the ikspline curve name not curveShape name
    jointList   list    must joint chain.The name list must form root to tip
    strechType  0 1 2   0 without stretch 1 by curveInfo 2 by distanceBetween 
    """

    # to know weather is a curve selected
    # init
    numJoints = len(jointList)

    # get input crv
    crvShapes = mc.listRelatives(crv, shapes=True, f=True)
    if crvShapes is None or mc.objectType(crvShapes[0], isType='nurbsCurve') == 0:
        mc.error('curve type error')
        return
    crvShape = crvShapes[0]

    # create bridge
    cbridge = prefix + '_stretch_cmd_bridge'
    vbridge = prefix + '_stretch_value_bridge'

    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge)
        aboutLock.lock(cbridge)

        aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['stretch'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['volume'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge)
        aboutLock.lock(vbridge)

        aboutPublic.addNewAttr(objects=[vbridge], attrName=['stretch', 'arcLength'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)

        # add org dis attr
        for i in range(1, numJoints, 1):
            jnt = jointList[i]
            orgv = mc.getAttr(jnt + '.' + axis)
            useAttr = 'orgdis{0}'.format(aboutName.letter(i))
            aboutPublic.addNewAttr(objects=[vbridge], attrName=[useAttr],
                                   lock=False, attributeType='float', keyable=True)
            mc.setAttr('{0}.{1}'.format(vbridge, useAttr), orgv)

    # create curveInfo node.
    curveInfo = mc.createNode('curveInfo', n='{0}_ikSys_stretch_crvInfo'.format(prefix))
    mc.connectAttr(crvShape + '.worldSpace', curveInfo + '.inputCurve')

    mc.connectAttr(cbridge+'.stretch', vbridge+'.stretch')
    init_Stretch = '{0}.stretch'.format(vbridge)

    # for global scale and scale
    gl_initScale_mdl = mc.createNode('multDoubleLinear', n='{0}_ikSys_gl_initScale_mdl'.format(prefix))
    mc.connectAttr(cbridge + '.initScale', gl_initScale_mdl + '.input1')
    mc.connectAttr(curveInfo+'.arcLength', gl_initScale_mdl + '.input2')
    mc.connectAttr(gl_initScale_mdl + '.output', vbridge + '.arcLength')

    gl_moveValue_md = mc.createNode('multiplyDivide', n='{0}_ikSys_gl_moveValue_md'.format(prefix))
    mc.setAttr(gl_moveValue_md + '.operation', 2)
    mc.connectAttr(gl_initScale_mdl + '.output', gl_moveValue_md + '.input1X')
    mc.setAttr(gl_moveValue_md + '.input2X', mc.getAttr(curveInfo+'.arcLength'))

    gl_stretchOnOff_bla = mc.createNode('blendTwoAttr', n='{0}_ikSys_gl_stretchOnOff_bla'.format(prefix))
    mc.connectAttr(init_Stretch, gl_stretchOnOff_bla + '.attributesBlender')
    mc.setAttr(gl_stretchOnOff_bla + '.input[0]', 1)
    mc.connectAttr(gl_moveValue_md + '.outputX', gl_stretchOnOff_bla + '.input[1]')

    # stretch by translate method
    for i in range(1, numJoints, 1):
        jnt = jointList[i]
        orgdisAttr = '{0}.orgdis{1}'.format(vbridge, aboutName.letter(i))
        moveValue_md = mc.createNode('multiplyDivide', n='{0}_ikSys_MoveV{1}_md'.format(prefix, aboutName.letter(i)))
        mc.connectAttr(orgdisAttr, moveValue_md + '.input1X')
        mc.connectAttr(gl_stretchOnOff_bla + '.output', moveValue_md + '.input2X')
        mc.connectAttr(moveValue_md + '.outputX', jnt + '.' + axis)

    if volume:
        axislist = ['x','y','z']
        scaleAxis = []
        for a in axislist:
            if a not in axis:
                scaleAxis.append('s'+a)

        squeezeInfo = squeezeTools.baseOnCrvInfo(prefix, curveInfo, jointList, scaleAxis, mpNode=None)
        mc.connectAttr(cbridge + '.volume', squeezeInfo['cmd'] + '.volume')
        mc.connectAttr(cbridge + '.initScale', squeezeInfo['cmd'] + '.initScale')

    # clean
    # create mpNode
    mpExists = False
    if not mpNode:
        mpNode = prefix + '_stretchIk_noTrans'
        mc.createNode('transform', n=mpNode)
        mpExists = True
    elif mc.objExists(mpNode):
        mpExists = True

    if mpExists:
        mc.parent(cbridge, mpNode)
        mc.parent(vbridge, mpNode)
        if volume:
            mc.parent(squeezeInfo['rootGrp'], mpNode)
        mc.hide(mpNode)
        aboutLock.lock(mpNode)

    result= {'rootGrp': mpNode, 'cmd': cbridge, 'vmd': vbridge}
    return result

def stretchByPointOnCurve(prefix, crv, jointList, axis='ty', volume=False, mpNode=None):
    """
    |---------------------------------------------|
    |you can make a in existence ikSpline stretchy|
    |---------------------------------------------|

    args:
    prefix  string  the ikSpline name
    crv  string  the ikspline curve name not curveShape name
    jointList   list    must joint chain.The name list must form root to tip
    """

    # init
    numJoints = len(jointList)
    globalScalMdLs, pociNodeList, disNodeList, splKVScaleYZSw_md = [], [], [], []

    # get input crv
    crvShapes = mc.listRelatives(crv, shapes=True, f=True)
    if crvShapes is None or mc.objectType(crvShapes[0], isType='nurbsCurve') == 0:
        mc.error('crv type error')
        return

    # create bridge
    cbridge = prefix + '_stretch_cmd_bridge'
    vbridge = prefix + '_stretch_value_bridge'

    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge)
        aboutLock.lock(cbridge)

        aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['stretch'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['volume'],
                               lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge)
        aboutLock.lock(vbridge)

        aboutPublic.addNewAttr(objects=[vbridge], attrName=['initScale'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=1)
        aboutPublic.addNewAttr(objects=[vbridge], attrName=['stretch'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
        # add org dis attr
        for i in range(1, numJoints, 1):
            jnt = jointList[i]
            orgv = mc.getAttr(jnt + '.' + axis)
            useAttr_orgdis = 'orgdis{0}'.format(aboutName.letter(i))
            aboutPublic.addNewAttr(objects=[vbridge], attrName=[useAttr_orgdis],
                                   lock=False, attributeType='float', keyable=True)
            mc.setAttr('{0}.{1}'.format(vbridge, useAttr_orgdis), orgv)

            useAttr_realdis = 'realdis{0}'.format(aboutName.letter(i))
            aboutPublic.addNewAttr(objects=[vbridge], attrName=[useAttr_realdis],
                                   lock=False, attributeType='float', keyable=True)

    mc.connectAttr(cbridge + '.initScale', vbridge + '.initScale')
    mc.connectAttr(cbridge + '.stretch', vbridge + '.stretch')

    for i in range(numJoints):
        jnt = jointList[i]
        paraV = pointOnCrv.nearestPointOnCurve(crv, jnt)
        pociNode = mc.createNode('pointOnCurveInfo', n='{0}PointOnCurve{1}_poci'.format(prefix, aboutName.letter(i)))
        mc.setAttr(pociNode + '.turnOnPercentage', 0)
        mc.connectAttr(crv + '.worldSpace[0]', pociNode + '.inputCurve', f=True)
        mc.setAttr(pociNode + '.parameter', float(paraV))
        pociNodeList.append(pociNode)

        if i != 0:
            disNode = mc.createNode('distanceBetween', n='{0}distance{1}_db'.format(prefix, aboutName.letter(i)))
            disNodeList.append(disNode)

    # connect pointOnCurveInfo with distanceBetween
    for i, disNode in enumerate(disNodeList):
        mc.connectAttr(pociNodeList[i] + '.position', disNode + '.point1')
        mc.connectAttr(pociNodeList[i + 1] + '.position', disNode + '.point2')

    # reDeisgn jnts number
    numJoints = len(jointList) - 1

    # stretch by translate method
    for m in range(numJoints):
        #(dis-Otx)/Otx*n*tx+tx = (dis/initScale-Otx)*n+tx

        globalScale_Md = mc.createNode('multiplyDivide', n='{0}globalScale{1}_md'.format(prefix, aboutName.letter(m + 1)))
        mc.setAttr('.operation', 2)

        initScale_mdl = mc.createNode('multDoubleLinear', n='{0}initScale{1}_mdl'.format(prefix, aboutName.letter(m + 1)))

        mc.connectAttr(disNodeList[m] + '.distance', initScale_mdl + '.input1')
        mc.connectAttr(cbridge + '.initScale', initScale_mdl + '.input2')

        mc.connectAttr(initScale_mdl + '.output', vbridge + '.realdis' + aboutName.letter(m + 1))
        mc.connectAttr(vbridge + '.realdis' + aboutName.letter(m + 1), globalScale_Md + '.input1X')
        mc.setAttr(globalScale_Md + '.input2X', 1)

        sub_orgdis_pma = mc.createNode('plusMinusAverage', n='{0}sub_orgdis{1}_md'.format(prefix, aboutName.letter(m + 1)))
        mc.setAttr('.operation', 2)
        mc.connectAttr(globalScale_Md + '.outputX', sub_orgdis_pma + '.input1D[0]')
        mc.connectAttr(vbridge + '.orgdis' + aboutName.letter(m + 1), sub_orgdis_pma + '.input1D[1]')

        stretchOnOff_mdl = mc.createNode('multDoubleLinear', n='{0}stretchOnOff{1}_mdl'.format(prefix, aboutName.letter(m + 1)))
        mc.connectAttr(sub_orgdis_pma + '.output1D', stretchOnOff_mdl + '.input1')
        mc.connectAttr(vbridge + '.stretch', stretchOnOff_mdl + '.input2')

        output_adl = mc.createNode('addDoubleLinear', n='{0}output{1}_adl'.format(prefix, aboutName.letter(m + 1)))
        mc.connectAttr(stretchOnOff_mdl + '.output', output_adl + '.input1')
        mc.connectAttr(vbridge + '.orgdis' + aboutName.letter(m + 1), output_adl + '.input2')

        mc.connectAttr(output_adl + '.output', jointList[m + 1] + '.' + axis, f=True)

    if volume:
        fllList = rivet.curve(jointList, crv, con=False, mo=True, wuo=None, mpnode=None)
        axislist = ['x','y','z']
        scaleAxis = []
        for a in axislist:
            if a not in axis:
                scaleAxis.append('s'+a)
        squeezeInfo = squeezeTools.baseOnSubsection(prefix, fllList, jointList, scaleAxis, mpNode=None)
        mc.connectAttr(cbridge + '.volume', squeezeInfo['cmd'] + '.volume')
        mc.connectAttr(cbridge + '.initScale', squeezeInfo['cmd'] + '.initScale')

    # clean
    # create mpNode
    mpExists = False
    if not mpNode:
        mpNode = prefix + '_stretchIk_noTrans'
        mc.createNode('transform', n=mpNode)
        mpExists = True
    elif mc.objExists(mpNode):
        mpExists = True

    if mpExists:
        mc.parent(cbridge, mpNode)
        mc.parent(vbridge, mpNode)
        if volume:
            mc.parent(squeezeInfo['rootGrp'], mpNode)
        mc.hide(mpNode)
        aboutLock.lock(mpNode)

    result= {'rootGrp': mpNode, 'cmd': cbridge, 'vmd': vbridge}
    return result


def getIkEffortJnt(ikh):
    """
    #--------------------------------------------------------------------------------
    #This Function can get joint list from ikh
    #Note: must have ikh or ikspline
    #FN: getBothJnt(ikh)
    #Date: 2012/10/30_v1.0
    #--------------------------------------------------------------------------------
    """

    stjnt = mc.listConnections(ikh + '.startJoint')
    # print stjnt
    JntList = mc.listRelatives(stjnt, ad=1, type='joint')
    JntList.append(stjnt[0])
    JntList.reverse()

    if len(JntList) == 3:
        return JntList[0], JntList[1], JntList[2]
    elif len(JntList) == 4:
        return JntList[0], JntList[1], JntList[2], JntList[3]    