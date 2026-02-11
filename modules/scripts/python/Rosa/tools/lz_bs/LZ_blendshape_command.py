import maya.cmds as mc
import maya.mel as mm

class LZ_blendshape_command(object):
    def __init__(self):
        print('update succese3')

    def AppendTarget02(self , targets = [''] , BlendMesh = '',blendshape_node = '' , value = 1 ,index = 0 ):
        seleObject = targets
        textResult01=''
        textResult02=''
        textResult=''
        
        blendhspae_is_inscence = mc.objExists(blendshape_node)
        if blendhspae_is_inscence == 1 :
            blendshape_exists = self.list_BlendNode( mesh = BlendMesh )
            #print(blendshape_exists)
            #print(blendshape_exists)
            if blendshape_exists != None:
            
                if seleObject==None:
                    pass
                else:
                    BaseMesh= BlendMesh 
                    feedback01=1
                    feedback02=1
                    blendshapeNode = blendshape_exists
                    for so in seleObject:
                        
                        if so in self.LZ_listAllTarget(blendshapeNode):
                            textResult02='there is some meshs has already existed in '+str(blendshapeNode)
                            feedback02=0
                        
                            
                                
                        else:
                            if so!= BaseMesh:
                
                                #lastIndex=self.findLastIndex(blendshapeNode)
                                
                                mc.blendShape(blendshapeNode,e=True,tc=True,t=[BaseMesh,index,so, value ], topologyCheck = False)
                                
                
                                
                            else:
                                
                                #mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='please select one mesh which name is not '+str(BaseMesh)+' at last')
                                feedback01=0
                                #mc.select(so)
                                #pass 
                    if feedback01==1:
                        
                        if feedback02==1:
                            textResult=str(seleObject)+'has appended to the '+str(blendshapeNode)+str(index)
                            #backGroundColor=[0,0.65,0]
                        else:
                            textResult=textResult01 + textResult02 + ',the others continued'
                            #backGroundColor=[0.9,0,0.5]
                    else:
                        textResult01='there is a mesh selected named '+str(BaseMesh)
                        textResult=textResult01 + textResult02 + ',the others continued'
                        #backGroundColor=[0.9,0,0.5]
                
                
                    #mc.textField('currentBlendWeightList',e=True,bgc=backGroundColor,text=textResult)   
                    #print( textResult )
            else:
                print( blendshape_node+ 'is not a input node on the mesh of '+ BlendMesh)
        else:
            mc.blendShape( targets , BlendMesh ,n= blendshape_node , frontOfChain =True , topologyCheck = False)
                
    def AppendTarget(self , targets = [''] , BlendMesh = '',blendshape_node = ''):
        seleObject = targets
        textResult01=''
        textResult02=''
        textResult=''
        
        blendhspae_is_inscence = mc.objExists(blendshape_node)
        if blendhspae_is_inscence == 1 :
            blendshape_exists = self.list_BlendNode( mesh = BlendMesh )
            #print(blendshape_exists)
            #print(blendshape_exists)
            if blendshape_exists != None:
            
                if seleObject==None:
                    pass
                else:
                    BaseMesh= BlendMesh 
                    feedback01=1
                    feedback02=1
                    blendshapeNode = blendshape_exists
                    for so in seleObject:
                        
                        if so in self.LZ_listAllTarget(blendshapeNode):
                            textResult02='there is some meshs has already existed in '+str(blendshapeNode)
                            feedback02=0
                        
                            
                                
                        else:
                            if so!=BaseMesh:
                
                                lastIndex=self.findLastIndex(blendshapeNode)
                                
                                mc.blendShape(blendshapeNode,e=True,tc=True,t=[BaseMesh,lastIndex,so,1], topologyCheck = False)
                                
                
                                
                            else:
                                
                                #mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='please select one mesh which name is not '+str(BaseMesh)+' at last')
                                feedback01=0
                                #mc.select(so)
                                #pass 
                    if feedback01==1:
                        
                        if feedback02==1:
                            textResult=str(seleObject)+'has appended to the '+str(blendshapeNode)+str(lastIndex)
                            #backGroundColor=[0,0.65,0]
                        else:
                            textResult=textResult01 + textResult02 + ',the others continued'
                            #backGroundColor=[0.9,0,0.5]
                    else:
                        textResult01='there is a mesh selected named '+str(BaseMesh)
                        textResult=textResult01 + textResult02 + ',the others continued'
                        #backGroundColor=[0.9,0,0.5]
                
                
                    #mc.textField('currentBlendWeightList',e=True,bgc=backGroundColor,text=textResult)   
                    #print( textResult )
            else:
                print( blendshape_node+ 'is not a input node on the mesh of '+ BlendMesh)
        else:
            mc.blendShape( targets , BlendMesh ,n= blendshape_node , frontOfChain =True , topologyCheck = False)
                
                  
    '''     


    '''    
    
    def AppendTarget_02(self , targets = [''] , BlendMesh = '',blendshape_node = ''):
        seleObject = targets
        textResult01=''
        textResult02=''
        textResult=''
        
        blendhspae_is_inscence = mc.objExists(blendshape_node)
        if blendhspae_is_inscence == 1 :
            blendshape_exists = self.list_BlendNode( mesh = BlendMesh )
            #print(blendshape_exists)
            #print(blendshape_exists)
            if blendshape_exists != None:
            
                if seleObject==None:
                    pass
                else:
                    BaseMesh= BlendMesh 
                    feedback01=1
                    feedback02=1
                    blendshapeNode = blendshape_exists
                    for so in seleObject:
                        
                        if so in self.LZ_listAllTarget(blendshapeNode):
                            textResult02='there is some meshs has already existed in '+str(blendshapeNode)
                            feedback02=0
                        
                            
                                
                        else:
                            if so!=BaseMesh:
                
                                lastIndex=self.findLastIndex(blendshapeNode)
                                
                                mc.blendShape(blendshapeNode,e=True,tc=True,t=[BaseMesh,lastIndex,so,1] , topologyCheck = False )
                                
                
                                
                            else:
                                
                                #mc.textField('currentBlendWeightList',e=True,bgc=[0,0.65,0],text='please select one mesh which name is not '+str(BaseMesh)+' at last')
                                feedback01=0
                                #mc.select(so)
                                #pass 
                    if feedback01==1:
                        
                        if feedback02==1:
                            textResult=str(seleObject)+'has appended to the '+str(blendshapeNode)+str(lastIndex)
                            #backGroundColor=[0,0.65,0]
                        else:
                            textResult=textResult01 + textResult02 + ',the others continued'
                            #backGroundColor=[0.9,0,0.5]
                    else:
                        textResult01='there is a mesh selected named '+str(BaseMesh)
                        textResult=textResult01 + textResult02 + ',the others continued'
                        #backGroundColor=[0.9,0,0.5]
                
                
                    #mc.textField('currentBlendWeightList',e=True,bgc=backGroundColor,text=textResult)   
                    #print( textResult )
            else:
                print( blendshape_node+ 'is not a input node on the mesh of '+ BlendMesh)
        else:
            mc.blendShape( targets , BlendMesh ,n= blendshape_node , frontOfChain =True , topologyCheck = False )
        
    def list_BlendNode(self , mesh = '' ):
        
        blendMember = 0
        blendShapes=[]
        input = mc.listHistory(mesh)   
        for ip in input:
            if mc.nodeType(ip) == 'blendShape':
                blendMember = blendMember + 1
                blendShapes.append(ip)
            else:
                pass
        
        if blendMember >= 1:
            return blendShapes[0]
        elif blendMember == 0:
             return None
    
    
    def LZ_listAllTarget(self,blendShape_node):
        
        blendshapeNode = blendShape_node
        getWeightName = self.getWeightName(blendshapeNode)
        
        return getWeightName
        
        
    def listAllTarget(self,blendShape_node):
        
        blendshapeNode=blendShape_node
        getWeightName=self.getWeightName(blendshapeNode)
        
        return getWeightName
    '''
    getTargetInputTargetItem ( string , int )
    
    get the value like 6000    get (int)
    '''
    def getTargetInputTargetItem(self,blendShapeNode,inputTargetNum):
        InputTargetItem=mc.getAttr(str(blendShapeNode)+'.inputTarget[0].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem' ,mi=True)
        return InputTargetItem
    '''
    getWeightIndex(string,string)
    get the index of the weight input    get (int)
    
    ''' 
    def getWeightIndex(self,blendShapeNode,target):
        aliases=mc.aliasAttr(blendShapeNode,q=True)
        #print(target)
        for i in range(len(aliases)):
            if target==aliases[i]:
                index=(aliases[i+1].split('[')[1]).split(']')[0]
                
                index=int(index)+1
                break
            else:
                index='something mistake has Occurred'

        return index
    '''
    getWeightName(string)
    get the weight names in the blendShape input
    
    '''
    ####def getWeightName(self,blendShapeNode):
    ####    aliases=mc.aliasAttr(blendShapeNode,q=True)
    ####    blendshapeTarget=[]
    ####    for bt in range(len(aliases)/2):
    ####        blendshapeTarget.append(aliases[bt*2])
    ####    return(blendshapeTarget)
    '''
    getWeightName(string)
    get the weight names in the blendShape input
    
    '''
    def getWeightName(self,blendShapeNode):
        aliases=mc.aliasAttr(blendShapeNode,q=True)
        blendshapeTarget={}
        for bt in range(len(aliases)//2):
            blendshapeTarget[aliases[bt*2+1]] = aliases[bt*2]
            
        num_blendtarget = blendshapeTarget.keys()
        
        allnum = []
        for keys  in num_blendtarget:
        
            split01 = str(keys).split('[')[1]
            split02 = str(split01).split(']')[0]
            
            allnum.append(int(split02))
        
        listBlend = {}
        for num in allnum:
            
            times = 0
            for set in allnum:
                
                if set < num:
                    times = times+1
                    
                    
            listBlend[str(times)] = blendshapeTarget.get('weight['+str(num) +']' )
        
        blendshapeTarget_all = []
        for n in  range(len(allnum)):
            
            blendshapeTarget_all.append(listBlend[str(n)]) 
            

        return(blendshapeTarget_all)
    
    
     
        
    def findLastIndex(self,blendShapeNode):
        aliases=mc.aliasAttr(blendShapeNode,q=True)
        index=1
        for i in range(len(aliases)/2):
            currentIndex=int((aliases[i*2+1].split('[')[1]).split(']')[0])+1
            if currentIndex>index:
                index=currentIndex
        return(index)
        #i =len(aliases)/2-1
        #index=int((aliases[i*2+1].split('[')[1]).split(']')[0])+1
        #return(int(index))
        #
    def getBlendshapeNode(self,obj=''):
        blendNode=''
        for leave in range(6):
            
        
            nodeHistory=mc.listHistory(obj,lv=leave+1)

            for i in nodeHistory:
                #print (i)
                if mc.nodeType(i)=='blendShape':
                    blendNode=i
            if blendNode!='':
                break
        return(blendNode)
        
    def LZ_getBlendshapeNode(self,obj=''):
        blendNode=''
        for leave in range(6):
            
        
            nodeHistory=mc.listHistory(obj,lv=leave+1)

            for i in nodeHistory:
                #print (i)
                if mc.nodeType(i)=='blendShape':
                    blendNode=i
            if blendNode!='':
                break
        return(blendNode)
        
        
    def renameTargetWeightName(self,newName,blendshapenode,targetWeight):
        
        mc.aliasAttr(newName,str(blendshapenode)+'.'+str(targetWeight))
    
    '''
    
    RebuildTargetConnect(string,string,string,int)
    
    reconnect the target and blendShape weight
    
    '''
    def RebuildTargetConnect(self,OriMesh,TargetMesh,blendshape,TargetIndex, inbetweenIndex = 1):

        getOriMeshShapes_all=mc.listRelatives(OriMesh,s=True)
        getTargetMeshShapes=mc.listRelatives(TargetMesh,s=True)
        #print(getOriMeshShapes)
        
        getOriMeshShapes= []
        for gom in getOriMeshShapes_all:
            #if 'Orig' in gom:
            #    print(  gom )
            #    getOriMeshShapes.remove(gom)
            source = mc.listConnections( str( gom )+'.inMesh' ,s=True , p=False ,d=False )
            #print(source , gom )
            if source:
                #if mc.nodeType(source[0]) == 'blendShape':

                getOriMeshShapes.append( gom )
                    
                #else:
                #    #getOriMeshShapes.remove(gom)
                #    pass
            else:
                #getOriMeshShapes.remove(gom)
                pass
            
            
            
        #print(getTargetMeshShapes)
        newTarList = []
        for gtm in getTargetMeshShapes:
            if 'Orig' in gtm:
                  
                #getTargetMeshShapes.remove(gtm)
                pass
            else:
            
                newTarList.append( gtm )
            #print( 'gtm' , gtm )    
            #source = mc.listConnections( str( gtm )+'.inMesh' ,s=True , p=False ,d=False )
            #if source:
            #    if mc.nodeType(source[0]) == 'blendShape':
            #        pass
            #        
            #    else:
            #        getTargetMeshShapes.remove(gtm)
            #        
            #else:
            #    getTargetMeshShapes.remove(gtm)
            #    
                
                
        #print(getOriMeshShapes)
        #print(getTargetMeshShapes)
        getTargetMeshShapes = newTarList
        #print('getOriMeshShapes',getOriMeshShapes)
        #print('getTargetMeshShapes',getTargetMeshShapes)
        if len(getOriMeshShapes)==len(getTargetMeshShapes):

            for i in range(len(getOriMeshShapes)):
                if 'Orig' in getTargetMeshShapes[i]:
                    pass
                else:
                    inputTargetNum=int(TargetIndex)-1
                    
                    #InputTargetItemNum=self.getTargetInputTargetItem(blendshape,inputTargetNum)
                    InputTargetItemNum = int(float(inbetweenIndex)*1000) +5000
                    connecteAttr=str(blendshape)+'.inputTarget['+str(i)+'].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem['+str(InputTargetItemNum)+'].inputGeomTarget'
                    sourceInput=str(getTargetMeshShapes[i])+'.worldMesh[0]'
                    
                    sourceMesh=mc.listConnections(connecteAttr,s=True)
                    print(sourceMesh)
                    if sourceMesh!=None:
                        sourceMeshShapes=mc.listRelatives(sourceMesh,s=True)
                        mc.disconnectAttr(str(sourceMeshShapes[i])+'.worldMesh[0]', connecteAttr)

                    mc.connectAttr(sourceInput,connecteAttr)
                    print('ok')
    '''
    selectConectInputObj(string,sting)
    select the object which is the target of blendShape

    ''' 
    def selectConectInputObj(self,blendShapeNode,getWeightName):
        inputTargetNum=self.getWeightIndex(blendShapeNode,getWeightName)-1
        InputTargetItemNum=self.getTargetInputTargetItem(blendShapeNode,inputTargetNum)
    
        conneSouce=mc.listConnections(str(blendShapeNode)+'.inputTarget[0].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem['+str(InputTargetItemNum[0])+'].inputGeomTarget',s=True)
        if conneSouce!=None:
            return conneSouce[0]
            
        else:
            return 0
    
    def selectConectInputObj_list(self,blendShapeNode,getWeightName):
        inputTargetNum=self.getWeightIndex(blendShapeNode,getWeightName)-1
        InputTargetItemNum=self.getTargetInputTargetItem(blendShapeNode,inputTargetNum)
        #print( getWeightName,inputTargetNum,InputTargetItemNum)
        selectSource = []
        for it in InputTargetItemNum:
            conneSouce=mc.listConnections(str(blendShapeNode)+'.inputTarget[0].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem['+str(it)+'].inputGeomTarget',s=True)
            if conneSouce!=None:
                #return conneSouce[0]
                #print(conneSouce)
                selectSource.append(conneSouce[0])
            else:
                pass
        if selectSource ==[]:
            return 0
        else:
            return selectSource
    
    def checkConnectObj_ifExists(self ,blendshape = '' , target = '' , index = 1.0):
        
        
        inputTargetNum=self.getWeightIndex(blendshape,target)-1
        #print('inputTargetNum',inputTargetNum)
        InputTargetItemNum=self.getTargetInputTargetItem(blendshape,inputTargetNum)
        
        for it in InputTargetItemNum:
            valueIndex = float((int(it) -5000))/1000
            if  index == valueIndex:
                conneSouce=mc.listConnections(str(blendshape)+'.inputTarget[0].inputTargetGroup['+str(inputTargetNum)+'].inputTargetItem['+str(it)+'].inputGeomTarget',s=True)
                if conneSouce:
                    print(conneSouce)
                    return conneSouce[0]
                    
                else:
                    return None
        
    
    
    ####def getInex_listInBetween(self ,  blendshapeNode = '' , index = 1 ):
    ####    
    ####    inputTargetItem = cmds.getAttr(blendShape[0]+'.inputTarget[0].inputTargetGroup[%d].inputTargetItem' %tragetIndexItem ,mi=True)
    ####
    
    def getBlend_inbetween_IndexList(self, targetNum = 0, blendNode = '' , tragetIndexItem = 1  ):
        #print('tragetIndexItem',tragetIndexItem)
        inputTargetItem = mc.getAttr(str(blendNode) +'.inputTarget['+ str(targetNum) + '].inputTargetGroup[%d].inputTargetItem' %tragetIndexItem ,mi=True)
        
        #cmds.textScrollList('targetInbetweenText',edit = True,removeAll = True)
        
        allIndex = []
        #print(inputTargetItem)
        if inputTargetItem:
            for i in inputTargetItem:
                indexInt = (int(i)-5000)/1000.0
                #cmds.textScrollList('targetInbetweenText',edit=True,append=str(indexInt),sii=1)
                #cmds.textFieldButtonGrp('MirrorTargetText',label=tragetBlendShapeIndex +' >>',edit=True)
                allIndex.append(indexInt)
            
            return  allIndex   
        else:
            return None
        #print(allIndex)
    
    
    def setAllTargetWeight2Off(self,blendshape):
        AllTargets=self.getWeightName(blendshape)
        for at in AllTargets:
            mc.setAttr(str(blendshape)+'.'+str(at),0)
    def setTargetWeight2On(self,blendshape,target , value = 1):
        mc.setAttr(str(blendshape)+'.'+str(target),value)
    def getTargetInputMesh(self,OriMesh='',blendshape='',target='' , inbtweenIndex = 1 ):
        
        self.setAllTargetWeight2Off(blendshape)
        
        self.setTargetWeight2On(blendshape,target, value = float(inbtweenIndex) )
        TargetIndex=self.getWeightIndex(blendshape,target)
        #print( float(inbtweenIndex) )
        targetMesh = target+'_'+str( int(float(inbtweenIndex) *1000))
        mc.duplicate(OriMesh,n=targetMesh)
        
        self.RebuildTargetConnect(OriMesh,targetMesh,blendshape,TargetIndex, inbetweenIndex = inbtweenIndex )
        
        
        
    ## =================================================================================
    ##    wrap  deformer menager
    
    ##----------------------------------------------------------------------------------
        
        
    def LZ_WrapDeformer(self,originalObj, shapeToCopy , newObj) :
    
        
    
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
        
        
        '''
        
        ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        
        
        '''
        wrapObj = shapeToCopy + "suffTemp"
        mc.duplicate (originalObj, rr = 1, n = "blendObj")
        mc.duplicate ( newObj , rr = 1, n = "tempName")
    
        mc.rename("tempName", wrapObj) 
        
        for  objD in [ "blendObj", wrapObj ]:
            for attr in  ['.tx','.ty','.tz','.rx','.ry','.rz']:
                mc.setAttr( str(objD)  + attr , 0 )
        
        
        
        
        
        blendshapeToWrap = originalObj + "_blendShapeToWarp"
        mc.blendShape (shapeToCopy, "blendObj", frontOfChain = 1, n = blendshapeToWrap , topologyCheck = False )
        
        mc.select ( wrapObj , "blendObj",  r=1) 
        
        wrapName = mm.eval('doWrapArgList "6" { "1","0","1", "2", "1", "1", "0" };')[0]
        
        #valeur blend shape mise 1
        blendShapeAttr = str(blendshapeToWrap)+"." + shapeToCopy
        mc.setAttr(blendShapeAttr, 1)
        
        #delete history de l'objet copi
        mc.select (wrapObj, r = 1)
        mc.DeleteHistory
        mc.delete (ch = 1)
        
        #suppression des deux objets temporaires
        mc.delete ('blendObjBase', 'blendObj')
        
        newName = shapeToCopy + '_wrap'
        mc.rename( wrapObj , newName)
        
        return newName
        
    ############################################################################################
    ##### ===================================== correct zhangjian plug-in ===========================================    
    def findBlendShapeInHistory(self, mesh = '' ):
        
        history = mc.listHistory(mesh)
        for hi in history:
            
            if mc.nodeType(hi) =='blendShape':
                return hi
                
        return None
        
    def disableAllBlendShapeTargets( self , blend = ''):
    
        existingNumTargets = mc.blendShape( blend , q =True ,  wc = True )
        if existingNumTargets <1:
            return 
            
        for i in range(existingNumTargets):
            
            mc.blendShape( blend ,  e =True , w = (i , 0.0 ) )
    
    
    def duplicateSkinnedMeshAtBindPos(self , mesh = '' ):
        
        skin = mm.eval('findRelatedSkinCluster ' + mesh )
        
        if skin == '':
            print("found no skin cluster!")
            return None
            
        mc.setAttr(skin+'.envelope' , 0  )
        duplicated = mc.duplicate( mesh , returnRootsOnly = True )
        
        mc.setAttr(skin+'.envelope' , 1  )
        
        refname = mc.rename( duplicated[0] , str(duplicated[0]) + 'CBSRef' )
        mc.setAttr( str(refname) + '.tx' , lock =False )
        
        mc.move( 37,0,0  , refname , r=True , os=True ,  wd= True   )
        
    
        return refname
        
    def duplicateMeshToSculpt(self, mesh):
        
        duplicated = mc.duplicate( mesh , rr = True )
        
        refname = mc.rename( duplicated[0] , str(duplicated[0]) + 'CBSculpt' )
        
        for attr in [".tx",".ty",".tz",".sx",".sy",".sz",".rx",".ry",".rz"]:
            
            mc.setAttr( str(refname) + str(attr) , lock =False  )
    
        mc.move( 37,0,0  , refname , r=True , os=True ,  wd= True   )
        
        return refname
        
        
        
    def duplicateMeshAsTarget( self , mesh = '' ):
    
        duplicated = mc.duplicate( mesh , rr = True )
        
        refname = mc.rename( duplicated[0] , str(duplicated[0]) + 'CBSculptTgt' )
    
        mc.setAttr( str(refname) + '.tx' , lock =False )
        
        mc.move( 37,0,0  , refname , r=True , os=True ,  wd= True   )
        
    
        return refname
        
    def addTargetToBlend(self , ref = '' , mesh = '' , blend = '' ):
        
        existingNumTargets = mc.blendShape( blend , q=True , wc =True )
        
        #realTgtIdx = mm.eval( 'bsMultiIndexForTarget( '+ str(blend) +','+str( existingNumTargets-1) +')' )
        #
        #if realTgtIdx<0:
        #    realTgtIdx = existingNumTargets
        #else:
        #    realTgtIdx = realTgtIdx+1
        realTgtIdx = existingNumTargets+1
        mc.blendShape( blend , e =True , t =  (mesh ,   realTgtIdx , ref , 1.0  ) )
        mc.blendShape( blend , e =True , w =  ( realTgtIdx , 1.0  ) )
        
    def removeTargetFromBlend( self , target , mesh , blend ):
        
        existingNumTargets = mc.blendShape( blend , q =True , wc=True )
        mc.blendShape( blend , e =True , rm =True , t= ( mesh , existingNumTargets+1 , target , 1.0  ) )
        
        
    def createCorrectBlendTarget( self , sculpt , cache  ):
        
        src = mc.pickWalk( sculpt , d= 'down')
        node = mc.createNode( 'sculptToBlendTarget' , n = 'correctBlendShape' )
        
        mc.connectAttr( str(cache) + '.poseSpaceRow0' , str(node) + '.poseSpaceRow0' )
        mc.connectAttr( str(cache) + '.poseSpaceRow1' , str(node) + '.poseSpaceRow1' )
        mc.connectAttr( str(cache) + '.poseSpaceRow2' , str(node) + '.poseSpaceRow2' )
        mc.connectAttr( str(cache) + '.bindPoint' , str(node) + '.bindPoint' )
        mc.connectAttr( str(cache) + '.posePoint' , str(node) + '.posePoint' )
        mc.connectAttr( str(src[0]) + '.outMesh' , str(node) + '.sculptMesh' )
        
        
        mc.setAttr( str(node)+'.poseFile'  , cache , type = 'string')
        
        target = mc.polyCube( ch =False , n = str(sculpt)+'Tgt' )
        mc.move( -27,0,0  , target[0] , r=True , os=True ,  wd= True )
        
        targetMesh = mc.pickWalk( target[0] ,d ='down'   )
        
        mc.connectAttr( str(node) + '.outMesh' , str(targetMesh[0]) + '.inMesh' )
        
        return target[0]
    
    def connectCorrectBlendTarget(self,sculpt ='', target='' , cache =''  ):
        
        
        src = mc.pickWalk( sculpt , d= 'down')
        node = mc.createNode( 'sculptToBlendTarget' , n = 'correctBlendShape' )
        
        mc.connectAttr( src[0] + ".outMesh" , node + ".sculptMesh" )
        
        mc.setAttr( str(node)+'.poseFile'  , cache, type = 'string' )
        
        targetMesh = mc.pickWalk( target , d= 'down')
        mc.connectAttr( node + ".outMesh" , targetMesh[0] + ".inMesh" )
    
    def getFullPath(self , obj ):
        
        full = mc.ls( obj , l= True )
        return full
    def getShapeFullPath(self , obj ):
    
        shape = mc.pickWalk( obj , d= 'down')
        
        return self.getFullPath( shape[0] )
    
    def setupCorrectBlendSkin(self , mesh = [''] ):
        
        
        #sel = mc.ls(sl=True)
        sel = mesh
        if len(sel) < 1:
            print('must select a mesh\n')
            return []
        
        sculpt = self.duplicateMeshToSculpt( sel[0])
        ref = self.duplicateSkinnedMeshAtBindPos( sel[0])
        
        blend = self.findBlendShapeInHistory( sel[0])
        if blend == None:
            ress = mc.blendShape( sel[0], frontOfChain =True )
            blend = ress[0]
        
        self.addTargetToBlend( ref,  sel[0],  blend)
        refMesh = self.getShapeFullPath( ref)
        poseMesh = self.getShapeFullPath( sel[0])
        #print(poseMesh)
        cache = mm.eval( 'calculatePoseSpace -pa ' + str(poseMesh[0]) + ' -bt ' +  str(refMesh[0]) + ' -cc')
        
        self.removeTargetFromBlend( ref,  sel[0],  blend)
        
        mc.delete(ref)
        
        if cache == '':
            return []
        
        target = self.createCorrectBlendTarget( sculpt,  cache)
        
        mc.select( str(sculpt) + '.vtx[0]' , r = True )
        
        mc.move( -0.177854 , -0.681621 ,  0.0358554 , str(target) + ".vtx[0]" , r=True  )
        mc.move( 0.177854 , 0.681621 ,  -0.0358554 , str(target) + ".vtx[0]" , r=True  )
        
        mc.select(cl=True)
        
        return [sculpt , target ]
        
    def rebuildCorrectBlendPose( self  ):
        sel = mc.ls(sl=True)
        if len(sel)<1:
            print( "must select a mesh\n" )
            return
            
        skinnedMesh = mc.pickWalk( sel[0] , d = 'down'    )
        print( "try find skin of " +  skinnedMesh[0] + "\n"  )
        
        
        skin = mm.eval( 'findRelatedSkinCluster ' +str(skinnedMesh[0]) )
        
        if skin == '':
            print("cannot find skin of " +  skinnedMesh[0] + "\n")
        else:
            print("found skin " +  skin + "\n")
        
        sculpt = self.duplicateMeshToSculpt( sel[0])
        
        ref = ""
        if skin == '':
            ref = sel[0]
        else:
            ref = self.duplicateMeshAsTarget( sel[0])
            
            
        poseMesh = self.getShapeFullPath( sculpt)
        refMesh = self.getShapeFullPath( ref)
        cacheName = mc.fileDialog()
        
        mm.eval( 'calculatePoseSpace  -pa ' +str(poseMesh) + ' -bt  ' +str(refMesh) + ' -lc '  + str( cacheName  ))
        self.connectCorrectBlendTarget( poseMesh,  refMesh,  cacheName)
        
        mm.eval( 'calculatePoseSpace  -pa ' +str(poseMesh) + ' -lp  ' +str(cacheName)  )
        
        
    def updateCorrectBlendPose(self):
        
        sel = mc.ls(sl=True)
        if len(sel)<1:
            print( "must select a sculpted mesh\n" )
            return
            
        poseMesh = self.getShapeFullPath( sel[0])
        
        cbshp = mc.listConnections( poseMesh , t = 'sculptToBlendTarget' )
        if len(cbshp)<1:
            
            print("cannot find correctBlendShape connected to " +  poseMesh)
            return
            
        cacheName = mc.getAttr( cbshp[0] + ".poseFile" )
        
        mm.eval( 'calculatePoseSpace  -pa ' +str(poseMesh) + ' -sp ' +str(cacheName)  )
        
    
    
    
    
    
    
    
    
        
        