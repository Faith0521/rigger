import os
import time
from imp import reload
import maya.cmds as mc
import maya.mel as mel
from pymel.core import *
from Faith.maya_utils import function_utils as func
from pymel import versions
from functools import partial
from maya import cmds, OpenMaya
from Rosa.tools.timeline_update import timeline_eio_update
from maya.api import OpenMaya as om

reload(func)

timeLineCtrlList = ["L_ArmA_curve", "L_ArmB_curve", "R_ArmA_curve", "R_ArmB_curve", "L_LegA_curve", "L_LegB_curve",
                    "R_LegA_curve", "R_LegB_curve", "L_UpLid_A_baseCrv", "L_UpLid_A_baseCrv", "L_UpLid_A_bindCrv",
                    "L_UpLid_A_bindCrv", "L_UpLid_A_secCrv", "L_UpLid_A_secCrv", "L_UpLid_A_blinkCrv",
                    "L_UpLid_A_blinkCrv", "L_UpLid_A_blinkWire", "L_UpLid_A_blinkWire", "L_UpLid_A_blinkTarget",
                    "L_UpLid_A_bindWire", "L_UpLid_A_bindWire", "L_UpLid_A_bindWireBaseWire",
                    "L_UpLid_A_blinkWireBaseWire", "L_UpLid_A_blinkDrver", "L_UpLid_A_blinkDrver",
                    "L_UpLid_A_blinkSecCrv", "L_UpLid_A_blinkSecCrv", "L_UpLid_A_blinkBindCrv",
                    "L_UpLid_A_blinkBindCrv", "L_UpLid_A_secWire", "L_UpLid_A_secWire", "L_UpLid_A_secWireBaseWire",
                    "L_UpLid_A_blinkSecWire", "L_UpLid_A_blinkSecWire", "L_UpLid_A_blinkSecWireBaseWire",
                    "L_UpLid0_A_sdk1_bind", "L_UpLid1_A_sdk1_bind", "L_UpLid2_A_sdk1_bind", "L_UpLid3_A_sdk1_bind",
                    "L_UpLid4_A_sdk1_bind", "L_LoLid_A_baseCrv", "L_LoLid_A_baseCrv", "L_LoLid_A_bindCrv",
                    "L_LoLid_A_bindCrv", "L_LoLid_A_secCrv", "L_LoLid_A_secCrv", "L_LoLid_A_blinkCrv",
                    "L_LoLid_A_blinkCrv", "L_LoLid_A_blinkWire", "L_LoLid_A_blinkWire", "L_LoLid_A_blinkTarget",
                    "L_LoLid_A_bindWire", "L_LoLid_A_bindWire", "L_LoLid_A_bindWireBaseWire",
                    "L_LoLid_A_blinkWireBaseWire", "L_LoLid_A_blinkDrver", "L_LoLid_A_blinkDrver",
                    "L_LoLid_A_blinkSecCrv", "L_LoLid_A_blinkSecCrv", "L_LoLid_A_blinkBindCrv",
                    "L_LoLid_A_blinkBindCrv", "L_LoLid_A_secWire", "L_LoLid_A_secWire", "L_LoLid_A_secWireBaseWire",
                    "L_LoLid_A_blinkSecWire", "L_LoLid_A_blinkSecWire", "L_LoLid_A_blinkSecWireBaseWire",
                    "L_LoLid0_A_sdk1_bind", "L_LoLid1_A_sdk1_bind", "L_LoLid2_A_sdk1_bind", "L_LoLid3_A_sdk1_bind",
                    "L_LoLid4_A_sdk1_bind", "L_UpRing_A_baseCrv", "L_UpRing_A_baseCrv", "L_UpRing_A_bindCrv",
                    "L_UpRing_A_bindCrv", "L_UpRing_A_secCrv", "L_UpRing_A_bindWire", "L_UpRing_A_bindWire",
                    "L_UpRing_A_secWire", "L_UpRing_A_bindWireBaseWire", "L_UpRing0_A_sdk1_bind",
                    "L_UpRing1_A_sdk1_bind", "L_UpRing2_A_sdk1_bind", "L_UpRing3_A_sdk1_bind", "L_UpRing4_A_sdk1_bind",
                    "L_LoRing_A_baseCrv", "L_LoRing_A_baseCrv", "L_LoRing_A_bindCrv", "L_LoRing_A_bindCrv",
                    "L_LoRing_A_secCrv", "L_LoRing_A_bindWire", "L_LoRing_A_bindWire", "L_LoRing_A_secWire",
                    "L_LoRing_A_bindWireBaseWire", "L_LoRing0_A_sdk1_bind", "L_LoRing1_A_sdk1_bind",
                    "L_LoRing2_A_sdk1_bind", "L_LoRing3_A_sdk1_bind", "L_LoRing4_A_sdk1_bind", "R_UpLid_A_baseCrv",
                    "R_UpLid_A_baseCrv", "R_UpLid_A_bindCrv", "R_UpLid_A_bindCrv", "R_UpLid_A_secCrv",
                    "R_UpLid_A_secCrv", "R_UpLid_A_blinkCrv", "R_UpLid_A_blinkCrv", "R_UpLid_A_blinkWire",
                    "R_UpLid_A_blinkWire", "R_UpLid_A_blinkTarget", "R_UpLid_A_bindWire", "R_UpLid_A_bindWire",
                    "R_UpLid_A_bindWireBaseWire", "R_UpLid_A_blinkWireBaseWire", "R_UpLid_A_blinkDrver",
                    "R_UpLid_A_blinkDrver", "R_UpLid_A_blinkSecCrv", "R_UpLid_A_blinkSecCrv", "R_UpLid_A_blinkBindCrv",
                    "R_UpLid_A_blinkBindCrv", "R_UpLid_A_secWire", "R_UpLid_A_secWire", "R_UpLid_A_secWireBaseWire",
                    "R_UpLid_A_blinkSecWire", "R_UpLid_A_blinkSecWire", "R_UpLid_A_blinkSecWireBaseWire",
                    "R_UpLid0_A_sdk1_bind", "R_UpLid1_A_sdk1_bind", "R_UpLid2_A_sdk1_bind", "R_UpLid3_A_sdk1_bind",
                    "R_UpLid4_A_sdk1_bind", "R_LoLid_A_baseCrv", "R_LoLid_A_baseCrv", "R_LoLid_A_bindCrv",
                    "R_LoLid_A_bindCrv", "R_LoLid_A_secCrv", "R_LoLid_A_secCrv", "R_LoLid_A_blinkCrv",
                    "R_LoLid_A_blinkCrv", "R_LoLid_A_blinkWire", "R_LoLid_A_blinkWire", "R_LoLid_A_blinkTarget",
                    "R_LoLid_A_bindWire", "R_LoLid_A_bindWire", "R_LoLid_A_bindWireBaseWire",
                    "R_LoLid_A_blinkWireBaseWire", "R_LoLid_A_blinkDrver", "R_LoLid_A_blinkDrver",
                    "R_LoLid_A_blinkSecCrv", "R_LoLid_A_blinkSecCrv", "R_LoLid_A_blinkBindCrv",
                    "R_LoLid_A_blinkBindCrv", "R_LoLid_A_secWire", "R_LoLid_A_secWire", "R_LoLid_A_secWireBaseWire",
                    "R_LoLid_A_blinkSecWire", "R_LoLid_A_blinkSecWire", "R_LoLid_A_blinkSecWireBaseWire",
                    "R_LoLid0_A_sdk1_bind", "R_LoLid1_A_sdk1_bind", "R_LoLid2_A_sdk1_bind", "R_LoLid3_A_sdk1_bind",
                    "R_LoLid4_A_sdk1_bind", "R_UpRing_A_baseCrv", "R_UpRing_A_baseCrv", "R_UpRing_A_bindCrv",
                    "R_UpRing_A_bindCrv", "R_UpRing_A_secCrv", "R_UpRing_A_bindWire", "R_UpRing_A_bindWire",
                    "R_UpRing_A_secWire", "R_UpRing_A_bindWireBaseWire", "R_UpRing0_A_sdk1_bind",
                    "R_UpRing1_A_sdk1_bind", "R_UpRing2_A_sdk1_bind", "R_UpRing3_A_sdk1_bind", "R_UpRing4_A_sdk1_bind",
                    "R_LoRing_A_baseCrv", "R_LoRing_A_baseCrv", "R_LoRing_A_bindCrv", "R_LoRing_A_bindCrv",
                    "R_LoRing_A_secCrv", "R_LoRing_A_bindWire", "R_LoRing_A_bindWire", "R_LoRing_A_secWire",
                    "R_LoRing_A_bindWireBaseWire", "R_LoRing0_A_sdk1_bind", "R_LoRing1_A_sdk1_bind",
                    "R_LoRing2_A_sdk1_bind", "R_LoRing3_A_sdk1_bind", "R_LoRing4_A_sdk1_bind", "L_Brow_A_baseCrv",
                    "L_Brow_A_baseCrv", "L_Brow_A_mainCrv", "L_Brow_A_mainCrv", "L_Brow_A_mainWire",
                    "L_Brow_A_mainWire", "L_Brow_A_twistCrv", "L_Brow_A_twistCrv", "L_Brow_A_twistWire",
                    "L_Brow_A_twistWire", "L_Brow_A_mainWireBaseWire", "L_Brow_A_twistWireBaseWire", "R_Brow_A_baseCrv",
                    "R_Brow_A_baseCrv", "R_Brow_A_mainCrv", "R_Brow_A_mainCrv", "R_Brow_A_mainWire",
                    "R_Brow_A_mainWire", "R_Brow_A_twistCrv", "R_Brow_A_twistCrv", "R_Brow_A_twistWire",
                    "R_Brow_A_twistWire", "R_Brow_A_mainWireBaseWire", "R_Brow_A_twistWireBaseWire",
                    "M_BrowJoint_A_crv", "M_UpLip_A_baseCrv", "M_UpLip_A_baseCrv", "M_UpLip_A_zipCrv",
                    "M_UpLip_A_zipCrv", "M_UpLip_A_zipOrig", "M_UpLip_A_zipOrig", "M_UpLip_A_zipTarget",
                    "M_UpLip_A_zipTarget", "M_UpLip_A_bindCrv", "M_UpLip_A_bindCrv", "M_UpLip_A_bindCrvRef",
                    "M_UpLip_A_zipTargetWire", "M_UpLip_A_zipTargetWire", "M_UpLip_A_zipTargetWireA",
                    "M_UpLip_A_zipTargetWireA", "M_UpLip_A_zipTargetWireB", "M_UpLip_A_zipTargetWireB",
                    "M_UpLip_A_bindCrvBaseWire", "M_UpLip_A_bindCrvBaseWire", "M_UpLip_A_zipTargetWireBaseWire",
                    "M_LoLip_A_baseCrv", "M_LoLip_A_baseCrv", "M_LoLip_A_zipCrv", "M_LoLip_A_zipCrv",
                    "M_LoLip_A_zipOrig", "M_LoLip_A_zipOrig", "M_LoLip_A_zipTarget", "M_LoLip_A_zipTarget",
                    "M_LoLip_A_bindCrv", "M_LoLip_A_bindCrv", "M_LoLip_A_bindCrvRef", "M_LoLip_A_zipTargetWire",
                    "M_LoLip_A_zipTargetWire", "M_LoLip_A_zipTargetWireA", "M_LoLip_A_zipTargetWireA",
                    "M_LoLip_A_zipTargetWireB", "M_LoLip_A_zipTargetWireB", "M_LoLip_A_bindCrvBaseWire",
                    "M_LoLip_A_bindCrvBaseWire", "M_LoLip_A_zipTargetWireBaseWire", "fake_R_add_hairA_01_jnt_ctrl",
                    "fake_R_add_hairA_02_jnt_ctrl", "fake_R_add_hairA_03_jnt_ctrl", "fake_R_add_hairA_04_jnt_ctrl",
                    "fake_R_add_hairA_05_jnt_ctrl", "fake_R_add_hair_01_jnt_ctrl", "fake_R_add_hair_02_jnt_ctrl",
                    "fake_R_add_hair_03_jnt_ctrl", "fake_R_add_hair_04_jnt_ctrl", "fake_R_add_hair_05_jnt_ctrl",
                    "fake_L_add_hair_01_jnt_ctrl", "fake_L_add_hair_02_jnt_ctrl", "fake_L_add_hair_03_jnt_ctrl",
                    "fake_L_add_hair_04_jnt_ctrl", "fake_L_add_hair_05_jnt_ctrl", "fake_L_add_hair_06_jnt_ctrl",
                    "fake_L_add_hair_07_jnt_ctrl", "fake_R_MustacheA_jnt_ctrl", "fake_L_MustacheA_jnt_ctrl",
                    "R_add_hairA_01_jnt_ctrl", "R_add_hairA_02_jnt_ctrl", "R_add_hairA_03_jnt_ctrl",
                    "R_add_hairA_04_jnt_ctrl", "R_add_hairA_05_jnt_ctrl", "R_add_hair_01_jnt_ctrl",
                    "R_add_hair_02_jnt_ctrl", "R_add_hair_03_jnt_ctrl", "R_add_hair_04_jnt_ctrl",
                    "R_add_hair_05_jnt_ctrl", "L_add_hair_01_jnt_ctrl", "L_add_hair_02_jnt_ctrl",
                    "L_add_hair_03_jnt_ctrl", "L_add_hair_04_jnt_ctrl", "L_add_hair_05_jnt_ctrl",
                    "L_add_hair_06_jnt_ctrl", "L_add_hair_07_jnt_ctrl", "R_MustacheA_jnt_ctrl", "L_MustacheA_jnt_ctrl",
                    "L_LoLipMain_A_refCrv", "L_LoLipMain_A_refCrv", "L_UpLipMain_A_refCrv", "L_UpLipMain_A_refCrv",
                    "M_LoLipMain_A_refCrv", "M_LoLipMain_A_refCrv", "R_LoLipMain_A_refCrv", "R_LoLipMain_A_refCrv",
                    "R_UpLipMain_A_refCrv", "R_UpLipMain_A_refCrv", "L_Eye_A_ctrl", "L_Eyeball_A_ctrl", "R_Eye_A_ctrl",
                    "R_Eyeball_A_ctrl", "M_EyesAim_A_ctrl", "R_EyeAim_A_ctrl", "R_EyeAim_A_line", "L_EyeAim_A_ctrl",
                    "L_EyeAim_A_line", "L_UpLid_A_ctrl", "L_LoLid_A_ctrl", "L_UpRing_A_ctrl", "L_LoRing_A_ctrl",
                    "L_EyeCornerInn_A_ctrl", "L_EyeCornerOut_A_ctrl", "R_UpLid_A_ctrl", "R_LoLid_A_ctrl",
                    "R_UpRing_A_ctrl", "R_LoRing_A_ctrl", "R_EyeCornerInn_A_ctrl", "R_EyeCornerOut_A_ctrl",
                    "L_Brow_A_ctrl", "L_InnBrow_A_ctrl", "L_MidBrow_A_ctrl", "L_OutBrow_A_ctrl",
                    "L_InnBrow_A_ctrl_L_MidBrow_A_ctrl_line", "L_InnBrow_A_ctrl_L_MidBrow_A_ctrl_line",
                    "L_MidBrow_A_ctrl_L_OutBrow_A_ctrl_line", "L_MidBrow_A_ctrl_L_OutBrow_A_ctrl_line", "R_Brow_A_ctrl",
                    "R_InnBrow_A_ctrl", "R_MidBrow_A_ctrl", "R_OutBrow_A_ctrl",
                    "R_InnBrow_A_ctrl_R_MidBrow_A_ctrl_line", "R_InnBrow_A_ctrl_R_MidBrow_A_ctrl_line",
                    "R_MidBrow_A_ctrl_R_OutBrow_A_ctrl_line", "R_MidBrow_A_ctrl_R_OutBrow_A_ctrl_line",
                    "M_UpLip_A_ctrl", "L_UpCheek_A_ctrl", "R_UpCheek_A_ctrl", "M_Mouth_A_ctrl", "M_Jaw_A_ctrl",
                    "M_LoTeeth_A_ctrl_handle", "M_LoTeethMid_A_ctrl_handle", "L_LoTeeth1_A_ctrl_handle",
                    "R_LoTeeth1_A_ctrl_handle", "M_Nose_A_ctrl", "M_NoseTip_A_ctrl", "M_UpTeeth_A_ctrl_handle",
                    "M_UpTeethMid_A_ctrl_handle", "L_UpTeeth1_A_ctrl_handle", "R_UpTeeth1_A_ctrl_handle",
                    "L_Ear1_A_ctrl", "L_Ear2_A_ctrl", "R_Ear1_A_ctrl", "R_Ear2_A_ctrl", "M_JawSS_A_ctrl", "curve899",
                    "curve900", "curve901", "curve902", "curve903", "curve904", "curve905", "curve906", "curve907",
                    "curve908", "curve909", "M_Phoneme_A_frame", "M_Phoneme_A_ctrl", "M_Expression_A_frame",
                    "M_Expression_A_ctrl", "M_Expression_A_ctrl", "M_Expression_A_ctrl", "M_Expression_A_ctrl",
                    "M_Expression_A_ctrl", "M_Expression_A_ctrl", "M_Expression_A_ctrl", "M_Expression_A_ctrl",
                    "M_Expression_A_ctrl", "M_UpTeeth_A_ctrl", "M_UpTeeth_A_ctrl", "M_UpTeeth_A_ctrl",
                    "L_UpTeeth1_A_ctrl", "M_UpTeethMid_A_ctrl", "R_UpTeeth1_A_ctrl", "M_LoTeeth_A_ctrl",
                    "M_LoTeeth_A_ctrl", "M_LoTeeth_A_ctrl", "L_LoTeeth1_A_ctrl", "M_LoTeethMid_A_ctrl",
                    "R_LoTeeth1_A_ctrl", "L_UpLidInn_A_ctrl", "L_UpLidMid_A_ctrl", "L_UpLidOut_A_ctrl",
                    "L_LoLidInn_A_ctrl", "L_LoLidMid_A_ctrl", "L_LoLidOut_A_ctrl", "L_UpRingInn_A_ctrl",
                    "L_UpRingMid_A_ctrl", "L_UpRingOut_A_ctrl", "L_LoRingInn_A_ctrl", "L_LoRingMid_A_ctrl",
                    "L_LoRingOut_A_ctrl", "L_EyeCornerInn1_A_ctrl", "L_EyeCornerOut1_A_ctrl", "L_EyeCornerInn2_A_ctrl",
                    "L_EyeCornerOut2_A_ctrl", "L_UpLidSec1_A_ctrl", "L_UpLidSec2_A_ctrl", "L_UpLidSec3_A_ctrl",
                    "L_UpLidSec4_A_ctrl", "L_UpLidSec5_A_ctrl", "L_LoLidSec1_A_ctrl", "L_LoLidSec2_A_ctrl",
                    "L_LoLidSec3_A_ctrl", "L_LoLidSec4_A_ctrl", "L_LoLidSec5_A_ctrl", "L_UpRingSec1_A_ctrl",
                    "L_UpRingSec2_A_ctrl", "L_UpRingSec3_A_ctrl", "L_UpRingSec4_A_ctrl", "L_UpRingSec5_A_ctrl",
                    "L_LoRingSec1_A_ctrl", "L_LoRingSec2_A_ctrl", "L_LoRingSec3_A_ctrl", "L_LoRingSec4_A_ctrl",
                    "L_LoRingSec5_A_ctrl", "R_UpLidInn_A_ctrl", "R_UpLidMid_A_ctrl", "R_UpLidOut_A_ctrl",
                    "R_LoLidInn_A_ctrl", "R_LoLidMid_A_ctrl", "R_LoLidOut_A_ctrl", "R_UpRingInn_A_ctrl",
                    "R_UpRingMid_A_ctrl", "R_UpRingOut_A_ctrl", "R_LoRingInn_A_ctrl", "R_LoRingMid_A_ctrl",
                    "R_LoRingOut_A_ctrl", "R_EyeCornerInn1_A_ctrl", "R_EyeCornerOut1_A_ctrl", "R_EyeCornerInn2_A_ctrl",
                    "R_EyeCornerOut2_A_ctrl", "R_UpLidSec1_A_ctrl", "R_UpLidSec2_A_ctrl", "R_UpLidSec3_A_ctrl",
                    "R_UpLidSec4_A_ctrl", "R_UpLidSec5_A_ctrl", "R_LoLidSec1_A_ctrl", "R_LoLidSec2_A_ctrl",
                    "R_LoLidSec3_A_ctrl", "R_LoLidSec4_A_ctrl", "R_LoLidSec5_A_ctrl", "R_UpRingSec1_A_ctrl",
                    "R_UpRingSec2_A_ctrl", "R_UpRingSec3_A_ctrl", "R_UpRingSec4_A_ctrl", "R_UpRingSec5_A_ctrl",
                    "R_LoRingSec1_A_ctrl", "R_LoRingSec2_A_ctrl", "R_LoRingSec3_A_ctrl", "R_LoRingSec4_A_ctrl",
                    "R_LoRingSec5_A_ctrl", "L_BrowSec1_A_ctrl", "L_BrowSec2_A_ctrl", "L_BrowSec3_A_ctrl",
                    "L_BrowSec4_A_ctrl", "L_BrowSec5_A_ctrl", "L_BrowSec6_A_ctrl", "R_BrowSec1_A_ctrl",
                    "R_BrowSec2_A_ctrl", "R_BrowSec3_A_ctrl", "R_BrowSec4_A_ctrl", "R_BrowSec5_A_ctrl",
                    "R_BrowSec6_A_ctrl", "M_MidBrow_A_ctrl", "L_UpLash1_A_ctrl", "L_UpLash2_A_ctrl", "L_UpLash3_A_ctrl",
                    "L_UpLash4_A_ctrl", "L_UpLash5_A_ctrl", "L_LoLash1_A_ctrl", "L_LoLash2_A_ctrl", "L_LoLash3_A_ctrl",
                    "L_LoLash4_A_ctrl", "L_LoLash5_A_ctrl", "R_UpLash1_A_ctrl", "R_UpLash2_A_ctrl", "R_UpLash3_A_ctrl",
                    "R_UpLash4_A_ctrl", "R_UpLash5_A_ctrl", "R_LoLash1_A_ctrl", "R_LoLash2_A_ctrl", "R_LoLash3_A_ctrl",
                    "R_LoLash4_A_ctrl", "R_LoLash5_A_ctrl", "R_UpLipMain1_A_ctrl", "M_UpLipMain1_A_ctrl",
                    "L_UpLipMain1_A_ctrl", "R_UpLipSec4_A_ctrl", "R_UpLipSec3_A_ctrl", "R_UpLipSec2_A_ctrl",
                    "R_UpLipSec1_A_ctrl", "M_UpLipSec1_A_ctrl", "L_UpLipSec1_A_ctrl", "L_UpLipSec2_A_ctrl",
                    "L_UpLipSec3_A_ctrl", "L_UpLipSec4_A_ctrl", "M_LoLip_A_ctrl", "R_LoLipMain1_A_ctrl",
                    "M_LoLipMain1_A_ctrl", "L_LoLipMain1_A_ctrl", "R_LoLipSec4_A_ctrl", "R_LoLipSec3_A_ctrl",
                    "R_LoLipSec2_A_ctrl", "R_LoLipSec1_A_ctrl", "M_LoLipSec1_A_ctrl", "L_LoLipSec1_A_ctrl",
                    "L_LoLipSec2_A_ctrl", "L_LoLipSec3_A_ctrl", "L_LoLipSec4_A_ctrl", "L_NasolabialFold_A_ctrl",
                    "L_CheekA_A_ctrl", "L_JawUpB_A_ctrl", "R_NasolabialFold_A_ctrl", "R_CheekA_A_ctrl",
                    "R_JawUpB_A_ctrl", "M_JawUpA_A_ctrl", "L_UpCheekInn_A_ctrl", "L_UpCheekMid_A_ctrl",
                    "L_UpCheekOut_A_ctrl", "L_Cheek_A_ctrl", "M_Chin_A_ctrl", "M_JawA_A_ctrl", "L_CheekB_A_ctrl",
                    "L_CheekC_A_ctrl", "L_JawB_A_ctrl", "L_JawC_A_ctrl", "L_JawD_A_ctrl", "R_UpCheekInn_A_ctrl",
                    "R_UpCheekMid_A_ctrl", "R_UpCheekOut_A_ctrl", "R_Cheek_A_ctrl", "R_CheekB_A_ctrl",
                    "R_CheekC_A_ctrl", "R_JawB_A_ctrl", "R_JawC_A_ctrl", "R_JawD_A_ctrl", "L_Mouth_A_ctrl",
                    "R_Mouth_A_ctrl", "L_Nose_A_ctrl", "M_NoseMid_A_ctrl", "L_Nostril_A_ctrl", "R_Nostril_A_ctrl",
                    "R_Nose_A_ctrl", "M_Tongue1_A_ctrl", "M_Tongue2_A_ctrl", "M_Tongue3_A_ctrl", "M_Tongue4_A_ctrl",
                    "M_Tongue5_A_ctrl", "M_Tongue6_A_ctrl", "Master_ctrl", "Local_ctrl", "Root_ctrl", "Head_ctrl",
                    "C_Head_poseBase_C_Head_Left_line", "C_Head_poseBase_C_Head_Right_line",
                    "C_Head_poseBase_C_Head_Front_line", "C_Head_poseBase_C_Head_Back_line", "Neck_curve", "Neck_curve",
                    "NeckFk01_ctrl", "Body_ctrl", "Chest_ctrl", "C_Neck_poseBase_C_Neck_Left_line",
                    "C_Neck_poseBase_C_Neck_Right_line", "C_Neck_poseBase_C_Neck_Front_line",
                    "C_Neck_poseBase_C_Neck_Back_line", "TorsoFk00_ctrl", "TorsoFk01_ctrl", "TorsoFk02_ctrl",
                    "C_Torso2_poseBase_C_Torso2_Left_line", "C_Torso2_poseBase_C_Torso2_Right_line",
                    "C_Torso2_poseBase_C_Torso2_Front_line", "C_Torso2_poseBase_C_Torso2_Back_line",
                    "C_Torso1_poseBase_C_Torso1_Left_line", "C_Torso1_poseBase_C_Torso1_Right_line",
                    "C_Torso1_poseBase_C_Torso1_Front_line", "C_Torso1_poseBase_C_Torso1_Back_line", "Hip_ctrl",
                    "L_Hip_ctrl", "L_Hip_poseBase_L_Hip_Left_line", "L_Hip_poseBase_L_Hip_Right_line",
                    "L_Hip_poseBase_L_Hip_Front_line", "L_Hip_poseBase_L_Hip_Back_line",
                    "L_Hip_poseBase_L_Hip_FrontLeft_line", "L_Hip_poseBase_L_Hip_FrontRight_line",
                    "L_Hip_poseBase_L_Hip_BackLeft_line", "L_Hip_poseBase_L_Hip_BackRight_line", "R_Hip_ctrl",
                    "R_Hip_poseBase_R_Hip_Left_line", "R_Hip_poseBase_R_Hip_Right_line",
                    "R_Hip_poseBase_R_Hip_Front_line", "R_Hip_poseBase_R_Hip_Back_line",
                    "R_Hip_poseBase_R_Hip_FrontLeft_line", "R_Hip_poseBase_R_Hip_FrontRight_line",
                    "R_Hip_poseBase_R_Hip_BackLeft_line", "R_Hip_poseBase_R_Hip_BackRight_line", "SpineIk_ctrl",
                    "Visibility", "Visibility", "Visibility", "Visibility", "C_Torso_poseBase_C_Torso_Left_line",
                    "C_Torso_poseBase_C_Torso_Right_line", "C_Torso_poseBase_C_Torso_Front_line",
                    "C_Torso_poseBase_C_Torso_Back_line", "back_curve", "back_curve", "L_ArmPoleVec01_ctrl",
                    "L_ArmPoleVec01_ctrl_L_ArmIk02_drv_line", "L_ArmPoleVec01_ctrl_L_ArmIk02_drv_line",
                    "L_ArmSettings_ctrl", "L_ArmStateFk_curve1", "L_ArmStateFk_curve2", "L_ArmStateIk_curve1",
                    "L_ArmStateIk_curve2", "L_Index03_ctrl", "L_Index02_ctrl", "L_Index01_ctrl", "L_Index00_ctrl",
                    "L_Middle03_ctrl", "L_Middle02_ctrl", "L_Middle01_ctrl", "L_Middle00_ctrl", "L_Ring03_ctrl",
                    "L_Ring02_ctrl", "L_Ring01_ctrl", "L_Ring00_ctrl", "L_Pinky03_ctrl", "L_Pinky02_ctrl",
                    "L_Pinky01_ctrl", "L_Pinky00_ctrl", "L_Thumb03_ctrl", "L_Thumb02_ctrl", "L_Thumb01_ctrl",
                    "L_ArmB_BendStart_ctrl", "L_ArmB_BendMid_ctrl", "L_ArmB_BendEnd_crv", "L_ArmA_BendStart_crv",
                    "L_ArmA_BendMid_ctrl", "L_ArmA_BendEnd_crv", "L_ArmFk03_ctrl", "L_ArmFk02_ctrl", "L_ArmFk01_ctrl",
                    "L_ArmIk01_ctrl", "L_Wrist_poseBase_L_Wrist_Up_line", "L_Wrist_poseBase_L_Wrist_Down_line",
                    "L_Wrist_poseBase_L_Wrist_Front_line", "L_Wrist_poseBase_L_Wrist_Back_line", "R_ArmPoleVec01_ctrl",
                    "R_ArmPoleVec01_ctrl_R_ArmIk02_drv_line", "R_ArmPoleVec01_ctrl_R_ArmIk02_drv_line",
                    "R_ArmSettings_ctrl", "R_ArmStateFk_curve1", "R_ArmStateFk_curve2", "R_ArmStateIk_curve1",
                    "R_ArmStateIk_curve2", "R_Index03_ctrl", "R_Index02_ctrl", "R_Index01_ctrl", "R_Index00_ctrl",
                    "R_Middle03_ctrl", "R_Middle02_ctrl", "R_Middle01_ctrl", "R_Middle00_ctrl", "R_Ring03_ctrl",
                    "R_Ring02_ctrl", "R_Ring01_ctrl", "R_Ring00_ctrl", "R_Pinky03_ctrl", "R_Pinky02_ctrl",
                    "R_Pinky01_ctrl", "R_Pinky00_ctrl", "R_Thumb03_ctrl", "R_Thumb02_ctrl", "R_Thumb01_ctrl",
                    "R_ArmB_BendStart_ctrl", "R_ArmB_BendMid_ctrl", "R_ArmB_BendEnd_crv", "R_ArmA_BendStart_crv",
                    "R_ArmA_BendMid_ctrl", "R_ArmA_BendEnd_crv", "R_ArmFk03_ctrl", "R_ArmFk02_ctrl", "R_ArmFk01_ctrl",
                    "R_ArmIk01_ctrl", "R_Wrist_poseBase_R_Wrist_Up_line", "R_Wrist_poseBase_R_Wrist_Down_line",
                    "R_Wrist_poseBase_R_Wrist_Front_line", "R_Wrist_poseBase_R_Wrist_Back_line",
                    "L_Shoulder_poseBase_L_Shoulder_Up_line", "L_Shoulder_poseBase_L_Shoulder_Down_line",
                    "L_Shoulder_poseBase_L_Shoulder_Front_line", "L_Shoulder_poseBase_L_Shoulder_Back_line",
                    "L_Shoulder_poseBase_L_Shoulder_FrontUp_line", "L_Shoulder_poseBase_L_Shoulder_FrontDown_line",
                    "L_Shoulder_poseBase_L_Shoulder_BackUp_line", "L_Shoulder_poseBase_L_Shoulder_BackDown_line",
                    "L_Clavicle_ctrl", "R_Shoulder_poseBase_R_Shoulder_Up_line",
                    "R_Shoulder_poseBase_R_Shoulder_Down_line", "R_Shoulder_poseBase_R_Shoulder_Front_line",
                    "R_Shoulder_poseBase_R_Shoulder_Back_line", "R_Shoulder_poseBase_R_Shoulder_FrontUp_line",
                    "R_Shoulder_poseBase_R_Shoulder_FrontDown_line", "R_Shoulder_poseBase_R_Shoulder_BackUp_line",
                    "R_Shoulder_poseBase_R_Shoulder_BackDown_line", "R_Clavicle_ctrl", "L_LegPoleVec01_ctrl",
                    "L_LegPoleVec01_ctrl_L_Leg02_drv_line", "L_LegPoleVec01_ctrl_L_Leg02_drv_line", "L_Toe_ctrl",
                    "L_LegSettings_ctrl", "L_LegStateFk_curve1", "L_LegStateFk_curve2", "L_LegStateIk_curve1",
                    "L_LegStateIk_curve2", "L_LegB_BendStart_ctrl", "L_LegB_BendMid_ctrl", "L_LegB_BendEnd_crv",
                    "L_LegA_BendStart_crv", "L_LegA_BendMid_ctrl", "L_LegA_BendEnd_crv", "L_LegFk01_ctrl",
                    "L_LegFk02_ctrl", "L_LegFk03_ctrl", "L_LegIk01_ctrl", "L_Ball_ctrl",
                    "L_Ankle_poseBase_L_Ankle_Left_line", "L_Ankle_poseBase_L_Ankle_Right_line",
                    "L_Ankle_poseBase_L_Ankle_Front_line", "L_Ankle_poseBase_L_Ankle_Back_line", "R_LegPoleVec01_ctrl",
                    "R_LegPoleVec01_ctrl_R_Leg02_drv_line", "R_LegPoleVec01_ctrl_R_Leg02_drv_line", "R_Toe_ctrl",
                    "R_LegSettings_ctrl", "R_LegStateFk_curve1", "R_LegStateFk_curve2", "R_LegStateIk_curve1",
                    "R_LegStateIk_curve2", "R_LegB_BendStart_ctrl", "R_LegB_BendMid_ctrl", "R_LegB_BendEnd_crv",
                    "R_LegA_BendStart_crv", "R_LegA_BendMid_ctrl", "R_LegA_BendEnd_crv", "R_LegFk01_ctrl",
                    "R_LegFk02_ctrl", "R_LegFk03_ctrl", "R_LegIk01_ctrl", "R_Ball_ctrl",
                    "R_Ankle_poseBase_R_Ankle_Left_line", "R_Ankle_poseBase_R_Ankle_Right_line",
                    "R_Ankle_poseBase_R_Ankle_Front_line", "R_Ankle_poseBase_R_Ankle_Back_line", "NeckMid_ctrl",
                    "L_Clavicle_UD_jnt_psd_follow_handle", "L_Clavicle_UD_jnt_psd_parent_handle",
                    "L_Arm01_drv_psd_follow_handle", "L_Arm01_drv_psd_parent_handle", "L_ArmB_01_jnt_psd_follow_handle",
                    "L_ArmB_01_jnt_psd_parent_handle", "L_Hand_jnt_psd_follow_handle", "L_Hand_jnt_psd_parent_handle",
                    "L_Leg01_drv_psd_follow_handle", "L_Leg01_drv_psd_parent_handle", "L_LegB_01_jnt_psd_follow_handle",
                    "L_LegB_01_jnt_psd_parent_handle", "L_Foot_jnt_psd_follow_handle", "L_Foot_jnt_psd_parent_handle",
                    "L_Toe_jnt_psd_follow_handle", "L_Toe_jnt_psd_parent_handle", "R_Clavicle_UD_jnt_psd_follow_handle",
                    "R_Clavicle_UD_jnt_psd_parent_handle", "R_Arm01_drv_psd_follow_handle",
                    "R_Arm01_drv_psd_parent_handle", "R_ArmB_01_jnt_psd_follow_handle",
                    "R_ArmB_01_jnt_psd_parent_handle", "R_Hand_jnt_psd_follow_handle", "R_Hand_jnt_psd_parent_handle",
                    "R_Leg01_drv_psd_follow_handle", "R_Leg01_drv_psd_parent_handle", "R_LegB_01_jnt_psd_follow_handle",
                    "R_LegB_01_jnt_psd_parent_handle", "R_Foot_jnt_psd_follow_handle", "R_Foot_jnt_psd_parent_handle",
                    "R_Toe_jnt_psd_follow_handle", "R_Toe_jnt_psd_parent_handle", "Chest_jnt_psd_follow_handle",
                    "Chest_jnt_psd_parent_handle", "Neck01_jnt_psd_follow_handle", "Neck01_jnt_psd_parent_handle",
                    "Torso1_jnt_psd_follow_handle", "Torso1_jnt_psd_parent_handle", "Head01_jnt_psd_follow_handle",
                    "Head01_jnt_psd_parent_handle"]


