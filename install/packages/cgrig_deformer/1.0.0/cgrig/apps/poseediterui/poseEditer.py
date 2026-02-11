""" ---------- Toolset Boiler Plate (Single Mode) -------------
The following code is a template (boiler plate) for building Zoo Toolset GUIs that have a single mode.

A single mode means there is no compact and medium or advanced modes.

"""
import os
import json
import collections
import re
from functools import partial
from cgrigvendor.Qt import QtWidgets, QtCore, QtGui
from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs import sdk_io
from cgrig.libs.pose import pose_util, pose_driver_api
from cgrig.libs.maya.cmds.objutils import attributes
from cgrig.libs.maya.cmds.rig import blendshape
from cgrig.libs.naming import naming
from cgrig.libs import serializers
from cgrig.libs.iconlib import iconlib
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.pyqt.widgets.elements import hBoxLayout, vBoxLayout
from maya import cmds
from cgrig.libs.pose import drivertypes
from cgrig.libs.pose.core import node_types
from cgrig.apps.poseediterui.selectui import SelectDialog


class SpacingDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, spacing=10):
        super().__init__(parent)
        self.spacing = spacing

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + self.spacing)  # 增加间距
        return size


class CtrlClickEventFilter(QtCore.QObject):
    def __init__(self, list_view):
        super().__init__()
        self.list_view = list_view

    def eventFilter(self, obj, event):
        # 只处理鼠标按下事件
        if event.type() == QtCore.QEvent.MouseButtonPress:
            # 检查是否按下了 Ctrl 键
            if event.modifiers() & QtCore.Qt.ControlModifier:
                # 获取当前点击的项
                index = self.list_view.indexAt(event.pos())
                if index.isValid() and self.list_view.selectionModel().isSelected(index):
                    # 取消选择当前项
                    self.list_view.selectionModel().select(
                        index,
                        QtCore.QItemSelectionModel.Deselect
                    )
                    return True
        return super().eventFilter(obj, event)


class PoseEditorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(PoseEditorWindow, self).__init__(parent)
        self.bs_targets = None
        self.bs_node = None
        self.pose_driver_create_btn = None
        self.scale_field = None
        self.axis_combo = None
        self.pose_center_radio = None
        self.pose_right_radio = None
        self.pose_left_radio = None
        self._extensions = None
        self._current_solver = None
        self.absWorld = True
        self.poses = None
        self.keyFrameNodes = []
        self.poseGrpNodes = []
        self.allSetupsInfo = {}
        self._currentPose = None
        self.bs_mesh = None
        self.is_pose_driver = False
        # self.pose_driver_ui = "pose_driver_win"
        # self.weight_grp = "weight_rbf_grp"
        self.setWindowTitle("Pose Editor")
        self.create_menus()
        self.create_main_widget()
        self.create_connections()
        # self.show_type_panel()
        # self.load()
        # self.updateKeyFrame()

    def create_menus(self):
        # 创建菜单栏
        self.menubar = self.menuBar()

        # 文件菜单
        self.file_menu = self.menubar.addMenu("File")
        self.import_rbfs_action = QtWidgets.QAction('Import RBFs', self)
        self.file_menu.addAction(self.import_rbfs_action)
        self.export_rbfs_action = QtWidgets.QAction('Export All RBFs', self)
        self.file_menu.addAction(self.export_rbfs_action)
        self.export_selected_rbf_action = QtWidgets.QAction('Export_Selected_Rbf', self)
        self.file_menu.addAction(self.export_selected_rbf_action)

        # 镜像菜单
        self.mirror_menu = self.menubar.addMenu("Mirror")
        self.mirror_all_rbfs_action = QtWidgets.QAction('Mirror All RBFs', self)
        self.mirror_menu.addAction(self.mirror_all_rbfs_action)
        self.mirror_selected_rbfs_action = QtWidgets.QAction('Mirror Selected RBFs', self)
        self.mirror_menu.addAction(self.mirror_selected_rbfs_action)

        # # 类型菜单
        # self.type_transform_action = QtWidgets.QAction('Transform', self)
        # self.type_blendShape_action = QtWidgets.QAction('BlendShape', self)
        # self.is_pose_driver_action = QtWidgets.QAction('IsPoseDriver', self)
        # self.is_pose_driver_action.setCheckable(True)
        #
        # self.type_action_group = QtWidgets.QActionGroup(self)
        # self.type_action_group.setExclusive(True)
        #
        # self.type_transform_action.setCheckable(True)
        # self.type_transform_action.setChecked(True)
        # self.type_action_group.addAction(self.type_transform_action)
        #
        # self.type_blendShape_action.setCheckable(True)
        # self.type_action_group.addAction(self.type_blendShape_action)
        #
        # self.type_menu = self.menubar.addMenu("Type")
        # self.type_menu.addAction(self.type_transform_action)
        # self.type_menu.addAction(self.type_blendShape_action)
        # self.type_menu.addAction(self.is_pose_driver_action)
        #
        # self.type_transform_action.triggered.connect(self.show_type_panel)
        # self.type_blendShape_action.triggered.connect(self.show_type_panel)
        # self.is_pose_driver_action.triggered.connect(self.show_type_panel)

    def show_type_panel(self, *args):
        if self.is_pose_driver_action.isChecked():
            self.is_pose_driver = True
            self.load()
            self.center_title_refresh_btn.setEnabled(False)
            self.center_title_add_btn.setEnabled(False)
            self.center_title_delete_btn.setEnabled(False)
        else:
            self.is_pose_driver = False
            self.center_title_refresh_btn.setEnabled(True)
            self.center_title_add_btn.setEnabled(True)
            self.center_title_delete_btn.setEnabled(True)
        if self.type_transform_action.isChecked():
            self.bs_panel.setHidden(True)
            self.right_splitter.setHidden(False)
        elif self.type_blendShape_action.isChecked():
            self.bs_panel.setHidden(False)
            self.right_splitter.setHidden(True)

    def create_main_widget(self):
        # 主中心部件
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # 主分割器 - 水平分割（左中右）
        self.main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # 左侧面板
        self.left_panel = elements.ListEditWidget('Pose 驱动')

        # 中间面板
        self.center_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        center_layout = QtWidgets.QVBoxLayout(self.center_splitter)
        center_layout.addWidget(elements.ListEditWidget('Pose 名称'))
        center_layout.addWidget(elements.ListEditWidget('Shape 列表'))
        self.center_splitter.setSizes([100, 70])

        # 将三个面板添加到主分割器
        self.main_splitter.addWidget(self.left_panel)
        self.main_splitter.addWidget(self.center_splitter)

        # 设置主分割器初始大小
        self.main_splitter.setSizes([180, 180])

        # 主布局
        self.main_layout = hBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.addWidget(self.main_splitter)


    def create_connections(self):
        # self.interpolators_list.clicked.connect(self.on_selection_changed)
        # self.details_list.clicked.connect(self.on_selection_show_attrs)
        #
        self.left_panel.plus_click.connect(self.addSetup)
        # self.left_title_refresh_btn.clicked.connect(self.load)
        #
        # self.center_title_add_btn.clicked.connect(self.addPose)
        # self.center_title_delete_btn.clicked.connect(self.deletePose)
        #
        # self.pose_list.clicked.connect(self.recallDriverPose)
        # self.right_top_title_apply_btn.clicked.connect(self.loadSdkDriven)
        # self.right_top_title_key_btn.clicked.connect(self.setDefaultKey)
        #
        # self.mirror_selected_rbfs_action.triggered.connect(self.mirrorSetup)
        # self.mirror_all_rbfs_action.triggered.connect(partial(self.mirrorSetup, False))
        # self.export_selected_rbf_action.triggered.connect(partial(self.exportNodes, False))
        # self.export_rbfs_action.triggered.connect(partial(self.exportNodes, True))
        # self.import_rbfs_action.triggered.connect(self.importNodes)
        #
        # self.setKey_action.triggered.connect(self.setKey)
        # self.deleteKey_action.triggered.connect(self.deleteKey)
        #
        # self.bs_title_load_btn.clicked.connect(self.loadBsMesh)
        #
        # self.bs_title_sculpt_btn.clicked.connect(self.apply_edit)
        # self.bs_delete_action.triggered.connect(self.deleteTarget)
        # self.bs_mirror_action.triggered.connect(self.mirror_by_targets)
        # self.bs_generate_action.triggered.connect(self.generateTarget)
        #
        # self.bs_copy_action.triggered.connect(self.copyBs)
        # self.bs_model.itemChanged.connect(self.renameTarget)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def loadSdkDriven(self):
        selected = cmds.ls(selection=True)
        if not selected:
            return
        for sel in selected:
            item = QtGui.QStandardItem(sel)
            # if not qtutils.is_item_exist(self.details_list, sel):
            self.details_list_model.appendRow(item)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def copyBs(self, skipLock=True, replaceConnect=True):
        selections = cmds.ls(selection=True)
        if not selections: return
        oldMesh = self.bs_mesh
        bsNode = self.bs_node
        if not bsNode:
            return

        copyTargets = [self.bs_list.selectedIndexes()[i].data() for i in range(len(self.bs_list.selectedIndexes()))]
        targets = self.bs_targets
        if not targets:
            return

        for target in copyTargets:
            if skipLock:
                if cmds.getAttr(bsNode + '.' + target, lock=True):
                    copyTargets.remove(target)

        for newMesh in selections:
            blendshape.copyBs(oldMesh, newMesh, skipLock=skipLock, replaceConnect=replaceConnect)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def generateTarget(self):
        if not self.bs_list.selectedIndexes(): return
        bsNode = self.bs_node
        for i, index in enumerate(self.bs_list.selectedIndexes()):
            target_name = self.bs_list.selectedIndexes()[i].data()
            targetGeo = pose_util.regenerateTarget(bsNode, target_name, inbetween=None, connect=True)

    def deleteSetUp(self):
        rbfNode = self.selected_solver
        driverNode = rbfNode.drivers()[0]
        if rbfNode:
            self.delete_rbf_solver(rbfNode)
            if cmds.objExists(f'{driverNode}_rbf_pose_grp'):
                cmds.delete(f'{driverNode}_rbf_pose_grp')

    def delete_rbf_solver(self, solver=None):
        """
        Delete the specified solver

        :param solver:  solver reference
        :type solver: api.RBFNode
        """
        # Delete the solver
        solver.delete()
        # If we are using the UI, delete the solver
        self.delete_solver(solver)

    def delete_solver(self, solver):
        """
        Delete the specified solver from the view
        :param solver :type api.RBFNode: solver ref
        """
        for row in range(self.left_model.rowCount()):
            # 创建当前行的索引
            index = self.left_model.index(row, 0)
            # 获取存储的自定义数据
            item_data = self.left_model.data(index, QtCore.Qt.UserRole)

            # 检查是否匹配要删除的solver
            if item_data and item_data.get('solver') == solver:
                # 从模型中删除该行
                self.left_model.removeRow(row)
                break
        self.pose_model.clear()

    @toolsetwidget.ToolsetWidget.undoDecorator
    def deletePose(self):
        """delete a pose from the UI and all the RBFNodes in the setup.

        Returns:
            n/a: n/a
        """
        poses = self.get_selected_poses()
        if not poses:
            return
        # Get the selected solver
        solver = self.selected_solver
        driverNode = solver.drivers()[0]
        for pose_name in poses:
            if cmds.objExists(f'{driverNode}_rbf_pose_grp.{pose_name}'):
                cmds.deleteAttr(f'{driverNode}_rbf_pose_grp.{pose_name}')
            self.delete_pose(pose_name, solver)
        poses_list = list(solver.poses().keys())
        for pose_name in poses_list:
            solver.setDrivenNode(driverNode, [pose_name])

        self.refreshTables(solver)

    def delete_pose(self, pose_name, solver=None):
        """
        Remove a pose from the given solver

        :param pose_name: name of the pose to remove
        :type pose_name: str
        :param solver: solver reference
        :type solver: api.RBFNode
        """
        # Ensure we have a solver
        solver = solver or self.selected_solver
        # Delete the pose
        solver.delete_pose(pose_name)

    def get_selected_poses(self):
        poses = []
        if not self.pose_list.selectedIndexes():
            return poses
        for i,index in enumerate(self.pose_list.selectedIndexes()):
            item_text = self.pose_list.selectedIndexes()[i].data()
            poses.append(item_text)
        return poses

    @toolsetwidget.ToolsetWidget.undoDecorator
    def recallDriverPose(self, *args):
        if not self.selected_solver:
            return
        if not self.pose_list.selectedIndexes():
            return
        solver = self.selected_solver
        pose_name = self.pose_list.selectedIndexes()[0].data()
        self.current_pose = pose_name
        if self.is_pose_driver:
            pass
        else:
            solver.go_to_pose(pose_name)
        self.updateKeyFrame()

    def on_selection_changed(self):
        current_node = self.selected_solver
        if current_node:
            if self.is_pose_driver:
                cmds.select(current_node.cmd_node, r=1)
                self.refreshTables(current_node.cmd_node)
            else:
                cmds.select(current_node._node, r=1)
                self.refreshTables(current_node)

    def on_selection_show_attrs(self, index):
        self.additional_info_model.clear()
        if index.isValid():
            selected_item = index.data(QtCore.Qt.DisplayRole)
            if cmds.objExists(selected_item):
                cmds.select(selected_item, r=1)
                plugAttrs = pose_util.getPlugAttrs([selected_item])
                if plugAttrs:
                    for plugAttr in plugAttrs:
                        item = QtGui.QStandardItem(plugAttr.split('.')[-1])
                        self.additional_info_model.appendRow(item)
                        if self._currentPose:
                            animCurves = sdk_io.getAnimCurve(self._currentPose, plugAttr)
                            if animCurves:
                                item.setBackground(QtGui.QColor(65, 120, 180))

    def refreshTables(self, node):
        if self.is_pose_driver:
            self.pose_model.clear()
            for attr in cmds.listAttr(node, k=True, v=True):
                self.pose_model.appendRow(QtGui.QStandardItem(iconlib.Icon.icon("p-head", size=20), attr))
        else:
            data = node.data()
            self.setDriverTable(data)

    def setDriverTable(self, weightInfo):
        poses = weightInfo.get("poses", {})
        self.pose_model.clear()
        poses_list = list(poses.keys())
        for pose in poses_list:
            self.pose_model.appendRow(QtGui.QStandardItem(iconlib.Icon.icon("p-head", size=20), pose))

    @staticmethod
    def deleteAssociatedWidgetsMaya(widget, attrName="associatedMaya"):
        """delete core ui items 'associated' with the provided widgets

        Args:
            widget (QWidget): Widget that has the associated attr set
            attrName (str, optional): class attr to query
        """
        if hasattr(widget, attrName):
            for t in getattr(widget, attrName):
                try:
                    cmds.deleteUI(t, ctl=True)
                except Exception:
                    pass
        else:
            setattr(widget, attrName, [])

    @staticmethod
    def deleteAssociatedWidgets(widget, attrName="associated"):
        """delete widget items 'associated' with the provided widgets

        Args:
            widget (QWidget): Widget that has the associated attr set
            attrName (str, optional): class attr to query
        """
        if hasattr(widget, attrName):
            for t in getattr(widget, attrName):
                try:
                    t.deleteLater()
                except Exception:
                    pass
        else:
            setattr(widget, attrName, [])

    @toolsetwidget.ToolsetWidget.undoDecorator
    def addSetup(self, *args):
        """
        选择骨骼在当前pose创建rbf node
        """
        pose_key = SelectDialog.select(
            options=[
                (i.type_name, i.type_name, i.icon_name)
                for i in node_types
            ],
            parent=self
        )
        if pose_key:
            print("yes, ", pose_key)
            # self.left_panel.updateItems()
            # self.left_panel.updateItems(
            #     [
            #         (i.name(), i.name(), i.icon_path, i.function_table())
            #         for i in get_pose_list()
            #     ]
            # )
        # selected = cmds.ls(sl=1)
        # if not selected: return
        # if self.is_pose_driver:
        #     if len(selected) > 2:
        #         RuntimeError("Please select one joint and parent joint node.")
        #         return
        #     joint, parent_joint = selected[0], selected[-1]
        #     self.create_pose_driver_ui(joint, parent_joint)
        # else:
        #     if len(selected) > 2:
        #         RuntimeError("Please select one control and one joint node.")
        #         return
        #     if cmds.objectType(selected[-1]) != 'joint':
        #         RuntimeError("Please select joint node.")
        #         return
        #     control, joint = selected[0], selected[-1]
        #     solver = self.create_rbf_solver("{joint}_WD".format(joint=joint), drivers=[joint], controllers=[control])
        #     current_rbf_pose_grp = self.createWeightBridge("{joint}_rbf_pose_grp".format(joint=joint), "default")
        #     cmds.setAttr("{}.default".format(current_rbf_pose_grp), 1)
        #     solver.setDrivenNode(current_rbf_pose_grp, ["default"])

    def create_rbf_solver(self, solver_name, drivers=None, controllers=None):
        """
        Create an rbf solver node with the given name and the specified driver transforms

        :param solver_name: name of the solver node
        :type solver_name: str
        :param drivers: list of driver transform node names
        :type drivers: list
        :param controllers: list of driver controllers node names
        :type controllers: list
        :return: RBFNode ref
        :rtype: api.RBFNode
        """
        # If no drivers are specified, grab the current selection
        drivers = drivers or pose_util.get_selection(_type='transform')
        print("Creating RBF solver '{name}' with drivers: {drivers}".format(name=solver_name, drivers=drivers))
        # Create the solver
        solver = ue_rbf_api.RBFNode.create(solver_name)
        # If drivers have been specified, add them
        if controllers:
            solver.add_controller(controllers)
        if drivers:
            self.add_drivers(drivers=drivers, solver=solver)
        # If we are in UI mode, add the solver to the view
        self.add_solver(solver)
        # Set the current solver
        self.current_solver = solver
        # Set the current solver to edit mode
        self.edit_solver(edit=True, solver=solver)
        return solver

    def edit_solver(self, edit=True, solver=None):
        """
        Edit or finish editing the specified solver. Enables pose creation/driven node changes via the ui

        :param edit:  set edit mode on or off
        :type edit: bool
        :param solver: solver reference
        :type solver: api.RBFNode
        """
        # If no solver is specified, grab the current solver
        solver = solver or self._current_solver
        # Edit the solver
        solver.edit_solver(edit=edit)
        # self.edit_solver(solver=solver, edit=edit)
        print("Setting edit status: {status} for solver: {solver}".format(status=edit, solver=solver))
        self.current_solver = solver
        # Return a context manager if edit is True so that users have the option to automatically finish editing
        # instead of running edit_solver twice.
        if edit:
            return pose_util.EditSolverContextManager(self, self.current_solver)

    def createWeightBridge(self, name, pose_name):
        if not cmds.objExists(self.weight_grp):
            self.weight_grp = cmds.createNode('transform', n=self.weight_grp)

        if not cmds.objExists(name):
            cmds.createNode('transform', n=name, p=self.weight_grp)
        if not cmds.objExists('{name}.{pose_name}'.format(name=name, pose_name=pose_name)):
            attributes.createAttribute(
                name, pose_name, attributeType="double", channelBox=True, nonKeyable=False, defaultValue=0,
                minValue=0, maxValue=1
            )
            attributes.lock_and_hide_default(name)
            # attribute.addAttributes(name, pose_name, "double", value=0.0, min=0.0, max=1.0)
            # attribute.lock_and_hide(name)
        return name

    def add_drivers(self, drivers=None, solver=None):
        """
        Add the specified drivers to the specified solver

        :param drivers: list of transform nodes
        :type drivers: list
        :param solver: solver reference
        :type solver: api.RBFNode
        """
        # If no solver is specified, grab the current solver
        solver = solver or self._current_solver
        # If we already have more than one pose, we can't add a new driver (would require manually updating every pose)
        if solver.num_poses() > 1:
            raise pose_exceptions.InvalidPoseIndex("Too many poses have been created, unable to add a new driver.")
        # Check if we have a default pose
        if solver.has_pose(pose_name='default'):
            # Delete the current rest pose if found
            solver.delete_pose(pose_name='default')
        # Add new drivers
        solver.add_driver(transform_nodes=drivers)
        # Create the new rest pose with all the drivers
        solver.add_pose_from_current(pose_name='default')
        # Set the current solver
        self.current_solver = solver

    @toolsetwidget.ToolsetWidget.undoDecorator
    def addPose(self, solver=None):
        """
        给rbf node添加当前驱动骨骼的pose
        """
        # Ensure we have a solver
        solver = solver or self.selected_solver

        pose_name, ok = QtWidgets.QInputDialog.getText(self, 'Create Pose', 'Pose Name:')
        if pose_name:
            driverNode = solver.drivers()[0]
            drivenNode = "{driverNode}_rbf_pose_grp".format(driverNode=driverNode)
            self.createWeightBridge(drivenNode, pose_name)
            # Create a new pose from the current position
            solver.add_pose_from_current(pose_name=pose_name)
            solver.setDrivenNode(drivenNode, [pose_name])
        self.refreshTables(solver)

    def approximateAndRound(self, values, tolerance=1e-10, decimalPlaces=3):
        """Approximate small values to zero and rounds the others.

        Args:
            values (list of float): The values to approximate and round.
            tolerance (float): The tolerance under which a value is considered zero.
            decimalPlaces (int): The number of decimal places to round to.

        Returns:
            list of float: The approximated and rounded values.
        """
        newValues = []
        for v in values:
            if abs(v) < tolerance:
                newValues.append(0)
            else:
                newValues.append(round(v, decimalPlaces))
        return newValues

    @toolsetwidget.ToolsetWidget.undoDecorator
    def mirrorSetup(self, selected=True):
        if self.is_pose_driver:
            if not self.pose_drivers: return
            topNode = 'Psd_System'
            if not cmds.objExists(topNode):
                cmds.createNode('transform', n=topNode)
            pose_drivers = self.pose_drivers
            if selected:
                pose_drivers = [self.selected_solver]
            for pose_driver in pose_drivers:
                joint = pose_driver.driver_joint
                parent_joint = pose_driver.parent_joint
                axis = pose_driver.axis
                side = pose_driver.side
                scale = pose_driver.scale
                mirror_joint = naming.convertRLName(joint)
                mirror_parent_joint = naming.convertRLName(parent_joint)
                mirror_side = naming.convertRLName(side)
                try:
                    psd = pose_driver_api.PoseDriverNode.create(mirror_joint, mirror_parent_joint, axis=axis, side=mirror_side, scale=scale)
                    cmds.parent(psd, topNode)
                except:
                    pass
        else:
            if not self.rbf_solvers:
                return
            rbfNodes = self.rbf_solvers
            if selected:
                rbfNodes = [self.selected_solver]

            for solver in rbfNodes:
                mirror_solver_name = naming.convertRLName(solver._node)
                if not cmds.objExists(mirror_solver_name):
                    mirrored_solver = solver.mirror(
                        mirror_rotation_axis='x',
                        mirror_translation_axis='x'
                    )
                    driverNode = mirrored_solver.drivers()[0]
                    poses = list(mirrored_solver.poses().keys())
                    selected_rbf_pose_grp = "{driverNode}_rbf_pose_grp".format(driverNode=driverNode)
                    for pose_name in poses:
                        self.createWeightBridge(selected_rbf_pose_grp, pose_name)

                    mirrored_solver.setDrivenNode(selected_rbf_pose_grp, poses)

        self.left_model.clear()
        self.load()

    @staticmethod
    def gatherMirroredInfo(rbfNodes):
        """gather all the info from the provided nodes and string replace
        side information for its mirror. Using mGear standard
        naming convections

        Args:
            rbfNodes (list): [of RBFNodes]

        Returns:
            dict: with all the info mirrored
        """
        mirrorWeightInfo = {}
        for rbfNode in rbfNodes:
            weightInfo = rbfNode.getNodeInfo()
            # connections -----------------------------------------------------
            mrConnections = []
            for pairs in weightInfo["connections"]:
                mrConnections.append(
                    [
                        naming.convertRLName(pairs[0]),
                        naming.convertRLName(pairs[1]),
                    ]
                )

            weightInfo["connections"] = mrConnections
            # weightInfo["drivenControlName"] = naming.convertRLName(
            #     weightInfo["drivenControlName"]
            # )
            weightInfo["drivenNode"] = [
                naming.convertRLName(n) for n in weightInfo["drivenNode"]
            ]
            weightInfo["drivenParentNode"] = [
                naming.convertRLName(n) for n in weightInfo["drivenParentNode"]
            ]
            weightInfo["driverControl"] = naming.convertRLName(
                weightInfo["driverControl"]
            )
            weightInfo["driverNode"] = [
                naming.convertRLName(n) for n in weightInfo["driverNode"]
            ]

            # setupName -------------------------------------------------------
            mrSetupName = naming.convertRLName(weightInfo["setupName"])
            if mrSetupName == weightInfo["setupName"]:
                mrSetupName = "{}{}".format(mrSetupName, '_mr')
            weightInfo["setupName"] = mrSetupName
            # transformNode ---------------------------------------------------
            tmp = weightInfo["transformNode"]["name"]
            mrTransformName = naming.convertRLName(tmp)
            weightInfo["transformNode"]["name"] = mrTransformName

            tmp = weightInfo["transformNode"]["parent"]
            if tmp is None:
                mrTransformPar = None
            else:
                mrTransformPar = naming.convertRLName(tmp)
            weightInfo["transformNode"]["parent"] = mrTransformPar
            # name ------------------------------------------------------------
            mirrorWeightInfo[naming.convertRLName(rbfNode.name)] = weightInfo
        return mirrorWeightInfo

    @toolsetwidget.ToolsetWidget.undoDecorator
    def exportNodes(self, allSetups=False):
        # TODO WHEN NEW RBF NODE TYPES ARE ADDED, THIS WILL NEED TO BE RETOOLED
        file_path = QtWidgets.QFileDialog.getSaveFileName(None, "Pose Wrangler Format", "", "*.json")[0]
        # If no path is specified, exit early
        if file_path == "":
            return

        # If all drivers is specified, get all solvers
        if allSetups:
            target_solvers = []
        else:
            # Get the currently selected solvers
            target_solvers = self.selected_solver
            # If no solvers found, skip export
            if not target_solvers:
                return

        # Export drivers
        self.serialize_to_file(file_path, target_solvers)

    def serialize_to_file(self, file_path, solvers=None, **kwargs):
        """
        Serialize the specified solvers to a file

        :param file_path: json file to serialize
        :type file_path: str
        :param solvers: list of api.RBFNode to serialize
        :type solvers: list
        """
        # Check that the directory exists before writing to it
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(file_path)
        # Dump the serialized data to the json file
        with open(file_path, 'w') as f:
            solvers = solvers or self.rbf_solvers
            data = self.serialize(solvers=solvers, **kwargs)
            print("Successfully serialized solvers: {solvers}".format(solvers=list(data.keys())))

            f.write(json.dumps(data, indent=4))
            print(
                "Successfully exported {num_solvers} solver(s) to {file_path}".format(
                    num_solvers=len(solvers),
                    file_path=file_path
                )
            )

    def serialize(self, solvers, **kwargs):
        """
        Serialize the specified solvers

        :param solvers: list of api.RBFNode to serialize
        :type solvers: list
        :return: serialized solver data
        :rtype: dict
        """
        # Always serialize with the latest solver
        serializer = serializers.SERIALIZERS[-1]
        return serializer.serialize(solvers=solvers, **kwargs)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def importNodes(self):
        """import a setup(s) from file select by user

        Returns:
            n/a: nada
        """
        # Get a json file path
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, "Pose Wrangler Format", "", "*.json")[0]
        # If no path is specified, exit early
        if file_path == "":
            return
        # Import the drivers
        self.deserialize_from_file(file_path, [])

    def deserialize_from_file(self, file_path, solver_names=None, **kwargs):
        """
        Deserialize solvers from a specific file.

        :param file_path: json file to load
        :type file_path: str
        """
        # Check the path exists
        if not os.path.exists(file_path):
            raise pose_exceptions.exceptions.PoseWranglerIOError(
                "Unable to deserialize from {file_path}, path does not exist".format(file_path=file_path)
            )
        if solver_names is None:
            solver_names = []
        # Load the json file and deserialize
        with open(file_path, 'r') as f:
            data = json.loads(f.read(), object_pairs_hook=collections.OrderedDict)

        self.deserialize(data, solver_names=solver_names, **kwargs)
        print(
            "Successfully loaded solver(s) from {file_path}".format(
                file_path=file_path
            )
        )

    def deserialize(self, data, solver_names=None, **kwargs):
        """
        Deserialize and load the solvers from the data specified

        :param data: serialized solver data
        :type data: dict
        :param solver_names: list of solver names to load from the data
        :type solver_names: list, optional
        """
        for serializer in serializers.SERIALIZERS:
            serializer.deserialize(data=data, solver_names=solver_names, **kwargs)
        self.left_model.clear()
        self.load()

    def updatePoseGrp(self):
        all_transforms = cmds.ls(type="transform")
        self.poseGrpNodes = []

        for obj in all_transforms:
            attrs = cmds.listAttr(obj)
            if attrs:
                matching_attrs = [attr for attr in attrs if re.search(r"pose_group", attr)]
                if matching_attrs:
                    self.poseGrpNodes.append(obj)

    def updateKeyFrame(self):
        if self._currentPose:
            self.details_list_model.clear()
            cns = sdk_io.getSdkConnections(self._currentPose, False)
            out_nodes = []
            if cns is not None:
                for animCurve, ref in cns.items():
                    out_node, out_attr = ref["output_connections"][0].split('.')[0], ref["output_connections"][0].split('.')[1]
                    out_nodes.append(out_node)
            out_nodes = list(set(out_nodes))
            for node in out_nodes:
                self.details_list_model.appendRow(QtGui.QStandardItem(node))

    @toolsetwidget.ToolsetWidget.undoDecorator
    def deleteKey(self):
        color = QtGui.QColor(44, 44, 44)
        selected = self.additional_info_list.selectedIndexes()
        if not selected or not self._currentPose: return

        node = self.details_list.selectedIndexes()[0].data()

        for i,index in enumerate(selected):
            item = self.additional_info_model.itemFromIndex(index)
            item.setBackground(color)
            attr = self.additional_info_list.selectedIndexes()[i].data()
            anim_dict = sdk_io.getSdkConnections(f"{node}.{attr}", True)
            for anim, ref in anim_dict.items():
                if ref['input_connections'][0] == self._currentPose:
                    cmds.delete(anim)
            # animCurves = sdk_io.getAnimCurve(self._currentPose, f"{node}.{attr}")
            # if animCurves:
            #     cmds.delete(animCurves)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def setKey(self):
        selected = self.additional_info_list.selectedIndexes()
        if not selected or not self._currentPose: return

        node = self.details_list.selectedIndexes()[0].data()

        for i,index in enumerate(selected):
            item = self.additional_info_model.itemFromIndex(index)
            item.setBackground(QtGui.QColor(65, 120, 180))
            attr = self.additional_info_list.selectedIndexes()[i].data()
            value = cmds.getAttr(f"{node}.{attr}")
            default_value = cmds.attributeQuery(attr, n=node, listDefault=True)[0]

            if self.is_pose_driver:
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose)
            else:
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose,
                                       dv=0, v=default_value)
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose,
                                       dv=1, v=value)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def setDefaultKey(self):
        if not self._currentPose: return

        node = self.details_list.selectedIndexes()[0].data()

        default_attrList = [
            "translateX", "translateY", "translateZ",
            "rotateX", "rotateY", "rotateZ",
            "scaleX", "scaleY", "scaleZ",
        ]
        for attr in default_attrList:
            value = cmds.getAttr(f"{node}.{attr}")
            default_value = cmds.attributeQuery(attr, n=node, listDefault=True)[0]

            if self.is_pose_driver:
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose)
            else:
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose,
                                       dv=0, v=default_value)
                cmds.setDrivenKeyframe(node, at=attr,
                                       cd=self._currentPose,
                                       dv=1, v=value)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def loadBsMesh(self):
        self.refreshBsList()

    def refreshBsList(self, selected_meshes=None):
        self.bs_model.clear()
        if not selected_meshes:
            selected_meshes = pose_util.get_selected_polygons()
            self.bs_mesh = selected_meshes[0]
            blendShapes = pose_util.get_selected_blend_shapes()
        else:
            blendShapes = [pose_util.get_bs(selected_meshes[0])]
        if not blendShapes: return
        self.bs_node = blendShapes[0]
        self.bs_targets = cmds.listAttr('{}.weight'.format(self.bs_node), multi=True)
        for t in self.bs_targets:
            item = QtGui.QStandardItem(t)
            item.setData(t, QtCore.Qt.UserRole)
            self.bs_model.appendRow(item)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def apply_edit(self):
        target_name = "newCorrective"
        if self.bs_list.selectedIndexes():
            target_name = self.bs_list.selectedIndexes()[0].data()

        attr = self._currentPose

        if pose_util.is_on_duplicate_edit():
            pose_util.finish_duplicate_edit()
            cmds.setAttr("{}.visibility".format(self.bs_mesh), 1)
        else:
            pose_util.duplicate_edit_selected_polygons2([target_name], attr)
            cmds.setAttr("{}.visibility".format(self.bs_mesh), 0)
        self.refreshBsList([self.bs_mesh])

    @toolsetwidget.ToolsetWidget.undoDecorator
    def deleteTarget(self):
        if not self.bs_list.selectedIndexes(): return
        for i,index in enumerate(self.bs_list.selectedIndexes()):
            target_name = self.bs_list.selectedIndexes()[i].data()
            pose_util.delete_target(self.bs_mesh, target_name)
        self.refreshBsList([self.bs_mesh])

    @toolsetwidget.ToolsetWidget.undoDecorator
    def renameTarget(self, item):
        if not self.bs_list.selectedIndexes(): return
        old_text = item.data(QtCore.Qt.UserRole)
        new_text = item.text()
        current_bs = pose_util.get_bs(self.bs_mesh)
        cmds.aliasAttr(new_text, current_bs + '.' + old_text)
        self.refreshBsList([self.bs_mesh])

    @toolsetwidget.ToolsetWidget.undoDecorator
    def mirror_by_targets(self):
        if not self.bs_list.selectedIndexes(): return
        targets = []
        for i,index in enumerate(self.bs_list.selectedIndexes()):
            target_name = self.bs_list.selectedIndexes()[i].data()
            targets.append(target_name)
        pose_util.mirror_by_targets(targets, [self.bs_mesh])
        self.refreshBsList([self.bs_mesh])

    @property
    def rbf_solvers(self):
        """
        :return: list of rbf solvers in the scene
        :rtype: list
        """
        return ue_rbf_api.RBFNode.find_all()

    @property
    def pose_drivers(self):
        """
        :return: list of rbf solvers in the scene
        :rtype: list
        """
        return pose_driver_api.PoseDriverNode.find_all()

    @property
    def current_pose(self):
        return self._currentPose

    @current_pose.setter
    def current_pose(self, pose_name):
        solver = self.selected_solver
        if self.is_pose_driver:
            self._currentPose = "{driver}.{pose_name}".format(driver=solver.cmd_node, pose_name=pose_name)
        else:
            driver = solver.drivers()[0]
            self._currentPose = "{driver}_rbf_pose_grp.{pose_name}".format(driver=driver, pose_name=pose_name)

    @property
    def selected_solver(self):
        current_solver = None
        if not self.interpolators_list.selectedIndexes(): return current_solver
        selected_item = self.interpolators_list.selectedIndexes()[0].data(QtCore.Qt.DisplayRole)
        if self.is_pose_driver:
            for solver in self.pose_drivers:
                if solver.cmd_node == selected_item:
                    current_solver = solver
        else:
            for solver in self.rbf_solvers:
                if solver._node == selected_item:
                    current_solver = solver
        return current_solver

    @property
    def current_solver(self):
        """
        :return: reference to the current solver
        :rtype: api.RBFNode or None
        """
        return self._current_solver

    @current_solver.setter
    def current_solver(self, solver):
        # If the specified solver is not an RBFNode class, raise exception
        if not isinstance(solver, ue_rbf_api.RBFNode):
            raise pose_exceptions.InvalidSolverError(
                "Solver is not a valid {node_type} node".format(node_type=ue_rbf_api.RBFNode)
            )
        # Set the current solver
        self._current_solver = solver

    def load(self):
        self.left_model.clear()
        if self.is_pose_driver:
            for driver in self.pose_drivers:
                self.add_solver(driver.cmd_node, type='pose_driver')
        else:
            for solver in self.rbf_solvers:
                self.add_solver(solver)

    def add_solver(self, solver, type='solver'):
        # Create a new widget item with the solver name
        item = QtGui.QStandardItem(iconlib.Icon.icon("pi-head", size=20), str(solver))
        # Add the solver and the edit status as custom data on the item
        item.setData({type: solver}, QtCore.Qt.UserRole)
        # Add the item to the solver list
        self.left_model.appendRow(item)

    def create_pose_driver_ui(self, joint, parent_joint):
        if cmds.window(self.pose_driver_ui, exists=True):
            cmds.deleteUI(self.pose_driver_ui)

        window = cmds.window(
            self.pose_driver_ui,
            title="pose_driver_win",
            widthHeight=(150, 60),
            sizeable=True
        )

        main_layout = cmds.rowLayout(numberOfColumns=10,
                                     adjustableColumn=10,
                                     columnAlign=((1, 'left'), (2, 'center')))

        cmds.radioCollection()
        self.pose_left_radio = cmds.radioButton(label='L', select=True)
        self.pose_right_radio = cmds.radioButton(label='R')
        self.pose_center_radio = cmds.radioButton(label='M')
        cmds.separator(width=5)
        self.axis_combo = cmds.optionMenu(label="Axis")
        cmds.menuItem(label="+x")
        cmds.menuItem(label="+y")
        cmds.menuItem(label="+z")
        cmds.menuItem(label="-x")
        cmds.menuItem(label="-y")
        cmds.menuItem(label="-z")
        cmds.separator(width=5)
        cmds.text("Scale: ")
        self.scale_field = cmds.floatField(minValue=0.01, maxValue=1.00, value=0.05, precision=2, step=0.01)
        cmds.separator(width=5)
        self.pose_driver_create_btn = cmds.button("Create", c=partial(self.create_psd, joint, parent_joint))
        cmds.showWindow(window)

    def create_psd(self, joint, parent_joint, *args):
        pass
        # topNode = 'Psd_System'
        # if not cmds.objExists(topNode):
        #     cmds.createNode('transform', n=topNode)
        #
        # axis = cmds.optionMenu(self.axis_combo, query=True, value=True)
        # psdScale = float(cmds.floatField(self.scale_field, query=True, value=True))
        # side = 'L'
        #
        # if cmds.radioButton(self.pose_left_radio, query=True, select=True):
        #     side = 'L'
        # if cmds.radioButton(self.pose_right_radio, query=True, select=True):
        #     side = 'R'
        # if cmds.radioButton(self.pose_center_radio, query=True, select=True):
        #     side = 'M'
        # if cmds.objExists(parent_joint) and cmds.objExists(joint) and not cmds.objExists(joint + '_psd_parent_handle'):
        #     psd = pose_driver_api.PoseDriverNode.create(joint, parent_joint, axis=axis, side=side, scale=psdScale)
        #     cmds.parent(psd._node, topNode)
        #
        # self.load()


class PoseEditerUI(elements.CgRigWindow):

    def __init__(self, title="Pose Editer",
                 width=600,
                 height=535, parent=None, **kwargs):

        super(PoseEditerUI, self).__init__(title=title, name="PoseEditerWindow",
                                           width=width, height=height, parent=parent,
                                           saveWindowPref=False, **kwargs)

        self.mainLayout = elements.hBoxLayout()
        self.pose_widget = PoseEditorWindow()
        self.mainLayout.addWidget(self.pose_widget)
        self.setMainLayout(self.mainLayout)




























