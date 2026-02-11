import pymel.core as pm
from maya import mel

class rig():
    rigGrp      = None
    locGrp      = None
    ctrlGrp     = None
    crvGrp      = None
    clusterGrp  = None
    name        = None
    
def createMotionPathAttachRig(prefix):
    grp = rig()
    
    rig.rigGrp = pm.group(em = 1, n = '%s_grp'%prefix)
    rig.locGrp = pm.group(em = 1, n = '%s_loc_grp'%prefix)
    rig.ctrlGrp = pm.group(em = 1, n = '%s_ctrl_grp'%prefix)
    rig.crvGrp = pm.group(em = 1, n = '%s_crv_grp'%prefix)
    rig.clusterGrp = pm.group(em = 1, n = '%s_clusterGrp_grp'%prefix)
    
    pm.parent(rig.ctrlGrp, rig.locGrp, rig.crvGrp, rig.clusterGrp, rig.rigGrp)
    pm.addAttr(rig.rigGrp, ln = 'go', k = 1, minValue = 0, maxValue = 100)
    
    rig.clusterGrp.v.set(0)
    rig.locGrp.v.set(0)

    return grp

def makeTransformAttachToCurve(path, arcLenNode, tr, org_pr, offsetAttr, isControledParams = True):
    pm.select(tr, path)
    motionPathNode = mel.eval('pathAnimation -fractionMode true -follow true -followAxis y -upAxis z -worldUpType "scene" -inverseUp false -inverseFront false -bank false -startTimeU `playbackOptions -query -minTime` -endTimeU  `playbackOptions -query -maxTime`;')

    if isControledParams:
        arcLength = arcLenNode.arcLength.get()

        crvLenMul = pm.createNode('multiplyDivide')
        crvLenMul.input1X.set(arcLength)
        crvLenMul.operation.set(2)
        arcLenNode.arcLength >> crvLenMul.input2X
        
        crvScaleParam = pm.createNode('multiplyDivide')
        crvScaleParam.input1X.set(org_pr)
        crvLenMul.outputX >> crvScaleParam.input2X
        
        addOffset = pm.createNode('plusMinusAverage')
        pm.connectAttr(offsetAttr, addOffset.input1D[0])
        crvScaleParam.outputX >> addOffset.input1D[1]
        pm.connectAttr(addOffset.output1D, '%s.uValue'%motionPathNode, f = 1)
        
    return pm.PyNode(motionPathNode)

def findNurbsIKFKBaseCrv(ctrl):
    jnt = pm.listRelatives(ctrl, ad = 1, typ = 'joint')[0]
    skin = pm.listConnections(jnt.worldMatrix[0])[-1]
    nurbs = pm.listConnections(skin.outputGeometry)[0]

    for n in pm.listConnections(nurbs.worldSpace[0]):
        if pm.objectType(n) == 'curveFromSurfaceIso':
            return pm.listConnections(n.outputCurve)[0]
            
def findNurbsIKFKCtrlOffsets(ctrl):
    pm.select(ctrl)
    while not pm.selected()[0] == pm.pickWalk(d = 'up')[0]:
        tr = pm.selected()[0]
        if pm.listConnections(tr.r):
            offset = pm.listConnections(tr.r)
            break
            
    pm.select(offset)
    lastSelection = pm.selected()[0]
    while not pm.selected()[0] == pm.pickWalk(d = 'up')[0]:
        tr = pm.selected()[0]
        if not ('_offset' in str(tr)):
            break
        lastSelection = tr

    return [lastSelection] + list(reversed(pm.listRelatives(lastSelection, ad = 1)))
    
def getNearestParamOnCurve(crv, positions):
    npoc = pm.createNode('nearestPointOnCurve')
    pm.connectAttr('%s.worldSpace'%crv, npoc.inputCurve)
    
    prs = []
    for pos in positions:
        npoc.ip.set(pos)
        prs += [npoc.parameter.get()]
        
    pm.delete(npoc)
    return prs
    
