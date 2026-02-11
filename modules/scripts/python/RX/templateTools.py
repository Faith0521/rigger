import maya.cmds as mc
import inspect
import os

from rxCore import aboutLock
import controlTools
import importMod

# Creates the top node hierarchy for template comonents
def createTopNode(part, args=None, lockArgs=None):

    if args is None:
        args = {}
    if lockArgs is None:
        lockArgs = []

    part = part.split('.')[-1]

    # creatre template
    if not mc.objExists('template'):
        mc.createNode('transform', n='template')
        mc.connectAttr ('template.sy', 'template.sx')
        mc.connectAttr ('template.sy', 'template.sz')
        aboutLock.lock('template', 't r v sx sz')
        mc.aliasAttr ('globalScale', 'template.sy')

    # create top node name
    side, prefix = '',''
    if 'side' in args.keys():
        if not args['side'] == 'cn': # if the side value not "cn", get current side value.
            side=args['side']

    os.environ['rxNOPREFIX'] = 'False' # design prefix env
    if 'prefix' in args.keys():
        prefix = args['prefix']

        # resolve prefix
        tokens = prefix.strip().split('_')
        text = tokens[0]
        for t in tokens[1:]:
            if t:
                text += t[0].capitalize()+t[1:]

        tokens = text.strip().split(' ')
        prefix = tokens[0]
        for t in tokens[1:]:
            if t:
                prefix += t[0].capitalize()+t[1:]
        args['prefix'] = prefix
    else:
        os.environ['rxNOPREFIX'] = 'True'

    if prefix:
        prefix += '_'

    if side:
        prefix = side+'_'+prefix

    prefix = prefix
    topnode = 'RXPREFIX'+prefix+part
    #topnode = prefix+part


    # Name check
    if mc.objExists(topnode):
        os.environ['rxCURRENT_TOPNODE'] = ''
        return

    if part == 'base' and mc.objExists('base'):
        os.environ['rxCURRENT_TOPNODE'] = ''
        mc.confirmDialog( title='Base already exists!', message='Cannot build a second base.', icon ='warning', button=['OK'])
        return

    if part == 'cog' and mc.objExists('cog'):
        os.environ['rxCURRENT_TOPNODE'] = ''
        mc.confirmDialog( title='Cog already exists!', message='Cannot build a second cog.', icon ='warning', button=['OK'])
        return

    ctrl = controlTools.create(topnode, shape='D07_circle', scale=2, color='black', tag='templateCtrl' , makeGroups=False)[0]
    topnode = mc.rename (ctrl, topnode)

    attrs = ['controlID','tagKeyable','tag']
    for a in attrs:
        mc.deleteAttr(topnode+'.'+a)

    # Create node heriarchy
    ctrls = mc.createNode('transform', n=topnode+'Ctrls',p=topnode)
    jnts = mc.createNode('transform', n=topnode+'Joints',p=topnode)
    planes = mc.createNode('transform', n=topnode+'Planes',p=topnode)
    nox = mc.createNode('transform', n=topnode+'Nox',p=topnode)

    mc.setAttr(jnts+'.inheritsTransform', 0)
    mc.setAttr(nox+'.inheritsTransform', 0)
    mc.setAttr(nox+'.it', l=1)

    mc.addAttr(topnode, ln='ctrlDisplay', at='long', min=0, max=1, dv=1, k=1)
    mc.addAttr(topnode, ln='jointDisplay', at='long', min=0, max=2,dv=1, k=1)

    mc.connectAttr(topnode+'.jointDisplay', jnts+'.v')
    mc.connectAttr(topnode+'.ctrlDisplay', ctrls+'.v')

    mc.setDrivenKeyframe(jnts+'.overrideDisplayType', v=0, dv=2, cd=topnode+'.jointDisplay')
    mc.setDrivenKeyframe(jnts+'.overrideDisplayType', v=2, dv=1, cd=topnode+'.jointDisplay')
    mc.setAttr(jnts+'.overrideEnabled', 1)

    mc.parent(topnode,'template')
    aboutLock.lock([nox, ctrls, jnts, planes])

    # Record args to top node
    recordArgs(topnode, part, args, lockArgs)

    os.environ['rxCURRENT_TOPNODE'] = topnode
    return topnode, 'RXPREFIX'+prefix

