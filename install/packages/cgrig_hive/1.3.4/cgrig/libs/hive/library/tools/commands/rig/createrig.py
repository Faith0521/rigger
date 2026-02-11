from cgrig.libs.maya.mayacommand import command
from cgrig.libs.hive import api
from maya import cmds

class CreateRigCommand(command.CgRigCommandMaya):
    id = "hive.rig.create"

    isUndoable = False
    isEnabled = True
    _rig = None


    def resolveArguments(self, arguments):
        arguments["namespace"] = arguments.get("namespace", None)
        name = arguments.get("name")
        # guard against name being an empty string switch .get doesn't deal with
        if not name:
            name = "HiveRig"
        arguments["name"] = api.naming.uniqueNameForRig(api.iterSceneRigs(), name)
        return arguments

    def doIt(self, name=None, namespace=None):
        _currentDisplayLayer = cmds.editDisplayLayerGlobals(query=True, useCurrent=False)
        try:
            cmds.editDisplayLayerGlobals(useCurrent=False)
            rig = api.Rig()
            self._rig = rig
            rig.startSession(name, namespace=namespace)
        finally:
            cmds.editDisplayLayerGlobals(useCurrent=_currentDisplayLayer)
        return rig
