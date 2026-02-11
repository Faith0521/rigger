#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.11.26
#========================================

######################################
#   Rig Build Part
######################################
from importlib import reload
def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from rxUi.pyside2 import hand_ui
        return QtCore, QtGui, QtWidgets, hand_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from rxUi.pyside6 import hand_ui
            return QtCore, QtGui, QtWidgets, hand_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets, hand_ui = get_pyside_module()

import maya.cmds as mc
import maya.mel as mel

import re
import random
import os
import shutil

import templateTools
import controlTools

from rxCore import aboutPublic
from rxCore import aboutName
from rxCore import aboutLock
from rxCore import aboutUI
import assetCommon
import spaceTools
import assetEnv


# Build Tempalte
def template(side='lf', prefix='', parent='lf_wrist', control=['new'], numFingers=4, numFingerJoints=4, createThumb=True, ikFingers=False):

    # Arg values to be recorded.
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['control'] = control
    args['numFingers'] = numFingers
    args['numFingerJoints'] = numFingerJoints
    args['createThumb'] = createThumb
    args['ikFingers'] = ikFingers

    # Args to lock once part is built
    lockArgs=[ 'numFingers', 'control', 'numFingerJoints', 'createThumb', 'ikFingers']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('hand', args, lockArgs)
    if not info:
        print ('Exiting... ')
        return

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...
    tokens=['index', 'middle', 'ring', 'pinky']
    colors=['blue', 'blue', 'blue', 'blue']
    fingerNames = []

    mirror = 1
    if side == 'rt':
         colors = ['red','red','red','red']
         mirror = -1

    for i in range(numFingers):
        if i<4:
            fingerNames.append(prefix+tokens[i])
        else:
            fingerNames.append(prefix+'finger'+aboutName.letter(i))
            colors.append(colors[random.randrange(0,3)])

    # Create all fingers
    fingers = []
    for i in range(len(fingerNames)):
        finger = createFinger(fingerNames[i], topnode, numFingerJoints, colors[i], mirror=mirror, ikFingers=ikFingers)
        mc.xform(finger, ws=1, t=[mirror*.1, 0, -i*.5])
        fingers.append(finger)

    tmp = mc.createNode('transform')
    mc.delete(mc.pointConstraint(fingers, tmp))
    mc.parent(fingers, tmp)

    mc.delete(mc.pointConstraint(topnode, tmp))
    mc.parent(fingers, topnode+'Ctrls')
    mc.xform(fingers, r=1, t=[mirror*.4,0,0])
    mc.delete(tmp)

    if control[0] == 'new':
        ctrl = controlTools.create(prefix+'fingers_ctrl', shape='C00_sphere', color=colors[0], scale=.5, jointCtrl=True)
        mc.parent(ctrl[0], topnode+'Ctrls')
        aboutLock.lock(ctrl)
        aboutLock.unlock(ctrl[-1], 't r s')


    # Create thumb
    if createThumb:
        thumb = createFinger(prefix+'thumb', topnode, numFingerJoints-1, colors[-1], mirror=mirror, ikFingers=ikFingers)
        mc.delete(mc.pointConstraint(fingers[0], thumb))
        mc.xform(thumb, r=1, t=[-mirror, -.5,.3])
        mc.xform(thumb, a=1, ro=[0, -mirror*45,0])

    aboutLock.unlock(topnode+'Ctrls')
    mc.parent(topnode+'Ctrls', w=1)
    aboutLock.unlock(topnode+'Joints')
    mc.parent(topnode+'Joints', w=1)
    controlTools.rollCtrlShape(topnode, axis='z')
    mc.parent(topnode+'Ctrls', topnode+'Joints', topnode)
    aboutLock.lock(topnode+'Ctrls', topnode+'Joints')

    mc.setAttr(topnode+'.s',  .5,.5,.5)
    if mc.objExists(parent):
        mc.delete(mc.parentConstraint(parent, topnode))

    return True

