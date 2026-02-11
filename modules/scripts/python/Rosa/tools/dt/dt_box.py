# coding=utf-8
import pymel.core as pm

def gui():
    window_name = 'ToolBox_window'
    window_title = 'Rig_ToolBox1.0'

    try:
        pm.deleteUI(window_name)
    except:
        pass

    pm.window(window_name, title=window_title, rtf=1, menuBar=1, s=1)
    pm.columnLayout('ToolBoxCL', adj=1)
    pm.tabLayout('ToolBoxTL', p='ToolBoxCL')
    #  Box_one
    pm.columnLayout('Box_one', p='ToolBoxTL', adj=0)

    # GUI Creat Joint
    pm.frameLayout(p='Box_one', mw=10, mh=1, w=360, l="Create Joint", collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('CreateJointCL', adj=True)
    pm.rowLayout(p='CreateJointCL', nc=2, adj=2)
    pm.button(l='Center Create Joint', h=35,w=160, c='creat_jointone()', bgc=(0.2, 0.5, 0.6))
    pm.button(l='Point Create Joint', h=35, w=160,c='creat_jointtwo()', bgc=(0.2, 0.5, 0.6))
    pm.setParent('..')
    pm.separator(h=10)

    # GUI: Rename and number
    pm.frameLayout(p='Box_one', mw=10, mh=1, w=360, l="Rename", collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('RenameCL', adj=True)
    pm.rowLayout(p='RenameCL', nc=2, cw2=[50, 150], adj=2)
    pm.text(l='Rename:')
    pm.textField('renameTF')
    pm.setParent('..')
    pm.rowLayout(p='RenameCL', nc=4, cw4=[50, 135, 50, 150], adj=4)
    pm.text(l='Starting:')
    pm.textField('startingTF', tx='1')
    pm.text(l='Padding:')
    pm.textField('paddingTF', tx='2')
    pm.setParent('..')
    pm.button(l='Rename and Number', w=260, h=35, c='rename_number()', bgc=(0.2, 0.5, 0.6))
    pm.separator(h=15)

    # GUI: Add suffix
    pm.rowLayout(p='RenameCL', nc=4)
    pm.button(l='_jnt', w=82.5, h=35, c='suffix_jnt()', bgc=(0.3, 0.3, 0.5))
    pm.button(l='_ctrl', w=82.5, h=35, c='suffix_ctrl()', bgc=(0.8, 0.5, 0.2))
    pm.button(l='_old', w=82.5, h=35, c='suffix_old()', bgc=(0.5, 0.1, 0.3))
    pm.button(l='_new', w=82.5, h=35, c='suffix_new()', bgc=(0.8, 0.5, 0.2))
    pm.setParent('..')
    pm.separator(h=15)

    # GUI Creat FkContol
    pm.frameLayout(p='Box_one', mw=10, mh=1, w=360, l="FkContol", collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('FkContolCL', adj=True)
    pm.rowLayout(p='FkContolCL', nc=4, adj=4)
    pm.text(l='Contraint:', w=80)
    pm.checkBox('fkConTCB', l='Translate', w=80, v=1)
    pm.checkBox('fkConRCB', l='Rotate', w=80, v=1)
    pm.checkBox('fkConSCB', l='Scale', w=80, v=1)
    pm.setParent('..')
    pm.button(l='Create Fk Contol', h=35, c='creat_controlone()', bgc=(0.2, 0.5, 0.6))
    pm.separator(h=15)

    pm.rowLayout(p='FkContolCL', nc=3, adj=3)
    pm.text(l='Joint Parent Contol:', w=150, h=35)
    pm.iconTextButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/no_hi.jpg", h=35,
                        c='creat_controltwo()')
    pm.iconTextButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/hi.jpg", h=35,
                        c='creat_controlthree()')
    pm.setParent('..')
    pm.separator(h=15)

    # GUI Jt Show Hide
    pm.frameLayout(p='Box_one', mw=10, mh=1, w=360, l="Joint Show Hide", collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('ShowHideCL', adj=True)
    pm.rowLayout(p='ShowHideCL', nc=2, adj=2)
    pm.button(l='Show Jt', h=35, w=160, c='show_Jt()', bgc=(0.2, 0.5, 0.6))
    pm.button(l='Hide Jt', h=35, w=160, c='hide_Jt()', bgc=(0.2, 0.5, 0.6))
    pm.setParent('..')
    pm.separator(h=15)

    # Box_two
    pm.columnLayout('Box_two', p='ToolBoxTL', adj=0)


    # ===========changColor
    pm.frameLayout(p='Box_two', mw=10, mh=1, w=360, l='Change_Color', collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('rtchangColCL', adj=True)
    pm.separator(style='none', h=6)
    pm.rowLayout('rtchangColRL', p='rtchangColCL', nc=2, cw2=(20, 240))
    pm.text(l='', w=20)
    pm.columnLayout('rtchangColCL2', p='rtchangColRL', adj=0)

    pm.separator(w=288)
    pm.separator(style='none', h=3)
    pm.gridLayout('rtchangColGL', numberOfRows=4, numberOfColumns=8, cellWidthHeight=(36, 36))
    bgcIconList = [(0.627, 0.627, 0.627), (0.467, 0.467, 0.467), (0.000, 0.000, 0.000), (0.247, 0.247, 0.247),
                   (0.498, 0.498, 0.498), (0.608, 0.000, 0.157), (0.000, 0.016, 0.373), (0.000, 0.000, 1.000),
                   (0.000, 0.275, 0.094), (0.145, 0.000, 0.263), (0.780, 0.000, 0.780), (0.537, 0.278, 0.200),
                   (0.243, 0.133, 0.122), (0.600, 0.145, 0.000), (1.000, 0.000, 0.000), (0.000, 1.000, 0.000),
                   (0.000, 0.255, 0.600), (1.000, 1.000, 1.000), (1.000, 1.000, 0.000), (0.388, 0.863, 1.000),
                   (0.263, 1.000, 0.635), (1.000, 0.686, 0.686), (0.890, 0.675, 0.475), (1.000, 1.000, 0.384),
                   (0.000, 0.600, 0.325), (0.627, 0.412, 0.188), (0.620, 0.627, 0.188), (0.408, 0.627, 0.188),
                   (0.188, 0.627, 0.365), (0.188, 0.627, 0.627), (0.188, 0.404, 0.627), (0.435, 0.188, 0.627)]
    for i in range(len(bgcIconList)):
        pm.iconTextButton(p='rtchangColGL', bgc=bgcIconList[i], c='ChangeOverColor(%d)' % i)
    pm.separator(p='rtchangColCL2', style='none', h=3)
    pm.separator(p='rtchangColCL2', w=288)
    pm.separator(p='rtchangColCL2', style='none', h=3)

    pm.rowLayout('rtchangOpRL', p='rtchangColCL2', nc=3, cw3=(40, 100, 100))
    pm.text(l='Type:')
    pm.radioCollection('rtchangOp')
    pm.radioButton('rtcoShapeRB', l='Shape', sl=1)
    pm.radioButton('rtcoTransformRB', l='Transform')
    pm.separator(p='rtchangColCL2', style='none', h=6)

    # ===========chang Shape
    pm.frameLayout(p='Box_two', mw=10, mh=1, w=360, l='Change_Shape', collapsable=1, cl=0, bgc=(0, 0, 0))
    pm.columnLayout('ChangeTL', adj=1)

    pm.separator(p='ChangeTL', h=10)
    pm.gridLayout(nc=6, cellWidthHeight=(55, 55))
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_01.bmp",
                      c='Dt_Cl_01()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_02.bmp",
                      c='Dt_Cl_02()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_03.bmp",
                      c='Dt_Cl_03()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_04.bmp",
                      c='Dt_Cl_04()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_05.bmp",
                      c='Dt_Cl_05()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_06.bmp",
                      c='Dt_Cl_06()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_07.bmp",
                      c='Dt_Cl_07()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_08.bmp",
                      c='Dt_Cl_08()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_09.bmp",
                      c='Dt_Cl_09()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_10.bmp",
                      c='Dt_Cl_10()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_11.bmp",
                      c='Dt_Cl_11()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_12.bmp",
                      c='Dt_Cl_12()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_13.bmp",
                      c='Dt_Cl_13()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_14.bmp",
                      c='Dt_Cl_14()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_15.bmp",
                      c='Dt_Cl_15()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_16.bmp",
                      c='Dt_Cl_16()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_17.bmp",
                      c='Dt_Cl_17()')
    pm.symbolButton(image="G:/Develop/TeamCode/OF3D_RIG/modules/scripts/python/Rosa/tools/dt/icons/Dt_Cl_18.bmp",
                      c='Dt_Cl_18()')

    pm.setParent('..')
    pm.separator(p='ChangeTL', h=10)

    pm.rowLayout(nc=4, cw4=[50, 90, 90, 90], adj=4)
    pm.text(l='Type:')
    pm.radioCollection('typeOpRC')
    pm.radioButton('Replace', sl=1)
    pm.radioButton('Create')
    pm.radioButton('Add')
    pm.setParent('..')
    pm.separator(h=10)

    # select cv
    pm.separator(style='none', h=8)
    pm.rowLayout('rtrsScaleCVRL', nc=4, cw4=[120, 40, 105, 40], cal=[(1, 'center')])
    pm.button(l='Select All CV', w=80, c='dt_selectAllCurveCVProc()', bgc=(0.2, 0.5, 0.6))
    pm.floatField('rtrsScaleMinCVFS', v=-1, max=-0.1, w=28, pre=1, cc='dt_chgScaCVSMaxMinProc(1)')
    pm.floatSlider('rtrsScaleCVFS', max=1, w=105, min=-1, v=0, cc='dt_changeScaleCVSliderProc()')
    pm.floatField('rtrsScaleMaxCVFS', v=1, min=0.1, w=28, pre=1, cc='dt_chgScaCVSMaxMinProc(1)')

    #  Box_three
    pm.columnLayout('Box_three', p = 'ToolBoxTL', adj = 0)

    # GUI KeyFarme
    pm.frameLayout(p = 'Box_three', mw = 10, mh = 1, w = 360, l = 'KeyFarme', collapsable = 1, cl = 0, bgc = (0, 0, 0))
    pm.columnLayout('KeyFarmeCL', adj=True)

    pm.gridLayout(nc = 6, cellWidthHeight = (57, 57))
    pm.button(l = u'20', c = 'kframe(20)')
    pm.button(l = u'30', bgc = (0.2, 0.5, 0.6), c = 'kframe(30)')
    pm.button(l = u'45', c = 'kframe(45)')
    pm.button(l = u'50', bgc = (0.2, 0.5, 0.6), c = 'kframe(50)')
    pm.button(l = u'60', c = 'kframe(60)')
    pm.button(l = u'90', bgc = (0.2, 0.5, 0.6), c = 'kframe(90)')

    pm.button(l = u'100', bgc = (0.2, 0.5, 0.6), c = 'kframe(100)')
    pm.button(l = u'110', c = 'kframe(110)')
    pm.button(l = u'120', bgc = (0.2, 0.5, 0.6), c = 'kframe(120)')
    pm.button(l = u'130', c = 'kframe(130)')
    pm.button(l = u'135', bgc = (0.2, 0.5, 0.6), c = 'kframe(135)')
    pm.button(l = u'140', c = 'kframe(140)')
    pm.setParent('..')

    pm.separator(h = 10)

    pm.rowLayout(p = 'KeyFarmeCL', nc = 6, adj = 6)
    pm.text(l = u'轴向:')
    pm.radioCollection('rotate')
    pm.radioButton('pass', l = 'Pass', sl = 1)
    pm.radioButton('rotateX', l = 'Rotate_X')
    pm.radioButton('rotateY', l = 'Rotate_Y')
    pm.radioButton('rotateZ', l = 'Rotate_Z')
    pm.setParent('..')

    pm.rowLayout(p = 'KeyFarmeCL', nc = 6, adj = 6)
    pm.text(l = u'正负:')
    pm.radioCollection('PosNeg')
    pm.radioButton('pass', l = 'Pass', en=0)
    pm.radioButton('positive', l = u'正方向    ', sl = 1)
    pm.radioButton('negative', l = u'负方向   ')
    pm.radioButton('PosandNeg', l = u'正and负')
    pm.setParent('..')
    pm.separator(h = 10)

    pm.button(l = u'删除K帧并归零', h = 40, c = 'deframe()')
    pm.separator(h = 5)
    pm.button(l = u'斜方向控制器', h = 40, c = 'oblique()')
    pm.separator(h = 10)

    pm.showWindow()




def mod_apply():
    pm.select(ado=1)
    list_sel = pm.ls(sl=1, tr=1)
    if len(list_sel) == 0:
        pm.error("This is an empty file")
    else:

        mod_check()
        pm.select(cl=1)

# creat joint

def creat_jointone():
    sel = pm.ls(sl=1)
    if len(sel) != 0:
        pm.setToolTo('Move')
        pos = pm.manipMoveContext('Move', q=True, p=True)
    else:
        pos = (0, 0, 0)
    pm.select(cl=1)
    jnt = pm.joint()
    grp = pm.group(jnt, n=jnt + '_grp')
    pm.xform(grp, t=pos, ws=1)
    pm.select(jnt)
    pm.isolateSelect('modelPanel4', addSelected=1)

    pm.parent(world=True)
    pm.delete(grp)


def creat_jointtwo():
    sel = pm.ls(sl=1, fl=1)
    for i in sel:
        if ':' in i:
            obj = i.split('.')[0]
            all_number = i.split('[')[-1][:-1].split(':')
            a = int(all_number[1]) - int(all_number[0])
            for x in range(a + 1):
                point = '{0}.vtx[{1}]'.format(obj, int(all_number[0]) + x)
                xx = pm.xform(point, q=True, ws=True, t=True)
                pm.select(cl=True)
                jnt = pm.joint(position=(xx[0], xx[1], xx[2]))
                pm.select(jnt)
                pm.isolateSelect('modelPanel4', addSelected=1)

        else:
            xx = pm.xform(i, q=True, ws=True, t=True)
            pm.select(cl=True)
            jnt = pm.joint(position=(xx[0], xx[1], xx[2]))
            pm.select(jnt)
            pm.isolateSelect('modelPanel4', addSelected=1)


# creat control one
def creat_controlone():
    conT = pm.checkBox('fkConTCB', q=1, v=1)
    conR = pm.checkBox('fkConRCB', q=1, v=1)
    conS = pm.checkBox('fkConSCB', q=1, v=1)
    list_jnt = pm.ls(sl=True)

    for jnt in list_jnt:
        crl = pm.circle(n=jnt + '_Ct')
        grp = pm.group(n=jnt + '_Ct_Grp')
        jnt = pm.rename(jnt, jnt + '_Jt')

        pm.select(jnt, r=True)
        pm.select(grp, r=True)
        pm.parentConstraint(jnt, grp)
        pm.delete(cn=True)
        pm.select(crl)
        pm.isolateSelect('modelPanel4', addSelected=1)
        if (conT and conR):
            pm.parentConstraint(crl[0], jnt)
        elif (conT):
            pm.pointConstraint(crl[0], jnt)
            pm.setAttr(crl[0] + '.rx', k=0, l=1)
            pm.setAttr(crl[0] + '.ry', k=0, l=1)
            pm.setAttr(crl[0] + '.rz', k=0, l=1)
        elif (conR):
            pm.orientConstraint(crl[0], jnt)
            pm.setAttr(crl[0] + '.tx', k=0, l=1)
            pm.setAttr(crl[0] + '.ty', k=0, l=1)
            pm.setAttr(crl[0] + '.tz', k=0, l=1)
        if (conS):
            pm.scaleConstraint(crl[0], jnt)
        else:
            pm.setAttr(crl[0] + '.sx', k=0, l=1)
            pm.setAttr(crl[0] + '.sy', k=0, l=1)
            pm.setAttr(crl[0] + '.sz', k=0, l=1)


# creat control two
def creat_controltwo():
    list_jnt = pm.ls(sl=True)
    if len(list_jnt) == 0:
        pm.error('Please select at least one joint !')
    else:
        for jnt in list_jnt:
            crl = pm.circle(n=jnt + '_Ct')
            grp = pm.group(n=jnt + '_Ct_Grp')
            jnt = pm.rename(jnt, jnt + '_Jt')

            pm.select(jnt, r=True)
            pm.select(grp, r=True)
            pm.parentConstraint(jnt, grp)
            pm.delete(cn=True)
            pm.parent(jnt, crl[0])
            pm.select(crl)
            pm.isolateSelect('modelPanel4', addSelected=1)


# # creat control three
def creat_controlthree():
    list_jnt = pm.ls(sl=True)
    list_crl = []
    list_grp = []
    if len(list_jnt) == 0:
        pm.error('Please select at least one joint !')
    else:
        for jnt in list_jnt:
            crl = pm.circle(n=jnt + '_Ct')
            list_crl.append(crl[0])
            grp = pm.group(n=jnt + '_Ct_Grp')
            list_grp.append(grp)
            jnt = pm.rename(jnt, jnt + '_Jt')

            pm.select(jnt, r=True)
            pm.select(grp, r=True)
            pm.parentConstraint(jnt, grp)
            pm.delete(cn=True)
            pm.parent(jnt, crl[0])
            pm.select(crl)
            pm.isolateSelect('modelPanel4', addSelected=1)

    a = 0
    c = len(list_crl)
    while a < c - 1:
        pm.parent(list_grp[a + 1], list_crl[a])
        a += 1


def openAttr():
    judge = pm.ls(sl=1)
    if len(judge) == 0:
        print("judge")

        pm.select('Model_Grp', hi=1)
        shape_list = pm.ls(sl=1, type="mesh")
        for shape in shape_list:
            shape_Enable = shape + ".rsEnableSubdivision"
            shape_Max = shape + ".rsMaxTessellationSubdivs"

            pm.setAttr(shape_Enable, 1)
            pm.setAttr(shape_Max, 3)

    else:
        shape_list = pm.listRelatives(c=1,type="mesh")

        for shape in shape_list:
            shape_Enable = shape + ".rsEnableSubdivision"
            shape_Max = shape + ".rsMaxTessellationSubdivs"

            pm.setAttr(shape_Enable, 1)
            pm.setAttr(shape_Max, 3)


# Rename and number
def rename_number():
    list_selone = pm.ls(sl=True)
    pm.select(list_selone)
    list_selall = pm.ls(sl=1, tr=1)
    input_one = pm.textField('renameTF', q=True, tx=True)

    str_starting = pm.textField('startingTF', q=True, tx=True)
    str_padding = pm.textField('paddingTF', q=True, tx=True)

    str_number = str_starting.zfill(int(str_padding))

    for name_l in list_selall:
        pm.rename(name_l, input_one + '_' + str_number)
        str_number = str(int(str_number) + 1).zfill(int(str_padding))


# Add fixed suffix _Jt
def suffix_jnt():
    suffix_Jt_a = '0'

    if suffix_Jt_a == '1':
        pass

    elif suffix_Jt_a == '0':
        list_selfour = pm.ls(sl=True)
        pm.select(list_selfour)
        list_selall = pm.ls(sl=True, tr=1)
        for suffix_Jt in list_selall:
            suffix_Jt_s = suffix_Jt
            if '|' in suffix_Jt:
                suffix_Jt_s = suffix_Jt.split('|')[-1]
            if suffix_Jt_a == '0':
                new_suffix = suffix_Jt_s + '_jnt'
                pm.rename(suffix_Jt, new_suffix)


# Add fixed suffix _ctrl
def suffix_ctrl():
    suffix_Ct_a = '0'

    if suffix_Ct_a == '1':
        pass

    elif suffix_Ct_a == '0':
        list_selfive = pm.ls(sl=True)
        pm.select(list_selfive)
        list_selall = pm.ls(sl=1, tr=1)

        for suffix_Ct in list_selall:
            suffix_Ct_s = suffix_Ct
            if '|' in suffix_Ct:
                suffix_Ct_s = suffix_Ct.split('|')[-1]
            if suffix_Ct_a == '0':
                new_suffix = suffix_Ct_s + '_ctrl'
                pm.rename(suffix_Ct, new_suffix)


# Add fixed suffix _old
def suffix_old():
    suffix_old_a = '0'

    if suffix_old_a == '1':
        pass

    elif suffix_old_a == '0':
        list_selsix = pm.ls(sl=True)
        pm.select(list_selsix)
        list_selall = pm.ls(sl=1, tr=1)

        for suffix_old in list_selall:
            suffix_old_s = suffix_old
            if '|' in suffix_old:
                suffix_old_s = suffix_old.split('|')[-1]
            if suffix_old_a == '0':
                new_suffix = suffix_old_s + '_old'
                pm.rename(suffix_old, new_suffix)

# Add fixed suffix _new
def suffix_new():
    suffix_new_a = '0'

    if suffix_new_a == '1':
        pass

    elif suffix_new_a == '0':
        list_selsix = pm.ls(sl=True)
        pm.select(list_selsix)
        list_selall = pm.ls(sl=1, tr=1)

        for suffix_new in list_selall:
            suffix_new_s = suffix_new
            if '|' in suffix_new:
                suffix_new_s = suffix_new.split('|')[-1]
            if suffix_new_a == '0':
                new_suffix = suffix_new_s + '_new'
                pm.rename(suffix_new, new_suffix)


# show hide jt
def show_Jt():
    jnt_sel = pm.ls(sl=1)
    jnts = pm.ls(type='joint')
    if len(jnt_sel) != 0:
        for jnt in jnt_sel:
            pm.setAttr(jnt + '.drawStyle', 0)
    else:
        for jnt in jnts:
            pm.setAttr(jnt + '.drawStyle', 0)
    




def hide_Jt():
    jnt_sel = pm.ls(sl=1)
    jnts = pm.ls(type='joint')
    if len(jnt_sel) != 0:
        for jnt in jnt_sel:
            pm.setAttr(jnt + '.drawStyle', 2)
    else:
        for jnt in jnts:
            pm.setAttr(jnt + '.drawStyle', 2)


# 改变控制器颜色
def ChangeOverColor(typ):
    sel = pm.ls(sl=1)
    for i in sel:
        objList = pm.listRelatives(i, s=1, f=1)
        if (pm.radioCollection('rtchangOp', q=1, sl=1) == 'rtcoTransformRB' or objList == None):
            objList = [i, ]
        if (typ == 0):
            typ = 4
        for o in objList:
            pm.setAttr(o + '.overrideEnabled', 1)
            pm.setAttr(o + '.overrideColor', typ - 1)


# Dt_Cl_01()
def Dt_Cl_01():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0.504214, 0, 0), (0.491572, 0.112198, 0), (0.454281, 0.21877, 0),
                                         (0.394211, 0.314372, 0), (0.314372, 0.394211, 0), (0.21877, 0.454281, 0),
                                         (0.112198, 0.491572, 0), (0, 0.504214, 0), (-0.112198, 0.491572, 0),
                                         (-0.21877, 0.454281, 0), (-0.314372, 0.394211, 0), (-0.394211, 0.314372, 0),
                                         (-0.454281, 0.21877, 0), (-0.491572, 0.112198, 0), (-0.504214, 0, 0),
                                         (-0.491572, -0.112198, 0), (-0.454281, -0.21877, 0), (-0.394211, -0.314372, 0),
                                         (-0.314372, -0.394211, 0), (-0.21877, -0.454281, 0), (-0.112198, -0.491572, 0),
                                         (0, -0.504214, 0), (0.112198, -0.491572, 0), (0.21877, -0.454281, 0),
                                         (0.314372, -0.394211, 0), (0.394211, -0.314372, 0), (0.454281, -0.21877, 0),
                                         (0.491572, -0.112198, 0), (0.504214, 0, 0), (0.491572, 0, -0.112198),
                                         (0.454281, 0, -0.21877), (0.394211, 0, -0.314372), (0.314372, 0, -0.394211),
                                         (0.21877, 0, -0.454281), (0.112198, 0, -0.491572), (0, 0, -0.504214),
                                         (-0.112198, 0, -0.491572), (-0.21877, 0, -0.454281), (-0.314372, 0, -0.394211),
                                         (-0.394211, 0, -0.314372), (-0.454281, 0, -0.21877), (-0.491572, 0, -0.112198),
                                         (-0.504214, 0, 0), (-0.491572, 0, 0.112198), (-0.454281, 0, 0.21877),
                                         (-0.394211, 0, 0.314372), (-0.314372, 0, 0.394211), (-0.21877, 0, 0.454281),
                                         (-0.112198, 0, 0.491572), (0, 0, 0.504214), (0, 0.112198, 0.491572),
                                         (0, 0.21877, 0.454281), (0, 0.314372, 0.394211), (0, 0.394211, 0.314372),
                                         (0, 0.454281, 0.21877), (0, 0.491572, 0.112198), (0, 0.504214, 0),
                                         (0, 0.491572, -0.112198), (0, 0.454281, -0.21877), (0, 0.394211, -0.314372),
                                         (0, 0.314372, -0.394211), (0, 0.21877, -0.454281), (0, 0.112198, -0.491572),
                                         (0, 0, -0.504214), (0, -0.112198, -0.491572), (0, -0.21877, -0.454281),
                                         (0, -0.314372, -0.394211), (0, -0.394211, -0.314372), (0, -0.454281, -0.21877),
                                         (0, -0.491572, -0.112198), (0, -0.504214, 0), (0, -0.491572, 0.112198),
                                         (0, -0.454281, 0.21877), (0, -0.394211, 0.314372), (0, -0.314372, 0.394211),
                                         (0, -0.21877, 0.454281), (0, -0.112198, 0.491572), (0, 0, 0.504214),
                                         (0.112198, 0, 0.491572), (0.21877, 0, 0.454281), (0.314372, 0, 0.394211),
                                         (0.394211, 0, 0.314372), (0.454281, 0, 0.21877), (0.491572, 0, 0.112198),
                                         (0.504214, 0, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0.504214, 0, 0), (0.491572, 0.112198, 0), (0.454281, 0.21877, 0),
                                         (0.394211, 0.314372, 0), (0.314372, 0.394211, 0), (0.21877, 0.454281, 0),
                                         (0.112198, 0.491572, 0), (0, 0.504214, 0), (-0.112198, 0.491572, 0),
                                         (-0.21877, 0.454281, 0), (-0.314372, 0.394211, 0), (-0.394211, 0.314372, 0),
                                         (-0.454281, 0.21877, 0), (-0.491572, 0.112198, 0), (-0.504214, 0, 0),
                                         (-0.491572, -0.112198, 0), (-0.454281, -0.21877, 0), (-0.394211, -0.314372, 0),
                                         (-0.314372, -0.394211, 0), (-0.21877, -0.454281, 0), (-0.112198, -0.491572, 0),
                                         (0, -0.504214, 0), (0.112198, -0.491572, 0), (0.21877, -0.454281, 0),
                                         (0.314372, -0.394211, 0), (0.394211, -0.314372, 0), (0.454281, -0.21877, 0),
                                         (0.491572, -0.112198, 0), (0.504214, 0, 0), (0.491572, 0, -0.112198),
                                         (0.454281, 0, -0.21877), (0.394211, 0, -0.314372), (0.314372, 0, -0.394211),
                                         (0.21877, 0, -0.454281), (0.112198, 0, -0.491572), (0, 0, -0.504214),
                                         (-0.112198, 0, -0.491572), (-0.21877, 0, -0.454281), (-0.314372, 0, -0.394211),
                                         (-0.394211, 0, -0.314372), (-0.454281, 0, -0.21877), (-0.491572, 0, -0.112198),
                                         (-0.504214, 0, 0), (-0.491572, 0, 0.112198), (-0.454281, 0, 0.21877),
                                         (-0.394211, 0, 0.314372), (-0.314372, 0, 0.394211), (-0.21877, 0, 0.454281),
                                         (-0.112198, 0, 0.491572), (0, 0, 0.504214), (0, 0.112198, 0.491572),
                                         (0, 0.21877, 0.454281), (0, 0.314372, 0.394211), (0, 0.394211, 0.314372),
                                         (0, 0.454281, 0.21877), (0, 0.491572, 0.112198), (0, 0.504214, 0),
                                         (0, 0.491572, -0.112198), (0, 0.454281, -0.21877), (0, 0.394211, -0.314372),
                                         (0, 0.314372, -0.394211), (0, 0.21877, -0.454281), (0, 0.112198, -0.491572),
                                         (0, 0, -0.504214), (0, -0.112198, -0.491572), (0, -0.21877, -0.454281),
                                         (0, -0.314372, -0.394211), (0, -0.394211, -0.314372), (0, -0.454281, -0.21877),
                                         (0, -0.491572, -0.112198), (0, -0.504214, 0), (0, -0.491572, 0.112198),
                                         (0, -0.454281, 0.21877), (0, -0.394211, 0.314372), (0, -0.314372, 0.394211),
                                         (0, -0.21877, 0.454281), (0, -0.112198, 0.491572), (0, 0, 0.504214),
                                         (0.112198, 0, 0.491572), (0.21877, 0, 0.454281), (0.314372, 0, 0.394211),
                                         (0.394211, 0, 0.314372), (0.454281, 0, 0.21877), (0.491572, 0, 0.112198),
                                         (0.504214, 0, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.504214, 0, 0), (0.491572, 0.112198, 0), (0.454281, 0.21877, 0),
                                       (0.394211, 0.314372, 0), (0.314372, 0.394211, 0), (0.21877, 0.454281, 0),
                                       (0.112198, 0.491572, 0), (0, 0.504214, 0), (-0.112198, 0.491572, 0),
                                       (-0.21877, 0.454281, 0), (-0.314372, 0.394211, 0), (-0.394211, 0.314372, 0),
                                       (-0.454281, 0.21877, 0), (-0.491572, 0.112198, 0), (-0.504214, 0, 0),
                                       (-0.491572, -0.112198, 0), (-0.454281, -0.21877, 0), (-0.394211, -0.314372, 0),
                                       (-0.314372, -0.394211, 0), (-0.21877, -0.454281, 0), (-0.112198, -0.491572, 0),
                                       (0, -0.504214, 0), (0.112198, -0.491572, 0), (0.21877, -0.454281, 0),
                                       (0.314372, -0.394211, 0), (0.394211, -0.314372, 0), (0.454281, -0.21877, 0),
                                       (0.491572, -0.112198, 0), (0.504214, 0, 0), (0.491572, 0, -0.112198),
                                       (0.454281, 0, -0.21877), (0.394211, 0, -0.314372), (0.314372, 0, -0.394211),
                                       (0.21877, 0, -0.454281), (0.112198, 0, -0.491572), (0, 0, -0.504214),
                                       (-0.112198, 0, -0.491572), (-0.21877, 0, -0.454281), (-0.314372, 0, -0.394211),
                                       (-0.394211, 0, -0.314372), (-0.454281, 0, -0.21877), (-0.491572, 0, -0.112198),
                                       (-0.504214, 0, 0), (-0.491572, 0, 0.112198), (-0.454281, 0, 0.21877),
                                       (-0.394211, 0, 0.314372), (-0.314372, 0, 0.394211), (-0.21877, 0, 0.454281),
                                       (-0.112198, 0, 0.491572), (0, 0, 0.504214), (0, 0.112198, 0.491572),
                                       (0, 0.21877, 0.454281), (0, 0.314372, 0.394211), (0, 0.394211, 0.314372),
                                       (0, 0.454281, 0.21877), (0, 0.491572, 0.112198), (0, 0.504214, 0),
                                       (0, 0.491572, -0.112198), (0, 0.454281, -0.21877), (0, 0.394211, -0.314372),
                                       (0, 0.314372, -0.394211), (0, 0.21877, -0.454281), (0, 0.112198, -0.491572),
                                       (0, 0, -0.504214), (0, -0.112198, -0.491572), (0, -0.21877, -0.454281),
                                       (0, -0.314372, -0.394211), (0, -0.394211, -0.314372), (0, -0.454281, -0.21877),
                                       (0, -0.491572, -0.112198), (0, -0.504214, 0), (0, -0.491572, 0.112198),
                                       (0, -0.454281, 0.21877), (0, -0.394211, 0.314372), (0, -0.314372, 0.394211),
                                       (0, -0.21877, 0.454281), (0, -0.112198, 0.491572), (0, 0, 0.504214),
                                       (0.112198, 0, 0.491572), (0.21877, 0, 0.454281), (0.314372, 0, 0.394211),
                                       (0.394211, 0, 0.314372), (0.454281, 0, 0.21877), (0.491572, 0, 0.112198),
                                       (0.504214, 0, 0)])