def mrDag():
    nodes = mc.ls('mr_display_driver_dag', '*mr_display_driver_dag*')
    if nodes:
        mc.delete(nodes)
    return True


def camsLightsImgPlanes():
    nodes = mc.ls(type='imagePlane') + mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
           'topShape',
           'frontShape',
           'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)

    if nodes:
        return
    return True


def camsLightsImgPlanesfix():
    nodes = mc.ls(type='imagePlane')
    if nodes:
        mc.delete(nodes)
    nodes = mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
           'topShape',
           'frontShape',
           'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)

    for n in nodes:
        xf = mc.listRelatives(n, p=1)
        mc.delete(xf)


def checkCtrls():
    timeline_ctrls = []
    for ctrl in timeline_ctrls:
        if not mc.objExists(ctrl):
            return False
    return True


def checkBadShapes():
    badones = []
    nodes = os.environ['RIGCHECK_MODELHI'].split(' ')

    for node in nodes:
        if not mc.objExists(node):
            print(node + ' no longer exists! Make sure you use the sane rig throughout the check process!')

        shapes = mc.listRelatives(node, s=1, ni=1)
        if len(shapes) > 1:
            badones.append(node)

        for shape in shapes:
            if not shape == node + 'Shape':
                badones.append(shape)

    if badones:
        mc.select(badones)
        msg = 'Bad shape nodes found:\n'
        msg += '\n'.join(badones)
        return str(msg)

    return True


