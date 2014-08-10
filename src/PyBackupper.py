'''
@title           :PBBackupper.py
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

from PBConfigParser import ConfigParser
from PBLogger import Logger
from PBBackup import Backup
import sys

def printCfg(pbParser): #TODO: add new config parameter
    configs = pbParser.getConfigs()
    print(str(len(configs)) + " readed!\n")
    for config in configs:
        params = config.getProjectParamCombis()
        print("Name: " + config.getBackupName())
        print("savePath: " + config.getProjectSavePath())
        print("zipProject: " + str(config.getZipRule()))
        if config.dbParamsSet():
            print("User: " + config.getSqlUserName())
            print("PW: " + config.getSqlUserPw())
            print("DB Name: " + config.getSqlName())
            print("DB Zip: " + str(config.getDBCompressRule()))
        else:
            print("DB: No Settings")
        print("Params: " + str(len(params)))
        for i in range(0, len(params)):
            param = params[i]
            print("   " + param.getParam() + " " + param.getPath())
        print("----------")

def main():
    pbLogger = Logger()
    
    #if True: #TODO: Only in RC
    if len(sys.argv) >= 2:
        #pbParser = ConfigParser("./config/config.cfg") #TODO: Only in RC
        pbParser = ConfigParser(sys.argv[1])
        
        pbBackup = Backup(pbLogger)
        
        pbLogger.writeMsg("[PyBackupper] " + "<main> PyBackupper started!", pbLogger.PB_LOGGER_INFO)
        
        try:
            if pbParser.readConfig(pbLogger):
                #printCfg(pbParser) #TODO: Only in RC
                
                configs = pbParser.getConfigs()
                for config in configs:
                    pbBackup.startBackup(config)
            else:
                pbLogger.writeMsg("[PyBackupper] " + "<main> Could not read config! Backup failed.", pbLogger.PB_LOGGER_INFO)
        except:
            pbLogger.writeMsg("[PyBackupper] " + "<main> An unexpected error occurred!" + sys.exc_info()[0], pbLogger.PB_LOGGER_FATAL_ERROR)
    else:
        pbLogger.writeMsg("[PyBackupper] " + "<main> No config set! Call (Linux): python3.X path_to_src_folder/PyBackupper.py path_to_your_config/your_config.cfg", pbLogger.PB_LOGGER_FATAL_ERROR)
    pbLogger.close()

if __name__ == "__main__":
    main()