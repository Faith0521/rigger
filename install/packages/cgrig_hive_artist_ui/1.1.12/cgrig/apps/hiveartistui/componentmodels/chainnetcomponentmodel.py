import itertools
from maya import cmds
from cgrig.apps.hiveartistui import model
from cgrig.apps.hiveartistui.views import componentsettings
from cgrig.apps.hiveartistui.views import widgethelpers
from cgrig.libs.maya import zapi
from cgrig.apps.hiveartistui.views import guideselectwidget
from Qt import  QtWidgets, QtCore
from cgrig.libs.pyqt.widgets import elements
from cgrig.libs.hive import api as hiveapi
from cgrig.libs.commands import hive


class ChainNetComponentModel(model.ComponentModel):
    """Base Class for Vchain class and subclasses to support better UI
    organization.
    """
    componentType = "chainnetcomponent"

    def createWidget(self, componentWidget, parentWidget):
        return ChainNetSettingsWidget(componentWidget,
                                    parentWidget,
                                    componentModel=self)


class DriverSelectWidget(guideselectwidget.GuideSelectWidget):

    def __init__(self, rigModel,
                 label,
                 toolTip,
                 buttonToolTip,
                 componentModel=None,
                 parent=None,
                 driverId=None):
        super(DriverSelectWidget, self).__init__(rigModel,
                                                 label, toolTip, buttonToolTip,
                                                 componentModel, parent)
        self.driverId = driverId
        self._guideSelect.clicked.connect(self._onGuideSelected)
        # self.

    def _hardRefresh(self):
        self._itemComboBox.blockSignals(True)
        self._itemComboBox.clear()
        self.itemData = [[None, None]]
        self._itemComboBox.addItem("")

        if not self.rigModel:
            self._itemComboBox.blockSignals(False)
            return
        comboSet = False
        compDrivers = self.componentModel.component.definition.drivers

        currentDriverExpr = hiveapi.DriverDef("", "", hiveapi.DriverMatrixConstParams([], "", False))
        for driver in compDrivers:
            if driver.label == self.driverId:
                currentDriverExpr = driver
        rig = self.rigModel.rig
        for comp in rig.iterComponents():
            if comp == self.componentModel.component:
                continue
            guideLayer = comp.guideLayer()
            if guideLayer is None:
                continue
            componentToken = comp.serializedTokenKey()
            idMapping = comp.idMapping()
            outputMap = idMapping[hiveapi.constants.OUTPUT_LAYER_TYPE]
            for guide in guideLayer.iterGuides(includeRoot=False):
                outputNode = outputMap.get(guide.id())
                if not outputNode:
                    continue
                self._itemComboBox.addItem(self.itemName(comp, guide))
                self.itemData.append([comp, guide])

                guideExpr = hiveapi.pathAsDefExpression((componentToken, "outputLayer", outputNode))
                if not comboSet:
                    if self.isCurrentUISelected(comp, guide):
                        comboSet = True
                        self._itemComboBox.setCurrentIndex(self._itemComboBox.count() - 1)
                        continue
                    for driverLabel, driverExpr in currentDriverExpr.params.drivers:
                        if guideExpr == driverExpr and not comboSet:
                            self._itemComboBox.setCurrentIndex(self._itemComboBox.count() - 1)

        self._itemComboBox.blockSignals(False)

    def _onGuideSelected(self):
        self._itemComboBox.blockSignals(True)
        for sel in zapi.selected():
            if not hiveapi.Guide.isGuide(sel):
                continue
            guide = hiveapi.Guide(sel.object())
            component = hiveapi.componentFromNode(guide)
            if not component or component == self.componentModel.component:
                continue
            self._createComponentDriver(component, guide)
            self._itemComboBox.setTexts(self.itemName(component, guide))
            break
        self._itemComboBox.blockSignals(False)

    def _createComponentDriver(self, component, guide):
        outputId = component.idMapping()[hiveapi.constants.OUTPUT_LAYER_TYPE].get(guide.id())
        if not outputId:
            return
        componentKey = component.serializedTokenKey()
        self.componentModel.component.setChainDriver(self.driverId,
                                                   hiveapi.pathAsDefExpression(
                                                       (componentKey, "outputLayer", outputId))
                                                   )

    def onValueChanged(self, event):
        """ on Value Changed

        :param event: Event with all the values related to the change.
        :type event: cgrig.libs.pyqt.extended.combobox.ComboItemChangedEvent
        :return:
        :rtype:
        """
        data = self.itemData[self._itemComboBox.currentIndex()]
        self._createComponentDriver(data[0], data[1])
        self.currentItem = data[0], data[1]


class ChainNetSettingsWidget(componentsettings.ComponentSettingsWidget):
    def __init__(self, componentWidget, parent, componentModel):
        super(ChainNetSettingsWidget, self).__init__(componentWidget, parent, componentModel)

    def initUi(self):
        layout = self.layout()
        guideLayerDef = self.componentModel.component.definition.guideLayer
        Settings = guideLayerDef.guideSettings("hasJoints", "hasControls",
                                               "jointCount", "fkCtrlCount", "percent")
        hasJoints = Settings["hasJoints"]
        hasControls = Settings["hasControls"]
        jointCount = Settings["jointCount"]
        fkCtrlCount = Settings["fkCtrlCount"]
        percent = Settings["percent"]

        hasJointsWidget = componentsettings.createBooleanWidget(
            self, hasJoints, "Has Joints", layout, self.settingCheckboxChanged
        )
        hasControlsWidget = componentsettings.createBooleanWidget(
            self, hasControls, "Has Controls", layout, self.settingCheckboxChanged
        )
        jointCountWidget = componentsettings.createIntWidget(
            self, jointCount, "Joint Count", layout, self.settingNumericChanged
        )
        fkCtrlCountWidget = componentsettings.createIntWidget(
            self, fkCtrlCount, "FK Ctrl Count", layout, self.settingNumericChanged
        )

        self.masterADriverWidget = DriverSelectWidget(rigModel=self.rigModel,
                                                     label="Master A Guide",
                                                     toolTip="",
                                                     buttonToolTip="",
                                                     componentModel=self.componentModel,
                                                     parent=self,
                                                     driverId="masterA")
        self.masterBDriverWidget = DriverSelectWidget(rigModel=self.rigModel,
                                                     componentModel=self.componentModel,
                                                     label="Master B Guide",
                                                     toolTip="",
                                                     buttonToolTip="",
                                                     parent=self,
                                                     driverId="masterB")
        percentWidget = componentsettings.createIntWidget(
            self, percent, "Percent", layout, self.settingNumericChanged
        )
        layout.addWidget(hasJointsWidget)
        layout.addWidget(hasControlsWidget)
        layout.addWidget(jointCountWidget)
        layout.addWidget(fkCtrlCountWidget)
        layout.addWidget(self.masterADriverWidget)
        layout.addWidget(self.masterBDriverWidget)
        layout.addWidget(percentWidget)

        self.createSpaceLayout()
        self.createNamingConventionLayout()
        self.createDeformSettingsLayout()


    def updateUi(self):
        super(ChainNetSettingsWidget, self).updateUi()
        self.masterADriverWidget.updateCombo()
        self.masterBDriverWidget.updateCombo()