def checkSets():
    rset = mc.ls('geoSet_*', type='objectSet')
    if rset:
        return True


def createSet(text, setType, objects):
    mc.select(objects)
    newset = mc.sets(name=text)
    mc.addAttr(newset, ln="setName", dt="string")
    mc.addAttr(newset, ln="setType", dt="string")
    mc.setAttr("{0}.setName".format(newset), text, type="string")
    mc.setAttr("{0}.setType".format(newset), setType, type="string")
    mc.setAttr("{0}.setName".format(newset), lock=True)
    mc.setAttr("{0}.setType".format(newset), lock=True)
    return newset


def fixSets():
    checkSets(1)


def playCheck():
    test = mc.confirmDialog(title='Rig Check Animation',
                            message='Play Animation?\n\nYour rig seems legit!\nDo you want to run through a quick animation to test your rig?\nHit escape to cancel at any time.',
                            button=['Yes', 'Skip'],
                            defaultButton='Yes',
                            cancelButton='Skip',
                            dismissString='Skip')
    if test == 'Yes':
        result = play()
        return result
    return True


def playCam(topnode):
    mel.eval('''setNamedPanelLayout "Single Perspective View"; updateToolbox();
    optionVar -query animateRollViewCompass;
    viewSet -home;
    viewSet -p -an 1 |persp|perspShape;''')

    tmp = mc.createNode('transform', n='perspPar')
    tmp2 = mc.createNode('transform', p='perspPar')
    mc.pointConstraint(topnode, tmp)

    bb = mc.exactWorldBoundingBox(topnode, ii=1)
    pos = [
        (bb[3] - bb[0]),
        (bb[4] - bb[1]) * 2,
        (bb[5] - bb[2])]

    cube = mc.polyCube(ch=0)
    mc.xform(cube, r=1, s=pos)

    mc.select(cube)
    mel.eval('fitPanel -selected;')
    pos = mc.xform('persp', q=1, a=1, t=1)
    mc.xform('persp', a=1, t=[pos[0] * 1.5, pos[1] * 1.5, pos[2] * 1.5])
    mc.delete(cube)

    mc.delete(mc.pointConstraint('persp', tmp2))
    mc.pointConstraint(tmp2, 'persp')
    mc.select(cl=1)


