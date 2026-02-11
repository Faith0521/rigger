import re,os,sys
from importlib import reload

import maya.cmds as mc
import maya.mel as mel
from PySide2 import QtCore, QtGui, QtWidgets

from ...maya_utils import aboutPath
from ...maya_utils import aboutCrv
from ...maya_utils import aboutPublic
from ...maya_utils import aboutName
from ...maya_utils import aboutUI

from . import controller_ui
reload(controller_ui)
reload(aboutUI)
reload(aboutPath)
reload(aboutCrv)
reload(aboutPublic)

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def undoable(function):
    """A decorator that will make commands undoable in maya"""

    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None

        # noinspection PyBroadException
        try:
            functionReturn = function(*args, **kwargs)

        except:
            print (sys.exc_info()[1])

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn

    return decoratorCode

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def uiShow():
    controller_dock().show(dockable=True)

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class controller_dock(aboutUI.UI_Dockable):
    title_name = 'controller_V1.0'  # Window display name
    control_name = 'controller_System'  # Window unique object name

    def __init__(self):
        super(self.__class__, self).__init__()

    def build_ui(self):
        self.main_layout.addWidget(controller())

class controller(QtWidgets.QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = controller_ui.Ui_ctrl_win()
        self.ui.setupUi(self)

        # data
        self.iconSuffix = '_icon_M.bmp'
        self.crvData_path = aboutPath.filePath('curve')
        self.crvIcon_List = aboutPath.fileList(self.crvData_path, self.iconSuffix)

        # set color
        self.ui.yellow_color_btn.clicked.connect( self.set_yellow_color )
        self.ui.blue_color_btn.clicked.connect( self.set_blue_color )
        self.ui.cobalt_color_btn.clicked.connect( self.set_cobalt_color )
        self.ui.turquoise_color_btn.clicked.connect( self.set_turquoise_color )
        self.ui.red_color_btn.clicked.connect( self.set_red_color )
        self.ui.violet_color_btn.clicked.connect( self.set_violet_color )
        self.ui.green_color_btn.clicked.connect( self.set_green_color )

        # set roll
        self.ui.rox_btn.clicked.connect(self.rollCtrl_x_forUI)
        self.ui.roy_btn.clicked.connect(self.rollCtrl_y_forUI)
        self.ui.roz_btn.clicked.connect(self.rollCtrl_z_forUI)

        # set scale
        self.ui.s01_btn.clicked.connect(lambda: self.ui.sv_line.setText('0.1'))
        self.ui.s05_btn.clicked.connect(lambda: self.ui.sv_line.setText('0.5'))
        self.ui.s07_btn.clicked.connect(lambda: self.ui.sv_line.setText('0.7'))
        self.ui.s09_btn.clicked.connect(lambda: self.ui.sv_line.setText('0.9'))
        self.ui.s12_btn.clicked.connect(lambda: self.ui.sv_line.setText('1.2'))
        self.ui.s15_btn.clicked.connect(lambda: self.ui.sv_line.setText('1.5'))
        self.ui.s20_btn.clicked.connect(lambda: self.ui.sv_line.setText('2.0'))
        self.ui.sc_shape_btn.clicked.connect(self.scaleCtrl_shapeCenter_forUI)
        self.ui.sc_object_btn.clicked.connect(self.scaleCtrl_objectCenter_forUI)

        # set mirror coontroller
        self.ui.mirrorControl_btn.clicked.connect(self.mirrorCtrl_forUI)
        self.ui.mirrorShapel_btn.clicked.connect(self.mirrorCtrlShape_forUI)

        # set export/import controller data
        self.ui.exportShape_btn.clicked.connect(self.exportCtrlData_forUI)
        self.ui.importShape_btn.clicked.connect(self.importCtrlData_forUI)

        # refresh
        self.buildCtrlIcon()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------


    def buildCtrlIcon(self):
        # LISTWIDGET SETTING
        self.ui.ctrl_listWidget.clear()
        self.ui.ctrl_listWidget.itemClicked.connect(self.createCtrl_forUI)

        for icon in self.crvIcon_List:
            # find real icon image path
            iconPath = self.crvData_path+'/'+icon
            # find real crvShape name from icon
            crvName = icon.replace(self.iconSuffix, '')

            item = QtWidgets.QListWidgetItem()
            item.setIcon( QtGui.QIcon(iconPath) )
            #item.setSizeHint(QtCore.QSize(120, 120))
            # set text used for create control
            item.setToolTip(crvName)
            #add item
            self.ui.ctrl_listWidget.addItem(item)

        self.ui.ctrl_listWidget.sortItems()
        # select first item, to fix right click not showing at startup
        self.ui.ctrl_listWidget.setCurrentRow(0)

        self.ui.ctrl_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.ctrl_listWidget.customContextMenuRequested.connect(self.iconMenu)


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def iconMenu(self, position):
        currentItem = self.ui.ctrl_listWidget.currentItem()
        if not currentItem:
            return
        # menu
        menu = QtWidgets.QMenu(self)
        replaceAction = menu.addAction("replace")

        # cmds
        action = menu.exec_( self.ui.ctrl_listWidget.mapToGlobal(position) )
        if action == replaceAction:
            self.replaceCtrlShape_forUI(ctrlName='', shapeName='')


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def movePiv(self):
        sel = mc.ls(sl=1)
        ctrl = ''
        if sel:
            if mc.objExists(sel[0]+'.controlID'):
                ctrl = sel[0]
        if ctrl:
            pivot(ctrl)
        else:
            mc.warning('This is not a ctrl.')


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    #@undoable
    def createCtrl_forUI(self):
        # crv name

        ctrlName = self.ui.nameLine.text()
        if not ctrlName:
            ctrlName = 'my_ctrl'

        if ctrlName and not ctrlName.endswith('_ctrl'):
            ctrlName += '_ctrl'

        # shape name
        currentItem = self.ui.ctrl_listWidget.currentItem()
        shapeName = currentItem.toolTip()
        crvData = '{0}{1}.cs'.format(self.crvData_path, shapeName)

        # snapTo
        snapTo = ''
        snapType = 't'
        if self.ui.orient_cb.isChecked():
            snapType = 'both'

        snapToList = mc.ls(sl=1)
        ctrlsList = []
        if snapToList:
            for snapTo in snapToList:
                ctrls = create(ctrlName, crvData, color='blue', scale=1, snapTo=snapTo, snapType=snapType, parent='', makeGroups=True, tag='animCtrl')
                ctrlsList.append(ctrls)
        else:
            create(ctrlName, crvData, color='blue', scale=1, snapTo=snapTo, parent='', makeGroups=True, tag='animCtrl')

        if self.ui.hirerachy_cb.isChecked():
            for i in range(len(ctrlsList)-1):
                mc.parent(ctrlsList[i+1][0], ctrlsList[i][4])

        if self.ui.revcon_cb.isChecked():
            for i in range(len(ctrlsList)):
                if mc.objExists(snapToList[i]) and mc.nodeType(snapToList[i]) == 'joint':
                    mc.parentConstraint(ctrlsList[i][4], snapToList[i], mo=True)
                    mc.scaleConstraint(ctrlsList[i][4], snapToList[i], mo=True)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # set color for ui command
    def setColor_forUI(self, color='yellow'):
        selCtrls = checkSelType_crv()
        [ setColor(ctrl, color) for ctrl in selCtrls ]
    def set_yellow_color(self):
        self.setColor_forUI(color='yellow')
    def set_blue_color(self):
            self.setColor_forUI(color='blue')
    def set_cobalt_color(self):
        self.setColor_forUI(color='cobalt')
    def set_turquoise_color(self):
        self.setColor_forUI(color='turquoise')
    def set_red_color(self):
        self.setColor_forUI(color='red')
    def set_violet_color(self):
        self.setColor_forUI(color='violet')
    def set_green_color(self):
        self.setColor_forUI(color='green')


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    @undoable
    def replaceCtrlShape_forUI(self, ctrlName, shapeName):
        # ctrl name
        selCtrls = ''
        if not ctrlName:
            selCtrls = checkSelType_crv()
        # shape name
        if not shapeName:
            currentItem = self.ui.ctrl_listWidget.currentItem()
            shapeName = currentItem.toolTip()
        # replace
        crvData = '{0}{1}.cs'.format(self.crvData_path, shapeName)
        for ctrl in selCtrls:
            replaceCtrlShape(ctrl, crvData)
            mc.select(cl=True)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # roll
    def rollCtrl_x_forUI(self):
        selCtrls = checkSelType_crv()
        [rollCtrlShape(ctrl, axis='x') for ctrl in selCtrls]

    def rollCtrl_y_forUI(self):
        selCtrls = checkSelType_crv()
        [rollCtrlShape(ctrl, axis='y') for ctrl in selCtrls]

    def rollCtrl_z_forUI(self):
        selCtrls = checkSelType_crv()
        [rollCtrlShape(ctrl, axis='z') for ctrl in selCtrls]


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # scale
    def scaleCtrl_shapeCenter_forUI(self):
        selCtrls = checkSelType_crv()
        value = float(self.ui.sv_line.text())
        [scaleCtrlShape(ctrl, value, editPivetType='shapeCenter') for ctrl in selCtrls]

    def scaleCtrl_objectCenter_forUI(self):
        selCtrls = checkSelType_crv()
        value = float(self.ui.sv_line.text())
        [scaleCtrlShape(ctrl, value, editPivetType='objectCenter') for ctrl in selCtrls]

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def mirrorCtrl_forUI(self):
        ctrlList = mc.ls(sl=True)
        for ctrl in ctrlList:
            mirrorCtrl(ctrl)

    def mirrorCtrlShape_forUI(self):
        startswithKeyDict = {'L_': 'R_', 'R_': 'L_',
                       'lf_': 'rt_', 'rt_': 'lf_'}
        middleKeyDict = {'_L_': '_R_', '_R_': '_L_'}

        ctrlList = mc.ls(sl=True)
        for ctrl in ctrlList:
            for key in startswithKeyDict.keys():
                if ctrl.startswith(key):
                    aboutCrv.mirrorCrvShape(ctrl, axisMirrors='x', search=key, replace=startswithKeyDict[key])
            for key in middleKeyDict.keys():
                if key in ctrl:
                    aboutCrv.mirrorCrvShape(ctrl, axisMirrors='x', search=key, replace=middleKeyDict[key])
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportCtrlData_forUI(self):
        selCtrls = checkSelType_crv()
        aboutCrv.exportCurveShape(selCtrls)
    def importCtrlData_forUI(self)   :
        aboutCrv.importCurveShape()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def copyShape(nodes=None, copyColor=True, mirror=False):
    if nodes is None:
        nodes = []
    aboutCrv.copyShape(nodes, copyColor, mirror)

# check seleted is ctrl
def checkSelType_crv():
    selCtrls = mc.ls(sl=True)
    realCtrls = []

    if selCtrls:
        for ctrl in selCtrls:
            if aboutPublic.getObjType(ctrl) == 'kNurbsCurve':
                realCtrls.append(ctrl)
    else:
        mc.error('Sorry, You need select curves !')

    if len(realCtrls) == 0:
        mc.error('Sorry, You need select curves')
    else:
        return realCtrls


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def create(name, crvData, color='blue', scale=None, snapTo='', snapType='t', useShape='', jointCtrl=False, makeGroups=True, worldOrientGroups=False, parent='', tag='animCtrl', ns=0):
    # unique name
    suff = '_ctrl'
    if ns:
        suff = ''

    if name:
        if not name.endswith('_ctrl'):
            name += '_ctrl'
        name = aboutName.unique(name, suffix=suff)

    # ctrlName / shapeName
    if jointCtrl:
        ctrl = mc.createNode('joint', name=name)
        mc.setAttr(ctrl+'.radius', 0)
        mc.setAttr(ctrl+'.drawStyle', 2)
        aboutCrv.addShape(name, crvData)
    else:
        ctrl = aboutCrv.createCrv(name, crvData)

    # color
    setColor(ctrl,color)

    # snap
    if snapTo:
        aboutPublic.snapAtoB(ctrl, snapTo, snapType)

    # use shape
    if mc.objExists(useShape):
        copyShape([useShape, ctrl], copyColor=True)

    # crvScale
    if type(scale) is not list:
        scale = [scale, scale, scale]
    aboutCrv.editCrvHull(name, xyzValue=scale, modifyType='scale')

    # parent
    if parent:
        mc.parent(ctrl, parent)

    # make groups
    ctrls=[]
    if makeGroups:
        grpNameList = ['grp','axis','con','sdk']
        ctrls = aboutPublic.fastGrp(ctrl, grpNameList, worldOrient=worldOrientGroups)
    ctrls.append(ctrl)

    # add tags
    mc.addAttr(ctrl, ln='controlID', dt='string')
    mc.addAttr(ctrl, ln='tagKeyable', dt='string')
    mc.addAttr(ctrl, ln='tagSpaces', dt='string')
    mc.addAttr(ctrl, ln='tag', dt='string')
    # set tags
    mc.setAttr(ctrl+'.controlID', ctrl, type='string')
    mc.setAttr(ctrl+'.tagKeyable', 'tx ty tz rx ry rz', type='string')
    mc.setAttr(ctrl+'.tagSpaces', '', type='string')
    mc.setAttr(ctrl+'.tag', tag, type='string')

    return ctrls

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
# Set color. typing "help" returns options
def setColor(ctrl, color=None):
    colors = {}
    colors['black'] = 1
    colors['grey'] = 2
    colors['lightGrey'] = 3
    colors['darkMagenta'] = 4
    colors['darkBlue'] = 5
    colors['blue'] = 6
    colors['forestGreen'] = 7
    colors['purple'] = 8
    colors['fuscia'] = 9
    colors['lightBrown'] = 10
    colors['brown'] = 11
    colors['burntSienna'] = 12
    colors['red'] = 13
    colors['green'] = 14
    colors['cobalt'] = 15
    colors['white'] = 16
    colors['yellow'] = 17
    colors['cyan'] = 18
    colors['mint'] = 19
    colors['peach'] = 20
    colors['sand'] = 21
    colors['lemon'] = 22
    colors['turquoise'] = 23
    colors['tan'] = 24
    colors['yellowGreen'] = 25
    colors['grass'] = 26
    colors['teal'] = 27
    colors['darkCyan'] = 28
    colors['blueGrey'] = 29
    colors['lightPurple'] = 30
    colors['violet'] = 31

    if ctrl == 'help':
        return colors.keys()

    mc.setAttr(ctrl+'.overrideColor', colors[color])
    mc.setAttr(ctrl+'.overrideEnabled', 1)
    mc.setAttr(ctrl+'.overrideDisplayType', 0)



#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# hTag Keyable attrs from channel box
def tagKeyableCB(add=False):
    sel = mc.ls(sl=1)
    if not(len(sel)):
        return

    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;') #fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=True, sma=True)
    if attrs is not None:
        attrs = ' '.join(mc.channelBox(channelBox, q=True, sma=True))
    else:
        attrs = ''

    for s in sel:
        if not(mc.objExists(s+'.tagKeyable')):
            mc.addAttr(s, ln="tagKeyable", dt="string")

        mc.setAttr(s+'.tagKeyable', l=0)
        if add:
            at = mc.getAttr(s+'.tagKeyable')+' '+attrs
            at = at.strip().replace('  ', ' ')
            mc.setAttr(s+'.tagKeyable', at, type='string')
        else:
            mc.setAttr(s+'.tagKeyable', attrs, type='string')

    return attrs


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# replace ctrl shape
@undoable
def replaceCtrlShape(name, crvData, color=''):

    # replace
    aboutCrv.replaceShape(name, crvData)

    if not color:
        color = mc.getAttr(name+'.overrideColor')
        mc.setAttr(name+'.overrideColor', color)
    else:
        mc.setAttr(name+'.overrideColor', color)

    mc.setAttr(name+'.overrideEnabled', 1)
    mc.setAttr(name+'.overrideDisplayType', 0)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def rollCtrlShape(name, axis='x', value=90):
    if axis=='x':
        aboutCrv.editCrvHull(name, xyzValue=[value, 0, 0], modifyType='rotate')
    if axis=='y':
        aboutCrv.editCrvHull(name, xyzValue=[0, value, 0], modifyType='rotate')
    if axis=='z':
        aboutCrv.editCrvHull(name, xyzValue=[0, 0, value], modifyType='rotate')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def scaleCtrlShape(name, value, editPivetType):
    xyzValue = [value, value, value]
    aboutCrv.editCrvHull(name, xyzValue=xyzValue, modifyType='scale', editPivetType=editPivetType)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# cop shape from one to another
def mirrorShape(crv):
    aboutCrv.mirrorCrvShape(crv, axisMirrors='x', search='lf_', replace='rt_')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def duplicateCtrl(orig='', name=''):
    # get real controller
    # you can select controller or it's groups.
    if not orig:
        sel = mc.ls(sl=1)
        if sel:
            s = sel[0].replace('_sdk','').replace('_con','').replace('_axis','').replace('_grp','')
            if mc.objExists(s):
                sel[0] = s
                mc.select(sel[0])

            if mc.objExists(sel[0]+'.controlID'):
                orig = sel[0]

    # set name
    if not name:
        result = mc.promptDialog(
                title='New Ctrl Name',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel',
                text=orig)

        if result == 'OK':
            name = mc.promptDialog(query=True, text=True)
            name = aboutName.unique(name)
        else:
            return

    if not name or not mc.objExists(orig+'.controlID'):
        return

    zeroGrp = mc.ls(orig+'_grp')
    axisGrp = mc.ls(orig+'_axis')
    conGrp = mc.ls(orig+'_con')
    sdkGrp = mc.ls(orig+'_sdk')

    nzeroGrp, naxisGrp, nconGrp, nsdkGrp = '','','',''
    if zeroGrp:
        nzeroGrp = mc.duplicate(zeroGrp, n=name+'_grp', po=1)[0]
    if axisGrp:
        naxisGrp = mc.duplicate(axisGrp, n=name+'_axis', po=1)[0]
        mc.parent(naxisGrp, nzeroGrp)
    if conGrp:
        nconGrp = mc.duplicate(conGrp, n=name+'_con', po=1)[0]
        mc.parent(nconGrp, naxisGrp)
    if sdkGrp:
        nsdkGrp = mc.duplicate(sdkGrp, n=name+'_sdk', po=1)[0]
        mc.parent(nsdkGrp, nconGrp)

    nctrl = mc.duplicate(orig, n=name, po=1)[0]
    mc.parent(nctrl, nsdkGrp)

    copyShape([orig, nctrl])

    return [nzeroGrp, naxisGrp, nconGrp, nsdkGrp, nctrl]



#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Movable Pibvot
@undoable
def pivot(node, ctrl=True, shape='jackThin', color='cyan', category='animCtrl'):

    bbox = mc.exactWorldBoundingBox(node)
    size =(((bbox[3]-bbox[0])+(bbox[4]-bbox[1])+(bbox[5]-bbox[2]))/3)*.5
    size = [size, size, size]
    parent = mc.listRelatives(node,p=1)[0]
    kids = mc.listRelatives(node,c=1,type='transform')

    #create pivot ctrls
    par = mc.createNode('transform', n=node+'_pivPar')
    neg = mc.createNode('transform', n=node+'_pivNeg')

    if ctrl:
        piv = create(node+'_piv', shape=shape, scale=size, color=color, tag=category, makeGroups=False)
        piv = [mc.rename(piv[0], node+'Pivot')]
        mc.parent(piv, par)

        #create and connect visibility attr
        mc.addAttr(node, longName='pivotDisplay', shortName='pvd', at='long', min=0, max=1, k=1, h=0, dv=0)
        mc.connectAttr(node+".pvd", piv[0]+"Shape.lodVisibility")

        tagKeyable(node, 'pvd', add=True)
        tagKeyable(piv[0],'t')

    else:
        piv = [mc.createNode('transform', n=node+'Pivot')]
        mc.parent(piv, par)

    #snap to node
    mc.delete(mc.parentConstraint(node, par))
    mc.delete(mc.parentConstraint(node, neg))

    # connect negs
    md = mc.createNode('multiplyDivide', n=piv[0]+'_md')
    mc.setAttr(md+'.input2X', -1)
    mc.setAttr(md+'.input2Y', -1)
    mc.setAttr(md+'.input2Z', -1)

    mc.connectAttr(piv[0]+'.t', md+'.i1')
    mc.connectAttr(md+'.o', neg+'.t')
    mc.connectAttr(piv[0]+'.t', par+'.t')

    #parent stuff
    if parent is not None:
        mc.parent(par, parent)

    mc.parent(node, par)
    mc.xform(node, a=1,t=[0,0,0])
    mc.parent(neg, node)
    mc.parent(piv, neg)

    if kids is not None:
        for k in kids:
            mc.parent(k, neg)

    if not ctrl:
        mc.connectAttr(par+'.t', md+'.i1', f=1)
        mc.delete(piv)
        mc.rename(par, piv[0])

    return piv[0]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def addRoll(node, axis='ry', refObj=None):
    """

    :param node:
    :param axis:
    :param refObj:
    :return:
    """
    # create roll bridge
    loc = aboutPublic.snapLoc(node, name=node+'_roll_loc')
    locGrp = aboutPublic.createParentGrp(loc, 'zero', nodeType='group')

    if not refObj:
        mc.delete(mc.parentConstraint(node, locGrp))
    else:
        if mc.objExists(refObj):
            mc.delete(mc.parentConstraint(refObj, locGrp))

    # get node child objects
    childs = mc.listRelatives(node, typ='transform')
    mc.parent(childs, loc)
    mc.parent(locGrp, node)

    # connect roll axis
    mc.addAttr(node, longName='roll', k=1, dv=0)
    mc.connectAttr(node+'.roll', loc+'.'+axis)

    # clean
    locShape = mc.listRelatives(loc, typ='shape')
    mc.hide(locShape)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# tag keyable attrs
def tagKeyable(nodes, at, add=False):

    attrs = ''
    nodes = mc.ls(nodes)
    
    at = ' '+at+' '
    at = re.sub(' t ', ' tx ty tz ', at)
    at = re.sub(' r ', '  ry rz ', at)
    at = re.sub(' s ', ' sx sy sz ', at)
    at = at.strip()
    # Result: ' tx ty tz  ry rz sx sy sz '

    for node in nodes:
        if not(mc.objExists(node+'.tagKeyable')):
            mc.addAttr(node, ln="tagKeyable", dt="string")

        attrs = at
        if add:
            attrs = mc.getAttr(node+'.tagKeyable')+' '+at

        attrs.replace('  ', ' ').strip()
        mc.setAttr(node+'.tagKeyable', attrs, type='string')

    return attrs

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def untag(nodes=None):
    if not nodes:
        nodes = mc.ls(sl=1)
    nodes = mc.ls(nodes)

    for node in nodes:

        # noinspection PyBroadException
        try:
            mc.deleteAttr(node+'.tagKeyable')
        except:
            pass

        # noinspection PyBroadException
        try:
            mc.deleteAttr(node+'.controlID')
        except:
            pass

        # noinspection PyBroadException
        try:
            mc.deleteAttr(node+'.tag')
        except:
            pass

        # noinspection PyBroadException
        try:
            mc.deleteAttr(node+'.tagSpaces')
        except:
            pass


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def mirrorCtrl(orig='', scaleMode=True):

    # get real control curve.
    # you can select controller or it's groups.
    if not orig:
        sel = mc.ls(sl=1)
        if sel:
            s = sel[0].replace('_sdk','').replace('_con','').replace('_axis','').replace('_grp','')
            if mc.objExists(s):
                sel[0] = s
                mc.select(sel[0])

            if mc.objExists(sel[0]+'.controlID'):
                orig = sel[0]

    if not mc.objExists(orig+'.controlID'):
        return

    # mirror name
    sideKeyDict = {'L_':'R_', 'R_':'L_',
                   'lf_':'rt_', 'rt_':'lf_'}

    mctrl = ''
    for key in sideKeyDict.keys():
        if orig.startswith(key):
            mctrl = orig.replace(key, sideKeyDict[key])
            break
        else:
            return

    # mirror control
    if not mc.objExists(mctrl):
        mctrls = duplicateCtrl(orig, mctrl)
    else:
        mctrls = [mctrl+'_grp', mctrl+'_axis', mctrl+'_con', mctrl+'_sdk', mctrl]

    # mirror axis
    if scaleMode:
        # help group
        grp = mc.createNode('transform')
        mc.parent(mctrls[0], grp)
        mc.setAttr(grp+'.sx', -1)
        # set axis
        mc.parent(mctrls[0], w=1)
        #clean
        mc.delete(grp)

    return mctrls


#--------------------------------------------------------------------------------------------------------------------------------------------------------------
@undoable
def reverseCtrl(ctrl, useShape='', t=False):

    if t:
        mc.setAttr(ctrl+'_grp.sx', -1)
        if useShape and mc.objExists(useShape):
            copyShape([useShape, ctrl])

    else:
        tmp = mc.createNode('joint')
        mc.delete(mc.parentConstraint(ctrl+'_grp', tmp))
        mc.select(tmp)
        mj = mc.mirrorJoint(mirrorYZ=1, mirrorBehavior=1)

        mc.xform(ctrl+'_grp', ws=1, ro=[0,0,0])
        mc.delete(mc.orientConstraint(mj[0], ctrl+'_axis'))
        mc.setAttr(ctrl+'_grp.sx', -1)

        if useShape and mc.objExists(useShape):
            copyShape([useShape, ctrl])

        mc.delete(tmp, mj)
