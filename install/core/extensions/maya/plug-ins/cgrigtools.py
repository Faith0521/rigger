import logging
import cProfile
import os
import sys
import traceback
from functools import wraps
from maya.api import OpenMaya as om2
from maya import cmds
from maya import utils


logger = logging.getLogger(__name__)
if not len(logger.handlers):
    logger.addHandler(logging.StreamHandler())
# set the level, we do this for the plugin since this module usually gets executed before cgrigtools is initialized
logLevel = os.getenv("CGRIG_LOG_LEVEL")
_DISPLAY_ERROR = True
if logLevel:
    logLevel = logging.getLevelName(logLevel)
    logger.setLevel(logLevel)
    _DISPLAY_ERROR = logLevel <= logging.ERROR

if not hasattr(om2, "_REQUIRED_COMMAND_SYNC"):
    om2._REQUIRED_COMMAND_SYNC = None

RETURN_STATE_SUCCESS = 0
RETURN_STATE_ERROR = 1

def _embedPaths():
    """This ensures cgrigtools python paths have been setup correctly"""
    rootPath = os.getenv("CGRIGTOOLS_PRO_ROOT", "")
    rootPythonPath = os.path.join(rootPath, "python")
    rootPythonPath = os.path.abspath(rootPythonPath)

    if rootPythonPath is None:
        msg = """CgRigtools is missing the 'CGRIGTOOLS_PRO_ROOT' environment variable
                in the maya mod file.
                """
        raise ValueError(msg)
    elif not os.path.exists(rootPythonPath):
        raise ValueError(
            "Failed to find valid cgrigtools python folder, incorrect .mod state"
        )
    if rootPythonPath not in sys.path:
        sys.path.append(rootPythonPath)


def loadCgRig():
    rootPath = os.getenv("CGRIGTOOLS_PRO_ROOT", "")
    rootPath = os.path.abspath(rootPath)

    if rootPath is None:
        msg = """CgRig Tools PRO is missing the 'CGRIGTOOLS_PRO_ROOT' environment variable
        in the maya mod file.
        """
        raise ValueError(msg)

    from cgrig.core import api
    from cgrig.core import engine
    from cgrig.core.util import zlogging

    manager = zlogging.CentralLogManager()
    manager.removeHandlers(zlogging.CENTRAL_LOGGER_NAME)

    manager.addHandler(zlogging.CENTRAL_LOGGER_NAME, utils.MayaGuiLogHandler())
    existingPackageEnv = os.getenv(api.constants.CGRIG_PACKAGE_VERSION_FILE)
    if not existingPackageEnv:
        os.environ[api.constants.CGRIG_PACKAGE_VERSION_FILE] = (
            "package_version_maya.config"
        )

    import cgrigmayaengine

    currentInstance = api.currentConfig()
    if currentInstance is None:
        coreConfig = api.cgrigFromPath(rootPath)
        engine.startEngine(coreConfig, cgrigmayaengine.MayaEngine, "maya")


def profileIt(func):
    """cProfile decorator to profile said function, must pass in a filename to write the information out to
    use RunSnakeRun to run the output

    :return: Function
    """
    profileFlag = int(os.environ.get("CGRIG_PROFILE", "0"))
    profileExportPath = os.path.expandvars(
        os.path.expanduser(os.environ.get("CGRIG_PROFILE_PATH", ""))
    )
    shouldProfile = False
    if profileFlag and profileExportPath:
        shouldProfile = True

    @wraps(func)
    def inner(*args, **kwargs):
        if shouldProfile:
            logger.debug("Running CProfile output to : {}".format(profileExportPath))
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            # Note use of name from outer scope
            prof.dump_stats(profileExportPath)
            return retval
        else:
            return func()

    return inner


