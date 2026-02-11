from cgrig.libs.maya.mayacommand import command
from cgrig.libs.hive.base import rig as hiverig


class RenameRigCommand(command.CgRigCommandMaya):
    """Rename's the rig instance
    """
    id = "hive.rig.rename"

    isUndoable = True

    _rig = None
    _oldName = ""

    def resolveArguments(self, arguments):
        rig = arguments.get("rig")
        name = arguments.get("name")
        if not rig:
            self.displayWarning("Must supply rig instance ")
            return
        if not name:
            self.displayWarning("Must specify a valid name parameter")
            return
        self._rig = rig
        self._oldName = rig.name()
        return arguments

    def doIt(self, rig=None, name=None):
        rig.rename(name)

    def undoIt(self):
        if self._rig is not None and self._oldName:
            self._rig.rename(self._oldName)
