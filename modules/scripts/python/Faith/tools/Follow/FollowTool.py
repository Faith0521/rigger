# Embedded file name: E:/JunCmds/tool/Follow\FollowTool.py
"""
import sys
sys.path.insert(0,r'R:\\JueJi\\JueJiTool')
import FollowTool as FollowTool
reload(FollowTool)
ft = FollowTool.followTool()
#---------------------------------------------------------
lockObj = 'pSphere1'#\xe8\xa2\xab\xe7\xba\xa6\xe6\x9d\x9f\xe7\x89\xa9\xe4\xbd\x93
addAttrObj = 'pSphere1'#\xe6\xb7\xbb\xe5\x8a\xa0\xe8\xb7\x9f\xe9\x9a\x8f\xe5\x88\x87\xe6\x8d\xa2\xe5\xb1\x9e\xe6\x80\xa7\xe7\x89\xa9\xe4\xbd\x93\xef\xbc\x8c\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\x88\x87\xe6\x8d\xa2\xe5\xb1\x9e\xe6\x80\xa7\xe5\xb0\xb1\xe4\xb8\xba\xe7\xa9\xba''
attr = 'follow'#\xe8\xb7\x9f\xe9\x9a\x8f\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\x88\x87\xe6\x8d\xa2\xe5\xb1\x9e\xe6\x80\xa7\xe5\xb0\xb1\xe4\xb8\xba\xe7\xa9\xba''
followEnumAttrs = ['body','world']#\xe8\xb7\x9f\xe9\x9a\x8f\xe5\xb1\x9e\xe6\x80\xa7\xe4\xb8\xad\xe7\x9a\x84\xe6\x9e\x9a\xe4\xb8\xbe\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\x88\x87\xe6\x8d\xa2\xe5\xb1\x9e\xe6\x80\xa7\xe5\xb0\xb1\xe4\xb8\xba\xe7\xa9\xba''
followObjs = ['locator1','locator2']#\xe7\xba\xa6\xe6\x9d\x9f\xe7\x89\xa9\xe4\xbd\x93
constrainType = ['orient','point']#\xe7\xba\xa6\xe6\x9d\x9f\xe6\x96\xb9\xe5\xbc\x8f ['orient','point','parent']
followObjBridgeZeros = ft.follow(lockObj,addAttrObj,attr,followEnumAttrs,followObjs,constrainType)
#cmds.parent(followObjBridgeZeros,'all_ctrl')
"""
import maya.cmds as cmds
import maya.mel as mel
import os

