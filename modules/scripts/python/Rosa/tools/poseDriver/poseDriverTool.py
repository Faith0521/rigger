# coding:utf-8
import maya.cmds as mc
import pymel.core as pm
from ...maya_utils import aboutCrv
from ...maya_utils import aboutLock


def multiplyCombine(attrA='', attrB='', toAttr=''):
    """
    attrA * attrB to AttrC
    :param attrA:
    :param attrB:
    :param toAttr:
    :return:
    """
    combineNode = pm.createNode('multDoubleLinear', n='%s_combine_mdl' % (toAttr.replace('.', '_')), ss=1)
    mc.connectAttr(attrA, combineNode + '.input1', f=True)
    mc.connectAttr(attrB, combineNode + '.input2', f=True)
    mc.connectAttr(combineNode + '.output', toAttr, f=True)

    # return
    returnDict = {
        'input1': combineNode.i1.inputs(p=True)[0].name(),
        'input2': combineNode.i2.inputs(p=True)[0].name(),
        'output': toAttr
    }
    return returnDict

def constraintBridge(parentObj='', followObj='', parentHandle='', followHandle=''):
    """
    constraint bridge
    :param parentObj:
    :param followObj:
    :param parentHandle:
    :param followHandle:
    :return:
    """
    mc.pointConstraint(followObj, parentHandle, n=parentHandle + '_pc')
    constraintNode = mc.orientConstraint(followObj, parentHandle, n=parentHandle + '_oc', mo=True)[0]

    # rotateOffset
    offsetX = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetX'))
    offsetY = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetY'))
    offsetZ = mc.getAttr('{0}.{1}'.format(constraintNode, 'offsetZ'))
    rotateOffset = [offsetX, offsetY, offsetZ]

    # normalize
    normalizeRotate = [round(rE / 90.0) * 90 for rE in rotateOffset]
    mc.setAttr('{0}.{1}'.format(constraintNode, 'offset'), *normalizeRotate)
    mc.delete(constraintNode)

    # final constraint
    mc.orientConstraint(parentObj, parentHandle, n=parentHandle + '_oc', mo=True)
    mc.parentConstraint(followObj, followHandle, n=followHandle + '_prc', mo=True)

