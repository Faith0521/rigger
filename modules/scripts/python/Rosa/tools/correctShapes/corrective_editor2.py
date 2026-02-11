#coding:utf-8
#AUTHOR: zeng long an
#AUTHOR: wang zi hang
#LAST UPDATE: 08/01/2023

import os
import re
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

pyPath = __file__

correctiveDataDict={
    #clavicle bridge
    'lf_clavicle_ctrl':{
        'preName' : 'lf_clavicle',
        'axis' :['up_60','bottom_60'],
        'rotate' : [(0,0,60),(0,0,-60)],
        'driverAttr' : ['L_clavicle_bridge.up_driver','L_clavicle_bridge.bottom_driver'],
        'bridge' : 'L_clavicle_grp'
        },
    'rt_clavicle_ctrl':{
        'preName' : 'rt_clavicle',
        'axis' :['up_60','bottom_60'],
        'rotate' : [(0,0,60),(0,0,-60)],
        'driverAttr' : ['R_clavicle_bridge.up_driver','R_clavicle_bridge.bottom_driver'],
        'bridge' : 'R_clavicle_grp'
        },
    #arm bridge
    'lf_arm_ctrl':{
        'preName' : 'lf_arm',
        'axis' :['up_60','up_90','down_55','down_80','front_60','front_90','front_110','back_90','frontUp_90','backUp_90','frontDown_90','backDown_90'],
        'rotate' : [(0,0,60),(0,0,90),(0,0,-55),(0,0,-80),(0,-60,0),(0,-90,0),(0,-110,0),(0,90,0),#4
                    (-45.0, -45.0, 90.0),(45.0, 45.0, 90.0),#upper
                    (45.0, -45.0, -90.0),(-45.0, 45.0, -90.0)],#lower
        'driverAttr' : ['L_arm_bridge.up_driver','L_arm_bridge.up_driver','L_arm_bridge.bottom_driver','L_arm_bridge.bottom_driver','L_arm_bridge.front_driver','L_arm_bridge.front_driver','L_arm_bridge.front_driver','L_arm_bridge.back_driver',
                        'L_arm_bridge.frontUp_driver','L_arm_bridge.backUp_driver',
                        'L_arm_bridge.frontBottom_driver','L_arm_bridge.backBottom_driver'],
        'bridge' : 'L_arm_bridge'
        },
    'rt_arm_ctrl':{
        'preName' : 'rt_arm',
        'axis' :['up_60','up_90','down_55','down_80','front_60','front_90','front_110','back_90','frontUp_90','backUp_90','frontDown_90','backDown_90'],
        'rotate' : [(0,0,60),(0,0,90),(0,0,-55),(0,0,-80),(0,-60,0),(0,-90,0),(0,-110,0),(0,90,0),#4
                    (-45.0, -45.0, 90.0),(45.0, 45.0, 90.0),#upper
                    (45.0, -45.0, -90.0),(-45.0, 45.0, -90.0)],#lower
        'driverAttr' : ['R_arm_bridge.up_driver','R_arm_bridge.up_driver','R_arm_bridge.bottom_driver','R_arm_bridge.bottom_driver','R_arm_bridge.front_driver','R_arm_bridge.front_driver','R_arm_bridge.front_driver','R_arm_bridge.back_driver',
                        'R_arm_bridge.frontUp_driver','R_arm_bridge.backUp_driver',
                        'R_arm_bridge.frontBottom_driver','R_arm_bridge.backBottom_driver'],
        'bridge' : 'R_arm_bridge'
        },
    #elbow bridge
    'lf_elbow_ctrl':{
        'preName' : 'lf_elbow',
        'axis' : ['front_90','front_120','front_140'],
        'rotate' : [(0,-90,0),(0,-120,0),(0,-140,0)],
        'driverAttr' : ['L_elbow_bridge.front_driver','L_elbow_bridge.front_driver','L_elbow_bridge.front_driver'],
        'bridge' : 'L_elbow_bridge'
        },
    'rt_elbow_ctrl':{
        'preName' : 'rt_elbow',
        'axis' : ['front_90','front_120','front_140'],
        'rotate' : [(0,-90,0),(0,-120,0),(0,-140,0)],
        'driverAttr' : ['R_elbow_bridge.front_driver','R_elbow_bridge.front_driver','R_elbow_bridge.front_driver'],
        'bridge' : 'R_elbow_bridge'
        },
    #hand bridge
    'lf_hand_ctrl':{
        'preName' : 'lf_hand',
        'axis' :['up_90','down_90','front_60','back_60','frontUp_75','frontDown_75','backUp_75','backDown_75'],
        'rotate' : [(0,0,90),(0,0,-90),(0,-60,0),(0,60,0),
            (-30.489181300930145, -43.07951714187093, 69.24642901631519),(30.48918130093016, -43.079517141870944, -69.2464290163152),
            (30.48918130093016, 43.079517141870944, 69.2464290163152),(-30.489181300930145, 43.07951714187093, -69.24642901631519)],
        'driverAttr' : ['L_hand_bridge.up_driver','L_hand_bridge.bottom_driver','L_hand_bridge.front_driver','L_hand_bridge.back_driver',
            'L_hand_bridge.frontUp_driver','L_hand_bridge.frontBottom_driver','L_hand_bridge.backUp_driver','L_hand_bridge.backBottom_driver'],
        'bridge' : 'L_hand_bridge'
        },
    'rt_hand_ctrl':{
        'preName' : 'rt_hand',
        'axis' :['up_90','down_90','front_60','back_60','frontUp_75','frontDown_75','backUp_75','backDown_75'],
        'rotate' : [(0,0,90),(0,0,-90),(0,-60,0),(0,60,0),
            (-30.489181300930145, -43.07951714187093, 69.24642901631519),(30.48918130093016, -43.079517141870944, -69.2464290163152),
            (30.48918130093016, 43.079517141870944, 69.2464290163152),(-30.489181300930145, 43.07951714187093, -69.24642901631519)],
        'driverAttr' : ['R_hand_bridge.up_driver','R_hand_bridge.bottom_driver','R_hand_bridge.front_driver','R_hand_bridge.back_driver',
            'R_hand_bridge.frontUp_driver','R_hand_bridge.frontBottom_driver','R_hand_bridge.backUp_driver','R_hand_bridge.backBottom_driver'],
        'bridge' : 'R_hand_bridge'
        },
    #finger fk
    'lf_index02_fk_ctrl':{
        'preName' : 'lf_index02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_index02_fk_ctrl.rz']
        },
    'lf_index03_fk_ctrl':{
        'preName' : 'lf_index03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_index03_fk_ctrl.rz']
        },
    'lf_index04_fk_ctrl':{
        'preName' : 'lf_index04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_index04_fk_ctrl.rz']
        },
    'lf_mid02_fk_ctrl':{
        'preName' : 'lf_mid02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_mid02_fk_ctrl.rz']
        },
    'lf_mid03_fk_ctrl':{
        'preName' : 'lf_mid03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_mid03_fk_ctrl.rz']
        },
    'lf_mid04_fk_ctrl':{
        'preName' : 'lf_mid04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_mid04_fk_ctrl.rz']
        },
    'lf_ring02_fk_ctrl':{
        'preName' : 'lf_ring02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_ring02_fk_ctrl.rz']
        },
    'lf_ring03_fk_ctrl':{
        'preName' : 'lf_ring03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_ring03_fk_ctrl.rz']
        },
    'lf_ring04_fk_ctrl':{
        'preName' : 'lf_ring04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_ring04_fk_ctrl.rz']
        },
    'lf_pinky02_fk_ctrl':{
        'preName' : 'lf_pinky02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_pinky02_fk_ctrl.rz']
        },
    'lf_pinky03_fk_ctrl':{
        'preName' : 'lf_pinky03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_pinky03_fk_ctrl.rz']
        },
    'lf_pinky04_fk_ctrl':{
        'preName' : 'lf_pinky04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_pinky04_fk_ctrl.rz']
        },
    'lf_thumb03_fk_ctrl':{
        'preName' : 'lf_thumb03',
        'axis' : ['down_60'],
        'rotate' : [(0,0,-60)],
        'driverAttr' : ['lf_thumb03_fk_ctrl.rz']
        },
    'lf_thumb04_fk_ctrl':{
        'preName' : 'lf_thumb02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['lf_thumb04_fk_ctrl.rz']
        },
    'rt_index02_fk_ctrl':{
        'preName' : 'rt_index02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_index02_fk_ctrl.rz']
        },
    'rt_index03_fk_ctrl':{
        'preName' : 'rt_index03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_index03_fk_ctrl.rz']
        },
    'rt_index04_fk_ctrl':{
        'preName' : 'rt_index04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_index04_fk_ctrl.rz']
        },
    'rt_mid02_fk_ctrl':{
        'preName' : 'rt_mid02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_mid02_fk_ctrl.rz']
        },
    'rt_mid03_fk_ctrl':{
        'preName' : 'rt_mid03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_mid03_fk_ctrl.rz']
        },
    'rt_mid04_fk_ctrl':{
        'preName' : 'rt_mid04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_mid04_fk_ctrl.rz']
        },
    'rt_ring02_fk_ctrl':{
        'preName' : 'rt_ring02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_ring02_fk_ctrl.rz']
        },
    'rt_ring03_fk_ctrl':{
        'preName' : 'rt_ring03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_ring03_fk_ctrl.rz']
        },
    'rt_ring04_fk_ctrl':{
        'preName' : 'rt_ring04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_ring04_fk_ctrl.rz']
        },
    'rt_pinky02_fk_ctrl':{
        'preName' : 'rt_pinky02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_pinky02_fk_ctrl.rz']
        },
    'rt_pinky03_fk_ctrl':{
        'preName' : 'rt_pinky03',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_pinky03_fk_ctrl.rz']
        },
    'rt_pinky04_fk_ctrl':{
        'preName' : 'rt_pinky04',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_pinky04_fk_ctrl.rz']
        },
    'rt_thumb03_fk_ctrl':{
        'preName' : 'rt_thumb03',
        'axis' : ['down_60'],
        'rotate' : [(0,0,-60)],
        'driverAttr' : ['rt_thumb03_fk_ctrl.rz']
        },
    'rt_thumb04_fk_ctrl':{
        'preName' : 'rt_thumb02',
        'axis' : ['down_90'],
        'rotate' : [(0,0,-90)],
        'driverAttr' : ['rt_thumb04_fk_ctrl.rz']
        },
    #leg bridge
    'lf_leg_ctrl':{
        'preName' : 'lf_leg',
        'axis' :['front_90','front_120','back_90','outside_90','inside_90','frontOut_90','backOut_90','frontIn_90','backIn_90'],
        'rotate' : [(-90,0,0),(-120,0,0),(90,0,0),(0,0,90),(0,0,-90),#4
                    (-54.73561031724535, 29.999999999999996, 54.73561031724535),(54.73561031724535, -30.000000000000004, 54.73561031724533),#upper
                    (-54.73561031724535, -30.000000000000004, -54.73561031724533),(54.73561031724535, 29.999999999999996, -54.73561031724535)],#lower
        'driverAttr' : ['L_leg_bridge.front_driver','L_leg_bridge.front_driver','L_leg_bridge.back_driver','L_leg_bridge.up_driver','L_leg_bridge.bottom_driver',
                        'L_leg_bridge.frontUp_driver','L_leg_bridge.backUp_driver',
                        'L_leg_bridge.frontBottom_driver','L_leg_bridge.backBottom_driver'],
        'bridge' : 'L_leg_bridge'
        },
    'rt_leg_ctrl':{
        'preName' : 'rt_leg',
        'axis' :['front_90','front_120','back_90','outside_90','inside_90','frontOut_90','backOut_90','frontIn_90','backIn_90'],
        'rotate' : [(-90,0,0),(-120,0,0),(90,0,0),(0,0,90),(0,0,-90),#4
                    (-54.73561031724535, 29.999999999999996, 54.73561031724535),(54.73561031724535, -30.000000000000004, 54.73561031724533),#upper
                    (-54.73561031724535, -30.000000000000004, -54.73561031724533),(54.73561031724535, 29.999999999999996, -54.73561031724535)],#lower
        'driverAttr' : ['R_leg_bridge.front_driver','R_leg_bridge.front_driver','R_leg_bridge.back_driver','R_leg_bridge.up_driver','R_leg_bridge.bottom_driver',
                        'R_leg_bridge.frontUp_driver','R_leg_bridge.backUp_driver',
                        'R_leg_bridge.frontBottom_driver','R_leg_bridge.backBottom_driver'],
        'bridge' : 'R_leg_bridge'
        },
    #knee bridge
    'lf_knee_ctrl':{
        'preName' : 'lf_knee',
        'axis' : ['back_90','back_120','back_140'],
        'rotate' : [(90,0,0),(120,0,0),(140,0,0)],
        'driverAttr' : ['L_knee_bridge.back_driver','L_knee_bridge.back_driver','L_knee_bridge.back_driver'],
        'bridge' : 'L_knee_bridge'
        },
    'rt_knee_ctrl':{
        'preName' : 'rt_knee',
        'axis' : ['back_90','back_120','back_140'],
        'rotate' : [(90,0,0),(120,0,0),(140,0,0)],
        'driverAttr' : ['R_knee_bridge.back_driver','R_knee_bridge.back_driver','R_knee_bridge.back_driver'],
        'bridge' : 'R_knee_bridge'
        },
    #ankle bridge
    'lf_ankle_ctrl':{
        'preName' : 'lf_ankle',
        'axis' :['front_60','back_60','outside_60','inside_60'],
        'rotate' : [(-60,0,0),(60,0,0),(0,0,60),(0,0,-60)],
        'driverAttr' : ['L_foot_bridge.front_driver','L_foot_bridge.back_driver','L_foot_bridge.up_driver','L_foot_bridge.bottom_driver'],
        'bridge' : 'L_foot_bridge'
        },
    'rt_ankle_ctrl':{
        'preName' : 'rt_ankle',
        'axis' :['front_60','back_60','outside_60','inside_60'],
        'rotate' : [(-60,0,0),(60,0,0),(0,0,60),(0,0,-60)],
        'driverAttr' : ['R_foot_bridge.front_driver','R_foot_bridge.back_driver','R_foot_bridge.up_driver','R_foot_bridge.bottom_driver'],
        'bridge' : 'R_foot_bridge'
        },
    #toe bridge
    'lf_toe_ctrl':{
        'preName' : 'lf_toe',
        'axis' :['up_60','bottom_60','outside_60','inside_60'],
        'rotate' : [(-60,0,0),(60,0,0),(0,60,0),(0,-60,0)],
        'driverAttr' : ['L_toe_bridge.up_driver','L_toe_bridge.bottom_driver','L_toe_bridge.back_driver','L_toe_bridge.front_driver'],
        'bridge' : 'L_toe_bridge'
        },
    'rt_toe_ctrl':{
        'preName' : 'rt_toe',
        'axis' :['up_60','bottom_60','outside_60','inside_60'],
        'rotate' : [(-60,0,0),(60,0,0),(0,60,0),(0,-60,0)],
        'driverAttr' : ['R_toe_bridge.up_driver','R_toe_bridge.bottom_driver','R_toe_bridge.back_driver','R_toe_bridge.front_driver'],
        'bridge' : 'R_toe_bridge'
        }
}



