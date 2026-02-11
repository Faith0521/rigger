"""Hive post buildscript template.  Blueprint for creating Hive buildscripts.


------------ TO CREATE YOUR NEW BUILD SCRIPT ----------------
Copy/paste this file and rename the `filename`, `class name` and the `id` ( id = "example" )

To enable the buildscript:

Change:

    class ExampleBuildScript(object):

To:

    class YourBuildScript(api.BaseBuildScript):

To assign to your rig in the Hive UI, reload CgRig Tools:

    CgRigToolsPro (shelf) > Dev (purple icon) > Reload (menu item)

Open Hive UI and set the build script under:

    Settings (right top cog icon) >  Scripts > Build Scripts (dropdown combo box)

Be sure to reload CgRig Tools with any script changes.


------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html

"""
from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.sets import selectionsets
from cgrig.libs.hive.rebuildtools import defaultattrs


class RebuildToolsBuildScript(api.BaseBuildScript):
    """Rebuild Tools Build Script for Hive. Set this buildscript to work with Hive's Rebuild Tools.

    """
    # unique identifier for the plugin which will be referenced by the registry.
    id = "rebuildTools_buildScript"  # change id to name that will appear in the hive UI.

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Useful for building space switching, optimizing the rig, binding asset meta data and
        preparing for the animator.
        """
        rig = self.rig
        # Rebuild CgRig Selection Sets Saved in Scene
        selectionsets.loadselSetHierarchyScene()
        # Override Default Attribute Values Saved in Scene
        defaultattrs.loadDefaultAttrsFromScene(rig=rig, message=True)
