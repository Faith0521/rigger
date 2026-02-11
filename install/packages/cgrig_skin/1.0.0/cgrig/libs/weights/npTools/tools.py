# -*- coding: utf-8 -*-
# coding:utf-8
from .api_core import *
from .solve_core import *


def tool_face_point_weight(max_influence=4):
    polygon = cmds.ls(sl=1, o=1)[0]
    kwargs = get_distance_data(polygon)
    weights = run(solve_distance_rbf_weight, max_influence=max_influence, **kwargs)
    set_weights(polygon, weights)
