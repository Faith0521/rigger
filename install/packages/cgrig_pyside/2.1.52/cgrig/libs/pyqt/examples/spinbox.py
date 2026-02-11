# -*- coding: utf-8 -*-
from cgrigvendor.Qt import QtWidgets
from cgrig.libs.pyqt.extended import spinbox


def DragSpinBoxExample():
    wid = QtWidgets.QWidget()

    horizontalLayout = QtWidgets.QHBoxLayout(wid)
    spinBox = spinbox.DragSpinBox(wid)
    horizontalLayout.addWidget(spinBox)
    doubleSpinBox = spinbox.DragDoubleSpinBox(wid)
    horizontalLayout.addWidget(doubleSpinBox)
    wid.show()
    return wid
