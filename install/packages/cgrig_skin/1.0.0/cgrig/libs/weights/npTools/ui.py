# coding:utf-8

from Faith.vendor.Qt.QtGui import *
from Faith.vendor.Qt.QtCore import *
from Faith.vendor.Qt.QtWidgets import *
# try:
#     from PySide.QtGui import *
#     from PySide.QtCore import *
# except ImportError:
#     from PySide2.QtGui import *
#     from PySide2.QtCore import *
#     from PySide2.QtWidgets import *
from . import tools


def get_app():
    top = QApplication.activeWindow()
    if top is None:
        return
    while True:
        parent = top.parent()
        if parent is None:
            return top
        top = parent


def q_add(layout, *elements):
    for elem in elements:
        if isinstance(elem, QLayout):
            layout.addLayout(elem)
        elif isinstance(elem, QWidget):
            layout.addWidget(elem)
    return layout


def q_button(text, action):
    but = QPushButton(text)
    but.clicked.connect(action)
    return but


qss = u"""
QWidget{
    font-size: 16px;
    font-family: 楷体;
}
"""


class FacePointWeight(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setStyleSheet(qss)
        self.max_inf = QSpinBox()
        self.max_inf.setRange(1, 100)
        self.max_inf.setValue(4)
        self.setWindowTitle(u"表面点")
        self.setLayout(q_add(
            QVBoxLayout(),
            q_add(
                QHBoxLayout(),
                QLabel(u"最大影响数："),
                self.max_inf,
            ),
            q_button(u"计算权重", self.apply)
        ))

    def apply(self):
        tools.tool_face_point_weight(max_influence=self.max_inf.value())

