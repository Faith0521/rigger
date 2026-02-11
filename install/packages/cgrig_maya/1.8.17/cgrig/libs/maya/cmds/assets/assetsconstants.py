# -*- coding: utf-8 -*-
"""Constants related to default internal assets included withing the CgRig Tools Pro scripts folder.
Light Presets, HDRI skydome texture paths, control curves etc.

.. code-block:: python

    from cgrig.libs.maya.cmds.assets import assetconstants
    assetconstants.DEFAULT_SKYDOME_PATH  # is the path to the default HDRI texture image

Author Andrew Silke
"""

import os

from cgrig.libs.utils import filesystem

# ---------------------------
# Internal Asset Folders
# ---------------------------

PREFERENCES_FOLDER_NAME = "preferences"  # preferences directory
ASSETS_FOLDER_NAME = "assets"  # main assets dir under the internal preferences folder
CONTROL_SHAPES_FOLDER_NAME = "control_shapes"  # the name of the control shapes folder under assets
MODEL_ASSETS_FOLDER_NAME = "model_assets"  # the name of the model assets folder under assets
HDR_SKYDOMES_FOLDER_NAME = "light_suite_ibl_skydomes"
LIGHT_PRESETS_FOLDER_NAME = "light_suite_light_presets"
SHADERS_FOLDER_NAME = "shaders"

# ---------------------------
# Paths To Asset Folders
# ---------------------------

currentPath = os.path.abspath(__file__)
packagePath = filesystem.upDirectory(currentPath, depth=7)  # TODO path is relative, will be a better way
CONTROL_SHAPES_PATH = os.path.join(packagePath, "preferences", ASSETS_FOLDER_NAME, CONTROL_SHAPES_FOLDER_NAME)
MODEL_ASSETS_PATH = os.path.join(packagePath, "preferences", ASSETS_FOLDER_NAME, MODEL_ASSETS_FOLDER_NAME)
HDR_SKYDOMES_PATH = os.path.join(packagePath, "preferences", ASSETS_FOLDER_NAME, HDR_SKYDOMES_FOLDER_NAME)
LIGHT_PRESETS_PATH = os.path.join(packagePath, "preferences", ASSETS_FOLDER_NAME, LIGHT_PRESETS_FOLDER_NAME)
SHADERS_PATH = os.path.join(packagePath, "preferences", ASSETS_FOLDER_NAME, SHADERS_FOLDER_NAME)

# ---------------------------
# Default Asset Names. Usually file names.
# ---------------------------

CONTROL_CIRCLE = "circle"
CONTROL_CUBE = "cube"
CONTROL_SPHERE = "sphere"

ASSET_SHADER_BOT = "shaderBot.cgrigScene"
ASSET_LIGHT_SCENE = "emptyA.cgrigScene"
ASSET_CYC_GREY_SCENE = "bgCycG.cgrigScene"
ASSET_CYC_DARK_SCENE = "bgCycDrk.cgrigScene"
ASSET_MACBETH_BALLS = "mcbthChart.cgrigScene"

LIGHT_PRESET_ASSET_DEFAULT = "aDflt.cgrigScene"
LIGHT_PRESET_THREE_POINT = "softThree.cgrigScene"
LIGHT_PRESET_THREE_POINT_DARK = "soft3Drk.cgrigScene"
LIGHT_PRESET_F_PUMPS = "fPumps.cgrigScene"
LIGHT_PRESET_WINTER_F = "wForest.cgrigScene"
LIGHT_PRESET_RED_AQUA_RIM = "redAqua.cgrigScene"
LIGHT_PRESET_SOFT_TOP = "sTpCircle.cgrigScene"
LIGHT_PRESET_SOFT_TOP_RIM = "pure_softTop_softBoxBehind.cgrigScene"

HDR_F_PUMPS = "factPumps.hdr"
HDR_F_PUMPS_ROT_OFFSET = 154.1
HDR_F_PUMPS_INT_MULT = 4.0

HDR_F_PUMPS_BW = "factPumps_g.hdr"
HDR_F_PUMPS_BW_ROT_OFFSET = 154.1
HDR_F_PUMPS_BW_INT_MULT = 4.0

HDR_WINTER_F = "wForest.hdr"
HDR_WINTER_F_ROT_OFFSET = 4.0
HDR_WINTER_F_INT_MULT = 1.9

HDR_PLATZ = "potsdamerPlatz_g.hdr"
HDR_PLATZ_ROT_OFFSET = -42.0
HDR_PLATZ_INT_MULT = 1.4

