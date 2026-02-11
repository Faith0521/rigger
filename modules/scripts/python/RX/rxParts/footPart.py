######################################
#   Rig Build Part
######################################
from importlib import reload
import maya.cmds as mc

import templateTools
import controlTools
from rxCore import aboutLock

reload(controlTools)

# Build Tempalte
def template(info, side='lf', prefix='', parent='', ikControl='', fkControl=''):

    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['ikControl'] = ikControl
    args['fkControl'] = fkControl

    # Args to lock once part is built
    #lockArgs=['numToes','numToeJoints']

    # Build template part topnode, get top node and prefix.
    '''
    info = templateTools.createTopNode(__name__, args, lockArgs)
    if not info:
        print ('Exiting... ')
        #return
    '''

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...

    # set mirror and color
    color = 'blue'
    mirror = 1
    if side =='rt':
        mirror = -1
        color = 'red'

    # Build a joint.
    ankle = templateTools.createJoint(prefix+'ankle', topnode, color)
    ball = templateTools.createJoint(prefix+'ball', topnode, color)
    ballEnd = templateTools.createJoint(prefix+'ballEnd', topnode, color)
    heel = templateTools.createJoint(prefix+'heel', topnode, color)

    mc.xform(ball[0], ws=1, t=[0,-1,1.4])
    mc.xform(ballEnd[0], ws=1, t=[0,-1,3])
    mc.xform(heel[0], ws=1, t=[0,-1, -1])

    # Parent joitns
    mc.parent(ball[-1], heel[-1], ankle[-1])
    mc.parent(ballEnd[-1], ball[-1])

    mc.parent(heel[0], ballEnd[-2])
    mc.parent(ball[0], heel[-2])

    mc.pointConstraint(ballEnd[-2], heel[-2], ball[0])

    mc.aimConstraint( ball[-2], ankle[-1], aim=[mirror,0,0], u=[0,mirror,0], wu=[0,1,0], wuo=topnode, wut='objectRotation')
    mc.aimConstraint( ballEnd[-2], ball[-1], aim=[mirror,0,0], u=[0,mirror,0], wu=[0,1,0], wuo=topnode, wut='objectRotation')
    mc.orientConstraint(ball[-1], heel[-1])
    mc.parent(ankle[0], ballEnd[0], topnode+'Ctrls')

    inPivCtrl = controlTools.create(prefix+'inPiv_pos', shape='locator', color=color, scale=.2, jointCtrl=True)
    outPivCtrl = controlTools.create(prefix+'outPiv_pos', shape='locator', color=color, scale=.2, jointCtrl=True)
    mc.parentConstraint(ball[-1], inPivCtrl[0])
    mc.parentConstraint(ball[-1], outPivCtrl[0])
    mc.parent(inPivCtrl[0], outPivCtrl[0], topnode+'Ctrls')
    mc.setAttr(inPivCtrl[1]+'.tz', mirror*-1.5)
    mc.setAttr(outPivCtrl[1]+'.tz', mirror*1.5)
    aboutLock.lock(inPivCtrl+outPivCtrl)
    aboutLock.unlock([inPivCtrl[-1], outPivCtrl[-1]], 'tx ty tz ry')

    # Create ctrls
    ballFkCtrl = controlTools.create(prefix+'ballFk_ctrl', shape='D07_circle', color=color, scale=1.5, jointCtrl=True)
    ballIkCtrl = controlTools.create(prefix+'ballIk_ctrl', shape='D07_circle', color=color, scale=1.5, jointCtrl=True)

    controlTools.rollCtrlShape(ballFkCtrl[-1], axis='z')
    controlTools.rollCtrlShape(ballIkCtrl[-1], axis='z')

    mc.parentConstraint(ball[-1], ballFkCtrl[0])
    mc.parentConstraint(ball[-1], ballIkCtrl[0])

    #Cleanup
    mc.parent(ballIkCtrl[0], topnode+'Ctrls')
    mc.parent(ballFkCtrl[0], topnode+'Ctrls')
    mc.parent(ballEnd[0], ankle[-2])

    if mc.objExists(parent):
        mc.pointConstraint(parent, ankle[0])
        mc.setAttr(ankle[-2]+'.drawStyle', 2)

    aboutLock.lock(ballFkCtrl+ballIkCtrl)
    aboutLock.unlock(ballFkCtrl[-1]+ballIkCtrl[-1], 't r s')

    aboutLock.lock(ankle[:-1]+heel[:-1]+ball[:-1]+ballEnd[:-1])
    aboutLock.unlock(ballEnd[-2], 't')
    aboutLock.unlock(ball[-2], 't')
    aboutLock.unlock(heel[-2], 'tx ty tz')
    aboutLock.lock(topnode, 'rx rz')

    mc.parent(ankle[-1], parent)


