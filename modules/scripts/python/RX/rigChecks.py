import maya.cmds as mc
import maya.mel as mel

import os,time

from rxCore import aboutName
import assetEnv

def mrDag():
    nodes = mc.ls('mr_display_driver_dag', '*mr_display_driver_dag*')
    if nodes:
        mc.delete(nodes)
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
        return 'You cannot have live references in your rig!\nMake sure you import any references and remove their namespaces.'
    return True
    
def namespaces():
    nss = mc.namespaceInfo(lon=1, r=1)
    if 'UI' in nss:
        nss.remove('UI')
    if 'shared' in nss:
        nss.remove('shared')
    if nss:
        mel.eval('NamespaceEditor;')
        return 'Namespaces found!\nUse the namespace editor to remove all namespaces from your scene.'
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

def camsLightsImgPlanesfix():
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

def dupNames():
    nodes = mc.ls(sn=1)
    dups = getDups()

    if dups:
        msg = 'Duplicate node names found! See script editor for details.\n\nDuplicate Names:\n'
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

def getDups():
    nodes = mc.ls(sn=1)
    dups = []
    for n in nodes:
        if '|' in n:
            dups.append(n)

    return dups

def dupNamesFixUI(*args):
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
    os.environ['RIGCHECK_TOPNODE'] = ''
    if mc.ls('mr_display_driver_dag', '*mr_display_driver_dag*'):
        mc.delete(mc.ls('mr_display_driver_dag', '*mr_display_driver_dag*'))
    nodes = mc.ls('|*')
    for n in ['front',
     'persp',
     'side',
     'top']:
        nodes.remove(n)

    if len(nodes) == 1:
        os.environ['RIGCHECK_TOPNODE'] = nodes[0]
        return True

    return 'Must have one single hierarchy in your rig scene.\nPlease clean this up!'

def checkModelHi():
    geos = []
    ok = False
    if 'RIGCHECK_MODELHI' in os.environ.keys():
        geos = os.environ['RIGCHECK_MODELHI'].split(' ')
    if geos:
        ok = True
        for g in geos:
            if not mc.objExists(g):
                ok = False

    if ok:
        return True

    os.environ['RIGCHECK_MODELHI'] = ''
    if mc.objExists('model.rigBuildNode'):
        mc.select('model', hi=1)
        nodes = mc.ls(sl=1, type='mesh')
        nodes.extend(mc.ls(sl=1, type='nurbsCurve'))

        if nodes:
            geos = []
            for n in nodes:
                geos.append(mc.listRelatives(n, p=1)[0])
            if geos:
                os.environ['RIGCHECK_MODELHI'] = ' '.join(geos)
                return True

    if mc.window('mcheckUI',q=1,ex=1):
        mc.deleteUI('mcheckUI')
    win = mc.window('mcheckUI', t='Model Hierarchy Check', s=1)
    mc.columnLayout(adj=True, rs = 5, co=['both', 10])
    mc.separator(st='none')

    msg = '''\tPlease select the top node of your model.

    NOTE: Your model must remain under the same single hierarchy as it was when imported, 
    otherwise your geo cache will have issues down the line. You should not be splitting out your model.

    Also, make sure you DO NOT have any rig nodes grouped under your model.
    Those rig nodes will export out with your rig and may cause problems.
    '''

    mc.text(msg)
    mc.button( label='Select', c=checkMhi )
    mc.showWindow(win)
    mc.window(win,e=1,  wh=[515, 145], s=0)
    return 'PENDING'

def checkMhi(*args):
    mc.select(hi=1)
    nodes = mc.ls(sl=1, type='mesh')
    nodes.extend(mc.ls(sl=1, type='nurbsCurve'))
    if nodes:
        geos = []
        for n in nodes:
            geos.append(mc.listRelatives(n, p=1)[0])

        if geos:
            os.environ['RIGCHECK_MODELHI'] = ' '.join(geos)

            if mc.window('mcheckUI',q=1,ex=1):
                mc.deleteUI('mcheckUI')
    mc.select(cl=1)

def checkCtrls():
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
    
def checkBadShapes():
    badones = []
    nodes = os.environ['RIGCHECK_MODELHI'].split(' ')

    for node in nodes:
        if not mc.objExists(node):
            print (node+' no longer exists! Make sure you use the sane rig throughout the check process!')

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

def fixBadShapes(*args):
    nodes = os.environ['RIGCHECK_MODELHI'].split(' ')
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

def checkSets(fix=False):

    rset = mc.ls('rigSet_*', type='objectSet')
    aset = mc.ls('animSet_*', type='objectSet')
    cset = mc.ls('cacheSet_*', type='objectSet')

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

    # Rig set 
    topnode = mc.ls(os.environ['RIGCHECK_TOPNODE'])
    if not topnode:
        return topnode[0]+' no longer exists! Make sure you use the sane rig throughout the check process!'

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

def fixSets():
    checkSets(1)

def playCheck():

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

        mc.setAttr(topnode+'.rx', i*20)

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

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
    mc.inViewMessage( amg='<hl>Finished. All good?</hl> Go forth and publish!', pos='botCenter', fade=1)
    killCam()
    return True