def buttonCommand_refreshBridge(mode='get', *args):
    
    bridgeAttrList = ['up', 'down', 'front', 'back', 'inner', 'outer', 'L_side', 'R_side']
        
    oldbridgeList = [[tempD for tempD in cmds.listRelatives(tempE.split('.')[0], c=True, type='transform') if 'bridge' in tempD] for tempE in cmds.ls('*_psd_parent_handle.tag') if cmds.getAttr(tempE) == 'poseDriver']
    bridgeList = [tempBridge[0] for tempBridge in oldbridgeList]

    if mode == 'get':
        return bridgeList
    elif mode == 'refresh':
        cmds.textScrollList('corrective_mainTextScrollList',e=True,ra=True)
        #filter list
        fStrList = []
        filterBridgeList = []
        filterList = cmds.textFieldGrp('corrective_bridge_filter_TFG',q=True,text=True)
        if filterList:
            for filterE in filterList.split(' '):
                fStr = filterE.strip()
                if fStr:
                    fStrList.append(fStr)
            for bridgeE in bridgeList:
                for fStrE in fStrList:
                    if fStrE in bridgeE:
                        filterBridgeList.append(bridgeE)
                        break
        else:
            #empty
            filterBridgeList = bridgeList
        #activated list
        activatedBridgeList = []
        if cmds.checkBoxGrp('corrective_bridge_activated_CBG',q=True,value1=True):
            for bridgeE in filterBridgeList:
                for baE in bridgeAttrList:
                    if cmds.objExists('%s.%s'%(bridgeE,baE)) and cmds.getAttr('%s.%s'%(bridgeE,baE)) >= 0.001:
                        activatedBridgeList.append(bridgeE)
                        break
            filterBridgeList = activatedBridgeList
        cmds.textScrollList('corrective_mainTextScrollList',e=True,a=filterBridgeList)


