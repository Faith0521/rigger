import maya.cmds as mc

def repointBodyCtrl():
    keyObj = ['Body_ctrl_zero','Body_ctrl','hip_jnt','torsoFK_base','Visibility_zero','C_Torso_poseGrp']
    for obj in keyObj:
        if not mc.objExists(obj):
            return

    # repoint
    mc.parent('torsoFK_base', w=True)
    mc.parent('Visibility_zero', w=True)
    mc.parent('C_Torso_poseGrp', w=True)

    mc.delete(mc.pointConstraint('hip_jnt', 'Body_ctrl_zero'))
    mc.parent('torsoFK_base', 'Body_ctrl')
    mc.parent('Visibility_zero', 'Body_ctrl')
    mc.parent('C_Torso_poseGrp', 'Body_ctrl')

