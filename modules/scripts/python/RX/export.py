import os,re,shutil

def get_pyside_module():
    try:
        from PySide2 import QtCore, QtGui, QtWidgets
        return QtCore, QtGui, QtWidgets
    except ImportError:
        try:
            from PySide6 import QtCore, QtGui, QtWidgets
            return QtCore, QtGui, QtWidgets
        except ImportError:
            raise ImportError("Neither PySide2 module nor PySide6 module could be imported.")

QtCore, QtGui, QtWidgets = get_pyside_module()

import maya.cmds as mc
import maya.mel as mel

from rxCore import aboutLock
from rxCore import aboutName
# from rxUi import export_ui

import skinClusterTools
import cluster as clusterTools
import customRigs
import assetEnv

####################
# Template Build UI

class Export(QtWidgets.QWidget):

    def __init__(self):
        super(Export, self).__init__()

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui = export_ui.Ui_exportUI()
        self.ui.setupUi(self)
        self.setObjectName ('export_ui')

        self.ui.listSelBtn.clicked.connect(self.listSelectedeGeo)
        self.ui.listModelBtn.clicked.connect(self.listModelGeo)
        self.ui.selDefBtn_2.clicked.connect(self.fixDefNames)
        self.ui.sclsChx.stateChanged.connect(self.listDeformers)
        self.ui.clsChx.stateChanged.connect(self.listDeformers)
        self.ui.ffdChx.stateChanged.connect(self.listDeformers)
        self.ui.constChx.stateChanged.connect(self.listDeformers)
        self.ui.bsChx.stateChanged.connect(self.listDeformers)
        self.ui.muscChx.stateChanged.connect(self.listDeformers)
        self.ui.sdkChx.stateChanged.connect(self.listDeformers)
        self.ui.geoList.itemSelectionChanged.connect(self.listDeformers)
        self.ui.geoList.itemSelectionChanged.connect(self.selectG)

        self.ui.geoList.itemDoubleClicked.connect(self.selectAllGeosInList)
        self.ui.defList.itemDoubleClicked.connect(self.selectAllDefsInList)

        self.ui.defFiltersGrp.clicked.connect(self.toggleDefFilterVis)
        self.ui.defOrderBtn.clicked.connect(self.exportDeformerOrder)

        self.ui.exportBtn.clicked.connect(self.exportDeformers)
        self.ui.handBuiltBtn.clicked.connect(customRigs.exportCustomRig)
        self.ui.reviewBtn.clicked.connect(unlockedAttrs)
        self.ui.reviewBtn.setText('Keyable Attributes')
        self.toggleDefFilterVis(0)

        self.reload()

        btns = [
            self.ui.defOrderBtn,
            self.ui.handBuiltBtn,
            self.ui.reviewBtn]

        for b in btns:
            b.setMinimumHeight(25)
            b.setMaximumHeight(25)

        self.ui.sclsChx.setText('Skin Clusters')
        self.ui.bsChx.setText('Blend Shapes')

        self.ui.muscChx.hide()
        self.ui.deltaChx.hide()
        self.ui.gridLayout_8.addWidget(self.ui.ffdChx, 1, 0, 1, 1)
        self.ui.gridLayout_8.addWidget(self.ui.sdkChx, 1, 1, 1, 1)

    def selectG(self):
        geoItems = self.ui.geoList.selectedItems()
        nodes = []
        for g in geoItems:
            nodes.append(g.text())
        mc.select(nodes)

    def reload(self):
        self.ui.geoList.clear()
        self.ui.defList.clear()

    def toggleDefFilterVis(self, hide=False):
        if not self.ui.defFiltersGrp.isChecked() or hide:
            self.ui.defFiltersGrp.setFlat(True)
            self.ui.defFilterFrame.setVisible(0)
            self.ui.defFiltersGrp.setChecked(0)
        else:
            self.ui.defFiltersGrp.setFlat(False)
            self.ui.defFilterFrame.setVisible(1)

    def listSelectedeGeo(self, add=False):
            sel = list(set(mc.ls(sl=1)))
            sel.sort()

            if sel:
                if not add:
                    self.ui.geoList.clear()
                for s in sel:
                    self.ui.geoList.addItem(s)
                self.ui.geoList.selectAll()

    def listModelGeo(self):
        if not mc.objExists('model'):
            return

        self.ui.geoList.clear()

        geos = [g for g in mc.listRelatives('model', ad=1, type='transform') if not 'Constraint' in mc.nodeType(g)]
        if not geos:
            return

        geos = list(set(geos))
        geos.sort()

        for geo in geos:
            self.ui.geoList.addItem(geo)
        self.ui.geoList.selectAll()

    def selectAllGeosInList(self):
        self.ui.geoList.selectAll()

    def selectAllDefsInList(self):
        self.ui.defList.selectAll()

    def fixDefNames(self):
        mc.undoInfo(ock=1)
        nodes = [i for i in [i.text().strip() for i in self.ui.defList.selectedItems()] if mc.objExists(i)]
        for node in nodes:
            ntype = mc.nodeType(node)
            try:
                if ntype == 'skinCluster':
                    skinClusterTools.fixNames(node)

                elif ntype == 'cluster':
                    geo = mc.cluster(node, q=1 , g=1)
                    if geo: geo = geo[0]
                    nn = aboutName.unique(geo+'_'+mc.cluster(node, q=1 , wn=1).replace('_ctrl', '_cls'))
                    if not node == nn:
                        mc.rename(node, nn)

                elif ntype == 'blendShape':
                    geo = mc.blendShape(node, q=1 , g=1)
                    if geo:
                        geo = mc.listRelatives(geo[0], p=1)
                        if geo: geo = geo[0]
                    nn = aboutName.unique(geo+'_bs')
                    if not node == nn:
                        mc.rename(node, nn)

                elif ntype == 'ffd':
                    geo = mc.lattice(node, q=1 , g=1)
                    if geo:
                        geo = mc.listRelatives(geo[0], p=1)
                        if geo: geo = geo[0]

                    nn = aboutName.unique(geo+'_ffd')
                    lnn = aboutName.unique(nn+'Lattice')
                    bnn = aboutName.unique(nn+'Base')

                    lshape=mc.listConnections (node+'.deformedLatticeMatrix')[0]
                    base=mc.listConnections (node+'.baseLatticeMatrix')[0]

                    if not node == nn:
                        mc.rename(node, nn)
                    if not lshape == lnn:
                        mc.rename(lshape, lnn)
                    if not base == bnn:
                        mc.rename(base, bnn)

                elif ntype == 'pointConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_pc'
                    if not node == nn: mc.rename(node, nn)
                elif ntype == 'orientConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_oc'
                    if not node == nn: mc.rename(node, nn)
                elif ntype == 'parentConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_prc'
                    if not node == nn: mc.rename(node, nn)
                elif ntype == 'scaleConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_sc'
                    if not node == nn: mc.rename(node, nn)
                elif ntype == 'poleVectorConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_pvc'
                    if not node == nn: mc.rename(node, nn)
                elif ntype == 'aimConstraint':
                    nn = mc.listConnections (node+'.constraintParentInverseMatrix')[0]+'_ac'
                    if not node == nn: mc.rename(node, nn)
            except:
                pass
        mc.undoInfo(cck=1)

        self.listDeformers()


    # lists deformers in list
    def listDeformers(self):
        self.ui.defList.clear()

        scls = self.ui.sclsChx.checkState()
        bs = self.ui.bsChx.checkState()
        cls = self.ui.clsChx.checkState()
        ffd = self.ui.ffdChx.checkState()
        musc = self.ui.muscChx.checkState()
        sdk = self.ui.sdkChx.checkState()
        const = self.ui.constChx.checkState()
        wrp = False
        nonl = False

        sclss, bss, clss, wrps, ffds, nonls, muscs, sdks, consts = [],[],[],[],[],[],[],[],[]
        geoItems = self.ui.geoList.selectedItems()
        geos = []
        for g in geoItems:
            if scls:
                defs = getDeformers(g.text(), 'skinCluster')
                if defs:
                    sclss.extend(defs)
            if cls:
                defs = getDeformers(g.text(), 'cluster')
                if defs:
                    clss.extend(defs)
            if bs:
                defs = getDeformers(g.text(), 'blendShape')
                if defs:
                    bss.extend(defs)
            if wrp:
                defs = getDeformers(g.text(), 'wrap')
                if defs:
                    wrps.extend(defs)
            if ffd:
                defs = getDeformers(g.text(), 'ffd')
                if defs:
                    ffds.extend(defs)
            if nonl:
                defs = getDeformers(g.text(), 'nonLinear')
                if defs:
                    nonls.extend(defs)
            if musc:
                defs = getDeformers(g.text(), 'cMuscleSystem')
                if defs:
                    muscs.extend(defs)
            if sdk:
                defs = getSDKs(g.text())
                if defs:
                    sdks.extend(defs)
            if const:
                defs = getConstraints(g.text())
                if defs:
                    consts.extend(defs)

        sclss = list(set(sclss))
        clss = list(set(clss))
        bss = list(set(bss))
        wrps = list(set(wrps))
        ffds = list(set(ffds))
        nonls = list(set(nonls))
        muscs = list(set(muscs))
        sdks = list(set(sdks))
        consts = list(set(consts))

        sclss.sort()
        clss.sort()
        ffds.sort()
        bss.sort()
        wrps.sort()
        nonls.sort()
        muscs.sort()
        sdks.sort()
        consts.sort()

        if sclss:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Skin Clusters')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in sclss:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if clss:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Clusters')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in clss:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if bss:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Blend Shapes')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in bss:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if ffds:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Lattices')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in ffds:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if wrps:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Wraps')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in wrps:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if nonls:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('NonLinear Deformers')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in nonls:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if muscs:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('cMuscle Skin Deformers')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in muscs:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if sdks:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Set Driven Keys')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in sdks:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        if consts:
            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText('Constraints')
            item.setForeground(QtCore.QtCore.darkGray)
            self.ui.defList.addItem(item)

            for sc in consts:
                item = QtWidgets.QListWidgetItem(self.ui.defList)
                item.setText('    '+sc)
                self.ui.defList.addItem(item)

            item = QtWidgets.QListWidgetItem(self.ui.defList)
            item.setText(' ')
            self.ui.defList.addItem(item)

        self.ui.defList.takeItem(self.ui.defList.count()-1)

    def exportDeformerOrder(self):
        rtype = assetEnv.getrigtype()

        path = os.path.join(assetEnv.getpath(), 'build', 'bind', rtype, 'stack')
        if not os.path.isdir(path):
            os.makedirs(path)

        if not os.path.isdir(path):
            mc.warning('Cannot create dir: '+path)
            return

        items = self.ui.geoList.selectedItems()
        geos = []
        for i in items:
            g = i.text()
            if mc.objExists(g) and g not in geos:
                geos.append(g)

        if geos:
            defOrder(geos, path)

    def exportDeformers(self):

        rtype = assetEnv.getrigtype()

        path = os.path.join(assetEnv.getpath(), 'build', 'bind', rtype)
        sel = self.ui.defList.selectedItems()
        geoso = self.ui.geoList.selectedItems()
        nodes = []
        for s in sel:
            node = s.text().strip()
            if mc.objExists(node):
                nodes.append(node)

        subdirs = {}
        subdirs['skinCluster'] = 'scls'
        subdirs['cluster'] = 'cls'
        subdirs['blendShape'] = 'bs'
        subdirs['wrap'] = 'wrp'
        subdirs['ffd'] = 'ffd'
        subdirs['sdk'] = 'sdk'
        subdirs['cMuscleSystem'] = 'cms'

        sdks = 0
        cons = []
        for n in nodes:
            ntype = mc.nodeType(n)
            if re.search ('animCurve', ntype):
                basepath = os.path.join(path, subdirs['sdk'])
            else:
                if ntype in subdirs.keys():
                    basepath = os.path.join(path, subdirs[ntype])
                else:
                    basepath = path

            filepath = os.path.join(basepath, n+'.mb')

            if not os.path.isdir(basepath):
                try:
                    os.makedirs(basepath)
                except:
                    mc.error('Could not create directories on disk!')

            if ntype == 'skinCluster':
                skinCluster([n], filepath)
            elif ntype =='cluster':
                cluster([n], filepath)
            elif ntype == 'blendShape':
                blendShape([n], filepath)
            elif ntype == 'ffd':
                lattice(n, filepath)
            elif ntype == 'cMuscleSystem':
                cMuscle(n, os.path.dirname(filepath))
            elif re.search ('animCurve', ntype):
                sdks = 1
            elif ntype == 'parentConstraint' or ntype == 'scaleConstraint' or ntype == 'pointConstraint'or ntype == 'orientConstraint':
                cons.append(n)

        if sdks:
            for g in geoso:
                sdk(g.text().strip(), os.path.dirname(filepath))

        if cons:
            constraints(cons, os.path.join(assetEnv.getpath(), 'build', 'scripts' ))