def buttonCommand_selectDriverAttr(ui_FSBGName='', colorA=0.4, colorB=0.2, mode='one'):
    selectBridgeOld = cmds.textScrollList('corrective_mainTextScrollList', q=True, si=True)[0]
    bridgeAttrList = cmds.listAttr(selectBridgeOld, k=True, v=True) 
    fsbgEList = ['UI_%s_FSBG'%bridgeAttr for bridgeAttr in bridgeAttrList]

    if mode == 'one':
        for fsbgE in fsbgEList:
            beforeColor = cmds.floatSliderButtonGrp(ui_FSBGName,q=True,bgc=True)
            if fsbgE == ui_FSBGName:
                #select inputCurve
                if beforeColor == [colorA,colorA,colorA]:
                    loadGeoStr = cmds.textFieldButtonGrp('corrective_geo_TFBG',q=True,text=True)
                    targetName = cmds.text('corrective_message_text',q=True,label=True).split('target name  :  ')[-1].split('\n')[0]
                    for geomeryE in loadGeoStr.split(','):
                        if cmds.objExists(geomeryE):
                            geomeryE = pm.PyNode(geomeryE)
                            bsList = geomeryE.listHistory(pdo=True,type='blendShape')
                            if bsList:
                                inputNodeList = []
                                targetPreName = targetName.rsplit('_',1)[0]
                                for weightAttrE in pm.listAttr(bsList[0].w,m=True):
                                    if targetPreName in weightAttrE:
                                        inputNodeList += cmds.listConnections('%s.%s'%(bsList[0],weightAttrE),d=False)
                                if inputNodeList:
                                    cmds.select(inputNodeList)
                                    cmds.GraphEditor()
                                break
                else:
                    cmds.floatSliderButtonGrp(fsbgE,e=True,bgc=(colorA,colorA,colorA))
            else:
                cmds.floatSliderButtonGrp(fsbgE,e=True,bgc=(colorB,colorB,colorB))
    #elif mode == 'all':
        #for fsbgE in ['UI_up_FSBG', 'UI_down_FSBG', 'UI_front_FSBG', 'UI_back_FSBG', 'UI_upFront_FSBG', 'UI_upBack_FSBG', 'UI_downFront_FSBG', 'UI_downBack_FSBG']:
            #cmds.floatSliderButtonGrp(fsbgE,e=True,bgc=(colorA,colorA,colorA))
    #updateUI
    updateUI_message()


def updateUI_driverAttrConnnect(attrList=[]):
    #driver attr connect UI
    
    selectBridgeOld = cmds.textScrollList('corrective_mainTextScrollList',q=True,si=True)

    selectBridge = selectBridgeOld[0].split('_cmd_bridge')


    for attrE in attrList:
        FSBGName = 'UI_%s_FSBG'%attrE
        cmds.connectControl(FSBGName, '%s.%s'%(selectBridgeOld[0],attrE))
    #build scriptJob
    #kill !!!
    for jobE in cmds.scriptJob( listJobs=True ):
        if 'attributeChange' in jobE and 'updateUI_message()' in jobE:
            killIndex = int(jobE.split(':')[0])
            cmds.scriptJob( kill=killIndex, force=True)
    #create
    cmds.scriptJob(attributeChange= ['%s_base_alb.angle'%selectBridge[0],'updateUI_message()'])

    updateUI_message()


def buttonCommand_loadGeometry():
    sel = cmds.ls(sl=True,tr=True)
    if sel:
        cmds.textFieldButtonGrp('corrective_geo_TFBG',e=True,text=sel[0] )
    else:
        cmds.textFieldButtonGrp('corrective_geo_TFBG',e=True,text='' )

    if cmds.textScrollList('corrective_mainTextScrollList',q=True,si=True):
        updateUI_message()


def updateUI_message(colorA=0.4, colorB=0.2):
    if cmds.window('corrective_mainWindow',q=True,ex=True):
        #blendShape
        bsNode = ''
        loadGeoStr = cmds.textFieldButtonGrp('corrective_geo_TFBG',q=True,text=True)

        if not loadGeoStr:
            return False

        for geometryE in loadGeoStr.split(','):
            if cmds.objExists(geometryE):
                bsNode = pm.listHistory(geometryE,type='blendShape',pdo=True)
                if bsNode:
                    bsNode = bsNode[0].name()
        #driver
        
        selectAttr = ''
        selectLabel = ''
        ctrlAngle = ''
        selectBridge = cmds.textScrollList('corrective_mainTextScrollList',q=True,si=True)
        bridgeAttrList = cmds.listAttr(selectBridge, k=True, v=True) 
        fsbgEList = ['UI_%s_FSBG'%bridgeAttr for bridgeAttr in bridgeAttrList]
        
        if selectBridge:
            for fsbgE in fsbgEList:
                if cmds.floatSliderButtonGrp(fsbgE,q=True,bgc=True) == [colorA,colorA,colorA]:
                    selectLabel = cmds.floatSliderButtonGrp(fsbgE,q=True,label=True)
                    selectAttr = '%s.%s'%( selectBridge[0] , selectLabel )
            #ctrl rotate   and   target name
            ctrlRotateValue = []
            targetName = ''
            for k,v in correctiveDataDict.items():
                if selectBridge[0] in v['driverAttr'][0]:
                    try:
                        #get ctrl rotate
                        ctrlRotateValue = cmds.getAttr('%s.r'%k)[0]
                        ctrlRotateValue = [round(rE,10) for rE in ctrlRotateValue]
                        #current angle
                        angleAttr = '%s_base_alb.angle'%selectBridge[0].split('_cmd_bridge')[0]
                        ctrlAngle = int( round(cmds.getAttr(angleAttr)) )
                        #targetName
                        targetName = '%s_%s_%s_%s'%(geometryE,v['preName'],selectLabel,ctrlAngle)
                        break
                    except:
                        pass
            # print targetName
            if not targetName:
                angleAttr = '%s_base_alb.angle'%selectBridge[0].split('_cmd_bridge')[0]
                if not cmds.objExists(angleAttr):
                    angMdName = cmds.listConnections('%s.driver_vulue'%selectBridge[0],d=False)
                    angleABName = cmds.listConnections('%s.i1x'%angMdName[0],d=True,scn=True)
                    if angleABName:
                        cmds.rename(angleABName[0],'%s_angle_AB_Bt'%selectBridge[0].split('_bridge')[0])
                        print ('--- auto rename %s'%angleABName[0])
                ctrlAngle = int( round(cmds.getAttr(angleAttr)) )
                bridgePreName = selectBridge[0].split('_psd_cmd_bridge')[0]
                targetName = '%s_%s_%s_%s'%(geometryE,bridgePreName,selectLabel,ctrlAngle)
                ctrlRotateValue = 'not define'
                # print (geometryE,selectLabel,ctrlAngle)
            #final update
            cmds.text('corrective_message_text', e=True , label='\nblendShape  :  %s\ndriver attribute :  %s\ntarget name  :  %s\nctrl rotate  :  %s\nctrl angle  :  %s\n'%(bsNode,selectAttr,targetName,ctrlRotateValue,ctrlAngle) )


