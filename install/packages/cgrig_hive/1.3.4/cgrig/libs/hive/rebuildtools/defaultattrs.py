"""Module for setting default attribute overrides for Hive rigs in Maya.

Example use:

.. code-block:: python

    from cgrig.libs.hive.rebuildtools import defaultattrs
    data = defaultattrs.get_channel_attrs_proxy_sel_string(rootOfProxies=True, longNames=False)
    print(data)

.. code-block:: python

    from cgrig.libs.hive.rebuildtools import defaultattrs
    rig = defaultattrs.defaultRig()
    dataString = "cheek:L controlPanel cheekMultiplierZX 1.0\ncheek:L controlPanel cheekMultiplierXY 0.0"
    defaultattrs.set_string_to_defaultAttr(dataString, rig=rig, message=True)


Author: Andrew Silke

"""
import re

from maya import cmds
import maya.mel as mel

from cgrig.libs.maya import zapi
from cgrig.libs.hive import api as hiveapi
from cgrig.libs.hive import constants
from cgrig.libs.hive.base.errors import HiveRigDuplicateRigsError

from cgrig.libs.utils import filesystem

from cgrig.libs.maya.cmds.objutils import attributes

from cgrig.libs.utils import output

HIVE_ATTR_DEFAULT_DATA = "cgrigHiveAttrData"
ATTR_APPLY_SYMMETRY = "applySym"

def rebuildHiveRig(rig=None):
    """Rebuilds the Hive rig by building guides, auto-aligning them, and polishing the rig.

    :param rig: The rig instance to rebuild. If None, the default rig will be used.
    :type rig: :class:`api.Rig`
    :return: True if the rig was successfully rebuilt, False if no rig was found.
    """
    return hiveapi.commands.rebuildHiveRig(rig)


def guidesMode(rig):
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return
    if rig.buildState() == constants.GUIDES_STATE:
        output.displayWarning("Rig is already in Guides Mode.")
        return
    hiveapi.commands.showComponents(list(rig.iterComponents()))  # show all components
    hiveapi.commands.buildGuides(rig)


def controlsMode(rig):
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return

    if rig.buildState() == constants.CONTROL_VIS_STATE:
        output.displayWarning("Rig is already in Controls Mode.")
        return
    hiveapi.commands.showComponents(list(rig.iterComponents()))  # show all components
    hiveapi.commands.buildGuideControls(rig)


def skeletonMode(rig):
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return
    if rig.buildState() == constants.SKELETON_STATE:
        output.displayWarning("Rig is already in Skeleton Mode.")
        return
    hiveapi.commands.showComponents(list(rig.iterComponents()))  # show all components
    hiveapi.commands.buildDeform(rig)


def preRigMode(rig):
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return
    if rig.buildState() == constants.RIG_STATE:
        output.displayWarning("Rig is already in PreRig Mode.")
        return
    if rig.buildState() == constants.POLISH_STATE:
        output.displayWarning("Cannot return to Pre-Rig from Polish Mode, please return to Guides mode first.")
        return
    hiveapi.commands.showComponents(list(rig.iterComponents()))  # show all components
    hiveapi.commands.buildRigs(rig)


def polishMode(rig):
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return
    if rig.buildState() == constants.POLISH_STATE:
        output.displayWarning("Rig is already in PreRig Mode.")
        return
    hiveapi.commands.showComponents(list(rig.iterComponents()))  # show all components
    hiveapi.commands.polishRig(rig)


def checkObjectCount(count=40):
    """Checks if the number of selected objects in the scene is less than or equal to a specified count.

    :param count: The maximum number of objects allowed in the selection.
    :type count: int
    :return: True if the number of selected objects is less than or equal to count, False otherwise.
    :rtype: bool
    """
    selObjs = cmds.ls(selection=True)
    if len(selObjs) > count:
        return False
    return True


# -----------------
# GET DATA
# -----------------

def rigNeedsNamespace(rigName):
    """If there are duplicated Hive rig names in the scene return True

    :param rigName: The name of a hive rig eg "cgrig_mannequin"
    :type rigName: str
    :return: If Duplicated rigs return True
    :rtype: bool
    """
    try:
        hiveapi.rootByRigName(rigName, "")
        return False
    except HiveRigDuplicateRigsError:
        return True


