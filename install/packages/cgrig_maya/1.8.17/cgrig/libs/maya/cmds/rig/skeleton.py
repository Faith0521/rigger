# -*- coding: utf-8 -*-
""""Module for skeleton discovery and manipulation

Supports name conventions for the following:

- Hive
- Skeleton Builder
- Accurig Character Creator
- HIK and varients
- UE5

example:

from cgrig.libs.maya.cmds.rig import skeleton
skeleton.getTwistSpineCount("spine00")

from cgrig.libs.maya.cmds.rig import skeleton
print(skeleton.IdentifySkeleton("god_M_godnode_jnt").skeletonFormat())


"""
import re
import pymel.core as pm
import math
from maya import cmds
from cgrig.libs.maya.cmds.math import mayadag
from cgrig.libs.utils import output
from cgrig.libs.maya.cmds.animation import batchconstraintconstants as bcc


def findListMatch(keyMatch, skeletonPreset):
    """Finds the matching index of a list of strings"""
    for jntDict in skeletonPreset:
        if keyMatch == next(iter(jntDict)):
            conventionStr = jntDict[keyMatch]["node"]
            # replace numbers with * for matching -------------------
            conventionStr = re.sub(r'\d', '?', conventionStr)
            conventionStr = re.sub(r'\*+', '?', conventionStr)
            findList = conventionStr.split("?")
            return list(filter(None, findList))  # remove empty strings
    return ""


def findStringsInOrder(mainString, findList):
    """Find if two strings are found anywhere in another string, must be in order of the two strings

    Searches only the first and last elements in a list.

    ['spine_M_', '', '_jnt']

    matches

    aNamespace:spine_M_01_jnt

    :param mainString: The main string to search in
    :type mainString: str
    :param findList: List of two strings to find in order
    :type findList: str
    :return: True if both strings are found in order, False otherwise
    :rtype: bool
    """
    if len(findList) == 1:
        if findList[0] in mainString:
            return True

    index1 = mainString.find(findList[0])
    if index1 == -1:
        return False

    index2 = mainString.find(findList[-1], index1 + len(findList[0]))
    if index2 == -1:
        return False
    return True


def jointHierarchy(baseJoint):
    allJoints = cmds.listRelatives(baseJoint, allDescendents=True, type="joint")
    if not allJoints:
        return list()
    allJoints.append(baseJoint)  # add the base joint to the list\
    return allJoints


def spineJoints(baseJoint, skeletonPreset=bcc.HIVE_BIPED_STRD_JOINTS_TWSTS):
    """Returns the spine joints from the base joint

    :param baseJoint: The parent joint to search down the chain
    :type baseJoint: str
    :param skeletonPreset: A skeleton preset list of dictionaries see bcc.HIVE_BIPED_STRD_JOINTS_TWSTS
    :type skeletonPreset: list(dict())
    :return: spineJnts
    :rtype: list(str)
    """
    spinejnts = list()

    # get all child joints -----------------------------------
    joints = jointHierarchy(baseJoint)
    if not joints:
        output.displayWarning("No joints found for {}".format(baseJoint))
        return

    spineFindList = findListMatch("spine00_M", skeletonPreset)
    for jnt in joints:
        if findStringsInOrder(jnt, spineFindList):  # "old:armUprTwst01_L" matches ["armUprTwst", "_L"]
            spinejnts.append(jnt)

    return spinejnts


def twistSpineJonts(baseJoint, skeletonPreset=bcc.HIVE_BIPED_STRD_JOINTS_TWSTS):
    """Returns joint lists for the arm twists, leg twists and spine components.

    :param baseJoint: The parent joint to search down the chain
    :type baseJoint: str
    :param skeletonPreset: A skeleton preset list of dictionaries see bcc.HIVE_BIPED_STRD_JOINTS_TWSTS
    :type skeletonPreset: list(dict())
    :return: uprArmTwist, lwrArmTwist, uprLegTwists, lwrLegTwists, spineJnts
    :rtype: tuple(list(str), list(str), list(str), list(str), list(str))
    """
    armUprTwists = list()
    armLwrTwists = list()
    legUprTwists = list()
    legLwrTwists = list()
    spinejnts = list()

    # get all child joints -----------------------------------
    joints = jointHierarchy(baseJoint)
    if not joints:
        output.displayWarning("No joints found for {}".format(baseJoint))
        return

    # Find lists are usually two strings in a list.  Representing two parts of joint name with a number in middle
    armUpprFindList = findListMatch("armUprTwst00_L", skeletonPreset)
    armLwrFindList = findListMatch("armLwrTwst00_L", skeletonPreset)
    legUprFindList = findListMatch("legUprTwst00_L", skeletonPreset)
    legLwrFindList = findListMatch("legLwrTwst00_L", skeletonPreset)
    spineFindList = findListMatch("spine00_M", skeletonPreset)

    for jnt in joints:
        if findStringsInOrder(jnt, armUpprFindList):  # "old:armUprTwst01_L" matches ["armUprTwst", "_L"]
            armUprTwists.append(jnt)
        if findStringsInOrder(jnt, armLwrFindList):
            armLwrTwists.append(jnt)
        if findStringsInOrder(jnt, legUprFindList):
            legUprTwists.append(jnt)
        if findStringsInOrder(jnt, legLwrFindList):
            legLwrTwists.append(jnt)
        if findStringsInOrder(jnt, spineFindList):
            spinejnts.append(jnt)

    return armUprTwists, armLwrTwists, legUprTwists, legLwrTwists, spinejnts


