#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/12/4 18:13
# @Author : yinyufei
# @File : skin.py
# @Project : TeamCode
from collections import defaultdict
from cgrig.libs.utils.filesystem import ProgressBarContext
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import ngSkinTools2.api as ng2
import struct
import os


def copySkin(oldMesh, newMesh, inf1A, inf2A):
    oldSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + oldMesh + "\")")
    if not oldSkinNode:
        cmds.warning('Can not find skin node on {0}'.format(oldMesh))
        return

    # do copy
    oldSkinJnts = cmds.skinCluster(oldSkinNode, q=True, inf=oldSkinNode)
    newSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + newMesh + "\")")
    # do copy
    if newSkinNode:
        newSkinJnts = cmds.skinCluster(newSkinNode, q=True, inf=newSkinNode)
        if newSkinJnts != oldSkinJnts:
            cmds.delete(newSkinNode)
            cmds.skinCluster(oldSkinJnts, newMesh, mi=10, rui=False, tsb=True, name=newSkinNode)
        else:
            pass

    else:
        cmds.skinCluster(oldSkinJnts, newMesh, mi=10, rui=False, tsb=True)

    cmds.copySkinWeights(oldMesh, newMesh, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[inf1A, inf2A])
    SkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + newMesh + "\")")
    return SkinNode


def getSkinWeights(skinFn, meshDag):
    """Get skin weights for all vertices"""
    weights = defaultdict(list)
    meshFn = om.MFnMesh(meshDag)
    vertIter = om.MItMeshVertex(meshDag)

    # Get influence indices
    infIndices = om.MIntArray()
    for i in range(len(skinFn.influenceObjects())):
        infIndices.append(i)

    progressBar = ProgressBarContext(maxValue=meshFn.numVertices, step=1, ismain=False, title='Get Skin Data')
    with progressBar:
        while not vertIter.isDone():
            if progressBar.isCanceled():
                break
            vertIdx = vertIter.index()
            progressBar.setText("Get skin weights for {}.vtx[{}]".format(meshFn.name(), vertIdx))
            vertComp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
            compFn = om.MFnSingleIndexedComponent(vertComp)
            compFn.addElement(vertIdx)
            weightArray = skinFn.getWeights(meshDag, vertComp, infIndices)

            weights[vertIdx] = list(weightArray)
            progressBar.updateProgress()
            vertIter.next()

    return dict(weights)


def del_ngSkinNode():
    """
    删除所有ng节点
    """
    nodes_to_delete = []
    if cmds.pluginInfo('ngSkinTools2', query=True, loaded=True):
        nodes_to_delete = cmds.ls(type='ngst2SkinLayerData')
    if cmds.pluginInfo('ngSkinTools', query=True, loaded=True):
        nodes_to_delete += cmds.ls(type='ngSkinLayerData')

    if nodes_to_delete:
        cmds.delete(nodes_to_delete)

    mel.eval(u'print "// Result: ngSkinTools nodes have been cleared from the scene."')
    cmds.select(cl=True)
    cmds.setToolTo('selectSuperContext')


def getNgLayersWeights(skin, mesh):
    """
    获取ng模型Base Weights层的权重信息
    """
    verts = cmds.ls(cmds.polyListComponentConversion(mesh, toVertex=True), fl=True)
    mesh = verts[0].split('.')[0]
    num_verts = cmds.polyEvaluate(mesh, v=True)

    skin_cluster_sl = om.MGlobal.getSelectionListByName(skin)
    skin_cluster_obj = skin_cluster_sl.getDependNode(0)
    skin_cluster_fn = oma.MFnSkinCluster(skin_cluster_obj)

    influence_dpa = skin_cluster_fn.influenceObjects()
    jnt_indices = [i for i in range(len(influence_dpa))]

    layers = ng2.layers.init_layers(mesh)
    layers_list = layers.list()

    layer_obj = next((l for l in layers_list if l.name == "Base Weights"), None)

    if not layer_obj:
        layers.add("Base Weights")
        layer_obj = next((l for l in layers_list if l.name == "Base Weights"), None)

    layer_wts = [layer_obj.get_weights(jnt_index) or [0] * num_verts for jnt_index in jnt_indices]

    return layer_wts


