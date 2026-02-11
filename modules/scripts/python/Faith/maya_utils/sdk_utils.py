# -*- coding: utf-8 -*-
# @Author: YinYuFei
# @Date:   2022-06-19 16:49:53
# @Last Modified by:   yinyufei
# @Last Modified time: 2022-08-04 09:45:03

import json
import re
import math
import maya.cmds as cmds
import maya.mel as mel
from pymel.core import *
from ..maya_utils import rigging_utils as rig

SDK_UTILITY_TYPE = ("blendWeighted",)
SDK_ANIMCURVES_TYPE = ("animCurveUA", "animCurveUL", "animCurveUU")


# ==============================================================================
# Data export
# ==============================================================================


def _importData(filePath):
    """导入给定路径的sdk的json文件

    Args:
        filePath (string): path to file

    Returns:
        dict: contents of json file, expected dict
    """
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(e)


def _exportData(data, filePath):
    """导出字典里的sdk数据到给定路径

    Args:
        data (dict): expected dict, not limited to
        filePath (string): path to output json file
    """
    try:
        with open(filePath, "w") as f:
            json.dump(data, f, sort_keys=False, indent=4)
    except Exception as e:
        print(e)


# ==============================================================================
# pymel Convenience
# ==============================================================================

def getPynodes(nodes):
    """Conevenience function to allow uses to pass in strings, but convert to
    pynodes if not already.

    Args:
        nodes (list): string names

    Returns:
        list: of pynodes
    """
    pynodes = []
    for node in nodes:
        if isinstance(node, str):
            node = PyNode(node)
        pynodes.append(node)
    return pynodes


def getSDKInfoFromNode(node, expType="after"):
    """

    :param node:
    :param expType:
    :return:
    """
    allSDKInfo_dict = {}
    if nodeType(node) == "blendShape":
        AllAlias = aliasAttr(node, q=True)
        AttrsList = [AllAlias[i] for i in range(
            0, len(AllAlias), 2
        )]
    else:
        AttrsList = listAttr(node, k=True)
    for eachAttr in AttrsList:
        if objExists("%s.%s" % (node, eachAttr)):
            testConnections = listConnections("%s.%s" % (node, eachAttr),
                                              plugs=True)
            if testConnections:
                retrievedSDKNodes = getConnectedSDKs(
                    attribute="%s.%s" % (node, eachAttr), expType=expType)

                if expType == "front":
                    retrievedSDKNodes.extend(getMultSDKs("%s.%s" % (node, eachAttr)))
                if expType == "front":
                    for animPlug, targetPlug in retrievedSDKNodes:
                        if checkAnimNodeNumberKeys(animPlug.nodeName()) > 1:
                            allSDKInfo_dict[animPlug.nodeName()] = getSDKInfo(animPlug.node(), node)
                if expType == "after":
                    for targetPlug, animPlug in retrievedSDKNodes:
                        if checkAnimNodeNumberKeys(animPlug.nodeName()) > 1:
                            allSDKInfo_dict[animPlug.nodeName()] = getSDKInfo(animPlug.node(), node)

    return allSDKInfo_dict


def getSDKInfoFromAttr(attr, expType="after"):
    allSDKInfo_dict = {}
    testConnections = listConnections(attr, plugs=True)
    if testConnections:
        retrievedSDKNodes = getConnectedSDKs(
            attribute=attr, expType=expType)
        if expType == "front":
            retrievedSDKNodes.extend(getMultSDKs(attr))
        if expType == "front":
            for animPlug, targetPlug in retrievedSDKNodes:
                allSDKInfo_dict[animPlug.nodeName()] = getSDKInfo(animPlug.node())
        else:
            for targetPlug, animPlug in retrievedSDKNodes:
                allSDKInfo_dict[animPlug.nodeName()] = getSDKInfo(animPlug.node())
    return allSDKInfo_dict


def getMultSDKs(attr):
    """

    :param attr:
    :return:
    """
    sdkDrivers = []
    for sdkUtility in SDK_UTILITY_TYPE:
        blend_NodePair = listConnections(attr,
                                         source=True,
                                         type=sdkUtility,
                                         exactType=True,
                                         plugs=True,
                                         connections=True,
                                         sourceFirst=True,
                                         scn=True) or []

        if not blend_NodePair:
            continue
        for pairs in blend_NodePair:
            blw_inAttr = pairs[0].replace("output", "input")
            sdkPairs = getConnectedSDKs(blw_inAttr, expType="front")
            for sPair in sdkPairs:
                sdkDrivers.append([sPair[0], pairs[1]])
    return sdkDrivers


def setSdkNodes(animKeys, driver, driven, preInfinity, postInfinity):
    for index in range(0, len(animKeys)):
        frameValue = animKeys[index]
        timeValue = frameValue[0]
        value = frameValue[1]

        setDrivenKeyframe(driven.split(".")[0], at=driven.split(".")[1], cd=driver, dv=timeValue,
                          value=value)

    for index in range(0, len(animKeys)):
        frameValue = animKeys[index]
        animCurrentCrv = getAnimCurve(
            driver, driven
        )
        if animCurrentCrv:
            mel.eval('keyTangent -index %s -e -itt %s -ott %s %s' % (index, frameValue[2],
                                                                     frameValue[3], animCurrentCrv[0]))
            mel.eval('keyTangent -index %s -e -ia %s -oa %s %s' % (
                index, frameValue[4], frameValue[5], animCurrentCrv[0]
            ))

            animCurrentCrv[0].preInfinity.set(preInfinity)
            animCurrentCrv[0].postInfinity.set(postInfinity)


def createSDKFromDict(sdkInfo_dict):
    """

    :param sdkInfo_dict:
    :return:
    """
    animKeys = sdkInfo_dict["keys"]
    driver = sdkInfo_dict['driver']
    driven = sdkInfo_dict['driven']

    if not objExists(driver):
        print("Object : %s does not in the scene." % driver)
        return

    if not isinstance(driven, list):
        setSdkNodes(animKeys, driver, driven, sdkInfo_dict['preInfinity'], sdkInfo_dict['postInfinity'])
    else:
        [setSdkNodes(animKeys, driver, driven[j], sdkInfo_dict['preInfinity'], sdkInfo_dict['postInfinity']) for j in
         range(len(driven))]


