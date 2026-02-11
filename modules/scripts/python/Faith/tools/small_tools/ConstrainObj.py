# Embedded file name: E:/JunCmds/tool/ConstrainObj.py
r"""
import sys
sys.path.insert(0,r'E:\JunCmds  ool')
import ConstrainObj as ConstrainObj
reload(ConstrainObj)
constrainObj = ConstrainObj.ConstrainObj()
constrainObj.win()
"""
import maya.cmds as cmds
import maya.mel as mel
import sys


class ConstrainObj:

    def __init__(self):
        self.objPrefixTF = ''
        self.ObjSuffixTF = ''
        self.ObjPrefix_asSelect = 1
        self.ObjSuffix_asSelect = 1

    def win(self):
        ws = (150, 40, 80)
        UI = 'ConstrainObj'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        a = cmds.window(UI, t='Jun ConstrainObj')
        scrollArea = cmds.scrollLayout(horizontalScrollBarThickness=32, verticalScrollBarThickness=16,
                                       childResizable=True)
        child1 = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=6, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l=u'\u7ea6\u675f\u65b9\u5f0f:', align='right', width=80)
        cmds.radioCollection()
        self.constrainObjParentRB = cmds.checkBox('constrainObjParentRB', label='parent', value=1, w=60,
                                                  changeCommand=lambda *args: self.windowsControlEdit(
                                                      [self.pointRB, self.orientRB]))
        self.pointRB = cmds.checkBox('pointRB', label='point', value=0, w=60,
                                     changeCommand=lambda *args: self.windowsControlEdit([self.constrainObjParentRB]))
        self.orientRB = cmds.checkBox('orientRB', label='orient', value=0, w=60,
                                      changeCommand=lambda *args: self.windowsControlEdit([self.constrainObjParentRB]))
        self.scaleRB = cmds.checkBox('scaleRB', label='scale', value=0, w=60)
        print(self.constrainObjParentRB)
        cmds.setParent(child1)
        cmds.rowLayout(numberOfColumns=3, columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        cmds.text(l=u'maintain offset:', align='right', width=80)
        cmds.radioCollection()
        cmds.radioButton('yesRB', label='yes', align='left', sl=True, w=60)
        cmds.radioButton('noRB', label='no', align='right', w=60)
        cmds.setParent(child1)
        cmds.rowLayout(numberOfColumns=3, columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        cmds.text(l=u'\u5220\u9664\u539f\u5148\u7ea6\u675f:', align='right', width=80)
        cmds.radioCollection()
        cmds.radioButton('delConstrYesRB', label='yes', align='left', sl=True, w=60)
        cmds.radioButton('delConstrNoRB', label='no', align='right', w=60)
        cmds.setParent(child1)
        cmds.setParent('..')
        cmds.button(l=u'\u5220\u9664\u7ea6\u675f(\u9009\u62e9\u88ab\u7ea6\u675f\u7269\u4f53\u6267\u884c)',
                    c=lambda *args: self.delConstr1(), width=200, h=40)
        cmds.button(
            l=u'\u9009\u9009\u62e9\u7ea6\u675f\u7269\u4f53\u52a0\u9009\u88ab\u7ea6\u675f\u7269\u4f53\u8fd0\u884c',
            c=lambda *args: self.oneToMultipleConstraint2(), width=100, h=40)
        oneToMultiConFL = cmds.frameLayout(label=u'\u4e00\u5bf9\u591a\u7ea6\u675f', labelAlign='left', cl=0, cll=True,
                                           bgc=[0.3, 0.3, 0])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u8f7d\u5165\u7ea6\u675f\u7269\u4f53', c=lambda *args: self.loadObj(1, 'constrainObjTF'),
                    width=70, h=30)
        objAttr = cmds.textField('constrainObjTF', text=u'\u7ea6\u675f\u7269\u4f53', h=30, w=260)
        cmds.setParent(oneToMultiConFL)
        cmds.button(l=u'\u9009\u62e9\u88ab\u7ea6\u675f\u7269\u4f53\u8fd0\u884c',
                    c=lambda *args: self.oneToMultipleConstraint(), width=100, h=30)
        cmds.setParent('..')
        oneToOneConFL = cmds.frameLayout(label=u'\u6839\u636e\u7269\u4f53\u547d\u540d\u4e00\u5bf9\u4e00\u7ea6\u675f',
                                         labelAlign='left', cl=True, cll=True, bgc=[0.3, 0.3, 0])
        row2 = cmds.rowLayout(numberOfColumns=6)
        cmds.text(l='objPrefix:')
        jntPrefix_as = cmds.optionMenu('ObjPrefix_as')
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('objPrefixTF', text=self.objPrefixTF, h=30)
        cmds.text(l='ObjSuffix:')
        jntSuffix_as = cmds.optionMenu('ObjSuffix_as')
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('ObjSuffixTF', text=self.ObjSuffixTF, h=30)
        cmds.setParent(oneToOneConFL)
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(l='replace old str', w=102)
        cmds.textField('replaceOldstrTF', text=u'_jnt', h=30)
        cmds.text(l='replace new str', w=105)
        cmds.textField('replaceNewstrTF', text=u'_ctrl', h=30)
        cmds.setParent(oneToOneConFL)
        cmds.button(l=u'\u4e00\u5bf9\u4e00\u7ea6\u675f(\u9009\u62e9\u88ab\u7ea6\u675f\u7269\u4f53)',
                    c=lambda *args: self.oneToOneConstraint(), width=100, h=40)
        cmds.setParent('..')
        oneToOneConSelListFL = cmds.frameLayout(
            label=u'\u6839\u636e\u5217\u8868\u987a\u5e8f\u4e00\u5bf9\u4e00\u7ea6\u675f', labelAlign='left', cl=True,
            cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u7ea6\u675f\u7269\u4f53\u5217\u8868:', c=lambda *args: self.loadObj('', 'constrObjsTF'),
                    width=90, h=30)
        cmds.textField(u'constrObjsTF', text=u'', h=30, w=300)
        cmds.setParent(oneToOneConSelListFL)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u88ab\u7ea6\u675f\u7269\u4f53\u5217\u8868:',
                    c=lambda *args: self.loadObj('', 'beconstrObjsTF'), width=90, h=30)
        cmds.textField(u'beconstrObjsTF', text=u'', h=30, w=300)
        cmds.setParent(oneToOneConSelListFL)
        cmds.button(l=u'\u4e00\u5bf9\u4e00\u7ea6\u675f(\u6309\u7167\u5217\u8868\u987a\u5e8f)',
                    c=lambda *args: self.oneToOneConstraintSelectList(), width=100, h=40)
        cmds.setParent('..')
        oneToMultiConAttrFL = cmds.frameLayout(label=u'\u4e00\u5c5e\u6027\u8fde\u591a\u5c5e\u6027',
                                               ann=u'\u529f\u80fd:\u2460\u4e2a\u7269\u4f53\u7684\u2460\u4e2a\u5c5e\u6027\u8fde\u63a5\u591a\u4e2a\u7269\u4f53\u591a\u4e2a\u5c5e\u6027\n\u8f7d\u5165\u2460\u4e2a\u7269\u4f53\u7684\u2460\u4e2a\u8f93\u51fa.\u5c5e\u6027\n\u8f7d\u5165\u88ab\u8fde\u63a5\u7269\u4f53\u7684\u5c5e\u6027\n\u9009\u4e2d\u88ab\u8fde\u63a5\u7269\u4f53\u8fd0\u884c',
                                               labelAlign='left', cl=True, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        loadconAttrbut = cmds.button(l=u'\u4e00\u4e2a\u7269\u4f53\u7684\u4e00\u4e2a\u8f93\u51fa.\u5c5e\u6027',
                                     c=lambda *args: self.LoadAttr(1, self.oneConAttrTF, 'objattr'), h=30, w=100)
        self.oneConAttrTF = cmds.textField('oneConAttrTF', text=u'\u8f93\u51fa\u5c5e\u6027(Outputs)', h=30)
        cmds.setParent(oneToMultiConAttrFL)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u88ab\u8fde\u63a5\u5c5e\u6027',
                    c=lambda *args: self.LoadAttr('', 'oneToMultiInputsAttrTF', 'attr'), h=30, w=100)
        oneToMultiInputsAttrTF = cmds.textField('oneToMultiInputsAttrTF',
                                                text=u'\u88ab\u8fde\u63a5\u5c5e\u6027(Inputs)', h=30)
        cmds.setParent(oneToMultiConAttrFL)
        cmds.button(l=u'\u9009\u4e2d\u88ab\u8fde\u63a5\u7269\u4f53', c=lambda *args: self.oneToMultiAttrCon(),
                    width=100, h=30)
        cmds.setParent('..')
        MultiToMultiConAttrFL = cmds.frameLayout(label=u'\u591a\u5c5e\u6027\u8fde\u591a\u5c5e\u6027',
                                                 ann=u'\u2460\u4e2a\u7269\u4f53\u7684\u5c5e\u6027\u8fde\u63a5\u5176\u4ed6\u7269\u4f53\u7684\u5c5e\u6027 \u4f8b\uff1a\u2460\u4e2a\u7269\u4f53\u7684\u7f29\u653e\u8fde\u63a5\u5176\u4ed6\u7269\u4f53\u7684\u7f29\u653e\n\u8f7d\u5165\u2460\u4e2a\u7269\u4f53\u7684\u8f93\u51fa\u5c5e\u6027\n\u8f7d\u5165\u88ab\u8fde\u63a5\u5c5e\u6027\n\u8f93\u51fa\u5c5e\u6027\u548c\u88ab\u8fde\u63a5\u5c5e\u6027\u6570\u91cf\u8981\u4e00\u81f4\n\u9009\u4e2d\u88ab\u8fde\u63a5\u7269\u4f53\u8fd0\u884c',
                                                 labelAlign='left', cl=True, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        loadconAttrbut = cmds.button(l=u'\u4e00\u4e2a\u7269\u4f53\u7684\u591a\u4e2a\u8f93\u51fa.\u5c5e\u6027',
                                     c=lambda *args: self.LoadAttr('', 'multiConAttrTF', 'objattr.attr'), h=30, w=100)
        multiConAttrTF = cmds.textField('multiConAttrTF', text=u'\u8f93\u51fa\u5c5e\u6027(Outputs)', h=30)
        cmds.setParent(MultiToMultiConAttrFL)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u88ab\u8fde\u63a5\u5c5e\u6027',
                    c=lambda *args: self.LoadAttr('', 'MultiToMultiInputsAttrTF', 'attr'), h=30, w=100)
        MultiToMultiInputsAttrTF = cmds.textField('MultiToMultiInputsAttrTF',
                                                  text=u'\u88ab\u8fde\u63a5\u5c5e\u6027(Inputs)', h=30)
        cmds.setParent(MultiToMultiConAttrFL)
        cmds.button(l=u'\u9009\u4e2d\u88ab\u8fde\u63a5\u7269\u4f53', c=lambda *args: self.MultiToMultiAttrCon(),
                    width=100, h=30)
        cmds.setParent('..')
        oneToOneConAttrFL = cmds.frameLayout(label=u'\u7269\u4f53\u4e00\u5bf9\u4e00\u8fde\u63a5\u5c5e\u6027',
                                             ann=u'\u529f\u80fd\uff1a\u6839\u636e\u7269\u4f53\u547d\u540d\u2460\u5bf9\u2460\u5c5e\u6027\u8fde\u63a5\n\u8f7d\u5165\u88ab\u8fde\u63a5.\u5c5e\u6027\n\u5206\u6790\u8f93\u51fa\u5c5e\u6027\u7269\u4f53\u548c\u88ab\u8fde\u63a5\u7269\u4f53\u7684\u547d\u540d\u5dee\u522b\n\u5728UI\u4e2d\u586b\u5199\u597d\u52a0\u51cf\u524d\u540e\u7f00\u7684\u6216\u9700\u8981\u66ff\u6362\u7684\u5b57\u7b26\n\u9009\u4e2d\u88ab\u8fde\u63a5\u7269\u4f53\u8fd0\u884c',
                                             labelAlign='left', cl=True, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0)])
        cmds.button(l=u'\u8f7d\u5165\u88ab\u8fde\u63a5.\u5c5e\u6027',
                    c=lambda *args: self.LoadAttr('', 'oneToOneInputsAttrTF', 'attr'), h=30, w=100)
        oneToOneInputsAttrTF = cmds.textField('oneToOneInputsAttrTF', text=u'\u88ab\u8fde\u63a5\u5c5e\u6027', h=30)
        cmds.setParent(oneToOneConAttrFL)
        row2 = cmds.rowLayout(numberOfColumns=6)
        cmds.text(l='objPrefix:')
        jntPrefix_as = cmds.optionMenu('ObjPrefix_as1')
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('objPrefixTF1', text=self.objPrefixTF, h=30)
        cmds.text(l='ObjSuffix:')
        jntSuffix_as = cmds.optionMenu('ObjSuffix_as1')
        cmds.menuItem(label='+')
        cmds.menuItem(label='-')
        cmds.textField('ObjSuffixTF1', text=self.ObjSuffixTF, h=30)
        cmds.setParent(oneToOneConAttrFL)
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(l='replace old str', w=102)
        cmds.textField('replaceOldstrTF1', text=u'', h=30)
        cmds.text(l='replace new str', w=105)
        cmds.textField('replaceNewstrTF1', text=u'', h=30)
        cmds.setParent(oneToOneConAttrFL)
        cmds.button(
            l=u'\u7269\u4f53\u4e00\u5bf9\u4e00\u5c5e\u6027\u8fde\u63a5(\u9009\u62e9\u88ab\u8fde\u63a5\u7269\u4f53)',
            c=lambda *args: self.oneToOneConAttr(), width=100, h=40)
        cmds.setParent('..')
        cmds.separator(style='in')
        cmds.showWindow()
        cmds.optionMenu('ObjPrefix_as', e=True, sl=self.ObjPrefix_asSelect)
        cmds.optionMenu('ObjSuffix_as', e=True, sl=self.ObjSuffix_asSelect)

    def windowsControlEdit(self, windowsControlNames):
        for windowsControlName in windowsControlNames:
            cmds.checkBox(windowsControlName, e=True, value=0)

    def loadObj(self, loadnum, tfName):
        sels = cmds.ls(sl=True)
        if len(sels) == loadnum:
            if loadnum > 1:
                cmds.textField(tfName, e=True, text=str(sels[:loadnum]))
            elif loadnum == 1:
                cmds.textField(tfName, e=True, text=sels[0])
        elif loadnum == '':
            cmds.textField(tfName, e=True, text=str(sels))
        else:
            cmds.warning(u'\u8bf7\u9009\u62e9' + str(loadnum) + u'\u4e2a\u7269\u4f53')

    def LoadAttr(self, loadnum, tfName, attr_OR_objAttr):
        sels = cmds.ls(sl=True)
        sel = sels[0]
        selectAttr = self.querySelectedAttr()
        longAttrList = selectAttr[1]
        if len(longAttrList) == loadnum:
            if loadnum > 1:
                obj_attrs = []
                for attr in longAttrList[:loadnum]:
                    if attr_OR_objAttr == 'objattr':
                        obj_attrs.append(sel + '.' + attr)
                    elif attr_OR_objAttr == 'attr':
                        obj_attrs.append(attr)

                cmds.textField(tfName, e=True, text=str(obj_attrs))
            elif loadnum == 1:
                obj_attrs = []
                attr = longAttrList[0]
                if attr_OR_objAttr == 'objattr':
                    obj_attrs.append(sel + '.' + attr)
                elif attr_OR_objAttr == 'attr':
                    obj_attrs.append(attr)
                cmds.textField(tfName, e=True, text=obj_attrs[0])
        elif loadnum == '':
            obj_attrs = []
            for attr in longAttrList:
                if attr_OR_objAttr == 'objattr':
                    obj_attrs.append(sel + '.' + attr)
                elif attr_OR_objAttr == 'attr':
                    obj_attrs.append(attr)
                elif attr_OR_objAttr == 'objattr.attr':
                    obj_attrs.append(attr)

            if attr_OR_objAttr == 'objattr.attr':
                obj_attrs = sel + '.' + str(obj_attrs)
            cmds.textField(tfName, e=True, text=str(obj_attrs))
        else:
            cmds.error('please select ' + str(loadnum) + ' attr')

    def querySelectedAttr(self):
        shortAttrList = cmds.channelBox('mainChannelBox', q=True, sma=True)
        longAttrList = []
        if shortAttrList == None:
            shortAttrList = []
        else:
            for shortAttr in shortAttrList:
                longAttr = cmds.attributeName('.' + shortAttr, l=True)
                longAttrList.append(longAttr)

        return (shortAttrList, longAttrList)

    def oneToMultipleConstraint(self):
        sels = cmds.ls(sl=True)
        conObj = cmds.textField('constrainObjTF', q=True, text=True)
        for beconObj in sels:
            self.creatrConstraint(conObj, beconObj)

    def oneToMultipleConstraint2(self):
        sels = cmds.ls(sl=True)
        conObj = sels[0]
        for beconObj in sels[1:]:
            self.creatrConstraint(conObj, beconObj)

    def creatrConstraint(self, conObj, beconObj):
        maintainoffset = cmds.radioButton('yesRB', q=True, sl=True)
        if cmds.checkBox(self.constrainObjParentRB, q=True, value=True) == True:
            if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                self.delConstr(beconObj, 'parentConstraint')
            cmds.parentConstraint(conObj, beconObj, mo=maintainoffset)
        if cmds.checkBox(self.pointRB, q=True, value=True) == True:
            if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                self.delConstr(beconObj, 'pointConstraint')
            cmds.pointConstraint(conObj, beconObj, mo=maintainoffset)
        if cmds.checkBox(self.orientRB, q=True, value=True) == True:
            if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                self.delConstr(beconObj, 'orientConstraint')
            cmds.orientConstraint(conObj, beconObj, mo=maintainoffset)
        if cmds.checkBox(self.scaleRB, q=True, value=True) == True:
            if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                self.delConstr(beconObj, 'scaleConstraint')
            cmds.scaleConstraint(conObj, beconObj, mo=maintainoffset)

    def oneToOneConstraint(self):
        sels = cmds.ls(sl=True)
        ObjPrefix = cmds.textField('objPrefixTF', q=True, text=True)
        ObjSuffix = cmds.textField('ObjSuffixTF', q=True, text=True)
        ObjPrefixAndSub = cmds.optionMenu('ObjPrefix_as', q=True, sl=True)
        ObjSuffixAndSub = cmds.optionMenu('ObjSuffix_as', q=True, sl=True)
        replaceOldstr = cmds.textField('replaceOldstrTF', q=True, text=True)
        replaceNewstr = cmds.textField('replaceNewstrTF', q=True, text=True)
        objs = self.strEdit(sels, ObjPrefix, ObjSuffix, ObjPrefixAndSub, ObjSuffixAndSub, replaceOldstr, replaceNewstr)
        conObjs = objs[0]
        beconObjs = objs[1]
        for i in range(len(conObjs)):
            conObj = conObjs[i]
            beconObj = beconObjs[i]
            self.creatrConstraint(conObj, beconObj)

        sys.stderr.write('# ------ creatrConstraint is ok')

    def oneToOneConstraintSelectList(self):
        conObjs = eval(cmds.textField(u'constrObjsTF', q=True, text=True))
        beconObjs = eval(cmds.textField(u'beconstrObjsTF', q=True, text=True))
        for i in range(len(conObjs)):
            conObj = conObjs[i]
            beconObj = beconObjs[i]
            self.creatrConstraint(conObj, beconObj)

        sys.stderr.write('# ------ creatrConstraint is ok')

    def oneToMultiAttrCon(self):
        sels = cmds.ls(sl=True)
        conAttr = cmds.textField(self.oneConAttrTF, q=True, text=True)
        inputsAttrs = cmds.textField('oneToMultiInputsAttrTF', q=True, text=True)
        beinputsAttrs = []
        beObjs = []
        for sel in sels:
            for inputsAttr in eval(inputsAttrs):
                print(inputsAttr)
                nodePartCons = cmds.listConnections(sel + '.' + inputsAttr, scn=True, destination=False)
                if nodePartCons != None:
                    beinputsAttrs.append(sel + '.' + inputsAttr)
                    beObjs.append(sel)

        if beinputsAttrs == []:
            for sel in sels:
                for inputsAttr in eval(inputsAttrs):
                    cmds.connectAttr(conAttr, sel + '.' + inputsAttr, f=True)

        else:
            cmds.select(beObjs)
            cmds.warning(u'\u6709\u5c5e\u6027\u5df2\u7ecf\u88ab\u8fde\u63a5---' + str(beinputsAttrs))
        return

    def oneToOneConAttr_old(self):
        conAttrs = eval(cmds.textField('oneToOneInputsAttrTF', q=True, text=True))
        outputsAttrObjs = eval(cmds.textField('outputsAttrObjTF', q=True, text=True))
        inputsAttrObjs = eval(cmds.textField('inputsAttrObjTF', q=True, text=True))
        if len(outputsAttrObjs) != len(inputsAttrObjs):
            cmds.error(u'\u8f93\u51fa\u548c\u8f93\u5165\u7269\u4f53\u6570\u91cf\u4e0d\u4e00\u81f4')
        else:
            objNum = len(inputsAttrObjs)
        for attr in conAttrs:
            for i in range(objNum):
                outputsAttrObj = outputsAttrObjs[i]
                inputsAttrObj = inputsAttrObjs[i]
                if i == 0:
                    print(outputsAttrObj)
                    print(inputsAttrObj)
                cmds.connectAttr(outputsAttrObj + '.' + attr, inputsAttrObj + '.' + attr)

    def MultiToMultiAttrCon(self):
        inputObjs = cmds.ls(sl=True)
        outputObj = cmds.textField('multiConAttrTF', q=True, text=True).split('.')[0]
        multiConAttrs = eval(cmds.textField('multiConAttrTF', q=True, text=True).split('.')[-1])
        MultiToMultiInputsAttrs = eval(cmds.textField('MultiToMultiInputsAttrTF', q=True, text=True))
        if len(multiConAttrs) == len(MultiToMultiInputsAttrs):
            for i in range(len(multiConAttrs)):
                multiConAttr = multiConAttrs[i]
                MultiToMultiInputsAttr = MultiToMultiInputsAttrs[i]
                for inputObj in inputObjs:
                    cmds.connectAttr(outputObj + '.' + multiConAttr, inputObj + '.' + MultiToMultiInputsAttr)

        else:
            cmds.error(u'\u8f93\u51fa\u5c5e\u6027\u548c\u88ab\u8fde\u63a5\u5c5e\u6027\u6570\u91cf\u4e0d\u4e00\u81f4')

    def oneToOneConAttr(self):
        replaceStrOldObjs = cmds.ls(sl=True)
        attrs = eval(cmds.textField('oneToOneInputsAttrTF', q=True, text=True))
        ObjPrefix = cmds.textField('objPrefixTF1', q=True, text=True)
        ObjSuffix = cmds.textField('ObjSuffixTF1', q=True, text=True)
        ObjPrefixAndSub = cmds.optionMenu('ObjPrefix_as1', q=True, sl=True)
        ObjSuffixAndSub = cmds.optionMenu('ObjSuffix_as1', q=True, sl=True)
        replaceOldstr = cmds.textField('replaceOldstrTF1', q=True, text=True)
        replaceNewstr = cmds.textField('replaceNewstrTF1', q=True, text=True)
        objs = self.strEdit(replaceStrOldObjs, ObjPrefix, ObjSuffix, ObjPrefixAndSub, ObjSuffixAndSub, replaceOldstr,
                            replaceNewstr)
        conObjs = objs[0]
        beconObjs = objs[1]
        for i in range(len(conObjs)):
            outputsAttrObj = conObjs[i]
            inputsAttrObj = beconObjs[i]
            for attr in attrs:
                cmds.connectAttr(outputsAttrObj + '.' + attr, inputsAttrObj + '.' + attr)

    def strEdit(self, replaceStrOldObjs, ObjPrefix, ObjSuffix, ObjPrefixAndSub, ObjSuffixAndSub, replaceOldstr,
                replaceNewstr):
        replaceStrNewObjs = []
        for replaceStrOldObj in replaceStrOldObjs:
            replaceStrNewObj = replaceStrOldObj.replace(replaceOldstr, replaceNewstr)
            if ObjPrefixAndSub == 1:
                replaceStrNewObj = ObjPrefix + replaceStrNewObj
            elif ObjPrefixAndSub == 2:
                replaceStrNewObj = replaceStrNewObj[len(ObjPrefix):]
            if ObjSuffixAndSub == 1:
                replaceStrNewObj = replaceStrNewObj + ObjSuffix
            elif ObjSuffixAndSub == 2:
                if len(ObjSuffix) == 0:
                    pass
                else:
                    replaceStrNewObj = replaceStrNewObj[:-len(ObjSuffix)]
            if cmds.objExists(replaceStrNewObj) != True:
                cmds.error(u'##\u66ff\u6362\u5b57\u7b26\u65b0\u7269\u4f53\u4e0d\u5b58\u5728------' + replaceStrNewObj,
                           u'##\u5bf9\u5e94\u7684\u9009\u62e9\u7269\u4f53---' + replaceStrOldObj)
            replaceStrNewObjs.append(replaceStrNewObj)

        sys.stderr.write('#--------is ok')
        print(replaceStrNewObjs)
        return (replaceStrNewObjs, replaceStrOldObjs)

    def delConstr(self, obj, constrType):
        ads = cmds.listRelatives(obj, c=True, f=True)
        if cmds.ls(ads, type=constrType) != []:
            cmds.delete(cmds.ls(ads, type=constrType))

    def delConstr1(self):
        sels = cmds.ls(sl=True)
        for beconObj in sels:
            if cmds.checkBox(self.constrainObjParentRB, q=True, value=True) == True:
                if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                    self.delConstr(beconObj, 'parentConstraint')
            if cmds.checkBox(self.pointRB, q=True, value=True) == True:
                if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                    self.delConstr(beconObj, 'pointConstraint')
            if cmds.checkBox(self.orientRB, q=True, value=True) == True:
                if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                    self.delConstr(beconObj, 'orientConstraint')
            if cmds.checkBox(self.scaleRB, q=True, value=True) == True:
                if cmds.radioButton('delConstrYesRB', q=True, sl=True) == True:
                    self.delConstr(beconObj, 'scaleConstraint')
