# -*- coding: utf-8 -*-

from cgrig.preferences import assets
from cgrig.preferences.core import prefinterface
from cgrig.core.util import zlogging


logger = zlogging.getLogger(__name__)


class MayaScenesPreference(prefinterface.PreferenceInterface):
    id = "maya_scenes_interface"
    _relativePath = "prefs/maya/cgrig_maya_scenes.pref"

    def __init__(self, preference):
        super(MayaScenesPreference, self).__init__(preference)
        self.scenesAssets = assets.BrowserPreference("maya_scenes", self)



