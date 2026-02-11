def source():
    rigType = ''
    return [rigType]
    
def functions(rigType = 'assetCustom'):
    func = []

    # ---------------------------------------------------------------------------------------------------- #
    func.append('Build Prep Build')
    func.append('assetPrep.build() :: Build Prep')
    func.append('{0}Custom.extraPrep() :: Custom Script: extra Prep'.format(rigType))

    # ---------------------------------------------------------------------------------------------------- #
    func.append('Build Control Rig')
    func.append('templateTools.getRigBuildType("anim") :: Rig Components')
    func.append('{0}Custom.extraControlRig() :: Custom Script: extra Control Rig'.format(rigType))

    if 'game' in rigType:
        func.append('assetCommon.controlBuild(game=True) :: Finalize Control Rig')
    else:
        func.append('assetCommon.controlBuild(game=False) :: Finalize Control Rig')

    # ---------------------------------------------------------------------------------------------------- #
    func.append('Custom Rig')
    func.append('customRigs.importRig() :: Import Custom Rigs')
    func.append('Import Model')
    func.append('assetImport.model() :: Import Model')
    func.append('assetCommon.connectLOD() :: Connect Model LODs')

    # ---------------------------------------------------------------------------------------------------- #
    func.append('Load Deformers')
    func.append('{0}Custom.extraPreBind() :: Custom Script: extra Start Bind'.format(rigType))

    func.append('assetCommon.importPoseDrivers() :: Import Pose Drivers')
    func.append('assetDeform.importDeformers(dtype="attrs") :: Import Custom Attributes')
    func.append('assetDeform.importDeformers(dtype="bs") :: Import Blendshapes')
    func.append('assetDeform.importDeformers(dtype="ffd") :: Import Lattices')
    func.append('assetDeform.importDeformers(dtype="scls") :: Import Skin Clusters')
    func.append('assetDeform.importDeformers(dtype="cls") :: Import Clusters')
    func.append('assetDeform.importConstraints() :: Import Constraints')
    func.append('assetDeform.importDeformers(dtype="sdk") :: Import Set Driven Keys')
    func.append('assetDeform.importDeformers(dtype="stack") :: Set Deformer Stack')
    func.append('{0}Custom.extraEndBind() :: Custom Script: extra End Bind'.format(rigType))

    # ---------------------------------------------------------------------------------------------------- #
    func.append('Finalize Rig')
    func.append('assetCommon.lockRig() :: Clean + Lock + Create Sets')
    func.append('{0}Custom.extraFinal() :: Custom Script: extra Final'.format(rigType))
    return func
