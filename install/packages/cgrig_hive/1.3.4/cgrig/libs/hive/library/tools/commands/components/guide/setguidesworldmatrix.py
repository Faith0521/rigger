from cgrig.libs.hive import api as hiveapi
from cgrig.libs.maya.mayacommand import command

from cgrig.libs.utils import general
if general.TYPE_CHECKING:
    from cgrig.libs.maya import zapi


class HiveSetGuideWorldMatrices(command.CgRigCommandMaya):
    """Sets guides worldMatrices
    """
    id = "hive.component.guide.setGuideWorldMatrix"
    
    isUndoable = True
    isEnabled = True
    _nodes = []
    _matrices = []
    _originalData = []

    def resolveArguments(self, arguments):
        super(HiveSetGuideWorldMatrices, self).resolveArguments(arguments)
        guides = arguments.get("guides") # type: list[zapi.DagNode]
        matrices = arguments.get("matrices")  # type: list[zapi.Matrix]
        if len(guides) != len(matrices):
            self.cancel("Provided nodes and matrices aren't the same length")
            return
        for n in guides:
            self._originalData.append((n, n.worldMatrix()))
        self._nodes = guides
        self._matrices = matrices
        return arguments

    def doIt(self, guides=None, matrices=None):
        hiveapi.setGuidesWorldMatrix(self._nodes, self._matrices)

    def undoIt(self):
        guides = [i for i, _ in self._originalData]
        matrices = [i for _, i in self._originalData]
        hiveapi.setGuidesWorldMatrix(guides, matrices)
