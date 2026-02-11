# > Pose Drivers
# ------------------------------------------------------------------------------------------------------------------
import maya.cmds as mc
from . import poseDriverTool

def createPsd(prefix):
    # topeNode
    topNode = 'Psd_System'
    if not mc.objExists(topNode):
        mc.createNode('transform', n=topNode)
        if mc.objExists('noTransform'):
            mc.parent(topNode, 'noTransform')

    mirror = False
    if prefix == 'L_':
        mirror = False
    elif prefix == 'R_':
        mirror = True

    # joint data
    if prefix == 'L_' or prefix == 'R_':
        clavicleP = 'Chest_jnt'
        clavicle = 'Clavicle_UD_jnt'

        armP = 'Clavicle_UD_jnt'
        arm = 'Arm01_drv'
        armReal = 'ArmA_01_jnt'

        elbowP = 'ArmA_04_jnt'
        elbow = 'ArmB_01_jnt'

        wristP = 'ArmB_04_jnt'
        wrist = 'Hand_jnt'

        legP = 'hip_jnt'
        leg = 'Leg01_drv'
        legReal = 'LegA_01_jnt'

        kneeP = 'LegA_04_jnt'
        knee = 'LegB_01_jnt'

        ankleP = 'LegB_04_jnt'
        ankle = 'Foot_jnt'

        toeP = 'Foot_jnt'
        toe = 'Toe_jnt'


        # armPsd, elbowPsd, wristPsd, legPsd, kneePsd, anklePsd =  {},{},{},{},{},{}
        if mc.objExists(clavicleP) and mc.objExists(prefix + clavicle) and not mc.objExists(prefix + clavicle + '_psd_parent_handle'):
            claviclePsd = poseDriverTool.createBridge(prefix + clavicle, axis='+x', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + clavicle, 0.05)
            poseDriverTool.constraintBridge(parentObj=clavicleP, followObj=prefix + clavicle, parentHandle=claviclePsd['parent'], followHandle=claviclePsd['follow'])
            mc.parent(claviclePsd['parent'], topNode)

        if mc.objExists(prefix + armP) and mc.objExists(prefix + arm) and not mc.objExists(prefix + arm + '_psd_parent_handle'):
            armPsd = poseDriverTool.createBridge(prefix + arm, axis='+x', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + arm, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + armP, followObj=prefix + arm, parentHandle=armPsd['parent'], followHandle=armPsd['follow'])
            mc.delete(armPsd['follow']+'_prc')
            mc.parentConstraint(prefix + armReal, armPsd['follow'], n=armPsd['follow']+'_prc', mo=True)
            mc.parent(armPsd['parent'], topNode)

        if mc.objExists(prefix + elbowP) and mc.objExists(prefix + elbow) and not mc.objExists(prefix + elbow + '_psd_parent_handle'):
            elbowPsd = poseDriverTool.createBridge(prefix + elbow, axis='+x', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + elbow, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + elbowP, followObj=prefix + elbow, parentHandle=elbowPsd['parent'], followHandle=elbowPsd['follow'])
            mc.parent(elbowPsd['parent'], topNode)

        if mc.objExists(prefix + wristP) and mc.objExists(prefix + wrist) and not mc.objExists(prefix + wrist + '_psd_parent_handle'):
            wristPsd = poseDriverTool.createBridge(prefix + wrist, axis='+x', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + wrist, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + wristP, followObj=prefix + wrist, parentHandle=wristPsd['parent'], followHandle=wristPsd['follow'])
            mc.parent(wristPsd['parent'], topNode)

        if mc.objExists(legP) and mc.objExists(prefix + leg) and not mc.objExists(prefix + leg + '_psd_parent_handle'):
            legPsd = poseDriverTool.createBridge(prefix + leg, axis='-y', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + leg, 0.05)
            poseDriverTool.constraintBridge(parentObj=legP, followObj=prefix + leg, parentHandle=legPsd['parent'], followHandle=legPsd['follow'])
            mc.delete(legPsd['follow']+'_prc')
            mc.parentConstraint(prefix + legReal, legPsd['follow'], n=legPsd['follow']+'_prc', mo=True)
            mc.parent(legPsd['parent'], topNode)

        if mc.objExists(prefix + kneeP) and mc.objExists(prefix + knee) and not mc.objExists(prefix + knee + '_psd_parent_handle'):
            kneePsd = poseDriverTool.createBridge(prefix + knee, axis='-y', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + knee, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + kneeP, followObj=prefix + knee, parentHandle=kneePsd['parent'], followHandle=kneePsd['follow'])
            mc.parent(kneePsd['parent'], topNode)

        if mc.objExists(prefix + ankleP) and mc.objExists(prefix + ankle) and not mc.objExists(prefix + ankle + '_psd_parent_handle'):
            anklePsd = poseDriverTool.createBridge(prefix + ankle, axis='-y', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + ankle, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + ankleP, followObj=prefix + ankle, parentHandle=anklePsd['parent'], followHandle=anklePsd['follow'])
            mc.parent(anklePsd['parent'], topNode)

        if mc.objExists(prefix + toeP) and mc.objExists(prefix + toe) and not mc.objExists(prefix + toe + '_psd_parent_handle'):
            toePsd = poseDriverTool.createBridge(prefix + toe, axis='+z', mirror=mirror)
            poseDriverTool.scaleBridge(prefix + toe, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + toeP, followObj=prefix + toe, parentHandle=toePsd['parent'], followHandle=toePsd['follow'])
            mc.parent(toePsd['parent'], topNode)

    if prefix == 'M_' or prefix == '':
        chestP = 'Torso4_jnt'
        chest = 'Chest_jnt'

        neckP = 'Chest_jnt'
        neck = 'Neck01_jnt'

        torsoP = 'hip_jnt'
        torso = 'Torso1_jnt'

        headP = 'Neck02_jnt'
        head = 'Head01_jnt'

        chestPsd, neckPsd, torsoPsd, headPsd = {},{},{},{}

        if mc.objExists(prefix + chestP) and mc.objExists(prefix + chest) and not mc.objExists(prefix + chest + '_psd_parent_handle'):
            chestPsd = poseDriverTool.createBridge(prefix + chest, axis='+y', mirror=mirror)
            poseDriverTool.scaleBridge(chest, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + chestP, followObj=prefix + chest, parentHandle=chestPsd['parent'], followHandle=chestPsd['follow'])
            mc.parent(chestPsd['parent'], topNode)

        if mc.objExists(prefix + neckP) and mc.objExists(prefix + neck) and not mc.objExists(prefix + neck + '_psd_parent_handle'):
            neckPsd = poseDriverTool.createBridge(prefix + neck, axis='+y', mirror=mirror)
            poseDriverTool.scaleBridge(neck, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + neckP, followObj=prefix + neck, parentHandle=neckPsd['parent'], followHandle=neckPsd['follow'])
            mc.parent(neckPsd['parent'], topNode)

        if mc.objExists(torsoP) and mc.objExists(prefix + torso) and not mc.objExists(prefix + torso + '_psd_parent_handle'):
            torsoPsd = poseDriverTool.createBridge(prefix + torso, axis='+y', mirror=mirror)
            poseDriverTool.scaleBridge(torso, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + torsoP, followObj=prefix + torso, parentHandle=torsoPsd['parent'], followHandle=torsoPsd['follow'])
            mc.parent(torsoPsd['parent'], topNode)

        if mc.objExists(headP) and mc.objExists(prefix + head) and not mc.objExists(prefix + head + '_psd_parent_handle'):
            headPsd = poseDriverTool.createBridge(prefix + head, axis='+y', mirror=mirror)
            poseDriverTool.scaleBridge(head, 0.05)
            poseDriverTool.constraintBridge(parentObj=prefix + headP, followObj=prefix + head, parentHandle=headPsd['parent'], followHandle=headPsd['follow'])
            mc.parent(headPsd['parent'], topNode)

        # rename driver attribute
        orgDriverAttrsDict =  {'inner':'R_side','outer':'L_side',
                           'outerFront':'L_side_Front','outerBack':'L_side_Back',
                           'innerFront':'R_side_Front','innerBack':'R_side_Back'}
        bridges = [chestPsd, neckPsd, torsoPsd, headPsd]
        for bridge in bridges:
            for key in orgDriverAttrsDict.keys():
                try:
                    if mc.objExists(bridge['cmd']):
                        mc.renameAttr(bridge['cmd']+'.'+key, orgDriverAttrsDict[key])
                except:
                    pass

def create_timeLine_psd():
    createPsd('L_')
    createPsd('R_')
    createPsd('')

