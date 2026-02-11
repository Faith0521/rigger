#!/usr/bin/python
# -*- coding: utf-8 -*-
# ========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.11.10
# ========================================
from importlib import reload
import maya.cmds as mc

import templateTools
import controlTools
from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutCrv
from rxCore import aboutPublic

import crvSpline
# import spaceTools
import assetCommon
import cluster

# reload
reload(cluster)

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
    info = templateTools.createTopNode('torso', args, lockArgs)
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

    chestlocalctrl = controlTools.create(prefix + 'chest_local_ctrl', shape='C01_cube', color='yellow', scale=.7)
    mc.parentConstraint(endPointCtrl, chestlocalctrl[0], n=chestlocalctrl[0] + '_prc')
    mc.parent(chestlocalctrl[0], topnode + 'Ctrls')

    # Create torso mid ik control
    torsoMidIkctrl = controlTools.create(prefix + 'torsoMid_ik_ctrl', shape='D01_aquare', color='peach', scale=2)
    controlTools.rollCtrlShape(torsoMidIkctrl[-1], axis='x')
    mc.parent(torsoMidIkctrl[0], topnode + 'Ctrls')

    # Create hip anim controls
    hipIkctrl = controlTools.create(prefix + 'hip_ik_ctrl', shape='hip', color='yellow', scale=1)
    mc.parentConstraint(startPointCtrl, hipIkctrl[0], n=hipIkctrl[0] + '_prc')
    mc.parent(hipIkctrl[0], topnode + 'Ctrls')

    hiplocalctrl = controlTools.create(prefix + 'hip_local_ctrl', shape='C01_cube', color='yellow', scale=.7)
    mc.parentConstraint(startPointCtrl, hiplocalctrl[0], n=hiplocalctrl[0] + '_prc')
    mc.parent(hiplocalctrl[0], topnode + 'Ctrls')


    if (numControls % 2) == 0:
        midStratPoint = ctrls[(numControls // 2) - 1]
        midEndPoint = ctrls[(numControls // 2)]
        mc.parentConstraint(midStratPoint, midEndPoint, torsoMidIkctrl[0], n=torsoMidIkctrl[0] + '_prc')
    else:
        midStratPoint = ctrls[(numControls - 1) // 2]
        mc.parentConstraint(midStratPoint, torsoMidIkctrl[0], n=torsoMidIkctrl[0] + '_prc')

    fkCtrlList = [prefix + 'torsoFk_hip_ctrl',
                  prefix + 'torsoFk_A_ctrl',
                  prefix + 'torsoFk_B_ctrl',
                  prefix + 'torsoFk_chest_ctrl']

    for i in range(numControls):
        fkctrl = controlTools.create(fkCtrlList[i], shape='D07_circle', color='cyan', scale=1.5)
        if i == 0:
            aboutCrv.editCrvHull(fkctrl[-1], xyzValue=[1.5, 1.5, 1.5], modifyType='scale')
        mc.parentConstraint(ctrls[i], fkctrl[0], n=fkctrl[0] + '_prc')
        mc.parent(fkctrl[0], topnode + 'Ctrls')
        fkCtrlList.append(fkctrl[-1])

    # Cleanup
    animCtrls = cogs + [chestIkctrl[-1], hipIkctrl[-1], torsoMidIkctrl[-1]]
    aboutLock.lock(animCtrls, 'v')
    aboutLock.lock(fkCtrlList, 'v')
    aboutLock.lock([hip[-2], chestEnd[-2]])
    aboutLock.unlock([hip[-2], chestEnd[-2]], 't ro')

    # mc.setAttr( topnode+'.s',1.15,1.15,1.15 )
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
    parts = templateTools.getParts('torso')
    RigSysInitScale = 'worldA_ctrl.initScale'

    for part in parts:

        # torso init data
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        numCogControls = templateTools.getArgs(part, 'numCogControls')
        numTorsoJoints = templateTools.getArgs(part, 'numTorsoJoints')
        numControls = templateTools.getArgs(part, 'numControls')
        squeeze = templateTools.getArgs(part, 'squeeze')

        # torso org jnts
        chestJnt = prefix + 'chest_drv'
        chestJntEnd = prefix + 'chestEnd_drv'
        hipJnt = prefix + 'hip_drv'
        hipJntEnd = prefix + 'hipEnd_drv'

        mc.parent(chestJnt, w=1)

        drvJnts = []
        for i in range(numTorsoJoints):
            serial = aboutName.letter(i)
            drvJnts.append('{0}torso{1}_drv'.format(prefix, serial))

        # torso template crv
        orgcrv = mc.ls(prefix + 'torso_crv_orgPrep')[0]
        crv = mc.duplicate(orgcrv, n=prefix + 'torso_crv', rc=1)[0]
        shape = mc.listRelatives(crv, s=True)[0]
        mc.rename(shape, crv + 'Shape')
        mc.rebuildCurve(crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=3, d=3, tol=0.01 )

        # torso point locator
        torsoAloc = aboutPublic.snapLoc(crv+'.cv[0]', name='{0}torsoA_loc'.format(prefix))
        torsoBloc = aboutPublic.snapLoc(crv+'.cv[1]', name='{0}torsoB_loc'.format(prefix))
        torsoCloc = aboutPublic.snapLoc(crv+'.cv[2]', name='{0}torsoC_loc'.format(prefix))
        torsoDloc = aboutPublic.snapLoc(crv+'.cv[3]', name='{0}torsoD_loc'.format(prefix))
        torsoEloc = aboutPublic.snapLoc(crv+'.cv[4]', name='{0}torsoE_loc'.format(prefix))
        torsoFloc = aboutPublic.snapLoc(crv+'.cv[5]', name='{0}torsoF_loc'.format(prefix))

        torsoUpperloc = aboutPublic.snapLoc(crv+'.cv[3]', name='{0}torsoUpper_loc'.format(prefix))
        torsoMidloc = aboutPublic.snapLoc(crv + '.cv[2:3]', name='{0}torsoMid_loc'.format(prefix))
        torsoLowerloc = aboutPublic.snapLoc(crv+'.cv[2]', name='{0}torsoLower_loc'.format(prefix))

        # CONTROLS ------------------------------------------------------------------------------------------------------
        # > Create cogs ctrl
        cogs = []
        loc = aboutPublic.snapLoc(prefix + 'torsoA')
        for i in range(numCogControls):
            ltr = aboutName.letter(i)
            name = prefix + 'cog{0}_ctrl'.format(ltr)

            # Only first one create ctrl group.
            grps = 0
            if i == 0:
                grps = 1
            mc.delete(mc.orientConstraint(name + 'Prep', loc))
            ctrls = controlTools.create(name, useShape=name + 'Prep', snapTo=loc, scale=2, makeGroups=grps)
            mc.addAttr(ctrls[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

            if cogs:
                mc.parent(ctrls[-1], cogs[-1])
            cogs.append(ctrls[-1])
        mc.delete(loc)

        # create can moveable pivot ctrl
        controlTools.pivot(cogs[-1])

        # add cog user attributes
        if squeeze:
            mc.addAttr(cogs[0], longName='volume', k=1, dv=0, min=0, max=1)
        mc.addAttr(cogs[0], ln='fk_vis', at='enum', k=1, en='off:on')
        mc.addAttr(cogs[0], ln='ik_vis', at='enum', k=1, en='off:on', dv=1)

        mc.parent(torsoMidloc, cogs[-1])

        # -----------------------------------------------------------------------------------------------------------------------------
        # > fk ctrl
        # Only Support numControls 4

        fkCtrlList = [prefix + 'torsoFk_hip_ctrl',
                      prefix + 'torsoFk_A_ctrl',
                      prefix + 'torsoFk_B_ctrl',
                      prefix + 'torsoFk_chest_ctrl']

        for x in fkCtrlList:
            loc = aboutPublic.snapLoc(x + 'Prep')
            mc.delete(mc.orientConstraint(x + 'Prep', loc))
            controlTools.create(x, useShape=x + 'Prep', snapTo=loc, color='cyan', scale=1.5)
            mc.delete(loc)

        mc.parent(fkCtrlList[2]+'_grp', fkCtrlList[1])

        # >> chest ctrl
        chestIkctrls = controlTools.create(prefix + 'chest_ik_ctrl', useShape=prefix + 'chest_ik_ctrlPrep', snapTo=prefix + 'chest_local_ctrlPrep', makeGroups=1)
        mc.addAttr(chestIkctrls[-1], longName='local', k=1, dv=0, min=0, max=1)

        # >> chest local ctrl
        chestLocalctrls = controlTools.create(prefix + 'chest_local_ctrl', useShape=prefix + 'chest_local_ctrlPrep', snapTo=prefix + 'chest_local_ctrlPrep', makeGroups=1)
        mc.parent(chestLocalctrls[0], fkCtrlList[3])
        mc.parent(fkCtrlList[3]+'_grp', chestIkctrls[-1])
        controlTools.pivot(fkCtrlList[3])

        # add vis
        mc.connectAttr(chestIkctrls[-1] + '.local', chestLocalctrls[0] + '.v')
        # add roll
        controlTools.addRoll(chestIkctrls[-1], axis='ry', refObj=drvJnts[-1])

        # >> mid ctrl
        loc = aboutPublic.snapLoc(crv + '.cv[2:3]')
        mc.delete(mc.orientConstraint(prefix + 'torsoMid_ik_ctrlPrep', loc))
        torsoMidIkctrls = controlTools.create(prefix + 'torsoMid_ik_ctrl', useShape=prefix + 'torsoMid_ik_ctrlPrep', snapTo=loc, makeGroups=1)
        mc.delete(loc)
        # >> add mid ctrl attributes
        mc.addAttr(torsoMidIkctrls[-1], longName='dataScale', k=1, dv=1, min=0.001)

        # >> hip ctrl
        hipIkctrls = controlTools.create(prefix + 'hip_ik_ctrl', useShape=prefix + 'hip_ik_ctrlPrep', snapTo=hipJnt, makeGroups=1)
        mc.addAttr(hipIkctrls[-1], longName='local', k=1, dv=0, min=0, max=1)

        # >> hip local control
        hipLocalctrls = controlTools.create(prefix + 'hip_local_ctrl', useShape=prefix + 'hip_local_ctrlPrep', snapTo=hipJnt, makeGroups=1)
        mc.parent(hipLocalctrls[0], fkCtrlList[0])
        mc.parent(fkCtrlList[0]+'_grp', hipIkctrls[-1])
        controlTools.pivot(fkCtrlList[0])

        # add vis
        mc.connectAttr(hipIkctrls[-1] + '.local', hipLocalctrls[0] + '.v')
        # add roll
        controlTools.addRoll(hipIkctrls[-1], axis='ry', refObj=drvJnts[0])


        # >> control follow ----------------------------------------------------------------------------------------------------
        # Create clusters
        cluster.create([crv + '.cv[0]', torsoAloc])
        cluster.create([crv + '.cv[1]', torsoBloc])
        cluster.create([crv + '.cv[2]', torsoCloc])
        cluster.create([crv + '.cv[3]', torsoDloc])
        cluster.create([crv + '.cv[4]', torsoEloc])
        cluster.create([crv + '.cv[5]', torsoFloc])

        mc.parent(torsoUpperloc, chestIkctrls[-1])
        mc.parent(torsoLowerloc, hipIkctrls[-1])
        mc.parent(torsoEloc, torsoFloc, fkCtrlList[3]+'_pivNeg')
        mc.parent(torsoAloc, torsoBloc, fkCtrlList[0]+'_pivNeg')
        mc.parent(torsoCloc, torsoDloc, torsoMidloc)
        aboutPublic.fastGrp(torsoCloc, ['grp','con','midZero','mid'])
        aboutPublic.fastGrp(torsoDloc, ['grp','con','midZero','mid'])

        mc.pointConstraint(torsoUpperloc, torsoLowerloc, torsoDloc+'_con', mo=1)
        mc.pointConstraint(torsoLowerloc, torsoCloc+'_con', mo=1)
        mc.parentConstraint(fkCtrlList[1], torsoDloc+'_grp', mo=1)
        mc.parentConstraint(fkCtrlList[2], chestIkctrls[0], mo=1)
        mc.pointConstraint(torsoUpperloc, torsoLowerloc, torsoMidIkctrls[0], mo=1)

        # modify mid torso loc rotate pivot.
        mc.parent(torsoCloc, torsoCloc + '_con')
        mc.parent(torsoDloc, torsoDloc + '_con')
        mc.delete(mc.parentConstraint(torsoMidIkctrls[-1], torsoCloc + '_midZero'))
        mc.delete(mc.parentConstraint(torsoMidIkctrls[-1], torsoDloc + '_midZero'))
        mc.parent(torsoCloc, torsoCloc + '_mid')
        mc.parent(torsoDloc, torsoDloc + '_mid')

        loclist = [torsoCloc, torsoDloc]
        for loc in loclist:
            # move
            dataScaleNode = mc.createNode('multiplyDivide', name=prefix + '{0}_dataScale_md'.format(loc))
            mc.connectAttr(torsoMidIkctrls[-1] + '.tx', dataScaleNode + '.input1X')
            mc.connectAttr(torsoMidIkctrls[-1] + '.ty', dataScaleNode + '.input1Y')
            mc.connectAttr(torsoMidIkctrls[-1] + '.tz', dataScaleNode + '.input1Z')
            mc.connectAttr(torsoMidIkctrls[-1] + '.dataScale', dataScaleNode + '.input2X')
            mc.connectAttr(torsoMidIkctrls[-1] + '.dataScale', dataScaleNode + '.input2Y')
            mc.connectAttr(torsoMidIkctrls[-1] + '.dataScale', dataScaleNode + '.input2Z')
            mc.connectAttr(dataScaleNode + '.outputX', loc + '_mid.tx')
            mc.connectAttr(dataScaleNode + '.outputY', loc + '_mid.ty')
            mc.connectAttr(dataScaleNode + '.outputZ', loc + '_mid.tz')
            # # roll
            mc.connectAttr(torsoMidIkctrls[-1] + '.rx', loc + '_mid.rx')
            mc.connectAttr(torsoMidIkctrls[-1] + '.rz', loc + '_mid.rz')

        # Setup spline rig
        ikSys = crvSpline.ikSplineByJoints(prefix + 'torso', crv, drvJnts, twistFix=False, strechType=1, volume=squeeze)
        ikh = ikSys['ikh']
        cmd = ikSys['cmd']

        if squeeze:
            mc.connectAttr(cogs[0] + '.volume', cmd + '.volume')
        if mc.objExists(RigSysInitScale):
            mc.connectAttr(RigSysInitScale, cmd + '.initScale')

        # advanced twist
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

        mc.connectAttr(chestLocalctrls[-1] + '.worldMatrix[0]', ikh + '.dWorldUpMatrixEnd')
        mc.connectAttr(hipLocalctrls[-1] + '.worldMatrix[0]', ikh + '.dWorldUpMatrix')

        # control joints orient
        mc.parent(chestJnt, ikSys['jointList'][-1])
        mc.parentConstraint(chestLocalctrls[-1], chestJnt, mo=1, n=chestJnt + '_prc')
        mc.parentConstraint(hipLocalctrls[-1], hipJnt, mo=1, n=hipJnt + '_prc')

        # >> fk ik vis
        for fkctrl in fkCtrlList:
            shape = mc.listRelatives(fkctrl, s=True)[0]
            mc.connectAttr(cogs[0] + '.fk_vis', shape + '.visibility')

        torsoMidIkctrlsShape = mc.listRelatives(torsoMidIkctrls, s=True)[0]
        mc.connectAttr(cogs[0] + '.ik_vis', torsoMidIkctrlsShape + '.visibility')

        mc.parent(fkCtrlList[1]+'_grp',
                  chestIkctrls[0],
                  torsoMidIkctrls[0],
                  hipIkctrls[0],
                  cogs[-1] + '_pivNeg')

        # IMPORTANT FUNCTION
        # every part need connect with torso rig system
        # ------------------------------------------------------
        connectLocs = mc.ls('*_connect_loc')
        for loc in connectLocs:
            mc.parent(loc, 'noTransform')
            if 'chest' in loc:
                mc.parentConstraint(chestLocalctrls[-1], loc, n=loc + '_prc', mo=1)
                mc.scaleConstraint(chestLocalctrls[-1], loc, n=loc + '_sc', mo=1)
            if 'hip' in loc:
                mc.parentConstraint(hipLocalctrls[-1], loc, n=loc + '_prc', mo=1)
                mc.scaleConstraint(hipLocalctrls[-1], loc, n=loc + '_sc', mo=1)
        # ------------------------------------------------------

        # modify motion joints
        mc.parent(chestJnt.replace('_drv', ''), drvJnts[-2].replace('_drv', ''))
        mc.delete(drvJnts[-1].replace('_drv', ''))
        mc.delete(chestJntEnd.replace('_drv', ''))
        mc.delete(hipJntEnd.replace('_drv', ''))

        # CLEAN UP
        #-------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'torso_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # ctrl parent
        ctrlNeedP = [cogs[0] + '_grp']
        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # noTrans Parent
        nox = mc.createNode('transform', n=prefix + 'torso_noTrans', p='noTransform')
        noTransNeedP = [ikSys['rootGrp']]
        for need in noTransNeedP:
            mc.parent(need, nox)

        # jnts Parent
        jntNeedP = [drvJnts[0]]
        for need in jntNeedP:
            mc.parent(need, mpNode)

        # hide
        needHList = [nox,torsoAloc, torsoBloc, torsoCloc, torsoDloc, torsoEloc, torsoFloc,
                     torsoUpperloc, torsoLowerloc, torsoMidloc]
        for need in needHList:
            mc.hide(need)

        # Tag
        controlTools.tagKeyable(torsoMidIkctrls[-2:], 't')
        controlTools.tagKeyable(chestIkctrls[-1], 't r roll local')
        controlTools.tagKeyable(chestLocalctrls[-1], 't r')
        controlTools.tagKeyable(hipIkctrls[-1], 't r roll local')
        controlTools.tagKeyable(hipLocalctrls[-1], 't r')
        controlTools.tagKeyable(fkCtrlList, 'r')
        controlTools.tagKeyable(cogs[-1], 't r pivotDisplay')

        #spaceTools.tag(chestIkctrls[-1], 'parent:{0} cog:cogGrp worldCtrl:controls world:noTransform'.format(fkCtrlList[-1]))
        mc.rename(cogs[-1] + '_pivNeg', aboutName.unique('cogGrp'))

        # bind joints set create
        bindJnts = drvJnts[0:-1]
        bindJnts.append(chestJnt)
        bindJnts.append(hipJnt)
        assetCommon.bindSet(bindJnts)