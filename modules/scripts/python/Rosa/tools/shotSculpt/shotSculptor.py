#Loading......
import maya.cmds as mc
import maya.mel as mel
from importlib import reload
from PySide2 import QtCore, QtGui, QtWidgets
from ...maya_utils import aboutUI
from . import shotSculpt_ui

reload(shotSculpt_ui)

# &"C:\Program Files\Autodesk\Maya2025\bin\uic" -g python .\shotSculpt_UI.ui -o .\shotSculpt_ui.py
# &"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2018\bin\pyside2-uic" -o .\shotSculpt_ui.py .\shotSculpt_UI.ui

def uiShow():
    mtxc = shotSculptCmd()
    mtxc.show()

class editBtnWidget(QtWidgets.QWidget):
    def __init__(self, layerItem, frameItem, shadercb, grabcb, parent=None):
        super(editBtnWidget, self).__init__(parent)
        self.layerItem = layerItem
        self.frameItem = frameItem
        self.shaderCB = shadercb
        self.grabCB = grabcb
        self.dln = self.layerItem.text(0)
        self.time = self.frameItem.text(1)
        self.bss = mc.getAttr(self.dln + '.bss')
        self.ifos = mc.getAttr(self.dln + '.ifos')
        self.shaders = eval(mc.getAttr(self.dln + '.shaders'))

        self.button = QtWidgets.QPushButton('Edit', self)
        self.button.setFixedSize(30, 18)

        # signal
        self.button.clicked.connect(lambda: self.toggle_button(self.button))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtGui.Qt.AlignLeft)
        self.layout.addWidget(self.button)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # init data
        self.resolveButtonStatus(self.button)

    def getIndexByName(self, blsNode, targetName):
        attr = blsNode + '.w[{}]'
        weightCount = mc.blendShape(blsNode, q=True, wc=True)
        for index in range(weightCount):
            if mc.aliasAttr(attr.format(index), q=True) == targetName:
                return index
        return -1

    def _updateEditStatusData(self, dln, editStatusData):
        mc.setAttr(dln + '.editStatus', lock=False)
        mc.setAttr(dln + '.editStatus', editStatusData, type='string')
        mc.setAttr(dln + '.editStatus', lock=True)

    def resolveButtonStatus(self, button):
        if not self.dln:
            return
        editStatus = eval(mc.getAttr(self.dln + '.editStatus'))

        if editStatus['frame_' + self.time] == 0:
            button.setStyleSheet("")
        else:
            button.setStyleSheet("background-color: red")

    def toggle_button(self, button):
        # use data
        if not self.dln:
            return
        editStatusData = eval(mc.getAttr(self.dln + '.editStatus'))

        # toggle --------------------------------------------------------------
        if button.styleSheet():
            button.setStyleSheet("")

            for bs in self.bss:
                mc.sculptTarget(bs, e=True, t=-1)

            # sculpt shader
            if self.shaderCB.isChecked():
                for key in self.shaders:
                    shape = key
                    org_mat = self.shaders[key]['orgShader']
                    new_mat = self.shaders[key]['sculptShader']
                    self.toggle_material(shape, org_mat, new_mat)

            mc.select(cl=True)
            # maya sculpt tool
            if self.grabCB.isChecked():
                try:
                    mc.setToolTo('selectSuperContext')
                except Exception as e:
                    print(f"Failed to set select tool: {e}")

            # edit status
            editStatusData['frame_' + self.time] = 0
            self._updateEditStatusData(self.dln, editStatusData)

        else:
            button.setStyleSheet("background-color: red")

            mc.currentTime(int(self.time), e=True)
            # sculptTargetMode for all blendshapes
            for bs in self.bss:
                targetName = 'frame_' + str(self.time)
                index = self.getIndexByName(bs, targetName)
                mc.sculptTarget(bs, e=True, t=index)

            # sculpt shader
            if self.shaderCB.isChecked():
                for key in self.shaders:
                    shape = key
                    org_mat = self.shaders[key]['orgShader']
                    new_mat = self.shaders[key]['sculptShader']
                    self.toggle_material(shape, org_mat, new_mat)

            mc.select(self.ifos)
            # maya sculpt tool
            if self.grabCB.isChecked():
                mel.eval("SetMeshGrabTool")

            # edit status
            editStatusData['frame_' + self.time] = 1
            self._updateEditStatusData(self.dln, editStatusData)

    def toggle_material(self, shape, org_mat, new_mat):
        # get current shader
        shading_groups = mc.listConnections(shape, type='shadingEngine')
        if not shading_groups:
            mc.warning('No shading group found for the {0}'.format(shape))
            return
        current_mat = mc.ls(mc.listConnections(shading_groups), materials=True)[0]

        # switch shader
        if current_mat == org_mat:
            mc.select(shape)
            mc.hyperShade(assign=new_mat)
        else:
            mc.select(shape)
            mc.hyperShade(assign=org_mat)


