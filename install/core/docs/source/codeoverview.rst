Code Overview
#############

.. Note::

    This page is a direct port of our old site version, we will be doing a complete rewrite
    of this page very soon by splitting this into separate pages.

CgRig Tools is a modular tools framework designed to be extended in a studio/pipeline environment or at home.
This page is for programmers who are either curious about adding custom tools to CgRig Tools Pro 2.

This page requires a good knowledge of Python programming, and you should be familiar with the
existing methods of adding tools to Maya. You should also understand how to edit JSON files,
if not, watch the video on `this page <https://realpython.com/lessons/what-is-json/>`_ .

This article only relates to CgRig Tools Pro 2, which is a complete re-write of earlier versions.
Please disregard any knowledge of previous versions of CgRig Tools. CgRig2 is entirely new and has been rebuilt from the ground up.


.. contents:: Table of Contents
   :local:
   :depth: 2


Code Environment – Ide Setup
============================

We use PyCharm (free) for our coding environment (IDE). CgRig is made of many Python Packages
which allow for modular-extendability of our tools, but it also makes the IDE setup a little more complex than usual.

If you’d like to follow along with the tutorial on this page then please complete the
`PyCharm/CgRig Setup Tutorial <pycharmsetup>`_ before continuing.

If you are using another program it may be worth reading the `PyCharm/CgRig Setup Tutorial <pycharmsetup>`_ ,
it may help you setup CgRig Tools Pro 2 in your IDE.



Discord – Channel
=================

All the CgRig Developers hang out on the `CgRig Discord Channel <https://discord.gg/RRrwSJBqFj>`_,
you’re welcome to jump on and ask us questions.


The Aim Of This Page
====================

CgRig Tools Pro 2 is a clean and organized way of managing tools within Maya, and potentially other DCCs.
CgRig offers a lot of functionality.
This quickstart page will explain how CgRig Tools manages multiple Python Packages and
their tools within Maya including shelves and menus.


It will help if you’ve completed the PyCharm/CgRig Setup Tutorial .

On this page, Part One, you’ll learn how CgRig Tools:

#. manages multiple python packages.
#. automatically discovers toolset tools.
#. manages toolset tools with string IDs.
#. adds tools to shelves, menus, and toolsets via JSON.
#. can merge tools from multiple packages into a single Maya shelf.

.. Note::

    The backend of CgRig Tools is still evolving, we’re making this process easier.
    We plan on adding UIs to automate the creation and management of CgRig Packages.
    For now, you’ll need to edit JSON files manually.


The Team
========

Version 2 of CgRig Tools has been created by David Sparrow, Keen Foong and Andrew Silke.

David Sparrow
-------------

David is our lead developer and is responsible for all backend systems, rigging and overseeing code design.
David has a background in Rigging, Assets and Pipeline Development from small scale to large.
David is former Animal Logic and Plastic Wax.
David is a major co-owner of CgRig Tools Pro.

Keen Foong
----------

Keen is our Pyside expert, UIX, and an all-rounder. He knows many coding languages and is also a big Blender fan
and a 3d generalist. Keen is ex Animal Logic and has worked for several smaller studios in Sydney.
Keen is a co-owner of CgRig Tools Pro.

Andrew Silke
------------

Andrew is a 20-year industry veteran, a 3d generalist with a passion for animation.
Andrew has coded the majority of our current artist tools focusing on UIX and artist usability.
Andrew has worked for Animal Logic, Weta, Framestore and Dr D along with many smaller studios.
He is the owner of create3dcharacters.com, he is the trainer on the site, writes these articles,
and is a major co-owner of CgRig Tools Pro.

Credit: Hamish McKenzie
-----------------------

Although Hamish is no longer part of the team, he created the first versions of CgRig Tools.
Version 2 does not use Hamish’s code. However, the spirit of the original CgRig Tools remains.
Many of the newer tools are direct modifications of his earlier tools. Hamish was a rigger and TD
at studios such as Valve, DNA Animation, Dr D, he now works in the mining industry.



Running CgRig Tools Standalone And Inside Maya
============================================

Please note that we’ve designed the CgRig Tools Pro 2 environment to operate outside of Maya.
It’s built to be run standalone and potentially with other DCCs. But for now our focus is on integrating CgRig with Maya.

If you are interested running CgRig standalone or inside of other DCCs please email us. info@create3dcharacters.com.




CgRig Refactoring And Git Access
==============================

We’re still making changes to the CgRig Tools backend code. You’re welcome to start testing your tools
with the caveat that some backend code is likely to change.

We have a page which walks through setting a local environment of cgrigtools via our gitlab repositories.
:ref:`vsc_setup`