def allRigsComboUI():
    """Returns a list of unique rig names usually for UI.  Namespaces are added if needed.

    :return: A list of rigNames and a matching set of rig instances
    :rtype: tuple(list(str), list(:class:`api.Rig`))
    """
    rigNamesCombo = list()
    rigInstances, rigNames, namespaces = allRigsInScene()
    if not rigInstances:
        return list(), list()
    for i, name in enumerate(rigNames):
        if namespaces[i] and rigNeedsNamespace(name):
            if namespaces[i].endswith(":"):
                namespaces[i] = namespaces[i][:-1]  # remove the trailing colon
            if namespaces[i].startswith(":"):
                namespaces[i] = namespaces[i][1:]  # remove the start colon
            rigNamesCombo.append("{}:{}".format(namespaces[i], name))
        else:
            rigNamesCombo.append("{}".format(name))
    return rigNamesCombo, rigInstances


def defaultRig():
    """Returns the default rig instance from the scene's Hive rigs.

    :return: The default rig instance
    :rtype: :class:`api.Rig`
    """
    rigInstances = list(hiveapi.iterSceneRigs())
    if not rigInstances:
        output.displayWarning("No rigs found in the scene.")
        return None
    return rigInstances[0]


def allRigsInScene():
    """Returns a list of rig instances, names and namespaces from the scene's Hive rigs.

    :return: A list of rig instances, names and namespaces
    :rtype: tuple(list(:class:`api.Rig`), list(str), list(str))
    """
    rigNames = list()
    rigNamespaces = list()
    rigInstances = list(hiveapi.iterSceneRigs())
    if not rigInstances:
        return list(), list(), list()
    for rigInstance in rigInstances:
        rigNames.append(rigInstance.name())
        rigNamespaces.append(rigInstance.meta.namespace())
    return rigInstances, rigNames, rigNamespaces


# -----------------
# HIVE NAME PARTS
# -----------------

def isControlPanelOrControl(node):
    """Checks if the selected node is a controlPanel or control node or neither in the Hive rig.

    Returns "controlPanel" if the node is a controlPanel, "control" if it is a control node, or None if neither.

    :param node: The Maya node to check
    :type node: :class:`maya.api.OpenMaya.MObject` or str

    :return: "controlPanel" if the node is a controlPanel, "control" if it is a control node, or None if neither
    :rtype: str or None
    """
    for dest in node.message.destinations():
        name = dest.partialName().rpartition(".")[-1]
        if name == "cgrigSettingNode" and dest.parent().child(1).value() == hiveapi.constants.CONTROL_PANEL_TYPE:
            return "controlPanel"
        elif name == "controlNode":
            return "control"
    return None


def hiveNameParts(node, rig=None):
    """Returns the Hive component, control ID, current side, and opposite side from a node.

    :param node: The Maya node to extract information from
    :type node: :class:`maya.api.OpenMaya.MObject` or str
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`, optional"""
    if rig is None:
        rig = defaultRig()
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return None, None
    # control ID --------------
    type = isControlPanelOrControl(node)
    if type == "control":
        controlId = hiveapi.ControlNode(node.object()).id()
    elif type == "controlPanel":
        controlId = "controlPanel"
    else:  # None
        output.displayWarning("Node {} is not a control or controlPanel node.".format(node))
        return None, None
    # get component ----------------
    component = hiveapi.componentFromNode(node, rig=rig)
    return component, controlId


