import traceback
from importlib import reload

def import_module(module, r=False, v=False):
    mod = None
    try:
        mod = __import__(module)
    except Exception as err:
        try:
            mod = __import__(module, globals(), locals(), [module], 0)
        except Exception as err:
            try:
                mod = __import__('rxParts.'+module, globals(), locals(), [module], 0)
            except Exception as err:
                msgs =  traceback.format_exc()
                if v :
                    print ( 'IMPORT ERROR: {0}'.format(err) )
                    print (msgs)
                return

    # return import data
    if v:
        pass
        #print '\nIMPORTED: {0} {1}'.format(mod, mod.__file__)
    if r and mod:
        try:
            reload(mod)
            if v:
                pass
                #print 'RELOADED: {0} {1}'.format(mod, mod.__file__)

        except Exception as err:
            pass

    if mod:
        return mod


# from AutoRig.BodySys.ui import importMod
# reload(importMod)

# module = 'maya.cmds'
# importMod.import_module(module, r=True, v=True)