import maya.cmds as mc
from rxCore import aboutPublic

def getdir(jnts):

    l0 = aboutPublic.snapLoc(jnts[0])
    l1 = aboutPublic.snapLoc(jnts[0])
    l2 = aboutPublic.snapLoc(jnts[1])
    l3 = aboutPublic.snapLoc(jnts[2])
    mc.xform(l0, r=1, t=[10,0,0])
    mc.delete(mc.aimConstraint(l0, l1, aim=[1,0,0], u=[0,-1,0], wut='object', wuo=l3))
    mc.parent (l2, l1)

    behind = False
    if mc.getAttr(l2+'.tz') < 0.0:
        behind = True

    mc.delete(l0, l1, l2, l3)
    return behind

def pvFollow(ctrl, jnts, footctrl, mirror):

    # Create nodesand offset attrs
    pvgrp = mc.createNode('transform', n=ctrl+'_Align_grp')
    pvalign = mc.createNode('transform', n=ctrl+'_pv_Align_space', p=pvgrp)
    mc.delete(mc.pointConstraint(jnts[0], pvgrp))
    mc.delete(mc.aimConstraint(jnts[-1], pvgrp, aim=[1,0,0], u=[0,1,0], wut='object', wuo=ctrl))
    mc.delete(mc.aimConstraint(footctrl, pvgrp, aim=[1,0,0], u=[0,1,0], wu=[0,0,1], wuo=footctrl, wut='objectRotation'))
    mc.aimConstraint(footctrl, pvalign, n=pvalign+'_ac', aim=[1,0,0], u=[0,1,0], wu=[0,0,1], wuo=footctrl, wut='objectRotation')

    result = {'root':pvgrp, 'space':pvalign}
    return result


def pvSide(pvctrl, ik, jnts, mirror):

    pvm = mc.createNode('transform', n=pvctrl+'_side', p=jnts[1])
    mc.setAttr(pvm + '.tz', -5 * mirror)
    mc.parent(pvm, jnts[0])
    mc.poleVectorConstraint(pvm, ik, n=ik+'_pvc')
    mc.setAttr(ik+'.twist', -90*mirror)
