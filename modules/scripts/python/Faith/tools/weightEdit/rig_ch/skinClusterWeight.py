# Embedded file name: \\yuweijun\E\JunCmds\tool\weightEdit\rig_ch\skinClusterWeight.py
"""
v1.0 2010
v2.0 20150104
    \xe5\x8d\x87\xe7\xba\xa7\xe6\x89\xb9\xe9\x87\x8f\xe5\xaf\xbc\xe5\x87\xba\xe6\x97\xb6\xe9\x83\xa8\xe5\x88\x86\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x87\xba\xe9\x94\x99\xe7\x9a\x84\xe9\x97\xae\xe9\xa2\x98


Blog: http://blog.sina.com.cn/u/2364869810
Email:51962215@qq.com
#Python Command
import sys
sys.path.append(r'E:\\JunCmds')
import tool.weightEdit.rig_ch.skinClusterWeight as skWt
reload(skWt)
skWt.win()
"""
__author__ = 'ZhaoChunHai'
import maya.cmds as cmds
import re, os
from weightEdit.shared_ch.mayaPrint import MayaPrint
from weightEdit.shared_ch.searchByName import Matching
from weightEdit.shared_ch.fileDialog import FDialog

class SkinWeightImExport(MayaPrint, Matching, FDialog):

    def __init__(self):
        MayaPrint.__init__(self)
        self.mayaVersion = cmds.about(f=True)
        self.userName = os.environ['USERNAME']

    def swReturnPath(self, fileName, fileType):
        self.swPath = fileName

    def searchSkinCluster(self, mod = ''):
        if mod == '':
            selObjs = cmds.ls(sl=True, ap=1, fl=True)
            if 0 == len(selObjs):
                self.mayaError('No object or points selected!')
                return
            mod = selObjs[0]
            shape = self.searchControlShape(mod)
            if shape == None or not cmds.objExists(mod):
                self.mayaWarning('No controlPoint object')
                return
        skinNode = self.findRelatedSkinCluster(mod)
        if None == skinNode:
            self.mayaWarning("Can't fint skinCluster: %s" % mod)
            return
        else:
            return skinNode

    def moveWeightOnFollow(self, addInfo = 'L_mothConner_jnt', W01 = 0.5):
        slVertex = cmds.ls(sl=True, fl=True)
        aJot = 'jawRot_jnt'
        bJot = 'jaw_jnt'
        for vtx in slVertex:
            valus = cmds.skinPercent('skinCluster1', vtx, query=True, value=True)
            trans = cmds.skinPercent('skinCluster1', vtx, query=True, t=None)
            idxA = trans.index(aJot)
            idxB = trans.index(bJot)
            idxAdd = trans.index(addInfo)
            if valus[idxAdd] == 0.0:
                valus[idxAdd] = valus[idxA] + valus[idxB] - abs(valus[idxA] - valus[idxB])
                if valus[idxA] > valus[idxB]:
                    valus[idxA] = abs(valus[idxA] - valus[idxB])
                    valus[idxB] = 0.0
                elif valus[idxA] < valus[idxB]:
                    valus[idxB] = abs(valus[idxA] - valus[idxB])
                    valus[idxA] = 0.0
                else:
                    valus[idxA] = 0.0
                    valus[idxB] = 0.0
                transformValue = []
                for idx in range(len(valus)):
                    transformValue.append((trans[idx], valus[idx]))

                cmds.skinPercent('skinCluster1', vtx, transformValue=transformValue)

        return

    def splitWeight(self, *pointName, **flags):
        """can form proportion split skin weight.
        flag: 
        replaceStr default ["L_","R_"]
        proportion defalut [1,1]"""
        defineFlags = {'replaceStr': (['L_', 'R_'], list),
         'proportion': ([1, 1], list)}
        flagDirect = self.funtionFlag(defineFlags, **flags)
        replaceStr = flagDirect['replaceStr']
        proportion = flagDirect['proportion']
        if pointName == ():
            pointName = cmds.filterExpand(sm=31)
        if pointName == None:
            self.mayaWarning('Nothing input or no poly vertex selected.')
            return
        else:
            valueList, transList = [], []
            for ver in pointName:
                cmds.select(ver)
                skNode = self.searchSkinCluster()
                if skNode == False:
                    self.mayaWarning('Can not find skinCluster node.%s' % ver)
                    continue
                allWeightJoints = cmds.skinCluster(skNode, q=True, wi=True)
                valueList = cmds.skinPercent(skNode, ver, v=True, q=True, ib=1e-13)
                transList = cmds.skinPercent(skNode, ver, t=None, q=True, ib=1e-13)
                for jnt in allWeightJoints:
                    cmds.setAttr('%s.liw' % jnt, 1)

                for inf in transList:
                    if re.search(replaceStr[0], inf) != None:
                        targetInf = re.sub(replaceStr[0], replaceStr[1], inf)
                        if cmds.objExists(targetInf) and cmds.objExists(inf):
                            cobinWeit = cmds.skinPercent(skNode, ver, t=inf, q=True)
                            cobinWeit += cmds.skinPercent(skNode, ver, t=targetInf, q=True)
                            sum = proportion[0] + proportion[1]
                            average = float(cobinWeit) / sum
                            cmds.setAttr('%s.liw' % inf, 0)
                            cmds.setAttr('%s.liw' % targetInf, 0)
                            va = average * proportion[0]
                            vb = average * proportion[1]
                            cmds.skinPercent(skNode, ver, tv=[inf, va])
                            cmds.skinPercent(skNode, ver, tv=[targetInf, vb])
                            print skNode, ver, inf, va
                            print skNode, ver, targetInf, vb

            cmds.select(pointName)
            return

    def importPointJointWeight(self, fileName, pointJoint, mod = None):
        """Import point joint skin weight """
        if mod == None:
            sels = cmds.ls(sl=True, ap=1)
            if sels == []:
                self.mayaWarning('No one mesh input or selected')
                return
            mod = sels[0]
        skinCluster = self.searchSkinCluster(mod)
        self.fileName = fileName
        pointJoints = []
        if type(pointJoint) == str or type(pointJoint) == unicode:
            pointJoints = [pointJoint]
        elif type(pointJoint) == list:
            pointJoints = pointJoint
        else:
            raise TypeError('pointJoint must a list .')
        infs = cmds.skinCluster(skinCluster, q=True, inf=True)
        for jot in pointJoints:
            if jot not in infs:
                cmds.skinCluster(skinCluster, e=True, ai=jot, lw=True, wt=0)

        rFile = file(self.fileName, 'r')
        self.jntNumDit = {}
        vertexCount = cmds.polyEvaluate(mod, v=True) - 1
        amount = 0
        cmds.progressWindow(title='Impoting Weight V1.1 ...', progress=amount, max=vertexCount, status='Progress: -/-', isInterruptable=True)
        for line in rFile:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            if re.search('^#|^\n|^\r|^ ', line) != None:
                continue
            line = re.sub('\n|\r', '', line)
            if line[0:8] == 'deformer':
                lineList = line.split(' ', 2)
                self.jntNumDit[lineList[1]] = lineList[2]
            else:
                strA = line.split(':  ', 1)
                vertex = strA[0]
                if int(vertex) > vertexCount:
                    break
                transformValue = strA[1].split(' ')
                total = 0.0
                for i in range(0, len(transformValue), 2):
                    for jnt in pointJoints:
                        transformValueList = []
                        vWet = float('%0.5f' % float(transformValue[i + 1]))
                        if self.jntNumDit[transformValue[i]] == jnt:
                            vertexName = '%s.vtx[%s]' % (mod, vertex)
                            transformValueList.append((self.jntNumDit[transformValue[i]], vWet))
                            cmds.skinPercent(skinCluster, vertexName, tv=transformValueList)

                amount += 1
                cmds.progressWindow(edit=True, progress=amount, status='Progress: %s/%s' % (amount, vertexCount))

        rFile.close()
        cmds.progressWindow(endProgress=True)
        self.mayaPrint(' Rewrite skinCluster weight from %s\n' % self.fileName)
        return

    def importSelPointsWeight(self):
        cmds.ls(sl=True, fl=True)

    def exportSkinWeight(self, mod, fileName = None):
        """mod : alist of one geo or vertexs
        export skin cluster weight
        """
        shape = self.searchControlShape(mod)
        objType = cmds.objectType(shape)
        if 'mesh' == objType:
            polygon = cmds.filterExpand(mod, sm=12)
            vertice = cmds.filterExpand(mod, sm=31)
            if None != polygon:
                self.exportMeshSkinWeight(polygon[0], fileName)
            elif None != vertice:
                self.exportMeshSelPointWeight(vertice, fileName)
        elif 'nurbsCurve' == objType:
            self.exportCurveSkinWeight(mod[0], fileName)
        elif 'nurbsSurface' == objType:
            self.exporpSufsSkinWeight(mod[0], fileName)
        elif 'lattice' == objType:
            self.exportLatticeSkinWeight(mod[0], fileName)
        return

    def exportMeshSkinWeight(self, mod, fileName = None):
        """----export selected mesh skinCluster weight----"""
        if fileName == None:
            fileName = self.fileDialog(m=1, ft='*.w')
            if fileName == [] or fileName == None:
                return False
        else:
            fileName = [fileName]
        skinCluster = self.searchSkinCluster(mod)
        if None == skinCluster:
            return
        else:
            fileName = re.sub('\\.w$', '', fileName[0])
            wFile = file(fileName + '.w', 'w')
            wFile.write('#Mesh skinWeight file <%s> CreateBy:%s written by Maya %s\n\n' % (skinCluster, self.userName, self.mayaVersion))
            skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
            self.jntNumDit = {}
            for i, joint in enumerate(skinJoints):
                wFile.write('%s %s %s\n' % ('deformer', i, joint))
                self.jntNumDit[joint] = i

            wFile.write('\n')
            number = cmds.polyEvaluate(mod, v=True)
            for i in range(number):
                wFile.write('%s: ' % i)
                infJnt = cmds.skinPercent(skinCluster, '%s.vtx[%s]' % (mod, i), ignoreBelow=1e-05, query=True, t=None)
                jntWet = cmds.skinPercent(skinCluster, '%s.vtx[%s]' % (mod, i), ignoreBelow=1e-05, query=True, v=True)
                totalWeight = 0.0
                for n, jnt in enumerate(infJnt):
                    toStr = '%0.5f' % jntWet[n]
                    rWeit = float(toStr)
                    if n == len(infJnt) - 1:
                        wFile.write(' %s %0.5f' % (self.jntNumDit[jnt], 1.0 - totalWeight))
                    else:
                        totalWeight += rWeit
                        wFile.write(' %s %s' % (self.jntNumDit[jnt], toStr))

                wFile.write('\n')

            wFile.close()
            self.mayaPrint(' %s.w\n' % fileName)
            return

    def exportMeshSelPointWeight(self, points, fileName = None):
        """----export selected vertexs skinCluster weight----"""
        if type(points) == str:
            points = self.changeStrToList(points)
        skinCluster = self.searchSkinCluster(points)
        if skinCluster == None:
            return
        elif points == None or points == []:
            self.mayaWarning('No vertex selected...')
            return
        else:
            if fileName == None:
                swPath = self.fileDialog(m=1, ft='*.evw')
                if swPath == [] or swPath == None:
                    return False
            eswFile = re.sub('\\.evw$', '', swPath[0])
            wFile = file(eswFile + '.evw', 'w')
            wFile.write('#mesh skin weight file, written by Maya %s\n\n' % (self.mayaVersion,))
            skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
            jntNumDit = {}
            for i, joint in enumerate(skinJoints):
                wFile.write('%s %s %s\n' % ('deformer', i, joint))
                jntNumDit[joint] = i

            wFile.write('\n')
            for x in points:
                reSpStr = re.split('\\[|\\]', x)
                wFile.write('%s: ' % reSpStr[1])
                infJnt = cmds.skinPercent(skinCluster, x, ignoreBelow=1e-05, query=True, t=None)
                jntWet = cmds.skinPercent(skinCluster, x, ignoreBelow=1e-05, query=True, v=True)
                for n, jnt in enumerate(infJnt):
                    wFile.write(' %s %s' % (jntNumDit[jnt], jntWet[n]))

                wFile.write('\n')

            wFile.close()
            self.mayaPrint('Write SkinWeight by selected vertex <%s.evw>.' % eswFile)
            return

    def exportCurveSkinWeight(self, mod, fileName = None):
        """----export nurbsCurve skinCluster weight----"""
        if fileName == None:
            fileName = self.fileDialog(m=1, ft='*.w')
            if fileName == [] or fileName == None:
                return False
        else:
            fileName = [fileName]
        skinCluster = self.searchSkinCluster(mod)
        if skinCluster == None:
            return
        else:
            fileName = re.sub('\\.w$', '', fileName[0])
            wFile = file(fileName + '.w', 'w')
            wFile.write('#NurbsCurve skinWeight file <%s> CreateBy:%s written by Maya %s\n\n' % (skinCluster, self.userName, self.mayaVersion))
            skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
            self.jntNumDit = {}
            for i, joint in enumerate(skinJoints):
                wFile.write('%s %s %s\n' % ('deformer', i, joint))
                self.jntNumDit[joint] = i

            wFile.write('\n')
            shape = self.searchControlShape(mod)
            number = cmds.getAttr('%s.degree' % shape) + cmds.getAttr('%s.spans' % shape)
            for i in range(number):
                wFile.write('%s: ' % i)
                infJnt = cmds.skinPercent(skinCluster, '%s.cv[%s]' % (mod, i), ignoreBelow=1e-05, query=True, t=None)
                jntWet = cmds.skinPercent(skinCluster, '%s.cv[%s]' % (mod, i), ignoreBelow=1e-05, query=True, v=True)
                totalWeight = 0.0
                for n, jnt in enumerate(infJnt):
                    toStr = '%0.5f' % jntWet[n]
                    rWeit = float(toStr)
                    if n == len(infJnt) - 1:
                        wFile.write(' %s %0.5f' % (self.jntNumDit[jnt], 1.0 - totalWeight))
                    else:
                        totalWeight += rWeit
                        wFile.write(' %s %s' % (self.jntNumDit[jnt], toStr))

                wFile.write('\n')

            wFile.close()
            self.mayaPrint(' %s.w\n' % fileName)
            return

    def exportLatticeSkinWeight(self, mod, fileName = None):
        """----export lattice skinCluster weight----"""
        if fileName == None:
            fileName = self.fileDialog(m=1, ft='*.w')
            if fileName == [] or fileName == None:
                return False
        else:
            fileName = [fileName]
        skinCluster = self.searchSkinCluster(mod)
        if skinCluster == None:
            return
        else:
            fileName = re.sub('\\.w$', '', fileName[0])
            wFile = file(fileName + '.w', 'w')
            wFile.write('#Lattice skinWeight file <%s> CreateBy:%s written by Maya %s\n\n' % (skinCluster, self.userName, self.mayaVersion))
            skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
            self.jntNumDit = {}
            for i, joint in enumerate(skinJoints):
                wFile.write('%s %s %s\n' % ('deformer', i, joint))
                self.jntNumDit[joint] = i

            wFile.write('\n')
            shape = self.searchControlShape(mod)
            sds = cmds.getAttr('%s.sDivisions' % shape)
            tds = cmds.getAttr('%s.tDivisions' % shape)
            uds = cmds.getAttr('%s.uDivisions' % shape)
            for sd in range(sds):
                for td in range(tds):
                    for ud in range(uds):
                        wFile.write('[%d][%d][%d]: ' % (sd, td, ud))
                        infJnt = cmds.skinPercent(skinCluster, '%s.pt[%d][%d][%d]' % (mod,
                         sd,
                         td,
                         ud), ignoreBelow=1e-05, query=True, t=None)
                        jntWet = cmds.skinPercent(skinCluster, '%s.pt[%d][%d][%d]' % (mod,
                         sd,
                         td,
                         ud), ignoreBelow=1e-05, query=True, v=True)
                        totalWeight = 0.0
                        for n, jnt in enumerate(infJnt):
                            toStr = '%0.5f' % jntWet[n]
                            rWeit = float(toStr)
                            if n == len(infJnt) - 1:
                                wFile.write(' %s %0.5f' % (self.jntNumDit[jnt], 1.0 - totalWeight))
                            else:
                                totalWeight += rWeit
                                wFile.write(' %s %s' % (self.jntNumDit[jnt], toStr))

                        wFile.write('\n')

            wFile.close()
            self.mayaPrint(' %s.w\n' % fileName)
            return

    def exporpSufsSkinWeight(self, mod, fileName = None):
        """----export nurbsSurface skinCluster weight----"""
        if fileName == None:
            fileName = self.fileDialog(m=1, ft='*.w')
            if fileName == [] or fileName == None:
                return False
        else:
            fileName = [fileName]
        skinCluster = self.searchSkinCluster(mod)
        if skinCluster == None:
            return
        else:
            fileName = re.sub('\\.w$', '', fileName[0])
            wFile = file(fileName + '.w', 'w')
            wFile.write('#NurbsSurface skinWeight file <%s> CreateBy:%s written by Maya %s\n\n' % (skinCluster, self.userName, self.mayaVersion))
            skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
            self.jntNumDit = {}
            for i, joint in enumerate(skinJoints):
                wFile.write('%s %s %s\n' % ('deformer', i, joint))
                self.jntNumDit[joint] = i

            wFile.write('\n')
            shape = self.searchControlShape(mod)
            numberU = cmds.getAttr('%s.su' % shape) + cmds.getAttr('%s.du' % shape)
            numberV = cmds.getAttr('%s.sv' % shape) + cmds.getAttr('%s.dv' % shape)
            for u in range(numberU):
                for v in range(numberV):
                    wFile.write('[%s][%s]: ' % (u, v))
                    infJnt = cmds.skinPercent(skinCluster, '%s.cv[%s][%s]' % (mod, u, v), ignoreBelow=1e-05, query=True, t=None)
                    jntWet = cmds.skinPercent(skinCluster, '%s.cv[%s][%s]' % (mod, u, v), ignoreBelow=1e-05, query=True, v=True)
                    totalWeight = 0.0
                    for n, jnt in enumerate(infJnt):
                        toStr = '%0.5f' % jntWet[n]
                        rWeit = float(toStr)
                        if n == len(infJnt) - 1:
                            wFile.write(' %s %0.5f' % (self.jntNumDit[jnt], 1.0 - totalWeight))
                        else:
                            totalWeight += rWeit
                            wFile.write(' %s %s' % (self.jntNumDit[jnt], toStr))

                    wFile.write('\n')

            wFile.close()
            self.mayaPrint(' %s.w\n' % fileName)
            return

    def importSkinWeight(self, fileName, mod, subs = {}):
        """import SkinWeight """
        if self.checkSkJoint(fileName, subs) == False:
            return
        else:
            skinCluster = self.searchSkinCluster(mod)
            shape = self.searchControlShape(mod)
            if skinCluster == None and shape != None:
                skinCluster = cmds.skinCluster(self.getInfsFrom_w(fileName, subs), mod, sm=0, tsb=True)
            objType = cmds.objectType(shape)
            curtInfs = cmds.skinCluster(skinCluster, q=True, inf=True)
            wetsInfs = self.getInfsFrom_w(fileName, subs)
            for inf in curtInfs:
                if inf in wetsInfs:
                    wetsInfs.remove(inf)

            if len(wetsInfs) > 0:
                cmds.skinCluster(skinCluster, e=True, dr=4, lw=False, wt=0, ai=wetsInfs)
            curtInfs = cmds.skinCluster(skinCluster, q=True, inf=True)
            for jot in curtInfs:
                cmds.setAttr('%s.liw' % jot, 0)

            shape = self.searchControlShape(mod)
            objType = cmds.objectType(shape)
            if 'mesh' == objType:
                self.importMeshSkinWeight(fileName, mod, subs)
            elif 'nurbsCurve' == objType:
                self.importCurveSkinWeight(fileName, mod)
            elif 'nurbsSurface' == objType:
                self.importSufsSkinWeight(fileName, mod)
            elif 'lattice' == objType:
                self.importLatticeSkinWeight(fileName, mod)
            self.mayaPrint(' Rewrite <%s> skinCluster weight from %s.' % (mod, fileName))
            return

    def importMeshSkinWeight(self, fileName, mod, subs = {}):
        rFile = file(fileName, 'r')
        self.jntNumDit = {}
        skinCluster = self.searchSkinCluster(mod)
        vertexCount = cmds.polyEvaluate(mod, v=True) - 1
        amount = 0
        cmds.progressWindow(title='MDL:%s' % mod, progress=amount, max=vertexCount, status='Import weight: -/-', isInterruptable=True)
        for line in rFile:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            if re.search('^#|^\n|^\r|^ ', line) != None:
                continue
            line = re.sub('\n|\r', '', line)
            if line[0:8] == 'deformer':
                lineList = line.split(' ', 2)
                jotName = self.getSubName(lineList[2], subs)
                self.jntNumDit[lineList[1]] = jotName
            else:
                strA = line.split(':  ', 1)
                vertex = strA[0]
                weights = strA[1].split(' ')
                weightsList = []
                total = 0.0
                for i in range(0, len(weights), 2):
                    vWet = round(eval(weights[i + 1]), 5)
                    if i == len(weights) - 2:
                        weightsList.append((self.jntNumDit[weights[i]], 1.0 - total))
                    else:
                        total += vWet
                        weightsList.append((self.jntNumDit[weights[i]], vWet))

                cmds.skinPercent(skinCluster, '%s.vtx[%s]' % (mod, vertex), transformValue=weightsList)
                amount += 1
                cmds.progressWindow(edit=True, progress=amount, status='Import weight: %s/%s' % (amount, vertexCount))

        cmds.progressWindow(endProgress=True)
        rFile.close()
        return

    def importCurveSkinWeight(self, fileName, mod):
        """import nurbs curve skin weight"""
        rFile = file(fileName, 'r')
        self.jntNumDit = {}
        skinCluster = self.searchSkinCluster(mod)
        shape = self.searchControlShape(mod)
        number = cmds.getAttr('%s.degree' % shape) + cmds.getAttr('%s.spans' % shape)
        amount = 0
        cmds.progressWindow(title='MDL:%s' % mod, progress=amount, max=number, status='Import weight: -/-', isInterruptable=True)
        for line in rFile:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            if re.search('^#|^\n|^\r|^ ', line) != None:
                continue
            line = re.sub('\n|\r', '', line)
            if line[0:8] == 'deformer':
                lineList = line.split(' ', 2)
                self.jntNumDit[lineList[1]] = lineList[2]
            else:
                strA = line.split(':  ', 1)
                vertex = strA[0]
                weights = strA[1].split(' ')
                weightsList = []
                total = 0.0
                for i in range(0, len(weights), 2):
                    vWet = round(eval(weights[i + 1]), 5)
                    if i == len(weights) - 2:
                        weightsList.append((self.jntNumDit[weights[i]], 1.0 - total))
                    else:
                        total += vWet
                        weightsList.append((self.jntNumDit[weights[i]], vWet))

                cmds.skinPercent(skinCluster, '%s.cv[%s]' % (mod, vertex), transformValue=weightsList)
                amount += 1
                cmds.progressWindow(edit=True, progress=amount, status='Import weight: %s/%s' % (amount, number))

        rFile.close()
        cmds.progressWindow(endProgress=True)
        return

    def importSufsSkinWeight(self, fileName, mod):
        """import nurbs curve skin weight"""
        rFile = file(fileName, 'r')
        self.jntNumDit = {}
        skinCluster = self.searchSkinCluster(mod)
        shape = self.searchControlShape(mod)
        numberU = cmds.getAttr('%s.su' % shape) + cmds.getAttr('%s.du' % shape)
        numberV = cmds.getAttr('%s.sv' % shape) + cmds.getAttr('%s.dv' % shape)
        amount = 0
        cmds.progressWindow(title='MDL:%s' % mod, progress=amount, max=numberU * numberV, status='Import weight: -/-', isInterruptable=True)
        for line in rFile:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            if re.search('^#|^\n|^\r|^ ', line) != None:
                continue
            line = re.sub('\n|\r', '', line)
            if line[0:8] == 'deformer':
                lineList = line.split(' ', 2)
                self.jntNumDit[lineList[1]] = lineList[2]
            else:
                strA = line.split(':  ', 1)
                vertex = strA[0]
                weights = strA[1].split(' ')
                weightsList = []
                total = 0.0
                for i in range(0, len(weights), 2):
                    vWet = round(eval(weights[i + 1]), 5)
                    if i == len(weights) - 2:
                        weightsList.append((self.jntNumDit[weights[i]], 1.0 - total))
                    else:
                        total += vWet
                        weightsList.append((self.jntNumDit[weights[i]], vWet))

                cmds.skinPercent(skinCluster, '%s.cv%s' % (mod, vertex), transformValue=weightsList)
                amount += 1
                cmds.progressWindow(edit=True, progress=amount, status='Import weight: %s/%s' % (amount, numberU * numberV))

        rFile.close()
        cmds.progressWindow(endProgress=True)
        return

    def importLatticeSkinWeight(self, fileName, mod):
        """import nurbs curve skin weight"""
        rFile = file(fileName, 'r')
        self.jntNumDit = {}
        skinCluster = self.searchSkinCluster(mod)
        shape = self.searchControlShape(mod)
        sds = cmds.getAttr('%s.sDivisions' % shape)
        tds = cmds.getAttr('%s.tDivisions' % shape)
        uds = cmds.getAttr('%s.uDivisions' % shape)
        number = sds * tds * uds
        amount = 0
        cmds.progressWindow(title='MDL:%s' % mod, progress=amount, max=number, status='Import weight: -/-', isInterruptable=True)
        for line in rFile:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            if re.search('^#|^\n|^\r|^ ', line) != None:
                continue
            line = re.sub('\n|\r', '', line)
            if line[0:8] == 'deformer':
                lineList = line.split(' ', 2)
                self.jntNumDit[lineList[1]] = lineList[2]
            else:
                strA = line.split(':  ', 1)
                vertex = strA[0]
                weights = strA[1].split(' ')
                weightsList = []
                total = 0.0
                for i in range(0, len(weights), 2):
                    vWet = round(eval(weights[i + 1]), 5)
                    if i == len(weights) - 2:
                        weightsList.append((self.jntNumDit[weights[i]], 1.0 - total))
                    else:
                        total += vWet
                        weightsList.append((self.jntNumDit[weights[i]], vWet))

                cmds.skinPercent(skinCluster, '%s.pt%s' % (mod, vertex), transformValue=weightsList)
                amount += 1
                cmds.progressWindow(edit=True, progress=amount, status='Import weight: %s/%s' % (amount, number))

        rFile.close()
        cmds.progressWindow(endProgress=True)
        return

    def batchExportSkinWeight(self):
        """batch Export SkinWeight in folder"""
        suptObjs = []
        filGeos = cmds.filterExpand(sm=[9, 10, 12])
        if filGeos != None:
            suptObjs.extend(filGeos)
        sels = cmds.ls(sl=True)
        for x in sels:
            shape = self.searchControlShape(x)
            if shape == None:
                continue
            objType = cmds.objectType(shape)
            if 'lattice' == objType and x not in suptObjs:
                suptObjs.append(x)

        if len(suptObjs) == []:
            self.mayaWarning('None support objects selected.')
            return False
        else:
            selFolder = self.fileDialog(m=4, okc='Select')
            if selFolder == None or selFolder == []:
                return False
            for geo in suptObjs:
                try:
                    self.exportSkinWeight([geo], '%s/%s' % (selFolder[0], geo))
                except:
                    self.mayaWarning('%s: export skin weight Failure.' % geo)

            return

    def batchImportSkinWeight(self, path = None):
        """batch Import SkinWeight from folder"""
        selFolder = [path]
        if path == None:
            selFolder = self.fileDialog(m=4, okc='Select')
            if selFolder == [] or selFolder == None:
                return False
        allFiles = os.listdir(selFolder[0])
        for f in allFiles:
            fileName = os.path.join(selFolder[0], f)
            if os.path.isfile(fileName) and re.search('\\.w$|\\.evw$', f) != None:
                name = os.path.splitext(f)
                if cmds.objExists(name[0]):
                    skined = self.searchSkinCluster(name[0])
                    if skined == None:
                        cmds.skinCluster(self.getInfsFrom_w(fileName), name[0], sm=0, tsb=True)
                    cmds.select(name[0])
                    cmds.refresh(f=True)
                    try:
                        self.importSkinWeight(fileName, name[0])
                    except:
                        self.mayaWarning('%s: import skin weight Failure.' % name[0])

        return

    def importSeldPntWet(self):
        pass

    def getSubName(self, oriName, subsDirt = {}):
        """replace oriName from subsDirt"""
        if subsDirt == {}:
            return oriName
        elif oriName in subsDirt:
            return subsDirt[oriName]
        else:
            return oriName

    def getInfsFrom_w(self, fileName, subs = {}):
        if self.checkSkJoint(fileName, subs) == False:
            return
        infJnts = []
        rFile = file(self.fileName, 'r')
        for idx, line in enumerate(rFile):
            if line[0:8] == 'deformer':
                line = re.sub('\n|\r', '', line)
                lineList = line.split(' ', 2)
                jotName = self.getSubName(lineList[2], subs)
                infJnts.append(jotName)
            elif idx > 10:
                break
            else:
                continue

        rFile.close()
        return infJnts

    def selInfluenceJoint(self, fileName, printer = True):
        infs = self.getInfsFrom_w(fileName)
        cmds.select(infs)
        if printer == True:
            self.mayaPrint(' %s' % infs)
        return infs

    def checkSkJoint(self, fileName, subs = {}):
        lostSkJoint = []
        self.fileName = fileName
        self.infJnt = []
        rFile = file(self.fileName, 'r')
        for idx, line in enumerate(rFile):
            if line[0:8] == 'deformer':
                line = re.sub('\n|\r', '', line)
                lineList = line.split(' ', 2)
                jotName = self.getSubName(lineList[2], subs)
                if cmds.objExists(jotName) == 0:
                    lostSkJoint.append(jotName)
                else:
                    self.infJnt.append(jotName)
            elif idx > 10:
                break
            else:
                continue

        rFile.close()
        if lostSkJoint == []:
            return True
        else:
            self.mayaWarning('Lost skinJoint:%s' % lostSkJoint)
            return False

    def holdAllInfJoint(self):
        mod = cmds.ls(sl=True, ap=1)[0]
        skinCluster = self.searchSkinCluster()
        if skinCluster == 0:
            self.mayaWaring("Can't find skinCluster deformer.")
            return 0
        skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
        for jot in skinJoints:
            cmds.setAttr('%s.liw' % jot, 1)

        self.mayaPrint('Hold all the inf joint.')

    def unHoldAllInfJoint(self):
        mod = cmds.ls(sl=True, ap=1)[0]
        skinCluster = self.searchSkinCluster()
        if skinCluster == 0:
            self.mayaWaring("Can't find skinCluster deformer.")
            return 0
        skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
        for jot in skinJoints:
            cmds.setAttr('%s.liw' % jot, 0)

        self.mayaPrint('unHold all the inf joint.')

    def editSelInfJointHold(self, hold):
        slJots = cmds.ls(sl=True, ap=True, type='joint')
        for jot in slJots:
            if cmds.objExists('%s.liw' % jot):
                cmds.setAttr('%s.liw' % jot, hold)
                self.mayaPrint('setAttr %s.liw %d;' % (jot, hold), addResult=False)

    def resetSelectSkinPose(self):
        for obj in cmds.ls(sl=True):
            skinNode = self.findRelatedSkinCluster(obj)
            if skinNode != None:
                sk_mx = '%s.matrix' % skinNode
                mx_mi = cmds.getAttr(sk_mx, mi=True)
                infs = cmds.listConnections(sk_mx, s=True, d=False, scn=True)
                if infs != None:
                    for idx in mx_mi:
                        inf = cmds.listConnections('%s[%d]' % (sk_mx, idx), s=True, d=False, scn=True)
                        if inf == None:
                            continue
                        matrix = cmds.getAttr('%s.worldInverseMatrix[0]' % inf[0])
                        cmds.setAttr('%s.pm[%d]' % (skinNode, idx), matrix, type='matrix')

        return

    def importPointJointWeightTool(self):
        """
        """

        def setIPJWPath():
            path = self.fileDialog(m=0)
            if path != None:
                cmds.textFieldButtonGrp(skWt_tfbg, e=True, text=path[0])
            return

        def doImport():
            mesh = cmds.textFieldButtonGrp(skms_tfbg, q=True, text=True)
            if mesh == '' or not cmds.objExists(mesh):
                self.mayaWarning('No one mesh loaded.')
                return
            infs = cmds.textFieldButtonGrp(skIf_tfbg, q=True, text=True)
            if infs == '':
                self.mayaWarning('No one inf joint loaded.')
                return
            path = cmds.textFieldButtonGrp(skWt_tfbg, q=True, text=True)
            if path == '':
                self.mayaWarning('No path loaded.')
                return
            for jot in re.split(';', infs):
                self.importPointJointWeight(path, jot, mesh)

        winName = 'zch_exportskw_win'
        self.closeWindow(winName)
        cmds.window(winName, t='SkinCluster Weight Tool')
        gFACWin_RootLayout = cmds.columnLayout(adj=1)
        cmds.frameLayout(label='mportPointJointWeight...', collapsable=1)
        cmds.columnLayout(adj=1)
        skms_tfbg = cmds.textFieldButtonGrp(label='Skined Mesh:', buttonLabel='<< Load', bc=lambda *args: self.loadSelectedIntoButtonGrp(skms_tfbg))
        skIf_tfbg = cmds.textFieldButtonGrp(label='Which Joint:', buttonLabel='<< Load', bc=lambda *args: self.loadSelectedIntoButtonGrp(skIf_tfbg))
        skWt_tfbg = cmds.textFieldButtonGrp(label='Weight File Paht:', buttonLabel='Select', bc=lambda *args: setIPJWPath())
        cmds.button(label='Apply', c=lambda *args: doImport())
        cmds.showWindow(winName)


