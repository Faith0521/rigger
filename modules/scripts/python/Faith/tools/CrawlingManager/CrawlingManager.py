# coding:utf-8
from functools import partial
from imp import reload
# maya import
from PySide2 import QtCore, QtWidgets
from pymel.core import *
from maya import cmds

# ui import
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from ...maya_utils import ui_utils, controller_utils, decorator_utils, rigging_utils, node_utils
from . import crawlingUI as UI

reload(UI)


# 创建履带工具
class MainGUI(QtWidgets.QWidget, UI.Ui_Form):
    """
    main ui window
    """

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.installEventFilter(self)


class DockableCrawlingMainUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        self.gmc_layout = None
        self.uiName = "CrawlingManager"
        super(DockableCrawlingMainUI, self).__init__(parent=parent)
        self.mainUI = MainGUI()
        self.ctrl = ''  # type:str
        self.name = ''  # type:str
        self.crawlingGrp = ''  # type:str
        self.aimGrp = ''  # type:str
        self.locGrp = ''  # type:str
        self.conGrp = ''  # type:str
        self.Size = 1.00  # type:float
        self.create_window()
        self.create_layout()
        self.create_connections()

    def create_window(self):
        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Craw Manager v0.0.1")
        self.resize(300, 150)
        self.setStyleSheet(ui_utils.qss)

    def create_layout(self):
        """
        create layouts
        :return:
        """
        self.gmc_layout = QtWidgets.QVBoxLayout()
        self.gmc_layout.addWidget(self.mainUI)
        self.setLayout(self.gmc_layout)

    def create_connections(self):
        self.mainUI.load_btn.clicked.connect(self.loadCurves)
        self.mainUI.ctrl_btn.clicked.connect(self.loadCtrl)
        self.mainUI.create_btn.clicked.connect(self.createRig)

    @decorator_utils.one_undo
    def loadCtrl(self, *args):
        selection = cmds.ls(sl=True)
        if not selection: return
        self.mainUI.ctrl_le.setText(selection[0])
        self.ctrl = selection[0]

    @decorator_utils.one_undo
    def createRig(self, *args):
        """

        :param args:
        :return:
        """
        curveList = eval(self.mainUI.load_le.text())
        self.name = self.mainUI.name_le.text()
        self.Size = self.mainUI.ctrlSize_dp.value()
        mount = self.mainUI.count_spin.value()

        surface = cmds.loft(curveList[0], curveList[1], ch=0, u=1, c=0, ar=1, d=3, ss=1, rn=0, po=0, rsn=1)[0]
        surface = cmds.rename(surface, self.name + "CrawSurface")
        cmds.addAttr(self.ctrl, ln="run", k=True)

        curFromIso = cmds.createNode("curveFromSurfaceIso", n=self.name + "CurFromIso")
        cmds.setAttr(curFromIso + ".isoparmValue", 0.5)  # noqa
        cmds.connectAttr(surface + ".worldSpace[0]", curFromIso + ".inputSurface")

        curveShape = cmds.createNode("nurbsCurve", n=self.name + "IsoCurveShape")
        curveTransform = cmds.listRelatives(curveShape, p=True)[0]
        curveTransform = cmds.rename(curveTransform, self.name + "IsoCurve")
        cmds.connectAttr(curFromIso + ".outputCurve", curveShape + ".create")

        locList = []
        jointList = []
        aimNodeList = []

        if not cmds.objExists(self.name + "CrawlingGrp"):
            self.crawlingGrp = cmds.createNode("transform", name=self.name + "CrawlingGrp")
            self.aimGrp = cmds.createNode("transform", name=self.name + "AimNodeGrp", p=self.crawlingGrp)
            self.locGrp = cmds.createNode("transform", name=self.name + "locGrp", p=self.crawlingGrp)
            self.conGrp = cmds.createNode("transform", name=self.name + "conGrp", p=self.crawlingGrp)
        cmds.parent([surface, curveTransform], self.crawlingGrp)
        for i in range(mount):
            value = (1.0 / mount) * i
            loc = cmds.spaceLocator(n="%sCrawling_%d_loc" % (self.name, i))[0]
            locShape = cmds.listRelatives(loc, s=True)[0]
            cmds.setAttr(locShape + ".visibility", 0)
            jnt = cmds.createNode("joint", n="%sCrawling_%d_jnt" % (self.name, i), p=loc)

            locList.append(loc)
            jointList.append(jnt)

            cmds.addAttr(loc, ln="default_value", k=1)  # todo: create loc attributes
            cmds.setAttr(loc + ".default_value", value)
            cmds.addAttr(loc, ln="int_run", at='long', k=1)

            md = node_utils.multiply(self.ctrl + ".run", 0.01, return_plug=False, name=self.name + "CrawlingMult")
            pma = node_utils.add(a=md + ".output", b=loc + ".default_value", value_list=None, return_plug=False,
                                 name="%sCrawling_%d_Pma" % (self.name, i))
            cmds.connectAttr(pma + ".output1D", loc + ".int_run")

            pma_add = node_utils.add(a=loc + ".int_run", b=-1, value_list=None, return_plug=False,
                                     name="%sCrawling_%d_PmaIntGetAdd" % (self.name, i))

            condition_run = node_utils.if_else(pma + ".output1D",
                                               ">=",
                                               loc + ".int_run",
                                               loc + ".int_run",
                                               pma_add + ".output1D",
                                               return_plug=False,
                                               name=self.name + "CrawlingCondition")

            pma_cicle = node_utils.subtract(a=pma + ".output1D", b=condition_run + ".outColorR", value_list=None,
                                            return_plug=False,
                                            name="%sCrawling_%d_PmaIntGetCicle" % (self.name, i))

            # 创建aimConstraint节点来控制上方向和自转
            aim_node = cmds.createNode("aimConstraint", n="%sCrawling_%d_aim" % (self.name, i), p=self.aimGrp)
            aimNodeList.append(aim_node)

            motionPath = node_utils.motion(curveShape, return_plug=False, uValue=pma_cicle + ".output1D", name="%sCrawling_%d_motionPath" % (self.name, i), fractionMode=1)
            cmds.connectAttr(motionPath + ".allCoordinates", loc + ".translate")

            closestPointOnSuface_node = cmds.createNode("closestPointOnSurface",
                                                        name="%sCrawling_%d_cpos" % (self.name, i))
            cmds.connectAttr(surface + ".worldSpace[0]", closestPointOnSuface_node + ".inputSurface")
            cmds.connectAttr(loc + ".translate", closestPointOnSuface_node + ".inPosition")

            surfaceInfo_node = cmds.createNode("pointOnSurfaceInfo", name="%sCrawling_%d_posi" % (self.name, i))
            cmds.connectAttr(closestPointOnSuface_node + ".parameterU", surfaceInfo_node + ".parameterU")
            cmds.connectAttr(closestPointOnSuface_node + ".parameterV", surfaceInfo_node + ".parameterV")
            cmds.connectAttr(surface + ".worldSpace[0]", surfaceInfo_node + ".inputSurface")

            cmds.connectAttr(surfaceInfo_node + ".normal", aim_node + ".worldUpVector")
            cmds.connectAttr(surfaceInfo_node + ".tangentV", aim_node + ".target[0].targetTranslate")
            cmds.setAttr(aim_node + ".aimVector", 0, 0, 1)
            cmds.connectAttr(aim_node + ".constraintRotate", loc + ".rotate")

        cmds.parent(locList, self.locGrp)

        # create ctrl
        conJntList = []
        for i, cv in enumerate(PyNode(curveShape).cv):
            ctrl = controller_utils.Icon().create_icon(
                "Cube",
                icon_name="%sCrawCon%d_ctrl" % (self.name, i),
                icon_color=13,
                scale=(self.Size * .5, self.Size * .5, self.Size * .5)
            )[0]
            con_jnt = cmds.createNode("joint", n="%sCrawCon%d_jnt" % (self.name, i), p=ctrl)
            conJntList.append(con_jnt)
            pos = cmds.xform(cv.name(), q=True, t=True, ws=True)
            cmds.xform(ctrl, ws=True, t=pos)
            Grps = rigging_utils.GrpAdd(ctrl, [ctrl + "_zero", ctrl + "_con", ctrl + "_sdk"], "Up")[0]
            cmds.parent(Grps["zero"].name(), self.conGrp)

        cmds.skinCluster(conJntList, surface, tsb=True, nw=1, mi=1, dropoffRate=3.0, rui=False)

    @decorator_utils.one_undo
    def loadCurves(self, *args):
        selection = cmds.ls(sl=True)
        if not selection: return
        self.mainUI.load_le.setText(str(selection))


def show_guide_component_manager(*args):
    ui_utils.showDialog(DockableCrawlingMainUI, dockable=True)
