"""
Serialize the difference for storing into the scene
resolve into scene component labels
"""
__all__ = [
    "SpaceSwitchDefinition",
    "SpaceSwitchDriverDefinition",
    "mergeAttributesWithSpaceSwitches",
    "spaceSwitchDefToScene",
    "componentToAttrExpression"
]

import copy
import logging

from collections import OrderedDict

from cgrig.libs.utils import general
from cgrig.libs.hive.base.definition import exprutils, definitionattrs
from cgrig.libs.hive.base import errors
from cgrig.libs.maya.api import attrtypes

logger = logging.getLogger(__name__)


class SpaceSwitchPanelFilterGroup(object):
    def __init__(self, label, name, insertAfter):
        self.label = label
        self.name = name
        self.insertAfter = insertAfter

    def serialize(self):
        return {
            "label": self.label,
            "name": self.name,
            "insertAfter": self.insertAfter,
        }


class SpaceSwitchPanelFilter(object):
    @classmethod
    def deserialize(cls, data):
        group = data.get("group", {})
        return cls(
            data.get("default", ""),
            SpaceSwitchPanelFilterGroup(
                group.get("label", ""),
                group.get("name", ""),
                group.get("insertAfter", ""),
            ),
            data.get("insertAfter", ""),
        )

    def __init__(self, default, group, insertAfter):
        self.default = default
        self.group = group
        self.insertAfter = insertAfter

    def serialize(self):
        return {
            "default": self.default,
            "group": self.group.serialize(),
            "insertAfter": self.insertAfter,
        }


class SpaceSwitchPermissions(object):
    @classmethod
    def deserialize(cls, data):
        return cls(data.get("allowRename", True),
                   data.get("allowDriverChange", True),
                   data.get("value", False))

    def __init__(self, allowRename=True, allowDriverChange=True, value=False):
        self.allowRename = allowRename
        self.allowDriverChange = allowDriverChange
        self.value = value

    def serialize(self):
        return {
            "allowRename": self.allowRename,
            "allowDriverChange": self.allowDriverChange,
            "value": self.value
        }


