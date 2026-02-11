# -*- coding: utf-8 -*-
from cgrig.apps.toolpalette import palette
from cgrig.core.engine import currentEngine
from cgrig.apps.preferencesui import preferencesui


class PreferencesUi(palette.ActionPlugin):
    id = "cgrig.preferencesui"
    creator = "Dave Sparrow"
    tags = ["preference"]
    uiData = {"icon": "menu_cgrig_preferences",
              "tooltip": "CgRig Tools Preferences",
              "label": "CgRig Tools Preferences: \nOpens the CgRig Preferences Window.",
              "color": "",
              "backgroundColor": "",
              "multipleTools": False,
              "dock": {"dockable": True, "tabToControl": ("AttributeEditor", -1), "floating": False}
              }

    def execute(self, *args, **kwargs):
        engine = currentEngine()
        return engine.showDialog(windowCls=preferencesui.PreferencesUI,
                                 name="PreferencesUI",
                                 allowsMultiple=False)
