import maya.cmds as mc
import maya.OpenMaya as om
import maya.api.OpenMaya as om2


def toMObject(node):
    """
    Convert a node into a om.MObject.

    :param str node:
    :return: MObject of parsed node
    :rtype: om.MObject
    """
    selectionList = om.MSelectionList()
    selectionList.add(node)
    obj = om.MObject()
    selectionList.getDependNode(0, obj)
    
    return obj


def toMObject2(node):
    """
    Convert a node into a om.MObject.

    :param str node:
    :return: MObject of parsed node
    :rtype: om.MObject
    """
    selectionList = om2.MSelectionList()
    selectionList.add(node)
    obj = selectionList.getDependNode(0)

    return obj


def toMDagPath(node):
    """
    Convert a node into a om.MDagPath.

    :param str node:
    :return: MDagPath of parsed node
    :rtype: om.MDagPath
    """
    obj = toMObject2(node)
    if obj.hasFn(om2.MFn.kDagNode):
        dag = om2.MDagPath.getAPathTo(obj)
        return dag


def toMPoint(node):
    """
    Convert a node pos into a om.MPoint.

    :param str node:
    :return: MFnNurbsCurve of parsed curve
    :rtype: om.MFnNurbsCurve
    """    
    point = mc.xform(node, q=1, t=1, ws=1)
    mp = om.MPoint(*point)
    
    return mp


def asMFnNurbsCurve(curve):
    """
    Convert a node into a om.MFnNurbsCurve.

    :param str curve:
    :return: MFnNurbsCurve of parsed curve
    :rtype: om.MFnNurbsCurve
    """
    dag = toMDagPath(curve)
    nurbsCurveFn = om2.MFnNurbsCurve(dag)

    return nurbsCurveFn

