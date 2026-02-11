import maya.cmds as mc
from maya import cmds
from rxCore import aboutLock
# ntype: type node need create
# mo: constraint offset
# wuo: worldUpMatrix object
# ch: slide
# po: point constraint
# mpnode: rivet group or user design
# exactpos: different pivot set
# offNode: offset node
# pocDrv: position driver node


def mesh(nodes, poly, ntype='transform', mo=True, po=False, ch=False, mpnode=None, exactpos=False):

    nodes = mc.ls(nodes)
    shapes = mc.listRelatives(poly, ni=1, type='mesh')
    if not shapes:
        mc.error('Not a poly Mesh!')
    shape = shapes[0]

    returns = []
    for n in nodes:
        # get unique name
        name = n + '_rvt'

        # create Fll
        mc.select(n)
        loc = mc.spaceLocator()
        if exactpos:
            mc.delete(mc.pointConstraint(n, loc))

        fll = mc.createNode(ntype, n=name)
        fllShape = mc.createNode('follicle', n=fll + 'Shape', p=fll)

        mc.connectAttr(fllShape + '.outRotate', fll + '.rotate')
        mc.connectAttr(fllShape + '.outTranslate', fll + '.translate')
        mc.connectAttr(poly + '.worldMatrix[0]',
                       fllShape + '.inputWorldMatrix')

        # do it for meshs
        mc.connectAttr(shape + '.outMesh', fllShape + '.inputMesh')
        cpos = mc.createNode('closestPointOnMesh', n=fll + '_cpos')
        mc.connectAttr(shape + '.outMesh', cpos + '.inMesh')
        mc.connectAttr(poly + '.worldMatrix[0]', cpos + '.inputMatrix')
        mc.setAttr(cpos + '.inPositionX', mc.xform(loc, q=1, ws=1, t=1)[0])
        mc.setAttr(cpos + '.inPositionY', mc.xform(loc, q=1, ws=1, t=1)[1])
        mc.setAttr(cpos + '.inPositionZ', mc.xform(loc, q=1, ws=1, t=1)[2])
        u = mc.getAttr(cpos + '.parameterU')
        v = mc.getAttr(cpos + '.parameterV')

        mc.setAttr(fllShape + '.parameterU', u)
        mc.setAttr(fllShape + '.parameterV', v)

        # leave cpom history
        if ch:
            mc.connectAttr(cpos + '.parameterU', fllShape + '.parameterU')
            mc.connectAttr(cpos + '.parameterV', fllShape + '.parameterV')
        else:
            mc.delete(cpos)

        # parent
        if not mpnode:
            mpnode = 'rivets'

        if not mc.objExists(mpnode):
            noX = mc.ls('noTransform_geo', 'noTransform')
            mc.createNode('transform', n=mpnode)
            mc.setAttr(mpnode + '.inheritsTransform', 0)
            mc.setAttr(mpnode + '.inheritsTransform', l=1)
            aboutLock.lock(mpnode)

            if noX:
                mc.parent(mpnode, noX[0])

        wX = mc.ls('worldTransform_geo', 'worldTransform')
        if wX:
            mc.scaleConstraint(wX, fll, n=fll + '_sc')

        # cleanup
        mc.parent(fll, mpnode)
        mc.delete(loc)

        # constrain node
        if po:
            mc.pointConstraint(fll, n, n=n + '_pc', mo=mo)
        else:
            mc.parentConstraint(fll, n, n=n + '_prc', mo=mo)
        returns.append(fll)

    mc.select(returns)
    return returns


