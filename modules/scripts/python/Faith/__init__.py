# -*- coding: utf-8 -*-
import os
import uuid
import maya.cmds as cmds
from functools import partial
from Faith.tools.small_tools import small_tool
import re

ScriptPath = os.path.dirname(__file__)


def LoadPlugin():
    maya_version = cmds.about(version=True)
    ScriptPath = os.path.dirname(__file__)
    PluginPath = ScriptPath.split('modules')[0].replace("\\","/") + "/modules/plugins/win64/" + maya_version + "/v0.3"
    maya_env = os.environ.get("MAYA_PLUG_IN_PATH", "")
    maya_env += str(os.pathsep + PluginPath)
    os.environ["MAYA_PLUG_IN_PATH"] = maya_env


KEY_FIELD = "KeyField"

floatUI_command = """
from imp import reload
import Faith.floatUI as ui
reload(ui)
w = ui.wnd()
w.show()
"""

help_command = """
cmds.showHelp( 'file:///R:/Public_Info/Ebook/mayaHelp2018_CHS/index.html', absolute=True )
"""

skin_command = """
from Faith.tools.weightEdit import weightTool as weightTool
weightTool = weightTool.weightTool()
weightTool.UI()
"""

bezier_weight_command = """
from imp import reload
from Faith.tools.weights import ui
reload(ui)
ui.show()
"""

sdk_command = """
from imp import reload
from Faith.tools.SDK_Manager import SDK_Manager as sdk
reload(sdk)
sdk.show_guide_component_manager()
"""

bs_command = """
from imp import reload
from Faith.tools.blendShapeManage import blendShapeManage_mirror as ggbs
reload(ggbs)
ggbs.blendShapeManage_UI()
"""

dr_command = """
from Faith.tools.small_tools import driver_win as lizhi_driver_win
lizhi_driver_win = lizhi_driver_win.driver_win()
lizhi_driver_win.driver_win()
"""

grp_command = """
from Faith.tools.AddGrpTool import addGrpUI as addGrpUI
addGrpUI.AddGrpWin().win()
"""

name_command = """
from imp import reload
from Rosa.tools.namer import namer
reload(namer)
ObjRename = namer.namer() 
ObjRename.namer_ui()
"""

combine_command = """
from Faith.tools.combineDirve import combinDriveToolUI as cbdWin
from imp import reload
reload(cbdWin)
jCombinDirveUI = cbdWin.JunCombinDirveUI()
jCombinDirveUI.CBDwin()
"""

nurbs_command = """
from imp import reload
from Faith.tools.NurbsManager import NurbsManager as nurbs
reload(nurbs)
nurbs.show_guide_component_manager()
"""

vis_command = """
from imp import reload
from Faith.tools.small_tools import createVisibility
reload(createVisibility)
CreateVis = createVisibility.CreateVis()
CreateVis.Create_vis_UI()
"""

sin_command = """
from Faith.tools.small_tools import AddObjSin
aos = AddObjSin.AddObjSin()
aos.win()
"""

follic_command = """
from imp import reload
from Faith.tools.FollicTool import FollicEdit as follicEdit
reload(follicEdit)
follic = follicEdit.Follic()
follic.win()
"""

const_command = """
from Faith.tools.small_tools import ConstrainObj
constrainObj = ConstrainObj.ConstrainObj()
constrainObj.win()
"""

lock_command = """
from Faith.tools.small_tools import LockObj
LockTool = LockObj.LockTool()
LockTool.win()
"""

select_command = """
from Faith.tools.small_tools import selectTool as selTool
selTool = selTool.selTool()
selTool.win()
"""

joint_command = """
from Faith.tools.small_tools import JntEditTool
JntEditTool = JntEditTool.JntEditTool()
JntEditTool.JntEditToolUI()
"""

crv_command = """
from imp import reload
from Faith.tools.small_tools import curveTool
reload(curveTool)
curveTool = curveTool.curveTool()
curveTool.win()
"""

ctrl_command = """
from Faith.tools.small_tools import ctrl
ctrl = ctrl.ctrl()
ctrl.win()
"""

sec_command = """
from Faith.tools.small_tools import secondaryTool
sec = secondaryTool.Secondary()
sec.win()
"""

