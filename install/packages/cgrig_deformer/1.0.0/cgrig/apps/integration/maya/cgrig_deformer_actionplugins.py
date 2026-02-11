# -*- coding: utf-8 -*-
from cgrig.apps.toolpalette import palette
from cgrig.libs.maya.cmds.hotkeys import definedhotkeys
from cgrig.core import engine
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.maya.utils import mayaenv


class RiggingIconShelf(palette.ActionPlugin):
    id = "cgrig.shelf.deformer"
    creator = "Yin Yu Fei"
    tags = ["shelf", "icon"]
    uiData = {"icon": "BsMenu_shlf",
              "label": u"CgRig Deformer 工具: \n有关和deformer(eg.blendShape)相关的工具集",
              "color": "",
              "multipleTools": False,
              "backgroundColor": ""
              }

    def execute(self, *args, **kwargs):
        pass


class PoseEditerUi(palette.ActionPlugin):
    id = "cgrig.deformer.poseediterui"
    creator = "Ikura"
    uiData = {"icon": "menu_hive",
              "label": "Pose Editer UI",
              "iconColor": [
                  115,
                  187,
                  211
              ]
              }

    def execute(self, variant=None, **kwargs):
        # temp until we have a better way of handle DCC code
        from cgrig.apps.poseediterui import poseEditer
        eng = engine.currentEngine()

        parentWindow = eng.host.qtMainWindow
        if mayaenv.mayaVersion() < 2020:
            message = "Hive Only supports Maya 2020+"
            elements.MessageBox.showWarning(title="Unsupported Version",
                                            message=message, buttonB=None, parent=parentWindow)
            return


        return eng.showDialog(poseEditer.PoseEditerUI,
                              name="PoseEditerUI",
                              allowsMultiple=False,
                              showTitleBarWhenDocked=True)