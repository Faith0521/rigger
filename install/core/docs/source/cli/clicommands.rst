.. _CLI_commands:

CLI Commands
####################################################

In CgRigtools we have have a CLI interface which allows
you run arbitrary commands for example loading an application with CgRigtoolsPro,
managing CgRig packages.

Before we begin playing around make sure you have
a copy of cgrigtools in a development location eg. documents/cgrigtoolspro.

Commands documentation

.. toctree::

    ./commands

CLI
===

You should cd into the root folder of cgrigtools.
This is required due to the cli using the working directly as a
way to determine the location of internal files.

All operations are done using the 'install/core/bin/cgrig_cmd'

Lets first setup cgrigtools and add it to maya.
::

    cd cgrigtoolspro
    call ./bin/cgrig_cmd.bat setup --destination destination/folder --zip myCgRigtools.zip --app maya --app_dir
    ~/Documents/maya/modules

In the case you want to install a new package you can use the '--install' flag.
Like the following.
::

    cd cgrigtoolspro
    call ./bin/cgrig_cmd.bat installPackage --path myPackagePath

You can also do --inPlace 1 if you want ot use the package directly without
::

    call ./bin/cgrig_cmd.bat installPackage --path myPackagePath --inPlace


Git tags are also supported defined like so
::

    cd cgrigtoolspro
    call install/core/bin/cgrig_cmd.bat installPackage --path https:\\myGitpath.git --tag v1.0.0


.. note: 

    It's important to understand that a package.json file MUST exist
    under the package directory.
    Once installed the package will be located in.
    cgrigtoolspro/install/packages/myPackage/{packageVersion}

Python
======

It's also Possible to run any CLI command via the python api

.. code-block:: python

    from cgrig.core import api
    cgrig = api.cgrigFromPath(os.environ["CGRIGTOOLS_PRO_ROOT"])
    cgrig.runCommand("installPackage" ("--path somePath/folder", "--inPlace"))