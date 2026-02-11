from cgrig.libs.hive import api
from cgrig.core.util import zlogging
from cgrig.libs.maya import zapi
from cgrig.libs.utils import output

logger = zlogging.getLogger(__name__)


class JawMouthAddAttrsBuildScript(api.BaseBuildScript):
    id = "mouth_addAttrsToJaw"  # change id to name that will appear in the hive UI.

    def postPolishBuild(self, properties):
        jawComponents = list(self.rig.componentsByType("jaw"))
        mouthComponents = list(self.rig.componentsByType("mouthcomponent"))
        if not jawComponents or not mouthComponents:
            output.displayWarning("No jaw components or mouth components found")
            return
        jawComponent = jawComponents[0]
        mouthComponent = mouthComponents[0]
        logger.debug("Adding mouth attributes to jaw")

        mouthControlPanel = mouthComponent.controlPanel()
        attrPlugs = [mouthControlPanel.attribute(i.name) for i in mouthComponent.definition.rigLayer.nodeSettings(api.constants.CONTROL_PANEL_TYPE)]
        for ctrl in jawComponent.rigLayer().iterControls():
            attrName = str("__")
            while ctrl.hasAttribute(attrName):
                attrName += "_"
            ctrl.addAttribute(attrName, Type=zapi.attrtypes.kMFnkEnumAttribute,
                              locked=True, keyable=False, channelBox=True,
                              enums=("MOUTH",))
            for attr in attrPlugs:
                name = attr.partialName(includeNodeName=False)
                if attr.apiType() == zapi.attrtypes.kMFnkEnumAttribute:
                    attrName = str(name)
                    while ctrl.hasAttribute(attrName):
                        attrName = attrName+"_"

                    ctrl.addAttribute(attrName, zapi.attrtypes.kMFnkEnumAttribute,
                                      locked=True, keyable=False, channelBox=True,
                                      enums=attr.enumFields())
                else:
                    ctrl.addProxyAttribute(attr, name)


