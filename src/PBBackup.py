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
import os, shutil, time, stat, datetime, zipfile, subprocess, shlex


class Backup(object):
    
    def __getTimeStamp(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
        return str(timestamp)
    
    def __init__(self, logger):
        self.__dstRootPath = ""
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
                
    def __backupFile(self, srcPath, dstPath, backupName):        
        try:             
            if not os.path.exists(dstPath):
                os.makedirs(dstPath)
            
            shutil.copy2(srcPath, dstPath) 
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupFile> Could not backup File!")
            
    def __backupSql(self, dbName, dbUser, dbUserPw, savePath, backupName, zipDB):
        
        #args = shlex.split(("mysqldump -u " + dbUser + " -p" + dbUserPw + " " + dbName))
        args = shlex.split(("ls"))
        try:
            
            with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
                dumpOutput = proc.stdout.read()
            
                if zipDB:
                    try:
                        zout = zipfile.ZipFile((savePath + "/" + dbName + ".zip"), "w", zipfile.ZIP_DEFLATED)
                        zout.writestr((dbName + ".sql"), dumpOutput)
                        zout.close()
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at compress process!")
                else:
                    try:
                        fWriter = open((savePath + "/" + dbName + ".sql"), "wb")
                        fWriter.write(dumpOutput)
                        fWriter.close()
                    except:
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at save process!")
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at process call 'mysqldump'!")
    
    def startBackup(self, config):
        self.__dstRootPath = str(config.getProjectSavePath()) + str(config.getBackupName()) + "/"
        os.makedirs(self.__dstRootPath, 0o777, True)
        
        if (config.getBackupType() == PBConfig.PB_BACKUP_TYPE_DATE):
            self.__dstRootPath += self.__getTimeStamp() + "/"
            os.mkdir(self.__dstRootPath)
        
        params = config.getProjectParamCombis()  
          
        for i in range(0, len(params)):
            param = params[i]
            
            srcPath = ""
            dstPath = ""
            srcFilePath = param.getPath()
            
            # If the path starts with a "/", it can't be created
            if srcFilePath.startswith("/"):
                srcFilePath = (srcFilePath)[1:]
            
            if (param.getParam() == ParamCombi.BACKUP_FILE):
                
                # Create the path to the file and the destination path with the subfolder
                srcPath = os.path.join(config.getSrcRootPath(), srcFilePath)                
                dstPath = os.path.join(self.__dstRootPath, (os.path.split(srcFilePath))[0])
                
                self.__backupFile(srcPath, dstPath, config.getBackupName())
                
            elif ((param.getParam() == ParamCombi.BACKUP_RECUSIVE) \
                    or (param.getParam() == ParamCombi.BACKUP_DIRECTORY)):                
                
                srcPath = os.path.join(config.getSrcRootPath(), srcFilePath) 
                dstPath = os.path.join(self.__dstRootPath, srcFilePath)
                
                self.__backupRecusive(srcPath, dstPath, config.getBackupName(), \
                                      (param.getParam() == ParamCombi.BACKUP_DIRECTORY))
                
            elif (param.getParam() == ParamCombi.BACKUP_MYSQLDB):
               
                savePath = os.path.join(self.__dstRootPath, "Database")
               
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)      
                
                self.__backupSql(config.getSqlName(), config.getSqlUserName(), \
                                 config.getSqlUserPw(), savePath, config.getBackupName(), config.getDBCompressRule())      