realFacs_face_system = """
from imp import reload
from Faith.tools.FacsTool import RealFacsFacial
reload(RealFacsFacial)
RealFacsFacial.show_guide_component_manager()
"""

follow_command = """
from Faith.tools.Follow import FollowTool as FollowTool
ft = FollowTool.followTool()
ft.win()
"""

fr_command = """
from imp import reload
from Faith.tools.Jun_projectTools.IMM_Tool import IMMORTAL_RigTool as IMMORTAL_RigTool
reload(IMMORTAL_RigTool)
IMMORTAL_RigTool = IMMORTAL_RigTool.IMMORTAL_RigTool()
IMMORTAL_RigTool.win()
"""

lztool_command = """
import sys
sys.path.append('R:\\rigToolset\\ToLizhi\\LZ_Tools')
sys.path.append('R:\\rigToolset\\ToLizhi\\LZ_Tools\\tools_Persional')
import LZ_Tools_UI
a = LZ_Tools_UI.LZ_tools()
a.LZ_Tools_UI()
"""

lowRig_facial_system = """
import os
pyPath = r'R:\\rigToolset\\ToLizhi\\LZ_Tools\\cartoon_sys\\basic_body_build\\mfc_layoutFaceTool'
tempPath = os.path.join(os.path.dirname(pyPath),'mfc_layoutFaceTool')
if cmds.about(linux=True):
    tempPath = self.convertPath_windows2linux(tempPath)
if tempPath not in sys.path:
    sys.path.append(tempPath)
import mfc_layoutFace
tempIns = mfc_layoutFace.mfc_layoutFace()
tempIns.showUI()
"""

longwang_CorrectiveShape = """
from importlib import reload
from Rosa.tools.correctShapes.corrective_editor2 import *
corrective_buildUI()
"""

longwang_keyFrameTool = """
pyPath = r'R:\\rigToolset\\ToLizhi\\LZ_Tools\\cartoon_sys\\basic_body_build\\mfc_layoutFaceTool'
scriptPath = os.path.dirname(pyPath)
tempPath = os.path.join(scriptPath,'oe_keyFrame/OE_KEYFRAME.mel')
if cmds.about(linux=True):
    tempPath = self.convertPath_windows2linux(tempPath)
tempPath = tempPath.replace('\\\\','/')
pm.mel.eval( 'source "%s";'%tempPath )
"""

# rosa code - -----------------------------------------------------------------------------------------------
timeline_redo_armTwist = """
from importlib import reload
from Rosa.tools.timeline_update import timeline_redo_armTwist as timeline_redo_armTwist
reload(timeline_redo_armTwist)
timeline_redo_armTwist.redoArmTwist()
"""

timeline_update_psd = """
from importlib import reload
from Rosa.tools.timeline_update import timeline_psd as timelinePSD
reload(timelinePSD)
timelinePSD.create_timeLine_psd()
"""

timeline_update_helper = """
from importlib import reload
from Faith.tools.small_tools import HelperJointCreate
reload(HelperJointCreate)
HelperJointCreate.TimeLineHelper()
"""

timeline_update_mirrorHelper = """
from imp import reload
from Faith.tools.small_tools import HelperJointCreate
reload(HelperJointCreate)
HelperJointCreate.mirrorHelperJoint()
"""

timeline_update_elo = """
from imp import reload
from Rosa.tools.timeline_update import timeline_eio_update
reload(timeline_eio_update)
timeline_eio_update.organize_files()
"""


averageSkin_command = """
from importlib import reload
from Rosa.tools.skinner import average_skin as average_skin
reload(average_skin)
average_skin.uiShow()
"""

pruneSkin_command = """
from importlib import reload
from Rosa.tools.skinner import prune_skin as prune_skin
reload(prune_skin)
prune_skin.uiShow()
"""

faith_splitSkin_command = """
from importlib import reload
from Rosa.tools.skinner import split_skin as split_skin
reload(split_skin)
split_skin.uiShow()
"""

ioSkin_command = """
from importlib import reload
from Rosa.tools.skinner import io_skin as io_skin
reload(io_skin)
io_skin.uiShow()
"""

exSkin_command = """
from imp import reload
from Faith.tools.small_tools import small_tool
reload(small_tool)
small_tool.transferSkinWeights(type='export')
"""


