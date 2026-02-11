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
from rxCore import aboutName

#-------------------------------------------------------------------------------------------------------------------------------------

def stretchSoftIk(prefix, parent, jnts, ikCtrl, pvCtrl, stretch=True, mpNode=None):

    stJnt = jnts[0]
    midJnt = jnts[1] 
    edJnt = jnts[2]

    mirror = 1
    if 'rt' in prefix:
        mirror = -1

    # create used locator
    stloc = aboutPublic.snapLoc(stJnt, name=prefix+'st_loc')
    stAimloc = aboutPublic.snapLoc(stJnt, name=prefix+'stAim_loc')
    pvloc = aboutPublic.snapLoc(pvCtrl, name=prefix+'mid_loc')
    softloc = aboutPublic.snapLoc(stJnt, name=prefix+'soft_loc')
    blendloc = aboutPublic.snapLoc(edJnt, name=prefix+'blend_loc')
    stretchloc = aboutPublic.snapLoc(edJnt, name=prefix+'stretch_loc')
    controlloc = aboutPublic.snapLoc(edJnt, name=prefix+'control_loc')

    # modify locator pos
    if not mpNode:
        mpNode = prefix+'softIk_noTrans'
        mc.createNode('transform', n=mpNode)
        mc.parent([stloc, pvloc, stAimloc, softloc, blendloc, controlloc, stretchloc], mpNode)

    mc.parentConstraint(parent, stloc, n=stloc+'_prc', mo=1)
    mc.parent(stAimloc, stloc)
    mc.parent(softloc, stAimloc)
    mc.aimConstraint(controlloc, stAimloc, n=stAimloc+'_ac', aim=[1,0,0], u=[0,1,0], wut='objectrotation', wuo=parent)
    mc.delete( mc.pointConstraint(edJnt, softloc) )
    mc.parent(stretchloc, controlloc)
    mc.pointConstraint(pvCtrl, pvloc, n=pvloc+'_pc')
    
    # create dist shape
    controlDist = mc.createNode('transform', n=prefix+'controlDist')
    controlDistShape = mc.createNode('distanceDimShape', p=controlDist, n=prefix+'controlDistShape')

    softDist = mc.createNode('transform', n=prefix+'softDist')
    softDistShape = mc.createNode('distanceDimShape', p=softDist, n=prefix+'softDistShape')

    stickyADist = mc.createNode('transform', n=prefix+'stickyADist')
    stickyADistShape = mc.createNode('distanceDimShape', p=stickyADist, n=prefix+'stickyADistShape')

    stickyBDist = mc.createNode('transform', n=prefix+'stickyBDist')
    stickyBDistShape = mc.createNode('distanceDimShape', p=stickyBDist, n=prefix+'stickyBDistShape')

    # set dist start and end points
    stlocShape=mc.listRelatives(stloc, s=1)[0]
    softlocShape=mc.listRelatives(softloc, s=1)[0]
    stretchlocShape=mc.listRelatives(stretchloc, s=1)[0]
    pvlocShape=mc.listRelatives(pvloc, s=1)[0]
    blendlocShape=mc.listRelatives(blendloc, s=1)[0]

    mc.connectAttr(stlocShape+'.worldPosition[0]', controlDistShape+'.startPoint')
    mc.connectAttr(stretchlocShape+'.worldPosition[0]', controlDistShape+'.endPoint')

    mc.connectAttr(softlocShape+'.worldPosition[0]', softDistShape+'.startPoint')
    mc.connectAttr(blendlocShape+'.worldPosition[0]', softDistShape+'.endPoint')

    mc.connectAttr(stlocShape+'.worldPosition[0]', stickyADistShape+'.startPoint')
    mc.connectAttr(pvlocShape+'.worldPosition[0]', stickyADistShape+'.endPoint')

    mc.connectAttr(pvlocShape+'.worldPosition[0]', stickyBDistShape+'.startPoint')
    mc.connectAttr(blendlocShape+'.worldPosition[0]', stickyBDistShape+'.endPoint')

    mc.parent([controlDist, softDist, stickyADist, stickyBDist], mpNode)

    # create bridge
    cbridge=prefix+'softIk_cmd_bridge'
    vbridge=prefix+'softIk_value_bridge'

    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge, p=mpNode)
        aboutLock.lock(cbridge)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['soft', 'stretch', 'sticky'], 
                               lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['slide'], 
                               lock=False, attributeType='float', keyable=True, dv=0, min=-10, max=10)
        aboutPublic.addNewAttr(objects=[cbridge], attrName=['upLength', 'loLength'], 
                               lock=False, attributeType='float', keyable=True, dv=1, min=-10, max=10)

    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge, p=mpNode)
        aboutLock.lock(vbridge)
        aboutPublic.addNewAttr(objects=[vbridge], attrName=['orgA', 'orgB'],
                               lock=False, attributeType='float', keyable=False)

        aboutPublic.addNewAttr(objects=[vbridge], attrName=['soft', 'stretch', 'sticky'], 
                               lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

        aboutPublic.addNewAttr(objects=[vbridge], attrName=['slide', 'inA', 'inB', 'chain', 'controlDist', 'softDist', 'stickyADist', 'stickyBDist'],
                               lock=False, attributeType='float', keyable=True, dv=0)

    #> connect cmd bridge
    #> initScale by base ctrl
    initScale = 'worldA_ctrl.initScale'

    #>> 'stretch', 'sticky', 'soft', 'upLength', 'loLength'
    aboutPublic.addNewAttr(objects=[ikCtrl], attrName=['soft','stretch'], 
                           lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

    aboutPublic.addNewAttr(objects=[ikCtrl], attrName=['slide'], 
                           lock=False, attributeType='float', keyable=True, dv=0, min=-10, max=10)

    aboutPublic.addNewAttr(objects=[ikCtrl], attrName=['upLength', 'loLength'], 
                           lock=False, attributeType='float', keyable=True, dv=1, min=-10, max=10)

    aboutPublic.addNewAttr(objects=[pvCtrl], attrName=['sticky'], 
                           lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

    # connect ctrl with bridges
    mc.connectAttr(cbridge+'.soft', vbridge+'.soft')
    mc.connectAttr(cbridge+'.stretch', vbridge+'.stretch')
    mc.connectAttr(cbridge+'.sticky', vbridge+'.sticky')
    mc.connectAttr(cbridge+'.slide', vbridge+'.slide')

    mc.connectAttr(ikCtrl+'.slide', cbridge+'.slide')
    mc.connectAttr(ikCtrl+'.stretch', cbridge+'.stretch')   
    mc.connectAttr(ikCtrl+'.upLength', cbridge+'.upLength')
    mc.connectAttr(ikCtrl+'.loLength', cbridge+'.loLength')
    mc.connectAttr(pvCtrl+'.sticky', cbridge+'.sticky')


    #> connect value bridge

    # -----------------------------------------------------------------------------------------------
    #  start check natural / quad
    #>> inA
    inA = abs( mc.getAttr(midJnt+'.tx') )
    mc.setAttr(vbridge+'.orgA', inA)
    realInA_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_inA_mdl')
    mc.connectAttr(cbridge+'.upLength', realInA_mdl+'.input1')
    mc.setAttr(realInA_mdl+'.input2', inA)
    mc.connectAttr(realInA_mdl+'.output', vbridge+'.inA')

    # >> inB
    inB = abs( mc.getAttr(edJnt+'.tx') )
    mc.setAttr(vbridge + '.orgB', inB)
    realInB_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_inB_mdl')
    mc.connectAttr(cbridge+'.loLength', realInB_mdl+'.input1')
    mc.setAttr(realInB_mdl+'.input2', inB)
    mc.connectAttr(realInB_mdl+'.output', vbridge+'.inB')

    #>> chain
    realChain_adl = mc.createNode('addDoubleLinear', n=prefix+'real_chain_adl')
    mc.connectAttr(realInA_mdl+'.output', realChain_adl+'.input1')
    mc.connectAttr(realInB_mdl+'.output', realChain_adl+'.input2')
    mc.connectAttr(realChain_adl+'.output', vbridge+'.chain')

    #>> controlDistv
    realControlDist_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_controlDist_mdl')
    mc.connectAttr(initScale, realControlDist_mdl+'.input1')
    mc.connectAttr(controlDistShape+'.distance', realControlDist_mdl+'.input2')
    mc.connectAttr(realControlDist_mdl+'.output', vbridge+'.controlDist')

    #>> softDistv
    realSoftDist_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_softDist_mdl')
    mc.connectAttr(initScale, realSoftDist_mdl+'.input1')
    mc.connectAttr(softDistShape+'.distance', realSoftDist_mdl+'.input2')
    mc.connectAttr(realSoftDist_mdl+'.output', vbridge+'.softDist')

    #>> stickyADistv
    realStickyADist_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_stickyADist_mdl')
    mc.connectAttr(initScale, realStickyADist_mdl+'.input1')
    mc.connectAttr(stickyADistShape+'.distance', realStickyADist_mdl+'.input2')
    mc.connectAttr(realStickyADist_mdl+'.output', vbridge+'.stickyADist')

    #>> stickyBDistv
    realStickyBDist_mdl = mc.createNode('multDoubleLinear', n=prefix+'real_stickyBDist_mdl')
    mc.connectAttr(initScale, realStickyBDist_mdl+'.input1')
    mc.connectAttr(stickyBDistShape+'.distance', realStickyBDist_mdl+'.input2')
    mc.connectAttr(realStickyBDist_mdl+'.output', vbridge+'.stickyBDist')

    # create soft system
    # >> expression example

    # $controlDist = vbridge.controlDist
    # $softValue = $controlDist
    # $chain = vbridge.chain
    # $soft = cbridge.soft

    # if( $controlDist > ($chain - $soft) )
    # {
    #   if($soft > 0)
    #   {
    #       $softValue = $chain - $soft * exp( -($controlDist-($chain-$soft)) / $soft );
    #   }

    #   else
    #   {
    #       $softValue = $chain
    #   }
    # }
    # softloc.tx = $softValue


    # >> create soft nodes
    chainSubSoft_pma = mc.createNode('plusMinusAverage', n=prefix+'chain_Sub_Soft_pma') #da
    controlDistSubDa_pma = mc.createNode('plusMinusAverage', n=prefix+'controlDist_Sub_Da_pma')
    regative_mdl = mc.createNode('multDoubleLinear', n=prefix+'regative_mdl')
    divideSoft_md = mc.createNode('multiplyDivide', n=prefix+'divideSoft_md')
    ePower_md = mc.createNode('multiplyDivide', n=prefix+'ePower_md')
    multSoft_mdl = mc.createNode('multDoubleLinear', n=prefix+'multSoft_mdl')
    chainSubBefore_pma = mc.createNode('plusMinusAverage', n=prefix+'chain_Sub_Before_pma')
    softGreatThanZero_cnd = mc.createNode('condition', n=prefix+'soft_GreatThan_Zero_cnd')
    controlDistGreatThanDa_cnd = mc.createNode('condition', n=prefix+'controlDist_GreatThan_Da_cnd')

    # >> connect soft nodes
    # >>> chainSubSoft_pma
    mc.connectAttr(vbridge+'.chain', chainSubSoft_pma+'.input1D[0]')
    mc.connectAttr(vbridge+'.soft', chainSubSoft_pma+'.input1D[1]')
    mc.setAttr(chainSubSoft_pma+'.operation', 2)

    # >>> controlDistSubDa_pma
    mc.connectAttr(vbridge+'.controlDist', controlDistSubDa_pma+'.input1D[0]')
    mc.connectAttr(chainSubSoft_pma+'.output1D', controlDistSubDa_pma+'.input1D[1]')
    mc.setAttr(controlDistSubDa_pma+'.operation', 2)

    # >>> regative_mdl
    mc.connectAttr(controlDistSubDa_pma+'.output1D', regative_mdl+'.input1')
    mc.setAttr(regative_mdl+'.input2', -1)

    # >>> divideSoft_md
    mc.connectAttr(regative_mdl+'.output', divideSoft_md+'.input1X')
    mc.connectAttr(vbridge+'.soft', divideSoft_md+'.input2X')
    mc.setAttr(divideSoft_md+'.operation', 2)

    # >>> ePower_md
    mc.connectAttr(divideSoft_md+'.output.outputX', ePower_md+'.input2X')
    mc.setAttr(ePower_md+'.input1X', 2.718282)
    mc.setAttr(ePower_md+'.operation', 3)

    # >>> multSoft_mdl
    mc.connectAttr(ePower_md+'.output.outputX', multSoft_mdl+'.input1')
    mc.connectAttr(vbridge+'.soft', multSoft_mdl+'.input2')

    # >>> chainSubBefore_pma
    mc.connectAttr(multSoft_mdl+'.output', chainSubBefore_pma+'.input1D[1]')
    mc.connectAttr(vbridge+'.chain', chainSubBefore_pma+'.input1D[0]')
    mc.setAttr(chainSubBefore_pma+'.operation', 2)

    # >>> softGreatThanZero_cnd
    mc.connectAttr(chainSubBefore_pma+'.output1D', softGreatThanZero_cnd+'.colorIfTrue.colorIfTrueR')
    mc.connectAttr(vbridge+'.chain', softGreatThanZero_cnd+'.colorIfFalse.colorIfFalseR')
    mc.connectAttr(vbridge+'.soft', softGreatThanZero_cnd+'.firstTerm')
    mc.setAttr(softGreatThanZero_cnd+'.secondTerm', 0)
    mc.setAttr(softGreatThanZero_cnd+'.operation', 2)

    # >>> controlDistGreatThanDa_cnd
    mc.connectAttr(softGreatThanZero_cnd+'.outColorR', controlDistGreatThanDa_cnd+'.colorIfTrue.colorIfTrueR')
    mc.connectAttr(vbridge+'.controlDist', controlDistGreatThanDa_cnd+'.colorIfFalse.colorIfFalseR')
    mc.connectAttr(chainSubSoft_pma+'.output1D', controlDistGreatThanDa_cnd+'.secondTerm')
    mc.connectAttr(vbridge+'.controlDist', controlDistGreatThanDa_cnd+'.firstTerm')
    mc.setAttr(controlDistGreatThanDa_cnd+'.operation', 2)

    mc.connectAttr(controlDistGreatThanDa_cnd+'.outColorR', softloc+'.tx')

    # create stretch nodes
    # >> expression example

    # $softDist = vbridge.softDist
    # $chain = vbridge.chain
    # $stretch = vbridge.stretch
    # $inA = vbridge.inA

    # loArm.tx = ($softDist * ($inA / $chain) * $stretch + $inA)

    # check stretch joints number
    needStretchJnts = [midJnt, edJnt]

    if stretch:
        pc = mc.pointConstraint(softloc, stretchloc, blendloc, n=blendloc+'_pc')[0]

        mc.setDrivenKeyframe('{0}.{1}W0'.format(pc, softloc), cd=cbridge+'.stretch', dv=0, v=1)
        mc.setDrivenKeyframe('{0}.{1}W0'.format(pc, softloc), cd=cbridge+'.stretch', dv=1, v=0)
        mc.setDrivenKeyframe('{0}.{1}W1'.format(pc, stretchloc), cd=cbridge+'.stretch', dv=0, v=0)
        mc.setDrivenKeyframe('{0}.{1}W1'.format(pc, stretchloc), cd=cbridge+'.stretch', dv=1, v=1)

        for i, jnt in enumerate(needStretchJnts):
            proportion_md = mc.createNode( 'multiplyDivide', n='{0}in{1}_divChain_md'.format(prefix, aboutName.letter(i)) )
            mulSoftDist_mdl = mc.createNode( 'multDoubleLinear', n='{0}in{1}_multSoftDist_mdl'.format(prefix, aboutName.letter(i)) )
            stretchOnOff_mdl = mc.createNode( 'multDoubleLinear', n='{0}in{1}_stretch_OnOff_mdl'.format(prefix, aboutName.letter(i)) )
            addBoneLen_adl = mc.createNode('addDoubleLinear', n='{0}in{1}_addBoneLen_mdl'.format(prefix, aboutName.letter(i)) )
            side_mdl = mc.createNode( 'multDoubleLinear', n='{0}in{1}_stretch_Side_mdl'.format(prefix, aboutName.letter(i)) )

            # >> proportion_md
            mc.connectAttr( '{0}.in{1}'.format(vbridge, aboutName.letter(i)),  proportion_md+'.input1X')
            mc.connectAttr( vbridge+'.chain',  proportion_md+'.input2X')
            mc.setAttr(proportion_md+'.operation', 2)

            # >> mulSoftDist_mdl
            mc.connectAttr(proportion_md+'.output.outputX', mulSoftDist_mdl+'.input2')
            mc.connectAttr(vbridge+'.softDist', mulSoftDist_mdl+'.input1')

            # >> stretchOnOff_mdl
            mc.connectAttr(mulSoftDist_mdl+'.output', stretchOnOff_mdl+'.input2')
            mc.connectAttr(vbridge+'.stretch', stretchOnOff_mdl+'.input1')

            # >> addBoneLen_adl
            mc.connectAttr(stretchOnOff_mdl+'.output', addBoneLen_adl+'.input2')
            mc.connectAttr('{0}.in{1}'.format(vbridge, aboutName.letter(i)), addBoneLen_adl+'.input1')

            # >> sticky & slide
            stickyOnOff_bla = mc.createNode( 'blendTwoAttr', n='{0}in{1}_sticky_OnOff_bla'.format(prefix, aboutName.letter(i)) )
            mulChainDist_mdl = mc.createNode( 'multDoubleLinear', n='{0}in{1}_multChainDist_mdl'.format(prefix, aboutName.letter(i)) )
            slideOnOff_mdl = mc.createNode( 'multDoubleLinear', n='{0}in{1}_slide_OnOff_mdl'.format(prefix, aboutName.letter(i)) )
            slideOutPut_pma = mc.createNode('plusMinusAverage', n='{0}in{1}_slide_OutPut_pma'.format(prefix, aboutName.letter(i)) )


            mc.connectAttr(proportion_md+'.output.outputX', mulChainDist_mdl+'.input1')
            mc.connectAttr(vbridge+'.chain', mulChainDist_mdl+'.input2')
            mc.connectAttr(mulChainDist_mdl+'.output', slideOnOff_mdl+'.input1')
            mc.connectAttr(vbridge+'.slide', slideOnOff_mdl+'.input2')  

            if i==0:
                slide_cnd = mc.createNode('condition', n='{0}inAB_slide_cnd'.format(prefix) )
                mc.connectAttr(vbridge+'.slide', slide_cnd+'.firstTerm')
                mc.setAttr(slide_cnd+'.operation', 4)
                mc.connectAttr(slideOnOff_mdl+'.output', slide_cnd+'.colorIfFalse.colorIfFalseR')
                mc.setAttr(slideOutPut_pma+'.operation', 1)
            else:
                mc.connectAttr(slideOnOff_mdl+'.output', slide_cnd+'.colorIfTrue.colorIfTrueR')
                mc.setAttr(slideOutPut_pma+'.operation', 2)

            mc.connectAttr(addBoneLen_adl+'.output', slideOutPut_pma+'.input1D[0]')
            mc.connectAttr(slide_cnd+'.outColorR', slideOutPut_pma+'.input1D[1]')            
            mc.connectAttr(slideOutPut_pma+'.output1D', stickyOnOff_bla+'.input[0]')

            mc.connectAttr('{0}.sticky{1}Dist'.format(vbridge, aboutName.letter(i)), stickyOnOff_bla+'.input[1]')
            mc.connectAttr(vbridge+'.sticky', stickyOnOff_bla+'.attributesBlender')
            mc.connectAttr(stickyOnOff_bla+'.output', side_mdl+'.input1')
            mc.setAttr(side_mdl+'.input2', mirror)
            mc.connectAttr(side_mdl+'.output', jnt+'.tx')
       
    else:
        pc = mc.pointConstraint(softloc, blendloc, n=blendloc+'_pc')[0]
        mc.deleteAttr(ikCtrl+'.stretch')
        mc.deleteAttr(ikCtrl+'.upLength')
        mc.deleteAttr(ikCtrl+'.loLength')
        mc.deleteAttr(pvCtrl+'.sticky') 
    
    # clean
    softMaxValue = mc.getAttr(vbridge+'.chain') * 0.12
    mc.setDrivenKeyframe(cbridge + '.soft', cd=ikCtrl + '.soft', dv=0, v=0, itt='linear', ott='linear')
    mc.setDrivenKeyframe(cbridge + '.soft', cd=ikCtrl + '.soft', dv=1, v=softMaxValue, itt='linear', ott='linear')

    mc.setAttr('ikRPsolver.tolerance', 1e-007)
    mc.scaleConstraint(parent, stloc)

    if mc.objExists('noTransform'):
        mc.parent(mpNode, 'noTransform')
        mc.hide(mpNode)

    result = {'blend':blendloc, 'controlloc':controlloc, 'cmd':cbridge, 'vmd':vbridge}
    return result


def stretchFk( prefix, FkCtrls, mpNode=None):

    ctrlNum = len(FkCtrls)
    attrName = []
    for i in range(ctrlNum):
        attrName.append('fkAdd'+str(i))

    # create bridge    
    bridge = mc.createNode('transform',  n = prefix+'stretch_FkCmd_Bridge')
    aboutLock.lock(bridge)
    aboutPublic.addNewAttr(objects=[bridge], attrName=attrName, lock=False, attributeType='float', keyable=True, dv=1, min=0.01, max=10000)#

    for i in range(ctrlNum):
        stretchLoc = aboutPublic.snapLoc(FkCtrls[i], name=FkCtrls[i]+'_length')
        mc.delete( mc.orientConstraint(FkCtrls[i], stretchLoc) )
        mc.parent(stretchLoc, FkCtrls[i])

        children = mc.listRelatives(FkCtrls[i], c=1)
        if len(children) > 1:
            mc.delete( mc.pointConstraint(children[1], stretchLoc) )
            mc.parent(children[1], stretchLoc)
            serial = aboutName.letter(i)
            stretchNode = mc.createNode('multDoubleLinear', n=prefix+'StretchFK'+serial+'_mdl')
            mc.connectAttr(bridge+'.'+attrName[i], stretchNode+'.input1')
            defaultDis = mc.getAttr(stretchLoc+'.tx')
            mc.setAttr(stretchNode+'.input2', defaultDis)
            mc.connectAttr(stretchNode+'.output', stretchLoc+'.tx')

        # clean
        shape =  mc.listRelatives(stretchLoc, s=1)
        mc.hide(shape)

    # add stretch attr
    for i in range(ctrlNum):
        mc.addAttr(FkCtrls[i], ln='length',at='float',k=1, dv=1, min=0.01)
        mc.connectAttr(FkCtrls[i]+'.length', bridge+'.'+attrName[i])

    # create mpNode
    if not mpNode:
        mpNode = mc.createNode('transform', n=prefix+'stretchFk_noTrans')
        mc.hide(mpNode)

    mc.parent(bridge, mpNode)

    # match rx system
    if mc.objExists('noTransform'):
        mc.parent(mpNode, 'noTransform')

    return bridge    