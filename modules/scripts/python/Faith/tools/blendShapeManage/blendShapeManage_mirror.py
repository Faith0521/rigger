# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import sys, math, os, re, time
from functools import partial
from cgrig.libs.maya.cmds.rig import blendshape
__myBlog__ = ''
__version__ = 'v 3.0.0  date:2026/01/28'
__author__ = ''
__email__ = ''


def getMesh():
    sel = cmds.ls(sl=1)
    ret = 'Please Loading Mesh.'
    mesh = []
    for i in sel:
        if cmds.nodeType(i) == 'transform':
            mesh = i

    if len(mesh):
        BaseRelatives = cmds.listRelatives(mesh, f=1)[0]
        if cmds.nodeType(BaseRelatives) == 'mesh':
            ret = mesh
        else:
            ret = 'Please Loading Mesh.'
    return ret


def meshOrig(meshNode):
    MeshOrigList = []
    Mesh_Orig = cmds.listHistory(meshNode)
    for i in range(len(Mesh_Orig)):
        if cmds.nodeType(Mesh_Orig[i]) == 'mesh':
            if 'Orig' in Mesh_Orig[i]:
                if Mesh_Orig[i] != None:
                    if cmds.listConnections(Mesh_Orig[i] + '.worldMesh[0]', source=True):
                        MeshOrigList.append(Mesh_Orig[i])

    return MeshOrigList


def meshExists(mesh):
    try:
        listMesh = cmds.listRelatives(mesh, s=True, f=1)
        if cmds.nodeType(listMesh[0]) == 'mesh':
            return True
        return False
    except TypeError:
        pass


def blendShapeNode_ONOFF():
    Nua = 0
    if cmds.textFieldGrp('meshShapeText', ex=1) == 1:
        obj = cmds.textFieldGrp('meshShapeText', query=True, text=True)
        if meshExists(obj):
            bsnodes = blendshape.getBlendshapeNodes(obj)
            if len(bsnodes):
                Nua = 1
    return Nua


def blendShapeNode(MeshNode):
    BlendShapeNode = []
    try:
        meshHistory = cmds.listHistory(MeshNode, pdo=True)
        BlendShapeNode = cmds.ls(meshHistory, type='blendShape')
    except TypeError:
        pass
    return BlendShapeNode


def blendShapeTextField():
    BlendShape_Node = blendShapeNode(cmds.textFieldGrp('meshShapeText', query=True, text=True))
    if BlendShape_Node.__len__() != 0:
        BlendShape_N = BlendShape_Node[0]
    else:
        BlendShape_N = ''
    return BlendShape_N


def Create_UI():
    cmds.columnLayout('')
    cmds.textFieldButtonGrp('newNameText', label='Name for new target:', cw3=(120, 260, 80), bl='Create', bc='CreateFinishtextFieldButton()')
    cmds.text(label='Options', height=20)
    cmds.checkBox('HideBox', label='Hide skinned mesh during blendShape target creation', height=20, value=True)
    cmds.checkBox('CreateBox', label='Create blendShapeNode,if not existing', align='left', height=20, value=True)
    cmds.checkBox('ConnectBox', label='Connect target to blendShapeNode', align='center', height=20, value=True)
    cmds.checkBox('DeletePoseBox', label='Delete inBindPose ', align='center', height=20, value=True)
    cmds.checkBox('DeleteBox', label='Delete target', align='center', height=20, value=False)
    cmds.frameLayout(w=435, label='Correct Space Driver', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=1)
    cmds.setParent('..')
    cmds.setParent('..')


def loadText(FieldButtonGrp):
    selObj = cmds.ls(sl=1)
    if len(selObj) > 0:
        cmds.textFieldButtonGrp(FieldButtonGrp, edit=True, text=selObj[0])


