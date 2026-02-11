import os
import maya.cmds as mc
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import smoothSkinPainter_ui
from ...maya_utils import aboutUI
reload(smoothSkinPainter_ui)

def uiShow():
    sspSkin = smoothSkinPainter()
    sspSkin.show()

class smoothSkinPainter(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(smoothSkinPainter, self).__init__(parent)

        try:
            mc.deleteUI('IoSkinUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('IoSkinUI')

        self.ui = smoothSkinPainter_ui.Ui_smoothSkinPainterUI()
        self.ui.setupUi(self)

        # singal -----------------------------------------
        self.ui.smoothBrush_btn.clicked.connect(self.bm_smoothSkinBrush_UIcmd)
        self.loadNeedPlug()

    def whereAmI(self):
        scriptPath = (os.path.split(os.path.abspath(__file__)))
        toolPath = scriptPath[0].replace('\\', '/')
        return toolPath

    def loadNeedPlug(self):
        smoothSkinBrushPlug = self.whereAmI() + '/smoothSkinBrush/bm_smoothSkinWeightBrushCmd.py'
        if not mc.pluginInfo(smoothSkinBrushPlug, query=True, loaded=True):
            mc.loadPlugin(smoothSkinBrushPlug)

    def bm_smoothSkinBrush_UIcmd(self):
        smoothSkinBrushPath = self.whereAmI() + '/smoothSkinBrush'
        print(smoothSkinBrushPath)
        mel.eval('source "{0}/bm_smoothSkinWeightBrush.mel"'.format(smoothSkinBrushPath))