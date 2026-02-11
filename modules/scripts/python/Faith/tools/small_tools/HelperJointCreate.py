# coding:utf-8
from imp import reload
from pymel.core import *
from pymel.core import PyNode
from ...maya_utils import controller_utils as ctrl
reload(ctrl)


def OneToOneCreateParentMatrix(targetObj, aimObj, T=True, R=True, S=True):
    """

    :param targetObj:
    :param aimObj:
    :param T:
    :param R:
    :param S:
    :return:
    """
    parentMult = createNode("multMatrix", n="%s_parentMM" % aimObj)
    father_ma = aimObj.worldMatrix[0].get()
    parent_RevMatrix = targetObj.worldInverseMatrix[0].get()
    parentMult.matrixIn[0].set(father_ma * parent_RevMatrix)
    targetObj.worldMatrix[0] >> parentMult.matrixIn[1]
    aimObj.parentInverseMatrix[0] >> parentMult.matrixIn[2]

    parentDecomp = createNode("decomposeMatrix", n="%s_parentDPM" % aimObj)
    parentMult.matrixSum >> parentDecomp.inputMatrix

    if T:
        parentDecomp.outputTranslate >> aimObj.translate

    if S:
        parentDecomp.outputScale >> aimObj.scale

    if R:
        fa_quatPr = createNode("quatProd", n="%s_quatPr" % aimObj)
        parentDecomp.outputQuat >> fa_quatPr.input1Quat
        fa_quatPr.input2QuatW.set(1)

        fa_quatEu = createNode("quatToEuler", n="%s_quatEu" % aimObj)
        fa_quatPr.outputQuat >> fa_quatEu.inputQuat
        aimObj.rotateOrder >> fa_quatEu.inputRotateOrder
        fa_quatEu.outputRotate >> aimObj.rotate


def addHelperJoint(AddJoint, ParentJoint, primaryAxis='x', size=1.0):
    """

    :param addJnt:
    :param parentJnt:
    :param prAxis:
    :param size:
    :return:
    """
    AddJoint_ = AddJoint.replace('_jnt', '')
    if not objExists("BranchSystem"):
        BranchSystem = createNode("transform", n="BranchSystem")
        BranchController = createNode("transform", n="BranchController", p=BranchSystem)

    SlideAxis = AxisList = ['+x', '+y', '+z', '-x', '-y', '-z']
    NumberDict = {0:'A', 1:'B', 2:'C', 3:'D'}
    [SlideAxis.remove(axis) for axis in AxisList if primaryAxis in axis]
    for i, axis in enumerate(SlideAxis):
        root = createNode("transform", n="%s_%s_root" % (AddJoint_, NumberDict[i]))
        delete(parentConstraint(AddJoint, root))
        parent(root, "BranchController")
        father = createNode("transform", n="%s_%s_father" % (AddJoint_, NumberDict[i]), p=root)
        origin = createNode("transform", n="%s_%s_origin" % (AddJoint_, NumberDict[i]), p=root)

        ctrlSdk2Zero = createNode("transform", n="%s_%s_base_zero" % (AddJoint_, NumberDict[i]))
        ctrlSdk2 = createNode("transform", n="%s_%s_base_sdk" % (AddJoint_, NumberDict[i]), p=ctrlSdk2Zero)
        ctrlZero = createNode("transform", n="%s_%s_zero" % (AddJoint_, NumberDict[i]), p=ctrlSdk2)

        ctrlSdk = createNode("transform", n="%s_%s_sdk" % (AddJoint_, NumberDict[i]), p=ctrlZero)
        Ctrl = PyNode(ctrl.Icon().create_icon("Sphere",icon_name="%s_%s_ctrl" % (AddJoint_, NumberDict[i]),
                                              icon_color=17,scale=(size * 0.13, size * 0.13, size * 0.13))[0])
        # Ctrl = PyNode(ctrl.Icon().create_icon("%s_%s_ctrl" % (AddJoint_, NumberDict[i]), 'C00_sphere', size * 0.13, 17, [0, 0, 0]))
        addAttr(Ctrl, ln="follow", at="double", min=0, max=10, dv=5)
        Ctrl.follow.set(e=True, k=True)
        jnt = createNode("joint", n="%s_%s_Helper" % (AddJoint_, NumberDict[i]), p=Ctrl)
        parent(Ctrl, ctrlSdk)

        delete(parentConstraint(origin, ctrlSdk2Zero))
        parent(ctrlSdk2Zero, origin)

        if '+' in axis:
            setAttr("%s.t%s" % (ctrlZero, axis[-1]), size)
        else:
            setAttr("%s.t%s" % (ctrlZero, axis[-1]), size * -1)

        parent(jnt, w=True)
        prc = parentConstraint(Ctrl, jnt)
        rename(prc, "%s_prc" % jnt)

        # root cnt
        OneToOneCreateParentMatrix(AddJoint, root, T=True, R=True, S=True)

        # father cnt
        OneToOneCreateParentMatrix(ParentJoint, father, T=False, R=True, S=False)

        multDiv = createNode("multDoubleLinear", n="%s_offset_mult" % Ctrl)
        Ctrl.follow >> multDiv.input1
        multDiv.input2.set(0.1)

        offset_plus = createNode("plusMinusAverage", n="%s_offset_plus" % Ctrl)
        offset_plus.operation.set(2)
        offset_plus.input1D[0].set(1)
        multDiv.output >> offset_plus.input1D[1]

        orig = orientConstraint(father, root, origin, mo=True)
        rename(orig, "%s_orc"%origin)
        orig.interpType.set(2)
        multDiv.output >> orig.w0
        offset_plus.output1D >> orig.w1

        parent(jnt, AddJoint)
        sc = scaleConstraint(Ctrl, jnt)
        rename(orig, "%s_sc" % jnt)
        if objExists("noTransform"):
            parent("BranchSystem", "noTransform")


