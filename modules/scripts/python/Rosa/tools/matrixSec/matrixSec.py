from importlib import reload
import sys, traceback, json, re
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
from PySide2 import QtCore, QtWidgets

from ...maya_utils import aboutPath
from ...maya_utils import aboutUI
from .. controller import controller
from .. namer import namer
from . import matrixSec_ui
from . import modifyData_ui

reload(namer)
reload(controller)
reload(matrixSec_ui)
reload(modifyData_ui)

# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\matrixSec_ui.py .\matrixSecUI.ui
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def undoable(function):
    """A decorator that will make commands undoable in maya"""

    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None

        # noinspection PyBroadException
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print (sys.exc_info()[1])

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode

def uiShow():
    mtxc = matrixSecCmd()
    mtxc.show()

class matrixSecCmd(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(matrixSecCmd, self).__init__(parent)

        try:
            mc.deleteUI('matrixSecUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = matrixSec_ui.Ui_matrixSecUI()
        self.ui.setupUi(self)

        # outside
        self.namer = namer.namer()

        # data -----------------------------------------
        self.ctrlSuffix = '_inmSec'
        self.rootJntSuffix = '_inmSec_root_jnt'
        self.sysGrpSuffix = '_inmSec_system_grp'
        self.geoGrpSuffix = '_inmSec_geo_grp'
        self.ctrlGrpSuffix = '_inmSec_ctrls_grp'
        self.jntGrpSuffix = '_inmSec_jnts_grp'
        self.uvPinGrpSuffix = '_inmSec_uvPin_grp'
        self.crvData_path = aboutPath.filePath('curve')
        self.sysData = {'prefix':'', 'rootJnt':'', 'initMesh':'', 'redoUV':'', 'meshs':{}, 'controls':{}}
        self.meshData = {}
        self.ctrlData = {}

        self.modifySysData = {}
        self.modifyCtrlData = {}
        self.mdArg = None
        self.mdField = None

        # ui edit
        self.ui.splitter02.setStretchFactor(0, 4)
        self.ui.splitter02.setStretchFactor(1, 6)
        mc.selectPref(tso=1)

        # singal -----------------------------------------
        self.ui.initMesh_btn.clicked.connect(self.loadMesh_forUI)
        self.ui.orgVtxs_btn.clicked.connect(lambda: self.ui.orgVtxs_line.setText(str(mc.ls(os=1, fl=1))))
        self.ui.sec_sys_btn.clicked.connect(self.createInmSystem)
        self.ui.sec_sys_lv.itemClicked.connect(self.resolveSecSystem_forUI)
        self.ui.mesh_add_btn.clicked.connect(self.addMeshForSys)
        self.ui.mesh_remove_btn.clicked.connect(self.removeMeshForSys)
        self.ui.ctrl_add_btn.clicked.connect(self.addCtrlForSys)
        self.ui.ctrl_remove_btn.clicked.connect(self.removeCtrlForSys)
        self.ui.genarate_btn.clicked.connect(self.importSecSys)
        self.ui.exit_btn.clicked.connect(self.exitModifyUI)

        # refresh
        self.ui.modify_gb.hide()
        self.getInmSystem()

        self.ui.sec_sys_lv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.sec_sys_lv.customContextMenuRequested.connect(self.sysViewMenu)
        self.ui.sec_sys_lv.clicked.connect(lambda: mc.select(self.ui.sec_sys_lv.selectedIndexes()[0].data()))

        self.ui.mesh_lv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.mesh_lv.customContextMenuRequested.connect(self.meshViewMenu)
        self.ui.mesh_lv.clicked.connect(lambda: mc.select(self.ui.mesh_lv.selectedIndexes()[0].data()))

        self.ui.ctrl_lv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.ctrl_lv.customContextMenuRequested.connect(self.controlViewMenu)
        self.ui.ctrl_lv.clicked.connect(lambda: mc.select(self.ui.ctrl_lv.selectedIndexes()[0].data()))

        mc.scriptJob(p=self.objectName(), e=['PreFileNewOrOpened', self.getInmSystem])

    def sysViewMenu(self, position):
        """
        sysViewMenu
        """
        # menu
        menu = QtWidgets.QMenu(self)
        refreshAciton = menu.addAction("refresh UI")
        removeAction = menu.addAction("remove")
        menu.addSeparator()
        exportAction = menu.addAction("export")
        importAction = menu.addAction("import")
        # cmds
        action = menu.exec_( self.ui.sec_sys_lv.mapToGlobal(position) )

        if action == exportAction:
            secSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
            self.exportSecSys(secSys)
        elif action == importAction:
            self.modifyUiFromJson()
        elif action == refreshAciton:
            self.getInmSystem()
        elif action == removeAction:
            secSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
            self.removeInmSystem(secSys)

    def meshViewMenu(self, position):
        """
        meshViewMenu
        """
        # menu
        menu = QtWidgets.QMenu(self)
        renameAction = menu.addAction("tips")
        replaceAction = menu.addAction("replace")
        # cmds
        action = menu.exec_( self.ui.mesh_lv.mapToGlobal(position) )
        # replace
        if action == replaceAction:
            secSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
            needRepMesh = self.ui.mesh_lv.selectedIndexes()[0].data()
            targetMesh = mc.ls(sl=1)[0]
            self.replaceMeshForSys(secSys, needRepMesh, targetMesh)
        elif action == renameAction:
            secSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
            needRenameMesh = self.ui.mesh_lv.selectedIndexes()[0].data()
            self.tipMeshForSys(secSys, needRenameMesh)

    def controlViewMenu(self, position):
        """
        controlViewMenu
        """
        # menu
        menu = QtWidgets.QMenu(self)
        adpAction = menu.addAction("add prefix")
        srAction = menu.addAction("search replace")
        menu.addSeparator()
        axisAction = menu.addAction("select Axis handle")
        mirrorAction = menu.addAction("mirror")
        menu.addSeparator()
        fkAction1 = menu.addAction("To Fk (one to one)")
        fkAction2 = menu.addAction("To Fk (mult to one)")
        fkAction3 = menu.addAction("To World (one to world)")

        secSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        secSysData = eval(mc.getAttr(secSys + '.inmSysData'))
        uiSelCtrls = [item.text(0) for item in self.ui.ctrl_lv.selectedItems()]
        if not uiSelCtrls:
            return

        # cmds
        action = menu.exec_( self.ui.ctrl_lv.mapToGlobal(position) )
        # replace
        if action == adpAction:
            self.renameSecCtrl(secSys, uiSelCtrls, reType='prefix')
        elif action == srAction:
            self.renameSecCtrl(secSys, uiSelCtrls, reType='search')
        elif action == axisAction:
            mc.select( [secSysData['controls'][ctrl]['offsetGrp'] for ctrl in uiSelCtrls] )
        elif action == mirrorAction:
            self.mirrorSecCtrl(secSys, uiSelCtrls)
        elif action == fkAction1:
            self.changeFk(secSys, uiSelCtrls, fkType='one2one')
        elif action == fkAction2:
            self.changeFk(secSys, uiSelCtrls, fkType='mult2one')
        elif action == fkAction3:
            self.changeFk(secSys, uiSelCtrls, fkType='one2world')

    def getInmSystem(self):
        """
        get sec system in sence
        """
        self.ui.initMesh_line.clear()
        self.ui.orgVtxs_line.clear()
        self.ui.prefix_line.clear()
        self.ui.sec_sys_lv.clear()
        self.ui.mesh_lv.clear()
        self.ui.ctrl_lv.clear()
        secSystems = mc.ls('*{0}'.format(self.sysGrpSuffix))
        for secSys in secSystems:
            if mc.objExists(secSys + '.inmSysData'):
                self.ui.sec_sys_lv.addItem(secSys)

    def loadMesh_forUI(self):
        """
        load mesh data from ui
        """
        mesh = mc.ls(sl=1)[0]
        # is poly ?
        if not mc.listRelatives(mesh, ni=1, type='mesh'):
            return
        self.ui.initMesh_line.setText(mesh)
        self.ui.prefix_line.setText(mesh)

    def updateInmSysData(self, inmSys, inmSysData):
        """
        rewrite system data.
        """
        mc.setAttr(inmSys + '.inmSysData', lock=False)
        mc.setAttr(inmSys + '.inmSysData', inmSysData, type='string')
        mc.setAttr(inmSys + '.inmSysData', lock=True)

    def invMatrix_mesh(self, prefix, mesh, redoUV=False):
        """
        create sec mesh
        """
        if not mesh:
            mesh = mc.ls(sl=1)[0]
        # is poly?
        if not mc.listRelatives(mesh, type='shape'):
            return

        # uv pin mesh -----------------------------------------------------

        # org mesh
        orgMesh = mc.rename(mesh, mesh + '_inmOrg')

        # uv mesh
        if redoUV:
            uvMesh = mesh + '_inmUv'
            if not mc.objExists(uvMesh):
                mc.duplicate(orgMesh, n=uvMesh)
            mc.polyAutoProjection(uvMesh + '.f[*]', lm=0, pb=0, ibd=1, cm=0, l=2, sc=1, o=1, p=12, ps=0.2, ws=0)
            mc.select(uvMesh)
            mc.DeleteHistory()
        else:
            uvMesh = orgMesh

        # output mesh
        outMesh = mesh
        if not mc.objExists(outMesh):
            mc.duplicate(orgMesh, n=outMesh)

        # coonect diff layer mode
        if redoUV:
            uvBs = mc.blendShape(orgMesh, uvMesh, name=mesh + '_uv_input_bs')[0]
            mc.setAttr(uvBs + '.' + orgMesh, 1)

        secBs = mc.blendShape(orgMesh, outMesh, name=mesh + '_sec_input_bs')[0]
        mc.setAttr(secBs + '.' + orgMesh, 1)

        # do not touch group
        meshTopNode = prefix + self.geoGrpSuffix

        # clean
        mc.setAttr(orgMesh + '.visibility', 0)
        mc.setAttr(uvMesh + '.visibility', 0)

        if mc.objExists(meshTopNode):
            if redoUV:
                mc.parent(uvMesh, meshTopNode)
            mc.parent(orgMesh, meshTopNode)

        # build data
        self.sysData['redoUV'] = redoUV
        self.sysData['meshs'] = {}
        self.meshData = {'orgMesh': '', 'uvMesh': '', 'outMesh': ''}
        self.meshData['orgMesh'] = orgMesh
        self.meshData['uvMesh'] = uvMesh
        self.meshData['outMesh'] = outMesh
        self.sysData['meshs'][mesh] = self.meshData


    def _invMatrix_ctrl(self, prefix, ctrlList):
        """
        create sec controls by existed ctrllist
        """
        controls = []
        ctrlTopNode = prefix + self.ctrlGrpSuffix

        for ctrl in ctrlList:
            mc.parent(ctrl[0], ctrlTopNode)
            controls.append(ctrl[-1])

        mc.select(cl=True)
        self.sysData['controls'] = {}
        for ctrl in controls:
            self.ctrlData = {'posT': '', 'posR': '', 'posS':'', 'skinJnt': '', 'revLoc': '', 'uvPinGrp': '', 'offsetGrp':'', 'uvPinIkLoc':'', 'uvPinFkLoc':'', 'uvPinNode':''}
            self.ctrlData['posT'] = mc.xform(ctrl, q=1, t=1, ws=1)
            self.ctrlData['posR'] = mc.xform(ctrl, q=1, ro=1, ws=1)
            self.ctrlData['posS'] = mc.xform(ctrl, q=1, s=1, ws=1)
            self.ctrlData['uvPinGrp'] = ctrl + '_grp'
            self.ctrlData['parent'] = []
            self.ctrlData['child'] = []
            self.sysData['controls'][ctrl] = self.ctrlData

    def invMatrix_ctrl(self, prefix, ctrlPosList=None, ctrlNameList=None):
        """
        create sec controls by vtxs positions
        """
        controls = []
        ctrlTopNode = prefix + self.ctrlGrpSuffix

        if not ctrlNameList:
            ctrlNameList = []
            for i in range(len(ctrlPosList)):
                ctrlNameList.append(prefix + self.ctrlSuffix)

        if len(ctrlPosList) != len(ctrlNameList):
            mc.error('len(ctrlPosList) != len(ctrlNameList)')

        for i in range(len(ctrlPosList)):
            posLoc = mc.spaceLocator(p=(0,0,0))[0]
            mc.xform(posLoc, t=ctrlPosList[i][0], ws=True)
            mc.xform(posLoc, ro=ctrlPosList[i][1], ws=True)
            mc.xform(posLoc, s=ctrlPosList[i][2], ws=True)
            crvData = '{0}{1}.cs'.format(self.crvData_path, 'C00_sphere')
            ctrls = controller.create(ctrlNameList[i], crvData, color='cobalt',
                              scale=None, snapTo=posLoc, snapType='both', useShape='',
                              jointCtrl=False, makeGroups=True, worldOrientGroups=False,
                              parent='', tag='animCtrl', ns=0)

            mc.parent(ctrls[0], ctrlTopNode)
            controls.append(ctrls[-1])
            mc.delete(posLoc)

        mc.select(cl=True)
        self.sysData['controls'] = {}
        for ctrl in controls:
            self.ctrlData = {'posT': '', 'posR': '', 'posS':'', 'skinJnt': '', 'revLoc': '', 'uvPinGrp': '', 'uvPinIkLoc':'', 'uvPinFkLoc':'', 'uvPinNode':''}
            self.ctrlData['posT'] = mc.xform(ctrl, q=1, t=1, ws=1)
            self.ctrlData['posR'] = mc.xform(ctrl, q=1, ro=1, ws=1)
            self.ctrlData['posS'] = mc.xform(ctrl, q=1, s=1, ws=1)
            self.ctrlData['uvPinGrp'] = ctrl + '_grp'
            self.ctrlData['parent'] = []
            self.ctrlData['child'] = []
            self.sysData['controls'][ctrl] = self.ctrlData

    def invMatrix_jnt(self, prefix, controls):
        """
        create sec joints by controls
        """
        jntTopNode = prefix + self.jntGrpSuffix

        for ctrl in controls:

            skinjnt = mc.joint(p=(0,0,0), n=ctrl.replace('_ctrl', '_jnt'))
            revLoc = mc.spaceLocator(p=(0,0,0), n=ctrl.replace('_ctrl', '_rev_loc'))[0]
            mc.delete(mc.pointConstraint(ctrl, skinjnt, mo=False))
            mc.delete(mc.pointConstraint(ctrl, revLoc, mo=False))
            mc.parentConstraint(ctrl, skinjnt, mo=True)
            mc.scaleConstraint(ctrl, skinjnt, mo=True)
            mc.parent(skinjnt, jntTopNode)
            mc.parent(revLoc, jntTopNode)

            # get data
            self.sysData['controls'][ctrl]['skinJnt'] = skinjnt
            self.sysData['controls'][ctrl]['revLoc'] = revLoc

    def getUseData_uvPin(self, mesh, obj):
        """
        before create uvPin, we need get some data.
        """
        shapeNode = mc.listRelatives(mesh, c=True)[0]
        closestNode = mc.createNode('closestPointOnMesh', n='uvConst_ClosestPoint_node')
        mc.connectAttr('%s.worldMatrix[0]' % shapeNode, '%s.inputMatrix' % closestNode)
        mc.connectAttr('%s.worldMesh[0]' % shapeNode, '%s.inMesh' % closestNode)
        pos = mc.xform(obj, q=True, ws=True, t=True)
        mc.setAttr('%s.ip' % closestNode, pos[0], pos[1], pos[2])
        # get uv
        closeNode_U = mc.getAttr('%s.u' % closestNode)
        closeNode_V = mc.getAttr('%s.v' % closestNode)
        mc.delete(closestNode)

        return {'u':closeNode_U, 'v':closeNode_V}

    def invMatrix_uvPin(self, prefix, mesh, controls, scaleControl=None):
        """
        create sec system ctrl uvPin
        """
        shapeNode = mc.listRelatives(mesh, c=True)[0]
        # is poly?
        if mc.nodeType(shapeNode) != 'mesh':
            return

        closestNode = mc.createNode('closestPointOnMesh', n='uvConst_ClosestPoint_node')
        mc.connectAttr('%s.worldMatrix[0]' % shapeNode, '%s.inputMatrix' % closestNode)
        mc.connectAttr('%s.worldMesh[0]' % shapeNode, '%s.inMesh' % closestNode)

        uvPinNode = '{0}_uvPin'.format(mesh)
        if not mc.objExists(uvPinNode):
            mc.createNode('uvPin', n=uvPinNode)
            mc.connectAttr('{0}.worldMesh[0]'.format(shapeNode), '{0}.deformedGeometry'.format(uvPinNode))
            mc.connectAttr('{0}.outMesh'.format(shapeNode), '{0}.originalGeometry'.format(uvPinNode))

        uvPinTopNode = prefix + self.uvPinGrpSuffix
        for control in controls:
            uvPinGrp = self.sysData['controls'][control]['uvPinGrp']
            revLoc = self.sysData['controls'][control]['revLoc']
            uvData = self.getUseData_uvPin(mesh, uvPinGrp)
            uvPinIkLoc = mc.spaceLocator(n='{0}_uvPin_ik_loc'.format(uvPinGrp))[0]

            # check attr seriel number
            seriel_num = 0
            coordinateList = mc.listAttr('{0}.coordinate'.format(uvPinNode), m=1)
            if coordinateList:
                seriel_num = int(len(coordinateList)/3)

            mc.connectAttr('{0}.outputMatrix[{1}]'.format(uvPinNode, seriel_num), '{0}.offsetParentMatrix'.format(uvPinIkLoc))
            mc.setAttr('{0}.coordinate[{1}].coordinateU'.format(uvPinNode, seriel_num), uvData['u'])
            mc.setAttr('{0}.coordinate[{1}].coordinateV'.format(uvPinNode, seriel_num), uvData['v'])

            offsetGrp = '{0}_{1}_offest_grp'.format(uvPinGrp, mesh)
            if not mc.objExists(offsetGrp):
                mc.createNode('transform', n=offsetGrp)

            mc.delete(mc.parentConstraint(uvPinGrp, offsetGrp, w=True, mo=False))
            mc.parent(offsetGrp, uvPinIkLoc)
            parentCon = mc.parentConstraint(offsetGrp, uvPinGrp, w=True, mo=True)[0]
            mc.setAttr('%s.interpType' % parentCon, 2)
            mc.scaleConstraint(offsetGrp, uvPinGrp, w=True, mo=True)
            mc.parent(revLoc, offsetGrp)
            mc.parent(uvPinIkLoc, uvPinTopNode)
            if scaleControl:
                mc.scaleConstraint(scaleControl, uvPinIkLoc)

            self.sysData['controls'][control]['uvPinIkLoc'] = uvPinIkLoc
            self.sysData['controls'][control]['uvPinNode'] = uvPinNode
            self.sysData['controls'][control]['offsetGrp'] = offsetGrp

        # clean
        mc.delete(closestNode)

    # def invMatrix_uvPin(self, prefix, mesh, controls, scaleControl=None):
    #     """
    #     create sec system ctrl uvPin
    #     """
    #     shapeNode = mc.listRelatives(mesh, c=True)[0]
    #     # is poly?
    #     if mc.nodeType(shapeNode) != 'mesh':
    #         return
    #
    #     closestNode = mc.createNode('closestPointOnMesh', n='uvConst_ClosestPoint_node')
    #     mc.connectAttr('%s.worldMatrix[0]' % shapeNode, '%s.inputMatrix' % closestNode)
    #     mc.connectAttr('%s.worldMesh[0]' % shapeNode, '%s.inMesh' % closestNode)
    #
    #     uvPinTopNode = prefix + self.uvPinGrpSuffix
    #     for control in controls:
    #         uvPinGrp = self.sysData['controls'][control]['uvPinGrp']
    #         revLoc = self.sysData['controls'][control]['revLoc']
    #         uvData = self.getUseData_uvPin(mesh, uvPinGrp)
    #         uvPinNode = mc.createNode('uvPin', n='{0}_uvPin'.format(uvPinGrp))
    #         uvPinIkLoc = mc.spaceLocator(n='{0}_uvPin_ik_loc'.format(uvPinGrp))[0]
    #
    #         mc.connectAttr('{0}.worldMesh[0]'.format(shapeNode), '{0}.deformedGeometry'.format(uvPinNode))
    #         mc.connectAttr('{0}.outMesh'.format(shapeNode), '{0}.originalGeometry'.format(uvPinNode))
    #         mc.connectAttr('{0}.outputMatrix[0]'.format(uvPinNode), '{0}.offsetParentMatrix'.format(uvPinIkLoc))
    #         mc.setAttr('{0}.coordinate[0].coordinateU'.format(uvPinNode), uvData['u'])
    #         mc.setAttr('{0}.coordinate[0].coordinateV'.format(uvPinNode), uvData['v'])
    #
    #         offsetGrp = '{0}_{1}_offest_grp'.format(uvPinGrp, mesh)
    #         if not mc.objExists(offsetGrp):
    #             mc.createNode('transform', n=offsetGrp)
    #
    #         mc.delete(mc.parentConstraint(uvPinGrp, offsetGrp, w=True, mo=False))
    #         mc.parent(offsetGrp, uvPinIkLoc)
    #         parentCon = mc.parentConstraint(offsetGrp, uvPinGrp, w=True, mo=True)[0]
    #         mc.setAttr('%s.interpType' % parentCon, 2)
    #         mc.scaleConstraint(offsetGrp, uvPinGrp, w=True, mo=True)
    #         mc.parent(revLoc, offsetGrp)
    #         mc.parent(uvPinIkLoc, uvPinTopNode)
    #         if scaleControl:
    #             mc.scaleConstraint(scaleControl, uvPinIkLoc)
    #
    #         self.sysData['controls'][control]['uvPinIkLoc'] = uvPinIkLoc
    #         self.sysData['controls'][control]['uvPinNode'] = uvPinNode
    #         self.sysData['controls'][control]['offsetGrp'] = offsetGrp
    #
    #     # clean
    #     mc.delete(closestNode)

    def redo_uvPin(self, inmSysData, mesh):
        """
        redo uvPin
        get closet point and u,v value
        """
        shapeNode = mc.listRelatives(mesh, c=True)[0]
        for key in inmSysData['controls'].keys():
            uvPinIkLoc = inmSysData['controls'][key]['uvPinIkLoc']
            uvPinGrp = inmSysData['controls'][key]['uvPinGrp']
            uvPinNode = inmSysData['controls'][key]['uvPinNode']
            offsetGrp = inmSysData['controls'][key]['offsetGrp']
            uvData = self.getUseData_uvPin(mesh, uvPinGrp)

            mc.parent(offsetGrp, w=True)
            # disConnect org attr
            orgConAttr_deformed = mc.connectionInfo('{0}.deformedGeometry'.format(uvPinNode), sfd=1)
            orgConAttr_original = mc.connectionInfo('{0}.originalGeometry'.format(uvPinNode), sfd=1)
            mc.disconnectAttr(orgConAttr_deformed, '{0}.deformedGeometry'.format(uvPinNode))
            mc.disconnectAttr(orgConAttr_original, '{0}.originalGeometry'.format(uvPinNode))

            # connect new attr
            mc.connectAttr('{0}.worldMesh[0]'.format(shapeNode), '{0}.deformedGeometry'.format(uvPinNode))
            mc.connectAttr('{0}.outMesh'.format(shapeNode), '{0}.originalGeometry'.format(uvPinNode))
            mc.setAttr('{0}.coordinate[0].coordinateU'.format(uvPinNode), uvData['u'])
            mc.setAttr('{0}.coordinate[0].coordinateV'.format(uvPinNode), uvData['v'])
            mc.parent(offsetGrp, uvPinIkLoc)

    def invMatrix_skin(self, mesh, skinJnt, revLoc):
        """
        create sec skin cluster
        """
        # check skinCluster node.
        skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + mesh + "\")")
        if not skinNode:
            return

        # add infulence.
        skinJnts = mc.skinCluster(skinNode, q=True, inf=True)
        if skinJnt not in skinJnts:
            mc.skinCluster(skinNode, edit=True, ai=skinJnt, dr=4, lw=True, wt=0)

        # invMatrix.
        self.connectBindPreMatrix(skinNode, skinJnt, revLoc)

    def connectBindPreMatrix(self, skinNode, skinJnt, revLoc):
        """
        use revers locator connect skin bindPreMatrix
        """
        skinMatrixList = []
        worldMatrixAttr = skinJnt + '.worldMatrix'
        # get skinMatrixList
        skinMatrixs = mc.listConnections(worldMatrixAttr, d=True, p=True)
        for attr in skinMatrixs:
            if skinNode in attr:
                skinMatrixList.append(attr)

        for matrix in skinMatrixList:
            bindPreMatrixAttr = matrix.replace('matrix', 'bindPreMatrix')
            connectONOFF = mc.listConnections(bindPreMatrixAttr, s=True, p=True)
            if connectONOFF is None:
                mc.connectAttr(revLoc + '.worldInverseMatrix[0]', bindPreMatrixAttr)
            else:
                pass

    def creatSyeTopNode(self, prefix):
        """
        create top node
        """
        self.sysData['prefix'] = prefix
        sysTopNode = prefix + self.sysGrpSuffix
        if not mc.objExists(sysTopNode):
            mc.createNode('transform', n=sysTopNode)

        # geo group & ctrl group & joint group
        meshTopNode = prefix + self.geoGrpSuffix
        if not mc.objExists(meshTopNode):
            mc.createNode('transform', n=meshTopNode)
            mc.setAttr(meshTopNode + '.visibility', 0)
            mc.parent(meshTopNode, sysTopNode)

        ctrlTopNode = prefix + self.ctrlGrpSuffix
        if not mc.objExists(ctrlTopNode):
            mc.createNode('transform', n=ctrlTopNode)
            mc.parent(ctrlTopNode, sysTopNode)

        jntTopNode = prefix + self.jntGrpSuffix
        if not mc.objExists(jntTopNode):
            mc.createNode('transform', n=jntTopNode)
            mc.setAttr(jntTopNode + '.visibility', 0)
            mc.parent(jntTopNode, sysTopNode)

        uvPinTopNode = prefix + self.uvPinGrpSuffix
        if not mc.objExists(uvPinTopNode):
            mc.createNode('transform', n=uvPinTopNode)
            mc.setAttr(uvPinTopNode + '.visibility', 0)
            mc.parent(uvPinTopNode, sysTopNode)

        rootJnt = prefix + self.rootJntSuffix
        if not mc.objExists(rootJnt):
            mc.select(cl=True)
            mc.joint(p=(0,0,0), n=rootJnt)
            self.sysData['rootJnt'] = rootJnt
            mc.parent(rootJnt, jntTopNode)

        # add system tag
        mc.addAttr(sysTopNode, ln='inmSysData', dt='string')
        mc.select(cl=True)
        return sysTopNode

    @undoable
    def createInmSystem(self, prefix=None, mesh=None, ctrlPosList=None):
        """
        create sec system
        """
        """
        create sec system.
        """
        # get mesh and vtxs --------------------------------------------
        if prefix is None:
            prefix = self.ui.prefix_line.text()
        if mesh is None:
            mesh = self.ui.initMesh_line.text()

        if ctrlPosList is None:
            ctrlPosList = []
            vtxs = eval(self.ui.orgVtxs_line.text())
            for vtx in vtxs:
                pos = []
                posT = mc.xform(vtx, q=1, t=1, ws=1)
                posR = mc.xform(vtx, q=1, ro=1, ws=1)
                posS = mc.xform(vtx, q=1, s=1, ws=1)
                pos.append(posT)
                pos.append(posR)
                pos.append(posS)
                ctrlPosList.append(pos)


        # topNode
        sysTopNode = self.creatSyeTopNode(prefix)

        # create meshs --------------------------------------------
        redoUV = aboutUI.confirmDialogWin('Warning', 'Redo UV ?')
        self.invMatrix_mesh(prefix, mesh, redoUV)

        # create ctrls --------------------------------------------
        self.invMatrix_ctrl(prefix, ctrlPosList)

        # create joints
        controls = [key for key in self.sysData['controls'].keys()]
        self.invMatrix_jnt(prefix, controls)

        # creat uvPin
        uvMesh = self.sysData['meshs'][mesh]['uvMesh']
        self.invMatrix_uvPin(prefix, uvMesh, controls)
        self.sysData['initMesh'] = mesh

        # # inv SkinCluster
        rootJnt = prefix + self.rootJntSuffix
        outMesh = self.sysData['meshs'][mesh]['outMesh']
        if mc.objExists(rootJnt) and mc.objExists(outMesh):
            mc.skinCluster(rootJnt, outMesh)

        skinJnts = [self.sysData['controls'][key]['skinJnt'] for key in self.sysData['controls'].keys()]
        revLocs = [self.sysData['controls'][key]['revLoc'] for key in self.sysData['controls'].keys()]

        for i in range(len(skinJnts)):
            self.invMatrix_skin(outMesh, skinJnts[i], revLocs[i])

        # create rebuild data
        mc.setAttr(sysTopNode + '.inmSysData', lock=False)
        mc.setAttr(sysTopNode + '.inmSysData', self.sysData, type='string')
        mc.setAttr(sysTopNode + '.inmSysData', lock=True)

        # clean
        sysTopNodes = [self.ui.sec_sys_lv.item(i).text() for i in range(self.ui.sec_sys_lv.count())]
        if sysTopNode not in sysTopNodes:
            self.ui.sec_sys_lv.addItem(sysTopNode)

    @undoable
    def removeInmSystem(self, inmSys):
        """
        kill sec system
        """
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        prefix = inmSysData['prefix']

        # first remove
        needRemoveGrpSuffix = [self.uvPinGrpSuffix, self.jntGrpSuffix, self.ctrlGrpSuffix]
        for grpSuffix in needRemoveGrpSuffix:
            if mc.objExists(prefix + grpSuffix):
                mc.delete(prefix + grpSuffix)

        # remove meshs
        for key in inmSysData['meshs'].keys():
            self.removeMeshForSys(inmSys, key, rmInitMesh=True)

        mc.delete(inmSys)
        # refresh UI
        self.getInmSystem()

    def resolveSecSystem(self, inmSysData):
        self.ui.prefix_line.setText(inmSysData['prefix'])
        self.resolveSecMeshs(inmSysData)
        self.resolveSecCtrls(inmSysData)

    def resolveSecMeshs(self, inmSysData):
        """
        refresh sec mesh view weight by system data.
        """
        meshs = inmSysData['meshs']
        self.ui.mesh_lv.clear()
        for mesh in meshs:
            self.ui.mesh_lv.addItem(mesh)

        # check initMesh
        allItems =  [self.ui.mesh_lv.item(i) for i in range(self.ui.mesh_lv.count())]
        for i, item in enumerate(allItems):
            if item.text() == inmSysData['initMesh']:
                self.ui.mesh_lv.item(i).setForeground(QtCore.Qt.green)

    def resolveSecCtrls(self, inmSysData):
        """
        refresh sec ctrl view weight by system data.
        """
        controls = inmSysData['controls']
        self.ui.ctrl_lv.clear()

        children = []
        childrenList = [inmSysData['controls'][control]['child'] for control in controls]
        for childList in childrenList:
            children.extend(childList)

        for control in controls:
            if not inmSysData['controls'][control]['parent']:
                item = QtWidgets.QTreeWidgetItem(self.ui.ctrl_lv, [control])
                self.populate_children(inmSysData, item, control)
        self.ui.ctrl_lv.expandAll()

    def resolveSecSystem_forUI(self):
        """
        refresh system ui by system data.
        """
        secSystem = self.ui.sec_sys_lv.currentItem().text()
        sysData = eval(mc.getAttr(secSystem + '.inmSysData'))
        self.resolveSecSystem(sysData)

    def populate_children(self, inmSysData, parent_item, parent_name):
        """
        iterator : add children to ui
        """
        children =  inmSysData['controls'][parent_name]['child']
        if children:
            for child in children:
                item = QtWidgets.QTreeWidgetItem(parent_item, [child])
                self.populate_children(inmSysData, item, child)

    # Modify -----------------------------------------------------------------------------------------
    # {'prefix': 'head_mdl',
    #  'meshs': {'head_mdl': {'orgMesh': 'head_mdl', 'uvMesh': 'head_mdl_uv', 'secMesh': 'head_mdl_sec'}},
    #  'controls': {'head_mdl_inmSec_ctrl': {'posT': [5.894423484802246, 162.91940307617188, 7.334357261657715], 'posR': [0.0, 0.0, 0.0], 'skinJnt': 'head_mdl_inmSec_jnt', 'revLoc': 'head_mdl_inmSec_rev_jnt', 'uvPinGrp': 'head_mdl_inmSec_ctrl_grp'}}}
    @undoable
    def addMeshForSys(self, inmSys=None, addMesh=None, redoUV=False):
        """
        Add sence mesh to sec system
        """
        # step1 - get org sec system data'
        if not inmSys:
            inmSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        # step2 - invMatrix add mesh
        initMesh = inmSysData['initMesh']
        initOutMesh = inmSysData['meshs'][initMesh]['outMesh']
        if not addMesh:
            addMesh = mc.ls(sl=True)[0]
        # is poly
        if not mc.listRelatives(addMesh, ni=1, type='mesh'):
            return
        self.invMatrix_mesh(inmSysData['prefix'], addMesh, redoUV)

        # step3 - invMatrix add mesh skin
        addOutMesh = self.sysData['meshs'][addMesh]['outMesh']
        addSkinNode = mc.skinCluster(inmSysData['rootJnt'], addOutMesh)[0]
        for key in inmSysData['controls']:
            skinJnt = (inmSysData['controls'][key]['skinJnt'])
            revLoc = (inmSysData['controls'][key]['revLoc'])
            self.invMatrix_skin(addOutMesh, skinJnt, revLoc)

        # step4 - update ui & sys date
        inmSysData['meshs'][addMesh] = self.sysData['meshs'][addMesh]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecMeshs(inmSysData)

        # step5 - auto copy base sec skin for add mesh
        baseSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + initOutMesh + "\")")
        if baseSkinNode:
            mc.copySkinWeights(ss=baseSkinNode, ds=addSkinNode, nm=True)


    @undoable
    def removeMeshForSys(self, inmSys=None, rmMesh=None, rmInitMesh=False):
        """
        remove select mesh for sec system,
        when rmInitMesh is False, you didn't can remove init mesh.
        """
        # step1 - get org sec system data'
        if not inmSys:
            inmSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        # step2 - invMatrix add mesh
        if not rmMesh:
            rmMesh = self.ui.mesh_lv.selectedIndexes()[0].data()
            if not mc.objExists(rmMesh):
                return
        if rmMesh == inmSysData['initMesh']:
            if not rmInitMesh:
                aboutUI.confirmDialogWin('Warning:', 'Can not remove init mesh!', button=['Yes'])
                return
            else:
                pass

        orgMesh = inmSysData['meshs'][rmMesh]['orgMesh']
        uvMesh = inmSysData['meshs'][rmMesh]['uvMesh']

        # step3 - reduction
        # Hierarchy
        rmMeshP = mc.listRelatives(rmMesh, p=True)
        if rmMeshP:
            mc.parent(orgMesh, rmMeshP)
        else:
            mc.parent(orgMesh, w=True)
        mc.setAttr(orgMesh + '.visibility', 1)

        # delete output mesh
        mc.select(rmMesh)
        mc.DeleteHistory()
        mc.delete(rmMesh)

        # delete uv mesh
        if uvMesh != orgMesh:
            mc.select(uvMesh)
            mc.DeleteHistory()
            mc.delete(uvMesh)
        mc.rename(orgMesh, rmMesh)

        # step4 - update ui & sys date
        if rmMesh in inmSysData['meshs']:
            del inmSysData['meshs'][rmMesh]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecMeshs(inmSysData)


    @undoable
    def tipMeshForSys(self, inmSys=None, needRenMesh=None, prefix=None):
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        self.sysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        if not prefix:
            prefix='needRep_'

        pyOrgMesh = pm.PyNode(self.sysData['meshs'][needRenMesh]['orgMesh'])
        pyOutMesh = pm.PyNode(self.sysData['meshs'][needRenMesh]['outMesh'])

        tipMesh = prefix + needRenMesh
        inmSysData['meshs'][tipMesh] = {}
        inmSysData['meshs'][tipMesh]['orgMesh'] = self.renameObjCmd(pyOrgMesh, reType='prefix', prefix=prefix)
        inmSysData['meshs'][tipMesh]['outMesh'] = self.renameObjCmd(pyOutMesh, reType='prefix', prefix=prefix)

        if needRenMesh == self.sysData['initMesh'] and self.sysData['redoUV']:
            pyUvMesh = pm.PyNode(self.sysData['meshs'][needRenMesh]['uvMesh'])
            inmSysData['initMesh'] = tipMesh
            inmSysData['meshs'][tipMesh]['uvMesh'] = self.renameObjCmd(pyUvMesh, reType='prefix', prefix=prefix)

        del inmSysData['meshs'][needRenMesh]
        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecMeshs(inmSysData)

    @undoable
    def replaceMeshForSys(self, inmSys=None, needRepMesh=None, targetMesh=None):
        """
        replace sec mesh
        when need replace is initMesh , redo uvPin.
        """
        if not mc.listRelatives(targetMesh, ni=1, type='mesh'):
            mc.warning('Current selected object is not mesh')
            return

        # get real system data
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        self.sysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        replaceUVPin = False
        redoUV = False
        if needRepMesh == inmSysData['initMesh']:
            replaceUVPin = True
            redoUV = inmSysData['redoUV']

        # find need replace mesh data
        needRepSecMesh = inmSysData['meshs'][needRepMesh]['outMesh']

        # add target mesh in sec system and refresh sys data
        self.addMeshForSys(inmSys, targetMesh, redoUV)
        inmSysData['meshs'][targetMesh] = self.sysData['meshs'][targetMesh]

        # do copy skin
        targetSecMesh = inmSysData['meshs'][targetMesh]['outMesh']
        addSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + targetSecMesh + "\")")
        needRepSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + needRepSecMesh + "\")")
        if needRepSkinNode:
            mc.copySkinWeights(ss=needRepSkinNode, ds=addSkinNode, nm=True)

        if replaceUVPin:
            uvMesh = inmSysData['meshs'][targetMesh]['uvMesh']
            self.redo_uvPin(inmSysData, uvMesh)
            inmSysData['initMesh'] = targetMesh

        # re write sys data
        self.updateInmSysData(inmSys, inmSysData)
        self.removeMeshForSys(inmSys, needRepMesh)

    @undoable
    def _addCtrlForSys(self, inmSys=None, ctrlList=None):
        """
        add existed ctrl for sys without create ctrl.
        """
        # step1 - get org sec system data
        if not inmSys:
            inmSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        prefix = inmSysData['prefix']

        # ctrl
        if ctrlList:
            self._invMatrix_ctrl(prefix, ctrlList)

        # jnt
        controls = [key for key in self.sysData['controls'].keys()]
        self.invMatrix_jnt(prefix, controls)

        # uvPin
        sysInitMesh = inmSysData['initMesh']
        uvMesh = inmSysData['meshs'][sysInitMesh]['uvMesh']
        self.invMatrix_uvPin(prefix, uvMesh, controls)

        # skin
        outMeshs = [inmSysData['meshs'][key]['outMesh'] for key in inmSysData['meshs'].keys()]
        skinJnts = [self.sysData['controls'][key]['skinJnt'] for key in self.sysData['controls'].keys()]
        revLocs = [self.sysData['controls'][key]['revLoc'] for key in self.sysData['controls'].keys()]
        for outMesh in outMeshs:
            for i in range(len(skinJnts)):
                self.invMatrix_skin(outMesh, skinJnts[i], revLocs[i])

        # update ui & sys date
        for ctrl in controls:
            inmSysData['controls'][ctrl] = self.sysData['controls'][ctrl]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecCtrls(inmSysData)

    @undoable
    def addCtrlForSys(self, inmSys=None, ctrlPosList=None):
        """
        add ctrl for sys
        select some vetex (get position)
        """
        # step1 - get org sec system data
        if not inmSys:
            inmSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        prefix = inmSysData['prefix']

        # ctrl
        if not ctrlPosList:
            ctrlPosList = []
            vtxs = mc.ls(sl=1, fl=1)
            for vtx in vtxs:
                pos = []
                posT = mc.xform(vtx, q=1, t=1, ws=1)
                posR = mc.xform(vtx, q=1, ro=1, ws=1)
                posS = mc.xform(vtx, q=1, s=1, ws=1)
                pos.append(posT)
                pos.append(posR)
                pos.append(posS)
                ctrlPosList.append(pos)

        self.invMatrix_ctrl(prefix, ctrlPosList)

        # jnt
        controls = [key for key in self.sysData['controls'].keys()]
        self.invMatrix_jnt(prefix, controls)

        # uvPin
        sysInitMesh = inmSysData['initMesh']
        uvMesh = inmSysData['meshs'][sysInitMesh]['uvMesh']
        self.invMatrix_uvPin(prefix, uvMesh, controls)

        # skin
        outMeshs = [inmSysData['meshs'][key]['outMesh'] for key in inmSysData['meshs'].keys()]
        skinJnts = [self.sysData['controls'][key]['skinJnt'] for key in self.sysData['controls'].keys()]
        revLocs = [self.sysData['controls'][key]['revLoc'] for key in self.sysData['controls'].keys()]
        for outMesh in outMeshs:
            for i in range(len(skinJnts)):
                self.invMatrix_skin(outMesh, skinJnts[i], revLocs[i])

        # update ui & sys date
        for ctrl in controls:
            inmSysData['controls'][ctrl] = self.sysData['controls'][ctrl]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecCtrls(inmSysData)


    def getCtrlChildForSys(self, inmSysData, control):
        """
        get ctrl child, when some ctrl need remove,
        this code can get ctrl child.
        """
        removeChildren = []
        children = inmSysData['controls'][control]['child']
        removeChildren.extend(children)
        for child in children:
            self.getCtrlChildForSys(inmSysData, child)
        return removeChildren

    @undoable
    def removeCtrlForSys(self):
        """
        remove ctrl for sec system
        """
        mc.select(cl=True)
        # step1 - get org sec system data
        inmSys = self.ui.sec_sys_lv.selectedIndexes()[0].data()
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        # need remove controls
        rootJnt = inmSysData['rootJnt']
        mc.setAttr(rootJnt + '.liw', 1)

        meshs = inmSysData['meshs']
        controls = [index.data() for index in self.ui.ctrl_lv.selectedIndexes()]
        skinJnts = [inmSysData['controls'][key]['skinJnt'] for key in inmSysData['controls'].keys()]
        for jnt in skinJnts:
            mc.setAttr(jnt + '.liw', 1)

        mc.select(cl=1)
        for control in controls:
            # get skin joint and reverse joint
            skinJnt = inmSysData['controls'][control]['skinJnt']
            revLoc = inmSysData['controls'][control]['revLoc']

            mc.setAttr(skinJnt + '.liw', 0)
            # remove skin joint weight.
            for mesh in meshs:
                outMesh = inmSysData['meshs'][mesh]['outMesh']
                if not outMesh:
                    return

                skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + outMesh + "\")")
                if skinJnt in mc.skinCluster(skinNode, q=True, inf=True):
                    mc.select(cl=1)
                    mc.skinCluster(skinNode, e=True, siv=skinJnt)
                    infVtxs = mc.ls(sl=True, fl=True)
                    mc.select(cl=1)
                    for vtx in infVtxs:
                        mc.skinPercent(skinNode, vtx, transformValue=[(rootJnt, 1.0)])
                    mc.skinCluster(skinNode, e=True, ri=skinJnt)
            mc.setAttr(skinJnt + '.liw', 1)

            # delete unused joint
            mc.delete(skinJnt)
            mc.delete(revLoc)
            # delete unused control & uvPinIkLoc & uvPinFkLoc
            mc.delete(inmSysData['controls'][control]['uvPinGrp'])
            mc.delete(inmSysData['controls'][control]['uvPinIkLoc'])
            if mc.objExists(inmSysData['controls'][control]['uvPinFkLoc']):
                mc.delete(inmSysData['controls'][control]['uvPinFkLoc'])

            # update system data and ui
            # remove parent data
            parentCtrl = inmSysData['controls'][control]['parent']
            if parentCtrl:
                inmSysData['controls'][parentCtrl[0]]['child'].remove(control)

            # remove child data
            neeRemoveChildrenData = self.getCtrlChildForSys(inmSysData, control)
            for child in neeRemoveChildrenData:
                del inmSysData['controls'][child]

            # remove self
            del inmSysData['controls'][control]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecCtrls(inmSysData)

    def exportSecSys(self, secSys):
        """
        export sec system data
        """
        mc.select(cl=True)
        # set path use to export secound system data
        inmSysData = eval(mc.getAttr(secSys + '.inmSysData'))
        setPath = mc.fileDialog2(fm=0, okc='Save', fileFilter="*.json")
        if not setPath:
            return

        try:
            fileName = setPath[0]
            with open(fileName, 'w') as f:
                exportData = json.dumps(inmSysData, sort_keys=True, indent=4)
                f.write(exportData)
            sys.stdout.write('{0} data export is Ok ! Path : {1} \n'.format(secSys, fileName))
        except:
            msgs = traceback.format_exc()
            mc.error(msgs)


    def modifyUiFromJson(self):
        """
        create ui widget by export json file.
        show modify ui widget and add some textField
        """
        mc.select(cl=True)
        # get system data
        setPath = mc.fileDialog2(fm=1, okc='read', fileFilter="*.json")
        if not setPath:
            return
        fileName = setPath[0]
        with open(fileName, 'r') as f:
            self.modifySysData = json.load(f)

        prefix = self.modifySysData['prefix']
        initMesh = self.modifySysData['initMesh']
        self.ui.md_prefix_line.setText(prefix)
        self.ui.md_initMesh_line.setText(initMesh)
        if not mc.objExists(initMesh):
            self.ui.md_initMesh_line.setStyleSheet("color: red;")

        # create ui widget
        for i, mesh in enumerate(self.modifySysData['meshs']):
            if mesh != self.modifySysData['initMesh']:
                # add label
                arg = mesh
                self.mdArg = QtWidgets.QLabel(mesh)
                self.ui.md_mesh_grid.addWidget(self.mdArg, i, 0)
                # add field
                self.mdField = QtWidgets.QLineEdit(self)
                self.mdField.setObjectName(arg + '_field')
                self.mdField.setText(str(mesh))
                if not mc.objExists(mesh):
                    self.mdField.setStyleSheet("color: red;")
                self.ui.md_mesh_grid.addWidget(self.mdField, i, 1)

        self.ui.mesh_gb.hide()
        self.ui.ctrl_gb.hide()
        self.ui.modify_gb.show()

    def getModifyDataFromUI(self):
        """
        get ui data behind user modify mesh names.
        """
        self.modifySysData['initMesh'] = self.ui.md_initMesh_line.text()
        # get modify meshs
        modifyMeshs = [self.ui.md_initMesh_line.text()]
        # modify meshs list add user modify result
        for i in range( self.ui.md_mesh_grid.count()):
            widget = self.ui.md_mesh_grid.itemAt(i).widget()
            if re.search('QtWidgets.QLabel', str(widget)):
                value = self.ui.md_mesh_grid.itemAt(i+1).widget().text()
                modifyMeshs.append(value)
        self.modifySysData['meshs'] = modifyMeshs

    def exitModifyUI(self):
        """
        exit modify ui
        """
        self.ui.mesh_gb.show()
        self.ui.ctrl_gb.show()
        self.ui.modify_gb.hide()
        self.clearMdMesh_grid()

    def clearMdMesh_grid(self):
        """
        delete ui widget from 10~1
        """
        for i in reversed(range(self.ui.md_mesh_grid.count())):
            self.ui.md_mesh_grid.itemAt(i).widget().deleteLater()
            self.ui.md_mesh_grid.removeItem( self.ui.md_mesh_grid.itemAt(i) )

    @undoable
    def importSecSys(self):
        """
        solve export sec data
        import sec system.
        """
        # get mesh and vtxs --------------------------------------------
        self.getModifyDataFromUI()

        prefix = self.modifySysData['prefix']
        initMesh = self.modifySysData['initMesh']
        ctrlPosList = []
        ctrlNameList = []
        for key in self.modifySysData['controls'].keys():
            ctrlNameList.append(key)
            pos = [self.modifySysData['controls'][key]['posT'],
                   self.modifySysData['controls'][key]['posR'],
                   self.modifySysData['controls'][key]['posS'],]
            ctrlPosList.append(pos)

        # topNode
        sysTopNode = self.creatSyeTopNode(prefix)

        # create meshs --------------------------------------------
        redoUV = aboutUI.confirmDialogWin('Warning', 'Redo UV ?')
        self.invMatrix_mesh(prefix, initMesh, redoUV)

        # create ctrls --------------------------------------------
        self.invMatrix_ctrl(prefix, ctrlPosList, ctrlNameList)

        # create joints
        controls = [key for key in self.sysData['controls'].keys()]
        self.invMatrix_jnt(prefix, controls)

        # creat uvPin
        uvMesh = self.sysData['meshs'][initMesh]['uvMesh']
        self.invMatrix_uvPin(prefix, uvMesh, controls)
        self.sysData['initMesh'] = initMesh

        # inv SkinCluster
        rootJnt = prefix + self.rootJntSuffix
        outMesh = self.sysData['meshs'][initMesh]['outMesh']
        if mc.objExists(rootJnt) and mc.objExists(outMesh):
            mc.skinCluster(rootJnt, outMesh)

        skinJnts = [self.sysData['controls'][key]['skinJnt'] for key in self.sysData['controls'].keys()]
        revLocs = [self.sysData['controls'][key]['revLoc'] for key in self.sysData['controls'].keys()]

        for i in range(len(skinJnts)):
            self.invMatrix_skin(outMesh, skinJnts[i], revLocs[i])

        # create rebuild data
        self.updateInmSysData(sysTopNode, self.sysData)

        # redo fk hierarchy
        for control in controls:
            children = self.modifySysData['controls'][control]['child']
            if children:
                for child in children:
                    controls = [control, child]
                    self.changeFk(sysTopNode, controls, fkType='one2one')

        # refresh UI
        sysTopNodes = [self.ui.sec_sys_lv.item(i).text() for i in range(self.ui.sec_sys_lv.count())]
        if sysTopNode not in sysTopNodes:
            self.ui.sec_sys_lv.addItem(sysTopNode)

        # add other meshs
        for mesh in self.modifySysData['meshs']:
            if mesh != initMesh:
                self.addMeshForSys(sysTopNode, mesh)
        # exit modify ui
        self.exitModifyUI()

    def renameObjCmd(self, obj, reType, **kwargs):
        """
        rename cmd include add prefix & replace string.
        """
        result = None
        if reType =='prefix':
            result = self.namer.addPrefix(obj, kwargs['prefix'])
        elif reType == 'search':
            result = self.namer.replaceStr(obj, kwargs['searchStr'], kwargs['replaceStr'])
        return result

    @undoable
    def renameSecCtrl(self, inmSys, ctrls, reType='prefix'):
        """
        rename sec ctrl (skinjnt revloc child parent uvpinGrp uvpinIkloc uvPinFkloc uvPinOffset uvPinNode)
        """
        mc.select(cl=True)
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))

        # get rename type and string
        prefix, searchStr, replaceStr = ('','','')
        if reType == 'prefix':
            prefix = aboutUI.promptDialogWin(titleDialog='Add Prefix', instrunctions='Prefix:', buttons=['OK', 'Cancel'], text=None)
        elif reType == 'search':
            searchReplace = aboutUI.promptDialogWin(titleDialog='Search & Replace', instrunctions='Search : Replace', buttons=['OK', 'Cancel'], text='L:R')
            if ':' in searchReplace:
                searchStr = searchReplace.split(':')[0]
                replaceStr = searchReplace.split(':')[1]

        # do rename
        for ctrl in ctrls:
            childs = mc.listRelatives(inmSysData['controls'][ctrl]['uvPinGrp'], ad=True)
            for child in childs:
                if child != inmSysData['controls'][ctrl]['uvPinGrp'] and child != ctrl and ctrl in child:
                    child = pm.PyNode(child)
                    self.renameObjCmd(child, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)

            pyctrl = pm.PyNode(ctrl)
            pySkinJnt = pm.PyNode(inmSysData['controls'][ctrl]['skinJnt'])
            pyRevJnt = pm.PyNode(inmSysData['controls'][ctrl]['revLoc'])
            pyUvPinGrp = pm.PyNode(inmSysData['controls'][ctrl]['uvPinGrp'])
            pyUvPinIkLoc = pm.PyNode(inmSysData['controls'][ctrl]['uvPinIkLoc'])
            pyOffsetGrp = pm.PyNode(inmSysData['controls'][ctrl]['offsetGrp'])
            #pyUvPinNode = pm.PyNode(inmSysData['controls'][ctrl]['uvPinNode'])

            newCtrl = self.renameObjCmd(pyctrl, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            inmSysData['controls'][newCtrl] = inmSysData['controls'][ctrl]
            inmSysData['controls'][newCtrl]['skinJnt'] = self.renameObjCmd(pySkinJnt, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            inmSysData['controls'][newCtrl]['revLoc'] = self.renameObjCmd(pyRevJnt, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            inmSysData['controls'][newCtrl]['uvPinGrp'] = self.renameObjCmd(pyUvPinGrp, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            inmSysData['controls'][newCtrl]['uvPinIkLoc'] = self.renameObjCmd(pyUvPinIkLoc, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            inmSysData['controls'][newCtrl]['offsetGrp'] = self.renameObjCmd(pyOffsetGrp, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)
            #inmSysData['controls'][newCtrl]['uvPinNode'] = self.renameObjCmd(pyUvPinNode, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)

            if inmSysData['controls'][ctrl]['uvPinFkLoc']:
                pyUvPinFkLoc = pm.PyNode(inmSysData['controls'][ctrl]['uvPinFkLoc'])
                inmSysData['controls'][newCtrl]['uvPinFkLoc'] = self.renameObjCmd(pyUvPinFkLoc, reType=reType, prefix=prefix, searchStr=searchStr, replaceStr=replaceStr)

            # rename parent & child
            for control in inmSysData['controls']:
                if inmSysData['controls'][control]['parent']:
                    parent = inmSysData['controls'][control]['parent'][0]
                    if parent == ctrl:
                        inmSysData['controls'][control]['parent'] = [newCtrl]

                child = inmSysData['controls'][control]['child']
                if child and ctrl in child:
                    inmSysData['controls'][control]['child'].remove(ctrl)
                    inmSysData['controls'][control]['child'].append(newCtrl)

            # delete old name control data
            del inmSysData['controls'][ctrl]

        self.updateInmSysData(inmSys, inmSysData)
        self.resolveSecCtrls(inmSysData)

    @undoable
    def mirrorSecCtrl(self, inmSys, ctrls):
        """
        mirror sec ctrl
        """
        mc.select(cl=True)
        ctrlList = []
        for ctrl in ctrls:
            ctrlData = controller.mirrorCtrl(ctrl)
            controller.setColor(ctrlData[-1], 'violet')
            ctrlList.append(ctrlData)
        self._addCtrlForSys(inmSys, ctrlList)

    @undoable
    def ctrl2Fk(self, inmSys, childCtrl, parentCtrl):
        """
        ik contro to fk hirerarchy
        create help fk locator
        get and set parent object and children object
        """
        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        uvPinChildFkLoc = childCtrl + '_uvPin_fk_loc'
        uvPinParentFkLoc = parentCtrl + '_uvPin_fk_loc'
        uvPinChildGrp = inmSysData['controls'][childCtrl]['uvPinGrp']
        uvPinParentGrp = inmSysData['controls'][parentCtrl]['uvPinGrp']
        uvPinFkChildOffsetGrp = mc.listRelatives(inmSysData['controls'][childCtrl]['uvPinIkLoc'], type='transform')[0]
        uvPinFkParentOffsetGrp = mc.listRelatives(inmSysData['controls'][parentCtrl]['uvPinIkLoc'], type='transform')[0]
        uvPinSysGrp = inmSysData['prefix'] + self.uvPinGrpSuffix
        keyAttr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']

        # modify hierarchy
        if not mc.objExists(uvPinChildFkLoc):
            mc.spaceLocator(p=(0, 0, 0), name=uvPinChildFkLoc)
            mc.delete(mc.parentConstraint(uvPinChildGrp, uvPinChildFkLoc, mo=False))
            mc.parentConstraint(uvPinFkChildOffsetGrp, uvPinChildFkLoc, mo=True)
            mc.delete(mc.listRelatives(uvPinChildGrp, type='constraint'))
            mc.parent(uvPinChildFkLoc, uvPinSysGrp)
            for attr in keyAttr:
                mc.connectAttr(uvPinChildFkLoc + attr, uvPinChildGrp + attr)

        if not mc.objExists(uvPinParentFkLoc):
            mc.spaceLocator(p=(0, 0, 0), name=uvPinParentFkLoc)
            mc.delete(mc.parentConstraint(uvPinParentGrp, uvPinParentFkLoc, mo=False))
            mc.parentConstraint(uvPinFkParentOffsetGrp, uvPinParentFkLoc, mo=True)
            mc.delete(mc.listRelatives(uvPinParentGrp, type='constraint'))
            mc.parent(uvPinParentFkLoc, uvPinSysGrp)
            for attr in keyAttr:
                mc.connectAttr(uvPinParentFkLoc + attr, uvPinParentGrp + attr)

        pObjs = mc.listRelatives(uvPinChildGrp, p=True)
        if parentCtrl != pObjs[0]:
            mc.parent(uvPinChildGrp, parentCtrl)
            mc.parent(uvPinChildFkLoc, uvPinParentFkLoc)

            # set parent data
            if inmSysData['controls'][childCtrl]['parent']:
                orgParentCtrl = inmSysData['controls'][childCtrl]['parent'][0]
                inmSysData['controls'][orgParentCtrl]['child'].remove(childCtrl)

            # set child
            if childCtrl not in inmSysData['controls'][parentCtrl]['child']:
                inmSysData['controls'][parentCtrl]['child'].append(childCtrl)
            inmSysData['controls'][childCtrl]['parent'] = []
            inmSysData['controls'][childCtrl]['parent'].append(parentCtrl)

        inmSysData['controls'][childCtrl]['uvPinFkLoc'] = uvPinChildFkLoc
        inmSysData['controls'][parentCtrl]['uvPinFkLoc'] = uvPinParentFkLoc

        # update inmsys data
        self.updateInmSysData(inmSys, inmSysData)

    @undoable
    def ctrl2World(self, inmSys, ctrl):
        """
        split fk ctrl hirerarchy
        """

        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        ctrlGrp = inmSysData['prefix'] + self.ctrlGrpSuffix
        uvlocGrp = inmSysData['prefix'] + self.uvPinGrpSuffix

        uvPinGrp = inmSysData['controls'][ctrl]['uvPinGrp']
        uvPinFkLoc = inmSysData['controls'][ctrl]['uvPinFkLoc']

        if mc.listRelatives(uvPinGrp, p=True) != ctrlGrp:
            # modify hirerarchy
            if mc.objExists(ctrlGrp) and mc.objExists(uvPinGrp):
                mc.parent(uvPinGrp, ctrlGrp)
            if uvPinFkLoc and mc.objExists(uvPinFkLoc):
                mc.parent(uvPinFkLoc, uvlocGrp)

            # modify data
            parentCtrl = inmSysData['controls'][ctrl]['parent']
            if parentCtrl:
                inmSysData['controls'][parentCtrl[0]]['child'].remove(ctrl)
                inmSysData['controls'][ctrl]['parent'] = []

        # update inmsys data
        self.updateInmSysData(inmSys, inmSysData)

    def changeFk(self, inmSys, controls, fkType='one2one'):
        """
        chang ik control to fk cmd
        """
        mc.select(cl=True)
        if fkType == 'one2one':
            for i in range(len(controls)-1):
                self.ctrl2Fk(inmSys, controls[i+1], controls[i])
        if fkType == 'mult2one':
            for i in range(len(controls)-1):
                self.ctrl2Fk(inmSys, controls[i], controls[-1])
        if fkType == 'one2world':
            for i in range(len(controls)):
                self.ctrl2World(inmSys, controls[i])

        inmSysData = eval(mc.getAttr(inmSys + '.inmSysData'))
        self.resolveSecCtrls(inmSysData)
