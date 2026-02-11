# -*- coding: utf-8 -*-
from cgrig.preferences.core import prefinterface
from cgrig.preferences.assets import BrowserPreference
from cgrig.core.util import zlogging


logger = zlogging.getLogger(__name__)


class ModelAssetsPreference(prefinterface.PreferenceInterface):
    id = "model_assets_interface"
    _relativePath = "prefs/maya/cgrig_model_assets.pref"

    def __init__(self, preference):
        super(ModelAssetsPreference, self).__init__(preference)
        self.modelAssetsPreference = BrowserPreference("model_assets", self)