def getBlendNodes(attrPlug):
    """

    :param attrPlug:
    :return:
    """
    blendNode = listConnections(attrPlug, scn=True)
    if nodeType(blendNode[0]) in SDK_ANIMCURVES_TYPE:
        existingAnimNode = blendNode[0]
        blendNodeName = "{0}_blw".format(attrPlug.replace(".", "_"))
        blendNode = [createNode("blendWeighted", n=blendNodeName)]
        connectAttr(blendNode[0].attr("output"), attrPlug, f=True)
        destPlug = "{0}.input[0]".format(blendNode[0].name())
        connectAttr(existingAnimNode.attr("output"), destPlug, f=True)
    if nodeType(blendNode[0]) in SDK_UTILITY_TYPE:
        blendNode = blendNode[0]
    if type(blendNode) == list:
        blendNode = blendNode[0]
    numOfInputs = len(blendNode.getAttr("input"))
    destPlug = "{0}.input[{1}]".format(blendNode.name(), numOfInputs)
    return destPlug


def getSDKInfo(animNode, driven=None):
    """
    get all the information from an sdk/animCurve in a dictionary
    for exporting.

    :param animNode:
    :return: dict: dictionary of all the attrs to be exported
    """
    sdkInfo_dict = {}
    sdkKey_Info = []
    numberOfKeys = int(len(listAttr("{0}.ktv".format(animNode), multi=True)) / 3)
    itt_list = keyTangent(animNode, itt=True, q=True)
    ott_list = keyTangent(animNode, ott=True, q=True)
    ia_list = keyTangent(animNode, ia=True, q=True)
    oa_list = keyTangent(animNode, oa=True, q=True)
    # maya doesnt return value if there is only one key frame set.
    if itt_list is None:
        itt_list = ["linear"]
    if ott_list is None:
        ott_list = ["linear"]
    for index in range(int(numberOfKeys)):
        value = getAttr("{0}.keyTimeValue[{1}]".format(animNode, index))
        absoluteValue = keyframe(animNode,
                                 q=True,
                                 valueChange=True,
                                 index=index)[0]

        keyData = [value[0], absoluteValue, itt_list[index], ott_list[index], ia_list[index], oa_list[index]]
        sdkKey_Info.append(keyData)
    sdkInfo_dict["keys"] = sdkKey_Info
    sdkInfo_dict["type"] = animNode.type()
    sdkInfo_dict["preInfinity"] = animNode.getAttr("preInfinity")
    sdkInfo_dict["postInfinity"] = animNode.getAttr("postInfinity")
    sdkInfo_dict["weightedTangents"] = animNode.getAttr("weightedTangents")

    animNodeInputPlug = "{0}.input".format(animNode.nodeName())
    sourceDriverAttr = listConnections(animNodeInputPlug,
                                       source=True,
                                       plugs=True,
                                       scn=True)[0]
    if "blendWeighted" in nodeType(sourceDriverAttr):
        sourceDriverAttr_new = listConnections(sourceDriverAttr.replace('output', 'input'),
                                               source=True,
                                               plugs=True,
                                               scn=True)[0]
        driverNode, driverAttr = sourceDriverAttr_new.split(".")
    else:
        driverNode, driverAttr = sourceDriverAttr.split(".")
    sdkInfo_dict["driver"] = "%s.%s" % (driverNode, driverAttr)

    animNodeOutputPlug = "{0}.output".format(animNode.nodeName())
    drivenNodes, drivenAttrs = getSDKDestination(animNodeOutputPlug)
    if driven and driven in drivenNodes:
        index = drivenNodes.index(driven)
        drivenNodes = driven.name()
        drivenAttrs = drivenAttrs[index]
        sdkInfo_dict["driven"] = "%s.%s" % (drivenNodes, drivenAttrs)
    elif len(drivenNodes) == 1:
        sdkInfo_dict["driven"] = "%s.%s" % (drivenNodes[0], drivenAttrs[0])
    else:
        sdkInfo_dict["driven"] = ["%s.%s" % (node, attr) for node, attr in zip(drivenNodes, drivenAttrs)]

    return sdkInfo_dict


def getSDKDestination(animNodeOutputPlug):
    """Get the final destination of the sdk node, skips blend weighted
    and conversion node to get the transform node.
    TODO: Open this up to provided type destination

    Args:
        animNodeOutputPlug (string): animationNode.output

    Returns:
        list: name of the node, and attr
    """
    attrTargets = connectionInfo(animNodeOutputPlug, dfs=1)
    drivenNodes = []
    drivenAttrs = []
    for i, attr in enumerate(attrTargets):
        if attr != '':
            while 'unitConversion' in nodeType(attrTargets[i]) or 'blendWeighted' in nodeType(attrTargets[i]):
                targets = connectionInfo(attrTargets[i][:attrTargets[i].index('.')] + '.output', dfs=1)
                if not targets:
                    error("Please clear not used 'unitConversion' or 'blendWeighted' nodes.")
                    break
                else:
                    attrTargets[i] = targets[0]
        else:
            attrTargets[i] = 'None'
        drivenNodes.append(attrTargets[i].split(".")[0])
        drivenAttrs.append(attrTargets[i].split(".")[1])
    return drivenNodes, drivenAttrs


def getConnectedSDKs(attribute="",
                     expType="after",
                     curvesOfType=None):
    """

    :param expType:
    :param attribute:
    :param curvesOfType:
    :return:
    """
    if curvesOfType is None:
        curvesOfType = []
    retrievedSDKNodes = []
    animCurveNodes = []
    if not curvesOfType:
        curvesOfType = SDK_ANIMCURVES_TYPE
    for animCurve in curvesOfType:
        if expType == "after":
            attrTargets = connectionInfo(attribute, dfs=1)
            for i, attr in enumerate(attrTargets):
                if attr != '':
                    if 'unitConversion' in nodeType(attrTargets[i]) or 'blendWeighted' in nodeType(
                            attrTargets[i]):
                        animCurveNodes = listConnections(attrTargets[i][:attrTargets[i].index('.')] + '.output',
                                                         source=False,
                                                         destination=True,
                                                         type=animCurve,
                                                         exactType=True,
                                                         plugs=True,
                                                         connections=True,
                                                         sourceFirst=True,
                                                         scn=True) or []
                    else:
                        animCurveNodes = listConnections(attribute,
                                                         source=False,
                                                         destination=True,
                                                         type=animCurve,
                                                         exactType=True,
                                                         plugs=True,
                                                         connections=True,
                                                         sourceFirst=True,
                                                         scn=True) or []
                    retrievedSDKNodes.extend(animCurveNodes)
        else:
            animCurveNodes = listConnections(attribute,
                                             source=True,
                                             destination=False,
                                             type=animCurve,
                                             exactType=True,
                                             plugs=True,
                                             connections=True,
                                             sourceFirst=True,
                                             scn=True) or []
            retrievedSDKNodes.extend(animCurveNodes)

    return retrievedSDKNodes