Pipeline Friendly Code
======================

CgRig is designed to be extended within company pipelines, and we’ve worked hard to make CgRig2 clean and
free from conflicts and other common pipe issues.

CgRig uses:

– Python Maya Commands (cmds)
– Python API 1 and 2, with a preferences towards API 2 (Open Maya om1 and om2)

We do not use PyMel for speed reasons and its long load times.
However, you’re welcome to use PyMel within the CgRig environment.

CgRig Tools is vanilla Maya compatible. We do not use script jobs, custom nodes, or C++ plugins.
You can save scenes modified with CgRig Tools Pro 2 and open them without loading CgRig and there will be no errors.

We’ll create a page with more technical information on how we’ve designed CgRig to minimize
any pipeline issues or any concerns you may have.

We are also happy to try and meet any specific requirements. Just let us know.


The Problem In Maya
===================

Adding custom and third-party tools to Maya can be difficult. Maya’s APIs are powerful,
but there’s a lot of writing extra code to fill the gaps.

1. It’s difficult to manage Maya shelves and menus.
2. It’s cumbersome to separate tools into different repositories and manage groups of tools.
3. Artist friendly UIs are hard to build and rarely maintain a consistent look and feel.
   Qt/PySide is difficult to maintain and add extra functionality.
4. There’s a lack of general core Maya code for higher level tasks.




The Solution
============

CgRig Tools Pro 2 provides a modular system for managing tools within Maya with Python.

1. All tools are automatically discovered, tracked, and can be added to shelves/menus.
2. Tools can be separated into different repositories via Python packages.
3. UIs can be built more easily with our Qt/PySide framework
4. We include additional core Maya code for common Maya functionality.




CgRig Tools Pro: A Modular Tools Framework
========================================

CgRig is a modular tools framework. It loads multiple Python Packages that can be stored in different locations
anywhere on your network or your local machine. Each Python Package can have its own git repository
so that tools can be grouped and managed more easily.

A single Python Package can contain a one, or many tools.
The contents of the package are entirely up to you as the programmer.
You do not have to use our UI or code frameworks.

CgRig can load each Python Package independently of other packages. So you can create different environments for artists,
departments, load, and unload tools as needed.

Packages are managed with a versioning system.

It’s not essential to know the details of how we combine multiple packages, but if you’re interested,
we’re using `pkgutil <https://docs.python.org/3/library/pkgutil.html>`_.




CgRig Packages
============

A CgRig Package is just a `python package <https://realpython.com/python-modules-packages/#python-packages>`_ .
It’s just a folder with code inside.
A CgRig Package is controlled by a JSON config file that tells CgRig where to find different elements related to Maya.
These elements can be code, tools, preferences, icons, menu and shelf information etc.

CgRig Tools Pro 2 supports the loading of multiple packages, and you can load different package configurations
depending on your requirements.

For example:

Example A – Large Company
-------------------------

A company has multiple departments, and each department requires a different set of tools.
You can create a package that contains all the tools for the “Animators”, another for the “Modelers”,
and another for the “FX” team. When each team loads Maya they can use a different configuration of CgRig Tools
and only load the tools from the corresponding departments.

Example B – Small Company
-------------------------

A smaller company might have a default set of tools that all artists use. However, recurring jobs have their own set of tools.
You could create a package for the “Company Tools” and then a package for “Toyota Car Commercials” and
another package for “McDonalds Commercials”.

The package “Company Tools” can always load, and when an artist works on a new McDonald’s job,
they can load the McDonalds Commercials package which adds additional tools.

Example C – School University
-----------------------------

A University can have different packages, they could be organised by class, subject, or year.
When a student loads Maya they only see the tools they need.

Example D – Dev Testing Environments
------------------------------------

You may wish to have a testing environment with developer package/s that are separate from the live artist package/s.
We support versioning as well, so you can configure testing with all the examples above.

Example E – Individual User
---------------------------

You may be an independent artist or TD who prefers to organise each tool on its own git repository to avoid clutter.
You can have a package for your “Car Auto Rigger” and another package for your “Snow Tracks” tool.

Sometimes individual users may prefer to have a single CgRig Package for all their tools.

Example F – create3dcharacters.com
----------------------------------

Here at create3dcharacters.com we use packages to group our artist tools by category,
if you look at all the tools on the CgRig Tools Pro page, each package is grouped by it’s category.
So “CgRig Model Assets” is a different package to “CgRig Light Suite” is a different package to the “CgRig Shader Tools”.

It doesn't matter what your packages contain or which packages you load. It’s entirely up to you.


Configuring Packages
--------------------

