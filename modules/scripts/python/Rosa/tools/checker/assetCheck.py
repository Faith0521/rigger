#!/usr/bin/python
# -*- coding: utf-8 -*-
from importlib import reload
from PySide2 import QtCore, QtGui, QtWidgets

import maya.cmds as mc

from . import modelChecks
from . import rigChecks
from . import assetCheck_ui
from ...maya_utils import aboutUI

reload(assetCheck_ui)
reload(modelChecks)
reload(rigChecks)


# Rig Check UI

def uiShow():
    avskin = AssetCheck()
    avskin.show()


class AssetCheck(QtWidgets.QWidget, assetCheck_ui.Ui_assetCheckUI):

    def __init__(self, uiName='assetCheckUI', parent=aboutUI.get_maya_window()):
        # UI modify
        super(AssetCheck, self).__init__(parent=parent)
        try:
            mc.deleteUI(uiName, control=True)
        except RuntimeError:
            pass

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(uiName)
        self.ui = assetCheck_ui.Ui_assetCheckUI()
        self.ui.setupUi(self)

        # Initiasl settings
        self.ui.checkTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.fixBtn.setText('Auto Fix Selected')

        if mc.window('checkReportUI', q=1, ex=1):
            mc.deleteUI('checkReportUI')

        # Menus
        # skip current item
        self.ui.checkTree.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        item = QtWidgets.QAction(self)
        item.setText('Skip This Check')
        item.triggered.connect(self.setSkipped)
        self.ui.checkTree.addAction(item)

        # Signals
        self.ui.checkTree.itemDoubleClicked.connect(self.checkItem)
        self.ui.checkBtn.clicked.connect(lambda: self.runCheck(index=None))
        self.ui.fixBtn.clicked.connect(self.runFix)

        # refresh check menu / check list.
        self.reloadChecks()

    # --------------------------------------------------------------------------------------------------------------
    @staticmethod
    def checklist():
        # DATA - set( Label, Function, Fix Function)
        # Difference rig type has different check list.
        checklist = {
            'BY_film_rig':
                [
                    ('Check for model normals', modelChecks.checkModelLockedNormals, modelChecks.fixModelLockedNormals, u"检查模型法线是否被锁定"),
                    ('Check for model smoothness', modelChecks.checkModelSmoothLevel, modelChecks.fixModelSmoothLevel, u"检查模型平滑显示是否为1"),
                    ('Check for namespaces', modelChecks.namespaces, u"检查文件中是否有未删除的命名空间"),
                    ('Check for sdk group value', rigChecks.checkSdkGroupValue, rigChecks.fixSdkGroupValue,
                     u"检查绑定中sdk组数值是否清零"),
                    ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes,
                     modelChecks.camsLightsImgPlanesfix, u'检查是否存在灯光，摄像机和Image平面'),
                    ('Check render & display layers', modelChecks.layers, u'检查是否有未删除的渲染显示层'),
                    ('Check for single rig hierarchy', modelChecks.singleHi, u"检查是否为单一的绑定层级"),
                    ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, u'检查场景中是否有重命名物体'),
                    ('Check for controller invalid name', rigChecks.checkInvalidCtrlNames,
                     rigChecks.fixInvalidCtrlNames, u"检查控制器是否有非法命名,eg.以'_'结尾命名"),
                    ('Check for controller default value', rigChecks.checkCtrlDefaultValue, rigChecks.fixCtrlDefaultValue, u"检查控制器默认数值是否清零"),
                    ('Check for controller been connected', rigChecks.checkControllerAttributesWithInput_elo, rigChecks.fixControllerAttributesWithInput_elo, u"检查控制器是否被连接"),
                    ('Check for not driven key objects', rigChecks.checkNotDrivenKey, rigChecks.fixNotDrivenKey, u"检查是否存在无用的动画节点"),
                    ('Check for closed skin node', rigChecks.checkClosedSkin, rigChecks.fixClosedSkin, u"检查是否有被关闭的蒙皮节点"),
                    ('Check for exists ngSkin nodes', rigChecks.checkNgskinExists, rigChecks.fixNgskinExists, u"检查是否存在没删除的Ng节点"),
                    ('Check for controller rotateOrder', rigChecks.checkInvalidCtrlRotateOrder, rigChecks.fixInvalidCtrlRotateOrder, u"检查控制器的rotateOrder是否为xyz"),
                    ('Check for rigging publish', rigChecks.checkPublish, rigChecks.fixUnPublish, "检查绑定是否点击过update"),
                    ('Check & create anim control ID Tags', rigChecks.checkCtrls, u"检查控制器ID"),
                ],

            'Elo_film_rig':
                [
                    ('Check for model normals', modelChecks.checkModelLockedNormals, modelChecks.fixModelLockedNormals, u"检查模型法线是否被锁定"),
                    ('Check for model smoothness', modelChecks.checkModelSmoothLevel, modelChecks.fixModelSmoothLevel, u"检查模型平滑显示是否为1"),
                    ('Check invalid helper joint controller name', rigChecks.checkHelperControlNames, rigChecks.fixHelperControlNames, u"检查辅助骨骼控制器是否不是以_ctrl结尾"),
                    ('Check for sdk group value', rigChecks.checkSdkGroupValue, rigChecks.fixSdkGroupValue, u"检查绑定中sdk组数值是否清零"),
                    ('Check for namespaces', modelChecks.namespaces, modelChecks.deleteNameSpaces, u"检查文件中是否有未删除的命名空间"),
                    ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes,
                     modelChecks.camsLightsImgPlanesfix, u'检查是否存在灯光，摄像机和Image平面'),
                    ('Check render & display layers', modelChecks.layers, u'检查是否有未删除的渲染显示层'),
                    ('Check for single rig hierarchy', modelChecks.singleHi, u"检查是否为单一的绑定层级"),
                    ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, u'检查场景中是否有重命名物体'),
                    ('Check for controller default value', rigChecks.checkCtrlDefaultValue,
                     rigChecks.fixCtrlDefaultValue, u"检查控制器默认数值是否清零"),
                    ('Check for controller invalid name', rigChecks.checkInvalidCtrlNames, rigChecks.fixInvalidCtrlNames, u"检查控制器是否有非法命名,eg.以'_'结尾命名"),
                    ('Check for controller been connected', rigChecks.checkControllerAttributesWithInput_elo,
                     rigChecks.fixControllerAttributesWithInput_elo, u"检查控制器是否被连接"),
                    ('Check for controller if endswith ctrl', rigChecks.checkControllerSuffixName,
                     rigChecks.fixControllerSuffixName, u"检查绑定系统外是否存在不是以_ctrl结尾命名的控制器"),
                    ('Check for not driven key objects', rigChecks.checkNotDrivenKey, rigChecks.fixNotDrivenKey, u"检查是否存在无用的动画节点"),
                    ('Check for closed skin node', rigChecks.checkClosedSkin, rigChecks.fixClosedSkin, u"检查是否有被关闭的蒙皮节点"),
                    ('Check for exists ngSkin nodes', rigChecks.checkNgskinExists, rigChecks.fixNgskinExists, u"检查是否存在没删除的Ng节点"),
                    ('Check for controller rotateOrder', rigChecks.checkInvalidCtrlRotateOrder,
                     rigChecks.fixInvalidCtrlRotateOrder, u"检查控制器的rotateOrder是否为xyz"),
                    ('Check for rigging publish', rigChecks.checkEloPublish, rigChecks.fixEloPublish, "检查绑定是否点击过update"),
                    ('Check & create anim control ID Tags', rigChecks.checkCtrls, u"检查控制器ID")
                ]
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

    def listCheckMenu(self):
        checklist = self.checklist()
        checkTypeMenu = QtWidgets.QMenu(self)
        self.ui.checkTypeBtn.setMenu(checkTypeMenu)

        for ctype in checklist.keys():
            item = QtWidgets.QAction(self)
            item.setText(ctype)
            item.triggered.connect(self.setCheckType)
            item.triggered.connect(self.listCheckItem)
            checkTypeMenu.addAction(item)

    def listCheckItem(self):
        self.ui.checkTree.clear()
        checklist = self.checklist()
        checkTypes = self.ui.checkTypeBtn.text()
        checkList = checklist[checkTypes]

        for i in range(len(checkList)):
            label = checkList[i][0]
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, label)
            item.setToolTip(0, str(checkList[i][-1]))
            item.setForeground(1, QtGui.QColor('lighGray'))
            item.setSizeHint(0, QtCore.QSize(18, 23))
            self.ui.checkTree.addTopLevelItem(item)

    def reloadChecks(self):
        self.listCheckMenu()
        self.listCheckItem()

    def checkItem(self, item, column):
        itemText = item.text(column)
        checkTypes = self.ui.checkTypeBtn.text()
        checklist = self.checklist()
        itemlist = [info[0] for info in checklist[checkTypes]]
        index = itemlist.index(itemText)
        self.runCheck(index)

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

        for idx in index:
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

                if len(itemlist[idx]) > 2:
                    print('\nAuto fix is available.')
                else:
                    print('\nManual fix is required.')

            QtCore.QCoreApplication.processEvents()
            mc.refresh()

        if somefailed:
            print('\n')
            mc.warning('Some checks failed.. See script editor for details.')
        else:
            print('\nEverything passed.. Go forth and publish!')

    def runFix(self):
        item = self.ui.checkTree.selectedItems()
        if not item:
            return

        checkTypes = self.ui.checkTypeBtn.text()
        checklist = self.checklist()
        itemlist = checklist[checkTypes]

        idx = self.ui.checkTree.indexOfTopLevelItem(item[0])
        if len(itemlist[idx]) > 2 and item[0].text(1) == 'FAIL':
            itemlist[idx][2]()
            self.runCheck(idx)

# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\assetCheck_ui.py .\assetCheckUI.ui