def blendShapeManage():
    version = __version__
    if cmds.window('blendShapeManage', exists=True):
        cmds.deleteUI('blendShapeManage')
    cmds.window('blendShapeManage', mb=True, t='BlendShapeManage_' + version)
    cmds.menu(l='Edit')
    cmds.menuItem(l='Append', c='ggbs.CreativeBlendShape().AppendTarget()')
    cmds.menuItem(l='Delete', c='ggbs.CreativeBlendShape().RemoveTarget()')
    cmds.menuItem(l='Gain', c='ggbs.CreativeBlendShape().GainTarget()')
    cmds.menuItem(l='Rename', c='ggbs.CreativeBlendShape().RenameTarget()')
    cmds.menuItem(l='RevertTarget', c='ggbs.CreativeBlendShape().GainTarget_All_for()')
    cmds.setParent('..')
    cmds.menu(l='Help')
    cmds.menuItem(d=True)
    cmds.menuItem(label='Close', c="cmds.window('blendShapeManage',e=True,vis=0)")
    cmds.menuItem(label=version)
    cmds.columnLayout('')
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 380)])
    cmds.button('buttonBlendShapeMesh', label='Reload\nModel', c='ggbs.reloadMesh(ggbs.getMesh())')
    cmds.textFieldGrp('meshShapeText', text='Please Loading Mesh.', ed=False, cw1=375)
    cmds.text(l='INPUT')
    cmds.text('blendShapeText', label=blendShapeTextField(), align='left')
    cmds.setParent('..')
    form_mian = cmds.formLayout()
    tabs = cmds.tabLayout('tabs', innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout(form_mian, edit=True, attachForm=((tabs, 'top', 0),
     (tabs, 'left', 0),
     (tabs, 'bottom', 0),
     (tabs, 'right', 0)))
    cmds.columnLayout('child1')
    Edit_UI()
    cmds.setParent('..')
    cmds.columnLayout('child2', en=1)
    Clone_UI()
    cmds.setParent('..')
    cmds.tabLayout(tabs, sc='ggbs.freshTargetBlendShape("append")', edit=True, tabLabel=(('child1', 'Edit'), ('child2', 'Clone')), st='child2')
    cmds.setParent('..')
    cmds.showWindow('blendShapeManage')
    cmds.window('blendShapeManage', edit=True, w=450, h=600)


def Edit_UI():
    cmds.columnLayout(adj=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 300), (2, 23), (3, 100)])
    cmds.text('availableText', l='Available blendShape target: ', font='boldLabelFont')
    cmds.text(l='')
    cmds.text('InbetweenText', l='Inbetween weight:')
    cmds.columnLayout()
    cmds.popupMenu(mm=True)
    cmds.menuItem(l='Delete', rp='S', c='ggbs.RemoveTarget()')
    cmds.menuItem(l='Gain', rp='W', c='ggbs.GainTarget()')
    cmds.menuItem(l='Rename', rp='E', c='ggbs.RenameTarget()')
    cmds.textScrollList('targetBlendShapeText', height=200, width=295, sc='ggbs.inbetweenWieght(),ggbs.getBlendShapeIndex()')
    cmds.setParent('..')
    cmds.text(l=' => ')
    cmds.columnLayout(adj=1)
    text2 = cmds.textScrollList('targetInbetweenText', allowMultiSelection=True, height=155, width=95, sc='ggbs.setBlendShape()')
    cmds.floatField('InbetweenField', w=100, en=False)
    cmds.button(l=' inputGeomTarget ', c='ggbs.CreativeBlendShape().inputGeomTarget()', en=0)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l='', h=5)
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 215), (2, 215)])
    b2 = cmds.button('EditFinsihButton', label='Edit', c='ggbs.EditFinishButton()', en=0)
    cmds.button(label='Cancel', en=0)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(w=435, label='In-between', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True, en=0)
    cmds.columnLayout(adj=1)
    cmds.checkBoxGrp('Inbetween', label='Add in-between target:', columnWidth=(1, 160), of1='ggbs.inbetweenBox()', on1='ggbs.inbetweenBox()')
    cmds.floatSliderGrp('InbetweenSlider', label='In-between weight:', field=True, min=-10.0, max=10.0, pre=2, enable=False, adj=3, en=0, cw3=(140, 80, 200))
    cmds.button('EditAddbetweenButton', label='inbetweenEdit', c='ggbs.inbetweenEditAddButton()', width=50, enable=False)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='MirrorShape', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    rb1 = cmds.radioButtonGrp('MirrorAxis', numberOfRadioButtons=3, l='Mirror Axis : ', labelArray3=('X', 'Y', 'Z'), sl=1, cw4=(85, 30, 30, 30), ct4=('left', 'left', 'left', 'left'))
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 300), (2, 120)])
    rb2 = cmds.radioButtonGrp('Position_of_MirrorsShapes', numberOfRadioButtons=2, l='Position of mirrors Shapes : ', labelArray2=('Shape', 'Original'), sl=2, cw3=(140, 80, 80), ct3=('left', 'left', 'left'))
    cmds.checkBox('DeleteMirrorObjBox', l='Delete Mirror Object', v=1)
    cmds.setParent('..')
    shapeOffset = cmds.floatFieldGrp('DuplicationOffset', label='==> Duplication Offset (shape mode) : ', numberOfFields=3, cw4=(200, 60, 60, 60), en=0)
    cmds.radioButtonGrp(rb2, e=1, cc="putOffsetInGray('" + shapeOffset + "','" + rb2 + "')")
    cmds.textFieldButtonGrp('Target_Text', label='Target : ', cw3=(100, 250, 120), bl=' <<<< ', en=0)
    cmds.textFieldButtonGrp('MirrorTargetText', label='Shape(s) to Copy : ', cw3=(100, 250, 120), bl=' Mirror ', bc='ggbs.CreativeBlendShape().MirrorBlendShape(0)')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='Mirror>Target', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 45),
     (2, 180),
     (3, 40),
     (4, 180)])
    cmds.checkBox('autoMirrorTargetNameCB', l='Auto', v=1)
    cmds.textField('targetField', tx='Target', en=0)
    cmds.text(l=' =>>= ')
    cmds.textField('sourceField', tx='Source', en=0)
    cmds.text(l='')
    cmds.button(l='Target', c='ggbs.editField("targetField")')
    cmds.text(l='')
    cmds.button(l='Source', c='ggbs.editField("sourceField")')
    cmds.setParent('..')
    cmds.button(l='Apply', w=435, c='ggbs.CreativeBlendShape().MirrorBlendShape(1)')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='Rebuild Target Items', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    cmds.text(l=u'运行前请确保除blendShape以外的变形器没有对模型造成变形效果')
    cmds.button(l='Rebuild Target Items', w=420, h=40, c="ggbs.rebuildTargetItems(cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True),'yes'),ggbs.reloadMesh(cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True))")
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label=u'target重新排序', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout('rearrangeTarget_CL')
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.textField('Target_strsTF', tx="['neck','head'\n,'L_shoulder','L_Tpose','L_arm'\n,'R_shoulder','R_Tpose','R_arm'\n,'L_elbow','L_hand'\n,'R_elbow','R_hand'\n,'finger'\n,'L_Leg','L_knee','L_foot','L_toe'\n,'R_Leg','R_knee','R_foot','R_toe','leg']", en=1, w=300, h=40)
    cmds.button(l=u'根据关键字排列target列表', h=40, c="ggbs.rearrangeTargetList(   cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True)   ,eval(cmds.textField('Target_strsTF',query=True,tx=True))   )")
    cmds.textField('rearrangeTargetTF', tx='', en=1, w=300, h=40)
    cmds.button(l=u'根据列表顺序重建target', h=40, c="ggbs.rearrangeTarget(   cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True)   ,'yes'   ,eval(cmds.textField('rearrangeTargetTF',q = True,tx = True))  )")
    cmds.setParent('rearrangeTarget_CL')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label=u'target批量镜像', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout('targetMirror_CL')
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.textField('Target_mirrorStrTF', tx='L_*=R_*,lf_*=rt_*,l_*=r_*,left_*=right_*,*_L=*_R,*_lf=*_rt,*_l=*_r,*_left=*_right,*_L_*=*_R_*,*_l_*=*_r_*,*_lf_*=*_rt_*,*_left_*=*_right_*', en=1, w=300, h=40)
    cmds.button(l=u'根据关键字整理对称的target列表', h=40, c="ggbs.targetMirrorList( cmds.textField('Target_mirrorStrTF',q = True,tx = True)  )")
    cmds.setParent('targetMirror_CL')
    cmds.textField('L_TargetList_TF', tx='', w=300, h=40)
    cmds.textField('R_TargetList_TF', tx='', w=300, h=40)
    cmds.button(l=u'批量镜像target', w=300, h=40, c="ggbs.CreativeBlendShape().MirrorBlendShapeList(1,  eval(cmds.textField('L_TargetList_TF',q = True,tx = True))  ,  eval(cmds.textField('R_TargetList_TF',q = True,tx = True))  )")
    cmds.setParent('targetMirror_CL')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')


def RemoveTarget():
    BlendShape = blendShapeTextField()
    tragetBlendShape = targetBlendShapeText()
    blendshape.delete_target(BlendShape, tragetBlendShape)
    freshTargetBlendShape('remove')

