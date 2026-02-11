from maya import cmds
from . import controller_utils as control
from .naming_utils import *
from .rigging_utils import *


class Helper(control.Ctrl):

    noTransform = "noTransform"
    correctionDataGrp = "of3dCorrectionDataGrp"
    netSuffix = "Net"
    correctionGrp = ""
    netList = []
    net = None


    def createCorrect(self,
                      nodeList=None,
                      name=None,
                      toRivet=False,
                      *args):
        """
        Create nodes to calculate the correction we want to mapper fix.
        :param nodeList:
        :param name:
        :param toRivet:
        :param args:
        :return: The created network node.
        """
        if not nodeList:
            nodeList = cmds.ls(selection=True, flatten=True)
        if nodeList:
            if len(nodeList) == 2:
                origNode = nodeList[0]
                actionNode = nodeList[1]
                cmds.undoInfo(openChunk=True)

                # main group
                if not cmds.objExists(self.correctionDataGrp):
                    self.correctionDataGrp = cmds.group(empty=True, name=self.correctionDataGrp)
                    cmds.addAttr(self.correctionDataGrp, longName="of3dCorrectionDataGrp",
                                 attributeType="bool")
                    cmds.setAttr(self.correctionDataGrp + ".of3dCorrectionDataGrp", 1)
                    self.setLockHide([self.correctionDataGrp],
                                     ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz'])

                    if cmds.objExists(self.noTransform):
                        cmds.parent(self.correctionDataGrp, self.noTransform)
                    cmds.setAttr("{}.visibility".format(self.correctionDataGrp), 0)

                # naming
                if not name:
                    name = "Correction"
                correctionName, name = resolveLetterName(name, self.netSuffix)
                self.net = cmds.createNode("network", name=name)
                self.addNetAttrs(correctionName)

                self.correctionGrp = cmds.group(empty=True, name=correctionName + "_Grp")
                cmds.parent(self.correctionGrp, self.correctionDataGrp)
                cmds.connectAttr(self.correctionGrp + ".message", self.net + ".of3dCorrectionDataGrp", force=True)
                originalLoc = self.createCorrectiveLocator(correctionName + "_Original", origNode, toRivet)
                actionLoc = self.createCorrectiveLocator(correctionName + "_Action", actionNode, toRivet)
                cmds.connectAttr(originalLoc + ".message", self.net + ".originalLoc", force=True)
                cmds.connectAttr(actionLoc + ".message", self.net + ".actionLoc", force=True)
                cmds.connectAttr(nodeList[0] + ".message", self.net + ".fatherNode", force=True)
                cmds.connectAttr(nodeList[1] + ".message", self.net + ".brotherNode", force=True)

                # create corrective, interpolation and rigScale nodes:
                correctiveMD = cmds.createNode("multiplyDivide", name=correctionName + "_Corrective_MD")
                interpolationPMA = cmds.createNode("plusMinusAverage", name=correctionName + "_Interpolation_PMA")
                cmds.connectAttr(correctiveMD + ".message", self.net + ".correctiveMD", force=True)
                cmds.connectAttr(interpolationPMA + ".message", self.net + ".interpolationPMA", force=True)
                cmds.connectAttr(self.net + ".corrective", correctiveMD + ".input2X", force=True)
                cmds.connectAttr(self.net + ".interpolation", interpolationPMA + ".input1D[0]", force=True)
                cmds.setAttr(interpolationPMA + ".input1D[1]", 1)

                extractAngleMM = cmds.createNode("multMatrix", name=correctionName + "_ExtractAngle_MM")
                extractAngleDM = cmds.createNode("decomposeMatrix", name=correctionName + "_ExtractAngle_DM")
                extractAngleQtE = cmds.createNode("quatToEuler", name=correctionName + "_ExtractAngle_QtE")
                extractAngleMD = cmds.createNode("multiplyDivide", name=correctionName + "_ExtractAngle_MD")
                angleAxisXCnd = cmds.createNode("condition", name=correctionName + "_ExtractAngle_AxisX_Cnd")
                angleAxisYZCnd = cmds.createNode("condition", name=correctionName + "_ExtractAngle_AxisYZ_Cnd")
                smallerThanOneCnd = cmds.createNode("condition",
                                                    name=correctionName + "_ExtractAngle_SmallerThanOne_Cnd")
                overZeroCnd = cmds.createNode("condition", name=correctionName + "_ExtractAngle_OverZero_Cnd")
                inputRmV = cmds.createNode("remapValue", name=correctionName + "_Input_RmV")
                outputSR = cmds.createNode("setRange", name=correctionName + "_Output_SR")
                cmds.setAttr(extractAngleMD + ".operation", 2)
                cmds.setAttr(smallerThanOneCnd + ".operation", 5)  # less or equal
                cmds.setAttr(smallerThanOneCnd + ".secondTerm", 1)
                cmds.setAttr(overZeroCnd + ".secondTerm", 0)
                cmds.setAttr(overZeroCnd + ".colorIfFalseR", 0)
                cmds.setAttr(overZeroCnd + ".operation", 3)  # greater or equal
                cmds.setAttr(angleAxisYZCnd + ".secondTerm", 1)  # Y
                cmds.connectAttr(actionLoc + ".worldMatrix[0]", extractAngleMM + ".matrixIn[0]", force=True)
                cmds.connectAttr(originalLoc + ".worldInverseMatrix[0]", extractAngleMM + ".matrixIn[1]", force=True)
                cmds.connectAttr(extractAngleMM + ".matrixSum", extractAngleDM + ".inputMatrix", force=True)
                # set general values and connections:
                cmds.setAttr(outputSR + ".oldMaxX", 1)
                cmds.connectAttr(self.net + ".inputStart", inputRmV + ".inputMin", force=True)
                cmds.connectAttr(self.net + ".inputEnd", inputRmV + ".inputMax", force=True)
                cmds.connectAttr(self.net + ".inputEnd", inputRmV + ".outputMax", force=True)
                cmds.connectAttr(self.net + ".outputStart", outputSR + ".minX", force=True)
                cmds.connectAttr(self.net + ".outputEnd", outputSR + ".maxX", force=True)
                cmds.connectAttr(interpolationPMA + ".output1D", inputRmV + ".value[0].value_Interp", force=True)
                # setup the rotation affection
                cmds.connectAttr(extractAngleDM + ".outputQuatX", extractAngleQtE + ".inputQuatX", force=True)
                cmds.connectAttr(extractAngleDM + ".outputQuatY", extractAngleQtE + ".inputQuatY", force=True)
                cmds.connectAttr(extractAngleDM + ".outputQuatZ", extractAngleQtE + ".inputQuatZ", force=True)
                cmds.connectAttr(extractAngleDM + ".outputQuatW", extractAngleQtE + ".inputQuatW", force=True)
                # axis setup
                cmds.connectAttr(self.net + ".axis", angleAxisXCnd + ".firstTerm", force=True)
                cmds.connectAttr(self.net + ".axis", angleAxisYZCnd + ".firstTerm", force=True)
                cmds.connectAttr(inputRmV + ".outValue", extractAngleMD + ".input1X", force=True)
                cmds.connectAttr(extractAngleQtE + ".outputRotateX", angleAxisXCnd + ".colorIfTrueR", force=True)
                cmds.connectAttr(extractAngleQtE + ".outputRotateY", angleAxisYZCnd + ".colorIfTrueR", force=True)
                cmds.connectAttr(extractAngleQtE + ".outputRotateZ", angleAxisYZCnd + ".colorIfFalseR", force=True)
                cmds.connectAttr(angleAxisYZCnd + ".outColorR", angleAxisXCnd + ".colorIfFalseR", force=True)
                cmds.connectAttr(angleAxisXCnd + ".outColorR", inputRmV + ".inputValue", force=True)
                cmds.connectAttr(angleAxisXCnd + ".outColorR", self.net + ".inputValue", force=True)
                cmds.setAttr(self.net + ".inputValue", lock=True)
                # axis order setup
                cmds.connectAttr(self.net + ".inputEnd", extractAngleMD + ".input2X",
                                 force=True)  # it'll be updated when changing angle
                cmds.connectAttr(extractAngleMD + ".outputX", smallerThanOneCnd + ".firstTerm", force=True)
                cmds.connectAttr(extractAngleMD + ".outputX", smallerThanOneCnd + ".colorIfTrueR", force=True)
                cmds.connectAttr(smallerThanOneCnd + ".outColorR", overZeroCnd + ".firstTerm", force=True)
                cmds.connectAttr(smallerThanOneCnd + ".outColorR", overZeroCnd + ".colorIfTrueR", force=True)
                cmds.connectAttr(self.net + ".axisOrder", extractAngleDM + ".inputRotateOrder", force=True)
                cmds.connectAttr(self.net + ".axisOrder", extractAngleQtE + ".inputRotateOrder", force=True)
                # corrective setup:
                cmds.connectAttr(overZeroCnd + ".outColorR", correctiveMD + ".input1X", force=True)
                cmds.connectAttr(correctiveMD + ".outputX", outputSR + ".valueX", force=True)
                # TODO create a way to avoid manual connection here, maybe using the UI new tab?
                cmds.connectAttr(outputSR + ".outValueX", self.net + ".outputValue", force=True)
                cmds.setAttr(self.net + ".outputValue", lock=True)
                # serialize angle nodes
                cmds.connectAttr(extractAngleMM + ".message", self.net + ".extractAngleMM", force=True)
                cmds.connectAttr(extractAngleDM + ".message", self.net + ".extractAngleDM", force=True)
                cmds.connectAttr(extractAngleQtE + ".message", self.net + ".extractAngleQtE", force=True)
                cmds.connectAttr(extractAngleMD + ".message", self.net + ".extractAngleMD", force=True)
                cmds.connectAttr(angleAxisXCnd + ".message", self.net + ".angleAxisXCnd", force=True)
                cmds.connectAttr(angleAxisYZCnd + ".message", self.net + ".angleAxisYZCnd", force=True)
                cmds.connectAttr(smallerThanOneCnd + ".message", self.net + ".smallerThanOneCnd", force=True)
                cmds.connectAttr(overZeroCnd + ".message", self.net + ".overZeroCnd", force=True)
                cmds.connectAttr(inputRmV + ".message", self.net + ".inputRmV", force=True)
                cmds.connectAttr(outputSR + ".message", self.net + ".outputSR", force=True)
                cmds.undoInfo(closeChunk=True)
        return self.net


    def addNetAttrs(self, correctionName):
        """
        Create corrective netWork attrs.
        :param name: netWork node name
        :param correctionName: netWork correctionName name
        :return:
        """
        cmds.addAttr(self.net, longName="of3dNetwork", attributeType="bool")
        cmds.addAttr(self.net, longName="of3dCorrection", attributeType="bool")
        cmds.addAttr(self.net, longName="name", dataType="string")
        cmds.addAttr(self.net, longName="inputValue", attributeType="float")
        cmds.addAttr(self.net, longName="interpolation", attributeType='enum', enumName="Linear:Smooth:Spline")
        cmds.addAttr(self.net, longName="decompose", attributeType="bool", defaultValue=0)
        cmds.addAttr(self.net, longName="axis", attributeType='enum', enumName="X:Y:Z")
        cmds.addAttr(self.net, longName="axisOrder", attributeType='enum', enumName="XYZ:YZX:ZXY:XZY:YXZ:ZYX")
        cmds.addAttr(self.net, longName="inputStart", attributeType="float", defaultValue=0)
        cmds.addAttr(self.net, longName="inputEnd", attributeType="float", defaultValue=90)
        cmds.addAttr(self.net, longName="outputStart", attributeType="float", defaultValue=0)
        cmds.addAttr(self.net, longName="outputEnd", attributeType="float", defaultValue=1)

        messageAttrList = ["of3dCorrectionDataGrp", "originalLoc", "actionLoc", "fatherNode", "brotherNode",
                           "correctiveMD", "extractAngleMM", "extractAngleDM", "extractAngleQtE", "connectCtrl",
                           "extractAngleMD", "angleAxisXCnd", "angleAxisYZCnd", "smallerThanOneCnd",
                           "overZeroCnd", "interpolationPMA", "inputRmV", "outputSR"]

        [cmds.addAttr(self.net, longName=messageAttr, attributeType="message") for messageAttr in messageAttrList]
        cmds.addAttr(self.net, longName="corrective", attributeType="float", minValue=0, defaultValue=1, maxValue=1)
        cmds.addAttr(self.net, longName="outputValue", attributeType="float")
        cmds.setAttr(self.net + ".of3dNetwork", 1)
        cmds.setAttr(self.net + ".of3dCorrection", 1)
        cmds.setAttr(self.net + ".name", correctionName, type="string")


    def createCorrectiveLocator(self, name, toAttach, *args):
        """
        Creates a space locator, zeroOut it to receive a parentConstraint.
        :param name:
        :param toAttach:
        :param toRivet:
        :param args:
        :return: locator to use it as a reader node to the system.
        """
        loc = None
        if cmds.objExists(toAttach):
            loc = cmds.spaceLocator(name=name + "_Loc")[0]
            cmds.addAttr(loc, longName="inputNode", attributeType="message")
            cmds.connectAttr(toAttach + ".message", loc + ".inputNode", force=True)
            grp = GrpAdd(loc, [loc + "_zero"], "Up")[0]
            cmds.parentConstraint(toAttach, grp, maintainOffset=False, name=grp + "_prc")
            cmds.parent(grp, getNodeByMessage(self.correctionDataGrp, self.net))
        return loc


    def articulationJoint(self, fatherNode, brotherNode, jcrNumber=0, jcrPosList=None, jcrRotList=None, dist=1, jarRadius=1.5, *args):
        """ Create a simple joint to help skinning with a half rotation value.
            Receives the number of corrective joints to be created. Zero by default.
            Place these corrective joints with the given vector list.
            Returns the created joint list.
        """
        jointList = []
        if fatherNode and brotherNode:
            if cmds.objExists(fatherNode) and cmds.objExists(brotherNode):
                jaxName = brotherNode + "_HelperRoot"
                jarName = brotherNode + "_HelperOrigin"
                cmds.select(clear=True)
                if not cmds.objExists(jaxName) or not cmds.objExists(jarName):
                    cmds.joint(name=jaxName, radius=0.5 * jarRadius)
                    cmds.joint(name=jarName, radius=jarRadius)
                    cmds.addAttr(jarName, longName='of3d_helperJoint', attributeType='float', keyable=False)
                    cmds.delete(cmds.parentConstraint(brotherNode, jaxName, maintainOffset=0))
                    cmds.parent(jaxName, fatherNode)
                    cmds.makeIdentity(jaxName, apply=True)
                    cmds.setAttr(jaxName + ".segmentScaleCompensate", 0)
                    cmds.setAttr(jarName + ".segmentScaleCompensate", 1)
                jointList.append(jaxName)
                for i in range(0, jcrNumber):
                    cmds.select(jarName)
                    name = resolveLetterName(brotherNode, "Helper")[-1]
                    jcr = cmds.joint(name=name)
                    cmds.setAttr(jcr + ".segmentScaleCompensate", 0)
                    cmds.addAttr(jcr, longName='of3d_helperJoint', attributeType='float', keyable=False)
                    if jcrPosList:
                        cmds.setAttr(jcr + ".translateX", jcrPosList[i][0] * dist)
                        cmds.setAttr(jcr + ".translateY", jcrPosList[i][1] * dist)
                        cmds.setAttr(jcr + ".translateZ", jcrPosList[i][2] * dist)
                    if jcrRotList:
                        cmds.setAttr(jcr + ".rotateX", jcrRotList[i][0])
                        cmds.setAttr(jcr + ".rotateY", jcrRotList[i][1])
                        cmds.setAttr(jcr + ".rotateZ", jcrRotList[i][2])
                    jointList.append(jcr)

                pc = cmds.pointConstraint(brotherNode, jaxName, maintainOffset=True, name=jarName + "_pc")[0]
                oc = cmds.parentConstraint(brotherNode, fatherNode, jaxName, skipTranslate=["x", "y", "z"], maintainOffset=True, name=jarName + "_orc")[0]
                cmds.setAttr(oc + ".interpType", 2)  # Shortest
                sc = cmds.scaleConstraint(brotherNode, jaxName, maintainOffset=True, name=jarName + "_sc")[0]

                return jointList