# Build Anim
# -----------------------------------------------------------------------------------------------------------------------------------------------

def anim( side, prefix, parent, ikControl, fkControl, limbSetCtrl):

        prefix = templateTools.getPrefix(side, prefix)

        ankle = prefix+'ankle_drv'
        ball = prefix+'ball_drv'
        ballEnd = prefix + 'ballEnd_drv'
        heel = prefix+'heel_drv'

        # set mirror and color
        color = 'blue'
        mirror = 1
        if side =='rt':
            mirror = -1
            color = 'red'

        # declare jnts
        drvJnts = [ ankle, ball, ballEnd, heel ]

        # fk jnts
        fkJnts=[]
        for i in range( len(drvJnts) ):
            jnt = drvJnts[i]
            if mc.objExists(jnt):
                fkJnt = mc.duplicate(jnt, n=jnt+'_fk', po=1)[0]
                fkJnts.append(fkJnt)
        fkJntsNum = len(fkJnts)       
        for i in range(fkJntsNum):
            mc.hide(fkJnts[i])
            if i!=0:
                mc.parent(fkJnts[i], fkJnts[i-1])
        mc.parent(fkJnts[-1], fkJnts[0])
                    
        # ik jnts
        ikJnts=[]
        for i in range( len(drvJnts) ):
            jnt = drvJnts[i]
            if mc.objExists(jnt):
                ikJnt = mc.duplicate(jnt, n=jnt+'_ik', po=1)[0]
                ikJnts.append(ikJnt)
        ikJntsNum = len(ikJnts)       
        for i in range(ikJntsNum):
            mc.hide(ikJnts[i])
            if i!=0:
                mc.parent(ikJnts[i], ikJnts[i-1])
        mc.parent(ikJnts[-1], ikJnts[0])

  
        #-----------------------------------------------------------------
        # match parent system
        #-----------------------------------------------------------------

        # parentIkJnt
        if mc.objExists(parent):
            parentIkJnt = parent.replace('_drv' , '_ik')

        # parentFkJnt
        if mc.objExists(parent):
            parentFkJnt = parent.replace('_drv' , '_fk')

        # parentIkCtrl
        parentIkCtrl = ikControl

        # parentIkHandle
        parentIkHandle = mc.listRelatives(parentIkCtrl, type='ikHandle')[0]

        # parentIkLocalCtrl
        parentIkLocalCtrl = parentIkCtrl.replace('_ctrl', 'Local_ctrl')

        # toeParentFkCtrl
        toeParentFkCtrl = fkControl 

        # ball and toe ctrls
        ballFkCtrl = controlTools.create(prefix+'ballFk_ctrl', snapTo=ball, useShape=prefix+'ballFk_ctrlPrep')
        ballIkCtrl = controlTools.create(prefix+'ballIk_ctrl', snapTo=ball, useShape=prefix+'ballIk_ctrlPrep')


        #--------------------------------------------------------------------------------------------------------------------------
        # Create movable pivot
        #--------------------------------------------------------------------------------------------------------------------------

        pivNode=mc.createNode('transform', p=ikControl+'_grp', n=prefix+'footPivots')
        mc.addAttr(ikControl, ln='footPivot', at='enum',k=1, en='ankle:heel:ball:toe:inner:outter:movable')

        pivGrp = mc.group(ikControl+'_con', n=ikControl+'_PivSys')
        mc.xform(pivGrp, os=1, piv=[0,0,0])

        pivNegGrp = mc.duplicate(pivGrp, n=ikControl+'_PivNegGrp', po=1)[0]
        pivNeg = mc.duplicate(pivGrp, n=ikControl+'_PivNeg', po=1)[0]
        
        mc.parent(pivNegGrp, parentIkLocalCtrl)
        mc.parent(pivNeg, pivNegGrp)
        
        md = mc.createNode('multiplyDivide', n=pivGrp+'_md')
        mc.setAttr(md+'.i2', -1,-1,-1)

        mc.connectAttr(pivGrp+'.t', md+'.i1')
        mc.connectAttr(md+'.o', pivNeg+'.t')

        bbox = mc.exactWorldBoundingBox(ikControl)
        size = [(((bbox[3]-bbox[0])+(bbox[4]-bbox[1])+(bbox[5]-bbox[2]))/3)*.5]*3

        pivCtrl = controlTools.create(ikControl+'Pivot', shape='jackThin', scale=size, color='cyan', makeGroups=0)
        pivCtrl = mc.rename(pivCtrl[0], ikControl+'Pivot')
        mc.parent(pivCtrl, pivNode)
        mc.setAttr(pivCtrl+'.t', 0,0,0)



        #---------------------------------------------------
        # create heel, toe, ball, in and outter pivots
        #---------------------------------------------------

        anklePos = mc.xform(ankle, q=1, ws=1, t=1)
        heelPos = mc.xform(heel, q=1, ws=1, t=1)
        ballPos = mc.xform(ball, q=1, ws=1, t=1)
        toePos = mc.xform(ballEnd, q=1, ws=1, t=1)
        inPos = mc.xform(prefix+'inPiv_pos_ctrlPrep', q=1, ws=1, t=1)
        outPos = mc.xform(prefix+'outPiv_pos_ctrlPrep', q=1, ws=1, t=1)

        anklePiv = mc.createNode('transform', n=prefix+'anklePiv', p=pivNode)
        heelPiv = mc.createNode('transform', n=prefix+'heelPiv', p=pivNode)
        ballPiv = mc.createNode('transform', n=prefix+'ballPiv', p=pivNode)
        toePiv = mc.createNode('transform', n=prefix+'toePiv', p=pivNode)
        inPiv = mc.createNode('transform', n=prefix+'inPiv', p=pivNode)
        outPiv = mc.createNode('transform', n=prefix+'outPiv', p=pivNode)

        mc.xform(anklePiv, ws=1, t=anklePos)
        mc.xform(heelPiv, ws=1, t=heelPos)
        mc.xform(ballPiv, ws=1, t=ballPos)
        mc.xform(toePiv, ws=1, t=toePos)
        mc.xform(inPiv, ws=1, t=inPos)
        mc.xform(outPiv, ws=1, t=outPos)

        # connect pivot
        nodes = [
                anklePiv,
                heelPiv,
                ballPiv,
                toePiv,
                inPiv,
                outPiv,
                pivCtrl]

        spc = mc.pointConstraint( nodes, pivGrp, n=pivGrp+'_pc')[0]

        for i in range(len(nodes)):
            mc.setDrivenKeyframe('{0}.w{1}'.format(spc, i), cd=ikControl+'.footPivot', dv=i-1, v=0)
            mc.setDrivenKeyframe('{0}.w{1}'.format(spc, i), cd=ikControl+'.footPivot', dv=i, v=1)
            mc.setDrivenKeyframe('{0}.w{1}'.format(spc, i), cd=ikControl+'.footPivot', dv=i+1, v=0)

        mc.setDrivenKeyframe(pivCtrl+'.v', cd=ikControl+'.footPivot', dv=len(nodes)-1, v=1)
        mc.setDrivenKeyframe(pivCtrl+'.v', cd=ikControl+'.footPivot', dv=len(nodes)-2, v=0)

        #---------------------------------------------------
        # DRV set
        #---------------------------------------------------
        #mc.parent(drvJnts[0], parent)

        #---------------------------------------------------
        # FK set
        #---------------------------------------------------
        mc.parentConstraint(ballFkCtrl[-1], fkJnts[1], n=fkJnts[1]+'_prc', mo=1)
        mc.parent(ballFkCtrl[0], toeParentFkCtrl)
        #mc.parent(fkJnts[0], parentParentFkJnt)


        #---------------------------------------------------
        # IK set
        # setup reverse foot
        #---------------------------------------------------
        #mc.parent(ikJnts[0], parentParentIkJnt)

        mc.addAttr(ikControl, ln='rollAngle', at='double', k=1, min=0, max=100, dv=25)
        mc.addAttr(ikControl, ln='roll', at='double', k=1, min=-5, max=10)
        mc.addAttr(ikControl, ln='sideRoll', at='double', k=1)
        mc.addAttr(ikControl, ln='toeLift', at='double', k=1)
        mc.addAttr(ikControl, ln='toe', at='double', k=1)
        mc.addAttr(ikControl, ln='ball', at='double', k=1)
        mc.addAttr(ikControl, ln='heel', at='double', k=1)
        mc.addAttr(ikControl, ln='toeTwist', at='double', k=1)
        mc.addAttr(ikControl, ln='ballTwist', at='double', k=1)
        mc.addAttr(ikControl, ln='heelTwist', at='double', k=1)

        # Create oriented top node
        revNode = mc.createNode('transform', n=prefix+'revFootPivots', p=parentIkLocalCtrl)

        # rev nodes
        ballTwistRev = mc.createNode('transform', n=ball+'TwistRev', p=revNode)
        inRev = mc.createNode('transform', n=prefix+'inFootRev', p=revNode)
        outRev = mc.createNode('transform', n=prefix+'outFootRev', p=revNode)
        heelRev = mc.createNode('transform', n=heel+'Rev', p=revNode)
        toeRev = mc.createNode('transform', n=ballEnd+'Rev', p=revNode)
        ballRev = mc.createNode('transform', n=ball+'Rev', p=revNode)
        ballRevNeg = mc.createNode('transform', n=ball+'RevNeg', p=revNode)
        toeFlopRev = mc.createNode('transform', n=ballEnd+'FlopRev', p=revNode)
        stretchRev = mc.createNode('transform', n=ballEnd+'StretchRev', p=revNode)

        mc.delete(mc.pointConstraint(ball, ballTwistRev))
        mc.delete(mc.pointConstraint(inPiv, inRev))
        mc.delete(mc.pointConstraint(outPiv, outRev))
        mc.delete(mc.pointConstraint(heel, heelRev))
        mc.delete(mc.pointConstraint(ballEnd, toeRev))
        mc.delete(mc.pointConstraint(ball, ballTwistRev))
        mc.delete(mc.pointConstraint(ball, toeFlopRev))
        mc.delete(mc.pointConstraint(ball, ballRev))
        mc.delete(mc.pointConstraint(ball, ballRevNeg))
        mc.delete(mc.pointConstraint(ankle, stretchRev))

        mc.parent(revNode, pivNeg)
        mc.parent(inRev, ballTwistRev)
        mc.parent(outRev, inRev)
        mc.parent(heelRev, outRev)
        mc.parent(toeRev, heelRev)
        mc.parent(ballRev, toeRev)
        mc.parent(ballRevNeg, ballRev)
        mc.parent(stretchRev, ballRevNeg)
        mc.parent(toeFlopRev, toeRev)
        mc.parent(ballIkCtrl[0], toeRev)

        # setup roll function
        mc.addAttr([ballRev, toeRev, heelRev], ln='roll', at='double', k=1)

        srn = mc.createNode('setRange', n=prefix+'footRoll_sr')
        mdln = mc.createNode('multDoubleLinear', n=prefix+'footAngleReverse_mdl')

        mc.connectAttr(ikControl+'.rollAngle', mdln+'.input1')
        mc.setAttr(mdln+'.input2', -1)
        mc.connectAttr(ikControl+'.rollAngle', srn+'.minX')

        mc.connectAttr( mdln+'.output', srn+'.maxY')
        mc.connectAttr( mdln+'.output', srn+'.maxZ')

        mc.connectAttr( ikControl+'.roll', srn+'.valueX' )
        mc.connectAttr( ikControl+'.roll', srn+'.valueY' )
        mc.connectAttr( ikControl+'.roll', srn+'.valueZ' )

        mc.setAttr(srn+'.oldMinX', -5)
        mc.setAttr(srn+'.oldMaxX', 0)
        mc.setAttr(srn+'.oldMinY', 0)
        mc.setAttr(srn+'.oldMaxY', 5)
        mc.setAttr(srn+'.oldMinZ', 5)
        mc.setAttr(srn+'.oldMaxZ', 10)

        mc.connectAttr(srn+'.outValueX', heelRev+'.roll')
        mc.connectAttr(srn+'.outValueY', ballRev+'.roll')
        mc.connectAttr(srn+'.outValueZ', toeRev+'.roll')
    
        
        # key fwd roll
        mc.setDrivenKeyframe(heelRev+'.rz', cd = heelRev+'.roll', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(heelRev+'.rz', cd = heelRev+'.roll', dv=0, v=0, ott='spline', itt='spline')        
        mc.setDrivenKeyframe(ballRev+'.rz', cd = ballRev+'.roll', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(ballRev+'.rz', cd = ballRev+'.roll', dv=0, v=0, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rz', cd = toeRev+'.roll', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rz', cd = toeRev+'.roll', dv=0, v=0, ott='spline', itt='spline')

        # key side roll
        mc.setDrivenKeyframe(inRev+'.ry', cd = ikControl+'.sideRoll', dv=360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(inRev+'.ry', cd = ikControl+'.sideRoll', dv=0, v=0, ott='spline', itt='spline')
        mc.setDrivenKeyframe(outRev+'.ry', cd = ikControl+'.sideRoll', dv=-360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(outRev+'.ry', cd = ikControl+'.sideRoll', dv=0, v=0, ott='spline', itt='spline')

        # key toe lift
        mc.setDrivenKeyframe(toeRev+'.rz', cd = ikControl+'.toeLift', dv=-360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rz', cd = ikControl+'.toeLift', dv=360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rz', cd = ikControl+'.toeLift', dv=0, v=0, ott='spline', itt='spline')

        # key toe
        mc.setDrivenKeyframe(toeFlopRev+'.rz', cd = ikControl+'.toe', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeFlopRev+'.rz', cd = ikControl+'.toe', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeFlopRev+'.rz', cd = ikControl+'.toe', dv=0, v=0, ott='spline', itt='spline')

        # key ball
        mc.setDrivenKeyframe(ballRev+'.rz', cd = ikControl+'.ball', dv=-360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(ballRev+'.rz', cd = ikControl+'.ball', dv=360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(ballRev+'.rz', cd = ikControl+'.ball', dv=0, v=0, ott='spline', itt='spline')

        # key heel
        mc.setDrivenKeyframe(heelRev+'.rz', cd = ikControl+'.heel', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(heelRev+'.rz', cd = ikControl+'.heel', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(heelRev+'.rz', cd = ikControl+'.heel', dv=0, v=0, ott='spline', itt='spline')

        # key ball twist
        mc.setAttr(ballTwistRev+'.ro', 1)
        mc.setDrivenKeyframe(ballTwistRev+'.rx', cd = ikControl+'.ballTwist', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(ballTwistRev+'.rx', cd = ikControl+'.ballTwist', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(ballTwistRev+'.rx', cd = ikControl+'.ballTwist', dv=0, v=0, ott='spline', itt='spline')

        # key ball twist
        mc.setDrivenKeyframe(toeRev+'.rx', cd = ikControl+'.toeTwist', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rx', cd = ikControl+'.toeTwist', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(toeRev+'.rx', cd = ikControl+'.toeTwist', dv=0, v=0, ott='spline', itt='spline')

        # key heel twist
        mc.setAttr(heelRev+'.ro', 1)
        mc.setDrivenKeyframe(heelRev+'.rx', cd = ikControl+'.heelTwist', dv=-360, v=-360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(heelRev+'.rx', cd = ikControl+'.heelTwist', dv=360, v=360, ott='spline', itt='spline')
        mc.setDrivenKeyframe(heelRev+'.rx', cd = ikControl+'.heelTwist', dv=0, v=0, ott='spline', itt='spline')
        
        # Setup ik
        ballIk = mc.ikHandle(sj=ikJnts[0], ee=ikJnts[1], n=ball+'_ikh', sol='ikSCsolver', s='sticky')[0]
        toeIk = mc.ikHandle(sj=ikJnts[1], ee=ikJnts[2], n=ikJnts[2]+'_ikh', sol='ikSCsolver', s='sticky')[0]

 

        #------------------------------------
        # IKFK Switch
        #------------------------------------

        footSetCtrl = mc.createNode('transform', n=prefix+'footSet_ctrl')
        mc.addAttr(footSetCtrl, ln='IKFK',at='double', dv=1,min=0,max=1,k=1)
        mc.connectAttr(limbSetCtrl+'.IKFK', footSetCtrl+'.IKFK')
        mc.parent(footSetCtrl, limbSetCtrl)

        # modify position
        junk = mc.ls(limbSetCtrl+'_grp*', type='parentConstraint')
        if junk:
            mc.delete(junk)

        mc.setAttr(limbSetCtrl+'.ty', 0)
        mc.parentConstraint(ballEnd, limbSetCtrl+'_grp', n=limbSetCtrl+'_grp_prc')
        refDis = abs( mc.getAttr(ballEnd+'.tx') )
        mc.setAttr(limbSetCtrl+'.tx', 0.4*refDis*mirror)


        switchNode = mc.createNode('remapValue', n= prefix+'footSwitchIKFK_rv')
        mc.connectAttr( footSetCtrl+'.IKFK', switchNode+'.inputValue')
        mc.setAttr( switchNode+'.outputMin', 1)
        mc.setAttr( switchNode+'.outputMax', 0)

        # Switch IKFK DRV constraint weights
        jntNum = len(drvJnts)
        for i in range(jntNum):
            prc = mc.parentConstraint(ikJnts[i], fkJnts[i], drvJnts[i], n=drvJnts[i]+'_prc', mo=1)[0]
            mc.connectAttr( footSetCtrl+'.IKFK', prc+'.'+ikJnts[i]+'W0')
            mc.connectAttr( switchNode+'.outValue',  prc+'.'+fkJnts[i]+'W1')

        mc.addAttr(ballIkCtrl[3], ln='IK',at='float', min=0.0, max=1.0, k=1, hidden=False)
        mc.connectAttr(footSetCtrl+'.IKFK', ballIk+'.ikBlend')
        mc.connectAttr(footSetCtrl+'.IKFK', toeIk+'.ikBlend')
        mc.hide(ballIk, toeIk)

        
        #------------------------------------
        # clean
        #------------------------------------
        mc.parent(parentIkHandle, ballRevNeg)
        mc.parent(ballIkCtrl[0], toeFlopRev)
        mc.parent(ballIk, ballRevNeg)
        mc.parent(toeIk, ballIkCtrl[-1])

        controlTools.tagKeyable(parentIkCtrl, 'ballTwist heelTwist toeTwist footPivot rollAngle roll sideRoll toeLift toe ball heel', add=1)
        controlTools.tagKeyable(ballFkCtrl[-2:], 'r')
        controlTools.tagKeyable(ballIkCtrl[-1], 'loStretch space', add=1)

        result = {'ankle':ankle, 'ball':ball, 'ballEnd':ballEnd, 'heel':heel, 'stretchRev':stretchRev}
        return result
        