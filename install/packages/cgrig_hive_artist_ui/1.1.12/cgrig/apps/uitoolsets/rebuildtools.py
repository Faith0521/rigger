""" ---------- Hive Rebuild Tools -------------
Toolset for Hive's Rebuild  Tools

"""
import os

from cgrigvendor.Qt import QtWidgets, QtCore
from cgrig.libs import iconlib

from cgrig.apps.toolsetsui.widgets import toolsetwidget
from cgrig.libs.pyqt import uiconstants as uic
from cgrig.libs.pyqt.widgets import elements
from cgrig.apps.toolsetsui.widgets.toolsetresizer import ToolsetResizer

from cgrig.libs.hive.rebuildtools import defaultattrs
from cgrig.libs.maya.cmds.sets import selectionsets
from cgrig.libs.maya.cmds.hotkeys import definedhotkeys

from cgrig.libs.maya.cmds.workspace import mayaworkspace

UI_MODE_COMPACT = 0
UI_MODE_ADVANCED = 1

TOOL_COMBO_OPTIONS = ["Select Tool...",
                      "Override Default Attribute Values",
                      "Keep Custom Selection Sets"
                      ]  # "Connection Rebuilder", "Add Custom Visibility"


class RebuildTools(toolsetwidget.ToolsetWidget):
    id = "rebuildTools"
    info = "Tools for rebuilding rigs in the Hive."
    uiData = {"label": "Hive Rebuild Tools",
              "icon": "hammer",
              "tooltip": "Tools for rebuilding rigs in the Hive.",
              "defaultActionDoubleClick": False,
              "helpUrl": "https://create3dcharacters.com/maya-tool-hive-rebuild-tools/"}

    # ------------------
    # STARTUP
    # ------------------

    def preContentSetup(self):
        """First code to run, treat this as the __init__() method"""
        pass

    def contents(self):
        """The UI Modes to build, compact, medium and or advanced """
        return [self.initCompactWidget()]  # self.initAdvancedWidget()

    def initCompactWidget(self):
        """Builds the Compact GUI (self.compactWidget) """
        self.compactWidget = GuiCompact(parent=self, properties=self.properties, toolsetWidget=self)
        return self.compactWidget

    def initAdvancedWidget(self):
        """Builds the Advanced GUI (self.advancedWidget) """
        self.advancedWidget = GuiAdvanced(parent=self, properties=self.properties, toolsetWidget=self)
        return self.advancedWidget

    def postContentSetup(self):
        """Last of the initialize code"""
        self.uiFolderPath = None
        self._rigStateChanged()  # Updates the rig combo box
        self.toolModeChanged()
        self.loadDefaultDataFromScene(message=False)  # default attr data
        self.loadSelSetSceneToUI(message=False)  # selection sets data
        self.uiConnections()

    @property
    def defaultBrowserPath(self):
        outputDirectory = os.path.expanduser("~")
        projectDirPath = mayaworkspace.getProjSubDirectory(sudDirectory="data", message=True)
        if projectDirPath:
            outputDirectory = projectDirPath
        return outputDirectory

    def defaultAction(self):
        """Double Click
        Double clicking the tools toolset icon will run this method
        Be sure "defaultActionDoubleClick": True is set inside self.uiData (meta data of this class)"""
        pass

    def currentWidget(self):
        """ Currently active widget

        :return:
        :rtype: GuiAdvanced or GuiCompact
        """
        return super(RebuildTools, self).currentWidget()

    def widgets(self):
        """ Override base method for autocompletion

        :return:
        :rtype: list[GuiAdvanced or GuiCompact]
        """
        return super(RebuildTools, self).widgets()

    # ------------------
    # ENTER WINDOW MOUSE EVENT
    # ------------------

    def enterEvent(self, event):
        """When the cursor enters the UI update it"""
        self._rigStateChanged()
        self.updateUISettings()  # Update the UI settings

    def _rigStateChanged(self):
        self._updateSceneRigs()
        for widget in self.widgets():
            widget.updateRigs(self.rigComboNames)

    def _updateSceneRigs(self):
        self.rigComboNames, self.rigInstances = defaultattrs.allRigsComboUI()

    def _currentRigChangedFromArtistUI(self, rigName):
        for widget in self.widgets():
            widget.setCurrentRig(rigName)

    def uiSettingsDict(self):
        uiSettingsDict = dict()
        self.updateUISettings()
        uiSettingsDict["rigCombo"] = self.rigCombo
        uiSettingsDict["outputFilePath"] = self.outputFilePath
        return uiSettingsDict

    def updateUISettings(self):
        """Updates all the class variables UI based on the current settings"""
        if not self.rigInstances:
            self.rigInstance = None
            self.rigName = ""
        else:
            self.rigInstance = self.rigInstances[self.properties.rigListCombo.value]
            self.rigName = self.rigComboNames[self.properties.rigListCombo.value]

        self.rigCombo = self.properties.rigListCombo.value

    # ------------------
    # TOOL VISIBILITY
    # ------------------

    def defaultAttrWidgetVis(self, vis):
        for widget in self.compactWidget.defaultAttrWidgets:
            widget.setVisible(vis)

    def cgrigSetsWidgetVis(self, vis):
        for widget in self.compactWidget.cgrigSetsWidgets:
            widget.setVisible(vis)

    def toolModeChanged(self):
        """Shows and hides the appropriate widgets based on the radio button selection.
        0 = No Tool
        1 = Override Default Attribute Values
        2 = Keep Custom Selection Sets
        3 = Connection Rebuilder
        4 = Add Custom Visibility
        """
        modeComboInt = self.properties.toolModeCombo.value
        if modeComboInt == 0:
            self.defaultAttrWidgetVis(False)
            self.cgrigSetsWidgetVis(False)
        elif modeComboInt == 1:
            self.defaultAttrWidgetVis(True)
            self.cgrigSetsWidgetVis(False)
        elif modeComboInt == 2:
            self.defaultAttrWidgetVis(False)
            self.cgrigSetsWidgetVis(True)
        elif modeComboInt == 3:
            self.defaultAttrWidgetVis(False)
            self.cgrigSetsWidgetVis(False)
        elif modeComboInt == 4:
            self.defaultAttrWidgetVis(False)
            self.cgrigSetsWidgetVis(False)

        # Update UI size ----------------------------
        self.updateTree(delayed=True)  # Refresh GUI size

    # ------------------
    # LOGIC - OVERRIDE DEFAULT ATTRIBUTE VALUES
    # ------------------
    def openHiveWindow(self):
        """Opens the Hive window"""
        import cgrig.libs.maya.cmds.hotkeys.definedhotkeys as hk
        hk.open_hiveArtistUI()

    def rebuildHiveRig(self):
        """Rebuilds the current rig with the current saved settings"""
        defaultattrs.rebuildHiveRig(rig=self.rigInstance)

    def guidesMode(self):
        """Sets the current rig to Guides Mode."""
        defaultattrs.guidesMode(rig=self.rigInstance)

    def controlsMode(self):
        """Sets the current rig to Controls Mode."""
        defaultattrs.controlsMode(rig=self.rigInstance)

    def skeletonMode(self):
        """Sets the current rig to Skeleton Mode."""
        defaultattrs.skeletonMode(rig=self.rigInstance)

    def preRigMode(self):
        """Sets the current rig to PreRig Mode."""
        defaultattrs.preRigMode(rig=self.rigInstance)

    def polishMode(self):
        """Sets the current rig to Polish Mode."""
        defaultattrs.polishMode(rig=self.rigInstance)

    def reloadCgRigTools(self):
        """Reloads the CgRig Tools in Maya.  Closes all windows and reloads the toolset."""
        definedhotkeys.reloadCgRigTools()

    def objLimitPopup(self):
        """Shows a popup message if the object limit is exceeded."""
        message = ("This function is not optimized and is limited to six selected objects. \n\n"
                   "Otherwise it may hang Maya.\n\n"
                   "Please select six or fewer objects.")
        elements.MessageBox.showWarning(title="Too Many Selected Objects", message=message, buttonB=None)

    def addDefaultDataFromChannelBoxSelection(self):
        """Adds the current channel box selection to the default attribute values text edit.
        """
        # limit object count to 6 check
        if not defaultattrs.checkObjectCount(count=6):
            self.objLimitPopup()
            return

        incomingText = defaultattrs.get_channel_attrs_proxy_sel_string(rootOfProxies=True, longNames=False)
        if not incomingText:
            return
        text = self.compactWidget.setDefaultAttrText.toPlainText()
        newText = text + "\n" + incomingText if text else incomingText
        self.compactWidget.setDefaultAttrText.setPlainText(newText)

    def addAutoDetectDefaultData(self):
        """Adds the current auto-detected changes to the default attribute values text edit.
        Also checks if the default values of the attributes have changed from the default values in the scene.
        """
        # limit object count to 6 check
        if not defaultattrs.checkObjectCount(count=6):
            self.objLimitPopup()
            return

        incomingText = defaultattrs.get_channel_attrs_proxy_sel_string(rootOfProxies=True,
                                                                       longNames=False,
                                                                       hasChangedFromDefault=True)
        if not incomingText:
            return
        text = self.compactWidget.setDefaultAttrText.toPlainText()
        newText = text + "\n" + incomingText if text else incomingText
        self.compactWidget.setDefaultAttrText.setPlainText(newText)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def deleteDefaultDataFromScene(self):
        """Deletes the default attribute values from the scene.
        """
        defaultattrs.deleteStringDataScene()

    def clearDefaultDataText(self):
        """Clears the text in the default attribute values text edit.
        """
        self.compactWidget.setDefaultAttrText.setPlainText("")

    def setDefaultValuesFromText(self):
        """Sets the current text as the default values on the current rig.
        """
        dataString = self.compactWidget.setDefaultAttrText.toPlainText()
        applySym = self.properties.attrsApplySymRadio.value
        defaultattrs.set_string_to_defaultAttr(dataString, applySym=applySym, rig=self.rigInstance, message=True)

    def alphabetizeDefaultDataText(self):
        """Alphabetizes the default attribute values text edit.
        """
        dataString = self.compactWidget.setDefaultAttrText.toPlainText()
        if not dataString:
            return
        sorted_data_string = defaultattrs.alphabetical_sort_string(dataString)
        self.compactWidget.setDefaultAttrText.setPlainText(sorted_data_string)

    @toolsetwidget.ToolsetWidget.undoDecorator
    def saveDefaultAttrDataToScene(self):
        """
        """
        dataString = self.compactWidget.setDefaultAttrText.toPlainText()
        applySym = self.properties.attrsApplySymRadio.value
        defaultattrs.saveStringDataScene(dataString, applySym, rig=self.rigInstance, message=True)

    def loadDefaultDataFromScene(self, message=True):
        """Loads the default attribute values from the scene.
        """
        dataString, applySym = defaultattrs.getStringDataScene(message=message)
        if not dataString:
            return  # message reported
        self.compactWidget.setDefaultAttrText.setPlainText(dataString)
        self.properties.attrsApplySymRadio.value = applySym  # update the radio button value
        self.updateFromProperties()

    def saveDefaultAttrDataToDisk(self):
        """Saves the Default Attribute Override data to a file on disk."""
        if not self.uiFolderPath:
            self.uiFolderPath = self.defaultBrowserPath
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Default Attribute Overrides",
                                                            self.defaultBrowserPath, "*.cgrigAttrDefaults")
        if not filePath:  # cancel
            return
        data, applySym = defaultattrs.write_to_json(filePath)
        self.uiFolderPath = os.path.dirname(filePath)  # update the default browser path
        return data, applySym

    def loadDefaultDataFromDisk(self):
        """Imports Default Attribute Override data from a file on disk."""
        if not self.uiFolderPath:
            self.uiFolderPath = self.defaultBrowserPath
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import Default Attribute Overrides",
                                                            dir=self.uiFolderPath,
                                                            filter="*.cgrigAttrDefaults")
        if not filePath:  # cancel
            return
        dataString, applySym = defaultattrs.load_from_json(filePath, message=True)
        if not dataString:
            return  # message reported
        self.compactWidget.setDefaultAttrText.setPlainText(dataString)
        self.properties.attrsApplySymRadio.value = applySym  # update the radio button value
        self.updateFromProperties()

    def searchReplaceDefaultAttrText(self):
        """ Searches and replaces the text in the default attribute values text edit.
        """
        dataString = self.compactWidget.setDefaultAttrText.toPlainText()
        if not dataString:
            return
        search = self.properties.searchDefaultAttrTxt.value
        replace = self.properties.replaceDefaultAttrTxt.value
        if not search:
            return
        self.compactWidget.setDefaultAttrText.setPlainText(dataString.replace(search, replace))

    def validateDefaultAttrData(self):
        """Validates the current default attribute values text edit.
        Opens the script editor with the validation results.
        """
        dataString = self.compactWidget.setDefaultAttrText.toPlainText()
        defaultattrs.validate_default_attr_data(dataString, rig=self.rigInstance)

    # ------------------
    # KEEP CUSTOM SELECTION SETS
    # ------------------
    def openCgRigSelectionSetsUI(self):
        definedhotkeys.open_cgrigSelectionSets(advancedMode=False)

    def loadSelSetDataFromSel(self):
        data = selectionsets.get_selSet_hierarchy_data_sel()
        dataString = selectionsets.hierarchyDataToString(data)
        if dataString == "{}":  # not "{}"
            dataString = ""
        self.compactWidget.cgrigSetsText.setPlainText(dataString)

    def createSelSetsFromText(self):
        """Creates selection sets from the text in the cgrigSetsText text edit."""
        dataString = self.compactWidget.cgrigSetsText.toPlainText()  # messages reported
        if not dataString:  # not "{}"
            dataString = ""
        selectionsets.loadSelSetHierarchySceneStr(dataString, message=True)

    def clearSetText(self):
        """Clears the text in the cgrigSetsText text edit."""
        self.compactWidget.cgrigSetsText.setPlainText("")

    def deleteSetDataScene(self):
        """Deletes the selection sets data from the scene."""
        selectionsets.deleteSetDataScene()

    # ------------------
    # CUSTOM SELECTION SETS SAVE/LOAD
    # ------------------

    def saveSelSetDiskFromUI(self):
        """Saves the selected set/s to a file on disk."""
        if not self.uiFolderPath:
            self.uiFolderPath = self.defaultBrowserPath
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Selected Set/s To File",
                                                            self.defaultBrowserPath, "*.cgrigSelSets")
        if not filePath:  # cancel
            return
        dataString = self.compactWidget.cgrigSetsText.toPlainText()
        data = selectionsets.write_sets_to_json_from_string(dataString, filePath)
        if not data:  # messages reported
            return
        self.uiFolderPath = os.path.dirname(filePath)  # update the default browser path
        return data

    def loadSelSetDiskToUI(self):
        """Imports the sets from a file on disk."""
        if not self.uiFolderPath:
            self.uiFolderPath = self.defaultBrowserPath
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import Selection Set/s",
                                                            dir=self.uiFolderPath,
                                                            filter="*.cgrigSelSets")
        if not filePath:  # cancel
            return
        dataStr = selectionsets.read_sets_from_json_to_string(filePath, message=True)
        if not dataStr:  # messages reported
            dataStr = ""
        self.compactWidget.cgrigSetsText.setPlainText(dataStr)

    def saveSelSetSceneFromUI(self):
        """Saves the UI text to the current scene as a string attribute."""
        dataStr = self.compactWidget.cgrigSetsText.toPlainText()
        return selectionsets.saveSelSetsHierarchySceneText(dataStr, rig=self.rigInstance, message=True)

    def loadSelSetSceneToUI(self, message=True):
        """Imports the sets from the current scene as a string attribute."""
        dataStr = selectionsets.loadSelSetHierarchySceneToUI(message=message)
        if not dataStr:  # messages reported
            dataStr = ""
        self.compactWidget.cgrigSetsText.setPlainText(dataStr)

    # ------------------
    # CONNECTIONS
    # ------------------

    def uiConnections(self):
        """Add all UI connections here, button clicks, on changed etc"""
        for widget in self.widgets():
            #  KEEP CUSTOM SELECTION SETS -------------------------------------------------------------
            widget.openCgRigSetsBtn.clicked.connect(self.openCgRigSelectionSetsUI)
            widget.addSetsBtn.clicked.connect(self.loadSelSetDataFromSel)
            widget.createCgRigSetsBtn.clicked.connect(self.createSelSetsFromText)
            widget.addSetsSceneSavedBtn.clicked.connect(self.loadSelSetSceneToUI)
            widget.openHiveUIBtn.clicked.connect(self.openHiveWindow)
            widget.rebuildRigBtn.clicked.connect(self.rebuildHiveRig)
            widget.reloadCgRigBtn.clicked.connect(self.reloadCgRigTools)

            # Rebuild Menu ---------------------------------------
            widget.rebuildRigBtn.addAction("Rebuild To Current State (Default)",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.rebuildHiveRig)
            widget.rebuildRigBtn.addAction("Rig To Guides Mode",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.guidesMode)
            widget.rebuildRigBtn.addAction("Rig To Controls Mode",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.controlsMode)
            widget.rebuildRigBtn.addAction("Rig To Skeleton Mode",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.skeletonMode)
            widget.rebuildRigBtn.addAction("Rig To PreRig Mode",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.preRigMode)
            widget.rebuildRigBtn.addAction("Rig To Polish Mode",
                                           mouseMenu=QtCore.Qt.RightButton,
                                           icon=iconlib.icon("hammer"),
                                           connect=self.polishMode)

            # Save Menu ---------------------------------------
            widget.saveSelectionSetsBtn.addAction("Save To Scene (For Auto Rebuilds)",
                                                  mouseMenu=QtCore.Qt.LeftButton,
                                                  icon=iconlib.icon("save"),
                                                  connect=self.saveSelSetSceneFromUI)
            widget.saveSelectionSetsBtn.addAction("Save To Disk (JSON)",
                                                  mouseMenu=QtCore.Qt.LeftButton,
                                                  icon=iconlib.icon("save"),
                                                  connect=self.saveSelSetDiskFromUI)
            # Load Menu ---------------------------------------
            widget.loadSelectionSetsBtn.addAction("Load From Scene",
                                                  mouseMenu=QtCore.Qt.LeftButton,
                                                  icon=iconlib.icon("openFolder01"),
                                                  connect=self.loadSelSetSceneToUI)
            widget.loadSelectionSetsBtn.addAction("Load From Disk (JSON)",
                                                  mouseMenu=QtCore.Qt.LeftButton,
                                                  icon=iconlib.icon("openFolder01"),
                                                  connect=self.loadSelSetDiskToUI)
            # Delete Menu ---------------------------------------
            widget.delSetsBtn.addAction("Clear Text",
                                        mouseMenu=QtCore.Qt.LeftButton,
                                        icon=iconlib.icon("crossXFat"),
                                        connect=self.clearSetText)
            widget.delSetsBtn.addAction("Delete Settings From Scene",
                                        mouseMenu=QtCore.Qt.LeftButton,
                                        icon=iconlib.icon("trash"),
                                        connect=self.deleteSetDataScene)

            #  OVERRIDE DEFAULT ATTRIBUTES VALUES -------------------------------------------------------------
            widget.toolModeCombo.currentIndexChanged.connect(self.toolModeChanged)
            widget.setDefaultAttrsBtn.clicked.connect(self.setDefaultValuesFromText)
            widget.reorderAttrsBtn.clicked.connect(self.alphabetizeDefaultDataText)
            widget.validateAttrsBtn.clicked.connect(self.validateDefaultAttrData)
            widget.searchReplaceBtn.clicked.connect(self.searchReplaceDefaultAttrText)

            # Add Menu ---------------------------------------
            widget.addAttrsBtn.addAction("Add From Object or Channel Box Selection",
                                         mouseMenu=QtCore.Qt.LeftButton,
                                         icon=iconlib.icon("plusHollow"),
                                         connect=self.addDefaultDataFromChannelBoxSelection)
            widget.addAttrsBtn.addAction("Add From Auto-Detect (Non Default) Changes",
                                         mouseMenu=QtCore.Qt.LeftButton,
                                         icon=iconlib.icon("plusHollow"),
                                         connect=self.addAutoDetectDefaultData)
            # Save Menu ---------------------------------------
            widget.saveAttrsBtn.addAction("Save To Scene (For Auto Rebuilds)",
                                          mouseMenu=QtCore.Qt.LeftButton,
                                          icon=iconlib.icon("save"),
                                          connect=self.saveDefaultAttrDataToScene)
            widget.saveAttrsBtn.addAction("Save To Disk (JSON)",
                                          mouseMenu=QtCore.Qt.LeftButton,
                                          icon=iconlib.icon("save"),
                                          connect=self.saveDefaultAttrDataToDisk)
            # Load Menu ---------------------------------------
            widget.loadAttrsBtn.addAction("Load From Scene",
                                          mouseMenu=QtCore.Qt.LeftButton,
                                          icon=iconlib.icon("openFolder01"),
                                          connect=self.loadDefaultDataFromScene)
            widget.loadAttrsBtn.addAction("Load From Disk (JSON)",
                                          mouseMenu=QtCore.Qt.LeftButton,
                                          icon=iconlib.icon("openFolder01"),
                                          connect=self.loadDefaultDataFromDisk)
            # Delete Menu ---------------------------------------
            widget.delAttrsBtn.addAction("Clear Text",
                                         mouseMenu=QtCore.Qt.LeftButton,
                                         icon=iconlib.icon("crossXFat"),
                                         connect=self.clearDefaultDataText)
            widget.delAttrsBtn.addAction("Delete Settings From Scene",
                                         mouseMenu=QtCore.Qt.LeftButton,
                                         icon=iconlib.icon("trash"),
                                         connect=self.deleteDefaultDataFromScene)


class GuiWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None, properties=None, uiMode=None, toolsetWidget=None):
        """Builds the main widgets for all GUIs

        properties is the list(dictionaries) used to set logic and pass between the different UI layouts
        such as compact/adv etc

        :param parent: the parent of this widget
        :type parent: QtWidgets.QWidget
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: cgrig.apps.toolsetsui.widgets.toolsetwidget.PropertiesDict
        :param uiMode: 0 is compact ui mode, 1 is advanced ui mode
        :type uiMode: int
        """
        super(GuiWidgets, self).__init__(parent=parent)
        self.properties = properties
        self.toolsetWidget = toolsetWidget
        # -----------------------------
        #  TOOL COMBOS
        # -----------------------------

        toolTip = ("Select the tool mode to save data.  All modes are supported by the \n"
                   "`rebuildTools_buildScript`. \n\n"
                   "- Override Attribute Default Values: \n"
                   "Use this to modify the default attribute values of a Hive rig. \n\n"
                   "- Keep Custom Selection Sets: \n"
                   "Use this to keep custom selection sets while rebuilding Hive rigs. \n\n"
                   "The `rebuildTools_buildScript` is automatically applied to the Hive rig's settings: \n"
                   "Hive UI > Global Rig Settings (cog icon).")
        self.toolModeCombo = elements.ComboBoxRegular("Tool Mode",
                                                      items=TOOL_COMBO_OPTIONS,
                                                      setIndex=0,
                                                      parent=parent,
                                                      labelRatio=1,
                                                      boxRatio=5,
                                                      toolTip=toolTip)

        # -----------------------------
        #  DEFAULT ATTRIBUTE VALUE OVERRIDES
        # -----------------------------

        # Default Attr Title ---------------------------------------
        self.defaultAttrTitle = elements.LabelDivider("Override Default Attribute Values")
        # Text Edit ---------------------------------------
        placeholderText = (
            "Add custom attributes to set their default values for Hive rebuilds. \n"
            "Hive Rigs will rebuild with the overridden default values. \n\n"
            "Maya native attributes like `translateX` cannot be changed. \n\n"
            "Use the `Add From Channel Box Selection` button to add your \n"
            "channel box selection from the scene.\n\n"
            "Example:\n\n"
            "arm:L controlPanel stretch 1\nspine:M controlPanel globalVolume 0.8\nleg:L controlPanel primaryBendyVis 1\n\n"
            "*The 'rebuildTools_buildScript' build script should be applied in the rig's \n"
            "Hive UI > Global Rig Settings (cog icon); this is auto-added on `Save To Scene`.")
        tooltip = placeholderText

        self.setDefaultAttrText = elements.TextEdit(toolTip=tooltip, placeholderText=placeholderText, minimumHeight=240,
                                                    maximumHeight=240)

        # Resizer widget ----------------------------------
        self.resizerAttrWidget = ToolsetResizer(parent=self,
                                                toolsetWidget=self.toolsetWidget,
                                                target=self.setDefaultAttrText,
                                                margins=(0, 3, 0, 10))
        # Search Replace Widget -----------------------
        tooltip = ("Search and replace the text area for specific words.\n\n"
                   "Useful when component names change and need updating.")
        self.searchDefaultAttrTxt = elements.StringEdit(parent=self, label="", editPlaceholder="Search Text",
                                                        labelRatio=1,
                                                        editRatio=2, toolTip=tooltip)
        self.replaceDefaultAttrTxt = elements.StringEdit(parent=self, label="", editPlaceholder="Replace Text",
                                                         labelRatio=1, editRatio=2, toolTip=tooltip)
        self.searchReplaceBtn = elements.styledButton("",
                                                      icon="cgrigRenamer",
                                                      toolTip=tooltip,
                                                      style=uic.BTN_DEFAULT)

        # Apply Symmetry Radio Button -----------------------
        radioNameList = ["Don't Auto-Apply Symmetry", "Auto-Apply Symmetry"]
        radioToolTipList = ["Do not automatically apply symmetry to opposite Hive components. \n"
                            "Only on used while setting values, ie rebuilds",
                            "Automatically apply symmetry to opposite component attributes arm:L to arm:R. \n"
                            "Only on used while setting values, ie rebuilds"]
        self.attrsApplySymRadio = elements.RadioButtonGroup(radioList=radioNameList, toolTipList=radioToolTipList,
                                                            default=1, parent=parent,
                                                            margins=(uic.REGPAD, 0, 0, uic.REGPAD))

        # Add Channel Box Selection ---------------------------------------
        tooltip = ("- Add From Channel Box: \n"
                   "Select object/s and channel box attributes in the channel box to add. \n"
                   "Adds the selected attributes to the text edit with Hive IDs. \n"
                   "If no channel box selection then all attributes will be added.\n\n"
                   "- Add From Auto-Detect: \n"
                   "Adds from channel box or the object, but instead filters only the attributes that have \n"
                   "changed from their default values.")
        self.addAttrsBtn = elements.styledButton("Add From Channel Box Selection",
                                                 icon="plusHollow",
                                                 toolTip=tooltip,
                                                 style=uic.BTN_DEFAULT)
        # Reorder ---------------------------------------
        tooltip = ("Alphabetically sort the current text in the text edit.\n"
                   "Removes missing lines.")
        self.reorderAttrsBtn = elements.styledButton("Sort",
                                                     icon="menu_list",
                                                     toolTip=tooltip,
                                                     style=uic.BTN_DEFAULT)
        # Save ---------------------------------------
        tooltip = ("Save the current text to the scene or disk. \n"
                   "*Data must be saved to the scene for the Hive Rebuilds.\n\n"
                   "Use `Save To Scene` for automatic Hive Rig rebuilds. \n"
                   "The `rebuildTools_buildScript` is automatically applied \n"
                   "to the Hive rig's settings in the \n"
                   "Hive UI > Global Rig Settings (cog icon). \n\n"
                   "`Save To Scene` data is saved to the node named `cgrigHiveAttrData`. ")
        self.saveAttrsBtn = elements.styledButton("",
                                                  icon="save",
                                                  toolTip=tooltip,
                                                  style=uic.BTN_DEFAULT)
        # Load ---------------------------------------
        tooltip = ("Load to the UI from the scene or from disk (JSON). \n\n"
                   "Scene data is loaded from the node named `cgrigHiveAttrData` if it exists.")
        self.loadAttrsBtn = elements.styledButton("",
                                                  icon="openFolder01",
                                                  toolTip=tooltip,
                                                  style=uic.BTN_DEFAULT)

        # Delete Btn ---------------------------------------
        tooltip = ("Clear the text or delete the current settings from the scene. \n\n"
                   "If the scene data is deleted the node named `cgrigHiveAttrData` will be deleted. ")
        self.delAttrsBtn = elements.styledButton("",
                                                 icon="trash",
                                                 toolTip=tooltip,
                                                 style=uic.BTN_DEFAULT)
        # Validate Current Values ---------------------------------------
        tooltip = ("Validate the current values.  (Opens the script editor) \n\n"
                   "Use this to check the current values against the default values in the scene. ")
        self.validateAttrsBtn = elements.styledButton("Validate Current Values",
                                                      icon="checkList",
                                                      toolTip=tooltip,
                                                      style=uic.BTN_DEFAULT)
        # Set Default Values ---------------------------------------
        tooltip = ("Sets the current text data as the default values on the current rig. \n\n"
                   "Default attributes will be changed to match the data in the text edit. ")
        self.setDefaultAttrsBtn = elements.styledButton("Set Default Values From Text",
                                                        icon="hammer",
                                                        toolTip=tooltip,
                                                        style=uic.BTN_DEFAULT)

        # -----------------------------
        #  CGRIG SELECTION SETS
        # -----------------------------

        # Default Attr Title ---------------------------------------
        self.cgrigSetsTitle = elements.LabelDivider("Keep Custom Selection Sets")
        # Text Edit ---------------------------------------
        placeholderText = ("Add `parent selection sets` to recreate while rebuilding Hive rigs. \n\n"
                           "Select sets in the scene and use the `Add Parent Sets` button to add/replace data.\n\n"
                           "The top set/s of set hierarchies will keep the entire set hierarchy/children. \n\n"
                           "Data must be saved to the scene for Hive rig rebuilds. \n\n"
                           "*The `rebuildTools_buildScript` in: \n"
                           "Hive UI > Global Rig Settings (cog) icon is auto-added on `Save To Scene`.")
        tooltip = placeholderText
        self.cgrigSetsText = elements.TextEdit(toolTip=tooltip, placeholderText=placeholderText, minimumHeight=240,
                                             maximumHeight=240)
        # Resizer widget ----------------------------------
        self.resizerSetsWidget = ToolsetResizer(parent=self,
                                                toolsetWidget=self.toolsetWidget,
                                                target=self.cgrigSetsText,
                                                margins=(0, 3, 0, 10))
        # Add Selected Sets Btn ----------------------------------
        toolTip = ("Select selection set/s in the scene and click to add to the text edit. \n"
                   "Only top parent sets of set hierarchies need to be selected.\n"
                   "All children sets will be added to the set data.")
        self.addSetsBtn = elements.styledButton("Add Parent Sets From Sel",
                                                icon="cursorSelect",
                                                toolTip=toolTip,
                                                style=uic.BTN_DEFAULT)
        # Add Selected Sets Btn ----------------------------------
        toolTip = ("Search the scene for saved data and loads to the UI if found. \n"
                   "Data is stored on the node named `cgrigSelectionSetsData`.")
        self.addSetsSceneSavedBtn = elements.styledButton("Add From Scene Saved",
                                                          icon="checkList",
                                                          toolTip=toolTip,
                                                          style=uic.BTN_DEFAULT)
        # Open Sets Btn ----------------------------------
        toolTip = ("Opens the CgRig Tools Selection Sets UI. \n"
                   "Use this UI to manage settings including marking menu icons and more. ")
        self.openCgRigSetsBtn = elements.styledButton("Open CgRig Sel Sets",
                                                    icon="windowBrowser",
                                                    toolTip=toolTip,
                                                    style=uic.BTN_DEFAULT)
        # Delete Btn ---------------------------------------
        tooltip = ("Clear the text or delete the current settings from the scene. \n\n"
                   "If the scene data is deleted the node named `cgrigSelectionSetsData` will be deleted. ")
        self.delSetsBtn = elements.styledButton("",
                                                icon="trash",
                                                toolTip=tooltip,
                                                style=uic.BTN_DEFAULT)
        # Create Sets Btn ----------------------------------
        toolTip = "Creates `selection sets` in the current scene from the text data in the UI. \n" \
                  "Existing selection sets will be recreated/updated."
        self.createCgRigSetsBtn = elements.styledButton("Create Sel Sets",
                                                      icon="sets",
                                                      toolTip=toolTip,
                                                      style=uic.BTN_DEFAULT)
        # Save Selected Sets Btn ----------------------------------
        toolTip = ("Saves the selected selection set and its hierarchy to: \n\n"
                   "- the current scene. \n"
                   "or\n"
                   "- a file on disk\n\n"
                   "Use `Save To Scene` for automatic Hive Rig rebuilds. \n"
                   "The `rebuildTools_buildScript` is automatically applied \n"
                   "to the Hive rig's settings in the \n"
                   "Hive UI > Global Rig Settings (cog icon). \n\n"
                   "`Save To Scene` data is saved to a node named `cgrigSelectionSetsData`")

        self.saveSelectionSetsBtn = elements.styledButton("",
                                                          icon="save",
                                                          toolTip=toolTip,
                                                          style=uic.BTN_DEFAULT)
        # Load Selected Sets Btn ----------------------------------
        toolTip = "Loads `selection set` data into the UI from: \n\n" \
                  "- the current scene. \n" \
                  "or\n" \
                  "- a file on disk\n\n" \
                  "Note: Scene data is loaded from a node named `cgrigSelectionSetsData`"
        self.loadSelectionSetsBtn = elements.styledButton("",
                                                          icon="openFolder01",
                                                          toolTip=toolTip,
                                                          style=uic.BTN_DEFAULT)
        # Rebuild Divider ----------------------------------
        self.rebuildDivider = elements.LabelDivider("Rebuild Hive Rig")
        # Rig combo ---------------------------------------
        toolTip = "Select the Hive rig from the scene to export. \n" \
                  "No rigs will appear if there are no valid Hive rigs in the scene."
        self.rigListCombo = elements.ComboBoxRegular("Hive Rig",
                                                     items=[],
                                                     parent=parent,
                                                     labelRatio=1,
                                                     boxRatio=5,
                                                     toolTip=toolTip)
        # Rebuild Rig Btn ----------------------------------
        toolTip = "Rebuilds the Hive rig back to its current state:\n\n" \
                  "- Pre Rig (Pre Rig > Guides > Pre-Rig)\n" \
                  "or\n" \
                  "- Polish (Polish > Guides > Polish)\n\n" \
                  "*Save the data to the scene in each `tool mode` before rebuilding. \n\n" \
                  "Right-click for more options."
        self.rebuildRigBtn = elements.styledButton("Rebuild Hive Rig (right-click)",
                                                   icon="hammer",
                                                   toolTip=toolTip,
                                                   style=uic.BTN_DEFAULT)
        # Reload CgRig Tools ----------------------------------
        toolTip = ("Reload CgRig Tools Pro if you are making code changes to Build Scripts on disk. \n\n"
                   "*Note all CgRig UIs will be closed and will need to reopened. ")
        self.reloadCgRigBtn = elements.styledButton("Reload CgRig Tools",
                                                  icon="cgrig_reload",
                                                  toolTip=toolTip,
                                                  style=uic.BTN_DEFAULT)
        # Open Hive UI Btn ----------------------------------
        toolTip = "Open the Hive UI"
        self.openHiveUIBtn = elements.styledButton("",
                                                   icon="hive",
                                                   toolTip=toolTip,
                                                   style=uic.BTN_DEFAULT)


