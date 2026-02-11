import maya.cmds as mc
import maya.mel as mel

import controlTools
import templateTools
import rivet
import cluster
from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutPublic


# Create template ref rig for a spline Rig
def createTemplate(name, part, prefix='', numControls=4, numJoints=5, numFkCtrls=4, aim=1):

    # Create Joints.
    color = 'teal'
    joints = []
    for i in range(numJoints):
        jname = prefix+name+aboutName.letter(i)
        jnt = templateTools.createJoint(jname, part, color, pc=1, oc=0)# default color set
        mc.xform(jnt[0], ws=1,t=[0,i,0])
        aboutPublic.displaySet([jnt[-2]], display = 'reference')
        joints.append(jnt[-1])

    # Orient Joints.
    for i in range(1, numJoints):
        mc.aimConstraint(joints[i]+'_pos', joints[i-1], n=joints[i-1]+'_ac', aim=[0,aim,0], u=[0,0,1], wut='objectRotation', wuo=joints[i-1]+'_pos', wu=[0,0,1])
        # fixed pos jnt right axis to next one.
        mc.delete(mc.aimConstraint(joints[i]+'_pos_grp', joints[i-1]+'_pos_grp', aim=[0,aim, 0], u=[0,0,aim], wut='vector', wu=[0,0,1]) )
        mc.parent(joints[i], joints[i-1])

    #fixed end pos jnt axis.
    mc.delete(mc.orientConstraint(joints[-2]+'_pos_grp', joints[-1]+'_pos_grp'))

    # Create Loft and controls
    div = float(numJoints-1)/float(numControls-1)
    arg = 'curve -d 2 -n "'+prefix+name+'A_crv" '


    ctrls = []
    for i in range(numControls):
        #controls
        ctrl = controlTools.create(prefix+name+aboutName.letter(i)+'_crvPos', shape='C02_pole', color='yellow', scale=.7, jointCtrl=True, tag='splineTemp')
        mc.setAttr(ctrl[-1]+'.drawStyle', 0)
        mc.setAttr(ctrl[-1]+'.radi', 0.01)
        #set pos
        mc.xform(ctrl[0], ws=1, t=[0, i*div, 0])
        ctrls.append(ctrl[-1])
        arg+='-p 0.1 {0} 0 '.format(i*div)

    # Create nurb
    crvA = mel.eval(arg)
    crvB = mel.eval(arg.replace('-p 0.1','-p -0.1'))
    nurb = mc.loft( crvB, crvA, n=prefix+name+'_nurb',ch=0)[0]
    mc.delete(crvA, crvB)

    # add stretch system
    offsetInfo = createOffsetStretch(nurb, uv='u')
    nurbs = offsetInfo['nurbs']
    rbcs = offsetInfo['rbcs']
    cmd = offsetInfo['cmd']
    vmd = offsetInfo['vmd']

    # attach joints to nurb
    groupNodes = []
    for j in joints:
        groupNodes.append(j+'_pos_grp')
    rivet.surface(groupNodes, nurbs[0], part+'Nox')

    for j in joints:
        fll = j+'_pos_grp_fllShape'
        dv = mc.getAttr(fll+'.parameterU')
        mc.addAttr(j+'_pos', ln='paramU', at='double', min=0, max=10, dv=dv*10, k=1)
        mc.setDrivenKeyframe(fll+'.parameterU' , cd=j+'_pos.paramU', dv=dv*10, v=dv)
        mc.setDrivenKeyframe(fll+'.parameterU' , cd=j+'_pos.paramU', dv=10, v=1)
        mc.setDrivenKeyframe(fll+'.parameterU' , cd=j+'_pos.paramU', dv=0, v=0)

    # Cluster nurbs
    for i in range(len(ctrls)):
        cluster.create(['{0}.cv[0:3][{1}]'.format(nurbs[1], i), ctrls[i] ])

    # part hook
    mc.setAttr(rbcs[0] + '.spans', numFkCtrls-1)
    mc.setAttr(rbcs[1] + '.spans', numFkCtrls-1)

    # cleanup
    mc.parent(nurbs, part + 'Nox')
    mc.parent(groupNodes, part + 'Ctrls')

    for i in range(len(ctrls)):
        mc.parent(ctrls[i]+'_grp', part+'Ctrls')
        aboutLock.lock( [ ctrls[i]+'_grp', ctrls[i]+'_con', ctrls[i]+'_sdk', ctrls[i] ] )
        aboutLock.unlock(ctrls[i]+'_grp','t r')
        aboutLock.unlock(ctrls[i],'t')

    for i in range(len(joints)):
        aboutLock.lock( [ joints[i]+'_pos_grp', joints[i]+'_pos_axis', joints[i]+'_pos_con', joints[i]+'_pos_sdk', joints[i]+'_pos' ] )
        aboutLock.unlock(joints[i]+'_pos', at='paramU ro')

    mc.setAttr(cmd+'.stretch', 1)
    #displayTools.set('template', nodes=nurb)

    result = {'jointList':joints, 'ctrls':ctrls, 'nurb':nurbs[0]}
    return result


