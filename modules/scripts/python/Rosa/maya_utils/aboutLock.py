import maya.cmds as mc
import maya.mel as mel
import re



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def set(nodes='', at='t r s jo u v ro', l=True, k=False):

    nodes = mc.ls(nodes)
    if not len(nodes):
        nodes = mc.ls(nodes)
    if nodes is not None:   
        if not len(nodes):
            nodes = mc.ls(sl=1)

    at = ' '+at+' '
    if re.search(' t ', at):
        at = re.sub(' t ',' tx ty tz ', at)
    if re.search(' r ', at):
        at = re.sub(' r ',' rx ry rz ', at)
    if re.search(' s ', at): 
        at = re.sub(' s ',' sx sy sz ', at)
    if re.search(' jo ', at):
        at = re.sub(' jo ',' jox joy joz roo radi ', at)

    ud = ''
    if re.search(' u ', at):
        for node in nodes:
            uds = mc.listAttr(node, ud=1)
            if uds is not None:
                ud += ' '.join(mc.listAttr(node, ud=1))+' '

        ud = ' '+ud.strip()+' '
        at = re.sub(' u ', ud, at)

    at = at.replace('  ', ' ').strip()
    attributes = at.split(' ')
    attributes.sort()

    for n in nodes:
        for a in attributes:
            if mc.objExists(n+'.'+a) and a:
                na = (n+'.'+a)
                mc.setAttr(na,l=l)
                mc.setAttr(na,k=k)  

                if l and not k and mc.getAttr (na, l=1) and not mc.getAttr (na, k=1): 
                    mc.setAttr(na, cb=k)



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def lock(nodes=None, at='t r s jo u v ro'):
    if not nodes:
        nodes=mc.ls(sl=1)
    else:
        nodes=mc.ls(nodes)
    set(nodes=nodes, at=at, l=1, k=0)



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def unlock(nodes=None, at='t r s jo u v ro'):
    if not nodes:
        nodes=mc.ls(sl=1)
    else:
        nodes=mc.ls(nodes)
    set(nodes=nodes, at=at, l=0, k=1)



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def countLock(nodes):

    if not nodes:
        return

    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status='Locking Nodes ...',
    maxValue=len(nodes) )

    for node in nodes:

        mc.progressBar(gMainProgressBar, edit=True, step=1)

        at = mc.listAttr(node, k=1)
        attrs = []
        if at is not None:
            attrs.extend(at)
        at = mc.listAttr(node, cb=1)
        if at is not None:
            attrs.extend(at)
            
        for a in attrs:
            if mc.objExists(node+'.'+a):
                mc.setAttr(node+'.'+a, l=1,k=0)
                if mc.getAttr (node+'.'+a, l=1) and not mc.getAttr (node+'.'+a, k=1): 
                        mc.setAttr(node+'.'+a, cb=0)

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def unlockTagged(nodes):
    if not nodes:
        return

    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status='unLocking Nodes ...',
    maxValue=len(nodes) )

    for n in nodes:
        mc.progressBar(gMainProgressBar, edit=True, step=1)
        at=None
        if mc.objExists(n+'.tagKeyable'):
            at = mc.getAttr(n+'.tagKeyable')
            if not at:
                at = 'space'
            else:
                at +=' space'

            if at:
                unlock(n, at=at)

        splits = mc.ls(n+'.__', n+'.___', n+'.____')
        for s in splits:
            mc.setAttr(s, cb=1, l=0, k=0)

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
