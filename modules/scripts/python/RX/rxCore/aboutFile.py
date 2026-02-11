import os 
import re 

# get name and path to a NEW highest versioned file
def getNewTemplateVersion(path, asset, suffix):
    if not os.path.isdir(path):
        return

    files = [f for f in os.listdir(path) if re.search('_v[0-9][0-9][0-9].', f)]
    files.sort()
    files.reverse()

    v = '001'
    if files:
        version = int(files[0].split('.')[0].split('_v')[-1])
        v = str(version + 1).zfill(3)

    new = os.path.abspath( os.path.join( path,  asset+'_'+suffix+'_v'+v+'.ma'))
    return new

def getNewModelVersion(path, asset, lod):
    return getNewTemplateVersion(path, asset, 'model_'+lod)

def getNewWorkRigVersion(path, asset, suffix, rig):
    if not os.path.isdir(path):
        return

    files = [f for f in os.listdir(path) if re.search(rig+'_v[0-9][0-9][0-9].', f)]
    files.sort()
    files.reverse()

    v = '001'
    if files:
        for i in range(len(files)):
            v = str(i+2).zfill(3)

    if suffix:
        suffix += '_'
    newname = asset+'_'+suffix+rig+'_v'+v+'.ma'
    newname = newname.replace('__', '_')
    new = os.path.abspath(os.path.join( path, newname))
    return new

def getNewVersion(path, name, suffix=''):

    if not os.path.isdir(path):
        return

    items = [f for f in os.listdir(path) if re.search('_v[0-9][0-9][0-9]', f)]
    items.sort()
    items.reverse()
    files = []

    for f in items:
        if name+'_v' in f:
            files.append(f)
            
    v = '001'
    if files:
        for i in range(len(files)):
            v = str(i+2).zfill(3)

    new = os.path.join(path, name+'_v'+v+suffix)
    return new

def getHighestVersion(path):
    if not os.path.isdir(path):
        return ''
    files = [f for f in os.listdir(path) if re.search('_v[0-9][0-9][0-9].', f)]
    itemdict = {}
    count = []
    for f in files:
        idx =  f.split('.')[0].split('_v')[-1]
        count.append(idx)
        itemdict[idx] = f

    items = []
    count.sort()
    for c in count:
        items.append(itemdict[c])

    items.reverse()
    if items:
        return items[0]
    else:
        return ''