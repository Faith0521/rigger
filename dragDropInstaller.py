"""Drag & Drop installer for Maya 2018+"""

import os, sys
# confirm the maya python interpreter
CONFIRMED = False
try:
    from maya import cmds
    CONFIRMED = True
except ImportError:
    CONFIRMED = False

def onMayaDroppedPythonFile(*args, **kwargs):
    _add_module()

def _add_module():
    rigger_module = os.path.normpath(os.path.join(os.path.dirname(__file__), "modules"))
    module_file_content = """+ cgrig any %s \n""" % rigger_module
    module_file_content += """CGRIG_ROOT := ../../ \n"""
    module_file_content += """+ OF3D_RIG any %s \n""" % rigger_module
    module_file_content += """icons: icons\n"""
    module_file_content += """scripts: scripts/python\n"""

    user_module_dir = os.path.join(cmds.internalVar(uad=True), "modules")
    if not os.path.isdir(user_module_dir):
        os.mkdir(user_module_dir)
    user_module_file = os.path.join(user_module_dir, "cgrig.mod")
    if os.path.isfile(user_module_file):
        os.remove(user_module_file)

    f = open(user_module_file, "w+")
    f.writelines(module_file_content)
    f.close()

    # first time initialize
    cmds.confirmDialog(title='Rigger Message', message="Trigger Module Installed. Please restart Maya.")
    pass
