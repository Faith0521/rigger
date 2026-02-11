from cgrig.libs.hive import api
from cgrig.libs.hive.base.serialization import graphconstants
from cgrig.libs.maya import zapi
from cgrig.libs.hive.base import basesubsystem, definition
from cgrig.libs.utils import cgrigmath
from maya import cmds


class VolumePreservationSubsystem(basesubsystem.BaseSubsystem):
    """
    """

    def __init__(self, component,
                 systemPrefix,
                 ctrlIds, jointIds,
                 activeStateAttrName,
                 initializeLengthConstantAttr=(),
                 reverseVolumeValues=False,
                 showVolumeAttrsInChannelBox=False):
        super(VolumePreservationSubsystem, self).__init__(component)
        self.systemPrefix = systemPrefix
        self.ctrlIds = ctrlIds
        self.jointIds = jointIds
        self.volumeAttrName = "globalVolume"
        self.volumeMultiplierAttrPrefix = "volume"
        self.curveNode = None
        self.reverseVolumeValues = reverseVolumeValues
        self.attrsInsertAfterName = "lowerStretch"
        self.animCurveSquashSettingAttr = "squashCurveNode"
        self.showVolumeAttrsInChannelBoxName = "displayVolumeAttrsChannelBox"
        self.showVolumeAttrsInChannelBox = showVolumeAttrsInChannelBox
        # used to determine if this subsystem should be active
        self.activeStateAttrName = activeStateAttrName
        # tuple first element the constant node id, second element the attrName
        self.initialLengthConstantAttr = initializeLengthConstantAttr

    def active(self):
        """Whether this subsystem should build,align etc. This is based on the required "activeStateAttrName" variable.

        :rtype: bool
        """
        return self.component.definition.guideLayer.guideSetting(
            self.activeStateAttrName
        ).value

    def squashCurve(self):
        return self.component.meta.sourceNodeByName(self.animCurveSquashSettingAttr)

    def postSetupGuide(self):
        if not self.active():
            return
        animCurveSquashSettingAttr = self.component.meta.addAttribute(self.animCurveSquashSettingAttr,
                                                                      Type=zapi.attrtypes.kMFnMessageAttribute)
        squashCurve = animCurveSquashSettingAttr.sourceNode()  # type: zapi.AnimCurve
        keyCount = len(self.jointIds) - 1

        if squashCurve is None:
            namingConfig = self.component.namingConfiguration()
            # create the animation squash curve node which the user can interact with
            squashCurve = api.splineutils.createSquashGuideCurve(
                namingConfig.resolve("object", {"componentName": self.component.name(),
                                                "side": self.component.side(),
                                                "section": "squashCurve",
                                                "type": "animCurve"},
                                     ), [0, keyCount * 0.5, keyCount], [0, 0.8, 1])
            self.component.meta.connectToByPlug(animCurveSquashSettingAttr, squashCurve)
            container = self.component.container()
            if container is not None:
                container.addNode(squashCurve)
                container.publishNode(squashCurve)

    def preSetupRig(self, parentNode):
        if not self.active():
            return
        settings = [
            {
                "name": "________",
                "value": 0,
                "enums": ["VOLUME"],
                "keyable": False,
                "locked": True,
                "channelBox": True,
                "Type": zapi.attrtypes.kMFnkEnumAttribute,
            },
            {
                "name": self.volumeAttrName,
                "Type": zapi.attrtypes.kMFnNumericFloat,
                "channelBox": False,
                "default": 0,
                "keyable": True,
                "max": 1.0,
                "min": 0.0,
                "value": 0
            }]

        settings.extend(self._createSquashCurveSettings())
        rigLayerDef = self.component.definition.rigLayer
        rigLayerDef.insertSettings(api.constants.CONTROL_PANEL_TYPE,
                                   rigLayerDef.settingIndex("controlPanel",
                                                            self.attrsInsertAfterName) + 1,
                                   settings)

    def _createSquashCurveSettings(self):
        squashCurve = self.squashCurve()
        constantSettings = []
        values = [squashCurve.mfn().evaluate(zapi.Time(i, zapi.Time.k24FPS)) for i in range(len(self.ctrlIds))]
        if self.reverseVolumeValues:
            values.reverse()
        for i, ctrlId in enumerate(self.ctrlIds):
            name = "_".join((self.volumeMultiplierAttrPrefix, ctrlId))
            kwargs = {"name": name,
                      "Type": zapi.attrtypes.kMFnNumericFloat,
                      "value": values[i]}
            if self.showVolumeAttrsInChannelBox:
                kwargs["channelBox"] = True
                kwargs["keyable"] = True

            constantSettings.append(kwargs)
        return constantSettings

    def setupRig(self, parentNode):
        if not self.active():
            return
        rigLayer = self.component.rigLayer()
        deformLayer = self.component.deformLayer()
        controlPanel = rigLayer.controlPanel()
        namingConfig = self.component.namingConfiguration()
        curve = self.curveNode.shapes()[0]
        ctrls = rigLayer.findControls(*self.ctrlIds)
        joints = deformLayer.findJoints(*self.jointIds)
        curveOut = curve.attribute("worldSpace")[0]
        curveInfo = zapi.createDG(curve.name() + "_length", "curveInfo")
        curveOut.connect(curveInfo.inputCurve)
        curveInfoOutput = curveInfo.attribute("arcLength")
        extras = [curveInfo]
        constantsNode = rigLayer.settingNode(self.initialLengthConstantAttr[0])
        initialLengthAttribute = constantsNode.attribute(self.initialLengthConstantAttr[1])

        animVolumeAttr = controlPanel.attribute(self.volumeAttrName)
        squashPlugs = []
        for ctrlId in self.ctrlIds:
            squashPlug = controlPanel.attribute("_".join((self.volumeMultiplierAttrPrefix, ctrlId)))
            squashPlugs.append(squashPlug)
        index = 0
        count = len(self.ctrlIds)
        positionValues = [value for value in cgrigmath.lerpCount(0, 1, count)] if count > 1 else [1.0]
        compName, compSide = self.component.name(), self.component.side()

        decompose = zapi.createDG(
            namingConfig.resolve(
                "object",
                {
                    "componentName": compName,
                    "side": compSide,
                    "section": self.systemPrefix + "GlobalScale",
                    "type": "expression",
                },
            ),
            "decomposeMatrix",
        )
        outMel = _MEL_SEGMENT_GLOBALS.format(
            initialLengthAttr=initialLengthAttribute.fullPathName(),
            globalScaleNode=decompose.fullPathName()
        )
        for ctrlId, twistJoint, ctrl in zip(self.ctrlIds, joints, ctrls):
            remapValue = zapi.createDG(namingConfig.resolve("object",
                                                             {
                                                                 "componentName": compName, "side": compSide,
                                                                 "section": ctrlId+"BlendyScaleCache",
                                                                 "type": "remapValue",
                                                             }),
                                       "remapValue")
            remapValue.inputValue.set(index)
            remapValue.inputMax.set(count)
            remapValue.outputMax.set(count)
            self._dumpCurveData(positionValues, squashPlugs, remapValue)
            ctrl.worldMatrixPlug().connect(decompose.inputMatrix)
            localScale = ctrl.attribute("scale")
            outScale = twistJoint.attribute("scale")
            outMel += "\n"+_MEL_PER_NODE.format(
                inputLength=curveInfoOutput.fullPathName(),
                volumeAttr=animVolumeAttr.fullPathName(),
                curveRemapAttr=remapValue.outValue.fullPathName(),
                squashValueMultAttr="0.2",
                localScaleX=localScale[0].fullPathName(),
                localScaleY=localScale[1].fullPathName(),
                localScaleZ=localScale[2].fullPathName(),
                outputAttrX=outScale[0].fullPathName(),
                outputAttrY=outScale[1].fullPathName(),
                outputAttrZ=outScale[2].fullPathName(),
                varPrefix=ctrlId
            )

            extras.append(remapValue)
            index += 1
        expr = cmds.expression(
            name=namingConfig.resolve(
                "object",
                {
                    "componentName": compName,
                    "side": compSide,
                    "section": self.systemPrefix + "Preservation",
                    "type": "expression",
                },
            ),
            alwaysEvaluate=False,
            string=outMel,
        )
        rigLayer.addExtraNodes(extras+[zapi.nodeByName(expr), decompose])

    def _dumpCurveData(self, positions, volumeAttrs, remap):
        for index, [pos, vol] in enumerate(zip(positions, volumeAttrs)):
            valueElement = remap.value[index]
            valueElement.child(0).set(pos)
            vol.connect(valueElement.child(1))
            valueElement.child(2).set(3)

