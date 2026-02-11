# -*- coding: utf-8 -*-
"""This flush module is a hardcore deletion of modules that live in sys.modules dict
"""
import os
import inspect
from cgrig.core.util import zlogging
import sys
import gc

logger = zlogging.cgrigLogger


def flushUnder(dirpath):
    """Flushes all modules that live under the given directory

    :param dirpath: the name of the top most directory to search under.
    :type dirpath: str
    """
    modulePaths = list()
    for name, module in sys.modules.items():
        if module is None:
            del sys.modules[name]
            continue
        try:
            moduleDirpath = os.path.realpath(os.path.dirname(inspect.getfile(module)))
            if moduleDirpath.startswith(dirpath):
                modulePaths.append((name, inspect.getfile(sys.modules[name])))
                del sys.modules[name]
                logger.debug('unloaded module: %s ' % name)

        except TypeError:
            continue

    # Force a garbage collection
    gc.collect()
    return modulePaths


def reloadCgRig():
    """Reload all cgrig modules from sys.modules
    This makes it trivial to make changes to plugin that have potentially
    complex reload dependencies.

    .. code-block:: python

        import flush;flush.reloadCgRig()

    The above will force all cgrig modules to be reloaded by loops over all base packages path in the environment variable
    "CGRIG_BASE_PATHS" then calling flushUnder(basePath)
    """

    bases = os.environ.get("CGRIG_BASE_PATHS", "").split(os.pathsep)
    for base in bases:
        if os.path.exists(base):
            flushUnder(os.path.realpath(base))


def reloadHard(moduleName):
    """Removes all modules from sys that starts with the module name

    :param moduleName: The module name to remove
    :type moduleName: str
    """
    import sys
    logger = zlogging.cgrigLogger
    for k in sys.modules.keys():
        if k.startswith(moduleName) or not sys.modules[k]:
            logger.debug("removing module-> %s" % k)
            try:
                del sys.modules[k]
            except TypeError:
                continue
