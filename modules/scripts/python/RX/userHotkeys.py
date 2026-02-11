# My custom user Hotkeys
import maya.cmds as mc
import maya.mel as mel


# Hotkeys [Ctrl + Shift + x] 'XRayJoints'
def xrayJnt():
    currentPanel = mc.getPanel(withFocus=1)
    xray = mc.modelEditor(currentPanel, q=1, jointXray=1)
    if xray:
        mc.modelEditor(currentPanel, e=1, jointXray=0)
    else:
        mc.modelEditor(currentPanel, e=1, jointXray=1)

# Hotkeys [Ctrl + Shift + w] 'wireFrameShader'
def wireFrameShader():
    currentPanel = mc.getPanel(withFocus=1)
    wireOnOff = mc.modelEditor(currentPanel, q=1, wos=1)
    if wireOnOff:
        mc.modelEditor(currentPanel, e=1, wos=0)
    else:
        mc.modelEditor(currentPanel, e=1, wos=1)

# Hotkeys [Alt + q] 'showSelect'
def showSelect():
    currentPanel = mc.getPanel(withFocus=1)
    showOnOff = mc.modelEditor(currentPanel, q=1, vs=1)
    if showOnOff:
        mc.isolateSelect(currentPanel, state=0)
    else:
        mc.isolateSelect(currentPanel, state=1)
        mc.isolateSelect(currentPanel, removeSelected=1)
        mc.isolateSelect(currentPanel, addSelected=1)

# Hotkeys [Alt + Shift + r] 'wireFrameShader'
def resetSelCtrls():
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:
        attrs = mc.listAttr(ctrl, k=1, w=1, unlocked=1, s=1)
        if attrs is not None:
            for attr in attrs:
                attrName = "%s.%s" % (ctrl, attr)
                settable = mc.getAttr(attrName, settable=1)
                if settable:
                    v = mc.attributeQuery(attr, listDefault=1, n=ctrl)
                    val = mc.getAttr(attrName)
                    if round(v[0], 2) != round(val, 2):
                        mc.setAttr((ctrl + "." + attr), v[0])

# Hotkeys  [???]  resetSelTranslate
def resetSelTranslate():
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:
        txlock = mc.getAttr(ctrl + '.tx', settable=1)
        tylock = mc.getAttr(ctrl + '.ty', settable=1)
        tzlock = mc.getAttr(ctrl + '.tz', settable=1)
        if txlock: mc.setAttr(ctrl + '.tx', 0)
        if tylock: mc.setAttr(ctrl + '.ty', 0)
        if tzlock: mc.setAttr(ctrl + '.tz', 0)

# Hotkeys  [Alt + Shift + e]  resetSelRotate
def resetSelRotate():
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:
        lock = mc.getAttr(ctrl + '.', settable=1)
        rylock = mc.getAttr(ctrl + '.ry', settable=1)
        rzlock = mc.getAttr(ctrl + '.rz', settable=1)
        if lock: mc.setAttr(ctrl + '.', 0)
        if rylock: mc.setAttr(ctrl + '.ry', 0)
        if rzlock: mc.setAttr(ctrl + '.rz', 0)

# Hotkeys  [???]  resetSelScale
def resetSelScale():
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:
        sxlock = mc.getAttr(ctrl + '.sx', settable=1)
        sylock = mc.getAttr(ctrl + '.sy', settable=1)
        szlock = mc.getAttr(ctrl + '.sz', settable=1)
        if sxlock: mc.setAttr(ctrl + '.sx', 1)
        if sylock: mc.setAttr(ctrl + '.sy', 1)
        if szlock: mc.setAttr(ctrl + '.sz', 1)


# Hotkeys  'j' 'm' 'n' 'k'
# args : 'joints' 'polymeshes' 'nurbsSurfaces' 'nurbsCurves'
def toggleMeshVis():
    panels = mc.getPanel(type='modelPanel')

    i = 1
    if mel.eval('modelEditor -q -'+'polymeshes'+' '+panels[0]):
        i = 0
    for p in panels:
        mel.eval('modelEditor -e -'+'polymeshes'+' '+str(i)+' '+p)

def toggleJntVis():
    panels = mc.getPanel(type='modelPanel')

    i = 1
    if mel.eval('modelEditor -q -'+'joints'+' '+panels[0]):
        i = 0
    for p in panels:
        mel.eval('modelEditor -e -'+'joints'+' '+str(i)+' '+p)

def toggleCurveVis():
    panels = mc.getPanel(type='modelPanel')

    i = 1
    if mel.eval('modelEditor -q -'+'nurbsCurves'+' '+panels[0]):
        i = 0
    for p in panels:
        mel.eval('modelEditor -e -'+'nurbsCurves'+' '+str(i)+' '+p)

# ADD USER HOTKEY
def load():
    # create hotkey and set current
    hotkeySet = 'RX_Hotkeys'
    if not mc.hotkeySet(hotkeySet, exists=1):
        mc.hotkeySet(hotkeySet, current=1)
    else:
        mc.hotkeySet(hotkeySet, e=1, current=1)

    # COMMAND--------------------------------------------------------------------------

    # mesh vis [ m ]polymeshes
    # commandName = 'toggleMeshVis'
    # mc.nameCommand(commandName, ann='[ m ] toggleMeshVis', stp='python', c='python("from  import userHotkeys; userHotkeys.toggleMeshVis()")')
    # mc.hotkey(keyShortcut='m', name=commandName)
    #
    # commandName = 'toggleJntVis'
    # mc.nameCommand(commandName, ann='[ j ] toggleJntVis', stp='python', c='python("from  import userHotkeys; userHotkeys.toggleJntVis()")')
    # mc.hotkey(keyShortcut='j', name=commandName)
    #
    # commandName = 'toggleCurveVis'
    # mc.nameCommand(commandName, ann='[ k ] toggleCurveVis', stp='python', c='python("from  import userHotkeys; userHotkeys.toggleCurveVis()")')
    # mc.hotkey(keyShortcut='k', name=commandName)

    commandName = 'xrayJnt'
    mc.nameCommand(commandName, ann='[ ctrl + shift + x ] xrayJnt', stp='python', c='python("from RX import userHotkeys; userHotkeys.xrayJnt()")')
    mc.hotkey(keyShortcut='x', ctl=1, sht=1, name=commandName)

    commandName = 'resetSelCtrls'
    mc.nameCommand(commandName, ann='[  alt + shift + r ] resetSelCtrls', stp='python', c='python("from RX import userHotkeys; userHotkeys.resetSelCtrls()")')
    mc.hotkey(keyShortcut='r', alt=1, sht=1, name=commandName)

    commandName = 'resetSelRotate'
    mc.nameCommand(commandName, ann='[ alt + shift + e ] resetSelRotate', stp='python', c='python("from RX import userHotkeys; userHotkeys.resetSelRotate()")')
    mc.hotkey(keyShortcut='e', alt=1, sht=1, name=commandName)

    commandName = 'wireFrameShader'
    mc.nameCommand(commandName, ann='[ ctrl + shift + w ] wireFrameShader', stp='python', c='python("from RX import userHotkeys; userHotkeys.wireFrameShader()")')
    mc.hotkey(keyShortcut='w', ctl=1, sht=1, name=commandName)

    commandName = 'showSelect'
    mc.nameCommand(commandName, ann='[ alt + q ] showSelect', stp='python', c='python("from RX import userHotkeys; userHotkeys.showSelect()")')
    mc.hotkey(keyShortcut='q', alt=1, name=commandName)

    print ('Loaded  Hotkeys...')
