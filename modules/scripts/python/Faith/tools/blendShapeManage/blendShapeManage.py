# Embedded file name: E:/JunCmds/tool/blendShapeManage\blendShapeManage.py
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import of3d_rig.publicClass.OF3D_zchPipePublicClass as PublicClass
import sys, math, os, re
import webbrowser
import sphereDriver


__myBlog__ = 'www.wangqiguang.me'
__version__ = 'version 1.3.7  date:20140515'

def open_myBlog():
    myBlog = __myBlog__
    webbrowser.open_new_tab(myBlog)


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
        listMesh = cmds.listRelatives(mesh, f=1)
        if cmds.nodeType(listMesh[0]) == 'mesh':
            return True
        return False
    except TypeError:
        pass


def blendShapeNode_ONOFF():
    if cmds.textFieldGrp('meshShapeText', ex=1) == 1:
        obj = cmds.textFieldGrp('meshShapeText', query=True, text=True)
        if meshExists(obj):
            BaseHistory = cmds.listHistory(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            Nua = 0
            for i in BaseHistory:
                if cmds.nodeType(i) == 'blendShape':
                    Nua = 1

            return Nua


def blendShapeNode(MeshNode):
    BlendShapeNode = []
    try:
        BaseHistory = cmds.listHistory(MeshNode)
        for i in BaseHistory:
            if cmds.nodeType(i) != 'blendShape':
                pass
            else:
                BlendShapeNode.append(i)

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
    cmds.frameLayout(w=435, label='Correct Space Driver', collapsable=True, labelAlign='top', borderStyle='etchedIn', marginHeight=2, marginWidth=2, collapse=1)
    sphereDriver.SphereDriver().sphereDriver_UI()
    cmds.setParent('..')
    cmds.setParent('..')


def Clone_UI():
    cmds.columnLayout('', adj=True)
    TargetGoemerty = cmds.textFieldButtonGrp('TargetGoemerty', label='Target Goemerty:', tx=getMesh(), cw3=(100, 280, 100), bl='Reload', bc='', ed=False, eb=False)
    SourceGoemerty = cmds.textFieldButtonGrp('SourceGoemerty', label='Source Goemerty:', cw3=(100, 280, 100), bl='Reload')
    cmds.textFieldButtonGrp('SourceGoemerty', e=True, bc='loadText("SourceGoemerty")')
    cmds.button(label='Apply', c='creativeTargetClone()')
    cmds.button('cloneButton', l='Clone Target List', c='Edit_CloneButton()')
    cmds.frameLayout('cloneFrame', label='Clone List', mw=5, mh=5, la='center', cll=1, cl=1)
    cmds.scrollLayout('cloneList', horizontalScrollBarThickness=16, verticalScrollBarThickness=16, h=285)
    cmds.setParent('cloneList')
    cmds.setParent('..')
    cmds.setParent('..')


def creativeTargetClone():
    TargetGoemerty = cmds.textFieldButtonGrp('TargetGoemerty', query=True, tx=True)
    SourceGoemerty = cmds.textFieldButtonGrp('SourceGoemerty', query=True, tx=True)
    creativeTarget_Clone(TargetGoemerty, SourceGoemerty)


def loadText(FieldButtonGrp):
    selObj = cmds.ls(sl=1)
    if len(selObj) > 0:
        cmds.textFieldButtonGrp(FieldButtonGrp, edit=True, text=selObj[0])


def Edit_UI():
    cmds.columnLayout(adj=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 300), (2, 23), (3, 100)])
    cmds.text('availableText', l='Available blendShape target: ', font='boldLabelFont')
    cmds.text(l='')
    cmds.text('InbetweenText', l='Inbetween weight:')
    cmds.columnLayout()
    cmds.popupMenu(mm=True)
    cmds.menuItem(l='Append', rp='N', c='CreativeBlendShape().AppendTarget()')
    cmds.menuItem(l='Delete', rp='S', c='CreativeBlendShape().RemoveTarget()')
    cmds.menuItem(l='Gain', rp='W', c='CreativeBlendShape().GainTarget()')
    cmds.menuItem(l='Rename', rp='E', c='CreativeBlendShape().RenameTarget()')
    cmds.textScrollList('targetBlendShapeText', height=200, width=295, sc='inbetweenWieght(),getBlendShapeIndex()')
    cmds.setParent('..')
    cmds.text(l=' => ')
    cmds.columnLayout(adj=1)
    text2 = cmds.textScrollList('targetInbetweenText', allowMultiSelection=True, height=155, width=95, sc='setBlendShape()')
    cmds.floatField('InbetweenField', w=100, en=False)
    cmds.button(l=' inputGeomTarget ', c='CreativeBlendShape().inputGeomTarget()')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.text(l='', h=5)
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 215), (2, 215)])
    b2 = cmds.button('EditFinsihButton', label='Edit', c='EditFinishButton()')
    cmds.button(label='Cancel')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.columnLayout()
    cmds.frameLayout(w=435, label='In-between', collapsable=True, labelAlign='top', borderStyle='etchedIn', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout(adj=1)
    cmds.checkBoxGrp('Inbetween', label='Add in-between target:', columnWidth=(1, 160), of1='inbetweenBox()', on1='inbetweenBox()')
    cmds.floatSliderGrp('InbetweenSlider', label='In-between weight:', field=True, min=-10.0, max=10.0, pre=2, enable=False, adj=3, en=0, cw3=(140, 80, 200))
    cmds.button('EditAddbetweenButton', label='inbetweenEdit', c='inbetweenEditAddButton()', width=50, enable=False)
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='MirrorShape', collapsable=True, labelAlign='top', borderStyle='etchedIn', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    rb1 = cmds.radioButtonGrp('MirrorAxis', numberOfRadioButtons=3, l='Mirror Axis : ', labelArray3=('X', 'Y', 'Z'), sl=1, cw4=(85, 30, 30, 30), ct4=('left', 'left', 'left', 'left'))
    cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 300), (2, 120)])
    rb2 = cmds.radioButtonGrp('Position_of_MirrorsShapes', numberOfRadioButtons=2, l='Position of mirrors Shapes : ', labelArray2=('Shape', 'Original'), sl=2, cw3=(140, 80, 80), ct3=('left', 'left', 'left'))
    cmds.checkBox('DeleteMirrorObjBox', l='Delete Mirror Object', v=1)
    cmds.setParent('..')
    shapeOffset = cmds.floatFieldGrp('DuplicationOffset', label='==> Duplication Offset (shape mode) : ', numberOfFields=3, cw4=(200, 60, 60, 60), en=0)
    cmds.radioButtonGrp(rb2, e=1, cc="putOffsetInGray('" + shapeOffset + "','" + rb2 + "')")
    cmds.textFieldButtonGrp('Target_Text', label='Target : ', cw3=(150, 150, 120), bl=' <<< ', en=0)
    cmds.textFieldButtonGrp('MirrorTargetText', label='Shape(s) to Copy : ', cw3=(150, 150, 120), bl=' Mirror ', bc='CreativeBlendShape().MirrorBlendShape(0)')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='Mirror>Target', collapsable=True, labelAlign='top', borderStyle='etchedIn', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 160), (2, 100), (3, 160)])
    cmds.textField('targetField', tx='Target', en=0)
    cmds.text(l='    ==>>==    ')
    cmds.textField('sourceField', tx='Source', en=0)
    cmds.button(l='Target', c='editField("targetField")')
    cmds.text(l='')
    cmds.button(l='Source', c='editField("sourceField")')
    cmds.setParent('..')
    cmds.button(l='Apply', w=435, c='CreativeBlendShape().MirrorBlendShape(1)')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.frameLayout(w=435, label='BlendTwoAttr', collapsable=True, labelAlign='top', borderStyle='etchedIn', marginHeight=2, marginWidth=2, collapse=True)
    cmds.columnLayout()
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 120), (2, 120), (3, 160)])
    cmds.textField('target_1Field', tx='Target1', en=0)
    cmds.textField('target_2Field', tx='Target2', en=0)
    cmds.text(l='')
    cmds.button(l='Target1', c='editField("target_1Field")')
    cmds.button(l='Target2', c='editField("target_2Field")')
    cmds.setParent('..')
    cmds.button(l='create', w=420, c='CreativeBlendShape().blendTwoAttrCreate()')
    cmds.button(l='finish', w=420, c='CreativeBlendShape().blendTwoAttrConnect()')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')


