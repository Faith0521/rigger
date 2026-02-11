# Embedded file name: E:/JunCmds/tool/blendShapeManage\ggWindows.py
import maya.cmds as cmds

class Windows:

    def cueDialog(self, text, title):
        result = cmds.promptDialog(title=title, text=text, message='Enter New Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        elif result == 'Cancel':
            text = None
        return text

    def loadText(self, fieldButtonGrp):
        selObj = cmds.ls(sl=1)
        if len(selObj) > 0:
            cmds.textFieldButtonGrp(fieldButtonGrp, edit=True, text=selObj[0])
            print selObj[0]

    def removeUnicode(self, str):
        frontIndex = str.index("u'") + 2
        backIndex = str.rfind("'")
        return str[frontIndex:backIndex]