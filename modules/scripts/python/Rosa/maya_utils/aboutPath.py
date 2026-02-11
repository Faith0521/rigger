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
    return datePath

def filePath(type):
    if type == 'curve':
        return whereAmI() + '/data' + '/curve/'
    elif type == 'ui':
        return whereAmI() + '/data' + '/ui/'
    else:
        mc.error('function <filePath> input wrong type!')
            
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



    