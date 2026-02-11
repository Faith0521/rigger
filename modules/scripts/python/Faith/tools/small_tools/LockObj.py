# Embedded file name: E:/JunCmds/tool/LockObj.py
import maya.cmds as cmds
import maya.mel as mel
import os, sys

class LockTool:

    def __init__(self):
        pass

    def win(self):
        LockUI = 'JunLockWin'
        if cmds.window(LockUI, exists=True):
            cmds.deleteUI(LockUI)
        cmds.window(LockUI, t='Jun LockWin')
        cmds.window(LockUI, e=True, w=200, h=60)
        cmds.columnLayout()
        cmds.button(l='Lock', c=lambda *args: self.constraintObj(), w=200, h=30)
        cmds.button(l='unLock', c=lambda *args: self.unLock(cmds.ls(sl=True)), w=200, h=30)
        cmds.button(l='All UnLock', c=lambda *args: self.allUnLock(), w=200, h=30)
        cmds.showWindow()

    def constraintObj(self):
        objs = cmds.ls(sl=True)
        for obj in objs:
            LockObj = obj + '_lock'
            LockObjZero = LockObj + '_zero'
            if cmds.objExists(LockObj) == False and cmds.objExists(LockObjZero) == False:
                setname = 'lockObjSet'
                cmds.select(cl=True)
                if cmds.objExists(setname) == False:
                    cmds.sets(n=setname)
                cmds.sets(obj, addElement=setname)
                cmds.spaceLocator(name=LockObj)
                cmds.setAttr(LockObj + '.visibility', 0)
                cmds.group(LockObj, name=LockObj + '_zero')
                cmds.delete(cmds.parentConstraint(obj, LockObjZero, mo=False))
                lockAttr = self.getLockAttr(obj, LockObj)
                skipTranslate = lockAttr[0]
                skipRotate = lockAttr[1]
                parnode = cmds.parentConstraint(LockObj, obj, mo=False, st=skipTranslate, sr=skipRotate, name=LockObj + '_lock_' + obj + '_parcon')[0]
                print (parnode)
            else:
                cmds.warning(LockObj + '------is exists')

        cmds.select(objs)

    def unLock(self, objs):
        for obj in objs:
            LockObj = obj + '_lock'
            if cmds.objExists(LockObj) == True:
                attr = self.getLockAttr(obj, LockObj)
                skipTranslate = attr[0]
                skipRotate = attr[1]
                showAttrTR = attr[2]
                ads = cmds.listRelatives(obj, c=True)
                if cmds.ls(ads, type='parentConstraint') != []:
                    cmds.delete(cmds.ls(ads, type='parentConstraint'))
                cmds.delete(obj + '_lock_zero')
            else:
                cmds.warning(obj + '------no constrain')

        cmds.select(cl=True)
        setname = 'lockObjSet'
        if cmds.objExists(setname) == True and cmds.objectType(setname) == 'objectSet':
            cmds.sets(objs, remove=setname)
            if cmds.listConnections(setname, scn=True, destination=False) == None:
                cmds.delete(setname)
        cmds.select(objs)
        return

    def allUnLock(self):
        if cmds.objExists('lockObjSet') == True:
            objs = cmds.sets('lockObjSet', q=True)
            self.unLock(objs)
            sys.stderr.write(u'\u7269\u4f53\u5df2\u7ecf\u5168\u90e8\u89e3\u9501')
        else:
            sys.stderr.write(u'\u6ca1\u6709\u9700\u8981\u89e3\u9501\u7684\u7269\u4f53')

    def getLockAttr(self, obj, LockObj):
        attrs = ['translateX',
         'translateY',
         'translateZ',
         'rotateX',
         'rotateY',
         'rotateZ']
        skipTranslate = []
        skipRotate = []
        showAttrs = cmds.listAttr(obj, k=True, write=True, unlocked=True, s=True)
        showAttrTR = []
        for attr in attrs:
            if attr not in showAttrs:
                if 'translate' in attr:
                    skipTranslate.append(attr[-1].lower())
                if 'rotate' in attr:
                    skipRotate.append(attr[-1].lower())
                cmds.setAttr(LockObj + '.' + attr, lock=True)
            else:
                showAttrTR.append(attr)

        return (skipTranslate, skipRotate, showAttrTR)