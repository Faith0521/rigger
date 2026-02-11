#-*- coding:utf-8 –*-
#/////////////////////////////////////////////////
#// LZ_mirror_blendshape            ///////////////
#//  modified from LZ_MirrorShapesWindow ////////////
#//    by li zhi                   ///////////////
#//      thx Florian Goussin    !  ///////////////
#//       09/04/2014             ///////////////
#/////////////////////////////////////////////////

import maya.cmds as mc
import maya.mel as mm 
class LZ_mirrior_BlendShape():
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
    
    def putOffsetInGray(self,shapeOffset, rb2) :
    
        #Edition du floatFieldGrp shapeToCopy
        if ((mc.radioButtonGrp(rb2, q=1, sl = 1)) == 1) :
            mc.floatFieldGrp (shapeOffset, e = 1, en = 1)
        
        if ((mc.radioButtonGrp(rb2, q=1, sl = 1)) == 2) :       
            mc.floatFieldGrp (shapeOffset, e = 1, en = 0)
    
    def LZ_MirrorShapesWindow(self) :
    
        aimModifier = 0
        upModifier = 0
        worldModifier = 0
    
        if (mc.window("LZ_MirrorShapesWindow", ex = 1 ) ) : mc.deleteUI("LZ_MirrorShapesWindow", window = 1) 
        if(mc.windowPref("LZ_MirrorShapesWindow", ex = 1) ) : mc.windowPref("LZ_MirrorShapesWindow", remove = 1)
    
        mc.window ( "LZ_MirrorShapesWindow",
                    title = "LZ_MirrorShapes",
                    width = 500,
                    height = 300,
                    menuBar = 1,
                    rtf = 0
                )
    
        base = mc.formLayout(numberOfDivisions = 100)
    
        #cr閍tion du textFieldButtonGrp originalObj
        originalObj = mc.textFieldButtonGrp('Original_Obj_TFB',
                            label = "Original Object", 
                            cw3 = (90, 350, 50), 
                            buttonLabel = "<<<"
                            ) 
                            
        #Edition du textFieldButtonGrp originalObj
        mc.textFieldButtonGrp(originalObj,
                    e=1,
                    buttonCommand = lambda *args:self.fillTextFieldOrig('Original_Obj_TFB')
                    )
    
        mc.formLayout (base,
                    e = 1, 
                    attachForm  =  [(originalObj, "left", 5),(originalObj, "top", 5) ]
                )
                
        #---------------------
        target_originalObj = mc.textFieldButtonGrp('Target_Original_Obj_TFB',
                            label = "Original Target", 
                            cw3 = (90, 350, 50), 
                            buttonLabel = "<<<"
                            ) 
                            
        #Edition du textFieldButtonGrp target_originalObj
        mc.textFieldButtonGrp(target_originalObj,
                    e=1,
                    buttonCommand = lambda *args:self.fillTextFieldOrig('Target_Original_Obj_TFB')
                    )
    
        mc.formLayout (base,
                    e = 1, 
                    attachForm  =  [(target_originalObj, "left", 5),(target_originalObj, "top", 31) ]
                )
        #=====================================
        
        #cr閍tion du textFieldButtonGrp  shapeToCopy    
        shapeToCopy = mc.textFieldButtonGrp (
                        label = "Shape(s) to copy", 
                        cw3 = (90, 350, 50),
                        buttonLabel = "<<<" 
                        )
                        
        #Edition du textFieldButtonGrp shapeToCopy
        mc.textFieldButtonGrp (shapeToCopy,
                                e = 1,
                                buttonCommand = lambda *args:self.fillTextFieldShape(shapeToCopy) 
                                )
                                
        mc.formLayout (base,
                    e = 1,
                    attachForm = [(shapeToCopy,"left", 5), (shapeToCopy, "top", 55)]
                    )
    
        rb1 = mc.radioButtonGrp  (
                        numberOfRadioButtons = 3,
                        l = "Mirror Axis : ",
                        labelArray3 = ("X", "Y", "Z"),
                        sl = 1,
                        cw4 = (85,30,30,30),
                        ct4 = ("left", "left", "left", "left") 
                    )
                
                
        mc.formLayout (base,
                    e = 1,
                    attachForm = [(rb1, "top", 80),(rb1, "left", 5)],
                    attachPosition = (rb1, "right", 0, 75)  
                    )
                    
        rb2 = mc.radioButtonGrp  (
                        numberOfRadioButtons = 2,
                        l = "Position of mirrors Shapes : ",
                        labelArray2 = ("Shape", "Original"),
                        sl = 1,
                        cw3 = (200,80,80),
                        ct3 = ("left", "left", "left")
                    )
                
                
        mc.formLayout (base,
                    e = 1,
                    attachForm = [(rb2, "top", 100),(rb2, "left", 5)],
                    attachPosition = (rb1, "right", 0, 75)
                    )       
        
        shapeOffset = mc.floatFieldGrp (
                    label = "==> Duplication Offset (shape mode) : ",
                    numberOfFields = 3,
                    cw4 = (200, 60, 60, 60),
                )
        
                
        mc.formLayout (base,
                    e = 1, 
                    attachForm  = [(shapeOffset,"left", 5),(shapeOffset, "top", 120)]
                )
                
        mc.radioButtonGrp  (rb2,
                        e = 1,
                        cc = lambda *args:self.putOffsetInGray(shapeOffset,rb2)
                    )
    
        #Search and Replace part of name
        #//////////////////////////////////////
        parentLabel = mc.text (
                label = "Replace part of the shape's name you want to copy :"
            )
                
        mc.formLayout (base,
                    e = 1, 
                    attachForm  = [(parentLabel, "left", 5),(parentLabel,"top", 165)],
                    attachPosition  = (parentLabel,"right", 0, 100)
                )
        
        replaceName = mc.textFieldGrp (
                    label = "Replace",
                    cw2 = (60, 200)
                )
                    
        mc.formLayout (base,
                    e = 1, 
                    attachForm  = [(replaceName,"left", 5),(replaceName, "top", 185)]
                )
    
        replaceNameBy = mc.textFieldGrp (
                    label = "by",
                    cw2 = (60, 200)
                    )
                    
        mc.formLayout (base,
                    e = 1, 
                    attachForm  = [(replaceNameBy, "left", 5),(replaceNameBy, "top", 210)]
                )
        #////////////////////////////////////////
        
        FGMail = mc.text (
                label = "294596787@qq.com for help"
            )
                
        mc.formLayout (base,
                    e = 1, 
                    attachForm  = [(FGMail, "left", 300),(FGMail,"top", 210)],
                    attachPosition  = (FGMail,"right", 0, 100)
                )
        
        #Bouton executer
        mirrorButton = mc.button  (
            label = "Mirror Blend Shape(s) !",
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            command = lambda *args:self.LZ_PreMirror(originalObj,target_originalObj,shapeToCopy,rb1,rb2,replaceName,replaceNameBy,shapeOffset) ,
            #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            width = 460,
            height = 32,
            al = "center"
            )
        
        mc.formLayout(base,
                e = 1, 
               attachForm  = [(mirrorButton, "left", 20),(mirrorButton, "top", 240)]
           )
          
        mc.showWindow("LZ_MirrorShapesWindow")
    
    
    def LZ_PreMirror(self,PATHoriginalObj, PATHTgargetoriginalObj ,PATHshapeToCopy, PATHxyz,PATHposition, PATHoldName, PATHnewName, PATHshapeOffset) :
        
        originalObj = mc.textFieldButtonGrp(PATHoriginalObj, q=1, text= 1) 
        tragetORG = mc.textFieldButtonGrp(PATHTgargetoriginalObj, q=1, text= 1) 
        shapeToCopy = mc.textFieldButtonGrp(PATHshapeToCopy, q=1, text= 1) 
        xyz = mc.radioButtonGrp(PATHxyz, q=1, sl = 1)
        shapePosition = mc.radioButtonGrp(PATHposition, q=1, sl = 1)
        oldName = mc.textFieldGrp(PATHoldName, q=1, text= 1)
        newName = mc.textFieldGrp(PATHnewName, q=1, text= 1)
        shapeOffset = mc.floatFieldGrp(PATHshapeOffset, q=1, value = 1)
        #Target_Original_Obj_TFB
        #On enl鑦e les espaces entre chaque objet du tableau
        listShapeToCopy = shapeToCopy.split(" ")
    
        
        if (len(originalObj) == 0) :
            return
        if (len(shapeToCopy) == 0) :
            return
                
        for objToCopy in listShapeToCopy :
            self.LZ_MirrorShapes(originalObj, tragetORG , objToCopy, xyz, shapePosition, oldName, newName, shapeOffset)
            
            
    def LZ_MirrorShapes(self,originalObj,tragetORG , shapeToCopy, xyz, shapePosition, oldName, newName, shapeOffset) :
        
    
        #//unlock attributes if originalMesh is skinned for example
        
        OriginalObjTX = originalObj + ".tx"
        mc.setAttr (OriginalObjTX, lock = 0 )
    
        OriginalObjTY = originalObj + ".ty"
        mc.setAttr (OriginalObjTY, lock = 0 )
    
        OriginalObjTZ = originalObj + ".tz"
        mc.setAttr (OriginalObjTZ, lock = 0)
    
        OriginalObjRX = originalObj + ".rx"
        mc.setAttr (OriginalObjRX ,lock = 0)
    
        OriginalObjRY = originalObj + ".ry"
        mc.setAttr (OriginalObjRY, lock = 0 )
    
        OriginalObjRZ = originalObj + ".rz"
        mc.setAttr (OriginalObjRZ, lock = 0 )
    
        OriginalObjSX = originalObj + ".sx"
        mc.setAttr (OriginalObjSX, lock = 0 )
    
        OriginalObjSY = originalObj + ".sy"
        mc.setAttr (OriginalObjSY, lock = 0 )
    
        OriginalObjSZ = originalObj + ".sz"
        mc.setAttr (OriginalObjSZ, lock = 0)
    
        #//On renomme l'objet dupliqucomme le shape copier, mais avec un suffixe temporaire en plus
        mirrorObj = shapeToCopy + "suffTemp"
        mc.duplicate (originalObj, rr = 1, n = "scaleObj")
        
        if mc.objExists(tragetORG)==True:
            print('tragetORG',tragetORG)
            targeO = tragetORG
        else:
            targeO = originalObj
        mc.duplicate (targeO, rr = 1, n = "tempName")
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
        mc.DeleteHistory()
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
        
        
        return [mirror2]
    #LZ_MirrorShapesWindow()