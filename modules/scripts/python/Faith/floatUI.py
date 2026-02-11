# -*- coding: utf-8 -*-
from imp import reload
# from Faith.vendor.Qt import QtCore, QtWidgets, QtGui
from PySide2 import QtCore, QtGui, QtWidgets
from functools import partial
from Faith.maya_utils import ui_utils, rigging_utils
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from Faith import ScriptPath
from Faith.tools.small_tools import small_tool
from maya import cmds
import json, getpass, os, sys, copy, random

reload(ui_utils)
reload(rigging_utils)

icon_path = ui_utils.icon_path
icon_json_file = ScriptPath + "/iconSettings.json"

iconInfoList = []

with open(icon_json_file, 'r') as f:
    iconInfoList = json.load(f)
Icon_config = iconInfoList[0]
ToolIcon_config = iconInfoList[1]
MenuConfig = iconInfoList[2]


class Dockable2048UI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.uiName = "2048UI"
        super(Dockable2048UI, self).__init__(parent=parent)
        # self.gameForm = GameForm()
        self.setObjectName(self.uiName)

        self.initUi()
        # 定义各数字的背景颜色
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
                       8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                       64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 207, 114),
                       512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114),
                       32768: (237, 207, 114), 65536: (237, 207, 114), 131072: (237, 207, 114),
                       262144: (237, 207, 114), 524288: (237, 207, 114), 1048576: (237, 207, 114)}
        self.initGameData()

    def initUi(self):
        self.setWindowTitle("2048")
        self.resize(505, 720)
        self.setFixedSize(self.width(), self.height())
        self.initGameOpt()

    def initGameOpt(self):
        """ 初始化游戏配置 """
        self.lbFont = QtGui.QFont('SimSun', 12)  # label字体
        self.lgFont = QtGui.QFont('SimSun', 50)  # Logo字体
        self.nmFont = QtGui.QFont('SimSun', 36)  # 面板数字字体

    def initGameData(self):
        """ 初始化游戏数字 """
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1

        self.curScore = 0
        self.bstScore = 0
        # 载入最高得分
        if os.path.exists("bestscore.ini"):
            with open("bestscore.ini", "r") as f:
                self.bstScore = int(f.read())

    def paintEvent(self, e):
        ''' 重写绘图事件 '''
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGameGraph(qp)
        qp.end()

    def keyPressEvent(self, e):
        keyCode = e.key()
        ret = False
        if keyCode == QtCore.Qt.Key_Left:
            ret = self.move("Left")
        elif keyCode == QtCore.Qt.Key_Right:
            ret = self.move("Right")
        elif keyCode == QtCore.Qt.Key_Up:
            ret = self.move("Up")
        elif keyCode == QtCore.Qt.Key_Down:
            ret = self.move("Down")
        else:
            pass

        if ret:
            self.repaint()

    def closeEvent(self, e):
        # 保存最高得分
        with open("bestscore.ini", "w") as f:
            f.write(str(self.bstScore))

    def drawGameGraph(self, qp):
        """ 绘制游戏图形 """
        self.drawLog(qp)
        self.drawLabel(qp)
        self.drawScore(qp)
        self.drawBg(qp)
        self.drawTiles(qp)

    def drawScore(self, qp):
        """ 绘制得分 """
        qp.setFont(self.lbFont)
        fontsize = self.lbFont.pointSize()
        scoreLabelSize = len(u"SCORE") * fontsize
        bestLabelSize = len(u"BEST") * fontsize
        curScoreBoardMinW = 15 * 2 + scoreLabelSize  # SCORE栏的最小宽度
        bstScoreBoardMinW = 15 * 2 + bestLabelSize  # BEST栏的最小宽度
        curScoreSize = len(str(self.curScore)) * fontsize
        bstScoreSize = len(str(self.bstScore)) * fontsize
        curScoreBoardNedW = 10 + curScoreSize
        bstScoreBoardNedW = 10 + bstScoreSize
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)
        bstScoreBoardW = max(bstScoreBoardMinW, bstScoreBoardNedW)
        qp.setBrush(QtGui.QColor(187, 173, 160))
        qp.setPen(QtGui.QColor(187, 173, 160))
        qp.drawRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 50)
        qp.drawRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 50)

        bstLabelRect = QtCore.QRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 25)
        bstScoreRect = QtCore.QRect(505 - 15 - bstScoreBoardW, 65, bstScoreBoardW, 25)
        scoerLabelRect = QtCore.QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 25)
        curScoreRect = QtCore.QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 65, curScoreBoardW, 25)

        qp.setPen(QtGui.QColor(238, 228, 218))
        qp.drawText(bstLabelRect, QtCore.Qt.AlignCenter, u"BEST")
        qp.drawText(scoerLabelRect, QtCore.Qt.AlignCenter, u"SCORE")

        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.drawText(bstScoreRect, QtCore.Qt.AlignCenter, str(self.bstScore))
        qp.drawText(curScoreRect, QtCore.Qt.AlignCenter, str(self.curScore))

    def drawBg(self, qp):
        """ 绘制背景图 """
        col = QtGui.QColor(187, 173, 160)
        qp.setPen(col)

        qp.setBrush(QtGui.QColor(187, 173, 160))
        qp.drawRect(15, 150, 475, 475)  # 绘制游戏区域

    def drawLog(self, qp):
        """ 绘制Logo """
        pen = QtGui.QPen(QtGui.QColor(255, 93, 29), 15)
        qp.setFont(self.lgFont)
        qp.setPen(pen)
        qp.drawText(QtCore.QRect(10, 0, 150, 130), QtCore.Qt.AlignCenter, "2048")

    def drawLabel(self, qp):
        """ 绘制所有标签信息 """
        qp.setFont(self.lbFont)
        qp.setPen(QtGui.QColor(119, 110, 101))
        qp.drawText(15, 134, u"合并相同数字，得到2048吧!")
        qp.drawText(15, 660, u"怎么玩:")
        qp.drawText(45, 680, u"用-> <- 上下左右箭头按键来移动方块.")
        qp.drawText(45, 700, u"当两个相同数字的方块碰到一起时，会合成一个!")

    def drawTiles(self, qp):
        """ 绘制数字背景 """
        qp.setFont(self.nmFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]

                qp.setPen(QtGui.QColor(*color))
                qp.setBrush(QtGui.QColor(*color))
                qp.drawRect(30 + col * 115, 165 + row * 115, 100, 100)  # 绘制数字的背景小方块
                size = self.nmFont.pointSize() * len(str(value))  # 获取当前字体下显示数字的长度
                # 根据尺寸调整字体大小
                while size > 100 - 15 * 2:
                    self.nmFont = QtGui.QFont('SimSun', self.nmFont.pointSize() * 4 // 5)
                    qp.setFont(self.nmFont)
                    size = self.nmFont.pointSize() * len(str(value))  # 获取当前字体下显示数字的长度
                print("[%d][%d]: value[%d] weight: %d" % (row, col, value, size))

                # 显示非0数字
                if value == 2 or value == 4:
                    qp.setPen(QtGui.QColor(119, 110, 101))  # 设置2和4数字的前景色
                else:
                    qp.setPen(QtGui.QColor(255, 255, 255))  # 设置其他数字的前景色
                if value != 0:
                    rect = QtCore.QRect(30 + col * 115, 165 + row * 115, 100, 100)
                    qp.drawText(rect, QtCore.Qt.AlignCenter, str(value))

    def putTile(self):
        """ 找到一个空位置（数值为0），并随机填充2或4 """
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:
                    available.append((row, col))
        if available:
            row, col = available[random.randint(0, len(available) - 1)]
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            return True
        return False

    def merge(self, row):
        """ 合并一行或一列 """
        pair = False
        newRow = []
        for i in range(len(row)):
            if pair:
                newRow.append(2 * row[i])
                self.curScore += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                else:
                    newRow.append(row[i])
        return newRow

    def slideUpDown(self, isUp):
        """ 上下方向移动数字方格 """
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            cvl = []
            for row in range(numRows):
                if self.data[row][col] != 0:
                    cvl.append(self.data[row][col])  # 将列里面的非0元素提取出来

            if len(cvl) >= 2:
                cvl = self.merge(cvl)  # 合并相同数字

            # 根据移动方向填充0
            for i in range(numRows - len(cvl)):
                if isUp:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)

            print("row=%d" % row)
            row = 0
            for row in range(numRows):
                self.data[row][col] = cvl[row]

        return oldData != self.data  # 返回数据是否发生了变化

    def slideLeftRight(self, isLeft):
        """ 左右方向移动数字方格 """
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = []
            for col in range(numCols):
                if self.data[row][col] != 0:
                    rvl.append(self.data[row][col])

            if len(rvl) >= 2:
                rvl = self.merge(rvl)

            for i in range(numCols - len(rvl)):
                if isLeft:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)

            col = 0
            for col in range(numCols):
                self.data[row][col] = rvl[col]

        return oldData != self.data

    def move(self, direction):
        """ 移动数字方格 """
        isMove = False
        if direction == "Up":
            isMove = self.slideUpDown(True)
        elif direction == "Down":
            isMove = self.slideUpDown(False)
        elif direction == "Left":
            isMove = self.slideLeftRight(True)
        elif direction == "Right":
            isMove = self.slideLeftRight(False)
        else:
            pass

        if not isMove:
            return False

        self.putTile()  # 新增一个数字
        if self.curScore > self.bstScore:
            self.bstScore = self.curScore

        if self.isGameOver():
            button = QtWidgets.QMessageBox.warning(self, "Warning", u"游戏结束，是否重新开始？",
                                                   QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.Ok)

            if button == QtWidgets.QMessageBox.Ok:
                self.initGameOpt()
                bstScore = self.bstScore
                self.initGameData()
                self.bstScore = bstScore
                return True
            else:
                return False
        else:
            return True

    def isGameOver(self):
        """ 判断游戏是否无法继续 """
        copyData = copy.deepcopy(self.data)  # 先暂存数据值
        curScore = self.curScore

        flag = False
        if not self.slideUpDown(True) and not self.slideUpDown(False) and not self.slideLeftRight(
                True) and not self.slideLeftRight(False):
            flag = True  # 全部方向都不能再移动
        self.curScore = curScore
        if not flag:
            self.data = copyData  # 仍可以移动，则恢复原来数据
        return flag