def addBlendShape(targetList=[], toObj=''):
    #2list
    if type(targetList) != list:
        targetList = [targetList]
    #top
    returnList = []
    bsNode = pm.listHistory(toObj,pdo=True,type='blendShape')
    if not bsNode:
        bsNode = pm.blendShape(toObj,foc=True,n='%s_correctiveBs'%toObj)
    for targetE in targetList:
        #no exists
        if not cmds.objExists(targetE):
            #create new target
            pm_toObj = pm.PyNode(toObj)
            orgShape = pm_toObj.getShapes()[-1].name()
            newMeshShape = cmds.createNode('mesh',n='%sShape'%targetE)
            newTarget = cmds.listRelatives(newMeshShape,p=True)
            cmds.connectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
            cmds.refresh(f=True)
            cmds.disconnectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
        #targetExists
        targetAttr = '%s.%s'%(bsNode[0],targetE)
        if cmds.objExists(targetAttr):
            continue
        #get Max+1 index
        wiList = bsNode[0].weightIndexList()
        if wiList:
            newIndex = wiList[-1]+1
        else:
            newIndex = 0
        pm.blendShape(bsNode[0],e=True,t=(toObj,newIndex,targetE,1))
        returnList.append(targetAttr)
    return returnList


def buttonCommand_newTarget():
    choiceButton = cmds.promptDialog(title='Rename Target',message=u'新目标体命名:',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel',tx='')
    newTargetName = cmds.promptDialog(query=True, text=True).replace('\n','')
    if choiceButton == 'OK':
        blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
        blendShapeNode = pm.PyNode(blendShapeName)
        geometryNode = blendShapeNode.getBaseObjects()[0].getParent()
        addBlendShape(targetList=[newTargetName],toObj = geometryNode.name())
        buttonCommand_refreshTargetList('refresh list')


def buttonCommand_addBlendShape():
    #add blendShape
    loadGeoStr = cmds.textFieldButtonGrp('corrective_geo_TFBG',q=True,text=True)
    targetName = cmds.text('corrective_message_text',q=True,label=True).split('target name  :  ')[-1].split('\n')[0]
    for geomeryE in loadGeoStr.split(','):
        if cmds.objExists(geomeryE):
            geomeryE = pm.PyNode(geomeryE)
            bsList = geomeryE.listHistory(pdo=True,type='blendShape')
            if bsList and targetName in pm.listAttr(bsList[0].w,m=True):
                cmds.warning( targetName+'  exists  !!!!!' )
                continue
            orgShape = geomeryE.getShapes()[-1].name()
            newMeshShape = cmds.createNode('mesh',n='%sShape'%targetName)
            newTarget = cmds.listRelatives(newMeshShape,p=True)
            cmds.connectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
            cmds.refresh(f=True)
            cmds.disconnectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
            bsAttrList = addBlendShape(newTarget,toObj=geomeryE)
            cmds.hide(newTarget)
            #sdk
            #get front angle
            sameSidePreStr,angleValue = targetName.rsplit('_',1)
            if bsList:
                sameSideList = [weightE for weightE in pm.listAttr(bsList[0].w,m=True) if sameSidePreStr in weightE and weightE != newTarget]
            else:
                sameSideList = []
            frontAngle = 0
            backAngle = 180
            front_lastFloat = 0
            back_lastFloat = 0
            backExists = False
            if sameSideList:
                for sameSideE in sameSideList:
                    eachAngle = sameSideE.rsplit('_',1)[-1]
                    if int(angleValue) > int(eachAngle) > frontAngle:
                        frontAngle = int(eachAngle)
                    if int(angleValue) < int(eachAngle) < backAngle:
                        backAngle = int(eachAngle)
                frontWeightAttr = '%s.%s_%s'%(bsList[0],sameSidePreStr,frontAngle)
                if cmds.objExists(frontWeightAttr):
                    inputCurve = cmds.listConnections(frontWeightAttr,d=False,p=False,scn=True)
                    if inputCurve and 'animCurve' in cmds.objectType(inputCurve[0]):
                        front_lastIndex = cmds.keyframe(inputCurve[0],q=True,iv=True)[-1]
                        front_lastFloat = cmds.keyframe(inputCurve[0],q=True,index=(front_lastIndex,front_lastIndex),fc=True)
                backWeightAttr = '%s.%s_%s'%(bsList[0],sameSidePreStr,backAngle)
                if cmds.objExists(backWeightAttr):
                    inputCurve = cmds.listConnections(backWeightAttr,d=False,p=False,scn=True)
                    if inputCurve and 'animCurve' in cmds.objectType(inputCurve[0]):
                        back_lastIndex = cmds.keyframe(inputCurve[0],q=True,iv=True)[-1]
                        back_lastFloat = cmds.keyframe(inputCurve[0],q=True,index=(back_lastIndex,back_lastIndex),fc=True)
                        backExists = True
            #
            driverAttr = cmds.text('corrective_message_text',q=True,label=True).split('driver attribute :  ')[-1].split('\n')[0]
            cmds.setDrivenKeyframe(bsAttrList[0],dv=front_lastFloat,v=0,cd=driverAttr,itt='linear',ott='linear')
            cmds.setDrivenKeyframe(bsAttrList[0],v=1,cd=driverAttr,itt='linear',ott='linear')
            if backExists:
                cmds.setDrivenKeyframe(bsAttrList[0],dv=back_lastFloat,v=0,cd=driverAttr,itt='linear',ott='linear')
            cmds.select(loadGeoStr)


def BLENDSHAPE_rebuildTarget(attrStr = ''):
    """ 输入一个bs目标体属性名类似 bsName.weightName后,会重建这个目标体"""
    targetIndex = pm.PyNode(attrStr).index()
    bsName,attrName = attrStr.split('.')
    bsNode = pm.PyNode(bsName)
    geometryNode = bsNode.getBaseObjects()[0].getParent()
    orgShape = bsNode.getInputGeometry()[0].name()
    #createTarget
    newMeshShape = cmds.createNode('mesh',n='%sShape'%attrName)
    newTarget = cmds.listRelatives(newMeshShape,p=True)
    cmds.connectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
    cmds.refresh(f=True)
    cmds.disconnectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
    cmds.hide(newTarget)
    #move vtx
    ictValue = cmds.getAttr( '%s.it[0].itg[%s].iti[6000].ict'%(bsName,targetIndex) )
    if ictValue:
        vtxList = cmds.ls( ['%s.%s'%(newTarget[0],vtxE) for vtxE in ictValue] ,fl=True)
        vtxRelativeTranslateList = cmds.getAttr('%s.it[0].itg[%s].iti[6000].ipt'%(bsName,targetIndex))
        for i in range(len(vtxList)):
            currentMoveValue = vtxRelativeTranslateList[i][:-1]
            cmds.move(currentMoveValue[0],currentMoveValue[1],currentMoveValue[2],vtxList[i],r=True,ws=True)
    #connect to blendShape
    cmds.connectAttr('%s.worldMesh[0]'%newMeshShape,'%s.it[0].itg[%s].iti[6000].igt'%(bsName,targetIndex))
    return newTarget



def buttonCommand_cpButtonChangeMode():
    labelStr = ['correctivePose','exit corrective']
    buttonLabel = cmds.button('corrective_correctivePose_button',q=True,label=True)
    if buttonLabel == labelStr[0]:
        #to red
        cmds.button('corrective_correctivePose_button',e=True,label=labelStr[1],bgc=(0.9,0.2,0.2),c = lambda *args:buttonCommand_correctivePoseExit())
    elif buttonLabel == labelStr[1]:
        #to green
        cmds.button('corrective_correctivePose_button',e=True,label=labelStr[0],bgc=(0.2,0.9,0.2),c = lambda *args:buttonCommand_correctivePose())


GLOBAL_deleteHistory_geometryList,GLOBAL_delete_geometryList,GLOBAL_showHidden_geometryList = [],[],[]


def buttonCommand_correctivePose(mode='load'):
    global GLOBAL_deleteHistory_geometryList,GLOBAL_delete_geometryList,GLOBAL_showHidden_geometryList
    #correctivePose_v0.5
    #20200518
    if "correctShape" not in pm.pluginInfo( query=True, listPlugins=True ):
        pm.loadPlugin("correctShape")
    if mode == 'sel':
        pm_geometryList = pm.selected(type='transform')
    elif mode == 'load':
        loadGeoStr = cmds.textFieldButtonGrp('corrective_geo_TFBG',q=True,text=True)
        if loadGeoStr:
            geometryName = loadGeoStr.split(',')[0]
            pm_geometryList = [pm.PyNode(geometryName)]
    if not pm_geometryList:
        return False
    hideList = pm_geometryList
    bsList = pm_geometryList[0].listHistory(pdo=True,type='blendShape')
    openList = []
    if bsList:
        bsName = bsList[0]
        #listAllAttr
        attrList = cmds.listAttr('%s.w'%bsName,m=True)
        sortAttrList = sorted(attrList,key = lambda r:cmds.getAttr('%s.%s'%(bsName.name(),r)) )
        #sortAttrList[-1] is max
        openList = [sortAttrE for sortAttrE in sortAttrList if cmds.getAttr('%s.%s'%(bsName.name(),sortAttrE)) > 0.999]
        #print openList
        if openList:
            finalTransform = openList[0]
            if len(openList) > 1:
                cancelButtonName = '---EXIT---'
                openList.append(cancelButtonName)
                finalTransform = cmds.confirmDialog(t='correctiveTarget',m='Please select a correctiveTarget.',b=openList,cancelButton=cancelButtonName,dismissString=cancelButtonName)
                if finalTransform == cancelButtonName:
                    #no corrective
                    return False
        else:
            return False
        #inherit 1
        tempGeo = pm.duplicate(pm_geometryList[0],n='tempGeometry')
        targetIndex = bsName.attr(finalTransform).index()
        inputTarget = bsName.it[0].itg[targetIndex].iti[6000].igt.listConnections(d=False)
        if inputTarget:
            orgGeo = bsName.getInputGeometry()
            orgGeo[0].outMesh >> pm.PyNode(inputTarget[0]).inMesh
        else:
            #rebuild target
            inputTarget = BLENDSHAPE_rebuildTarget( '%s.%s'%(bsName.name(),finalTransform) )
            inputTarget = [pm.PyNode( inputTarget[0] )]
        #beZero
        orgGeo = bsName.getInputGeometry()
        orgGeo[0].outMesh >> pm.PyNode(inputTarget[0]).inMesh
        pm.refresh(f=True)
        orgGeo[0].outMesh // pm.PyNode(inputTarget[0]).inMesh
        #CCS
        pm.select(pm_geometryList[0])
        ccsReturn = mel.eval('source correctShape.mel;setupCorrectBlendSkin();')
        if not ccsReturn:
            mel.eval('setupCorrectBlendSkin();')
        ccsShape = cmds.listHistory(ccsReturn[1],pdo=True)
        #inherit 2
        pm.blendShape(tempGeo,ccsReturn[0],w=(0,1))
        pm.delete(ccsReturn[0],ch=True)
        #connect 2 target
        pm.PyNode(ccsShape[0]).outMesh >> inputTarget[0].inMesh
        #pm.blendShape(ccsReturn[1],inputTarget[0],w=(0,1))
        #clear
        pm.delete(tempGeo)
        if cmds.listRelatives(ccsReturn[0],p=True):
            cmds.parent(ccsReturn[0],w=True)
        pm.hide(ccsReturn[1],hideList[0])
        cmds.setAttr(ccsReturn[0]+'.t',0,0,0)
        cmds.select(ccsReturn[0])
        #global var save
        GLOBAL_delete_geometryList = ccsReturn
        GLOBAL_deleteHistory_geometryList = inputTarget
        GLOBAL_showHidden_geometryList = hideList
        #change button
        buttonCommand_cpButtonChangeMode()


def buttonCommand_correctivePoseExit():
    global GLOBAL_deleteHistory_geometryList,GLOBAL_delete_geometryList,GLOBAL_showHidden_geometryList
    buttonCommand_cpButtonChangeMode()
    try:
        pm.delete(GLOBAL_deleteHistory_geometryList,ch=True)
        pm.delete(GLOBAL_deleteHistory_geometryList)
        pm.delete(GLOBAL_delete_geometryList)
    except:
        pass
    pm.showHidden(GLOBAL_showHidden_geometryList)


def BLENDSHAPE_mirrorTarget(attrStr='bsName.weightName', searchStr = 'lf_', searchToStr = 'rt_'):
    """ 镜像指定名称的bs目标体"""
    bsName,attrName = attrStr.split('.')
    bsNode = pm.PyNode(bsName)
    geometryNode = bsNode.getBaseObjects()[0].getParent()
    orgShape = bsNode.getInputGeometry()[0].name()
    toAttrName = attrName.replace(searchStr,searchToStr)
    bsWeightList = pm.listAttr(bsNode.w,m=True)
    targetIndex = pm.PyNode(attrStr).index()

    #check targetName is mirrorable
    if not searchStr in attrName:
        return False

    #fromTarget get
    inputTarget = cmds.listConnections('%s.it[0].itg[%s].iti[6000].igt'%(bsName,targetIndex),d=False)
    if not inputTarget:
        inputTarget = BLENDSHAPE_rebuildTarget(attrStr)
    
    #toAttr get
    if toAttrName in bsWeightList:
        #toTarget check
        toAttr_targetIndex = pm.PyNode('%s.%s'%(bsName,toAttrName)).index()
        toAttr_inputTarget = cmds.listConnections('%s.it[0].itg[%s].iti[6000].igt'%(bsName,toAttr_targetIndex),d=False)
        if not toAttr_inputTarget:
            toAttr_inputTarget = BLENDSHAPE_rebuildTarget('%s.%s'%(bsName,toAttrName))
            print(toAttr_inputTarget[0]+'aad')
    else:
        #toTarget not exists   so   create new one
        newMeshShape = cmds.createNode('mesh',n='%sShape'%toAttrName)
        newTarget = cmds.listRelatives(newMeshShape,p=True)
        cmds.connectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
        cmds.refresh(f=True)
        cmds.disconnectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
        cmds.hide(newTarget)
        addBlendShape(targetList = newTarget,toObj = geometryNode.name())
        toAttr_inputTarget = newTarget
        print('aad')
    
    #reverse WRAP
    #---createORG
    newMeshShape = cmds.createNode('mesh',n='%sShape'%'TEMP_ORG')
    newTarget = cmds.listRelatives(newMeshShape,p=True)
    cmds.connectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
    cmds.refresh(f=True)
    cmds.disconnectAttr('%s.worldMesh[0]'%orgShape,'%s.inMesh'%newMeshShape)
    cmds.hide(newTarget)
    toWrapGeo = reverseWrap([inputTarget[0],newTarget[0]],False)
    #wrapMesh connect toTargetMesh
    cmds.connectAttr('%s.worldMesh[0]'%toWrapGeo[0],'%s.inMesh'%toAttr_inputTarget[0])
    cmds.refresh(f=True)    
    #setZero
    vtxAttrList = cmds.ls('%s.pnts[*]'%toAttr_inputTarget[0],fl=True)
    setDataList = len(vtxAttrList)*[0,0,0]
    cmds.setAttr('%s.pnts[*]'%toAttr_inputTarget[0],*setDataList)
    #clean
    cmds.delete(toAttr_inputTarget, ch=True)
    cmds.delete(toWrapGeo,newTarget,inputTarget,toAttr_inputTarget)


def reverseWrap(objList=[],deleteWrapGroup=True):
    """ 0 = target  1 = org"""
    if not cmds.objExists('reverseWrap_delete') and objList: #create wrapGroup
        deleteGroup = cmds.group(em=True,n='reverseWrap_delete')
        wrapGeo = cmds.duplicate(objList[1], rr=True, name='reverseWrap_outputGeometry')
        newBaseGeo = cmds.duplicate(objList[1],n='reverseWrap_bsGeometry')
        cmds.parent(newBaseGeo,wrapGeo,deleteGroup)
        cmds.setAttr(newBaseGeo[0]+'.sx',-1)
        cmds.select(wrapGeo,newBaseGeo[0])
        pm.mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "1", "0" }')
        print ('-----wrap-----')

    else:
        deleteGroup = ['reverseWrap_delete']
        wrapGeo = ['reverseWrap_outputGeometry']
        newBaseGeo = ['reverseWrap_bsGeometry']
    reverseGeo = []
    if objList: #output
        bsNodeName = cmds.blendShape(objList[0],newBaseGeo[0],w=(0,1))
        cmds.refresh(f=True)
        reverseGeo = cmds.duplicate(wrapGeo[0],n=objList[0]+'_reverseWrap')
        cmds.parent(reverseGeo,w=True)
        cmds.delete(bsNodeName)
    if deleteWrapGroup: #delete useless
        cmds.delete(wrapGeo[0],ch=True)
        cmds.delete(deleteGroup)
    return reverseGeo


