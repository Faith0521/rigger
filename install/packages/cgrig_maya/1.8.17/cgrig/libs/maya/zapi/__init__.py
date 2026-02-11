# -*- coding: utf-8 -*-
from .base import *
from .spaceswitching import *
from .nodecreation import *
from cgrig.libs.maya.api import (constants, attrtypes)

from .animation import (gimbalTolerance,
                        allGimbalTolerances,
                        setRotationOrderOverFrames,
                        keyFramesForNodes,
                        keyFramesForNode,
                        frameRanges
                        )
from .errors import (ObjectDoesntExistError,
                     InvalidPlugPathError,
                     ReferenceObjectError,
                     InvalidTypeForPlugError,
                     ExistingNodeAttributeError)