def findSkinFilter(dag:om.MDagPath):
    """Find skin filter"""
    skinFn = None
    dag_name = om.MFnDependencyNode(dag.node()).name()
    skin_name = mel.eval("findRelatedSkinCluster" + "(\"" + dag_name + "\")")
    if skin_name != "":
        selection = om.MSelectionList()
        selection.add(skin_name)
        skin_obj = selection.getDependNode(0)
        skinFn = oma.MFnSkinCluster(skin_obj)

    return skinFn


def collectSkinData():
    """Collect skin weight data from all skin clusters in scene"""
    skinData = []
    selection = om.MGlobal.getActiveSelectionList()
    selectionItList = om.MItSelectionList(selection)
    while not selectionItList.isDone():
        path_dag = selectionItList.getDagPath()
        path_dag.extendToShape()
        skinFn = findSkinFilter(path_dag)
        if not skinFn:
            selectionItList.next()
            continue
        # Get influences
        influences = []
        infPaths = skinFn.influenceObjects()
        for i in range(len(infPaths)):
            influences.append(infPaths[i].partialPathName())
        # Get weights
        weights = getSkinWeights(skinFn, path_dag)

        skinData.append({
            'skinCluster': skinFn.name(),
            'mesh': path_dag.partialPathName(),
            'influences': influences,
            'weights': weights
        })
        selectionItList.next()

    return skinData


def writeSkinCluster(f, data):
    """Write a single skin cluster to binary file"""
    # Prepare header
    skinName = data['skinCluster'].encode('utf-8')
    meshName = data['mesh'].encode('utf-8')
    influenceNames = [name.encode('utf-8') for name in data['influences']]

    # Write cluster header
    f.write(struct.pack('<IIII',
                        len(skinName), len(meshName),
                        len(influenceNames), len(data['weights'])))

    # Write names
    f.write(skinName)
    f.write(meshName)

    # Write influence names
    for name in influenceNames:
        f.write(struct.pack('<I', len(name)))
        f.write(name)

    # Write weight data
    progressBar = ProgressBarContext(maxValue=len(list(data['weights'].values())), step=1, ismain=False, title='Write Skin Data')
    for vertIdx, weights in data['weights'].items():
        f.write(struct.pack('<II', vertIdx, len(weights)))
        f.write(struct.pack('<%dd' % len(weights), *weights))


def exportWeights(filePath, FILE_MAGIC = b'SKIN\x00'):
    """Export skin weights to binary file"""
    skinData = collectSkinData()
    with open(filePath, 'wb') as f:
        # Write file header
        f.write(FILE_MAGIC)
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', len(skinData)))  # Number of skin clusters

        # Write each skin cluster
        for data in skinData:
            writeSkinCluster(f, data)

    om.MGlobal.displayInfo("Exported {} skin clusters to {}".format(len(skinData), filePath))


def readSkinCluster(f):
    """Read a single skin cluster from binary file"""
    # Read header
    header = struct.unpack('<IIII', f.read(16))
    nameLen, meshLen, infCount, vertCount = header

    # Read names
    skinName = f.read(nameLen).decode('utf-8')
    meshName = f.read(meshLen).decode('utf-8')

    # Read influence names
    influences = []
    for _ in range(infCount):
        infLen = struct.unpack('<I', f.read(4))[0]
        influences.append(f.read(infLen).decode('utf-8'))

    # Read weight data
    weights = {}
    for _ in range(vertCount):
        vertIdx, weightCount = struct.unpack('<II', f.read(8))
        weightValues = struct.unpack('<%dd' % weightCount, f.read(8 * weightCount))
        weights[vertIdx] = list(weightValues)

    return {
        'skinCluster': skinName,
        'mesh': meshName,
        'influences': influences,
        'weights': weights
    }