def surface(nodes, nurbs, mpnode=None, con='prc', mo=True, offNode=True, pocDrv=None):

    if not mpnode:
        mpnode = 'rivets'

    nodes = mc.ls(nodes)
    nox = mpnode

    # check nurbs
    shapes = mc.listRelatives(nurbs, type='nurbsSurface')
    if not shapes:
        mc.error('Not a Nurbs Surface!')

    # create nox group
    if not mc.objExists(nox):
        nox = mc.createNode('transform', n=nox)
        mc.setAttr(nox + '.inheritsTransform', 0)

    fllList = []

    for node in nodes:

        poc = mc.createNode('closestPointOnSurface')
        mc.connectAttr(nurbs + '.worldSpace', poc + '.inputSurface')

        mc.setAttr(poc + '.inPositionX', mc.xform(node, q=1, ws=1, t=1)[0])
        mc.setAttr(poc + '.inPositionY', mc.xform(node, q=1, ws=1, t=1)[1])
        mc.setAttr(poc + '.inPositionZ', mc.xform(node, q=1, ws=1, t=1)[2])

        fll = mc.createNode('transform', n=node + '_fll', p=nox)
        fllShape = mc.createNode('follicle', n=(fll + 'Shape'), p=fll)
        mc.hide(fllShape)
        fllList.append(fll)

        mc.connectAttr((fllShape + ".outRotate"), (fll + ".rotate"), f=1)
        mc.connectAttr((fllShape + ".outTranslate"), (fll + ".translate"), f=1)
        mc.connectAttr(
            (nurbs + ".worldMatrix[0]"), (fllShape + ".inputWorldMatrix"), f=1)
        mc.connectAttr((nurbs + ".local"), (fllShape + ".inputSurface"), f=1)

        mc.setAttr(fllShape + '.simulationMethod', 0)
        mc.setAttr(fllShape + '.startDirection', 0)

        if pocDrv:
            world = mc.createNode('transform', n=pocDrv + 'World', p=mpnode)
            mc.pointConstraint(pocDrv, world, n=world + '_pc')
            mc.connectAttr(world + '.t', poc + '.inPosition')
            mc.connectAttr(poc + '.parameterU', fllShape + '.parameterU')
            mc.connectAttr(poc + '.parameterV', fllShape + '.parameterV')

        else:
            paramU = mc.getAttr(poc + '.parameterU')
            paramV = mc.getAttr(poc + '.parameterV')
            mc.setAttr((fllShape + '.parameterU'), paramU)
            mc.setAttr((fllShape + '.parameterV'), paramV)
            mc.delete(poc)

        if offNode:
            off = mc.createNode('transform', n=fll + 'Off', p=fll)
            mc.delete(mc.parentConstraint(node, off))

    for node in nodes:
        if offNode:
            off = node + '_fllOff'
        else:
            off = node + '_fll'

        if 'pc' in con:
            mc.pointConstraint(off, node, n=node + '_pc', mo=mo)
        if 'oc' in con:
            mc.orientConstraint(off, node, n=node + '_oc', mo=mo)
        if con == 'prc':
            mc.parentConstraint(off, node, n=node + '_prc', mo=mo)

    return fllList


def curve(nodes, crv, con=True, mo=True, wuo=None, mpnode=None):
    """
    :param nodes: transform
    :param crv: curve name
    :param mo: True / False
    :param wuo: dict { upObjects:[], frontAxis:0, upAxis:1, worldUpVector:(1,0,0), 'inverseFront':0 } len(upObjects) = len(nodes)
    :param con: True / False
    :param mpnode: none / transform
    :return:
    """
    if not mpnode:
        mpnode = 'rivets'

    # check curve
    shapes = mc.listRelatives(crv, type='nurbsCurve')
    if mc.nodeType(crv) == 'nurbsCurve' or mc.nodeType(crv) == 'curveVarGroup':
        shapes = [crv]
    elif not shapes:
        mc.error('Not a Nurbs Curve!')

    # create do not touch group
    if not mc.objExists(mpnode):
        mpnode = mc.createNode('transform', n=mpnode)

    cpoc = mc.createNode('nearestPointOnCurve')
    mc.connectAttr(shapes[0] + '.worldSpace', cpoc + '.ic')

    mpxs = []
    for i, node in enumerate(nodes):
        pos = mc.xform(node, ws=1, q=1, t=1)
        mc.setAttr(cpoc + '.inPosition', pos[0], pos[1], pos[2])
        paramu = mc.getAttr(cpoc + '.pr')
        mpx = mc.createNode('transform', n='{0}_mpx'.format(node), p=mpnode)
        mp = mc.createNode('motionPath', n='{0}_mpNode'.format(node))
        mc.setAttr(mp + '.uValue', paramu)
        mpxs.append(mpx)

        mc.connectAttr(shapes[0] + '.worldSpace', mp + '.geometryPath')
        mc.connectAttr(mp + '.xCoordinate', mpx + '.tx')
        mc.connectAttr(mp + '.yCoordinate', mpx + '.ty')
        mc.connectAttr(mp + '.zCoordinate', mpx + '.tz')

        if wuo:
            mc.setAttr(mp + '.follow', 1)
            mc.setAttr(mp + '.worldUpType', 2)
            mc.setAttr(mp+ '.inverseFront', wuo['inverseFront'])
            mc.setAttr(mp + '.upAxis', wuo['upAxis'])
            mc.setAttr(mp + '.frontAxis', wuo['frontAxis'])
            mc.setAttr(mp + '.worldUpVectorX', wuo['worldUpVector'][0])
            mc.setAttr(mp + '.worldUpVectorY', wuo['worldUpVector'][1])
            mc.setAttr(mp + '.worldUpVectorZ', wuo['worldUpVector'][2])
            mc.connectAttr(wuo['upObjects'][i] + '.worldMatrix[0]', mp + '.worldUpMatrix')
            mc.connectAttr(mp + '.r', mpx + '.r')
            if con:
                mc.pointConstraint(mpx, node, n=node + '_pc', mo=mo)
                mc.orientConstraint(mpx, node, n=node + '_oc', mo=mo)

        else:
            if con:
                mc.pointConstraint(mpx, node, n=node + '_pc', mo=mo)
    # clean
    return mpxs