def createIkCtrls(color = 13):
    ctrlGrps = []
    bbox = pm.xform(pm.selected()[0], query=True, boundingBox=True)
    size = (bbox[3] - bbox[0])*1.1
    for i in pm.selected():
        crv1 = pm.circle(n = 'IK%s'%i, nr = [1, 0, 0], ch = 0, r = 1)[0]
        crv2 = pm.circle(n = 'IK%s2'%i, nr = [0, 1, 0], ch = 0, r = 1)[0]
        crv3 = pm.circle(n = 'IK%s3'%i, nr = [0, 0, 1], ch = 0, r = 1)[0]
        
        pm.parent(crv2.getShape(), crv3.getShape(), crv1, add = 1, shape = 1)
        pm.delete(crv2, crv3)
        
        for s in pm.listRelatives(crv1, s = 1):
            s.overrideEnabled.set(True)
            s.overrideColor.set(color)
            
        extra = pm.group(n = 'Extra%s'%crv1, em = 1)
        offset = pm.group(n = 'Offset%s'%crv1, em = 1)
        
        for ci, c in enumerate(pm.listRelatives(crv1, s = 1)):
            c.rename('%sShape%s'%(crv1, ci + 1))
        
        pm.parent(extra, offset)
        pm.parent(crv1, extra)
        pm.delete(pm.parentConstraint(i, offset))
        pc = pm.parentConstraint(crv1, i)
        
        crv1 = crv1.rename('IK%s'%i.replace('_loc', '_ctrl'))
        pm.select(crv1 + ".cv[*]", r=1)
        pm.scale(size, size, size )
        extra = extra.rename('IK%s'%i.replace('_loc', '_drv'))
        offset = offset.rename('IK%s'%i.replace('_loc', '_grp'))
        
        ctrlGrps.append(offset)
        
    return ctrlGrps

def createNurbsIKFKAttachToCurve(rig, inputMotionPathCrv, baseCrv, offsetGrps, numMotionPathCtrls):
    motionPathCrv = inputMotionPathCrv
    
    pm.rebuildCurve(motionPathCrv, ch = 0, rpo = 1, rt = 0, end = 1, kr = 0, kcp = 0, kep = 1, kt = 0, s = numMotionPathCtrls - 3, d = 3, tol = 0.01)
    
    motionPathUpCrv = pm.duplicate(motionPathCrv)[0]

    motionPath = pm.duplicate(baseCrv, n = '%s_motionPath'%rig.name)[0]
    upVectorPath = pm.duplicate(baseCrv, n = '%s_up_motionPath'%rig.name)[0]

    for cv in motionPathUpCrv.cv:
        pos = pm.xform(cv, q = 1, ws = 1, t = 1)
        pm.xform(cv, ws = 1, t = [pos[0], pos[1] + .01, pos[2]])
    for cv in upVectorPath.cv:
        pos = pm.xform(cv, q = 1, ws = 1, t = 1)
        pm.xform(cv, ws = 1, t = [pos[0], pos[1] + .01, pos[2]])

    pm.parent(motionPath, upVectorPath, w = 1)
    pm.reverseCurve(motionPath, ch = 0, rpo = 1)
    pm.reverseCurve(upVectorPath, ch = 0, rpo = 1)
    
    pm.rebuildCurve(motionPath, ch = 0, rpo = 1, rt = 0, end = 1, kr = 0, kcp = 0, kep = 1, kt = 0, s = len(pm.PyNode(motionPathCrv).cv) - 3, d = 3, tol = 0.01)
    pm.rebuildCurve(upVectorPath, ch = 0, rpo = 1, rt = 0, end = 1, kr = 0, kcp = 0, kep = 1, kt = 0, s = len(pm.PyNode(motionPathCrv).cv) - 3, d = 3, tol = 0.01)

    bs1 = pm.blendShape(motionPathCrv, motionPath)[0]
    bs2 = pm.blendShape(motionPathUpCrv, upVectorPath)[0]

    prs = getNearestParamOnCurve(motionPath, [pm.xform(tr, q = 1, ws = 1, t = 1) for tr in offsetGrps])
    arcNode = pm.arclen(motionPath, ch = 1)
    upVecArcNode = pm.arclen(upVectorPath, ch = 1)

    mul = pm.createNode('multDoubleLinear')
    mul.input2.set(0.01)
    pm.connectAttr('%s.go'%rig.rigGrp, mul.input1)

    for i, (offset, pr) in enumerate(zip(offsetGrps, prs)):
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
            if not mel.eval('attributeExists "org_%s" "%s"'%(attr, offset)):
                pm.addAttr(offset, ln = 'org_%s'%attr, at = 'double', k = 1)
            pm.setAttr('%s.org_%s'%(offset, attr), pm.getAttr('%s.%s'%(offset, attr)))

        loc = pm.spaceLocator(n = '%s_pos%s_loc'%(rig.name, i))
        upLoc = pm.spaceLocator(n = '%s_up%s_loc'%(rig.name, i))
        motionPathNode = makeTransformAttachToCurve(motionPath, arcNode, loc, pr, mul.output)
        makeTransformAttachToCurve(upVectorPath, upVecArcNode, upLoc, pr, mul.output)

        motionPathNode.worldUpType.set(1)
        upLoc.worldMatrix >> motionPathNode.worldUpMatrix

        pm.parentConstraint(loc, offset, mo = 1)

        pm.parent(loc, upLoc, rig.locGrp)

    bs1.w[0].set(1)
    bs2.w[0].set(1)

    pm.parent(motionPath, upVectorPath, rig.crvGrp)
    pm.parent(motionPathCrv, motionPathUpCrv, rig.crvGrp)

    upVectorPath.ty.set(0)

    return pm.PyNode(motionPathCrv), pm.PyNode(motionPathUpCrv)
    
