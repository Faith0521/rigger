import argparse

from cgrig.core import constants


class Parser(argparse.ArgumentParser):
    def error(self, message):
        pass


def fromCli(cfg, arguments):
    """A function which runs a cgrigcli action based on the arguments passed.


    :param cfg:
    :type cfg: :class:`cgrig.core.manage.CgRig`
    :param arguments:
    :type arguments: list(str)
    :return:
    :rtype: bool
    """

    argumentParser, subParser = createRootParser()

    for name, clsObj in cfg.commands.plugins.items():
        instance = clsObj(config=cfg)
        instance.processArguments(subParser)
    if not arguments:
        argumentParser.print_help()
        return False
    groupedArguments = [[]]
    for arg in arguments:
        if arg == "--":
            groupedArguments.append([])
            continue
        groupedArguments[-1].append(arg)
    try:
        args = argumentParser.parse_args(groupedArguments[0])
    except TypeError:
        argumentParser.error("Invalid command name: {}".format(groupedArguments[0][0]))
        return False
    extraArguments = []
    if len(groupedArguments) > 1:
        extraArguments = groupedArguments[-1]

    def runCmd():
        try:
            # python3 will not automatically handle cases where no sub parser
            # has been selected. In these cases func will not exist, and an
            # AttributeError will be raised.
            func = args.func
        except AttributeError:
            argumentParser.error("too few arguments.")
        else:
            return func(args, extraArguments=extraArguments)

    return runCmd()


def createRootParser():
    helpHeader = """
Welcome to CgRigTools Pro

This Command allows you to modify the cgrigtools configuration from a shell.
You can embed the cgrigtools python environment by simply running this command without
arguments.
To see the arguments for each cgrig command run cgrig_cmd [command] --help
    """
    argumentParser = Parser(prog=constants.CLI_ROOT_NAME,
                            description=helpHeader,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
    subParser = argumentParser.add_subparsers()
    return argumentParser, subParser
