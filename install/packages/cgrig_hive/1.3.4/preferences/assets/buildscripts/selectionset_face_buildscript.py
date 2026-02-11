"""Face Selection Sets Build Script for adding custom selection sets to the rig after Polish.

Handles
- Animator selection sets


------------ BUILD SCRIPT UI DOCUMENTATION ----------------

More Hive Build Script documentation found at:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting.html

Common build script code examples:
    https://create3dcharacters.com/cgrig-dev-documentation/packages/cgrig_hive/buildscripting_examples.html

Author: David Sparrow, Andrew Silke
"""
from maya import cmds

from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.sets import selectionsets


class SelectionSetFaceBuildScript(api.BaseBuildScript):
    """
    """
    id = "selectionSetFaceBuildScript"  # name that appears in the hive UI.

    def _validateSets(self, sets):
        """Validates the sets exist, if not they are removed from the list

        :param sets: A list of sets to validate
        :type sets: list[str]
        """
        newSet = []
        for s in sets:
            if cmds.objExists(s):
                newSet.append(s)
        return newSet

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        # TODO make the set names more generic and not hard coded
        """
        # r = self.rig  # use later

        # Container Set Names -------------------------------------------------------------------------------------
        face_all_set = "face_all_set"
        eyeAll_sSet = "eyeAll_sSet"
        browAll_sSet = "browAll_sSet"
        earAll_sSet = "earAll_sSet"
        teethAll_sSet = "teethAll_sSet"
        mouthAll_sSet = "mouthAll_sSet"
        mouthJaw_sSet = "mouthJaw_sSet"
        cheekAll_sSet = "cheekAll_sSet"
        noseAll_sSet = "noseAll_sSet"

        # Component Set Names -------------------------------------------------------------------------------------
        eye_L_sSet = "eye_L_sSet"
        eye_R_sSet = "eye_R_sSet"
        eyesMain_M_sSet = "eyesMain_M_sSet"
        brow_L_sSet = "brow_L_sSet"
        brow_R_sSet = "brow_R_sSet"
        mouth_sSet = "mouth_M_sSet"
        ear_L_sSet = "ear_L_sSet"
        ear_R_sSet = "ear_R_sSet"
        jaw_M_sSet = "jaw_M_sSet"
        teethLower_M_sSet = "teethLower_M_sSet"
        teethUpper_M_sSet = "teethUpper_M_sSet"
        tongue_M_sSet = "tongue_M_sSet"
        nose_M_sSet = "nose_M_sSet"
        nose_L_sSet = "nose_L_sSet"
        nose_R_sSet = "nose_R_sSet"
        noseLower_M_sSet = "noseLower_M_sSet"
        headSections_M_sSet = "headSections_M_sSet"
        cheek_L_sSet = "cheek_L_sSet"
        cheek_R_sSet = "cheek_R_sSet"

        # Create the sets as a list of names, also checks if they exist ------------------------------
        eye_sets = self._validateSets([eye_L_sSet, eye_R_sSet, eyesMain_M_sSet])
        brow_sets = self._validateSets([brow_L_sSet, brow_R_sSet])
        ear_sets = self._validateSets([ear_L_sSet, ear_R_sSet])
        mouthJaw_sets = self._validateSets([mouth_sSet, jaw_M_sSet])
        teethAll_sets = self._validateSets([teethLower_M_sSet, teethUpper_M_sSet])
        mouthAll_sets = self._validateSets([tongue_M_sSet])
        nose_sets = self._validateSets([nose_M_sSet, nose_L_sSet, nose_R_sSet, noseLower_M_sSet])
        cheek_sets = self._validateSets([cheek_L_sSet, cheek_R_sSet])
        headSections_sets = self._validateSets([headSections_M_sSet])
        face_sets = eye_sets + ear_sets + mouthAll_sets + nose_sets + brow_sets + mouthJaw_sets + teethAll_sets + cheek_sets + headSections_sets

        if not cmds.objExists(face_all_set):  # create the face_all_set if it doesn't exist --------------------------
            selectionsets.addSSetCgRigOptions(face_all_set, [],
                                            icon="st_circlePurple",
                                            visibility=False,
                                            parentSet="all_sSet", soloParent=True)
        # Create the container selection sets, children, and parents to the face_all_set ------------------------------
        for sset in face_sets:
            selectionsets.setMarkingMenuVis(sset, visibility=False)
            selectionsets.setIcon(sset, "st_squarePink")
            # unparent all sets, usually from the body set
            selectionsets.unParentAll(sset)
        if headSections_sets:
            selectionsets.parentSelectionSets([headSections_M_sSet], face_all_set)
        if nose_sets:
            selectionsets.addSSetCgRigOptions(noseAll_sSet, nose_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if cheek_sets:
            selectionsets.addSSetCgRigOptions(cheekAll_sSet, cheek_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if eye_sets:
            selectionsets.addSSetCgRigOptions(eyeAll_sSet, eye_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if brow_sets:
            selectionsets.addSSetCgRigOptions(browAll_sSet, brow_sets,
                                            icon="st_circleOrange",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if ear_sets:
            selectionsets.addSSetCgRigOptions(earAll_sSet, ear_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if mouthAll_sets:
            selectionsets.addSSetCgRigOptions(mouthAll_sSet, mouthAll_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=face_all_set, soloParent=True)
        if mouthJaw_sets:
            selectionsets.addSSetCgRigOptions(mouthJaw_sSet, mouthJaw_sets,
                                            icon="st_trianglePink",
                                            visibility=False,
                                            parentSet=mouthAll_sSet, soloParent=True)
        if teethAll_sets:
            selectionsets.addSSetCgRigOptions(teethAll_sSet, teethAll_sets,
                                            icon="st_circlePink",
                                            visibility=False,
                                            parentSet=mouthAll_sSet, soloParent=True)
