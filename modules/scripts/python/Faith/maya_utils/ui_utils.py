# -*- coding: utf-8 -*-
"""mgear qt functions"""
import os, traceback, shiboken2
import maya.OpenMayaUI as omui, pymel.core as pm, maya.cmds as cmds, maya.mel as mel
from collections import OrderedDict
from Faith.vendor.Qt import QtCore, QtWidgets, QtGui
from Faith.vendor.Qt.QtCompat import wrapInstance
from .python_utils import PY2

if not PY2:
    long = int

icon_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/icons"


def marginsDpiScale(left, top, right, bottom):
    """Convenience function to return contents margins

    :param left:
    :param top:
    :param right:
    :param bottom:
    :return:
    """

    if type(left) == tuple:
        margins = left
        return (
            dpiScale(margins[0]),
            dpiScale(margins[1]),
            dpiScale(margins[2]),
            dpiScale(margins[3]),
        )
    return (dpiScale(left), dpiScale(top), dpiScale(right), dpiScale(bottom))


def setShadowEffectEnabled(widget, enabled):
    """Set shadow effect for a widget

    :param widget:
    :type widget: QtWidgets.QWidget
    :param enabled:
    """
    if enabled:
        shadowEffect = widget.property("shadowEffect")
        if shadowEffect is None:
            shadowEffect = QtWidgets.QGraphicsDropShadowEffect(widget)
            widget.setProperty("shadowEffect", shadowEffect)
            shadowEffect.setBlurRadius(dpiScale(15))
            shadowEffect.setColor(QtGui.QColor(0, 0, 0, 150))
            shadowEffect.setOffset(dpiScale(0))
        widget.setGraphicsEffect(shadowEffect)
    else:
        widget.setGraphicsEffect(None)


def currentScreen():
    """Gets current screen.

    :rtype: :class:`QRect`
    """
    return QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())



def dpiMult():
    # todo: Replace with a Host agnostic version
    #  Maya has a different way of getting DPI compared to QT where it doesn't modify QT

    try:
        from maya import cmds

        dpi = cmds.mayaDpiSetting(query=True, realScaleValue=True)
    # AttributeError is raised on OSX because mayaDPISetting doesn't exist, ImportError for non maya
    except (ImportError, AttributeError):
        screen = currentScreen()
        logicalY = 96
        if screen is not None:
            logicalY = screen.logicalDotsPerInch()
        dpi = max(1, float(logicalY) / float(96))
    return dpi


def dpiScale(value):
    """Resize by value based on current DPI

    :param value: the default 2k size in pixels
    :type value: int
    :return value: the size in pixels now dpi monitor ready (4k 2k etc)
    :rtype value: int
    """
    mult = dpiMult()
    return value * mult


def mayaWindow():
    """
    :return: instance, the mainWindow ptr as a QMainWindow widget.
    :rtype: :class:`QtWidgets.QMainWindow`
    """
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtWidgets.QMainWindow)


def maya_main_window():
    """Get Maya's main window

    Returns:
        QMainWindow: main window.

    """

    main_window_ptr = omui.MQtUtil.mainWindow()
    if PY2:
        return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def showDialog(dialog, dInst=True, dockable=False, *args):
    """
    Show the defined dialog window

    Attributes:
        dialog (QDialog): The window to show.

    """
    if dInst:
        try:
            for c in maya_main_window().children():
                if isinstance(c, dialog):
                    c.deleteLater()
        except Exception:
            pass

    # Create minimal dialog object
    windw = dialog()
    # dayu_theme.apply(windw)
    # ensure clean workspace name
    if hasattr(windw, "uiName") and dockable:
        control = windw.uiName + "WorkspaceControl"
        if pm.workspaceControl(control, q=True, exists=True):
            pm.workspaceControl(control, e=True, close=True)
            pm.deleteUI(control, control=True)
    desktop = QtWidgets.QApplication.desktop()
    screen = desktop.screen()
    screen_center = screen.rect().center()
    windw_center = windw.rect().center()
    windw.move(screen_center - windw_center)

    # Delete the UI if errors occur to avoid causing winEvent
    # and event errors (in Maya 2014)
    try:
        if dockable:
            windw.show(dockable=True)
        else:
            windw.show()
        return windw
    except Exception:
        windw.deleteLater()
        traceback.print_exc()


def convertMayaUIToQt(uiName):
    """

    :param uiName:
    :return:
    """
    getcontrol = omui.MQtUtil.findControl(uiName)
    if PY2:
        getobjPyside = shiboken2.wrapInstance(long(getcontrol), QtWidgets.QWidget)
    else:
        getobjPyside = shiboken2.wrapInstance(int(getcontrol), QtWidgets.QWidget)
    return getobjPyside