#   Record build args to top component node
def recordArgs(topnode, part, args, lockArgs=None):

    # Create strign for all args and their values.
    if lockArgs is None:
        lockArgs = []

    args = '{0}'.format(args)
    if lockArgs:
        lockArgs = '{0}'.format(lockArgs)

    # Record ars strings to top node.
    attrs = ['rigPart','rigPartArgs','rigPartLockArgs']
    for a in attrs:
        if not mc.objExists(topnode+'.'+a):
            mc.addAttr(topnode, ln=a, dt='string')
            mc.setAttr(topnode+'.'+a, '', type='string')
        mc.setAttr(topnode+'.'+a, l=0)

    mc.setAttr(topnode+'.rigPart', part, type='string',)
    mc.setAttr(topnode+'.rigPartArgs', args, type='string')

    if lockArgs:
        mc.setAttr(topnode+'.rigPartLockArgs', lockArgs, type='string')

    for a in attrs:
        mc.setAttr(topnode+'.'+a, l=1)

def resolveTempPrefix():
    topnode = os.environ['rxCURRENT_TOPNODE']
    if not mc.objExists(topnode):
        return ''

    nodes = mc.ls('*RXPREFIX*')
    if not nodes:
        return

    # set topnode in front of all item in nodes
    nodes.remove(topnode)
    nodes.insert(0, topnode)

    newnames = []
    for n in nodes:
        newnames.append(n.replace('_RXPREFIX_', '_').replace('RXPREFIX_', '').replace('RXPREFIX', ''))

    # check and promot for new prefix
    side = getArgs(topnode, 'side')
    prefix = getArgs(topnode, 'prefix')
    newprefix = getPrefix(side, prefix)

    passCheck = checkNames(newnames, nodes)
    while not passCheck:
        if os.environ['rxNOPREFIX'] == 'True':
            if 'cog' in topnode:
                msg = 'You cannot have a "cog" and "torso" part in the same template. Choose one.'
            else:
                msg = 'Can only have one instance of this part. Removing duplicate.'

            mc.confirmDialog(   title='Connot Build Part!',
                                message=msg,
                                icon ='critical',
                                button=['OK'] )

            mc.delete(topnode)
            passCheck = True
            return

        if 'torso' in topnode and mc.objExists('cog'):
            msg = 'You cannot have a "cog" and "torso" part in the same template. Choose one.'
            mc.confirmDialog( title='Connot Build Part!',
                message=msg,
                icon ='critical',
                button=['OK'])

            mc.delete (topnode)
            passCheck = True
            return

        result = mc.promptDialog(
                title='Set Prefix',
                message='You must change the prefix to avoid duplicate names!\n\nNew prefix:',
                button=['OK', 'Remove Part'],
                defaultButton='OK',
                dismissString='Remove Part',
                text='')
        if result =='Remove Part':
            mc.delete(nodes[0])
            return

        # rebuild prefix
        text = mc.promptDialog(query=1, text=1).strip().replace(' ','_')
        tokens = text.strip().split('_')
        text = tokens[0]
        for t in tokens[1:]:
            if t:
                text += t[0].capitalize()+t[1:]

        newprefix = getPrefix(side, text)
        newnames = []

        for n in nodes:
            newnames.append( n.replace('RXPREFIX'+prefix, newprefix).replace('RXPREFIX_', newprefix).replace('RXPREFIX', newprefix) )
        passCheck = checkNames(newnames, nodes)
        newargs = getArgs(topnode)
        newargs['prefix'] = text

        recordArgs(topnode, mc.getAttr(topnode+'.rigPart'), newargs)

    # rename node to new prefix
    for i in range(len(newnames)):
        if mc.objExists(nodes[i]):
            mc.rename(nodes[i], newnames[i])

    # rename expression nodes
    exp = mc.ls(newnames[0] + '_exp')
    if exp:
        expArg = mc.expression(exp, q=True, s=True)
        for i in range(len(newnames)):
            if nodes[i] in expArg:
                expArg = expArg.replace(nodes[i], newnames[i])
        mc.expression(exp, e=True, s=expArg)

    mc.select(newnames[0])
    return newprefix

def checkNames(newnames, nodes):
    allnodes = mc.ls()
    passCheck = True
    for i in range(len(newnames)):
        if mc.listRelatives(nodes[i], p=1):
            if newnames[i] in allnodes:
                passCheck = False
    return passCheck

# this queries a python module and returns is arguments, default values and path
def getModuleInfo(part):
    module = importMod.import_module(part)
    if not module:
        return []

    func = module.template
    labels = list(inspect.getfullargspec(func).args)

    if inspect.getfullargspec(func).defaults:
        values = list(inspect.getfullargspec(func).defaults)
    else:
        values = []

    modulepath = os.path.abspath(module.__file__.replace('.pyc','.py'))
    return [labels, values, modulepath]

#   Get build args to top component node, if no arg is specified it will rreturn ALL build args
def getArgs(topnode, arg=None):

    if not mc.objExists(topnode+'.rigPart'):
        return
    # get args
    args = eval(mc.getAttr(topnode+'.rigPartArgs'))
    if arg == 'side' or arg == 'prefix':  # want get side and prefix if arg not None.
        rarg = args.get(arg, '')
    else:
        rarg = args.get(arg, args)
    return rarg

