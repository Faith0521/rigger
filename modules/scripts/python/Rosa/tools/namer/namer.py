#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author: rosa.w
#Mail: wrx1844@qq.com
#Computer language: Python.3.2.2
#scriptName : rosa_RenameTool.py
# add in git 2015/09/21
#------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#update:
#2016/03/08: support NonUniqueNames object.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
   █████▒█    ██  ▄████▄   ██ ▄█▀       ██████╗ ██╗   ██╗ ██████╗
 ▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒        ██╔══██╗██║   ██║██╔════╝
 ▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░        ██████╔╝██║   ██║██║  ███╗
 ░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄        ██╔══██╗██║   ██║██║   ██║
 ░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄       ██████╔╝╚██████╔╝╚██████╔╝
  ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒       ╚═════╝  ╚═════╝  ╚═════╝
  ░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░
  ░ ░    ░░░ ░ ░ ░        ░ ░░ ░
           ░     ░ ░      ░  ░
"""

import maya.cmds as mc
import pymel.core as pm
from ...maya_utils import aboutName


class namer(object):

    def __init__(self):
        pass

    def namer_ui(self):
        uiname = 'namer_ui'
        if mc.window(uiname ,ex = True):
            mc.deleteUI(uiname)

        mc.window(uiname , t = 'N a m e r - v 1 . 0' , s=False)
        mc.columnLayout(adjustableColumn = True)
        mc.separator( style='in',h=10 )
        mc.rowColumnLayout( numberOfColumns=2 ,columnAttach=(1, 'right',3), columnWidth=[(1, 70),(2,200)] )
        mc.text('SearchText',label = u'S e a r c h :')
        mc.textField('Load_Search',text = '')
        mc.separator( style='none',h=3 )
        mc.separator( style='none',h=3 )
        mc.text('ReplaceText',label = u'R e p l a c e :')
        mc.textField('Load_Replace',text = '')
        mc.separator( style='none',h=4 )
        mc.separator( style='none',h=4 )
        mc.setParent( '..' )
        mc.columnLayout(adjustableColumn = True)
        mc.iconTextButton( style='textOnly' , bgc=[0.5, 0.4, 0.33] , label='S e a r c h - A n d - R e p l a c e' , c=lambda *args:self.batchReplaceStr() )

        mc.separator( style='in',h=20 )
        mc.rowColumnLayout( numberOfColumns=2 ,columnAttach=(1, 'right', 5), columnWidth=[(1, 70),(2,200)] )
        mc.text('Prefix_Text',label = u'P r e f i x :')
        mc.textField('Load_Prefix',text = '')
        mc.setParent( '..' )
        mc.separator( style='none',h=3 )
        mc.separator( style='none',h=3 )
        mc.columnLayout(adjustableColumn = True)
        mc.iconTextButton( style='textOnly' , bgc=[0.5, 0.4, 0.33] , label='A d d - P r e f i x' , c=lambda *args:self.batchAddPrefix() )

        mc.separator( style='in',h=20 )
        mc.rowColumnLayout( numberOfColumns=2 ,columnAttach=(1, 'right', 5), columnWidth=[(1, 70),(2,200)] )
        mc.text('Suffix_Text',label = u'S u f f i x :')
        mc.textField('Load_Suffix',text = '')
        mc.separator( style='none',h=3 )
        mc.separator( style='none',h=3 )
        mc.setParent( '..' )
        mc.columnLayout(adjustableColumn = True)
        mc.iconTextButton( style='textOnly' , bgc=[0.5, 0.4, 0.33] , label='A d d - S u f f i x' , c=lambda *args:self.batchAddSuffix() )

        mc.separator( style='in',h=20 )
        mc.rowColumnLayout( numberOfColumns=2 ,columnAttach=(1, 'right', 5), columnWidth=[(1, 70),(2,200)] )
        mc.text('Rename_Text',label = u' R e n a m e :')
        mc.textField('Load_Rename',text = '')
        mc.separator( style='none',h=3 )
        mc.separator( style='none',h=3 )
        mc.setParent( '..' )
        mc.columnLayout(adjustableColumn = True)
        mc.iconTextButton( style='textOnly' , bgc=[0.23,0.33,0.39] , label='R e n a m e - A d d - N u m b e r' , c=lambda *args:self.batchOrderStr() )
        mc.separator(style='in', h=20)

        # add button
        mc.columnLayout('quickBtnLayout', en=1)
        mc.rowLayout('addPrefixRow',numberOfColumns=10)
        sizeH = 30
        sizeW = 51
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'L_', c=lambda *args: self.batchAddPrefix('L_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'R_', c=lambda *args: self.batchAddPrefix('R_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'lf_', c=lambda *args: self.batchAddPrefix('lf_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'rt_', c=lambda *args: self.batchAddPrefix('rt_'), h=sizeH, w=sizeW)
        mc.setParent('..')
        mc.rowLayout('addSuffixRow',numberOfColumns=10)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'_ctrl', c=lambda *args: self.batchAddSuffix('_ctrl'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'_jnt', c=lambda *args: self.batchAddSuffix('_jnt'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'_old', c=lambda *args: self.batchAddSuffix('_old'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'_new', c=lambda *args: self.batchAddSuffix('_new'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.5, 0.4, 0.33], l=u'_org', c=lambda *args: self.batchAddSuffix('_org'), h=sizeH, w=sizeW)
        mc.setParent('..')
        mc.rowLayout('replaceRow', numberOfColumns=10)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'L_ > R_', c=lambda *args: self.batchReplaceStr('L_', 'R_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'R_ > L_', c=lambda *args: self.batchReplaceStr('R_', 'L_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'lf_ > rt_', c=lambda *args: self.batchReplaceStr('lf_', 'rt_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'rt_ > lf_', c=lambda *args: self.batchReplaceStr('rt_', 'lf_'), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'_jnt > _ctrl', c=lambda *args: self.batchReplaceStr('_jnt', '_ctrl'), h=sizeH, w=sizeW)
        mc.setParent('..')
        mc.rowLayout('removeRow', numberOfColumns=10)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'_jnt > " "', c=lambda *args: self.batchReplaceStr('_jnt', ''), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'_ctrl > " "', c=lambda *args: self.batchReplaceStr('_ctrl', ''), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'_old > " "', c=lambda *args: self.batchReplaceStr('_old', ''), h=sizeH, w=sizeW)
        mc.iconTextButton(style='textOnly' , bgc=[0.23,0.33,0.39], l=u'_new > " "', c=lambda *args: self.batchReplaceStr('_new', ''), h=sizeH, w=sizeW)
        mc.setParent('..')
        
        mc.showWindow(uiname)

    def replaceStr(self, obj, searchStr,  replaceStr):
        if '|' in obj:
            realName = obj.name().split('|')[-1]
        else:
            realName = obj.name()

        newName = realName.replace(searchStr, replaceStr)
        if searchStr in realName:
            mc.rename(obj.name(), newName)
            return newName
        else:
            return realName

    def batchReplaceStr(self, searchStr='', replaceStr=''):
        if searchStr == '':
            searchStr = mc.textField('Load_Search', q=True , text=True)
        if replaceStr == '':
            replaceStr = mc.textField('Load_Replace', q=True , text=True)
        objs = pm.ls(sl=1)

        if len(objs) == 1 and mc.nodeType(objs[0].name()) == 'blendShape':
            bsNode = objs[0].name()
            attrs = aboutName.getSelectedAttrs()
            for i in range(0, attrs.__len__()):
                newName = attrs[i].replace(searchStr, replaceStr)
                mc.aliasAttr(newName, '{0}.{1}'.format(bsNode, attrs[i]))
        else:
            for obj in objs:
                self.replaceStr(obj, searchStr,  replaceStr)

    def addPrefix(self, obj, prefix):
        if '|' in obj.name():
            realName = obj.name().split('|')[-1]
        else:
            realName = obj.name()

        newName = prefix + realName
        mc.rename(obj.name(), newName)
        return newName

    def batchAddPrefix(self, prefix=''):
        if prefix == '':
            prefix = mc.textField('Load_Prefix', q=True , text=True)
        objs = pm.ls(sl=1)

        if len(objs) == 1 and mc.nodeType(objs[0].name()) == 'blendShape':
            bsNode = objs[0].name()
            attrs = aboutName.getSelectedAttrs()
            for i in range(0, attrs.__len__()):
                newName = prefix + attrs[i]
                mc.aliasAttr(newName, '{0}.{1}'.format(bsNode, attrs[i]))
        else:
            for obj in objs:
                self.addPrefix(obj, prefix)


    def addSuffix(self, obj, suffix):
        if '|' in obj.name():
            realName = obj.name().split('|')[-1]
        else:
            realName = obj.name()

        newName = realName + suffix
        mc.rename(obj.name(), newName)
        return newName

    def batchAddSuffix(self, suffix=''):
        if suffix == '':
            suffix = mc.textField('Load_Suffix', q=True , text=True)
        objs = pm.ls(sl=1)

        if len(objs) == 1 and mc.nodeType(objs[0].name()) == 'blendShape':
            bsNode = objs[0].name()
            attrs = aboutName.getSelectedAttrs()
            for i in range(0, attrs.__len__()):
                newName = attrs[i] + suffix
                mc.aliasAttr(newName, '{0}.{1}'.format(bsNode, attrs[i]))
        else:
            for obj in objs:
                self.addSuffix(obj, suffix)

    def batchOrderStr(self):
        newStr = mc.textField('Load_Rename', q=True , text=True)
        objs = pm.ls(sl=1)
        if '#' not in newStr:
            mc.error("You must used '#' instead order number")
        for i in range( len(objs) ):
            newOrderStr = newStr.replace('#' , str(i))
            mc.rename(objs[i].name() , newOrderStr)
