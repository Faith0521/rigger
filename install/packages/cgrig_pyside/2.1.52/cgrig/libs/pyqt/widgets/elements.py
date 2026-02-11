# -*- coding: utf-8 -*-
from cgrig.core.util import env
from cgrig.libs import iconlib
from cgrig.libs.pyqt.extended.imageview.thumbnail.virtualslider import VirtualSlider
from cgrig.libs.pyqt.widgets import dialogs
from cgrig.libs.pyqt.widgets.listwidget import ListWidget, ListEditWidget
from cgrig.libs.pyqt.widgets.frame import CollapsableFrame, CollapsableFrameThin
from cgrig.libs.pyqt.widgets.frameless.window import CgRigWindow, CgRigWindowThin
from cgrig.libs.pyqt.widgets.joinedradio import JoinedRadioButton
from cgrig.libs.utils import color

# Imports so we can use the other widgets from elements (eg elements.IconMenuButton())
from cgrig.libs.pyqt.widgets.radiobuttongroup import RadioButtonGroup
from cgrig.libs.pyqt.widgets.slider import Slider, HSlider, VSlider, FloatSlider, IntSlider
from cgrig.libs.pyqt.widgets.spacer import Divider, QHLine, QVLine, Spacer
from cgrig.libs.pyqt.widgets.popups import SaveDialog, InputDialogQt, MessageBox, MessageBoxQt, \
    FileDialog_directory, InputDialog, MessageBoxBase
from cgrig.libs.pyqt.widgets.iconmenu import IconMenuButton, iconMenuButtonCombo, DotsMenu

from cgrig.libs.pyqt.widgets.label import Label, HeaderLabel, LabelDivider, TitleLabel, LabelDividerCheckBox, IconLabel
from cgrig.libs.pyqt.widgets.textedit import TextEdit
from cgrig.libs.pyqt.widgets.layouts import (hBoxLayout,
                                           vBoxLayout,
                                           GridLayout,
                                           hGraphicsLinearLayout,
                                           vGraphicsLinearLayout,
                                           formLayout)

from cgrig.libs.pyqt.widgets.extendedbutton import ExtendedButton
from cgrig.libs.pyqt.widgets.extendedmenu import ExtendedMenu
from cgrig.libs.pyqt.widgets.buttons import (OkCancelButtons,
                                           buttonRound,
                                           styledButton,
                                           buttonExtended,
                                           regularButton,
                                           iconShadowButton,
                                           AlignedButton,
                                           ShadowedButton,
                                           LeftAlignedButtonBase,
                                           leftAlignedButton)
from cgrig.libs.pyqt.widgets.searchwidget import SearchLineEdit
from cgrig.libs.pyqt.widgets.stringedit import StringEdit, FloatEdit, IntEdit
from cgrig.libs.pyqt.extended.combobox import ComboBox, ComboBoxRegular, ComboBoxSearchable, ExtendedComboBox
from cgrig.libs.pyqt.extended.combobox.comboeditwidget import ComboEditWidget, ComboEditRename, EditChangedEvent, \
    IndexChangedEvent
from cgrig.libs.pyqt.extended.spinbox import VectorSpinBox, Transformation, Matrix
from cgrig.libs.pyqt.extended.lineedit import LineEdit, FloatLineEdit, IntLineEdit, VectorLineEdit
from cgrig.libs.pyqt.extended.menu import MenuCreateClickMethods
from cgrig.libs.pyqt.extended.checkbox import CheckBox
from cgrig.libs.pyqt.extended.hotkeydetectedit import HotkeyDetectEdit
from cgrig.libs.pyqt.extended.color import LabelColorBtn, ColorPaletteColorList, ColorHsvBtns, ColorSlider, ColorBtn
from cgrig.libs.pyqt.extended.embeddedwindow import EmbeddedWindow
from cgrig.libs.pyqt.extended.clippedlabel import ClippedLabel
from cgrig.libs.pyqt.widgets.imagebutton import ImageButton
from cgrig.libs.pyqt.widgets.iconmenu import IconMenuButton
from cgrig.libs.pyqt.extended.combobox.combomenupopup import ComboCustomEvent
from cgrig.libs.pyqt.widgets.stackwidget import LineClickEdit
from cgrig.libs.pyqt.extended.snapshotui import SnapshotUi
from cgrig.libs.pyqt.extended.imageview.thumbnail.minibrowser import ThumbnailSearchWidget, MiniBrowser
from cgrig.libs.pyqt.extended.imageview.thumbnail.thumbnailwidget import ThumbnailWidget
from cgrig.libs.pyqt.widgets.pathwidget import (PathWidget,
                                              PathOpenWidget,
                                              DirectoryPathWidget,
                                              DirectoryPathListWidget,
                                              BrowserPathListWidget,
                                              BrowserPathWidget)


if env.isMaya():
    from cgrig.libs.maya.qt.cmdswidgets import MayaColorBtn as ColorBtn, MayaColorHsvBtns as ColorHsvBtns, \
        MayaColorSlider as ColorSlider
    from cgrig.libs.maya.qt.changerendererui import checkRenderLoaded  # todo should this be here?

