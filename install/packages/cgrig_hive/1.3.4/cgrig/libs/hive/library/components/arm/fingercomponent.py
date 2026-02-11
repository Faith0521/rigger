from cgrig.libs.hive.library.components.general import fkcomponent
from cgrig.libs.maya.cmds.objutils import attributes
from maya import cmds


class FingerComponent(fkcomponent.FkComponent):
    creator = "David Sparrow"
    definitionName = "finger"
    uiData = {"icon": "componentFK", "iconColor": (), "displayName": "Finger"}
    _bindJntIdPrefix = "bind"

    def preSetupGuide(self):
        """Overridden to force autoAlign off, this is temporary measure until we expose the world up Vector
        of the alignment.
        """
        super(FingerComponent, self).preSetupGuide()
        for guide in self.definition.guideLayer.iterGuides(False):
            attrDef = guide.attribute("autoAlign")
            if attrDef:
                attrDef.value = False

        for guide in self.guideLayer().iterGuides(False):
            guide.autoAlign.set(False)

