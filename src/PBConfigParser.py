'''
Created on 18.04.2014

@author: Dennis
'''
import configparser
from PBConfig import PBConfig
from PBParamCombi import ParamCombi
from PBLogger import Logger
from _winapi import NULL

class ConfigParser(object):
    
    def __init__(self, configFile):
        self.__file = str(configFile)
        self.__configs = []
        self.__logger = NULL
        
        
    def __readProjectConfig(self, config, cfgPath):
        
        errorOccurred = False
        configParser = configparser.ConfigParser(allow_no_value=True)
        
        if (configParser.read(cfgPath) and isinstance(config, PBConfig)):
            #[options] - Part
            try:
                savePath = configParser["options"]["savePath"]
                
                if (len(savePath) == 0):
                    errorOccurred = True
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> savePath was not set!")
                    
                if (not errorOccurred):                
                    backupType = configParser["options"]["backupType"]
                    
                    if ((len(backupType) == 0) or \
                            (backupType != config.PB_BACKUP_TYPE_OVERWRITE) or (backupType != config.PB_BACKUP_TYPE_OVERWRITE)):
                        errorOccurred = True 
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> backupType was not set or is wrong!")   
                
                if (not errorOccurred):
                    zipProject = configParser.getboolean("options", "zipProject") 
                    
                    config.setBackupSavePath(savePath)
                    config.setBackupType(backupType)
                    config.setZipRule(zipProject)
                
            except:
                errorOccurred = True
                self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> Could not parse config! [options]-Section is missing.") 
                
            #[paths], [operations] - Part
            if not errorOccurred:
                try:
                    cfgOperations = configParser.items("operations")
                    cfgPaths = configParser.items("paths")
                    
                    if (len(cfgOperations) == len(cfgPaths)):
                       
                        for i in range(0, len(cfgPaths)):
                            if ((cfgOperations[i][1] == ParamCombi.BACKUP_FILE) or (cfgOperations[i][1] == ParamCombi.BACKUP_RECUSIVE)):
                                paramCombi = ParamCombi(cfgOperations[i][1], cfgPaths[i][1])
                                config.insertBackupParamCombi(paramCombi)
                            else:
                                self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + \
                                                        "] <__readProjectConfig> Wrong parameter at: [operations] -> " + \
                                                        str(cfgOperations[i][0]) + "! Must be '-d' or '-f' but was: " + str(cfgOperations[i][1]))
                    else:
                        errorOccurred = True
                        self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> Could not parse [paths], [operations]! Different length!")
                    
                except:  
                    errorOccurred = True             
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> Could not parse config! [paths], [operations]-Section is missing")
        else:
            
            self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) + "] <__readProjectConfig> Config file does not exist")       
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
                    self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Start reading config")
                    
                    if self.__readProjectConfig(config, configPath):
                        
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Read config successfully")
                        self.__configs.append(config)
                    else:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <readConfig> Error while reading the config")
                    
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
        