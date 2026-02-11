from cgrig.libs.maya import zapi
from cgrig.libs.hive import constants


def createBlendShapeLocator(rig, deformLayer, parent, worldMatrix, tagId, name):
    """ Creates a Locator attached to the deformLayer which is to be used for output blendshape
    data.

    :param rig: The hive rig instance which the locator will be add to the rig selectionset.
    :type rig: rig
    :param deformLayer:
    :type deformLayer: :class:`cgrig.libs.hive.base.hivenodes.HiveDeformLayer`
    :param parent: The parent node for the locator
    :type parent: :class:`zapi.DagNode`
    :param worldMatrix: The world matrix.
    :type worldMatrix: :class:`zapi.Matrix`
    :param tagId: The tag id which the locator will have.
    :type tagId: str
    :param name: The name for the locator
    :type name: str
    :return: The locator Dag node.
    :rtype: :class:`zapi.DagNode`
    """
    # create space locator which contains attributes for primary motion output
    valueOutput = zapi.createDag(name, "locator")
    valueOutput.setWorldMatrix(worldMatrix)
    valueOutput.setParent(parent)
    valueOutput.setShapeColour((1.000, 0.587, 0.073))
    deformLayer.addTaggedNode(valueOutput, tagId)
    selSet = rig.meta.selectionSet(constants.BS_SELECTION_SET_ATTR)
    if selSet is not None:
        selSet.addMember(valueOutput)
    return valueOutput

def createIfNotExistBlendShapeLocator(rig, deformLayer,checkLayerAttr, parent, worldMatrix, tagId, name):
    """ Creates the blendshape Locator if it doesn't already exist.

    :param checkLayerAttr:
    :type checkLayerAttr:
    :param rig: The hive rig instance which the locator will be add to the rig selectionset.
    :type rig: rig
    :param deformLayer:
    :type deformLayer: :class:`cgrig.libs.hive.base.hivenodes.HiveDeformLayer`
    :param parent: The parent node for the locator
    :type parent: :class:`zapi.DagNode`
    :param worldMatrix: The world matrix.
    :type worldMatrix: :class:`zapi.Matrix`
    :param tagId: The tag id which the locator will have.
    :type tagId: str
    :param name: The name for the locator
    :type name: str
    :return: The locator Dag node.
    :rtype: :class:`zapi.DagNode`
    """
    extraAttr = deformLayer.addAttribute(
        checkLayerAttr, Type=zapi.attrtypes.kMFnMessageAttribute, isFalse=True
    )

    bsNode = extraAttr.sourceNode() or deformLayer.taggedNode(tagId)
    if bsNode is None:
        bsNode = createBlendShapeLocator(rig, deformLayer, parent, worldMatrix, tagId, name)
    else:
        bsNode.setWorldMatrix(worldMatrix)
        bsNode.setParent(parent)
        bsNode.rename(name)
        selSet = rig.meta.selectionSet(constants.BS_SELECTION_SET_ATTR)
        if selSet is not None:
            selSet.addMember(bsNode)
    bsNode.message.connect(extraAttr)
    return bsNode

def addCurveLengthToDiff(curveShape, namingConfig, compName, compSide, sectionName, outAttr):
    """Creates a curveInfo node and connect the curveShape to it then connects the arcLength to the outAttr.

    :type curveShape: :class:`zapi.NurbsCurve`
    :type namingConfig: :class:`cgrig.libs.naming.naming.NameManager`
    :param compName: The naming Rule component name
    :type compName: str
    :param compSide: The naming Rule component side.
    :type compSide: str
    :param sectionName: The naming Rule section name.
    :type sectionName: str
    :param outAttr: The attribute to which the arc length will be connected to
    :type outAttr: :class:`zapi.Plug`
    :rtype: :class:`zapi.DGNode`
    """
    crvInfo = zapi.createDG(
        namingConfig.resolve("object", {"componentName": compName,
                                        "side": compSide,
                                        "section": sectionName,
                                        "type": "curveInfo"}),
        "curveInfo")
    curveShape.worldSpace[0].connect(crvInfo.inputCurve)
    crvInfo.arcLength.connect(outAttr)
    return crvInfo