#################################################################
def defOrder(geos, path):

    geos = mc.ls(geos)

    for geo in geos:

        stackOrders = mc.listHistory(geo, il= 1, pdo=1)

        arg = 'import maya.mel as mm\n'
        arg += 'import os\n\n'
        if len(stackOrders) > 1:
            for i in range(len(stackOrders)-1):
                arg += 'mel.eval("catch(`reorderDeformers {0} {1} {2}`)")\n'.format(stackOrders[i], stackOrders[i+1], geo)

        arg+='print "Done"\n'
        arg += 'if os.environ["rbDEBUG"] == "False":\n' \
                '\tmc.delete(mc.ls("*_exportedWeights*", type="cluster"))\n' \
                '\tmc.delete(mc.ls("*exportedWeights_scriptNode*", type="script"))'

        scrNode = mc.scriptNode(n='exportedWeights_scriptNode', stp='python', bs=arg, st=1)
        mc.select(scrNode)

        filename = os.path.join(path, geo+'_stack.mb')
        mc.file(filename, f=1, op='', typ='mayaBinary', es=1)
        mc.delete(scrNode)

        print ('Exported Deformer Order: '+filename)
        return filename

def sdk(nodes, path, asp=False):

    nodes = mc.ls(nodes)
    for node in nodes:

        if asp:
            attributes([node], path)
        else:
            attributes([node])

        # get driven SDKd attrs
        crvs = mc.listConnections(node, s=1, d=0, p=1, scn=1,type='animCurve')
        bws = mc.listConnections(node, s=1, d=0, p=1, scn=1,type='blendWeighted')

        if not crvs:
            crvs = []
        if bws:
            crvs.extend (bws)

        if crvs:
            drivens = mc.listConnections (crvs, d=1, s=0, p=1)
            drivens = list(set(drivens))
            export = []

            # Build arg
            arg = '# Connect SDK\n'
            arg += 'import maya.cmds as mc\n'
            arg +='''

try:
    import rigtools;
    from rigtools import export
except:
    from mpc.tvcRiggingSandbox import rigtools;
    from mpc.tvcRiggingSandbox.rigtools import export\n\n'''

            arg += 'try:\n'

            # get driver, driven, SDK curve, duplicate weight, and add to arg
            for driven in drivens:

                # get sdk name
                crvs = getSDKs(driven)
                for crv in crvs:
                    driver = mc.listConnections(crv,s=1, d=0, scn=1, p=1)
                    if driver:
                        driver = driver[0]
                        if asp:
                            attributes([driver.split('.')[0]], path)
                        else:
                            attributes([driver.split('.')[0]])

                    else:
                        driver = ''

                    weight = mc.duplicate(crv, n=crv+'_weights')[0]
                    export.append(weight)
                    arg += '\texport.reconnectSDK("{0}", "{1}", "{2}")\n'.format(weight, driver, driven)

            arg += '\tprint "Reconnected SDKs for {0}"\n'.format(node)
            arg += 'except:\n\tmc.warning("Could not reconnect all SDKs for:   {0}")\n'.format(node)

            # Export
            filename = os.path.join(path, node+'_sdk.ma')
            scrNode = mc.scriptNode(n='exportedWeights_scriptNode', bs=arg, st=1, stp='python')
            mc.select(export, scrNode)
            mc.file(filename, f=1, op='', typ='mayaAscii', es=1)
            mc.delete(export, scrNode)

            print ('Exported SDKs for '+node)
            print ('Wrote SDK file to: '+filename)

