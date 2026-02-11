# -*- coding: utf-8 -*-
"""

from cgrig.libs.maya.cmds.rig import follicles
follicles.connectFollicleToSelMesh()

"""

from maya import cmds, mel
from maya.api import OpenMaya as om2
from cgrig.libs.maya.api import mesh, plugs, curves
from cgrig.libs.utils import output
from cgrig.libs.maya.cmds.objutils import attributes, filtertypes, namehandling, matrix


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


def connectFollicleToShape(shape, follicleShape):
    """Connects a follicle to a new mesh shape node.

    :param shape: A mesh/nurbs shape node
    :type shape: str
    :param follicleShape: a maya hair follicle
    :type follicleShape: str
    """
    attributes.disconnectAttr(follicleShape, "inputMesh")  # will break the connection if connected.
    attributes.disconnectAttr(follicleShape, "inputWorldMatrix")
    cmds.connectAttr("{}.outMesh".format(shape), "{}.inputMesh".format(follicleShape))
    cmds.connectAttr("{}.worldMatrix[0]".format(shape), "{}.inputWorldMatrix".format(follicleShape))


def connectFollicleToSelMesh(message=True):
    """Transfers a follicle onto another mesh.

    Select one or multiple follicles and then the single mesh to transfer to and run.
    """
    selObjs = cmds.ls(selection=True)

    # Do error checks ---------------------------------------------
    if not selObjs:
        if message:
            output.displayWarning("No objects are selected.  Please select follicle/s and then a mesh.")
            return
    if len(selObjs) < 2:
        if message:
            output.displayWarning("Only one object is selected.  Please select follicle/s and then a mesh.")
        return

    # Check for correct node types --------------------------------
    mesh = selObjs[-1]
    meshObjs = filtertypes.filterGeoOnly([mesh])
    if not meshObjs:
        if message:
            output.displayWarning("The last selected object is not a mesh.")
        return
    meshShape = cmds.listRelatives(mesh, shapes=True)[0]
    follicleShapes = filtertypes.filterTypeReturnShapes(selObjs[:-1], children=False, shapeType="follicle")
    if not follicleShapes:
        if message:
            output.displayWarning("First selected objects should be follicles, none found.")
        return

    # Checks passed do the follicle transfer ----------------------
    for f in follicleShapes:
        connectFollicleToShape(meshShape, f)

    if message:
        fShapes = namehandling.getShortNameList(follicleShapes)
        meshShort = namehandling.getShortName(mesh)
        output.displayInfo("Success: Follicles transferred to mesh `{}`, {}.".format(meshShort, fShapes))


