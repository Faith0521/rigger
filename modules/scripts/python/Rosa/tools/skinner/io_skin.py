import maya.cmds as mc
import maya.mel as mel
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import IoSkin_ui
from . skinIO import skinUtils
from ...maya_utils import aboutUI

reload(IoSkin_ui)

def uiShow():
    iSkin = IoSkin()
    iSkin.show()

class IoSkin(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(IoSkin, self).__init__(parent)

        try:
            mc.deleteUI('IoSkinUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName('IoSkinUI')

        self.ui = IoSkin_ui.Ui_IoSkinUI()
        self.ui.setupUi(self)

        self.skinManager = skinUtils.SkinIO()
        # singal -----------------------------------------
        self.ui.selectSkinJnts_btn.clicked.connect(self.selectSkinJnts_UIcmd)
        self.ui.exportSkin_btn.clicked.connect(self.exportSkin_UIcmd)
        self.ui.importSkin_btn.clicked.connect(self.importSkin_UIcmd)

    def searchSkinCluster(self, obj=None):
        if obj is None:
            obj = mc.ls(sl=1)[0]

        skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + obj + "\")")
        if skinNode != '':
            return skinNode
        else:
            return False

    def selectSkinJnts_UIcmd(self):
        # select skin object/
        mesh = mc.ls(sl=True, ap=1)[0]
        if len(mesh) == 0:
            mc.error(' You should select one skin object ! ')
        else:
            skinNode = self.searchSkinCluster(mesh)
            skinJoints = mc.skinCluster(skinNode, q=True, inf=True)
            mc.select(skinJoints)

    def exportSkin_UIcmd(self):
        # use maya fileDialog2/
        setPath = mc.fileDialog2(fm=0, okc='Save', fileFilter="*.zip")
        if setPath is not None:
            outputPath = setPath[0]
        else:
            mc.warning('can not find save file path')
            return

        if len(outputPath) == 0:
            return
        self.skinManager.skinHandler = str(self.ui.injectionMode_cb.currentText())
        self.skinManager.exportAssetWeights(mc.ls(sl=True),
                                            outputPath,
                                            exposeWeightDetails=True)

        report = self.skinManager.skinProcessor.batchProcessing.report
        print (report)

    def importSkin_UIcmd(self):
        # use maya fileDialog2/
        setPath = mc.fileDialog2(fm=1, okc='Load', fileFilter="*.zip")
        if setPath is not None:
            outputPath = setPath[0]
        else:
            mc.warning('can not find load file path')
            return
        if len(outputPath) == 0:
            return

        self.skinManager.importAssetWeights(outputPath,
                                            exposeWeightDetails=True)

        report = self.skinManager.skinProcessor.batchProcessing.report
        print (report)