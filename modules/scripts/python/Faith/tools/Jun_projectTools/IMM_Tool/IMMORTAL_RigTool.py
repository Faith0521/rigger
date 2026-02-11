# coding:utf-8
from imp import reload
import maya.cmds as cmds
import maya.mel as mel
import sys, os
from Rosa.tools.timeline_update import poseDriverTool
from Faith.maya_utils import sdk_utils, decorator_utils
from Faith.maya_utils import rigging_utils


class IMMORTAL_RigTool:

    def __init__(self):
        pass

    def whereAmI(self):
        scriptPath = os.path.split(os.path.abspath(__file__))
        datePath = scriptPath[0].replace('\\', '/')
        Path = datePath.replace('', '')
        return Path

    def win(self):
        bh1 = 40
        winName = 'JunIMMORTAL_RigTool'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t='JunIMMORTAL_RigTool')
        columnLayout1 = cmds.columnLayout(adjustableColumn=True)
        frameLayout1 = cmds.frameLayout(label=u'\u9053\u5177 : -------------------------------------------------', cl=1,
                                        cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(l=u'rollNum', h=20, w=60)
        cmds.textField('rollNumTF', text=1, h=20, w=60)
        cmds.text(l=u'pointNum', h=20, w=60)
        cmds.textField('pointNumTF', text=1, h=20, w=60)
        cmds.setParent(frameLayout1)
        cmds.rowColumnLayout(numberOfColumns=6)
        cmds.button(l=u'<<\u751f\u6210\u9aa8\u9abc>>\n\u9009\u4e2d\u6a21\u578b\u5927\u7ec4',
                    c=lambda *args: self.propsrigTool1(), h=bh1, w=130)
        cmds.separator(style='single')
        cmds.button(
            l=u'<<\u751f\u6210\u63a7\u5236\u5668>>\n\u5148\u8499\u76ae\u4e0d\u7136\u4f1a\u8fd0\u884c\u9519\u8bef\n\u9009\u4e2d\u6a21\u578b\u5927\u7ec4',
            c=lambda *args: self.propsrigTool2(), h=bh1, w=130)
        cmds.separator(style='single')
        cmds.setParent(frameLayout1)
        cmds.setParent('..')
        frameLayout2 = cmds.frameLayout(
            label=u'\u4eba\u7c7b\u89d2\u8272 : -------------------------------------------------', cl=0, cll=True,
            bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=6)
        cmds.button(l=u'\u2605 Rig Update', h=bh1, w=130,
                    annotation=u'#\u5934\u90e8FK\u9aa8\u9abc\u7ec4\u7ea6\u675f\u5934\u90e8IK\u9aa8\u9abc\u7ec4\n#\u624b\u8155\u7684\u9a71\u52a8\u6709\u95ee\u9898\uff0c\u4fee\u6539\u4e00\u4e0b\n#\u5220\u9664\u624b\u6307\u4e0a\u7684\u63e1\u62f3\u5c5e\u6027\n#\u5220\u9664\u624b\u6307\u4e0a\u7684\u63e1\u62f3\u5c5e\u6027\n#\u7ed9\u91cd\u53e0\u9aa8\u9abc\u52a0\u5c42\u6807\u7b7e',
                    c=lambda *args: self.rig_update(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'\u2605 \u63a7\u5236\u5668\u8c03\u6210FK\n\u7edf\u4e00\u63a7\u5236\u5668\u53c2\u6570', h=bh1,
                    w=130, c=lambda *args: self.ctrlDefault(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'\u2605 \u63a7\u5236\u5668\u65e0\u7528\u8f74\u5411\u9501\u5b9a', h=bh1, w=130,
                    c=lambda *args: self.lockCtrlAttr(1, 0), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(
            l=u'\u2605 <<\u663e\u793a\u4e00\u4e9b\u9690\u85cf\u7684\u63a7\u5236\u5668\uff0c\n\u624b\u52a8\u8c03\u6574\u5927\u5c0f\u540e\u9690\u85cf',
            h=bh1, w=130, c=lambda *args: self.showAllCtrl())
        cmds.separator(style='single')
        cmds.button(l=u'\u7ea6\u675f\u516b\u8f74\u8bbe\u7f6e', h=bh1, w=130, c=lambda *args: self.con_bridge())
        cmds.separator(style='single')
        cmds.button(l=u'Create New Pose Driver', h=bh1, w=130, c=lambda *args: self.con_bridge_new())
        cmds.separator(style='single')
        cmds.button(l=u'Fix Arm Twist', h=bh1, w=130, c=lambda *args: self.fixArmTwist())
        cmds.separator(style='single')
        cmds.button(l=u'Create Hand Scale', h=bh1, w=130, c=lambda *args: self.createHandScale())
        cmds.separator(style='single')
        cmds.button(l=u'Create Breathe(Select Mesh)', h=bh1, w=130, c=lambda *args: self.createBreathe())
        cmds.separator(style='single')
        cmds.setParent(frameLayout2)
        cmds.setParent('..')
        frameLayout3 = cmds.frameLayout(label=u'\u901a\u7528 : -------------------------------------------------', cl=0,
                                        cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=6)
        cmds.button(
            l=u'\u2605 <<\u6dfb\u52a0\u706f\u5149\u9aa8\u9abc>>\n\u9ad8\u7ed1,\u9ad8\u7ed1,\u9ad8\u7ed1\n\u9009\u4e2d\u6a21\u578b\u5927\u7ec4',
            h=bh1, w=130, c=lambda *args: self.addLightJnt(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'unlockInfluenceWeights\n(\u9632\u6b62\u6e05\u7406\u5c0f\u6743\u91cd\u9519\u8bef)', h=bh1, w=130,
                    c=lambda *args: self.unlockInfluenceWeights())
        cmds.separator(style='single')
        cmds.button(l=u'\u4fee\u6539\u6240\u6709bs\u8282\u70b9\u547d\u540d', h=bh1, w=130,
                    c=lambda *args: self.checkBlendShapeName(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'\u63a7\u5236\u5668\u7ed1\u5b9a\u548c\nfbx\u7ed1\u5b9abs\u6570\u636e\u5bf9\u6bd4', h=bh1, w=130,
                    c=lambda *args: self.rigBsTarComparisonWin(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.setParent(frameLayout3)
        cmds.setParent('..')
        frameLayout4 = cmds.frameLayout(label=u'\u4e0d\u5e38\u7528: -------------------------------------------------',
                                        cl=1, cll=1, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=6)
        cmds.button(l=u'\u4fee\u590d\u5931\u6548\u7684BS Target', h=bh1, w=130,
                    c=lambda *args: self.repairBlendShapeTar(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'body_ctrl\u548cHips_ctrl\n\u7684\u8f74\u5411\u6539\u6210\u5e73\u7684', h=bh1, w=130,
                    c=lambda *args: self.editBody_ctrlRotate(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.button(l=u'\u6dfb\u52a0\u8170\u90e8\u5927\u73af\nbody02_ctrl', h=bh1, w=130,
                    c=lambda *args: self.add_body02_ctrl(), bgc=[0.75, 0, 0])
        cmds.separator(style='single')
        cmds.setParent(frameLayout4)
        cmds.setParent('..')
        frameLayout4 = cmds.frameLayout(
            label=u'\u6587\u4ef6\u6e05\u7406\uff0c\u51fa\u7eaf\u9aa8\u9abc\u7ed1\u5b9a: -------------------------------------------------',
            cl=1, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=3)
        cmds.button(l=u'\u5220\u9664temp_model\n\u65ad\u5f00\u6240\u6709bs_target\u8fde\u63a5', h=bh1, w=130,
                    c=lambda *args: self.Disconnect_bsTarget(), bgc=[0.75, 0, 0])
        cmds.button(
            l=u'\u5220\u9664\u6240\u6709\u7ea6\u675f\n\u89e3\u9501\u9aa8\u9abc,\u65ad\u5f00\u9aa8\u9abc\u8fde\u63a5\n\u663e\u793a\u9aa8\u9abc',
            h=bh1, w=130, c=lambda *args: self.deleteAllConstraint(), bgc=[0.75, 0, 0])
        cmds.button(l=u'delExpression', h=bh1, w=130, c=lambda *args: self.delExpression(), bgc=[0.75, 0, 0])
        cmds.button(l=u'del bindPose', h=bh1, w=130, c=lambda *args: self.delbindPose(), bgc=[0.75, 0, 0])
        cmds.button(l=u'\u4f4e\u6a21\u9aa8\u9abc\u65e0\u7528\u8f74\u5411\u9501\u5b9a', h=bh1, w=130, bgc=[0.969, 1, 0],
                    c=lambda *args: self.lockmocapJntAttr())
        cmds.button(l=u'特殊骨骼限制', h=bh1, w=130, bgc=[0.969, 1, 0], c=lambda *args: self.lockmocapJntAttr_zt())
        cmds.showWindow()

    def loadObj(self, loadnum, tfName):
        sels = cmds.ls(sl=True)
        if len(sels) == loadnum:
            if loadnum > 1:
                cmds.textField(tfName, e=True, text=sels[:loadnum])
            elif loadnum == 1:
                cmds.textField(tfName, e=True, text=sels[0])
        elif loadnum == '':
            cmds.textField(tfName, e=True, text=sels)
        else:
            cmds.warning(u'\u8bf7\u9009\u62e9' + str(loadnum) + u'\u4e2a\u7269\u4f53')

    def creatCtrCuv(self, cuv, name):
        if cuv == 'sphere':
            cname = cmds.curve(n=name, d=1, p=[(0.504214, 0, 0),
                                               (0.491572, 0.112198, 0),
                                               (0.454281, 0.21877, 0),
                                               (0.394211, 0.314372, 0),
                                               (0.314372, 0.394211, 0),
                                               (0.21877, 0.454281, 0),
                                               (0.112198, 0.491572, 0),
                                               (0, 0.504214, 0),
                                               (-0.112198, 0.491572, 0),
                                               (-0.21877, 0.454281, 0),
                                               (-0.314372, 0.394211, 0),
                                               (-0.394211, 0.314372, 0),
                                               (-0.454281, 0.21877, 0),
                                               (-0.491572, 0.112198, 0),
                                               (-0.504214, 0, 0),
                                               (-0.491572, -0.112198, 0),
                                               (-0.454281, -0.21877, 0),
                                               (-0.394211, -0.314372, 0),
                                               (-0.314372, -0.394211, 0),
                                               (-0.21877, -0.454281, 0),
                                               (-0.112198, -0.491572, 0),
                                               (0, -0.504214, 0),
                                               (0.112198, -0.491572, 0),
                                               (0.21877, -0.454281, 0),
                                               (0.314372, -0.394211, 0),
                                               (0.394211, -0.314372, 0),
                                               (0.454281, -0.21877, 0),
                                               (0.491572, -0.112198, 0),
                                               (0.504214, 0, 0),
                                               (0.491572, 0, -0.112198),
                                               (0.454281, 0, -0.21877),
                                               (0.394211, 0, -0.314372),
                                               (0.314372, 0, -0.394211),
                                               (0.21877, 0, -0.454281),
                                               (0.112198, 0, -0.491572),
                                               (0, 0, -0.504214),
                                               (-0.112198, 0, -0.491572),
                                               (-0.21877, 0, -0.454281),
                                               (-0.314372, 0, -0.394211),
                                               (-0.394211, 0, -0.314372),
                                               (-0.454281, 0, -0.21877),
                                               (-0.491572, 0, -0.112198),
                                               (-0.504214, 0, 0),
                                               (-0.491572, 0, 0.112198),
                                               (-0.454281, 0, 0.21877),
                                               (-0.394211, 0, 0.314372),
                                               (-0.314372, 0, 0.394211),
                                               (-0.21877, 0, 0.454281),
                                               (-0.112198, 0, 0.491572),
                                               (0, 0, 0.504214),
                                               (0, 0.112198, 0.491572),
                                               (0, 0.21877, 0.454281),
                                               (0, 0.314372, 0.394211),
                                               (0, 0.394211, 0.314372),
                                               (0, 0.454281, 0.21877),
                                               (0, 0.491572, 0.112198),
                                               (0, 0.504214, 0),
                                               (0, 0.491572, -0.112198),
                                               (0, 0.454281, -0.21877),
                                               (0, 0.394211, -0.314372),
                                               (0, 0.314372, -0.394211),
                                               (0, 0.21877, -0.454281),
                                               (0, 0.112198, -0.491572),
                                               (0, 0, -0.504214),
                                               (0, -0.112198, -0.491572),
                                               (0, -0.21877, -0.454281),
                                               (0, -0.314372, -0.394211),
                                               (0, -0.394211, -0.314372),
                                               (0, -0.454281, -0.21877),
                                               (0, -0.491572, -0.112198),
                                               (0, -0.504214, 0),
                                               (0, -0.491572, 0.112198),
                                               (0, -0.454281, 0.21877),
                                               (0, -0.394211, 0.314372),
                                               (0, -0.314372, 0.394211),
                                               (0, -0.21877, 0.454281),
                                               (0, -0.112198, 0.491572),
                                               (0, 0, 0.504214),
                                               (0.112198, 0, 0.491572),
                                               (0.21877, 0, 0.454281),
                                               (0.314372, 0, 0.394211),
                                               (0.394211, 0, 0.314372),
                                               (0.454281, 0, 0.21877),
                                               (0.491572, 0, 0.112198),
                                               (0.504214, 0, 0)])
        if cuv == 'cube':
            cname = cmds.curve(n=name, d=1, p=[(-5, 5, 5),
                                               (5, 5, 5),
                                               (5, 5, -5),
                                               (-5, 5, -5),
                                               (-5, 5, 5),
                                               (-5, -5, 5),
                                               (-5, -5, -5),
                                               (5, -5, -5),
                                               (5, -5, 5),
                                               (-5, -5, 5),
                                               (5, -5, 5),
                                               (5, 5, 5),
                                               (5, 5, -5),
                                               (5, -5, -5),
                                               (-5, -5, -5),
                                               (-5, 5, -5)])
        if cuv == 'locator':
            cname = cmds.curve(n=name, d=1, p=[(0, 0.5, 0),
                                               (0, -0.5, 0),
                                               (0, 0, 0),
                                               (-0.5, 0, 0),
                                               (0.5, 0, 0),
                                               (0, 0, 0),
                                               (0, 0, 0.5),
                                               (0, 0, -0.5)])
        if cuv == 'circleArrow2':
            cname = cmds.curve(n=name, d=1, p=[(0.0, 0.0, 0.972),
                                               (0.289, 0.0, 0.683),
                                               (0.144, 0.0, 0.683),
                                               (0.144, 0.0, 0.538),
                                               (0.17, 0.0, 0.532),
                                               (0.216, 0.0, 0.516),
                                               (0.28, 0.0, 0.485),
                                               (0.341, 0.0, 0.444),
                                               (0.396, 0.0, 0.396),
                                               (0.444, 0.0, 0.341),
                                               (0.485, 0.0, 0.28),
                                               (0.516, 0.0, 0.216),
                                               (0.532, 0.0, 0.17),
                                               (0.539, 0.0, 0.144),
                                               (0.683, 0.0, 0.144),
                                               (0.683, 0.0, 0.289),
                                               (0.972, 0.0, 0.0),
                                               (0.683, 0.0, -0.289),
                                               (0.683, 0.0, -0.144),
                                               (0.538, 0.0, -0.144),
                                               (0.532, 0.0, -0.17),
                                               (0.516, 0.0, -0.216),
                                               (0.485, 0.0, -0.28),
                                               (0.444, 0.0, -0.341),
                                               (0.396, 0.0, -0.396),
                                               (0.341, 0.0, -0.444),
                                               (0.28, 0.0, -0.485),
                                               (0.216, 0.0, -0.516),
                                               (0.17, 0.0, -0.532),
                                               (0.144, 0.0, -0.539),
                                               (0.144, 0.0, -0.683),
                                               (0.289, 0.0, -0.683),
                                               (0.0, 0.0, -0.972),
                                               (-0.289, 0.0, -0.683),
                                               (-0.144, 0.0, -0.683),
                                               (-0.144, 0.0, -0.538),
                                               (-0.17, 0.0, -0.532),
                                               (-0.216, 0.0, -0.516),
                                               (-0.28, 0.0, -0.485),
                                               (-0.341, 0.0, -0.444),
                                               (-0.396, 0.0, -0.396),
                                               (-0.444, 0.0, -0.341),
                                               (-0.485, 0.0, -0.28),
                                               (-0.516, 0.0, -0.216),
                                               (-0.532, 0.0, -0.17),
                                               (-0.539, 0.0, -0.144),
                                               (-0.683, 0.0, -0.144),
                                               (-0.683, 0.0, -0.289),
                                               (-0.972, 0.0, 0.0),
                                               (-0.683, 0.0, 0.289),
                                               (-0.683, 0.0, 0.144),
                                               (-0.538, 0.0, 0.144),
                                               (-0.533, 0.0, 0.168),
                                               (-0.517, 0.0, 0.214),
                                               (-0.485, 0.0, 0.28),
                                               (-0.444, 0.0, 0.341),
                                               (-0.396, 0.0, 0.396),
                                               (-0.341, 0.0, 0.444),
                                               (-0.28, 0.0, 0.485),
                                               (-0.216, 0.0, 0.516),
                                               (-0.17, 0.0, 0.532),
                                               (-0.144, 0.0, 0.539),
                                               (-0.144, 0.0, 0.683),
                                               (-0.289, 0.0, 0.683),
                                               (0.0, 0.0, 0.972)])
        if cuv == 'circle':
            cname = cmds.circle(n=name, nr=[0, 1, 0], r=0.5, ch=0)
        return cname

    def checkRigMode(self):
        RigMode = 'Y_Front'
        jntList = cmds.ls(type='joint')
        upJntNum = jntList.count(upJnt)
        botJntNum = jntList.count(botJnt)
        leftJntNum = jntList.count(leftJnt)
        rightJntNum = jntList.count(rightJnt)
        if upJntNum + botJntNum > leftJntNum + rightJntNum:
            RigMode = 'Y_Front'
        elif upJntNum + botJntNum < leftJntNum + rightJntNum:
            RigMode = 'Z_Front'
        return RigMode

    def propsrigTool1(self):
        namePre = cmds.ls(sl=1)[0]
        cmds.select(namePre)
        self.rootJnt = namePre + '_Hips'
        if not cmds.objExists(self.rootJnt):
            cmds.joint(n=self.rootJnt)
            cmds.setAttr(self.rootJnt + '.t', lock=1)
            cmds.setAttr(self.rootJnt + '.r', lock=1)
            cmds.setAttr(self.rootJnt + '.s', lock=1)
        cmds.select(self.rootJnt)
        upJnt = namePre + '_Up'
        if not cmds.objExists(upJnt):
            cmds.joint(n=upJnt)
            cmds.setAttr(upJnt + '.ty', 5)
        cmds.select(self.rootJnt)
        botJnt = namePre + '_Bottom'
        if not cmds.objExists(botJnt):
            cmds.joint(n=botJnt)
            cmds.setAttr(botJnt + '.ty', -5)
        cmds.select(self.rootJnt)
        leftJnt = namePre + '_Left'
        if not cmds.objExists(leftJnt):
            cmds.joint(n=leftJnt)
            cmds.setAttr(leftJnt + '.tx', 5)
        cmds.select(self.rootJnt)
        rightJnt = namePre + '_Right'
        if not cmds.objExists(rightJnt):
            cmds.joint(n=rightJnt)
            cmds.setAttr(rightJnt + '.tx', -5)
        cmds.select(self.rootJnt)
        frontJnt = namePre + '_Front'
        if not cmds.objExists(frontJnt):
            cmds.joint(n=frontJnt)
            cmds.setAttr(frontJnt + '.tz', 5)
        cmds.select(self.rootJnt)
        backJnt = namePre + '_Back'
        if not cmds.objExists(backJnt):
            cmds.joint(n=backJnt)
            cmds.setAttr(backJnt + '.tz', -5)
        self.rollNum = int(cmds.textField('rollNumTF', q=True, text=True))
        self.pointNum = int(cmds.textField('pointNumTF', q=True, text=True))
        self.geoName = self.rootJnt[:-len('_Hips')]
        if self.rollNum >= 1:
            self.RollLoc = cmds.spaceLocator(n=self.geoName + '_roll_Loc')
            if self.rollNum >= 2:
                self.HandleLoc = cmds.spaceLocator(n=self.geoName + '_handle_loc')

    def propsrigTool2(self):
        self.rollNum = int(cmds.textField('rollNumTF', q=True, text=True))
        self.pointNum = int(cmds.textField('pointNumTF', q=True, text=True))
        namePre = cmds.ls(sl=1)[0]
        self.rootJnt = namePre + '_Hips'
        self.geoName = self.rootJnt[:-len('_Hips')]
        if self.rollNum >= 1:
            self.RollLoc = self.geoName + '_roll_Loc'
            if self.rollNum >= 2:
                self.HandleLoc = self.geoName + '_handle_loc'
        cmds.setAttr(self.rootJnt + '.t', lock=0)
        cmds.setAttr(self.rootJnt + '.r', lock=0)
        cmds.setAttr(self.rootJnt + '.s', lock=0)
        JntList = cmds.ls(type='joint')
        checkJntList = set(JntList)
        for checkJnt in checkJntList:
            count = 0
            checkJntSpList = checkJnt.split('|')
            checkJnt = checkJntSpList[-1]
            print(checkJnt)
            for jnt in JntList:
                jntSpList = jnt.split('|')
                jnt = jntSpList[-1]
                if checkJnt == jnt:
                    count += 1
                    if count > 1:
                        mel.eval('warning "Have same name!"')
                        break
                    else:
                        ctrlList = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), r=8, sw=360, ch=0, n=jnt + '_ctrl')
                        ctrl = ctrlList[0]
                        cmds.setAttr(ctrl + '.overrideEnabled', 1)
                        cmds.setAttr(ctrl + '.overrideColor', 17)
                        cmds.setAttr(ctrl + '.sx', l=1, k=0, cb=0)
                        cmds.setAttr(ctrl + '.sy', l=1, k=0, cb=0)
                        cmds.setAttr(ctrl + '.sz', l=1, k=0, cb=0)
                        cmds.makeIdentity(ctrl, apply=1, r=1)
                        grpName = ctrl + '_zero'
                        ctrlGrp = cmds.group(ctrl, n=grpName)
                        cons = cmds.parentConstraint(jnt, ctrlGrp)
                        cmds.delete(cons)
                        cmds.parentConstraint(ctrl, jnt)
                        cmds.scaleConstraint(ctrl, jnt)

        HipsCtrlLsit = cmds.ls('*Hips_ctrl*', type='transform')
        for obj in HipsCtrlLsit:
            obj = str(obj)
            cmds.rename(obj, obj.replace('Hips', 'root'))

        cubeRootCur = self.creatCtrCuv('cube', 'cube_' + self.geoName + '_root_ctrl')
        cubeRootCurShape = cmds.listRelatives(cubeRootCur, c=1, ni=1)[0]
        OldRootCurShape = cmds.listRelatives(self.geoName + '_root_ctrl', c=1, ni=1)[0]
        cmds.delete(OldRootCurShape)
        cubeRootCurShape = cmds.rename(cubeRootCurShape, OldRootCurShape)
        cmds.parent(cubeRootCurShape, self.geoName + '_root_ctrl', add=1, s=1)
        cmds.delete(cubeRootCur)
        meshList = cmds.ls(type='mesh', ni=1)
        meshTList = []
        for shape in meshList:
            tObj = cmds.listRelatives(shape, p=1)[0]
            if tObj not in meshTList:
                meshTList.append(tObj)

        cmds.select(JntList, meshTList)
        mel.eval('skinClusterInfluence 1 "-ug -dr 4 -ps 0 -ns 10 -lw true -wt 0";')
        mel.eval('AddInfluence')
        for shape in meshList:
            cnn = cmds.listConnections(shape + '.inMesh', c=1)
            if cnn != None:
                cmds.select(shape)
                mel.eval('removeUnusedInfluences;')

        uiJntList = []
        infJntList = []
        for jnt in JntList:
            cmds.setAttr(jnt + '.radius', 1)
            cnn = cmds.listConnections(jnt + '.lockInfluenceWeights', c=1)
            if not cnn:
                uiJntList.append(jnt)
            else:
                infJntList.append(jnt)
            pjntList = cmds.listRelatives(jnt, p=1)
            if pjntList != None:
                pjnt = pjntList[0]
                pctrl = pjnt + '_ctrl'
                if cmds.objExists(pctrl + '_zero'):
                    cmds.parent(jnt + '_ctrl_zero', pctrl)

        i = 0
        PuiJntList = []
        for i in range(len(uiJntList)):
            jntChList = cmds.listRelatives(uiJntList[i], ad=1, type='joint')
            if jntChList == None:
                cmds.delete(uiJntList[i] + '_ctrl_zero', hi=1)
            if jntChList != None:
                PuiJntList.append(uiJntList[i])

        allctrlName = 'all_ctrl'
        allctrlgrpName = allctrlName + '_zero'
        allctrl = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), r=15, sw=360, ch=0, n=allctrlName)[0]
        cmds.setAttr(allctrl + '.overrideEnabled', 1)
        cmds.setAttr(allctrl + '.overrideColor', 17)
        allctrlGrp = cmds.group(allctrl, n=allctrl + '_zero')
        cmds.parent(self.geoName + '_root_ctrl_zero', allctrl)
        globalName = 'global_ctrl'
        globalgrpName = globalName + '_zero'
        globalctrl = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), r=25, sw=360, ch=0, n=globalName)[0]
        cmds.setAttr(globalctrl + '.overrideEnabled', 1)
        cmds.setAttr(globalctrl + '.overrideColor', 25)
        globalctrlGrp = cmds.group(globalctrl, n=globalctrl + '_zero')
        cmds.parent(allctrlGrp, globalctrl)
        wdctrlName = 'world_ctrl'
        wdctrlgrpName = wdctrlName + '_zero'
        wdctrl = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), r=30, sw=360, ch=0, n=wdctrlName)[0]
        cmds.setAttr(wdctrl + '.overrideEnabled', 1)
        cmds.setAttr(wdctrl + '.overrideColor', 17)
        wdctrlGrp = cmds.group(wdctrl, n=wdctrl + '_zero')
        cmds.parent(globalctrlGrp, wdctrl)
        rig_all_grp_Name = str(self.geoName)
        if not cmds.objExists(rig_all_grp_Name):
            rig_all_grp = cmds.group(em=1, n=rig_all_grp_Name)
        if self.rollNum >= 2:
            con = cmds.listRelatives(self.rootJnt, c=1, type='parentConstraint')[0]
            cmds.delete(con)
            rollzeroGrp = cmds.group(em=1, n=self.geoName + '_roll_ctrl_zero')
            rollctr = self.creatCtrCuv('circle', self.geoName + '_roll_ctrl')[0]
            cmds.setAttr(rollctr + '.overrideEnabled', 1)
            cmds.setAttr(rollctr + '.overrideColor', 21)
            cmds.scale(15, 15, 15, rollctr)
            cmds.makeIdentity(rollctr, apply=1, t=0, r=0, s=1, n=0, pn=1)
            cmds.parent(rollctr, rollzeroGrp)
            cmds.parentConstraint(self.RollLoc, rollzeroGrp, weight=1)
            cmds.delete(self.RollLoc)
            handlezeroGrp = cmds.group(em=1, n=self.geoName + '_handle_ctrl_zero')
            handlectr = self.creatCtrCuv('circle', self.geoName + '_handle_ctrl')[0]
            cmds.setAttr(handlectr + '.overrideEnabled', 1)
            cmds.setAttr(handlectr + '.overrideColor', 17)
            cmds.scale(10, 10, 10, handlectr)
            cmds.makeIdentity(handlectr, apply=1, t=0, r=0, s=1, n=0, pn=1)
            cmds.parent(handlectr, handlezeroGrp)
            cmds.parentConstraint(self.HandleLoc, handlezeroGrp, weight=1)
            cmds.delete(self.HandleLoc)
            oldC = cmds.listRelatives(self.geoName + '_root_ctrl', c=1, typ='transform')
            if oldC != None:
                cmds.parent(oldC, rollctr)
            cmds.parent(handlezeroGrp, self.geoName + '_root_ctrl')
            cmds.parent(rollzeroGrp, handlectr)
            cmds.parentConstraint(rollctr, self.rootJnt, mo=1)
        else:
            con = cmds.listRelatives(self.rootJnt, c=1, type='parentConstraint')[0]
            cmds.delete(con)
            rollzeroGrp = cmds.group(em=1, n=self.geoName + '_roll_ctrl_zero')
            rollctr = self.creatCtrCuv('circle', self.geoName + '_roll_ctrl')[0]
            cmds.setAttr(rollctr + '.overrideEnabled', 1)
            cmds.setAttr(rollctr + '.overrideColor', 21)
            cmds.parent(rollctr, rollzeroGrp)
            cmds.parentConstraint(self.RollLoc, rollzeroGrp, weight=1)
            cmds.delete(self.RollLoc)
            cmds.scale(10, 10, 10, rollctr)
            cmds.setAttr(rollctr + '.ry', 0)
            cmds.makeIdentity(rollctr, apply=1, t=1, r=1, s=1, n=0, pn=1)
            oldC = cmds.listRelatives(self.geoName + '_root_ctrl', c=1, typ='transform')
            if oldC != None:
                cmds.parent(oldC, rollctr)
            cmds.parent(rollzeroGrp, self.geoName + '_root_ctrl')
            cmds.parentConstraint(rollctr, self.rootJnt, mo=1)
        if self.pointNum >= 1:
            for i in range(self.pointNum):
                i += 1
                CurpointNum = '%d' % i
                pointzeroGrp = cmds.group(em=1, n=self.geoName + '_point_' + CurpointNum + '_ctrl' + '_zero')
                pointctr = self.creatCtrCuv('locator', self.geoName + '_point_' + CurpointNum + '_ctrl')
                cmds.setAttr(pointctr + '.overrideEnabled', 1)
                cmds.setAttr(pointctr + '.overrideColor', 18)
                cmds.scale(8, 8, 8, pointctr)
                cmds.makeIdentity(pointctr, apply=1, t=0, r=0, s=1, n=0, pn=1)
                cmds.parent(pointctr, pointzeroGrp)
                cmds.parent(pointzeroGrp, rollctr)
                for Attr in ['sx',
                             'sy',
                             'sz',
                             'visibility']:
                    cmds.setAttr(pointctr + '.' + Attr, lock=1, keyable=0, channelBox=0)

        for jnt in infJntList:
            if cmds.listRelatives(jnt, p=1, type='joint') != None and cmds.listRelatives(jnt + '_ctrl_zero',
                                                                                         p=1) == None:
                pJnt = cmds.listRelatives(jnt, p=1, type='joint')[0]
                pCon = cmds.listConnections(pJnt + '.tx', s=1)[0]
                pCtrlList = cmds.listConnections(pCon + '.target', s=1)
                for Ctrl in pCtrlList:
                    if Ctrl[-4:] == 'ctrl':
                        pCtrl = Ctrl

                cmds.parent(jnt + '_ctrl_zero', pCtrl)

        crateN = cmds.textCurves(n=self.geoName + '_name_cur_', ch=1, f='Times New Roman|h-500|w2000|c0',
                                 t=self.geoName)
        selShapeAll = cmds.listRelatives(crateN, c=1)
        sel = cmds.listRelatives(selShapeAll, c=1)
        for i in sel[1:]:
            selShape = cmds.listRelatives(i, s=1, f=1)
            for s in selShape:
                newShape = cmds.rename(s, sel[0].split('|')[-1] + 'Shape')
                cmds.parent(i, sel[0])
                cmds.makeIdentity(i, apply=1, t=1, r=1, s=1, n=0)
                cmds.parent(i, w=1)
                cmds.parent(newShape, sel[0], r=1, s=1)

            cmds.delete(i)

        for a in range(1, len(selShapeAll)):
            selShapeTall = selShapeAll[a]
            cmds.delete(selShapeTall)

        cmds.setAttr(sel[0] + '.overrideEnabled', 1)
        cmds.setAttr(sel[0] + '.overrideColor', 17)
        cmds.setAttr(sel[0] + '.scaleX', 2)
        cmds.setAttr(sel[0] + '.scaleY', 2)
        cmds.setAttr(sel[0] + '.scaleZ', 2)
        cmds.xform(crateN, cpc=1)
        cmds.addAttr(sel[0], ln='Mod_Type', at='enum', en='Nor:Ref:Hide:', k=1)
        cmds.addAttr(sel[0], ln='CtrlVis', at='enum', en='On:Off:', k=1)
        cmds.setAttr('world_ctrl_zero.overrideEnabled', 1)
        revNode = cmds.createNode('reverse', n='rev_ctrl')
        cmds.connectAttr(sel[0] + '.CtrlVis', revNode + '.inputX', f=1)
        cmds.connectAttr(revNode + '.outputX', 'world_ctrl_zero.drawOverride.overrideVisibility')
        conRef = cmds.createNode('condition', n=self.geoName + '_con_Ref')
        conHide = cmds.createNode('condition', n=self.geoName + '_con_Hide')
        cmds.setAttr(conRef + '.secondTerm', 1)
        cmds.setAttr(conRef + '.colorIfFalseR', 0)
        cmds.setAttr(conRef + '.colorIfTrueR', 2)
        cmds.setAttr(conHide + '.secondTerm', 2)
        cmds.setAttr(conHide + '.colorIfFalseR', 1)
        cmds.setAttr(conHide + '.colorIfTrueR', 0)
        cmds.connectAttr(sel[0] + '.Mod_Type', conRef + '.firstTerm', f=1)
        cmds.connectAttr(sel[0] + '.Mod_Type', conHide + '.firstTerm', f=1)
        shapeList = cmds.ls(type='mesh', ni=1)
        for shape in shapeList:
            cmds.setAttr(shape + '.overrideEnabled', 1)
            cmds.connectAttr(conHide + '.outColorR', shape + '.overrideVisibility', f=1)
            cmds.connectAttr(conRef + '.outColorR', shape + '.overrideDisplayType', f=1)

        cmds.connectAttr(conHide + '.outColorR', self.geoName + '_Hips.visibility')
        cmds.connectAttr(conHide + '.outColorR', 'world_ctrl_zero.visibility')
        rootCtrl = cmds.ls('*_root_ctrl')
        # raise rootCtrl or AssertionError
        rootCtrl = rootCtrl[0]
        cmds.pointConstraint(rootCtrl, crateN, w=1, e=0)
        cmds.delete(crateN[0] + '_pointConstraint1')
        RigAllCtrl = cmds.group(em=1, w=1, n='rig_grp')
        # raise RigAllCtrl or AssertionError
        cmds.parent(crateN[0], RigAllCtrl)
        cmds.makeIdentity(crateN[0], apply=1, t=1, r=1, s=1, n=0)
        for Attr in ['tx',
                     'ty',
                     'tz',
                     'rx',
                     'ry',
                     'rz',
                     'sx',
                     'sy',
                     'sz',
                     'visibility']:
            cmds.setAttr(sel[0] + '.' + Attr, lock=1, keyable=0, channelBox=0)

        cmds.parent('world_ctrl_zero', 'rig_grp')
        cmds.parent('rig_grp', self.geoName)
        jntList = cmds.ls(type='joint')
        self.rootJnt = cmds.ls('*_Hips')[0]
        rootCtr = self.rootJnt[:-5] + '_root_ctrl'
        for Attr in ['.sx',
                     '.sy',
                     '.sz',
                     '.v']:
            cmds.setAttr('all_ctrl' + Attr, k=0, l=1)
            cmds.setAttr('global_ctrl' + Attr, k=0, l=1)
            cmds.setAttr(rootCtr + Attr, k=0, l=1)
            cmds.setAttr(rollctr + Attr, k=0, l=1)
            if self.rollNum >= 2:
                cmds.setAttr(handlectr + Attr, k=0, l=1)

        cmds.scaleConstraint(rootCtr, self.rootJnt, mo=1)
        cmds.delete(sel[0], ch=1)
        cmds.disconnectAttr(crateN[1] + '.position[0]', selShapeAll[0] + '.translate')
        nameCur = cmds.rename(sel[0], self.geoName + '_name_cur')
        cmds.pointConstraint(rootCtrl, crateN[0], w=1, mo=1, e=0)
        cmds.parent(nameCur + '_Shape', 'world_ctrl')
        cmds.delete(namePre + '_name_cur_Shape')
        cmds.setAttr('world_ctrl.v', lock=True, channelBox=0, keyable=0)
        return

    def createAssetText(self):
        crateN = cmds.textCurves(n=self.geoName + '_name_cur_', ch=1, f='Times New Roman|h-500|w2000|c0',
                                 t=self.geoName)
        selShapeAll = cmds.listRelatives(crateN, c=1)
        sel = cmds.listRelatives(selShapeAll, c=1)
        for i in sel[1:]:
            selShape = cmds.listRelatives(i, s=1, f=1)
            for s in selShape:
                newShape = cmds.rename(s, sel[0].split('|')[-1] + 'Shape')
                cmds.parent(i, sel[0])
                cmds.makeIdentity(i, apply=1, t=1, r=1, s=1, n=0)
                cmds.parent(i, w=1)
                cmds.parent(newShape, sel[0], r=1, s=1)

            cmds.delete(i)

        for a in range(1, len(selShapeAll)):
            selShapeTall = selShapeAll[a]
            cmds.delete(selShapeTall)

        cmds.setAttr(sel[0] + '.overrideEnabled', 1)
        cmds.setAttr(sel[0] + '.overrideColor', 17)
        cmds.setAttr(sel[0] + '.scaleX', 2)
        cmds.setAttr(sel[0] + '.scaleY', 2)
        cmds.setAttr(sel[0] + '.scaleZ', 2)
        cmds.xform(crateN, cpc=1)
        cmds.addAttr(sel[0], ln='Mod_Type', at='enum', en='Nor:Ref:Hide:', k=1)
        cmds.addAttr(sel[0], ln='CtrlVis', at='enum', en='On:Off:', k=1)
        cmds.setAttr('world_ctrl_zero.overrideEnabled', 1)
        revNode = cmds.createNode('reverse', n='rev_ctrl')
        cmds.connectAttr(sel[0] + '.CtrlVis', revNode + '.inputX', f=1)
        cmds.connectAttr(revNode + '.outputX', 'world_ctrl_zero.drawOverride.overrideVisibility')
        conRef = cmds.createNode('condition', n=self.geoName + '_con_Ref')
        conHide = cmds.createNode('condition', n=self.geoName + '_con_Hide')
        cmds.setAttr(conRef + '.secondTerm', 1)
        cmds.setAttr(conRef + '.colorIfFalseR', 0)
        cmds.setAttr(conRef + '.colorIfTrueR', 2)
        cmds.setAttr(conHide + '.secondTerm', 2)
        cmds.setAttr(conHide + '.colorIfFalseR', 1)
        cmds.setAttr(conHide + '.colorIfTrueR', 0)
        cmds.connectAttr(sel[0] + '.Mod_Type', conRef + '.firstTerm', f=1)
        cmds.connectAttr(sel[0] + '.Mod_Type', conHide + '.firstTerm', f=1)
        shapeList = cmds.ls(type='mesh', ni=1)
        for shape in shapeList:
            cmds.setAttr(shape + '.overrideEnabled', 1)
            cmds.connectAttr(conHide + '.outColorR', shape + '.overrideVisibility', f=1)
            cmds.connectAttr(conRef + '.outColorR', shape + '.overrideDisplayType', f=1)

        cmds.connectAttr(conHide + '.outColorR', self.geoName + '_Hips.visibility')
        cmds.connectAttr(conHide + '.outColorR', 'world_ctrl_zero.visibility')
        rootCtrl = cmds.ls('*_root_ctrl')
        raise rootCtrl or AssertionError
        rootCtrl = rootCtrl[0]
        cmds.pointConstraint(rootCtrl, crateN, w=1, e=0)
        cmds.delete(crateN[0] + '_pointConstraint1')

    def delpropsctrl(self):
        rootGrp = cmds.ls(sl=1)[0]
        JntList = []
        JntList = cmds.listRelatives(rootGrp, ad=1, type='joint')
        for jnt in JntList:
            for attr in ['tx',
                         'ty',
                         'tz',
                         'rx',
                         'ry',
                         'rz',
                         'sx',
                         'sy',
                         'sz',
                         'visibility']:
                cnn = cmds.listConnections(jnt + '.' + attr, d=0, s=1, p=1)
                if not cnn:
                    continue
                cnn = cnn[0]
                cmds.disconnectAttr(cnn, jnt + '.' + attr)

        con = cmds.ls(type='constraint')
        cmds.delete(con)
        if cmds.objExists('rig_grp'):
            cmds.delete('rig_grp')
        EXP = cmds.ls(type='expression')
        cmds.delete(EXP)
        Bpose = cmds.ls(type='dagPose')
        cmds.delete(Bpose)
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

    def rig_update_all(self):
        self.rig_update()
        self.ctrlDefault()
        self.lockCtrlAttr(1, 0)
        sys.stderr.write(
            u'------rig update------\u63a7\u5236\u5668\u7edf\u4e00\u8bbe\u7f6e------\u63a7\u5236\u5668\u65e0\u7528\u65cb\u8f6c\u8f74\u9501\u5b9a')

    def rig_update(self):
        if cmds.objExists('neck_fk_ctrl_grp') == True and cmds.objExists('neck_ik_jnt_grp') == True:
            cmds.parentConstraint('neck_fk_ctrl_grp', 'neck_ik_jnt_grp', mo=1)
            print(u'\u5934\u90e8FK\u9aa8\u9abc\u7ec4\u7ea6\u675f\u5934\u90e8IK\u9aa8\u9abc\u7ec4')
        if cmds.objExists('L_hand_dr_angleDriver_handle_pointConstraint1') == True:
            cmds.delete('L_hand_dr_angleDriver_handle_pointConstraint1')
            cmds.parentConstraint('L_lowarm_sec5_dr', 'L_hand_dr_angleDriver_handle', mo=True)
        if cmds.objExists('R_hand_dr_angleDriver_handle_pointConstraint1') == True:
            cmds.delete('R_hand_dr_angleDriver_handle_pointConstraint1')
            cmds.parentConstraint('R_lowarm_sec5_dr', 'L_hand_dr_angleDriver_handle', mo=True)
            print(u'\u624b\u8155\u7684\u9a71\u52a8\u6709\u95ee\u9898\uff0c\u4fee\u6539\u4e00\u4e0b')
        hideAttrs = ['thumb',
                     'index',
                     'middle',
                     'ring',
                     'pinky']
        armikfkCtrls = ['L_arm_switch_ctrl', 'R_arm_switch_ctrl']
        a = []
        for armikfkCtrl in armikfkCtrls:
            if cmds.objExists(armikfkCtrl) == True:
                armikfkCtrlAttrs = cmds.listAttr(armikfkCtrl)
                for hideAttr in hideAttrs:
                    if hideAttr in armikfkCtrlAttrs:
                        cmds.setAttr(armikfkCtrl + '.' + hideAttr, lock=1, keyable=0, channelBox=0)
                        a.append(hideAttr)

        if a != []:
            print(u'\u5220\u9664\u624b\u6307\u4e0a\u7684\u63e1\u62f3\u5c5e\u6027')
        a = []
        for jnt in ['ForeArm',
                    'Arm_sec4',
                    'Hand',
                    'ForeArm_sec4',
                    'Leg',
                    'UpLeg_sec4',
                    'Foot',
                    'Leg_sec4']:
            if cmds.objExists('Left' + jnt):
                cmds.setAttr('Left' + jnt + '.side', 1)
                cmds.setAttr('Left' + jnt + '.type', 18)
                cmds.setAttr('Left' + jnt + '.otherType', '%s' % jnt, type='string')
                a.append(1)
            if cmds.objExists('Right' + jnt):
                cmds.setAttr('Right' + jnt + '.side', 2)
                cmds.setAttr('Right' + jnt + '.type', 18)
                cmds.setAttr('Right' + jnt + '.otherType', '%s' % jnt, type='string')
                a.append(1)

        for jnt in ['Hips', 'Spine']:
            if cmds.objExists(jnt):
                cmds.setAttr(jnt + '.type', 18)
                cmds.setAttr(jnt + '.otherType', '%s' % jnt, type='string')
                a.append(1)

        if a != []:
            print(u'\u7ed9\u91cd\u53e0\u9aa8\u9abc\u52a0\u5c42\u6807\u7b7e')
        ctrls = [u'spine_5_ctrl',
                 u'chect_mid_ctrl',
                 u'spine_3_ctrl',
                 u'spine_1_ctrl']
        self.connAttr('body_ctrl.fkVis', ctrls, 1, 'v', 1)
        ctrls = [u'L_thumbfinger_ctrl',
                 u'L_middlefinger_ctrl',
                 u'L_indexfinger_ctrl',
                 u'L_ringfinger_ctrl',
                 u'L_pinkyfinger_ctrl']
        self.connAttr('L_arm_switch_ctrl.fingerRootVis', ctrls, 1, 'v', 1)
        ctrls = [u'R_thumbfinger_ctrl',
                 u'R_middlefinger_ctrl',
                 u'R_indexfinger_ctrl',
                 u'R_ringfinger_ctrl',
                 u'R_pinkyfinger_ctrl']
        self.connAttr('R_arm_switch_ctrl.fingerRootVis', ctrls, 1, 'v', 1)
        ctrls = ['L_arm_fk_root_ctrl']
        self.connAttr('L_arm_fk_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['R_arm_fk_root_ctrl']
        self.connAttr('R_arm_fk_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['L_arm_ik_root_ctrl']
        self.connAttr('L_arm_ik_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['R_arm_ik_root_ctrl']
        self.connAttr('R_arm_ik_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['L_leg_fk_root_ctrl']
        self.connAttr('L_leg_fk_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['R_leg_fk_root_ctrl']
        self.connAttr('R_leg_fk_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['L_leg_ik_root_ctrl']
        self.connAttr('L_leg_ik_ctrl.rootVis', ctrls, 1, 'v', 1)
        ctrls = ['R_leg_ik_root_ctrl']
        self.connAttr('R_leg_ik_ctrl.rootVis', ctrls, 1, 'v', 1)
        if cmds.getAttr('L_arm_switch_ctrl.fingerRootVis') == 1:
            cmds.setAttr('L_arm_switch_ctrl.fingerRootVis', lock=0)
            cmds.setAttr('L_arm_switch_ctrl.fingerRootVis', 0)
        cmds.setAttr('L_arm_switch_ctrl.fingerRootVis', lock=1, keyable=0)
        if cmds.getAttr('R_arm_switch_ctrl.fingerRootVis') == 1:
            cmds.setAttr('R_arm_switch_ctrl.fingerRootVis', lock=0)
            cmds.setAttr('R_arm_switch_ctrl.fingerRootVis', 0)
        cmds.setAttr('R_arm_switch_ctrl.fingerRootVis', lock=1, keyable=0)
        print(u'\u4ee5\u4e0a\u4e3a\u5347\u7ea7\u5185\u5bb9')
        sys.stderr.write(u'------\u5347\u7ea7 is ok')

    def connAttr(self, outputAttr, inputObjs, conShape, inputAttr, forceCon):
        for inputObj in inputObjs:
            if cmds.objExists(inputObj) == True:
                if conShape == 1:
                    inputObjshapes = cmds.listRelatives(inputObj, s=True)
                    if inputObjshapes != None:
                        for inputObjshape in inputObjshapes:
                            inputObjshape_parNode = cmds.listConnections(inputObjshape + '.' + inputAttr, scn=True,
                                                                         source=1, p=1)
                            if inputObjshape_parNode != None:
                                if inputObjshape_parNode[0] not in outputAttr:
                                    cmds.connectAttr(outputAttr, inputObjshape + '.' + inputAttr, f=forceCon)

                elif conShape == 0:
                    inputObj_parNode = cmds.listConnections(inputObj + '.' + inputAttr, scn=True, source=1, p=1)
                    if inputObj_parNode != None:
                        if inputObj_parNode[0] not in outputAttr:
                            cmds.connectAttr(outputAttr, inputObj + '.' + inputAttr, f=forceCon)
                elif conShape == 2:
                    pass

        return

    def ctrlDefault(self):
        objAttrs_and_values = ['L_arm_switch_ctrl.ikfk',
                               1,
                               'R_arm_switch_ctrl.ikfk',
                               1,
                               'L_leg_switch_ctrl.ikfk',
                               1,
                               'R_leg_switch_ctrl.ikfk',
                               1,
                               'body_ctrl.fkVis',
                               1,
                               'L_arm_fk_ctrl.follow',
                               1,
                               'R_arm_fk_ctrl.follow',
                               1,
                               'L_leg_fk_ctrl.follow',
                               1,
                               'R_leg_fk_ctrl.follow',
                               1,
                               'neck_1_ctrl.follow',
                               1,
                               'head_ctrl.follow',
                               1,
                               'head_ctrl.aimVis',
                               0,
                               'neck_1_ctrl.stretch',
                               0,
                               'L_arm_ik_pole_ctrl.follow',
                               0,
                               'L_leg_ik_pole_ctrl.follow',
                               0,
                               'R_arm_ik_pole_ctrl.follow',
                               0,
                               'R_leg_ik_pole_ctrl.follow',
                               0,
                               'L_arm_ik_pole_ctrl.lock',
                               0,
                               'L_leg_ik_pole_ctrl.lock',
                               0,
                               'R_arm_ik_pole_ctrl.lock',
                               0,
                               'R_leg_ik_pole_ctrl.lock',
                               0,
                               'L_arm_fk_ctrl.upLength',
                               0,
                               'L_lowarm_fk_ctrl.dnLength',
                               0,
                               'L_leg_fk_ctrl.upLength',
                               0,
                               'L_lowleg_fk_ctrl.dnLength',
                               0,
                               'R_arm_fk_ctrl.upLength',
                               0,
                               'R_lowarm_fk_ctrl.dnLength',
                               0,
                               'R_leg_fk_ctrl.upLength',
                               0,
                               'R_lowleg_fk_ctrl.dnLength',
                               0]
        for i in range(int(len(objAttrs_and_values) / 2)):
            attr = objAttrs_and_values[i * 2]
            attr_value = objAttrs_and_values[i * 2 + 1]
            cmds.setAttr(attr, attr_value)

        ctrlvisAttrs = ['L_arm_fk_ctrl.rootVis',
                        'R_arm_fk_ctrl.rootVis',
                        'L_arm_ik_ctrl.rootVis',
                        'R_arm_ik_ctrl.rootVis',
                        'L_leg_fk_ctrl.rootVis',
                        'R_leg_fk_ctrl.rootVis',
                        'L_leg_ik_ctrl.rootVis',
                        'R_leg_ik_ctrl.rootVis',
                        'L_arm_switch_ctrl.secVis',
                        'L_leg_switch_ctrl.secVis',
                        'R_arm_switch_ctrl.secVis',
                        'R_leg_switch_ctrl.secVis']
        for ctrlvisAttr in ctrlvisAttrs:
            cmds.setAttr(ctrlvisAttr, 0)

        sys.stderr.write(u'------is ok')

    def lockmocapJntAttr(self):
        lowRig = True
        keyString = ['LeftArm_sec1',
                     'RightArm_sec1',
                     'LeftLeg_sec1',
                     'RightLeg_sec1']
        for key in keyString:
            if cmds.objExists(key):
                lowRig = False

        if lowRig:
            joint_a = ['Spine',
                       'Spine1',
                       'Spine2',
                       'Spine3',
                       'Spine4',
                       'Chest',
                       'ChestMid',
                       'Neck1',
                       'Neck2',
                       'Neck3',
                       'Head',
                       'LeftShoulder',
                       'LeftArm',
                       'LeftForeArm',
                       'LeftHand',
                       'LeftHandThumbRoot',
                       'LeftHandThumb1',
                       'LeftHandThumb2',
                       'LeftHandThumb3',
                       'LeftHandThumb4',
                       'LeftHandIndexRoot',
                       'LeftHandIndex1',
                       'LeftHandIndex2',
                       'LeftHandIndex3',
                       'LeftHandIndex4',
                       'LeftHandMiddleRoot',
                       'LeftHandMiddle1',
                       'LeftHandMiddle2',
                       'LeftHandMiddle3',
                       'LeftHandMiddle4',
                       'LeftHandRingRoot',
                       'LeftHandRing1',
                       'LeftHandRing2',
                       'LeftHandRing3',
                       'LeftHandRing4',
                       'LeftHandPinkyRoot',
                       'LeftHandPinky1',
                       'LeftHandPinky2',
                       'LeftHandPinky3',
                       'LeftHandPinky4',
                       'RightShoulder',
                       'RightArm',
                       'RightForeArm',
                       'RightHand',
                       'RightHandThumbRoot',
                       'RightHandThumb1',
                       'RightHandThumb2',
                       'RightHandThumb3',
                       'RightHandThumb4',
                       'RightHandIndexRoot',
                       'RightHandIndex1',
                       'RightHandIndex2',
                       'RightHandIndex3',
                       'RightHandIndex4',
                       'RightHandMiddleRoot',
                       'RightHandMiddle1',
                       'RightHandMiddle2',
                       'RightHandMiddle3',
                       'RightHandMiddle4',
                       'RightHandRingRoot',
                       'RightHandRing1',
                       'RightHandRing2',
                       'RightHandRing3',
                       'RightHandRing4',
                       'RightHandPinkyRoot',
                       'RightHandPinky1',
                       'RightHandPinky2',
                       'RightHandPinky3',
                       'RightHandPinky4',
                       'LeftUpLeg',
                       'LeftLeg',
                       'LeftFoot',
                       'LeftToeBase',
                       'LeftToeBaseEnd',
                       'RightUpLeg',
                       'RightLeg',
                       'RightFoot',
                       'RightToeBase',
                       'RightToeBaseEnd']
            joint_b = ['RightHandPinky4',
                       'RightHandPinky3',
                       'RightHandPinky2',
                       'RightHandRing4',
                       'RightHandRing3',
                       'RightHandRing2',
                       'RightHandMiddle4',
                       'RightHandMiddle3',
                       'RightHandMiddle2',
                       'RightHandIndex4',
                       'RightHandIndex3',
                       'RightHandIndex2',
                       'RightHandThumb4',
                       'RightHandThumb2',
                       'LeftHandPinky4',
                       'LeftHandPinky3',
                       'LeftHandPinky2',
                       'LeftHandRing4',
                       'LeftHandRing3',
                       'LeftHandRing2',
                       'LeftHandMiddle4',
                       'LeftHandMiddle3',
                       'LeftHandMiddle2',
                       'LeftHandIndex4',
                       'LeftHandIndex3',
                       'LeftHandIndex2',
                       'LeftHandThumb4',
                       'LeftHandThumb3',
                       'RightHandThumb3']
            joint_c = ['RightLeg',
                       'LeftLeg',
                       'RightForeArm',
                       'LeftForeArm']
            joint_d = ['ChestMid']
            cmds.setAttr('Hips.sx', lock=1)
            cmds.setAttr('Hips.sy', lock=1)
            cmds.setAttr('Hips.sz', lock=1)
            for i in joint_a:
                cmds.setAttr(i + '.tx', lock=1)
                cmds.setAttr(i + '.ty', lock=1)
                cmds.setAttr(i + '.tz', lock=1)
                cmds.setAttr(i + '.sx', lock=1)
                cmds.setAttr(i + '.sy', lock=1)
                cmds.setAttr(i + '.sz', lock=1)

            for o in joint_b:
                cmds.setAttr(o + '.rx', lock=1)
                cmds.setAttr(o + '.ry', lock=1)

            for k in joint_c:
                cmds.setAttr(k + '.ry', lock=1)
                cmds.setAttr(k + '.rz', lock=1)

        else:
            cmds.warning(u'\u9ad8\u6a21\u7ed1\u5b9a\u4e0d\u9700\u8981\u9501\u5b9a\u9aa8\u9abc\u5c5e\u6027')

    def lockmocapJntAttr_zt(self):
        """
        # only for zhetian project
        # lock chest mid jnt t r s
        # lock rotate range for shoulder jnt
        :return: None
        """
        chestMid = 'ChestMid'
        if cmds.objExists(chestMid):
            cmds.setAttr(chestMid + '.tx', lock=1)
            cmds.setAttr(chestMid + '.ty', lock=1)
            cmds.setAttr(chestMid + '.tz', lock=1)
            cmds.setAttr(chestMid + '.rx', lock=1)
            cmds.setAttr(chestMid + '.ry', lock=1)
            cmds.setAttr(chestMid + '.rz', lock=1)
            cmds.setAttr(chestMid + '.sx', lock=1)
            cmds.setAttr(chestMid + '.sy', lock=1)
            cmds.setAttr(chestMid + '.sz', lock=1)
        shoulderJnt = ['LeftShoulder', 'RightShoulder']
        for shoulder in shoulderJnt:
            if cmds.objExists(shoulder):
                cmds.transformLimits(shoulder, rx=(-5, 3), erx=(1, 1))

    def lockCtrlAttr(self, lockValue, keyable):
        L_fingerctrls = ['L_indexfinger_2_ctrl',
                         'L_indexfinger_3_ctrl',
                         'L_middlefinger_2_ctrl',
                         'L_middlefinger_3_ctrl',
                         'L_ringfinger_2_ctrl',
                         'L_ringfinger_3_ctrlL_pinkyfinger_2_ctrl',
                         'L_pinkyfinger_3_ctrl',
                         'L_thumbfinger_2_ctrl',
                         'L_thumbfinger_3_ctrl']
        L_ctrl1s = ['L_lowarm_fk_ctrl', 'L_lowleg_fk_ctrl']
        attrs = ['rx', 'ry']
        for L_ctrl1 in L_ctrl1s:
            r_ctrl1 = 'R' + L_ctrl1[1:]
            for attr in attrs:
                cmds.setAttr(L_ctrl1 + '.' + attr, lock=lockValue, keyable=keyable)
                cmds.setAttr(r_ctrl1 + '.' + attr, lock=lockValue, keyable=keyable)

        sys.stderr.write(u'------\u63a7\u5236\u5668\u65e0\u7528\u8f74\u5411\u5df2\u7ecf\u9501\u5b9a is ok')

    def editBody_ctrlRotate(self):
        grp = cmds.group(em=True)
        cmds.setAttr(grp + '.r', 180, 0, 90)
        cmds.parent('hip_follow_grp', w=True)
        cmds.delete('Hips_dr_parentConstraint1')
        cmds.delete(cmds.orientConstraint(grp, 'Hips_ctrl_zero', offset=(0, 0, 0), w=1, mo=0))
        cmds.parent('hip_follow_grp', 'Hips_ctrl')
        cmds.parentConstraint('Hips_ctrl', 'Hips_dr', mo=1)
        cmds.parent('spine_rig_grp', 'Hips_ctrl_zero', 'body_follow_grp', w=True)
        cmds.setAttr('body_ctrl_zero.r', 0, 0, 0)
        if cmds.objExists('body02_ctrl') == True:
            cmds.parent('spine_rig_grp', 'Hips_ctrl_zero', 'body_follow_grp', 'body02_ctrl')
        elif cmds.objExists('body_ctrl') == True:
            cmds.parent('spine_rig_grp', 'Hips_ctrl_zero', 'body_follow_grp', 'body_ctrl')
        cmds.delete(grp)
        cmds.select(cl=True)

    def curveScaleRun(self, sels, scaleValue, ScaleAxis):
        for sel in sels:
            crv = sel
            if cmds.objectType(crv) == 'nurbsCurve':
                curveshape = crv
                cvTxs = []
                cvTys = []
                cvTzs = []
                cvs = cmds.ls(curveshape + '.cv[*]', fl=True)
                for cv in cvs:
                    cvTs = cmds.xform(cv, q=True, t=True, ws=True)
                    cvTxs.append(cvTs[0])
                    cvTys.append(cvTs[1])
                    cvTzs.append(cvTs[2])

                centerPivet = (
                    (min(cvTxs) + max(cvTxs)) / 2, (min(cvTys) + max(cvTys)) / 2, (min(cvTzs) + max(cvTzs)) / 2)
                cmds.select(curveshape + '.cv[*]')
                cmds.scale(scaleValue, scaleValue, scaleValue, r=True, p=centerPivet)
            else:
                curveshapes = cmds.listRelatives(crv, s=True, type='nurbsCurve')
                if ScaleAxis == 'curveShapeAxis':
                    cvTxs = []
                    cvTys = []
                    cvTzs = []
                    for curveshape in curveshapes:
                        cvs = cmds.ls(curveshape + '.cv[*]', fl=True)
                        for cv in cvs:
                            cvTs = cmds.xform(cv, q=True, t=True, ws=True)
                            cvTxs.append(cvTs[0])
                            cvTys.append(cvTs[1])
                            cvTzs.append(cvTs[2])

                    centerPivet = (
                        (min(cvTxs) + max(cvTxs)) / 2, (min(cvTys) + max(cvTys)) / 2, (min(cvTzs) + max(cvTzs)) / 2)
                elif ScaleAxis == 'objAxis':
                    centerPivet = cmds.xform(crv, q=True, ws=True, t=True)
                if curveshapes != None:
                    for curveshape in curveshapes:
                        cmds.select(curveshape + '.cv[*]')
                        cmds.scale(scaleValue, scaleValue, scaleValue, r=True, p=centerPivet)

        cmds.select(sels)
        return

    def add_body02_ctrl(self):
        if cmds.objExists('body02_ctrl') == True:
            cmds.error(u'body02_ctrl---\u5df2\u7ecf\u5b58\u5728')
        body_ctrl_cs = cmds.listRelatives('body_ctrl', c=True)
        body_ctrl_shapes = cmds.listRelatives('body_ctrl', s=True)
        for body_ctrl_shape in body_ctrl_shapes:
            body_ctrl_cs.remove(body_ctrl_shape)

        cmds.parent(body_ctrl_cs, w=True)
        body02_ctrl_zero = cmds.duplicate('body_ctrl_zero')[0]
        body02_ctrl = cmds.rename(cmds.listRelatives(body02_ctrl_zero, c=True, f=True)[0], 'body02_ctrl')
        body02_ctrl_zero = cmds.rename(body02_ctrl_zero, 'body02_ctrl_zero')
        self.curveScaleRun(['body02_ctrl'], 0.95, 'curveShapeAxis')
        self.curveScaleRun(['body_ctrl'], 1.05, 'curveShapeAxis')
        cmds.parent('body02_ctrl_zero', 'body_ctrl')
        cmds.parent(body_ctrl_cs, 'body02_ctrl')
        cmds.select('body02_ctrl')
        cmds.deleteAttr('body02_ctrl', attribute='ikVis')
        cmds.deleteAttr('body02_ctrl', attribute='fkVis')
        cmds.deleteAttr('body02_ctrl', attribute='TCHour')
        cmds.deleteAttr('body02_ctrl', attribute='TCMinute')
        cmds.deleteAttr('body02_ctrl', attribute='TCSecond')
        cmds.deleteAttr('body02_ctrl', attribute='TCFrame')

    def showAllCtrl(self):
        ctrlvisAttrs = ['L_arm_fk_ctrl.rootVis',
                        'R_arm_fk_ctrl.rootVis',
                        'L_arm_ik_ctrl.rootVis',
                        'R_arm_ik_ctrl.rootVis',
                        'L_leg_fk_ctrl.rootVis',
                        'R_leg_fk_ctrl.rootVis',
                        'L_leg_ik_ctrl.rootVis',
                        'R_leg_ik_ctrl.rootVis',
                        'L_arm_switch_ctrl.secVis',
                        'L_leg_switch_ctrl.secVis',
                        'R_arm_switch_ctrl.secVis',
                        'R_leg_switch_ctrl.secVis']
        for ctrlvisAttr in ctrlvisAttrs:
            cmds.setAttr(ctrlvisAttr, 1)

        ctrls = [u'L_thumbfinger_ctrl',
                 u'L_middlefinger_ctrl',
                 u'L_indexfinger_ctrl',
                 u'L_ringfinger_ctrl',
                 u'L_pinkyfinger_ctrl',
                 u'R_thumbfinger_ctrl',
                 u'R_middlefinger_ctrl',
                 u'R_indexfinger_ctrl',
                 u'R_ringfinger_ctrl',
                 u'R_pinkyfinger_ctrl',
                 'L_arm_fk_root_ctrl',
                 'R_arm_fk_root_ctrl',
                 'L_arm_ik_root_ctrl',
                 'R_arm_ik_root_ctrl',
                 'L_leg_fk_root_ctrl',
                 'R_leg_fk_root_ctrl',
                 'L_leg_ik_root_ctrl',
                 'R_leg_ik_root_ctrl']
        cmds.select(ctrls + cmds.ls('*_*_second_*_ctrl'))

    def selectModelhi(self):
        hiList = cmds.ls('*hi')
        modelhis = []
        for modelhi in hiList:
            modelhiShape = cmds.listRelatives(modelhi, s=True)[0]
            if cmds.objectType(modelhiShape) == 'mesh':
                modelhis.append(modelhi)

        cmds.select(modelhis)

    def addLightJnt(self):
        geoName = cmds.ls(sl=True)[0]
        hipsjnts = cmds.ls(geoName + '_Hips', 'Hips', type='joint')
        if len(hipsjnts) == 1:
            hipsjnt = hipsjnts[0]
            if cmds.objExists('Wlight_hip') != True:
                light_hip_jnt = cmds.joint(n='Wlight_hip')
                cmds.parent(light_hip_jnt, hipsjnt)
                cmds.orientConstraint(geoName, light_hip_jnt)
                cmds.setAttr(light_hip_jnt + '.t', 0, 0, 0)
            else:
                cmds.warning(
                    u'\u706f\u5149\u9aa8\u9abc\u5df2\u7ecf\u5b58\u5728,\u8bf7\u68c0\u67e5\u706f\u5149\u9aa8\u9abc\u662f\u5426\u6b63\u786e,Wlight_hip,Wlight_head')
            if cmds.objExists('Wlight_head') != True:
                light_head_jnt = cmds.joint(n='Wlight_head')
                cmds.parent(light_head_jnt, hipsjnt)
                cmds.orientConstraint(geoName, light_head_jnt)
                cmds.setAttr(light_head_jnt + '.t', 0, 80, 0)
            else:
                cmds.warning(
                    u'\u706f\u5149\u9aa8\u9abc\u5df2\u7ecf\u5b58\u5728,\u8bf7\u68c0\u67e5\u706f\u5149\u9aa8\u9abc\u662f\u5426\u6b63\u786e,Wlight_hip,Wlight_head')
            cmds.select('Wlight_hip', 'Wlight_head')
        elif len(hipsjnts) == 0:
            cmds.warning(
                u'\u8fd0\u884c\u5931\u8d25\uff0c\u6ca1\u6709\u6b63\u786e\u7684Hipse\u9aa8\u9abc\uff0c\u9053\u5177:\u5927\u7ec4\u540d+Hips\uff0c\u89d2\u8272:Hips')
        else:
            cmds.select(hipsjnts)
            cmds.warning(u'\u8fd0\u884c\u5931\u8d25\uff0c\u5e26\u6709Hips\u5b57\u7b26\u7684\u9aa8\u9abc\u6709' + str(
                len(hipsjnts)) + u'\u4e2a------', str(hipsjnts))

    def lizhi_create_driver(self):
        import maya.cmds as mc
        import driver_win as lizhi_driver_win
        reload(lizhi_driver_win)
        lizhi_driver_win = lizhi_driver_win.driver_win()
        lizhi_driver_win.driver_win()

    def createVisibility(self):
        """\xe5\x88\x9b\xe5\xbb\xbaVisibility"""
        import createVisibility
        reload(createVisibility)
        CreateVis = createVisibility.CreateVis()
        CreateVis.Create_vis_UI()

    def sdktool(self):
        import maya.cmds as mc
        import sys
        sys.path.append(self.whereAmI() + '\\RoseSdkTool')
        print(self.whereAmI() + '\\RoseSdkTool')
        import Tools.rosa_SdkManager as sdk
        reload(sdk)
        SDK = sdk.sdkManager()
        SDK.MainUI()

    def limitSkinWeight(self):
        import limitSkinWeight
        reload(limitSkinWeight)
        melCallClsLimitSkinWeightClssAs = limitSkinWeight.LimitSkinWeightClss()
        melCallClsLimitSkinWeightClssAs.ui()

    def ImportExport_ctrlShape(self):
        import ImportExport_ctrlShape
        reload(ImportExport_ctrlShape)
        aa = ImportExport_ctrlShape.SK_ImportExportUI(setName='ctrl_set')
        aa.displayUI()

    def heightScaling(self):
        winName = 'heightScalingWin'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t=u'\u51e1\u4eba1\u89d2\u8272\u8eab\u9ad8\u7f29\u653e\u503c')
        columnLayout1 = cmds.columnLayout(adjustableColumn=True)
        cmds.scrollField(editable=True, wordWrap=True,
                         text=u'\u7537\u6027\u4ee5178\u4e3a1\u7684\u7f29\u653e\u503c\n178 \u7f29\u653e 1.000000000000\n172 \u7f29\u653e 0.965345671939\n176 \u7f29\u653e 0.98\n183 \u7f29\u653e 1.02228144224\n186 \u7f29\u653e 1.04269915857\n188 \u7f29\u653e 1.05353483939\n197 \u7f29\u653e 1.10257388453\n\n\u5973\u6027\u4ee5170\u4e3a1\u7684\u7f29\u653e\u503c\n170 \u7f29\u653e 1.00000000000\n145 \u7f29\u653e 0.870413575344\n165 \u7f29\u653e 0.972693395092\n180 \u7f29\u653e 1.05516866767\n\u51e1\u4eba1\u901a\u7528\u8eab\u4f53\u6587\u4ef6:I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\u6807\u51c6\u4eba\u4f53\\\u6807\u51c6rig',
                         h=300)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=4)
        start_directory = 'I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe6\xa0\x87\xe5\x87\x86\xe4\xba\xba\xe4\xbd\x93\\tem'.decode(
            'utf8').encode('cp936')
        cmds.button(l=u'\u6a21\u677f\u8def\u5f84', h=40, w=65, c=lambda *args: self.Open_the_file_path(start_directory))
        cmds.button(l=u'\u4eba\u4f53\u6a21\u578b', h=40, w=65, c=lambda *args: self.Open_the_file_path(
            'I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe6\xa0\x87\xe5\x87\x86\xe4\xba\xba\xe4\xbd\x93\\Tpose'.decode(
                'utf8').encode('cp936')))
        cmds.button(l=u'\u7ed1\u5b9a\u6559\u7a0b', h=40, w=65, c=lambda *args: self.Open_the_file_path(
            'I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe7\xbb\x91\xe5\xae\x9a\xef\xbc\x8c\xe8\xa7\x84\xe8\x8c\x83\xef\xbc\x8c\xe5\xb7\xa5\xe5\x85\xb7\xef\xbc\x8c\xe4\xbd\xbf\xe7\x94\xa8\xe8\xaf\xb4\xe6\x98\x8e\\\xe5\x87\xa1\xe4\xba\xba\xe4\xbf\xae\xe4\xbb\x99\xe4\xbc\xa0'.decode(
                'utf8').encode('cp936')))
        cmds.button(l=u'nan178', h=40, w=65,
                    c="cmds.file('I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe6\xa0\x87\xe5\x87\x86\xe4\xba\xba\xe4\xbd\x93\\\xe4\xb8\x8d\xe5\x90\x8c\xe4\xbd\x93\xe5\x9e\x8b\xe6\xa8\xa1\xe5\x9e\x8b\\\xe6\xa0\x87\xe5\x87\x86\xe8\xba\xab\xe6\x9d\x90\xe7\x94\xb7\xe5\xa5\xb3\xe6\xa8\xa1\xe5\x9e\x8b_A_T_pose\\Nan_178_Biao_Tpose.ma',i = True)")
        cmds.button(l=u'\u5973145', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.870413575344,0.870413575344,0.870413575344)")
        cmds.button(l=u'\u5973165', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.972693395092,0.972693395092,0.972693395092)")
        cmds.button(l=u'\u5973170', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1,1,1)")
        cmds.button(l=u'\u5973180', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.05516866767,1.05516866767,1.05516866767)")
        cmds.button(l=u'\u7537178', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1,1,1)")
        cmds.button(l=u'\u7537172', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.965345671939,0.965345671939,0.965345671939)")
        cmds.button(l=u'\u7537176', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.98,0.98,0.98)")
        cmds.button(l=u'\u7537183', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.02228144224,1.02228144224,1.02228144224)")
        cmds.button(l=u'\u7537186', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.04269915857,1.04269915857,1.04269915857)")
        cmds.button(l=u'\u7537188', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.05353483939,1.05353483939,1.05353483939)")
        cmds.button(l=u'\u7537197', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.10257388453,1.10257388453,1.10257388453)")
        cmds.showWindow()

    def heightScaling2(self):
        winName = 'heightScalingWin'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t=u'\u51e1\u4eba\u5e74\u756a\u89d2\u8272\u8eab\u9ad8\u7f29\u653e\u503c')
        columnLayout1 = cmds.columnLayout(adjustableColumn=True)
        cmds.scrollField(editable=True, wordWrap=True,
                         text=u'\u7537\u6027\u4ee5178\u4e3a1\u7684\u7f29\u653e\u503c\n165 \u7f29\u653e 0.9229\n170 \u7f29\u653e 0.9509\n175 \u7f29\u653e 0.9788\n178 \u7f29\u653e 1.000000000000\n180 \u7f29\u653e 1.0068\n183 \u7f29\u653e 1.02228144224\n188 \u7f29\u653e 1.05353483939\n\n\u5973\u6027\u4ee5165\u4e3a1\u7684\u7f29\u653e\u503c\n160 \u7f29\u653e 0.969697\n165 \u7f29\u653e 1.0\n168 \u7f29\u653e 1.01818\n170 \u7f29\u653e 1.0303\n\u51e1\u4eba\u5e74\u756a\u901a\u7528\u6587\u4ef6\u8def\u5f84:I:\\proj\\pj2020wj006\\syncData\\workgroup\\RIG_WorkGrp\\\u6807\u51c6\u4eba\u4f53\\\u6807\u51c6\u8eab\u4f53rig',
                         h=300)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=4)
        start_directory = 'I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe6\xa0\x87\xe5\x87\x86\xe4\xba\xba\xe4\xbd\x93\\tem'.decode(
            'utf8').encode('cp936')
        cmds.button(l=u'\u6a21\u677f\u8def\u5f84', h=40, w=65, c=lambda *args: self.Open_the_file_path(start_directory))
        cmds.button(l=u'\u4eba\u4f53\u6a21\u578b', h=40, w=65, c=lambda *args: self.Open_the_file_path(
            'I:\\proj\\mopian_immortal_epi\\syncData\\workgroup\\RIG_WorkGrp\\\xe6\xa0\x87\xe5\x87\x86\xe4\xba\xba\xe4\xbd\x93\\Tpose'.decode(
                'utf8').encode('cp936')))
        cmds.button(l=u'\u7537165', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.9229,0.9229,0.9229)")
        cmds.button(l=u'\u7537170', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.9509,0.9509,0.9509)")
        cmds.button(l=u'\u7537175', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.9788,0.9788,0.9788)")
        cmds.button(l=u'\u7537180', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.0068,1.0068,1.0068)")
        cmds.button(l=u'\u7537183', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.02228144224,1.02228144224,1.02228144224)")
        cmds.button(l=u'\u7537188', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.05353483939,1.05353483939,1.05353483939)")
        cmds.button(l=u'\u5973160', h=40, w=65,
                    c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',0.969697,0.969697,0.969697)")
        cmds.button(l=u'\u5973168', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.01818,1.01818,1.01818)")
        cmds.button(l=u'\u5973170', h=40, w=65, c="cmds.setAttr(cmds.ls(sl = True)[0] + '.s',1.0303,1.0303,1.0303)")
        cmds.showWindow()

    def Open_the_file_path(self, path1):
        os.system('explorer.exe %s' % path1)

    def createHandScale(self):
        for side in ["L_", "R_"]:
            if cmds.objExists(side + "arm_switch_ctrl"):
                if not cmds.objExists(side + "arm_switch_ctrl.hand_scale"):
                    cmds.addAttr(side + "arm_switch_ctrl", ln="hand_scale", at="double", min=0, dv=1)
                    cmds.setAttr(side + "arm_switch_ctrl.hand_scale", e=1, k=1)

                if cmds.objExists(side + "hand_finger_rig_grp") and cmds.objExists(side + "hand_dr"):
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_finger_rig_grp.sx")
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_finger_rig_grp.sy")
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_finger_rig_grp.sz")
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_dr.sx")
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_dr.sy")
                    cmds.connectAttr(side + "arm_switch_ctrl.hand_scale", side + "hand_dr.sz")

    def fixArmTwist(self):
        for i in ["L", "R"]:
            oldp = "%s_arm_nonroll_ikHandle_zero" % i
            old = "%s_arm_nonroll_ikHandle" % i
            oldLoc = "%s_arm_nonroll_follow_jnt_loc" % i
            oldS = "%s_arm_nonroll" % i
            oldE = "%s_arm_nonroll_end" % i

            cmds.delete(old)
            ikh = cmds.ikHandle(sj=oldS, ee=oldE, sol='ikSCsolver', name="%s" % old)[0]
            cmds.parent(ikh, oldp)
            cmds.pointConstraint(oldLoc, ikh, mo=True)
            cmds.setAttr(old + '.poleVectorX', 0)
            cmds.setAttr(old + '.poleVectorY', 0)
            cmds.setAttr(old + '.poleVectorZ', 0)

    @decorator_utils.one_undo
    def createBreathe(self):
        """

        :return:
        """
        selection = cmds.ls(sl=1)
        if not selection:
            cmds.warning("Please select at least one mesh!")
            return
        scriptPath = os.path.dirname(__file__).replace('/', '\\')
        ctrlPath = scriptPath + "\\breathe_ctrl.ma"
        if not cmds.objExists("breathe_ctrl"):
            cmds.file(ctrlPath, i=1)
            cmds.parent("breathe_ctrl_zero", "chest_ctrl")

        breathe_up = cmds.duplicate(selection[0], name="breathe_up")[0]
        breathe_dn = cmds.duplicate(selection[0], name="breathe_dn")[0]

        historyList = cmds.listHistory(selection[0])
        bs = [h for h in historyList if cmds.objectType(h) == "blendShape"]
        if bs:
            cmds.blendShape(bs[0], edit=True, tc=False, target=(
                selection[0], len(cmds.aliasAttr(bs[0], q=1)) + 1, breathe_up,
                1.0))
            cmds.blendShape(bs[0], edit=True, tc=False, target=(
                selection[0], len(cmds.aliasAttr(bs[0], q=1)) + 1, breathe_dn,
                1.0))

        cmds.delete([breathe_up, breathe_dn])

    def con_bridge_new(self):

        con_dict = {
            "L_Shoulder": ["L_shoulder_dr", "chect_mid_dr", "+x"],
            "L_Arm": ["L_arm_sec1_dr", "L_shoulder_dr", "+x"],
            "L_ForeArm": ["L_lowarm_sec1_dr", "L_arm_sec4_dr", "+x"],
            "L_Hand": ["L_hand_dr", "L_lowarm_sec4_dr", "+x"],
            "M_Neck1": ["neck_1_dr", "chect_mid_dr", "+y"],
            "M_Neck2": ["neck_2_dr", "neck_1_dr", "+y"],
            "M_Neck3": ["neck_3_dr", "neck_2_dr", "+y"],
            "M_Head": ["head_dr", "neck_3_dr", "+y"],
            "L_UpLeg": ["L_leg_sec1_dr", "Hips_dr", "-y"],
            "L_Leg": ["L_lowleg_sec1_dr", "L_leg_sec4_dr", "-y"],
            "L_Foot": ["L_foot_dr", "L_lowleg_sec4_dr", "-y"],
            "L_ToeBase": ["L_toebase_dr", "L_foot_dr", "+z"],
            "R_Shoulder": ["R_shoulder_dr", "chect_mid_dr", "+x"],
            "R_Arm": ["R_arm_sec1_dr", "R_shoulder_dr", "+x"],
            "R_ForeArm": ["R_lowarm_sec1_dr", "R_arm_sec4_dr", "+x"],
            "R_Hand": ["R_hand_dr", "R_lowarm_sec4_dr", "+x"],
            "R_UpLeg": ["R_leg_sec1_dr", "Hips_dr", "-y"],
            "R_Leg": ["R_lowleg_sec1_dr", "R_leg_sec4_dr", "-y"],
            "R_Foot": ["R_foot_dr", "R_lowleg_sec4_dr", "-y"],
            "R_ToeBase": ["R_toebase_dr", "R_foot_dr", "+z"]
        }

        topNode = 'Psd_System'
        if not cmds.objExists(topNode):
            cmds.createNode('transform', n=topNode)
            if cmds.objExists('all_ctrl'):
                cmds.parent(topNode, 'all_ctrl')

        for prefix, jntList in con_dict.items():
            mirror = False
            if "L_" in prefix:
                mirror = False
            if "R_" in prefix:
                mirror = True
            self.createNewPoseDriver(prefix, jntList[1], jntList[0], jntList[-1], mirror)

        if cmds.objExists("body_sdk_handle") and not cmds.objExists('body_sdk_handle_org'):
            org_handle = cmds.duplicate("body_sdk_handle", name="body_sdk_handle_org")[0]
            cmds.parent(org_handle, topNode)
            driverAttrs = [u'chest_dr_',
                           u'chest_dr_D',
                           u'chest_dr_F',
                           u'chest_dr_B',
                           u'chect_mid_dr_',
                           u'chect_mid_dr_D',
                           u'chect_mid_dr_F',
                           u'chect_mid_dr_B',
                           u'neck_1_dr_',
                           u'neck_1_dr_D',
                           u'neck_1_dr_F',
                           u'neck_1_dr_B',
                           u'head_dr_',
                           u'head_dr_D',
                           u'head_dr_F',
                           u'head_dr_B',
                           u'L_shoulder_dr_U',
                           u'L_shoulder_dr_D',
                           u'L_shoulder_dr_F',
                           u'L_shoulder_dr_B',
                           u'L_shoulder_dr_UF',
                           u'L_shoulder_dr_UB',
                           u'L_shoulder_dr_DF',
                           u'L_shoulder_dr_DB',
                           u'L_arm_dr_U',
                           u'L_arm_dr_D',
                           u'L_arm_dr_F',
                           u'L_arm_dr_B',
                           u'L_arm_dr_UF',
                           u'L_arm_dr_UB',
                           u'L_arm_dr_DF',
                           u'L_arm_dr_DB',
                           u'L_lowarm_dr_U',
                           u'L_lowarm_dr_D',
                           u'L_lowarm_dr_F',
                           u'L_lowarm_dr_B',
                           u'L_lowarm_dr_UF',
                           u'L_lowarm_dr_UB',
                           u'L_lowarm_dr_DF',
                           u'L_lowarm_dr_DB',
                           u'L_hand_dr_U',
                           u'L_hand_dr_D',
                           u'L_hand_dr_F',
                           u'L_hand_dr_B',
                           u'L_hand_dr_UF',
                           u'L_hand_dr_UB',
                           u'L_hand_dr_DF',
                           u'L_hand_dr_DB',
                           u'L_thumbfinger_1_dr_',
                           u'L_thumbfinger_1_dr_D',
                           u'L_thumbfinger_1_dr_F',
                           u'L_thumbfinger_1_dr_B',
                           u'L_thumbfinger_2_dr_',
                           u'L_thumbfinger_2_dr_D',
                           u'L_thumbfinger_2_dr_F',
                           u'L_thumbfinger_2_dr_B',
                           u'L_thumbfinger_3_dr_',
                           u'L_thumbfinger_3_dr_D',
                           u'L_thumbfinger_3_dr_F',
                           u'L_thumbfinger_3_dr_B',
                           u'L_thumbfinger_4_dr_',
                           u'L_thumbfinger_4_dr_D',
                           u'L_thumbfinger_4_dr_F',
                           u'L_thumbfinger_4_dr_B',
                           u'L_indexfinger_1_dr_',
                           u'L_indexfinger_1_dr_D',
                           u'L_indexfinger_1_dr_F',
                           u'L_indexfinger_1_dr_B',
                           u'L_indexfinger_2_dr_',
                           u'L_indexfinger_2_dr_D',
                           u'L_indexfinger_2_dr_F',
                           u'L_indexfinger_2_dr_B',
                           u'L_indexfinger_3_dr_',
                           u'L_indexfinger_3_dr_D',
                           u'L_indexfinger_3_dr_F',
                           u'L_indexfinger_3_dr_B',
                           u'L_indexfinger_4_dr_',
                           u'L_indexfinger_4_dr_D',
                           u'L_indexfinger_4_dr_F',
                           u'L_indexfinger_4_dr_B',
                           u'L_middlefinger_1_dr_',
                           u'L_middlefinger_1_dr_D',
                           u'L_middlefinger_1_dr_F',
                           u'L_middlefinger_1_dr_B',
                           u'L_middlefinger_2_dr_',
                           u'L_middlefinger_2_dr_D',
                           u'L_middlefinger_2_dr_F',
                           u'L_middlefinger_2_dr_B',
                           u'L_middlefinger_3_dr_',
                           u'L_middlefinger_3_dr_D',
                           u'L_middlefinger_3_dr_F',
                           u'L_middlefinger_3_dr_B',
                           u'L_middlefinger_4_dr_',
                           u'L_middlefinger_4_dr_D',
                           u'L_middlefinger_4_dr_F',
                           u'L_middlefinger_4_dr_B',
                           u'L_ringfinger_1_dr_',
                           u'L_ringfinger_1_dr_D',
                           u'L_ringfinger_1_dr_F',
                           u'L_ringfinger_1_dr_B',
                           u'L_ringfinger_2_dr_',
                           u'L_ringfinger_2_dr_D',
                           u'L_ringfinger_2_dr_F',
                           u'L_ringfinger_2_dr_B',
                           u'L_ringfinger_3_dr_',
                           u'L_ringfinger_3_dr_D',
                           u'L_ringfinger_3_dr_F',
                           u'L_ringfinger_3_dr_B',
                           u'L_ringfinger_4_dr_',
                           u'L_ringfinger_4_dr_D',
                           u'L_ringfinger_4_dr_F',
                           u'L_ringfinger_4_dr_B',
                           u'L_pinkyfinger_1_dr_',
                           u'L_pinkyfinger_1_dr_D',
                           u'L_pinkyfinger_1_dr_F',
                           u'L_pinkyfinger_1_dr_B',
                           u'L_pinkyfinger_2_dr_',
                           u'L_pinkyfinger_2_dr_D',
                           u'L_pinkyfinger_2_dr_F',
                           u'L_pinkyfinger_2_dr_B',
                           u'L_pinkyfinger_3_dr_',
                           u'L_pinkyfinger_3_dr_D',
                           u'L_pinkyfinger_3_dr_F',
                           u'L_pinkyfinger_3_dr_B',
                           u'L_pinkyfinger_4_dr_',
                           u'L_pinkyfinger_4_dr_D',
                           u'L_pinkyfinger_4_dr_F',
                           u'L_pinkyfinger_4_dr_B',
                           u'R_shoulder_dr_U',
                           u'R_shoulder_dr_D',
                           u'R_shoulder_dr_F',
                           u'R_shoulder_dr_B',
                           u'R_shoulder_dr_UF',
                           u'R_shoulder_dr_UB',
                           u'R_shoulder_dr_DF',
                           u'R_shoulder_dr_DB',
                           u'R_arm_dr_U',
                           u'R_arm_dr_D',
                           u'R_arm_dr_F',
                           u'R_arm_dr_B',
                           u'R_arm_dr_UF',
                           u'R_arm_dr_UB',
                           u'R_arm_dr_DF',
                           u'R_arm_dr_DB',
                           u'R_lowarm_dr_U',
                           u'R_lowarm_dr_D',
                           u'R_lowarm_dr_F',
                           u'R_lowarm_dr_B',
                           u'R_lowarm_dr_UF',
                           u'R_lowarm_dr_UB',
                           u'R_lowarm_dr_DF',
                           u'R_lowarm_dr_DB',
                           u'R_hand_dr_U',
                           u'R_hand_dr_D',
                           u'R_hand_dr_F',
                           u'R_hand_dr_B',
                           u'R_hand_dr_UF',
                           u'R_hand_dr_UB',
                           u'R_hand_dr_DF',
                           u'R_hand_dr_DB',
                           u'R_thumbfinger_1_dr_',
                           u'R_thumbfinger_1_dr_D',
                           u'R_thumbfinger_1_dr_F',
                           u'R_thumbfinger_1_dr_B',
                           u'R_thumbfinger_2_dr_',
                           u'R_thumbfinger_2_dr_D',
                           u'R_thumbfinger_2_dr_F',
                           u'R_thumbfinger_2_dr_B',
                           u'R_thumbfinger_3_dr_',
                           u'R_thumbfinger_3_dr_D',
                           u'R_thumbfinger_3_dr_F',
                           u'R_thumbfinger_3_dr_B',
                           u'R_thumbfinger_4_dr_',
                           u'R_thumbfinger_4_dr_D',
                           u'R_thumbfinger_4_dr_F',
                           u'R_thumbfinger_4_dr_B',
                           u'R_indexfinger_1_dr_',
                           u'R_indexfinger_1_dr_D',
                           u'R_indexfinger_1_dr_F',
                           u'R_indexfinger_1_dr_B',
                           u'R_indexfinger_2_dr_',
                           u'R_indexfinger_2_dr_D',
                           u'R_indexfinger_2_dr_F',
                           u'R_indexfinger_2_dr_B',
                           u'R_indexfinger_3_dr_',
                           u'R_indexfinger_3_dr_D',
                           u'R_indexfinger_3_dr_F',
                           u'R_indexfinger_3_dr_B',
                           u'R_indexfinger_4_dr_',
                           u'R_indexfinger_4_dr_D',
                           u'R_indexfinger_4_dr_F',
                           u'R_indexfinger_4_dr_B',
                           u'R_middlefinger_1_dr_',
                           u'R_middlefinger_1_dr_D',
                           u'R_middlefinger_1_dr_F',
                           u'R_middlefinger_1_dr_B',
                           u'R_middlefinger_2_dr_',
                           u'R_middlefinger_2_dr_D',
                           u'R_middlefinger_2_dr_F',
                           u'R_middlefinger_2_dr_B',
                           u'R_middlefinger_3_dr_',
                           u'R_middlefinger_3_dr_D',
                           u'R_middlefinger_3_dr_F',
                           u'R_middlefinger_3_dr_B',
                           u'R_middlefinger_4_dr_',
                           u'R_middlefinger_4_dr_D',
                           u'R_middlefinger_4_dr_F',
                           u'R_middlefinger_4_dr_B',
                           u'R_ringfinger_1_dr_',
                           u'R_ringfinger_1_dr_D',
                           u'R_ringfinger_1_dr_F',
                           u'R_ringfinger_1_dr_B',
                           u'R_ringfinger_2_dr_',
                           u'R_ringfinger_2_dr_D',
                           u'R_ringfinger_2_dr_F',
                           u'R_ringfinger_2_dr_B',
                           u'R_ringfinger_3_dr_',
                           u'R_ringfinger_3_dr_D',
                           u'R_ringfinger_3_dr_F',
                           u'R_ringfinger_3_dr_B',
                           u'R_ringfinger_4_dr_',
                           u'R_ringfinger_4_dr_D',
                           u'R_ringfinger_4_dr_F',
                           u'R_ringfinger_4_dr_B',
                           u'R_pinkyfinger_1_dr_',
                           u'R_pinkyfinger_1_dr_D',
                           u'R_pinkyfinger_1_dr_F',
                           u'R_pinkyfinger_1_dr_B',
                           u'R_pinkyfinger_2_dr_',
                           u'R_pinkyfinger_2_dr_D',
                           u'R_pinkyfinger_2_dr_F',
                           u'R_pinkyfinger_2_dr_B',
                           u'R_pinkyfinger_3_dr_',
                           u'R_pinkyfinger_3_dr_D',
                           u'R_pinkyfinger_3_dr_F',
                           u'R_pinkyfinger_3_dr_B',
                           u'R_pinkyfinger_4_dr_',
                           u'R_pinkyfinger_4_dr_D',
                           u'R_pinkyfinger_4_dr_F',
                           u'R_pinkyfinger_4_dr_B',
                           u'L_leg_dr_U',
                           u'L_leg_dr_D',
                           u'L_leg_dr_F',
                           u'L_leg_dr_B',
                           u'L_leg_dr_UF',
                           u'L_leg_dr_UB',
                           u'L_leg_dr_DF',
                           u'L_leg_dr_DB',
                           u'L_lowleg_dr_U',
                           u'L_lowleg_dr_D',
                           u'L_lowleg_dr_F',
                           u'L_lowleg_dr_B',
                           u'L_lowleg_dr_UF',
                           u'L_lowleg_dr_UB',
                           u'L_lowleg_dr_DF',
                           u'L_lowleg_dr_DB',
                           u'L_foot_dr_U',
                           u'L_foot_dr_D',
                           u'L_foot_dr_F',
                           u'L_foot_dr_B',
                           u'L_foot_dr_UF',
                           u'L_foot_dr_UB',
                           u'L_foot_dr_DF',
                           u'L_foot_dr_DB',
                           u'L_toebase_dr_U',
                           u'L_toebase_dr_D',
                           u'L_toebase_dr_F',
                           u'L_toebase_dr_B',
                           u'L_toebase_dr_UF',
                           u'L_toebase_dr_UB',
                           u'L_toebase_dr_DF',
                           u'L_toebase_dr_DB',
                           u'R_leg_dr_U',
                           u'R_leg_dr_D',
                           u'R_leg_dr_F',
                           u'R_leg_dr_B',
                           u'R_leg_dr_UF',
                           u'R_leg_dr_UB',
                           u'R_leg_dr_DF',
                           u'R_leg_dr_DB',
                           u'R_lowleg_dr_U',
                           u'R_lowleg_dr_D',
                           u'R_lowleg_dr_F',
                           u'R_lowleg_dr_B',
                           u'R_lowleg_dr_UF',
                           u'R_lowleg_dr_UB',
                           u'R_lowleg_dr_DF',
                           u'R_lowleg_dr_DB',
                           u'R_foot_dr_U',
                           u'R_foot_dr_D',
                           u'R_foot_dr_F',
                           u'R_foot_dr_B',
                           u'R_foot_dr_UF',
                           u'R_foot_dr_UB',
                           u'R_foot_dr_DF',
                           u'R_foot_dr_DB',
                           u'R_toebase_dr_U',
                           u'R_toebase_dr_D',
                           u'R_toebase_dr_F',
                           u'R_toebase_dr_B',
                           u'R_toebase_dr_UF',
                           u'R_toebase_dr_UB',
                           u'R_toebase_dr_DF',
                           u'R_toebase_dr_DB']
            for driverAttr in driverAttrs:
                cmds.connectAttr('body_sdk_handle.' + driverAttr, org_handle + '.' + driverAttr)

    def createNewPoseDriver(self, name, parentObj, followObj, axis, mirror):

        posePsd = poseDriverTool.createBridge(name, axis=axis, mirror=mirror)
        poseDriverTool.scaleBridge(name, 0.1)
        poseDriverTool.constraintBridge(parentObj=parentObj, followObj=followObj,
                                        parentHandle=posePsd['parent'], followHandle=posePsd['follow'])
        cmds.parent(posePsd['parent'], 'Psd_System')

    def con_bridge(self):
        self.ctrlDefault()
        self.con_bridge1('chect_mid_dr', 'L_shoulder_dr', 'L_shoulder')
        self.con_bridge1('L_shoulder_dr', 'L_arm_sec1_dr', 'L_arm')
        self.con_bridge1('L_arm_sec5_dr', 'L_lowarm_sec1_dr', 'L_lowarm')
        self.con_bridge1('L_lowarm_sec5_dr', 'L_hand_dr', 'L_hand')
        self.con_bridge1('Hips_dr', 'L_leg_sec1_dr', 'L_leg')
        self.con_bridge1('L_leg_sec5_dr', 'L_lowleg_sec1_dr', 'L_lowleg')
        self.con_bridge1('L_lowleg_sec5_dr', 'L_foot_dr', 'L_foot')
        self.con_bridge1('L_foot_dr', 'L_toebase_dr', 'L_toebase')
        if cmds.objExists('neck_1_driver_grp'):
            self.con_bridge1('chect_mid_dr', 'neck_2_dr', 'neck_1')
        if cmds.objExists('neck_2_driver_grp'):
            self.con_bridge1('neck_1_dr', 'neck_2_dr', 'neck_2')
        if cmds.objExists('neck_3_driver_grp'):
            self.con_bridge1('neck_2_dr', 'neck_3_dr', 'neck_3')
        if cmds.objExists('head_driver_grp'):
            self.con_bridge1('neck_3_dr', 'head_dr', 'head')
        driverAttrs = [u'chest_dr_',
                       u'chest_dr_D',
                       u'chest_dr_F',
                       u'chest_dr_B',
                       u'chect_mid_dr_',
                       u'chect_mid_dr_D',
                       u'chect_mid_dr_F',
                       u'chect_mid_dr_B',
                       u'neck_1_dr_',
                       u'neck_1_dr_D',
                       u'neck_1_dr_F',
                       u'neck_1_dr_B',
                       u'head_dr_',
                       u'head_dr_D',
                       u'head_dr_F',
                       u'head_dr_B',
                       u'L_shoulder_dr_U',
                       u'L_shoulder_dr_D',
                       u'L_shoulder_dr_F',
                       u'L_shoulder_dr_B',
                       u'L_shoulder_dr_UF',
                       u'L_shoulder_dr_UB',
                       u'L_shoulder_dr_DF',
                       u'L_shoulder_dr_DB',
                       u'L_arm_dr_U',
                       u'L_arm_dr_D',
                       u'L_arm_dr_F',
                       u'L_arm_dr_B',
                       u'L_arm_dr_UF',
                       u'L_arm_dr_UB',
                       u'L_arm_dr_DF',
                       u'L_arm_dr_DB',
                       u'L_lowarm_dr_U',
                       u'L_lowarm_dr_D',
                       u'L_lowarm_dr_F',
                       u'L_lowarm_dr_B',
                       u'L_lowarm_dr_UF',
                       u'L_lowarm_dr_UB',
                       u'L_lowarm_dr_DF',
                       u'L_lowarm_dr_DB',
                       u'L_hand_dr_U',
                       u'L_hand_dr_D',
                       u'L_hand_dr_F',
                       u'L_hand_dr_B',
                       u'L_hand_dr_UF',
                       u'L_hand_dr_UB',
                       u'L_hand_dr_DF',
                       u'L_hand_dr_DB',
                       u'L_thumbfinger_1_dr_',
                       u'L_thumbfinger_1_dr_D',
                       u'L_thumbfinger_1_dr_F',
                       u'L_thumbfinger_1_dr_B',
                       u'L_thumbfinger_2_dr_',
                       u'L_thumbfinger_2_dr_D',
                       u'L_thumbfinger_2_dr_F',
                       u'L_thumbfinger_2_dr_B',
                       u'L_thumbfinger_3_dr_',
                       u'L_thumbfinger_3_dr_D',
                       u'L_thumbfinger_3_dr_F',
                       u'L_thumbfinger_3_dr_B',
                       u'L_thumbfinger_4_dr_',
                       u'L_thumbfinger_4_dr_D',
                       u'L_thumbfinger_4_dr_F',
                       u'L_thumbfinger_4_dr_B',
                       u'L_indexfinger_1_dr_',
                       u'L_indexfinger_1_dr_D',
                       u'L_indexfinger_1_dr_F',
                       u'L_indexfinger_1_dr_B',
                       u'L_indexfinger_2_dr_',
                       u'L_indexfinger_2_dr_D',
                       u'L_indexfinger_2_dr_F',
                       u'L_indexfinger_2_dr_B',
                       u'L_indexfinger_3_dr_',
                       u'L_indexfinger_3_dr_D',
                       u'L_indexfinger_3_dr_F',
                       u'L_indexfinger_3_dr_B',
                       u'L_indexfinger_4_dr_',
                       u'L_indexfinger_4_dr_D',
                       u'L_indexfinger_4_dr_F',
                       u'L_indexfinger_4_dr_B',
                       u'L_middlefinger_1_dr_',
                       u'L_middlefinger_1_dr_D',
                       u'L_middlefinger_1_dr_F',
                       u'L_middlefinger_1_dr_B',
                       u'L_middlefinger_2_dr_',
                       u'L_middlefinger_2_dr_D',
                       u'L_middlefinger_2_dr_F',
                       u'L_middlefinger_2_dr_B',
                       u'L_middlefinger_3_dr_',
                       u'L_middlefinger_3_dr_D',
                       u'L_middlefinger_3_dr_F',
                       u'L_middlefinger_3_dr_B',
                       u'L_middlefinger_4_dr_',
                       u'L_middlefinger_4_dr_D',
                       u'L_middlefinger_4_dr_F',
                       u'L_middlefinger_4_dr_B',
                       u'L_ringfinger_1_dr_',
                       u'L_ringfinger_1_dr_D',
                       u'L_ringfinger_1_dr_F',
                       u'L_ringfinger_1_dr_B',
                       u'L_ringfinger_2_dr_',
                       u'L_ringfinger_2_dr_D',
                       u'L_ringfinger_2_dr_F',
                       u'L_ringfinger_2_dr_B',
                       u'L_ringfinger_3_dr_',
                       u'L_ringfinger_3_dr_D',
                       u'L_ringfinger_3_dr_F',
                       u'L_ringfinger_3_dr_B',
                       u'L_ringfinger_4_dr_',
                       u'L_ringfinger_4_dr_D',
                       u'L_ringfinger_4_dr_F',
                       u'L_ringfinger_4_dr_B',
                       u'L_pinkyfinger_1_dr_',
                       u'L_pinkyfinger_1_dr_D',
                       u'L_pinkyfinger_1_dr_F',
                       u'L_pinkyfinger_1_dr_B',
                       u'L_pinkyfinger_2_dr_',
                       u'L_pinkyfinger_2_dr_D',
                       u'L_pinkyfinger_2_dr_F',
                       u'L_pinkyfinger_2_dr_B',
                       u'L_pinkyfinger_3_dr_',
                       u'L_pinkyfinger_3_dr_D',
                       u'L_pinkyfinger_3_dr_F',
                       u'L_pinkyfinger_3_dr_B',
                       u'L_pinkyfinger_4_dr_',
                       u'L_pinkyfinger_4_dr_D',
                       u'L_pinkyfinger_4_dr_F',
                       u'L_pinkyfinger_4_dr_B',
                       u'R_shoulder_dr_U',
                       u'R_shoulder_dr_D',
                       u'R_shoulder_dr_F',
                       u'R_shoulder_dr_B',
                       u'R_shoulder_dr_UF',
                       u'R_shoulder_dr_UB',
                       u'R_shoulder_dr_DF',
                       u'R_shoulder_dr_DB',
                       u'R_arm_dr_U',
                       u'R_arm_dr_D',
                       u'R_arm_dr_F',
                       u'R_arm_dr_B',
                       u'R_arm_dr_UF',
                       u'R_arm_dr_UB',
                       u'R_arm_dr_DF',
                       u'R_arm_dr_DB',
                       u'R_lowarm_dr_U',
                       u'R_lowarm_dr_D',
                       u'R_lowarm_dr_F',
                       u'R_lowarm_dr_B',
                       u'R_lowarm_dr_UF',
                       u'R_lowarm_dr_UB',
                       u'R_lowarm_dr_DF',
                       u'R_lowarm_dr_DB',
                       u'R_hand_dr_U',
                       u'R_hand_dr_D',
                       u'R_hand_dr_F',
                       u'R_hand_dr_B',
                       u'R_hand_dr_UF',
                       u'R_hand_dr_UB',
                       u'R_hand_dr_DF',
                       u'R_hand_dr_DB',
                       u'R_thumbfinger_1_dr_',
                       u'R_thumbfinger_1_dr_D',
                       u'R_thumbfinger_1_dr_F',
                       u'R_thumbfinger_1_dr_B',
                       u'R_thumbfinger_2_dr_',
                       u'R_thumbfinger_2_dr_D',
                       u'R_thumbfinger_2_dr_F',
                       u'R_thumbfinger_2_dr_B',
                       u'R_thumbfinger_3_dr_',
                       u'R_thumbfinger_3_dr_D',
                       u'R_thumbfinger_3_dr_F',
                       u'R_thumbfinger_3_dr_B',
                       u'R_thumbfinger_4_dr_',
                       u'R_thumbfinger_4_dr_D',
                       u'R_thumbfinger_4_dr_F',
                       u'R_thumbfinger_4_dr_B',
                       u'R_indexfinger_1_dr_',
                       u'R_indexfinger_1_dr_D',
                       u'R_indexfinger_1_dr_F',
                       u'R_indexfinger_1_dr_B',
                       u'R_indexfinger_2_dr_',
                       u'R_indexfinger_2_dr_D',
                       u'R_indexfinger_2_dr_F',
                       u'R_indexfinger_2_dr_B',
                       u'R_indexfinger_3_dr_',
                       u'R_indexfinger_3_dr_D',
                       u'R_indexfinger_3_dr_F',
                       u'R_indexfinger_3_dr_B',
                       u'R_indexfinger_4_dr_',
                       u'R_indexfinger_4_dr_D',
                       u'R_indexfinger_4_dr_F',
                       u'R_indexfinger_4_dr_B',
                       u'R_middlefinger_1_dr_',
                       u'R_middlefinger_1_dr_D',
                       u'R_middlefinger_1_dr_F',
                       u'R_middlefinger_1_dr_B',
                       u'R_middlefinger_2_dr_',
                       u'R_middlefinger_2_dr_D',
                       u'R_middlefinger_2_dr_F',
                       u'R_middlefinger_2_dr_B',
                       u'R_middlefinger_3_dr_',
                       u'R_middlefinger_3_dr_D',
                       u'R_middlefinger_3_dr_F',
                       u'R_middlefinger_3_dr_B',
                       u'R_middlefinger_4_dr_',
                       u'R_middlefinger_4_dr_D',
                       u'R_middlefinger_4_dr_F',
                       u'R_middlefinger_4_dr_B',
                       u'R_ringfinger_1_dr_',
                       u'R_ringfinger_1_dr_D',
                       u'R_ringfinger_1_dr_F',
                       u'R_ringfinger_1_dr_B',
                       u'R_ringfinger_2_dr_',
                       u'R_ringfinger_2_dr_D',
                       u'R_ringfinger_2_dr_F',
                       u'R_ringfinger_2_dr_B',
                       u'R_ringfinger_3_dr_',
                       u'R_ringfinger_3_dr_D',
                       u'R_ringfinger_3_dr_F',
                       u'R_ringfinger_3_dr_B',
                       u'R_ringfinger_4_dr_',
                       u'R_ringfinger_4_dr_D',
                       u'R_ringfinger_4_dr_F',
                       u'R_ringfinger_4_dr_B',
                       u'R_pinkyfinger_1_dr_',
                       u'R_pinkyfinger_1_dr_D',
                       u'R_pinkyfinger_1_dr_F',
                       u'R_pinkyfinger_1_dr_B',
                       u'R_pinkyfinger_2_dr_',
                       u'R_pinkyfinger_2_dr_D',
                       u'R_pinkyfinger_2_dr_F',
                       u'R_pinkyfinger_2_dr_B',
                       u'R_pinkyfinger_3_dr_',
                       u'R_pinkyfinger_3_dr_D',
                       u'R_pinkyfinger_3_dr_F',
                       u'R_pinkyfinger_3_dr_B',
                       u'R_pinkyfinger_4_dr_',
                       u'R_pinkyfinger_4_dr_D',
                       u'R_pinkyfinger_4_dr_F',
                       u'R_pinkyfinger_4_dr_B',
                       u'L_leg_dr_U',
                       u'L_leg_dr_D',
                       u'L_leg_dr_F',
                       u'L_leg_dr_B',
                       u'L_leg_dr_UF',
                       u'L_leg_dr_UB',
                       u'L_leg_dr_DF',
                       u'L_leg_dr_DB',
                       u'L_lowleg_dr_U',
                       u'L_lowleg_dr_D',
                       u'L_lowleg_dr_F',
                       u'L_lowleg_dr_B',
                       u'L_lowleg_dr_UF',
                       u'L_lowleg_dr_UB',
                       u'L_lowleg_dr_DF',
                       u'L_lowleg_dr_DB',
                       u'L_foot_dr_U',
                       u'L_foot_dr_D',
                       u'L_foot_dr_F',
                       u'L_foot_dr_B',
                       u'L_foot_dr_UF',
                       u'L_foot_dr_UB',
                       u'L_foot_dr_DF',
                       u'L_foot_dr_DB',
                       u'L_toebase_dr_U',
                       u'L_toebase_dr_D',
                       u'L_toebase_dr_F',
                       u'L_toebase_dr_B',
                       u'L_toebase_dr_UF',
                       u'L_toebase_dr_UB',
                       u'L_toebase_dr_DF',
                       u'L_toebase_dr_DB',
                       u'R_leg_dr_U',
                       u'R_leg_dr_D',
                       u'R_leg_dr_F',
                       u'R_leg_dr_B',
                       u'R_leg_dr_UF',
                       u'R_leg_dr_UB',
                       u'R_leg_dr_DF',
                       u'R_leg_dr_DB',
                       u'R_lowleg_dr_U',
                       u'R_lowleg_dr_D',
                       u'R_lowleg_dr_F',
                       u'R_lowleg_dr_B',
                       u'R_lowleg_dr_UF',
                       u'R_lowleg_dr_UB',
                       u'R_lowleg_dr_DF',
                       u'R_lowleg_dr_DB',
                       u'R_foot_dr_U',
                       u'R_foot_dr_D',
                       u'R_foot_dr_F',
                       u'R_foot_dr_B',
                       u'R_foot_dr_UF',
                       u'R_foot_dr_UB',
                       u'R_foot_dr_DF',
                       u'R_foot_dr_DB',
                       u'R_toebase_dr_U',
                       u'R_toebase_dr_D',
                       u'R_toebase_dr_F',
                       u'R_toebase_dr_B',
                       u'R_toebase_dr_UF',
                       u'R_toebase_dr_UB',
                       u'R_toebase_dr_DF',
                       u'R_toebase_dr_DB']
        for driverAttr in driverAttrs:
            cmds.connectAttr('body_sdk_handle.' + driverAttr, 'body_sdk_handle_org.' + driverAttr)

        sys.stderr.write(u'#---is ok')

    def con_bridge1(self, jnt1, jnt2, bridge):
        cmds.parentConstraint(jnt1, bridge + '_driver_grp', mo=1)
        cmds.parentConstraint(jnt2, bridge + '_driver_posLoc', mo=1)
        if 'L_' == jnt1[:2]:
            jnt1 = 'R_' + jnt1[2:]
        if 'L_' == jnt2[:2]:
            jnt2 = 'R_' + jnt2[2:]
        if 'L_' == bridge[:2]:
            bridge = 'R_' + bridge[2:]
        cmds.parentConstraint(jnt1, bridge + '_driver_grp', mo=1)
        cmds.parentConstraint(jnt2, bridge + '_driver_posLoc', mo=1)

    def bsTool(self):
        import BSE
        reload(BSE)
        BSE.BSEditToolsUI('')

    def blendShapeNode(self, MeshNode):
        BlendShapeNode = []
        try:
            meshHistory = cmds.listHistory(MeshNode, pdo=True)
            BlendShapeNode = cmds.ls(meshHistory, type='blendShape')
        except TypeError:
            pass

        return BlendShapeNode

    def checkBlendShapeName(self):
        """\xe4\xbf\xae\xe6\x94\xb9blendShape\xe5\x91\xbd\xe5\x90\x8d"""
        errorstr = u'BlendShape\u547d\u540d\u4e0d\u89c4\u8303\n\u6b63\u786e\u547d\u540d:\u6a21\u578b\u540d_blendShape'
        issues = []
        meshShapes = cmds.ls(type='mesh')
        for meshShape in meshShapes:
            mesh = cmds.listRelatives(meshShape, p=True)[0]
            bsNode = self.blendShapeNode(mesh)
            if bsNode != []:
                print(mesh, '\n', bsNode[0], '\n')
                if bsNode[0] != mesh + '_blendShape':
                    print('modelName:------', mesh)
                    print('old_bs_name:------', bsNode)
                    print('new_bs_name:------', mesh + '_blendShape')
                    cmds.rename(bsNode[0], mesh + '_blendShape')

        sys.stderr.write(u'------is ok')

    def createBlendShape(self, targetModel, addblendShapeModel):
        targetModel1 = targetModel.split(':')[-1]
        bsNode = cmds.blendShape(targetModel, addblendShapeModel)[0]
        cmds.setAttr(bsNode + '.' + targetModel1, 1)

    def parobj(self, objs, pargrp):
        for obj in objs:
            if cmds.objExists(obj) == True:
                obj_grp = cmds.listRelatives(obj, p=True)
                if obj_grp == None:
                    cmds.parent(obj, pargrp)
                elif obj_grp[0] != pargrp:
                    cmds.parent(obj, pargrp)
            else:
                cmds.warning(obj + u'---\u7269\u4f53\u4e0d\u5b58\u5728\uff0c\u8bf7\u68c0\u67e5')

        return

    def parent_to_world(self, objs):
        for obj in objs:
            if cmds.objExists(obj) == True:
                if cmds.listRelatives(obj, p=True) != None:
                    cmds.parent(obj, w=True)
            else:
                cmds.warning(obj + u'---\u7269\u4f53\u4e0d\u5b58\u5728\uff0c\u8bf7\u68c0\u67e5')

        return

    def face_clear_up(self):
        print('grp')
        ziva_face_rig_grp = 'ziva_face_rig_grp'
        if cmds.objExists('ziva_face_rig_grp') != True:
            ziva_face_rig_grp = cmds.group(em=True, name=ziva_face_rig_grp)
        print('parent')
        ziva_face_rig_objs = ['face_control',
                              'face_joint',
                              'Mesh_fol',
                              'face_follicle_grp',
                              'teeth_rivet_geo',
                              'tongue_fol_grp',
                              'head_skin']
        self.parobj(ziva_face_rig_objs, ziva_face_rig_grp)
        face_ctrl_grps = ['facial_UI_Env', 'teeth_ctrl_all', 'eye_rig_all']
        self.parobj(face_ctrl_grps, 'face_UI_rig_all')
        print('parent -w')
        self.parent_to_world(['eye_follow_head_joint', 'teeth_follow_head_joint'])
        print('bs')
        self.createBlendShape('head_mdl', 'Mesh_fol')
        print('rename')
        jnts = cmds.listRelatives('face_joint', ad=True, type='joint')
        for jnt in jnts:
            if jnt[:5] != 'face_':
                cmds.rename(jnt, 'face_' + jnt)

        sys.stderr.write(u'------\u8868\u60c5\u6574\u7406 is ok')

    def face_body_rig_combine(self):
        self.face_body_rig_combineHelp()
        cmds.select('ziva_face_rig_grp', 'eye_follow_head_joint', 'teeth_follow_head_joint', 'face_UI_rig_all')
        objs = ['rig_grp',
                'ziva_face_rig_grp',
                'Head',
                'eye_follow_head_joint',
                'teeth_follow_head_joint',
                'head_ctrl',
                'face_UI_rig_all']
        if cmds.listRelatives('ziva_face_rig_grp', p=True)[0] != 'rig_grp':
            cmds.parent('ziva_face_rig_grp', 'rig_grp')
        if cmds.listRelatives('eye_follow_head_joint', p=True)[0] != 'Head':
            cmds.parent('eye_follow_head_joint', 'teeth_follow_head_joint', 'Head')
        if cmds.listRelatives('face_UI_rig_all', p=True)[0] != 'head_ctrl':
            cmds.parent('face_UI_rig_all', 'head_ctrl')
        facejnts = ['Spine',
                    'Spine1',
                    'Spine2',
                    'Spine3',
                    'Spine4',
                    'Chest',
                    'ChestMid',
                    'Neck1',
                    'Neck2',
                    'Neck3',
                    'Head',
                    'LeftShoulder',
                    'RightShoulder',
                    'LeftArm',
                    'LeftArm_sec1',
                    'RightArm',
                    'RightArm_sec1']

    def face_body_rig_combineHelp(self):
        winName = 'face_body_rig_combineHelp'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t='face_body_rig_combineHelp')
        columnLayout1 = cmds.columnLayout(adjustableColumn=True)
        cmds.scrollField(editable=True, wordWrap=True,
                         text=u'\u5de5\u5177\u5b8c\u6210\u5185\u5bb9:\nziva\u7684\u8bbe\u7f6e\u7ec4(ziva_face_rig_grp) P\u5230 rig_grp\u7ec4\u4e0b\u9762\n\u773c\u7403\u548c\u7259\u9f7f\u7684\u9aa8\u9abc P\u5230 \u8eab\u4f53\u5934\u90e8\u9aa8\u9abc(Head)\u4e0b\u9762\n\u8868\u60c5\u63a7\u5236\u5668\u7ec4(face_UI_rig_all) P\u5230 \u5934\u90e8\u63a7\u5236\u5668(head_ctrl)\u4e0b\u9762\n\n\n\u5de5\u5177\u6682\u65e0\u6cd5\u5b8c\u6210\u5185\u5bb9:\n\u628a\u8868\u60c5\u7684\u6a21\u578b(\u5934\uff0c\u7259\u9f7f\uff0c\u773c\u7403) \u66ff\u6362\u76f8\u5e94\u5c42\u7ea7\u4e0b\u7684\u6a21\u578b\n\u4f7f\u7528\u8eab\u4f53\u7684\u9aa8\u9abc\u7ea6\u675f\u5934\u90e8\u7684\u9aa8\u9abc\n\u4f7f\u7528\u8868\u60c5\u6b21\u7ea7\u63a7\u5236\u5668\u7ea6\u675f\u8868\u60c5\u7684\u6b21\u7ea7\u9aa8\u9abc\n',
                         w=400)
        cmds.setParent('..')
        cmds.showWindow()

    def repairBlendShapeTar(self):
        allBsList = cmds.ls(type='blendShape')
        for bsE in allBsList:
            bsErrorList = []
            weightAttrList = cmds.listAttr(bsE + '.w', m=True)
            maxIndex = len(weightAttrList)
            for i in range(maxIndex):
                itgName = bsE + '.it[0].itg[%s]' % i
                if cmds.listAttr(itgName + '.iti', m=True) == None:
                    cmds.getAttr(itgName + '.iti[6000].igt')
                    bsErrorList.append('%s%s%s' % (i, '-', weightAttrList[i]))

            if bsErrorList:
                sys.stderr.write(u'%s  \u76ee\u6807\u4f53\u4fee\u590d %s \u4e2a:  %s\n' % (
                    bsE, len(bsErrorList), '  '.join(bsErrorList)))

        return

    def checkSkin(self):
        skinNodeList = cmds.ls(type='skinCluster')
        errorskin = []
        for skin in skinNodeList:
            if cmds.getAttr(skin + '.envelope') == 0:
                errorskin.append(skin)

        if errorskin != []:
            cmds.error(u'\u4ee5\u4e0b\u8499\u76ae\u4e3a\u5173\u95ed\u72b6\u6001\uff0c\u8bf7\u68c0\u67e5---', errorskin)

    def openSkin(self):
        skinNodeList = cmds.ls(type='skinCluster')
        for skin in skinNodeList:
            cmds.setAttr(skin + '.envelope', 1)

    def closeSkin(self):
        skinNodeList = cmds.ls(type='skinCluster')
        for skin in skinNodeList:
            cmds.setAttr(skin + '.envelope', 0)

    def ________________________fbx_rig_________________________(self):
        pass

    def Disconnect_bsTarget(self):
        if cmds.objExists('temp_model') == True:
            cmds.delete('temp_model')
            print(u'\u5220\u9664\u4e86 temp_model \u7ec4')
        bsNodes = cmds.ls(type='blendShape')
        for bsNode in bsNodes:
            listTarget = cmds.listAttr(bsNode + '.weight', multi=True)
            if listTarget != None:
                for i in listTarget:
                    targetConnect = cmds.listConnections(bsNode + '.' + i, p=True, s=True, d=False)
                    if targetConnect != None:
                        for m in targetConnect:
                            cmds.disconnectAttr(m, bsNode + '.' + i)

        sys.stderr.write(u'------Disconnect bs Target is ok')
        if cmds.objExists('ac_cn_settings_ctrl') == True:
            cmds.setAttr('ac_cn_settings_ctrl.geo_display_type', 0)
        return

    def deleteAllConstraint(self):
        selTypes = ['parentConstraint',
                    'pointConstraint',
                    'orientConstraint',
                    'scaleConstraint',
                    'aimConstraint',
                    'pointOnPolyConstraint',
                    'geometryConstraint',
                    'normalConstraint',
                    'tangentConstraint',
                    'poleVectorConstraint']
        for selType in selTypes:
            objs = cmds.ls(type=selType)
            if objs != []:
                cmds.delete(objs)

        self.DisconnectJnt_unlockJntAttr()
        sys.stderr.write(u'delete All Constraint')

    def DisconnectJnt_unlockJntAttr(self):
        attrs = ['t',
                 'r',
                 's',
                 'tx',
                 'ty',
                 'tz',
                 'rx',
                 'ry',
                 'rz',
                 'sx',
                 'sy',
                 'sz',
                 'visibility',
                 'radi',
                 'inverseScale']
        jnts = cmds.ls(type='joint')
        for jnt in jnts:
            cmds.setAttr(jnt + '.visibility', lock=0)
            cmds.setAttr(jnt + '.visibility', 1)
            for attr in attrs:
                cmds.setAttr(jnt + '.' + attr, lock=0)
                parCons = cmds.listConnections(jnt + '.' + attr, p=True, s=True, d=False)
                if parCons != None:
                    for parCon in parCons:
                        cmds.disconnectAttr(parCon, jnt + '.' + attr)

        sys.stderr.write(u'DisconnectJnt UnlockJntAttr')
        return

    def unlockJntAttr(self):
        jnts = cmds.ls(type='joint')
        attrs = ['tx',
                 'ty',
                 'tz',
                 'rx',
                 'ry',
                 'rz',
                 'sx',
                 'sy',
                 'sz',
                 'v',
                 'radi']
        for jnt in jnts:
            for attr in attrs:
                cmds.setAttr(jnt + '.' + attr, lock=0)

    def delbindPose(self):
        Bpose = cmds.ls(type='dagPose')
        if Bpose != []:
            cmds.delete(Bpose)
        sys.stderr.write(u'del BindPose')

    def delExpression(self):
        expressions = cmds.ls(type='expression')
        if expressions != []:
            cmds.delete(expressions)
            print(expressions)
        sys.stderr.write(u'del expression')

    def ____________ctrl_rig_and_fbx_rig_comparison_blendShape____________(self):
        pass

    def rigBsTarComparisonWin(self):
        win = 'rigBsTarComparison'
        if cmds.window(win, exists=True):
            cmds.deleteUI(win)
        simulationWindow = cmds.window(win, t='rigBsTarComparison')
        child1 = cmds.columnLayout(adjustableColumn=True)
        cmds.rowColumnLayout(numberOfColumns=9)
        cmds.text(l=u'\u6309\u94ae', h=20, w=100)
        cmds.text(l=u'\u6587\u4ef6\u540d', h=20, w=200)
        cmds.text(l=u'blendShape\u5217\u8868', h=20, w=200)
        cmds.text(l=u'BS', h=20, w=30)
        cmds.text(l=u'target\u5217\u8868', h=20, w=200)
        cmds.text(l=u'Tar', h=20, w=40)
        cmds.text(l=u'\u5931\u6548tar', h=20, w=40)
        cmds.text(l=u'Jnt \u5217\u8868', h=20, w=100)
        cmds.text(l=u'Jnt', h=20, w=40)
        cmds.button(l=u'\u63a7\u5236\u5668 rig', c=lambda *args: self.get_ctrlrig_BsTarData(), h=30, w=100)
        cmds.textField('ctrl_rig_asset_tf', text=u'asset', h=30, w=200)
        cmds.textField('ctrl_rig_bs_tf', text=u'ctrl_rig_bs\u6570\u636e', h=30, w=200)
        cmds.textField('ctrl_rig_bs_num_tf', text=u'\u6570\u91cf', h=30, w=30)
        cmds.textField('ctrl_rig_tar_tf', text=u'ctrl_rig_tar\u6570\u636e', h=30, w=200)
        cmds.textField('ctrl_rig_tar_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.textField('ctrl_rig_errortar_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.textField('ctrl_rig_jnt_tf', text=u'\u5217\u8868', h=30, w=100)
        cmds.textField('ctrl_rig_jnt_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.button(l=u'FBX rig', c=lambda *args: self.get_fbxrig_BsTarData(), h=30, w=100)
        cmds.textField('fbx_rig_asset_tf', text=u'asset', h=30, w=200)
        cmds.textField('fbx_rig_bs_tf', text=u'fbx_rig_bs\u6570\u636e', h=30, w=200)
        cmds.textField('fbx_rig_bs_num_tf', text=u'\u6570\u91cf', h=30, w=30)
        cmds.textField('fbx_rig_tar_tf', text=u'fbx_rig_tar\u6570\u636e', h=30, w=200)
        cmds.textField('fbx_rig_tar_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.textField('fbx_rig_errortar_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.textField('fbx_rig_jnt_tf', text=u'\u5217\u8868', h=30, w=100)
        cmds.textField('fbx_rig_jnt_num_tf', text=u'\u6570\u91cf', h=30, w=40)
        cmds.setParent('..')
        cmds.button('comparisonBut', l=u'\u5bf9\u6bd4', c=lambda *args: self.rigBsTarComparison(), h=30)
        cmds.showWindow()

    def editUI(self):
        winName = 'message'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        bgc = [0.1686, 0.1686, 0.1686]
        cmds.textField('ctrl_rig_asset_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_bs_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_bs_num_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_tar_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_tar_num_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_jnt_tf', e=True, bgc=bgc)
        cmds.textField('ctrl_rig_jnt_num_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_asset_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_bs_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_bs_num_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_tar_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_tar_num_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_jnt_tf', e=True, bgc=bgc)
        cmds.textField('fbx_rig_jnt_num_tf', e=True, bgc=bgc)

    def get_ctrlrig_BsTarData(self):
        bgc = [0.1686, 0.1686, 0.1686]
        cmds.textField('ctrl_rig_asset_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_bs_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_bs_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_tar_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_tar_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_errortar_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_jnt_tf', e=True, text='', bgc=bgc)
        cmds.textField('ctrl_rig_jnt_num_tf', e=True, text='', bgc=bgc)
        if cmds.ls('*_ctrl') == []:
            cmds.error(u'\u5f53\u524d\u6587\u4ef6\u4e0d\u662f\u63a7\u5236\u5668\u7ed1\u5b9a')
        else:
            self.get_render_modelBsTarData('ctrl_rig_asset_tf', 'ctrl_rig_bs_tf', 'ctrl_rig_bs_num_tf',
                                           'ctrl_rig_tar_tf', 'ctrl_rig_tar_num_tf', 'ctrl_rig_errortar_num_tf',
                                           'ctrl_rig_jnt_tf', 'ctrl_rig_jnt_num_tf')

    def get_fbxrig_BsTarData(self):
        bgc = [0.1686, 0.1686, 0.1686]
        cmds.textField('fbx_rig_asset_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_bs_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_bs_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_tar_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_tar_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_errortar_num_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_jnt_tf', e=True, text='', bgc=bgc)
        cmds.textField('fbx_rig_jnt_num_tf', e=True, text='', bgc=bgc)
        if cmds.ls('*_ctrl') != []:
            cmds.error(
                u'\u5f53\u524d\u6587\u4ef6\u5b58\u5728*_ctrl,\u4e0d\u662f\u7eaf\u9aa8\u9abcFBX\u7ed1\u5b9a,\u8bf7\u8f7d\u5165\u7eaf\u9aa8\u9abc\u7ed1\u5b9a')
        else:
            self.get_render_modelBsTarData('fbx_rig_asset_tf', 'fbx_rig_bs_tf', 'fbx_rig_bs_num_tf', 'fbx_rig_tar_tf',
                                           'fbx_rig_tar_num_tf', 'fbx_rig_errortar_num_tf', 'fbx_rig_jnt_tf',
                                           'fbx_rig_jnt_num_tf')

    def get_render_modelBsTarData(self, assetTf, bsListTf, bsNumTF, tarListTf, tarNumTF, errorTarNumTF, jnt_listTF,
                                  jnt_num_tf):
        self.editUI()
        geometryGroup = 'render_model'
        bsList = []
        bstarsList = []
        alltars = []
        models = []
        meshs = cmds.listRelatives('render_model', ad=True, type='mesh')
        for mesh in meshs:
            model = cmds.listRelatives(mesh, p=True)[0]
            if model not in models:
                models.append(model)

        models.sort()
        errorTars = []
        for transformNode in models:
            meshHistory = cmds.listHistory(transformNode, pdo=True)
            bsNodeList = cmds.ls(meshHistory, type='blendShape')
            if bsNodeList != []:
                bsE = bsNodeList[0]
                bsErrorList = []
                bstars = cmds.listAttr(bsE + '.w', m=True)
                maxIndex = len(bstars)
                for i in range(maxIndex):
                    bstar = bstars[i]
                    itgName = bsE + '.it[0].itg[%s]' % i
                    if cmds.listAttr(itgName + '.iti', m=True) == None:
                        errorTars.append(bstar)

                if bsE not in bsList:
                    bsList.append(bsE)
                    bstarsList.append(bstars)
                    alltars = alltars + bstars

        asset = cmds.file(q=1, sn=1).split('/')[-1]
        cmds.textField(assetTf, e=True, text=asset)
        cmds.textField(bsListTf, e=True, text=str(bsList))
        cmds.textField(tarListTf, e=True, text=str(bstarsList))
        cmds.textField(bsNumTF, e=True, text=len(bsList))
        cmds.textField(tarNumTF, e=True, text=len(alltars))
        if len(errorTars) > 0:
            cmds.textField(errorTarNumTF, e=True, text=len(errorTars), bgc=[0.75, 0, 0])
        else:
            cmds.textField(errorTarNumTF, e=True, text=len(errorTars), bgc=[0.4, 0.4, 0])
        hipsjnt = 'Hips'
        if cmds.objExists(hipsjnt) != True:
            hipsjnt = cmds.ls(sl=True)[0]
        jnts = cmds.listRelatives(hipsjnt, ad=True, type='joint')
        cmds.textField(jnt_listTF, e=True, text=str(jnts))
        cmds.textField(jnt_num_tf, e=True, text=len(jnts))
        return

    def rigBsTarComparison(self):
        ctrl_rig_bsList = eval(cmds.textField('ctrl_rig_bs_tf', q=True, text=True))
        ctrl_rig_tarList = eval(cmds.textField('ctrl_rig_tar_tf', q=True, text=True))
        fbx_rig_bsList = eval(cmds.textField('fbx_rig_bs_tf', q=True, text=True))
        fbx_rig_tarList = eval(cmds.textField('fbx_rig_tar_tf', q=True, text=True))
        ctrl_rig_errortar_num = int(cmds.textField('ctrl_rig_errortar_num_tf', q=True, text=True))
        fbx_rig_errortar_num = int(cmds.textField('fbx_rig_errortar_num_tf', q=True, text=True))
        ctrl_rig_jntList = eval(cmds.textField('ctrl_rig_jnt_tf', q=True, text=True))
        fbx_rig_jntList = eval(cmds.textField('fbx_rig_jnt_tf', q=True, text=True))
        messagestr = ''
        fbxRig_absenceBsList = []
        tardiff_bslist = []
        fbxRig_absenceTarList = []
        for i in range(len(ctrl_rig_bsList)):
            ctrl_rig_bs = ctrl_rig_bsList[i]
            ctrl_rig_tars = ctrl_rig_tarList[i]
            if ctrl_rig_bs not in fbx_rig_bsList:
                fbxRig_absenceBsList.append(ctrl_rig_bs + '-' + str(len(ctrl_rig_tars)))
            else:
                i1 = fbx_rig_bsList.index(ctrl_rig_bs)
                print(i, i1)
                fbx_rig_tars = fbx_rig_tarList[i1]
                if fbx_rig_tars != ctrl_rig_tars:
                    tardiff_bslist.append(ctrl_rig_bs)
                    for ctrl_rig_tar in ctrl_rig_tars:
                        if ctrl_rig_tar not in fbx_rig_tars:
                            fbxRig_absenceTarList.append(ctrl_rig_tar)

        print(fbxRig_absenceBsList)
        print(tardiff_bslist)
        print(fbxRig_absenceTarList)
        if ctrl_rig_bsList != fbx_rig_bsList:
            cmds.textField('ctrl_rig_bs_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('fbx_rig_bs_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('ctrl_rig_bs_num_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('fbx_rig_bs_num_tf', e=True, bgc=[0.75, 0, 0])
            messagestr = messagestr + u'fbx rig bs\u8282\u70b9\u7f3a\u5c11----' + str(fbxRig_absenceBsList) + '\n'
        if ctrl_rig_tarList != fbx_rig_tarList:
            cmds.textField('ctrl_rig_tar_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('fbx_rig_tar_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('ctrl_rig_tar_num_tf', e=True, bgc=[0.75, 0, 0])
            cmds.textField('fbx_rig_tar_num_tf', e=True, bgc=[0.75, 0, 0])
        if tardiff_bslist != []:
            messagestr = messagestr + u'tar\u4e0d\u540c\u7684bs\u8282\u70b9:---' + str(tardiff_bslist) + '\n'
            messagestr = messagestr + u'fabx rig tar\u7f3a\u5c11:---' + str(fbxRig_absenceTarList) + '\n'
        if ctrl_rig_errortar_num != 0 and fbx_rig_errortar_num != 0:
            messagestr = messagestr + u'\u6709\u5931\u6548\u7684tar:---\u63a7\u5236\u5668rig:' + str(
                ctrl_rig_errortar_num) + u'\u4e2a,fbx rig:' + str(fbx_rig_errortar_num) + u'\u4e2a' + '\n'
        if ctrl_rig_jntList != fbx_rig_jntList:
            messagestr = messagestr + u'\u9aa8\u9abc\u4e0d\u4e00\u81f4:---' + '\n' + str(ctrl_rig_jntList) + '\n' + str(
                fbx_rig_jntList)
            jnt_bgc = [0.75, 0, 0]
        else:
            jnt_bgc = [0.4, 0.4, 0]
        cmds.textField('ctrl_rig_jnt_tf', e=True, bgc=jnt_bgc)
        cmds.textField('ctrl_rig_jnt_num_tf', e=True, bgc=jnt_bgc)
        cmds.textField('fbx_rig_jnt_tf', e=True, bgc=jnt_bgc)
        cmds.textField('fbx_rig_jnt_num_tf', e=True, bgc=jnt_bgc)
        ctrl_rig_jntList_sort = ctrl_rig_jntList + []
        fbx_rig_jntList_sort = fbx_rig_jntList + []
        ctrl_rig_jntList_sort.sort()
        fbx_rig_jntList_sort.sort()
        if ctrl_rig_jntList_sort != fbx_rig_jntList_sort:
            messagestr = messagestr + u'\u9aa8\u9abc\u4e0d\u4e00\u81f4:---' + '\n' + str(ctrl_rig_jntList) + '\n' + str(
                fbx_rig_jntList)
        if messagestr == '':
            cmds.textField('ctrl_rig_bs_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_bs_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('ctrl_rig_bs_num_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_bs_num_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('ctrl_rig_tar_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_tar_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('ctrl_rig_tar_num_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_tar_num_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('ctrl_rig_jnt_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('ctrl_rig_jnt_num_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_jnt_tf', e=True, bgc=[0.4, 0.4, 0])
            cmds.textField('fbx_rig_jnt_num_tf', e=True, bgc=[0.4, 0.4, 0])
            messagestr = 'is ok'
            sys.stderr.write(u'------is ok')
        self.errorMessage(messagestr)

    def errorMessage(self, messagestr):
        winName = 'message'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t='message')
        columnLayout1 = cmds.columnLayout(adjustableColumn=True)
        cmds.scrollField(text=messagestr, w=100, h=100)
        cmds.setParent('..')
        cmds.showWindow()

    def unlockInfluenceWeights(self):
        jnts = cmds.ls(type='joint')
        for jnt in jnts:
            if 'lockInfluenceWeights' in cmds.listAttr(jnt):
                cmds.setAttr(jnt + '.liw', 0)
