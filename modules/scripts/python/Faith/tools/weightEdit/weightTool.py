# Embedded file name: E:/JunCmds/tool/weightEdit\weightTool.py
"""
import sys
sys.path.insert(0,r'E:\\JunCmds  ool')
import weightEdit.weightTool as weightTool
reload(weightTool)
weightTool = weightTool.weightTool()
weightTool.UI()

v2.1\xe4\xbf\xae\xe5\xa4\x8d\xe4\xba\x86\xe6\x9d\x83\xe9\x87\x8d\xe7\xbb\x98\xe5\x88\xb6\xe6\xa8\xa1\xe5\xbc\x8f\xe4\xb8\x8b\xe4\xb8\x8d\xe8\x83\xbd\xe4\xbd\xbf\xe7\x94\xa8\xe9\x97\xae\xe9\xa2\x98
v2.2\xe5\xa2\x9e\xe5\x8a\xa0\xe4\xba\x86\xe6\x9d\x83\xe9\x87\x8d\xe5\x80\xbc\xe5\xbf\xab\xe9\x80\x9f\xe9\x80\x89\xe6\x8b\xa9\xe6\x8c\x89\xe9\x92\xae
"""
import maya.cmds as cmds
import maya.mel as mel
import pickle
import os

class weightTool(object):

    def __init__(self):
        self.winprefix = 'Jun'

    def UI(self):
        ws = (150, 40, 80)
        ver = 'v3.0'
        model = cmds.ls(sl=True)
        if len(model) == 0:
            model = 'model'
            skin_jnts = ['< Nothing joint >']
        else:
            model = model[0]
            model = model.split('.')[0]
            skin = mel.eval('findRelatedSkinCluster' + '("' + model + '")')
            if skin == '':
                skin_jnts = ['< Nothing joint >']
            else:
                skin_jnts = cmds.skinCluster(skin, q=True, inf=skin)
        UI = 'weightToolUI'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        cmds.window(UI, t=self.winprefix + ' weight Tool ' + ver)
        menuBarLayout1 = cmds.menuBarLayout()
        cmds.menu(label='File')
        cmds.menuItem(label='New')
        cmds.menuItem(label='Open')
        cmds.menuItem(label='Close')
        cmds.menu(label='Help', helpMenu=True)
        cmds.menuItem(label='Weight Tool Help')
        cmds.setParent('..')
        cmds.setParent('..')
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        child1 = cmds.scrollLayout(horizontalScrollBarThickness=32, verticalScrollBarThickness=16, childResizable=True)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(40, 10, 100), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        t1 = cmds.text(l='vtx:')
        tf1 = cmds.textField('vtxWeightJntTF', text=model)
        b1 = cmds.button(l='load', c=lambda *args: self.loadJnt())
        cmds.setParent('..')
        cmds.frameLayout(label='skintJoint:')
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(40, 10, 100), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        t2 = cmds.text(l='jointA:')
        tf2 = cmds.textField('jointA', text='jntA')
        b2 = cmds.button(l='load', c=lambda *args: self.loadSel('jointA', 1))
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnWidth3=(40, 10, 100), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        t3 = cmds.text(l='jointB:')
        tf3 = cmds.textField('jointB', text='jntB')
        b3 = cmds.button(l='load', c=lambda *args: self.loadSel('jointB', 1))
        cmds.setParent('..')
        cmds.button(l='inversion', c=lambda *args: self.reverse())
        cmds.rowLayout(numberOfColumns=3, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l='Paint operation:', align='right', width=140)
        cmds.radioCollection()
        cmds.radioButton('Replace', label='Replace', align='left', sl=True, w=130)
        cmds.radioButton('Add', label='Add', align='right', w=50)
        cmds.setParent('..')
        cmds.floatSliderGrp('Opacity', label='Opacity:', field=True, minValue=0.0, maxValue=1.0, value=1.0, s=0.001)
        cmds.floatSliderGrp('Value', label='Value:', field=True, minValue=0.0, maxValue=1.0, value=0.5, s=0.001)
        cmds.flowLayout(columnSpacing=10)
        cmds.button(l=0.05, w=35, c=lambda *args: self.editValue(0.05))
        cmds.button(l=0.1, w=35, c=lambda *args: self.editValue(0.1))
        cmds.button(l=0.25, w=35, c=lambda *args: self.editValue(0.25))
        cmds.button(l=0.5, w=35, c=lambda *args: self.editValue(0.5))
        cmds.button(l=0.75, w=35, c=lambda *args: self.editValue(0.75))
        cmds.button(l=0.9, w=35, c=lambda *args: self.editValue(0.9))
        cmds.button(l='+0.05', w=35, c=lambda *args: self.editValue(cmds.floatSliderGrp('Value', q=True, value=True) + 0.05))
        cmds.button(l='-0.05', w=35, c=lambda *args: self.editValue(cmds.floatSliderGrp('Value', q=True, value=True) - 0.05))
        cmds.button(l='* 2', w=35, c=lambda *args: self.editValue(cmds.floatSliderGrp('Value', q=True, value=True) * 2.0))
        cmds.button(l='// 2', w=35, c=lambda *args: self.editValue(cmds.floatSliderGrp('Value', q=True, value=True) / 2.0))
        cmds.button(l='Ratio', w=35, c=lambda *args: self.getVtxWeightRatio())
        cmds.setParent('..')
        cmds.button(l='Flood', h=50, c=lambda *args: self.paint_skin_Weights(self.UIqury()[0], self.UIqury()[1], self.UIqury()[2], self.UIqury()[3]))
        cmds.setParent(tabs)
        copyWeightTab = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        t5 = cmds.text(l='Influence Association 1 :', h=20, w=130)
        copyWeightTypeUiom = cmds.optionMenu('InfluenceAssociation', h=20)
        cmds.menuItem(label='Closest joint')
        cmds.menuItem(label='Closest bone')
        cmds.menuItem(label='One to one')
        cmds.menuItem(label='Label')
        cmds.menuItem(label='name')
        cmds.optionMenu(copyWeightTypeUiom, e=True, sl=4)
        cmds.setParent(copyWeightTab)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        t6 = cmds.text(l='Influence Association 2 :', h=20, w=130)
        copyWeightTypeUiom2 = cmds.optionMenu('InfluenceAssociation2', h=20)
        cmds.menuItem(label='Closest joint')
        cmds.menuItem(label='Closest bone')
        cmds.menuItem(label='One to one')
        cmds.optionMenu(copyWeightTypeUiom2, e=True, sl=3)
        cmds.setParent(copyWeightTab)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.text(l='Weight Copy Mode :', h=20, w=130)
        self.WeightCopyMode_optionMenu = cmds.optionMenu('WeightCopyMode_optionMenu', h=25, w=100, cc=lambda *args: self.editUi1())
        cmds.menuItem(label=u'One Copy Multiple \u9009\u4e00\u4e2a\u6743\u91cd\u6a21\u578b\u52a0\u9009\u591a\u4e2a\u88ab\u62f7\u8d1d\u6743\u91cd\u6a21\u578b')
        cmds.menuItem(label=u'One Copy One      \u9009\u62e9\u88ab\u62f7\u8d1d\u6743\u91cd\u6a21\u578b')
        cmds.menuItem(label=u'Multiple Copy One \u9009\u591a\u4e2a\u6743\u91cd\u6a21\u578b\u52a0\u9009\u4e00\u4e2a\u88ab\u62f7\u8d1d\u6743\u91cd\u6a21\u578b')
        cmds.setParent(copyWeightTab)
        self.JntPrefix_row = cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text(l='Jnt Prefix :', w=130)
        jntPrefix_as = cmds.optionMenu('JntPrefix_as', w=40)
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.optionMenu('JntPrefix_as', e=True, sl=2)
        cmds.textField('JntPrefixTF', text=u'', h=25)
        cmds.setParent(copyWeightTab)
        self.JntSuffix_row = cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text(l='Jnt Suffix :', w=130)
        jntSuffix_as = cmds.optionMenu('JntSuffix_as', w=40)
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('JntSuffixTF', text=u'', h=25)
        cmds.setParent(copyWeightTab)
        self.weightMeshPrefix_row = cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], vis=1)
        cmds.text(l='weight mesh Prefix :', w=130)
        meshPrefix_as = cmds.optionMenu('meshPrefix_as', w=40)
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.optionMenu(meshPrefix_as, e=True, sl=1)
        cmds.textField('meshPrefixTF', text='', h=25)
        cmds.setParent(copyWeightTab)
        self.weightMeshSuffix_row = cmds.rowLayout(numberOfColumns=3, adjustableColumn=3, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], vis=1)
        cmds.text(l='weight mesh Suffix :', w=130)
        meshSuffix_as = cmds.optionMenu('meshSuffix_as', w=40)
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('meshSuffixTF', text='', h=25)
        cmds.setParent(copyWeightTab)
        cmds.rowLayout(numberOfColumns=6, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l=u'\u8fd0\u884c\u5b8c\u9690\u85cf:', align='right', width=130)
        cmds.radioCollection()
        self.skinModelVisCheckBox = cmds.checkBox('skinModelVisCheckBox', label=u'\u6743\u91cd\u6a21\u578b', value=1, w=80)
        self.by_copySkinModelVisCheckBox = cmds.checkBox('by_copySkinModelVisCheckBox', label=u'\u88ab\u62f7\u8d1d\u6743\u91cd\u6a21\u578b', value=0, w=100)
        cmds.setParent(copyWeightTab)
        copybutton3 = cmds.button(l=u'\u62f7\u8d1d\u6743\u91cd', h=40, c=lambda *args: self.copySkinWeightRun())
        frameLayout_face = cmds.frameLayout(label=u'\u8f85\u52a9\u5de5\u5177: -------------------------------------------------', cl=0, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=3)
        cmds.button(l=u'unlockInfluenceWeights\n(\u9632\u6b62\u6e05\u7406\u5c0f\u6743\u91cd\u9519\u8bef)', w=150, h=35, c=lambda *args: self.unlockInfluenceWeights())
        cmds.button(l=u'removeUnusedInfluences\n(\u79fb\u9664\u8499\u76ae\u4e2d\u65e0\u6743\u91cd\u9aa8\u9abc)', w=150, h=35, c=lambda *args: self.removeUnusedInfluences())
        selectSkinJntButton = cmds.button(l='Select Skin Jnt', w=150, h=35, c=lambda *args: self.selectSkinJnt(cmds.ls(sl=True)))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=4)
        cmds.text(l='Prune Below :', w=110, h=35)
        cmds.textField('pruneBelowTF', text='0.001', w=70, h=35)
        cmds.checkBox('unlockInfluenceWeightsCheckBox', label=u'unlock\nInfluenceWeights', value=1, w=120, h=35)
        cmds.button(l=u'\u6e05 \u9664 \u5c0f \u6743 \u91cd\n\u6e05\u9664\u524d\u4f1a\u81ea\u52a8\u89e3\u9501\u9aa8\u9abc', w=150, h=35, c=lambda *args: self.pruneWeightOptions(cmds.textField('pruneBelowTF', q=True, text=True)))
        cmds.setParent('..')
        frameLayout_face = cmds.frameLayout(label=u'  \u5176\u4ed6  : -------------------------------------------------', cl=1, cll=True, bgc=[0.3, 0.3, 0])
        BSWeightCopyButton = cmds.button(l='blendShape weight Copy', h=40, c=lambda *args: self.blendShapeWeightCopy())
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(l='Export bs Weight', h=30, w=160, c=lambda *args: self.Export_bsWeight())
        cmds.button(l='Import bs Weight', h=30, w=160, c=lambda *args: self.Import_bsWeight())
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(l=u'\u9009\u4e2dbs\u6743\u91cd\u4e3a1\u7684\u70b9', h=30, w=160, c=lambda *args: self.selectWeight_1_vtxs())
        cmds.setParent('..')
        cmds.setParent(copyWeightTab)
        cmds.setParent(tabs)
        replaceSkinJnt = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text(l='replaceSkinJntData:', h=30, w=100)
        cmds.textField('replaceSkinJntDataTF', text="{('zero_jnt','L_crotch_ik_jnt', 'R_crotch_ik_jnt', 'L_crotchend_ik_jnt','R_crotchend_ik_jnt', 'hips_simple_skin_jnt') :('Root')\n, ('body_hips_simple_skin_jnt') :('Spine')\n, ('waist01_simple_skin_jnt') :('Spine1')\n, ('waist02_simple_skin_jnt') :('Spine2')\n, ('waist03_simple_skin_jnt') :('Spine3')\n, ('waist04_simple_skin_jnt') :('Spine4')\n, ('chest_simple_skin_jnt') :('Chest')\n, ('chestmid_simple_skin_jnt','chestend_simple_skin_jnt') :('ChestMid')\n, ('neckroot_simple_skin_jnt','neckroot_simple_noroll_jnt') :('Neck1')\n, ('neck01_simple_skin_jnt') :('Neck2')\n, ('neck02_simple_skin_jnt') :('Neck3')\n, ('head_simple_skin_jnt') :('Head')\n, ('L_shoulder_ik_jnt') :('LeftShoulder')\n, ('L_uparm_second04_jnt', 'L_uparm_second03_jnt', 'L_uparm_second02_jnt', 'L_uparm_second01_jnt', 'L_uparm_dri_jnt') :('LeftArm')\n, ('L_lowarm_second04_jnt', 'L_lowarm_second03_jnt', 'L_lowarm_second02_jnt', 'L_lowarm_second01_jnt', 'L_lowarm_dri_jnt') :('LeftForeArm')\n, ('L_wrist_dri_jnt') :('LeftHand')\n, ('L_thumbfinger01_dri_jnt') :('LeftHandThumbRoot')\n, ('L_thumbfinger02_dri_jnt') :('LeftHandThumb1')\n, ('L_thumbfinger03_dri_jnt') :('LeftHandThumb2')\n, ('L_thumbfinger04_dri_jnt') :('LeftHandThumb3')\n, ('L_thumbfinger05_dri_jnt') :('LeftHandThumb4')\n, ('L_indexfinger01_dri_jnt') :('LeftHandIndexRoot')\n, ('L_indexfinger02_dri_jnt') :('LeftHandIndex1')\n, ('L_indexfinger03_dri_jnt') :('LeftHandIndex2')\n, ('L_indexfinger04_dri_jnt') :('LeftHandIndex3')\n, ('L_indexfinger05_dri_jnt') :('LeftHandIndex4')\n, ('L_middlefinger01_dri_jnt') :('LeftHandMiddleRoot')\n, ('L_middlefinger02_dri_jnt') :('LeftHandMiddle1')\n, ('L_middlefinger03_dri_jnt') :('LeftHandMiddle2')\n, ('L_middlefinger04_dri_jnt') :('LeftHandMiddle3')\n, ('L_middlefinger05_dri_jnt') :('LeftHandMiddle4')\n, ('L_ringfinger01_dri_jnt') :('LeftHandRingRoot')\n, ('L_ringfinger02_dri_jnt') :('LeftHandRing1')\n, ('L_ringfinger03_dri_jnt') :('LeftHandRing2')\n, ('L_ringfinger04_dri_jnt') :('LeftHandRing3')\n, ('L_ringfinger05_dri_jnt') :('LeftHandRing4')\n, ('L_pinkyfinger01_dri_jnt') :('LeftHandPinkyRoot')\n, ('L_pinkyfinger02_dri_jnt') :('LeftHandPinky1')\n, ('L_pinkyfinger03_dri_jnt') :('LeftHandPinky2')\n, ('L_pinkyfinger04_dri_jnt') :('LeftHandPinky3')\n, ('L_pinkyfinger05_dri_jnt') :('LeftHandPinky4')\n, ('L_upleg_second05_jnt', 'L_upleg_second04_jnt', 'L_upleg_second03_jnt', 'L_upleg_second02_jnt', 'L_upleg_second01_jnt', 'L_upleg_dri_jnt') :('LeftUpLeg')\n, ('L_lowleg_second05_jnt', 'L_lowleg_second04_jnt', 'L_lowleg_second03_jnt', 'L_lowleg_second02_jnt', 'L_lowleg_second01_jnt', 'L_lowleg_dri_jnt') :('LeftLeg')\n, ('L_ankle_dri_jnt') :('LeftFoot')\n, ('L_sole_dri_jnt') :('LeftToeBase')\n, ('R_shoulder_ik_jnt') :('RightShoulder')\n, ('R_uparm_second04_jnt', 'R_uparm_second03_jnt', 'R_uparm_second02_jnt', 'R_uparm_second01_jnt', 'R_uparm_dri_jnt') :('RightArm')\n, ('R_lowarm_second04_jnt', 'R_lowarm_second03_jnt', 'R_lowarm_second02_jnt', 'R_lowarm_second01_jnt', 'R_lowarm_dri_jnt') :('RightForeArm')\n, ('R_wrist_dri_jnt') :('RightHand')\n, ('R_thumbfinger01_dri_jnt') :('RightHandThumbRoot')\n, ('R_thumbfinger02_dri_jnt') :('RightHandThumb1')\n, ('R_thumbfinger03_dri_jnt') :('RightHandThumb2')\n, ('R_thumbfinger04_dri_jnt') :('RightHandThumb3')\n, ('R_thumbfinger05_dri_jnt') :('RightHandThumb4')\n, ('R_indexfinger01_dri_jnt') :('RightHandIndexRoot')\n, ('R_indexfinger02_dri_jnt') :('RightHandIndex1')\n, ('R_indexfinger03_dri_jnt') :('RightHandIndex2')\n, ('R_indexfinger04_dri_jnt') :('RightHandIndex3')\n, ('R_indexfinger05_dri_jnt') :('RightHandIndex4')\n, ('R_middlefinger01_dri_jnt') :('RightHandMiddleRoot')\n, ('R_middlefinger02_dri_jnt') :('RightHandMiddle1')\n, ('R_middlefinger03_dri_jnt') :('RightHandMiddle2')\n, ('R_middlefinger04_dri_jnt') :('RightHandMiddle3')\n, ('R_middlefinger05_dri_jnt') :('RightHandMiddle4')\n, ('R_ringfinger01_dri_jnt') :('RightHandRingRoot')\n, ('R_ringfinger02_dri_jnt') :('RightHandRing1')\n, ('R_ringfinger03_dri_jnt') :('RightHandRing2')\n, ('R_ringfinger04_dri_jnt') :('RightHandRing3')\n, ('R_ringfinger05_dri_jnt') :('RightHandRing4')\n, ('R_pinkyfinger01_dri_jnt') :('RightHandPinkyRoot')\n, ('R_pinkyfinger02_dri_jnt') :('RightHandPinky1')\n, ('R_pinkyfinger03_dri_jnt') :('RightHandPinky2')\n, ('R_pinkyfinger04_dri_jnt') :('RightHandPinky3')\n, ('R_pinkyfinger05_dri_jnt') :('RightHandPinky4')\n, ('R_upleg_second05_jnt', 'R_upleg_second04_jnt', 'R_upleg_second03_jnt', 'R_upleg_second02_jnt', 'R_upleg_second01_jnt', 'R_upleg_dri_jnt') :('RightUpLeg')\n, ('R_lowleg_second05_jnt', 'R_lowleg_second04_jnt', 'R_lowleg_second03_jnt', 'R_lowleg_second02_jnt', 'R_lowleg_second01_jnt', 'R_lowleg_dri_jnt') :('RightLeg')\n, ('R_ankle_dri_jnt') :('RightFoot')\n, ('R_sole_dri_jnt') :('RightToeBase')}", h=30)
        cmds.setParent('..')
        cmds.button(l=u'\u8fd0\u884c\u524d\u68c0\u67e5(\u9009\u62e9skin\u6a21\u578b)', h=50, c=lambda *args: self.skinJntTolistJntDifferenceSet())
        cmds.button(l=u'\u9009\u62e9\u6a21\u578b\u8fd0\u884c', h=50, c=lambda *args: self.replaceSkinJnt())
        cmds.setParent(tabs)
        ImExPort = cmds.formLayout('ImExPort', numberOfDivisions=100)
        ImExPortButton = cmds.button(l='ImExPort', h=50, c=lambda *args: self.ImportExport())
        cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'paint'),
         (copyWeightTab, 'Copy'),
         (replaceSkinJnt, 'replaceSkinJnt'),
         (ImExPort, 'ImExPort')), st=copyWeightTab)
        cmds.showWindow()
        self.editUi1()

    def WeightHelp(self):
        pass

    def loadModel(self):
        sel = cmds.ls(sl=True)[0]
        model = sel.split('.')[0]
        cmds.textField('skinModel', e=True, text=model)
        skin = mel.eval('findRelatedSkinCluster' + '("' + model + '")')
        if skin == '':
            cmds.textScrollList('jntList', e=True, ra=1)
            cmds.textScrollList('jntList', allowMultiSelection=True, e=True, append=['< Nothing joint >'], en=False)
        else:
            skin_jnts = cmds.skinCluster(skin, q=True, inf=skin)
            cmds.textScrollList('jntList', e=True, ra=1)
            cmds.textScrollList('jntList', allowMultiSelection=True, e=True, append=skin_jnts, en=True)
            return skin_jnts

    def editValue(self, Num):
        cmds.floatSliderGrp('Value', e=True, value=Num)

    def loadSel(self, tF, loadNum):
        sels = cmds.ls(sl=True)
        if len(sels) == loadNum:
            sel = sels[0]
            cmds.textField(tF, e=True, text=str(sel))
        else:
            cmds.warning('place Load --' + str(loadNum) + ' --objects')

    def loadJnt(self):
        vtx = cmds.ls(sl=True, fl=True)[0]
        vtxWeightJnts = self.getVtxWeightJnt()
        cmds.textField('vtxWeightJntTF', e=True, text=str(vtx) + '---' + str(vtxWeightJnts))
        if len(vtxWeightJnts) == 2:
            cmds.textField('jointA', e=True, text=vtxWeightJnts[0])
            cmds.textField('jointB', e=True, text=vtxWeightJnts[1])
        else:
            cmds.textField('jointA', e=True, text='')
            cmds.textField('jointB', e=True, text='')

    def UIqury(self):
        jointA = cmds.textField('jointA', q=True, text=True)
        jointB = cmds.textField('jointB', q=True, text=True)
        if cmds.radioButton('Replace', q=True, sl=True) == True:
            paint_operation = 'Replace'
        if cmds.radioButton('Add', q=True, sl=True) == True:
            paint_operation = 'Add'
        Opacity = cmds.floatSliderGrp('Opacity', q=True, value=True)
        Value = cmds.floatSliderGrp('Value', q=True, value=True)
        weightValue = Opacity * Value
        print(paint_operation, weightValue)
        return (jointA,
         jointB,
         paint_operation,
         weightValue)

    def reverse(self):
        jointA = cmds.textField('jointA', q=True, text=True)
        jointB = cmds.textField('jointB', q=True, text=True)
        print(jointA, jointB)
        cmds.textField('jointA', e=True, text=jointB)
        cmds.textField('jointB', e=True, text=jointA)

    def editUi1(self):
        print(cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True))
        if cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 1:
            cmds.rowLayout(self.JntPrefix_row, e=1, en=1)
            cmds.rowLayout(self.JntSuffix_row, e=1, en=1)
            cmds.rowLayout(self.weightMeshPrefix_row, e=1, en=0)
            cmds.rowLayout(self.weightMeshSuffix_row, e=1, en=0)
        elif cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 2:
            cmds.rowLayout(self.JntPrefix_row, e=1, en=1)
            cmds.rowLayout(self.JntSuffix_row, e=1, en=1)
            cmds.rowLayout(self.weightMeshPrefix_row, e=1, en=1)
            cmds.rowLayout(self.weightMeshSuffix_row, e=1, en=1)
        elif cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 3:
            cmds.rowLayout(self.JntPrefix_row, e=1, en=0)
            cmds.rowLayout(self.JntSuffix_row, e=1, en=0)
            cmds.rowLayout(self.weightMeshPrefix_row, e=1, en=0)
            cmds.rowLayout(self.weightMeshSuffix_row, e=1, en=0)

    def paint_skin_Weights(self, jnt01, jnt02, paint_operation, weight_value):
        verts1 = cmds.ls(sl=True, fl=True)
        verts = []
        for vert in verts1:
            if '.' in vert:
                verts.append(vert)

        if cmds.objExists(jnt01) != True:
            exit(jnt01 + ' ------ is not exists')
        if cmds.objExists(jnt02) != True:
            exit(jnt02 + ' ------ is not exists')
        model = verts[0].split('.')[0]
        skin = mel.eval('findRelatedSkinCluster' + '("' + model + '")')
        skin_jnts = cmds.skinCluster(skin, q=True, inf=skin)
        for jnt in skin_jnts:
            cmds.setAttr(jnt + '.liw', 1)

        cmds.setAttr(jnt01 + '.liw', 0)
        cmds.setAttr(jnt02 + '.liw', 0)
        if paint_operation == 'Replace':
            cmds.skinPercent(skin, verts, tv=[(jnt02, 0)])
        elif paint_operation == 'Add':
            pass
        for vert in verts:
            jnt01weight = cmds.skinPercent(skin, vert, t=jnt01, q=True)
            jnt02weight = cmds.skinPercent(skin, vert, t=jnt02, q=True)
            if paint_operation == 'Replace':
                weight = jnt01weight * (1.0 - weight_value)
                cmds.skinPercent(skin, vert, tv=[(jnt02, weight)])
            if paint_operation == 'Add':
                jnt01weight = jnt01weight + jnt02weight * weight_value
                cmds.skinPercent(skin, vert, tv=[(jnt01, jnt01weight)])

    def getVtxWeightRatio(self):
        jnt01 = cmds.textField('jointA', q=True, text=True)
        jnt02 = cmds.textField('jointB', q=True, text=True)
        vert = cmds.ls(sl=True)[0]
        model = vert.split('.')[0]
        print(vert, model)
        skin = mel.eval('findRelatedSkinCluster' + '("' + model + '")')
        jnt01weight = cmds.skinPercent(skin, vert, t=jnt01, q=True)
        jnt02weight = cmds.skinPercent(skin, vert, t=jnt02, q=True)
        VtxWeightRatio = jnt01weight / (jnt01weight + jnt02weight)
        self.editValue(VtxWeightRatio)

    def getVtxWeightJnt(self):
        vtx = cmds.ls(sl=True)[0]
        obj = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True)[0]
        skin = mel.eval('findRelatedSkinCluster' + '("' + obj + '")')
        skin_jnts = cmds.skinCluster(skin, q=True, inf=skin)
        vtxWeightJnts = []
        for jnt in skin_jnts:
            if cmds.skinPercent(skin, vtx, query=True, t=jnt) > 0.0001:
                vtxWeightJnts.append(jnt)

        print(vtx, '------', vtxWeightJnts)
        return vtxWeightJnts

    def copySkinWeightRun(self):
        WeightObjVis = 1
        copyWeightObjVis = 1
        if cmds.checkBox(self.skinModelVisCheckBox, q=True, value=True) == 1:
            WeightObjVis = 0
        if cmds.checkBox(self.by_copySkinModelVisCheckBox, q=True, value=True) == 1:
            copyWeightObjVis = 0
        if cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 1:
            self.copySkinWeight_one_to_multiple(cmds.ls(sl=True)[0], 'yes', WeightObjVis, copyWeightObjVis)
        elif cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 2:
            self.weightCopyOneToOne('yes', WeightObjVis, copyWeightObjVis)
        elif cmds.optionMenu(self.WeightCopyMode_optionMenu, q=True, sl=True) == 3:
            self.copyWeight_MultipleToOne()

    def copySkinWeight_one_to_multiple(self, WeightObj, delCopyObjSkin, WeightObjVis, copyWeightObjVis):
        copyWeightObjs = cmds.ls(sl=True)
        copyWeightObjs.remove(WeightObj)
        for copyWeightObj in copyWeightObjs:
            self.copySkinWeight(WeightObj, copyWeightObj, delCopyObjSkin, WeightObjVis, copyWeightObjVis)

        print('------- All is ok')
        cmds.select(WeightObj, copyWeightObjs)

    def weightCopyOneToOne(self, delCopyObjSkin, WeightObjVis, copyWeightObjVis):
        meshPrefix = cmds.textField('meshPrefixTF', q=True, text=True)
        meshSuffix = cmds.textField('meshSuffixTF', q=True, text=True)
        if cmds.optionMenu('meshPrefix_as', q=True, sl=True) == 1:
            meshPrefix = '+' + meshPrefix
        elif cmds.optionMenu('meshPrefix_as', q=True, sl=True) == 2:
            meshPrefix = '-' + meshPrefix
        if cmds.optionMenu('meshSuffix_as', q=True, sl=True) == 1:
            meshSuffix = '+' + meshSuffix
        elif cmds.optionMenu('meshSuffix_as', q=True, sl=True) == 2:
            meshSuffix = '-' + meshSuffix
        noSkin_Objs = []
        WeightObjs_noExists = []
        copyWeightObjs = cmds.ls(sl=True)
        for copyWeightObj in copyWeightObjs:
            remeshPrefix = meshPrefix[1:]
            remeshSuffix = meshSuffix[1:]
            meshPrefixNum = len(remeshPrefix)
            meshSuffixNum = len(remeshSuffix)
            if meshPrefix[0] == '+' and meshSuffix[0] == '+':
                WeightObj = remeshPrefix + copyWeightObj + remeshSuffix
            elif meshPrefix[0] == '+' and meshSuffix[0] == '-':
                if meshSuffixNum == 0:
                    WeightObj = remeshPrefix + copyWeightObj
                else:
                    WeightObj = remeshPrefix + copyWeightObj[:-meshSuffixNum]
            elif meshPrefix[0] == '-' and meshSuffix[0] == '+':
                WeightObj = copyWeightObj[meshPrefixNum:] + remeshSuffix
            elif meshPrefix[0] == '-' and meshSuffix[0] == '-':
                if meshSuffixNum == 0:
                    WeightObj = copyWeightObj[meshPrefixNum:]
                else:
                    WeightObj = copyWeightObj[meshPrefixNum:][:-meshSuffixNum]
            else:
                cmds.warning('please confirm meshPrefix and meshSuffix +- ')
                WeightObj = remeshPrefix + copyWeightObj + remeshSuffix
            errorObj = self.copySkinWeight(WeightObj, copyWeightObj, delCopyObjSkin, WeightObjVis, copyWeightObjVis)
            print(errorObj)
            if errorObj != None and errorObj[0] != None:
                noSkin_Objs.append(errorObj[0])
            if errorObj != None and errorObj[1] != None:
                WeightObjs_noExists.append(errorObj[1])

        print('weight obj no skin:-----' + str(noSkin_Objs) + '\n' + 'no weight obj:------' + 'cmds.setAttr(' + str(WeightObjs_noExists) + ')' + '\n' + '------' * 8, 'All is ok', '------' * 8)
        return

    def copySkinWeight(self, WeightObj, copyWeightObj, delCopyObjSkin, WeightObjVis, copyWeightObjVis):
        jntPrefix = cmds.textField('JntPrefixTF', q=True, text=True)
        jntSuffix = cmds.textField('JntSuffixTF', q=True, text=True)
        if cmds.optionMenu('JntPrefix_as', q=True, sl=True) == 1:
            jntPrefix = '+' + jntPrefix
        elif cmds.optionMenu('JntPrefix_as', q=True, sl=True) == 2:
            jntPrefix = '-' + jntPrefix
        if cmds.optionMenu('JntSuffix_as', q=True, sl=True) == 1:
            jntSuffix = '+' + jntSuffix
        elif cmds.optionMenu('JntSuffix_as', q=True, sl=True) == 2:
            jntSuffix = '-' + jntSuffix
        if cmds.objExists(WeightObj) == True:
            if mel.eval('findRelatedSkinCluster' + '("' + WeightObj + '")') != '':
                skin = mel.eval('findRelatedSkinCluster' + '("' + WeightObj + '")')
                skin_jntList = cmds.skinCluster(skin, q=True, inf=skin)
                newSkinJnts = []
                for skinJnt in skin_jntList:
                    rejntPrefix = jntPrefix[1:]
                    rejntSuffix = jntSuffix[1:]
                    if jntPrefix[0] == '+' and jntSuffix[0] == '+':
                        newSkinJnt = rejntPrefix + skinJnt + rejntSuffix
                    elif jntPrefix[0] == '+' and jntSuffix[0] == '-':
                        jntSuffixNum = len(rejntSuffix)
                        if jntSuffixNum == 0:
                            newSkinJnt = rejntPrefix + skinJnt
                        else:
                            newSkinJnt = rejntPrefix + skinJnt[:-jntSuffixNum]
                    elif jntPrefix[0] == '-' and jntSuffix[0] == '+':
                        jntPrefixNum = len(rejntPrefix)
                        newSkinJnt = skinJnt[jntPrefixNum:] + rejntSuffix
                    elif jntPrefix[0] == '-' and jntSuffix[0] == '-':
                        jntPrefixNum = len(rejntPrefix)
                        jntSuffixNum = len(rejntSuffix)
                        if jntSuffixNum == 0:
                            newSkinJnt = skinJnt[jntPrefixNum:]
                        else:
                            newSkinJnt = skinJnt[jntPrefixNum:][:-jntSuffixNum]
                    else:
                        cmds.warning('please confirm jntPrefix and jntSuffix +- ')
                    newSkinJnts.append(newSkinJnt)

                for newSkinJnt in newSkinJnts:
                    if cmds.objExists(newSkinJnt) != True:
                        cmds.warning(u'\u65b0\u9aa8\u9abc\u4e0d\u5b58\u5728------' + newSkinJnt)

                copyWeightObjSkin = mel.eval('findRelatedSkinCluster' + '("' + copyWeightObj + '")')
                if copyWeightObjSkin != '' and cmds.nodeType(copyWeightObjSkin) == 'skinCluster':
                    copyWeightObjJnts = cmds.skinCluster(copyWeightObjSkin, q=True, inf=copyWeightObjSkin)
                    if skin_jntList == copyWeightObjJnts:
                        print(u'\u8499\u76ae\u9aa8\u9abc\u4e00\u81f4')
                    elif delCopyObjSkin == 'yes':
                        print(u'\u91cd\u65b0\u8499\u76ae\u4e86')
                        cmds.delete(copyWeightObjSkin)
                        cmds.skinCluster(newSkinJnts, copyWeightObj, mi=10, rui=False, tsb=True)
                elif copyWeightObjSkin == '':
                    cmds.skinCluster(newSkinJnts, copyWeightObj, mi=10, rui=False, tsb=True)
                copyWeightTypeNum = cmds.optionMenu('InfluenceAssociation', q=True, sl=True)
                if copyWeightTypeNum == 1:
                    influenceAssociation = 'closestJoint'
                if copyWeightTypeNum == 2:
                    influenceAssociation = 'closestBone'
                if copyWeightTypeNum == 3:
                    influenceAssociation = 'oneToOne'
                if copyWeightTypeNum == 4:
                    influenceAssociation = 'label'
                if copyWeightTypeNum == 5:
                    influenceAssociation = 'name'
                copyWeightTypeNum2 = cmds.optionMenu('InfluenceAssociation2', q=True, sl=True)
                if copyWeightTypeNum2 == 1:
                    influenceAssociation2 = 'closestJoint'
                if copyWeightTypeNum2 == 2:
                    influenceAssociation2 = 'closestBone'
                if copyWeightTypeNum2 == 3:
                    influenceAssociation2 = 'oneToOne'
                cmds.copySkinWeights(WeightObj, copyWeightObj, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[influenceAssociation, influenceAssociation2])
                cmds.select(copyWeightObj)
                cmds.setAttr(WeightObj + '.visibility', WeightObjVis)
                cmds.setAttr(copyWeightObj + '.visibility', copyWeightObjVis)
                print(copyWeightObj + '------------is ok')
            else:
                print(WeightObj + '----------- no skinCluster')
                return (WeightObj, None)
        else:
            print(WeightObj + '-----------no object')
            return (None, copyWeightObj)
        return None

    def copySkinWeight2(self, WeightObjVis, copyWeightObjVis):
        sels = cmds.ls(sl=True)
        WeightObj = sels[0]
        copyWeightObjs = sels[1:]
        copyWeightTypeNum = cmds.optionMenu('InfluenceAssociation', q=True, sl=True)
        if copyWeightTypeNum == 1:
            influenceAssociation = 'closestJoint'
        if copyWeightTypeNum == 2:
            influenceAssociation = 'closestBone'
        if copyWeightTypeNum == 3:
            influenceAssociation = 'oneToOne'
        if copyWeightTypeNum == 4:
            influenceAssociation = 'label'
        if copyWeightTypeNum == 5:
            influenceAssociation = 'name'
        copyWeightTypeNum2 = cmds.optionMenu('InfluenceAssociation2', q=True, sl=True)
        if copyWeightTypeNum2 == 1:
            influenceAssociation2 = 'closestJoint'
        if copyWeightTypeNum2 == 2:
            influenceAssociation2 = 'closestBone'
        if copyWeightTypeNum2 == 3:
            influenceAssociation2 = 'oneToOne'
        for copyWeightObj in copyWeightObjs:
            cmds.copySkinWeights(WeightObj, copyWeightObj, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[influenceAssociation, influenceAssociation2])
            cmds.setAttr(copyWeightObj + '.v', copyWeightObjVis)

        cmds.setAttr(WeightObj + '.v', WeightObjVis)

    def copyVtxweight(self):
        vtxs = cmds.ls(sl=True)
        onevtxs = []
        for vtx in vtxs:
            vtx.split('[')[-1].split(':')[0]
            onevtx = vtx.split('.')[0] + '.vtx' + '[' + str(int(vtx.split('[')[-1].split(':')[0]) + 3) + ']'
            onevtxs.append(onevtx)
            cmds.select(onevtx)
            mel.eval('artAttrSkinWeightCopy')
            cmds.select(vtx)
            mel.eval('artAttrSkinWeightPaste')

    def copyWeight_MultipleToOne(self):
        sels = cmds.ls(sl=True)
        weightObjs = sels[:-1]
        copyWeightObj = sels[-1]
        print('weightObjs-----', weightObjs)
        print('copyWeightObj--', copyWeightObj)
        copyWeightObjSkin = mel.eval('findRelatedSkinCluster' + '("' + copyWeightObj + '")')
        if copyWeightObjSkin != '' and cmds.nodeType(copyWeightObjSkin):
            cmds.delete(copyWeightObjSkin)
        skinJntAlls = self.selectSkinJnt(weightObjs)
        print('skinJntAlls------', skinJntAlls)
        cmds.skinCluster(skinJntAlls, copyWeightObj, mi=10, rui=False, tsb=True)
        copyWeightTypeNum = cmds.optionMenu('InfluenceAssociation', q=True, sl=True)
        if copyWeightTypeNum == 1:
            influenceAssociation = 'closestJoint'
        if copyWeightTypeNum == 2:
            influenceAssociation = 'closestBone'
        if copyWeightTypeNum == 3:
            influenceAssociation = 'oneToOne'
        if copyWeightTypeNum == 4:
            influenceAssociation = 'label'
        if copyWeightTypeNum == 5:
            influenceAssociation = 'name'
        copyWeightTypeNum2 = cmds.optionMenu('InfluenceAssociation2', q=True, sl=True)
        if copyWeightTypeNum2 == 1:
            influenceAssociation2 = 'closestJoint'
        if copyWeightTypeNum2 == 2:
            influenceAssociation2 = 'closestBone'
        if copyWeightTypeNum2 == 3:
            influenceAssociation2 = 'oneToOne'
        cmds.copySkinWeights(weightObjs, copyWeightObj, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[influenceAssociation, influenceAssociation2])
        for weightObj in weightObjs:
            cmds.setAttr(weightObj + '.visibility', 0)

        cmds.setAttr(copyWeightObj + '.visibility', 0)
        print(copyWeightObj + '------------is ok')
        cmds.select(sels)

    def selectSkinJnt(self, objs):
        skinJntAlls = []
        for obj in objs:
            skin = mel.eval('findRelatedSkinCluster' + '("' + obj + '")')
            if skin == '' or skin == [] or skin == None:
                cmds.warning('no skinCluster')
            else:
                skin_jnts = cmds.skinCluster(skin, q=True, inf=skin)
                skinJnts = cmds.ls(skin_jnts, fl=True)
                for skinJnt in skinJnts:
                    if skinJnt not in skinJntAlls:
                        skinJntAlls.append(skinJnt)

        skinJntAlls = list(set(skinJntAlls))
        cmds.select(skinJntAlls)
        return skinJntAlls

    def modifyHierarchy(self):
        sels = cmds.ls(sl=True)
        errorHierarchyObj = sels[0]
        okHierarchyObj = sels[-1]
        okHierarchyObjPar = cmds.listRelatives(okHierarchyObj, p=True, f=True)[0]
        errorHierarchyObjPar = cmds.listRelatives(errorHierarchyObj, p=True, f=True)[0]
        childrens = cmds.listRelatives(okHierarchyObjPar, c=True)
        relative = childrens.index(okHierarchyObj)
        if errorHierarchyObjPar != okHierarchyObjPar:
            cmds.parent(errorHierarchyObj, okHierarchyObjPar)
        else:
            cmds.parent(errorHierarchyObj, w=True)
            cmds.parent(errorHierarchyObj, okHierarchyObjPar)
        cmds.reorder(errorHierarchyObj, relative=relative + 2)

    def blendShapeWeightCopy(self):
        sels = cmds.ls(sl=True)
        if len(sels) >= 2:
            sourceObj = sels[0]
            sourceShape = cmds.listRelatives(sourceObj, s=True)[0]
            sourceBlendShape = cmds.listConnections(sourceShape + '.inMesh', scn=True, destination=False)
            destinationObjs = sels[1:]
            for destinationObj in destinationObjs:
                destinationShape = cmds.listRelatives(destinationObj, s=True)[0]
                destinationBlendShape = cmds.listConnections(destinationShape + '.inMesh', scn=True, destination=False)
                if sourceBlendShape != None:
                    if cmds.objectType(sourceBlendShape[0]) == 'blendShape':
                        if destinationBlendShape != None:
                            if cmds.objectType(destinationBlendShape[0]) == 'blendShape':
                                vtxs = cmds.ls(sourceShape + '.vtx[0:]', fl=True)
                                vtxNum = len(vtxs)
                                for x in range(vtxNum):
                                    weight = cmds.getAttr('%s.it[0].bw[%d]' % (sourceBlendShape[0], int(x)))
                                    cmds.setAttr('%s.it[0].bw[%d]' % (destinationBlendShape[0], int(x)), weight)

                            else:
                                cmds.warning(destinationBlendShape + ' There is no blendShape')
                        else:
                            cmds.warning(destinationBlendShape + ' There is no blendShape')
                    else:
                        cmds.warning(sourceObj + ' There is no blendShape')
                else:
                    cmds.warning(sourceObj + ' There is no blendShape')

        else:
            cmds.warning('plase select at least two model')
        return

    def shrinkWrapWeightCopy(self):
        sels = cmds.ls(sl=True)
        if len(sels) >= 2:
            sourceObj = sels[0]
            sourceShape = cmds.listRelatives(sourceObj, s=True)[0]
            sourceBlendShape = cmds.listConnections(sourceShape + '.inMesh', scn=True, destination=False)
            destinationObjs = sels[1:]
            for destinationObj in destinationObjs:
                destinationShape = cmds.listRelatives(destinationObj, s=True)[0]
                destinationBlendShape = cmds.listConnections(destinationShape + '.inMesh', scn=True, destination=False)
                if sourceBlendShape != None:
                    if cmds.objectType(sourceBlendShape[0]) == 'shrinkWrap':
                        if destinationBlendShape != None:
                            if cmds.objectType(destinationBlendShape[0]) == 'shrinkWrap':
                                vtxs = cmds.ls(sourceShape + '.vtx[0:]', fl=True)
                                vtxNum = len(vtxs)
                                for x in range(vtxNum):
                                    weight = cmds.percent(sourceBlendShape[0], sourceObj + '.vtx[' + str(x) + ']', q=True, v=True)
                                    cmds.percent(destinationBlendShape[0], destinationObj + '.vtx[' + str(x) + ']', v=weight[0])

                            else:
                                cmds.warning(destinationBlendShape + ' There is no blendShape')
                        else:
                            cmds.warning(destinationBlendShape + ' There is no blendShape')
                    else:
                        cmds.warning(sourceObj + ' There is no blendShape')
                else:
                    cmds.warning(sourceObj + ' There is no blendShape')

        else:
            cmds.warning('plase select at least two model')
        return

    def skinJntTolistJntDifferenceSet(self):
        objs = cmds.ls(sl=True)
        jntDatas = cmds.textField('replaceSkinJntDataTF', q=True, text=True)
        jntDatas = eval(jntDatas)
        print(jntDatas)
        oldjnts = []
        newJnts = []
        errorJnts = []
        for oldJnt in jntDatas:
            newJnt = jntDatas.get(oldJnt)
            if type(oldJnt) == tuple:
                for oldJntx in oldJnt:
                    oldjnts.append(oldJntx)

            if type(oldJnt) == str:
                oldjnts.append(oldJnt)
            newJnts.append(newJnt)

        for jnt in oldjnts:
            if cmds.objExists(jnt) != True:
                cmds.warning(u'\u539f\u9aa8\u9abc\u4e0d\u5b58\u5728---' + jnt + '---is no old Jnt')
                errorJnts.append(jnt)

        for jnt in newJnts:
            if cmds.objExists(jnt) != True:
                cmds.warning(u'\u65b0\u9aa8\u9abc\u4e0d\u5b58\u5728---' + jnt + '---is no new Jnt')
                errorJnts.append(jnt)

        skinJntAlls = self.selectSkinJnt(objs)
        listnotJnts = []
        for jnt in skinJntAlls:
            if jnt not in oldjnts:
                cmds.warning(u'\u6709\u8499\u76ae\u9aa8\u9abc\u4e0d\u5728\u5217\u8868\u4e2d---' + jnt)
                listnotJnts.append(jnt)
                errorJnts.append(jnt)

        cmds.select(objs)
        cmds.sets(listnotJnts)
        if errorJnts == []:
            print('---all is ok')

    def replaceSkinJnt(self):
        jntDatas = cmds.textField('replaceSkinJntDataTF', q=True, text=True)
        jntDatas = eval(jntDatas)
        alljnts = []
        for oldJnt in jntDatas:
            newJnt = jntDatas.get(oldJnt)
            if type(oldJnt) == tuple:
                for oldJntx in oldJnt:
                    alljnts.append(oldJntx)

            if type(oldJnt) == str:
                alljnts.append(oldJnt)
            alljnts.append(newJnt)

        notExistsjnts = []
        for jnt in alljnts:
            if cmds.objExists(jnt) != True:
                cmds.warning(jnt + '---is no Jnt')
                notExistsjnts.append(jnt)

        if notExistsjnts != []:
            cmds.error(u'\u6709\u9aa8\u9abc\u4e0d\u5b58\u5728')
        sels = cmds.ls(sl=True)
        for obj in sels:
            skin = mel.eval('findRelatedSkinCluster' + '("' + obj + '")')
            skinJnts = cmds.skinCluster(skin, q=True, inf=skin)
            for jnt in skinJnts:
                cmds.setAttr(jnt + '.liw', 1)

            for oldJnt in jntDatas:
                newJnt = jntDatas.get(oldJnt)
                if newJnt not in skinJnts:
                    cmds.skinCluster(skin, e=True, dr=4, lw=True, wt=0, ai=newJnt)
                cmds.setAttr(newJnt + '.liw', 0)
                if type(oldJnt) == tuple:
                    for oldJntx in oldJnt:
                        if oldJntx in skinJnts:
                            cmds.skinPercent(skin, obj, tv=[(oldJntx, 0)])
                            cmds.skinCluster(skin, e=True, ri=oldJntx)

                elif type(oldJnt) == str:
                    if oldJnt in skinJnts:
                        cmds.skinPercent(skin, obj, tv=[(oldJnt, 0)])
                        cmds.skinCluster(skin, e=True, ri=oldJnt)
                cmds.setAttr(newJnt + '.liw', 1)

        cmds.select(sels)

    def ImportExport(self):
        import weightEdit.rig_ch.skinClusterWeight as skWt
        skWt.win()
        objs = cmds.ls(sl=True)
        print(len(objs))
        noseekObjs = []
        for obj in objs:
            cmds.select(cl=True)
            noseekObj = obj + '_mo'
            if cmds.objExists(noseekObj) == True:
                print(noseekObj)
            else:
                noseekObjs.append(noseekObj)

        cmds.select(noseekObjs)

    def Export_bsWeight(self):
        obj = cmds.ls(sl=True)[0]
        objShape = cmds.listRelatives(obj, s=True)[0]
        meshHistory = cmds.listHistory(obj, pdo=True)
        objBlendShape = cmds.ls(meshHistory, type='blendShape')
        if objBlendShape == []:
            cmds.error(u'\u6ca1\u6709bs\u8282\u70b9')
        vtxs = cmds.ls(objShape + '.vtx[0:]', fl=True)
        vtxNum = len(vtxs)
        weights = []
        for x in range(vtxNum):
            weight = cmds.getAttr('%s.it[0].bw[%d]' % (objBlendShape[0], int(x)))
            weights.append(weight)

        print(weights)
        f = cmds.file(q=1, sn=1)
        filePath = cmds.fileDialog(dm=f[0:-len(f.split('/')[-1])] + '*.cs', m=1)
        if filePath:
            newFile = open(filePath, 'w')
            pickle.dump(weights, newFile)
            newFile.close()

    def Import_bsWeight(self):
        obj = cmds.ls(sl=True)[0]
        objShape = cmds.listRelatives(obj, s=True)[0]
        meshHistory = cmds.listHistory(obj, pdo=True)
        objBlendShape = cmds.ls(meshHistory, type='blendShape')
        if objBlendShape == []:
            cmds.error(u'\u6ca1\u6709bs\u8282\u70b9')
        f = cmds.file(q=1, sn=1)
        filePath = cmds.fileDialog(dm=f[0:-len(f.split('/')[-1])] + '*.cs', m=0)
        if filePath:
            readFile = open(filePath, 'r')
            weights = pickle.load(readFile)
            readFile.close()
            vtxs = cmds.ls(objShape + '.vtx[0:]', fl=True)
            vtxNum = len(vtxs)
            for x in range(vtxNum):
                weight = weights[x]
                cmds.setAttr('%s.it[0].bw[%d]' % (objBlendShape[0], int(x)), weight)

    def selectWeight_1_vtxs(self):
        obj = cmds.ls(sl=True)[0]
        objShape = cmds.listRelatives(obj, s=True)[0]
        meshHistory = cmds.listHistory(obj, pdo=True)
        objBlendShape = cmds.ls(meshHistory, type='blendShape')
        if objBlendShape == []:
            cmds.error(u'\u6ca1\u6709bs\u8282\u70b9')
        vtxs = cmds.ls(objShape + '.vtx[0:]', fl=True)
        vtxNum = len(vtxs)
        weights = []
        selvtxs = []
        for x in range(vtxNum):
            vtx = vtxs[x]
            weight = cmds.getAttr('%s.it[0].bw[%d]' % (objBlendShape[0], int(x)))
            if round(weight, 2) == 1.0:
                selvtxs.append(vtx)

        cmds.select(selvtxs)

    def unlockInfluenceWeights(self):
        jnts = cmds.ls(type='joint')
        for jnt in jnts:
            if 'lockInfluenceWeights' in cmds.listAttr(jnt):
                cmds.setAttr(jnt + '.liw', 0)

    def removeUnusedInfluences(self):
        mel.eval('removeUnusedInfluences;')

    def pruneWeightOptions(self, pruneBelow):
        uiwValue = cmds.checkBox('unlockInfluenceWeightsCheckBox', q=True, value=True)
        if uiwValue == True:
            uiwValue = 1
        else:
            uiwValue = 0
        mel.eval('doPruneSkinClusterWeightsArgList %d { "%s" }' % (uiwValue, str(pruneBelow)))