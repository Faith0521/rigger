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
def template(side='lf', prefix='', parent='hip', doubleKnee=True, twist=True, bendy=True, stretch=True, volume=False, autoPelvis=True, addFoot=True, poseDriver=True, helpJoint=True):
    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['parent'] = parent
    args['doubleKnee'] = doubleKnee
    args['twist'] = twist
    args['bendy'] = bendy
    args['stretch'] = stretch
    args['volume'] = volume
    args['autoPelvis'] = autoPelvis
    args['addFoot'] = addFoot
    args['poseDriver'] = poseDriver
    args['helpJoint'] = helpJoint
    footprefix = prefix

    # Args to lock once part is built
    lockArgs = ['doubleKnee', 'addFoot', 'twist', 'stretch', 'bendy']

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
    pelvis = templateTools.createJoint(prefix + 'pelvis', topnode, color)
    pelvisEnd = templateTools.createJoint(prefix + 'pelvisEnd', topnode, color)
    upLeg = templateTools.createJoint(prefix + 'upLeg', topnode, color)
    loLeg = templateTools.createJoint(prefix + 'loLeg', topnode, color)
    legEnd = templateTools.createJoint(prefix + 'legEnd', topnode, color)
    legToe = templateTools.createJoint(prefix + 'legToe', topnode, color)
    loLegA = []
    loLegB = []
    loLegC = []
    upLegHelper = []
    upLegHelperA = []
    upLegHelperAEnd = []
    upLegHelperB = []
    upLegHelperBEnd = []
    upLegHelperC = []
    upLegHelperCEnd = []
    upLegHelperD = []
    upLegHelperDEnd = []
    loLegHelper = []
    loLegHelperA = []
    loLegHelperAEnd = []
    loLegHelperB = []
    loLegHelperBEnd = []
    legEndHelper = []
    legEndHelperA = []
    legEndHelperAEnd = []
    legEndHelperB = []
    legEndHelperBEnd = []
    legEndHelperC = []
    legEndHelperCEnd = []
    legEndHelperD = []
    legEndHelperDEnd = []

    if doubleKnee:
        loLegA = templateTools.createJoint(prefix + 'loLegA', topnode, doubleColor, pc=1, oc=0)
        loLegB = templateTools.createJoint(prefix + 'loLegB', topnode, doubleColor, pc=1, oc=0)
        loLegC = templateTools.createJoint(prefix + 'loLegC', topnode, doubleColor, pc=1, oc=0)
        mc.hide(loLegC[0])

    if helpJoint:
        # upLeg help joints
        upLegHelper = templateTools.createJoint(prefix + 'upLegHelper', topnode, doubleColor, pc=1, oc=0)
        upLegHelperA = templateTools.createJoint(prefix + 'upLegHelperA', topnode, doubleColor, pc=1, oc=0)
        upLegHelperAEnd = templateTools.createJoint(prefix + 'upLegHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        upLegHelperB = templateTools.createJoint(prefix + 'upLegHelperB', topnode, doubleColor, pc=1, oc=0)
        upLegHelperBEnd = templateTools.createJoint(prefix + 'upLegHelperBEnd', topnode, color, pc=1, oc=0)
        upLegHelperC = templateTools.createJoint(prefix + 'upLegHelperC', topnode, doubleColor, pc=1, oc=0)
        upLegHelperCEnd = templateTools.createJoint(prefix + 'upLegHelperCEnd', topnode, doubleColor, pc=1, oc=0)
        upLegHelperD = templateTools.createJoint(prefix + 'upLegHelperD', topnode, doubleColor, pc=1, oc=0)
        upLegHelperDEnd = templateTools.createJoint(prefix + 'upLegHelperDEnd', topnode, doubleColor, pc=1, oc=0)

        # loLeg help joints
        loLegHelper = templateTools.createJoint(prefix + 'loLegHelper', topnode, doubleColor, pc=1, oc=0)
        loLegHelperA = templateTools.createJoint(prefix + 'loLegHelperA', topnode, doubleColor, pc=1, oc=0)
        loLegHelperAEnd = templateTools.createJoint(prefix + 'loLegHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        loLegHelperB = templateTools.createJoint(prefix + 'loLegHelperB', topnode, doubleColor, pc=1, oc=0)
        loLegHelperBEnd = templateTools.createJoint(prefix + 'loLegHelperBEnd', topnode, doubleColor, pc=1, oc=0)

        # wrist help joints
        legEndHelper = templateTools.createJoint(prefix + 'legEndHelper', topnode, doubleColor, pc=1, oc=0)
        legEndHelperA = templateTools.createJoint(prefix + 'legEndHelperA', topnode, doubleColor, pc=1, oc=0)
        legEndHelperAEnd = templateTools.createJoint(prefix + 'legEndHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        legEndHelperB = templateTools.createJoint(prefix + 'legEndHelperB', topnode, doubleColor, pc=1, oc=0)
        legEndHelperBEnd = templateTools.createJoint(prefix + 'legEndHelperBEnd', topnode, doubleColor, pc=1, oc=0)
        legEndHelperC = templateTools.createJoint(prefix + 'legEndHelperC', topnode, doubleColor, pc=1, oc=0)
        legEndHelperCEnd = templateTools.createJoint(prefix + 'legEndHelperCEnd', topnode, doubleColor, pc=1, oc=0)
        legEndHelperD = templateTools.createJoint(prefix + 'legEndHelperD', topnode, doubleColor, pc=1, oc=0)
        legEndHelperDEnd = templateTools.createJoint(prefix + 'legEndHelperEnd', topnode, doubleColor, pc=1, oc=0)

    # set template pose
    mc.xform(pelvis[0], ws=1, t=[mirror * 3.2, 0, 0])
    mc.xform(pelvisEnd[0], ws=1, t=[mirror * 3.2, -3, 0])
    mc.xform(upLeg[0], ws=1, t=[mirror * 3.2, -3, 0])
    mc.xform(loLeg[0], ws=1, t=[mirror * 3.2, -11, 0.1])
    mc.xform(legEnd[0], ws=1, t=[mirror * 3.2, -18, -0.5])
    mc.xform(legToe[0], ws=1, t=[mirror * 3.2, -19, -0.5])

    # orient joints
    mc.pointConstraint(upLeg[-2], pelvisEnd[0], n=pelvisEnd[0] + '_pc')
    mc.aimConstraint(upLeg[-2], pelvis[-1], n=pelvis[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.aimConstraint(loLeg[-2], upLeg[-1], n=upLeg[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=legEnd[-2])
    mc.aimConstraint(legToe[-2], legEnd[-1], n=legEnd[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='object', wuo=legEnd[-2])
    mc.aimConstraint(legEnd[-2], loLeg[-1], n=loLeg[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=upLeg[-2])

    if doubleKnee:
        mc.pointConstraint(upLeg[-2], loLegA[0], w=.05)
        mc.pointConstraint(loLeg[-2], loLegA[0], w=.95)
        mc.pointConstraint(loLeg[-2], loLegB[0], w=.95)
        mc.pointConstraint(legEnd[-2], loLegB[0], w=.05)

        mc.pointConstraint(legEnd[-2], loLegC[0])
        mc.orientConstraint(upLeg[-1], loLegA[0])
        mc.orientConstraint(loLeg[-1], loLegB[0], mo=1)

        mc.aimConstraint(loLegB[-2], loLegA[-1], n=loLegA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=legEnd[-2])
        mc.aimConstraint(legEnd[-2], loLegB[-1], n=loLegB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, -mirror, 0], wut='object', wuo=upLeg[-2])

    if helpJoint:
        # up arm helper joint parent
        mc.parent(upLegHelper[-1], upLeg[-1])
        mc.parent(upLegHelperA[-1], upLegHelper[-1])
        mc.parent(upLegHelperB[-1], upLegHelper[-1])
        mc.parent(upLegHelperC[-1], upLegHelper[-1])
        mc.parent(upLegHelperD[-1], upLegHelper[-1])
        mc.parent(upLegHelperAEnd[-1], upLegHelperA[-1])
        mc.parent(upLegHelperBEnd[-1], upLegHelperB[-1])
        mc.parent(upLegHelperCEnd[-1], upLegHelperC[-1])
        mc.parent(upLegHelperDEnd[-1], upLegHelperD[-1])

        # up arm helper control pos parent
        mc.parent(upLegHelper[0], upLeg[-2])
        mc.parent(upLegHelperA[0], upLegHelper[-2])
        mc.parent(upLegHelperB[0], upLegHelper[-2])
        mc.parent(upLegHelperC[0], upLegHelper[-2])
        mc.parent(upLegHelperD[0], upLegHelper[-2])
        mc.parent(upLegHelperAEnd[0], upLegHelperA[-2])
        mc.parent(upLegHelperBEnd[0], upLegHelperB[-2])
        mc.parent(upLegHelperCEnd[0], upLegHelperC[-2])
        mc.parent(upLegHelperDEnd[0], upLegHelperD[-2])

        mc.delete(mc.parentConstraint(upLeg[-2], upLegHelper[0]))
        mc.orientConstraint(upLeg[-1], upLegHelper[0], n=upLegHelper[0] + '_oc')
        mc.setAttr(upLegHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(upLegHelperBEnd[-2] + '.tz', 0.5)
        mc.setAttr(upLegHelperCEnd[-2] + '.ty', -0.5)
        mc.setAttr(upLegHelperDEnd[-2] + '.tz', -0.5)

        mc.aimConstraint(upLegHelperAEnd[-2], upLegHelperA[-1], n=upLegHelperA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upLegHelperBEnd[-2], upLegHelperB[-1], n=upLegHelperB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upLegHelperCEnd[-2], upLegHelperC[-1], n=upLegHelperC[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
        mc.aimConstraint(upLegHelperDEnd[-2], upLegHelperD[-1], n=upLegHelperD[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)

        # loLeg help joint parent
        mc.parent(loLegHelper[-1], loLeg[-1])
        mc.parent(loLegHelperA[-1], loLegHelper[-1])
        mc.parent(loLegHelperB[-1], loLegHelper[-1])
        mc.parent(loLegHelperAEnd[-1], loLegHelperA[-1])
        mc.parent(loLegHelperBEnd[-1], loLegHelperB[-1])

        # loLeg help control pos parent
        mc.parent(loLegHelper[0], loLeg[-2])
        mc.parent(loLegHelperA[0], loLegHelper[-2])
        mc.parent(loLegHelperB[0], loLegHelper[-2])
        mc.parent(loLegHelperAEnd[0], loLegHelperA[-2])
        mc.parent(loLegHelperBEnd[0], loLegHelperB[-2])

        mc.delete(mc.parentConstraint(loLeg[-2], loLegHelper[0]))
        mc.orientConstraint(loLeg[-1], loLegHelper[0], n=loLegHelper[0] + '_oc')
        mc.setAttr(loLegHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(loLegHelperBEnd[-2] + '.ty', -0.5)

        # ankle help joint parent
        mc.parent(legEndHelper[-1], legEnd[-1])
        mc.parent(legEndHelperA[-1], legEndHelper[-1])
        mc.parent(legEndHelperB[-1], legEndHelper[-1])
        mc.parent(legEndHelperC[-1], legEndHelper[-1])
        mc.parent(legEndHelperD[-1], legEndHelper[-1])
        mc.parent(legEndHelperAEnd[-1], legEndHelperA[-1])
        mc.parent(legEndHelperBEnd[-1], legEndHelperB[-1])
        mc.parent(legEndHelperCEnd[-1], legEndHelperC[-1])
        mc.parent(legEndHelperDEnd[-1], legEndHelperD[-1])

        # legEnd help control pose parent
        mc.parent(legEndHelper[0], legEnd[-2])
        mc.parent(legEndHelperA[0], legEndHelper[-2])
        mc.parent(legEndHelperB[0], legEndHelper[-2])
        mc.parent(legEndHelperC[0], legEndHelper[-2])
        mc.parent(legEndHelperD[0], legEndHelper[-2])
        mc.parent(legEndHelperAEnd[0], legEndHelperA[-2])
        mc.parent(legEndHelperBEnd[0], legEndHelperB[-2])
        mc.parent(legEndHelperCEnd[0], legEndHelperC[-2])
        mc.parent(legEndHelperDEnd[0], legEndHelperD[-2])

        mc.delete(mc.parentConstraint(legEnd[-2], legEndHelper[0]))
        mc.orientConstraint(legEnd[-1], legEndHelper[0], n=legEndHelper[0] + '_oc')
        mc.setAttr(legEndHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(legEndHelperBEnd[-2] + '.tz', 0.5)
        mc.setAttr(legEndHelperCEnd[-2] + '.ty', -0.5)
        mc.setAttr(legEndHelperDEnd[-2] + '.tz', -0.5)

        helpJointObjs = [upLegHelper, upLegHelperA, upLegHelperAEnd, upLegHelperB, upLegHelperBEnd, upLegHelperC, upLegHelperCEnd, upLegHelperD, upLegHelperDEnd,
                        loLegHelper, loLegHelperA, loLegHelperAEnd, loLegHelperB, loLegHelperBEnd,
                        legEndHelper, legEndHelperA, legEndHelperAEnd, legEndHelperB, legEndHelperBEnd, legEndHelperC, legEndHelperCEnd, legEndHelperD, legEndHelperDEnd]
        for helpJointObj in helpJointObjs:
            mc.setAttr(helpJointObj[-2] + '.radius', 0.5)
            
    # Parent joints
    mc.parent(pelvisEnd[-1], pelvis[-1])
    mc.parent(upLeg[-1], pelvisEnd[-1])
    mc.parent(loLeg[-1], upLeg[-1])
    mc.parent(legEnd[-1], loLeg[-1])
    mc.parent(legToe[-1], legEnd[-1])

    # set tag ------------------------------------------------------------------------------------------
    needTagObjs = [pelvis, pelvisEnd, upLeg, loLeg, legEnd, legToe]
    if doubleKnee:
        needTagObjs.extend([loLegA, loLegB, loLegC])
    if helpJoint:
        needTagObjs.extend([upLegHelper, upLegHelperA, upLegHelperAEnd, upLegHelperB, upLegHelperBEnd, upLegHelperC, upLegHelperCEnd, upLegHelperD, upLegHelperDEnd,
                            loLegHelper, loLegHelperA, loLegHelperAEnd, loLegHelperB, loLegHelperBEnd,
                            legEndHelper, legEndHelperA, legEndHelperAEnd, legEndHelperB, legEndHelperBEnd, legEndHelperC, legEndHelperCEnd, legEndHelperD, legEndHelperDEnd])
    for tagObj in needTagObjs:
        mc.setAttr(tagObj[-1] + '.tag', 'templateJoint tPose', type='string')

    # set doubleKnee math ------------------------------------------------------------------------------------------
    if doubleKnee:
        mc.parent(loLegB[-1], loLegA[-1])
        mc.parent(loLegC[-1], loLegB[-1])

        # help position loc
        mc.addAttr(loLeg[-2], ln='doubleKneeWeight', at='float', k=1, min=0.1, max=9.9, dv=1)
        mc.addAttr(topnode, ln='doubleKneeWeight', at='float', k=1, uap=1, min=0.1, max=9.9, dv=1)
        mc.connectAttr(loLeg[-2]+'.doubleKneeWeight', topnode+'.doubleKneeWeight')
        loLegAloc = aboutPublic.snapLoc(loLegA[-1], name=loLegA[-1]+'_loc')
        mc.parent(loLegAloc, loLegA[-2])
        mc.hide(loLegAloc)

        arg = 'vector $posupLeg = `xform - q - ws - rp "{0}"`;'.format(upLeg[-2]) + '\n'
        arg += 'vector $posloLeg = `xform - q - ws - rp "{0}"`;'.format(loLeg[-2]) + '\n'
        arg += 'vector $posEndLeg = `xform - q - ws - rp "{0}"`;'.format(legEnd[-2]) + '\n'
        arg += 'vector $posloLegA = << {0}.wpx, {0}.wpy, {0}.wpz >>;'.format(loLegAloc+'Shape.worldPosition[0]') + '\n\n'

        arg += 'float $uplength = `mag($posloLeg - $posloLegA)`;' + '\n'
        arg += 'float $lolength = `mag($posEndLeg - $posloLeg)`;' + '\n'
        arg += 'float $sumLength = $uplength + $lolength;' + '\n'
        arg += 'float $weight = {0}.doubleKneeWeight * 0.1;'.format(loLeg[-2]) + '\n\n'

        arg += '$lenB = $weight * $sumLength;' + '\n'
        arg += '$lenA = $sumLength - $lenB;' + '\n'
        arg += '$lenC = `mag($posEndLeg - $posloLegA)`;' + '\n\n'

        arg += '$angle = acos( (pow($lenB, 2) + pow($lenC, 2) - pow($lenA, 2)) / (2 *$lenB * $lenC) );' + '\n'
        arg += 'vector $roVorg = $posEndLeg - $posloLegA;' + '\n'
        arg += 'vector $roVnew = unit($roVorg) * $lenB;' + '\n'
        arg += 'vector $axis = cross(($posupLeg - $posloLeg), ($posEndLeg - $posloLeg));' + '\n'
        arg += 'vector $unitTransform = rot($roVnew, $axis, $angle) + $posloLegA;' + '\n'
        arg += 'float $trsX = $unitTransform.x;' + '\n'
        arg += 'float $trsY = $unitTransform.y;' + '\n'
        arg += 'float $trsZ = $unitTransform.z;' + '\n\n'
        arg += 'xform - ws - t $trsX $trsY $trsZ {0};'.format(loLegB[2]) + '\n'
        arg += '{0}.scaleX = {1}.scaleX;'.format(loLegB[2], loLegAloc)

        mc.expression(n=topnode + '_exp', s=arg)
        
    # Create Ctrls-----------------------------------------------------------------------------------------------------------------------
    # should ctrls
    pelvisFkCtrl = controlTools.create(prefix + 'pelvisFk_ctrl', shape='semiCircle', color=color, scale=[3, 1.5, 1.5])
    mc.setAttr(pelvisFkCtrl[0] + '.sx', mirror)
    mc.pointConstraint(upLeg[-1], pelvis[-1], pelvisFkCtrl[1], n=pelvisFkCtrl[1] + '_pc')
    mc.pointConstraint(pelvis[-1], pelvisFkCtrl[0], n=pelvisFkCtrl[0] + '_pc')
    # mc.orientConstraint(pelvis[-1], pelvisFkCtrl[0], n=pelvisFkCtrl[0] + '_prc')

    pelvisIkCtrl = controlTools.create(prefix + 'pelvisIk_ctrl', shape='C00_sphere', color=color, scale=1)
    mc.setAttr(pelvisIkCtrl[0] + '.sx', mirror)
    mc.pointConstraint(upLeg[-1], pelvisIkCtrl[1], n=pelvisIkCtrl[1] + '_pc')


    # Fk Ctrls
    upLegFkCtrl = controlTools.create(prefix + 'upLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(upLegFkCtrl[-1], axis='z')
    mc.parentConstraint(upLeg[-1], upLegFkCtrl[0], n=upLegFkCtrl[0] + '_prc')

    loLegFkCtrl = controlTools.create(prefix + 'loLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(loLegFkCtrl[-1], axis='z')
    mc.parentConstraint(loLeg[-1], loLegFkCtrl[0], n=loLegFkCtrl[0] + '_prc')

    toeLegFkCtrl = controlTools.create(prefix + 'toeLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(toeLegFkCtrl[-1], axis='z')
    mc.parentConstraint(legEnd[-1], toeLegFkCtrl[0], n=toeLegFkCtrl[0] + '_prc')

    # IK Ctrls
    legIkCtrl = controlTools.create(prefix + 'legIk_ctrl', shape='C00_sphere', color=color, scale=1.5, jointCtrl=True)
    mc.pointConstraint(legEnd[-1], legIkCtrl[0], n=legIkCtrl[0] + '_pc')

    legIkLocalCtrl = controlTools.create(prefix + 'legIkLocal_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(legIkLocalCtrl[-1], axis='z')
    mc.parentConstraint(legEnd[-1], legIkLocalCtrl[0], n=legIkLocalCtrl[0] + '_prc')

    # >>Knee PV
    kneeIkCtrl = controlTools.create(prefix + 'kneeIk_ctrl', shape='C00_sphere', color=color, scale=0.4, jointCtrl=True)
    mc.pointConstraint(loLeg[-1], kneeIkCtrl[0], n=kneeIkCtrl[0] + '_pc')
    mc.orientConstraint(upLeg[-1], loLeg[-1], kneeIkCtrl[0], n=kneeIkCtrl[0] + '_oc', mo=1)
    mc.setAttr(kneeIkCtrl[2] + '.tz', 6 * mirror)

    # Set ctrl
    limbSetCtrl = controlTools.create(prefix + 'legSet_ctrl', shape='C01_cube', color=color, scale=0.4)
    mc.setAttr(limbSetCtrl[0] + '.sx', mirror)
    mc.pointConstraint(legEnd[-1], limbSetCtrl[0], n=limbSetCtrl[0] + '_pc')

    # >> PSD Driver Create
    if poseDriver:
        # create psd.
        legpsd = {}
        legEndpsd = {}

        if mirror == 1:
            legpsd = poseDriverTool.createBridge(prefix + 'leg', axis='-y', mirror=False)
            legEndpsd = poseDriverTool.createBridge(prefix + 'legEnd', axis='-y', mirror=False)
        elif mirror == -1:
            legpsd = poseDriverTool.createBridge(prefix + 'leg', axis='-y', mirror=True)
            legEndpsd = poseDriverTool.createBridge(prefix + 'legEnd', axis='-y', mirror=True)

        # match temp size.
        # arm psd
        poseDriverTool.scaleBridge(prefix + 'leg', 0.05)
        poseDriverTool.constraintBridge(parentObj=upLeg[-1], followObj=upLeg[-1], parentHandle=legpsd['parent'], followHandle=legpsd['follow'])
        legfollow_ConstraintNode = mc.parentConstraint(legpsd['follow'], q=True)
        mc.delete(legfollow_ConstraintNode)

        # legEnd psd
        poseDriverTool.scaleBridge(prefix + 'legEnd', 0.05)
        poseDriverTool.constraintBridge(parentObj=legEnd[-1], followObj=legEnd[-1], parentHandle=legEndpsd['parent'], followHandle=legEndpsd['follow'])
        legEndfollow_ConstraintNode = mc.parentConstraint(legEndpsd['follow'], q=True)
        mc.delete(legEndfollow_ConstraintNode)

        # clean
        mc.parent(legpsd['parent'], topnode + 'Ctrls')
        mc.parent(legEndpsd['parent'], topnode + 'Ctrls')

    # Cleanup
    mc.parent(pelvis[0], pelvisEnd[0], upLeg[0], loLeg[0], legEnd[0], topnode + 'Ctrls')
    if doubleKnee:
        mc.parent(loLegA[0], loLegB[0], loLegC[0], topnode + 'Ctrls')

    mc.parent(legIkCtrl[0], legIkLocalCtrl[0], kneeIkCtrl[0], upLegFkCtrl[0], loLegFkCtrl[0], toeLegFkCtrl[0], limbSetCtrl[0], pelvisFkCtrl[0], pelvisIkCtrl[0], topnode + 'Ctrls')
    mc.parent(legToe[0], legEnd[-2])
    mc.hide(legToe[-2])
    mc.hide(pelvisEnd[0])

    mc.setAttr(legToe[-1] + '.jointOrientX', 0)
    mc.setAttr(legToe[-1] + '.jointOrientY', 0)
    mc.setAttr(legToe[-1] + '.jointOrientZ', 0)

    # Lock
    aboutLock.lock(pelvis + upLeg + loLeg + legEnd + loLegA + loLegB + loLegC)
    aboutLock.unlock([pelvis[-2], upLeg[-2], loLeg[-2], legEnd[-2]], 't ro')
    aboutLock.unlock(legEnd[-2], 'r')

    if doubleKnee:
        aboutLock.unlock([ loLegA[-2] ], 'tx')
        aboutLock.unlock([ loLegB[2] ], 't ro s')
        aboutLock.unlock([ loLeg[-2] ], 'doubleKneeWeight')

    if bendy:
        if doubleKnee:
            bendy2Limb.template(prefix + 'leg', topnode, [upLeg[-1], loLegA[-1], loLegB[-1], legEnd[-1]])
        else:
            bendy2Limb.template(prefix + 'leg', topnode, [upLeg[-1], loLeg[-1], legEnd[-1]])

    aboutLock.lock(pelvisFkCtrl + pelvisIkCtrl + upLegFkCtrl + loLegFkCtrl + legIkCtrl + legIkLocalCtrl + kneeIkCtrl + limbSetCtrl)
    aboutLock.unlock([pelvisFkCtrl[-1], pelvisIkCtrl[-1], upLegFkCtrl[-1], loLegFkCtrl[-1], legIkCtrl[-1], legIkLocalCtrl[-1]], 't s')
    aboutLock.unlock(kneeIkCtrl[-1], 'ty tz s')

    # Positiion
    mc.xform(topnode, r=1, s=[1, 1, 1])
    mc.xform(topnode, ws=1, t=[0, 19, 0])
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))

    if addFoot:
        reload(footPart)
        footPart.template(info, side, footprefix, legEnd[-1], legIkCtrl[-1], loLegFkCtrl[-1])


# Build Anim
def anim():
    parts = templateTools.getParts('bipedLeg')
    for part in parts:

        side = templateTools.getArgs(part, 'side')
        prefix = templateTools.getArgs(part, 'prefix')
        parent = templateTools.getArgs(part, 'parent')
        doubleKnee = templateTools.getArgs(part, 'doubleKnee')
        twist = templateTools.getArgs(part, 'twist')
        bendy = templateTools.getArgs(part, 'bendy')
        stretch = templateTools.getArgs(part, 'stretch')
        volume = templateTools.getArgs(part, 'volume')
        autoPelvis = templateTools.getArgs(part, 'autoPelvis')
        addFoot = templateTools.getArgs(part, 'addFoot')
        poseDriver = templateTools.getArgs(part, 'poseDriver')

        footprefix = prefix
        prefix = templateTools.getPrefix(side, prefix)

        # declare jnts
        pelvis = prefix + 'pelvis_drv'
        pelvisEnd = prefix + 'pelvisEnd_drv'
        upLeg = prefix + 'upLeg_drv'
        loLeg = prefix + 'loLeg_drv'
        loLegA = prefix + 'loLegA_drv'
        loLegB = prefix + 'loLegB_drv'
        loLegC = prefix + 'loLegC_drv'
        legEnd = prefix + 'legEnd_drv'
        legToe = prefix + 'legToe_drv'

        # drv jnts
        drvJnts = [upLeg, loLeg, legEnd]

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
        el = aboutPublic.snapLoc(prefix + 'kneeIk_ctrlPrep')
        ul = aboutPublic.snapLoc(upLeg)
        wl = aboutPublic.snapLoc(legEnd)

        # mirror value
        mirror = 1
        if side == 'rt':
            mirror = -1

        # Create Ctrls-----------------------------------------------------------------------------------------------------------------------

        # > set up ankle / toeFk control axis
        #  >> create helpfull locator
        upAxisloc = aboutPublic.snapLoc(legEnd, prefix + 'ankle_up_loc')
        orgAxisloc = aboutPublic.snapLoc(legEnd, prefix + 'ankle_org_loc')
        aimAxisloc = aboutPublic.snapLoc(legEnd, prefix + 'ankle_axis_loc')
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

            # match fk leg original axis
            mc.setAttr(orgAxisloc + '_offset.rx', 90 * mirror)
            mc.setAttr(orgAxisloc + '_offset.rz', -90 * mirror)
        else:
            mc.group(orgAxisloc, n=orgAxisloc + '_grp')
            mc.delete(mc.orientConstraint(legEnd, orgAxisloc))

        # Seting ctrl
        limbSetCtrl = controlTools.create(prefix + 'legSet_ctrl', snapTo=wl, useShape=prefix + 'legSet_ctrlPrep')
        mc.delete(mc.orientConstraint(orgAxisloc, limbSetCtrl[0]))
        refDis = abs(mc.getAttr(legEnd + '.tx'))
        mc.setAttr(limbSetCtrl[-1] + '.ty', -0.2 * refDis * mirror)
        mc.parentConstraint(legEnd, limbSetCtrl[0], n=limbSetCtrl[0] + '_prc', mo=1)

        # Pelvis ctrls
        pelvisFkCtrl = controlTools.create(prefix + 'pelvisFk_ctrl', snapTo=pelvis, useShape=prefix + 'pelvisFk_ctrlPrep')
        pelvisIkCtrl = controlTools.create(prefix + 'pelvisIk_ctrl', snapTo=ul, useShape=prefix + 'pelvisIk_ctrlPrep')

        # IK ctrls
        legIkCtrl = controlTools.create(prefix + 'legIk_ctrl', snapTo=wl, useShape=prefix + 'legIk_ctrlPrep')
        legIkLocalCtrl = controlTools.create(prefix + 'legIkLocal_ctrl', snapTo=orgAxisloc, useShape=prefix + 'legIkLocal_ctrlPrep')
        kneeIkCtrl = controlTools.create(prefix + 'kneeIk_ctrl', snapTo=el, useShape=prefix + 'kneeIk_ctrlPrep')
        legEndIkSnapCtrl = controlTools.create(prefix + 'legEndIk_snap_ctrl', snapTo=wl)
        kneeIkSnapCtrl = controlTools.create(prefix + 'kneeIkSnap_ctrl', snapTo=el)


        if side == 'rt':
            controlTools.reverseCtrl(pelvisFkCtrl[-1], prefix + 'pelvisFk_ctrlPrep')
            controlTools.reverseCtrl(pelvisIkCtrl[-1], prefix + 'pelvisIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(legIkCtrl[-1], prefix + 'legIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(legEndIkSnapCtrl[-1], t=1)

        # FK ctrls
        upLegFkCtrl = controlTools.create(prefix + 'upLegFk_ctrl', snapTo=upLeg, useShape=prefix + 'upLegFk_ctrlPrep')
        loLegFkCtrl = controlTools.create(prefix + 'loLegFk_ctrl', snapTo=loLeg, useShape=prefix + 'loLegFk_ctrlPrep')
        toeLegFkCtrl = controlTools.create(prefix + 'toeLegFk_ctrl', snapTo=orgAxisloc, useShape=prefix + 'toeLegFk_ctrlPrep')
        legEndFkSnapCtrl = controlTools.create(prefix + 'legEndFk_snap_ctrl', snapTo=orgAxisloc)

        # set rotate orider
        nodes = [pelvis,
                 upLeg,
                 loLeg,
                 loLegB,
                 legEnd,
                 pelvisFkCtrl[-1],
                 legIkCtrl[-1],
                 legIkLocalCtrl[-1],
                 upLegFkCtrl[-1],
                 loLegFkCtrl[-1],
                 toeLegFkCtrl[-1]]

        for j in nodes:
            if mc.objExists(j):
                mc.setAttr(j + '.ro', 0)

        # Setup fk --------------------
        mc.addAttr(upLegFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(loLegFkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

        mc.parentConstraint(upLegFkCtrl[-1], fkJnts[0], mo=0, n=fkJnts[0] + '_prc')
        mc.parentConstraint(loLegFkCtrl[-1], fkJnts[1], mo=0, n=fkJnts[1] + '_prc')
        mc.parentConstraint(toeLegFkCtrl[-1], fkJnts[2], mo=0, n=fkJnts[2] + '_prc')
        mc.parent(loLegFkCtrl[0], upLegFkCtrl[-1])
        mc.parent(toeLegFkCtrl[0], loLegFkCtrl[-1])
        mc.parent(upLegFkCtrl[0], pelvisFkCtrl[-1])
        mc.pointConstraint(pelvisEnd, upLegFkCtrl[0], n=upLegFkCtrl[0] + '_pc')

        # Setup ik --------------------
        ik = mc.ikHandle(sj=ikJnts[0], ee=ikJnts[2], ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'leg_ikh')[0]
        mc.parent(ik, legIkCtrl[-1])
        mc.hide(ik)
        mc.orientConstraint(legIkLocalCtrl[-1], ikJnts[2], n=ikJnts[2] + '_oc', mo=1)

        # attr add
        mc.addAttr(legIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(kneeIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(legIkCtrl[-1], ln='local', at='enum', k=1, en='off:on')
        mc.addAttr(legIkCtrl[-1], ln='twist', at='double', k=1)
        controlTools.tagKeyable(legIkCtrl[-2:], 't r twist local soft stretch slide upLength loLength twist')

        # local ctrl vis
        localCtrlShape = mc.listRelatives(legIkLocalCtrl[-1], s=1)[0]
        mc.connectAttr(legIkCtrl[-1] + '.local', localCtrlShape + '.v')
        mc.setAttr(legIkCtrl[-1] + '.local', k=0, cb=1)

        # Setup IK PV/twist
        kneeIkLineGrp = aboutCrv.createCrvBetween2Pos(name=kneeIkCtrl[-1] + '_crv', st=loLeg, ed=kneeIkCtrl[-1])
        mc.setAttr(kneeIkLineGrp + '.inheritsTransform', 0)

        # -->> Setup IK PV - offset/twist
        pvnodes = poleVectorTools.pvFollow(kneeIkCtrl[-1], ikJnts, legIkCtrl[-1], mirror)
        mc.poleVectorConstraint(kneeIkCtrl[-1], ik, n=ik + '_pvc')
        mc.pointConstraint(pelvisEnd, ikJnts[0], n=ikJnts[0] + '_pc')
        mc.connectAttr(legIkCtrl[-1] + '.twist', ik + '.twist')

        # > Pelvis
        # ---------------------------------------------------------------------------------------------------------------
        mc.parentConstraint(pelvisFkCtrl[-1], pelvis, n=pelvis + '_prc', mo=1)
        mc.pointConstraint(pelvisIkCtrl[-1], pelvisEnd, n=pelvisEnd + '_pc', mo=1)
        mc.parent(pelvisIkCtrl[0], pelvisFkCtrl[-1])
        autoPelvisGrp = ''

        if autoPelvis:
            # create aim ik system
            aimOrgJnt = mc.duplicate(pelvis, po=True, n=pelvis.replace('_drv', '') + '_aimOrg')[0]
            aimStJnt = mc.duplicate(pelvis, po=True, n=pelvis.replace('_drv', '') + '_aimSt')[0]
            aimEdJnt = mc.duplicate(legEnd, po=True, n=pelvis.replace('_drv', '') + '_aimEd')[0]
            mc.parent(aimStJnt, aimOrgJnt)
            mc.parent(aimEdJnt, aimStJnt)
            pelvisAimIk = mc.ikHandle(sj=aimStJnt, ee=aimEdJnt, ap=1, sol='ikSCsolver', n=prefix + 'pelvisAim_ik')[0]

            pelvisRollLoc = aboutPublic.snapLoc(aimOrgJnt, name=prefix + 'pelvisRoll_loc')
            pelvisRollLocGrp = aboutPublic.fastGrp(pelvisRollLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]
            mc.delete(mc.orientConstraint(aimOrgJnt, pelvisRollLocGrp))

            pelvisAimLoc = aboutPublic.snapLoc(legEnd, name=prefix + 'autoPelvisAim_loc')
            pelvisAimLocGrp = aboutPublic.fastGrp(pelvisAimLoc, grpNameList=['grp', 'axis', 'con', 'sdk'], worldOrient=False)[0]

            if side == 'rt':
                controlTools.reverseCtrl(pelvisRollLoc)
                controlTools.reverseCtrl(pelvisAimLoc, t=1)

            # Auto pelvis system connect
            autoPelvisGrp = mc.createNode('transform', n=prefix + 'autoPelvis_grp')
            mc.addAttr(pelvisFkCtrl[-1], ln='autoPelvis', at='double', k=1, max=10)

            mc.parent(pelvisAimIk, pelvisAimLoc)
            mc.parent(aimOrgJnt, pelvisRollLocGrp, pelvisAimLocGrp, autoPelvisGrp)

            autoPelvisOc = mc.orientConstraint(aimOrgJnt, aimStJnt, pelvisRollLoc, n=pelvisRollLoc + '_oc', mo=True)[0]
            mc.setAttr(autoPelvisOc + '.interpType', 0)
            mc.setDrivenKeyframe(autoPelvisOc + '.{0}W0'.format(aimOrgJnt), cd=pelvisFkCtrl[-1] + '.autoPelvis', dv=0, v=1, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoPelvisOc + '.{0}W0'.format(aimOrgJnt), cd=pelvisFkCtrl[-1] + '.autoPelvis', dv=10, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoPelvisOc + '.{0}W1'.format(aimStJnt), cd=pelvisFkCtrl[-1] + '.autoPelvis', dv=0, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(autoPelvisOc + '.{0}W1'.format(aimStJnt), cd=pelvisFkCtrl[-1] + '.autoPelvis', dv=10, v=1, itt='linear', ott='linear')

            mc.connectAttr(legIkCtrl[-1] + '.tx', pelvisAimLoc + '.tx')
            mc.connectAttr(legIkCtrl[-1] + '.ty', pelvisAimLoc + '.ty')
            mc.connectAttr(legIkCtrl[-1] + '.tz', pelvisAimLoc + '.tz')

            mc.connectAttr(pelvisRollLoc + '.rx', pelvisFkCtrl[2] + '.rx')
            mc.connectAttr(pelvisRollLoc + '.ry', pelvisFkCtrl[2] + '.ry')
            mc.connectAttr(pelvisRollLoc + '.rz', pelvisFkCtrl[2] + '.rz')
            
        # connect with torso
        if mc.objExists(parent):
            connectLoc = parent + '_connect_loc'
            mc.parentConstraint(connectLoc, pelvisFkCtrl[0], n=pelvisFkCtrl[0] + '_prc', mo=1)
            if autoPelvis:
                mc.parentConstraint(connectLoc, autoPelvisGrp, n=autoPelvisGrp + '_prc', mo=1)
        else:
            connectLoc = None


        # > Double Knee -------------------------------
        db_mpNode = '{0}mod'.format(prefix + 'legdb_')
        if doubleKnee:
            # db center pivot joint set
            db_root = mc.duplicate(loLeg, po=1, n=prefix + 'db_root_drv')[0]
            db_pviot = mc.duplicate(loLeg, po=1, n=prefix + 'db_pviot_drv')[0]
            mc.parentConstraint(upLeg, db_root, n=db_root + '_prc', mo=1)
            mc.parent(db_pviot, db_root)
            mc.parent(loLegA, db_pviot)
            mc.pointConstraint(loLeg, db_pviot)

            # db ikhandle set
            dbik = mc.ikHandle(sj=loLegA, ee=loLegC, ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'legdb_ikh')[0]

            # db ik control loc
            dbikloc = aboutPublic.snapLoc(legEnd, name=prefix + 'legdb_ikloc')
            mc.pointConstraint(legEnd, dbikloc, n=dbikloc + '_pc')
            mc.pointConstraint(dbikloc, dbik, n=dbik + '_pc')
            mc.orientConstraint(legEnd, loLegC, n=loLegC + '_oc')

            # db pv control loc
            dbPvloc = aboutPublic.snapLoc(loLeg, name=prefix + 'legdb_pvloc')
            mc.parentConstraint(loLeg, dbPvloc, n=dbPvloc + '_pc')
            mc.poleVectorConstraint(dbPvloc, dbik, n=dbik + '_pvc')


            # db stretch
            disJnts = [loLeg, legEnd]
            stretch1Tools.stretchIk_db(prefix + 'legdb_', db_pviot, disJnts, loLegC, dbikloc, 'tx', mpNode=None)

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
        # bridgeNum must be same with bendy joint numb
        #
        # er.

        twistBridges = []
        bendyInfo = {}
        bendyUpRootJntGrp = []
        bendyLoRootJntGrp = []
        bendyJointList = []
        twistInfo = {}

        if twist:
            twistInfo = nonRoll.limbTwist(limbJnts=[[pelvis, upLeg], [upLeg, loLeg, legEnd]], twistAxis='x', mirror=mirror)
            twistBridges = twistInfo['vmd']

        if bendy:
            if doubleKnee:
                bendyInfo = bendy2Limb.anim(prefix + 'leg', [upLeg, loLegA, loLegB, loLegC], twistBridges=twistBridges, volume=volume)
            else:
                bendyInfo = bendy2Limb.anim(prefix + 'leg', [upLeg, loLeg, legEnd], twistBridges=twistBridges, volume=volume)

            bendyUpRootJnt = bendyInfo['upjnts'][0]
            bendyLoRootJnt = bendyInfo['lojnts'][0]
            bendyJointList = bendyInfo['jointList']

            bendyUpRootJntGrp = aboutPublic.createParentGrp(bendyUpRootJnt, 'grp')
            bendyLoRootJntGrp = aboutPublic.createParentGrp(bendyLoRootJnt, 'grp')

            mc.parentConstraint(pelvisEnd, bendyUpRootJntGrp, n=bendyUpRootJntGrp + '_prc', mo=True)
            mc.parentConstraint(upLeg, bendyLoRootJntGrp, n=bendyLoRootJntGrp + '_prc', mo=True)

        # fk ik switch / display
        # ---------------------------------------------------------------------------------------------------------------

        # switch
        mc.addAttr(limbSetCtrl[-1], ln='IKFK', at='double', dv=1, min=0, max=1, k=1)
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', ik + '.ikBlend')

        switchNode = mc.createNode('remapValue', n=prefix + 'legSwitchIKFK_rv')
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
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', legIkCtrl[0] + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', kneeIkLineGrp + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', kneeIkCtrl[0] + '.v')
        displayRv = mc.createNode('reverse', n=prefix + 'legIKFK_vis_rv')
        mc.connectAttr(legIkCtrl[0] + '.v', displayRv + '.ix')
        mc.connectAttr(displayRv + '.ox', upLegFkCtrl[0] + '.v')

        # --------------------------------------- Start: !!! Do not modify the running order !!!---------------------------------------------------------------------------
        # > Sticky & Soft & Stretch
        # ---------------------------------------------------------------------------------------------------------------
        # ik
        stretch2Info = stretch2Tools.stretchSoftIk(prefix + 'leg_', pelvisEnd, ikJnts, legIkCtrl[-1], kneeIkCtrl[-1], stretch)
        blendloc = stretch2Info['blend']
        controlloc = stretch2Info['controlloc']
        mc.pointConstraint(blendloc, ik)

        # Add Foot System
        # ---------------------------------------------------------------------------------------------------------------
        footInfo = {}
        if addFoot:
            footInfo = footPart.anim(side, footprefix, legEnd, legIkCtrl[-1], toeLegFkCtrl[-1], limbSetCtrl[-1])
            footjnts = [footInfo['ankle'], footInfo['ball']]
            assetCommon.bindSet(footjnts)
            mc.pointConstraint(footInfo['stretchRev'], controlloc, n=controlloc + '_pc')
        else:
            mc.pointConstraint(legIkCtrl[-1], controlloc, n=controlloc + '_pc')

        # fk
        stretch2Tools.stretchFk(prefix + 'leg_', FkCtrls=[upLegFkCtrl[-1], loLegFkCtrl[-1]])

        # --------------------------------------- End: !!! Do not modify the running order !!!---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------------------------------
        # Pose Drivers
        psdGrp = '{0}leg_psd_noTrans'.format(prefix)
        if poseDriver:
            if not mc.objExists(psdGrp):
                mc.createNode('transform', n=psdGrp)
                mc.hide(psdGrp)

            # arm psd
            legPsdPrep = prefix + 'leg'
            legPsdParent = legPsdPrep + '_psd_parent_handle'
            legPsdFollow = legPsdPrep + '_psd_follow_handle'
            mc.parent(legPsdParent,  psdGrp)
            poseDriverTool.constraintBridge(parentObj=pelvis, followObj=upLeg, parentHandle=legPsdParent, followHandle=legPsdFollow)

            # legEnd psd
            legEndPsdPrefix = prefix + 'legEnd'
            legEndPsdParent = legEndPsdPrefix + '_psd_parent_handle'
            legEndPsdFollow = legEndPsdPrefix + '_psd_follow_handle'
            mc.parent(legEndPsdParent, psdGrp)

            if bendy:
                poseDriverTool.constraintBridge(parentObj=bendyInfo['lojnts'][-1], followObj=legEnd,
                                                parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)
            else:
                if doubleKnee:
                    poseDriverTool.constraintBridge(parentObj=loLegB, followObj=legEnd,
                                                    parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)
                else:
                    poseDriverTool.constraintBridge(parentObj=loLeg, followObj=legEnd,
                                                    parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)

        # ---------------------------------------------------------------------------------------------------------------
        # IK FK Snap
        snapGrp = '{0}leg_snap_noTrans'.format(prefix)
        if not mc.objExists(snapGrp):
            mc.createNode('transform', n=snapGrp)
            mc.hide(snapGrp)

        mc.parent(legEndIkSnapCtrl[0], legEndFkSnapCtrl[0], kneeIkSnapCtrl[0], snapGrp)

        mc.delete(kneeIkSnapCtrl[2])
        kneeIkSnap = mc.rename(kneeIkSnapCtrl[1], prefix + 'kneeIk_ctrl_snap')
        mc.setAttr(kneeIkSnap + '.ro', 0)
        mc.rename(kneeIkSnapCtrl[0], prefix + 'kneeIk_ctrl_snap_grp')
        mc.parentConstraint(drvJnts[1], kneeIkSnap, n=kneeIkSnap+'_prc', mo=1)

        snapEnd = drvJnts[2]
        if addFoot:
            snapEnd = footInfo['ankle']
            mc.setAttr(snapEnd + '.ro', 0)

        mc.delete(legEndFkSnapCtrl[2])
        legEndFkSnap = mc.rename(legEndFkSnapCtrl[1], prefix + 'toeLegFk_ctrl_snap')
        mc.setAttr(legEndFkSnap + '.ro', 0)
        mc.rename(legEndFkSnapCtrl[0], prefix + 'toeLegFk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, legEndFkSnap, n=legEndFkSnap+'_prc', mo=1)

        mc.delete(legEndIkSnapCtrl[2])
        legEndIkSnap = mc.rename(legEndIkSnapCtrl[1], prefix + 'legIk_ctrl_snap')
        mc.setAttr(legEndIkSnap + '.ro', 0)
        mc.rename(legEndIkSnapCtrl[0], prefix + 'legIk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, legEndIkSnap, n=legEndIkSnap + '_prc', mo=1)


        # modify motion joints
        if bendy:
            if doubleKnee:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-1].replace('_drv', ''))
                mc.delete(loLegB.replace('_drv', ''))
            else:
                mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-2].replace('_drv', ''))
                mc.delete(bendyInfo['upjnts'][-1].replace('_drv', ''))

            if addFoot:
                mc.parent(footInfo['ankle'].replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))
                mc.delete(legEnd.replace('_drv', ''))
                mc.delete(footInfo['ballEnd'].replace('_drv', ''))
                mc.delete(footInfo['heel'].replace('_drv', ''))
            else:
                mc.parent(legEnd.replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))

            mc.parent(bendyInfo['upjnts'][0].replace('_drv', ''), pelvis.replace('_drv', ''))
            mc.delete(bendyInfo['lojnts'][-1].replace('_drv', ''))
            mc.delete(pelvisEnd.replace('_drv', ''))


        # CLEAN UP
        # ---------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'leg_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # parent
        # ctrls Parent
        mc.parent(legIkLocalCtrl[0], legIkCtrl[-1])

        ctrlNeedP = [kneeIkCtrl[0], pvnodes['root'], kneeIkLineGrp, legIkCtrl[0], limbSetCtrl[0], pelvisFkCtrl[0]]
        if bendy:
            ctrlNeedP.append(bendyInfo['rootGrp'])
        if autoPelvis:
            ctrlNeedP.append(autoPelvisGrp)
        if doubleKnee:
            ctrlNeedP.append(db_mpNode)
        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # jnts Parent
        jntNeedP = [pelvis, ikJnts[0], fkJnts[0]]
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
        if autoPelvis:
            needHList.append(autoPelvisGrp)
        for need in needHList:
            mc.hide(need)

        # delete
        mc.delete(orgAxisloc + '_grp', aimAxisloc, upAxisloc, el, ul, wl)

        # keyable tag
        # -----------------------------------------------------------------------------------------------
        # > pelvis
        controlTools.tagKeyable(pelvisFkCtrl[-2:], 't r')
        controlTools.tagKeyable(pelvisIkCtrl[-2:], 't')
        # > ik controls
        controlTools.tagKeyable(legIkCtrl[-2:], 't r local twist stretch soft slide upLength loLength')
        controlTools.tagKeyable(legIkLocalCtrl[-2:], 'r')
        controlTools.tagKeyable(kneeIkCtrl[-2:], 't sticky')
        # >fk controls
        controlTools.tagKeyable(upLegFkCtrl[-2:] + toeLegFkCtrl[-2:], 'r length')
        controlTools.tagKeyable(loLegFkCtrl[-2:], 'rz length')
        # >setting control
        controlTools.tagKeyable(limbSetCtrl[-2:], 'IKFK')

        spaceTools.tag(upLegFkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(pelvisFkCtrl[-1], connectLoc), oo=True, dv=1)
        spaceTools.tag(legIkCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls'.format(connectLoc), dv=2)
        spaceTools.tag(kneeIkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(pvnodes['space'], connectLoc), dv=0, con=kneeIkCtrl[-2])
        tagTools.tagIkFkSnap([upLegFkCtrl[-1], loLegFkCtrl[-1], toeLegFkCtrl[-1], legIkCtrl[-1], kneeIkCtrl[-1]], prefix, 'bipedLeg')

        if bendy:
            assetCommon.bindSet([pelvis] + bendyJointList)
        else:
            assetCommon.bindSet([pelvis, upLeg, loLeg, loLegB, legEnd])
