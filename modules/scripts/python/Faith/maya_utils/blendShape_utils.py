from maya import cmds
import maya.mel as mel


def blendShapeNode(MeshNode):
    BlendShapeNode = []
    try:
        meshHistory = cmds.listHistory(MeshNode, pdo=True)
        BlendShapeNode = cmds.ls(meshHistory, type='blendShape')
    except TypeError:
        pass

    return BlendShapeNode


def meshOrig(meshNode):
    MeshOrigList = []
    Mesh_Orig = cmds.listHistory(meshNode)
    for i in range(len(Mesh_Orig)):
        if cmds.nodeType(Mesh_Orig[i]) == 'mesh':
            if 'Orig' in Mesh_Orig[i]:
                if Mesh_Orig[i] != None:
                    if cmds.listConnections(Mesh_Orig[i] + '.worldMesh[0]', source=True):
                        MeshOrigList.append(Mesh_Orig[i])

    return MeshOrigList


def GetWeightIndex(blendShapeNode, target):
    aliases = cmds.aliasAttr(blendShapeNode, q=True)
    a = aliases.index(target)
    weight = aliases[a + 1]
    index = weight.split('[')[-1][:-1]
    return int(index)


def InputTargetGroup(blendShapeNode, target):
    tragetIndexItem = GetWeightIndex(blendShapeNode, target)
    return tragetIndexItem


def creativeTarget(blendShape, target = [], prefix = None):
    listConnect = []
    listConnect_target = []
    listLock_target = []
    listValue_target = []
    listConnect_Name = []
    MeshOrigList = []
    listTargetBlendShape = cmds.listAttr(blendShape + '.weight', multi=True)

    for i in listTargetBlendShape:
        if cmds.getAttr(blendShape + '.' + i, l=1) == True:
            cmds.setAttr(blendShape + '.' + i, l=0)
            listLock_target.append(i)
        get = cmds.getAttr(blendShape + '.' + i)
        listValue_target.append(get)
        targetConnect = cmds.listConnections(blendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, blendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        cmds.setAttr(blendShape + '.' + i, 0)

    MeshOrigList = meshOrig(blendShape)

    for x in target:
        if listTargetBlendShape.__contains__(x) != 1 or 'weight[' in x:
            continue
        tragetIndexItem = InputTargetGroup(blendShape, x)
        inputTargetItem = cmds.getAttr(blendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        for c in inputTargetItem:
            indexInt = (int(c) - 5000) / 1000.0
            Mesh = cmds.createNode('mesh', name=x + '_Shape')
            MeshMianShape = cmds.createNode('mesh', name=x + '_MianShape')
            cmds.sets(Mesh, edit=True, forceElement='initialShadingGroup')
            listRel = cmds.listRelatives(Mesh, p=True)
            MianlistRel = cmds.listRelatives(MeshMianShape, p=True)
            cmds.setAttr(blendShape + '.' + x, float(indexInt))
            cmds.connectAttr(blendShape + '.outputGeometry[0]', MeshMianShape + '' + '.inMesh')
            cmds.connectAttr(MeshOrigList[0] + '.outMesh', Mesh + '' + '.inMesh')
            copyMesh = cmds.duplicate(MianlistRel)
            count = str(indexInt).split('.')
            if count[0] == '-0':
                ne = 'm'
            else:
                ne = 'p'
            if float(indexInt) == 1:
                targetName = x
            else:
                targetName = x + '_' + ne + count[1]
            # cmds.parent(copyMesh, blendShape + '_Grp')
            if prefix == 1:
                targetName = '_' + targetName
            ToName = cmds.rename(copyMesh, targetName)
            cmds.addAttr(ToName, longName=x, at='double')
            cmds.setAttr(ToName + '.' + x, float(indexInt))
            cmds.setAttr(blendShape + '.' + x, 0)
            cmds.delete(listRel, MianlistRel)
            listConnect_Name.append(ToName)

    for i in range(len(listTargetBlendShape)):
        val = listValue_target[i]
        cmds.setAttr(blendShape + '.' + listTargetBlendShape[i], val)

    for i in listLock_target:
        cmds.setAttr(blendShape + '.' + i, l=1)

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], blendShape + '.' + listConnect_target[i])

    return listConnect_Name


def tragetIndexItem(bsNode, target):
    """
    GetWeightIndex = 'gg_GetWeightIndex '+str(self.BlendShape[0])+' '+str(self.tragetBlendShape)+' '
    tragetIndexItem  = mel.eval(GetWeightIndex)
    return tragetIndexItem
    """
    tragetIndexItem = GetWeightIndex(bsNode, target)
    return tragetIndexItem


