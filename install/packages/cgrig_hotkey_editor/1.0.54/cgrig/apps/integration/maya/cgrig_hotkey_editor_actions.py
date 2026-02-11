# -*- coding: utf-8 -*-
from cgrig.apps.toolpalette import palette


class HotkeyEditorUi(palette.ActionPlugin):
    id = "cgrig.hotkeyeditorui"
    creator = "Keen Foong"
    tags = ["hotkey", "hotkeys", "editor"]
    uiData = {"icon": "menu_keyboard",
              "label": "CgRig Hotkey Editor",
              "tooltip": "CgRig Hotkey Editor: \nLoad, edit and create CgRig Tools hotkey sets.",
              "label": "Hotkey Editor"
              }

    def execute(self, *args, **kwargs):
        from cgrig.apps.hotkeyeditor import hotkeyeditorui
        from cgrig.core.engine import currentEngine

        engine = currentEngine()
        return engine.showDialog(windowCls=hotkeyeditorui.HotkeyEditorUI,
                                 name="HotkeyEditor",
                                 allowsMultiple=False)
