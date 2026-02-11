import maya.cmds as mc

from rxCore import aboutName
from rxCore import aboutLock
from rxCore import aboutPublic

import controlTools
import pointOnCrv
import crvSpline
import rivet
import templateTools
import cluster

def template(prefix, topnode, jnts):

    # create snap object
    l0 = mc.createNode('transform')
    l1 = mc.createNode('transform')
    l2 = mc.createNode('transform')
    l3 = mc.createNode('transform')
    l4 = mc.createNode('transform')
    l5 = mc.createNode('transform')
    l6 = mc.createNode('transform')

    mc.pointConstraint(jnts[0], l0)
    mc.pointConstraint(jnts[0:2], l1)
    mc.pointConstraint(jnts[1], l2)
    mc.pointConstraint(jnts[-3:-1], l3)
    mc.pointConstraint(jnts[-2], l4)
    mc.pointConstraint(jnts[-2:], l5)
    mc.pointConstraint(jnts[-1], l6)

    mc.orientConstraint(jnts[0], l0)
    mc.orientConstraint(jnts[0], l1)
    mc.orientConstraint(jnts[1], l2)
    mc.orientConstraint(jnts[1], l3)
    mc.orientConstraint(jnts[2], l4)
    mc.orientConstraint(jnts[2], l5)
    mc.orientConstraint(jnts[-1], l6)

    # create ctrl
    ctrls = []
    nodes = [l0,l1,l2,l3,l4,l5,l6]
    for i in range(len(nodes)):
        if mc.objExists(nodes[i]):
            ctrls.append( controlTools.create(prefix+'Bendy'+aboutName.letter(i)+'_ctrl', 
                                              snapTo=nodes[i], 
                                              shape='D07_circle',
                                              color='peach', 
                                              scale=[1.5,1.5,1.5]) [-1] )

    for ctrl in ctrls:
        controlTools.rollCtrlShape(ctrl, axis='z',value=90)

    # A
    mc.pointConstraint(jnts[0], ctrls[0]+'_grp')
    mc.orientConstraint(jnts[0], ctrls[0]+'_grp')
    mc.hide(ctrls[0]+'_grp')

    # B
    mc.pointConstraint(jnts[0:2], ctrls[1]+'_grp')
    mc.orientConstraint(jnts[0], ctrls[1]+'_grp')

    # C
    if len(jnts) == 5:
        # jnts = [upleg, midlegA, midlegB, loleg, legEnd]
        mc.pointConstraint(jnts[1], jnts[2], ctrls[2] + '_grp')
        oc = mc.orientConstraint(jnts[1], ctrls[2] + '_grp')[0]
    else:
        mc.pointConstraint(jnts[1], ctrls[2] + '_grp')
        oc = mc.orientConstraint(jnts[1], ctrls[2] + '_grp')[0]

    mc.setAttr(oc + '.interpType', 2)
    mc.hide(ctrls[2] + '_grp')

    # D
    mc.pointConstraint(jnts[-3:-1], ctrls[3]+'_grp')
    mc.orientConstraint(jnts[-3], ctrls[3]+'_grp')

    # E
    mc.pointConstraint(jnts[-2], ctrls[4]+'_grp')
    mc.orientConstraint(jnts[-2], ctrls[4]+'_grp')
    mc.hide(ctrls[4] + '_grp')

    # F
    mc.pointConstraint(jnts[-2:], ctrls[5]+'_grp')
    mc.orientConstraint(jnts[-2], ctrls[5]+'_grp')

    # G
    mc.pointConstraint(jnts[-1], ctrls[6]+'_grp')
    mc.orientConstraint(jnts[-1], ctrls[6]+'_grp')
    mc.hide(ctrls[6] + '_grp')


    for c in ctrls:
        if 'rt_' in prefix:
            mc.xform(c+'_grp', r=1, s=[-1,-1,-1])
        mc.parent(c+'_grp', topnode+'Ctrls')
        aboutLock.lock([c+'_grp', c+'_con', c+'_sdk', c])
        aboutLock.unlock(c, 's')

    # create joints
    # jnts
    numJoints = 5
    bendyUpJnts = []
    bendyMdJnts = []
    bendyLoJnts = []
    bendyUpJntsGrp = []
    bendyMdJntsGrp = []
    bendyLoJntsGrp = []

    for i in range(numJoints):
        upjnt = templateTools.createJoint(prefix + '_ub' + aboutName.letter(i), topnode, color='yellow', pc=1, oc=1)
        mdjnt = templateTools.createJoint(prefix + '_mb' + aboutName.letter(i), topnode, color='yellow', pc=1, oc=1)
        lojnt = templateTools.createJoint(prefix + '_lb' + aboutName.letter(i), topnode, color='yellow', pc=1, oc=1)

        mc.hide(upjnt[-2])
        mc.hide(mdjnt[-2])
        mc.hide(lojnt[-2])

        mc.setAttr(upjnt[-1] + '.radius', 0.5)
        mc.setAttr(mdjnt[-1] + '.radius', 0.5)
        mc.setAttr(lojnt[-1] + '.radius', 0.5)

        bendyUpJnts.append(upjnt[-1])
        bendyMdJnts.append(mdjnt[-1])
        bendyLoJnts.append(lojnt[-1])

        bendyUpJntsGrp.append(upjnt[0])
        bendyMdJntsGrp.append(mdjnt[0])
        bendyLoJntsGrp.append(lojnt[0])

    # set position
    upStartPoint = mc.xform(jnts[0], q=1, t=1, ws=1)
    upEndPoint = mc.xform(jnts[1], q=1, t=1, ws=1)
    mdStartPoint = mc.xform(jnts[-3], q=1, t=1, ws=1)
    mdEndPoint = mc.xform(jnts[-2], q=1, t=1, ws=1)
    loStartPoint = mc.xform(jnts[-2], q=1, t=1, ws=1)
    loEndPoint = mc.xform(jnts[-1], q=1, t=1, ws=1)

    upCrv = mc.curve(n=prefix + '_ub_temp_crv', p=[upStartPoint, upEndPoint], d=1, k=(0, 1))
    mdCrv = mc.curve(n=prefix + '_md_temp_crv', p=[mdStartPoint, mdEndPoint], d=1, k=(0, 1))
    loCrv = mc.curve(n=prefix + '_lb_temp_crv', p=[loStartPoint, loEndPoint], d=1, k=(0, 1))
    cluster.create([upCrv + '.cv[0]', jnts[0] + '_pos'])
    cluster.create([upCrv + '.cv[1]', jnts[1] + '_pos'])
    cluster.create([mdCrv + '.cv[0]', jnts[-3] + '_pos'])
    cluster.create([mdCrv + '.cv[1]', jnts[-2] + '_pos'])
    cluster.create([loCrv + '.cv[0]', jnts[-2] + '_pos'])
    cluster.create([loCrv + '.cv[1]', jnts[-1] + '_pos'])

    upPoslist = pointOnCrv.posListOnCrv(upCrv, numJoints - 1, ev=0, start=0, end=1)
    mdPoslist = pointOnCrv.posListOnCrv(mdCrv, numJoints - 1, ev=0, start=0, end=1)
    loPoslist = pointOnCrv.posListOnCrv(loCrv, numJoints - 1, ev=0, start=0, end=1)

    for i in range(numJoints):
        if i != numJoints - 1:
            mc.parent(bendyUpJnts[i + 1], bendyUpJnts[i])
            mc.parent(bendyMdJnts[i + 1], bendyMdJnts[i])
            mc.parent(bendyLoJnts[i + 1], bendyLoJnts[i])

        mc.xform(bendyUpJntsGrp[i], t=upPoslist[i], ws=1)
        mc.xform(bendyMdJntsGrp[i], t=mdPoslist[i], ws=1)
        mc.xform(bendyLoJntsGrp[i], t=loPoslist[i], ws=1)
        mc.orientConstraint(jnts[0], bendyUpJntsGrp[i])
        mc.orientConstraint(jnts[-3], bendyMdJntsGrp[i])
        mc.orientConstraint(jnts[-2], bendyLoJntsGrp[i])

    rivet.curve(bendyUpJntsGrp, upCrv, con=True, mo=True, wuo=None, mpnode=topnode + 'Nox')
    rivet.curve(bendyMdJntsGrp, mdCrv, con=True, mo=True, wuo=None, mpnode=topnode + 'Nox')
    rivet.curve(bendyLoJntsGrp, loCrv, con=True, mo=True, wuo=None, mpnode=topnode + 'Nox')

    # clean
    mc.parent(bendyUpJntsGrp, bendyMdJntsGrp, bendyLoJntsGrp, topnode + 'Nox')
    mc.parent(upCrv, mdCrv, loCrv, topnode + 'Nox')
    mc.hide(upCrv)
    mc.hide(mdCrv)
    mc.hide(loCrv)
    mc.delete(nodes)


