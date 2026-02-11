# -*- coding: utf-8 -*-
"""
@Author: Faith
@Date: 2026/2/1
@Time: 20:15
@Description:
            树形数据结构模块

            该模块实现了支持点分隔键路径的树形数据结构，主要用于Mikan绑定系统中的配置管理和数据组织。

            主要功能包括：
            - 支持点分隔的键路径（如 'a.b.c'）
            - 支持嵌套和扁平化数据结构的相互转换
            - 支持分支操作和子树访问
            - 支持通配符查询
            - 支持深度复制和浅复制
            - 提供SuperTree类用于处理更复杂的树形结构

            在绑定系统中的应用：
            - 管理模板配置和参数
            - 组织绑定控制器和关节的层级关系
            - 处理模块和变形器的配置数据
            - 支持复杂的命名空间和路径管理
@FilePath: tree.py
"""
import re
from fnmatch import fnmatch
from abc import abstractmethod
from copy import copy, deepcopy
from collections import defaultdict

try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections import Mapping, MutableMapping

__all__ = ['Tree', 'SuperTree']


class BaseTree(MutableMapping):
    """
    树形数据结构的抽象基类

    定义了树形数据结构的基本接口和通用方法，是Tree和Branch类的基类。
    实现了MutableMapping接口，支持字典式的操作。
    """

    def __init__(self, sep='.'):
        """
        初始化BaseTree

        Args:
            sep: 键路径的分隔符，默认为 '.'
        """
        self._key_sep = sep

    def rare_keys(self):
        """
        获取所有顶级键（稀有键）

        对于点分隔的键路径，只返回第一级的键，避免重复。
        例如，对于键 'a.b.c'，只返回 'a'。

        Yields:
            str: 顶级键名
        """
        branches = set()
        for key in self.keys():
            if self._key_sep not in key:
                yield key
                continue
            key = key.split(self._key_sep, 1)[0]
            if key not in branches:
                yield key
                branches.add(key)

    def rare_values(self):
        """
        获取所有顶级键对应的值

        Yields:
            顶级键对应的值
        """
        for key in self.rare_keys():
            yield self[key]

    def rare_items(self):
        """
        获取所有顶级键值对

        Yields:
            tuple: (顶级键名, 对应值)
        """
        for key in self.rare_keys():
            yield key, self[key]

    @property
    def sep(self):
        """
        获取键路径分隔符

        Returns:
            str: 键路径分隔符
        """
        return self._key_sep

    @abstractmethod
    def copy(self):
        """
        复制当前树形结构

        Returns:
            复制后的树形结构
        """
        pass

    def rare_copy(self):
        """
        创建当前树形结构的稀有副本（嵌套形式）

        Returns:
            dict: 嵌套形式的字典
        """
        return BaseTree.rarefy(self)

    @abstractmethod
    def branch(self, key):
        """
        获取指定键的分支

        Args:
            key: 分支键名

        Returns:
            Branch: 分支对象
        """
        pass

    @staticmethod
    def rarefy(tree):
        """
        将扁平化的树形结构转换为嵌套形式

        Examples:
            rarefy(Tree({'a.b.c' : 1}))
            {'a': {'b': {'c': 1}}}
            rarefy({'a.b.c' : 1})
            {'a': {'b': {'c': 1}}}

        Args:
            tree: 要转换的树形结构

        Returns:
            dict: 嵌套形式的字典
        """
        result = {}
        for key, value in tree.items():
            target = result
            if tree.sep in key:
                keyparts = key.split(tree.sep)
                key = keyparts.pop()
                for keypart in keyparts:
                    target = target.setdefault(keypart, {})
            if isinstance(value, Mapping):
                value = BaseTree.rarefy(value)
            target[key] = value

        return result

    @staticmethod
    def flatten(d, sep='.'):
        """
        将嵌套的字典转换为扁平化形式（点分隔键路径）

        Examples:
            nested = {'a': {'b': {'c': 1}}}
            Tree(nested)                        # without flatten
            Tree({'a': {'b': {'c': 1}}})
            Tree(flatten(nested))               # with flatten
            Tree({'a.b.c': 1})

        Args:
            d: 要转换的嵌套字典
            sep: 键路径分隔符，默认为 '.'

        Yields:
            tuple: (扁平化的键, 值)
        """
        for key, value in d.items():
            if isinstance(value, Mapping):
                for subkey, subvalue in BaseTree.flatten(value, sep=sep):
                    yield str(key) + sep + str(subkey), subvalue
            else:
                yield str(key), value

    def get(self, item, default=None):
        """
        获取指定键的值，如果键不存在则返回默认值

        Args:
            item: 要获取的键
            default: 默认值

        Returns:
            获取的值或默认值
        """
        try:
            return self[item]
        except KeyError:
            return default


