from importlib import reload
import maya.cmds as mc
import maya.mel as mel
import maya.api.OpenMaya as om
from PySide2 import QtCore, QtGui, QtWidgets

from ...maya_utils import aboutUI
from . import batchCopy_ui
reload(batchCopy_ui)
reload(aboutUI)

def uiShow():
    batchCopySys_dock().show(dockable=True)

class batchCopySys_dock(aboutUI.UI_Dockable):
    title_name = 'batchCopy_v01'  # Window display name
    control_name = 'batchCopy_system'  # Window unique object name

    def __init__(self):
        super(self.__class__, self).__init__()

    def build_ui(self):
        self.main_layout.addWidget(batchCopySys())

class batchCopySys(QtWidgets.QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = batchCopy_ui.Ui_batchCopyUI()
        self.ui.setupUi(self)

        # refresh
        self.ui.new_mode_btn.setEnabled(0)
        self.ui.cm_cb.currentIndexChanged.connect(self.copyType_UICmd)

        # signal
        self.ui.old_mode_btn.clicked.connect(self.loadOrgMesh)
        self.ui.new_mode_btn.clicked.connect(self.loadNewMesh)
        self.ui.copySkin_btn.clicked.connect(self.copySkin_UICmd)
        self.ui.copyBs_btn.clicked.connect(self.copyBs_UICmd)
        self.ui.old_mode_view.itemDoubleClicked.connect(lambda *args:self.viewItem_UICmd(self.ui.old_mode_view))
        self.ui.new_mode_view.itemDoubleClicked.connect(lambda *args:self.viewItem_UICmd(self.ui.new_mode_view))

        # data
        self.orgMeshDict = {}
        self.newMeshDict = {}
        self.newItemColor = {}

    def viewItem_UICmd(self, item):
        obj = item.currentItem().text().split(' : ')[1]
        if mc.objExists(obj):
            mc.select(obj)

    def copyType_UICmd(self):
        self.ui.old_mode_view.clear()
        self.ui.new_mode_view.clear()
        self.ui.new_mode_btn.setEnabled(1)
        self.ui.copyBs_btn.setEnabled(1)

        if self.ui.cm_cb.currentIndex() == 0:
            self.ui.new_mode_btn.setEnabled(0)
        elif self.ui.cm_cb.currentIndex() == 2:
            self.ui.copyBs_btn.setEnabled(0)


    def apiMesh(self, mesh):
        sel = mc.ls(mesh)
        selList = om.MSelectionList()
        selList.add(sel[0])
        dagPath = selList.getDagPath(0)
        mfn_mesh = om.MFnMesh(dagPath)
        return mfn_mesh

    def get_mesh_topology(self, mesh):
        meshDag = mc.ls(mesh, dag=1, r=1, l=1, ni=1, type="mesh")[0]
        msel = om.MSelectionList()
        msel.add(meshDag)
        mobj = msel.getDependNode(0)
        fn_mesh = om.MFnMesh(mobj)

        vtx_count = fn_mesh.numVertices
        face_count = fn_mesh.numPolygons
        if not face_count: return "0"

        elements = [vtx_count, face_count]
        face_ids = map(int, ((face_count - 1) * x / 3.0 for x in range(4)))
        for face_id in face_ids:
            vtx_array = fn_mesh.getPolygonVertices(face_id)
            elements.extend(list(vtx_array))

        return "-".join(map(str, elements))

    def check_mesh_topology(self, src, dst):
        src_ident = self.get_mesh_topology(src)
        dst_ident = self.get_mesh_topology(dst)
        if src_ident != dst_ident:
            return False
        else:
            return True

    def meshCompare(self):
        self.newMeshDict = {}
        for key in self.orgMeshDict.keys():
            oldMesh = self.orgMeshDict[key].split(' : ')[1]
            similarMeshs = mc.ls(oldMesh.split('|')[-1])
            if oldMesh in similarMeshs:
                similarMeshs.remove(oldMesh)
                if len(similarMeshs) == 1:
                    self.newMeshDict[key] = similarMeshs[0]

                    if self.check_mesh_topology(oldMesh, similarMeshs[0]):
                        self.newItemColor[key] = 'green'
                    else:
                        self.newItemColor[key] = 'yellow'
                else:
                    self.newMeshDict[key] = 'MISS'
                    self.newItemColor[key] = 'red'

        self.ui.new_mode_view.clear()
        for key in self.newMeshDict.keys():
            self.ui.new_mode_view.addItem( str(key) + ' : ' + self.newMeshDict[key])
            self.ui.new_mode_view.item(key).setForeground(QtGui.QColor(self.newItemColor[key]))

    def loadOrgMesh(self):
        self.orgMeshDict = {}
        meshs = mc.ls(sl=1, ap=1)
        self.ui.old_mode_view.clear()
        for index, mesh in enumerate(meshs):
            shape = mc.listRelatives(mesh, c=True, f=True)[0]
            self.orgMeshDict[index] = str(index) + ' : ' + str(mesh)
            if mc.nodeType(shape, api=True) == 'kMesh':
                self.ui.old_mode_view.addItem( str(index) + ' : ' + str(mesh) )

        if self.ui.cm_cb.currentIndex() == 0:
            self.meshCompare()

        elif self.ui.cm_cb.currentIndex() == 1:
            self.ui.old_mode_view.clear()
            self.ui.old_mode_view.addItem('0 : ' + str(meshs[0]))
            self.orgMeshDict = {0: '0 : ' + str(meshs[0])}

    def loadNewMesh(self):
        self.newMeshDict = {}
        meshs = mc.ls(sl=1, ap=1)
        self.ui.new_mode_view.clear()
        for index, mesh in enumerate(meshs):
            shape = mc.listRelatives(mesh, c=True, f=True)[0]
            self.newMeshDict[index] = str(index) + ' : ' + str(mesh)
            if mc.nodeType(shape, api=True) == 'kMesh':
                self.ui.new_mode_view.addItem(str(index) + ' : ' + str(mesh))

        if self.ui.cm_cb.currentIndex() == 2:
            self.ui.new_mode_view.clear()
            self.ui.new_mode_view.addItem(meshs[0])
            self.newMeshDict = {0: '0 : ' + str(meshs[0])}

    def getMeshsSkinJnts(self, meshs):
        skinJntAlls = []
        for mesh in meshs:
            if mc.listRelatives(mesh, s=True) is not None:
                skinNode = mel.eval('findRelatedSkinCluster' + '("' + meshs + '")')
                if not skinNode:
                    pass
                else:
                    skin_jnts = mc.skinCluster(skinNode, q=True, inf=skinNode)
                    for jnt in skin_jnts:
                        skinJntAlls.append(jnt)

        skinJntAlls = list(set(skinJntAlls))
        return skinJntAlls

    def copySkin(self, oldMesh, newMesh, inf1A, inf2A):
        oldSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + oldMesh + "\")")
        if not oldSkinNode:
            mc.warning('Can not find blendshape node on {0}'.format(oldMesh))
            return

        # do copy
        oldSkinJnts = mc.skinCluster(oldSkinNode, q=True, inf=oldSkinNode)
        newSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + newMesh + "\")")
        # do copy
        if newSkinNode:
            newSkinJnts = mc.skinCluster(newSkinNode, q=True, inf=newSkinNode)
            if newSkinJnts != oldSkinJnts:
                mc.delete(newSkinNode)
                mc.skinCluster(oldSkinJnts, newMesh, mi=10, rui=False, tsb=True, name=newSkinNode)
            else:
                pass

        else:
            mc.skinCluster(oldSkinJnts, newMesh, mi=10, rui=False, tsb=True)

        mc.copySkinWeights(oldMesh, newMesh, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[inf1A, inf2A])


    def copySkin_UICmd(self):
        inf1A = self.ui.inf1_cb.currentText()
        inf2A = self.ui.inf2_cb.currentText()
        oldMeshs = [self.ui.old_mode_view.item(i).text().split(' : ')[1] for i in range(self.ui.old_mode_view.count())]
        newMeshs = [self.ui.new_mode_view.item(i).text().split(' : ')[1] for i in range(self.ui.new_mode_view.count())]

        if self.ui.cm_cb.currentIndex() == 0:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if mc.objExists(oldMeshs[index]) and mc.objExists(newMeshs[index]):
                    self.copySkin(oldMeshs[index], newMeshs[index], inf1A, inf2A)

        elif self.ui.cm_cb.currentIndex() == 1:
            for index, mesh in enumerate(newMeshs):
                self.copySkin(oldMeshs[0], newMeshs[index], inf1A, inf2A)

        elif self.ui.cm_cb.currentIndex() == 2:
            allSkinJnts = self.getMeshsSkinJnts(oldMeshs)
            newSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + newMeshs[0] + "\")")
            mc.delete(newSkinNode)
            mc.skinCluster(allSkinJnts, newMeshs[0], mi=10, rui=False, tsb=True)
            mc.copySkinWeights(oldMeshs, newMeshs[0], noMirror=True, surfaceAssociation='closestPoint', influenceAssociation=[inf1A, inf2A])

        elif self.ui.cm_cb.currentIndex() == 3:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if mc.objExists(oldMeshs[index]) and mc.objExists(newMeshs[index]):
                    self.copySkin(oldMeshs[index], newMeshs[index], inf1A, inf2A)

    def getBlendShapeNode(self, mesh):
        try:
            meshHistory = mc.listHistory(mesh, pdo=True)
            bsNode = mc.ls(meshHistory, type='blendShape')[0]
            return bsNode
        except:
            return None

    def getBlendShapeTarget(self, bsNode):
        weightAttrPath = bsNode + '.weight'
        weightList = mc.listAttr(weightAttrPath, multi=True)
        return weightList

    def copyBs(self, oldMesh, newMesh, skipLock=True, replaceConnect=True, rename=True):
        # get org blendShape node
        if not mc.objExists(oldMesh) or not mc.objExists(newMesh):
            return
        bsNode = self.getBlendShapeNode(mesh=oldMesh)

        if not bsNode:
            return

        copyTargets = []
        targets=self.getBlendShapeTarget(bsNode)

        if not targets:
            return

        for target in targets:
            if skipLock:
                if not mc.getAttr(bsNode+'.'+target, lock=True):
                    copyTargets.append(target)
            else:
                copyTargets.append(target)

        if rename:
            oldTargetNameStr = oldMesh+'_'
            newTargetNameStr = newMesh+'_'
        else:
            oldTargetNameStr = ''
            newTargetNameStr = ''

        targetsGrp = mc.createNode('transform', name=oldTargetNameStr+'targets_grp')

        mc.select(newMesh)
        mc.select(oldMesh, add=True)
        warpNode = mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0"}')[0]
        mc.select(cl=True)

        for target in copyTargets:
            mc.setAttr(bsNode+'.'+target, 1)
            mc.duplicate(newMesh, name=newTargetNameStr + target)
            mc.setAttr(bsNode + '.' + target, 0)
            mc.parent(target, targetsGrp)

        # clean
        mc.delete(warpNode)
        if mc.objExists(oldMesh+'Base'):
            mc.delete(oldMesh+'Base')

        #create newMesh blendShape
        targetMeshs = mc.listRelatives(targetsGrp)
        mc.select(targetMeshs)
        mc.select(newMesh, add=1)
        newBsNode = mc.blendShape(tc=True, name=newMesh.split('|')[-1]+'_seekOutBsNode')[0]
        if not rename:
            mc.delete(targetsGrp)

        #rebuild connection
        if replaceConnect:
            for mesh in targetMeshs:
                attrSource=mc.connectionInfo(bsNode+'.'+mesh, sfd=1)
                if attrSource!='':
                    mc.connectAttr(attrSource, newBsNode+'.'+mesh)

    def copyBs_UICmd(self):
        oldMeshs = [self.ui.old_mode_view.item(i).text().split(' : ')[1] for i in range(self.ui.old_mode_view.count())]
        newMeshs = [self.ui.new_mode_view.item(i).text().split(' : ')[1] for i in range(self.ui.new_mode_view.count())]

        if self.ui.cm_cb.currentIndex() == 0:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if mc.objExists(oldMeshs[index]) and mc.objExists(newMeshs[index]):
                    self.copyBs(oldMeshs[index], newMeshs[index], skipLock=True, replaceConnect=True, rename=False)

        elif self.ui.cm_cb.currentIndex() == 1:
            for index, mesh in enumerate(newMeshs):
                self.copyBs(oldMeshs[0], newMeshs[index], skipLock=True, replaceConnect=True, rename=False)

        elif self.ui.cm_cb.currentIndex() == 2:
            mc.warning(' "* to One" can not support bs copy !')
            return

        elif self.ui.cm_cb.currentIndex() == 3:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if mc.objExists(oldMeshs[index]) and mc.objExists(newMeshs[index]):
                    self.copyBs(oldMeshs[index], newMeshs[index], skipLock=True, replaceConnect=True, rename=False)


