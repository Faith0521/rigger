from functools import partial
import maya.cmds as mc
import maya.mel as mel
from ...maya_utils import aboutName
from pymel.core import *
from . import rigChecks
from maya import OpenMaya as om
from maya.api import OpenMaya as om2


# Rig Checks and Fixes
def deleteCh():
    mc.delete(ch=1, all=1)
    return True


def assignLambert():
    nodes = mc.ls(type=('mesh', 'nurbsSurface'))
    mc.sets(nodes, e=1, fe='initialShadingGroup')

    mel.eval('source "hyperShadePanel.mel"')
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    return True


def layers():
    rlayers = mc.ls(type=('renderLayer', 'displayLayer'))
    if 'defaultRenderLayer' in rlayers:
        rlayers.remove('defaultRenderLayer')
    if 'defaultLayer' in rlayers:
        rlayers.remove('defaultLayer')

    if rlayers:
        mc.delete(rlayers)
    return True


def refNodes():
    if mc.ls(type='reference'):
        return 'You cannot have live references in your sence!\nMake sure you import any references and remove their namespaces.'
    return True


def namespaces():
    nss = namespaceInfo(lon=1, r=1)
    if 'UI' in nss:
        nss.remove('UI')
    if 'shared' in nss:
        nss.remove('shared')
    if nss:
        print('Namespaces found!\nPlease remove all namespaces from your scene.')
        return False
    return True


def deleteNameSpaces():
    namespaces = mc.namespaceInfo(listOnlyNamespaces=True, recurse=True)

    # 过滤掉默认的命名空间（如 "UI" 和 "shared"）
    namespaces = [ns for ns in namespaces if ns not in ["UI", "shared"]]

    # 按命名空间深度排序（从最深到最浅）
    namespaces.sort(key=lambda x: x.count(":"), reverse=True)

    # 删除命名空间
    for ns in namespaces:
        try:
            mc.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
            print(f"已删除命名空间: {ns}")
        except Exception as e:
            print(f"删除命名空间 {ns} 时出错: {e}")



def camsLightsImgPlanes():
    nodes = mc.ls(type='imagePlane') + mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
           'topShape',
           'frontShape',
           'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)
    if nodes:
        return
    return True


def camsLightsImgPlanesfix():
    nodes = mc.ls(type='imagePlane')
    if nodes:
        mc.delete(nodes)
    nodes = mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
           'topShape',
           'frontShape',
           'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)

    for n in nodes:
        xf = mc.listRelatives(n, p=1)
        mc.delete(xf)


def sameNames():
    sames = getSames()

    if sames:
        msg = 'Same names found! See script editor for details.\n\nSame Names:\n'
        mc.select(sames)
        i = 1
        for s in sames:
            print(s)
            if i < 50:
                msg += '   {0}\n'.format(s)
            i += 1
        if i > 49:
            msg += '\n   Plus {0} more ...'.format(i - 49)

        if mc.window('mcheckUI', q=1, ex=1):
            return
        else:
            print(msg)
            return False
    return True


def getSames():
    nodes = mc.ls(sn=1)
    sames = []
    for n in nodes:
        if '|' in n:
            sames.append(n)
    return sames


def sameNamesFixUI():
    if mc.window('mcheckUI', q=1, ex=1):
        mc.deleteUI('mcheckUI')
    win = mc.window('mcheckUI', t='Fix Same Names', s=1)
    mc.columnLayout(adj=True, rs=5, co=['both', 10])
    mc.separator(st='none')

    msg = '''\tFix duplicate node names?.

    NOTE: This will rename all duplicate nodes in your scene. Are you sure?\nAlternatively you can resolve this yourself.'''

    mc.text(msg)
    mc.button(label='Fix', c=fixSameNames)
    mc.showWindow(win)
    mc.window(win, e=1, wh=[500, 105], s=0)
    return 'PENDING'


def fixSameNames():
    if mc.window('mcheckUI', q=1, ex=1):
        mc.deleteUI('mcheckUI')

    i = 0
    while getSames() and i < 20:
        for s in getSames():
            if mc.objExists(s):
                newn = aboutName.unique(s.split('|')[-1])
                mc.rename(s, newn)
        i += 1


def singleHi():
    nodes = mc.ls('|*')
    for n in ['front', 'persp', 'side', 'top']:
        nodes.remove(n)

    if len(nodes) == 1:
        return True

    return 'Must have one single hierarchy in your rig scene.\nPlease clean this up!'


def find_objects_with_attribute(attribute_name):
    """
    查找场景中具有特定属性的物体
    :param attribute_name: 属性名称（字符串）
    :return: 具有该属性的物体名称列表
    """
    # 初始化结果列表
    result = []

    # 创建节点迭代器
    iter_nodes = om.MItDependencyNodes()

    # 遍历场景中的所有节点
    while not iter_nodes.isDone():
        # 获取当前节点的 MObject
        mobject = iter_nodes.thisNode()

        # 创建 MFnDependencyNode
        dep_node = om.MFnDependencyNode(mobject)

        # 检查节点是否具有指定属性
        if dep_node.hasAttribute(attribute_name):
            # 获取节点名称并添加到结果列表
            node_name = dep_node.name()
            result.append(node_name)

        # 继续下一个节点
        iter_nodes.next()

    return result



