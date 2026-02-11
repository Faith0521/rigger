# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: rosa.w
# Mail: wrx1844@qq.com
# Python.3.7
#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

from importlib import reload
import maya.cmds as mc


class jntHelper(object):

    def __init__(self):
        pass

    def matrixParent(self, driver, driven):
        driven_mm = '{0}_mm'.format(driven)
        driven_dm = '{0}_dm'.format(driven)
        driven_qp = '{0}_qp'.format(driven)
        driven_qe = '{0}_qe'.format(driven)

        # create node
        if not mc.objExists(driven_mm):
            mc.createNode('multMatrix', n=driven_mm)
        if not mc.objExists(driven_dm):
            mc.createNode('multMatrix', n=driven_dm)
        if not mc.objExists(driven_qp):
            mc.createNode('multMatrix', n=driven_qp)
        if not mc.objExists(driven_qe):
            mc.createNode('multMatrix', n=driven_qe)

        # connect
        mc.connectAttr('{0}.matrixSum'.format(driven_mm), '{0}.inputMatrix'.format(driven_dm))
        mc.connectAttr('{0}.outputQuat'.format(driven_dm), '{0}.input1Quat'.format(driven_qp))
        mc.connectAttr('{0}.outputQuat'.format(driven_qp), '{0}.inputQuat'.format(driven_qe))
        mc.connectAttr('{0}.rotateOrder'.format(driven), '{0}.inputRotateOrder'.format(driven_qe))

        mc.connectAttr('{0}.worldMatrix[0]'.format(driver), '{0}.matrixIn[0]'.format(driven_mm))
        mc.connectAttr('{0}.parentInverseMatrix[0]'.format(driven), '{0}.matrixIn[1]'.format(driven_mm))
        mc.connectAttr('{0}.outputTranslate'.format(driven_dm), '{0}.translate'.format(driven))
        mc.connectAttr('{0}.outputRotate'.format(driven_qe), '{0}.rotate'.format(driven))
        mc.connectAttr('{0}.outputScale'.format(driven_dm), '{0}.scale'.format(driven))

        # container
        driven_ct = '{0}_ct'.format(driven)
        if not mc.objExists(driven_ct):
            mc.createNode('container', n=driven_ct)
        mc.container(driven_ct, an=[driven_mm, driven_dm, driven_qp, driven_qe])


    def matrixHalfRoll(self, driver, driverP, halfObj):
        driverP_mm = '{0}_mm'.format(driverP)
        driverP_dm = '{0}_dm'.format(driverP)
        driverP_qp = '{0}_qp'.format(driverP)
        driverP_qe = '{0}_qe'.format(driverP)

        # create node
        if not mc.objExists(driverP_mm):
            mc.createNode('multMatrix', n=driverP_mm)
        if not mc.objExists(driverP_dm):
            mc.createNode('multMatrix', n=driverP_dm)
        if not mc.objExists(driverP_qp):
            mc.createNode('multMatrix', n=driverP_qp)
        if not mc.objExists(driverP_qe):
            mc.createNode('multMatrix', n=driverP_qe)

        # connect
        mc.connectAttr('{0}.matrixSum'.format(driverP_mm), '{0}.inputMatrix'.format(driverP_dm))
        mc.connectAttr('{0}.outputQuat'.format(driverP_dm), '{0}.input1Quat'.format(driverP_qp))
        mc.connectAttr('{0}.outputQuat'.format(driverP_qp), '{0}.inputQuat'.format(driverP_qe))
        mc.connectAttr('{0}.outputRotate'.format(driverP_qe), '{0}.rotate'.format(driverP))

