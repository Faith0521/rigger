"""Face Visibility build script.  Adds two visibility attributes to the head, spine cog and god controls.

- Face Primary (vis)
- Face Secondary (vis)

Add this if a face components exists.

The script will add a face visibility attribute to the head, or other controls.

User can change the control names in the UI to match the controls in the scene.

Face components that get hidden are hardcoded in the self.compPrimaryNameSide and self.compSecondaryNameSide lists.

Primary:
    [["jaw", "M"], ["eye", "L"], ["eye", "R"], ["ear", "L"], ["ear", "R"],
   ["teethUpper", "M"], ["teethLower", "M"], ["tongue", "M"], ["brow", "L"], ["brow", "R"],
   ["eyesMain", "M"], ["nose", "M"], ["mouth", "M"]]
Secondary:
    [["nose", "L"], ["nose", "R"], ["noseLower", "M"], ["cheek", "L"], ["cheek", "R"],

------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html


"""

from maya import cmds

from cgrig.libs.utils import output
from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.objutils import attributes


class FaceVisibilityBuildScript(api.BaseBuildScript):
    """Post polish buildscript for rigs with faces.  Handles face visibility on the head, spine cog and god controls.

    .. note::

        Best to read the properties method in the base class :func:`api.BaseBuildScript.properties`

    """
    # Unique identifier which will seen in the Hive settings UI drop-down.
    id = "face_visibility_buildscript"
    compPrimaryNameSide = [["jaw", "M"], ["eye", "L"], ["eye", "R"], ["ear", "L"], ["ear", "R"],
                           ["teethUpper", "M"], ["teethLower", "M"], ["tongue", "M"], ["brow", "L"], ["brow", "R"],
                           ["eyesMain", "M"], ["nose", "M"], ["mouth", "M"]]
    compSecondaryNameSide = [["nose", "L"], ["nose", "R"], ["noseLower", "M"], ["cheek", "L"], ["cheek", "R"],
                             ["headSections", "M"]]

    @staticmethod
    def properties():
        """Defines the maya reference filePath. For more information about properties see
        :func:`cgrig.libs.hive.base.buildscript.BaseBuildScript.properties`

        :rtype: list[dict]
        """
        return [{"name": "control01",
                 "displayName": "Control 1 With Face Vis Attr",
                 "value": "head_M_head_anim",
                 "type": "string",
                 "layout": [0, 0]},
                {"name": "control02",
                 "displayName": "Control 2 With Face Vis Attr",
                 "value": "spine_M_cog_anim",
                 "type": "string",
                 "layout": [1, 0]},
                {"name": "control03",
                 "displayName": "Control 3 With Face Vis Attr",
                 "value": "god_M_godnode_anim",
                 "type": "string",
                 "layout": [2, 0]}
                ]

    # ------------------------
    # Helper Methods
    # ------------------------

    def _connectVisAttribute(self):
        pass

    # ------------------------
    # Build Script Methods
    # ------------------------

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Connects the face visibility attribute to the head, spine cog and god controls.
        """
        rig = self.rig  # The current rig object from the hive API
        faceRootList = list()
        faceSecondaryList = list()
        visDividerAttr = "VIS OTHER"
        facePrimaryVisAttr = "facePrimary"
        faceSecondaryVisAttr = "faceSecondary"

        controlsWithVisAttr = []
        # get the controls from the UI
        controlList = [properties.get("control01"), properties.get("control02"), properties.get("control03")]
        for control in controlList:
            if cmds.objExists(control):
                controlsWithVisAttr.append(control)

        if not controlsWithVisAttr:
            output.displayWarning("Build Script: No controls found to connect the face visibility "
                                  "attribute {}".format(controlList))
            return

        # Find face components root grps, create a list of [component, rootGrpStr] for existing components
        for comp in rig.iterComponents():
            for compPair in self.compPrimaryNameSide:
                if compPair[0] == comp.name() and compPair[1] == comp.side():
                    faceRootList.append(comp.rootTransform().fullPathName())
            for compPair in self.compSecondaryNameSide:
                if compPair[0] == comp.name() and compPair[1] == comp.side():
                    faceSecondaryList.append(comp.rootTransform().fullPathName())

        # Build the face vis attribute and connect to
        attributes.labelAttr(visDividerAttr, controlsWithVisAttr[0], checkExists=True)

        if faceRootList:
            # Connect the primary face visibility attribute on the first control usually the head control
            attributes.visibilityConnectObjs(facePrimaryVisAttr,
                                             controlsWithVisAttr[0],
                                             faceRootList,
                                             nonKeyable=True,
                                             defaultValue=True)

        if faceSecondaryList:
            # Connect the secondary face visibility attribute on the first control usually the head control
            attributes.visibilityConnectObjs(faceSecondaryVisAttr,
                                             controlsWithVisAttr[0],
                                             faceSecondaryList,
                                             nonKeyable=True,
                                             defaultValue=True)
        # Check other controls are valid and exist
        if len(controlsWithVisAttr) == 1:  # only one control so exit
            return
        # Connect other controls to the same attribute via proxy attrs
        for control in controlsWithVisAttr[1:]:
            # Build the face vis attribute and connect to
            attributes.labelAttr(visDividerAttr, control, checkExists=True)
            attributes.addProxyAttribute(control, controlsWithVisAttr[0], facePrimaryVisAttr, proxyAttr="")
            attributes.addProxyAttribute(control, controlsWithVisAttr[0], faceSecondaryVisAttr, proxyAttr="")

        # draw style on the unused nose joint to None, if it exists.
        if cmds.objExists("noseLower_M_nasolabial_jnt"):
            cmds.setAttr("noseLower_M_nasolabial_jnt.drawStyle", 2)


    def _showFaceRootGroups(self):
        """ Make sure all face root groups are visible, could be hidden in polish mode
        """
        rig = self.rig  # The current rig object from the hive API
        for comp in rig.iterComponents():
            for compPair in self.compPrimaryNameSide:
                if compPair[0] == comp.name() and compPair[1] == comp.side():
                    rootGrp = comp.rootTransform().fullPathName()
                    cmds.setAttr("{}.visibility".format(rootGrp), 1)
            for compPair in self.compSecondaryNameSide:
                if compPair[0] == comp.name() and compPair[1] == comp.side():
                    rootGrp = comp.rootTransform().fullPathName()
                    cmds.setAttr("{}.visibility".format(rootGrp), 1)

    def postGuideBuild(self, properties):
        """Executed once all guides on all components have been built into the scene.
        """
        self._showFaceRootGroups()  # make sure all face root groups are visible, could be hidden in polish mode

    def postDeformBuild(self, properties):
        """ Executed after the deformation and I/O layers has been built for all components
        including all joints.
        """
        self._showFaceRootGroups()  # make sure all face root groups are visible, could be hidden in polish mode
