'''
@title           :PBBackupper.py
@description     :
@author          :Dennis Luensch
@date            :2014.04.18
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
@license         :GPL v2 
'''

from PBConfigParser import ConfigParser
from PBLogger import Logger
from PBBackup import Backup

def printCfg(pbParser):
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
        else:
            print("DB: No Settings")
        print("Params: " + str(len(params)))
        for i in range(0, len(params)):
            param = params[i]
            print("   " + param.getParam() + " " + param.getPath())
        print("----------")

def main():
    pbLogger = Logger()
    pbParser = ConfigParser("./config/config.cfg")
    pbBackup = Backup(pbLogger)
    
    if pbParser.readConfig(pbLogger):
        print("read successfull")
        printCfg(pbParser)
        
        configs = pbParser.getConfigs()
        for config in configs:
            pbBackup.startBackup(config)
    else:
        print("reading failed")
        
    pbLogger.close()

if __name__ == "__main__":
    main()