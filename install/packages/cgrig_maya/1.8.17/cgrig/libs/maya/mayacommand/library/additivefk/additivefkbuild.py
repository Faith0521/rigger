# -*- coding: utf-8 -*-
from cgrig.libs.maya.cmds.meta import metaadditivefk
from cgrig.libs.maya.mayacommand import command
from cgrig.libs.maya import zapi
from cgrig.libs.maya.cmds.objutils.joints import getJointChain


class AdditiveFKBuildCommand(command.CgRigCommandMaya):
    """This command Creates a meta node from the registry.
    """
    id = "cgrig.maya.additiveFk.build"
    isUndoable = True
    _modifier = None

    def doIt(self, joints=None, startJoint=None, endJoint=None, controlSpacing=1, rigName="additive", message=True):
        """ Bake the controls

        :type meta: :class:`metaadditivefk.CgRigMetaAdditiveFk`
        :return:
        :rtype: :class:`metaadditivefk.CgRigMetaAdditiveFk`

        """
        if joints is None:
            joints = zapi.nodesByNames(getJointChain(startJoint.fullPathName(), endJoint.fullPathName()))
        self.meta = metaadditivefk.CgRigMetaAdditiveFk()
        self.meta.createAdditiveFk(zapi.fullNames(joints), rigName=rigName, controlSpacing=controlSpacing)
        return self.meta

    def undoIt(self):
        """ Undo

        :return:
        :rtype:
        """

        self.meta.deleteSetup(message=False) if self.meta else None