def blendShapeManage():
    version = __version__
    if cmds.window('blendShapeManage', exists=True):
        cmds.deleteUI('blendShapeManage')
    cmds.window('blendShapeManage', mb=True, t='BlendShapeManage_' + version)
    cmds.menu(l='Edit')
    cmds.menuItem(l='Append', c='CreativeBlendShape().AppendTarget()')
    cmds.menuItem(l='Delete', c='CreativeBlendShape().RemoveTarget()')
    cmds.menuItem(l='Gain', c='CreativeBlendShape().GainTarget()')
    cmds.menuItem(l='Rename', c='CreativeBlendShape().RenameTarget()')
    cmds.menuItem(l='RevertTarget', c='CreativeBlendShape().GainTarget_All_for()')
    cmds.setParent('..')
    cmds.menu(l='Help')
    cmds.menuItem(label='Wang Blog', c='open_myBlog()')
    cmds.menuItem(d=True)
    cmds.menuItem(label='Close', c="cmds.window('blendShapeManage',e=True,vis=0)")
    cmds.menuItem(label=version)
    cmds.columnLayout('')
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 380)])
    cmds.button('buttonBlendShapeMesh', label='Reload Sel', c='reloadMesh()')
    cmds.textFieldGrp('meshShapeText', text=getMesh(), ed=False, cw1=375)
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
    Create_UI()
    cmds.setParent('..')
    cmds.columnLayout('child2')
    Edit_UI()
    cmds.setParent('..')
    cmds.columnLayout('child3')
    Clone_UI()
    cmds.setParent('..')
    cmds.tabLayout(tabs, sc='freshTargetBlendShape("append")', edit=True, tabLabel=(('child1', 'Create'), ('child2', 'Edit'), ('child3', 'Clone')))
    cmds.setParent('..')
    cmds.showWindow('blendShapeManage')
    cmds.window('blendShapeManage', edit=True, w=450, h=600)


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


def Clone_list_on():
    if blendShapeNode_ONOFF() == True:
        targetBlendShape = cmds.listAttr(blendShapeTextField() + '.weight', multi=True)
        targetInt = cmds.blendShape(blendShapeTextField(), query=True, wc=True)
        if targetInt > 0:
            for t in targetBlendShape:
                cmds.checkBox('Clone_%s' % t, l=t, p='cloneList', ann='%s' % t)

    cmds.frameLayout('cloneFrame', e=1, cl=0)


def Clone_list_off():
    cloneList = cmds.scrollLayout('cloneList', q=1, ca=1)
    if cloneList != None:
        for b in cloneList:
            fpn = cmds.checkBox(b, q=1, fpn=1)
            cmds.deleteUI(fpn)

    cmds.frameLayout('cloneFrame', e=1, cl=1)
    return


def Edit_CloneButton():
    if blendShapeNode_ONOFF() == True:
        buttonLebal = cmds.button('cloneButton', query=True, label=True)
        if buttonLebal == 'Clone Target List':
            cmds.button('cloneButton', edit=True, label='Cancel')
            Clone_list_on()
        if buttonLebal == 'Cancel':
            cmds.button('cloneButton', edit=True, label='Clone Target List')
            Clone_list_off()
    elif blendShapeNode_ONOFF() == 0:
        Dialog = 'The Goemerty has no BlendShape node.'
        cmds.confirmDialog(title='Confirm', message=Dialog, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')


def freshTargetBlendShape(temp, fresh = None):
    blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
    indexIntS = []
    targetName = targetBlendShapeText()
    if temp == 'append':
        if blendShapeNode_ONOFF() == True:
            targetBlendShape = cmds.listAttr(blendShapeTextField() + '.weight', multi=True)
            cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=True)
            targetInt = cmds.blendShape(blendShapeTextField(), query=True, wc=True)
            if targetInt > 0:
                for t in targetBlendShape:
                    cmds.textScrollList('targetBlendShapeText', edit=True, append=t)

            targetItems = cmds.textScrollList('targetBlendShapeText', query=True, ni=True)
            cmds.text('availableText', edit=True, l='Available blendShape target:' + str(targetItems))
            if cmds.tabLayout('tabs', q=1, sti=1) == 3:
                if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
                    Clone_list_off()
                    Clone_list_on()
        else:
            print('No Available BlendShape ')
            cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=1)
    if temp == 'remove':
        cmds.textScrollList('targetBlendShapeText', edit=True, ri=targetName)
        targetItems = cmds.textScrollList('targetBlendShapeText', query=True, ni=True)
        cmds.text('availableText', edit=True, l='Available blendShape target:' + str(targetItems))
    if fresh != None:
        targetItems = cmds.textScrollList('targetBlendShapeText', si=fresh, e=1)
    return


def targetBlendShapeText():
    targetBlendShape_Text = cmds.textScrollList('targetBlendShapeText', query=True, selectItem=True)
    if targetBlendShape_Text == None:
        targetBlendShape = 'None'
    else:
        targetBlendShape = targetBlendShape_Text[0].split('[')
        return targetBlendShape[0]
    return


def getBlendShapeIndex():
    tragetBlendShapeList = cmds.textScrollList('targetBlendShapeText', q=True, sii=True)
    cmds.floatField('InbetweenField', e=True, v=tragetBlendShapeList[0])


def setBlendShape():
    blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
    In = cmds.textScrollList('targetInbetweenText', query=True, si=True)
    tragetBlendShapeSel = targetBlendShapeText()


def inbetweenEditAddButton():
    buttonLebal = cmds.button('EditAddbetweenButton', query=True, label=True)
    if buttonLebal == 'inbetweenEdit':
        cmds.button('EditAddbetweenButton', edit=True, label='inbetweenAdd')
        CreativeBlendShape().EditBlendShape()
        cmds.floatSliderGrp('InbetweenSlider', edit=True, v=cmds.getAttr(blendShapeTextField() + '.' + targetBlendShapeText()))
    if buttonLebal == 'inbetweenAdd':
        cmds.button('EditAddbetweenButton', edit=True, label='inbetweenEdit')
        CreativeBlendShape().AddInbetweenBlendShape()


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


