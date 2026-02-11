import os
from basetest import BaseTest


class TestCgRigConfig(BaseTest):
    def setUp(self):
        from cgrig.core import api
        self.api = api
        self.cgrigConfig = api.cgrigFromPath(os.environ["CGRIGTOOLS_ROOT"])

    def testHasCorrectEnvPaths(self):
        self.assertTrue(os.path.exists(self.cgrigConfig.rootPath))
        self.assertEqual(self.cgrigConfig, self.api.currentConfig())
        self.assertTrue(self.cgrigConfig.configPath.endswith("config"),
                        msg="Config Folder Doesn't end with 'config', {}".format(self.cgrigConfig.configPath))
        self.assertTrue(self.cgrigConfig.corePath.endswith("core"),
                        msg="core Folder Doesn't end with python', {}".format(self.cgrigConfig.corePath))

        self.assertTrue(self.cgrigConfig.packagesPath.endswith("packages"),
                        msg="Package Folder Doesn't end with 'packages', {}".format(self.cgrigConfig.packagesPath))
        self.assertTrue(os.path.exists(self.cgrigConfig.configPath),
                        msg="Config Folder Doesn't exist, {}".format(self.cgrigConfig.configPath))
        self.assertTrue(os.path.exists(self.cgrigConfig.corePath),
                        msg="core Folder Doesn't exist, {}".format(self.cgrigConfig.corePath))
        self.assertTrue(os.path.exists(self.cgrigConfig.packagesPath),
                        msg="Package Folder Doesn't exist, {}".format(self.cgrigConfig.packagesPath))
        self.assertTrue(os.path.exists(os.path.join(self._mayaFolder, "cgrigtoolspro.mod")),
                        msg="maya module Folder Doesn't exist, {}".format(os.path.join(self._mayaFolder,
                                                                                       "cgrigtoolspro.mod")))

    def testCreateEnvironmentFile(self):
        # grab the current env and rename it so we dont fuck it
        # now create the new env and test it's existence
        # now delete the new one and rename the old back again
        originalEnvFile = self.cgrigConfig.resolver.environmentPath()
        newPath = os.path.join(os.path.dirname(originalEnvFile), "testEnv.config")
        os.rename(originalEnvFile, newPath)
        self.cgrigConfig.resolver.createEnvironmentFile({})
        self.assertTrue(os.path.exists(newPath))
        os.remove(self.cgrigConfig.resolver.environmentPath())
        os.rename(newPath, originalEnvFile)

    def testLoadEnvironmentFile(self):
        self.assertIsInstance(self.cgrigConfig.resolver.loadEnvironmentFile(), dict)

    def testSetupCommand(self):
        """While the base class setupClass() handles installing cgrigtools into a temp
        Folder, this is normally run from the bare repo which isn't installed.

        So here we run the setup again but this time from the new location
        """

        batFile = os.path.join(self.cgrigConfig.corePath, "bin", "cgrig_cmd.bat")
        if not os.path.exists(batFile):
            raise OSError("Bat file doesn't exist: {}".format(batFile))
        self._runSetup(batFile)

    def testIsAdmin(self):
        self.assertFalse(self.cgrigConfig.isAdmin)
        self.cgrigConfig.isAdmin = True
        self.assertTrue(self.cgrigConfig.isAdmin)

    def testShutdown(self):
        self.cgrigConfig.shutdown()
        self.assertIsNone(self.api.currentConfig())
        self.cgrigConfig = self.api.cgrigFromPath(os.environ["CGRIGTOOLS_ROOT"])
        self.assertIsNotNone(self.api.currentConfig())

    def testInstallUpdateEnvironment(self):
        for k, v in self._originalEnv.items():
            v["name"] = k
            break
        envDict = v
        self.cgrigConfig.resolver.updateEnvironmentDescriptorFromDict(envDict)
        self.cgrigConfig.resolver.resolveFromPath(self.cgrigConfig.resolver.environmentPath())
        self.assertTrue(len(list(self.cgrigConfig.resolver.cache.keys())) != 0)

        package = self.cgrigConfig.resolver.cache[list(self.cgrigConfig.resolver.cache.keys())[0]]
        descriptorInstance = self.cgrigConfig.descriptorForPackageName(package.name)

        # local imports are used due to cgrig requiring bootstrapping otherwise configuration don't exist.
        from cgrig.core.descriptors import descriptor
        self.assertIsNotNone(descriptorInstance)
        self.assertIsInstance(descriptorInstance, descriptor.Descriptor)
        resolvedDescriptor = self.cgrigConfig.descriptorFromDict(descriptorInstance.serialize())
        self.assertEqual(resolvedDescriptor, descriptorInstance)