def inbetweenWieght():
    blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
    blendShape = blendShapeNode(blendShapeMesh)
    tragetBlendShapeIndex = targetBlendShapeText()
    if tragetBlendShapeIndex[:2] == 'L_':
        mirrortragetBlendShapeIndex = 'R_' + tragetBlendShapeIndex[2:]
    elif tragetBlendShapeIndex[:2] == 'R_':
        mirrortragetBlendShapeIndex = 'L_' + tragetBlendShapeIndex[2:]
    elif tragetBlendShapeIndex[:2] == 'lf_':
        mirrortragetBlendShapeIndex = 'rt_' + tragetBlendShapeIndex[2:]
    elif tragetBlendShapeIndex[:2] == 'rt_':
        mirrortragetBlendShapeIndex = 'lf_' + tragetBlendShapeIndex[2:]
    elif tragetBlendShapeIndex[:2] == 'l_':
        mirrortragetBlendShapeIndex = 'r_' + tragetBlendShapeIndex[:2]
    elif tragetBlendShapeIndex[:2] == 'r_':
        mirrortragetBlendShapeIndex = 'l_' + tragetBlendShapeIndex[:2]
    elif tragetBlendShapeIndex[-2:] == '_l':
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex[:-2] + '_r'
    elif tragetBlendShapeIndex[-2:] == '_r':
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex[:-2] + '_l'
    elif tragetBlendShapeIndex[-2:] == '_L':
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex[:-2] + '_R'
    elif tragetBlendShapeIndex[-2:] == '_R':
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex[:-2] + '_L'
    elif '_L_' in tragetBlendShapeIndex:
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex.replace('_L_', '_R_')
    elif '_R_' in tragetBlendShapeIndex:
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex.replace('_R_', '_L_')
    elif '_lf_' in tragetBlendShapeIndex:
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex.replace('_lf_', '_rt_')
    elif '_rt_' in tragetBlendShapeIndex:
        mirrortragetBlendShapeIndex = tragetBlendShapeIndex.replace('_rt_', '_lf_')
    else:
        mirrortragetBlendShapeIndex = ''
    tragetIndexItem = blendshape.get_index(blendShape[0], tragetBlendShapeIndex)
    inputTargetItem = cmds.getAttr(blendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
    cmds.textScrollList('targetInbetweenText', edit=True, removeAll=True)
    if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
        cmds.floatSliderGrp('InbetweenSlider', edit=True, v=0)
    for i in inputTargetItem:
        indexInt = (int(i) - 5000) / 1000.0
        cmds.textScrollList('targetInbetweenText', edit=True, append=str(indexInt), sii=1)

    cmds.textFieldButtonGrp('Target_Text', tx=tragetBlendShapeIndex, edit=True)
    cmds.textFieldButtonGrp('MirrorTargetText', tx=mirrortragetBlendShapeIndex, edit=True)
    cmds.textField('targetField', tx=tragetBlendShapeIndex, e=True)
    if cmds.checkBox('autoMirrorTargetNameCB', q=True, v=True) == False:
        mirrortragetBlendShapeIndex = ''
    cmds.textField('sourceField', tx='', e=True)
    if mirrortragetBlendShapeIndex in cmds.textScrollList('targetBlendShapeText', q=1, ai=1):
        cmds.textField('sourceField', tx=mirrortragetBlendShapeIndex, e=True)


def editTargetVlue():
    bs_target = cmds.textScrollList('targetBlendShapeText', q=True, si=True)[0]
    target_value = cmds.floatSliderGrp('seltargetFSG', q=True, value=True)
    cmds.setAttr(blendShapeTextField() + '.' + bs_target, target_value)


def rearrangeTargetList(TargetGeo, tar_strs):
    TargetBlendShapeList = blendShapeNode(TargetGeo)
    if TargetBlendShapeList != [] and len(TargetBlendShapeList) == 1:
        TargetBlendShape = TargetBlendShapeList[0]
        if TargetBlendShape == TargetGeo + '_blendShape':
            TargetBlendShape = cmds.rename(TargetBlendShape, TargetBlendShape + '_old')
    elif len(TargetBlendShapeList) > 1:
        cmds.error(u'#------More than one blendShape Node')
    elif TargetBlendShapeList == []:
        cmds.error('#------There is no blendShape Node')
    if cmds.getAttr(TargetBlendShape + '.envelope') != 1:
        cmds.setAttr(TargetBlendShape + '.envelope', 1)
    listTarget = cmds.listAttr(TargetBlendShape + '.weight', multi=True)
    newTargets = []
    specialTars = []
    noRightTars = []
    noLeftTars = []
    for tar_str in tar_strs:
        for bs_target in listTarget:
            if bs_target not in newTargets:
                if tar_str in bs_target:
                    newTargets.append(bs_target)
                    if bs_target[:2] == 'L_':
                        if 'R_' + bs_target[2:] not in listTarget:
                            noRightTars.append(bs_target)
                    if bs_target[:2] == 'R_':
                        if 'L_' + bs_target[2:] not in listTarget:
                            noLeftTars.append(bs_target)

    for bs_target in listTarget:
        if bs_target not in newTargets:
            specialTars.append(bs_target)

    newTarget2s = newTargets + specialTars
    print('[')
    for target1 in newTarget2s:
        print("'" + target1 + "',")

    print(']')
    print(len(listTarget), '---', len(newTarget2s))
    print(u'\u5de6\u8fb9\u5f62\u6001\uff0c\u53f3\u8fb9\u6ca1\u6709---', noRightTars)
    print(u'\u53f3\u8fb9\u5f62\u6001\uff0c\u5de6\u8fb9\u6ca1\u6709---', noLeftTars)
    print(u'\u4e0d\u5728\u4e0a\u8ff0\u89c4\u5219\u4e2d\u7684target,\u653e\u5728\u5217\u8868\u6700\u540e---', specialTars)
    print(newTarget2s)


def targetMirrorList(mirrorStrList):
    listTarget = cmds.listAttr(blendShapeTextField() + '.weight', multi=True)
    print(listTarget)
    print(mirrorStrList)
    mirrorStrList = mirrorStrList.split(',')
    print(mirrorStrList)
    listTarget1 = []
    L_targetList = []
    R_targetList = []
    m_targetList = []
    for bs_target in listTarget:
        if bs_target not in listTarget1:
            for mirrorStr in mirrorStrList:
                mirrorStr = mirrorStr.split('=')
                L_Str = mirrorStr[0]
                R_Str = mirrorStr[1]
                if L_Str[-1] == '*' and L_Str[0] != '*':
                    L_Str = L_Str[:-1]
                    R_Str = R_Str[:-1]
                    L_str_len = len(L_Str)
                    if bs_target[:L_str_len] == L_Str:
                        R_target = R_Str + bs_target[L_str_len:]
                        if R_target in listTarget:
                            L_targetList.append(bs_target)
                            R_targetList.append(R_target)
                            listTarget1.append(bs_target)
                            listTarget1.append(R_target)
                            break
                elif L_Str[0] == '*' and L_Str[-1] != '*':
                    L_Str = L_Str[1:]
                    R_Str = R_Str[1:]
                    L_str_len = len(L_Str)
                    if bs_target[-L_str_len:] == L_Str:
                        R_target = bs_target[:-L_str_len] + R_Str
                        if R_target in listTarget:
                            L_targetList.append(bs_target)
                            R_targetList.append(R_target)
                            listTarget1.append(bs_target)
                            listTarget1.append(R_target)
                            break
                elif L_Str[0] == '*' and L_Str[-1] == '*':
                    L_Str = L_Str[1:-1]
                    R_Str = R_Str[1:-1]
                    L_str_len = len(L_Str)
                    if L_Str in bs_target:
                        R_target = bs_target.replace(L_Str, R_Str)
                        if R_target in listTarget:
                            L_targetList.append(bs_target)
                            R_targetList.append(R_target)
                            listTarget1.append(bs_target)
                            listTarget1.append(R_target)
                            break

    for bs_target in listTarget:
        if bs_target not in L_targetList and bs_target not in R_targetList:
            m_targetList.append(bs_target)

    print(u'\u539f\u59cbtarget\u6570\u91cf', len(listTarget))
    print(u'\u5de6\u53f3target\u6570\u91cf + \u4e2d\u95f4target\u6570\u91cf=', len(L_targetList), ' + ', len(R_targetList), '+', len(m_targetList), '=', len(L_targetList + R_targetList + m_targetList))
    print(u'\u5de6\u8fb9\u7684target\n', L_targetList)
    print(u'\u53f3\u8fb9\u7684target\n', R_targetList)
    print(u'\u4e2d\u95f4\u7684target\n', m_targetList)
    for bs_target in listTarget:
        if bs_target in L_targetList and bs_target in R_targetList:
            print(bs_target)
        if bs_target in L_targetList and bs_target in m_targetList:
            print(bs_target)
        if bs_target in R_targetList and bs_target in m_targetList:
            print(bs_target)


def freeze_channelBox(nodeName, *attr):
    for a in attr:
        mc.setAttr('%s.%s' % (nodeName, a), 0)


def selectTargetBlendShapeText():
    last = cmds.textScrollList('targetBlendShapeText', q=1, ai=1)[-1]
    cmds.textScrollList('targetBlendShapeText', si=last, e=1)


def cueDialog(text, title):
    result = cmds.promptDialog(title=title, text=text, message='Enter New Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
    elif result == 'Cancel':
        text = ''
    return text


def select_olDrv(temp):
    selectItems = cmds.textScrollList('olDrv_tcl', q=1, si=1)
    cmds.select(cl=1)
    if temp == 1:
        for i in selectItems:
            cmds.select(i, tgl=1)

    if temp == 0:
        cmds.select(cl=1)


def Clone_UI():
    cmds.columnLayout('', adj=True)
    cmds.textFieldButtonGrp('TargetGoemerty', label='Target Goemerty:', tx=getMesh(), cw3=(100, 280, 200), bl='Reload', bc='', ed=False, eb=False)
    cmds.textFieldButtonGrp('SourceGoemerty', label='Source Goemerty:', cw3=(100, 280, 200), bl='Reload')
    cmds.textFieldButtonGrp('SourceGoemerty', e=True, bc='ggbs.loadText("SourceGoemerty")')
    cmds.button(label='Apply', c='ggbs.creativeTargetClone()')
    cmds.button('cloneButton', l='Clone Target List', c='ggbs.Edit_CloneButton()')
    cmds.frameLayout('cloneFrame', label='Clone List', mw=5, mh=5, la='center', cll=1, cl=1)
    cmds.textFieldButtonGrp('selTarget_TF_but', label='Select Target:', cw3=(100, 280, 200), bl='select')
    cmds.textFieldButtonGrp('selTarget_TF_but', e=True, bc='ggbs.select_by_keyword()')
    cmds.rowColumnLayout(numberOfColumns=5)
    selTarget_ui_w1 = 83
    cmds.button(label='shoulder', c='ggbs.sel_tar_CB(["shoulder"])', w=selTarget_ui_w1)
    cmds.button(label='arm', c='ggbs.sel_tar_CB(["arm"])', w=selTarget_ui_w1)
    cmds.button(label='elbow', c='ggbs.sel_tar_CB(["elbow"])', w=selTarget_ui_w1)
    cmds.button(label='wrist , hand', c='ggbs.sel_tar_CB(["wrist","hand"])', w=selTarget_ui_w1)
    cmds.button(label='finger', c='ggbs.sel_tar_CB(["finger","middle","index","ring","pinky","thumb"])', w=selTarget_ui_w1)
    cmds.button(label='leg', c='ggbs.sel_tar_CB(["leg"])', w=selTarget_ui_w1)
    cmds.button(label='knee', c='ggbs.sel_tar_CB(["knee"])', w=selTarget_ui_w1)
    cmds.button(label='ankle', c='ggbs.sel_tar_CB(["ankle"])', w=selTarget_ui_w1)
    cmds.button(label='toe', c='ggbs.sel_tar_CB(["toe"])', w=selTarget_ui_w1)
    cmds.button(label='neck , head', c='ggbs.sel_tar_CB(["neck","head"])', w=selTarget_ui_w1)
    cmds.setParent('..')
    cmds.scrollLayout('cloneList', horizontalScrollBarThickness=16, verticalScrollBarThickness=16, h=285)
    cmds.rowColumnLayout('clone_rclayout', numberOfColumns=2)
    cmds.setParent('cloneFrame')
    cmds.text(
        l='红色无连接且数值大于0，黄色无连接且数值为0\n蓝色有连接但数值大于0，灰色有连接数值为0\n没有勾选的Target会保持当前数值,包裹时不操作数值'
    )
    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.checkBox(
        'delTargetCB',  # 复选框名称
        l='删除目标体',  # label：复选框显示文本
        ann='克隆完成后自动删除目标体',  # annotation：鼠标悬停提示
        v=1  # value：默认勾选
    )
    cmds.setParent('cloneFrame')
    cmds.button(
        'cloneSelInvertBut',  # 按钮名称
        l='反选',  # label：按钮显示文本
        c='ggbs.cloneSelInvert()'  # command：点击按钮执行的命令
    )
    cmds.setParent('..')


def getcloneTarget_vlaue_List():
    if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
        cloneTarget_value_List = cmds.rowColumnLayout('clone_rclayout', q=1, childArray=1)
        cloneList = []
        targetValues = []
        for cloneTarget_value in cloneTarget_value_List:
            if 'Clone_' in cloneTarget_value:
                cloneList.append(cloneTarget_value)
            elif 'targetValue_' in cloneTarget_value:
                targetValues.append(cloneTarget_value)

    else:
        cloneList = []
        targetValues = []
    return (cloneList, targetValues)


def select_by_keyword():
    input_text = cmds.textFieldButtonGrp('selTarget_TF_but', query=True, tx=True)
    cleaned_text = input_text.strip() if input_text else ""
    # 处理关键词：有逗号则分割，无逗号则作为单个关键词，过滤空字符串
    if cleaned_text:
        # 分割后对每个关键词再次清洗，过滤分割后产生的空值（比如输入",,test,,")
        keywords = [kw.strip() for kw in cleaned_text.split(',') if kw.strip()]
    else:
        keywords = []

    # 调用回调函数（可增加空值提示，提升用户体验）
    if not keywords:
        cmds.warning(u"未输入有效的关键词，请检查输入内容！")
    sel_tar_CB(keywords)


def sel_tar_CB(sel_target_names):
    """
    关键词匹配勾选复选框的回调函数
    根据输入的关键词列表，匹配Clone_前缀的复选框并勾选（仅在cloneButton标签为Cancel时执行）

    Args:
        sel_target_names (list): 用于匹配的关键词列表
    """
    # 1. 校验克隆按钮状态，非Cancel则直接返回
    if cmds.button('cloneButton', q=True, label=True) != 'Cancel':
        return

    # 2. 获取布局下所有子组件并遍历
    for widget in cmds.rowColumnLayout('clone_rclayout', q=True, childArray=True):
        # 3. 筛选Clone_前缀的复选框，按关键词（忽略大小写）匹配
        if 'Clone_' in widget and any(kw.lower() in widget.lower() for kw in sel_target_names):
            cmds.checkBox(widget, e=True, value=True)


def creativeTargetClone():
    """
    克隆 BlendShape 目标体核心函数
    功能：根据界面控件的配置，将指定源模型的 BlendShape 目标体克隆到目标模型
    """
    # 1. 获取界面控件的关键参数
    # 目标模型名称（从文本框按钮组获取）
    target_geometry = cmds.textFieldButtonGrp('TargetGoemerty', query=True, text=True)
    # 源模型名称（从文本框按钮组获取）
    source_geometry = cmds.textFieldButtonGrp('SourceGoemerty', query=True, text=True)
    # 获取克隆目标体的列表数据
    clone_targets_data = getcloneTarget_vlaue_List()
    clone_list = clone_targets_data[0]

    # 2. 判断是否需要删除原有目标体（简化三元表达式替代 if-else）
    is_delete_target = cmds.checkBox('delTargetCB', query=True, value=True)

    # 3. 筛选需要克隆的目标体列表（仅当克隆按钮标签为 Cancel 时执行）
    selected_clone_list = None
    if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
        selected_clone_list = []
        # 遍历所有可选的克隆目标体，筛选勾选的项
        for clone_target in clone_list:  # 简化遍历方式，直接迭代列表而非索引
            if cmds.checkBox(clone_target, query=True, value=True):
                # 获取勾选项的注释（即目标体名称）并加入列表
                target_annotation = cmds.checkBox(clone_target, query=True, annotation=True)
                selected_clone_list.append(target_annotation)

    # 4. 执行 BlendShape 目标体克隆核心操作
    blendshape.copyBs(
        target_geometry,
        source_geometry,
        skipLock=True,
        replaceConnect=True,
        cloneList=selected_clone_list,
        delTarget=is_delete_target
    )


def Clone_list_on():
    if blendShapeNode_ONOFF() == True:
        blendShapeNode = blendShapeTextField()
        targetBlendShape = blendshape.getTargetList(blendShapeNode)
        targetInt = cmds.blendShape(blendShapeNode, query=True, wc=True)
        if targetInt > 0:
            for t in targetBlendShape:
                targetValue = cmds.getAttr(blendShapeNode + '.' + t)
                targetConnect = cmds.listConnections(blendShapeNode + '.' + t, p=True, s=True, d=False)
                if targetValue < 0.0001:
                    targetValue = 0
                if targetConnect == None and targetValue >= 0.001:
                    cmds.text('targetValue_%s' % t, l='%.2g' % targetValue, p='clone_rclayout', en=0, w=40, bgc=[0.8, 0, 0])
                elif targetConnect == None:
                    cmds.text('targetValue_%s' % t, l='%.2g' % targetValue, p='clone_rclayout', en=0, w=40, bgc=[0.8, 0.8, 0])
                elif targetValue >= 0.0001 and targetConnect != None:
                    cmds.text('targetValue_%s' % t, l='%.2g' % targetValue, p='clone_rclayout', en=0, w=40, bgc=[0, 0.45, 1])
                else:
                    cmds.text('targetValue_%s' % t, l='%.2g' % targetValue, p='clone_rclayout', en=0, w=40)
                cmds.checkBox('Clone_%s' % t, l=t, p='clone_rclayout', ann='%s' % t)

            if len(targetBlendShape) * 20 > 400:
                scrollLayout_h = 400
            elif len(targetBlendShape) * 20 < 200:
                scrollLayout_h = 200
            else:
                scrollLayout_h = len(targetBlendShape) * 20
    cmds.frameLayout('cloneFrame', e=1, cl=0)
    return


def Clone_list_off():
    cmds.deleteUI(cmds.rowColumnLayout('clone_rclayout', q=1, fpn=1))
    cmds.rowColumnLayout('clone_rclayout', numberOfColumns=2, p='cloneList')
    cmds.frameLayout('cloneFrame', e=1, cl=1)


def Edit_CloneButton():
    buttonLebal = cmds.button('cloneButton', query=True, label=True)
    if blendShapeNode_ONOFF() == True:
        if buttonLebal == 'Clone Target List':
            cmds.button('cloneButton', edit=True, label='Cancel')
            Clone_list_on()
    if buttonLebal == 'Cancel':
        cmds.button('cloneButton', edit=True, label='Clone Target List')
        Clone_list_off()
    if blendShapeNode_ONOFF() == 0:
        Dialog = 'The Goemerty has no BlendShape node.'
        cmds.confirmDialog(title='Confirm', message=Dialog, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        cmds.text('blendShapeText', e=True, label=blendShapeTextField())


def cloneSelInvert():
    cloneList = getcloneTarget_vlaue_List()[0]
    for b in cloneList:
        if cmds.checkBox(b, q=1, v=1) == 1:
            cmds.checkBox(b, e=1, v=0)
        else:
            cmds.checkBox(b, e=1, v=1)


def InputTargetGroup(blendShapeNode, target):
    tragetIndexItem = blendshape.get_index(blendShapeNode, target)
    return tragetIndexItem


def freshTargetBlendShape(temp, fresh = None):
    targetName = targetBlendShapeText()
    if temp == 'append':
        if blendShapeNode_ONOFF() == True:
            targetBlendShape = blendshape.getTargetList(blendShapeTextField())
            cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=True)
            targetInt = cmds.blendShape(blendShapeTextField(), query=True, wc=True)

            if targetInt > 0:
                for t in targetBlendShape:
                    cmds.textScrollList('targetBlendShapeText', edit=True, append=t)

            if cmds.tabLayout('tabs', q=1, sti=1) == 3:
                if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
                    Clone_list_off()
                    Clone_list_on()
        else:
            cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=1)
    if temp == 'remove':
        cmds.textScrollList('targetBlendShapeText', edit=True, ri=targetName)
    if fresh != None:
        cmds.textScrollList('targetBlendShapeText', si=fresh, e=1)
    if blendShapeNode_ONOFF() == True:
        targetBlendShape = cmds.listAttr(blendShapeTextField() + '.weight', multi=True)
        if targetBlendShape == None:
            cmds.text('availableText', edit=True, l='No BlendShape target', bgc=[0.8, 0, 0])
        else:
            targetItems = cmds.textScrollList('targetBlendShapeText', query=True, ni=True)
            Target_neg1_num = InputTargetGroup(blendShapeTextField(), targetBlendShape[-1])
            if targetItems - 1 == Target_neg1_num:
                targetNumhint = u'序号正确'
                bgc = [0, 0.4, 0]
            else:
                targetNumhint = u'序号错误\n序号是从 0 开始的，最高序号比target数量少1才对'
                bgc = [0.8, 0.8, 0]
            cmds.text('availableText', edit=True, bgc=bgc,
                      l='target数量:' + str(targetItems) + '--最高序号:' + str(Target_neg1_num) + '--' + targetNumhint)
    else:
        cmds.text('availableText', edit=True, l='No BlendShape Node', bgc=[0.8, 0, 0])


def rebuildTargetItems(TargetGeo, delTarget):
    sels = cmds.ls(sl=True, type='transform')
    listConnect = []
    listConnect_target = []
    listConnect_get = []
    TargetBlendShapeList = blendShapeNode(TargetGeo)
    if TargetBlendShapeList != [] and len(TargetBlendShapeList) == 1:
        TargetBlendShape = TargetBlendShapeList[0]
        if TargetBlendShape == TargetGeo + '_blendShape':
            TargetBlendShape = cmds.rename(TargetBlendShape, TargetBlendShape + '_old')
    elif len(TargetBlendShapeList) > 1:
        cmds.error(u'#------More than one blendShape Node')
    elif TargetBlendShapeList == []:
        cmds.error('#------There is no blendShape Node')
    if cmds.getAttr(TargetBlendShape + '.envelope') != 1:
        cmds.setAttr(TargetBlendShape + '.envelope', 1)
    listTarget = cmds.listAttr(TargetBlendShape + '.weight', multi=True)
    listShpae = cmds.listRelatives(TargetGeo, s=True)
    listTargetBlendShape = listTarget
    TargetGeoNewBlendShape = TargetGeo + '_blendShape'
    TargetGeoNewBlendShape = cmds.blendShape(TargetGeo, exclusive='deformPartition#', frontOfChain=True, name=TargetGeoNewBlendShape)[0]
    xi = 0
    for i in listTargetBlendShape:
        targetConnect = cmds.listConnections(TargetBlendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, TargetBlendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        else:
            get = i + '>' + str(cmds.getAttr(TargetBlendShape + '.' + i))
            listConnect_get.append(get)
        cmds.setAttr(TargetBlendShape + '.' + i, 0)

    for x in listTargetBlendShape:
        tragetIndexItem = InputTargetGroup(TargetBlendShape, x)
        inputTargetItem = cmds.getAttr(TargetBlendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        ToNames = creativeTarget(TargetBlendShape, [x], None)
        for i in range(len(inputTargetItem)):
            c = inputTargetItem[i]
            ToName = ToNames[i]
            indexInt = (int(c) - 5000) / 1000.0
            if float(indexInt) == 1:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 1.0))
            else:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, ib=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 float(indexInt)))

        if delTarget == 'yes':
            cmds.delete(ToNames)
        xi += 1

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], TargetBlendShape + '.' + listConnect_target[i])
        cmds.connectAttr(listConnect[i], TargetGeoNewBlendShape + '.' + listConnect_target[i])

    for i in listConnect_get:
        listConnect_wt = i.split('>')
        cmds.setAttr(TargetBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))
        cmds.setAttr(TargetGeoNewBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))

    cmds.delete(TargetBlendShape)
    cmds.select(sels)
    return


