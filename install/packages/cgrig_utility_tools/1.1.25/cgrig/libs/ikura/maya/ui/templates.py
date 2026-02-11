#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 17:09
# @Author : yinyufei
# @File : templates.py
# @Project : TeamCode

from Qt import QtWidgets, QtCore, QtGui
from Qt.QtCore import Qt, QSize
from Qt.QtWidgets import (
    QMainWindow, QTreeWidget, QTreeWidgetItem, QLabel, QSplitter, QPushButton,
    QLineEdit, QToolButton, QWidget, QSizePolicy, QComboBox, QMenu, QCheckBox,
    QItemDelegate, QShortcut, QAbstractItemView, QTextEdit, QApplication,
    QPlainTextEdit, QSpinBox, QGridLayout, QVBoxLayout,
)
from maya import cmds as mc
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.ikura.core.ui.widgets import *
from cgrig.core.util.zlogging import *
from .widgets import OptVarSettings
from cgrig.libs.ikura.maya.core import Template


class TemplateManager(QMainWindow, OptVarSettings):
    def __init__(self, parent=None):
        super(TemplateManager, self).__init__(parent)

        self.setWindowFlag(Qt.Widget)
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # 初始化各个面板组件
        self.tree = TemplateTreeWidget()  # 模板树控件
        self.tab_add = TemplateAddWidget()  # 添加模板标签页
        self.tab_edit = TemplateEditWidget() # 添加编辑标签页
        self.tab_log = TemplateLogWidget() # 添加日志标签页
        self.tab_add._tree = self.tree
        self.tab_edit._tree = self.tree
        self.tab_edit._manager = self
        self.tab_log.log_box.widget._manager = self

        # 设置各个面板的引用
        self.tab_add._tree = self.tree  # 为添加面板设置树引用

        self.tabs = TabScrollWidget()
        self.tabs.addTab(self.tab_add, '添加')
        self.tabs.addTab(self.tab_edit, '编辑')
        self.tabs.addTab(self.tab_log, '日志')

        # layout
        # 创建垂直分割器并添加控件
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.tree)  # 添加模板树
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(2, 1)  # 设置拉伸
        splitter.setSizes([256, 256])  # 设置初始大小
        self.setCentralWidget(splitter)


class TemplateTreeDelegate(QItemDelegate):
    role_highlighted = get_palette_role('HighlightedText')
    role_foreground = get_palette_role('Text')

    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):

        # foreground color highlight
        palette = option.palette

        w = option.styleObject
        item = w.itemFromIndex(index)
        if item.isSelected():
            color = item.foreground(index.column()).color()
            if color == Qt.black:
                color = palette.color(self.role_foreground)
            palette.setColor(self.role_highlighted, color.lighter())

        option.palette = palette
        QItemDelegate.paint(self, painter, option, index)


class TemplateTreeWidget(QTreeWidget):
    INDENT_SIZE = 12

    FONT_SIZE = 11
    TREE_STYLE = 'QTreeView {selection-background-color: transparent; font-size: ' + str(FONT_SIZE) + ';}'


    def __init__(self, parent=None):
        super(TemplateTreeWidget, self).__init__(parent)
        self.setHeaderLabels(['id', '方向', '类型', '模式'])
        self.setIndentation(self.INDENT_SIZE)
        header = self.header()
        header.setStretchLastSection(True)

        header.resizeSection(0, 256)
        header.resizeSection(1, 80)
        header.resizeSection(2, 96)
        header.resizeSection(3, 32)

        self._callbacks = {}
        self.tree_items = {}

        self.setExpandsOnDoubleClick(False)
        # self.doubleClicked.connect(self.select)

        self.setStyleSheet(TemplateTreeWidget.TREE_STYLE)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setFocusPolicy(Qt.NoFocus)
        self.setItemDelegate(TemplateTreeDelegate())

        self.setContextMenuPolicy(Qt.CustomContextMenu)



        # drag'n drop
        self.setAcceptDrops(True)
        self.current_tab = 0
        self._middle_pressed_pos = None
        self._dragged_item = None