class followTool:

    def __init__(self):
        self.winName = 'followToolWin'

    def win(self):
        if cmds.window(self.winName, ex=True):
            cmds.deleteUI(self.winName, window=True)
        cmds.window(self.winName, t='FollowTool  v1.0', w=350, h=175)
        self.form = cmds.formLayout()
        row = cmds.rowColumnLayout(nc=2, adjustableColumn=2, cat=[1, 'right', 5], ro=[(1, 'both', 2),
         (2, 'both', 2),
         (3, 'both', 2),
         (4, 'both', 2)])
        self.lockObjBN = cmds.iconTextButton(style='textOnly', w=100, bgc=[0.5, 0.4, 0.33], label='L o c k - O b j', c=lambda *args: self.uiLoadCmd(self.lockObjTF, 1))
        self.lockObjTF = cmds.textField('lockObjText', w=245, ed=False)
        self.followObjsBN = cmds.iconTextButton(style='textOnly', w=100, bgc=[0.5, 0.4, 0.33], label='F o l l o w - O b j s', c=lambda *args: self.uiLoadCmd([self.followObjsTF, self.followEnumAttrsTF], 'all'))
        self.followObjsTF = cmds.textField('followObjsText', w=245, ed=True)
        self.addAttrObjBN = cmds.iconTextButton(style='textOnly', w=100, bgc=[0.5, 0.4, 0.33], label='A d d A t t r - O b j', c=lambda *args: self.uiLoadCmd(self.addAttrObjTF, 1))
        self.addAttrObjTF = cmds.textField('addAttrObjText', w=245, ed=False)
        self.followEnumAttrsBN = cmds.iconTextButton(style='textOnly', w=100, bgc=[0.5, 0.4, 0.33], label='E n u m A t t r s', c=lambda *args: self.uiLoadCmd(self.followEnumAttrsTF, 'all'))
        self.followEnumAttrsTF = cmds.textField('followEnumAttrsText', w=245, ed=True)
        cmds.setParent('..')
        column = cmds.columnLayout(adj=True)
        cmds.rowLayout(nc=4, cat=[1, 'left', 25])
        self.typeRID = cmds.radioCollection('typeRID')
        self.pointTypeRID = cmds.radioButton('point', l='point', w=70)
        self.orientTypeRID = cmds.radioButton('orient', l='Orient', w=70)
        self.ParentTypeRID = cmds.radioButton('parent', l='Parent', w=70)
        self.point_orientTypeRID = cmds.radioButton('point_orient', l='point + orient', w=100)
        cmds.radioCollection(self.typeRID, edit=True, select=self.ParentTypeRID)
        cmds.setParent('..')
        cmds.iconTextButton(style='textOnly', h=30, bgc=[0.23, 0.33, 0.39], label='C r e a t e  F o l l o w', c=lambda *args: self.followuiRunCmd())
        cmds.rowColumnLayout(nc=2, adjustableColumn=2, cat=[1, 'right', 5], ro=[(1, 'both', 2),
         (2, 'both', 2),
         (3, 'both', 2),
         (4, 'both', 2)])
        cmds.text(u'\u8df3\u8fc7\u5c0f\u6743\u91cd', w=100)
        cmds.textField('skipLittleWeightTF', text=0.01, w=60, ed=True)
        cmds.setParent('..')
        cmds.iconTextButton(style='textOnly', h=30, bgc=[0.23, 0.33, 0.39], label=u'G e t  V t x  W e i g h t', c=lambda *args: self.getVtxWeight())
        cmds.iconTextButton(style='textOnly', h=30, bgc=[0.23, 0.33, 0.39], label=u'g e t V t x S k i n J n t C o n O b j', c=lambda *args: self.getVtxSkinJntConObjRunCmd())
        cmds.setParent('..')
        cmds.formLayout(self.form, edit=True, attachForm=[(row, 'top', 5),
         (row, 'left', 5),
         (row, 'right', 5),
         (column, 'bottom', 5),
         (column, 'right', 5),
         (column, 'left', 5)], attachControl=[(row,
          'bottom',
          5,
          column)])
        cmds.showWindow(self.winName)

    def uiLoadCmd(self, nameFileds, objNum):
        selectObj = cmds.ls(sl=True)
        if selectObj == []:
            selectObj = ['']
        if type(nameFileds) == list:
            for nameFiled in nameFileds:
                if type(objNum) == int:
                    if objNum == 1:
                        cmds.textField(nameFiled, e=True, text=str(selectObj[0]))
                    else:
                        cmds.textField(nameFiled, e=True, text=str(selectObj[:objNum]))
                elif objNum == 'all':
                    cmds.textField(nameFiled, e=True, text=str(selectObj[:]))

        else:
            nameFiled = nameFileds
            if type(objNum) == int:
                if objNum == 1:
                    cmds.textField(nameFiled, e=True, text=str(selectObj[0]))
                else:
                    cmds.textField(nameFiled, e=True, text=str(selectObj[:objNum]))
            elif objNum == 'all':
                cmds.textField(nameFiled, e=True, text=str(selectObj[:]))

    def uiGetCmd(self, nameFiled):
        data = cmds.textField(nameFiled, q=True, text=True)
        data = eval(data)
        return data

    def followuiRunCmd(self):
        lockObj = cmds.textField(self.lockObjTF, q=True, text=True)
        addAttrObj = cmds.textField(self.addAttrObjTF, q=True, text=True)
        attr = 'follow'
        followEnumAttrs = cmds.textField(self.followEnumAttrsTF, q=True, text=True)
        if followEnumAttrs == '':
            pass
        else:
            followEnumAttrs = eval(followEnumAttrs)
        followObjs = eval(cmds.textField(self.followObjsTF, q=True, text=True))
        constrainType = [cmds.radioCollection(self.typeRID, q=True, select=True)]
        if constrainType == ['point_orient']:
            constrainType = ['point', 'orient']
        print ('-----------', constrainType)
        followObjBridgeZeros = self.follow(lockObj, addAttrObj, attr, followEnumAttrs, followObjs, constrainType)

    def getVtxSkinJntConObjRunCmd(self):
        lockObj = cmds.textField(self.lockObjTF, q=True, text=True)
        addAttrObj = ''
        attr = ''
        constrainType = [cmds.radioCollection(self.typeRID, q=True, select=True)]
        if constrainType == ['point_orient']:
            constrainType = ['point', 'orient']
        print ('-----------', constrainType)
        self.vtxWeight_follow(lockObj, addAttrObj, attr, constrainType)

    def setDrivenKey(self, driver, driven, driverNums, drivenNums, itt, ott):
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

    def follow(self, lockObj, addAttrObj, attr, followEnumAttrs, followObjs, constrainType, conValues = []):
        aa = []
        if addAttrObj != '' and attr != '':
            if len(followObjs) != len(followEnumAttrs):
                cmds.error("followObj and followEnumAttrs don't match")
            aa = cmds.listAttr(addAttrObj)
        if attr in aa and aa != []:
            cmds.warning(addAttrObj + '.' + attr + ' ------is exists')
        else:
            followObjBridges = []
            driverNums = []
            drivenNums = []
            followObjBridgeZeros = []
            locksGrp = cmds.group(em=True, name=lockObj + '_followGrp')
            for i in range(len(followObjs)):
                followObj = followObjs[i]
                followObjBridge = cmds.spaceLocator(name=followObj + '_Lock_' + lockObj)[0]
                followObjBridgeZero = cmds.group(followObjBridge, name=followObjBridge + '_zero')
                cmds.delete(cmds.parentConstraint(lockObj, followObjBridgeZero, mo=0, w=1))
                cmds.parentConstraint(followObj, followObjBridgeZero, mo=1, w=1)
                followObjBridges.append(followObjBridge)
                driverNums.append(i)
                drivenNums.append(0)
                followObjBridgeZeros.append(followObjBridgeZero)
                cmds.parent(followObjBridgeZero, locksGrp)

            followcons = []
            if 'orient' in constrainType:
                print ('orient')
                followcon = cmds.orientConstraint(followObjBridges, lockObj)[0]
                cmds.setAttr(followcon + '.interpType', 2)
                followcons.append(followcon)
                if conValues != []:
                    for i in range(len(followObjBridges)):
                        followObjBridge = followObjBridges[i]
                        cmds.setAttr(followcon + '.' + followObjBridge + 'W' + str(i), conValues[i])

            if 'point' in constrainType:
                print ('point')
                followcon = cmds.pointConstraint(followObjBridges, lockObj)[0]
                followcons.append(followcon)
                if conValues != []:
                    for i in range(len(followObjBridges)):
                        followObjBridge = followObjBridges[i]
                        cmds.setAttr(followcon + '.' + followObjBridge + 'W' + str(i), conValues[i])

            if 'parent' in constrainType:
                print ('parent')
                followcon = cmds.parentConstraint(followObjBridges, lockObj, mo=1)[0]
                cmds.setAttr(followcon + '.interpType', 2)
                followcons.append(followcon)
                if conValues != []:
                    for i in range(len(followObjBridges)):
                        followObjBridge = followObjBridges[i]
                        cmds.setAttr(followcon + '.' + followObjBridge + 'W' + str(i), conValues[i])

            if len(followObjs) == 2 and addAttrObj == '' and conValues == []:
                for followcon in followcons:
                    self.setDrivenKey(followcon + '.' + followObjBridges[0] + 'W' + str(0), followcon + '.' + followObjBridges[1] + 'W' + str(1), [0, 1], [1, 0], 'linear', 'linear')
                    cmds.setAttr(followcon + '.' + followObjBridges[0] + 'W' + str(0), 0.5)
                    cmds.addAttr(followcon + '.' + followObjBridges[0] + 'W' + str(0), e=True, maxValue=1.0)

            if addAttrObj != '' and attr != '':
                followEnumAttrs1 = ''
                for i in range(len(followEnumAttrs)):
                    followEnumAttr = followEnumAttrs[i]
                    followEnumAttrs1 = followEnumAttrs1 + followEnumAttr + ':'

                cmds.addAttr(addAttrObj, ln=attr, at='enum', en=followEnumAttrs1[:-1], keyable=1)
                for followcon in followcons:
                    for x, followObjBridge in enumerate(followObjBridges):
                        drivenNums[x] = 1
                        self.setDrivenKey(addAttrObj + '.' + attr, followcon + '.' + followObjBridge + 'W' + str(x), driverNums, drivenNums, 'linear', 'linear')
                        print (addAttrObj + '.' + attr, followcon + '.' + followObjBridge + 'W' + str(x), driverNums, drivenNums)
                        drivenNums[x] = 0

            return (locksGrp, followObjBridgeZeros)

    def vtxWeight_follow(self, lockObj, addAttrObj, attr, constrainType):
        LittleWeight = float(cmds.textField('skipLittleWeightTF', q=True, text=True))
        vtxs = cmds.ls(sl=True)
        if '.vtx[' in vtxs[0] and len(vtxs) == 1:
            vtx = vtxs[0]
            WeightObj = vtx.split('.vtx[')[0]
            skin = mel.eval('findRelatedSkinCluster' + '("' + WeightObj + '")')
            skin_jntList = cmds.skinCluster(skin, q=True, inf=skin)
            followObjs = []
            conValues = []
            for skin_jnt in skin_jntList:
                jnt01weight = cmds.skinPercent(skin, vtx, t=skin_jnt, q=True)
                if jnt01weight > LittleWeight:
                    followObjs.append(skin_jnt)
                    conValues.append(jnt01weight)
                    print (skin_jnt, '---', jnt01weight)

            followEnumAttrs = followObjs
            followObjs = followObjs
            self.follow(lockObj, addAttrObj, attr, followEnumAttrs, followObjs, constrainType, conValues)
        else:
            cmds.warning('plese select one weight vtx')

    def getVtxWeight(self):
        LittleWeight = float(cmds.textField('skipLittleWeightTF', q=True, text=True))
        vtxs = cmds.ls(sl=True)
        if '.vtx[' in vtxs[0] and len(vtxs) == 1:
            vtx = vtxs[0]
            WeightObj = vtx.split('.vtx[')[0]
            skin = mel.eval('findRelatedSkinCluster' + '("' + WeightObj + '")')
            skin_jntList = cmds.skinCluster(skin, q=True, inf=skin)
            followObjs = []
            conValues = []
            for skin_jnt in skin_jntList:
                jnt01weight = cmds.skinPercent(skin, vtx, t=skin_jnt, q=True)
                if jnt01weight > LittleWeight:
                    followObjs.append(skin_jnt)
                    conValues.append(jnt01weight)
                    print (skin_jnt, '---', jnt01weight)