# -*- coding: utf-8 -*-
from cgrig.libs.maya.mayacommand import command



class AdditiveFKDeleteCommand(command.CgRigCommandMaya):
    id = "cgrig.maya.additiveFk.delete"
    isUndoable = True

    _modifier = None

    def doIt(self, meta=None, bake=False, message=True):
        """ Bake the controls

        :type meta: :class:`metaadditivefk.CgRigMetaAdditiveFk`
        :return:
        :rtype: :class:`metaadditivefk.CgRigMetaAdditiveFk`

        """

        meta.deleteSetup(bake=bake)
