#!/usr/bin/python
# -*- coding: utf-8 -*-
#========================================
#    author: ruixi.Wang
#      mail: wrx1844@qq.com
#      time: 2019.07.02
#========================================
import os
import sys
import re
import subprocess
import zipfile
import shutil
import getpass
import json
import datetime
from importlib import reload
import maya.cmds as mc

def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from PySide2.QtWidgets import QAction
        from rxUi.pyside2 import main_ui
        from rxUi.pyside2 import newAsset_ui
        return QtCore, QtGui, QtWidgets, QAction, main_ui, newAsset_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from PySide6.QtGui import QAction
            from rxUi.pyside6 import main_ui
            from rxUi.pyside6 import newAsset_ui
            return QtCore, QtGui, QtWidgets, QAction, main_ui, newAsset_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets, QAction, main_ui, newAsset_ui= get_pyside_module()

# core
from rxCore import aboutUI
from rxCore import aboutFile

# public
import template
import build
import assetEnv
import assetCheck

# reload
reload(aboutUI)
reload(main_ui)
reload(template)
reload(build)
reload(assetEnv)
reload(assetCheck)

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

def run():
    aboutUI.dockWin(RigSys)

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

class RigSys(QtWidgets.QWidget):
    DOCK_NAME = 'RiggingBox'
    DOCK_LABEL = 'Rig_System'

    def __init__( self, parent=None ):

        super(RigSys, self).__init__(parent)

        # UI size init
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.DOCK_LABEL)

        # load UI
        self.ui = main_ui.Ui_rs_win()
        self.ui.setupUi(self)

        # set button icons
        self.iconPath = assetEnv.geticons()
        self.ui.setBtn.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'editOff.png')))
        self.ui.newRigBtn.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'plus.png')))
        self.ui.openPathBtn.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'openPath.png')))

        # set project env
        while not assetEnv.getroot():
            assetEnv.setroot()

        # add template
        self.cui = assetCheck.AssetCheck()
        self.tui = template.Template()
        self.bui = build.Build()
        # self.eui = export.Export()
        # self.ttui = tagTools.TagTools()

        # add core tab
        self.ui.tabsWdg.addTab(self.cui, 'Check')
        self.ui.tabsWdg.addTab(self.tui, 'Template')
        self.ui.tabsWdg.addTab(self.bui, 'Build')
        # self.ui.tabsWdg.addTab(self.eui, 'Export')
        # self.tui.createPartsMenu()

        # actions and menus
        self.ui.assetList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # self.ui.idLb.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # self.ui.idLb.setCursor(QtCore.Qt.PointingHandCursor)
        self.ui.stratInfoLb.setPixmap(QtGui.QPixmap(os.path.join(self.iconPath, 'headInfo.png')))
        # self.ui.idLb.setBaseSize(QtCore.QSize(100, 100))

        item = QAction(self)
        item.setText('Snapshot Icon')
        item.triggered.connect(self.createIcon)
        self.ui.idLb.addAction(item)

        item = QAction(self)
        item.setText('Reset Icon')
        item.triggered.connect(self.clearIcon)
        self.ui.idLb.addAction(item)

        # inintial display
        self.ui.rootLine.setText(assetEnv.getroot())
        self.ui.tabsWdg.setCurrentIndex(2)
        aboutUI.hide_layout_items(self.ui.assetsInfoHBox)

        # Signals
        self.ui.setBtn.toggled.connect(self.toggleEnvWidget)
        self.ui.rootBtn.clicked.connect(self.setroot)
        self.ui.assetList.itemSelectionChanged.connect(self.setEnv)
        self.ui.assetList.itemSelectionChanged.connect(self.listAssetInfo)
        self.ui.assetList.itemSelectionChanged.connect(self.toggleDisableTabs)

        self.ui.newRigBtn.clicked.connect(self.createNewRigType)
        self.ui.openPathBtn.clicked.connect(self.browseAssetPath)
        self.ui.newAssetBtn.clicked.connect(self.createNewAsset)

        self.ui.tabsWdg.currentChanged.connect(self.reloadTemplateWidgets)
        self.ui.tabsWdg.currentChanged.connect(lambda: self.reloadBuildWidgets(keepcurrent=True))

        assetEnv.setasset()
        self.toggleEnvWidget()
        self.toggleDisableTabs()
        self.listAssets()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------

    def setroot(self):
        assetEnv.setroot(1)
        self.ui.rootLine.setText(assetEnv.getroot())
        self.listAssets()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------

    def setEnv(self):

        # lock tabsWdg wight
        self.ui.tabsWdg.setEnabled(0)

        # clean current asset env
        # clean ui display
        assetEnv.setasset()
        assetEnv.setsys()

        # set select asset env and update ui info.
        if self.ui.assetList.selectedItems():
            # list[0]
            asset = self.ui.assetList.selectedItems()[0].text()
            assetEnv.setasset(asset)
            assetEnv.setsys()

            asset = assetEnv.getasset()
            path = assetEnv.getpath()

            if asset and path:
                setlabel = asset
                if not assetEnv.getuser() == getpass.getuser():
                    setlabel += ' | '+assetEnv.getuser()

            self.ui.tabsWdg.setEnabled(1)
            self.ui.assetPathLine.setText(path)
        else:
            pass

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------


    def listAssetInfo(self):
        # self.ui.assetNameDate.setText('Nothing was selected ！')
        # self.ui.createdDate.setText('')
        # self.ui.modDate.setText('')
        # self.ui.rigTypeDate.setText('')

        self.ui.stratInfoLb.show()
        aboutUI.hide_layout_items(self.ui.assetsInfoHBox)

        asset = assetEnv.getasset()
        assetPath = assetEnv.getpath()

        if self.ui.assetList.selectedItems():
            self.ui.stratInfoLb.hide()
            aboutUI.show_layout_items(self.ui.assetsInfoHBox)

            if asset and assetPath:
                # set icon
                iconpath = os.path.join(assetPath, 'build', 'icon.png')
                iconpath = iconpath.replace('\\', '/')

                if os.path.isfile(iconpath):
                    self.ui.idLb.setPixmap(QtGui.QPixmap(iconpath))
                    self.ui.idLb.setBaseSize(QtCore.QSize(100, 100))
                else:
                    self.ui.idLb.setPixmap(QtGui.QPixmap(os.path.join(self.iconPath, 'Shinji.png')))
                    self.ui.idLb.setBaseSize(QtCore.QSize(100, 100))

                # list creation info from json
                data = assetEnv.getjsoninfo()
                if data:
                    rigs = ''
                    for typ in data['rigTypes']:
                        rigs += typ+' / '
                    self.ui.assetNameDate.setText(data['asset'])
                    self.ui.createdDate.setText(data['creationDate'])
                    self.ui.modDate.setText(data['createdBy'])
                    self.ui.rigTypeDate.setText(rigs)
                else:
                    self.ui.assetNameDate.setText('--')
                    self.ui.createdDate.setText('--')
                    self.ui.modDate.setText('--')
                    self.ui.rigTypeDate.setText('--')
                    self.ui.newRigBtn.hide()
            else:
                # clean asset env
                assetEnv.setasset()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------


    def createIcon(self):
        #Use maya playblast to create a asset image.
        tmp = os.path.join(mc.internalVar(utd=1), 'icon.png')
        iconpath = os.path.join(assetEnv.getpath(), 'build',  'icon.png')
        mc.playblast(fr=mc.currentTime(q=1), cf=tmp,
                    format='image',
                    clearCache=0,
                    viewer=0,
                    showOrnaments=0,
                    offScreen=1,
                    percent=100,
                    compression= 'png',
                    quality=100,
                    widthHeight=[120, 120])

        if not os.path.isfile(tmp):
            mc.warning ('Could not save image!')
            return

        image = QtGui.QImage(tmp)
        out = QtGui.QImage(image.width(), image.height(), QtGui.QImage.Format_ARGB32)
        out.fill(QtCore.Qt.transparent)

        brush = QtGui.QBrush(image)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(43,43,43))
        pen.setJoinStyle(QtCore.Qt.RoundJoin)

        painter = QtGui.QPainter()
        painter.begin(out)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(1, 1, image.width(), image.height(), 1, 1)
        painter.end()

        out.save(iconpath, 'PNG', 100)
        if os.path.isfile(iconpath):
            self.ui.idLb.setPixmap(QtGui.QPixmap(iconpath))
            #self.ui.idLb.setIconSize(QtCore.QSize(100, 100))
        else:
            mc.warning ('Could not save image!')

        self.listAssets()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------

    def clearIcon(self):
        iconpath = os.path.join(assetEnv.getpath(), 'build', 'icon.png')
        if os.path.isfile(iconpath):
            os.remove(iconpath)
            # set default icon
            self.ui.idLb.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'Shinji.png')))
            #self.ui.idLb.setIconSize(QtCore.QSize(100, 100))
        self.listAssets()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def zipAsset():

        #zip rig file

        result = mc.fileDialog2(fm=3)
        if not result:
            return

        asset = assetEnv.getasset()
        path = assetEnv.getpath()
        apath = aboutFile.getNewVersion(result[0], asset+'_archive')

        # check everything
        for d in ['template', 'scripts', 'assetinfo.json']:
            if not os.path.exists(os.path.join(path, 'build', d)):
                print ( os.path.join(path, 'build', d) )
                mc.warning( d+' doesnt exist! Cannot archive..')
                return

        # search template file.
        templates = [f for f in os.listdir(os.path.join(path, 'build', 'template')) if re.search('_template_v[0-9][0-9][0-9].', f)]
        if not templates:
            print ( os.path.join(os.path.join(path, 'build', 'template')) )
            mc.warning('template file doesnt exist! Cannot archive..')
            return

        # create base dir
        try:
            os.makedirs(apath)
        except:
            mc.warning('Cannot create archive dir. Please choose a different location..')
            return

        # Copy build dir items
        os.makedirs(os.path.join(apath, 'build'))
        builditems = os.listdir(os.path.join(path, 'build'))
        if 'template' in builditems:
            builditems.remove('template')
        if 'cache' in builditems:
            builditems.remove('cache')

        for item in builditems:
            sitem = os.path.join(path, 'build', item)
            ditem = os.path.join(apath, 'build', item)

            if os.path.isfile(sitem):
                shutil.copyfile(sitem, ditem)
                shutil.copystat(sitem, ditem)

            elif os.path.isdir(sitem):
                shutil.copytree(sitem, ditem)

        # copy latest template file / templateParts file
        templates.sort()
        temp = templates[-1]

        os.makedirs(os.path.join(apath, 'build', 'template'))

        sitem = os.path.join(path, 'build', 'template', temp)
        ditem = os.path.join(apath, 'build', 'template', temp)
        if os.path.isfile(sitem):
            shutil.copyfile(sitem, ditem)
            shutil.copystat(sitem, ditem)

        sitem = os.path.join(path, 'build', 'template', 'templateParts.py')
        ditem = os.path.join(apath, 'build', 'template', 'templateParts.py')
        if os.path.isfile(sitem):
            shutil.copyfile(sitem, ditem)
            shutil.copystat(sitem, ditem)

        # Copy everything else
        items = os.listdir(path)
        if 'build' in items:
            items.remove('build')

        for item in items:
            ipath = os.path.join(path, item)
            dipath = os.path.join(apath, item)

            if not os.path.isdir(dipath):
                os.makedirs(dipath)

            # Get latest files in each
            sitem = os.path.join(ipath, aboutFile.getHighestVersion(ipath))
            ditem = os.path.join(dipath, aboutFile.getHighestVersion(ipath))

            if os.path.isfile(sitem):
                shutil.copyfile(sitem, ditem)
                shutil.copystat(sitem, ditem)

        shutil.make_archive(apath, 'zip', apath)
        os.rename(apath+'.zip', apath+'.rig')
        shutil.rmtree(apath)

        print ( 'Successfully Zip {0} to: {1}.rig'.format(asset, apath) )


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------


    def unzipAsset(self):
        multipleFilters = "Rig Package File (*.rig)"
        result = mc.fileDialog2(fileFilter=multipleFilters, fm=1, okc='Unpack')

        if not result or not assetEnv.getroot():
            return

        asset = os.path.basename(result[0]).split('_archive_')[0]
        dpath = os.path.join(assetEnv.getroot(), asset)
        zipf = result[0].split('_archive_')[0]+'.zip'
        shutil.copyfile(result[0], zipf)

        if os.path.isdir(dpath):
            cn = mc.confirmDialog( title='Overwrite Asset',
                message='Asset {0} already exists. Do you want to overwrite?'.format(asset),
                button=['Yes','No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No' )
            if cn == 'Yes':
                shutil.rmtree(dpath)
        try:
            os.makedirs(dpath)
        except:
            mc.warning('Cannot create asset dir!')

        zipfile.ZipFile(zipf).extractall(dpath)
        os.remove(zipf)
        self.listAssets()


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------


    def listAssets(self):
        if not os.path.isdir(assetEnv.getroot()):
            return []

        items = []
        for p in [f for f in os.listdir(assetEnv.getroot()) if os.path.isdir(os.path.join(assetEnv.getroot(), f))]:
            if os.path.isfile(os.path.join(assetEnv.getroot(), p, 'build','assetinfo.json')):
                items.append(p)

        items = sorted(items, key=lambda s: s.lower())

        # Get asset list data
        selItemID = self.ui.assetList.currentRow()
        # Clear asset list
        self.ui.assetList.clear()

        # Icon list widget set
        itemIconsData = {}
        for item in items:
            itemIcon = os.path.join(assetEnv.getroot(), item, 'build', 'icon.png')
            if not os.path.isfile(itemIcon):
                itemIcon = os.path.join(self.iconPath, 'Shinji.png')

            itemIconsData[item] = itemIcon

        for key in itemIconsData:
            iconItem = QtWidgets.QListWidgetItem()
            iconItem.setText(key)
            iconItem.setIcon( QtGui.QIcon(itemIconsData[key]) )
            # iconItem.setSizeHint(QtCore.QSize(60, 60))
            #add item
            self.ui.assetList.addItem(iconItem)

        self.ui.assetList.sortItems()
        if selItemID:
            self.ui.assetList.setCurrentRow(selItemID)

        self.ui.assetList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # Item right button menu
        self.ui.assetList.customContextMenuRequested.connect(self.iconMenu)
        return items

    def iconMenu(self, position):
        """
        design assetList item's right menu
        :param position:
        :return:
        """
        selectItem = self.ui.assetList.selectedItems()

        # menu
        menu = QtWidgets.QMenu(self)
        div = QAction(self)
        div.setSeparator(1)

        # add action
        zipAction = menu.addAction("zip")
        menu.addAction(div)
        unzipAction = menu.addAction("unzip")

        # cmds
        action = menu.exec_( self.ui.assetList.mapToGlobal(position) )

        if action == zipAction:
            if selectItem:
                self.zipAsset()
            else:
                print ('zip file need selected one asset')
        elif action == unzipAction:
            self.unzipAsset()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # modify widgets

    def reloadModelCheckWidgets(self):
        self.cui.reloadChecks()

    def reloadRigCheckWidgets(self):
        self.bui.listRigTypes()
        self.cui.reloadChecks()

    def reloadTemplateWidgets(self):
        self.tui.createPartsMenu()
        self.tui.listPartsInScene()
        self.tui.listTemplateVersions()
        self.tui.clearBuildOptions()

    def reloadBuildWidgets(self, keepcurrent=False):
        self.bui.listRigTypes(keepcurrent=keepcurrent)
        self.bui.listWorkVersions()
        self.bui.listSteps()
        self.bui.setStep()

    def toggleEnvWidget(self):
        if not assetEnv.getasset() or not self.ui.setBtn.isChecked():
            self.ui.setBtn.setChecked(0)
            self.ui.setBtn.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'editOff.png')))
            self.ui.tabsWdg.hide()
            self.ui.envWdg.show()
            self.ui.openPathBtn.hide()
            self.ui.assetPathLine.hide()
            self.ui.assetNameDate.setStyleSheet("color:red;")
        else:
            self.ui.setBtn.setIcon(QtGui.QPixmap(os.path.join(self.iconPath, 'editOn.png')))
            self.ui.tabsWdg.show()
            self.ui.envWdg.hide()
            self.ui.openPathBtn.show()
            self.ui.assetPathLine.show()
            self.ui.assetNameDate.setStyleSheet("color:lime;")

        self.reloadTemplateWidgets()
        self.reloadBuildWidgets()
        self.reloadRigCheckWidgets()
        self.reloadModelCheckWidgets()

    def toggleDisableTabs(self):
        if assetEnv.getasset():
            self.ui.tabsWdg.setEnabled(1)
            self.ui.openPathBtn.setEnabled(1)
        else:
            self.ui.tabsWdg.setEnabled(0)
            self.ui.openPathBtn.setEnabled(0)


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # create new assets or new rig type.

    def createNewAsset(self):
        newRigType()
        self.listAssets()
        for i in range(self.ui.assetList.count()):
            if self.ui.assetList.item(i).text() == os.environ['rxNEWASSET']:
                self.ui.assetList.setCurrentItem(self.ui.assetList.item(i))
        self.listAssetInfo()

    def createNewRigType(self):
        if self.ui.assetList.selectedItems():
            newRigType(self.ui.assetList.currentItem().text())

        self.setEnv()
        self.listAssetInfo()
        self.ui.openPathBtn.setEnabled(1)

    def browseAssetPath(self):
        path = self.ui.assetPathLine.text()
        if os.path.isdir(path):
            if sys.platform == 'darwin':
                subprocess.check_call(['open', '-R', path])
            elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', path])
            elif sys.platform == 'win32':
                subprocess.check_call(['explorer', path])

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create a new asset on disk
def newRigType(asset=None):
    #widget = QtWidgets.QWidget()
    dlg = NewAsset(asset)
    dlg.exec_()


