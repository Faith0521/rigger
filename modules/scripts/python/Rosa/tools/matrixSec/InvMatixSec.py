# coding:utf-8
#maya command:
'''
from OERU_sec_UI import *
OERU_sec_UI_window()
'''
import maya.cmds as cmds
import pymel.core as pm

def OERU_sec_connectMatrix(geoName,revName):
	skinNode = pm.PyNode(geoName).listHistory(pdo=1,type = 'skinCluster')

	if skinNode:
		for num,jnt in enumerate(pm.skinCluster(skinNode[0],q=1,inf=1)):
			jointIndex = [infc.name()[:-1].rsplit('[',1)[-1] for infc in jnt.obcc.listConnections(s=0,p=1) if skinNode[0].name() in infc.name()]
			if not pm.isConnected(pm.PyNode(jnt).worldInverseMatrix[0],skinNode[0].bindPreMatrix[ int(jointIndex[0]) ]):
				if num < 1:
					jnt.worldInverseMatrix[0] >> skinNode[0].bindPreMatrix[ int(jointIndex[0]) ]
				else:
					revGrp = pm.listRelatives(pm.listRelatives(pm.listRelatives(jnt,p=True)[0],p=True)[0],p=True)[0]
					pm.PyNode(revGrp).worldInverseMatrix[0] >> skinNode[0].bindPreMatrix[ int(jointIndex[0]) ]
			print(jnt,jointIndex)

def OERU_sec_replaceGeo(objs):
	originalGeo = objs[0].split('.')[0]
	newName = cmds.rename(originalGeo,originalGeo+'_secOriginalGeo')
	dupGeo = cmds.duplicate(newName,n = originalGeo,st=0)[0]
	testNum = 0
	while True:
		if cmds.pickWalk(dupGeo,d='left')[0] == newName or testNum == 100:
			break
		testNum+=1
		cmds.reorder(dupGeo,r=-1)
	if cmds.listRelatives(newName,p=1):
		cmds.parent(newName,w=1)
	cmds.blendShape(newName,dupGeo,w=(0,1),n='%s_secBlendShape'%dupGeo)
	return newName

def OERU_sec_CreateCtrl(name):
	curveName = cmds.curve(d=1,p=[(0,1,0),(0,0.92388,0.382683),(0,0.707107,0.707107),(0,0.382683,0.92388),(0,0,1),(0,-0.382683,0.92388),(0,-0.707107,0.707107),(0,-0.92388,0.382683),(0,-1,0),(0,-0.92388,-0.382683),(0,-0.707107,-0.707107),(0,-0.382683,-0.92388),(0,0,-1),(0,0.382683,-0.92388),(0,0.707107,-0.707107),(0,0.92388,-0.382683),(0,1,0),(0.382683,0.92388,0),(0.707107,0.707107,0),(0.92388,0.382683,0),(1,0,0),(0.92388,-0.382683,0),(0.707107,-0.707107,0),(0.382683,-0.92388,0),(0,-1,0),(-0.382683,-0.92388,0),(-0.707107,-0.707107,0),(-0.92388,-0.382683,0),(-1,0,0),(-0.92388,0.382683,0),(-0.707107,0.707107,0),(-0.382683,0.92388,0),(0,1,0),(0,0.92388,-0.382683),(0,0.707107,-0.707107),(0,0.382683,-0.92388),(0,0,-1),(-0.382683,0,-0.92388),(-0.707107,0,-0.707107),(-0.92388,0,-0.382683),(-1,0,0),(-0.92388,0,0.382683),(-0.707107,0,0.707107),(-0.382683,0,0.92388),(0,0,1),(0.382683,0,0.92388),(0.707107,0,0.707107),(0.92388,0,0.382683),(1,0,0),(0.92388,0,-0.382683),(0.707107,0,-0.707107),(0.382683,0,-0.92388),(0,0,-1)])
	newName = cmds.rename(curveName,name)
	sdkGrp = cmds.group(n=name+'_sdk')
	reserveGrp = cmds.group(n=name+'_reserve')
	
	jointName = cmds.joint(newName,r=1,n='%s_jnt'%name)

	return cmds.group(reserveGrp,n=name+'_zero'),jointName

