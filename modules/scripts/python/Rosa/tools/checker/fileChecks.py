import os, time

import maya.cmds as mc
import maya.mel as mel
from ... maya_utils import aboutName
import assetEnv

#-------------------------------------------------------------#
# CORE CHECK LIST
#-------------------------------------------------------------#

def del_Layers():
    """Delete Unneeded Layer"""
    layers = mc.ls(type=('renderLayer', 'displayLayer'))
    if 'defaultRenderLayer' in layers:
        layers.remove('defaultRenderLayer')
    if 'defaultLayer' in layers:
        layers.remove('defaultLayer')

    if layers:
        mc.delete(layers)
    return True

def check_RefNodes():
    if mc.ls(type='reference'):
        return 'You cannot have live references in your rig!\nMake sure you import any references and remove their namespaces.'
    return True
    
def check_NameSpaces():
    nss = mc.namespaceInfo(lon=1, r=1)
    if 'UI' in nss:
        nss.remove('UI')
    if 'shared' in nss:
        nss.remove('shared')
    if nss:
        mel.eval('NamespaceEditor;')
        return 'Namespaces found!\nUse the namespace editor to remove all namespaces from your scene.'
    return True

def check_camsLightsImgPlanes():
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

def fix_camsLightsImgPlanes():
    """Delete cameras / lights / image planes"""
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

def getSameNames():
    nodes = mc.ls(sn=1)
    sames = []
    for n in nodes:
        if '|' in n:
            sames.append(n)
    return sames

def check_SameNames():

    sames = getSameNames()

    if sames:
        msg = 'Same node names found! See script editor for details.\n\nsame Names:\n'
        mc.select(sames)
        i = 1
        for d in sames:
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


def sameNamesFixUI():
    if mc.window('mcheckUI',q=1,ex=1):
        mc.deleteUI('mcheckUI')
    win = mc.window('mcheckUI',t='Fix Sames Names', s=1)
    mc.columnLayout(adj=True, rs = 5, co=['both', 10])
    mc.separator(st='none')

    msg = '''\tFix same node names?.

    NOTE: This will rename all same nodes in your scene. Are you sure?\nAlternatively you can resolve this yourself.'''

    mc.text(msg)
    mc.button(label='Fix', c=fix_SameNames)
    mc.showWindow(win)
    mc.window(win, e=1,  wh=[500, 105], s=0)
    return 'PENDING'

def fix_SameNames():
    if mc.window('mcheckUI',q=1,ex=1):
        mc.deleteUI('mcheckUI')


    i = 0
    while getSameNames() and i < 20:
        for d in getSameNames():
            if mc.objExists(d):
                nn = aboutName.unique(d.split('|')[-1])
                mc.rename(d, nn)
        i += 1

def check_BadShapes():
    badones = []

    # get mesh list
    mc.SelectAllGeometry()
    nodes = mc.ls(sl=1)
    mc.select(cl=1)

    for node in nodes:
        shapes = mc.listRelatives(node, s=1, ni=1)
        if len(shapes) > 1:
            badones.append(node)

        for shape in shapes:
            if not shape == node + 'Shape':
                badones.append(shape)

    if badones:
        mc.select(badones)
        msg = 'Bad shape nodes found:\n'
        msg += '\n'.join(badones)
        return str(msg)

    return True

def fix_BadShapes():

    # get mesh list
    mc.SelectAllGeometry()
    nodes = mc.ls(sl=1)
    mc.select(cl=1)

    for node in nodes:

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

def check_Hierarchy():
    nodes = mc.ls('|*')
    for n in ['front','persp','side','top']:
        nodes.remove(n)

    if len(nodes) == 1:
        return True
    else:
        return 'Must have one single hierarchy in your scene.\nPlease clean up!'


#-------------------------------------------------------------#
# MODEL CHECK LIST
#-------------------------------------------------------------#



#-------------------------------------------------------------#
# RIG CHECK LIST
#-------------------------------------------------------------#

