#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.11.10
#========================================
from importlib import reload
import maya.cmds as mc

import templateTools
import controlTools
from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutPublic
from rxCore import aboutMatrix

import crvSpline
import spaceTools
import assetCommon
import cluster
import squeezeTools
import stretch1Tools

reload(stretch1Tools)
reload(crvSpline)
reload(squeezeTools)
reload(aboutMatrix)

# Build Tempalte
def template(prefix='', parent='root', numCogControls=2, numTorsoJoints=7, numControls=4, squeeze=False):

    # Arg values to be recorded
    if numCogControls < 1:
        numCogControls = 1

    if numTorsoJoints < 3:
        numTorsoJoints = 3

    args = {}
    args['prefix'] = prefix
    args['parent'] = parent
    args['numCogControls'] = numCogControls
    args['numTorsoJoints'] = numTorsoJoints
    args['numControls'] = numControls
    args['squeeze'] = squeeze

    # Args to lock once part is built
    lockArgs = ['numCogControls',
                'numTorsoJoints',
                'numControls']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('torso_simple', args, lockArgs)
    if not info:
        return

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...

    # Best Human Torso numControls is 4 !!!!
    # If you want more spine template control, please connect TD.
    numControls = 4

    # create torso template rig
    splineOutput = crvSpline.crvSplineTemplate(prefix, 'torso', topnode, numJoints=numTorsoJoints, numControls=numControls)
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

    # Create chest joints
    chest = templateTools.createJoint(prefix + 'chest', topnode, color='teal', oc=1, pc=1)
    chestEnd = templateTools.createJoint(prefix + 'chestEnd', topnode, color='teal', oc=1, pc=1)
    mc.xform(chest[0], ws=1, t=[0, mc.xform(joints[-1], q=1, ws=1, t=1)[1], 0])
    mc.xform(chestEnd[0], ws=1, t=[0, mc.xform(joints[-1], q=1, ws=1, t=1)[1] + 0.5, 0])

    mc.parent(chest[-1], joints[-1])
    mc.parent(chestEnd[-1], chest[-1])
    mc.parent(chest[0], endPointCtrl)
    mc.parent(chestEnd[0], endPointCtrl)

    mc.delete(chest[-1] + '_oc')
    mc.aimConstraint(chestEnd[-2], chest[-1], n=chest[-1] + '_ac', aim=[0, 1, 0], u=[0, 0, 1], wut='objectRotation', wu=[0, 0, 1], wuo=chest[-1] + '_pos')
    mc.aimConstraint(chestEnd[-2], joints[-1], n=joints[-1] + '_ac', aim=[0, 1, 0], u=[0, 0, 1], wut='objectRotation', wu=[0, 0, 1], wuo=joints[-1] + '_pos')

    # Create hip joints
    hip = templateTools.createJoint(prefix + 'hip', topnode, color='teal', oc=1, pc=1)
    hipEnd = templateTools.createJoint(prefix + 'hipEnd', topnode, color='teal', oc=1, pc=1)

    mc.delete(mc.pointConstraint(joints[0], hip[0]))
    mc.xform(hipEnd[0], ws=1, t=[0, -.5, 0])

    mc.delete(hip[-1] + '_oc')
    mc.aimConstraint(hipEnd[-2], hip[-1], n=hip[-1] + '_ac', aim=[0, -1, 0], u=[0, 0, 1], wut='objectRotation', wu=[0, 0, 1], wuo=hip[-1] + '_pos')

    mc.parent(hip[-1], joints[0])
    mc.parent(hipEnd[-1], hip[-1])
    mc.parent(hip[0], startPointCtrl)
    mc.parent(hipEnd[0], startPointCtrl)

    # Create COG anim controls
    cogs = []
    li = 0
    for i in reversed(range(numCogControls)):
        ltr = aboutName.letter(li)

        size = 1.65 + (i * .188)
        ctrl = controlTools.create(prefix + 'cog' + ltr + '_ctrl', shape='D07_circle', color='peach', scale=size)
        mc.parent(ctrl[0], topnode + 'Ctrls')
        cogs.append(ctrl[-1])
        li += 1

    controlTools.setColor(cogs[0], 'yellow')
    
    # Create chest control
    chestIkctrl = controlTools.create(prefix + 'chest_ik_ctrl', shape='D07_circle', color='yellow', scale=2)
    mc.parentConstraint(endPointCtrl, chestIkctrl[0], n=chestIkctrl[0] + '_prc')
    mc.parent(chestIkctrl[0], topnode + 'Ctrls')
    mc.xform(chestIkctrl[-1] + '.cv[3]', chestIkctrl[-1] + '.cv[7]', r=1, t=[0, -.45, 0])

    chestlocalIkctrl = controlTools.create(prefix + 'chest_local_ik_ctrl', shape='C01_cube', color='yellow', scale=.7)
    mc.parentConstraint(endPointCtrl, chestlocalIkctrl[0], n=chestlocalIkctrl[0] + '_prc')
    mc.parent(chestlocalIkctrl[0], topnode + 'Ctrls')

    # Create torso mid ik control
    torsoMidIkctrl = controlTools.create(prefix + 'torsoMid_ik_ctrl', shape='D01_aquare', color='peach', scale=2)
    controlTools.rollCtrlShape(torsoMidIkctrl[-1], axis='x')
    mc.parent(torsoMidIkctrl[0], topnode + 'Ctrls')

    # Create hip anim controls
    hipIkctrl = controlTools.create(prefix + 'hip_ik_ctrl', shape='hip', color='yellow', scale=1)
    mc.parentConstraint(startPointCtrl, hipIkctrl[0], n=hipIkctrl[0] + '_prc')
    mc.parent(hipIkctrl[0], topnode + 'Ctrls')

    hiplocalIkctrl = controlTools.create(prefix + 'hip_local_ik_ctrl', shape='C01_cube', color='yellow', scale=.7)
    mc.parentConstraint(startPointCtrl, hiplocalIkctrl[0], n=hiplocalIkctrl[0] + '_prc')
    mc.parent(hiplocalIkctrl[0], topnode + 'Ctrls')


    if (numControls % 2) == 0:
        midStratPoint = ctrls[(numControls // 2) - 1]
        midEndPoint = ctrls[(numControls // 2)]
        mc.parentConstraint(midStratPoint, midEndPoint, torsoMidIkctrl[0], n=torsoMidIkctrl[0] + '_prc')
    else:
        midStratPoint = ctrls[(numControls - 1) // 2]
        mc.parentConstraint(midStratPoint, torsoMidIkctrl[0], n=torsoMidIkctrl[0] + '_prc')

    # Create torso FK controls
    # fkPointList = []
    # for num in range(numControls):
    #     if num != 0 and num != numControls - 1:
    #         fkPointList.append(ctrls[num])

    fkCtrlList = []
    for i in range(numControls):
        if i != numControls-1:
            ctrlName = prefix + 'torsoFk{0}_ctrl'.format(aboutName.letter(i))
            fkctrl = controlTools.create(ctrlName, shape='D07_circle', color='cyan', scale=1.5)
            mc.parentConstraint(ctrls[i], fkctrl[0], n=fkctrl[0] + '_prc')
            mc.parent(fkctrl[0], topnode + 'Ctrls')
            fkCtrlList.append(fkctrl[-1])


    # Cleanup
    animCtrls = cogs + [chestIkctrl[-1], hipIkctrl[-1], torsoMidIkctrl[-1]]
    aboutLock.lock(animCtrls, 'v')
    aboutLock.lock(fkCtrlList, 'v')
    aboutLock.lock([hip[-2], chestEnd[-2]])
    aboutLock.unlock([hip[-2], chestEnd[-2]], 't ro')

    #mc.setAttr( topnode+'.s',1.15,1.15,1.15 )
    for ctrl in ctrls:
        mc.setAttr(ctrl + '.radi', l=0)
        mc.setAttr(ctrl + '.radi', .6)
        mc.setAttr(ctrl + '.radi', l=1)

    mc.setAttr(topnode + '.ty', 13)
    mc.select(topnode)
    return


# Build Anim
def anim():
    # In fact, we need get parts use getParts funtion
    # but in rig work sence, system want torso part is unique

    # init
    parts = templateTools.getParts('torso_simple')
    RigSysInitScale = 'worldA_ctrl.initScale'


    for part in parts:

        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        numCogControls = templateTools.getArgs(part, 'numCogControls')
        numTorsoJoints = templateTools.getArgs(part, 'numTorsoJoints')
        numControls = templateTools.getArgs(part, 'numControls')
        squeeze = templateTools.getArgs(part, 'squeeze')

        # org jnts
        chestJnt = prefix + 'chest_drv'
        chestJntEnd = prefix + 'chestEnd_drv'
        hipJnt = prefix + 'hip_drv'
        hipJntEnd = prefix + 'hipEnd_drv'

        mc.parent(chestJnt, w=1)
        drvJnts = []
        for i in range(numTorsoJoints):
            serial = aboutName.letter(i)
            drvJnts.append('{0}torso{1}_drv'.format(prefix, serial))

        # Create cogs ctrl
        cogs = []
        loc = aboutPublic.snapLoc(prefix + 'torsoA')
        for i in range(numCogControls):
            ltr = aboutName.letter(i)
            name = prefix + 'cog{0}_ctrl'.format(ltr)

            # Only first one create ctrl group.
            grps = 0
            if i == 0:
                grps = 1
            mc.delete( mc.orientConstraint(name + 'Prep', loc) )
            ctrls = controlTools.create(name, useShape=name + 'Prep', snapTo=loc, scale=2, makeGroups=grps)
            mc.addAttr(ctrls[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

            if cogs:
                mc.parent(ctrls[-1], cogs[-1])
            cogs.append(ctrls[-1])
        mc.delete(loc)

        # add used attribute.
        mc.addAttr(cogs[0], ln='_',at='enum', en='cmds', k=1)
        if squeezeTools:
            mc.addAttr(cogs[0], longName='volume', k=1, dv=0, min=0, max=1)
        mc.addAttr(cogs[0], ln='fk_vis', at='enum',k=1, en='off:on')
        mc.addAttr(cogs[0], ln='ik_vis', at='enum', k=1, en='off:on', dv=1)

        # create can moveable pivot ctrl
        controlTools.pivot(cogs[-1])

        # get template crv
        orgcrv = mc.ls(prefix + 'torso_crv_orgPrep')[0]
        crv = mc.duplicate(orgcrv, n=prefix + 'torso_crv', rc=1)[0]
        shape = mc.listRelatives(crv, s=True)[0]
        mc.rename(shape, crv+'Shape')

        # Create ctrls
        # Only Support numControls 4
        # -----------------------------------------------------------------------------------------------------------------------------

        # >> fk ctrl
        fkCtrlList = []
        for i in range(numControls - 1):
            ctrlName = prefix + 'torsoFk{0}_ctrl'.format(aboutName.letter(i))
            loc = aboutPublic.snapLoc(ctrlName + 'Prep')
            mc.delete(mc.orientConstraint(ctrlName + 'Prep', loc))
            fkCtrl = controlTools.create(ctrlName, useShape=ctrlName + 'Prep', snapTo=loc, color='cyan', scale=1.5)
            fkCtrlList.append(fkCtrl[-1])
            mc.delete(loc)

        fkCtrlList.reverse()
        fkCtrlNum = len(fkCtrlList)
        for i in range(fkCtrlNum):
            if i != fkCtrlNum - 1:
                mc.parent(fkCtrlList[i] + '_grp', fkCtrlList[i + 1])
        fkCtrlList.reverse()

        # >> chest ctrl
        chestPosloc = aboutPublic.snapLoc(chestJnt, name = '{0}chest_pos_loc'.format(prefix))
        chestNonRollloc = mc.duplicate(chestPosloc, n=prefix + 'chest_NonRoll_loc')[0]
        chestTwistloc = mc.duplicate(chestPosloc, n=prefix + 'chest_twist_loc')[0]
        mc.delete(mc.orientConstraint(chestJnt, chestPosloc))

        chestIkctrls = controlTools.create(prefix + 'chest_ik_ctrl', useShape=prefix + 'chest_ik_ctrlPrep', snapTo=chestPosloc,  makeGroups=1)

        chestLocalctrls = controlTools.create(prefix + 'chest_local_ik_ctrl', useShape=prefix + 'chest_local_ik_ctrlPrep', snapTo=chestPosloc,  makeGroups=1)
        mc.parent(chestLocalctrls[0], chestIkctrls[-1])
        mc.parentConstraint(chestLocalctrls[-1], chestPosloc, mo=1, n=chestPosloc+'_prc')
        mc.pointConstraint(chestLocalctrls[-1], chestNonRollloc, n=chestNonRollloc + '_pc')
        mc.parent(chestPosloc, chestNonRollloc, chestTwistloc, chestIkctrls[0])
        controlTools.addRoll(chestIkctrls[-1], axis='ry', refObj=drvJnts[-1])

        # >> mid ctrl
        loc = aboutPublic.snapLoc(prefix + 'torsoMid_ik_ctrlPrep')
        mc.delete( mc.orientConstraint(prefix + 'torsoMid_ik_ctrlPrep', loc) )
        torsoMidIkctrls = controlTools.create(prefix + 'torsoMid_ik_ctrl', useShape=prefix + 'torsoMid_ik_ctrlPrep', snapTo=loc,  makeGroups=1)
        mc.delete(loc)

        # >> hip ctrl
        hipPosloc = aboutPublic.snapLoc(hipJnt, name = '{0}hip_pos_loc'.format(prefix))
        mc.delete(mc.orientConstraint(hipJnt, hipPosloc))

        hipNonRollloc = mc.duplicate(hipPosloc, n=prefix + 'hip_NonRoll_loc')[0]
        hipTwistloc = mc.duplicate(hipPosloc, n=prefix + 'hip_twist_loc')[0]

        hipIkctrls = controlTools.create(prefix + 'hip_ik_ctrl', useShape=prefix + 'hip_ik_ctrlPrep', snapTo=hipPosloc,  makeGroups=1)
        hipLocalctrls = controlTools.create(prefix + 'hip_local_ik_ctrl', useShape=prefix + 'hip_local_ik_ctrlPrep', snapTo=hipPosloc,  makeGroups=1)

        mc.parent(hipLocalctrls[0], hipIkctrls[-1])
        mc.parentConstraint(hipLocalctrls[-1], hipPosloc, mo=1, n=hipPosloc + '_prc')
        mc.pointConstraint(hipLocalctrls[-1], hipNonRollloc, n=hipNonRollloc+'_pc')
        mc.parent(hipPosloc, hipNonRollloc, hipTwistloc, hipIkctrls[0])

        controlTools.addRoll(hipIkctrls[-1], axis='ry', refObj=drvJnts[0])

        # >> control follow
        mc.select(cl=1)
        midAxisSt_jnt = mc.duplicate(hipJnt, po=1, n = '{0}torso_midAxis_st_jnt'.format(prefix))[0]
        midAxisEd_jnt = mc.duplicate(chestJnt, po=1, n = '{0}torso_midAxis_ed_jnt'.format(prefix))[0]
        mc.parent(midAxisEd_jnt, midAxisSt_jnt)

        midAxis_iksys = mc.ikHandle(sj=midAxisSt_jnt, ee=midAxisEd_jnt, sol='ikRPsolver', n='{0}torso_midAxis_ikh'.format(prefix))
        midAxis_ikh = midAxis_iksys[0]
        mc.rename(midAxis_iksys[1], '{0}torso_midAxis_ikh_eff'.format(prefix))

        midAxis_stretchInfo = stretch1Tools.stretchIk(prefix+'torso_midAxis_', hipPosloc, [midAxisSt_jnt, midAxisEd_jnt], chestPosloc, 'ty', mpNode=None)

        mc.parentConstraint(midAxisSt_jnt, midAxisEd_jnt, torsoMidIkctrls[0], mo=1, n=torsoMidIkctrls[0] + '_prc')

        mc.delete( mc.parentConstraint(midAxisEd_jnt, chestTwistloc) )
        mc.delete( mc.parentConstraint(midAxisSt_jnt, hipTwistloc) )
        mc.parent(chestTwistloc, midAxisEd_jnt)
        mc.parent(hipTwistloc, midAxisSt_jnt)
        # -----------------------------------------------------------------------------------------------------------------------------

        # Parent and connect ctrls
        midIkPosloc = mc.duplicate( chestPosloc, n='{0}torso_midAxisIk_posloc'.format(prefix) )[0]
        aboutPublic.createParentGrp(midIkPosloc, 'grp')
        mc.parent(midAxis_ikh, midIkPosloc)

        mc.connectAttr(chestPosloc+'.tx', midIkPosloc+'.tx')
        mc.connectAttr(chestPosloc+'.ty', midIkPosloc+'.ty')
        mc.connectAttr(chestPosloc+'.tz', midIkPosloc+'.tz')

        aboutPublic.createParentGrp(midAxisSt_jnt, 'grp')
        mc.connectAttr(hipPosloc+'.tx', midAxisSt_jnt+'.tx')
        mc.connectAttr(hipPosloc+'.ty', midAxisSt_jnt+'.ty')
        mc.connectAttr(hipPosloc+'.tz', midAxisSt_jnt+'.tz')

        # Create clusters
        cluster.create([crv + '.cv[0]', hipPosloc])
        cluster.create([crv + '.cv[3]', chestPosloc])
        cluster.create([crv + '.cv[1:2]', torsoMidIkctrls[-1]])

        # Setup spline rig
        ikSys = crvSpline.ikSplineByJoints(prefix + 'torso', crv, drvJnts, twistFix=False, strechType=1, volume=squeeze)
        ikh = ikSys['ikh']
        cmd = ikSys['cmd']

        if squeeze:
            mc.connectAttr(cogs[0] + '.volume', cmd + '.volume')
        if mc.objExists(RigSysInitScale):
            mc.connectAttr(RigSysInitScale, cmd+'.initScale')

        # set nonroll axis twist by maya matrix
        aboutMatrix.matrixTwist(chestPosloc, chestNonRollloc, twistObj=chestTwistloc, weightList=[1,0], axis='y')
        aboutMatrix.matrixTwist(hipPosloc, hipNonRollloc, twistObj=hipTwistloc, weightList=[1,0], axis='y')

        mc.setAttr(ikh+'.dTwistControlEnable', 1)
        mc.setAttr(ikh+'.dWorldUpType', 4)
        mc.setAttr(ikh+'.dForwardAxis', 2)
        mc.setAttr(ikh+'.dWorldUpAxis', 3)

        mc.setAttr(ikh+'.dWorldUpVectorX', 0)
        mc.setAttr(ikh+'.dWorldUpVectorY', 0)
        mc.setAttr(ikh+'.dWorldUpVectorZ', 1)

        mc.setAttr(ikh+'.dWorldUpVectorEndX', 0)
        mc.setAttr(ikh+'.dWorldUpVectorEndY', 0)
        mc.setAttr(ikh+'.dWorldUpVectorEndZ', 1)

        mc.connectAttr(chestTwistloc+'.worldMatrix[0]', ikh+'.dWorldUpMatrixEnd')
        mc.connectAttr(hipTwistloc+'.worldMatrix[0]', ikh+'.dWorldUpMatrix')

        # control joints orient
        mc.parent(chestJnt, ikSys['jointList'][-1])
        mc.parentConstraint(chestPosloc, chestJnt, mo=1, n=chestJnt + '_prc')
        mc.parentConstraint(hipPosloc, hipJnt, mo=1, n=hipJnt + '_prc')

        # >> fk ik vis
        for fkctrl in fkCtrlList:
            shape = mc.listRelatives(fkctrl, s=True)[0]
            mc.connectAttr(cogs[0]+'.fk_vis', shape+'.visibility')

        torsoMidIkctrlsShape = mc.listRelatives(torsoMidIkctrls, s=True)[0]
        mc.connectAttr(cogs[0]+'.ik_vis', torsoMidIkctrlsShape+'.visibility')

        mc.parent(chestIkctrls[0], fkCtrlList[-1])
        midAxis_needP = prefix+'torso_midAxis_p_to_cogs'
        if not mc.objExists(midAxis_needP):
            mc.createNode('transform', n=midAxis_needP)
            mc.parent( midIkPosloc + '_grp', midAxisSt_jnt+'_grp', midAxis_needP)
            mc.hide(midAxis_needP)

        mc.parent(fkCtrlList[0] + '_grp', midAxis_needP, torsoMidIkctrls[0], hipIkctrls[0], cogs[-1] + '_pivNeg')
        
        # IMPORTANT FUNCTION
        # every part need connect with torso rig system
        #------------------------------------------------------
        connectLocs = mc.ls('*_connect_loc')
        for loc in connectLocs:
            mc.parent(loc, 'noTransform')
            if 'chest' in loc:
                mc.parentConstraint(chestLocalctrls[-1], loc, n=loc + '_prc', mo=1)
                mc.scaleConstraint(chestLocalctrls[-1], loc, n=loc + '_prc', mo=1)
            if 'hip' in loc:
                mc.parentConstraint(hipLocalctrls[-1], loc, n=loc + '_prc',  mo=1)
                mc.scaleConstraint(hipLocalctrls[-1], loc, n=loc + '_prc',  mo=1)
        # ------------------------------------------------------

        # modify motion joints
        mc.parent(chestJnt.replace('_drv', ''), drvJnts[-2].replace('_drv', ''))
        mc.delete(drvJnts[-1].replace('_drv', ''))
        mc.delete(chestJntEnd.replace('_drv', ''))
        mc.delete(hipJntEnd.replace('_drv', ''))

        # clean
        mpNode = '{0}mod'.format(prefix+'torso_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n = mpNode)
            mc.parent(mpNode, 'controls')

        # ctrl parent
        ctrlNeedP = [ cogs[0] + '_grp' ]
        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # noTrans Parent
        nox = mc.createNode('transform', n=prefix + 'torso_noTrans', p='noTransform')
        noTransNeedP = [ midAxis_stretchInfo['rootGrp'], ikSys['rootGrp'] ]
        for need in noTransNeedP:
            mc.parent(need, nox)

        # jnts Parent
        jntNeedP = [ drvJnts[0] ]
        for need in jntNeedP:
            mc.parent(need, mpNode)

        # hide
        needHList = [nox, chestPosloc, chestNonRollloc, chestTwistloc, hipPosloc, hipNonRollloc, hipTwistloc]
        for need in needHList:
            mc.hide(need)

        # Tag
        controlTools.tagKeyable(torsoMidIkctrls[-2:], 't')
        controlTools.tagKeyable(chestIkctrls[-1], 't r roll')
        controlTools.tagKeyable(hipIkctrls[-1], 't r roll')
        controlTools.tagKeyable(chestLocalctrls[-1], 't r')
        controlTools.tagKeyable(fkCtrlList, 'r')
        controlTools.tagKeyable(cogs[-1], 't r pivotDisplay')
        controlTools.tagKeyable(cogs[0], 't r volume ik_vis fk_vis')

        spaceTools.tag(chestIkctrls[-1], 'parent:{0} cog:cogGrp worldCtrl:controls world:noTransform'.format(fkCtrlList[-1]))

        mc.rename(cogs[-1] + '_pivNeg', aboutName.unique('cogGrp'))

        # bind joints set create
        bindJnts = drvJnts[0:-1]
        bindJnts.append(chestJnt)
        bindJnts.append(hipJnt)
        assetCommon.bindSet(bindJnts)
