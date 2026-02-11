import weakref
import maya.cmds as mc
from maya.app.general.mayaMixin import *


# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class BroMainWindow_Dockable(MayaQWidgetDockableMixin, QMainWindow):
    DOCK_LABEL_NAME = 'no name window'  # Window display name
    CONTROL_NAME = 'no_name_window'  # Window unique object name
    instances = list()

    def __init__(self):
        super(BroMainWindow_Dockable, self).__init__()
        self.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))
        # Not sure, but I suppose that we better keep track of instances of our window and keep Maya environment clean.
        # So we'll remove all instances before creating a new one.
        if mc.window(self.CONTROL_NAME + "WorkspaceControl", ex=True):
            mc.deleteUI(self.CONTROL_NAME + "WorkspaceControl")

        self.setAttribute(Qt.WA_DeleteOnClose, True)

        # Set object name and window title
        self.setObjectName(self.CONTROL_NAME)
        self.setWindowTitle(self.DOCK_LABEL_NAME)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.build_ui()

    @staticmethod
    def delete_instances():
        for ins in BroMainWindow_Dockable.instances:
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass
            try:
                BroMainWindow_Dockable.instances.remove(ins)
                del ins
            except:
                # Supress error
                pass

    def build_ui(self):
        """
        This function is called at the end of window initialization and creates your actual UI.
        Override it with your UI.
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
# Example class
# ----------------------------------------------------------------------------------------------------------------------
class ChildTestWindow(BroMainWindow_Dockable):
    """
    Example child window inheriting from main class.
    """
    DOCK_LABEL_NAME = 'child test window'  # Window display name
    instances = list()
    CONTROL_NAME = 'child_test_win'  # Window unique object name

    def __init__(self):
        super(ChildTestWindow, self).__init__()

    def build_ui(self):
        self.my_label = QLabel('Beam me up, Scotty!')
        self.main_layout.addWidget(self.my_label)

        self.menuBar = QMenuBar()
        self.presetsMenu = self.menuBar.addMenu(("&Presets"))
        self.saveConfigAction = QAction(("&Save Settings"), self)
        self.presetsMenu.addAction(self.saveConfigAction)

        self.setMenuBar(self.menuBar)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Status bar ready.")

        self.setStatusBar(self.statusBar)

        self.statusBar.setObjectName("statusBar")
        self.setStyleSheet("#statusBar {background-color:#faa300;color:#fff}")

# ----------------------------------------------------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------------------------------------------------

def show_test():
    # This is how to call and show a window
    ChildTestWindow().show(dockable=True)

