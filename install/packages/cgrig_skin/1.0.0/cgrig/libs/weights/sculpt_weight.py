# -*- coding: utf-8 -*-
# coding:utf-8
from maya import cmds
from .api_lib import sculpt_api
from .common import *


class LSculptJob(object):

    def __init__(self):
        self.attr_name = None

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self):
        sculpt_api.part_sdr_solve()
        cmds.scriptJob(attributeChange=[self.attr_name, self], runOnce=True)

    def add_job(self):
        self.del_job()
        skin_polygon = get_selected_geometry(Shape.mesh)
        if skin_polygon is None:
            return
        skin_cluster = get_skin_cluster(skin_polygon)
        if skin_cluster is None:
            return
        influences = cmds.skinCluster(skin_cluster, q=1, influence=1)
        unlock_joints = [joint for joint in influences if not cmds.getAttr(joint+'.liw')]
        unlock_joint_ids = [influences.index(joint) for joint in unlock_joints]
        if len(unlock_joint_ids) == 0:
            return cmds.warning("please unlock some joints")
        group = cmds.group(em=1, n="LushSplitSculptGroup")
        sculpt_polygon = cmds.duplicate(skin_polygon, )[0]
        for shape in cmds.listRelatives(sculpt_polygon, s=1):
            if cmds.getAttr(shape+'.io'):
                cmds.delete(shape)
        cmds.parent(sculpt_polygon, group)
        name = "LushSplitSculpt_"+get_short_name(skin_polygon)
        sculpt_polygon = cmds.rename(sculpt_polygon, name)

        for shape in cmds.listRelatives(sculpt_polygon, s=1):
            cmds.setAttr(shape+'.overrideEnabled', True)
            cmds.setAttr(shape+'.overrideColor', 13)
        panels = cmds.getPanel(all=True)
        for panel in panels:
            if cmds.modelPanel(panel, ex=1):
                cmds.modelEditor(panel, e=1, wireframeOnShaded=True)
        cmds.setAttr(skin_polygon+'.v', 0)
        cmds.select(cl=1)
        sculpt_api.part_sdr_init(skin_polygon, skin_cluster, sculpt_polygon, unlock_joint_ids)
        self.attr_name = cmds.listRelatives(sculpt_polygon, s=1)[0] + ".outMesh"

        cmds.scriptJob(attributeChange=[self.attr_name, self], runOnce=True)

    def del_job(self):
        for job in cmds.scriptJob(listJobs=True):
            if repr(self) in job:
                cmds.scriptJob(kill=int(job.split(":")[0]))
        if not cmds.objExists("|LushSplitSculptGroup"):
            return
        group = "|LushSplitSculptGroup"
        for child in cmds.listRelatives(group):
            name = child.split(":")[-1].split("|")[-1]
            if not name.startswith("LushSplitSculpt_"):
                continue
            polygon_name = name[len("LushSplitSculpt_"):]
            if is_shape(polygon_name, Shape.mesh):
                cmds.setAttr(polygon_name+'.v', True)
        cmds.delete(group)


def auto_apply():
    if not cmds.objExists("|LushSplitSculptGroup"):
        LSculptJob().add_job()
    else:
        LSculptJob().del_job()

