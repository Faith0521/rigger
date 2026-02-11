import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


def get_skin_cluster(geometry):
    """get skinCluster node"""
    history = cmds.listHistory(geometry)
    skin_clusters = cmds.ls(history, type='skinCluster')
    if not skin_clusters:
        raise RuntimeError("No skinCluster found for {}".format(geometry))
    return skin_clusters[0]


def is_reference(node):
    """
    Parameters:
        node (str):

    Returns:
        bool:  t/f
    """
    return cmds.referenceQuery(node, isNodeReferenced=True)


def add_move_origin_grp():
    if cmds.objExists('move_origin_ctrl'):
        return
    if not cmds.objExists('Root_grp'):
        return
    cmds.createNode('transform', n="move_origin_ctrl", parent="Root_grp")


def add_follow_worldSpace():
    if cmds.objExists('root_base'):
        return

    # sels = cmds.ls(sl=1)
    sels = ["L_Clavicle_ctrl", "R_Clavicle_ctrl"]

    if sels:

        if not cmds.objExists('root_base'):
            cmds.createNode('transform', n="root_base", parent="Root_ctrl")

        if not cmds.objExists('world_space_grp'):
            world_space_grp = cmds.createNode('transform', n="world_space_grp", parent="root_base")

        if not cmds.objExists('chest_base'):
            cmds.createNode('transform', n="chest_base", parent="Chest_jnt")

        if not cmds.objExists('chest_space_grp'):
            chest_space_grp = cmds.createNode('transform', n="chest_space_grp", parent="chest_base")

        for i in sels:

            Order = int(cmds.getAttr("{}.rotateOrder".format(i)))

            chest_worldspace_zero = cmds.createNode('transform', name="chest_space_{}_zero_worldspace".format(i))
            world_worldspace_zero = cmds.createNode('transform', name="world_space_{}_zero_worldspace".format(i))

            chest_worldspace = cmds.createNode('transform', name="chest_space_{}_worldspace".format(i))
            world_worldspace = cmds.createNode('transform', name="world_space_{}_worldspace".format(i))

            cmds.setAttr("{}.rotateOrder".format(chest_worldspace_zero), Order)
            cmds.setAttr("{}.rotateOrder".format(world_worldspace_zero), Order)

            cmds.setAttr("{}.rotateOrder".format(chest_worldspace), Order)
            cmds.setAttr("{}.rotateOrder".format(world_worldspace), Order)

            cmds.delete(cmds.parentConstraint(i, chest_worldspace_zero))
            cmds.delete(cmds.parentConstraint(i, world_worldspace_zero))
            cmds.delete(cmds.scaleConstraint(i, chest_worldspace_zero))
            cmds.delete(cmds.scaleConstraint(i, world_worldspace_zero))

            cmds.delete(cmds.parentConstraint(i.replace("ctrl", "grp"), chest_worldspace))
            cmds.delete(cmds.parentConstraint(i.replace("ctrl", "grp"), world_worldspace))
            cmds.delete(cmds.scaleConstraint(i.replace("ctrl", "grp"), chest_worldspace))
            cmds.delete(cmds.scaleConstraint(i.replace("ctrl", "grp"), world_worldspace))

            if cmds.objExists(i.replace("ctrl", "zero")):
                Constraint = \
                cmds.orientConstraint(chest_worldspace_zero, world_worldspace_zero, i.replace("ctrl", "zero"), mo=1)[0]

            Constraint2 = cmds.orientConstraint(chest_worldspace, world_worldspace, i.replace("ctrl", "grp"), mo=1)[0]

            attrs = ["followSet", "followWorld"]
            ctrl_attrs = cmds.listAttr(i)

            if attrs[0] not in ctrl_attrs:
                cmds.addAttr(i, longName=attrs[0], niceName='________________', attributeType='enum',
                             enumName='{}:'.format(attrs[0].split("Set")[0]), keyable=True)
                cmds.setAttr('{}.{}'.format(i, attrs[0]), keyable=False, channelBox=True, lock=True)
            if attrs[1] not in ctrl_attrs:
                cmds.addAttr(i, longName=attrs[1], attributeType='double', defaultValue=1,
                             minValue=0, maxValue=1,
                             keyable=True)

            cmds.connectAttr("{}.{}".format(i, attrs[1]), "{}.{}W1".format(Constraint, world_worldspace_zero), f=True)
            cmds.connectAttr("{}.{}".format(i, attrs[1]), "{}.{}W1".format(Constraint2, world_worldspace), f=True)

            rev = cmds.shadingNode('reverse', asUtility=1, name="{}_cons_rev".format(Constraint2))

            cmds.connectAttr("{}.{}W1".format(Constraint, world_worldspace_zero), '{}.inputX'.format(rev), f=1)
            cmds.connectAttr("{}.{}W1".format(Constraint2, world_worldspace), '{}.inputY'.format(rev), f=1)

            cmds.connectAttr('{}.outputX'.format(rev), "{}.{}W0".format(Constraint, chest_worldspace_zero), f=1)

            cmds.connectAttr('{}.outputY'.format(rev), "{}.{}W0".format(Constraint2, chest_worldspace), f=1)

            # 整理
            cmds.parent(world_worldspace_zero, world_worldspace, "world_space_grp")
            cmds.parent(chest_worldspace_zero, chest_worldspace, "chest_space_grp")

        om.MGlobal.displayInfo("follow world succeeded !")

    else:
        om.MGlobal.displayError(u"Please select what needs to be added to the controller!")


