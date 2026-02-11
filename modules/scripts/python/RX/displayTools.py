import maya.cmds as mc

# Options: 'normal' 'template' 'reference' 'off'
def set(display, nodes=None, shape=True):

    if nodes is None:
        nodes=mc.ls(sl=1, l=1)

    for n in nodes:

        cn=mc.listConnections(n+'.overrideEnabled')
        cnb=mc.listConnections(n+'.overrideDisplayType')
        if cn is None and cnb is None:
            mc.setAttr(n+'.overrideEnabled',l=0)
            mc.setAttr(n+'.overrideDisplayType',l=0)

            if display=='off':
                mc.setAttr(n+'.overrideEnabled', 0)
            else:
                mc.setAttr(n+'.overrideEnabled', 1)

            if display=='off' or display=='normal':
                mc.setAttr(n+'.overrideDisplayType', 0)            
            elif display=='template':
                mc.setAttr(n+'.overrideDisplayType', 1)          
            elif display=='reference':
                mc.setAttr(n+'.overrideDisplayType', 2)

            if shape:
                shapenode=mc.listRelatives(n, s=1, f=1)
                if shapenode is not None:
                    for sh in shapenode:
                        scn=mc.listConnections(sh+'.overrideEnabled')
                        scnb=mc.listConnections(sh+'.overrideDisplayType')

                        if scn is None and scnb is None:
                            mc.setAttr(sh+'.overrideEnabled',l=0)
                            mc.setAttr(sh+'.overrideEnabled', 0)

                            mc.setAttr(sh+'.overrideDisplayType',l=0)
                            mc.setAttr(sh+'.overrideDisplayType', 0) 


def shader(node=None, shdType='lambert', name=None):

    if not node:
        node = mc.ls(sl=1)
    node = mc.ls(node)

    if not name:
        name = node[0].split('.')[0]+'_shd'

    shd = mc.shadingNode(shdType, asShader=1, n=name)
    sg = mc.sets(renderable=1, noSurfaceShader=1, empty=1, n=shd+'SG')
    mc.connectAttr (shd+'.outColor', sg+'.surfaceShader', f=1)
    mc.sets (node, e=1, fe=sg)

    mc.select(shd)
    return shd