def mirrorSDKs(nodes, attributes=None, type="front"):
    """

    :param type:
    :param attributes:
    :param nodes:
    :return:
    """
    if attributes is None:
        attributes = []
    for node in nodes:
        node = getPynodes(nodes)[0]
        if nodeType(node) == "blendShape":
            AllAlias = aliasAttr(node, q=True)
            AttrsList = [AllAlias[i] for i in range(
                0, len(AllAlias), 2
            )]
        else:
            AttrsList = listAttr(node, k=True)

        if not attributes:
            for eachAttr in AttrsList:
                if objExists("%s.%s" % (node, eachAttr)):
                    testConnections = listConnections("%s.%s" % (node, eachAttr),
                                                      plugs=True)
                    if testConnections:
                        mirrorKeys("%s.%s" % (node, eachAttr), type=type)
        else:
            for eachAttr in attributes:
                if objExists("%s.%s" % (node, eachAttr)):
                    testConnections = listConnections("%s.%s" % (node, eachAttr),
                                                      plugs=True)
                    if testConnections:
                        mirrorKeys("%s.%s" % (node, eachAttr), type=type)


def checkAnimNodeNumberKeys(animNode):
    numberOfKeys = int(len(listAttr("{0}.ktv".format(animNode), multi=True)) / 3)
    return numberOfKeys


def mirrorKeys(attr, type="front"):
    """

    :param type:
    :param attr:
    :return:
    """

    sourceSDKInfo = getConnectedSDKs(attr, type)
    sourceSDKInfo.extend(getMultSDKs(attr))
    for source, dest in sourceSDKInfo:
        info = {}
        if type == "front":
            if checkAnimNodeNumberKeys(source.nodeName()) > 1:
                info = {source.nodeName(): getSDKInfo(source.node())}
        elif type == "after":
            if checkAnimNodeNumberKeys(dest.nodeName()) > 1:
                info = {dest.nodeName(): getSDKInfo(dest.node())}
        if info:
            invertKeyValues(info)


def invertKeyValues(sdkInfo):
    for animNode, infoDict in sdkInfo.items():
        animKeys = infoDict["keys"]
        driver = infoDict['driver']
        driven = infoDict['driven']

        if not isinstance(driven, list):
            mirrorDriv(driver, driven, animKeys, infoDict["preInfinity"], infoDict["postInfinity"])
        else:
            [mirrorDriv(driver, driven[j], animKeys, infoDict["preInfinity"], infoDict["postInfinity"]) for j in
             range(len(driven))]


def mirrorDriv(driver, driven, animKeys, preInfinity, postInfinity):
    checkResult = checkSymAttrIfMirror(driver, driven)
    driver_Attr = checkResult[0]
    driven_Attr = checkResult[1]
    for index in range(0, len(animKeys)):
        frameValue = animKeys[index]
        connectionObj = connectionInfo(driven, sfd=1)

        if connectionObj != '' and 'animCurve' in nodeType(connectionObj):
            pass

        if '-' in checkResult[0] and '-' not in checkResult[1]:
            cmds.setDrivenKeyframe(driven_Attr.split('.')[0], at=driven_Attr.split('.')[1],
                                   cd=driver_Attr[:-1],
                                   dv=float(frameValue[0]) * -1, v=float(frameValue[1]))
        elif '-' not in checkResult[0] and '-' in checkResult[1]:
            cmds.setDrivenKeyframe(driven_Attr.split('.')[0], at=driven_Attr.split('.')[1],
                                   cd=driver_Attr,
                                   dv=float(frameValue[0]), v=float(frameValue[1]) * (-1))
        elif '-' in checkResult[0] and '-' in checkResult[1]:
            cmds.setDrivenKeyframe(driven_Attr.split('.')[0], at=driven_Attr.split('.')[1],
                                   cd=driver_Attr[:-1], dv=float(frameValue[0]) * -1,
                                   v=float(frameValue[1]) * (-1))
        elif '-' not in checkResult[0] and '-' not in checkResult[1]:
            cmds.setDrivenKeyframe(driven_Attr.split('.')[0], at=driven_Attr.split('.')[1],
                                   cd=driver_Attr,
                                   dv=float(frameValue[0]), v=float(frameValue[1]))

    for index in range(0, len(animKeys)):
        # set key frame
        frameValue = animKeys[index]
        realdriverAttr = ""
        if '-' in driven_Attr:
            realdriverAttr = driver_Attr[:-1] if '-' in driver_Attr else driver_Attr
        elif '-' not in driven_Attr:
            realdriverAttr = driver_Attr[:-1] if '-' in driver_Attr else driver_Attr
        animCurrentCrv = getAnimCurve(realdriverAttr, driven_Attr)
        if animCurrentCrv:
            mel.eval('keyTangent -index %s -e -itt %s -ott %s %s' % (index, frameValue[2],
                                                                     frameValue[3], animCurrentCrv[0]))
            mel.eval('keyTangent -index %s -e -ia %s -oa %s %s' % (
                index, frameValue[4], frameValue[5], animCurrentCrv[0]
            ))

            animCurrentCrv[0].preInfinity.set(preInfinity)
            animCurrentCrv[0].postInfinity.set(postInfinity)


def getAnimCurve(driverAttr, setdrivenAttr=None):
    """

    @param driverAttr:
    @param setdrivenAttr:
    @return:
    """
    setdrivenCrv = []
    # ------------------------------

    animCList = listConnections(driverAttr, type='animCurve', s=False, d=True, scn=True)

    if animCList is None:
        return None
    elif animCList is not None and setdrivenAttr is None:
        return animCList
    elif animCList is not None and setdrivenAttr is not None:
        for x in animCList:
            drivenAttr = removeEXnodes(x, 'output', 'dfs')[0]
            if drivenAttr == setdrivenAttr:
                setdrivenCrv.append(x)
        return setdrivenCrv


def removeEXnodes(nodeName, nodeAttr, direction):
    """

    @param nodeName:
    @param nodeAttr:
    @param direction:
    @return:
    """
    if direction == 'sfd':
        attrSource = connectionInfo(nodeName + '.' + nodeAttr, sfd=1)

        while 'unitConversion' in attrSource:
            attrSource = connectionInfo(attrSource.replace('output', 'input'), sfd=1)
        if attrSource == '':
            attrSource = 'None'
        return attrSource

    elif direction == 'dfs':
        attrTargets = connectionInfo(nodeName + '.' + nodeAttr, dfs=1)

        for i, attr in enumerate(attrTargets):
            if attr != '':
                while 'unitConversion' in attrTargets[i] or 'blendWeighted' in attrTargets[i]:
                    attrTargets[i] = \
                        connectionInfo(attrTargets[i][:attrTargets[i].index('.')] + '.output', dfs=1)[0]
            else:
                attrTargets[i] = 'None'
        return attrTargets