def mirror_hand_ikctrl():
    if cmds.objExists('R_Hand_drvloc_ofs'):
        return

    R_ArmIk01_ctrl_offset = "R_ArmIk01_ctrl_offset"

    grp = cmds.createNode('transform', name="Temp_ik_grp")

    cmds.select('R_ArmIk01_drv_distance_end', 'R_Hand_ikh', 'R_Hand_loc', r=1)
    ik_hand = cmds.group(n="R_Hand_drvloc_ofs")

    cmds.select(R_ArmIk01_ctrl_offset, r=1)

    cons = cmds.parentConstraint(R_ArmIk01_ctrl_offset, weightAliasList=True, targetList=True)[0]

    obj_name = cmds.parentConstraint(cons, query=True, targetList=1)

    cmds.disconnectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_HeadW0.output',
                        'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_HeadW0')
    cmds.disconnectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_BodyW1.output',
                        'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_BodyW1')
    cmds.disconnectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_WeaponW2.output',
                        'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_WeaponW2')
    cmds.disconnectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_WorldW3.output',
                        'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_WorldW3')

    cmds.delete(cons)

    cmds.parent(ik_hand, grp)

    cmds.setAttr("{}.rotateY".format(R_ArmIk01_ctrl_offset), 180)
    cmds.setAttr("{}.scaleZ".format(R_ArmIk01_ctrl_offset), -1)

    value = cmds.getAttr("R_ArmIk01_ctrl.jointOrientZ")
    cmds.setAttr("R_ArmIk01_ctrl.jointOrientZ", value * -1)

    con = cmds.parentConstraint(obj_name, R_ArmIk01_ctrl_offset, mo=True)[0]
    if con != cons:
        cmds.rename(con, cons)

    cmds.connectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_HeadW0.output',
                     'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_HeadW0', f=1)
    cmds.connectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_BodyW1.output',
                     'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_BodyW1', f=1)
    cmds.connectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_WeaponW2.output',
                     'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_WeaponW2', f=1)
    cmds.connectAttr('R_ArmIk01_ctrl_offset_parentConstraint1_R_ArmIKFollow_WorldW3.output',
                     'R_ArmIk01_ctrl_offset_parentConstraint1.R_ArmIKFollow_WorldW3', f=1)

    cmds.parent(ik_hand, "R_ArmIk01_ctrl")

    cmds.delete(grp)
    om.MGlobal.displayInfo(" mirror hand ik succeeded !")


def mirror_foot_ikctrl():
    if cmds.objExists('R_LegPoleVectorFollow_FootAim_eio_aimConstraint1'):
        return

    cmds.delete("R_LegPoleVectorFollow_FootAim_aimConstraint1")
    cmds.delete("R_LegPoleVec01_ctrl_offset_parentConstraint1")
    cmds.parent("R_Heel_pivot_zero", w=1)
    cmds.parent("R_Ankle_loc", w=1)
    cmds.setAttr("R_LegIk01_ctrl_zero.rotateZ", 180)
    cmds.setAttr("R_LegIk01_ctrl_zero.scaleY", -1)

    cmds.aimConstraint("R_LegIk01_ctrl", "R_LegPoleVectorFollow_FootAim", mo=0, aimVector=[1, 0, 0],
                       upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[-1, 0, 0],
                       worldUpObject="R_LegIk01_ctrl", n='R_LegPoleVectorFollow_FootAim_eio_aimConstraint1')

    Constraint = \
    cmds.parentConstraint(["R_LegPoleVectorFollow_Static", "R_LegPoleVectorFollow_Foot"], "R_LegPoleVec01_ctrl_offset",
                          mo=1)[0]
    cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_StaticW0',
                           cd='R_LegPoleVec01_ctrl.followFoot', driverValue=0, value=1)
    cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_StaticW0',
                           cd='R_LegPoleVec01_ctrl.followFoot', driverValue=1, value=0)

    rev = cmds.shadingNode('reverse', asUtility=1, name="{}_cons_rev".format(Constraint))

    cmds.connectAttr('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_StaticW0',
                     '{}.inputX'.format(rev), f=1)
    cmds.connectAttr('{}.outputX'.format(rev),
                     'R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_FootW1', f=1)

    cmds.parent(["R_Heel_pivot_zero", "R_Ankle_loc"], "R_LegIk01_ctrl")
    cmds.select(cl=1)

    om.MGlobal.displayInfo(" mirror foot ik succeeded !")


