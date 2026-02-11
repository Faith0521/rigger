# coding:utf-8
from imp import reload
import maya.cmds as cmds
import maya.mel as mel
from . import CombineDirveToll as CBD
cbdprefix = 'Jun'
cbd_layout = cbdprefix + 'cbdv_dvrColumnLayout'

class JunCombinDirveUI:

    def __init__(self):
        pass

    def CBDwin(self):
        global cbdprefix
        winName = cbdprefix + 'combinDirveTool_win'
        if cmds.window(winName, ex=True):
            cmds.deleteUI(winName)
        runCmd = 'import %s as cmdrTool\ncmdrTool' % __name__
        cmds.window(winName, t=cbdprefix + ' Combin Dirve Tool v2015/04/17')
        scrollArea = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16, childResizable=True)
        rotLayout = cmds.columnLayout(adj=True)
        cmds.text(label=' ', h=5)
        cmds.textFieldButtonGrp(cbdprefix + 'cbdr_loadDvnChannlAttr_tfg', l='driven: ', text='', h=25, columnWidth3=[85, 200, 50], cl2=['center', 'left'], bl='<<Load', bc=lambda *args: self.Load('%scbdr_loadDvnChannlAttr_tfg' % cbdprefix))
        cmds.floatFieldGrp(cbdprefix + 'cbdr_setDvnAttrMix_tfg', l='start Value:', pre=4, v1=0.0)
        cmds.floatFieldGrp(cbdprefix + 'cbdr_setDvnAttrMax_tfg', l='finish Value:', pre=4, v1=1.0)
        cmds.separator(style='single', en=0)
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label='+', c=lambda *args: self.addButton(1))
        cmds.button(label='--', c=lambda *args: self.addButton(-1))
        cmds.setParent(rotLayout)
        cmds.separator(style='single', en=0)
        dvrLayout = cmds.columnLayout(cbdprefix + 'cbdv_dvrColumnLayout', adj=True)
        self.addButton(1)
        self.addButton(1)
        cmds.setParent(rotLayout)
        cmds.separator(style='single', en=0)
        cmds.button(l='Apply', c=lambda *args: self.Generate())
        cmds.showWindow(winName)

    def addButton(self, v):
        global cbd_layout
        winName = cbdprefix + 'combinDirveTool_win'
        if v == 1:
            numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
            i = numCdrn / 3
            cbdr_loadChannlAttr_tfg = cbdprefix + 'cbdr_loadChannlAttr' + str(i) + '_tfg'
            cbdr_setAttrMix_tfg = cbdprefix + 'cbdr_setAttrMix%s_tfg' % i
            cbdr_setAttrMax_tfg = cbdprefix + 'cbdr_setAttrMax%s_tfg' % i
            a = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, p=cbd_layout, l='driver: ', text='', h=25, columnWidth3=[85, 200, 50], cl2=['center', 'left'], bl='<<Load')
            print(a)
            cmds.textFieldButtonGrp(a, edit=1, bc=lambda *args: self.Load(a))
            cmds.floatFieldGrp(cbdr_setAttrMix_tfg, p=cbd_layout, l='start Value:', pre=4, v1=0.0)
            cmds.floatFieldGrp(cbdr_setAttrMax_tfg, p=cbd_layout, l='finish Value:', pre=4, v1=1.0)
        if v == -1:
            childArray = cmds.columnLayout(cbd_layout, q=True, childArray=True)
            if childArray != None:
                cmds.deleteUI(childArray[-1])
                cmds.deleteUI(childArray[-2])
                cmds.deleteUI(childArray[-3])
        cmds.window(winName, e=True, w=370)
        return

    def Load(self, Field):
        sels = cmds.ls(sl=True)
        if len(sels) != 1:
            cmds.error('please select one object')
        selectAttr = self.querySelectedAttr()
        longAttrList = selectAttr[1]
        if len(longAttrList) != 1:
            cmds.error('please select one Attribute')
        cmds.textFieldButtonGrp(Field, e=True, text=sels[0] + '.' + longAttrList[0])
        return sels[0] + '.' + longAttrList[0]

    @staticmethod
    def querySelectedAttr():
        """
        #--------------------------------------------------------------------------------
        get Selected attribute name form mainChannelBox
        #--------------------------------------------------------------------------------
        """
        shortAttrList = cmds.channelBox('mainChannelBox', q=True, sma=True)
        longAttrList = []
        if shortAttrList == None:
            shortAttrList = []
        else:
            for shortAttr in shortAttrList:
                longAttr = cmds.attributeName('.' + shortAttr, l=True)
                longAttrList.append(longAttr)

        return (shortAttrList, longAttrList)

    def Generate(self):
        """
        dicts1 = [{ ( ('locator1.translateY',(0,5)),('locator2.translateY',(0,5)),('locator3.translateY',(0,5)) ) : ('locator7.translateY',(0,5)) }]
        """
        numCdrn = cmds.columnLayout(cbd_layout, q=True, numberOfChildren=True)
        driverDataList = []
        for i in range(int(numCdrn / 3)):
            driverNums = []
            driverData = []
            cbdr_loadChannlAttr_tfg = cbdprefix + 'cbdr_loadChannlAttr%s_0_tfg' % i
            cbdr_setAttrMix_tfg = cbdprefix + 'cbdr_setAttrMix%s_0_tfg' % i
            cbdr_setAttrMax_tfg = cbdprefix + 'cbdr_setAttrMax%s_0_tfg' % i
            cbdr_loadChannlAttr = cmds.textFieldButtonGrp(cbdr_loadChannlAttr_tfg, q=True, text=True)
            cbdr_setAttrMix = cmds.floatFieldGrp(cbdr_setAttrMix_tfg, q=True, v1=True)
            cbdr_setAttrMax = cmds.floatFieldGrp(cbdr_setAttrMax_tfg, q=True, v1=True)
            driverNums.append(cbdr_setAttrMix)
            driverNums.append(cbdr_setAttrMax)
            driverData.append(cbdr_loadChannlAttr)
            driverNums = tuple(driverNums)
            driverData.append(driverNums)
            driverData = tuple(driverData)
            driverDataList.append(driverData)

        driverDatatuple = tuple(driverDataList)
        drivenNums = []
        drivenData = []
        cbdr_loadChannlAttr = cmds.textFieldButtonGrp(cbdprefix + 'cbdr_loadDvnChannlAttr_tfg', q=True, text=True)
        cbdr_setAttrMix = cmds.floatFieldGrp(cbdprefix + 'cbdr_setDvnAttrMix_tfg', q=True, v1=True)
        cbdr_setAttrMax = cmds.floatFieldGrp(cbdprefix + 'cbdr_setDvnAttrMax_tfg', q=True, v1=True)
        drivenNums.append(cbdr_setAttrMix)
        drivenNums.append(cbdr_setAttrMax)
        drivenData.append(cbdr_loadChannlAttr)
        drivenNums = tuple(drivenNums)
        drivenData.append(drivenNums)
        drivenDataTuple = tuple(drivenData)
        dicts = [{driverDatatuple: drivenDataTuple}]
        combineDirve = CBD.CombineDirve()
        combineDirve.createCombineDirve(dicts)