def matrixSurface(nodes, nurbs, mpnode=None, con='prc', mo=True):

    # load matrix plug
    if not mc.pluginInfo('matrixNodes', query=True, loaded=True):
        mc.loadPlugin('matrixNodes')

    if not mc.objExists(nurbs):
        return

    nodes = mc.ls(nodes)

    # check type
    shape = mc.listRelatives(nurbs, c=True)[0]
    shapeType = mc.nodeType(shape, api=True)
    if shapeType != 'kNurbsSurface':
        mc.error('%s is not kNurbsSurface !' % nurbs)
        return

    # create node
    for node in nodes:

        pointOnSurface = mc.createNode(
            'pointOnSurfaceInfo', n=node + '_pointOnSurface')
        mc.connectAttr(
            shape + '.worldSpace[0]', pointOnSurface + '.inputSurface')
        paramLengthU = mc.getAttr(shape + '.minMaxRangeU')
        paramLengthV = mc.getAttr(shape + '.minMaxRangeV')

        poc = mc.createNode('closestPointOnSurface', n='TEMP_poc')
        mc.connectAttr(nurbs + '.worldSpace', poc + '.inputSurface')

        mc.setAttr(poc + '.inPositionX', mc.xform(node, q=1, ws=1, t=1)[0])
        mc.setAttr(poc + '.inPositionY', mc.xform(node, q=1, ws=1, t=1)[1])
        mc.setAttr(poc + '.inPositionZ', mc.xform(node, q=1, ws=1, t=1)[2])
        uPos = mc.getAttr(poc + '.parameterU')
        vPos = mc.getAttr(poc + '.parameterV')

        rivetLoc = mc.spaceLocator(n=node + '_rivet_loc')[0]
        mc.addAttr(rivetLoc, longName='parameterU',
                   at='float', keyable=True, dv=uPos)
        mc.addAttr(rivetLoc, longName='parameterV',
                   at='float', keyable=True, dv=vPos)

        mc.addAttr(rivetLoc + '.parameterU', e=True, min=paramLengthU[0][1])
        mc.addAttr(rivetLoc + '.parameterU', e=True, max=paramLengthU[0][1])
        mc.addAttr(rivetLoc + '.parameterV', e=True, min=paramLengthV[0][0])
        mc.addAttr(rivetLoc + '.parameterV', e=True, max=paramLengthV[0][1])

        mc.connectAttr(rivetLoc + '.parameterU',
                       pointOnSurface + '.parameterU')
        mc.connectAttr(rivetLoc + '.parameterV',
                       pointOnSurface + '.parameterV')

        # Compose a 4x4 matrix
        mtx = mc.createNode('fourByFourMatrix', n=node + '_4by4_mtx')
        outMatrix = mc.createNode('decomposeMatrix', n=node + '_dec_mtx')
        mc.connectAttr(mtx + '.output', outMatrix + '.inputMatrix')

        mc.connectAttr(outMatrix + '.outputTranslate', rivetLoc + '.translate')
        mc.connectAttr(outMatrix + '.outputRotate', rivetLoc + '.rotate')

        mc.connectAttr(pointOnSurface + '.normalizedTangentUX', mtx + '.in00')
        mc.connectAttr(pointOnSurface + '.normalizedTangentUY', mtx + '.in01')
        mc.connectAttr(pointOnSurface + '.normalizedTangentUZ', mtx + '.in02')
        mc.setAttr(mtx + '.in03', 0)

        mc.connectAttr(pointOnSurface + '.normalizedNormalX', mtx + '.in10')
        mc.connectAttr(pointOnSurface + '.normalizedNormalY', mtx + '.in11')
        mc.connectAttr(pointOnSurface + '.normalizedNormalZ', mtx + '.in12')
        mc.setAttr(mtx + '.in13', 0)

        mc.connectAttr(pointOnSurface + '.normalizedTangentVX', mtx + '.in20')
        mc.connectAttr(pointOnSurface + '.normalizedTangentVY', mtx + '.in21')
        mc.connectAttr(pointOnSurface + '.normalizedTangentVZ', mtx + '.in22')
        mc.setAttr(mtx + '.in23', 0)

        mc.connectAttr(pointOnSurface + '.positionX', mtx + '.in30')
        mc.connectAttr(pointOnSurface + '.positionY', mtx + '.in31')
        mc.connectAttr(pointOnSurface + '.positionZ', mtx + '.in32')
        mc.setAttr(mtx + '.in33', 0)

        if 'pc' in con:
            mc.pointConstraint(rivetLoc, node, n=node + '_pc', mo=mo)
        if 'oc' in con:
            mc.orientConstraint(rivetLoc, node, n=node + '_oc', mo=mo)
        if con == 'prc':
            mc.parentConstraint(rivetLoc, node, n=node + '_prc', mo=mo)

        # clean
        if not mpnode:
            mpnode = 'rivets'

        if not mc.objExists(mpnode):
            mc.createNode('transform', n=mpnode)
            mc.setAttr(mpnode + '.inheritsTransform', 0)
            mc.setAttr(mpnode + '.inheritsTransform', l=1)

        if mc.objExists(mpnode):
            mc.parent(rivetLoc, mpnode)

    return mpnode


