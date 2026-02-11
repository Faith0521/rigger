# coding:utf-8
from maya import cmds


def copymodel(*args):
    """copy model"""
    sels = cmds.ls(sl=True)
    attrs = ['tx',
             'ty',
             'tz',
             'rx',
             'ry',
             'rz',
             'sx',
             'sy',
             'sz']
    copysels = []
    for sel in sels:
        copysel = cmds.duplicate(sel, name=sel + '_duplicate')[0]
        copysels.append(copysel)
        shapes = cmds.listRelatives(copysel, s=True, f=True)
        for shape in shapes:
            if cmds.getAttr(shape + '.intermediateObject') == 1:
                cmds.delete(shape)

        for attr in attrs:
            cmds.setAttr(copysel + '.' + attr, lock=0)

    cmds.select(copysels)


def getCurveLength(*args):
    crvs = cmds.ls(sl=True)
    for crv in crvs:
        arclenNode = cmds.arclen(crv, ch=1)
        cmds.warning(crv + u'长度------' + str(cmds.getAttr(arclenNode + '.arcLength')))
        cmds.delete(arclenNode)


def get_model_shaders(model_name):
    shapes = cmds.listRelatives(model_name, shapes=True, fullPath=True) or []

    shaders = []
    for shape in shapes:
        shading_engines = cmds.listConnections(shape, type="shadingEngine") or []
        for se in shading_engines:
            materials = cmds.ls(cmds.listConnections(se), materials=True)
            shaders.extend(materials)

    return list(set(shaders))


def driveGama(*args):
    selection = cmds.ls(sl=1)
    if not selection:
        cmds.warning(u"请选择一个模型!")
        return
    shaders = get_model_shaders(selection[0])
    if not shaders:
        RuntimeError(u"选择的模型没有材质球")
    sourceConnections = cmds.listConnections(shaders[0] + ".color", s=1, d=0)
    if not sourceConnections:
        RuntimeError(u"选择的模型材质球没有连接")

    gamas = [s for s in sourceConnections if cmds.objectType(s) == "gammaCorrect"]

    if not gamas:
        gama = cmds.createNode("gammaCorrect")
        cmds.disconnectAttr(sourceConnections[0] + ".outColor", shaders[0] + ".color")
        cmds.connectAttr(sourceConnections[0] + ".outColor", gama + ".value")
        cmds.connectAttr(gama + ".outValue", shaders[0] + ".color")
        gamas.append(gama)

    if cmds.objExists("Visibility.pupilGamma"):
        [cmds.setDrivenKeyframe(
            "{0}.gamma{1}".format(gamas[0], axis),
            currentDriver="Visibility.pupilGamma",
            driverValue=0,
            value=1.3) for axis in ["X", "Y", "Z"]]
        [cmds.setDrivenKeyframe(
            "{0}.gamma{1}".format(gamas[0], axis),
            currentDriver="Visibility.pupilGamma",
            driverValue=1,
            value=1.6) for axis in ["X", "Y", "Z"]]


def transferSkinWeights(type="import", *args):
    try:
        cmds.loadPlugin("transferSkinWeights")
    except:
        pass

    if type=="import":
        cmds.skinWeightBatch(i=True, f=cmds.fileDialog2(fileFilter="*.swb", dialogStyle=2, fileMode=1)[0])
    else:
        cmds.skinWeightBatch(e=True, f=cmds.fileDialog2(fileFilter="*.swb", dialogStyle=2, fileMode=0)[0])


def convertSkin2NgLayer():
    selected = cmds.ls(sl=1)
    if not selected:
        return
    if len(selected) > 2:
        print("Please select one joint and one mesh!")

    mesh = selected[-1]
    joint = selected[0]

    from imp import reload
    import Faith.tools.small_tools.jointMask as mask
    reload(mask)
    mask.SkinLayer(mesh).build(joint)
