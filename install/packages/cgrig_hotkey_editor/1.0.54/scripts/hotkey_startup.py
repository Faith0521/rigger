# -*- coding: utf-8 -*-

from cgrig.core.util import env


def startup(package):
    """ Updates the hotkeys on start up if it has already been installed.

    :param package:
    :return:
    """
    try:
        from cgrig.apps.hotkeyeditor.core import keysets
        if env.isInMaya():
            keysets.KeySetManager()
    except ImportError:
        pass