class GuiCompact(GuiWidgets):
    def __init__(self, parent=None, properties=None, uiMode=UI_MODE_COMPACT, toolsetWidget=None):
        """Adds the layout building the compact version of the GUI:

            default uiMode - 0 is advanced (UI_MODE_COMPACT)

        :param parent: the parent of this widget
        :type parent: QtWidgets.QWidget
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: cgrig.apps.toolsetsui.widgets.toolsetwidget.PropertiesDict
        """
        super(GuiCompact, self).__init__(parent=parent, properties=properties, uiMode=uiMode,
                                         toolsetWidget=toolsetWidget)
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(self,
                                         margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)

        modeLayout = elements.hBoxLayout(spacing=uic.SLRG, margins=(uic.REGPAD, 0, uic.REGPAD, 0))
        modeLayout.addWidget(self.toolModeCombo, 1)

        rigLayout = elements.hBoxLayout(spacing=uic.SLRG, margins=(uic.REGPAD, 0, uic.REGPAD, 0))
        rigLayout.addWidget(self.rigListCombo, 1)

        # TOOL MODE AND RIG COMBO
        searchReplaceAttrLayout = elements.hBoxLayout(spacing=uic.SREG,
                                                      margins=(0, 0, 0, 0))
        searchReplaceAttrLayout.addWidget(self.searchDefaultAttrTxt, 10)
        searchReplaceAttrLayout.addWidget(self.replaceDefaultAttrTxt, 10)
        searchReplaceAttrLayout.addWidget(self.searchReplaceBtn, 1)

        btnLayout = elements.hBoxLayout(margins=(0, 0, 0, 0), spacing=uic.SPACING)
        btnLayout.addWidget(self.addAttrsBtn, 20)
        btnLayout.addWidget(self.reorderAttrsBtn, 6)
        btnLayout.addWidget(self.saveAttrsBtn, 1)
        btnLayout.addWidget(self.loadAttrsBtn, 1)
        btnLayout.addWidget(self.delAttrsBtn, 1)

        botButtonLayout = elements.hBoxLayout(margins=(0, 0, 0, 0), spacing=uic.SPACING)
        botButtonLayout.addWidget(self.validateAttrsBtn, 1)
        botButtonLayout.addWidget(self.setDefaultAttrsBtn, 1)

        btnVerticalLayout = elements.vBoxLayout(margins=(0, 0, 0, 0), spacing=uic.SPACING)
        btnVerticalLayout.addLayout(btnLayout)
        btnVerticalLayout.addLayout(botButtonLayout)

        self.defaultAttrWidgets = [self.defaultAttrTitle, self.setDefaultAttrText, self.resizerAttrWidget,
                                   self.addAttrsBtn, self.reorderAttrsBtn, self.saveAttrsBtn, self.loadAttrsBtn,
                                   self.delAttrsBtn, self.validateAttrsBtn, self.setDefaultAttrsBtn,
                                   self.attrsApplySymRadio, self.searchDefaultAttrTxt, self.replaceDefaultAttrTxt,
                                   self.searchReplaceBtn]

        # CGRIG SELECTION SETS
        cgrigSetsBtnLayout1 = elements.hBoxLayout(spacing=uic.SPACING, margins=(0, 0, 0, 0))
        cgrigSetsBtnLayout1.addWidget(self.addSetsBtn, 10)
        cgrigSetsBtnLayout1.addWidget(self.addSetsSceneSavedBtn, 10)

        cgrigSetsBtnLayout2 = elements.hBoxLayout(spacing=uic.SPACING, margins=(0, 0, 0, 0))
        cgrigSetsBtnLayout2.addWidget(self.createCgRigSetsBtn, 10)
        cgrigSetsBtnLayout2.addWidget(self.openCgRigSetsBtn, 10)
        cgrigSetsBtnLayout2.addWidget(self.saveSelectionSetsBtn, 1)
        cgrigSetsBtnLayout2.addWidget(self.loadSelectionSetsBtn, 1)
        cgrigSetsBtnLayout2.addWidget(self.delSetsBtn, 1)

        cgrigSetsBtnLayout = elements.vBoxLayout(spacing=uic.SPACING, margins=(0, 0, 0, 0))
        cgrigSetsBtnLayout.addLayout(cgrigSetsBtnLayout1)
        cgrigSetsBtnLayout.addLayout(cgrigSetsBtnLayout2)

        rebuildLayout = elements.hBoxLayout(spacing=uic.SPACING, margins=(0, 0, 0, 0))
        rebuildLayout.addWidget(self.rebuildRigBtn, 20)
        rebuildLayout.addWidget(self.reloadCgRigBtn, 12)
        rebuildLayout.addWidget(self.openHiveUIBtn, 1)

        self.cgrigSetsWidgets = [self.addSetsBtn, self.openCgRigSetsBtn, self.saveSelectionSetsBtn,
                               self.loadSelectionSetsBtn, self.cgrigSetsTitle, self.cgrigSetsText,
                               self.resizerSetsWidget, self.createCgRigSetsBtn, self.delSetsBtn,
                               self.addSetsSceneSavedBtn]

        # Add To Main Layout ---------------------------------------
        # TOOL MODE AND RIG COMBO
        mainLayout.addLayout(modeLayout)

        # OVERRIDE DEFAULT ATTRIBUTES VALUES
        mainLayout.addWidget(self.defaultAttrTitle)
        mainLayout.addWidget(self.setDefaultAttrText)
        mainLayout.addLayout(searchReplaceAttrLayout)
        mainLayout.addWidget(self.resizerAttrWidget)
        mainLayout.addWidget(self.attrsApplySymRadio)
        mainLayout.addLayout(btnVerticalLayout)

        # CGRIG SELECTION SETS
        mainLayout.addWidget(self.cgrigSetsTitle)
        mainLayout.addWidget(self.cgrigSetsText)
        mainLayout.addWidget(self.resizerSetsWidget)
        mainLayout.addLayout(cgrigSetsBtnLayout)

        # REBUILD RIG
        mainLayout.addWidget(self.rebuildDivider)
        mainLayout.addLayout(rigLayout)
        mainLayout.addLayout(rebuildLayout)

    def updateRigs(self, rigNames):
        oldPropertyValue = self.rigListCombo.currentText()
        self.rigListCombo.clear()
        self.rigListCombo.addItems(rigNames)
        self.rigListCombo.setToText(oldPropertyValue)

    def setCurrentRig(self, rigName):
        self.rigListCombo.setToText(rigName)


class GuiAdvanced(GuiWidgets):
    def __init__(self, parent=None, properties=None, uiMode=UI_MODE_ADVANCED, toolsetWidget=None):
        """Adds the layout building the advanced version of the GUI:

            default uiMode - 1 is advanced (UI_MODE_ADVANCED)

        :param parent: the parent of this widget
        :type parent: QtWidgets.QWidget
        :param properties: the properties dictionary which tracks all the properties of each widget for UI modes
        :type properties: cgrig.apps.toolsetsui.widgets.toolsetwidget.PropertiesDict
        """
        super(GuiAdvanced, self).__init__(parent=parent, properties=properties, uiMode=uiMode,
                                          toolsetWidget=toolsetWidget)
        # Main Layout ---------------------------------------
        mainLayout = elements.vBoxLayout(self,
                                         margins=(uic.WINSIDEPAD, uic.WINBOTPAD, uic.WINSIDEPAD, uic.WINBOTPAD),
                                         spacing=uic.SREG)
        # Add To Main Layout ---------------------------------------
