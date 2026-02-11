######################################################################
# This module holds standard build templates.
#
# each module will automatically be listed in the template build ui
import maya.cmds as mc
import maya.mel as mel

import templateTools
import importMod

# Build full biped template rigs
def biped():
    if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
        return
    mc.file (new=1, f=1)

    #modules = ['base','torso','neck','eyes','bipedArm','bipedLeg','hand']
    modules = ['base','torso','neck','bipedArm','bipedLeg','hand']
    for m in modules:
        mod = importMod.import_module(m, r=1)
        mod.template()
        templateTools.resolveTempPrefix()

    return True

# Build full biped template rigs
def quadriped():
    if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
        return
    mc.file (new=1, f=1)

    modules = ['base','torso','neck','quadArm','quadLeg','tail']
    for m in modules:
        mod = importMod.import_module(m, r=1)
        mod.template()
        templateTools.resolveTempPrefix()

        if m == 'torso':
            mc.setAttr('torso.rx',  90)

    return True

# Build simple prop rigs
def prop():
    if not mel.eval('checkForUnknownNodes(); int $result = `saveChanges("file -f -new")`;'):
        return
    mc.file (new=1, f=1)

    modules = ['base','cog']
    for m in modules:
        mod = importMod.import_module(m, r=1)
        mod.template()
        #templateTools.resolveTempPrefix()

    return True
