'''
@title           :PBConfig.py
@description     :
@author          :Dennis Luensch
@date            :2014.04.18
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
@license         :GPL v2
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
        self.__backUpType = "owrite"
        self.__dbUser = ""
        self.__dbUserPw = ""
        self.__dbName = ""
        self.__dbParamsSet = False
        
    def setZipRule(self, value):
        self.__zipProject = bool(value)
        
    def setMySqlDbParams(self, dbUser, dbUserPw, dbName):        
        
        if (dbUser and dbUserPw and dbName):
            self.__dbUser = dbUser
            self.__dbUserPw = dbUserPw
            self.__dbName = dbName        
            self.__dbParamsSet = True
        
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
    
    def getSqlUserName(self):
        return self.__dbUser
    
    def getSqlUserPw(self):
        return self.__dbUserPw
    
    def getSqlName(self):
        return self.__dbName
    
    def dbParamsSet(self):
        return self.__dbParamsSet
    