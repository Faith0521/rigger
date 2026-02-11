import maya.cmds as mc
import controlTools
from rxCore import aboutName

# Space arg should be formated as follows:  'label:driver label:driver label:driver'
def tag(node, spaceArg, oo=False, con=None, dv=0):
    nodes = mc.ls(node)

    if con is None:
        con = mc.ls(node+'_grp')
        if con:
            con = con[0]
        else:
            con = mc.listRelatives(node, p=1)
            if con:
                con=con[0]
            else:
                return

    # boole to string
    if oo:
        oo = 'True'
    else:
        oo = 'False'

    for n in nodes:
        # if haven't, add new tagSpace
        if not mc.objExists(n+'.tagSpaces'):
            mc.addAttr(n, ln="tagSpaces", dt="string")

        # set tagSpaces
        mc.setAttr(n+'.tagSpaces', l=0)
        mc.setAttr(n+'.tagSpaces', 'DV:{0} OO:{1} CON:{2} {3}'.format(dv, oo, con, spaceArg), type='string')

        # set tagKeyable
        if mc.objExists(n+'.tagKeyable'):
            if not 'space' in mc.getAttr(n+'.tagKeyable'):
                controlTools.tagKeyable(n, 'space', add=1)

    return spaceArg


# Create spaces on ctrl. Space Arg must be formatted like this: 'enumlabel:spaceDriver enumlabel:spaceDriver'
def create(ctrl, parent, spaceArg, oo=False, dv=0, mpNode=None):

    # spaceArg = parent:chest cog:cogGrp worldCtrl:controls world:noTransform
    if not mpNode:
        mpNode = ctrl+'_spaces'
        mc.createNode('transform', n=mpNode)
        mc.addAttr(mpNode, ln='rigBuildNode', at='message')
        
    top = mc.ls( 'controls', 'worldOffset')
    if top:
        mc.parent(mpNode, top[0])

    spaces = spaceArg.split(' ')
    prc, enum = '', ''

    for i in range(len(spaces)):

        driver = spaces[i].split(':')[1]
        enum += spaces[i].split(':')[0]+':'

        if not mc.objExists(driver):
            driver = 'root'
        
        spc = mc.createNode('transform', n=aboutName.unique(ctrl+'_'+driver+'_spc'))
        mc.delete( mc.parentConstraint(ctrl, spc) )
        mc.parentConstraint(driver, spc, mo=1, n=spc+'_prc')
        mc.addAttr(spc, ln='rigBuildNode', at='message')
        mc.setAttr(spc+'.ro', mc.getAttr(parent+'.ro'))
        mc.parent(spc, mpNode)

        if oo:
            prc = mc.orientConstraint(spc, parent, mo=1, n=parent+'_oc')[0]
            mc.setAttr(prc+'.interpType', 2)
        else:
            prc = mc.parentConstraint(spc, parent, mo=1, n=parent+'_prc')[0]
            mc.setAttr(prc+'.interpType', 2)

    mc.addAttr(prc, ln='rigBuildNode', at='message')
    mc.addAttr(ctrl, ln='space', at='enum', en=enum, dv=dv, k=1 )

    for i in range(len(spaces)):
        mc.setDrivenKeyframe(prc+'.w{0}'.format(i), cd=ctrl+'.space', v=0, dv=i-1)
        mc.setDrivenKeyframe(prc+'.w{0}'.format(i), cd=ctrl+'.space', v=1, dv=i)
        mc.setDrivenKeyframe(prc+'.w{0}'.format(i), cd=ctrl+'.space', v=0, dv=i+1)
