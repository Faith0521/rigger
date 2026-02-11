from cgrig.libs.hive import api
from cgrig.libs.maya.utils import mayatestutils


class TestHiveBatchComponent(mayatestutils.BaseMayaTest):
    keepPluginsLoaded = True
    newSceneAfterTearDownCls = True
    newSceneAfterTest = True
    componentType = "fkchain"
    _componentName = "test{}"
    _componentSide = "L"
    _rigName = "unittestRig"

    @classmethod
    def setUpClass(cls):
        super(TestHiveBatchComponent, cls).setUpClass()

    def setUp(self):
        cfg = api.Configuration()
        cfg.blackBox = True
        self.rig = api.Rig(cfg)
        self.rig.startSession(self._rigName)
        self.component = self.rig.createComponent(self.componentType, self._componentName.format(self.componentType),
                                                  self._componentSide)

    def test_buildGuide(self):
        self.rig.buildGuides([self.component])
        self.assertTrue(self.component.hasGuide())
        self.assertFalse(self.component.hasRig())
        self.assertIsInstance(self.component.guideLayer(), api.HiveGuideLayer)
        self.assertIsInstance(self.component.container(), api.ContainerAsset)
        self.assertEqual(
            self.component.container().blackBox, self.rig.configuration.blackBox
        )

    def test_buildRigWithGuide(self):
        self.rig.buildGuides([self.component])
        self.assertFalse(self.component.hasRig())
        self.rig.buildRigs([self.component])
        self.assertIsInstance(self.component.rigLayer(), api.HiveRigLayer)
        self.assertIsInstance(self.component.inputLayer(), api.HiveInputLayer)
        self.assertIsInstance(self.component.outputLayer(), api.HiveOutputLayer)
        self.assertIsInstance(self.component.deformLayer(), api.HiveDeformLayer)
        self.assertTrue(self.component.hasRig())

    def test_parent(self):
        newComponent = self.rig.createComponent("fkchain", "testcomp", "M")
        self.rig.buildGuides([self.component, newComponent])
        self.assertIsNone(self.component.parent())
        self.component.setParent(newComponent)
        self.assertIsNotNone(self.component.parent())
        self.assertIsInstance(self.component.parent(), api.Component)

    def test_duplicate(self):
        self.rig.buildGuides([self.component])
        newComp = self.component.duplicate("newComponent", "R")
        self.assertEqual(newComp.name(), "newComponent")
        self.assertEqual(newComp.side(), "R")
        self.assertTrue(newComp.exists())
        self.assertIsInstance(newComp, api.Component)

    def test_deserialize(self):
        self.rig.buildGuides([self.component])
        deff = self.component.serializeFromScene()
        self.rig.deleteComponent(self.component.name(), self.component.side())
        self.rig.createComponent(definition=deff)

    def test_deleteGuide(self):
        self.rig.buildGuides([self.component])
        self.assertTrue(self.component.deleteGuide())
        self.assertIsNone(self.component.guideLayer())

    def test_deleteRig(self):
        self.rig.buildGuides([self.component])
        self.rig.buildRigs([self.component])
        self.assertTrue(self.rig.deleteRigs())
        for i in (self.component.rigLayer(),):
            self.assertIsNone(i)

    def test_delete(self):
        self.rig.buildGuides([self.component])
        self.rig.buildRigs([self.component])
        self.rig.deleteComponent(self.component.name(), self.component.side())
        self.component.rootTransform()
        self.assertFalse(self.component.exists())

    def test_polish(self):
        self.rig.buildGuides([self.component])
        self.rig.buildRigs([self.component])
        self.rig.polish()
        self.assertIsNone(self.component.guideLayer())
        self.assertIsNone(self.component.container())

    def test_polishWithContainers(self):
        self.rig.configuration.useContainers = True
        self.rig.buildGuides([self.component])
        self.rig.buildRigs([self.component])
        self.rig.polish()
        self.assertIsNone(self.component.guideLayer())
        self.assertIsNotNone(self.component.container())
        self.assertTrue(
            self.component.container().blackBox, self.rig.configuration.blackBox
        )


    def test_animSettings(self):
        """Tests whether the rig build matches the definition from the guides update"""
        self.rig.buildGuides([self.component])
        self.rig.polish()
        _testAnimSettingsForComponent(self, self.rig, self.component)