def win():
    winName = 'zch_skinWeight_win'
    impStr = 'import %s as skWeight\nskWeight' % __name__
    if cmds.window(winName, ex=True):
        cmds.deleteUI(winName)
    timeStamp = '2010-2015'
    showHelpCmd = "import maya.cmds;maya.cmds.showHelp('http://blog.sina.com.cn/u/2364869810',absolute=True)"
    cmds.window(winName, t='SkinCluster Weight Tool v2.0', menuBar=True)
    theMenu = cmds.menu(label='Edit', tearOff=False, allowOptionBoxes=True)
    cmds.menuItem(label='Save Seting', tearOff=False)
    cmds.menuItem(label='Reset Seting', tearOff=False)
    cmds.menuItem(divider=True)
    cmds.radioMenuItemCollection()
    cmds.menuItem(label='As Tool', rb=True, en=0)
    cmds.menuItem(label='As Action', rb=True, en=0)
    cmds.setParent(menu=True)
    cmds.menu(label='Help', tearOff=False, allowOptionBoxes=True)
    cmds.menuItem(label='Help On This Tool ...', tearOff=False, c=showHelpCmd)
    cmds.setParent(menu=True)
    rootLaytou = cmds.columnLayout(adj=1)
    cmds.separator(style='single', h=5)
    cmds.text(label='First Select The Poly Vertex')
    cmds.separator(style='none', h=3)
    cmds.textFieldGrp('splWet_searchFor_tfg', label='Search for:', text='L_')
    cmds.textFieldGrp('splWet_replaceWith_tfg', label='Replace with:', text='R_')
    cmds.floatFieldGrp('splWet_proportion_ffg', numberOfFields=2, label='Proportion:', value=[1.0,
     1.0,
     0,
     0])
    cmds.button(label='Split Seleced Vertex Skin Weight', h=30, c='%s.splitWeightCmd()' % impStr)
    cmds.separator(style='single', h=5)
    cmds.button(label='Hold All Inf Joint', c='%s.SkinWeight.holdAllInfJoint()' % impStr)
    cmds.button(label='Unhold All In Joint', c='%s.SkinWeight.unHoldAllInfJoint()' % impStr)
    cmds.separator(style='single', h=5)
    cmds.button(label='Select Skin Joint', c='%s.selectSkinJoint()' % impStr)
    cmds.button(label='Reset Select Skined Pose', c='%s.SkinWeight.resetSelectSkinPose()' % impStr)
    cmds.button(label='Get Inf Joint(from .w file)', c='%s.selFunFileDialog()' % impStr)
    cmds.separator(style='single', h=5)
    cmds.button(label='Export SkinWeight', c='%s.exportSkinClusterWeight()' % impStr)
    cmds.button(label='Import SkinWeight', c='%s.imFileDialog()' % impStr)
    cmds.button(label='Batch Export SkinWeight', c='%s.SkinWeight.batchExportSkinWeight()' % impStr)
    cmds.button(label='Batch Import SkinWeight', c='%s.SkinWeight.batchImportSkinWeight()' % impStr)
    thisLayout = cmds.frameLayout(lv=0, bs='etchedOut')
    cmds.iconTextButton(label='Copyright (C) %s Rigging TD | ChunHai Zhao' % timeStamp, style='textOnly', image='blendShape.png', h=22, al='center', c=showHelpCmd)
    cmds.setParent('..')
    cmds.showWindow(winName)


