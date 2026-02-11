# -*- coding: utf-8 -*-
""" ---------- Toolset Boiler Plate (Single Mode) -------------
The following code is a template (boiler plate) for building Zoo Toolset GUIs that have a single mode.

A single mode means there is no compact and medium or advanced modes.

"""
from functools import partial
from maya import cmds
from maya import mel
from cgrigvendor.Qt import QtWidgets, QtCore
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt.widgets.elements import styledButton as button
from cgrig.libs.pyqt.widgets.elements import hBoxLayout, vBoxLayout, Label, PathWidget
from cgrig.libs import sdk_io
import time


class Ui_Form(object):
    def setupUi(self, Form):
        self.verticalLayout_2 = vBoxLayout(Form)
        self.tab_3 = QtWidgets.QWidget()
        self.verticalLayout = vBoxLayout(self.tab_3)
        self.horizontalLayout_4 = hBoxLayout()
        self.loadDrv_btn = button(parent=self.tab_3)
        self.horizontalLayout_4.addWidget(self.loadDrv_btn)
        self.del_btn = button(parent=self.tab_3)
        self.horizontalLayout_4.addWidget(self.del_btn)
        self.spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.spacer)
        self.source_cb = QtWidgets.QCheckBox(self.tab_3)
        self.horizontalLayout_4.addWidget(self.source_cb)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = hBoxLayout()
        self.verticalLayout_14 = vBoxLayout()
        self.label_9 = Label(parent=self.tab_3)
        self.verticalLayout_14.addWidget(self.label_9)
        self.node_list = QtWidgets.QListWidget(self.tab_3)
        self.node_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.verticalLayout_14.addWidget(self.node_list)
        self.horizontalLayout_6.addLayout(self.verticalLayout_14)
        self.verticalLayout_16 = vBoxLayout()
        self.label_11 = Label(parent=self.tab_3)
        self.verticalLayout_16.addWidget(self.label_11)
        self.driven_list = QtWidgets.QListWidget(self.tab_3)
        self.driven_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.verticalLayout_16.addWidget(self.driven_list)
        self.horizontalLayout_6.addLayout(self.verticalLayout_16)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = hBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.path_wdget = PathWidget()
        self.path_wdget.setSearchFilter("*.json")
        self.verticalLayout.addWidget(self.path_wdget)
        self.horizontalLayout_3 = hBoxLayout()
        self.Imp_btn = button(parent=self.tab_3)
        self.horizontalLayout_3.addWidget(self.Imp_btn)
        self.expScene_btn = button(parent=self.tab_3)
        self.horizontalLayout_3.addWidget(self.expScene_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.tab_3)
        # self.label_9.addActionList(["adad", "Sdad"], mouseButton=QtCore.Qt.RightButton)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.loadDrv_btn.setText(_translate("Form", "Load Nodes"))
        self.del_btn.setText(_translate("Form", "Delete Useless Nodes"))
        self.source_cb.setText(_translate("Form", "source"))
        self.label_9.setText(_translate("Form", "Node"))
        self.label_11.setText(_translate("Form", "Driven"))
        self.Imp_btn.setText(_translate("Form", "Import"))
        self.expScene_btn.setText(_translate("Form", "Export Scene SDK"))