def createReferenceCurveCtrls(rig, motionPath, upVectorPath):
    ctrlLocs = []
    for i in range(len(motionPath.cv)):
        bCluster = pm.cluster(motionPath.cv[i], n = '%s_cv%s_cluster'%(motionPath, i))
        upCluster = pm.cluster(upVectorPath.cv[i], n = '%s_cv%s_cluster'%(upVectorPath, i))
        
        loc = pm.spaceLocator(n = '%s_cv%s_loc'%(rig.name, i))
        pm.delete(pm.parentConstraint(bCluster, loc))
        
        pm.parentConstraint(loc, bCluster, mo = 1)
        pm.parentConstraint(loc, upCluster, mo = 1)
        
        pm.parent(loc, rig.locGrp)
        pm.parent(bCluster, upCluster, rig.clusterGrp)
        
        ctrlLocs.append(loc)
        
    pm.select(ctrlLocs)
    pm.parent(createIkCtrls(), rig.ctrlGrp)

class mwnd():
    WND = 'NURBSIKFK_ATTATCH_WND'
    LD_CTRL_BC = 'NURBSIKFKATTACH_LOADCTRL'
    LD_CURVES_BC = 'NURBSIKFKATTACH_LOADCURVES'
    NUM_CTRLS_SLIDER = 'NURBSIKFKATTACH_NUMCTRLS'
    RIG_NAME = 'NURBSIKFKATTACH_NAME'
    
    def __init__(self):
        if pm.window(self.WND, q = 1, ex = 1):
            pm.deleteUI(self.WND)
        if pm.windowPref(self.WND, q = 1, ex = 1):
            pm.windowPref(self.WND, r = 1)
        
        pm.window(self.WND, t = 'MotionPath', w = 330, h = 1)
        pm.columnLayout(adj = 1)
        pm.rowColumnLayout(nc = 2)
        pm.text(l = ' Rig ')
        pm.textField(self.RIG_NAME)
        pm.text(l = ' NumberOfCtrls ')
        pm.intSliderGrp(self.NUM_CTRLS_SLIDER, f = 1, minValue = 5, maxValue = 100, fieldMinValue = 5, fieldMaxValue = 1000, v = 5)
        pm.setParent('..')
        pm.setParent('..')
        
        pm.columnLayout(adj = 1, w = 330)
        pm.textFieldButtonGrp(self.LD_CTRL_BC, bl = '      Control       ', bc = __class__.loadControl)
        pm.textFieldButtonGrp(self.LD_CURVES_BC, bl = '  Motion Path   ', bc = __class__.loadCurves)
        pm.setParent('..')
  
        pm.rowColumnLayout(nc = 3, w = 330)
        pm.button(l = 'Attach', w = 164, c = lambda *args : __class__.attach(), bgc = [0, 1, 0])
        pm.text(' ')
        pm.button(l = 'Detach', w = 164, c = lambda *args : __class__.detach(), bgc = [1, 0, 0])
        pm.setParent('..')

    def show(self):
        pm.showWindow(self.WND)
        
    @classmethod
    def loadControl(cls):
        pm.textFieldButtonGrp(cls.LD_CTRL_BC, e = 1, text = pm.selected()[0])
        
    @classmethod
    def loadCurves(cls):
        pm.textFieldButtonGrp(cls.LD_CURVES_BC, e = 1, text = pm.selected()[0])
        
    @classmethod
    def attach(cls):
        name = pm.textField(cls.RIG_NAME, q = 1, text = 1)
        ctrl = pm.textFieldButtonGrp(cls.LD_CTRL_BC, q = 1, text = 1)
        inputMotionPathCrv = pm.textFieldButtonGrp(cls.LD_CURVES_BC, q = 1, text = 1)
        numberOfCtrls = pm.intSliderGrp(cls.NUM_CTRLS_SLIDER, q = 1, v = 1)
        
        rig = createMotionPathAttachRig(name)
        rig.name = name
        
        baseCrv = findNurbsIKFKBaseCrv(ctrl)

        offsetGrps = findNurbsIKFKCtrlOffsets(ctrl)
        
        motionPath, upVectorPath = createNurbsIKFKAttachToCurve(rig, inputMotionPathCrv, baseCrv, offsetGrps, numberOfCtrls)
        createReferenceCurveCtrls(rig, motionPath, upVectorPath)

        upVectorPath.v.set(0)
        motionPath.overrideEnabled.set(1)
        motionPath.overrideDisplayType.set(1)

        pm.select(cl = 1)

    @classmethod
    def detach(cls):
        ctrl = pm.textFieldButtonGrp(cls.LD_CTRL_BC, q = 1, text = 1)
        offsetGrps = findNurbsIKFKCtrlOffsets(ctrl)
        
        offsets = []
        parentConstraints = []
        
        for tr in offsetGrps:
            if pm.objectType(tr) == 'parentConstraint':
                parentConstraints.append(tr)
            else:
                offsets.append(tr)
                
        loc = pm.parentConstraint(parentConstraints[0], q = 1, tl = 1)[0]
        motionPathCrv = pm.listConnections(pm.listConnections(loc.rx)[0].geometryPath)[0]
        orgMotionPath = pm.listConnections('%s.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget'%pm.listConnections(motionPathCrv.create)[0])[0]
        orgMotionPath.overrideDisplayType.set(0)
        pm.parent(orgMotionPath, w = 1)
        pm.mel.eval('DeleteHistory')
        
        pm.delete(parentConstraints)
        pm.delete(loc.getParent().getParent())

        for offset in offsets:
            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                try:
                    pm.setAttr('%s.%s'%(offset, attr), pm.getAttr('%s.org_%s'%(offset, attr)))
                except:
                    pass
            
        pm.select(cl = 1)

# if __name__ == '__main__':
#     wnd = mwnd()
#     wnd.show()
