import maya.cmds as mc
import maya.OpenMaya as om
from importlib import reload

from rxCore import aboutMath
from rxCore import aboutName
from rxCore import aboutPublic
from rxCore import aboutApi
from rxCore import aboutCrv

reload(aboutMath)


def controlCvs(crvName, mpnode=None):
    if mpnode is None:
        mpnode = 'controlCvPoints'

    ctrls = []
    crvs = mc.ls(crvName + '.cv[:]', fl=1)

    for i, point in enumerate(crvs):
        pos = mc.xform(point, q=1, t=1, ws=1)

        ctrl = mc.spaceLocator(p=(0, 0, 0), name='%s_%s_control_loc' % (crvName, i))[0]
        mc.xform(ctrl, ws=True, t=pos)

        ctrlShape = mc.listRelatives(ctrl, s=True)[0]
        crvShape = mc.listRelatives(crvName, s=True)[0]
        mc.connectAttr('%s.worldPosition' % ctrlShape, '%s.controlPoints[%s]' % (crvShape, i))
        aboutPublic.fastGrp(ctrl, grpNameList=['grp'])
        ctrls.append(ctrl)

    # clean
    if not mc.objExists(mpnode):
        mc.createNode('transform', n=mpnode)
        mc.hide(mpnode)

    for ctrl in ctrls:
        mc.parent(ctrl + '_grp', mpnode)

    return ctrls


def posListOnCrv(crvName, numbs, ev=0, start=0, end=1):
    """
    return avege postion list on crv
    """
    itsShape = mc.listRelatives(crvName, shapes=True, fullPath=True)
    if itsShape is None or not mc.objectType(itsShape[0], isType='nurbsCurve'):  # no shape object
        raise TypeError('must a curve input')

    curveFn = aboutApi.asMFnNurbsCurve(crvName)
    length = curveFn.length(0.01)
    sepLens = aboutMath.averageNumber(ev, numbs)
    sepLensRmp = aboutMath.remapValue(sepLens, [0, 1], [start, end])
    position = om.MPoint()
    posList = []
    for lgh in sepLensRmp:
        param = curveFn.findParamFromLength(lgh * length)
        position = curveFn.getPointAtParam(param, om.MSpace.kWorld)
        posList.append((position[0], position[1], position[2]))
    return posList


def createJntByCrv(prefix, crvName, jointNum, orientRef, continuous=1, mpNode=None):
    # mpNode
    if mpNode is None:
        mpNode = prefix + '_ribbon_jnt_grp'
    if not mc.objExists(mpNode):
        mc.createNode('transform', n=mpNode)
        mc.select(cl=1)

    jntList = []
    posList = posListOnCrv(crvName, (jointNum - 1), ev=0, start=0, end=1)

    for i in range(len(posList)):
        mc.select(cl=1)
        jnt = mc.joint(p=posList[i], n=prefix + aboutName.letter(i) + '_drv')
        mc.delete(mc.orientConstraint(orientRef, jnt))
        mc.makeIdentity(jnt, apply=True, t=0, r=1, s=0)
        jntList.append(jnt)

    if continuous:
        for i in range(len(jntList)):
            if i != len(jntList) - 1:
                mc.parent(jntList[i + 1], jntList[i])
        mc.parent(jntList[0], mpNode)
    else:
        for i in range(len(jntList)):
            mc.parent(jntList[i], mpNode)

    # if not orientRef:
    #     mc.joint(jntList[0], e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    #     mc.joint(jntList[-1], e=True, oj='none', secondaryAxisOrient='yup', ch=True, zso=True)

    return jntList