CgRig controls which packages load via a CONFIG file. It’s also possible to have multiple CONFIG files
but we’ll leave that for another page.

For simplicity we’ll concentrate on the default file package_version.config file that comes with CgRig Tools Pro 2.

After installing CgRig Tools Pro, you can open the package_version.config file in a text editor.
The default install location is inside Maya’s preferences folder. For example on Windows::

    Documents\maya\scripts\cgrigtoolspro\config\env\package_version.config

This package_version.config is a JSON file that controls what packages CgRig Tools Pro loads.

Our default packages are stored internally within cgrigtoolspro folder::

    maya/scripts/cgrigtoolspro/install/packages/

Our internal packages in CgRig are entered as “type”: “cgrigtools” rather than specifying a
hardcoded paths such as “type”: “path”.

Internal CgRig Packages example:

.. code-block:: json

    {
        "third_party_community": {
            "name": "third_party_community",
            "type": "cgrigtools",
            "version": "1.1.0"
        },
        "cgrig_animation_tools": {
            "name": "cgrig_animation_tools",
            "type": "cgrigtools",
            "version": "1.1.8"
        },
        "cgrig_artist_palette": {
            "name": "cgrig_artist_palette",
            "type": "cgrigtools",
            "version": "1.2.5"
        },
        "cgrig_camera_tools": {
            "name": "cgrig_camera_tools",
            "type": "cgrigtools",
            "version": "1.3.5"
        },

If you delete a CgRig Package entry inside the package_version.config and save, then when you reload Maya,
CgRig Tools won’t load the deleted package. When you restart Maya all related tools that are found inside
that removed package will be missing.




Adding Your Own Packages By Path
--------------------------------

You can add external path location to your packages by adding the path to the package_version.config.
If you’ve completed the `PyCharm/CgRig Setup Tutorial <pycharmsetup>`_ then you’ve already added the cgrig_example_custom_tools
package to CgRig and completed some of the following sections.

.. code-block:: json

    },
        "my_custom_tools": {
            "type": "path",
            "path": "D:/myPath/my_custom_tools"
    }

In the next section you’ll see this in more detail by downloading our Example Custom Tools Package
and add it to CgRig Tools Pro.

.. note::

    We’re planning to add a UI to help you create and set custom packages, but for now,
    you have to make the package manually by editing the JSON files.




CgRig Example Custom Tools – Download
-----------------------------------

Download our example package `cgrig_example_custom_tools here <https://www.dropbox.com/s/xatpxrf2b1zv0ho/cgrig_example_custom_tools_2.5.0.zip?dl=1>`_ .
Unzip the package anywhere on your machine or network.

Open your package_version.config (previous section) and add the lines below to connect the Example Tools with CgRig Tools Pro.

.. code-block:: json

    },
        "cgrig_example_custom_tools": {
            "type": "path",
            "path": "D:/yourPath/my_tools/cgrig_example_custom_tools"
    }

Save the file and restart Maya. When Maya loads, you should see a new shelf called Custom_Tools.

.. Note::

    In the future, we are planning on creating a CgRig Tools UI where you can create and load your
    custom package from inside Maya without editing the JSON file.




Toolsets
========

When CgRig loads in Maya, it’s now looking for the path,::


    "path": "D:/yourPath/my_tools/cgrig_example_custom_tools"

Inside of that path it wants to find a file called “cgrig_package.json”. So in our case,::

    cgrig_example_custom_tools/cgrig_package.json

Open cgrig_package.json in a text editor, you can see that there are many relative path locations.

The location of the Toolsets Tools is configured with:

.. code-block:: json

    "CGRIG_TOOLSET_UI_PATHS": [
        "{self}/cgrig/apps/uitoolsets"
    ],

{self} refers to the current path of the package.
So in this example {self} is D:/yourPath/cgrig_example_custom_tools and the full path is::

    D:/yourPath/cgrig_example_custom_tools/cgrig/apps/uitoolsets

CgRig will automatically discover any Toolset UIs found inside this location.::

    {self}/cgrig/apps/uitoolsets

It discovers Toolset Tools based on the Python Modules in that directory.
Inside the modules it’s looking for the base class type ToolsetWidgetMaya.

.. code-block:: python

    class PolyCubeBuilder(toolsetwidgetmaya.ToolsetWidgetMaya):

You can disable a UI by changing the base class to object.

.. code-block:: python

    class PolyCubeBuilder(object):  # Disabled



Toolset Tools Vs Regular Tools
------------------------------

At this point its worth mentioning differences between Regular Tools and Toolset Tools. We support both of these types.