class BaseLabel(QtWidgets.QLabel):
    mouseDoubleClickSignal = QtCore.Signal(object)  # 自定义鼠标双击信号

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

    def mouseDoubleClickEvent(self, e):
        self.mouseDoubleClickSignal.emit(e)


class DockableScriptUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent=None):
        self.uiName = "scriptUI"
        self.userPath = r"R:\\TeamCode\\users\\"
        super(DockableScriptUI, self).__init__(parent=parent)
        self.setObjectName(self.uiName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Add Custom Script")
        self.resize(330, 300)

        self.setStyleSheet(ui_utils.qss)

        self.initWidget()
        self.createConnections()

    def initWidget(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setPlaceholderText(u"请输入脚本启动代码")
        self.mainLayout.addWidget(self.textEdit)

        self.nameHBox = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.nameHBox)
        self.nameLb = QtWidgets.QLabel("Script Name")
        self.nameLe = QtWidgets.QLineEdit()
        self.nameHBox.addWidget(self.nameLb)
        self.nameHBox.addWidget(self.nameLe)

        self.scriptPathHBox = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.scriptPathHBox)
        self.scriptPathLb = QtWidgets.QLabel("Script Path")
        self.scriptPathLe = QtWidgets.QLineEdit()
        self.scriptBtn = QtWidgets.QPushButton("...")
        self.scriptPathHBox.addWidget(self.scriptPathLb)
        self.scriptPathHBox.addWidget(self.scriptPathLe)
        self.scriptPathHBox.addWidget(self.scriptBtn)

        self.iconPathHBox = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.iconPathHBox)
        self.iconPathLb = QtWidgets.QLabel("Icon Path")
        self.iconPathLe = QtWidgets.QLineEdit()
        self.iconBtn = QtWidgets.QPushButton("...")
        self.iconPathHBox.addWidget(self.iconPathLb)
        self.iconPathHBox.addWidget(self.iconPathLe)
        self.iconPathHBox.addWidget(self.iconBtn)

        self.languageHBox = QtWidgets.QHBoxLayout()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.mainLayout.addLayout(self.languageHBox)
        self.languageLb = QtWidgets.QLabel("Language")
        self.languageLb.setSizePolicy(sizePolicy)
        self.languageHBox.addWidget(self.languageLb)

        self.radioMel = QtWidgets.QRadioButton("Mel")
        self.radioPy = QtWidgets.QRadioButton("Python")
        self.radioPy.setChecked(True)
        self.addBtn = QtWidgets.QPushButton("Add")
        self.radioPy.setSizePolicy(sizePolicy)
        self.radioMel.setSizePolicy(sizePolicy)
        self.languageHBox.addWidget(self.radioMel)
        self.languageHBox.addWidget(self.radioPy)
        self.languageHBox.addWidget(self.addBtn)

    def createConnections(self):
        self.addBtn.clicked.connect(self.addScript)
        self.scriptBtn.clicked.connect(partial(self.getDirecPath, self.scriptPathLe))
        self.iconBtn.clicked.connect(partial(self.getIcon, self.iconPathLe))

    def getIcon(self, lineEdit, *args):
        path, type = QtWidgets.QFileDialog.getOpenFileName(None, "Select File", "", "Png Files (*.png)")
        lineEdit.setText(path)

    def getDirecPath(self, lineEdit, *args):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory')
        lineEdit.setText(directory)

    def addScript(self, *args):
        startCode = self.textEdit.toPlainText()
        scriptName = self.nameLe.text()
        scriptPath = self.scriptPathLe.text()
        iconPath = self.iconPathLe.text()
        userName = getpass.getuser()

        addInfo = {
            "favorites": [],
            scriptName: {
                "path": scriptPath,
                "icon": iconPath,
                "command": startCode
            }
        }

        if os.path.exists(scriptPath):
            sys.path.append(scriptPath)

        jsonFile = self.userPath + userName + ".json"
        if not os.path.exists(jsonFile):
            with open(jsonFile, "w") as f:
                json.dump(addInfo, f, indent=4)
        else:
            with open(jsonFile, "r") as f:
                data = json.load(f)
            data.update(addInfo)

            with open(jsonFile, "w") as f:
                json.dump(data, f, indent=4)