# Dt_Cl_02()
def Dt_Cl_02():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                                         (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                         (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                                         (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                                         (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                         (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                                         (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                                       (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                       (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
                                       (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)])


# Dt_Cl_03()
def Dt_Cl_03():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0.0, -0.5, 0.5), (0.0, 0.5, 0.5), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                         (0.0, -0.5, 0.5), (1.0, 0.0, 0.0), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                         (1.0, 0.0, 0.0), (0.0, 0.5, 0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0.0, -0.5, 0.5), (0.0, 0.5, 0.5), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                         (0.0, -0.5, 0.5), (1.0, 0.0, 0.0), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                         (1.0, 0.0, 0.0), (0.0, 0.5, 0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.0, -0.5, 0.5), (0.0, 0.5, 0.5), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                       (0.0, -0.5, 0.5), (1.0, 0.0, 0.0), (0.0, 0.5, -0.5), (0.0, -0.5, -0.5),
                                       (1.0, 0.0, 0.0), (0.0, 0.5, 0.5)])


# Dt_Cl_04()
def Dt_Cl_04():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1,
                                 p=[(0.0, 0.0, 0.972), (0.289, 0.0, 0.683), (0.144, 0.0, 0.683), (0.144, 0.0, 0.538),
                                    (0.17, 0.0, 0.532), (0.216, 0.0, 0.516), (0.28, 0.0, 0.485), (0.341, 0.0, 0.444),
                                    (0.396, 0.0, 0.396), (0.444, 0.0, 0.341), (0.485, 0.0, 0.28), (0.516, 0.0, 0.216),
                                    (0.532, 0.0, 0.17), (0.539, 0.0, 0.144), (0.683, 0.0, 0.144), (0.683, 0.0, 0.289),
                                    (0.972, 0.0, 0.0), (0.683, 0.0, -0.289), (0.683, 0.0, -0.144), (0.538, 0.0, -0.144),
                                    (0.532, 0.0, -0.17), (0.516, 0.0, -0.216), (0.485, 0.0, -0.28),
                                    (0.444, 0.0, -0.341), (0.396, 0.0, -0.396), (0.341, 0.0, -0.444),
                                    (0.28, 0.0, -0.485), (0.216, 0.0, -0.516), (0.17, 0.0, -0.532),
                                    (0.144, 0.0, -0.539), (0.144, 0.0, -0.683), (0.289, 0.0, -0.683),
                                    (0.0, 0.0, -0.972), (-0.289, 0.0, -0.683), (-0.144, 0.0, -0.683),
                                    (-0.144, 0.0, -0.538), (-0.17, 0.0, -0.532), (-0.216, 0.0, -0.516),
                                    (-0.28, 0.0, -0.485), (-0.341, 0.0, -0.444), (-0.396, 0.0, -0.396),
                                    (-0.444, 0.0, -0.341), (-0.485, 0.0, -0.28), (-0.516, 0.0, -0.216),
                                    (-0.532, 0.0, -0.17), (-0.539, 0.0, -0.144), (-0.683, 0.0, -0.144),
                                    (-0.683, 0.0, -0.289), (-0.972, 0.0, 0.0), (-0.683, 0.0, 0.289),
                                    (-0.683, 0.0, 0.144), (-0.538, 0.0, 0.144), (-0.533, 0.0, 0.168),
                                    (-0.517, 0.0, 0.214), (-0.485, 0.0, 0.28), (-0.444, 0.0, 0.341),
                                    (-0.396, 0.0, 0.396), (-0.341, 0.0, 0.444), (-0.28, 0.0, 0.485),
                                    (-0.216, 0.0, 0.516), (-0.17, 0.0, 0.532), (-0.144, 0.0, 0.539),
                                    (-0.144, 0.0, 0.683), (-0.289, 0.0, 0.683), (0.0, 0.0, 0.972)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1,
                                 p=[(0.0, 0.0, 0.972), (0.289, 0.0, 0.683), (0.144, 0.0, 0.683), (0.144, 0.0, 0.538),
                                    (0.17, 0.0, 0.532), (0.216, 0.0, 0.516), (0.28, 0.0, 0.485), (0.341, 0.0, 0.444),
                                    (0.396, 0.0, 0.396), (0.444, 0.0, 0.341), (0.485, 0.0, 0.28), (0.516, 0.0, 0.216),
                                    (0.532, 0.0, 0.17), (0.539, 0.0, 0.144), (0.683, 0.0, 0.144), (0.683, 0.0, 0.289),
                                    (0.972, 0.0, 0.0), (0.683, 0.0, -0.289), (0.683, 0.0, -0.144), (0.538, 0.0, -0.144),
                                    (0.532, 0.0, -0.17), (0.516, 0.0, -0.216), (0.485, 0.0, -0.28),
                                    (0.444, 0.0, -0.341), (0.396, 0.0, -0.396), (0.341, 0.0, -0.444),
                                    (0.28, 0.0, -0.485), (0.216, 0.0, -0.516), (0.17, 0.0, -0.532),
                                    (0.144, 0.0, -0.539), (0.144, 0.0, -0.683), (0.289, 0.0, -0.683),
                                    (0.0, 0.0, -0.972), (-0.289, 0.0, -0.683), (-0.144, 0.0, -0.683),
                                    (-0.144, 0.0, -0.538), (-0.17, 0.0, -0.532), (-0.216, 0.0, -0.516),
                                    (-0.28, 0.0, -0.485), (-0.341, 0.0, -0.444), (-0.396, 0.0, -0.396),
                                    (-0.444, 0.0, -0.341), (-0.485, 0.0, -0.28), (-0.516, 0.0, -0.216),
                                    (-0.532, 0.0, -0.17), (-0.539, 0.0, -0.144), (-0.683, 0.0, -0.144),
                                    (-0.683, 0.0, -0.289), (-0.972, 0.0, 0.0), (-0.683, 0.0, 0.289),
                                    (-0.683, 0.0, 0.144), (-0.538, 0.0, 0.144), (-0.533, 0.0, 0.168),
                                    (-0.517, 0.0, 0.214), (-0.485, 0.0, 0.28), (-0.444, 0.0, 0.341),
                                    (-0.396, 0.0, 0.396), (-0.341, 0.0, 0.444), (-0.28, 0.0, 0.485),
                                    (-0.216, 0.0, 0.516), (-0.17, 0.0, 0.532), (-0.144, 0.0, 0.539),
                                    (-0.144, 0.0, 0.683), (-0.289, 0.0, 0.683), (0.0, 0.0, 0.972)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.0, 0.0, 0.972), (0.289, 0.0, 0.683), (0.144, 0.0, 0.683), (0.144, 0.0, 0.538),
                                       (0.17, 0.0, 0.532), (0.216, 0.0, 0.516), (0.28, 0.0, 0.485), (0.341, 0.0, 0.444),
                                       (0.396, 0.0, 0.396), (0.444, 0.0, 0.341), (0.485, 0.0, 0.28),
                                       (0.516, 0.0, 0.216), (0.532, 0.0, 0.17), (0.539, 0.0, 0.144),
                                       (0.683, 0.0, 0.144), (0.683, 0.0, 0.289), (0.972, 0.0, 0.0),
                                       (0.683, 0.0, -0.289), (0.683, 0.0, -0.144), (0.538, 0.0, -0.144),
                                       (0.532, 0.0, -0.17), (0.516, 0.0, -0.216), (0.485, 0.0, -0.28),
                                       (0.444, 0.0, -0.341), (0.396, 0.0, -0.396), (0.341, 0.0, -0.444),
                                       (0.28, 0.0, -0.485), (0.216, 0.0, -0.516), (0.17, 0.0, -0.532),
                                       (0.144, 0.0, -0.539), (0.144, 0.0, -0.683), (0.289, 0.0, -0.683),
                                       (0.0, 0.0, -0.972), (-0.289, 0.0, -0.683), (-0.144, 0.0, -0.683),
                                       (-0.144, 0.0, -0.538), (-0.17, 0.0, -0.532), (-0.216, 0.0, -0.516),
                                       (-0.28, 0.0, -0.485), (-0.341, 0.0, -0.444), (-0.396, 0.0, -0.396),
                                       (-0.444, 0.0, -0.341), (-0.485, 0.0, -0.28), (-0.516, 0.0, -0.216),
                                       (-0.532, 0.0, -0.17), (-0.539, 0.0, -0.144), (-0.683, 0.0, -0.144),
                                       (-0.683, 0.0, -0.289), (-0.972, 0.0, 0.0), (-0.683, 0.0, 0.289),
                                       (-0.683, 0.0, 0.144), (-0.538, 0.0, 0.144), (-0.533, 0.0, 0.168),
                                       (-0.517, 0.0, 0.214), (-0.485, 0.0, 0.28), (-0.444, 0.0, 0.341),
                                       (-0.396, 0.0, 0.396), (-0.341, 0.0, 0.444), (-0.28, 0.0, 0.485),
                                       (-0.216, 0.0, 0.516), (-0.17, 0.0, 0.532), (-0.144, 0.0, 0.539),
                                       (-0.144, 0.0, 0.683), (-0.289, 0.0, 0.683), (0.0, 0.0, 0.972)])


# Dt_Cl_05()
def Dt_Cl_05():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=3,
                                 p=[(0.0, -0.001, 0.758), (0.0, -0.0, 0.758), (0.0, -0.0, 0.758), (0.0, 0.023, 0.76),
                                    (0.0, 0.091, 0.774), (0.0, 0.123, 0.881), (0.0, 0.087, 0.956), (0.0, -0.0, 0.992),
                                    (0.0, -0.087, 0.956), (0.0, -0.124, 0.868), (0.0, -0.085, 0.782),
                                    (0.0, -0.021, 0.758), (0.0, -0.001, 0.758), (0.0, -0.001, 0.758),
                                    (0.0, -0.0, 0.758), (0.0, -0.0, -0.764), (0.0, -0.0, -0.764), (0.0, -0.0, -0.764),
                                    (0.0, -0.021, -0.764), (0.0, -0.085, -0.788), (0.0, -0.124, -0.874),
                                    (0.0, -0.087, -0.962), (0.0, -0.0, -0.998), (0.0, 0.087, -0.962),
                                    (0.0, 0.123, -0.887), (0.0, 0.091, -0.78), (0.0, 0.023, -0.766),
                                    (0.0, -0.0, -0.764), (0.0, -0.0, -0.764)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=3,
                                 p=[(0.0, -0.001, 0.758), (0.0, -0.0, 0.758), (0.0, -0.0, 0.758), (0.0, 0.023, 0.76),
                                    (0.0, 0.091, 0.774), (0.0, 0.123, 0.881), (0.0, 0.087, 0.956), (0.0, -0.0, 0.992),
                                    (0.0, -0.087, 0.956), (0.0, -0.124, 0.868), (0.0, -0.085, 0.782),
                                    (0.0, -0.021, 0.758), (0.0, -0.001, 0.758), (0.0, -0.001, 0.758),
                                    (0.0, -0.0, 0.758), (0.0, -0.0, -0.764), (0.0, -0.0, -0.764), (0.0, -0.0, -0.764),
                                    (0.0, -0.021, -0.764), (0.0, -0.085, -0.788), (0.0, -0.124, -0.874),
                                    (0.0, -0.087, -0.962), (0.0, -0.0, -0.998), (0.0, 0.087, -0.962),
                                    (0.0, 0.123, -0.887), (0.0, 0.091, -0.78), (0.0, 0.023, -0.766),
                                    (0.0, -0.0, -0.764), (0.0, -0.0, -0.764)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=3, p=[(0.0, -0.001, 0.758), (0.0, -0.0, 0.758), (0.0, -0.0, 0.758), (0.0, 0.023, 0.76),
                                       (0.0, 0.091, 0.774), (0.0, 0.123, 0.881), (0.0, 0.087, 0.956),
                                       (0.0, -0.0, 0.992), (0.0, -0.087, 0.956), (0.0, -0.124, 0.868),
                                       (0.0, -0.085, 0.782), (0.0, -0.021, 0.758), (0.0, -0.001, 0.758),
                                       (0.0, -0.001, 0.758), (0.0, -0.0, 0.758), (0.0, -0.0, -0.764),
                                       (0.0, -0.0, -0.764), (0.0, -0.0, -0.764), (0.0, -0.021, -0.764),
                                       (0.0, -0.085, -0.788), (0.0, -0.124, -0.874), (0.0, -0.087, -0.962),
                                       (0.0, -0.0, -0.998), (0.0, 0.087, -0.962), (0.0, 0.123, -0.887),
                                       (0.0, 0.091, -0.78), (0.0, 0.023, -0.766), (0.0, -0.0, -0.764),
                                       (0.0, -0.0, -0.764)])


# Dt_Cl_06()
def Dt_Cl_06():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1,
                                 p=[(0.0, 0.0, 0.976), (0.0, -0.29, 0.686), (0.0, -0.145, 0.686), (0.0, -0.145, 0.541),
                                    (0.0, -0.209, 0.523), (0.0, -0.321, 0.47), (0.0, -0.452, 0.347),
                                    (0.0, -0.54, 0.183), (0.0, -0.57, 0.0), (0.0, -0.54, -0.183), (0.0, -0.452, -0.347),
                                    (0.0, -0.317, -0.474), (0.0, -0.204, -0.525), (0.0, -0.145, -0.541),
                                    (0.0, -0.145, -0.686), (0.0, -0.29, -0.686), (0.0, 0.0, -0.976),
                                    (0.0, 0.29, -0.686), (0.0, 0.145, -0.686), (0.0, 0.145, -0.541),
                                    (0.0, 0.209, -0.523), (0.0, 0.321, -0.47), (0.0, 0.452, -0.347),
                                    (0.0, 0.54, -0.183), (0.0, 0.57, 0.0), (0.0, 0.54, 0.183), (0.0, 0.452, 0.347),
                                    (0.0, 0.321, 0.47), (0.0, 0.209, 0.523), (0.0, 0.145, 0.54), (0.0, 0.145, 0.686),
                                    (0.0, 0.29, 0.686), (0.0, 0.0, 0.976)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1,
                                 p=[(0.0, 0.0, 0.976), (0.0, -0.29, 0.686), (0.0, -0.145, 0.686), (0.0, -0.145, 0.541),
                                    (0.0, -0.209, 0.523), (0.0, -0.321, 0.47), (0.0, -0.452, 0.347),
                                    (0.0, -0.54, 0.183), (0.0, -0.57, 0.0), (0.0, -0.54, -0.183), (0.0, -0.452, -0.347),
                                    (0.0, -0.317, -0.474), (0.0, -0.204, -0.525), (0.0, -0.145, -0.541),
                                    (0.0, -0.145, -0.686), (0.0, -0.29, -0.686), (0.0, 0.0, -0.976),
                                    (0.0, 0.29, -0.686), (0.0, 0.145, -0.686), (0.0, 0.145, -0.541),
                                    (0.0, 0.209, -0.523), (0.0, 0.321, -0.47), (0.0, 0.452, -0.347),
                                    (0.0, 0.54, -0.183), (0.0, 0.57, 0.0), (0.0, 0.54, 0.183), (0.0, 0.452, 0.347),
                                    (0.0, 0.321, 0.47), (0.0, 0.209, 0.523), (0.0, 0.145, 0.54), (0.0, 0.145, 0.686),
                                    (0.0, 0.29, 0.686), (0.0, 0.0, 0.976)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1,
                               p=[(0.0, 0.0, 0.976), (0.0, -0.29, 0.686), (0.0, -0.145, 0.686), (0.0, -0.145, 0.541),
                                  (0.0, -0.209, 0.523), (0.0, -0.321, 0.47), (0.0, -0.452, 0.347), (0.0, -0.54, 0.183),
                                  (0.0, -0.57, 0.0), (0.0, -0.54, -0.183), (0.0, -0.452, -0.347), (0.0, -0.317, -0.474),
                                  (0.0, -0.204, -0.525), (0.0, -0.145, -0.541), (0.0, -0.145, -0.686),
                                  (0.0, -0.29, -0.686), (0.0, 0.0, -0.976), (0.0, 0.29, -0.686), (0.0, 0.145, -0.686),
                                  (0.0, 0.145, -0.541), (0.0, 0.209, -0.523), (0.0, 0.321, -0.47), (0.0, 0.452, -0.347),
                                  (0.0, 0.54, -0.183), (0.0, 0.57, 0.0), (0.0, 0.54, 0.183), (0.0, 0.452, 0.347),
                                  (0.0, 0.321, 0.47), (0.0, 0.209, 0.523), (0.0, 0.145, 0.54), (0.0, 0.145, 0.686),
                                  (0.0, 0.29, 0.686), (0.0, 0.0, 0.976)])


# Dt_Cl_07()
def Dt_Cl_07():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(-0.4, 0.0, 0.2), (0.2, 0.0, 0.2), (0.2, 0.0, 0.4), (0.6, 0.0, 0.0),
                                         (0.2, 0.0, -0.4), (0.2, 0.0, -0.2), (-0.4, 0.0, -0.2), (-0.4, 0.0, 0.2)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(-0.4, 0.0, 0.2), (0.2, 0.0, 0.2), (0.2, 0.0, 0.4), (0.6, 0.0, 0.0),
                                         (0.2, 0.0, -0.4), (0.2, 0.0, -0.2), (-0.4, 0.0, -0.2), (-0.4, 0.0, 0.2)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1,
                               p=[(-0.4, 0.0, 0.2), (0.2, 0.0, 0.2), (0.2, 0.0, 0.4), (0.6, 0.0, 0.0), (0.2, 0.0, -0.4),
                                  (0.2, 0.0, -0.2), (-0.4, 0.0, -0.2), (-0.4, 0.0, 0.2)])


# Dt_Cl_08()
def Dt_Cl_08():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.5), (0.0, -0.15, 0.35), (0.0, -0.05, 0.35), (0.0, -0.05, 0.05),
                                         (0.0, -0.35, 0.05), (0.0, -0.35, 0.15), (0.0, -0.5, 0.0), (0.0, -0.35, -0.15),
                                         (0.0, -0.35, -0.05), (0.0, -0.05, -0.05), (0.0, -0.05, -0.35),
                                         (0.0, -0.15, -0.35), (0.0, 0.0, -0.5), (0.0, 0.15, -0.35), (0.0, 0.05, -0.35),
                                         (0.0, 0.05, -0.05), (0.0, 0.35, -0.05), (0.0, 0.35, -0.15), (0.0, 0.5, 0.0),
                                         (0.0, 0.35, 0.15), (0.0, 0.35, 0.05), (0.0, 0.05, 0.05), (0.0, 0.05, 0.35),
                                         (0.0, 0.15, 0.35), (0, 0, 0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.5), (0.0, -0.15, 0.35), (0.0, -0.05, 0.35), (0.0, -0.05, 0.05),
                                         (0.0, -0.35, 0.05), (0.0, -0.35, 0.15), (0.0, -0.5, 0.0), (0.0, -0.35, -0.15),
                                         (0.0, -0.35, -0.05), (0.0, -0.05, -0.05), (0.0, -0.05, -0.35),
                                         (0.0, -0.15, -0.35), (0.0, 0.0, -0.5), (0.0, 0.15, -0.35), (0.0, 0.05, -0.35),
                                         (0.0, 0.05, -0.05), (0.0, 0.35, -0.05), (0.0, 0.35, -0.15), (0.0, 0.5, 0.0),
                                         (0.0, 0.35, 0.15), (0.0, 0.35, 0.05), (0.0, 0.05, 0.05), (0.0, 0.05, 0.35),
                                         (0.0, 0.15, 0.35), (0, 0, 0.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.0, 0.0, 0.5), (0.0, -0.15, 0.35), (0.0, -0.05, 0.35), (0.0, -0.05, 0.05),
                                       (0.0, -0.35, 0.05), (0.0, -0.35, 0.15), (0.0, -0.5, 0.0), (0.0, -0.35, -0.15),
                                       (0.0, -0.35, -0.05), (0.0, -0.05, -0.05), (0.0, -0.05, -0.35),
                                       (0.0, -0.15, -0.35), (0.0, 0.0, -0.5), (0.0, 0.15, -0.35), (0.0, 0.05, -0.35),
                                       (0.0, 0.05, -0.05), (0.0, 0.35, -0.05), (0.0, 0.35, -0.15), (0.0, 0.5, 0.0),
                                       (0.0, 0.35, 0.15), (0.0, 0.35, 0.05), (0.0, 0.05, 0.05), (0.0, 0.05, 0.35),
                                       (0.0, 0.15, 0.35), (0, 0, 0.5)])


