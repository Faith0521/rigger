import maya.cmds as mc
import os
import re
import assetEnv

# Import highest template
def importVersioned(path):
    # Import newest file from path

    if not os.path.isdir(path):
        mc.warning('Path doesnt exist: '+path)
        return

    # Get template files
    regexp = '_v({0}|{1}|{2}|{3}).'.format('[0-9]', '[0-9]'*2, '[0-9]'*3, '[0-9]'*4)

    afiles = os.listdir(path)
    files = [f for f in afiles if re.search(regexp, f)]
    files.sort()
    # Put newest file in files[0]
    files.reverse()

    if not files:
        mc.warning('No versioned template files in: '+path)
        return

    if files:
        filepath = os.path.join(path, files[0])
        snap = mc.ls('|*')
        if os.path.isfile(filepath):
            mc.file(filepath, i=1)
            print ('IMPORTED FILE: '+filepath)

            newsnap = mc.ls('|*')
            for n in snap: newsnap.remove(n)
            return newsnap

# import layout
def template():
    path = os.path.join(assetEnv.getpath(), 'build', 'template')
    importVersioned(path)

# Import rigrx
def rig(rigType):
    path = os.path.join(assetEnv.getpath(), rigType)
    importVersioned(path)

# Import model
def model():
    try:
        importVersioned(os.path.join(assetEnv.getpath(), 'model'))
    except:
        mc.error('Import model failed !')