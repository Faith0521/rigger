#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2019.07.04
#========================================
import os, sys, re, inspect, traceback
from importlib import reload

import maya.cmds as mc
import maya.mel as mel


def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from PySide2.QtWidgets import QAction
        from rxUi.pyside2 import template_ui
        return QtCore, QtGui, QtWidgets, QAction, template_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from PySide6.QtGui import QAction
            from rxUi.pyside6 import template_ui
            return QtCore, QtGui, QtWidgets, QAction, template_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")


QtCore, QtGui, QtWidgets, QAction, template_ui = get_pyside_module()

# core
from rxCore import aboutCrv
from rxCore import aboutLock
from rxCore import aboutFile

# public
import controlTools
import standardBuilds
import importMod
import templateTools
import assetEnv
import assetImport


# reload
# reload(template_ui)
# reload(standardBuilds)
# reload(importMod)
# reload(templateTools)
# reload(aboutFile)
# reload(assetImport)


def undoable(function):
    """A decorator that will make commands undoable in maya"""

    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None

        # noinspection PyBroadException
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print(sys.exc_info()[1])

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode


class Template(QtWidgets.QWidget, template_ui.Ui_TemplateUI):

    def __init__(self):
        super(Template, self).__init__()

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(r'TemplateUI')
        self.ui = template_ui.Ui_TemplateUI()
        self.ui.setupUi(self)

        # Menus
        # create meun object
        self.addPartsMenu = QtWidgets.QMenu(self)
        self.importRigMenu = QtWidgets.QMenu(self)
        # set menu to buttons
        self.ui.addBtn.setMenu(self.addPartsMenu)
        self.ui.loadBtn.setMenu(self.importRigMenu)

        # Initial display
        self.ui.splitter.setStretchFactor(0, 0)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.splitter.setSizes([100, 100])
        self.ui.buildBtn.setEnabled(False)

        self.ui.partsList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        item = QAction(self)
        item.setText('Mirror')
        item.triggered.connect(self.mirrorPart)
        self.ui.partsList.addAction(item)

        item = QAction(self)
        item.setText('Modify')
        item.triggered.connect(self.modifyPart)
        self.ui.partsList.addAction(item)

        item = QAction(self)
        item.setText('Duplicate')
        item.triggered.connect(self.copyPart)
        self.ui.partsList.addAction(item)

        item = QAction(self)
        item.setText('Delete')
        item.triggered.connect(self.deleteParts)
        self.ui.partsList.addAction(item)

        # UI Controls
        self.arg = ''
        self.btn = ''
        self.field = ''
        self.prevMenu = ''
        self.modifyNodes = []
        self.modifyPositions = []
        self.verts = {}
        self.modifySurfs = []
        self.modifySurfPositions = []

        # Signals
        self.ui.buildBtn.clicked.connect(self.buildTemplate)
        self.ui.partsList.itemSelectionChanged.connect(self.createSelectedPartOptionsMenu)
        self.ui.saveBtn.clicked.connect(self.exportTemplate)
        self.ui.partsList.itemDoubleClicked.connect(self.listPartsInScene)

        # Refresh UI
        mc.scriptJob(p=self.objectName(), e=['PreFileNewOrOpened', self.listPartsInScene])

    # List parts in scene
    def listPartsInScene(self):
        self.ui.partsList.clear()
        if not mc.objExists('|template'):
            return

        nodes = mc.listRelatives('|template', c=1)
        if nodes:
            for n in nodes:
                if mc.objExists(n + '.rigPart'):
                    self.ui.partsList.addItem(n)

    # create menu list for add part.
    def createPartsMenu(self):

        self.addPartsMenu.clear()
        # get file and test them
        # path = 'template.py path' + 'change path ui to parts'
        # get mod list from rxParts path

        # os.path.realpath(__file__)  >>>>E:\RosaCmds\AutoRig\BodySys\ui\template.py
        # os.path.dirname(os.path.realpath(__file__)) >>>>E:\RosaCmds\AutoRig\BodySys\ui
        # os.path.join(os.path.dirname(os.path.realpath(__file__)) , 'rxParts') >>>>E:\RosaCmds\AutoRig\BodySys\ui\parts
        path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rxParts'))

        # get items from rxParts file
        parts = []
        # remove __init__ / base file
        for item in [f.split('.')[0] for f in os.listdir(path) if '.py' in f]:
            if not item == '__init__' and not item == 'base' and item not in parts:
                parts.append(item)

        # add parts to menu
        parts.sort()
        parts.insert(0, 'base')

        for part in parts:
            importMod.import_module(part, r=1, v=1)  #import part
            paction = QAction(self)  #create part aciton
            paction.setText(str(part))  #action set text name

            # assign the part command that to create part menu
            paction.triggered.connect(self.createNewPartMenu)  #action connect command self.createNewPartMenu
            self.addPartsMenu.addAction(paction)  #addPartsMenu add this action

            # add separator
            if part == 'base':
                div = QAction(self)
                div.setSeparator(1)
                self.addPartsMenu.addAction(div)

        # Build standard builds list
        div = QAction(self)
        div.setSeparator(1)
        self.addPartsMenu.addAction(div)

        reload(standardBuilds)
        # get standardBuilds's all functions
        all_functions = inspect.getmembers(standardBuilds, inspect.isfunction)

        for f in all_functions:
            label = f[0] + ' Template'

            paction = QAction(self)
            paction.setText(label)
            paction.triggered.connect(self.runStandardBuild)
            paction.triggered.connect(self.listPartsInScene)
            self.addPartsMenu.addAction(paction)

        div = QAction(self)
        div.setSeparator(1)
        self.addPartsMenu.addAction(div)

        # create camera rig
        paction = QAction(self)
        paction.setText('camera Rig')
        #paction.triggered.connect(self.createCameraRig)
        self.addPartsMenu.addAction(paction)

    # Run standard build tempalts
    def runStandardBuild(self):
        # get part from current sender
        part = self.sender().text().replace(' Template', '')
        cmd = 'import {0}; {0}.{1}()'.format('standardBuilds', part)
        exec(cmd)

    # Create new Parts Options Menu.
    def createNewPartMenu(self):
        part = self.sender().text()
        self.createBuildOptions(part)
        self.ui.buildBtn.setEnabled(1)
        # info = templateTools.getModuleInfo(part)
        self.ui.label.setText(part + ' Set')

    def getSelectedAction(self):
        action = self.sender()
        index = self.ui.optionsGrid.indexOf(action)

        if action.objectName() == 'parent_btn':
            sel = mc.ls(sl=1, fl=1)
            if sel:
                sel = mc.ls(sl=1, fl=1)[0].replace('_pos', '')
            else:
                sel = ''

            error = True
            if mc.objExists(sel + '.tag'):
                if 'templateJoint' in mc.getAttr(sel + '.tag'):
                    error = False
            if error:
                mc.confirmDialog(title='Invalid Parent',
                                 icon='critical',
                                 message='''Parent must be part of the skeleton.\n\nSelect a joint or a joint's "pos" handle''',
                                 button=['Ok'])
                return
        else:
            sel = ' '.join(mc.ls(sl=1, fl=1)).strip().replace('_pos', '')

        self.ui.optionsGrid.itemAt(index - 1).widget().setText(sel)
        self.updatePartsArgs()

    # Create Exissting part options Menu.
    def createSelectedPartOptionsMenu(self, part=None, topnode=None):
        if not part and not topnode:
            selection = self.ui.partsList.selectedItems()

            if len(selection) == 1:
                topnode = selection[-1].text()

                if mc.objExists(topnode + '.rigPart'):
                    part = mc.getAttr(topnode + '.rigPart')
                    self.createBuildOptions(part, topnode)
            else:
                self.clearBuildOptions()

    # def comboxColorChange(self):
    #     if self.field.currentIndex() == 0:
    #         self.field.setStyleSheet("color:red;")
    #     elif self.field.currentText() == 1:
    #         self.field.setStyleSheet("color:Green;")

    # Create options menu for new and exisiting parts
    def createBuildOptions(self, part, topnode=None, modify=False):

        # init ui : clear / enable / setText / connect
        if not topnode and not modify:
            self.ui.partsList.clearSelection()

        self.clearBuildOptions()
        self.ui.buildBtn.setEnabled(1)

        self.ui.buildBtn.clicked.disconnect()
        self.ui.buildBtn.clicked.connect(self.buildTemplate)

        # get module info or return if failed
        info = templateTools.getModuleInfo(part)

        if not info:
            return

        args = info[0]
        values = info[1]
        # modulepath = info[2]
        lockArgs = []

        #populate module path and set color
        #basedir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

        # set Hearder Label
        self.ui.label.setText(part + ' Set')

        #if the node exists in the scene try to get the exisitng values
        if mc.objExists('{0}.rigPart'.format(topnode)):
            values = [templateTools.getArgs(topnode)[arg] for arg in args]  # get label's value on topnode.
            lockArgs = eval(mc.getAttr(topnode + '.rigPartLockArgs'))  # get unable value on topnode.

            if not modify:
                self.ui.label.setText(topnode + ' Set')
                self.ui.buildBtn.setEnabled(0)

        # build widgets based on value type
        if values:
            for i in range(len(values)):

                arg = args[i]
                value = values[i]

                # create the label
                self.arg = QtWidgets.QLabel(arg)
                self.ui.optionsGrid.addWidget(self.arg, i, 0)

                # create string fields
                if type(value) is str or type(value) is bytes:
                    self.btn = None

                    # speciel SIDE case
                    if arg == 'side':
                        self.field = QtWidgets.QComboBox(self)
                        self.field.setObjectName(arg + '_field')
                        self.field.addItems(['cn', 'lf', 'rt'])
                        self.ui.optionsGrid.addWidget(self.field, i, 1)
                        self.field.setStyleSheet('background-color:rgb(48,48,48)')

                        if value == 'cn':
                            self.field.setCurrentIndex(0)
                        elif value == 'lf':
                            self.field.setCurrentIndex(1)
                        elif value == 'rt':
                            self.field.setCurrentIndex(2)
                    else:
                        self.field = QtWidgets.QLineEdit(self)
                        self.field.setObjectName(arg + '_field')
                        self.field.setText(value)
                        self.field.setToolTip('Input String')
                        self.ui.optionsGrid.addWidget(self.field, i, 1)

                    if arg == 'parent':
                        # create get button
                        self.btn = QtWidgets.QPushButton('Get')
                        self.btn.setObjectName(arg + '_btn')
                        self.btn.setMinimumWidth(60)
                        self.btn.setMaximumHeight(19)
                        self.ui.optionsGrid.addWidget(self.btn, i, 2)
                        self.btn.clicked.connect(self.getSelectedAction)

                        #self.btn.clicked.connect(self.getSelectedAction)
                        if topnode:
                            if arg in lockArgs and not modify:
                                self.btn.setEnabled(0)
                                self.btn.setStyleSheet('background-color:#4b4b4b')

                # list fields
                elif type(value) is list:
                    self.field = QtWidgets.QLineEdit(self)
                    self.field.setObjectName(arg + '_field')
                    self.field.setText(' '.join(value))
                    self.field.setToolTip('Input List - seperated by spaces')
                    self.ui.optionsGrid.addWidget(self.field, i, 1)

                    # create get button
                    self.btn = QtWidgets.QPushButton('Get')
                    self.btn.setObjectName(arg + '_btn')
                    self.btn.setMinimumWidth(60)
                    self.btn.setMaximumHeight(19)
                    self.ui.optionsGrid.addWidget(self.btn, i, 2)
                    self.btn.clicked.connect(self.getSelectedAction)

                    if topnode:
                        if arg in lockArgs and not modify:
                            self.btn.setEnabled(0)
                            self.btn.setStyleSheet('background-color:#4b4b4b')

                elif type(value) is int or type(value) is float:
                    self.field = QtWidgets.QLineEdit(self)
                    self.field.setObjectName(arg + '_field')
                    self.field.setToolTip('Input Number')

                    if type(value) is int:
                        self.field.setValidator(QtGui.QIntValidator())
                    else:
                        self.field.setValidator(QtGui.QDoubleValidator())

                    self.field.setText('{0}'.format(value))
                    self.ui.optionsGrid.addWidget(self.field, i, 1)

                elif type(value) is bool:
                    self.field = QtWidgets.QComboBox(self)
                    self.field.setObjectName(arg + '_field')
                    self.field.addItems(['No', 'Yes'])
                    self.field.setStyleSheet('background-color:rgb(48,48,48)')
                    self.field.setCurrentIndex(0)
                    self.ui.optionsGrid.addWidget(self.field, i, 1)

                    if value:
                        self.field.setCurrentIndex(1)

                self.ui.optionsGrid.setRowStretch(self.ui.optionsGrid.rowCount(), 1)

                # If top node exists then this is in edit mode.
                if topnode and not modify:
                    # Lock args
                    if arg in lockArgs:
                        self.field.setEnabled(0)

                    # Set update args slot.
                    if type(self.field) is QtWidgets.QLineEdit:
                        self.field.returnPressed.connect(self.updatePartsArgs)

                    if type(self.field) is QtWidgets.QComboBox:
                        self.field.currentIndexChanged.connect(self.updatePartsArgs)
                    mc.select(topnode)

    # Clear Build Options
    def clearBuildOptions(self):
        # clear UI
        self.ui.label.setText('Part Set')
        # use reversed : delete ui widget from 10~1
        for i in reversed(range(self.ui.optionsGrid.count())):
            self.ui.optionsGrid.itemAt(i).widget().deleteLater()
            self.ui.optionsGrid.removeItem(self.ui.optionsGrid.itemAt(i))
        self.ui.buildBtn.setEnabled(0)

    # Get options from UI
    def getCurrentOptions(self):

        options = {}
        for i in range(self.ui.optionsGrid.count()):

            widget = self.ui.optionsGrid.itemAt(i).widget()
            if re.search('QtWidgets.QLabel', str(widget)):

                label = widget.text()
                value = None
                vwidget = self.ui.optionsGrid.itemAt(i + 1).widget()

                if re.search('QtWidgets.QLineEdit', str(vwidget)):

                    value = vwidget.text()
                    if vwidget.toolTip() == 'Input List - seperated by spaces':
                        value = vwidget.text().strip().split(' ')

                    if vwidget.toolTip() == 'Input Number':
                        value = vwidget.text()
                        if r'.' in value:
                            value = float(value)
                        else:
                            value = int(value)

                elif re.search('QtWidgets.QComboBox', str(vwidget)):

                    value = vwidget.currentText()
                    if value == 'Yes':
                        value = True

                    elif value == 'No':
                        value = False

                options[label] = value
        return options

    # Build the actioa; part
    @undoable
    def buildTemplate(self):

        # if not part args, retrun.
        part = self.ui.label.text().split(' ')[0]  # 'base Part' == 'base'
        if part == 'Part':
            return

        # system must have a base template.
        if not part == 'base' and not mc.ls('base'):
            base = importMod.import_module('base')
            base.template()

        mod = importMod.import_module(part, r=1)  # import part
        options = self.getCurrentOptions()  # get part data

        # noinspection PyBroadException
        try:
            mod.template(**options)  # create part template by data
        except:
            msgs = traceback.format_exc()
            print(msgs)
            return
        templateTools.resolveTempPrefix()  # set part template prefix

        self.clearBuildOptions()  # clean options ui
        self.listPartsInScene()  # list part template in scene

    @undoable
    def updatePartsArgs(self, *args):

        currentSel = mc.ls(sl=1)

        if not self.ui.partsList.selectedItems():
            return

        topnode = mc.ls(self.ui.partsList.selectedItems()[-1].text())[0]

        if mc.objExists(topnode + '.rigPart'):

            part = mc.getAttr(topnode + '.rigPart')
            options = self.getCurrentOptions()

            oldPrefix = templateTools.getArgs(topnode, 'prefix')
            oldSide = templateTools.getArgs(topnode, 'side')
            oldPrefix = templateTools.getPrefix(oldSide, oldPrefix)

            # noinspection PyBroadException
            try:
                lockArgs = eval(mc.getAttr(topnode + '.rigPartLockArgs'))
            except:
                # maybe need delete
                lockArgs = mc.getAttr(topnode + '.rigPartLockArgs').split('%')

            # Rename nodes
            newPrefix = options.get('prefix', '')
            newSide = options.get('side', '')
            newPrefix = templateTools.getPrefix(newSide, newPrefix)

            if newPrefix != oldPrefix:

                if oldPrefix:
                    oldPrefix = oldPrefix[:-1] + oldPrefix[-1].replace('_', '')

                if newPrefix:
                    newPrefix = newPrefix[:-1] + newPrefix[-1].replace('_', '')

                mc.select(topnode, hi=1)
                nodes = mc.ls(sl=1, l=1)
                newnames = []

                for i in range(len(nodes)):
                    newname = ''
                    node = mc.ls(sl=1)[i]
                    if oldPrefix == '':
                        newname = node.split('|')[-1].replace(oldPrefix, newPrefix + '_', 1)
                    elif oldPrefix == oldSide:
                        newname = node.split('|')[-1].replace(oldPrefix + '_', newPrefix + '_', 1)
                    elif node.startswith(oldPrefix + '_'):
                        newname = node.split('|')[-1].replace(oldPrefix + '_', newPrefix + '_', 1)
                    # e = newname.replace('__','_')
                    print(newname)
                    newname = newname[0].replace('_', '') + newname[1:]

                    if '_lf_' in newname:
                        newname = 'lf_' + newname.replace('_lf_', '_')
                    if '_rt_' in newname:
                        newname = 'rt_' + newname.replace('_rt_', '_')

                    if not mc.objExists(newname):
                        newnames.append(newname)

                if len(nodes) != len(newnames):
                    mc.warning('New options would cause clashing names.. Use a different prefix!')
                    self.createSelectedPartOptionsMenu()
                    return

                mc.select(nodes)
                for i in range(len(nodes)):
                    node = mc.ls(sl=1)[i]
                    if mc.objExists(node):
                        mc.rename(node, newnames[i])

                topnode = newnames[0]
                self.ui.partsList.selectedItems()[-1].setText(topnode)

            templateTools.recordArgs(topnode, part, options, lockArgs)
            self.createSelectedPartOptionsMenu()

        if currentSel:
            mc.select(currentSel)

    @undoable
    # Delete RigPart From List
    def deleteParts(self):
        sel = self.ui.partsList.selectedItems()
        for s in sel:
            mc.delete(s.text())

        self.clearBuildOptions()
        self.listPartsInScene()

    # Modify RigPart From List
    def modifyPart(self):

        # NOTE: I create some global variable in this function that use to rebuild rig template.
        # self.modifyNodes / self.modifyPositions / self.verts / self.modifySurfs / self.modifySurfPositions

        sel = self.ui.partsList.selectedItems()
        if not sel:
            return

        topnode = self.ui.partsList.selectedItems()[0].text()
        if not mc.objExists(topnode):
            return

        # Prep UI
        part = mc.getAttr(topnode + '.rigPart')
        self.createBuildOptions(part, topnode=topnode, modify=True)

        # Save positins
        # Get all the node in part template
        self.modifyNodes = [topnode] + mc.listRelatives(topnode + 'Ctrls', ad=1, type='joint')
        self.modifyNodes += mc.listRelatives(topnode + 'Ctrls', ad=1, type='transform')
        self.modifyPositions = []

        hi = mc.listRelatives(topnode, ad=1)

        # self.verts = {}
        # self.modifySurfs = []
        # self.modifySurfPositions = []

        # Save temp surface before rebuild part
        for h in hi:
            if mc.objExists(h + '.tempSurf'):
                verts = mc.ls(h + '.cv[*]', fl=1)
                for v in verts:
                    self.verts[v] = mc.xform(v, q=1, ws=1, t=1)
                if h in self.modifyNodes:
                    self.modifyNodes.remove(h)
                    t = mc.xform(h, q=1, ws=1, t=1)
                    r = mc.xform(h, q=1, ws=1, ro=1)
                    s = mc.xform(h, q=1, r=1, s=1)
                    self.modifySurfs.append(h)
                    self.modifySurfPositions.append([t, r, s])

        # Save template node: name / transform position before rebuild part
        for node in self.modifyNodes:
            t = mc.xform(node, q=1, ws=1, t=1)
            r = mc.xform(node, q=1, ws=1, ro=1)
            s = mc.xform(node, q=1, r=1, s=1)
            self.modifyPositions.append([t, r, s])

        # change buildBtn command
        self.ui.buildBtn.clicked.disconnect()
        self.ui.buildBtn.clicked.connect(self.rebuildTemplate)
        self.ui.buildBtn.setText('Rebuild Part')

    # Rebuild modified part
    @undoable
    def rebuildTemplate(self):
        self.ui.buildBtn.clicked.disconnect()
        self.ui.buildBtn.clicked.connect(self.buildTemplate)
        self.ui.buildBtn.setText('Build Part')

        # noinspection PyBroadException
        try:
            nodes = mc.ls(self.modifyNodes)
            if nodes:
                mc.delete(nodes)
        except:
            pass

        self.buildTemplate()  #build

        if mc.objExists(self.modifyNodes[0] + ".tagIfRestorePos") and mc.getAttr(self.modifyNodes[0] + ".tagIfRestorePos"):
            return

        modifyNodes = self.modifyNodes * 8
        modifyPositions = self.modifyPositions * 8

        modifySurfs = self.modifySurfs
        modifySurfPositions = self.modifySurfPositions

        tmp = mc.createNode('transform')
        tcons = []
        for i in range(len(modifySurfs)):
            if mc.objExists(modifySurfs[i]):
                t = modifySurfPositions[i][0]
                r = modifySurfPositions[i][1]
                s = modifySurfPositions[i][2]

                mc.xform(modifySurfs[i], ws=1, t=t)
                mc.xform(modifySurfs[i], ws=1, ro=r)
                mc.xform(modifySurfs[i], ws=1, s=s)
                tcons.extend(mc.parentConstraint(tmp, modifySurfs[i], mo=1))
                tcons.extend(mc.scaleConstraint(tmp, modifySurfs[i], mo=1))

        for v, pos, in self.verts.items():
            mc.xform(v, ws=1, t=pos)

        # restore tempalte nodes position
        for i in range(len(modifyNodes)):
            if mc.objExists(modifyNodes[i]):
                t = modifyPositions[i][0]
                r = modifyPositions[i][1]
                s = modifyPositions[i][2]

                mc.xform(modifyNodes[i], ws=1, t=t)
                mc.xform(modifyNodes[i], ws=1, ro=r)
                mc.xform(modifyNodes[i], ws=1, s=s)
            else:
                print(modifyNodes[i])

        # clean
        mc.delete(tmp)
        # refresh UI
        self.clearBuildOptions()
        self.listPartsInScene()

    @undoable
    def mirrorPart(self):
        topnodes = [i.text() for i in self.ui.partsList.selectedItems()]  # get part name
        for topnode in topnodes:
            part = mc.getAttr(topnode + '.rigPart')

            # noinspection PyBroadException
            try:
                mod = importMod.import_module(part)
                mod.mirror()
                continue

            except:
                side = templateTools.getArgs(topnode, 'side')
                if side == 'cn' or not side:
                    mc.warning('Part must be either left or right sided. Skipping..')
                    continue

            # Get args and build mirror arg
            mside = ''
            if side == 'lf':
                mside = 'rt'
            elif side == 'rt':
                mside = 'lf'

            # If can not found mside parts, build it by current part args.
            if not mc.objExists(topnode.replace(side, mside, 1)):
                argStr = mc.getAttr(topnode + '.rigPartArgs')
                margs = eval(argStr.replace(side, mside))

                mod = importMod.import_module(part)
                mod.template(**margs)
                templateTools.resolveTempPrefix()

            # Mirror top node
            mtopnode = topnode.replace(side, mside, 1)

            axis = ['tx', 'ty', 'tz']
            axisnodes = []
            for a in axis:
                axisnodes.append(mc.createNode('transform', n=topnode + a, p=topnode))
                mc.setAttr(axisnodes[-1] + '.' + a, 1)

            piv = mc.createNode('transform', n='piv', p=topnode)
            tmp = mc.createNode('transform', n='tmp')
            mc.parent(axisnodes, piv, tmp)
            mc.setAttr(tmp + '.sx', -1)
            mc.parent(piv, w=1)
            mc.setAttr(piv + '.s', 1, 1, 1)

            mc.aimConstraint(axisnodes[1], piv, aim=[0, 1, 0], u=[0, 0, 1], wut='object', wuo=axisnodes[2])

            mc.xform(mtopnode, ws=1, t=mc.xform(piv, q=1, ws=1, t=1))
            mc.xform(mtopnode, ws=1, ro=mc.xform(piv, q=1, ws=1, ro=1))
            mc.xform(mtopnode, a=1, s=mc.xform(topnode, q=1, r=1, s=1))

            mc.delete(tmp, piv)

            # mirror surfaces
            hi = mc.listRelatives(topnode, ad=1)
            surfs = []
            for h in hi:
                if mc.objExists(h + '.tempSurf'):
                    surfs.append(h)

            for surf in surfs:
                msurf = surf.replace(side, mside)
                if not mc.objExists(surf) and not mc.objExists(msurf):
                    continue

                mc.delete(mc.parentConstraint(surf, msurf))
                mc.delete(mc.scaleConstraint(surf, msurf))

                verts = mc.ls(surf + '.cv[*]', fl=1)
                for v in verts:
                    mv = v.replace(surf, msurf)
                    mc.xform(mv, ws=1, t=mc.xform(v, q=1, ws=1, t=1))

                par = mc.listRelatives(msurf, p=1)[0]
                tmp = mc.createNode('transform')
                mc.parent(msurf, tmp)
                mc.setAttr(tmp + '.sx', -1)
                mc.parent(msurf, par)

            # Mirror all pos joints
            mnodes = []
            nodes = mc.listRelatives(topnode + 'Ctrls', ad=1, type='joint')
            tmp = mc.createNode('joint')

            for node in nodes:
                tj = mc.duplicate(node, n='tmp' + node, po=1)
                aboutLock.unlock(tj)
                mc.parent(tj, tmp)
                mnodes.append(tj[0].replace('tmp' + side, 'tmp' + mside))

            mtmp = mc.mirrorJoint(tmp, mirrorBehavior=1, mirrorYZ=1, searchReplace=['tmp' + side, 'tmp' + mside])[0]
            mc.delete(tmp)

            # Snap right side nodes.
            # why the code *6, because the pos jnt had different hierarchy
            for tnode in mnodes * 6:
                mnode = tnode.replace('tmp' + mside, mside, 1)
                if mc.objExists(topnode) and mc.objExists(mtopnode):
                    mc.xform(mnode, ws=1, t=mc.xform(tnode, q=1, ws=1, t=1))
                    mc.xform(mnode, ws=1, ro=mc.xform(tnode, q=1, ws=1, ro=1))
                    mc.xform(mnode, a=1, s=mc.xform(tnode, q=1, r=1, s=1))

            # set mtopnode attr value
            if mc.objExists(topnode) and mc.objExists(mtopnode):
                attrs = mc.listAttr(topnode, ud=1, k=1)
                if 'ctrlDisplay' in attrs:
                    attrs.remove('ctrlDisplay')
                if 'jointDisplay' in attrs:
                    attrs.remove('jointDisplay')
                for a in attrs:
                    mc.setAttr(mtopnode + '.' + a, mc.getAttr(topnode + '.' + a))

            mc.delete(mtmp)

            # Mirror Ctrls
            shapes = mc.listRelatives(topnode + 'Ctrls', ad=1, type='nurbsCurve')
            if shapes:
                ctrls = []
                for s in shapes:
                    ctrls.append(mc.listRelatives(s, p=1)[0])

                for ctrl in ctrls:
                    mctrl = ctrl.replace(side, mside, 1)
                    if mc.objExists(ctrl) and mc.objExists(mctrl):
                        # noinspection PyBroadException
                        try:
                            if ctrl.startswith(side + '_') or ctrl.startswith(mside + '_'):
                                aboutCrv.mirrorCrvShape(ctrl, axisMirrors='x', search=side, replace=mside)
                        except:
                            pass

        mc.select(cl=1)

        self.clearBuildOptions()
        self.listPartsInScene()

    @undoable
    def copyPart(self):
        mel.eval('cycleCheck -e off')
        topnodes = [i.text() for i in self.ui.partsList.selectedItems()]
        if not topnodes:
            return

        topnode = topnodes[0]

        result = mc.promptDialog(
            title='Set Prefix',
            message='Add a new prefix to avoid duplicate names!\n\nNew prefix:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            dismissString='Cancel',
            text='')

        if result == 'Cancel':
            return

        text = mc.promptDialog(query=1, text=1).strip().replace(' ', '_')
        tokens = text.strip().split('_')
        text = tokens[0]
        for t in tokens[1:]:
            if t:
                text += t[0].capitalize() + t[1:]

        side = templateTools.getArgs(topnode, 'side')
        prefix = templateTools.getArgs(topnode, 'prefix')
        part = mc.getAttr(topnode + '.rigPart')
        argStr = mc.getAttr(topnode + '.rigPartArgs ')

        if not side:
            side = ''
        newprefix = text

        # Replace sides arg
        margs = eval(argStr)
        margs['prefix'] = newprefix

        mod = importMod.import_module(part)

        # noinspection PyBroadException
        try:
            mod.template(**margs)
            templateTools.resolveTempPrefix()
        except:
            mc.warning('Part cannot be duplicated.. ')
            return

        mtopnode = mc.ls(sl=1)[0]
        newprefix = templateTools.getArgs(mtopnode, 'prefix')

        prefix = templateTools.getPrefix(side, prefix)
        mprefix = templateTools.getPrefix(side, newprefix)

        if prefix.endswith('_'):
            prefix = prefix[:-1]

        if mprefix.endswith('_'):
            mprefix = mprefix[:-1]

        hi = mc.listRelatives(topnode, ad=1)
        surfs = []
        for h in hi:
            if mc.objExists(h + '.tempSurf'):
                surfs.append(h)

        for surf in surfs:
            msurf = surf.replace(prefix, mprefix)
            if not mc.objExists(surf) and not mc.objExists(msurf):
                continue

            mc.delete(mc.parentConstraint(surf, msurf))
            mc.delete(mc.scaleConstraint(surf, msurf))

            verts = mc.ls(surf + '.cv[*]', fl=1)
            for v in verts:
                mv = v.replace(surf, msurf)
                mc.xform(mv, ws=1, t=mc.xform(v, q=1, ws=1, t=1))

        # Snap joints and ctrls
        nodes = [topnode] + mc.listRelatives(topnode, ad=1, type='joint')
        for node in nodes * 6:
            mnode = node.replace(prefix, mprefix, 1)
            if mc.objExists(node) and mc.objExists(mnode):
                mc.xform(mnode, ws=1, t=mc.xform(node, q=1, ws=1, t=1))
                mc.xform(mnode, ws=1, ro=mc.xform(node, q=1, ws=1, ro=1))
                mc.xform(mnode, a=1, s=mc.xform(node, q=1, r=1, s=1))

        if mc.objExists(topnode) and mc.objExists(mtopnode):
            attrs = mc.listAttr(topnode, ud=1, k=1)
            if 'ctrlDisplay' in attrs:
                attrs.remove('ctrlDisplay')

            if 'jointDisplay' in attrs:
                attrs.remove('jointDisplay')
            for a in attrs:
                mc.setAttr(mtopnode + '.' + a, mc.getAttr(topnode + '.' + a))

        # Mirror Ctrls
        ctrls = []
        shapes = mc.listRelatives(topnode + 'Ctrls', ad=1, type='nurbsCurve')
        if shapes:
            for s in shapes:
                ctrls.append(mc.listRelatives(s, p=1)[0])

        for ctrl in ctrls:
            mctrl = ctrl.replace(prefix, mprefix, 1)
            if mc.objExists(ctrl) and mc.objExists(mctrl) and not ctrl == mctrl:
                # noinspection PyBroadException
                try:
                    controlTools.copyShape([ctrl, mctrl], 1)
                except:
                    pass

        #mel.eval('cycleCheck -e on')
        mc.select(cl=1)

        self.clearBuildOptions()
        self.listPartsInScene()

    # List sabved template file versions
    def listTemplateVersions(self):
        self.importRigMenu.clear()
        if not assetEnv.getpath():
            return

        items = []
        path = os.path.join(assetEnv.getpath(), 'build', 'template')

        if os.path.isdir(path):
            items = [f for f in os.listdir(path) if re.search('v[0-9][0-9][0-9].', f)]
            items.sort()
            items.reverse()

        paction = QAction(self)
        paction.setText('Import Model')
        paction.triggered.connect(lambda: assetImport.model())
        self.importRigMenu.addAction(paction)

        div = QAction(self)
        div.setSeparator(1)
        self.importRigMenu.addAction(div)

        maxitems = 20
        for item in items[:maxitems]:
            paction = QAction(self)
            paction.setText(str(item))
            paction.triggered.connect(self.importTemplate)
            self.importRigMenu.addAction(paction)

        if len(items) > maxitems:
            div = QAction(self)
            div.setSeparator(1)
            self.importRigMenu.addAction(div)

            self.prevMenu = QtWidgets.QMenu('Older Versions')
            self.importRigMenu.addMenu(self.prevMenu)

            for item in items[maxitems:]:
                paction = QAction(self)
                paction.setText(str(item))
                paction.triggered.connect(self.importTemplate)
                self.prevMenu.addAction(paction)

    # import template file
    def importTemplate(self):
        filename = self.sender().text()
        path = os.path.join(assetEnv.getpath(), 'build', 'template', filename)

        if not mc.file(path, q=1, ex=1):
            mc.warning("File doesn't exist: " + path)
            return

        if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
            return

        mc.file(path, i=1)
        if mc.objExists('rigBuild_currentStep'):
            mc.delete('rigBuild_currentStep')

        self.listPartsInScene()
        print('# Imported: ' + path)

    # Export template file
    def exportTemplate(self):
        if not mc.objExists('|template'):
            mc.warning('No template exists to export!')
            return

        if not templateTools.validateOptions():
            return

        asset = assetEnv.getasset()
        path = os.path.join(assetEnv.getpath(), 'build', 'template')

        # check for proper variables or retun
        if not asset or not path:
            mc.warning('You must set all your asset to export a template!')
            return

        # get file name and export
        newfile = aboutFile.getNewTemplateVersion(path, asset, 'template')

        mel.eval('source "cleanUpScene.mel";')
        mel.eval('deleteUnknownNodes();')

        if mc.objExists('rigBuild_currentStep'):
            mc.delete('rigBuild_currentStep')

        mc.select('|template', hi=1)
        mc.file(newfile, options='v=0', type='mayaAscii', pr=1, es=1, f=1)
        templateTools.writePartsFile(path)
        mc.select('|template')

        print('Exported Asset Version: ' + newfile)
        self.listTemplateVersions()


'''
    # Enable disable buttons
    def setEnabled(self, btn, enable=True):
        if enable :
            st = ''
            {
            background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:1 #0072bc, stop:0 #0054a6);
            border-radius: 0px;


            QPushButton:pressed
            {
            background-color: #1d1d1d;
            border-radius: 0px;
            }''
        else:
            st = ''
            background-color: #4b4b4b;
            border-radius: 0px;

        #btn.setStyleSheet(st)
        btn.setEnabled(enable)

# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\template_ui.py .\templateUI.ui
# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\controlTools_ui.py .\controlToolsUI.ui
'''