class NewAsset(QtWidgets.QDialog):
    def __init__(self, asset=None):
        super(NewAsset, self).__init__()
        self.ui = newAsset_ui.Ui_newAssetUI()
        self.ui.setupUi(self)

        # connect
        self.ui.createBtn.clicked.connect(self.createTask)
        self.ui.cancelBtn.clicked.connect(self.deleteLater)

        # use setPlaceholderText set lineEdit default string.
        self.ui.otherLine.setPlaceholderText('assetName_newRig')

        if asset:
            self.ui.label.setText('Add Rig Type')
            self.asset = asset
            self.ui.nameLine.setText(asset)
            self.ui.otherLine.setText(asset+'_newRig')
            self.ui.nameLine.setEnabled(0)

        self.asset = asset
        os.environ['rxNEWASSET'] = ''

    #############################################
    # create the new asset, set env and makedirs
    def createTask(self):
        if not self.asset and self.ui.nameLine.text():
            self.asset = self.ui.nameLine.text()

        if not self.asset:
            mc.warning('No asset specified!')
            return

        # build paths and create dirs on disk
        root = assetEnv.getroot()
        rigs = []

        if self.ui.animChx.isChecked():
            rigs.append('rig')

        if self.ui.gameChx.isChecked():
            rigs.append('gameRig')

        if self.ui.mocapChx.isChecked():
            rigs.append('mocapRig')

        if self.ui.otherChx.isChecked():
            other = self.ui.otherLine.text().strip().replace(' ', '_')
            rigs.append(other)

        if not rigs:
            mc.warning ('Must choose at least one rig type to create.')
            return

        basepath = os.path.join(root, self.asset)

        # check if asset.json exists
        jfile = os.path.join(basepath, 'build','assetinfo.json')
        if os.path.isfile(jfile):
            with open(jfile, 'r') as f:
                data = json.load(f)
                allrigs = list(set(data['rigTypes']+rigs))
                allrigs.sort()
                if self.asset+'_rig' in allrigs:
                    allrigs.remove(self.asset+'_rig')
                    allrigs.insert(0, self.asset+'_rig')

                assetdata = {
                   'asset' : self.asset,
                   'creationDate' : data['creationDate'],
                   'createdBy' : data['createdBy'],
                   'rigTypes' : allrigs }

        else:
            assetdata = {
               'asset' : self.asset,
               'creationDate' : datetime.datetime.strftime(datetime.datetime.now(), '%a, %b %d %Y'),
               'createdBy' : getpass.getuser(),
               'rigTypes' : rigs }

        # create paths
        paths = [
                os.path.join(basepath, 'build', 'template'),
                os.path.join(basepath, 'build', 'scripts'),
                os.path.join(basepath, 'work')]

        for rig in rigs:
            paths.append(os.path.join(basepath, 'build', 'bind', rig))

        paths = list(set(paths))
        for p in paths:
            if not os.path.isdir(p):
                try:
                    os.makedirs(p)
                except:
                    mc.warning('Could not create: '+p)

        with open(jfile, 'w') as f:
            json.dump(assetdata, f, indent=4, sort_keys=True)

        for rig in rigs:
            # rig build list scripts
            self.createAssetCustom(os.path.join(basepath, 'build', 'scripts'), rig)
            self.createRigBuildList(os.path.join(basepath, 'build', 'scripts'), rig)

        assetEnv.setasset(self.asset)
        self.deleteLater()

    @staticmethod
    def createAssetCustom(dpath, rig):
        sfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assetCustom.py')
        dfile = os.path.join(dpath, rig+'Custom.py')

        if not os.path.isdir(os.path.dirname(dfile)) or sfile == dfile:
            return

        if not os.path.isfile(dfile):
            shutil.copyfile(sfile, dfile)

    @staticmethod
    def createRigBuildList(dpath, rig):

        sfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rigBuildList.py')
        dfile = os.path.join(dpath, rig+'BuildList.py')
        if not os.path.isdir(os.path.dirname(dfile)) or os.path.isfile(dfile):
            return

        if not os.path.isfile(dfile):
            shutil.copyfile(sfile, dfile)


# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\main_ui.py .\mainUI.ui
# &"C:\Program Files\Autodesk\Maya2025\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2025\bin\uic" -o .\main_ui.py .\mainUI.ui
# &"C:\Program Files\Autodesk\Maya2025\bin\uic" -g python .\mainUI.ui -o .\main_ui.py