def _testTwistsCountForComponent(test, comp, twistSettingNames, twistSegmentIdPrefix):
    countSettings = comp.definition.guideLayer.guideSettings(*twistSettingNames)
    twists = {}
    guides = {guide.id(): guide for guide in comp.guideLayer().iterGuides()}
    for settingName, segmentPrefix in zip(twistSettingNames, twistSegmentIdPrefix):
        for guideId, guide in guides.items():
            if guideId.startswith(segmentPrefix) and "TwistOffset" not in guideId:
                twists.setdefault(settingName, []).append(guide)
    for settingName, segmentGuides in twists.items():
        count = countSettings[settingName].value
        test.assertTrue(
            count == len(segmentGuides),
            "UprTwists do not match settings: Scene Count: {}, setting: {}".format(
                len(segmentGuides), count
            ),
        )


def _testAnimSettingsForComponent(test, rig, comp):
    rigLayer = comp.rigLayer()
    animSettings = comp.definition.rigLayer.settings.get(
        api.constants.CONTROL_PANEL_TYPE, []
    )
    if not animSettings:
        return
    controlPanel = rigLayer.settingNode(api.constants.CONTROL_PANEL_TYPE)
    if controlPanel is None:
        return
    controls = rigLayer.iterControls()
    for animSetting in animSettings:
        # make sure the settings exist
        # todo: check value, default, min/max etc
        test.assertTrue(controlPanel.hasAttribute(animSetting["name"]))
        if rig.configuration.useProxyAttributes:
            for ctrl in controls:
                test.assertTrue(ctrl.hasAttribute(animSetting["name"]))
        elif (
                not rig.configuration.useProxyAttributes
                and rig.configuration.useContainers
        ):
            container = comp.container()
            publishNames = [
                i.partialName(
                    includeNonMandatoryIndices=True,
                    useLongNames=False,
                    includeInstancedIndices=True,
                )
                for i in container.publishedAttributes()
            ]
            test.assertTrue(animSetting["name"] in publishNames)

class TestHiveFkComponent(mayatestutils.BaseMayaTest):
    keepPluginsLoaded = True
    newSceneAfterTearDownCls = True
    newSceneAfterTest = True
    componentType = "fkchain"
    _componentName = "test{}"
    _componentSide = "L"
    _rigName = "unittestRig"

    @classmethod
    def setUpClass(cls):
        super(TestHiveFkComponent, cls).setUpClass()

    def setUp(self):
        cfg = api.Configuration()
        cfg.blackBox = True
        self.rig = api.Rig(cfg)
        self.rig.startSession(self._rigName)
        self.component = self.rig.createComponent(self.componentType, self._componentName.format(self.componentType),
                                                  self._componentSide)

    def test_fkDeleteGuide(self):
        self.rig.buildGuides([self.component])
        layer = self.component.guideLayer()
        guideToDelete = layer.guide("fk02")
        api.commands.deleteFkGuide({self.component: [guideToDelete]})
        self.assertIsNone(layer.guide("fk02"))

    def test_fkParentGuide(self):
        self.rig.buildGuides([self.component])
        layer = self.component.guideLayer()
        childGuides = layer.guide("fk02")
        api.commands.setFkGuideParent(layer.guide("fk00"), [childGuides])
        self.assertTrue(childGuides.guideParent(), layer.guide("fk00"))