def CreateFinishtextFieldButton():
    buttonLabel = cmds.textFieldButtonGrp('newNameText', query=True, bl=True)
    meshLabel = cmds.textFieldGrp('meshShapeText', text=1, q=1)
    if buttonLabel == 'Finish':
        cmds.textFieldButtonGrp('newNameText', edit=True, bl='Create', ed=True)
        CreativeBlendShape().FinishBlendShape()
        cmds.textFieldButtonGrp('newNameText', edit=True, tx='')
        cmds.text('blendShapeText', e=1, label=blendShapeTextField())
    if buttonLabel == 'Create':
        if meshExists(meshLabel):
            CreativeBlendShape().CreateBlendShape()


def EditFinishButton():
    buttonLebal = cmds.button('EditFinsihButton', query=True, label=True)
    if buttonLebal == 'Edit':
        cmds.button('EditFinsihButton', edit=True, label='Finsih')
        cmds.textScrollList('targetBlendShapeText', edit=True, enable=False)
        cmds.textScrollList('targetInbetweenText', edit=True, enable=False)
        CreativeBlendShape().EditBlendShape()
    if buttonLebal == 'Finsih':
        cmds.button('EditFinsihButton', edit=True, label='Edit')
        cmds.textScrollList('targetBlendShapeText', edit=True, enable=True)
        cmds.textScrollList('targetInbetweenText', edit=True, enable=True)
        CreativeBlendShape().EditDoneBlendShape()


def reloadMesh():
    sel = getMesh()
    if len(sel) > 0 and meshExists(sel):
        meshShapeText = cmds.textFieldGrp('meshShapeText', text=sel, e=1)
        freshTargetBlendShape('append')
        cmds.text('blendShapeText', e=1, label=blendShapeTextField())
        cmds.textFieldButtonGrp('TargetGoemerty', e=1, tx=cmds.textFieldGrp('meshShapeText', text=1, q=1))
    else:
        meshShapeText = cmds.textFieldGrp('meshShapeText', text='No deformable objects selected.', e=1)
        cmds.text('blendShapeText', e=1, label='')


def object_vis(objVisible, obj, vis):
    if cmds.attributeQuery('visible_obj', n=objVisible, ex=1) == False:
        cmds.addAttr(objVisible, ln='visible_obj', at='bool')
        cmds.setAttr('%s.visible_obj' % objVisible, e=1, keyable=1)
    hasInput_v = cmds.listConnections('%s.v' % obj, s=True, d=False, scn=True)
    hasInput_ov = cmds.listConnections('%s.overrideVisibility' % obj, s=True, d=False, scn=True)
    if hasInput_v == None:
        if cmds.getAttr('%s.v' % obj, l=1):
            cmds.setAttr('%s.v' % obj, l=0)
        cmds.connectAttr('%s.visible_obj' % objVisible, '%s.v' % obj)
    elif hasInput_ov == None:
        try:
            cmds.setAttr('%s.lodVisibility' % obj, 1)
        except TypeError:
            pass

    if vis == 1:
        cmds.setAttr('%s.visible_obj' % objVisible, 1)
    if vis == 0:
        cmds.setAttr('%s.visible_obj' % objVisible, 0)
    return


def putOffsetInGray(shapeOffset, rb2):
    if cmds.radioButtonGrp(rb2, q=1, sl=1) == 1:
        cmds.floatFieldGrp(shapeOffset, e=1, en=1)
    if cmds.radioButtonGrp(rb2, q=1, sl=1) == 2:
        cmds.floatFieldGrp(shapeOffset, e=1, en=0)


