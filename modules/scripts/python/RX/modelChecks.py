import maya.cmds as mc
import maya.mel as mel
from rxCore import aboutName

# Rig Checks and Fixes 

def deleteCh():
    mc.delete(ch=1, all=1)
    return True

def assignLambert():
    nodes = mc.ls(type=('mesh','nurbsSurface'))
    mc.sets(nodes, e=1, fe='initialShadingGroup')

    mel.eval('source "hyperShadePanel.mel"')
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    return True

def layers():
    rlayers = mc.ls(type=('renderLayer', 'displayLayer'))
    if 'defaultRenderLayer' in rlayers:
        rlayers.remove('defaultRenderLayer')
    if 'defaultLayer' in rlayers:
        rlayers.remove('defaultLayer')

    if rlayers:
        mc.delete(rlayers)
    return True

def refNodes():
    if mc.ls(type='reference'):
        return 'You cannot have live references in your sence!\nMake sure you import any references and remove their namespaces.'
    return True
    
def namespaces():
    nss = mc.namespaceInfo(lon=1, r=1)
    if 'UI' in nss:
        nss.remove('UI')
    if 'shared' in nss:
        nss.remove('shared')
    if nss:
        #mel.eval('NamespaceEditor;')
        return 'Namespaces found!\nPlease remove all namespaces from your scene.'
    return True

def camsLightsImgPlanes():
    nodes = mc.ls(type='imagePlane') + mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
     'topShape',
     'frontShape',
     'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)
    if nodes:
        return
    return True

def camsLightsImgPlanesfix(*args):
    nodes = mc.ls(type='imagePlane')
    if nodes:
        mc.delete(nodes)
    nodes = mc.ls(type='camera') + mc.ls(type='light')
    sel = ['perspShape',
     'topShape',
     'frontShape',
     'sideShape']
    for s in sel:
        if s in nodes:
            nodes.remove(s)

    for n in nodes:
        xf = mc.listRelatives(n, p=1)
        mc.delete(xf)

def sameNames():
    dups = getSames()

    if dups:
        msg = 'Same names found! See script editor for details.\n\nDuplicate Names:\n'
        mc.select(dups)
        i = 1
        for d in dups:
            print (d)
            if i < 50:
                msg += '   {0}\n'.format(d)
            i += 1
        if i > 49:
            msg += '\n   Plus {0} more ...'.format(i-49)

        if mc.window('mcheckUI',q=1,ex=1):
            return
        else:
            return msg
    return True

def getSames():
    nodes = mc.ls(sn=1)
    dups = []
    for n in nodes:
        if '|' in n:
            dups.append(n)

    return dups

def sameNamesFixUI(*args):
    if mc.window('mcheckUI',q=1,ex=1):
        mc.deleteUI('mcheckUI')
    win = mc.window('mcheckUI',t='Fix Duplicate Names', s=1)
    mc.columnLayout(adj=True, rs = 5, co=['both', 10])
    mc.separator(st='none')

    msg = '''\tFix duplicate node names?.

    NOTE: This will rename all duplicate nodes in your scene. Are you sure?\nAlternatively you can resolve this yourself.'''

    mc.text(msg)
    mc.button(label='Fix', c=fixDupNames)
    mc.showWindow(win)
    mc.window(win, e=1,  wh=[500, 105], s=0)
    return 'PENDING'

def fixDupNames(*args):
    if mc.window('mcheckUI',q=1,ex=1):
        mc.deleteUI('mcheckUI')

    i = 0
    while getDups() and i < 20:
        for d in getDups():
            if mc.objExists(d):
                nn = aboutName.unique(d.split('|')[-1])
                mc.rename(d, nn)
        i += 1

def singleHi():
    nodes = mc.ls('|*')
    for n in ['front','persp','side','top']:
        nodes.remove(n)

    if len(nodes) == 1:
        return True

    return 'Must have one single hierarchy in your rig scene.\nPlease clean this up!'
    
def checkBadShapes(fix=False):
    badones = []
    nodes = [mc.listRelatives(n, p=1, f=1)[0] for n in mc.ls(type=('mesh','nurbsCurve'))]

    if not nodes:
        nodes = []

    for node in nodes:
        shapes = mc.listRelatives(node, s=1, ni=1)
        if shapes:
            i = 1
            if len(shapes) > 1:
                if i < 50:
                    badones.append(node)
                i += 1

                badones.append(node)

            for shape in shapes:
                if not shape == node.split('|')[-1] + 'Shape':
                    badones.append(shape)

    if badones:
        if fix:
            for node in badones:
                node = mc.listRelatives(node, p=1)[0]
                shape = mc.listRelatives(node, s=1, ni=1)
                shapes = mc.listRelatives(node, s=1)

                for sh in shape:
                    if sh in shapes:
                        shapes.remove(sh) 

                for sh in shapes:
                    if sh == node+'Shape':
                        mc.rename(sh, node+'ShapeOrig')

                for sh in shape:
                    if not sh == node+'Shape':
                        mc.rename(sh, node+'Shape')
            return

        else:
            mc.select(badones)
            msg = 'Bad shape nodes found:\n'
            msg += '\n'.join(badones)
            return str(msg)
    return True

def fixBadShapes(*args):
    checkBadShapes(fix=True)

def checkSets():
    rset = mc.ls('geoSet_*', type = 'objectSet')
    if rset:
        return True

def fixSets(*args):
    nodes = mc.ls('|*')
    for n in ['front','persp','side','top']:
        nodes.remove(n)
    if nodes:
        mc.select(nodes)