def splitWeightWin():
    winName = 'zch_splitWeight_win'
    impStr = 'import %s as skWeight\nskWeight' % __name__
    if cmds.window(winName, ex=True):
        cmds.deleteUI(winName)
    cmds.window(winName, t='SplitWeight V12/08/22')
    rootLaytou = cmds.columnLayout(adj=1)
    cmds.separator(style='none', h=5)
    cmds.text(label='First Select The Poly Vertex')
    cmds.separator(style='single', h=5)
    cmds.textFieldGrp('splWet_searchFor_tfg', label='Search for:', text='L_')
    cmds.textFieldGrp('splWet_replaceWith_tfg', label='Replace with:', text='R_')
    cmds.floatFieldGrp('splWet_proportion_ffg', numberOfFields=2, label='Proportion:', value=[1.0,
     1.0,
     0,
     0])
    cmds.button(label='Split Seleced Vertex Skin Weight', h=30, c='%s.splitWeightCmd()' % impStr)
    cmds.separator(style='single', h=5)
    cmds.text(label='(author) |Zhao ChunHai', en=0)
    cmds.separator(style='single', h=5)
    cmds.showWindow(winName)


def splitWeightCmd():
    searchFor = cmds.textFieldGrp('splWet_searchFor_tfg', q=True, text=True)
    replaceWith = cmds.textFieldGrp('splWet_replaceWith_tfg', q=True, text=True)
    v1 = cmds.floatFieldGrp('splWet_proportion_ffg', q=True, v1=True)
    v2 = cmds.floatFieldGrp('splWet_proportion_ffg', q=True, v2=True)
    SkinWeight.splitWeight(replaceStr=[searchFor, replaceWith], proportion=[v1, v2])