def rearrangeTarget(TargetGeo, delTarget, listTarget):
    sels = cmds.ls(sl=True, type='transform')
    listConnect = []
    listConnect_target = []
    listConnect_get = []
    TargetBlendShapeList = blendShapeNode(TargetGeo)
    if TargetBlendShapeList != [] and len(TargetBlendShapeList) == 1:
        TargetBlendShape = TargetBlendShapeList[0]
        if TargetBlendShape == TargetGeo + '_blendShape':
            TargetBlendShape = cmds.rename(TargetBlendShape, TargetBlendShape + '_old')
    elif len(TargetBlendShapeList) > 1:
        cmds.error(u'#------More than one blendShape Node')
    elif TargetBlendShapeList == []:
        cmds.error('#------There is no blendShape Node')
    if cmds.getAttr(TargetBlendShape + '.envelope') != 1:
        cmds.setAttr(TargetBlendShape + '.envelope', 1)
    listShpae = cmds.listRelatives(TargetGeo, s=True)
    listTargetBlendShape = listTarget
    TargetGeoNewBlendShape = TargetGeo + '_blendShape'
    TargetGeoNewBlendShape = cmds.blendShape(TargetGeo, exclusive='deformPartition#', frontOfChain=True, name=TargetGeoNewBlendShape)[0]
    xi = 0
    for i in listTargetBlendShape:
        targetConnect = cmds.listConnections(TargetBlendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, TargetBlendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        else:
            get = i + '>' + str(cmds.getAttr(TargetBlendShape + '.' + i))
            listConnect_get.append(get)
        cmds.setAttr(TargetBlendShape + '.' + i, 0)

    for x in listTargetBlendShape:
        tragetIndexItem = InputTargetGroup(TargetBlendShape, x)
        inputTargetItem = cmds.getAttr(TargetBlendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        ToNames = creativeTarget(TargetBlendShape, [x], None)
        for i in range(len(inputTargetItem)):
            c = inputTargetItem[i]
            ToName = ToNames[i]
            indexInt = (int(c) - 5000) / 1000.0
            if float(indexInt) == 1:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 1.0))
            else:
                cmds.blendShape(TargetGeoNewBlendShape, edit=True, ib=True, tc=False, target=(TargetGeo,
                 xi,
                 ToName,
                 float(indexInt)))

        if delTarget == 'yes':
            cmds.delete(ToNames)
        xi += 1

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], TargetBlendShape + '.' + listConnect_target[i])
        cmds.connectAttr(listConnect[i], TargetGeoNewBlendShape + '.' + listConnect_target[i])

    for i in listConnect_get:
        listConnect_wt = i.split('>')
        cmds.setAttr(TargetBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))
        cmds.setAttr(TargetGeoNewBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))

    cmds.delete(TargetBlendShape)
    cmds.select(sels)
    return


