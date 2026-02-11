# Embedded file name: E:/JunCmds/tool/createVisibility.py
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re


class CreateVis(object):

    def __init__(self, setName='set_ctrl'):
        self.setName = setName
        if cmds.objExists('ac_cn_settings_ctrl') == 1:
            self.visCtrlAttr = 'ac_cn_settings_ctrl' + '.ctrlVis'
            self.geo_display_typeAttr = 'ac_cn_settings_ctrl' + '.geo_display_type'
        elif cmds.objExists('ac_cn_settings') == 1:
            self.visCtrlAttr = 'ac_cn_settings' + '.ctrlVis'
            self.geo_display_typeAttr = 'ac_cn_settings' + '.geo_display_type'
        else:
            self.visCtrlAttr = ''
            self.geo_display_typeAttr = ''

    def Create_vis_UI(self):
        visUI = 'visUi'
        if cmds.window(visUI, ex=True):
            cmds.deleteUI(visUI, window=True)
        cmds.window(visUI, t='createVIS', s=True, tb=True)
        ws = (90, 10, 80)
        cmds.columnLayout('main_columnLY', adj=True)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text('Asset Name:')
        cmds.textField('CN')
        cmds.button(l='Create', c=lambda i: self.ui_createVis())
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text('CtrlVis Attr:')
        cmds.textField('ctrlVisTF', text=self.visCtrlAttr, en=0)
        cmds.button(l='Load Attr', c=lambda *args: self.Load('ctrlVisTF'))
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, columnWidth3=ws, adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
        cmds.text('DisplayType Attr:')
        cmds.textField('GeoDisplayTypeTF', text=self.geo_display_typeAttr, en=0)
        cmds.button(l='Load Attr', c=lambda *args: self.Load('GeoDisplayTypeTF'))
        cmds.setParent('..')
        cmds.setParent('main_columnLY')
        cmds.button(l='Ctrl Vis\nModel DisplayType ', h=30, c=lambda i: self.connectVisAttr())
        cmds.button(l='Model \nVis', h=40, c=lambda i: self.MeshconnectVisAttr())
        cmds.button(l='Replace \nVis', h=40, c=lambda i: self.ReplaceVisAttr())
        cmds.frameLayout(
            label=u'\u4ee5\u4e0b\u6309\u94ae\u9700\u8981\u9009\u4e2d\u663e\u793a\u9690\u85cf\u7684\u7269\u4f53\u6216\u7ec4\u624d\u80fd\u8fd0\u884c',
            cl=0, cll=True, bgc=[0.3, 0.3, 0])
        cmds.rowColumnLayout(numberOfColumns=8)
        cmds.button(l='FaceLwModel\nSwit', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.FaceMode', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [0, 1]))
        cmds.separator(style='single')
        cmds.button(l='FaceHiModel\nSwit', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.FaceMode', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [1, 0]))
        cmds.separator(style='single')
        cmds.button(l='BodyLwModel\nSwit', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.BodyMode', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [0, 1]))
        cmds.separator(style='single')
        cmds.button(l='BodyHiModel\nSwit', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.BodyMode', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [1, 0]))
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=8)
        cmds.button(l='HairModel\nVis', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.HairModeVis', cmds.ls(sl=True), '.lodVisibility',
                                                  [0, 1], [0, 1]))
        cmds.separator(style='single')
        cmds.button(l='FaceCtrl\nVis', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.facial_ctrl_vis', cmds.ls(sl=True),
                                                  '.visibility', [0, 1], [0, 1]))
        cmds.separator(style='single')
        cmds.button(l='SecCtrl\nVis', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.SecCtrlVis', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [0, 1]))
        cmds.separator(style='single')
        cmds.button(l='FaceSecCtrl\nVis', h=35, w=80,
                    c=lambda i: self.setDrivenKey('ac_cn_settings_ctrl.FaceSecCtrlVis', cmds.ls(sl=True), '.visibility',
                                                  [0, 1], [0, 1]))
        cmds.setParent('main_columnLY')
        cmds.showWindow(visUI)
        assteName = self.getAssteName()
        cmds.textField('CN', e=True, text=assteName)

    def Load(self, Field):
        sels = cmds.ls(sl=True)
        if len(sels) != 1:
            cmds.error('please select one object')
        selectAttr = self.querySelectedAttr()
        longAttrList = selectAttr[1]
        if len(longAttrList) != 1:
            cmds.error('please select one Attribute')
        cmds.textField(Field, e=True, text=sels[0] + '.' + longAttrList[0])
        return sels[0] + '.' + longAttrList[0]

    def getAssteName(self):
        assteName = ''
        sels = cmds.ls(sl=True)
        mel.eval('SelectAll;')
        selupObjs = cmds.ls(sl=True)
        transformupObjs = []
        for selupObj in selupObjs:
            if cmds.objectType(selupObj) == 'transform' and cmds.listRelatives(selupObj,
                                                                               s=1) is None and cmds.listRelatives(
                    selupObj, ad=1, type='mesh') is not None:
                transformupObjs.append(selupObj)

        cmds.select(sels)
        if len(transformupObjs) == 1:
            assteName = transformupObjs[0]
        elif len(transformupObjs) > 1:
            for transformupObj in transformupObjs:
                if 'geometry' in str(cmds.listRelatives(transformupObj, ad=1)) or 'render_model' in str(
                        cmds.listRelatives(transformupObj, ad=1)):
                    assteName = transformupObj

        else:
            assteName = ''
        return assteName

    def querySelectedAttr(self):
        """
        #--------------------------------------------------------------------------------
        get Selected attribute name form mainChannelBox
        #--------------------------------------------------------------------------------
        """
        shortAttrList = cmds.channelBox('mainChannelBox', q=True, sma=True)
        longAttrList = []
        if shortAttrList is None:
            shortAttrList = []
        else:
            for shortAttr in shortAttrList:
                longAttr = cmds.attributeName('.' + shortAttr, l=True)
                longAttrList.append(longAttr)

        return shortAttrList, longAttrList

    def ui_createVis(self):
        textCtrl = cmds.textField('CN', q=True, text=True)
        self.createVis(charactor=textCtrl)
        cmds.textField('ctrlVisTF', e=True, text='ac_cn_settings_ctrl' + '.ctrlVis')
        cmds.textField('GeoDisplayTypeTF', e=True, text='ac_cn_settings_ctrl' + '.geo_display_type')

    def lockAttr(self, obj='', attr=None):
        if attr is None:
            attr = ['']
        for at in attr:
            cmds.setAttr(obj + '.' + at, lock=True, keyable=False, channelBox=False)

    def createVis(self, charactor=''):
        assteName = self.getAssteName()
        assteName2 = cmds.textField('CN', q=True, text=True)
        if assteName != '':
            objBoxSize = cmds.getAttr(assteName + '.boundingBoxSize')[0]
        elif cmds.objExists(assteName2):
            objBoxSize = cmds.getAttr(assteName2 + '.boundingBoxSize')[0]
        else:
            objBoxSize = (200, 150, 100)
        if objBoxSize == (0.0, 0.0, 0.0):
            objBoxSize = (200, 150, 100)

        textName = charactor
        if textName != '':
            tempObj = cmds.textCurves(ch=False, f='Times New Roman|h-13|w400|c0', t=textName)[0]
            TextCurve = cmds.ls('makeTextCurves*')
            cmds.delete(TextCurve)
            cmds.makeIdentity(tempObj, apply=True, t=True, r=True, s=True)
            allObj = cmds.listRelatives(tempObj, ad=True)
            allObj.append(tempObj)
            shapeList = []
            for obj in allObj:
                if cmds.nodeType(obj) == 'nurbsCurve':
                    shapeList.append(obj)

            visCtrl = cmds.group(em=True, n='ac_cn_settings_ctrl')
            for i, shape in enumerate(shapeList):
                cmds.parent(shape, visCtrl, r=True, s=True)
                cmds.setAttr(shape + '.overrideEnabled', 1)
                cmds.setAttr(shape + '.overrideColor', 17)

            cmds.delete(tempObj)
            ctrlShape = cmds.listRelatives(visCtrl, s=True)
            for i, s in enumerate(ctrlShape):
                cmds.rename(s, visCtrl + str(i + 1) + 'Shape')

            cmds.addAttr(visCtrl, ln='ctrlVis', at='long', k=True, dv=1, min=0, max=1)
            cmds.setAttr(visCtrl + '.ctrlVis', k=False, cb=True)
            cmds.addAttr(visCtrl, ln='geo_display_type', at='enum', en='Normal:Template:refrence', k=True)
            cmds.setAttr(visCtrl + '.geo_display_type', k=False, cb=True)
            visCtrlZero = str(visCtrl) + '_zero'
            cmds.group(visCtrl, n=visCtrlZero)
            grp = cmds.group(em=True)
            cmds.delete(cmds.pointConstraint(grp, visCtrlZero, mo=0), grp)
            cmds.makeIdentity(visCtrlZero, apply=True, t=True, r=True, s=True)
            self.lockAttr(obj=visCtrl, attr=['tx',
                                             'ty',
                                             'tz',
                                             'rx',
                                             'ry',
                                             'rz',
                                             'sx',
                                             'sy',
                                             'sz',
                                             'v'])
            objLength = objBoxSize[0]
            objWidth = objBoxSize[2]
            objHeight = objBoxSize[1]
            if objLength / objWidth > 0.1:
                pass
            else:
                cmds.setAttr(visCtrlZero + '.ry', -90)
            assetLengthWidthRatio = (objLength + objWidth + objHeight) / 28
            cmds.setAttr(visCtrlZero + '.scale', assetLengthWidthRatio, assetLengthWidthRatio, assetLengthWidthRatio)
            cmds.setAttr(str(visCtrlZero) + '.translateY', objHeight * 1.05 + 1.0)
            cmds.select(visCtrlZero)
        else:
            visCtrlZero = ''
        return visCtrlZero

    def connectVisAttr(self):
        visCtrl = cmds.textField('ctrlVisTF', q=True, text=True).split('.')[0]
        ctrlVisAttr = cmds.textField('ctrlVisTF', q=True, text=True).split('.')[-1]
        GeoDisplayTypeAttr = cmds.textField('GeoDisplayTypeTF', q=True, text=True)
        if not cmds.objExists(visCtrl):
            cmds.error(u'---\u8bf7\u52a0\u8f7d\u6b63\u786e\u7684\u7269\u4f53\u5c5e\u6027---')
        hideJntAttr = 'globalctrl_grp.hideJnt'
        if cmds.objExists(hideJntAttr):
            cmds.connectAttr(visCtrl + '.jntHide', hideJntAttr)
            cmds.setAttr(hideJntAttr, l=True, k=False)
        meshList = cmds.ls(type='mesh')

        if meshList:
            for mesh in meshList:
                if mesh.startswith("CTRL") or mesh.startswith("FRM") or mesh.startswith("TEXT"):
                    continue
                parentObj = cmds.listRelatives(mesh, p=True, c=False)
                if '_cntr' in parentObj[0]:
                    cmds.setAttr(mesh + '.overrideEnabled', 0)
                elif '_adj' in parentObj[0]:
                    cmds.setAttr(mesh + '.overrideEnabled', 0)
                else:
                    cmds.setAttr(mesh + '.overrideEnabled', 1)
                    spurceConnect = cmds.listConnections(mesh + '.overrideDisplayType', s=True)
                    if spurceConnect is None:
                        cmds.connectAttr(GeoDisplayTypeAttr, mesh + '.overrideDisplayType')

        annotationList = cmds.ls(type='annotationShape')
        if annotationList:
            for ann in annotationList:
                input = cmds.listConnections(ann + '.v', s=True, d=False, p=True)
                if input:
                    pass
                else:
                    cmds.connectAttr(visCtrl + '.' + ctrlVisAttr, ann + '.v')

        curvesList = cmds.ls(type='nurbsCurve')
        facialCtrl_all = []
        facial_ctrl = cmds.ls('*_cntr', '*_Controller', '*_adj', '*_sec_ctrl')
        for fc in facial_ctrl:
            shapes = cmds.listRelatives(fc, s=True)
            if shapes:
                for sh in shapes:
                    if fc not in facialCtrl_all:
                        facialCtrl_all.append(sh)
                    if fc not in curvesList:
                        curvesList.append(sh)

        ac_cn_settings_ctrl = visCtrl
        ac_cn_settings_ctrlShapes = cmds.listRelatives(ac_cn_settings_ctrl, s=True)
        for ac_cn_settings_ctrlShape in ac_cn_settings_ctrlShapes:
            curvesList.remove(ac_cn_settings_ctrlShape)

        for curve in curvesList:
            if curve in facialCtrl_all:
                connObj_attr = cmds.listConnections(curve + '.v', s=True, d=False, p=True)
                parentTrans_node = cmds.listRelatives(curve, p=True)
                if parentTrans_node[0] == str(visCtrl) and connObj_attr is not None:
                    cmds.disconnectAttr(connObj_attr[0], str(curve) + '.v')
                    cmds.setAttr(str(curve) + '.v', 1)
                else:
                    if connObj_attr:
                        cmds.disconnectAttr(connObj_attr[0], str(curve) + '.v')
                        cmds.setAttr(str(curve) + '.v', 1)
                    connObj = cmds.listConnections(curve + '.v', s=True, d=False, p=True)
                    if connObj == None and visCtrl != parentTrans_node:
                        spurceConnect = cmds.listConnections(str(curve) + '.v', s=True)
                        attrChanale = cmds.listAttr(visCtrl)
                        if 'facial_ctrl_vis' not in attrChanale:
                            cmds.addAttr(visCtrl, ln='facial_ctrl_vis', k=True, min=0, max=1, dv=1)
                            cmds.setAttr(str(visCtrl) + '.facial_ctrl_vis', cb=True)
                        if spurceConnect == None:
                            if curve != visCtrl:
                                cmds.connectAttr(str(visCtrl) + '.facial_ctrl_vis', str(curve) + '.v')
            else:
                connObj_attr = cmds.listConnections(curve + '.lodVisibility', s=True, d=False, p=True)
                parentTrans_node = cmds.listRelatives(curve, p=True)
                if parentTrans_node[0] == str(visCtrl) and connObj_attr != None:
                    cmds.disconnectAttr(connObj_attr[0], str(curve) + '.lodVisibility')
                    cmds.setAttr(str(curve) + '.lodVisibility', 1)
                else:
                    if connObj_attr:
                        cmds.disconnectAttr(connObj_attr[0], str(curve) + '.lodVisibility')
                        cmds.setAttr(str(curve) + '.lodVisibility', 1)
                    connObj_attr = cmds.listConnections(curve + '.lodVisibility', s=True, d=False, p=True)
                    if connObj_attr == None and visCtrl != parentTrans_node:
                        spurceConnect = cmds.listConnections(str(curve) + '.lodVisibility', s=True, d=False)
                        if spurceConnect == None:
                            if curve != visCtrl:
                                if cmds.getAttr(str(curve) + '.lodVisibility') == 0:
                                    pass
                                else:
                                    cmds.setAttr(str(curve) + '.lodVisibility', lock=False)
                                    cmds.connectAttr(str(visCtrl) + '.' + ctrlVisAttr, str(curve) + '.lodVisibility')

        return

    def MeshconnectVisAttr(self):
        GeoDisplayTypeAttr = cmds.textField('GeoDisplayTypeTF', q=True, text=True)
        meshList = cmds.ls(type='mesh')
        if meshList != []:
            for mesh in meshList:
                if mesh.startswith("CTRL") or mesh.startswith("FRM") or mesh.startswith("TEXT"):
                    continue
                parentObj = cmds.listRelatives(mesh, p=True, c=False)
                if '_cntr' in parentObj[0]:
                    cmds.setAttr(mesh + '.overrideEnabled', 0)
                    print(mesh, 1)
                elif '_adj' in parentObj[0]:
                    cmds.setAttr(mesh + '.overrideEnabled', 0)
                    print(mesh, 2)
                else:
                    cmds.setAttr(mesh + '.overrideEnabled', 1)
                    spurceConnect = cmds.listConnections(mesh + '.overrideDisplayType', s=True)
                    print(mesh, 3)
                    if spurceConnect == None:
                        cmds.connectAttr(GeoDisplayTypeAttr, mesh + '.overrideDisplayType')

        return

    def ReplaceVisAttr(self):
        """

        :return:
        """
        old_vis_ctrl = ""
        old_vis_ctrl_zero = ""
        if cmds.objExists('ac_cn_settings_ctrl') and cmds.objExists('ac_cn_settings_ctrl_zero'):
            old_vis_ctrl = cmds.rename('ac_cn_settings_ctrl', 'ac_cn_settings_ctrl_old')
            old_vis_ctrl_zero = cmds.rename('ac_cn_settings_ctrl_zero', 'ac_cn_settings_ctrl_zero_old')

        [cmds.delete(s) for s in cmds.listRelatives(old_vis_ctrl, ad=1, s=1)]

        self.ui_createVis()
        allShapeList = cmds.listRelatives('ac_cn_settings_ctrl', ad=1, s=1)
        [cmds.parent(s, old_vis_ctrl, r=1, s=1) for s in allShapeList]
        cmds.delete('ac_cn_settings_ctrl_zero')

        cmds.rename('ac_cn_settings_ctrl_old', 'ac_cn_settings_ctrl')
        cmds.rename('ac_cn_settings_ctrl_zero_old', 'ac_cn_settings_ctrl_zero')

    def setDrivenKey(self, driver, drivenObjs, drivenAttr, driverNums, drivenNums):
        visCtrl = 'ac_cn_settings_ctrl'
        visCtrlAttrs = cmds.listAttr(visCtrl)
        if 'FaceMode' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='FaceMode', at='enum', en='High:Low', k=True)
            cmds.setAttr(visCtrl + '.FaceMode', k=False, cb=0)
        if 'BodyMode' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='BodyMode', at='enum', en='High:Low', k=True)
            cmds.setAttr(visCtrl + '.BodyMode', k=False, cb=0)
        if 'HairModeVis' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='HairModeVis', at='long', k=True, dv=1, min=0, max=1)
            cmds.setAttr(visCtrl + '.HairModeVis', k=False, cb=0)
        if 'FaceCtrlVis' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='FaceCtrlVis', at='long', k=True, dv=1, min=0, max=1)
            cmds.setAttr(visCtrl + '.FaceCtrlVis', k=False, cb=0)
        if 'SecCtrlVis' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='SecCtrlVis', at='long', k=True, dv=1, min=0, max=1)
            cmds.setAttr(visCtrl + '.SecCtrlVis', k=False, cb=0)
        if 'FaceSecCtrlVis' not in visCtrlAttrs:
            cmds.addAttr(visCtrl, ln='FaceSecCtrlVis', at='long', k=True, dv=1, min=0, max=1)
            cmds.setAttr(visCtrl + '.FaceSecCtrlVis', k=False, cb=0)

        cmds.setAttr(driver, k=False, cb=1)
        num = len(driverNums)
        for drivenObj in drivenObjs:
            for i in range(num):
                animCv = cmds.setDrivenKeyframe(drivenObj + drivenAttr, currentDriver=driver, driverValue=driverNums[i],
                                                v=drivenNums[i], itt='linear', ott='linear')
                print(driver, drivenObj + drivenAttr, driverNums[i], drivenNums[i])

        print('ok')
