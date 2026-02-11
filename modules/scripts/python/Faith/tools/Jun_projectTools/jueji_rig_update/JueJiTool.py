# Embedded file name: E:/JunCmds/tool/projectTools\jueji_rig_update\JueJiTool.py
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import string, random
import os, re, sys, time
import maya.cmds as cmds
import Follow.FollowTool as FollowTool
reload(FollowTool)
ft = FollowTool.followTool()

class JueJiToolC(object):

    def __init__(self):
        pass

    def win(self):
        ver = 'ver 1.0'
        winName = 'JueJiTool'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        simulationWindow = cmds.window(winName, t=str(time.strftime('%m/%d %H:%M', time.localtime(time.time()))) + '  JueJiTool' + ver)
        child1 = cmds.columnLayout(adjustableColumn=True)
        cmds.button(l=u'1) rig update1 (\u4fee\u6539\u4e00\u4e9b\u5c42\u7ea7\u95ee\u9898)', h=30, c=lambda *args: self.rigUpdate1())
        cmds.button('addIKFKSeamlessSwitchButton', l=u'2) add IKFK \u65e0\u7f1d\u5207\u6362\u8bbe\u7f6e', h=30, c=lambda *args: self.addIkfkSeamlessSwitSet(), en=True)
        cmds.button('addNeckFollowButton', l=u'3) add neck follow(\u6dfb\u52a0\u8116\u5b50\u8ddf\u968f\u5207\u6362)', h=30, c=lambda *args: self.addNeckFollow(), en=True)
        cmds.button('rigUpdate2Button', l=u'4) rig update2 (\u6dfb\u52a0\u63a7\u5236\u5668\u9690\u85cf\u663e\u793a\uff0c\u624b\u6307\u9a71\u52a8)', h=30, c=lambda *args: self.rigUpdate2(), en=True)
        cmds.button('editPoleFollowButton', l=u'5) edit pole follow(\u4fee\u6539\u6781\u5411\u91cf\u8ddf\u968f\u95ee\u9898)', h=30, c=lambda *args: self.pole_con_update(), en=True)
        cmds.button('', l=u'\u9009\u62e9\u624b\u81c2ikhandle\uff0c\u67e5\u770b\u662f\u5426\u8bbe\u7f6e\u8fc7Tpose', h=30, c="cmds.select('L_uparm_nonroll_ikhandle'),cmds.button('correctArm_AxisButton',e = True,en = True)", en=True)
        cmds.rowLayout(numberOfColumns=2)
        cmds.textField('correctArm_Axis_numTF', text=50, en=1, w=50)
        cmds.button('correctArm_AxisButton', l=u') correctArm_Axis (\u8bbe\u7f6eTpose\n\u89e3\u51b3\u624b\u81c2\u524d\u540e\u65cb\u8f6c\u4f1a\u81ea\u8f6c\u95ee\u9898)', h=50, c=lambda *args: self.correctArm_Axis(), en=True)
        cmds.setParent(child1)
        cmds.button(l=u'\u6dfb\u52a0\u65f6\u7801\u5c5e\u6027', h=30, c=lambda *args: self.addRootAttr(), en=True)
        cmds.button(l=u'7) \u90e8\u5206\u5c5e\u6027\u8bbe\u7f6e\u4e3a\u9ed8\u8ba4\u53c2\u6570  (\u786e\u4fdd\u662fFK\u72b6\u6001)', h=40, bgc=[0, 0.3, 0], c=lambda *args: self.rigDefaultParameters())
        cmds.button('rigCheckButton', l=u'6) rig check(\u611f\u8c22\u73ba\u54e5)', h=35, bgc=[0, 1, 0], c=lambda *args: self.rigCheck(), en=True)
        cmds.button(l=u'7) \u90e8\u5206\u5c5e\u6027\u8bbe\u7f6e\u4e3a\u9ed8\u8ba4\u53c2\u6570  (\u786e\u4fdd\u662fFK\u72b6\u6001)', h=40, bgc=[0, 0.3, 0], c=lambda *args: self.rigDefaultParameters())
        cmds.button(l=u'8) rig mocap jnt \u5bf9\u6bd4', h=30, c=lambda *args: self.mocapComparison())
        cmds.button('addHipsJntButton', l=u'3.1) add hips Jnt (\u5148\u5347\u7ea7rig update2)', h=30, bgc=[0, 0.5, 0], c=lambda *args: self.addHipsHelpJnt(), en=True)
        cmds.button(l=u'\u52a8\u4f5c\u5e93', h=30, bgc=[0, 0.2, 0], c=lambda *args: self.studiolibrary(), en=True)
        cmds.button(l=u'combinSdkTool', w=100, c=lambda *args: self.cbdWin())
        cmds.rowLayout(numberOfColumns=3)
        cmds.button(l=u'ShowJnt(\u663e\u793a\u9aa8\u9abc)', w=100, c=lambda *args: self.ShowJnt())
        cmds.button(l=u'HideJnt(\u9690\u85cf\u9aa8\u9abc)', w=100, c=lambda *args: self.HideJnt())
        cmds.setParent(child1)
        cmds.showWindow()

    def rigUpdate1(self):
        cmds.button('addIKFKSeamlessSwitchButton', e=True, en=True)
        cmds.select(cl=True)
        if cmds.listRelatives('L_arm_shoulder_zero_MB', p=True)[0] != 'chestmid_simple_fk_ctrl_MB':
            cmds.parent('L_arm_shoulder_zero_MB', 'chestmid_simple_fk_ctrl_MB')
        if cmds.listRelatives('R_arm_shoulder_zero_MB', p=True)[0] != 'chestmid_simple_fk_ctrl_MB':
            cmds.parent('R_arm_shoulder_zero_MB', 'chestmid_simple_fk_ctrl_MB')
        if cmds.listRelatives('neck_simple_fk01_zero_MB', p=True)[0] != 'chestmid_simple_fk_ctrl_MB':
            cmds.parent('neck_simple_fk01_zero_MB', 'chestmid_simple_fk_ctrl_MB')
        if cmds.listRelatives('L_leg_crotch_zero_MB', p=True)[0] != 'body_simple_master_ctrl_MB':
            cmds.parent('L_leg_crotch_zero_MB', 'body_simple_master_ctrl_MB')
        if cmds.listRelatives('R_leg_crotch_zero_MB', p=True)[0] != 'body_simple_master_ctrl_MB':
            cmds.parent('R_leg_crotch_zero_MB', 'body_simple_master_ctrl_MB')
        cmds.setAttr('L_uparm_fk_ctrl.armFollow', 0)
        cmds.setAttr('R_uparm_fk_ctrl.armFollow', 0)
        mbJnts = [u'Root',
         u'Spine',
         u'Spine1',
         u'Spine2',
         u'Chest',
         u'ChestMid',
         u'LeftShoulder',
         u'LeftArm',
         u'LeftForeArm',
         u'LeftHand',
         u'LeftHandIndexRoot',
         u'LeftHandIndex1',
         u'LeftHandIndex2',
         u'LeftHandIndex3',
         u'LeftHandIndex4',
         u'LeftHandMiddleRoot',
         u'LeftHandMiddle1',
         u'LeftHandMiddle2',
         u'LeftHandMiddle3',
         u'LeftHandMiddle4',
         u'LeftHandPinkyRoot',
         u'LeftHandPinky1',
         u'LeftHandPinky2',
         u'LeftHandPinky3',
         u'LeftHandPinky4',
         u'LeftHandRingRoot',
         u'LeftHandRing1',
         u'LeftHandRing2',
         u'LeftHandRing3',
         u'LeftHandRing4',
         u'LeftHandThumbRoot',
         u'LeftHandThumb1',
         u'LeftHandThumb2',
         u'LeftHandThumb3',
         u'LeftHandThumb4',
         u'RightShoulder',
         u'RightArm',
         u'RightForeArm',
         u'RightHand',
         u'RightHandIndexRoot',
         u'RightHandIndex1',
         u'RightHandIndex2',
         u'RightHandIndex3',
         u'RightHandIndex4',
         u'RightHandMiddleRoot',
         u'RightHandMiddle1',
         u'RightHandMiddle2',
         u'RightHandMiddle3',
         u'RightHandMiddle4',
         u'RightHandPinkyRoot',
         u'RightHandPinky1',
         u'RightHandPinky2',
         u'RightHandPinky3',
         u'RightHandPinky4',
         u'RightHandRingRoot',
         u'RightHandRing1',
         u'RightHandRing2',
         u'RightHandRing3',
         u'RightHandRing4',
         u'RightHandThumbRoot',
         u'RightHandThumb1',
         u'RightHandThumb2',
         u'RightHandThumb3',
         u'RightHandThumb4',
         u'Neck1',
         u'Neck2',
         u'Head',
         u'LeftUpLeg',
         u'LeftLeg',
         u'LeftFoot',
         u'LeftToeBase',
         u'LeftToeBaseEnd',
         u'RightUpLeg',
         u'RightLeg',
         u'RightFoot',
         u'RightToeBase',
         u'RightToeBaseEnd']
        attrs = ['.tx',
         '.ty',
         '.tz',
         '.rx',
         '.ry',
         '.rz',
         '.sx',
         '.sy',
         '.sz',
         '.v',
         '.radi']
        attrs = [('L_arm_switch_ctrl.ikFk', 0),
         ('R_arm_switch_ctrl.ikFk', 0),
         ('L_leg_switch_ctrl.ikFk', 0),
         ('R_leg_switch_ctrl.ikFk', 0),
         ('body_simple_master_ctrl.IKVis', 0),
         ('body_simple_master_ctrl.secVis', 0),
         ('L_uparm_fk_ctrl.armFollow', 0),
         ('R_uparm_fk_ctrl.armFollow', 0),
         ('L_thumb_finger_ctrl.CtrlVis', 1),
         ('L_index_finger_ctrl.CtrlVis', 1),
         ('L_middle_finger_ctrl.CtrlVis', 1),
         ('L_pinky_finger_ctrl.CtrlVis', 1),
         ('L_ring_finger_ctrl.CtrlVis', 1),
         ('R_thumb_finger_ctrl.CtrlVis', 1),
         ('R_index_finger_ctrl.CtrlVis', 1),
         ('R_middle_finger_ctrl.CtrlVis', 1),
         ('R_pinky_finger_ctrl.CtrlVis', 1),
         ('R_ring_finger_ctrl.CtrlVis', 1)]
        for attr in attrs:
            cmds.setAttr(attr[0], attr[1])
            cmds.addAttr(attr[0], e=True, dv=attr[1])

        nodePartCons = cmds.listConnections('waist_simple_fk01_dr_MB.translate', scn=True, source=False)
        if len(nodePartCons) == 1 and nodePartCons[0] == 'waist_simple_fk01_dr':
            cmds.disconnectAttr('waist_simple_fk01_dr_MB.translate', 'waist_simple_fk01_dr.translate')
            cmds.disconnectAttr('waist_simple_fk01_dr_MB.rotate', 'waist_simple_fk01_dr.rotate')
            print 'waist_simple_fk01_dr.translate  waist_simple_fk01_dr.rotate discon'
        if len(nodePartCons) == 1 and nodePartCons[0] != 'body_simple_offset_dr':
            cmds.connectAttr('waist_simple_fk01_dr_MB.translate', 'body_simple_offset_dr.translate')
            cmds.connectAttr('waist_simple_fk01_dr_MB.rotate', 'body_simple_offset_dr.rotate')
            print 'body_simple_offset_dr.translate   body_simple_offset_dr.rotate   con'
        cmds.select(cl=True)
        print '------------------------------------all is ok'
        sys.stderr.write('# ------ rig Update1 is ok')

    def addIkfkSeamlessSwitSet(self):
        cmds.button('addNeckFollowButton', e=True, en=True)
        cmds.select(cl=True)
        if cmds.objExists('R_knee_ik_ctrlForMatch_zero') == True:
            cmds.warning('------addIkfkSeamlessSwitSet is exists')
        else:
            fkCtrls = ['L_uparm_fk_ctrl', 'L_lowarm_fk_ctrl', 'L_wrist_fk_ctrl']
            ikJots = ['L_uparm_ik_jnt', 'L_lowarm_ik_jnt', 'L_arm_ik_ctrl']
            fkGims = []
            ikCtls = ['L_arm_ik_ctrl']
            poCtls = ['L_elbow_ik_ctrl']
            import rig_toolset.IkFkSwitch as ikfk
            reload(ikfk)
            ikfk_in = ikfk.AnyIkFkSwitch()
            ikfk_in.remberIkFkComponents('L_arm_switch_ctrl.ikFk', 0, 1, fkCtrls, ikJots, ikCtls, poCtls, fkGmbs=fkGims)
            fkCtrls = ['R_uparm_fk_ctrl', 'R_lowarm_fk_ctrl', 'R_wrist_fk_ctrl']
            ikJots = ['R_uparm_ik_jnt', 'R_lowarm_ik_jnt', 'R_arm_ik_ctrl']
            fkGims = []
            ikCtls = ['R_arm_ik_ctrl']
            poCtls = ['R_elbow_ik_ctrl']
            import rig_toolset.IkFkSwitch as ikfk
            reload(ikfk)
            ikfk_in.remberIkFkComponents('R_arm_switch_ctrl.ikFk', 0, 1, fkCtrls, ikJots, ikCtls, poCtls, fkGmbs=fkGims)
            fkCtrls = ['L_upleg_fk_ctrl',
             'L_lowleg_fk_ctrl',
             'L_ankle_fk_ctrl',
             'L_sole_fk_ctrl']
            ikJots = ['L_upleg_ik_jnt',
             'L_lowleg_ik_jnt',
             'L_ankle_ik_jnt',
             'L_sole_ik_jnt']
            fkGmbs = []
            ikGims = []
            ikCtls = ['L_leg_ik_ctrl']
            poCtls = ['L_knee_ik_ctrl']
            import rig_toolset.IkFkSwitch as ikfk
            reload(ikfk)
            ikfk_in.remberIkFkComponents('L_leg_switch_ctrl.ikFk', 0, 1, fkCtrls, ikJots, ikCtls, poCtls, fkGmbs=fkGmbs, ikGmbs=ikGims)
            fkCtrls = ['R_upleg_fk_ctrl',
             'R_lowleg_fk_ctrl',
             'R_ankle_fk_ctrl',
             'R_sole_fk_ctrl']
            ikJots = ['R_upleg_ik_jnt',
             'R_lowleg_ik_jnt',
             'R_ankle_ik_jnt',
             'R_sole_ik_jnt']
            fkGmbs = []
            ikGims = []
            ikCtls = ['R_leg_ik_ctrl']
            poCtls = ['R_knee_ik_ctrl']
            import rig_toolset.IkFkSwitch as ikfk
            reload(ikfk)
            ikfk_in.remberIkFkComponents('R_leg_switch_ctrl.ikFk', 0, 1, fkCtrls, ikJots, ikCtls, poCtls, fkGmbs=fkGmbs, ikGmbs=ikGims)
            sys.stderr.write('# add Ikfk Seamless Swit Set is ok')

    def addNeckFollow(self):
        cmds.select(cl=True)
        lockObj = 'neck_simple_fk01_con'
        addAttrObj = 'neck_simple_fk01_ctrl'
        followObjs = ['chestmid_simple_skin_jnt', 'all_ctrl']
        followEnumAttrs = ['body', 'world']
        attr = 'follow'
        constrainType = ['orient']
        aa = cmds.listAttr(addAttrObj)
        if attr in aa:
            cmds.warning(addAttrObj + '.' + attr + ' ------is exists')
        followObjBridgeZeros = ft.follow(lockObj, addAttrObj, attr, followEnumAttrs, followObjs, constrainType)
        if followObjBridgeZeros != None:
            cmds.parent(followObjBridgeZeros[0], 'all_ctrl')
            sys.stderr.write('# add pole con update is ok')
        return

    def rigUpdate2(self):
        cmds.select(cl=True)

        def setDrivenKey(driver, driven, driverNums, drivenNums, itt = 'linear', ott = 'linear'):
            driverSplit = driver.split('.')
            driverObj = driverSplit[0]
            driverAttr = ''
            for x, Attr in enumerate(driverSplit[1:]):
                if x == 0:
                    driverAttr = Attr
                else:
                    driverAttr = driverAttr + '.' + Attr

            drivenSplit = driven.split('.')
            drivenObj = drivenSplit[0]
            drivenAttr = ''
            for x, Attr in enumerate(drivenSplit[1:]):
                if x == 0:
                    drivenAttr = Attr
                else:
                    drivenAttr = drivenAttr + '.' + Attr

            if cmds.objExists(driverObj) == True and cmds.objExists(drivenObj) != True:
                exit('There is no ' + driverObj + ' or ' + drivenObj)
            elif cmds.attributeQuery(driverAttr, node=driverObj, exists=True) != True:
                exit('There is no ' + driverObj + '.' + driverAttr)
            elif cmds.attributeQuery(drivenAttr, node=drivenObj, exists=True) != True:
                exit('There is no ' + drivenObj + '.' + drivenAttr)
            num = len(driverNums)
            for i in range(num):
                animCv = cmds.setDrivenKeyframe(driven, currentDriver=driver, driverValue=driverNums[i], v=drivenNums[i], itt=itt, ott=ott)

        def objAddAttr(addObjAttrs, keyable, lock):
            for i in range(len(addObjAttrs)):
                addObjAttr = addObjAttrs[i]
                obj = addObjAttr.split('.')[0]
                attr = addObjAttr.split('.')[1]
                fkVis = cmds.addAttr(obj, ln=attr, at='double', min=0, max=10, dv=0, keyable=keyable)

        if cmds.objExists('L_leg_ik02_ctrl_zero') == True:
            cmds.warning('------rigUpdate2 is Update')
            if cmds.listRelatives('L_leg_ik02_ctrl_zero', p=True)[0] != 'L_leg_crotch_SN':
                cmds.parent('L_leg_ik02_ctrl_zero', 'L_leg_crotch_SN')
            if cmds.listRelatives('R_leg_ik02_ctrl_zero', p=True)[0] != 'R_leg_crotch_SN':
                cmds.parent('R_leg_ik02_ctrl_zero', 'R_leg_crotch_SN')
            cmds.setAttr('head_simple_second_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('neck_simple_ik04_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('hips_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('waist_simple_ik06_ctrl.v', lock=True, channelBox=False, keyable=False)
        else:
            addObjAttrs = ['body_simple_master_ctrl.fkvis', 'neck_simple_fk01_ctrl.fkvis']
            conAttrss = [['chestmid_simple_fk_ctrlShape.overrideVisibility', 'waist_simple_fk05_ctrlShape.overrideVisibility', 'waist_simple_fk03_ctrlShape.overrideVisibility'], ['neck_simple_fk02_ctrlShape.overrideVisibility']]
            for i in range(len(addObjAttrs)):
                addObjAttr = addObjAttrs[i]
                conAttrs = conAttrss[i]
                obj = addObjAttr.split('.')[0]
                attr = addObjAttr.split('.')[1]
                fkVis = cmds.addAttr(obj, ln=attr, at='double', min=0, max=1, dv=0, keyable=True)
                cmds.setAttr(addObjAttr, keyable=False, channelBox=True)
                for attr in conAttrs:
                    cmds.connectAttr(addObjAttr, attr)

            renameObjs = ['waist_simple_ik01_zero',
             'waist_simple_ik01_con',
             'waist_simple_ik01_dr',
             'waist_simple_ik01_PH',
             'waist_simple_ik01_SN',
             'waist_simple_ik01_ctrl']
            for obj in renameObjs:
                newname = 'hips_' + obj.split('_')[-1]
                cmds.rename(obj, newname)

            objs = ['L_leg_crotch_ctrl', 'R_leg_crotch_ctrl']
            for obj in objs:
                print obj
                legctrl = cmds.duplicate(obj)[0]
                leg_ik02_ctrl = cmds.rename(legctrl, obj[0] + '_leg_ik02_ctrl')
                cmds.connectAttr(leg_ik02_ctrl + '.frontFollow', obj + '.frontFollow')
                cmds.connectAttr(leg_ik02_ctrl + '.sideFollow', obj + '.sideFollow')
                cmds.connectAttr(leg_ik02_ctrl + '.upFollow', obj + '.upFollow')
                cmds.parent(leg_ik02_ctrl, w=True)
                leg_ik02_ctrlzero = cmds.group(name=leg_ik02_ctrl + '_zero', em=True)
                cmds.delete(cmds.parentConstraint(leg_ik02_ctrl, leg_ik02_ctrlzero, mo=0))
                cmds.parent(leg_ik02_ctrl, leg_ik02_ctrlzero)
                cmds.delete(cmds.pointConstraint(leg_ik02_ctrl[0] + '_upleg_fk_ctrl', leg_ik02_ctrlzero, mo=0))
                cmds.parent(leg_ik02_ctrlzero, leg_ik02_ctrl[0] + '_leg_crotch_SN')
                leg_ik_crotch_ikHandle = leg_ik02_ctrl[0] + '_crotch_ikHandle'
                if len(cmds.ls(leg_ik_crotch_ikHandle)) == 1:
                    cmds.parent(leg_ik_crotch_ikHandle, leg_ik02_ctrl)
                elif len(cmds.ls(leg_ik_crotch_ikHandle)) == 2:
                    a = cmds.listRelatives(leg_ik02_ctrl, children=True, f=True)
                    cmds.delete(a[1:])
                    cmds.parent(leg_ik_crotch_ikHandle + '_grp', leg_ik02_ctrl)
                cmds.setAttr(obj + '.v', lock=False, keyable=True, channelBox=True)
                cmds.setAttr(obj + '.v', 0)
                cmds.setAttr(obj + '.v', lock=True, keyable=False, channelBox=True)
                cmds.rename(obj, obj + '_old')

            drivers = ['L_leg_switch_ctrl.ikFk']
            driverNums = (0, 1)
            drivens = ['L_leg_ik02_ctrl_zero.v']
            drivenNumlists = [(0, 1)]
            for driver in drivers:
                for i in range(len(drivens)):
                    driven = drivens[i]
                    drivenNums = drivenNumlists[i]
                    setDrivenKey(driver, driven, driverNums, drivenNums, itt='linear', ott='linear')

            drivers = ['R_leg_switch_ctrl.ikFk']
            driverNums = (0, 1)
            drivens = ['R_leg_ik02_ctrl_zero.v']
            drivenNumlists = [(0, 1)]
            for driver in drivers:
                for i in range(len(drivens)):
                    driven = drivens[i]
                    drivenNums = drivenNumlists[i]
                    setDrivenKey(driver, driven, driverNums, drivenNums, itt='linear', ott='linear')

            addObjAttrs = ['L_arm_switch_ctrl.clench', 'R_arm_switch_ctrl.clench']
            keyable = 1
            lock = 0
            objAddAttr(addObjAttrs, keyable, lock)
            drivers = ['L_arm_switch_ctrl.clench']
            driverNums = (0, 10)
            drivens = ['L_thumbfinger01_dri_dr.rotateZ',
             'L_thumbfinger02_dri_dr.rotateZ',
             'L_thumbfinger03_dri_dr.rotateZ',
             'L_thumbfinger04_dri_dr.rotateZ',
             'L_indexfinger01_dri_dr.rotateZ',
             'L_indexfinger02_dri_dr.rotateZ',
             'L_indexfinger03_dri_dr.rotateZ',
             'L_indexfinger04_dri_dr.rotateZ',
             'L_middlefinger01_dri_dr.rotateZ',
             'L_middlefinger02_dri_dr.rotateZ',
             'L_middlefinger03_dri_dr.rotateZ',
             'L_middlefinger04_dri_dr.rotateZ',
             'L_ringfinger01_dri_dr.rotateZ',
             'L_ringfinger02_dri_dr.rotateZ',
             'L_ringfinger03_dri_dr.rotateZ',
             'L_ringfinger04_dri_dr.rotateZ',
             'L_pinkyfinger01_dri_dr.rotateZ',
             'L_pinkyfinger02_dri_dr.rotateZ',
             'L_pinkyfinger03_dri_dr.rotateZ',
             'L_pinkyfinger04_dri_dr.rotateZ']
            drivenNumlists = [(0, 0),
             (0, -10),
             (0, -20),
             (0, -40),
             (0, 0),
             (0, -85),
             (0, -95),
             (0, -80),
             (0, 0),
             (0, -85),
             (0, -95),
             (0, -80),
             (0, 0),
             (0, -85),
             (0, -95),
             (0, -80),
             (0, 0),
             (0, -85),
             (0, -95),
             (0, -80)]
            for driver in drivers:
                for i in range(len(drivens)):
                    driven = drivens[i]
                    drivenNums = drivenNumlists[i]
                    setDrivenKey(driver, driven, driverNums, drivenNums, itt='linear', ott='linear')

            drivers = ['R_arm_switch_ctrl.clench']
            driverNums = (0, 10)
            drivens = ['R_thumbfinger01_dri_dr.rotateZ',
             'R_thumbfinger02_dri_dr.rotateZ',
             'R_thumbfinger03_dri_dr.rotateZ',
             'R_thumbfinger04_dri_dr.rotateZ',
             'R_indexfinger01_dri_dr.rotateZ',
             'R_indexfinger02_dri_dr.rotateZ',
             'R_indexfinger03_dri_dr.rotateZ',
             'R_indexfinger04_dri_dr.rotateZ',
             'R_middlefinger01_dri_dr.rotateZ',
             'R_middlefinger02_dri_dr.rotateZ',
             'R_middlefinger03_dri_dr.rotateZ',
             'R_middlefinger04_dri_dr.rotateZ',
             'R_ringfinger01_dri_dr.rotateZ',
             'R_ringfinger02_dri_dr.rotateZ',
             'R_ringfinger03_dri_dr.rotateZ',
             'R_ringfinger04_dri_dr.rotateZ',
             'R_pinkyfinger01_dri_dr.rotateZ',
             'R_pinkyfinger02_dri_dr.rotateZ',
             'R_pinkyfinger03_dri_dr.rotateZ',
             'R_pinkyfinger04_dri_dr.rotateZ']
            drivenNumlists = [(0, 0),
             (0, 10),
             (0, 20),
             (0, 40),
             (0, 0),
             (0, 85),
             (0, 95),
             (0, 80),
             (0, 0),
             (0, 85),
             (0, 95),
             (0, 80),
             (0, 0),
             (0, 85),
             (0, 95),
             (0, 80),
             (0, 0),
             (0, 85),
             (0, 95),
             (0, 80)]
            for driver in drivers:
                for i in range(len(drivens)):
                    driven = drivens[i]
                    drivenNums = drivenNumlists[i]
                    setDrivenKey(driver, driven, driverNums, drivenNums, itt='linear', ott='linear')

            cmds.setAttr('head_simple_second_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('neck_simple_ik04_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('hips_ctrl.v', lock=True, channelBox=False, keyable=False)
            cmds.setAttr('waist_simple_ik06_ctrl.v', lock=True, channelBox=False, keyable=False)
            sys.stderr.write('------# Rig Update 2 is ok #' * 3)

    def pole_con_update(self):
        cmds.select(cl=True)

        def poleWorldCon(ctrl, ctrlgrp, addAttrs, driveAttr):
            aa = cmds.listAttr(ctrl, ud=True)
            if 'world_type' in aa:
                cmds.warning(' ------world type is exists')
            else:
                loc = ['knee_elbow_con_loc']
                if cmds.objExists(loc[0]) == 0:
                    loc = cmds.spaceLocator(n=loc[0])
                    cmds.parent(loc[0], 'all_ctrl')
                    cmds.setAttr(loc[0] + '.v', 0)
                parentConstraints = cmds.listRelatives(ctrlgrp, type='parentConstraint')
                if parentConstraints != None:
                    cmds.delete(parentConstraints)
                parentConName = cmds.parentConstraint(loc[0], ctrlgrp, n=ctrlgrp + '_parentCon', mo=True)
                animC = parentConName[0] + '_' + loc[0] + 'W0'
                if cmds.objExists(animC) == 1:
                    cmds.delete(animC)
                cmds.setDrivenKeyframe(parentConName[0] + '.' + loc[0] + 'W0', cd=driveAttr, dv=2, v=1)
                cmds.setDrivenKeyframe(parentConName[0] + '.' + loc[0] + 'W0', cd=driveAttr, dv=1, v=0)
                cmds.addAttr(ctrl, ln='world_type', k=True, at='long', min=0, max=1, dv=1)
                MD = cmds.shadingNode('multiplyDivide', n=ctrl + '_MD', asShader=True)
                cmds.connectAttr(animC + '.output', MD + '.input1.input1X')
                cmds.connectAttr(ctrl + '.world_type', MD + '.input2.input2X')
                connectNode = cmds.connectionInfo(parentConName[0] + '.' + loc[0] + 'W0', sfd=True)
                if connectNode != None:
                    cmds.disconnectAttr(connectNode, parentConName[0] + '.' + loc[0] + 'W0')
                cmds.connectAttr(MD + '.outputX', parentConName[0] + '.' + loc[0] + 'W0')
                cmds.select(cl=True)
                sys.stderr.write('# add pole con update is ok')
            return

        ctrl = 'L_elbow_ik_ctrl'
        ctrlgrp = 'L_elbow_ik_dr'
        addAttrs = 'world_type'
        driveAttr = 'L_elbow_ik_ctrl.elbowFollow'
        poleWorldCon(ctrl, ctrlgrp, addAttrs, driveAttr)
        ctrl = 'R_elbow_ik_ctrl'
        ctrlgrp = 'R_elbow_ik_dr'
        addAttrs = 'world_type'
        driveAttr = 'R_elbow_ik_ctrl.elbowFollow'
        poleWorldCon(ctrl, ctrlgrp, addAttrs, driveAttr)
        ctrl = 'R_knee_ik_ctrl'
        ctrlgrp = 'R_knee_ik_dr'
        addAttrs = 'world_type'
        driveAttr = 'R_knee_ik_ctrl.kneeFollow'
        poleWorldCon(ctrl, ctrlgrp, addAttrs, driveAttr)
        ctrl = 'L_knee_ik_ctrl'
        ctrlgrp = 'L_knee_ik_dr'
        addAttrs = 'world_type'
        driveAttr = 'L_knee_ik_ctrl.kneeFollow'
        poleWorldCon(ctrl, ctrlgrp, addAttrs, driveAttr)
        cmds.select(cl=True)

    def addRootAttr(self):
        cmds.addAttr('Root', ln='TCHour', at='long', dv=0, keyable=True)
        cmds.addAttr('Root', ln='TCMinute', at='long', dv=0, keyable=True)
        cmds.addAttr('Root', ln='TCSecond', at='long', dv=0, keyable=True)
        cmds.addAttr('Root', ln='TCFrame', at='long', dv=0, keyable=True)

    def rigCheck(self):
        import maya.cmds as mc
        import sys
        sys.path.insert(0, 'R:\\JueJi\\JueJiTool\\rigCmds')
        import tool.rigChecker.Ui as ui
        reload(ui)
        UI = ui.rosaCheckerUI()
        UI.open()

    def rigDefaultParameters(self):
        attrs = [('L_arm_switch_ctrl.ikFk', 0),
         ('R_arm_switch_ctrl.ikFk', 0),
         ('L_leg_switch_ctrl.ikFk', 0),
         ('R_leg_switch_ctrl.ikFk', 0),
         ('body_simple_master_ctrl.IKVis', 0),
         ('body_simple_master_ctrl.secVis', 0),
         ('L_uparm_fk_ctrl.armFollow', 0),
         ('R_uparm_fk_ctrl.armFollow', 0),
         ('L_thumb_finger_ctrl.CtrlVis', 1),
         ('L_index_finger_ctrl.CtrlVis', 1),
         ('L_middle_finger_ctrl.CtrlVis', 1),
         ('L_pinky_finger_ctrl.CtrlVis', 1),
         ('L_ring_finger_ctrl.CtrlVis', 1),
         ('R_thumb_finger_ctrl.CtrlVis', 1),
         ('R_index_finger_ctrl.CtrlVis', 1),
         ('R_middle_finger_ctrl.CtrlVis', 1),
         ('R_pinky_finger_ctrl.CtrlVis', 1),
         ('R_ring_finger_ctrl.CtrlVis', 1)]
        for attr in attrs:
            cmds.setAttr(attr[0], attr[1])
            cmds.addAttr(attr[0], e=True, dv=attr[1])
            print str(attr) + '---is ok'

        cmds.setAttr('body_simple_master_ctrl.fkvis', 0)
        cmds.setAttr('neck_simple_fk01_ctrl.follow', 0)
        cmds.setAttr('neck_simple_fk01_ctrl.fkvis', 0)
        cmds.setAttr('L_uparm_fk_ctrl.armFollow', 0)
        cmds.setAttr('R_uparm_fk_ctrl.armFollow', 0)
        cmds.setAttr('L_elbow_ik_ctrl.elbowFollow', 0)
        cmds.setAttr('R_elbow_ik_ctrl.elbowFollow', 0)
        cmds.setAttr('L_elbow_ik_ctrl.world_type', 1)
        cmds.setAttr('R_elbow_ik_ctrl.world_type', 1)
        cmds.setAttr('L_upleg_fk_ctrl.legFollow', 0)
        cmds.setAttr('R_upleg_fk_ctrl.legFollow', 0)
        cmds.setAttr('L_knee_ik_ctrl.kneeFollow', 0)
        cmds.setAttr('R_knee_ik_ctrl.kneeFollow', 0)
        cmds.setAttr('L_knee_ik_ctrl.world_type', 1)
        cmds.setAttr('R_knee_ik_ctrl.world_type', 1)

    def mocapComparison(self):
        import mocap_rig_comparison as mocap
        reload(mocap)
        fmm = mocap.MocapComparison()
        MocapComparison = fmm.MocapComparisonUI()

    def addHipsHelpJnt(self):
        cmds.select(cl=True)
        hipsCtrl = 'hips_ctrl'
        hips_help = 'hips_help'
        jntsuffix = '_jnt'
        if cmds.objExists(hips_help + '_con') == True:
            cmds.warning('-------addHipsHelpJnt is exists')
        else:
            hips_help_con = cmds.group(name=hips_help + '_con', em=True)
            hips_help_zero = cmds.group(name=hips_help + '_zero')
            hips_help01_jnt = cmds.joint(name=hips_help + '01' + jntsuffix)
            cmds.joint(name=hips_help + '02' + jntsuffix, p=(0, -20, 0))
            cmds.parent(hips_help01_jnt, hips_help_con)
            cmds.delete(cmds.parentConstraint(hipsCtrl, hips_help_zero, mo=False))
            lockObj = hips_help_con
            addAttrObj = ''
            followObjs = ['hips_ctrl', 'body_simple_local02_ctrl']
            followEnumAttrs = ['hips', 'body']
            attr = 'follow'
            constrainType = ['parent']
            print 'ok'
            locksGrp = ft.follow(lockObj, addAttrObj, attr, followEnumAttrs, followObjs, constrainType)
            print 'ok'
            cmds.parent(locksGrp[0], 'all_ctrl')
            cmds.parent(hips_help_zero, 'all_ctrl')
            body_Par_hipsHelp = locksGrp[1][1]
            cmds.parentConstraint(hipsCtrl, body_Par_hipsHelp, mo=True)
            ft.setDrivenKey('L_leg_switch_ctrl.ikFk', body_Par_hipsHelp + '_parentConstraint1' + '.' + hipsCtrl + 'W1', [0, 1], [1, 0], 'linear', 'linear')
            ft.setDrivenKey('L_leg_switch_ctrl.ikFk', body_Par_hipsHelp + '_parentConstraint1' + '.' + 'body_simple_local02_ctrl' + 'W0', [1, 0], [1, 0], 'linear', 'linear')
            sys.stderr.write('# add Hips Help Jnt is ok')

    def skinOff(self):
        skinNodes = cmds.ls(type='skinCluster')
        skinEnvelopeOffs = []
        for skinNode in skinNodes:
            skinEnvelope = cmds.getAttr(skinNode + '.envelope')
            if skinEnvelope != 1.0:
                skinEnvelopeOffs.append(skinNode)

        skinEnvelopeOffset = 'skinEnvelopeOffset'
        if cmds.objExists(skinEnvelopeOffset) == True:
            cmds.delete(skinEnvelopeOffset)
        cmds.sets(skinEnvelopeOffs, n=skinEnvelopeOffset)
        if skinEnvelopeOffs != []:
            cmds.warning('skinCluster Envelope \xe4\xb8\x8d\xe4\xb8\xba1\xe7\x9a\x84,\xe8\xaf\xb7\xe7\xa1\xae\xe8\xae\xa4------' + str(skinEnvelopeOffs))
        else:
            for skinNode in skinNodes:
                cmds.setAttr(skinNode + '.envelope', 0)

    def skinOn(self):
        skinNodes = cmds.ls(type='skinCluster')
        for skinNode in skinNodes:
            cmds.setAttr(skinNode + '.envelope', 1)

    def ShowJnt(self):
        sels = cmds.ls(type='joint')
        for sel in sels:
            cmds.setAttr(sel + '.drawStyle', 0)
            cmds.setAttr(sel + '.hideOnPlayback', 1)

    def HideJnt(self):
        sels = cmds.ls(type='joint')
        for sel in sels:
            cmds.setAttr(sel + '.drawStyle', 2)
            cmds.setAttr(sel + '.hideOnPlayback', 1)

    def correctArm_Axis(rotateValue):
        rotateValue = int(cmds.textField('correctArm_Axis_numTF', q=True, text=True))
        checkUpdate = 'L_uparm_nonroll_ikhandle_update'
        if cmds.objExists(checkUpdate) == True:
            cmds.warning(u'\u5df2\u7ecf\u8fd0\u884c\u8fc7\u4e86\uff0c\u8bf7\u68c0\u67e5\u6548\u679c\u662f\u5426\u6b63\u786e')
        else:
            cmds.group(name=checkUpdate, em=True)
            cmds.parent(checkUpdate, 'L_uparm_nonroll_ikhandle')
            L_Handle = 'L_uparm_nonroll_ikhandle'
            R_Handle = 'R_uparm_nonroll_ikhandle'
            L_ctrl = 'L_uparm_fk_ctrl'
            R_ctrl = 'R_uparm_fk_ctrl'
            locator_tem = 'temple_locator'
            cmds.spaceLocator(n=locator_tem)
            consnode = 'temple_node'
            cmds.setAttr(str(L_ctrl) + '.rotateZ', 0)
            cmds.parentConstraint(L_Handle, locator_tem, mo=False, n=consnode)
            cmds.delete(consnode)
            cmds.parent(locator_tem, L_ctrl)
            cmds.setAttr(str(L_ctrl) + '.rotateZ', rotateValue)
            cmds.parent(locator_tem, world=True)
            cmds.orientConstraint(locator_tem, L_Handle, n=consnode)
            cmds.delete(consnode)
            cmds.setAttr(str(R_ctrl) + '.rotateZ', 0)
            cmds.parentConstraint(R_Handle, locator_tem, mo=False, n=consnode)
            cmds.delete(consnode)
            cmds.parent(locator_tem, R_ctrl)
            cmds.setAttr(str(R_ctrl) + '.rotateZ', rotateValue)
            cmds.parent(locator_tem, world=True)
            cmds.orientConstraint(locator_tem, R_Handle, n=consnode)
            cmds.delete(consnode)
            cmds.delete(locator_tem)

    def studiolibrary(self):
        studio_library_path = '//storage1.of3d.com/centralizedTools/third_party'
        if studio_library_path not in sys.path:
            sys.path.insert(0, studio_library_path)
        import studiolibrary
        reload(studiolibrary)
        studiolibrary.main()
        mel.eval('jAniLib_main();jAniLib_ui_saveType();jAniLib_ui_loadType();')

    def cbdWin(self):
        import sys
        sys.path.insert(0, 'R:\\JueJi\\JueJiTool')
        import combineDirve.combinDriveToolUI as cbdWin
        reload(cbdWin)
        jCombinDirveUI = cbdWin.JunCombinDirveUI()
        jCombinDirveUI.CBDwin()