######################################
#   Rig Build Part
######################################
from importlib import reload
import maya.cmds as mc
import templateTools
import controlTools
from rxCore import aboutLock
from rxCore import aboutCrv
from rxCore import aboutPublic
import nonRoll
import bendy2Limb
import tagTools
import spaceTools
import stretch1Tools
import stretch2Tools
import assetCommon
import poleVectorTools
import poseDriverTool

reload(poseDriverTool)


# Build Tempalte
def template(side='lf', prefix='', parent='chest', doubleElbow=False, twist=True, bendy=True, stretch=True,
             volume=False, autoShoulder=True, poseDriver=False, helpJoint=False):
    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['doubleElbow'] = doubleElbow
    args['twist'] = twist
    args['stretch'] = stretch
    args['bendy'] = bendy
    args['volume'] = volume
    args['autoShoulder'] = autoShoulder
    args['poseDriver'] = poseDriver
    args['helpJoint'] = helpJoint

    # Args to lock once part is built
    lockArgs = ['doubleElbow', 'twist', 'bendy', 'stretch']

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('bipedArm', args, lockArgs)
    if not info:
        print('Exiting... ')
        return

    topnode = info[0]
    prefix = info[1]

    # Set mirror value and colorID
    color = 'blue'
    doubleColor = 'cobalt'
    mirror = 1
    if side == 'rt':
        mirror = -1
        color = 'red'
        doubleColor = 'violet'

    # > Create joints
    # > CreateJoint return [grp, con, sdk, pos, jnt]
    # ------------------------------------------------------------------------------------------------------------------
    shoulder = templateTools.createJoint(prefix + 'shoulder', topnode, color, pc=1, oc=0)
    shoulderEnd = templateTools.createJoint(prefix + 'shoulderEnd', topnode, color, pc=1, oc=0)
    upArm = templateTools.createJoint(prefix + 'upArm', topnode, color, pc=1, oc=0)
    loArm = templateTools.createJoint(prefix + 'loArm', topnode, color, pc=1, oc=0)
    wrist = templateTools.createJoint(prefix + 'wrist', topnode, color, pc=1, oc=0)
    wristEnd = templateTools.createJoint(prefix + 'wristEnd', topnode, color, pc=1, oc=1)
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
    wristHelper = []
    wristHelperA = []
    wristHelperAEnd = []
    wristHelperB = []
    wristHelperBEnd = []
    wristHelperC = []
    wristHelperCEnd = []
    wristHelperD = []
    wristHelperDEnd = []

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

        # wrist help joints
        wristHelper = templateTools.createJoint(prefix + 'wristHelper', topnode, doubleColor, pc=1, oc=0)
        wristHelperA = templateTools.createJoint(prefix + 'wristHelperA', topnode, doubleColor, pc=1, oc=0)
        wristHelperAEnd = templateTools.createJoint(prefix + 'wristHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        wristHelperB = templateTools.createJoint(prefix + 'wristHelperB', topnode, doubleColor, pc=1, oc=0)
        wristHelperBEnd = templateTools.createJoint(prefix + 'wristHelperBEnd', topnode, doubleColor, pc=1, oc=0)
        wristHelperC = templateTools.createJoint(prefix + 'wristHelperC', topnode, doubleColor, pc=1, oc=0)
        wristHelperCEnd = templateTools.createJoint(prefix + 'wristHelperCEnd', topnode, doubleColor, pc=1, oc=0)
        wristHelperD = templateTools.createJoint(prefix + 'wristHelperD', topnode, doubleColor, pc=1, oc=0)
        wristHelperDEnd = templateTools.createJoint(prefix + 'wristHelperEnd', topnode, doubleColor, pc=1, oc=0)

    # Set template controls orignal position.
    mc.xform(shoulder[0], ws=1, t=[mirror, 0, 0])
    mc.xform(shoulderEnd[0], ws=1, t=[mirror * 3.5, 0, 0])
    mc.xform(upArm[0], ws=1, t=[mirror * 3.5, 0, 0])
    mc.xform(loArm[0], ws=1, t=[mirror * 7.5, 0, -0.05])
    mc.xform(wrist[0], ws=1, t=[mirror * 11, 0, 0])
    mc.xform(wristEnd[0], ws=1, t=[mirror * 12, 0, 0])

    # Auto fix joints axis.
    mc.delete(
        mc.aimConstraint(wristEnd[0], wrist[0], aim=[mirror, 0, 0], u=[0, 0, mirror], wut='object', wuo=shoulder[0]))
    mc.delete(mc.orientConstraint(wrist[0], wristEnd[0], mo=0))
    mc.pointConstraint(upArm[-2], shoulderEnd[0], n=shoulderEnd[0] + '_pc')
    mc.aimConstraint(upArm[-2], shoulder[-1], n=shoulder[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror],
                     wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.aimConstraint(upArm[-2], shoulder[-1], n=shoulder[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror],
                     wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.aimConstraint(loArm[-2], upArm[-1], n=upArm[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wut='object',
                     wuo=wrist[-2])
    mc.aimConstraint(wristEnd[-2], wrist[-1], n=wrist[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[1, 0, 0],
                     wut='objectRotation', wuo=wrist[-2])
    mc.aimConstraint(wrist[-2], loArm[-1], n=loArm[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wut='object',
                     wuo=upArm[-2])

    if doubleElbow:
        mc.pointConstraint(upArm[-2], loArmA[0], w=.05)
        mc.pointConstraint(loArm[-2], loArmA[0], w=.95)
        mc.pointConstraint(loArm[-2], loArmB[0], w=.95)
        mc.pointConstraint(wrist[-2], loArmB[0], w=.05)

        mc.pointConstraint(wrist[-2], loArmC[0])
        mc.orientConstraint(upArm[-1], loArmA[0])
        mc.orientConstraint(loArm[-1], loArmB[0], mo=1)

        mc.aimConstraint(loArmB[-2], loArmA[-1], n=loArmA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror],
                         wut='object', wuo=wrist[-2])
        mc.aimConstraint(wrist[-2], loArmB[-1], n=loArmB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror],
                         wut='object', wuo=upArm[-2])

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
        mc.setAttr(upArmHelperAEnd[-2] + '.tz', 0.5)
        mc.setAttr(upArmHelperBEnd[-2] + '.ty', 0.5)
        mc.setAttr(upArmHelperCEnd[-2] + '.tz', -0.5)
        mc.setAttr(upArmHelperDEnd[-2] + '.ty', -0.5)

        mc.aimConstraint(upArmHelperAEnd[-2], upArmHelperA[-1], n=upArmHelperA[-1] + '_ac', aim=[mirror, 0, 0],
                         u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperBEnd[-2], upArmHelperB[-1], n=upArmHelperB[-1] + '_ac', aim=[mirror, 0, 0],
                         u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperCEnd[-2], upArmHelperC[-1], n=upArmHelperC[-1] + '_ac', aim=[mirror, 0, 0],
                         u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upArmHelperDEnd[-2], upArmHelperD[-1], n=upArmHelperD[-1] + '_ac', aim=[mirror, 0, 0],
                         u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)

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
        mc.setAttr(loArmHelperAEnd[-2] + '.tz', 0.5)
        mc.setAttr(loArmHelperBEnd[-2] + '.tz', -0.5)

        # wrist help joint parent
        mc.parent(wristHelper[-1], wrist[-1])
        mc.parent(wristHelperA[-1], wristHelper[-1])
        mc.parent(wristHelperB[-1], wristHelper[-1])
        mc.parent(wristHelperC[-1], wristHelper[-1])
        mc.parent(wristHelperD[-1], wristHelper[-1])
        mc.parent(wristHelperAEnd[-1], wristHelperA[-1])
        mc.parent(wristHelperBEnd[-1], wristHelperB[-1])
        mc.parent(wristHelperCEnd[-1], wristHelperC[-1])
        mc.parent(wristHelperDEnd[-1], wristHelperD[-1])

        # wrist help control pose parent
        mc.parent(wristHelper[0], wrist[-2])
        mc.parent(wristHelperA[0], wristHelper[-2])
        mc.parent(wristHelperB[0], wristHelper[-2])
        mc.parent(wristHelperC[0], wristHelper[-2])
        mc.parent(wristHelperD[0], wristHelper[-2])
        mc.parent(wristHelperAEnd[0], wristHelperA[-2])
        mc.parent(wristHelperBEnd[0], wristHelperB[-2])
        mc.parent(wristHelperCEnd[0], wristHelperC[-2])
        mc.parent(wristHelperDEnd[0], wristHelperD[-2])

        mc.delete(mc.parentConstraint(wrist[-2], wristHelper[0]))
        mc.orientConstraint(wrist[-1], wristHelper[0], n=wristHelper[0] + '_oc')
        mc.setAttr(wristHelperAEnd[-2] + '.tz', 0.5)
        mc.setAttr(wristHelperBEnd[-2] + '.ty', 0.5)
        mc.setAttr(wristHelperCEnd[-2] + '.tz', -0.5)
        mc.setAttr(wristHelperDEnd[-2] + '.ty', -0.5)

        helpJointObjs = [upArmHelper, upArmHelperA, upArmHelperAEnd, upArmHelperB, upArmHelperBEnd, upArmHelperC,
                         upArmHelperCEnd, upArmHelperD, upArmHelperDEnd,
                         loArmHelper, loArmHelperA, loArmHelperAEnd, loArmHelperB, loArmHelperBEnd,
                         wristHelper, wristHelperA, wristHelperAEnd, wristHelperB, wristHelperBEnd, wristHelperC,
                         wristHelperCEnd, wristHelperD, wristHelperDEnd]
        for helpJointObj in helpJointObjs:
            mc.setAttr(helpJointObj[-2] + '.radius', 0.5)

    # Set joints original Hierarchy
    mc.parent(shoulderEnd[-1], shoulder[-1])
    mc.parent(upArm[-1], shoulderEnd[-1])
    mc.parent(loArm[-1], upArm[-1])
    mc.parent(wrist[-1], loArm[-1])
    mc.parent(wristEnd[-1], wrist[-1])

    # set tag ------------------------------------------------------------------------------------------
    needTagObjs = [shoulder, shoulderEnd, upArm, loArm, wrist, wristEnd]
    if doubleElbow:
        needTagObjs.extend([loArmA, loArmB, loArmC])
    if helpJoint:
        needTagObjs.extend(
            [upArmHelper, upArmHelperA, upArmHelperAEnd, upArmHelperB, upArmHelperBEnd, upArmHelperC, upArmHelperCEnd,
             upArmHelperD, upArmHelperDEnd,
             loArmHelper, loArmHelperA, loArmHelperAEnd, loArmHelperB, loArmHelperBEnd,
             wristHelper, wristHelperA, wristHelperAEnd, wristHelperB, wristHelperBEnd, wristHelperC, wristHelperCEnd,
             wristHelperD, wristHelperDEnd])
    for tagObj in needTagObjs:
        mc.setAttr(tagObj[-1] + '.tag', 'templateJoint tPose', type='string')

    # set doubleEblow math ------------------------------------------------------------------------------------------
    if doubleElbow:
        # > Get loArmB position use math expression.
        # ------------------------------------------------------------------------------------------------------------------
        mc.parent(loArmB[-1], loArmA[-1])
        mc.parent(loArmC[-1], loArmB[-1])

        # > loArmA / loArmB position help loc.
        # > loArmA / loArmB position weight attribute.
        mc.addAttr(loArm[-2], ln='doubleElbowWeight', at='float', k=1, min=0.1, max=9.9, dv=1)
        mc.addAttr(topnode, ln='doubleElbowWeight', at='float', k=1, uap=1, min=0.1, max=9.9, dv=1)
        mc.connectAttr(loArm[-2] + '.doubleElbowWeight', topnode + '.doubleElbowWeight')
        loArmAloc = aboutPublic.snapLoc(loArmA[-1], name=loArmA[-1] + '_loc')
        mc.parent(loArmAloc, loArmA[-2])
        mc.hide(loArmAloc)

        # > expression.
        arg = 'vector $posUpArm = `xform - q - ws - rp "{0}"`;'.format(upArm[-2]) + '\n'
        arg += 'vector $posLoArm = `xform - q - ws - rp "{0}"`;'.format(loArm[-2]) + '\n'
        arg += 'vector $posEndArm = `xform - q - ws - rp "{0}"`;'.format(wrist[-2]) + '\n'
        arg += 'vector $posLoArmA = << {0}.wpx, {0}.wpy, {0}.wpz >>;'.format(
            loArmAloc + 'Shape.worldPosition[0]') + '\n\n'

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

    # Create Rig Ctrls-----------------------------------------------------------------------------------------------------------------------

    # > limb set ctrl : ikfk switch / display / ....
    limbSetCtrl = controlTools.create(prefix + 'armSet_ctrl', shape='C01_cube', color=color, scale=0.4)
    mc.setAttr(limbSetCtrl[0] + '.sx', mirror)
    mc.parentConstraint(wristEnd[-1], limbSetCtrl[0], n=limbSetCtrl[0] + '_prc')

    # > should / pelvis ctrls
    shoulderFkCtrl = controlTools.create(prefix + 'armShoulderFk_ctrl', shape='semiCircle', color=color,
                                         scale=[3, 1.5, 1.5])
    mc.setAttr(shoulderFkCtrl[0] + '.sx', mirror)
    mc.pointConstraint(upArm[-1], shoulder[-1], shoulderFkCtrl[2], n=shoulderFkCtrl[2] + '_pc')
    mc.pointConstraint(shoulder[-1], shoulderFkCtrl[0], n=shoulderFkCtrl[0] + '_pc')
    # mc.orientConstraint(shoulder[-1], shoulderFkCtrl[0], n=shoulderFkCtrl[0] + '_oc', mo=1)

    shoulderIkCtrl = controlTools.create(prefix + 'armShoulderIk_ctrl', shape='C00_sphere', color=color, scale=1)
    mc.pointConstraint(upArm[-1], shoulderIkCtrl[2], n=shoulderIkCtrl[2] + '_pc')

    # > create Fk ctrls
    upArmCtrl = controlTools.create(prefix + 'upArmFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(upArmCtrl[-1], axis='z')
    mc.parentConstraint(upArm[-1], upArmCtrl[0], n=upArmCtrl[0] + '_prc')

    loArmCtrl = controlTools.create(prefix + 'loArmFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(loArmCtrl[-1], axis='z')
    mc.parentConstraint(loArm[-1], loArmCtrl[0], n=loArmCtrl[0] + '_prc')

    wristCtrl = controlTools.create(prefix + 'wristFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(wristCtrl[-1], axis='z')
    mc.parentConstraint(wrist[-1], wristCtrl[0], n=wristCtrl[0] + '_prc')

    # > create Ik ctrls
    armIkCtrl = controlTools.create(prefix + 'armIk_ctrl', shape='C00_sphere', color=color, scale=1.5, jointCtrl=True)
    mc.pointConstraint(wrist[-1], armIkCtrl[0], n=armIkCtrl[0] + '_pc')

    armIkLocalCtrl = controlTools.create(prefix + 'armIkLocal_ctrl', shape='D07_circle', color=color, scale=2,
                                         jointCtrl=True)
    controlTools.rollCtrlShape(armIkLocalCtrl[-1], axis='z')
    mc.parentConstraint(wrist[-1], armIkLocalCtrl[0], n=armIkLocalCtrl[0] + '_prc')

    elbowIkCtrl = controlTools.create(prefix + 'elbowIk_ctrl', shape='C00_sphere', color=color, scale=.4,
                                      jointCtrl=True)
    mc.pointConstraint(loArm[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_pc')
    mc.orientConstraint(upArm[-1], loArm[-1], elbowIkCtrl[0], n=elbowIkCtrl[0] + '_oc')
    mc.setAttr(elbowIkCtrl[2] + '.tz', -6 * mirror)

    # > Create pose Driver
    # ------------------------------------------------------------------------------------------------------------------
    if poseDriver:
        # create psd.
        armpsd = {}
        wristpsd = {}

        if mirror == 1:
            armpsd = poseDriverTool.createBridge(prefix + 'arm', axis='+x', mirror=False)
            wristpsd = poseDriverTool.createBridge(prefix + 'wrist', axis='+x', mirror=False)
        elif mirror == -1:
            armpsd = poseDriverTool.createBridge(prefix + 'arm', axis='+x', mirror=True)
            wristpsd = poseDriverTool.createBridge(prefix + 'wrist', axis='+x', mirror=True)

        # match temp size.
        # arm psd
        poseDriverTool.scaleBridge(prefix + 'arm', 0.05)
        poseDriverTool.constraintBridge(parentObj=upArm[-1], followObj=upArm[-1], parentHandle=armpsd['parent'],
                                        followHandle=armpsd['follow'])
        armfollow_ConstraintNode = mc.parentConstraint(armpsd['follow'], q=True)
        mc.delete(armfollow_ConstraintNode)

        # wrist psd
        poseDriverTool.scaleBridge(prefix + 'wrist', 0.05)
        poseDriverTool.constraintBridge(parentObj=wrist[-1], followObj=wrist[-1], parentHandle=wristpsd['parent'],
                                        followHandle=wristpsd['follow'])
        wristfollow_ConstraintNode = mc.parentConstraint(wristpsd['follow'], q=True)
        mc.delete(wristfollow_ConstraintNode)

        #clean
        mc.parent(armpsd['parent'], topnode + 'Ctrls')
        mc.parent(wristpsd['parent'], topnode + 'Ctrls')

    # > Template CLean Up
    # ------------------------------------------------------------------------------------------------------------------
    mc.parent(shoulder[0], shoulderEnd[0], upArm[0], loArm[0], wrist[0], topnode + 'Ctrls')
    if doubleElbow:
        mc.parent(loArmA[0], loArmB[0], loArmC[0], topnode + 'Ctrls')

    mc.parent(shoulderFkCtrl[0], shoulderIkCtrl[0], armIkCtrl[0], elbowIkCtrl[0], upArmCtrl[0], loArmCtrl[0],
              wristCtrl[0], armIkLocalCtrl[0], limbSetCtrl[0], topnode + 'Ctrls')
    mc.parent(wristEnd[0], wrist[-2])
    mc.hide(shoulderEnd[0])

    # > Lock & unLock.
    # ------------------------------------------------------------------------------------------------------------------
    # >> pos ctrls
    aboutLock.lock(shoulder + upArm + loArm + wrist + wristEnd + loArmA + loArmB + loArmC)
    aboutLock.unlock([shoulder[-2], upArm[-2], loArm[-2], wrist[-2]], 't ro')
    aboutLock.unlock(wrist[-2], 'r')
    aboutLock.unlock(wristEnd[-2], 'tx')

    if doubleElbow:
        aboutLock.unlock([loArmA[-2]], 'tx')
        aboutLock.unlock([loArmB[2]], 't ro s')
        aboutLock.unlock([loArm[-2]], 'doubleElbowWeight')

    # >> rig ctrls
    aboutLock.lock(
        shoulderFkCtrl + shoulderIkCtrl + upArmCtrl + loArmCtrl + wristCtrl + armIkCtrl + elbowIkCtrl + limbSetCtrl)
    aboutLock.unlock(limbSetCtrl[-1], 'tx')
    aboutLock.unlock(elbowIkCtrl[-1], 'tz')

    # > Create bendy template.
    if bendy:
        if doubleElbow:
            bendy2Limb.template(prefix + 'arm', topnode, [upArm[-1], loArmA[-1], loArmB[-1], wrist[-1]])
        else:
            bendy2Limb.template(prefix + 'arm', topnode, [upArm[-1], loArm[-1], wrist[-1]])

    # > TopNode Position
    mc.xform(topnode, ws=1, t=[0, 19, 0])
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))

    return


# Rig Build Anim-------------------------------------------------------------------------------------------------------------------------------------------------

def anim():
    parts = templateTools.getParts('bipedArm')
    for part in parts:

        # > get parts data
        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        twist = templateTools.getArgs(part, 'twist')
        stretch = templateTools.getArgs(part, 'stretch')
        doubleElbow = templateTools.getArgs(part, 'doubleElbow')
        bendy = templateTools.getArgs(part, 'bendy')
        volume = templateTools.getArgs(part, 'volume')
        autoShoulder = templateTools.getArgs(part, 'autoShoulder')
        poseDriver = templateTools.getArgs(part, 'poseDriver')
        prefix = templateTools.getPrefix(side, prefix)

        # > create jnts
        # ------------------------------------------------------------------------------------------------------------------
        # >> org jnts
        shoulder = prefix + 'shoulder_drv'
        shoulderEnd = prefix + 'shoulderEnd_drv'
        upArm = prefix + 'upArm_drv'
        loArm = prefix + 'loArm_drv'
        loArmA = prefix + 'loArmA_drv'
        loArmB = prefix + 'loArmB_drv'
        loArmC = prefix + 'loArmC_drv'
        wrist = prefix + 'wrist_drv'
        wristEnd = prefix + 'wristEnd_drv'
        print(shoulder)
        # >> drv jnts
        drvJnts = [upArm, loArm, wrist]

        # >> fk jnts
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

        # >> ik jnts
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

        # > Create controls
        # ------------------------------------------------------------------------------------------------------------------
        # >> positon help loc
        el = aboutPublic.snapLoc(prefix + 'elbowIk_ctrlPrep')
        sde = aboutPublic.snapLoc(shoulderEnd)
        ul = aboutPublic.snapLoc(upArm)
        wl = aboutPublic.snapLoc(wrist)

        mirror = 1
        if side == 'rt':
            mirror = -1

        # >> limb ctrl
        limbSetCtrl = controlTools.create(prefix + 'armSet_ctrl', snapTo=wristEnd, useShape=prefix + 'armSet_ctrlPrep')
        refDis = abs(mc.getAttr(wristEnd + '.tx'))
        mc.setAttr(limbSetCtrl[-1] + '.tx', 0.2 * refDis * mirror)
        mc.parentConstraint(wristEnd, limbSetCtrl[0], n=limbSetCtrl[0] + '_prc')

        # >> shoulder ctrl
        shoulderFkCtrl = controlTools.create(prefix + 'armShoulderFk_ctrl', snapTo=shoulder,
                                             useShape=prefix + 'armShoulderFk_ctrlPrep')
        shoulderIkCtrl = controlTools.create(prefix + 'armShoulderIk_ctrl', snapTo=sde,
                                             useShape=prefix + 'armShoulderIk_ctrlPrep')

        # >> ik ctrls
        armIkCtrl = controlTools.create(prefix + 'armIk_ctrl', snapTo=wl, useShape=prefix + 'armIk_ctrlPrep')
        armIkLocalCtrl = controlTools.create(prefix + 'armIkLocal_ctrl', snapTo=wrist,
                                             useShape=prefix + 'armIkLocal_ctrlPrep')
        elbowIkCtrl = controlTools.create(prefix + 'elbowIk_ctrl', snapTo=el, useShape=prefix + 'elbowIk_ctrlPrep')

        # >> fk switch to ik need create snap bridges
        armEndIkSnapCtrl = controlTools.create(prefix + 'armEndIk_snap_ctrl', snapTo=wl)
        elbowIkSnapCtrl = controlTools.create(prefix + 'elbowIkSnap_ctrl', snapTo=el)

        # >> reverse IKFK ctrl axis (need mirror axis)
        if side == 'rt':
            controlTools.reverseCtrl(shoulderFkCtrl[-1], prefix + 'armShoulderFk_ctrlPrep')
            controlTools.reverseCtrl(shoulderIkCtrl[-1], prefix + 'armShoulderIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(armIkCtrl[-1], prefix + 'armIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(elbowIkCtrl[-1], prefix + 'elbowIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(armEndIkSnapCtrl[-1], t=1)

        # >> fk ctrls
        upArmFkCtrl = controlTools.create(prefix + 'upArmFk_ctrl', snapTo=upArm, useShape=prefix + 'upArmFk_ctrlPrep')
        loArmFkCtrl = controlTools.create(prefix + 'loArmFk_ctrl', snapTo=loArm, useShape=prefix + 'loArmFk_ctrlPrep')
        wristFkCtrl = controlTools.create(prefix + 'wristFk_ctrl', snapTo=wrist, useShape=prefix + 'wristFk_ctrlPrep')

        mc.delete(el, sde, ul, wl)

        # >> set rotate order
        # ------------------------------------------------------------------------------------------------------------------
        nodes = [
            shoulder,
            upArm,
            loArm,
            loArmB,
            wrist,
            wristEnd,
            shoulderFkCtrl[-1],
            armIkCtrl[-1],
            upArmFkCtrl[-1],
            loArmFkCtrl[-1],
            wristFkCtrl[-1]]

        for j in nodes:
            if mc.objExists(j):
                mc.setAttr(j + '.ro', 1)

        # > Setup FK rig
        # ------------------------------------------------------------------------------------------------------------------
        mc.addAttr(upArmFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(loArmFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

        mc.parent(loArmFkCtrl[0], upArmFkCtrl[-1])
        mc.parent(wristFkCtrl[0], loArmFkCtrl[-1])

        mc.parentConstraint(upArmFkCtrl[-1], fkJnts[0], mo=0, n=upArmFkCtrl[-1] + '_prc')
        mc.parentConstraint(loArmFkCtrl[-1], fkJnts[1], mo=0, n=loArmFkCtrl[-1] + '_prc')
        mc.parentConstraint(wristFkCtrl[-1], fkJnts[-1], mo=0, n=wristFkCtrl[-1] + '_prc')
        mc.pointConstraint(shoulderEnd, upArmFkCtrl[0], n=upArmFkCtrl[0] + '_prc')

        # > Setup IK rig
        # ------------------------------------------------------------------------------------------------------------------
        ik = mc.ikHandle(sj=ikJnts[0], ee=ikJnts[-1], ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'arm_ikh')[0]
        mc.orientConstraint(armIkLocalCtrl[-1], ikJnts[-1], mo=0, n=armIkLocalCtrl[-1] + '_oc')

        # >> attr add
        mc.addAttr(armIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(armIkCtrl[-1], ln='local', at='enum', k=1, en='off:on')
        mc.addAttr(armIkCtrl[-1], ln='twist', at='double', k=1)
        mc.addAttr(elbowIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

        # >> local ctrl vis
        localCtrlShape = mc.listRelatives(armIkLocalCtrl[-1], s=1)[0]
        mc.connectAttr(armIkCtrl[-1] + '.local', localCtrlShape + '.visibility')
        mc.setAttr(armIkCtrl[-1] + '.local', k=0, cb=1)

        # >> Setup IK PV/twist
        elbowIkLineGrp = aboutCrv.createCrvBetween2Pos(name=elbowIkCtrl[-1] + '_crv', st=loArm, ed=elbowIkCtrl[-1])
        mc.setAttr(elbowIkLineGrp + '.inheritsTransform', 0)

        # >> Setup IK PV - offset/twist
        pvnodes = poleVectorTools.pvFollow(elbowIkCtrl[-1], ikJnts, armIkCtrl[-1], mirror)
        mc.poleVectorConstraint(elbowIkCtrl[-1], ik, n=ik + '_pvc')
        mc.pointConstraint(shoulderEnd, ikJnts[0], n=ikJnts[0] + '_pc')
        mc.connectAttr(armIkCtrl[-1] + '.twist', ik + '.twist')

        # > Setup Shoulder Rig
        # ------------------------------------------------------------------------------------------------------------------
        mc.parentConstraint(shoulderFkCtrl[-1], shoulder, n=shoulder + '_prc', mo=1)
        mc.pointConstraint(shoulderIkCtrl[-1], shoulderEnd, n=shoulderEnd + '_prc', mo=1)
        mc.parent(shoulderIkCtrl[0], shoulderFkCtrl[-1])
        autoShoulderGrp = ''

        # >> autoShoulder rig.
        if autoShoulder:

            # > create aim ik system
            aimOrgJnt = mc.duplicate(shoulder, po=True, n=shoulder.replace('_drv', '') + '_aimOrg')[0]
            aimStJnt = mc.duplicate(shoulder, po=True, n=shoulder.replace('_drv', '') + '_aimSt')[0]
            aimEdJnt = mc.duplicate(wrist, po=True, n=shoulder.replace('_drv', '') + '_aimEd')[0]
            mc.parent(aimStJnt, aimOrgJnt)
            mc.parent(aimEdJnt, aimStJnt)
            shoulderAimIk = mc.ikHandle(sj=aimStJnt, ee=aimEdJnt, ap=1, sol='ikSCsolver', n=prefix + 'shoulderAim_ik')[
                0]

            shoulderRollLoc = aboutPublic.snapLoc(aimOrgJnt, name=prefix + 'shoulderRoll_loc')
            shoulderRollLocGrp = \
            aboutPublic.fastGrp(shoulderRollLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]
            mc.delete(mc.orientConstraint(aimOrgJnt, shoulderRollLocGrp))

            shoulderAimLoc = aboutPublic.snapLoc(wrist, name=prefix + 'autoShoulderAim_loc')
            shoulderAimLocGrp = \
            aboutPublic.fastGrp(shoulderAimLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]

            if side == 'rt':
                controlTools.reverseCtrl(shoulderRollLoc)
                controlTools.reverseCtrl(shoulderAimLoc, t=1)

            # > Auto shoulder system connect
            autoShoulderGrp = mc.createNode('transform', n=prefix + 'autoShoulder_grp')
            mc.addAttr(shoulderFkCtrl[-1], ln='autoShoulder', at='double', k=1, max=10)

            mc.parent(shoulderAimIk, shoulderAimLoc)
            mc.parent(aimOrgJnt, shoulderRollLocGrp, shoulderAimLocGrp, autoShoulderGrp)

            autoShoulderOc = \
            mc.orientConstraint(aimOrgJnt, aimStJnt, shoulderRollLoc, n=shoulderRollLoc + '_oc', mo=True)[0]
            mc.setAttr(autoShoulderOc + '.interpType', 0)
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W0'.format(aimOrgJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder',
                                 dv=0, v=1, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W0'.format(aimOrgJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder',
                                 dv=10, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W1'.format(aimStJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder',
                                 dv=0, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoShoulderOc + '.{0}W1'.format(aimStJnt), cd=shoulderFkCtrl[-1] + '.autoShoulder',
                                 dv=10, v=1, itt='linear', ott='linear')

            mc.connectAttr(armIkCtrl[-1] + '.tx', shoulderAimLoc + '.tx')
            mc.connectAttr(armIkCtrl[-1] + '.ty', shoulderAimLoc + '.ty')
            mc.connectAttr(armIkCtrl[-1] + '.tz', shoulderAimLoc + '.tz')

            mc.connectAttr(shoulderRollLoc + '.rx', shoulderFkCtrl[2] + '.rx')
            mc.connectAttr(shoulderRollLoc + '.ry', shoulderFkCtrl[2] + '.ry')
            mc.connectAttr(shoulderRollLoc + '.rz', shoulderFkCtrl[2] + '.rz')

        # > Connect with torso / hand
        # ------------------------------------------------------------------------------------------------------------------
        connectInLoc = parent + '_connect_loc'
        if mc.objExists(connectInLoc):
            mc.parentConstraint(connectInLoc, shoulderFkCtrl[0], n=shoulderFkCtrl[0] + '_prc', mo=1)
            if autoShoulder:
                mc.parentConstraint(connectInLoc, autoShoulderGrp, n=autoShoulderGrp + '_prc', mo=1)
        else:
            connectInLoc = None

        connectOutLoc = prefix + 'wrist_connect_loc'
        if mc.objExists(connectOutLoc):
            mc.parentConstraint(prefix + 'wrist_drv', connectOutLoc, n=connectOutLoc + '_prc')

        # > Double Elbow
        # ------------------------------------------------------------------------------------------------------------------
        db_mpNode = '{0}mod'.format(prefix + 'armdb_')
        if doubleElbow:
            # >> db center pivot joint set
            db_root = mc.duplicate(loArm, po=1, n=prefix + 'db_root_drv')[0]
            db_pviot = mc.duplicate(loArm, po=1, n=prefix + 'db_pviot_drv')[0]
            mc.parentConstraint(upArm, db_root, n=db_root + '_prc', mo=1)
            mc.parent(db_pviot, db_root)
            mc.parent(loArmA, db_pviot)
            mc.pointConstraint(loArm, db_pviot)

            # >> db ikhandle set
            dbik = mc.ikHandle(sj=loArmA, ee=loArmC, ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'armdb_ikh')[0]

            # >> db ik control loc
            dbikloc = aboutPublic.snapLoc(wrist, name=prefix + 'armdb_ikloc')
            mc.pointConstraint(wrist, dbikloc, n=dbikloc + '_pc')
            mc.pointConstraint(dbikloc, dbik, n=dbik + '_pc')
            mc.orientConstraint(wrist, loArmC, n=loArmC + '_oc')

            # >> db pv control loc
            dbPvloc = aboutPublic.snapLoc(loArm, name=prefix + 'armdb_pvloc')
            mc.parentConstraint(loArm, dbPvloc, n=dbPvloc + '_pc')
            mc.poleVectorConstraint(dbPvloc, dbik, n=dbik + '_pvc')

            # >> db stretch
            disJnts = [loArm, wrist]
            stretch1Tools.stretchIk_db(prefix + 'armdb_', db_pviot, disJnts, loArmC, dbikloc, 'tx', mpNode=None)

            # >> clean db
            if not mc.objExists(db_mpNode):
                mc.createNode('transform', n=db_mpNode)
                mc.parent(db_mpNode, 'controls')

            db_needP = [dbik, dbikloc, dbPvloc, db_root]
            mc.parent(db_needP, db_mpNode)

            db_needVis = [dbik, dbikloc, dbPvloc]
            for need in db_needVis:
                mc.hide(need)

        # > Twist & Bendy
        # tips: the default joint num is 5 .
        # bridgeNum must be same with bendy joint number.
        # ------------------------------------------------------------------------------------------------------------------

        twistBridges = []
        bendyInfo = {}
        bendyUpRootJntGrp = []
        bendyLoRootJntGrp = []
        bendyJointList = []
        twistInfo = {}

        if twist:
            twistInfo = nonRoll.limbTwist(limbJnts=[[shoulder, upArm], [upArm, loArm, wrist]], twistAxis='x',
                                          mirror=mirror)
            twistBridges = twistInfo['vmd']

        if bendy:
            if doubleElbow:
                bendyInfo = bendy2Limb.anim(prefix + 'arm', [upArm, loArmA, loArmB, loArmC], twistBridges=twistBridges,
                                            volume=volume)
            else:
                bendyInfo = bendy2Limb.anim(prefix + 'arm', [upArm, loArm, wrist], twistBridges=twistBridges,
                                            volume=volume)

            bendyUpRootJnt = bendyInfo['upjnts'][0]
            bendyLoRootJnt = bendyInfo['lojnts'][0]
            bendyJointList = bendyInfo['jointList']

            bendyUpRootJntGrp = aboutPublic.createParentGrp(bendyUpRootJnt, 'grp')
            bendyLoRootJntGrp = aboutPublic.createParentGrp(bendyLoRootJnt, 'grp')

            mc.parentConstraint(shoulderEnd, bendyUpRootJntGrp, n=bendyUpRootJntGrp + '_prc', mo=True)
            mc.parentConstraint(upArm, bendyLoRootJntGrp, n=bendyLoRootJntGrp + '_prc', mo=True)

        # > Sticky & Soft & Stretch
        # >> ik
        # >> if stretch : stretch = stretch
        stretch2Info = stretch2Tools.stretchSoftIk(prefix + 'arm_', shoulderEnd, ikJnts, armIkCtrl[-1], elbowIkCtrl[-1],
                                                   stretch)
        blendloc = stretch2Info['blend']
        controlloc = stretch2Info['controlloc']
        mc.pointConstraint(armIkCtrl[-1], controlloc, n=controlloc + '_pc')
        mc.pointConstraint(blendloc, ik, n=ik + '_pc')

        # >> fk
        stretch2Tools.stretchFk(prefix + 'arm_', FkCtrls=[upArmFkCtrl[-1], loArmFkCtrl[-1]])

        # >> fk ik switch / display
        # >> switch
        mc.addAttr(limbSetCtrl[-1], ln='IKFK', at='double', dv=1, min=0, max=1, k=1)
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', ik + '.ikBlend')

        switchNode = mc.createNode('remapValue', n=prefix + 'armSwitchIKFK_rv')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', switchNode + '.inputValue')
        mc.setAttr(switchNode + '.outputMin', 1)
        mc.setAttr(switchNode + '.outputMax', 0)

        # >> switch constraint node weights
        jntNum = len(drvJnts)
        for i in range(jntNum):
            prc = mc.parentConstraint(ikJnts[i], fkJnts[i], drvJnts[i], n=drvJnts[i] + '_prc', mo=1)[0]
            mc.connectAttr(limbSetCtrl[-1] + '.IKFK', prc + '.' + ikJnts[i] + 'W0')
            mc.connectAttr(switchNode + '.outValue', prc + '.' + fkJnts[i] + 'W1')

        # >> display
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', armIkCtrl[0] + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', elbowIkLineGrp + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', elbowIkCtrl[0] + '.v')
        displayRv = mc.createNode('reverse', n=prefix + 'armIKFK_vis_rv')
        mc.connectAttr(armIkCtrl[0] + '.v', displayRv + '.ix')
        mc.connectAttr(displayRv + '.ox', upArmFkCtrl[0] + '.v')

        # > Pose Drivers
        # ------------------------------------------------------------------------------------------------------------------
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
            poseDriverTool.constraintBridge(parentObj=shoulder, followObj=upArm, parentHandle=armPsdParent,
                                            followHandle=armPsdFollow)

            # wrist psd
            wristPsdPrefix = prefix + 'wrist'
            wristPsdParent = wristPsdPrefix + '_psd_parent_handle'
            wristPsdFollow = wristPsdPrefix + '_psd_follow_handle'
            mc.parent(wristPsdParent, psdGrp)

            if bendy:
                poseDriverTool.constraintBridge(parentObj=bendyInfo['lojnts'][-1], followObj=wrist,
                                                parentHandle=wristPsdParent, followHandle=wristPsdFollow)
            else:
                if doubleElbow:
                    poseDriverTool.constraintBridge(parentObj=loArmB, followObj=wrist,
                                                    parentHandle=wristPsdParent, followHandle=wristPsdFollow)
                else:
                    poseDriverTool.constraintBridge(parentObj=loArm, followObj=wrist,
                                                    parentHandle=wristPsdParent, followHandle=wristPsdFollow)

        # > IK FK Snap
        # ------------------------------------------------------------------------------------------------------------------
        snapGrp = '{0}arm_snap_noTrans'.format(prefix)
        if not mc.objExists(snapGrp):
            mc.createNode('transform', n=snapGrp)
            mc.hide(snapGrp)

        mc.parent(armEndIkSnapCtrl[0], elbowIkSnapCtrl[0], snapGrp)

        mc.delete(elbowIkSnapCtrl[2])
        elbowIkSnap = mc.rename(elbowIkSnapCtrl[1], prefix + 'elbowIk_ctrl_snap')
        mc.setAttr(elbowIkSnap + '.ro', 1)
        mc.rename(elbowIkSnapCtrl[0], prefix + 'elbowIk_ctrl_snap_grp')
        mc.parentConstraint(drvJnts[1], elbowIkSnap, n=elbowIkSnap + '_prc', mo=1)

        mc.delete(armEndIkSnapCtrl[2])
        armEndIkSnap = mc.rename(armEndIkSnapCtrl[1], prefix + 'armIk_ctrl_snap')
        mc.setAttr(armEndIkSnap + '.ro', 1)
        mc.rename(armEndIkSnapCtrl[0], prefix + 'armIk_ctrl_snap_grp')
        mc.parentConstraint(drvJnts[2], armEndIkSnap, n=armEndIkSnap + '_prc', mo=1)

        # modify motion joints
        if bendy:
            if doubleElbow:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), loArmA.replace('_drv', ''))
                mc.parent(loArmA.replace('_drv', ''), bendyInfo['upjnts'][-2].replace('_drv', ''))
                mc.delete(bendyInfo['upjnts'][-1].replace('_drv', ''))
            else:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-2].replace('_drv', ''))
                mc.delete(bendyInfo['upjnts'][-1].replace('_drv', ''))

            mc.parent(bendyInfo['upjnts'][0].replace('_drv', ''), shoulder.replace('_drv', ''))
            mc.parent(wrist.replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))

            mc.delete(bendyInfo['lojnts'][-1].replace('_drv', ''))
            mc.delete(shoulderEnd.replace('_drv', ''))
            mc.delete(wristEnd.replace('_drv', ''))

            # db elbow
            if mc.objExists(loArmB.replace('_drv', '')):
                mc.delete(loArmB.replace('_drv', ''))

        # Clean Up
        # ------------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'arm_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # > Parent
        # ------------------------------------------------------------------------------------------------------------------

        # >> ctrls Parent
        mc.parent(armIkLocalCtrl[0], armIkCtrl[-1])
        ctrlNeedP = [elbowIkCtrl[0], pvnodes['root'], upArmFkCtrl[0], elbowIkLineGrp, armIkCtrl[0], limbSetCtrl[0],
                     shoulderFkCtrl[0], ik]
        if bendy:
            ctrlNeedP.append(bendyInfo['rootGrp'])
        if autoShoulder:
            ctrlNeedP.append(autoShoulderGrp)
        if doubleElbow:
            ctrlNeedP.append(db_mpNode)

        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # >> jnts Parent
        jntNeedP = [shoulder, ikJnts[0], fkJnts[0]]
        if bendy:
            jntNeedP.append(bendyUpRootJntGrp)
            jntNeedP.append(bendyLoRootJntGrp)

        for need in jntNeedP:
            mc.parent(need, mpNode)

        # >> noTrans Parent
        noTransNeedP = [snapGrp]
        if twist:
            noTransNeedP.append(twistInfo['noTrans'])
        if bendy:
            noTransNeedP.append(bendyInfo['noTrans'])
        if poseDriver:
            noTransNeedP.append(psdGrp)

        for need in noTransNeedP:
            mc.parent(need, 'noTransform')

        # > hide
        # ------------------------------------------------------------------------------------------------------------------

        needHList = [fkJnts[0], ikJnts[0], ik, connectInLoc]
        if autoShoulder:
            needHList.append(autoShoulderGrp)

        for need in needHList:
            mc.hide(need)

        # > keyable tag
        # ------------------------------------------------------------------------------------------------------------------
        # >> shoulder / pelvis
        controlTools.tagKeyable(shoulderFkCtrl[-2:], 't r')
        controlTools.tagKeyable(shoulderIkCtrl[-2:], 't')
        # >> ik ctrls
        controlTools.tagKeyable(armIkCtrl[-2:], 't r local twist stretch soft slide upLength loLength')
        controlTools.tagKeyable(armIkLocalCtrl[-2:], 'r')
        controlTools.tagKeyable(elbowIkCtrl[-2:], 't sticky')
        # >> fk ctrls
        controlTools.tagKeyable(upArmFkCtrl[-2:] + wristFkCtrl[-2:], 'r length')
        controlTools.tagKeyable(loArmFkCtrl[-2:], 'rz length')
        # >> setting ctrl
        controlTools.tagKeyable(limbSetCtrl[-2:], 'IKFK')

        # > follow tag
        # ------------------------------------------------------------------------------------------------------------------
        spaceTools.tag(upArmFkCtrl[-1],
                       'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(shoulderFkCtrl[-1], connectInLoc),
                       oo=True, dv=1)
        spaceTools.tag(armIkCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(connectInLoc), dv=2)
        spaceTools.tag(elbowIkCtrl[-1],
                       'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(pvnodes['space'], connectInLoc),
                       dv=0, con=elbowIkCtrl[-2])
        tagTools.tagIkFkSnap([upArmFkCtrl[-1], loArmFkCtrl[-1], wristFkCtrl[-1], armIkCtrl[-1], elbowIkCtrl[-1]],
                             prefix, 'bipedArm')

        if bendy:
            assetCommon.bindSet([shoulder] + bendyJointList + [wrist])
        else:
            assetCommon.bindSet([shoulder, upArm, loArm, loArmA, loArmB, wrist])
