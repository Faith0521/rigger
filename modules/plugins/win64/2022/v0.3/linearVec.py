#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/12/22 17:46
# @Author : yinyufei
# @File : linearVec.py
# @Project : TeamCode
import maya.api.OpenMaya as om


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class linearVecNode(om.MPxNode):

    TYPE_NAME = "linearVecNode"
    TYPE_ID = om.MTypeId(0x0515)

    vecA = None
    vecAx = None
    vecAy = None
    vecAz = None
    vecB = None
    vecBx = None
    vecBy = None
    vecBz = None
    blend = None
    outVec = None


    def __init__(self):
        super(linearVecNode, self).__init__()

    def compute(self, plug, data):
        if plug == linearVecNode.outVec:
            product_data_handle = data.outputValue(linearVecNode.outVec)
            in_blend = data.inputValue(linearVecNode.blend).asDouble()

            h_A = data.inputValue(linearVecNode.vecA)
            v_A = h_A.asFloatVector()
            vecAx = v_A.x
            vecAy = v_A.y
            vecAz = v_A.z

            h_B = data.inputValue(linearVecNode.vecB)
            v_B = h_B.asFloatVector()
            vecBx = v_B.x
            vecBy = v_B.y
            vecBz = v_B.z

            vecCx = (vecBx * in_blend) + ((1.0 - in_blend) * vecAx)
            vecCy = (vecBy * in_blend) + ((1.0 - in_blend) * vecAy)
            vecCz = (vecBz * in_blend) + ((1.0 - in_blend) * vecAz)

            product_data_handle.set3Float(vecCx, vecCy, vecCz)

            data.setClean(plug)

    @classmethod
    def creator(cls):
        return linearVecNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.vecA = numeric_attr.createPoint("vectorA", "vectorA")
        cls.vecAx = numeric_attr.child(0)
        cls.vecAy = numeric_attr.child(1)
        cls.vecAz = numeric_attr.child(2)
        numeric_attr.channelBox = True
        numeric_attr.writable = True
        numeric_attr.storable = False
        cls.addAttribute(cls.vecA)

        cls.vecB = numeric_attr.createPoint("vectorB", "vectorB")
        cls.vecBx = numeric_attr.child(0)
        cls.vecBy = numeric_attr.child(1)
        cls.vecBz = numeric_attr.child(2)
        numeric_attr.channelBox = True
        numeric_attr.writable = True
        numeric_attr.storable = False
        cls.addAttribute(cls.vecB)

        cls.blend = numeric_attr.create("blend", "blend", om.MFnNumericData.kDouble, 0.5)
        numeric_attr.writable = True
        numeric_attr.keyable = True
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.addAttribute(cls.blend)

        cls.outVec = numeric_attr.createPoint("outVec", "outVec")
        numeric_attr.storable = False
        numeric_attr.writable = False
        numeric_attr.readable = True
        cls.addAttribute(cls.outVec)

        cls.attributeAffects(cls.vecA, cls.outVec)
        cls.attributeAffects(cls.vecAx, cls.outVec)
        cls.attributeAffects(cls.vecAy, cls.outVec)
        cls.attributeAffects(cls.vecAz, cls.outVec)
        cls.attributeAffects(cls.vecB, cls.outVec)
        cls.attributeAffects(cls.vecBx, cls.outVec)
        cls.attributeAffects(cls.vecBy, cls.outVec)
        cls.attributeAffects(cls.vecBz, cls.outVec)
        cls.attributeAffects(cls.blend, cls.outVec)


def initializePlugin(plugin):
    """
    Entry point for a plugin.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "yyf"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(linearVecNode.TYPE_NAME,
							   linearVecNode.TYPE_ID,
                               linearVecNode.creator,
                               linearVecNode.initialize,
                               om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(linearVecNode.TYPE_NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """

    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(linearVecNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(linearVecNode.TYPE_NAME))
