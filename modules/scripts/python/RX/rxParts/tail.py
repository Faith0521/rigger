######################################
#   Rig Build Part
######################################
from importlib import reload
import maya.cmds as mc
import maya.mel as mel

import templateTools
import controlTools
from rxCore import aboutName
from rxCore import aboutLock
from rxCore import aboutPublic

import nurbSpline
import spaceTools
import rivet
import cluster

reload(nurbSpline)


# Build Tempalte
def template(side='cn', prefix='', parent='hip', numControls=5, numIkCtrls=5, numFkCtrls=7, numJoints=10, numTipJoints=6, wave=False, roll=False, dynamic=False):
    if numFkCtrls < 3:
        numFkCtrls = 3

    if numIkCtrls < 3 and numIkCtrls != 0:
        numIkCtrls = 3

    if numTipJoints > 0 and numTipJoints > numJoints:
        numTipJoints = numJoints / 3

    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['numControls'] = numControls
    args['numJoints'] = numJoints
    args['numFkCtrls'] = numFkCtrls
    args['numIkCtrls'] = numIkCtrls
    args['numTipJoints'] = numTipJoints
    args['wave'] = wave
    args['roll'] = roll
    args['dynamic'] = dynamic

    # Args to lock once part is built
    lockArgs = ['numJoints', 'numFkCtrls', 'numIkCtrls', 'numTipJoints']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('tail', args, lockArgs)
    if not info:
        print ('Exiting... ')
        return

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...

    # set mirror and color
    color = 'blue'
    mirror = 1
    if side == 'rt':
        mirror = -1
        color = 'red'

    # Create torso template rig
    tailOutput = nurbSpline.createTemplate('tail', topnode, prefix, numControls=numControls, numJoints=numJoints, numFkCtrls=numFkCtrls, )
    joints = tailOutput['jointList']
    ctrls = tailOutput['ctrls']
    nurb = tailOutput['nurb']

    # Create main Ctrls
    stposCtrl = controlTools.create(prefix + 'tail_stMainPos_ctrl', shape='C02_pole', color='lemon', scale=1, snapTo=ctrls[0], jointCtrl=True, tag='splineTemp')
    edposCtrl = controlTools.create(prefix + 'tail_edMainPos_ctrl', shape='C02_pole', color='lemon', scale=1, snapTo=ctrls[-1], jointCtrl=True, tag='splineTemp')
    mc.setAttr(stposCtrl[-1] + '.drawStyle', 0)
    mc.setAttr(edposCtrl[-1] + '.drawStyle', 0)

    stctrl = controlTools.create(prefix + 'tail_stMain_ctrl', shape='C00_sphere', color='lemon', scale=1, snapTo=ctrls[0], jointCtrl=False)
    edctrl = controlTools.create(prefix + 'tail_edMain_ctrl', shape='C00_sphere', color='lemon', scale=1, snapTo=ctrls[-1], jointCtrl=False)
    mc.parentConstraint(stposCtrl[-1], stctrl[0])
    mc.parentConstraint(edposCtrl[-1], edctrl[0])

    mc.parent(stposCtrl[0], topnode + 'Ctrls')
    mc.parent(edposCtrl[0], topnode + 'Ctrls')
    mc.parent(stctrl[0], topnode + 'Ctrls')
    mc.parent(edctrl[0], topnode + 'Ctrls')

    # create aim loc use to control main nurb
    stMainAimLoc = aboutPublic.snapLoc(stposCtrl[-1], name=stposCtrl[-1].replace('_ctrl', '') + '_aim_loc')
    edMainAimLoc = aboutPublic.snapLoc(edposCtrl[-1], name=edposCtrl[-1].replace('_ctrl', '') + '_aim_loc')
    aboutPublic.snapAtoB(stMainAimLoc, stposCtrl[-1])
    aboutPublic.snapAtoB(edMainAimLoc, edposCtrl[-1])
    mc.parent(stMainAimLoc, stposCtrl[-1])
    mc.parent(edMainAimLoc, edposCtrl[-1])

    stMainUpLoc = mc.duplicate(stMainAimLoc, n=stposCtrl[-1].replace('_ctrl', '') + '_upAxis_loc')[0]
    edMainUpLoc = mc.duplicate(edMainAimLoc, n=edposCtrl[-1].replace('_ctrl', '') + '_upAxis_loc')[0]
    mc.setAttr(stMainUpLoc + '.tz', 0.1)
    mc.setAttr(edMainUpLoc + '.tz', 0.1)
    mc.aimConstraint(stposCtrl[-1], edMainAimLoc, n=edMainAimLoc + '_ac', aim=[0, -1, 0], u=[1, 0, 0], wu=[0, 0, 1],
                     wut='objectRotation', wuo=edMainUpLoc)
    mc.aimConstraint(edposCtrl[-1], stMainAimLoc, n=stMainAimLoc + '_ac', aim=[0, -1, 0], u=[1, 0, 0], wu=[0, 0, 1],
                     wut='objectRotation', wuo=stMainUpLoc)

    # Create main nurb
    # main nurb usefor rigging / do not delete
    mainNurb = mc.duplicate(nurb, n=nurb.replace('output_org', 'mainPos_org'), rc=True)[0]
    # deleteChild = mc.listRelatives(mainNurb)[1:]
    # mc.delete(deleteChild)

    mel.eval('rebuildSurface -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kc 0 -su 1 -du 1 -sv 0 -dv 1 -tol 0.01 -fr 0  -dir 2 "{0}";'.format(mainNurb))
    cluster.create(['{0}.cv[0][0:2]'.format(mainNurb), stMainAimLoc])
    cluster.create(['{0}.cv[1][0:2]'.format(mainNurb), edMainAimLoc])

    # Rivet pos ctrls
    posCtrlGrp = []
    for posctrl in ctrls:
        posCtrlGrp.append(posctrl + '_grp')
    rivet.surface(posCtrlGrp, mainNurb, topnode + 'Nox')
    aboutLock.unlock([ctrls[0], ctrls[-1]], 'v')
    mc.setAttr(ctrls[0] + '.visibility', 0)
    mc.setAttr(ctrls[-1] + '.visibility', 0)

    # Create FkCtrls Ctrls
    if numFkCtrls > 0:
        div = mc.xform(ctrls[-1], q=1, ws=1, t=1)[1] / (numFkCtrls - 1)
        for i in range(numFkCtrls):
            ltr = aboutName.letter(i)
            ctrlName = '{0}tail_fk{1}_ctrl'.format(prefix, ltr)
            secctrlName = '{0}tail_fk{1}_sec_ctrl'.format(prefix, ltr)

            fkctrl = controlTools.create(ctrlName, shape='D07_circle', color='cyan', scale=1.5, jointCtrl=False)
            fksecctrl = controlTools.create(secctrlName, shape='E01_doctor', color='sand', scale=1, jointCtrl=False)

            mc.setAttr(fkctrl[0] + '.ty', div * i)
            mc.setAttr(fksecctrl[0] + '.ty', div * i)

            mc.parent(fkctrl[0], topnode + 'Ctrls')
            mc.parent(fksecctrl[0], topnode + 'Ctrls')

            rivet.surface(fkctrl[0], nurb, topnode + 'Nox')
            rivet.surface(fksecctrl[0], nurb, topnode + 'Nox')

            aboutLock.lock(fkctrl)
            aboutLock.unlock(fkctrl[-1], 't r s')

    # Create IkCtrls Ctrls
    if numIkCtrls:
        div = mc.xform(ctrls[-1], q=1, ws=1, t=1)[1] / (numIkCtrls - 1)
        for i in range(numIkCtrls):
            ltr = aboutName.letter(i)
            ikctrl = controlTools.create(prefix + 'tail_' + 'ik' + ltr + '_ctrl', shape='jackThin', color='sand', scale=0.7, jointCtrl=False)
            mc.setAttr(ikctrl[0] + '.ty', div * i)
            mc.parent(ikctrl[0], topnode + 'Ctrls')
            rivet.surface(ikctrl[0], nurb, topnode + 'Nox')
            aboutLock.lock(ikctrl)
            aboutLock.unlock(ikctrl[-1], 't r s')

    # Create fk tip Jnts
    if numTipJoints:
        numTipJoints += 1
        tipJoints = joints[-numTipJoints:]
        order = 0

        for i in range(0, len(tipJoints) - 1, 2):
            ltr = aboutName.letter(order)
            ctrl = controlTools.create(prefix + 'tail_' + 'TipFk' + ltr + '_ctrl', shape='star', color='cyan', scale=.5, jointCtrl=False)
            controlTools.rollCtrlShape(ctrl[-1], axis='x', value=-90)
            mc.delete( mc.parentConstraint(tipJoints[i], tipJoints[i + 1], ctrl[0]) )
            mc.parentConstraint(tipJoints[i], ctrl[0], n=ctrl[0] + '_prc', mo=True)
            mc.parent(ctrl[0], topnode + 'Ctrls')
            aboutLock.lock(ctrl)
            aboutLock.unlock(ctrl[-1], 't r s')
            order += 1

    # Clean
    hidelocs = [stMainAimLoc, edMainAimLoc, stMainUpLoc, edMainUpLoc]
    for loc in hidelocs:
        mc.hide(loc)

    aboutLock.unlock(topnode + 'Ctrls')
    mc.setAttr(topnode + 'Ctrls.rx', -90)
    aboutLock.lock(topnode + 'Ctrls')

    # Find parent
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))
    return


