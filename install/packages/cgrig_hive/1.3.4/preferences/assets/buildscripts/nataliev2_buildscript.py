"""Natalie Hive build script.

Handles
- Visibility attributes for switching hair
- Disables the ability to non-uniform scale on the god node


------------ BUILD SCRIPT DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html


"""

from maya import cmds

from cgrig.libs.maya import zapi
from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.objutils import attributes

animCtrls = ("cheek_L_cheek_anim", "cheek_L_cheekBone_anim", "cheek_L_nasolabial_anim", "cheek_R_nasolabial_anim",
             "cheek_R_cheek_anim", "cheek_R_cheekBone_anim", "nose_L_cheek_anim", "nose_L_cheekBone_anim",
             "nose_R_cheek_anim", "nose_R_cheekBone_anim")
sdks = ("cheek_L_cheek_sdk", "cheek_L_cheekBone_sdk", "cheek_L_nasolabial_sdk", "cheek_R_nasolabial_sdk",
        "cheek_R_cheek_sdk", "cheek_R_cheekBone_sdk", "nose_L_cheek_sdk", "nose_L_cheekBone_sdk", "nose_R_cheek_sdk",
        "nose_R_cheekBone_sdk")
srts = ("cheek_L_cheek_anim_srt", "cheek_L_cheekBone_anim_srt", "cheek_L_nasolabial_anim_srt",
        "cheek_R_nasolabial_anim_srt", "cheek_R_cheek_anim_srt", "cheek_R_cheekBone_anim_srt", "nose_L_cheek_anim_srt",
        "nose_L_cheekBone_anim_srt", "nose_R_cheek_anim_srt", "nose_R_cheekBone_anim_srt")


class NatalieV2BuildScript(api.BaseBuildScript):
    """Post polish buildscript for Natalie rig with Hive's full face including mouth component.
    """
    # Unique identifier which will seen in the Hive UI > settings cog icon > Build Script UI drop-down.
    id = "natalie_v2_buildscript"

    # ------------------------
    # Build Script Methods
    # ------------------------
    def preDeleteRigLayer(self, properties):
        """Executed when the entire hive rig gets deleted.  Unparent the SDK grps.
        """
        for i, ctrl in enumerate(animCtrls):
            if not cmds.objExists(sdks[i]):
                break
            cmds.parent(ctrl, srts[i])
            cmds.parent(sdks[i], world=True)

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Adds:
            - Hair visibility toggle attributes on the controls.
            - God node can not be non-uniform scaled.
        """
        rig = self.rig  # The current rig object from the hive API, in this case the Natalie rig.
        hairExists = cmds.objExists("hairTop_C_00_anim")

        # Get Hive Controls ------------------------
        # Control name ID's are found on the control transform: Attribute Editor > Extra Attributes > CgRig Hive ID
        godNode = rig.god_M.rigLayer().control("godnode").fullPathName()  # fullPathName() returns a string name
        hipsNode = rig.spine_M.rigLayer().control("cog").fullPathName()
        headNode = rig.head_M.rigLayer().control("head").fullPathName()

        # Create hair visibility attribute and connections ----------------------------
        if hairExists:
            hairVisAttr = "hairVis"
            hairRoots = list()  # Root transform node of each hair component, there are 13 hair components.
            for comp in rig.iterComponents():  # Find all root transforms of components with "hair" in the name
                if "hair" in comp.name().lower():
                    hairRoots.append(comp.rootTransform().fullPathName())  # fullPathName() returns a string
            if hairRoots:
                attributes.visibilityConnectObjs(hairVisAttr, str(godNode), hairRoots,
                                                 channelBox=True, nonKeyable=True, defaultValue=True)
                attributes.addProxyAttribute(str(headNode), str(godNode), hairVisAttr, proxyAttr="")
                attributes.addProxyAttribute(str(hipsNode), str(godNode), hairVisAttr, proxyAttr="")

        # Turn off .prepopulate attribute, solved cycle issues related to disabling non uniform scale ----------------
        for i in zapi.nodesByNames(cmds.ls(type="controller")):
            pre = i.prepopulate
            if not pre.isDestination:
                pre.set(0)

        # Disable non-uniform scale ---------------------------
        attributes.disableNonUniformScale(godNode)

        # Temp SDK rebuild -------------------------------
        for i, ctrl in enumerate(animCtrls):
            if not cmds.objExists(sdks[i]):
                break
            cmds.parent(sdks[i], srts[i])
            cmds.parent(ctrl, sdks[i])
            cmds.setAttr("{}.translate".format(sdks[i]), 0.0, 0.0, 0.0, type="float3")
            cmds.setAttr("{}.rotate".format(sdks[i]), 0.0, 0.0, 0.0, type="float3")
            cmds.setAttr("{}.translate".format(ctrl), 0.0, 0.0, 0.0, type="float3")
            cmds.setAttr("{}.rotate".format(ctrl), 0.0, 0.0, 0.0, type="float3")
