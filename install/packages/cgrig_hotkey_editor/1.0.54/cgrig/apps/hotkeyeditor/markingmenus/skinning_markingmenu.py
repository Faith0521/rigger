# -*- coding: utf-8 -*-
import maya.mel as mel

from cgrig.apps.toolsetsui.run import openToolset
from cgrig.libs.maya.markingmenu import menu
from cgrig.libs.maya.cmds.skin import bindskin
from cgrig.libs.maya.cmds.hotkeys import definedhotkeys
from cgrig.libs.braverabbitsmoothskin import brsmoothskin


class SkinMarkingMenuCommand(menu.MarkingMenuCommand):
    """Command class for the skinning marking menu.

    Commands are related to the file (JSON) in the same directory:

    .. code-block:: python

        skinning.mmlayout

    CgRig paths must point to this directory, usually on cgrig startup inside the repo root package.json file.

    Example add to package.json:

    .. code-block:: python

        "CGRIG_MM_COMMAND_PATH": "{self}/cgrig/libs/maya/cmds/hotkeys",
        "CGRIG_MM_MENU_PATH": "{self}/cgrig/libs/maya/cmds/hotkeys",
        "CGRIG_MM_LAYOUT_PATH": "{self}/cgrig/libs/maya/cmds/hotkeys",

    Or if not on startup:

    .. code-block:: python

        os.environ["CGRIG_MM_COMMAND_PATH"] = r"D:\repos\cgrigtools_pro\cgrigcore_pro\cgrig\libs\maya\cmds\hotkeys"
        os.environ["CGRIG_MM_MENU_PATH"] = r"D:\repos\cgrigtools_pro\cgrigcore_pro\cgrig\libs\maya\cmds\hotkeys"
        os.environ["CGRIG_MM_LAYOUT_PATH"] = r"D:\repos\cgrigtools_pro\cgrigcore_pro\cgrig\libs\maya\cmds\hotkeys"

    Map the following code to a hotkey press. Note: Change the key modifiers if using shift alt ctrl etc:

    .. code-block:: python

        import maya.mel as mel
        from cgrig.libs.maya.markingmenu import menu as cgrigMenu
        cgrigMenu.MarkingMenu.buildFromLayout("markingMenu.skinning",
                                            "markingMenuSkinning",
                                            parent=mel.eval("findPanelPopupParent"),
                                            options={"altModifier": False,
                                                     "shiftModifier": True})

    Map to hotkey release:

    .. code-block:: python

        from cgrig.libs.maya.markingmenu import menu as cgrigMenu
        cgrigMenu.MarkingMenu.removeExistingMenu("markingMenuSkinning")

    """
    id = "skiningMarkingMenu"  # a unique identifier for a class, should never be changed
    creator = "CgRigtools"

    @staticmethod
    def uiData(arguments):
        """This method is mostly over ridden by the associated json file"""
        return {"icon": "",
                "label": "",
                "bold": False,
                "italic": False,
                "optionBox": False,
                "optionBoxIcon": ""
                }

    def execute(self, arguments):
        """The main execute methods for the skinning marking menu. see executeUI() for option box commands

        :type arguments: dict
        """
        operation = arguments.get("operation", "")
        if operation == "skinSelected":
            bindskin.bindSkinSelected(toSelectedBones=True, maximumInfluences=5, maxEditLimit=5, bindMethod=0,
                                      displayMessage=True)
        elif operation == "unbindSkin":
            bindskin.unbindSkinSelected()
        elif operation == "mirrorXToNegX":
            bindskin.mirrorSkinSelection(mirrorMode='YZ', mirrorInverse=False)
        elif operation == "smoothSkinWeights":
            brsmoothskin.setBrushToolHotkeyMap()
        elif operation == "ngSkinTools":
            definedhotkeys.open_ngSkinTools()
        elif operation == "copySkinWeights":
            bindskin.copySkinWeightsSel()
        elif operation == "pasteSkinWeights":
            bindskin.pasteSkinWeightsSel()
        elif operation == "cgrigVertSkinning":
            pass
        elif operation == "NGSkinTools":
            pass
        elif operation == "paintWeightsWindow":
            mel.eval("artAttrSkinToolScript 3")
        elif operation == "transferSkinWeights":
            bindskin.transferSkinWeightsSelected()
        elif operation == "duplicateOriginal":
            bindskin.duplicateSelectedBeforeBind()
        elif operation == "bindSelHeatMap":
            bindskin.bindSkinSelected(bindMethod=2)
        elif operation == "bindHierarchyDefaults":
            bindskin.bindSkinSelected(toSelectedBones=False, maximumInfluences=5, maxEditLimit=5, bindMethod=0,
                                      displayMessage=True)
        elif operation == "bindSelectedRigid":
            bindskin.bindSkinSelected(toSelectedBones=True, maximumInfluences=0, maxEditLimit=5, bindMethod=0,
                                      displayMessage=True)
        elif operation == "bindSkinGeodesic":
            bindskin.bindSkinSelected(bindMethod=3)
        elif operation == "addJointsToSkin":
            bindskin.addJointsToSkinnedSelected()
        elif operation == "removeInfluences":
            bindskin.removeInfluenceSelected()
        elif operation == "componentEditor":
            mel.eval('tearOffRestorePanel "Component Editor" "componentEditorPanel" true;')
        elif operation == "cgrigSkinWeightsWindow":
            pass
        elif operation == "importWeightsBraverabbit":
            pass
        elif operation == "exportWeightsBraverabbit":
            pass
        elif operation == "hammerWeights":
            mel.eval("weightHammerVerts;")
        elif operation == "pruneSmallWeights":
            mel.eval("performPruneWeights false;")
        elif operation == "skinToWeightBlended":
            bindskin.skinClusterMethodSwitch(skinningMethod=2, displayMessage=True)
        elif operation == "combineSkinnedMeshes":
            bindskin.combineSkinnedMeshesSelected(constructionHistory=True)
        elif operation == "openSkinningToolbox":
            openToolset("skinningUtilities", advancedMode=False)

    def executeUI(self, arguments):
        """The option box execute methods for the skinning marking menu. see execute() for main commands

        For this method to be called "optionBox": True.

        :type arguments: dict
        """
        operation = arguments.get("operation", "")
        if operation == "skinSelected" \
                or operation == "bindSelHeatMap" \
                or operation == "bindHierarchyDefaults" \
                or operation == "bindSelectedRigid" \
                or operation == "bindSkinGeodesic":
            # Open Skin Window, command changed in some versions of Maya
            try:
                mel.eval("pythonRunTimeCommand skincluster.cmd_create 1")
            except:
                mel.eval("performSkinCluster true;")
        elif operation == "unbindSkin":
            mel.eval("DetachSkinOptions;")
        elif operation == "addJointsToSkin":
            mel.eval("performAddInfluence true;")
        elif operation == "mirrorXToNegX":
            mel.eval("performMirrorSkinWeights true;")
        elif operation == "pruneSmallWeights":
            mel.eval("performPruneWeights true;")
        elif operation == "smoothSkinWeights":
            definedhotkeys.open_brSmoothWeights(advancedMode=False)