# Build Anim
def anim():
    parts = templateTools.getParts('tail')
    for part in parts:

        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        numFkCtrls = templateTools.getArgs(part, 'numFkCtrls')
        numIkCtrls = templateTools.getArgs(part, 'numIkCtrls')
        numJoints = templateTools.getArgs(part, 'numJoints')
        numTipJoints = templateTools.getArgs(part, 'numTipJoints')
        wave = templateTools.getArgs(part, 'wave')
        roll = templateTools.getArgs(part, 'roll')
        dynamic = templateTools.getArgs(part, 'dynamic')

        # set mirror and color
        color = 'blue'
        mirror = 1
        if side == 'rt':
            mirror = -1
            color = 'red'

        # jnts in list
        joints = []
        for i in range(numJoints):
            a = aboutName.letter(i)
            joints.append(prefix + 'tail' + a + '_drv')

        temp_output_nurb = mc.rename(prefix + 'tail_nurb_output_orgPrep', prefix + 'tail_temp_output_nurb')
        main_nurb = mc.rename(prefix + 'tail_nurb_mainPos_orgPrep', prefix + 'tail_main_nurb')
        noTrans = mc.createNode('transform', p='noTransform', n=prefix + 'tail_noTrans')

        # build Fk Ctrls
        fkCtrls = []
        fkSecCtrls = []
        fkBridges = []
        fk_nurb = mc.duplicate(temp_output_nurb, n=prefix + 'tail_fk_nurb')[0]

        for i in range(numFkCtrls):

            a = aboutName.letter(i)
            PrepShape = '{0}tail_fk{1}_ctrlPrep'.format(prefix, a)
            secPrepShape = '{0}tail_fk{1}_sec_ctrlPrep'.format(prefix, a)

            ctrlName = '{0}tail_fk{1}_ctrl'.format(prefix, a)
            secCtrlName = '{0}tail_fk{1}_sec_ctrl'.format(prefix, a)

            ctrl = controlTools.create(ctrlName, snapTo=PrepShape, useShape=PrepShape)
            secCtrl = controlTools.create(secCtrlName, snapTo=secPrepShape, useShape=secPrepShape)

            controlTools.tagKeyable(ctrl[2:], 't r')
            controlTools.tagKeyable(secCtrl[2:], 't r')

            fkCtrls.append(ctrl[-1])
            fkSecCtrls.append(secCtrl[-1])

            # connect bridge
            bridge = mc.spaceLocator(p=(0, 0, 0), n=ctrlName.replace('_ctrl', '_connect_loc'))[0]
            bridgeGrp = aboutPublic.createParentGrp(bridge, 'grp')
            aboutPublic.snapAtoB(bridgeGrp, ctrl)
            fkBridges.append(bridge)

            mc.parent(secCtrl[0], ctrl[-1])

            # do connect
            keyAttr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']
            for attr in keyAttr:
                mc.connectAttr(bridge + attr, ctrl[1] + attr)

            mc.hide(bridge)

        for i in range(len(fkCtrls)):
            if i != 0:
                mc.parent(fkCtrls[i] + '_grp', fkCtrls[i - 1])

        for i in range(len(fkBridges)):
            if i != 0:
                mc.parent(fkBridges[i] + '_grp', fkBridges[i - 1])

        # build Ik Ctrls
        ikCtrls = []
        ikBridges = []
        ik_nurb = ''

        if numIkCtrls:
            ik_nurb = mc.duplicate(temp_output_nurb, n=prefix + 'tail_ik_nurb')[0]
            mel.eval('rebuildSurface -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kc 0 -su {0} -du 3 -sv 1 -dv 3 -tol 0.01 -fr 0  -dir 2 "{1}";'
                     .format(numIkCtrls - 1, ik_nurb))

            for i in range(numIkCtrls):

                # ctrl
                a = aboutName.letter(i)
                PrepShape = '{0}tail_ik{1}_ctrlPrep'.format(prefix, a)
                ctrlName = '{0}tail_ik{1}_ctrl'.format(prefix, a)
                loc = aboutPublic.snapLoc(PrepShape)
                aboutPublic.snapAtoB(PrepShape, loc)

                ctrl = controlTools.create(ctrlName, snapTo=loc, useShape=PrepShape)
                ikCtrls.append(ctrl[-1])

                # connect bridge
                bridge = mc.spaceLocator(p=(0, 0, 0), n=ctrlName.replace('_ctrl', '_connect_loc'))[0]
                bridgeGrp = aboutPublic.createParentGrp(bridge, 'grp')
                aboutPublic.snapAtoB(bridgeGrp, ctrl)
                ikBridges.append(bridge)

                # do connect
                keyAttr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']
                for attr in keyAttr:
                    mc.connectAttr(bridge + attr, ctrl[1] + attr)

                mc.hide(bridge)
                mc.delete(loc)

        # build Main Ctrls
        stMainPrep = prefix + 'tail_stMain_ctrlPrep'
        edMainPrep = prefix + 'tail_edMain_ctrlPrep'
        stMainCtrl = controlTools.create(prefix + 'tail_stMain_ctrl', snapTo=stMainPrep, useShape=stMainPrep, scale=1.8)
        edMainCtrl = controlTools.create(prefix + 'tail_edMain_ctrl', snapTo=edMainPrep, useShape=edMainPrep, scale=1.8)

        # >> add cmd attributes
        mc.addAttr(stMainCtrl[-1], ln='fk_vis', at='double', min=0, max=1, dv=0, k=1)
        if numIkCtrls:
            mc.addAttr(stMainCtrl[-1], ln='ik_vis', at='double', min=0, max=1, dv=1, k=1)
        if numTipJoints:
            mc.addAttr(stMainCtrl[-1], ln='tip_vis', at='double', min=0, max=1, dv=0, k=1)
        mc.addAttr(stMainCtrl[-1], ln='stretch', at='double', min=0, max=1, dv=1, k=1)

        # create aim loc use to control main nurb
        stMainAimLoc = aboutPublic.snapLoc(stMainCtrl[-1], name=stMainCtrl[-1].replace('_ctrl', '') + '_aim_loc')
        edMainAimLoc = aboutPublic.snapLoc(edMainCtrl[-1], name=edMainCtrl[-1].replace('_ctrl', '') + '_aim_loc')
        aboutPublic.snapAtoB(stMainAimLoc, stMainCtrl[-1])
        aboutPublic.snapAtoB(edMainAimLoc, edMainCtrl[-1])
        mc.parent(stMainAimLoc, stMainCtrl[-1])
        mc.parent(edMainAimLoc, edMainCtrl[-1])

        stMainUpLoc = mc.duplicate(stMainAimLoc, n=stMainCtrl[-1].replace('_ctrl', '') + '_upAxis_loc')[0]
        edMainUpLoc = mc.duplicate(edMainAimLoc, n=edMainCtrl[-1].replace('_ctrl', '') + '_upAxis_loc')[0]
        mc.setAttr(stMainUpLoc + '.tz', 0.1)
        mc.setAttr(edMainUpLoc + '.tz', 0.1)
        mc.aimConstraint(stMainCtrl[-1], edMainAimLoc, n=edMainAimLoc + '_ac', aim=[0, -1, 0], u=[1, 0, 0], wu=[0, 0, 1],
                         wut='objectRotation', wuo=edMainUpLoc)
        mc.aimConstraint(edMainCtrl[-1], stMainAimLoc, n=stMainAimLoc + '_ac', aim=[0, -1, 0], u=[1, 0, 0], wu=[0, 0, 1],
                         wut='objectRotation', wuo=stMainUpLoc)

        cluster.create(['{0}.cv[0][0:2]'.format(main_nurb), stMainAimLoc])
        cluster.create(['{0}.cv[1][0:2]'.format(main_nurb), edMainAimLoc])

        mc.parent(edMainCtrl[0], stMainCtrl[-1])

        # Stretch ----------------------------------
        # stretchInfo['nurbs'][0] output
        # stretchInfo['nurbs'][1] input
        # Control & nurb &joints ---------------- connect ------------------

        if numIkCtrls:
            # main control set
            rivet.surface(ikBridges, main_nurb, noTrans)

            # create ik nurb stretcb
            stretchInfo = nurbSpline.createOffsetStretch(ik_nurb, uv='v')

            input_nurb = stretchInfo['nurbs'][1]
            output_nurb = stretchInfo['nurbs'][0]

            # ik connect nurb
            ikCtrlsTemp = []
            for ctrl in ikCtrls:
                ikCtrlsTemp.append(ctrl)
            ikCtrlsTemp.insert(0, ikCtrls[0])
            ikCtrlsTemp.append(ikCtrls[-1])

            # ik control ik input nurb
            for i in range(len(ikCtrlsTemp)):
                cluster.create(['{0}.cv[{1}][0:3]'.format(input_nurb, i), ikCtrlsTemp[i]])

            # fk rivet on ik output nurb
            rivet.surface(fkBridges, output_nurb, noTrans)

            # fk control temp nurb
            fkCtrlsTemp = []
            for ctrl in fkSecCtrls:
                fkCtrlsTemp.append(ctrl)
            fkCtrlsTemp.insert(0, fkCtrls[0])
            fkCtrlsTemp.append(fkCtrls[-1])

            for i in range(len(fkCtrlsTemp)):
                cluster.create(['{0}.cv[{1}][0:4]'.format(temp_output_nurb, i), fkCtrlsTemp[i]])

        else:
            # main control set
            rivet.surface(fkBridges, main_nurb, noTrans)

            # create fk nurb stretch
            stretchInfo = nurbSpline.createOffsetStretch(fk_nurb, uv='v')
            mc.setAttr(stretchInfo['rbcs'][0] + '.spans', numFkCtrls - 1)
            mc.setAttr(stretchInfo['rbcs'][1] + '.spans', numFkCtrls - 1)

            input_nurb = stretchInfo['nurbs'][1]
            output_nurb = stretchInfo['nurbs'][0]

            # fk control temp nurb
            fkCtrlsTemp = []
            for ctrl in fkCtrls:
                fkCtrlsTemp.append(ctrl)
            fkCtrlsTemp.insert(0, fkCtrls[0])
            fkCtrlsTemp.append(fkCtrls[-1])

            for i in range(len(fkCtrlsTemp)):
                cluster.create(['{0}.cv[{1}][0:4]'.format(input_nurb, i), fkCtrlsTemp[i]])

            # fk output nurb control temp nurb
            outputShape = mc.listRelatives(output_nurb, s=1)[0]
            tempShape = mc.listRelatives(temp_output_nurb, s=1)[0]
            mc.connectAttr(outputShape + '.worldSpace[0]', tempShape + '.create')

        # connect stretch bridge
        stretchCmd = stretchInfo['cmd']
        mc.connectAttr(stMainCtrl[-1] + '.stretch', stretchCmd + '.stretch')


        # Tip joints rig ----------------------------------------------------------------------
        # Create fk tip Jnts
        tipJoints = []
        tipCtrls = []
        tiplocs = []

        if numTipJoints:
            numTipJoints += 1
            tipJoints = joints [-numTipJoints:]
            for j in tipJoints:
                joints.remove(j)

        rivet.surface(joints, temp_output_nurb, noTrans)

        if numTipJoints:
            # Create fk ctrls
            order=0

            for i in range(1, len(tipJoints), 2):

                # tip jnt control
                ltr = aboutName.letter(order)
                jnt = tipJoints[i-1]
                name = prefix+'tail_'+'TipFk'+ltr+'_ctrl'
                Prep = name+'Prep'
                ctrl = controlTools.create(name, snapTo=jnt, useShape=Prep)
                controlTools.tagKeyable(ctrl[-1], 'r')
                mc.parent(ctrl[-1], ctrl[0])
                mc.delete(ctrl[1])

                if i>1:
                    mc.parent(ctrl[0], tipCtrls[-1])
                tipCtrls.append(ctrl[-1])

                # next jnt control
                jnt = tipJoints[i]
                name = prefix+'tail_'+'TipFk'+ltr+'_next_ctrl'
                ctrl = controlTools.create(name, snapTo=jnt, useShape=name+'Prep')

                mc.delete(ctrl[-1]+'Shape')
                mc.parent(ctrl[-1], ctrl[0])
                mc.delete(ctrl[1])
                mc.connectAttr(tipCtrls[-1]+'.r', ctrl[-1]+'.r')

                mc.parent(ctrl[0], tipCtrls[-1])
                tipCtrls.append(ctrl[-1])

                order += 1


            # end control
            jnt = tipJoints[-1]
            name = prefix+'tail_'+'FkEnd_ctrl'
            ctrl = controlTools.create(name, snapTo=jnt, useShape=name+'Prep')
            mc.setAttr(ctrl[-1]+'.ro', 1)
            mc.delete(mc.parentConstraint(jnt, ctrl[0]))

            mc.parent(ctrl[-1], ctrl[0])
            mc.delete(ctrl[1])
            mc.delete(ctrl[-1]+'Shape')

            mc.parent(ctrl[0], tipCtrls[-1])
            mc.connectAttr(tipCtrls[-1]+'.t', ctrl[-1]+'.t')

            tipCtrls.append(ctrl[-1])

            # rivet nurb
            for i in range(len(tipCtrls)):
                ctrl = tipCtrls[i]
                loc = mc.spaceLocator(p=(0,0,0), n=ctrl.replace('_ctrl','loc'))[0]
                mc.hide(loc)
                aboutPublic.snapAtoB(loc, ctrl+'_grp')
                if tiplocs:
                    mc.parent(loc, tiplocs[-1])
                tiplocs.append(loc)

                rivet.surface(loc, temp_output_nurb, noTrans)
                mc.connectAttr(loc + '.t', ctrl+'_grp.t')
                mc.connectAttr(loc + '.r', ctrl+'_grp.r')

            for i in range(len(tipJoints)):
                mc.parentConstraint(tipCtrls[i], tipJoints[i], n=tipJoints[i]+'_prc', mo=True)

        # Connect with torso ---------------------------------------------------------------------------------------
        connectInLoc = parent + '_connect_loc'
        if mc.objExists(connectInLoc):
            mc.parentConstraint(connectInLoc, stMainCtrl[0], n=stMainCtrl[0] + '_prc', mo=1)

        # Clean
        # ---------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'tail_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
        mc.parent(mpNode, 'controls')

        # need parent
        needParent = [fkCtrls[0] + '_grp', fkBridges[0] + '_grp', stMainCtrl[0], joints[0]]
        if numIkCtrls:
            for ikctrl in ikCtrls:
                needParent.append(ikctrl + '_grp')
            for bridge in ikBridges:
                needParent.append(bridge + '_grp')

        if numTipJoints:
            needParent.append(tipCtrls[0]+'_grp')
            needParent.append(tiplocs[0])

        for need in needParent:
            if mc.objExists(need):
                mc.parent(need, mpNode)

        # noTrans Parent
        mc.hide(noTrans)
        noTransNeedP = [input_nurb, output_nurb, temp_output_nurb, main_nurb]

        for need in noTransNeedP:
            if mc.objExists(need):
                mc.parent(need, noTrans)

        # hide
        needHList = [stMainAimLoc, edMainAimLoc, stMainUpLoc, edMainUpLoc]
        for need in needHList:
            mc.hide(need)

        # vis
        mc.connectAttr(stMainCtrl[-1] + '.fk_vis', fkCtrls[0] + '_grp' + '.v')
        if numIkCtrls:
            for ikctrl in ikCtrls:
                mc.connectAttr(stMainCtrl[-1] + '.ik_vis', ikctrl + '_grp' + '.v')
        if numTipJoints:
            mc.connectAttr(stMainCtrl[-1] + '.tip_vis', tipCtrls[0] + '_grp' + '.v')

        # Tag
        spaceTools.tag(stMainCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(connectInLoc), oo=True, con=stMainCtrl[2], dv=0)
        spaceTools.tag(edMainCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(stMainCtrl[-1]), dv=0)