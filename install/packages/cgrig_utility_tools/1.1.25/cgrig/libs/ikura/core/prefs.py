# coding: utf-8

import os
import json
import yaml
from six import string_types

from .tree import Tree, Branch
from .utils import ordered_load, ordered_dump, unique
from cgrig.core.util.zlogging import create_logger

try:
    from PySide2.QtCore import QStandardPaths
except ImportError:
    try:
        from PySide6.QtCore import QStandardPaths
    except ImportError:
        QStandardPaths = None

log = create_logger('ikura.prefs')

__all__ = ['UserPrefs', 'Prefs']


# -- user preferences


class UserPrefs(object):
    name = 'ikura'
    filename = 'prefs.json'
    path = None
    prefs = {}

    @classmethod
    def get_path(cls):
        if QStandardPaths is None:
            raise RuntimeError('PySide is required for saving user preferences.')

        base_dir = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

        full_dir = os.path.join(base_dir, cls.name)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        return os.path.join(full_dir, cls.filename)

    @classmethod
    def load(cls):
        if os.path.exists(cls.path):
            try:
                with open(cls.path, 'r') as f:
                    cls.prefs = json.load(f)
            except:
                log.warning('failed to load user preferences')

    @classmethod
    def save(cls):
        try:
            with open(cls.path, 'w') as f:
                json.dump(cls.prefs, f, indent=4)
        except Exception as e:
            log.error('failed to save user preferences: {}'.format(e))

    @classmethod
    def get(cls, key, default=None):
        return cls.prefs.get(key, default)

    @classmethod
    def set(cls, key, value):
        cls.prefs[key] = value
        cls.save()


UserPrefs.path = UserPrefs.get_path()
UserPrefs.load()


# -- production prefs

class Prefs(object):
    prefs = Tree(sep='/')
    loaded = False
    filename = 'mikan.yml'
    paths = []

    @classmethod
    def load(cls):
        cls.prefs.clear()

        data = {}
        path = cls.get_config_file()

        if path:
            with open(path, 'r') as stream:
                try:
                    data = ordered_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

        if data:
            try:
                for k, v in Tree.flatten(data, sep='/'):
                    cls.prefs[k] = v
            except:
                log.warning('/!\\ failed to parse config file from "{}"'.format(path))

    @classmethod
    def write(cls, data):
        if isinstance(data, Tree):
            data = Tree.rarefy(data)

        if not isinstance(data, dict):
            raise TypeError('dict expected (received a {})'.format(type(data)))

        path = cls.get_config_file()
        if not path:
            raise RuntimeError('no valid path found')

        with open(path, 'w') as stream:
            try:
                ordered_dump(data, stream, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)

    @classmethod
    def get_config_file(cls):
        for path in cls.paths:
            path = path + os.path.sep + cls.filename
            if os.path.exists(path):
                return path

        # log.warning('/!\\ cannot find any config file for mikan')

    @classmethod
    def get_paths(cls):
        sep = os.path.sep

        if 'MAYA_PROJECT' in os.environ:
            cls.paths.append(os.path.realpath(os.environ['MAYA_PROJECT'] + sep + 'rig'))

        # maya prefs
        try:
            import maya.cmds as mc
            cls.paths.append(os.path.realpath(mc.workspace(q=1, rd=1)) + sep + 'rig')
        except:
            pass

        # unique paths
        cls.paths = unique(cls.paths)

    @classmethod
    def guess_path(cls, path):
        # guess prefs path from any given path
        sep = os.path.sep

        # maya project?
        workspace = find_maya_project_root(path)
        if workspace:
            path = os.path.realpath(workspace) + sep + 'rig'
            if path not in cls.paths:
                cls.paths.append(path)

    @classmethod
    def reload(cls):
        cls.loaded = False
        cls.load()

    @classmethod
    def get(cls, key, default=None):
        if not cls.loaded:
            cls.load()
            cls.loaded = True

        value = cls.prefs.get(key, default)
        if value is None:
            value = default
        if isinstance(value, Branch):
            value = Tree.rarefy(value)
        return value

    @classmethod
    def as_dict(cls):
        return Tree.rarefy(cls.prefs)

    @classmethod
    def get_project_name(cls):
        # name from prefs
        name = cls.get('name')
        if name:
            return name

        # name from path
        path = find_maya_project_root(cls.get_config_file())
        if path:
            name = os.path.split(path)[-1]

        return name


# init paths
Prefs.get_paths()


# utils

def find_maya_project_root(start_path):
    """
    Remonte récursivement les dossiers parents depuis start_path
    jusqu'à trouver un dossier contenant un fichier 'workspace.mel'.
    Retourne le chemin du dossier trouvé ou None si non trouvé.
    """
    if not isinstance(start_path, string_types):
        return

    current_path = os.path.abspath(start_path)

    while True:
        workspace_file = os.path.join(current_path, 'workspace.mel')
        if os.path.isfile(workspace_file):
            return current_path

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            return

        current_path = parent_path