def getTwistSpineCount(baseJoint, skeletonPreset=bcc.HIVE_BIPED_STRD_JOINTS_TWSTS):
    """Returns the twist count for the arm, leg and spine components.

    :param baseJoint: The parent joint to search down the chain
    :type baseJoint: str
    :param skeletonPreset: A skeleton preset list of dictionaries see bcc.HIVE_BIPED_STRD_JOINTS_TWSTS
    :type skeletonPreset: list(dict())
    :return: uprArmTwistCount, lwrArmTwistCount, uprLegTwistCount, lwrLegTwistCount, spineCount
    :rtype: tuple(int, int, int, int, int)
    """
    armUprTwists, armLwrTwists, legUprTwists, legLwrTwists, spinejnts = twistSpineJonts(baseJoint, skeletonPreset)
    return len(armUprTwists), len(armLwrTwists), len(legUprTwists), len(legLwrTwists), len(spinejnts)


class IdentifySkeleton(object):
    """

    TODO handle namespaces

    """

    def __init__(self,
                 parentJoint
                 ):
        """Initialize variables for the class

        :param parentJoint: The source list of dictionaries
        :type parentJoint: dict(str)

        """
        super(IdentifySkeleton, self).__init__()
        self.parentJoint = parentJoint
        self.joints = list()
        self.skeletonType = ""

    def _validateSkeleton(self, jointDict):
        """Checks the joints match the name structure of the skeleton type.

        Checks to find biped joint naming in the jointList self.joints such as

        - spine
        - neck
        - head
        - shoulder_L
        - elbow_L
        - wrist_L
        - lowerLeg
        - foot
        - ball

        :param jointDict: The dictionary of joint names to match eg. bcc.HIVE_BIPED_STRD_JOINTS
        :type jointDict: dict(str)
        :return: True if valid, False otherwise
        :rtype: bool
        """
        spine = False
        neck = False
        head = False
        shoulder = False
        elbow = False
        wrist = False
        thigh = False
        knee = False
        ankle = False
        ball = False

        spineSearchList = findListMatch(bcc.SPINE01, jointDict)
        neckSearchList = findListMatch(bcc.NECK01, jointDict)
        headSearchList = findListMatch(bcc.HEAD, jointDict)
        shoulderSearchList = findListMatch(bcc.SHOULDER_L, jointDict)
        elbowSearchList = findListMatch(bcc.ELBOW_L, jointDict)
        wristSearchList = findListMatch(bcc.WRIST_L, jointDict)
        thighSearchList = findListMatch(bcc.THIGH_L, jointDict)
        kneeSearchList = findListMatch(bcc.KNEE_L, jointDict)
        ankleSearchList = findListMatch(bcc.ANKLE_L, jointDict)
        ballSearchList = findListMatch(bcc.BALL_L, jointDict)

        for jnt in self.joints:
            if findStringsInOrder(jnt, spineSearchList):  # "old:spine_M_00_jnt" matches ["spine_M_", "", "_M"]
                spine = True
            elif findStringsInOrder(jnt, neckSearchList):
                neck = True
            elif findStringsInOrder(jnt, headSearchList):
                head = True
            elif findStringsInOrder(jnt, shoulderSearchList):
                shoulder = True
            elif findStringsInOrder(jnt, elbowSearchList):
                elbow = True
            elif findStringsInOrder(jnt, wristSearchList):
                wrist = True
            elif findStringsInOrder(jnt, thighSearchList):
                thigh = True
            elif findStringsInOrder(jnt, kneeSearchList):
                knee = True
            elif findStringsInOrder(jnt, ankleSearchList):
                ankle = True
            elif findStringsInOrder(jnt, ballSearchList):
                ball = True

        if kneeSearchList == ['L_leg']:  # Skeleton Builder exception
            knee = True
            ankle = True

        if spine and neck and head and shoulder and elbow and wrist and thigh and knee and ankle and ball:
            return True

        return False

    def spineJoints(self):
        """Returns the spine joints from the base joint

        Requires skeletonFormat to be run first.
        """
        spineNameList = list()
        spineJoints = list()

        if not self.skeletonType or not self.jointDict:
            return list()

        for spineId in bcc.SPINE_IDS:
            for dict in self.jointDict:
                if next(iter(dict)) == spineId:
                    spineNameList.append(dict[spineId]["node"])
                    break

        if not spineNameList:
            return list()

        for spineName in spineNameList:
            for jnt in self.joints:
                if spineName in jnt:
                    spineJoints.append(jnt)
                    break
        return spineJoints

    def skeletonFormat(self):
        """Returns the type of skeleton based on the parent joint.

        See bcc.SKELETON_MAPPINGS for the list of skeleton types. Eg:

            "HIVE Biped Strd Jnts"
            "HIVE Biped Light Jnts"
            "Hive BIPED UE Jnts"
            "HIK Jnts"
            "UE5 Jnts"
            "AccuRig Jnts"
            "Skele Bldr Jnts"

        :return: The skeleton format of the current skeleton "HIVE Biped Strd Jnts", "" if unknown
        :rtype: str
        """
        # get all child joints -----------------------------------
        self.joints = jointHierarchy(self.parentJoint)
        if not self.joints:
            output.displayWarning("No joints found for {}".format(self.parentJoint))
            self.skeletonType = ""
            return ""
        for skeleDict in bcc.SKELETON_MAPPINGS:
            skeletonType = next(iter(skeleDict))
            self.jointDict = skeleDict[skeletonType]["nodes"]  # get the first key
            spineFindList = findListMatch(bcc.SPINE00, self.jointDict)
            if not spineFindList:
                continue
            for jnt in self.joints:
                if findStringsInOrder(jnt, spineFindList):  # "old:armUprTwst01_L" matches ["armUprTwst", "_L"]
                    if self._validateSkeleton(self.jointDict):  # always HIK
                        if (skeletonType == bcc.ROKOKO_JNTS_K or
                                skeletonType == bcc.UNITY_JNTS_K or
                                skeletonType == bcc.QUICK_RIG_JNTS_K or
                                skeletonType == bcc.MIXAMO_JNTS_K):
                            return bcc.HIK_JNTS_K
                        if (skeletonType == bcc.HIVE_BIPED_UE5_JNTS_K):  # always UE5
                            return bcc.UE5_JNTS_K
                        return skeletonType
                    break  # can't be this skele type
        self.skeletonType = ""
        return ""


