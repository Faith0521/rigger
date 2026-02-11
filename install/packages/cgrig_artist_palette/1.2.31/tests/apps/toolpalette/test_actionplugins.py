# -*- coding: utf-8 -*-
from cgrig.libs.utils import unittestBase
from cgrig.apps.toolpalette import run
from cgrig.apps.toolpalette import default_actions
from cgrig.apps.toolpalette import palette
from cgrig.core.util import zlogging

try:
    from unittest import mock
except ImportError:
    from cgrigvendor import mock


class TestDefaultActions(unittestBase.BaseUnitest):

    def setUp(self):
        self.instance = run.currentInstance()
        if self.instance is None:
            self.instance = run.load()

    def test_loadsDefaultActions(self):
        actions = self.instance.typeRegistry.getPlugin("action")  # type: palette.ActionType
        plugins = list(actions.plugins())
        self.assertTrue(default_actions.ToggleCgRigLogging.id in plugins)
        self.assertTrue(default_actions.HelpIconShelf.id in plugins)
        self.assertTrue(default_actions.ResetAllWindowPosition.id in plugins)

    def test_helpCallsWebBrowser(self):

        for variant in default_actions.HelpIconShelf._ADDRESSES:
            with mock.patch("webbrowser.open") as mockwbopen:
                self.instance.executePluginById(default_actions.HelpIconShelf.id, variant=variant)
                self.assertTrue(mockwbopen.called)

    def test_loggingTogglesDebugMode(self):
        """Tests the toggling of debug logging through the action works.
        """
        zlogging.setGlobalDebug(False)  # actual core test is in cgrigTools main repo
        self.instance.executePluginById(default_actions.ToggleCgRigLogging.id)
        self.assertTrue(zlogging.isGlobalDebug())
        self.instance.executePluginById(default_actions.ToggleCgRigLogging.id)
        self.assertFalse(zlogging.isGlobalDebug())
