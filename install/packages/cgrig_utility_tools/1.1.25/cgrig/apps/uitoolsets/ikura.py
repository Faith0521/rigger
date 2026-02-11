#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/30 12:28
# @Author : yinyufei
# @File : ikura.py
# @Project : TeamCode


from Qt import QtWidgets, QtCore
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.ikura.maya.ui.widgets import OptVarSettings
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.core.util import zlogging
from cgrig.libs.ikura.maya.core import Template
from cgrig.libs.ikura.core.utils import *
from cgrig.libs.ikura.core.ui.widgets import *
from cgrig.libs.ikura.maya.ui.templates import TemplateManager

log = zlogging.cgrigLogger


class IkuraMain(QtWidgets.QMainWindow, OptVarSettings):
    def __init__(self, parent=None):
        super(IkuraMain, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.tabs = TabScrollWidget()
        self.setCentralWidget(self.tabs)

        # 实例化各个功能标签页
        self.tab_templates = TemplateManager()  # 模板管理标签页

        # 将标签页添加到容器中
        self.tabs.addTab(self.tab_templates, '模板')

        # 恢复上次选中的标签页（从用户首选项中获取）
        self.tabs.setCurrentIndex(self.get_optvar('selected_main_tab', 0))

        # 构建菜单栏
        # self.build_menu_bar()

        # 连接标签页切换信号与槽函数
        self.tabs.currentChanged.connect(self.tab_changed)

    def tab_changed(self, v):
        self.set_optvar('selected_main_tab', v)

    # ----- menu ---------------------------------------------------------------
    def build_menu_bar(self):
        """
        构建MikanUI应用程序的菜单栏

        该方法负责：
        1. 清除现有菜单项
        2. 加载工具菜单和帮助菜单
        3. 添加用户自定义菜单
        4. 在菜单栏右上角显示项目信息
        """
        # 获取菜单栏实例
        menu_bar = self.menuBar()

        # 清除菜单栏中所有现有的菜单项
        for action in menu_bar.actions():
            menu_bar.removeAction(action)

        # 获取菜单配置文件路径
        sep = os.path.sep  # 获取当前操作系统的路径分隔符
        base_path = os.path.abspath(__file__).split(sep)  # 获取当前文件的绝对路径并分割
        path_tools = sep.join(base_path[:-1]) + sep + 'tools.yml'  # 构建工具菜单配置文件路径
        # path_help = sep.join(base_path[:-1]) + sep + 'help.yml'  # 构建帮助菜单配置文件路径

        # 获取菜单配置列表
        menus = []
        menus.append(('&Tools', path_tools))  # 添加工具菜单
        # menus += UserPrefs.get('user_menu_paths', [])  # 从用户首选项中获取自定义菜单路径
        # menus.append(('&Help', path_help))  # 添加帮助菜单

        # 更新UI，加载所有菜单
        for name, path in menus:
            IkuraMain.PATHS = self.get_paths_dict(path)  # 设置路径字典，供菜单加载时使用
            menu = self.load_menu(name, path)  # 加载菜单
            if menu and 'Help' not in name:  # 为除帮助菜单外的所有菜单启用可分离功能
                menu.setTearOffEnabled(True)

    def load_menu(self, name, file_menu):
        data = None

        if not os.path.isfile(file_menu):
            log.error('could not find menu file "{}"'.format(file_menu))
            return

        try:
            with open(file_menu, 'r') as stream:
                try:
                    data = ordered_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except (OSError, IOError) as e:
            log.error('could not read menu file "{}": {}'.format(file_menu, e))
            return

        if not data:
            return

        menu = self.menuBar().addMenu(name)
        print(data, menu)
        # IkuraMain.load_menuitems(data, menu)
        return menu

    @staticmethod
    def get_paths_dict(path_yml):
        sep = os.path.sep
        base_path = os.path.abspath(__file__).split(sep)

        path_mikan = sep.join(base_path[:-3])
        path_utils = path_mikan + sep + 'maya' + sep + 'utils'
        path_ui = sep.join(base_path[:-1])

        # get paths from yml
        path_menu = os.path.split(path_yml)[0]

        paths = {
            'mikan': path_mikan,
            'ui': path_ui,
            'vendor': path_mikan + sep + 'vendor',
            'utils': path_utils,
            'snippets': path_utils + sep + 'snippets',
            'rig': path_menu,  # legacy
            'menu': path_menu,
        }

        # # add project path
        # path_project = find_maya_project_root(path_yml)
        # if path_project:
        #     paths['project'] = path_project

        return paths

class IkuraUI(toolsetwidget.ToolsetWidget):
    id = "ikura"
    uiData = {"label": "Ikura Window",
              "icon": "hive",
              "tooltip": "Modular Rigging Tool",
              "defaultActionDoubleClick": False
              }

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run"""
        pass

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        parent = QtWidgets.QWidget(parent=self)
        self.widgetsAll(parent)
        self.allLayouts(parent)
        return parent

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiConnections()

    def defaultAction(self):
        """Double Click"""
        pass

    # ------------------
    # PROPERTIES
    # ------------------
    def widgetsAll(self, parent):
        """Create all widgets for the GUI here

        See elements.py for all available widgets in the Zoo PySide framework.
        cgrig_pyside repo then cgrig.libs.pyqt.widgets.elements

        :param parent: The parent widget
        :type parent: obj
        """
        self.mainui = IkuraMain()

    # ------------------
    # UI Layouts
    # ------------------

    def allLayouts(self, parent):
        """Builds the layout for the GUI.  Builds all qt layouts and adds all widgets

        :param parent: the parent widget
        :type parent: obj
        """
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(parent, margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)
        # Add To Main Layout ---------------------------------------
        mainLayout.addWidget(self.mainui)
    # ------------------
    # CALLBACKS
    # ------------------

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        # handles the coPlanar close event
        pass

