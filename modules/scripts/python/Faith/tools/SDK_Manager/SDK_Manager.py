# -*- coding: utf-8 -*-
import time
from functools import partial
from imp import reload

import maya.mel as mel
import maya.cmds as cmds
from Faith.vendor.Qt import QtCore, QtWidgets, QtGui
# ui import
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from ...maya_utils import ui_utils, sdk_utils, python_utils, decorator_utils
from ...tools.SDK_Manager.UI import UI as mui

PY2 = python_utils.PY2

reload(sdk_utils)
reload(mui)


class MainSDKGUI(QtWidgets.QDialog, mui.Ui_Form):
    """
    main ui window
    """

    def __init__(self, parent=None):
        super(MainSDKGUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        # self.driver_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.driven_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.installEventFilter(self)


class DockableMainUI(MayaQWidgetDockableMixin, QtWidgets.QDialog, sdk_utils.AnimationCurveIO_API):

    def __init__(self, parent=None):
        self.comp_menu = None
        self.gmc_layout = None
        self.allSDKInfo_dict = {}
        self.is_source = True
        self.uiName = "SDKManager"
        # self.clickType = "after"
        super(DockableMainUI, self).__init__(parent=parent)

        self.mainUI = MainSDKGUI()
        self.mirrorTypes = {}
        self.context_menu = TypeRadioButtonMenu(self)
        self.start_dir = cmds.workspace(q=True, rootDirectory=True)
        self.create_window()
        self.create_layout()
        self.create_connections()

    def create_window(self):

        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("SDK Tool v0.0.1")
        self.resize(900, 560)
        self.setStyleSheet(ui_utils.qss)
        self.mainUI.node_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainUI.driven_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def create_layout(self):
        """
        create layouts
        :return:
        """
        self.gmc_layout = QtWidgets.QVBoxLayout()
        self.gmc_layout.addWidget(self.mainUI)
        self.gmc_layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self.gmc_layout)

    def create_connections(self):
        """
        ui slots connections
        :return:
        """
        self.mainUI.loadDrv_btn.clicked.connect(self.loadObj)
        self.mainUI.node_list.itemClicked.connect(self.refreshDrv)
        self.mainUI.driven_list.itemClicked.connect(self.updateDriven)
        # self.mainUI.node_list.customContextMenuRequested.connect(partial(self.compMenu, self.mainUI.node_list))
        self.mainUI.driven_list.customContextMenuRequested.connect(partial(self.compMenu, self.mainUI.driven_list))
        self.context_menu.action_group.triggered.connect(self.on_option_selected)
        self.mainUI.mirrorSel_btn.clicked.connect(self.mirrorSelected)
        self.mainUI.mirrorAll_btn.clicked.connect(self.mirrorAll)
        self.mainUI.del_btn.clicked.connect(self.delUselessNode)
        self.mainUI.load_btn.clicked.connect(self.loadPath)
        self.mainUI.expSel_btn.clicked.connect(partial(self.exportSdk, True))
        self.mainUI.expAll_btn.clicked.connect(partial(self.exportSdk, False))
        self.mainUI.expScene_btn.clicked.connect(self.exportSceneSdk)
        self.mainUI.Imp_btn.clicked.connect(self.importSdk)

    def on_option_selected(self, action):
        """处理选项选择"""
        if not self.context_menu.current_items:
            return

        selected_index = self.context_menu.options.index(action.text())

        for item in self.context_menu.current_items:
            # 存储选择到item数据中
            item.setData(QtCore.Qt.UserRole, selected_index)

            self.mirrorTypes[item.text()] = selected_index

    def importSdk(self, *args):
        filePath = self.mainUI.path_le.text()
        if filePath == "":
            return
        sdk_utils.AnimationCurveIO_API().import_animation_curves(filePath)

    def exportSdk(self, select=False, driver=None, *args):
        filePath = self.mainUI.path_le.text()
        exportData = {}
        if filePath == "":
            return
        if driver:
            pass
        else:
            if select:
                if self.mainUI.driven_list.selectedIndexes():
                    for i in self.mainUI.driven_list.selectedItems():
                        sdk_data = self.getSdkConnections(i.data(0), True)
                        exportData.update(sdk_data)
            else:
                if self.mainUI.node_list.selectedIndexes():
                    for i in range(self.mainUI.driven_list.count()):
                        sdk_data = self.getSdkConnections(self.mainUI.driven_list.item(i).text(), True)
                        exportData.update(sdk_data)
        sdk_utils.AnimationCurveIO_API().exportSdks(exportData, filePath)

    def loadPath(self, *args):
        filepath, type = QtWidgets.QFileDialog.getSaveFileName(self, 'import', '/', 'json(*.json)')
        if not filepath:
            return
        self.mainUI.path_le.setText(filepath)

    def mirrorNodeSdk(self, node, is_source):
        sdkConnectionData = self.getSdkConnections(node, is_source)
        for animCurve, data in sdkConnectionData.items():
            input_node = data["input_connections"][0]
            if cmds.objectType(node) == 'blendShape':
                output_nodes = []
                for output_node in data["output_connections"]:
                    if output_node.split('.')[0] == node:
                        output_nodes.append(output_node)
            else:
                output_nodes = data["output_connections"]

            sym_input_info = self.find_symmetric_attribute(input_node)
            sym_outputs_info = [self.find_symmetric_attribute(out) for out in output_nodes]
            sym_input_node = '{0}.{1}'.format(sym_input_info["symmetric_object"], sym_input_info["symmetric_attribute"]) if sym_input_info["status"] == "success" else ""
            sym_outputs_nodes = []
            if sym_input_node == "":
                continue
            for sym_output in sym_outputs_info:
                sym_output_node = '{0}.{1}'.format(sym_output["symmetric_object"], sym_output["symmetric_attribute"]) if sym_output["status"] == "success" else ""
                if sym_output_node == "":
                    continue
                sym_outputs_nodes.append(sym_output_node)

            # 如果获取到的对称的驱动物体名字，被驱动物体名字和现在的一样，则不需要镜像
            for output, sym_output in zip(output_nodes, sym_outputs_nodes):
                if output == sym_output:
                    sym_outputs_nodes.remove(sym_output)

            for i, out in enumerate(sym_outputs_nodes):
                existsAnimCurves = self.getAnimCurve(sym_input_node, out)
                outNode, outAttr = output_nodes[i].split('.')[0], output_nodes[i].split('.')[-1]
                symOutNode, symOutAttr = out.split('.')[0], out.split('.')[-1]
                value_scale = 1

                if self.mirrorTypes[outNode] == 1:
                    if 'translate' in symOutAttr:
                        value_scale = -1
                elif self.mirrorTypes[outNode] == 2:
                    if 'translateX' in symOutAttr or 'rotateY' in symOutAttr or 'rotateZ' in symOutAttr:
                        value_scale = -1

                if existsAnimCurves:
                    if existsAnimCurves[0] == animCurve:
                        continue
                    self.setAnimCurve(existsAnimCurves[0], data, value_scale)
                else:
                    for k in range(len(data["times"])):
                        cmds.setDrivenKeyframe(symOutNode, at=symOutAttr,
                                               cd=sym_input_node,
                                               dv=data["times"][k], v=data["values"][k] * value_scale)

                    animCurrentCrv = self.getAnimCurve(sym_input_node, out)
                    if animCurrentCrv:
                        self.setAnimCurve(animCurrentCrv[0], data, value_scale)

    def exportSceneSdk(self, *args):
        file_path = self.mainUI.path_le.text()
        self.export_animation_curves(file_path)

    @decorator_utils.one_undo
    def mirrorAll(self, *args):
        mirrorDrivens = []

        if not self.mainUI.node_list.selectedIndexes():
            cmds.warning(u"请选择ui中的一个驱动物体!")
            return

        for i in range(self.mainUI.driven_list.count()):
            node = self.mainUI.driven_list.item(i).text()
            self.mirrorNodeSdk(node, True)

    @decorator_utils.one_undo
    def mirrorSelected(self, *args):
        if not self.mainUI.node_list.selectedIndexes():
            return

        mirrorDrivens = [item.data() for item in self.mainUI.driven_list.selectedIndexes()]

        for node in mirrorDrivens:
            self.mirrorNodeSdk(node, True)

    def compMenu(self, widget, pos, *args):
        item = widget.itemAt(pos)
        selected_items = widget.selectedItems()

        if item and item not in selected_items:
            selected_items = [item]

        real_items = []
        if selected_items:
            for item in selected_items:
                name = item.text()
                if 'transform' in cmds.objectType(name):
                    real_items.append(item)
        self.context_menu.set_current_items(real_items)
        self.context_menu.exec_(widget.mapToGlobal(pos))

    def updateDriven(self, *args):
        cmds.select(d=True)
        if self.mainUI.driven_list.selectedIndexes():
            for item in self.mainUI.driven_list.selectedIndexes():
                node = item.data()
                if cmds.objExists(node):
                    cmds.select(node, add=True)

    def refreshDrv(self, *args):
        self.mainUI.driven_list.clear()

        drivers = []
        drivens = []

        if self.mainUI.node_list.selectedIndexes():
            item = self.mainUI.node_list.currentItem()
            node = item.text()
            if cmds.objExists(node):
                cmds.select(node, r=True)

            sdkConnectionsData = self.getSdkConnections(node, False)
            for animCurve, data in sdkConnectionsData.items():
                drivers += data["input_connections"]
                drivens += data["output_connections"]

            add_drivens = list(sorted(set([drv.split('.')[0] for drv in list(set(drivens))])))
            for add in add_drivens:
                self.mainUI.driven_list.addItem(add)
                self.mirrorTypes[add] = 0

    @decorator_utils.one_undo
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
        # self.mainUI.loadDrv_btn.setText()
        self.mainUI.node_list.addItems(sorted([obj for obj in selection]))

    def mirrorKeys(self, nodeList, *args):
        """

        :param nodeList:
        :param args:
        :return:
        """
        if not isinstance(nodeList, list):
            raise TypeError
        for node in nodeList:
            drivenNodes = self.getDrivenNodes(node, [], "after")
            sdk_utils.mirrorSDKs(drivenNodes, attributes=[], type="front")

    @decorator_utils.one_undo
    def mirrorNode(self, widget=None, *args):
        """

        :return:
        """
        selectAttrs = []
        if widget and widget.selectedIndexes():
            selectAttrs = [item.data().split('.')[1] for item in widget.selectedIndexes() if cmds.objExists(item.data())]
            node = [item.data().split('.')[0] for item in widget.selectedIndexes() if cmds.objExists(item.data())]
            if widget == self.mainUI.driver_list:
                sdk_utils.mirrorSDKs([node[0]], attributes=selectAttrs, type="after")
            elif widget == self.mainUI.driven_list:
                sdk_utils.mirrorSDKs([node[0]], attributes=selectAttrs, type="front")

    @decorator_utils.one_undo
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