def killCam():
    mc.delete('perspPar')


def play(delay=0.1):
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar(gMainProgressBar, e=True, bp=True, ii=True, st='Running Rig Test ...', maxValue=3)

    topnode = ''
    rigtype = ''
    nodes = mc.ls('worldA_ctrl', 'worldTransform')
    if nodes and mc.objExists(nodes[0] + '.UniformScale') and mc.objExists(nodes[0] + '.modelDisplay'):
        topnode = nodes[0]
        rigtype = 'ftrack'

    elif mc.ls('global_CTRL'):
        nodes = mc.ls('global_CTRL')
        if nodes and mc.objExists(nodes[0] + '.modelType') and mc.objExists(nodes[0] + '.skeletonType'):
            topnode = nodes[0]
            rigtype = 'hub'
    else:
        nodes = mc.ls(sl=1)
        if nodes:
            topnode = nodes[0]

    if not topnode:
        msg = 'If your rig was not built using the HUB Tools or the LA Rig Tools,\nselect the top transformable node of your rig and re-run the checks.\n\nMake sure the translate, rotate and scale channels are all unlocked.'
        mc.confirmDialog(message=msg, title='Select Top Node', icon='information')
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        return

    # play through anim 
    mc.select(cl=1)
    mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])

    playCam(topnode)

    mc.inViewMessage(amg='Testing rig <hl>uniform scale</hl>.', pos='botCenter', fade=1)
    mc.refresh()

    for i in reversed(range(1, 11)):
        mc.xform(topnode, a=1, s=[i * .1, i * .1, i * .1])
        time.sleep(delay)
        mc.refresh()

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 11):
        time.sleep(delay)
        mc.refresh()
        mc.xform(topnode, a=1, s=[i * .1, i * .1, i * .1])

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 9):
        time.sleep(delay)
        mc.refresh()
        mc.xform(topnode, a=1, s=[i, i, i])

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(1, 9)):
        time.sleep(delay)
        mc.refresh()

        mc.xform(topnode, a=1, s=[i, i, i])

    mc.inViewMessage(amg='Testing rig <hl>world transform & rotate</hl>.', pos='botCenter', fade=1)
    mc.refresh()

    bb = mc.exactWorldBoundingBox(topnode)
    mult = ((bb[3] + bb[4] + bb[5]) / 3) - ((bb[0] + bb[1] + bb[2]) / 3)

    mc.progressBar(gMainProgressBar, edit=True, step=1)
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(0, 21):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.t', i * mult, i * mult, -i * mult)

    for i in reversed(range(0, 21)):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.t', i * mult, i * mult, -i * mult)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.ry', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.rz', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode + '.rx', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode + '.ry', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode + '.rz', i * 20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 1)):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode + '.t', i * mult, i * mult, -i * mult)

    mc.progressBar(gMainProgressBar, edit=True, step=1)
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    if rigtype == 'hub':

        mc.inViewMessage(amg='Testing visibility switch for <hl>model.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.modelVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelType', 0)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
            mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage(amg='Testing visibility switch for <hl>skeleton.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.skeletonVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.skeletonVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.skeletonType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.skeletonType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.skeletonType', 0)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
            mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage(amg='Testing visibility switch for <hl>controls.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.controlVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.controlVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.controlType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.controlType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.controlType', 0)
        time.sleep(1)
        mc.refresh()

    if rigtype == 'ftrack':

        mc.inViewMessage(amg='Testing visibility switch for <hl>model.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.modelDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelDisplay', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.modelDisplay', 1)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
            mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage(amg='Testing visibility switch for <hl>skeleton.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.jointDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.jointDisplay', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.jointDisplay', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.jointDisplay', 0)

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
            mc.inViewMessage(amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage(amg='Testing visibility switch for <hl>controls.</hl>.', pos='botCenter', fade=1)
        mc.setAttr(topnode + '.ctrlDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode + '.ctrlDisplay', 1)
        time.sleep(1)
        mc.refresh()

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
    mc.inViewMessage(amg='<hl>Finished. All good?</hl> Go forth and publish!', pos='botCenter', fade=1)
    killCam()
    return True


def createSelectUI(winTitle, msg, badNodes, func=None, fix=False):
    """ Main UI func. """
    winName = "fixWindow"
    if window(winName, q=True, ex=True):
        deleteUI(winName)
    window(winName, title=winTitle, widthHeight=(500, 500))
    scrollArea = scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16,
                              childResizable=True)
    if msg is not None:
        msgLay = columnLayout(adjustableColumn=True)
        scrollField(editable=False, wordWrap=True, text=msg, height=200)
        separator(style='none')
    mainLayout = columnLayout(adjustableColumn=True)
    if not len(badNodes) == 0:
        iconTextButton(style='textOnly', label='---select all---', command=lambda: select(badNodes))
        for eachNode in badNodes:
            iconTextButton(style='textOnly', label=str(eachNode), command=partial(selectNode, eachNode))
        if func and fix:
            iconTextButton(style='textOnly', label='Fix', command=func)

    showWindow(winName)


def selectNode(node, *args):
    select(node, r=True)


def checkResult(**kwargs):
    d = {'allowPublish': True,
         'msg': '',
         'nodes': [],
         'warning': False}
    d.update(kwargs)
    return d


def getSceneCtrls(*args):
    ctrlList = []
    iter_nodes = om.MItDependencyNodes(om.MFn.kNurbsCurve)
    # 遍历所有节点
    while not iter_nodes.isDone():
        # 获取当前节点的 MObject
        mobject = iter_nodes.thisNode()
        # om.MDagPath.partialPathName
        # 获取曲线的变换节点
        dag_path = om.MDagPath.getAPathTo(mobject)
        transform_mobject = dag_path.transform()

        # 创建 MFnTransform
        transform_name = om.MFnDependencyNode(transform_mobject).name()
        ctrlList.append(transform_name)
        # 继续下一个节点
        iter_nodes.next()
    return ctrlList


def get_all_children(parent_name):
    """
    递归获取物体下所有层级的子物体
    :param parent_name: 父物体名称
    :return: 所有子物体名称列表
    """

    def traverse(dag_path, result):
        for i in range(dag_path.childCount()):
            child_mobj = dag_path.child(i)
            child_dag_path = om.MDagPath(dag_path)
            child_dag_path.push(child_mobj)

            result.append(child_mobj)

            # 如果是变换节点，继续递归
            if child_mobj.hasFn(om.MFn.kTransform):
                traverse(child_dag_path, result)

    selection_list = om.MSelectionList()
    selection_list.add(parent_name)

    dag_path = selection_list.getDagPath(0)

    all_children = []
    traverse(dag_path, all_children)
    return all_children


def getBranchCtrls():
    """
    get branch ctrls
    :return:
    """
    curve_names = []
    if cmds.objExists("BranchSystem"):
        object_name = "BranchSystem"

        # 创建 MSelectionList
        selection_list = om.MSelectionList()

        # 将物体名称添加到选择列表
        selection_list.add(object_name)

        # 获取 MDagPath
        dag_path = selection_list.getDagPath(0)

        # 存储曲线名称

        ch_mObjList = get_all_children(object_name)
        for obj in ch_mObjList:
            child_mobject = obj

            # 检查是否为 NURBS 曲线
            if child_mobject.hasFn(om.MFn.kNurbsCurve):
                # 创建子节点的 MDagPath
                child_dag_path = om.MDagPath(dag_path)
                child_dag_path.push(child_mobject)  # 将子节点添加到路径
                trans = child_dag_path.transform()
                # 获取曲线名称
                curve_names.append(om.MFnDependencyNode(trans).name())
    return curve_names


def getCtrlDefaultValue(*args, **kwargs):
    errorObjs = []
    iter_nodes = om.MItDependencyNodes(om.MFn.kNurbsCurve)
    # 遍历所有节点
    while not iter_nodes.isDone():
        # 获取当前节点的 MObject
        mobject = iter_nodes.thisNode()
        # om.MDagPath.partialPathName
        # 获取曲线的变换节点
        dag_path = om.MDagPath.getAPathTo(mobject)
        transform_mobject = dag_path.transform()

        # 创建 MFnTransform
        transform_fn = om.MFnTransform(transform_mobject)
        transform_name = om.MFnDependencyNode(transform_mobject).name()

        default_translate = om.MVector(0.00, 0.00, 0.00)
        default_rotate = om.MEulerRotation(0.00, 0.00, 0.00)
        default_scale = [1.00, 1.00, 1.00]

        translate = transform_fn.translation(om.MSpace.kTransform)
        rotate = transform_fn.rotation()
        scale = transform_fn.scale()

        is_default = (om.MVector(round(translate.x, 2), round(translate.y, 2),
                                 round(translate.z, 2)) == default_translate and
                      om.MEulerRotation(round(rotate.x, 2), round(rotate.y, 2),
                                        round(rotate.z, 2)) == default_rotate and
                      [round(scale[0], 2), round(scale[1], 2), round(scale[2], 2)] == default_scale)
        if not is_default and transform_name.endswith("_ctrl"):
            errorObjs.append(transform_name)
        # 继续下一个节点
        iter_nodes.next()
    issues = list(set(errorObjs))
    if not issues:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg=u'# 有数值控制器---\n' + str(issues),
                           nodes=issues)


def checkCtrlDefaultValue(*args, **kwargs):
    """检查控制器是否为默认值"""
    result = getCtrlDefaultValue()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def restoreSelectionCtrlValue(ctrlList):
    attrs = ['translateX',
             'translateY',
             'translateZ',
             'rotateX',
             'rotateY',
             'rotateZ']
    scaleAttrs = ['scaleX', 'scaleY', 'scaleZ']
    [cmds.setAttr("%s.%s" % (ctrl, attr), 0) for attr in attrs for ctrl in ctrlList if
     not cmds.getAttr("%s.%s" % (ctrl, attr), lock=1)]
    [cmds.setAttr("%s.%s" % (ctrl, attr), 1) for attr in scaleAttrs for ctrl in ctrlList if
     not cmds.getAttr("%s.%s" % (ctrl, attr), lock=1)]


def fixCtrlDefaultValue(*args, **kwargs):
    result = getCtrlDefaultValue()
    if result['nodes']:
        createSelectUI("FixCtrlValue", result['msg'], result['nodes'],
                       partial(restoreSelectionCtrlValue, result['nodes']), fix=True)


def getControllerAttributesWithInput_elo():
    issues = []
    controllers = getSceneCtrls()
    if not len(controllers) == 0:
        for controller in controllers:
            if objExists('%s.allowPublishWithConnections' % controller) is True:
                continue
            if controller.endswith("_ctrl"):
                attrs = func.listStorableAttrs(controller)
                if attrs is not None:
                    for attr in attrs:
                        input = []
                        input = listConnections('%s.%s' % (controller, attr), s=True, d=False)
                        if input:
                            issues.append(controller)
    issues = set(issues)
    if len(issues) == 0:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg='Those controllers have input connection\n' + str(issues),
                           nodes=issues)


