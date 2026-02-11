# -*- coding: utf-8 -*-
# @Author: 46314
# @Date:   2022-09-18 17:13:36
# @Last Modified by:   46314
# @Last Modified time: 2022-09-18 17:13:43
from maya import OpenMaya

from pymel.core import *
from maya import cmds


def addAttributes(node,
                  longName,
                  type,
                  value=None,
                  niceName=None,
                  shortName=None,
                  min=None,
                  max=None,
                  multi=False,
                  keyable=True,
                  readable=True,
                  storable=True,
                  writable=True,
                  channelBox=False,
                  lock=False):
    """

    :param node:
    :param longName:
    :param type:
    :param value:
    :param niceName:
    :param shortName:
    :param min:
    :param max:
    :param keyable:
    :param readable:
    :param storable:
    :param writable:
    :param channelBox:
    :param lock:
    :return:
    """
    if cmds.attributeQuery(longName, node=node, ex=True):
        return

    flag_data = {}

    if shortName is not None:
        flag_data["shortName"] = shortName
    if niceName is not None:
        flag_data["niceName"] = niceName
    if type == "string":
        flag_data["dataType"] = type
    else:
        flag_data["attributeType"] = type

    if min is not None and min is not False:
        flag_data["minValue"] = min
    if max is not None and max is not False:
        flag_data["maxValue"] = max

    flag_data["keyable"] = keyable
    flag_data["readable"] = readable
    flag_data["storable"] = storable
    flag_data["writable"] = writable
    flag_data["multi"] = multi

    if value is not None and type not in ["string"]:
        flag_data["defaultValue"] = value

    cmds.addAttr(node, ln=longName, **flag_data)

    if value is not None:
        if type in ["string"]:
            cmds.setAttr("%s.%s" % (node, longName), value, type=type)
        else:
            cmds.setAttr("%s.%s" % (node, longName), value)

    if channelBox:
        cmds.setAttr("%s.%s" % (node, longName), channelBox=True)

    cmds.setAttr("%s.%s" % (node, longName), lock=lock)

    return node + "." + longName


def addEnumAttribute(node,
                     longName,
                     value,
                     enum,
                     niceName=None,
                     shortName=None,
                     keyable=True,
                     readable=True,
                     storable=True,
                     writable=True,
                     lock=False):
    """

    :param node:
    :param longName:
    :param value:
    :param enum:
    :param niceName:
    :param shortName:
    :param keyable:
    :param readable:
    :param storable:
    :param writable:
    :param lock:
    :return:
    """
    if cmds.attributeQuery(longName, node=node, ex=True):
        return

    data = {}

    if shortName is not None:
        data["shortName"] = shortName
    if niceName is not None:
        data["niceName"] = niceName

    data["attributeType"] = "enum"
    data["en"] = ":".join(enum)

    data["keyable"] = keyable
    data["readable"] = readable
    data["storable"] = storable
    data["writable"] = writable

    cmds.addAttr(node, ln=longName, **data)
    cmds.setAttr("%s.%s" % (node, longName), value)
    cmds.setAttr("%s.%s" % (node, longName), lock=lock)

    return node + "." + longName


def lock_and_hide(node, channelArray=None, hide=True):
    """
    Locks and hides the channels specified in the channelArray.
    Args:
        node : (String) target object
        channelArray: (List) the channels as string values. eg: ["sx", "sy", "sz"] or ["translateX", "rotateX", "sz"]
        hide: (Bool) if false, the attributes will be only locked but not hidden. Defaulf True
    Returns: None

    """
    channelArray = (
        ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        if not channelArray
        else channelArray
    )
    for i in channelArray:
        attribute = "{0}.{1}".format(node, i)
        cmds.setAttr(attribute, lock=True, keyable=not hide, channelBox=not hide)


class ImmutableDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("%r object does not support item assignment" % type(self).__name__)

    def __delitem__(self, key):
        raise TypeError("%r object does not support item deletion" % type(self).__name__)

    def __getattribute__(self, attribute):
        if attribute in ('clear', 'update', 'pop', 'popitem', 'setdefault'):
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, attribute))
        return dict.__getattribute__(self, attribute)

    def __hash__(self):
        return hash(tuple(sorted(self.iteritems())))

    def fromkeys(self, sequence, v):
        return type(self)(dict(self).fromkeys(sequence, v))