def uvPinConstraint(target, meshName, constraint="parent", st=[], sr=[], createMid=False):
    """
    为目标对象创建UV Pin约束，使目标对象基于网格/曲面的UV坐标吸附并跟随其变形运动

    参数:
        target (str): 待约束的目标对象（Maya中的transform节点，如控制器、关节等）
        meshName (str): 作为约束载体的网格或NURBS曲面名称（目标对象将吸附于该载体）
            若为True，约束后目标对象会保留当前位置/旋转与驱动源的相对偏移
        constraint (str, optional): 最终约束类型，默认为"parent"（父约束）
            可选值: "parent"（父约束，控制位置+旋转）、"point"（点约束，仅控制位置）、"orient"（方向约束，仅控制旋转）
        createMid (bool, optional): 是否创建中间过渡节点，默认为False
            若为True，会在核心驱动节点下创建中间transform，用中间节点作为最终约束源，方便后续调整

    返回:
        tuple: (uvPinNode, outputPlug)
            - uvPinNode: 创建或找到的uvPin节点名称
            - outputPlug: uvPin节点上对应此约束的输出矩阵属性（格式如"uvPin1.outputMatrix[0]"）

    异常:
        Exception: 若指定的约束载体（meshName）在Maya场景中不存在时抛出
    """
    # 检查约束载体（网格/曲面）是否存在，不存在则抛出异常终止流程
    if not cmds.objExists(meshName):
        raise Exception("the mesh {} does not exist".format(meshName))

    # 创建空的组节点（命名规则：目标对象名 + "_rivet"），用于承载UV Pin的输出变换
    # "rivet"意为"铆钉"，形象表示该组会像铆钉一样固定在载体上
    target_group = cmds.group(em=True, name=target + "_rivet")
    # 用父约束将目标对象的当前变换（位置+旋转）复制到空组，随后删除约束
    # 目的：让空组与目标对象初始状态完全对齐，避免约束后位置跳动
    cmds.delete(cmds.parentConstraint(target, target_group))

    # 定义最终约束的驱动源：默认使用上面创建的空组（target_group）
    driver = target_group
    if createMid:
        # 若需要中间节点，在空组下创建transform节点（命名规则：目标对象名 + "_rivet_xform"）
        target_mid = cmds.createNode("transform", name=target + "_rivet_xform", p=target_group)
        # 将驱动源切换为中间节点，后续约束会基于中间节点生效
        driver = target_mid

    # 获取载体的原始形状节点（origShape）：用于UV Pin计算变形前后的位置对比
    # 1. 先尝试获取已存在的原始形状节点（og=True表示original geometry）
    origShape = cmds.deformableShape(meshName, og=True)[0]
    # 2. 若不存在原始形状节点，则自动创建一个
    if not origShape:
        origShape = cmds.deformableShape(meshName, createOriginalGeometry=True)[0]
    # 3. 提取节点名称（去除可能的".shape"后缀，确保是transform节点）
    origShape = origShape.split(".")[0]

    # 获取载体的可变形形状节点（deformShape）：存储载体当前变形后的几何信息
    # （该函数需提前定义，作用类似前序代码中的getDeformShape，获取网格/曲面的核心形状节点）
    deformShape = getDeformShape(meshName)

    # 查找场景中是否已存在与当前载体关联的uvPin节点（避免重复创建）
    uvPinNode = None  # 存储找到或创建的uvPin节点
    connections = []   # 存储载体形状节点的下游连接节点

    # 根据载体类型（NURBS曲面/mesh网格），获取不同的输出属性连接
    if cmds.objectType(deformShape) == "nurbsSurface":
        # NURBS曲面：获取"worldSpace"属性的下游连接节点
        connections = (
            cmds.listConnections(
                "{}.worldSpace".format(deformShape), d=True, s=False, p=False
            )
            or []  # 若无连接，返回空列表
        )
    elif cmds.objectType(deformShape) == "mesh":
        # 网格：获取"worldMesh"属性的下游连接节点
        connections = (
                cmds.listConnections(
                    "{}.worldMesh".format(deformShape), d=True, s=False, p=False
                )
                or []  # 若无连接，返回空列表
        )

    # 遍历连接节点，检查是否有uvPin节点
    for node in connections:
        if cmds.nodeType(node) == "uvPin":
            uvPinNode = node  # 找到已存在的uvPin节点，终止遍历
            break

    # 若未找到已存在的uvPin节点，则创建新的uvPin节点
    if not uvPinNode:
        # 定义uvPin节点名称（命名规则：载体名 + "_uvPin"）
        name = "{}_uvPin".format(meshName)
        uvPinNode = cmds.createNode("uvPin", name=name)

        # 根据载体类型，连接uvPin节点的关键属性（原始几何与变形后几何）
        if cmds.objectType(deformShape) == "nurbsSurface":
            # NURBS曲面：连接变形后曲面（deformedGeometry）和原始曲面（originalGeometry）
            cmds.connectAttr(
                "{}.worldSpace[0]".format(deformShape),
                "{}.deformedGeometry".format(uvPinNode),
                f=True,  # f=True表示强制覆盖现有连接
            )
            cmds.connectAttr(
                "{}.local".format(origShape),
                "{}.originalGeometry".format(uvPinNode),
                f=True,
            )
        elif cmds.objectType(deformShape) == "mesh":
            # 网格：连接变形后网格（deformedGeometry）和原始网格（originalGeometry）
            cmds.connectAttr(
                "{}.worldMesh[0]".format(deformShape),
                "{}.deformedGeometry".format(uvPinNode),
                f=True,
            )
            cmds.connectAttr(
                "{}.outMesh".format(origShape),
                "{}.originalGeometry".format(uvPinNode),
                f=True,
            )

    # 计算目标对象在载体上的UV坐标（用于UV Pin定位）
    # 1. 获取目标对象的世界空间坐标（q=True表示查询，t=True表示translate，ws=True表示world space）
    point = om2.MPoint(cmds.xform(target, q=True, t=True, ws=True))
    uvCoords = []  # 存储计算出的UV坐标（U/V参数）

    # 2. 根据载体类型，用Maya API计算最近点的UV坐标
    if cmds.objectType(deformShape) == "mesh":
        # 网格：通过MFnMesh函数集获取最近点及对应UV
        mfnMesh = mesh.getMeshFn(meshName)  # 获取网格的API函数集（需提前定义mesh模块）
        # 计算世界空间中目标点到网格的最近点（_忽略返回的额外信息）
        closestPoint, _ = mfnMesh.getClosestPoint(point, space=om2.MSpace.kWorld)
        # 根据最近点获取对应的UV坐标
        uvCoords = mfnMesh.getUVAtPoint(closestPoint, space=om2.MSpace.kWorld)
    elif cmds.objectType(deformShape) == "nurbsSurface":
        # NURBS曲面：通过MFnNurbsSurface函数集获取最近点及U/V参数
        mfnSurface = curves.getSurfaceFn(meshName)  # 获取曲面的API函数集（需提前定义curves模块）
        # 计算世界空间中目标点到曲面的最近点，返回最近点坐标和对应的U/V参数
        closestPoint, U, V = mfnSurface.closestPoint(point, space=om2.MSpace.kWorld)
        uvCoords = [U, V]  # 存储U/V参数为UV坐标列表

    # 为UV Pin节点添加新的坐标元素（一个UV Pin可管理多个吸附点）
    # 1. 获取uvPin节点的"coordinate"数组属性（用于存储多个UV坐标）
    plug = plugs._getPlug("{}.coordinate".format(uvPinNode))  # 需提前定义plugs模块，用于属性操作
    # 2. 找到"coordinate"数组的下一个可用索引（避免覆盖已有元素）
    nextIndex = plugs.getNextAvailableElement(plug)
    # 3. 将计算出的UV坐标设置到该索引的coordinateU/coordinateV属性
    cmds.setAttr("{}.coordinateU".format(nextIndex), uvCoords[0])
    cmds.setAttr("{}.coordinateV".format(nextIndex), uvCoords[1])

    # 1. 获取当前UV坐标对应的输出矩阵索引（数组元素数-1，因索引从0开始）
    index = plug.evaluateNumElements() - 1
    # 2. 构造UV Pin的输出矩阵属性路径（如"mesh1_uvPin.outputMatrix[0]"）
    outputPlug = "{}.outputMatrix[{}]".format(uvPinNode, index)

    # 3. 连接输出矩阵到驱动组的偏移父矩阵（offsetParentMatrix）
    # 作用：让驱动组跟随UV Pin的输出变换运动，mo=maintainOffset控制是否保留初始偏移
    cmds.connectAttr(
        outputPlug, "{}.{}".format(target_group, "offsetParentMatrix"), f=True
    )
    matrix.resetTransformations(target_group)

    # 根据指定的约束类型，创建目标对象与驱动源（driver）之间的约束
    if constraint == "parent":
        # 父约束：驱动源同时控制目标对象的位置和旋转
        cmds.parentConstraint(driver, target, st=st, sr=sr, maintainOffset=True)
    elif constraint == "point":
        # 点约束：仅控制目标对象的位置，不影响旋转
        cmds.pointConstraint(driver, target, maintainOffset=True)
    elif constraint == "orient":
        # 方向约束：仅控制目标对象的旋转，不影响位置
        cmds.orientConstraint(driver, target, maintainOffset=True)

    # 返回uvPin节点和对应的输出矩阵属性，供外部后续操作（如修改UV坐标、断开连接等）
    return uvPinNode, outputPlug, target_group