imSkin_command = """
from imp import reload
from Faith.tools.small_tools import small_tool
reload(small_tool)
small_tool.transferSkinWeights(type='import')
"""

skin2Layer_command = """
from imp import reload
from Faith.tools.small_tools import small_tool
reload(small_tool)
small_tool.convertSkin2NgLayer()
"""

smoothSkinPainter_command = """
from importlib import reload
from Rosa.tools.skinner import smoothSkinPainter as smoothSkinPainter
reload(smoothSkinPainter)
smoothSkinPainter.uiShow()
"""

batchCopy_command = """
from importlib import reload
from Rosa.tools.batchCopy import batchCopy as batchCopy
reload(batchCopy)
batchCopy.uiShow()
"""

sdkEditor_command = """
from importlib import reload
from Rosa.tools.sdker import sdkEditor as sdkEditor
reload(sdkEditor)
sdkEditor.uiShow()
"""

check_command = """
from importlib import reload
from Rosa.tools.checker import assetCheck as assetCheck
reload(assetCheck)
assetCheck.uiShow()
"""

deformer_command = """
from imp import reload
import Faith.tools.small_tools.splitBlendShape as sp
reload(sp)
sp.deformer_manager().deformer_manager_UI()
"""

psder_command = """
from imp import reload
import Rosa.tools.poseDriver.psder as psder
reload(psder)
psder.uiShow()
"""

niceKey_command = """
from imp import reload
from Rosa.tools.dt import niceKey as niceKey
reload(niceKey)
nkey = niceKey.niceKeyFrame()
nkey.gui()
"""

controller_command = """
from imp import reload
from Rosa.tools.controller import controller as ctrl
reload(ctrl)
ctrl.uiShow()
"""

matrixSec_command = """
from imp import reload
from Rosa.tools.matrixSec import matrixSec as matrixSec
reload(matrixSec)
matrixSec.uiShow()
"""

QuadRemesher_command = """
import Rosa.tools.QuadRemesher.Contents.scripts.QuadRemesher as QuadRemesher
qr = QuadRemesher.QuadRemesher()
"""

rxRig_command = """
from imp import reload
import Rosa.tools.RX.main as main
reload(main)
main.run()
"""

lz_bs_command = """
from imp import reload
from Rosa.tools.lz_bs import blendshape_menager as lzbsm
reload(lzbsm)
lzbs = lzbsm.blendshape_menege()
lzbs.blendshape_menege_UI()
"""

helperJoints_command = """
from imp import reload
import Faith.tools.HelperJoints.Helper_Manager as helper
reload(helper)
helper.show()
"""

bsTool_command = """
from imp import reload
from Faith.tools.BlendShapeManager import BlendShapeManager as bs
reload(bs)
bs.show_guide_component_manager()
"""

craw_command = """
from imp import reload
from Faith.tools.CrawlingManager import CrawlingManager as cw
reload(cw)
cw.show_guide_component_manager()
"""

ng_command = """
from ngSkinTools2.ui import shelf
shelf.install_shelf()
"""

shotSculptor_command = """
from imp import reload
from Rosa.tools.shotSculpt import shotSculptor as ssp
reload(ssp)
ssp.uiShow()
"""

def makeMyCustomUI():
    checkLicense()


