# -*- coding: utf-8 -*-
__path__ = __import__('pkgutil').extend_path(__path__, __name__)


# Set rot axis based on strings
ROT_AXIS_DICT = {"+x": (0.0, -90.0, 90.0),
                 "-x": (0.0, 90.0, 90.0),
                 "+y": (0.0, 0.0, 0.0),
                 "-y": (0.0, 180.0, 0.0),
                 "+z": (90.0, 0.0, 0.0),
                 "-z": (-90.0, 0.0, 0.0)}

# Set rot up axis based on lists
X_UP = 0
X_DOWN = 1
Y_UP = 2
Y_DOWN = 3
Z_UP = 4
Z_DOWN = 5

NEW_CONTROL = "newControl"
CONTROLS_GRP_SUFFIX = "controls_grp"
CGRIG_TRANSLATE_TRACK_ATTR = "cgrigTranslateTrack"
CGRIG_TRANSLATE_DEFAULT_ATTR = "cgrigTranslateDefault"
CGRIG_ROTATE_TRACK_ATTR = "cgrigRotateTrack"
CGRIG_ROTATE_DEFAULT_ATTR = "cgrigRotateDefault"
CGRIG_SCALE_TRACK_ATTR = "cgrigScaleTrack"
CGRIG_SCALE_DEFAULT_ATTR = "cgrigScaleDefault"
CGRIG_COLOR_TRACK_ATTR = "cgrigColorTrack"
CGRIG_COLOR_DEFAULT_ATTR = "cgrigColorDefault"
CGRIG_SHAPE_TRACK_ATTR = "cgrigShapeTrack"
CGRIG_SHAPE_DEFAULT_ATTR = "cgrigShapeDefault"
XYZ_LIST = ["x", "y", "z"]
RGB_LIST = ["r", "g", "b"]
CONTROL_BUILD_TYPE_LIST = ["Joint, Shape Parent Ctrl", "Match Selection Only", "Constrain Obj, Cnstn Ctrl",
                           "Constrain Obj, Parent Ctrl", "Constrain Obj, Float Ctrl"]

CGRIG_CONTROLTRACK_VECTOR_LIST = [CGRIG_TRANSLATE_TRACK_ATTR, CGRIG_TRANSLATE_DEFAULT_ATTR,
                                CGRIG_ROTATE_TRACK_ATTR, CGRIG_ROTATE_DEFAULT_ATTR,
                                CGRIG_SCALE_TRACK_ATTR, CGRIG_SCALE_DEFAULT_ATTR]
CGRIG_CONTROLTRACK_RGB_LIST = [CGRIG_COLOR_TRACK_ATTR, CGRIG_COLOR_DEFAULT_ATTR]
CGRIG_CONTROLTRACK_STRING_LIST = [CGRIG_SHAPE_TRACK_ATTR, CGRIG_SHAPE_DEFAULT_ATTR]

CGRIG_TEMPBREAK_NETWORK = "breakTrack_network"
CGRIG_TEMPBREAK_CTRL_ATTR = "cgrig_ctrl_tempBreakTrack"
CGRIG_TEMPBREAK_GRP_ATTR = "cgrig_grp_tempBreakTrack"
CGRIG_TEMPBREAK_MASTER_ATTR = "cgrig_mstr_tempBreakTrack"


# ---------------------------
# ROTATE CONTROLS
# ---------------------------

ROTATE_UP_DICT = {Y_UP: [0, 0, 0],
                  Y_DOWN: [0, 180, 0],
                  X_UP: [0, -90, 90],
                  X_DOWN: [0, 90, 90],
                  Z_UP: [90, 0, 0],
                  Z_DOWN: [-90, 0, 0]}



