import maya.cmds as mc

def redoArmTwist():
    for i in ["L", "R"]:
        oldp = "%s_Arm01_NonRoll_grp" % i
        old = "%s_Arm01_nonRoll_ikHandle" % i
        olds = "%s_Arm01_nonRoll_start" % i
        olde = "%s_Arm01_nonRoll_end" % i
        old02 = '%s_Arm02_drv' % i
        oldCon = '%s_ArmA_twist_grp_parentConstraint1' % i
        oldTg = '%s_ArmA_twist_grp' % i
        oldFK = '%s_ArmFk01_ctrl' % i
        oldCL = '%s_Clavicle_ctrl' % i

        mc.delete(old)
        oldra = mc.getAttr(olds + ".rz")
        oldjir = mc.getAttr(olds + ".jointOrientZ")
        mc.setAttr(olds + ".jointOrientZ", oldjir + oldra)
        mc.setAttr(olds + ".rz", 0)
        ikh = mc.ikHandle(sj=olds, ee=olde, sol='ikRPsolver', name="%s" % old)[0]
        mc.parent(ikh, oldp)
        mc.pointConstraint(old02, ikh)

        mc.delete(oldCon)
        offsetV = mc.getAttr(oldFK + '.rz')
        if i == 'R':
            offsetV *= -1

        mc.setAttr(oldTg + '.rz', offsetV)
        mc.parentConstraint(oldCL, oldTg, mo=1)

        mc.setAttr(old + '.poleVectorX', 0)
        mc.setAttr(old + '.poleVectorY', 0)
        mc.setAttr(old + '.poleVectorZ', 0)