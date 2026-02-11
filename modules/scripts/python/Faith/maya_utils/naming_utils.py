# -*- coding: utf-8 -*-
from maya import cmds
from .python_utils import PY3
import string
import re
import sys
import collections

Letters = string.ascii_uppercase
LeftList = ['left_', '_left', 'Left_', '_Left', 'lt_', '_lt', 'Lt_', '_Lt', 'lft_', '_lft', 'Lft_', '_Lft', 'Lf_',
            '_Lf', 'lf_', '_lf', 'l_', '_l', 'L_', '_L']
RightList = ['right_', '_right', 'Right_', '_Right', 'rt_', '_rt', 'Rt_', '_Rt', 'rgt_', '_rgt', 'Rgt_', '_Rgt', 'Rg_',
             '_Rg', 'rg_', '_rg', 'r_', '_r', 'R_', '_R']


# TODO: update the unique_name function to accept suffix to ignore
def unique_name(name, return_counter=False, suffix=None):
    """
    Searches the scene for match and returns a unique name for given name
    Args:
        name: (String) Name to query
        return_counter: (Bool) If true, returns the next available number instead of the object name
        suffix: (String) If defined and if name ends with this suffix, the increment numbers will be put before the.

    Returns: (String) uniquename

    """
    search_name = name
    base_name = name
    if suffix and name.endswith(suffix):
        base_name = name.replace(suffix, "")
    else:
        suffix = ""

    id_counter = 0
    while cmds.objExists(search_name):
        search_name = "{0}{1}{2}".format(base_name, str(id_counter + 1), suffix)
        id_counter = id_counter + 1

    if return_counter:
        return id_counter
    else:
        if id_counter:
            result_name = "{0}{1}{2}".format(base_name, str(id_counter), suffix)
        else:
            result_name = name
        return result_name


def resolveLetterName(name, suffix, *args):
    """

    :param name:
    :param suffix:
    :param args:
    :return:
    """
    name = name[0].upper() + name[1:].replace(" ", "_")
    baseName = name
    name = name + "_A_" + suffix
    if cmds.objExists(name):
        i = 1
        while cmds.objExists(name):
            name = baseName + "_" + Letters[i] + "_" + suffix
            i = i + 1
        baseName = baseName + "_" + Letters[i - 1]
    else:
        baseName = baseName + "_A"

    return baseName, name


def resolveNumName(name, suffix, *args):
    """
    Resolve repeated name adding number in the middle of the string.
        Returns the resolved baseName and name (including the suffix).
    :param name:
    :param suffix:
    :param args:
    :return:
    """
    name = name[0].upper() + name[1:].replace(" ", "_")
    baseName = name
    name = name + "_00_" + suffix
    if cmds.objExists(name):
        i = 1
        while cmds.objExists(name):
            name = baseName + "_" + str(i).zfill(2) + "_" + suffix
            i = i + 1
        baseName = baseName + "_" + str(i - 1).zfill(2)
    else:
        baseName = baseName + "_00"

    return baseName, name


def getReferencePath(path):
    """
    returns the last item if a referenced path is present
    :param path:
    :return:
    """
    if re.match(".*:.*", path):
        parts = path.split(":")
        return parts[0]


def MirrorSideLabel(name):
    """
    replace the side identifier with the opposite side
    :param name:
    :return:
    """

    for i in range(len(LeftList)):
        if re.match(r".*" + LeftList[i] + ".*", name):
            name = name.replace(LeftList[i], RightList[i])
            return name

        if re.match(r".*" + RightList[i] + ".*", name):
            name = name.replace(RightList[i], LeftList[i])
            return name


def encode(data):
    """Encodes the data as unicode data if the interpreter is Python 2.x"""
    try:
        return unicode(data).encode("utf-8")  # noqa
    except NameError:
        return data


def decode(data):
    """Decodes the unicode data if the interpreter is Python 2.x"""
    try:
        return unicode(data).decode("utf-8")  # noqa
    except NameError:
        if type(data) == bytes:
            return data.decode("utf-8")
        else:
            return data


def is_string(data):
    if sys.version_info.major == 3:
        if isinstance(data, str):
            return True
        else:
            return False
    else:
        if isinstance(data, (unicode, str)):  # noqa
            return True
        else:
            return False


def flatten(l):
    for el in l:
        if not PY3:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):  # noqa
                for sub in flatten(el):
                    yield sub
            else:
                yield el
        else:
            if isinstance(el, collections.abc.Iterable) and not isinstance(
                    el, (str, bytes)
            ):
                yield from flatten(el)
            else:
                yield el


def convertRLName(name):
    """Convert a string with underscore

    i.e: "_\L", "_L0\_", "L\_", "_L" to "R". And vice and versa.

    :param string name: string to convert
    :return: Tuple of Integer

    """
    if name == "L":
        return "R"
    elif name == "R":
        return "L"
    elif name == "l":
        return "r"
    elif name == "r":
        return "l"

    re_str = "_[RLrl][0-9]+_|^[RLrl][0-9]+_"
    re_str = re_str + "|_[RLrl][0-9]+$|_[RLrl]_|^[RLrl]_|_[RLrl]$"
    re_str = re_str + "|_[RLrl][.]|^[RLrl][.]"
    re_str = re_str + "|_[RLrl][0-9]+[.]|^[RLrl][0-9]+[.]"
    rePattern = re.compile(re_str)

    matches = re.findall(rePattern, name)
    if matches:
        for match in matches:
            if match.find("R") != -1:
                rep = match.replace("R", "L")
            elif match.find("L") != -1:
                rep = match.replace("L", "R")
            elif match.find("r") != -1:
                rep = match.replace("r", "l")
            elif match.find("l") != -1:
                rep = match.replace("l", "r")
            name = re.sub(match, rep, name)

    return name