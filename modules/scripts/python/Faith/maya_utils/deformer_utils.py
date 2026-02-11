
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from . import api_utils as api
# from . import naming_utils as name
from .decorator_utils import one_undo


# TODO: create ccs mesh
def invert(base=None, corrective=None, name=None):
    """Inverts a shape through the deformation chain.

    @param[in] base Deformed base mesh.
    @param[in] corrective Sculpted corrective mesh.
    @param[in] name Name of the generated inverted shape.
    @return The name of the inverted shape.
    """
    # cmds.loadPlugin('cvshapeinverter_plugin.py', qt=True)
    if not base or not corrective:
        sel = cmds.ls(sl=True)
        if not sel or len(sel) != 2:
            cmds.undoInfo(closeChunk=True)
            raise (RuntimeError, 'Select base then corrective')
        base, corrective = sel

    # Get points on base mesh
    base_points = get_points(base)
    point_count = base_points.length()

    # Get points on corrective mesh
    corrective_points = get_points(corrective)

    # Get the intermediate mesh
    orig_mesh = get_shape(base, intermediate=True)

    # Get the component offset axes
    orig_points = get_points(orig_mesh)
    x_points = OpenMaya.MPointArray(orig_points)
    y_points = OpenMaya.MPointArray(orig_points)
    z_points = OpenMaya.MPointArray(orig_points)

    cmds.undoInfo(openChunk=True)
    for i in range(point_count):
        x_points[i].x += 1.0
        y_points[i].y += 1.0
        z_points[i].z += 1.0
    set_points(orig_mesh, x_points)
    x_points = get_points(base)
    set_points(orig_mesh, y_points)
    y_points = get_points(base)
    set_points(orig_mesh, z_points)
    z_points = get_points(base)
    set_points(orig_mesh, orig_points)

    # Create the mesh to get the inversion deformer
    if not name:
        name = '%s_inverted' % corrective

    inverted_shapes = cmds.duplicate(base, name=name)[0]
    # Delete the unnessary shapes
    shapes = cmds.listRelatives(inverted_shapes, children=True, shapes=True, path=True)
    for s in shapes:
        if cmds.getAttr('%s.intermediateObject' % s):
            cmds.delete(s)
    set_points(inverted_shapes, orig_points)
    # Unlock the transformation attrs
    for attr in 'trs':
        for x in 'xyz':
            cmds.setAttr('%s.%s%s' % (inverted_shapes, attr, x), lock=False)
    cmds.setAttr('%s.visibility' % inverted_shapes, 1)
    deformer = cmds.deformer(inverted_shapes, type='CorrectShapes')[0]

    # Calculate the inversion matrices
    deformer_mobj = get_mobject(deformer)
    fn_deformer = OpenMaya.MFnDependencyNode(deformer_mobj)
    plug_matrix = fn_deformer.findPlug('inversionMatrix', False)
    fn_matrix_data = OpenMaya.MFnMatrixData()

    for i in range(point_count):
        matrix = OpenMaya.MMatrix()
        set_matrix_row(matrix, x_points[i] - base_points[i], 0)
        set_matrix_row(matrix, y_points[i] - base_points[i], 1)
        set_matrix_row(matrix, z_points[i] - base_points[i], 2)
        set_matrix_row(matrix, corrective_points[i], 3)
        matrix = matrix.inverse()
        matrix_mobj = fn_matrix_data.create(matrix)

        plug_matrixElement = plug_matrix.elementByLogicalIndex(i)
        plug_matrixElement.setMObject(matrix_mobj)

    # Store the base points.
    fn_point_data = OpenMaya.MFnPointArrayData()
    point_data_mobj = fn_point_data.create(base_points)
    plug_deformed_points = fn_deformer.findPlug('deformedPoints', False)
    plug_deformed_points.setMObject(point_data_mobj)

    cmds.connectAttr('%s.outMesh' % get_shape(corrective), '%s.correctiveMesh' % deformer)

    cmds.undoInfo(closeChunk=True)
    return inverted_shapes