def returnCVCoordsToList(surfaceCV):
    """
    DESCRIPTION:
    Returns cv coordinates from a surface CV

    ARGUMENTS:
    surfaceCV(string)

    RETURNS:
    coordinates(list)
    """
    coordinates = []
    """ strip out the first [ and following """
    stripBuffer1 = '['.join(surfaceCV.split('[')[-2:-1])
    stripBuffer2 = '['.join(surfaceCV.split('[')[-1:])
    """ strip out the ] """
    coordinates.append (']'.join(stripBuffer1.split(']')[-2:-1]))
    coordinates.append (']'.join(stripBuffer2.split(']')[-2:-1]))
    return coordinates


def returnListNoDuplicates(searchList):
    """
    DESCRIPTION:
    Removes duplicates from a list

    ARGUMENTS:
    searchList(list)

    RETURNS:
    newList(list)
    """
    newList = []
    for item in searchList:
        if item not in newList:
            newList.append(item)
    return newList


def cvListSimplifier(listToSimplify,mode):
    """
    DESCRIPTION:
    Simplifies a cv list. In a semi intelligent manner

    ARGUMENTS:
    listToSimplify(list) - list or nested list of cv stuff
    mode -  0 - mid only
            1 - ends only
            2 - mid and ends only
            3 - odds only
            4 - evens only
            5 - all exceipt start and end anchors
            6 - all

    RETURNS:
    newList(List)
    """
    culledList = []
    listLength = len(listToSimplify)
    # middle only mode
    if mode == 0:
        culledList.append(listToSimplify[int(round(listLength*1/2))])
    # ends only mode
    elif mode == 1:
        culledList.append(listToSimplify[0])
        culledList.append(listToSimplify[-1])
    # ends and mid mode
    elif mode == 2:
        culledList.append(listToSimplify[0])
        culledList.append(listToSimplify[int(round(listLength*1/2))])
        culledList.append(listToSimplify[-1])
    # odds mode
    elif mode == 3:
        #first pulling out the extra cv's on the ends rows [1] and [-2]
        tmpList = []
        tmpList.append(listToSimplify[0])
        midBuffer = listToSimplify[2:-3]
        for item in midBuffer:
            tmpList.append(item)
        tmpList.append(listToSimplify[-1])
        # now let's pick our stuff
        cnt = 1
        # checks if we have an even number or not. If it is...
        if len(tmpList)%2==0:
            for n in range (int(round(len(tmpList)*1/2))-1):
                culledList.append (tmpList[cnt])
                cnt+=2
            culledList.append (listToSimplify[-3])
        # if it's not...
        else:
            for n in range (int(round(len(tmpList)*1/2))):
                culledList.append (tmpList[cnt])
                cnt+=2
            culledList.append (tmpList[-1])
    # evens mode
    elif mode == 4:
        #first pulling out the extra cv's on the ends rows [1] and [-2]
        tmpList = []
        tmpList.append(listToSimplify[0])
        midBuffer = listToSimplify[2:-3]
        for item in midBuffer:
            tmpList.append(item)
        tmpList.append(listToSimplify[-1])
        cnt = 0
        # checks if we have an even number or not. If it is...
        if len(tmpList)%2==0:
            for n in range (int(round(len(tmpList)*1/2))):
                culledList.append (tmpList[cnt])
                cnt+=2
            culledList.append (tmpList[-1])
        # if it's not...
        else:
            for n in range (int(round(len(tmpList)*1/2))):
                culledList.append (tmpList[cnt])
                cnt+=2
            culledList.append (listToSimplify[-3])
    elif mode == 5:
        culledList.append(listToSimplify[0])
        midBuffer = listToSimplify[2:-2]
        for item in midBuffer:
            culledList.append(item)
        culledList.append(listToSimplify[-1])
    elif mode == 6:
        culledList = listToSimplify
    return culledList


