import maya.api.OpenMaya as om
import maya.mel as mel
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import struct
import os
from collections import defaultdict

# Plugin information
kPluginCmdName = "skinWeightBatch"
kPluginVendor = "YourCompany"
kPluginVersion = "1.0.0"

# File format constants
FILE_MAGIC = b'SWB\x00'
FILE_VERSION = 1

def maya_useNewAPI():
    pass

class SkinWeightBatchPlugin(om.MPxCommand):
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return SkinWeightBatchPlugin()

    def doIt(self, args):
        try:
            # Parse arguments
            self.parseArguments(args)

            if self.mode == 'export':
                self.exportWeights()
            elif self.mode == 'import':
                self.importWeights()
            else:
                raise RuntimeError("Invalid mode specified")

        except Exception as e:
            om.MGlobal.displayError(f"SkinWeightBatch error: {str(e)}")

    def parseArguments(self, args):
        """Parse command arguments"""
        argData = om.MArgParser(self.syntax(), args)

        # Get mode (export/import)
        if argData.isFlagSet('-e'):
            self.mode = 'export'
        elif argData.isFlagSet('-i'):
            self.mode = 'import'
        else:
            raise RuntimeError("Must specify either -export or -import")

        # Get file path
        if argData.isFlagSet('-f'):
            self.filePath = argData.flagArgumentString('-f', 0)
        else:
            raise RuntimeError("File path (-f) must be specified")

    def exportWeights(self):
        """Export skin weights to binary file"""
        skinData = self.collectSkinData()
        with open(self.filePath, 'wb') as f:
            # Write file header
            f.write(FILE_MAGIC)
            f.write(struct.pack('<H', FILE_VERSION))
            f.write(struct.pack('<I', len(skinData)))  # Number of skin clusters

            # Write each skin cluster
            for data in skinData:
                self.writeSkinCluster(f, data)

        om.MGlobal.displayInfo(f"Exported {len(skinData)} skin clusters to {self.filePath}")

    def importWeights(self):
        """Import skin weights from binary file"""
        if not os.path.exists(self.filePath):
            raise RuntimeError(f"File not found: {self.filePath}")

        with open(self.filePath, 'rb') as f:
            # Verify file header
            magic = f.read(4)
            if magic != FILE_MAGIC:
                raise RuntimeError("Invalid skin weight file format")

            # Read version and skin count
            version, skinCount = struct.unpack('<HI', f.read(6))

            # Read each skin cluster
            successCount = 0
            for _ in range(skinCount):
                try:
                    skinData = self.readSkinCluster(f)
                    self.applySkinData(skinData)
                    successCount += 1
                except Exception as e:
                    om.MGlobal.displayWarning(f"Failed to import skin cluster: {str(e)}")

            om.MGlobal.displayInfo(f"Imported {successCount}/{skinCount} skin clusters from {self.filePath}")

    # ========== Data Collection Methods ==========

    def collectSkinData(self):
        """Collect skin weight data from all skin clusters in scene"""
        skinData = []
        selection = om.MGlobal.getActiveSelectionList()
        selectionItList = om.MItSelectionList(selection)
        while not selectionItList.isDone():
            path_dag = selectionItList.getDagPath()
            path_dag.extendToShape()
            mesh_name = om.MFnDependencyNode(path_dag.node()).name()

            dg_skin_it = om.MItDependencyGraph(path_dag.node(), om.MFn.kSkinClusterFilter, om.MItDependencyGraph.kUpstream)
            if not (dg_skin_it.currentNode().hasFn(om.MFn.kSkinClusterFilter)):
                continue
            skinFn = oma.MFnSkinCluster(dg_skin_it.currentNode())

            # Get influences
            influences = []
            infPaths = skinFn.influenceObjects()
            for i in range(len(infPaths)):
                influences.append(infPaths[i].partialPathName())
            # Get weights
            weights = self.getSkinWeights(skinFn, path_dag)

            skinData.append({
                'skinCluster': om.MFnDependencyNode(dg_skin_it.currentNode()).name(),
                'mesh': path_dag.partialPathName(),
                'influences': influences,
                'weights': weights
            })
            selectionItList.next()

        return skinData

    def getSkinnedMesh(self, skinFn):
        """Get the mesh influenced by a skin cluster"""
        try:
            # Get the first output geometry
            outputGeom = om.MObject()
            outputGeom = skinFn.outputShapeAtIndex(0)

            if outputGeom.hasFn(om.MFn.kMesh):
                return om.MDagPath.getAPathTo(outputGeom)
        except Exception as e:
            om.MGlobal.displayWarning(f"Error getting skinned mesh: {str(e)}")
        return None

    def getSkinWeights(self, skinFn, meshDag):
        """Get skin weights for all vertices"""
        weights = defaultdict(list)
        meshFn = om.MFnMesh(meshDag)
        vertIter = om.MItMeshVertex(meshDag)

        # Get influence indices
        infIndices = om.MIntArray()
        for i in range(len(skinFn.influenceObjects())):
            infIndices.append(i)

        while not vertIter.isDone():
            vertIdx = vertIter.index()
            vertComp = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
            compFn = om.MFnSingleIndexedComponent(vertComp)
            compFn.addElement(vertIdx)

            # weightArray = om.MDoubleArray()
            weightArray = skinFn.getWeights(meshDag, vertComp, infIndices)

            weights[vertIdx] = list(weightArray)
            vertIter.next()

        return dict(weights)

    # ========== Binary I/O Methods ==========

    def writeSkinCluster(self, f, data):
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
        for vertIdx, weights in data['weights'].items():
            f.write(struct.pack('<II', vertIdx, len(weights)))
            f.write(struct.pack('<%dd' % len(weights), *weights))

    def readSkinCluster(self, f):
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

    # ========== Application Methods ==========

    def applySkinData(self, skinData):
        """Apply skin weight data to scene"""
        # Find skinned mesh
        try:
            selList = om.MSelectionList()
            selList.add(skinData['mesh'])
            meshDag = selList.getDagPath(0)
        except:
            raise RuntimeError(f"Mesh not found: {skinData['mesh']}")

        # Find or create skin cluster
        skinFn = self.findOrCreateSkinCluster(
            skinData['skinCluster'],
            meshDag,
            skinData['influences']
        )
        if not skinFn:
            raise RuntimeError(f"Failed to create skin cluster: {skinData['skinCluster']}")

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

    def findOrCreateSkinCluster(self, skinName, meshDag, influenceNames):
        """Find or create a skin cluster"""

        meshObj = meshDag.node()
        mesh_name = om.MFnDependencyNode(meshObj).name()

        skinFn = self.findSkinFilter(dag=meshDag)

        if skinFn:
            return skinFn
        else:
            current_skin = cmds.skinCluster(influenceNames, mesh_name, tsb=1, nw=1, mi=1, dr=3.0, rui=0)[0]
            cmds.rename(current_skin, skinName)
            skinFn = self.findSkinFilter(dag=meshDag)
            return skinFn

    def findSkinFilter(self, dag):
        """Find skin filter"""
        it_dg = om.MItDependencyGraph(
            dag.node(),
            om.MItDependencyGraph.kUpstream,
            True
        )
        skinFn = None

        while not it_dg.isDone():
            current_node = it_dg.currentNode()
            node_fn = om.MFnDependencyNode(current_node)
            node_name = node_fn.name()
            node_type = current_node.apiTypeStr
            if node_type == 'kSkinClusterFilter':
                skinFn = oma.MFnSkinCluster(it_dg.currentNode())
            it_dg.next()
        return skinFn

    def findExistingSkinCluster(self, meshObj, skinName):
        """Find an existing skin cluster"""
        meshFn = om.MFnDependencyNode(meshObj)
        inMeshPlug = meshFn.findPlug("inMesh", True)

        if inMeshPlug.isNull:
            return None

        # Get nodes connected to inMesh
        connections = inMeshPlug.connectedTo(True, False)

        for i in range(len(connections)):
            node = connections[i].node()
            if node.hasFn(om.MFn.kSkinClusterFilter):
                if om.MFnDependencyNode(node).name() == skinName:
                    return oma.MFnSkinCluster(node)

        return None

    @classmethod
    def syntaxCreator(cls):
        """Create command syntax"""
        syntax = om.MSyntax()

        # Mode flags
        syntax.addFlag('-e', '-export', om.MSyntax.kNoArg)
        syntax.addFlag('-i', '-import', om.MSyntax.kNoArg)

        # File path flag
        syntax.addFlag('-f', '-file', om.MSyntax.kString)

        return syntax


# ========== Plugin Initialization ==========

def initializePlugin(plugin):
    """Initialize the plugin"""
    pluginFn = om.MFnPlugin(plugin, kPluginVendor, kPluginVersion)

    try:
        pluginFn.registerCommand(
            kPluginCmdName,
            SkinWeightBatchPlugin.cmdCreator,
            SkinWeightBatchPlugin.syntaxCreator
        )
    except Exception as e:
        om.MGlobal.displayError(f"Failed to register command {kPluginCmdName}: {str(e)}")


def uninitializePlugin(plugin):
    """Uninitialize the plugin"""
    pluginFn = om.MFnPlugin(plugin)

    try:
        pluginFn.deregisterCommand(kPluginCmdName)
    except:
        om.MGlobal.displayError(f"Failed to deregister command: {kPluginCmdName}")

