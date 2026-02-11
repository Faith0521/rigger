# -*- coding: utf-8 -*-
"""
@Author: Faith
@Date: 2026/1/30
@Time: 21:41
@Description:
@FilePath: template.py
"""
from cgrig.libs.ikura.core import abstract
from cgrig.libs.ikura.maya import cmdx as mx


class Template(abstract.Template):
    """Main class for all components of different types of templates.

       Attributes:
           node (str, mx.Node): root node of the template hierarchy

       """
    software = 'maya'


    def __init__(self, node):
        # init template instance from the given node
        if not isinstance(node, mx.Node):
            node = mx.encode(str(node))
        self.node = node

        self.branches = ['']  # no branch by default
        self.root = self.node

        self.modes = set()

        if not self.node.is_referenced():
            try:
                self.node['useOutlinerColor'] = 1
                self.node['outlinerColor'] = (0.33, 0.73, 1)
            except:
                pass


    def build_template(self, data):
        pass

    def build_rig(self):
        pass