def targetBlendShapeText():
    targetBlendShape_Text = cmds.textScrollList('targetBlendShapeText', query=True, selectItem=True)
    if targetBlendShape_Text == None:
        targetBlendShape = 'None'
    else:
        targetBlendShape = targetBlendShape_Text[0].split('[')
    return targetBlendShape[0]


def getBlendShapeIndex():
    tarName = cmds.textScrollList('targetBlendShapeText', q=True, si=True)[0]
    tarIndex = InputTargetGroup(blendShapeTextField(), tarName)
    cmds.floatField('InbetweenField', e=True, v=tarIndex)
    sys.stderr.write(str(tarIndex) + '---' + str(tarName) + '\n')


def setBlendShape():
    blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
    In = cmds.textScrollList('targetInbetweenText', query=True, si=True)
    tragetBlendShapeSel = targetBlendShapeText()


def inbetweenBox():
    if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
        cmds.floatSliderGrp('InbetweenSlider', edit=True, enable=0)
        cmds.button('EditFinsihButton', edit=True, enable=False)
        cmds.button('EditAddbetweenButton', edit=True, enable=True)
        cmds.textScrollList('targetInbetweenText', edit=True, enable=False)
    else:
        cmds.floatSliderGrp('InbetweenSlider', edit=True, enable=1)
        cmds.button('EditFinsihButton', edit=True, enable=True)
        cmds.button('EditAddbetweenButton', edit=True, enable=False)
        cmds.textScrollList('targetInbetweenText', edit=True, enable=True)


