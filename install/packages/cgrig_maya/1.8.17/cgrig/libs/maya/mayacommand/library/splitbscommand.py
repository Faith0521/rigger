# -*- coding: utf-8 -*-
from maya import cmds

# from cgrig.libs.maya.cmds.rig import jointsalongcurve
from cgrig.libs.maya import zapi
from cgrig.libs.maya.mayacommand import command


class SplitBsCommand(command.CgRigCommandMaya):
    """Joints along curve that is undoable
    """
    id = "cgrig.maya.splitBlendShape"
    isUndoable = True
    useUndoChunk = False
    disableQueue = True

    _modifier = None

    def resolveArguments(self, arguments):
        return arguments

    def doIt(self, **kwargs):
        """ Bake the controls

        :return:
        :rtype: list[:class:`DagNode`]

        """
        pass

    def undoIt(self):
        """ Delete the joints if it exists

        :return:
        :rtype:
        """
        pass


