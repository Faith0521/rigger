"""Selection set that builds sets from the sets saved in the scene by the CgRig Selection Sets UI or the Rebuild Tools.

Note this is now depreciated in favor of the new Rebuild Tools Build Script, which handles sel sets and more.

------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html

"""
from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.sets import selectionsets


class SelectionSetBuildFromSaved(api.BaseBuildScript):
    """Post polish buildscript for building selection sets from saved sets in the scene.
    This script will load selection sets as saved in the scene by the CgRig Selection Sets UI.
    It is now depreciated in favor of the new Rebuild Tools Build Script, which handles sel sets and more.
    """
    id = "selectionSetBuildFromSaved"  # name that appears in the hive UI.

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Builds selections sets as saved in the scene, from the CgRig Selection Sets UI
        The node with the settings will try to import and load on polish from the node "cgrigHiveExportSettings"
        """
        selectionsets.loadselSetHierarchyScene()
