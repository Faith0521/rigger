#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.11.26
#========================================

######################################
#   Rig Build Part
######################################
from importlib import reload
import maya.cmds as mc

import templateTools
import controlTools
from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutPublic
from rxCore import aboutMatrix
import spaceTools
import cluster
import crvSpline
import stretch1Tools

reload(controlTools)

# Build Tempalte
def template(side='cn', prefix='', parent='chest', numNeckJoints=5, numControls=4, squeeze=False, createJaw=True):

    if numNeckJoints < 1:
        numNeckJoints = 1

    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['numNeckJoints'] = numNeckJoints
    args['numControls'] = numControls
    args['squeeze'] = squeeze
    args['createJaw'] = createJaw

    # Args to lock once part is built
    lockArgs=[ 'numNeckJoints', 'numControls', 'createJaw']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('neck', args, lockArgs)
    if not info:
        print ('Exiting... ')
        return

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...
    # Best numControls is 4 !!!!
    # If you want more spine template control, please connect TD.
    numControls = 4

    # create neck template rig
    splineOutput = crvSpline.crvSplineTemplate(prefix, 'neck', topnode, numJoints=numNeckJoints, numControls=numControls)
    joints = splineOutput['jointList']
    ctrls = splineOutput['ctrls']

    # Constrain center crv points
    num = 0
    aw = 1.0
    bw = 0.0
    incriment = 1.0 / (numControls - 1)

    startPointCtrl = ctrls[0]
    endPointCtrl = ctrls[numControls - 1]

    while num < numControls:
        if num != 0 and num != numControls - 1:
            mc.pointConstraint(startPointCtrl, ctrls[num] + '_grp', weight=aw, n=ctrls[num] + '_pc', mo=1)
            mc.pointConstraint(endPointCtrl, ctrls[num] + '_grp', weight=bw, mo=1)
        aw = aw - incriment
        bw = bw + incriment
        num += 1

    # Create head joints
    head = templateTools.createJoint(prefix + 'head', topnode, color='teal', oc=1, pc=1)
    headEnd = templateTools.createJoint(prefix + 'headEnd', topnode, color='teal', oc=1, pc=1)
    mc.xform(head[0], ws=1, t=[0, mc.xform(joints[-1], q=1, ws=1, t=1)[1], 0])
    mc.xform(headEnd[0], ws=1, t=[0, mc.xform(joints[-1], q=1, ws=1, t=1)[1] + 1, 0])

    mc.parent(head[-1], joints[-1])
    mc.parent(headEnd[-1], head[-1])
    mc.parent(head[0], endPointCtrl)
    mc.parent(headEnd[0], endPointCtrl)

    mc.delete(head[-1] + '_oc')
    mc.aimConstraint(headEnd[-2], head[-1], n=head[-1] + '_ac', aim=[0, 1, 0],
                     u=[0, 0, 1], wut='objectRotation', wu=[0, 0, 1], wuo=head[-1] + '_pos')
    mc.aimConstraint(headEnd[-2], joints[-1], n=joints[-1] + '_ac', aim=[0, 1, 0],
                     u=[0, 0, 1], wut='objectRotation', wu=[0, 0, 1], wuo=joints[-1] + '_pos')

    # Create head anim control
    headIkctrl = controlTools.create(prefix + 'head_ik_ctrl', shape='D07_circle', color='yellow', scale=1.5)
    mc.parentConstraint(endPointCtrl, headIkctrl[0], n=headIkctrl[0] + '_prc')
    mc.parent(headIkctrl[0], topnode + 'Ctrls')

    headlocalIkctrl = controlTools.create(prefix + 'head_local_ik_ctrl', shape='C01_cube', color='yellow', scale=.5)
    mc.parentConstraint(endPointCtrl, headlocalIkctrl[0], n=headlocalIkctrl[0] + '_prc')
    mc.parent(headlocalIkctrl[0], topnode + 'Ctrls')
    
    # Create neck anim controls
    neckIkctrl = controlTools.create(prefix + 'neck_ik_ctrl', shape='D07_circle', color='yellow', scale=1.7)
    mc.parentConstraint(startPointCtrl, neckIkctrl[0], n=neckIkctrl[0] + '_prc')
    mc.parent(neckIkctrl[0], topnode + 'Ctrls')

    necklocalIkctrl = controlTools.create(prefix + 'neck_local_ik_ctrl', shape='C01_cube', color='yellow', scale=.5)
    mc.parentConstraint(startPointCtrl, necklocalIkctrl[0], n=necklocalIkctrl[0] + '_prc')
    mc.parent(necklocalIkctrl[0], topnode + 'Ctrls')
    
    # Create neck anim control
    neckMidIkctrl = controlTools.create(prefix + 'neckMid_ik_ctrl', shape='D01_aquare', color='peach', scale=1.5)
    controlTools.rollCtrlShape(neckMidIkctrl[-1], axis='x')
    mc.parent(neckMidIkctrl[0], topnode + 'Ctrls')

    if (numControls % 2) == 0:
        midStratPoint = ctrls[(numControls // 2) - 1]
        midEndPoint = ctrls[(numControls // 2)]
        mc.parentConstraint(midStratPoint, midEndPoint, neckMidIkctrl[0], n=neckMidIkctrl[0] + '_prc')
    else:
        midStratPoint = ctrls[(numControls - 1) // 2]
        mc.parentConstraint(midStratPoint, neckMidIkctrl[0], n=neckMidIkctrl[0] + '_prc')

    if createJaw:
        jaw = templateTools.createJoint(prefix+'jaw', topnode, color='teal', oc=0, pc=1)
        jawEnd = templateTools.createJoint(prefix+'jawEnd', topnode, color='teal',oc=0, pc=1)
        mc.parent(jawEnd[0], jaw[-2])
        mc.parent(jawEnd[-1], jaw[-1])

        mc.aimConstraint(jawEnd[-2], jaw[-1], n=jaw[-1]+'_ac', aim=[0,0,1], u=[1,0,0], wut='objectRotation', wu=[1,0,0], wuo=jaw[-1]+'_pos')
        mc.delete(mc.pointConstraint(joints[-1], jaw[0]))
        mc.setAttr(jaw[0]+'.tz', .5)
        mc.setAttr(jawEnd[0]+'.tz', 2)

        mc.parent(jaw[0], head[-1]+'_pos')
        mc.parent(jaw[-1], head[-1])

        jawCtrl = controlTools.create(prefix+'jaw_ctrl', shape='Y00_proxy_limb_ankle', color='lemon', scale=[1,1,1])
        controlTools.rollCtrlShape(jawCtrl[-1], axis='z', value=180)
        controlTools.rollCtrlShape(jawCtrl[-1], axis='x', value=90)
        mc.parentConstraint(jaw[-1], jawCtrl[0], n=jawCtrl[0]+'_prc')
        mc.pointConstraint(jaw[-1], jawEnd[-1], jawCtrl[1], n=jawCtrl[1]+'_pc')
        mc.parent(jawCtrl[0], topnode+'Ctrls')

        aboutLock.lock(jaw+jawEnd)
        aboutLock.unlock([jaw[-2], jawEnd[-2], headEnd[-2]], 't')
        aboutLock.lock(jawCtrl)


    # Cleanup
    animCtrls = [headIkctrl[-1], headlocalIkctrl[-1], neckIkctrl[-1], necklocalIkctrl[-1], neckMidIkctrl[-1]]
    aboutLock.lock(animCtrls, 'v')
    aboutLock.lock(headEnd)
    aboutLock.unlock(headEnd[-1]+'_pos', 'ty')

    for ctrl in ctrls:
        mc.setAttr(ctrl + '.radi', l=0)
        mc.setAttr(ctrl + '.radi', .6)
        mc.setAttr(ctrl + '.radi', l=1)

    # Positiion
    mc.xform(topnode, ws=1, t=[0, 13, 0])
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))

    return


# Build Anim

def anim():

    parts = templateTools.getParts('neck')
    RigSysInitScale = 'worldA_ctrl.initScale'

    for part in parts:
    
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        numNeckJoints = templateTools.getArgs(part, 'numNeckJoints')
        numControls = templateTools.getArgs(part, 'numControls')
        prefix = templateTools.getPrefix('', prefix)
        squeeze = templateTools.getArgs(part, 'squeeze')
        createJaw = templateTools.getArgs(part, 'createJaw')

        # org jnts
        headJnt = prefix + 'head_drv'
        neckJnt = prefix + 'neckA_drv'
        drvJnts = []
        for i in range(numNeckJoints):
            serial = aboutName.letter(i)
            drvJnts.append('{0}neck{1}_drv'.format(prefix, serial))

        # get template crv
        orgcrv = mc.ls(prefix + 'neck_crv_orgPrep')[0]
        crv = mc.duplicate(orgcrv, n=prefix + 'neck_crv', rc=1)[0]
        shape = mc.listRelatives(crv, s=True)[0]
        mc.rename(shape, crv + 'Shape')

        # Create ctrls
        # -----------------------------------------------------------------------------------------------------------------------------
        # >> head ctrl
        headPosLoc = aboutPublic.snapLoc(drvJnts[-1], name=prefix + 'head_pos_loc')
        mc.delete( mc.parentConstraint(prefix + 'head_ik_ctrlPrep', headPosLoc) )

        headNonRollloc = mc.duplicate(headPosLoc, n=prefix + 'head_NonRoll_loc')[0]
        headTwistloc = mc.duplicate(headPosLoc, n=prefix + 'head_twist_loc')[0]

        headIkctrls = controlTools.create(prefix + 'head_ik_ctrl', useShape=prefix + 'head_ik_ctrlPrep', snapTo=headPosLoc, makeGroups=1)
        headlocalIkctrl = controlTools.create(prefix + 'head_local_ik_ctrl', useShape=prefix + 'head_local_ik_ctrlPrep', snapTo=headPosLoc, scale=1)

        mc.parent(headlocalIkctrl[0], headIkctrls[-1])
        mc.parentConstraint(headlocalIkctrl[-1], headPosLoc, n=headPosLoc+'_prc')
        mc.pointConstraint(headlocalIkctrl[-1], headNonRollloc, n=headNonRollloc + '_pc')
        mc.parent(headPosLoc, headNonRollloc, headTwistloc, headIkctrls[0])
        controlTools.addRoll(headIkctrls[-1], axis='ry', refObj=drvJnts[-1])

        # >> mid ctrl
        loc = aboutPublic.snapLoc(prefix + 'neckMid_ik_ctrlPrep')
        mc.delete(mc.parentConstraint(prefix + 'neckMid_ik_ctrlPrep', loc))
        neckMidIkctrls = controlTools.create(prefix + 'neckMid_ik_ctrl', useShape=prefix + 'neckMid_ik_ctrlPrep', snapTo=loc, makeGroups=1)
        mc.delete(loc)
    
        # >> neck ctrl
        neckPosLoc = aboutPublic.snapLoc(drvJnts[0], name=prefix + 'neck_pos_loc')
        mc.delete(mc.parentConstraint(prefix + 'neck_ik_ctrlPrep', neckPosLoc))

        neckNonRollloc = mc.duplicate(neckPosLoc, n=prefix + 'neck_NonRoll_loc')[0]
        neckTwistloc = mc.duplicate(neckPosLoc, n=prefix + 'neck_twist_loc')[0]

        neckIkctrls = controlTools.create(prefix + 'neck_ik_ctrl', useShape=prefix + 'neck_ik_ctrlPrep', snapTo=neckPosLoc, makeGroups=1)
        necklocalIkctrl = controlTools.create(prefix + 'neck_local_ik_ctrl', useShape=prefix + 'neck_local_ik_ctrlPrep', snapTo=neckPosLoc, scale=1)

        mc.parent(necklocalIkctrl[0], neckIkctrls[-1])
        mc.parentConstraint(necklocalIkctrl[-1], neckPosLoc, n=neckPosLoc+'_prc')
        mc.pointConstraint(necklocalIkctrl[-1], neckNonRollloc, n=neckNonRollloc+'_pc')
        mc.parent(neckPosLoc, neckNonRollloc, neckTwistloc, neckIkctrls[-1])
        controlTools.addRoll(neckIkctrls[-1], axis='ry', refObj=drvJnts[0])

        # add used attribute.
        mc.addAttr(neckIkctrls[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        if squeeze:
            mc.addAttr(neckIkctrls[-1], longName='volume', k=1, dv=0, min=0, max=1)
        mc.addAttr(neckIkctrls[-1], ln='ik_vis', at='enum', k=1, en='off:on', dv=1)

        # >> jaw ctrl
        if createJaw:
            jawJnt = prefix + 'jaw_drv'
            loc = aboutPublic.snapLoc(jawJnt)
            jawCtrls = controlTools.create(prefix + 'jaw_ctrl', useShape=prefix + 'jaw_ctrlPrep', snapTo=loc, makeGroups=1)
            controlTools.tagKeyable(jawCtrls[-1:], 'r')
            mc.parentConstraint(jawCtrls[-1], jawJnt, mo=1, n=jawJnt+'_prc')
            mc.parent(jawCtrls[0], headlocalIkctrl[-1])
            mc.delete(loc)

        # >> control follow
        mc.select(cl=1)
        midAxisSt_jnt = mc.duplicate(prefix + 'neckA', po=1, n='{0}neck_midAxis_st_jnt'.format(prefix))[0]
        midAxisEd_jnt = mc.duplicate(prefix + 'head', po=1, n='{0}neck_midAxis_ed_jnt'.format(prefix))[0]
        mc.parent(midAxisEd_jnt, midAxisSt_jnt)
    
        midAxis_iksys = mc.ikHandle(sj=midAxisSt_jnt, ee=midAxisEd_jnt, sol='ikRPsolver', n='{0}neck_midAxis_ikh'.format(prefix))
        midAxis_ikh = midAxis_iksys[0]
        mc.rename(midAxis_iksys[1], '{0}neck_midAxis_ikh_eff'.format(prefix))
    
        midAxis_stretchInfo = stretch1Tools.stretchIk(prefix + 'neck_midAxis_', neckPosLoc, [midAxisSt_jnt, midAxisEd_jnt], headPosLoc, 'ty', mpNode=None)
    
        mc.parentConstraint(midAxisSt_jnt, midAxisEd_jnt, neckMidIkctrls[0], mo=1, n=neckMidIkctrls[0] + '_prc')

        mc.delete( mc.parentConstraint(midAxisEd_jnt, headTwistloc) )
        mc.delete( mc.parentConstraint(midAxisSt_jnt, neckTwistloc) )
        mc.parent(headTwistloc, midAxisEd_jnt)
        mc.parent(neckTwistloc, midAxisSt_jnt)
        # -----------------------------------------------------------------------------------------------------------------------------

        # Parent and connect ctrls
        # Parent and connect ctrls
        midIkPosloc = mc.duplicate( headPosLoc, n='{0}neck_midAxisIk_posloc'.format(prefix) )[0]
        aboutPublic.createParentGrp(midIkPosloc, 'grp')
        mc.parent(midAxis_ikh, midIkPosloc)

        mc.connectAttr(headPosLoc + '.tx', midIkPosloc + '.tx')
        mc.connectAttr(headPosLoc + '.ty', midIkPosloc + '.ty')
        mc.connectAttr(headPosLoc + '.tz', midIkPosloc + '.tz')
    
        aboutPublic.createParentGrp(midAxisSt_jnt, 'grp')
        mc.connectAttr(neckPosLoc + '.tx', midAxisSt_jnt + '.tx')
        mc.connectAttr(neckPosLoc + '.ty', midAxisSt_jnt + '.ty')
        mc.connectAttr(neckPosLoc + '.tz', midAxisSt_jnt + '.tz')
    
        # Create clusters
        cluster.create([crv + '.cv[0]', neckPosLoc])
        cluster.create([crv + '.cv[3]', headPosLoc])
        cluster.create([crv + '.cv[1:2]', neckMidIkctrls[-1]])
    
        # Hook up joints
        joints = []
        for i in range(numNeckJoints):
            serialString = aboutName.letter(i)
            joints.append('{0}neck{1}'.format(prefix, serialString))
    
        # Setup spline rig
        ikSys = crvSpline.ikSplineByJoints(prefix + 'neck', crv, drvJnts, twistFix=False, strechType=2, volume=squeeze)
        ikh = ikSys['ikh']
        cmd = ikSys['cmd']

        if squeeze:
            mc.connectAttr(neckIkctrls[-1] + '.volume', cmd + '.volume')

        if mc.objExists(RigSysInitScale):
            mc.connectAttr(RigSysInitScale, cmd + '.initScale')

        # set nonroll axis twist by maya matrix
        aboutMatrix.matrixTwist(headPosLoc, headNonRollloc, twistObj=headTwistloc, weightList=[1, 0], axis='y')
        aboutMatrix.matrixTwist(neckPosLoc, neckNonRollloc, twistObj=neckTwistloc, weightList=[1, 0], axis='y')

        mc.setAttr(ikh + '.dTwistControlEnable', 1)
        mc.setAttr(ikh + '.dWorldUpType', 4)
        mc.setAttr(ikh + '.dForwardAxis', 2)
        mc.setAttr(ikh + '.dWorldUpAxis', 3)
    
        mc.setAttr(ikh + '.dWorldUpVectorX', 0)
        mc.setAttr(ikh + '.dWorldUpVectorY', 0)
        mc.setAttr(ikh + '.dWorldUpVectorZ', 1)
    
        mc.setAttr(ikh + '.dWorldUpVectorEndX', 0)
        mc.setAttr(ikh + '.dWorldUpVectorEndY', 0)
        mc.setAttr(ikh + '.dWorldUpVectorEndZ', 1)

        mc.connectAttr(headTwistloc + '.worldMatrix[0]', ikh + '.dWorldUpMatrixEnd')
        mc.connectAttr(neckTwistloc + '.worldMatrix[0]', ikh + '.dWorldUpMatrix')
    
        # control joints orient
        mc.parentConstraint(headPosLoc, headJnt, mo=1, n=headJnt + '_prc')

        # clean
        neckMidIkctrlsShape = mc.listRelatives(neckMidIkctrls, s=True)[0]
        mc.connectAttr(neckIkctrls[-1]+'.ik_vis', neckMidIkctrlsShape+'.visibility')

        drvJnts.append(headJnt)
        drvJnts.append(neckJnt)

        midAxis_needP = prefix + 'neck_midAxis_p_to_root'
        if not mc.objExists(midAxis_needP):
            mc.createNode('transform', n=midAxis_needP)
            mc.parent(midIkPosloc + '_grp', midAxisSt_jnt + '_grp', midAxis_needP)
            mc.hide(midAxis_needP)
    
        mc.parent(midAxis_needP, neckMidIkctrls[0], neckIkctrls[-1])

        # connect with torso
        if mc.objExists(parent):
            connectLoc = parent + '_connect_loc'
            mc.parentConstraint(connectLoc, neckIkctrls[0], n=neckIkctrls[0]+'_prc', mo=1)
        else:
            connectLoc = None

        # clean
        mpNode = '{0}mod'.format(prefix + 'neck_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # ctrl parent
        mc.parent(headIkctrls[0], neckIkctrls[-1])
        ctrlNeedP = [neckIkctrls[0]]
        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        nox = mc.createNode('transform', n=prefix + 'neck_noTrans', p='noTransform')
        noTransNeedP = [midAxis_stretchInfo['rootGrp'], ikSys['rootGrp']]
        for need in noTransNeedP:
            mc.parent(need, nox)

        # jnts Parent
        jntNeedP = [ drvJnts[0] ]
        for need in jntNeedP:
            mc.parent(need, mpNode)

        # hide
        needHList = [nox, headPosLoc, headTwistloc, headNonRollloc, neckPosLoc, neckTwistloc, neckNonRollloc]
        for need in needHList:
            mc.hide(need)

        # Tag
        controlTools.tagKeyable(neckIkctrls[-1], 't r volume')
        controlTools.tagKeyable(neckMidIkctrls[-2:], 't')
        controlTools.tagKeyable(headIkctrls[-1], 't r')

        # Space
        spaceTools.tag(headIkctrls[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(neckIkctrls[-1]), oo=True)