class TemplateOpts(StackWidget):
    """
    模板选项基类，用于管理模板的选项和名称

    该类是一个基类，提供了构建选项面板和名称面板的基本功能，
    子类可以通过重写get_current_template_modules方法来提供模板模块。
    """

    def __init__(self, parent=None):
        """
        初始化模板选项对象

        Args:
            parent: 父窗口部件，默认为None
        """
        StackWidget.__init__(self, parent)
        self.last_add_item = None
        self.last_opts_item = []

        self.wd_adds = {}  # 添加选项控件
        self.wd_opts = {}  # 公共选项控件
        self.wd_custom_opts = {}  # 自定义选项控件
        self.wd_names = {}  # 名称控件

        self.item = None  # 当前选中的单个项目
        self.items = []  # 当前选中的项目列表


class TemplateAddWidget(TemplateOpts, OptVarSettings):
    ICON_ADD = elements.iconlib.icon('cross')

    def __init__(self, parent=None):
        TemplateOpts.__init__(self, parent)

        # build template data
        self.template_types = {}
        # 遍历所有已注册的模板模块
        # Template.modules

        # 构建UI界面 - 添加模块区域
        # 创建"添加模块"按钮
        self.wd_add = elements.IconMenuButton(iconName="plus", parent=self)

        # 创建"Add Module"标签
        lbl_add = elements.Label(text="添加模块")

        # 创建模块名称输入框
        self.wd_name = elements.LineEdit()
        # 构建UI界面 - 添加资产区域
        # 创建"添加资产"按钮
        self.wd_add_asset = elements.IconMenuButton(iconName="plus", parent=self)
        # 创建"Add Asset"标签
        lbl_add_asset = elements.Label(text="添加资产")
        # 创建资产名称输入框
        self.txt_add_asset = elements.LineEdit()


        _col = self.add_columns(stretch=[2, 2])  # 创建两列，比例为2:2
        # 第一列布局：添加模块
        _row = self.add_row(_col[0])
        _row.addWidget(self.wd_add)
        _row.addWidget(lbl_add)
        _row.addWidget(self.wd_name)

        # 第二列布局：添加资产
        _row = self.add_row(_col[1])
        _row.addWidget(self.wd_add_asset)
        _row.addWidget(lbl_add_asset)
        _row.addWidget(self.txt_add_asset)

        # 获取资产布局的父容器
        self.layout_asset = _row.parent()
        # 如果已经存在资产，则隐藏添加资产的布局

        # 构建UI界面 - 模板类型选择
        self.wd_type = StringListPlugWidget(label='类型')  # 模板类型选择框
        self.wd_subtype = StringListPlugWidget()  # 模板子类型选择框

        # 构建UI界面 - 数量输入
        self.wd_number = IntPlugWidget(label='数量', min_value=1, default=1)  # 数量输入框，最小值为1
        self.wd_number.widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        # 网格布局 - 类型和数量选择
        _grid = self.add_grid()
        _grid.addWidget(self.wd_type, 0, 0)  # 类型选择框 - 第0行第0列
        _grid.addWidget(self.wd_subtype, 1, 0)  # 子类型选择框 - 第1行第0列
        _grid.addWidget(self.wd_number, 0, 1)  # 数量输入框 - 第0行第1列

        # 可折叠面板 - 用于组织创建和选项区域

        self.box_add = self.add_collapse('创建')  # "创建"折叠面板
        self.box_opts = self.add_collapse('设置')  # "选项"折叠面板
        self.box_opts.collapse.set_collapsed(True)  # 默认折叠"选项"面板

        # 添加伸缩控件，使布局更美观
        self.layout.addStretch(1)

        # 初始化UI组件
        # self.build_wd_type()  # 构建类型选择下拉框

    def build_wd_type(self, *args):
        types = sorted(self.template_types)
        priority = ['core', 'default', 'world']
        ordered = [t for t in priority if t in types]
        types = [t for t in types if t not in priority]
        types = ordered + types

        self.wd_type.set_list(types)
        self.wd_type.set_value(0)
        self.build_wd_subtype()

    def build_wd_subtype(self, *args):
        types = self.template_types[self.wd_type.value][:]
        types.sort()
        if 'default' in types:
            types.remove('default')
            types = ['default'] + types

        self.wd_subtype.set_list(types)

        subtype = self.get_optvar('opt_subtype_{}'.format(self.wd_type.value), types[0])
        if subtype in types:
            self.wd_subtype.set_value(subtype)
        else:
            self.wd_subtype.set_value(0)

        self.build_wd_name()
        self.build_box_add()
        self.build_box_opt()

    def build_wd_name(self, *args):
        module = self.get_current_template_modules()[0]
        name = module.template_data['name']
        self.wd_name.setText(name)


