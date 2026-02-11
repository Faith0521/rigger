# -*- coding: utf-8 -*-

def startup(package):
    from cgrig.libs.pyqt import stylesheet
    from cgrigvendor.Qt import QtWidgets
    if QtWidgets.QApplication.instance() is not None:
        stylesheet.loadDefaultFonts()


def shutdown(package):
    from cgrig.libs.pyqt import stylesheet
    from cgrigvendor.Qt import QtWidgets
    if QtWidgets.QApplication.instance() is not None:
        stylesheet.unloadFonts()