class shotSculptCmd(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window()):
        super(shotSculptCmd, self).__init__(parent)

        try:
            mc.deleteUI('shot_sculpt_ui', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = shotSculpt_ui.Ui_shot_sculpt_ui()
        self.ui.setupUi(self)

        # data
        self.characterSuffix = '_sculpt'
        self.sculptPrefix = 'frame'
        self.ssShader = 'shotSculptShader'
        self.is_expanded = True

        # signal
        self.ui.stree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.stree.customContextMenuRequested.connect(self.sculptTreeMenu)
        self.ui.ccd_btn.clicked.connect(self.createCharacterNode)

        self.ui.stree.itemChanged.connect(self.stree_item_changed)
        self.ui.stree.itemClicked.connect(self.stree_item_clicked)
        self.ui.stree.itemDoubleClicked.connect(self.stree_item_double_clicked)

        self.ui.refresh_tree_btn.clicked.connect(self.resolveScupltList_forUI)
        self.ui.layer_oc_btn.clicked.connect(self.toggle_items_expanded_collapse)

        self.ui.easyin_sp.valueChanged.connect(self.editAnimCurve)
        self.ui.holdin_sp.valueChanged.connect(self.editAnimCurve)
        self.ui.holdout_sp.valueChanged.connect(self.editAnimCurve)
        self.ui.easyout_sp.valueChanged.connect(self.editAnimCurve)

        # init ui
        self.ui.refresh_tree_btn.setIcon(QtGui.QPixmap(":/refresh.png"))
        self.ui.layer_oc_btn.setIcon(QtGui.QPixmap(":/layerEditor.png"))

        self.ui.grab_cb.setChecked(0)
        self.ui.grab_cb.hide()
        self.ui.shader_cb.setChecked(0)
        self.ui.stree.setColumnCount(3)  # 设置列数
        self.ui.stree.setHeaderLabels(['Name', 'Frame', 'Enabled'])
        self.ui.stree.setColumnWidth(0, 200)


        # init data
        self.createSculptShader()
        self.resolveScupltList_forUI()
        mc.scriptJob(p=self.objectName(), e=['PreFileNewOrOpened', self.resolveScupltList_forUI])

    def createSculptShader(self):
        if not mc.objExists(self.ssShader):
            mc.shadingNode('lambert', asShader=True, name=self.ssShader)
            mc.setAttr(f"{self.ssShader}.color", 0.254, 0.331, 0.431, type='double3')


    def stree_item_changed(self, item, column):
        if column == 2:
            if item.checkState(column) == QtCore.Qt.Checked:
                mc.setAttr(item.text(0) + '.envelope', 1)
            else:
                mc.setAttr(item.text(0) + '.envelope', 0)

    def stree_item_clicked(self, item):
        if item.parent() is not None and item.parent().parent() is not None:
            dln = item.parent().text(0)
            if not mc.objExists(dln):
                return
            mc.select(dln)

    def stree_item_double_clicked(self, item):
        if item.parent() is not None and item.parent().parent() is None:
            dln = item.text(0)
            if not mc.objExists(dln):
                return
            mc.select(dln)

    #def qtreeOpenClose()
    def resolveScupltList_forUI(self):
        self.ui.stree.clear()

        # add character item
        characterNodes = mc.ls('*{0}'.format(self.characterSuffix))
        for node in characterNodes:
                characterItem = QtWidgets.QTreeWidgetItem(self.ui.stree)
                characterItem.setText(0, node)
                characterItem.setIcon(0, QtGui.QPixmap(":/out_character.png"))

                # add deformer layers item
                deformerLayers = mc.listRelatives(node, children=True)
                if deformerLayers:
                    for layer in deformerLayers:
                        layerItem = QtWidgets.QTreeWidgetItem(characterItem)
                        layerItem.setText(0, layer)
                        layerItem.setIcon(0, QtGui.QPixmap(":/out_layeredTexture.png"))

                        # check deformer envelope on/off
                        if mc.getAttr(layerItem.text(0) + '.envelope') == 1:
                            layerItem.setCheckState(2, QtCore.Qt.Checked)
                        else:
                            layerItem.setCheckState(2, QtCore.Qt.Unchecked)

                        # add frames item
                        layerAttrs = mc.listAttr(layer, userDefined=True)
                        frames = [item for item in layerAttrs if self.sculptPrefix in item]
                        for frame in frames:
                            frameItem = QtWidgets.QTreeWidgetItem(layerItem)
                            frameItem.setText(0, self.sculptPrefix)
                            frameItem.setText(1, str(frame.split('_')[1]))
                            frameItem.setIcon(0, QtGui.QPixmap(":/teAdditive.png"))

                            # add edit button
                            btn_widget = editBtnWidget(layerItem, frameItem, self.ui.shader_cb, self.ui.grab_cb)
                            self.ui.stree.setItemWidget(frameItem, 2, btn_widget)

        self.ui.stree.expandAll()


    def sculptTreeMenu(self, position):

        # 获取当前点击的项
        item = self.ui.stree.itemAt(position)
        if item:
            level = 0
            current_item = item
            while current_item.parent():
                current_item = current_item.parent()
                level += 1

            # right key
            menu = QtWidgets.QMenu(self)

            # different right key for different item level
            if level == 0:
                actionA = QtWidgets.QAction("create deformer layer", self.ui.stree)
                actionA.triggered.connect(lambda: self.createDeformerLayer(item))
                menu.addAction(actionA)

                actionB = QtWidgets.QAction("delete character", self.ui.stree)
                actionB.triggered.connect(lambda: self.delCharacterNode(item))
                menu.addAction(actionB)

            elif level == 1:
                actionA = QtWidgets.QAction("add deformer", self.ui.stree)
                actionA.triggered.connect(lambda: self.addDeformerOnFrame(item))
                menu.addAction(actionA)

                actionB = QtWidgets.QAction("delete layer", self.ui.stree)
                actionB.triggered.connect(lambda: self.delDeformerLayer(item))
                menu.addAction(actionB)

            elif level == 2:
                actionA = QtWidgets.QAction("delete deformer", self.ui.stree)
                actionA.triggered.connect(lambda: self.delDeformerOnFrame(item))
                menu.addAction(actionA)

            # display
            menu.exec_(self.ui.stree.viewport().mapToGlobal(position))

    def toggle_items_expanded_collapse(self):
        if self.is_expanded:
            self.set_all_items_expanded(False)
            #self.toggle_button.setText("Expand All")
        else:
            self.set_all_items_expanded(True)
            #self.toggle_button.setText("Collapse All")
        self.is_expanded = not self.is_expanded

    def set_all_items_expanded(self, expanded):
        root = self.ui.stree.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            self.expand_or_collapse_item(item, expanded)

    def expand_or_collapse_item(self, item, expanded):
        if expanded:
            self.ui.stree.expandItem(item)
        else:
            self.ui.stree.collapseItem(item)

        child_count = item.childCount()
        for i in range(child_count):
            child = item.child(i)
            self.expand_or_collapse_item(child, expanded)

    def createCharacterNode(self):
        characterName = aboutUI.promptDialogWin(titleDialog='characterName', instrunctions='Character:', buttons=['OK', 'Cancel'], text=None)
        if characterName:
            mc.createNode('transform', n=characterName + self.characterSuffix)
            self.resolveScupltList_forUI()

    def createDeformerLayer(self, item):

        sel = mc.ls(sl=True)
        selSize = len(sel)

        ##Run error Checks
        if selSize < 1:
            mc.error('No objects selected')
        for s in sel:
            if mc.filterExpand(sm=12, fp=True) is None:
                mc.error('{0} is not a mesh object. Cannot create a deformer layer.'.format(s), noContext=True)

            shapes = mc.listRelatives(s, shapes=True)
            if not shapes:
                mc.error('{0} is not a mesh object. Cannot create a deformer layer.'.format(s), noContext=True)

        ##get the name of the new node
        result = mc.promptDialog(
            title='create Shot Sculpt Node',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        # dln : deformerLayerNode
        if result == 'OK':
            name = mc.promptDialog(q=True, t=True)
            characterNode = item.text(0)
            dln = mc.createNode('transform', n=name + '_deformerlayer', p=characterNode)

            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
                channel = dln + '.' + attr
                mc.setAttr(channel, l=True, k=False, cb=False)

            ##store the influence objects and blendshapes
            mc.addAttr(dln, longName='ifos', dt='stringArray', k=False)
            mc.addAttr(dln, longName='bss', dt='stringArray', k=False)
            mc.addAttr(dln, longName='shaders', dt='string', k=False)
            mc.addAttr(dln, longName='editStatus', dt='string', k=False)
            mc.addAttr(dln, longName='envelope', at='float', hasMinValue=True, min=0, hasMaxValue=True, max=1, k=True, dv=1)

            selArray = []
            BssArray = []
            for i in range(selSize):
                ##add the selection to the array
                selArray.append(sel[i])
                bsName = sel[i] + '_' + dln + '_bs'

                ##create a blendshape
                mc.blendShape(sel[i], n=bsName, foc=False)
                BssArray.append(bsName)
                mc.connectAttr(dln + '.envelope', BssArray[i] + '.envelope')

            mc.setAttr(dln + '.ifos', type='stringArray', *([len(selArray)] + selArray))
            mc.setAttr(dln + '.bss', type='stringArray', *([len(BssArray)] + BssArray))

            # shape data
            ifos = mc.getAttr(dln + '.ifos')
            shadersDict = {}
            ifosShapes = [mc.listRelatives(ifo, s=True, ni=True)[0] for ifo in ifos]
            for shape in ifosShapes:
                shaderDict = {}
                shading_groups = mc.listConnections(shape, type='shadingEngine')
                current_mat = mc.ls(mc.listConnections(shading_groups), materials=True)[0]
                shaderDict['orgShader'] = current_mat
                shaderDict['sculptShader'] = self.ssShader
                shadersDict[shape] = shaderDict
            mc.setAttr(dln + '.shaders', shadersDict, type='string')
            mc.setAttr(dln + '.shaders', lock=True)

            # edit status
            self.updateEditStatusData(dln, editStatusData={})

            # support ui
            layerItem = QtWidgets.QTreeWidgetItem(item)
            layerItem.setText(0,dln)
            layerItem.setIcon(0, QtGui.QPixmap(":/out_layeredTexture.png"))
            layerItem.setCheckState(2, QtCore.Qt.Checked)
            self.ui.stree.expandAll()

    def updateEditStatusData(self, dln, editStatusData):
        mc.setAttr(dln + '.editStatus', lock=False)
        mc.setAttr(dln + '.editStatus', editStatusData, type='string')
        mc.setAttr(dln + '.editStatus', lock=True)

    def addDeformerOnFrame(self, item):
        layerItem = item
        #layerItem = self.ui.stree.selectedItems()[0]
        dln = self.ui.stree.selectedItems()[0].text(0)
        if not mc.objExists(dln):
            return

        ifos = mc.getAttr(dln + '.ifos')
        bss = mc.getAttr(dln + '.bss')

        #create a new tangentSpace blendshapes
        time = int(mc.currentTime(query=True))
        frameName = self.sculptPrefix + '_' + str(time)
        mc.addAttr(dln, longName=frameName, at="float", hasMinValue=True, min=0, hasMaxValue=True, max=1, k=True, dv=1)
        dlnFrameAttr = dln + "." + frameName

        # edit status
        editStatusData = eval(mc.getAttr(dln + '.editStatus'))
        editStatusData[frameName] = 0
        self.updateEditStatusData(dln, editStatusData)

        ##add new frame attr to the UI -------------------------------------------------------
        frameItem = QtWidgets.QTreeWidgetItem(layerItem)
        frameItem.setText(0, self.sculptPrefix)
        frameItem.setText(1, str(time))
        frameItem.setIcon(0, QtGui.QPixmap(":/teAdditive.png"))
        # add edit button
        btn_widget = editBtnWidget(layerItem, frameItem, self.ui.shader_cb, self.ui.grab_cb)
        self.ui.stree.setItemWidget(frameItem, 2, btn_widget)
        self.ui.stree.expandAll()

        for i in range(len(ifos)):
            ##create a new Blendshape and connect all attrs to dln
            bsIndex = mc.blendShape(bss[i], q=True, wc=True)

            ##create a temporary targetObj
            bs_target = mc.duplicate(ifos[i], name=ifos[i]+'_sc')

            mc.blendShape(bss[i], edit=True, tangentSpace=True, tc=True, t=[ifos[i], bsIndex, bs_target[0], 1])
            mc.blendShape(bss[i], e=True, rtd=(0, bsIndex))
            mc.aliasAttr(frameName, bss[i] + '.w[' + str(bsIndex) + ']')

            #delete the tempory obj
            mc.delete(bs_target)
            mc.connectAttr(dlnFrameAttr, bss[i] + "." + frameName)

        # auto key
        self.autoKey(dlnFrameAttr, time)

    def _getIndexByName(self, blsNode, targetName):
        attr = blsNode + '.w[{}]'
        weightCount = mc.blendShape(blsNode, q=True, wc=True)
        for index in range(weightCount):
            if mc.aliasAttr(attr.format(index), q=True) == targetName:
                return index
        return -1

    def delCharacterNode(self, item):
        characterNode = item.text(0)
        if not mc.objExists(characterNode):
            return

        result = mc.confirmDialog(
            title='Delete Character Node',
            message='Are you sure you want to delete ' + characterNode + "?",
            button=['Yes', 'No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No')

        if result == 'Yes':
            while item.childCount() > 0:
                child = item.child(0)
                self.delDeformerLayer(child, skipWarning=False)

            # support ui
            index = self.ui.stree.indexOfTopLevelItem(item)
            self.ui.stree.takeTopLevelItem(index)
            # delete self
            mc.delete(characterNode)

    def delDeformerLayer(self, item, skipWarning=True):
        parentItem = item.parent()
        if not parentItem:
            return

        characterNode = parentItem.text(0)
        dln = item.text(0)

        if not mc.objExists(characterNode):
            return

        if skipWarning:
            result = mc.confirmDialog(
                title='Delete Sculpt-Frame',
                message='Are you sure you want to delete ' + dln + "?",
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No')
        else:
            result = 'Yes'

        if result == 'Yes':
            # delete root bs node
            bss = mc.getAttr(dln + '.bss')
            for bs in bss:
                mc.delete(bs)

            # delete deformer layer node
            mc.delete(dln)

            # delete ui items
            while item.childCount() > 0:
                child = item.child(0)
                item.removeChild(child)
            parentItem.removeChild(item)

    def delDeformerOnFrame(self, item, skipWarning=True):
        parentItem = item.parent()
        if not parentItem:
            return

        dln = parentItem.text(0)
        if not mc.objExists(dln):
            return

        bss = mc.getAttr(dln + '.bss')
        frame = item.text(0) + '_' + str(item.text(1))

        if skipWarning:
            result = mc.confirmDialog(
                title='Delete Sculpt-Frame',
                message='Are you sure you want to delete ' + frame + "?",
                button=['Yes', 'No'],
                defaultButton='Yes',
                cancelButton='No',
                dismissString='No')
        else:
            result = 'Yes'

        if result == 'Yes':
            for bs in bss:
                index = self._getIndexByName(bs, frame)
                # delete the target
                mc.removeMultiInstance(bs + '.weight[' + str(index) + ']', b=True)
                # remove the bs attr
                mc.aliasAttr(bs + '.' + frame, remove=True)

            mc.deleteAttr(dln + '.' + frame)
            parentItem.removeChild(item)

    def autoKey(self, attr, time):
            ##Get attrs from ui
            easeInFrames = int(self.ui.easyin_sp.text())
            holdInFrames = int(self.ui.holdin_sp.text())
            holdOutFrames = int(self.ui.holdout_sp.text())
            easeOutFrames = int(self.ui.easyout_sp.text())
            InTangentType = self.ui.easyin_cmb.currentText()
            OutTangentType = self.ui.easyout_cmb.currentText()

            # clean keys
            mc.cutKey(attr.split('.')[0], attribute=attr.split('.')[1], time=(":",))

            # do keys
            mc.setKeyframe(attr, v=1, t=time, inTangentType=InTangentType, outTangentType=OutTangentType)

            if easeInFrames > 0:
                mc.setKeyframe(attr, v=0, t=[time - easeInFrames - holdInFrames], outTangentType=InTangentType)
            if holdInFrames > 0:
                mc.setKeyframe(attr, v=1, t=(time - holdInFrames), inTangentType=InTangentType, outTangentType=InTangentType)
            if holdOutFrames > 0:
                mc.setKeyframe(attr, v=1, t=(time + holdOutFrames), inTangentType=OutTangentType, outTangentType=OutTangentType)
            if easeOutFrames > 0:
                mc.setKeyframe(attr, v=0, t=[time + easeOutFrames + holdOutFrames], inTangentType=OutTangentType)

    def editAnimCurve(self):
        frameItem = self.ui.stree.selectedItems()[0]
        if 'frame' not in frameItem.text(0):
            mc.warning('No Frame deformer selected')
            return

        dln = frameItem.parent().text(0)
        time = frameItem.text(1)

        if len(time) < 1:
            mc.warning('No Frame selected')
            return

        attr = dln + '.' + frameItem.text(0) + '_' + time
        self.autoKey(attr, int(time))