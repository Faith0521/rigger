# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma
from cgrig.libs.maya.api import generic
from cgrig.libs.naming import naming
from cgrig.libs.maya.cmds.rig import curve
from cgrig.libs.maya.cmds.mesh import shape, mesh
from cgrig.libs.maya.cmds.objutils import namehandling, shapenodes
try:
    import numpy as np
except:
    pass


class DeformOrder:
    after = "after"
    before = "before"
    parallel = "parallel"
    split = "split"
    foc = "foc"


def createClustersOnCurve(partPrefixName, splineCurve, relative=False, showHandles=False, padding=2):
    """Creates clusters on a curve automatically adding the clusters to each cv in order

    :param partPrefixName:  The prefix, name of the rig/part, optional, can be an empty string (auto), is a shortname
    :type partPrefixName: str
    :param splineCurve: can be a nurbsCurve shape node or transform with nurbsCurve shape, longname preferred
    :type splineCurve: str
    :param relative:  If True only the transformations directly above the cluster are used by the cluster.
    :type relative: bool
    :param showHandles:  If True show the Maya handles display mode, little crosses on each handle
    :type showHandles: bool
    :param padding:  The numerical padding
    :type padding: bool
    :return clusterList: The created cluster names
    :rtype clusterList: list
    """
    rememberObjs = cmds.ls(selection=True, long=True)
    clusterList = list()
    numSpans = cmds.getAttr("{}.spans".format(splineCurve))
    degree = cmds.getAttr("{}.degree".format(splineCurve))
    form = cmds.getAttr("{}.form".format(splineCurve))
    numCVs = numSpans + degree
    if form == 2:
        numCVs -= degree
    nameSuffix = "cluster"
    if partPrefixName:  # then add it to the beginning of the name
        nameSuffix = "{}_cluster".format(partPrefixName)
    for i in range(numCVs):
        clusterName = "{}_{}_".format(nameSuffix, str(i).zfill(padding))
        clusterList.append(cmds.cluster("{}.cv[{}]".format(splineCurve, i), name=clusterName, relative=relative))
    cmds.select(rememberObjs, replace=True)  # as clusters are created they're selected, so return to orig
    if showHandles:
        for clusterPair in clusterList:  # cluster pair is a list, [clusterNode, transformNode]
            cmds.setAttr("{}.displayHandle".format(clusterPair[1]), True)
    return clusterList


def createClustersOnCurveSelection(partPrefixName="", relative=False, showHandles=False):
    """Creates a cluster on each CV of a nurbsCurve of the first selected object.

    If a transform selection will check shapes for the first nurbsCurve shape node

    :param showHandles:  if not an empty string overrides the default cluster name which uses the spline name as prefix
    :type showHandles: bool
    :param showHandles:  If True show the Maya handles display mode, little crosses on each handle
    :type showHandles: bool
    :param padding:  The numerical padding
    :type padding: bool
    :return clusterList: The created cluster names,
    :rtype clusterList: list(list(str))
    """
    # TODO support lists not only first selected obj
    selObjs = cmds.ls(selection=True, long=True)
    if not selObjs:
        om2.MGlobal.displayWarning("Nothing selected. Please select a curve")
        return list()
    splineShape = shapenodes.transformHasShapeOfType(selObjs[0], "nurbsCurve")
    if not splineShape:
        om2.MGlobal.displayWarning("Please select a curve.")
        return list()
    # Curve found so build
    if partPrefixName:  # use the partPrefixName as the prefix for each cluster
        return createClustersOnCurve(partPrefixName, splineShape, relative=relative, showHandles=showHandles)
    firstObjShortName = namehandling.mayaNamePartTypes(selObjs[0])[2]  # short name and no namespace
    # firstObj as prefix for each cluster
    return createClustersOnCurve(firstObjShortName, splineShape, relative=relative, showHandles=showHandles)


def get_polygon_points(mesh):
    selection_list = om2.MSelectionList()
    selection_list.add(mesh)

    dag_path = selection_list.getDagPath(0)

    mesh_fn = om2.MFnMesh(dag_path)

    points = mesh_fn.getPoints(om2.MSpace.kWorld)

    return points


def py_to_mArray(cls, _list):
    result = cls()
    for elem in _list:
        result.append(elem)
    return result

