from maya import cmds, utils
from pymel import mayautils
import sys,os

def plugin_load():
    import Faith
    Faith.LoadPlugin()
    Faith.makeMyCustomUI()

if not cmds.about(batch = True):
    mayautils.executeDeferred(plugin_load)