def createBridge(prefix='', axis='+x', mirror=False):
    """
    create pose driver bridge
    :param prefix: prefix '{prefix}_bridge'
    :param axis: default axis
    :param mirror:
    :return:
    """

    # check cmds bridge exists
    if mc.objExists('{0}_psd_cmd_bridge'.format(prefix)):
        return False

    # build data
    # 判断创建朝向的dict
    axisDict = {'AXIS': ['rotateList', 'isReverse'],
                '+x': [(0, 0, 0), False],
                '-x': [(0, 0, 0), True],
                '+y': [(0, 0, -90), True],
                '-y': [(0, 0, -90), False],
                '+z': [(0, -90, 0), False],
                '-z': [(0, -90, 0), True]}

    # 不同轴向的属性名dict
    attrNameDict = {'x': ['up', 'down', 'front', 'back'],
                    'y': ['outer', 'inner', 'front', 'back'],
                    'z': ['up', 'down', 'inner', 'outer']}

    # 平面角度区间判断的dict
    driverAxisDict = {'sort': [0, 1, 2, 3],
                      0: [-90, -180, 180, 90],
                      1: [-90, 0, 90],
                      2: [-180, -90, 0],
                      3: [180, 90, 0]}

    followCurvePointList = [(0.0, 0.0, 0.0), (-5.0, 0.0, 0.0)]

    parentCurvePointList = [(0.0, -3.5, 0.0), (1.5543122344752192e-15, -5.0, 3.3306690738754706e-16),
                            (4.440892098500626e-16, -3.535533905029297, 3.535533905029297),
                            (-1.1102230246251565e-15, 1.1102230246251565e-16, 5.0), (0.0, 0.0, 3.5),
                            (-1.1102230246251565e-15, 1.1102230246251565e-16, 5.0),
                            (-2.0141816681326294e-15, 3.535533905029297, 3.535533905029297),
                            (-1.5543122344752192e-15, 5.0, -2.220446049250314e-16),
                            (-4.440892098500626e-16, 3.535533905029297, -3.535533905029297),
                            (1.1102230246251565e-15, -3.3306690738754696e-16, -5.0),
                            (2.0141816681326294e-15, -3.535533905029297, -3.535533905029297),
                            (1.5543122344752192e-15, -5.0, 3.3306690738754706e-16),
                            (0.0, -3.5, 0.0)]

    followPosition = [5, 0, 0]  # 指向默认位置的向量  绝对角度的起点
    downPosition = [0, -5, 0]  # 指向down的向量  平面角度的起点
    parentRotate = axisDict[axis][0]

    # side
    sideReverse = axisDict[axis][1]
    if mirror:
        sideReverse = not sideReverse
        parentRotate = [rE * -1 for rE in parentRotate]
    if sideReverse:
        followCurvePointList = [[listE2 * -1 for listE2 in listE] for listE in followCurvePointList]
        followPosition = [vE * -1 for vE in followPosition]

    # build
    followHandle = mc.curve(n='{0}_psd_follow_handle'.format(prefix), d=1, p=followCurvePointList)
    parentHandle = mc.curve(n='{0}_psd_parent_handle'.format(prefix), d=1, p=parentCurvePointList)
    cmdBridge = mc.createNode('transform', n='{0}_psd_cmd_bridge'.format(prefix))
    mc.parent(followHandle, cmdBridge, parentHandle)
    mc.setAttr('{0}.t'.format(followHandle), *followPosition)
    mc.setAttr('{0}.r'.format(parentHandle), *parentRotate)

    # modify handle curve
    for handle in [followHandle, parentHandle]:
        aboutCrv.setShapeName(handle)
        aboutCrv.setShapeColor(handle, 30)
        aboutCrv.setShapeWidth(handle, 5)
        aboutLock.lock(handle)
        aboutLock.unlock(handle, 't r')

    # modify cmds bridge
    aboutLock.lock(cmdBridge)

    # angle angleBetween
    angleABName = mc.createNode('angleBetween', n='{0}_psd_base_alb'.format(prefix))
    for axisE in 'xyz':
        mc.connectAttr('{0}.t{1}'.format(followHandle, axisE), '{0}.v1{1}'.format(angleABName, axisE))
    mc.setAttr('{0}.v2'.format(angleABName), *followPosition)

    # plane angleBetween
    planeABName = mc.createNode('angleBetween', n='{0}_psd_plane_alb'.format(prefix))
    mc.connectAttr('{0}.ty'.format(followHandle), '{0}.v1y'.format(planeABName))
    mc.connectAttr('{0}.tz'.format(followHandle), '{0}.v1z'.format(planeABName))
    mc.setAttr('{0}.v2'.format(planeABName), *downPosition)

    # plane condition
    angleCNode = mc.createNode('condition', n='{0}_psd_angle_cnd'.format(prefix))
    mc.setAttr('{0}.operation'.format(angleCNode), 2)
    mc.connectAttr('{0}.tz'.format(followHandle), '{0}.ft'.format(angleCNode))
    mc.connectAttr('{0}.a'.format(planeABName), '{0}.ctr'.format(angleCNode))
    mc.connectAttr('{0}.a'.format(planeABName), '{0}.cfr'.format(angleCNode))

    # input reverse
    unitConversionList = mc.listConnections('{0}.ctr'.format(angleCNode), d=False)
    if unitConversionList:
        mc.setAttr('{0}.conversionFactor'.format(unitConversionList[0]), mc.getAttr('{0}.conversionFactor'.format(unitConversionList[0])) * -1)

    # 单方向sdk
    inputUnitConversion = []
    intputAttr = []

    for keyE in driverAxisDict['sort']:
        angleList = driverAxisDict[keyE]
        attrName = '{0}.{1}'.format(cmdBridge, attrNameDict[axis[1]][keyE])
        mc.addAttr(cmdBridge, ln=attrNameDict[axis[1]][keyE], at='double', dv=0, k=True)

        for angleE in angleList:
            sdkValue = 0
            if angleE in angleList[1:-1]:
                sdkValue = 1
            remapSDK(attrName, dv=angleE, v=sdkValue, cd='{0}.ocr'.format(angleCNode))
            intputAttr = mc.listConnections(attrName, d=False, p=True)

        if inputUnitConversion:
            multiplyCombine(intputAttr[0], inputUnitConversion, attrName)
        else:
            connectDict = multiplyCombine(intputAttr[0], '{0}.a'.format(angleABName), attrName)
            inputUnitConversion = connectDict['input2']

    # 斜方向sdk
    for prefixStrIndex in driverAxisDict['sort'][:2]:
        prefixStr = attrNameDict[axis[1]][prefixStrIndex]

        for suffixStrIndex in driverAxisDict['sort'][2:]:
            suffixStr = attrNameDict[axis[1]][suffixStrIndex]
            attrStr = '{0}{1}'.format(prefixStr, suffixStr.title())
            attrName = '{0}.{1}'.format(cmdBridge, attrStr)
            mc.addAttr(cmdBridge, ln=attrStr, at='double', dv=0, k=True)

            sdk0List = []
            for zeroListE in (driverAxisDict[prefixStrIndex], driverAxisDict[suffixStrIndex]):
                angleList = zeroListE[1:-1]
                if len(angleList) > 1:
                    if driverAxisDict[suffixStrIndex][1] > 0:
                        sdk0List.append(angleList[1])
                    elif driverAxisDict[suffixStrIndex][1] < 0:
                        sdk0List.append(angleList[0])
                else:
                    sdk0List.append(angleList[0])

            sdk1Angle = (sdk0List[0] + sdk0List[1]) / 2.0
            remapSDK(attrName, dv=sdk1Angle, v=1, cd='{0}.ocr'.format(angleCNode))
            remapSDK(attrName, dv=sdk0List[0], v=0, cd='{0}.ocr'.format(angleCNode))
            remapSDK(attrName, dv=sdk0List[1], v=0, cd='{0}.ocr'.format(angleCNode))

            # multipy angle
            intputAttr = mc.listConnections(attrName, d=False, p=True)
            multiplyCombine(intputAttr[0], inputUnitConversion, attrName)

    # tag
    mc.addAttr(parentHandle, ln='tag', dt='string')
    mc.setAttr('{0}.tag'.format(parentHandle), 'poseDriver', type='string')

    # return
    result = {'parent':parentHandle, 'follow':followHandle, 'cmd':cmdBridge}
    return result