def exportSkinClusterWeight():
    skinNode = SkinWeight.searchSkinCluster()
    if None == skinNode:
        return
    else:
        mod = cmds.ls(sl=True, fl=True)
        if len(mod) > 0:
            SkinWeight.exportSkinWeight(mod)
        return


def selectSkinJoint():
    mod = cmds.ls(sl=True, ap=1)[0]
    skinCluster = SkinWeight.searchSkinCluster()
    if skinCluster == 0:
        return 0
    skinJoints = cmds.skinCluster(skinCluster, q=True, inf=True)
    cmds.select(skinJoints)


def importFileName(fileName, fileType):
    sl = cmds.ls(sl=True, ap=True)
    if len(sl) != 1:
        return
    mod = sl[0]
    SkinWeight.importSkinWeight(fileName, mod)


def imFileDialog():
    if SkinWeight.searchSkinCluster() == 0:
        return False
    else:
        if SkinWeight.mayaVersion < '2011':
            cmds.fileBrowserDialog(m=0, fc=importFileName, an='Import', om='Import')
        elif SkinWeight.mayaVersion >= '2011':
            setPath = cmds.fileDialog2(fm=1, okc='Import Weight', fileFilter='*.w *.evw')
            if setPath != None:
                importFileName(setPath[0], '.w')
            else:
                return
        return


def selectFunFileName(fileName, fileType):
    SkinWeight.selInfluenceJoint(fileName)


def selFunFileDialog():
    if SkinWeight.mayaVersion < '2011':
        cmds.fileBrowserDialog(m=0, fc=selectFunFileName, an='Get', om='Import')
    elif SkinWeight.mayaVersion >= '2011':
        setPath = cmds.fileDialog2(fm=1, okc='Select File', fileFilter='*.w')
        if setPath != None:
            selectFunFileName(setPath[0], '.w')
        else:
            return
    return


SkinWeight = SkinWeightImExport()