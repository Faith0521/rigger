import os

import argparse
from cgrig.core.util import zlogging
from cgrig.core.plugin import plugin


logger = zlogging.getLogger(__name__)


class Action(plugin.Plugin):
    id = ""

    def __init__(self, config, manager=None):
        """
        :param config: The cgrig config manager instance.
        :type config: :class:`cgrig.core.manager.CgRig`
        """
        super(Action, self).__init__(manager)
        self.config = config
        self._argumentParser = None  # type: argparse.ArgumentParser or None
        self.options = None  # type: argparse.Namespace or None

    def processArguments(self, parentParser):
        self._argumentParser = parentParser.add_parser(self.id,
                                                       help=self.__doc__,
                                                       )
        self._argumentParser.set_defaults(func=self._execute)
        self.arguments(self._argumentParser)

    def _execute(self, args, extraArguments=None):
        self.options = args
        logger.debug("Running command with arguments: \n{}".format(args))
        self.stats.start()
        try:
            results = self.run()

            # todo: move post command execution to env command and push this to a shell resolver
            # if extra arguments are passed after the "--" then we consider this a shell command
            if extraArguments:
                import subprocess
                subprocess.Popen(extraArguments,
                                 universal_newlines=True,
                                 env=os.environ,
                                 shell=False)
            return results
        finally:
            self.stats.finish()

    def arguments(self, subParser):
        """Method that adds arguments to the argument parser

        :param subParser:
        :type subParser: :class:`argparse.ArgumentParser`
        """
        pass

    def run(self):
        pass

    def cleanup(self):
        pass