_void = object()


class Tree(BaseTree):
    """
    树形数据结构的核心实现类

    继承自BaseTree，实现了完整的树形数据结构功能，支持点分隔的键路径、分支操作、通配符查询等。
    """

    def __init__(self, data=None, sep='.'):
        """
        初始化Tree对象

        Args:
            data: 初始数据，可以是字典或其他可迭代对象
            sep: 键路径分隔符，默认为 '.'
        """
        BaseTree.__init__(self, sep=sep)

        self._branches = defaultdict(set)
        self._items = {}
        if data:
            self.update(data)

    def __setitem__(self, key, value):
        """
        设置指定键的值

        Args:
            key: 键名，可以是点分隔的路径
            value: 要设置的值
        """
        if key in self._branches:
            del self[key]
        self._items[key] = value
        if self._key_sep in key:
            path = key.split(self._key_sep)
            for i in range(1, len(path)):
                lead = self._key_sep.join(path[:i])
                tail = self._key_sep.join(path[i:])
                if lead in self._items:
                    del self[lead]
                self._branches[lead].add(tail)

    def __getitem__(self, key):
        """
        获取指定键的值

        支持通配符查询和分支访问

        Args:
            key: 键名，可以是点分隔的路径或包含通配符

        Returns:
            键对应的值，或分支对象，或通配符查询结果

        Raises:
            KeyError: 如果键不存在
        """
        try:
            return self._items[key]
        except KeyError:
            if '*' in key:
                tree = Subtree()
                for _key in self._items:
                    if fnmatch(_key, key):
                        tree[_key] = self._items[_key]
                if not tree:
                    raise KeyError(key)
                elif len(tree) == 1:
                    return list(tree._items.values())[0]
                else:
                    return tree
            else:
                if key not in self._branches:
                    raise KeyError(key)
                return self.branch(key)

    def __delitem__(self, key):
        """
        删除指定键

        Args:
            key: 要删除的键名

        Raises:
            KeyError: 如果键不存在
        """
        try:
            del self._items[key]
            if self._key_sep in key:
                path = key.split(self._key_sep)
                for i in range(1, len(path)):
                    lead = self._key_sep.join(path[:i])
                    tail = self._key_sep.join(path[i:])
                    self._branches[lead].discard(tail)
                    if not self._branches[lead]:
                        del self._branches[lead]
        except KeyError:
            if key not in self._branches:
                raise
            self.branch(key).clear()

    def __iter__(self):
        """
        返回键的迭代器

        Returns:
            iterator: 键的迭代器
        """
        return iter(self._items)

    def __len__(self):
        """
        获取键的数量

        Returns:
            int: 键的数量
        """
        return len(self._items)

    def __repr__(self):
        """
        返回对象的字符串表示

        Returns:
            str: 对象的字符串表示
        """
        return '{0}({1!r})'.format(self.__class__.__name__, self._items)

    def __copy__(self):
        """ Returns a shallow copy of the tree.  The result has the same type. """
        return self.__class__(self)

    def __deepcopy__(self, memo):
        """ Returns a deep copy of the tree.  The result has the same type. """
        tree = self.__class__()
        tree._branches = deepcopy(self._branches)
        tree._items = deepcopy(self._items)
        return tree

    copy = __copy__

    def branch(self, key):
        """ Returns a :class:`Branch` object for specified ``key`` """
        return Branch(key, self)

    def branches(self):
        """
        获取所有分支

        Yields:
            Branch: 分支对象
        """
        for key in self._branches:
            yield self.branch(key)

    def pop(self, key, default=_void):
        """
        删除指定键并返回对应的值

        If key is not found, ``default`` is returned if given,
        otherwise KeyError is raised.

        If extracted value is a branch, it will be converted to :class:`Tree`.

        Args:
            key: 要删除的键名
            default: 默认值，如果键不存在

        Returns:
            键对应的值，或默认值

        Raises:
            KeyError: 如果键不存在且没有提供默认值
        """
        try:
            value = self[key]
        except KeyError:
            if default is _void:
                raise
            return default
        else:
            if isinstance(value, Branch):
                value = value.copy()
            del self[key]
            return value