def reconnectSDK(weight, driver, driven):

    # Create default sdk
    for node in [weight, driver, driven]:
        if not mc.objExists(node):
            return

    # create intial SDK
    mc.setDrivenKeyframe (driven, cd=driver)

    # Find the name of that new SDK
    crvs = mc.listConnections(driven, s=1, d=0, p=0, scn=1, type='animCurve')
    bws = mc.listConnections(driven, s=1, d=0, p=0, scn=1, type='blendWeighted')

    if not crvs:
        crvs = []
    if bws:
        for bw in bws:
            cnn = mc.listConnections(bw, s=1, d=0, p=0, scn=1, type='animCurve')
            if cnn:
                crvs.extend (cnn)

    crv = ''
    for c in crvs:
        cnn = mc.listConnections (c+'.input', d=0, s=1, scn =1, p=1)
        if cnn:
            if cnn[0] == driver:
                crv = c

    # Finad actuall connections of that SDK
    icnn = mc.listConnections(crv+'.input', s=1, d=0, p=1, scn=1)
    ocnn = mc.listConnections(crv+'.output', s=0, d=1, p=1, scn=1)

    if icnn and ocnn:
        mc.connectAttr (icnn[0], weight+'.input', f=1)
        mc.connectAttr (weight+'.output', ocnn[0], f=1)
        print ('{0} connected! {1} >> {2}'.format(weight, driver, driven))

    mc.delete (crv)
    mc.rename (weight, crv)