def getControllerAttributesWithInput(*args, **kwargs):
    """获取有约束或被连接的控制器"""
    issues = []
    controllers = getSceneCtrls()
    if not len(controllers) == 0:
        for controller in controllers:
            if objExists('%s.allowPublishWithConnections' % controller) is True:
                continue
            attrs = func.listStorableAttrs(controller)
            if attrs is not None:
                for attr in attrs:
                    input = []
                    input = listConnections('%s.%s' % (controller, attr), s=True, d=False)
                    if input:
                        issues.append(controller)
    issues = set(issues)
    if len(issues) == 0:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg='Those controllers have input connection\n' + str(issues),
                           nodes=issues)


def checkControllerAttributesWithInput(*args, **kwargs):
    """检查有约束或被连接的控制器"""
    result = getControllerAttributesWithInput()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixControllerAttributesWithInput(*args, **kwargs):
    result = getControllerAttributesWithInput()
    if result['nodes']:
        createSelectUI("FixCtrlInputs", result['msg'], result['nodes'], fix=False)


def checkControllerAttributesWithInput_elo():
    result = getControllerAttributesWithInput_elo()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixControllerAttributesWithInput_elo(*args, **kwargs):
    result = getControllerAttributesWithInput_elo()
    if result['nodes']:
        createSelectUI("FixCtrlInputs", result['msg'], result['nodes'], fix=False)


