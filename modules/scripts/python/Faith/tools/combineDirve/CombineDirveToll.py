# coding:utf-8
import maya.cmds as cmds
import maya.mel as mel
import types, os

class CombineDirve(object):

    def __init__(self):
        pass

    def nodeCreate(self, Nodetype, name, attrDatadic):
        if cmds.objExists(name) == True:
            cmds.warning(name + '----is exists')
        node = cmds.createNode(Nodetype, name=name)
        for attr in attrDatadic:
            Data = attrDatadic.get(attr)
            cmds.setAttr(node + '.' + attr, Data)

        return node

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

    def createCombineDirve(self, dicts):
        """
        dicts = [{ ( ('locator1.translateY',(0,5)),('locator2.translateY',(0,5)),('locator3.translateY',(0,5)) ) : ('locator7.translateY',(0,5)) }]
        """
        sels = cmds.ls(sl=True)
        for dict in dicts:
            for drivers in dict:
                drivenData = dict.get(drivers)
                driven = drivenData[0]
                drivenNums = drivenData[1]
                driverLen = len(drivers)
                NodeConditions = []
                for x in range(driverLen):
                    driver = drivers[x][0]
                    driverNums = drivers[x][1]
                    if x == 1:
                        priorDriver = drivers[x - 1][0]
                        priordriverNums = drivers[x - 1][1]
                        print(drivenNums)
                        drivenNum0_str = str(drivenNums[0]).replace('-', '_N').replace('.', 'd')
                        drivenNum1_str = str(drivenNums[1]).replace('-', '_N').replace('.', 'd')
                        firstNodeCondition = self.nodeCreate('condition', driven.replace('.', '_') + str(x) + '_' + drivenNum0_str + '_' + drivenNum1_str + '_Condition', {'operation': 5})
                        self.setDrivenKey(driver, firstNodeCondition + '.firstTerm', driverNums, (0, 1), itt='linear', ott='linear')
                        self.setDrivenKey(priorDriver, firstNodeCondition + '.secondTerm', priordriverNums, (0, 1), itt='linear', ott='linear')
                        cmds.connectAttr(firstNodeCondition + '.firstTerm', firstNodeCondition + '.colorIfTrueR')
                        cmds.connectAttr(firstNodeCondition + '.secondTerm', firstNodeCondition + '.colorIfFalseR')
                        NodeConditions.append(firstNodeCondition)
                    elif x > 1:
                        endDriver = drivers[-1][0]
                        NodeCondition = self.nodeCreate('condition', driven.replace('.', '_') + str(x) + '_Condition', {'operation': 5})
                        self.setDrivenKey(driver, NodeCondition + '.firstTerm', driverNums, (0, 1), itt='linear', ott='linear')
                        cmds.connectAttr(NodeConditions[-1] + '.outColorR', NodeCondition + '.secondTerm')
                        cmds.connectAttr(NodeCondition + '.firstTerm', NodeCondition + '.colorIfTrueR')
                        cmds.connectAttr(NodeCondition + '.secondTerm', NodeCondition + '.colorIfFalseR')
                        NodeConditions.append(NodeCondition)

                self.setDrivenKey(NodeConditions[-1] + '.outColorR', driven, (0, 1), drivenNums, itt='linear', ott='linear')

        cmds.select(sels)