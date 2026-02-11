# Embedded file name: E:/JunCmds/tool/displayEdit.py
r"""
import sys
sys.path.append(r'\yuweijun\E\JunCmds   ool')
import JntVis as JntVis
reload(JntVis)
JntVisEdit = JntVis.JntVisEdit()
JntVisEdit.JntVisUI()
"""
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import sys, re, os, string

class displayEdit:

    def __init__(self):
        pass

    def win(self):
        UI = 'displayEdit'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        a = cmds.window(UI, t='Jun displayEdit')
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(l='dispCV', c=lambda *args: self.displayNurbs('dispCV'), width=100, h=40)
        cmds.button(l='dispEP', c=lambda *args: self.displayNurbs('dispEP'), width=100, h=40)
        cmds.button(l=u'\u5173\u95ed\u6240\u6709\u8f74\u5411\u663e\u793a', c=lambda *args: self.closeLocalRotationAxes(), width=100, h=40)
        cmds.showWindow()

    def displayNurbs(self, displayType):
        sels = cmds.ls(sl=True)
        dispcv = cmds.getAttr(sels[0] + '.' + displayType)
        for sel in sels:
            if dispcv == 0:
                cmds.setAttr(sel + '.' + displayType, 1)
            if dispcv == 1:
                cmds.setAttr(sel + '.' + displayType, 0)

    def closeLocalRotationAxes(self):
        """\xe5\x85\xb3\xe9\x97\xad\xe6\x89\x80\xe6\x9c\x89\xe8\xbd\xb4\xe5\x90\x91\xe6\x98\xbe\xe7\xa4\xba"""
        allObjs = cmds.ls(type='transform')
        for obj in allObjs:
            cmds.setAttr(obj + '.displayLocalAxis', 0)