def createFinger(name, topnode, numFingerJoints, color, mirror=1, ikFingers=False):

    # Create joints
    joints = []
    for i in range(numFingerJoints + 1):
        if i == 0:
            # the first finger named "Base"
            ltr = 'Base'
        elif i == numFingerJoints:
            # the last finger named "End"
            ltr = 'End'
        else:
            ltr = aboutName.letter(i-1)

        joint = templateTools.createJoint(name+ ltr, topnode, color, makeGroups=True, ctrlOnly=False, pc=1, oc=0)
        mc.setAttr(joint[0]+'.tx', mirror*i)
        joints.append(joint[-1])

    mc.parent(joints[0]+'_pos_grp', topnode+'Ctrls')

    for i in range(1, len(joints)):
        mc.parent(joints[i], joints[i-1])

        # base
        #   --A : axisCrv
        #       --B
        #       --C
        #       --End

        if i==1:
            mc.parent(joints[i]+'_pos_grp', joints[0] + '_pos')
        elif i>1:
            mc.parent(joints[i] + '_pos_grp', joints[1] + '_pos')

        mc.aimConstraint( joints[i]+'_pos', joints[i-1], n=joints[i-1]+'_ac', aim=[mirror,0,0], u=[0,0,1], wu=[0,0,1], wut='objectRotation', wuo=joints[i-1]+'_pos')

        aboutLock.lock([joints[i]+'_pos_grp', joints[i]+'_pos_con', joints[i]+'_pos_sdk', joints[i]+'_pos'])
        aboutLock.unlock(joints[i]+'_pos', 't r')

        # Create ctrl
        ctrl = controlTools.create(joints[i-1]+'_ctrl', shape='D07_circle', color=color, scale=1, jointCtrl=True)
        mc.parent(ctrl[0], topnode+'Ctrls')
        controlTools.rollCtrlShape(ctrl[-1], axis='z')
        mc.parentConstraint(joints[i-1], ctrl[0], n=ctrl[0] + '_prc')
        aboutLock.lock(ctrl)
        aboutLock.unlock(ctrl[-1], 't r s')

        if ikFingers:
            ctrl = controlTools.create(name+'Ik_ctrl', shape='C01_cube', color=color, scale=.5, jointCtrl=True)
            mc.parent(ctrl[0], topnode+'Ctrls')
            mc.parentConstraint(joints[-1], ctrl[0], n=ctrl[0]+'_prc')
            aboutLock.lock(ctrl)
            aboutLock.unlock(ctrl[-1], 't r s')

    aboutLock.lock([ joints[0]+'_pos_con', joints[0]+'_pos_sdk', joints[0]+'_pos'])
    aboutLock.unlock(joints[0]+'_pos', 't r')

    # finger upper axis displate curve.
    axisCrv = mel.eval('curve -d 1 -p 0 -1 0 -p 0 0 0 -p 0 1 0 -k 0 -k 1 -k 2 ;')
    axisCrv = mc.rename(axisCrv, joints[1]+'_axis')
    mc.parentConstraint(joints[1], axisCrv, mo=False, n=axisCrv+'_prc')
    mc.parent(axisCrv, topnode+'Ctrls')
    mc.select(axisCrv)
    aboutPublic.displaySet([axisCrv],'reference')

    return joints[0]+'_pos_grp'