def check_Ctrls():
    nodes = []
    os.environ['RIGCHECK_CTRLS'] = ''
    if mc.objExists('*worldOffset|controls.rigBuildNode'):
        mc.select('controls', hi=1)
        nodes = mc.ls(sl=1, type='nurbsCurve')

        ctrls = []
        for n in nodes:
            ctrls.append(mc.listRelatives(n, p=1)[0])

        ctrls.extend(mc.ls('*.controlID'))
        ctrls = list(set(ctrls))
        for i in range(len(ctrls)):
            ctrls[i] = ctrls[i].split('.')[0]

    else:
        nodes = mc.ls(type='nurbsCurve')
        ctrls = []
        for n in nodes:
            p = mc.listRelatives(n, p=1)[0]
            if p not in os.environ['RIGCHECK_MODELHI']:
                ctrls.append(mc.listRelatives(n, p=1)[0])
        ctrls = list(set(ctrls))

    asset = 'test'
    aset = mc.ls('animSet_*'.format(assetEnv.getasset()), type = 'objectSet')
    if aset:
        current = mc.sets(aset[0], q=1, no=1)
        if current:
            ctrls = list(set(ctrls+current))

    for c in ctrls:
        if mc.objExists(c+'.controlID'):
            mc.setAttr(c+'.controlID', l=0)
            mc.deleteAttr(c+'.controlID')

        mc.addAttr(c, ln='controlID', dt='string')
        mc.setAttr(c+'.controlID', c, type='string')

        if not mc.listRelatives(c, s=1):
            mc.deleteAttr(c+'.controlID')
            ctrls.remove(c)

    os.environ['RIGCHECK_CTRLS'] = ' '.join(ctrls)
    return True
    

def check_Sets(fix=False):

    rset = mc.ls('rigSet_*', type = 'objectSet')
    aset = mc.ls('animSet_*', type = 'objectSet')
    cset = mc.ls('cacheSet_*', type = 'objectSet')

    if fix:
        if rset:
            aset = [rset[0].replace('rigSet_', 'animSet_')]
            cset = [rset[0].replace('rigSet_', 'cacheSet_')]

        else:
            result = mc.promptDialog(
            title='Create Asset Rig Sets',
            message='Current Asset:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel',
            text=assetEnv.getasset())

            if result == 'OK':
                asset = mc.promptDialog(query=True, text=True).strip()
                rset = ['rigSet_'+asset]
                aset = [rset[0].replace('rigSet_', 'animSet_')]
                cset = [rset[0].replace('rigSet_', 'cacheSet_')]
            else:
                return

    else:
        if not rset or not aset or not cset or not mc.objExists(rset[0]+'.setType') or not mc.objExists(aset[0]+'.setType') or not mc.objExists(cset[0]+'.setType'):
            return 


    if mc.objExists(rset[0]):
        mc.delete(rset)
    rset[0] = createSet(rset[0], 'rig', topnode[0])
    mc.sets(topnode, add=rset[0])
        
    # anim set
    ctrls = os.environ['RIGCHECK_CTRLS'].split(' ')
    for c in ctrls:
        if not mc.objExists(c):
            return c+' no longer exists! Make sure you use the sane rig throughout the check process!'

    if mc.objExists(aset[0]):
        mc.delete(aset)
    aset[0] = createSet(aset[0], 'animCurves', ctrls)
    mc.sets(ctrls, add=aset[0])
    mc.sets(aset, add=rset[0])

    # geo set
    geos = os.environ['RIGCHECK_MODELHI'].split(' ')
    for c in geos:
        if not mc.objExists(c):
            return c+' no longer exists! Make sure you use the sane rig throughout the check process!'

    if mc.objExists(cset[0]):
        mc.delete(cset)
    cset[0] = createSet(cset[0], 'geometryCache', geos)
    mc.sets(geos, add=cset[0])
    mc.sets(cset, add=rset[0])
    return True

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

def fix_Sets():
    check_Sets(True)

def check_Play():

    test = mc.confirmDialog( title='Rig Check Animation', message='Play Animation?\n\nYour rig seems legit!\nDo you want to run through a quick animation to test your rig?\nHit escape to cancel at any time.', 
        button=['Yes','Skip'], 
        defaultButton='Yes', 
        cancelButton='Skip', 
        dismissString='Skip')
    if test == 'Yes':
        result = play()
        return result

    return True

def playCam(topnode):

    mel.eval('''setNamedPanelLayout "Single Perspective View"; updateToolbox();
    optionVar -query animateRollViewCompass;
    viewSet -home;
    viewSet -p -an 1 |persp|perspShape;''')

    tmp = mc.createNode('transform', n='perspPar')
    tmp2 = mc.createNode('transform', p='perspPar')
    mc.pointConstraint(topnode, tmp)
    
    bb = mc.exactWorldBoundingBox(topnode, ii=1)
    pos = [
                (bb[3]-bb[0]),
                (bb[4]-bb[1])*2,
                (bb[5]-bb[2])]

    cube = mc.polyCube(ch=0)
    mc.xform(cube, r=1, s=pos)

    mc.select(cube)
    mel.eval('fitPanel -selected;')
    pos = mc.xform('persp', q=1, a=1, t=1)
    mc.xform('persp', a=1, t=[pos[0]*1.5, pos[1]*1.5, pos[2]*1.5])
    mc.delete(cube)

    mc.delete(mc.pointConstraint('persp', tmp2))
    mc.pointConstraint(tmp2, 'persp')
    mc.select(cl=1)

def killCam():
    mc.delete('perspPar')
    
