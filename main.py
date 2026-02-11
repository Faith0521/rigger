from Qt import QtWidgets, QtCore, QtGui

class ShapeEditor(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ShapeEditor, self).__init__(parent)
        self.setWindowTitle("Shape Editor")
        self.setMinimumSize(800, 540)
        self._setup_ui()

    def _setup_ui(self):
        # 主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. 菜单栏
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("QMenuBar { background-color: #3c3c3c; color: #dcdcdc; }")
        for menu_name in ["File", "Edit", "Create", "Shapes", "Options", "Help"]:
            menu_bar.addMenu(menu_name)

        # 2. 工具栏
        tool_bar = QtWidgets.QToolBar()
        tool_bar.setStyleSheet("QToolBar { background-color: #4a4a4a; }")
        self.addToolBar(tool_bar)

        # 工具栏控件
        tool_bar.addAction("Create Blend Shape")
        tool_bar.addSeparator()
        tool_bar.addAction("Add Target")

        search_widget = QtWidgets.QWidget()
        search_layout = QtWidgets.QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_field = QtWidgets.QLineEdit()
        search_field.setPlaceholderText("Search...")
        search_field.setFixedWidth(150)
        search_layout.addWidget(search_field)
        search_layout.addWidget(QtWidgets.QPushButton("+"))
        search_layout.addWidget(QtWidgets.QPushButton("⊕"))
        tool_bar.addWidget(search_widget)

        # 3. 树形表格区域
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setStyleSheet("""
            QTreeWidget { background-color: #2d2d2d; color: #dcdcdc; }
            QHeaderView::section { background-color: #3c3c3c; color: #dcdcdc; border: 1px solid #555; }
            QTreeWidget::item:selected { background-color: #3a5169; }
        """)
        self.tree_widget.setColumnCount(4)
        self.tree_widget.setHeaderLabels(["Name", "Weight/Drivers", "", "Edit"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        main_layout.addWidget(self.tree_widget)

        # 构建树形结构
        root_item = QtWidgets.QTreeWidgetItem(self.tree_widget, ["blendShape1"])
        root_item.setCheckState(0, QtCore.Qt.Checked)
        root_item.setText(1, "1.000")
        self._add_slider_to_item(root_item, 2)

        # 添加子项
        for name in ["pTorus2", "pTorus3", "pTorus4", "pTorus5"]:
            child_item = QtWidgets.QTreeWidgetItem(root_item, [name])
            child_item.setCheckState(0, QtCore.Qt.Checked)
            child_item.setText(1, "0.000")
            self._add_slider_to_item(child_item, 2)
            self._add_edit_button_to_item(child_item, 3)
            # 选中效果
            if name == "pTorus5":
                child_item.setSelected(True)

    def _add_slider_to_item(self, item, column):
        """为表格项添加滑块控件"""
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setStyleSheet("QSlider::groove:horizontal { background-color: #555; } QSlider::handle:horizontal { background-color: #888; }")
        slider.setRange(0, 1000)
        slider.setValue(int(float(item.text(1)) * 1000))
        self.tree_widget.setItemWidget(item, column, slider)

    def _add_edit_button_to_item(self, item, column):
        """为表格项添加Edit按钮"""
        btn = QtWidgets.QPushButton("Edit")
        btn.setStyleSheet("QPushButton { background-color: #4a4a4a; color: #dcdcdc; border: none; padding: 2px 8px; }")
        self.tree_widget.setItemWidget(item, column, btn)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ShapeEditor()
    window.show()
    sys.exit(app.exec_())