class CreativeBlendShape():

    def __init__(self):
        self.blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
        self.blendShapeMesh_line = cmds.textFieldGrp('meshShapeText', query=True, text=True).replace('|', '_')
        self.newNameBlendShape = cmds.textFieldButtonGrp('newNameText', query=True, text=True)
        self.tragetBlendShape = targetBlendShapeText()
        self.BlendShape = blendShapeNode(self.blendShapeMesh)
        self.ConnectBox = cmds.checkBox('ConnectBox', query=True, value=True)
        self.CreateBox = cmds.checkBox('CreateBox', query=True, value=True)
        self.HideBox = cmds.checkBox('HideBox', query=True, value=True)
        self.PoseBox = cmds.checkBox('DeletePoseBox', query=True, value=True)
        self.DeleteBox = cmds.checkBox('DeleteBox', query=True, value=True)
        self.DeleteMirrorObjBox = cmds.checkBox('DeleteMirrorObjBox', q=1, v=1)
        self.targetInbetween = cmds.textScrollList('targetInbetweenText', query=True, si=True)
        self.InbetweenSlider = cmds.floatSliderGrp('InbetweenSlider', query=True, value=True)
        self.InbetweenField = cmds.floatField('InbetweenField', query=True, value=True)
        self.MirrorTargetText = cmds.textFieldButtonGrp('MirrorTargetText', tx=True, query=True)
        self.sourceField = cmds.textField('sourceField', tx=1, q=1)
        self.targetField = cmds.textField('targetField', tx=1, q=1)

    def indexTarget(self):
        tragetBlendShapeIndex = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        Index = tragetBlendShapeIndex.index(self.tragetBlendShape)
        return Index

    def count(self):
        count = cmds.getAttr(self.BlendShape[0] + '.inputTarget[0].inputTargetGroup', mi=True)[-1] + 1
        return count

    def tragetIndexItem(self):
        GetWeightIndex = 'gg_GetWeightIndex ' + str(self.BlendShape[0]) + ' ' + str(self.tragetBlendShape) + ' '
        tragetIndexItem = mel.eval(GetWeightIndex)
        return tragetIndexItem

    def tragetIndexItem_TXET(self):
        tragetIndex = int(self.indexTarget())
        indexItem = []
        inputTargetItem = cmds.getAttr(self.BlendShape[0] + '.inputTarget[0].inputTargetGroup', mi=True)
        for i in inputTargetItem:
            inputNone = cmds.getAttr(self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % i, mi=True)
            if inputNone != None:
                indexItem.append(i)

        tragetIndexItem = indexItem[tragetIndex]
        return tragetIndexItem

    def GainTarget(self):
        self.GainTarget_All(self.tragetBlendShape)

    def GainTarget_All(self, tragetBlendShape):
        count = self.count()
        tragetIndexItem = InputTargetGroup(self.BlendShape[0], tragetBlendShape)
        sel = creativeTarget(self.BlendShape[0], [tragetBlendShape])
        for i in sel:
            get = cmds.getAttr(i + '.' + tragetBlendShape) * 1000.0 + 5000
            shape = cmds.listHistory(i)
            cmds.connectAttr(shape[0] + '.worldMesh[0]', self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (tragetIndexItem, get), f=True)

        cmds.select(self.BlendShape[0])

    def GainTarget_All_for(self):
        tragetBlendShapeIndex = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        amount = 0
        multiple = len(tragetBlendShapeIndex) / 100.0
        x = 0
        if multiple == 0:
            multiple = 1
        cmds.progressWindow(title='RevertTarget...', progress=amount, status='Completed: 0%', isInterruptable=False)
        for i in tragetBlendShapeIndex:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            x += 1
            self.GainTarget_All(i)
            print(x)
            amount = x / multiple
            cmds.progressWindow(edit=True, progress=amount, status='Complete: ' + str(amount) + '%')
            cmds.pause(seconds=1)

        cmds.progressWindow(endProgress=1)

    def blendTwoAttrCreate(self):
        blendTwoAttrBase = 'blendTwoAttrBase'
        target_1 = cmds.textField('target_1Field', tx=1, q=True)
        target_2 = cmds.textField('target_2Field', tx=1, q=True)
        target_TwoAttr = creativeTarget(self.BlendShape[0], [target_1, target_2])
        baseMesh = cmds.createNode('mesh', name=blendTwoAttrBase + 'Shape')
        cmds.sets(baseMesh, edit=True, forceElement='initialShadingGroup')
        listMeshShape_Orig = cmds.listRelatives(self.blendShapeMesh, c=True)
        cmds.connectAttr(listMeshShape_Orig[1] + '.outMesh', baseMesh + '.inMesh')
        listTwoAttrBase = cmds.listRelatives(baseMesh, p=True, f=1)
        copyMesh = cmds.duplicate(baseMesh)
        cmds.delete(listTwoAttrBase)
        blendShapeTwoAttr = cmds.blendShape(self.BlendShape[0] + '_Grp|' + target_1, self.BlendShape[0] + '_Grp|' + target_2, copyMesh[0], n='blendTwoAttr')
        cmds.setAttr(blendShapeTwoAttr[0] + '.' + target_1, 1)
        cmds.setAttr(blendShapeTwoAttr[0] + '.' + target_2, 1)
        copyToWork = duplicateMesh(copyMesh, 'blendTwoAttr_copyToWork')
        cmds.delete(self.BlendShape[0] + '_Grp|' + target_1, self.BlendShape[0] + '_Grp|' + target_2)
        cmds.rename(copyMesh[0], blendTwoAttrBase)
        cmds.setAttr(blendTwoAttrBase + '.lodVisibility', 0)
        cmds.setAttr(self.blendShapeMesh + '.lodVisibility', 0)

    def blendTwoAttrConnect(self):
        target_1 = cmds.textField('target_1Field', tx=1, q=True)
        target_2 = cmds.textField('target_2Field', tx=1, q=True)
        multiplyTwo = cmds.createNode('multiplyDivide', n='multiplyTwo_' + target_1 + target_2)
        cmds.blendShape('blendTwoAttr', edit=True, tc=False, target=('blendTwoAttrBase', 2, 'blendTwoAttr_copyToWork', 1.0))
        cmds.setAttr('blendTwoAttr.' + target_1, -1)
        cmds.setAttr('blendTwoAttr.' + target_2, -1)
        cmds.setAttr('blendTwoAttr.' + 'blendTwoAttr_copyToWork', 1)
        targetTwo = duplicateMesh('blendTwoAttrBase', target_1 + target_2 + '_Two')
        cmds.connectAttr(self.BlendShape[0] + '.' + target_1, multiplyTwo + '.input1X')
        cmds.connectAttr(self.BlendShape[0] + '.' + target_2, multiplyTwo + '.input2X')
        count = self.count()
        cmds.blendShape(self.BlendShape[0], edit=True, tc=False, target=(self.blendShapeMesh,
         int(count),
         target_1 + target_2 + '_Two',
         1.0))
        cmds.connectAttr(multiplyTwo + '.outputX', self.BlendShape[0] + '.' + target_1 + target_2 + '_Two')
        cmds.delete('blendTwoAttrBase', 'blendTwoAttr_copyToWork', target_1 + target_2 + '_Two')

    def MirrorBlendShape(self, type):
        xyz = cmds.radioButtonGrp('MirrorAxis', q=1, sl=1)
        shapePosition = cmds.radioButtonGrp('Position_of_MirrorsShapes', q=1, sl=1)
        shapeOffset = cmds.floatFieldGrp('DuplicationOffset', q=1, value=1)
        tragetBlendShapeWeight = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        if cmds.objExists(self.sourceField):
            standerd = len(cmds.ls('*%s*' % self.sourceField))
            nMirror = self.sourceField + '_' + str(standerd)
        else:
            nMirror = self.sourceField
        nameMirror = nMirror
        if type == 0:
            nameMirror = self.MirrorTargetText
        if type == 1:
            nameMirror = self.sourceField
        if type == 0:
            if tragetBlendShapeWeight.__contains__(nameMirror):
                blendShapeExists(nameMirror)
                return
        GetWeightIndex = 'gg_GetWeightIndex ' + str(self.BlendShape[0]) + ' ' + str(self.sourceField) + ' '
        tragetIndexItem = mel.eval(GetWeightIndex)
        shapeToMirror = cmds.textFieldButtonGrp('Target_Text', tx=1, q=True)
        baseMesh = cmds.createNode('mesh', name='baseIn_' + self.blendShapeMesh)
        cmds.sets(baseMesh, edit=True, forceElement='initialShadingGroup')
        listMeshShape_Orig = meshOrig(self.blendShapeMesh)
        print(listMeshShape_Orig)
        cmds.connectAttr(listMeshShape_Orig[0] + '.outMesh', baseMesh + '.inMesh')
        base = cmds.listRelatives(baseMesh, p=True, f=1)[0]
        if type == 0:
            count = self.count()
        if type == 1:
            count = tragetIndexItem
        if type == 0:
            duplicateMesh(self.blendShapeMesh, nameMirror)
            cmds.blendShape(self.BlendShape[0], edit=True, target=(self.blendShapeMesh,
             int(count),
             nameMirror,
             1.0))
            cmds.delete(nameMirror)
        if type == 0:
            sel = creativeTarget(self.BlendShape[0], [shapeToMirror], prefix=1)
        if type == 1:
            sel = creativeTarget(self.BlendShape[0], [cmds.textField('targetField', tx=1, q=1)], prefix=1)
        if type == 0:
            traget_BlendShape = shapeToMirror
        if type == 1:
            traget_BlendShape = cmds.textField('targetField', tx=1, q=1)
        for i in range(len(sel)):
            targetN = str(sel[i]).replace(self.targetField, '')
            mirror = str(nameMirror) + targetN + '_mirror'
            if cmds.objExists(mirror):
                standerd = len(cmds.ls('*%s*' % mirror))
                mirror = str(nameMirror) + targetN + '_mirror_' + str(standerd)
            FGMirrorShapes(str(base), str(sel[i]), xyz, shapePosition, mirror, shapeOffset)
            get = cmds.getAttr(sel[i] + '.' + traget_BlendShape)
            if type == 1:
                dele = cmds.listConnections(self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (count, get * 1000.0 + 5000), p=1, s=1)
                if dele != None:
                    cmds.disconnectAttr(dele[0], self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (count, get * 1000.0 + 5000))
            cmds.blendShape(self.BlendShape[0], edit=True, ib=True, tc=False, target=(self.blendShapeMesh,
             count,
             mirror,
             get))
            cmds.delete(sel[i])
            if self.DeleteMirrorObjBox:
                cmds.delete(mirror)

        cmds.delete(base)
        freshTargetBlendShape('append')
        selectTargetBlendShapeText()
        return

    def AppendTarget(self):
        selectionObj = cmds.ls(sl=True)
        if blendShapeNode_ONOFF() == True:
            tragetBlendShapeIndex = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        for i in range(len(selectionObj)):
            if blendShapeNode_ONOFF() == True:
                count = self.count()
                if tragetBlendShapeIndex.__contains__(selectionObj[i]) or self.blendShapeMesh in selectionObj[i]:
                    print('Object will not allow alias ' + selectionObj[
                        i] + 'to be set.  Possibly because an attribute of that name already exists.')
                    continue
                else:
                    cmds.blendShape(self.BlendShape[0], edit=True, tc=False, target=(self.blendShapeMesh,
                     int(count + i),
                     selectionObj[i],
                     1.0))
            elif self.blendShapeMesh in selectionObj[i]:
                continue
            else:
                cmds.blendShape(selectionObj[i], self.blendShapeMesh, frontOfChain=True)

        freshTargetBlendShape('append')
        selectTargetBlendShapeText()

    def RemoveTarget(self):
        count = self.count()
        tragetIndexItem = self.tragetIndexItem()
        sel = creativeTarget(self.BlendShape[0], [self.tragetBlendShape])
        tragetBlendShapeIndex = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        for i in sel:
            get = cmds.getAttr(i + '.' + self.tragetBlendShape) * 1000.0 + 5000
            shape = cmds.listHistory(i)
            cmds.connectAttr(shape[0] + '.worldMesh[0]', self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (tragetIndexItem, get), f=True)
            cmds.blendShape(self.BlendShape[0], edit=True, rm=True, t=(self.blendShapeMesh,
             tragetIndexItem,
             i,
             1))
            cmds.delete(i)

        cmds.select(self.BlendShape[0])
        if cmds.blendShape(self.BlendShape[0], q=1, wc=True) == 0:
            cmds.delete(self.BlendShape[0])
        freshTargetBlendShape('remove')

    def RenameTarget(self):
        text = cueDialog(self.tragetBlendShape, 'Rename Object')
        if text != '':
            cmds.aliasAttr(text, self.BlendShape[0] + '.' + self.tragetBlendShape)
            freshTargetBlendShape('append')
            cmds.textScrollList('targetBlendShapeText', si=text, e=1)

    def CreateBlendShape(self):
        copyToWork = self.blendShapeMesh + '_copyToWork_' + self.newNameBlendShape
        if not self.newNameBlendShape:
            return 0
        if cmds.nodeType(blendShapeNode(self.blendShapeMesh)) == 'blendShape':
            if cmds.blendShape(self.BlendShape[0], q=1, wc=True) != 0:
                tragetBlendShapeIndex = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
                if tragetBlendShapeIndex.__contains__(self.newNameBlendShape):
                    blendShapeExists(self.newNameBlendShape)
                    return
        else:
            print('ok')
        blendShapeMesh_copyToWork = duplicateMesh(self.blendShapeMesh, copyToWork)
        SculptGeometryTool = 'SculptGeometryTool'
        mel.eval(SculptGeometryTool)
        if int(self.HideBox) == 1:
            object_vis(blendShapeMesh_copyToWork, self.blendShapeMesh, 0)
        else:
            object_vis(blendShapeMesh_copyToWork, self.blendShapeMesh, 1)
        cmds.select(blendShapeMesh_copyToWork)
        cmds.textFieldButtonGrp('newNameText', edit=True, bl='Finish', ed=False)

    def FinishBlendShape(self):
        blendShapeMesh_copyToWork = self.blendShapeMesh_line + '_copyToWork_' + self.newNameBlendShape
        object_vis(blendShapeMesh_copyToWork, self.blendShapeMesh, 1)
        CorrectiveShape(blendShapeMesh_copyToWork, self.blendShapeMesh, self.newNameBlendShape).CorrectiveShapeRoutine()
        if int(self.ConnectBox) == 1:
            if blendShapeNode_ONOFF() == True and int(self.CreateBox) == 1:
                count = self.count()
                cmds.blendShape(self.BlendShape[0], edit=True, tc=False, target=(self.blendShapeMesh,
                 int(count),
                 self.newNameBlendShape,
                 1.0))
            elif blendShapeNode_ONOFF() != True:
                cmds.blendShape(self.newNameBlendShape, self.blendShapeMesh, frontOfChain=True, exclusive='deformPartition#')
            cmds.setAttr(self.newNameBlendShape + '.v', 0)
        else:
            print('Creatr garget ' + self.newNameBlendShape)
            cmds.setAttr(self.newNameBlendShape + '.v', 1)
        if self.DeleteBox == 1:
            cmds.delete(self.newNameBlendShape)
        if self.PoseBox == 1:
            cmds.delete(blendShapeMesh_copyToWork)
        freshTargetBlendShape('append')
        cmds.select(self.blendShapeMesh)
        SelectTool = 'SelectTool'
        mel.eval(SelectTool)

    def EditBlendShape(self):
        targetBlendShape = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        InbetweenField = cmds.getAttr(self.BlendShape[0] + '.' + self.tragetBlendShape)
        if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
            set = float(InbetweenField)
        else:
            set = float(self.targetInbetween[0])
        if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
            BindPose = self.blendShapeMesh_line + '_inbetweenBindPose_' + self.tragetBlendShape
        else:
            BindPose = self.blendShapeMesh_line + '_inBindPose_' + self.tragetBlendShape
        duplicateBindPose = duplicateMesh(self.blendShapeMesh, BindPose)
        cmds.setAttr(self.BlendShape[0] + '.' + self.tragetBlendShape, set)
        vertex = cmds.polyEvaluate(self.blendShapeMesh, vertex=True)
        int(vertex)
        for v in range(vertex):
            ployPosition = cmds.pointPosition(self.blendShapeMesh + '.vtx[%d]' % v, w=True)
            cmds.move(ployPosition[0], ployPosition[1], ployPosition[2], duplicateBindPose + '.vtx[%d]' % v)

        SculptGeometryTool = 'SculptGeometryTool'
        mel.eval(SculptGeometryTool)
        object_vis(duplicateBindPose, self.blendShapeMesh, 0)
        cmds.select(duplicateBindPose)

    def EditDoneBlendShape(self):
        cmds.setAttr(self.BlendShape[0] + '.' + self.tragetBlendShape, 0)
        blendShapeMesh_inBindPose = self.blendShapeMesh_line + '_inBindPose_' + self.tragetBlendShape
        inBindPose = 'inBindPose_' + self.tragetBlendShape
        CorrectiveShape(blendShapeMesh_inBindPose, self.blendShapeMesh, inBindPose).CorrectiveShapeRoutine()
        Input = self.tragetIndexItem()
        indexWeight = float(self.targetInbetween[0]) * 1000.0 + 5000
        cmds.connectAttr(inBindPose + '.worldMesh[0]', self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (Input, indexWeight), f=True)
        cmds.textScrollList('targetBlendShapeText', edit=True, enable=True)
        object_vis(blendShapeMesh_inBindPose, self.blendShapeMesh, 1)
        cmds.delete(blendShapeMesh_inBindPose, inBindPose)
        cmds.select(self.blendShapeMesh)
        SelectTool = 'SelectTool'
        mel.eval(SelectTool)

    def AddInbetweenBlendShape(self):
        targetBlendShape = cmds.listAttr(self.BlendShape[0] + '.weight', multi=True)
        inbetweenBind_Target = self.blendShapeMesh_line + '_inbetweenBindPose_' + self.tragetBlendShape
        cmds.setAttr(self.BlendShape[0] + '.' + self.tragetBlendShape, 0)
        InputTarget = self.tragetIndexItem()
        inbetweenBindPose = 'inbetweenBindPose_' + self.tragetBlendShape
        CorrectiveShape(inbetweenBind_Target, self.blendShapeMesh, inbetweenBindPose).CorrectiveShapeRoutine()
        cmds.blendShape(self.BlendShape[0], edit=True, tc=False, ib=True, target=(self.blendShapeMesh,
         int(InputTarget),
         inbetweenBindPose,
         float(self.InbetweenSlider)))
        object_vis(inbetweenBind_Target, self.blendShapeMesh, 1)
        cmds.delete(inbetweenBind_Target, inbetweenBindPose)
        cmds.select(self.blendShapeMesh)
        SelectTool = 'SelectTool'
        mel.eval(SelectTool)

    def inputGeomTarget(self):
        GeomTarget = cmds.ls(sl=True)
        shape = cmds.listHistory(GeomTarget[0])
        Input = self.tragetIndexItem()
        indexWeight = float(self.targetInbetween[0]) * 1000.0 + 5000
        cmds.connectAttr(shape[0] + '.worldMesh[0]', self.BlendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d].inputGeomTarget' % (Input, indexWeight), f=True)
        print(GeomTarget)


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


