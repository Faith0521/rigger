# -*- coding: utf-8 -*-
from functools import partial
import maya.cmds as cmds
import Faith.tools.AddGrpTool.addGrp as addGrp
addGrp = addGrp.AddGrp()
cbdprefix = 'Jun'
grp_layout = cbdprefix + '_AddGrpWinLayout'
addGrpWin = cbdprefix + '_AddGrpWin'

class AddGrpWin:
    def win(self):
        global cbdprefix
        global grp_layout
        global addGrpWin
        AddGrpWintext = cbdprefix + ' AddGrp v2015/05/8'
        if cmds.window(addGrpWin, ex=True):
            cmds.deleteUI(addGrpWin)
        cmds.window(addGrpWin, t=AddGrpWintext)
        rotLayout = cmds.columnLayout(adj=True)
        cmds.text(label=' ', h=5)
        cmds.rowLayout(numberOfColumns=6)
        cmds.button(label='+', c=partial(self.addButton, 1, '', ''))
        cmds.button(label='--', c=partial(self.addButton, -1, '', ''))
        cmds.button(label='zero', c=partial(self.addButtonGrp, [''], ['_zero']))
        cmds.button(label='zero/con/sdk', c=partial(self.addButtonGrp, ['', '', ''], ['_zero', '_con', '_sdk']))
        cmds.button(label='zero/PH/SN', c=partial(self.addButtonGrp, ['', '', ''], ['_zero', '_PH', '_SN']))
        cmds.button(label='ctrl', c=partial(self.addButtonGrp, ['_jnt'], ['_ctrl']))
        cmds.setParent(rotLayout)
        cmds.separator(style='single', en=0)
        cmds.button('aa', l='Add Grp', c=partial(self.Generate))
        cmds.rowLayout(numberOfColumns=3, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l='addgrpRelativeTier:', align='right', width=100)
        cmds.radioCollection()
        cmds.radioButton('UP', label='UP', align='left', sl=True, w=80)
        cmds.radioButton('DN', label='DN', align='right')
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l='AddObjType:', align='right', width=100)
        cmds.radioCollection()
        cmds.radioButton('transformRadio', label='transform', align='left', sl=True, w=80)
        cmds.radioButton('jntRadio', label='jnt', align='right')
        cmds.setParent('..')
        cmds.columnLayout(grp_layout, adj=True)
        self.addButton(1, '', '_con')
        self.addButton(1, '', '_sdk')
        cmds.showWindow(addGrpWin)

    def addButton(self, v, beRestr, reStr, *args):
        if v == 1:
            numCdrn = cmds.columnLayout(grp_layout, q=True, numberOfChildren=True)
            row = cmds.rowLayout(numberOfColumns=3, p=grp_layout, columnAlign=(1, 'right'))
            cmds.text(l='Grp0' + str(numCdrn + 1) + ':', p=row, w=100)
            textFieldbe = cbdprefix + 'Grp0' + str(numCdrn) + '_beRestrtext'
            textFieldre = cbdprefix + 'Grp0' + str(numCdrn) + '_Restrtext'
            cmds.textField(textFieldbe, text=beRestr, w=60, p=row)
            cmds.textField(textFieldre, text=reStr, w=60, p=row)
            cmds.setParent(grp_layout)
        if v == -1:
            childArray = cmds.columnLayout(grp_layout, q=True, childArray=True)
            if childArray != None:
                cmds.deleteUI(childArray[-1])
        cmds.window(addGrpWin, e=True, h=100, w=100)
        return

    def delAllButton(self):
        numCdrn = cmds.columnLayout(grp_layout, q=True, numberOfChildren=True)
        i = numCdrn / 4

    def addButtonGrp(self, bereStrs, reStrs, *args):
        childArray = cmds.columnLayout(grp_layout, q=True, childArray=True)
        if childArray != None:
            cmds.deleteUI(childArray)
        for i in range(len(reStrs)):
            self.addButton(1, bereStrs[i], reStrs[i])

        return

    def Generate(self, *args):
        numCdrn = cmds.columnLayout(grp_layout, q=True, numberOfChildren=True)
        sels = cmds.ls(sl=True)
        beRestrs = []
        Restrs = []
        for i in range(numCdrn):
            textFieldbe = cbdprefix + 'Grp0' + str(i) + '_beRestrtext'
            textFieldre = cbdprefix + 'Grp0' + str(i) + '_Restrtext'
            beRestr = cmds.textField(textFieldbe, q=True, text=True)
            Restr = cmds.textField(textFieldre, q=True, text=True)
            beRestrs.append(beRestr)
            Restrs.append(Restr)

        topGrps = []
        if cmds.radioButton('UP', q=True, sl=True) == True:
            addgrpRelativeTier = 'Up'
        elif cmds.radioButton('DN', q=True, sl=True) == True:
            addgrpRelativeTier = 'Dn'
        for sel in sels:
            sel1 = sel.split('|')[-1]
            grps = []
            for i in range(len(Restrs)):
                if beRestr == '':
                    grp = sel1 + Restrs[i]
                    grps.append(grp)
                elif beRestr != '':
                    grp = sel1.replace(beRestrs[i], Restrs[i])
                    grps.append(grp)

            grp = addGrp.GrpAdd(sel, grps, addgrpRelativeTier)
            topGrp = grp[0][0]
            topGrps.append(topGrp)

        cmds.select(topGrps)