# Dt_Cl_09()
def Dt_Cl_09():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0, 0, 0), (0, 0.6, -0.15), (0, 0.6, 0.15), (0, 0, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0, 0, 0), (0, 0.6, -0.15), (0, 0.6, 0.15), (0, 0, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0, 0, 0), (0, 0.6, -0.15), (0, 0.6, 0.15), (0, 0, 0)])


# Dt_Cl_10()
def Dt_Cl_10():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(-.5, .5, 0), (.5, 0, 0), (-.5, -.5, 0), (-.5, .5, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(-.5, .5, 0), (.5, 0, 0), (-.5, -.5, 0), (-.5, .5, 0)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(-.5, .5, 0), (.5, 0, 0), (-.5, -.5, 0), (-.5, .5, 0)])


# Dt_Cl_11()
def Dt_Cl_11():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0, -.5, .5), (0, -.5, -.5), (0, .5, -.5), (0, .5, .5), (0, -.5, .5)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0, -.5, .5), (0, -.5, -.5), (0, .5, -.5), (0, .5, .5), (0, -.5, .5)])
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0, -.5, .5), (0, -.5, -.5), (0, .5, -.5), (0, .5, .5), (0, -.5, .5)])


# Dt_Cl_12()
def Dt_Cl_12():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.circle(n="curve", c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1)
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.circle(n="curve", c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1)
            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.circle(n="curve", c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1)


