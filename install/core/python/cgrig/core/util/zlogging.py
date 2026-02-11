import logging
from logging import handlers as loggingHandleres
import os
from contextlib import contextmanager
from timeit import default_timer
from six import string_types
from cgrigvendor import six
from cgrig.core.util import classtypes

LOG_PREFIX = "cgrigtools"
CENTRAL_LOGGER_NAME = "cgrigtools"
LOG_LEVEL_ENV_NAME = "CGRIG_LOG_LEVEL"
logging.SUCCESS = 25  # between WARNING and INFO


class SafeHandler(logging.Handler):
    pass


class SafeFileHandler(logging.FileHandler, SafeHandler):
    pass


@six.add_metaclass(classtypes.Singleton)
class CentralLogManager(object):
    """This class is a singleton object that globally handles logging, any log added will managed by the class.
    """

    def __init__(self):
        self.logs = {}  # type: dict[str, logging.Logger]
        self.jsonFormatter = "%(asctime) %(name) %(processName) %(pathname)  %(funcName) %(levelname) %(lineno) %(" \
                             "module) %(threadName) %(message)"
        self.rotateFormatter = "%(asctime)s: [%(process)d - %(name)s - %(levelname)s]: %(message)s"
        self.shellFormatter = "[%(name)s - %(module)s - %(funcName)s - %(levelname)s]: %(message)s"
        self.guiFormatter = "[%(name)s]: %(message)s"

    def addLog(self, logger):
        """Adds logger to this manager instance

        :param logger: the python logger instance.
        :type logger: :class:`logging.Logger`
        """
        if logger.name not in self.logs:
            self.logs[logger.name] = logger
        globalLogLevelOverride(logger)

    def removeLog(self, loggerName):
        """Remove's the logger instance by name

        :param loggerName: The logger instance name.
        :type: loggerName: str
        """
        if loggerName in self.logs:
            del self.logs[loggerName]

    def changeLevel(self, loggerName, level):
        """Changes the logger instance level.

        :param loggerName: The logger instance name.
        :type loggerName: str
        :param level: eg. logging.DEBUG.
        :type level: int
        """
        if loggerName in self.logs:
            log = self.logs[loggerName]
            if log.level != level:
                log.setLevel(level)

    def addRotateHandler(self, loggerName, filePath):
        """Add a rotating file handler to the logger with the specified name.

        :param loggerName: The name of the logger to which the handler will be added.
        :type loggerName: str
        :param filePath: The path to the log file to which the handler will write.
        :type filePath: str
        :return: The file handler object that was added to the logger.
        :rtype: logging.handlers.RotatingFileHandler or None
        """
        logger = self.logs.get(loggerName)
        if not logger:
            return

        handler = loggingHandleres.RotatingFileHandler(filePath, maxBytes=1.5e6, backupCount=5)
        handler.setFormatter(logging.Formatter(self.rotateFormatter))
        logger.addHandler(handler)
        return handler

    def addShellHandler(self, loggerName):
        """Add a stream handler to the logger with the specified name that outputs to the shell.

        :param loggerName: The name of the logger to which the handler will be added.
        :type loggerName: str
        :return: The stream handler object that was added to the logger.
        :rtype: logging.StreamHandler or None
        """
        logger = self.logs.get(loggerName)
        if not logger:
            return
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(self.shellFormatter))
        logger.addHandler(handler)
        return handler

    def addNullHandler(self, loggerName):
        """Add a null handler to the logger with the specified name.

        :param loggerName: The name of the logger to which the handler will be added.
        :type loggerName: str
        :return: The null handler object that was added to the logger.
        :rtype: logging.NullHandler or None
        """
        logger = self.logs.get(loggerName)
        if not logger:
            return
        # Create an null handler
        handler = logging.NullHandler()
        # Create a logging formatter
        formatter = logging.Formatter(self.shellFormatter)
        # Assign the formatter to the io_handler
        handler.setFormatter(formatter)
        # Add the io_handler to the logger
        logger.addHandler(handler)
        return handler

    def addHandler(self, loggerName, handler):
        """
        :param loggerName:
        :param handler:
        :type handler: :class:`logging.StreamHandler`
        """
        log = self.logs.get(loggerName)
        if log is None:
            return
        formatter = logging.Formatter(self.shellFormatter)
        handler.setFormatter(formatter)
        log.addHandler(handler)

        return handler

    def removeHandlers(self, loggerName):
        log = self.logs.get(loggerName)
        if log is None:
            return False
        log.handlers = []  # could do clear() but py etc compat
        return True


class MayaGuiLogHandler(logging.Handler):
    """
    A python logging handler that displays error and warning
    records with the appropriate color labels within the Maya GUI
    """

    def __init__(self):
        super(MayaGuiLogHandler, self).__init__()
        from maya.OpenMaya import MGlobal
        self.MGlobal = MGlobal

    def emit(self, record):
        msg = self.format(record)
        if record.levelno > logging.WARNING:
            # Error (40) Critical (50)
            self.MGlobal.displayError(msg)
        elif record.levelno > logging.SUCCESS:
            # Warning (30)
            self.MGlobal.displayWarning(msg)
        else:
            # Debug (10) and Info (20)
            self.MGlobal.displayInfo(msg)


class BaseHandler(MayaGuiLogHandler, SafeHandler):
    pass



def logLevels():
    """Returns a Map of stdlib logging levels.

    :rtype: Iterable[str]
    """
    return map(logging.getLevelName, range(0, logging.CRITICAL + 1, 10))


def levelsDict():
    """Returns the stdlib logging levels as a dict.

    The keys are the formal logging names and values are the logging constant value.

    :rtype: dict[str: int]
    """
    return {logging.getLevelName(i): i for i in range(0, logging.CRITICAL + 1, 10)}


