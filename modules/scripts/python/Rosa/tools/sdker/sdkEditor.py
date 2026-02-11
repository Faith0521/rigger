#!/usr/bin/python
# -*- coding: utf-8 -*-
#--------------------------------------------<<<<<rosa_SdkManager.py - Python Script>>>>>--------------------------------------------------#
# AUTHOR: rosa.w
# MAIL: wrx1844@qq.com
# DATE: OUT/2014
# RELEASE DATE: 08/15/2014
# LAST UPDATE: 07/24/2023
# VERSION: 1.0
# MAYA: 2023

#------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Loading......
import maya.cmds as mc
import maya.mel as mel
import sys
import traceback

from ...maya_utils import aboutName
from importlib import reload

reload(aboutName)


#------------------------------------------------------------------------------------------------------------------------------------------------------------#

def uiShow():
    sdk = sdkEditor()
    sdk.MainUI()


class sdkEditor(object):

    def __init__(self):
        super(sdkEditor, self).__init__()
        self.PoseWinName = 'getPose_win'
        self.SdkWinName = 'SDKManage_win'
        self.OriginalWinName = 'originalsdk'
        self.displayTypeUsed = ''
        self.displayTypeLR = ''
        self.drvText = ''
        self.drvField = ''
        self.rightKey01 = ''
        self.selectDriver = ''
        self.drvLoadButton = ''
        self.driverScroll = ''
        self.rightKey01 = ''
        self.mirrorpose = ''
        self.orgpose = ''
        self.gomaxpose = ''
        self.gominpose = ''
        self.drivenScroll = ''
        self.rightKey02 = ''
        self.plusDrivens = ''
        self.redutiondrivens = ''
        self.updateSel = ''
        self.mirrorSel = ''
        self.drivenAttrScroll = ''
        self.rightKey03 = ''
        self.animcEditor = ''
        self.updataButton = ''
        self.mirrorButton = ''

    def MainUI(self):
        # ------------------------------------------------------------------------------------------------------------------
        # windows
        # This is a main window for sdk manager tools ,so if you have no grasp, do not chang and edit it.
        # ------------------------------------------------------------------------------------------------------------------
        if mc.window(self.SdkWinName, exists=True):
            if mc.window(self.PoseWinName, exists=True):
                mc.deleteUI(self.SdkWinName, window=True)
                mc.deleteUI(self.PoseWinName, window=True)
            else:
                mc.deleteUI(self.SdkWinName, window=True)

        mc.window(self.SdkWinName, title="S D K - M a n a g e r - v 2.0", menuBar=True, wh=(400, 475), sizeable=False)

        # meun set

        # File
        mc.menu(label="F i l e", tearOff=False, allowOptionBoxes=True)
        mc.menuItem(label='E x p o r t - S D K - F r o m - B r i d g e',
                    c=lambda *args: self.exportSdkData(driver=[mc.textField(self.drvField, q=True, text=True)]))
        mc.menuItem(label='E x p o r t - S D K - F r o m - D r i v e n O b j s ',
                    c=lambda *args: self.exportSdkFromDrivenObjs())
        mc.menuItem(label='E x p o r t - S D K - F r o m - D r i v e n A t t r s ',
                    c=lambda *args: self.exportSdkFromDrivenAttrs())
        mc.menuItem(divider=True)
        mc.menuItem(label='I m p o r t - S D K', c=lambda *args: self.importSdkData())
        mc.menuItem(divider=True)
        mc.menuItem(label='M i r r o r - S D K',
                    c=lambda *args: self.mirrorSDK(driver=[mc.textField(self.drvField, q=True, text=True)]))
        mc.setParent('..', menu=True)
        mc.menuItem(divider=True)

        mc.menuItem(label='D e l e t e - u s e l e s s - n o d e', c=lambda *args: self.delUselessNode())
        mc.menuItem(divider=True)

        mc.menuItem(label='N o m a l i z e - S D K - n a m e s', c=lambda *args: self.renameSdkCurve())
        mc.menuItem(divider=True)
        self.displayTypeUsed = mc.menuItem(label='D i s p l a y - U s e d - D r i v e r A t t r', checkBox=True,
                                           c=lambda *args: self.load())
        self.displayTypeLR = mc.menuItem(label='D i s p l a y - L e f t - D r i v e r A t t r', checkBox=True,
                                         c=lambda *args: self.load())

        # main layout
        mainlayout = mc.columnLayout('mainLayout', adj=True)
        mc.separator(style="in", h=2)

        # load driver
        # ---------------------------------------------------------------------------------------------------------------------------------------------
        onelayout = mc.formLayout('oneForm')
        self.drvText = mc.text('drvText', label='D r i v e r :')
        self.drvField = mc.textField('drvField', ed=0, w=245)
        self.rightKey01 = mc.popupMenu()
        self.selectDriver = mc.menuItem(label='s e l e c t - b r i d g e', c=lambda *args: self.selectDriverBridge())
        self.drvLoadButton = mc.iconTextButton(style='textOnly', w=65, bgc=[0.5, 0.4, 0.33], label='L o a d',
                                               c=lambda *args: self.load())

        # set formlayout positions
        mc.formLayout(onelayout, edit=True, attachForm=[(self.drvText, 'top', 9), (self.drvText, 'left', 10)])
        mc.formLayout(onelayout, edit=True, attachForm=[(self.drvField, 'top', 8), (self.drvField, 'left', 70)])
        mc.formLayout(onelayout, edit=True,
                      attachForm=[(self.drvLoadButton, 'top', 6), (self.drvLoadButton, 'left', 325)])
        mc.setParent(mainlayout)
        # ---------------------------------------------------------------------------------------------------------------------------------------------

        mc.separator(style="in", h=9)
        # drvier and driven list
        # --------------------------------------------------------------------------------
        mc.paneLayout(configuration="vertical3", h=358, ps=([1, 40, 0], [2, 60, 0], [3, 0, 0]))

        mc.frameLayout(label='A t t r i b u t e :')
        self.driverScroll = mc.textScrollList(fn='plainLabelFont', append=[], en=False,
                                              sc=lambda *args: self.listDrivenForSelectItem())
        mc.setParent("..")
        self.rightKey01 = mc.popupMenu(button=3, markingMenu=True)

        mc.frameLayout(label='D r i v e n :')
        self.drivenScroll = mc.textScrollList(fn='plainLabelFont', ams=1, append=[], en=False,
                                              sc=lambda *args: self.listDrivenAttrForSelectItem())
        mc.setParent("..")
        self.rightKey02 = mc.popupMenu(button=3, markingMenu=True)
        self.plusDrivens = mc.menuItem(label='Add Driven ', rp='NW', c=lambda *args: self.addDrivens())
        self.redutiondrivens = mc.menuItem(label='Remove Driven', rp='SW', c=lambda *args: self.removeDrivens())
        self.updateSel = mc.menuItem(label='Update Selected ', rp='NE',
                                     c=lambda *args: self.updateSdk(updateSelected=True))
        self.mirrorSel = mc.menuItem(label='Mirror Selected', rp='SE',
                                     c=lambda *args: self.mirrorSdkForSelectItem(mirrorSelected=True))
        mc.setParent(menu=True)

        mc.frameLayout(label='D r i v e n A t t r :')
        self.drivenAttrScroll = mc.textScrollList(fn='plainLabelFont', ams=1, append=[], en=True,
                                                  sc=lambda *args: self.selectAnimCForSelectItem())
        mc.setParent("..")
        self.rightKey03 = mc.popupMenu(button=3, markingMenu=True)
        self.animcEditor = mc.menuItem(label='GraphEditor', rp='N',
                                       c=lambda *args: mel.eval('GraphEditor'))  # label='N'
        mc.setParent(menu=True)
        mc.setParent("..")

        mc.setParent(mainlayout)
        # ---------------------------------------------------------------------------------

        mc.separator(style="in", h=10)
        # mirror sdk
        # --------------------------------------------------------------------------------
        mc.formLayout('twoForm')
        #self.updataButton = mc.iconTextButton(style='textOnly', w=195, bgc=[0.23, 0.33, 0.39], label='U p d a t e', en=False, c=lambda *args: self.updateSdk(updateSelected=False))
        self.mirrorButton = mc.iconTextButton(style='textOnly', w=400, bgc=[0.5, 0.4, 0.33], label='M i r r o r',
                                              en=False,
                                              c=lambda *args: self.mirrorSdkForSelectItem(mirrorSelected=False),
                                              ann='Click this button to import the selected driver')
        # set formlayout positions
        #mc.formLayout(twolayout, edit=True, attachForm=[(self.updataButton, 'top', 0), (self.updataButton, 'left', 0), (self.updataButton, 'bottom', 5)])
        #mc.formLayout(twolayout, edit=True, attachForm=[(self.mirrorButton, 'top', 0), (self.mirrorButton, 'left', 200), (self.mirrorButton, 'bottom', 5)])

        mc.setParent("..")

        # author data
        # --------------------------------------------------------------------------------
        mc.frameLayout(lv=0)
        mc.text(label="C o p y r i g h t (C)  |  O F 3 D  -  R i g g e r  |  R u i X i", h=15, en=0, al="center")
        mc.setParent(mainlayout)
        # --------------------------------------------------------------------------------
        mc.showWindow(self.SdkWinName)

    def removeEXnodes(self, nodeName, nodeAttr, direction):

        if direction == 'sfd':
            attrSource = mc.connectionInfo(nodeName + '.' + nodeAttr, sfd=1)

            while 'unitConversion' in attrSource:
                attrSource = mc.connectionInfo(attrSource.replace('output', 'input'), sfd=1)
            if attrSource == '':
                attrSource = 'None'
            return attrSource

        elif direction == 'dfs':
            attrTargets = mc.connectionInfo(nodeName + '.' + nodeAttr, dfs=1)

            for i, attr in enumerate(attrTargets):
                if attr != '':
                    while 'unitConversion' in attrTargets[i] or 'blendWeighted' in attrTargets[i]:
                        attrTargets[i] = \
                        mc.connectionInfo(attrTargets[i][:attrTargets[i].index('.')] + '.output', dfs=1)[0]
                else:
                    attrTargets[i] = 'None'
            return attrTargets

    def fromAtoB(self, a, b, ro):
        if ro == 1:
            mc.delete(mc.parentConstraint(b, a, mo=False))
        elif ro == 0:
            mc.delete(mc.pointConstraint(b, a, mo=False))

    def makeObjZero(self, suffix, rotation, *obj):
        objNum = len(obj)

        for i in range(0, objNum, 1):
            grp = mc.createNode('transform', name='%s_%s' % (obj[i], suffix))
            parentObj = mc.listRelatives(obj[i], p=True)

            if rotation == 'On':
                mc.delete(mc.pointConstraint(obj[i], grp, mo=False))
                mc.delete(mc.orientConstraint(obj[i], grp, mo=False))

                if parentObj is None:
                    mc.parent(obj[i], grp)
                else:
                    mc.parent(grp, parentObj[0])
                    mc.parent(obj[i], grp)

                mc.select(grp)
                return grp

            elif rotation == 'Off':
                mc.pointConstraint(obj[i], grp, mo=False)
                mc.delete('%s_pointConstraint1' % grp)

                if parentObj is None:
                    mc.parent(obj[i], grp)
                else:
                    mc.parent(grp, parentObj[0])
                    mc.parent(obj[i], grp)

                mc.select(grp)
                return grp

    def getSpace(self, obj, type):
        if type == 'both':
            objT = mc.xform(obj, q=1, t=1, ws=1)
            objR = mc.xform(obj, q=1, ro=1, ws=1)
            aboutObjDate = objT + objR
            return aboutObjDate
        elif type == 'translate':
            objT = mc.xform(obj, q=1, t=1, ws=1)
            return objT
        elif type == 'rotate':
            objR = mc.xform(obj, q=1, ro=1, ws=1)
            return objR

    def delUselessNode(self):
        try:
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
        except:
            pass

        ani = mc.ls(type="animCurve")
        if len(ani) == 0:
            pass
        else:
            pointsNum = len(ani) - 1
            gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            mc.progressBar(gMainProgressBar,
                           edit=True,
                           beginProgress=True,
                           isInterruptable=True,
                           status='delete useless nodes ......',
                           maxValue=pointsNum)
            for x in ani:
                if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
                    break
                if mc.objExists(x):
                    hasInput = mc.listConnections(x, s=True, d=False, scn=True)
                    hasOutput = mc.listConnections(x, s=False, d=True, scn=True)
                    if 'hyperLayout' in str(hasOutput) and len(hasOutput) == 1:
                        hasOutput = None

                    isLocked = mc.lockNode(x, q=1, l=1)[0]
                    if isLocked:
                        mc.lockNode(x, l=False)
                    if not hasInput or not hasOutput:
                        if "scalePower" not in str(x):
                            mc.delete(x)
                            print("Delete useless node %s." % x, True)

                mc.progressBar(gMainProgressBar, edit=True, step=1)
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    def renameSdkCurve(self):
        animCList = mc.ls(type='animCurve')
        for x in animCList:
            driverAttr = self.removeEXnodes(x, 'input', 'sfd')
            drivenAttr = self.removeEXnodes(x, 'output', 'dfs')[0]
            mc.rename(x, '%s_TO_%s_animCurve' % (driverAttr.replace('.', '_'), drivenAttr.replace('.', '_')))

    def getFinalConnection(self, obj, direction):
        objList = [obj]
        connectObj = ''
        while objList:
            connectObj = objList
            if direction == 'front':
                objList = mc.listConnections(objList, s=1, d=0)
            elif direction == 'back':
                objList = mc.listConnections(objList, s=0, d=1)
            if objList is not None:
                objList = sorted(set(objList), key=objList.index)
        return connectObj

    def getAnimCurve(self, driverAttr, setdrivenAttr=None):
        setdrivenCrv = []
        animCList = mc.listConnections(driverAttr, type='animCurve', s=False, d=True, scn=True)

        if animCList is None:
            return None
        elif animCList is not None and setdrivenAttr is None:
            return animCList
        elif animCList is not None and setdrivenAttr is not None:
            for x in animCList:
                try:
                    drivenAttr = self.removeEXnodes(x, 'output', 'dfs')[0]
                    if drivenAttr == setdrivenAttr:
                        setdrivenCrv.append(x)
                except:
                    mc.error('maybe this sdk anim curve ({0}) has only one connection'.format(x))
            return setdrivenCrv

    def getSdkData(self, animC, setDrivenAttr=None):
        key = []
        row = []
        animCType = 'sdk'
        driverAttr = self.removeEXnodes(animC, 'input', 'sfd')
        drivenAttrs = self.removeEXnodes(animC, 'output', 'dfs')
        if setDrivenAttr:
            drivenAttr = setDrivenAttr
        else:
            drivenAttr = drivenAttrs[0]

        if mc.nodeType(drivenAttr.split('.')[0]) == 'multiplyDivide':
            return 'Pass Line : ' + drivenAttr
        else:
            #---------------------------------------------------
            times = mc.keyframe(animC, q=1, fc=1)
            values = mc.keyframe(animC, q=1, vc=1)
            #---------------------------------------------------
            itts = mc.keyTangent(animC, q=1, itt=1)
            otts = mc.keyTangent(animC, q=1, ott=1)
            ias = mc.keyTangent(animC, q=1, ia=1)
            oas = mc.keyTangent(animC, q=1, oa=1)
            weighted = mc.keyTangent(animC, q=1, wt=1)[0]
            pre = mc.getAttr(animC + '.preInfinity')
            post = mc.getAttr(animC + '.postInfinity')

            weighted = 1 if weighted == True else 0

            if times is not None:
                for num in range(len(times)):
                    row.append(times[num])
                    row.append(values[num])
                    row.append(itts[num])
                    row.append(otts[num])
                    key.append(row)
                    row = []

                return animCType + '|' + animC + '|' + str(driverAttr) + '|' + str(drivenAttr) + '|' + str(
                    weighted) + '|' + str(pre) + '|' + str(post) + '|' + str(ias) + '|' + str(oas) + '|' + str(key)
            else:
                return 'Pass Line : ' + drivenAttr

    def removeUnicode(self, strs):
        frontIndex = strs.index('u\'') + 2
        backIndex = strs.rfind('\'')
        return strs[frontIndex:backIndex]

    def checkSymObj(self, orgObj=None, searchFor='L_', replaceWith='R_'):
        #------------------------------
        if orgObj is None:
            orgObj = []

        symObj = []
        keyword = [searchFor]
        #------------------------------
        if not orgObj:
            selobjs = mc.ls(sl=1)
        else:
            selobjs = orgObj

        for x in selobjs:
            for n in keyword:
                if n not in x:
                    symObj.append(x)
                else:
                    theOtherSideobj = x.replace(searchFor, replaceWith)
                    if mc.objExists(theOtherSideobj):
                        symObj.append(theOtherSideobj)
                    else:
                        mc.warning('can not find the sysmmetry : %s' % theOtherSideobj)

            symObj = sorted(set(symObj), key=symObj.index)

        if len(symObj) == 1:
            return symObj[0]
        else:
            return symObj

    def checkSymAxis(self, orgobj, symobj):
        symAxis = []

        orghelploc = mc.spaceLocator(p=(0, 0, 0), name=str(orgobj) + '_help_loc')[0]
        symhelploc = mc.spaceLocator(p=(0, 0, 0), name=str(symobj) + '_help_loc')[0]

        self.fromAtoB(orghelploc, orgobj, 1)
        self.fromAtoB(symhelploc, symobj, 1)

        orghelplocGrp = self.makeObjZero('zero', 'On', orghelploc)
        symhelplocGrp = self.makeObjZero('zero', 'On', symhelploc)

        zeroValue = ['.tx', '.ty', '.tz']
        for x in zeroValue:
            mc.setAttr(orghelplocGrp + x, 0)
            mc.setAttr(symhelplocGrp + x, 0)

        axisKey = ['X', 'Y', 'Z', 'X-', 'Y-', 'Z-']
        orgaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        symaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

        orghelplocOrgTx = mc.getAttr(orghelploc + '.tx')
        orghelplocOrgTy = mc.getAttr(orghelploc + '.ty')
        orghelplocOrgTz = mc.getAttr(orghelploc + '.tz')

        symhelplocOrgTx = mc.getAttr(symhelploc + '.tx')
        symhelplocOrgTy = mc.getAttr(symhelploc + '.ty')
        symhelplocOrgTz = mc.getAttr(symhelploc + '.tz')

        #==========
        # CHECKING......
        #==========
        i = 0
        while i < len(orgaxisValue):
            j = 0

            mc.setAttr(orghelploc + '.tx', orghelplocOrgTx + orgaxisValue[i][0])
            mc.setAttr(orghelploc + '.ty', orghelplocOrgTy + orgaxisValue[i][1])
            mc.setAttr(orghelploc + '.tz', orghelplocOrgTz + orgaxisValue[i][2])

            orgcurrentPos = self.getSpace(orghelploc, type='translate')
            orgcurrentPos[0] = round(orgcurrentPos[0], 1)
            orgcurrentPos[1] = round(orgcurrentPos[1], 1)
            orgcurrentPos[2] = round(orgcurrentPos[2], 1)

            mc.setAttr(orghelploc + '.tx', orghelplocOrgTx)
            mc.setAttr(orghelploc + '.ty', orghelplocOrgTy)
            mc.setAttr(orghelploc + '.tz', orghelplocOrgTz)

            while j < len(symaxisValue):

                mc.setAttr(symhelploc + '.tx', symhelplocOrgTx + symaxisValue[j][0])
                mc.setAttr(symhelploc + '.ty', symhelplocOrgTy + symaxisValue[j][1])
                mc.setAttr(symhelploc + '.tz', symhelplocOrgTz + symaxisValue[j][2])

                symcurrentPos = self.getSpace(symhelploc, type='translate')
                symcurrentPos[0] = round(symcurrentPos[0], 1)
                symcurrentPos[1] = round(symcurrentPos[1], 1)
                symcurrentPos[2] = round(symcurrentPos[2], 1)

                mc.setAttr(symhelploc + '.tx', symhelplocOrgTx)
                mc.setAttr(symhelploc + '.ty', symhelplocOrgTy)
                mc.setAttr(symhelploc + '.tz', symhelplocOrgTz)

                if orgcurrentPos[0] == symcurrentPos[0] * -1 and orgcurrentPos[1] == symcurrentPos[1] and orgcurrentPos[
                    2] == symcurrentPos[2]:

                    symAxis.append(orgobj + '.translate' + axisKey[i])
                    symAxis.append(symobj + '.translate' + axisKey[j])
                    #
                    # if '-' in axisKey[j]:
                    #     symAxis.append(orgobj + '.rotate' + axisKey[i])
                    #     symAxis.append(symobj + '.rotate' + axisKey[j][:-1])
                    # elif '-' not in axisKey[j]:
                    #     symAxis.append(orgobj + '.rotate' + axisKey[i])
                    #     symAxis.append(symobj + '.rotate' + axisKey[j] + '-')

                j += 1
            i += 1

        mc.delete(orghelplocGrp , symhelplocGrp)
        axisNote = {}
        for i in range(0, len(symAxis), 2):
            axisNote[symAxis[i]] = symAxis[i + 1]
        return axisNote

    def checkSymAttrIfMirror(self, baseDriverAttr, baseDrivenAttr):
        PrefixKey = ['L_', 'lf_', '_lt_', 'left_', 'Left_', 'R_', 'rt_', '_rt_', 'right_', 'Right_']
        keyNum = len(PrefixKey)
        symAttr = []
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #check driver attribute
        driverAttr = ''
        drivenAttr = ''
        i = 0
        while i < keyNum:
            if PrefixKey[i] in baseDriverAttr:
                driverAttr = (self.checkSymObj(orgObj=[baseDriverAttr], searchFor=PrefixKey[i],
                                               replaceWith=PrefixKey[(i + keyNum // 2) % keyNum]))

                if len(driverAttr) == 0:
                    driverAttr = baseDriverAttr
                    break

                elif len(driverAttr) != 0:
                    symDriver = driverAttr.split('.')[0]
                    if 'translate' in baseDriverAttr or 'rotate' in baseDriverAttr and 'order' not in baseDriverAttr and 'Order' not in baseDriverAttr:
                        mirrorAxis = self.checkSymAxis(baseDriverAttr.split('.')[0], symDriver)
                        driverAttr = mirrorAxis[baseDriverAttr]
                break
            else:
                i = i + 1
                if i == keyNum:
                    driverAttr = baseDriverAttr
                    break
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #check driven attribute
        j = 0
        while j < keyNum:
            if PrefixKey[j] in baseDrivenAttr:
                drivenAttr = (self.checkSymObj(orgObj=[baseDrivenAttr], searchFor=PrefixKey[j],
                                               replaceWith=PrefixKey[(j + keyNum // 2) % keyNum]))

                if len(drivenAttr) == 0:
                    drivenAttr = baseDrivenAttr
                    driverAttr = baseDriverAttr
                    break

                elif len(drivenAttr) != 0:
                    symDriven = drivenAttr.split('.')[0]
                    if 'translate' in baseDrivenAttr or 'rotate' in baseDrivenAttr and 'order' not in baseDrivenAttr and 'Order' not in baseDrivenAttr:
                        mirrorAxis = self.checkSymAxis(baseDrivenAttr.split('.')[0], symDriven)
                        drivenAttr = mirrorAxis[baseDrivenAttr]
                break
            else:
                j = j + 1
                if j == keyNum:
                    if 'translate' in baseDrivenAttr or 'rotate' in baseDrivenAttr and 'order' not in baseDrivenAttr and 'Order' not in baseDrivenAttr:
                        mirrorAxis = self.checkSymAxis(baseDrivenAttr.split('.')[0], baseDrivenAttr.split('.')[0])
                        print(mirrorAxis)
                        print(baseDrivenAttr)
                        drivenAttr = mirrorAxis[baseDrivenAttr]
                    else:
                        drivenAttr = baseDrivenAttr
                    break

        symAttr.append(driverAttr)
        symAttr.append(drivenAttr)
        return symAttr

    def generateSDK(self, sdkData, mirror=False, sc=1):
        splitList = sdkData.split('|')
        driverAttr = ''
        drivenAttr = ''
        if 'sdk' in splitList[0]:
            if not mirror:
                driverAttr = splitList[2]
                drivenAttr = splitList[3]
            elif mirror:
                checkResult = self.checkSymAttrIfMirror(splitList[2], splitList[3])
                driverAttr = checkResult[0]
                drivenAttr = checkResult[1]
            valueScale = sc if 'translate' in drivenAttr else 1

            #----------------------------------------------------------->>
            #Began to extract single values ......
            # weighted = splitList[4]
            pre = splitList[5]
            post = splitList[6]
            ia = splitList[7][1:-1].split(',')
            oa = splitList[8][1:-1].split(',')
            keyframeData = splitList[9][2:-2].split('], [')

            # --------------------------------------------------------------------------------------------------------------------------------------------
            # Began to generate the new SDK ......
            # Edit scale value.
            for i in range(len(keyframeData)):

                frameData = keyframeData[i].split(', ')
                dv = frameData[0]
                v = frameData[1]

                if not mirror:
                    mc.setDrivenKeyframe(drivenAttr.split('.')[0], at=drivenAttr.split('.')[1], cd=driverAttr,
                                         dv=float(dv), v=float(v) * valueScale)

                elif mirror:
                    # value data set.
                    if '-' in driverAttr and '-' not in drivenAttr:
                        mc.setDrivenKeyframe(drivenAttr.split('.')[0], at=drivenAttr.split('.')[1], cd=driverAttr[:-1],
                                             dv=float(dv) * -1, v=float(v) * valueScale)
                    elif '-' not in driverAttr and '-' in drivenAttr:
                        mc.setDrivenKeyframe(drivenAttr.split('.')[0], at=drivenAttr.split('.')[1][:-1], cd=driverAttr,
                                             dv=float(dv), v=float(v) * (-1) * valueScale)
                    elif '-' in driverAttr and '-' in drivenAttr:
                        mc.setDrivenKeyframe(drivenAttr.split('.')[0], at=drivenAttr.split('.')[1][:-1],
                                             cd=driverAttr[:-1], dv=float(dv) * -1, v=float(v) * (-1) * valueScale)
                    elif '-' not in driverAttr and '-' not in drivenAttr:
                        mc.setDrivenKeyframe(drivenAttr.split('.')[0], at=drivenAttr.split('.')[1], cd=driverAttr,
                                             dv=float(dv), v=float(v) * valueScale)

            # --------------------------------------------------------------------------------------------------------------------------------------------
            # itt ott set
            for i in range(len(keyframeData)):
                frameData = keyframeData[i].split(', ')
                itt = eval(frameData[2])
                ott = eval(frameData[3])

                if '-' in drivenAttr:
                    realdriverAttr = driverAttr[:-1] if '-' in driverAttr else driverAttr
                    animCurrentCrv = self.getAnimCurve(realdriverAttr, drivenAttr[:-1])[0]
                    mel.eval('keyTangent -index %s -e -itt %s -ott %s %s' % (i, itt, ott, animCurrentCrv))
                    mel.eval('keyTangent -index %s -e -ia %s -oa %s %s' % (
                    i, (float(ia[i]) * -1), (float(oa[i]) * -1), animCurrentCrv))
                    mc.setAttr(animCurrentCrv + '.preInfinity', float(pre))
                    mc.setAttr(animCurrentCrv + '.postInfinity', float(post))

                elif '-' not in drivenAttr:
                    realdriverAttr = driverAttr[:-1] if '-' in driverAttr else driverAttr
                    animCurrentCrv = self.getAnimCurve(realdriverAttr, drivenAttr)[0]
                    mel.eval('keyTangent -index %s -e -itt %s -ott %s %s' % (i, itt, ott, animCurrentCrv))
                    mel.eval(
                        'keyTangent -index %s -e -ia %s -oa %s %s' % (i, float(ia[i]), float(oa[i]), animCurrentCrv))
                    mc.setAttr(animCurrentCrv + '.preInfinity', float(pre))
                    mc.setAttr(animCurrentCrv + '.postInfinity', float(post))

        else:
            mc.error('Data type is wrong')

    def getWeightName(self, blendShapeNode):
        aliases = mc.aliasAttr(blendShapeNode, q=True)
        Target = []
        for i in range(int(len(aliases) / 2)):
            Target.append(aliases[i * 2])
        Target = sorted(Target)
        return Target

    def checkUsedSdkAttr(self, obj, type='driver', longName=True, driverAttr=None):
        usedSDKAttr = []
        Attrlist = []
        if mc.nodeType(obj) != 'blendShape':
            Attrlist = mc.listAttr(obj, l=1, v=1, k=1, c=1, u=1, s=1)
        elif mc.nodeType(obj) == 'blendShape':
            Attrlist = self.getWeightName(obj)

        for x in Attrlist:
            if type == 'driver':
                conobj = mc.listConnections('%s.%s' % (obj, x), type='animCurve', s=False, d=True, scn=True)
                if conobj is None:
                    pass
                else:
                    if longName:
                        usedSDKAttr.append(obj + '.' + x)
                    elif not longName:
                        usedSDKAttr.append(x)

            elif type == 'driven':
                conobj = mc.listConnections('%s.%s' % (obj, x), s=True, d=False, scn=True)
                if conobj is None:
                    pass
                elif 'animCurve' in mc.objectType(conobj) or mc.objectType(conobj) == 'blendWeighted':
                    if driverAttr is None:
                        if longName:
                            usedSDKAttr.append(obj + '.' + x)
                        elif not longName:
                            usedSDKAttr.append(x)
                    else:
                        animC = self.getAnimCurve(driverAttr, obj + '.' + x)
                        if len(animC) != 0:
                            if longName:
                                usedSDKAttr.append(obj + '.' + x)
                            elif not longName:
                                usedSDKAttr.append(x)
                        else:
                            pass

        return usedSDKAttr

    def mirrorSDK(self, driver=None, driven=None):
        # used return.
        if driven is None:
            driven = []
        if driver is None:
            driver = []

        driverAttrList = []
        drivenAttrList = []
        animCList = []

        # get used driver/driven attributes.
        for x in driver:
            if '.' in x:
                driverAttrList.append(x)
            else:
                driverSdkAttrList = self.checkUsedSdkAttr(x, type='driver')
                for j in driverSdkAttrList:
                    if 'R_' not in j and 'right_' not in j and 'Right_' not in j:
                        driverAttrList.append(j)

        if len(driven) == 0:
            pass
        else:
            for x in driven:
                if '.' in x:
                    drivenAttrList.append(x)
                else:
                    drivenSdkAttrList = self.checkUsedSdkAttr(x, type='driven')
                    drivenSdkAttrList = sorted(drivenSdkAttrList)

                    for j in drivenSdkAttrList:
                        drivenAttrList.append(j)

        # get used driver/driven animCurves
        for x in driverAttrList:
            if len(drivenAttrList) == 0:
                animcrv = self.getAnimCurve(x)
                for j in animcrv:
                    animCList.append(j)
            else:
                i = 0
                while i < len(drivenAttrList):
                    animcrv = self.getAnimCurve(x, drivenAttrList[i])
                    if len(animcrv) != 0:
                        animCList.append(animcrv[0])
                    i += 1

        #progressWin start---------------------------------------------------->>
        pointsNum = None
        if len(animCList) > 1:
            pointsNum = len(animCList) - 1
        elif len(animCList) == 1:
            pointsNum = len(animCList)

        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        mc.progressBar(gMainProgressBar,
                       edit=True,
                       beginProgress=True,
                       isInterruptable=True,
                       status='mirror set driven key ......',
                       maxValue=pointsNum)

        #progressWin end---------------------------------------------------->>

        if not animCList:
            pass
        else:
            for j in animCList:
                if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
                    break
                sdkData = self.getSdkData(j)
                if 'Pass Line' not in sdkData:
                    self.generateSDK(sdkData, mirror=True)
                    mc.progressBar(gMainProgressBar, edit=True, step=1)
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)

        print('Mirror is successful !')

    def addDrivens(self):
        pass

    def removeDrivens(self):
        pass

    def updateSdk(self, updateSelected=True):
        pass

    def exportSdkData(self, driver=None, driven=None):
        if driven is None:
            driven = []
        if driver is None:
            driver = []

        driverAttrList = []
        drivenAttrList = []
        animCList = []

        # get used driver/driven attributes.
        for x in driver:
            driverSdkAttrList = self.checkUsedSdkAttr(x, type='driver')
            for j in driverSdkAttrList:
                driverAttrList.append(j)
        if len(driven) == 0:
            pass
        else:
            for x in driven:
                drivenSdkAttrList = self.checkUsedSdkAttr(x, type='driven')
                for j in drivenSdkAttrList:
                    drivenAttrList.append(j)

        # get used driver/driven animCurves
        for x in driverAttrList:
            if len(drivenAttrList) == 0:
                animcrv = self.getAnimCurve(x)
                for j in animcrv:
                    animCList.append(j)
            else:
                i = 0
                while i < len(drivenAttrList):
                    animcrv = self.getAnimCurve(x, drivenAttrList[i])
                    if len(animcrv) != 0:
                        animCList.append(animcrv[0])
                    i += 1
        #End---This is a duplicated code.

        filePath = mc.fileDialog2(fm=0, okc='export', fileFilter="*.sdk")
        fp = ''
        if filePath is not None:
            fileName = filePath[0]
            fp = open(fileName, 'w')

        #progressWin start---------------------------------------------------->>
        pointsNum = len(driverAttrList)
        if pointsNum == 1:
            pass
        else:
            pointsNum = pointsNum - 1

        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        mc.progressBar(gMainProgressBar,
                       edit=True,
                       beginProgress=True,
                       isInterruptable=True,
                       status='export set driven key ......',
                       maxValue=pointsNum)

        #progressWin end---------------------------------------------------->>
        if not animCList:
            fp.write('There is nothing sdk data find , please check you files.')
        else:
            for j in animCList:
                if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
                    break
                sdkData = self.getSdkData(j)
                fp.write(sdkData + '\n')
                mc.progressBar(gMainProgressBar, edit=True, step=1)

        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        print('SDK data Export is Ok !')
        fp.close()

    def exportSdkFromDrivenObjs(self):
        drivenObjs = mc.ls(sl=1)
        if drivenObjs is None:
            return

        animCList = []
        for driven in drivenObjs:
            drivenAttrList = self.checkUsedSdkAttr(driven, type='driven')
            for attr in drivenAttrList:
                blendWeightedNode = mc.listConnections(attr, type='blendWeighted', s=True, d=False, scn=True)
                if blendWeightedNode:
                    bl_animCs = mc.listConnections('{0}.input'.format(blendWeightedNode[0]), type='animCurve', s=True,
                                                   d=False, scn=True)
                    for bl_animC in bl_animCs:
                        animCList.append(bl_animC)
                else:
                    animC = mc.listConnections(attr, type='animCurve', s=True, d=False, scn=True)
                    animCList.append(animC[0])

        filePath = mc.fileDialog2(fm=0, okc='export', fileFilter="*.sdk")
        fp = ''
        if filePath is not None:
            fileName = filePath[0]
            fp = open(fileName, 'w')

        if not animCList:
            fp.write('There is nothing sdk data find , please check you files.')
        else:
            for animC in animCList:
                sdkData = self.getSdkData(animC)
                fp.write(sdkData + '\n')

        print('SDK data Export is Ok !')
        fp.close()

    def exportSdkFromDrivenAttrs(self):
        driven = mc.ls(sl=1)[0]
        sel_attrs = aboutName.getSelectedAttrs()
        if sel_attrs is None:
            return

        animCList = []
        bsAttrs = []
        drivenAttrList = self.checkUsedSdkAttr(driven, type='driven')

        for drivenAttr in drivenAttrList:
            for sel_attr in sel_attrs:
                if sel_attr in drivenAttr:
                    aimAttr = '{0}.{1}'.format(driven, sel_attr)
                    bsAttrs.append(aimAttr)
                    blendWeightedNode = mc.listConnections(aimAttr, type='blendWeighted', s=True, d=False, scn=True)

                    if blendWeightedNode:
                        bl_animCs = mc.listConnections('{0}.input'.format(blendWeightedNode[0]), type='animCurve',
                                                       s=True, d=False, scn=True)
                        for bl_animC in bl_animCs:
                            animCList.append(bl_animC)
                    else:
                        animC = mc.listConnections(aimAttr, type='animCurve', s=True, d=False, scn=True)
                        animCList.append(animC[0])

        filePath = mc.fileDialog2(fm=0, okc='export', fileFilter="*.sdk")
        fp = ''
        if filePath is not None:
            fileName = filePath[0]
            fp = open(fileName, 'w')

        if not animCList:
            fp.write('There is nothing sdk data find , please check you files.')
        else:
            for i, animC in enumerate(animCList):
                if mc.nodeType(driven) == 'blendShape':
                    sdkData = self.getSdkData(animC, bsAttrs[i])
                else:
                    sdkData = self.getSdkData(animC)
                fp.write(sdkData + '\n')

        print('SDK data Export is Ok !')
        fp.close()

    def importSdkData(self, animCvalueScale=1, filePath=None):
        fp = ''
        if filePath is None:
            filePath = mc.fileDialog2(fm=1, okc='import', fileFilter="*.sdk")
            if filePath is not None:
                fileName = filePath[0]
                fp = open(fileName, 'r')
        else:
            filePath = filePath
            if filePath is not None:
                fileName = filePath
                fp = open(fileName, 'r')

        readlines = fp.readlines()

        #progressWin start---------------------------------------------------->>
        pointsNum = len(readlines)
        if pointsNum == 1:
            pass
        else:
            pointsNum = pointsNum - 1

        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        mc.progressBar(gMainProgressBar,
                       edit=True,
                       beginProgress=True,
                       isInterruptable=True,
                       status='import set driven key ...',
                       maxValue=pointsNum)

        #progressWin end---------------------------------------------------->>
        for sdkdata in readlines:
            sdkdata = sdkdata.rstrip()
            if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
                break
            if 'Pass Line' not in sdkdata:
                self.generateSDK(sdkdata, mirror=False, sc=animCvalueScale)
                mc.progressBar(gMainProgressBar, edit=True, step=1)

        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        sys.stdout.write('SDK data Import is Ok !')
        fp.close()

    def load(self):
        try:
            driverBridge = mc.textField(self.drvField, q=True, text=True)
            selectDriver = mc.ls(sl=True)
            if driverBridge != '' and selectDriver != []:
                driverBridge = selectDriver[0]
            #-----------------------------------------------------------------------------------------------------------------
            driver = ''
            if driverBridge != '' and driverBridge != 'Please select one driver.':
                driver = driverBridge
            else:
                driverBridge = mc.ls(sl=True)
                if not driverBridge:
                    mc.error('Please select one driver.')
                else:
                    driver = driverBridge[0]

            mc.textField(self.drvField, e=True, text='%s' % driver, bgc=(0.273163, 0.607843, 0.119185))
            #-----------------------------------------------------------------------------------------------------------------

            #----------------------------------------------------CHECKBOX------------------------------------------------------------
            attrList = ''
            #check used attr display
            if mc.menuItem(self.displayTypeUsed, q=True, cb=True):
                attrList = self.checkUsedSdkAttr(driver, type='driver', longName=False)
            elif not mc.menuItem(self.displayTypeUsed, q=True, cb=True):
                attrList = mc.listAttr(driver, v=True, k=True, u=True)

            #check left or right display
            if mc.menuItem(self.displayTypeLR, q=True, cb=True):
                rmattrList = []
                PrefixKey = ['R_', 'right_', 'Right_']

                for attr in attrList:
                    keyNum = len(PrefixKey)
                    i = 0
                    while i < keyNum:
                        if PrefixKey[i] in attr:
                            rmattrList.append(attr)
                            break
                        else:
                            i = i + 1
                            if i == keyNum:
                                break
                        break

                for rm in rmattrList:
                    attrList.remove(rm)
            #----------------------------------------------------------------------------------------------------------------
            #edit ui
            mc.textScrollList(self.driverScroll, e=True, ra=True, en=True, append=attrList)
            mc.textScrollList(self.drivenScroll, e=True, ra=True, en=True)
            mc.iconTextButton(self.mirrorButton, e=True, en=True)

            if len(attrList) == 0:
                mc.textField(self.drvField, e=True, text='%s' % 'You select driver has no correct attribute.',
                             bgc=(0.490196, 0.201845, 0.201845))
                mc.textScrollList(self.driverScroll, e=True, ra=True, en=False, append=[''])
                mc.textScrollList(self.drivenScroll, e=True, ra=True, en=False, append=[''])
                mc.iconTextButton(self.updataButton, e=True, en=False)
                mc.iconTextButton(self.mirrorButton, e=True, en=False)
        except:
            mc.textField(self.drvField, e=True, text='Please select one driver.', bgc=(0.490196, 0.201845, 0.201845))
            mc.textScrollList(self.driverScroll, e=True, ra=True, en=False, append=[''])
            print(traceback.print_exc())

    def listDrivenForSelectItem(self, supportUI=True):
        driverAttr = self.getDriverAttrFromUI(type='one')
        animCList = self.getAnimCurve(driverAttr)
        drivenList = []

        if animCList is not None:
            for x in animCList:
                drivenAttr = self.removeEXnodes(x, 'output', 'dfs')[0]
                driven = drivenAttr.split('.')[0]

                if mc.nodeType(driven) == 'multiplyDivide':
                    pass
                else:
                    drivenList.append(driven)
        else:
            drivenList = []

        drivenList = sorted(set(drivenList), key=drivenList.index)  #remove repeat.

        if supportUI:
            mc.select(cl=True)
            if drivenList:
                drivenList = sorted(set(drivenList), key=drivenList.index)  #remove repeat.
                mc.textScrollList(self.drivenScroll, e=True, ra=True, append=sorted(drivenList))
            else:
                mc.textScrollList(self.drivenScroll, e=True, ra=True, append=['Not drive any object'])
        #---------------------------------------------------------------------------------------------
        return drivenList

    def selectScrollList(self, ScrollList):
        #support UI
        selected = mc.textScrollList(ScrollList, q=True, selectItem=True)
        mc.select(selected)

    def getSelectScrollList(self, ScrollList):
        selected = mc.textScrollList(ScrollList, q=True, selectItem=True)
        result = []
        if selected is not None:
            for x in selected:
                if '+' in x or '*' in x:
                    result.append(x[:-1])
                else:
                    result.append(x)
            return result
        else:
            return None

    def mirrorSdkForSelectItem(self, mirrorSelected=False):

        driverAttr = self.getDriverAttrFromUI(type='one')

        drivenList = mc.textScrollList(self.drivenScroll, q=True, selectItem=True)

        if not mirrorSelected:
            if driverAttr is not None:
                self.mirrorSDK(driver=[driverAttr])
            else:
                mc.warning('You should select one driver attribute')

        elif mirrorSelected:
            if driverAttr is not None and drivenList is not None:
                self.mirrorSDK(driver=[driverAttr], driven=drivenList)
            else:
                mc.warning('You should select some drivens')

    def listDrivenAttrForSelectItem(self):

        driverAttr = self.getDriverAttrFromUI(type='one')
        drivens = self.getSelectScrollList(self.drivenScroll)
        mc.select(drivens)
        drivenAttrs = []

        for i, driven in enumerate(drivens):
            attrs = self.checkUsedSdkAttr(driven, type='driven', longName=False, driverAttr=driverAttr)
            if i == 0:
                drivenAttrs = attrs
            else:
                drivenAttrs = list(set(attrs) & set(drivenAttrs))
        #result
        mc.textScrollList(self.drivenAttrScroll, e=True, append=sorted(drivenAttrs), ra=1)

    def selectAnimCForSelectItem(self):

        animCList = []
        driverAttr = self.getDriverAttrFromUI(type='one')
        drivens = self.getSelectScrollList(self.drivenScroll)
        selectDrivenAttrs = self.getSelectScrollList(self.drivenAttrScroll)

        for x in selectDrivenAttrs:
            for j in drivens:
                drivenAttr = j + '.' + x
                animC = self.getAnimCurve(driverAttr, setdrivenAttr=drivenAttr)
                if len(animC) != 0:
                    animCList.append(animC[0])

        if len(animCList) != 0:
            mc.select(animCList)

    def getDriverAttrFromUI(self, type='one'):

        driverAttrList = []
        driver = mc.textField(self.drvField, q=True, text=True)
        if type == 'one':
            attr = self.getSelectScrollList(self.driverScroll)[0]
            return driver + '.' + attr
        elif type == 'more':
            attr = self.getSelectScrollList(self.driverScroll)
            for x in attr:
                driverAttrList.append(driver + '.' + x)
                return driverAttrList

    def selectDriverBridge(self):
        bridge = mc.textField(self.drvField, q=True, text=True)
        mc.select(bridge)
