import maya.cmds as mc

def create(types, nodes=None, mo=False, snapOnly=False):

    types = types.split(' ')
    returns = []
    if not nodes:
        nodes = mc.ls(sl=1)

    for conType in types:
        con = ''
        if conType == 'prc':
            con = mc.parentConstraint(nodes, mo=1,n=nodes[len(nodes)-1]+'_prc')[0]
        elif conType == 'pc':
            con = mc.pointConstraint(nodes, mo=mo, n=nodes[len(nodes)-1]+'_pc')[0]
        elif conType == 'oc':
            con = mc.orientConstraint(nodes, mo=mo, n=nodes[len(nodes)-1]+'_oc')[0]
        elif conType == 'sc':
            con = mc.scaleConstraint(nodes, n=nodes[len(nodes)-1]+'_sc', mo=1)[0]
        elif conType == 'ac':
            con = mc.aimConstraint([nodes[0], nodes[2]], mo=mo, worldUpObject=nodes[1], aimVector=[0,1,0], upVector=[1,0,0], worldUpType='object', n=nodes[2]+'_ac')[0]

        if snapOnly:
            mc.delete(con)
        else:
            returns.append(con)

    mc.select(nodes)
    if not snapOnly:
        return returns

def remove(nodes=None, type='All'):
    if nodes is None:
        nodes = mc.ls(sl=1)

    for s in nodes:
        if mc.objExists(s):
            if type == 'All' or 'prc' in type:
                cn = mc.listConnections(s, type='parentConstraint', s=1, d=0)
                if cn: mc.delete(cn)

            if type == 'All' or 'pc' in type:    
                cn = mc.listConnections(s, type='pointConstraint', s=1, d=0)
                if cn: mc.delete(cn)

            if type == 'All' or 'oc' in type:
                cn = mc.listConnections(s, type='orientConstraint', s=1, d=0)
                if cn: mc.delete(cn)

            if type == 'All' or 'sc' in type:
                cn = mc.listConnections(s, type='scaleConstraint', s=1, d=0)
                if cn: mc.delete(cn)

            if type == 'All' or 'ac' in type:
                cn = mc.listConnections(s, type='aimConstraint', s=1, d=0)
                if cn: mc.delete(cn)