def constraints(nodes, path):

    arg = 'import maya.cmds as mc\n'
    arg += 'def load():\n'
    for node in nodes:

        #scale contraints
        targets = mc.listConnections (node+'.constraintParentInverseMatrix')
        drivers = mc.listConnections (node+'.target')
        while node in drivers:
            drivers.remove(node)

        drivers = list(set(drivers))
        targets = list(set(targets))

        if mc.nodeType(node)=='pointConstraint':
            arg += "    try:\n        mc.pointConstraint({0}, {1}, n='{2}', mo=1)\n".format(drivers, targets, node)
            arg += '    except:\n        print "Could not create constraint {0}"\n'.format(node)

        if mc.nodeType(node)=='orientConstraint':
            arg += "    try:\n        mc.orientConstraint({0}, {1}, n='{2}', mo=1)\n".format(drivers, targets, node)
            arg += '    except:\n        print "Could not create constraint {0}"\n'.format(node)

        if mc.nodeType(node)=='scaleConstraint':
            arg += "    try:\n        mc.scaleConstraint({0}, {1}, n='{2}', mo=1)\n".format(drivers, targets, node)
            arg += '    except:\n        print "Could not create constraint {0}"\n'.format(node)

        if mc.nodeType(node) == 'parentConstraint':
            interpType = mc.getAttr(node+'.interpType')
            arg += "    try:\n        mc.parentConstraint({0}, {1}, n='{2}', mo=1)\n".format(drivers, targets, node)
            arg += "        mc.setAttr('{0}.interpType', {1})\n".format(node, interpType)
            arg += '    except:\n        print "Could not create constraint {0}"\n'.format(node)

    rtype = assetEnv.getrigtype()

    filename = os.path.join(path, rtype+'Constraints.py')
    if os.path.isfile(filename):
        result = mc.confirmDialog( title='Overwrite Feather Build File?', message=assetEnv.getasset()+'Constraints.py already exists.\nOverwrite file?\n\n'+filename, \
                                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return
        shutil.copyfile(filename, filename+'.bak')

    f = open(filename, 'w')
    f.write(arg)
    f.close()

    print ('Wrote contraints file to: '+filename)

def lattice(node, path):

    filename = os.path.abspath(path.split('.')[0]+'.mb')

    # get geos
    geos=mc.listConnections (node+'.outputGeometry')

    # get latticeShape and base
    lshape=mc.listConnections (node+'.deformedLatticeMatrix')[0]
    base=mc.listConnections (node+'.baseLatticeMatrix')[0]

    # dup base and shspe
    ebase=mc.duplicate(base, n=base+'_weights')
    elshape=mc.duplicate(lshape, n=lshape+'_weights')

    # disconnect + delte junk
    cnn=mc.listConnections(elshape[1],d=1, p=1)
    if cnn :
        for c in cnn:
            dst=  mc.listConnections(c,s=1, p=1)
            if dst:
                for d in dst:
                    try:
                        mc.disconnectAttr(c, d)
                    except:
                        pass

    cnn = mc.listConnections(elshape[1],s=1, p=1)
    if cnn :
        for c in cnn:
            dst=  mc.listConnections(c,d=1, p=1)
            if dst:
                for d in dst:
                    try:
                        mc.disconnectAttr(  d, c)
                    except:
                        pass

    mc.delete(elshape[1:])

    # get parents
    basepar=mc.listRelatives(base, p=1)
    shapepar=mc.listRelatives(lshape, p=1)

    # get args
    ol=mc.getAttr(node+'.outsideLattice')

    # build arg
    arg='mc.select({0})\n'.format(geos)
    arg+='latt=mc.lattice(n="{0}", oc=1, ol={1})\n'.format(node,ol)
    arg+='mc.connectAttr("{0}.worldMatrix", latt[0]+".deformedLatticeMatrix", f=1)\n'.format(elshape[0])
    arg+='mc.connectAttr("{0}.latticeOutput", latt[0]+".deformedLatticePoints", f=1)\n'.format(elshape[0])
    arg+='mc.connectAttr("{0}.worldMatrix", latt[0]+".baseLatticeMatrix", f=1)\n'.format(ebase[0])
    arg+='mc.delete(latt[1:])\n'
    arg+='mc.rename ("{0}", "{1}")\n'.format(elshape[0], lshape)
    arg+='mc.rename ("{0}", "{1}")\n'.format(ebase[0], base)

    if shapepar:
        arg+='mc.parent("{0}", "{1}")\n'.format(lshape, shapepar[0])
    if basepar:
        arg+='mc.parent("{0}", "{1}")\n'.format(base, basepar[0])

    arg+= 'if os.environ["rbDEBUG"] == "False":\n'
    arg+= ('\tmc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))\n')

    scrNode = mc.scriptNode(n='exportedWeights_scriptNode', bs=arg, st=1, stp='python')
    aboutLock.unlock([elshape[0], ebase[0]])

    try:
        mc.parent (elshape[0], ebase[0], w=1)
    except:
        pass

    mc.select (elshape[0], ebase[0], scrNode)
    mc.file (filename, f=1, op='', typ='mayaBinary', es=1)
    mc.delete (elshape[0], ebase[0], scrNode)

    print ('Exported Lattices: '+filename)
    return filename

def cMuscle(nodes, path):

    nodes = mc.ls(nodes)
    for node in nodes:
        geos = getMesh(node)[0]
        comps = mel.eval('cMuscle_getSelComps("{0}", true);'.format(node))
        wtName = 'smooth'

        if not comps:
            return

        wgt = mc.duplicate(node, n=node+'_Weights' )

        mc.setAttr(node+'.envelope', 1)
        mc.refresh()
        mc.setAttr(node+'.envelope', 0)

        mc.select(comps)
        filename = os.path.join(path, node+'.weight.mb')
        mel.eval('cMuscleWeightSave -sys "{0}" -wt "{1}" -f "{2}" -action "save"'.format(node, wtName, filename))

        arg = 'import export\n'+\
                'reload (export)\n'+\
                'export.connectCMuscle("{0}", "{1}", "{2}")'.format(geos, wgt[0], filename)

        scrNode = mc.scriptNode(n='exportedWeights_scriptNode', bs=arg, st=1, stp='python')
        mc.select (wgt, scrNode)

        filename = os.path.join(path, node+'.mb')
        mc.file (filename, f=1,  typ='mayaBinary', es=1)
        mc.delete (wgt, scrNode)

        print ('Exported cMuscle Weights: '+filename)

def connectCMuscle(node, wgt, wgtfile):
    try:
        mc.select(node)
        cms = mel.eval('cMuscle_makeMuscleSystem 0')
        cms = mc.rename (cms, wgt.replace('_Weights',''))

        comps = mel.eval('cMuscle_getSelComps("{0}", true)'.format(cms))


        modeStr = 'pointorder'
        prunePlaces = 3
        mirrorMode = -1
        tol = -1
        bNormalize = 0

        mc.select(comps)
        mel.eval('cMuscleWeightSave -sys "{0}" -wt "smooth" -f "{1}" -action "load"'.format(cms, wgtfile))
        mc.setAttr(cms+'.envelope', 1)

        attrs = ['en', 'esmth', 'scll', 'sitr', 'sstr', 'scmp', 'sexp', 'shld']
        for a in attrs:
            mc.setAttr(cms+'.'+a, mc.getAttr(wgt+'.'+a))

        mc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))
        mc.delete(wgt)
    except:
        pass