def get_uv_at_surface(node, dest_node):
    """

    :param node:
    :param dest_node:
    :return:
    """
    grp = cmds.group(em=True)
    cmds.parentConstraint(node, grp, mo=False)
    closest_PointNode = cmds.createNode("closestPointOnSurface")
    cmds.connectAttr(grp + '.translateX', closest_PointNode + '.inPosition.inPositionX')
    cmds.connectAttr(grp + '.translateY', closest_PointNode + '.inPosition.inPositionY')
    cmds.connectAttr(grp + '.translateZ', closest_PointNode + '.inPosition.inPositionZ')
    cmds.connectAttr(dest_node + ".local", closest_PointNode + ".inputSurface")
    minMaxRangeU = int(cmds.getAttr(dest_node + '.minMaxRangeU')[0][1])
    minMaxRangeV = int(cmds.getAttr(dest_node + '.minMaxRangeV')[0][1])
    U = cmds.getAttr(closest_PointNode + '.result.parameterU') / minMaxRangeU
    V = cmds.getAttr(closest_PointNode + '.result.parameterV') / minMaxRangeV
    cmds.delete([closest_PointNode, grp])
    return U, V


def rivetSurface(tempGrp, surface):
    posi = cmds.createNode("pointOnSurfaceInfo", name=f"{tempGrp}_posi")
    fourByFour = cmds.createNode("fourByFourMatrix", name=f"{tempGrp}_fourByFour")
    decomp = cmds.createNode("decomposeMatrix", name=f"{tempGrp}_decomp")
    cmds.connectAttr(f"{surface}.worldSpace[0]", f"{posi}.inputSurface")
    uv = get_uv_at_surface(tempGrp, surface)
    cmds.setAttr(f"{posi}.parameterU", uv[0])
    cmds.setAttr(f"{posi}.parameterV", uv[1])
    cmds.connectAttr(f"{posi}.result.normalizedTangentU.normalizedTangentUX", f"{fourByFour}.in00")
    cmds.connectAttr(f"{posi}.result.normalizedTangentU.normalizedTangentUY", f"{fourByFour}.in01")
    cmds.connectAttr(f"{posi}.result.normalizedTangentU.normalizedTangentUZ", f"{fourByFour}.in02")

    cmds.connectAttr(f"{posi}.result.normalizedNormal.normalizedNormalX", f"{fourByFour}.in10")
    cmds.connectAttr(f"{posi}.result.normalizedNormal.normalizedNormalY", f"{fourByFour}.in11")
    cmds.connectAttr(f"{posi}.result.normalizedNormal.normalizedNormalZ", f"{fourByFour}.in12")

    cmds.connectAttr(f"{posi}.result.normalizedTangentV.normalizedTangentVX", f"{fourByFour}.in20")
    cmds.connectAttr(f"{posi}.result.normalizedTangentV.normalizedTangentVY", f"{fourByFour}.in21")
    cmds.connectAttr(f"{posi}.result.normalizedTangentV.normalizedTangentVZ", f"{fourByFour}.in22")

    cmds.connectAttr(f"{posi}.result.position.positionX", f"{fourByFour}.in30")
    cmds.connectAttr(f"{posi}.result.position.positionY", f"{fourByFour}.in31")
    cmds.connectAttr(f"{posi}.result.position.positionZ", f"{fourByFour}.in32")

    cmds.connectAttr(f"{posi}.result.position", f"{tempGrp}.translate")
    cmds.connectAttr(f"{fourByFour}.output", f"{decomp}.inputMatrix")
    cmds.connectAttr(f"{decomp}.outputRotate", f"{tempGrp}.rotate")



