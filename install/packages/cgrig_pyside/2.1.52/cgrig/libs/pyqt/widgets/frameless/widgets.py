# -*- coding: utf-8 -*-
import webbrowser
from cgrig.libs.utils import output
from cgrigvendor.Qt import QtCore, QtWidgets, QtGui
from cgrig.libs.pyqt import utils, uiconstants
from cgrig.libs.pyqt.extended.clippedlabel import ClippedLabel
from cgrig.libs.pyqt.widgets import layouts, buttons, overlay
from cgrig.libs.pyqt.widgets.frameless.containerwidgets import SpawnerIcon
from cgrig.preferences.interfaces import coreinterfaces
from cgrig.core.util import zlogging
from cgrig.libs.pyqt.widgets import elements
from cgrigvendor.Qt.QtCompat import wrapInstance
from maya.OpenMayaUI import MQtUtil

maya_main_widget = wrapInstance(int(MQtUtil.mainWindow()), QtWidgets.QWidget)

logger = zlogging.getLogger(__name__)
MODIFIER = QtCore.Qt.AltModifier


class ResizeDirection:
    """Flag attributes to tell what position the resizer is"""

    Left = 1
    Top = 2
    Right = 4
    Bottom = 8


class TitleBar(QtWidgets.QFrame):
    doubleClicked = QtCore.Signal()
    moving = QtCore.Signal(object, object)

    class TitleStyle:
        Default = "DEFAULT"
        Thin = "THIN"
        VerticalThin = "VERTICAL_THIN"

    def __init__(
            self,
            parent=None,
            showTitle=True,
            alwaysShowAll=False,
            titleBarHeight=40,
            showDockTabs=True,
            style=TitleStyle.Default,
    ):
        """Title bar of the frameless window.

        Click drag this widget to move the window widget

        :param parent:
        :type parent: cgrig.libs.pyqt.widgets.window.CgRigWindow
        """
        super(TitleBar, self).__init__(parent=parent)

        self.titleBarHeight = titleBarHeight
        self.pressedAt = None
        self.leftContents = QtWidgets.QFrame(self)
        self.rightContents = QtWidgets.QWidget(self)

        self._mainLayout = None
        self._mainRightLayout = None
        self.contentsLayout = None
        self.cornerContentsLayout = None
        self.titleLayout = None
        self.windowButtonsLayout = None
        self._splitLayout = None
        self._initLayouts()
        self._titleStyle = style
        self._previousTitleStyle = style

        self.cgrigWindow = parent
        self.mousePos = None  # type: QtCore.QPoint
        self.widgetMousePos = None  # type: QtCore.QPoint
        self.themePref = coreinterfaces.coreInterface()

        # Title bar buttons
        self.logoButton = SpawnerIcon(
            cgrigWindow=parent, showDockTabs=showDockTabs, parent=self
        )

        self.toggle = True

        self.iconSize = 13  # note: iconSize gets dpiScaled in internally
        self.closeButton = buttons.ExtendedButton(parent=self, themeUpdates=False)
        self.minimizeButton = buttons.ExtendedButton(parent=self, themeUpdates=False)
        self.maxButton = buttons.ExtendedButton(parent=self, themeUpdates=False)
        self.helpButton = buttons.ExtendedButton(parent=self, themeUpdates=False)
        self.titleLabel = TitleLabel(parent=self, alwaysShowAll=alwaysShowAll)

        self._moveEnabled = True

        if not showTitle:
            self.titleLabel.hide()

        self.initUi()
        self._connections()

    def setDirection(self, direction):
        self._mainLayout.setDirection(direction)
        self._mainRightLayout.setDirection(direction)
        self.contentsLayout.setDirection(direction)
        self.cornerContentsLayout.setDirection(direction)
        self.titleLayout.setDirection(direction)
        self.windowButtonsLayout.setDirection(direction)
        self._splitLayout.setDirection(direction)

    def setDebugColors(self, debug):
        if debug:
            self.leftContents.setStyleSheet("background-color: green")
            self.titleLabel.setStyleSheet("background-color: red")
            self.rightContents.setStyleSheet("background-color: blue")
        else:
            self.leftContents.setStyleSheet("")
            self.titleLabel.setStyleSheet("")
            self.rightContents.setStyleSheet("")

    def _initLayouts(self):
        self._mainLayout = layouts.hBoxLayout(self)
        self._mainRightLayout = layouts.hBoxLayout()
        self.contentsLayout = layouts.hBoxLayout()
        self.cornerContentsLayout = layouts.hBoxLayout()
        self.titleLayout = layouts.hBoxLayout()
        self.windowButtonsLayout = layouts.hBoxLayout()
        self._splitLayout = layouts.hBoxLayout()

    def initUi(self):
        """Init UI"""

        self.setFixedHeight(utils.dpiScale(self.titleBarHeight))

        col = self.themePref.FRAMELESS_TITLELABEL_COLOR
        self.closeButton.setIconByName(
            "xMark", colors=col, size=self.iconSize, colorOffset=80
        )
        self.minimizeButton.setIconByName(
            "minus", colors=col, size=self.iconSize, colorOffset=80
        )
        self.maxButton.setIconByName(
            "checkbox", colors=col, size=self.iconSize, colorOffset=80
        )
        toolTip = "Open the help URL for this window."
        if self.cgrigWindow.helpUrl:
            toolTip = "{} \n{}  ".format(toolTip, self.cgrigWindow.helpUrl)
        self.helpButton.setIconByName(
            "help", colors=col, size=self.iconSize, colorOffset=80
        )
        self.helpButton.setToolTip(toolTip)

        # _mainLayout: The whole titlebar main layout

        # Button Settings
        btns = [self.helpButton, self.closeButton, self.minimizeButton, self.maxButton]
        for b in btns:
            b.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            b.setDoubleClickEnabled(False)

        """ The widget layout is laid out into the following:

        _mainLayout
            logoButton
            _mainRightLayout
                _splitLayout
                    leftContents
                    titleLayoutWgt -> titleLayout
                    rightContents   

                windowButtonsLayout
                    helpButton
                    minimizeButton
                    maxButton
                    closeButton
        """

        # Layout setup
        self._mainRightLayout.setContentsMargins(*utils.marginsDpiScale(0, 5, 6, 0))
        self.contentsLayout.setContentsMargins(0, 0, 0, 0)
        self.cornerContentsLayout.setContentsMargins(*utils.marginsDpiScale(0, 0, 0, 0))
        self.rightContents.setLayout(self.cornerContentsLayout)

        # Window buttons (Min, Max, Close button)
        self.windowButtonsLayout.setContentsMargins(*utils.marginsDpiScale(0, 0, 0, 0))
        self.windowButtonsLayout.addWidget(self.helpButton)
        self.windowButtonsLayout.addWidget(self.minimizeButton)
        self.windowButtonsLayout.addWidget(self.maxButton)
        self.windowButtonsLayout.addWidget(self.closeButton)

        # Split Layout
        self._splitLayout.addWidget(self.leftContents)
        self._splitLayout.addLayout(self.titleLayout, 1)
        self._splitLayout.addWidget(self.rightContents)

        # Title Layout
        self.leftContents.setLayout(self.contentsLayout)
        self.contentsLayout.setSpacing(0)
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.setSpacing(0)
        self.titleLayout.setContentsMargins(*utils.marginsDpiScale(0, 8, 0, 7))
        self.titleLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.titleLabel.setMinimumWidth(1)

        # The main title layout (Logo | Main Right Layout)
        self._mainLayout.setContentsMargins(*utils.marginsDpiScale(4, 0, 0, 0))
        self._mainLayout.setSpacing(0)
        self.spacingItem = QtWidgets.QSpacerItem(8, 8)
        self.spacingItem2 = QtWidgets.QSpacerItem(6, 6)

        self._mainLayout.addWidget(self.logoButton)
        self._mainLayout.addSpacerItem(self.spacingItem2)
        self._mainLayout.addLayout(self._mainRightLayout)
        self._mainLayout.setAlignment(self.logoButton, QtCore.Qt.AlignLeft)

        # The Main right layout (Title, Window buttons)
        self._mainRightLayout.addLayout(self._splitLayout)
        # self._mainRightLayout.addWidget(self.rightContents)
        self._mainRightLayout.addLayout(self.windowButtonsLayout)
        self._mainRightLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.windowButtonsLayout.setAlignment(QtCore.Qt.AlignVCenter)

        # Left right margins have to be zero otherwise the title toolbar will flicker (eg toolsets)
        self._mainRightLayout.setStretch(0, 1)
        QtCore.QTimer.singleShot(0, self.refreshTitleBar)
        self.setTitleSpacing(False)

        if not self.cgrigWindow.helpUrl:
            self.helpButton.hide()

    def setTitleSpacing(self, spacing):
        """

        :param spacing:
        :return:
        """
        if spacing:
            self.spacingItem2.changeSize(6, 6)
        else:
            self.spacingItem2.changeSize(0, 0)
            self._splitLayout.setSpacing(0)

    def setTitleAlign(self, align):
        """Set Title Align

        :param align:
        :type align:
        """
        if align == QtCore.Qt.AlignCenter:
            self._splitLayout.setStretch(1, 0)
        else:
            self._splitLayout.setStretch(1, 1)

    def setDockable(self, dockable):
        if dockable:
            pass

    def setMoveEnabled(self, enabled):
        """Window moving enabled

        :param enabled:
        :type enabled:
        :return:
        :rtype:
        """
        self._moveEnabled = enabled

    def setTitleStyle(self, style):
        """Set the title style

        :param style:
        :type style: TitleStyle
        :return: TitleStyle.Default or TitleStyle.Thin
        :rtype:
        """
        self._previousTitleStyle = self._titleStyle
        self._titleStyle = style
        if style == self.TitleStyle.Default:
            self.setDirection(QtWidgets.QBoxLayout.LeftToRight)
            utils.setStylesheetObjectName(self.titleLabel, "")
            self.setFixedHeight(utils.dpiScale(self.titleBarHeight))
            self.setMaximumWidth(uiconstants.QWIDGETSIZE_MAX)  # unlock the width
            self.titleLayout.setContentsMargins(*utils.marginsDpiScale(0, 5, 0, 7))
            self._mainRightLayout.setContentsMargins(*utils.marginsDpiScale(0, 5, 6, 0))
            self.logoButton.setIconSize(QtCore.QSize(24, 24))
            self.logoButton.setFixedSize(QtCore.QSize(30, 24))
            self.minimizeButton.setFixedSize(QtCore.QSize(28, 24))
            self.maxButton.setFixedSize(QtCore.QSize(28, 24))
            self.maxButton.setIconSize(QtCore.QSize(24, 24))
            self.closeButton.setFixedSize(QtCore.QSize(28, 24))
            self.closeButton.setIconSize(QtCore.QSize(16, 16))
            if self.cgrigWindow.helpUrl:
                self.helpButton.show()

            self.windowButtonsLayout.setSpacing(utils.dpiScale(6))
            self._mainRightLayout.setContentsMargins(*utils.marginsDpiScale(0, 5, 6, 0))
            self.contentsLayout.setContentsMargins(0, 0, 0, 0)
            self.cornerContentsLayout.setContentsMargins(
                *utils.marginsDpiScale(0, 0, 0, 0)
            )
            self.windowButtonsLayout.setContentsMargins(
                *utils.marginsDpiScale(0, 0, 0, 0)
            )
            self.titleLayout.setContentsMargins(*utils.marginsDpiScale(0, 8, 0, 7))
            self._mainLayout.setContentsMargins(*utils.marginsDpiScale(4, 0, 0, 0))

        elif style == self.TitleStyle.Thin:
            self.setDirection(QtWidgets.QBoxLayout.LeftToRight)
            self.setMaximumWidth(uiconstants.QWIDGETSIZE_MAX)  # unlock the width
            self.logoButton.setIconSize(QtCore.QSize(12, 12))
            self.logoButton.setFixedSize(QtCore.QSize(10, 12))
            self.minimizeButton.setFixedSize(QtCore.QSize(10, 18))
            self.maxButton.setFixedSize(QtCore.QSize(10, 18))
            self.maxButton.setIconSize(QtCore.QSize(12, 12))
            self.closeButton.setFixedSize(QtCore.QSize(10, 18))
            self.closeButton.setIconSize(QtCore.QSize(12, 12))
            self.setFixedHeight(utils.dpiScale(int(self.titleBarHeight * 0.5)))
            self.titleLabel.setFixedHeight(utils.dpiScale(20))
            self.windowButtonsLayout.setSpacing(utils.dpiScale(6))
            self.helpButton.hide()

            utils.setStylesheetObjectName(self.titleLabel, "Minimized")
            self.titleLayout.setContentsMargins(*utils.marginsDpiScale(0, 3, 15, 7))
            self._mainRightLayout.setContentsMargins(*utils.marginsDpiScale(0, 0, 6, 0))
            self._mainLayout.setContentsMargins(*utils.marginsDpiScale(4, 0, 0, 0))
            self.contentsLayout.setContentsMargins(0, 0, 0, 0)
            self.cornerContentsLayout.setContentsMargins(
                *utils.marginsDpiScale(0, 0, 0, 0)
            )
            self.windowButtonsLayout.setContentsMargins(
                *utils.marginsDpiScale(0, 0, 0, 0)
            )

        elif style == self.TitleStyle.VerticalThin:
            self.setDirection(QtWidgets.QBoxLayout.TopToBottom)
            self.logoButton.setIconSize(QtCore.QSize(12, 12))
            self.logoButton.setFixedSize(QtCore.QSize(10, 12))
            self.minimizeButton.setFixedSize(QtCore.QSize(10, 18))
            self.maxButton.setFixedSize(QtCore.QSize(10, 18))
            self.maxButton.setIconSize(QtCore.QSize(12, 12))
            self.closeButton.setFixedSize(QtCore.QSize(10, 18))
            self.closeButton.setIconSize(QtCore.QSize(12, 12))
            self.setFixedWidth(int(self.titleBarHeight * 0.5))
            utils.setStylesheetObjectName(self.titleLabel, "Minimized")
            self.setMaximumHeight(uiconstants.QWIDGETSIZE_MAX)  # unlock the height
            self._mainLayout.setContentsMargins(*utils.marginsDpiScale(3, 3, 3, 3))
            self._mainRightLayout.setContentsMargins(*utils.marginsDpiScale(3, 3, 3, 3))
            self.contentsLayout.setContentsMargins(*utils.marginsDpiScale(3, 3, 3, 3))
            self.cornerContentsLayout.setContentsMargins(
                *utils.marginsDpiScale(3, 3, 3, 3)
            )
            self.titleLayout.setContentsMargins(*utils.marginsDpiScale(3, 3, 3, 3))
            self.windowButtonsLayout.setContentsMargins(
                *utils.marginsDpiScale(3, 3, 3, 3)
            )
            self._splitLayout.setContentsMargins(*utils.marginsDpiScale(3, 3, 3, 3))
        else:
            output.displayError(
                "'{}' style doesn't exist for {}.".format(
                    style, self.cgrigWindow.__class__.__name__
                )
            )

    def moveEnabled(self):
        """If the titlebar can drive movement.

        :return:
        :rtype:
        """
        return self._moveEnabled

    def setMaxButtonVisible(self, vis):
        """Set max button visible

        :param vis:
        :type vis:
        :return:
        :rtype:
        """
        self.maxButton.setVisible(vis)

    def setMinButtonVisible(self, vis):
        """Set Minimize button visible

        :param vis:
        :type vis:
        :return:
        :rtype:
        """
        self.minimizeButton.setVisible(vis)

    def titleStyle(self):
        """Return the title style

        :return:
        :rtype:
        """
        return self._titleStyle

    def previousTitleStyle(self):
        return self._previousTitleStyle

    def mouseDoubleClickEvent(self, event):
        """Mouse double clicked event

        :param event:
        :type event: :class:`QtGui.QMouseEvent`
        :return:
        :rtype:
        """
        # note: we don't call super to avoid mousePressEvent being called a second time
        self.doubleClicked.emit()

    def setLogoHighlight(self, highlight):
        """Set logo highlight.

        Highlight the logo

        :param highlight:
        :type highlight:
        :return:
        :rtype:
        """
        self.logoButton.setLogoHighlight(highlight)

    def refreshTitleBar(self):
        """Workaround for mainLayout not showing

        :return:
        """
        QtWidgets.QApplication.processEvents()
        self.updateGeometry()
        self.update()

    def setTitleText(self, value=""):
        """The text of the title bar in the window

        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.titleLabel.setText(value.upper())

    def _connections(self):
        """

        :return:
        """
        self.closeButton.leftClicked.connect(self.cgrigWindow.close)
        self.minimizeButton.leftClicked.connect(self._onMinimizeButtonClicked)
        self.maxButton.leftClicked.connect(self._onMaximizeButtonClicked)
        self.helpButton.leftClicked.connect(self.openHelp)

    def openHelp(self):
        """Open help url

        :return:
        """
        webbrowser.open(self.cgrigWindow.helpUrl)

    def setWindowIconSize(self, size):
        """
        Sets the icon size of the titlebar icons
        :param size:
        :return:
        """
        self.iconSize = size

    def setMaximiseVisible(self, show=True):
        """Set Maximise button visible

        :param show:
        """
        if show:
            self.maxButton.show()
        else:
            self.maxButton.hide()

    def setMinimiseVisible(self, show=True):
        """Set minimize button visibility

        :param show:
        """
        if show:
            self.minimizeButton.show()
        else:
            self.minimizeButton.hide()

    def toggleContents(self):
        """Show or hide the additional contents in the titlebar"""
        if self.contentsLayout.count() > 0:
            for i in range(1, self.contentsLayout.count()):
                widget = self.contentsLayout.itemAt(i).widget()
                if widget.isHidden():
                    widget.show()
                else:
                    widget.hide()

    def mousePressEvent(self, event):
        """Mouse click event to start the moving of the window

        :type event: :class:`QtGui.QMouseEvent`
        """
        if event.buttons() & QtCore.Qt.LeftButton:
            self.startMove()

        event.ignore()

    def mouseReleaseEvent(self, event):
        """Mouse release for title bar

        :type event: :class:`QtGui.QMouseEvent`
        """
        self.endMove()

    def startMove(self):
        if self._moveEnabled:
            self.widgetMousePos = self.cgrigWindow.mapFromGlobal(QtGui.QCursor.pos())

    def endMove(self):
        if self._moveEnabled:
            self.widgetMousePos = None

    def mouseMoveEvent(self, event):
        """Move the window based on if the titlebar has been clicked or not

        :type event: :class:`QtGui.QMouseEvent`
        """
        if self.widgetMousePos is None or not self._moveEnabled:
            return

        pos = QtGui.QCursor.pos() - self.widgetMousePos

        delta = pos - self.window().pos()
        self.moving.emit(pos, delta)

        self.window().move(pos)

    def _onMinimizeButtonClicked(self):
        self.cgrigWindow.minimize()

    def _onMaximizeButtonClicked(self):
        self.cgrigWindow.maximize()


class FramelessOverlay(overlay.OverlayWidget):
    MOVEBUTTON = QtCore.Qt.MiddleButton
    RESIZEBUTTON = QtCore.Qt.RightButton

    def __init__(self, parent, titleBar, resizable=True):
        """Handles linux like window movement.

        Eg Alt-Middle click to move entire window
        Alt Left Click corner to resize

        """
        super(FramelessOverlay, self).__init__(parent=parent)
        self.resizable = resizable

        self.titleBar = titleBar
        self.pressedAt = QtCore.QPoint()  # for detect change between press/release

        # note 2 different positions used here, resizePos for resize left/top
        # and previousMovePos for resize right, bottom
        self._resizePos = QtCore.QPoint()
        self.resizeDir = 0

    def mousePressEvent(self, event):
        """Alt-Middle click to move window

        :param event:
        :return:
        """
        self.pressedAt = QtGui.QCursor.pos()

        if not self.isEnabled():
            event.ignore()
            super(FramelessOverlay, self).mousePressEvent(event)
            return

        if self.isModifier() and event.buttons() & self.MOVEBUTTON:
            self.titleBar.startMove()
            self.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

        if self.isModifier() and event.buttons() & self.RESIZEBUTTON and self.resizable:
            self.resizeDir = self.quadrant()
            self._resizePos = QtGui.QCursor.pos()
            if self.resizeDir == ResizeDirection.Top | ResizeDirection.Right:
                self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
            elif self.resizeDir == ResizeDirection.Top | ResizeDirection.Left:
                self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
            elif self.resizeDir == ResizeDirection.Bottom | ResizeDirection.Left:
                self.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
            elif self.resizeDir == ResizeDirection.Bottom | ResizeDirection.Right:
                self.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)

        if (not self.isModifier() and event.buttons() & self.MOVEBUTTON) or (
                not self.isModifier() and event.buttons() & self.RESIZEBUTTON
        ):
            self.hide()

        event.ignore()
        return super(FramelessOverlay, self).mousePressEvent(event)

    @classmethod
    def isModifier(cls):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        # return modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier
        return modifiers == MODIFIER

    def mouseReleaseEvent(self, event):

        if not self.isEnabled():
            event.ignore()
            super(FramelessOverlay, self).mouseReleaseEvent(event)
            return

        self.titleBar.endMove()
        self.resizeDir = 0
        event.ignore()

        # If there is no difference in position at all, let the mouse click through
        if self.pressedAt - QtGui.QCursor.pos() == QtCore.QPoint(0, 0):
            utils.clickUnder(QtGui.QCursor.pos(), 1, modifier=MODIFIER)
        self._resizePos = QtCore.QPoint()
        super(FramelessOverlay, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """

        :param event:
        :type event:
        """
        if not self.isEnabled():
            event.ignore()
            super(FramelessOverlay, self).mouseMoveEvent(event)
            return

        if not self.isModifier():
            self.hide()
            return

        self.titleBar.mouseMoveEvent(event)

        if self.resizeDir != 0:
            self._handleResize()
            self._resizePos = QtGui.QCursor.pos()

        event.ignore()

        super(FramelessOverlay, self).mouseMoveEvent(event)

    def _handleResize(self):
        pos = QtGui.QCursor.pos()
        window = self.window()
        width, height = window.width(), window.height()
        minSize = self.window().minimumSize()
        geom = window.frameGeometry()
        # Minimum Size
        delta = pos - self._resizePos
        # Check to see if the ResizeDirection flag is in self.direction
        if self.resizeDir & ResizeDirection.Left == ResizeDirection.Left:
            width = max(window.minimumWidth(), width - delta.x())
            geom.setLeft(geom.right() - width)
        if self.resizeDir & ResizeDirection.Top == ResizeDirection.Top:
            height = max(window.minimumHeight(), height - delta.y())
            geom.setTop(geom.bottom() - height)
        if self.resizeDir & ResizeDirection.Right == ResizeDirection.Right:
            width = max(minSize.width(), width + delta.x())
            geom.setWidth(width)
        if self.resizeDir & ResizeDirection.Bottom == ResizeDirection.Bottom:
            height = max(minSize.height(), height + delta.y())
            geom.setHeight(height)
        window.setGeometry(geom)

    def quadrant(self):
        """Get the quadrant of where the mouse is pointed, and return the direction

        :return: The direction ResizeDirection
        :rtype: ResizeDirection
        """
        midX = self.geometry().width() * 0.5
        midY = self.geometry().height() * 0.5
        ret = 0

        pos = self.mapFromGlobal(QtGui.QCursor.pos())

        if pos.x() < midX:
            ret = ret | ResizeDirection.Left
        elif pos.x() > midX:
            ret = ret | ResizeDirection.Right

        if pos.y() < midY:
            ret = ret | ResizeDirection.Top
        elif pos.y() > midY:
            ret = ret | ResizeDirection.Bottom

        return ret

    def show(self):
        self.updateStyleSheet()
        if self.isEnabled():
            super(FramelessOverlay, self).show()
        else:
            logger.warning("FramelessOverlay.show() was called when it is disabled")

    def setEnabled(self, enabled):
        self.setDebugMode(not enabled)
        self.setVisible(enabled)
        super(FramelessOverlay, self).setEnabled(enabled)

    def updateStyleSheet(self):
        """Set style sheet

        :return:
        """
        self.setDebugMode(self._debug)


class WindowContents(QtWidgets.QFrame):
    """For CSS purposes"""


class TitleLabel(ClippedLabel):
    """For CSS purposes"""

    def __init__(self, *args, **kwargs):
        super(TitleLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight)


class _HeadWidget(QtWidgets.QWidget):
    def __init__(self, custom_widget, icon_path, parent=None):
        super(_HeadWidget, self).__init__(parent)
        self.setFixedHeight(30)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 0, 0, 0)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.logo_label = QtWidgets.QLabel(self)
        logo_pix = QtGui.QPixmap(icon_path)
        logo_pix = logo_pix.scaled(20, 20)
        self.logo_label.setPixmap(logo_pix)

        self.main_layout.addWidget(self.logo_label)
        # self.main_layout.addStretch(0)
        self.main_layout.addWidget(custom_widget)


class FrameLessWindow(QtWidgets.QWidget):
    """
    无边框的主窗口（优化版）
    """

    def __init__(self, custom_head_widget=None, body_widget=None, icon_path=None, parent=None):
        super(FrameLessWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMinimumSize(QtCore.QSize(120, 60))  # 最小尺寸限制

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        if custom_head_widget is not None:
            self.main_layout.addWidget(_HeadWidget(custom_head_widget, icon_path, self))
        if body_widget is not None:
            self.main_layout.addWidget(body_widget)

        # 状态变量
        self.is_drag = False
        self.drag_offset = None
        self.drag_side_select = set()
        self.resize_margin = 5  # 调整大小的边缘宽度，统一变量更易维护

        # 光标更新定时器（降低频率，减少性能消耗）
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateCursor)
        self.timer.start(50)  # 原10ms太频繁，50ms足够流畅且更省资源

    def updateCursor(self):
        """更新鼠标光标样式（优化坐标计算逻辑）"""
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        # 统一使用 resize_margin，避免魔法数字
        margin = self.resize_margin

        # 定义边缘/角落的矩形区域和对应光标
        select_table = [
            # 四个角落
            (QtCore.QRect(0, 0, margin, margin), QtCore.Qt.SizeFDiagCursor),  # 左上
            (QtCore.QRect(self.width() - margin, 0, margin, margin), QtCore.Qt.SizeBDiagCursor),  # 右上
            (QtCore.QRect(0, self.height() - margin, margin, margin), QtCore.Qt.SizeBDiagCursor),  # 左下
            (QtCore.QRect(self.width() - margin, self.height() - margin, margin, margin), QtCore.Qt.SizeFDiagCursor),
            # 右下

            # 四条边
            (QtCore.QRect(0, 0, margin, self.height()), QtCore.Qt.SizeHorCursor),  # 左边
            (QtCore.QRect(self.width() - margin, 0, margin, self.height()), QtCore.Qt.SizeHorCursor),  # 右边
            (QtCore.QRect(0, 0, self.width(), margin), QtCore.Qt.SizeVerCursor),  # 上边
            (QtCore.QRect(0, self.height() - margin, self.width(), margin), QtCore.Qt.SizeVerCursor),  # 下边
        ]

        for rect, cursor in select_table:
            if rect.contains(pos):
                self.setCursor(cursor)
                return
        self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        """鼠标按下事件（修复边缘检测逻辑）"""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_drag = True
            self.drag_offset = event.globalPos() - self.pos()
            rect = self.geometry()
            margin = self.resize_margin

            # 边缘检测：改用局部坐标，避免全局坐标偏移问题
            local_pos = self.mapFromGlobal(event.globalPos())
            side_check_table = {
                'left': QtCore.QRect(0, 0, margin, self.height()),
                'right': QtCore.QRect(self.width() - margin, 0, margin, self.height()),
                'top': QtCore.QRect(0, 0, self.width(), margin),
                'bottom': QtCore.QRect(0, self.height() - margin, self.width(), margin),
            }

            self.drag_side_select = set()
            for side, side_rect in side_check_table.items():
                if side_rect.contains(local_pos):
                    self.drag_side_select.add(side)
            # print('drag_side_select:', self.drag_side_select)

    def mouseMoveEvent(self, event):
        """鼠标移动事件（修复调整大小的边界问题）"""
        if not self.is_drag:
            return

        now_rect = self.geometry()
        # 拖拽移动窗口（无边缘选中时）
        if not self.drag_side_select:
            self.move(event.globalPos() - self.drag_offset)
        # 调整窗口大小（有边缘选中时）
        else:
            global_pos = event.globalPos()
            local_pos = self.mapFromGlobal(global_pos)

            # 左边缘：限制最小宽度
            if 'left' in self.drag_side_select:
                new_x = global_pos.x()
                new_width = now_rect.right() - new_x
                if new_width >= self.minimumWidth():
                    now_rect.setX(new_x)
                    now_rect.setWidth(new_width)

            # 右边缘：限制最小宽度
            if 'right' in self.drag_side_select:
                new_width = global_pos.x() - now_rect.x()
                if new_width >= self.minimumWidth():
                    now_rect.setWidth(new_width)

            # 上边缘：限制最小高度
            if 'top' in self.drag_side_select:
                new_y = global_pos.y()
                new_height = now_rect.bottom() - new_y
                if new_height >= self.minimumHeight():
                    now_rect.setY(new_y)
                    now_rect.setHeight(new_height)

            # 下边缘：限制最小高度
            if 'bottom' in self.drag_side_select:
                new_height = global_pos.y() - now_rect.y()
                if new_height >= self.minimumHeight():
                    now_rect.setHeight(new_height)

            self.setGeometry(now_rect)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == QtCore.Qt.LeftButton:
            self.is_drag = False
            self.drag_offset = None
            self.drag_side_select = set()

    def paintEvent(self, event):
        """绘制圆角背景（优化抗锯齿）"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)  # 抗锯齿
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)  # 平滑渲染
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor('#444444'))  # 窗口背景色
        # 绘制圆角矩形（半径10px）
        painter.drawRoundedRect(self.rect(), 10, 10)
        painter.end()


class DialogCustomHeadWidget(QtWidgets.QWidget):
    def __init__(self):
        super(DialogCustomHeadWidget, self).__init__()
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addStretch(0)

        self.close_button = elements.styledButton(icon="close")
        # self.close_button = IconButton(os.path.join(asset.ICON_PATH, 'x.png'), 20, hit_color=QColor('#F75B5B'))

        self.close_button.clicked.connect(lambda: self.window().close())

        self.main_layout.addWidget(self.close_button)


class Dialog(FrameLessWindow):
    def __init__(self, body_widget, parent=None):
        super(Dialog, self).__init__(DialogCustomHeadWidget(), body_widget, parent)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def exec_(self):
        self.show()
        while self.isVisible():
            QtWidgets.QApplication.processEvents()



