def createJointChainsFromNurbsSurface(name,surface,chainMode=0,directionMode=0,reverse=False):
    """ 
    DESCRIPTION:
    Created joint chains from a lofted surface

    ARGUMENTS:
    name(string) - your root name for the joints	
    surface(string) - the lofted surface to be used
    chainMode -   0 - mid only
                  1 - ends only
                  2 - mid and ends only
                  3 - odds only
                  4 - evens only
                  5 - all except start and end anchors
                  6 - all
      directionMode - 0 - with surface flow
                      1 - against the grain 
      reverse(bool) - True/False - if you want to reverse the joint flow

    RETURNS:
    jointChainsList(nested list)
    """
    cmds.select(cl=True)
    """ Makes a series of joints chains on a nurbs surface with the input direciton mode of 1 or 2 as well as a True/False reverse option"""
    cvList = (cmds.ls ([surface+'.cv[*][*]'],flatten=True))
    #>>>>>Figuring out which direction to make our chains from
    cvListFirstTerm = []
    cvListSecondTerm = []
    firstTermCharacterSearchList = []
    secondTermCharacterSearchList = []
    for cv in cvList:
        cvBuffer = returnCVCoordsToList(cv)
        cvListFirstTerm.append(cvBuffer[0])
        cvListSecondTerm.append(cvBuffer[1])
    #Clean up our lists of cv parts -----------Great info for other places
    cleanFirstTermCVList = returnListNoDuplicates(cvListFirstTerm)
    cleanSecondTermCVList = returnListNoDuplicates(cvListSecondTerm)
    #pick some chain positions to make chains from
    chainToMakeBuffer=[]
    chainsToMakeBuffer=[]
    """ direction mode stuff """
    if directionMode == 0:
        """ pop out the second and second to last items cause we don't want joints on those extra cv's"""
        cleanSecondTermCVList.remove(cleanSecondTermCVList[1])
        cleanSecondTermCVList.remove(cleanSecondTermCVList[-2])
        for firstTerm in cleanFirstTermCVList:
            for secondTerm in cleanSecondTermCVList:
                chainToMakeBuffer.append ('%s%s%i%s%i%s' % (surface,'.cv[',int(firstTerm),'][',int(secondTerm),']'))
            chainsToMakeBuffer.append (chainToMakeBuffer)
            chainToMakeBuffer=[]
    if directionMode == 1:
        cleanFirstTermCVList.remove(cleanFirstTermCVList[1])
        cleanFirstTermCVList.remove(cleanFirstTermCVList[-2])
        for secondTerm in cleanSecondTermCVList:
            for firstTerm in cleanFirstTermCVList:
                chainToMakeBuffer.append ('%s%s%i%s%i%s' % (surface,'.cv[',int(firstTerm),'][',int(secondTerm),']'))
            chainsToMakeBuffer.append (chainToMakeBuffer)
            chainToMakeBuffer=[]
    """ reverse mode stuff """
    if reverse == True:
        for chain in chainsToMakeBuffer:
            chain.reverse()
    """ accounts for chainMode """
    chainBuffer = cvListSimplifier(chainsToMakeBuffer,chainMode)
    chainsToMakeBuffer = chainBuffer
    """ making the joints """
    jntCnt=0
    chainCnt=1                                         
    jointChainBuffer = []
    jointChainsBuffer = []
    for chain in chainsToMakeBuffer:
        for cv in chain:
            jointPos = cmds.pointPosition (cv,world=True)
            """Inserts our new joint, names it and positions it"""
            currentJnt = ('%s%s%i%s%i' % (name,'_',chainCnt,'_',jntCnt))
            cmds.joint (p=(jointPos[0],jointPos[1],jointPos[2]),n=currentJnt)
            """adds it to our return joint list"""
            jointChainBuffer.append (currentJnt)
            jntCnt+=1
        jointChainsBuffer.append (jointChainBuffer)
        chainCnt +=1
        jntCnt = 0
        jointChainBuffer = []
        cmds.select (clear=True)
    # """ fix the joint sizes """
    # for chain in jointChainsBuffer:
    #     setGoodJointRadius (chain,.5)
    cmds.select(cl=True)
    return jointChainsBuffer