class widget(QtWidgets.QWidget):
    def __init__(self, p=None):
        super(__class__, self).__init__(p)
        self.resize(350, 600)
        self.setMouseTracking(True)
        self.setStyleSheet("""QPushButton{text-align:left;}""")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)


class wnd(QtWidgets.QDialog):
    def __init__(self, p=None):
        super(__class__, self).__init__(p)

        self.firstClickedPos = None
        self.isClicked = None
        self.minOpacity = .5
        self.maxOpacity = 1
        self.isLocked = False  # 激活鼠标事件的开关属性
        self.coWidgets = {}
        self.favorites = []
        self.userSettings = {}

        # get userPath
        userPath = r"R:\\TeamCode\\users\\"
        userName = getpass.getuser()
        self.jsonFile = userPath + userName + ".json"
        self.opacity = self.minOpacity

        self.orgSize = QtCore.QSize(60, 60)
        self.scaledSize = QtCore.QSize(600, 60)
        self.setStyleSheet(ui_utils.qss)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowOpacity(self.opacity)
        self.resize(self.orgSize)

        self.updateCustomConfig()

        self.w = widget(self)
        self.initWidget()

        self.label.mouseDoubleClickSignal.connect(self.refreshType)

        self.closeBtn = QtWidgets.QPushButton('', self)
        self.closeBtn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path + "/SP_MessageBoxCritical.png")))
        self.closeBtn.resize(20, 20)
        self.closeBtn.move(575, 0)
        self.closeBtn.clicked.connect(self.close)

        self.opacityTimer = QtCore.QTimer()
        self.opacityTimer.timeout.connect(self.updateOpacity)

    def initWidget(self):
        self.lb_h = QtWidgets.QHBoxLayout()
        self.w.mainLayout.addLayout(self.lb_h)

        self.label = BaseLabel('')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(60, 60))

        self.pix = QtGui.QPixmap(icon_path + "/hemu.png")
        self.pix.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(self.pix)


        self.toolBtnHbox = QtWidgets.QHBoxLayout()
        self.toolBtnHbox.setContentsMargins(0,0,0,0)
        self.toolBtnHbox.setSpacing(1)
        # self.createToolBtn()

        for i in range(10):
            btn = QtWidgets.QPushButton()
            self.toolBtnHbox.addWidget(btn)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolBtnHbox.addItem(spacerItem)

        self.lb_h.addWidget(self.label)
        self.lb_h.addLayout(self.toolBtnHbox)

        spacerItem = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.w.mainLayout.addItem(spacerItem)


    def updateCustomConfig(self):
        outputDict = {"favorites": self.favorites}
        if not os.path.exists(self.jsonFile):
            with open(self.jsonFile, 'w') as f:
                json.dump(outputDict, f, indent=4)
        else:
            with open(self.jsonFile, 'r') as f:
                self.favorites = json.load(f)["favorites"]
                [Icon_config["Favorites"].update({btn: btnInfo}) for name, info in Icon_config.items() for btn, btnInfo
                 in info.items() for fa in self.favorites if fa == btn]

    def menu_show(self, *args):
        self.isLocked = True

    def menu_hide(self, *args):
        self.isLocked = False

    def createToolBtn(self):
        toolBtnInfo = {}
        for name, info in ToolIcon_config.items():
            lb = ui_utils.IconLabel()
            pix1 = QtGui.QPixmap(icon_path + info["icon"])
            pix2 = QtGui.QPixmap(icon_path + info["icon_bright"])
            lb.setupIcon(pix2, pix1)
            lb.setToolTip(info["tip"])
            toolBtnInfo[name] = lb
            self.toolBtnHbox.addWidget(lb)
        return toolBtnInfo

    def createBtnWidget(self, type, layout, *args):
        """

        :param type:
        :return:
        """
        btnList = []
        for name, info in Icon_config[type].items():
            btn = QtWidgets.QPushButton(name)
            btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path + info["icon"])))
            btn.clicked.connect(partial(cmds.evalDeferred, info["command"]))
            btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(self.create_rightmenu)
            btn.installEventFilter(self)
            btnList.append(name)
            layout.addWidget(btn)
        return btnList

    def addCoWidget(self):
        for name, info in Icon_config.items():
            self.createCoWidget(name)

        self.createCustomCo()
        self.spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scrollVBox.addItem(self.spacerItem1)

    def createCoWidget(self, name):
        widget = QtWidgets.QWidget()
        vBox = QtWidgets.QVBoxLayout(widget)
        vBox.setContentsMargins(0, 0, 0, 0)
        btnList = self.createBtnWidget(name, vBox)

        csCo = ui_utils.createCollapsibleWidget(addWidget=widget, expanded=False, text=name,
                                                parent=self)
        self.scrollVBox.addWidget(csCo)
        self.coWidgets.update({name: {widget: btnList}})

    def refreshUI(self, *args):
        widgets_to_remove = []
        for i in reversed(range(self.scrollVBox.count())):
            widget = self.scrollVBox.itemAt(i).widget()
            if widget is not None:
                widgets_to_remove.append(widget)

        # 逐个调用deleteLater()方法删除控件
        for widget in widgets_to_remove:
            widget.deleteLater()

        self.scrollVBox.removeItem(self.spacerItem1)
        self.addCoWidget()

    def showAddUI(self, *args):
        ui_utils.showDialog(DockableScriptUI)

    def createCustomCo(self):

        widget = QtWidgets.QWidget()
        self.customVBox = QtWidgets.QVBoxLayout(widget)
        self.customVBox.setContentsMargins(0, 0, 0, 0)

        self.Co = ui_utils.createCollapsibleWidget(addWidget=widget, expanded=False, text="Custom Script",
                                                   parent=self)
        self.scrollVBox.addWidget(self.Co)

        if not os.path.exists(self.jsonFile):
            return
        else:
            with open(self.jsonFile, 'r') as f:
                customData = json.load(f)
            for name, info in customData.items():
                if name != "favorites":
                    path = info["path"]
                    sys.path.append(path)
                    icon_path = info["icon"]
                    cmd = info["command"]
                    btn = QtWidgets.QPushButton(name)
                    btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))
                    btn.clicked.connect(partial(cmds.evalDeferred, cmd))
                    self.customVBox.addWidget(btn)

    # 创建右键菜单函数
    def create_rightmenu(self, pos):
        sender = self.sender()
        # 菜单对象
        menu = QtWidgets.QMenu(self)
        save_action = menu.addAction("Save Script To Shelf")
        favorite_action = menu.addAction("Add Favorite")
        cancel_action = menu.addAction("Cancel Favorite")

        save_action.triggered.connect(partial(self.addCurrentShelf, sender))
        favorite_action.triggered.connect(partial(self.addFavorite, sender))
        cancel_action.triggered.connect(partial(self.restoreBtnBc, sender))

        menu.exec_(sender.mapToGlobal(pos))

    def exportUserConfig(self):
        exportDict = {}
        with open(self.jsonFile, 'r') as f:
            exportDict = json.load(f)
        self.favorites = list(Icon_config["Favorites"].keys())

        exportDict.update({"favorites": self.favorites})
        with open(self.jsonFile, 'w') as fp:
            json.dump(exportDict, fp, indent=4)

    def addFavorite(self, control):
        [Icon_config["Favorites"].update({btnName: btnInfo}) for type, typeInfo in Icon_config.items() for
         btnName, btnInfo in typeInfo.items() if control.text() == btnName]

        favoritesWidget = list(self.coWidgets["Favorites"].keys())[0]

        child_btnList = favoritesWidget.findChildren(QtWidgets.QPushButton)
        child_btnNameList = [btn.text() for btn in child_btnList]

        # for btnName in child_btnNameList:
        if control.text() not in child_btnNameList:
            controlInfoDict = {}
            for type, btnInfo in Icon_config.items():
                if control.text() in btnInfo:
                    controlInfoDict = btnInfo[control.text()]
            button = QtWidgets.QPushButton(control.text())
            button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path + controlInfoDict["icon"])))
            button.clicked.connect(partial(cmds.evalDeferred, controlInfoDict["command"]))
            button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(self.create_rightmenu)
            button.installEventFilter(self)
            favoritesWidget.layout().addWidget(button)
        favoritesWidget.update()
        self.exportUserConfig()

    def restoreBtnBc(self, control):
        keys_to_remove = []
        for btnName, btnInfo in Icon_config["Favorites"].items():
            if control.text() == btnName:
                keys_to_remove.append(btnName)

        for key in keys_to_remove:
            del Icon_config["Favorites"][key]

        favoritesWidget = list(self.coWidgets["Favorites"].keys())[0]
        child_btnList = favoritesWidget.findChildren(QtWidgets.QPushButton)
        child_btnNameList = [btn.text() for btn in child_btnList]
        if control.text() in child_btnNameList:
            for i in range(favoritesWidget.layout().count()):
                item = favoritesWidget.layout().itemAt(i)
                if item.widget() and isinstance(item.widget(),
                                                QtWidgets.QPushButton) and item.widget().text() == control.text():
                    button = item.widget()
                    favoritesWidget.layout().removeWidget(button)
                    button.deleteLater()
                    break

        favoritesWidget.update()
        self.exportUserConfig()

    def addCurrentShelf(self, control):
        for itemName, infoDict in Icon_config.items():
            if itemName != "Favorites":
                for btnName, btnInfo in infoDict.items():
                    if control.text() == btnName:
                        ui_utils.addShelfButton(btnName, btnInfo["command"], icon_path + btnInfo["icon"], "")

    @staticmethod
    def executeCmd(cmd, *args):
        cmds.evalDeferred(cmd)

    def refreshType(self):
        self.isLocked = not self.isLocked

    def mousePressEvent(self, event):
        if event.buttons == QtCore.Qt.RightButton:
            self.isLocked = True
        self.isClicked = True
        self.firstClickedPos = event.pos()

    def mouseMoveEvent(self, event):
        if self.isClicked:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(event.globalPos() - self.firstClickedPos)

    def mouseReleaseEvent(self, event):
        self.isClicked = False

    def resizeEvent(self, event):
        # 窗口圆角事件
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRoundedRect(pixmap.rect(), 15, 15)
        painter.end()

        self.setMask(pixmap.mask())

    def enterEvent(self, event):
        if event.type() == QtCore.QEvent.Enter:
            if not self.isLocked:
                self.resize(self.scaledSize)
                self.opacityTimer.start(10)
            self.pix = QtGui.QPixmap(icon_path + "/hemu.png")
            self.pix.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label.setPixmap(self.pix)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if event.type() == QtCore.QEvent.Leave:
            if not self.isLocked:
                self.resize(self.orgSize)
                self.opacityTimer.start(10)
            self.pix = QtGui.QPixmap(icon_path + "/hemu1.png")
            self.pix.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label.setPixmap(self.pix)
        super().leaveEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter or event.type() == QtCore.QEvent.Leave:
            if obj.metaObject().className() == 'QPushButton':
                self.isLocked = True
        return super().eventFilter(obj, event)

    def updateOpacity(self):
        if not self.isLocked:
            self.opacity = min(self.opacity + .01, self.maxOpacity) if self.underMouse() else max(self.opacity - .01,
                                                                                                  self.minOpacity)
            self.setWindowOpacity(self.opacity)