class CorrectiveShape():

    def __init__(self, poesMesh, skinMesh, deformerMesh):
        self.poesMesh = poesMesh
        self.skinMesh = skinMesh
        self.deformerMesh = deformerMesh
        self.BlendShape = blendShapeNode(self.skinMesh)
        targetCount = targetBlendShapeText()

    def searchSkinCluster(self, selObj):
        try:
            result = cmds.ls(cmds.listHistory(selObj), type='skinCluster')[0]
        except:
            return False

        try:
            result = cmds.ls(cmds.listHistory(selObj), type='skinCluster')[0]
        except:
            return False

        return result

    def CorrectiveShapeRoutine(self):
        correctShapeInfo = cmds.pluginInfo('RosaCorrectShape.py', query=True, loaded=True)
        try:
            if not correctShapeInfo:
                cmds.loadPlugin('RosaCorrectShape.py')
        except RuntimeError:
            publicCls.mayaWarning('The RosaCorrectShape is not existed')

        cmds.select(cl=True)
        if self.searchSkinCluster(self.skinMesh):
            cmds.select(self.poesMesh, self.skinMesh, add=True)
            BSpirit = 'gg_BSpiritCorrectiveShape ' + str(self.deformerMesh) + ' '
            BSpirit_run = mel.eval(BSpirit)
        elif not self.searchSkinCluster(self.skinMesh):
            duplicateMesh(self.poesMesh, self.deformerMesh)
        cmds.select(cl=True)


