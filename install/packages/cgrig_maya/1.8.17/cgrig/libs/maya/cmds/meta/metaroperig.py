#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/16 13:39
# @Author : yinyufei
# @File : metaroperig.py
# @Project : TeamCode
import os

import math

from maya import cmds

import maya.api.OpenMaya as om2
from cgrig.libs.maya.mayacommand.library.additivefk import additivefkbuild
from cgrigvendor import six

from cgrig.libs.maya.mayacommand import mayaexecutor as executor
from cgrig.libs.maya import zapi
from cgrig.libs.maya.api import deformers
from cgrig.libs.maya.cmds.objutils import namehandling, joints, connections
from cgrig.libs.maya.cmds.rig import splinebuilder, controls, splines
from cgrig.libs.maya import triggers
from cgrig.libs.maya.meta import base
from cgrig.libs.maya.cmds.rig import splinerigswitcher
from cgrig.libs.utils import filesystem
from cgrig.libs.maya.cmds.meta import metaadditivefk


class MetaRopeRig(base.MetaBase):

    id = "MetaRopeRig"

    _default_attrs = [
        # {"name": "startJoint", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "endJoint", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        #
        # {"name": "splineIkList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "splineSolver", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "clusterList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "fkControlList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "fkGroupList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "revfkControlList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "revfkGroupList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "floatControlList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "floatGroupList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "spineControlList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "spineRotControl", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "spineOtherConstraintList", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "cogControl", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "cogGroup", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "scaleGroup", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "scaleMultiplyNode", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "scaleGroupConstraint", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "rigGrp", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "multStretchNodes", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "maintainScaleNodes", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},
        # {"name": "curveInfo", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "ikHandleBuild", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "jointsSpline", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "additiveFkMeta", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute},
        # {"name": "meshes", "value": "", "Type": zapi.attrtypes.kMFnMessageAttribute, "isArray": True},

        # Attributes
        {"name": "rigName", "value": "", "Type": zapi.attrtypes.kMFnDataString},
        {"name": "controlCount", "value": 5, "Type": zapi.attrtypes.kMFnNumericInt},
        {"name": "controlSpacing", "value": 1, "Type": zapi.attrtypes.kMFnNumericInt},
        {"name": "rigType", "value": 0, "Type": zapi.attrtypes.kMFnNumericInt},
        {"name": "size", "value": 1.0, "Type": zapi.attrtypes.kMFnNumericFloat},
        {"name": "addUp", "value": True, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "controlSpacingUp", "value": 1, "Type": zapi.attrtypes.kMFnNumericInt},
        {"name": "stretch", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "reverseUp", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "rigUpType", "value": 0, "Type": zapi.attrtypes.kMFnNumericInt},
        {"name": "sinCos", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "rotateAll", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "rotateGradient", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},
        {"name": "slide", "value": False, "Type": zapi.attrtypes.kMFnNumericBoolean},

    ]

    def __init__(self, node=None, name=None, initDefaults=True, lock=False,
                 jointList=None, controlCount=5, size=1.0, rigType=0,
                 addUp=False, controlSpacingUp=False, stretch=False, reverseUp=False,
                 controlSpacing=1, mod=None, **attrs):

        if not node:
            name = name or attrs.get('rigName', "")
            name = self.generateUniqueName(name)
            metaAttrs = dict(locals())  # Get all the parameters
            metaAttrs.pop('self')
            metaName = name + "_meta"

        super(MetaRopeRig, self).__init__(node=node, name=name, initDefaults=initDefaults, lock=lock, mod=mod)

        self.setMetaAttributes(**metaAttrs)


    def generateUniqueName(self, name=""):
        """ Generates a unique rig name, if its already unique it will return name

        :return:
        :rtype: str
        """
        metaNames = self.metaNodeRigNames()
        while name in metaNames:
            name = namehandling.incrementName(name)

        return name

    @classmethod
    def metaNodeRigNames(cls):
        """ Gets the rig names in the scene based on available metanodes

        :return:
        :rtype:
        """
        rigNames = []
        for n in base.findMetaNodesByClassType(MetaRopeRig.__name__):
            rigNames.append(n.rigName.value())
        return rigNames


    def setMetaAttributes(self, mod=None, **metaAttrs):
        """ Sets the setup's attributes usually from the UI. Will not update rig automatically
        """
        # self.buildFk.set(metaAttrs['buildFk'], mod)  # type: zapi.Plug
        # self.buildRevFk.set(metaAttrs['buildRevFk'], mod)
        # self.buildFloat.set(metaAttrs['buildFloat'], mod)  # type: zapi.Plug
        # self.buildSpine.set(metaAttrs['buildSpine'], mod)  # type: zapi.Plug
        # self.orientRoot.set(metaAttrs['orientRoot'], mod)  # type: zapi.Plug
        # self.scale.set(metaAttrs['scale'], mod)  # type: zapi.Plug
        # self.controlCount.set(metaAttrs['controlCount'], mod)  # type: zapi.Plug
        # self.hierarchySwitch.set(metaAttrs['hierarchySwitch'], mod)  # type: zapi.Plug
        # self.controlSpacing.set(metaAttrs['controlSpacing'], mod)  # type: zapi.Plug
        #
        # if metaAttrs.get('buildAdditiveFk'):
        #     self.buildAdditiveFk.set(True, mod)
        #
        # if metaAttrs['jointsSpline'] and metaAttrs['jointsSpline'].exists():
        #     metaAttrs['jointsSpline'].message.connect(self.jointsSpline, mod)
        #
        # if metaAttrs['ikHandleBuild'] and metaAttrs['ikHandleBuild'].exists():
        #     metaAttrs['ikHandleBuild'].message.connect(self.ikHandleBuild, mod)


    def build(self, buildType=0, mod=None):
        pass



