class SpaceSwitchDefinition(object):
    """A class representing the raw form of a single space switch.

    :param data: The data for the space switch definition.
    :type data: dict

    .. code-block:: json

        {
                "label": "ikSpace",
                "driven": "endik",
                "type": "parent",
                "controlPanelFilter": {
                    "group": {
                        "name": "__",
                        "label": "Space",
                        "insertAfter": "lock"
                    },
                    "default": "world"
                },
                "permissions": {
                    "value": true,
                    "allowRename": false
                },
                "drivers": [
                    {
                        "label": "parent",
                        "driver": "@{self.inputLayer.upr}",
                        "permissions": {
                            "value": true,
                            "allowRename": false,
                            "allowDriverChange": false,
                        }
                    }

                ]
        }
    """

    def __init__(self, data):
        super(SpaceSwitchDefinition, self).__init__()
        self.type = data.get("type", "")
        self._label = data.get("label", "")
        self.driven = data.get("driven", "")
        self._active = data.get("active", True)
        self._controlPanelFilter = SpaceSwitchPanelFilter.deserialize(data.get("controlPanelFilter", {}))
        self._permissions = SpaceSwitchPermissions.deserialize(data.get("permissions", {}))
        self._drivers = []

        for driver in data.get("drivers", []):
            self._drivers.append(SpaceSwitchDriverDefinition(driver))

    @property
    def isProtected(self):
        """Get the protection state of the space switch.

        :return: Whether the space switch is protected or not.
        :rtype: bool
        """
        return self._permissions.value

    @isProtected.setter
    def isProtected(self, state):
        """Set the protection state of the space switch.

        :param state: The protection state to set.
        :type state: bool
        """
        self._permissions.value = state

    @property
    def renameAllowed(self):
        """Get whether renaming the space switch is allowed.

        :return: Whether renaming the space switch is allowed or not.
        :rtype: bool
        """
        return self._permissions.allowRename

    @renameAllowed.setter
    def renameAllowed(self, state):
        """Set whether renaming the space switch is allowed.

        :param state: The allowed state to set.
        :type state: bool
        """
        self._permissions.allowRename = state

    @property
    def label(self):
        """Get the label of the space switch.

       :return: The label of the space switch.
       :rtype: str
       """
        return self._label

    @label.setter
    def label(self, value):
        """Set the label of the space switch driver.

        :param value: The label to set.
        :type value: str
        :raise ValueError: If renaming the label is protected.
        """
        if not self.renameAllowed:
            raise ValueError("Renaming the label is protected for: {}".format(self._label))
        self._label = value

    @property
    def controlPanelFilter(self):
        """Get the control panel filter of the space switch driver.

        :return: The control panel filter of the space switch driver.
        :rtype: :class:`SpaceSwitchPanelFilter`
        """
        return self._controlPanelFilter

    @controlPanelFilter.setter
    def controlPanelFilter(self, panelFilter):
        """Set the control panel filter of the space switch driver.

        :param panelFilter: The control panel filter to set.
        :type panelFilter: dict
        """
        self._controlPanelFilter = SpaceSwitchPanelFilter.deserialize(panelFilter)

    @property
    def active(self):
        """Get the active state of the space switch driver.

        :return: The active state of the space switch driver.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, value):
        """Set the active state of the space switch driver.

        :param value: The active state to set.
        :type value: bool
        """
        self._active = value

    @property
    def defaultDriver(self):
        """Get the default driver of the space switch.

        :return: The label of the default driver.
        :rtype: str
        """
        default = self._controlPanelFilter.default
        if default:
            return default
        drivers = self._drivers
        if drivers:
            return drivers[0].label
        return ""

    @defaultDriver.setter
    def defaultDriver(self, driverLabel):
        """Set the default driver of the space switch.

        :param driverLabel: The label of the driver to set as default.
        :type driverLabel: str
        """
        if not self.hasDriver(driverLabel):
            return
        self._controlPanelFilter.default = str(driverLabel)

    @property
    def drivers(self):
        """

        :return:
        :rtype: list[:class:`SpaceSwitchDriverDefinition`]
        """
        return self._drivers

    @drivers.setter
    def drivers(self, drivers):
        self._drivers = drivers

    def createDriver(self, driverInfo):
        """Create a new driver for the space switch.

        :param driverInfo: The information for the new driver.
        :type driverInfo: dict
        :raise ValueError: If the space switch already has a driver with the same label.
        :return: The newly created driver.
        :rtype: :class:`SpaceSwitchDriverDefinition`
        """
        if self.hasDriver(driverInfo["label"]):
            raise ValueError("Already contains driver: {}".format(driverInfo))
        driver = SpaceSwitchDriverDefinition(driverInfo)
        self._drivers.append(driver)
        return driver

    def removeDriver(self, driverLabel):
        """Remove a driver from the space switch.

        :param driverLabel: The label of the driver to remove.
        :type driverLabel: str
        :raise ValueError: If deleting the driver is not allowed.
        """
        for index, driver in enumerate(self._drivers):
            if driver.label != driverLabel:
                logger.debug("No Driver by the name: {}".format(driverLabel))
                continue
            if driver.isProtected:
                raise ValueError("Deleting driver '{}' not allowed".format(driverLabel))
            del self._drivers[index]
            break

    def hasDriver(self, driverLabel):
        """Check if the space switch has a driver with the given label.

        :param driverLabel: The label of the driver to check for.
        :type driverLabel: str
        :return: Whether the space switch has a driver with the given label or not.
        :rtype: bool
        """
        for index, driver in enumerate(self._drivers):
            if driver.label == driverLabel:
                return True
        return False

    def driver(self, driverLabel):
        """Get the driver with the given label.

        :param driverLabel: The label of the driver to get.
        :type driverLabel: str
        :return: The driver with the given label.
        :rtype: :class:`SpaceSwitchDriverDefinition`
        """
        for index, driver in enumerate(self._drivers):
            if driver.label == driverLabel:
                return driver

    def clearDrivers(self):
        """Remove all drivers from the space switch.

        :raise ValueError: If deleting any of the drivers is not allowed.
        """
        if any(d.isProtected for d in self._drivers):
            raise ValueError("Drivers can't be deleted")
        self._drivers = []

    def difference(self, otherDef):
        """Serializes the changes between the current definition and the `otherDef` skipping
        any drivers which are read only or spaces that have not changed.

        :param otherDef: The Base or original spaceSwitch coming from the base component.
        :type otherDef: :class:`SpaceSwitchDefinition`
        :return:
        :rtype: :class:`SpaceSwitchDefinition` or None
        """
        if not otherDef:
            return self
        if self == otherDef:
            return
        otherDrivers = OrderedDict([[i.label, i] for i in otherDef.drivers])
        otherDriverLabels = list(otherDrivers.keys())
        selfDriverLabels = [i.label for i in self.drivers]

        # if the ordering is different then we serialize everything but only keep the label key for any protected
        # drivers.
        differentOrder = False
        if not otherDriverLabels:
            return

        # check ordering
        if otherDriverLabels != selfDriverLabels:
            differentOrder = True

        serializedData = SpaceSwitchDefinition(self.serialize())
        drivers = []
        for index, driver in enumerate(serializedData.drivers):
            if driver.isProtected and differentOrder:
                drivers.append(SpaceSwitchDriverDefinition({"label": driver.label}))
                continue
            # if the driver is protected and doesn't support renaming then we expect it to be
            # a default driver
            if driver.isProtected and not driver.renameAllowed:
                continue
            drivers.append(driver)
        if not drivers and serializedData.defaultDriver == otherDef.defaultDriver:
            return
        if drivers:
            serializedData.drivers = drivers
        serializedData.defaultDriver = otherDef.defaultDriver

        return serializedData

    def serialize(self):
        return {
            "type": self.type,
            "label": self._label,
            "driven": self.driven,
            "active": self._active,
            "controlPanelFilter": self._controlPanelFilter.serialize(),
            "permissions": self._permissions.serialize(),
            "drivers": [dict(i) for i in self.drivers]
        }


class SpaceSwitchDriverDefinition(general.ObjectDict):
    """Representation of a single space switch driver.

    .. code-block:: json

         {
            "label": "parent",
            "driver": "@{self.inputLayer.upr}",
            "permissions": {"allowsDeletion": true, "allowRename": true}
        }

    """

    @property
    def driver(self):
        """Get the driver value.

        :return: The driver value.
        :rtype: str
        """
        _driver = self.get("driver")
        return _driver or ""

    @driver.setter
    def driver(self, value):
        """Set the driver value.

        :param value: The driver value to set.
        :type value: str
        :raise ValueError: If changing the driver is not allowed.
        """
        if not self.driverChangeAllowed:
            raise ValueError("Unable to change a protected driver!.")
        self["driver"] = value

    @property
    def isProtected(self):
        """Get whether the space switch driver is protected or not.

        :return: Whether the space switch driver is protected or not.
        :rtype: bool
        """
        return self.get("permissions", {}).get("value", False)

    @isProtected.setter
    def isProtected(self, state):
        """Set whether the space switch driver is protected or not.

        :param state: The protected state to set.
        :type state: bool
        """
        self.get("permissions", {})["value"] = state

    @property
    def renameAllowed(self):
        """Get whether renaming the space switch driver is allowed or not.

        :return: Whether renaming the space switch driver is allowed or not.
        :rtype: bool
        """
        return self.get("permissions", {}).get("allowRename", True)

    @renameAllowed.setter
    def renameAllowed(self, state):
        """Set whether renaming the space switch driver is allowed or not.

        :param state: The allowed state to set.
        :type state: bool
        """
        self.get("permissions", {})["allowRename"] = state

    @property
    def driverChangeAllowed(self):
        """Get whether changing the driver value is allowed or not.

        :return: Whether changing the driver value is allowed or not.
        :rtype: bool
        """
        return self.get("permissions", {}).get("allowDriverChange", True)

    @driverChangeAllowed.setter
    def driverChangeAllowed(self, state):
        """Set whether changing the driver value is allowed or not.

        :param state: The allowed state to set.
        :type state: bool
        """
        self.get("permissions", {})["allowDriverChange"] = state

    @property
    def label(self):
        """Get the label of the space switch driver.

        :return: The label of the space switch driver.
        :rtype: str
        """
        return self["label"]

    @label.setter
    def label(self, value):
        """Set the label of the space switch driver.

        :param value: The label to set.
        :type value: str
        :raise ValueError: If renaming the label is protected.
        """
        if not self.renameAllowed:
            raise ValueError("Renaming the label is protected for: {}".format(self.label))
        self["label"] = value


def componentToAttrExpression(driver, component):
    """Returns the fully qualified attribute expression for the component.

    The Attribute expression returned will be similar to the below:

        "@{component:componentName}" or "@{self}"

    .. note:
        The driver and component and the same then the name will become "self".

    :param driver: The driver component, it may be the same as the provided component to return it as "self"
    :type driver: :class:`cgrig.libs.hive.base.base.component.Component` or :class:`cgrig.libs.maya.zapi.base.DGNode`
    :param component:
    :type component: :class:`cgrig.libs.hive.base.base.component.Component`
    :return: The formatted expression for the component
    :rtype: str
    """
    if driver == component:
        return exprutils.pathAsDefExpression(("self",))
    return exprutils.pathAsDefExpression((":".join((component.name(), component.side())),))


def spaceSwitchDefToScene(rig, component, spaceSwitch):
    """Translates The space switching definition to scene nodes i.e. hive nodes.

    The returns value will be in same form as the spaceSwitch but with the driven and driver fields
    Replace with the scene node instances.

    :param rig: The Hive rig Instance.
    :type rig: :class:`cgrig.libs.hive.base.rig.Rig`
    :param component: The Hive component Instance this space switch belongs too.
    :type component: :class:`cgrig.libs.hive.base.component.Component`
    :param spaceSwitch:
    :type spaceSwitch: :class:`SpaceSwitchDefinition`
    :return: The Returned structure will be in the same form as the provided space switch.
    :rtype: :class:`SpaceSwitchDefinition`
    """
    # Create a copy because we remap driver state to scene nodes which we don't want to mess with the raw
    returnData = copy.deepcopy(spaceSwitch)
    drivenExpr = spaceSwitch.driven
    _, drivenNode = exprutils.attributeRefToSceneNode(rig, component, drivenExpr)
    returnData.driven = drivenNode
    # early out here with the driven node set to None on the spaceswitch for checking results in client code.
    if drivenNode is None:
        return returnData
    drivers = []
    for driver in returnData.drivers:
        driverName = driver.driver
        driverNode = None
        if driverName:
            try:
                comp, driverNode = exprutils.attributeRefToSceneNode(rig, component, driverName)
            except errors.InvalidDefinitionAttrExpression:
                logger.warning("Invalid space Switch: {}, Driver: {}".format(spaceSwitch.label, driverName))
                continue
        driver["driver"] = driverNode
        drivers.append(driver)
    returnData.drivers = drivers
    return returnData


def mergeAttributesWithSpaceSwitches(attributes, spaceSwitches, excludeActive=True):
    """Function which merges the space switching definitions with the attribute list ensure only those
    that don't already exist are created.
    Used by the component when constructing the rig controlPanel.

    :param attributes: Existing Control Panel definition attributes.
    :type attributes: list[:class:`definitionattrs.AttributeDefinition`]
    :param spaceSwitches: The list of spaceswitches for the component for merge
    :type spaceSwitches: list[:class:`SpaceSwitchDefinition`]
    :param excludeActive: Whether the spaceSwitches which are set to active should be merged
    """
    currentAttrs = OrderedDict((i.name, i) for i in attributes)
    currentAttrLabels = list(currentAttrs.keys())  # used for reordering while currentAttrs provides lookup
    outAttributes = list(currentAttrs.values())
    previousAttrLabel = currentAttrLabels[-1] if currentAttrLabels else ""
    # cache the enum attribute definition class type for both the group and space.
    spaceAttrType = definitionattrs.attributeClassForType(attrtypes.kMFnkEnumAttribute)

    # label, group, insert
    for space in spaceSwitches:
        spaceAttrName = space.label
        existingSpaceAttr = currentAttrs.get(spaceAttrName)
        # ignore inActive spaces and purge any existing space attribute if needed
        if excludeActive and not space.active:
            for index, attr in enumerate(outAttributes):
                if attr.name == spaceAttrName:
                    del outAttributes[index]
                    break
            previousAttrLabel = spaceAttrName
            continue
        assert (spaceAttrName)
        panelFilter = space.controlPanelFilter
        group = panelFilter.group
        driverLabels = [i.label for i in space.drivers]
        try:
            defaultIndex = driverLabels.index(panelFilter.default)
        except ValueError:
            defaultIndex = 0
        # existing space switch attribute in the definition so update the enums and default
        if existingSpaceAttr is not None:
            existingSpaceAttr["enums"] = driverLabels
            existingSpaceAttr["default"] = defaultIndex
            outAttributes.insert(currentAttrLabels.index(spaceAttrName), existingSpaceAttr)
            previousAttrLabel = spaceAttrName
            continue

        # no existing space so let's create and insert into the right spot
        # search for the space group attribute name which likely just got added in a previous loop
        currentGroupAttr = currentAttrs.get(group.name)
        if not currentGroupAttr and group.name:
            # create a new group attribute
            currentGroupAttr = spaceAttrType(name=group.name,
                                             Type=attrtypes.kMFnkEnumAttribute,
                                             enums=[group.label],
                                             keyable=False,
                                             channelBox=True,
                                             locked=True)
            # figure out 2 insert indices, one for the group and one for the new attribute which will be created.
            groupInsertAfter = group.insertAfter if group.insertAfter else previousAttrLabel
            try:
                existingAttrIndex = currentAttrLabels.index(groupInsertAfter)
            except ValueError:
                existingAttrIndex = len(currentAttrLabels)

            currentAttrs[currentGroupAttr.name] = currentGroupAttr
            # new attribute index which is one below the group hence +2
            insertIndex = existingAttrIndex + 2
            # insert the new group attribute
            currentAttrLabels.insert(existingAttrIndex + 1, currentGroupAttr.name)
            outAttributes.insert(existingAttrIndex + 1, currentGroupAttr)
        else:
            insertAfter = panelFilter.insertAfter or previousAttrLabel  # handle None and ""
            try:
                insertIndex = currentAttrLabels.index(insertAfter) + 1
            except ValueError:
                insertIndex = -1

        # now handle the creation of the attribute and insert it into the attribute list.
        spaceAttr = spaceAttrType(name=spaceAttrName,
                                  Type=attrtypes.kMFnkEnumAttribute,
                                  default=defaultIndex,
                                  enums=driverLabels,
                                  keyable=True,
                                  channelBox=False)

        currentAttrLabels.insert(insertIndex, spaceAttr.name)
        currentAttrs[spaceAttr.name] = spaceAttr
        previousAttrLabel = spaceAttr.name
        outAttributes.insert(insertIndex, spaceAttr)
    attributes[:] = outAttributes[:]