def get_channelboxAttr_list_proxy_sel(rootOfProxies=True, longNames=False, hasChangedFromDefault=False):
    """Returns a list of channel box attributes for selected proxies, formatted for Hive.

    If the selected object is not a Hive rig component, it will return the object name, attribute name, and value.

    Automatically finds root proxy attributes and rootOfProxies=True returns the object/node of the base proxy.

    The returned list can contain the following formats:
    If Hive [<component>, <id>, <attr>, <val>]
    If not Hive [<objectName>, <attrName>, <value>]

    :param rootOfProxies:  Whether to include root of proxies in the search
    :type rootOfProxies:  bool
    :param longNames: Whether to return long names of attributes
    :type longNames: bool
    :param hasChangedFromDefault: Check if the attr value has changed from the default value, if so keep it
    :type hasChangedFromDefault: bool

    :return: A list of attributes formatted for Hive, where each entry is a list containing
    :rtype: list[list(str, str, str, str)]
    """
    hiveDataList = list()
    dataList = attributes.get_channelbox_attribute_list_proxy_sel(rootOfProxies=rootOfProxies, longNames=longNames)
    if not dataList:
        return hiveDataList
    for attributeData in dataList:
        objStr = attributeData[0]
        attrStr = attributeData[1]
        value = attributeData[2]

        if hasChangedFromDefault:
            # check the default value of the attribute
            defaultValue = cmds.attributeQuery(attrStr, node=objStr, listDefault=True)
            if defaultValue:
                defaultValue = defaultValue[0]
            else:  # strange that it would get here
                continue
            # check if the value matches the default value, if a float check within a tolerance of .0001
            if isinstance(value, float) and isinstance(defaultValue, float):
                if abs(value - defaultValue) < 0.0001:
                    continue  # fail floats match
            elif value == defaultValue:  # if the value is the same as the default value int enum etc
                continue  # fail match

        # get hive ID data from the object
        component, controlId = hiveNameParts(zapi.nodeByName(objStr))
        if not controlId:
            hiveDataList.append(attributeData[0:3])  # remains the same but remove the proxy tag string
        else:  # success
            hiveDataList.append([component, controlId, attrStr, value])
    # remove duplicates from the list
    hiveDataList = [list(x) for x in set(tuple(x) for x in hiveDataList)]
    return hiveDataList


def get_channel_attrs_proxy_sel_string(rootOfProxies=True, longNames=False, hasChangedFromDefault=False):
    """Returns a string of channel box attributes for selected proxies, formatted for Hive.

    If the selected object is not a Hive rig component, it will return the object name, attribute name, and value.

    Automatically finds root proxy attributes and rootOfProxies=True returns the object/node of the base proxy.

    The returned string can contain the following formats:
    If Hive: "<component> <id> <attr> <val>\n"
    If not Hive: "<objectName> <attrName> <value>\n"

    :param rootOfProxies: Whether to include root of proxies in the search
    :type rootOfProxies: bool
    :param longNames: Whether to return long names of attributes
    :type longNames: bool
    :param hasChangedFromDefault: Check if the attr value has changed from the default value, if so keep it
    :type hasChangedFromDefault: bool

    :return: A string of attributes formatted for Hive, where each entry is a line containing
    :rtype: str
    """
    attrDataString = ""
    attrDataList = get_channelboxAttr_list_proxy_sel(rootOfProxies=rootOfProxies, longNames=longNames,
                                                     hasChangedFromDefault=hasChangedFromDefault)
    if not attrDataList:
        return attrDataString

    for attrData in attrDataList:
        # attrData is a list of [component, controlId, attrName, value]
        if len(attrData) == 3:  # objectName, attributeName, value
            attrDataString += "{} {} {}\n".format(attrData[0], attrData[1], attrData[2])
        else:
            componentName = attrData[0].serializedTokenKey()
            controlId = attrData[1]
            attrName = attrData[2]
            value = attrData[3]
            attrDataString += "{} {} {} {}\n".format(componentName, controlId, attrName, value)
    sortedString = alphabetical_sort_string(attrDataString)  # sort the string alphabetically by line
    return sortedString


# -----------------
# SAVE DATA
# -----------------

def deleteStringDataScene(message=True):
    """Deletes the string data node from the scene if it exists."""
    dataNodeList = cmds.ls(HIVE_ATTR_DEFAULT_DATA, type="network", long=True)
    if dataNodeList:
        cmds.delete(dataNodeList[0])
        if message:
            output.displayInfo(
                "Success: Deleted Default Attribute data node from scene: `{}`".format(HIVE_ATTR_DEFAULT_DATA))
    else:
        if message:
            output.displayWarning(
                "No selection set data found in the scene. Node `{}` not found.".format(HIVE_ATTR_DEFAULT_DATA))


