# -*- coding: utf-8 -*-
"""
@Author: Faith
@Date: 2026/2/8
@Time: 11:01
@Description:
@FilePath: protocol.py
"""
from typing import List, Type
from maya import cmds
from abc import abstractmethod, abstractmethod


node_types = []  # type: List[Type[NodeProtocol]]


def register_node_type(cls):
    node_types.append(cls)
    return cls


def find_node_type(type_name):
    for node_type in node_types:
        if node_type.type_name == type_name:
            return node_type
    raise LookupError('can not find node type: {}'.format(type_name))


class NodeProtocol(object):
    """
    Node的增删改查协议
    """
    type_name = 'unimplemented'  # type: str
    icon_name = None  # type: str|None

    def __init__(self, node):
        """
        Initialize NodeProtocol on give node
        """
        self._node = node

    def __repr__(self):
        """
        Returns class string representation
        """
        return '<{}>: {}'.format(self.type_name, self)

    def __str__(self):
        """
        Returns class as string
        """
        return str(self._node)

    def __eq__(self, other):
        """
        Overrides equals operator to allow for different RBFNode instances to be matched against each other
        """
        return str(self) == str(other)

    @abstractmethod
    def create(cls):
        # type: () -> NodeProtocol
        """创建Pose"""
        raise NotImplementedError

    @abstractmethod
    def drive_attribute(self):
        # type: () -> str
        """
        返回驱动属性的名称字符串，用于驱动Shape的属性。
        驱动属性的值范围为0-1
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        # type: () -> None
        """删除"""
        raise NotImplementedError

    @abstractmethod
    def name(self):
        # type: () -> str
        """获取Node的名称"""
        raise NotImplementedError

    @abstractmethod
    def info(self):
        # type: () -> str
        """获取展示到PoseInfoWidget的字符串"""
        raise NotImplementedError

    @classmethod
    def load(cls, data):
        # type: (str) -> NodeProtocol
        """反序列化Pose信息"""
        raise NotImplementedError

    @abstractmethod
    def mirror(self):
        # type: () -> NodeProtocol
        """镜像"""
        raise NotImplementedError

    @classmethod
    def find_all(cls):
        # type: () -> List[NodeProtocol]
        """查找所有NodeProtocol"""
        raise NotImplementedError

    @classmethod
    def data(cls):
        # type: () -> dict
        """获取NodeProtocol的序列化数据"""
        raise NotImplementedError

    @classmethod
    def drivers(cls):
        # type: () -> List[str]
        """获取所有驱动的节点"""
        raise NotImplementedError

    @classmethod
    def drivens(cls):
        # type: () -> List[str]
        """获取所有被驱动的节点"""
        raise NotImplementedError

    @classmethod
    def controllers(cls):
        # type: () -> List[str]
        """获取所有控制器节点"""
        raise NotImplementedError




