def editField(Field):
    cmds.textField(Field, tx=targetBlendShapeText(), edit=True)


def inbetweenWieght():
    blendShapeMesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
    blendShape = blendShapeNode(blendShapeMesh)
    tragetBlendShapeIndex = targetBlendShapeText()
    tragetIndexItem = CreativeBlendShape().tragetIndexItem()
    print(tragetIndexItem)
    inputTargetItem = cmds.getAttr(blendShape[0] + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
    cmds.textScrollList('targetInbetweenText', edit=True, removeAll=True)
    if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
        cmds.floatSliderGrp('InbetweenSlider', edit=True, v=0)
    for i in inputTargetItem:
        indexInt = (int(i) - 5000) / 1000.0
        cmds.textScrollList('targetInbetweenText', edit=True, append=str(indexInt), sii=1)

    cmds.textFieldButtonGrp('Target_Text', tx=tragetBlendShapeIndex, edit=True)


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
            MeshMian = cmds.createNode('mesh', name=x + '_MianShape')
            cmds.sets(Mesh, edit=True, forceElement='initialShadingGroup')
            listRel = cmds.listRelatives(Mesh, p=True)
            MianlistRel = cmds.listRelatives(MeshMian, p=True)
            cmds.setAttr(blendShape + '.' + x, float(indexInt))
            cmds.connectAttr(blendShape + '.outputGeometry[0]', MeshMian + '' + '.inMesh')
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


def InputTargetGroup(blendShapeNode, target):
    GetWeightIndex = 'gg_GetWeightIndex ' + str(blendShapeNode) + ' ' + str(target) + ' '
    tragetIndexItem = mel.eval(GetWeightIndex)
    return tragetIndexItem


def creativeTarget_Clone(TargetGeo, SourceGeo):
    listConnect = []
    listConnect_target = []
    listConnect_get = []
    SourceOrigList = []
    appendCloneList = []
    cloneList = cmds.scrollLayout('cloneList', q=1, childArray=1)
    SourceBlendShape = blendShapeNode(TargetGeo)[0]
    if cmds.getAttr(SourceBlendShape + '.envelope') != 1:
        cmds.setAttr(SourceBlendShape + '.envelope', 1)
    it = len(cmds.ls(SourceGeo + '_BlendShape*', type='blendShape'))
    SourceGeo_name = SourceGeo + '_BlendShape' + str(it + 1)
    listTarget = cmds.listAttr(SourceBlendShape + '.weight', multi=True)
    listShpae = cmds.listHistory(SourceGeo)
    if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
        for b in cloneList:
            if cmds.checkBox(b, q=1, v=1) == 1:
                ann = cmds.checkBox(b, q=1, ann=1)
                appendCloneList.append(ann)

    if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
        listTargetBlendShape = appendCloneList
    else:
        listTargetBlendShape = listTarget
    if len(listTargetBlendShape) > 0:
        pass
    else:
        print('Select at least one please.')
        sys.exit()
    blendShapeGrp = SourceGeo_name + '_grp'
    if cmds.objExists(blendShapeGrp) != 1:
        cmds.createNode('transform', name=blendShapeGrp)
    for i in listTargetBlendShape:
        targetConnect = cmds.listConnections(SourceBlendShape + '.' + i, p=True, s=True, d=False)
        if targetConnect != None:
            for m in targetConnect:
                cmds.disconnectAttr(m, SourceBlendShape + '.' + i)

            listConnect.append(m)
            listConnect_target.append(i)
        else:
            get = i + '>' + str(cmds.getAttr(SourceBlendShape + '.' + i))
            listConnect_get.append(get)
        cmds.setAttr(SourceBlendShape + '.' + i, 0)

    cmds.blendShape(SourceGeo, exclusive='deformPartition#', frontOfChain=True, name=SourceGeo_name)
    cmds.select(SourceGeo)
    cmds.select(TargetGeo, add=True)
    CreateWrap = 'doWrapArgList "6" { "1","0","1", "2", "1", "1", "0" };'
    mel.eval(CreateWrap)
    SourceOrigList = meshOrig(SourceGeo)
    amount = 0
    multiple = len(listTargetBlendShape) / 100.0
    xi = 0
    if multiple == 0:
        multiple = 1
    cmds.progressWindow(title='Clone...', progress=amount, status='Completed: 0%', isInterruptable=False)
    for x in listTargetBlendShape:
        if cmds.progressWindow(query=True, isCancelled=True):
            break
        if listTargetBlendShape.__contains__(x) != 1 or 'weight[' in x:
            continue
        xi += 1
        tragetIndexItem = InputTargetGroup(SourceBlendShape, x)
        inputTargetItem = cmds.getAttr(SourceBlendShape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % tragetIndexItem, mi=True)
        for c in inputTargetItem:
            indexInt = (int(c) - 5000) / 1000.0
            Mesh = cmds.createNode('mesh', name=x + '_Shape')
            MeshMian = cmds.createNode('mesh', name=x + '_MianShape')
            cmds.sets(Mesh, edit=True, forceElement='initialShadingGroup')
            listRel = cmds.listRelatives(Mesh, p=True)
            MianlistRel = cmds.listRelatives(MeshMian, p=True)
            cmds.setAttr(SourceBlendShape + '.' + x, indexInt)
            cmds.connectAttr(listShpae[0] + '.outMesh', MeshMian + '' + '.inMesh')
            cmds.connectAttr(SourceOrigList[0] + '.outMesh', Mesh + '' + '.inMesh')
            copyMesh = cmds.duplicate(Mesh)
            vertex = cmds.polyEvaluate(MeshMian, vertex=True)
            int(vertex)
            for v in range(vertex):
                ployPosition = cmds.pointPosition(MeshMian + '.vtx[%d]' % v, w=True)
                cmds.move(ployPosition[0], ployPosition[1], ployPosition[2], copyMesh[0] + '.vtx[%d]' % v)

            count = str(indexInt).split('.')
            if count[0] == '-0':
                ne = 'm'
            else:
                ne = 'p'
            if float(indexInt) == 1:
                targetName = x
            else:
                targetName = x + '_' + str(tragetIndexItem) + '_' + ne + count[1]
            cmds.parent(copyMesh, blendShapeGrp)
            ToName = cmds.rename(copyMesh, targetName)
            cmds.addAttr(ToName, longName=x, at='double')
            cmds.setAttr(ToName + '.' + x, float(indexInt))
            cmds.setAttr(SourceBlendShape + '.' + x, 0)
            cmds.delete(listRel, MianlistRel)
            if float(indexInt) == 1:
                cmds.blendShape(SourceGeo_name, edit=True, tc=False, target=(SourceGeo,
                 xi,
                 ToName,
                 1.0))
            else:
                cmds.blendShape(SourceGeo_name, edit=True, ib=True, tc=False, target=(SourceGeo,
                 xi,
                 ToName,
                 float(indexInt)))
            print(xi)

        amount = xi / multiple
        cmds.progressWindow(edit=True, progress=amount, status='Complete: ' + str(amount) + '%')
        cmds.pause(seconds=1)

    cmds.progressWindow(endProgress=1)
    SourceGeoHistory = cmds.listHistory(SourceGeo)
    for i in SourceGeoHistory:
        try:
            if cmds.nodeType(i) == 'wrap':
                cmds.delete(i)
        except RuntimeError:
            print('No wrap deformable .')

    for i in range(len(listConnect)):
        cmds.connectAttr(listConnect[i], SourceBlendShape + '.' + listConnect_target[i])
        cmds.connectAttr(listConnect[i], SourceGeo_name + '.' + listConnect_target[i])

    for i in listConnect_get:
        listConnect_wt = i.split('>')
        cmds.setAttr(SourceBlendShape + '.' + listConnect_wt[0], float(listConnect_wt[1]))
        cmds.setAttr(SourceGeo_name + '.' + listConnect_wt[0], float(listConnect_wt[1]))

    return


def setDriverKey(attr1, attr2, dv, v, driven):
    mdNode = cmds.createNode('multiplyDivide', name='ff_multiplyDrv')
    cmds.setDrivenKeyframe('%s.input1X' % mdNode, cd=attr1, dv=0, v=0)
    cmds.setDrivenKeyframe('%s.input1X' % mdNode, cd=attr1, dv=dv, v=v)
    cmds.setDrivenKeyframe('%s.input2X' % mdNode, cd=attr2, dv=0, v=0)
    cmds.setDrivenKeyframe('%s.input2X' % mdNode, cd=attr2, dv=dv, v=v)
    cmds.connectAttr('%s.outputX' % mdNode, '%s' % driven)


def correctSpace(sphereName, *attributes):
    driverN = '%s_driver_bridge' % sphereName
    locN = '%s_locator_help' % sphereName
    pointOnSurface = cmds.createNode('closestPointOnSurface', n='%s_pointOnSurface' % sphereName)
    multiplyScale = cmds.createNode('multiplyDivide', n='%s_multiplyScale' % sphereName)
    sphere = cmds.sphere(n=driverN, ch=1, o=1, po=0, ax=(0, 1, 0), esw=180, s=4, nsp=4)
    spaceLocater = cmds.spaceLocator(n=locN, p=(0, 0, 0))
    grp = cmds.createNode('transform', n='%s_shapeHelp_grp' % sphereName)
    sphereShape = cmds.listRelatives(sphere, s=1)[0]
    locaterShape = cmds.listRelatives(spaceLocater)[0]
    cmds.select(cl=1)
    cmds.parent(driverN, locN, grp)
    cmds.addAttr(driverN, at='double', ln='globalScale')
    cmds.setAttr('%s.globalScale' % driverN, keyable=1)
    cmds.setAttr('%s.globalScale' % driverN, 1)
    cmds.addAttr(sphereShape, at='double', ln='driver_bridge')
    cmds.connectAttr('%s.worldPosition[0]' % locaterShape, '%s.inPosition' % pointOnSurface)
    cmds.connectAttr('%s.worldSpace[0]' % sphereShape, '%s.inputSurface' % pointOnSurface)
    cmds.connectAttr('%s.globalScale' % driverN, '%s.sx' % driverN)
    cmds.connectAttr('%s.globalScale' % driverN, '%s.sy' % driverN)
    cmds.connectAttr('%s.globalScale' % driverN, '%s.sz' % driverN)
    cmds.setAttr('%s.sx' % driverN, cb=0, k=0, l=1)
    cmds.setAttr('%s.sy' % driverN, cb=0, k=0, l=1)
    cmds.setAttr('%s.sz' % driverN, cb=0, k=0, l=1)
    cmds.setAttr('%s.input1X' % multiplyScale, 1)
    cmds.setAttr('%s.input2X' % multiplyScale, 1.414214)
    cmds.setAttr('%s_locator_help.tz' % sphereName, 1)
    cmds.connectAttr('%s.globalScale' % driverN, '%s.input1X' % multiplyScale)
    for i in range(len(attributes)):
        attr = attributes[i]
        if attr in ('left', 'right', 'uper', 'down'):
            posN = '%s_%s_pointOnSurface' % (sphereName, attr)
            disN = '%s_%s_distance' % (sphereName, attr)
            remapN = '%s_%s_remapValue' % (sphereName, attr)
            distanceN = '%s_%s_distance' % (sphereName, attr)
            dis = cmds.createNode('distanceBetween', n=distanceN)
            point = cmds.createNode('pointOnSurfaceInfo', n=posN)
            remap = cmds.createNode('remapValue', n=remapN)
            parameterU = '%s.%s_parameterU' % (sphereShape, attr)
            parameterV = '%s.%s_parameterV' % (sphereShape, attr)
            cmds.addAttr(sphereShape, at='double', ln='%s_parameterU' % attr)
            cmds.addAttr(sphereShape, at='double', ln='%s_parameterV' % attr)
            cmds.setAttr(parameterU, keyable=1)
            cmds.setAttr(parameterV, keyable=1)
            cmds.connectAttr(parameterU, '%s.parameterU' % posN)
            cmds.connectAttr(parameterV, '%s.parameterV' % posN)
            cmds.connectAttr('%s.worldSpace[0]' % sphereShape, '%s.inputSurface' % point)
            cmds.connectAttr('%s.position' % point, '%s.point2' % dis)
            cmds.connectAttr('%s.position' % pointOnSurface, '%s.point1' % dis)
            cmds.connectAttr('%s.outputX' % multiplyScale, '%s.inputMax' % remap)
            cmds.connectAttr('%s.distance' % dis, '%s.inputValue' % remap)
            if attr == 'down':
                cmds.setAttr(parameterU, 0)
                cmds.setAttr(parameterV, 0)
            if attr == 'left':
                cmds.setAttr(parameterU, 2)
                cmds.setAttr(parameterV, 0)
            if attr == 'uper':
                cmds.setAttr(parameterU, 4)
                cmds.setAttr(parameterV, 0)
            if attr == 'right':
                cmds.setAttr(parameterU, 2)
                cmds.setAttr(parameterV, 4)
            cmds.addAttr(driverN, at='double', ln=str(attr))
            driven = '%s.%s' % (driverN, attr)
            if cmds.getAttr(driven, k=1) != 1:
                cmds.setAttr('%s.%s' % (driverN, attr), keyable=1)
                cmds.connectAttr('%s.outValue' % remapN, driven)
                cmds.setAttr('%s.value[0].value_Position' % remapN, 0)
                cmds.setAttr('%s.value[0].value_FloatValue' % remapN, 1)
                cmds.setAttr('%s.value[1].value_Position' % remapN, 1)
                cmds.setAttr('%s.value[1].value_FloatValue' % remapN, 0)
        if attr in ('uper_left', 'uper_right', 'down_right', 'down_left'):
            attrs = attr.split('_')
            attr1 = '%s.%s' % (driverN, attrs[0])
            attr2 = '%s.%s' % (driverN, attrs[1])
            cmds.addAttr(driverN, at='double', ln=str(attr))
            driven = '%s.%s' % (driverN, attr)
            cmds.setAttr('%s.%s' % (driverN, attr), keyable=1)
            remap = '%s_%s_remapValue' % (sphereName, attr)
            setDriverKey(attr1, attr2, 0.458804, 1, driven)


def invert(base = None, corrective = None, name = None):
    cmds.undoInfo(openChunk=True)
    if not base or not corrective:
        sel = cmds.ls(sl=True)
        if not sel or len(sel) != 2:
            cmds.undoInfo(closeChunk=True)
            raise RuntimeError('Select base then corrective')
        base, corrective = sel
    basePoints = getPoints(base)
    numPoints = basePoints.length()
    correctivePoints = getPoints(corrective)
    shapes = cmds.listRelatives(base, children=True, shapes=True)
    for s in shapes:
        if cmds.getAttr('%s.intermediateObject' % s) and cmds.listConnections('%s.worldMesh' % s, source=False):
            origMesh = s
            break
    else:
        cmds.undoInfo(closeChunk=True)
        raise RuntimeError('No intermediate shape found for %s.' % base)

    origPoints = getPoints(origMesh)
    xPoints = OpenMaya.MPointArray(origPoints)
    yPoints = OpenMaya.MPointArray(origPoints)
    zPoints = OpenMaya.MPointArray(origPoints)
    for i in range(numPoints):
        xPoints[i].x += 1.0
        yPoints[i].y += 1.0
        zPoints[i].z += 1.0

    setPoints(origMesh, xPoints)
    xPoints = getPoints(base)
    setPoints(origMesh, yPoints)
    yPoints = getPoints(base)
    setPoints(origMesh, zPoints)
    zPoints = getPoints(base)
    setPoints(origMesh, origPoints)
    if not name:
        name = '%s_inverted' % corrective
    invertedShape = cmds.duplicate(base, name=name)[0]
    shapes = cmds.listRelatives(invertedShape, children=True, shapes=True)
    for s in shapes:
        if cmds.getAttr('%s.intermediateObject' % s):
            cmds.delete(s)

    setPoints(invertedShape, origPoints)
    for attr in 'trs':
        for x in 'xyz':
            cmds.setAttr('%s.%s%s' % (invertedShape, attr, x), lock=False)

    cmds.setAttr('%s.visibility' % invertedShape, 1)
    deformer = cmds.deformer(invertedShape, type='RosaCorrectShape')[0]
    oDeformer = getMObject(deformer)
    fnDeformer = OpenMaya.MFnDependencyNode(oDeformer)
    plugMatrix = fnDeformer.findPlug('inversionMatrix', False)
    fnMatrixData = OpenMaya.MFnMatrixData()
    for i in range(numPoints):
        matrix = OpenMaya.MMatrix()
        setMatrixRow(matrix, xPoints[i] - basePoints[i], 0)
        setMatrixRow(matrix, yPoints[i] - basePoints[i], 1)
        setMatrixRow(matrix, zPoints[i] - basePoints[i], 2)
        matrix = matrix.inverse()
        oMatrix = fnMatrixData.create(matrix)
        plugMatrixElement = plugMatrix.elementByLogicalIndex(i)
        plugMatrixElement.setMObject(oMatrix)

    fnPointData = OpenMaya.MFnPointArrayData()
    oPointData = fnPointData.create(basePoints)
    plugDeformedPoints = fnDeformer.findPlug('deformedPoints', False)
    plugDeformedPoints.setMObject(oPointData)
    cmds.connectAttr('%s.outMesh' % getShape(corrective), '%s.correctiveMesh' % deformer)
    cmds.setAttr('%s.activate' % deformer, True)
    cmds.undoInfo(closeChunk=True)
    return invertedShape


def getShape(node):
    if cmds.nodeType(node) == 'transform':
        shapes = cmds.listRelatives(node, shapes=True)
        if not shapes:
            raise RuntimeError('%s has no shape' % node)
        return shapes[0]
    if cmds.nodeType(node) in ('mesh', 'nurbsCurve', 'nurbsSurface'):
        return node


def getMObject(node):
    selectionList = OpenMaya.MSelectionList()
    selectionList.add(node)
    oNode = OpenMaya.MObject()
    selectionList.getDependNode(0, oNode)
    return oNode


def getDagPath(node):
    selectionList = OpenMaya.MSelectionList()
    selectionList.add(node)
    pathNode = OpenMaya.MDagPath()
    selectionList.getDagPath(0, pathNode)
    return pathNode


def getPoints(path, space = OpenMaya.MSpace.kObject):
    if isinstance(path, str) or isinstance(path, unicode):
        path = getDagPath(getShape(path))
    itGeo = OpenMaya.MItGeometry(path)
    points = OpenMaya.MPointArray()
    itGeo.allPositions(points, space)
    return points


def setPoints(path, points, space = OpenMaya.MSpace.kObject):
    if isinstance(path, str) or isinstance(path, unicode):
        path = getDagPath(getShape(path))
    itGeo = OpenMaya.MItGeometry(path)
    itGeo.setAllPositions(points, space)


def setMatrixRow(matrix, newVector, row):
    setMatrixCell(matrix, newVector.x, row, 0)
    setMatrixCell(matrix, newVector.y, row, 1)
    setMatrixCell(matrix, newVector.z, row, 2)


def setMatrixCell(matrix, value, row, column):
    OpenMaya.MScriptUtil.setDoubleArray(matrix[row], column, value)


def blendShapeManage_UI():
    blendShapeManage()
    if blendShapeNode_ONOFF() == True:
        freshTargetBlendShape('append')
    else:
        print('Please Loading Mesh.')
