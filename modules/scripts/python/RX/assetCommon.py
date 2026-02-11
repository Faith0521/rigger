import maya.cmds as mc
import maya.mel as mel
import os,re

from rxCore import aboutLock
import spaceTools
import displayTools
# import customRigs
# import assetDeform
import cluster
import assetEnv
import importMod


def importTags():
    try:
        customTags = importMod.import_module('customTags', r=1)
        customTags.load()
    except:
        print ('Skipping customTags file..')

def createSpaces(nodes=None):
    if not nodes:
        nodes = mc.ls('*.tagSpaces')
    else:
        tn = mc.ls(nodes)
        nodes = []
        for n in tn:
            if mc.objExists(n+'.tagSpaces'):
                nodes.append(n+'.tagSpaces')

    for node in nodes:
        arg = mc.getAttr(node)
        if arg:
            arg = arg.replace('  ', ' ').strip()
            args=arg.split(' ')

            a0 = args[0]
            a1 = args[2]
            a2 = args[1]

            args.remove(a0)
            args.remove(a1)
            args.remove(a2)

            ctrl = node.split('.')[0]
            dv = int(a0.split(':')[1])
            parent = a1.split(':')[1]
            oo = a2.split(':')[1]

            if oo == 'True':
                oo=True
            else:
                oo=False

            spaceArg = ' '.join(args)

            if mc.objExists(parent):
                spaceTools.create(ctrl, parent , spaceArg, oo=oo, dv=dv)

        mc.setAttr(node, l=0)

def getDuplicateNames():
    dups=[]
    nodes=mc.ls(sn=1)
    for n in nodes:
        if re.search('\|', n):
            dups.append(n)
    return dups

def lockRig():

    # kill blend systems
    # sculpts = mc.ls('blends', [s.split('.')[0] for s in mc.ls('*.blendsculpt')])
    # if sculpts:
    #     mc.delete(sculpts)

    # fix cvlusters
    cluster.fixShapeNames()
    nodes = mc.listRelatives ('noTransform', f=1, c=1)
    mc.hide (nodes)

    # lock all nodes under controls\
    nodes = mc.listRelatives('controls', ad=1, type='transform',  f=1)
    nolock = mc.listRelatives('controls', ad=1, type=('joint', 'ikHandle', 'poleVectorConstraint', 'pointConstraint', 'orientConstraint', 'parentConstraint'),  f=1)
    if nolock:
        for n in nolock:
            nodes.remove(n)

    aboutLock.countLock(nodes)
    aboutLock.unlockTagged(nodes)

    # trash skel
    mc.delete (mc.ls('skel'))

    # set attrs
    mc.setAttr('worldA_ctrl.ctrlDisplay', 1)
    mc.setAttr('worldA_ctrl.jointDisplay', 0)
    mc.setAttr('worldA_ctrl.modelDisplay', 1)

    # trash layers
    layers = mc.ls(typ='displayLayer')
    if 'defaultLayer' in layers: layers.remove('defaultLayer')
    if layers:
        mc.delete(layers)

    # set unreferenced model and smoothnes
    nodes = mc.listRelatives('model', ad=1, f=1)
    displayTools.set('off')

    mc.select(nodes)
    mel.eval('displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;')

    # delete unused nodes
    try:
        mel.eval ('source "hyperShadePanel.mel"')
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    except:
        pass

    # removeAllTags()
    # print ('removed all tags')

    try:
        mod = assetEnv.getrigtype()+'AttributeSettings'
        mod = importMod.import_module(mod, r=1)
        mod.load()
        print ('Loaded Attrute Settings from file..')
    except:
        pass

    mc.select(cl=1)

def bindSet(nodes):
    """create bind joints set"""
    joints = []
    for j in nodes:
        if mc.objExists(j):
            joints.append(j)

    bset = 'bindJoints_'+assetEnv.getasset()
    if not mc.objExists(bset):
        bset = mc.sets(n=bset, em=1)
    mc.sets(joints, add=bset)

# Connect model LODS and variations
def connectLOD():

    if not mc.objExists('worldA_ctrl'):
        return

    try:
        rtype = assetEnv.getrigtype()
        modelInfo = importMod.import_module(rtype+'ModelInfo', r=1)
        info = modelInfo.info()
    except:
        print ('No LOD file was found.. Skipping...')
        return

    if not info:
        return

    enum = [i[0] for i in info]
    nodes = [i[1] for i in info]

    if mc.objExists('worldA_ctrl.modelLOD'):
        mc.deleteAttr('worldA_ctrl.modelLOD')

    mc.addAttr('worldA_ctrl', ln='modelLOD', at='enum', en=':'.join(enum), k=1)
    for i in range(len(enum)):
        for n in nodes[i]:
            if mc.objExists(n+'.v'):
                try:
                    mc.setDrivenKeyframe(n+'.v', cd='worldA_ctrl.modelLOD', dv=i, v=1)
                    if i > 0 and n not in nodes[i-1]:
                        mc.setDrivenKeyframe(n+'.v', cd='worldA_ctrl.modelLOD', dv=i-1, v=0)
                    if i < len(nodes)-1 and n not in nodes[i+1]:
                        mc.setDrivenKeyframe(n+'.v', cd='worldA_ctrl.modelLOD', dv=i+1, v=0)
                except:
                    pass

    print ('Created LODs : '+', '.join(enum))