# creates stretchy spline rig
def createOffsetStretch(nurb, uv='u'):

    # start/
    # org nurb----->duplicate crv----->rebuild crv----->detach crv----->loft new nurb
    # end/

    # create bridge
    cbridge = nurb + '_stretch_cmd_bridge'
    if not mc.objExists(cbridge):
        mc.createNode('transform', n=cbridge)
        aboutLock.lock(cbridge)
        mc.addAttr(cbridge, ln='stretch', at='double', min=0, max=1, k=1)
        mc.addAttr(cbridge, ln='root', at='double', k=1, min=0, max=10)
        mc.addAttr(cbridge, ln='initScale', at='double', k=1, dv=1)

    # create bridge
    vbridge = nurb + '_stretch_value_bridge'
    if not mc.objExists(vbridge):
        mc.createNode('transform', n=vbridge)
        aboutLock.lock(vbridge)
        mc.addAttr(vbridge, k=1, ln='positive', at='double')
        mc.addAttr(vbridge, k=1, ln='negative' , at='double')


    #  create curves and loft for uniform stretch---------------------------------------------

    # duplicate curve from nurb
    crva=mc.duplicateCurve('{0}.{1}[0]'.format(nurb, uv), ch=1, rn=0, local=0, n=nurb+'_a_crv')
    crvb=mc.duplicateCurve('{0}.{1}[1]'.format(nurb, uv), ch=1, rn=0, local=0, n=nurb+'_b_crv')
    crva[1] = mc.rename(crva[1], nurb + '_a_cfs')
    crvb[1] = mc.rename(crvb[1], nurb + '_b_cfs')

    # rebuild curve double knots
    knots=len( mc.ls(crva[0]+'.cv[*]',fl=1) ) * 2
    rbcs1=mc.rebuildCurve(crva, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=knots, d=3, tol=0.01 )
    rbcs2=mc.rebuildCurve(crvb, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=knots, d=3, tol=0.01 )

    # rename rebuild node
    rbc1=mc.rename(rbcs1[1], rbcs1[0]+'_rbc')
    rbc2=mc.rename(rbcs2[1], rbcs2[0]+'_rbc')

    # set rebuild node smooth value
    mc.setAttr(rbc1 + '.smooth', 4)
    mc.setAttr(rbc2 + '.smooth', 4)

    # detach curve
    crvsA=mc.detachCurve(crva[0], p=(0.001, .999 ), ch=1, cos=1, rpo=0)
    crvsB=mc.detachCurve(crvb[0], p=(0.001, .999 ), ch=1, cos=1, rpo=0)

    # rename detach node
    detatchA=mc.rename(crvsA[3], crva[0]+'_detach')
    detatchB=mc.rename(crvsB[3], crvb[0]+'_detach')

    mc.delete(crvsA[0], crvsA[2], crvsB[0], crvsB[2])
    crvA=mc.rename(crvsA[1],crva[0]+'_loft_crv')
    crvB=mc.rename(crvsB[1],crvb[0]+'_loft_crv')

    # loft new nurb
    loftrb=mc.loft(crvA, crvB, n=(nurb+'_rebuild'), ch=1, c=0, ar=1, d=3, ss=2, rn=0, po=0, rsn=1)

    mc.parent(crva[0], crvb[0], crvA, crvB, cbridge, vbridge, nurb)
    mc.hide(crva[0], crvb[0], crvA, crvB, cbridge, vbridge)
    #----------------------------------------------------------------------------------------

    # ------------------------ Offset and Stretch ------------------------

    # add arclength node use for get length
    info = mc.arclen(crva[0], ch=1)
    info = mc.rename(info, crva[0]+'_arclen')

    # set range root value 0~10 to 0~1
    sr=mc.createNode('setRange', n= nurb+'_offset_str')
    mc.connectAttr(cbridge+'.root', sr+'.valueX')
    mc.setAttr(sr+'.oldMinX', 0)
    mc.setAttr(sr+'.oldMaxX', 10)
    mc.setAttr(sr+'.minX', 0)
    mc.setAttr(sr+'.maxX', 1)

    # get real crv length
    arcLenOrgScaleMdl = mc.createNode('multDoubleLinear', n=nurb+'_org_length_initScale_mdl')
    mc.setAttr(arcLenOrgScaleMdl + '.input1', mc.getAttr(info+'.arcLength'))
    mc.connectAttr(cbridge+'.initScale', arcLenOrgScaleMdl+'.input2')

    arcLenRealScaleMdl = mc.createNode('multDoubleLinear', n=nurb + '_real_length_initScale_mdl')
    mc.connectAttr(info + '.arcLength', arcLenRealScaleMdl + '.input1')
    mc.connectAttr(cbridge + '.initScale', arcLenRealScaleMdl + '.input2')

    if mc.attributeQuery('initScale', node='worldA_ctrl', ex=True):
        mc.connectAttr('worldA_ctrl.initScale', cbridge+'.initScale')


    # clamp crv length
    arcClamp=mc.createNode('clamp', n=nurb+'_length_cl')
    mc.connectAttr(arcLenOrgScaleMdl+'.output', arcClamp+'.minR')
    mc.setAttr(arcClamp+'.maxR', 100000000)
    mc.connectAttr(arcLenRealScaleMdl+'.output', arcClamp+'.inputR' )

    blendNode = mc.createNode('blendTwoAttr', n=nurb+'_real_length_bd')
    mc.connectAttr(cbridge+'.stretch', blendNode+'.attributesBlender')
    mc.connectAttr(arcLenOrgScaleMdl+'.output', blendNode + '.input[0]')
    mc.connectAttr(arcClamp+'.outputR', blendNode+'.input[1]')

    # get stretch proportion
    md=mc.createNode('multiplyDivide', n=nurb+'_length_proportion_md')
    mc.setAttr(md+'.operation', 2)
    mc.connectAttr(blendNode+'.output', md+'.input1X')
    mc.connectAttr(arcClamp+'.outputR', md+'.input2X')

    #store min and max offset values
    negativePma=mc.createNode('plusMinusAverage', n=nurb+'_negative_pma')
    mc.setAttr(negativePma+'.operation', 2)

    mc.setAttr(negativePma + '.input1D[0]', 1)
    mc.connectAttr(md+'.outputX', negativePma+'.input1D[1]')
    mc.connectAttr(md+'.outputX', vbridge+'.positive')
    mc.connectAttr(negativePma+'.output1D', vbridge+'.negative')

    #set ranges for min and Max
    minMaxSr=mc.createNode('setRange', n=nurb+'_minMaxValue_sr')
    mc.setAttr(minMaxSr + '.oldMaxX', 1)
    mc.setAttr(minMaxSr + '.oldMaxY', 1)

    mc.connectAttr(sr+'.outValueX', minMaxSr+'.valueX')
    mc.connectAttr(sr+'.outValueX', minMaxSr+'.valueY')

    mc.setAttr(minMaxSr + '.minX', 0)
    mc.connectAttr(vbridge+'.negative', minMaxSr+'.maxX')
    mc.connectAttr(vbridge+'.positive', minMaxSr+'.minY')
    mc.setAttr(minMaxSr+'.maxY', 1)

    mc.setAttr(cbridge+'.stretch', 1)
    cnd=mc.createNode('condition', n=nurb+'_nonUni_cnd')
    mc.connectAttr(cbridge+'.stretch', cnd+'.firstTerm')
    mc.setAttr(cnd+'.secondTerm', 1)
    mc.connectAttr(minMaxSr+'.outValueY', cnd+'.colorIfFalseR')
    mc.setAttr(cnd+'.colorIfTrueR', mc.getAttr( crva[0]+'Shape.maxValue'))

    mc.connectAttr(minMaxSr+'.outValueX', detatchA +'.parameter[0]')
    mc.connectAttr(minMaxSr+'.outValueX', detatchB +'.parameter[0]')
    mc.connectAttr(cnd+'.outColorR', detatchA +'.parameter[1]')
    mc.connectAttr(cnd+'.outColorR', detatchB +'.parameter[1]')

    mc.setAttr(cbridge+'.stretch', 0)

    mc.rename(nurb, nurb+'_input_org')
    mc.rename(loftrb[0], nurb+'_output_org')
    mc.hide(nurb + '_input_org')
    mc.hide(nurb + '_output_org')

    result = { 'nurbs':[nurb+'_output_org', nurb+'_input_org'], 'rbcs':[rbc1, rbc2], 'cmd':cbridge, 'vmd':vbridge }
    return result

