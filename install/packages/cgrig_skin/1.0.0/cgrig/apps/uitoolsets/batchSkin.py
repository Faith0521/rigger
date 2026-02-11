#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/11/14 14:43
# @Author : yinyufei
# @File : batchSkin.py
# @Project : TeamCode
from functools import partial
from maya import cmds
import maya.mel as mel
from Qt import QtWidgets, QtCore, QtGui
from cgrig.libs.maya.cmds.skin import skinreplacejoints
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.maya.cmds.rig import skin, blendshape
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.utils.filesystem import ProgressBarContext


class BatchSkinToolUI(toolsetwidget.ToolsetWidget):
    id = "batchSkinTool"
    uiData = {"label": "Batch Skin Window",
              "icon": "split",
              "tooltip": "Batch Skin Tool",
              "defaultActionDoubleClick": False
              }

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run"""
        # data
        self.orgMeshDict = {}
        self.newMeshDict = {}
        self.jointTransferDict = {}

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = CompactLayout(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def postContentSetup(self):
        """Last of the initialize code"""
        self.compactWidgetConnections()

    def defaultAction(self):
        """Double Click"""
        pass

    # ------------------
    # PROPERTIES
    # ------------------
    def _onTypeChanged(self):
        if self.compactWidget.type_cb.currentIndex() == 0:
            self.compactWidget.loadNew.setEnabled(False)
        else:
            self.compactWidget.loadNew.setEnabled(True)

        if self.compactWidget.type_cb.currentIndex() == 2:
            self.compactWidget.copyBs.setEnabled(False)
        else:
            self.compactWidget.copyBs.setEnabled(True)
        if self.compactWidget.prefixonCb.isChecked():
            self.compactWidget.loadTarget.setEnabled(False)
        else:
            self.compactWidget.loadTarget.setEnabled(True)
    
    def meshCompare(self):
        self.newMeshDict = {}
        for key in self.orgMeshDict.keys():
            oldMesh = self.orgMeshDict[key].split(' : ')[1]
            similarMeshs = cmds.ls(oldMesh.split('|')[-1])
            if oldMesh in similarMeshs:
                similarMeshs.remove(oldMesh)
                if len(similarMeshs) == 1:
                    self.newMeshDict[key] = similarMeshs[0]
                else:
                    self.newMeshDict[key] = 'MISS'
        self.compactWidget.newView.clear()
        for key in self.newMeshDict.keys():
            self.compactWidget.newView.addItem(str(key) + ' : ' + self.newMeshDict[key])
    
    def loadOrgMesh(self):
        meshs = cmds.ls(sl=1, ap=1)
        self.compactWidget.oldView.clear()
        self.compactWidget.newView.clear()
        for index, mesh in enumerate(meshs):
            shape = cmds.listRelatives(mesh, c=True, f=True)[0]
            self.orgMeshDict[index] = str(index) + ' : ' + str(mesh)
            if cmds.nodeType(shape, api=True) == 'kMesh':
                self.compactWidget.oldView.addItem( str(index) + ' : ' + str(mesh) )

        if self.compactWidget.type_cb.currentIndex() == 0:
            self.meshCompare()

        elif self.compactWidget.type_cb.currentIndex() == 1:
            self.compactWidget.oldView.clear()
            self.compactWidget.oldView.addItem('0 : ' + str(meshs[0]))
            self.orgMeshDict = {0: '0 : ' + str(meshs[0])}

    def loadNewMesh(self):
        meshs = cmds.ls(sl=1, ap=1)
        self.compactWidget.newView.clear()
        for index, mesh in enumerate(meshs):
            shape = cmds.listRelatives(mesh, c=True, f=True)[0]
            self.newMeshDict[index] = str(index) + ' : ' + str(mesh)
            if cmds.nodeType(shape, api=True) == 'kMesh':
                self.compactWidget.newView.addItem(str(index) + ' : ' + str(mesh))

        if self.compactWidget.type_cb.currentIndex() == 2:
            self.compactWidget.newView.clear()
            self.compactWidget.newView.addItem(meshs[0])
            self.newMeshDict = {0: '0 : ' + str(meshs[0])}
    
    @toolsetwidget.ToolsetWidget.undoDecorator
    def copySkin_cmd(self):
        inf1A = self.compactWidget.inf1_cb.currentText()
        inf2A = self.compactWidget.inf2_cb.currentText()
        oldMeshs = [self.compactWidget.oldView.item(i).text().split(' : ')[1] for i in range(self.compactWidget.oldView.count())]
        newMeshs = [self.compactWidget.newView.item(i).text().split(' : ')[1] for i in range(self.compactWidget.newView.count())]

        if self.compactWidget.type_cb.currentIndex() == 0:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if cmds.objExists(oldMeshs[index]) and cmds.objExists(newMeshs[index]):
                    skin.copySkin(oldMeshs[index], newMeshs[index], inf1A, inf2A)

        elif self.compactWidget.type_cb.currentIndex() == 1:
            for index, mesh in enumerate(newMeshs):
                skin.copySkin(oldMeshs[0], newMeshs[index], inf1A, inf2A)

        elif self.compactWidget.type_cb.currentIndex() == 2:
            allSkinJnts = self.getMeshsSkinJnts(oldMeshs)
            newSkinNode = mel.eval("findRelatedSkinCluster" + "(\"" + newMeshs[0] + "\")")
            cmds.delete(newSkinNode)
            cmds.skinCluster(allSkinJnts, newMeshs[0], mi=10, rui=False, tsb=True)
            cmds.copySkinWeights(oldMeshs, newMeshs[0], noMirror=True, surfaceAssociation='closestPoint',
                               influenceAssociation=[inf1A, inf2A])

        elif self.compactWidget.type_cb.currentIndex() == 3:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if cmds.objExists(oldMeshs[index]) and cmds.objExists(newMeshs[index]):
                    skin.copySkin(oldMeshs[index], newMeshs[index], inf1A, inf2A)
    
    @toolsetwidget.ToolsetWidget.undoDecorator
    def copyBs_cmd(self):
        oldMeshs = [self.compactWidget.oldView.item(i).text().split(' : ')[1] for i in range(self.compactWidget.oldView.count())]
        newMeshs = [self.compactWidget.newView.item(i).text().split(' : ')[1] for i in range(self.compactWidget.newView.count())]

        if self.compactWidget.type_cb.currentIndex() == 0:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if cmds.objExists(oldMeshs[index]) and cmds.objExists(newMeshs[index]):
                    blendshape.copyBs(oldMeshs[index], newMeshs[index], skipLock=True, replaceConnect=True)

        elif self.compactWidget.type_cb.currentIndex() == 1:
            for index, mesh in enumerate(newMeshs):
                blendshape.copyBs(oldMeshs[0], newMeshs[index], skipLock=True, replaceConnect=True)

        elif self.compactWidget.type_cb.currentIndex() == 2:
            cmds.warning(' "* to One" can not support bs copy !')
            return

        elif self.compactWidget.type_cb.currentIndex() == 3:
            if len(oldMeshs) != len(newMeshs):
                return
            for index, mesh in enumerate(oldMeshs):
                if cmds.objExists(oldMeshs[index]) and cmds.objExists(newMeshs[index]):
                    blendshape.copyBs(oldMeshs[index], newMeshs[index], skipLock=True, replaceConnect=True)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def unlockJoints_cmd(self):
        jnts = cmds.ls(type='joint')
        for jnt in jnts:
            if 'lockInfluenceWeights' in cmds.listAttr(jnt):
                cmds.setAttr(jnt + '.liw', 0)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def remove_cmd(self):
        mel.eval('removeUnusedInfluences;')

    @toolsetwidget.ToolsetWidget.undoDecorator
    def pruneWeightOptions(self):
        pruneBelow = self.compactWidget.pruneSmallLe.value()
        mel.eval('doPruneSkinClusterWeightsArgList 1 { "%s" }' % str(pruneBelow))

    @toolsetwidget.ToolsetWidget.undoDecorator
    def exporttSkin(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save skin weights path", filter="*.skin")
        if not filePath:  # cancel
            return
        skin.exportWeights(filePath)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def importSkin(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import skin weights path", filter="*.skin")
        if not filePath:  # cancel
            return
        skin.importWeights(filePath)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def copyBsWeight_cmd(self):
        sels = cmds.ls(sl=True)
        if len(sels) >= 2:
            sourceObj = sels[0]
            sourceShape = cmds.listRelatives(sourceObj, s=True)[0]
            sourceBlendShape = blendshape.getBlendshapeNodes(sourceObj)[0]
            destinationObjs = sels[1:]
            for destinationObj in destinationObjs:
                destinationBlendShape = blendshape.getBlendshapeNodes(destinationObj)[0]
                if sourceBlendShape != None:
                    if destinationBlendShape != None:
                        vtxs = cmds.ls(sourceShape + '.vtx[0:]', fl=True)
                        vtxNum = len(vtxs)
                        for x in range(vtxNum):
                            weight = cmds.getAttr('%s.it[0].bw[%d]' % (sourceBlendShape, int(x)))
                            cmds.setAttr('%s.it[0].bw[%d]' % (destinationBlendShape, int(x)), weight)
        else:
            cmds.warning('plase select at least two model')

    def loadSource_cmd(self):
        selections = cmds.ls(selection=True, type="joint")
        self.compactWidget.sourceView.clear()
        self.jointTransferDict = {}
        if not selections: return
        for joint in selections:
            self.compactWidget.sourceView.addItem(joint)
            self.jointTransferDict[joint] = 'MISS'
            if self.compactWidget.prefixonCb.isChecked():
                prefix = self.compactWidget.Prefix.text()
                suffix = self.compactWidget.Suffix.text()
                target_joint = "{}{}{}".format(prefix, joint, suffix)
                if cmds.objExists(target_joint) and not target_joint == joint:
                    self.jointTransferDict[joint] = target_joint
        if self.compactWidget.prefixonCb.isChecked():
            self.compactWidget.targetView.clear()
            for source,target in self.jointTransferDict.items():
                self.compactWidget.targetView.addItem(target)

    def loadTarget_cmd(self):
        selections = cmds.ls(selection=True, type="joint")
        self.compactWidget.targetView.clear()
        if not selections: return
        target_joints = []
        for joint in selections:
            self.compactWidget.targetView.addItem(joint)
            target_joints.append(joint)
        if len(list(self.jointTransferDict.keys())) != len(target_joints):
            cmds.warning('the number of source joints is not equal to the number of target joints selected')
            return

        for key, new_val in zip(self.jointTransferDict.keys(), target_joints):
            self.jointTransferDict[key] = new_val

    @toolsetwidget.ToolsetWidget.undoDecorator
    def transfer_cmd(self):
        selections = cmds.ls(selection=True)
        if not selections: return
        for mesh in selections:
            skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + mesh + "\")")
            if not skinNode: continue
            boundJoints = list(self.jointTransferDict.keys())
            replaceJoints = list(self.jointTransferDict.values())
            progressBar = ProgressBarContext(maxValue=len(boundJoints), step=1, ismain=False,
                                             title='Transfer Skin Joints......')
            with progressBar:
                for i, boundJnt in enumerate(boundJoints):
                    if progressBar.isCanceled():
                        break

                    if replaceJoints[i] != "MISS":
                        progressBar.setText('Transferring skin joint: %s -> %s' % (boundJnt, replaceJoints[i]))
                        # skinreplacejoints.replaceSkinMatrixJoint(boundJnt, replaceJoints[i])
                        skinreplacejoints.replaceSkinJoint(boundJnt, replaceJoints[i], skin_name=skinNode)

                    progressBar.updateProgress()

    # CALLBACKS
    # ------------------

    # ------------------
    # CONNECTIONS
    # ------------------
    def compactWidgetConnections(self):
        # handles the coPlanar close event
        self.compactWidget.type_cb.currentIndexChanged.connect(self._onTypeChanged)
        self.compactWidget.prefixonCb.stateChanged.connect(self._onTypeChanged)
        self.compactWidget.loadOld.clicked.connect(self.loadOrgMesh)
        self.compactWidget.loadNew.clicked.connect(self.loadNewMesh)
        self.compactWidget.copySkin.clicked.connect(self.copySkin_cmd)
        self.compactWidget.copyBs.clicked.connect(self.copyBs_cmd)
        self.compactWidget.unlockJoints.clicked.connect(self.unlockJoints_cmd)
        self.compactWidget.removeUnusedJoints.clicked.connect(self.remove_cmd)
        self.compactWidget.pruneSmall.clicked.connect(self.pruneWeightOptions)
        self.compactWidget.exportSKinWeights.clicked.connect(self.exporttSkin)
        self.compactWidget.importSKinWeights.clicked.connect(self.importSkin)
        self.compactWidget.copyBsWeight.clicked.connect(self.copyBsWeight_cmd)

        self.compactWidget.loadSource.clicked.connect(self.loadSource_cmd)
        self.compactWidget.loadTarget.clicked.connect(self.loadTarget_cmd)
        self.compactWidget.transfer.clicked.connect(self.transfer_cmd)


class GuiWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc
        """
        super(GuiWidgets, self).__init__(parent=parent)

        self.copySkinCollapsable = elements.CollapsableFrameThin("Batch Copy Skin",
                                                                 contentMargins=(uic.SREG, uic.SREG, uic.SREG, uic.SREG),
                                                                 contentSpacing=uic.SLRG,
                                                                 collapsed=True,
                                                                 parent=parent)

        self.inf1_lb = elements.Label(text="Inf Association 1")
        self.inf1_cb = elements.ComboBoxRegular(parent=self, items=["closestJoint", "closestBone", "oneToOne", "label", "name"])
        self.inf2_lb = elements.Label(text="Inf Association 2")
        self.inf2_cb = elements.ComboBoxRegular(parent=self, items=["closestJoint", "closestBone", "oneToOne", "label", "name"])
        self.type_lb = elements.Label(text="Copy Type")
        self.type_cb = elements.ComboBoxRegular(parent=self, items=["* to *", "One to *", "* to One", "Custom"], setIndex=1)
        # list view
        self.oldView = QtWidgets.QListWidget()
        self.oldView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.oldView.setMinimumHeight(300)
        self.newView = QtWidgets.QListWidget()
        self.newView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.newView.setMinimumHeight(300)

        self.loadOld = elements.styledButton(text="Load Old Mesh")
        self.loadNew = elements.styledButton(text="Load New Mesh")
        self.copySkin = elements.styledButton(text="Copy Skin")
        self.copyBs = elements.styledButton(text="Copy BS")
        self.unlockJoints = elements.styledButton(text="Unlock Joints")
        self.pruneSmallLb = elements.Label(text="Prune Below")
        self.pruneSmallLe = elements.FloatLineEdit(text="0.001")
        self.pruneSmall = elements.styledButton(text="Prune Small Weights")
        self.removeUnusedJoints = elements.styledButton(text="Remove Unused Skin Joints")
        self.copyBsWeight = elements.styledButton(text="Copy BS Weights")
        self.exportBsWeights = elements.styledButton(text="Export BS Weights")
        self.importBsWeights = elements.styledButton(text="Import BS Weights")
        self.exportSKinWeights = elements.styledButton(text="Export Skin Weights", toolTip="Please select one more mesh.")
        self.importSKinWeights = elements.styledButton(text="Import Skin Weights")

        self.transferSkinCollapsable = elements.CollapsableFrameThin("Replace Skin Joints",
                                                                     contentMargins=(uic.SREG, uic.SREG, uic.SREG,
                                                                                     uic.SREG),
                                                                     contentSpacing=uic.SLRG,
                                                                     collapsed=True,
                                                                     parent=parent)
        self.prefixonCb = elements.CheckBox(label="Use Prefix/Suffix", checked=False)
        self.Prefix = elements.StringEdit(label="Prefix",
                                          editPlaceholder="xxx_",
                                          labelRatio=3,
                                          editRatio=6,
                                          parent=parent)
        self.Suffix = elements.StringEdit(label="Suffix",
                                          editPlaceholder="_xxx",
                                          labelRatio=3,
                                          editRatio=6,
                                          parent=parent)

        self.sourceView = QtWidgets.QListWidget(self)
        self.sourceView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.sourceView.setMinimumHeight(300)
        self.targetView = QtWidgets.QListWidget(self)
        self.targetView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.targetView.setMinimumHeight(300)

        self.loadSource = elements.styledButton(text="Load Source")
        self.loadTarget = elements.styledButton(text="Load Target")
        self.transfer = elements.styledButton(text="Transfer")


