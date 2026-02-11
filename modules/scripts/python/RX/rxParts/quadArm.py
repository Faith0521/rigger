######################################
#   Rig Build Part
######################################
from importlib import reload

import maya.cmds as mc

import templateTools
import controlTools
import tagTools
import assetCommon
import nonRoll
import bendy2Limb
import stretch1Tools
import stretch2Tools
import spaceTools
import poleVectorTools
import poseDriverTool

from rxCore import aboutLock
from rxCore import aboutPublic
from rxCore import aboutCrv
from rxParts import footPart


# Build Tempalte
def template(side='lf', prefix='fr', parent='chest', doubleElbow=True, twist=True, bendy=True, stretch=True, volume=False, autoShoulder=True, addFoot=True, poseDriver=True, helpJoint=True):
    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['doubleElbow'] = doubleElbow
    args['twist'] = twist
    args['bendy'] = bendy
    args['stretch'] = stretch
    args['volume'] = volume
    args['autoShoulder'] = autoShoulder
    args['addFoot'] = addFoot
    args['poseDriver'] = poseDriver
    args['helpJoint'] = helpJoint
    footprefix = prefix

    # Args to lock once part is built
    lockArgs = ['doubleElbow', 'addFoot', 'twist', 'stretch', 'bendy']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode(__name__, args, lockArgs)
    if not info:
        print ('Exiting... ')
        return

    topnode = info[0]
    prefix = info[1]

    # Template Build Code...

    # set mirror and color
    color = 'blue'
    doubleColor = 'cobalt'
    mirror = 1
    if side == 'rt':
        mirror = -1
        color = 'red'
        doubleColor = 'violet'

    # create joints
    scapula = templateTools.createJoint(prefix + 'scapula', topnode, color)
    shoulder = templateTools.createJoint(prefix + 'shoulder', topnode, color)
    shoulderEnd = templateTools.createJoint(prefix + 'shoulderEnd', topnode, color)
    upArm = templateTools.createJoint(prefix + 'upArm', topnode, color)
    loArm = templateTools.createJoint(prefix + 'loArm', topnode, color)
    armEnd = templateTools.createJoint(prefix + 'armEnd', topnode, color)
    armToe = templateTools.createJoint(prefix + 'armToe', topnode, color)
    loArmA = []
    loArmB = []
    loArmC = []
    upArmHelper = []
    upArmHelperA = []
    upArmHelperAEnd = []
    upArmHelperB = []
    upArmHelperBEnd = []
    upArmHelperC = []
    upArmHelperCEnd = []
    upArmHelperD = []
    upArmHelperDEnd = []
    loArmHelper = []
    loArmHelperA = []
    loArmHelperAEnd = []
    loArmHelperB = []
    loArmHelperBEnd = []
    armEndHelper = []
    armEndHelperA = []
    armEndHelperAEnd = []
    armEndHelperB = []
    armEndHelperBEnd = []
    armEndHelperC = []
    armEndHelperCEnd = []
    armEndHelperD = []
    armEndHelperDEnd = []


    if doubleElbow:
        loArmA = templateTools.createJoint(prefix + 'loArmA', topnode, doubleColor, pc=1, oc=0)
        loArmB = templateTools.createJoint(prefix + 'loArmB', topnode, doubleColor, pc=1, oc=0)
        loArmC = templateTools.createJoint(prefix + 'loArmC', topnode, doubleColor, pc=1, oc=0)
        mc.hide(loArmC[0])

    if helpJoint:
        # upArm help joints
        upArmHelper = templateTools.createJoint(prefix + 'upArmHelper', topnode, doubleColor, pc=1, oc=0)
        upArmHelperA = templateTools.createJoint(prefix + 'upArmHelperA', topnode, doubleColor, pc=1, oc=0)
        upArmHelperAEnd = templateTools.createJoint(prefix + 'upArmHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        upArmHelperB = templateTools.createJoint(prefix + 'upArmHelperB', topnode, doubleColor, pc=1, oc=0)
        upArmHelperBEnd = templateTools.createJoint(prefix + 'upArmHelperBEnd', topnode, color, pc=1, oc=0)
        upArmHelperC = templateTools.createJoint(prefix + 'upArmHelperC', topnode, doubleColor, pc=1, oc=0)
        upArmHelperCEnd = templateTools.createJoint(prefix + 'upArmHelperCEnd', topnode, doubleColor, pc=1, oc=0)
        upArmHelperD = templateTools.createJoint(prefix + 'upArmHelperD', topnode, doubleColor, pc=1, oc=0)
        upArmHelperDEnd = templateTools.createJoint(prefix + 'upArmHelperDEnd', topnode, doubleColor, pc=1, oc=0)

        # loArm help joints
        loArmHelper = templateTools.createJoint(prefix + 'loArmHelper', topnode, doubleColor, pc=1, oc=0)
        loArmHelperA = templateTools.createJoint(prefix + 'loArmHelperA', topnode, doubleColor, pc=1, oc=0)
        loArmHelperAEnd = templateTools.createJoint(prefix + 'loArmHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        loArmHelperB = templateTools.createJoint(prefix + 'loArmHelperB', topnode, doubleColor, pc=1, oc=0)
        loArmHelperBEnd = templateTools.createJoint(prefix + 'loArmHelperBEnd', topnode, doubleColor, pc=1, oc=0)

        # armEnd help joints
        armEndHelper = templateTools.createJoint(prefix + 'armEndHelper', topnode, doubleColor, pc=1, oc=0)
        armEndHelperA = templateTools.createJoint(prefix + 'armEndHelperA', topnode, doubleColor, pc=1, oc=0)
        armEndHelperAEnd = templateTools.createJoint(prefix + 'armEndHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        armEndHelperB = templateTools.createJoint(prefix + 'armEndHelperB', topnode, doubleColor, pc=1, oc=0)
        armEndHelperBEnd = templateTools.createJoint(prefix + 'armEndHelperBEnd', topnode, doubleColor, pc=1, oc=0)
        armEndHelperC = templateTools.createJoint(prefix + 'armEndHelperC', topnode, doubleColor, pc=1, oc=0)
        armEndHelperCEnd = templateTools.createJoint(prefix + 'armEndHelperCEnd', topnode, doubleColor, pc=1, oc=0)
        armEndHelperD = templateTools.createJoint(prefix + 'armEndHelperD', topnode, doubleColor, pc=1, oc=0)
        armEndHelperDEnd = templateTools.createJoint(prefix + 'armEndHelperEnd', topnode, doubleColor, pc=1, oc=0)

    # set template pose
    mc.xform(scapula[0], ws=1, t=[mirror * 3.2, 0, 0])
    mc.xform(shoulder[0], ws=1, t=[mirror * 3.2, -3, 0])
    mc.xform(shoulderEnd[0], ws=1, t=[mirror * 3.2, -3, -1])
    mc.xform(upArm[0], ws=1, t=[mirror * 3.2, -7, -1])
    mc.xform(loArm[0], ws=1, t=[mirror * 3.2, -13, 0.5])
    mc.xform(armEnd[0], ws=1, t=[mirror * 3.2, -18, -1])
    mc.xform(armToe[0], ws=1, t=[mirror * 3.2, -19, -1])

    # orient joints
    mc.aimConstraint(shoulder[-2], scapula[-1], n=scapula[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.pointConstraint(upArm[-2], shoulderEnd[0], n=shoulderEnd[0] + '_pc')
    mc.aimConstraint(upArm[-2], shoulder[-1], n=shoulder[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.aimConstraint(loArm[-2], upArm[-1], n=upArm[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=armEnd[-2])
    mc.aimConstraint(armEnd[-2], loArm[-1], n=loArm[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=upArm[-2])
    mc.aimConstraint(armToe[-2], armEnd[-1], n=armEnd[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='object', wuo=armEnd[-2])

    if doubleElbow:
        mc.pointConstraint(upArm[-2], loArmA[0], w=.05)
        mc.pointConstraint(loArm[-2], loArmA[0], w=.95)
        mc.pointConstraint(loArm[-2], loArmB[0], w=.95)
        mc.pointConstraint(armEnd[-2], loArmB[0], w=.05)

        mc.pointConstraint(armEnd[-2], loArmC[0])
        mc.orientConstraint(upArm[-1], loArmA[0])
        mc.orientConstraint(loArm[-1], loArmB[0], mo=1)

        mc.aimConstraint(loArmB[-2], loArmA[-1], n=loArmA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=armEnd[-2])
        mc.aimConstraint(armEnd[-2], loArmB[-1], n=loArmB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=upArm[-2])

    if helpJoint:
        # up arm helper joint parent
        mc.parent(upArmHelper[-1], upArm[-1])
        mc.parent(upArmHelperA[-1], upArmHelper[-1])
        mc.parent(upArmHelperB[-1], upArmHelper[-1])
        mc.parent(upArmHelperC[-1], upArmHelper[-1])
        mc.parent(upArmHelperD[-1], upArmHelper[-1])
        mc.parent(upArmHelperAEnd[-1], upArmHelperA[-1])
        mc.parent(upArmHelperBEnd[-1], upArmHelperB[-1])
        mc.parent(upArmHelperCEnd[-1], upArmHelperC[-1])
        mc.parent(upArmHelperDEnd[-1], upArmHelperD[-1])

        # up arm helper control pos parent
        mc.parent(upArmHelper[0], upArm[-2])
        mc.parent(upArmHelperA[0], upArmHelper[-2])
        mc.parent(upArmHelperB[0], upArmHelper[-2])
        mc.parent(upArmHelperC[0], upArmHelper[-2])
        mc.parent(upArmHelperD[0], upArmHelper[-2])
        mc.parent(upArmHelperAEnd[0], upArmHelperA[-2])
        mc.parent(upArmHelperBEnd[0], upArmHelperB[-2])
        mc.parent(upArmHelperCEnd[0], upArmHelperC[-2])
        mc.parent(upArmHelperDEnd[0], upArmHelperD[-2])

        mc.delete(mc.parentConstraint(upArm[-2], upArmHelper[0]))
        mc.orientConstraint(upArm[-1], upArmHelper[0], n=upArmHelper[0] + '_oc')
        mc.setAttr(upArmHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(upArmHelperBEnd[-2] + '.tz', 0.5)
        mc.setAttr(upArmHelperCEnd[-2] + '.ty', -0.5)
        mc.setAttr(upArmHelperDEnd[-2] + '.tz', -0.5)

        mc.aimConstraint(upArmHelperAEnd[-2], upArmHelperA[-1], n=upArmHelperA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperBEnd[-2], upArmHelperB[-1], n=upArmHelperB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperCEnd[-2], upArmHelperC[-1], n=upArmHelperC[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperDEnd[-2], upArmHelperD[-1], n=upArmHelperD[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)

        # loArm help joint parent
        mc.parent(loArmHelper[-1], loArm[-1])
        mc.parent(loArmHelperA[-1], loArmHelper[-1])
        mc.parent(loArmHelperB[-1], loArmHelper[-1])
        mc.parent(loArmHelperAEnd[-1], loArmHelperA[-1])
        mc.parent(loArmHelperBEnd[-1], loArmHelperB[-1])

        # loArm help control pos parent
        mc.parent(loArmHelper[0], loArm[-2])
        mc.parent(loArmHelperA[0], loArmHelper[-2])
        mc.parent(loArmHelperB[0], loArmHelper[-2])
        mc.parent(loArmHelperAEnd[0], loArmHelperA[-2])
        mc.parent(loArmHelperBEnd[0], loArmHelperB[-2])

        mc.delete(mc.parentConstraint(loArm[-2], loArmHelper[0]))
        mc.orientConstraint(loArm[-1], loArmHelper[0], n=loArmHelper[0] + '_oc')
        mc.setAttr(loArmHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(loArmHelperBEnd[-2] + '.ty', -0.5)

        # armEnd help joint parent
        mc.parent(armEndHelper[-1], armEnd[-1])
        mc.parent(armEndHelperA[-1], armEndHelper[-1])
        mc.parent(armEndHelperB[-1], armEndHelper[-1])
        mc.parent(armEndHelperC[-1], armEndHelper[-1])
        mc.parent(armEndHelperD[-1], armEndHelper[-1])
        mc.parent(armEndHelperAEnd[-1], armEndHelperA[-1])
        mc.parent(armEndHelperBEnd[-1], armEndHelperB[-1])
        mc.parent(armEndHelperCEnd[-1], armEndHelperC[-1])
        mc.parent(armEndHelperDEnd[-1], armEndHelperD[-1])

        # armEnd help control pose parent
        mc.parent(armEndHelper[0], armEnd[-2])
        mc.parent(armEndHelperA[0], armEndHelper[-2])
        mc.parent(armEndHelperB[0], armEndHelper[-2])
        mc.parent(armEndHelperC[0], armEndHelper[-2])
        mc.parent(armEndHelperD[0], armEndHelper[-2])
        mc.parent(armEndHelperAEnd[0], armEndHelperA[-2])
        mc.parent(armEndHelperBEnd[0], armEndHelperB[-2])
        mc.parent(armEndHelperCEnd[0], armEndHelperC[-2])
        mc.parent(armEndHelperDEnd[0], armEndHelperD[-2])

        mc.delete(mc.parentConstraint(armEnd[-2], armEndHelper[0]))
        mc.orientConstraint(armEnd[-1], armEndHelper[0], n=armEndHelper[0] + '_oc')
        mc.setAttr(armEndHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(armEndHelperBEnd[-2] + '.tz', 0.5)
        mc.setAttr(armEndHelperCEnd[-2] + '.ty', -0.5)
        mc.setAttr(armEndHelperDEnd[-2] + '.tz', -0.5)

        helpJointObjs = [upArmHelper, upArmHelperA, upArmHelperAEnd, upArmHelperB, upArmHelperBEnd, upArmHelperC, upArmHelperCEnd, upArmHelperD, upArmHelperDEnd,
                        loArmHelper, loArmHelperA, loArmHelperAEnd, loArmHelperB, loArmHelperBEnd,
                        armEndHelper, armEndHelperA, armEndHelperAEnd, armEndHelperB, armEndHelperBEnd, armEndHelperC, armEndHelperCEnd, armEndHelperD, armEndHelperDEnd]
        for helpJointObj in helpJointObjs:
            mc.setAttr(helpJointObj[-2] + '.radius', 0.5)

    # Parent joints
    mc.parent(shoulder[-1], scapula[-1])
    mc.parent(shoulderEnd[-1], shoulder[-1])
    mc.parent(upArm[-1], shoulderEnd[-1])
    mc.parent(loArm[-1], upArm[-1])
    mc.parent(armEnd[-1], loArm[-1])
    mc.parent(armToe[-1], armEnd[-1])

    # set tag ------------------------------------------------------------------------------------------
    needTagObjs = [shoulder, shoulderEnd, upArm, loArm, armEnd, armToe]
    if doubleElbow:
        needTagObjs.extend([loArmA, loArmB, loArmC])
    if helpJoint:
        needTagObjs.extend([upArmHelper, upArmHelperA, upArmHelperAEnd, upArmHelperB, upArmHelperBEnd, upArmHelperC, upArmHelperCEnd, upArmHelperD, upArmHelperDEnd,
                            loArmHelper, loArmHelperA, loArmHelperAEnd, loArmHelperB, loArmHelperBEnd,
                            armEndHelper, armEndHelperA, armEndHelperAEnd, armEndHelperB, armEndHelperBEnd, armEndHelperC, armEndHelperCEnd, armEndHelperD, armEndHelperDEnd])
    for tagObj in needTagObjs:
        mc.setAttr(tagObj[-1] + '.tag', 'templateJoint tPose', type='string')

    # set doubleEblow math ------------------------------------------------------------------------------------------
    
    if doubleElbow:
        mc.parent(loArmB[-1], loArmA[-1])
        mc.parent(loArmC[-1], loArmB[-1])

        # help position loc
        mc.addAttr(loArm[-2], ln='doubleElbowWeight', at='float', k=1, min=0.1, max=9.9, dv=1)
        mc.addAttr(topnode, ln='doubleElbowWeight', at='float', k=1, uap=1, min=0.1, max=9.9, dv=1)
        mc.connectAttr(loArm[-2]+'.doubleElbowWeight', topnode+'.doubleElbowWeight')
        loArmAloc = aboutPublic.snapLoc(loArmA[-1], name=loArmA[-1]+'_loc')
        mc.parent(loArmAloc, loArmA[-2])
        mc.hide(loArmAloc)

        arg = 'vector $posUpArm = `xform - q - ws - rp "{0}"`;'.format(upArm[-2]) + '\n'
        arg += 'vector $posLoArm = `xform - q - ws - rp "{0}"`;'.format(loArm[-2]) + '\n'
        arg += 'vector $posEndArm = `xform - q - ws - rp "{0}"`;'.format(armEnd[-2]) + '\n'
        arg += 'vector $posLoArmA = << {0}.wpx, {0}.wpy, {0}.wpz >>;'.format(loArmAloc+'Shape.worldPosition[0]') + '\n\n'

        arg += 'float $uplength = `mag($posLoArm - $posLoArmA)`;' + '\n'
        arg += 'float $lolength = `mag($posEndArm - $posLoArm)`;' + '\n'
        arg += 'float $sumLength = $uplength + $lolength;' + '\n'
        arg += 'float $weight = {0}.doubleElbowWeight * 0.1;'.format(loArm[-2]) + '\n\n'

        arg += '$lenB = $weight * $sumLength;' + '\n'
        arg += '$lenA = $sumLength - $lenB;' + '\n'
        arg += '$lenC = `mag($posEndArm - $posLoArmA)`;' + '\n\n'

        arg += '$angle = acos( (pow($lenB, 2) + pow($lenC, 2) - pow($lenA, 2)) / (2 *$lenB * $lenC) );' + '\n'
        arg += 'vector $roVorg = $posEndArm - $posLoArmA;' + '\n'
        arg += 'vector $roVnew = unit($roVorg) * $lenB;' + '\n'
        arg += 'vector $axis = cross(($posUpArm - $posLoArm), ($posEndArm - $posLoArm));' + '\n'
        arg += 'vector $unitTransform = rot($roVnew, $axis, $angle) + $posLoArmA;' + '\n'
        arg += 'float $trsX = $unitTransform.x;' + '\n'
        arg += 'float $trsY = $unitTransform.y;' + '\n'
        arg += 'float $trsZ = $unitTransform.z;' + '\n\n'
        arg += 'xform - ws - t $trsX $trsY $trsZ {0};'.format(loArmB[2]) + '\n'
        arg += '{0}.scaleX = {1}.scaleX;'.format(loArmB[2], loArmAloc)

        mc.expression(n=topnode + '_exp', s=arg)

    # Create Ctrls-----------------------------------------------------------------------------------------------------------------------

    # scapula ctrls
    scapulaFkCtrl = controlTools.create(prefix + 'scapulaFk_ctrl', shape='jackThin', color=color, scale=[1.5, 1, 1])
    mc.pointConstraint(shoulder[-1], scapula[-1], scapulaFkCtrl[1], n=scapulaFkCtrl[1] + '_pc')
    mc.parentConstraint(scapula[-1], scapulaFkCtrl[0], n=scapulaFkCtrl[0] + '_prc')
    mc.setAttr(scapulaFkCtrl[0] + '.sx', mirror)
    mc.setAttr(scapulaFkCtrl[2] + '.ty', mirror)

    # should ctrls
    shoulderFkCtrl = controlTools.create(prefix + 'shoulderFk_ctrl', shape='semiCircle', color=color, scale=[3, 1.5, 1.5])
    mc.setAttr(shoulderFkCtrl[0] + '.sx', mirror)
    mc.pointConstraint(upArm[-1], shoulder[-1], shoulderFkCtrl[1], n=shoulderFkCtrl[1] + '_pc')
    mc.pointConstraint(shoulder[-1], shoulderFkCtrl[0], n=shoulderFkCtrl[0] + '_pc')
    # mc.orientConstraint(shoulder[-1], shoulderFkCtrl[0], n=shoulderFkCtrl[0] + '_prc')

    shoulderIkCtrl = controlTools.create(prefix + 'shoulderIk_ctrl', shape='C00_sphere', color=color, scale=1)
    mc.setAttr(shoulderIkCtrl[0] + '.sx', mirror)
    mc.pointConstraint(upArm[-1], shoulderIkCtrl[1], n=shoulderIkCtrl[1] + '_pc')

    # Fk Ctrls
    upArmFkCtrl = controlTools.create(prefix + 'upArmFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(upArmFkCtrl[-1], axis='z')
    mc.parentConstraint(upArm[-1], upArmFkCtrl[0], n=upArmFkCtrl[0] + '_prc')

    loArmFkCtrl = controlTools.create(prefix + 'loArmFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(loArmFkCtrl[-1], axis='z')
    mc.parentConstraint(loArm[-1], loArmFkCtrl[0], n=loArmFkCtrl[0] + '_prc')

    if doubleElbow:
        mc.parentConstraint(loArmB[-1], loArmFkCtrl[0], n=loArmFkCtrl[0] + '_prc')
    else:
        mc.parentConstraint(loArm[-1], loArmFkCtrl[0], n=loArmFkCtrl[0] + '_prc')

    toeArmFkCtrl = controlTools.create(prefix + 'toeArmFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(toeArmFkCtrl[-1], axis='z')
    mc.parentConstraint(armEnd[-1], toeArmFkCtrl[0], n=toeArmFkCtrl[0] + '_prc')

    # IK Ctrls
    armIkCtrl = controlTools.create(prefix + 'armIk_ctrl', shape='C00_sphere', color=color, scale=1.5, jointCtrl=True)
    mc.pointConstraint(armEnd[-1], armIkCtrl[0], n=armIkCtrl[0] + '_pc')

    armIkLocalCtrl = controlTools.create(prefix + 'armIkLocal_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(armIkLocalCtrl[-1], axis='z')
    mc.parentConstraint(armEnd[-1], armIkLocalCtrl[0], n=armIkLocalCtrl[0] + '_prc')

    # >>Elbow PV
    elbowIkCtrl = controlTools.create(prefix + 'elbowIk_ctrl', shape='C00_sphere', color=color, scale=0.4, jointCtrl=True)

    if doubleElbow:
        mc.pointConstraint(loArm[-1], loArmB[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_pc')
        mc.orientConstraint(loArm[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_oc', mo=1)
    else:
        mc.pointConstraint(loArm[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_pc')
        mc.orientConstraint(upArm[-1], loArm[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_oc', mo=1)
    mc.setAttr(elbowIkCtrl[2] + '.tz', 6 * mirror)

    # Set ctrl
    limbSetCtrl = controlTools.create(prefix + 'armSet_ctrl', shape='C01_cube', color=color, scale=0.4)
    mc.setAttr(limbSetCtrl[0] + '.sx', mirror)
    mc.pointConstraint(armEnd[-1], limbSetCtrl[0], n=limbSetCtrl[0] + '_pc')

    # >> PSD Driver Create
    if poseDriver:
        # create psd.
        armpsd = {}
        armEndpsd = {}

        if mirror == 1:
            armpsd = poseDriverTool.createBridge(prefix + 'arm', axis='-y', mirror=False)
            armEndpsd = poseDriverTool.createBridge(prefix + 'armEnd', axis='-y', mirror=False)
        elif mirror == -1:
            armpsd = poseDriverTool.createBridge(prefix + 'arm', axis='-y', mirror=True)
            armEndpsd = poseDriverTool.createBridge(prefix + 'armEnd', axis='-y', mirror=True)

        # match temp size.
        # arm psd
        poseDriverTool.scaleBridge(prefix + 'arm', 0.05)
        poseDriverTool.constraintBridge(parentObj=upArm[-1], followObj=upArm[-1], parentHandle=armpsd['parent'], followHandle=armpsd['follow'])
        armfollow_ConstraintNode = mc.parentConstraint(armpsd['follow'], q=True)
        mc.delete(armfollow_ConstraintNode)

        # armEnd psd
        poseDriverTool.scaleBridge(prefix + 'armEnd', 0.05)
        poseDriverTool.constraintBridge(parentObj=armEnd[-1], followObj=armEnd[-1], parentHandle=armEndpsd['parent'], followHandle=armEndpsd['follow'])
        armEndfollow_ConstraintNode = mc.parentConstraint(armEndpsd['follow'], q=True)
        mc.delete(armEndfollow_ConstraintNode)

        #clean
        mc.parent(armpsd['parent'], topnode + 'Ctrls')
        mc.parent(armEndpsd['parent'], topnode + 'Ctrls')

    # CLEAN----------------------------------------------------------------------------------------------------------------------
    mc.parent(scapula[0], shoulder[0], shoulderEnd[0], upArm[0], loArm[0], armEnd[0], topnode + 'Ctrls')
    if doubleElbow:
        mc.parent(loArmA[0], loArmB[0], loArmC[0], topnode + 'Ctrls')

    mc.parent(scapulaFkCtrl[0], shoulderFkCtrl[0], shoulderIkCtrl[0],
              armIkCtrl[0], armIkLocalCtrl[0], elbowIkCtrl[0],
              upArmFkCtrl[0], loArmFkCtrl[0], toeArmFkCtrl[0],
              limbSetCtrl[0], topnode + 'Ctrls')

    mc.parent(armToe[0], armEnd[-2])
    mc.hide(armToe[-2])
    mc.hide(shoulderEnd[0])

    mc.setAttr(armToe[-1] + '.jointOrientX', 0)
    mc.setAttr(armToe[-1] + '.jointOrientY', 0)
    mc.setAttr(armToe[-1] + '.jointOrientZ', 0)

    # Lock
    aboutLock.lock(shoulder + upArm + loArm + armEnd + loArmA + loArmB + loArmC)
    aboutLock.unlock([shoulder[-2], upArm[-2], loArm[-2], armEnd[-2]], 't ro')
    aboutLock.unlock(armEnd[-2], 'r')

    if doubleElbow:
        aboutLock.unlock(loArmA[-2], 'tx')
        aboutLock.unlock(loArmB[2], 't ro s')
        aboutLock.unlock(loArm[-2], 'doubleElbowWeight')

    if bendy:
        if doubleElbow:
            bendy2Limb.template(prefix + 'arm', topnode, [upArm[-1], loArm[-1], loArmB[-1], armEnd[-1]])
        else:
            bendy2Limb.template(prefix + 'arm', topnode, [upArm[-1], loArm[-1], armEnd[-1]])

    aboutLock.lock(scapulaFkCtrl + shoulderFkCtrl + shoulderIkCtrl + upArmFkCtrl + loArmFkCtrl + armIkCtrl + armIkLocalCtrl + elbowIkCtrl + limbSetCtrl)
    aboutLock.unlock([scapulaFkCtrl[-1], shoulderFkCtrl[-1], shoulderIkCtrl[-1], upArmFkCtrl[-1], loArmFkCtrl[-1], armIkCtrl[-1], armIkLocalCtrl[-1]], 't s')
    aboutLock.unlock(elbowIkCtrl[-1], 'ty tz s')

    # Positiion
    mc.xform(topnode, r=1, s=[1, 1, 1])
    mc.xform(topnode, ws=1, t=[0, 19, 0])
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))

    if addFoot:
        reload(footPart)
        footPart.template(info, side, footprefix, armEnd[-1], armIkCtrl[-1], loArmFkCtrl[-1])


# Build Anim
def anim():
    parts = templateTools.getParts('quadArm')
    for part in parts:

        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        doubleElbow = templateTools.getArgs(part, 'doubleElbow')
        twist = templateTools.getArgs(part, 'twist')
        bendy = templateTools.getArgs(part, 'bendy')
        stretch = templateTools.getArgs(part, 'stretch')
        volume = templateTools.getArgs(part, 'volume')
        autoShoulder = templateTools.getArgs(part, 'autoShoulder')
        addFoot = templateTools.getArgs(part, 'addFoot')
        poseDriver = templateTools.getArgs(part, 'poseDriver')
        footprefix = prefix
        prefix = templateTools.getPrefix(side, prefix)

        # declare jnts
        scapula = prefix + 'scapula_drv'
        shoulder = prefix + 'shoulder_drv'
        shoulderEnd = prefix + 'shoulderEnd_drv'
        upArm = prefix + 'upArm_drv'
        loArm = prefix + 'loArm_drv'
        loArmA = prefix + 'loArmA_drv'
        loArmB = prefix + 'loArmB_drv'
        loArmC = prefix + 'loArmC_drv'
        armEnd = prefix + 'armEnd_drv'
        armToe = prefix + 'armToe_drv'

        # drv jnts
        drvJnts = [upArm, loArm, armEnd]

        # fk jnts
        fkJnts = []
        for i in range(len(drvJnts)):
            jnt = drvJnts[i]
            if mc.objExists(jnt):
                fkJnt = mc.duplicate(jnt, n=jnt.replace('_drv', '_fk'), po=1)[0]
                fkJnts.append(fkJnt)
        fkJntsNum = len(fkJnts)
        for i in range(fkJntsNum):
            if i != 0:
                mc.parent(fkJnts[i], fkJnts[i - 1])

        # ik jnts
        ikJnts = []
        for i in range(len(drvJnts)):
            jnt = drvJnts[i]
            if mc.objExists(jnt):
                ikJnt = mc.duplicate(jnt, n=jnt.replace('_drv', '_ik'), po=1)[0]
                ikJnts.append(ikJnt)
        ikJntsNum = len(ikJnts)
        for i in range(ikJntsNum):
            if i != 0:
                mc.parent(ikJnts[i], ikJnts[i - 1])

        # create controls
        el = aboutPublic.snapLoc(prefix + 'elbowIk_ctrlPrep')
        ul = aboutPublic.snapLoc(upArm)
        wl = aboutPublic.snapLoc(armEnd)

        # mirror value
        mirror = 1
        if side == 'rt':
            mirror = -1


        # > Create Ctrls
        # -----------------------------------------------------------------------------------------------------------------------
        # > set up ankle / toeFk control axis
        #  >> create helpfull locator
        upAxisloc = aboutPublic.snapLoc(armEnd, prefix + 'ankle_up_loc')
        orgAxisloc = aboutPublic.snapLoc(armEnd, prefix + 'ankle_org_loc')
        aimAxisloc = aboutPublic.snapLoc(armEnd, prefix + 'ankle_axis_loc')
        orgTy = mc.getAttr(upAxisloc + '.ty')
        mc.setAttr(upAxisloc + '.ty', orgTy + 0.1)

        if addFoot:
            # match foot aim axis
            ball = prefix + 'ball_drv'
            mc.delete(mc.aimConstraint(ball, aimAxisloc, aim=[0, 0, 1], u=[0, 1, 0], wut='object', wuo=upAxisloc))

            # set one axis roll
            axisValue = aboutPublic.getAxisTwistValue(orgAxisloc, aimAxisloc, axis='Y')
            mc.setAttr(orgAxisloc + '.ry', axisValue)
            aboutPublic.fastGrp(orgAxisloc, grpNameList=['grp', 'offset'], worldOrient=False)

            # match fk arm original axis
            mc.setAttr(orgAxisloc + '_offset.rx', 90 * mirror)
            mc.setAttr(orgAxisloc + '_offset.rz', -90 * mirror)
        else:
            mc.group(orgAxisloc, n=orgAxisloc + '_grp')
            mc.delete(mc.orientConstraint(armEnd, orgAxisloc))

        # Seting ctrl
        limbSetCtrl = controlTools.create(prefix + 'armSet_ctrl', snapTo=wl, useShape=prefix + 'armSet_ctrlPrep')
        mc.delete(mc.orientConstraint(orgAxisloc, limbSetCtrl[0]))
        refDis = abs(mc.getAttr(armEnd + '.tx'))
        mc.setAttr(limbSetCtrl[-1] + '.ty', -0.2 * refDis * mirror)
        mc.parentConstraint(armEnd, limbSetCtrl[0], n=limbSetCtrl[0] + '_prc', mo=1)

        # scapula ctrls
        scapulaFkCtrl = controlTools.create(prefix + 'scapulaFk_ctrl', snapTo=scapula, useShape=prefix + 'scapulaFk_ctrlPrep')

        # Shoulder ctrls
        shoulderFkCtrl = controlTools.create(prefix + 'shoulderFk_ctrl', snapTo=shoulder, useShape=prefix + 'shoulderFk_ctrlPrep')
        shoulderIkCtrl = controlTools.create(prefix + 'shoulderIk_ctrl', snapTo=ul, useShape=prefix + 'shoulderIk_ctrlPrep')

        # IK ctrls
        armIkCtrl = controlTools.create(prefix + 'armIk_ctrl', snapTo=wl, useShape=prefix + 'armIk_ctrlPrep')
        armIkLocalCtrl = controlTools.create(prefix + 'armIkLocal_ctrl', snapTo=orgAxisloc, useShape=prefix + 'armIkLocal_ctrlPrep')
        elbowIkCtrl = controlTools.create(prefix + 'elbowIk_ctrl', snapTo=el, useShape=prefix + 'elbowIk_ctrlPrep')
        armEndIkSnapCtrl = controlTools.create(prefix + 'armEndIk_snap_ctrl', snapTo=wl)
        elbowIkSnapCtrl = controlTools.create(prefix + 'elbowIkSnap_ctrl', snapTo=el)

        if side == 'rt':
            controlTools.reverseCtrl(scapulaFkCtrl[-1], prefix + 'scapulaFk_ctrlPrep')
            controlTools.reverseCtrl(shoulderFkCtrl[-1], prefix + 'shoulderFk_ctrlPrep')
            controlTools.reverseCtrl(shoulderIkCtrl[-1], prefix + 'shoulderIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(armIkCtrl[-1], prefix + 'armIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(armEndIkSnapCtrl[-1], t=1)

        # FK ctrls
        upArmFkCtrl = controlTools.create(prefix + 'upArmFk_ctrl', snapTo=upArm, useShape=prefix + 'upArmFk_ctrlPrep')
        loArmFkCtrl = controlTools.create(prefix + 'loArmFk_ctrl', snapTo=loArm, useShape=prefix + 'loArmFk_ctrlPrep')
        toeArmFkCtrl = controlTools.create(prefix + 'toeArmFk_ctrl', snapTo=orgAxisloc, useShape=prefix + 'toeArmFk_ctrlPrep')
        armEndFkSnapCtrl = controlTools.create(prefix + 'armEndFk_snap_ctrl', snapTo=orgAxisloc)
        
        # set rotate orider
        nodes = [shoulder,
                 upArm,
                 loArm,
                 loArmB,
                 armEnd,
                 armIkCtrl[-1],
                 upArmFkCtrl[-1],
                 loArmFkCtrl[-1],
                 shoulderFkCtrl[-1],
                 shoulderIkCtrl[-1]]

        for j in nodes:
            if mc.objExists(j):
                mc.setAttr(j + '.ro', 0)


        # > Setup fk
        # ----------------------------------------------------------------------------------------------------------
        mc.addAttr(upArmFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(loArmFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

        mc.parentConstraint(upArmFkCtrl[-1], fkJnts[0], mo=0, n=fkJnts[0] + '_prc')
        mc.parentConstraint(loArmFkCtrl[-1], fkJnts[1], mo=0, n=fkJnts[1] + '_prc')
        mc.parentConstraint(toeArmFkCtrl[-1], fkJnts[-1], mo=0, n=fkJnts[-1] + '_prc')
        mc.parent(loArmFkCtrl[0], upArmFkCtrl[-1])
        mc.parent(toeArmFkCtrl[0], loArmFkCtrl[-1])
        mc.parent(upArmFkCtrl[0], shoulderFkCtrl[-1])

        mc.pointConstraint(shoulderEnd, upArmFkCtrl[0], n=upArmFkCtrl[0] + '_pc')


        # > Setup ik
        # ----------------------------------------------------------------------------------------------------------
        ik = mc.ikHandle(sj=ikJnts[0], ee=ikJnts[-1], ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'arm_ikh')[0]
        mc.parent(ik, armIkCtrl[-1])
        mc.hide(ik)
        mc.orientConstraint(armIkLocalCtrl[-1], ikJnts[-1], n=ikJnts[-1] + '_oc', mo=1)

        # attr add
        mc.addAttr(armIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(elbowIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(armIkCtrl[-1], ln='twist', at='double', k=1)
        mc.addAttr(armIkCtrl[-1], ln='local', at='enum', k=1, en='off:on')
        controlTools.tagKeyable(armIkCtrl[-2:], 't r twist local soft stretch slide upLength loLength twist')

        # local ctrl vis
        localCtrlShape = mc.listRelatives(armIkLocalCtrl[-1], s=1)[0]
        mc.connectAttr(armIkCtrl[-1] + '.local', localCtrlShape + '.v')
        mc.setAttr(armIkCtrl[-1] + '.local', k=0, cb=1)

        # Setup IK PV/twist
        elbowIkLineGrp = aboutCrv.createCrvBetween2Pos(name=elbowIkCtrl[-1] + '_crv', st=loArm, ed=elbowIkCtrl[-1])
        mc.setAttr(elbowIkLineGrp + '.inheritsTransform', 0)

        # -->> Setup IK PV - offset/twist
        pvnodes = poleVectorTools.pvFollow(elbowIkCtrl[-1], ikJnts, armIkCtrl[-1], mirror)
        mc.poleVectorConstraint(elbowIkCtrl[-1], ik, n=ik + '_pvc')
        mc.pointConstraint(shoulderEnd, ikJnts[0], n=ikJnts[0] + '_pc')

        # > scapula
        mc.parentConstraint(scapulaFkCtrl[-1], scapula, n=scapula + '_prc', mo=1)

        # > Shoulder
        # ---------------------------------------------------------------------------------------------------------------
        mc.parentConstraint(shoulderFkCtrl[-1], shoulder, n=shoulder + '_prc', mo=1)
        mc.pointConstraint(shoulderIkCtrl[-1], shoulderEnd, n=shoulderEnd + '_pc', mo=1)
        mc.parent(shoulderIkCtrl[0], shoulderFkCtrl[-1])
        mc.parent(shoulderFkCtrl[0], scapulaFkCtrl[-1])
        autoShoulderGrp = ''

        if autoShoulder:
            # create aim ik system
            aimOrgJnt = mc.duplicate(shoulder, po=True, n=shoulder.replace('_drv', '') + '_aimOrg')[0]
            aimStJnt = mc.duplicate(shoulder, po=True, n=shoulder.replace('_drv', '') + '_aimSt')[0]
            aimEdJnt = mc.duplicate(armEnd, po=True, n=shoulder.replace('_drv', '') + '_aimEd')[0]
            mc.parent(aimStJnt, aimOrgJnt)
            mc.parent(aimEdJnt, aimStJnt)
            shoulderAimIk = mc.ikHandle(sj=aimStJnt, ee=aimEdJnt, ap=1, sol='ikSCsolver', n=prefix + 'shoulderAim_ik')[0]

            shoulderRollLoc = aboutPublic.snapLoc(aimOrgJnt, name=prefix + 'shoulderRoll_loc')
            shoulderRollLocGrp = aboutPublic.fastGrp(shoulderRollLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]
            mc.delete(mc.orientConstraint(aimOrgJnt, shoulderRollLocGrp))

            shoulderAimLoc = aboutPublic.snapLoc(armEnd, name=prefix + 'autoShoulderAim_loc')
            shoulderAimLocGrp = aboutPublic.fastGrp(shoulderAimLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]

            if side == 'rt':
                controlTools.reverseCtrl(shoulderRollLoc)
                controlTools.reverseCtrl(shoulderAimLoc, t=1)

            # Auto shoulder system connect
            autoShoulderGrp = mc.createNode('transform', n=prefix + 'autoShoulder_grp')
            mc.addAttr(shoulderFkCtrl[-1], ln='autoShoulder', at='double', k=1, max=10)

            mc.parent(shoulderAimIk, shoulderAimLoc)
            mc.parent(aimOrgJnt, shoulderRollLocGrp, shoulderAimLocGrp, autoShoulderGrp)

            autoShoulderOc = mc.orientConstraint(aimOrgJnt, aimStJnt, shoulderRollLoc, n=shoulderRollLoc + '_oc', mo=True)[0]
            mc.setAttr(autoShoulderOc + '.interpType', 0)
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W0'.format(aimOrgJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder', dv=0, v=1, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W0'.format(aimOrgJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder', dv=10, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W1'.format(aimStJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder', dv=0, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W1'.format(aimStJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder', dv=10, v=1, itt='linear', ott='linear')

            mc.connectAttr(armIkCtrl[-1] + '.tx', shoulderAimLoc + '.tx')
            mc.connectAttr(armIkCtrl[-1] + '.ty', shoulderAimLoc + '.ty')
            mc.connectAttr(armIkCtrl[-1] + '.tz', shoulderAimLoc + '.tz')

            mc.connectAttr(shoulderRollLoc + '.rx', shoulderFkCtrl[2] + '.rx')
            mc.connectAttr(shoulderRollLoc + '.ry', shoulderFkCtrl[2] + '.ry')
            mc.connectAttr(shoulderRollLoc + '.rz', shoulderFkCtrl[2] + '.rz')


        # > Connect with torso
        # ---------------------------------------------------------------------------------------------------------------
        if mc.objExists(parent):
            connectLoc = parent + '_connect_loc'
            mc.parentConstraint(connectLoc, scapulaFkCtrl[0], n=scapulaFkCtrl[0] + '_prc', mo=1)
            if autoShoulder:
                mc.parentConstraint(connectLoc, autoShoulderGrp, n=autoShoulderGrp + '_prc', mo=1)
        else:
            connectLoc = None


        # > Double Elbow Rig
        # ---------------------------------------------------------------------------------------------------------------
        db_mpNode = '{0}mod'.format(prefix + 'armdb_')
        if doubleElbow:
            # db center pivot joint set
            db_root = mc.duplicate(loArm, po=1, n=prefix + 'db_root_drv')[0]
            db_pviot = mc.duplicate(loArm, po=1, n=prefix + 'db_pviot_drv')[0]
            mc.parentConstraint(upArm, db_root, n=db_root + '_prc', mo=1)
            mc.parent(db_pviot, db_root)
            mc.parent(loArmA, db_pviot)
            mc.pointConstraint(loArm, db_pviot)

            # db ikhandle set
            dbik = mc.ikHandle(sj=loArmA, ee=loArmC, ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'armdb_ikh')[0]

            # db ik control loc
            dbikloc = aboutPublic.snapLoc(armEnd, name=prefix + 'armdb_ikloc')
            mc.pointConstraint(armEnd, dbikloc, n=dbikloc + '_pc')
            mc.pointConstraint(dbikloc, dbik, n=dbik + '_pc')
            mc.orientConstraint(armEnd, loArmC, n=loArmC + '_oc')

            # db pv control loc
            dbPvloc = aboutPublic.snapLoc(loArm, name=prefix + 'armdb_pvloc')
            mc.parentConstraint(loArm, dbPvloc, n=dbPvloc + '_pc')
            mc.poleVectorConstraint(dbPvloc, dbik, n=dbik + '_pvc')

            # db stretch
            disJnts = [loArm, armEnd]
            stretch1Tools.stretchIk_db(prefix + 'armdb_', db_pviot, disJnts, loArmC, dbikloc, 'tx', mpNode=None)

            # clean db
            if not mc.objExists(db_mpNode):
                mc.createNode('transform', n=db_mpNode)
                mc.parent(db_mpNode, 'controls')

            db_needP = [dbik, dbikloc, dbPvloc, db_root]
            mc.parent(db_needP, db_mpNode)

            db_needVis = [dbik, dbikloc, dbPvloc]
            for need in db_needVis:
                mc.hide(need)

        # > Twist & Bendy
        # ---------------------------------------------------------------------------------------------------------------
        #
        # tips: the default joint num is 5 .
        # bridgeNum must be same with bendy joint number.

        twistBridges = []
        bendyInfo = {}
        bendyUpRootJntGrp = []
        bendyLoRootJntGrp = []
        bendyJointList = []
        twistInfo = {}

        if twist:
            twistInfo = nonRoll.limbTwist(limbJnts=[[shoulder, upArm], [upArm, loArm, armEnd]], twistAxis='x', mirror=mirror)
            twistBridges = twistInfo['vmd']

        if bendy:
            if doubleElbow:
                bendyInfo = bendy2Limb.anim(prefix + 'arm', [upArm, loArmA, loArmB, loArmC], twistBridges=twistBridges, volume=volume)
            else:
                bendyInfo = bendy2Limb.anim(prefix + 'arm', [upArm, loArm, armEnd], twistBridges=twistBridges, volume=volume)

            bendyUpRootJnt = bendyInfo['upjnts'][0]
            bendyLoRootJnt = bendyInfo['lojnts'][0]
            bendyJointList = bendyInfo['jointList']

            bendyUpRootJntGrp = aboutPublic.createParentGrp(bendyUpRootJnt, 'grp')
            bendyLoRootJntGrp = aboutPublic.createParentGrp(bendyLoRootJnt, 'grp')

            mc.parentConstraint(shoulderEnd, bendyUpRootJntGrp, n=bendyUpRootJntGrp + '_prc', mo=True)
            mc.parentConstraint(loArm, bendyLoRootJntGrp, n=bendyLoRootJntGrp + '_prc', mo=True)

        # fk ik switch / display
        # ---------------------------------------------------------------------------------------------------------------

        # switch
        mc.addAttr(limbSetCtrl[-1], ln='IKFK', at='double', dv=1, min=0, max=1, k=1)
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', ik + '.ikBlend')

        switchNode = mc.createNode('remapValue', n=prefix + 'armSwitchIKFK_rv')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', switchNode + '.inputValue')
        mc.setAttr(switchNode + '.outputMin', 1)
        mc.setAttr(switchNode + '.outputMax', 0)

        # switch constraint node weights
        jntNum = len(drvJnts)

        for i in range(jntNum):
            prc = mc.parentConstraint(ikJnts[i], fkJnts[i], drvJnts[i], n=drvJnts[i] + '_prc', mo=1)[0]
            mc.connectAttr(limbSetCtrl[-1] + '.IKFK', prc + '.' + ikJnts[i] + 'W0')
            mc.connectAttr(switchNode + '.outValue', prc + '.' + fkJnts[i] + 'W1')

        # display
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', armIkCtrl[0] + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', elbowIkLineGrp + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', elbowIkCtrl[0] + '.v')
        displayRv = mc.createNode('reverse', n=prefix + 'armIKFK_vis_rv')
        mc.connectAttr(armIkCtrl[0] + '.v', displayRv + '.ix')
        mc.connectAttr(displayRv + '.ox', upArmFkCtrl[0] + '.v')

        # --------------------------------------- Start: !!! Do not modify the running order !!!---------------------------------------------------------------------------
        # > Sticky & Soft & Stretch
        # ---------------------------------------------------------------------------------------------------------------
        # ik
        stretch2Info = stretch2Tools.stretchSoftIk(prefix + 'arm_', shoulderEnd, ikJnts, armIkCtrl[-1], elbowIkCtrl[-1], stretch)
        blendloc = stretch2Info['blend']
        controlloc = stretch2Info['controlloc']
        mc.pointConstraint(blendloc, ik)

        # Add Foot System
        # ---------------------------------------------------------------------------------------------------------------
        footInfo = {}
        if addFoot:
            footInfo = footPart.anim(side, footprefix, armEnd, armIkCtrl[-1], toeArmFkCtrl[-1], limbSetCtrl[-1])
            footjnts = [footInfo['ankle'], footInfo['ball']]
            assetCommon.bindSet(footjnts)
            mc.pointConstraint(footInfo['stretchRev'], controlloc, n=controlloc + '_pc')
        else:
            mc.pointConstraint(armIkCtrl[-1], controlloc, n=controlloc + '_pc')

        # fk
        stretch2Tools.stretchFk(prefix + 'arm_', FkCtrls=[upArmFkCtrl[-1], loArmFkCtrl[-1]])

        # --------------------------------------- End: !!! Do not modify the running order !!!---------------------------------------------------------------------------

        # > Pose Drivers
        # ---------------------------------------------------------------------------------------------------------------
        psdGrp = '{0}arm_psd_noTrans'.format(prefix)
        if poseDriver:
            if not mc.objExists(psdGrp):
                mc.createNode('transform', n=psdGrp)
                mc.hide(psdGrp)

            # arm psd
            armPsdPrefix = prefix + 'arm'
            armPsdParent = armPsdPrefix + '_psd_parent_handle'
            armPsdFollow = armPsdPrefix + '_psd_follow_handle'
            mc.parent(armPsdParent, psdGrp)
            poseDriverTool.constraintBridge(parentObj=shoulder, followObj=upArm, parentHandle=armPsdParent, followHandle=armPsdFollow)

            # armEnd psd
            armEndPsdPrefix = prefix + 'armEnd'
            armEndPsdParent = armEndPsdPrefix + '_psd_parent_handle'
            armEndPsdFollow = armEndPsdPrefix + '_psd_follow_handle'
            mc.parent(armEndPsdParent, psdGrp)

            if bendy:
                poseDriverTool.constraintBridge(parentObj=bendyInfo['lojnts'][-1], followObj=armEnd,
                                                parentHandle=armEndPsdParent, followHandle=armEndPsdFollow)
            else:
                if doubleElbow:
                    poseDriverTool.constraintBridge(parentObj=loArmB, followObj=armEnd,
                                                    parentHandle=armEndPsdParent, followHandle=armEndPsdFollow)
                else:
                    poseDriverTool.constraintBridge(parentObj=loArm, followObj=armEnd,
                                                    parentHandle=armEndPsdParent, followHandle=armEndPsdFollow)

        # ---------------------------------------------------------------------------------------------------------------
        # IK FK Snap
        snapGrp = '{0}arm_snap_noTrans'.format(prefix)
        if not mc.objExists(snapGrp):
            mc.createNode('transform', n=snapGrp)
            mc.hide(snapGrp)

        mc.parent(armEndIkSnapCtrl[0], armEndFkSnapCtrl[0], elbowIkSnapCtrl[0], snapGrp)

        mc.delete(elbowIkSnapCtrl[2])
        elbowIkSnap = mc.rename(elbowIkSnapCtrl[1], prefix + 'elbowIk_ctrl_snap')
        mc.rename(elbowIkSnapCtrl[0], prefix + 'elbowIk_ctrl_snap_grp')
        mc.parentConstraint(drvJnts[1], elbowIkSnap, n=elbowIkSnap + '_prc', mo=1)

        snapEnd = drvJnts[2]
        if addFoot:
            snapEnd = footInfo['ankle']

        mc.delete(armEndFkSnapCtrl[2])
        armEndFkSnap = mc.rename(armEndFkSnapCtrl[1], prefix + 'toeArmFk_ctrl_snap')
        mc.rename(armEndFkSnapCtrl[0], prefix + 'toeArmFk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, armEndFkSnap, n=armEndFkSnap + '_prc', mo=1)

        mc.delete(armEndIkSnapCtrl[2])
        armEndIkSnap = mc.rename(armEndIkSnapCtrl[1], prefix + 'armIk_ctrl_snap')
        mc.rename(armEndIkSnapCtrl[0], prefix + 'armIk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, armEndIkSnap, n=armEndIkSnap + '_prc', mo=1)


        # modify motion joints
        if bendy:
            if doubleElbow:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-1].replace('_drv', ''))
                mc.delete(loArmB.replace('_drv', ''))
            else:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-2].replace('_drv', ''))
                mc.delete(bendyInfo['upjnts'][-1].replace('_drv', ''))

        if addFoot:
            mc.parent(footInfo['ankle'].replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))
            mc.delete(armEnd.replace('_drv', ''))
            mc.delete(footInfo['ballEnd'].replace('_drv', ''))
            mc.delete(footInfo['heel'].replace('_drv', ''))
        else:
            mc.parent(armEnd.replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))

        mc.parent(bendyInfo['upjnts'][0].replace('_drv', ''), shoulder.replace('_drv', ''))
        mc.delete(bendyInfo['lojnts'][-1].replace('_drv', ''))
        mc.delete(shoulderEnd.replace('_drv', ''))


        # Clean
        # ---------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'arm_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # parent
        # ctrls Parent
        mc.parent(armIkLocalCtrl[0], armIkCtrl[-1])

        ctrlNeedP = [elbowIkCtrl[0], pvnodes['root'], elbowIkLineGrp, armIkCtrl[0], limbSetCtrl[0], scapulaFkCtrl[0]]
        if bendy:
            ctrlNeedP.append(bendyInfo['rootGrp'])
        if autoShoulder:
            ctrlNeedP.append(autoShoulderGrp)

        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # jnts Parent
        jntNeedP = [scapula, ikJnts[0], fkJnts[0]]
        if bendy:
            jntNeedP.append(bendyUpRootJntGrp)
            jntNeedP.append(bendyLoRootJntGrp)
        for need in jntNeedP:
            mc.parent(need, mpNode)

        # noTrans Parent
        noTransNeedP = [snapGrp]
        if twist:
            noTransNeedP.append(twistInfo['noTrans'])
        if bendy:
            noTransNeedP.append(bendyInfo['noTrans'])
        if poseDriver:
            noTransNeedP.append(psdGrp)
        for need in noTransNeedP:
            mc.parent(need, 'noTransform')

        # hide
        needHList = [fkJnts[0], ikJnts[0], ik, connectLoc]
        if autoShoulder:
            needHList.append(autoShoulderGrp)
        for need in needHList:
            mc.hide(need)

        # delete
        mc.delete(orgAxisloc + '_grp', aimAxisloc, upAxisloc, el, ul, wl)

        # keyable tag
        # -----------------------------------------------------------------------------------------------
        # > shoulder
        controlTools.tagKeyable(shoulderFkCtrl[-2:], 't r')
        controlTools.tagKeyable(shoulderIkCtrl[-2:], 't')
        # > ik controls
        controlTools.tagKeyable(armIkCtrl[-2:], 't r local twist stretch soft slide upLength loLength midLength '
                                                'footPivot rollAngle heelTwist roll sideRoll toeLift toe ball heel toeTwist ballTwist')
        controlTools.tagKeyable(armIkLocalCtrl[-2:], 'r')
        controlTools.tagKeyable(elbowIkCtrl[-2:], 't sticky')
        # >fk controls
        controlTools.tagKeyable(upArmFkCtrl[-2:] + toeArmFkCtrl[-2:], 'r length')
        controlTools.tagKeyable(loArmFkCtrl[-2:], 'rz length')
        # >setting control
        controlTools.tagKeyable(limbSetCtrl[-2:], 'IKFK')

        spaceTools.tag(upArmFkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(shoulderFkCtrl[-1], connectLoc), oo=True, dv=1)
        spaceTools.tag(armIkCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(connectLoc), dv=2)
        spaceTools.tag(elbowIkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(pvnodes['space'], connectLoc), dv=0, con=elbowIkCtrl[-2])
        tagTools.tagIkFkSnap([ upArmFkCtrl[-1], loArmFkCtrl[-1], toeArmFkCtrl[-1], armIkCtrl[-1], elbowIkCtrl[-1]], prefix, 'quadArm')

        if bendy:
            assetCommon.bindSet([shoulder] + bendyJointList)
        else:
            assetCommon.bindSet([shoulder, upArm, loArm, loArmB, armEnd])
