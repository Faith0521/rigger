######################################
#   Rig Build Part
######################################

import maya.cmds as mc

import assetEnv
import templateTools
import controlTools
from rxCore import aboutLock
from rxCore import aboutName
from rxCore import aboutPublic


# Build Tempalte
def template(numCtrls=2):
    # Arg values to be recorded
    args = {'numCtrls':numCtrls}
    lockArgs = ['numCtrls']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('base', args, lockArgs)
    if not info:
        return

    topnode = info[0]
    prefix = info[1]

    # Build Contorls
    ctrls=[]
    for i in reversed(range(numCtrls+1)):
        ctrls.append( controlTools.create(name='world_ctrl', shape='D07_circle', scale=5, color='darkCyan' )[-1] )

    mc.delete(ctrls[0]+'_grp')
    ctrls.remove( ctrls[0] )
    ctrls.reverse()
    controlTools.setColor(ctrls[-1], 'cyan')

    for i in range(len(ctrls)):
        mc.xform(ctrls[i]+'.cv[*]', r=1, s=[1 +(i*.2), 1 +(i*.2), 1 +(i*.2)])
        mc.parent(ctrls[i]+'_grp', topnode+'Ctrls')

    # Buidl worldRoot joint
    worldRoot = templateTools.createJoint('worldRoot', topnode)
    mc.setAttr(worldRoot[-1]+'.inheritsTransform', 0)
    mc.delete(worldRoot[-1]+'_pc')

    root = templateTools.createJoint('root', topnode)

    mc.parent(worldRoot[0], topnode+'Ctrls')
    mc.parent(root[0], topnode+'Ctrls')
    mc.parent(root[-1], worldRoot[-1])

    # Cleanup
    mc.hide(worldRoot[2])
    aboutLock.lock(root+worldRoot)
    aboutLock.lock(topnode, 'r')
    #mc.setAttr(worldRoot[-2]+'.ro', 1)
    mc.hide(topnode+'Shape')

    return


# Build Anim
def anim():
    part = templateTools.getParts('base')[0]

    worldRoot = 'worldRoot_drv'
    root = 'root_drv'

    # create global rig group
    assetName = assetEnv.getasset()
    rigGrp = mc.createNode('transform', name=assetName)

    # create ctrls
    numCtrls = templateTools.getArgs(part, 'numCtrls')

    ctrls = []
    l = aboutPublic.snapLoc('root_drv')
    for i in range(numCtrls):
        ltr = aboutName.letter(i)
        name = 'world{0}_ctrl'.format(ltr)
        ctrl = controlTools.create(name, useShape=name+'Prep' , snapTo=l, makeGroups=0)[0]
        if ctrls:
            mc.parent(ctrl, ctrls[-1])
        ctrls.append(ctrl)

        if 'A' in ltr:
            mc.connectAttr(ctrl+'.sy', ctrl+'.sx')
            mc.connectAttr(ctrl+'.sy', ctrl+'.sz')
            mc.aliasAttr('globalScale', ctrl+'.scaleY')

    mc.delete(l)

    # creATE BASE NODES
    mc.addAttr(ctrls[0], ln='initScale', at='float')
    mc.addAttr(ctrls[0], ln='ctrlDisplay', at='enum', en='off:on', dv=1, k=1)
    mc.addAttr(ctrls[0], ln='jointDisplay', at='enum', en='off:on:selectable', dv=2, k=1)
    mc.addAttr(ctrls[0], ln='modelDisplay', at='enum', en='off:on:selectable', dv=2, k=1)
    mc.addAttr(ctrls[0], ln='modelLod', at='enum', en=' ', k=0)

    mc.setAttr('worldRoot.inheritsTransform', 1)


    # create nodes
    nodes = ['controls', 'joints', 'noTransform', 'model']
    mc.createNode('transform', n='worldOffset')

    for n in nodes:
        mc.createNode('transform', n=n, p=rigGrp)

    #connect
    mc.connectAttr(ctrls[0]+'.ctrlDisplay', 'controls.v')
    mc.connectAttr(ctrls[0]+'.jointDisplay', 'joints.v')
    mc.connectAttr(ctrls[0]+'.modelDisplay', 'model.v')
    mc.setAttr(ctrls[0] + '.jointDisplay', 0)

    cnd = mc.createNode('condition', n= 'modelDisplay_cnd')
    mc.setAttr('model.overrideEnabled', 1)
    mc.setAttr(cnd+'.secondTerm', 2)

    mc.connectAttr(ctrls[0]+'.modelDisplay', cnd+'.firstTerm')
    mc.connectAttr(cnd+'.outColorR','model.overrideDisplayType')

    mc.setAttr(cnd+'.colorIfFalseR', 2)
    mc.setAttr(cnd+'.colorIfTrueR', 0)

    cnd = mc.createNode('condition', n= 'jntDisplay_cnd')
    mc.setAttr('joints.overrideEnabled', 1)
    mc.setAttr(cnd+'.secondTerm', 2)

    mc.connectAttr(ctrls[0]+'.jointDisplay', cnd+'.firstTerm')
    mc.connectAttr(cnd+'.outColorR','joints.overrideDisplayType')

    mc.setAttr(cnd+'.colorIfFalseR', 2)
    mc.setAttr(cnd+'.colorIfTrueR', 0)

    mc.parentConstraint(ctrls[0], worldRoot, mo=1, n=worldRoot + '_prc')
    mc.parentConstraint(ctrls[-1], root, mo=1, n=root + '_prc')

    #parent stuff
    # for rig
    mpNode = '{0}mod'.format('base_')
    if not mc.objExists(mpNode):
        mc.createNode('transform', n=mpNode)
        mc.parent(mpNode, 'controls')

    # ctrl parent
    mc.parent('controls', 'worldOffset')
    mc.parent('worldOffset', ctrls[-1])
    mc.parent(ctrls[0], rigGrp)

    # jnts Parent
    mc.parent(worldRoot, mpNode)

    # hide
    mc.hide(worldRoot)

    # for next system
    mc.parent('worldRoot', 'joints')
    mc.parent('Prep', 'noTransform')
    mc.hide('Prep')

    mc.setAttr('model.inheritsTransform', 0)
    mc.setAttr('model.inheritsTransform', l=1)

    mc.setAttr('noTransform.inheritsTransform', 0)
    mc.setAttr('noTransform.inheritsTransform', l=1)
    mc.setAttr('root.drawStyle', 2)
    mc.setAttr('worldRoot.drawStyle', 2)

    # connect unfiorm scale
    aboutLock.lock(ctrls)
    aboutLock.unlock(ctrls, 't r tagKeyable')
    aboutLock.unlock(ctrls[0], 't r sy initScale tagKeyable ctrlDisplay jointDisplay modelDisplay modelLod')
    controlTools.tagKeyable(ctrls, 't r')
    controlTools.tagKeyable(ctrls[0], 't r sy jointDisplay ctrlDisplay modelDisplay modelLod')
    aboutLock.lock(nodes, 'worldOffset')

    mc.addAttr(ctrls[0], ln ='rigAsset', at='message')

    # init scaleY
    md = mc.createNode('multiplyDivide', n='initScale_md')
    mc.setAttr(md+'.operation', 2)
    mc.setAttr(md+'.input1X', 1)
    mc.connectAttr(ctrls[0]+'.globalScale', md+'.input2X')
    mc.connectAttr(md+'.output.outputX', ctrls[0]+'.initScale')
    mc.setAttr(ctrls[0] + '.initScale', cb=0, k=0)
    return


