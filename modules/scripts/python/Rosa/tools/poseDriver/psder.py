import maya.cmds as mc
from PySide2 import QtCore, QtWidgets
from importlib import reload

from . import poseDriverTool
from ...maya_utils import aboutUI
from . import psd_ui
reload(psd_ui)
reload(poseDriverTool)


def uiShow():
    avskin = psder()
    avskin.show()

class psder(QtWidgets.QMainWindow):

    def __init__(self, parent=aboutUI.get_maya_window() ):
        super(psder, self).__init__(parent)

        try:
            mc.deleteUI('PsdUI', control=True)
        except RuntimeError:
            pass

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui = psd_ui.Ui_PsdUI()
        self.ui.setupUi(self)

        # singal -----------------------------------------
        self.ui.parentObj_btn.clicked.connect(lambda: self.ui.parentObj_line.setText(mc.ls(sl=1)[0]))
        self.ui.followObj_btn.clicked.connect(lambda: self.ui.followObj_line.setText(mc.ls(sl=1)[0]))
        self.ui.createPsd_btn.clicked.connect(self.createPsd)

    def createPsd(self):
        # topeNode
        topNode = 'Psd_System'
        if not mc.objExists(topNode):
            mc.createNode('transform', n=topNode)

        parentObj = self.ui.parentObj_line.text()
        followObj = self.ui.followObj_line.text()
        axis = self.ui.axis_cb.currentText()
        psdScale = self.ui.scalePSD_dsb.value()

        axisAttrMirror = False
        renameAttr = True
        if self.ui.lside_rb.isChecked():
            axisAttrMirror = False
            renameAttr = False
        if self.ui.rside_rb.isChecked():
            axisAttrMirror = True
            renameAttr = False
        if self.ui.mside_rb.isChecked():
            axisAttrMirror = False
            renameAttr = True

        if mc.objExists(parentObj) and mc.objExists(followObj) and not mc.objExists(followObj + '_psd_parent_handle'):
            psd = poseDriverTool.createBridge(followObj, axis=axis, mirror=axisAttrMirror)
            poseDriverTool.scaleBridge(followObj, psdScale)
            poseDriverTool.constraintBridge(parentObj=parentObj, followObj=followObj, parentHandle=psd['parent'], followHandle=psd['follow'])
            mc.parent(psd['parent'], topNode)

            if renameAttr:
                orgDriverAttrsDict = {'inner': 'R_side', 'outer': 'L_side',
                                      'outerFront': 'L_side_Front', 'outerBack': 'L_side_Back',
                                      'innerFront': 'R_side_Front', 'innerBack': 'R_side_Back'}
                for key in orgDriverAttrsDict.keys():
                    try:
                        if mc.objExists(psd['cmd']):
                            mc.renameAttr(psd['cmd'] + '.' + key, orgDriverAttrsDict[key])
                    except:
                        pass