def skinCluster(nodes, path, filename=None, rebuild=True):

    nodes = mc.ls(nodes)
    if not filename:
        filename = os.path.abspath(path.split('.')[0]+'.mb')

    wtList=[]
    cmd='import maya.cmds as mc\nimport maya.mel as mm\n\n'
    for node in nodes:
        geo = mc.skinCluster(node, q=1,g=1)[0]
        if mc.nodeType(geo) == 'mesh' and rebuild:
            print ('Rebuilding: '+node)
            skinClusterTools.rebuildSkinClusterNode(node)

        attr = '.weightList'
        battr = '.blendWeights'

        wts = mc.createNode('skinCluster', n=node+'_exportedWeights')
        wtList.append(wts)
        mc.connectAttr(node+attr, wts+attr)
        mc.disconnectAttr(node+attr,wts+attr)
        mc.setAttr(wts+'.skinningMethod', mc.getAttr(node+'.skinningMethod'))

        mc.connectAttr(node+'.blendWeights', wts+'.blendWeights')
        mc.disconnectAttr(node+'.blendWeights',wts+'.blendWeights')

        jnts = '"'+'","'.join(mc.skinCluster(node, q=1,inf=1))+'"'

        cmd += '##############################################\n'
        cmd += 'geo="'+geo+'"\n'
        cmd += 'joints=['+jnts+']\n'
        cmd += 'scls=mel.eval("findRelatedSkinCluster '+geo+'")\n\n'

        cmd += 'if not mc.objExists(scls):\n'
        cmd += '    scls=mc.skinCluster(geo, joints, n=geo+"_scls", tsb=1)[0]\n\n'
        cmd += 'mc.connectAttr("'+wts+attr+'", scls+"'+attr+'")\n'
        cmd += 'mc.disconnectAttr("'+wts+attr+'", scls+"'+attr+'")\n'

        cmd += 'mc.connectAttr("'+wts+battr+'", scls+"'+battr+'")\n'
        cmd += 'mc.disconnectAttr("'+wts+battr+'", scls+"'+battr+'")\n'
        cmd += 'mc.setAttr(scls+".skinningMethod", mc.getAttr("'+wts+'.skinningMethod"))\n'
        cmd += 'mc.rename(scls, "'+node+'")\n'

    cmd+= 'if os.environ["rbDEBUG"] == "False":\n'
    cmd += '\tmc.delete(mc.ls("*_exportedWeights*", typ="skinCluster"))\n'
    cmd += '\tmc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))\n'

    scrNode = mc.scriptNode(n='exportedWeights_scriptNode', bs=cmd, st=1, stp='python')
    mc.select(wtList, scrNode)
    mc.file(filename, f=1, op='', typ='mayaBinary', es=1)
    mc.delete(wtList, scrNode)

    print ('Exported Skin Clusters: '+filename)
    return filename