def loftSurfaceFromJointList(jointList,outChannel):
    """ 
    ACKNOWLEDMENT:

    DESCRIPTION:
    Lofts a surface from a joint list

    ARGUMENTS:
    jointList(list) - list of the joints you want to loft from
    outChannel(string)['x','y','z'] - the extrude out direction

    RETURNS:
    surface(string)
    """

    """ return a good length for out loft curves """
    length = (mayadag.distanceTwoObjs(jointList[0], jointList[-1]) / 2) * 0.2
    loftCurveList = []
    crvPosBuffer = []
    crvPosBuffer.append ([0,0,0])
    if outChannel == 'x':
        crvPosBuffer.append ([length,0,0])
    elif outChannel == 'y':
        crvPosBuffer.append ([0,length,0])
    elif outChannel == 'z':
        crvPosBuffer.append ([0,0,length])
    crvPosBuffer.reverse ()
    """ for each joint, make a loft curve and snap it to the joint it goes with """
    for jnt in jointList:
        crvBuffer = cmds.curve (d=1, p = crvPosBuffer , os=True, n=(jnt+'_tmpCrv'))
        cmds.xform (crvBuffer, cp = True)
        cnstBuffer = cmds.parentConstraint ([jnt], [crvBuffer], maintainOffset = False)
        cmds.delete (cnstBuffer)
        loftCurveList.append (crvBuffer)

    controlSurface = cmds.loft (loftCurveList, reverseSurfaceNormals = True, ch = False, uniform = True, degree = 3)[0]
    controlSurface = cmds.rebuildSurface(controlSurface, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=0, du=3, sv=0, dv=3, fr=0, dir=2)[0]

    """ deletes our loft curve list"""
    for crv in loftCurveList:
        cmds.delete (crv)

    return controlSurface