def buttonCommand_refreshTargetList(mode='refresh'):
    if mode == 'refresh':
        sel = pm.selected()
        if sel:
            bsNode = sel[0].listHistory(pdo=True,type='blendShape')
            #update text
            if not bsNode:
                return False
            bsName = bsNode[0].name()
            cmds.text('corrective_blendShape_text',e=True,label='    blendShape   :   %s'%bsName)
            targetList = cmds.listAttr('%s.w'%bsName,m=True)
        else:
            cmds.text('corrective_blendShape_text',e=True,label='    blendShape   :   ')
            cmds.textScrollList('corrective_tab2_targetList_textScrollList',e=True,ra=True)
            return False
    elif mode == 'refresh list':
        blendShapeNameList = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')
        bsName = blendShapeNameList[-1]
        if cmds.objExists(bsName):
            targetList = cmds.listAttr('%s.w'%bsName,m=True)
        else:
            return False

    #update textScrollList
    #save select
    selectTarget = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    cmds.textScrollList('corrective_tab2_targetList_textScrollList',e=True,ra=True)
    #filter list
    fStrList = []
    filtertargetList = []
    filterList = cmds.textFieldGrp('corrective_tab2_target_filter_TFG',q=True,text=True)
    if filterList:
        for filterE in filterList.split(' '):
            fStr = filterE.strip()
            if fStr:
                fStrList.append(fStr)
        for targetE in targetList:
            for fStrE in fStrList:
                if fStrE in targetE:
                    filtertargetList.append(targetE)
                    break
    else:
        #empty
        filtertargetList = targetList

    #activated list
    activatedTargetList = []
    if cmds.checkBoxGrp('corrective_target_activated_CBG',q=True,value1=True):
        for targetE in filtertargetList:
            if cmds.getAttr('%s.%s'%(bsName,targetE)) >= 0.001:
                activatedTargetList.append(targetE)
        filtertargetList = activatedTargetList
    cmds.textScrollList('corrective_tab2_targetList_textScrollList',e=True,a=filtertargetList)
    #load select
    allItemList = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,ai=True)
    if allItemList and selectTarget:
        selectTarget = [aiE for aiE in allItemList if aiE in selectTarget]
        cmds.textScrollList('corrective_tab2_targetList_textScrollList',e=True,si=selectTarget,da=True)