# New Cluster Export
def cluster(nodes, path):

    clusterTools.fixShapeNames()
    nodes = mc.ls(nodes)

    arg = '# load clusters\n'
    arg += 'import maya.cmds as mc\n'
    arg +='''
try:
    import rigtools;
    from rigtools import cluster
except:
    from mpc.tvcRiggingSandbox import rigtools;
    from mpc.tvcRiggingSandbox.rigtools import cluster\n\n'''

    for node in nodes:
        driver = mc.cluster(node, q=1 , wn=1)
        prebind = mc.listConnections(node+'.bindPreMatrix', d=0,s=1)

        if driver:
            driver = '"{0}"'.format(driver)
        else:
            driver = '""'

        if prebind:
            prebind = '"{0}"'.format(prebind[0])
        else:
            prebind = 'None'

        sets = mc.listConnections (node, type='objectSet')
        mc.select(sets)
        points = mc.ls(sl=1, fl=1)
        weights = mc.percent(node, points, q=1, v=1)

        # Build arg
        arg += 'weightlist = {\n'
        for i in range(len(points)):
            arg += '\t"{0}" : {1},\n'.format(points[i], weights[i])
        arg += '}\n\n'

        arg += 'if mc.objExists("{0}"):\n'.format(node)+\
                '    mc.delete("{0}")\n\n'.format(node)

        arg +='cls = cluster.create(nodes=weightlist.keys(), name="{0}", driver={1}, prebind={2})\n'.format(node, driver, prebind)
        arg += 'cluster.fixShapeNames()\n\n'

        if len(list(set(weights))) == 1:
            arg += 'mc.percent(cls, weightlist.keys(), v={0})\n\n'.format(list(set(weights))[0])
        else:
            arg += 'mc.percent(cls, weightlist.keys(), v=0.0)\n'
            arg += 'for p, v in weightlist.items():\n'\
                    '    if v > 0.0:\n'\
                    '        mc.percent(cls, p, v=v)\n\n'

        arg += 'if "rbDEBUG" in os.environ.keys() and os.environ["rbDEBUG"] == "False":\n'\
                '    mc.delete(mc.ls("*exportedWeights_scriptNode*", type="script"))'

    # write out
    filename = os.path.abspath(path.split('.')[0]+'.mb')
    scrNode = mc.scriptNode(n='exportedWeights_scriptNode', stp='python', bs=arg, st=1)
    mc.select(scrNode)
    mc.file(filename, f=1, op='', typ='mayaBinary', es=1)
    mc.delete(scrNode)

    print ('Exported Clusters: '+filename)
    return filename

def blendShape(nodes, path, filename=None):
    nodes = mc.ls(nodes)
    if not filename:
        filename = os.path.abspath(path.split('.')[0]+'.mb')
    weights = []

    for node in nodes:
        geos = [mc.listRelatives(g, p=1)[0] for g in mc.blendShape(node, q=1, g=1)]
        wgt = mc.duplicate (node, name=node+'_exportedWeights')[0]
        weights.append(wgt)

        arg = 'import maya.cmds as mc\n\n'

        arg += "bs = mc.blendShape('{0}', n='{1}')\n".format(geos[0], node)
        if len(geos) > 1:
            arg += "mc.blendShape(bs[0], e=1, g={0})\n".format(geos)

        arg += 'cnn = mc.listConnections(bs[0], s=0, d=1, p=1)\n'
        arg += 'for c in cnn:\n'
        arg += '    try:\n'
        arg += '        src=mc.listConnections(c,d=0,s=1, p=1)[0]\n'
        arg += "        mc.connectAttr( src.replace (bs[0], '{0}'), c, f=1)\n".format(wgt)
        arg += '    except:\n        pass\n'
        arg += 'cnn=mc.listConnections(bs[0], s=1, d=0, p=1)\n'
        arg += 'for c in cnn:\n'
        arg += '    try:\n'
        arg += '        src=mc.listConnections(c,d=1,s=0, p=1)[0]\n'
        arg += "        mc.connectAttr(c, src.replace (bs[0], '{0}'), f=1)\n".format(wgt)
        arg += '    except:\n        pass\n'
        arg += 'mc.delete (bs)\n'
        arg += "mc.rename('{0}', '{1}')\n".format(wgt, node)
        arg +=  ('mc.delete(mc.ls("*_weights_*", typ="script"))\n\n')

    arg += 'if os.environ["rbDEBUG"] == "False":\n'
    arg += '\tmc.delete(mc.ls("*_exportedWeights*", typ="blendShape"))\n'
    arg += '\tmc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))\n'
    scrNode = mc.scriptNode(n='exportedWeights_scriptNode',stp='python', bs=arg, st=1)

    mc.select(weights, scrNode)
    mc.file(filename, f=1,  typ='mayaBinary', es=1)
    mc.delete(weights, scrNode)

    print ('Exported Blendshapes: '+filename)
    return filename

