# -*- coding: utf-8 -*-
from cgrig.libs.maya.mayacommand import command
from cgrig.libs.maya import zapi
from cgrig.libs.maya.cmds.meta import metasplinerig


class SplineRigSwitchCommand(command.CgRigCommandMaya):
    """This command switches the controls of the rig
    """
    id = "cgrig.maya.splinerig.switch"
    isUndoable = True

    _modifier = None
    _selected = []
    _meta = None

    def doIt(self, meta=None, switchTo=None):
        """ Switches the controls of the rig

        :param meta:
        :type meta: metasplinerig.MetaSplineRig
        :type switchTo: str
        :return: True if successful, false otherwise
        :rtype: bool
        """
        self._selected = list(zapi.selected())
        self._meta = meta
        switched = meta.switchControls(switchTo)

        return switched

    def undoIt(self):
        return