def buttonCommand_mirrorSelectTarget():
    blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
    selectTarget = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    searchStr = cmds.textFieldGrp('corrective_tab2_bs_search_TFG',q=True,text=True)
    replaceStr = cmds.textFieldGrp('corrective_tab2_bs_replace_TFG',q=True,text=True)
    if selectTarget:
        for targetE in selectTarget:
            BLENDSHAPE_mirrorTarget('%s.%s'%(blendShapeName,targetE),searchStr,replaceStr)            
        reverseWrap(deleteWrapGroup=True)
        buttonCommand_refreshTargetList('refresh list')


def ATTRIBUTE_mirrorSDK(attrStr='bsName.weightName',attrSearchStr = '_L_', attrReplaceToStr = '_R_', driverSearchStr = 'L_', driverReplaceToStr = 'R_'):
    ''' '''
    driverType = ''
    #attr input get
    if True:
        objName,attrName = attrStr.split('.')
        mirrorToAttrName = '%s.%s'%(objName,attrName.replace(attrSearchStr,attrReplaceToStr))
        if not cmds.objExists(attrStr) or not cmds.objExists(mirrorToAttrName):
            #attrbute not exists !!!
            return False
    
        inputCurve = cmds.listConnections(attrStr,d=False,p=False,scn=True)
        if not inputCurve:
            return u'属性没有输入连接 !!!'
        
        mirrorCurve = []
        if 'animCurve' in cmds.objectType(inputCurve[0]):
            #type curve
            driverAttr = cmds.listConnections('%s.input'%inputCurve[0],d=False,p=True,scn=True)
            if not driverAttr:
                return u'驱动曲线没有输入连接 !!!'
            #-----type
            driverType = 'animCurve'
        else:
            #other type  or  single connect
            driverAttr = cmds.listConnections(attrStr,d=False,p=True,scn=True)
            #-----type
            driverType = 'other'

        driverObjName,driverAttrName = driverAttr[0].split('.')
        newDriverAttr = '%s.%s'%(driverObjName.replace(driverSearchStr,driverReplaceToStr),driverAttrName.replace(driverSearchStr,driverReplaceToStr))
        if not cmds.objExists(newDriverAttr) or newDriverAttr == driverAttr[0]:
            return u'没找到新驱动属性 !!!'
    
    #toAttr input get
    if True:
        #if inputCurve.output only one connect  then  delete this curve 
        toAttrInput = cmds.listConnections(mirrorToAttrName,d=False,p=False,scn=True)
        if toAttrInput:
            if 'animCurve' in cmds.objectType(toAttrInput[0]):
                if len(cmds.listConnections('%s.output'%toAttrInput[0],s=False)) == 1:
                    cmds.delete(toAttrInput[0])
    if driverType == 'animCurve':
        #---mirror curve
        mirrorCurve = cmds.duplicate(inputCurve[0],n='%s_MIRROR'%inputCurve[0])
        #newDriver -> newCurve
        cmds.connectAttr(newDriverAttr,'%s.input'%mirrorCurve[0],f=True)
        #newCurve -> toAttr
        cmds.connectAttr('%s.output'%mirrorCurve[0],mirrorToAttrName,f=True)
    elif driverType == 'other':
        #newDriver -> toAttr
        cmds.connectAttr(newDriverAttr,mirrorToAttrName,f=True)


def buttonCommand_mirrorSelectTargetInputSDK():
    blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
    selectTarget = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    attrSearchStr = cmds.textFieldGrp('corrective_tab2_bs_search_TFG',q=True,text=True)
    attrReplaceStr = cmds.textFieldGrp('corrective_tab2_bs_replace_TFG',q=True,text=True)
    driverSearchStr = cmds.textFieldGrp('corrective_tab2_sdk_search_TFG',q=True,text=True)
    driverReplaceStr = cmds.textFieldGrp('corrective_tab2_sdk_replace_TFG',q=True,text=True)
    returnList = []
    if selectTarget:
        for targetE in selectTarget:
            blendShapeWeightName = '%s.%s'%(blendShapeName,targetE)
            returnValue = ATTRIBUTE_mirrorSDK(blendShapeWeightName,attrSearchStr,attrReplaceStr,driverSearchStr,driverReplaceStr)
            if returnValue:
                returnList.append([blendShapeWeightName,returnValue])
        if returnList:
            finalStr = ''
            for returnValueE in returnList:
                finalStr += '   '.join(returnValueE)
                finalStr += '\n'
            cmds.confirmDialog(m=finalStr)


