# Embedded file name: E:/JunCmds/tool/driver_win.py
import maya.cmds as cmds

class driver_win:

    def driver_win(self):
        driver_win = 'driver_win'
        if cmds.window(driver_win, ex=True):
            cmds.deleteUI(driver_win)
        cmds.window(driver_win, widthHeight=(300, 200), t='driver_win v1.01', menuBar=True, rtf=True, s=True)
        cmds.rowColumnLayout('Main', numberOfColumns=1, w=300, cal=(5, 'center'), m=True)
        cmds.rowColumnLayout('createSettingLY', numberOfColumns=3, w=300, cal=(5, 'center'), m=True)
        cmds.text('setting section', w=100, l='setting  name :')
        cmds.textField('settingBasename', w=120, text='L_arm')
        cmds.textField('settingBasename2', w=100, text='_driver', en=0)
        cmds.setParent('..')
        cmds.button('crete Setting', h=30, c=lambda *args: self.createSetting())
        cmds.rowColumnLayout('nameFieldLay', numberOfColumns=3, w=300, cal=(5, 'center'), m=True)
        cmds.text('distanceText', l='distance name :', w=100)
        cmds.textField('SDK_bridge_name')
        cmds.button(l='load distance', w=100, c=lambda *args: self.loadBridgeNode())
        cmds.setParent('..')
        cmds.radioButtonGrp('mirrorAxis', numberOfRadioButtons=3, label='mirror Axis  :', labelArray3=['x', 'y', 'z'], columnWidth4=[120,
         50,
         50,
         50], select=1, w=300, enableBackground=True)
        cmds.rowColumnLayout('mirrorLY', numberOfColumns=2, cal=(5, 'center'), m=True)
        cmds.text('prefixname', l='search for :', w=130)
        cmds.textField('prefixname', w=150, text='L_')
        cmds.text('suffixname', l='replace with :', w=130)
        cmds.textField('suffixname', w=150, text='R_')
        cmds.setParent('..')
        cmds.button(l='mirrior driver setting ', c=lambda *args: self.mirrorSetting(), h=40)
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.button(l=u'\u9a71\u52a8\u5c5e\u6027\u540d\u4fee\u6539\u6210\u5bf9\u79f0\n\u9009\u4e2dbridge', c=lambda *args: self.bridgeAttrsMirror(), h=40, w=150)
        cmds.button(l=u'\u9a71\u52a80\u20141\u8f6c\u6210\u5ea6\u65700\u2014180\n\u9009\u4e2dbridge', c=lambda *args: self.bridgeValue_to_angle(), h=40, w=150)
        cmds.showWindow()

    def continer_BG(self, name = '', addNodeMember = [], inputAttr_grp = [('inputA', 'connectInputAttr')], outAttr = ['']):
        cmds.createNode('dagContainer', n=name)
        cmds.container(name, e=True, addNode=addNodeMember, includeNetwork=True, includeHierarchyBelow=True)
        cmds.setAttr(str(name) + '.blackBox', 1, lock=True)
        cmds.setAttr(str(name) + '.creator', 'author: li zhi ', type='string', lock=True)
        cmds.addAttr(name, ln='input_Attributes')
        cmds.setAttr(str(name) + '.input_Attributes', cb=True, lock=True)
        for at in inputAttr_grp:
            inputAttr = at[0]
            outputAttr = at[1]
            cmds.addAttr(name, ln=inputAttr)
            cmds.setAttr(str(name) + '.' + str(inputAttr), k=True)
            cmds.connectAttr(str(name) + '.' + str(inputAttr), outputAttr)

        cmds.addAttr(name, ln='output_Attributes')
        cmds.setAttr(str(name) + '.output_Attributes', cb=True, lock=True)
        for outAt in outAttr:
            cmds.addAttr(name, ln=outAt)
            cmds.setAttr(str(name) + '.' + str(outAt), k=True)

    def changAngle(self):
        bridge = cmds.textField('SDK_bridge_name', q=True, text=True)
        selValue = cmds.optionMenu('SDK_DirectionMenu', q=True, sl=True)
        attrSDK = ['.angle_frontUp',
         '.angle_backUp',
         '.angle_frontBottom',
         '.angle_backBottom']
        currentAttr = '.angle_base'
        currentValue = cmds.getAttr(str(bridge) + currentAttr)
        cmds.setAttr(str(bridge) + attrSDK[selValue - 5], currentValue)

    def changSelectButtonEnbale(self):
        selValue = cmds.optionMenu('SDK_DirectionMenu', q=True, sl=True)
        if selValue < 4:
            cmds.button('changeAngle', e=True, en=False)
        else:
            cmds.button('changeAngle', e=True, en=True)

    def createSetting(self):
        settignname = cmds.textField('settingBasename', q=True, text=True) + cmds.textField('settingBasename2', q=True, text=True)
        print (settignname)
        self.createSettingLoc(settignname)

    def loadBridgeNode(self):
        slObj = cmds.ls(sl=True)[0]
        cmds.textField('SDK_bridge_name', e=True, text=slObj)

    def setMinValue(self):
        bridge = cmds.textField('SDK_bridge_name', q=True, text=True)
        selValue = cmds.optionMenu('SDK_DirectionMenu', q=True, sl=True)
        attrSDK = ['.min_front_input',
         '.min_up_input',
         '.min_back_input',
         '.min_bottom_input',
         '.min_frontUp_input',
         '.min_backUp_input',
         '.min_frontBottom_input',
         '.min_backBottom_input']
        currentAttr = ['.distance_front_currentlen',
         '.distance_up_currentlen',
         '.distance_back_currentlen',
         '.distance_bottom_currentlen',
         '.distance_frontUp_currentlen',
         '.distance_backUp_currentlen',
         '.distance_frontBottom_currentlen',
         '.distance_backBottom_currentlen']
        globalScale = cmds.getAttr(str(bridge) + '.global_scale')
        currentValue = cmds.getAttr(str(bridge) + currentAttr[selValue - 1])
        sdkValue = currentValue / globalScale
        cmds.setAttr(str(bridge) + attrSDK[selValue - 1], sdkValue)

    def setMaxValue(self):
        bridge = cmds.textField('SDK_bridge_name', q=True, text=True)
        selValue = cmds.optionMenu('SDK_DirectionMenu', q=True, sl=True)
        attrSDK = ['.max_front_input',
         '.max_up_input',
         '.max_back_input',
         '.max_bottom_input',
         '.max_frontUp_input',
         '.max_backUp_input',
         '.max_frontBottom_input',
         '.max_backBottom_input']
        currentAttr = ['.distance_front_currentlen',
         '.distance_up_currentlen',
         '.distance_back_currentlen',
         '.distance_bottom_currentlen',
         '.distance_frontUp_currentlen',
         '.distance_backUp_currentlen',
         '.distance_frontBottom_currentlen',
         '.distance_backBottom_currentlen']
        globalScale = cmds.getAttr(str(bridge) + '.global_scale')
        currentValue = cmds.getAttr(str(bridge) + currentAttr[selValue - 1])
        sdkValue = currentValue / globalScale
        cmds.setAttr(str(bridge) + attrSDK[selValue - 1], sdkValue)

    def setMinV(self):
        bridge = cmds.textField('SDK_bridge_name', q=True, text=True)
        globalScale = cmds.getAttr(str(bridge) + '.global_scale')
        globalScale = cmds.getAttr(str(bridge) + '.global_scale')

    def setMaxV(self):
        node = cmds.textField('nodename', q=True, text=True)
        distance = cmds.textField('distancename', q=True, text=True)
        shapenode = cmds.listRelatives(distance, s=True)[0]
        distanceValue = cmds.getAttr(str(shapenode) + '.distance')
        cmds.setAttr(str(node) + '.inputMin', distanceValue)

    def mirrorSetting(self):
        bridge = cmds.textField('SDK_bridge_name', q=True, text=True)
        grp = bridge.replace('bridge', 'grp')
        org = cmds.textField('prefixname', q=True, text=True)
        replace = cmds.textField('suffixname', q=True, text=True)
        mirrorBridge = bridge.replace(org, replace)
        mirrorGrp = grp.replace(org, replace)
        splits = mirrorGrp.split('_')
        pre = splits[0:-1]
        for i in range(len(pre)):
            if i == 0:
                mirrorsetting = pre[i]
            else:
                mirrorsetting = mirrorsetting + '_' + pre[i]

        self.createSettingLoc(mirrorsetting)
        orgsetting = mirrorsetting.replace(replace, org)
        locPos = '_pos_grp'
        locpon = ['_frontLoc',
         '_upLoc',
         '_backLoc',
         '_bottomLoc',
         '_frontUpLoc',
         '_backUpLoc',
         '_frontBottomLoc',
         '_backBottomLoc',
         '_state_Angloc']
        attr = ['angle_frontUp',
         'angle_backUp',
         'angle_frontBottom',
         'angle_backBottom']
        orggrptranslate = cmds.xform(grp, q=True, t=True, ws=True)
        orggrprotate = cmds.xform(grp, q=True, ro=True, ws=True)
        mirrorAxis = cmds.radioButtonGrp('mirrorAxis', q=True, select=True)
        if mirrorAxis == 1:
            cmds.xform(mirrorGrp, ws=True, t=(-1 * orggrptranslate[0], orggrptranslate[1], orggrptranslate[2]))
            cmds.xform(mirrorGrp, ws=True, ro=(orggrprotate[0], -1 * orggrprotate[1], -1 * orggrprotate[2]))
            org_postranslateX = cmds.getAttr(orgsetting + locPos + '.translateX')
            cmds.setAttr(mirrorsetting + locPos + '.translateX', -1 * org_postranslateX)
            for lp in locpon:
                org_translateX = cmds.getAttr(orgsetting + lp + '.translateX')
                cmds.setAttr(mirrorsetting + lp + '.translateX', -1 * org_translateX)

        if mirrorAxis == 2:
            cmds.xform(mirrorGrp, ws=True, t=(orggrptranslate[0], -1 * orggrptranslate[1], orggrptranslate[2]))
            cmds.xform(mirrorGrp, ws=True, ro=(-1 * orggrprotate[0], orggrprotate[1], -1 * orggrprotate[2]))
            org_postranslateY = cmds.getAttr(orgsetting + locPos + '.translateY')
            cmds.setAttr(mirrorsetting + locPos + '.translateY', -1 * org_postranslateY)
            for lp in locpon:
                org_translateY = cmds.getAttr(orgsetting + lp + '.translateY')
                cmds.setAttr(mirrorsetting + lp + '.translateY', -1 * org_translateY)

        if mirrorAxis == 3:
            cmds.xform(mirrorGrp, ws=True, t=(orggrptranslate[0], orggrptranslate[1], -1 * orggrptranslate[2]))
            cmds.xform(mirrorGrp, ws=True, ro=(-1 * orggrprotate[0], -1 * orggrprotate[1], orggrprotate[2]))
            org_postranslateZ = cmds.getAttr(orgsetting + locPos + '.translateZ')
            cmds.setAttr(mirrorsetting + locPos + '.translateZ', -1 * org_postranslateZ)
            for lp in locpon:
                org_translateZ = cmds.getAttr(orgsetting + lp + '.translateZ')
                cmds.setAttr(mirrorsetting + lp + '.translateZ', -1 * org_translateZ)

        for at in attr:
            org_at = cmds.getAttr(bridge + '.' + at)
            cmds.setAttr(mirrorBridge + '.' + at, org_at)

    def createSettingLoc(self, locPart):
        locAll = ['frontLoc',
         'upLoc',
         'backLoc',
         'bottomLoc',
         'pointLoc',
         'posLoc',
         'stateLoc']
        angleLoc = ['base_Angloc', 'follow_Angloc', 'state_Angloc']
        obliqueLocAll = ['frontUpLoc',
         'backUpLoc',
         'frontBottomLoc',
         'backBottomLoc']
        locname = [str(locPart) + '_' + locAll[0],
         str(locPart) + '_' + locAll[1],
         str(locPart) + '_' + locAll[2],
         str(locPart) + '_' + locAll[3],
         str(locPart) + '_' + locAll[4],
         str(locPart) + '_' + locAll[5],
         str(locPart) + '_' + locAll[6]]
        obliqueLoc = [str(locPart) + '_' + obliqueLocAll[0],
         str(locPart) + '_' + obliqueLocAll[1],
         str(locPart) + '_' + obliqueLocAll[2],
         str(locPart) + '_' + obliqueLocAll[3]]
        anglocAll = [str(locPart) + '_' + angleLoc[0], str(locPart) + '_' + angleLoc[1], str(locPart) + '_' + angleLoc[2]]
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[0])
        cmds.move(-5, 0, 5, locname[0])
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[1])
        cmds.move(-5, 5, 0, locname[1])
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[2])
        cmds.move(-5, 0, -5, locname[2])
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[3])
        cmds.move(-5, -5, 0, locname[3])
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[4])
        cmds.move(0, 0, 0, locname[4])
        cmds.setAttr(str(locname[4]) + '.visibility', 0)
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[5])
        cmds.move(5, 0, 0, locname[5])
        cmds.select(cl=True)
        cmds.spaceLocator(n=locname[6])
        cmds.move(5, 0, 0, locname[6])
        cmds.setAttr(str(locname[6]) + '.visibility', 0)
        cmds.select(cl=True)
        cmds.spaceLocator(n=obliqueLoc[0])
        cmds.move(-5, 5, 5, obliqueLoc[0])
        cmds.select(cl=True)
        cmds.spaceLocator(n=obliqueLoc[1])
        cmds.move(-5, 5, -5, obliqueLoc[1])
        cmds.select(cl=True)
        cmds.spaceLocator(n=obliqueLoc[2])
        cmds.move(-5, -5, 5, obliqueLoc[2])
        cmds.select(cl=True)
        cmds.spaceLocator(n=obliqueLoc[3])
        cmds.move(-5, -5, -5, obliqueLoc[3])
        cmds.select(cl=True)
        cmds.spaceLocator(n=anglocAll[0])
        cmds.move(0, 0, 0, anglocAll[0])
        cmds.setAttr(str(anglocAll[0]) + '.visibility', 0)
        cmds.select(cl=True)
        cmds.spaceLocator(n=anglocAll[1])
        cmds.move(5, 0, 0, anglocAll[1])
        cmds.setAttr(str(anglocAll[1]) + '.visibility', 0)
        cmds.select(cl=True)
        cmds.spaceLocator(n=anglocAll[2])
        cmds.move(5, 0, 0, anglocAll[2])
        cmds.setAttr(str(anglocAll[2]) + '.visibility', 0)
        cmds.transformLimits(locname[4], tx=(0, 0), etx=(True, True))
        cmds.pointConstraint(locname[5], locname[4])
        cmds.pointConstraint(locname[5], anglocAll[1])
        cmds.group(n=str(locPart) + '_grp', em=True)
        cmds.parent(locname[0], locname[1], locname[2], locname[3], locname[4], locname[5], locname[6], obliqueLoc[0], obliqueLoc[1], obliqueLoc[2], obliqueLoc[3], anglocAll[0], anglocAll[1], anglocAll[2], str(locPart) + '_grp')
        cmds.group(n=str(locPart) + '_bridge', em=True)
        cmds.parent(str(locPart) + '_bridge', str(locPart) + '_grp')
        cmds.addAttr(str(locPart) + '_bridge', at='enum', ln='__', en='current_length')
        cmds.setAttr(str(locPart) + '_bridge.__', keyable=True, l=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='driver_vulue')
        cmds.setAttr(str(locPart) + '_bridge.driver_vulue', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', at='enum', ln='_______', en='angle_base')
        cmds.setAttr(str(locPart) + '_bridge._______', keyable=True, l=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='angle_base')
        cmds.setAttr(str(locPart) + '_bridge.angle_base', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='angle_frontUp', dv=45, min=1, max=89)
        cmds.setAttr(str(locPart) + '_bridge.angle_frontUp', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='angle_backUp', dv=135, min=91, max=179)
        cmds.setAttr(str(locPart) + '_bridge.angle_backUp', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='angle_frontBottom', dv=45, min=1, max=89)
        cmds.setAttr(str(locPart) + '_bridge.angle_frontBottom', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='angle_backBottom', dv=135, min=91, max=179)
        cmds.setAttr(str(locPart) + '_bridge.angle_backBottom', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', at='enum', ln='_________', en='Interval_sevalue')
        cmds.setAttr(str(locPart) + '_bridge._________', keyable=True, l=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='Interval_sevalue')
        cmds.setAttr(str(locPart) + '_bridge.Interval_sevalue', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', at='enum', ln='__________', en='SDK_driver')
        cmds.setAttr(str(locPart) + '_bridge.__________', keyable=True, l=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='front_driver')
        cmds.setAttr(str(locPart) + '_bridge.front_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='up_driver')
        cmds.setAttr(str(locPart) + '_bridge.up_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='back_driver')
        cmds.setAttr(str(locPart) + '_bridge.back_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='bottom_driver')
        cmds.setAttr(str(locPart) + '_bridge.bottom_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='frontUp_driver')
        cmds.setAttr(str(locPart) + '_bridge.frontUp_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='backUp_driver')
        cmds.setAttr(str(locPart) + '_bridge.backUp_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='frontBottom_driver')
        cmds.setAttr(str(locPart) + '_bridge.frontBottom_driver', keyable=True)
        cmds.addAttr(str(locPart) + '_bridge', ln='backBottom_driver')
        cmds.setAttr(str(locPart) + '_bridge.backBottom_driver', keyable=True)
        angleNode = str(locPart) + '_angle_AB_Bt'
        anglePMANode01 = str(locPart) + '_anglePMA01'
        anglePMANode02 = str(locPart) + '_anglePMA02'
        cmds.createNode('angleBetween', n=angleNode)
        cmds.createNode('plusMinusAverage', n=anglePMANode01)
        cmds.setAttr(str(anglePMANode01) + '.operation', 2)
        cmds.connectAttr(str(anglocAll[1]) + '.translateX', str(anglePMANode01) + '.input3D[0].input3Dx')
        cmds.connectAttr(str(anglocAll[1]) + '.translateY', str(anglePMANode01) + '.input3D[0].input3Dy')
        cmds.connectAttr(str(anglocAll[1]) + '.translateZ', str(anglePMANode01) + '.input3D[0].input3Dz')
        cmds.connectAttr(str(anglocAll[0]) + '.translateX', str(anglePMANode01) + '.input3D[1].input3Dx')
        cmds.connectAttr(str(anglocAll[0]) + '.translateY', str(anglePMANode01) + '.input3D[1].input3Dy')
        cmds.connectAttr(str(anglocAll[0]) + '.translateZ', str(anglePMANode01) + '.input3D[1].input3Dz')
        cmds.createNode('plusMinusAverage', n=anglePMANode02)
        cmds.setAttr(str(anglePMANode01) + '.operation', 2)
        cmds.connectAttr(str(anglocAll[2]) + '.translateX', str(anglePMANode02) + '.input3D[0].input3Dx')
        cmds.connectAttr(str(anglocAll[2]) + '.translateY', str(anglePMANode02) + '.input3D[0].input3Dy')
        cmds.connectAttr(str(anglocAll[2]) + '.translateZ', str(anglePMANode02) + '.input3D[0].input3Dz')
        cmds.connectAttr(str(anglocAll[0]) + '.translateX', str(anglePMANode02) + '.input3D[1].input3Dx')
        cmds.connectAttr(str(anglocAll[0]) + '.translateY', str(anglePMANode02) + '.input3D[1].input3Dy')
        cmds.connectAttr(str(anglocAll[0]) + '.translateZ', str(anglePMANode02) + '.input3D[1].input3Dz')
        cmds.connectAttr(str(anglePMANode02) + '.output3Dx', str(angleNode) + '.vector1X')
        cmds.connectAttr(str(anglePMANode02) + '.output3Dy', str(angleNode) + '.vector1Y')
        cmds.connectAttr(str(anglePMANode02) + '.output3Dz', str(angleNode) + '.vector1Z')
        cmds.connectAttr(str(anglePMANode01) + '.output3Dx', str(angleNode) + '.vector2X')
        cmds.connectAttr(str(anglePMANode01) + '.output3Dy', str(angleNode) + '.vector2Y')
        cmds.connectAttr(str(anglePMANode01) + '.output3Dz', str(angleNode) + '.vector2Z')
        angleValueMD = str(locPart) + '_angValueMD'
        cmds.createNode('multiplyDivide', n=angleValueMD)
        cmds.connectAttr(str(angleNode) + '.angle', str(angleValueMD) + '.input1X')
        cmds.setAttr(str(angleValueMD) + '.input2X', 180)
        cmds.setAttr(str(angleValueMD) + '.operation', 2)
        cmds.connectAttr(str(angleValueMD) + '.outputX', str(locPart) + '_bridge.driver_vulue')
        cmds.select(cl=True)
        cmds.spaceLocator(n=str(locPart) + '_basefrontangle_loc')
        cmds.move(0, 0, 5, str(locPart) + '_basefrontangle_loc')
        cmds.setAttr(str(locPart) + '_basefrontangle_loc.visibility', 0)
        cmds.select(cl=True)
        cmds.spaceLocator(n=str(locPart) + '_baseangle_loc')
        cmds.move(0, 0, 0, str(locPart) + '_baseangle_loc')
        cmds.setAttr(str(locPart) + '_baseangle_loc.visibility', 0)
        cmds.parent(str(locPart) + '_baseangle_loc', str(locPart) + '_basefrontangle_loc', str(locPart) + '_grp')
        cmds.createNode('angleBetween', n=str(locPart) + '_angleBt')
        angleLoc = [str(locPart) + '_basefrontangle_loc', locname[4], str(locPart) + '_baseangle_loc']
        pmanode = [str(locPart) + '_angle01_pma', str(locPart) + '_angle02_pma']
        cmds.createNode('plusMinusAverage', n=pmanode[0])
        cmds.setAttr(str(pmanode[0]) + '.operation', 2)
        cmds.createNode('plusMinusAverage', n=pmanode[1])
        cmds.setAttr(str(pmanode[1]) + '.operation', 2)
        for al in range(2):
            shape01 = cmds.listRelatives(angleLoc[al], s=True)[0]
            shape02 = cmds.listRelatives(angleLoc[2], s=True)[0]
            cmds.connectAttr(str(shape01) + '.worldPosition[0]', str(pmanode[al]) + '.input3D[0]')
            cmds.connectAttr(str(shape02) + '.worldPosition[0]', str(pmanode[al]) + '.input3D[1]')

        cmds.connectAttr(str(pmanode[0]) + '.output3D', str(locPart) + '_angleBt.vector1')
        cmds.connectAttr(str(pmanode[1]) + '.output3D', str(locPart) + '_angleBt.vector2')
        cmds.connectAttr(str(locPart) + '_angleBt.axisAngle.angle', str(locPart) + '_bridge.angle_base')
        self.IntervalSection(locname[4], str(locPart) + '_bridge')
        cmds.group(n=str(locPart) + '_pos_grp', em=True)
        cmds.parentConstraint(locname[5], str(locPart) + '_pos_grp', mo=False, n='templeConstraint')
        cmds.delete('templeConstraint')
        cmds.parent(locname[5], locname[6], str(locPart) + '_pos_grp')
        cmds.parent(str(locPart) + '_pos_grp', str(locPart) + '_grp')
        cmds.pointConstraint(locname[5], locname[6])
        cmds.transformLimits(locname[6], tx=(0, 0), etx=(True, True))
        continername = str(locPart) + '_continer'
        addMember = str(locPart) + '_grp'
        inputAttributes = [('angle_backBottom', str(str(locPart) + '_bridge') + '.angle_backBottom'),
         ('angle_frontUp', str(str(locPart) + '_bridge') + '.angle_frontUp'),
         ('angle_backUp', str(str(locPart) + '_bridge') + '.angle_backUp'),
         ('angle_frontBottom', str(str(locPart) + '_bridge') + '.angle_frontBottom')]
        outputAttibute = ['front_driver',
         'up_driver',
         'back_driver',
         'bottom_driver',
         'frontUp_driver',
         'backUp_driver',
         'frontBottom_driver',
         'backBottom_driver']
        attrs = ['tx',
         'ty',
         'tz',
         'rx',
         'ry',
         'rz',
         'sx',
         'sy',
         'sz',
         'v']
        for attr in attrs:
            cmds.setAttr(locPart + '_bridge' + '.' + attr, lock=1, keyable=False, channelBox=False)

        cmds.select(locPart + '_bridge')

    def createDistance(self, starPos, endPos, nameNode):
        startShape = cmds.listRelatives(starPos, s=True)[0]
        endShape = cmds.listRelatives(endPos, s=True)[0]
        cmds.createNode('distanceBetween', n=nameNode)
        cmds.connectAttr(str(startShape) + '.worldPosition', str(nameNode) + '.point1')
        cmds.connectAttr(str(endShape) + '.worldPosition', str(nameNode) + '.point2')

    def IntervalSection(self, referenceObj, attrObj):
        sections = referenceObj.split('_')
        pre = sections[0:-1]
        objpre = ''
        prenum = 0
        for i in pre:
            if prenum == 0:
                objpre = objpre + i
            else:
                objpre = objpre + '_' + i
            prenum = prenum + 1

        selectY = objpre + '_Y_selecton_conditon'
        selectZ = objpre + '_Z_selecton_conditon'
        selectYliner = objpre + '_Yliner_selecton_conditon'
        selectZliner = objpre + '_Zliner_selecton_conditon'
        multiPMA = objpre + '_multi_pma'
        cmds.createNode('condition', n=objpre + '_Y_selecton_conditon')
        cmds.createNode('condition', n=objpre + '_Yliner_selecton_conditon')
        cmds.createNode('condition', n=objpre + '_Z_selecton_conditon')
        cmds.createNode('condition', n=objpre + '_Zliner_selecton_conditon')
        cmds.connectAttr(str(referenceObj) + '.translateY', str(selectY) + '.firstTerm')
        cmds.setAttr(str(selectY) + '.secondTerm', 0)
        cmds.setAttr(str(selectY) + '.operation', 3)
        cmds.setAttr(str(selectY) + '.colorIfTrueR', 3)
        cmds.setAttr(str(selectY) + '.colorIfFalseR', 1)
        cmds.connectAttr(str(referenceObj) + '.translateZ', str(selectZ) + '.firstTerm')
        cmds.setAttr(str(selectZ) + '.secondTerm', 0)
        cmds.setAttr(str(selectZ) + '.operation', 3)
        cmds.setAttr(str(selectZ) + '.colorIfTrueR', 6)
        cmds.setAttr(str(selectZ) + '.colorIfFalseR', 2)
        cmds.connectAttr(str(referenceObj) + '.translateY', str(selectYliner) + '.firstTerm')
        cmds.setAttr(str(selectYliner) + '.secondTerm', 0)
        cmds.setAttr(str(selectYliner) + '.operation', 0)
        cmds.setAttr(str(selectYliner) + '.colorIfTrueR', 1)
        cmds.setAttr(str(selectYliner) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(referenceObj) + '.translateZ', str(selectZliner) + '.firstTerm')
        cmds.setAttr(str(selectZliner) + '.secondTerm', 0)
        cmds.setAttr(str(selectZliner) + '.operation', 0)
        cmds.setAttr(str(selectZliner) + '.colorIfTrueR', 0.5)
        cmds.setAttr(str(selectZliner) + '.colorIfFalseR', 0)
        cmds.createNode('plusMinusAverage', n=multiPMA)
        cmds.connectAttr(str(selectY) + '.outColorR', str(multiPMA) + '.input1D[0]')
        cmds.connectAttr(str(selectZ) + '.outColorR', str(multiPMA) + '.input1D[1]')
        cmds.connectAttr(str(selectYliner) + '.outColorR', str(multiPMA) + '.input1D[2]')
        cmds.connectAttr(str(selectZliner) + '.outColorR', str(multiPMA) + '.input1D[3]')
        cmds.connectAttr(str(multiPMA) + '.output1D', str(attrObj) + '.Interval_sevalue')
        outputInterval01 = objpre + '_outputInterval01_conditon'
        outputInterval02 = objpre + '_outputInterval02_conditon'
        outputInterval03 = objpre + '_outputInterval03_conditon'
        outputInterval04 = objpre + '_outputInterval04_conditon'
        outputIntervalAxis_PosY = objpre + '_outputInterval_axis_PosY_conditon'
        outputIntervalAxis_NegY = objpre + '_outputInterval_axis_negY_conditon'
        outputIntervalAxis_PosZ = objpre + '_outputInterval_axis_PosZ_conditon'
        outputIntervalAxis_NegZ = objpre + '_outputInterval_axis_negZ_conditon'
        cmds.createNode('condition', n=outputInterval01)
        cmds.createNode('condition', n=outputInterval02)
        cmds.createNode('condition', n=outputInterval03)
        cmds.createNode('condition', n=outputInterval04)
        cmds.createNode('condition', n=outputIntervalAxis_PosY)
        cmds.createNode('condition', n=outputIntervalAxis_NegY)
        cmds.createNode('condition', n=outputIntervalAxis_PosZ)
        cmds.createNode('condition', n=outputIntervalAxis_NegZ)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputInterval01) + '.firstTerm')
        cmds.setAttr(str(outputInterval01) + '.secondTerm', 9)
        cmds.setAttr(str(outputInterval01) + '.operation', 0)
        cmds.setAttr(str(outputInterval01) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputInterval01) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputInterval02) + '.firstTerm')
        cmds.setAttr(str(outputInterval02) + '.secondTerm', 5)
        cmds.setAttr(str(outputInterval02) + '.operation', 0)
        cmds.setAttr(str(outputInterval02) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputInterval02) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputInterval03) + '.firstTerm')
        cmds.setAttr(str(outputInterval03) + '.secondTerm', 7)
        cmds.setAttr(str(outputInterval03) + '.operation', 0)
        cmds.setAttr(str(outputInterval03) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputInterval03) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputInterval04) + '.firstTerm')
        cmds.setAttr(str(outputInterval04) + '.secondTerm', 3)
        cmds.setAttr(str(outputInterval04) + '.operation', 0)
        cmds.setAttr(str(outputInterval04) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputInterval04) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputIntervalAxis_PosY) + '.firstTerm')
        cmds.setAttr(str(outputIntervalAxis_PosY) + '.secondTerm', 9.5)
        cmds.setAttr(str(outputIntervalAxis_PosY) + '.operation', 0)
        cmds.setAttr(str(outputIntervalAxis_PosY) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputIntervalAxis_PosY) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputIntervalAxis_NegY) + '.firstTerm')
        cmds.setAttr(str(outputIntervalAxis_NegY) + '.secondTerm', 7.5)
        cmds.setAttr(str(outputIntervalAxis_NegY) + '.operation', 0)
        cmds.setAttr(str(outputIntervalAxis_NegY) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputIntervalAxis_NegY) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputIntervalAxis_PosZ) + '.firstTerm')
        cmds.setAttr(str(outputIntervalAxis_PosZ) + '.secondTerm', 10)
        cmds.setAttr(str(outputIntervalAxis_PosZ) + '.operation', 0)
        cmds.setAttr(str(outputIntervalAxis_PosZ) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputIntervalAxis_PosZ) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.Interval_sevalue', str(outputIntervalAxis_NegZ) + '.firstTerm')
        cmds.setAttr(str(outputIntervalAxis_NegZ) + '.secondTerm', 6)
        cmds.setAttr(str(outputIntervalAxis_NegZ) + '.operation', 0)
        cmds.setAttr(str(outputIntervalAxis_NegZ) + '.colorIfTrueR', 1)
        cmds.setAttr(str(outputIntervalAxis_NegZ) + '.colorIfFalseR', 0)
        stateY = str(objpre) + '_Y_state_conditon'
        stateZ = str(objpre) + '_Z_state_conditon'
        cmds.createNode('condition', n=stateZ)
        cmds.connectAttr(str(referenceObj) + '.translateY', str(stateZ) + '.firstTerm')
        cmds.setAttr(str(stateZ) + '.secondTerm', 0)
        cmds.setAttr(str(stateZ) + '.operation', 3)
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(stateZ) + '.colorIfTrueR')
        cmds.setAttr(str(stateZ) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(stateZ) + '.colorIfFalseG')
        cmds.setAttr(str(stateZ) + '.colorIfTrueG', 0)
        cmds.createNode('condition', n=stateY)
        cmds.connectAttr(str(referenceObj) + '.translateZ', str(stateY) + '.firstTerm')
        cmds.setAttr(str(stateY) + '.secondTerm', 0)
        cmds.setAttr(str(stateY) + '.operation', 3)
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(stateY) + '.colorIfTrueR')
        cmds.setAttr(str(stateY) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(stateY) + '.colorIfFalseG')
        cmds.setAttr(str(stateY) + '.colorIfTrueG', 0)
        frontsdk_pma = str(objpre) + '_front_sdk01_pma'
        upsdk_pma = str(objpre) + '_up_sdk01_pma'
        backsdk_pma = str(objpre) + '_back_sdk01_pma'
        bottomsdk_pma = str(objpre) + '_bottom_sdk01_pma'
        cmds.createNode('plusMinusAverage', n=frontsdk_pma)
        cmds.createNode('plusMinusAverage', n=upsdk_pma)
        cmds.createNode('plusMinusAverage', n=backsdk_pma)
        cmds.createNode('plusMinusAverage', n=bottomsdk_pma)
        frontsdk02_pma = str(objpre) + '_front_sdk02_pma'
        upsdk02_pma = str(objpre) + '_up_sdk02_pma'
        backsdk02_pma = str(objpre) + '_back_sdk02_pma'
        bottomsdk02_pma = str(objpre) + '_bottom_sdk02_pma'
        cmds.createNode('plusMinusAverage', n=frontsdk02_pma)
        cmds.createNode('plusMinusAverage', n=upsdk02_pma)
        cmds.createNode('plusMinusAverage', n=backsdk02_pma)
        cmds.createNode('plusMinusAverage', n=bottomsdk02_pma)
        frontsdk_cdn = str(objpre) + '_front_sdk01_condition'
        upsdk_cdn = str(objpre) + '_up_sdk01_condition'
        backsdk_cdn = str(objpre) + '_back_sdk01_condition'
        bottomsdk_cdn = str(objpre) + '_bottom_sdk01_condition'
        cmds.createNode('condition', n=frontsdk_cdn)
        cmds.createNode('condition', n=upsdk_cdn)
        cmds.createNode('condition', n=backsdk_cdn)
        cmds.createNode('condition', n=bottomsdk_cdn)
        frontsdk_md = str(objpre) + '_front_sdk01_md'
        upsdk_md = str(objpre) + '_up_sdk01_md'
        backsdk_md = str(objpre) + '_back_sdk01_md'
        bottomsdk_md = str(objpre) + '_bottom_sdk01_md'
        cmds.createNode('multiplyDivide', n=frontsdk_md)
        cmds.createNode('multiplyDivide', n=upsdk_md)
        cmds.createNode('multiplyDivide', n=backsdk_md)
        cmds.createNode('multiplyDivide', n=bottomsdk_md)
        frontsdk02_md = str(objpre) + '_front_sdk02_md'
        upsdk02_md = str(objpre) + '_up_sdk02_md'
        backsdk02_md = str(objpre) + '_back_sdk02_md'
        bottomsdk02_md = str(objpre) + '_bottom_sdk02_md'
        cmds.createNode('multiplyDivide', n=frontsdk02_md)
        cmds.createNode('multiplyDivide', n=upsdk02_md)
        cmds.createNode('multiplyDivide', n=backsdk02_md)
        cmds.createNode('multiplyDivide', n=bottomsdk02_md)
        frontUpsdk_cdn = str(objpre) + '_frontUp_sdk01_condition'
        backUpsdk_cdn = str(objpre) + '_backUp_sdk01_condition'
        frontBottomsdk_cdn = str(objpre) + '_frontBottom_sdk01_condition'
        backBottomsdk_cdn = str(objpre) + '_backBottomsdk_sdk01_condition'
        cmds.createNode('condition', n=frontUpsdk_cdn)
        cmds.createNode('condition', n=backUpsdk_cdn)
        cmds.createNode('condition', n=frontBottomsdk_cdn)
        cmds.createNode('condition', n=backBottomsdk_cdn)
        frontUpsdk_md = str(objpre) + '_frontUp_sdk01_md'
        backUpsdk_md = str(objpre) + '_backUp_sdk01_md'
        frontBottomsdk_md = str(objpre) + '_frontBottom_sdk01_md'
        backBottomsdk_md = str(objpre) + '_backBottomsdk_sdk01_md'
        cmds.createNode('multiplyDivide', n=frontUpsdk_md)
        cmds.createNode('multiplyDivide', n=backUpsdk_md)
        cmds.createNode('multiplyDivide', n=frontBottomsdk_md)
        cmds.createNode('multiplyDivide', n=backBottomsdk_md)
        frontUpsdk02_md = str(objpre) + '_frontUp_sdk02_md'
        backUpsdk02_md = str(objpre) + '_backUp_sdk02_md'
        frontBottomsdk02_md = str(objpre) + '_frontBottom_sdk02_md'
        backBottomsdk02_md = str(objpre) + '_backBottomsdk_sdk02_md'
        cmds.createNode('multiplyDivide', n=frontUpsdk02_md)
        cmds.createNode('multiplyDivide', n=backUpsdk02_md)
        cmds.createNode('multiplyDivide', n=frontBottomsdk02_md)
        cmds.createNode('multiplyDivide', n=backBottomsdk02_md)
        cmds.connectAttr(str(outputInterval01) + '.outColorR', str(frontsdk_pma) + '.input1D[0]')
        cmds.connectAttr(str(outputInterval03) + '.outColorR', str(frontsdk_pma) + '.input1D[1]')
        cmds.connectAttr(str(outputIntervalAxis_PosZ) + '.outColorR', str(frontsdk_pma) + '.input1D[2]')
        cmds.connectAttr(str(frontsdk_pma) + '.output1D', str(frontsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(frontsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(frontsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(frontsdk_cdn) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontsdk02_pma) + '.input2D[1].input2Dx')
        cmds.setAttr(str(frontsdk02_pma) + '.input2D[0].input2Dx', 90)
        cmds.setAttr(str(frontsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(frontsdk02_pma) + '.output2D.output2Dx', str(frontsdk_md) + '.input1.input1X')
        cmds.setAttr(str(frontsdk_md) + '.input2.input2X', 90)
        cmds.setAttr(str(frontsdk_md) + '.operation', 2)
        cmds.connectAttr(str(frontsdk_md) + '.outputX', str(frontsdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(frontsdk_cdn) + '.outColorR', str(frontsdk02_md) + '.input1.input1X')
        cmds.connectAttr(str(stateY) + '.outColorR', str(frontsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(frontsdk02_md) + '.output.outputX', str(attrObj) + '.front_driver')
        cmds.connectAttr(str(outputInterval01) + '.outColorR', str(upsdk_pma) + '.input1D[0]')
        cmds.connectAttr(str(outputInterval02) + '.outColorR', str(upsdk_pma) + '.input1D[1]')
        cmds.connectAttr(str(outputIntervalAxis_PosY) + '.outColorR', str(upsdk_pma) + '.input1D[2]')
        cmds.connectAttr(str(upsdk_pma) + '.output1D', str(upsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(upsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(upsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(upsdk_cdn) + '.colorIfFalseR', 0)
        upanglesdk_cdn = str(objpre) + '_front_anglesdk_condition'
        cmds.createNode('condition', n=upanglesdk_cdn)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(upanglesdk_cdn) + '.firstTerm')
        cmds.setAttr(str(upanglesdk_cdn) + '.secondTerm', 90)
        cmds.setAttr(str(upanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(upsdk02_pma) + '.input2D[1].input2Dx')
        cmds.setAttr(str(upsdk02_pma) + '.input2D[0].input2Dx', 180)
        cmds.setAttr(str(upsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(upsdk02_pma) + '.output2D.output2Dx', str(upanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(attrObj) + '.angle_base', str(upanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(upanglesdk_cdn) + '.outColorR', str(upsdk_md) + '.input1.input1X')
        cmds.setAttr(str(upsdk_md) + '.input2.input2X', 90)
        cmds.setAttr(str(upsdk_md) + '.operation', 2)
        cmds.connectAttr(str(upsdk_md) + '.outputX', str(upsdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(upsdk_cdn) + '.outColorR', str(upsdk02_md) + '.input1.input1X')
        cmds.connectAttr(str(stateZ) + '.outColorR', str(upsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(upsdk02_md) + '.output.outputX', str(attrObj) + '.up_driver')
        cmds.connectAttr(str(outputInterval02) + '.outColorR', str(backsdk_pma) + '.input1D[0]')
        cmds.connectAttr(str(outputInterval04) + '.outColorR', str(backsdk_pma) + '.input1D[1]')
        cmds.connectAttr(str(outputIntervalAxis_NegZ) + '.outColorR', str(backsdk_pma) + '.input1D[2]')
        cmds.connectAttr(str(backsdk_pma) + '.output1D', str(backsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(backsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(backsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(backsdk_cdn) + '.colorIfFalseR', 0)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backsdk02_pma) + '.input2D[0].input2Dx')
        cmds.setAttr(str(backsdk02_pma) + '.input2D[1].input2Dx', 90)
        cmds.setAttr(str(backsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(backsdk02_pma) + '.output2D.output2Dx', str(backsdk_md) + '.input1.input1X')
        cmds.setAttr(str(backsdk_md) + '.input2.input2X', 90)
        cmds.setAttr(str(backsdk_md) + '.operation', 2)
        cmds.connectAttr(str(backsdk_md) + '.outputX', str(backsdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(backsdk_cdn) + '.outColorR', str(backsdk02_md) + '.input1.input1X')
        cmds.connectAttr(str(stateY) + '.outColorG', str(backsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(backsdk02_md) + '.output.outputX', str(attrObj) + '.back_driver')
        cmds.connectAttr(str(outputInterval03) + '.outColorR', str(bottomsdk_pma) + '.input1D[0]')
        cmds.connectAttr(str(outputInterval04) + '.outColorR', str(bottomsdk_pma) + '.input1D[1]')
        cmds.connectAttr(str(outputIntervalAxis_NegY) + '.outColorR', str(bottomsdk_pma) + '.input1D[2]')
        cmds.connectAttr(str(bottomsdk_pma) + '.output1D', str(bottomsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(bottomsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(bottomsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(bottomsdk_cdn) + '.colorIfFalseR', 0)
        bottomanglesdk_cdn = str(objpre) + '_bottom_anglesdk_condition'
        cmds.createNode('condition', n=bottomanglesdk_cdn)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(bottomanglesdk_cdn) + '.firstTerm')
        cmds.setAttr(str(bottomanglesdk_cdn) + '.secondTerm', 90)
        cmds.setAttr(str(bottomanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(bottomsdk02_pma) + '.input2D[1].input2Dx')
        cmds.setAttr(str(bottomsdk02_pma) + '.input2D[0].input2Dx', 180)
        cmds.setAttr(str(bottomsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(bottomsdk02_pma) + '.output2D.output2Dx', str(bottomanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(attrObj) + '.angle_base', str(bottomanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(bottomanglesdk_cdn) + '.outColorR', str(bottomsdk_md) + '.input1.input1X')
        cmds.setAttr(str(bottomsdk_md) + '.input2.input2X', 90)
        cmds.setAttr(str(bottomsdk_md) + '.operation', 2)
        cmds.connectAttr(str(bottomsdk_md) + '.outputX', str(bottomsdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(bottomsdk_cdn) + '.outColorR', str(bottomsdk02_md) + '.input1.input1X')
        cmds.connectAttr(str(stateZ) + '.outColorG', str(bottomsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(bottomsdk02_md) + '.output.outputX', str(attrObj) + '.bottom_driver')
        cmds.connectAttr(str(outputInterval01) + '.outColorR', str(frontUpsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(frontUpsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(frontUpsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(frontUpsdk_cdn) + '.colorIfFalseR', 0)
        cmds.setAttr(str(frontUpsdk_cdn) + '.colorIfTrueR', 1)
        frontUpanglesdk_cdn = str(objpre) + '_frontUp_anglesdk_condition'
        cmds.createNode('condition', n=frontUpanglesdk_cdn)
        frontUpsdk02_pma = str(objpre) + '_frontUp_anglesdk_pma'
        cmds.createNode('plusMinusAverage', n=frontUpsdk02_pma)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontUpanglesdk_cdn) + '.firstTerm')
        cmds.connectAttr(str(attrObj) + '.angle_frontUp', str(frontUpanglesdk_cdn) + '.secondTerm')
        cmds.setAttr(str(frontUpanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontUpsdk02_pma) + '.input3D[1].input3Dx')
        cmds.setAttr(str(frontUpsdk02_pma) + '.input3D[0].input3Dx', 90)
        cmds.connectAttr(str(attrObj) + '.angle_frontUp', str(frontUpsdk02_pma) + '.input3D[1].input3Dz')
        cmds.setAttr(str(frontUpsdk02_pma) + '.input3D[0].input3Dz', 90)
        cmds.setAttr(str(frontUpsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(frontUpsdk02_pma) + '.output3D.output3Dx', str(frontUpanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontUpanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(frontUpsdk02_pma) + '.output3D.output3Dz', str(frontUpanglesdk_cdn) + '.colorIfTrueG')
        cmds.connectAttr(str(attrObj) + '.angle_frontUp', str(frontUpanglesdk_cdn) + '.colorIfFalseG')
        cmds.connectAttr(str(frontUpanglesdk_cdn) + '.outColorR', str(frontUpsdk_md) + '.input1.input1X')
        cmds.connectAttr(str(frontUpanglesdk_cdn) + '.outColorG', str(frontUpsdk_md) + '.input2.input2X')
        cmds.setAttr(str(frontUpsdk_md) + '.operation', 2)
        frontUpsdkout_md = str(objpre) + '_frontUp_anglesdkout_md'
        cmds.createNode('multiplyDivide', n=frontUpsdkout_md)
        cmds.connectAttr(str(frontUpsdk_md) + '.outputX', str(frontUpsdkout_md) + '.input1.input1X')
        cmds.connectAttr(str(frontUpsdk_cdn) + '.outColorR', str(frontUpsdkout_md) + '.input2.input2X')
        cmds.setAttr(str(frontUpsdkout_md) + '.operation', 1)
        cmds.connectAttr(str(frontUpsdkout_md) + '.outputX', str(frontUpsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(frontUpsdk02_md) + '.input1.input1X')
        cmds.setAttr(str(frontUpsdk02_md) + '.operation', 1)
        cmds.connectAttr(str(frontUpsdk02_md) + '.output.outputX', str(attrObj) + '.frontUp_driver')
        cmds.connectAttr(str(outputInterval02) + '.outColorR', str(backUpsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(backUpsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(backUpsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(backUpsdk_cdn) + '.colorIfFalseR', 0)
        cmds.setAttr(str(backUpsdk_cdn) + '.colorIfTrueR', 1)
        backUpanglesdk_cdn = str(objpre) + '_backUp_anglesdk_condition'
        cmds.createNode('condition', n=backUpanglesdk_cdn)
        backUpsdk02_pma = str(objpre) + '_backUp_anglesdk_pma'
        cmds.createNode('plusMinusAverage', n=backUpsdk02_pma)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backUpanglesdk_cdn) + '.firstTerm')
        cmds.connectAttr(str(attrObj) + '.angle_backUp', str(backUpanglesdk_cdn) + '.secondTerm')
        cmds.setAttr(str(backUpanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backUpsdk02_pma) + '.input3D[1].input3Dx')
        cmds.setAttr(str(backUpsdk02_pma) + '.input3D[0].input3Dx', 180)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backUpsdk02_pma) + '.input3D[0].input3Dy')
        cmds.setAttr(str(backUpsdk02_pma) + '.input3D[1].input3Dy', 90)
        cmds.connectAttr(str(attrObj) + '.angle_backUp', str(backUpsdk02_pma) + '.input2D[0].input2Dx')
        cmds.setAttr(str(backUpsdk02_pma) + '.input2D[1].input2Dx', 90)
        cmds.connectAttr(str(attrObj) + '.angle_backUp', str(backUpsdk02_pma) + '.input3D[1].input3Dz')
        cmds.setAttr(str(backUpsdk02_pma) + '.input3D[0].input3Dz', 180)
        cmds.setAttr(str(backUpsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(backUpsdk02_pma) + '.output3D.output3Dx', str(backUpanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(backUpsdk02_pma) + '.output3D.output3Dy', str(backUpanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(backUpsdk02_pma) + '.output3D.output3Dz', str(backUpanglesdk_cdn) + '.colorIfTrueG')
        cmds.connectAttr(str(backUpsdk02_pma) + '.output2D.output2Dx', str(backUpanglesdk_cdn) + '.colorIfFalseG')
        cmds.connectAttr(str(backUpanglesdk_cdn) + '.outColorR', str(backUpsdk_md) + '.input1.input1X')
        cmds.connectAttr(str(backUpanglesdk_cdn) + '.outColorG', str(backUpsdk_md) + '.input2.input2X')
        cmds.setAttr(str(backUpsdk_md) + '.operation', 2)
        backUpsdkout_md = str(objpre) + '_backUp_anglesdkout_md'
        cmds.createNode('multiplyDivide', n=backUpsdkout_md)
        cmds.connectAttr(str(backUpsdk_md) + '.outputX', str(backUpsdkout_md) + '.input1.input1X')
        cmds.connectAttr(str(backUpsdk_cdn) + '.outColorR', str(backUpsdkout_md) + '.input2.input2X')
        cmds.setAttr(str(backUpsdkout_md) + '.operation', 1)
        cmds.connectAttr(str(backUpsdkout_md) + '.outputX', str(backUpsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(backUpsdk02_md) + '.input1.input1X')
        cmds.setAttr(str(backUpsdk02_md) + '.operation', 1)
        cmds.connectAttr(str(backUpsdk02_md) + '.output.outputX', str(attrObj) + '.backUp_driver')
        cmds.connectAttr(str(outputInterval03) + '.outColorR', str(frontBottomsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(frontBottomsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(frontBottomsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(frontBottomsdk_cdn) + '.colorIfFalseR', 0)
        cmds.setAttr(str(frontBottomsdk_cdn) + '.colorIfTrueR', 1)
        frontBottomanglesdk_cdn = str(objpre) + '_frontBottom_anglesdk_condition'
        cmds.createNode('condition', n=frontBottomanglesdk_cdn)
        frontBottomsdk02_pma = str(objpre) + '_frontBottom_anglesdk_pma'
        cmds.createNode('plusMinusAverage', n=frontBottomsdk02_pma)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontBottomanglesdk_cdn) + '.firstTerm')
        cmds.connectAttr(str(attrObj) + '.angle_frontBottom', str(frontBottomanglesdk_cdn) + '.secondTerm')
        cmds.setAttr(str(frontBottomanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontBottomsdk02_pma) + '.input3D[1].input3Dx')
        cmds.setAttr(str(frontBottomsdk02_pma) + '.input3D[0].input3Dx', 90)
        cmds.connectAttr(str(attrObj) + '.angle_frontBottom', str(frontBottomsdk02_pma) + '.input3D[1].input3Dz')
        cmds.setAttr(str(frontBottomsdk02_pma) + '.input3D[0].input3Dz', 90)
        cmds.setAttr(str(frontBottomsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(frontBottomsdk02_pma) + '.output3D.output3Dx', str(frontBottomanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(attrObj) + '.angle_base', str(frontBottomanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(frontBottomsdk02_pma) + '.output3D.output3Dz', str(frontBottomanglesdk_cdn) + '.colorIfTrueG')
        cmds.connectAttr(str(attrObj) + '.angle_frontBottom', str(frontBottomanglesdk_cdn) + '.colorIfFalseG')
        cmds.connectAttr(str(frontBottomanglesdk_cdn) + '.outColorR', str(frontBottomsdk_md) + '.input1.input1X')
        cmds.connectAttr(str(frontBottomanglesdk_cdn) + '.outColorG', str(frontBottomsdk_md) + '.input2.input2X')
        cmds.setAttr(str(frontBottomsdk_md) + '.operation', 2)
        frontBottomsdkout_md = str(objpre) + '_frontBottom_anglesdkout_md'
        cmds.createNode('multiplyDivide', n=frontBottomsdkout_md)
        cmds.connectAttr(str(frontBottomsdk_md) + '.outputX', str(frontBottomsdkout_md) + '.input1.input1X')
        cmds.connectAttr(str(frontBottomsdk_cdn) + '.outColorR', str(frontBottomsdkout_md) + '.input2.input2X')
        cmds.setAttr(str(frontBottomsdkout_md) + '.operation', 1)
        cmds.connectAttr(str(frontBottomsdkout_md) + '.outputX', str(frontBottomsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(frontBottomsdk02_md) + '.input1.input1X')
        cmds.setAttr(str(frontBottomsdk02_md) + '.operation', 1)
        cmds.connectAttr(str(frontBottomsdk02_md) + '.output.outputX', str(attrObj) + '.frontBottom_driver')
        cmds.connectAttr(str(outputInterval04) + '.outColorR', str(backBottomsdk_cdn) + '.firstTerm')
        cmds.setAttr(str(backBottomsdk_cdn) + '.secondTerm', 1)
        cmds.setAttr(str(backBottomsdk_cdn) + '.operation', 0)
        cmds.setAttr(str(backBottomsdk_cdn) + '.colorIfFalseR', 0)
        cmds.setAttr(str(backBottomsdk_cdn) + '.colorIfTrueR', 1)
        backBottomanglesdk_cdn = str(objpre) + '_backBottom_anglesdk_condition'
        cmds.createNode('condition', n=backBottomanglesdk_cdn)
        backBottomsdk02_pma = str(objpre) + '_backBottom_anglesdk_pma'
        cmds.createNode('plusMinusAverage', n=backBottomsdk02_pma)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backBottomanglesdk_cdn) + '.firstTerm')
        cmds.connectAttr(str(attrObj) + '.angle_backBottom', str(backBottomanglesdk_cdn) + '.secondTerm')
        cmds.setAttr(str(backBottomanglesdk_cdn) + '.operation', 2)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backBottomsdk02_pma) + '.input3D[1].input3Dx')
        cmds.setAttr(str(backBottomsdk02_pma) + '.input3D[0].input3Dx', 180)
        cmds.connectAttr(str(attrObj) + '.angle_base', str(backBottomsdk02_pma) + '.input3D[0].input3Dy')
        cmds.setAttr(str(backBottomsdk02_pma) + '.input3D[1].input3Dy', 90)
        cmds.connectAttr(str(attrObj) + '.angle_backBottom', str(backBottomsdk02_pma) + '.input3D[1].input3Dz')
        cmds.setAttr(str(backBottomsdk02_pma) + '.input3D[0].input3Dz', 180)
        cmds.connectAttr(str(attrObj) + '.angle_backBottom', str(backBottomsdk02_pma) + '.input2D[0].input2Dx')
        cmds.setAttr(str(backBottomsdk02_pma) + '.input2D[1].input2Dx', 90)
        cmds.setAttr(str(backBottomsdk02_pma) + '.operation', 2)
        cmds.connectAttr(str(backBottomsdk02_pma) + '.output3D.output3Dx', str(backBottomanglesdk_cdn) + '.colorIfTrueR')
        cmds.connectAttr(str(backBottomsdk02_pma) + '.output3D.output3Dy', str(backBottomanglesdk_cdn) + '.colorIfFalseR')
        cmds.connectAttr(str(backBottomsdk02_pma) + '.output3D.output3Dz', str(backBottomanglesdk_cdn) + '.colorIfTrueG')
        cmds.connectAttr(str(backBottomsdk02_pma) + '.output2D.output2Dx', str(backBottomanglesdk_cdn) + '.colorIfFalseG')
        cmds.connectAttr(str(backBottomanglesdk_cdn) + '.outColorR', str(backBottomsdk_md) + '.input1.input1X')
        cmds.connectAttr(str(backBottomanglesdk_cdn) + '.outColorG', str(backBottomsdk_md) + '.input2.input2X')
        cmds.setAttr(str(backBottomsdk_md) + '.operation', 2)
        backBottomsdkout_md = str(objpre) + '_backBottom_anglesdkout_md'
        cmds.createNode('multiplyDivide', n=backBottomsdkout_md)
        cmds.connectAttr(str(backBottomsdk_md) + '.outputX', str(backBottomsdkout_md) + '.input1.input1X')
        cmds.connectAttr(str(backBottomsdk_cdn) + '.outColorR', str(backBottomsdkout_md) + '.input2.input2X')
        cmds.setAttr(str(backBottomsdkout_md) + '.operation', 1)
        cmds.connectAttr(str(backBottomsdkout_md) + '.outputX', str(backBottomsdk02_md) + '.input2.input2X')
        cmds.connectAttr(str(objpre) + '_bridge' + '.driver_vulue', str(backBottomsdk02_md) + '.input1.input1X')
        cmds.setAttr(str(backBottomsdk02_md) + '.operation', 1)
        cmds.connectAttr(str(backBottomsdk02_md) + '.output.outputX', str(attrObj) + '.backBottom_driver')

    def bridgeAttrsMirror(self):
        bridgeGrps = cmds.ls(sl=True)
        for bridgeGrp in bridgeGrps:
            cmds.renameAttr(bridgeGrp + '.' + 'bottom_driver', 'L_out_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'frontBottom_driver', 'L_out_front_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'backBottom_driver', 'L_out_back_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'up_driver', 'R_out_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'frontUp_driver', 'R_out_front_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'backUp_driver', 'R_out_back_driver')

        cmds.select(bridgeGrps)

    def bridgeAttrsMirror2(self):
        bridgeGrps = cmds.ls(sl=True)
        for bridgeGrp in bridgeGrps:
            cmds.renameAttr(bridgeGrp + '.' + 'bottom_driver', 'out_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'frontBottom_driver', 'out_front_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'backBottom_driver', 'out_back_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'up_driver', 'inn_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'frontUp_driver', 'inn_front_driver')
            cmds.renameAttr(bridgeGrp + '.' + 'backUp_driver', 'inn_back_driver')

        cmds.select(bridgeGrps)

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

    def bridgeValue_to_angle(self):
        bridges = cmds.ls(sl=True)
        bridge_angles = []
        for bridge in bridges:
            bridge_grp = cmds.listRelatives(bridge, p=True)
            bridgeAttrs = cmds.listAttr(bridge, ud=1, u=1)
            bridge_angle = cmds.group(em=True, name=bridge + '_angle')
            cmds.delete(cmds.parentConstraint(bridge, bridge_angle, mo=0))
            cmds.parent(bridge_angle, bridge_grp)
            attrs = ['tx',
             'ty',
             'tz',
             'rx',
             'ry',
             'rz',
             'sx',
             'sy',
             'sz',
             'v']
            for attr in attrs:
                cmds.setAttr(bridge_angle + '.' + attr, lock=1, keyable=False, channelBox=False)

            for bridgeAttr in bridgeAttrs:
                cmds.addAttr(bridge_angle, ln=bridgeAttr)
                cmds.setAttr(bridge_angle + '.' + bridgeAttr, keyable=True)
                self.setDrivenKey(bridge + '.' + bridgeAttr, bridge_angle + '.' + bridgeAttr, [0, 1], [0, 180], 'linear', 'linear')

            bridge_angles.append(bridge_angle)

        cmds.select(bridge_angles)

    def test(self):
        import maya.cmds as cmds
        Obj_keyword = 'L_finger01'
        pos1Loc = cmds.spaceLocator(name=Obj_keyword + '_pos1Loc')[0]
        pos2Loc = cmds.spaceLocator(name=Obj_keyword + '_pos2Loc')[0]
        cmds.setAttr(pos1Loc + '.tz', 5)
        cmds.setAttr(pos2Loc + '.tx', 5)
        angleBetweenNode = cmds.createNode('angleBetween')
        cmds.connectAttr(pos1Loc + '.translate', angleBetweenNode + '.vector1')
        cmds.connectAttr(pos2Loc + '.translate', angleBetweenNode + '.vector2')