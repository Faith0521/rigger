import os

from basetest import BaseTest


class TestCgRigConfig(BaseTest):
    def setUp(self):
        from cgrig.core import api
        self.api = api
        self.cgrigConfig = api.cgrigFromPath(os.environ["CGRIGTOOLS_ROOT"])

    def testCreatePackage(self):
        outputDir = self._testFolder
        packagePath = os.path.join(outputDir, "testPackage")
        args = ["--destination", packagePath, "--name", "myPackage", "--author", "sparrow", "--displayName",
                "my Package"]
        self.cgrigConfig.runCommand("createPackage",
                                  arguments=args)
        self.assertTrue(os.path.exists(packagePath))
        self.assertTrue(os.path.exists(os.path.join(packagePath, "cgrig_package.json")))
        self.cgrigConfig.runCommand("uninstallPackage",
                                  ["--name", "myPackage", "--remove"])
        self.assertFalse(os.path.exists(packagePath))