HDR_PLATZ_PATH = os.path.join(HDR_SKYDOMES_PATH, HDR_PLATZ)
HDR_F_PUMPS_PATH = os.path.join(HDR_SKYDOMES_PATH, HDR_F_PUMPS)
HDR_F_PUMPS_BW_PATH = os.path.join(HDR_SKYDOMES_PATH, HDR_F_PUMPS_BW)
HDR_WINTER_F_PATH = os.path.join(HDR_SKYDOMES_PATH, HDR_WINTER_F)

DEFAULT_SKYDOME_PATH = HDR_PLATZ_PATH
DEFAULT_SKYDOME_INT_MULT = HDR_PLATZ_INT_MULT
DEFAULT_SKYDOME_ROT_OFFSET = HDR_PLATZ_ROT_OFFSET

# --------------------
# Light Preset Internal Files
# --------------------

DEFAULT_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_F_PUMPS)  # bw factory pumps
WINTER_F_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_WINTER_F)  # Default IBL no changes
ASSET_LIGHTPRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_ASSET_DEFAULT)  # rim studio
THREE_POINT_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_THREE_POINT)  # three point soft
THREE_POINT_DRK_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_THREE_POINT_DARK)  # three point dark
RED_AQUA_RIM_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_RED_AQUA_RIM)  # three point soft
SOFT_TOP_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_SOFT_TOP)  # three point soft
SOFT_TOP_RIM_LIGHT_PRESET_PATH = os.path.join(LIGHT_PRESETS_PATH, LIGHT_PRESET_SOFT_TOP_RIM)  # three point soft

# Dictionaries with the preset path and HDRI overriddes as the internal presets HDRI don't work correctly.
PRESET_DEFAULT = {"path": ASSET_LIGHTPRESET_PATH,
                  "hdriPath": HDR_F_PUMPS_BW_PATH,
                  "intMult": HDR_F_PUMPS_BW_INT_MULT,
                  "rotOffset": HDR_F_PUMPS_BW_ROT_OFFSET}  # this is the factory pump bw with rims
PRESET_THREEPOINT = {"path": THREE_POINT_LIGHT_PRESET_PATH,
                     "hdriPath": HDR_F_PUMPS_BW_PATH,
                     "intMult": HDR_F_PUMPS_BW_INT_MULT,
                     "rotOffset": HDR_F_PUMPS_BW_ROT_OFFSET}
PRESET_THREEPOINTDRK = {"path": THREE_POINT_DRK_LIGHT_PRESET_PATH,
                        "hdriPath": "",
                        "intMult": 1.0,
                        "rotOffset": 0.0}
PRESET_SOFTTOP = {"path": SOFT_TOP_LIGHT_PRESET_PATH,
                  "hdriPath": "",
                  "intMult": 1.0,
                  "rotOffset": 0.0}
PRESET_REDAQUA = {"path": RED_AQUA_RIM_LIGHT_PRESET_PATH,
                  "hdriPath": HDR_F_PUMPS_PATH,
                  "intMult": HDR_F_PUMPS_INT_MULT,
                  "rotOffset": HDR_F_PUMPS_ROT_OFFSET}

# SKydomes -----------------
PRESET_FACTORYCOLOR = {"path": WINTER_F_LIGHT_PRESET_PATH,
                       "hdriPath": HDR_F_PUMPS_PATH,
                       "intMult": HDR_F_PUMPS_INT_MULT,
                       "rotOffset": HDR_F_PUMPS_ROT_OFFSET}
PRESET_FACTORYGREY = {"path": WINTER_F_LIGHT_PRESET_PATH,
                      "hdriPath": HDR_F_PUMPS_BW_PATH,
                      "intMult": HDR_F_PUMPS_BW_INT_MULT,
                      "rotOffset": HDR_F_PUMPS_BW_ROT_OFFSET}
PRESET_WINTER = {"path": WINTER_F_LIGHT_PRESET_PATH,
                 "hdriPath": HDR_WINTER_F_PATH,
                 "intMult": HDR_WINTER_F_INT_MULT,
                 "rotOffset": HDR_WINTER_F_ROT_OFFSET}
PRESET_CITYPLATZ = {"path": WINTER_F_LIGHT_PRESET_PATH,
                    "hdriPath": HDR_PLATZ_PATH,
                    "intMult": HDR_PLATZ_INT_MULT,
                    "rotOffset": HDR_PLATZ_ROT_OFFSET}  # this is the default city platz

# ---------------------------
# Shader CgRig Scenes
# ---------------------------

SHADERS_SKIN_DARK_BACKLIT = "skBnDrkB.cgrigScene"
SHADERS_DARK_BACKGROUND = "dkMtBg.cgrigScene"

# ---------------------------
# Camera Types
# ---------------------------
CAMTYPE_DEFAULT = "default"
CAMTYPE_HDR = "hdr"
CAMTYPE_CONTROL = "control"

# ---------------------------
# Default Renderer
# ---------------------------

RENDERER = "Arnold"  # Not used by UIs, just for testing