class attrDef(object):
    def __init__(self, name):
        self.attr_name = name
        self.value = None
        self.valueType = None
        self.attr_dict = {}

    def add(self, node):
        """

        :param node:
        :return:
        """
        attr_name = addAttributes(node,
                                  self.attr_name,
                                  self.valueType,
                                  self.value,
                                  self.niceName,
                                  self.shortName,
                                  self.minimum,
                                  self.maximum,
                                  self.keyable,
                                  self.readable,
                                  self.storable,
                                  self.writable)

        return node, attr_name

    def get_as_dict(self):
        self.attr_dict["attr_name"] = self.attr_name
        self.attr_dict["valueType"] = self.valueType
        self.attr_dict["value"] = self.value
        self.attr_dict["niceName"] = self.niceName
        self.attr_dict["shortName"] = self.shortName
        self.attr_dict["minimum"] = self.minimum
        self.attr_dict["maximum"] = self.maximum
        self.attr_dict["keyable"] = self.keyable
        self.attr_dict["readable"] = self.readable
        self.attr_dict["storable"] = self.storable
        self.attr_dict["writable"] = self.writable

        return self.attr_dict

    def set_from_dict(self, attr_dict):
        self.attr_name = attr_dict["attr_name"]
        self.valueType = attr_dict["valueType"]
        self.value = attr_dict["value"]
        self.niceName = attr_dict["niceName"]
        self.shortName = attr_dict["shortName"]
        self.minimum = attr_dict["minimum"]
        self.maximum = attr_dict["maximum"]
        self.keyable = attr_dict["keyable"]
        self.readable = attr_dict["readable"]
        self.storable = attr_dict["storable"]
        self.writable = attr_dict["writable"]


class attrDef_create(attrDef):

    def __init__(self,
                 name,
                 type,
                 value,
                 niceName=None,
                 shortName=None,
                 minimum=None,
                 maximum=None,
                 keyable=True,
                 readable=True,
                 storable=True,
                 writable=True
                 ):
        self.attr_name = name
        self.niceName = niceName
        self.shortName = shortName
        self.valueType = type
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.keyable = keyable
        self.readable = readable
        self.storable = storable
        self.writable = writable
        self.attr_dict = {}


class EnumAttrDef_create(attrDef):

    def __init__(self, attr_name, enum, value=False):
        self.attr_name = attr_name
        self.value = value
        self.enum = enum
        self.valueType = None
        self.attr_dict = {}

    def add(self, node):
        attr_name = addEnumAttribute(
            node, self.attr_name, enum=self.enum, value=self.value
        )
        return node, attr_name

    def get_as_dict(self):
        self.attr_dict["attr_name"] = self.attr_name
        self.attr_dict["value"] = self.value
        self.attr_dict["enum"] = self.enum
        self.attr_dict["valueType"] = self.valueType

        return self.attr_dict

    def set_from_dict(self, attr_dict):
        self.attr_name = attr_dict["scriptName"]
        self.value = attr_dict["value"]
        self.enum = attr_dict["enum"]
        self.valueType = attr_dict["valueType"]


class CurveAttrDef_create(attrDef):

    def __init__(self,
                 attr_name,
                 keys=None,
                 interpolation=0,
                 extrapolation=0
                 ):
        self.attr_name = attr_name
        self.keys = keys
        self.interpolation = interpolation
        self.extrapolation = extrapolation
        self.value = None
        self.valueType = None
        self.attr_dict = {}

    def add(self, node):
        attr_name = addAttributes(node, self.attr_name, "double", 0)

        attrDummy_name = addAttributes(
            node, self.attr_name + "_dummy", "double", 0)

        for key in self.keys:
            setDrivenKeyframe(
                attr_name, cd=attrDummy_name, dv=key[0], v=key[1], itt='clamped', ott='clamped')

        # clean dummy attr
        deleteAttr(attrDummy_name)

        return node, attr_name

    def get_as_dict(self):
        self.attr_dict["attr_name"] = self.attr_name
        self.attr_dict["keys"] = self.keys
        self.attr_dict["interpolation"] = self.interpolation
        self.attr_dict["extrapolation"] = self.extrapolation
        self.attr_dict["value"] = self.value
        self.attr_dict["valueType"] = self.valueType

        return self.attr_dict

    def set_from_dict(self, attr_dict):
        self.attr_name = attr_dict["attr_name"]
        self.keys = attr_dict["keys"]
        self.interpolation = attr_dict["interpolation"]
        self.extrapolation = attr_dict["extrapolation"]
        self.value = attr_dict["value"]
        self.valueType = attr_dict["valueType"]


def unlock(node, attr_list=None):
    """Unlocks the list of provided attributes on defined node"""

    attr_list = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"] if not attr_list else attr_list
    if type(attr_list) != list:
        attr_list = [attr_list]
    for attr in attr_list:
        cmds.setAttr("{0}.{1}".format(node, attr), e=True, k=True, l=False)


def get_max_index(node, attribute):
    """
    获取节点多元素属性的最大索引值
    :param node: 节点名称
    :param attribute: 属性名称（不带索引，例如 "roots"）
    :return: 最大索引值（int），如果属性不存在返回 -1
    """
    if not cmds.objExists(node):
        raise ValueError(f"节点 {node} 不存在")

    full_attr = f"{node}.{attribute}"
    if not cmds.attributeQuery(attribute, node=node, exists=True):
        raise ValueError(f"属性 {full_attr} 不存在")

    # 获取所有索引
    indices = cmds.getAttr(full_attr, multiIndices=True)

    if indices:
        return max(indices)  # 返回最大索引值
    else:
        return -1  # 如果属性没有元素，返回 -1
