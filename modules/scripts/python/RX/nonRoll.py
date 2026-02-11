#!/usr/bin/python
# -*- coding: utf-8 -*-
# AUTHOR: wangruixi
# RELEASE DATE: 2020/04/22
# LAST UPDATE: 2020/04/22
# VERSION: 1.0
# MAYA: 2018
#--------------------------------------------------------------------------------------------------------------------------------------------

import maya.cmds as mc
from rxCore import aboutPublic
from rxCore import aboutLock
from rxCore import aboutMath

def create( parentJnt, startJnt, rollJnt, nonRollAxis='x', mirror=1, offsetValue=1):
    """

    :param parentJnt: string
    :param startJnt: string
    :param rollJnt:
    :param nonRollAxis: string
    :param mirror: 0 / 1
    :param offsetValue: 0 / 1
    :return: twist objects
    """

    mc.select(cl=True)
    startNonRollJnt = mc.joint(n='{0}_{1}_st_nonRoll_jnt'.format(startJnt, nonRollAxis))
    endNonRollJnt = mc.joint(n='{0}_{1}_ed_nonRoll_jnt'.format(startJnt, nonRollAxis))
    rollLoc = mc.spaceLocator(n='{0}_{1}_twist_loc'.format(startJnt, nonRollAxis))[0]
    mc.select(cl=True)

    # nonroll joint joint
    aboutPublic.snapAtoB(startNonRollJnt, startJnt)
    aboutPublic.snapAtoB(endNonRollJnt, startNonRollJnt)

    # noinspection PyBroadException
    try:
        endJnt = mc.listRelatives(startJnt)[0]
        distance = aboutMath.getDistance(startJnt, endJnt)
    except:
        distance=1

    mc.setAttr(endNonRollJnt+'.t{0}'.format(nonRollAxis), distance*0.2*mirror)

    mc.makeIdentity( startNonRollJnt , apply=True, t=0, r=1, s=0)
    mc.makeIdentity( endNonRollJnt , apply=True, t=0, r=1, s=0)

    # loc   
    mc.delete( mc.parentConstraint(startJnt, rollLoc) )
    mc.parent(rollLoc, startNonRollJnt)
    aboutLock.lock(rollLoc, at='t s jo u v')

    offsetValueJntGrp = ''
    if offsetValue !=1 :
        offsetValueJnt = '{0}_{1}_offset_jnt'.format(startJnt, nonRollAxis)
        offsetValueNode = '{0}_{1}_offset_node'.format(startJnt, nonRollAxis)

        if not mc.objExists(offsetValueJnt):
            mc.duplicate( startJnt, po=1, n=offsetValueJnt )
            mc.makeIdentity( offsetValueJnt , apply=True, t=0, r=1, s=0 )
            offsetValueJntGrp = aboutPublic.fastGrp( offsetValueJnt , grpNameList=['grp', 'rz', 'ry', 'rx'] )

        if not mc.objExists(offsetValueNode):
            mc.createNode('multiplyDivide' , name=offsetValueNode)
                      
        mc.connectAttr( rollLoc+'.'+nonRollAxis , offsetValueNode+'.input1X' )
        mc.setAttr( offsetValueNode+'.input2X', offsetValue)
        mc.connectAttr( offsetValueNode+'.outputX' , offsetValueJnt+'_'+nonRollAxis+'.'+nonRollAxis )

    #create nonroll ikhandle and aim locator.
    nonRollIkh = mc.ikHandle( sj=startNonRollJnt , ee=endNonRollJnt ,sol='ikRPsolver' , n='{0}_{1}_nonRoll_ikh'.format(startJnt, nonRollAxis) )
    mc.setAttr(nonRollIkh[0]+'.rx', 0)
    mc.setAttr(nonRollIkh[0]+'.ry', 0)
    mc.setAttr(nonRollIkh[0]+'.rz', 0)
    mc.setAttr(nonRollIkh[0]+'.poleVectorX', 0)
    mc.setAttr(nonRollIkh[0]+'.poleVectorY', 0)
    mc.setAttr(nonRollIkh[0]+'.poleVectorZ', 0)

    mc.rename( nonRollIkh[1], '{0}_{1}_nonRoll_ikh_eff'.format(startJnt, nonRollAxis) )

    # create and connect bridge
    cmdBridge = mc.createNode('transform', n='{0}_{1}_twist_cmd'.format(startJnt, nonRollAxis))
    valueBridge = mc.createNode('transform', n='{0}_{1}_twist_value'.format(startJnt, nonRollAxis))
    aboutLock.lock(cmdBridge)
    aboutLock.lock(valueBridge)
    aboutPublic.addNewAttr(objects=[cmdBridge],  attrName=['forward','inverse','offset'], lock=False, k=True)
    aboutPublic.addNewAttr(objects=[valueBridge],  attrName=['twist'], lock=False, k=True)

    mdl = mc.createNode('multDoubleLinear', n='{0}_mdl'.format(cmdBridge) )
    mc.connectAttr('{0}.r{1}'.format(rollLoc, nonRollAxis), '{0}.input1'.format(mdl) )
    mc.setAttr('{0}.input2'.format(mdl), mirror*2)

    mdv = mc.createNode('multiplyDivide', n='{0}_mdv'.format(cmdBridge) )
    mc.connectAttr('{0}.output'.format(mdl), '{0}.input1X'.format(mdv) )
    mc.connectAttr('{0}.output'.format(mdl), '{0}.input1Y'.format(mdv) )
    mc.setAttr('{0}.input2X'.format(mdv), 1)
    mc.setAttr('{0}.input2Y'.format(mdv), -1)
    mc.connectAttr('{0}.outputX'.format(mdv), '{0}.forward'.format(cmdBridge) )
    mc.connectAttr('{0}.outputY'.format(mdv), '{0}.inverse'.format(cmdBridge) )

    #pma
    twist_pma = mc.createNode('plusMinusAverage', n='{0}_twist_pma'.format(cmdBridge) )

    mc.connectAttr('{0}.forward'.format(cmdBridge), '{0}.input1D[0]'.format(twist_pma))
    mc.connectAttr('{0}.offset'.format(cmdBridge), '{0}.input1D[2]'.format(twist_pma))
    mc.connectAttr('{0}.output1D'.format(twist_pma), '{0}.twist'.format(valueBridge))

    # clean rig
    # >>>>>> connect nonroll group
    startNonRollJntGrp = aboutPublic.fastGrp( startNonRollJnt, grpNameList=['grp'] )
    nonRollIkhGrp = aboutPublic.fastGrp( nonRollIkh[0], grpNameList=['grp'] )

    mc.parentConstraint(parentJnt, startNonRollJntGrp[0], mo=1)
    mc.pointConstraint(startJnt, startNonRollJnt, mo=1)
    oc = mc.orientConstraint(rollJnt, startNonRollJnt, rollLoc, mo=1, n=rollLoc+'_oc')[0]
    mc.setAttr(oc+'.interpType', 0)
    mc.parentConstraint(startJnt, nonRollIkh[0], mo=1)

    mc.parent(nonRollIkhGrp[0], startNonRollJntGrp[0])

    # >>>>>> create mp nodes
    nox = '{0}_{1}_nonRoll_noTrans'.format(startJnt, nonRollAxis)
    if not mc.objExists(nox):
        mc.createNode('transform', n=nox)
        mc.hide(nox)

    mc.parent(startNonRollJntGrp[0], nox)
    mc.parent(nonRollIkhGrp[0], nox)
    mc.parent(cmdBridge, nox)
    mc.parent(valueBridge, nox)

    if offsetValue != 1:
        mc.parent(offsetValueJntGrp[0], nox)

    result = {'noTrans':nox, 'cmd':cmdBridge, 'vmd':valueBridge}
    return result


def limbTwist(limbJnts=None, twistAxis='x', mirror=1):
    """
    # limbJnts = [['lf_shoulder', 'lf_upArm'], ['lf_upArm', 'lf_loArm', 'lf_wrist']]
    :param limbJnts:
    :param twistAxis:
    :param mirror:
    :return:
    """

    noTrans = []
    vmds = []
    # create nonroll is system
    for i in range( len(limbJnts) ):
        parentJnt = limbJnts[i][0]
        startJnt = limbJnts[i][1]
        rollJnt = limbJnts[i][-1]
        info = create(parentJnt, startJnt, rollJnt, twistAxis, mirror, offsetValue=1)
        noTrans.append(info['noTrans'])
        vmds.append(info['vmd'])

    result = {'noTrans':noTrans, 'vmd':vmds}
    return result