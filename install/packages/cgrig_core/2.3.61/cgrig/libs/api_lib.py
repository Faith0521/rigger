import maya.cmds as cmds
import os
import sys


version = int(round(float(cmds.about(q=1, v=1))))
plugin_paths = os.environ["CGRIG_CORE_PYD_PATHS"]
pyd_path = os.path.abspath(plugin_paths + "/maya%i" % version).replace("\\", "/")
py_path = os.path.abspath(plugin_paths + "/maya%s" % "default").replace("\\", "/")

if os.path.exists(pyd_path):
    path = pyd_path
else:
    path = py_path

if path not in sys.path:
    sys.path.insert(0, path)


import bs_api
# import skin_api


