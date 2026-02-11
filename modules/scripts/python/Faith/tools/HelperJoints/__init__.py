from maya import cmds
if not cmds.pluginInfo("quatNodes", q=True, loaded=True):
    try:
        cmds.loadPlugin("quatNodes")
    except RuntimeError:
        cmds.error("You need the quatNodes plugins!")