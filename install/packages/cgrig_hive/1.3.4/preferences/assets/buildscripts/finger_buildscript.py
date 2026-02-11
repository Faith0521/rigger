from maya import cmds

from cgrig.libs.hive import api
from cgrig.libs.maya.cmds.objutils import attributes, matching
from cgrig.libs.maya.cmds.rig import controls as con



class FingerBuildScript(api.BaseBuildScript):  # Change (object) to (api.BaseBuildScript), change the class name to your name.
    """

    .. note::

        最好阅读基类中的properties方法 :func:`api.BaseBuildScript.properties`

    """
    # unique identifier for the plugin which will be referenced by the registry.
    # 插件的唯一标识符，将在注册表中引用
    id = "finger"  # change id to name that will appear in the hive UI.

    def postPolishBuild(self, properties):
        baseName = "finger"  # can be renamed, duplicate script and rename along with the id (above and class name)
        rig = self.rig

        mainComp = rig.componentCache
        control_dict = {}

        for comp in mainComp:
            side = comp.side()
            if side not in control_dict:
                control_dict[side] = {}

            if comp.componentType != baseName:
                continue
            mainCompLayer = comp.rigLayer()
            compName = comp.name()

            if compName not in control_dict[side]:
                control_dict[side][compName] = []
            controllers = []
            for control in mainCompLayer.iterControls():
                controllers.append(control)

            control_dict[side][compName].extend(controllers)



        compTypes = list()

        for side,comps in control_dict.items():
            for compName,ctrls in comps.items():
                compTypes.append(compName)
        compTypes = list(set(compTypes))

        for side, comps in control_dict.items():
            for compName, ctrls in comps.items():
                for control in ctrls:
                    driven = cmds.createNode("transform", name="{}_driven".format(control.name()), p=control.parent().fullPathName())
                    cmds.parent(control.fullPathName(), driven)


            # for controls in allControls:
        #     drivens = list()
        #     for control in controls:
        #         driven = cmds.createNode("transform", name="{}_driven".format(control.name()), p=control.parent().fullPathName())
        #         cmds.parent(control.fullPathName(), driven)
        #         drivens.append(driven)
        #     allDrivenList.append(drivens)


        # print(allDrivenList)
        # for side in [left, right]:
        #     Control = con.createControlCurve(folderpath="",
        #                                       ctrlName="{}_finger_setting_ctrl".format(side),
        #                                       curveScale=[control_scale] * 3,
        #                                       designName=controlconstants.CTRL_SPHERE,
        #                                       addSuffix=False,
        #                                       shapeParent=None,
        #                                       rotateOffset=(0.0, 0.0, 0.0),
        #                                       trackScale=True,
        #                                       lineWidth=-1,
        #                                       rgbColor=[0.1, 0.3, 1.0],
        #                                       addToUndo=True)[0]

                # for compName in allCompTypeList:
                #     attributes.createAttribute(control.name(),
                #                                compName,
                #                                attributeType="float",
                #                                channelBox=True,
                #                                defaultValue=0,
                #                                minValue=0,
                #                                maxValue=10)

            # cmds.setDrivenKeyframe(driven, at="rotateZ",
            #                        cd="{}.{}".format(control.name(), compName),
            #                        dv=0, v=0)
            # cmds.setDrivenKeyframe(driven, at="rotateZ",
            #                        cd="{}.{}".format(control.name(), compName),
            #                        dv=10, v=-90)