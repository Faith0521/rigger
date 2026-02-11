######################################
#   Rig Build - Prep Build
######################################
import maya.cmds as mc

from rxCore import aboutPublic
from rxCore import aboutLock
import controlTools
import templateTools
import assetImport

def build(segScale=False, importAsset=True):
    print ('ASSETVAL = {0}'.format(importAsset))

    # use newest template file
    if importAsset:
        mc.file(new=1, f=1)
        assetImport.template()

    # remove constraints
    cstNodes = mc.ls(type =('pointConstraint', 'aimConstraint', 'orientConstraint', 'parentConstraint', 'ikHandle', 'follicle'))
    if cstNodes:
        mc.delete(cstNodes)

    # Get parts from .rigPart attribute
    parts = []
    nodes = mc.ls('*.rigPart')
    for n in nodes:
        parts.append( n.replace('.rigPart', '') )

    # Get ctrls and joints from .tag
    tagNodes = mc.ls('*.tag')
    ctrls, tPose= [], []

    for n in tagNodes:
        tag = mc.getAttr(n)
        if 'animCtrl' in tag:
            ctrls.append(n.replace('.tag', ''))
        if 'tPose' in tag:
            tPose.append(n.replace('.tag', ''))

    # dup off part nodes:
    partTop = mc.createNode('transform', n='partsPrep')
    for p in parts:
        sc = mc.duplicate(p, n=p+'Prep', po=1)
        mc.parent(sc[0], partTop)

    # create new ctrlgrp and put ctrl in this grp
    ctrlsPrep = mc.createNode('transform', n='ctrlsPrep' )
    mc.hide(ctrlsPrep)

    for ctrl in ctrls:
        sctrl = mc.duplicate(ctrl, n=ctrl+'Prep', po=1)[0]
        controlTools.copyShape([ctrl, sctrl], copyColor=1)
        aboutLock.unlock(sctrl)

        par = mc.listRelatives(ctrl, p=1)
        if par:
            par = par[0]
            spar = mc.duplicate(par, n=par+'Prep', po=1)[0]
            aboutLock.unlock(spar)
            mc.parent(sctrl, spar)
            mc.parent(spar, ctrlsPrep)
        else:
            mc.parent(sctrl, ctrlsPrep)

    # get joints and parents and dups
    partParents, partJoints, dupJoints= [], [], []
    for part in parts:
        parent = templateTools.getArgs(part, 'parent')
        if parent:
            partParents.append(parent)
        else:
            partParents.append('')

        # joints
        djnts = []
        jnts = mc.listRelatives(part+'Joints', c=1, type='joint')
        if jnts:
            partJoints.append(jnts)
            for jnt in jnts:
                djnt = mc.duplicate(jnt, n=jnt+'DupTmp')[0]
                sel = mc.select(djnt, hi=1)
                aboutLock.unlock(sel)
                mc.parent(djnt, w=1)
                djnts.append(djnt)

            dupJoints.append(djnts)
        else:
            partJoints.append([])
            dupJoints.append([])

    # crvs
    # Get useful crvs for rigging
    crvsPrep = mc.createNode('transform', n='crvsPrep')
    crvShapes = mc.ls(type='nurbsCurve', ni=1)

    # remove control shapes
    for c in crvShapes:
        if '_org' in c :
            crv = mc.listRelatives(c, p=1)[0]
            aboutLock.unlock(crv)

            usefull_crv = crv + 'Prep'
            mc.duplicate(crv, n=usefull_crv)
            mc.delete(crv)
            mc.parent(usefull_crv, crvsPrep)

    # Nurbs
    # Get useful nurbs for rigging
    nurbsPrep = mc.createNode('transform', n='nurbsPrep')
    nurbShapes = mc.ls(type='nurbsSurface', ni=1)

    for n in nurbShapes:
        if '_org' in n:
            nurb = mc.listRelatives(n, p=1)[0]
            aboutLock.unlock(nurb)

            usefull_nurb = nurb + 'Prep'
            mc.duplicate(nurb, n=usefull_nurb, rc=1)

            # delete nurb child but shapes
            childs = mc.listRelatives(usefull_nurb)
            nshape = mc.listRelatives(usefull_nurb, s=True)[0]
            for c in childs:
                if c != nshape:
                    mc.delete(c)

            mc.delete(nurb)
            mc.parent(usefull_nurb, nurbsPrep)

    # pose driver
    tagNodes = mc.ls('*.tag')
    poseDrivers = []

    for n in tagNodes:
        tag = mc.getAttr(n)
        if 'poseDriver' in tag:
            poseDrivers.append(n.replace('.tag', ''))

    psdPrep = mc.createNode('transform', n='psdPrep' )
    mc.hide(psdPrep)

    if poseDrivers:
        for psd in poseDrivers:
            mc.parent(psd, psdPrep)


    # Delete Prep
    mc.delete('template')

    for i in range(len(parts)):
        cjnts = partJoints[i] # jnt
        djnts = dupJoints[i] # jnt

        # rename DupTmp jnts by org
        for j in range(len(djnts)):
            cjnts[j] = mc.rename(djnts[j], cjnts[j])

        # refresh partJoints
        partJoints[i] = cjnts

    # lf_wrist [u'lf_indexBase', u'lf_middleBase', u'lf_ringBase', u'lf_pinkyBase', u'lf_thumbBase']
    for i in range( len(parts) ):
        cpar = partParents[i]
        cjnts = partJoints[i]

        # parent jnts to part parents
        if 'worldRoot' not in cjnts:
            if mc.objExists(cpar):
                mc.parent(cjnts, cpar)
            else:
                mc.parent(cjnts, 'worldRoot')


    # clean it up
    joints = mc.ls(type='joint')
    for j in joints:
        mc.setAttr(j+'.radi', 1)
        # modify global scale
        if not segScale:
            mc.setAttr(j+'.segmentScaleCompensate', 0)

    mc.makeIdentity('worldRoot', a=1, t=1, r=1,s=1, n=1, pn=1)
    Prep = mc.createNode('transform', n='Prep')

    # drv jnts
    drvJnts = mc.duplicate('worldRoot', rc=True)
    for jnt in drvJnts:
        newName = jnt.replace('1', '_drv')
        mc.rename(jnt, newName)

    # connect locators
    connectLocs = []
    for parent in partParents:
        if 'numCtrls' not in parent:
            if mc.objExists(parent):
                locName = parent + '_connect_loc'
                if not mc.objExists(locName):
                    loc = aboutPublic.snapLoc(parent, parent + '_connect_loc')
                    mc.hide(loc)
                    connectLocs.append(loc)
                else:
                    connectLocs.append(locName)

    mc.parent('worldRoot', 'worldRoot_drv', partTop, ctrlsPrep, crvsPrep, nurbsPrep, psdPrep, connectLocs, Prep)

