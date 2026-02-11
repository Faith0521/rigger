from imp import reload
import maya.cmds as cmds
import pymel.versions as version
import Faith.maya_utils.rigging_utils as rig
reload(rig)


class Follic(object):

    def __init__(self):
        self.midGrpCB = None
        self.locCreateFollicBut = None
        self.version = version.current()

    def win(self):
        ver = 'v1.0'
        winName = 'JunFollicTool'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        cmds.window(winName, t='Jun FollicTool' + ver)
        cmds.menuBarLayout()
        cmds.menu(label='File')
        cmds.menuItem(label='root', c=lambda *args: self.root())
        cmds.menu(label='Help', helpMenu=True)
        cmds.menuItem(label='help')
        cmds.setParent('..')
        child1 = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout('UVModelwinRL', numberOfColumns=2, vis=0)
        cmds.button(l=u'getUvValueModel:', w=100, c=lambda *args: self.loadObj(1, 'UVmodelTF'))
        cmds.textField('UVmodelTF', text=u'', w=140)
        cmds.setParent(child1)
        cmds.rowLayout(numberOfColumns=4, columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        cmds.text(l=u'\u63a7\u5236\u65b9\u5f0f:', align='right', width=50)
        cmds.radioCollection()
        cmds.radioButton('patentConstrRB', label='parentConstr', align='left', sl=True, w=90)
        cmds.radioButton('pointConstrRB', label='pointConstr', w=90)
        cmds.setParent('..')
        self.midGrpCB = cmds.checkBox('mid_grp', label='create_mid_grp', value=0, w=60)
        self.locCreateFollicBut = cmds.button(
            l=u'\u9009\u4e2d\u88ab\u6bdb\u56ca\u63a7\u5236\u7269\u4f53\n\u52a0\u9009\u9489\u6bdb\u56ca\u6a21\u578b\u521b\u5efa\u6bdb\u56ca',
            h=30, bgc=[0, 0.5, 0],
            c=lambda *args: self.selectObjCreateFollic(cmds.textField('follicNameTF', q=True, text=True)))
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(l=u'follicName:', w=60)
        cmds.textField('follicNameTF', text=u'follic_Name', w=140)
        cmds.setParent(child1)
        cmds.rowLayout(numberOfColumns=3)
        cmds.text(l=u'follic\u6570\u91cf:', w=60)
        cmds.textField('follicNumTF', text=20, w=40)
        cmds.text(l=u'mean\u8868\u793aUV\u503c\u5e73\u5747\u9012\u589e:')
        cmds.setParent(child1)
        cmds.rowLayout(numberOfColumns=4)
        cmds.text(l=u'U\u503c:', w=60)
        cmds.textField('uTF', text='mean', w=70)
        cmds.text(l=u'V\u503c:', w=27)
        cmds.textField('vTF', text='0.5', w=70)
        cmds.setParent(child1)
        cmds.button(l=u'\u5e73\u5747\u521b\u5efa\u6bdb\u56ca', h=30, bgc=[0.5, 0.4, 0.33],
                    c=lambda *args: self.averageCreateFollic(cmds.textField('follicNumTF', q=True, text=True),
                                                             cmds.textField('follicNameTF', q=True, text=True),
                                                             [cmds.textField('uTF', q=True, text=True),
                                                              cmds.textField('vTF', q=True, text=True)]))
        cmds.button(l=u'\u66ff\u6362\u6bdb\u56ca\u6a21\u578b\n(\u9009\u4e2d\u6bdb\u56ca\u52a0\u9009\u6a21\u578b)', h=30,
                    c=lambda *args: self.replaceFollicModel())
        cmds.showWindow()

    def root(self):
        cmds.rowLayout('UVModelwinRL', e=True, vis=1)

    def loadObj(self, loadnum, tfName):
        sels = cmds.ls(sl=True)
        if len(sels) == loadnum:
            if loadnum > 1:
                cmds.textField(tfName, e=True, text=sels[:loadnum])
            elif loadnum == 1:
                cmds.textField(tfName, e=True, text=sels[0])
        elif loadnum == '':
            cmds.textField(tfName, e=True, text=sels)
        else:
            cmds.warning(u'\u8bf7\u9009\u62e9' + str(loadnum) + u'\u4e2a\u7269\u4f53')

    def queryShapeNumber(self, obj):
        shapes = cmds.listRelatives(obj, s=True)
        showShapes = []
        for shape1 in shapes:
            intermediateObject = cmds.getAttr(shape1 + '.intermediateObject')
            if intermediateObject == 0:
                showShapes.append(shape1)

        shapeNum = len(showShapes)
        return shapeNum, showShapes

    @staticmethod
    def closestPointOnModel(modelShape, pointObjs):
        modelShapeType = cmds.nodeType(modelShape)
        Us = []
        Vs = []
        UVs = []
        closest_Point = []
        for pointObj in pointObjs:
            grp = cmds.group(em=True, name=pointObj + '_point')
            cmds.parentConstraint(pointObj, grp, mo=False)
            UV = []
            minMaxRangeU = 1
            minMaxRangeV = 1
            if modelShapeType == 'nurbsSurface':
                closest_Point = ['closestPointOnSurface',
                                 grp + '_cpos',
                                 'local',
                                 'inputSurface']
                minMaxRangeU = int(cmds.getAttr(modelShape + '.minMaxRangeU')[0][1])
                minMaxRangeV = int(cmds.getAttr(modelShape + '.minMaxRangeV')[0][1])
            elif modelShapeType == 'mesh':
                closest_Point = ['closestPointOnMesh',
                                 grp + '_cpom',
                                 'outMesh',
                                 'inMesh']
            closest_PointNode = cmds.createNode(closest_Point[0], name=closest_Point[1])
            cmds.connectAttr(grp + '.translateX', closest_PointNode + '.inPosition.inPosition' + 'X')
            cmds.connectAttr(grp + '.translateY', closest_PointNode + '.inPosition.inPosition' + 'Y')
            cmds.connectAttr(grp + '.translateZ', closest_PointNode + '.inPosition.inPosition' + 'Z')
            cmds.connectAttr(modelShape + '.' + closest_Point[2], closest_PointNode + '.' + closest_Point[3])
            U = cmds.getAttr(closest_PointNode + '.result.parameterU') / minMaxRangeU
            V = cmds.getAttr(closest_PointNode + '.result.parameterV') / minMaxRangeV
            Us.append(U)
            Vs.append(V)
            UV.append(U)
            UV.append(V)
            UVs.append(UV)
            cmds.delete(closest_PointNode, grp)
        return Us, Vs, UVs

    def follicCreate(self, modelShape, follicNum, Us=None, Vs=None, nameStart='', follicNames=[], UVs=None):
        UV_MeanNum = None
        U_value = 0
        V_value = 0
        if Vs is None:
            Vs = []
        if Us is None:
            Us = []
        modelShapeType = cmds.nodeType(modelShape)
        if follicNum == 1:
            UV_MeanNum = 0.5
        elif follicNum == 0:
            cmds.error('fuck you')
        else:
            UV_MeanNum = float(1.0 / (follicNum - 1.0))
        follicList = []
        if self.version <= 2020:
            if Us == 'mean':
                Us = [float(UV_MeanNum * i) for i in range(follicNum)]
            elif isinstance(Us, float):
                Us = [float(Us) for i in range(follicNum)]
            if Vs == 'mean':
                Vs = [float(UV_MeanNum * i) for i in range(follicNum)]
            elif isinstance(Vs, float):
                Vs = [float(Vs) for i in range(follicNum)]
            if (not isinstance(Us, list)) or (not isinstance(Vs, list)):
                return
            model = cmds.listRelatives(modelShape,
                                       parent=True)[0]

            follicList = [cmds.createNode("transform", n=follicNames[i]) for i in range(follicNum)]

            if UVs is None:
                rig.uvPin(model, [[u,v] for u,v in zip(Us, Vs)], follicList=follicList, type=modelShapeType)
            else:
                rig.uvPin(model, UVs, follicList=follicList, type=modelShapeType)
        else:
            for i in range(follicNum):
                if Us == 'mean':
                    U_value = float(UV_MeanNum * i)
                elif type(Us) == float:
                    U_value = Us
                elif type(Us) == list:
                    U_value = Us[i]
                if Vs == 'mean':
                    V_value = float(UV_MeanNum * i)
                elif type(Vs) == float:
                    V_value = Vs
                elif type(Vs) == list:
                    V_value = Vs[i]

                follic_shape = follicNames[i] + "Shape"
                follic_shape = cmds.createNode('follicle', n=follic_shape)
                cmds.setAttr(follic_shape + '.parameterU', U_value)
                cmds.setAttr(follic_shape + '.parameterV', V_value)
                follic = cmds.listRelatives(follic_shape, p=True)[0]
                cmds.connectAttr(follic_shape + '.outTranslate', follic + '.translate')
                cmds.connectAttr(follic_shape + '.outRotate', follic + '.rotate')
                cmds.connectAttr(modelShape + '.worldMatrix[0]', follic_shape + '.inputWorldMatrix')
                if modelShapeType == 'nurbsSurface':
                    cmds.connectAttr(modelShape + '.local', follic_shape + '.inputSurface')
                elif modelShapeType == 'mesh':
                    cmds.connectAttr(modelShape + '.outMesh', follic_shape + '.inputMesh')
                follicList.append(follic)
        cmds.select(cl=1)

        return follicList

    @staticmethod
    def CreateCtrl(pointObjs, follicList):
        for i, pointObj in enumerate(pointObjs):
            cmds.select(pointObj)
            cmds.joint(name=pointObj + '_jnt')

    def replaceFollicModel(self):
        sels = cmds.ls(sl=True)
        follics = sels[:-1]
        model = sels[-1]
        shapeData = self.queryShapeNumber(model)
        shapeNum = shapeData[0]
        modelShape = shapeData[1]
        if shapeNum == 1:
            modelShape = modelShape[0]
            modelShapeType = cmds.objectType(modelShape)
            for follic in follics:
                follic_shape = cmds.listRelatives(follic, s=True)[0]
                cmds.connectAttr(modelShape + '.worldMatrix[0]', follic_shape + '.inputWorldMatrix', f=True)
                if modelShapeType == 'nurbsSurface':
                    cmds.connectAttr(modelShape + '.local', follic_shape + '.inputSurface', f=True)
                elif modelShapeType == 'mesh':
                    cmds.connectAttr(modelShape + '.outMesh', follic_shape + '.inputMesh', f=True)

    def selectObjCreateFollic(self, follicName, *args):
        patentConstr = cmds.radioButton('patentConstrRB', q=True, sl=True)
        pointConstr = cmds.radioButton('pointConstrRB', q=True, sl=True)
        getUvValueModel = cmds.textField('UVmodelTF', q=True, text=True)
        sels = cmds.ls(sl=True)

        pointObjs = sels[0:-1]
        follicModel = sels[-1]
        rivetModel = follicModel
        # rivetModel = rig.create_and_process_planes(follicModel, pointObjs)
        if getUvValueModel == '':
            getUvValueModel = rivetModel

        follicModelShapeData = self.queryShapeNumber(rivetModel)
        getUvValueModelShapeData = self.queryShapeNumber(getUvValueModel)
        follicList = []
        if follicModelShapeData[0] == 1 and getUvValueModelShapeData[0] == 1:
            follicmodelShape = follicModelShapeData[1][0]
            getUvValueModelShape = getUvValueModelShapeData[1][0]
            UV = self.closestPointOnModel(getUvValueModelShape, pointObjs)
            Us = UV[0]
            Vs = UV[1]
            follicNum = len(pointObjs)
            follicNames = []
            for follicName in pointObjs:
                follicName = follicName + '_follic'
                follicNames.append(follicName)

            follicList = self.follicCreate(follicmodelShape, follicNum, Us, Vs, 1, follicNames, UVs=UV[-1])
            self.midGrpCB = cmds.checkBox('mid_grp', q=True, value=True)
            for i in range(follicNum):
                conObjgGrp = follicList[i]
                if self.midGrpCB == 1:
                    conObjgGrp = cmds.group(em=True, name='con_' + pointObjs[i])
                    cmds.delete(cmds.parentConstraint(pointObjs[i], conObjgGrp, mo=0))
                    cmds.parent(conObjgGrp, follicList[i])
                if patentConstr:
                    cmds.parentConstraint(conObjgGrp, pointObjs[i], mo=1)
                elif pointConstr:
                    cmds.pointConstraint(conObjgGrp, pointObjs[i], mo=1)
                else:
                    cmds.parent(pointObjs[i], conObjgGrp)

        return follicList

    def averageCreateFollic(self, follicNum, follicName, uv, *args):
        sels = cmds.ls(sl=True)
        pointObjs = sels[0:-1]
        model = sels[-1]
        modelShapeData = self.queryShapeNumber(model)
        if modelShapeData[0] == 1:
            modelShape = modelShapeData[1][0]
            follicNum = int(follicNum)
            try:
                u = float(uv[0])
            except ValueError:
                u = uv[0]

            try:
                v = float(uv[1])
            except ValueError:
                v = uv[1]
            follicNames = []
            for i in range(follicNum):
                follicName1 = follicName + '_0' + str(i + 1) + '_rivet'
                follicNames.append(follicName1)
            follicList = self.follicCreate(modelShape, follicNum, u, v, 1, follicNames)
