import os
import sys


def _currentFolder():
    currentFolder = os.path.dirname(__file__)
    return currentFolder


def _embedPaths():
    """This ensures cgrigtools python paths have been setup correctly"""
    currentFolder = _currentFolder()
    envPath = os.getenv("CGRIGTOOLS_PRO_ROOT", "")
    rootPath = ""
    if envPath:
        rootPath = os.path.abspath(os.path.expandvars(os.path.expanduser(envPath)))
    if not os.path.exists(rootPath):
        rootPath = os.path.abspath(os.path.join(currentFolder, "..", ".."))

    rootPythonPath = os.path.join(rootPath, "python")
    if rootPath is None:
        msg = """CgRigtools is missing the 'CGRIGTOOLS_PRO_ROOT' environment variable
                in the maya mod file.
                """
        raise ValueError(msg)
    elif not os.path.exists(rootPythonPath):
        raise ValueError("Failed to find valid cgrigtools python folder")
    if rootPythonPath not in sys.path:
        sys.path.append(rootPythonPath)
    if currentFolder not in sys.path:
        sys.path.append(currentFolder)
    return rootPath


def loadCgRig():
    rootPath = _embedPaths()

    if rootPath is None:
        msg = """CgRig Tools PRO is missing the 'CGRIGTOOLS_PRO_ROOT' environment variable
        in the maya mod file.
        """
        raise ValueError(msg)

    from cgrig.core import api
    from cgrig.core import engine
    from cgrigunreal import unreallogging
    from cgrig.core.util import zlogging

    manager = zlogging.CentralLogManager()
    manager.removeHandlers(zlogging.CENTRAL_LOGGER_NAME)
    manager.addHandler(zlogging.CENTRAL_LOGGER_NAME, unreallogging.UnrealLogHandler())

    from cgrigunreal import unrealengine
    currentInstance = api.currentConfig()
    if currentInstance is None:
        coreConfig = api.cgrigFromPath(rootPath)
        engine.startEngine(coreConfig, unrealengine.UnrealEngine, "unreal")


if __name__ == "__main__":
    loadCgRig()