def get_weights(mesh_name, skin_name, indices):
    selection = om2.MSelectionList()
    selection.add(skin_name)
    selection.add(mesh_name + ".vtx[*]")

    skin_obj = selection.getDependNode(0)
    # mesh_dag = selection.getDagPath(1)
    mesh_dag, mesh_comp = selection.getComponent(1)
    fn_skin = oma.MFnSkinCluster(skin_obj)
    weights = fn_skin.getWeights(mesh_dag, mesh_comp, indices)

    return weights


def get_py_weights(mesh_name):
    skin_cluster_name = cmds.ls(cmds.listHistory(mesh_name), type="skinCluster")[0]
    jointLength = len(cmds.skinCluster(skin_cluster_name, q=1, inf=1))
    indices = py_to_mArray(om2.MIntArray, range(jointLength))
    weights = get_weights(mesh_name, skin_cluster_name, indices)
    vtx_length = int(len(weights) / jointLength)
    weights = [weights[i] for i in range(len(weights))]
    weights = [weights[jointLength * vtx_id:jointLength * (vtx_id + 1)] for vtx_id in range(vtx_length)]
    return jointLength, weights


def split_target_by_weights(org_points, target_points, weights):
    vectors = target_points - org_points
    weights = weights.transpose(1, 0)
    split_vec = weights[:, :, None] * vectors[None]
    split_points = org_points + split_vec
    return split_points


def set_mesh_points(mesh_name, points):
    selection_list = om2.MSelectionList()
    selection_list.add(mesh_name)

    dag_path = selection_list.getDagPath(0)

    mesh_fn = om2.MFnMesh(dag_path)

    mesh_fn.setPoints(om2.MPointArray(points), om2.MSpace.kWorld)

    mesh_fn.updateSurface()


def splitBlendshape(inputBSMesh, orgMesh, skinMesh, jointInputs):
    org_points = np.array(get_polygon_points(orgMesh))
    target_points = np.array(get_polygon_points(inputBSMesh))

    jointLength, weights = get_py_weights(skinMesh)
    weights = np.array(weights)
    split_meshes = []
    for num in range(len(jointInputs)):
        m = cmds.duplicate(skinMesh)[0]
        split_meshes.append(m)
    result = split_target_by_weights(org_points, target_points, weights)
    for split_mesh, split_points in zip(split_meshes, result):
        set_mesh_points(split_mesh, split_points.tolist())


def getDeformersForShape(geo, ignoreTypes=None, ignoreTweaks=True):
    """
    Return the whole deformer stack as a list

    :param str geo: geometry object
    :param list ignoreTypes: types of deformers to exclude from the list
    :param bool ignoreTweaks: Ignore tweak nodes from the deformer list
    :return: list of deformers affecting the specified geo
    :rtype: list
    """
    ignoreTypes = ignoreTypes or list()

    geo = naming.getFirst(geo)
    result = []
    if ignoreTweaks:
        ignoreTypes += ["tweak"]

    geometryFilters = cmds.ls(cmds.listHistory(geo), type="geometryFilter")
    shape = getDeformShape(geo)

    if shape is not None:
        shapeSets = cmds.ls(cmds.listConnections(shape), type="objectSet")

    for deformer in geometryFilters:
        # first lets try to use this using the old version from Maya2020.
        # if that fails we can ty another method.
        deformerSet = cmds.ls(cmds.listConnections(deformer), type="objectSet") or list()
        if deformerSet:
            if deformerSet[0] in shapeSets:
                # in almost every case we
                if not cmds.nodeType(deformer) in ignoreTypes:
                    result.append(deformer)

        else:
            result = cmds.deformableShape(shape, chain=True)

    return result


def getOrigShape(node):
    """
    Get an orig shape from the given geometry node

    :param node:  geometry or deformer name to get the orig shape for
    :return: orig shape or orig shape output plug
    """
    deformShape = getDeformShape(node)
    origShape = naming.getFirst(cmds.deformableShape(deformShape, originalGeometry=True))

    origShape = origShape.split(".")[0]
    return origShape