# Dt_Cl_13()
def Dt_Cl_13():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1,
                                 p=[(0.075, -0.075, 0.0), (0.298, -0.075, 0.0), (0.3, 0.075, 0.0), (0.075, 0.075, 0.0),
                                    (0.075, 0.3, 0.0), (-0.075, 0.3, 0.0), (-0.075, 0.075, 0.0), (-0.3, 0.075, 0.0),
                                    (-0.3, -0.075, 0.0), (-0.075, -0.075, 0.0), (-0.075, -0.3, 0.0), (0.075, -0.3, 0.0),
                                    (0.075, -0.075, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1,
                                 p=[(0.075, -0.075, 0.0), (0.298, -0.075, 0.0), (0.3, 0.075, 0.0), (0.075, 0.075, 0.0),
                                    (0.075, 0.3, 0.0), (-0.075, 0.3, 0.0), (-0.075, 0.075, 0.0), (-0.3, 0.075, 0.0),
                                    (-0.3, -0.075, 0.0), (-0.075, -0.075, 0.0), (-0.075, -0.3, 0.0), (0.075, -0.3, 0.0),
                                    (0.075, -0.075, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1,
                               p=[(0.075, -0.075, 0.0), (0.298, -0.075, 0.0), (0.3, 0.075, 0.0), (0.075, 0.075, 0.0),
                                  (0.075, 0.3, 0.0), (-0.075, 0.3, 0.0), (-0.075, 0.075, 0.0), (-0.3, 0.075, 0.0),
                                  (-0.3, -0.075, 0.0), (-0.075, -0.075, 0.0), (-0.075, -0.3, 0.0), (0.075, -0.3, 0.0),
                                  (0.075, -0.075, 0.0)])


# Dt_Cl_14()
def Dt_Cl_14():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1,
                                 p=[(0, .5, 0), (0, -.5, 0), (0, 0, 0), (-.5, 0, 0), (.5, 0, 0), (0, 0, 0), (0, 0, .5),
                                    (0, 0, -.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1,
                                 p=[(0, .5, 0), (0, -.5, 0), (0, 0, 0), (-.5, 0, 0), (.5, 0, 0), (0, 0, 0), (0, 0, .5),
                                    (0, 0, -.5)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1,
                               p=[(0, .5, 0), (0, -.5, 0), (0, 0, 0), (-.5, 0, 0), (.5, 0, 0), (0, 0, 0), (0, 0, .5),
                                  (0, 0, -.5)])


# Dt_Cl_15()
def Dt_Cl_15():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.654, 0.0), (0.0, 0.756, -0.103), (0.0, 0.859, 0.0),
                                         (0.0, 0.756, 0.103), (0.0, 0.654, 0.0), (0.0, 0.859, 0.0),
                                         (0.0, 0.756, -0.103), (0.0, 0.756, 0.103)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.654, 0.0), (0.0, 0.756, -0.103), (0.0, 0.859, 0.0),
                                         (0.0, 0.756, 0.103), (0.0, 0.654, 0.0), (0.0, 0.859, 0.0),
                                         (0.0, 0.756, -0.103), (0.0, 0.756, 0.103)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.654, 0.0), (0.0, 0.756, -0.103), (0.0, 0.859, 0.0),
                                       (0.0, 0.756, 0.103), (0.0, 0.654, 0.0), (0.0, 0.859, 0.0), (0.0, 0.756, -0.103),
                                       (0.0, 0.756, 0.103)])


