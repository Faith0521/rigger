# -*- coding: utf-8 -*-
from cgrig.apps.toolpalette import palette
from cgrig.libs.maya.cmds.hotkeys import definedhotkeys

class RiggingIconShelf(palette.ActionPlugin):
    id = "cgrig.shelf.skin"
    creator = "Yin Yu Fei"
    tags = ["shelf", "icon"]
    uiData = {"icon": "JointMenu_shlf",
              "label": "CgRig Skin Tools",
              "color": "",
              "multipleTools": False,
              "backgroundColor": ""
              }

    def execute(self, *args, **kwargs):
        pass