def get_shape(node, intermediate=False):
    """Returns a shape node from a given transform or shape.

    @param[in] node Name of the node.
    @param[in] intermediate True to get the intermediate mesh
    @return The associated shape node.
    """
    if cmds.nodeType(node) == 'transform':
        shapes = cmds.listRelatives(node, shapes=True, path=True)
        if not shapes:
            raise (RuntimeError, '%s has no shape' % node)
        for shape in shapes:
            is_intermediate = cmds.getAttr('%s.intermediateObject' % shape)
            if intermediate and is_intermediate:
                return shape
            elif not intermediate and not is_intermediate:
                return shape
        raise RuntimeError('Could not find shape on node {0}'.format(node))
    elif cmds.nodeType(node) in ['mesh', 'nurbsCurve', 'nurbsSurface']:
        return node


def get_mobject(node):
    """Gets the dag path of a node.

    @param[in] node Name of the node.
    @return The dag path of a node.
    """
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(node)
    node_mobj = OpenMaya.MObject()
    selection_list.getDependNode(0, node_mobj)
    return node_mobj


def get_dag_path(node):
    """Gets the dag path of a node.

    @param[in] node Name of the node.
    @return The dag path of a node.
    """
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(node)
    path_node = OpenMaya.MDagPath()
    selection_list.getDagPath(0, path_node)
    return path_node


def get_points(path, space=OpenMaya.MSpace.kObject):
    """Get the control point positions of a geometry node.

    @param[in] path Name or dag path of a node.
    @param[in] space Space to get the points.
    @return The MPointArray of points.
    """
    if isinstance(path, str):
        path = get_dag_path(get_shape(path))
    it_geo = OpenMaya.MItGeometry(path)
    points = OpenMaya.MPointArray()
    it_geo.allPositions(points, space)
    return points


def set_points(path, points, space=OpenMaya.MSpace.kObject):
    """Set the control points positions of a geometry node.

    @param[in] path Name or dag path of a node.
    @param[in] points MPointArray of points.
    @param[in] space Space to get the points.
    """
    if isinstance(path, str) or isinstance(path, str):
        path = get_dag_path(get_shape(path))
    it_geo = OpenMaya.MItGeometry(path)
    it_geo.setAllPositions(points, space)


def set_matrix_row(matrix, new_vector, row):
    """Sets a matrix row with an MVector or MPoint.

    @param[in/out] matrix Matrix to set.
    @param[in] new_vector Vector to use.
    @param[in] row Row number.
    """
    set_matrix_cell(matrix, new_vector.x, row, 0)
    set_matrix_cell(matrix, new_vector.y, row, 1)
    set_matrix_cell(matrix, new_vector.z, row, 2)


def set_matrix_cell(matrix, value, row, column):
    """Sets a matrix cell

    @param[in/out] matrix Matrix to set.
    @param[in] value Value to set cell.
    @param[in] row Row number.
    @param[in] column Column number.
    """
    OpenMaya.MScriptUtil.setDoubleArray(matrix[row], column, value)


def get_deformers(mesh=None, names_only=False):
    """
    Collects defomers in a dictionary by type
    :param mesh: Shape or transform node -> str
    :param names_only: If True, returns a flattened list with only deformer names
    :return: dictionary: {<type>: [list of deformers]}
    """
    valid_deformers = [
        "skinCluster",
        "blendShape",
        "nonLinear",
        "cluster",
        "jiggle",
        "deltaMush",
        "shrinkWrap",
        "tension",
        "ffd"
    ]
    # get deformer from mesh
    if not mesh:
        mesh = cmds.ls(sl=True)
    history = cmds.listHistory(mesh, pruneDagObjects=True)

    deformer_data = {
        deformer_type: cmds.ls(history, type=deformer_type, shapes=True)
        for deformer_type in valid_deformers
    }
    if names_only:
        name_list = name.flatten([value for key, value in deformer_data.items()])
        return name_list
    else:
        return deformer_data