def scaleBridge(prefix='', value=0.5):
    """
    scale pose driver
    :param prefix:
    :param value:
    :return:
    """

    # init data
    parentHandle = '{0}_psd_parent_handle'.format(prefix)
    followHandle = '{0}_psd_follow_handle'.format(prefix)

    # if not find Parent handle, return.
    if not mc.objExists(parentHandle) or not mc.objExists(followHandle):
        return
    mc.scale(value, value, value, '{0}.cv[*]'.format(parentHandle), '{0}.cv[*]'.format(followHandle))

    # scale tranlate
    constrainNode = mc.parentConstraint(followHandle, q=True)

    if constrainNode:
        attrStr = '{0}.tg[0].tot'.format(constrainNode)
    else:
        attrStr = '{0}.t'.format(followHandle)

    for axisE in 'xyz':
        fullAttrStr = '{0}{1}'.format(attrStr, axisE)
        mc.setAttr(fullAttrStr, mc.getAttr(fullAttrStr) * value)

def remapSDK(toAttr='', dv=0.0, v=0.0, cd=''):
    """
    use remapValue node instance setDrivenKey node
    :param toAttr:
    :param dv:
    :param v:
    :param cd:
    :return:
    """

    # createNode
    rvNode = '{0}_rv'.format(toAttr.replace('.', '_'))

    if not mc.objExists(rvNode):
        mc.createNode('remapValue', n=rvNode)
        mc.removeMultiInstance('{0}.value[1]'.format(rvNode), b=True)
        mc.removeMultiInstance('{0}.value[0]'.format(rvNode), b=True)

        # connect
        mc.connectAttr(cd, '{0}.inputValue'.format(rvNode))
        mc.connectAttr('{0}.outValue'.format(rvNode), toAttr)

    # get Index
    index = 0
    attrList = mc.listAttr(rvNode + '.value', m=True)
    if attrList:
        index = len(attrList) // 4

    # setValue
    mc.setAttr('{0}.value[{1}].value_Position'.format(rvNode, index), dv)
    mc.setAttr('{0}.value[{1}].value_FloatValue'.format(rvNode, index), v)
    mc.setAttr('{0}.value[{1}].value_Interp'.format(rvNode, index), 1)