def stripKeys(animNode):
    """remove animation keys from the provided sdk node

    Args:
        animNode (pynode): sdk/anim node
    """
    numKeys = int(len(listAttr(animNode + ".ktv", multi=True)) / 3)
    for x in range(0, numKeys):
        animNode.remove(0)


def checkSymObj(orgObj=None, searchFor='L_', replaceWith='R_'):
    """
    Check the symmetry of objects and attributes.
    :param orgObj:
    :param searchFor:
    :param replaceWith:
    :return:
    """
    if orgObj is None:
        orgObj = []
    symObj = []
    keyword = [searchFor]
    # ------------------------------
    if not orgObj:
        selobjs = cmds.ls(sl=1)
    else:
        selobjs = orgObj

    for x in selobjs:
        for n in keyword:
            if n not in x:
                symObj.append(x)
            else:
                theOtherSideobj = x.replace(searchFor, replaceWith)
                if cmds.objExists(theOtherSideobj):
                    symObj.append(theOtherSideobj)
                else:
                    continue

        symObj = sorted(set(symObj), key=symObj.index)

    if len(symObj) == 1:
        return symObj[0]
    else:
        return symObj


def checkSymAttrIfMirror(baseDriverAttr, baseDrivenAttr):
    """
    Check the symmetry of objects and attributes, set used value.
    :param baseDriverAttr:
    :param baseDrivenAttr:
    :return:
    """
    LeftKey = [
        'L_', 'lf_', '_L', 'facial_L_', 'left_', 'Left_'
    ]
    RightKey = [
        'R_', 'rt_', '_R', 'facial_R_', 'right_', 'Right_'
    ]
    keyNum = len(LeftKey)
    symAttr = []

    driverAttr = ""
    drivenAttr = ""

    i = 0
    # print(baseDriverAttr)
    while i < keyNum:
        if LeftKey[i] in baseDriverAttr:
            driverAttr = (checkSymObj(orgObj=[baseDriverAttr], searchFor=LeftKey[i],
                                      replaceWith=RightKey[i]))

            if len(driverAttr) == 0:
                driverAttr = baseDriverAttr
                break

            elif len(driverAttr) != 0:
                symDriver = driverAttr.split('.')[0]
                if 'translate' in baseDriverAttr or 'rotate' in baseDriverAttr and 'order' not in baseDriverAttr and 'Order' not in baseDriverAttr:
                    mirrorAxis = checkSymAxis(baseDriverAttr.split('.')[0], symDriver)
                    driverAttr = mirrorAxis[baseDriverAttr]
            break
        else:
            i = i + 1
            if i == keyNum:
                driverAttr = baseDriverAttr
                break

    j = 0
    while j < keyNum:
        if LeftKey[j] in baseDrivenAttr:
            drivenAttr = (checkSymObj(orgObj=[baseDrivenAttr], searchFor=LeftKey[j],
                                      replaceWith=RightKey[j]))

            if len(drivenAttr) == 0:
                drivenAttr = baseDrivenAttr
                driverAttr = baseDriverAttr
                break

            elif len(drivenAttr) != 0:
                symDriven = drivenAttr.split('.')[0]
                if 'translate' in baseDrivenAttr or 'rotate' in baseDrivenAttr and 'order' not in baseDrivenAttr and 'Order' not in baseDrivenAttr:
                    mirrorAxis = checkSymAxis(baseDrivenAttr.split('.')[0], symDriven)
                    drivenAttr = mirrorAxis[baseDrivenAttr]

            break
        else:
            j = j + 1
            if j == keyNum:
                if 'translate' in baseDrivenAttr or 'rotate' in baseDrivenAttr and 'order' not in baseDrivenAttr and 'Order' not in baseDrivenAttr:
                    mirrorAxis = checkSymAxis(baseDrivenAttr.split('.')[0], baseDrivenAttr.split('.')[0])
                    # print(baseDrivenAttr.split('.')[0], baseDrivenAttr.split('.')[0])
                    drivenAttr = mirrorAxis[baseDrivenAttr]
                else:
                    drivenAttr = baseDrivenAttr
                break

    symAttr.append(driverAttr)
    symAttr.append(drivenAttr)
    return symAttr


def makeObjZero(type, suffix, rotation, *obj):
    """
    This Function can make object zero
    :param type:
    :param suffix:
    :param rotation:
    :param obj:
    :return:
    """
    if len(obj) == 0:
        cmds.error(
            '------------------------->>>You must select one or more object !<<<----------------------------')

    else:

        # this type is joint .

        if type == 'joint':

            objNum = len(obj)

            for i in range(0, objNum, 1):

                if rotation == 'On':
                    cmds.makeIdentity(obj[i], apply=True, t=1, r=1, s=1, n=0)
                    cmds.duplicate(obj[i], name='%s_%s' % (obj[i], suffix))
                    childObj = cmds.listRelatives('%s_%s' % (obj[i], suffix))

                    if childObj is None:
                        cmds.parent(obj[i], '%s_%s' % (obj[i], suffix))
                    else:
                        cmds.delete('%s_%s|%s' %
                                    (obj[i], suffix, childObj[0]))
                        cmds.parent(obj[i], '%s_%s' % (obj[i], suffix))

                elif rotation == 'Off':

                    cmds.makeIdentity(obj[i], apply=True, t=1, r=1, s=1, n=0)
                    cmds.duplicate(obj[i], name='%s_%s' % (obj[i], suffix))
                    cmds.makeIdentity(obj[i], apply=True, t=1, r=1, s=1, n=0)
                    cmds.setAttr('%s_%s.rotateX' % (obj[i], suffix), 0)
                    cmds.setAttr('%s_%s.rotateY' % (obj[i], suffix), 0)
                    cmds.setAttr('%s_%s.rotateZ' % (obj[i], suffix), 0)
                    childObj = cmds.listRelatives('%s_%s' % (obj[i], suffix))

                    if childObj is None:
                        cmds.parent(obj[i], '%s_%s' % (obj[i], suffix))
                    else:
                        cmds.delete('%s_%s|%s' %
                                    (obj[i], suffix, childObj[0]))
                        cmds.parent(obj[i], '%s_%s' % (obj[i], suffix))

        # type is group ,it is have flag rotateOn / rotateOff ,you can use
        # it for ik controls  con sdk zero and so on.

        elif type == 'group':

            objNum = len(obj)

            for i in range(0, objNum, 1):

                grp = cmds.createNode(
                    'transform', name='%s_%s' % (obj[i], suffix))
                parentObj = cmds.listRelatives(obj[i], p=True)

                if rotation == 'On':
                    cmds.delete(cmds.pointConstraint(obj[i], grp, mo=False))
                    cmds.delete(cmds.orientConstraint(obj[i], grp, mo=False))

                    if parentObj is None:
                        cmds.parent(obj[i], grp)
                    else:
                        cmds.parent(grp, parentObj[0])
                        cmds.parent(obj[i], grp)

                    cmds.select(grp)
                    return grp

                elif rotation == 'Off':

                    cmds.pointConstraint(obj[i], grp, mo=False)
                    cmds.delete('%s_pointConstraint1' % grp)

                    if parentObj is None:
                        cmds.parent(obj[i], grp)
                    else:

                        cmds.parent(grp, parentObj[0])
                        cmds.parent(obj[i], grp)

                    cmds.select(grp)
                    return grp


