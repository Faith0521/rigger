# -*- coding: utf-8 -*-
from cgrig.libs.maya.mayacommand import command


class TestCommandReg(command.CgRigCommandMaya):
    id = "test.testCommand"
    isUndoable = False
    isEnabled = True

    def doIt(self, value="hello"):
        return value


class FailCommandArguments(command.CgRigCommandMaya):
    id = "test.failCommandArguments"
    isUndoable = False
    isEnabled = True

    def doIt(self, value):
        pass


class TestCommandUndoable(command.CgRigCommandMaya):
    id = "test.testCommandUndoable"
    isUndoable = True
    isEnabled = True
    value = ""

    def doIt(self, value="hello"):
        self.value = value
        return value

    def undoIt(self):
        self.value = ""


class TestCommandNotUndoable(command.CgRigCommandMaya):
    id = "test.testCommandNotUndoable"
    isUndoable = False
    isEnabled = True
    value = ""

    def doIt(self, value="hello"):
        self.value = value
        return value

    def undoIt(self):
        self.value = ""