def rebuildTargetItems(TargetGeo, delTarget):
    sels = cmds.ls(sl=True, type='transform')
    listConnect = []
    listConnect_target = []
    listConnect_get = []
    TargetBlendShapeList = blendShapeNode(TargetGeo)
    if TargetBlendShapeList != [] and len(TargetBlendShapeList) == 1:
        TargetBlendShape = TargetBlendShapeList[0]
        if TargetBlendShape == TargetGeo + '_blendShape':
            TargetBlendShape = cmds.rename(TargetBlendShape, TargetBlendShape + '_old')
    elif len(TargetBlendShapeList) > 1:
        cmds.error(u'#------More than one blendShape Node')
    elif TargetBlendShapeList == []:
        cmds.error('#------There is no blendShape Node')
    if cmds.getAttr(TargetBlendShape + '.envelope') != 1:
        cmds.setAttr(TargetBlendShape + '.envelope', 1)
    listTarget = cmds.listAttr(TargetBlendShape + '.weight', multi=True)
    listShpae = cmds.listRelatives(TargetGeo, s=True)
    listTargetBlendShape = listTarget
    TargetGeoNewBlendShape = TargetGeo + '_blendShape'
    TargetGeoNewBlendShape = cmds.blendShape(TargetGeo, exclusive='deformPartition#', frontOfChain=True, name=TargetGeoNewBlendShape)[0]
    xi = 0
    for i in listTargetBlendShape:
        targetConnect = cmds.listConnections(TargetBlendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, TargetBlendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        else:
            get = i + '>' + str(cmds.getAttr(TargetBlendShape + '.' + i))
            listConnect_get.append(get)
        cmds.setAttr(TargetBlendShape + '.' + i, 0)

    for x in listTargetBlendShape:
        tragetIndexItem = InputTargetGroup(TargetBlendShape, x)
        inputTargetItem = cmds.getAttr(TargetBlendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        ToNames = creativeTarget(TargetBlendShape, [x], None)
        for i in range(len(inputTargetItem)):
            c = inputTargetItem[i]
            ToName = ToNames[i]
            indexInt = (int(c) - 5000) / 1000.0
            if float(indexInt) == 1:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 1.0))
            else:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, ib=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 float(indexInt)))

        if delTarget == 'yes':
            cmds.delete(ToNames)
        xi += 1

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], TargetBlendShape + '.' + listConnect_target[i])
        cmds.connectAttr(listConnect[i], TargetGeoNewBlendShape + '.' + listConnect_target[i])

    for i in listConnect_get:
        listConnect_wt = i.split('>')
        cmds.setAttr(TargetBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))
        cmds.setAttr(TargetGeoNewBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))

    cmds.delete(TargetBlendShape)
    cmds.select(sels)
    return


    def tragetIndexItem(self):
        """
        GetWeightIndex = 'gg_GetWeightIndex '+str(self.BlendShape[0])+' '+str(self.tragetBlendShape)+' '
        tragetIndexItem  = mel.eval(GetWeightIndex)
        return tragetIndexItem
        """
        tragetIndexItem = GetWeightIndex(self.BlendShape[0], self.tragetBlendShape)
        return tragetIndexItem