# Create joints to use in template builds
def createJoint(name, topnode, color='blue', makeGroups=True, ctrlOnly=False, pc=1, oc=0):

    jnt = controlTools.create(name, shape='jack', color=color, tag='templateJointCtrl', jointCtrl=True, makeGroups=makeGroups)
    for i in range (len(jnt)):
        jnt[i] = mc.rename(jnt[i] , jnt[i].replace('_ctrl','_pos'))

    mc.delete(mc.listRelatives(jnt[-1], s=1))
    mc.select(jnt[-1])
    mc.toggle(rotatePivot=1)
    mc.setAttr(jnt[-1]+'.drawStyle', 0)
    mc.setAttr(jnt[-1]+'.radi', 1)

    if ctrlOnly:
        return jnt

    # create the actual joint
    # put part+Joints
    actualJnt = mc.createNode('joint', n=name, p=topnode+'Joints')
    jnt.append(actualJnt)
    mc.addAttr(jnt[-1], ln='tag', dt='string')
    mc.setAttr(jnt[-1]+'.tag', 'templateJoint', type='string')

    if pc:
        mc.pointConstraint(jnt[-2], jnt[-1], n=jnt[-1]+'_pc')
    if oc:
        mc.orientConstraint(jnt[-2], jnt[-1], n=jnt[-1]+'_oc')

    mc.setAttr(jnt[-2]+'.radi', 1.25)
    mc.setAttr(jnt[-2]+'.displayHandle', 0)
    mc.connectAttr(jnt[-2]+'.ro', jnt[-1]+'.ro')
    aboutLock.unlock(jnt[-2], 'jox joy joz ro')

    return jnt


def writePartsFile(path):

    if not os.path.isdir (path):
        return

    filepath = os.path.abspath (os.path.join (path, 'templateParts.py'))

    cmpts = mc.listRelatives('template',c=1, type='transform')
    parts = []

    if cmpts:
        for c in cmpts:
            if mc.objExists(c+'.rigPart'):
                if mc.getAttr(c+'.rigPart') not in parts:
                    parts.append(mc.getAttr(c+'.rigPart'))

    if 'base' in parts:
        parts.remove('base')
    parts.insert (0, 'base')

    arg =  '#########################################\n'
    arg += '#   Rig Build - Components function file\n'
    arg += '\n'
    arg += 'def parts():\n'
    arg += '    return {0}\n'.format(parts)
    arg += '\n'

    functionsfile= open(filepath, 'w')
    functionsfile.write(arg)
    functionsfile.close()
    return filepath

# Geet types of rig parts to build (anim, proxy etc)
def getRigBuildType(buildType):
    return buildType


def getParts(partType):
    if not mc.objExists('partsPrep'):
        return[]

    parts = []
    nodes = mc.listRelatives('partsPrep')
    for n in nodes:
        if mc.objExists (n+'.rigPart'):
            ptype = mc.getAttr (n+'.rigPart')
            if ptype == partType:
                parts.append(n)
    return parts


def getPrefix(side, prefix):

    if prefix is None:
        prefix = ''
    if side is None:
        side = ''

    elif 'lf' in side or 'rt' in side:
        side = side.replace('_', '').strip()
        side+='_'
    else:
        side = ''

    if prefix:
        prefix = prefix.replace('_','').strip()
        prefix += '_'

    prefix = side+prefix
    prefix = prefix.replace('__','_')

    return prefix


def validateOptions():

    # check parts require nodes

    if not mc.objExists('|template'):
        return

    parts = mc.listRelatives('template', c=1)

    passCheck = True
    msg = 'Some parts parent nodes that do not exist.\n\n'

    pcheck = True
    tmsg = ''
    for topnode in parts:

        options = getArgs(topnode)
        lockArgs = eval(mc.getAttr(topnode+'.rigPartLockArgs'))

        tmsg = '  {0}\n'.format(topnode)

        for label, value in options.items():
            if label not in lockArgs:
                if type(value) is list or label == 'parent':
                    skip = 0
                    for v in value:
                        if '.' in v:
                            skip = 1
                    if not skip:
                        nodes = mc.ls(value)
                        if not nodes:
                            tmsg += '    {0} : "{1}" ---- Exist Failed\n'.format(label, value)
                            passCheck = False
                            pcheck = False

    if not pcheck:
        msg += tmsg+'\n'

    if not passCheck:
        mc.confirmDialog( title='Export failed !',
                    message=msg,
                    icon ='warning',
                    button=['OK'])
        print (msg)
        return False

    else:
        return True