def ChestMenu():
    customMenu = cmds.menu("FaithMenu", label="CG RIG", parent="MayaWindow", to=1)

    cmds.menuItem(l='Open Script By Float UI', p=customMenu, c=floatUI_command)
    cmds.menuItem(l='Open Maya Help Doc', p=customMenu, c=help_command)

    # rigging system menu ------------------------------------------------------------
    cmds.menuItem(d=1, dl='Systems', p=customMenu)
    timeline_Update_menu = cmds.menuItem(parent=customMenu, label="TimeLine System Update", subMenu=True, to=1)
    cmds.menuItem(l='Redo Arm Twist', p=timeline_Update_menu, c=timeline_redo_armTwist)
    cmds.menuItem(l='Create Pose Drivers', p=timeline_Update_menu, c=timeline_update_psd)
    cmds.menuItem(l='Create Helper Joints', p=timeline_Update_menu, c=timeline_update_helper)
    cmds.menuItem(l='Mirror Helper Joints', p=timeline_Update_menu, c=timeline_update_mirrorHelper)
    cmds.menuItem(d=1, p=timeline_Update_menu)
    cmds.menuItem(l='Elo Timeline Update', p=timeline_Update_menu, c=timeline_update_elo)

    cmds.menuItem(l='RealFacs Facial System', p=customMenu, c=realFacs_face_system)
    # cmds.menuItem(l='RX System', p=customMenu, c=rxRig_command)
    cmds.menuItem(l='LowRig Facial System', p=customMenu, c=lowRig_facial_system)

    cmds.menuItem(l='Nurbs IKFK System', p=customMenu, c=nurbs_command)
    # cmds.menuItem(l='Matrix Secondary System', p=customMenu, c=sec_command)

    cmds.menuItem(l='Check System', p=customMenu, c=check_command)

    shot_final_menu = cmds.menuItem(parent=customMenu, label="Shot Final System", subMenu=True, to=1)
    cmds.menuItem(l='shot sculpt', p=shot_final_menu, c=shotSculptor_command)

    # manager system menu ------------------------------------------------------------
    cmds.menuItem(d=1, dl='Managers', p=customMenu)

    # Mesh Manager
    meshMenu = cmds.menuItem(l='Mesh', p=customMenu, subMenu=True, to=1)
    # cmds.menuItem(l='Mirror Mesh', p=meshMenu, c=skin_command)
    cmds.menuItem(l='Quad Remesher', p=meshMenu, c=QuadRemesher_command)

    # Skin Manager
    skinMenu = cmds.menuItem(l='Skin', p=customMenu, subMenu=True, to=1)
    cmds.menuItem(l='Ng Skin2', p=skinMenu, c=ng_command)
    cmds.menuItem(d=1, p=skinMenu)
    cmds.menuItem(l='Jun Skin', p=skinMenu, c=skin_command)
    cmds.menuItem(d=1, p=skinMenu)
    cmds.menuItem(l='Bezier Split', p=skinMenu, c=bezier_weight_command)
    cmds.menuItem(l='Faith Split', p=skinMenu, c=faith_splitSkin_command)
    cmds.menuItem(d=1, p=skinMenu)
    cmds.menuItem(l='Average', p=skinMenu, c=averageSkin_command)
    cmds.menuItem(l='Prune', p=skinMenu, c=pruneSkin_command)
    cmds.menuItem(l='Smooth Painter', p=skinMenu, c=smoothSkinPainter_command)
    cmds.menuItem(d=1, p=skinMenu)
    cmds.menuItem(l='Export Skin', p=skinMenu, c=exSkin_command)
    cmds.menuItem(l='Import Skin', p=skinMenu, c=imSkin_command)
    cmds.menuItem(l='IO Skin', p=skinMenu, c=ioSkin_command)

    # SDK Manager
    sdkMenu = cmds.menuItem(l='Set Driven Key', p=customMenu, subMenu=True, to=1)
    # cmds.menuItem(l='SDK Tool', p=sdkMenu, c=sdk_command)
    cmds.menuItem(l='SDK Editor', p=sdkMenu, c=sdkEditor_command)
    cmds.menuItem(l='Pose Driver', p=sdkMenu, c=dr_command)
    cmds.menuItem(l='Pose Driver 2.0', p=sdkMenu, c=psder_command)
    cmds.menuItem(l='Combine Driver', p=sdkMenu, c=combine_command)
    cmds.menuItem(l='SDK IO', p=sdkMenu, c=sdk_command)

    # Bs Manager
    bsMenu = cmds.menuItem(l='Correct Shape', p=customMenu, subMenu=True, to=1)
    cmds.menuItem(l='Split blendShape', p=bsMenu, c=deformer_command)
    cmds.menuItem(l='BlendShape Manager', p=bsMenu, c=bs_command)
    cmds.menuItem(l='Corrective Manager', p=bsMenu, c=longwang_CorrectiveShape)
    cmds.menuItem(l='Helper Manager', p=bsMenu, c=helperJoints_command)
    cmds.menuItem(l='Nice Key', p=bsMenu, c=niceKey_command)

    # Crv Manager
    crvMenu = cmds.menuItem(l='Curve', p=customMenu, subMenu=True, to=1)
    cmds.menuItem(l='Create Ctrl', p=crvMenu, c=ctrl_command)
    cmds.menuItem(l='Control Tool', p=crvMenu, c=controller_command)
    cmds.menuItem(l='Matrix Control', p=crvMenu, c=matrixSec_command)

    # Other Manager
    popularMenu = cmds.menuItem(l='Popular', p=customMenu, subMenu=True, to=1)
    cmds.menuItem(l='Obj Rename', p=popularMenu, c=name_command)
    cmds.menuItem(l='Add Group', p=popularMenu, c=grp_command)
    cmds.menuItem(l='Batch Copy', p=popularMenu, c=batchCopy_command)
    cmds.menuItem(l='Skin To Ng Layer', p=popularMenu, c=skin2Layer_command)
    cmds.menuItem(l='Lock Tool', p=popularMenu, c=lock_command)
    cmds.menuItem(l='Object Sin', p=popularMenu, c=sin_command)
    cmds.menuItem(l='Crawling Tool', p=popularMenu, c=craw_command)

    # Old Manager
    otherMenu = cmds.menuItem(l='Other', p=customMenu, subMenu=True, to=1)
    # --------------------------------------------------------------------------------
    cmds.menuItem(l='Constrain Obj', p=otherMenu, c=const_command)
    cmds.menuItem(l='Select Tool', p=otherMenu, c=select_command)
    cmds.menuItem(l=u'骨骼工具', p=otherMenu, c=joint_command)
    cmds.menuItem(l='Follic Tool', p=otherMenu, c=follic_command)
    cmds.menuItem(l=u'创建Visibility', p=otherMenu, c=vis_command)
    cmds.menuItem(l=u'Follow Tool', p=otherMenu, c=follow_command)
    # --------------------------------------------------------------------------------
    cmds.menuItem(d=1, p=otherMenu)
    cmds.menuItem(parent=otherMenu, label=u"番剧", c=fr_command)
    cmds.menuItem(parent=otherMenu, label=u"获取曲线长度", c=small_tool.getCurveLength)
    cmds.menuItem(parent=otherMenu, label=u"无orig复制模型", c=small_tool.copymodel)
    cmds.menuItem(parent=otherMenu, label=u"曾龙安Key帧工具", c=longwang_keyFrameTool)
    cmds.menuItem(parent=otherMenu, label=u"李志BS工具", c=lz_bs_command)
    cmds.menuItem(parent=otherMenu, label=u"elo驱动Gama节点", c=small_tool.driveGama)


