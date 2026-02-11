# -*- coding: utf-8 -*-
import os

from cgrig.libs.maya.utils import mayatestutils
from cgrig.libs.maya import triggers
from cgrig.libs.maya.triggers.triggerlib import selectioncommand
from cgrig.libs.maya.triggers import triggercallbackutils
from cgrig.libs.maya import zapi


class TestMayaTriggers(mayatestutils.BaseMayaTest):
    application = "maya"

    def setUp(self):
        self._reg = triggers.TriggerRegistry()
        self._testNode = zapi.createDag("TestTrigger", "transform")
        triggers.removeSelectionCallback()

    def test_defaultRegisteredPlugins(self):
        commands = self._reg.commands()
        self.assertTrue(len(commands.keys()), 2)
        self.assertTrue(triggers.MENU_COMMAND_TYPE in commands)
        self.assertTrue(triggers.SelectConnectedCommand.id in commands)

    def test_createSelectionTrigger(self):
        selectableNode = zapi.createDag("test", "transform")
        triggerNodes = triggers.createSelectionTrigger([self._testNode], "print('helloworld')",
                                                       connectables=[selectableNode]
                                                       )
        self.assertEqual(len(triggerNodes), 1)
        for n in triggerNodes:
            self.assertTrue(triggers.hasTrigger(self._testNode, strict=True))
            self.assertTrue(n.isCommandType(triggers.SelectConnectedCommand))

    def test_createMenuTrigger(self):
        triggerNodes = triggers.createMenuTriggers([self._testNode], None)
        self.assertEqual(len(triggerNodes), 1)
        for n in triggerNodes:
            self.assertTrue(triggers.hasTrigger(self._testNode, strict=True))
            self.assertTrue(n.isCommandType(triggers.TriggerMenuCommand))

    def test_deleteTriggers(self):
        triggerNodes = triggers.createMenuTriggers([self._testNode], None)
        self.assertEqual(len(triggerNodes), 1)
        triggers.deleteTriggers([self._testNode])
        self.assertFalse(triggers.hasTrigger(self._testNode))

    def test_mayaSelectionCallback(self):
        selectableNode = zapi.createDag("test", "transform")
        triggers.createSelectionTrigger([self._testNode], "import os; os.environ['CGRIG_TEST_CB']='1'",
                                        connectables=[selectableNode]
                                        )
        triggers.createSelectionCallback()
        zapi.select([self._testNode])
        triggers.removeSelectionCallback()
        self.assertEqual(os.environ.get("CGRIG_TEST_CB"), "1")
        self.assertEqual(list(zapi.selected()), [selectableNode])
        os.environ["CGRIG_TEST_CB"] = "0"
        triggers.createSelectionCallback()
        # now test the context manager to ensure callbacks are turned off in scope
        with triggers.blockSelectionCallback():
            self.assertFalse(triggercallbackutils.CURRENT_SELECTION_CALLBACK.currentCallbackState)
            zapi.select([self._testNode])
            self.assertEqual(list(zapi.selected()), [self._testNode])
            self.assertNotEqual(os.environ.get("CGRIG_TEST_CB"), "1")
        self.assertTrue(triggercallbackutils.CURRENT_SELECTION_CALLBACK.currentCallbackState)
        os.environ["CGRIG_TEST_CB"] = "0"

        # now test the decorator to ensure callbacks are turned off in scope
        @triggers.blockSelectionCallbackDecorator
        def testCallbackFunction():
            self.assertFalse(triggercallbackutils.CURRENT_SELECTION_CALLBACK.currentCallbackState)
            zapi.select([self._testNode])
            self.assertEqual(list(zapi.selected()), [self._testNode])
            self.assertNotEqual(os.environ.get("CGRIG_TEST_CB"), "1")

        testCallbackFunction()
        self.assertTrue(triggercallbackutils.CURRENT_SELECTION_CALLBACK.currentCallbackState)
        os.environ["CGRIG_TEST_CB"] = "0"
