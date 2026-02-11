# -*- coding: utf-8 -*-
from collections import OrderedDict

from cgrig.libs.maya.mayacommand import mayaexecutor as executor
from cgrig.libs.maya.cmds.meta.metaadditivefk import CgRigMetaAdditiveFk
from cgrig.libs.maya.markingmenu import menu
from cgrig.libs.maya.meta import base
from cgrig.libs.utils.general import uniqify


class AdditiveFKMarkingMenuCommand(menu.MarkingMenuCommand):
    """ Additive fk Marking menu command
    """
    id = "additiveFkRigMarkingMenu"  # a unique identifier for a class, should never be changed
    creator = "CgRigtools"

    @staticmethod
    def uiData(arguments):
        """

        :param arguments:
        :type arguments:
        :return:
        :rtype:
        """
        ret = {"icon": "",
               "label": "",
               "bold": False,
               "italic": False,
               "optionBox": False,
               "optionBoxIcon": ""
               }

        op = arguments['operation']
        if op == "toggleControls":
            meta = base.metaNodeFromZApiObjects(arguments['nodes'])[-1]  # type: CgRigMetaAdditiveFk
            ret['checkBox'] = not meta.controlsHidden()

        return ret

    def execute(self, arguments):
        """The main execute methods for the joints marking menu. see executeUI() for option box commands

        :type arguments: dict
        """
        metaNodes = base.metaNodeFromZApiObjects(arguments['nodes'])[-1]  # type: CgRigMetaAdditiveFk
        operation = arguments.get("operation", "")

        for m in metaNodes:

            if operation == "delete":
                executor.execute("cgrig.maya.additiveFk.delete", meta=m)
            if operation == "bake":
                executor.execute("cgrig.maya.additiveFk.delete", meta=m, bake=True)
            elif operation == "toggleControls":
                m.toggleControls()