def saveStringDataScene(dataString, applySym, rig=None, message=True):
    """Saves a string of data to the scene as a network node with custom attributes.

    The dataString should be formatted as:
    .. code-block:: python
        "componentName controlId attrName value\n nodeStr attrName value\n "

    :param dataString: The string of data to save
    :type dataString: str
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`, optional
    :param applySym: Whether to apply symmetry to the data as a boolean attribute stored on the message node.
    :type applySym: bool
    :param message: Report messages to the user?
    """
    dataNodeList = cmds.ls(HIVE_ATTR_DEFAULT_DATA, type="network", long=True)
    if not dataNodeList:  # create the node
        dataNode = cmds.createNode("network", name=HIVE_ATTR_DEFAULT_DATA)
        cmds.addAttr(dataNode, longName=HIVE_ATTR_DEFAULT_DATA, dataType="string")
        cmds.addAttr(dataNode, longName=ATTR_APPLY_SYMMETRY, attributeType='bool', defaultValue=False)
    else:
        dataNode = dataNodeList[0]
    cmds.setAttr("{}.{}".format(dataNode, HIVE_ATTR_DEFAULT_DATA), dataString, type="string")
    cmds.setAttr("{}.{}".format(dataNode, ATTR_APPLY_SYMMETRY), applySym)

    if rig:  # add the rebuild tools build script to the current rig. If it already exists, it will be ignored.
        try:
            rig.configuration.addBuildScript("rebuildTools_buildScript")
            rig.saveConfiguration()
        except:  # rare case that the rig is not valid.
            pass
    if message:
        output.displayInfo("Success: Saved Default Attribute data to scene: {}".format(dataNode))
    return dataNode


def getStringDataScene(message=True):
    """ Loads a string of data from the scene's network node with custom attributes.

    The network node is expected to be named `cgrigHiveAttrData` and have a string attribute and a
    bool attribute for symmetry.

    The dataString should be formatted as:
    .. code-block:: python
        "componentName controlId attrName value\n nodeStr attrName value\n "

    :param message: Report messages to the user?
    :type message: bool
    :return: A tuple containing the data string and a boolean indicating whether symmetry should be applied.
    :rtype: tuple(str, bool)
    """
    if not cmds.objExists(HIVE_ATTR_DEFAULT_DATA):
        if message:
            output.displayWarning("No selection set data has been saved or found in the scene. "
                                  "Node {} not found.".format(HIVE_ATTR_DEFAULT_DATA))
        return None, None
    dataString = cmds.getAttr("{}.{}".format(HIVE_ATTR_DEFAULT_DATA, HIVE_ATTR_DEFAULT_DATA))
    applySymBool = cmds.getAttr("{}.{}".format(HIVE_ATTR_DEFAULT_DATA, ATTR_APPLY_SYMMETRY))

    if message:
        output.displayInfo("Success: Set Attribute Default data loaded from scene: {}".format(HIVE_ATTR_DEFAULT_DATA))
    return dataString, applySymBool


def loadDefaultAttrsFromScene(rig=None, message=True):
    """ Loads default attributes from the scene's network node with custom attributes and sets the default attributes
    """
    dataString, applySym = getStringDataScene(message=message)
    if not dataString:  # message already displayed in getStringDataScene
        return
    set_string_to_defaultAttr(dataString, applySym=applySym, rig=rig, removeDefaultAttrs=True, message=message)


# -----------------
# SET DATA
# -----------------

def get_opposite_side(componentToken, id, attr, value, components):
    for component in components:
        if component.serializedTokenKey() == componentToken:
            oppositeSide = component.namingConfiguration().field("sideSymmetry").valueForKey(component.side())
            if oppositeSide:  # opposite side is a string label for example "L" or "R"
                oppositeComponent = component.rig.component(component.name(), oppositeSide)
                if oppositeComponent:
                    return [oppositeComponent.serializedTokenKey(), id, attr, value]
    else:
        return []  # no opposite side found


