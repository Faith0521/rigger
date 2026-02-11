import os
import maya.cmds as mc
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import splitSkin_ui
from ...maya_utils import aboutUI
reload(splitSkin_ui)

def uiShow():
    avskin = splitSkin()
    avskin.show()

class splitSkin(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(splitSkin, self).__init__(parent)

        try:
            mc.deleteUI('splitSkinUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('splitSkinUI')

        self.ui = splitSkin_ui.Ui_splitSkinUI()
        self.ui.setupUi(self)

        # singal -----------------------------------------
        self.ui.loadMesh_btn.clicked.connect(lambda: self.ui.loadMesh_line.setText(str(mc.ls(sl=1)[0])))
        self.ui.splitSkin_btn.clicked.connect(self.split_skin_Weights_UIcmd)

    def split_skin_Weights(self, objlist, type, softness):
        softness = mc.softSelect(q=1, ssd=1) * softness * 2
        mc.splitSkin(objlist, type=type, r=softness)

    def split_skin_Weights_UIcmd(self):
        mesh = self.ui.loadMesh_line.text()
        jnts = mc.ls(sl=1, type='joint')
        type = self.ui.splite_type_cb.currentIndex()
        softness = self.ui.split_softness_dsb.value()
        needObjs = []

        # check
        if not mc.objExists(mesh):
            return
        try:
            shape = mc.listRelatives(mesh, c=True)[0]
            shapeType = mc.nodeType(shape, api=True)
            if shapeType == 'kMesh':
                pass
        except:
            return

        needObjs.append(mesh)
        needObjs.extend(jnts)

        # do it
        self.split_skin_Weights(needObjs, type, softness)