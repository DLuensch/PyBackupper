'''
@title           :PBConfigParser.py
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

import configparser
from PBConfig import PBConfig
from PBParamCombi import ParamCombi
from PBLogger import Logger

class ConfigParser(object):
    
    def __init__(self, configFile):
        self.__file = str(configFile)
        self.__configs = []
        self.__logger = None
        
        
    def __readProjectConfig(self, config, cfgPath):
        
        errorOccurred = False
        configParser = configparser.ConfigParser(allow_no_value=True)
        
        if (configParser.read(cfgPath) and isinstance(config, PBConfig)):
            #[options] - Part
            try:
                dstRootPath = configParser["options"]["dstBackupRootPath"]
                srcRootPath = configParser["options"]["srcRootPath"]
                
                
                if (len(dstRootPath) == 0):
                    errorOccurred = True
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                           + "] <__readProjectConfig> dstRootPath was not set!")
                    
                if (not errorOccurred):                
                    backupType = configParser["options"]["backupType"]
                    
                    if ((len(backupType) == 0) or \
                            ((backupType != config.PB_BACKUP_TYPE_OVERWRITE) and \
                                            (backupType != config.PB_BACKUP_TYPE_DATE))):
                        errorOccurred = True 
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                               + "] <__readProjectConfig> backupType was not set or is wrong!")   
                
                #Read additional options and set them
                if (not errorOccurred):
                    
                    try:
                        zipProject = configParser.getboolean("options", "zipProject") 
                        config.setZipRule(zipProject)
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                                   + "] <__readProjectConfig> Missing parameter 'zipProject'! Set to default ('no' zip)", Logger.PB_LOGGER_INFO)
                    
                    try:
                        copySysLinks = configParser.getboolean("options", "copySysLinks")
                        config.setCopySysLinksRule(copySysLinks) 
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                                   + "] <__readProjectConfig> Missing parameter 'copySysLinks'! Set to default ('no' system link copy)", Logger.PB_LOGGER_INFO)
                    
                    try:
                        blackList = (configParser.get("options", "blackList").replace(" ", "")).split(',')
                        config.setBlackList(blackList)
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                                   + "] <__readProjectConfig> Missing parameter 'blackList'! Set list empty", Logger.PB_LOGGER_INFO)
                    
                    try:
                        whiteList = (configParser.get("options", "whiteList").replace(" ", "")).split(',')
                        config.setWhiteList(whiteList)
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                                   + "] <__readProjectConfig> Missing parameter 'whiteList'! Set list empty", Logger.PB_LOGGER_INFO)
                                        
                    try:
                        dbUser = configParser.get("options", "dbUserName")
                        dbUserPw = configParser["options"]["dbUserPW"]
                        dbName = configParser["options"]["dbName"]                                              
                        config.setMySqlDbParams(dbUser, dbUserPw, dbName)
                        
                        # Optional parameter  
                        try:                        
                            dbCompress = configParser.getboolean("options", "dbCompress")
                            config.setDBCompressRule(dbCompress)
                        except:
                            self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                                   + "] <__readProjectConfig> DB backup parameter missing: 'dbCompress'! Set to default ('no' compression)", Logger.PB_LOGGER_INFO)
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                               + "] <__readProjectConfig> DB backup parameter missing: 'dbUserName' or 'dbUserPW' or 'dbName'! Database backup not possible!", Logger.PB_LOGGER_INFO)
                    
                    config.setBackupSavePath(dstRootPath)
                    config.setSrcRootPath(srcRootPath)
                    config.setBackupType(backupType)               
            except:
                errorOccurred = True
                self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                       + "] <__readProjectConfig> Could not parse config! [options]-Section is missing.") 
                
            #[paths], [operations] - Part
            if not errorOccurred:
                try:
                    cfgOperations = configParser.items("operations")
                    cfgPaths = configParser.items("paths")
                    
                    if (len(cfgOperations) == len(cfgPaths)):
                       
                        for i in range(0, len(cfgPaths)):
                            if ((cfgOperations[i][1] == ParamCombi.BACKUP_FILE) or (cfgOperations[i][1] == ParamCombi.BACKUP_RECUSIVE) \
                                or (cfgOperations[i][1] == ParamCombi.BACKUP_DIRECTORY) or (cfgOperations[i][1] == ParamCombi.BACKUP_MYSQLDB)):
                                paramCombi = ParamCombi(cfgOperations[i][1], cfgPaths[i][1])
                                config.insertBackupParamCombi(paramCombi)
                            else:
                                self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + \
                                                        "] <__readProjectConfig> Wrong parameter at: [operations] -> " + \
                                                        str(cfgOperations[i][0]) + "! Must be '-d', '-r' or '-f' but was: " + str(cfgOperations[i][1]))
                    else:
                        errorOccurred = True
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                               + "] <__readProjectConfig> Could not parse [paths], [operations]! Different length!")
                    
                except:  
                    errorOccurred = True             
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                           + "] <__readProjectConfig> Could not parse config! [paths], [operations]-Section is missing")
        else:
            
            self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                   + "] <__readProjectConfig> Config file does not exist")       
            errorOccurred = True
        
        return not errorOccurred       
        
    def readConfig(self, logger):
        """Reads the config file"""
        errorOccurred = False
        configParser = configparser.ConfigParser()    
        
        if configParser.read(self.__file) and isinstance(logger, Logger):
            
            configItems = configParser.items("PyBackupperConfigs")
            self.__logger = logger
            
            if len(configItems) > 0:
                for backupName, configPath in configItems:
                    config = PBConfig(str(backupName))
                    self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Start reading config", self.__logger.PB_LOGGER_INFO)
                    
                    if self.__readProjectConfig(config, configPath):
                        
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Read config successfully", self.__logger.PB_LOGGER_INFO)
                        self.__configs.append(config)
                    else:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Error while reading the config")
                        errorOccurred = True
                    
            else:
                if not isinstance(logger, Logger):
                    self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Logger has a wrong type. Must be: Logger!")
                else:
                    self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Config file does not exist")
                errorOccurred = True
        else:
            errorOccurred = True
        
        return not errorOccurred   
    
    def getConfigs(self):
        return self.__configs     
        