# -*- coding: utf-8 -*-
import shutil
import os
import glob
import traceback

from maya import cmds
from maya.api import OpenMaya as om2
from cgrig.core import api
from cgrig.core.manager import currentConfig

from cgrig.libs.maya.utils import general
from cgrig.core.util import zlogging
from cgrig.preferences.interfaces import coreinterfaces

logger = zlogging.getLogger(__name__)


class UninstallerCore(object):

    def __init__(self):
        super(UninstallerCore, self).__init__()
        self.coreInterface = coreinterfaces.coreInterface()

    def uninstall(self, cgrigtools, assets, prefs, cache):
        """ Uninstall

        :param cgrigtools:
        :param assets:
        :param prefs:
        :param customPackages:
        :return:
        """
        self._initVars()
        if cache:
            self.deletePythonCache()
        if cgrigtools:
            self.deleteModFiles()
            cmds.unloadPlugin("cgrigtools.py")
            self.deleteCgRigTools()
            self.deleteShelf()

        # Delete Mod (modFiles)
        if prefs:
            self.deletePrefs()  # this crashes maya for some reason

        if assets:
            self.deleteAssets()

        self.finishUp()
        return True

    def _initVars(self):
        """ Get all the required variables before disabling cgrig tools

        :return:
        """
        self._cgrig = currentConfig()
        self._prefsPath = self.coreInterface.prefsPath()
        self._cgrigPrefsRoot = self.coreInterface.defaultPreferencePath()
        self._resolver = api.currentConfig().resolver
        self._assetPath = self.coreInterface.assetPath()
        self._shelvesDir = general.userShelfDir()

    def deletePythonCache(self):
        """Deletes the cgrigtools cache folder
        """
        cacheFolder = api.currentConfig().cacheFolderPath()
        if not os.path.exists(cacheFolder):
            return
        logger.info("Deleting cache folder: {}".format(cacheFolder))
        try:
            shutil.rmtree(cacheFolder)
        except (PermissionError, OSError):
            om2.MGlobal.displayWarning("Unable to delete cache folder due to permissions, "
                                       "please manually delete folder: {}".format(cacheFolder))

    def deletePrefs(self):

        logger.info("Delete preferences: '{}'".format(self._prefsPath))
        self.deleteFolder(self._prefsPath)

    def checkPreferenceFolder(self):
        # Delete prefs if there are no files left
        if len(os.listdir(self._cgrigPrefsRoot)) == 0:
            os.rmdir(self._cgrigPrefsRoot)

    def finishUp(self):
        """ Finish up the uninstall script

        :return:
        """
        self.checkPreferenceFolder()
        cmds.pluginInfo("cgrigtools.py", remove=1, e=1)

    def deleteAssets(self):
        """ Delete the assets

        :return:
        """

        logger.info("Deleting assets: '{}'".format(self._assetPath))
        self.deleteFolder(self._assetPath)

    @classmethod
    def deleteFolder(cls, path):
        """ Delete folder if it exists

        :param path:
        :return:
        """

        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=False)
            except:

                import maya.api.OpenMaya as om2
                traceback.print_exc()
                om2.MGlobal.displayWarning("Unable to delete '{}'".format(path))

    def deleteCgRigTools(self):
        """ Delete cgrig tools pro

        :return:
        """
        # Delete scripts (cgrigPath)
        cgrigPath = self._cgrig.rootPath
        logger.info("Deleting CgRigToolsPro: '{}'".format(cgrigPath))
        self.deleteFolder(cgrigPath)

    def deleteShelf(self):
        """ Deletes the cgrig tools pro shelf

        :return:
        """
        shelfPath = os.path.join(self._shelvesDir, "shelf_CgRigToolsPro.mel")
        if os.path.exists(shelfPath):
            os.remove(shelfPath)
            logger.info("Deleting CgRigToolsPro shelf")

    def modDirs(self):
        return os.getenv("MAYA_MODULE_PATH").split(os.pathsep)

    def deleteModFiles(self):
        """ Delete the mod files

        :return:
        """
        modFiles = []
        modDirs = self.modDirs()
        for m in modDirs:
            mod = glob.glob(os.path.join(m, "cgrigtoolspro.mod"))
            if mod:
                modFiles += mod

        # Delete all the mod files
        for m in modFiles:
            logger.info("Deleting Mod: '{}'".format(m))
            os.remove(m)
