from importlib import reload

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

QtCore, QtGui, QtWidgets= get_pyside_module()

import maya.OpenMaya as om
import maya.cmds as mc
import maya.mel as mel

from rxCore import aboutName
reload(aboutName)

def Create():
    sel = mc.ls(sl=1)
    create(sel[:-1], sel[-1])


def create(nodes=None, driver='', soft=False, prebind=None, name=None):

    if nodes is None :
        nodes = mc.ls(sl=1)

    if len(nodes) > 1 and not driver and mc.nodeType(nodes[-1]) in ['transform', 'joint']:
        driver = nodes[-1]
        nodes.remove(driver)

    mc.select(nodes)
    mel.eval('ConvertSelectionToVertices')
    nodes = mc.ls(sl=1)
    info = {}
    if soft:
        info = getSoftSelectWeights()
        geos = []
        for v in info[0]:
            x = v.split('|')[-1].split('.')[0]
            if x not in geos:
                geos.append(x)
        mc.select(geos)
        mel.eval('ConvertSelectionToVertices')
        nodes = mc.ls(sl=1, fl=1, l=1)
        info = info[1]

    if not name:
        name = nodes[0].split('|')[-1].split('.')[0]+'_cls'
        name = aboutName.unique(name)

    mc.select(nodes)
    if not mc.objExists(driver):
        cls = mc.cluster(nodes, bs=1)
        cls[0] = mc.rename(cls[0], name)
        cls[1] = mc.rename(cls[1], name+'Handle')
        driver = cls[1]
    else:
        cls = mc.cluster(nodes, wn=[driver, driver], bs=1)
        cls[0] = mc.rename(cls[0], name)
        clusterTransformsAttr = mc.listConnections(cls[0]+'.clusterXforms', p=1)[0]
        clusterHandleShape = clusterTransformsAttr.split('.')[0]
        mc.rename(clusterHandleShape, name+'_HandleShape')

    if prebind is not None:
        if mc.objExists(prebind):
            mc.connectAttr(prebind+'.parentInverseMatrix', cls[0]+'.bindPreMatrix')

    if soft:
        mc.select(nodes)
        mc.percent(cls[0], v=0)
        for i in info.keys():
            mc.percent(cls[0], i, v=info[i])

    fixShapeNames()
    mc.select(driver)
    return cls[0]


def rebuild(node):

    fixShapeNames()
    driver = mc.listConnections(node +'.clusteforms',  d= 1)[0]
    prebind = mc.listConnections(node+'.bindPreMatrix', d=0, s=1)
    sets = mc.listConnections(node, type='objectSet')

    mc.select(sets)
    verts = mc.ls(sl=1, fl=1)
    geos, tgeos, tverts = [], [], []

    for v in verts:
        x = v.split('|')[-1].split('.')[0]
        if x not in geos:
            geos.append(x)
            tgeos.append(mc.duplicate(x)[0])
        tverts.append(v.replace(geos[-1], tgeos[-1]))
    mc.parent(tgeos, w=1)
    mc.select(geos)

    # Copy to new temp cls
    tcls = mc.cluster(tverts, bs=1)
    mc.select(tgeos)
    mc.percent(tcls[0], v=0.0)
    for i in range(len(tgeos)):
        mc.copyDeformerWeights( ss=geos[i], ds=tgeos[i], sd=node, dd=tcls[0], sa='closestPoint', nm=1)

    mc.delete(node)
    cls = create(nodes=verts, name=node, driver=driver, prebind=prebind[0])

    mc.select(geos)
    mc.percent(cls, v=0.0)
    for i in range(len(geos)):
        mc.copyDeformerWeights( ss=tgeos[i], ds=geos[i], sd=tcls[0], dd=cls, sa='closestPoint', nm=1)
    mc.delete(tcls, tgeos)

    fixShapeNames()
    return cls


def fixShapeNames():
    shapes = mc.ls(type='clusterHandle', sn=1)
    for s in shapes:
        if '|' in s:
            nn = aboutName.unique(mc.listRelatives(s, p=1)[0]+'Shape')
            mc.rename(s, nn)


def getSoftSelectWeights():
    weightInfo = {}

    #Grab the soft selection
    selection = om.MSelectionList()
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)

    dagPath = om.MDagPath()
    component = om.MObject()

    # Filter Defeats the purpose of the else statement
    iter = om.MItSelectionList( selection,om.MFn.kMeshVertComponent )
    while not iter.isDone():
        iter.getDagPath( dagPath, component )
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = om.MFnSingleIndexedComponent(component)
        getWeight = lambda i: fnComp.weight(i).influence() if fnComp.hasWeights() else 1.0

        for i in range(fnComp.elementCount()):
            weightInfo['%s.vtx[%i]'%(node, fnComp.element(i))] = getWeight(i)
        iter.next()

    nodes, weight = [],[]
    for i in weightInfo.items():
        nodes.append(i[0])
        weight.append(i[1])

    return [nodes, weightInfo]