def FGMirrorShapes(originalObj, shapeToCopy, xyz, shapePosition, newName, shapeOffset):
    OriginalObjTX = originalObj + '.tx'
    cmds.setAttr(OriginalObjTX, lock=0)
    OriginalObjTY = originalObj + '.ty'
    cmds.setAttr(OriginalObjTY, lock=0)
    OriginalObjTZ = originalObj + '.tz'
    cmds.setAttr(OriginalObjTZ, lock=0)
    OriginalObjRX = originalObj + '.rx'
    cmds.setAttr(OriginalObjRX, lock=0)
    OriginalObjRY = originalObj + '.ry'
    cmds.setAttr(OriginalObjRY, lock=0)
    OriginalObjRZ = originalObj + '.rz'
    cmds.setAttr(OriginalObjRZ, lock=0)
    OriginalObjSX = originalObj + '.sx'
    cmds.setAttr(OriginalObjSX, lock=0)
    OriginalObjSY = originalObj + '.sy'
    cmds.setAttr(OriginalObjSY, lock=0)
    OriginalObjSZ = originalObj + '.sz'
    cmds.setAttr(OriginalObjSZ, lock=0)
    mirrorObj = shapeToCopy + 'suffTemp'
    cmds.duplicate(originalObj, rr=1, n='scaleObj')
    cmds.duplicate(originalObj, rr=1, n='tempName')
    cmds.rename('tempName', mirrorObj)
    cmds.setAttr(OriginalObjTX, lock=0)
    cmds.setAttr(OriginalObjTY, lock=0)
    cmds.setAttr(OriginalObjTZ, lock=0)
    cmds.setAttr(OriginalObjRX, lock=0)
    cmds.setAttr(OriginalObjRY, lock=0)
    cmds.setAttr(OriginalObjRZ, lock=0)
    cmds.setAttr(OriginalObjSX, lock=0)
    cmds.setAttr(OriginalObjSY, lock=0)
    cmds.setAttr(OriginalObjSZ, lock=0)
    posScaleAttr = 0
    negScaleAttr = 0
    if xyz == 1:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleX'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleX', negScaleAttr)
    if xyz == 2:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleY'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleY', negScaleAttr)
    if xyz == 3:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleZ'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleZ', negScaleAttr)
    cmds.blendShape(shapeToCopy, 'scaleObj', frontOfChain=1, n='blendShapeToWarp')
    cmds.select(mirrorObj, 'scaleObj', r=1)
    wrap = mel.eval('doWrapArgList "6" { "1","0","1", "2", "1", "1", "0" };')
    cmds.rename(wrap[0], 'wrapToMirror')
    cmds.setAttr('wrapToMirror.exclusiveBind', 1)
    blendShapeAttr = 'blendShapeToWarp.' + shapeToCopy
    cmds.setAttr(blendShapeAttr, 1)
    cmds.select(mirrorObj, r=1)
    cmds.DeleteHistory
    cmds.delete(ch=1)
    cmds.delete('scaleObjBase', 'scaleObj')
    offsetX = shapeOffset[0]
    offsetY = shapeOffset[1]
    offsetZ = shapeOffset[2]
    if shapePosition == 1:
        shapeTCAttrX = shapeToCopy + '.tx'
        shapeTCAttrY = shapeToCopy + '.ty'
        shapeTCAttrZ = shapeToCopy + '.tz'
        shapeTCPositionX = float(cmds.getAttr(shapeTCAttrX)) + offsetX
        shapeTCPositionY = float(cmds.getAttr(shapeTCAttrY)) + offsetY
        shapeTCPositionZ = float(cmds.getAttr(shapeTCAttrZ)) + offsetZ
        mirrorObjPositionX = mirrorObj + '.tx'
        mirrorObjPositionY = mirrorObj + '.ty'
        mirrorObjPositionZ = mirrorObj + '.tz'
        cmds.setAttr(mirrorObjPositionX, shapeTCPositionX)
        cmds.setAttr(mirrorObjPositionY, shapeTCPositionY)
        cmds.setAttr(mirrorObjPositionZ, shapeTCPositionZ)
    cmds.select(mirrorObj, r=1)
    cmds.rename(mirrorObj, newName)


def seekOutBs(skipLock=True, replaceConnect=True, bsList=[]):
    """seek out blendshape targt with original connection """

    meshList = cmds.ls(sl=True)
    length = len(meshList)

    if length == 2:
        pass
    else:
        cmds.error('please select aimMesh(1st) and orgMesh(2st)')

    aimObject = meshList[0]
    orgObject = meshList[1]

    # get org blendShape node
    bsNode = blendShapeNode(orgObject)

    if bsNode is not None:
        bsNode  = bsNode[0]
        if bsList is not None:
            targtGrp = cmds.createNode('transform', name=orgObject + '_targt_grp')
            if aimObject is not None:

                for bs in bsList:
                    if skipLock:
                        result = cmds.getAttr(bsNode + '.' + bs, lock=True)
                        if result:
                            pass
                        else:
                            cmds.select(aimObject)
                            cmds.select(orgObject, add=True)
                            warpNode = mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0"}')[0]
                            cmds.select(cl=True)
                            cmds.setAttr(bsNode + '.' + bs, 1)
                            cmds.duplicate(aimObject, name=bs)
                            cmds.delete(warpNode)
                            cmds.setAttr(bsNode + '.' + bs, 0)

                    elif not skipLock:
                        cmds.select(aimObject)
                        cmds.select(orgObject, add=True)
                        warpNode = mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0"}')[0]
                        cmds.select(cl=True)
                        cmds.setAttr(bsNode + '.' + bs, 1)
                        cmds.duplicate(aimObject, name=bs)
                        cmds.delete(warpNode)
                        cmds.setAttr(orgObject + '.' + bs, 0)

                        # clean
                    if cmds.objExists(orgObject + 'Base'):
                        cmds.delete(orgObject + 'Base')
                    if cmds.objExists(bs):
                        cmds.parent(bs, targtGrp)

                # create aimObject blendShape
                targetList = cmds.listRelatives(targtGrp)
                newBsNode = cmds.blendShape(targetList, aimObject, tc=True, name=aimObject + '_seekOutBsNode')[0]

                cmds.delete(targtGrp)
                # rebuild connection
                if replaceConnect:
                    for bs in targetList:
                        attrSource = cmds.connectionInfo(bsNode + '.' + bs, sfd=1)
                        if attrSource != '':
                            cmds.connectAttr(attrSource, newBsNode + '.' + bs)