def nearestPointOnCurve(curve, node):
    """
    Find the nearest point on a curve, the function will return
    the parameter and point. The point is of type om.MPoint.

    :param str curve:
    :param str node:
    :return: parameter, point
    :rtype: float, om.MPoint
    """
    pos = aboutApi.toMPoint(node)
    mFnCurve = aboutApi.asMFnNurbsCurve(curve)

    pUtil = om.MScriptUtil()
    pPtr = pUtil.asDoublePtr()

    point = mFnCurve.closestPoint(
        pos,
        pPtr,
        0.001,
        om.MSpace.kWorld
    )

    return pUtil.getDouble(pPtr)


def nearestParameterOnCurve(curve, node):
    """
    Find the nearest point on a curve, the function will return
    the parameter and point. The point is of type om.MPoint.

    :param str curve:
    :param str node:
    :return: parameter
    :rtype: float
    """
    mFnCurve = aboutApi.asMFnNurbsCurve(curve)
    nearestPoint = nearestPointOnCurve(curve, node)[1]
    pUtil = om.MScriptUtil()
    pPtr = pUtil.asDoublePtr()
    mFnCurve.getParamAtPoint(nearestPoint, pPtr, 0.001, om.MSpace.kWorld)

    return pUtil.getDouble(pPtr)


def splitCurveToParametersByNodes(curve, nodes):
    """
    Get a list of parameters from nodes, based on the
    length of the curve. Ranges are normalizes to be between 0-1.

    :param str curve:
    :param list nodes:
    :return: parameters
    :rtype: list
    """

    num = len(nodes)

    # get parameters
    parameters = []
    for i in range(num):
        parameter = nearestParameterOnCurve(curve, nodes[i])
        parameters.append(parameter)

    # normalize
    factor = parameters[-1]
    parameters = [p / factor for p in parameters]

    if mc.getAttr("{0}.form".format(curve)) == 2:
        parameters.insert(0, parameters[-1])
        parameters.pop(-1)

    return parameters


def splitCurveToParametersByLength(curve, num):
    """
    Get a list of parameters evenly spaced along a curve, based on the
    length of the curve. Ranges are normalizes to be between 0-1.

    :param str curve:
    :param int num:
    :return: parameters
    :rtype: list
    """
    mFnCurve = aboutApi.asMFnNurbsCurve(curve)
    increment = 1.0 / (num - 1)

    # get parameters
    parameters = []
    for i in range(num):
        parameter = mFnCurve.findParamFromLength(
            mFnCurve.length() * increment * i
        )
        parameters.append(parameter)

    # normalize
    factor = parameters[-1]
    parameters = [p / factor for p in parameters]

    if mc.getAttr("{0}.form".format(curve)) == 2:
        parameters.insert(0, parameters[-1])
        parameters.pop(-1)

    return parameters


def splitCurveToParametersByParameter(curve, num):
    """
    Get a list of parameters evenly spaced along a curve, based on the
    division of its parameters. Ranges are normalizes to be between 0-1.

    :param str curve:
    :param int num:

    :return: parameters
    :rtype: list
    """
    increment = 1.0 / (num - 1)
    parameters = [i * increment for i in range(num)]

    if mc.getAttr("{0}.form".format(curve)) == 2:
        parameters.insert(0, parameters[-1])
        parameters.pop(-1)

    return parameters


def clusterCurve(prefix, curve):
    """
    Create a cluster on each cv of a curve.

    :param str prefix:
    :param str curve:
    :return: List of created clusters
    :rtype: list of strings
    """
    clusters = []

    # get num cvs on curve
    num = aboutCrv.numCVs(curve)

    # create clusters
    for i in range(num):
        # create cluster
        clusterShape, clusterTransform = mc.cluster("{0}.cv[{1}]".format(curve, i))

        # rename shape and transform
        mc.rename(clusterShape, "{0}_clusterShape_{1:03d}".format(prefix, i + 1))
        clusterTransform = mc.rename(clusterTransform, "{0}_cluster_{1:03d}".format(prefix, i + 1))

        # set and lock visibility
        mc.setAttr("{0}.visibility".format(clusterTransform), 0)
        mc.setAttr("{0}.visibility".format(clusterTransform), lock=True)

        # store transform
        clusters.append(clusterTransform)

    return clusters