def string_to_data_list(dataString):
    """Converts a string of data into a list of lists.

    The string should be formatted as:
    .. code-block:: python
        "componentName controlId attrName value\n nodeStr attrName value\n "

    Each line in the string will be split into a list of strings, where each string is a part of the line.
    If the line contains commas, they will be removed and the line will be split by whitespace.
    If the line is empty, contains whitespace only or only commas it will be skipped.

    :param dataString: The string to convert
    :type dataString: str
    :return: A list of lists containing the data
    :rtype: list[list(str)]
    """
    dataList = list()
    lines = dataString.strip().split("\n")
    if not lines:
        return dataList
    for line in lines:
        # remove commas from string
        line = line.replace(",", "")  # replace commas with spaces
        parts = line.split()  # split by whitespace
        if not parts:
            continue
        dataList.append(parts)  # append the whole line as a list
    return dataList


def alphabetical_sort_string(dataString):
    """Sorts a string of data alphabetically by each line.

    :param dataString: The string to sort
    :type dataString: str

    :return: A sorted string of data
    :rtype: str
    """
    # create a list from a string with each line as an entry
    lines = dataString.splitlines()
    # remove empty lines
    lines = [line for line in lines if line.strip()]
    # sort the lines alphabetically
    lines = sorted(lines)
    # join the lines back into a string
    sorted_data_string = "\n".join(lines)
    return sorted_data_string


def componentToken_id_to_zapi(componentToken, controlId, rig):
    """Converts a component token and control ID to a Maya API object.

    :param componentToken: The component token to convert
    :type componentToken: str
    :param controlId: The control ID to convert
    :type controlId: str
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`

    :return: A Maya API object corresponding to the component and control ID
    :rtype: :class:`maya.api.OpenMaya.MObject`
    """
    # get the component from the component token
    components = list(rig.iterComponents())
    if not components:
        return None
    for component in components:
        if component.serializedTokenKey() == componentToken:
            # get the node by ID
            if controlId == "controlPanel":
                node = component.rigLayer().controlPanel()
            else:
                node = component.rigLayer().control(controlId)
            return node
    return None  # no component found with the token


def list_to_zapi_attr_value(lineList, rig):
    """Converts a list of data into a list of Maya API objects.
    ["componentName", "controlId", "attrName", "value"]
    to
    ["zapiNode", "attrName", "value"]

    :param lineList: The list of data to convert
    :type lineList: list[list(str)]
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`

    :return: A list of Maya API objects
    :rtype: list[:class:`maya.api.OpenMaya.MObject`]
    """
    componentToken = lineList[0]
    controlId = lineList[1]
    attrName = lineList[2]
    value = lineList[3]

    # get the zapi node name from componentToken controlId
    node = componentToken_id_to_zapi(componentToken, controlId, rig)
    if node:
        # return the zapi node, attrName and value
        return [node, attrName, value]
    else:
        return None, None, None


def convert_dataList_to_zapiDataList(dataList, rig=None, message=False):
    """Converts a list of data whether string names [["nodeStrName", "attrName", "value"]]
    or component ID [["componentName", "controlId", "attrName", "value"]]
    to a list of zapi nodes, attr names and values. [["zapiNode", "attrName", "value"]]

    Missing nodes will be ignored.

    :param dataList: A list of data to convert, where each entry is a list string names or component IDs.
    :type dataList: list[list(str)]
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`, optional default rig in scene will be used.
    :param message: Report messages to the user?
    :type message: bool

    :return: A list of zapi nodes, attribute names, and values.
    :rtype: list[list(:class:`maya.api.OpenMaya.MObject`, str, str)]
    """
    zapiDataList = list()  # will hold the zapi node, attrName and value

    for lineList in dataList:
        if len(lineList) == 4:  # then component id attr value
            newLineList = list_to_zapi_attr_value(lineList, rig=rig)
            if newLineList[0] is not None:  # if the zapi node was found
                zapiDataList.append(newLineList)
            else:
                if message:
                    output.displayWarning(
                        "Node/Object with component `{}` and control ID `{}` not found.".format(lineList[0],
                                                                                                lineList[1]))
        elif len(lineList) == 3:  # then strName attr value
            # check if object exists in the scene
            if not cmds.objExists(lineList[0]):
                if message:
                    output.displayWarning("Node named `{}` not found in the scene.".format(lineList[0]))
                continue
            # get the zapi node by name
            node = zapi.nodeByName(lineList[0])
            if node:
                zapiDataList.append([node, lineList[1], lineList[2]])
            else:
                if message:
                    output.displayWarning("Node `{}` not found.".format(lineList[0]))
        else:
            if message:
                output.displayWarning("Item count invalid format in line: {}".format(lineList))
            continue
    return zapiDataList


