"""Management of the component widget registry.
"""

import os

from cgrig.apps.hiveartistui import model
from cgrig.core.plugin import pluginmanager
from cgrig.core.util import zlogging
from cgrigvendor.Qt import QtCore

logger = zlogging.getLogger("hiveartistui")


class ComponentModelRegistry(QtCore.QObject):
    """Registry class to handle matching custom component model to hive component, this match is valid if the widget
    has the componentType class variable equal to a component Type.

    .. code-block:: python

        from cgrig.libs.api import configuration
        from cgrig.apps.hiveartistui.registries import registry
        config = configuration.Configuration()
        reg = registry.ComponentModelRegistry(config.componentRegistry())
        reg.discoverComponents()
        print reg.models
        # result: {'FkComponent': {'components': <class 'cgrig.libs.hivelibrary.components.fkcomponent.fkcomponent.FkComponent'>,
                 'widget': <class 'FKComponent.FKComponentWidget'>}}

    """
    registryEnv = "HIVE_COMPONENT_MODELS"

    def __init__(self, componentRegistry):
        """
        :param componentRegistry: The core hive api component registry instance
        :type componentRegistry:  :class:`cgrig.libs.hive.base.registry.ComponentRegistry`
        """
        self.componentRegistry = componentRegistry
        # {componentType: {"widget": :class:`ComponentWidget`,
        #                   "instance": :class:`cgrig.libs.hivebase.component.Component`}}
        self.models = {}
        # for discovering the component models
        self._manager = pluginmanager.PluginManager(interface=[model.ComponentModel], variableName="componentType")

    def discoverComponents(self):
        """Searches the component library specfied by the environment variable "CGRIG_HIVE_COMPONENT_PATH"
        """
        self.models = {}
        paths = os.environ[self.registryEnv].split(os.pathsep)
        if not paths:
            return False
        self._manager.registerPaths(paths)
        models = {m.componentType: {"model": m} for m in self._manager.plugins.values()}
        for hiveType, data in self.componentRegistry.components.items():
            if hiveType in models:
                models[hiveType].update({"component": data["object"],
                                         "type": hiveType})
            else:
                models[hiveType] = {"component": data["object"],
                                    "model": model.ComponentModel,
                                    "type": hiveType}
        self.models = models

        return True

    def findComponentModel(self, componentType):
        """Returns a matching component widget object.

        :param componentType: The hive component type
        :type componentType: str
        :return: A matching component model
        :rtype: :class::`cgrig.apps.hiveartistui.model.ComponentModel`
        """
        widgetInfo = self.models.get(componentType)
        if widgetInfo:
            return widgetInfo["model"], widgetInfo["type"]

    def findComponent(self, componentType):
        """Returns a matching component class

        :param componentType: The hive component type
        :type componentType: str
        :return: A matching hive component
        :rtype: :class::`cgrig.libs.hive.base.component.Component`
        """
        widgetInfo = self.models.get(componentType)
        if widgetInfo:
            return widgetInfo["component"]