# Build Anim
def anim():
    #numFingers  ['index', 'middle', 'ring', 'pinky']
    #fingerNames ['lf_index', 'lf_middle', 'lf_ring', 'lf_pinky']

    parts = templateTools.getParts('hand')
    for part in parts:

        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        control = templateTools.getArgs(part, 'control')[0]
        numFingerJoints = templateTools.getArgs(part, 'numFingerJoints')
        numFingers = templateTools.getArgs(part, 'numFingers')
        createThumb = templateTools.getArgs(part, 'createThumb')
        ikFingers = templateTools.getArgs(part, 'ikFingers')

        prefix = templateTools.getPrefix(side, prefix)

        # Template Build Code...
        tokens=['index', 'middle', 'ring', 'pinky']
        colors=['green','grass','turquoise','forestGreen']
        fingerNames = []
        thumb = []

        if createThumb:
            thumb=[prefix+'thumb']

        mirror = 1
        if side == 'rt':
             colors = ['red','lightPurple','violet', 'darkMagenta']
             mirror = -1

        for i in range(numFingers):
            if i<4:
                fingerNames.append(prefix+ tokens[i])
            else:
                fingerNames.append(prefix+ 'finger'+aboutName.letter(i))
                colors.append(colors[random.randrange(0,3)])

        if control == 'new':
            control = controlTools.create(prefix+'fingers_ctrl', snapTo=prefix+'fingers_ctrlPrep', useShape=prefix+'fingers_ctrlPrep')[-1]
            controlTools.tagKeyable(control, 'fkFingerDisplay spread fist cup reverseCup', add=0)
        else:
            controlTools.tagKeyable(control, 'fkFingerDisplay spread fist cup reverseCup', add=1)

        # Create all finger attrs
        mc.addAttr(control, ln='fkFingerDisplay', at='long', min=0, dv=0, max=1, k=1)
        mc.addAttr(control, ln='spread', at='double', k=1)
        mc.addAttr(control, ln='fist', at='double', k=1)
        mc.addAttr(control, ln='cup', at='double', k=1)
        mc.addAttr(control, ln='reverseCup', at='double', k=1)
        mc.addAttr(control, ln='thumbCurl', at='double', k=1)
        mc.addAttr(control, ln='indexCurl', at='double', k=1)
        mc.addAttr(control, ln='middleCurl', at='double', k=1)
        mc.addAttr(control, ln='ringCurl', at='double', k=1)
        mc.addAttr(control, ln='pinkyCurl', at='double', k=1)

        # FK
        allOrgJoints = []
        allDrvJoints = []
        fkctrls = {}

        for name in fingerNames+thumb:
            ctrls = []
            for i in range(numFingerJoints):
                if i == 0:
                    ltr = 'Base'
                else:
                    ltr = aboutName.letter(i-1)

                orgjnt = name+ltr
                drvjnt = name + ltr + '_drv'

                if mc.objExists(drvjnt):

                    allOrgJoints.append(orgjnt)
                    allDrvJoints.append(drvjnt)

                    ctrl = controlTools.create(orgjnt+'_ctrl', snapTo=orgjnt, useShape=orgjnt+'_ctrlPrep')
                    mc.parentConstraint(ctrl[-1], drvjnt, n=drvjnt+'_prc')

                    if ctrls:
                        mc.parent(ctrl[0], ctrls[-1])
                    ctrls.append(ctrl[-1])
                    controlTools.tagKeyable(ctrl[-2:], 'ty r')

            # mc.parentConstraint(parent, ctrls[0]+'_grp', n=ctrls[0]+'_grp_prc', mo=1)
            mc.connectAttr(control+'.fkFingerDisplay', ctrls[0]+'_grp.v')
            mc.parent(ctrls[0]+'_grp', control)
            fkctrls[name] = ctrls+[name+'Ik_ctrl']

        # IK
        if ikFingers:
            for name in fingerNames+thumb:

                drvjnts = []
                for i in range(numFingerJoints):
                    ltr = 'Base'
                    if i > 0:
                        ltr = aboutName.letter(i-1)
                    if mc.objExists(name+ltr):
                        drvjnts.append(name+ltr+'_drv')
                if mc.objExists(name+'End'):
                    drvjnts.append(name+'End'+'_drv')

                for j in drvjnts:
                    mc.setAttr(j+'.preferredAngleZ', -45)

                ikCtrl = controlTools.create(name+'Ik_ctrl', snapTo=drvjnts[-1], useShape=name+'Ik_ctrlPrep')
                ikAHnd = mc.ikHandle(sj=drvjnts[1], ee=drvjnts[-2], sol='ikSCsolver', n=name+'_ik')
                ikBHnd = mc.ikHandle(sj=drvjnts[-2], ee=drvjnts[-1], sol='ikSCsolver', n=name+'Tip_ik')
                mc.parent(ikAHnd[0], ikBHnd[0], ikCtrl[-1])

                mc.addAttr(ikCtrl[-1], ln='IK', at='double', min=0, max=1, k=1)
                mc.connectAttr(ikCtrl[-1]+'.IK', ikAHnd[0]+'.ikBlend')
                mc.connectAttr(ikCtrl[-1]+'.IK', ikBHnd[0]+'.ikBlend')
                mc.hide(ikAHnd, ikBHnd)
                controlTools.tagKeyable(ikCtrl[-2:], 't r IK')

                spaceTools.tag(ikCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls world:noTransform'.format(parent))
                #tagTools.tagIkSnap(fkctrls[name], name, 'hand')
                mc.parent(ikCtrl[0], 'controls')

        # pose ctrl
        attrs = ['spread','fist','cup','reverseCup', 'thumbCurl', 'indexCurl', 'middleCurl', 'ringCurl', 'pinkyCurl']
        for attr in attrs:
            for jnt in allOrgJoints:
                # add attrs
                mc.addAttr(jnt+'_ctrl', ln=attr+'X', at='double',k=0)
                mc.addAttr(jnt+'_ctrl', ln=attr+'Y', at='double',k=0)
                mc.addAttr(jnt+'_ctrl', ln=attr+'Z', at='double',k=0)

                # create md
                md=mc.createNode('multiplyDivide', n =jnt+'_'+attr+'_md')
                mc.connectAttr(jnt+'_ctrl.'+attr+'X', md+'.input1X')
                mc.connectAttr(jnt+'_ctrl.'+attr+'Y', md+'.input1Y')
                mc.connectAttr(jnt+'_ctrl.'+attr+'Z', md+'.input1Z')

                mc.connectAttr(control+'.'+attr, md+'.input2X')
                mc.connectAttr(control+'.'+attr, md+'.input2Y')
                mc.connectAttr(control+'.'+attr, md+'.input2Z')

                for axis in ['x','y','z']:
                    mc.setDrivenKeyframe(jnt+'_ctrl_con.r'+axis, cd=md+'.output'+axis.upper(), itt='spline', ott='spline', dv=0, v=0)
                    mc.setDrivenKeyframe(jnt+'_ctrl_con.r'+axis, cd=md+'.output'+axis.upper(), itt='spline', ott='spline', dv=10, v=1)

                crv=mc.listConnections(md, type='animCurve', scn=1)
                mc.selectKey(crv, k=1)
                mc.setInfinity( pri='linear', poi='linear' )

        assetCommon.bindSet(allDrvJoints)

        # Set defaults

        spreadVals = []
        cupVals = []
        revCupVals = []

        if numFingers == 1:
            spreadVals = [0]
            cupVals = [-60]
            revCupVals = list(cupVals)
            revCupVals.reverse()

        elif numFingers == 2:
            spreadVals = [30, -30]
            cupVals = [0, -60]
            revCupVals = list(cupVals)
            revCupVals.reverse()

        elif numFingers == 3:
            spreadVals = [30, 0, -30]
            cupVals = [0, -30, -60]
            revCupVals = list(cupVals)
            revCupVals.reverse()

        elif numFingers >= 4:
            spreadVals = [30, 10, -10, -30]
            cupVals = [0, -20, -40, -60]
            revCupVals = list(cupVals)
            revCupVals.reverse()

        # x y z

        for i in range(len(fingerNames)):
            if i > 3:
                spreadVals.append(-30)
                cupVals.append(-60)
                revCupVals = list(cupVals)
                revCupVals.reverse()

            # set finger base default value
            # ctrl = fingerNames[i]+'Base_ctrl'
            # if mc.objExists(ctrl):
            #     mc.setAttr(ctrl+'.cupY', cupVals[i]*.3)
            #     mc.setAttr(ctrl+'.reverseCupY', -revCupVals[i]*.3)

            ctrl = fingerNames[i]+'A_ctrl'
            if mc.objExists(ctrl):
                mc.setAttr(ctrl+'.spreadY', -spreadVals[i])

            for ii in range(0, numFingerJoints):
                ltr = aboutName.letter(ii)
                ctrl = fingerNames[i] + ltr + '_ctrl'

                if mc.objExists(ctrl):
                    mc.setAttr(ctrl+'.cupZ', cupVals[i])
                    mc.setAttr(ctrl+'.reverseCupZ', revCupVals[i])
                    mc.setAttr(ctrl+'.fistZ', -89)

        # set thumb
        if createThumb:
            ctrl = thumb[0]+'Base_ctrl'
            if mc.objExists(ctrl):
                mc.setAttr(ctrl+'.fistZ', -60)
                mc.setAttr(ctrl+'.fistY', -30)

            for ii in range(0, numFingerJoints):
                ltr = aboutName.letter(ii)
                ctrl = thumb[0] + ltr + '_ctrl'

                if mc.objExists(ctrl):
                    mc.setAttr(ctrl+'.fistZ', -60)

        # connect with torso
        connectInLoc = parent + '_connect_loc'
        if mc.objExists(connectInLoc):

            # clear org constraint node.
            mc.select(control+'_grp')
            mel.eval("DeleteConstraints;")

            # connect with wrist part.
            mc.parentConstraint(connectInLoc, control+'_grp', n=control+'_grp' + '_prc', mo=1)

        # Clean Up
        # ---------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'hand_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        ctrlNeedP = [control+'_grp']
        for ctrl in ctrlNeedP:
            mc.parent(ctrl, ctrlNeedP)


def buildPose():
    """
    # custom finger pose by attributes
    :return:
    """
    ctrl = mc.ls(sl=1)[0]
    prefix = ctrl.replace('fingers_ctrl','')

    if mc.objExists(ctrl+'.spread') and mc.objExists(ctrl+'.fist') and mc.objExists(ctrl+'.cup') and mc.objExists(ctrl+'.reverseCup') and mc.objExists(ctrl+'.indexCurl') and mc.objExists(ctrl+'.middleCurl') and mc.objExists(ctrl+'.ringCurl') and mc.objExists(ctrl+'.pinkyCurl') and mc.objExists(ctrl+'.thumbCurl') :
        poses = aboutPublic.getChannelBox()

        if poses:
            pose = poses[0]
            if re.match(pose, 'spread') or re.match(pose, 'fist') or re.match(pose, 'cup') or re.match(pose, 'reverseCup') or mc.objExists(ctrl+'.indexCurl') or mc.objExists(ctrl+'.middleCurl') or mc.objExists(ctrl+'.ringCurl') or mc.objExists(ctrl+'.pinkyCurl') or mc.objExists(ctrl+'.thumbCurl') :
                ctrls = mc.ls( prefix+'thumb*_ctrl',
                                prefix+'index*_ctrl',
                                prefix+'middle*_ctrl',
                                prefix+'ring*_ctrl',
                                prefix+'pinky*_ctrl',
                                prefix+'finger*_ctrl' )

                for ct in ctrls:
                    if mc.objExists(ct+'.'+pose+'X'):
                        mc.setAttr(ct+'.'+pose+'X',(mc.getAttr(ct+'.rx')))
                    if mc.objExists(ct+'.'+pose+'Y'):
                        mc.setAttr(ct+'.'+pose+'Y',(mc.getAttr(ct+'.ry')))
                    if mc.objExists(ct+'.'+pose+'Z'):
                        mc.setAttr(ct+'.'+pose+'Z',(mc.getAttr(ct+'.rz')))
                    mc.xform(ct, a=1,ro=[0,0,0])
                mc.select(ctrl)

def rebuildPose():
    """
    # rebuild finger pose by attributes
    :return:
    """
    ctrl = mc.ls(sl=1)[0]
    prefix = ctrl.replace('fingers_ctrl','')

    if mc.objExists(ctrl+'.spread') and mc.objExists(ctrl+'.fist') and mc.objExists(ctrl+'.cup') and mc.objExists(ctrl+'.reverseCup'):
        poses = aboutPublic.getChannelBox()

        if poses:
            pose = poses[0]
            if re.match(pose, 'spread') or re.match(pose, 'fist') or re.match(pose, 'cup') or re.match(pose, 'reverseCup') or mc.objExists(ctrl+'.indexCurl') or mc.objExists(ctrl+'.middleCurl') or mc.objExists(ctrl+'.ringCurl') or mc.objExists(ctrl+'.pinkyCurl') or mc.objExists(ctrl+'.thumbCurl') :
                ctrls = mc.ls( prefix+'thumb*_ctrl',
                                prefix+'index*_ctrl',
                                prefix+'middle*_ctrl',
                                prefix+'ring*_ctrl',
                                prefix+'pinky*_ctrl',
                                prefix+'finger*_ctrl' )

                mc.setAttr(ctrl+'.spread', 0)
                mc.setAttr(ctrl+'.fist', 0)
                mc.setAttr(ctrl+'.cup', 0)
                mc.setAttr(ctrl+'.reverseCup', 0)

                for ct in ctrls:
                    if mc.objExists(ct+'.'+pose+'X'):
                        mc.setAttr(ct+'.rx',(mc.getAttr(ct+'.'+pose+'X')))
                    if mc.objExists(ct+'.'+pose+'Y'):
                        mc.setAttr(ct+'.ry',(mc.getAttr(ct+'.'+pose+'Y')))
                    if mc.objExists(ct+'.'+pose+'Z'):
                        mc.setAttr(ct+'.rz',(mc.getAttr(ct+'.'+pose+'Z')))
                mc.select(ctrls)

def mirrorPose():
    """
    # mirror finger pose by attributes, before mirror, you need selected lf/rt finger controls both.
    :return:
    """
    nodes = mc.ls(sl=1)
    prefix = nodes[0].replace('fingers_ctrl','')
    mprefix = nodes[1].replace('fingers_ctrl','')

    poses = ['spread', 'fist', 'cup', 'reverseCup', 'thumbCurl', 'indexCurl', 'middleCurl', 'ringCurl', 'pinkyCurl']
    for pose in poses:

        ctrls = mc.ls( prefix+'thumb*_ctrl',
                        prefix+'index*_ctrl',
                        prefix+'middle*_ctrl',
                        prefix+'ring*_ctrl',
                        prefix+'pinky*_ctrl',
                        prefix+'finger*_ctrl' )

        for ct in ctrls:
            mct = ct.replace(prefix, mprefix)
            if mc.objExists(mct+'.'+pose+'X'):
                mc.setAttr(mct+'.'+pose+'X', mc.getAttr(ct+'.'+pose+'X'))
            if mc.objExists(mct+'.'+pose+'Y'):
                mc.setAttr(mct+'.'+pose+'Y', mc.getAttr(ct+'.'+pose+'Y'))
            if mc.objExists(mct+'.'+pose+'Z'):
                mc.setAttr(mct+'.'+pose+'Z', mc.getAttr(ct+'.'+pose+'Z'))
    mc.select(nodes[1])

def exportPose():
    """
    # Export finger pose to assets env "handPoses.py"
    :return:
    """
    # get nodes
    poses = ['spread','fist','cup','reverseCup', 'thumbCurl', 'indexCurl', 'middleCurl', 'ringCurl', 'pinkyCurl']
    jnts = mc.ls( '*thumb*_ctrl',
    '*index*_ctrl',
    '*middle*_ctrl',
    '*ring*_ctrl',
    '*pinky*_ctrl',
    '*finger*_ctrl' )

    nodes = []
    for j in jnts:
        for p in poses:
            if mc.objExists(j+'.'+p+'X'):
                nodes.append(j+'.'+p+'X')
            if mc.objExists(j+'.'+p+'Y'):
                nodes.append(j+'.'+p+'Y')
            if mc.objExists(j+'.'+p+'Z'):
                nodes.append(j+'.'+p+'Z')

    if not nodes:
        mc.warning('No hands in scene.')
        return
    arg = '# Load finger sttings\nimport maya.cmds as mc\n\n'
    arg += 'def load():\n'

    for n in nodes:
        arg+="    try:\n"
        arg+="        mc.setAttr('{0}', {1})\n".format(n, mc.getAttr(n))
        arg+="    except:\n"
        arg+="        mc.warning('Could not load tag: {0}')\n".format(n)

    filename = os.path.join(assetEnv.getpath(), 'build', 'scripts', 'handPoses.py')

    if os.path.isfile(filename):
        result = mc.confirmDialog( title='Overwrite Hand Poses File?',
                                   message='handPoses.py already exists.\nOverwrite file?\n\n'+filename,
                                   button=['Yes','No'],
                                   defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return

        shutil.copyfile(filename, filename+'.bak')

    f = open(filename, 'w')
    f.write(arg)
    f.close()
    print ('Exported Finger Pose Script: ' + filename)


# Util UI
class UI(QtWidgets.QWidget):

    def __init__(self, parent=aboutUI.get_maya_window()):
        super(UI, self).__init__(parent=parent)
        if mc.window('Hand_Pose_UI', q=1, ex=1):
            mc.deleteUI('Hand_Pose_UI')

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui = hand_ui.Ui_handUI()
        self.ui.setupUi(self)
        self.setObjectName('Hand_Pose_UI')

        self.ui.buildBtn.clicked.connect(buildPose)
        self.ui.rebuildBtn.clicked.connect(rebuildPose)
        self.ui.mirrorBtn.clicked.connect(mirrorPose)
        self.ui.exportBtn.clicked.connect(exportPose)


# from rxParts import hand
# handPoseUi = hand.UI()
# handPoseUi.show()