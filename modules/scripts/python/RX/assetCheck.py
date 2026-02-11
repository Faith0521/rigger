#!/usr/bin/python
# -*- coding: utf-8 -*-
from importlib import reload

def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from PySide2.QtWidgets import QAction
        from rxUi.pyside2 import assetCheck_ui
        return QtCore, QtGui, QtWidgets, QAction, assetCheck_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from PySide6.QtGui import QAction
            from rxUi.pyside6 import assetCheck_ui
            return QtCore, QtGui, QtWidgets, QAction, assetCheck_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets, QAction, assetCheck_ui= get_pyside_module()

import os
import maya.cmds as mc
import maya.mel as mel

import assetEnv
import modelChecks
import rigChecks
from rxCore import aboutFile

# Rig Check UI 
class AssetCheck(QtWidgets.QWidget, assetCheck_ui.Ui_assetCheckUI):

    def __init__(self, uiName='assetCheckUI', parent=None, publish=1):
        # UI modify
        super(AssetCheck, self).__init__()
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(uiName)
        self.ui = assetCheck_ui.Ui_assetCheckUI()
        self.ui.setupUi(self)

        # Initiasl settings
        self.ui.checkTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.fixBtn.setText('Auto Fix Selected')

        if not 'RIGCHECK_MODELHI' in os.environ.keys():
            os.environ['RIGCHECK_MODELHI'] = ''
        os.environ['RIGCHECK_CTRLS'] = ''
        os.environ['RIGCHECK_TOPNODE'] = ''

        if mc.window('checkReportUI', q=1, ex=1):
            mc.deleteUI('checkReportUI')

        # Menus
        # skip current item
        self.ui.checkTree.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        item = QAction(self)
        item.setText('Skip This Check')
        item.triggered.connect(self.setSkipped)
        self.ui.checkTree.addAction(item)

        # Signals
        self.ui.checkTree.itemDoubleClicked.connect(self.listCheckItem)
        self.ui.checkBtn.clicked.connect(lambda :self.runCheck(index=None))
        self.ui.fixBtn.clicked.connect(self.runFix)

        if not publish:
            self.ui.ExportBtn.hide()
        else:
            self.ui.ExportBtn.setEnabled(1)
            self.ui.ExportBtn.clicked.connect(self.publishFile)

        # refresh check menu / check list.
        self.reloadChecks()

    # --------------------------------------------------------------------------------------------------------------
    @staticmethod
    def checklist():
        # DATA - set( Label, Function, Fix Function)
        # Difference rig type has different check list.
        checklist =  {'model': [
                ('Check for referenced nodes', modelChecks.refNodes,),
                ('Check for namespaces', modelChecks.namespaces),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for single model hierarchy', modelChecks.singleHi),
                ('Check for bad model names', modelChecks.checkBadShapes, modelChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', modelChecks.layers, 'Remove Layers'),
                ('Check all history', modelChecks.deleteCh, 'Remove History')],

            'rig': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

            'gameRig': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

            'mocapRig': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

            'other': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)]

                }
        return checklist

    def setSkipped(self):
        item = self.ui.checkTree.selectedItems()
        if not item:
            return
        # item [0] [1] [2]
        item[0].setText(1, 'SKIPPING')
        item[0].setForeground(1, QtGui.QColor('orange'))

    def setCheckType(self, text=None):
        if not text:
            text = self.sender().text()
        self.ui.checkTypeBtn.setText(text)
        self.ui.ExportBtn.setText( 'Publish {0}'.format(text) )

    def listCheckMenu(self):
        checklist = self.checklist()
        checkTypeMenu = QtWidgets.QMenu(self)
        self.ui.checkTypeBtn.setMenu(checkTypeMenu)

        for ctype in checklist.keys():
            item = QAction(self)
            item.setText(ctype)
            item.triggered.connect(self.setCheckType)
            item.triggered.connect(self.listCheckItem)
            checkTypeMenu.addAction(item)

    def listCheckItem(self):
        self.ui.checkTree.clear()
        checklist = self.checklist()
        checkTypes = self.ui.checkTypeBtn.text()
        checkList = checklist[checkTypes]

        for i in range( len(checkList) ):
            label = checkList[i][0]
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, label)
            item.setForeground(1, QtGui.QColor('lighGray'))
            item.setSizeHint(0, QtCore.QSize(18, 23))
            self.ui.checkTree.addTopLevelItem(item)

    def reloadChecks(self):
        self.listCheckMenu()
        self.listCheckItem()

    def runCheck(self, index=None):
        checkTypes = self.ui.checkTypeBtn.text()
        checklist = self.checklist()
        itemlist = checklist[checkTypes]
        currentSel = mc.ls(sl=1)

        if index is None:
            index = range(len(itemlist))
        else:
            index = [index]

        somefailed = False

        print ('\n\n#----------------------------------------------------------------#')
        print ('# ASSET CHECK REPORT')
        print ('#----------------------------------------------------------------#')

        for idx in index:
            #print(idx)
            mc.select(currentSel)
            item = self.ui.checkTree.topLevelItem(idx)

            if item.text(1) == 'SKIPPING':
                continue

            result = itemlist[idx][1]()
            item.setText(1, '...')

            if result:
                item.setForeground(1, QtGui.QColor('lime'))
                item.setText(1, 'PASS')

            elif result == 'PENDING':
                item.setText(1, 'PENDING')
                return

            else:
                item.setForeground(1, QtGui.QColor('red'))
                item.setText(1, 'FAIL')
                somefailed = True
                print ('\n\n#------------------------------------------------------------#')
                print ('FAILED CHECK: "{0}"\n'.format(itemlist[idx][0]))
                print ('{0}'.format(result))

                if len(itemlist[idx]) > 2:
                    print ('\nAuto fix is available.')
                else:
                    print ('\nManual fix is required.')

            QtCore.QCoreApplication.processEvents()
            mc.refresh()

        if somefailed:
            print ('\n')
            mc.warning('Some checks failed.. See script editor for details.')
        else:
            print ('\nEverything passed.. Go forth and publish!')


    def runFix(self):
        item = self.ui.checkTree.selectedItems()
        if not item:
            return

        idx = self.ui.checkTree.indexOfTopLevelItem(item[0])

        if len(self.checklist[idx]) > 2 and item[0].text(1) == 'FAIL':
            self.checklist[idx][2]()
            self.runCheck(idx)

    def publishFile(self):
        asset = assetEnv.getasset()

        fileTypes = ['model']
        fileTypes.extend(assetEnv.getjsoninfo('rigTypes'))
        currentType = self.ui.checkTypeBtn.text()
        if not currentType in fileTypes:
            mc.confirmDialog(title='Warning', icn='warning', b='Failed', m='{0} has no "{1}" type in env !'.format(asset, currentType))
            return

        path = os.path.join(assetEnv.getpath(), currentType)
        if not os.path.isdir(path):
            os.makedirs(path)

        newfile = aboutFile.getNewTemplateVersion(path, asset, currentType)

        mel.eval('source "cleanUpScene.mel";')
        mel.eval('deleteUnknownNodes();')

        if mc.objExists('rigBuild_currentStep'):
            mc.delete('rigBuild_currentStep')

        # select all top node.
        mc.select('|*', hi=1)
        mc.file(newfile, options='v=0', type='mayaAscii', pr=1, es=1, f=1)
        mc.select(cl=1)

        print ('Publish {0} file: {1}'.format(currentType, newfile))