class CompactLayout(GuiWidgets):
    def __init__(self, parent=None, properties=None, toolsetWidget=None):
        """Adds the layout building the compact version of the GUI:

            default uiMode - 0 is advanced (UI_MODE_COMPACT)

        :param parent: the parent of this widget
        :type parent: qtObject
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: list[dict]
        """
        super(CompactLayout, self).__init__(parent=parent, properties=properties,
                                            toolsetWidget=toolsetWidget)
        # Main Layout ------------------------------------
        contentsLayout = elements.vBoxLayout(self,
                                             margins=(uic.WINSIDEPAD,
                                                      uic.WINBOTPAD,
                                                      uic.WINSIDEPAD,
                                                      uic.WINBOTPAD),
                                             spacing=5)
        copyLayout = elements.vBoxLayout(self)
        inf1_hLayout = elements.hBoxLayout(self)
        inf1_hLayout.addWidget(self.inf1_lb)
        inf1_hLayout.addWidget(self.inf1_cb)

        inf2_hLayout = elements.hBoxLayout(self)
        inf2_hLayout.addWidget(self.inf2_lb)
        inf2_hLayout.addWidget(self.inf2_cb)

        type_hLayout = elements.hBoxLayout(self)
        type_hLayout.addWidget(self.type_lb)
        type_hLayout.addWidget(self.type_cb)

        listLayout = elements.hBoxLayout(self)
        listLayout.addWidget(self.oldView)
        listLayout.addWidget(self.newView)

        loadLayout = elements.hBoxLayout(self)
        loadLayout.addWidget(self.loadOld)
        loadLayout.addWidget(self.loadNew)

        transferLayout = elements.hBoxLayout(self)
        transferLayout.addWidget(self.copySkin)
        transferLayout.addWidget(self.copyBs)

        toolsLayout1 = elements.hBoxLayout(self)
        toolsLayout1.addWidget(self.unlockJoints)
        toolsLayout1.addWidget(self.pruneSmallLb)
        toolsLayout1.addWidget(self.pruneSmallLe)
        toolsLayout1.addWidget(self.pruneSmall)
        toolsLayout1.addWidget(self.removeUnusedJoints)

        bsLayout = elements.hBoxLayout(self)
        bsLayout.addWidget(self.copyBsWeight)
        bsLayout.addWidget(self.exportBsWeights)
        bsLayout.addWidget(self.importBsWeights)

        skinLayout = elements.hBoxLayout(self)
        skinLayout.addWidget(self.exportSKinWeights)
        skinLayout.addWidget(self.importSKinWeights)

        copyLayout.addLayout(inf1_hLayout)
        copyLayout.addLayout(inf2_hLayout)
        copyLayout.addLayout(type_hLayout)
        copyLayout.addLayout(listLayout)
        copyLayout.addLayout(loadLayout)
        copyLayout.addItem(elements.Spacer(40,10))
        copyLayout.addLayout(transferLayout)
        copyLayout.addLayout(toolsLayout1)
        copyLayout.addLayout(bsLayout)
        copyLayout.addItem(skinLayout)

        self.copySkinCollapsable.hiderLayout.addLayout(copyLayout)
        self.copySkinCollapsable.toggled.connect(toolsetWidget.treeWidget.updateTree)

        trMainLayout = elements.vBoxLayout(self)

        prefixLayout = elements.hBoxLayout(self)
        prefixLayout.addWidget(self.Prefix)
        prefixLayout.addWidget(self.Suffix)
        prefixLayout.addWidget(self.prefixonCb)

        jointListLayout = elements.hBoxLayout(self)
        jointListLayout.addWidget(self.sourceView)
        jointListLayout.addWidget(self.targetView)

        loadJointLayout = elements.hBoxLayout(self)
        loadJointLayout.addWidget(self.loadSource)
        loadJointLayout.addWidget(self.loadTarget)

        trMainLayout.addLayout(prefixLayout)
        trMainLayout.addLayout(jointListLayout)
        trMainLayout.addLayout(loadJointLayout)
        trMainLayout.addWidget(self.transfer)

        self.transferSkinCollapsable.hiderLayout.addLayout(trMainLayout)
        self.transferSkinCollapsable.toggled.connect(toolsetWidget.treeWidget.updateTree)

        contentsLayout.addWidget(self.copySkinCollapsable)
        contentsLayout.addWidget(self.transferSkinCollapsable)
        contentsLayout.addStretch(1)
