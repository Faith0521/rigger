#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import json
import getpass
import maya.cmds as mc

# store clean sys path
# path = os.path.realpath(os.path.dirname(__file__))
# if not path in os.environ['MAYA_PLUG_IN_PATH']:
#     os.environ['MAYA_PLUG_IN_PATH'] = os.environ['MAYA_PLUG_IN_PATH']+':'+os.path.join(path, 'plugins')

if not 'rxSYSPATH' in os.environ:
    os.environ['rxSYSPATH'] = '%'.join(sys.path)

if not 'rxROOT' in os.environ:
    os.environ['rxROOT'] = ''

if not 'rxUSER' in os.environ:
    os.environ['rxUSER'] = getpass.getuser()

if not 'rxASSET' in os.environ:
    os.environ['rxASSET'] = ''

if not 'rxPATH' in os.environ:
    os.environ['rxPATH'] = ''

if not 'rxCACHE' in os.environ:
    os.environ['rxCACHE'] = 'True'

if not 'rxRIG_TYPE' in os.environ:
    os.environ['rxRIG_TYPE'] = ''

if not 'rxRIGHT_MENU' in os.environ:
    os.environ['rxRIGHT_MENU'] = 'True'


def whereAmI():
    path = os.path.dirname(os.path.realpath(__file__))
    path  = path.replace('\assetEnv.py', '')
    return path


# Set env functions
def setsys():
    # string to list
    sys.path = os.environ['rxSYSPATH'].split('%')

    # rtPATH
    path = getpath()
    if path:
        # os.path.join path\build\template
        sys.path.insert(0, os.path.join(path, 'build', 'template'))
        sys.path.insert(0, os.path.join(path, 'build', 'scripts'))


def setuser(user=None, prompt=False):
    """Set current user in env """

    if prompt:
        result = mc.promptDialog(
                    title='Set User',
                    message='User Name:',
                    button=['Cancel', 'Set'],
                    defaultButton='Set',
                    cancelButton='Cancel',
                    dismissString='Cancel')

        if result == 'Set':
            user = mc.promptDialog(query=True, text=True)
            user.strip()
            os.environ['rxUSER'] = user
    elif user:
        os.environ['rxUSER'] = user
    else:
        os.environ['rxUSER'] = getpass.getuser()
    return os.environ['rxUSER']


def setroot(browse=False):
    """Set rigsystem root path in env """

    try:
        #'C:/Users/wangruixi/Documents/maya/2018/prefs/'
        if mc.internalVar(upd=1) not in sys.path:
            sys.path.append(mc.internalVar(upd=1))

        # when the new root path generate, there is a rigtools setting file create.
        import rigtools_settings

    except:
        pass

    if browse or not os.path.isdir(os.environ['rxROOT']):
        msg = ' ----   Set Asset Root Env   ---- '
        result = mc.confirmDialog( title='Set Env',
                                message=msg,
                                button=['Cancel', 'Browse'],
                                defaultButton='Browse',
                                cancelButton='Cancel',
                                dismissString='Cancel' )

        if result == 'Browse':
            bpath = mc.workspace('default', q=1, rd=1)
            bresult = mc.fileDialog2(dir=bpath, fm=3)

            if bresult:
                if not os.path.isdir(bresult[0]):
                    try:
                       # useless?
                       os.makedirs(bresult[0])
                    except:
                        pass

                if os.path.isdir(bresult[0]):
                    # use (os.path.join) to merge path string.
                    filename = os.path.join(mc.internalVar(upd=1), 'rigtools_settings.py')
                    # write env info in *.py
                    f = open(filename, 'w')
                    f.write('import os\nos.environ["rxROOT"] = "{0}"'.format(bresult[0]))
                    f.close()

                os.environ['rxROOT'] = bresult[0]
    return os.environ['rxROOT']

def setasset(asset=None):
    if asset is None:
        os.environ['rxASSET'] = ''
        os.environ['rxPATH'] = ''

    else:
        root = getroot()
        path = os.path.join(root, asset)
        if root and os.path.isdir(path):
            path = path.replace('\\', '/')
            jfile = os.path.join(path, 'build', 'assetinfo.json')
            if os.path.isfile(jfile):
                os.environ['rxASSET'] = asset
                os.environ['rxPATH'] = path
        else:
            os.environ['rxASSET'] = ''
            os.environ['rxPATH'] = ''
    setrigtype()

def setrigtype(rigType=None):
    asset = getasset()
    if not asset:
        os.environ['rxRIG_TYPE'] = ''
        return
    elif not rigType:
        rigType = getrigtype()

    rigTypes = getjsoninfo('rigTypes')

    if rigTypes and rigType in rigTypes:
        os.environ['rxRIG_TYPE'] = rigType

    elif rigTypes:
        os.environ['rxRIG_TYPE'] = rigTypes[0]

    else:
        os.environ['rxRIG_TYPE'] = ''

def setcache(state=True):
    if state:
        os.environ['rxCACHE'] = 'True'
    else:
        os.environ['rxCACHE'] = 'False'

def setRightMenu(state=True):
    if state:
        os.environ['rxRIGHT_MENU'] = 'True'
    else:
        os.environ['rxRIGHT_MENU'] = 'False'


# Get env functions
def getroot():
    return os.environ['rxROOT']

def getuser():
    return os.environ['rxUSER']

def getasset():
    return os.environ['rxASSET']

def getpath():
    return os.environ['rxPATH']

def getrigtype():
    return os.environ['rxRIG_TYPE']

def getcache():
    if os.environ['rxCACHE'] == 'True':
        return True
    else:
        return False

def getjsoninfo(key=None):
    # "asset": "test",
    # "createdBy": "rosa",
    # "creationDate": "Wed, Jul 03 2019",
    # "rigTypes": [
    #     "gameRrig",
    #     "mocapRig",
    #     "rig"   ]

    asset = getasset()
    path = getpath()

    if asset and path:
        jfile = os.path.join(path, 'build', 'assetinfo.json')
        if os.path.isfile(jfile):
            with open(jfile, 'r') as f:
                data = json.load(f)
                return data.get(key, data)

def geticons():
    iconpath = whereAmI() + '/rxIcons'
    return iconpath
