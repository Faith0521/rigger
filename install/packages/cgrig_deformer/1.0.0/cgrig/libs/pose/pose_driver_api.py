# Copyright Epic Games, Inc. All Rights Reserved.

# Built-in

import json
from collections import OrderedDict

# External
from maya import cmds

# Internal
from cgrig.libs.pose import pose_util as util
from cgrig.libs.maya.cmds.objutils import curves, attributes


class PoseDriverNode(object):
    node_flag = 'tag'

    def __init__(self, node):
        """
        Initialize PoseDriverNode on give node

        >>> node = str()
        >>> PoseDriverNode(node)
        """

        if not cmds.objExists('{node}.{attr}'.format(node=node, attr=self.node_flag)):
            raise TypeError('Found no node attribute: "{}.{}"'.format(node, self.node_flag))
        if cmds.objExists('{node}.{attr}'.format(node=node, attr=self.node_flag)):
            if not cmds.getAttr('{node}.{attr}'.format(node=node, attr=self.node_flag)) == "poseDriver":
                raise AttributeError('Object node attribute {} value is not "poseDriver"'.format(self.node_flag))

        # self._node = node
        self._node = node
        self.cmd_node = node.replace('parent_handle', 'cmd_bridge')

    def __repr__(self):
        """
        Returns class string representation
        """
        return '<PoseDriverNode>: {}'.format(self._node)

    def __str__(self):
        """
        Returns class as string
        """
        return str(self._node)

    def __eq__(self, other):
        """
        Overrides equals operator to allow for different RBFNode instances to be matched against each other
        """
        return str(self) == str(other)

    # -------------------------------------------------------------------------

    @classmethod
    def create(cls, name=None, parent=None, axis='+x', side='L', scale=1.0):
        """
        Create Pose Driver

        >>> pose_driver_node = PoseDriverNode.create()
        """

        if name is None:
            name = '{}#'.format('poseDriver')

        mirror = False
        renameAttr = True
        if side == 'L':
            mirror = False
            renameAttr = False
        if side == 'R':
            mirror = True
            renameAttr = False
        if side == 'M':
            mirror = False
            renameAttr = True

        # build data
        # 判断创建朝向的dict
        axisDict = {'AXIS': ['rotateList', 'isReverse'],
                    '+x': [(0, 0, 0), False],
                    '-x': [(0, 0, 0), True],
                    '+y': [(0, 0, -90), True],
                    '-y': [(0, 0, -90), False],
                    '+z': [(0, -90, 0), False],
                    '-z': [(0, -90, 0), True]}

        # 不同轴向的属性名dict
        attrNameDict = {'x': ['up', 'down', 'front', 'back'],
                        'y': ['outer', 'inner', 'front', 'back'],
                        'z': ['up', 'down', 'inner', 'outer']}

        # 平面角度区间判断的dict
        driverAxisDict = {'sort': [0, 1, 2, 3],
                          0: [-90, -180, 180, 90],
                          1: [-90, 0, 90],
                          2: [-180, -90, 0],
                          3: [180, 90, 0]}

        followCurvePointList = [(0.0, 0.0, 0.0), (-5.0, 0.0, 0.0)]

        parentCurvePointList = [(0.0, -3.5, 0.0), (1.5543122344752192e-15, -5.0, 3.3306690738754706e-16),
                                (4.440892098500626e-16, -3.535533905029297, 3.535533905029297),
                                (-1.1102230246251565e-15, 1.1102230246251565e-16, 5.0), (0.0, 0.0, 3.5),
                                (-1.1102230246251565e-15, 1.1102230246251565e-16, 5.0),
                                (-2.0141816681326294e-15, 3.535533905029297, 3.535533905029297),
                                (-1.5543122344752192e-15, 5.0, -2.220446049250314e-16),
                                (-4.440892098500626e-16, 3.535533905029297, -3.535533905029297),
                                (1.1102230246251565e-15, -3.3306690738754696e-16, -5.0),
                                (2.0141816681326294e-15, -3.535533905029297, -3.535533905029297),
                                (1.5543122344752192e-15, -5.0, 3.3306690738754706e-16),
                                (0.0, -3.5, 0.0)]

        followPosition = [5, 0, 0]  # 指向默认位置的向量  绝对角度的起点
        downPosition = [0, -5, 0]  # 指向down的向量  平面角度的起点
        parentRotate = axisDict[axis][0]

        # side
        sideReverse = axisDict[axis][1]
        if mirror:
            sideReverse = not sideReverse
            parentRotate = [rE * -1 for rE in parentRotate]
        if sideReverse:
            followCurvePointList = [[listE2 * -1 for listE2 in listE] for listE in followCurvePointList]
            followPosition = [vE * -1 for vE in followPosition]

        # build
        followHandle = cmds.curve(n='{0}_psd_follow_handle'.format(name), d=1, p=followCurvePointList)
        parentHandle = cmds.curve(n='{0}_psd_parent_handle'.format(name), d=1, p=parentCurvePointList)
        cmdBridge = cmds.createNode('transform', n='{0}_psd_cmd_bridge'.format(name))
        cmds.parent(followHandle, cmdBridge, parentHandle)
        cmds.setAttr('{0}.t'.format(followHandle), *followPosition)
        cmds.setAttr('{0}.r'.format(parentHandle), *parentRotate)

        # modify handle curve
        for handle in [followHandle, parentHandle]:
            curves.Control(handle).set_shape_name()
            curves.Control(handle).set_color(30)
            curves.Control(handle).set_shape_width(5)
            curves.Control(handle).set_locked(["sx", "sy", "sz", "v"])

        # modify cmds bridge
        attributes.lock_and_hide_default(cmdBridge)
        # aboutLock.lock(cmdBridge)

        # angle angleBetween
        angleABName = cmds.createNode('angleBetween', n='{0}_psd_base_alb'.format(name))
        for axisE in 'xyz':
            cmds.connectAttr('{0}.t{1}'.format(followHandle, axisE), '{0}.v1{1}'.format(angleABName, axisE))
        cmds.setAttr('{0}.v2'.format(angleABName), *followPosition)

        # plane angleBetween
        planeABName = cmds.createNode('angleBetween', n='{0}_psd_plane_alb'.format(name))
        cmds.connectAttr('{0}.ty'.format(followHandle), '{0}.v1y'.format(planeABName))
        cmds.connectAttr('{0}.tz'.format(followHandle), '{0}.v1z'.format(planeABName))
        cmds.setAttr('{0}.v2'.format(planeABName), *downPosition)

        # plane condition
        angleCNode = cmds.createNode('condition', n='{0}_psd_angle_cnd'.format(name))
        cmds.setAttr('{0}.operation'.format(angleCNode), 2)
        cmds.connectAttr('{0}.tz'.format(followHandle), '{0}.ft'.format(angleCNode))
        cmds.connectAttr('{0}.a'.format(planeABName), '{0}.ctr'.format(angleCNode))
        cmds.connectAttr('{0}.a'.format(planeABName), '{0}.cfr'.format(angleCNode))

        # input reverse
        unitConversionList = cmds.listConnections('{0}.ctr'.format(angleCNode), d=False)
        if unitConversionList:
            cmds.setAttr('{0}.conversionFactor'.format(unitConversionList[0]),
                       cmds.getAttr('{0}.conversionFactor'.format(unitConversionList[0])) * -1)

        # 单方向sdk
        inputUnitConversion = []
        intputAttr = []

        for keyE in driverAxisDict['sort']:
            angleList = driverAxisDict[keyE]
            attrName = '{0}.{1}'.format(cmdBridge, attrNameDict[axis[1]][keyE])
            attributes.createAttribute(
                cmdBridge, attrNameDict[axis[1]][keyE], attributeType="double", channelBox=True, nonKeyable=False, defaultValue=0
            )
            for angleE in angleList:
                sdkValue = 0
                if angleE in angleList[1:-1]:
                    sdkValue = 1
                util.remapSDK(attrName, dv=angleE, v=sdkValue, cd='{0}.ocr'.format(angleCNode))
                intputAttr = cmds.listConnections(attrName, d=False, p=True)

            if inputUnitConversion:
                util.multiplyCombine(intputAttr[0], inputUnitConversion, attrName)
            else:
                connectDict = util.multiplyCombine(intputAttr[0], '{0}.a'.format(angleABName), attrName)
                inputUnitConversion = connectDict['input2']

        # 斜方向sdk
        for nameStrIndex in driverAxisDict['sort'][:2]:
            nameStr = attrNameDict[axis[1]][nameStrIndex]

            for suffixStrIndex in driverAxisDict['sort'][2:]:
                suffixStr = attrNameDict[axis[1]][suffixStrIndex]
                attrStr = '{0}{1}'.format(nameStr, suffixStr.title())
                attrName = '{0}.{1}'.format(cmdBridge, attrStr)
                # attribute.addAttributes(cmdBridge, attrStr, "double", value=0, keyable=True)
                attributes.createAttribute(
                    cmdBridge, attrStr, attributeType="double", channelBox=True, nonKeyable=False,
                    defaultValue=0
                )
                sdk0List = []
                for zeroListE in (driverAxisDict[nameStrIndex], driverAxisDict[suffixStrIndex]):
                    angleList = zeroListE[1:-1]
                    if len(angleList) > 1:
                        if driverAxisDict[suffixStrIndex][1] > 0:
                            sdk0List.append(angleList[1])
                        elif driverAxisDict[suffixStrIndex][1] < 0:
                            sdk0List.append(angleList[0])
                    else:
                        sdk0List.append(angleList[0])

                sdk1Angle = (sdk0List[0] + sdk0List[1]) / 2.0
                util.remapSDK(attrName, dv=sdk1Angle, v=1, cd='{0}.ocr'.format(angleCNode))
                util.remapSDK(attrName, dv=sdk0List[0], v=0, cd='{0}.ocr'.format(angleCNode))
                util.remapSDK(attrName, dv=sdk0List[1], v=0, cd='{0}.ocr'.format(angleCNode))

                # multipy angle
                intputAttr = cmds.listConnections(attrName, d=False, p=True)
                util.multiplyCombine(intputAttr[0], inputUnitConversion, attrName)

        # tag
        attributes.createAttribute(
            parentHandle, 'tag', attributeType="string", channelBox=False, nonKeyable=True, defaultValue='poseDriver'
        )
        attributes.createAttribute(
            parentHandle, 'axis', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=axis
        )
        attributes.createAttribute(
            parentHandle, 'follow', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=followHandle
        )
        attributes.createAttribute(
            parentHandle, 'parent', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=parentHandle
        )
        attributes.createAttribute(
            parentHandle, 'joint', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=name
        )
        attributes.createAttribute(
            parentHandle, 'parent_joint', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=parent
        )
        attributes.createAttribute(
            parentHandle, 'side', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=side
        )
        attributes.createAttribute(
            parentHandle, 'scale_value', attributeType="string", channelBox=False, nonKeyable=True, defaultValue=scale
        )

        util.scaleBridge(name, scale)
        if parent:
            util.constraintBridge(parentObj=parent, followObj=name, parentHandle=parentHandle, followHandle=followHandle)

        node = cls(parentHandle)

        if renameAttr:
            orgDriverAttrsDict = {'inner': 'R_side', 'outer': 'L_side',
                                  'outerFront': 'L_side_Front', 'outerBack': 'L_side_Back',
                                  'innerFront': 'R_side_Front', 'innerBack': 'R_side_Back'}
            for key in orgDriverAttrsDict.keys():
                try:
                    cmds.renameAttr(node.cmd_node + '.' + key, orgDriverAttrsDict[key])
                except:
                    pass

        return node

    @classmethod
    def create_from_data(cls, data):
        """
        Creates RBF network from dictionary

        >>> new_joint = cmds.createNode('joint')
        >>> data = {'drivers': [new_joint], 'poses': {'drivers': {'default': [[1,0,0,0,0,1,0,0,0,0,1,0,2,0,0,1]]}}}
        >>> RBFNode.create_from_data(data)
        """

        if not cmds.objExists(data['solver_name']):
            rbf_node = cls.create(name=data['solver_name'])
        else:
            rbf_node = cls(data['solver_name'])

        # add drivers
        drivers = data['drivers']
        for driver in drivers:
            if not rbf_node.has_driver(driver):
                rbf_node.add_driver(driver)

        # add controllers
        controllers = data.get('controllers', [])
        for controller in controllers:
            if not rbf_node.has_controller(controller):
                rbf_node.add_controller(controller)

        driven_transforms = data.get('driven_transforms', [])
        if driven_transforms:
            rbf_node.add_driven_transforms(driven_nodes=driven_transforms, edit=False)

        # add poses
        for pose_name, pose_data in data['poses'].items():
            drivers_matrices = pose_data['drivers']
            controllers_matrices = pose_data.get('controllers', [])
            driven_matrices = pose_data.get('driven', {})
            function_type = pose_data.get('function_type', 'DefaultFunctionType')
            distance_method = pose_data.get('distance_method', 'DefaultMethod')
            scale_factor = pose_data.get('scale_factor', 1.0)
            target_enable = pose_data.get('target_enable', True)

            rbf_node.add_pose(
                pose_name, drivers=drivers, matrices=drivers_matrices, driven_matrices=driven_matrices,
                controller_matrices=controllers_matrices, function_type=function_type,
                distance_method=distance_method, scale_factor=scale_factor, target_enable=target_enable
            )

        # set solver attributes
        attributes = ['radius', 'automaticRadius', 'weightThreshold']
        enum_attributes = ['mode', 'distanceMethod', 'normalizeMethod',
                           'functionType', 'twistAxis', 'inputMode']

        for attr in attributes:
            if attr in data:
                cmds.setAttr('{}.{}'.format(rbf_node, attr), data[attr])

        for attr in enum_attributes:
            if attr in data:
                value = data[attr]
                attr = "{node}.{attr}".format(node=rbf_node, attr=attr)
                rbf_node._set_enum_attribute(attr, value)

        return rbf_node

    @classmethod
    def find_all(cls):
        """
        Returns all RBF nodes in scene
        """
        return [cls(node) for node in [node for node in cmds.ls(type='transform') if cmds.objExists(node+'.tag') if cmds.getAttr(node+'.tag') == 'poseDriver' ]]

    @property
    def driver_joint(self):
        joint = cmds.getAttr("{}.joint".format(str(self)))
        return joint

    @property
    def parent_joint(self):
        parent_joint = cmds.getAttr("{}.parent_joint".format(str(self)))
        return parent_joint

    @property
    def axis(self):
        axis = cmds.getAttr("{}.axis".format(str(self)))
        return axis

    @property
    def side(self):
        side = cmds.getAttr("{}.side".format(str(self)))
        return side

    @property
    def scale(self):
        scale = cmds.getAttr("{}.scale_value".format(str(self)))
        return scale

    def data(self):
        """
        Returns dictionary with the setup
        """
        data = OrderedDict()
        data['solver_name'] = str(self)
        data['drivers'] = self.drivers()
        data['controllers'] = self.controllers()
        data['poses'] = self.poses()
        data['driven_attrs'] = self.driven_attributes()
        data['mode'] = self.mode(enum_value=True)
        data['radius'] = self.radius()
        data['automaticRadius'] = self.automatic_radius()
        data['weightThreshold'] = self.weight_threshold()
        data['distanceMethod'] = self.distance_method(enum_value=True)
        data['normalizeMethod'] = self.normalize_method(enum_value=True)
        data['functionType'] = self.function_type(enum_value=True)
        data['twistAxis'] = self.twist_axis(enum_value=True)
        data['inputMode'] = self.input_mode(enum_value=True)

        return data

    def export_data(self, file_path):
        """
        Exports data dictionary to disk
        """
        with open(file_path, 'w') as outfile:
            json.dump(self.data(), outfile, sort_keys=1, indent=4, separators=(",", ":"))

        return file_path

    def delete(self):
        """
        Delete the Maya node associated with this class
        """
        # If we have blendshapes, disconnect them all
        if self.driven_nodes(type='blendShape'):
            for pose in self.poses().keys():
                self.delete_blendshape(pose)

        cmds.delete(self._node)