def getInvalidControllerSuffixName():
    issues = []
    ctrlList = getSceneCtrls()
    branchCtrls = getBranchCtrls()
    for ctrl in ctrlList:
        if ctrl not in timeLineCtrlList and not ctrl.endswith("_ctrl") and ctrl not in branchCtrls:
            issues.append(ctrl)
    if len(issues) == 0:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False, msg=u'#有不是以_ctrl命名的控制器，请修改---\n' + str(issues),
                           nodes=issues)


def checkControllerSuffixName():
    result = getInvalidControllerSuffixName()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixControllerSuffixName():
    result = getInvalidControllerSuffixName()
    if result['nodes']:
        createSelectUI("FixCtrlSuffixName", result['msg'], result['nodes'], fix=False)


def getNotDrivenKey(*args, **kw):
    """获取key帧物体 select Not Driven Key """
    ani = ls(type='animCurve')
    keyObjs = []
    for x in ani:
        if objExists(x):
            hasInput = listConnections('%s.input' % x, s=True, d=False, scn=True)
            hasOutput = listConnections('%s.output' % x, s=False, d=True, scn=True)
            if hasInput == [] or hasOutput == []:
                if "scalePower" not in x.name():
                    keyObjs.append(x)

    issues = list(set(keyObjs))
    if len(issues) == 0:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False, msg=u'#有无用的动画曲线，请判断后删除---\n' + str(issues),
                           nodes=issues)


