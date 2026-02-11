#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2026/1/29 17:17
# @Author : yinyufei
# @File : test.py
# @Project : TeamCode


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import maya.cmds as cmds

# 导入本地blendshape模块
from cgrig.libs.maya.cmds.rig import blendshape

# 全局变量
__version__ = 'v 3.1.0  date:2026/01/29'


class BlendShapeManager:
    """BlendShape管理类"""

    def __init__(self):
        """初始化BlendShape管理器"""
        self.window_name = "blendShapeManage"

    def get_mesh(self):
        """获取当前选中的网格对象

        Returns:
            str: 选中的网格对象名称，或提示信息
        """
        sel = cmds.ls(sl=1)
        ret = 'Please Loading Mesh.'
        mesh = []

        for i in sel:
            if cmds.nodeType(i) == 'transform':
                mesh = i

        if mesh:
            base_relatives = cmds.listRelatives(mesh, f=1)
            if base_relatives:
                base_rel = base_relatives[0]
                if cmds.nodeType(base_rel) == 'mesh':
                    ret = mesh
                else:
                    ret = 'Please Loading Mesh.'

        return ret

    def mesh_exists(self, mesh):
        """检查网格对象是否存在且有效

        Args:
            mesh (str): 网格对象名称

        Returns:
            bool: 网格是否有效
        """
        try:
            list_mesh = cmds.listRelatives(mesh, s=True, f=1)
            if list_mesh and cmds.nodeType(list_mesh[0]) == 'mesh':
                return True
        except Exception as e:
            print("检查网格时出错: {0}".format(e))

        return False

    def get_blend_shape_node(self, mesh_node):
        """获取对象上的blendShape节点

        Args:
            mesh_node (str): 网格对象名称

        Returns:
            str: blendShape节点名称，或空字符串
        """
        try:
            blend_shape_nodes = blendshape.getBlendshapeNodes(mesh_node)
            if blend_shape_nodes:
                return blend_shape_nodes[0]
        except Exception as e:
            print("获取blendShape节点时出错: {0}".format(e))

        return ''

    def blend_shape_node_on_off(self):
        """检查blendShape节点是否存在且有效

        Returns:
            int: 1表示存在有效节点，0表示不存在
        """
        nua = 0
        if cmds.textFieldGrp('meshShapeText', ex=1) == 1:
            obj = cmds.textFieldGrp('meshShapeText', query=True, text=True)
            if self.mesh_exists(obj):
                bsnodes = blendshape.getBlendshapeNodes(obj)
                if bsnodes:
                    nua = 1
        return nua

    def get_target_blend_shape_text(self):
        """获取当前选中的目标文本

        Returns:
            str: 选中的目标名称，或'None'
        """
        target_blend_shape_text = cmds.textScrollList('targetBlendShapeText', query=True, selectItem=True)
        if target_blend_shape_text is None:
            target_blend_shape = 'None'
        else:
            target_blend_shape = target_blend_shape_text[0].split('[')
        return target_blend_shape[0]

    def get_mirror_target_name(self, target_name):
        """获取目标的镜像名称

        Args:
            target_name (str): 原始目标名称

        Returns:
            str: 镜像目标名称
        """
        # 左右前缀映射
        prefix_mappings = {
            'L_': 'R_',
            'R_': 'L_',
            'lf_': 'rt_',
            'rt_': 'lf_',
            'l_': 'r_',
            'r_': 'l_'
        }

        # 左右后缀映射
        suffix_mappings = {
            '_l': '_r',
            '_r': '_l',
            '_L': '_R',
            '_R': '_L'
        }

        # 中间部分映射
        middle_mappings = {
            '_L_': '_R_',
            '_R_': '_L_',
            '_lf_': '_rt_',
            '_rt_': '_lf_'
        }

        # 检查前缀
        for prefix, mirror_prefix in prefix_mappings.items():
            if target_name.startswith(prefix):
                return mirror_prefix + target_name[len(prefix):]

        # 检查后缀
        for suffix, mirror_suffix in suffix_mappings.items():
            if target_name.endswith(suffix):
                return target_name[:-len(suffix)] + mirror_suffix

        # 检查中间部分
        for middle, mirror_middle in middle_mappings.items():
            if middle in target_name:
                return target_name.replace(middle, mirror_middle)

        return ''

    def create_ui(self):
        """创建主UI窗口"""
        # 检查窗口是否存在
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)

        # 创建窗口
        cmds.window(
            self.window_name,
            mb=True,
            t='BlendShapeManage_' + __version__
        )

        # 创建菜单栏
        self._create_menu_bar()

        # 创建主布局
        cmds.columnLayout('')

        # 创建工具栏
        self._create_toolbar()

        # 创建表格区域
        self._create_table_area()

        # 显示窗口
        cmds.showWindow(self.window_name)
        cmds.window(self.window_name, edit=True, w=450, h=600)

    def _create_menu_bar(self):
        """创建菜单栏"""
        # 创建编辑菜单
        edit_menu = cmds.menu(l='Edit', parent=self.window_name)
        cmds.menuItem(l='Append', c='blendShapeManager.append_target()')
        cmds.menuItem(l='Delete', c='blendShapeManager.remove_target()')
        cmds.menuItem(l='Gain', c='blendShapeManager.gain_target()')
        cmds.menuItem(l='Rename', c='blendShapeManager.rename_target()')
        cmds.menuItem(l='RevertTarget', c='blendShapeManager.revert_target()')
        cmds.setParent('..')

        # 创建帮助菜单
        help_menu = cmds.menu(l='Help', parent=self.window_name)
        cmds.menuItem(d=True, parent=help_menu)
        cmds.menuItem(label='Close', c="cmds.window('%s',e=True,vis=0)" % self.window_name, parent=help_menu)
        cmds.menuItem(label=__version__, parent=help_menu)
        cmds.setParent('..')

    def _create_toolbar(self):
        """创建工具栏"""
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 60), (2, 380)])
        cmds.button('buttonBlendShapeMesh', label='Reload\nModel',
                    c='blendShapeManager.reload_mesh(blendShapeManager.get_mesh())')
        cmds.textFieldGrp('meshShapeText', text='Please Loading Mesh.', ed=False, cw1=375)
        cmds.text(l='INPUT')
        cmds.text('blendShapeText',
                  label='',
                  align='left')
        cmds.setParent('..')

    def _create_table_area(self):
        """创建表格区域"""
        form_main = cmds.formLayout()
        tabs = cmds.tabLayout(
            'tabs',
            innerMarginWidth=5,
            innerMarginHeight=5
        )

        cmds.formLayout(
            form_main,
            edit=True,
            attachForm=(
                (tabs, 'top', 0),
                (tabs, 'left', 0),
                (tabs, 'bottom', 0),
                (tabs, 'right', 0)
            )
        )

        # 创建编辑选项卡
        cmds.columnLayout('child1')
        self._create_edit_ui()
        cmds.setParent('..')

        # 创建克隆选项卡
        cmds.columnLayout('child2', en=1)
        self._create_clone_ui()
        cmds.setParent('..')

        # 设置选项卡属性
        cmds.tabLayout(
            tabs,
            sc='blendShapeManager.refresh_target_list("append")',
            edit=True,
            tabLabel=(('child1', 'Edit'), ('child2', 'Clone')),
            st='child2'
        )
        cmds.setParent('..')

    def _create_edit_ui(self):
        """创建编辑选项卡UI"""
        cmds.columnLayout(adj=True)
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 300), (2, 23), (3, 100)])
        cmds.text('availableText', l='Available blendShape target: ', font='boldLabelFont')
        cmds.text(l='')
        cmds.text('InbetweenText', l='Inbetween weight:')
        cmds.columnLayout()
        cmds.popupMenu(mm=True)
        cmds.menuItem(l='Append', rp='N')
        cmds.menuItem(l='Delete', rp='S', c='blendShapeManager.remove_target()')
        cmds.menuItem(l='Gain', rp='W', c='blendShapeManager.gain_target()')
        cmds.menuItem(l='Rename', rp='E', c='blendShapeManager.rename_target()')
        cmds.textScrollList('targetBlendShapeText', height=200, width=295,
                            sc='blendShapeManager.update_inbetween_weight(),blendShapeManager.update_target_info()')
        cmds.setParent('..')
        cmds.text(l=' => ')
        cmds.columnLayout(adj=1)
        cmds.textScrollList('targetInbetweenText', allowMultiSelection=True, height=155, width=95,
                            sc='blendShapeManager.set_blend_shape()')
        cmds.floatField('InbetweenField', w=100, en=False)
        cmds.button(l=' inputGeomTarget ', c='blendShapeManager.input_geom_target()', en=0)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.text(l='', h=5)
        cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 215), (2, 215)])
        cmds.button('EditFinsihButton', label='Edit', c='blendShapeManager.edit_finish_button()', en=0)
        cmds.button(label='Cancel', en=0)
        cmds.setParent('..')
        cmds.setParent('..')

        # In-between 框架
        cmds.columnLayout()
        cmds.frameLayout(w=435, label='In-between', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2,
                         collapse=True, en=0)
        cmds.columnLayout(adj=1)
        cmds.checkBoxGrp('Inbetween', label='Add in-between target:', columnWidth=(1, 160),
                         of1='blendShapeManager.inbetween_box()', on1='blendShapeManager.inbetween_box()')
        cmds.floatSliderGrp('InbetweenSlider', label='In-between weight:', field=True, min=-10.0, max=10.0, pre=2,
                            enable=False, adj=3, en=0, cw3=(140, 80, 200))
        cmds.button('EditAddbetweenButton', label='inbetweenEdit', c='blendShapeManager.inbetween_edit_add_button()',
                    width=50, enable=False)
        cmds.setParent('..')
        cmds.setParent('..')

        # MirrorShape 框架
        cmds.frameLayout(w=435, label='MirrorShape', collapsable=True, labelAlign='top', marginHeight=2, marginWidth=2,
                         collapse=True)
        cmds.columnLayout()
        cmds.radioButtonGrp('MirrorAxis', numberOfRadioButtons=3, l='Mirror Axis : ', labelArray3=('X', 'Y', 'Z'), sl=1,
                            cw4=(85, 30, 30, 30), ct4=('left', 'left', 'left', 'left'))
        cmds.rowColumnLayout(numberOfColumns=2, cw=[(1, 300), (2, 120)])
        cmds.radioButtonGrp('Position_of_MirrorsShapes', numberOfRadioButtons=2, l='Position of mirrors Shapes : ',
                            labelArray2=('Shape', 'Original'), sl=2, cw3=(140, 80, 80), ct3=('left', 'left', 'left'))
        cmds.checkBox('DeleteMirrorObjBox', l='Delete Mirror Object', v=1)
        cmds.setParent('..')
        shape_offset = cmds.floatFieldGrp('DuplicationOffset', label='==> Duplication Offset (shape mode) : ',
                                          numberOfFields=3, cw4=(200, 60, 60, 60), en=0)
        cmds.radioButtonGrp('Position_of_MirrorsShapes', e=1,
                            cc="blendShapeManager.put_offset_in_gray('" + shape_offset + "','Position_of_MirrorsShapes')")
        cmds.textFieldButtonGrp('Target_Text', label='Target : ', cw3=(100, 250, 120), bl=' <<<< ', en=0)
        cmds.textFieldButtonGrp('MirrorTargetText', label='Shape(s) to Copy : ', cw3=(100, 250, 120), bl=' Mirror ',
                                bc='blendShapeManager.mirror_blend_shape(0)')
        cmds.setParent('..')
        cmds.setParent('..')

        # # Mirror>Target 框架
        # cmds.frameLayout(w=435, label='Mirror>Target', collapsable=True, labelAlign='top', marginHeight=2,
        #                  marginWidth=2, collapse=True)
        # cmds.columnLayout()
        # cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 45), (2, 180), (3, 40), (4, 180)])
        # cmds.checkBox('autoMirrorTargetNameCB', l='Auto', v=1)
        # cmds.textField('targetField', tx='Target', en=0)
        # cmds.text(l=' =>>= ')
        # cmds.textField('sourceField', tx='Source', en=0)
        # cmds.text(l='')
        # cmds.button(l='Target', c='blendShapeManager.edit_field("targetField")')
        # cmds.text(l='')
        # cmds.button(l='Source', c='blendShapeManager.edit_field("sourceField")')
        # cmds.setParent('..')
        # cmds.button(l='Apply', w=435, c='blendShapeManager.mirror_blend_shape(1)')
        # cmds.setParent('..')
        # cmds.setParent('..')

        # Rebuild Target Items 框架
        cmds.frameLayout(w=435, label='Rebuild Target Items', collapsable=True, labelAlign='top', marginHeight=2,
                         marginWidth=2, collapse=True)
        cmds.columnLayout()
        cmds.text(l='运行前请确保除blendShape以外的变形器没有对模型造成变形效果')
        cmds.button(l='Rebuild Target Items', w=420, h=40,
                    c="blendShapeManager.rebuild_target_items(cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True),'yes'),blendShapeManager.reload_mesh(cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True))")
        cmds.setParent('..')
        cmds.setParent('..')

        # target重新排序 框架
        cmds.frameLayout(w=435, label='target重新排序', collapsable=True, labelAlign='top', marginHeight=2,
                         marginWidth=2, collapse=True)
        cmds.columnLayout('rearrangeTarget_CL')
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.textField('Target_strsTF',
                       tx="['neck','head'\n,'L_shoulder','L_Tpose','L_arm'\n,'R_shoulder','R_Tpose','R_arm'\n,'L_elbow','L_hand'\n,'R_elbow','R_hand'\n,'finger'\n,'L_Leg','L_knee','L_foot','L_toe'\n,'R_Leg','R_knee','R_foot','R_toe','leg']",
                       en=1, w=300, h=40)
        cmds.button(l='根据关键字排列target列表', h=40,
                    c="blendShapeManager.rearrange_target_list(   cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True)   ,eval(cmds.textField('Target_strsTF',query=True,tx=True))   )")
        cmds.textField('rearrangeTargetTF', tx='', en=1, w=300, h=40)
        cmds.button(l='根据列表顺序重建target', h=40,
                    c="blendShapeManager.rearrange_target(   cmds.textFieldButtonGrp('TargetGoemerty',query=True,tx=True)   ,'yes'   ,eval(cmds.textField('rearrangeTargetTF',q = True,tx = True))  )")
        cmds.setParent('rearrangeTarget_CL')
        cmds.setParent('..')
        cmds.setParent('..')

        # target批量镜像 框架
        cmds.frameLayout(w=435, label='target批量镜像', collapsable=True, labelAlign='top', marginHeight=2,
                         marginWidth=2, collapse=True)
        cmds.columnLayout('targetMirror_CL')
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.textField('Target_mirrorStrTF',
                       tx='L_*=R_*,lf_*=rt_*,l_*=r_*,left_*=right_*,*_L=*_R,*_lf=*_rt,*_l=*_r,*_left=*_right,*_L_*=*_R_*,*_l_*=*_r_*,*_lf_*=*_rt_*,*_left_*=*_right_*',
                       en=1, w=300, h=40)
        cmds.button(l='根据关键字整理对称的target列表', h=40,
                    c="blendShapeManager.target_mirror_list( cmds.textField('Target_mirrorStrTF',q = True,tx = True)  )")
        cmds.setParent('targetMirror_CL')
        cmds.textField('L_TargetList_TF', tx='', w=300, h=40)
        cmds.textField('R_TargetList_TF', tx='', w=300, h=40)
        cmds.button(l='批量镜像target', w=300, h=40,
                    c="blendShapeManager.mirror_blend_shape_list(1,  eval(cmds.textField('L_TargetList_TF',q = True,tx = True))  ,  eval(cmds.textField('R_TargetList_TF',q = True,tx = True))  )")
        cmds.setParent('targetMirror_CL')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

    def _create_clone_ui(self):
        """创建克隆选项卡UI"""
        cmds.columnLayout('', adj=True)
        cmds.textFieldButtonGrp('TargetGoemerty', label='Target Goemerty:', tx=self.get_mesh(), cw3=(100, 280, 200),
                                bl='Reload', bc='', ed=False, eb=False)
        cmds.textFieldButtonGrp('SourceGoemerty', label='Source Goemerty:', cw3=(100, 280, 200), bl='Reload')
        cmds.textFieldButtonGrp('SourceGoemerty', e=True, bc='blendShapeManager.load_text("SourceGoemerty")')
        cmds.button(label='Apply', c='blendShapeManager.creative_target_clone()')
        cmds.button('cloneButton', l='Clone Target List', c='blendShapeManager.edit_clone_button()')
        cmds.frameLayout('cloneFrame', label='Clone List', mw=5, mh=5, la='center', cll=1, cl=1)
        cmds.textFieldButtonGrp('selTarget_TF_but', label='Select Target:', cw3=(100, 280, 200), bl='select')
        cmds.textFieldButtonGrp('selTarget_TF_but', e=True, bc='blendShapeManager.select_by_keyword()')
        cmds.rowColumnLayout(numberOfColumns=5)
        cmds.button(label='shoulder', c='blendShapeManager.select_target_by_keyword(["shoulder"])')
        cmds.button(label='arm', c='blendShapeManager.select_target_by_keyword(["arm"])')
        cmds.button(label='elbow', c='blendShapeManager.select_target_by_keyword(["elbow"])')
        cmds.button(label='wrist , hand', c='blendShapeManager.select_target_by_keyword(["wrist","hand"])')
        cmds.button(label='finger',
                    c='blendShapeManager.select_target_by_keyword(["finger","middle","index","ring","pinky","thumb"])')
        cmds.button(label='leg', c='blendShapeManager.select_target_by_keyword(["leg"])')
        cmds.button(label='knee', c='blendShapeManager.select_target_by_keyword(["knee"])')
        cmds.button(label='ankle', c='blendShapeManager.select_target_by_keyword(["ankle"])')
        cmds.button(label='toe', c='blendShapeManager.select_target_by_keyword(["toe"])')
        cmds.button(label='neck , head', c='blendShapeManager.select_target_by_keyword(["neck","head"])')
        cmds.setParent('..')
        cmds.scrollLayout('cloneList', horizontalScrollBarThickness=16, verticalScrollBarThickness=16, h=285)
        cmds.rowColumnLayout('clone_rclayout', numberOfColumns=2)
        cmds.setParent('cloneFrame')
        cmds.text(
            l='红色无连接且数值大于0，黄色无连接且数值为0\n蓝色有连接但数值大于0，灰色有连接数值为0\n没有勾选的Target会保持当前数值,包裹时不操作数值'
        )
        cmds.rowColumnLayout(numberOfColumns=2)
        cmds.checkBox(
            'delTargetCB',
            l='删除目标体',
            ann='克隆完成后自动删除目标体',
            v=1
        )
        cmds.setParent('cloneFrame')
        cmds.button(
            'cloneSelInvertBut',
            l='反选',
            c='blendShapeManager.clone_sel_invert()'
        )
        cmds.setParent('..')

    def refresh_target_list(self, mode='append', fresh=None):
        """刷新目标列表

        Args:
            mode (str): 刷新模式 ('append' 或 'remove')
            fresh (str): 要选中的目标名称
        """
        target_name = self.get_target_blend_shape_text()

        if mode == 'append':
            if self.blend_shape_node_on_off():
                blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
                target_blend_shape = blendshape.getTargetList(blend_shape_field)
                cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=True)
                target_int = cmds.blendShape(blend_shape_field, query=True, wc=True)

                if target_int > 0:
                    for t in target_blend_shape:
                        cmds.textScrollList('targetBlendShapeText', edit=True, append=t)

                if cmds.tabLayout('tabs', q=1, sti=1) == 3:
                    if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
                        self.clone_list_off()
                        self.clone_list_on()
            else:
                cmds.textScrollList('targetBlendShapeText', edit=True, removeAll=1)

        if mode == 'remove':
            cmds.textScrollList('targetBlendShapeText', edit=True, ri=target_name)

        if fresh is not None:
            cmds.textScrollList('targetBlendShapeText', si=fresh, e=1)

        if self.blend_shape_node_on_off():
            blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            target_blend_shape = cmds.listAttr(blend_shape_field + '.weight', multi=True)
            if target_blend_shape is None:
                cmds.text('availableText', edit=True, l='No BlendShape target', bgc=[0.8, 0, 0])
            else:
                target_items = cmds.textScrollList('targetBlendShapeText', query=True, ni=True)
                try:
                    target_neg1_num = blendshape.getTargetIndex(blend_shape_field, target_blend_shape[-1])
                    if target_items - 1 == target_neg1_num:
                        target_num_hint = '序号正确'
                        bgc = [0, 0.4, 0]
                    else:
                        target_num_hint = '序号错误\n序号是从 0 开始的，最高序号比target数量少1才对'
                        bgc = [0.8, 0.8, 0]
                    cmds.text('availableText', edit=True, bgc=bgc,
                              l='target数量:' + str(target_items) + '--最高序号:' + str(
                                  target_neg1_num) + '--' + target_num_hint)
                except Exception as e:
                    print("更新目标列表时出错: {0}".format(e))
        else:
            cmds.text('availableText', edit=True, l='No BlendShape Node', bgc=[0.8, 0, 0])

    def reload_mesh(self, sel):
        """重载网格

        Args:
            sel (str): 网格对象名称
        """
        if sel and self.mesh_exists(sel):
            cmds.textFieldGrp('meshShapeText', text=sel, e=1)
            self.refresh_target_list('append')
            blend_shape_node = self.get_blend_shape_node(sel)
            cmds.text('blendShapeText', e=1, label=blend_shape_node)
            cmds.textFieldButtonGrp('TargetGoemerty', e=1, tx=cmds.textFieldGrp('meshShapeText', text=1, q=1))
        else:
            cmds.textFieldGrp('meshShapeText', text='No deformable objects selected.', e=1)
            cmds.text('blendShapeText', e=1, label='')

    def load_text(self, field_button_grp):
        """加载文本到文本框

        Args:
            field_button_grp (str): 文本框按钮组名称
        """
        sel_obj = cmds.ls(sl=1)
        if sel_obj:
            cmds.textFieldButtonGrp(field_button_grp, edit=True, text=sel_obj[0])

    def update_inbetween_weight(self):
        """更新in-between权重"""
        blend_shape_mesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
        blend_shape_node = self.get_blend_shape_node(blend_shape_mesh)
        target_blend_shape_text = self.get_target_blend_shape_text()

        mirror_target_name = self.get_mirror_target_name(target_blend_shape_text)

        try:
            target_index = blendshape.getTargetIndex(blend_shape_node, target_blend_shape_text)
            input_target_item = cmds.getAttr(
                blend_shape_node + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % target_index, mi=True)
            cmds.textScrollList('targetInbetweenText', edit=True, removeAll=True)

            if cmds.checkBoxGrp('Inbetween', query=True, v1=True) == 1:
                cmds.floatSliderGrp('InbetweenSlider', edit=True, v=0)

            for i in input_target_item:
                index_int = (int(i) - 5000) / 1000.0
                cmds.textScrollList('targetInbetweenText', edit=True, append=str(index_int), sii=1)

            cmds.textFieldButtonGrp('Target_Text', tx=target_blend_shape_text, edit=True)
            cmds.textFieldButtonGrp('MirrorTargetText', tx=mirror_target_name, edit=True)
            cmds.textField('targetField', tx=target_blend_shape_text, e=True)

            if not cmds.checkBox('autoMirrorTargetNameCB', q=True, v=True):
                mirror_target_name = ''

            cmds.textField('sourceField', tx='', e=True)
            if mirror_target_name in cmds.textScrollList('targetBlendShapeText', q=1, ai=1):
                cmds.textField('sourceField', tx=mirror_target_name, e=True)
        except Exception as e:
            print("更新in-between权重时出错: {0}".format(e))

    def update_target_info(self):
        """更新目标信息"""
        try:
            tar_name = cmds.textScrollList('targetBlendShapeText', q=True, si=True)[0]
            blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            tar_index = blendshape.getTargetIndex(blend_shape_field, tar_name)
            cmds.floatField('InbetweenField', e=True, v=tar_index)
        except Exception as e:
            print("更新目标信息时出错: {0}".format(e))

    def set_blend_shape(self):
        """设置blendShape"""
        blend_shape_mesh = cmds.textFieldGrp('meshShapeText', query=True, text=True)
        in_list = cmds.textScrollList('targetInbetweenText', query=True, si=True)
        target_blend_shape_sel = self.get_target_blend_shape_text()

    def inbetween_box(self):
        """处理in-between复选框"""
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

    def put_offset_in_gray(self, shape_offset, rb2):
        """处理偏移量灰度显示"""
        if cmds.radioButtonGrp(rb2, q=1, sl=1) == 1:
            cmds.floatFieldGrp(shape_offset, e=1, en=1)
        if cmds.radioButtonGrp(rb2, q=1, sl=1) == 2:
            cmds.floatFieldGrp(shape_offset, e=1, en=0)

    def edit_field(self, field):
        """编辑字段"""
        cmds.textField(field, tx=self.get_target_blend_shape_text(), edit=True)

    def remove_target(self):
        """删除目标"""
        blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
        target_blend_shape = self.get_target_blend_shape_text()
        try:
            blendshape.delete_target(blend_shape_field, target_blend_shape)
            self.refresh_target_list('remove')
        except Exception as e:
            print("删除目标时出错: {0}".format(e))

    def gain_target(self):
        """增益目标"""
        blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
        target_blend_shape = self.get_target_blend_shape_text()
        generate_mesh = blendshape.regenerateTarget(blend_shape_field, target_blend_shape)
        cmds.select(generate_mesh, add=True)

    def rename_target(self):
        """重命名目标"""
        blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
        target_blend_shape = self.get_target_blend_shape_text()

        result = cmds.promptDialog(
            title='Rename Target',
            text=target_blend_shape,
            message='Enter New Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel'
        )

        if result == 'OK':
            new_name = cmds.promptDialog(query=True, text=True)
            if new_name and new_name != target_blend_shape:
                try:
                    blendshape.renameTarget(blend_shape_field, target_blend_shape, newName=new_name)
                    self.refresh_target_list('append')
                except Exception as e:
                    print("重命名目标时出错: {0}".format(e))

    def append_target(self):
        """追加目标"""
        pass

    def revert_target(self):
        """恢复目标"""
        pass

    def edit_finish_button(self):
        """编辑完成按钮"""
        pass

    def input_geom_target(self):
        """输入几何体目标"""
        pass

    def inbetween_edit_add_button(self):
        """in-between编辑添加按钮"""
        pass

    def mirror_blend_shape(self, mode=0):
        """镜像blendShape

        Args:
            mode (int): 镜像模式 (0: 标准镜像, 1: 目标到源镜像)
        """
        # 实现镜像逻辑
        pass

    def mirror_blend_shape_list(self, mode, l_target_list, r_target_list):
        """批量镜像blendShape

        Args:
            mode (int): 镜像模式
            l_target_list (list): 左侧目标列表
            r_target_list (list): 右侧目标列表
        """
        # 实现批量镜像逻辑
        pass

    def rebuild_target_items(self, target_geo, del_target):
        """重建目标项目

        Args:
            target_geo (str): 目标几何体
            del_target (str): 是否删除目标 ('yes' 或 'no')
        """
        sels = cmds.ls(sl=True, type='transform')
        list_connect = []
        list_connect_target = []
        list_connect_get = []

        try:
            target_blend_shape_list = blendshape.getBlendshapeNodes(target_geo)
            if target_blend_shape_list and len(target_blend_shape_list) == 1:
                target_blend_shape = target_blend_shape_list[0]
                if target_blend_shape == target_geo + '_blendShape':
                    target_blend_shape = cmds.rename(target_blend_shape, target_blend_shape + '_old')
            elif len(target_blend_shape_list) > 1:
                cmds.error('More than one blendShape Node')
            elif not target_blend_shape_list:
                cmds.error('There is no blendShape Node')

            if cmds.getAttr(target_blend_shape + '.envelope') != 1:
                cmds.setAttr(target_blend_shape + '.envelope', 1)

            list_target = cmds.listAttr(target_blend_shape + '.weight', multi=True)
            list_shpae = cmds.listRelatives(target_geo, s=True)
            list_target_blend_shape = list_target
            target_geo_new_blend_shape = target_geo + '_blendShape'
            target_geo_new_blend_shape = cmds.blendShape(target_geo, exclusive='deformPartition#', frontOfChain=True,
                                                         name=target_geo_new_blend_shape)[0]

            xi = 0
            for i in list_target_blend_shape:
                target_connect = cmds.listConnections(target_blend_shape + '.' + i, p=True, s=True, d=False)
                if target_connect:
                    for m in target_connect:
                        cmds.disconnectAttr(m, target_blend_shape + '.' + i)
                    list_connect.append(m)
                    list_connect_target.append(i)
                else:
                    get = i + '>' + str(cmds.getAttr(target_blend_shape + '.' + i))
                    list_connect_get.append(get)
                cmds.setAttr(target_blend_shape + '.' + i, 0)

            for x in list_target_blend_shape:
                try:
                    target_index = blendshape.getTargetIndex(target_blend_shape, x)
                    input_target_item = cmds.getAttr(
                        target_blend_shape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % target_index,
                        mi=True)
                    to_names = self.creative_target(target_blend_shape, [x], None)

                    for i in range(len(input_target_item)):
                        c = input_target_item[i]
                        to_name = to_names[i]
                        index_int = (int(c) - 5000) / 1000.0
                        if float(index_int) == 1:
                            cmds.blendShape(target_geo_new_blend_shape, edit=True, tc=False,
                                            target=(target_geo, xi, to_name, 1.0))
                        else:
                            cmds.blendShape(target_geo_new_blend_shape, edit=True, ib=True, tc=False,
                                            target=(target_geo, xi, to_name, float(index_int)))

                    if del_target == 'yes':
                        cmds.delete(to_names)
                    xi += 1
                except Exception as e:
                    print("处理目标 {0} 时出错: {1}".format(x, e))

            for i in range(len(list_connect)):
                cmds.connectAttr(list_connect[i], target_blend_shape + '.' + list_connect_target[i])
                cmds.connectAttr(list_connect[i], target_geo_new_blend_shape + '.' + list_connect_target[i])

            for i in list_connect_get:
                list_connect_wt = i.split('>')
                cmds.setAttr(target_blend_shape + '.' + list_connect_wt[0], float(list_connect_wt[1]))
                cmds.setAttr(target_geo_new_blend_shape + '.' + list_connect_wt[0], float(list_connect_wt[1]))

            cmds.delete(target_blend_shape)
            cmds.select(sels)
        except Exception as e:
            print("重建目标项目时出错: {0}".format(e))

    def rearrange_target_list(self, target_geo, tar_strs):
        """重新排列目标列表

        Args:
            target_geo (str): 目标几何体
            tar_strs (list): 目标字符串列表
        """
        try:
            target_blend_shape_list = blendshape.getBlendshapeNodes(target_geo)
            if target_blend_shape_list and len(target_blend_shape_list) == 1:
                target_blend_shape = target_blend_shape_list[0]
                if target_blend_shape == target_geo + '_blendShape':
                    target_blend_shape = cmds.rename(target_blend_shape, target_blend_shape + '_old')
            elif len(target_blend_shape_list) > 1:
                cmds.error('More than one blendShape Node')
            elif not target_blend_shape_list:
                cmds.error('There is no blendShape Node')

            if cmds.getAttr(target_blend_shape + '.envelope') != 1:
                cmds.setAttr(target_blend_shape + '.envelope', 1)

            list_target = cmds.listAttr(target_blend_shape + '.weight', multi=True)
            new_targets = []
            special_tars = []
            no_right_tars = []
            no_left_tars = []

            for tar_str in tar_strs:
                for bs_target in list_target:
                    if bs_target not in new_targets:
                        if tar_str in bs_target:
                            new_targets.append(bs_target)
                            if bs_target[:2] == 'L_':
                                if 'R_' + bs_target[2:] not in list_target:
                                    no_right_tars.append(bs_target)
                            if bs_target[:2] == 'R_':
                                if 'L_' + bs_target[2:] not in list_target:
                                    no_left_tars.append(bs_target)

            for bs_target in list_target:
                if bs_target not in new_targets:
                    special_tars.append(bs_target)

            new_target_2s = new_targets + special_tars
            print('[')
            for target1 in new_target_2s:
                print("'" + target1 + "',")
            print(']')
            print(len(list_target), '---', len(new_target_2s))
            print('左侧形状，右侧没有---', no_right_tars)
            print('右侧形状，左侧没有---', no_left_tars)
            print('不在上述规则中的target,放在列表最后---', special_tars)
            print(new_target_2s)
        except Exception as e:
            print("重新排列目标列表时出错: {0}".format(e))

    def rearrange_target(self, target_geo, del_target, list_target):
        """重新排列目标

        Args:
            target_geo (str): 目标几何体
            del_target (str): 是否删除目标 ('yes' 或 'no')
            list_target (list): 目标列表
        """
        sels = cmds.ls(sl=True, type='transform')
        list_connect = []
        list_connect_target = []
        list_connect_get = []

        try:
            target_blend_shape_list = blendshape.getBlendshapeNodes(target_geo)
            if target_blend_shape_list and len(target_blend_shape_list) == 1:
                target_blend_shape = target_blend_shape_list[0]
                if target_blend_shape == target_geo + '_blendShape':
                    target_blend_shape = cmds.rename(target_blend_shape, target_blend_shape + '_old')
            elif len(target_blend_shape_list) > 1:
                cmds.error('More than one blendShape Node')
            elif not target_blend_shape_list:
                cmds.error('There is no blendShape Node')

            if cmds.getAttr(target_blend_shape + '.envelope') != 1:
                cmds.setAttr(target_blend_shape + '.envelope', 1)

            list_shpae = cmds.listRelatives(target_geo, s=True)
            list_target_blend_shape = list_target
            target_geo_new_blend_shape = target_geo + '_blendShape'
            target_geo_new_blend_shape = cmds.blendShape(target_geo, exclusive='deformPartition#', frontOfChain=True,
                                                         name=target_geo_new_blend_shape)[0]

            xi = 0
            for i in list_target_blend_shape:
                target_connect = cmds.listConnections(target_blend_shape + '.' + i, p=True, s=True, d=False)
                if target_connect:
                    for m in target_connect:
                        cmds.disconnectAttr(m, target_blend_shape + '.' + i)
                    list_connect.append(m)
                    list_connect_target.append(i)
                else:
                    get = i + '>' + str(cmds.getAttr(target_blend_shape + '.' + i))
                    list_connect_get.append(get)
                cmds.setAttr(target_blend_shape + '.' + i, 0)

            for x in list_target_blend_shape:
                try:
                    target_index = blendshape.getTargetIndex(target_blend_shape, x)
                    input_target_item = cmds.getAttr(
                        target_blend_shape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % target_index,
                        mi=True)
                    to_names = self.creative_target(target_blend_shape, [x], None)

                    for i in range(len(input_target_item)):
                        c = input_target_item[i]
                        to_name = to_names[i]
                        index_int = (int(c) - 5000) / 1000.0
                        if float(index_int) == 1:
                            cmds.blendShape(target_geo_new_blend_shape, edit=True, tc=False,
                                            target=(target_geo, xi, to_name, 1.0))
                        else:
                            cmds.blendShape(target_geo_new_blend_shape, edit=True, ib=True, tc=False,
                                            target=(target_geo, xi, to_name, float(index_int)))

                    if del_target == 'yes':
                        cmds.delete(to_names)
                    xi += 1
                except Exception as e:
                    print("处理目标 {0} 时出错: {1}".format(x, e))

            for i in range(len(list_connect)):
                cmds.connectAttr(list_connect[i], target_blend_shape + '.' + list_connect_target[i])
                cmds.connectAttr(list_connect[i], target_geo_new_blend_shape + '.' + list_connect_target[i])

            for i in list_connect_get:
                list_connect_wt = i.split('>')
                cmds.setAttr(target_blend_shape + '.' + list_connect_wt[0], float(list_connect_wt[1]))
                cmds.setAttr(target_geo_new_blend_shape + '.' + list_connect_wt[0], float(list_connect_wt[1]))

            cmds.delete(target_blend_shape)
            cmds.select(sels)
        except Exception as e:
            print("重新排列目标时出错: {0}".format(e))

    def target_mirror_list(self, mirror_str_list):
        """目标镜像列表

        Args:
            mirror_str_list (str): 镜像字符串列表
        """
        try:
            blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            list_target = cmds.listAttr(blend_shape_field + '.weight', multi=True)
            print(list_target)
            print(mirror_str_list)
            mirror_str_list = mirror_str_list.split(',')
            print(mirror_str_list)
            list_target1 = []
            l_target_list = []
            r_target_list = []
            m_target_list = []

            for bs_target in list_target:
                if bs_target not in list_target1:
                    for mirror_str in mirror_str_list:
                        mirror_str = mirror_str.split('=')
                        l_str = mirror_str[0]
                        r_str = mirror_str[1]
                        if l_str[-1] == '*' and l_str[0] != '*':
                            l_str = l_str[:-1]
                            r_str = r_str[:-1]
                            l_str_len = len(l_str)
                            if bs_target[:l_str_len] == l_str:
                                r_target = r_str + bs_target[l_str_len:]
                                if r_target in list_target:
                                    l_target_list.append(bs_target)
                                    r_target_list.append(r_target)
                                    list_target1.append(bs_target)
                                    list_target1.append(r_target)
                                    break
                        elif l_str[0] == '*' and l_str[-1] != '*':
                            l_str = l_str[1:]
                            r_str = r_str[1:]
                            l_str_len = len(l_str)
                            if bs_target[-l_str_len:] == l_str:
                                r_target = bs_target[:-l_str_len] + r_str
                                if r_target in list_target:
                                    l_target_list.append(bs_target)
                                    r_target_list.append(r_target)
                                    list_target1.append(bs_target)
                                    list_target1.append(r_target)
                                    break
                        elif l_str[0] == '*' and l_str[-1] == '*':
                            l_str = l_str[1:-1]
                            r_str = r_str[1:-1]
                            l_str_len = len(l_str)
                            if l_str in bs_target:
                                r_target = bs_target.replace(l_str, r_str)
                                if r_target in list_target:
                                    l_target_list.append(bs_target)
                                    r_target_list.append(r_target)
                                    list_target1.append(bs_target)
                                    list_target1.append(r_target)
                                    break

            for bs_target in list_target:
                if bs_target not in l_target_list and bs_target not in r_target_list:
                    m_target_list.append(bs_target)

            print('原始target数量', len(list_target))
            print('左右target数量 + 中间target数量=', len(l_target_list), ' + ', len(r_target_list), '+',
                  len(m_target_list), '=', len(l_target_list + r_target_list + m_target_list))
            print('左侧的target\n', l_target_list)
            print('右侧的target\n', r_target_list)
            print('中间的target\n', m_target_list)

            for bs_target in list_target:
                if bs_target in l_target_list and bs_target in r_target_list:
                    print(bs_target)
                if bs_target in l_target_list and bs_target in m_target_list:
                    print(bs_target)
                if bs_target in r_target_list and bs_target in m_target_list:
                    print(bs_target)

            # 更新UI文本框
            cmds.textField('L_TargetList_TF', tx=str(l_target_list), e=True)
            cmds.textField('R_TargetList_TF', tx=str(r_target_list), e=True)
        except Exception as e:
            print("处理目标镜像列表时出错: {0}".format(e))

    def creative_target(self, blend_shape, target=[], prefix=None):
        """创建目标

        Args:
            blend_shape (str): blendShape节点
            target (list): 目标列表
            prefix (str): 前缀

        Returns:
            list: 创建的目标名称列表
        """
        list_connect = []
        list_connect_target = []
        list_lock_target = []
        list_value_target = []
        list_connect_name = []
        mesh_orig_list = []
        list_target_blend_shape = cmds.listAttr(blend_shape + '.weight', multi=True)

        if not cmds.objExists(blend_shape + '_Grp'):
            blend_shape_grp = cmds.createNode('transform', name=blend_shape + '_Grp')

        for i in list_target_blend_shape:
            if cmds.getAttr(blend_shape + '.' + i, l=1):
                cmds.setAttr(blend_shape + '.' + i, l=0)
                list_lock_target.append(i)
            get = cmds.getAttr(blend_shape + '.' + i)
            list_value_target.append(get)
            target_connect = cmds.listConnections(blend_shape + '.' + i, p=True, s=True, d=False)
            if target_connect:
                for m in target_connect:
                    cmds.disconnectAttr(m, blend_shape + '.' + i)
                list_connect.append(m)
                list_connect_target.append(i)
            cmds.setAttr(blend_shape + '.' + i, 0)

        # 获取原始形状
        mesh_orig_list = self.mesh_orig(blend_shape)

        for x in target:
            if x not in list_target_blend_shape or 'weight[' in x:
                continue
            try:
                target_index = blendshape.getTargetIndex(blend_shape, x)
                input_target_item = cmds.getAttr(
                    blend_shape + '.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % target_index, mi=True)

                for c in input_target_item:
                    index_int = (int(c) - 5000) / 1000.0
                    mesh = cmds.createNode('mesh', name=x + '_Shape')
                    mesh_mian_shape = cmds.createNode('mesh', name=x + '_MianShape')
                    cmds.sets(mesh, edit=True, forceElement='initialShadingGroup')
                    list_rel = cmds.listRelatives(mesh, p=True)
                    mian_list_rel = cmds.listRelatives(mesh_mian_shape, p=True)
                    cmds.setAttr(blend_shape + '.' + x, float(index_int))
                    cmds.connectAttr(blend_shape + '.outputGeometry[0]', mesh_mian_shape + '.inMesh')
                    if mesh_orig_list:
                        cmds.connectAttr(mesh_orig_list[0] + '.outMesh', mesh + '.inMesh')
                    copy_mesh = cmds.duplicate(mian_list_rel)
                    count = str(index_int).split('.')
                    if count[0] == '-0':
                        ne = 'm'
                    else:
                        ne = 'p'
                    if float(index_int) == 1:
                        target_name = x
                    else:
                        target_name = x + '_' + ne + count[1]
                    cmds.parent(copy_mesh, blend_shape + '_Grp')
                    if prefix == 1:
                        target_name = '_' + target_name
                    to_name = cmds.rename(copy_mesh, target_name)
                    cmds.addAttr(to_name, longName=x, at='double')
                    cmds.setAttr(to_name + '.' + x, float(index_int))
                    cmds.setAttr(blend_shape + '.' + x, 0)
                    cmds.delete(list_rel, mian_list_rel)
                    list_connect_name.append(to_name)
            except Exception as e:
                print("创建目标 {0} 时出错: {1}".format(x, e))

        for i in range(len(list_target_blend_shape)):
            val = list_value_target[i]
            cmds.setAttr(blend_shape + '.' + list_target_blend_shape[i], val)

        for i in list_lock_target:
            cmds.setAttr(blend_shape + '.' + i, l=1)

        for i in range(len(list_connect)):
            cmds.connectAttr(list_connect[i], blend_shape + '.' + list_connect_target[i])

        return list_connect_name

    def mesh_orig(self, mesh_node):
        """获取网格的原始形状

        Args:
            mesh_node (str): 网格节点

        Returns:
            list: 原始形状列表
        """
        mesh_orig_list = []
        try:
            mesh_orig = cmds.listHistory(mesh_node)
            for i in range(len(mesh_orig)):
                if cmds.nodeType(mesh_orig[i]) == 'mesh':
                    if 'Orig' in mesh_orig[i]:
                        if mesh_orig[i] and cmds.listConnections(mesh_orig[i] + '.worldMesh[0]', source=True):
                            mesh_orig_list.append(mesh_orig[i])
        except Exception as e:
            print("获取原始形状时出错: {0}".format(e))
        return mesh_orig_list

    def creative_target_clone(self):
        """创建目标克隆"""
        target_geometry = cmds.textFieldButtonGrp('TargetGoemerty', query=True, text=True)
        source_geometry = cmds.textFieldButtonGrp('SourceGoemerty', query=True, text=True)
        clone_targets_data = self.get_clone_target_value_list()
        clone_list = clone_targets_data[0]

        is_delete_target = cmds.checkBox('delTargetCB', query=True, value=True)

        selected_clone_list = None
        if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
            selected_clone_list = []
            for clone_target in clone_list:
                if cmds.checkBox(clone_target, query=True, value=True):
                    target_annotation = cmds.checkBox(clone_target, query=True, annotation=True)
                    selected_clone_list.append(target_annotation)

        # 使用blendshape模块的copyBs函数执行克隆
        try:
            blendshape.copyBs(
                source_geometry,
                target_geometry,
                skipLock=True,
                replaceConnect=True,
                cloneList=selected_clone_list,
                delTarget=is_delete_target
            )
        except Exception as e:
            print("克隆目标时出错: {0}".format(e))

    def get_clone_target_value_list(self):
        """获取克隆目标值列表

        Returns:
            tuple: (克隆列表, 目标值列表)
        """
        if cmds.button('cloneButton', query=True, label=True) == 'Cancel':
            clone_target_value_list = cmds.rowColumnLayout('clone_rclayout', q=1, childArray=1)
            clone_list = []
            target_values = []
            for clone_target_value in clone_target_value_list:
                if 'Clone_' in clone_target_value:
                    clone_list.append(clone_target_value)
                elif 'targetValue_' in clone_target_value:
                    target_values.append(clone_target_value)
        else:
            clone_list = []
            target_values = []
        return (clone_list, target_values)

    def edit_clone_button(self):
        """编辑克隆按钮"""
        button_label = cmds.button('cloneButton', query=True, label=True)
        if self.blend_shape_node_on_off():
            if button_label == 'Clone Target List':
                cmds.button('cloneButton', edit=True, label='Cancel')
                self.clone_list_on()
        if button_label == 'Cancel':
            cmds.button('cloneButton', edit=True, label='Clone Target List')
            self.clone_list_off()
        if not self.blend_shape_node_on_off():
            dialog = 'The Goemerty has no BlendShape node.'
            cmds.confirmDialog(title='Confirm', message=dialog, button=['Yes', 'No'], defaultButton='Yes',
                               cancelButton='No', dismissString='No')
            blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            cmds.text('blendShapeText', e=True, label=blend_shape_field)

    def clone_list_on(self):
        """显示克隆列表"""
        if self.blend_shape_node_on_off():
            blend_shape_field = self.get_blend_shape_node(cmds.textFieldGrp('meshShapeText', query=True, text=True))
            target_blend_shape = blendshape.getTargetList(blend_shape_field)
            target_int = cmds.blendShape(blend_shape_field, query=True, wc=True)

            if target_int > 0:
                for t in target_blend_shape:
                    try:
                        target_value = cmds.getAttr(blend_shape_field + '.' + t)
                        target_connect = cmds.listConnections(blend_shape_field + '.' + t, p=True, s=True, d=False)

                        if target_value < 0.0001:
                            target_value = 0

                        if target_connect is None and target_value >= 0.001:
                            cmds.text('targetValue_%s' % t, l='%.2g' % target_value, p='clone_rclayout', en=0, w=40,
                                      bgc=[0.8, 0, 0])
                        elif target_connect is None:
                            cmds.text('targetValue_%s' % t, l='%.2g' % target_value, p='clone_rclayout', en=0, w=40,
                                      bgc=[0.8, 0.8, 0])
                        elif target_value >= 0.0001 and target_connect is not None:
                            cmds.text('targetValue_%s' % t, l='%.2g' % target_value, p='clone_rclayout', en=0, w=40,
                                      bgc=[0, 0.45, 1])
                        else:
                            cmds.text('targetValue_%s' % t, l='%.2g' % target_value, p='clone_rclayout', en=0, w=40)

                        cmds.checkBox('Clone_%s' % t, l=t, p='clone_rclayout', ann='%s' % t)
                    except Exception as e:
                        print("显示克隆列表项时出错: {0}".format(e))

            if len(target_blend_shape) * 20 > 400:
                scroll_layout_h = 400
            elif len(target_blend_shape) * 20 < 200:
                scroll_layout_h = 200
            else:
                scroll_layout_h = len(target_blend_shape) * 20

        cmds.frameLayout('cloneFrame', e=1, cl=0)

    def clone_list_off(self):
        """隐藏克隆列表"""
        try:
            cmds.deleteUI(cmds.rowColumnLayout('clone_rclayout', q=1, fpn=1))
            cmds.rowColumnLayout('clone_rclayout', numberOfColumns=2, p='cloneList')
            cmds.frameLayout('cloneFrame', e=1, cl=1)
        except Exception as e:
            print("隐藏克隆列表时出错: {0}".format(e))

    def clone_sel_invert(self):
        """克隆选择反选"""
        clone_list = self.get_clone_target_value_list()[0]
        for b in clone_list:
            if cmds.checkBox(b, q=1, v=1):
                cmds.checkBox(b, e=1, v=0)
            else:
                cmds.checkBox(b, e=1, v=1)

    def select_by_keyword(self):
        """根据关键字选择"""
        input_text = cmds.textFieldButtonGrp('selTarget_TF_but', query=True, tx=True)
        cleaned_text = input_text.strip() if input_text else ""

        if cleaned_text:
            keywords = [kw.strip() for kw in cleaned_text.split(',') if kw.strip()]
        else:
            keywords = []

        if not keywords:
            cmds.warning("未输入有效的关键词，请检查输入内容！")
        else:
            self.select_target_by_keyword(keywords)

    def select_target_by_keyword(self, keywords):
        """根据关键字选择目标

        Args:
            keywords (list): 关键字列表
        """
        if cmds.button('cloneButton', q=True, label=True) != 'Cancel':
            return

        try:
            for widget in cmds.rowColumnLayout('clone_rclayout', q=True, childArray=True):
                if 'Clone_' in widget and any(kw.lower() in widget.lower() for kw in keywords):
                    cmds.checkBox(widget, e=True, value=True)
        except Exception as e:
            print("根据关键字选择目标时出错: {0}".format(e))


