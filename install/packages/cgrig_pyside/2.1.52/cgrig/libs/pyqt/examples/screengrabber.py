# -*- coding: utf-8 -*-
from cgrig.libs.pyqt.widgets import screengrabber
from cgrig.libs.pyqt import utils


if __name__ == "__main__":
    win = screengrabber.ScreenGrabDialog()
    win.exec_()
    print(utils.desktopPixmapFromRect(win.thumbnailRect, win))