def follicleConstraint(target, meshName, constraint="parent", st=[], sr=[], createMid=False):
    """
    为目标对象创建毛囊约束（Follicle Constraint），使目标对象吸附并跟随网格/曲面运动

    参数:
        target (str): 要被约束的目标对象名称（Maya中的transform节点）
        meshName (str): 作为约束载体的网格或NURBS曲面名称
        constraint (str, optional): 约束类型，默认为"parent"（父约束）
            可选值: "parent"（父约束）、"point"（点约束）、"orient"（方向约束）
        createMid (bool, optional): 是否创建中间过渡节点，默认为False
            若为True，会在毛囊下创建中间transform节点，用中间节点作为约束驱动源

    返回:
        str: 创建的毛囊（follicle）节点名称

    异常:
        Exception: 若指定的网格/曲面对象（meshName）不存在时抛出
    """
    # 检查约束载体（网格/曲面）是否存在，不存在则抛出异常
    if not cmds.objExists(meshName):
        raise Exception("the mesh {} does not exist".format(meshName))

    # 获取约束载体的可变形形状节点（deformShape）
    # 注：可变形形状节点是网格/曲面的核心形状节点，存储几何信息
    deformShape = getDeformShape(meshName)

    # 获取目标对象的世界空间坐标（用于计算在载体上的最近点）
    # om2.MPoint：Maya API 2.0中的点数据类型，用于高精度几何计算
    point = om2.MPoint(cmds.xform(target, q=True, t=True, ws=True))
    uvCoords = []  # 存储载体上最近点的UV参数坐标

    # 根据约束载体的类型（网格/mesh 或 NURBS曲面/nurbsSurface）计算UV坐标
    if cmds.objectType(deformShape) == "mesh":
        # 获取网格的MFnMesh函数集（用于网格几何操作）
        mfnMesh = mesh.getMeshFn(meshName)
        # 计算世界空间中目标点到网格的最近点
        closestPoint, _ = mfnMesh.getClosestPoint(point, space=om2.MSpace.kWorld)
        # 根据最近点获取对应的UV坐标（用于毛囊定位）
        uvCoords = mfnMesh.getUVAtPoint(closestPoint, space=om2.MSpace.kWorld)

    elif cmds.objectType(deformShape) == "nurbsSurface":
        # 获取NURBS曲面的MFnNurbsSurface函数集（用于曲面几何操作）
        mfnSurface = curves.getSurfaceFn(meshName)
        # 计算世界空间中目标点到曲面的最近点，返回最近点坐标和对应的U/V参数
        closestPoint, U, V = mfnSurface.closestPoint(point, space=om2.MSpace.kWorld)
        uvCoords = [U, V]  # 存储NURBS曲面的U/V参数

    # 定义毛囊节点的命名规则（基于目标对象名称）
    name = "{}_follic".format(target)
    follic_shape = name + "Shape"  # 毛囊形状节点名称
    # 创建follicle节点（毛囊节点用于吸附在网格/曲面上并跟随其运动）
    follic_shape = cmds.createNode('follicle', n=follic_shape)
    # 设置毛囊在载体上的UV参数（定位毛囊位置）
    cmds.setAttr(follic_shape + '.parameterU', uvCoords[0])
    cmds.setAttr(follic_shape + '.parameterV', uvCoords[1])
    # 获取毛囊的父transform节点（shape节点的父节点，用于整体变换）
    follic = cmds.listRelatives(follic_shape, p=True)[0]
    # 连接毛囊的输出变换到自身的translate/rotate属性
    cmds.connectAttr(follic_shape + '.outTranslate', follic + '.translate')
    cmds.connectAttr(follic_shape + '.outRotate', follic + '.rotate')
    # 连接载体的世界矩阵到毛囊的输入世界矩阵（用于坐标空间转换）
    cmds.connectAttr(meshName + '.worldMatrix[0]', follic_shape + '.inputWorldMatrix')

    # 定义约束驱动源：默认使用毛囊本身，若createMid为True则使用中间节点
    driver = follic
    if createMid:
        # 创建中间过渡transform节点，父对象设为毛囊
        target_mid = cmds.createNode("transform", name=target + "_rivet_xform", p=follic)
        driver = target_mid  # 将约束驱动源切换为中间节点

    # 根据载体类型，连接对应的输入属性到毛囊
    if cmds.objectType(deformShape) == "nurbsSurface":
        # NURBS曲面：连接曲面的local属性到毛囊的inputSurface
        cmds.connectAttr(meshName + '.local', follic_shape + '.inputSurface')
    elif cmds.objectType(deformShape) == "mesh":
        # 网格：连接网格的outMesh属性到毛囊的inputMesh
        cmds.connectAttr(meshName + '.outMesh', follic_shape + '.inputMesh')

    # 根据指定的约束类型，创建对应的约束
    if constraint == "parent":
        # 父约束：驱动源同时控制目标对象的位置和旋转
        cmds.parentConstraint(driver, target, st=st, sr=sr, maintainOffset=True)
    elif constraint == "point":
        # 点约束：仅控制目标对象的位置
        cmds.pointConstraint(driver, target, maintainOffset=True)
    elif constraint == "orient":
        # 方向约束：仅控制目标对象的旋转
        cmds.orientConstraint(driver, target, maintainOffset=True)

    return follic