def findOrCreateSkinCluster(skinName, meshDag, influenceNames):
    """Find or create a skin cluster"""

    meshObj = meshDag.node()
    mesh_name = om.MFnDependencyNode(meshObj).name()

    skinFn = findSkinFilter(dag=meshDag)

    if skinFn:
        cmds.delete(skinFn.name())

    current_skin = cmds.skinCluster(influenceNames, mesh_name, tsb=1, nw=1, mi=1, dr=3.0, rui=0)[0]
    cmds.rename(current_skin, skinName)
    skinFn = findSkinFilter(dag=meshDag)
    return skinFn


def applySkinData(skinData):
    """Apply skin weight data to scene"""
    # Find skinned mesh
    try:
        selList = om.MSelectionList()
        selList.add(skinData['mesh'])
        meshDag = selList.getDagPath(0)
    except:
        raise RuntimeError("Mesh not found: {}".format(skinData['mesh']))

    # Find or create skin cluster
    skinFn = findOrCreateSkinCluster(
        skinData['skinCluster'],
        meshDag,
        skinData['influences']
    )
    if not skinFn:
        raise RuntimeError("Failed to create skin cluster: {}".format(skinData['skinCluster']))

    # Prepare vertex component
    singleIndexComp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
    compFn = om.MFnSingleIndexedComponent(singleIndexComp)

    # Prepare weight data
    infIndices = om.MIntArray()
    weights = om.MDoubleArray()

    # Fill influence indices
    for i in range(len(skinData['influences'])):
        infIndices.append(i)

    # Set weights for each vertex
    for vertIdx, vertWeights in skinData['weights'].items():
        compFn.addElement(vertIdx)
        for w in vertWeights:
            weights.append(w)

    # Apply weights
    skinFn.setWeights(
        meshDag,
        singleIndexComp,
        infIndices,
        weights
    )


def importWeights(filePath, FILE_MAGIC=b'SKIN\x00'):
    """Import skin weights from binary file"""
    if not os.path.exists(filePath):
        raise RuntimeError("File not found: {filePath}".format(filePath=filePath))

    with open(filePath, 'rb') as f:
        # Verify file header
        magic = f.read(5)
        if magic != FILE_MAGIC:
            raise RuntimeError("Invalid skin weight file format")

        # Read version and skin count
        version, skinCount = struct.unpack('<HI', f.read(6))

        # Read each skin cluster
        successCount = 0
        for _ in range(skinCount):
            try:
                skinData = readSkinCluster(f)
                applySkinData(skinData)
                successCount += 1
            except Exception as e:
                om.MGlobal.displayWarning(f"Failed to import skin cluster: {str(e)}")

        om.MGlobal.displayInfo("Imported {successCount}/{skinCount} skin clusters from {filePath}".format(successCount=successCount, skinCount=skinCount, filePath=filePath))


def smoothSkinWeights(skin=None, joints=None, iterations=1):
    currentTool = cmds.currentCtx()

    if not joints:
        joints = cmds.skinCluster(skin, q=True, inf=True)

    skinPaintTool = 'artAttrSkinContext'
    if not cmds.artAttrSkinPaintCtx(skinPaintTool, ex=True):
        cmds.artAttrSkinPaintCtx(skinPaintTool, i1='paintSkinWeights.xpm', whichTool='skinWeights')

    cmds.setToolTo(skinPaintTool)
    cmds.artAttrSkinPaintCtx(skinPaintTool, edit=True, sao='smooth')

    for influence in joints:
        for _ in range(iterations):
            mel.eval('artSkinSelectInfluence artAttrSkinPaintCtx "' + influence + '"')
            cmds.artAttrSkinPaintCtx(skinPaintTool, e=True, clear=True)

    cmds.setToolTo(currentTool)