def TimeLineHelper():
    AddJntList = ['L_LegA_01_jnt',
                  'L_LegB_01_jnt',
                  'L_Foot_jnt',
                  'L_Toe_jnt',
                  'L_ArmA_01_jnt',
                  'L_ArmB_01_jnt',
                  'L_Hand_jnt',
                  'L_Index01_jnt',
                  'L_Middle01_jnt',
                  'L_Ring01_jnt',
                  'L_Pinky01_jnt',
                  'L_Thumb02_jnt',
                  'Neck01_jnt',
                  'Head01_jnt',
                  'Chest_jnt']
    for jnt in AddJntList:
        addJnt = PyNode(jnt)
        size = calculateTL_size() / 35.0
        if -0.01 < addJnt.getTranslation(space="world")[0] < 0.01 or "Clavicle" in addJnt.name():
            size = calculateTL_size() / 20.0
        if addJnt in listRelatives('*_Hand_jnt', ad=1, type='joint'):
            size = calculateTL_size() / 30.0
        if "hip" in addJnt.name() or "Chest" in addJnt.name() or "Foot" in addJnt.name() or "Head" in addJnt.name() or "Toe" in addJnt.name():
            size = calculateTL_size() / 30.0
            primaryAxis = "y"
        else:
            primaryAxis = "x"

        addHelperJoint(addJnt, addJnt.getParent(), primaryAxis=primaryAxis, size=size)


def calculateTL_size():
    size = 15
    if objExists("Head_ctrl") and objExists("Root_ctrl"):
        topPos = PyNode('Head_ctrl').getTranslation(space='world')
        btnPos = PyNode('Root_ctrl').getTranslation(space='world')
        size = (topPos - btnPos).length()
    return size


def mirrorHelperJoint():
    AddJntList = ['L_LegA_01_jnt',
                  'L_LegB_01_jnt',
                  'L_Foot_jnt',
                  'L_ArmA_01_jnt',
                  'L_ArmB_01_jnt',
                  'L_Hand_jnt',
                  'L_Index01_jnt',
                  'L_Middle01_jnt',
                  'L_Ring01_jnt',
                  'L_Pinky01_jnt',
                  'L_Thumb02_jnt']
    for jnt in AddJntList:
        helperName = jnt.replace('_jnt', '')
        otherSideJnt = PyNode(jnt.replace('L_', 'R_'))
        rootGrpList = ls("%s_*_root" % helperName)
        tempGrp = createNode("transform", n="mirrorTemp")
        parent(rootGrpList, tempGrp)

        dupTemp = duplicate(tempGrp, n="TempMirror")[0]
        dupTemp.sx.set(-1)

        parent(rootGrpList, "BranchController")
        rSideRootList = []
        for c in listRelatives(dupTemp, ad=1):
            if "Constraint" in c:
                delete(c)
            obj = rename(c, c.replace("L_", "R_"))
            if "root" in obj.name():
                rSideRootList.append(obj)

        for root in rSideRootList:
            OneToOneCreateParentMatrix(otherSideJnt, root, T=True, R=True, S=True)
            if objExists(root.replace('root', 'father')):
                ctrl = PyNode(root.replace('root', 'ctrl'))
                father = PyNode(root.replace('root', 'father'))
                origin = PyNode(root.replace('root', 'origin'))
                jnt = createNode("joint", n=root.replace('root', 'Helper'))
                # father cnt
                OneToOneCreateParentMatrix(otherSideJnt.getParent(), father, T=False, R=True, S=False)

                multDiv = createNode("multDoubleLinear", n="%s_offset_mult" % ctrl)
                ctrl.follow >> multDiv.input1
                multDiv.input2.set(0.1)

                offset_plus = createNode("plusMinusAverage", n="%s_offset_plus" % ctrl)
                offset_plus.operation.set(2)
                offset_plus.input1D[0].set(1)
                multDiv.output >> offset_plus.input1D[1]

                orig = orientConstraint(father, root, origin, mo=True)
                orig.interpType.set(2)
                multDiv.output >> orig.w0
                offset_plus.output1D >> orig.w1

                parent(jnt, otherSideJnt)
                delete(parentConstraint(ctrl, jnt))
                makeIdentity(jnt, apply=True, r=True)
                prc = parentConstraint(ctrl, jnt)
                sc = scaleConstraint(ctrl, jnt)

                rename(orig, "%s_orc" % origin)
                rename(prc, "%s_prc" % jnt)
                rename(sc, "%s_slc" % jnt)

        mirrorGrp = "MirrorBranchCotroller"
        if not objExists("MirrorBranchCotroller"):
            mirrorGrp = duplicate(tempGrp, n="MirrorBranchCotroller")[0]
            mirrorGrp.sx.set(-1)

        parent(rSideRootList, mirrorGrp)
        delete([tempGrp, dupTemp])

        if objExists("BranchController"):
            parent(mirrorGrp, "BranchController")