def mirror_ik_ctrl():
    mirror_hand_ikctrl()
    mirror_foot_ikctrl()


def create_midNeck_ctrl():
    if cmds.objExists('NeckMid_bind'):
        return

    joint = cmds.joint(n="NeckMid_bind")
    cmds.delete(cmds.parentConstraint("NeckStart_bind", "NeckEnd_bind", "NeckMid_bind"))

    ctrl = cmds.curve(d=1, p=[(-2, 0, -2), (-2, 0, 2), (2, 0, 2), (2, 0, -2), (-2, 0, -2)], k=[0, 1, 2, 3, 4],
                      name=joint.replace("bind", "ctrl"))

    shape = cmds.listRelatives(ctrl, s=1)[0]
    cmds.setAttr((shape + ".overrideEnabled"), 1)
    cmds.setAttr((shape + ".overrideColor"), 4)
    cmds.setAttr(ctrl + '.v', lock=True, keyable=False, channelBox=False)
    cmds.select(ctrl, r=1)
    cmds.DeleteHistory()
    drv = cmds.group(n=(ctrl + "_drv"))
    con = cmds.group(n=(ctrl + "_con"))
    ofs = cmds.group(n=(ctrl + "_zero"))

    cmds.delete(cmds.parentConstraint(joint, ofs))
    cmds.parent(joint, ctrl)
    cmds.parent(ofs, "NeckFk01_ctrl")

    skinCluster = get_skin_cluster("Neck_curve")

    cmds.skinCluster(skinCluster, edit=True, ai='NeckMid_bind', lockWeights=True)
    cmds.skinPercent(skinCluster, 'Neck_curve.cv[0:1]', tv=('NeckStart_bind', 1))
    cmds.skinPercent(skinCluster, 'Neck_curve.cv[2]',
                     tv=[('NeckEnd_bind', 0.022), ('NeckMid_bind', 0.619), ('NeckStart_bind', 0.359)])
    cmds.skinPercent(skinCluster, 'Neck_curve.cv[3]',
                     tv=[('NeckEnd_bind', 0.316), ('NeckMid_bind', 0.634), ('NeckStart_bind', 0.05)])
    cmds.skinPercent(skinCluster, 'Neck_curve.cv[4:5]', tv=('NeckEnd_bind', 1))

    cmds.pointConstraint("NeckStart_bind", "NeckEnd_bind", con, mo=1)

    for attr in ["sx", "sy", "sz", "v"]:
        cmds.setAttr('{}.{}'.format(ctrl, attr), lock=True, keyable=False, channelBox=False)

    cmds.setAttr('{}.v'.format(joint), 0)

    om.MGlobal.displayInfo("neckMid_bind succeeded !")


def vis_fk_ctrls():
    if cmds.objExists('Visibility.Body_FK_VIS'):
        return

    visCtrl = "Visibility"
    body_ctrl_vis_attr = "Body_FK_VIS"
    body_fk_ctrl = "TorsoFk0*_ctrl"

    attrs = ["extraRigSet", body_ctrl_vis_attr]
    ctrl_attrs = cmds.listAttr(visCtrl)

    if attrs[0] not in ctrl_attrs:
        cmds.addAttr(visCtrl, longName=attrs[0], niceName='________________', attributeType='enum',
                     enumName='{}:'.format(attrs[0].split("Set")[0]), keyable=True)
        cmds.setAttr('{}.{}'.format(visCtrl, attrs[0]), keyable=False, channelBox=True, lock=True)

    if attrs[1] not in ctrl_attrs:
        cmds.addAttr(visCtrl, longName=attrs[1], attributeType='long', defaultValue=0,
                     minValue=0, maxValue=1,
                     keyable=True)
        cmds.setAttr('{}.{}'.format(visCtrl, attrs[1]), keyable=False, channelBox=True)

    cmds.select(body_fk_ctrl, r=1)
    fk_ctrls = cmds.ls(sl=True)

    for ctrl in fk_ctrls:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr("{}.{}".format(visCtrl, body_ctrl_vis_attr), "{}.visibility".format(shape))


def organize_files():
    if cmds.objExists("Root_ctrl"):
        add_move_origin_grp()
        create_midNeck_ctrl()
        mirror_ik_ctrl()
        add_follow_worldSpace()
        vis_fk_ctrls()
        cmds.select(cl=1)
        om.MGlobal.displayInfo(u"organize files succeeded ! 场景整理成功")