def createFollicle(
        prefix,
        curve,
        parameter,
        forwardDirection='y',
        upDirection='x',
        overrideNormal=None,
        subtractPositionFromNormal=False):
    """
    Create a follicle on a curve. The name will be used for the
    creation of all of the nodes. The overrideNormal attribute can be
    used if the up vector needs to be any different then what the
    curve can provide, this can be the translation attribute of a
    transform. The subtractPositionFromNormal can be used of the
    normal parsed is in world space, this means that the normal will
    be converted to local space.

    :param str prefix:
    :param str curve: curve to attach follicle too
    :param float parameter: parameter on curve between 0-1
    :param str forwardDirection: ('x', 'y', 'z'), default 'z'
    :param str upDirection: ('x', 'y', 'z'), default 'y'
    :param str overrideNormal: override normal connection, (eg. translate)
    :param bool subtractPositionFromNormal: subtract the position from the normal
    :return: locator, pointOnCurve, aimConstraint
    :rtype: tuple
    """
    # catch numbered naming
    suffix = ''
    sections = prefix.rsplit('_', 1)
    if sections[-1].isdigit():
        prefix = sections[0]
        suffix = '_{0}'.format(sections[-1])

    # create follicle
    loc = mc.spaceLocator(n='{0}_loc{1}'.format(prefix, suffix))[0]
    mc.setAttr('{0}.inheritsTransform'.format(loc), 0)
    mc.setAttr('{0}.localScale'.format(loc), 0.1, 0.1, 0.1)

    # create point on curve node
    poc = mc.createNode('pointOnCurveInfo', n='{0}_poc{1}'.format(prefix, suffix))

    # connect to curve
    mc.setAttr('{0}.parameter'.format(poc), parameter)
    mc.setAttr('{0}.turnOnPercentage'.format(poc), 1)
    mc.connectAttr('{0}.worldSpace'.format(curve), '{0}.inputCurve'.format(poc))

    # catch override normal
    normalAttribute = '{0}.normalizedNormal'.format(poc)
    if overrideNormal:
        normalAttribute = overrideNormal

    # catch subtract position from normal
    if subtractPositionFromNormal:
        pma = mc.createNode('plusMinusAverage', n='{0}_pma{1}'.format(prefix, suffix))

        mc.setAttr('{0}.operation'.format(pma), 2)
        mc.connectAttr(normalAttribute, '{0}.input3D[0]'.format(pma))
        mc.connectAttr('{0}.result.position'.format(poc), '{0}.input3D[1]'.format(pma))

        normalAttribute = '{0}.output3D'.format(pma)

    # create vectors
    forwardVector = aboutMath.convertAxisToVector(forwardDirection)
    upVector = aboutMath.convertAxisToVector(upDirection)

    # create aim constraint
    aim = mc.createNode('aimConstraint', n='{0}_aim{1}'.format(prefix, suffix))
    mc.parent(aim, loc)

    # set aim constraint
    mc.setAttr('{0}.tg[0].tw'.format(aim), 1)
    mc.setAttr('{0}.worldUpType'.format(aim), 3)
    mc.setAttr('{0}.aimVector'.format(aim), *forwardVector)
    mc.setAttr('{0}.upVector'.format(aim), *upVector)

    mc.connectAttr('{0}.tangent'.format(poc), '{0}.tg[0].tt'.format(aim))
    mc.connectAttr(normalAttribute, '{0}.worldUpVector'.format(aim))

    # connect to locator
    mc.connectAttr('{0}.result.position'.format(poc), '{0}.translate'.format(loc))
    mc.connectAttr('{0}.constraintRotate'.format(aim), '{0}.rotate'.format(loc))

    return loc, poc, aim