class TemplateEditWidget(TemplateOpts):
    def __init__(self, parent=None):
        TemplateOpts.__init__(self, parent)

        # 构建字段UI区域 - 用于显示和编辑模板的基本属性
        # 创建一个列布局容器，用于放置所有字段相关的UI组件
        self.box_fields = self.add_column(margins=0, spacing=0)

        # 创建模板类型标签
        self.wd_type = QLabel()

        # 创建模板重命名输入框
        self.wd_rename = QLineEdit()

        # 创建模式选择下拉框
        self.wd_mode = StringPlugWidget(label='模式', default='')
        self.wd_mode.layout.setStretch(0, 1)  # 设置布局伸缩比例
        self.wd_mode.color_changed = 'color: #ddd;'  # 设置修改时的颜色
        self.wd_mode.color_altered = 'color: #ddd;'  # 设置变更时的颜色

        # 创建启用/禁用复选框
        # self.wd_enable = elements.CheckBox(label='禁用', checked=False)
        self.wd_enable = BoolPlugWidget(label='禁用', default=0)
        self.wd_enable.color_changed = 'color: #ddd;'  # 设置修改时的颜色
        self.wd_enable.color_altered = 'color: #ddd;'  # 设置变更时的颜色

        # 创建重命名网格布局
        self.box_rename = self.add_grid(self.box_fields)
        self.box_rename.setSpacing(5)  # 设置控件间距
        # 添加类型标签，右对齐，占4份宽度
        self.box_rename.addWidget(self.wd_type, 0, 0, stretch=4, align=Qt.AlignRight)
        # 添加重命名输入框，占4份宽度
        self.box_rename.addWidget(self.wd_rename, 0, 1, stretch=4)
        # 添加模式选择框，占5份宽度
        self.box_rename.addWidget(self.wd_mode, 0, 2, stretch=5)
        # 添加启用/禁用复选框，占1份宽度
        self.box_rename.addWidget(self.wd_enable, 0, 3, stretch=1)

        # 添加"Options"折叠面板
        self.box_opts = self.add_collapse('设置', self.box_fields)
        # 添加"Names"折叠面板
        self.box_names = self.add_collapse('名称', self.box_fields)

        # 添加伸缩控件，使布局更美观
        self.box_fields.addStretch(1)


class TemplateLogWidget(StackWidget):

    def __init__(self, parent=None):
        """
        初始化模板日志搜索和过滤组件

        Args:
            parent (QtWidgets.QWidget, optional): 父窗口部件. Defaults to None.
        """
        # 调用父类StackWidget的构造函数，初始化基础UI组件
        StackWidget.__init__(self, parent)

        # 创建主列布局
        _col = self.add_column(margins=0, spacing=1)

        # 创建搜索和过滤控制行布局
        _row = self.add_row(_col, margins=0, spacing=2)

        # 创建"Pattern"标签
        _lbl = elements.Label(text='Pattern ')
        _row.addWidget(_lbl, stretch=1, alignment=Qt.AlignRight)

        # 创建搜索模式输入框
        self.pattern_edit = elements.LineEdit()
        _row.addWidget(self.pattern_edit, stretch=3)
        self.pattern_edit.setMaximumHeight(24)  # 设置最大高度
        # 连接回车信号到搜索模式方法
        # self.pattern_edit.returnPressed.connect(self.search_pattern)

        # 创建"Search"按钮
        _btn = elements.styledButton(text='搜索')
        _row.addWidget(_btn, stretch=1)
        # 连接点击信号到搜索模式方法
        # _btn.clicked.connect(self.search_pattern)

        # 创建"Filter"按钮
        _btn = elements.styledButton(text='过滤')
        _row.addWidget(_btn, stretch=1)
        # 连接点击信号到过滤块方法
        # _btn.clicked.connect(self.filter_blocks)

        # 创建"Reset"按钮
        _btn = elements.styledButton(text='重置')
        _row.addWidget(_btn, stretch=1)
        # 连接点击信号到重置块方法
        # _btn.clicked.connect(self.reset_blocks)

        # 创建"Clear"按钮
        _btn = elements.styledButton(text='清除')
        _row.addWidget(_btn, stretch=1)
        # 连接点击信号到清除文本方法
        # _btn.clicked.connect(self.clear_text)

        # 创建并添加模板日志记录器
        self.log_box = TemplateLogger(self)
        _col.addWidget(self.log_box.widget, stretch=1)

        # 配置日志记录器
        _log = create_logger()
        # 移除现有的TemplateLogger处理器
        _log.handlers = [handler for handler in _log.handlers if not isinstance(handler, TemplateLogger)]
        # 添加新的TemplateLogger处理器
        _log.addHandler(self.log_box)

        # 初始化备份变量
        self.backup = None


