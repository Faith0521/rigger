# coding=utf-8
import pymel.core as pm


class niceKeyFrame:

    def __init__(self):
        # gui
        self.window_name = 'niceKey_window'
        self.window_title = 'niceKey_1.0'

    # 创建界面
    def gui(self):
        try:
            pm.deleteUI(self.window_name)
        except:
            pass

        pm.window(self.window_name, title=self.window_title, wh=(290, 258), s=False)
        pm.columnLayout('KeyFarmeCL', adj=1)

        pm.gridLayout(nc=6, cellWidthHeight=(48, 48), p='KeyFarmeCL')
        pm.button(l=u'20', c=lambda x:self.kframe(20))
        pm.button(l=u'30', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(30))
        pm.button(l=u'45', c=lambda x:self.kframe(45))
        pm.button(l=u'50', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(50))
        pm.button(l=u'60', c=lambda x:self.kframe(60))
        pm.button(l=u'90', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(90))

        pm.button(l=u'100', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(100))
        pm.button(l=u'110', c=lambda x:self.kframe(110))
        pm.button(l=u'120', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(120))
        pm.button(l=u'130', c=lambda x:self.kframe(130))
        pm.button(l=u'135', bgc=(0.2, 0.5, 0.6), c=lambda x:self.kframe(135))
        pm.button(l=u'150', c=lambda x:self.kframe(150))
        pm.setParent('..')

        pm.separator(h=10)

        pm.rowLayout(p='KeyFarmeCL', nc=6, adj=6)
        pm.text(l=u'轴向:')
        pm.radioCollection('rotate')
        pm.radioButton('pass', l='Pass', sl=1)
        pm.radioButton('rotateX', l='Rotate_X')
        pm.radioButton('rotateY', l='Rotate_Y')
        pm.radioButton('rotateZ', l='Rotate_Z')
        pm.setParent('..')

        pm.separator(h=10)

        pm.rowLayout(p='KeyFarmeCL', nc=6, adj=6)
        pm.text(l=u'正负:')
        pm.radioCollection('PosNega')
        pm.radioButton('pass', l='Pass', sl=1)
        pm.radioButton('positive', l=u'正方向')
        pm.radioButton('negative', l=u'负方向')
        pm.radioButton('PosandNeg', l=u'正and负')
        pm.setParent('..')

        pm.separator(h=10)

        pm.button(l=u'删除K帧并归零', w=40, h=40, c=lambda x:self.deframe())
        pm.separator(h=10)
        pm.button(l=u'斜方向控制器', w=40, h=40, c=lambda x:self.oblique())
        pm.setParent('..')

        pm.showWindow()

    # function
    def kframe(self, integer):

        sel = pm.selected()[0]
        xyz = ['rotateX', 'rotateY', 'rotateZ']

        radio_a = pm.radioCollection('rotate', query=True, select=True)
        radio_b = pm.radioCollection('PosNega', query=True, select=True)
        if pm.radioCollection('rotate', query=True, select=True) == 'pass':
            if pm.getAttr('%s.rotateX' % sel) == 0 and pm.getAttr('%s.rotateY' % sel) == 0 and pm.getAttr('%s.rotateZ' % sel) == 0:

                pm.warning(u'如果旋转XYZ为零，请选择轴向和正负')
            else:
                for rt in xyz:
                    if pm.getAttr('%s.%s' % (sel, rt)) > 0:
                        self.deframe()
                        pm.setKeyframe(v=0, time=0, at=rt, itt='linear', ott='linear')
                        pm.setKeyframe(v=integer, time=integer, at=rt, itt='linear', ott='linear')
                        pm.playbackOptions(min=0, max=integer)
                    elif pm.getAttr('%s.%s' % (sel, rt)) < 0:
                        self.deframe()
                        pm.setKeyframe(v=0, time=0, at=rt, itt='linear', ott='linear')
                        pm.setKeyframe(v=integer * -1, time=integer * 1, at=rt, itt='linear', ott='linear')
                        pm.playbackOptions(min=0, max=integer)

        elif pm.radioCollection('rotate', query=True, select=True):
            if pm.radioButton('positive', query=True, select=True):
                self.deframe()
                pm.setKeyframe(v=0, time=0, at=radio_a, itt='linear', ott='linear')
                pm.setKeyframe(v=integer, time=integer, at=radio_a, itt='linear', ott='linear')
                pm.playbackOptions(min=0, max=integer)

            elif pm.radioButton('negative', query=True, select=True):
                self.deframe()
                pm.setKeyframe(v=0, time=0, at=radio_a, itt='linear', ott='linear')
                pm.setKeyframe(v=integer * -1, time=integer * 1, at=radio_a, itt='linear', ott='linear')
                pm.playbackOptions(min=0, max=integer)

            elif pm.radioButton('PosandNeg', query=True, select=True):
                self.deframe()
                pm.setKeyframe(v=integer * -1, time=integer * -1, at=radio_a, itt='linear', ott='linear')
                pm.setKeyframe(v=0, time=0, at=radio_a, itt='linear', ott='linear')
                pm.setKeyframe(v=integer, time=integer, at=radio_a, itt='linear', ott='linear')
                pm.playbackOptions(min=integer * -1, max=integer)

    # 删除K帧并归零
    def deframe(self):
        pm.currentTime(0)
        pm.cutKey(time=(-200, 200), clear=True)
        pm.playbackOptions(min=0, max=120)

    # 创建斜方向控制器
    def oblique(self):
        ctl = pm.selected()[0]
        loc = pm.spaceLocator(n=ctl + '_Locator')
        loc_1x_grp = pm.group(loc, n=loc + '_1x_Grp')
        loc_grp = pm.group(loc_1x_grp, n=loc + '_Grp')

        pm.setAttr(loc + 'Shape.localScaleX', 16)
        pm.setAttr(loc + 'Shape.localScaleY', 16)
        pm.setAttr(loc + 'Shape.localScaleZ', 16)

        pm.delete(pm.parentConstraint(ctl, loc_grp, w=1))
        pm.setAttr(loc_1x_grp + '.rotateX', 45)
        pm.orientConstraint(loc, ctl, mo=1, w=1)

        pm.select(loc)
