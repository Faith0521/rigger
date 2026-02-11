# coding: utf-8
# This Function can stretch IK joint
# Note: can maintain volume on and off.
# FN: Ik_stretch(ikhandle,keepVolum )
# Date: 2014/03/12_v1.0
#-------------------------------------------------------------------------

# inPuts = []
# outPuts=[]
# import squeezeTools
# reload(squeezeTools)
# squeezeTools.create('lf_', inPuts, outPuts, mpNode=None )

#-------------------------------------------------------------------------
import maya.cmds as mc
from rxCore import aboutPublic
from rxCore import aboutLock
from rxCore import aboutName


#---------#(pow((lenth/OriLen),frameCache)-1)*n+1  -------------#
#(pow((tx/oriTx),frameCache)-1)*n+1
#(pow((scaleX),frameCache)-1)*n+1

def baseOnSubsection(prefix, inPuts, outPuts, scaleAxis=['sy','sz'], mpNode=None):
	"""
	:param prefix: string
	:param inPuts: use for get different between distance.
	:param outPuts: scale objects
	:param scaleAxis: axis use for scale
	:param mpNode: none / transform
	:return:
	"""

	if len(inPuts) != len(outPuts):
		return

	num = len(inPuts)

	# create squeeze bridge
	cbridge = prefix + '_squeeze_cmd_bridge'
	if not mc.objExists(cbridge):
		mc.createNode('transform', n=cbridge)
		aboutLock.lock(cbridge)
		aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'],
							   lock=False, attributeType='float', keyable=True, dv=1, min=0.01, max=1000000)
		aboutPublic.addNewAttr(objects=[cbridge], attrName=['volume'],
							   lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

	vbridge = prefix + '_squeeze_value_bridge'
	if not mc.objExists(vbridge):
		mc.createNode('transform', n=vbridge)
		aboutLock.lock(vbridge)

	# add value attr, I used double loop because attribute oreder.
	for i in range(num):
		aboutPublic.addNewAttr(objects=[vbridge], attrName=['orgDis' + aboutName.letter(i)],
							   lock=False, attributeType='float', keyable=True, dv=0)
	for i in range(num):
		aboutPublic.addNewAttr(objects=[vbridge], attrName=['realDis' + aboutName.letter(i)],
							   lock=False, attributeType='float', keyable=True, dv=0)
	for i in range(num):
		aboutPublic.addNewAttr(objects=[vbridge], attrName=['power' + aboutName.letter(i)],
							   lock=False, attributeType='float', keyable=True, dv=0)

	dv = -0.1
	for i in range(num):

		# set jnts
		inPut = inPuts[i]
		outPut = outPuts[i]
		nextOrgDisAttr1=''
		nextOrgDisAttr2=''
		nextRealDisAttr1=''
		nextRealDisAttr2=''

		# set power value
		powAttr = 'power' + aboutName.letter(i)
		maxValue = (3.0 / num)
		if i < num / 2.0:
			dv += maxValue
		elif i == num / 2.0:
			pass
		else:
			dv -= maxValue
		mc.setAttr('%s.%s' % (vbridge, powAttr), (dv + maxValue))

		# string nextDisAttr
		if i != (num-1):
				nextInPut = inPuts[i+1]
				nextOrgDisAttr1 = 'orgDis' + aboutName.letter(i)
				nextOrgDisAttr2 = 'orgDis' + aboutName.letter(i+1)
				nextRealDisAttr1 = 'realDis' + aboutName.letter(i)
				nextRealDisAttr2 = 'realDis' + aboutName.letter(i+1)

		if i !=0 and i!=(num-1): # ignore A and ignore last dis node.
			disNode = mc.createNode( 'distanceBetween', name='{0}_volume_RealDis_{1}_md'.format(prefix, aboutName.letter(i+1)) )
			mc.connectAttr(inPut+'.worldMatrix[0]', disNode+'.inMatrix1')
			mc.connectAttr(nextInPut+'.worldMatrix[0]', disNode+'.inMatrix2')

			globalScale_Mdl = mc.createNode('multDoubleLinear', name='{0}_volume_InitScale_{1}_mdl'.format(prefix, aboutName.letter(i+1)) )
			mc.connectAttr(cbridge+'.initScale', globalScale_Mdl+'.input1')
			mc.connectAttr(disNode+'.distance', globalScale_Mdl+'.input2')

			# set org dis value
			value = mc.getAttr(disNode+'.distance')
			mc.setAttr( '%s.%s'%(vbridge, nextOrgDisAttr2), value )

			# set real dis value
			mc.connectAttr( globalScale_Mdl+'.output', '{0}.{1}'.format(vbridge, nextRealDisAttr2) )

			# --------------------------------------------------create nodes--------------------------------------------------
			# pow Node
			KVScaleYZ_Md = mc.createNode( 'multiplyDivide', name='{0}_volume_Power_{1}_md'.format(prefix, aboutName.letter(i)) )
			mc.setAttr('.operation', 3)
			#->pow.2x
			mc.connectAttr( '{0}.{1}'.format(vbridge, powAttr), (KVScaleYZ_Md + '.input2X') )

			# lenProportion Node
			refOrgdis_Adl =  mc.createNode( 'addDoubleLinear', name='{0}_volume_refOrgDis_{1}_Adl'.format(prefix, aboutName.letter(i)) )
			refRealdis_Adl = mc.createNode( 'addDoubleLinear', name='{0}_volume_refRealDis_{1}_Adl'.format(prefix, aboutName.letter(i)) )

			mc.connectAttr( '{0}.{1}'.format(vbridge, nextOrgDisAttr1) , refOrgdis_Adl+'.input1')
			mc.connectAttr('{0}.{1}'.format(vbridge, nextOrgDisAttr2), refOrgdis_Adl + '.input2')

			mc.connectAttr( '{0}.{1}'.format(vbridge, nextRealDisAttr1) , refRealdis_Adl+'.input1')
			mc.connectAttr('{0}.{1}'.format(vbridge, nextRealDisAttr2), refRealdis_Adl + '.input2')


			lenProportion_Md = mc.createNode( 'multiplyDivide', name='{0}_volume_lenProportion_{1}_md'.format( prefix, aboutName.letter(i) ) )
			mc.setAttr('.operation', 2)
			mc.connectAttr( refOrgdis_Adl+'.output', '{0}.input1X'.format(lenProportion_Md) )
			mc.connectAttr( refRealdis_Adl+'.output', '{0}.input2X'.format(lenProportion_Md) )
			mc.connectAttr( (lenProportion_Md + '.outputX'), (KVScaleYZ_Md + '.input1X') )

			KVScaleSub_Md = mc.createNode( 'plusMinusAverage', name='{0}_volume_Subtract_{1}_pma'.format(prefix, aboutName.letter(i) ) )
			mc.setAttr('.operation', 2)
			mc.setAttr('.input1D[1]', 1)
			mc.connectAttr( (KVScaleYZ_Md + '.outputX'), (KVScaleSub_Md + '.input1D[0]') )

			KVScaleYZOnOff_Mdl = mc.createNode( 'multDoubleLinear', name='{0}_volume_OnOff_{1}_mdL'.format(prefix, aboutName.letter(i)) )
			mc.connectAttr( (KVScaleSub_Md + '.output1D'), ( KVScaleYZOnOff_Mdl + '.input1') )
			mc.connectAttr( cbridge + '.volume', ( KVScaleYZOnOff_Mdl + '.input2') )

			KVScaleSum_Adl = mc.createNode( 'addDoubleLinear', name='{0}_volume_Sum_{1}_Adl'.format(prefix, aboutName.letter(i)) )
			mc.setAttr('.input1', 1)
			mc.connectAttr( (KVScaleYZOnOff_Mdl + '.output'), (KVScaleSum_Adl + '.input2') )

			# connect to joint.
			# remove start jnt and end jnt.
			# if i!=0 and i!=num-1:
			for axis in scaleAxis:
				mc.connectAttr( (KVScaleSum_Adl + '.output'), (outPut + '.' + axis) )

	# mpNode / clean
	mpExists = False
	if not mpNode:
		mpNode = prefix + '_squeeze_noTrans'
		mc.createNode('transform', n=mpNode)
		mpExists = True
	elif mc.objExists(mpNode):
		mpExists = True

	if mpExists:
		mc.hide(mpNode)
		mc.parent(cbridge, mpNode)
		mc.parent(vbridge, mpNode)

	# output
	result = {'rootGrp':mpNode,'cmd': cbridge, 'vmd':vbridge}
	return result


def baseOnCrvInfo(prefix, crvInfo, outPuts, scaleAxis=['sy','sz'], mpNode=None):
	"""
	:param prefix: string
	:param crvInfo: curve info attributes.
	:param outPuts: scale objects
	:param scaleAxis: axis use for scale
	:param mpnode: none / transform
	:return:
	"""
	# create squeeze bridge

	num = len(outPuts)

	cbridge = prefix + '_squeeze_cmd_bridge'
	if not mc.objExists(cbridge):
		mc.createNode('transform', n=cbridge)
		aboutLock.lock(cbridge)
		aboutPublic.addNewAttr(objects=[cbridge], attrName=['initScale'],
							   lock=False, attributeType='float', keyable=True, dv=1, min=0.01, max=1000000)
		aboutPublic.addNewAttr(objects=[cbridge], attrName=['volume'],
							   lock=False, attributeType='float', keyable=True, dv=0, min=0, max=1)

	vbridge = prefix + '_squeeze_value_bridge'
	if not mc.objExists(vbridge):
		mc.createNode('transform', n=vbridge)
		aboutLock.lock(vbridge)
		aboutPublic.addNewAttr(objects=[vbridge], attrName=['orgDis'],
							   lock=False, attributeType='float', keyable=True, dv=0)
		aboutPublic.addNewAttr(objects=[vbridge], attrName=['realDis'],
							   lock=False, attributeType='float', keyable=True, dv=0)
		for i in range(num):
			aboutPublic.addNewAttr(objects=[vbridge], attrName=['power' + aboutName.letter(i)],
			                       lock=False, attributeType='float', keyable=True, dv=0)

	mc.setAttr( vbridge+'.orgDis', (mc.getAttr(crvInfo+'.arcLength')) )

	# dd
	# init dis
	globalScale_Mdl = mc.createNode('multDoubleLinear',
									name='{0}_volume_InitScale_mdl'.format(prefix))
	mc.connectAttr(cbridge + '.initScale', globalScale_Mdl + '.input1')
	mc.connectAttr(crvInfo+'.arcLength', globalScale_Mdl + '.input2')
	mc.connectAttr(globalScale_Mdl + '.output', vbridge + '.realDis')

	# onoff
	KVScaleOnOff_Bla = mc.createNode('blendTwoAttr', n='{0}_volume_OnOff_Bla'.format(prefix))
	mc.setAttr( KVScaleOnOff_Bla+'.input[0]', (mc.getAttr(crvInfo+'.arcLength')) )
	mc.connectAttr(vbridge + '.realDis', KVScaleOnOff_Bla+'.input[1]')
	mc.connectAttr(cbridge+'.volume', KVScaleOnOff_Bla+'.attributesBlender')

	# Proportion
	Proportion_Md = mc.createNode('multiplyDivide', name='{0}_volume_Proportion_md'.format(prefix))
	mc.setAttr(Proportion_Md + '.operation', 2)
	mc.connectAttr( KVScaleOnOff_Bla + '.output', Proportion_Md + '.input1X' )
	mc.setAttr( Proportion_Md + '.input2X', (mc.getAttr(crvInfo+'.arcLength')) )

	# sqrt
	sqrt_Md = mc.createNode('multiplyDivide', name='{0}_volume_sqrt_md'.format(prefix))
	mc.setAttr(sqrt_Md + '.operation', 3)
	mc.connectAttr(Proportion_Md + '.outputX', sqrt_Md + '.input1X')
	mc.setAttr(sqrt_Md+'.input2X', 0.5)

	# sqrt divied
	sqrtDivide_Md = mc.createNode('multiplyDivide', name='{0}_volume_sqrtDivide_md'.format(prefix))
	mc.setAttr(sqrtDivide_Md + '.operation', 2)
	mc.setAttr(sqrtDivide_Md + '.input1X', 1)
	mc.connectAttr(sqrt_Md+'.outputX', sqrtDivide_Md+'.input2X')

	# scale output
	dv = -0.1
	for i in range(num):
		# init
		output = outPuts[i]
		powerAttr = vbridge + '.power' + aboutName.letter(i)

		# set power value
		maxValue = (3.0 / num )
		if i < num / 2.0:
			dv += maxValue
		elif i == num / 2.0:
			pass
		else:
			dv -= maxValue
		mc.setAttr(powerAttr, (dv + maxValue) )

		if i!=0 and i!=(num-1):
			# connect
			outputPower_Md = mc.createNode( 'multiplyDivide', name='{0}_volume_outputPower_{1}_md'.format( prefix, aboutName.letter(i) ) )
			mc.setAttr(outputPower_Md + '.operation', 3)
			mc.connectAttr(sqrtDivide_Md + '.outputX', outputPower_Md + '.input1X')
			mc.connectAttr(powerAttr, outputPower_Md + '.input2X')
			mc.connectAttr(outputPower_Md + '.outputX', output + '.' + scaleAxis[0])
			mc.connectAttr(outputPower_Md + '.outputX', output + '.' + scaleAxis[1])

	# mpNode / clean
	mpExists = False
	if not mpNode:
		mpNode = prefix + '_squeeze_noTrans'
		mc.createNode('transform', n=mpNode)
		mpExists = True
	elif mc.objExists(mpNode):
		mpExists = True

	if mpExists:
		mc.hide(mpNode)
		mc.parent(cbridge, mpNode)
		mc.parent(vbridge, mpNode)

	# output
	result = {'rootGrp':mpNode,'cmd': cbridge, 'vmd':vbridge}
	return result