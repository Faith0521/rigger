# -*- coding: utf-8 -*-
import os
from maya import cmds
from cgrig.apps.toolpalette import palette
from cgrig.core import engine

from cgrig.core import api
from cgrig.libs.maya.qt import mayaui
from cgrigvendor.Qt import QtWidgets
from cgrig.apps.toolpalette import run
from cgrig.libs.utils import output


class InstallPackageZip(palette.ActionPlugin):
    id = "cgrig.packages.installZip"
    creator = "David Sparrow"
    tags = ["package"]
    uiData = {"icon": "downloadCircle",
              "tooltip": "Allows Install cgrig packages from Zip",
              "label": "Install CgRig Package",
              }

    def execute(self, *args, **kwargs):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(mayaui.mayaWindow(),
                                                            "Set the Zip file to load",
                                                            os.path.expanduser("~"),
                                                            "*.zip")
        if filePath:
            installed = api.currentConfig().runCommand("installPackage", ["--path", filePath])
            if not installed:
                output.displayWarning("No CgRig packages found in {}".format(filePath))
                return
            run.currentInstance().executePluginById(Reload.id)

class TriggerStateToggle(palette.ActionPlugin):
    id = "cgrig.triggers.state"
    creator = "David Sparrow"
    tags = ["triggers"]
    _requiresAutoStartup = bool(int(os.getenv("CGRIG_TRIGGERS_STARTUP", "1")))
    uiData = {"icon": "menu_reload",
              "tooltip": "Toggles the state of triggers, if off then marking menus will no longer operate",
              "label": "Trigger Toggle",
              "color": "",
              "backgroundColor": "",
              "isCheckable": True,
              "isChecked": _requiresAutoStartup,
              "multipleTools": False,
              "loadOnStartup": _requiresAutoStartup
              }

    def execute(self, state):
        from cgrig.libs.maya import triggers
        if state:
            # turn on the triggers
            triggers.setupMarkingMenuTrigger()
            triggers.createSelectionCallback()
            return
        # remove the triggers
        triggers.resetMarkingMenuTrigger()
        triggers.removeSelectionCallback()

    def teardown(self):
        from cgrig.libs.maya import triggers
        # remove the triggers
        triggers.resetMarkingMenuTrigger()
        triggers.removeSelectionCallback()


class MayaToolTipsToggle(palette.ActionPlugin):
    id = "cgrig.help.tooltips"
    creator = "Keen Foong"
    tags = ["toggle"]
    uiData = {"icon": "menu_reload",
              "tooltip": "Toggle Maya Tooltips",
              "label": "Toggle Maya Tooltips",
              "color": "",
              "backgroundColor": "",
              "isCheckable": True,
              "isChecked": True,
              "multipleTools": False,
              "loadOnStartup": True
              }

    def __init__(self, *args, **kwargs):
        from cgrig.libs.maya.utils import tooltips
        self.uiData['isChecked'] = tooltips.tooltipState()
        super(MayaToolTipsToggle, self).__init__(*args, **kwargs)

    def execute(self, state):
        """ Execute toggle

        :param state:
        :return:
        """
        from cgrig.libs.maya.utils import tooltips
        tooltips.setMayaTooltipState(state)


class UninstallerUi(palette.ActionPlugin):
    id = "cgrig.uninstaller"
    creator = "Keen Foong"
    tags = ["toggle"]
    uiData = {"icon": "trash",
              "tooltip": "Uninstall CgRigToolsPro",
              "label": "Uninstall CgRigToolsPro",
              "color": "",
              "backgroundColor": "",
              }

    def execute(self, *args, **kwargs):
        from cgrig.apps.uninstallerui import uninstaller
        eng = engine.currentEngine()
        return eng.showDialog(uninstaller.UninstallerUi)


class Reload(palette.ActionPlugin):
    id = "cgrig.reload"
    creator = "David Sparrow"
    tags = ["reload"]
    uiData = {"icon": "menu_cgrig_reload",
              "tooltip": "Reloads cgrigtools by reloading the cgrigtools.py plugin",
              "label": "Reload",
              "color": "",
              "multipleTools": False,
              "backgroundColor": ""
              }

    def execute(self, *args, **kwargs):
        cmds.evalDeferred('from maya import cmds;cmds.flushUndo();cmds.unloadPlugin("cgrigtools.py")\ncmds.loadPlugin("cgrigtools.py")')


class Shutdown(palette.ActionPlugin):
    id = "cgrig.shutdown"
    creator = "David Sparrow"
    tags = ["menu_shutdown"]
    uiData = {"icon": "cgrig_shutdown",
              "tooltip": "shutdown cgrigtools by unloading the cgrigtools.py plugin",
              "label": "Shutdown",
              "color": "",
              "multipleTools": False,
              "backgroundColor": ""
              }

    def execute(self):
        cmds.evalDeferred('from maya import cmds;cmds.flushUndo();cmds.unloadPlugin("cgrigtools.py")')


class ReloadViewport(palette.ActionPlugin):
    id = "cgrig.reloadViewport"
    creator = "David Sparrow"
    tags = ["viewport", "reload"]
    uiData = {"icon": "reload2",
              "tooltip": "Forces mayas viewport to refresh",
              "label": "Refresh Viewport",
              "multipleTools": False,
              }

    def execute(self, *args, **kwargs):
        """Reload/refreshes the viewport, fixing various update issues"""
        from cgrig.libs.maya.cmds.display import viewportmodes
        viewportmodes.reloadViewport(message=True)  # cmds.ogs(reset=True)