def rigTags(path):
    nodes = mc.ls('*.tagCtrl')
    nodes.extend(mc.ls('*.tagKeyable'))
    nodes.extend(mc.ls('*.tagSpaces'))
    filename=os.path.join(path, 'asset_tags.py')

    arg = '# Load keyable attr tags\n'
    arg = 'import maya.cmds as mc\n\n'
    arg += 'def load():\n'
    for n in nodes:
        arg += "    try:\n"
        arg += "        mc.setAttr('{0}', '{1}', type='string')\n".format(n, mc.getAttr(n))
        arg += "    except:\n"
        arg += "        mc.warning('Could not load tag: {0}')\n".format(n)

    if os.path.isfile(filename):
        result = mc.confirmDialog( title='Overwrite Feather Build File?', message='asset_tags.py already exists.\nOverwrite file?\n\n'+filename, \
                                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return
        shutil.copyfile(filename, filename+'.bak')

    f=open(filename, 'w')
    f.write(arg)
    f.close()

    print ('Exported Tags: '+filename)

def rigSettings():
    nodes = mc.ls('*.controlID')
    filename = os.path.join(assetEnv.getpath(), assetEnv.getasset()+'Settings.py')

    arg = '# Load default rig settings\n'
    arg = 'import maya.cmds as mc\n\n'
    arg += 'def load():\n'

    for nn in nodes:
        if 'Skel.' in nn:
            continue

        node = nn.split('.')[0]
        kattrs = mc.listAttr (node, k=1)
        sattrs = ['tagKeyable', 'tagSpaces', 'tag', 'controlID']

        for s in sattrs:
            if s in kattrs:
                kattrs.remove (s)

        for a in kattrs:
            n = node.split('.')[0]+'.'+a
            if mc.objExists(n):
                arg += "    try:\n"
                arg += "        mc.setAttr('{0}', {1})\n".format(n, mc.getAttr(n))
                arg += "    except:\n"
                arg += "        mc.warning('Could not set attr: {0}')\n".format(n)

        for a in sattrs:
            n = node.split('.')[0]+'.'+a
            if mc.objExists(n):
                arg += "    try:\n"
                arg += "        mc.setAttr('{0}', '{1}', type = 'string')\n".format(n, mc.getAttr(n))
                arg += "    except:\n"
                arg += "        mc.warning('Could not set STRING attr: {0}')\n".format(n)
    if os.path.isfile(filename):
        result = mc.confirmDialog( title='Overwrite Feather Build File?', message=assetEnv.getasset()+'Settings.py already exists.\nOverwrite file?\n\n'+filename, \
                                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return
        shutil.copyfile(filename, filename+'.bak')

    f = open(filename, 'w')
    f.write(arg)
    f.close()
    print ('Exported Rig Default Settings: '+filename)

# Helper funcs
def getMesh(node, checkNurbs=False):
    hist = mc.listHistory(node)
    meshs = []
    for h in hist:
        if mc.nodeType(h) == 'mesh':
            m = mc.listRelatives(h, p=1)[0]
            if not m in meshs:
                meshs.append(m)

    if checkNurbs and not meshs:
        for h in hist:
            if mc.nodeType(h) == 'nurbsSurface':
                m = mc.listRelatives(h, p=1)[0]
                if not m in meshs:
                    meshs.append(m)
    return meshs

def getDeformers(node, ntype):

    if not mc.objExists(node):
        return
    deformers=[]
    shape = mc.listRelatives (node, s=1, noIntermediate=1)
    if shape:
        history = mc.listHistory(shape[0])
        for obj in history:
            if mc.nodeType(obj) == ntype:
                deformers.append(obj)
    return deformers

def getConstraints(node):
    cons = []
    cnn = mc.listConnections(node,s=1, d=0, scn=1,type='pointConstraint')
    if cnn:
        cons.extend(cnn)
    cnn = mc.listConnections(node,s=1, d=0, scn=1,type='orientConstraint')
    if cnn:
        cons.extend(cnn)
    cnn = mc.listConnections(node,s=1, d=0, scn=1,type='parentConstraint')
    if cnn:
        cons.extend(cnn)
    cnn = mc.listConnections(node,s=1, d=0, scn=1,type='scaleConstraint')
    if cnn:
        cons.extend(cnn)

    cons = list(set(cons))
    return cons

def getSDKs(node):
    crvs = mc.listConnections(node,s=1, d=0, scn=1,type='animCurve')
    bws = mc.listConnections(node,s=1, d=0, scn=1,type='blendWeighted')

    if not crvs:
        crvs = []

    if bws:
        for bw in bws:
            cnn = mc.listConnections(bw, s=1, d=0, scn=1,type='animCurve')
            if cnn:
                crvs.extend(cnn)
    return crvs

def attributes(nodes, path=None):
    for node in nodes:
        uds = mc.listAttr(node, ud=1)

        arg = '# Create user defined attributes\n\n' + \
        'import maya.cmds as mc\nimport maya.mel as mm\n'
        arg +='''

try:
    import rigtools;
    from rigtools import controlTools
except:
    from mpc.tvcRiggingSandbox import rigtools;
    from mpc.tvcRiggingSandbox.rigtools import controlTools\n\n'''

        validate = False
        if uds:
            for ud in uds:
                if ud not in ['controlID', 'tagKeyable', 'tagSpaces', 'tag', 'space', 'rigBuildNode']:
                    atype = mc.addAttr(node+'.'+ud, q=1, at=1)
                    print (ud)

                    # ints and floats
                    if atype in ['long', 'double', 'bool', 'enum']:

                        minv = mc.addAttr(node+'.'+ud, q=1, min=1)
                        maxv = mc.addAttr(node+'.'+ud, q=1, max=1)

                        dv = mc.addAttr(node+'.'+ud, q=1, dv=1)

                        if minv is not None and atype not in ['bool', 'enum']:
                            minv = ', min={0}'.format(minv)
                        else:
                            minv = ''
                        if maxv is not None and atype not in ['bool', 'enum']:
                            maxv = ', max={0}'.format(maxv)
                        else:
                            maxv = ''
                        if atype == 'enum':
                            enum = mc.addAttr(node+'.'+ud, q=1, en=1)
                            enum = ', en="{0}"'.format(enum)
                        else:
                            enum = ''

                        arg += '\nif mc.objExists("{0}") and not mc.objExists("{0}.{1}"):\n'.format(node, ud)
                        arg += '\tmc.addAttr("{0}", ln="{1}", at="{2}", k=1, dv={5}{3}{4}{6})\n'.format(node, ud, atype, minv, maxv, dv, enum)
                        arg += '\tcontrolTools.tagKeyable("{0}", "{1}", add=1)\n'.format(node, ud)
                        validate = True

        arg += '\tmc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))\n'

        if validate:
            rtype = assetEnv.getrigtype()

            if not path:
                path = os.path.join(assetEnv.getpath(), 'build', 'bind', rtype, 'attrs')

            if not os.path.isdir(path):
                os.makedirs(path)

            filename = os.path.join(path, node+'_attrs.mb')
            scrNode = mc.scriptNode(n='exportedWeights_scriptNode', stp='python', bs=arg, st=1)
            mc.select(scrNode)
            mc.file(filename, f=1, op='', typ='mayaBinary', es=1)
            mc.delete(scrNode)
            print ('Exported Custom attributes to: '+filename)

def unlockedAttrs():
    asset = assetEnv.getasset()
    if not mc.objExists('animSet_'+asset):
        mc.warning('Ctrl set not found! Export settings AFTER your sets have been created.')
        return

    mc.select('animSet_'+asset)
    ctrls = mc.ls(sl=1)

    if not ctrls:
        mc.warning('No controls in Ctrl set.. Recreate it to proceed..')
        return

    arg = '''try:
    import rigtools;
    from rigtools import lockTools
except:
    from mpc.tvcRiggingSandbox import rigtools;
    from mpc.tvcRiggingSandbox.rigtools import lockTools
import maya.cmds as mc\n\n
'''
    arg += 'def load():\n'
    arg += '\tmc.select(mc.ls({0}))\n'.format(ctrls)
    arg += '\taboutLock.set( l=1, k=0)\n\n'

    for c in ctrls:
        attrs = mc.listAttr(c, k=1)
        ignore = ['tagSpaces', 'tagKeyable', 'controlID', 'tag']
        for ig in ignore:
            if ig in attrs:
                attrs.remove(ig)

        for a in attrs:
            try:
                v = mc.getAttr(c+'.'+a)
                if not type(v) is unicode:
                    arg += '\ttry:\n'
                    arg += '\t\tmc.setAttr("{0}.{1}", l=0, k=1)\n'.format(c, a)
                    arg += '\t\tmc.setAttr("{0}.{1}", {2})\n'.format(c, a, mc.getAttr(c+'.'+a))
                    arg += '\texcept:\n\t\tpass\n'
            except:
                pass

    rtype = assetEnv.getrigtype()
    filename = os.path.join(assetEnv.getpath(), 'build', 'scripts', rtype+'AttributeSettings.py')
    if os.path.isfile(filename):
        result = mc.confirmDialog( title='Overwrite Feather Build File?', message=assetEnv.getasset()+'Constraints.py already exists.\nOverwrite file?\n\n'+filename, \
                                button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return
        shutil.copyfile(filename, filename+'.bak')

    f = open(filename, 'w')
    f.write(arg)
    f.close()
    print ('Exported Attribute Settings to: '+filename)

'''
def nonLinear(node, path=None):

if not path:
        path = mc.fileDialog2(fm=3, fileFilter=('*.none'))
        if path:
            path = path[0]
        else:
            return
# find set
cnn = mc.listConnections (node+'.message', type='objectSet')

# get verts and geos in set
mc.select(cnn[0])
geos = mc.ls(sl=1)

#gget handle
hnd = mc.listConnections (node+'.matrix')[0]
ehnd = mc.duplicate(hnd, n=hnd+'_exportedWeights')
ehnd[1] = mc.rename (ehnd[1], node+'_exportedWeights')
ehnd[2] = mc.rename (ehnd[2], node+'_exportedWeights')

try:
    mc.parent(ehnd[0], w=1)
except:
    pass
# get parent
par = mc.listRelatives (hnd, p=1)

# create arg
ntype = mc.nodeType(mc.listRelatives(ehnd[0], s=1)).replace('deform', '').lower()

arg='mc.select({0})\n'.format(geos)
arg+="nonlin=mc.nonLinear(type='{0}')\n".format( ntype)
arg+='cnn=mc.listConnections(nonlin[0], s=0, d=1, p=1)\n'
arg+='for c in cnn:\n'
arg+='    try:\n'
arg+='        src=mc.listConnections(c,d=0,s=1, p=1)[0]\n'
arg+="        mc.connectAttr( src.replace (nonlin[0], '{0}'), c, f=1)\n".format(ehnd[1])
arg+='    except:\n        pass\n'
arg+='cnn=mc.listConnections(nonlin[0], s=1, d=0, p=1)\n'
arg+='for c in cnn:\n'
arg+='    try:\n'
arg+='        src=mc.listConnections(c,d=1,s=0, p=1)[0]\n'
arg+="        mc.connectAttr(c, src.replace (nonlin[0], '{0}'), f=1)\n".format(ehnd[1])
arg+='    except:\n        pass\n'

arg+='cnn=mc.listConnections(nonlin[1], s=0, d=1, p=1)\n'
arg+='for c in cnn:\n'
arg+='    try:\n'
arg+='        src=mc.listConnections(c,d=0,s=1, p=1)[0]\n'
arg+="        mc.connectAttr( src.replace (nonlin[1], '{0}'), c, f=1)\n".format(ehnd[0])
arg+='    except:\n        pass\n'
arg+='cnn=mc.listConnections(nonlin[1], s=1, d=0, p=1)\n'
arg+='for c in cnn:\n'
arg+='    try:\n'
arg+='        src=mc.listConnections(c,d=1,s=0, p=1)[0]\n'
arg+="        mc.connectAttr(c, src.replace (nonlin[1], '{0}'), f=1)\n".format(ehnd[0])
arg+='    except:\n        pass\n'

arg+='mc.delete (nonlin)\n'
arg+="mc.rename('{0}', '{1}')\n".format(ehnd[1], node)
arg+="mc.rename('{0}', '{1}')\n".format(ehnd[0], hnd)

arg+= ('mc.delete(mc.ls("*_exportedWeights*", typ="blendShape"))\n')
arg+= ('mc.delete(mc.ls("*exportedWeights_scriptNode*", typ="script"))\n')

if par:
    arg+= ('mc.parent("{0}", "{1}")\n'.format(ehnd[0], par[0]))

scrNode=mc.scriptNode(n='exportedWeights_scriptNode',stp='python', bs=arg, st=1)


filename=os.path.join(path, node+'.mb')
mc.select (ehnd, scrNode)
mc.file (filename, f=1,  typ='mayaBinary', es=1)
mc.delete (ehnd, scrNode)

print 'Exported Blendshapes: '+filename
return filename

'''