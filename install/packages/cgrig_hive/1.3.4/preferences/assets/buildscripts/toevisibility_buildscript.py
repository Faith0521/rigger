"""Toes buildscript for bipeds.  Adds visibility attributes to the left and right toes so you can hide the toes.


------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html


"""
from cgrig.libs.utils import output
from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.objutils import attributes


class ToeVisibilityBuildScript(api.BaseBuildScript):
    """Post polish buildscript for Natalie rig with Hives full face including mouth component.

    .. note::

        Best to read the properties method in the base class :func:`api.BaseBuildScript.properties`

    """
    # Unique identifier which will seen in the Hive settings UI drop-down.
    id = "toe_visibility_buildscript"

    @staticmethod
    def properties():
        """Defines the maya reference filePath. For more information about properties see
        :func:`cgrig.libs.hive.base.buildscript.BaseBuildScript.properties`

        :rtype: list[dict]
        """
        return [{"name": "godNode",
                 "displayName": "God Component ID",
                 "value": "god_M_godnode_anim",
                 "type": "string",
                 "layout": [0, 0]},
                {"name": "footLNode",
                 "displayName": "IK L Control Name",
                 "value": "leg_L_foot_ik_anim",
                 "type": "string",
                 "layout": [1, 0]},
                {"name": "footRNode",
                 "displayName": "IK R Control Name",
                 "value": "leg_R_foot_ik_anim",
                 "type": "string",
                 "layout": [2, 0]}
                ]

    # ------------------------
    # Build Script Methods
    # ------------------------

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Adds:
            - toeL and toeR visibility toggle attributes on the controls.
        """
        rig = self.rig  # The current rig object from the hive API, in this case the Natalie rig.

        # Get Hive Controls For Vis Attrs ------------------------
        godNode = properties.get("godNode")  # string name from self.properties()
        footLNode = properties.get("footLNode")
        footRNode = properties.get("footRNode")

        # Create toes visibility attribute and connections ----------------------------
        toeLVisAttr = "toesVis"
        toeRVisAttr = "toesVis"

        toeLObjs = []
        toeRObjs = []

        # get the root of each toe component if they exist
        try:
            toeLObjs.append(rig.toe01_L.rootTransform().fullPathName())
        except:
            pass
        try:
            toeLObjs.append(rig.toe02_L.rootTransform().fullPathName())
        except:
            pass
        try:
            toeLObjs.append(rig.toe03_L.rootTransform().fullPathName())
        except:
            pass
        try:
            toeLObjs.append(rig.toe04_L.rootTransform().fullPathName())
        except:
            pass
        try:
            toeLObjs.append(rig.toe05_L.rootTransform().fullPathName())
        except:
            pass
        try:
            toeRObjs.append(rig.toe01_R.rootTransform().fullPathName())
        except:
            pass
        try:
            toeRObjs.append(rig.toe02_R.rootTransform().fullPathName())
        except:
            pass
        try:
            toeRObjs.append(rig.toe03_R.rootTransform().fullPathName())
        except:
            pass
        try:
            toeRObjs.append(rig.toe04_R.rootTransform().fullPathName())
        except:
            pass
        try:
            toeRObjs.append(rig.toe05_R.rootTransform().fullPathName())
        except:
            pass

        if toeLObjs:
            attributes.visibilityConnectObjs(toeLVisAttr, footLNode, toeLObjs,
                                             channelBox=True, nonKeyable=True, defaultValue=True)
        else:
            output.displayWarning("Build Script: No left toes found to connect the toe visibility attribute.")

        if toeRObjs:
            attributes.visibilityConnectObjs(toeRVisAttr, footRNode, toeRObjs,
                                             channelBox=True, nonKeyable=True, defaultValue=True)
        else:
            output.displayWarning("Build Script: No right toes found to connect the toe visibility attribute.")

        # Add proxy attrs feet controls ----------------------------
        attributes.addProxyAttribute(godNode, footLNode, toeLVisAttr, proxyAttr="toesLVis", nonKeyable=True)
        attributes.addProxyAttribute(godNode, footRNode, toeRVisAttr, proxyAttr="toesRVis", nonKeyable=True)