# def re_joints(joints, count, axis, typ, prefix='control_', mirror=False, surface=None, world=False, add=True):
#     u"""
#     重建骨骼
#     :param joints: 源骨
#     :param count: 新骨骼个
#     :param axis: 第二轴轴
#     :param typ: 第二轴朝向类
#     :param prefix: 前缀名
#     :param mirror: 是否镜像骨骼
#     :param surface: 根据曲面创建骨骼
#     :param world: 世界轴
#     :param add: 添加属性
#     :return:
#     """
#     # 获取骨骼矩阵，避免骨骼删掉后无法获取
#     joints = [joint for joint in joints if cmds.objectType(joint) in ["joint", "transform"]]
#     matrix_list = [cmds.xform(joint, q=1, ws=1, m=1) for joint in joints]
#     if is_shape(joints[0], "nurbsCurve"):
#         # 如果选择了曲线，则获取ep点坐
#         points = cmds.xform(joints[0]+".cv[*]", q=1, ws=1, t=1)
#         points = [points[i:i+3] for i in range(0, len(points), 3)]
#     else:
#         # 如果选择了骨骼，获取选择骨骼的坐
#         points = [cmds.xform(joint, q=1, ws=1, t=1) for joint in joints]
#         cmds.delete(joints)
#     normals = []
#     if surface:
#         normals = get_joint_normals_by_surface(surface, count)
#
#     # 创建经过points的曲
#     curve = create_curve_by_joints(points)
#     # 按骨骼长度，创建等长骨骼
#     length = cmds.arclen(curve, ch=0)
#     step = length/(count-1)
#     joint = None
#     joints = []
#     for i in range(count):
#         name = "{prefix}0{index}_jnt".format(prefix=prefix, index=i)
#         if cmds.objExists(name):
#             cmds.delete(name)
#         joint = cmds.joint(joint, name="{prefix}0{index}_jnt".format(prefix=prefix, index=i))
#         if add:
#             attribute.addAttributes(joint, "rope_control_joint", "bool", value=True, keyable=False)
#             attribute.addAttributes(joint, "rigName", "string", value=prefix, keyable=False)
#             attribute.addAttributes(joint, "axis", "string", value=axis, keyable=False)
#         cmds.setAttr(joint+".tx", step)
#         joints.append(joint)
#     cmds.xform(joints[0], ws=1, t=points[0])
#
#     # 创建样条IK
#     ik = cmds.ikHandle(sol="ikSplineSolver", ccv=0, sj=joints[0], ee=joints[-1], curve=curve)[0]
#
#     for _ in range(3):
#         # 在倒数第二个骨骼出，放止一个临时组，位置设置为points[-1]
#         temp = cmds.group(em=1, p=joints[-2])
#         cmds.xform(temp, ws=1, t=points[-1])
#         # 此时，最后以跟x轴的坐标与临时组x轴坐标的差，越为线段长度与曲线长度的
#         err = (cmds.getAttr(joints[-1]+".tx") - cmds.getAttr(temp+".tx"))/(count-1)
#         # 缩小tx的值，减少误差，让最后一根骨骼落地在曲线末短
#         for joint in joints[1:]:
#             cmds.setAttr(joint + ".tx", cmds.getAttr(joint + ".tx")-err)
#         cmds.delete(temp)
#
#     # 设置骨骼第二轴朝
#     if axis == "y":
#         cmds.setAttr(ik + ".dWorldUpAxis", 0)
#     elif axis == "z":
#         cmds.setAttr(ik + ".dWorldUpAxis", 3)
#     up_map = {
#         "+x": [1, 0, 0],
#         "-x": [-1, 0, 0],
#         "+y": [0, 1, 0],
#         "-y": [0, -1, 0],
#         "+z": [0, 0, 1],
#         "-z": [0, 0, -1]
#     }
#     if typ in up_map:
#         # 设置up为世界正方向
#         up1, up2 = up_map[typ], up_map[typ]
#     else:
#         # 设置up为首尾骨骼的y/z轴朝
#         axis_index = slice(4, 7) if axis == "y" else slice(8, 11)
#         joint_index = -1 if typ == u"首尾骨骼" else 0
#         up1, up2 = matrix_list[0][axis_index], matrix_list[joint_index][axis_index]
#     if normals:
#         up1, up2 = normals[0], normals[-1]
#     # 设置ik高级旋转
#     cmds.setAttr(ik + ".dTwistControlEnable", True)
#     cmds.setAttr(ik + ".dWorldUpType", 4)
#     cmds.setAttr(ik + ".dWorldUpAxis", 0 if axis == "y" else 3)
#     cmds.setAttr(ik + ".dWorldUpVector", *up1)
#     cmds.setAttr(ik + ".dWorldUpVectorEnd", *up2)
#     # 获取骨骼矩阵，触发ik计算更新
#     cmds.xform(joints[0], q=1, ws=1, m=1)
#     cmds.delete(ik, curve)
#     # 显示轴向，冻结旋
#     cmds.toggle(joints, la=1)
#     cmds.makeIdentity(joints, apply=1, r=1)
#     if world:
#         clear_rotation_keep_position(joints)
#     if mirror:
#         for joint in joints:
#             mirror_joint = naming.convertRLName(joint)
#             if cmds.objExists(mirror_joint):
#                 cmds.delete(mirror_joint)
#         mirror_joints = cmds.mirrorJoint(joints[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=["L_", "R_"])
#         if add:
#             [attribute.addAttributes(jnt, "rope_control_joint", "bool", value=True, keyable=False) for jnt in mirror_joints]
#             [cmds.setAttr("{}.rigName".format(jnt), naming.convertRLName(prefix), type='string') for jnt in mirror_joints]
#         joints += mirror_joints
#
#     return joints
#