def addShelfButton(labelName, command, imagePath, annotation):
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    cmds.shelfButton(parent=currentShelf, c=command, imageOverlayLabel=labelName, annotation=annotation, image=imagePath)


class DragQListView(QtWidgets.QListView):

    def __init__(self, parent):
        super(DragQListView, self).__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setDropIndicatorShown(True)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.exp = 3
        self.ignore_self = True

    def mouseMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        mimeData.setText("%d,%d" % (event.x(), event.y()))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())
        dropAction = drag.start(QtCore.Qt.MoveAction)
        if not dropAction == QtCore.Qt.MoveAction:
            pos = QtGui.QCursor.pos()
            widget = QtWidgets.QApplication.widgetAt(pos)
            if self.ignore_self and (
                    widget is self or widget.objectName() == "qt_scrollarea_viewport"):
                return

            relpos = widget.mapFromGlobal(pos)
            invY = widget.frameSize().height() - relpos.y()
            # sel = selectFromScreenApi(relpos.x() - self.exp,
            #                           invY - self.exp,
            #                           relpos.x() + self.exp,
            #                           invY + self.exp)
            #
            # self.doAction(sel)

    def setAction(self, action):
        self.theAction = action

    def doAction(self, sel):
        self.theAction(sel)


class CollapsibleHeader(QtWidgets.QWidget):
    COLLAPSED_PIXMAP = QtGui.QPixmap(":teRightArrow.png")
    EXPANDED_PIXMAP = QtGui.QPixmap(":teDownArrow.png")

    clicked = QtCore.Signal()

    def __init__(self, text, parent=None):
        super(CollapsibleHeader, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.set_background_color(None)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedWidth(self.COLLAPSED_PIXMAP.width())

        self.text_label = QtWidgets.QLabel()
        self.text_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.text_label)

        self.set_text(text)
        self.set_expanded(False)

    def set_text(self, text):
        self.text_label.setText(u"<b>{0}</b>".format(text))

    def set_background_color(self, color):
        if not color:
            color = QtWidgets.QPushButton().palette().color(QtGui.QPalette.Button)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)

    def is_expanded(self):
        return self._expanded

    def set_expanded(self, expanded):
        self._expanded = expanded

        if (self._expanded):
            self.icon_label.setPixmap(self.EXPANDED_PIXMAP)
        else:
            self.icon_label.setPixmap(self.COLLAPSED_PIXMAP)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # pylint: disable=E1101


class CollapsibleWidget(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(CollapsibleWidget, self).__init__(parent)

        self.header_wdg = CollapsibleHeader(text)
        self.header_wdg.clicked.connect(self.on_header_clicked)  # pylint: disable=E1101

        self.body_wdg = QtWidgets.QWidget()

        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(3)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.header_wdg)
        self.main_layout.addWidget(self.body_wdg)

        self.set_expanded(False)

    def add_widget(self, widget):
        self.body_layout.addWidget(widget)

    def add_layout(self, layout):
        self.body_layout.addLayout(layout)

    def set_expanded(self, expanded):
        self.header_wdg.set_expanded(expanded)
        self.body_wdg.setVisible(expanded)

    def set_header_background_color(self, color):
        self.header_wdg.set_background_color(color)

    def on_header_clicked(self):
        self.set_expanded(not self.header_wdg.is_expanded())


class RampPoint(object):
    class InterpType(object):
        None_ = 0
        Linear = 1
        Smooth = 2
        Spline = 3

        @classmethod
        def asDict(cls):
            return OrderedDict((("None", cls.None_),
                                ("Linear", cls.Linear),
                                ("Smooth", cls.Smooth),
                                ("Spline", cls.Spline)))

    def __init__(self, val, pos, interp):
        self.pos = float(pos)
        self.value = float(val)
        self.interp = int(interp)

    def asString(self):
        return ",".join([str(each) for each in (self.value, self.pos, self.interp)])


def createCollapsibleWidget(addWidget=None, expanded=False, text="", parent=None):
    """

    :param expanded:
    :return:
    """
    collapsible_wdg = CollapsibleWidget(text, parent)
    collapsible_wdg.set_expanded(expanded)
    if not addWidget:
        return collapsible_wdg
    collapsible_wdg.add_widget(addWidget)
    return collapsible_wdg


