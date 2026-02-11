"""


"""
from cgrig.libs.hive import api
from cgrig.libs.hive.rebuildtools import defaultattrs


class FaceVisibilityBuildScript(api.BaseBuildScript):
    """Post polish buildscript for rigs with faces.
    Handles default values for the nose_L nose_R and noseLower_M component drivers.
    """
    id = "face_attributes_buildscript"  # name that appears in the hive UI.
    # Hardcoded default attribute overrides that can be changed in the rebuild tools.
    rebuildAttrsStrList = ["nose:L controlPanel cheekBoneMultiplierXX 0.04",
                           "nose:L controlPanel cheekBoneMultiplierYY 0.04",
                           "nose:L controlPanel cheekBoneMultiplierYZ 0.0",
                           "nose:L controlPanel cheekBoneMultiplierZZ 0.02",
                           "nose:L controlPanel cheekMultiplierXX 0.05",
                           "nose:L controlPanel cheekMultiplierXZ 0.0",
                           "nose:L controlPanel cheekMultiplierYY 0.08",
                           "nose:L controlPanel nasolabialMultiplierXX 0.01",
                           "nose:L controlPanel nasolabialMultiplierXZ 0.0",
                           "nose:L controlPanel nasolabialMultiplierYY 0.01",
                           "nose:L controlPanel nasolabialMultiplierYZ 0.0",
                           "nose:L controlPanel nasolabialMultiplierZZ 0.01",
                           "noseLower:M controlPanel cheekBoneMultiplierXX 0.05",
                           "noseLower:M controlPanel cheekBoneMultiplierYY 0.1",
                           "noseLower:M controlPanel cheekBoneMultiplierYZ 0.0",
                           "noseLower:M controlPanel cheekBoneMultiplierZZ 0.05",
                           "noseLower:M controlPanel cheekMultiplierXX 0.2",
                           "noseLower:M controlPanel cheekMultiplierXZ 0.0",
                           "noseLower:M controlPanel cheekMultiplierYY 0.2",
                           "noseLower:M controlPanel cheekMultiplierZZ 0.05",
                           "noseLower:M controlPanel nasolabialMultiplierXX 0.05",
                           "noseLower:M controlPanel nasolabialMultiplierXZ 0.0",
                           "noseLower:M controlPanel nasolabialMultiplierYY 0.05",
                           "noseLower:M controlPanel nasolabialMultiplierYZ 0.0",
                           "noseLower:M controlPanel nasolabialMultiplierZZ 0.05"]

    # ------------------------
    # Build Script Methods
    # ------------------------

    def createSaveNewBuildScriptScene(self):
        """Creates a new build script scene with the rebuild attributes string list."""
        newString = ""
        # Iterate through the rebuild attributes string list and create a new string
        for attrStr in self.rebuildAttrsStrList:
            newString += attrStr + "\n"
        # save the new string data to the scene
        defaultattrs.saveStringDataScene(newString, True, message=True)

    def postPolishBuild(self, properties):
        """Executed after the polish stage.

        Connects the face visibility attribute to the head, spine cog and god controls.
        """
        rig = self.rig  # The current rig object from the hive API
        dataShouldBeWritten = False
        stringData, applySymBool = defaultattrs.getStringDataScene(message=True)
        if not stringData:
            self.createSaveNewBuildScriptScene()
            return
        if not stringData:
            self.createSaveNewBuildScriptScene()
            return
        # Iterate through the string data and split into each line
        existingLinesList = stringData.split("\n")
        if not existingLinesList:
            self.createSaveNewBuildScriptScene()
            return

        # Add lines if they don't exist
        for defaultLine in self.rebuildAttrsStrList:
            found = False
            # Check if the default line is in the rebuild attributes string list
            for existingLine in existingLinesList:
                # check the defaultLine to see if the start is a match with existingLine
                if existingLine.startswith(defaultLine):
                    found = True
                    break
            if found:  # line exists so we don't need to add it
                continue
            else:
                # If the line does not match, add it to the rebuild attributes string list
                stringData += "{}\n".format(defaultLine)
                dataShouldBeWritten = True

        # if the data exists, save the new build script scene
        if dataShouldBeWritten:
            defaultattrs.saveStringDataScene(stringData, True, message=True)
