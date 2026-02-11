from cgrig.libs.hive import api
from cgrig.libs.maya import zapi
from cgrig.libs.hive.base import basesubsystem
from cgrig.libs.hive.base.serialization import graphconstants


class chainnetSubsystem(basesubsystem.BaseSubsystem):
    """Generic Chainnet Subsystem which only handles the creation of Chainnet rig controls
    """
    _jointNumPrefix = "bind"
    _fkNumPrefix = "fk"
    _ikNumPrefix = "ik"
    def __init__(self, component):
        super(chainnetSubsystem, self).__init__(component)

    def setupDeformLayer(self, parentJoint):
        nameConfig = self.component.namingConfiguration()
        # build skin joints if any
        definition = self.component.definition
        deformLayerDef = definition.deformLayer
        guideLayer = definition.guideLayer
        hasJoints = guideLayer.guideSetting("hasJoints").value
        compName, compSide = self.component.name(), self.component.side()
        parentNode = None
        deformLayerDef.clearJoints()
        if hasJoints:
            for guide in guideLayer.iterGuides(includeRoot=False):
                guideId = guide.id
                if not guideId.startswith(self._jointNumPrefix):
                    continue
                name = nameConfig.resolve(
                    "skinJointName",
                    {
                        "componentName": compName,
                        "side": compSide,
                        "id": guideId,
                        "type": "joint",
                    },
                )
                deformLayerDef.createJoint(
                    name=name,
                    id=guideId,
                    translate=guide.translate,
                    rotate=guide.rotate,
                    rotateOrder=guide.rotateOrder,
                    parent=parentNode,
                )
                parentNode = guide.id

    def setupOutputs(self, parentNode):
        deformLayer = self.component.definition.deformLayer  # type: api.DeformLayerDefinition
        outputLayer = self.component.definition.outputLayer  # type: api.OutputLayerDefinition
        nameConfig = self.component.namingConfiguration()
        compName, compSide = self.component.name(), self.component.side()
        parent = None
        outputLayer.clearOutputs()
        for jnt in deformLayer.iterDeformJoints():
            jntId = jnt.id
            name = nameConfig.resolve(
                "outputName",
                {
                    "componentName": compName,
                    "side": compSide,
                    "id": jntId,
                    "type": "joint",
                },
            )
            outputLayer.createOutput(id=jntId, name=name, parent=parent)

    def preSetupRig(self, parentNode):
        spaceSwitches = {i.label: i for i in self.component.definition.spaceSwitching}
        for guide in self.component.definition.guideLayer.iterGuides(includeRoot=False):
            if not guide.id.startswith(self._fkNumPrefix):
                continue
            hasSpace = guide.attribute("hasSpaceSwitch")
            if not hasSpace:
                continue
            spaceSwitch = spaceSwitches.get("_".join((guide.id, "space")))
            if not spaceSwitch:
                continue
            spaceSwitch.active = hasSpace.value

    def setupRig(self, parentNode):
        definition = self.component.definition
        guideLayerDef = definition.guideLayer
        rigLayer = self.component.rigLayer()
        idMapping = self.component.idMapping()
        naming = self.component.namingConfiguration()
        deformLayer = self.component.deformLayer()
        inputLayer = self.component.inputLayer()
        outputLayer = self.component.outputLayer()
        rigLayerRoot = rigLayer.rootTransform()
        compName, compSide = self.component.name(), self.component.side()
        rootTransform = rigLayer.rootTransform()
        controlPanel = self.component.controlPanel()
        graphRegistry = self.component.configuration.graphRegistry()
        localTGraphData = graphRegistry.graph(graphconstants.kMotionPathCns)
        localTGraphName = localTGraphData.name
        controls = {}  # guideId: [node, parentId]
        extras = []
        div_cns = []
        upv_cns = []
        lvls = []
        # note controls default parent is the root transform, the appropriate parent will be set after
        # this is because iterGuides is in creation order which may not be the real order meaning the parent
        # may not be created yet.
        hasControls = guideLayerDef.guideSetting("hasControls")
        jointCount = guideLayerDef.guideSetting("jointCount").value
        if hasControls is not None and not hasControls.value:
            return
        fkGuides = [
            i
            for i in guideLayerDef.iterGuides(includeRoot=False)
            if i.id.startswith(self._fkNumPrefix)
        ]
        bindGuides = [
            i
            for i in guideLayerDef.iterGuides(includeRoot=False)
            if i.id.startswith(self._jointNumPrefix)
        ]

        for index, guidDef in enumerate(fkGuides):
            ctrlName = naming.resolve(
                "controlName",
                {
                    "componentName": compName,
                    "side": compSide,
                    "id": guidDef.id,
                    "type": "control",
                },
            )
            ikCtrlName = naming.resolve(
                "controlName",
                {
                    "componentName": compName,
                    "side": compSide,
                    "id": guidDef.id.replace("fk", "ik"),
                    "type": "control",
                },
            )
            scale, _ = guidDef.mirrorScaleVector()
            ctrl = rigLayer.createControl(
                name=ctrlName,
                id=guidDef.id,
                translate=guidDef.translate,
                rotate=guidDef.rotate,
                scale=scale,
                shape=guidDef.shape,
                rotateOrder=guidDef.rotateOrder,
                selectionChildHighlighting=self.component.configuration.selectionChildHighlighting,
                srts=[{"id": guidDef.id, "name": "_".join([ctrlName, "srt"])},
                      {"id": guidDef.id, "name": "_".join([ctrlName, "a_in"])},
                      {"id": guidDef.id, "name": "_".join([ctrlName, "b_in"])},
                      {"id": guidDef.id, "name": "_".join([ctrlName, "driven"])},
                      {"id": guidDef.id, "name": "_".join([ctrlName, "sdk"])}],
            )

            ik_ctrl = rigLayer.createControl(
                name=ikCtrlName,
                id=guidDef.id.replace("fk", "ik"),
                translate=guidDef.translate,
                rotate=guidDef.rotate,
                scale=scale,
                shape='cube',
                parent=guidDef.id,
                rotateOrder=guidDef.rotateOrder,
                selectionChildHighlighting=self.component.configuration.selectionChildHighlighting,
                srts=[{"id": guidDef.id.replace("fk", "ik"), "name": "_".join([ikCtrlName, "srt"])},
                      {"id": guidDef.id.replace("fk", "ik"), "name": "_".join([ikCtrlName, "a_in"])},
                      {"id": guidDef.id.replace("fk", "ik"), "name": "_".join([ikCtrlName, "b_in"])},
                      {"id": guidDef.id.replace("fk", "ik"), "name": "_".join([ikCtrlName, "driven"])},
                      {"id": guidDef.id.replace("fk", "ik"), "name": "_".join([ikCtrlName, "sdk"])}
                      ]
            )

            controls[guidDef.id] = (ctrl, guidDef.parent)
            controls[guidDef.id.replace("fk", "ik")] = (ik_ctrl, guidDef.id)

        # Handle reparenting all controls into correct hierarchy
        for ctrlId, (childCtrl, parentId) in controls.items():
            parent = controls.get(parentId)
            if not parent:
                parent = rigLayerRoot
            else:
                parent = parent[0]
            childCtrl.setParent(parent, maintainOffset=True)

        joints = {i.id(): i for i in deformLayer.iterJoints()}
        outputs = {i.id(): i for i in outputLayer.outputs()}
        rootInputNode = inputLayer.inputNode("parent")
        jointMapping = idMapping[api.constants.DEFORM_LAYER_TYPE]
        outputMapping = idMapping[api.constants.OUTPUT_LAYER_TYPE]
        hasJoints = guideLayerDef.guideSetting("hasJoints").value
        parentNode = parentNode
        hasControls = guideLayerDef.guideSetting("hasControls")
        if hasControls is not None and not hasControls.value:
            super(chainnetSubsystem, self).postSetupRig(parentNode)
            return

        ikCtrls = list()
        ik_a_in = list()
        ik_b_in = list()
        fkCtrls = list()
        fk_a_in = list()
        fk_b_in = list()

        for ctrl in rigLayer.iterControls():
            if ctrl.id().startswith("fk"):
                fkCtrls.append(ctrl)
                fk_a_in.append(ctrl.srt(1))
                fk_b_in.append(ctrl.srt(2))
            if ctrl.id().startswith("ik"):
                ikCtrls.append(ctrl)
                ik_a_in.append(ctrl.srt(1))
                ik_b_in.append(ctrl.srt(2))

        # add Objects
        for index, ikCtrl in enumerate(ikCtrls):
            lvl = zapi.createDag(name=ikCtrl.name() + "_lvl", nodeType="transform", parent=ikCtrl)
            lvl.attribute("translateZ").set(0.01)
            lvls.append(lvl)


        for index in range(jointCount):
            div_cn_name = naming.resolve("object", {"componentName": compName,
                                                    "side": compSide,
                                                    "section": "div_{}".format(index),
                                                    "type": "transform"})
            div_up_cn_name = div_cn_name.replace("div", "div_up")
            div_cn = zapi.createDag(name=div_cn_name, nodeType="transform", parent=rootTransform)
            div_up_cn = zapi.createDag(name=div_up_cn_name, nodeType="transform", parent=rootTransform)
            div_cns.append(div_cn)
            upv_cns.append(div_up_cn)

        extras += div_cns + upv_cns + lvls

        points = [guide.translate for guide in fkGuides]

        mst_curveName = naming.resolve("object", {"componentName": compName,
                                                  "side": compSide,
                                                  "section": "mst_curve",
                                                  "type": "curve"})
        upv_curveName = mst_curveName.replace("mst_curve", "upv_curve")

        mstCurveTransform, _ = zapi.nurbsCurveFromPoints(mst_curveName, points)
        upvCurveTransform, _ = zapi.nurbsCurveFromPoints(upv_curveName, points)

        mstCurveTransform.rename(mst_curveName)
        mstCurveTransform.setParent(rootTransform)
        upvCurveTransform.rename(upv_curveName)
        upvCurveTransform.setParent(rootTransform)
        mstCurveTransform.attribute("visibility").set(0)
        upvCurveTransform.attribute("visibility").set(0)

        mstPrimaryCurveShape = mstCurveTransform.shapes()[0]
        mstControlPointsAttr = mstPrimaryCurveShape.attribute("controlPoints")
        for index, ikCtrl in enumerate(ikCtrls):
            decompName = naming.resolve("object", {"componentName": compName,
                                                   "side": compSide,
                                                   "section": ikCtrl.name(),
                                                   "type": "decomposeMatrix"})
            decompose = zapi.createDG(decompName, "decomposeMatrix")
            ikCtrl.attribute("worldMatrix")[0].connect(decompose.inputMatrix)
            decompose.outputTranslate.connect(mstControlPointsAttr[index])
            extras.append(decompose)

        upvPrimaryCurveShape = upvCurveTransform.shapes()[0]
        upvControlPointsAttr = upvPrimaryCurveShape.attribute("controlPoints")
        for index, lvl in enumerate(lvls):
            decompName = naming.resolve("object", {"componentName": compName,
                                                   "side": compSide,
                                                   "section": lvl.name(),
                                                   "type": "decomposeMatrix"})
            decompose = zapi.createDG(decompName, "decomposeMatrix")
            lvl.attribute("worldMatrix")[0].connect(decompose.inputMatrix)
            decompose.outputTranslate.connect(upvControlPointsAttr[index])
            extras.append(decompose)

        mst_arclen_name = naming.resolve("object", {"componentName": compName,
                                                    "side": compSide,
                                                    "section": "mstArclenLength",
                                                    "type": "transform"})

        root_decompose = zapi.createDG(mst_arclen_name.replace("mstArclenLength", "rootDecompose"), "decomposeMatrix")
        rootInputNode.attribute("worldMatrix")[0].connect(root_decompose.attribute("inputMatrix"))

        mst_curveOut = mstPrimaryCurveShape.attribute("worldSpace")[0]
        mst_curveInfo = zapi.createDG(mst_arclen_name, "curveInfo")
        mst_curveOut.connect(mst_curveInfo.inputCurve)
        alAttr = mst_curveInfo.attribute("arcLength").value().value

        ration_node = zapi.createDG(mst_arclen_name.replace("mstArclenLength", "rationMult"), "multiplyDivide")
        controlPanel.attribute("length_ratio").connect(ration_node.attribute("input1X"))
        ration_node.attribute("input2X").set(alAttr)

        mstCurveTransform.addAttribute("length_ratio",
                                       Type=zapi.attrtypes.kMFnNumericFloat,
                                       min=1.0, max=10.0, value=1.0,
                                       channelBox=True, keyable=False)
        length_div = zapi.createDG(mst_arclen_name.replace("mstArclenLength", "lengthDiv"), "multiplyDivide")
        length_div.attribute("operation").set(2)
        mst_curveInfo.attribute("arcLength").connect(length_div.attribute("input1X"))
        ration_node.attribute("outputX").connect(length_div.attribute("input2X"))
        length_div.attribute("outputX").connect(mstCurveTransform.attribute("length_ratio"))

        div_scl_node = zapi.createDG(mst_arclen_name.replace("mstArclenLength", "sclDiv"), "multiplyDivide")
        div_scl_node.attribute("operation").set(2)
        mstCurveTransform.attribute("length_ratio").connect(div_scl_node.attribute("input1X"))
        root_decompose.attribute("outputScaleX").connect(div_scl_node.attribute("input2X"))

        u = 0.000
        step = 1.000 / (jointCount - 1)

        for i in range(len(ikCtrls)):
            controlPanel.attribute("ikVis").connect(ikCtrls[i].shapes()[0].attribute("visibility"))
            controlPanel.attribute("fkVis").connect(fkCtrls[i].shapes()[0].attribute("visibility"))


        for i in range(jointCount):
            localTGraphData.name = localTGraphName + "motion_{}".format(i)
            sceneGraph = self.createGraph(rigLayer, localTGraphData)
            motionDiv = sceneGraph.node("motionScale")
            divUpMotionNode = sceneGraph.node("divUp")
            divMotionNode = sceneGraph.node("divPos")
            motionDiv.attribute("input1X").set(u)

            motionDivInAttr = sceneGraph.inputAttr("motionScaleInput2X")[0]
            motionDivWdAttr = sceneGraph.inputAttr("motionDivWorldUpMatrix")[0]
            upv_cns[i].attribute("worldMatrix")[0].connect(motionDivWdAttr)

            div_scl_node.attribute("outputX").connect(motionDivInAttr)
            upvPrimaryCurveShape.attribute("worldSpace")[0].connect(divUpMotionNode.attribute("geometryPath"))
            mstPrimaryCurveShape.attribute("worldSpace")[0].connect(divMotionNode.attribute("geometryPath"))

            sceneGraph.connectFromOutput("divAllCoordinates", [div_cns[i].attribute("translate")])
            sceneGraph.connectFromOutput("divRotate", [div_cns[i].attribute("rotate")])
            sceneGraph.connectFromOutput("divRotateOrder", [div_cns[i].attribute("rotateOrder")])
            sceneGraph.connectFromOutput("divUpAllCoordinates", [upv_cns[i].attribute("translate")])
            sceneGraph.connectFromOutput("divUpRotate", [upv_cns[i].attribute("rotate")])
            sceneGraph.connectFromOutput("divUpRotateOrder", [upv_cns[i].attribute("rotateOrder")])
            _, mainUtilities = api.buildConstraint(
                div_cns[i],
                drivers={"targets": (("", rootInputNode),)},
                constraintType="scale",
                maintainOffset=True
            )
            extras += mainUtilities

            u += step

        extras += [ration_node, mst_curveInfo, length_div, div_scl_node]

        for ctrl in rigLayer.iterControls():
            ctrlId = ctrl.id()
            if not ctrlId.startswith("fk"):
                continue
            ctrlParent = ctrl.srt().parent()
            if ctrlParent == rootTransform:
                _, constUtilities = zapi.buildConstraint(
                    ctrl.srt(),
                    drivers={"targets": ((ctrlId, rootInputNode),)},
                    constraintType="matrix",
                    maintainOffset=True,
                )
                extras += constUtilities

        for index, joint in enumerate(bindGuides):
            jointId = joint.id
            if not hasJoints:
                continue
            driven = joints.get(jointMapping[jointId])
            _, mainUtilities = api.buildConstraint(
                driven,
                drivers={"targets": (("", div_cns[index]),)},
                constraintType="matrix",
                maintainOffset=True,
                decompose=True,
            )

            extras += mainUtilities

        rigLayer.addExtraNodes(extras)


































