#!/usr/bin/python
# -*- coding: utf-8 -*-
import maya.cmds as mc
from . import LZ_blendshape_command as LZ_blendshape_command

class LZ_wrapBlend( LZ_blendshape_command.LZ_blendshape_command ,
                    
                    ):


    def LZ_WrapDeformer_UI(self):
    
        LZ_WrapDeformer_Win = 'LZ_WrapDeformer_UI'
    
        if (mc.window( LZ_WrapDeformer_Win , ex = 1 ) ) : mc.deleteUI(  LZ_WrapDeformer_Win , window = 1) 
        if(mc.windowPref( LZ_WrapDeformer_Win , ex = 1) ) : mc.windowPref( LZ_WrapDeformer_Win , remove = 1)
    
        mc.window ( LZ_WrapDeformer_Win,
                    title = LZ_WrapDeformer_Win,
                    width = 500,
                    height = 300,
                    menuBar = 1,
                    rtf = 0
                )
    
        base = mc.columnLayout( )
    
        #cr閍tion du textFieldButtonGrp originalObj
        originalObj = mc.textFieldButtonGrp('Original_Obj_TFB',
                            label = " Org Object", 
                            cw3 = (90, 350, 50), 
                            buttonLabel = "   <<< "
                            ) 
                            
        #Edition du textFieldButtonGrp originalObj
        mc.textFieldButtonGrp(originalObj,
                    e=1,
                    buttonCommand = lambda *args:self.fillTextFieldOrig('Original_Obj_TFB')
                    )
    
        
        #cr閍tion du textFieldButtonGrp  shapeToWrap    
        shapeToWrap = mc.textFieldButtonGrp (
                        label = " Target_mesh ", 
                        cw3 = (90, 350, 50),
                        buttonLabel = "   <<< " 
                        )
        #Edition du textFieldButtonGrp shapeToWrap
        mc.textFieldButtonGrp (shapeToWrap,
                                e = 1,
                                buttonCommand = lambda *args:self.fillTextFieldShape(shapeToWrap) 
                                )
                                
        #cr閍tion du textFieldButtonGrp  newShape    
        newShape = mc.textFieldButtonGrp (
                        label = "newShape", 
                        cw3 = (90, 350, 50),
                        buttonLabel = "   <<< " 
                        )
                        
        #Edition du textFieldButtonGrp newShape
        mc.textFieldButtonGrp (newShape,
                                e = 1,
                                buttonCommand = lambda *args:self.fillTextFieldOrig(newShape) 
                                )
                                
        
        mirrorButton = mc.button  (
            label = "Wrap Blend Shape(s) !",
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            command = lambda *args:self.LZ_WrapDeformer_order(  PathOrg = originalObj , PathWrap = shapeToWrap  , PathNew = newShape  ) ,
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            width = 490,
            height = 32,
            al = "center"
            )
            
        replaceButton = mc.button  (
            label = " replace_meshConnections  ",
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            command = lambda *args:self.LZ_replace_meshConnections(  PathOrg = originalObj , PathWrap = shapeToWrap  , PathNew = newShape  ) ,
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            width = 490,
            height = 32,
            al = "center"
            )
            
        CloneButton = mc.button  (
            label = " clone_meshConnections  ",
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            command = lambda *args:self.LZ_clone_meshConnections(  PathOrg = originalObj , PathWrap = shapeToWrap  , PathNew = newShape  ) ,
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            width = 490,
            height = 32,
            al = "center"
            )
        
        
          
        mc.showWindow( LZ_WrapDeformer_Win )
        
    def LZ_replace_meshConnections(self , PathOrg = '' , PathWrap = '' , PathNew = '' ):
        shapeOrg = mc.textFieldButtonGrp(PathOrg, q=1, text= 1) 
        shapeToWrap = mc.textFieldButtonGrp(PathWrap, q=1, text= 1) 
        shapeNew = mc.textFieldButtonGrp(PathNew, q=1, text= 1) 
        
        if (len(shapeOrg) == 0) :
            return
        if (len(shapeToWrap) == 0) :
            return
        if (len(shapeNew) == 0) :
            return
        print( [shapeOrg ,shapeToWrap,shapeNew ])
        self.replaceMesh_connection(  orgMesh = shapeOrg , Origmesh = shapeToWrap  , cloneMehs = shapeNew  )
    
    def LZ_clone_meshConnections(self , PathOrg = '' , PathWrap = '' , PathNew = '' ):
        shapeOrg = mc.textFieldButtonGrp(PathOrg, q=1, text= 1) 
        shapeToWrap = mc.textFieldButtonGrp(PathWrap, q=1, text= 1) 
        shapeNew = mc.textFieldButtonGrp(PathNew, q=1, text= 1) 
        
        if (len(shapeOrg) == 0) :
            return
        if (len(shapeToWrap) == 0) :
            return
        if (len(shapeNew) == 0) :
            return
        print( [shapeOrg ,shapeToWrap,shapeNew ])
        self.replaceMesh_connection(  orgMesh = shapeOrg , Origmesh = shapeToWrap  , cloneMehs = shapeNew  )
        
    
    def fillTextFieldOrig(self,textFieldGrp) :
        listObj = mc.ls(sl = 1)
        if len(listObj) == 0 :
            return
        mc.textFieldButtonGrp(textFieldGrp, e = 1, text = listObj[0] )
    def fillTextFieldShape(self,textFieldGrp) :
        listObj = mc.ls(sl = 1)
    
        listObjConcat =""
        for i, obj in enumerate(listObj) :
            
            if (i == (len(listObj) - 1)) :
                listObjConcat += obj
            else :
                listObjConcat += obj + " "
            
        if len(listObj) == 0 :
            return
                    
        mc.textFieldButtonGrp(textFieldGrp, e = 1, text = listObjConcat)
    
    def LZ_WrapDeformer_order(self , PathOrg = '' , PathWrap = '' , PathNew = '' ):
        shapeOrg = mc.textFieldButtonGrp(PathOrg, q=1, text= 1) 
        shapeToWrap = mc.textFieldButtonGrp(PathWrap, q=1, text= 1) 
        shapeNew = mc.textFieldButtonGrp(PathNew, q=1, text= 1) 
        
        ShapeWrap_all = shapeToWrap.split(" ")
        
        if (len(shapeOrg) == 0) :
            return
        if (len(shapeToWrap) == 0) :
            return
        if (len(shapeNew) == 0) :
            return
        
        for sw in ShapeWrap_all:
            self.LZ_WrapDeformer( shapeOrg, sw , shapeNew)
        
        
    
    
        '''
        ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        
        
        #//On renomme l'objet dupliqucomme le shape copier, mais avec un suffixe temporaire en plus
        mirrorObj = shapeToCopy + "suffTemp"
        mc.duplicate (originalObj, rr = 1, n = "scaleObj")
        mc.duplicate (originalObj, rr = 1, n = "tempName")
        mc.rename("tempName", mirrorObj)  #//on peut lui donner le nom exact de la forme copier sans ajout d'un chiffre en suffixe
        
        #mc.select (r = originalObj)
        
        #//lock attributes if originalMesh
        mc.setAttr (OriginalObjTX, lock = 0 )
        mc.setAttr (OriginalObjTY, lock = 0 )
        mc.setAttr (OriginalObjTZ, lock = 0)
        mc.setAttr (OriginalObjRX , lock = 0 )
        mc.setAttr (OriginalObjRY , lock = 0 )
        mc.setAttr (OriginalObjRZ , lock = 0 )
        mc.setAttr (OriginalObjSX , lock = 0 )
        mc.setAttr (OriginalObjSY , lock = 0)
        mc.setAttr (OriginalObjSZ, lock = 0 )
    
        
        #//En fonction du bouton radio coch le scale de -1 se fait en x, y ou z.
        #//scale doit 阾re juste n間atif et non -1
        posScaleAttr = 0
        negScaleAttr = 0
        
        if (xyz == 1) :
            posScaleAttr = float(mc.getAttr("scaleObj.scaleX"))
            negScaleAttr = ((-1)*(posScaleAttr))
            mc.setAttr("scaleObj.scaleX", negScaleAttr)
    
        if (xyz == 2) :
            posScaleAttr = float(mc.getAttr("scaleObj.scaleY"))
            negScaleAttr = ((-1)*(posScaleAttr))
            mc.setAttr("scaleObj.scaleY", negScaleAttr)
        
        if (xyz == 3) :
            posScaleAttr = float(mc.getAttr("scaleObj.scaleZ"))
            negScaleAttr = ((-1)*(posScaleAttr))
            mc.setAttr("scaleObj.scaleZ", negScaleAttr)
        
        
        #//on cr閑 un blend shape inverssur l'objet scal
        #mc.select (r = shapeToCopy)
        #mc.select (add = scaleObj)
        
        blendshapeToWrap = originalObj + "_blendShapeToWarp"
        mc.blendShape (shapeToCopy, "scaleObj", frontOfChain = 1, n = blendshapeToWrap)
    
        #//Wrap
        mc.select ( mirrorObj, "scaleObj", r=1) 
        
        wrapName = mm.eval('doWrapArgList "6" { "1","0","1", "2", "1", "1", "0" };')[0]
        #// maya 2008 : doWrapArgList "4" { "1","0","1", "2", "1" }
        
        wrapWrapToMirror = originalObj + "_wrapToMirror"
        mc.rename (wrapName, wrapWrapToMirror)
        mc.setAttr (str(wrapWrapToMirror)+".exclusiveBind", 1)
        
        #valeur blend shape mise 1
        blendShapeAttr = str(blendshapeToWrap)+"." + shapeToCopy
        mc.setAttr(blendShapeAttr, 1)
        
        #delete history de l'objet copi
        mc.select (mirrorObj, r = 1)
        mc.DeleteHistory
        mc.delete (ch = 1)
        
        #suppression des deux objets temporaires
        mc.delete ('scaleObjBase', 'scaleObj')
    
        
        #valeurs de shapeOffset plac閑s ind閜endement dans des variables float
        offsetX = shapeOffset[0]
        offsetY = shapeOffset[1]
        offsetZ = shapeOffset[2]
            
        #//Boutons radios 2 : position relative du shape final :    
        #ShapeTC : ShapeToCopy
        if (shapePosition == 1) :
            shapeTCAttrX = shapeToCopy + ".tx"
            shapeTCAttrY = shapeToCopy + ".ty"
            shapeTCAttrZ = shapeToCopy + ".tz"
            
            shapeTCPositionX = float(mc.getAttr(shapeTCAttrX)) + offsetX
            shapeTCPositionY = float(mc.getAttr(shapeTCAttrY)) + offsetY
            shapeTCPositionZ = float(mc.getAttr(shapeTCAttrZ)) + offsetZ
            
            mirrorObjPositionX = mirrorObj + ".tx"
            mirrorObjPositionY = mirrorObj + ".ty"
            mirrorObjPositionZ = mirrorObj + ".tz"
            
            mc.setAttr (mirrorObjPositionX, shapeTCPositionX)
            mc.setAttr (mirrorObjPositionY, shapeTCPositionY)
            mc.setAttr (mirrorObjPositionZ, shapeTCPositionZ)
            
        
        #para1 : renomme l'objet copien fonction de de la nomenclature de l'utilisateur
        mc.select (mirrorObj, r = 1)
        mirror = mirrorObj.replace(oldName, newName)
    
        #para2 : suppression de la cha頽e de caract鑢es en suffixe temporaire pour emp阠her maya de renommer automatiquement
        mirror2 = mirror.replace("suffTemp", "")
        
        #renomme en fonction rescpectivement de para1 et para2
        mc.rename(mirrorObj, mirror2)
        
        #LZ_MirrorShapesWindow()
    
        '''
        
        
    def replaceMesh_connection(self , orgMesh = '' ,  Origmesh = '' , cloneMehs = '' ):
        #print(Origmesh)
        blendshape_node = self.list_BlendNode(  mesh = Origmesh )
        #print('q'+blendshape_node+'p')
        targets = self.getWeightName( blendShapeNode = blendshape_node )
        ainnode = ['animCurveUU' ,'animCurveUL' ]

        connection_info = []
        for tg in targets:
        
            blendAttr = str(blendshape_node) + '.' +  str(tg) 

            connected_Attr = mc.listConnections( blendAttr , s= True ,d =False , p=True, skipConversionNodes = True )

            if connected_Attr :
                
                sdk_sourceInfo = connected_Attr
                valueAttr = 0

                mc.disconnectAttr( connected_Attr[0]  , blendAttr   )
            else:
                sdk_sourceInfo = None
                valueAttr = mc.getAttr( blendAttr )

            connection_info.append(  [ sdk_sourceInfo , blendshape_node , tg , valueAttr ] )

            mc.setAttr( blendAttr , 0 )
        
        all_cloneMesh = []
        for ci in connection_info :

            blendAttr = str(ci[1] ) + '.' + str(ci[2])
            
            targetMesh_clone = str(ci[2]) + '_clone'

            mc.setAttr( blendAttr , 1  )
            
            wrapMesh = self.LZ_WrapDeformer( originalObj = orgMesh , shapeToCopy =  Origmesh    , newObj = cloneMehs  ) 
            
            mc.rename( wrapMesh , targetMesh_clone )
            mc.setAttr( blendAttr , 0 )
            
            all_cloneMesh.append( targetMesh_clone )

        blendNode_clone = mc.blendShape( all_cloneMesh , cloneMehs )
        
        for ci in connection_info :
            targetMesh_clone = str(ci[2]) + '_clone'
            blendAttr = str(blendNode_clone[0]) + '.' + str(targetMesh_clone) 
            oldblendAttr = str(blendshape_node) + '.' + str(ci[2]) 
            
            
            if ci[0] == None :
                mc.setAttr( blendAttr ,ci[3]   )
                
                mc.setAttr( blendAttr ,ci[3]   )
                mc.setAttr( oldblendAttr ,ci[3]   )
                
            else:
                mc.connectAttr( ci[0][0] ,  blendAttr )
                mc.connectAttr( ci[0][0] ,  oldblendAttr )
                
                
                