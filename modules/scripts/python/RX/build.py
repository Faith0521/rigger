#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2020.02.17
#========================================
from importlib import reload

def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from PySide2.QtWidgets import QAction
        from rxUi.pyside2 import build_ui
        return QtCore, QtGui, QtWidgets, QAction, build_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from PySide6.QtGui import QAction
            from rxUi.pyside6 import build_ui
            return QtCore, QtGui, QtWidgets, QAction, build_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets, QAction, build_ui= get_pyside_module()


import maya.cmds as mc
import maya.mel as mel

import traceback
import importlib
import sys
import os
import re

from rxCore import aboutFile
import importMod
import assetEnv

# reload(importMod)
# reload(build_ui)
# reload(assetEnv)

class Build(QtWidgets.QWidget):

    def __init__(self):
        super(Build, self).__init__()

        #self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('buildUI')

        self.ui = build_ui.Ui_buildUI()
        self.ui.setupUi(self)

        # Menus
        self.ui.buildList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # button click menu
        self.importRigMenu = QtWidgets.QMenu(self)
        self.ui.loadBtn_2.setMenu(self.importRigMenu)

        self.rigTypeMenu = QtWidgets.QMenu(self)
        self.ui.rigTypeBtn.setMenu(self.rigTypeMenu)

        # right mouse menu
        item = QAction(self)
        item.setText('Load This Step')
        item.triggered.connect (self.loadCache)
        self.ui.buildList.addAction(item)

        item = QAction(self)
        item.setText('Rebuild This Step')
        item.triggered.connect (self.rebuildSelected)
        self.ui.buildList.addAction(item)

        item = QAction(self)
        item.setText('Build Only This Step')
        item.triggered.connect (self.buildSelected)
        self.ui.buildList.addAction(item)

        self.editItem = QAction(self)
        self.editItem.setText('Edit Asset Custom File')
        self.editItem.triggered.connect (self.editCustomFile)
        self.ui.buildList.addAction(self.editItem)
        self.editItem.setEnabled(0)

        # Initial display
        btns = [
            self.ui.rigTypeBtn,
            self.ui.loadBtn_2,
            self.ui.saveBtn_2]

        for b in btns:
            b.setMinimumHeight(25)
            b.setMaximumHeight(25)

        # signals
        self.ui.buildList.itemSelectionChanged.connect(self.enableEditMenu)
        self.ui.nextBtn.clicked.connect(self.buildNext)
        self.ui.selBtn.clicked.connect(lambda: self.buildBatch(1))
        self.ui.buildBtn.clicked.connect(self.buildBatch)
        self.ui.saveBtn_2.clicked.connect(self.saveWorkFile)
        self.ui.buildList.itemDoubleClicked.connect(self.newsceneReload)

        # When the maya open a file or create new sence, it will be clear the rig system ui data.
        mc.scriptJob( p=self.objectName(), e=['PreFileNewOrOpened', self.newsceneReload])


    #--------------------------------------------------------------------------------------------------------------------------

    def undoable(function):
        """A decorator that will make commands undoable in maya"""

        def decoratorCode(*args, **kwargs):
            mc.undoInfo(openChunk=True)
            functionReturn = None
            try:
                functionReturn = function(*args, **kwargs)
            except:
                print (sys.exc_info()[1])

            finally:
                mc.undoInfo(closeChunk=True)
                return functionReturn
        return decoratorCode


    #--------------------------------------------------------------------------------------------------------------------------


    def newsceneReload(self):
        self.listSteps()
        self.setStep()

    def enableEditMenu(self):
        self.editItem.setEnabled(0)
        items = self.ui.buildList.selectedItems()
        if not items:
            return

        item = items[0].whatsThis()
        if 'Custom.' in  item:
            self.editItem.setEnabled(1)

    def editCustomFile(self):
        mod = importlib.import_module(self.ui.buildList.currentItem().whatsThis().split('.')[0])
        path = mod.__file__.replace('.pyc', '.py')
        cmd = '{0} {1} &'.format('sublime', path)
        os.system(cmd)


    #--------------------------------------------------------------------------------------------------------------------------


    def listRigTypes(self, keepcurrent=False):
        crtype = assetEnv.getrigtype()

        self.rigTypeMenu.clear()
        rtypes = assetEnv.getjsoninfo('rigTypes')
        if not rtypes:
            return

        for rtype in rtypes:
            item = QAction(self)
            item.setText(rtype)
            item.triggered.connect(self.setRigType)
            item.triggered.connect(self.listSteps)
            item.triggered.connect(self.setStep)
            item.triggered.connect(self.listWorkVersions)
            self.rigTypeMenu.addAction(item)

        if rtypes:
            self.setRigType(rtypes[0])

        if keepcurrent and crtype in rtypes:
            self.setRigType(crtype)

    def setRigType(self, text=None):
        if not text:
            text = self.sender().text()

        self.ui.rigTypeBtn.setText(text)
        assetEnv.setrigtype(text)


    #--------------------------------------------------------------------------------------------------------------------------


    def listSteps(self):
        # Populate build list modelues
        # used rigBuildList.py / templatePart.py
        # get build modules from list
        rigType = assetEnv.getrigtype()
        self.ui.buildList.clear()
        self.ui.rigTypeBtn.setToolTip('')

        # read buildlist file / read templateParts file
        try:
            rigBuildList = importMod.import_module(rigType+'BuildList', r=1)
            modules = rigBuildList.functions(rigType=rigType)

            templateParts = importMod.import_module('templateParts', r=1)
            parts = templateParts.parts()
        except:
            self.ui.buildList.addItem('# No Template Found #')
            return

        self.ui.rigTypeBtn.setToolTip(rigBuildList.__file__)

        # create command set / add command item in self.buildList
        commands = []
        labels = []

        for module in modules:
            module.strip()

            # ['assetPrep.build()', 'Build Prep']
            tokens = module.split (' :: ')
            # control rig set
            if len(tokens) > 1 and module.startswith('templateTools.getRigBuildType'):
                for p in parts:
                    commands.append ('{0}.anim()'.format(p))
                    labels.append('{0}Build {1}'.format(' '*12, p))

            # import or custom set
            elif len(tokens) > 1:
                commands.append(tokens[0])
                labels.append('{0}{1}'.format(' '*12, tokens[1]))

            # head label set
            else:
                commands.append('')
                labels.append('\n{0}{1}'.format(' '*8, tokens[0]))

        # Add to list
        for i in range(len(labels)):
            item = QtWidgets.QListWidgetItem()
            item.setText(labels[i])
            # set item command data --->buildStep()
            item.setWhatsThis(commands[i])
            self.checkSource(item, commands[i])
            self.ui.buildList.addItem(item)


    #--------------------------------------------------------------------------------------------------------------------------

    def checkSource(self, item, command):
        asset = assetEnv.getasset()
        if not command:
            item.setForeground(QtGui.QColor('gray')) # gray
            item.setToolTip('')
            return

        # Get command parent module
        test = '.'.join(command.split('(')[0].split('.')[:-1])
        sfile = ''

        if len(test) > 1: # Remove'\n' in buildList
            if not test[0] == 'mc' and not test[0] == 'mel':

                try:
                    func = importMod.import_module(test, r=1)
                    sfile = func.__file__
                    if asset in sfile:
                        # custom rig set
                        item.setForeground(QtGui.QColor(102, 204, 255)) # cyan

                    elif 'parts' in sfile:
                        # base part rig set
                        item.setForeground(QtGui.QColor(255,255,102)) # yellow

                    item.setToolTip('Function:\n   {0}\n\nFile Path:\n   {1}'.format(command, sfile))

                except:
                    # error rig set
                    item.setForeground(QtGui.QColor(255,51,102)) # pink
                    item.setToolTip('Function:\n   {0}\n\nFile Path Not Found! ***'.format(command))

    #--------------------------------------------------------------------------------------------------------------------------


    # build functions
    def createStepNode(self):
        # create a rig build data node in current sence.
        current = mc.ls(sl=1)
        if not assetEnv.getasset():
            return

        if not mc.objExists('rigBuild_currentStep'):
            mc.createNode ('mute', n='rigBuild_currentStep')
            mc.select (current)

        if not mc.objExists('rigBuild_currentStep.asset'):
            mc.addAttr('rigBuild_currentStep', ln='asset' , dt='string')
            mc.setAttr ('rigBuild_currentStep.asset', assetEnv.getasset(), type= 'string')

        if not mc.objExists('rigBuild_currentStep.rigType'):
            mc.addAttr('rigBuild_currentStep', ln='rigType' , dt='string')
            mc.setAttr ('rigBuild_currentStep.rigType', assetEnv.getrigtype(), type= 'string')

        if not mc.objExists('rigBuild_currentStep.step'):
            mc.addAttr('rigBuild_currentStep', ln='step' ,at='long', dv=-1)


    #--------------------------------------------------------------------------------------------------------------------------


    def getStep(self):
        self.createStepNode()# check build data node
        asset = mc.getAttr ('rigBuild_currentStep.asset')
        rigType = mc.getAttr('rigBuild_currentStep.rigType')

        if asset == assetEnv.getasset() and rigType == assetEnv.getrigtype():
            return mc.getAttr('rigBuild_currentStep.step')
        else:
            return -1

    def setStep(self, step=None):
        self.createStepNode()
        try:
            asset = mc.getAttr('rigBuild_currentStep.asset')
            rigType = mc.getAttr('rigBuild_currentStep.rigType')
        except:
            return

        if not asset == assetEnv.getasset() or not rigType == assetEnv.getrigtype():
            return

        node = 'rigBuild_currentStep'
        if step is None:
            step = self.getStep()

        # get max step
        if step >= self.ui.buildList.count():
            step = self.ui.buildList.count()-1
        mc.setAttr(node+'.step', step)

        # get step failed
        if step == -1:
            return

        # can not found buildList.py
        if self.ui.buildList.item(0):
            if self.ui.buildList.item(0).text() == '**No Layout Found**':
                return

        if step > -1:
            try:
                # set final step item color.
                for i in range(step):
                    self.ui.buildList.item(i).setForeground(QtGui.QColor(0,153,102))
                # set last step item color.
                self.ui.buildList.item(step).setForeground(QtGui.QColor(51,255,153))
            except:
                pass


    #--------------------------------------------------------------------------------------------------------------------------


    # Build this step!!
    @undoable
    def buildStep(self, step, gMainProgressBar=None):
        if not self.ui.buildList.item(0) or self.ui.buildList.item(0).text() == 'Cannot find Layout!':
            return

        item = self.ui.buildList.item(step)
        if not item:
            return

        cmd = str(item.whatsThis().strip())
        label = str(item.text().strip())

        if not cmd:
            self.cacheStep(step)
            self.setStep(step)
            return True

        try:
            self.ui.buildList.item(step).setForeground(QtGui.QColor(255,153,51))
            tokens = cmd.split('(')[0].split('.')
            module = '.'.join(tokens[0:-1])

            if module:
                mod = importMod.import_module(module, r=1)
                if not assetEnv.getasset() or not assetEnv.getrigtype() or not assetEnv.getpath():
                    if gMainProgressBar:
                        mc.progressBar(gMainProgressBar, e=True, ep=True)
                    return

                func = cmd.split('(')[0].split('.')[-1]
                args = eval('dict('+cmd.split('(')[-1].split(')')[0]+')')
                print(args)
                print(mod)
                print(func)
                print ('\n\nRUNNING: {0}'.format(cmd))
                print ('ASSET: {0}'.format(assetEnv.getasset()))
                print ('RIG TYPE: {0}'.format(assetEnv.getrigtype()))
                print ('MODULE PATH: {0}'.format(mod))


                getattr(mod, func)(**args)
                print ('\nSUCCESS: {0}'.format(cmd))

            else:
                exec(cmd)

            self.cacheStep(step)
            self.setStep(step)
            return True

        except Exception:
            if gMainProgressBar:
                mc.progressBar(gMainProgressBar, e=True, ep=True)

            self.ui.buildList.item(step).setForeground(QtGui.QColor(255,51,102))
            traceback.print_exc()
            return


    #--------------------------------------------------------------------------------------------------------------------------


    def buildNext(self):
        step = self.getStep()+1
        if not step or step < 0:
            step = 0
        self.buildStep(step)

        print (self.getStep()+1)


    #--------------------------------------------------------------------------------------------------------------------------


    def buildBatch(self, maxstep=False):

        print ('\nBATCH BUILDING')
        step = self.getStep()+1
        if not step or step < 0:
            step = 0

        if maxstep and not self.ui.buildList.selectedItems():
            return
        elif maxstep and self.ui.buildList.selectedItems():
            maxstep = self.ui.buildList.currentRow()
        else:
            maxstep = self.ui.buildList.count()

        if maxstep < step:
            return

        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        mc.progressBar( gMainProgressBar, e=True, bp=True, ii=True, st='Building Rig ...', max=maxstep-step+1)

        for i in range(step, maxstep+1):
            if mc.progressBar(gMainProgressBar, q=True, ic=True):
                mc.progressBar(gMainProgressBar, e=True, ep=True)
                return

            result = self.buildStep(i, gMainProgressBar)
            if result:
                mc.progressBar(gMainProgressBar, e=True, step=1)
                QtCore.QCoreApplication.processEvents()
                mc.refresh()
            else:
                mc.progressBar(gMainProgressBar, e=True, ep=True)

        try:
            mc.progressBar(gMainProgressBar, e=True, ep=1)
        except:
            pass


    #--------------------------------------------------------------------------------------------------------------------------


    def buildSelected(self):
        if self.ui.buildList.selectedItems():
            self.buildStep(self.ui.buildList.currentRow())

    def rebuildSelected(self):
        step = self.ui.buildList.currentRow()
        if step > 0:
            if self.loadCache(1):
                self.buildStep(step)
            else:
                mc.warning('No previously saved step was found!')


    #--------------------------------------------------------------------------------------------------------------------------


    # caching
    def cacheStep(self, index=None):
        path = assetEnv.getpath()

        if os.path.isdir(path) and assetEnv.getcache():
            cachepath = os.path.join (path,'build','cache')

            if not os.path.isdir(cachepath):
                os.makedirs(cachepath)
            if index is None:
                index = self.getStep()

            mel.eval('source "cleanUpScene.mel";')
            mel.eval('deleteUnknownNodes();')

            filename = os.path.join (cachepath, '{0}{1}_{2}step.ma'.format (assetEnv.getasset(), assetEnv.getrigtype().replace(' ',''), index))
            mc.file(filename, pr=1, ea=1, f=1, type='mayaAscii')

            print ('# Cached Step: '+filename)

    def loadCache(self, previous=False):
        if not assetEnv.getcache():
            return

        if not self.ui.buildList.count():
            return

        if self.ui.buildList.item(0).text() == 'Cannot find Layout!':
            return

        if self.ui.buildList.currentRow() < 0:
            return

        index = self.ui.buildList.currentRow()

        if previous and index >= 1:
            index = index-1

        path = assetEnv.getpath()
        if not os.path:
            return

        cachepath = os.path.join (path, 'build','cache')
        if not os.path.isdir(cachepath):
            os.makedirs(cachepath)
            return

        filename = os.path.join (cachepath, '{0}{1}_{2}step.ma'.format (assetEnv.getasset(), assetEnv.getrigtype().replace(' ',''), index))

        # check for proper variables or retun
        if not mc.file(filename, q=1,ex=1):
            mc.warning('No previously saved step was found!')
            return

        if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
            return

        mc.file (filename, i=1)

        self.listSteps()
        self.setStep(self.getStep()+1)
        print ('# Loaded cache Step: '+filename)
        return True


    #--------------------------------------------------------------------------------------------------------------------------


    def listWorkVersions(self):

        self.importRigMenu.clear()

        if not assetEnv.getrigtype():
            return

        sub = assetEnv.getrigtype()
        if not sub :
            return

        items = []
        path = os.path.join(assetEnv.getpath(), 'work')

        if not os.path.isdir(path):
            return

        files = [f for f in os.listdir(path) if re.search(sub+'_v[0-9][0-9][0-9].', f)]
        itemdict = {}
        count = []
        for f in files:
            id =  f.split('.')[0].split('_v')[-1]
            count.append(id)
            itemdict[id] = f

        items = []
        count.sort()
        for c in count:
            items.append(itemdict[c])

        items.reverse()

        maxitems = 20
        for item in items[:maxitems]:
            paction = QAction(self)
            paction.setText(str(item))
            paction.triggered.connect( self.importAsset)
            self.importRigMenu.addAction (paction)

        if len(items) > maxitems:
            div = QAction(self)
            div.setSeparator (1)
            self.importRigMenu.addAction (div)

            self.prevMenu = QtWidgets.QMenu('Older Versions')
            self.importRigMenu.addMenu (self.prevMenu)

            for item in items[maxitems:]:
                paction = QAction(self)
                paction.setText(str(item))
                paction.triggered.connect( self.importAsset)
                self.prevMenu.addAction (paction)


    #--------------------------------------------------------------------------------------------------------------------------


    def saveWorkFile(self):
        sub = assetEnv.getrigtype()
        items = []
        asset = assetEnv.getasset()
        path = os.path.join(assetEnv.getpath(), 'work')

        if not sub or not asset or not os.path.isdir(path):
            mc.warning ('Cannot export! Make sure your asset is set.')
            return

        result = mc.promptDialog(
                        title='Save Work File',
                        message='Set an optional name.',
                        button=['Save', 'Cancel'],
                        defaultButton='Save',
                        dismissString='Cancel',
                        text='')

        if result == 'Cancel':
            return

        # get file name and export
        text = mc.promptDialog(q=1, tx=1)

        tokens = text.strip().split(' ')
        token = tokens[0]
        for t in tokens[1:]:
            if tokens:
                token += t[0].capitalize()+t[1:]

        token = token.strip()

        if token:
            token += '_'

        filename = aboutFile.getNewWorkRigVersion(path, asset, token, sub)
        mc.file(filename, options='v=0', type='mayaAscii', pr=1, ea=1, f=1)

        self.listWorkVersions()
        print ('Exported Asset Version: '+filename)

    def importAsset(self):

        sub = assetEnv.getrigtype()

        items = []
        asset = assetEnv.getasset()
        path = os.path.join(assetEnv.getpath(), 'work')
        if not sub or not asset or not os.path.isdir(path):
            mc.warning ('Cannot import! Make sure your asset is set.')
            return

        filename = rig = self.sender().text()
        path = os.path.join(path, filename)

        if not mc.file(path, q=1,ex=1):
            mc.warning ("File doesn't exist: "+path)
            return

        if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
            return

        mc.file (path, i=1)
        print ('# Imported: '+path)