def checkNotDrivenKey(*args, **kwargs):
    """检查有约束或被连接的控制器"""
    result = getNotDrivenKey()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixNotDrivenKey(*args, **kwargs):
    result = getNotDrivenKey()
    if result['nodes']:
        createSelectUI("FixNotDrivenKey", result['msg'], result['nodes'], fix=False)


def getClosedSkin(*args, **kwargs):
    """get closed skin node"""
    issues = []
    skinNodeList = ls(type='skinCluster')
    errorSkin = []
    for skin in skinNodeList:
        if getAttr(skin + '.envelope') == 0:
            errorSkin.append(skin)
            issues.append(skin)

    if not issues:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False, msg=u'# 以下蒙皮节点未打开,请检查-----\n' + str(issues), nodes=issues)


def checkClosedSkin(*args):
    result = getClosedSkin()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixClosedSkin(*args, **kwargs):
    result = getClosedSkin()
    if result['nodes']:
        createSelectUI("FixClosedSkinNodes", result['msg'], result['nodes'], fix=False)


def getNgskinExists(*args, **kwargs):
    """获取ngSkin节点"""
    issues = []
    if versions.current() >= 20220000:
        ngSkinLayerDatas = ls(type="ngst2SkinLayerData")
    else:
        ngSkinLayerDatas = ls(type="ngSkinLayerData")
    if ngSkinLayerDatas:
        issues = ngSkinLayerDatas
        promptStr = u'ngSkin 节点未删除-----'
    if not issues:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False, msg=promptStr + str(issues), nodes=issues)


def checkNgskinExists(*args):
    result = getNgskinExists()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixNgskinExists(*args, **kwargs):
    result = getNgskinExists()
    if result['nodes']:
        createSelectUI("FixClosedSkinNodes", result['msg'], result['nodes'], fix=False)


def getBlendShapeName(*args, **kw):
    """get invalid bs name"""
    errorStr = u'BlendShape命名不规范\n正确命名:模型名_blendShape\n'
    issues = []
    meshShapes = ls(type='mesh')
    for meshShape in meshShapes:
        mesh = meshShape.getParent()
        bsNode = []
        try:
            meshHistory = listHistory(mesh, pdo=True)
            bsNode = ls(meshHistory, type='blendShape')
        except TypeError:
            pass
        if bsNode:
            if bsNode[0] != mesh + '_blendShape':
                issues.append(mesh)

    issues = list(set(issues))
    if not issues:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False, msg=errorStr + str(issues), nodes=issues)


def checkBlendShapeName(*args):
    result = getBlendShapeName()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def renameInvalidBsName(*args):
    inValidMeshList = getBlendShapeName()["nodes"]
    invalidBsNameList = []
    if inValidMeshList:
        for mesh in inValidMeshList:
            bsNodes = mesh.history(type="blendShape")
            if bsNodes:
                try:
                    rename(bsNodes[0], "%s_blendShape" % mesh)
                except:
                    pass


def fixBlendShapeName(*args, **kwargs):
    result = getBlendShapeName()
    if result['nodes']:
        createSelectUI("FixClosedSkinNodes", result['msg'], result['nodes'], func=renameInvalidBsName, fix=True)


def getInvalidSkinJoints():
    """
    蒙皮骨骼是否在指定骨骼链中
    :return:
    """
    geometryList = ls("geometry")
    if len(geometryList) != 1:
        return
    root_jnt = None
    issues = []
    if objExists("Root_jnt"):
        root_jnt = PyNode("Root_jnt")
    elif objExists("Root_M"):
        root_jnt = PyNode("Root_M")
    jointChainList = listRelatives(root_jnt, ad=True, c=True, typ="joint")
    meshList = listRelatives("geometry", children=True,
                             ad=True, type="mesh", ni=True)
    for mesh in meshList:
        skinNodeList = mesh.history(type="skinCluster")
        if skinNodeList:
            skinJoints = skinNodeList[0].influenceObjects()
            for jnt in skinJoints:
                if jnt not in jointChainList:
                    issues.append(mesh.getParent().name())

    issues = list(set(issues))
    if not issues:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg="蒙皮骨骼不规范\n以下模型有蒙皮骨骼不在指定骨骼链中-----请检查是否需要删除:\n" + str(
                               issues),
                           nodes=issues)


def checkInvalidSkinJoints(*args):
    result = getInvalidSkinJoints()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixInvalidSkinJoints(*args, **kwargs):
    result = getInvalidSkinJoints()
    if result['nodes']:
        createSelectUI("FixInvalidSkinJoints", result['msg'], result['nodes'], fix=False)


def getInvalidCtrlRotateOrder():
    """
    胳膊控制器和大腿控制器的rotateOrder是否为xyz
    :return:
    """
    checkCtrlList = ["L_ArmFk01_ctrl", "R_ArmFk01_ctrl",
                     "L_LegFk01_ctrl", "R_LegFk01_ctrl"]
    issues = []
    for ctrl in checkCtrlList:
        if not objExists(ctrl):
            break
        rotOrder = getAttr(ctrl + ".rotationOrder")
        if rotOrder != 0:
            issues.append(ctrl)
    issues = list(set(issues))
    if issues:
        return checkResult(allowPublish=False, msg="以下控制器rotateOrder不是xyz:\n" + str(issues),
                           nodes=issues)
    else:
        return checkResult(allowPublish=True)


def checkInvalidCtrlRotateOrder(*args):
    result = getInvalidCtrlRotateOrder()
    if not result["nodes"]:
        return True
    else:
        print(result['msg'])
        return False


def fixInvalidCtrlRotateOrder(*args):
    result = getInvalidCtrlRotateOrder()
    if result['nodes']:
        createSelectUI("FixInvalidCtrlRotateOrder", result['msg'], result['nodes'],
                       func=lambda: [setAttr(node + ".rotationOrder", 0)
                                     for node in result['nodes']], fix=True)


def checkFollowAttr():
    """
    胳膊FK控制器和头部控制器的follow属性是否打开
    :return:
    """
    checkCtrlList = ['Head_ctrl', 'L_ArmFk01_ctrl', 'R_ArmFk01_ctrl']
    for ctrl in checkCtrlList:
        if not getAttr('%s.followWorld' % ctrl):
            return False
        else:
            return True