**Toolset Tools** are the mini-tools that can be managed in sets. These small tools open with a width that is
halfway between the width of Maya’s Channel Box and the Attribute Editor.
Toolset UIs can be dragged off and combined with other tools. Most of our current tools are Toolset Tools.

**Regular Tools** are tools that do not fit into the small width setting of the Toolset window.
The CgRig Preferences Window and the CgRig Hotkey Manager are examples of windows that are regular tools.

On this page we’ll concentrate on Toolset Tools. The majority ofMaya tools fit into the Toolset compact size.
Artists can easily mix and match and search for Toolset Tools, so Toolsets have a number of advantages so long
as the tool fits into the compact format.




Poly Cube Builder Ui
--------------------

In this section we’ll see how an example Toolset Tool called Poly Cube Builder connects to CgRig.

The Poly Cube Builder tool is a simple UI that builds a cube in Maya with basic options.

.. code-block:: python

    cmds.polyCube()

Navigate to cgrig_example_custom_tools/cgrig/apps/uitoolsets and you’ll find the python UI modules.
Open the code for the UI of the tool Poly Cube Builder UI.::

    cgrig_example_custom_tools/cgrig/apps/uitoolsets/polycubebuilder.py

To see what the tool looks like inside Maya, find the Custom_Tools shelf and click on the
Sphere Icon > Poly Cube Builder open the tool in Maya.




Change A Tool Icon
------------------

Changing the icon of a tool is a fun way of seeing how CgRig works.
We’ll change the icon of this tool to a “save” icon, then reload CgRig to see that
the icon has updated in multiple locations. You’ll see how the add your custom icons as PNG too.

To change the icon of Poly Cube Builder open polycubebuilder.py and edit line 13::

    "icon": "cubeWire",

Change it to the “save” icon,::

    "icon": "save",

The “save” icon is a default CgRig icon, it’s included in our cgrig_core package. Now reload CgRig Tools Pro to see the new icon.

