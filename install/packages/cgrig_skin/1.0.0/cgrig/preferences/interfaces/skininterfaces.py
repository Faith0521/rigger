# -*- coding: utf-8 -*-
from cgrig.preferences.core import preference


def deformerInterface():
    """ Get the general settings

    :return: Returns the preference interface "deformer_interface"
    :rtype: :class:`preferences.interface.controljointspreferences.ControlJointsPreferences`
    """
    return preference.interface("deformer_interface")