def createUpVectors(prefix, twistCtrls, Parameters, upDirection='x'):
    """
    Create a object twist upvectors .

    :param str prefix: node first name.
    :param list twistCtrls: twist start / end locator or controls
    :param list Parameters: parameter on curve between 0-1
    :param str upDirection: ('x', 'y', 'z'), default 'y'
    :return: wtAddMatrix, plusMinusAverage
    :rtype: tuple
    """

    # variables
    ups = []
    blends = []
    weights = aboutMath.remapWeighting(Parameters, [0.0, 1.0])

    if len(twistCtrls) != 2:
        mc.error('Only Support Two twistCtrls')

    # loop weights
    for i, weight in enumerate(weights):
        # create blend matrix
        bm = mc.createNode('wtAddMatrix', n='{0}_bm_{1:03d}'.format(prefix, i + 1))

        # blend cluster weights
        for j, k in enumerate(weight.keys()):
            # get control
            control = twistCtrls[k]

            # set blend weight
            mc.setAttr('{0}.wtMatrix[{1}].weightIn'.format(bm, j), weight[k])

            # connect to control
            mc.connectAttr('{0}.worldMatrix[0]'.format(control), '{0}.wtMatrix[{1}].matrixIn'.format(bm, j))

        # multiply up vector
        pmm = mc.createNode('pointMatrixMult', n='{0}_up_pmm_{1:03d}'.format(prefix, i + 1))

        mc.setAttr('{0}.vectorMultiply'.format(pmm), 1)
        mc.setAttr('{0}.inPoint{1}'.format(pmm, upDirection.upper()), 100)
        mc.connectAttr('{0}.matrixSum'.format(bm), '{0}.inMatrix'.format(pmm))

        # decompose blend matrix
        dm = mc.createNode('decomposeMatrix', n='{0}_up_dm_{1:03d}'.format(prefix, i + 1))

        mc.connectAttr('{0}.matrixSum'.format(bm), '{0}.inputMatrix'.format(dm))

        # add up with blend
        pma = mc.createNode('plusMinusAverage', n='{0}_up_pma_{1:03d}'.format(prefix, i + 1))

        mc.connectAttr('{0}.output'.format(pmm), '{0}.input3D[0]'.format(pma))

        mc.connectAttr('{0}.outputTranslate'.format(dm), '{0}.input3D[1]'.format(pma))

        # store nodes
        blends.append(bm)
        ups.append(pma)

    return blends, ups

def createPointOnCurve(prefix, curve, nodes, twistCtrls, upDirection='x', forwardDirection='y'):
    """
    Create a object twist upvectors .

    :param str prefix: node first name.
    :param str curve: node curve name.
    :param list twistCtrls: twist start / end locator or controls
    :param list nodes: get nodes parameter on curve between 0-1
    :param str upDirection: ('x', 'y', 'z'), default 'y'
    :param str forwardDirection: ('x', 'y', 'z'), default 'x'
    :return: wtAddMatrix, plusMinusAverage
    :rtype: tuple
    """

    pocs = []
    aims = []

    if len(twistCtrls) != 2:
        return

    Parameters = splitCurveToParametersByNodes(curve, nodes)
    blends, ups = createUpVectors(prefix, twistCtrls, Parameters, upDirection)

    for i, parameter in enumerate(Parameters):
        # create locator follicle
        loc, poc, aim = createFollicle(
            "{0}_{1:03d}".format(prefix, i + 1),
            curve,
            parameter=parameter,
            upDirection = upDirection,
            forwardDirection = forwardDirection,
            overrideNormal="{0}.output3D".format(ups[i]),
            subtractPositionFromNormal=True
        )
        mc.connectAttr(aim + '.constraintRotate', nodes[i]+'.rotate')
        mc.connectAttr(poc + '.position', nodes[i] + '.translate')
        aims.append(aim)
        pocs.append(poc)

        mc.parent(aim, world=True)
        # remove locator, will be replaced with joint later
        mc.delete(loc)

    return pocs, aims