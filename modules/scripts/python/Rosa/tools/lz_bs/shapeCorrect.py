#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2014 RigTd ChunHai Zhao
## @brief Inverts a shape through the deformation chain
# @author ChunHai Zhao - http://blog.sina.com.cn/u/2364869810
#
"""update list:
#my test command:
import sys
sys.path.append(r"H:\script\prefs\plug-ins\pluginSource\shapeCorrect\scripts")
import shapeCorrect;reload(shapeCorrect)
shapeCorrect.cort.correctiveShapeCmd()

20141027:
    the first version
20141104(v1.10)：
    修复保存文件再打开后节点有可能失效的问题
    修复correctiveShapeCmd在以后blendshape关闭的情况下无法正确计算的问题
20141105（v1.20）：
    envelope加入计算
20141117:
    修复已经存在blendShape的情况下 可能计算错误的问题
"""


#put shapeCorrect.py in your scripts
#load plugin
#--python command--
#import shapeCorrect;reload(shapeCorrect)
#shapeCorrect.cort.correctiveShapeCmd()


import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as om
import re

class ShapeCorrect():
    
    def pluginName(self,plugin):
        """ get plugin name of current maya version"""
        if mc.about(is64=1):
            x86x64 = "x64"
        else:
            x86x64 = "x86"
        mayaVersion = mc.about(f=1)
        pluginName = "%s%s%s.mll"%(plugin,mayaVersion,x86x64)
        return pluginName
        
    def searchControlShape(self,inObj):
        """
        Creation Date:  2014-04-04
        <doc>
        <name searchByName-->searchControlShape>
        <synopsis>
                searchControlShape(str inObj)
        <description>
              Script for finding a shape that can deforms.
        <examples>
         // To find the skinCluster for a skin called "GreatZ", type:
         searchControlShape("GreatZ")
        """
        controlShape,controlShapeWithPath,hiddenShape,hiddenShapeWithPath = "","","",""
        #if conponent list input pick first
        if type(inObj)==list or type(inObj)==tuple and len(inObj)>0:
            inObj = inObj[0]
        if None!=re.search("\.",inObj):
            inObj = re.split("\.",inObj)[0]
        cpTest = mc.ls(inObj,type="controlPoint")
        if len(cpTest):
            return inObj
        else:
            rels = mc.listRelatives(inObj)
            if rels==None:
                return
            for r in rels:
                cpTest = mc.ls(inObj+"|"+r,type="controlPoint")
                if 0==len(cpTest):
                    continue
                io = mc.getAttr(inObj+"|"+r+".io")
                if io:
                    continue
                visible = mc.getAttr(inObj+"|"+r+".v")
                if 0==visible:
                    hiddenShape = r
                    hiddenShapeWithPath = (inObj+"|"+r)
                    continue
                controlShape = r
                controlShapeWithPath = (inObj+"|"+r)
                break
        for shape in [controlShape,controlShapeWithPath,hiddenShape,hiddenShapeWithPath]:
            if 0!=len(shape) and len( mc.ls(shape) )==1:
                return shape
                
    def findRelatedBlendshape(self,bldObj=""):
        """
        Creation Date:  2014-04-04
        <doc>
        <name findRelatedBlendshape>
        <synopsis>
                findRelatedBlendshape(str bldObj)
        <description>
              Script for finding a blendshape that deforms the specified blendShape
        <examples>
         // To find the blendShape for a bld called "GreatZ", type:
         findRelatedBlendshape("GreatZ")
        """
        resBls = []
        if bldObj=="":
            selObjs = mc.ls(sl=True,ap=1,fl=True)
            if len(selObjs)>0:
                bldObj = selObjs[0]
            else:
                return []
        shape = self.searchControlShape(bldObj)
        if shape==None:
            return []
        blendShapes = mc.ls(type="blendShape")
        for bls in blendShapes:
            geom = mc.blendShape(bls,q=True,g=True)
            if geom!=None:
                for g in geom:
                    if g == shape:
                        resBls.append(bls)
        return resBls
        
    def findRelatedSkinCluster(self,wetMod):
        skinNode = mel.eval( 'findRelatedSkinCluster("%s")'%wetMod )
        if skinNode=="":
            return
        return skinNode
        
    def CCo_getMeshOrig(self,inObj):
        """...shared\mesh
        get MeshOrig
        """
        #if obj has deform node
        allList = mc.ls(mc.listRelatives(inObj,shapes=True,c=True),type="mesh")
        itsShapes = mc.listRelatives(inObj,shapes=1,pa=1)
        for sp in itsShapes:
            if sp not in allList:
                allList.append(sp)
                

        for obj in allList:
            value = mc.getAttr('%s.intermediateObject'%(obj))
            upTrans = mc.listRelatives(obj,parent=True,pa=True)
            hasOutPut = mc.listConnections("%s.worldMesh"%(obj),d=1)
            hasInPut = mc.listConnections( "%s.inMesh"%(obj),s=1,d=0 )
            #self.mayaPrint(upTrans)
            if value and upTrans==[inObj] and hasOutPut!=None and hasInPut==None:
                #self.mayaPrint(obj)
                return obj
        
    def CC_getOneMesh(self,obj=""):
        """
        obj== "objectName" check is mesh ?
        obj==None get one mesh from select and check is mesh?
        """
        objLs = [obj]
        #check input
        if objLs==[None]:
            objLs = mc.ls(sl=True)
        #is mesh ?
        if len(objLs)==1 and mc.objExists(objLs[0]):
            polys = mc.filterExpand(objLs,sm=12)
            if polys!=None:
                return objLs[0]
                
    def __dupAsSculpt(self,deformed):
        "duplicate object as sculpt mesh"
        sculpt = mc.duplicate(deformed,name="%s_Sculpture1"%deformed)[0]
        for atr in ["tx","ty","tz","rx","ry","rz","sx","sy","sz","v"]:
            mc.setAttr("%s.%s"%(sculpt,atr),lock=False)
        itShapes = mc.listRelatives(sculpt,s=True,f=True)
        if itShapes!=None and len(itShapes)>1:
            for sp in itShapes:
                if mc.getAttr( "%s.intermediateObject"%sp ):
                    mc.delete( sp )
        itShapes = mc.listRelatives(sculpt,s=True,f=True)
        shapeName = "%sShape"%sculpt
        if(itShapes[0]!=shapeName):
            shapeName = mc.rename( itShapes[0],shapeName )
        mc.setAttr( "%s.intermediateObject"%shapeName,0 )
        if mc.listRelatives(sculpt,p=True)!=None:
            mc.parent(sculpt,w=True)
        #raise Warning( "Runturn" )
        return sculpt
        
        
    def correctiveShapeCmd(self,deformed=None,ignoreBls=False,correctNodeType = 'chunhai' ):
        """...shared\mesh
        create corrective shape by shapeCorrect
        deformed : 加了变形器物体 可以输入 也可以通过选择获取
        ignoreBls: 忽略blendShap造成的变形
        """
        #plugin = self.pluginName("shapeCorrect")
        #if not mc.pluginInfo(plugin, query=True, loaded=True):
        #    mc.loadPlugin(plugin)
        #end if
        
        if correctNodeType == 'chunhai':
            
            type_correct = 'shapeCorrect'
        else:
            type_correct = 'shapeCorrect'
            
        deformed = self.CC_getOneMesh(deformed)
        if deformed==None:
            om.MGlobal.displayWarning("No one mesh input or selected")
            return
            
        #print(deformed)
        shapOrg = self.CCo_getMeshOrig(deformed)
        if shapOrg==None:
            om.MGlobal.displayWarning("Can not find shapeOrig of %s;"%deformed)
            return
        #        #duplicate for sculpt
        sculpt = self.__dupAsSculpt(deformed)
        target = mc.polyCreateFacet(ch=False,s=1,p=[(1,0,0),(0,1,0),(0,0,1)],name="%s_BlendShape_QQ51962215"%deformed)[0]
        mc.connectAttr("%s.worldMesh"%shapOrg,"%s.inMesh"%target)
        mc.setAttr("%s.intermediateObject"%shapOrg,0)
        mc.delete(target,ch=True)
        mc.setAttr("%s.intermediateObject"%shapOrg,1)
        #get it blendShape deformer
        bldShapes = self.findRelatedBlendshape(deformed)
        #remember blendshape state
        rmbVals = []
        for bls in  bldShapes:
            evl = "%s.envelope"%bls
            nst = "%s.nodeState"%bls
            rmbVals.extend(  [mc.getAttr(evl),mc.getAttr(nst)]  )
            if ignoreBls==True:
                mc.setAttr(nst,1)
        newBlsNode = ""
        removeTart = False
        if bldShapes==[] or ignoreBls==True:
            newBlsNode = mc.blendShape(target,deformed,frontOfChain=True,w=[0,1])[0]
        elif bldShapes!=[] and ignoreBls==False:
            removeTart = True
            bls = bldShapes[0]
            mc.setAttr("%s.envelope"%bls,1)
            mc.setAttr("%s.nodeState"%bls,0)
            counts = mc.blendShape(bls,q=1,wc=1)
            mis = mel.eval('bsMultiIndexForTarget("%s",%d)'%(bls,counts-1))
            mi = counts if mis==-1 else (mis+1)
            mc.blendShape(bls,e=1,target=[deformed,mi+1,target,1])
            mc.setAttr("%s.%s"%(bls,target),1)
        #set inverse matrix
        spCrt_dfm = mc.deformer(target,type= type_correct )[0]
        mc.setShapeCorrectMatrix(s=sculpt,d=deformed,bs=target,sc=spCrt_dfm)
        mc.connectAttr("%s.worldMesh"%sculpt,"%s.sculptMesh"%spCrt_dfm)
        #reset blendshape state
        for idx in range( len(bldShapes) ):
            mc.setAttr( "%s.envelope"%bldShapes[idx],rmbVals[idx] )
            mc.setAttr( "%s.nodeState"%bldShapes[idx],rmbVals[idx+1] )
        if mc.objExists(newBlsNode):
            mc.delete(newBlsNode)
        if removeTart==True:
            mc.blendShape(bldShapes[0],e=True,rm=True,target=[deformed,1,target,1])
        target = mc.rename(target,"%s_BlendShape1"%deformed)
        #move side+ side++
        bdingBx = mc.polyEvaluate(target,boundingBox=True)
        xDifVal = bdingBx[0][1]-bdingBx[0][0]
        mc.move(xDifVal*1.10,sculpt,r=True,moveX=True)
        mc.move(xDifVal*2.20,target,r=True,moveX=True)
        mc.select(sculpt,target)
        #print(sculpt,target)
        return sculpt,target
        
#cort = ShapeCorrect()
        
        