def inputTargetBlendShape(blendShape):
    inputTarget = cmds.listAttr(blendShape + '.inputTarget[0].inputTargetGroup[0]', multi=True)
    geomTarget = []
    for i in inputTarget:
        if i.find('inputGeomTarget') != -1:
            geomTarget.append(i)

    return geomTarget


def reloadMesh(sel):
    if len(sel) > 0 and meshExists(sel):
        meshShapeText = cmds.textFieldGrp('meshShapeText', text=sel, e=1)
        freshTargetBlendShape('append')
        cmds.text('blendShapeText', e=1, label=blendShapeTextField())
        cmds.textFieldButtonGrp('TargetGoemerty', e=1, tx=cmds.textFieldGrp('meshShapeText', text=1, q=1))
    else:
        meshShapeText = cmds.textFieldGrp('meshShapeText', text='No deformable objects selected.', e=1)
        cmds.text('blendShapeText', e=1, label='')


def putOffsetInGray(shapeOffset, rb2):
    if cmds.radioButtonGrp(rb2, q=1, sl=1) == 1:
        cmds.floatFieldGrp(shapeOffset, e=1, en=1)
    if cmds.radioButtonGrp(rb2, q=1, sl=1) == 2:
        cmds.floatFieldGrp(shapeOffset, e=1, en=0)