def play(delay=0.1):

    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar( gMainProgressBar, e=True, bp=True, ii=True, st='Running Rig Test ...', maxValue=3 )

    topnode = ''
    rigtype = ''
    nodes = mc.ls('worldA_ctrl', 'worldTransform')
    if nodes and mc.objExists(nodes[0]+'.UniformScale') and mc.objExists(nodes[0]+'.modelDisplay'):
        topnode = nodes[0]
        rigtype = 'ftrack'

    elif mc.ls('global_CTRL'):
        nodes = mc.ls('global_CTRL')
        if nodes and mc.objExists(nodes[0]+'.modelType') and mc.objExists(nodes[0]+'.skeletonType'):
            topnode = nodes[0]
            rigtype = 'hub'
    else:
        nodes = mc.ls(sl=1)
        if nodes:
            topnode = nodes[0]

    if not topnode:
        msg = 'If your rig was not built using the HUB Tools or the LA Rig Tools,\nselect the top transformable node of your rig and re-run the checks.\n\nMake sure the translate, rotate and scale channels are all unlocked.'
        mc.confirmDialog(message = msg, title='Select Top Node', icon='information')
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        return

    # play through anim 
    mc.select(cl=1)
    mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

    playCam(topnode)

    mc.inViewMessage( amg='Testing rig <hl>uniform scale</hl>.', pos='botCenter', fade=1 )
    mc.refresh()

    for i in reversed(range(1, 11)):
        mc.xform(topnode, a=1, s=[i*.1, i*.1, i*.1])
        time.sleep(delay)
        mc.refresh()

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 11):
        time.sleep(delay)
        mc.refresh()
        mc.xform(topnode, a=1, s=[i*.1, i*.1, i*.1])

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 9):
        time.sleep(delay)
        mc.refresh()
        mc.xform(topnode, a=1, s=[i, i, i])
        
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(1, 9)):
        time.sleep(delay)
        mc.refresh()

        mc.xform(topnode, a=1, s=[i, i, i])
        
    mc.inViewMessage( amg='Testing rig <hl>world transform & rotate</hl>.', pos='botCenter', fade=1 )
    mc.refresh()

    bb = mc.exactWorldBoundingBox(topnode)
    mult = ((bb[3]+bb[4]+bb[5]) / 3) - ((bb[0]+bb[1]+bb[2]) / 3) 

    mc.progressBar(gMainProgressBar, edit=True, step=1)
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(0, 21):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.t', i*mult, i*mult, -i*mult)
        
    for i in reversed(range(0, 21)):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.t', i*mult, i*mult, -i*mult)
        
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.', i*20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.ry', i*20)   

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in range(1, 10):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.rz', i*20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode+'.', i*20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode+'.ry', i*20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 10)):
        time.sleep(delay)
        mc.refresh()

        mc.setAttr(topnode+'.rz', i*20)

    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    for i in reversed(range(0, 1)):
        time.sleep(delay)
        mc.refresh()
        mc.setAttr(topnode+'.t', i*mult, i*mult, -i*mult)
        
    mc.progressBar(gMainProgressBar, edit=True, step=1)
    if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
        mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
        mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
        killCam()
        return True

    if rigtype == 'hub':

        mc.inViewMessage( amg='Testing visibility switch for <hl>model.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.modelVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelType', 0)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage( amg='Testing visibility switch for <hl>skeleton.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.skeletonVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.skeletonVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.skeletonType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.skeletonType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.skeletonType', 0)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage( amg='Testing visibility switch for <hl>controls.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.controlVis', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.controlVis', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.controlType', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.controlType', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.controlType', 0)
        time.sleep(1)
        mc.refresh()

    if rigtype == 'ftrack':

        mc.inViewMessage( amg='Testing visibility switch for <hl>model.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.modelDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelDisplay', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.modelDisplay', 1)
        time.sleep(1)
        mc.refresh()

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage( amg='Testing visibility switch for <hl>skeleton.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.jointDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.jointDisplay', 2)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.jointDisplay', 1)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.jointDisplay', 0)

        if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
            mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
            mc.xform(topnode, a=1, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            mc.inViewMessage( amg='<hl>Cancelled</hl>', pos='botCenter', fade=1)
            killCam()
            return True

        mc.inViewMessage( amg='Testing visibility switch for <hl>controls.</hl>.', pos='botCenter', fade=1 )
        mc.setAttr(topnode+'.ctrlDisplay', 0)
        time.sleep(1)
        mc.refresh()

        mc.setAttr(topnode+'.ctrlDisplay', 1)
        time.sleep(1)
        mc.refresh()

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
    mc.inViewMessage( amg='<hl>Finished. All good?</hl> Go forth and publish!', pos='botCenter', fade=1)
    killCam()
    return True
