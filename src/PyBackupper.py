'''
Created on 18.04.2014

@author: Dennis
'''
from PBConfigParser import ConfigParser
from PBLogger import Logger
from PBBackup import Backup

def printCfg(pbParser):
    configs = pbParser.getConfigs()
    print(str(len(configs)) + " gelesen!\n")
    for config in configs:
        params = config.getProjectParamCombis()
        print("Name: " + config.getBackupName())
        print("savePath: " + config.getProjectSavePath())
        print("zipProject: " + str(config.getZipRule()))
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
        print("Lesen erfolgreich")
        printCfg(pbParser)
        
        configs = pbParser.getConfigs()
        for config in configs:
            pbBackup.startBackup(config)
    else:
        print("Lesen nicht erfolgreich")
        
    pbLogger.close()

if __name__ == "__main__":
    main()