# -*- coding: utf-8 -*-
from cgrig.core.util import zlogging

from cgrig.preferences.prefinterface import PreferenceInterface
from cgrig.preferences.assets import BrowserPreference

logger = zlogging.getLogger(__name__)


class ControlJointsPreferences(PreferenceInterface):
    id = "control_joints_interface"
    _relativePath = "prefs/maya/cgrig_controls_joints.pref"
    _settings = None

    def __init__(self, preference):
        super(ControlJointsPreferences, self).__init__(preference)
        self.controlAssets = BrowserPreference("control_shapes", self, fileTypes=["shape"])

    def updatePrefsKeys(self):
        """ Update any old prefs keys here

        :return:
        """
        return
