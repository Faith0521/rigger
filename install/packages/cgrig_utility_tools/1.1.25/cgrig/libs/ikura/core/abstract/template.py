#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 12:47
# @Author : yinyufei
# @File : template.py
# @Project : TeamCode
import os.path
import pkgutil
import cgrig.libs.ikura.templates.template
from copy import deepcopy
from six import string_types
from cgrig.core.util import zlogging
from cgrig.libs.ikura.core.utils import ordered_load, ordered_dict


log = zlogging.cgrigLogger

common_data = ''' 
 opts: 
   branches: 
     help: | 
       绑定模块复制的分支列表
       - 示例: [L, R] 会构建模块两次，左右镜像
     value: '' 
     yaml: on 
     presets: 
      - 'L, R' 
      - 'up, dn' 
      - 'ft, bk' 
     legacy: forks 
   sym: 
     help: 动画菜单中翻转和镜像功能的对称轴
     value: 0 
     enum: 
       0: parent 
       1: x 
       2: y 
       3: z 
   group: 
     help: | 
       模块层次结构中父组的名称
       如果组不存在，将创建并父化到"all"下
     value: '' 
   parent: 
     help: | 
       确定模块组如何集成到资产的组层次结构中
       - parent: 将模块组父化到模板父组下
       - merge up: 将模块的控制器合并到模板父组中
       - merge down: 将模块的控制器合并到模板子组中
     value: 0 
     enum: 
       0: parent 
       1: merge up 
       2: merge down 
   do_ctrl: 
     help: 标记控制器以使其可动画
     value: on 
   do_skin: 
     help: 标记绑定关节以使其可用于蒙皮
     value: on 
   virtual_parent: 
     help: | 
       为虚拟层次结构构建设置新的模板父级
       如果模板层次结构不合适，这允许绑定骨架更连贯地连接
       同时相应地连接控制器的选择漫游
     value: '' 
   isolate_skin: 
     help: 将蒙皮关节分离到绑定中的专用组
     value: off 
 '''

branch_pairs = '''
x:
 - [L, R]
 - [l, r]
 - [ex, in]
 - [ext, int]
y:
 - [up, dn]
z:
 - [ft, bk]
'''


class TemplateMeta(type):
    """
    模板元类

    用于在创建类时自动为类添加funcs字典属性，用于存储和管理该类的功能方法。
    每个使用此元类创建的类都会获得自己独立的funcs字典。
    """

    def __new__(mcs, name, bases, attrs):
        """
        创建新类时的回调方法

        Args:
            mcs (type): 元类本身
            name (str): 要创建的类的名称
            bases (tuple): 要创建的类的父类元组
            attrs (dict): 要创建的类的属性字典

        Returns:
            type: 创建的新类对象

        实现细节：
        1. 调用父类的__new__方法创建类对象
        2. 为新创建的类添加一个空的funcs字典属性
        3. 返回新创建的类对象
        """
        # 调用父类的__new__方法创建类对象
        new_class = super(TemplateMeta, mcs).__new__(mcs, name, bases, attrs)

        # 为每个类创建自己的funcs字典，用于存储该类的功能方法
        new_class.funcs = dict()  # each class gets its own funcs dict

        return new_class


class Template(object):
    """
    模板基类

    使用TemplateMeta元类创建的基类，所有子类将自动继承funcs字典属性，
    可用于注册和管理功能方法，实现可扩展的模板机制。
    """
    __metaclass__ = TemplateMeta
    modules = {}
    classes = {}
    software = None

    type_name = "template"

    common_data = ordered_load(common_data)
    branch_pairs = ordered_load(branch_pairs)

    template = None
    template_data = ordered_dict()

    @classmethod
    def get_all_modules(cls, module=cgrig.libs.ikura.templates.template):
        """
        获取所有模块名称列表
        """
        print("aaaaaaaaaaaaaaaaaaaaa")
        cls.modules.clear()
        cls.classes.clear()

        def safe_import(modname, importer):
            if sys.version_info[0] >= 3:
                import importlib
                return importlib.import_module(modname)
            else:
                import pkgutil
                return importer.find_module(modname).load_module(modname)

        # get all template modules
        for importer, modname, ispkg in pkgutil.iter_modules(module.__path__):
            if not ispkg:
                continue


    # def __new__(cls, node):
    #     # return instance of the corresponding class of template
    #     module_name = cls.get_module_from_node(node)
    #     new_cls = cls.get_class(module_name)
    #
    #     return super(Template, new_cls).__new__(new_cls)

    def __init__(self, node):
        # init template instance from the given node
        self.node = node

        self.branches = ['']  # branchless default
        self.root = self.node

        self.modes = set()



Template.get_all_modules()



