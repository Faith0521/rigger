# -*- coding: utf-8 -*-
from maya import cmds
from maya.api import OpenMaya as om2
from cgrig.libs.maya.cmds.rig import jointsalongcurve
from cgrig.libs.maya import zapi
from cgrig.libs.maya.mayacommand import command


class JointsAlongCurveCommand(command.CgRigCommandMaya):
    """Joints along curve that is undoable
    """
    id = "cgrig.maya.jointsAlongCurve"
    isUndoable = True
    useUndoChunk = False
    disableQueue = True

    _modifier = None
    _jointsList = None

    def resolveArguments(self, arguments):
        self._curve = zapi.nodeByName(arguments['splineCurve'])
        return arguments

    def doIt(self, **kwargs):
        """ Bake the controls

        :return:
        :rtype: list[:class:`DagNode`]

        """
        jointList = jointsalongcurve.jointsAlongACurve(**kwargs)
        self._jointsList = list(zapi.nodesByNames(jointList))
        return jointList

    def undoIt(self):
        """ Delete the joints if it exists

        :return:
        :rtype:
        """
        if self._jointsList:
            cmds.delete(zapi.fullNames(self._jointsList))
            self._curve.show()


class JointsAlongCurveSelectedCommand(command.CgRigCommandMaya):
    """Joints along curve that is undoable
    """
    id = "cgrig.maya.jointsAlongCurve.selected"
    isUndoable = True
    useUndoChunk = False
    disableQueue = True

    _modifier = None
    _jointsList = None

    def doIt(self, **kwargs):
        """ Bake the controls

        :return:
        :rtype: list[:class:`DagNode`]

        """
        jointList = jointsalongcurve.jointsAlongACurveSelected(**kwargs)[0]
        self._jointsList = list(zapi.nodesByNames(jointList))
        return jointList

    def undoIt(self):
        """ Delete the joints if it exists

        :return:
        :rtype:
        """
        if self._jointsList:
            cmds.delete(zapi.fullNames(self._jointsList))


class JointsAlongCurveRebuildCommand(command.CgRigCommandMaya):
    """Joints along curve that is undoable
    """
    id = "cgrig.maya.jointsAlongCurve.rebuild"
    isUndoable = True
    useUndoChunk = True
    disableQueue = False

    _modifier = None
    _jointsList = None

    def doIt(self, **kwargs):
        """ Bake the controls

        :return:
        :rtype: list[:class:`DagNode`]

        """
        jointList = jointsalongcurve.rebuildSplineJointsSelected(**kwargs)
        # self._jointsList = list(zapi.nodesByNames(jointList))
        return jointList

    def undoIt(self):
        """ Delete the joints if it exists

        :return:
        :rtype:
        """


class JointsOnCurveCommand(command.CgRigCommandMaya):
    """This command Creates a meta node from the registry.
    """
    id = "cgrig.maya.jointsOnCurve"
    isUndoable = True
    useUndoChunk = False
    disableQueue = True

    _modifier = None
    _jointsList = None

    def doIt(self, **kwargs):
        """ Build the curve joints based on meta

        :return:
        :rtype:

        """
        jointList = jointsalongcurve.jointsSplineAlongACurve(**kwargs)
        self._jointsList = list(zapi.nodesByNames(jointList))
        return jointList

    def undoIt(self):
        """ Delete the joints if it exists

        :return:
        :rtype:
        """
        if self._jointsList:
            cmds.delete(zapi.fullNames(self._jointsList))