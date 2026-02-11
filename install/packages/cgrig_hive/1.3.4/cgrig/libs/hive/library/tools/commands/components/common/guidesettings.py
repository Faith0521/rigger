from cgrig.libs.maya.mayacommand import command
from cgrig.libs.hive import api


class UpdateGuideSettings(command.CgRigCommandMaya):
    """Update component guide settings
    """
    id = "component.guides.setting.update"

    
    isUndoable = True
    _component = None  # type: api.Component
    _settings = {}
    _originalSettings = {}

    def resolveArguments(self, arguments):
        component = arguments.get("component")
        self._component = component
        self._settings = arguments["settings"]
        return arguments

    def doIt(self, component=None, settings=None):
        """ Execute update guide settings

        :type component: :class:`cgrig.libs.hive.base.component.Component`
        """
        self._originalSettings = self._component.updateGuideSettings(self._settings)

    def undoIt(self):
        if self._component.exists():
            self._component.updateGuideSettings(self._originalSettings)
