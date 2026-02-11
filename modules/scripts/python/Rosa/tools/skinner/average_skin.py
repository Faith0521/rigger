import maya.cmds as mc
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import averageSkin_ui
from ...maya_utils import aboutUI
reload(averageSkin_ui)

def uiShow():
    avskin = averageSkin()
    avskin.show()

class averageSkin(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(averageSkin, self).__init__(parent)

        try:
            mc.deleteUI('averageSkinUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('averageSkinUI')

        self.ui = averageSkin_ui.Ui_averageSkinUI()
        self.ui.setupUi(self)

        # singal -----------------------------------------
        self.ui.skinPer_sd.valueChanged.connect(lambda: self.ui.skinPer_sp.setValue(self.ui.skinPer_sd.value() / 10))
        self.ui.skinPer_sp.valueChanged.connect(lambda: self.ui.skinPer_sd.setValue(self.ui.skinPer_sp.value() * 10))
        self.ui.jnt_a_btn.clicked.connect( lambda: self.ui.jnt_a_line.setText(str(mc.ls(sl=1)[0])) )
        self.ui.jnt_b_btn.clicked.connect( lambda: self.ui.jnt_b_line.setText(str(mc.ls(sl=1)[0])) )
        self.ui.avSkin_btn.clicked.connect(self.average_skin_Weights_UIcmd)

    def average_skin_Weights(self, jntA, jntB, weight_value):
        verts = mc.ls(sl=True, fl=True)
        model = verts[0].split('.')[0]
        skin = mel.eval("findRelatedSkinCluster" + "(\"" + model + "\")")
        influence_jnts = mc.skinCluster(skin, q=True, inf=skin)

        for jnt in influence_jnts:
            mc.setAttr(jnt + '.liw', 1)
        mc.setAttr(jntA + '.liw', 0)
        mc.setAttr(jntB + '.liw', 0)
        mc.skinPercent(skin, verts, tv=[(jntB, 0)])

        for vert in verts:
            jntAweight = mc.skinPercent(skin, vert, t=jntA, q=True)
            weight = jntAweight * (1.0 - weight_value)
            mc.skinPercent(skin, vert, tv=[(jntB, weight)])

    def average_skin_Weights_UIcmd(self):
        jntA = self.ui.jnt_a_line.text()
        jntB = self.ui.jnt_b_line.text()
        weight_value = self.ui.skinPer_sp.value()

        # check
        if not mc.objExists(jntA) or not mc.objExists(jntB):
            return
        if not mc.nodeType(jntA) == 'joint' or not mc.nodeType(jntB) == 'joint':
            return

        self.average_skin_Weights(jntA, jntB, weight_value)

