#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/11/13 15:49
# @Author : yinyufei
# @File : mesh.py
# @Project : TeamCode

"""
Geometry utilities
"""
import maya.api.OpenMaya as om2
import maya.cmds as cmds

from cgrig.libs.maya.cmds.mesh import shape
from cgrig.libs.naming import naming


def isMesh(node):
    """
    check if the node is a mesh.
    The function will return True for both transforms with a mesh Shape node or for a mesh Shapenode

    :param node: node to check
    :return: If the provided node is a mesh
    :rtype: bool
    """
    if not cmds.objExists(node):
        return False

    if "transform" in cmds.nodeType(node, i=True):
        shape = cmds.ls(
            cmds.listRelatives(node, s=True, ni=True, pa=True) or [], type="mesh"
        )
        if not shape:
            return False
        node = shape[0]
    if cmds.objExists(cmds.objExists(node) != "mesh"):
        return False

    return True


def getMeshFn(mesh):
    """
    Get the MFn mesh object for a given mesh

    :param mesh: mesh name
    :return: Open Maya API mesh function set object.
    :rtype: MFnMesh
    """
    selList = om2.MSelectionList()
    selList.add(mesh)
    dagPath = selList.getDagPath(0)
    meshFn = om2.MFnMesh(dagPath)

    return meshFn


def getVertPositions(mesh, world=True):
    """
    Get a list of vertex positions for a single mesh.

    :param str mesh: mesh to get positions of
    :param bool world: Get the vertex position in world space. False is local position
    :return: List of vertex positions
    :rtype: list
    """
    if isinstance(mesh, (list, tuple)):
        mesh = mesh[0]

    if shape.getType(mesh) != "mesh":
        cmds.error(
            "Node must be of type 'mesh'. {} is of type {}".format(
                mesh, shape.getType(mesh)
            )
        )

    sel = om2.MGlobal.getSelectionListByName(mesh)
    dagPath = sel.getDagPath(0)

    meshFn = om2.MFnMesh(dagPath)

    if world:
        points = meshFn.getPoints(space=om2.MSpace.kWorld)
    else:
        points = meshFn.getPoints(space=om2.MSpace.kObject)

    vertPos = list()
    for i in range((len(points))):
        vertPos.append(
            [round(points[i].x, 5), round(points[i].y, 5), round(points[i].z, 5)]
        )

    return vertPos


def setVertPositions(mesh, vertList, world=False):
    """
    Using a list of vertex positions set the vertex positions of the provided mesh.
    This function uses the maya commands. it is slower than the API version but undoable if run from the script editor.

    :param str mesh: mesh to set the vertices of
    :param list vertList: list of vertex positions:
    :param bool world: Space to set the vertex positions
    """
    for i, vtx in enumerate(getVerts(mesh)):
        if world:
            cmds.xform(vtx, worldSpace=True, translation=vertList[i])
        else:
            cmds.xform(vtx, worldSpace=False, translation=vertList[i])


def getVerts(mesh):
    """
    get a list of all verticies in a mesh

    :param str mesh: mesh to get verticies of
    :return: list of verticies. ie ('pCube1.vtx[0]', 'pCube1.vtx[1]'...)
    :rtype: list

    """
    if isinstance(mesh, (list, tuple)):
        mesh = mesh[0]

    verts = cmds.ls("{}.vtx[*]".format(mesh))
    return naming.flattenList(verts)


def getVertexNormal(mesh, vertex, world=True):
    """
    Get the vertex normal of a vertex

    :param str mesh: mesh to get the vertex normal of
    :param int vertex: vertex ID to get the normal of
    :param bool world: Space to get the vertex normal in
    :return:
    """

    if isinstance(mesh, (list, tuple)):
        mesh = mesh[0]

    if shape.getType(mesh) != "mesh":
        cmds.error(
            "Node must be of type 'mesh'. {} is of type {}".format(
                mesh, shape.getType(mesh)
            )
        )

    mfnMesh = getMeshFn(mesh)

    # fn_mesh.getVertexNormal(vertex, False, om.MSpace.kWorld)
    space = om2.MSpace.kWorld if world else om2.MSpace.kObject

    vertexNormal = mfnMesh.getVertexNormal(vertex, False, space)

    return vertexNormal


def get_mesh_topology(mesh):
    """
    生成网格拓扑特征标识字符串，用于快速对比网格拓扑是否一致
    核心逻辑：提取顶点数、面数 + 关键面的顶点索引，生成唯一特征串

    :param mesh: 网格节点名称(str) / MDagPath / MObject
    :return: str 拓扑特征标识（空网格返回"0"）
    :raise RuntimeError: 网格无效/获取拓扑失败时抛出异常
    """
    # 1. 获取网格函数集（确保网格有效）
    try:
        fn_mesh = getMeshFn(mesh)
    except Exception as e:
        raise RuntimeError(u"获取网格函数集失败: {mesh}, 错误: {e}".format(mesh=mesh, e=e))

    # 2. 提取基础拓扑信息（顶点数、面数）
    vtx_count = fn_mesh.numVertices  # 顶点总数
    face_count = fn_mesh.numPolygons  # 面总数

    # 空网格直接返回标识"0"
    if face_count == 0:
        return "0"

    # 3. 初始化特征列表（基础拓扑 + 关键面顶点信息）
    topology_elements = [vtx_count, face_count]

    # 4. 选取4个关键面（均匀分布在面索引范围内），提取其顶点索引
    # 目的：通过关键面的顶点连接关系增强拓扑唯一性，避免仅顶点/面数相同但拓扑不同的误判
    face_ids = [
        int((face_count - 1) * x / 3.0)  # 生成0、1/3、2/3、1倍面数的索引，覆盖网格不同区域
        for x in range(4)
    ]

    # 5. 遍历关键面，提取每个面的顶点索引并加入特征列表
    for face_id in face_ids:
        # 安全校验：避免面索引越界（极端情况下面数动态变化）
        if 0 <= face_id < face_count:
            # 获取面的顶点索引数组，转换为列表后合并到特征列表
            vtx_indices = fn_mesh.getPolygonVertices(face_id)
            topology_elements.extend(vtx_indices)

    # 6. 将所有特征元素拼接为字符串（用"-"分隔，保证唯一性）
    return "-".join(map(str, topology_elements))


def check_mesh_topology(src, dst):
    """
    对比两个网格的拓扑结构是否完全一致（快速校验）
    注：该方法为快速校验，若需100%精准对比需遍历所有面的顶点索引

    :param src: 源网格（名称/MDagPath/MObject）
    :param dst: 目标网格（名称/MDagPath/MObject）
    :return: bool - True=拓扑一致，False=拓扑不一致
    :raise RuntimeError: 网格无效/获取拓扑失败时抛出异常
    """
    # 生成两个网格的拓扑特征标识
    src_topology = get_mesh_topology(src)
    dst_topology = get_mesh_topology(dst)

    # 对比特征标识（完全相等则拓扑一致）
    is_same = (src_topology == dst_topology)

    return is_same

