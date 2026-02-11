import maya.cmds as mc
import maya.mel as mel


def limb():
    nodes = mc.ls(sl=1)
    if not nodes:
        return
        # get snap info from ctrl
    info = getSnapInfo(nodes[0])
    if info:
        # run snap use exec
        exec ('{0}("{1}")'.format(info[-1], nodes[0]))


def hand(node):
    prefix = getSnapInfo(node)[0]
    ikctrl = prefix + 'Ik_ctrl'
    fkctrls = mc.ls([prefix + '?_ctrl'])
    jnts = mc.ls([prefix + '?', prefix + 'End'], type='joint')

    if mc.getAttr(ikctrl + '.IK'):
        for i in range(len(fkctrls)):
            mc.xform(fkctrls[i], ws=1, ro=mc.xform(jnts[i], q=1, ws=1, ro=1))
        mc.setAttr(ikctrl + '.IK', 0)

    else:
        mc.xform(ikctrl, ws=1, t=mc.xform(jnts[-1], q=1, ws=1, t=1))
        mc.xform(ikctrl, ws=1, ro=mc.xform(jnts[-1], q=1, ws=1, ro=1))
        mc.setAttr(ikctrl + '.IK', 1)


def bipedArm(node):
    prefix = getSnapInfo(node)[0]

    ikctrls = [prefix + 'armIk_ctrl', prefix + 'elbowIk_ctrl']
    fkctrls = [prefix + 'upArmFk_ctrl', prefix + 'loArmFk_ctrl', prefix + 'wristFk_ctrl']

    iksnaps = [ikctrls[0] + '_snap', ikctrls[1] + '_snap', ]
    fksnaps = [prefix + 'upArm_drv', prefix + 'loArm_drv', prefix + 'wrist_drv',]

    ikJnts = [prefix + 'upArm_ik', prefix + 'loArm_ik', prefix + 'wrist_ik']
    fkJnts = [prefix + 'upArm_fk', prefix + 'loArm_fk', prefix + 'wrist_fk']

    stretchCmd = prefix + 'arm_softIk_value_bridge'
    setCtrl = prefix + 'armSet_ctrl'


    # SNAPING...
    if mc.getAttr(setCtrl + '.IKFK'):
        # snap ik to fk
        # pos
        for i in range(len(fkctrls)):
            mc.xform(fkctrls[i], ws=1, ro=mc.xform(fksnaps[i], q=1, ws=1, ro=1))

        # length
        upperLength = abs(mc.getAttr(ikJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
        lowerLength = abs(mc.getAttr(ikJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

        mc.setAttr(fkctrls[0] + '.length', upperLength)
        mc.setAttr(fkctrls[1] + '.length', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 0)
        mc.select(fkctrls[0])

    else:
        # snap fk to ik
        # clean ik ctrl value
        mc.setAttr(ikctrls[0] + '.twist', 0)
        mc.setAttr(ikctrls[0] + '.upLength', 1)
        mc.setAttr(ikctrls[0] + '.loLength', 1)
        mc.setAttr(ikctrls[1] + '.sticky', 0)

        # snap pos
        mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
        mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
        mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))

        # length
        upperLength = abs(mc.getAttr(fkJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
        lowerLength = abs(mc.getAttr(fkJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

        mc.setAttr(ikctrls[0] + '.upLength', upperLength)
        mc.setAttr(ikctrls[0] + '.loLength', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 1)
        mc.select(ikctrls[0])




def bipedLeg(node):
    # init data
    prefix = getSnapInfo(node)[0]

    ikctrls = [prefix + 'legIk_ctrl', prefix + 'kneeIk_ctrl']
    fkctrls = [prefix + 'upLegFk_ctrl', prefix + 'loLegFk_ctrl']

    fksnaps = [prefix + 'upLeg_drv', prefix + 'loLeg_drv']
    iksnaps = [ikctrls[0] + '_snap', ikctrls[1] + '_snap', ]

    fkJnts = [prefix + 'upLeg_fk', prefix + 'loLeg_fk', prefix + 'legEnd_fk']
    ikJnts = [prefix + 'upLeg_ik', prefix + 'loLeg_ik', prefix + 'legEnd_ik']

    stretchCmd = prefix + 'leg_softIk_value_bridge'
    setCtrl = prefix + 'legSet_ctrl'

    foot = False
    if mc.objExists(ikctrls[0] + '.footPivot'):
        fkctrls.extend( mc.ls(prefix + 'toeLegFk_ctrl', prefix + 'ballFk_ctrl') )
        fksnaps.extend( mc.ls(prefix + 'toeLegFk_ctrl_snap', prefix + 'ball_drv') )
        ikctrls.extend( mc.ls(prefix + 'ballIk_ctrl') )
        iksnaps.extend( mc.ls(prefix + 'ball_drv') )
        foot = True

    # SNAPING...
    if mc.getAttr(setCtrl + '.IKFK'):
        # snap ik to fk
        # pos
        for i in range(len(fkctrls)):
            mc.xform(fkctrls[i], ws=1, ro=mc.xform(fksnaps[i], q=1, ws=1, ro=1))

        # length
        upperLength = abs(mc.getAttr(ikJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
        lowerLength = abs(mc.getAttr(ikJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

        mc.setAttr(fkctrls[0] + '.length', upperLength)
        mc.setAttr(fkctrls[1] + '.length', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 0)
        mc.select(fkctrls[0])

    else:
        # snap fk to ik
        if foot:
            pivots = {}
            pivots['0'] = 'ankle'
            pivots['1'] = 'heel'
            pivots['2'] = 'ball'
            pivots['3'] = 'toe'
            pivots['4'] = 'inner'
            pivots['5'] = 'outter'
            pivots['6'] = 'movable'
            pivot = pivots[str(mc.getAttr(ikctrls[0] + '.footPivot'))]
            mc.setAttr(ikctrls[0] + '.footPivot', 0)

            # clean ik ctrl value
            mc.setAttr(ikctrls[0] + '.twist', 0)
            mc.setAttr(ikctrls[0] + '.upLength', 1)
            mc.setAttr(ikctrls[0] + '.loLength', 1)
            mc.setAttr(ikctrls[1] + '.sticky', 0)


            attrs = ['roll', 'sideRoll', 'toeLift', 'toe',
                     'ball', 'heel', 'toeTwist', 'ballTwist', 'heelTwist']
            for a in attrs:
                mc.setAttr(ikctrls[0] + '.' + a, 0)

            # snap pos
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))

            # length
            upperLength = abs(mc.getAttr(fkJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
            lowerLength = abs(mc.getAttr(fkJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

            mc.setAttr(ikctrls[0] + '.upLength', upperLength)
            mc.setAttr(ikctrls[0] + '.loLength', lowerLength)

            mc.setAttr(setCtrl + '.IKFK', 1)
            mc.select(ikctrls[0])

            footPivot(pivot)
        else:
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))
            mc.setAttr(setCtrl + '.IKFK', 1)
            mc.select(ikctrls[0])


def quadLeg(node):
    # init data
    prefix = getSnapInfo(node)[0]

    ikctrls = [prefix + 'legIk_ctrl', prefix + 'kneeIk_ctrl']
    iksnaps = [ikctrls[0] + '_snap', ikctrls[1] + '_snap', ]

    fkctrls = [prefix + 'upLegFk_ctrl', prefix + 'midLegFk_ctrl', prefix + 'loLegFk_ctrl']
    fksnaps = [prefix + 'upLeg_drv', prefix + 'midLeg_drv', prefix + 'loLeg_drv']

    fkJnts = [prefix + 'upLeg_fk', prefix + 'midLeg_fk', prefix + 'loLeg_fk', prefix + 'legEnd_fk']
    ikJnts = [prefix + 'upLeg_ik', prefix + 'midLeg_ik', prefix + 'loLeg_ik', prefix + 'legEnd_ik']

    stretchCmd = prefix + 'qleg_softIk_value_bridge'
    setCtrl = prefix + 'legSet_ctrl'

    foot = False
    if mc.objExists(ikctrls[0] + '.footPivot'):
        fkctrls.extend( mc.ls(prefix + 'toeLegFk_ctrl', prefix + 'ballFk_ctrl') )
        fksnaps.extend( mc.ls(prefix + 'toeLegFk_ctrl_snap', prefix + 'ball_drv') )
        ikctrls.extend( mc.ls(prefix + 'ballIk_ctrl') )
        iksnaps.extend( mc.ls(prefix + 'ball_drv') )
        foot = True

    stretch = False
    if mc.objExists(stretchCmd):
        stretch = True

    # snap ik to fk
    if mc.getAttr(setCtrl + '.IKFK'):

        # pos
        for i in range(len(fkctrls)):
            mc.xform(fkctrls[i], ws=1, ro=mc.xform(fksnaps[i], q=1, ws=1, ro=1))

        if stretch:
            # length
            upperLength = abs(mc.getAttr(ikJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
            midLength = abs(mc.getAttr(ikJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')
            lowerLength = abs(mc.getAttr(ikJnts[3] + '.tx')) / mc.getAttr(stretchCmd + '.orgC')

            mc.setAttr(fkctrls[0] + '.length', upperLength)
            mc.setAttr(fkctrls[1] + '.length', midLength)
            mc.setAttr(fkctrls[2] + '.length', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 0)
        mc.select(fkctrls[0])

    # snap fk to ik
    else:
        # snap fk to ik
        if foot:
            pivots = {}
            pivots['0'] = 'ankle'
            pivots['1'] = 'heel'
            pivots['2'] = 'ball'
            pivots['3'] = 'toe'
            pivots['4'] = 'inner'
            pivots['5'] = 'outter'
            pivots['6'] = 'movable'
            pivot = pivots[str(mc.getAttr(ikctrls[0] + '.footPivot'))]
            mc.setAttr(ikctrls[0] + '.footPivot', 0)

            # clean ik ctrl value
            mc.setAttr(ikctrls[0] + '.upLength', 1)
            mc.setAttr(ikctrls[0] + '.midLength', 1)
            mc.setAttr(ikctrls[0] + '.loLength', 1)

            attrs = ['roll', 'sideRoll', 'toeLift', 'toe',
                     'ball', 'heel', 'toeTwist', 'ballTwist', 'heelTwist']
            for a in attrs:
                mc.setAttr(ikctrls[0] + '.' + a, 0)

            # snap pos
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))
            footPivot(pivot)

        else:
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))

        if stretch:
            # length
            upperLength = abs(mc.getAttr(fkJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
            midLength = abs(mc.getAttr(fkJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')
            lowerLength = abs(mc.getAttr(fkJnts[3] + '.tx')) / mc.getAttr(stretchCmd + '.orgC')

            mc.setAttr(ikctrls[0] + '.upLength', upperLength)
            mc.setAttr(ikctrls[0] + '.midLength', midLength)
            mc.setAttr(ikctrls[0] + '.loLength', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 1)
        mc.select(ikctrls[0])

        # offset angel
        mc.setAttr(ikctrls[0] + '.angleSet', 0)
        mc.setAttr(ikctrls[0] + '.angleOffset', 0)

        angleOffset = getAngle(fkJnts[0], fkJnts[1], ikJnts[1])
        if angleOffset != 0:
            mc.setAttr(ikctrls[0] + '.angleOffset', angleOffset)
        # Check again: because I can't resolution the value positive or negetive.
        checkAngle = getAngle(fkJnts[0], fkJnts[1], ikJnts[1])
        if checkAngle != 0:
            mc.setAttr(ikctrls[0] + '.angleOffset', angleOffset*-1)


def quadArm(node):
    # init data
    prefix = getSnapInfo(node)[0]

    ikctrls = [prefix + 'armIk_ctrl', prefix + 'elbowIk_ctrl']
    fkctrls = [prefix + 'upArmFk_ctrl', prefix + 'loArmFk_ctrl']

    fksnaps = [prefix + 'upArm_drv', prefix + 'loArm_drv']
    iksnaps = [ikctrls[0] + '_snap', ikctrls[1] + '_snap', ]

    fkJnts = [prefix + 'upArm_fk', prefix + 'loArm_fk', prefix + 'armEnd_fk']
    ikJnts = [prefix + 'upArm_ik', prefix + 'loArm_ik', prefix + 'armEnd_ik']

    stretchCmd = prefix + 'arm_softIk_value_bridge'
    setCtrl = prefix + 'armSet_ctrl'

    foot = False
    if mc.objExists(ikctrls[0] + '.footPivot'):
        fkctrls.extend( mc.ls(prefix + 'toeArmFk_ctrl', prefix + 'ballFk_ctrl') )
        fksnaps.extend( mc.ls(prefix + 'toeArmFk_ctrl_snap', prefix + 'ball_drv') )
        ikctrls.extend( mc.ls(prefix + 'ballIk_ctrl') )
        iksnaps.extend( mc.ls(prefix + 'ball_drv') )
        foot = True

    # SNAPING...
    if mc.getAttr(setCtrl + '.IKFK'):
        # snap ik to fk
        # pos
        for i in range(len(fkctrls)):
            mc.xform(fkctrls[i], ws=1, ro=mc.xform(fksnaps[i], q=1, ws=1, ro=1))

        # length
        upperLength = abs(mc.getAttr(ikJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
        lowerLength = abs(mc.getAttr(ikJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

        mc.setAttr(fkctrls[0] + '.length', upperLength)
        mc.setAttr(fkctrls[1] + '.length', lowerLength)

        mc.setAttr(setCtrl + '.IKFK', 0)
        mc.select(fkctrls[0])

    else:
        # snap fk to ik
        if foot:
            pivots = {}
            pivots['0'] = 'ankle'
            pivots['1'] = 'heel'
            pivots['2'] = 'ball'
            pivots['3'] = 'toe'
            pivots['4'] = 'inner'
            pivots['5'] = 'outter'
            pivots['6'] = 'movable'
            pivot = pivots[str(mc.getAttr(ikctrls[0] + '.footPivot'))]
            mc.setAttr(ikctrls[0] + '.footPivot', 0)

            # clean ik ctrl value
            mc.setAttr(ikctrls[1] + '.sticky', 0)
            mc.setAttr(ikctrls[0] + '.upLength', 1)
            mc.setAttr(ikctrls[0] + '.loLength', 1)

            attrs = ['roll', 'sideRoll', 'toeLift', 'toe',
                     'ball', 'heel', 'toeTwist', 'ballTwist', 'heelTwist']
            for a in attrs:
                mc.setAttr(ikctrls[0] + '.' + a, 0)

            # snap pos
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))

            # length
            upperLength = abs(mc.getAttr(fkJnts[1] + '.tx')) / mc.getAttr(stretchCmd + '.orgA')
            lowerLength = abs(mc.getAttr(fkJnts[2] + '.tx')) / mc.getAttr(stretchCmd + '.orgB')

            mc.setAttr(ikctrls[0] + '.upLength', upperLength)
            mc.setAttr(ikctrls[0] + '.loLength', lowerLength)

            mc.setAttr(setCtrl + '.IKFK', 1)
            mc.select(ikctrls[0])

            footPivot(pivot)
        else:
            mc.xform(ikctrls[0], ws=1, t=mc.xform(iksnaps[0], q=1, ws=1, t=1))
            mc.xform(ikctrls[0], ws=1, ro=mc.xform(iksnaps[0], q=1, ws=1, ro=1))
            mc.xform(ikctrls[1], ws=1, t=mc.xform(iksnaps[1], q=1, ws=1, t=1))
            mc.xform(ikctrls[2], ws=1, ro=mc.xform(iksnaps[2], q=1, ws=1, ro=1))
            mc.setAttr(setCtrl + '.IKFK', 1)
            mc.select(ikctrls[0])


#----------------------------------------------------------------------------------------------
# snap space
def space(part):
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:
        spaces = mc.addAttr(ctrl + '.space', q=1, en=1).split(':')
        if not part in spaces:
            continue

        t = mc.duplicate(ctrl, n='tmp#', po=1)[0]
        tp = mc.duplicate(ctrl, n='tmp#', po=1)[0]

        unlock([t, tp])
        mc.parent(t, tp)
        mc.parent(tp, w=1)

        ii = 0
        for i in range(len(spaces)):
            if part == spaces[i]:
                ii = i

        mc.setAttr(ctrl + '.space', ii)
        tt = mc.duplicate(ctrl, n='tmp#', po=1)[0]

        unlock(tt)
        mc.pointConstraint(t, tt)
        mc.orientConstraint(t, tt)

        mc.xform(ctrl, a=1, ro=mc.xform(tt, q=1, a=1, ro=1))
        mc.xform(ctrl, ws=1, t=mc.xform(t, q=1, ws=1, t=1))
        mc.delete(tp, tt)

    mc.select(ctrls)


######################################################
# snap foot pivot
def footPivot(pivot):
    ctrls = mc.ls(sl=1)
    for ctrl in ctrls:

        if not mc.objExists(ctrl + '.footPivot'):
            continue

        # get prefix
        grp = ctrl + '_grp'
        childs = mc.listRelatives(grp, c=1)
        pivPar = ''
        if childs:
            for c in childs:
                if c.endswith('_footPivots'):
                    pivPar = c
        if not pivPar:
            continue

        prefix = pivPar.replace('footPivots', '')
        pivots = {}
        pivots['ankle'] = prefix + 'ankle_drv'
        pivots['heel'] = prefix + 'heel_drv'
        pivots['ball'] = prefix + 'ball_drv'
        pivots['toe'] = prefix + 'ballEnd_drv'
        pivots['inner'] = prefix + 'inFootRev'
        pivots['outter'] = prefix + 'outFootRev'
        pivots['movable'] = prefix + 'ankle_drv'

        if pivot in pivots.keys():
            posnode = pivots[pivot]
            pivots = mc.addAttr(ctrl + '.footPivot', q=1, en=1).split(':')
            pi = 0
            for i in range(len(pivots)):
                if pivot == pivots[i]:
                    pi = i
        else:
            continue

        if not mc.objExists(posnode):
            continue

        # get autokey state and turn it off
        autostate = mc.autoKeyframe(q=1, state=1)
        if autostate:
            mc.autoKeyframe(state=0)

        # get vals
        tval = mc.getAttr(ctrl + '.toe')
        bval = mc.getAttr(ctrl + '.ball')
        hval = mc.getAttr(ctrl + '.heel')
        rollval = mc.getAttr(ctrl + '.roll')
        srollval = mc.getAttr(ctrl + '.sideRoll')
        tliftval = mc.getAttr(ctrl + '.toeLift')
        ttwistval = mc.getAttr(ctrl + '.toeTwist')
        btwistval = mc.getAttr(ctrl + '.ballTwist')
        htwistval = mc.getAttr(ctrl + '.heelTwist')

        # zero vals
        mc.setAttr(ctrl + '.toe', 0)
        mc.setAttr(ctrl + '.ball', 0)
        mc.setAttr(ctrl + '.heel', 0)
        mc.setAttr(ctrl + '.toeTwist', 0)
        mc.setAttr(ctrl + '.ballTwist', 0)
        mc.setAttr(ctrl + '.heelTwist', 0)
        mc.setAttr(ctrl + '.toeLift', 0)
        mc.setAttr(ctrl + '.roll', 0)
        mc.setAttr(ctrl + '.sideRoll', 0)

        # repo ctrl
        pos = mc.xform(posnode, q=1, ws=1, t=1)
        mc.setAttr(ctrl + '.footPivot', pi)
        mc.xform(ctrl, ws=1, t=pos)

        # reset vals
        mc.setAttr(ctrl + '.toe', tval)
        mc.setAttr(ctrl + '.ball', bval)
        mc.setAttr(ctrl + '.heel', hval)
        mc.setAttr(ctrl + '.roll', rollval)
        mc.setAttr(ctrl + '.sideRoll', srollval)
        mc.setAttr(ctrl + '.toeLift', tliftval)
        mc.setAttr(ctrl + '.toeTwist', ttwistval)
        mc.setAttr(ctrl + '.ballTwist', btwistval)
        mc.setAttr(ctrl + '.heelTwist', htwistval)

        if autostate:
            mc.autoKeyframe(state=1)


# helper functions
def getDistance(vtx1, vtx2):
    v1 = mc.xform(vtx1, q=1, ws=1, t=1)
    v2 = mc.xform(vtx2, q=1, ws=1, t=1)
    mel.eval('vector $vector1 = <<' + str(v1[0]) + ', ' + str(v1[1]) + ', ' + str(v1[2]) + '>>;')
    mel.eval('vector $vector2 = <<' + str(v2[0]) + ', ' + str(v2[1]) + ', ' + str(v2[2]) + '>>;')
    return mel.eval('mag($vector1 - $vector2)')


def unlock(node):
    node = mc.ls(node)
    attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    for a in attrs:
        mc.setAttr(node[0] + '.' + a, l=0, k=1)


def getSnapInfo(node):
    snapArgs = []
    if mc.objExists(node + '.tagIkFkSnap'):
        sna = mc.getAttr(node + '.tagIkFkSnap').split(' ')
        for n in sna:
            snapArgs.append(n.split(':')[-1])

    # get namespace
    nss = node.split(':')
    if len(nss) == 2 and snapArgs:
        snapArgs[0] = nss[0] + ':' + snapArgs[0]

    return snapArgs


def getAngle(base, objA, objB):
    # dmx node
    baseMt = mc.createNode('decomposeMatrix')
    objAMt = mc.createNode('decomposeMatrix')
    objBMt = mc.createNode('decomposeMatrix')
    mc.connectAttr(base + '.worldMatrix', baseMt + '.inputMatrix')
    mc.connectAttr(objA + '.worldMatrix', objAMt + '.inputMatrix')
    mc.connectAttr(objB + '.worldMatrix', objBMt + '.inputMatrix')

    # plus node
    objAPlus = mc.createNode('plusMinusAverage')
    objBPlus = mc.createNode('plusMinusAverage')
    mc.setAttr(objAPlus + '.operation', 2)
    mc.setAttr(objBPlus + '.operation', 2)
    mc.connectAttr(objAMt + '.outputTranslate', objAPlus + '.input3D[0]')
    mc.connectAttr(objBMt + '.outputTranslate', objBPlus + '.input3D[0]')
    mc.connectAttr(baseMt + '.outputTranslate', objAPlus + '.input3D[1]')
    mc.connectAttr(baseMt + '.outputTranslate', objBPlus + '.input3D[1]')

    # angel node
    outputAngle = mc.createNode('angleBetween')
    mc.connectAttr(objAPlus + '.output3D', outputAngle + '.vector1')
    mc.connectAttr(objBPlus + '.output3D', outputAngle + '.vector2')

    angle = mc.getAttr(outputAngle + '.angle')
    mc.delete(baseMt, objAMt, objBMt, objAPlus, objBPlus, outputAngle)
    return angle




