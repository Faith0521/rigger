# coding:utf-8
from maya import cmds
import common
import sculpt_weight
reload(common)
reload(sculpt_weight)
import weight_pickle
reload(weight_pickle)
import weight_tool
reload(weight_tool)


def test_sculpt_weight():
    if cmds.objExists("LushSplitSculptGroup"):
        sculpt_weight.auto_apply()
    else:
        cmds.file("D:/work/weights/sculpt_weight.ma", o=1, f=1)
        cmds.select("pCube1")
        sculpt_weight.auto_apply()


def test_weight_pickle():
    cmds.file("D:/work/weights/weight_pickle.ma", o=1, f=1)
    cmds.select("pCube1")
    weight_pickle.save_weight("D:/work/weights/weight_pickle.pk")
    cmds.select("pCube2")
    weight_pickle.load_weight("D:/work/weights/weight_pickle.pk")


def test_copy_weights():
    cmds.file("D:/work/weights/weight_pickle.ma", o=1, f=1)
    cmds.select("pCube1", "pCube2")
    weight_tool.copy_weights()


def test_re_skin():
    cmds.file("D:/work/weights/re_skin.ma", o=1, f=1)
    cmds.select("joint1")
    weight_tool.re_skin()


def test_limit_weights():
    cmds.file("D:/work/weights/limit_influence.ma", o=1, f=1)
    cmds.select("pSphere1")
    weight_tool.limit_max_influence(max_influence=3)


def test_lock_influence_smooth():
    cmds.file("D:/work/weights/limit_influence.ma", o=1, f=1)
    cmds.select("pSphere1.vtx[*]")
    weight_tool.lock_influence_smooth()


def test_copy_unlock_skin_polygon():
    cmds.file("D:/work/weights/copy_unlock.ma", o=1, f=1)
    cmds.select("pSphere1")
    weight_tool.copy_unlock_skin_polygon()


def test_create_vx():
    cmds.file("D:/work/weights/copy_unlock.ma", o=1, f=1)
    cmds.select("joint3", "joint6")
    weight_tool.create_vx()


def test_paint_eye():
    cmds.file("D:/work/weights/paint_eye.ma", o=1, f=1)
    cmds.select("pTorus1")
    weight_tool.paint_eye()


def test_copy_pase():
    cmds.file("D:/work/weights/copy_pase.ma", o=1, f=1)
    cmds.select("src")
    weight_tool.copy_joint_weight()
    cmds.select("dst")
    weight_tool.paste_joint_weight()


def doit():
    # test_sculpt_weight()
    # test_weight_pickle()
    # test_copy_weights()
    # test_re_skin()
    # test_limit_weights()
    # test_copy_unlock_skin_polygon()
    # test_create_vx()
    # test_paint_eye()
    test_re_skin()