# Dt_Cl_16()
def Dt_Cl_16():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.669, 0.0), (0.0, 0.669, -0.118), (0.0, 0.846, 0.0),
                                         (0.0, 0.669, 0.118), (0.0, 0.669, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)

            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.669, 0.0), (0.0, 0.669, -0.118), (0.0, 0.846, 0.0),
                                         (0.0, 0.669, 0.118), (0.0, 0.669, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=1, p=[(0.0, 0.0, 0.0), (0.0, 0.669, 0.0), (0.0, 0.669, -0.118), (0.0, 0.846, 0.0),
                                       (0.0, 0.669, 0.118), (0.0, 0.669, 0.0)])


# Dt_Cl_17()
def Dt_Cl_17():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=3, p=[(0.0, 0.0, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0),
                                         (0.0, 0.661, -0.02), (0.0, 0.683, -0.081), (0.0, 0.768, -0.107),
                                         (0.0, 0.834, -0.076), (0.0, 0.866, 0.0), (0.0, 0.834, 0.077),
                                         (0.0, 0.757, 0.108), (0.0, 0.682, 0.075), (0.0, 0.661, 0.019),
                                         (0.0, 0.66, 0.0), (0.0, 0.66, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)

            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=3, p=[(0.0, 0.0, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0),
                                         (0.0, 0.661, -0.02), (0.0, 0.683, -0.081), (0.0, 0.768, -0.107),
                                         (0.0, 0.834, -0.076), (0.0, 0.866, 0.0), (0.0, 0.834, 0.077),
                                         (0.0, 0.757, 0.108), (0.0, 0.682, 0.075), (0.0, 0.661, 0.019),
                                         (0.0, 0.66, 0.0), (0.0, 0.66, 0.0)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=3, p=[(0.0, 0.0, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0), (0.0, 0.66, 0.0),
                                       (0.0, 0.661, -0.02), (0.0, 0.683, -0.081), (0.0, 0.768, -0.107),
                                       (0.0, 0.834, -0.076), (0.0, 0.866, 0.0), (0.0, 0.834, 0.077),
                                       (0.0, 0.757, 0.108), (0.0, 0.682, 0.075), (0.0, 0.661, 0.019), (0.0, 0.66, 0.0),
                                       (0.0, 0.66, 0.0)])


# Dt_Cl_18()
def Dt_Cl_18():
    list_sel = pm.ls(sl=1)
    radio = pm.radioCollection('typeOpRC', query=True, select=True)
    if radio == "Replace":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            pm.delete(delShape)
            newName = pm.curve(d=3, p=[(0, 0.055, -0.495), (-0.11, 0.055, -0.495), (-0.37796, 0.055, -0.411902),
                                         (-0.55, 0.055, 0), (-0.388909, 0.055, 0.388909), (0, 0.055, 0.55),
                                         (0.388909, 0.055, 0.388909), (0.55, 0.055, 0), (0.39325, 0.055, -0.3575),
                                         (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                         (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                         (0.189373, 0.11, -0.459162), (0.189373, 0.11, -0.459162),
                                         (0.189373, 0.11, -0.459162), (0, 0, -0.495), (0, 0, -0.495), (0, 0, -0.495),
                                         (0.189373, -0.11, -0.459162), (0.189373, -0.11, -0.459162),
                                         (0.189373, -0.11, -0.459162), (0.189373, -0.055, -0.459162),
                                         (0.189373, -0.055, -0.459162), (0.189373, -0.055, -0.459162),
                                         (0.393078, -0.055, -0.358684), (0.55, -0.055, 0), (0.388909, -0.055, 0.388909),
                                         (0, -0.055, 0.55), (-0.388909, -0.055, 0.388909), (-0.55, -0.055, 0),
                                         (-0.385624, -0.055, -0.382339), (-0.11, -0.055, -0.495), (0, -0.055, -0.495),
                                         (0, -0.055, -0.495), (0, -0.055, -0.495), (0, 0.055, -0.495)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)

            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)


    elif radio == "Add":
        for i in list_sel:
            delShape = pm.listRelatives(i, s=1, f=1)
            newName = pm.curve(d=3, p=[(0, 0.055, -0.495), (-0.11, 0.055, -0.495), (-0.37796, 0.055, -0.411902),
                                         (-0.55, 0.055, 0), (-0.388909, 0.055, 0.388909), (0, 0.055, 0.55),
                                         (0.388909, 0.055, 0.388909), (0.55, 0.055, 0), (0.39325, 0.055, -0.3575),
                                         (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                         (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                         (0.189373, 0.11, -0.459162), (0.189373, 0.11, -0.459162),
                                         (0.189373, 0.11, -0.459162), (0, 0, -0.495), (0, 0, -0.495), (0, 0, -0.495),
                                         (0.189373, -0.11, -0.459162), (0.189373, -0.11, -0.459162),
                                         (0.189373, -0.11, -0.459162), (0.189373, -0.055, -0.459162),
                                         (0.189373, -0.055, -0.459162), (0.189373, -0.055, -0.459162),
                                         (0.393078, -0.055, -0.358684), (0.55, -0.055, 0), (0.388909, -0.055, 0.388909),
                                         (0, -0.055, 0.55), (-0.388909, -0.055, 0.388909), (-0.55, -0.055, 0),
                                         (-0.385624, -0.055, -0.382339), (-0.11, -0.055, -0.495), (0, -0.055, -0.495),
                                         (0, -0.055, -0.495), (0, -0.055, -0.495), (0, 0.055, -0.495)])

            tmpPos = pm.xform(i, q=1, ws=1, t=1)
            tmpPos = [round(tmpPos[0], 3), round(tmpPos[1], 3), round(tmpPos[2], 3)]
            if (tmpPos == [0, 0, 0]):
                pm.parentConstraint(i, newName, n='tmp_shape_con')
                pm.delete('tmp_shape_con')
            pm.makeIdentity(apply=1, t=1, r=1, s=1)
            tmpShape = pm.listRelatives(newName, s=1, f=1)
            tmpName = pm.rename(tmpShape[0], i + 'Shape')
            pm.parent(tmpName, i, add=1, s=1)
            pm.delete(newName)
        pm.select(list_sel)

    elif radio == "Create":
        new_curve = pm.curve(d=3, p=[(0, 0.055, -0.495), (-0.11, 0.055, -0.495), (-0.37796, 0.055, -0.411902),
                                       (-0.55, 0.055, 0), (-0.388909, 0.055, 0.388909), (0, 0.055, 0.55),
                                       (0.388909, 0.055, 0.388909), (0.55, 0.055, 0), (0.39325, 0.055, -0.3575),
                                       (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                       (0.189373, 0.055, -0.459162), (0.189373, 0.055, -0.459162),
                                       (0.189373, 0.11, -0.459162), (0.189373, 0.11, -0.459162),
                                       (0.189373, 0.11, -0.459162), (0, 0, -0.495), (0, 0, -0.495), (0, 0, -0.495),
                                       (0.189373, -0.11, -0.459162), (0.189373, -0.11, -0.459162),
                                       (0.189373, -0.11, -0.459162), (0.189373, -0.055, -0.459162),
                                       (0.189373, -0.055, -0.459162), (0.189373, -0.055, -0.459162),
                                       (0.393078, -0.055, -0.358684), (0.55, -0.055, 0), (0.388909, -0.055, 0.388909),
                                       (0, -0.055, 0.55), (-0.388909, -0.055, 0.388909), (-0.55, -0.055, 0),
                                       (-0.385624, -0.055, -0.382339), (-0.11, -0.055, -0.495), (0, -0.055, -0.495),
                                       (0, -0.055, -0.495), (0, -0.055, -0.495), (0, 0.055, -0.495)])


def dt_chgScaCVSMaxMinProc(typ):
    if (typ == 1):
        ma = pm.floatField('rtrsScaleMaxCVFS', q=1, v=1)
        pm.floatSlider('rtrsScaleCVFS', e=1, en=0, max=ma)
        pm.floatSlider('rtrsScaleCVFS', e=1, en=1)
    if (typ == 2):
        mi = pm.floatField('rtrsScaleMinCVFS', q=1, v=1)
        pm.floatSlider('rtrsScaleCVFS', e=1, min=mi)


def dt_changeScaleCVSliderProc():
    sel = pm.ls(sl=1, fl=1)
    if (len(sel) == 0):
        pm.floatSlider('rtrsScaleCVFS', e=1, v=0)
        return
    sV = pm.floatSlider('rtrsScaleCVFS', q=1, v=1)
    if (sV > 0):
        sV = sV + 1
    if (sV < 0):
        sV = 1 - abs(sV) / 2
    for i in sel:
        pm.select(i)
        if (len(i.split('.')) != 1):
            pm.scale(sV, sV, sV, r=1)
        else:
            pm.scale(sV, sV, sV, i + '.cv[*]', r=1)
    pm.select(sel)
    pm.floatSlider('rtrsScaleCVFS', e=1, v=0)


def dt_selectAllCurveCVProc():
    sel = pm.ls(sl=1)
    pm.select(cl=1)
    for i in sel:
        pm.select(i + '.cv[*]', add=1)


def kframe(integer):
    sel = pm.selected()[0]
    xyz = ['rotateX', 'rotateY', 'rotateZ']

    radio_a = pm.radioCollection('rotate', query = True, select = True)

    radio_b = pm.radioCollection('PosNeg', query = True, select = True)
    if radio_a == 'pass':
        if pm.getAttr('%s.rotateX' % sel) == 0 and pm.getAttr('%s.rotateY' % sel) == 0 and pm.getAttr(
                '%s.rotateZ' % sel) == 0:

            pm.warning(u'如果旋转XYZ为零，请选择轴向和正负')
        else:
            for rt in xyz:
                if pm.getAttr('%s.%s' % (sel, rt)) > 0:
                    deframe()
                    pm.setKeyframe(v = 0, time = 0, at = rt, itt = 'linear', ott = 'linear')
                    pm.setKeyframe(v = integer, time = integer, at = rt, itt = 'linear', ott = 'linear')
                    pm.playbackOptions(min = 0, max = integer)
                elif pm.getAttr('%s.%s' % (sel, rt)) < 0:
                    deframe()
                    pm.setKeyframe(v = 0, time = 0, at = rt, itt = 'linear', ott = 'linear')
                    pm.setKeyframe(v = integer * -1, time = integer * 1, at = rt, itt = 'linear', ott = 'linear')
                    pm.playbackOptions(min = 0, max = integer)


    else :
        if radio_b == 'positive':
            deframe()
            pm.setKeyframe(v = 0, time = 0, at = radio_a, itt = 'linear', ott = 'linear')
            pm.setKeyframe(v = integer, time = integer, at = radio_a, itt = 'linear', ott = 'linear')
            pm.playbackOptions(min = 0, max = integer)
        elif radio_b == 'negative':
            deframe()
            pm.setKeyframe(v = 0, time = 0, at = radio_a, itt = 'linear', ott = 'linear')
            pm.setKeyframe(v = integer * -1, time = integer * 1, at = radio_a, itt = 'linear', ott = 'linear')
            pm.playbackOptions(min = 0, max = integer)
        elif radio_b == 'PosandNeg':
            deframe()
            pm.setKeyframe(v = integer * -1, time = integer * -1, at = radio_a, itt = 'linear', ott = 'linear')
            pm.setKeyframe(v = 0, time = 0, at = radio_a, itt = 'linear', ott = 'linear')
            pm.setKeyframe(v = integer, time = integer, at = radio_a, itt = 'linear', ott = 'linear')
            pm.playbackOptions(min = integer * -1, max = integer)

# 删除K帧并归零
def deframe():
    # sel = pm.selected()
    pm.currentTime(0)
    pm.cutKey(time = (-200, 200), clear = True)
    pm.playbackOptions(min = 0, max = 120)

# 创建斜方向控制器
def oblique():
    ctl = pm.selected()[0]
    loc = pm.spaceLocator(n = ctl + '_Locator')
    loc_1x_grp = pm.group(loc, n = loc + '_1x_Grp')
    loc_grp = pm.group(loc_1x_grp, n = loc + '_Grp')

    pm.setAttr(loc + 'Shape.localScaleX', 16)
    pm.setAttr(loc + 'Shape.localScaleY', 16)
    pm.setAttr(loc + 'Shape.localScaleZ', 16)

    pm.delete(pm.parentConstraint(ctl, loc_grp, w = 1))
    pm.setAttr(loc_1x_grp + '.rotateX', 45)
    pm.orientConstraint(loc, ctl, mo = 1, w = 1)

    pm.select(loc)

gui()