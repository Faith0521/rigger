# -*- coding: utf-8 -*-
import webbrowser

from cgrig.apps.toolpalette import palette
from cgrig.libs.pyqt.widgets.frameless import window
from cgrig.core.util import zlogging
from cgrig.apps.toolpalette import qtshelf
from cgrig.core import engine
from cgrigvendor.Qt import QtGui

logger = zlogging.getLogger(__name__)


class HelpIconShelf(palette.ActionPlugin):
    id = "cgrig.shelf.help"
    creator = "Andrew Silke"
    tags = ["shelf", "icon"]
    uiData = {"icon": "helpMenu_shlf", "label": "Help Menu"}
    _ADDRESSES = dict(
        create3dcharacters="https://create3dcharacters.com",
        latestNews="https://create3dcharacters.com/latest-news",
        cgrigToolsHelpContents="https://create3dcharacters.com/cgrig2",
        cgrigToolsGettingStarted="https://create3dcharacters.com/cgrigtools-getting-started",
        cgrigToolsInstallUpdate="https://create3dcharacters.com/maya-cgrig-tools-pro-installer",
        cgrigToolsAssetsPresets="https://create3dcharacters.com/maya-cgrig-tools-pro-installer",
        cgrigChangelog="https://create3dcharacters.com/maya-cgrig-tools-pro-changelog",
        cgrigIssuesFixes="https://create3dcharacters.com/maya-cgrig-tools-pro-known-issues",
        coursesByOrder="https://create3dcharacters.com/package-courses",
        coursesByPopularity="https://create3dcharacters.com/package-by-popularity",
        coursesByDateAdded="https://create3dcharacters.com/package-by-date-added",
        intermediateCourse="https://create3dcharacters.com/package-maya-generalist-intermediate",
        advancedCourse="https://create3dcharacters.com/package-maya-generalist-advanced",
        mayaHotkeyList="https://create3dcharacters.com/maya-hotkeys-cgrig2",
        developerDocumentation="https://create3dcharacters.com/cgrig-dev-documentation/index.html",
    )

    def execute(self, *args, **kwargs):
        name = kwargs["variant"]
        address = HelpIconShelf._ADDRESSES.get(name)
        if address:
            webbrowser.open(address)


class CgRigShelfFloatingWindow(palette.ActionPlugin):
    id = "cgrig.shelf.cgrigFloatingShelf"
    creator = "CgRigTools"
    tags = ["shelf", "icon"]
    uiData = {
        "icon": "cgrigToolsZ",
        "tooltip": "Floating Shelf For CgRig Tools",
        "label": "CgRig Floating Shelf (shift+alt+Q)",
    }
    WINDOW_OFFSET_X = int(-(17 / 2 * 32))
    WINDOW_OFFSET_Y = -10

    def execute(self, *args, **kwargs):
        point = QtGui.QCursor.pos()
        point.setX(point.x() + CgRigShelfFloatingWindow.WINDOW_OFFSET_X)
        point.setY(point.y() + CgRigShelfFloatingWindow.WINDOW_OFFSET_Y)
        win = engine.currentEngine().showDialog(
            qtshelf.ShelfWindow, name="cgrigShelf", shelfId="CgRigToolsPro", show=False
        )
        win.show(point)


class ResetAllWindowPosition(palette.ActionPlugin):
    id = "cgrig.shelf.resetAllWindows"
    creator = "CgRigTools"
    tags = ["shelf", "icon"]
    uiData = {
        "icon": "reloadWindows",
        "tooltip": "Resets all CgRig windows to be at the center of the host application",
        "label": "Reset All CgRig Windows",
    }

    def execute(self, *args, **kwargs):
        for i in window.getCgRigWindows():
            win = i.cgrigWindow
            if win is not None:
                win.centerToParent()


class ToggleCgRigLogging(palette.ActionPlugin):
    id = "cgrig.logging"
    creator = "CgRigtools"
    tags = ["debug", "logging"]
    uiData = {
        "icon": "",
        "tooltip": "Sets CgRig tools logging to either DEBUG or INFO",
        "label": "Debug Logging",
        "isCheckable": True,
        "isChecked": zlogging.isGlobalDebug(),
    }

    def execute(self, *args, **kwargs):
        state = not zlogging.isGlobalDebug()
        if zlogging.isGlobalDebug():
            zlogging.setGlobalDebug(False)
        else:
            zlogging.setGlobalDebug(True)

        return state


class SliderTest(palette.SliderActionPlugin):
    id = "cgrig.sliderTest"
    creator = "CgRigtools"

    @property
    def uiData(self):
        # example data for the plugin this is called for all child variants as well,
        # todo: provide variant id to uiData() maybe uiDataForVariant()?
        data = {
            "icon": "blender",
            "iconColor": (255.0, 153.0, 153.0),
            "tooltip": "Tween Machine Slider with Options",
            "widgetInfo": {
                "defaultValue": 0.5,
                "minValue": -0.25,
                "maxValue": 1.25,
                "value": 0.5,
                "someRandoKey": "something Weird",
            },
        }
        return data

    def execute(self, *args, **kwargs):
        # means we're executing a menu action so we get the parent item
        if kwargs.get("variant", "") == "create3dcharacters":
            widgetInfo = kwargs["item"].parent.widgetInfo
            print(widgetInfo)
            print(widgetInfo["value"])
            print(widgetInfo["maxValue"])
            print(widgetInfo["minValue"])
