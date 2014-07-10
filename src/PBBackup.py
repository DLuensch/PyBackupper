'''
@title           :PBBackup.py
@description     :
@author          :Dennis Luensch
@date            :20140420
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.3  
'''

from PBConfig import PBConfig
from PBParamCombi import ParamCombi
from PBLogger import Logger
import os, shutil, time, stat

class Backup(object):
    
    def __getTimeStamp(self):
        t = time.localtime()        
        return  str(t.tm_year) + "." \
                      + str(t.tm_mon).zfill(2) + "." + str(t.tm_mday).zfill(2) \
                      + "_" + str(t.tm_hour).zfill(2) + ":" + str(t.tm_min).zfill(2) + ":" + str(t.tm_sec).zfill(2)
    
    def __init__(self, logger):
        self.__dstPath = ""
        self.__logger = logger
        
    def __backupRecusive(self, src, dst, backupName, symlinks = False, ignore = None):
        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
                shutil.copystat(src, dst)
            lst = os.listdir(src)
            if ignore:
                excl = ignore(src, lst)
                lst = [x for x in lst if x not in excl]
            for item in lst:
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if symlinks and os.path.islink(s):
                    if os.path.lexists(d):
                        os.remove(d)
                    os.symlink(os.readlink(s), d)
                    try:
                        st = os.lstat(s)
                        mode = stat.S_IMODE(st.st_mode)
                        os.lchmod(d, mode)
                    except:
                        pass # lchmod not available
                elif os.path.isdir(s):
                    self.__backupRecusive(s, d, backupName, symlinks, ignore)
                else:
                    shutil.copy2(s, d)
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupRecusive> Could not backup folder!")
                
    
    def __backupFile(self, srcPath, backupName):        
        try: 
            shutil.copy2(srcPath, self.__dstPath) 
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupFile> Could not backup File!")
    
    def startBackup(self, config):
        self.__dstPath = str(config.getProjectSavePath()) + str(config.getBackupName()) + "/"
        os.makedirs(self.__dstPath, 0o777, True)
        
        if (config.getBackupType() == PBConfig.PB_BACKUP_TYPE_DATE):
            self.__dstPath += self.__getTimeStamp() + "/"
            os.mkdir(self.__dstPath)
        
        params = config.getProjectParamCombis()    
        for i in range(0, len(params)):
            param = params[i]
            
            if (param.getParam() == ParamCombi.BACKUP_FILE):
                self.__backupFile(param.getPath(), config.getBackupName())
            elif (param.getParam() == ParamCombi.BACKUP_RECUSIVE):
                self.__backupRecusive(param.getPath(), self.__dstPath, config.getBackupName())
                
            
            
        
        