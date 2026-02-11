#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 13:13
# @Author : yinyufei
# @File : typeutils.py
# @Project : TeamCode

"""

该模块提供了各种类型处理和字符串操作的工具函数。

"""

import re
import sys
import unicodedata
from functools import reduce
from itertools import takewhile
from contextlib import contextmanager
from collections import OrderedDict
from six import string_types

from cgrigvendor.unidecode import unidecode


__all__ = [
    'is_python_3',
    're_add', 're_slash', 're_pipe', 're_is_int', 're_is_float', 're_get_keys',
    'ordered_dict', 'get_slice', 'longest_common_prefix', 'longest_common_suffix', 'cleanup_str', 'filter_str',
    'flatten_list', 'flatten_dict', 'unique', 'nullcontext',
    'SingletonMetaClass', 'singleton'
]

is_python_3 = (sys.version_info[0] == 3)

# 正则表达式模式
re_add = re.compile(r'[^+]+')  # 匹配非加号字符
re_slash = re.compile(r'[^/]+')  # 匹配非斜杠字符
re_pipe = re.compile(r'[^|]+')  # 匹配非管道字符
re_is_int = re.compile(r'^-?\d+$')  # 匹配整数
re_is_float = re.compile(r'^[-+]?[0-9]*\.?[0-9]+$')  # 匹配浮点数
re_get_keys = re.compile(r'\[([A-Za-z0-9_:-]+)\]')  # 匹配方括号中的键

# 有序字典，根据Python版本选择实现
ordered_dict = dict
if not is_python_3:
    ordered_dict = OrderedDict


def get_slice(item):
    """获取切片对象

    根据字符串创建切片对象。

    参数:
        item: 切片字符串，格式如 "start:end:step"

    返回值:
        切片对象
    """
    return slice(*[{True: lambda n: None, False: int}[x == ''](x) for x in (item.split(':') + ['', '', ''])[:3]])


def longest_common_prefix(xs):
    """最长公共前缀

    查找字符串列表中所有字符串共享的最长前缀。

    参数:
        xs: 字符串列表

    返回值:
        最长公共前缀字符串
    """
    if not xs:
        return ''
    if len(xs) == 1:
        return xs[0]
    xs.sort()
    shortest = xs[0]
    prefix = ''
    for i in range(len(shortest)):
        if xs[len(xs) - 1][i] == shortest[i]:
            prefix += xs[len(xs) - 1][i]
        else:
            break
    return prefix


def longest_common_suffix(xs):
    """最长公共后缀

    查找字符串列表中所有字符串共享的最长后缀。

    参数:
        xs: 字符串列表

    返回值:
        最长公共后缀字符串
    """

    def all_same(cs):
        """检查所有字符是否相同"""
        h = cs[0]
        return all(h == c for c in cs[1:])

    def first_char_prepended(s, cs):
        """将第一个字符添加到字符串前面"""
        return cs[0] + s

    return reduce(
        first_char_prepended,
        takewhile(
            all_same,
            zip(*(reversed(x) for x in xs))
        ),
        ''
    )


def cleanup_str(text, sub='_'):
    """清理字符串

    清理字符串，去除特殊字符，转换为ASCII格式。

    参数:
        text: 要清理的字符串
        sub: 替换特殊字符的字符，默认为下划线

    返回值:
        清理后的字符串
    """
    try:
        text = str(text)
        text = text.decode('latin-1')
    except:
        pass

    nfkd_form = unicodedata.normalize('NFKD', text)
    ascii_string = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    clean_string = re.sub(r'\W+', sub, ascii_string)

    return clean_string


def filter_str(text, r='_'):
    """过滤字符串

    过滤字符串，去除特殊字符，使用unidecode处理Unicode字符。

    参数:
        text: 要过滤的字符串
        r: 替换特殊字符的字符，默认为下划线

    返回值:
        过滤后的字符串
    """
    text = unidecode(text)
    if r is not None:
        text = re.sub(r'\W+', r, text)
    return text


def flatten_list(l):
    """展平列表

    递归展平嵌套列表。

    参数:
        l: 要展平的列表

    返回值:
        展平后的元素生成器
    """
    for el in l:
        if type(el) in (tuple, list) and not isinstance(el, string_types):
            for sub in flatten_list(el):
                yield sub
        else:
            yield el


def flatten_dict(obj, objects=None):
    """展平字典

    递归展平嵌套字典，收集所有值。

    参数:
        obj: 要展平的字典
        objects: 收集值的列表，默认为None

    返回值:
        包含所有值的列表
    """
    if objects is None:
        objects = []

    for k in sorted(obj):
        v = obj[k]
        if isinstance(v, dict):
            flatten_dict(v, objects)
        else:
            objects.append(v)
    return objects


def unique(elements):
    """去重

    去除列表中的重复元素，保持原始顺序。

    参数:
        elements: 要去重的元素列表

    返回值:
        去重后的列表
    """
    return list(ordered_dict.fromkeys(elements))


def _unique3(elements):
    """Python 3 专用去重

    使用Python 3的dict.fromkeys方法去重。

    参数:
        elements: 要去重的元素列表

    返回值:
        去重后的列表
    """
    return list(dict.fromkeys(elements))


if is_python_3:
    unique = _unique3


@contextmanager
def nullcontext(enter_result=None):
    """空上下文管理器

    一个不做任何事情的上下文管理器，用于需要上下文管理器但不需要特殊处理的情况。

    参数:
        enter_result: 上下文管理器进入时返回的结果
    """
    yield enter_result


# ----- singleton

class SingletonMetaClass(type):
    """单例元类

    用于创建单例类的元类。
    """

    def __init__(cls, name, bases, dict):
        """初始化类

        参数:
            cls: 类对象
            name: 类名
            bases: 基类元组
            dict: 类字典
        """
        super(SingletonMetaClass, cls).__init__(name, bases, dict)
        original_new = cls.__new__

        def my_new(cls, *args, **kwds):
            """自定义__new__方法

            确保类只有一个实例。

            参数:
                cls: 类对象
                *args: 位置参数
                **kwds: 关键字参数

            返回值:
                类的唯一实例
            """
            if cls.instance == None:
                cls.instance = original_new(cls, *args, **kwds)
            return cls.instance

        cls.instance = None
        cls.__new__ = staticmethod(my_new)


def singleton(cls):
    """单例装饰器

    用于将类转换为单例。

    参数:
        cls: 要转换为单例的类

    返回值:
        单例工厂函数
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """获取实例

        确保类只有一个实例。

        参数:
            *args: 位置参数
            **kwargs: 关键字参数

        返回值:
            类的唯一实例
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