def getClusterPosition(cluster):
    """
    Get the origin position of a cluster, positions are rounded to 6 
    decimals to be able to match positions.
    
    :param str cluster:
    :return: origin position of cluster
    :rtype: list
    """
    pos = mc.getAttr("{0}.origin".format(cluster))[0]
    return [round(p, 6) for p in pos]


class UI(QtWidgets.QDialog):

    def __init__(self):
        super(UI, self).__init__()

        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setObjectName("cluster")
        self.resize(359, 175)
        self.setMinimumSize(QtCore.QSize(359, 175))
        self.setMaximumSize(QtCore.QSize(359, 175))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(8)

        self.gridLayout.setObjectName("gridLayout")
        self.setGroup = QtWidgets.QGroupBox(self)
        self.setGroup.setTitle("")
        self.setGroup.setObjectName("setGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.setGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setGrid = QtWidgets.QGridLayout()
        self.setGrid.setObjectName("setGrid")
        self.driverLabel = QtWidgets.QLabel(self.setGroup)
        self.driverLabel.setObjectName("driverLabel")
        self.setGrid.addWidget(self.driverLabel, 1, 0, 1, 1)
        self.driverEdit = QtWidgets.QLineEdit(self.setGroup)
        self.driverEdit.setObjectName("driverEdit")
        self.setGrid.addWidget(self.driverEdit, 1, 1, 1, 1)
        self.driverBtn = QtWidgets.QPushButton(self.setGroup)
        self.driverBtn.setMaximumSize(QtCore.QSize(60, 16777215))
        self.driverBtn.setObjectName("driverBtn")
        self.setGrid.addWidget(self.driverBtn, 1, 2, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.setGroup)
        self.nameLabel.setObjectName("nameLabel")
        self.setGrid.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(self.setGroup)
        self.nameEdit.setObjectName("nameEdit")
        self.setGrid.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.prebindBtn = QtWidgets.QPushButton(self.setGroup)
        self.prebindBtn.setMaximumSize(QtCore.QSize(60, 16777215))
        self.prebindBtn.setObjectName("prebindBtn")
        self.setGrid.addWidget(self.prebindBtn, 2, 2, 1, 1)
        self.prebindEdit = QtWidgets.QLineEdit(self.setGroup)
        self.prebindEdit.setObjectName("prebindEdit")
        self.setGrid.addWidget(self.prebindEdit, 2, 1, 1, 1)
        self.prebindLabel = QtWidgets.QLabel(self.setGroup)
        self.prebindLabel.setObjectName("prebindLabel")
        self.setGrid.addWidget(self.prebindLabel, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.setGrid)
        self.gridLayout.addWidget(self.setGroup, 0, 0, 1, 1)
        self.createBtn = QtWidgets.QPushButton(self)
        self.createBtn.setObjectName("createBtn")
        self.gridLayout.addWidget(self.createBtn, 2, 0, 1, 1)
        self.createWeightsBtn = QtWidgets.QPushButton(self)
        self.createWeightsBtn.setObjectName("createWeightsBtn")
        self.gridLayout.addWidget(self.createWeightsBtn, 3, 0, 1, 1)
        self.setGrid.setContentsMargins(4,4,4,4)
        self.setGrid.setHorizontalSpacing(4)
        self.setGrid.setVerticalSpacing(4)

        self.setWindowTitle('Clusters')
        self.driverLabel.setText('Driver')
        self.driverBtn.setText('Get')
        self.nameLabel.setText('Name')
        self.prebindBtn.setText('Get')
        self.prebindLabel.setText('Prebind Node')
        self.createBtn.setText('Create Cluster')
        self.createWeightsBtn.setText('Create With Soft Selected Weights')

        self.driverBtn.clicked.connect(self.getAction)
        self.prebindBtn.clicked.connect(self.getAction)

        self.nameEdit.setPlaceholderText('Optional cls')
        self.prebindEdit.setPlaceholderText('Optional prebind node')

        self.createBtn.clicked.connect(self.create)
        self.createWeightsBtn.clicked.connect(lambda: self.create(soft=True))

    def getAction(self):
        sel = mc.ls(sl=1)[0]
        obj = self.sender().objectName().replace('Btn', 'Edit')
        if obj == 'prebindEdit' and mc.objExists(sel+'Offset'):
            sel = sel+'Offset'
        exec('self.{0}.setText("{1}")'.format(obj, sel))

    def create(self, soft=False):
        name = self.nameEdit.text().strip().replace(' ', '_')
        driver = self.driverEdit.text().strip().replace(' ', '_')
        prebind = self.prebindEdit.text().strip().replace(' ', '_')

        if not name:
            name = aboutName.unique(driver.replace('_ctrl', '')+'_cls', suffix='_cls')
        create(name=name, driver=driver, prebind=prebind, soft=soft)