class Subtree(Tree):
    pass


class Branch(BaseTree):
    """
    树分支代理类

    表示Tree的一个分支，提供对分支内容的访问和操作。
    """

    def __init__(self, key, parent):
        """
        初始化Branch对象

        Args:
            key: 分支键名
            parent: 父Tree对象
        """
        self._key_sep = parent._key_sep
        self._key = key
        self._parent = parent

    def _itemkey(self, key):
        """
        生成完整的项目键名

        Args:
            key: 相对键名

        Returns:
            str: 完整的键名
        """
        return self._key_sep.join((self._key, key))

    def keys(self):
        """
        获取分支中的键名集合

        Returns:
            set: 键名集合
        """
        if self._key not in self._parent._branches:
            return set()
        return self._parent._branches[self._key]

    def __getitem__(self, key):
        """
        获取分支中指定键的值

        Args:
            key: 键名

        Returns:
            键对应的值
        """
        return self._parent[self._itemkey(key)]

    def __setitem__(self, key, value):
        """
        设置分支中指定键的值

        Args:
            key: 键名
            value: 要设置的值
        """
        self._parent[self._itemkey(key)] = value

    def __delitem__(self, key):
        """
        删除分支中指定的键

        Args:
            key: 要删除的键名
        """
        del self._parent[self._itemkey(key)]

    def __iter__(self):
        """
        返回分支键的迭代器

        Returns:
            iterator: 键的迭代器
        """
        return iter(self.keys())

    def __len__(self):
        """
        获取分支中键的数量

        Returns:
            int: 键的数量
        """
        return len(self.keys())

    def __repr__(self):
        """
        返回对象的字符串表示

        Returns:
            str: 对象的字符串表示
        """
        return '{0}({1!r}): {2!r}'.format(
            self.__class__.__name__,
            self._key,
            dict(self),
        )

    @property
    def key(self):
        """
        获取分支键名

        Returns:
            str: 分支键名
        """
        return self._key

    def branch(self, key):
        """ Returns a :class:`Branch` object for specified ``key`` """
        return self._parent.branch(self._itemkey(key))

    def copy(self):
        """
        创建分支的浅副本

        Returns a shallow copy of the branch.  The result has the same type
        as the branch owner, i.e. :class:`Tree` or derrived from one.

        Returns:
            Tree: 分支的浅副本
        """
        return self._parent.__class__(self)

    def pop(self, key, default=_void):
        """
        删除分支中指定的键并返回对应的值

        Removes specified key and returns the corresponding value.
        If key is not found, ``default`` is returned if given,
        otherwise KeyError is raised.

        If extracted value is a branch, it will be converted to :class:`Tree`.

        Args:
            key: 要删除的键名
            default: 默认值，如果键不存在

        Returns:
            键对应的值，或默认值

        Raises:
            KeyError: 如果键不存在且没有提供默认值
        """
        return self._parent.pop(self._itemkey(key), default)