def set_string_to_defaultAttr(dataString, applySym=False, rig=None, removeDefaultAttrs=True, message=True):
    """Sets the default attributes for a Hive rig based on a string of data.

    The string should be formatted as:
    .. code-block:: python

        "componentName controlId attrName value\n nodeStr attrName value\n "

    :param dataString: The string of data to set as default attributes
    :type dataString: str
    :param applySym: Whether to apply symmetry to the data
    :type applySym: bool
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`, optional
    :param removeDefaultAttrs: Whether to ignore default attributes from the data attributes.
    :type removeDefaultAttrs: bool
    :param message: Report messages to the user?
    :type message: bool

    """
    if rig is None:
        rig = defaultRig()
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene.")
        return False  # did not set any attributes

    dataList = string_to_data_list(dataString)
    if not dataList:
        if message:
            output.displayWarning("No data found in the string.")
        return False  # did not set any attributes

    if applySym:
        oppositeSideList = list()  # will hold the opposite side attributes
        components = list(rig.iterComponents())  # better to get all components here as not to iterate for each attr
        if components:
            for attrList in dataList:
                if len(attrList) == 4:
                    newattrList = get_opposite_side(attrList[0], attrList[1], attrList[2], attrList[3], components)
                    if newattrList:
                        oppositeSideList.append(newattrList)  # append the opposite side attribute
        if oppositeSideList:
            dataList.extend(oppositeSideList)

    # Convert the dataList to zapiDataList and remove entries that are not found ----------------
    zapiDataList = convert_dataList_to_zapiDataList(dataList, rig=rig, message=message)
    # remove items that contain None, suchs as [None, None, None] which means the node was not found
    zapiDataList = [item for item in zapiDataList if item[0] is not None]

    if not zapiDataList:
        if message:
            output.displayWarning("No valid object/attributes found in the scene.")
        return False
    if removeDefaultAttrs:  # Remove default attributes MAYA_DEFAULT_ATTRS, they cannot be default set
        zapiDataList = [item for item in zapiDataList if item[1] not in attributes.MAYA_DEFAULT_ATTRS]
        # remove pure underscore attributes as they are dividers
        zapiDataList = [item for item in zapiDataList if not re.compile(r'^_+$').match(item[1])]

    if not zapiDataList:
        if message:
            output.displayWarning("Likely no matching object.attributes could not be found in scene.")
        return False

    # Set the default attributes ---------------------
    for lineData in zapiDataList:
        nodeZapi = lineData[0]  # zapi node
        if not nodeZapi:
            if message:
                output.displayWarning("Node {} not found.".format(lineData[0]))
            continue
        nodeStr = str(nodeZapi)
        attr = lineData[1]
        valueStr = lineData[2]  # str
        # check attribute exists and convert value to appropriate type ----------
        autoConvertedValue = attributes.convert_str_attrType(nodeStr, attr, valueStr, message=message)
        if autoConvertedValue is None:  # message reported in convert_str_attrType
            continue

        # Set the attribute default value ----------------
        attributes.attributeDefault(nodeStr, attr, autoConvertedValue, setValue=True, setProxies=True)
        if message:
            output.displayInfo("Success: Set Default Attribute: {}.{} = {}".format(nodeStr,
                                                                                   attr,
                                                                                   autoConvertedValue))

    # Display success message if any attributes were set ----------------
    if message:
        output.displayInfo("Success: Some default attributes overridden. See Script Editor for details.")


# -----------------
# SET DATA
# -----------------


def write_to_json(file_path, message=True):
    """
    Writes the Override Default Attribute values to a file on disk in JSON format.

    Returns the data written to the file.
    :param file_path: The full path to the JSON file to write.
    :type file_path: str
    :param message: Report a message to the user?
    :type message: bool

    :return: The string data written to the JSON file.
    :rtype: str
    """
    dataStr, applySym = getStringDataScene(message=True)

    if dataStr is None:
        output.displayWarning("No Default Attribute Values found to write to JSON file.")
        return {}

    dictData = {"default_attr_data": {"default_attr_string": dataStr,
                                      "default_attr_applySym": applySym}
                }

    filesystem.saveJson(dictData, file_path, indent=4, separators=(",", ":"))

    if message:
        output.displayInfo("Success: Default Attribute Values saved to JSON file: {}".format(file_path))

    return dataStr, applySym


