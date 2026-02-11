# Embedded file name: E:/JunCmds/tool/selectTool.py
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
selprefix = 'Jun'
cbd_layout = selprefix + 'selPlusMinus_ColumnLayout'

class selTool:

    def __init__(self):
        pass

    def win(self):
        UI = 'selTool'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        a = cmds.window(UI, t='Jun selTool')
        cmds.rowColumnLayout(numberOfColumns=2)
        objTypeTF = cmds.textField('objTypeTF', text=u'\u7269\u4f53\u7c7b\u578b')
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684(UI\u4e2d\u586b\u5199\u7684\u7c7b\u578b)', c=lambda *args: self.sel([cmds.textField(objTypeTF, text=True, q=True)]), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684transform', c=lambda *args: self.sel(['transform']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684mesh', c=lambda *args: self.sel(['mesh']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684joint', c=lambda *args: self.sel(['joint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684\u7ea6\u675f\u8282\u70b9', c=lambda *args: self.sel(['parentConstraint',
         'pointConstraint',
         'orientConstraint',
         'scaleConstraint',
         'aimConstraint',
         'pointOnPolyConstraint',
         'geometryConstraint',
         'normalConstraint',
         'tangentConstraint',
         'poleVectorConstraint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684parentConstraint', c=lambda *args: self.sel(['parentConstraint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684pointConstraint', c=lambda *args: self.sel(['pointConstraint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684orientConstraint', c=lambda *args: self.sel(['orientConstraint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u7ec4\u4e0b\u9762\u6240\u6709\u7684scaleConstraint', c=lambda *args: self.sel(['scaleConstraint']), h=40)
        cmds.button(l=u'\u9009\u62e9\u6240\u6709\u5c42', c="cmds.select(cmds.ls(type = 'displayLayer'))", h=40)
        cmds.button(l=u'\u9009\u62e9\u52a0\u51cf', c=lambda *args: self.selPlusMinusWin(), h=40)
        cmds.showWindow()

    def sel(self, selTypes):
        sels = cmds.ls(sl=True)
        grp_ads = []
        for grp in sels:
            for selType in selTypes:
                selTypeObjs = cmds.listRelatives(grp, ad=True, type=selType, f=True)
                print (selTypeObjs)
                if selTypeObjs != None:
                    grp_ads = grp_ads + selTypeObjs

        if grp_ads != []:
            cmds.select(grp_ads)
        else:
            cmds.warning(u'no ---', selTypes)
        return

    def selPlusMinusWin(self):
        global cbd_layout
        global selprefix
        winName = selprefix + 'selPlusMinusTool_win'
        if cmds.window(winName, ex=True):
            cmds.deleteUI(winName)
        runCmd = 'import %s as cmdrTool\ncmdrTool' % __name__
        cmds.window(winName, t=selprefix + ' selPlusMinus Tool ')
        scrollArea = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16, childResizable=True)
        self.rotLayout = cmds.columnLayout(adj=True)
        cmds.rowLayout(numberOfColumns=6)
        cmds.button(label='+', c=lambda *args: self.addButton(1), h=30, w=30)
        cmds.button(label='--', c=lambda *args: self.addButton(-1), h=30, w=30)
        cmds.textField('archiveTF', text=u'A1', h=30, w=50)
        cmds.button(label=u'  \u5b58\u6863  ', c=lambda *args: self.objsTFArchive(), h=30)
        cmds.button(label=u'  \u6062\u590d \u5b58\u6863  ', c=lambda *args: self.restoreArchive(), h=30)
        cmds.button(label=u'  \u5220\u9664 \u5b58\u6863  ', c=lambda *args: self.objsTFArchive(), h=30)
        cmds.setParent(self.rotLayout)
        dvrLayout = cmds.columnLayout(cbd_layout, adj=True)
        self.addButton(1)
        self.addButton(1)
        cmds.setParent(self.rotLayout)
        cmds.button(l='Apply', c=lambda *args: self.selObjPM(), h=30)
        cmds.showWindow(winName)
        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        cmds.window(winName, e=True, h=numCdrn * 25 + 70, w=450)

    def addButton(self, v):
        winName = selprefix + 'selPlusMinusTool_win'
        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        if v == 1:
            row1 = cmds.rowLayout(numberOfColumns=5, p=cbd_layout)
            numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
            print (numCdrn)
            i = numCdrn / 2
            cbdr_loadChannlAttr_tfg = selprefix + 'cbdr_loadChannlAttr' + str(i) + '_tfg'
            a = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, p=row1, l='select: ', text='[]', ed=0, h=25, columnWidth3=[40, 200, 50], cl2=['center', 'left'], bl='<<Load', bc=lambda *args: self.Load('%s' % cbdr_loadChannlAttr_tfg))
            cmds.button(label='select', c=lambda *args: self.selectTFobj('%s' % cbdr_loadChannlAttr_tfg), h=25)
            cmds.button(label=u'\u8bb0\u5f55\u4f4d\u79fb\u65cb\u8f6c', c=lambda *args: self.objvalerecord('%s' % i), h=25)
            cmds.button(label=u'\u6062\u590d\u4f4d\u79fb\u65cb\u8f6c', c=lambda *args: self.objRecover('%s' % i), h=25)
            cmds.button(label=u'\u955c\u50cf\u4f4d\u79fb\u65cb\u8f6c', c=lambda *args: self.objmirror('%s' % i), h=25)
            cmds.setParent(cbd_layout)
            selPlusMinusbutName = selprefix + 'selPlusMinus' + str(i) + '_optionMenu'
            print (selPlusMinusbutName)
            jntSuffix_as = cmds.optionMenu(selPlusMinusbutName, h=25)
            cmds.menuItem(selPlusMinusbutName + '_menuItem1', label='+')
            cmds.menuItem(selPlusMinusbutName + '_menuItem2', label='-')
            cmds.menuItem(selPlusMinusbutName + '_menuItem3', label=u'&\u4ea4\u96c6')
            cmds.setParent(cbd_layout)
            if numCdrn > 0:
                print ('----------------', numCdrn)
                cmds.window(winName, e=True, h=(numCdrn + 2) * 25 + 70, w=450)
        if v == -1:
            childArray = cmds.columnLayout(cbd_layout, q=True, childArray=True)
            if childArray != None:
                cmds.deleteUI(childArray[-1])
                cmds.deleteUI(childArray[-2])
            cmds.window(winName, e=True, h=(numCdrn - 2) * 25 + 70, w=450)
        return

    def Load(self, Field):
        sels = cmds.ls(sl=True, fl=True)
        cmds.textFieldButtonGrp(Field, e=True, text=str(sels))
        return sels

    def selObjPM(self):
        selprefix = 'Jun'
        cbd_layout = selprefix + 'selPlusMinus_ColumnLayout'
        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        numCdrn = numCdrn / 2
        allObjs = []
        allplusMinus = []
        for i in range(numCdrn):
            cbdr_loadChannlAttr_tfg = selprefix + 'cbdr_loadChannlAttr' + str(i) + '_tfg'
            objs = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, q=True, text=True)
            selPlusMinusbutName = selprefix + 'selPlusMinus' + str(i) + '_optionMenu'
            plusMinus = cmds.optionMenu(selPlusMinusbutName, q=True, sl=True)
            objs = eval(objs)
            if i != 0:
                print (allplusMinus[-1])
                if allplusMinus[-1] == 1:
                    for obj in objs:
                        allObjs.append(obj)

                elif allplusMinus[-1] == 2:
                    for obj in objs:
                        if obj in allObjs:
                            allObjs.remove(obj)

                elif allplusMinus[-1] == 3:
                    allObjs = list(set(allObjs) & set(objs))
            else:
                allObjs = objs
            print (allObjs)
            print (objs)
            allplusMinus.append(plusMinus)

        cmds.select(allObjs)

    def selectTFobj(self, Field):
        TFobjs = cmds.textFieldButtonGrp(Field, q=True, text=True)
        cmds.select(eval(TFobjs))
        print (TFobjs)

    def objsTFArchive(self):
        archiveName = cmds.textField('archiveTF', q=True, text=True)
        selprefix = 'Jun'
        cbd_layout = selprefix + 'selPlusMinus_ColumnLayout'
        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        numCdrn = numCdrn / 2
        allObjs = []
        allplusMinus = []
        enumNames = ''
        for i in range(numCdrn):
            cbdr_loadChannlAttr_tfg = selprefix + 'cbdr_loadChannlAttr' + str(i) + '_tfg'
            objs = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, q=True, text=True)
            selPlusMinusbutName = selprefix + 'selPlusMinus' + str(i) + '_optionMenu'
            plusMinus = cmds.optionMenu(selPlusMinusbutName, q=True, sl=True)
            if plusMinus == 1:
                plusMinus = '+'
            elif plusMinus == 2:
                plusMinus = '-'
            enumNames = enumNames + objs + ':' + plusMinus + ':'

        lambert1Attrs = cmds.listAttr('lambert1', keyable=True)
        if archiveName in lambert1Attrs:
            cmds.deleteAttr('lambert1', attribute=archiveName)
        cmds.addAttr('lambert1', ln=archiveName, at='enum', en=enumNames, keyable=1)

    def restoreArchive(self):
        archiveName = cmds.textField('archiveTF', q=True, text=True)
        selprefix = 'Jun'
        enumNames = cmds.addAttr('lambert1.' + archiveName, q=True, en=True)
        enumNameSplits = enumNames.split(':')
        numCdrn1 = len(enumNames.split(':'))
        for i in range(numCdrn1 / 2):
            self.addButton(1)

        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        for i in range((numCdrn - numCdrn1) / 2):
            self.addButton(-1)

        for i in range(numCdrn1 / 2):
            cbdr_loadChannlAttr_tfg = selprefix + 'cbdr_loadChannlAttr' + str(i) + '_tfg'
            objs = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, e=True, text=enumNameSplits[i * 2])
            selPlusMinusbutName = selprefix + 'selPlusMinus' + str(i) + '_optionMenu'
            if enumNameSplits[i * 2 + 1] == '+':
                plusMinus = cmds.optionMenu(selPlusMinusbutName, e=True, sl=1)
            elif enumNameSplits[i * 2 + 1] == '-':
                plusMinus = cmds.optionMenu(selPlusMinusbutName, e=True, sl=2)

    def objvalerecord(self, i):
        sdks = cmds.ls(sl=True)
        r_sdklist = []
        l_sdk_tslist = []
        l_sdk_rslist = []
        for l_sdk in sdks:
            if 'L_' in l_sdk:
                r_sdk = l_sdk.replace('L_', 'R_')
            else:
                r_sdk = l_sdk
            l_sdk_ts = cmds.getAttr(l_sdk + '.t')[0]
            l_sdk_rs = cmds.getAttr(l_sdk + '.r')[0]
            r_sdklist.append(r_sdk)
            l_sdk_tslist.append(l_sdk_ts)
            l_sdk_rslist.append(l_sdk_rs)
            if cmds.objExists(r_sdk) == 0:
                cmds.warning(r_sdk, u'------\u4e0d\u5b58\u5728')

        lambert1Attrs = cmds.listAttr('lambert1', keyable=True)
        if 'r_sdklist' + str(i) in lambert1Attrs:
            cmds.deleteAttr('lambert1', attribute='sdklist' + str(i))
            cmds.deleteAttr('lambert1', attribute='r_sdklist' + str(i))
            cmds.deleteAttr('lambert1', attribute='l_sdk_tslist' + str(i))
            cmds.deleteAttr('lambert1', attribute='l_sdk_rslist' + str(i))
        cmds.addAttr('lambert1', ln='sdklist' + str(i), at='enum', en=str(sdks), keyable=1)
        cmds.addAttr('lambert1', ln='r_sdklist' + str(i), at='enum', en=str(r_sdklist), keyable=1)
        cmds.addAttr('lambert1', ln='l_sdk_tslist' + str(i), at='enum', en=str(l_sdk_tslist), keyable=1)
        cmds.addAttr('lambert1', ln='l_sdk_rslist' + str(i), at='enum', en=str(l_sdk_rslist), keyable=1)

    def objRecover(self, i):
        sdklist = eval(cmds.addAttr('lambert1.sdklist' + str(i), q=True, en=True))
        l_sdk_tslist = eval(cmds.addAttr('lambert1.' + 'l_sdk_tslist' + str(i), q=True, en=True))
        l_sdk_rslist = eval(cmds.addAttr('lambert1.' + 'l_sdk_rslist' + str(i), q=True, en=True))
        for i in range(len(sdklist)):
            sdk = sdklist[i]
            l_sdk_ts = l_sdk_tslist[i]
            l_sdk_rs = l_sdk_rslist[i]
            cmds.setAttr(sdk + '.t', l_sdk_ts[0], l_sdk_ts[1], l_sdk_ts[2])
            cmds.setAttr(sdk + '.r', l_sdk_rs[0], l_sdk_rs[1], l_sdk_rs[2])

        cmds.select(sdklist)

    def objmirror(self, i):
        r_sdklist = eval(cmds.addAttr('lambert1.r_sdklist' + str(i), q=True, en=True))
        l_sdk_tslist = eval(cmds.addAttr('lambert1.' + 'l_sdk_tslist' + str(i), q=True, en=True))
        l_sdk_rslist = eval(cmds.addAttr('lambert1.' + 'l_sdk_rslist' + str(i), q=True, en=True))
        for i in range(len(r_sdklist)):
            r_sdk = r_sdklist[i]
            l_sdk_ts = l_sdk_tslist[i]
            l_sdk_rs = l_sdk_rslist[i]
            cmds.setAttr(r_sdk + '.t', l_sdk_ts[0], l_sdk_ts[1], l_sdk_ts[2])
            cmds.setAttr(r_sdk + '.r', l_sdk_rs[0], l_sdk_rs[1], l_sdk_rs[2])

        cmds.select(r_sdklist)

    def x1(self):
        sels = cmds.ls(sl=True)
        r_jnts = []
        for sel in sels:
            r_jnt = 'R_' + sel[2:]
            if cmds.objExists(r_jnt) == True:
                r_jnts.append(r_jnt)
            else:
                print ('\xe5\xaf\xb9\xe5\xba\x94\xe7\x89\xa9\xe4\xbd\x93\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8---' + str(sel))

        cmds.select(r_jnts)