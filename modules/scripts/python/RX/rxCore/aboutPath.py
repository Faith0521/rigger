# coding: utf-8
#Author: rosa.w
#Mail: wrx1844@qq.com
#Computer language: Python.3.2.2
#scriptName : Path.py
#----------------------------------------------

# May 06 | first write.

#----------------------------------------------
import maya.cmds as mc
import os
import inspect



def getModulesPath(moudle):
        """
        return dir for imported moudle..
        """
        moduleFile = inspect.getfile(moudle)
        modulePath = os.path.dirname(moduleFile)
        return modulePath

def getScriptPath():
        """
        return dir path for used script..
        """
        scriptPath = getModulesPath(inspect.currentframe().f_back)
        return scriptPath

def whereAmI():
        scriptPath = (  os.path.split( os.path.abspath(__file__) )  )
        datePath = scriptPath[0].replace('\\' , '/')
        Path = datePath.replace( '/rxCore' , '' )
        return Path

def filePath(type):
        if type == 'curve':
                return whereAmI() + '/rxData' + '/curve/'
        elif type == 'ui':
                return whereAmI() + '/rxData' + '/ui/'
        elif type == 'icon':
                return whereAmI() + '/rxData' + '/icons/'

        elif type == 'browCmd':
                return whereAmI() + '/rxData' + '/facial/' + 'browCmdLink.sdk'
        elif type == 'browCombineDriver':
                return whereAmI() + '/rxData' + '/facial/' + 'browCombineDriverLink.sdk'
        elif type == 'browCtrl':
                return whereAmI() + '/rxData' + '/facial/' + 'browCtrlLink.sdk'  

        elif type == 'L_eyeCmd':
                return whereAmI() + '/rxData' + '/facial/' + 'L_eyeCmdLink.sdk' 
        elif type == 'L_eyeCtrl':
                return whereAmI() + '/rxData' + '/facial/' + 'L_eyeCtrlLink.sdk'  
        elif type == 'R_eyeCmd':
                return whereAmI() + '/rxData' + '/facial/' + 'R_eyeCmdLink.sdk' 
        elif type == 'R_eyeCtrl': 
                return whereAmI() + '/rxData' + '/facial/' + 'R_eyeCtrlLink.sdk' 

        elif type == 'mouthCmd':
                return whereAmI() + '/rxData' + '/facial/' + 'mouthCmdLink.sdk'
        elif type == 'mouthCtrl':
                return whereAmI() + '/rxData' + '/facial/' + 'mouthCtrlLink.sdk'
        elif type == 'mouthCombineDriver':
                return whereAmI() + '/rxData' + '/facial/' + 'mouthCombineDriverLink.sdk'                          
        else:
                mc.error( 'function <filePath> input wrong type!' )

def fileList(path , suffix):
        result=[]
        allFileList = os.listdir(path)
        if suffix is not None:
                for file in allFileList:
                        if suffix in str(file):
                                result.append(file)
        else:
                result = allFileList

        return result



        