class ListItemWidget(QtWidgets.QWidget):
    def __init__(self, text, addCombo=True, parent=None):
        super().__init__(parent)
        # 创建水平布局
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 设置边距

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)
        if addCombo:
            self.combo = QtWidgets.QComboBox()
            self.combo.addItems(["Base", "Skeleton", "World"])
            layout.addWidget(self.combo)

            # 使用样式表固定ComboBox宽度和位置
            self.setStyleSheet("""
                        QComboBox {
                            min-width: 120px;
                            max-width: 120px;
                            margin-left: 10px;
                        }
                    """)

        self.setLayout(layout)


class TypeRadioButtonMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(u"镜像类型")

        # 创建互斥的 ActionGroup
        self.action_group = QtWidgets.QActionGroup(self)
        self.action_group.setExclusive(True)

        # 添加单选按钮选项
        self.options = [u"完全对称", u"骨骼模式对称", u"世界位置"]
        self.actions = []
        for i, text in enumerate(self.options):
            action = QtWidgets.QAction(text, self)
            action.setCheckable(True)
            if i == 0:  # 默认选中"中优先级"
                action.setChecked(True)
            self.action_group.addAction(action)
            self.addAction(action)
            self.actions.append(action)

        # 存储当前选中的项
        self.current_items = []

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
            # 如果选择不一致，默认选中"中"优先级
            self.actions[0].setChecked(True)


def show_guide_component_manager(*args):
    ui_utils.showDialog(DockableMainUI, dockable=True)
