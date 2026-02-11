# coding: utf-8
# This Function can stretch IK joint
# Date: 2020/09/02_v1.0
#-------------------------------------------------------------------------------------------------------------------------------------

# import stretchTools
# reload(stretchTools)
# jnts=['lf_upArm', 'lf_loArm', 'lf_wrist']
# stretchTools.stretchSoftIk('lf_', 'lf_shoulder', jnts, 'lf_armIk_ctrl', 'lf_elbowIk_ctrl', sticky=True, mpNode=None )

#-------------------------------------------------------------------------------------------------------------------------------------

import maya.cmds as mc

from rxCore import aboutPublic
from rxCore import aboutLock

#-------------------------------------------------------------------------------------------------------------------------------------

def stretchIk(prefix, parent, jnts, ikCtrl, axis, mpNode=None):

    stJnt = jnts[0]
    edJnt = jnts[1]

    mirror = 1
    if 'rt' in prefix:
        mirror = -1

    # create used locator
    stloc = aboutPublic.snapLoc(stJnt, name=prefix+'stretch_st_loc')
    edloc = aboutPublic.snapLoc(edJnt, name=prefix+'stretch_ed_loc')

    # modify locator pos
    if not mpNode:
        mpNode = prefix+'stretchIk_noTrans'
        mc.createNode('transform', n=mpNode)
        mc.parent([stloc, edloc], mpNode)  

    mc.parentConstraint(parent, stloc, n=stloc+'_prc', mo=1)
    mc.pointConstraint(ikCtrl, edloc, n=edloc+'_pc')

    # create dist shape
    realDist = mc.createNode('transform', n=prefix+'realDist')
    realDistShape = mc.createNode('distanceDimShape', p=realDist, n=prefix+'realDistShape')

    # set dist start and end points
    stlocShape=mc.listRelatives(stloc, s=1)[0]
    edlocShape=mc.listRelatives(edloc, s=1)[0]

    mc.connectAttr(stlocShape+'.worldPosition[0]', realDistShape+'.startPoint')
    mc.connectAttr(edlocShape+'.worldPosition[0]', realDistShape+'.endPoint')
    mc.parent(realDist, mpNode)

    # create bridge
    cbridge=prefix+'stretchIk_cmd_bridge'
    vbridge=prefix+'stretchIk_value_bridge'

    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge, p=mpNode)
        aboutLock.lock(cbridge)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['stretch'], 
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'], 
                               lock=False, attributeType='float', keyable=True, dv=1, min=0.001, max=1)

    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge, p=mpNode)
        aboutLock.lock(vbridge)
        aboutPublic.addNewAttr(objects=[vbridge], attrName=['stretch', 'inA'],
                               lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

    #> connect cmd bridge

    #> initScale by base ctrl
    if mc.objExists('worldA_ctrl.initScale'):
        initScaleAttr = 'worldA_ctrl.initScale'
        mc.connectAttr(initScaleAttr, cbridge+'.initScale')
    else:
        mc.setAttr(cbridge + '.initScale', 1)

    # connect ctrl with bridges
    mc.connectAttr(cbridge+'.stretch', vbridge+'.stretch')

    orgdis = abs( mc.getAttr(edJnt+'.'+axis) )
    realInA_mdl = mc.createNode('multDoubleLinear', n=prefix+'stretch_real_inA_mdl')
    mc.connectAttr(cbridge+'.initScale', realInA_mdl+'.input1')
    mc.connectAttr(realDistShape+'.distance', realInA_mdl+'.input2')
    mc.connectAttr(realInA_mdl+'.output', vbridge+'.inA') 

    needMove_pma = mc.createNode('plusMinusAverage', n=prefix+'needMove_pma')
    mc.setAttr(needMove_pma+'.operation', 2)
    mc.connectAttr(vbridge+'.inA', needMove_pma+'.input1D[0]')
    mc.setAttr(needMove_pma+'.input1D[1]', orgdis)

    outPut_adl = mc.createNode('addDoubleLinear', n=prefix+'stretch_outPut_adl')
    mc.connectAttr(needMove_pma+'.output1D', outPut_adl+'.input1')
    mc.setAttr(outPut_adl+'.input2', orgdis)

    OnOff_bla = mc.createNode('blendTwoAttr', n=prefix+'stretch_OnOff_bla')
    mc.connectAttr(vbridge+'.stretch', OnOff_bla+'.attributesBlender')    
    mc.setAttr(OnOff_bla+'.input[0]', orgdis)
    mc.connectAttr(outPut_adl+'.output', OnOff_bla+'.input[1]')
    mc.connectAttr(OnOff_bla+'.output', edJnt+'.'+axis)

    # clean
    if mc.objExists('noTransform'):
        mc.parent(mpNode, 'noTransform')
        mc.hide(mpNode)

    result = {'rootGrp':mpNode,'cmd': cbridge, 'vmd':vbridge}
    return result


def stretchIk_db(prefix, parent, jnts, aimjnt, ikCtrl, axis, mpNode=None):

    stJnt = jnts[0]
    edJnt = jnts[1]

    mirror = 1
    if 'rt' in prefix:
        mirror = -1

    # create used locator
    stloc = aboutPublic.snapLoc(stJnt, name=prefix+'stretch_st_loc')
    edloc = aboutPublic.snapLoc(edJnt, name=prefix+'stretch_ed_loc')

    # modify locator pos
    if not mpNode:
        mpNode = prefix+'stretchIk_noTrans'
        mc.createNode('transform', n=mpNode)
        mc.parent([stloc, edloc], mpNode)

    mc.parentConstraint(parent, stloc, n=stloc+'_prc', mo=1)
    mc.pointConstraint(ikCtrl, edloc, n=edloc+'_pc')

    # create dist shape
    realDist = mc.createNode('transform', n=prefix+'realDist')
    realDistShape = mc.createNode('distanceDimShape', p=realDist, n=prefix+'realDistShape')

    # set dist start and end points
    stlocShape=mc.listRelatives(stloc, s=1)[0]
    edlocShape=mc.listRelatives(edloc, s=1)[0]

    mc.connectAttr(stlocShape+'.worldPosition[0]', realDistShape+'.startPoint')
    mc.connectAttr(edlocShape+'.worldPosition[0]', realDistShape+'.endPoint')
    mc.parent(realDist, mpNode)

    # create bridge
    cbridge=prefix+'stretchIk_cmd_bridge'
    vbridge=prefix+'stretchIk_value_bridge'

    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge, p=mpNode)
        aboutLock.lock(cbridge)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['stretch'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0, max=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'],
                               lock=False, attributeType='float', keyable=True, dv=1, min=0.001, max=1)

    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge, p=mpNode)
        aboutLock.lock(vbridge)
        aboutPublic.addNewAttr(objects=[vbridge], attrName=['stretch', 'inA'],
                               lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

    #> connect cmd bridge

    #> initScale by base ctrl
    if mc.objExists('worldA_ctrl.initScale'):
        initScaleAttr = 'worldA_ctrl.initScale'
        mc.connectAttr(initScaleAttr, cbridge+'.initScale')
    else:
        mc.setAttr(cbridge + '.initScale', 1)

    # connect ctrl with bridges
    mc.connectAttr(cbridge+'.stretch', vbridge+'.stretch')

    orgdis = abs( mc.getAttr(edJnt+'.'+axis) )
    realInA_mdl = mc.createNode('multDoubleLinear', n=prefix+'stretch_real_inA_mdl')
    mc.connectAttr(cbridge+'.initScale', realInA_mdl+'.input1')
    mc.connectAttr(realDistShape+'.distance', realInA_mdl+'.input2')
    mc.connectAttr(realInA_mdl+'.output', vbridge+'.inA')

    needMove_pma = mc.createNode('plusMinusAverage', n=prefix+'needMove_pma')
    mc.setAttr(needMove_pma+'.operation', 2)
    mc.connectAttr(vbridge+'.inA', needMove_pma+'.input1D[0]')
    mc.setAttr(needMove_pma+'.input1D[1]', orgdis)

    aimOrgDis = abs( mc.getAttr(aimjnt+'.'+axis) )
    outPut_adl = mc.createNode('addDoubleLinear', n=prefix+'stretch_outPut_adl')
    mc.connectAttr(needMove_pma+'.output1D', outPut_adl+'.input1')
    mc.setAttr(outPut_adl+'.input2', aimOrgDis)

    OnOff_bla = mc.createNode('blendTwoAttr', n=prefix+'stretch_OnOff_bla')
    mc.connectAttr(vbridge+'.stretch', OnOff_bla+'.attributesBlender')
    mc.setAttr(OnOff_bla+'.input[0]', aimOrgDis)
    mc.connectAttr(outPut_adl+'.output', OnOff_bla+'.input[1]')
    mc.connectAttr(OnOff_bla+'.output', aimjnt+'.'+axis)

    # clean
    if mc.objExists('noTransform'):
        mc.parent(mpNode, 'noTransform')
        mc.hide(mpNode)

    result = {'rootGrp':mpNode,'cmd': cbridge, 'vmd':vbridge}
    return result