# 计算距离
def dis(start, End):
    outDis = 0
    for i, t in zip(start, End):
        outDis += math.pow(abs(i - t), 2)
    return math.sqrt(outDis)


def get_close_obj(obj, obj_list):
    pos = pm.xform(obj, q=True, t=True, ws=True)
    dis_list = [(i, dis(pos, pm.xform(i, q=True, t=True, ws=True))) for i in obj_list]
    return min(dis_list, key=lambda i: i[1])[0]


def set_cure_color(curve, color_ids=1):
    sh = curve.getShape()
    sh.dispCV.set(1)
    sh.dispEP.set(1)
    sh.dispHull.set(1)
    sh.overrideEnabled.set(1)
    sh.ovc.set(color_ids)
    pm.delete(curve, ch=True)
    return 0


# polyToCurve -form 1 -degree 1 -conformToSmoothMeshPreview 0;c_curve()
def c_curve(name, color=10):
    """
    将选中的多边形转换为标准化曲线

    :param name: 生成曲线的名称
    :type name: str
    :param color: 曲线的颜色索引，默认值为10（蓝色）
    :type color: int
    :return: 处理后的曲线对象
    :rtype: pm.PyNode
    :raises RuntimeError: 当多边形转换为曲线失败或曲线没有控制点时
    """
    try:
        # 将选中的多边形转换为曲线
        curve_list = pm.polyToCurve(ch=False, form=1, degree=1)
        if not curve_list:
            raise RuntimeError("多边形转换为曲线失败")

        copy_curve = pm.ls(curve_list)[0]
        pm.rename(copy_curve, name)

        # 检查曲线是否有控制点
        if not copy_curve.cv:
            raise RuntimeError("转换后的曲线没有控制点")

        # 获取控制点信息
        point_list = [pm.xform(i, q=True, t=True, ws=True) for i in copy_curve.cv]
        id_list = list(range(len(copy_curve.cv)))
        id_pt_list = list(zip(point_list, id_list))

        if not id_pt_list:
            raise RuntimeError("无法获取有效的控制点数据")

        # 标准化曲线起始点
        id_size = len(copy_curve.cv)
        x_min_id = min(id_pt_list, key=lambda i: i[0][0])[1]

        for i in id_list:
            s_id = i
            e_id = (i + x_min_id) % id_size
            pm.xform(copy_curve.cv[s_id], ws=True, t=point_list[e_id])

        # 重新获取调整后的控制点信息
        point_list = [pm.xform(i, q=True, t=True, ws=True) for i in copy_curve.cv]
        id_pt_list = list(zip(point_list, id_list))

        if not id_pt_list:
            raise RuntimeError("调整后无法获取有效的控制点数据")

        # 标准化曲线方向
        y_min_id = min(id_pt_list, key=lambda i: i[0][1])[1]
        y_max_id = max(id_pt_list, key=lambda i: i[0][1])[1]

        if y_min_id > y_max_id:
            pm.reverseCurve(ch=0, rpo=1)

        # 设置曲线颜色
        set_cure_color(copy_curve, color)
        return copy_curve

    except Exception as e:
        pm.error(f"创建曲线时发生错误: {str(e)}")
        raise