# delete the ui
def removeMyCustomUI():
    cmds.deleteUI("FaithMenu")


def getLicense(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            data = f.readline()
        return data
    else:
        return False


def getlic():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    nums = re.findall("\d", mac)
    key = ''
    for n in nums:
        transformValue = (int(n) * 0.8 + 16) / 2.6
        nNum = round(transformValue, 1)
        key += (str(nNum).split('.')[1])

    return key


def checkLicense(*args):
    # get mac address
    key = getlic()
    prefsPath = cmds.internalVar(userPrefDir=True)
    licPath = os.path.join(os.path.abspath(os.path.join(prefsPath, "../..")), "modules")
    licData = getLicense(licPath + '/License.lic')

    if licData == key:
        ChestMenu()
    else:
        if cmds.window('License', ex=True):
            cmds.deleteUI('License')
        window = cmds.window('License', title="License Window", widthHeight=(500, 35))
        cmds.columnLayout(adjustableColumn=True)
        cmds.warning("Mac UUID is : %s" % (uuid.UUID(int=uuid.getnode()).hex[-12:]))
        textGrp = cmds.textFieldButtonGrp(KEY_FIELD, label='Mac Active',
                                          text='', buttonLabel='Active',
                                          bc=partial(active, licPath + '/License.lic', key))
        cmds.setParent('..')
        cmds.showWindow(window)


def active(path, lic, *args):
    key = cmds.textFieldButtonGrp(KEY_FIELD, q=True, text=True)
    with open(path, "w") as f:
        f.write(key)
    if key == lic:
        ChestMenu()
    else:
        cmds.warning("License Error!")