def checkArmIKFKSwitch():
    """
    手臂是否切换为FK
    :return:
    """
    for ctrl in ['L_ArmSettings_ctrl', 'R_ArmSettings_ctrl']:
        if not getAttr("%s.fkIkBlend" % ctrl):
            return True
        else:
            return False


def checkLegIKFKSwitch():
    """
    手臂是否切换为FK
    :return:
    """
    for ctrl in ['L_LegSettings_ctrl', 'R_LegSettings_ctrl']:
        if getAttr("%s.fkIkBlend" % ctrl):
            return True
        else:
            return False


def checkPublish():
    if (not checkFollowAttr()) or (not checkArmIKFKSwitch()) or (not checkLegIKFKSwitch()):
        return False
    else:
        return True


def checkEloPublish():
    if (not cmds.objExists("root_base")) or (not cmds.objExists("NeckMid_ctrl")) or (
    not cmds.objExists("Visibility.Body_FK_VIS")):
        return False
    else:
        return True


def fixEloPublish():
    test = mc.confirmDialog(title='Rig Check Publish',
                            message='Do you want to publish your Elo Timeline rigging?.',
                            button=['Yes', 'Cancel'],
                            defaultButton='Yes',
                            cancelButton='Cancel',
                            dismissString='Cancel')
    if test == 'Yes':
        timeline_eio_update.organize_files()


def fixUnPublish():
    test = mc.confirmDialog(title='Rig Check Publish',
                            message='Do you want to publish your Timeline rigging?.',
                            button=['Yes', 'Cancel'],
                            defaultButton='Yes',
                            cancelButton='Cancel',
                            dismissString='Cancel')
    if test == 'Yes':
        PublishByRig()


def PublishByRig():
    sels = cmds.ls(sl=True)

    for ctrl in ['Head_ctrl', 'L_ArmFk01_ctrl', 'R_ArmFk01_ctrl']:
        cmds.setAttr('%s.followWorld' % ctrl, 1)

    for ctrl in ['L_ArmSettings_ctrl', 'R_ArmSettings_ctrl']:
        cmds.setAttr('%s.fkIkBlend' % ctrl, 0)

    for ctrl in ['L_LegSettings_ctrl', 'R_LegSettings_ctrl']:
        cmds.setAttr('%s.fkIkBlend' % ctrl, 1)

    Visibility_zero_Parent = cmds.listRelatives('Visibility_zero', p=True)[0]
    if Visibility_zero_Parent != 'Root_ctrl':
        cmds.parent('Visibility_zero', 'Root_ctrl')

    cmds.setDrivenKeyframe('NeckFk01_ctrl_zero.v', cd="Visibility.head_vis", dv=0, v=0)
    cmds.setDrivenKeyframe('NeckFk01_ctrl_zero.v', cd="Visibility.head_vis", dv=1, v=1)

    if cmds.objExists('L_ArmIk01_ctrl_handHeart_ctrl'):
        for ctrl in ['L_ArmIk01_ctrl_handHeart_ctrl', 'R_ArmIk01_ctrl_handHeart_ctrl']:
            for attr in ['indexIKFK', 'indexFollow', 'middleIKFK', 'middleFollow', 'ringIKFK', 'ringFollow',
                         'pinkyIKFK', 'pinkyFollow']:
                cmds.setAttr('%s.%s' % (ctrl, attr), 0)

        cmds.setDrivenKeyframe('L_ArmIk01_ctrl_handHeart_ctrl_pos_grp.v', cd="Visibility.L_Arm_vis", dv=0, v=0)
        cmds.setDrivenKeyframe('L_ArmIk01_ctrl_handHeart_ctrl_pos_grp.v', cd="Visibility.L_Arm_vis", dv=1, v=1)

        cmds.setDrivenKeyframe('R_ArmIk01_ctrl_handHeart_ctrl_pos_grp.v', cd="Visibility.R_Arm_vis", dv=0, v=0)
        cmds.setDrivenKeyframe('R_ArmIk01_ctrl_handHeart_ctrl_pos_grp.v', cd="Visibility.R_Arm_vis", dv=1, v=1)

    Master_ctrl_Parent = cmds.listRelatives('Master_ctrl', p=True)[0]
    if Master_ctrl_Parent != 'global_ctrl':
        cmds.group('Master_ctrl', n='global_ctrl')

    if cmds.objExists('lf_eye_blink_ctrl'):
        for ctrl in ['lf_eye_blink_ctrl', 'rt_eye_blink_ctrl']:
            for attr in ['upBlink', 'dnBline']:
                lockInfo = cmds.getAttr('%s.%s' % (ctrl, attr), l=True)
                if not lockInfo:
                    cmds.setAttr('%s.%s' % (ctrl, attr), l=True)

    if sels:
        cmds.select(sels)
    else:
        cmds.select(cl=True)


def getInvalidHelperControlNames():
    invalid_helper_control_names = []
    if mc.objExists("BranchSystem"):
        helperNodes = mc.listRelatives("BranchSystem", c=True, ad=True, type="transform")
        for helperNode in helperNodes:
            if cmds.objExists(helperNode + ".follow"):
                if helperNode.endswith("_ctrl"):
                    invalid_helper_control_names.append(helperNode)

    if invalid_helper_control_names:
        return checkResult(allowPublish=False,
                           msg="以下辅助骨骼控制器是以_ctrl结尾,需要修改:\n" + str(invalid_helper_control_names),
                           nodes=invalid_helper_control_names)
    else:
        return checkResult(allowPublish=True)


def checkHelperControlNames():
    result = getInvalidHelperControlNames()
    if not result["nodes"]:
        return True
    else:
        OpenMaya.MGlobal.displayInfo(result['msg'])
        return False


def fixHelperControlNames():
    result = getInvalidHelperControlNames()
    if result['nodes']:
        createSelectUI("FixHelperControlNames", result['msg'], result['nodes'],
                       func=lambda: [mc.rename(node, node.replace("_ctrl", "_con"))
                                     for node in result['nodes']], fix=True)


def getInvalidCtrlNames():
    ctrlList = getSceneCtrls()

    errorObjs = []
    for ctrl in ctrlList:
        if ctrl.endswith("_") or ctrl.startswith("_"):
            if ctrl.endswith("_ctrl"):
                errorObjs.append(ctrl)
    if not errorObjs:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg=u'# 非法控制器名称---\n' + str(errorObjs),
                           nodes=errorObjs)


def checkInvalidCtrlNames():
    result = getInvalidCtrlNames()
    if not result["nodes"]:
        return True
    else:
        OpenMaya.MGlobal.displayInfo(result['msg'])
        return False


def fixInvalidCtrlNames():
    result = getInvalidCtrlNames()
    if result['nodes']:
        createSelectUI("FixInvalidCtrlNames", result['msg'], result['nodes'],
                       func=partial(fixInvalidName, result['nodes']), fix=True)


def fixInvalidName(names):
    for name in names:
        new_name = name
        if name.startswith("_"):
            new_name = name.lstrip("_")
        elif name.endswith("_"):
            new_name = name.rstrip("_")
        mc.rename(name, new_name)


def getInvalidSdkGroupValue():
    errorGrps = []
    attrList = [".translateX", ".translateY", ".translateZ",
                ".rotateX", ".rotateY", ".rotateZ",
                ".scaleX", ".scaleY", ".scaleZ"]
    sdkGrps = cmds.ls("*_sdk", type="transform")
    if sdkGrps:
        for sdk in sdkGrps:
            if cmds.objectType(sdk) != "joint" and sdk != "L_Toe_sdk" and sdk != "R_Toe_sdk":
                invalids = []
                for attr in attrList:
                    if "scale" not in attr:
                        if round(cmds.getAttr(sdk + attr), 2) != 0.00:
                            invalids.append(1)
                    else:
                        if round(cmds.getAttr(sdk + attr), 2) != 1.00:
                            invalids.append(1)
                if invalids:
                    errorGrps.append(sdk)
    if not errorGrps:
        return checkResult(allowPublish=True)
    else:
        return checkResult(allowPublish=False,
                           msg=u'# sdk组上默认值不为0---\n' + str(errorGrps),
                           nodes=errorGrps)


def checkSdkGroupValue():
    result = getInvalidSdkGroupValue()
    if not result["nodes"]:
        return True
    else:
        OpenMaya.MGlobal.displayInfo(result['msg'])
        return False


def fixSdkGroupValue():
    result = getInvalidSdkGroupValue()
    if result['nodes']:
        createSelectUI("FixInvalidSdkValue", result['msg'], result['nodes'], fix=False)
