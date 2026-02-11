import maya.cmds as mc
import string
import itertools


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def letter(i):
    variations = [''.join(letters)
                  for length in range(1, 4)
                  for letters in itertools.product(string.ascii_uppercase, repeat=length)]
    return variations[i]


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def unique(name, suffix=None):
    i = 0
    newname = name
    while mc.objExists(newname):
        ltr = letter(i)
        if suffix:
            newname = name.replace(suffix, ltr + suffix, 1)
        else:
            newname = name + ltr
        i += 1
    return newname


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def mirrorNames(nodes, so=False):
    returnNodes = []
    if not nodes:
        return

    if isinstance(nodes, str):
        nodes = [nodes]

    side = ''
    mSide = ''
    for n in nodes:
        if 'L_' in n:
            side = 'L_'
            mSide = 'R_'
        elif 'Lf_' in n:
            side = 'Lf_'
            mSide = 'Rt_'
        elif 'Lf' in n:
            side = 'Lf'
            mSide = 'Rt'
        elif 'lf_' in n:
            side = 'lf_'
            mSide = 'rt_'
        elif 'l_' in n:
            side = 'l_'
            mSide = 'r_'
        elif 'Rt_' in n:
            side = 'Rt_'
            mSide = 'Lf_'
        elif 'Rt' in n:
            side = 'Rt'
            mSide = 'Lf'
        elif 'rt_' in n:
            side = 'rt_'
            mSide = 'lf_'
        elif 'r_' in n:
            side = 'r_'
            mSide = 'l_'
        elif 'Cn_' in n:
            side = 'Cn_'
            mSide = ''
        elif 'cn_' in n:
            side = 'cn_'
            mSide = ''
        elif 'C_' in n:
            side = 'C_'
            mSide = ''
        elif 'c_' in n:
            side = 'c_'
            mSide = ''
        elif '_lf_' in n:
            side = '_lf_'
            mSide = '_rt_'
        elif '_l_' in n:
            side = '_l_'
            mSide = '_r_'
        elif '_rt_' in n:
            side = '_rt_'
            mSide = '_lf_'
        elif 'R_' in n:
            side = 'R_'
            mSide = 'L_'
        elif '_r_' in n:
            side = '_r_'
            mSide = '_l_'
        elif '_cn_' in n:
            side = '_cn_'
            mSide = ''
        elif '_c_' in n:
            side = '_c_'
            mSide = ''

        mNode = n.replace(side, mSide, 1)
        if not (n == mNode):
            returnNodes.append(mNode)

    if len(returnNodes) == 1:
        returnNodes = returnNodes[0]

    if so:
        return [side, mSide]
    return returnNodes


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def selectMirrorNodes(add=0):
    nodes = mc.ls(sl=1)
    mnodes = mc.ls(sl=1)

    mtable = {}
    mtable['L_'] = 'R_'
    mtable['l_'] = 'r_'
    mtable['lf_'] = 'rt_'
    mtable['Lf_'] = 'Rt_'
    mtable['Lf'] = 'Rt'
    mtable['LF_'] = 'RT_'
    mtable['R_'] = 'L_'
    mtable['r_'] = 'l_'
    mtable['rt_'] = 'lf_'
    mtable['Rt_'] = 'Lf_'
    mtable['Rt'] = 'Lf'
    mtable['RT_'] = 'LF_'

    for i in range(len(nodes)):
        for s, ms in mtable.items():
            if nodes[i].startswith(s):
                mnodes[i] = nodes[i].replace(s, ms, 1)

    mnodes = mc.ls(mnodes)
    if mnodes:
        mc.select(mnodes, add=add)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def searchReplace(search, replace, hi=True):
    if search == replace:
        return

    renamed = []
    nodes = mc.ls(sl=1, l=1)
    if hi:
        nodes = mc.ls(sl=1, dag=1, l=1)
    nodes.reverse()

    for n in nodes:
        shortname = n.split('|')[-1]
        if not mc.reference(n, q=1, isNodeReferenced=1):
            newname = shortname.replace(search, replace, 1)
            if mc.objExists(n):
                renamed.append(mc.rename(n, newname))
    return renamed


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def prefix(prefix, hi=True):
    renamed = []
    nodes = mc.ls(sl=1, l=1)
    if hi:
        nodes = mc.ls(sl=1, dag=1, l=1)
    nodes.reverse()

    for n in nodes:
        shortname = n.split('|')[-1]
        if not mc.reference(n, q=1, isNodeReferenced=1):
            newname = prefix + shortname
            if mc.objExists(n):
                renamed.append(mc.rename(n, newname))
    return renamed


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def suffix(suffix, hi=True):
    renamed = []
    nodes = mc.ls(sl=1, l=1)
    if hi:
        nodes = mc.ls(sl=1, dag=1, l=1)
    nodes.reverse()

    for n in nodes:
        shortname = n.split('|')[-1]
        if not mc.reference(n, q=1, isNodeReferenced=1):
            newname = shortname + suffix
            if mc.objExists(n):
                renamed.append(mc.rename(n, newname))
    return renamed

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def getSelectedAttrs():
    attrs = []
    currentAttrSelected = mc.channelBox("mainChannelBox", q=True, sma=True)
    if currentAttrSelected is None:
        return
    for x in currentAttrSelected:
        longName = mc.attributeName('.' + x, l=True)
        attrs.append(longName)
    return attrs