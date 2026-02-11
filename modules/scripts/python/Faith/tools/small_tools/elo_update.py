import maya.cmds as cmds

def main():

    if not cmds.objExists("move_origin_ctrl"):
        if cmds.objExists("Master_ctrl_PH"):
            cmds.group("Master_ctrl_PH", name="move_origin_ctrl")

    # IK脚控制器对称补丁
    if cmds.objExists("R_LegPoleVectorFollow_FootAim_aimConstraint1") or cmds.objExists("R_LegPoleVec01_ctrl_offset_parentConstraint1"):
        cmds.delete("R_LegPoleVectorFollow_FootAim_aimConstraint1")
        cmds.delete("R_LegPoleVec01_ctrl_offset_parentConstraint1")
        cmds.parent("R_Heel_pivot_zero", w=1)
        cmds.parent("R_Ankle_loc", w=1)
        cmds.setAttr("R_LegIk01_ctrl_zero.rotateZ", 180)
        cmds.setAttr("R_LegIk01_ctrl_zero.scaleY", -1)
        cmds.aimConstraint("R_LegIk01_ctrl", "R_LegPoleVectorFollow_FootAim", mo=0, aimVector=[1, 0, 0],
                           upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[-1, 0, 0],
                           worldUpObject="R_LegIk01_ctrl")
        cmds.parentConstraint(["R_LegPoleVectorFollow_Static", "R_LegPoleVectorFollow_Foot"], "R_LegPoleVec01_ctrl_offset",
                              mo=1)
        cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_StaticW0',
                               cd='R_LegPoleVec01_ctrl.followFoot', driverValue=0, value=1)
        cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_StaticW0',
                               cd='R_LegPoleVec01_ctrl.followFoot', driverValue=1, value=0)
        cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_FootW1',
                               cd='R_LegPoleVec01_ctrl.followFoot', driverValue=0, value=0)
        cmds.setDrivenKeyframe('R_LegPoleVec01_ctrl_offset_parentConstraint1.R_LegPoleVectorFollow_FootW1',
                               cd='R_LegPoleVec01_ctrl.followFoot', driverValue=1, value=1)
        cmds.parent(["R_Heel_pivot_zero", "R_Ankle_loc"], "R_LegIk01_ctrl")
        cmds.select(cl=1)

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
    if not cmds.objExists("neck_mid_grp"):
        ma_file = r"R:\\TeamCode\\OF3D_RIG\\modules\\scripts\\python\\Faith\\tools\\small_tools\\neck_midCtrl_rig.ma"
        cmds.file(ma_file, i=1, ns=':')

        cmds.matchTransform('NeckFK_Base_jnt_zero', 'Neck01_anim')

        cmds.matchTransform('NeckFK_Base_jnt2', 'Neck04_end')

        neckFK_ikh = cmds.ikHandle(sj='NeckFK_Base_jnt1', ee='NeckFK_Base_jnt2', solver='ikSCsolver')[0]

        cmds.setAttr(neckFK_ikh + ".visibility", 0)

        neckFK_ikh_grp = cmds.createNode('transform', n='neckFK_ikh_grp')

        cmds.parent(neckFK_ikh, neckFK_ikh_grp)

        neckFK_ikh = cmds.rename(neckFK_ikh, 'neckFK_ikh')

        NeckMid_ctrl_grp_Constraint = cmds.parentConstraint(['NeckFK_Base_jnt1', 'NeckFK_Base_jnt2'], 'NeckMid_ctrl_grp',
                                                            mo=0)
        cmds.delete(NeckMid_ctrl_grp_Constraint)

        cmds.parentConstraint('NeckFK_Base_jnt1', 'NeckMid_ctrl_grp', mo=1)

        cmds.pointConstraint('Head01_anim', neckFK_ikh, mo=1)

        cmds.skinCluster('NeckCurve_skinCluster', edit=True, ai='NeckMid_bind', lockWeights=True)

        cmds.skinPercent('NeckCurve_skinCluster', 'Neck_curve.cv[0:1]', tv=('NeckStart_bind', 1))

        cmds.skinPercent('NeckCurve_skinCluster', 'Neck_curve.cv[2]',
                         tv=[('NeckEnd_bind', 0.022), ('NeckMid_bind', 0.619), ('NeckStart_bind', 0.359)])

        cmds.skinPercent('NeckCurve_skinCluster', 'Neck_curve.cv[3]',
                         tv=[('NeckEnd_bind', 0.316), ('NeckMid_bind', 0.634), ('NeckStart_bind', 0.05)])

        cmds.skinPercent('NeckCurve_skinCluster', 'Neck_curve.cv[4:5]', tv=('NeckEnd_bind', 1))

        neck_mid_grp = cmds.createNode("transform", name="neck_mid_grp", p="Neck_grp")
        cmds.parent(["NeckMid_ctrl_grp", "NeckFK_Base_jnt_zero", "neckFK_ikh_grp"], neck_mid_grp)

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    # 肩膀 添加followWorld属性补丁
    if (not cmds.objExists("L_Clavicle_ctrl.followWorld")) or (not cmds.objExists("R_Clavicle_ctrl.followWorld")):
        cmds.addAttr("L_Clavicle_ctrl", longName='followWorld', attributeType='float', keyable=True, defaultValue=0,
                     minValue=0, maxValue=1)
        cmds.addAttr("R_Clavicle_ctrl", longName='followWorld', attributeType='float', keyable=True, defaultValue=0,
                     minValue=0, maxValue=1)
        # LLLLLLL
        cmds.orientConstraint(["Chest_jnt", "Root_ctrl"], "L_Clavicle_grp", mo=1)
        cmds.setDrivenKeyframe('L_Clavicle_grp_orientConstraint1.Chest_jntW0', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=0, value=1)
        cmds.setDrivenKeyframe('L_Clavicle_grp_orientConstraint1.Chest_jntW0', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=1, value=0)

        cmds.setDrivenKeyframe('L_Clavicle_grp_orientConstraint1.Root_ctrlW1', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=0, value=0)
        cmds.setDrivenKeyframe('L_Clavicle_grp_orientConstraint1.Root_ctrlW1', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=1, value=1)

        cmds.orientConstraint(["Chest_jnt", "Root_ctrl"], "L_Clavicle_zero", mo=1)
        cmds.setDrivenKeyframe('L_Clavicle_zero_orientConstraint1.Chest_jntW0', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=0, value=1)
        cmds.setDrivenKeyframe('L_Clavicle_zero_orientConstraint1.Chest_jntW0', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=1, value=0)

        cmds.setDrivenKeyframe('L_Clavicle_zero_orientConstraint1.Root_ctrlW1', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=0, value=0)
        cmds.setDrivenKeyframe('L_Clavicle_zero_orientConstraint1.Root_ctrlW1', cd='L_Clavicle_ctrl.followWorld',
                               driverValue=1, value=1)
        # RRRRRRR
        cmds.orientConstraint(["Chest_jnt", "Root_ctrl"], "R_Clavicle_grp", mo=1)
        cmds.setDrivenKeyframe('R_Clavicle_grp_orientConstraint1.Chest_jntW0', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=0, value=1)
        cmds.setDrivenKeyframe('R_Clavicle_grp_orientConstraint1.Chest_jntW0', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=1, value=0)

        cmds.setDrivenKeyframe('R_Clavicle_grp_orientConstraint1.Root_ctrlW1', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=0, value=0)
        cmds.setDrivenKeyframe('R_Clavicle_grp_orientConstraint1.Root_ctrlW1', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=1, value=1)

        cmds.orientConstraint(["Chest_jnt", "Root_ctrl"], "R_Clavicle_zero", mo=1)
        cmds.setDrivenKeyframe('R_Clavicle_zero_orientConstraint1.Chest_jntW0', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=0, value=1)
        cmds.setDrivenKeyframe('R_Clavicle_zero_orientConstraint1.Chest_jntW0', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=1, value=0)

        cmds.setDrivenKeyframe('R_Clavicle_zero_orientConstraint1.Root_ctrlW1', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=0, value=0)
        cmds.setDrivenKeyframe('R_Clavicle_zero_orientConstraint1.Root_ctrlW1', cd='R_Clavicle_ctrl.followWorld',
                               driverValue=1, value=1)

        cmds.setAttr("L_Clavicle_ctrl.followWorld", 0)
        cmds.setAttr("R_Clavicle_ctrl.followWorld", 0)

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    # 一些基本规范整理：移动大组不要双倍位移、模型显示模式连接、默认不显示躯干FK控制器 。
    cmds.setAttr('noTransform.inheritsTransform', 0)
    if not cmds.objExists('Visibility.body_FK_VIS'):
        cmds.addAttr('Visibility', longName='body_FK_VIS', attributeType='bool', keyable=False)
        cmds.setAttr('Visibility.body_FK_VIS', channelBox=1)
        cmds.connectAttr('Visibility.body_FK_VIS', 'TorsoFk00_ctrl_zero.visibility')