CgRigToolsPro (shelf) > Developer Icon (purple code icon) > Reload
or
Reload CgRig Hotkey: ctrl shift alt [

You’ll see that the tool’s icon has changed in Maya.

Custom_Tools (shelf) > Sphere (Icon) > Poly Cube Builder

Load the tool, and you’ll also see that the icon has changed inside the CgRig Toolsets Window.

You can also see the tool in the CgRig Tools Menu.

CgRigTools (top menu) > Modeling > Poly Cube Builder

The icon has changed here too.

When CgRig reloads it deletes and rebuilds any shelves/menus in Maya that are related to CgRig Tools while reloading all of CgRig’s code.

The Poly Cube Builder tool will display it’s new “save” icon.




Add A Custom Icon
-----------------

To add a custom icon, place a new 64 x 64 PNG in the icons folder.::

    cgrig_example_custom_tools/icons

Icons can be any color, but we use PNGs with white on transparent backgrounds.
In code CgRig colors white icons for our stylesheets and Toolset shelves.
By using white on black it’s also easy to add icons from a library such as `The Noun Project <https://thenounproject.com/>` .
Few TDs want to create icons themselves.

We usually default our icons to be 64 x 64 so name the new image with the suffix “_64.png” so “myNewIcon_64.png”.

New icons require unique names as they are registered as a giant list and merged with all CgRig icons. Be sure your icon has a unique name.

While adding icons in code always use the name without the “_64.png”.
So don’t call the icon as “myNewIcon_64.png” instead use “myNewicon” for the icon name.::

    "icon": "myNewIcon",



Tracking Tools With String Ids
------------------------------

Each Toolset tool is registered with a unique string ID. In the case of a Toolsets Mini Tool
you set the string identifier in the Toolset UI code.

The string IDs of tools are important because CgRig tracks all UIs,
and you can send functionality from one UI to another. For example,
if you change the renderer then CgRig will automatically change the renderer for all renderering tools.

Go back to the UI file::

    cgrig_example_custom_tools/cgrig/apps/uitoolsets/polycubebuilder.py

See line 10,::


    id = "polyCubeBuilder"

The Poly Cube Builder’s Toolset ID is called polyCubeBuilder.
CgRig Tools keeps track of all tools with their string IDs to call them in numerous ways.
For example, we also use the string IDs to create shelf icons, menu entries or within our Toolsets Shelf.
String IDs are also compatible with JSON data, and we use them in our marking menus too.

You can also open the Toolset tool using the string ID with code such as:

.. code-block:: python

    from cgrig.apps.toolsetsui import run
    run.openTool("polyCubeBuilder")



How CgRig Creates Shelf And Menu Items
------------------------------------
In this section, you’ll see how CgRig uses the tool’s string IDs inside JSON files to build shelf icons,
menu entries and add tools to CgRig’s Toolset Window. You can also make CgRig marking menus with JSON too.

Lets start by seeing how CgRig adds shelf icons.

Back inside the cgrig_example_custom_tools/cgrig_package.json you can see another dict entry called CGRIG_SHELF_LAYOUTS

.. code-block:: json

    "CGRIG_SHELF_LAYOUTS": [
     "{self}/cgrig/apps/maya_integrate/example_custom_tools_shelf.layout"
    ],

This cgrig_package.json points to another JSON that builds the icons on the shelf. See,::

    cgrig_example_custom_tools/cgrig/apps/maya_integrate/example_custom_tools_shelf.layout

Open example_custom_tools_shelf.layout in a text editor, and you can see how the Poly Cube
Builder is added to Maya’s shelf on line 12.

.. code-block:: json

    {
        "type": "toolset",
        "id": "polyCubeBuilder"
    },

The CgRig Menu layout is identical to the shelf. See,::

    cgrig_example_custom_tools/cgrig/apps/maya_integrate/example_custom_tools_menu.layout

.. code-block:: json

    {
        "type": "toolset",
        "id": "polyCubeBuilder"
    },

The tool’s metadata, including its icon, is given inside the tool’s UI code. So when we add the tool
to a shelf or a menu, we only need its string ID.




How CgRig Manages The CgRig Toolset Shelf
-------------------------------------

We also need to specify how the tool gets added to the CgRig Toolsets Window. Open,::

    cgrig_example_custom_tools/cgrig/apps/maya_integrate/example_custom_tools_toolsets.layout

You can see that the Toolset Window specifies the set name “My Custom Tools” the color, [42,255,0] and
adds the tool ID “polyCubeBuilder” as the first icon in the “My Custom Tools” shelf.

.. code-block:: json

    {
      "toolsetGroups": [
        {
          "type": "myCustomTools",
          "name": "My Custom Tools",
          "color": [
            42,
            255,
            0
          ],
          "hueShift": 0,
          "toolsets": [
            "polyCubeBuilder",
            "polyCubeBuilderColor",
            "objectCubeArraySimple",
            "objectCubeArrayProperties",
            "objectCubeArrayUIModes",
            "objectCubeArrayImageTest"
          ]
        }
      ]
    }



Change The Custom Shelf Name
----------------------------

It’s easy to change the shelf name of “Custom_Tools”. Open,

cgrig_example_custom_tools/cgrig/apps/maya_integrate/example_custom_tools_shelf.layout

And change the name of the menu on line 4 to be:


"name": "My Named Shelf",
Save the file and reload CgRig Tools with:

CgRigToolsPro (shelf) > Developer Icon (purple code icon) > Reload

You should see the “Custom_Tools” shelf becomes “My Named Shelf.”




Merge The Custom & CgRig Shelves
------------------------------

Multiple packages can share the same shelf. In this example we’ll merge the Custom Shelf with the CgRigToolsPro shelf.

Open, ::

    cgrig_example_custom_tools/cgrig/apps/maya_integrate/example_custom_tools_shelf.layout

And rename the shelf to be the same as CgRig Tools, so line 4::

    "name": "CgRigToolsPro",

Now reload CgRig Tools,

CgRigToolsPro (shelf) > Developer Icon (purple code icon) > Reload

The Custom_Tools shelf will disappear, now all the tools from the example_custom_tools
package have been merged with the CgRigToolsPro shelf.

You can now find the Poly Cube Builder tool under,

CgRigToolsPro (shelf) > Sphere Green Modeling (Icon) > Poly Cube Builder

CgRig can find tools from multiple packages and create a single shelf or various shelves.

We’re building the CgRigToolsPro shelf from multiple packages.
And you can sort the order of icons with a weighting too, see “sortOrder” in the cgrig_dynamics_tools package.

.. code-block:: json

    {
      "sortOrder": -930,
      "shelves": [
        {
          "name": "CgRigToolsPro",
          "children": [
            {
              "id": "cgrig.shelf.dynamics",
              "displayLabel": false,
              "icon": "fxDynamicsMenu_shlf",
              "children": [
                {
                  "id": "nclothwrinklecreator",
                  "type": "toolset"
                }
              ]
            }
          ]
        }
      ]
    }

Conclusion
==========

This concludes the first part of this walk through tutorial.

On this page, you’ve learned how CgRig Tools:

#. manages multiple python packages.
#. automatically discovers toolset tools.
#. manages toolset tools with string IDs.
#. adds tools to shelves, menus, and toolsets via JSON.
#. can merge tools from multiple packages into a single Maya shelf.