class main_sdk_ui(QtWidgets.QDialog, Ui_Form):
    leftClicked = QtCore.Signal()
    middleClicked = QtCore.Signal()
    rightClicked = QtCore.Signal()
    stateChanged = QtCore.Signal(object)
    def __init__(self, parent=None):
        super(main_sdk_ui, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        self.node_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.driven_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.installEventFilter(self)


class TypeRadioButtonMenu(QtWidgets.QMenu):
    def __init__(self, file_path, is_source=True, init=True, parent=None):
        super().__init__(parent)
        self.setTitle(u"镜像类型")
        self.options = [u"完全对称", u"骨骼模式对称", u"世界位置"]
        self.settings = QtCore.QSettings("type_menu", "type_index")
        self.selected_index = self.load_last_index()
        self.file_path = file_path
        self.is_source = is_source
        self.file_path = file_path
        self.is_source = is_source
        self.mirrorType = 0
        # 创建互斥的 ActionGroup
        self.action_group = QtWidgets.QActionGroup(self)
        self.action_group.setExclusive(True)

        # 添加单选按钮选项
        self.actions = []
        self.mirror_action = QtWidgets.QAction(u"镜像", self)
        self.export_action = QtWidgets.QAction(u"导出", self)
        self.is_source = is_source
        if not init:
            for i, text in enumerate(self.options):
                action = QtWidgets.QAction(text, self)
                action.setCheckable(True)
                if i == 0:
                    action.setChecked(True)
                self.action_group.addAction(action)
                self.addAction(action)
                self.actions.append(action)
            self.addAction(self.mirror_action)
            self.addAction(self.export_action)
            self.actions += [self.mirror_action, self.export_action]
        # 存储当前选中的项
        self.current_items = []
        self.mirror_action.triggered.connect(self.mirror)
        self.action_group.triggered.connect(self.on_option_selected)
        self.export_action.triggered.connect(partial(self.exportSdk, file_path))

    def set_current_items(self, items):
        """设置当前右键点击的项"""
        self.current_items = items
        if not items:
            return
        # 从 item 数据中恢复之前的选择状态
        first_index = items[0].data(QtCore.Qt.UserRole)
        all_same = all(item.data(QtCore.Qt.UserRole) == first_index for item in items)
        if all_same and first_index is not None and 0 <= first_index < len(self.actions):
            self.actions[first_index].setChecked(True)
        else:
            if self.actions:
                # 如果选择不一致，默认选中"中"优先级
                self.actions[0].setChecked(True)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def mirror(self):
        for item in self.current_items:
            node = item.text()
            sdk_io.mirrorNodeSdk(node, self.is_source, mirror_type=self.selected_index)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def on_option_selected(self, action):
        """处理选项选择"""
        if not self.current_items:
            return

        selected_index = self.options.index(action.text())
        self.selected_index = selected_index
        for item in self.current_items:
            # 存储选择到item数据中
            item.setData(QtCore.Qt.UserRole, selected_index)
            self.save_last_index()

    def save_last_index(self):
        """用QSettings保存序号到系统配置"""
        self.settings.setValue("selected_index", self.selected_index)

    def load_last_index(self):
        """从QSettings读取上次保存的序号"""
        index = self.settings.value("selected_index", 0, type=int)
        return index

    @toolsetwidget.ToolsetWidget.undoDecorator
    def exportSdk(self, filePath, *args):
        exportData = {}
        if filePath == "":
            return

        for item in self.current_items:
            node = item.text()
            sdk_data = sdk_io.getSdkConnections(node, self.is_source)
            exportData.update(sdk_data)

        sdk_io.exportSdks(exportData, filePath)


class SDKTool(toolsetwidget.ToolsetWidget):
    id = "sdkBatch"
    info = "SDK Tool GUI."
    uiData = {"label": "SDK Tool",
              "icon": "yaochi",
              "tooltip": "SDK GUI.",
              "defaultActionDoubleClick": False}

    # ------------------
    # STARTUP
    # ------------------

    is_source = True
    allSDKInfo_dict = {}
    mirrorTypes = {}

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        pass

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced, in this case we are only building one UI mode """
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
        """Double Click
        Double clicking the tools toolset icon will run this method
        Be sure "defaultActionDoubleClick": True is set inside self.uiData (meta data of this class)"""
        pass

    # ------------------
    # UI WIDGETS
    # ------------------

    def widgetsAll(self, parent):
        """Create all widgets for the GUI here

        See elements.py for all available widgets in the Zoo PySide framework.
        cgrig_pyside repo then cgrig.libs.pyqt.widgets.elements

        :param parent: The parent widget
        :type parent: obj
        """
        self.mainUI = main_sdk_ui()
        # self.context_menu = TypeRadioButtonMenu('', True, False, parent=self.mainUI)

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
        mainLayout.addWidget(self.mainUI)

    # ------------------
    # LOGIC
    # ------------------

    def loadObj(self, *args):
        """

        :return:
        """
        self.mainUI.node_list.clear()
        self.mainUI.driven_list.clear()
        selection = cmds.ls(sl=1)

        if not selection:
            cmds.warning(u"请至少选择一个物体!")
            return

        self.mainUI.node_list.addItems(sorted([obj for obj in selection]))

    def refreshDrv(self, *args):
        self.mainUI.driven_list.clear()

        if self.mainUI.node_list.selectedIndexes():
            item = self.mainUI.node_list.currentItem()
            node = item.text()
            if cmds.objExists(node):
                cmds.select(node, r=True)

            adds = self.getDriveList(node)
            for add in adds:
                self.mainUI.driven_list.addItem(add)
                self.mirrorTypes[add] = 0

    def getDriveList(self, node):
        is_source = self.mainUI.source_cb.isChecked()
        sdkConnectionsData = sdk_io.getSdkConnections(node, is_source)
        drivers = []
        drivens = []
        for animCurve, data in sdkConnectionsData.items():
            drivers += data["input_connections"]
            drivens += data["output_connections"]
        add_drivens = list()
        if is_source:
            add_drivens = list(sorted(set([drv.split('.')[-1] for drv in list(set(drivens))])))
        else:
            add_drivens = list(sorted(set([drv.split('.')[0] for drv in list(set(drivens))])))
        return add_drivens

    def updateDriven(self, *args):
        cmds.select(d=True)
        if self.mainUI.driven_list.selectedIndexes():
            for item in self.mainUI.driven_list.selectedIndexes():
                node = item.data()
                if cmds.objExists(node):
                    cmds.select(node, add=True)

    def compMenu(self, widget, pos, *args):
        is_source = self.mainUI.source_cb.isChecked()
        filePath = self.mainUI.path_wdget.path()
        self.context_menu = TypeRadioButtonMenu(filePath, is_source, False, self)
        item = widget.itemAt(pos)
        selected_items = widget.selectedItems()

        if item and item not in selected_items:
            selected_items = [item]

        if not is_source and widget == self.mainUI.driven_list:
            is_source = not is_source
        real_items = []
        if selected_items:
            for item in selected_items:
                node = item.text()
                if not cmds.objExists(node):
                    self.context_menu = TypeRadioButtonMenu(filePath, is_source, True, self)
                real_items.append(item)
        self.context_menu.set_current_items(real_items)
        self.context_menu.exec_(widget.mapToGlobal(pos))


    @toolsetwidget.ToolsetWidget.undoDecorator
    def delUselessNode(self):

        """delete all useless node"""
        # -------------------------------------------------
        # Delete all useless node in current scene.
        # -------------------------------------------------

        try:
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')
        except:
            pass
        removeType = ["animCurve", "blendWeighted"]
        ani = cmds.ls(type=removeType)

        if len(ani) == 0:
            pass
        else:
            progress_dialog = QtWidgets.QProgressDialog(
                "Waiting to process...", "Cancel", 0, 8, self
            )
            progress_dialog.setWindowTitle("Delete Useless Nodes")
            progress_dialog.setValue(0)
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()

            QtCore.QCoreApplication.processEvents()
            removeNodes = []
            for i, x in enumerate(ani):
                if progress_dialog.wasCanceled():
                    break
                if cmds.objExists(x):
                    hasInput = cmds.listConnections(x, s=True, d=False, scn=True)
                    hasOutput = cmds.listConnections(x, s=False, d=True, scn=True)
                    if 'hyperLayout' in str(hasOutput) and len(hasOutput) == 1:
                        hasOutput = None
                    isLocked = cmds.lockNode(x, q=1, l=1)[0]
                    if isLocked:
                        cmds.lockNode(x, l=False)
                    if (not hasInput) or (not hasOutput):
                        if "scalePower" not in x:
                            removeNodes.append(x)
            for i in range(0, len(removeNodes)):
                progress_dialog.setLabelText("Delete useless node %s." % (removeNodes[i]))
                progress_dialog.setValue(i)
                cmds.delete(removeNodes[i])
                time.sleep(0.5)
                QtCore.QCoreApplication.processEvents()
            progress_dialog.close()

    def exportSceneSdk(self, *args):
        file_path = self.mainUI.path_wdget.path()
        sdk_io.export_animation_curves(file_path)

    def importSdk(self, *args):
        filePath = self.mainUI.path_wdget.path()
        if filePath == "":
            return
        sdk_io.import_animation_curves(filePath)

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        self.mainUI.loadDrv_btn.clicked.connect(self.loadObj)
        self.mainUI.node_list.itemClicked.connect(self.refreshDrv)
        self.mainUI.driven_list.itemClicked.connect(self.updateDriven)
        self.mainUI.node_list.customContextMenuRequested.connect(partial(self.compMenu, self.mainUI.node_list))
        self.mainUI.driven_list.customContextMenuRequested.connect(partial(self.compMenu, self.mainUI.driven_list))
        self.mainUI.del_btn.clicked.connect(self.delUselessNode)
        self.mainUI.expScene_btn.clicked.connect(self.exportSceneSdk)
        self.mainUI.Imp_btn.clicked.connect(self.importSdk)
