# Embedded file name: \\yuweijun\E\JunCmds\tool\weightEdit\shared_ch\fileDialog.py
import maya.cmds as mc
from mayaPrint import MayaPrint

class FDialog(MayaPrint):

    def fileDialog(self, **flags):
        """
        m(fileMode) int: 
            0 for read 
            1 for write 
            2 for write without paths (segmented files) 
            4 for directories have meaning when used with the action 
            +100 for returning short names 
            
        """
        defineFlags = {'m': (0, int),
         'wt': ('',
                str,
                u'',
                unicode),
         'ft': ('',
                str,
                u'',
                unicode),
         'okc': ('',
                 str,
                 u'',
                 unicode)}
        flagDirect = self.funtionFlag(defineFlags, **flags)
        self.path = []
        m = flagDirect['m']
        ft = flagDirect['ft']
        okc = flagDirect['okc']
        mayaVersion = mc.about(f=True)
        res = []
        if mayaVersion <= '2010':
            if m <= 1:
                path = mc.fileDialog(m=m, directoryMask=ft)
                if path != '':
                    res = [path]
                elif path == '':
                    return
            else:
                mc.fileBrowserDialog(m=m, fc=self.returnPath, an='ZCH', om='Import')
                res = self.path
        else:
            mapToOld = {0: 1,
             1: 0,
             4: 3}
            m = mapToOld[m]
            path = mc.fileDialog2(fileMode=m, dialogStyle=2, fileFilter=ft, okCaption=okc)
            if path != None:
                res = path
        return res

    def returnPath(self, fileName, fileType):
        """For fileBrowserDialog"""
        self.path.append(fileName)