def checkSymAxis(orgobj, symobj):
    # ------------------------------------------------------------
    # Check the symmetry axis of objects and attributes.
    # ------------------------------------------------------------

    symAxis = []

    orghelploc = cmds.createNode("transform", name=str(orgobj) + '_help_loc')
    symhelploc = cmds.createNode("transform", name=str(symobj) + '_help_loc')

    orghelplocGrp = makeObjZero('group', 'zero', 'On', orghelploc)
    symhelplocGrp = makeObjZero('group', 'zero', 'On', symhelploc)

    # update date 2017/03/16 >>
    # set zero value in object space
    cmds.parent(orghelplocGrp, orgobj)
    cmds.parent(symhelplocGrp, symobj)

    defaultAttr = ['.tx', '.ty', '.tz', '.rx',
                   '.ry', '.rz', '.sx', '.sy', '.sz']
    for attr in defaultAttr:
        if 's' in attr:
            cmds.setAttr(orghelplocGrp + attr, 1)
            cmds.setAttr(symhelplocGrp + attr, 1)
        else:
            cmds.setAttr(orghelplocGrp + attr, 0)
            cmds.setAttr(symhelplocGrp + attr, 0)

    # set zero value in world space
    cmds.parent(orghelplocGrp, w=1)
    cmds.parent(symhelplocGrp, w=1)

    zeroValue = ['.tx', '.ty', '.tz']
    for x in zeroValue:
        cmds.setAttr(orghelplocGrp + x, 0)
        cmds.setAttr(symhelplocGrp + x, 0)

    orgaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    axisKey = ['X', 'Y', 'Z', 'X-', 'Y-', 'Z-']
    symaxisValue = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                    (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

    i = 0
    while i < len(orgaxisValue):
        j = 0

        cmds.setAttr(orghelploc + '.tx', orgaxisValue[i][0])
        cmds.setAttr(orghelploc + '.ty', orgaxisValue[i][1])
        cmds.setAttr(orghelploc + '.tz', orgaxisValue[i][2])

        orgcurrentPos = cmds.xform(orghelploc, q=1, t=1, ws=1)

        orgcurrentPos[0] = round(orgcurrentPos[0], 1)
        orgcurrentPos[1] = round(orgcurrentPos[1], 1)
        orgcurrentPos[2] = round(orgcurrentPos[2], 1)

        cmds.setAttr(orghelploc + '.tx', 0)
        cmds.setAttr(orghelploc + '.ty', 0)
        cmds.setAttr(orghelploc + '.tz', 0)

        while j < len(symaxisValue):

            cmds.setAttr(symhelploc + '.tx', symaxisValue[j][0])
            cmds.setAttr(symhelploc + '.ty', symaxisValue[j][1])
            cmds.setAttr(symhelploc + '.tz', symaxisValue[j][2])

            symcurrentPos = cmds.xform(symhelploc, q=1, t=1, ws=1)

            symcurrentPos[0] = round(symcurrentPos[0], 1)
            symcurrentPos[1] = round(symcurrentPos[1], 1)
            symcurrentPos[2] = round(symcurrentPos[2], 1)

            cmds.setAttr(symhelploc + '.tx', 0)
            cmds.setAttr(symhelploc + '.ty', 0)
            cmds.setAttr(symhelploc + '.tz', 0)

            if symcurrentPos[0] * -1 == orgcurrentPos[0] and symcurrentPos[1] == orgcurrentPos[1] \
                    and symcurrentPos[2] == orgcurrentPos[2]:

                symAxis.append(orgobj + '.translate' + axisKey[i])
                symAxis.append(symobj + '.translate' + axisKey[j])

                # check rotate
                # create rotate help locator
                orgRollLoc = cmds.createNode("transform", name=str(orgobj) + '_roll_loc')
                symRollLoc = cmds.createNode("transform", name=str(symobj) + '_roll_loc')

                # sym help loc
                cmds.setAttr(orgRollLoc + '.tx', 1)
                cmds.setAttr(symRollLoc + '.tx', -1)
                cmds.setAttr(orgRollLoc + '.ty', 1)
                cmds.setAttr(symRollLoc + '.ty', 1)

                rig.matrixConstraint(orghelploc, orgRollLoc, maintainOffset=True)
                rig.matrixConstraint(symhelploc, symRollLoc, maintainOffset=True)

                # give help loc rotate
                cmds.setAttr(orghelploc + '.rotate' + axisKey[i], 10)

                # check rotate at two type
                if '-' in axisKey[j]:
                    cmds.setAttr(symhelploc + '.rotate' +
                                 axisKey[j][:-1], -10)
                    orgRollLocPos = cmds.xform(orgRollLoc, q=1, t=1, ws=1)
                    symRollLocPos = cmds.xform(symRollLoc, q=1, t=1, ws=1)

                    orgRollLocPos[0] = round(orgRollLocPos[0], 1)
                    orgRollLocPos[1] = round(orgRollLocPos[1], 1)
                    orgRollLocPos[2] = round(orgRollLocPos[2], 1)

                    symRollLocPos[0] = round(symRollLocPos[0], 1)
                    symRollLocPos[1] = round(symRollLocPos[1], 1)
                    symRollLocPos[2] = round(symRollLocPos[2], 1)

                    if symRollLocPos[0] * -1 == orgRollLocPos[0] and symRollLocPos[1] == orgRollLocPos[1] and \
                            symRollLocPos[2] == orgRollLocPos[2]:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(symobj + '.rotate' + axisKey[j])
                    else:
                        # print 'test'
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(
                            symobj + '.rotate' + axisKey[j][:-1])

                elif '-' not in axisKey[j]:
                    cmds.setAttr(symhelploc + '.rotate' + axisKey[j], 10)
                    orgRollLocPos = cmds.xform(orgRollLoc, q=1, t=1, ws=1)
                    symRollLocPos = cmds.xform(symRollLoc, q=1, t=1, ws=1)

                    orgRollLocPos[0] = round(orgRollLocPos[0], 1)
                    orgRollLocPos[1] = round(orgRollLocPos[1], 1)
                    orgRollLocPos[2] = round(orgRollLocPos[2], 1)

                    symRollLocPos[0] = round(symRollLocPos[0], 1)
                    symRollLocPos[1] = round(symRollLocPos[1], 1)
                    symRollLocPos[2] = round(symRollLocPos[2], 1)

                    if symRollLocPos[0] * -1 == orgRollLocPos[0] and symRollLocPos[1] == orgRollLocPos[1] and \
                            symRollLocPos[2] == orgRollLocPos[2]:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(symobj + '.rotate' + axisKey[j])
                    else:
                        symAxis.append(orgobj + '.rotate' + axisKey[i])
                        symAxis.append(
                            symobj + '.rotate' + axisKey[j] + '-')

                # clean
                cmds.delete(orgRollLoc)
                cmds.delete(symRollLoc)
            j += 1
        i += 1

    cmds.delete(orghelplocGrp, symhelplocGrp)
    axisNote = {}
    for i in range(0, len(symAxis), 2):
        axisNote[symAxis[i]] = symAxis[i + 1]
    return axisNote


def getSdkDestnition(node):
    typ = "front"
    AttrsList = []
    if nodeType(node) == "blendShape":
        AllAlias = aliasAttr(node, q=True)
        AttrsList = [AllAlias[i] for i in range(0, len(AllAlias), 2)]
    else:
        AttrsList = listAttr(node, k=True)
    AttrsList = ["%s.%s" % (node, attr) for attr in AttrsList]
    sdkCnsFront = getConnectedSDKs(AttrsList, typ)
    sdkCnsFront.extend(getMultSDKs(AttrsList))
    if not (sdkCnsFront):
        typ = "after"
    return typ


def exportSDKs(nodes, filePath):
    """
    exports the sdk information based on the provided nodes to a json file
    :param nodes:
    :param filePath:
    :param expType:
    :return:
    """
    sdksToExport_dict = {}
    for node in nodes:
        node = getPynodes([node])[0]
        expType = getSdkDestnition(node)
        sdksToExport_dict.update(getSDKInfoFromNode(node, expType=expType))
    _exportData(sdksToExport_dict, filePath)
    print("Export Successfully!")
    return sdksToExport_dict


def get_all_connected_animation_curves():
    """
    获取场景中所有有效连接的动画曲线
    (既有输入连接又有输出连接的动画曲线)
    :return: 动画曲线节点名称列表
    """
    # 获取场景中所有动画曲线
    all_curves = ls(type='animCurve') or []

    valid_curves = []

    for curve in all_curves:
        # 检查输入连接
        input_connections = listConnections(
            "{}.input".format(curve),
            source=True,
            destination=False,
            plugs=True
        ) or []

        # 检查输出连接
        output_connections = listConnections(
            "{}.output".format(curve),
            source=False,
            destination=True,
            plugs=True
        ) or []

        # 只有同时有输入和输出连接才算有效
        if input_connections and output_connections:
            valid_curves.append(curve)

    return valid_curves


def exportSceneSDKs(filePath):
    """
    exports all the sdk information based on the provided nodes to a json file
    :param filePath:
    :return:
    """
    anim = AnimationCurveIO_API()
    try:
        anim.export_animation_curves(filePath)
    except:
        RuntimeError


def importSDKs(filePath):
    """create sdk nodes from json file, connected to drivers and driven

    Args:
        filePath (string): path to json file
    """
    allSDKInfo_dict = _importData(filePath)
    failedNodes = []
    for sdkName, sdkInfo_dict in allSDKInfo_dict.items():
        try:
            createSDKFromDict(sdkInfo_dict)

        except Exception as e:
            failedNodes.append(sdkName)
            print("{0}:{1}".format(sdkName, e))

    print("Nodes successfully created ---------------------------------")


import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oman
import json
import os


class AnimationCurveIO_API:

    mirror_config = {
        # 基本镜像设置
        0: {
            "mirror_axis": "x",
            "attribute_rules": {
                "translateX": {
                    "x": 1,  # invert/keep/pair
                    "y": 1,
                    "z": 1
                },
                "rotate": {
                    "x": 1,
                    "y": 1,
                    "z": 1
                },
                "scale": {
                    "x": 1,
                    "y": 1,
                    "z": 1
                }
            }
        },
        1: {
            "mirror_axis": "x",
            "attribute_rules": {
                "translate": {
                    "x": -1,  # invert/keep/pair
                    "y": -1,
                    "z": -1
                },
                "rotate": {
                    "x": 1,
                    "y": 1,
                    "z": 1
                },
                "scale": {
                    "x": 1,
                    "y": 1,
                    "z": 1
                }
            }
        },
        2: {
            "mirror_axis": "x",
            "attribute_rules": {
                "translate": {
                    "x": -1,  # invert/keep/pair
                    "y": 1,
                    "z": 1
                },
                "rotate": {
                    "x": 1,
                    "y": -1,
                    "z": -1
                },
                "scale": {
                    "x": 1,
                    "y": 1,
                    "z": 1
                }
            }
        }
    }
    # 切线类型映射
    tangent_type_map = {
        0: "auto",
        1: "fixed",
        2: "linear",
        3: "flat",
        4: "smooth",
        5: "step",
        6: "slow",
        7: "fast",
        8: "clamped",
        9: "plateau",
        10: "stepnext"
    }
    reverse_tangent_type_map = {v: k for k, v in tangent_type_map.items()}

    def get_valid_animation_curves(self):
        """
        使用API 2.0获取所有有效连接的动画曲线
        :return: (MObject列表, 曲线名称列表)
        """
        valid_mobjs = []
        valid_names = []

        # for curve_type in self.curve_types:
        iter = om.MItDependencyNodes(om.MFn.kAnimCurve)

        while not iter.isDone():
            mobj = iter.thisNode()
            dep_node = om.MFnDependencyNode(mobj)

            # 检查输入连接
            input_plug = dep_node.findPlug("input", False)
            input_connected = input_plug.isConnected

            # 检查输出连接
            output_plug = dep_node.findPlug("output", False)
            output_connected = output_plug.isConnected

            # 只有同时有输入和输出连接才算有效
            if input_connected and output_connected:
                valid_mobjs.append(mobj)
                valid_names.append(dep_node.name())

            iter.next()

        return valid_mobjs, valid_names

    def get_curve_data(self, mobj):
        """
        使用API 2.0获取动画曲线数据
        :param mobj: 动画曲线MObject
        :return: 包含曲线数据的字典
        """
        curve_fn = oman.MFnAnimCurve(mobj)
        dep_node = om.MFnDependencyNode(mobj)
        curve_name = dep_node.name()

        input_plug = dep_node.findPlug("input", False)

        output_plug = dep_node.findPlug("output", False)
        # 获取连接信息
        input_conns = self.removeEXnodes(input_plug.name().split('.')[0], True)
        output_conns = self.removeEXnodes(output_plug.name().split('.')[0], False)

        # 获取关键帧数据
        times = []
        values = []
        itt_list = []
        ott_list = []
        in_angles = []
        out_angles = []
        for i in range(curve_fn.numKeys):
            times.append(curve_fn.input(i))
            # value = curve_fn.value(i)
            ia, iv = curve_fn.getTangentAngleWeight(i, True)
            oa, ov = curve_fn.getTangentAngleWeight(i, False)
            value = cmds.getAttr("{0}.keyTimeValue[{1}]".format(curve_name, i))
            values.append(value[0][-1])
            in_angles.append(ia.asRadians())
            out_angles.append(oa.asRadians())
            itt_list.append(curve_fn.inTangentType(i))
            ott_list.append(curve_fn.outTangentType(i))

        return {
            'type': curve_fn.typeName,
            'input_connections': input_conns,
            'output_connections': output_conns,
            'times': times,
            'values': values,
            'in_tangent_types': itt_list,
            'out_tangent_types': ott_list,
            'in_angles': in_angles,
            'out_angles': out_angles,
            'pre_infinity': cmds.getAttr(curve_name + ".preInfinity"),
            'post_infinity': cmds.getAttr(curve_name + ".postInfinity"),
            'is_weighted': curve_fn.isWeighted,
            'is_static': curve_fn.isStatic
        }

    def removeEXnodes(self, nodeName, is_source):
        connections = []
        results = []
        if is_source:
            connections = cmds.listConnections(nodeName + ".input", source=True, destination=False, plugs=True) or []
        else:
            connections = cmds.listConnections(nodeName + ".output", source=False, destination=True, plugs=True) or []

        for conn in connections:
            # 获取连接的节点（去掉属性部分）
            connected_node = conn.split('.')[0]

            # 检查节点类型
            node_type = cmds.objectType(connected_node)

            if node_type in ['unitConversion', 'blendWeighted', 'unitToTimeConversion']:
                # 如果是转换节点，继续递归查找
                connections = self.removeEXnodes(connected_node, is_source)
            else:
                results.append(conn)

        return list(set(connections + results))

    def export_animation_curves(self, file_path):
        """
        使用API 2.0导出动画曲线数据到JSON文件
        :param file_path: 导出文件路径
        """
        mobjs, names = self.get_valid_animation_curves()
        export_data = {}

        for mobj, name in zip(mobjs, names):
            export_data[name] = self.get_curve_data(mobj)

        # 写入JSON文件
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=4)

        print("成功导出 {0} 条动画曲线到 {1}".format(len(export_data), file_path))
        return True

    def exportSdks(self, export_data, file_path):
        # 写入JSON文件
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=4)

        print("成功导出 {0} 条动画曲线到 {1}".format(len(export_data), file_path))
        return True

    def import_animation_curves(self, file_path):
        """
        使用API 2.0从JSON文件导入动画曲线数据
        :param file_path: 导入文件路径
        """
        if not os.path.exists(file_path):
            print("错误: 文件 {} 不存在".format(file_path))
            return False

        with open(file_path, 'r') as f:
            import_data = json.load(f)

        # 重建连接关系
        for old_curve, curve_data in import_data.items():
            for i, output_conn in enumerate(curve_data['output_connections']):
                if cmds.objExists(curve_data['input_connections'][0]) and cmds.objExists(output_conn):
                    for i, output_conn in enumerate(curve_data['output_connections']):
                        animCurrentCrv = getAnimCurve(curve_data['input_connections'][0], output_conn)
                        if not cmds.objExists(output_conn.split('.')[0]) or not cmds.objExists(
                                curve_data['input_connections'][0]):
                            continue
                        if not animCurrentCrv:
                            for k in range(len(curve_data["times"])):
                                cmds.setDrivenKeyframe(output_conn.split('.')[0], at=output_conn.split('.')[1],
                                                       cd=curve_data['input_connections'][0],
                                                       dv=curve_data["times"][k], v=curve_data["values"][k])
                        else:
                            if not self.checkAnimCurveInput(animCurrentCrv[0]):
                                cmds.delete(animCurrentCrv[0])
                                for k in range(len(curve_data["times"])):
                                    cmds.setDrivenKeyframe(output_conn.split('.')[0], at=output_conn.split('.')[1],
                                                           cd=curve_data['input_connections'][0],
                                                           dv=curve_data["times"][k], v=curve_data["values"][k])
                        animCurrentCrv = getAnimCurve(curve_data['input_connections'][0], output_conn)
                        if animCurrentCrv:
                            self.setAnimCurve(animCurrentCrv[0], curve_data)

    def getAnimCurve(self, driverAttr, drivenAttr):
        setdrivenCrv = []
        connections = cmds.listConnections(driverAttr, source=False, destination=True, type="animCurve", scn=True) or []
        if connections:
            for anim in connections:
                driven = self.removeEXnodes(anim, 0)
                if driven:
                    driven = driven[0]
                    if driven == drivenAttr:
                        setdrivenCrv.append(anim)
        return setdrivenCrv

    def setAnimCurve(self, new_curve, curve_data, value_multi=1.0):
        # 设置曲线属性
        selectionList = om.MSelectionList()
        selectionList.add(new_curve)
        curve_node = selectionList.getDependNode(0)

        curve_fn = oman.MFnAnimCurve(curve_node)
        curve_fn.setPreInfinityType(curve_data['pre_infinity'])
        curve_fn.setPostInfinityType(curve_data['post_infinity'])

        times = curve_data['times']
        values = curve_data['values']
        in_tangent_types = curve_data['in_tangent_types']
        out_tangent_types = curve_data['out_tangent_types']
        in_angles = curve_data['in_angles']
        out_angles = curve_data['out_angles']

        if len(times) == curve_fn.numKeys:
            for i, time in enumerate(times):
                curve_fn.setValue(i, math.radians(values[i])*value_multi)
                curve_fn.setInTangentType(i, in_tangent_types[i])
                curve_fn.setOutTangentType(i, out_tangent_types[i])

            for i, time in enumerate(times):
                if in_tangent_types[i] == 1 or out_tangent_types[i] == 1:
                    curve_fn.setAngle(i, om.MAngle(in_angles[i], om.MAngle.kRadians), True)
                    curve_fn.setAngle(i, om.MAngle(out_angles[i], om.MAngle.kRadians), False)

        # for i, time in enumerate(times):
        #     cmds.keyframe(new_curve, e=True, absolute=True, valueChange=values[i]*value_multi)
        #     mel.eval('keyTangent -index %s -e -itt %s -ott %s %s' % (i, in_tangent_types[i],
        #                                                              out_tangent_types[i], new_curve))
        #     mel.eval('keyTangent -index %s -e -ia %s -oa %s %s' % (
        #         i, in_angles[i], out_angles[i], new_curve
        #     ))

    def is_valid_sdk_connection(self, target_plug, source_plug):
        """
        验证两个属性之间是否存在有效的SDK驱动关系

        :param target_plug: 目标属性（动画曲线输入端）
        :param source_plug: 源属性（驱动属性）
        :return: bool
        """
        attr_name = target_plug.partialName(
            includeNodeName=False,
            includeNonMandatoryIndices=False,
            useLongNames=True
        ).lower()

        return attr_name.startswith('input')

    def find_sdk_connections(self, node, is_source, visited=None):
        if visited is None:
            visited = set()

        if node in visited:
            return {'all_nodes': [], 'sdk_nodes': []}

        visited.add(node)

        connections = []
        if is_source:
            connections = cmds.listConnections(node, source=True, destination=False, plugs=False) or []
        else:
            connections = cmds.listConnections(node, source=False, destination=True, plugs=False) or []

        all_nodes = []
        sdk_nodes = []

        for n in connections:
            if 'animCurve' in cmds.objectType(n):
                sdk_nodes.append(n)
            else:
                result = self.find_sdk_connections(n, is_source, visited)
                all_nodes.extend(result['all_nodes'])
                sdk_nodes.extend(result['sdk_nodes'])

            all_nodes.append(n)
        return {
            'all_nodes': list(set(all_nodes)),  # 去重
            'sdk_nodes': list(set(sdk_nodes))  # 去重
        }

    def find_symmetric_attribute(self, attr_name):
        obj, attribute = attr_name.split('.')[0], attr_name.split('.')[1]
        # 常见的对称命名模式
        symmetry_patterns = [
            (r'_L(\D|$)', r'_R\1'),  # _L 和 _R 后缀
            (r'_R(\D|$)', r'_L\1'),
            (r'L_(\D|$)', r'R_\1'),
            (r'R_(\D|$)', r'L_\1'),
            (r'lf_(\D|$)', r'rt_\1'),
            (r'_left(\D|$)', r'_right\1'),  # _left 和 _right 后缀
            (r'_right(\D|$)', r'_left\1'),
            (r'Left(\D|$)', r'Right\1'),  # Left 和 Right 驼峰式
            (r'Right(\D|$)', r'Left\1'),
            (r'\.l(\D|$)', r'.r\1'),  # .l 和 .r 后缀
            (r'\.r(\D|$)', r'.l\1')
        ]

        # 检查属性是否存在
        if 'output' not in attribute:
            if not cmds.attributeQuery(attribute, node=obj, exists=True):
                return {
                    'status': 'error',
                    'message': '属性 {attribute} 在物体 {obj} 上不存在'.format(attribute=attribute, obj=obj)
                }

        # 尝试找到对称物体
        symmetric_obj = None
        if cmds.objectType(obj) == "blendShape":
            symmetric_obj = obj
        else:
            for pattern, replacement in symmetry_patterns:
                symmetric_name = re.sub(pattern, replacement, obj)
                if symmetric_name != obj and cmds.objExists(symmetric_name):
                    symmetric_obj = symmetric_name
                    break

        if not symmetric_obj:
            symmetric_obj = obj

        # 尝试找到对称属性
        symmetric_attr = None
        for pattern, replacement in symmetry_patterns:
            symmetric_attr_name = re.sub(pattern, replacement, attribute)
            if symmetric_attr_name != attribute and cmds.attributeQuery(symmetric_attr_name, node=symmetric_obj,
                                                                        exists=True):
                symmetric_attr = symmetric_attr_name
                break

        if not symmetric_attr:
            if cmds.objExists("{symmetric_obj}.{attribute}".format(symmetric_obj=symmetric_obj, attribute=attribute)):
                symmetric_attr = attribute
            else:
                return {
                    'status': 'attr_not_found',
                    'message': '在对称物体 {symmetric_obj} 上未找到 {attribute} 的对称属性'.format(symmetric_obj=symmetric_obj, attribute=attribute),
                    'symmetric_object': symmetric_obj
                }

        return {
            'status': 'success',
            'original_object': obj,
            'original_attribute': attribute,
            'symmetric_object': symmetric_obj,
            'symmetric_attribute': symmetric_attr
        }

    def getSdkConnections(self, node, is_source):
        sdkNodes = self.find_sdk_connections(node, is_source)["sdk_nodes"]
        sdkConnections = {}
        for animCurve in sdkNodes:
            selectionList = om.MSelectionList()
            selectionList.add(animCurve)
            anim_obj = selectionList.getDependNode(0)

            dep_node = om.MFnDependencyNode(anim_obj)

            input_plug = dep_node.findPlug("input", False)
            input_connected = input_plug.isConnected

            # 检查输出连接
            output_plug = dep_node.findPlug("output", False)
            output_connected = output_plug.isConnected

            # 只有同时有输入和输出连接才算有效
            if (not input_connected) or (not output_connected):
                continue

            anim_data = self.get_curve_data(anim_obj)

            if is_source:
                for out in anim_data["output_connections"]:
                    if node in out:
                        sdkConnections[animCurve] = anim_data
            else:
                if node in anim_data["input_connections"][0]:
                    sdkConnections[animCurve] = anim_data

        return sdkConnections

    def checkAnimCurveInput(self, animCurve):
        isValid = True
        selectionList = om.MSelectionList()
        selectionList.add(animCurve)
        curve_node = selectionList.getDependNode(0)

        curve_fn = oman.MFnAnimCurve(curve_node)
        if curve_fn.numKeys <= 1:
            isValid = False
        return isValid