def FGMirrorShapes(originalObj, shapeToCopy, xyz, shapePosition, newName, shapeOffset):
    OriginalObjTX = originalObj + '.tx'
    cmds.setAttr(OriginalObjTX, lock=0)
    OriginalObjTY = originalObj + '.ty'
    cmds.setAttr(OriginalObjTY, lock=0)
    OriginalObjTZ = originalObj + '.tz'
    cmds.setAttr(OriginalObjTZ, lock=0)
    OriginalObjRX = originalObj + '.rx'
    cmds.setAttr(OriginalObjRX, lock=0)
    OriginalObjRY = originalObj + '.ry'
    cmds.setAttr(OriginalObjRY, lock=0)
    OriginalObjRZ = originalObj + '.rz'
    cmds.setAttr(OriginalObjRZ, lock=0)
    OriginalObjSX = originalObj + '.sx'
    cmds.setAttr(OriginalObjSX, lock=0)
    OriginalObjSY = originalObj + '.sy'
    cmds.setAttr(OriginalObjSY, lock=0)
    OriginalObjSZ = originalObj + '.sz'
    cmds.setAttr(OriginalObjSZ, lock=0)
    mirrorObj = shapeToCopy + 'suffTemp'
    cmds.duplicate(originalObj, rr=1, n='scaleObj')
    cmds.duplicate(originalObj, rr=1, n='tempName')
    cmds.rename('tempName', mirrorObj)
    cmds.setAttr(OriginalObjTX, lock=0)
    cmds.setAttr(OriginalObjTY, lock=0)
    cmds.setAttr(OriginalObjTZ, lock=0)
    cmds.setAttr(OriginalObjRX, lock=0)
    cmds.setAttr(OriginalObjRY, lock=0)
    cmds.setAttr(OriginalObjRZ, lock=0)
    cmds.setAttr(OriginalObjSX, lock=0)
    cmds.setAttr(OriginalObjSY, lock=0)
    cmds.setAttr(OriginalObjSZ, lock=0)
    posScaleAttr = 0
    negScaleAttr = 0
    if xyz == 1:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleX'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleX', negScaleAttr)
    if xyz == 2:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleY'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleY', negScaleAttr)
    if xyz == 3:
        posScaleAttr = float(cmds.getAttr('scaleObj.scaleZ'))
        negScaleAttr = -1 * posScaleAttr
        cmds.setAttr('scaleObj.scaleZ', negScaleAttr)
    cmds.blendShape(shapeToCopy, 'scaleObj', frontOfChain=1, n='blendShapeToWarp')
    cmds.select(mirrorObj, 'scaleObj', r=1)
    wrap = mel.eval('doWrapArgList "6" { "1","0","1", "2", "1", "1", "0" };')
    cmds.rename(wrap[0], 'wrapToMirror')
    cmds.setAttr('wrapToMirror.exclusiveBind', 1)
    blendShapeAttr = 'blendShapeToWarp.' + shapeToCopy
    cmds.setAttr(blendShapeAttr, 1)
    cmds.select(mirrorObj, r=1)
    cmds.DeleteHistory
    cmds.delete(ch=1)
    cmds.delete('scaleObjBase', 'scaleObj')
    offsetX = shapeOffset[0]
    offsetY = shapeOffset[1]
    offsetZ = shapeOffset[2]
    if shapePosition == 1:
        shapeTCAttrX = shapeToCopy + '.tx'
        shapeTCAttrY = shapeToCopy + '.ty'
        shapeTCAttrZ = shapeToCopy + '.tz'
        shapeTCPositionX = float(cmds.getAttr(shapeTCAttrX)) + offsetX
        shapeTCPositionY = float(cmds.getAttr(shapeTCAttrY)) + offsetY
        shapeTCPositionZ = float(cmds.getAttr(shapeTCAttrZ)) + offsetZ
        mirrorObjPositionX = mirrorObj + '.tx'
        mirrorObjPositionY = mirrorObj + '.ty'
        mirrorObjPositionZ = mirrorObj + '.tz'
        cmds.setAttr(mirrorObjPositionX, shapeTCPositionX)
        cmds.setAttr(mirrorObjPositionY, shapeTCPositionY)
        cmds.setAttr(mirrorObjPositionZ, shapeTCPositionZ)
    cmds.select(mirrorObj, r=1)
    cmds.rename(mirrorObj, newName)