def get_pre_blendshapes(mesh):  # noqa
    """Returns the blendshape node(s) before the skinCluster"""
    all_deformers = get_deformers(mesh)
    skin_clusters = all_deformers.get("skinCluster")
    if not skin_clusters:
        return []

    bs_deformers = all_deformers.get("blendShape")
    skin_cluster_history = cmds.listHistory(skin_clusters[0])
    pre_blendshapes = [node for node in bs_deformers if node in skin_cluster_history]

    return pre_blendshapes


# @one_undo
def connect_bs_targets(
        driver_attr,
        targets_dictionary,
        driver_range=None,
        force_new=False,
        front_of_chain=True,
        bs_node_name=None,
):
    """Creates or adds Blendshape target and connects them into the same controller attribute

    Args:
        driver_attr (String): driver attribute which controls. tooth_ctrl.gumRetract
        targets_dictionary (Dict): Dictionary for the targets.
                    Format: {<base>: <target_blendShape>}
                    Example: {
                        "face_mesh": "faceGumRetract",
                        "meniscus": "meniscusGumRetract",
                    }
        driver_range (List): If defined, remaps the driver attribute. Example: [0, 100]
        force_new (Bool): If True, a new blendshape will be created for each mesh even though there are existing ones.
        front_of_chain: Created blendshapes will be added front of the chain. Default True
        bs_node_name: If a new blendshape node will be created it will take this name. If a blendshape node with this
                        name exists, it will use that one.
    """
    if driver_range:
        custom_range = True
    else:
        custom_range = False
        driver_range = [0, 1]

    # check the driver, create a float attr if not present
    ch_node, ch_attr = driver_attr.split(".")
    assert cmds.objExists(ch_node), (
            "The Driver object (%s) does not exist in the scene" % ch_node
    )
    attr_state = cmds.attributeQuery(ch_attr, node=ch_node, exists=True)
    if not attr_state:
        cmds.addAttr(
            ch_node,
            ln=ch_attr,
            at="float",
            min=driver_range[0],
            max=driver_range[1],
            k=True,
        )
    else:
        user_attributes = cmds.listAttr(ch_node, ud=True) or []
        if ch_attr in user_attributes:
            # check if the given values are in range
            min_val = cmds.addAttr("%s.%s" % (ch_node, ch_attr), q=True, min=True)
            max_val = cmds.addAttr("%s.%s" % (ch_node, ch_attr), q=True, max=True)
            if min_val > driver_range[0]:
                cmds.addAttr("%s.%s" % (ch_node, ch_attr), e=True, min=driver_range[0])
            if max_val < driver_range[1]:
                cmds.addAttr("%s.%s" % (ch_node, ch_attr), e=True, max=driver_range[1])

    if custom_range:
        remap_node = cmds.createNode("remapValue")
        cmds.setAttr("{0}.inputMin".format(remap_node), driver_range[0])
        cmds.setAttr("{0}.inputMax".format(remap_node), driver_range[1])
        cmds.setAttr("{0}.outputMin".format(remap_node), 0)
        cmds.setAttr("{0}.outputMax".format(remap_node), 1)
        cmds.connectAttr(driver_attr, "{0}.inputValue".format(remap_node))
        driver_attr = "{0}.outValue".format(remap_node)

    bs_attrs = []
    for base, target_shape in targets_dictionary.items():
        # get the blendshape
        history = cmds.listHistory(base, pdo=True)
        bs_nodes = cmds.ls(history, type="blendShape")
        if force_new or not bs_nodes:
            bs_node = cmds.blendShape(
                target_shape,
                base,
                w=[0, 1],
                foc=front_of_chain,
                sd=True,
                name=bs_node_name,
            )[0]
        else:
            if bs_node_name in bs_nodes:
                bs_node = bs_node_name
            else:
                bs_node = bs_nodes[0]
            next_index = cmds.blendShape(bs_node, q=True, wc=True)
            cmds.blendShape(
                bs_node,
                edit=True,
                t=(base, next_index, target_shape, 1.0),
                w=[next_index, 1.0],
            )
        bs_attrs.append("{0}.{1}".format(bs_node, target_shape))

    for bs_attr in bs_attrs:
        cmds.connectAttr(driver_attr, bs_attr)
