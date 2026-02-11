from maya.api import OpenMaya as om2

from cgrig.libs.hive.library.tools.commands.components import guide
from cgrig.libs.maya.utils import mayamath
from collections import OrderedDict
from cgrig.libs.utils import cgrigmath
from cgrig.libs.hive.base.definition import exprutils
from cgrig.libs.maya.cmds.objutils import attributes
from cgrig.libs.hive.library.subsystems import chainnetsubsystem
from cgrig.libs.maya.api import curves
from cgrig.libs.hive import api
import math
from cgrig.core.util import strutils
from cgrig.libs.maya import zapi


class ChainNetComponent(api.Component):
    creator = "David Sparrow"
    definitionName = "chainnetcomponent"
    uiData = {"icon": "componentFK", "iconColor": (), "displayName": "Chain Net"}
    documentation = "Forward Kinematics component"
    _jointNumPrefix = "bind"
    _fkNumPrefix = "fk"
    _ikNumPrefix = "ik"
    # primary translation axis which each new fk will generate along relative to the parent.
    _translationAxis = zapi.Vector(1, 0, 0)
    # default fk pivot rotation
    _rotationAxis = (0, 0, 0)
    # default rotation to apply to all created control shapes
    _shapeRotationAxis = (0, 0, (math.pi * 0.5))
    _firstIndexRotationOrder = zapi.kRotateOrder_XYZ
    _guideCurveInfluenceIds = (
        "startCurvePiv",
        "endCurvePiv"
    )
    _chainCrvAttributeName = "chainIkCrv"

    @classmethod
    def jointIdForNumber(cls, number):
        return cls._jointNumPrefix + str(number).zfill(2)

    @classmethod
    def ikJointIdForNumber(cls, number):
        return cls._ikNumPrefix + str(number).zfill(2)

    @classmethod
    def fkGuideIdForNumber(cls, number):
        return cls._fkNumPrefix + str(number).zfill(2)

    def idMapping(self):
        guideLayer = self.definition.guideLayer
        bindJointCount = guideLayer.guideSetting("jointCount").value

        deformIds = {}
        outputIds = {}
        inputIds = {}
        rigLayerIds = {}
        for index in range(bindJointCount):
            jntId = self.jointIdForNumber(index)
            deformIds[jntId] = jntId
            outputIds[jntId] = jntId

        for index in range(guideLayer.guideSetting("fkCtrlCount").value):
            ctrlId = self.fkGuideIdForNumber(index)
            rigLayerIds[ctrlId] = ctrlId

        return {
            api.constants.DEFORM_LAYER_TYPE: deformIds,
            api.constants.INPUT_LAYER_TYPE: inputIds,
            api.constants.OUTPUT_LAYER_TYPE: outputIds,
            api.constants.RIG_LAYER_TYPE: rigLayerIds,
        }

    def spaceSwitchUIData(self):
        driven = []
        drivers = [
            api.SpaceSwitchUIDriver(
                id_=api.pathAsDefExpression(("self", "inputLayer", "parent")),
                label="Parent Component",
                internal=True,
            ),
            api.SpaceSwitchUIDriver(
                id_=api.pathAsDefExpression(("self", "inputLayer", "world")),
                label="World Space",
                internal=True,
            ),
        ]

        guideLayerDef = self.definition.guideLayer

        for guide in guideLayerDef.iterGuides(includeRoot=False):
            name = strutils.titleCase(guide.id)
            driven.append(
                api.SpaceSwitchUIDriven(
                    id_=api.pathAsDefExpression(("self", "rigLayer", guide.id)),
                    label=name,
                )
            )
            drivers.append(
                api.SpaceSwitchUIDriver(
                    id_=api.pathAsDefExpression(("self", "rigLayer", guide.id)),
                    label=name,
                )
            )
        return {"driven": driven, "drivers": drivers}

    def updateGuideSettings(self, settings):
        originalGuideSettings = super(ChainNetComponent, self).updateGuideSettings(settings)
        if any(i in settings for i in ("jointCount", "fkCtrlCount")):
            # ensure the definition contains the latest scene state.
            # todo: starting to think we need to proxy the component class
            self.serializeFromScene(layerIds=api.constants.GUIDE_LAYER_TYPE)
            self.deleteGuide()
            self.rig.buildGuides([self])
        return originalGuideSettings

    def preSetupGuide(self):
        nameConfig = self.namingConfiguration()
        guideLayer = self.definition.guideLayer
        fkCtrlCount = guideLayer.guideSetting("fkCtrlCount").value
        bindJointCount = guideLayer.guideSetting("jointCount").value
        fkGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id.startswith(self._fkNumPrefix)
        ]
        ikGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id.startswith(self._ikNumPrefix)
        ]
        bindGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id.startswith(self._jointNumPrefix)
        ]

        currentFkGuideCount = max(0, len(fkGuides))
        currentBindGuideCount = max(0, len(bindGuides))
        fkParentGuide = guideLayer.guide("startCurvePiv")
        # handle FK
        # if the definition is the same as the required then just call the base
        # this will happen on a rebuild with a single guide count difference
        if currentFkGuideCount != fkCtrlCount:

            if currentFkGuideCount:
                [guideLayer.deleteGuides(fkGuides[i].id) for i in range(currentFkGuideCount)]

            self._createFkGuides(
                guideLayer,
                nameConfig,
                parentGuide=fkParentGuide,
                fkGuides=fkGuides,
                count=fkCtrlCount,
                )


        # handle Bind skeleton guides
        bindParent = guideLayer.guide("root")
        # if the definition is the same as the required then just call the base
        # this will happen on a rebuild with a single guide count difference
        if currentBindGuideCount != bindJointCount:
            # case where the new count is less than the current, in this case we just
            # delete the definition for the guide from the end.
            if bindJointCount < currentBindGuideCount:
                bindParent = bindGuides[bindJointCount].id
                guideLayer.deleteGuides(bindParent)
                # lerp and update the guide settings. 2.0 is the parameter length of mayas nurbs curve
                for index, uValue in enumerate(
                        cgrigmath.lerpCount(0.0, 1.0, bindJointCount)
                ):
                    guideId = self.jointIdForNumber(index)
                    self._createOrUpdateDistanceGuideSetting(
                        guideLayer, guideId, uValue
                    )

            else:
                # the parent for the fk is the end guide ie -1
                if currentBindGuideCount:
                    bindParent = bindGuides[-1]
                _, __ = self._createBindGuides(
                    guideLayer,
                    nameConfig,
                    parentGuide=bindParent,
                    bindGuides=bindGuides,
                    count=bindJointCount,
                )

        return super(ChainNetComponent, self).preSetupGuide()

    def _createOrUpdateDistanceGuideSetting(self, guideLayer, guideId, value):
        """internal helper method to generate the distance setting for a bind guide.
        This will either create one or update the existing definition value.

        :type guideLayer: :class:`api.GuideLayerDefinition`
        :type guideId: str
        :type value: float
        """
        distanceSettingName = "{}Distance".format(guideId)
        existingSetting = guideLayer.guideSetting(distanceSettingName)
        if not existingSetting:
            distanceSetting = api.AttributeDefinition(
                name="{}Distance".format(guideId),
                Type=zapi.attrtypes.kMFnNumericFloat,
                channelBox=True,
                keyable=False,
                value=value,
                max=1,
                min=0,
                default=value,
            )
            guideLayer.addGuideSetting(distanceSetting)
        else:
            existingSetting.value = value
            existingSetting.default = value

    def _createBindGuides(self, guideLayer, nameConfig, parentGuide, bindGuides, count):
        """

        :param guideLayer:
        :type guideLayer: :class:`api.GuideLayerDefinition`
        :param nameConfig:
        :type nameConfig:
        :param parentGuide:
        :type parentGuide:
        :param bindGuides:
        :type bindGuides:
        :param count:
        :type count:
        :return:
        :rtype:
        """
        bindGuidesIdMap = {i.id: i for i in bindGuides}

        compName, compSide = self.name(), self.side()
        guides = []
        # bind guides
        for index, value in enumerate(cgrigmath.lerpCount(0, 1, count)):
            guideId = self.jointIdForNumber(index)
            existingGuide = bindGuidesIdMap.get(guideId)

            transform = parentGuide.worldMatrix
            if not existingGuide:
                name = nameConfig.resolve(
                    "guideName",
                    {
                        "componentName": compName,
                        "side": compSide,
                        "id": guideId,
                        "type": "guide",
                    },
                )
                existingGuide = self._createGuide(
                    guideLayer,
                    name=name,
                    guideId=guideId,
                    worldMatrix=transform,
                    rotationOrder=parentGuide.rotateOrder,
                    parent=parentGuide.id,
                    shape=None,
                )
            else:
                form = zapi.TransformationMatrix(transform)
                existingGuide.translate = list(form.translation(zapi.kWorldSpace))
                existingGuide.rotate = list(form.rotation(asQuaternion=True))
                existingGuide.scale = list(form.scale(zapi.kWorldSpace))
                existingGuide.shapeTransform = transform
            self._createOrUpdateDistanceGuideSetting(guideLayer, guideId, value)

            guides.append(existingGuide)
            parentGuide = existingGuide
        return parentGuide, guides

    def _createFkGuides(self, guideLayer, nameConfig, parentGuide, fkGuides, count):
        fkGuidesIdMap = {i.id: i for i in fkGuides}
        sceneLayer = self.guideLayer()
        sceneGuides = {i.id(): i for i in sceneLayer.iterGuides(includeRoot=False)}
        fkCtrls = []
        compName, compSide = self.name(), self.side()
        startPosition, endPosition = (
            guideLayer.guide("startCurvePiv").translate,
            guideLayer.guide("endCurvePiv").translate,
        )
        parentId = "root"

        values = list(cgrigmath.lerpCount(0, 1, count))
        fkGuideList = []
        # fk guides
        for index, [position, _] in enumerate(
                mayamath.firstLastOffsetLinearPointDistribution(
                    zapi.Vector(startPosition), zapi.Vector(endPosition), count, offset=0.0
                )
        ):
            guideId = self.fkGuideIdForNumber(index)
            transform = zapi.TransformationMatrix()
            transform.setTranslation(position, zapi.kWorldSpace)
            name = nameConfig.resolve(
                "guideName",
                {
                    "componentName": compName,
                    "side": compSide,
                    "id": guideId,
                    "type": "guide",
                },
            )

            existingGuideDef = self._createGuide(
                guideLayer,
                name=name,
                guideId=guideId,
                worldMatrix=transform,
                rotationOrder=parentGuide.rotateOrder,
                pivotColor=[0.25, 1, 0],
                parent=parentId,
                pivotShape="cube",
                shape="sphere",
                scale_fraction=1.5
            )
            fkGuides.append(existingGuideDef)
            self._createOrUpdateDistanceGuideSetting(guideLayer, guideId, values[index])
            fkGuideList.append(existingGuideDef)
            parentGuide = existingGuideDef
            parentId = parentGuide.id

        return parentGuide, fkCtrls

    def _createGuide(
            self,
            guideLayer,
            name,
            guideId,
            parent,
            worldMatrix,
            rotationOrder,
            pivotColor=api.constants.DEFAULT_GUIDE_PIVOT_COLOR,
            shape="circle",
            pivotShape="sphere",
            scale_fraction=1.0,
    ):
        """

        :param guideLayer:
        :type guideLayer: :class:`api.GuideDefinition`
        :param name:
        :type name: str
        :param guideId:
        :type guideId: str
        :param parent:
        :type parent: str
        :param worldMatrix:
        :type worldMatrix: :class:`zapi.Matrix`
        :param rotationOrder:
        :type rotationOrder: int
        :param pivotColor:
        :type pivotColor: tuple
        :return:
        :rtype: :class:`api.GuideDefinition`
        """
        transform = zapi.TransformationMatrix(worldMatrix)
        scale = [sc*scale_fraction for sc in transform.scale(zapi.kWorldSpace)]
        return guideLayer.createGuide(
            name=name,
            shape=shape,
            id=guideId,
            parent=parent,
            color=(0.0, 0.5, 0.5),
            rotationOrder=rotationOrder,
            pivotShape=pivotShape,
            selectionChildHighlighting=self.configuration.selectionChildHighlighting,
            translate = transform.translation(zapi.kWorldSpace),
            rotate = [0,0,0.707,0.707],
            scale = transform.scale(zapi.kWorldSpace),
            shapeTransform=dict(
                translate=list(transform.translation(zapi.kWorldSpace)),
                rotation=list(transform.rotation(asQuaternion=True)),
                scale=scale,
            ),
            srts=[{"name": "_".join((guideId, "piv", "srt"))}],
            pivotColor=pivotColor,
        )

    def _purgeGuideMotionPaths(self, srtAttr, motionPathAttr):
        # delete any existing spline srts because it's much easier than diffing the scene.
        modifier = zapi.dagModifier()
        for splineSrtElement in srtAttr:
            sourceNode = splineSrtElement.sourceNode()
            if sourceNode is not None:
                sourceNode.delete(mod=modifier, apply=False)
        # delete any existing spline motionPaths because it's much easier than diffing the scene.
        for splineMotionPathsAttr in motionPathAttr:
            sourceNode = splineMotionPathsAttr.sourceNode()
            if sourceNode is not None:
                sourceNode.delete(mod=modifier, apply=False)
        modifier.doIt()

    def postSetupGuide(self):
        super(ChainNetComponent, self).postSetupGuide()
        guideLayer = self.guideLayer()
        definition = self.definition

        for guide in guideLayer.iterGuides(includeRoot=False):
            hasSpace = guide.attribute("hasSpaceSwitch")
            guideId = guide.id()
            if not guideId.startswith(self._fkNumPrefix):
                continue
            spaceName = "_".join((guideId, "space"))
            if hasSpace is None:
                guide.addAttribute(
                    name="hasSpaceSwitch",
                    Type=zapi.attrtypes.kMFnNumericBoolean,
                    default=True,
                    value=True,
                    channelBox=True,
                    keyable=False,
                )
            else:
                hasSpace = hasSpace.value()
                if not hasSpace:
                    continue
            existingSpaceSwitch = definition.spaceSwitchByLabel(spaceName)
            if existingSpaceSwitch:
                continue
            definition.createSpaceSwitch(
                label=spaceName,
                drivenId=api.pathAsDefExpression(("self", "rigLayer", guideId)),
                constraintType="orient",
                controlPanelFilter={
                    "default": "parent",
                    "group": {"name": "_", "label": "Space"},
                },
                permissions={"allowRename": False, "value": True},
                drivers=[
                    {
                        "label": "parent",
                        "driver": api.constants.ATTR_EXPR_INHERIT_TOKEN,
                        "permissions": {
                            "allowDriverChange": False,
                            "allowRename": False,
                        },
                    },
                    {
                        "label": "world",
                        "driver": api.pathAsDefExpression(
                            ("self", "inputLayer", "world")
                        ),
                        "permissions": {
                            "allowDriverChange": False,
                            "allowRename": False,
                        },
                    },
                ],
            )

        nameConfig = self.namingConfiguration()
        guideLayerTransform = guideLayer.rootTransform()
        guideSettingsDef = self.definition.guideLayer.guideSettings("jointCount", "fkCtrlCount")
        jointCount = guideSettingsDef["jointCount"].value
        fkCtrlCount = guideSettingsDef["fkCtrlCount"].value

        bindGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id().startswith(self._jointNumPrefix)
        ]
        fkGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id().startswith(self._fkNumPrefix)
        ]

        settingsNode = guideLayer.guideSettings()
        curve, extras = api.splineutils.createCurveFromDefinition(
            self.definition,
            layer=guideLayer,
            influences=guideLayer.findGuides(*self._guideCurveInfluenceIds),
            parent=guideLayerTransform,
            attributeName=self._chainCrvAttributeName,
            curveName="chainNet_crv",
            namingObject=nameConfig,
            namingRule="object",
            curveVisControlAttr=settingsNode.showCurveTemplate,
        )

        # track the srts created for attaching the spline
        splineSrtAttr = guideLayer.addAttribute(
            "splineSrts", Type=zapi.attrtypes.kMFnMessageAttribute, isArray=True
        )
        splineMotionPathsAttr = guideLayer.addAttribute(
            "splineMotionPaths", Type=zapi.attrtypes.kMFnMessageAttribute, isArray=True
        )

        guideLayer.addExtraNodes(extras + [curve])

        self._purgeGuideMotionPaths(splineSrtAttr, splineMotionPathsAttr)
        self._createMotionPaths(
            guideLayer,
            settingsNode,
            guideLayerTransform,
            bindGuides,
            curve,
            splineSrtAttr,
            splineMotionPathsAttr,
            jointCount,
        )
        self._createMotionPaths(
            guideLayer,
            settingsNode,
            guideLayerTransform,
            fkGuides,
            curve,
            splineSrtAttr,
            splineMotionPathsAttr,
            fkCtrlCount,
        )

    def _createMotionPaths(
            self,
            guideLayer,
            settingsNode,
            guideLayerTransform,
            bindGuides,
            curve,
            splineSrtAttr,
            splineMotionPathsAttr,
            jointCount,
    ):
        worldUpVectorGuide = guideLayer.guide("worldUpVec")
        for bindGuide, [srtTransform, motionPath] in zip(
                bindGuides,
                curves.iterGenerateSrtAlongCurve(
                    curve.shapes()[0].dagPath(),
                    jointCount,
                    "bindGuideSrt",
                    rotate=True,
                    fractionMode=True,
                ),
        ):
            aimVector = bindGuide.autoAlignAimVector.value()
            upVector = bindGuide.autoAlignUpVector.value()
            axisIndex, invert = mayamath.perpendicularAxisFromAlignVectors(
                aimVector, upVector
            )
            motionPathUpVector = mayamath.AXIS_VECTOR_BY_IDX[axisIndex]
            bindId = bindGuide.id()
            motionPath = zapi.DGNode(motionPath)
            srtTransform = zapi.nodeByObject(srtTransform)
            motionPath.worldUpType.set(2)
            motionPath.worldUpVector.set(motionPathUpVector)
            worldUpVectorGuide.attribute("worldMatrix")[0].connect(
                motionPath.worldUpMatrix
            )
            srtTransform.setParent(guideLayerTransform)
            guideLayer.connectToByPlug(
                splineSrtAttr.nextAvailableDestElementPlug(), srtTransform
            )
            guideLayer.connectToByPlug(
                splineMotionPathsAttr.nextAvailableDestElementPlug(), motionPath
            )
            guideSrt = bindGuide.srt()
            for attr in ("XYZ"):
                attributes.lockAttr(guideSrt.name(), "translate" + attr, lock=False)
                attributes.lockAttr(guideSrt.name(), "rotate" + attr, lock=False)

            guideSrt.setWorldMatrix(srtTransform.worldMatrix())
            with zapi.lockStateAttrContext(bindGuide, zapi.localTransformAttrs, False):
                bindGuide.resetTransform(scale=False)

            _buildJntConstraint(
                guideSrt,
                [srtTransform],
                guideLayer,
                scale=False,
                constraintType=(
                    "parent"
                    if bindId
                       not in (
                           self.jointIdForNumber(0),
                           self.jointIdForNumber(jointCount - 1),
                       )
                    else "point"
                ),
            )
            guideLayer.addExtraNodes((motionPath, srtTransform))

            distanceSetting = settingsNode.attribute(
                "{}Distance".format(bindGuide.id())
            )
            if distanceSetting.value() == 0.0:
                distanceSetting.set(motionPath.uValue.value().value)
            distanceSetting.connect(motionPath.uValue)

    def postMirror(self, translate=("x",), rotate="yz", parent=om2.MObject.kNullObj):
        guideLayer = self.guideLayer()
        bindGuides = [
            i
            for i in guideLayer.iterGuides(includeRoot=False)
            if i.id().startswith(self._jointNumPrefix)
        ]
        for bindGuide in bindGuides:
            with zapi.lockStateAttrContext(bindGuide, zapi.localTransformAttrs, False):
                bindGuide.resetTransform(scale=False)

    def setupInputs(self):
        super(ChainNetComponent, self).setupInputs()
        layer = self.inputLayer()
        if layer:
            inputNode = layer.inputNode("parent")
            inputNode.resetTransform()

    def setupDeformLayer(self, parentJoint=None):
        for system in self.subsystems().values():
            system.setupDeformLayer(parentJoint)
        super(ChainNetComponent, self).setupDeformLayer(parentJoint)

    def setupOutputs(self, parentNode):
        for system in self.subsystems().values():
            system.setupOutputs(parentNode)
        super(ChainNetComponent, self).setupOutputs(parentNode)
        self._connectOutputs()

    def _connectOutputs(self):
        # connect the outputs to the deform layer
        layer = self.outputLayer()
        hasJoints = self.definition.guideLayer.guideSetting("hasJoints").value
        if not hasJoints:
            return
        sourceNodes = {jnt.id(): jnt for jnt in self.deformLayer().joints()}

        for index, output in enumerate(layer.outputs()):
            driver = sourceNodes.get(output.id())
            if not driver:
                continue
            zapi.buildConstraint(output, {"targets": [("", driver)]}, constraintType="parent",
                                 trace=False, maintainOffset=False)
            zapi.buildConstraint(output, {"targets": [("", driver)]}, constraintType="scale",
                                 trace=False, maintainOffset=True)

    def preSetupRig(self, parentNode):
        for system in self.subsystems().values():
            system.preSetupRig(parentNode)
        super(ChainNetComponent, self).preSetupRig(parentNode)

    def createSubSystems(self):
        systems = OrderedDict()
        systems["chainnet"] = chainnetsubsystem.chainnetSubsystem(
            self
        )
        return systems

    def setupRig(self, parentNode):
        for system in self.subsystems().values():
            system.setupRig(parentNode)

    def connect_master(self, mstr_out, slave_in, idx, percent_attr, rev_bias=False):
        """Connect master and slave chain
        """
        # we need to check if  master have enought sections
        # if  connection is out of index, will fallback to the latest
        # section in the master
        outs = []
        if (idx) > len(mstr_out) - 1:
            mstr_e = len(mstr_out) - 1
        else:
            mstr_e = idx
        m_out = mstr_out[mstr_e]
        s_in = slave_in[idx]

        if rev_bias:
            rev = zapi.createDG(m_out.name()+"_rev", "reverse")
            percent_attr.connect(rev.attribute("inputX"))
            bias = rev.attribute("outputX")
            outs.append(rev)
        else:
            bias = percent_attr
        for srt in ["rotate", "translate"]:
            plus = zapi.createDG(m_out.name()+"_plus", "plusMinusAverage")
            m_out.attribute(srt).connect(plus.attribute("input3D[0]"))
            m_out.srt(3).attribute(srt).connect(plus.attribute("input3D[1]"))
            m_out.srt(4).attribute(srt).connect(plus.attribute("input3D[2]"))

            m_node = zapi.createDG(m_out.name()+"_mult", "multiplyDivide")
            plus.attribute("output3Dx").connect(m_node.attribute("input1X"))
            plus.attribute("output3Dy").connect(m_node.attribute("input1Y"))
            plus.attribute("output3Dz").connect(m_node.attribute("input1Z"))
            bias.connect(m_node.attribute("input2X"))
            bias.connect(m_node.attribute("input2Y"))
            bias.connect(m_node.attribute("input2Z"))
            m_node.attribute("outputX").connect(s_in.attribute(srt + "X"))
            m_node.attribute("outputY").connect(s_in.attribute(srt + "Y"))
            m_node.attribute("outputZ").connect(s_in.attribute(srt + "Z"))
            outs += [plus, m_node]
        return outs

    def setChainDriver(self, drivenId, driverExpression):
        """

        :param drivenId:
        :type drivenId: str
        :param driverExpression:
        :type driverExpression: str
        """
        defini = self.definition
        defini.createDriver(api.constants.DRIVER_TYPE_MATRIX, drivenId, api.DriverMatrixConstParams(
            drivers=[("", driverExpression)],
            driven=api.pathAsDefExpression(("self", "inputLayer", drivenId)),
            maintainOffset=False
        ))
        self.saveDefinition(defini)

    def postPolish(self):
        super(ChainNetComponent, self).postPolish()
        rigLayer = self.rigLayer()
        controlPanel = self.controlPanel()
        drivers = self.definition.drivers
        extras = list()
        ikCtrls = list()
        ik_a_in = list()
        ik_b_in = list()
        fkCtrls = list()
        fk_a_in = list()
        fk_b_in = list()

        for ctrl in rigLayer.iterControls():
            for attr in ("XYZ"):
                attributes.lockAttr(ctrl.srt(1).name(), "translate"+attr, lock=False)
                attributes.lockAttr(ctrl.srt(2).name(), "translate"+attr, lock=False)
                attributes.lockAttr(ctrl.srt(1).name(), "rotate"+attr, lock=False)
                attributes.lockAttr(ctrl.srt(2).name(), "rotate"+attr, lock=False)

            if ctrl.id().startswith("fk"):
                fkCtrls.append(ctrl)
                fk_a_in.append(ctrl.srt(1))
                fk_b_in.append(ctrl.srt(2))
            if ctrl.id().startswith("ik"):
                ikCtrls.append(ctrl)
                ik_a_in.append(ctrl.srt(1))
                ik_b_in.append(ctrl.srt(2))

        mst_a = None
        mst_b = None

        if drivers:
            percent_val = self.definition.guideLayer.guideSetting("percent").value/100.0
            controlPanel.attribute("bend").set(percent_val)
            mst_a_driver = drivers[0].serialize()["params"]["drivers"][0][-1]
            mst_b_driver = drivers[1].serialize()["params"]["drivers"][0][-1]
            exp_a = exprutils.splitAttrExpression(mst_a_driver)
            exp_b = exprutils.splitAttrExpression(mst_b_driver)
            name_a = exp_a[0].split(":")[0]
            name_b = exp_b[0].split(":")[0]
            componentLayer = self.rig.componentLayer()
            compRegistry = self.configuration.componentRegistry()
            comps = {}
            for comp in componentLayer.iterComponents():
                comp = compRegistry.fromMetaNode(rig=self, metaNode=comp)
                comps[comp.name()] = comp
            if name_a in comps:
                mst_a = comps[name_a]
            if name_b in comps:
                mst_b = comps[name_b]
            if not mst_a or not mst_b:
                return

            mst_a_iks = [ctrl for ctrl in mst_a.rigLayer().iterControls() if ctrl.id().startswith("ik")]
            mst_a_fks = [ctrl for ctrl in mst_a.rigLayer().iterControls() if ctrl.id().startswith("fk")]
            mst_b_iks = [ctrl for ctrl in mst_b.rigLayer().iterControls() if ctrl.id().startswith("ik")]
            mst_b_fks = [ctrl for ctrl in mst_b.rigLayer().iterControls() if ctrl.id().startswith("fk")]
            for e, ctrl in enumerate(fkCtrls):
                a_outs = self.connect_master(mst_a_fks,
                                    fk_a_in,
                                    e,
                                    controlPanel.attribute("bend"))
                b_outs = self.connect_master(mst_b_fks,
                                    fk_b_in,
                                    e,
                                    controlPanel.attribute("bend"),
                                    rev_bias=True)
                rigLayer.addExtraNodes(a_outs)
                rigLayer.addExtraNodes(b_outs)

            for e, ctrl in enumerate(ikCtrls):
                a_outs = self.connect_master(mst_a_iks,
                                    ik_a_in,
                                    e,
                                    controlPanel.attribute("bend"))
                b_outs = self.connect_master(mst_b_iks,
                                    ik_b_in,
                                    e,
                                    controlPanel.attribute("bend"),
                                    rev_bias=True)
                rigLayer.addExtraNodes(a_outs)
                rigLayer.addExtraNodes(b_outs)

def _buildJntConstraint(driven, targets, layer, scale=True, constraintType="parent"):
    targets = [
        (i.fullPathName(partialName=True, includeNamespace=False), i) for i in targets
    ]
    parentConstraint, parentUtilities = api.buildConstraint(
        driven,
        drivers={"targets": targets},
        constraintType=constraintType,
        maintainOffset=True,
        trace=False,
    )
    scaleConstraint, scaleUtilities = None, []
    if scale:
        scaleConstraint, scaleUtilities = api.buildConstraint(
            driven,
            drivers={"targets": targets},
            constraintType="scale",
            maintainOffset=True,
            trace=False,
        )

    layer.addExtraNodes(parentUtilities + scaleUtilities)
    return parentConstraint, scaleConstraint