def blendShapeExists(name):
    cmds.confirmDialog(title='Warning', message=name + ' Possibly because an attribute of that name already exists.', button=['Yes'], defaultButton='Yes')


def duplicateMesh(nodeMesh, nameMesh):
    reNameMesh = nameMesh.replace('|', '_')
    copyToWorkOn = cmds.duplicate(nodeMesh, rr=True, name=reNameMesh)
    cmds.select(cl=1)
    unLock = [ cmds.setAttr(reNameMesh + '.' + x, keyable=True, lock=False, channelBox=False) for x in ['tx',
     'ty',
     'tz',
     'rx',
     'ry',
     'rz',
     'sx',
     'sy',
     'sz',
     'v'] ]
    cmds.setAttr(reNameMesh + '.v', 1)
    return reNameMesh


def editField(Field):
    cmds.textField(Field, tx=targetBlendShapeText(), edit=True)

def creativeTarget(blendShape, target = [], prefix = None):
    listConnect = []
    listConnect_target = []
    listLock_target = []
    listValue_target = []
    listConnect_Name = []
    MeshOrigList = []
    listTargetBlendShape = cmds.listAttr(blendShape + '.weight', multi=True)
    if cmds.objExists(blendShape + '_Grp') != 1:
        blendShapeGrp = cmds.createNode('transform', name=blendShape + '_Grp')
    for i in listTargetBlendShape:
        if cmds.getAttr(blendShape + '.' + i, l=1) == True:
            cmds.setAttr(blendShape + '.' + i, l=0)
            listLock_target.append(i)
        get = cmds.getAttr(blendShape + '.' + i)
        listValue_target.append(get)
        targetConnect = cmds.listConnections(blendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, blendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        cmds.setAttr(blendShape + '.' + i, 0)

    MeshOrigList = meshOrig(blendShape)
    for x in target:
        if listTargetBlendShape.__contains__(x) != 1 or 'weight[' in x:
            continue
        tragetIndexItem = InputTargetGroup(blendShape, x)
        inputTargetItem = cmds.getAttr(blendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        for c in inputTargetItem:
            indexInt = (int(c) - 5000) / 1000.0
            Mesh = cmds.createNode('mesh', name=x + '_Shape')
            MeshMianShape = cmds.createNode('mesh', name=x + '_MianShape')
            cmds.sets(Mesh, edit=True, forceElement='initialShadingGroup')
            listRel = cmds.listRelatives(Mesh, p=True)
            MianlistRel = cmds.listRelatives(MeshMianShape, p=True)
            cmds.setAttr(blendShape + '.' + x, float(indexInt))
            cmds.connectAttr(blendShape + '.outputGeometry[0]', MeshMianShape + '' + '.inMesh')
            cmds.connectAttr(MeshOrigList[0] + '.outMesh', Mesh + '' + '.inMesh')
            copyMesh = cmds.duplicate(MianlistRel)
            count = str(indexInt).split('.')
            if count[0] == '-0':
                ne = 'm'
            else:
                ne = 'p'
            if float(indexInt) == 1:
                targetName = x
            else:
                targetName = x + '_' + ne + count[1]
            cmds.parent(copyMesh, blendShape + '_Grp')
            if prefix == 1:
                targetName = '_' + targetName
            ToName = cmds.rename(copyMesh, targetName)
            cmds.addAttr(ToName, longName=x, at='double')
            cmds.setAttr(ToName + '.' + x, float(indexInt))
            cmds.setAttr(blendShape + '.' + x, 0)
            cmds.delete(listRel, MianlistRel)
            listConnect_Name.append(ToName)

    for i in range(len(listTargetBlendShape)):
        val = listValue_target[i]
        cmds.setAttr(blendShape + '.' + listTargetBlendShape[i], val)

    for i in listLock_target:
        cmds.setAttr(blendShape + '.' + i, l=1)

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], blendShape + '.' + listConnect_target[i])

    return listConnect_Name


def blendShapeManage_UI():
    blendShapeManage()
    if blendShapeNode_ONOFF():
        freshTargetBlendShape('append')
    else:
        print('Please Loading Mesh.')