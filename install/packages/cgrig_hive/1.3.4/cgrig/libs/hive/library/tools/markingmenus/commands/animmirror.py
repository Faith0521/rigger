from cgrig.libs.maya.markingmenu import menu
from cgrig.core.util import zlogging

from cgrig.libs.hive.anim import mirroranim
from cgrig.apps.toolsetsui.run import openToolset

logger = zlogging.getLogger(__name__)


class AnimMirror(menu.MarkingMenuCommand):
    id = "hiveAnimMirror"
    creator = "CgRigtools"

    def execute(self, arguments):
        """Mirrors animation or a pose on the selected controls.

        :type arguments: dict
        """
        mirroranim.flipPoseCtrlsSelected(flip=False, animation=arguments["animation"])


class AnimFlipMirror(menu.MarkingMenuCommand):
    id = "hiveAnimFlipMirror"
    creator = "CgRigtools"

    def execute(self, arguments):
        """Flip Mirrors animation or a pose on the selected controls.

        :type arguments: dict
        """
        mirroranim.flipPoseCtrlsSelected(flip=True, animation=arguments["animation"])


class OpenMirrorWindow(menu.MarkingMenuCommand):
    id = "hiveOpenMirrorWindow"
    creator = "CgRigtools"

    def execute(self, arguments):
        """Opens the Hive Mirror Flip Animation Toolset

        :type arguments: dict
        """
        openToolset("hiveMirrorPasteAnim", advancedMode=False)