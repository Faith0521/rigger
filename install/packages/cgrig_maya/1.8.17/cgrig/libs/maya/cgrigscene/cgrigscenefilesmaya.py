# -*- coding: utf-8 -*-
import os

from maya import cmds
from cgrig.libs.maya.cmds.objutils import meshhandling, namehandling
from cgrig.libs.general.exportglobals import MESHOBJECTS
from cgrig.preferences.interfaces import assetinterfaces
from cgrig.libs.utils import path


def setSubDDict(cgrigSceneDict):
    """Sets the subD attributes from the cgrigSceneDict

    :param cgrigSceneDict: the nested exported dict which contains subD information
    :type cgrigSceneDict: dict
    """
    if MESHOBJECTS in cgrigSceneDict:  # check if meshesDict were recorded
        for meshTransform in cgrigSceneDict[MESHOBJECTS]:  # cycle through meshes
            if cmds.objExists(meshTransform):  # if the mesh is in the scene set subDs
                meshhandling.setMeshSubDSettings(meshTransform,
                                                 cgrigSceneDict[MESHOBJECTS][meshTransform],
                                                 longName=True)


def getExportedNamespaces(objectRootList, gShaderDict):
    """Gets all namespaces in the nodes under the objectRootList and from shader names

    :param objectRootList: object roots as to be exported from alembic, needs to all children
    :type objectRootList: list
    :param gShaderDict: the .cgrigScene dictionary with light data
    :type gShaderDict: dict
    :return namespaceList: A list of Maya Namespaces Found
    :rtype namespaceList: list
    """
    # get all objects below the roots
    if objectRootList:  # may only be shaders
        objectRootList += cmds.listRelatives(objectRootList, allDescendents=True)
    # collect any namespaces
    namespaceList = namehandling.getNamespacesFromList(objectRootList)
    # get a shader list
    if not gShaderDict:
        return namespaceList
    for shaderDictKey in gShaderDict:
        if ":" in shaderDictKey:
            namespaceList.append(shaderDictKey.split(":")[0])
    return list(set(namespaceList))


def findMayaSceneByName(category, assetName):
    """Searches and returns the maya scene path based on the category and asset name.

    :param category:  The cgrig asset category which the asset resides in.
    :type category: str
    :param assetName: The cgrig asset Name.
    :type assetName: str
    :return: The maya scene path or an empty string.
    :rtype: str
    """
    pref = assetinterfaces.mayaScenesInterface()
    for directory in pref.scenesAssets.browserFolderPaths():
        if directory.alias != category:
            continue
        dirPath = directory.path
        for assetFolder in os.listdir(dirPath):
            d = os.path.join(dirPath, assetFolder)
            for filePath in path.filesByExtension(d, ["ma", "mb"], sort=True):
                if path.getFileNameNoExt(filePath) == assetName:
                    return os.path.join(d, filePath)
    return ""
