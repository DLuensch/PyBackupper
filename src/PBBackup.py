'''
@title           :PBBackup.py
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
        
    def __checkList(self, file, list):
        found = False
        fileExt = os.path.splitext(file)[1]
        try:            
            for key in list:
                if str(fileExt) == str(key):
                    found = True
                    break
        except:
            print("Hier lief was falsch")
        
        return found
    
    # folderOnly means not recursive    
    def __backupRecusive(self, src, dst, backupName, folderOnly = False, symlinks = False, whiteList = None, blackList = None, zipper = None):
        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
                shutil.copystat(src, dst)
            lst = os.listdir(src)
            
            for item in lst:
                s = os.path.join(src, item)
                d = os.path.join(dst, item)               
                    
                if folderOnly and os.path.isdir(s):
                    continue
                
                if not os.path.isdir(s) and whiteList:
                    if not self.__checkList(s, whiteList):
                        continue                    
                elif not os.path.isdir(s) and blackList:
                    if self.__checkList(s, blackList):
                        continue
                
                if symlinks and os.path.islink(s):
                    if os.path.lexists(d):
                        os.remove(d)
                    os.symlink(os.readlink(s), d)
                    try:
                        st = os.lstat(s)
                        mode = stat.S_IMODE(st.st_mode)
                        os.chmod(d, mode)
                    except:
                        pass # lchmod not available
                elif os.path.isdir(s):
                    self.__backupRecusive(s, d, backupName, folderOnly, symlinks, whiteList, blackList, zipper)
                else:
                    if zipper:
                        zipper.write(s, d)
                    else:
                        shutil.copy2(s, d)
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupRecusive> Could not backup folder!")
                
    def __backupFile(self, srcPath, dstPath, backupName, zipper = None):        
        try:
            if zipper:
                dstPath = os.path.join(dstPath, os.path.basename(srcPath))
                zipper.write(srcPath, dstPath)
            else:                 
                if not os.path.exists(dstPath):
                    os.makedirs(dstPath)
                
                shutil.copy2(srcPath, dstPath) 
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupFile> Could not backup File!")
            
    def __backupSql(self, dbName, dbUser, dbUserPw, savePath, backupName, zipDB, zipper = None):
        
        args = shlex.split(("mysqldump -u " + dbUser + " -p" + dbUserPw + " " + dbName))
        #args = shlex.split("ls") #TODO: Only in RC
        
        try:            
            with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
                dumpOutput = proc.stdout.read()
                
                errorOccurred = False
                file = ""
            
                if zipDB:
                    try:
                        file = dbName + ".zip"
                        zout = zipfile.ZipFile((savePath + "/" + file), "w", zipfile.ZIP_DEFLATED)
                        zout.writestr((dbName + ".sql"), dumpOutput)
                        zout.close()
                    except:
                        errorOccurred = True
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at compress process!")
                else:
                    try:
                        file = dbName + ".sql"
                        fWriter = open((savePath + "/" + file), "wb")
                        fWriter.write(dumpOutput)
                        fWriter.close()
                    except:
                        errorOccurred = True
                        self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at save process!")
                
                if not errorOccurred and zipper:
                    zipper.write((savePath + "/" + file), "Database/" + file)
                    shutil.rmtree(savePath)
        except:
            self.__logger.writeMsg("[PBConfigParser] [" + str(backupName) + "] <__backupSql> Something went wrong at process call 'mysqldump'!")
    
    def startBackup(self, config):
        self.__dstRootPath = os.path.join(str(config.getProjectSavePath()), str(config.getBackupName()))
        os.makedirs(self.__dstRootPath, 0o777, True)
        zipper = None
        
        if (config.getBackupType() == PBConfig.PB_BACKUP_TYPE_DATE):
            self.__dstRootPath = os.path.join(str(config.getProjectSavePath()), self.__getTimeStamp())
            os.mkdir(self.__dstRootPath)
        
        if config.getZipRule():
            zipper = zipfile.ZipFile((self.__dstRootPath + "/" + config.getBackupName() + ".zip"), "w", zipfile.ZIP_DEFLATED)
        
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
                if config.getZipRule():
                    dstPath = (os.path.split(srcFilePath))[0]
                else:                  
                    dstPath = os.path.join(self.__dstRootPath, (os.path.split(srcFilePath))[0])
                
                self.__backupFile(srcPath, dstPath, config.getBackupName(), zipper)
                
            elif ((param.getParam() == ParamCombi.BACKUP_RECUSIVE) \
                    or (param.getParam() == ParamCombi.BACKUP_DIRECTORY)):                
                
                srcPath = os.path.join(config.getSrcRootPath(), srcFilePath) 
                if config.getZipRule():
                    dstPath = os.path.join("", srcFilePath)
                else:
                    dstPath = os.path.join(self.__dstRootPath, srcFilePath)
                
                if os.path.isdir(srcPath):    
                    self.__backupRecusive(srcPath, dstPath, config.getBackupName(), \
                                      (param.getParam() == ParamCombi.BACKUP_DIRECTORY), \
                                        config.getCopySysLinksRule(), config.getWhiteList(), config.getBlackList(), zipper)
                else:
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                          + "] <startBackup> Could not backup folder! Path '" + str(srcPath) +"' is no folder or does not exist!")
                
            elif (param.getParam() == ParamCombi.BACKUP_MYSQLDB):
               
                if config.dbParamsSet():
                    savePath = os.path.join(self.__dstRootPath, "Database")
                   
                    if not os.path.isdir(savePath):
                        os.makedirs(savePath)      
                    
                    self.__backupSql(config.getSqlName(), config.getSqlUserName(), \
                                     config.getSqlUserPw(), savePath, config.getBackupName(), config.getDBCompressRule(), zipper)   
                else:
                    self.__logger.writeMsg("[PBConfigParser] [" + str(config.getBackupName()) \
                                          + "] <startBackup> Could not backup sql-database! Database parameter not set! Needed parameter in config file are: " \
                                          + "'dbUserName', 'dbUserPW' and 'dbName'")   
        
        if config.getZipRule():
            zipper.close()