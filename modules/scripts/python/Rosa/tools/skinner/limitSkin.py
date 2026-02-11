import maya.cmds as mc
import maya.OpenMaya as OpenMaya
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.mel as mel


class LimitSkinWeightClss():

    def __init__(self):
        pass

    def searchSkinClusterByName(self, model):
        obj = model
        skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + obj + "\")")
        if skinNode != '':
            return skinNode
        else:
            return False

    def unlockliw(self, jntList):
        for one in jntList:
            mc.setAttr(one + '.liw', 0)

    def setLimit(self, limitNum, decimal):
        selectionList = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(selectionList)
        if selectionList.isEmpty():
            return None
        dagpath = OpenMaya.MDagPath()
        component = OpenMaya.MObject()
        # the 1th object selected!!
        selectionList.getDagPath(0, dagpath, component)
        modelShape = dagpath.fullPathName()
        if mc.nodeType(modelShape) == 'mesh':
            model = mc.listRelatives(modelShape, parent=True)[0]
        if mc.nodeType(modelShape) == 'transform':
            model = modelShape
        # model = mc.ls(sl=True)[0]
        if len(model) == 0:
            mc.error('Sorry,you must select one poly mesh before.')
        else:
            skinNode = self.searchSkinClusterByName(model)
        if skinNode == 0:
            mc.error('------>>>Sorry , can not find skincluster on you select mesh!')
        skinJoints = mc.skinCluster(skinNode, q=True, inf=True)
        self.unlockliw(skinJoints)
        jntNum = len(skinJoints)
        if not limitNum < jntNum:
            return None
        vertexCount = mc.polyEvaluate(model, v=True)
        ################################################################################### mitvtx
        mitvertex = OpenMaya.MItMeshVertex(dagpath, component)
        # tempSkinList_2[194]
        # len(reWeightList)
        # reWeightList[91]
        mitvertex.reset()
        countVtx = mitvertex.count()
        print('countVtx : %s' % countVtx)
        amount = 0
        mc.progressWindow(title="MDL:%s" % model, progress=amount, max=vertexCount,
                            status='Reset weight: -/-',
                            isInterruptable=True)
        while not mitvertex.isDone():
            if mc.progressWindow(query=True, isCancelled=True):
                break
            currentIndex = mitvertex.index()
            ########################get skin
            weightList = mc.skinPercent(skinNode, '%s.vtx[%s]' % (model, currentIndex), query=True, v=True)
            # sort
            sortList = sorted(weightList, reverse=True)
            # get the index list.
            indexList = []
            for i in range(0, limitNum):
                for x in range(len(weightList)):
                    if sortList[i] == weightList[x]:
                        if x not in indexList:
                            indexList.append(x)
                            break
            # compute new weightlsit.
            totel = 0.000
            for v in indexList:
                totel = totel + weightList[v]
            # create new [(),(),()]
            jntWeight = []
            exceptLast = 0.00
            for i in range(limitNum):
                newWeight = round(weightList[indexList[i]] / totel, decimal)
                if i < limitNum - 1:
                    exceptLast = exceptLast + newWeight
                    jntWeight.append((skinJoints[indexList[i]], newWeight))
                else:
                    # round(weightList[indexList[i]]/totel,decimal)
                    jntWeight.append((skinJoints[indexList[i]], round(1.000 - exceptLast, decimal)))
            mc.skinPercent(skinNode, '%s.vtx[%s]' % (model, currentIndex), transformValue=jntWeight)
            amount += 1
            mc.progressWindow(edit=True, progress=amount, status=('Reset weight: %s/%s' % (amount, vertexCount)))
            mitvertex.next()
        mc.progressWindow(endProgress=1)

    ######
    def toMObject(self, name):
        msel = om.MSelectionList()
        msel.add(name)
        return msel.getDependNode(0)

    def toMDagPath(self, name):
        msel = om.MSelectionList()
        msel.add(name)
        return msel.getDagPath(0)

    def checkSkinLimit(self, skin, mesh, limit=4, style=0):
        mobj = self.toMObject(skin)
        mdp = self.toMDagPath(mesh)

        mfnm = om.MFnMesh(mdp)
        mitmv = om.MItMeshVertex(mdp)

        mfnsc = oma.MFnSkinCluster(mobj)

        result = []
        while not mitmv.isDone():
            mda, total = mfnsc.getWeights(mdp, mitmv.currentItem())
            # print total
            # mda= [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
            count = len( list(filter(bool, mda)) )
            if style == 0:
                # greater Than
                if count > limit:
                    result.append("%s.vtx[%s]" % (mesh, mitmv.index()))
            elif style == 1:
                # equal
                if count == limit:
                    result.append("%s.vtx[%s]" % (mesh, mitmv.index()))
            else:
                # less Than
                if count < limit:
                    result.append("%s.vtx[%s]" % (mesh, mitmv.index()))
            mitmv.next()
        return result

    def checkSkinLimitStyle(self, limitNum, style):
        sels = mc.filterExpand(sm=12)
        if sels is None:
            mc.error('Please select some mesh.')
            return None
        if not sels:
            mc.error('Please select some mesh.')
            return None
        toSelect = []
        for one in sels:
            skinNode = self.searchSkinClusterByName(one)
            if not skinNode:
                mc.warning('cant find no skincluster for %s' % one)
            res = self.checkSkinLimit(skinNode, one, limitNum, style)
            if res:
                toSelect = toSelect + res
        if toSelect:
            mc.select(toSelect, r=True)
        else:
            mc.select(cl=True)