def createCleanGeo(geo, name=None):
    """
    create a completely clean version of the given geo. To do this we will revert the mesh to the shape of the orig shape

    :param geo: name of the geometry to create a clean shape for
    :param name: name for the newly created clean geometery
    :return:
    """
    dupGeo = cmds.duplicate(geo)[0]
    if not name:
        name = "{}_clean".format(geo)

    dupGeo = cmds.rename(dupGeo, name)
    origShape = getOrigShape(geo)

    if shape.getType(dupGeo) == shape.MESH:
        return createCleanMesh(dupGeo, origShape)
    elif shape.getType(dupGeo) == shape.CURVE:
        return createCleanCurve(dupGeo, origShape)
    else:
        raise NotImplementedError(f"Shape types other than {[shape.MESH, shape.CURVE]} are not currently supported")


def createCleanMesh(dupGeo, origShape) -> str:
    """Create a clean version of geo for a mesh"""
    shapes = cmds.listRelatives(dupGeo, s=True)

    # get the point positions of the orig shape
    origPoints = mesh.getVertPositions(origShape, world=False)

    # delete all intermediate shapes
    for eachShape in shapes:
        if cmds.getAttr("{}.intermediateObject".format(eachShape)):
            cmds.delete(eachShape)

    # set the point positions the ones from the orig shape
    mesh.setVertPositions(dupGeo, vertList=origPoints, world=False)

    return dupGeo


def createCleanCurve(dupGeo, origShape) -> str:
    """Create a clean version of geo for a nurbs curve"""
    shapes = cmds.listRelatives(dupGeo, s=True)

    # get the point positions of the orig shape
    origPoints = curve.getCvPositions(origShape, world=False)

    # delete all intermediate shapes
    for eachShape in shapes:
        if cmds.getAttr("{}.intermediateObject".format(eachShape)):
            cmds.delete(eachShape)

    # set the point positions the ones from the orig shape
    curve.setCvPositions(dupGeo, cvList=origPoints, world=False)

    return dupGeo


def getDeformShape(node):
    """
    Get the visible geo regardless of deformations applied

    :param str node: Name of the node to retreive shape node from
    """

    if cmds.nodeType(node) in ["nurbsSurface", "mesh", "nurbsCurve"]:
        node = cmds.listRelatives(node, p=True)
    shapes = cmds.listRelatives(node, s=True, ni=False) or []

    if len(shapes) == 1:
        return shapes[0]
    else:
        realShapes = [x for x in shapes if not cmds.getAttr("{}.intermediateObject".format(x))]
        return realShapes[0] if len(realShapes) else None


def getDeformerStack(geo, ignoreTypes=None):
    """
    Return the whole deformer stack as a list

    :param str geo: geometry object
    :param list ignoreTypes: types of deformers to exclude from the list
    :return: list of deformers affecting the specified geo
    :rtype: list
    """

    ignoreTypes = ignoreTypes or ["tweak"]
    geo = naming.getFirst(geo)

    inputs = cmds.ls(
        cmds.listHistory(geo, pruneDagObjects=True, interestLevel=1),
        type="geometryFilter",
    )

    # sometimes deformers can be connected to inputs that dont affect the deformation of the given geo.
    # This happens alot in blendshapes where one blendshape drives a bunch of others for small details.
    # we need to filter out any deformers from this list that dont affect the given geo.
    deformShape = getDeformShape(geo)
    for i in inputs:
        tgtDeformShape = naming.getFirst(cmds.deformer(i, q=1, g=1, gi=1))
        if tgtDeformShape != deformShape:
            inputs.remove(i)

    return [i for i in inputs if not cmds.nodeType(i) in ignoreTypes]


def getGeoIndex(deformer, geo):
    """
    Get the index of specifed geo in the deformer

    :param deformer: name of the deformer to
    :param geo:
    :return:
    """
    geo = shape.getShapes(geo)
    if not geo:
        return
    deformedGeometry = cmds.deformer(deformer, q=1, g=1, gi=1)
    if not deformedGeometry:
        return

    # Get full path names in case a full path name was passed
    deformedGeometry = cmds.ls(deformedGeometry, l=1)
    geo = cmds.ls(geo, l=1)[0]

    # Get all used indexes
    deformedIndecies = cmds.deformer(deformer, q=1, gi=1)

    for n in range(len(deformedGeometry)):
        if deformedGeometry[n] == geo:
            return int(deformedIndecies[n])

