def replaceFollicModel():
    """
    替换毛囊（follicle）或UV Pin约束的目标载体模型
    功能逻辑：通过场景选择集操作，将多个毛囊/UV Pin约束从原载体切换到新载体
    选择规则：选中的最后一个对象为【新目标载体】，前面所有选中对象为【待替换约束的毛囊/UV Pin节点】
    """
    # 获取当前Maya场景中的选中对象列表（sl=True表示select list）
    sels = cmds.ls(sl=True)

    # 若未选中任何对象，直接返回，不执行后续操作
    if not sels:
        return

    # 拆分选中对象：前N-1个为待替换约束的毛囊/UV Pin节点（称为rivets，铆钉节点）
    rivets = sels[:-1]
    # 最后一个选中对象为新的约束目标载体模型（即将吸附的新网格/曲面）
    model = sels[-1]

    # 获取新载体模型的可变形形状节点（deformShape，存储核心几何信息）
    modelShape = getDeformShape(model)
    # 获取新载体形状节点的类型（判断是网格mesh还是NURBS曲面nurbsSurface）
    modelShapeType = cmds.objectType(modelShape)

    # 遍历每个待替换约束的节点（rivets列表）
    for rivet in rivets:
        # 获取当前节点的子形状节点（s=True表示shape节点）
        shapes = cmds.listRelatives(rivet, s=True)

        # 分支1：若当前节点是毛囊（follicle）节点（通过shape节点类型判断）
        if shapes and cmds.objectType(shapes[0]) == "follicle":
            # 明确毛囊的shape节点（follicle的核心功能节点）
            follic_shape = shapes[0]

            # 强制重新连接：新载体的世界矩阵 → 毛囊的输入世界矩阵
            cmds.connectAttr(modelShape + '.worldMatrix[0]', follic_shape + '.inputWorldMatrix', f=True)

            # 根据新载体类型，连接对应的输入几何属性
            if modelShapeType == 'nurbsSurface':
                # 若新载体是NURBS曲面：连接曲面的local属性 → 毛囊的inputSurface
                cmds.connectAttr(modelShape + '.local', follic_shape + '.inputSurface', f=True)
            elif modelShapeType == 'mesh':
                # 若新载体是网格：连接网格的outMesh属性 → 毛囊的inputMesh
                cmds.connectAttr(modelShape + '.outMesh', follic_shape + '.inputMesh', f=True)

        # 分支2：若当前节点是UV Pin节点（直接通过节点类型判断）
        elif cmds.objectType(rivet) == "uvPin":
            # 获取新载体的原始形状节点（origShape，用于UV Pin计算变形前后对比）
            origShape = cmds.deformableShape(model, og=True)[0]
            # 若新载体没有原始形状节点，则自动创建一个
            if not origShape:
                origShape = cmds.deformableShape(model, createOriginalGeometry=True)[0]
            # 提取原始形状节点的名称（去除可能的.shape后缀，确保是transform节点）
            origShape = origShape.split(".")[0]

            # 根据新载体类型，重新连接UV Pin的核心属性（变形后几何+原始几何）
            if cmds.objectType(modelShape) == "nurbsSurface":
                # NURBS曲面：连接变形后曲面 → UV Pin的deformedGeometry
                cmds.connectAttr(
                    "{}.worldSpace[0]".format(modelShape),
                    "{}.deformedGeometry".format(rivet),
                    f=True
                )
                # 连接原始曲面 → UV Pin的originalGeometry
                cmds.connectAttr(
                    "{}.local".format(origShape),
                    "{}.originalGeometry".format(rivet),
                    f=True
                )
            elif cmds.objectType(modelShape) == "mesh":
                # 网格：连接变形后网格 → UV Pin的deformedGeometry
                cmds.connectAttr(
                    "{}.worldMesh[0]".format(modelShape),
                    "{}.deformedGeometry".format(rivet),
                    f=True
                )
                # 连接原始网格 → UV Pin的originalGeometry
                cmds.connectAttr(
                    "{}.outMesh".format(origShape),
                    "{}.originalGeometry".format(rivet),
                    f=True
                )



























