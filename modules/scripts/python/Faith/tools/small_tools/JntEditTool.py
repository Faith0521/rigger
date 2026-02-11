# Embedded file name: E:/JunCmds/tool/JntEditTool.py
r"""
import sys
sys.path.append(r'\yuweijun\E\JunCmds   ool')
import JntVis as JntVis
reload(JntVis)
JntVisEdit = JntVis.JntVisEdit()
JntVisEdit.JntVisUI()
"""
import maya.cmds as cmds

class JntEditTool:

    def __init__(self):
        pass

    def JntEditToolUI(self):
        UI = 'JntEditTool'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        a = cmds.window(UI, t='Jun JntEditToolwin')
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(l=u'\u9009\u62e9\u5f53\u524d\u9009\u62e9\u7269\u4f53\u4e0b\u7684joint', c=lambda *args: self.sel(['joint']), h=40)
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.checkBox('hideOnPlaybackCB', label='edit hideOnPlayback', value=0, width=125, h=40)
        cmds.button(l='Inverse Select', c=lambda *args: self.Inverse(), width=125, h=40)
        cmds.button(l='show', c=lambda *args: self.ShowHideJnt(0, 1), width=125, h=40)
        cmds.button(l='hidden', c=lambda *args: self.ShowHideJnt(2, 1), width=125, h=40)
        cmds.setParent('..')
        cmds.showWindow()

    def ShowHideJnt(self, drawStyle, hideOnPlayback):
        edithideOnPlayback = cmds.checkBox('hideOnPlaybackCB', q=True, value=1)
        print(edithideOnPlayback)
        jnts = cmds.ls(type='joint')
        sels = cmds.ls(sl=True, type='joint')
        if sels != []:
            jnts = sels
        for jnt in jnts:
            cmds.setAttr(jnt + '.drawStyle', drawStyle)
            if edithideOnPlayback == True:
                cmds.setAttr(jnt + '.hideOnPlayback', hideOnPlayback)

    def Inverse(self):
        selJnts = cmds.ls(sl=True, type='joint')
        AllJnt = cmds.ls(type='joint')
        InverseJnt = AllJnt
        for sj in selJnts:
            if sj in AllJnt:
                InverseJnt.remove(sj)

        cmds.select(InverseJnt)

    def sel(self, selTypes):
        sels = cmds.ls(sl=True)
        grp_ads = []
        for grp in sels:
            for selType in selTypes:
                selTypeObjs = cmds.listRelatives(grp, ad=True, type=selType, f=True)
                print(selTypeObjs)
                if selTypeObjs != None:
                    grp_ads = grp_ads + selTypeObjs

        if grp_ads != []:
            cmds.select(grp_ads)
        else:
            cmds.warning(u'no ---', selTypes)
        return