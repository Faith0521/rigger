# coding: utf-8
#=============================================
# author: rosa_w
#   mail: wrx1844@qq.com
#   date: Wed, 25 Jun 2019 12:03:02
#=============================================
import sys
import maya.cmds as mc
import maya.mel as mel

import pickle
import maya.OpenMaya as om

from . import aboutApi
from . import aboutPublic

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def undoable(function):
    """A decorator that will make commands undoable in maya"""

    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None

        # noinspection PyBroadException
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print (sys.exc_info()[1])

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def readCrvData(crvDataPath):
    f = open(crvDataPath, 'r')
    text = ''
    for i in f.readlines():
        text = text + i
    mel.eval(text)
    f.close()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def addShape(crvName, data):
    shapeNode = mc.createNode('nurbsCurve', n=crvName + 'Shape', p=crvName)
    if data:
        readCrvData(data)
    return shapeNode

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def replaceShape(crvName, crvData):
    shapes = mc.listRelatives(crvName, f=1, s=1)
    for shape in shapes:
        mc.delete(shape)
    result = addShape(crvName, crvData)
    return result

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def createCrv(crvName, crvData):
    # name
    crv = mc.createNode('transform', n=crvName)
    # shape
    if crvData:
        addShape(crv, crvData)
    return crv

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def mirrorCrvShape(crv, axisMirrors='x', search='lf_', replace='rt_'):
    axisInfo = []
    if axisMirrors == 'x':
        axisInfo = [-1, 1, 1]
    if axisMirrors == 'y':
        axisInfo = [1, -1, 1]
    if axisMirrors == 'z':
        axisInfo = [1, 1, -1]

    crvShapes = mc.listRelatives(crv, s=True)
    mirrorCrv = aboutPublic.checkSymObj(orgObj=[crv], searchFor=search, replaceWith=replace)
    mirrorShapes = mc.listRelatives(mirrorCrv, s=True)

    if len(crvShapes) == len(mirrorShapes):
        for i in range(len(crvShapes)):
            cvNum = len(mc.ls(str(crvShapes[i]) + '.cv[*]', fl=True))

            for j in range(cvNum + 2):
                pos = mc.xform(crvShapes[i] + '.cv[' + str(j) + ']', q=True, ws=True, t=True)
                mc.xform(mirrorShapes[i] + '.cv[' + str(j) + ']', t=(pos[0] * axisInfo[0], pos[1] * axisInfo[1], pos[2] * axisInfo[2]), ws=True)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def copyShape(nodes=None, copyColor=True, mirror=False):

    # if san lian
    if nodes is None:
        nodes = []
    if not nodes:
        nodes = mc.ls(sl=1)
    if not len(nodes) == 2:
        return

    srcCtrl = nodes[0]
    dstCtrl = nodes[1]

    srcShapes = mc.listRelatives(srcCtrl, type='nurbsCurve', s=1)
    dstShapes = mc.listRelatives(dstCtrl, type='nurbsCurve', s=1)

    if dstShapes:
        for ns in dstShapes:
            if mc.nodeType(ns)=='nurbsCurve':
                mc.delete(ns)

    newnode = mc.duplicate(srcCtrl, rr=1)
    dstShapes = mc.listRelatives(newnode, s=1)
    mc.parent(dstShapes, dstCtrl, r=1, s=1)

    if srcShapes :
        for i in range(len(srcShapes)):
            newShape = dstShapes[i].replace(newnode[0], dstCtrl)
            newShape = mc.rename(dstShapes[i], newShape)

            cvs = mc.ls (srcShapes[i]+'.cv[*]', fl=1)
            newcvs = mc.ls(newShape+'.cv[*]', fl=1)

            for j in range(len(cvs)):
                if not mirror:
                    mc.xform(newcvs[j], ws=1, t=mc.xform(cvs[j], q=1, ws=1, t=1))
                else:
                    pos = mc.xform (cvs[j], q=1, ws=1, t=1)
                    mc.xform(newcvs[j], ws=1, t=[pos[0]*-1, pos[1], pos[2]])

    mc.delete(newnode)

    if copyColor:
        mc.setAttr(dstCtrl+'.overrideEnabled', 1)
        mc.setAttr(dstCtrl+'.overrideDisplayType', 0)
        mc.setAttr(dstCtrl+'.overrideColor', mc.getAttr(srcCtrl+'.overrideColor'))
        try:
            mc.setAttr(dstCtrl+'.overrideRGBColors', mc.getAttr(srcCtrl+'.overrideRGBColors'))
            v = mc.getAttr (srcCtrl +'.overrideColorRGB')[0]
            mc.setAttr(dstCtrl+'.overrideColorRGB', v[0], v[1], v[2])
        except:
            pass

    mc.select(nodes[1])
    return mc.listRelatives(dstCtrl, type='nurbsCurve', s=1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getUserAttr(con):
    udAttr = mc.listAttr(con, k=True, ud=True)
    if udAttr:
        udData = [[att, mc.getAttr(con + '.' + att)] for att in udAttr]
    else:
        udData = []

    return udData

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def setUserAttr(con, conData):
    for att in conData:
        if mc.attributeQuery(att[0], node=con, ex=True):
            mc.setAttr(con + '.' + att[0], att[1])

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def setCurveShape(shapeData, editShape=True):
    if shapeData:
        for crvData in shapeData:
            crvName = crvData[0]
            if mc.objExists(crvName):
                vtxDatas = crvData[1]
                if editShape:
                    for i, pos in enumerate(vtxDatas):
                        mc.xform(crvName + '.cv[' + str(i) + ']', t=pos, wd=True, ws=False)
                else:
                    mc.xform(crvName, m=crvData[1], p=False)
                    mc.setAttr(crvName + '.sx', crvData[2][0])
                    mc.setAttr(crvName + '.sy', crvData[2][1])
                    mc.setAttr(crvName + '.sz', crvData[2][2])
                    mc.setAttr(crvName + '.rx', crvData[3][0])
                    mc.setAttr(crvName + '.ry', crvData[3][1])
                    mc.setAttr(crvName + '.rz', crvData[3][2])

                    if crvData[4]:  # 恢复旋转属性
                        setUserAttr(crvName, crvData[4])

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getCurveShape(curves, editShape=True):

    # if shapeSign:  # 得到shape信息
    shapeData = []
    if editShape:
        for crv in curves:
            curveShapes = mc.listRelatives(crv, s=True, ni=False)
            for crvShape in curveShapes:
                Data = [crvShape, [mc.xform(vtx, q=True, t=True, wd=True, ws=False) for vtx in mc.ls(
                    crvShape + '.cv[*]', fl=True)]]
                shapeData.append(Data)

    else:  # 得到transform信息
        shapeData = [[crv, mc.getAttr(crv + '.matrix'), [mc.getAttr(crv + '.sx'), mc.getAttr(crv + '.sy'), mc.getAttr(
            crv + '.sz')], mc.xform(crv, q=True, ro=True, wd=True, r=True), getUserAttr(crv)]for crv in curves]

    return shapeData

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def exportCurveShape(crvs):
    if not crvs:
        crvs = mc.ls(sl=True)

    filePath = mc.fileDialog(dm='*.cs', m=1)
    if filePath:
        if 'cs' != filePath.split('.')[-1]:
            filePath += '.cs'
        shapeData = getCurveShape(crvs)
        newFile = open(filePath, 'wb')
        pickle.dump(shapeData, newFile)
        newFile.close()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def importCurveShape():
    filePath = mc.fileDialog(dm='*.cs', m=0)
    if filePath:
        readFile = open(filePath, 'rb')
        shapeData = pickle.load(readFile)
        readFile.close()
        setCurveShape(shapeData)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def editCrvHull(crvName, xyzValue=None, modifyType='rotate', editPivetType='shapeCenter'):

    if xyzValue is None:
        xyzValue = [0, 0, 0]

    #pointsMounts =
    crvShapes = mc.listRelatives(crvName, s=True)
    pointsMounts = None
    cvAllX = []
    cvAllY = []
    cvAllZ = []

    # get pivot point.
    for crvShape in crvShapes:
        spans = mc.getAttr(str(crvShape) + '.spans')
        degree = mc.getAttr(str(crvShape) + '.degree')
        pointsMounts = spans + degree

        for i in range(pointsMounts):
            pointcvPos = mc.xform(
                str(crvShape) + '.cv[' + str(i) + ']', q=True, t=True, ws=True)

            cvAllX.append(pointcvPos[0])
            cvAllY.append(pointcvPos[1])
            cvAllZ.append(pointcvPos[2])

    centerPivet = []
    if editPivetType == 'shapeCenter':
        pointCVposXMin = cvAllX[0]
        pointCVposYMin = cvAllY[0]
        pointCVposZMin = cvAllZ[0]

        pointCVposXMax = cvAllX[0]
        pointCVposYMax = cvAllY[0]
        pointCVposZMax = cvAllZ[0]

        for k in range(len(cvAllX)):
            pointCVposXMin = min(pointCVposXMin, cvAllX[k])
            pointCVposXMax = max(pointCVposXMax, cvAllX[k])

            pointCVposYMin = min(pointCVposYMin, cvAllY[k])
            pointCVposYMax = max(pointCVposYMax, cvAllY[k])

            pointCVposZMin = min(pointCVposZMin, cvAllZ[k])
            pointCVposZMax = max(pointCVposZMax, cvAllZ[k])

        centerPivetX = (pointCVposXMin + pointCVposXMax) / 2
        centerPivetY = (pointCVposYMin + pointCVposYMax) / 2
        centerPivetZ = (pointCVposZMin + pointCVposZMax) / 2

        centerPivet = [centerPivetX, centerPivetY, centerPivetZ]

    elif editPivetType == 'objectCenter':
        centerPivet = mc.xform(crvName, q=True, ws=True, t=True)

    # edit.
    for crvShape in crvShapes:
        if modifyType == 'rotate':
            mc.rotate(xyzValue[0], xyzValue[1], xyzValue[2], str(crvShape) + '.cv[0:' + str(pointsMounts) + ']',
                      os=True, r=True, p=centerPivet)
        elif modifyType == 'scale':
            mc.scale(xyzValue[0], xyzValue[1], xyzValue[2], str(crvShape) + '.cv[0:' + str(pointsMounts) + ']',
                     r=True, p=centerPivet)




def getCrvCached(crvName):

    #1
    crvShape = mc.listRelatives(crvName, f=True, s=True)[0]
    onelineData = '    setAttr ".cc" -type "nurbsCurve" \n'

    #2
    degree = mc.getAttr(crvShape+'.degree')
    spans = mc.getAttr(crvShape+'.spans')
    form = mc.getAttr(crvShape+'.form')
    rational = 'no'
    dimension = 3
    twolineData = '        '+str(degree)+' '+str(spans)+' '+str(form)+' '+str(rational)+' '+str(dimension) + '\n'

    #3
    crvObj = aboutApi.toMDagPath(crvShape)
    knots = crvObj.getKnots()
    knotsNum = len(knots)
    threeline = '        '
    threeline += str(knotsNum)+' '
    for knot in knots:
        threeline += str(knot)+' '
    threeline += '\n'

    #4
    cvs = mc.ls(crvShape + '.cv[*]', fl=True)
    fourline = ''
    fourline += '        ' + str(len(cvs)) + '\n'

    #5
    otherline = ''
    for cv in cvs:
        cvPos = mc.xform(cv, q=True, ws=True, t=True)
        otherline += '        '+str(cvPos[0]) + ' ' + str(cvPos[1]) + ' ' + str(cvPos[2]) + '\n'
    otherline += ';'

    filePath = mc.fileDialog(dm='*.cs', m=1)
    if filePath:
        if 'cs' != filePath.split('.')[-1]:
            filePath += '.cs'

        newFile = open(filePath, 'w')
        newFile.write(onelineData)
        newFile.write(twolineData)
        newFile.write(threeline)
        newFile.write(fourline)
        newFile.write(otherline)
        newFile.close()


def createCrvBetween2Pos(name, st, ed, mpNode=None):
    """
    #--------------------------------------------------------------------------------
    #This Function can connect a curve line between two point or two object
    #Note: none
    #FN: crv_connect(a , b)
    #Date: 2013/01/04_v1.0
    #Date: 2014/06/18_v1.1
    #--------------------------------------------------------------------------------
    """

    stPoint = mc.xform(st, q=1, t=1, ws=1)
    edPoint = mc.xform(ed, q=1, t=1, ws=1)
    crv = mc.curve( p=((stPoint[0], stPoint[1], stPoint[2]),(edPoint[0], edPoint[1], edPoint[2])), d=1, n=name )

    #st cluster
    mc.select(crv+'.cv[0]')
    stCluSys = mc.cluster()
    stCluster = mc.rename(stCluSys[0], '%s_st_cluster' % crv)
    stHandle = mc.rename(stCluSys[1], '%s_st_clusterHandle' % crv)
    mc.parentConstraint(st, stHandle)
    mc.setAttr(stHandle+'.visibility', 0)

    #ed cluster
    mc.select(crv+'.cv[1]')
    edCluSys = mc.cluster()
    mc.rename(edCluSys[0], '%s_ed_cluster' % name)
    edHandle = mc.rename(edCluSys[1], '%s_ed_clusterHandle' % name)
    mc.parentConstraint(ed, edHandle)
    mc.setAttr(edHandle+'.visibility', 0)

    mc.select(cl=True)
    mc.setAttr(crv+'.overrideEnabled', 1)
    mc.setAttr(crv+'.overrideDisplayType', 2)

    # clean
    if not mpNode:
        mpNode=mc.createNode('transform', n=name+'_grp')

    mc.parent(crv, mpNode)
    mc.parent(stHandle, mpNode)
    mc.parent(edHandle, mpNode)

    return mpNode


def numCVs(curve):
    """
    Get the number of CVs of a curve.

    :param curve:
    :return: number of cvs
    :rtype: int
    """
    return mc.getAttr("{0}.cp".format(curve), s=1)


def convertToBezierCurve(curve):
    """
    Check if the parsed curve is a bezier curve, if this is not the case
    convert the curve to a bezier curve.
    
    :param str curve: Name of curve
    """
    # get shape
    curveShape = mc.listRelatives(curve, s=True)[0]

    # convert to bezier curve
    if mc.nodeType(curveShape) == "bezierCurve":
        return
        
    mc.select(curve)
    mc.nurbsCurveToBezier()


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

    return pUtil.getDouble(pPtr), point


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
    parameters = [p/factor for p in parameters]

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
    parameters = [p/factor for p in parameters]

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
    num = numCVs(curve)

    # create clusters
    for i in range(num):
        # create cluster
        clusterShape, clusterTransform = mc.cluster("{0}.cv[{1}]".format(curve, i))

        # rename shape and transform
        mc.rename(clusterShape, "{0}_clusterShape_{1:03d}".format(prefix, i+1))
        clusterTransform = mc.rename(clusterTransform, "{0}_cluster_{1:03d}".format(prefix, i+1))
        
        # set and lock visibility
        mc.setAttr("{0}.visibility".format(clusterTransform), 0)
        mc.setAttr("{0}.visibility".format(clusterTransform), lock=True)

        # store transform
        clusters.append(clusterTransform)

    return clusters


def setShapeWidth(curve, width=-1):
    shapes = mc.listRelatives(curve, s=True)
    for shape in shapes:
        mc.setAttr('%s.lineWidth'%shape, width)

def setShapeName(curve):
    shapes = mc.listRelatives(curve, s=True)
    for shape in shapes:
        mc.rename(shape,'{0}Shape'.format(curve))

def setShapeColor(curve, colorID):
    shapes = mc.listRelatives(curve, s=True)
    for shape in shapes:
        mc.setAttr(shape + ".ove", 1)
        mc.setAttr(shape + ".ovc", colorID)