def createMayaCurveEditer(interType="Smooth", getValue=None):
    """

    :param interType:
    :return:
    """
    if cmds.window('MyCrvEditorWindow', ex=True):
        cmds.deleteUI('MyCrvEditor')
        cmds.deleteUI('MyCrvEditorWindow')
    cmds.window('MyCrvEditorWindow')
    cmds.columnLayout()
    cmds.gradientControlNoAttr('MyCrvEditor')

    cmds.optionVar(rm='falloffCurveOptionVar')
    cmds.optionVar(stringValueAppend=['falloffCurveOptionVar', '0,1,2'])
    cmds.optionVar(stringValueAppend=['falloffCurveOptionVar', '1,0,2'])
    cmds.gradientControlNoAttr('MyCrvEditor', e=True, optionVar='falloffCurveOptionVar')

    rampPoints, strVals = createCrvEditerInterType(interType=interType)

    cmds.gradientControlNoAttr('MyCrvEditor', e=True, asString=strVals)

    if getValue:
        value = cmds.gradientControlNoAttr('MyCrvEditor', q=True, valueAtPoint=getValue)
        cmds.deleteUI('MyCrvEditor')
        return value

    getobjPyside = convertMayaUIToQt('MyCrvEditor')
    return getobjPyside


def createCrvEditerInterType(interType="Smooth"):
    """

    :param interType:
    :return:
    """
    if interType == "None":
        rampPoints = (RampPoint(0, 0, RampPoint.InterpType.None_), RampPoint(1, 1, RampPoint.InterpType.None_))
    if interType == "Linear":
        rampPoints = (RampPoint(0, 0, RampPoint.InterpType.Linear), RampPoint(1, 1, RampPoint.InterpType.Linear))
    if interType == "Smooth":
        rampPoints = (RampPoint(0, 0, RampPoint.InterpType.Smooth), RampPoint(1, 1, RampPoint.InterpType.Smooth))
    if interType == "Spline":
        rampPoints = (RampPoint(0, 0, RampPoint.InterpType.Spline), RampPoint(1, 1, RampPoint.InterpType.Spline))

    strVals = ",".join([each.asString() for each in rampPoints])
    return [rampPoints, strVals]


def increase_brightness(pixmap, factor):
    image = pixmap.toImage()

    for x in range(image.width()):
        for y in range(image.height()):
            color = QtGui.QColor(image.pixel(x, y))
            h, s, v, a = color.getHsv()
            v = min(255, v + factor)  # 增加亮度，确保不超过255
            new_color = QtGui.QColor.fromHsv(h, s, v, a)
            image.setPixel(x, y, new_color.rgba())

    return QtGui.QPixmap.fromImage(image)


class IconLabel(QtWidgets.QLabel):
    mouseClicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.icon1 = None
        self.icon2 = None

    def setupIcon(self, icon1, icon2):
        self.icon1 = icon1
        self.icon2 = icon2
        self.setPixmap(icon2)

    def enterEvent(self, e):
        self.setPixmap(self.icon1)

    def leaveEvent(self, e):
        self.setPixmap(self.icon2)

    def mousePressEvent(self, e):
        sigContent = self.objectName()
        self.mouseClicked.emit(sigContent)


class MyLabel(QtWidgets.QLabel):
    mylabelSig = QtCore.Signal(str)
    mylabelDoubleClickSig = QtCore.Signal(str)

    def __int__(self):
        super(MyLabel, self).__init__()

    def mouseDoubleClickEvent(self, e):  # 双击
        sigContent = self.objectName()
        self.mylabelDoubleClickSig.emit(sigContent)

    def mousePressEvent(self, e):  # 单击
        sigContent = self.objectName()
        self.mylabelSig.emit(sigContent)

    def leaveEvent(self, e):  # 鼠标离开label
        print("leaveEvent")

    def enterEvent(self, e):  # 鼠标移入label
        print("enterEvent")


qss = """
QScrollArea{
border-radius: 8px;
border:1px;
}

QPushButton
{
    color: white;
    background-color: rgb(85, 120, 210);
    border-width: 1px;
    border-radius:10px;
    border-color: #1e1e1e;
    border-style: solid;
    padding: 5px;
    font-size: 12px;
    font: "Consolas";
}

QPushButton:hover
{
    background-color: #505050;
    border: 1px solid #ff8d1c;
}

QPushButton:disabled {
  background-color: #303030;
  border: 1px solid #404040;
  color: #505050;
  padding: 5px;
  font-size: 12px;
}

QPushButton:pressed {
  background-color: #ff8d1c;
  border: 1px solid #ff8d1c;
}

QPushButton[override = "0"]{
    border-color: #1e1e1e;
}

QPushButton[override = "1"]{
    border-color: green;
}

QPushButton[menuButton=true] {
  min-width: 120;
  min-height: 45;
}

"""






















