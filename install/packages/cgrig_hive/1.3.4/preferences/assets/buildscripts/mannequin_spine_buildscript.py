"""Mannequin buildscript for hiding controls on the spline spine.



------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html

"""

from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.objutils import attributes


class MannequinSpineBuildscript(api.BaseBuildScript):
    """

    .. note::

        Best to read the properties method in the base class :func:`api.BaseBuildScript.properties`

    """
    # unique identifier for the plugin which will be referenced by the registry.
    id = "mannequinSpine_buildscript"  # change id to name that will appear in the hive UI.

    def postPolishBuild(self, properties):
        """Hides two controls on the spline spine
        """
        # Sets default control visibility for the spine, simplifies the amount of controls for simple mannequin spines.
        spineTop_M = self.rig.spine_M.rigLayer().control("ctrl02")
        for attr in ["ctrl02Vis", "ctrl00Vis"]:
            attributes.attributeDefault(str(spineTop_M), attr, 0)