def load_from_json(file_path, message=True):
    """Loads a JSON file containing the Override Default Attribute Values
    Returns the string data and applySym bool

    Function used in the UI to load the default attribute values from a JSON file.

    Format of the JSON file:

    {"default_attr_data": {"default_attr_string": dataStr,
                           "default_attr_applySym": applySym}
                          }

    :param file_path: The full path to the JSON file to read.
    :type file_path: str
    :param message: Report a message to the user?
    :type message: bool

    :return: A tuple containing the default attribute string and applySym boolean.
    :rtype: tuple(str, bool)
    """
    dataDict = filesystem.loadJson(file_path)
    if not dataDict:
        output.displayWarning("No Default Attribute Values found in JSON file.")
        return

    default_attr_data = dataDict["default_attr_data"]
    default_attr_string = default_attr_data["default_attr_string"]
    default_attr_applySym = default_attr_data["default_attr_applySym"]

    if message:
        output.displayInfo("Success: Default Attribute Values loaded from JSON file: {}".format(file_path))

    return default_attr_string, default_attr_applySym


# -----------------
# SEARCH REPLACE & VALIDATE
# -----------------

def openScriptEditor():
    mel.eval("if (`scriptedPanel - q - exists scriptEditorPanel1`) "
             "{scriptedPanel -e -tor scriptEditorPanel1; "
             "showWindow scriptEditorPanel1Window; "
             "selectCurrentExecuterControl;} "
             "else {CommandWindow;}")


def validate_default_attr_data(dataString, rig):
    """Validates the source and target objects, checks if they exist in the scene.

    :param dataString: The string of data to validate, formatted as:
    :    .. code-block:: python
        "componentName controlId attrName value\n nodeStr attrName value\n "
    :type dataString: str
    :param rig: The rig instance to use, defaults to the default rig
    :type rig: :class:`api.Rig`, optional
    """
    logFinText = ("----------------- LOG FINISHED ----------------\n"
                  "Validation Complete: Check the script editor for object details.")
    output.displayInfo("\n\n\n\n------------------ START LOG ----------------")
    if not rig:
        output.displayWarning("No Hive rig instance found in the scene. Could not find a Hive rig to validate against.")
        output.displayWarning(logFinText)
        openScriptEditor()
        return
    dataList = string_to_data_list(dataString)
    # Convert the dataList to zapiDataList and remove entries that are not found ----------------
    zapiDataList = convert_dataList_to_zapiDataList(dataList, rig=rig, message=True)
    # remove items that contain None, suchs as [None, None, None] which means the node was not found
    zapiDataList = [item for item in zapiDataList if item[0] is not None]

    if not zapiDataList:
        output.displayWarning("Error: No useable data was found from the text string.")
        output.displayWarning(logFinText)
        openScriptEditor()
        return
    for objData in zapiDataList:
        nodeStr = str(objData[0])  # zapi node
        nodeUniqueName = cmds.ls([nodeStr], shortNames=True)[0]
        attr = objData[1]
        if attr in attributes.MAYA_DEFAULT_ATTRS:
            output.displayWarning(
                "Node.Attribute {}.{} is a default Maya attribute and cannot be set as a default.".format(
                    nodeUniqueName, attr))
            continue
        # check if the object exists in the scene
        if not cmds.objExists(nodeStr):
            output.displayWarning(
                "Node.Attribute {} object does not exist in the scene.".format(nodeUniqueName, attr))
            continue
        # check if the attribute exists on the object
        if not cmds.attributeQuery(attr, node=nodeStr, exists=True):
            output.displayWarning(
                "Node.Attribute {}.{} does not exist on the object.".format(nodeUniqueName, attr))
            continue
        else:
            output.displayInfo("Success: Node.Attribute {}.{} exists in the scene.".format(nodeUniqueName, attr))

    output.displayInfo(logFinText)
    openScriptEditor()
