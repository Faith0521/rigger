import maya.cmds as mc
import maya.mel as mel
import os
import sys
import traceback
from importlib import reload

#  env
scriptPath = (os.path.split(os.path.abspath(__file__)))[0].replace('\\', '/')
sys.path.append(scriptPath)

# user
import userHotkeys
import rightClickMenu
from rxCore import aboutUI

def hotkeys():
    userHotkeys.load()

# top menu
def menu(mainwin=None):
    os.environ['RIGTOOLS_ANIMDAG'] = 'False'

    # Create Menu
    # noinspection PyBroadException
    try:
        mc.deleteUI('ToolsMenu')
    except:
        pass

    rigMenu = ''
    if not mainwin:
        mel.eval('global string $gMainWindow;')
        mainwin = mel.eval('$tmp = $gMainWindow;')
        rigMenu = mc.menu('ToolsMenu', l=' RX', p=mainwin, to=1)
    else:
        pass

    # ---------------------------------------
    mc.menuItem(d=1, dl='Main', p=rigMenu)
    mc.menuItem(l='Checker', p=rigMenu, c=checkTool)
    mc.menuItem(d=1, dl='Modeling', p=rigMenu)
    mc.menuItem(l='Symmetry Mesh', p=rigMenu)
    mc.menuItem(l='Normalize Shape Name', p=rigMenu)

    # ---------------------------------------
    mc.menuItem(d=1, dl='Rigging', p=rigMenu)
    mc.menuItem(l='Auto Rig System', p=rigMenu, c=autoRigSystem)
    mc.menuItem(l='Hand Pose Tool', p=rigMenu, c=handPoseTool)
    mc.menuItem(l='Control Tool', p=rigMenu, c=controlTool)
    mc.menuItem(l='SDK Tool', p=rigMenu)
    mc.menuItem(l='Correct Shapes Tool', p=rigMenu)
    # ---------------------------------------
    mc.menuItem(d=1, dl='Animation', p=rigMenu)
    mc.menuItem(cb=0, l='Custom Right-Button Menu', p=rigMenu, c=rightClick)

    # ---------------------------------------
    #mc.menuItem(d=1, dl='ToolBox', p=rigMenu)

    #---------------------------------------
    mc.menuItem(d=1, dl='Misc', p=rigMenu)
    mc.menuItem(l='Load Shelf', p=rigMenu, c=shelf)
    mc.menuItem(l='Help Docs', p=rigMenu)


mel.eval('source "createAndAssignShader.mel"')
mel.eval('source "channelBoxCommand.mel"')
mc.evalDeferred('import maya.cmds as mc')
mc.evalDeferred('import maya.mel as mel')
mc.evalDeferred('import os')
mc.evalDeferred('import sys')
mc.evalDeferred('{0}.hotkeys()'.format(__name__.split('.')[-1]))
mc.evalDeferred('{0}.menu()'.format(__name__.split('.')[-1]))


def autoRigSystem(*kargs):
    # noinspection PyBroadException
    try:
        import main
        reload(main)
        main.run()
    except:
        msgs = traceback.format_exc()
        mc.error('Load Auto Rig system failed\n' + msgs)


def handPoseTool(*kargs):
    """
    hand system need a tool to set initial finger pose.
    :param kargs:
    :return:
    """
    # noinspection PyBroadException
    try:
        from rxParts import hand
        reload(hand)
        handPoseUi = hand.UI()
        handPoseUi.show()
    except:
        msgs = traceback.format_exc()
        mc.error('Load hand pose system failed\n' + msgs)


def controlTool(*kargs):
    """

    :param kargs:
    :return:
    """
    # noinspection PyBroadException
    try:
        import controlTools
        controlTools.run()
    except:
        msgs = traceback.format_exc()
        mc.error('Load control tool failed\n' + msgs)


def checkTool(*kargs):
    """
    load check tool : alone mode.
    :param kargs:
    :return:
    """
    # noinspection PyBroadException
    try:
        import assetCheck
        reload(assetCheck)
        checkUI = assetCheck.AssetCheck(uiName='assetCheckUI_alone',
                                        parent=aboutUI.get_maya_window(),
                                        publish=0)
        checkUI.show()
    except:
        msgs = traceback.format_exc()
        mc.error(' Load check tool system failed\n' + msgs)


def rightClick(*kargs):
    """
    load rig system right click menu
    :param kargs:
    :return:
    """
    reload(rightClickMenu)
    rightClickMenu.toggle()


# Load rigging shelf
def shelf(*kargs):
    shelfName = 'Tools'
    if mc.layout(shelfName, q=1, ex=1):
        result = mel.eval('deleteShelfTab "{0}";'.format(shelfName))
        if not result:
            return

            # delete off disk
    sfiles = [os.path.join(mc.internalVar(ush=1).split(':')[-1], 'shelf_{0}.mel'.format(shelfName)),
              os.path.join(mc.internalVar(ush=1).split(':')[-1], 'shelf_{0}.mel.deleted'.format(shelfName))]

    for sfile in sfiles:
        if os.path.isfile(sfile):
            os.remove(sfile)
    mel.eval('addRigShelfTab "{0}";'.format(shelfName))
    #loadShelfItems(assetEnv.geticons())