def anim(prefix, jnts, twistBridges, volume=True):

    # create ctrls
    ctrls = [controlTools.create(prefix + 'BendyA_ctrl', snapTo=prefix + 'BendyA_ctrlPrep', useShape=prefix + 'BendyA_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyB_ctrl', snapTo=prefix + 'BendyB_ctrlPrep', useShape=prefix + 'BendyB_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyC_ctrl', snapTo=prefix + 'BendyC_ctrlPrep', useShape=prefix + 'BendyC_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyD_ctrl', snapTo=prefix + 'BendyD_ctrlPrep', useShape=prefix + 'BendyD_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyE_ctrl', snapTo=prefix + 'BendyE_ctrlPrep', useShape=prefix + 'BendyE_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyF_ctrl', snapTo=prefix + 'BendyF_ctrlPrep', useShape=prefix + 'BendyF_ctrlPrep')[-1],
             controlTools.create(prefix + 'BendyG_ctrl', snapTo=prefix + 'BendyG_ctrlPrep', useShape=prefix + 'BendyG_ctrlPrep')[-1]]

    mirror = 1
    if 'rt_' in prefix:
        mirror = -1

        mc.xform(ctrls[0]+'_grp', r=1, s=[-1,-1,-1])
        mc.xform(ctrls[1]+'_grp', r=1, s=[-1,-1,-1])
        mc.xform(ctrls[2]+'_grp', r=1, s=[-1,-1,-1])
        mc.xform(ctrls[3]+'_grp', r=1, s=[-1,-1,-1])
        mc.xform(ctrls[4]+'_grp', r=1, s=[-1,-1,-1])

        mc.delete(mc.orientConstraint(prefix+'BendyA_ctrlPrep', ctrls[0]+'_grp'))
        mc.delete(mc.orientConstraint(prefix+'BendyB_ctrlPrep', ctrls[1]+'_grp'))
        mc.delete(mc.orientConstraint(prefix+'BendyC_ctrlPrep', ctrls[2]+'_grp'))
        mc.delete(mc.orientConstraint(prefix+'BendyD_ctrlPrep', ctrls[2]+'_grp'))
        mc.delete(mc.orientConstraint(prefix+'BendyE_ctrlPrep', ctrls[2]+'_grp'))

    # ctrl pos
    #------------------------------------------------------------------------------------------------------------------------------------------
    # A
    mc.parentConstraint(jnts[0], ctrls[0]+'_grp')
    mc.hide(ctrls[0]+'_grp')

    # B
    mc.delete( mc.pointConstraint(jnts[0:2], ctrls[1]+'_grp') )
    mc.delete( mc.orientConstraint(jnts[0], ctrls[1]+'_grp') )

    # C
    if len(jnts) == 5:
        # jnts = [upleg, midlegA, midlegB, loleg, legEnd]
        mc.pointConstraint(jnts[1], jnts[2], ctrls[2] + '_grp')
        coc = mc.orientConstraint(jnts[1], ctrls[2] + '_grp')[0]
    else:
        mc.pointConstraint(jnts[1], ctrls[2] + '_grp')
        coc = mc.orientConstraint(jnts[1], ctrls[2] + '_grp')[0]
    mc.setAttr(coc + '.interpType', 2)

    upMidloc = aboutPublic.snapLoc(jnts[1], name=prefix + '_upMid_loc')
    loMidloc = aboutPublic.snapLoc(jnts[-3], name=prefix + '_loMid_loc')
    mc.hide(upMidloc)
    mc.hide(loMidloc)

    mc.parent(upMidloc, ctrls[2])
    mc.parent(loMidloc, ctrls[2])

    keyAttrs = ['.rx', '.ry', '.rz']
    for key in keyAttrs:
        mc.setAttr(upMidloc + key, 0)
        mc.setAttr(loMidloc + key, 0)

    # D
    mc.delete( mc.pointConstraint(jnts[-3:-1], ctrls[3]+'_grp') )
    mc.delete( mc.orientConstraint(jnts[-3], ctrls[3]+'_grp') )

    # E
    mc.pointConstraint(jnts[-2], ctrls[4] + '_grp')
    eoc = mc.orientConstraint(jnts[-2], ctrls[4] + '_grp')[0]
    mc.setAttr(eoc + '.interpType', 2)

    # F
    mc.delete( mc.pointConstraint(jnts[-2:], ctrls[5]+'_grp') )
    mc.delete( mc.orientConstraint(jnts[-2], ctrls[5]+'_grp') )

    # G
    mc.parentConstraint(jnts[-1], ctrls[6]+'_grp')
    mc.hide(ctrls[6]+'_grp')


    # dyn
    mc.pointConstraint(ctrls[0], upMidloc, ctrls[1]+'_grp')
    mc.pointConstraint(loMidloc, ctrls[4], ctrls[3]+'_grp')
    mc.pointConstraint(ctrls[4], ctrls[6], ctrls[5]+'_grp')

    mc.aimConstraint(upMidloc, ctrls[1]+'_grp', n=ctrls[1]+'_grp_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='objectRotation', wuo=ctrls[0])
    mc.aimConstraint(ctrls[4], ctrls[3]+'_grp', n=ctrls[3]+'_grp_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='objectRotation', wuo=loMidloc)
    mc.aimConstraint(ctrls[6], ctrls[5]+'_grp', n=ctrls[5]+'_grp_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='objectRotation', wuo=ctrls[4])

    
    # create elbow smooth 
    smoothA_info = smoothJointLink(prefix, ctrls[1], ctrls[2], ctrls[3])
    smoothB_info = smoothJointLink(prefix, ctrls[3], ctrls[4], ctrls[5])
    #------------------------------------------------------------------------------------------------------------------------------------------

    # create crv
    stAPos = mc.xform(jnts[0], q=1, t=1, ws=1 )
    edAPos = mc.xform(jnts[1], q=1, t=1, ws=1 )
    crvA = mc.curve( p=[(stAPos), (edAPos)], d=1, n=prefix+'BendyA_crv' )
    mc.rename( (mc.listRelatives(crvA, s=True)[0]), prefix+'BendyA_crv_shape')

    stBPos = mc.xform(jnts[-3], q=1, t=1, ws=1 )
    edBPos = mc.xform(jnts[-2], q=1, t=1, ws=1 )
    crvB = mc.curve( p=[(stBPos), (edBPos)], d=1, n=prefix+'BendyB_crv' )
    mc.rename( (mc.listRelatives(crvB, s=True)[0]), prefix+'BendyB_crv_shape')

    stCPos = mc.xform(jnts[-2], q=1, t=1, ws=1 )
    edCPos = mc.xform(jnts[-1], q=1, t=1, ws=1 )
    crvC = mc.curve( p=[(stCPos), (edCPos)], d=1, n=prefix+'BendyC_crv' )
    mc.rename( (mc.listRelatives(crvC, s=True)[0]), prefix+'BendyC_crv_shape')

    # rebuild crv
    mc.rebuildCurve(crvA, ch=1, rpo=1, rt=0, end=1, s=4, d=3, tol=0.01 )
    mc.rebuildCurve(crvB, ch=1, rpo=1, rt=0, end=1, s=4, d=3, tol=0.01 )
    mc.rebuildCurve(crvC, ch=1, rpo=1, rt=0, end=1, s=4, d=3, tol=0.01)
    crvA_cvs = mc.ls(crvA + '.cv[:]', fl=1)
    crvB_cvs = mc.ls(crvB + '.cv[:]', fl=1)
    crvC_cvs = mc.ls(crvC + '.cv[:]', fl=1)

    # delete two cvs
    needDeleteCv = [ crvA_cvs[1], crvA_cvs[-2], crvB_cvs[1], crvB_cvs[-2], crvC_cvs[1], crvC_cvs[-2]]
    mc.delete(needDeleteCv)
    mc.rebuildCurve(crvA, ch=1, rpo=1, rt=0, kcp=1, end=1, kr=0)
    mc.rebuildCurve(crvB, ch=1, rpo=1, rt=0, kcp=1, end=1, kr=0)
    mc.rebuildCurve(crvC, ch=1, rpo=1, rt=0, kcp=1, end=1, kr=0)

    crvLocMpnode = prefix+'Bendy_loc_grp'
    crvALocs = pointOnCrv.controlCvs(crvA, mpnode=crvLocMpnode)
    crvBLocs = pointOnCrv.controlCvs(crvB, mpnode=crvLocMpnode)
    crvCLocs = pointOnCrv.controlCvs(crvC, mpnode=crvLocMpnode)

    #------------------------------------------------------------------------------------------------------------------------------------------

    # connect crv loc
    # A
    mc.pointConstraint(ctrls[0], crvALocs[0]+'_grp', mo=1)
    mc.pointConstraint(ctrls[1], crvALocs[2]+'_grp', mo=1)
    mc.pointConstraint(upMidloc, crvALocs[4]+'_grp', mo=1)
    mc.pointConstraint(ctrls[0], ctrls[1], crvALocs[1]+'_grp', mo=1)
    mc.pointConstraint(ctrls[1], upMidloc, crvALocs[3]+'_grp', mo=1)

    # B
    mc.pointConstraint(loMidloc, crvBLocs[0]+'_grp', mo=1)
    mc.pointConstraint(ctrls[3], crvBLocs[2]+'_grp', mo=1)
    mc.pointConstraint(ctrls[4], crvBLocs[4]+'_grp', mo=1)  
    mc.pointConstraint(loMidloc, ctrls[3], crvBLocs[1]+'_grp', mo=1)
    mc.pointConstraint(ctrls[3], ctrls[4], crvBLocs[3]+'_grp', mo=1)

    # C
    mc.pointConstraint(ctrls[4], crvCLocs[0]+'_grp', mo=1)
    mc.pointConstraint(ctrls[5], crvCLocs[2]+'_grp', mo=1)
    mc.pointConstraint(ctrls[6], crvCLocs[4]+'_grp', mo=1)
    mc.pointConstraint(ctrls[4], ctrls[5], crvCLocs[1]+'_grp', mo=1)
    mc.pointConstraint(ctrls[5], ctrls[6], crvCLocs[3]+'_grp', mo=1)

    # smooth elbow
    mc.pointConstraint(smoothA_info['vmd'][0], crvALocs[3], mo=1)
    mc.pointConstraint(smoothA_info['vmd'][1], crvBLocs[1], mo=1)
    mc.pointConstraint(smoothB_info['vmd'][0], crvBLocs[3], mo=1)
    mc.pointConstraint(smoothB_info['vmd'][1], crvCLocs[1], mo=1)

    # create jnts
    upjntlist = []
    mdjntlist = []
    lojntlist = []

    for i in range(5):
        upjnt = prefix + '_ub' + aboutName.letter(i) + '_drv'
        mdjnt = prefix + '_mb' + aboutName.letter(i) + '_drv'
        lojnt = prefix + '_lb' + aboutName.letter(i) + '_drv'
        if mc.objExists(upjnt):
            upjntlist.append(upjnt)
        if mc.objExists(mdjnt):
            mdjntlist.append(mdjnt)
        if mc.objExists(lojnt):
            lojntlist.append(lojnt)

    upBikSys = crvSpline.ikSplineByJoints(prefix + '_ub', crvA, upjntlist, 1, strechAxis='tx', twistFix=False, volume=volume, mpNode=None)
    mdBikSys = crvSpline.ikSplineByJoints(prefix + '_mb', crvB, mdjntlist, 1, strechAxis='tx', twistFix=False, volume=volume, mpNode=None)
    loBikSys = crvSpline.ikSplineByJoints(prefix + '_lb', crvC, lojntlist, 1, strechAxis='tx', twistFix=False, volume=volume, mpNode=None)
    upBjnts = upBikSys['jointList']
    mdBjnts = mdBikSys['jointList']
    loBjnts = loBikSys['jointList']

    mc.connectAttr(twistBridges[0]+'.twist', upBikSys['ikh']+'.twist')
    mc.connectAttr(twistBridges[1]+'.twist', mdBikSys['ikh']+'.twist')
    mc.connectAttr(twistBridges[2]+'.twist', loBikSys['ikh']+'.twist')
    #------------------------------------------------------------------------------------------------------------------------------------

    if volume:
        aboutPublic.addNewAttr( objects=[ctrls[1]], attrName=['volume'], keyable=True, dv=0, min=0, max=1 )
        aboutPublic.addNewAttr( objects=[ctrls[3]], attrName=['volume'], keyable=True, dv=0, min=0, max=1 )
        aboutPublic.addNewAttr( objects=[ctrls[5]], attrName=['volume'], keyable=True, dv=0, min=0, max=1 )

        mc.connectAttr( ctrls[1]+'.volume', upBikSys['cmd']+'.volume' )
        mc.connectAttr( ctrls[3]+'.volume', mdBikSys['cmd']+'.volume' )
        mc.connectAttr( ctrls[3]+'.volume', loBikSys['cmd']+'.volume' )


    # clean
    # nox
    bendyNoxGrp = prefix+'Bendy_noTrans'
    if not mc.objExists(bendyNoxGrp):
        mc.createNode('transform', n=bendyNoxGrp)
        mc.hide(bendyNoxGrp)

    bendyNoxs = [crvLocMpnode, crvA, crvB, crvC, upBikSys['rootGrp'], mdBikSys['rootGrp'], loBikSys['rootGrp']]
    for nox in bendyNoxs:    
        mc.parent(nox, bendyNoxGrp)   

    # ctrl grp
    ctrlsGrp = prefix+'Bendy_ctrl_grp'
    if not mc.objExists(ctrlsGrp):
        mc.createNode('transform', n=ctrlsGrp)

    for ctrl in ctrls:
        mc.parent(ctrl+'_grp', ctrlsGrp)
        controlTools.tagKeyable(ctrl, 't smoothElbow keepVolume upTangent loTangent')

    # global scale
    initScale = 'worldA_ctrl.initScale'
    if mc.objExists(initScale):
        mc.connectAttr(initScale, upBikSys['cmd']+'.initScale')
        mc.connectAttr(initScale, mdBikSys['cmd']+'.initScale')
        mc.connectAttr(initScale, loBikSys['cmd']+'.initScale')

    bjnts = upBjnts[0:-2] + mdBjnts[0:-2] + loBjnts[0:-2]
    result = {'rootGrp':ctrlsGrp, 'noTrans':bendyNoxGrp, 'jointList':bjnts, 'upjnts':upBjnts, 'mdjnts':mdBjnts, 'lojnts':loBjnts}
    return result


def smoothJointLink(prefix, stCtrl, midCtrl, edCtrl):
    # inite
    midName = midCtrl.split('_')[-2]

    # create elbow smooth
    ctrlsOri = mc.createNode('transform', n=midCtrl + 'Ori', p=stCtrl)
    ctrlsOff = mc.createNode('transform', p=ctrlsOri, n=midCtrl + 'Off')

    mc.pointConstraint(stCtrl, ctrlsOri, n=ctrlsOri + '_pc')
    mc.pointConstraint(midCtrl, ctrlsOff, n=ctrlsOff + '_pc')
    mc.aimConstraint(edCtrl, ctrlsOri, aim=[0, 1, 0], u=[1, 0, 0], wu=[1, 0, 0], wut='objectRotation', wuo=midCtrl, n=ctrlsOri + '_ac')

    # create {0} blend poin
    bup = mc.createNode('transform', n=prefix + '_Up{0}_Static'.format(midName), p=ctrlsOff)
    blo = mc.createNode('transform', n=prefix + '_Lo{0}_Static'.format(midName), p=ctrlsOff)
    mc.pointConstraint(stCtrl, midCtrl, bup, n=bup + '_pc')
    mc.pointConstraint(midCtrl, edCtrl, blo, n=blo + '_pc')

    sup = mc.duplicate(bup, po=1, n=prefix + '_Up{0}_Smooth'.format(midName))[0]
    slo = mc.duplicate(blo, po=1, n=prefix + '_Lo{0}_Smooth'.format(midName))[0]
    mc.setAttr(sup + '.tx', 0)
    mc.setAttr(sup + '.tz', 0)
    mc.setAttr(slo + '.tx', 0)
    mc.setAttr(slo + '.tz', 0)
    mc.setAttr(sup + '.ty', mc.getAttr(bup + '.ty'))
    mc.setAttr(slo + '.ty', mc.getAttr(blo + '.ty'))

    blup = mc.duplicate(sup, po=1, n=prefix + 'Up{0}Blend'.format(midName))[0]
    bllo = mc.duplicate(slo, po=1, n=prefix + 'Lo{0}Blend'.format(midName))[0]

    upc = mc.pointConstraint(sup, bup, blup, n=blup + '_pc')[0]
    lpc = mc.pointConstraint(slo, blo, bllo, n=bllo + '_pc')[0]

    mc.addAttr(midCtrl, ln='___', nn=' ', at='enum', en=' ', k=1)
    mc.addAttr(midCtrl, ln='smooth', at='double', min=0, max=1, k=1)
    mc.addAttr(midCtrl, ln='upTangent', at='double', dv=1, min=0, max=10, k=1)
    mc.addAttr(midCtrl, ln='loTangent', at='double', dv=1, min=0, max=10, k=1)

    mc.connectAttr(midCtrl + '.smooth', upc + '.w0')
    mc.connectAttr(midCtrl + '.smooth', lpc + '.w0')
    mc.setDrivenKeyframe(upc + '.w1', cd=midCtrl + '.smooth', dv=0, v=1)
    mc.setDrivenKeyframe(upc + '.w1', cd=midCtrl + '.smooth', dv=1, v=0)
    mc.setDrivenKeyframe(lpc + '.w1', cd=midCtrl + '.smooth', dv=0, v=1)
    mc.setDrivenKeyframe(lpc + '.w1', cd=midCtrl + '.smooth', dv=1, v=0)

    mc.setDrivenKeyframe(sup + '.ty', cd=midCtrl + '.upTangent', dv=1)
    mc.setDrivenKeyframe(sup + '.ty', cd=midCtrl + '.upTangent', dv=0, v=0)
    mc.setDrivenKeyframe(sup + '.ty', cd=midCtrl + '.upTangent', dv=10, v=mc.getAttr(blup + '.ty') * 30)

    mc.setDrivenKeyframe(slo + '.ty', cd=midCtrl + '.loTangent', dv=1)
    mc.setDrivenKeyframe(slo + '.ty', cd=midCtrl + '.loTangent', dv=0, v=0)
    mc.setDrivenKeyframe(slo + '.ty', cd=midCtrl + '.loTangent', dv=10, v=mc.getAttr(bllo + '.ty') * 30)

    result={'vmd':[blup, bllo]}
    return result