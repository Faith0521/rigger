# -*- coding: utf-8 -*-
"""Sets the Default Presets for the shaderpresets_ior.json

"""

import json
import os

from cgrig.core.util import env

if env.isMaya(): # todo fix this

    from cgrig.libs.maya.cmds.lighting.presets import IBLQUICKDIRKEY, PRESETQUICKDIR

    PRESETS = {IBLQUICKDIRKEY: "",
               PRESETQUICKDIR: ""}

    jsonFilePath = os.path.join(os.path.dirname(__file__), 'lightpresets.json')
    with open(jsonFilePath, 'w') as outfile:
        json.dump(PRESETS, outfile, sort_keys=True, indent=4, ensure_ascii=False)

