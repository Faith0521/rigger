#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/2/11 17:14
# @Author : yinyufei
# @File : metapose.py
# @Project : TeamCode
import maya.api.OpenMaya as om2

from cgrig.libs.maya import zapi
from cgrig.libs.maya.meta import base

META_TYPE = "CgRigPoseEdit"


class CgRigPoseEdit(base.MetaBase):

    _default_attrs = [
                      {
                          "name": "poseType",
                          "value": "",
                          "Type": zapi.attrtypes.kMFnDataString,
                          "isArray": True,
                          "children":(
                              {
                              "name": "nodeName",
                              "Type": zapi.attrtypes.kMFnDataString,
                              "isArray": False,
                              },
                              {
                                  "name": "rotate",
                                  "Type": zapi.attrtypes.kMFnNumericDouble,
                                  "isArray": True,
                              },
                              {
                                  "name": "rotateVector",
                                  "Type": zapi.attrtypes.kMFnNumericDouble,
                                  "isArray": True,
                              },
                              {
                                  "name": "pose",
                                  "Type": zapi.attrtypes.kMFnNumericDouble,
                                  "isArray": False,
                              },
                              {
                                  "name": "createdNodes",
                                  "Type": zapi.attrtypes.kMFnMessageAttribute,
                                  "isArray": True,
                              }
                          )
                          # "children":(
                          #     {
                          #         "name": "driverJoints",
                          #         "isArray": True,
                          #         "children": (
                          #             {
                          #                 "name": "nodeName",
                          #                 "value": "",
                          #                 "Type": zapi.attrtypes.kMFnDataString,
                          #                 "isArray": False,
                          #             },
                          #             {
                          #                 "name": "rotate",
                          #                 "Type": zapi.attrtypes.kMFnNumericDouble,
                          #                 "isArray": True,
                          #             },
                          #             {
                          #                 "name": "rotateVector",
                          #                 "Type": zapi.attrtypes.kMFnNumericDouble,
                          #                 "isArray": True,
                          #             },
                          #             {
                          #                 "name": "pose",
                          #                 "Type": zapi.attrtypes.kMFnNumericDouble,
                          #                 "isArray": False,
                          #             },
                          #             {
                          #                 "name": "createdNodes",
                          #                 "Type": zapi.attrtypes.kMFnMessageAttribute,
                          #                 "isArray": True,
                          #             }
                          #         ),
                          #     }
                          # )
                      },
                      ]

    def metaAttributes(self):
        """Creates the dictionary as attributes if they don't already exist"""
        defaults = super(CgRigPoseEdit, self).metaAttributes()
        defaults.extend(CgRigPoseEdit._default_attrs)
        return defaults

    # def connectAttributes(self, jointNodeList, curveNode):
    #     """Connects the maya nodes to the meta node
    #
    #     :param jointNodeList: list of zapi joint nodes
    #     :type jointNodeList: list(:class:`zapi.DGNode`)
    #     :param curveNode: curve as a zapi node
    #     :type curveNode: :class:`zapi.DGNode`
    #     """
    #     for jointNode in jointNodeList:
    #         jointNode.message.connect(self.joints.nextAvailableDestElementPlug())
    #     curveNode.message.connect(self.curve)
    #
    # def setMetaAttributes(self, jointCount, jointName, spacingWeight, spacingStart,
    #                       spacingEnd, secondaryAxisOrient, fractionMode, numberPadding, suffix, reverse):
    #     """Sets the setup's attributes usually from the UI"""
    #     self.jointCount = jointCount
    #     self.jointName = jointName
    #     self.spacingWeight = spacingWeight
    #     self.spacingStart = spacingStart
    #     self.spacingEnd = spacingEnd
    #     self.secondaryAxisOrient = secondaryAxisOrient
    #     self.fractionMode = fractionMode
    #     self.numberPadding = numberPadding
    #     self.suffix = suffix
    #     self.reverse = reverse
    #
    # def getMetaAttributes(self):
    #     return {"jointName": self.jointName.asString(),
    #             "jointCount": self.jointCount.asInt(),
    #             "spacingWeight": self.spacingWeight.asFloat(),
    #             "spacingStart": self.spacingStart.asFloat(),
    #             "spacingEnd": self.spacingEnd.asFloat(),
    #             "secondaryAxisOrient": self.secondaryAxisOrient.asString(),
    #             "fractionMode": self.fractionMode.asBool(),
    #             "numberPadding": self.numberPadding.asInt(),
    #             "suffix": self.suffix.asBool(),
    #             "reverse": self.reverse.asBool()}
    #
    # def setMetaJointName(self, jointName):
    #     self.jointName = jointName
    #
    # def getMetaJointName(self):
    #     return self.jointName.asString()
    #
    # def getJoints(self):
    #     """Returns the joints as zapi dag node list
    #
    #     :return: list of zapi joint nodes
    #     :rtype: list(:class:`zapi.DGNode`)
    #     """
    #     jointList = list()
    #     for i in self.joints:
    #         sourcePlug = i.source()
    #         if sourcePlug is None:
    #             continue
    #         jointList.append(sourcePlug.node())
    #     return jointList
    #
    # def getJointsStr(self):
    #     """Returns the joints as string names
    #
    #     :return: list of joint long names
    #     :rtype: list(str)
    #     """
    #     return zapi.fullNames(self.getJoints())
    #
    # def getCurve(self):
    #     """Returns the curve as a zapi dag node
    #
    #     :return: zapi curve nodes
    #     :rtype: :class:`zapi.DGNode`
    #     """
    #     return self.curve.source().node()
    #
    # def getCurveStr(self):
    #     """Returns the curve as a long name
    #
    #     :return: curve node names
    #     :rtype: str
    #     """
    #     return self.getCurve().fullPathName()
    #
    # def deleteJoints(self):
    #     """Deletes all the joints associated with the meta node"""
    #     jointList = self.getJoints()
    #     for joint in jointList:
    #         joint.delete()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #




