#   Creates Distributed Twist
def createTwist(tctrls, tjnts):

    #create attrs
    numCtrls=len(tctrls)
    numJnts=len(tjnts)
    if not mc.objExists(tctrls[0]+'.baseTwist'):
        mc.addAttr(tctrls[0], ln='baseTwist',at='double', k=1)
    mc.addAttr(tctrls[-1], ln='endTwist',at='double', k=1)
    mc.addAttr(tctrls, ln='twist',at='double', k=1)

    # create ramps
    div=1.0 /(numCtrls-1)
    ramps=[]
    for i in range(numCtrls):

        pre=(i-1)*div
        post=(i+1)*div
        cDiv=i*div

        ramp=mc.createNode('ramp', n=tctrls[i]+'_ramp')

        mc.setAttr(ramp+'.colorEntryList[0].color', 0,0,0, type='double3')
        mc.setAttr(ramp+'.colorEntryList[1].color', 1,1,1,type='double3')
        mc.setAttr(ramp+'.colorEntryList[2].color', 0,0,0, type='double3')

        mc.setAttr(ramp+'.colorEntryList[0].position', max(min(1, pre), 0) )
        mc.setAttr(ramp+'.colorEntryList[1].position', cDiv)
        mc.setAttr(ramp+'.colorEntryList[2].position', max(min(1, post), 0))
        mc.setAttr(ramp+'.interpolation', 1)
        ramps.append(ramp)

    mc.removeMultiInstance(ramps[-1]+'.colorEntryList[2]', b=True)
    mc.removeMultiInstance(ramps[0]+'.colorEntryList[0]', b=True)

    # setup joint twist and Scale readers//
    div=1.0/( numJnts-1)
    crv=[]
    for i in range(numCtrls):
        for ji in range(numJnts):
            mc.setAttr(ramps[i]+'.vCoord',div*ji)
            value=mc.getAttr(ramps[i]+'.outColorR')

            mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[i]+'.twist', dv=0, v=0, ott='spline', itt='spline')
            mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[i]+'.twist', dv=1, v=value, ott='spline', itt='spline')

        # set infinity
        crv.extend(mc.listConnections(tctrls[i]+'.twist', type='animCurve') )

    mc.delete(ramps)

    #base twist
    for ji in range(numJnts):
        mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[0]+'.baseTwist', dv=0, v=0, ott='spline', itt='spline')
        mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[0]+'.baseTwist', dv=1, v=div*ji, ott='spline', itt='spline')

    #end twist
    for ji in reversed(range(numJnts)):
        mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[-1]+'.endTwist', dv=0, v=0, ott='spline', itt='spline')
        mc.setDrivenKeyframe(tjnts[ji]+'.ry', cd=tctrls[-1]+'.endTwist', dv=1, v=div*ji, ott='spline', itt='spline')

    # set infinity
    crv.extend(mc.listConnections(tctrls[0]+'.baseTwist', type='animCurve'))
    crv.extend(mc.listConnections(tctrls[-1]+'.endTwist', type='animCurve'))

    mc.selectKey(crv)
    mc.setInfinity( poi='linear', pri='linear')