class SuperTree(object):
    """
    超级树形数据结构

    用于处理更复杂的树形结构，支持双分隔符的键路径（如 'main::sub.key'）。
    主要用于Mikan绑定系统中的命名空间管理和复杂数据组织。
    """

    def __init__(self, key_sep='::'):
        """
        初始化SuperTree对象

        Args:
            key_sep: 主分隔符，默认为 '::'
        """
        self.tree = Tree()
        self.dict = dict()

        self._key_sep = key_sep

    def __setitem__(self, key, value):
        """
        设置指定键的值

        Args:
            key: 键名，可以包含主分隔符 '::'
            value: 要设置的值
        """
        mainkey, sep, subkey = key.partition(self._key_sep)

        if mainkey not in self.tree:
            self.tree[mainkey] = Tree()
        if subkey:
            self.tree[mainkey][subkey] = value
        else:
            self.dict[mainkey] = value

    def __getitem__(self, key):
        """
        获取指定键的值

        Args:
            key: 键名，可以包含主分隔符 '::'

        Returns:
            键对应的值

        Raises:
            KeyError: 如果键不存在
        """
        mainkey, sep, subkey = key.partition(self._key_sep)

        if subkey:
            subtree = self.tree[mainkey]
            if type(subtree) is Tree:
                v = subtree[subkey]
                if type(v) in (Branch, Subtree):
                    return v.rare_copy()
                else:
                    return v
            elif type(subtree) in [Branch, Subtree]:
                newtree = Tree()
                for k, i in subtree.items():
                    try:
                        newtree[k] = i[subkey]
                    except:
                        pass

                if not newtree._items:
                    return None
                elif len(newtree._items) != 1:
                    return newtree.rare_copy()
                else:
                    v = list(newtree._items.values())[0]
                    if type(v) in [Branch, Subtree]:
                        return v.rare_copy()
                    else:
                        return v
        else:
            return self.dict[mainkey]

    def __delitem__(self, key):
        """
        删除指定键

        Args:
            key: 要删除的键名

        Raises:
            KeyError: 如果键不存在
        """
        mainkey, sep, subkey = key.partition(self._key_sep)

        if subkey:
            subtree = self.tree[mainkey]
            if isinstance(subtree, Tree):
                del subtree[subkey]
            elif isinstance(subtree, Branch):
                subtrees = subtree.rare_copy()
                for k in subtrees:
                    try:
                        del subtrees[k][subkey]
                    except:
                        pass
        else:
            del self.dict[mainkey]

    def __iter__(self):
        """
        返回主键的迭代器

        Returns:
            iterator: 主键的迭代器
        """
        return iter(self.tree._items)

    def __len__(self):
        """
        获取主键的数量

        Returns:
            int: 主键的数量
        """
        return len(self.tree._items)

    def __repr__(self):
        """
        返回对象的字符串表示

        Returns:
            str: 对象的字符串表示
        """
        return '{0}({1!r})'.format(self.__class__.__name__, self.tree)

    def __copy__(self):
        """
        创建对象的浅副本

        Returns:
            SuperTree: 浅副本
        """
        tree = SuperTree(key_sep=self._key_sep)
        tree.tree = copy(self.tree)
        tree.dict = copy(self.dict)
        return tree

    def __deepcopy__(self, memo):
        """
        创建对象的深副本

        Args:
            memo: 深拷贝备忘录

        Returns:
            SuperTree: 深副本
        """
        tree = SuperTree(key_sep=self._key_sep)
        tree.tree = deepcopy(self.tree)
        tree.dict = deepcopy(self.dict)
        return tree

    copy = __copy__

    def clear(self):
        """
        清空所有数据
        """
        self.tree.clear()
        self.dict.clear()

    def get(self, item, default=None, as_list=False):
        """
        获取指定键的值，如果键不存在则返回默认值

        Args:
            item: 要获取的键
            default: 默认值
            as_list: 是否以列表形式返回

        Returns:
            获取的值或默认值
        """
        try:
            if not as_list:
                return self[item]
            else:
                if isinstance(self[item], dict):
                    return SuperTree.flatten(self[item])
                return [self[item]]

        except KeyError:
            return default

    def keys(self):
        """
        获取所有完整键名

        Returns:
            list: 完整键名列表
        """
        keys = []
        for key in self:
            for subkey in self.tree[key]:
                keys.append(key + self._key_sep + subkey)
        return keys

    @staticmethod
    def flatten(obj, objects=None):
        """
        将嵌套对象展平为列表

        Args:
            obj: 要展平的对象
            objects: 结果列表

        Returns:
            list: 展平后的列表
        """
        if objects is None:
            objects = []

        try:
            iter(obj)
        except TypeError:
            objects.append(obj)
            return objects

        for k in sorted(obj, key=_int_key):
            v = obj[k]
            if isinstance(v, dict):
                SuperTree.flatten(v, objects)
            else:
                objects.append(v)
        return objects

    # todo: rare keys for supertree
    # def rare_keys(self):
    #     return []


_find_index = re.compile(r'\d+')


def _int_key(key):
    i = _find_index.findall(key)
    if i:
        return 0, int(i[-1])
    else:
        return 1, key