class TemplateLogger(SafeHandler):

    def __init__(self, parent):
        super(SafeHandler, self).__init__()

        formatter = get_formatter(name=False)
        self.setFormatter(formatter)

        self.widget = TemplateLoggerTextEdit(parent)

        self.syntax = SyntaxHighlighter(self.widget.document())
        self.syntax.add_styles([
            ('debug', (152, 152, 152)),
            ('info', (70, 155, 200), {'bold': True}),
            ('success', (160, 180, 50), {'bold': True}),
            ('warning', '#ECD790'),
            ('error', '#E69F85'),
            ('critical', '#F54859'),

            ('debug+', (152, 152, 152), {'bold': True}),
            ('info+', (70, 155, 200), {'bold': True}),
            ('success+', (160, 180, 50), {'bold': True}),
            ('warning+', '#F3C93E', {'bold': True}),
            ('error+', '#EB5C28', {'bold': True}),
            ('critical+', (230, 40, 60), {'bold': True}),
        ])
        self.syntax.add_rules([
            (r'^(DEBUG).+', 0, 'debug'),
            # (r'^(INFO).+', 0, 'info'),
            # (r'^(SUCCESS).+', 0, 'success'),
            (r'^(WARNING|Warning).+', 0, 'warning'),
            (r'^(ERROR|Error).+', 0, 'error'),
            (r'^(CRITICAL).+', 0, 'critical'),

            # (r'^(DEBUG)\b', 0, 'debug'),
            (r'^(INFO)\b', 0, 'info'),
            (r'^(SUCCESS)\b', 0, 'success'),
            (r'^(WARNING|Warning)\b', 0, 'warning+'),
            (r'^(ERROR|Error)\b', 0, 'error+'),
            (r'^(CRITICAL)\b', 0, 'critical+'),
        ])

        self._alive = True
        self.widget.destroyed.connect(self._on_destroyed)

    def emit(self, record):
        if self._alive:
            msg = self.format(record)
            msg = msg.replace('<', '&lt;')
            msg = "<p style=\"white-space: pre-wrap;\">" + msg + "</p>"
            self.widget.appendHtml(msg)

    def _on_destroyed(self):
        self._alive = False


class TemplateLoggerTextEdit(QPlainTextEdit):
    FONT_LOGGER = QtGui.QFont('Courier New', 8)
    FONT_LOGGER.setFixedPitch(True)
    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)

        self.setReadOnly(True)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFont(TemplateLoggerTextEdit.FONT_LOGGER)

        self.re_node = QtCore.QRegExp(r'[:|_a-zA-z0-9]+')

    # def mouseReleaseEvent(self, event):
    #     key_mod = QApplication.keyboardModifiers()
    #
    #     if key_mod == Qt.CTRL and event.button() == Qt.LeftButton:
    #         focus_widget = QApplication.focusWidget()
    #
    #         cursor = self.textCursor()
    #
    #         line = cursor.block().text()
    #         b = cursor.positionInBlock()
    #
    #         # regex mikan ids
    #         find = ''
    #         index = self.re_node.indexIn(line, 0)
    #         while index >= 0:
    #             index = self.re_node.pos(0)
    #             length = len(self.re_node.cap(0))
    #             if index <= b < index + length:
    #                 find = line[index:index + length]
    #             index = self.re_node.indexIn(line, index + length)
    #
    #         if find and mc.objExists(find):
    #             mc.select(mc.ls(find))
    #             tree_widget = self._manager.tree
    #             items = [x for x in tree_widget.tree_items if isinstance(x, Helper) and (x.has_mod() or x.has_deformer())]
    #
    #             for item in items:
    #                 if str(item.node) == find:
    #                     for _item in tree_widget.selectedItems():
    #                         _item.setSelected(False)
    #                     tree_widget.setCurrentItem(tree_widget.tree_items[item])
    #                     self._manager.update_tabs()
    #                     self._manager.select_tab_edit()
    #                     focus_widget.setFocus()
    #                     break
    #
    #     QPlainTextEdit.mouseReleaseEvent(self, event)