class TestArmComponent(TestHiveBatchComponent):
    componentType = "armcomponent"

    def test_buildWithTwist(self):
        self.rig.buildGuides([self.component])
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist"],
        )
        api.commands.updateGuideSettings(
            self.component, {"uprSegmentCount": 4, "lwrSegmentCount": 3}
        )
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist"],
        )
        self.rig.buildDeform([self.component])
        self.rig.buildRigs([self.component])
        self.rig.polish()


class TestLegComponent(TestHiveBatchComponent):
    componentType = "legcomponent"

    def test_build(self):
        self.rig.buildGuides([self.component])
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist"],
        )
        api.commands.updateGuideSettings(
            self.component, {"uprSegmentCount": 4, "lwrSegmentCount": 3}
        )
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist"],
        )
        self.rig.buildDeform([self.component])
        self.rig.buildRigs([self.component])
        self.rig.polish()


class TestQuadComponent(TestHiveBatchComponent):
    componentType = "quadLeg"

    def test_build(self):
        self.rig.buildGuides([self.component])
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount", "ankleSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist", "ankleTwist"],
        )
        # self._testTwistCounts(comp)
        api.commands.updateGuideSettings(
            self.component, {"uprSegmentCount": 4, "lwrSegmentCount": 3, "ankleSegmentCount": 3}
        )
        # self._testTwistCounts(comp)
        _testTwistsCountForComponent(
            self,
            self.component,
            ["uprSegmentCount", "lwrSegmentCount", "ankleSegmentCount"],
            twistSegmentIdPrefix=["uprTwist", "lwrTwist", "ankleTwist"],
        )
        self.rig.buildDeform([self.component])
        self.rig.buildRigs([self.component])
        self.rig.polish()


class TestFingerComponent(TestHiveBatchComponent):
    componentType = "finger"


class TestVChainComponent(TestHiveBatchComponent):
    componentType = 'vchaincomponent'


class TestGodNodeComponent(TestHiveBatchComponent):
    componentType = "godnodecomponent"


class TestHeadComponent(TestHiveBatchComponent):
    componentType = "headcomponent"


class TestJawComponent(TestHiveBatchComponent):
    componentType = "jaw"


class TestSplineIkComponent(TestHiveBatchComponent):
    componentType = "spineIk"


class TestSpineFkComponent(TestHiveBatchComponent):
    componentType = "spineFk"


class TestAimComponent(TestHiveBatchComponent):
    componentType = "aimcomponent"


class TestCheekComponent(TestHiveBatchComponent):
    componentType = "cheekcomponent"


# todo: 'browcomponent', 'eyecomponent', 'mouthcomponent'
class TestUserComponents(mayatestutils.BaseMayaTest):
    newSceneAfterTest = True
    newSceneAfterTearDownCls = True
    keepPluginsLoaded = True
    # ignore because these are manually tested
    ignoredComponents = ('armcomponent', 'finger', 'browcomponent', 'cheekcomponent', 'eyecomponent',
                         'headcomponent', 'jaw', 'quadLeg', 'spineFk', 'spineIk', 'mouthcomponent',
                         'aimcomponent', 'fkchain', 'godnodecomponent', 'vchaincomponent', 'legcomponent',
                         )

    def setUp(self):
        self.rig = api.Rig()
        self.rig.startSession("hiveTest")
        comps = self.rig.configuration.componentRegistry().components
        for n, data in comps.items():
            if n in self.ignoredComponents:
                continue
            self.rig.createComponent(n, n, "M")

    def test_buildAllComponentGuides(self):
        comps = self.rig.components()
        if not comps:
            return
        self.rig.buildGuides()
        for comp in comps:
            self.assertIsInstance(comp.meta, api.HiveComponent)
            self.assertIsInstance(comp.guideLayer(), api.HiveGuideLayer)

    def test_buildAllComponentRigs(self):
        comps = self.rig.components()
        if not comps:
            return
        self.rig.buildGuides()
        self.rig.buildDeform()
        self.rig.buildRigs()
        self.rig.polish()
        for comp in comps:
            _testAnimSettingsForComponent(self, self.rig, comp)