# Creates Distributed Twist
def createSegScale(ctrls, jnts, attrs=['sx','sz']):

    numCtrls = len(ctrls)
    numJnts = len(jnts)

    # create ramps
    div = 1.0 /(numCtrls-1)
    ramps = []
    for i in range(numCtrls):

        pre =(i-1)*div
        post =(i+1)*div
        cDiv = i*div

        ramp = mc.createNode('ramp', n=ctrls[i]+'_ramp')
        ramps.append(ramp)

        mc.setAttr(ramp+'.colorEntryList[0].color', 0,0,0, type='double3')
        mc.setAttr(ramp+'.colorEntryList[1].color', 1,1,1,type='double3')
        mc.setAttr(ramp+'.colorEntryList[2].color', 0,0,0, type='double3')
        mc.setAttr(ramp+'.colorEntryList[0].position', max(min(1, pre), 0) )
        mc.setAttr(ramp+'.colorEntryList[1].position', cDiv)
        mc.setAttr(ramp+'.colorEntryList[2].position', max(min(1, post), 0))
        mc.setAttr(ramp+'.interpolation', 1)

    mc.removeMultiInstance(ramps[-1]+'.colorEntryList[2]', b=True)
    mc.removeMultiInstance(ramps[0]+'.colorEntryList[0]', b=True)

    # setup joint twist and Scale readers//
    div = 1.0 /(numJnts-1)
    crvs = []
    for i in range(numCtrls):
        for ji in range(numJnts):
            mc.setAttr(ramps[i]+'.vCoord', div*ji)
            value = mc.getAttr(ramps[i]+'.outColorR')
            for att in attrs:
                if not mc.objExists(ctrls[i]+'.sdk'+att):
                    mc.addAttr(ctrls[i], ln='sdk'+att, at='double')
                    mc.setDrivenKeyframe(ctrls[i]+'.sdk'+att, cd=ctrls[i]+'.'+att, dv=0, v=-1, itt='spline', ott='spline')
                    mc.setDrivenKeyframe(ctrls[i]+'.sdk'+att, cd=ctrls[i]+'.'+att, dv=1, v=0, itt='spline', ott='spline')
                    mc.setDrivenKeyframe(ctrls[i]+'.sdk'+att, cd=ctrls[i]+'.'+att, dv=2, v=1, itt='spline', ott='spline')

                mc.setDrivenKeyframe(jnts[ji]+'.'+att, cd=ctrls[i]+'.sdk'+att, dv=-1, v=-value, ott='spline', itt='spline')
                mc.setDrivenKeyframe(jnts[ji]+'.'+att, cd=ctrls[i]+'.sdk'+att, dv=0, v=0, ott='spline', itt='spline')
                mc.setDrivenKeyframe(jnts[ji]+'.'+att, cd=ctrls[i]+'.sdk'+att, dv=1, v=value, ott='spline', itt='spline')

        for att in attrs:
            crvs.extend(mc.listConnections(ctrls[i]+'.'+att, type='animCurve'))

        mc.delete(ramps)
        mc.selectKey(crvs)
        mc.setInfinity( poi='linear', pri='linear')