# main(outer_loop_curve,main_loop_curve,inner_loop_curve,joint_list,total_joint,mesh)
def main(outer_loop_curve, main_loop_curve, inner_loop_curve, joint_list, total_joint, mesh):
    # outer_loop_curve = c_curve('outer_loop',15)
    # main_loop_curve = c_curve('main_loop',14)
    # inner_loop_curve = c_curve('inner_loop',13)

    # joint_list = pm.selected()

    # total_joint = pm.selected()[0]

    # mesh = pm.selected()[0]

    skin_joint = pm.skinCluster(mesh, q=True, inf=True)
    liw_list = [i.liw.get() for i in skin_joint]

    ###
    sh = mesh.getShape()
    skin = sh.history(type='skinCluster')
    if len(skin) < 1:
        om.MGlobal.displayError('错误没有蒙皮关节')
        return 1
    if len(skin) > 1:
        om.MGlobal.displayWarning('蒙皮关节过多')
    skin = skin[0]

    closest_mesh = pm.createNode('closestPointOnMesh')
    sh.worldMesh >> closest_mesh.inMesh

    outer_to_mesh = [(closest_mesh.ip.set(pm.xform(i, q=True, t=True, ws=True)), closest_mesh.vt.get())[1] for i in
                     outer_loop_curve.cv]
    main_to_mesh = [(closest_mesh.ip.set(pm.xform(i, q=True, t=True, ws=True)), closest_mesh.vt.get())[1] for i in
                    main_loop_curve.cv]
    inner_to_mesh = [(closest_mesh.ip.set(pm.xform(i, q=True, t=True, ws=True)), closest_mesh.vt.get())[1] for i in
                     inner_loop_curve.cv]

    pm.select(cl=True)
    test_joint = pm.joint()
    pm.skinCluster(skin, e=True, dr=4, lw=True, wt=0, ai=test_joint)

    [i.liw.set(1) for i in skin_joint]
    total_joint.liw.set(0)
    test_joint.liw.set(0)

    pm.select(sh.vtx[main_to_mesh], r=True)
    sel_vtx_lenth = len(pm.selected(fl=True))
    for i in range(sel_vtx_lenth):
        pm.mel.eval('''PolySelectTraverse 1;''')
        pm.select(sh.vtx[outer_to_mesh], sh.vtx[inner_to_mesh], d=True)
    pm.select(sh.vtx[outer_to_mesh], sh.vtx[inner_to_mesh], add=True)

    pm.skinPercent(skin, pm.selected(), tv=(test_joint, 1))

    eye_total_sel = pm.selected()

    pm.select(sh.vtx[inner_to_mesh], r=True)
    for i in range(sel_vtx_lenth):
        pm.mel.eval('PolySelectTraverse 1;')
        pm.select(sh.vtx[main_to_mesh], d=True)
    pm.select(sh.vtx[main_to_mesh], add=True)

    pm.select(eye_total_sel, tgl=True)

    pm.mel.ArtPaintSkinWeightsTool()

    pm.mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
    pm.mel.eval('artAttrSkinPaintCtx -e -opacity 1 `currentCtx`;')

    pm.mel.artSkinInflListChanging(total_joint, 1)
    pm.mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
    for i in range(sel_vtx_lenth):
        pm.mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')

    pm.mel.artSkinInflListChanging(test_joint, 1)
    pm.mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
    for i in range(sel_vtx_lenth):
        pm.mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')

    [i.liw.set(1) for i in pm.skinCluster(mesh, q=True, inf=True)]
    test_joint.liw.set(0)
    for i, t, s in zip(outer_to_mesh, main_to_mesh, inner_to_mesh):
        pm.select(cl=True)
        joint = get_close_obj(sh.vtx[t], joint_list)
        pm.polySelect(sh, sep=(i, t))
        pm.polySelect(sh, sep=(t, s))
        pm.skinPercent(skin, tv=(joint, 1))

    ###
    pm.delete(closest_mesh)
    pm.delete(test_joint)
    [i.liw.set(t) for i, t in zip(skin_joint, liw_list)]
    return 0


class data:
    outer_loop_curve = None
    main_loop_curve = None
    inner_loop_curve = None

    joint_list = None
    total_joint = None
    mesh = None


def set_outer_loop_curve(*args):
    data.outer_loop_curve = c_curve('outer_loop', 15)


def set_main_loop_curve(*args):
    data.main_loop_curve = c_curve('main_loop_curve', 14)


def set_inner_loop_curve(*args):
    data.inner_loop_curve = c_curve('inner_loop_curve', 13)


def set_joint_list(*args):
    data.joint_list = pm.selected()


def set_total_joint(*args):
    if len(pm.selected()) > 0: data.total_joint = pm.selected()[0]


def set_mesh(*args):
    if len(pm.selected()) > 0: data.mesh = pm.selected()[0]


def doIt(*args):
    if data.outer_loop_curve is None:
        return 1
    if data.main_loop_curve is None:
        return 1
    if data.inner_loop_curve is None:
        return 1
    if data.joint_list is None:
        return 1
    if data.total_joint is None:
        return 1
    if data.mesh is None:
        return 1
    main(data.outer_loop_curve,
         data.main_loop_curve,
         data.inner_loop_curve,
         data.joint_list,
         data.total_joint,
         data.mesh)


def gui():
    window = pm.window(title="眼睛权重工具", iconName='Short Name', widthHeight=(200, 220))
    pm.columnLayout(adjustableColumn=True)
    pm.button(label='设置外环线', c=set_outer_loop_curve)
    pm.button(label='设置主环线', c=set_main_loop_curve)
    pm.button(label='设置内环线', c=set_inner_loop_curve)
    pm.button(label='蒙皮关节列表', c=set_joint_list)
    pm.button(label='主关节', c=set_total_joint)
    pm.button(label='模型', c=set_mesh)
    pm.button(label='执行', c=doIt)
    pm.setParent('..')
    pm.showWindow(window)



























