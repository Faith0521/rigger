# coding:utf-8
"""Methods that use Maya Api"""

from maya.api import OpenMaya


def asMObject(node):
    """
    #brief Convert a node to an MObject.
    #return : MObject

    ARGS :
            #param node - String - Name of the node to convert.
    """
    sel = OpenMaya.MSelectionList()
    nodeMObj = OpenMaya.MObject()
    sel.add(node)
    sel.getDependNode(0, nodeMObj)
    return nodeMObj


def get_mdag_path(node):
    """Return the API 2.0 dagPath of given node."""
    sel_list = OpenMaya.MSelectionList()
    sel_list.add(node)
    return sel_list.getDagPath(0)


def get_world_translation(node):
    """Return given nodes world translation of rotate pivot."""
    target_m_transform = OpenMaya.MFnTransform(get_mdag_path(node))
    target_rotate_pivot = OpenMaya.MVector(
        target_m_transform.rotatePivot(OpenMaya.MSpace.kWorld))
    return target_rotate_pivot


def walkDag(node):
    """
    #brief Walk through a hierarchy and return the full path name of every node under the given root node.
    #return : List

    ARGS :
                    #param node - String - Root node to get the hierarchy of.
    """
    result = []
    nodeMObj = asMObject(node)
    iter = OpenMaya.MItDag()
    iter.reset(nodeMObj)
    while not iter.isDone():
        dagPath = OpenMaya.MDagPath()
        iter.getPath(dagPath)
        result.append(dagPath.fullPathName())
        iter.next()

    return result


# todo:get all vertices of given mesh
def get_all_vertices(mesh_transform):
    """Return all vertices of given mesh"""

    selection_ls = OpenMaya.MSelectionList()
    selection_ls.add(mesh_transform)
    sel_obj = selection_ls.getDagPath(0)

    mfn_object = OpenMaya.MFnMesh(sel_obj)
    return mfn_object.getPoints(OpenMaya.MSpace.kWorld)


def get_all_objects_by_type(type=OpenMaya.MFn.kJoint):
    """
    使用Maya API 2.0获取场景中所有骨骼（关节）的完整路径
    :type: 类型
    :return: 骨骼完整路径的列表，如['|root_jnt', '|root_jnt|arm_jnt']
    """
    joint_list = []

    # 创建骨骼类型的迭代器（MFn.kJoint指定只遍历骨骼节点）
    joint_iterator = OpenMaya.MItDependencyNodes(type)

    # 遍历所有骨骼
    while not joint_iterator.isDone():
        # 获取当前骨骼的MObject
        joint_mobject = joint_iterator.thisNode()

        # 创建DAG路径函数集，用于获取完整层级路径
        dag_path = OpenMaya.MDagPath.getAPathTo(joint_mobject)

        # 获取骨骼的完整路径名称（包含所有父级节点）
        full_joint_path = dag_path.fullPathName()

        joint_list.append(full_joint_path)

        # 移动到下一个骨骼
        joint_iterator.next()

    return joint_list


# todo:解锁法线
def unlock_normals(transform, soften=False):
    """Unlock the normals of the specified geometry.

    Args:
        transform (str or list): string or list of strings for the geometries
            to unlock.
        soften (bool, optional): If true, softens the edges with given
            softedge_angle value. Defaults to True.
    """

    # Retrieve the MFnMesh api object.
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(transform)
    mfn_mesh = OpenMaya.MFnMesh(selection_list.getDagPath(0))
    # if it's already unlocked, do not process again.
    lock_state = any(
        mfn_mesh.isNormalLocked(normal_index)
        for normal_index in range(mfn_mesh.numNormals)
    )
    if lock_state:
        mfn_mesh.unlockVertexNormals(OpenMaya.MIntArray(range(mfn_mesh.numVertices)))
    if soften:
        edge_ids = OpenMaya.MIntArray(range(mfn_mesh.numEdges))
        smooths = OpenMaya.MIntArray([True] * mfn_mesh.numEdges)
        mfn_mesh.setEdgeSmoothings(edge_ids, smooths)
        mfn_mesh.cleanupEdgeSmoothing()
        mfn_mesh.updateSurface()






