def getLogger(name):
    """Returns the CgRig tools log name in the form of 'cgrigtools.*.*'

    This is to ensure consistent logging names across all applications

    :param name: The logger name to format.
    :type name: str
    :return:
    :rtype: :class:`logging.Logger`
    """

    if name == CENTRAL_LOGGER_NAME:
        name = CENTRAL_LOGGER_NAME
    elif name.startswith("cgrig."):
        name = ".".join((LOG_PREFIX, name[4:]))
    elif name.startswith("preferences."):
        name = ".".join((LOG_PREFIX, "preferences", name[len("preferences."):]))
    logger = logging.getLogger(name)
    CentralLogManager().addLog(logger)
    return logger


def globalLogLevelOverride(logger):
    """Override a logger's logging level with the value of an environment variable.

    :param logger: The logger object to override the logging level for.
    :type logger: logging.Logger
    """
    globalLoggingLevel = os.environ.get(LOG_LEVEL_ENV_NAME, "INFO")
    envLvl = logging.getLevelName(globalLoggingLevel)
    currentLevel = logger.getEffectiveLevel()

    if not currentLevel or currentLevel != envLvl:
        logger.setLevel(envLvl)


def reloadLoggerHierarchy():
    """Reload the hierarchy of the logging system by removing and re-adding loggers to their parents."""
    for log in logging.Logger.manager.loggingDict.values():
        if hasattr(log, "children"):
            del log.children
    for name, log in logging.Logger.manager.loggingDict.items():
        if not isinstance(log, logging.Logger):
            continue
        try:
            if log not in log.parent.children:
                log.parent.children.append(log)
        except AttributeError:
            log.parent.children = [log]


def iterLoggers():
    """Iterates through all cgrigtools loggers.

    :return: generator(str, logging.Logger)
    """
    for name, logObject in sorted(logging.root.manager.loggerDict.items()):
        if name.startswith("cgrig."):
            yield name, logObject


def rootLogger():
    """Retrieves the top most cgrigtools logger instance in the cgrig hierarchy
    """
    return logging.root.getChild("cgrigtools")


def setGlobalDebug(state):
    """Toggles the root cgrig tools logger between DEBUG and INFO
    """
    rootLog = rootLogger()
    if state:
        rootLog.setLevel(logging.DEBUG)
        os.environ[LOG_LEVEL_ENV_NAME] = "DEBUG"
        rootLog.info("{} has been set to debug mode".format(rootLog.name))
    else:
        rootLog.setLevel(logging.INFO)
        os.environ[LOG_LEVEL_ENV_NAME] = "INFO"
        rootLog.info("{} has been set to Info mode".format(rootLog.name))


def isGlobalDebug():
    """Returns whether the cgrigtools logging level is set to DEBUG.

    :rtype: bool
    """
    return os.environ.get(LOG_LEVEL_ENV_NAME, "INFO") == "DEBUG"


def get_formatter(name=True):
    msg = '%(message)s'
    if name:
        s = '[%(name)s] %(levelname)8s| ' + msg
    else:
        s = '%(levelname)-8s| ' + msg

    return logging.Formatter(s)


def create_logger(name='', level=None, save=False):
    if not name:
        name = CENTRAL_LOGGER_NAME

    set_level = False
    if name not in logging.root.manager.loggerDict or level is not None:
        set_level = True

    logger = logging.getLogger(name)

    if set_level:
        if level is None:
            level = 'INFO'
        logger.setLevel(level.upper() if isinstance(level, str) else level)

    logger.propagate = False

    # add a success level
    setattr(logger, 'success', lambda message, *args: logger._log(logging.SUCCESS, message, args))

    # cleanup handlers
    logger.handlers = [handler for handler in logger.handlers if isinstance(handler, SafeHandler)]

    # create base handler
    add_handler = True
    for handler in logger.handlers:
        if isinstance(handler, BaseHandler):
            add_handler = False
            break

    if add_handler:
        handler = BaseHandler()

        handler.setFormatter(get_formatter())
        logger.addHandler(handler)

    # save to file
    if save:
        log_file_path = r"%tmp%\{}.log".format(name)
        if isinstance(save, string_types):
            log_file_path = save
        log_file_path = os.path.expandvars(log_file_path)
        log_file_path = os.path.realpath(log_file_path)

        # crate log file
        fh = SafeFileHandler(log_file_path, encoding=None, delay=False)

        if set_level:
            if level is None:
                level = 'INFO'
            fh.setLevel(level.upper() if isinstance(level, str) else level)

        fh.setFormatter(get_formatter())
        logger.addHandler(fh)

    # exit
    return logger

log = create_logger()
debug_timings = False


def time_to_str(t):
    next_unit = iter(('s', 'ms', u'µs', 'ns'))

    unit = next(next_unit)
    while t < 1:
        t *= 1000.0
        try:
            unit = next(next_unit)
        except StopIteration:
            break

    return u'{:.2f}{}'.format(t, unit)


@contextmanager
def timed_code(name=None, level='INFO', force=False):
    level = getattr(logging, level.upper())

    msg = '{} took'.format(name) if name else 'section took'
    t0 = default_timer()
    try:
        yield
    finally:
        if debug_timings or force:
            delta = default_timer() - t0
            log.log(level, u'{}: {}'.format(msg, time_to_str(delta)))


def set_time_logging(state):
    global debug_timings
    debug_timings = bool(state)



cgrigLogger = getLogger(CENTRAL_LOGGER_NAME)
# to avoid log messages propagating upwards in the
# log hierarchy.
cgrigLogger.propagate = False
handlers = cgrigLogger.handlers
if not handlers:
    CentralLogManager().addShellHandler(cgrigLogger.name)