def mocap(suffix='mj'):

    if suffix.startswith('_'):
        suffix = suffix[1:]
    suffix = '_'+suffix

    joints = mc.listRelatives('worldRoot', ad=1, type= 'joint')

    # creATE BASE NODES
    ctrl = mc.createNode('transform', n='mocap')
    mc.addAttr (ctrl, ln='modelDisplay', at='long', min=0, max=2, dv=2, k=1)
    mc.addAttr (ctrl, ln='modelLod', at='enum', en=' ', k=0)

    # Creae nodes
    mc.parent('worldRoot', ctrl)
    mc.createNode('transform', n='model', p=ctrl)

    #connect
    mc.connectAttr(ctrl+'.modelDisplay', 'model.v')
    cnd = mc.createNode('condition', n= 'display_cnd')
    mc.setAttr('model.overrideEnabled', 1)
    mc.setAttr(cnd+'.secondTerm', 2)

    mc.connectAttr(ctrl+'.modelDisplay', cnd+'.firstTerm')
    mc.connectAttr(cnd+'.outColorR','model.overrideDisplayType')
    mc.setAttr(cnd+'.colorIfFalseR', 2)
    mc.setAttr(cnd+'.colorIfTrueR', 0)

    # clean up
    mc.delete('Prep')
    mc.setAttr('model.inheritsTransform', 0)
    mc.setAttr('model.inheritsTransform', l=1)

    mc.setAttr('mocap.inheritsTransform', 0)
    mc.setAttr('mocap.inheritsTransform', l=1)

    # connect unfiorm scale
    aboutLock.lock([ctrl, 'model'], 't r s v')
    aboutLock.unlock(ctrl, 'modelDisplay')
    mc.addAttr(ctrl, ln ='rigAsset', at='message')


    # rename and tag jointd
    for jnt in joints:
        mc.addAttr(jnt, ln='connectTo', dt='string')
        mc.setAttr(jnt+'.connectTo', jnt, type='string')
        mc.deleteAttr(jnt+'.tag')
        mc.rename(jnt, jnt+suffix)

    mc.deleteAttr('worldRoot'+'.tag')
    mc.rename('worldRoot', 'worldRoot'+suffix)

    return