class UndoCmd(om2.MPxCommand):
    """Specialised MPxCommand to get around maya api retarded features.
    Stores cgrig Commands on the UndoCmd
    """

    REQUIRED_COMMAND_SYNC = None
    kCmdName = "cgrigAPIUndo"
    kId = "-id"
    kIdLong = "-commandId"

    def __init__(self):
        """We initialize a storage variable for a list of commands."""
        om2.MPxCommand.__init__(self)
        # store the cgrig command and executor for the life of the MPxcommand instance.
        self._command = None
        self._commandName = ""

    def doIt(self, argumentList):
        """Grab the list of current commands from the stack and dump it on our command so we can call undo.

        :param argumentList: :class:`om2.MArgList`
        """
        parser = om2.MArgParser(self.syntax(), argumentList)
        commandId = parser.flagArgumentString(UndoCmd.kId, 0)
        self._commandName = commandId
        # add the current queue into the mpxCommand instance then clean the queue since we dont need it anymore
        if om2._REQUIRED_COMMAND_SYNC is not None:
            self._command = om2._REQUIRED_COMMAND_SYNC
            om2._REQUIRED_COMMAND_SYNC = None
            self.redoIt()

    def redoIt(self):
        """Runs the doit method on each of our stored commands"""
        if self._command is None:
            return
        prevState = cmds.undoInfo(stateWithoutFlush=True, q=True)

        try:
            if self._command.disableQueue:
                cmds.undoInfo(stateWithoutFlush=False)
            self._callDoIt(self._command)
        finally:
            cmds.undoInfo(stateWithoutFlush=prevState)

    def undoIt(self):
        """Calls undoIt on each stored command in reverse order"""
        if self._command is None:
            return
        if not self._command.isUndoable:
            return

        prevState = cmds.undoInfo(stateWithoutFlush=True, q=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            self._command.undoIt()
        finally:
            cmds.undoInfo(stateWithoutFlush=prevState)

    def _callDoIt(self, cmd):
        try:
            result = cmd.doIt(**cmd.arguments)
            cmd._returnResult = result
            cmd._returnStatus = RETURN_STATE_SUCCESS
        except Exception:
            traceback.print_exception(*sys.exc_info())
            cmd._returnResult = None
            cmd.returnStatus = RETURN_STATE_ERROR
            cmd.errors = traceback.format_exception(*sys.exc_info())
            result = None
        else:
            cmd._returnResult = result
        return result

    def isUndoable(self):
        """True if we have stored commands
        :return: bool
        """

        return self._command.isUndoable

    @staticmethod
    def cmdCreator():
        return UndoCmd()

    @staticmethod
    def syntaxCreator():
        syntax = om2.MSyntax()
        syntax.addFlag(UndoCmd.kId, UndoCmd.kIdLong, om2.MSyntax.kString)
        return syntax


def maya_useNewAPI():
    """WTF AutoDesk? Its existence tells maya that we are using api 2.0. seriously this should of just been a flag"""
    pass


def create():
    om2.MGlobal.displayInfo("Loading CgRig Tools PRO, please wait!")
    logger.debug("Loading CgRig Tools PRO")
    _embedPaths()
    loadCgRig()


def initializePlugin(obj):
    mplugin = om2.MFnPlugin(obj, "David Sparrow", "1.0")

    try:
        create()
    except Exception:
        logger.error(
            "Unhandled Exception occurred during CgRig tools startup", exc_info=True
        )
        if _DISPLAY_ERROR:
            om2.MGlobal.displayError("Unknown cgrig tools startup failure")
    try:
        mplugin.registerCommand(
            UndoCmd.kCmdName, UndoCmd.cmdCreator, UndoCmd.syntaxCreator
        )
    except:
        if _DISPLAY_ERROR:
            om2.MGlobal.displayError("Failed to register command: {}".format(UndoCmd.kCmdName))


def uninitializePlugin(obj):
    mplugin = om2.MFnPlugin(obj)
    try:
        from cgrig.core import api

        cfg = api.currentConfig()
        if cfg is not None:
            cfg.shutdown()
    except Exception:
        logger.error(
            "Unhandled Exception occurred during CgRig tools shutdown", exc_info=True
        )
        if _DISPLAY_ERROR:
            om2.MGlobal.displayError("Unknown cgrig tools shutdown failure")
        return
    try:
        mplugin.deregisterCommand(UndoCmd.kCmdName)
    except:
        if _DISPLAY_ERROR:
            om2.MGlobal.displayError(
                "Failed to unregister command: {}".format(UndoCmd.kCmdName)
            )
