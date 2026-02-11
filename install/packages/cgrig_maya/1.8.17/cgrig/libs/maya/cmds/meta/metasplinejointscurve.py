# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om2

from cgrig.libs.maya import zapi
from cgrig.libs.maya.meta import base

META_TYPE = "CgRigJointsCurve"


class CgRigSplineJointsCurve(base.MetaBase):
    """Class that controls the meta network node setup for the joint on curve functionality

    Found in cgrig.libs.maya.cmds.rig.splines
    """
    _default_attrs = [{"name": "joints", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
                      {"name": "curve", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
                      {"name": "jointCount", "value": 24, "Type": zapi.attrtypes.kMFnNumericInt},
                      {"name": "jointName", "value": "joint", "Type": zapi.attrtypes.kMFnDataString},
                      {"name": "secondaryAxisOrient", "value": 0, "Type": zapi.attrtypes.kMFnNumericInt},
                      {"name": "numberPadding", "value": 2, "Type": zapi.attrtypes.kMFnNumericInt},
                      {"name": "suffix", "value": True, "Type": zapi.attrtypes.kMFnNumericBoolean},
                      {"name": "reverse", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean}
                      ]

    def metaAttributes(self):
        """Creates the dictionary as attributes if they don't already exist"""
        defaults = super(CgRigSplineJointsCurve, self).metaAttributes()
        defaults.extend(CgRigSplineJointsCurve._default_attrs)
        return defaults

    def connectAttributes(self, jointNodeList, curveNode):
        """Connects the maya nodes to the meta node

        :param jointNodeList: list of zapi joint nodes
        :type jointNodeList: list(:class:`zapi.DGNode`)
        :param curveNode: curve as a zapi node
        :type curveNode: :class:`zapi.DGNode`
        """
        for jointNode in jointNodeList:
            jointNode.message.connect(self.joints.nextAvailableDestElementPlug())
        curveNode.message.connect(self.curve)

    def setMetaAttributes(self, jointCount, jointName, secondaryAxisOrient, numberPadding, suffix, reverse):
        """Sets the setup's attributes usually from the UI"""
        self.jointCount = jointCount
        self.jointName = jointName
        self.secondaryAxisOrient = secondaryAxisOrient
        self.numberPadding = numberPadding
        self.suffix = suffix
        self.reverse = reverse

    def getMetaAttributes(self):
        return {"jointName": self.jointName.asString(),
                "jointCount": self.jointCount.asInt(),
                "secondaryAxisOrient": self.secondaryAxisOrient.asInt(),
                "numberPadding": self.numberPadding.asInt(),
                "suffix": self.suffix.asBool(),
                "reverse": self.reverse.asBool()}

    def setMetaJointName(self, jointName):
        self.jointName = jointName

    def getMetaJointName(self):
        return self.jointName.asString()

    def getJoints(self):
        """Returns the joints as zapi dag node list

        :return: list of zapi joint nodes
        :rtype: list(:class:`zapi.DGNode`)
        """
        jointList = list()
        for i in self.joints:
            sourcePlug = i.source()
            if sourcePlug is None:
                continue
            jointList.append(sourcePlug.node())
        return jointList

    def getJointsStr(self):
        """Returns the joints as string names

        :return: list of joint long names
        :rtype: list(str)
        """
        return zapi.fullNames(self.getJoints())

    def getCurve(self):
        """Returns the curve as a zapi dag node

        :return: zapi curve nodes
        :rtype: :class:`zapi.DGNode`
        """
        return self.curve.source().node()

    def getCurveStr(self):
        """Returns the curve as a long name

        :return: curve node names
        :rtype: str
        """
        return self.getCurve().fullPathName()

    def deleteJoints(self):
        """Deletes all the joints associated with the meta node"""
        jointList = self.getJoints()
        for joint in jointList:
            joint.delete()


def deleteSplineJoints(nodes, message=False):
    """Deletes all joints and the meta node setup related to the selection

    :param nodes: any zapi nodes, will be joints or curves related to joint setup
    :type nodes:  list(:class:`zapi.DGNode`)
    :param message: report the message to the user
    :type message: bool

    :return success: True if joints were deleted
    :rtype success: bool
    """
    metaNodes = base.findRelatedMetaNodesByClassType(nodes, CgRigSplineJointsCurve.__name__)
    if not metaNodes:
        if message:
            relatedObjs = list(zapi.fullNames(nodes))
            om2.MGlobal.displayWarning("No `{}` meta nodes found related to objects "
                                       "{}".format(CgRigSplineJointsCurve.__name__, relatedObjs))
        return False
    for metaNode in metaNodes:  # Delete the joints
        metaNode.deleteJoints()
        metaNode.delete()
    if message:
        om2.MGlobal.displayInfo("Success joints deleted")
    return True
