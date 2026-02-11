def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        from rxUi.pyside2 import tagTools_ui
        return QtCore, QtGui, QtWidgets, tagTools_ui
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            from rxUi.pyside6 import tagTools_ui
            return QtCore, QtGui, QtWidgets, tagTools_ui
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")


QtCore, QtGui, QtWidgets, tagTools_ui = get_pyside_module()

from importlib import reload
import os, shutil

import maya.cmds as mc
import controlTools
from rxCore import aboutPublic
import spaceTools
import assetEnv


####################
# Template Build UI
class TagTools(QtWidgets.QWidget):

    def __init__(self):
        super(TagTools, self).__init__()

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui = tagTools_ui.Ui_tagToolsUI()
        self.ui.setupUi(self)

        self.iconpath = os.path.join(assetEnv.geticons(), 'reload.png')
        self.ui.reloadBtn.setIcon(QtGui.QPixmap(self.iconpath))
        # self.ui.reloadBtn_2.setIcon(QtGui.QPixmap(self.iconpath))

        self.setObjectName('tagToolsUI')
        # self.ui.spaceTree_3.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        # self.ui.spaceTree_3.header().setResizeMode(1, QtGui.QHeaderView.Stretch)

        self.ui.widget_2.hide()
        self.ui.tagKeyBtn.setEnabled(0)

        self.ui.tagKeyBtn.clicked.connect(lambda: self.ui.tagKeyBtn.setEnabled(0))
        self.ui.tagSpaceBtn.clicked.connect(lambda: self.ui.tagSpaceBtn.setEnabled(0))

        self.ui.tagKeyBtn.clicked.connect(lambda: self.ui.tagSpaceBtn.setEnabled(1))
        self.ui.tagSpaceBtn.clicked.connect(lambda: self.ui.tagKeyBtn.setEnabled(1))

        self.ui.reloadBtn.clicked.connect(self.reloadAll)
        # self.ui.reloadBtn_2.clicked.connect(self.reloadAll)

        self.ui.addCtrlBtn_4.clicked.connect(self.addNewKeyableNode)
        self.ui.remCtrlBtn_4.clicked.connect(self.remKeyableNode)

        self.ui.ctrlList_6.itemSelectionChanged.connect(self.listKeyable)
        self.ui.ctrlList_5.itemSelectionChanged.connect(self.listSpaces)

        self.ui.setCbBtn.clicked.connect(self.tagFromCB)
        self.ui.addCbBtn.clicked.connect(lambda: self.tagFromCB(1))
        self.ui.remCbBtn.clicked.connect(self.removeKeyTag)

        self.ui.addCtrlBtn_3.clicked.connect(self.addNewSpaceNode)
        self.ui.remCtrlBtn_3.clicked.connect(self.remSpaceNode)
        self.ui.conBtn.clicked.connect(self.getCon)

        self.ui.spaceTree_3.header().setStyleSheet('background-color:rgb(65,65,65);')
        self.ui.spaceTree_3.setHeaderLabels(['Label', 'Space Nodes', ' '])

        self.ui.remSpaceBtn.clicked.connect(self.remSpace)
        self.ui.applySpaceBtn.clicked.connect(self.applySpaces)
        self.ui.addSpaceBtn.clicked.connect(self.addSpace)
        self.ui.checkBox.setTristate(0)

        self.ui.exportBtn.clicked.connect(self.export)
        self.ui.spaceTree_3.header().setMovable(0)
        #self.ui.defaultCmb.currentIndexChanged.connect(self.applySpaces)
        #self.ui.checkBox.stateChanged.connect(self.applySpaces)
        self.ui.downBtn.clicked.connect(lambda: self.moveSpaces(1))
        self.ui.upBtn.clicked.connect(lambda: self.moveSpaces(-1))

        self.ui.exportBtn.setText('Export Space Tags')
        self.reloadAll()

        btns = [
            self.ui.reloadBtn,

            self.ui.addCtrlBtn_4,
            self.ui.remCtrlBtn_4,
            self.ui.setCbBtn,
            self.ui.addCbBtn,
            self.ui.remCbBtn,

            self.ui.addCtrlBtn_3,
            self.ui.remCtrlBtn_3,
            self.ui.addSpaceBtn,
            self.ui.remSpaceBtn,
            self.ui.applySpaceBtn,
            self.ui.downBtn,
            self.ui.upBtn,
            self.ui.tagSpaceBtn,
            self.ui.tagKeyBtn]

        for b in btns:
            b.setMinimumHeight(25)
            b.setMaximumHeight(25)

        self.ui.tagSpaceBtn.hide()
        self.ui.tagKeyBtn.hide()

    def reloadAll(self):
        self.listKeyableNodes()
        self.listSpaceNodes()

    # KEYABLE functions ##########################################################
    def listKeyableNodes(self):
        self.ui.ctrlList_6.clear()

        filename = os.path.join(assetEnv.getpath(), 'build', 'scripts', 'customTags.py')
        if not os.path.isfile(filename):
            return
        try:
            import customTags
            reload(customTags)
            nodes = customTags.keyableNodes()
            for node in nodes:
                self.ui.ctrlList_6.addItem(node)
        except:
            pass

    def listKeyable(self):
        items = self.ui.ctrlList_6.selectedItems()
        attrs = []
        nodes = []

        for i in items:
            if not mc.objExists(i.text()):
                continue

            nodes.append(i.text())
            if not mc.objExists(i.text() + '.tagKeyable'):
                controlTools.tagKeyable(i.text(), '')

            at = mc.getAttr(i.text() + '.tagKeyable').strip().split(' ')
            for a in at:
                if a not in attrs:
                    attrs.append(a)

        self.ui.listWidget.clear()
        for a in attrs:
            item = QtWidgets.QListWidgetItem(a)
            self.ui.listWidget.addItem(item)

        mc.select(nodes)

    def addNewKeyableNode(self):
        nodes = mc.ls(sl=1)

        items = [self.ui.ctrlList_6.item(i) for i in range(self.ui.ctrlList_6.count())]
        inlist = [i.text() for i in items]

        for node in nodes:
            if not node in inlist:
                self.ui.ctrlList_6.addItem(node)

    def remKeyableNode(self):
        items = self.ui.ctrlList_6.selectedItems()
        for i in items:
            r = self.ui.ctrlList_6.row(i)
            self.ui.ctrlList_6.takeItem(r)

    def tagFromCB(self, add=False):

        nodes = [i.text() for i in self.ui.ctrlList_6.selectedItems()]
        nodes += mc.ls(sl=1)
        nodes = list(set(nodes))

        current = []
        for n in nodes:
            if mc.objExists(n + '.tagKeyable'):
                attrs = mc.getAttr(n + '.tagKeyable').split(' ')
                for a in attrs:
                    if a not in current:
                        current.append(a)

        cbAttrs = aboutPublic.getChannelBox()
        if add:
            cbAttrs = current + cbAttrs

        if nodes and cbAttrs:
            controlTools.tagKeyable(nodes, ' '.join(cbAttrs))
        self.addNewKeyableNode()
        self.listKeyable()

    def removeKeyTag(self):

        nodes = [i.text() for i in self.ui.ctrlList_6.selectedItems()]
        current = []
        for n in nodes:
            attrs = mc.getAttr(n + '.tagKeyable').split(' ')
            for a in attrs:
                if a not in current:
                    current.append(a)

        rmAttrs = [i.text() for i in self.ui.listWidget.selectedItems()]
        for a in rmAttrs:
            current.remove(a)

        current = ' '.join(current)
        if nodes and current:
            controlTools.tagKeyable(nodes, current)

        self.addNewKeyableNode()
        self.listKeyable()

    # SPACE functions ##########################################################
    def listSpaceNodes(self):
        self.ui.ctrlList_5.clear()

        filename = os.path.join(assetEnv.getpath(), 'build', 'scripts', 'customTags.py')
        if not os.path.isfile(filename):
            return
        try:
            import customTags
            reload(customTags)
            nodes = customTags.spaceNodes()
            for node in nodes:
                self.ui.ctrlList_5.addItem(node)
        except:
            pass

    def addNewSpaceNode(self):
        nodes = mc.ls(sl=1)

        items = [self.ui.ctrlList_5.item(i) for i in range(self.ui.ctrlList_5.count())]
        inlist = [i.text() for i in items]

        for node in nodes:
            if not node in inlist:
                self.ui.ctrlList_5.addItem(node)

    def remSpaceNode(self):
        items = self.ui.ctrlList_5.selectedItems()
        for i in items:
            r = self.ui.ctrlList_5.row(i)
            self.ui.ctrlList_5.takeItem(r)

    def getCon(self):
        sel = mc.ls(sl=1)
        if sel:
            self.ui.conLine.setText(sel[0])
        #self.applySpaces()

    def getSpaceNode(self):
        row = int(self.sender().objectName()[-1])
        sel = mc.ls(sl=1)
        if sel:
            self.ui.spaceTree_3.topLevelItem(row).setText(1, sel[0])
        #self.applySpaces()

    def remSpace(self):
        items = self.ui.spaceTree_3.selectedItems()
        for i in items:
            r = self.ui.spaceTree_3.indexOfTopLevelItem(i)
            self.ui.spaceTree_3.takeTopLevelItem(r)
            self.ui.defaultCmb.removeItem(r)
        #self.applySpaces()

    def listSpaces(self):

        items = self.ui.ctrlList_5.selectedItems()
        attrs = []
        nodes = []

        self.ui.spaceTree_3.clear()
        self.ui.conLine.setText('')
        self.ui.defaultCmb.clear()
        self.ui.checkBox.setChecked(0)

        if not len(items) == 1:
            return

        item = items[0]
        node = item.text()

        c = mc.ls(node + 'Grp')
        if c:
            self.ui.conLine.setText(c[0])

        if not mc.objExists:
            return

        try:
            at = mc.getAttr(node + '.tagSpaces')
            if at:
                at = at.strip().split(' ')
        except:
            return

        if not at:
            return

        if at[1].split(':')[1] == 'True' or at[1] == 'OO:1':
            oo = True
        else:
            oo = False

        dv = int(at[0].split(':')[1])
        con = at[2].split(':')[1]
        spaces = at[3:]

        sitems, i = [], 0
        for s in spaces:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, s.split(':')[0])
            item.setText(1, s.split(':')[1])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.spaceTree_3.addTopLevelItem(item)
            self.ui.defaultCmb.addItem(s.split(':')[0])

            btn = QtWidgets.QPushButton(self)
            btn.setText('Get')
            btn.setStyleSheet('background-color:rgb(65,65,65);')
            btn.setObjectName('spaceNodeBtn' + str(i))
            btn.setMaximumHeight(18)
            btn.clicked.connect(self.getSpaceNode)
            self.ui.spaceTree_3.setItemWidget(item, 2, btn)
            i += 1

        self.ui.defaultCmb.setCurrentIndex(dv)
        self.ui.conLine.setText(con)

        if oo:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState(1))
        else:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState(0))

        self.ui.checkBox.setTristate(0)
        mc.select(node)

    def addSpace(self):
        items = self.ui.ctrlList_5.selectedItems()
        if not len(items) == 1:
            return

        i = self.ui.spaceTree_3.topLevelItemCount()
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, 'Space Label')
        item.setText(1, 'Space Node')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.ui.spaceTree_3.addTopLevelItem(item)
        self.ui.defaultCmb.addItem('New Space ' + str(i))

        btn = QtWidgets.QPushButton(self)
        btn.setText('Get')
        btn.setStyleSheet('background-color:rgb(65,65,65);')
        btn.setObjectName('spaceNodeBtn' + str(i))
        btn.setMaximumHeight(18)
        btn.clicked.connect(self.getSpaceNode)
        self.ui.spaceTree_3.setItemWidget(item, 2, btn)
        #self.applySpaces()

    def applySpaces(self):

        items = self.ui.ctrlList_5.selectedItems()
        if not len(items) == 1:
            return

        node = items[0].text()

        if not mc.objExists(node):
            mc.warning('Node does not exists! ' + node)
            return

        count = self.ui.spaceTree_3.topLevelItemCount()
        items = [self.ui.spaceTree_3.topLevelItem(i) for i in range(count)]
        spaces = ''
        for i in items:
            spaces += '{0}:{1} '.format(i.text(0).replace(' ', '').strip(), i.text(1).replace(' ', '').strip())

        dv = self.ui.defaultCmb.currentIndex()
        con = self.ui.conLine.text()
        oo = bool(self.ui.checkBox.checkState())

        if not items:
            if mc.objExists(node + '.tagSpaces'):
                mc.deleteAttr(node + '.tagSpaces')
        else:
            spaceTools.tag(node, spaces, dv=dv, oo=oo, con=con)

    def moveSpaces(self, dir=1):
        items = self.ui.spaceTree_3.selectedItems()
        if not len(items) == 1:
            return

        crows = []
        for i in items:
            crows.append(self.ui.spaceTree_3.indexOfTopLevelItem(i))

        for i in range(len(crows)):
            if not crows[i] + dir > self.ui.spaceTree_3.topLevelItemCount() - 1:
                if not crows[i] + dir < 0:
                    self.ui.spaceTree_3.takeTopLevelItem(crows[i])
                    self.ui.spaceTree_3.insertTopLevelItem(crows[i] + dir, items[i])

                    btn = QtWidgets.QPushButton(self)
                    btn.setText('Get')
                    btn.setStyleSheet('background-color:rgb(65,65,65);')
                    btn.setObjectName('spaceNodeBtn' + str(i))
                    btn.setMaximumHeight(18)
                    btn.clicked.connect(self.getSpaceNode)
                    self.ui.spaceTree_3.setItemWidget(items[i], 2, btn)

        self.ui.spaceTree_3.setCurrentItem(items[-1])
        #self.applySpaces()

    def export(self):

        filename = os.path.join(assetEnv.getpath(), 'build', 'scripts', 'customTags.py')
        spaceNodes = [self.ui.ctrlList_5.item(i).text() for i in range(self.ui.ctrlList_5.count())]
        kNodes = [self.ui.ctrlList_6.item(i).text() for i in range(self.ui.ctrlList_6.count())]

        if not len(spaceNodes + kNodes):
            return

        arg = '# Load keyable attr tags\n'
        arg = 'import maya.cmds as mc\n\n'
        arg += 'def load():\n'
        for node in spaceNodes + kNodes:
            nas = []
            if mc.objExists(node + '.tagSpaces') and node in spaceNodes:
                nas.append(node + '.tagSpaces')
            if mc.objExists(node + '.tagKeyable') and node in kNodes:
                nas.append(node + '.tagKeyable')

            for n in nas:
                arg += "    try:\n"
                arg += "        mc.setAttr('{0}', '{1}', type='string')\n".format(n, mc.getAttr(n))
                arg += "    except:\n"
                arg += "        mc.warning('Could not load tag: {0}')\n".format(n)

        arg += '\treturn True\n'
        arg += '\ndef spaceNodes():\n'
        arg += '\treturn {0}\n'.format(spaceNodes)

        arg += '\ndef keyableNodes():\n'
        arg += '\treturn {0}\n'.format(kNodes)

        if os.path.isfile(filename):
            result = mc.confirmDialog(title='Overwrite Feather Build File?',
                                      message='asset_tags.py already exists.\nOverwrite file?\n\n' + filename, \
                                      button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
            if result == 'No':
                return
            shutil.copyfile(filename, filename + '.bak')

        f = open(filename, 'w')
        f.write(arg)
        f.close()

        print('Exported Tags: ' + filename)


def tagIkFkSnap(node, prefix, part):
    nodes = mc.ls(node)
    for s in nodes:
        if not mc.objExists(s + '.tagIkFkSnap'):
            mc.addAttr(s, ln="tagIkFkSnap", dt="string")
        mc.setAttr(s + '.tagIkFkSnap', l=0)
        mc.setAttr(s + '.tagIkFkSnap', 'prefix:{0} part:{1}'.format(prefix, part), type='string')


def tagIfRestorePos(node, prefix):
    nodes = mc.ls(node)
    for s in nodes:
        if not mc.objExists(s + '.tagIfRestorePos'):
            mc.addAttr(s, ln="tagIfRestorePos", at="bool")
        mc.setAttr(s + '.tagIfRestorePos', l=0)
        mc.setAttr(s + '.tagIfRestorePos', 1)