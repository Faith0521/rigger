import maya.cmds as mc
import maya.mel as mel
import numpy as np
import time
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


class deformer_manager(object):

    @staticmethod
    def loadTextField(tfName=''):

        objsel = mc.ls(sl=True, fl=True)

        fillCon = ''
        num = 0
        for obj in objsel:
            if num == 0:
                fillCon = obj
            else:
                fillCon = fillCon + ' ' + obj
            num = num + 1
        mc.textField(tfName, e=True, text=fillCon)

    @staticmethod
    def listSkinCluster(inputMesh=''):
        obj = inputMesh
        skinNode = mel.eval("findRelatedSkinCluster" + "(\"" + obj + "\")")
        if skinNode != '':
            return skinNode
        else:
            return False

    def deformer_manager_UI(self):
        deformer_manager_UI = 'deformer_manager_UI'
        if mc.window(deformer_manager_UI, ex=True):
            mc.deleteUI(deformer_manager_UI)

        mc.window(deformer_manager_UI, widthHeight=(450, 400), t=deformer_manager_UI, menuBar=True, rtf=True, s=True)

        main = mc.columnLayout('mdlar_SDK_main', columnAttach=('both', 5), rowSpacing=10, columnWidth=450)

        split_BS_frame = mc.frameLayout('splitBS_frameLY', label='BS_split_mdlar', borderStyle='in', collapsable=False,
                                        bgc=(0.1, 0.1, 0.1), font='boldLabelFont')

        mc.rowLayout('splitBS01_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])

        mc.text(' orgMesh : ')
        mc.textField('load_OrgMesh_textField', text='')
        mc.button('load_splitBS_orgMesh', l='load', c=lambda *args: self.loadTextField('load_OrgMesh_textField'))

        mc.setParent(split_BS_frame)

        mc.rowLayout('splitBS02_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])

        mc.text(' BS_Mesh : ')
        mc.textField('load_BS_Mesh_textField', text='')
        mc.button('load_splitBS_BS_Mesh', l='load', c=lambda *args: self.loadTextField('load_BS_Mesh_textField'))

        mc.setParent(split_BS_frame)

        mc.rowLayout('splitBS03_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])

        mc.text(' skin_Mesh : ')
        mc.textField('load_skin_Mesh_textField', text='')
        mc.button('load_splitBS_skin_Mesh', l='load', c=lambda *args: self.loadTextField('load_skin_Mesh_textField'))

        mc.setParent(split_BS_frame)
        mc.button('splitBS_bt', l='modify', c=lambda *args: self.splitBS_for_UI())

        mc.setParent(main)
        mc.separator(style='none')

        mirrorDeformer_frame = mc.frameLayout('mirrorDeformer_frameLY', label='mirrorDeformer_mdlar', borderStyle='in',
                                              collapsable=False, bgc=(0.1, 0.1, 0.1), font='boldLabelFont')

        mc.rowLayout('mirrorDeformer01_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])

        mc.text(' orgMesh : ')
        mc.textField('load_deformerMesh_textField', text='')
        mc.button('load_splitBS_orgMesh', l='load', c=lambda *args: self.loadTextField('load_deformerMesh_textField'))

        mc.setParent(mirrorDeformer_frame)

        mc.rowLayout('mirrorDeformer02_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])
        mc.text(' inputDeformer : ')
        mc.textField('load_inputDeformer_textField', text='')
        mc.button('load_inputDeformer_orgMesh', l='load',
                  c=lambda *args: self.loadTextField('load_inputDeformer_textField'))

        mc.setParent(mirrorDeformer_frame)

        mc.rowLayout('mirrorDeformer03_rowLY', numberOfColumns=3, columnWidth3=(100, 250, 100), adjustableColumn=3,
                     columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0)])
        mc.text(' mirrorDeformer : ')
        mc.textField('load_mirrorDeformer_textField', text='')
        mc.button('load_mirrorDeformer_orgMesh', l='load',
                  c=lambda *args: self.loadTextField('load_mirrorDeformer_textField'))

        mc.setParent(mirrorDeformer_frame)

        mc.rowLayout('mirrorDeformer04_rowLY', numberOfColumns=4, columnWidth4=(100, 80, 80, 10), adjustableColumn=4,
                     columnAlign=(1, 'right'),
                     columnAttach=[(1, 'both', 0), (2, 'both', 0), (2, 'both', 0), (2, 'both', 0)])
        mc.text(' mirrorAxis : ')
        mc.optionMenu('posneg_menu', label='  ', w=60)

        mc.menuItem(label='+')
        mc.menuItem(label='-')

        mc.optionMenu('axis_menu', label='  ', w=100)

        mc.menuItem(label='X')
        mc.menuItem(label='Y')
        mc.menuItem(label='Z')

        mc.setParent(mirrorDeformer_frame)
        mc.button('mirrorDeformer_bt', l='modify', c=lambda *args: self.mirrorDeformer_forUI())

        mc.showWindow(deformer_manager_UI)

    ###===================================================================================================================

    def splitBS_for_UI(self):

        bsMesh = mc.textField('load_BS_Mesh_textField', q=True, text=True)
        orgMesh = mc.textField('load_OrgMesh_textField', q=True, text=True)
        skinmesh = mc.textField('load_skin_Mesh_textField', q=True, text=True)

        skinNode = self.listSkinCluster(inputMesh=skinmesh)

        jnts = mc.skinCluster(skinNode, q=True, inf=True)
        self.splitBlendshape(inputBSMesh=bsMesh, orgMesh=orgMesh, skinMesh=skinmesh, jointInput=jnts)

    def mirrorDeformer_forUI(self):

        deformerMesh = mc.textField('load_deformerMesh_textField', q=True, text=True)
        deformer_input = mc.textField('load_inputDeformer_textField', q=True, text=True)
        deformer_mirror = mc.textField('load_mirrorDeformer_textField', q=True, text=True)

        posneg = mc.optionMenu('posneg_menu', q=True, v=True)
        Axis = mc.optionMenu('axis_menu', q=True, v=True)

        if posneg == '+':
            posneg_value = 0
        else:
            posneg_value = 1

        if deformer_input == deformer_mirror:
            lonly = 1
        else:
            lonly = 0

        self.mirrorDerformerWeight(inputMesh=deformerMesh, inputDerformer=deformer_input,
                                   mirrorDeformer=deformer_mirror, mirrorAxis=Axis, ifRverse=posneg_value,
                                   ifLonly=lonly)

    def mirrorDerformerWeight(self, inputMesh='', inputDerformer='', mirrorDeformer='', mirrorAxis='X', ifRverse=0,
                              ifLonly=0):

        meshTemple = str(inputMesh) + '_mirrorTemple'
        mc.duplicate(inputMesh, n=meshTemple)

        baseJnt = str(inputMesh) + '_templeBaseJnt'
        mc.select(cl=True)
        mc.joint(n=baseJnt)

        if ifLonly == 0:

            targetMesh = str(inputMesh) + '_mirrorMesh'
            mc.duplicate(inputMesh, n=targetMesh)
            mc.setAttr(str(targetMesh) + '.scaleX', lock=False)
            mc.setAttr(str(targetMesh) + '.scaleX', -1)

            L_mirrorJnt = 'L_' + str(inputMesh) + '_templeJnt'

            R_mirrorJnt = 'R_' + str(inputMesh) + '_templeJnt'

            mc.select(cl=True)
            mc.joint(n=L_mirrorJnt)

            mc.select(cl=True)
            mc.joint(n=R_mirrorJnt)

            if mirrorAxis == 'X':
                mc.setAttr(str(L_mirrorJnt) + '.translateX', 1)
                mc.setAttr(str(R_mirrorJnt) + '.translateX', 1)

            elif mirrorAxis == 'Y':
                mc.setAttr(str(L_mirrorJnt) + '.translateY', 1)
                mc.setAttr(str(R_mirrorJnt) + '.translateY', 1)
            else:
                mc.setAttr(str(L_mirrorJnt) + '.translateZ', 1)
                mc.setAttr(str(R_mirrorJnt) + '.translateZ', 1)

            skinInfo = mc.skinCluster(baseJnt, meshTemple, normalizeWeights=3)

            targetskinInfo = mc.skinCluster(baseJnt, targetMesh, normalizeWeights=3)

            mc.skinCluster(skinInfo[0], e=True, ug=True, dr=5, ps=0, ns=10, lw=True, wt=0, ai=[L_mirrorJnt])

            mc.skinCluster(targetskinInfo[0], e=True, ug=True, dr=5, ps=0, ns=10, lw=True, wt=0, ai=[R_mirrorJnt])

            mc.setAttr(str(skinInfo[0]) + '.envelope', 0)
            mc.setAttr(str(targetskinInfo[0]) + '.envelope', 0)

            self.deformer_2_skin(skinNode=skinInfo[0], skinMesh=meshTemple, wireMesh=inputMesh, infJoint=L_mirrorJnt,
                                 deformerNode=inputDerformer)

            mc.copySkinWeights(ss=skinInfo[0], ds=targetskinInfo[0], surfaceAssociation='closestPoint',
                               influenceAssociation='closestJoint', noMirror=True)

            self.setSkinValue_2_deformer_OnMesh(skinNode=targetskinInfo[0], skinMesh=targetMesh, wireMesh=inputMesh,
                                                infJoint=R_mirrorJnt, deformerNode=mirrorDeformer)

            mc.delete(meshTemple, baseJnt, L_mirrorJnt, R_mirrorJnt)
        else:
            mirrorJnt = str(inputMesh) + '_templeJnt'

            mc.select(cl=True)
            mc.joint(n=mirrorJnt)

            mc.setAttr(str(mirrorJnt) + '.translateY', 1)

            skinInfo = mc.skinCluster(baseJnt, meshTemple, normalizeWeights=3)
            mc.setAttr(str(skinInfo[0]) + '.skinningMethod', 2)
            mc.skinCluster(skinInfo[0], e=True, ug=True, dr=5, ps=0, ns=10, lw=True, wt=0, ai=[mirrorJnt])
            mc.setAttr(str(skinInfo[0]) + '.envelope', 0)
            self.deformer_2_skin(skinNode=skinInfo[0], skinMesh=meshTemple, wireMesh=inputMesh, infJoint=mirrorJnt,
                                 deformerNode=inputDerformer)

            if mirrorAxis == 'X':
                mAxis = 'YZ'
            elif mirrorAxis == 'Y':
                mAxis = 'XZ'
            else:
                mAxis = 'XY'

            mc.copySkinWeights(ss=skinInfo[0], ds=skinInfo[0], mirrorInverse=True, mirrorMode=mAxis)

            self.setSkinValue_2_deformer_OnMesh(skinNode=skinInfo[0], skinMesh=meshTemple, wireMesh=inputMesh,
                                                infJoint=mirrorJnt, deformerNode=mirrorDeformer)

            mc.delete(mirrorJnt, baseJnt, meshTemple)

    ### ==================================================================================================================
    def getinputWireDeformer(self, inputMesh=''):
        inputHistory = mc.listHistory(inputMesh, lv=1)
        wire_all = []
        for ih in inputHistory:
            if mc.nodeType(ih) == 'wire':
                wire_all.append(ih)

        return wire_all

    def setSkinValue_2_deformer_OnMesh(self, skinNode='', skinMesh='', wireMesh='', infJoint='', deformerNode=''):
        start_time = time.time()
        polyPoints = mc.polyEvaluate(skinMesh, v=True)
        for i in range(polyPoints):
            infJnt = mc.skinPercent(skinNode, '%s.vtx[%s]' % (skinMesh, i), query=True,
                                    t=None)  # per model inf joint list
            jntWet = mc.skinPercent(skinNode, '%s.vtx[%s]' % (skinMesh, i), query=True, v=True)  # per joint weight

            num = 0
            for inj in infJnt:
                if inj == infJoint:
                    weight = jntWet[num]
                    mc.percent(deformerNode, str(wireMesh) + '.vtx[' + str(i) + ']', v=weight)


                else:
                    pass
                num = num + 1

    def deformer_2_skin(self, skinNode='', skinMesh='', wireMesh='', infJoint='', deformerNode=''):
        polyPoints = mc.polyEvaluate(wireMesh, v=True)
        for i in range(polyPoints):
            weight = mc.percent(deformerNode, str(wireMesh) + '.vtx[' + str(i) + ']', q=True, v=True)

            mc.skinPercent(skinNode, '%s.vtx[%s]' % (skinMesh, i),
                           tv=(infJoint, weight[0]))  # per model inf joint list

    def get_polygon_points(self, mesh):
        selection_list = om.MSelectionList()
        selection_list.add(mesh)

        dag_path = selection_list.getDagPath(0)

        mesh_fn = om.MFnMesh(dag_path)

        points = mesh_fn.getPoints(om.MSpace.kWorld)

        return points

    def py_to_mArray(self, cls, _list):
        result = cls()
        for elem in _list:
            result.append(elem)
        return result

    def get_weights(self, mesh_name, skin_name, indices):
        selection = om.MSelectionList()
        selection.add(skin_name)
        selection.add(mesh_name + ".vtx[*]")

        skin_obj = selection.getDependNode(0)
        # mesh_dag = selection.getDagPath(1)
        mesh_dag, mesh_comp = selection.getComponent(1)
        fn_skin = oma.MFnSkinCluster(skin_obj)
        weights = fn_skin.getWeights(mesh_dag, mesh_comp, indices)

        return weights

    def get_py_weights(self, mesh_name):
        skin_cluster_name = mc.ls(mc.listHistory(mesh_name), type="skinCluster")[0]
        jointLength = len(mc.skinCluster(skin_cluster_name, q=1, inf=1))
        indices = self.py_to_mArray(om.MIntArray, range(jointLength))
        weights = self.get_weights(mesh_name, skin_cluster_name, indices)
        vtx_length = int(len(weights) / jointLength)
        weights = [weights[i] for i in range(len(weights))]
        weights = [weights[jointLength * vtx_id:jointLength * (vtx_id + 1)] for vtx_id in range(vtx_length)]
        return jointLength, weights

    def split_target_by_weights(self, org_points, target_points, weights):
        vectors = target_points - org_points
        weights = weights.transpose(1, 0)
        split_vec = weights[:, :, None] * vectors[None]
        split_points = org_points + split_vec
        return split_points

    def set_mesh_points(self, mesh_name, points):
        selection_list = om.MSelectionList()
        selection_list.add(mesh_name)

        dag_path = selection_list.getDagPath(0)

        mesh_fn = om.MFnMesh(dag_path)

        mesh_fn.setPoints(om.MPointArray(points), om.MSpace.kWorld)

        mesh_fn.updateSurface()

    ### ==================================================================================================================
    def splitBlendshape(self, inputBSMesh='', orgMesh='', skinMesh='', jointInput=['']):
        org_points = np.array(self.get_polygon_points(orgMesh))
        target_points = np.array(self.get_polygon_points(inputBSMesh))

        jointLength, weights = self.get_py_weights(skinMesh)
        weights = np.array(weights)
        split_meshes = []
        for num in range(len(jointInput)):
            m = mc.duplicate(skinMesh)[0]
            split_meshes.append(m)
        result = self.split_target_by_weights(org_points, target_points, weights)
        for split_mesh, split_points in zip(split_meshes, result):
            self.set_mesh_points(split_mesh, split_points.tolist())