def doubleClickCommand_tab2_targetList_textScrollList():
    selectTarget = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    choiceButton = cmds.promptDialog(title='Rename Target',message=u'修改目标体命名:',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel',tx=selectTarget[0])
    newTargetName = cmds.promptDialog(query=True, text=True)
    if choiceButton == 'OK' and selectTarget[0] != newTargetName:
        blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
        pm_weightAttr = pm.PyNode('%s.%s'%(blendShapeName,selectTarget[0]))
        pm.aliasAttr(newTargetName,pm_weightAttr)
        buttonCommand_refreshTargetList('refresh list')


def Search_Replace_renameTarget():
    blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
    selectTargetList = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    choiceButton = cmds.promptDialog(title='Search_Replace Target',message=u'根据条件修改目标体命名:',button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    SearchAndReplaceText = cmds.promptDialog(query=True, text=True)
    spName = SearchAndReplaceText.split(' ')     
    for selectTarget in selectTargetList: 
        pm_weightAttr = pm.PyNode('%s.%s'%(blendShapeName,selectTarget))
        newTargetName = selectTarget.replace(spName[0], spName[-1])   
        if choiceButton == 'OK' and selectTarget != newTargetName:  
            pm.aliasAttr(newTargetName,pm_weightAttr)
            buttonCommand_refreshTargetList('refresh list')


def menuItemCommand_openHelpDocumentation(docPath):
    docPath = os.path.join(os.path.dirname(docPath),'corrective_editor_HELP.docx')
    if cmds.about(linux=True):
        docPath = convertPath_windows2linux(docPath)
    cmds.launch(dir=docPath)


def convertPath_windows2linux(self,sourcePath = ''):
    import os
    inputPath = sourcePath.replace('\n','')
    inputPath = inputPath.replace('\\','/')
    inputPath = inputPath.split('/proj/')[-1]
    #
    if '//' in inputPath:
        inputPath = inputPath.split('.',2)[-1]
    #
    if '/proj/' in sourcePath or '\\proj\\' in sourcePath:
        projStr = 'proj/'
    else:
        projStr = ''
    outputPath = os.path.join('/mnt/%s'%projStr,inputPath)
    if inputPath:
        return outputPath

def corrective_floatSliderButtonUI():
    
    selectBridgeOld = cmds.textScrollList('corrective_mainTextScrollList', q=True, si=True)[0]
    bridgeAttrList = cmds.listAttr(selectBridgeOld, k=True, v=True)    

    if cmds.columnLayout('corrective_float_columnLayout', q=True, ex=True):
        cmds.deleteUI('corrective_float_columnLayout')

    cmds.columnLayout('corrective_float_columnLayout',adj=True,h=245,bgc=(0.2,0.2,0.2),p='corrective_B_columnLayout')
    cmds.text('diver attrbute :')

    for bridgeAttrE in bridgeAttrList:
        FSBGName = 'UI_%s_FSBG'%bridgeAttrE

        cmds.floatSliderButtonGrp(FSBGName, label=bridgeAttrE,
            en=False,
            field=True,
            fieldMinValue=0.000,
            fieldMaxValue=1.000,
            value=0.000,
            adjustableColumn=3,
            height=28,
            columnWidth=([1,70],[2,50],[3,150],[4,50]),columnAttach=[(1, 'both', 0),(2, 'both', 0),(3, 'both', 0),(4, 'both', 0)],
            rowAttach=[(1, 'both', 0),(2, 'both', 0),(3, 'both', 0),(4, 'both', 0)],
            buttonLabel=' select ',
            minValue=0.000,
            maxValue=180.000,
            precision=3,
            parent = 'corrective_float_columnLayout',
            buttonCommand = lambda tempStr=FSBGName:buttonCommand_selectDriverAttr(tempStr))

    return bridgeAttrList

def deleteBlendshapeAttrList(bsNode,attr):
    
    alizList = cmds.aliasAttr(bsNode,q=True)        
    temp = cmds.setAttr('%s.%s'%(bsNode, attr), 0) 
    weightTemp = alizList[alizList.index(attr)+1]
    targetIndex = int(re.findall(r'\d+', weightTemp)[0])

    cmds.removeMultiInstance('%s.w[%s]'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.parentDirectory[%s]'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.nextTarget[%s]'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.targetVisibility[%s]'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.targetParentVisibility[%s]'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.it[0].itg[%s].targetWeights'%(bsNode, targetIndex), b=True)
    cmds.removeMultiInstance('%s.it[0].itg[%s]'%(bsNode, targetIndex), b=True)
    cmds.aliasAttr('%s.%s'%(bsNode, attr), rm=True)


def buttonCommand_rebuildSelectTarget(mode):
    blendShapeName = cmds.text('corrective_blendShape_text',q=True,label=True).split('   :   ')[-1]
    selectTarget = cmds.textScrollList('corrective_tab2_targetList_textScrollList',q=True,si=True)
    if selectTarget:
        for targetE in selectTarget:
            if mode == 'reBuildTarget':            
                rebuildTargetMod = BLENDSHAPE_rebuildTarget('%s.%s'%(blendShapeName,targetE))
                cmds.setAttr('%s.v'%rebuildTargetMod[0],1)
            
            elif mode == 'removeTarget':
                deleteBlendshapeAttrList(blendShapeName,targetE)
                buttonCommand_refreshTargetList('refresh list')
        if mode == 'replaceTarget':
            if len(selectTarget) == 1:
                newTarget = cmds.ls(sl=True)[0]
                oldTarget = BLENDSHAPE_rebuildTarget('%s.%s'%(blendShapeName,targetE))
                cmds.blendShape(newTarget,oldTarget,w=(0,1),n='%s_secBlendShape'%newTarget)
                cmds.delete(oldTarget, ch=True)
                cmds.delete(newTarget)
                cmds.rename(oldTarget,newTarget)
            else:
                cmds.warning('only select one Target')


def corrective_Enter():
    bridgeAttrList = corrective_floatSliderButtonUI()
    updateUI_driverAttrConnnect(bridgeAttrList)

def doubleSelectBridge():
    selectBridgeOld = cmds.textScrollList('corrective_mainTextScrollList', q=True, si=True)[0]
    cmds.select(selectBridgeOld)

def corrective_buildUI():
    """
             tab1Layout
    |---------------------------|
    |           rowA            |
    |---------------------------|
    |         |                 |
    |         |                 |
    | columnA |    columnB      |   (rowB)
    |         |                 |
    |         |                 |
    |---------------------------|
    |                 |         |
    |     cloumnC     | cloumnD |   (rowC)
    |                 |         |
    |---------------------------|
    """


    #build window
    

    if cmds.window('corrective_mainWindow',q=True,ex=True):
        cmds.deleteUI('corrective_mainWindow')
    cmds.window('corrective_mainWindow',title='corrective',tlb=False,sizeable=False)
    cmds.columnLayout('corrective_main_columnLayout',adj=True)
    cmds.menuBarLayout('corrective_main_menuBarLayout')
    cmds.menu('corrective_Help_menu',label='Help', helpMenu=True)
    cmds.menuItem('corrective_Help_menuItem',label='help documentation',c = lambda *args:menuItemCommand_openHelpDocumentation(pyPath))
    cmds.setParent('corrective_main_columnLayout')

    corrective_mainTabLayout01 = cmds.tabLayout('corrective_mainTabLayout',innerMarginWidth=5, innerMarginHeight=5,bs='none')

    #              #
    #-----tab1-----#
    #              #
    corrective_mainTabLayout01_child1 = cmds.columnLayout('corrective_tab1_columnLayout',adj=True)
    #rowA
    cmds.rowLayout('corrective_A_rowLayout',nc=2,cw2=(150,330),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.button(label='refresh bridge',h=25,c = lambda *args:buttonCommand_refreshBridge('refresh'))
    cmds.textFieldButtonGrp('corrective_geo_TFBG',label='geometry  :  ', text='', buttonLabel='Load' ,cw=([1,80],[2,185],[3,60]),columnAttach=[(1, 'both', 0),(2, 'both', 0),(3, 'both', 0)],bc = lambda *args:buttonCommand_loadGeometry() )
    
    cmds.setParent('..')
    #rowB
    cmds.rowLayout('corrective_B_rowLayout',nc=2,cw2=(150,200))
    #columnA
    cmds.columnLayout('corrective_A_columnLayout',adj=True,h=245)
    cmds.text('bridge list :')
    cmds.textScrollList('corrective_mainTextScrollList',h=190,allowMultiSelection=False,append=buttonCommand_refreshBridge('get'),sc = lambda *args:corrective_Enter(),dcc = lambda *args:doubleSelectBridge())
    cmds.checkBoxGrp('corrective_bridge_activated_CBG',label='   ', label1='Activated',columnWidth=([1,5],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)],cc= lambda *args:buttonCommand_refreshBridge(mode='refresh'))
    cmds.textFieldGrp('corrective_bridge_filter_TFG',label='filter : ', text='',columnWidth=([1,40],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)],cc = lambda *args:buttonCommand_refreshBridge(mode='refresh'))
    cmds.setParent('corrective_B_rowLayout')
    #columnB
    cmds.columnLayout('corrective_B_columnLayout',adj=True,h=245,bgc=(0.2,0.2,0.2))
    cmds.setParent('corrective_tab1_columnLayout')
    #rowC
    cmds.rowLayout('corrective_C_rowLayout',nc=2,cw2=(350,130),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    #columnC
    cmds.columnLayout('corrective_C_columnLayout',adj=True)
    cmds.text('corrective_message_text',label='''
    blendShape  :  %s
    driver attribute :  %s
    target name  :  %s
    ctrl rotate  :  %s
    ctrl angle  :  %s
    '''%('','','','',''),al='left')
    cmds.setParent('..')
    #columnD
    cmds.columnLayout('corrective_D_columnLayout',adj=True)
    cmds.button('corrective_addBlendShape_button',label='add blendShape',h=45,c=lambda *args:buttonCommand_addBlendShape(),bgc=(0.7,0.7,0.7))
    cmds.button('corrective_correctivePose_button',label='correctivePose',h=45,c=lambda *args:buttonCommand_correctivePose(),bgc=(0.3,0.9,0.3))
    
    #              #
    #-----tab2-----#
    #              #
    cmds.setParent('corrective_mainTabLayout')
    corrective_mainTabLayout01_child2 = cmds.columnLayout('corrective_tab2_columnLayout',adj=True)
    #tab2_rowA
    cmds.rowLayout('corrective_tab2_A_rowLayout',nc=2,cw2=(150,330),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.button('corrective_refreshTarget_button',label='refresh target',h=25,c = lambda *args:buttonCommand_refreshTargetList('refresh'))
    cmds.text('corrective_blendShape_text',label='    blendShape   :   ',al='left',h=25)
    
    cmds.setParent('..')
    #tab2_rowB
    cmds.rowLayout('corrective_tab2_B_rowLayout',nc=2,cw2=(150,200))
    #tab2_columnA
    cmds.columnLayout('corrective_tab2_A_columnLayout',adj=True,h=330)
    cmds.text(label='target list :')
    cmds.textScrollList('corrective_tab2_targetList_textScrollList',h=190,allowMultiSelection=True,append=[],dcc = lambda *args:doubleClickCommand_tab2_targetList_textScrollList() )
    cmds.popupMenu(button=4, markingMenu=True)
    cmds.menuItem('ReplaceTarget_menu',l='Replace', rp='W', c=lambda *args:buttonCommand_rebuildSelectTarget('replaceTarget'))
    cmds.menuItem('RemoveTarget_menu',l= 'Remove', rp='E', c=lambda *args:buttonCommand_rebuildSelectTarget('removeTarget'))
    cmds.menuItem('ReBuild_Target_menu',l= 'ReBuild_Target', rp='S', c=lambda *args:buttonCommand_rebuildSelectTarget('reBuildTarget'))
    cmds.menuItem('SearchReplace_TargetName_menu',l= 'Search_ReplaceName', rp='N', c=lambda *args:Search_Replace_renameTarget())
    cmds.checkBoxGrp('corrective_target_activated_CBG',label='   ', label1='Activated',columnWidth=([1,5],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)],cc= lambda *args:buttonCommand_refreshTargetList('refresh list'))
    cmds.textFieldGrp('corrective_tab2_target_filter_TFG',label='filter : ', text='',columnWidth=([1,40],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)],cc = lambda *args:buttonCommand_refreshTargetList('refresh list'))
    cmds.button('corrective_newTarget_button',label='add new target',h=85,bgc=(0.7,0.7,0.7),c= lambda *args:buttonCommand_newTarget())
    cmds.setParent('..')
    #tab2_columnB
    cmds.columnLayout('corrective_tab2_B_columnLayout',adj=True,h=330)
    #                     #
    #-----tab2_subTab-----#
    #                     #
    cmds.tabLayout('corrective_tab2_subTab_tabLayout',innerMarginWidth=5, innerMarginHeight=5,bs='notop',h=230)
    #
    #mirror
    #
    cmds.columnLayout('corrective_tab2_mirror_columnLayout',adj=True)
    #mirror target
    cmds.frameLayout( label='mirror blendShape target'.title(),bgc=(0.2,0.2,0.2))
    cmds.rowLayout('corrective_tab2_C_rowLayout',nc=2,h=80)
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('corrective_tab2_bs_search_TFG',label='search for : ', text='_L_',columnWidth=([1,100],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.separator( height=5,st='none')
    cmds.textFieldGrp('corrective_tab2_bs_replace_TFG',label='replace with : ', text='_R_',columnWidth=([1,100],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.setParent('..')
    cmds.button(label='Mirror',w=90,h=45,command= lambda *args:buttonCommand_mirrorSelectTarget())
    #mirror sdk
    cmds.setParent('corrective_tab2_mirror_columnLayout')
    cmds.frameLayout( label='mirror target sdk'.title(),bgc=(0.2,0.2,0.2))
    cmds.rowLayout('corrective_tab2_D_rowLayout',nc=2,h=80)
    cmds.columnLayout(adj=True)
    cmds.textFieldGrp('corrective_tab2_sdk_search_TFG',label='search for : ', text='L_',columnWidth=([1,100],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.separator(height=5,st='none')
    cmds.textFieldGrp('corrective_tab2_sdk_replace_TFG',label='replace with : ', text='R_',columnWidth=([1,100],[2,105]),columnAttach=[(1, 'both', 0),(2, 'both', 0)])
    cmds.setParent('..')
    cmds.button(label='Mirror',w=90,h=45,command = lambda *args:buttonCommand_mirrorSelectTargetInputSDK())
    cmds.setParent('corrective_tab2_subTab_tabLayout')

    cmds.columnLayout('corrective_tab2_rebuildTarget_columnLayout',adj=True)
    cmds.button(label='developing',h=85)
    cmds.setParent('corrective_tab2_subTab_tabLayout')

    #tab2_subTab set
    cmds.tabLayout( corrective_mainTabLayout01, edit=True, tabLabel=((corrective_mainTabLayout01_child1, 'corrective'), (corrective_mainTabLayout01_child2, 'blendShape')) )
    cmds.tabLayout('corrective_tab2_subTab_tabLayout',e=True,tabLabel=[('corrective_tab2_mirror_columnLayout','mirror'),('corrective_tab2_rebuildTarget_columnLayout','developing')],st='corrective_tab2_mirror_columnLayout' )
    #showUI
    cmds.showWindow('corrective_mainWindow')






