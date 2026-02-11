import os
import maya.cmds as cmds
import pymel.core as pm
from pymel.core import mel

cmds.select(allDagObjects = 1)
file_name = cmds.ls(sl = 1)
def export_fbx(export_fbx_file, start_frame, end_frame, step, namespace):
        export_folder = os.path.dirname(export_fbx_file)
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        #load_plugin('fbxmaya')

        name = os.path.basename(pm.sceneName())
        shot_name = name.split('_ani_')[0].split('_', 1)[-1]

        mel.FBXLoadMBExportPresetFile()
        mel.FBXExportFileVersion(v="FBX201400")
        mel.FBXExportSmoothingGroups(v=True)
        mel.FBXExportHardEdges(v=False)
        mel.FBXExportTangents(v=False)
        mel.FBXExportSmoothMesh(v=True)
        mel.FBXExportInstances(v=False)
        mel.FBXExportReferencedAssetsContent(v=False)
        mel.FBXExportBakeComplexAnimation(v=True)
        mel.FBXExportBakeComplexStart(v=int(start_frame))
        mel.FBXExportBakeComplexEnd(v=int(end_frame))
        mel.FBXExportBakeComplexStep(v=int(step))
        mel.FBXExportUseSceneName(v=False)
        mel.FBXExportQuaternion(v='euler')
        mel.FBXExportShapes(v=True)
        mel.FBXExportSkins(v=True)
        mel.FBXExportConstraints(v=False)
        mel.FBXExportCameras(v=False)
        mel.FBXExportLights(v=False)
        mel.FBXExportEmbeddedTextures(v=False)
        mel.FBXExportInputConnections(v=False)
        mel.FBXExportUpAxis("y")
        mel.FBXExportSplitAnimationIntoTakes(start_frame, end_frame, v='%s_%s' % (namespace, shot_name))
        mel.FBXExport(f=export_fbx_file, s=True)
start_frame = cmds.playbackOptions(q=1, min=1)
end_frame = cmds.playbackOptions(q=1, max=1)    
export_fbx(r"I:\proj\pj2019wj003\syncData\workgroup\Rig_Workgroup\ss\%s_hi_sklt.fbx"%(file_name[0]),start_frame,end_frame,1,'')