# globals inputs per segment
_MEL_SEGMENT_GLOBALS = """
float $initialLength = abs({initialLengthAttr});
float $globalScaleX = {globalScaleNode}.outputScaleX;
float $globalScaleY = {globalScaleNode}.outputScaleY;
float $globalScaleZ = {globalScaleNode}.outputScaleZ;
"""

_MEL_PER_NODE = """
float ${varPrefix}SquashValue = {curveRemapAttr} * {squashValueMultAttr};
// negative length  can occur with mirrored limb


float ${varPrefix}GlobalScaleNormalizedX = $initialLength / {inputLength} * $globalScaleX; 
float ${varPrefix}GlobalScaleNormalizedY = $initialLength / {inputLength} * $globalScaleY; 
float ${varPrefix}GlobalScaleNormalizedZ = $initialLength / {inputLength} * $globalScaleZ;
// solve negative scale ensure pow is called with absolute value before multiplying back to signed value
float ${varPrefix}SignX = (${varPrefix}GlobalScaleNormalizedX < 0) ? -1 : 1;
float ${varPrefix}SignY = (${varPrefix}GlobalScaleNormalizedY < 0) ? -1 : 1;
float ${varPrefix}SignZ = (${varPrefix}GlobalScaleNormalizedZ < 0) ? -1 : 1;

float ${varPrefix}PowX = ${varPrefix}SignX * pow(abs(${varPrefix}GlobalScaleNormalizedX), ${varPrefix}SquashValue);
float ${varPrefix}PowY = ${varPrefix}SignY * pow(abs(${varPrefix}GlobalScaleNormalizedY), ${varPrefix}SquashValue);
float ${varPrefix}PowZ = ${varPrefix}SignZ * pow(abs(${varPrefix}GlobalScaleNormalizedZ), ${varPrefix}SquashValue);

{outputAttrX} = (${varPrefix}PowX * {volumeAttr}) + ((1.0 - {volumeAttr}) * {localScaleX});
{outputAttrY} = (${varPrefix}PowY * {volumeAttr}) + ((1.0 - {volumeAttr}) * {localScaleY});
{outputAttrZ} = (${varPrefix}PowZ * {volumeAttr}) + ((1.0 - {volumeAttr}) * {localScaleZ});
"""
