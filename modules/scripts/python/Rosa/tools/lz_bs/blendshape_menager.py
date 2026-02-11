import maya.cmds as mc
from importlib import reload

from . import LZ_blendshape_command as _LZ_blendshape_command
from . import shapeCorrect as _shapeCorrect
from . import LZ_mirrior_BlendShape as _LZ_mirrior_BlendShape
from . import LZ_wrapDeformer as _LZ_wrapDeformer

# reload(_LZ_blendshape_command)
# reload(_shapeCorrect)
# reload(_LZ_mirrior_BlendShape)
# reload(_LZ_wrapDeformer)

class blendshape_menege(_shapeCorrect.ShapeCorrect,
                        _LZ_mirrior_BlendShape.LZ_mirrior_BlendShape,
                        _LZ_wrapDeformer.LZ_wrapBlend,
                        _LZ_blendshape_command.LZ_blendshape_command
                        ):

    def blendshape_menege_UI(self):
        blendshape_menege_UI = 'blendshape_menege_UI'
        if mc.window(blendshape_menege_UI,ex = True):
            mc.deleteUI(blendshape_menege_UI)
            
        mc.window(blendshape_menege_UI,widthHeight=(400, 250),t='LZ_blendshape_menege_UI_v1.01_2014/04/16',menuBar = True,rtf=True,s=True)
        mc.columnLayout('main_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=400 )
        
        mc.columnLayout('ObjLoad_collayout',columnAttach=('both', 1), rowSpacing=10, columnWidth=390 )
        mc.rowLayout('ObjLoad_rowLY',numberOfColumns=4, columnWidth4=(60,150,40,150), adjustableColumn=4, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)] )
        
        mc.button('loadObj',c=lambda *args:self.loadObj2List01())
        mc.textField('ObjSelLoadTF',ed=True,cc=lambda *args:self.loadObj2List01_changeCommand())
        mc.text('-->>')
        mc.textField('blenshapeName',ed=True,cc=lambda *args:self.loadObj2List01_changeCommand()  )
        
        mc.setParent('main_layout')
        mc.rowLayout('blendList_rowLY',numberOfColumns=3, columnWidth3=(200,40, 150), adjustableColumn=3, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
        
        mc.textScrollList('blendShapeList',allowMultiSelection=True, height =  155,width = 95,dcc=lambda *args:self.selectConnectedObj(),sc=lambda *args:self.showCurrentNodeInfo())
        mc.popupMenu(mm=True)
        mc.menuItem('AppendTarget_menu',l ="Append",rp= "N",c=lambda *args:self.AppendTarget_forUi())
        mc.menuItem('RemoveTarget_menu',l= "Remove",rp ="S",c=lambda *args:self.RemoveTarget())
        mc.menuItem( 'ReplaceTarget_menu',l="Replace",rp ="W",c= lambda *args:self.ReplaceTarget())
        mc.menuItem('RenameTarget_menu',l= "Rename",rp ="E",c=lambda *args:self.renameTargetWin())
        mc.menuItem('ReBuild_Target_menu',l= "ReBuild_Target",rp ="NE",c=lambda *args:self.Rebuild_Target())
        mc.menuItem('normalize_Target_menu',l= "normalize_Target",rp ="NW",c=lambda *args:self.normalize_Target())
        mc.menuItem('select_target',l= "select_Target",rp ="SW",c=lambda *args:self.select_selected_Target())

        
        #mc.textScrollList('blendShapeIndexList',allowMultiSelection=True, height =  155,width = 40,dcc=lambda *args:self.selectConnectedObj(),sc=lambda *args:self.showCurrentNodeInfo())
        mc.textScrollList('blendShape_inbetween_IndexList',allowMultiSelection=True, height =  155,width = 40,dcc=lambda *args:self.select_inbetween_Target())
        mc.popupMenu(mm=True)
        mc.menuItem( 'inbetween_AppendTarget_menu',l="Append",rp ="N",c= lambda *args:self.inbetween_AppendTarget_Ui())
        mc.menuItem( 'inbetween_ReplaceTarget_menu',l="Replace",rp ="W",c= lambda *args:self.ReplaceTarget_forInbetween())
        mc.menuItem('inbetween_ReBuild_Target_menu',l= "ReBuild_Target",rp ="NE",c=lambda *args:self.Rebuild_Target_forInbetween())
        mc.menuItem('RemoveTarget_forInbetweenRemoveTarget_menu',l= "Remove",rp ="S",c=lambda *args:self.RemoveTarget_forInbetween())
        
        
        mc.columnLayout('blendshapeMenage_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=150 )
        
        mc.text('->> blend_Batch_menage <<-')
        mc.button('Got_BlendShapeTarget',h=30)
        mc.button('normalize_BlendShapeName',h=30,c=lambda *args:self.normalize_Target_All())
        mc.button('select_All_Target',h=30,c=lambda *args:self.select_All_Target())
        
        mc.setParent('main_layout')
        
        mc.columnLayout('currentBlendWeightList_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=390 )
        mc.textField('currentBlendWeightList',w=390,ed=False)
        
        mc.button('create  correct shape ',h=30,c=lambda *args:self.correctiveShapeCmd())
        mc.button('Mirror shape Window ',h=30,c=lambda *args:self.LZ_MirrorShapesWindow())
        mc.button('replace connection Window ',h=30,c=lambda *args:self.LZ_WrapDeformer_UI())
        
        #mc.separator (type = 'in')
        #mc.button('export BlendShape ',h=30,c=lambda *args:self.LZ_WrapDeformer_UI())
        #mc.button('import BlendShape ',h=30,c=lambda *args:self.LZ_WrapDeformer_UI())
        
        
        mc.window(blendshape_menege_UI,e=True,widthHeight=(400, 360))
        mc.showWindow()
    
    
    

    
    #==================================================================================================================
    #------------------------------------------------------------------------------------------------------------------
    def inbetween_AppendTarget_Ui(self):
        inbetween_AppendTarget_Ui = 'inbetween_AppendTarget_Ui'
        if mc.window(inbetween_AppendTarget_Ui,ex = True):
            mc.deleteUI(inbetween_AppendTarget_Ui)
            
        mc.window(inbetween_AppendTarget_Ui,widthHeight=(400, 250),t='inbetween_AppendTarget_Ui',menuBar = True,rtf=True,s=True)
        mc.columnLayout('inbetween_AppendTarget_main_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=400 )
        #mc.rowLayout('inbetween_AppendTarget_value_rowLY',numberOfColumns=2, columnWidth4=(60,150,40,150), adjustableColumn=4, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0), (4, 'both', 0)] )
        
        mc.floatSliderGrp( 'inbetween_AppendTarget_main_fsg' ,label=' value : ', field=True, minValue= 1 , maxValue=5, fieldMinValue=-10, fieldMaxValue=10, value=1 ,step =0.1 )

        mc.button( 'inbetween_AppendTarget_main_btn' , l = ' append ' ,c=lambda *args:self.inbetween_AppendTarget_forUi())
        
        mc.showWindow()
    def inbetween_AppendTarget_forUi(self ):
        value = mc.floatSliderGrp( 'inbetween_AppendTarget_main_fsg' ,q=True, value=True  )

        seleObject=mc.ls(sl=True)
        Base_Mesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendshapeNode=mc.textField('blenshapeName',q=True,text=True)
        getWeightName=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        
        for name in getWeightName:
            inputTargetNum= self.getWeightIndex(blendshapeNode,name )-1
        
            self.AppendTarget02(  targets = seleObject  , BlendMesh = Base_Mesh ,blendshape_node = blendshapeNode , value = value ,index = inputTargetNum )
        self.showCurrentNodeInfo()
    
    def normalize_Target_All(self):
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,allItems=True)
        
        self.normalize_Target_Command(OriMesh,blendShapeNode,OriWeight)
    def normalize_Target(self):
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        self.normalize_Target_Command(OriMesh,blendShapeNode,OriWeight)
    '''
    normalize_Target_Command('XXX','XXXX',[])
    '''
    def normalize_Target_Command(self,OriMesh,blendShapeNode,OriWeight):

        errorTarget=[]
        Non_Unique=[]
        finishMesh=[]
        
        for ow in OriWeight:
            connectObj=self.selectConectInputObj_list(blendShapeNode,ow)
            if connectObj==ow:
                pass
            else:
             
                if connectObj=='':
                    errorTarget.append(ow)
                    
                else:
                    if '|' in connectObj:
                        Non_Unique.append(connectObj)
                    else:
                        
                        self.renameTargetWeightName(connectObj,blendShapeNode,ow)
                        finishMesh.append(connectObj)
                
                
        if finishMesh==[]:
            finishMeshText=''
        else:
            finishMeshText=str(finishMesh)+' has finished   '
        
        if errorTarget==[]:
            errorTargetText=''
        else:
            errorTargetText=str(errorTarget)+' has missing Target Mesh   '
            
        if Non_Unique==[]:
            Non_UniqueText=''
        else:
            Non_UniqueText=str(Non_Unique)+' has Non Unique name in scene'

        mc.select(OriMesh)
        self.loadObj2List01()
        mc.textScrollList('blendShapeList',e=True,selectItem=finishMesh)
        mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=finishMeshText+errorTargetText+Non_UniqueText)

    def Rebuild_Target(self):
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        getWeightName=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        #selectValue =mc.textScrollList('blendShape_inbetween_IndexList',q=True, si=True)
        
        FailObj=[]
        failInfo=0
        for target in getWeightName:
            getWeightInedex=self.getWeightIndex(blendShapeNode,target)
            all_index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendShapeNode , tragetIndexItem = getWeightInedex-1  )
            
            for aii in all_index_inbetween:
                info_source = self.checkConnectObj_ifExists( blendshape = blendShapeNode , target = target , index = aii )
            
                if info_source:
                    FailObj.append( (target,aii ) )
                    mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='the target of '+str(FailObj)+' has already existed in current secne ')
                else:
                    self.getTargetInputMesh(OriMesh,blendShapeNode,target,aii )
                    mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='rebuild Target Successed')

    def Rebuild_Target_forInbetween(self):
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        getWeightName=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        selectValue =mc.textScrollList('blendShape_inbetween_IndexList',q=True, si=True)
        
        FailObj=[]
        failInfo=0
        for target in getWeightName:
            
            info_source = self.checkConnectObj_ifExists( blendshape = blendShapeNode , target = target , index = selectValue )
            
            if info_source:
                FailObj.append( (target,selectValue ) )
                mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='the target of '+str(FailObj)+' has already existed in current secne ')
            else:
                self.getTargetInputMesh(OriMesh,blendShapeNode,target,selectValue[0] )
                mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='rebuild Target Successed')

    def select_All_Target(self):
        AllTarget=self.listAllTarget_forUi()
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        sourceObjInput=[]
        failInput=[]
        for at in AllTarget:
            objInput=self.selectConectInputObj_list(blendShapeNode,at)
            if objInput:
                if objInput!=0 :
                    #print(objInput)
                    for oi in objInput:
                       if mc.objExists(oi) == 1:
                           sourceObjInput.append(oi)
                       else:
                           failInput.append(at)
        #print(sourceObjInput)
        mc.select(sourceObjInput)
        
        listInfo=str(sourceObjInput)+' has selected,   '+str(failInput)+' missed target'
        if failInput==[]:
            colorGetBack=[0,0.65,0]
        else:
            colorGetBack=[0.9,0,0.5]
        
        mc.textField('currentBlendWeightList',e=True,bgc=colorGetBack,text=listInfo)
        
        
    def select_selected_Target(self):
    
        
    
        AllTarget = mc.textScrollList('blendShapeList', q =True ,selectItem = True)
    
        #AllTarget=self.listAllTarget()
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        sourceObjInput=[]
        failInput=[]
        #print(AllTarget)
        for at in AllTarget:
            
            
            objInput=self.selectConectInputObj_list(blendShapeNode,at)
            
            #print(objInput)
            if objInput != 0:
                for oi in objInput:
                   if mc.objExists(oi) == True:
                       sourceObjInput.append(oi)
                   else:
                       failInput.append(at)
        #print(sourceObjInput)
        #print(sourceObjInput)
        mc.select(sourceObjInput)
        
        listInfo=str(sourceObjInput)+' has selected,   '+str(failInput)+' missed target'
        if failInput==[]:
            colorGetBack=[0,0.65,0]
        else:
            colorGetBack=[0.9,0,0.5]
        
        mc.textField('currentBlendWeightList',e=True,bgc=colorGetBack,text=listInfo)
    
    def select_inbetween_Target(self):
    
        
    
        AllTarget = mc.textScrollList('blendShapeList', q =True ,selectItem = True)
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        indexCurrent_inbetween = mc.textScrollList('blendShape_inbetween_IndexList',q=True , selectItem =True )
        
        
        value = int(float(indexCurrent_inbetween[0])*1000 + 5000)
        
        if len(AllTarget) ==1:
            
            sourceObjInput =[]
            failInput=[]
            inputTargetNum= self.getWeightIndex(blendShapeNode,AllTarget[0])-1
            #InputTargetItemNum=self.getTargetInputTargetItem(blendShapeNode,inputTargetNum)
            conneSouce=mc.listConnections(str(blendShapeNode)+'.inputTarget[0].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem['+str(value)+'].inputGeomTarget',s=True)
            
            #objInput = self.selectConectInputObj_list(blendShapeNode,AllTarget)
            if conneSouce:
                if mc.objExists(conneSouce[0]) == True:
                
                    sourceObjInput=(conneSouce[0],indexCurrent_inbetween[0])
                    
                    mc.select(sourceObjInput[0])
                
                else:
                    failInput.append(indexCurrent_inbetween[0])
                    
                    
                    
            else:
                    failInput.append(indexCurrent_inbetween[0])
                    #pass
                
            listInfo=str(sourceObjInput)+' has selected,   '+str(failInput)+' missed target'
            if failInput==[]:
                colorGetBack=[0,0.65,0]
            else:
                colorGetBack=[0.9,0,0.5]
            
            mc.textField('currentBlendWeightList',e=True,bgc=colorGetBack,text=listInfo)
            

    def selectConnectedObj(self):
        blendShapeNode=mc.textField('blenshapeName',q=True,text=True)
        getWeightName=mc.textScrollList('blendShapeList',q=True,selectItem=True)[0]

        objsource=self.selectConectInputObj_list(blendShapeNode,getWeightName)
        
        if objsource !=0:
            mc.select(objsource)
            mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='selected '+str(objsource))
        else:
            mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='the source blendShape target has missed ')
    
    
        
    def AppendTarget_forUi(self):
        seleObject=mc.ls(sl=True)
        Base_Mesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        blendshapeNode=mc.textField('blenshapeName',q=True,text=True)
        #print(seleObject )
        #print(Base_Mesh )
        #print(blendshapeNode )
        lastIndex=self.findLastIndex(blendshapeNode)
        self.AppendTarget(  targets = seleObject , BlendMesh = Base_Mesh ,blendshape_node = blendshapeNode )#, value = 1 ,index = lastIndex 
        self.refreshList(blendshapeNode)

    def refreshWinShow(self):
        mc.button('rename_Targets',e=True,en=False)
        self.refreshUI()
    
    def refreshUI(self):
        child_LYs=mc.columnLayout('renameTargetWinmain_layout',q=True, ca=True )
        blendshape=mc.textField('blenshapeName',q=True,text=True)
        for cdl in child_LYs:
            
            RL_Mems = mc.rowLayout(cdl,q=True, ca=True )
            OriWeight=mc.textField(RL_Mems[1],q=True,text=True)
            newNameWeight=mc.textField(RL_Mems[0],q=True,text=True)
            
            mc.textField(RL_Mems[0],e=True,text=OriWeight)
            mc.textField(RL_Mems[1],e=True,ed=True)
            mc.textField(RL_Mems[1],e=True,bgc=[0,0,0])
            
            
        mc.button('rename_Targets',e=True,en=True)
    def ReplaceTarget(self):
        objsel=mc.ls(sl=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        #index_Inbetween = mc.textScrollList('blendShape_inbetween_IndexList',q=True ,si =True )
        
        if len(OriWeight)==len(objsel):
            #print(len(objsel))
            for num in range(len(objsel)):
                #print(objsel[num],OriWeight[num])
                
                self.RebuildTarget(objsel[num],OriWeight[num] , inbetweenValue = 1 )

            mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=' finish replaced   ')
        else:
            mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text=' the count of selected is not equal the count of list ')
    
    def ReplaceTarget_forInbetween(self):
        objsel=mc.ls(sl=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        index_Inbetween = mc.textScrollList('blendShape_inbetween_IndexList',q=True ,si =True )
        #print(index_Inbetween)
        if len(OriWeight)==len(objsel):
            #print(len(objsel))
            for num in range(len(objsel)):
                #print(objsel[num],OriWeight[num])
                
                self.RebuildTarget(objsel[num],OriWeight[num] , inbetweenValue = index_Inbetween[0] )

            mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=' finish replaced   ')
        else:
            mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text=' the count of selected is not equal the count of list ')
    
    
    
    def RebuildTarget(self,TargetMesh,target , inbetweenValue = 1 ):
        #newNameWeight='blendshapeNeedDelete_target'
        blendshape=mc.textField('blenshapeName',q=True,text=True)

        #OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)

        #for target in OriWeight:

        TargetIndex=self.getWeightIndex(blendshape,target)
        #print(OriMesh,TargetMesh,TargetIndex,TargetIndex)

        self.RebuildTargetConnect(OriMesh,TargetMesh,blendshape,TargetIndex , inbetweenIndex  = inbetweenValue )
        

    def renameTarget(self):
        child_LYs=mc.columnLayout('renameTargetWinmain_layout',q=True, ca=True )
        blendshape=mc.textField('blenshapeName',q=True,text=True)
        for cdl in child_LYs:
            
            RL_Mems = mc.rowLayout(cdl,q=True, ca=True )
            OriWeight=mc.textField(RL_Mems[0],q=True,text=True)
            newNameWeight=mc.textField(RL_Mems[1],q=True,text=True)
            mc.textField(RL_Mems[1],e=True,ed=False)
            mc.textField(RL_Mems[1],e=True,bgc=[0,0.65,0])
            

            self.renameTargetWeightName(newNameWeight,blendshape,OriWeight)
            
        self.refreshList(blendshape)
            
        mc.button('rename_Targets',e=True,en=False)
        mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=' finish renamed  ')
    def renameTargetWin(self):
        renameTargetWin = 'renameTargetWin'
        if mc.window(renameTargetWin,ex = True):
            mc.deleteUI(renameTargetWin)
            
        mc.window(renameTargetWin,widthHeight=(300, 300),t='renameTargetWin',menuBar = True,rtf=True,s=True)
        mc.columnLayout('renameTarget_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=300 )
        mc.columnLayout('renameTargetWinmain_layout',columnAttach=('both', 1), rowSpacing=10, columnWidth=300 )
        #mc.rowLayout('renameTargetWinmain_rowLY',numberOfColumns=2, columnWidth2=(100,100), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
        targetAll=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        for ta in targetAll:
            mc.setParent('renameTargetWinmain_layout')
            mc.rowLayout(ta+'_rowLY',parent='renameTargetWinmain_layout',numberOfColumns=2, columnWidth2=(150,150), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )

            mc.textField(ta+'_TF',text=ta,ed=False)
            mc.textField(ta+'_RN',text='')
        mc.setParent('renameTarget_layout')
        mc.button('rename_Targets',c=lambda *args:self.renameTarget())
        mc.button('refresh_UI_show',c=lambda *args:self.refreshWinShow())
        
        
        
        mc.window(renameTargetWin,e=True,widthHeight=(300, 300))
        mc.showWindow(renameTargetWin)
    def RemoveTarget(self):
        ##    mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='there is no target is selected ,one target at last is selected in textScrollList')
        newNameWeight='blendshapeNeedDelete_targetTemple'
        blendshape=mc.textField('blenshapeName',q=True,text=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)

        for ow in OriWeight:
        
            getWeightInedex=self.getWeightIndex(blendshape,ow)
            #print(getWeightInedex)
            self.renameTargetWeightName(newNameWeight,blendshape,ow)
            
            all_index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendshape , tragetIndexItem = getWeightInedex-1  )
            
            for aii in all_index_inbetween:
                #print( ow,aii)
                info_source = self.checkConnectObj_ifExists( blendshape = blendshape , target = newNameWeight , index = aii )
             
                newTarget = newNameWeight+'_'+str( int(float(aii))  *1000)
                mc.duplicate(OriMesh,n=newTarget )

                self.refreshList(blendshape)
            

                self.RebuildTarget(newTarget,newNameWeight, inbetweenValue = aii)
                mc.blendShape(blendshape,e=True,rm=True,t=[OriMesh,getWeightInedex,newTarget,aii] , topologyCheck = False )
            
                mc.delete(newTarget)
                self.refreshList(blendshape)
            
        
        mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=str(OriWeight)+' has removed from '+blendshape)
    
    def RemoveTarget_forInbetween(self):
        ##    mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='there is no target is selected ,one target at last is selected in textScrollList')
        newNameWeight='blendshapeNeedDelete_targetTemple'
        blendshape=mc.textField('blenshapeName',q=True,text=True)
        OriWeight=mc.textScrollList('blendShapeList',q=True,selectItem=True)
        OriMesh=mc.textField('ObjSelLoadTF',q=True,text=True)
        index_Inbetween = mc.textScrollList('blendShape_inbetween_IndexList',q=True ,si =True )
        

        for ow in OriWeight:
        
            getWeightInedex=self.getWeightIndex(blendshape,ow)
            #print(getWeightInedex)
            #self.renameTargetWeightName(newNameWeight,blendshape,ow)
            
            all_index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendshape , tragetIndexItem = getWeightInedex-1  )
            
            for aii in all_index_inbetween:
                #print( ow,aii)
                #print(float(index_Inbetween[0]) , aii )
                if float(index_Inbetween[0]) == aii:
                    #print('ok')
                    info_source = self.checkConnectObj_ifExists( blendshape = blendshape , target = ow , index = aii )
                    
                    newTarget = ow+'_'+str( int(float(aii))  *1000)
                    mc.duplicate(OriMesh,n=newTarget )
                    
                    self.refreshList(blendshape)
                    
                    
                    self.RebuildTarget(newTarget,ow, inbetweenValue = aii)
                    #print([OriMesh,getWeightInedex,newTarget,aii])
                    mc.blendShape(blendshape,e=True,rm=True,t=[OriMesh,getWeightInedex,newTarget,aii] , topologyCheck = False )
                    
                    mc.delete(newTarget)
                    self.refreshList(blendshape)
                    
        
        mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=str(OriWeight)+' has removed from '+blendshape)
        self.refreshList(blendshape)
    
    
    
    def refreshList(self,blendshapeNode):
        targetName=self.getWeightName(blendshapeNode)
        selectedII=mc.textScrollList('blendShapeList',q=True,selectIndexedItem=True)
        mc.textScrollList('blendShapeList',e=True, ra=True)

        for tn in targetName:
            mc.textScrollList('blendShapeList',e=True, a =tn)
        #if selectedII!=None:  
        #    print('selectedII',selectedII)
        #    mc.textScrollList('blendShapeList',e=True,selectIndexedItem=int(selectedII[0]))
    def showCurrentNodeInfo(self):
        blendshape=mc.textField('blenshapeName',q=True,text=True)
        getWeightName=mc.textScrollList('blendShapeList',q=True,selectItem=True)[0]
        getWeightInedex=self.getWeightIndex(blendshape,getWeightName)
        #print(getWeightName)
        mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0.9,0.3],text='Weight name :  '+ blendshape + ' ;' + 'Weight Index : '+ str(getWeightInedex))
        #print(getWeightInedex)
        index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendshape , tragetIndexItem = getWeightInedex-1  )
        
        mc.textScrollList('blendShape_inbetween_IndexList',e =True , removeAll =True )
        
        for i in index_inbetween:
            #mc.textScrollList('blendShape_inbetween_IndexList',allowMultiSelection=True, height =  155,width = 40,dcc=lambda *args:self.selectConnectedObj(),sc=lambda *args:self.showCurrentNodeInfo())
            
            mc.textScrollList('blendShape_inbetween_IndexList',e =True , append=str(i) , sii = 1 )
    
    def loadObj2List01(self):
        objsel=mc.ls(sl=True)[0]
        mc.textField('ObjSelLoadTF',e=True,text=objsel)
        blendshapeNode=self.list_BlendNode( mesh  = objsel )
        if blendshapeNode==None:
            mc.textField('currentBlendWeightList',e=True,bgc=[0.9,0,0],text='the object selected has no a node which type is "blendShape"')
        else:
            mc.textField('blenshapeName',e=True,text=blendshapeNode)
        
            targetName=self.getWeightName(blendshapeNode)
        
            mc.textScrollList('blendShapeList',e=True, ra=True)
            num = 1
            for tn in targetName:
                getWeightInedex=self.getWeightIndex(blendshapeNode,tn)
                index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendshapeNode , tragetIndexItem = getWeightInedex-1  )
                if index_inbetween:
                    mc.textScrollList('blendShapeList',e=True, appendPosition =[ num , tn ])
                
                num = num+1
                
            mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=' the first blendShape is '+str(blendshapeNode))
    def loadObj2List01_changeCommand(self):

        objsel = mc.textField('ObjSelLoadTF',q=True,text=True)
        blendshapeNode=mc.textField('blenshapeName',q=True,text=True)
        
        targetName=self.getWeightName(blendshapeNode)
        
        mc.textScrollList('blendShapeList',e=True, ra=True)
        num = 1
        for tn in targetName:
            getWeightInedex=self.getWeightIndex(blendshapeNode,tn)
            index_inbetween = self.getBlend_inbetween_IndexList(  blendNode = blendshapeNode , tragetIndexItem = getWeightInedex-1  )
            if index_inbetween:
                mc.textScrollList('blendShapeList',e=True, appendPosition =[ num , tn ])
            
            num = num+1
            
        mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text=' the first blendShape is '+str(blendshapeNode))

    def listAllTarget_forUi(self):
        blendshapeNode=mc.textField('blenshapeName',q=True,text=True)
        AllTargets = mc.textScrollList('blendShapeList',q=True, ai =True )
        return AllTargets
        
    
