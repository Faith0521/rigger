import maya.cmds as mc
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import pruneSkin_ui
from . import limitSkin
from ...maya_utils import aboutUI
reload(pruneSkin_ui)

def uiShow():
    avskin = pruneSkin()
    avskin.show()

class pruneSkin(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(pruneSkin, self).__init__(parent)

        try:
            mc.deleteUI('pruneSkinUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('pruneSkinUI')

        self.ui = pruneSkin_ui.Ui_pruneSkinUI()
        self.ui.setupUi(self)

        self.limiter = limitSkin.LimitSkinWeightClss()
        # singal -----------------------------------------
        self.ui.greater_btn.clicked.connect(self.checkGreater_UIcmd)
        self.ui.equal_btn.clicked.connect(self.checkEqual_UIcmd)
        self.ui.less_btn.clicked.connect(self.checkLess_UIcmd)
        self.ui.setSkinLimit_btn.clicked.connect(self.setSkinLimit_UIcmd)
        self.ui.prune_gb.clicked.connect(self.pruneWeightOptions_UIcmd)

    def setSkinLimit_UIcmd(self):
        limitNum = self.ui.limit_sb.value()
        decimalNum = self.ui.decimal_sb.value()
        self.limiter.setLimit(limitNum, decimalNum)

    def checkGreater_UIcmd(self):
        limitNum = self.ui.limit_sb.value()
        self.limiter.checkSkinLimitStyle(limitNum, style=0)

    def checkEqual_UIcmd(self):
        limitNum = self.ui.limit_sb.value()
        self.limiter.checkSkinLimitStyle(limitNum, style=1)

    def checkLess_UIcmd(self):
        limitNum = self.ui.limit_sb.value()
        self.limiter.checkSkinLimitStyle(limitNum, style=2)

    def pruneWeightOptions(self, pruneBelow):
        # pruneBelow = 0.1
        unlockInfluence = 1
        mel.eval('doPruneSkinClusterWeightsArgList %d { "%s" }' % (unlockInfluence, str(pruneBelow)))

    def pruneWeightOptions_UIcmd(self):
        pruneBelow = self.ui.smallWeight_sp.value()
        self.pruneWeightOptions(pruneBelow)