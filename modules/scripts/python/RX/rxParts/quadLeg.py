######################################
#   Rig Build Part
######################################
from importlib import reload

import maya.cmds as mc
import maya.api.OpenMaya as om
import math

import templateTools
import controlTools

from rxCore import aboutLock
from rxCore import aboutCrv
from rxCore import aboutPublic

import nonRoll
import bendy3Limb
import spaceTools

import tagTools
import stretch3Tools
import stretch2Tools
import stretch1Tools
import assetCommon
import poleVectorTools
import poseDriverTool
from rxParts import footPart

reload(bendy3Limb)
reload(nonRoll)
reload(footPart)

# Build Tempalte
def template(side='lf', prefix='bk', parent='hip', doubleKnee=True, twist=True, bendy=True, stretch=True, volume=False, autoPelvis=False, addFoot=True, poseDriver=True, helpJoint=True):
    # Arg values to be recorded
    args = {}
    args['side'] = side
    args['prefix'] = prefix
    args['doubleKnee'] = doubleKnee
    args['parent'] = parent
    args['twist'] = twist
    args['stretch'] = stretch
    args['bendy'] = bendy
    args['volume'] = volume
    args['autoPelvis'] = autoPelvis
    args['addFoot'] = addFoot
    args['poseDriver'] = poseDriver
    args['helpJoint'] = helpJoint

    # Args to lock once part is built
    lockArgs = ['doubleKnee', 'addFoot', 'twist', 'stretch', 'bendy']
    footprefix = prefix

    # Build template part topnode, get top node and prefix.
    info = templateTools.createTopNode('quadLeg', args, lockArgs)
    if not info:
        print ('QuadLeg Template Error... ')
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
    pelvis = templateTools.createJoint(prefix + 'pelvis', topnode, color, pc=1, oc=0)
    pelvisEnd = templateTools.createJoint(prefix + 'pelvisEnd', topnode, color)
    upLeg = templateTools.createJoint(prefix + 'upLeg', topnode, color, pc=1, oc=0)
    midLeg = templateTools.createJoint(prefix + 'midLeg', topnode, color, pc=1, oc=0)
    loLeg = templateTools.createJoint(prefix + 'loLeg', topnode, color, pc=1, oc=0)
    legEnd = templateTools.createJoint(prefix + 'legEnd', topnode, color, pc=1, oc=0)
    legToe = templateTools.createJoint(prefix + 'legToe', topnode, color, pc=1, oc=0)
    midLegA = []
    midLegB = []
    midLegC = []
    upLegHelper = []
    upLegHelperA = []
    upLegHelperAEnd = []
    upLegHelperB = []
    upLegHelperBEnd = []
    upLegHelperC = []
    upLegHelperCEnd = []
    upLegHelperD = []
    upLegHelperDEnd = []
    midLegHelper = []
    midLegHelperA = []
    midLegHelperAEnd = []
    midLegHelperB = []
    midLegHelperBEnd = []
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

    mc.setAttr(upLeg[-1] + '.tag', 'templateJoint tPose', type='string')
    mc.setAttr(midLeg[-1] + '.tag', 'templateJoint tPose', type='string')
    mc.setAttr(loLeg[-1] + '.tag', 'templateJoint tPose', type='string')
    mc.setAttr(legEnd[-1] + '.tag', 'templateJoint tPose', type='string')

    if doubleKnee:
        midLegA = templateTools.createJoint(prefix + 'midLegA', topnode, doubleColor, pc=1, oc=0)
        midLegB = templateTools.createJoint(prefix + 'midLegB', topnode, doubleColor, pc=1, oc=0)
        midLegC = templateTools.createJoint(prefix + 'midLegC', topnode, doubleColor, pc=1, oc=0)
        mc.setAttr(midLegA[-1] + '.tag', 'templateJoint tPose', type='string')
        mc.setAttr(midLegB[-1] + '.tag', 'templateJoint tPose', type='string')
        mc.setAttr(midLegC[-1] + '.tag', 'templateJoint tPose', type='string')
        mc.hide(midLegC[0])

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

        # midLeg help joints
        midLegHelper = templateTools.createJoint(prefix + 'midLegHelper', topnode, doubleColor, pc=1, oc=0)
        midLegHelperA = templateTools.createJoint(prefix + 'midLegHelperA', topnode, doubleColor, pc=1, oc=0)
        midLegHelperAEnd = templateTools.createJoint(prefix + 'midLegHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        midLegHelperB = templateTools.createJoint(prefix + 'midLegHelperB', topnode, doubleColor, pc=1, oc=0)
        midLegHelperBEnd = templateTools.createJoint(prefix + 'midLegHelperBEnd', topnode, doubleColor, pc=1, oc=0)
        
        # loLeg help joints
        loLegHelper = templateTools.createJoint(prefix + 'loLegHelper', topnode, doubleColor, pc=1, oc=0)
        loLegHelperA = templateTools.createJoint(prefix + 'loLegHelperA', topnode, doubleColor, pc=1, oc=0)
        loLegHelperAEnd = templateTools.createJoint(prefix + 'loLegHelperAEnd', topnode, doubleColor, pc=1, oc=0)
        loLegHelperB = templateTools.createJoint(prefix + 'loLegHelperB', topnode, doubleColor, pc=1, oc=0)
        loLegHelperBEnd = templateTools.createJoint(prefix + 'loLegHelperBEnd', topnode, doubleColor, pc=1, oc=0)

        # armEnd help joints
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
    mc.xform(midLeg[0], ws=1, t=[mirror * 3.2, -10, 1.5])
    mc.xform(loLeg[0], ws=1, t=[mirror * 3.2, -14, -2])
    mc.xform(legEnd[0], ws=1, t=[mirror * 3.2, -18, -1])
    mc.xform(legToe[0], ws=1, t=[mirror * 3.2, -19, -1])

    # orient joints
    mc.pointConstraint(upLeg[-2], pelvisEnd[0], n=pelvisEnd[0] + '_pc')
    aim = mc.createNode('transform', p=upLeg[-2], n=upLeg[-2] + 'Aim')
    mc.aimConstraint(legEnd[-2], aim, n=aim + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='object', wuo=midLeg[-2])

    mc.aimConstraint(upLeg[-2], pelvis[-1], n=pelvis[-1] + '_ac', aim=[mirror, 0, 0], u=[0, 0, mirror], wu=[0, 0, 1], wut='objectRotation', wuo=topnode)
    mc.aimConstraint(midLeg[-2], upLeg[-1], n=upLeg[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wu=[0, mirror, 0], wut='objectRotation', wuo=aim)
    mc.aimConstraint(loLeg[-2], midLeg[-1], n=midLeg[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wu=[0, mirror, 0], wut='objectRotation', wuo=aim)
    mc.aimConstraint(legEnd[-2], loLeg[-1], n=loLeg[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wu=[0, mirror, 0], wut='objectRotation', wuo=aim)
    mc.aimConstraint(legToe[-2], legEnd[-1], n=legEnd[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wut='object', wuo=legEnd[-2])

    if doubleKnee:
        mc.pointConstraint(upLeg[-2], midLegA[0], w=.05)
        mc.pointConstraint(midLeg[-2], midLegA[0], w=.95)
        mc.pointConstraint(midLeg[-2], midLegB[0], w=.95)
        mc.pointConstraint(loLeg[-2], midLegB[0], w=.05)

        mc.pointConstraint(loLeg[-2], midLegC[0])
        mc.orientConstraint(upLeg[-1], midLegA[0])
        mc.orientConstraint(midLeg[-1], midLegB[0], mo=1)

        mc.aimConstraint(midLegB[-2], midLegA[-1], n=midLegA[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wu=[0, mirror, 0], wut='objectRotation', wuo=aim)
        mc.aimConstraint(loLeg[-2], midLegB[-1], n=midLegB[-1] + '_ac', aim=[mirror, 0, 0], u=[0, mirror, 0], wu=[0, mirror, 0],  wut='objectRotation', wuo=aim)

    if helpJoint:
        # up leg helper joint parent
        mc.parent(upLegHelper[-1], upLeg[-1])
        mc.parent(upLegHelperA[-1], upLegHelper[-1])
        mc.parent(upLegHelperB[-1], upLegHelper[-1])
        mc.parent(upLegHelperC[-1], upLegHelper[-1])
        mc.parent(upLegHelperD[-1], upLegHelper[-1])
        mc.parent(upLegHelperAEnd[-1], upLegHelperA[-1])
        mc.parent(upLegHelperBEnd[-1], upLegHelperB[-1])
        mc.parent(upLegHelperCEnd[-1], upLegHelperC[-1])
        mc.parent(upLegHelperDEnd[-1], upLegHelperD[-1])

        # up leg helper control pos parent
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

        # midLeg help joint parent
        mc.parent(midLegHelper[-1], midLeg[-1])
        mc.parent(midLegHelperA[-1], midLegHelper[-1])
        mc.parent(midLegHelperB[-1], midLegHelper[-1])
        mc.parent(midLegHelperAEnd[-1], midLegHelperA[-1])
        mc.parent(midLegHelperBEnd[-1], midLegHelperB[-1])

        # midLeg help control pos parent
        mc.parent(midLegHelper[0], midLeg[-2])
        mc.parent(midLegHelperA[0], midLegHelper[-2])
        mc.parent(midLegHelperB[0], midLegHelper[-2])
        mc.parent(midLegHelperAEnd[0], midLegHelperA[-2])
        mc.parent(midLegHelperBEnd[0], midLegHelperB[-2])

        mc.delete(mc.parentConstraint(midLeg[-2], midLegHelper[0]))
        mc.orientConstraint(midLeg[-1], midLegHelper[0], n=midLegHelper[0] + '_oc')
        mc.setAttr(midLegHelperAEnd[-2] + '.ty', 0.5)
        mc.setAttr(midLegHelperBEnd[-2] + '.ty', -0.5)
        
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

        # legEnd help joint parent
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
    mc.parent(midLeg[-1], upLeg[-1])
    mc.parent(loLeg[-1], midLeg[-1])
    mc.parent(legEnd[-1], loLeg[-1])
    mc.parent(legToe[-1], legEnd[-1])
    
    # set tag ------------------------------------------------------------------------------------------
    needTagObjs = [pelvis, pelvisEnd, upLeg, loLeg, legEnd, legToe]
    if doubleKnee:
        needTagObjs.extend([midLegA, midLegB, midLegC])
    if helpJoint:
        needTagObjs.extend([upLegHelper, upLegHelperA, upLegHelperAEnd, upLegHelperB, upLegHelperBEnd, upLegHelperC, upLegHelperCEnd, upLegHelperD, upLegHelperDEnd,
                            loLegHelper, loLegHelperA, loLegHelperAEnd, loLegHelperB, loLegHelperBEnd,
                            legEndHelper, legEndHelperA, legEndHelperAEnd, legEndHelperB, legEndHelperBEnd, legEndHelperC, legEndHelperCEnd, legEndHelperD, legEndHelperDEnd])
    for tagObj in needTagObjs:
        mc.setAttr(tagObj[-1] + '.tag', 'templateJoint tPose', type='string')
        
    if doubleKnee:
        mc.parent(midLegB[-1], midLegA[-1])
        mc.parent(midLegC[-1], midLegB[-1])

        # help position loc
        mc.addAttr(midLeg[-2], ln='doubleKneeWeight', at='float', k=1, min=0.1, max=9.9, dv=1)
        mc.addAttr(topnode, ln='doubleKneeWeight', at='float', k=1, uap=1, min=0.1, max=9.9, dv=1)
        mc.connectAttr(midLeg[-2]+'.doubleKneeWeight', topnode+'.doubleKneeWeight')
        midLegAloc = aboutPublic.snapLoc(midLegA[-1], name=midLegA[-1]+'_loc')
        mc.parent(midLegAloc, midLegA[-2])
        mc.hide(midLegAloc)

        arg = 'vector $posupLeg = `xform - q - ws - rp "{0}"`;'.format(upLeg[-2]) + '\n'
        arg += 'vector $posmidLeg = `xform - q - ws - rp "{0}"`;'.format(midLeg[-2]) + '\n'
        arg += 'vector $posEndLeg = `xform - q - ws - rp "{0}"`;'.format(loLeg[-2]) + '\n'
        arg += 'vector $posmidLegA = << {0}.wpx, {0}.wpy, {0}.wpz >>;'.format(midLegAloc+'Shape.worldPosition[0]') + '\n\n'

        arg += 'float $uplength = `mag($posmidLeg - $posmidLegA)`;' + '\n'
        arg += 'float $lolength = `mag($posEndLeg - $posmidLeg)`;' + '\n'
        arg += 'float $sumLength = $uplength + $lolength;' + '\n'
        arg += 'float $weight = {0}.doubleKneeWeight * 0.1;'.format(midLeg[-2]) + '\n\n'

        arg += '$lenB = $weight * $sumLength;' + '\n'
        arg += '$lenA = $sumLength - $lenB;' + '\n'
        arg += '$lenC = `mag($posEndLeg - $posmidLegA)`;' + '\n\n'

        arg += '$angle = acos( (pow($lenB, 2) + pow($lenC, 2) - pow($lenA, 2)) / (2 *$lenB * $lenC) );' + '\n'
        arg += 'vector $roVorg = $posEndLeg - $posmidLegA;' + '\n'
        arg += 'vector $roVnew = unit($roVorg) * $lenB;' + '\n'
        arg += 'vector $axis = cross(($posupLeg - $posmidLeg), ($posEndLeg - $posmidLeg));' + '\n'
        arg += 'vector $unitTransform = rot($roVnew, $axis, $angle) + $posmidLegA;' + '\n'
        arg += 'float $trsX = $unitTransform.x;' + '\n'
        arg += 'float $trsY = $unitTransform.y;' + '\n'
        arg += 'float $trsZ = $unitTransform.z;' + '\n\n'
        arg += 'xform - ws - t $trsX $trsY $trsZ {0};'.format(midLegB[2]) + '\n'
        arg += '{0}.scaleX = {1}.scaleX;'.format(midLegB[2], midLegAloc)

        mc.expression(n=topnode + '_exp', s=arg)

    # Create Ctrls
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

    midLegFkCtrl = controlTools.create(prefix + 'midLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(midLegFkCtrl[-1], axis='z')
    mc.parentConstraint(midLeg[-1], midLegFkCtrl[0], n=midLegFkCtrl[0] + '_prc')

    loLegFkCtrl = controlTools.create(prefix + 'loLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(loLegFkCtrl[-1], axis='z')
    mc.parentConstraint(loLeg[-1], loLegFkCtrl[0], n=loLegFkCtrl[0] + '_prc')

    toeLegFkCtrl = controlTools.create(prefix + 'toeLegFk_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(toeLegFkCtrl[-1], axis='z')
    mc.parentConstraint(legEnd[-1], toeLegFkCtrl[0], n=toeLegFkCtrl[0] + '_prc')

    # Ik Leg
    legIkCtrl = controlTools.create(prefix + 'legIk_ctrl', shape='C00_sphere', color=color, scale=1, jointCtrl=True)
    mc.pointConstraint(legEnd[-1], legIkCtrl[0], n=legIkCtrl[0] + '_pc')

    legIkLocalCtrl = controlTools.create(prefix + 'legIkLocal_ctrl', shape='D07_circle', color=color, scale=2, jointCtrl=True)
    controlTools.rollCtrlShape(legIkLocalCtrl[-1], axis='z')
    mc.parentConstraint(legEnd[-1], legIkLocalCtrl[0], n=legIkLocalCtrl[0] + '_prc')

    kneeIkCtrl = controlTools.create(prefix + 'kneeIk_ctrl', shape='C00_sphere', color=color, scale=.5, jointCtrl=True)
    mc.pointConstraint(midLeg[-1], kneeIkCtrl[0], n=kneeIkCtrl[0] + '_pc')
    mc.orientConstraint(upLeg[-1], midLeg[-1], kneeIkCtrl[0], n=kneeIkCtrl[0] + '_oc', mo=1)
    mc.setAttr(kneeIkCtrl[0] + '.sx', mirror)
    mc.setAttr(kneeIkCtrl[2] + '.tz', 4 * mirror)

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
        # leg psd
        poseDriverTool.scaleBridge(prefix + 'leg', 0.05)
        poseDriverTool.constraintBridge(parentObj=upLeg[-1], followObj=upLeg[-1], parentHandle=legpsd['parent'], followHandle=legpsd['follow'])
        legfollow_ConstraintNode = mc.parentConstraint(legpsd['follow'], q=True)
        mc.delete(legfollow_ConstraintNode)

        # legEnd psd
        poseDriverTool.scaleBridge(prefix + 'legEnd', 0.05)
        poseDriverTool.constraintBridge(parentObj=legEnd[-1], followObj=legEnd[-1], parentHandle=legEndpsd['parent'], followHandle=legEndpsd['follow'])
        legEndfollow_ConstraintNode = mc.parentConstraint(legEndpsd['follow'], q=True)
        mc.delete(legEndfollow_ConstraintNode)

        # psd clean
        mc.parent(legpsd['parent'], topnode + 'Ctrls')
        mc.parent(legEndpsd['parent'], topnode + 'Ctrls')
        
    # ----------------------------------------------------------------------------------------------------------------
    # Rig Ending Cleanup
    mc.parent(pelvis[0], pelvisEnd[0], upLeg[0], midLeg[0], loLeg[0], legEnd[0], legToe[0], topnode + 'Ctrls')
    mc.parent(pelvisFkCtrl[0], pelvisIkCtrl[0], legIkCtrl[0], legIkLocalCtrl[0], kneeIkCtrl[0], upLegFkCtrl[0],
              midLegFkCtrl[0], loLegFkCtrl[0], toeLegFkCtrl[0], limbSetCtrl[0], topnode + 'Ctrls')
    mc.parentConstraint(aim, loLeg[0], n=loLeg[0] + '_prc', mo=1)

    if doubleKnee:
        mc.parent(midLegA[0], midLegB[0], midLegC[0], topnode + 'Ctrls')

    # > Lock & unLock.
    # ------------------------------------------------------------------------------------------------------------------
    # >> pos ctrls
    aboutLock.lock(pelvis + upLeg + midLeg + loLeg + legEnd + midLegA + midLegB + midLegC)
    aboutLock.unlock([pelvis[-2], midLeg[-2], upLeg[-2], legEnd[-2]], 't ro')
    aboutLock.unlock([loLeg[-2]], 'ty tz')

    if doubleKnee:
        aboutLock.unlock(midLegA[-2], 'tx')
        aboutLock.unlock(midLegB[2], 't ro s')
        aboutLock.unlock(midLeg[-2], 'doubleKneeWeight')

    # >> rig ctrls
    aboutLock.lock(pelvisFkCtrl + pelvisIkCtrl + upLegFkCtrl + loLegFkCtrl + midLegFkCtrl + legIkCtrl + legIkLocalCtrl + kneeIkCtrl)
    aboutLock.unlock([pelvisFkCtrl[-1], pelvisIkCtrl[-1], upLegFkCtrl[-1], loLegFkCtrl[-1], midLegFkCtrl[-1], legIkCtrl[-1], legIkLocalCtrl[-1]], 't r s ')
    aboutLock.unlock(kneeIkCtrl[-1], 'ty tz s')

    # > Create bendy template.
    # ------------------------------------------------------------------------------------------------------------------
    if bendy:
        if doubleKnee:
            bendy3Limb.template(prefix + 'qleg', topnode, [upLeg[-1], midLegA[-1], midLegB[-1], loLeg[-1], legEnd[-1]])
        else:
            bendy3Limb.template(prefix + 'qleg', topnode, [upLeg[-1], midLeg[-1], loLeg[-1], legEnd[-1]])


    # > parent
    mc.parent(legToe[0], legEnd[-2])
    mc.hide(legToe[-2])
    mc.hide(pelvisEnd[0])

    mc.setAttr(legToe[-1] + '.jointOrientX', 0)
    mc.setAttr(legToe[-1] + '.jointOrientY', 0)
    mc.setAttr(legToe[-1] + '.jointOrientZ', 0)

    # > TopNode Position
    mc.xform(topnode, r=1, s=[1, 1, 1])
    mc.xform(topnode, ws=1, t=[0, 19, 0])
    if mc.objExists(parent):
        mc.delete(mc.pointConstraint(parent, topnode))
    if addFoot:
        footPart.template(info, side, footprefix, legEnd[-1], legIkCtrl[-1], loLegFkCtrl[-1])


# Build Anim
def anim():
    # Code to get parts to build.
    parts = templateTools.getParts('quadLeg')
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
        midLeg = prefix + 'midLeg_drv'
        midLegA = prefix + 'midLegA_drv'
        midLegB = prefix + 'midLegB_drv'
        midLegC = prefix + 'midLegC_drv'
        loLeg = prefix + 'loLeg_drv'
        legEnd = prefix + 'legEnd_drv'

        # drv jnts
        drvJnts = [upLeg, midLeg, loLeg, legEnd]

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
        le = aboutPublic.snapLoc(legEnd)
        le2 = aboutPublic.snapLoc(legEnd)

        mirror = 1
        if side == 'rt':
            mirror = -1

        mc.xform(le2, r=1, t=[0, mirror, 0])
        mc.aimConstraint(le2, le, aim=[0, 1, 0], u=[1, 0, 0], wu=[1, 0, 0], wut='objectRotation', wuo=legEnd)

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

        # Create ctrls
        # >> setting ctrl
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

        # FK ctrls
        upLegFkCtrl = controlTools.create(prefix + 'upLegFk_ctrl', snapTo=upLeg, useShape=prefix + 'upLegFk_ctrlPrep')
        midLegFkCtrl = controlTools.create(prefix + 'midLegFk_ctrl', snapTo=midLeg, useShape=prefix + 'midLegFk_ctrlPrep')
        loLegFkCtrl = controlTools.create(prefix + 'loLegFk_ctrl', snapTo=loLeg, useShape=prefix + 'loLegFk_ctrlPrep')
        toeLegFkCtrl = controlTools.create(prefix + 'toeLegFk_ctrl', snapTo=orgAxisloc, useShape=prefix + 'toeLegFk_ctrlPrep')
        legEndFkSnapCtrl = controlTools.create(prefix + 'legEndFk_snap_ctrl', snapTo=orgAxisloc)

        if side == 'rt':
            controlTools.reverseCtrl(legIkCtrl[-1], prefix + 'legIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(legIkLocalCtrl[-1], prefix + 'legIkLocal_ctrlPrep', t=1)
            controlTools.reverseCtrl(pelvisIkCtrl[-1], prefix + 'pelvisIk_ctrlPrep', t=1)
            controlTools.reverseCtrl(pelvisFkCtrl[-1], prefix + 'pelvisFk_ctrlPrep')
            controlTools.reverseCtrl(legEndIkSnapCtrl[-1], t=1)
        else:
            mc.parent(pelvisFkCtrl[1], w=1)
            mc.xform(pelvisFkCtrl[0], ws=1, ro=[0,0,0])
            mc.parent(pelvisFkCtrl[1], pelvisFkCtrl[0])

        # set rotate orider
        nodes = [
            pelvis,
            upLeg,
            loLeg,
            midLeg,
            legEnd,
            legIkCtrl[-1],
            pelvisFkCtrl[-1],
            upLegFkCtrl[-1],
            midLegFkCtrl[-1],
            loLegFkCtrl[-1],
            toeLegFkCtrl[-1]]

        for j in nodes:
            if mc.objExists(j):
                mc.setAttr(j + '.ro', 0)

        # Set Fks
        mc.parentConstraint(upLegFkCtrl[-1], fkJnts[0], mo=0, n=fkJnts[0] + '_prc')
        mc.parentConstraint(midLegFkCtrl[-1], fkJnts[1], mo=0, n=fkJnts[1] + '_prc')
        mc.parentConstraint(loLegFkCtrl[-1], fkJnts[2], mo=0, n=fkJnts[2] + '_prc')
        mc.parentConstraint(toeLegFkCtrl[-1], fkJnts[3], mo=0, n=fkJnts[3] + '_prc')

        mc.parent(upLegFkCtrl[0], pelvisFkCtrl[-1])
        mc.parent(midLegFkCtrl[0], upLegFkCtrl[-1])
        mc.parent(loLegFkCtrl[0], midLegFkCtrl[-1])
        mc.parent(toeLegFkCtrl[0], loLegFkCtrl[-1])


        mc.pointConstraint(pelvisEnd, upLegFkCtrl[0], n=upLegFkCtrl[0] + '_pc')

        # Setup Iks
        # >> create global ik layer. ---------------------------------------------------------
        # pri help ik layout joints
        upLegPri = mc.duplicate(upLeg, n=upLeg.replace('_drv','') + 'Pri', po=1)[0]
        loLegPri = mc.duplicate(midLeg, n=loLeg.replace('_drv','') + 'Pri', po=1)[0]
        legEndPri = mc.duplicate(legEnd, n=legEnd.replace('_drv','') + 'Pri', po=1)[0]
        priJnts = [upLegPri, loLegPri, legEndPri]

        # fixed help jnt axis
        mc.parent(loLegPri, upLegPri)

        # > Thanks bro lixue and wangchong.
        # > get "?" position used math.
        # ------------- * ---
        # ----------- * -----
        # --------- * -------
        # ------- * ---------
        # ----- *--- *-------
        # --- ? ------ *-----
        # ---- *----- *------
        # ------ *-- *-------
        # -------- *---------
        # ----------------------------------------------------------------------------
        pos_a = om.MVector(mc.xform(legEnd, q=True, ws=True, t=True))
        pos_b = om.MVector(mc.xform(loLeg, q=True, ws=True, t=True))
        pos_c = om.MVector(mc.xform(midLeg, q=True, ws=True, t=True))
        pos_d = om.MVector(mc.xform(upLeg, q=True, ws=True, t=True))

        ca_vec = pos_a - pos_c
        dc_vec = pos_c - pos_d

        angle = ca_vec.angle(dc_vec)
        cos_angle = math.cos(angle)
        ca_len = ca_vec.length()
        t_l = (pos_b - pos_a).length() + (pos_c - pos_b).length()
        midLegLength = mc.getAttr(midLeg + '.tx')
        loLegPriPos = (mirror * (t_l * t_l - ca_len * ca_len) / (2 * t_l - 2 * ca_len * cos_angle)) + midLegLength
        # >> ----------------------------------------------------------------------------

        mc.setAttr(loLegPri + '.tx', loLegPriPos)
        mc.delete(mc.aimConstraint(legEndPri, loLegPri, aim=[mirror, 0, 0], u=[0, -mirror, 0], wuo=pelvisEnd))
        mc.makeIdentity(loLegPri, apply=True, r=1)
        mc.parent(legEndPri, loLegPri)

        mc.setAttr(legEndPri + '.jointOrientX', 0)
        mc.setAttr(legEndPri + '.jointOrientY', 0)
        mc.setAttr(legEndPri + '.jointOrientZ', 0)


        priIk = mc.ikHandle(sj=upLegPri, ee=legEndPri, ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'legPri_ik')[0]
        # ---------------------------------------------------------------------------------
        
        # ->> create main ik layer
        # ->> -------------------------------------------------------------------------------------------
        # -->> main ikhandle create
        ik = mc.ikHandle(sj=ikJnts[1], ee=ikJnts[3], ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'leg_ik')[0]
        
        # -->> leg ik ctrl attr add
        mc.addAttr(legIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(legIkCtrl[-1], ln='twist', at='double', k=1)
        mc.addAttr(legIkCtrl[-1], ln='local', at='enum', k=1, en='off:on')
        mc.addAttr(legIkCtrl[-1], ln='___', nn=' ', at='enum', en=' ', k=1)
        mc.addAttr(legIkCtrl[-1], ln='angleSet', at='double', k=1, min=-10, max=10)
        mc.addAttr(legIkCtrl[-1], ln='angleOffset', at='double', k=1)
        mc.addAttr(legIkCtrl[-1], ln='angleSide', at='double', k=1)
        mc.addAttr(legIkCtrl[-1], ln='____', nn=' ', at='enum', en=' ', k=1)
        controlTools.tagKeyable(legIkCtrl[-2:], 't r upLength midLength loLength stretch soft slide twist')

        # -->> knee ik ctrl attr add
        mc.addAttr(kneeIkCtrl[-1], ln='__', nn=' ', at='enum', en=' ', k=1)

        # -->> Ik local ctrl
        mc.orientConstraint(legIkLocalCtrl[-1], ikJnts[3], n=ikJnts[3] + '_oc', mo=1)
        localCtrlShape = mc.listRelatives(legIkLocalCtrl[-1], s=1)[0]
        mc.connectAttr(legIkCtrl[-1] + '.local', localCtrlShape + '.v')
        mc.setAttr(legIkCtrl[-1] + '.local', k=0, cb=1)
        
        # -->> Setup IK PV - offset/twist
        pvnodes = poleVectorTools.pvFollow(kneeIkCtrl[-1], ikJnts, legIkCtrl[-1], mirror)
        poleVectorTools.pvSide(kneeIkCtrl[-1], ik, ikJnts, mirror)

        
        mc.poleVectorConstraint(kneeIkCtrl[-1], priIk, n=priIk + '_pvc')
        mc.connectAttr(legIkCtrl[-1] + '.twist', priIk + '.twist')
        
        kneeIkLineGrp = aboutCrv.createCrvBetween2Pos(name=kneeIkCtrl[-1] + '_crv', st=ikJnts[1], ed=kneeIkCtrl[-1])
        mc.setAttr(kneeIkLineGrp + '.inheritsTransform', 0)

        # -->> combine ik layer
        ikRoll = mc.duplicate(upLegFkCtrl[-1], n=ikJnts[0] + '_roll', po=1)[0]
        mc.parent(ikRoll, upLegPri)
        mc.pointConstraint(ikRoll, ikJnts[0], n=ikJnts[0] + '_pc')
        oc = mc.orientConstraint(ikRoll, ikJnts[0], n=ikJnts[0] + '_oc')
        mc.setAttr(oc[0] + '.interpType', 2)
        mc.parent(ik, priIk)
        mc.parent(priIk, legIkCtrl[-1])

        mc.pointConstraint(pelvisEnd, priJnts[0], n=priJnts[0] + '_pc')

        # ->> -------------------------------------------------------------------------------------------

        # leg angle function set
        # ->> ---------------------------------------------------------------------------------
        # -->> offset / side
        md = mc.createNode('multiplyDivide', n=prefix + 'upLegAngleOffset_md')
        mc.connectAttr(legIkCtrl[-1] + '.angleOffset', md + '.i1x')
        mc.connectAttr(legIkCtrl[-1] + '.angleSide', md + '.i1y')

        mc.connectAttr(md + '.ox', oc[0] + '.oz')
        mc.connectAttr(md + '.oy', oc[0] + '.oy')

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

        # > Double Elbow Rig
        # ---------------------------------------------------------------------------------------------------------------
        db_mpNode = '{0}mod'.format(prefix + 'legdb_')
        if doubleKnee:
            # >> db center pivot joint set
            db_root = mc.duplicate(midLeg, po=1, n=prefix + 'db_root_drv')[0]
            db_pviot = mc.duplicate(midLeg, po=1, n=prefix + 'db_pviot_drv')[0]
            mc.parentConstraint(upLeg, db_root, n=db_root + '_prc', mo=1)
            mc.parent(db_pviot, db_root)
            mc.parent(midLegA, db_pviot)
            mc.pointConstraint(midLeg, db_pviot)

            # >> db ikhandle set
            dbik = mc.ikHandle(sj=midLegA, ee=midLegC, ap=1, sol='ikRPsolver', s='sticky', n=prefix + 'legdbikh')[0]

            # >> db ik ctrl loc
            dbikloc = aboutPublic.snapLoc(loLeg, name=prefix + 'legdbikloc')
            mc.pointConstraint(loLeg, dbikloc, n=dbikloc + '_pc')
            mc.pointConstraint(dbikloc, dbik, n=dbik + '_pc')
            mc.orientConstraint(loLeg, midLegC, n=midLegC + '_oc')

            # >> db pv ctrl loc
            dbPvloc = aboutPublic.snapLoc(midLeg, name=prefix + 'legdbpvloc')
            mc.parentConstraint(midLeg, dbPvloc, n=dbPvloc + '_pc')
            mc.poleVectorConstraint(dbPvloc, dbik, n=dbik + '_pvc')

            # >> db stretch
            disJnts = [midLeg, loLeg]
            stretch1Tools.stretchIk_db(prefix + 'legdb', db_pviot, disJnts, midLegC, dbikloc, 'tx', mpNode=None)

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
        # ---------------------------------------------------------------------------------------------------------------
        # tips: the default joint num is 5 .
        # bridgeNum must be same with bendy joint number.

        twistBridges = []
        bendyInfo = {}
        bendyUpRootJntGrp = []
        bendyMdRootJntGrp = []
        bendyLoRootJntGrp = []
        bendyJointList = []
        twistInfo = {}

        if twist:
            twistInfo = nonRoll.limbTwist(limbJnts=[[pelvis, upLeg], [upLeg, midLeg], [midLeg, loLeg, legEnd]], twistAxis='x', mirror=mirror)
            twistBridges = twistInfo['vmd']

        if bendy:
            if doubleKnee:
                bendyInfo = bendy3Limb.anim(prefix + 'qleg', [upLeg, midLegA, midLegB, loLeg, legEnd], twistBridges=twistBridges, volume=volume)
            else:
                bendyInfo = bendy3Limb.anim(prefix + 'qleg', [upLeg, midLeg, loLeg, legEnd], twistBridges=twistBridges, volume=volume)

            bendyUpRootJnt = bendyInfo['upjnts'][0]
            bendyMdRootJnt = bendyInfo['mdjnts'][0]
            bendyLoRootJnt = bendyInfo['lojnts'][0]
            bendyJointList = bendyInfo['jointList']

            bendyUpRootJntGrp = aboutPublic.createParentGrp(bendyUpRootJnt, 'grp')
            bendyMdRootJntGrp = aboutPublic.createParentGrp(bendyMdRootJnt, 'grp')
            bendyLoRootJntGrp = aboutPublic.createParentGrp(bendyLoRootJnt, 'grp')

            mc.parentConstraint(pelvisEnd, bendyUpRootJntGrp, n=bendyUpRootJntGrp + '_prc', mo=True)
            mc.parentConstraint(upLeg, bendyMdRootJntGrp, n=bendyMdRootJntGrp + '_prc', mo=True)
            mc.parentConstraint(midLeg, bendyLoRootJntGrp, n=bendyLoRootJntGrp + '_prc',  mo=True)

        # fk ik switch / display
        # ---------------------------------------------------------------------------------------------------------------
        mc.addAttr(limbSetCtrl[-1], ln='IKFK', at='double', dv=1, min=0, max=1, k=1)
        switchNode = mc.createNode('remapValue', n=prefix + 'legSwitchIKFK_rv')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', switchNode + '.inputValue')
        mc.setAttr(switchNode + '.outputMin', 1)
        mc.setAttr(switchNode + '.outputMax', 0)

        # -->> switch constraint node weights
        jntNum = len(drvJnts)
        for i in range(jntNum):
            prc = mc.parentConstraint(ikJnts[i], fkJnts[i], drvJnts[i], n=drvJnts[i] + '_prc', mo=1)[0]
            mc.connectAttr(limbSetCtrl[-1] + '.IKFK', prc + '.' + ikJnts[i] + 'W0')
            mc.connectAttr(switchNode + '.outValue', prc + '.' + fkJnts[i] + 'W1')

        # -->> display
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', legIkCtrl[0] + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', kneeIkLineGrp + '.v')
        mc.connectAttr(limbSetCtrl[-1] + '.IKFK', kneeIkCtrl[0] + '.v')
        displayRv = mc.createNode('reverse', n=prefix + 'legIKFK_vis_rv')
        mc.connectAttr(legIkCtrl[0] + '.v', displayRv + '.ix')
        mc.connectAttr(displayRv + '.ox', upLegFkCtrl[0] + '.v')

        # --------------------------------------- Start: !!! Do not modify the running order !!!---------------------------------------------------------------------------
        # > Sticky & Soft & Stretch
        # ---------------------------------------------------------------------------------------------------------------
        # ik stretch
        stretch2Info = stretch2Tools.stretchSoftIk(prefix + 'pleg_', pelvisEnd, priJnts, legIkCtrl[-1], kneeIkCtrl[-1], stretch)
        stretch3Info = stretch3Tools.stretchSoftIk(prefix + 'qleg_', pelvisEnd, ikJnts, legIkCtrl[-1], kneeIkCtrl[-1], stretch)
        priBlendloc = stretch2Info['blend']
        controlloc2 = stretch2Info['controlloc']
        controlloc3 = stretch3Info['controlloc']

        mc.pointConstraint(priBlendloc, priIk, n= priIk + '_pc')

        if stretch:
            # mc.disconnectAttr(legIkCtrl[-1] + '.upLength', stretch2Info['cmd'] + '.upLength')
            # mc.disconnectAttr(legIkCtrl[-1] + '.loLength', stretch2Info['cmd'] + '.loLength')
            mc.disconnectAttr(legIkCtrl[-1] + '.slide', stretch2Info['cmd'] + '.slide')
            mc.setDrivenKeyframe(stretch2Info['cmd'] + '.slide', cd=legIkCtrl[-1] + '.angleSet', dv=0, v=0, itt='linear', ott='linear')
            mc.setDrivenKeyframe(stretch2Info['cmd'] + '.slide', cd=legIkCtrl[-1] + '.angleSet', dv=10, v=0.4, itt='linear', ott='linear')
            mc.setDrivenKeyframe(stretch2Info['cmd'] + '.slide', cd=legIkCtrl[-1] + '.angleSet', dv=-10, v=-0.4, itt='linear', ott='linear')

            mc.deleteAttr(kneeIkCtrl[-1] + '.sticky')
            mc.deleteAttr(legIkCtrl[-1] + '.slide')

        # -->> angle set
        else:
            mc.deleteAttr(legIkCtrl[-1] + '.angleSet')

        # ->> ---------------------------------------------------------------------------------
        # Add Foot System
        # ---------------------------------------------------------------------------------------------------------------
        # foot
        footInfo = {}

        if addFoot:
            footInfo = footPart.anim(side, footprefix, legEnd, legIkCtrl[-1], toeLegFkCtrl[-1], limbSetCtrl[-1])
            footjnts = [footInfo['ankle'], footInfo['ball']]
            assetCommon.bindSet(footjnts)
            mc.pointConstraint(footInfo['stretchRev'], controlloc2, n=controlloc2 + '_pc')
            mc.pointConstraint(footInfo['stretchRev'], controlloc3, n=controlloc3 + '_pc')
        else:
            mc.pointConstraint(legIkCtrl[-1], controlloc2, n=controlloc2 + '_pc')
            mc.pointConstraint(legIkCtrl[-1], controlloc3, n=controlloc3 + '_pc')

        # fk
        stretch3Tools.stretchFk(prefix + 'qleg_', FkCtrls=[upLegFkCtrl[-1], midLegFkCtrl[-1], loLegFkCtrl[-1]])

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
            mc.parent(legPsdParent, psdGrp)
            poseDriverTool.constraintBridge(parentObj=pelvis, followObj=upLeg, parentHandle=legPsdParent, followHandle=legPsdFollow)

            # wrist psd
            legEndPsdPrefix = prefix + 'legEnd'
            legEndPsdParent = legEndPsdPrefix + '_psd_parent_handle'
            legEndPsdFollow = legEndPsdPrefix + '_psd_follow_handle'
            mc.parent(legEndPsdParent, psdGrp)

            if bendy:
                poseDriverTool.constraintBridge(parentObj=bendyInfo['lojnts'][-1], followObj=legEnd,
                                                parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)
            else:
                if doubleKnee:
                    poseDriverTool.constraintBridge(parentObj=midLegB, followObj=legEnd,
                                                    parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)
                else:
                    poseDriverTool.constraintBridge(parentObj=loLeg, followObj=legEnd,
                                                    parentHandle=legEndPsdParent, followHandle=legEndPsdFollow)

        # ---------------------------------------------------------------------------------------------------------------
        # IK FK Snap
        snapGrp = '{0}qleg_snap_noTrans'.format(prefix)
        if not mc.objExists(snapGrp):
            mc.createNode('transform', n=snapGrp)
            mc.hide(snapGrp)

        mc.parent(legEndIkSnapCtrl[0], legEndFkSnapCtrl[0], kneeIkSnapCtrl[0], snapGrp)

        mc.delete(kneeIkSnapCtrl[2])
        kneeIkSnap = mc.rename(kneeIkSnapCtrl[1], prefix + 'kneeIk_ctrl_snap')
        mc.rename(kneeIkSnapCtrl[0], prefix + 'kneeIk_ctrl_snap_grp')
        mc.parentConstraint(drvJnts[1], kneeIkSnap, n=kneeIkSnap+'_prc', mo=1)

        snapEnd = drvJnts[2]
        if addFoot:
            snapEnd = footInfo['ankle']

        mc.delete(legEndFkSnapCtrl[2])
        legEndFkSnap = mc.rename(legEndFkSnapCtrl[1], prefix + 'toeLegFk_ctrl_snap')
        mc.rename(legEndFkSnapCtrl[0], prefix + 'toeLegFk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, legEndFkSnap, n=legEndFkSnap+'_prc', mo=1)

        mc.delete(legEndIkSnapCtrl[2])
        legEndIkSnap = mc.rename(legEndIkSnapCtrl[1], prefix + 'legIk_ctrl_snap')
        mc.rename(legEndIkSnapCtrl[0], prefix + 'legIk_ctrl_snap_grp')
        mc.parentConstraint(snapEnd, legEndIkSnap, n=legEndIkSnap + '_prc', mo=1)


        # modify motion joints
        if bendy:
            mc.parent(bendyInfo['lojnts'][0].replace('_drv', ''), bendyInfo['mdjnts'][-2].replace('_drv', ''))
            mc.parent(bendyInfo['mdjnts'][0].replace('_drv', ''), bendyInfo['upjnts'][-2].replace('_drv', ''))
            mc.parent(bendyInfo['upjnts'][0].replace('_drv', ''), pelvis.replace('_drv', ''))

        if addFoot:
            mc.parent(footInfo['ankle'].replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))
            mc.delete(legEnd.replace('_drv', ''))
            mc.delete(footInfo['ballEnd'].replace('_drv', ''))
            mc.delete(footInfo['heel'].replace('_drv', ''))
        else:
            mc.parent(legEnd.replace('_drv', ''), bendyInfo['lojnts'][-2].replace('_drv', ''))

        mc.delete(bendyInfo['upjnts'][-1].replace('_drv', ''))
        mc.delete(bendyInfo['mdjnts'][-1].replace('_drv', ''))
        mc.delete(bendyInfo['lojnts'][-1].replace('_drv', ''))
        mc.delete(pelvisEnd.replace('_drv', ''))


        # CLEAN
        # ---------------------------------------------------------------------------------------------------------------
        mpNode = '{0}mod'.format(prefix + 'qleg_')
        if not mc.objExists(mpNode):
            mc.createNode('transform', n=mpNode)
            mc.parent(mpNode, 'controls')

        # parent
        # >> ctrls Parent
        mc.parent(legIkLocalCtrl[0], legIkCtrl[-1])

        ctrlNeedP = [ kneeIkCtrl[0], pvnodes['root'], kneeIkLineGrp, legIkCtrl[0], limbSetCtrl[0], pelvisFkCtrl[0] ]
        if bendy:
            ctrlNeedP.append(bendyInfo['rootGrp'])
        if autoPelvis:
            ctrlNeedP.append(autoPelvisGrp)

        for need in ctrlNeedP:
            mc.parent(need, mpNode)

        # >> jnts Parent
        jntNeedP = [pelvis, priJnts[0], ikJnts[0], fkJnts[0]]
        if bendy:
            jntNeedP.append(bendyUpRootJntGrp)
            jntNeedP.append(bendyMdRootJntGrp)
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

        # hide
        needHList = [ik, priIk, upLegPri, fkJnts[0], ikJnts[0], ik, connectLoc]
        if autoPelvis:
            needHList.append(autoPelvisGrp)

        for need in needHList:
            mc.hide(need)

        # delete
        mc.delete(orgAxisloc + '_grp', aimAxisloc, upAxisloc, el, ul, wl, le, le2)

        # keyable tag
        # -----------------------------------------------------------------------------------------------
        # > pelvis
        controlTools.tagKeyable(pelvisFkCtrl[-2:], 't r')
        controlTools.tagKeyable(pelvisIkCtrl[-2:], 't')
        # > ik controls
        controlTools.tagKeyable(legIkCtrl[-2:], 't r local twist stretch soft slide upLength loLength midLength '
                                                'footPivot rollAngle heelTwist roll sideRoll toeLift toe ball heel toeTwist ballTwist')
        controlTools.tagKeyable(legIkLocalCtrl[-2:], 'r')
        controlTools.tagKeyable(kneeIkCtrl[-2:], 't offset')
        # >fk controls
        controlTools.tagKeyable(upLegFkCtrl[-2:] + toeLegFkCtrl[-2:], 'r length')
        controlTools.tagKeyable(midLegFkCtrl[-2:] + loLegFkCtrl[-2:], 'rz length')
        # >setting control
        controlTools.tagKeyable(limbSetCtrl[-2:], 'IKFK')

        spaceTools.tag(upLegFkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls'.format(pelvisFkCtrl[-1], connectLoc), oo=True, dv=1)
        spaceTools.tag(legIkCtrl[-1], 'parent:{0} cog:cogGrp worldCtrl:controls world:noXform'.format(connectLoc), dv=2)
        spaceTools.tag(kneeIkCtrl[-1], 'align:{0} parent:{1} cog:cogGrp worldCtrl:controls world:noXform'.format(pvnodes['space'], connectLoc), dv=0, con=kneeIkCtrl[1])
        tagTools.tagIkFkSnap([upLegFkCtrl[-1], midLegFkCtrl[-1], loLegFkCtrl[-1], legIkCtrl[-1], kneeIkCtrl[-1], limbSetCtrl[-1]], prefix, 'quadLeg')

        if bendy:
            assetCommon.bindSet([pelvis] + bendyJointList)
        else:
            assetCommon.bindSet([pelvis, upLeg, midLeg, loLeg, legEnd])