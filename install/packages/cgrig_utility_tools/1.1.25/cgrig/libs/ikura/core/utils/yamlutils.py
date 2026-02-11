#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 13:07
# @Author : yinyufei
# @File : yamlutils.py
# @Project : TeamCode

"""

该模块提供了YAML文件的加载和转储功能，支持有序字典和Python 2/3兼容性。

"""

import sys
import yaml
from collections import OrderedDict
# from yaml.representer import SafeRepresenter
from cgrig.libs.ikura.core.utils import ordered_dict

is_python_3 = (sys.version_info[0] == 3)

__all__ = ['YamlDumper', 'YamlLoader', 'ordered_dump', 'ordered_load']

# 尝试使用C扩展版本的Loader，提高性能
try:
    BaseLoader = yaml.CSafeLoader
except AttributeError:
    BaseLoader = yaml.SafeLoader

# 尝试使用C扩展版本的Dumper，提高性能
try:
    BaseDumper = yaml.CSafeDumper
except AttributeError:
    BaseDumper = yaml.SafeDumper


class YamlLoader(BaseLoader):
    """YAML加载器类

    继承自yaml的Loader类，用于加载YAML文件。
    """
    pass


class YamlDumper(BaseDumper):
    """YAML转储器类

    继承自yaml的Dumper类，用于将数据转储为YAML格式。
    """
    pass


# # safe unicode
# if not is_python_3:
#     yaml.add_representer(unicode, SafeRepresenter.represent_unicode, Dumper=YamlDumper)


# safe ordered dict
def _construct_ordered_mapping(loader, node):
    """构建有序映射

    用于在加载YAML时构建有序字典。

    参数:
        loader: YAML加载器
        node: YAML节点

    返回值:
        有序字典
    """
    loader.flatten_mapping(node)
    return ordered_dict(loader.construct_pairs(node))


if not is_python_3:
    YamlLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_ordered_mapping,
    )


def _dict_representer(dumper, data):
    """字典表示器

    用于在转储YAML时表示字典类型。

    参数:
        dumper: YAML转储器
        data: 要表示的字典数据

    返回值:
        YAML映射节点
    """
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        data.items()
    )


if not is_python_3:
    yaml.add_representer(dict, _dict_representer, Dumper=YamlDumper)
    yaml.add_representer(OrderedDict, _dict_representer, Dumper=YamlDumper)


# clean number list
def _number_sequence_representer(dumper, data):
    """数字序列表示器

    用于在转储YAML时表示数字列表，使其以流风格显示。

    参数:
        dumper: YAML转储器
        data: 要表示的列表数据

    返回值:
        YAML序列节点
    """
    if all(isinstance(i, (float, int)) for i in data):
        return dumper.represent_sequence(
            yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG,
            data,
            flow_style=True,
        )
    return dumper.represent_sequence(
        yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG,
        data,
    )


yaml.add_representer(list, _number_sequence_representer, Dumper=YamlDumper)


# custom loader/dumper
def ordered_load(stream, Loader=YamlLoader):
    """有序加载YAML

    加载YAML文件并保持字典的顺序。

    参数:
        stream: YAML文件流
        Loader: 使用的加载器类，默认为YamlLoader

    返回值:
        加载的数据结构
    """
    return yaml.load(stream, Loader=Loader)


def ordered_dump(data, stream=None, Dumper=YamlDumper, **kwds):
    """有序转储YAML

    将数据转储为YAML格式并保持字典的顺序。

    参数:
        data: 要转储的数据
        stream: 输出流，默认为None
        Dumper: 使用的转储器类，默认为YamlDumper
        **kwds: 其他关键字参数

    返回值:
        如果stream为None，返回YAML字符串；否则返回None
    """
    return yaml.dump(data, stream, Dumper=Dumper, **kwds)








