'''
Created on 18.04.2014

@author: Dennis
'''

import configparser, time
from PBParamCombi import ParamCombi

class PBConfig(object):
    
    PB_BACKUP_TYPE_OVERWRITE = "owrite"
    PB_BACKUP_TYPE_DATE = "date"

    def __init__(self, backupName):
        self.__backupName = backupName
        self.__paramCombis = []
        self.__savePath = ""
        self.__zipProject = False
        self.__backUpType = "o"
        
    def setZipRule(self, value):
        self.__zipProject = bool(value)
        
    def setBackupType(self, backUpType):
        
        errorOccurred = False
        
        if (backUpType == self.PB_BACKUP_TYPE_OVERWRITE or 
                backUpType == self.PB_BACKUP_TYPE_DATE):
                        
            self.__backUpType = backUpType
        else:
            errorOccurred = True
        
        return errorOccurred
        
    def setBackupSavePath(self, savePath):
        
        fullSavePath = savePath
        
        if not (savePath[-1:] == "/"): 
            fullSavePath = (savePath + "/")
            
        self.__savePath = fullSavePath
    
    def insertBackupParamCombi(self, paramCombi):
        
        errorOccurred = False
        
        if type(paramCombi) is ParamCombi:
            
            self.__paramCombis.append(paramCombi)                
        else:
            errorOccurred = True
        
        return errorOccurred
    
    def getBackupName(self):
        return self.__backupName
    
    def getBackupType(self):
        return self.__backUpType
    
    def getZipRule(self):
        return self.__zipProject
    
    def getProjectSavePath(self):
        return self.__savePath
            
    def getProjectParamCombis(self):
        return self.__paramCombis
    