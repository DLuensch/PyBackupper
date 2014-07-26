'''
@title           :PBBackup.py
@description     :
@author          :Dennis Luensch
@date            :2014.04.20
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
@license         :GPL v2
'''

from PBConfig import PBConfig
from PBParamCombi import ParamCombi
from PBLogger import Logger
import os, shutil, time, stat, datetime

class Backup(object):
    
    def __getTimeStamp(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
        return str(timestamp)
    
    def __init__(self, logger):
        self.__dstPath = ""
        self.__logger = logger
        
    def __backupRecusive(self, src, dst, backupName, folderOnly = False, symlinks = False, ignore = None):
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
                
                if folderOnly and os.path.isdir(s):
                    continue
                
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
                
            elif ((param.getParam() == ParamCombi.BACKUP_RECUSIVE) \
                    or (param.getParam() == ParamCombi.BACKUP_DIRECTORY)):                
                folder = ""
                dst = self.__dstPath
                
                # Is needed, because the base folder name is not copied
                if param.getPath().endswith("/"):
                    folder = os.path.basename(os.path.dirname(param.getPath()))
                else:
                    folder = os.path.basename(param.getPath())
                dst = os.path.join(dst, folder)
                
                self.__backupRecusive(param.getPath(), dst, config.getBackupName(), \
                                      (param.getParam() == ParamCombi.BACKUP_DIRECTORY))
            elif (param.getParam() == ParamCombi.BACKUP_MYSQLDB):
                #TODO paste sql backup code
                print("Backup sql db: " + param.getPath())
                
            
            
        
        