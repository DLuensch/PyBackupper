'''
@title           :PBConfig.py
@description     :
@author          :Dennis Luensch
@contact         :dennis[dot]luensch[at]gmail[dot]com
@date            :2014.08.03
@version         :RC 1
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
@license         :GPL v2
'''

from PBParamCombi import ParamCombi

class PBConfig(object):
    
    PB_BACKUP_TYPE_OVERWRITE = "owrite"
    PB_BACKUP_TYPE_DATE = "date"

    def __init__(self, backupName):
        self.__backupName = backupName
        self.__paramCombis = []
        self.__dstRootPath = ""
        self.__srcRootPath = ""
        self.__zipProject = False
        self.__copySysLinks = False
        self.__backUpType = "owrite"
        self.__dbUser = ""
        self.__dbUserPw = ""
        self.__dbName = ""
        self.__dbParamsSet = False
        self.__dbCompress = False
        self.__whiteList = []
        self.__blackList = []
        
    def setWhiteList(self, list):
        if list[0] == "":
            self.__whiteList = []
        else:
            self.__whiteList = list
    
    def setBlackList(self, list):
        if list[0] == "":
            self.__blackList = []
        else:
            self.__blackList = list
    
    def setZipRule(self, value):
        self.__zipProject = bool(value)
    
    def setDBCompressRule(self, value):
        self.__dbCompress = bool(value)
    
    def setCopySysLinksRule(self, value):
        self.__copySysLinks = bool(value)
        
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
            
        self.__dstRootPath = fullSavePath
        
    def setSrcRootPath(self, srcRootPath):
        
        fullSavePath = srcRootPath
        
        if not (srcRootPath[-1:] == "/"): 
            fullSavePath = (srcRootPath + "/")
            
        self.__srcRootPath = fullSavePath
    
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
    
    def getDBCompressRule(self):
        return self.__dbCompress
    
    def getCopySysLinksRule(self):
        return self.__copySysLinks
    
    def getProjectSavePath(self):
        return self.__dstRootPath
    
    def getSrcRootPath(self):
        return self.__srcRootPath
            
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
    
    def getWhiteList(self):
        return self.__whiteList
    
    def getBlackList(self):
        return self.__blackList
    