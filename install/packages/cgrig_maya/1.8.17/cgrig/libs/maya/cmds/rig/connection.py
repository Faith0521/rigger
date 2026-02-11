#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/11/14 11:01
# @Author : yinyufei
# @File : connection.py
# @Project : TeamCode
import maya.api.OpenMaya as om2
import maya.cmds as cmds
from cgrig.libs.maya.cmds.objutils import attributes


def getPlugInput(plug):
    """
    Returns the input of a plug

    :param str plug: Plug to get the input of
    :return: The input connection of the plug
    :rtype: str
    """
    plugList = list()
    for sourcePlug in (
        cmds.listConnections(plug, source=True, destination=False, plugs=True) or []
    ):
        plugList.append(str(sourcePlug))
    return plugList


def getPlugOutput(plug):
    """
    Returns the output of a plug

    :param str plug: Plug to get the output of
    :return: The output connection of the plug
    :rtype: str
    """
    plugList = list()
    for sourcePlug in (
        cmds.listConnections(plug, source=False, destination=True, plugs=True) or []
    ):
        plugList.append(str(sourcePlug))
    return plugList


def connectPlugs(source, destination):
    """
    Connect input plug to output plug using maya API

    :param str source: plug on the source end of the connection
    :param str destination: plug on the destination end of the connection
    """
    sourcePlug = attributes._getPlug(source)
    destPlug = attributes._getPlug(destination)

    mdgModifier = om2.MDGModifier()
    mdgModifier.connect(sourcePlug, destPlug)
    mdgModifier.doIt()


def connectTransforms(source, destination, translate=True, rotate=True, scale=True):
    """
    Connect the transform plugs between two nodes.

    :param str source: node on the source end of the connection
    :param str destination: node on the destination end of the connection
    :param bool translate:
    :param bool rotate:
    :param bool scale:
    """
    attrs = list()
    if translate:
        attrs += ["tx", "ty", "tz"]
    if rotate:
        attrs += ["rx", "ry", "rz"]
    if scale:
        attrs += ["sx", "sy", "sz"]

    for attr in attrs:
        connectPlugs("{}{}".format(source, attr), "{}{}".format(destination, attr))

