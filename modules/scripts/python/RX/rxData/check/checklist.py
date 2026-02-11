import modelChecks
import rigChecks

def load():

    # DATA - set( Label, Function, Fix Function)
    # Difference rig type has different check list.
    checkList = { 'model': [
                ('Check for referenced nodes', modelChecks.refNodes,),
                ('Check for namespaces', modelChecks.namespaces),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for single model hierarchy', modelChecks.singleHi),
                ('Check for bad model names', modelChecks.checkBadShapes, modelChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', modelChecks.layers, 'Remove Layers'),
                ('Check all history', modelChecks.deleteCh, 'Remove History')],

                'rig':[
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

                'gameRig': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

                'mocapRig': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)],

                'other': [
                ('Check for referenced nodes', rigChecks.refNodes,),
                ('Check for namespaces', rigChecks.namespaces),
                ('Check for lights, cameras & image planes', modelChecks.camsLightsImgPlanes, modelChecks.camsLightsImgPlanesfix, 'Remove Lights, Cams & IPs'),
                ('Check render & display layers', rigChecks.layers, 'Remove Layers'),
                ('Check for single rig hierarchy', rigChecks.singleHi),
                ('Check for single model hierarchy', rigChecks.checkModelHi),
                ('Check for same node name', modelChecks.sameNames, modelChecks.sameNamesFixUI, 'Fix Same Names'),
                ('Check for bad model names', rigChecks.checkBadShapes, rigChecks.fixBadShapes, 'Fix Shape Names'),
                ('Check & create anim control ID Tags', rigChecks.checkCtrls),
                ('Check rig Animation', rigChecks.playCheck)]

                }


    return checkList