def checkBadShapes(fix=False):
    badones = []
    nodes = [mc.listRelatives(n, p=1, f=1)[0] for n in mc.ls(type=('mesh', 'nurbsCurve'))]

    if not nodes:
        nodes = []

    for node in nodes:
        shapes = mc.listRelatives(node, s=1, ni=1)
        if shapes:
            i = 1
            if len(shapes) > 1:
                if i < 50:
                    badones.append(node)
                i += 1

                badones.append(node)

            for shape in shapes:
                if not shape == node.split('|')[-1] + 'Shape':
                    badones.append(shape)

    if badones:
        if fix:
            for node in badones:
                node = mc.listRelatives(node, p=1)[0]
                shape = mc.listRelatives(node, s=1, ni=1)
                shapes = mc.listRelatives(node, s=1)

                for sh in shape:
                    if sh in shapes:
                        shapes.remove(sh)

                for sh in shapes:
                    if sh == node + 'Shape':
                        mc.rename(sh, node + 'ShapeOrig')

                for sh in shape:
                    if not sh == node + 'Shape':
                        mc.rename(sh, node + 'Shape')
            return

        else:
            mc.select(badones)
            msg = 'Bad shape nodes found:\n'
            msg += '\n'.join(badones)
            return str(msg)
    return True


def fixBadShapes():
    checkBadShapes(fix=True)


def fixSets():
    nodes = mc.ls('|*')
    for n in ['front', 'persp', 'side', 'top']:
        nodes.remove(n)
    if nodes:
        mc.select(nodes)

    try:
        mel.eval(
            'python ("from mpc.tvcRiggingSandbox.ftrackSetCreator import FtrackSetCreator; f = FtrackSetCreator(); f.cb_type.setCurrentIndex(1); f.show()");')
    except:
        mc.warning('Cannot load Ftrack set creator!')


def getLockedNormals(asset):
    lockNormalObjs = []
    object_list = mc.listRelatives(asset, c=1, ad=1, noIntermediate=True)
    for obj in object_list:
        isLockedNormals = []
        selection_list = om2.MSelectionList()
        selection_list.add(obj)
        dag_mobj = selection_list.getDependNode(0)
        if dag_mobj.hasFn(om2.MFn.kMesh):
            dag_path = selection_list.getDagPath(0)
            mesh_fn = om2.MFnMesh(dag_path)
            normalCounts, normals = mesh_fn.getNormalIds()
            for index in normals:
                isNormalLocked = mesh_fn.isNormalLocked(index)
                if isNormalLocked:
                    isLockedNormals.append(index)
        if isLockedNormals:
            lockNormalObjs.append(obj)

    if not lockNormalObjs:
        return rigChecks.checkResult(allowPublish=True)
    else:
        return rigChecks.checkResult(allowPublish=False,
                                     msg=u'# 以下Mesh节点法线被锁定---\n' + str(lockNormalObjs),
                                     nodes=lockNormalObjs)


def checkModelLockedNormals():
    asset_chars = "geometry"
    if not asset_chars:
        return

    result = getLockedNormals(asset_chars)
    if not result["nodes"]:
        return True
    else:
        om.MGlobal.displayInfo(result['msg'])
        return False


def fixModelLockedNormals():
    asset_chars = "geometry"
    if not asset_chars:
        return

    result = getLockedNormals(asset_chars)
    if result['nodes']:
        rigChecks.createSelectUI("FixModelLockedNormals", result['msg'], result['nodes'], fix=False)


def UnlockVertNormals(shapeList):
    for shape in shapeList:
        selection_list = om2.MSelectionList()
        selection_list.add(shape)
        dag_path = selection_list.getDagPath(0)
        mesh_fn = om2.MFnMesh(dag_path)
        vertexCount, vertexList = mesh_fn.getVertices()
        mesh_fn.unlockVertexNormals(vertexList)
        om2.MGlobal.displayInfo("Done-----------")


def getModelSmoothLevel(asset):
    error_level_models = []
    object_list = mc.listRelatives(asset, c=1, ad=1, noIntermediate=True)
    for obj in object_list:
        selection_list = om2.MSelectionList()
        selection_list.add(obj)
        dag_mobj = selection_list.getDependNode(0)
        if dag_mobj.hasFn(om2.MFn.kMesh):
            smooth_level = mc.displaySmoothness(obj, query=True, polygonObject=True)
            if smooth_level:
                if smooth_level[0] != 1:
                    error_level_models.append(obj)
    if not error_level_models:
        return rigChecks.checkResult(allowPublish=True)
    else:
        return rigChecks.checkResult(allowPublish=False,
                                     msg=u'# 平滑预览不为1的模型---\n' + str(error_level_models),
                                     nodes=error_level_models)


def checkModelSmoothLevel():
    asset_chars = "geometry"
    if not asset_chars:
        return

    result = getModelSmoothLevel(asset_chars)
    if not result["nodes"]:
        return True
    else:
        om.MGlobal.displayInfo(result['msg'])
        return False


def fixModelSmoothLevel():
    asset_chars = "geometry"
    if not asset_chars:
        return

    result = getModelSmoothLevel(asset_chars)
    if result['nodes']:
        rigChecks.createSelectUI("FixModelLockedNormals", result['msg'], result['nodes'])




