def createSet(text, setType, objects):
    mc.select(objects)
    newset = mc.sets(name=text)
    mc.addAttr(newset, ln="setName", dt="string")
    mc.addAttr(newset, ln="setType", dt="string")
    mc.setAttr("{0}.setName".format(newset), text, type="string")
    mc.setAttr("{0}.setType".format(newset), setType, type="string")
    mc.setAttr("{0}.setName".format(newset), lock=True)
    mc.setAttr("{0}.setType".format(newset), lock=True)
    return newset

def connectMocapRig():
    # connect joints
    mc.delete ('worldOffset|model')
    joints = mc.listRelatives('worldRoot_mj', ad=1, type='joint')
    for j in joints:
        if mc.objExists(j+'.connectTo'):
            driver = mc.getAttr (j+'.connectTo')
            if mc.objExists(driver):
                try:
                    mc.parentConstraint(driver, j, mo=1, n=j+'_prc')
                    mc.scaleConstraint(driver, j, mo=1, n=j+'_sc')
                except:
                    aboutLock.unlock(j)
                    mc.parentConstraint(driver, j, mo=1, n=j+'_prc')
                    mc.scaleConstraint(driver, j, mo=1, n=j+'_sc')

    mc.rename ('root', 'worldRootB')
    mc.rename ('worldRoot_mj', 'root')

    mc.parent ('root', w=1)
    model = mc.listRelatives('model', c=1)
    if not model:
        model = ['']
    os.environ['MOCAP_MODEL'] = model[0]

    mc.parent (mc.listRelatives('model', c=1), w=1)
    mc.delete ('mocap', 'model')

def controlBuild(game=True):
    importTags()
    createSpaces()
    #assetDeform.importDeformers('attrs')
    #customRigs.tagRigBuildNodes()
    if game:
        gameRig()

def importPoseDrivers():
    try:
        assetPoseDrivers = importMod.import_module('assetPoseDrivers', r=1)
        assetPoseDrivers.load()
    except:
        pass

def removeAllTags():
    nodes = mc.ls('.controlID')
    for n in nodes:
        node = n.split('.')[0]
        mc.setAttr(n, node, type= 'string')

    nodes = mc.ls('*.tagKeyable', '*.tagSpaces', '*.tag', '*.rigBuildNode', '*.blendfaces', '*.filepath')
    for n in nodes:
        try:
            mc.deleteAttr(n)
        except:
            pass

def gameRig():
    mc.select('worldRoot', hi=1)
    animjnts = mc.ls(sl=1, l=1)
    bindroot = mc.duplicate('worldRoot')[0]

    # Rename control joins and bind joints
    mc.select('worldRoot', hi=1)
    for i in range(len(animjnts)):
        mc.rename(animjnts[i], animjnts[i].split('|')[-1]+'_AC')
        animjnts = mc.ls(sl=1, l=1)

    mc.rename('root_AC', 'animRoot_AC')
    mc.rename('worldRoot_AC', 'root_AC')

    mc.rename ('root', 'animRoot')
    bindroot = mc.rename(bindroot, 'root')

    # Clean up bind hierarchy
    mc.select(bindroot, hi=1)
    for n in mc.ls(sl=1, l=1):
        if 'Constraint' in mc.nodeType(n):
            mc.delete(n)

    mc.select(bindroot, hi=1)
    bindjnts = mc.ls(sl=1)
    aboutLock.unlock()

    grps = []
    for j in bindjnts:
        if mc.nodeType(j) == 'transform':
            jj = mc.createNode('joint', p=j)
            mc.parent (jj, mc.listRelatives(j, p=1))

            ch = mc.listRelatives(j, c=1)
            if ch:
                mc.parent (ch, jj)
            mc.delete(j)
            grps.append(jj)

    for g in grps:
        mc.select(g)
        try:
            mel.eval('RemoveJoint;')
        except:
            pass

    mc.select(bindroot, hi=1)
    bindjnts = mc.ls(sl=1)
    aboutLock.unlock()

    for j in bindjnts:
        mc.setAttr(j+'.v', 1)

    bindjnts.remove('root')

    congrp = mc.createNode('transform', p='noTransform', n='constraints')
    for j in bindjnts:
        ac = j+'_AC'
        if mc.objExists(ac):
            prc = mc.parentConstraint(ac, j, n=j+'_prc', mo=1)[0]
            if mc.objExists(j+'.ssc'):
                mc.setAttr(j+'.ssc', 0)
            mc.parent (prc, congrp)

    mc.setAttr('animRoot.ssc', 0)
    prc = mc.scaleConstraint('animRoot_AC', 'animRoot', n='animRoot_sc', mo=1)[0]
    mc.parent (prc, congrp)

    bset = 'bindJoints_'+assetEnv.getasset()
    if mc.objExists(bset):
        mc.delete(bset)

    bindSet(bindjnts)
    mc.parent('root_AC', 'controls')
    mc.hide('root_AC')

    if 'gameRig' in assetEnv.getrigtype():
        mc.parent ('root', 'model', w=1)

    if 'mocapRig' in assetEnv.getrigtype():
        mc.parent ('root', 'model', w=1)
        mc.delete('worldA_ctrl')




