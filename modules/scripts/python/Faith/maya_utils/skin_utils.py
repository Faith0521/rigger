import numpy as np
from maya import cmds, mel, OpenMaya, OpenMayaAnim
from maya.api import OpenMaya as OpenMayaAPI
from maya.api import OpenMayaAnim as OpenMayaAnimAPI
import numpy
import time
import os


class SkinClusterIO(object):

    def __init__(self):
        # self.cDataIO =

        # vars
        self.name = ""
        self.type = "skinCluster"
        self.weightsNonZero_Array = []
        self.weights_Array = []
        self.infMap_Array = []
        self.vertSplit_Array = []
        self.inf_Array = []
        self.skinningMethod = 1
        self.normalizeWeights = 1
        self.geometry = None
        self.blendWeights = []
        self.vtxCount = 0
        self.envelope = 1
        self.skinningMethod = 1
        self.useComponents = 0
        self.normalizeWeights = 1
        self.deformUserNormals = 1

    def get_data(self, skinCluster):
        # ...get the MFnSkinCluster for skinCluster
        selList = OpenMaya.MSelectionList()
        selList.add(skinCluster)
        clusterNode = OpenMaya.MObject()
        selList.getDependNode(0, clusterNode)
        skinFn = OpenMayaAnim.MFnSkinCluster(clusterNode)

        # ...get components
        fnSet = OpenMaya.MFnSet(skinFn.deformerSet())
        members = OpenMaya.MSelectionList()
        fnSet.getMembers(members, False)
        dagPath = OpenMaya.MDagPath()
        components = OpenMaya.MObject()
        members.getDagPath(0, dagPath, components)

        # ...get mesh
        geometry = cmds.skinCluster(skinCluster, query=True, geometry=True)[0]

        # ...get vtxID_Array
        vtxID_Array = list(range(0, len(cmds.ls('%s.vtx[*]' % geometry, fl=1))))

        # ...get skin
        selList = OpenMayaAPI.MSelectionList()
        selList.add(mel.eval('findRelatedSkinCluster %s' % geometry))
        skinPath = selList.getDependNode(0)

        # ...get mesh
        selList = OpenMayaAPI.MSelectionList()
        selList.add(geometry)
        meshPath = selList.getDagPath(0)

        # ...get vtxs
        fnSkinCluster = OpenMayaAnimAPI.MFnSkinCluster(skinPath)
        fnVtxComp = OpenMayaAPI.MFnSingleIndexedComponent()
        vtxComponents = fnVtxComp.create(OpenMayaAPI.MFn.kMeshVertComponent)
        fnVtxComp.addElements(vtxID_Array)

        # ...get weights/infs
        dWeights, infCount = fnSkinCluster.getWeights(meshPath, vtxComponents)
        weights_Array = numpy.array(list(dWeights), type="float64")
        inf_Array = [dp.partialPathName() for dp in fnSkinCluster.influenceObjects()]

        # ...convert to weightsNonZero_Array
        weightsNonZero_Array, infMap_Array, vertSplit_Array = self.compress_weightData()

        # ...gatherBlendWeights
        blendWeights_mArray = OpenMaya.MDoubleArray()
        skinFn.getBlendWeights(dagPath, components, blendWeights_mArray)

        # ...set data to self vars
        self.name = skinCluster
        self.weightsNonZero_Array = np.array(weightsNonZero_Array)
        self.infMap_Array = np.array(infMap_Array)
        self.vertSplit_Array = np.array(vertSplit_Array)
        self.inf_Array = np.array(inf_Array)
        self.geometry = geometry
        self.blendWeights = np.array(blendWeights_mArray)
        self.vtxCount = len(vertSplit_Array) - 1

        # ...get attrs
        self.envelope = cmds.getAttr(skinCluster + ".envelope")
        self.skinningMethod = cmds.getAttr(skinCluster + ".skinningMethod")
        self.useComponents = cmds.getAttr(skinCluster + ".useComponents")
        self.normalizeWeights = cmds.getAttr(skinCluster + ".normalizeWeights")
        self.deformUserNormals = cmds.getAttr(skinCluster + ".deformUserNormals")

        return True

    def set_data(self, skinCluster):

        # ...get the MFnSkinCluster for skinCluster
        selList = OpenMaya.MSelectionList()
        selList.add(skinCluster)
        skinClusterMObject = OpenMaya.MObject()
        selList.getDependNode(0, skinClusterMObject)
        skinFn = OpenMayaAnim.MFnSkinCluster(skinClusterMObject)

        # ...get dagPath and member components of skinned shape
        fnSet = OpenMaya.MFnSet(skinFn.deformerSet())
        members = OpenMaya.MSelectionList()
        fnSet.getMembers(members, False)
        dagPath = OpenMaya.MDagPath()
        components = OpenMaya.MObject()
        members.getDagPath(0, dagPath, components)

        #########################################################

        # ...set infs
        influencePaths = OpenMaya.MDagPathArray()
        infCount = skinFn.influenceObjects(influencePaths)
        influences_Array = [influencePaths[i].partialPathName() for i in range(influencePaths.length())]

        # ...change the order in set(i,i)
        influenceIndices = OpenMaya.MIntArray(infCount)
        [influenceIndices.set(i, i) for i in range(infCount)]

        # ...set data
        skinFn.setWeights(dagPath, components, influenceIndices, weights_mArray, False)

        return True

    def save(self, node=None, dirPath=None):
        # ...get selection
        if node is None:
            node = cmds.ls(sl=1)
            if node is None:
                print("ERROR: Select Something!")
                return False
            else:
                node = node[0]

        # ...get skinCluster
        skinCluster = mel.eval("findRelatedSkinCluster " + node)
        if not cmds.objExists(skinCluster):
            print("ERROR: Node has no skinCluster!")
            return False

        # ...get dirPath
        if dirPath is None:
            startDir = cmds.workspace(q=True, rootDirectory=True)
            dirPath = cmds.fileDialog2(caption="Save SkinWeights", dialogStyle=2, fileMode=3, startingDiretory=startDir,
                                       fileFilter="*.npy", okCaption="Select")

        # ...get filePath
        skinCluster = "skinCluster_%s" % node
        filePath = "%s/%s.npy" % (dirPath, skinCluster)

        # ...timeStart
        timeStart = time.time()

        # ...get data
        self.get_data(skinCluster)

        # ...timeEnd
        timeEnd = time.time()
        timeElapsed = timeEnd - timeStart

        # ...print time
        print(f"GetData Elapsed: {timeElapsed}")

        # ...construct data_array
        legend = ()

        data = []

        # ...time start
        timeStart = time.time()

        # ...write data
        numpy.save(filePath, data)

        # ...timeEnd
        timeEnd = time.time()
        timeElapsed = timeEnd - timeStart

        # ...print time
        print(f"SaveData Elapsed: {timeElapsed}")

    def load(self, node=None, dirPath=None):
        # ...get selection
        if node is None:
            node = cmds.ls(sl=1)
            if node is None:
                print("ERROR: Select Something!")
                return False
            else:
                node = node[0]

        # ...get dirPath
        if dirPath is None:
            startDir = cmds.workspace(q=True, rootDirectory=True)
            dirPath = cmds.fileDialog2(caption="Load SkinWeights", dialogStyle=2, fileMode=1, startingDiretory=startDir,
                                       fileFilter="*.npy", okCaption="Select")

        # ...get filePath
        skinCluster = "skinCluster_%s" % node
        filePath = "%s/%s.npy" % (dirPath, skinCluster)

        # ...check if skinCluster exists
        if not os.path.exists(filePath):
            print(f"ERROR: SkinCluster for node '{node}' not found on disk!")
            return False

        # ...unbind current skinCluster
        skinCluster = mel.eval("findRelatedSkinCluster " + node)
        if cmds.objExists(skinCluster):
            mel.eval("skinCluster -e -ub " + skinCluster)

        # ...timeStart
        timeStart = time.time()

        # ...read data
        data = numpy.load(filePath)

        # ...timeEnd
        timeEnd = time.time()
        timeElapsed = timeEnd - timeStart

        # ...print time
        print(f"ReadData Elapsed: {timeElapsed}")

        # ...get item data from numpy array

        # ...bind skin
        inf_Array = [inf[0] for inf in data[data.keys()[0]]]

        # ...create the joint if it doesnt exist
        for inf in self.inf_Array:
            if not cmds.objExists(inf):
                cmds.select(cl=True)
                cmds.joint(n=inf)
        skinCluster = "skinCluster_%s" % node
        skinCluster = cmds.skinCluster(self.inf_Array, node, n=skinCluster, tsb=True)

        # ...timeStart
        timeStart = time.time()

        # ...set data
        [cmds.skinPercent(skinCluster, vtx, tv=data[vtx], zri=1) for vtx in data.keys()]
        # self.set_data(skinCluster)

        # ...time end
        timeEnd = time.time()
        timeElapsed = timeEnd - timeStart

        # ...print time
        print(f"SetData Elapsed: {timeElapsed}")

    def compress_weightData(self):
        return