def OERU_sec_rivetFollicle(objsList,rivetGeo):
	''' 指定定位模型和受控物体,会在接近定位模型处创建毛囊父子约束受控物体'''
	if type(objsList) != list:
		objsList = [objsList]
	shapeNode = pm.PyNode(rivetGeo).getShape()
	returnList = []
	#buildClosestNode
	closestNode = pm.createNode('closestPointOnMesh',n='OERU_ClosestPoint_node')
	shapeNode.worldMatrix[0] >> closestNode.inputMatrix
	shapeNode.worldMesh >> closestNode.inMesh
	#buildFollicle
	for objEO in objsList:
		obj = pm.PyNode(objEO)
		rpPosition = obj.getRotatePivot()
		UVpinNode =  pm.createNode('uvPin',n='%s_inverseuvPin'%obj)
		UVloc = pm.spaceLocator(n='%s_uvPin_Loc'%obj)
		
		shapeNode.worldMesh[0] >> UVpinNode.deformedGeometry
		shapeNode.outMesh >> UVpinNode.originalGeometry
		UVpinNode.outputMatrix[0] >> UVloc.offsetParentMatrix

		#ending
		returnList.append(UVloc.name())
		closestNode.ip.set(rpPosition)
		UVpinNode.coord[0].cu.set( closestNode.u.get() )
		UVpinNode.coord[0].cv.set( closestNode.v.get() )
		offsetGrp = pm.group(em=1,p=UVloc,n='%s_offset'%UVloc)
		parentCon = pm.parentConstraint(offsetGrp,obj)
		cmds.setAttr('%s.interpType'%parentCon,2)
		pm.scaleConstraint(offsetGrp,obj)
	#clear
	pm.delete(closestNode)
	return returnList

def OERU_sec_UI_button(model):
	''' UI_button'''
	if model == 'load':
		cmds.textScrollList('OERU_sec_UI_Scroll',e=1,ra=1)
		cmds.textScrollList('OERU_sec_UI_Scroll',e=1,append=cmds.ls(sl=1,fl=1))
	if model == 'add':
		for sl in cmds.ls(sl=1,fl=1):
			if not sl in cmds.textScrollList('OERU_sec_UI_Scroll',q=1,ai=1):
				cmds.textScrollList('OERU_sec_UI_Scroll',e=1,append=sl)
	if model == 'build':
		objsList = cmds.textScrollList('OERU_sec_UI_Scroll',q=1,ai=1)
		geoName = objsList[0].split('.')[0]
		if not cmds.objExists('%s_secOriginalGeo'%geoName):
			# 未创建
			originalGeo = OERU_sec_replaceGeo(objsList)
			#buildGrp
			secGrp = cmds.group(em=1,n='%s_sec_Group'%geoName)
			rootJoint = cmds.joint(secGrp,r=1,n='%s_sec_rootJoint'%geoName)
			skinNode = cmds.skinCluster(rootJoint,geoName,tsb=1,n='%s_sec_skinCluster'%geoName)
			#buildCtrl
			ctrlGrp = cmds.group(em=1,n='%s_secCtrl_Group'%geoName)
			follicleGrp = cmds.group(em=1,n='%s_secFollicle_Group'%geoName)
			#clearUp
			cmds.parent(originalGeo,ctrlGrp,follicleGrp,secGrp)
			cmds.hide(originalGeo,follicleGrp,rootJoint)
		else:
			# 已创建
			ctrlGrp = '%s_secCtrl_Group'%geoName
			originalGeo = '%s_secOriginalGeo'%geoName
			follicleGrp = '%s_secuvPinLoc_Group'%geoName
			skinNode = '%s_sec_skinCluster'%geoName
		# 通用
		eAdd = 0
		while True:
			if not cmds.objExists('%s_secCtrl_%s'%(geoName,eAdd)) or eAdd==100:
				break
			eAdd+=1
		for i,obj in enumerate(objsList):
			vtxPosition = cmds.xform(obj,q=1,ws=1,t=1)
			ctrlReturn = OERU_sec_CreateCtrl('%s_secCtrl_%s'%(geoName,i+eAdd))
			cmds.parent(ctrlReturn[0],ctrlGrp)
			cmds.move(vtxPosition[0],vtxPosition[1],vtxPosition[2],ctrlReturn[0])
			follicleList = OERU_sec_rivetFollicle(ctrlReturn[0],rivetGeo=originalGeo)
			cmds.parent(follicleList,follicleGrp)
			cmds.skinCluster(skinNode,e=1,wt=0,ai=ctrlReturn[1])
		OERU_sec_connectMatrix(geoName,'%s_secCtrl_%s_reserve'%(geoName,i+eAdd))
		cmds.select(cl=1)

def OERU_sec_UI_window():
	OERU_sec_version = 'v 2.0'
	bgColor = (0.3,0.3,0.3)
	buttonColor = (0.13,0.13,0.13)
	if cmds.window('OERU_sec_UI',q=1,ex=1):
		cmds.deleteUI('OERU_sec_UI')
	cmds.window('OERU_sec_UI',title='OERU_secBuild %s'%OERU_sec_version,s=1,tlb=1)
	cmds.columnLayout(adj=1)
	cmds.rowLayout(nc=2,cw=(100,100),adj=1)
	cmds.button(label=u'加载模型点',c='OERU_sec_UI_button("load")',bgc=buttonColor)
	cmds.button(label=u'+',c='OERU_sec_UI_button("add")',bgc=buttonColor)
	cmds.setParent('..')
	cmds.textScrollList('OERU_sec_UI_Scroll',h=70,nr=15,ams=0)
	cmds.button(label=u'创建',c='OERU_sec_UI_button("build")',h=50,bgc=buttonColor)
	cmds.window('OERU_sec_UI',e=1,wh=(200,145))
	cmds.window('OERU_sec_UI',e=1,vis=1)

OERU_sec_UI_window()