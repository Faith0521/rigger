# Embedded file name: E:/JunCmds/tool/AddObjSin.py
r"""
import sys
sys.path.insert(0,r'E:\JunCmds  ool')
import AddObjSin as AddObjSin
reload(AddObjSin)
aos = AddObjSin.AddObjSin()
aos.win()
"""
import maya.cmds as cmds
import maya.mel as mel
import sys
from ...maya_utils import node_utils


class AddObjSin:

    def __init__(self):
        pass

    def win(self):
        UI = 'AddObjSin'
        if cmds.window(UI, exists=True):
            cmds.deleteUI(UI)
        a = cmds.window(UI, t='Jun AddObjSin')
        child1 = cmds.columnLayout(adjustableColumn=True)
        objAttr = cmds.textField('AddattrObj', text='AddattrObj', h=30)
        cmds.button(l=u'\u8f7d\u5165\u6dfb\u52a0\u5c5e\u6027\u7269\u4f53', c=lambda *args: self.loadObj(), width=100,
                    h=30)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=4, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l=u'sin\u8f74\u5411:', align='right', width=50)
        cmds.radioCollection()
        cmds.radioButton('Trb', label='translate', align='left', sl=True, w=60)
        cmds.radioButton('Rrb', label='rotate', align='right', w=60)
        cmds.radioButton('Srb', label='scale', align='right', w=60)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=4, columnAttach=[(1, 'left', 0), (2, 'left', 0), (3, 'right', 0)])
        cmds.text(l=u'sin\u8f74\u5411:', align='right', width=50)
        cmds.radioCollection()
        cmds.radioButton('Xrb', label='X', align='left', sl=True, w=60)
        cmds.radioButton('Yrb', label='Y', align='right', w=60)
        cmds.radioButton('Zrb', label='Z', align='right', w=60)
        cmds.setParent('..')
        cmds.button(l=u'\u9009\u62e9sin\u7269\u4f53\u521b\u5efa(\u4ece\u6839\u90e8\u5f80\u5934\u90e8\u9009\u62e9)',
                    c=lambda *args: self.CreateSine1(), width=100, h=30)
        cmds.showWindow()

    def loadObj(self):
        sels = cmds.ls(sl=True)
        if len(sels) == 1:
            cmds.textField('AddattrObj', e=True, text=sels[0])
        else:
            cmds.warning(str(sels), u'---\u9009\u62e9\u552f\u4e00\u7269\u4f53')

    def CreateSine1(self):
        tailName = cmds.textField('AddattrObj', q=True, text=True)
        addAttrObj = cmds.textField('AddattrObj', q=True, text=True)
        if cmds.radioButton('Trb', q=True, sl=True):
            Axial1 = 'translate'
        elif cmds.radioButton('Rrb', q=True, sl=True):
            Axial1 = 'rotate'
        elif cmds.radioButton('Srb', q=True, sl=True):
            Axial1 = 'scale'
        if cmds.radioButton('Xrb', q=True, sl=True):
            Axial2 = 'X'
        elif cmds.radioButton('Yrb', q=True, sl=True):
            Axial2 = 'Y'
        elif cmds.radioButton('Zrb', q=True, sl=True):
            Axial2 = 'Z'
        Axial = Axial1 + Axial2
        self.CreateSine(tailName, addAttrObj, Axial)

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

        num = len(driverNums)
        for i in range(num):
            animCv = cmds.setDrivenKeyframe(driven, currentDriver=driver, driverValue=driverNums[i], v=drivenNums[i],
                                            itt=itt, ott=ott)

    def CreateSine(self, tailName, addAttrObj, Axial):
        objList = cmds.ls(sl=True)
        sinJntNum = len(objList)
        AttrPrefix = Axial[0] + Axial[-1]
        waveAttName = '____________' + AttrPrefix
        EnumName = AttrPrefix + '_wave'
        waveAttAdd = cmds.addAttr(addAttrObj, ln=waveAttName, at='enum', en=EnumName)
        waveAttSet = cmds.setAttr(addAttrObj + '.' + waveAttName, e=True, keyable=True)
        waveAtt = addAttrObj + '.' + waveAttName
        cmds.setAttr(waveAtt, lock=True)
        EnvelopeAttName = AttrPrefix + '_Envelope'
        EnvelopeAttAdd = cmds.addAttr(addAttrObj, ln=EnvelopeAttName, at='double', min=0, max=1, dv=0)
        EnvelopeAttSet = cmds.setAttr(addAttrObj + '.' + EnvelopeAttName, 0, e=True, keyable=True)
        Envelope = addAttrObj + '.' + EnvelopeAttName
        AmplitudeAttName = AttrPrefix + '_Amplitude'
        AmplitudeAttAdd = cmds.addAttr(addAttrObj, ln=AmplitudeAttName, at='double', dv=5)
        AmplitudeAttSet = cmds.setAttr(addAttrObj + '.' + AmplitudeAttName, 5, e=True, keyable=True)
        Amplitude = addAttrObj + '.' + AmplitudeAttName
        WavelengthAttName = AttrPrefix + '_Wavelength'
        WavelengthAttAdd = cmds.addAttr(addAttrObj, ln=WavelengthAttName, at='double', dv=10)
        WavelengthAttSet = cmds.setAttr(addAttrObj + '.' + WavelengthAttName, 10, e=True, keyable=True)
        Wavelength = addAttrObj + '.' + WavelengthAttName
        WaveFollowAttName = AttrPrefix + '_WaveFollow'
        WaveFollowAttAdd = cmds.addAttr(addAttrObj, ln=WaveFollowAttName, at='double', dv=0)
        WaveFollowAttSet = cmds.setAttr(addAttrObj + '.' + WaveFollowAttName, 0, e=True, keyable=True)
        WaveFollow = addAttrObj + '.' + WaveFollowAttName
        StartingPositionAttName = AttrPrefix + '_StartingPosition'
        StartingPositionAttAdd = cmds.addAttr(addAttrObj, ln=StartingPositionAttName, at='double', min=0, max=sinJntNum,
                                              dv=0)
        StartingPositionAttSet = cmds.setAttr(addAttrObj + '.' + StartingPositionAttName, 0, e=True, keyable=True)
        StartingPosition = addAttrObj + '.' + StartingPositionAttName
        StartingreversalAttName = AttrPrefix + '_reversal'
        StartingreversalAttAdd = cmds.addAttr(addAttrObj, ln=StartingreversalAttName, at='double', min=-1, max=1, dv=1,
                                              keyable=True)
        Startingreversal = addAttrObj + '.' + StartingreversalAttName
        objNum = len(objList)
        if objNum == 1:
            averageNum = 1
        else:
            averageNum = 1.0 / (objNum - 1)
        expressionStr = ''
        for x in range(objNum):
            StartingPosition_PMA01 = cmds.shadingNode('plusMinusAverage', asUtility=True,
                                                      name=tailName + '_' + Axial + '_StartingPosition0' + str(
                                                          x) + '_PMA01')
            cmds.setAttr(StartingPosition_PMA01 + '.operation', 1)
            cmds.setAttr(StartingPosition_PMA01 + '.input2D[0].input2Dx', objNum - 1 - x)
            cmds.connectAttr(StartingPosition, StartingPosition_PMA01 + '.input2D[1].input2Dx')
            driver = Startingreversal
            driven = StartingPosition_PMA01 + '.input2D[0].input2Dx'
            itt = 'linear'
            ott = 'linear'
            driverNums = [1, -1]
            drivenNums = [objNum - 1 - x, x]
            self.setDrivenKey(driver, driven, driverNums, drivenNums, itt, ott)
            StartingPosition_SR = cmds.shadingNode('setRange', asUtility=True,
                                                   name=tailName + '_' + Axial + '_StartingPosition0' + str(
                                                       x) + '_setRange')
            cmds.setAttr(StartingPosition_SR + '.maxX', 1)
            cmds.setAttr(StartingPosition_SR + '.oldMaxX', objNum)
            cmds.connectAttr(StartingPosition_PMA01 + '.output2Dx', StartingPosition_SR + '.valueX')
            StartingPosition_PMA02 = cmds.shadingNode('plusMinusAverage', asUtility=True,
                                                      name=tailName + '_' + Axial + '_StartingPosition0' + str(
                                                          x) + '_PMA02')
            cmds.setAttr(StartingPosition_PMA02 + '.operation', 2)
            cmds.setAttr(StartingPosition_PMA02 + '.input2D[0].input2Dx', 1)
            cmds.connectAttr(StartingPosition_SR + '.outValueX', StartingPosition_PMA02 + '.input2D[1].input2Dx')
            Envelope_MD = cmds.shadingNode('multiplyDivide', asUtility=True,
                                           name=tailName + '_' + Axial + '_Envelope0' + str(x) + '_MD')
            cmds.connectAttr(Envelope, Envelope_MD + '.input1X')
            cmds.connectAttr(StartingPosition_PMA02 + '.output2Dx', Envelope_MD + '.input2X')
            Amplitude_MD = cmds.shadingNode('multiplyDivide', asUtility=True,
                                            name=tailName + '_' + Axial + '_Amplitude0' + str(x) + '_MD')
            cmds.connectAttr(Amplitude, Amplitude_MD + '.input1X')
            cmds.connectAttr(Envelope_MD + '.outputX', Amplitude_MD + '.input2X')
            result_MD = cmds.shadingNode('multiplyDivide', asUtility=True,
                                         name=tailName + '_' + Axial + '_result0' + str(x) + '_MD')
            cmds.connectAttr(Amplitude_MD + '.outputX', result_MD + '.input1X')
            cmds.connectAttr(result_MD + '.outputX', objList[x] + '.' + Axial)
            Wavelength_MD = cmds.shadingNode('multiplyDivide', asUtility=True,
                                             name=tailName + '_' + Axial + '_Wavelength0' + str(x) + '_MD')
            cmds.connectAttr(Wavelength, Wavelength_MD + '.input1.input1X')
            WavelengthMulriple = averageNum * x
            cmds.setAttr(Wavelength_MD + '.input2X', WavelengthMulriple)
            WaveFollow_MD = cmds.shadingNode('multiplyDivide', asUtility=True,
                                             name=tailName + '_' + Axial + '_WaveFollow0' + str(x) + '_MD')
            cmds.connectAttr(WaveFollow, WaveFollow_MD + '.input1.input1X')
            cmds.setAttr(WaveFollow_MD + '.input2X', -1)
            sine_PMA = cmds.shadingNode('plusMinusAverage', asUtility=True,
                                        name=tailName + '_' + Axial + '_sine0' + str(x) + '_PMA')
            cmds.connectAttr(Wavelength_MD + '.outputX', sine_PMA + '.input2D[0].input2Dx')
            cmds.connectAttr(WaveFollow_MD + '.outputX', sine_PMA + '.input2D[1].input2Dx')
            expressionStr01 = result_MD + '.input2X' + ' = ' + 'sin(' + sine_PMA + '.output2Dx);' + '\n'
            expressionStr = expressionStr + expressionStr01

        cmds.expression(s=expressionStr, name='sine_' + Axial, ae=True, uc=all)
        sys.stderr.write('# ------ CreateSine is ok')
