PyBackupper
===========

Backup software for cyclical backup creation for Windows and Linux. Creates backups of entire folders, sql-database and individual files. Easy to use!

# Requirements
* Python 3.4 or later
* Windows or Linux sytem

# Excute

At startup you need to call the 'global_config'!
```
python3 PyBackupper.py path_to_your_config/config.cfg
```

# The config files
You need 2 different types of configs for this project, a 'global_config' and a 'project_config'. 

* The 'global_config' at startup. In this file, all 'project_config' files will be referenced for the backup. You can have multiple 'project_configs' in a 'global_config'. You can create 'global_configs' for e.g. daily backup, weekly backup and so on. <br><br> 
**Sample 'global_config.cfg':**
```
[PyBackupperConfigs] #Do not change this line!
#
# This file must be refereced at PyBackupper startup!
#
# Add your configs here! All configs will be successively executed!
# Configs can be referenced absolutely or relatively. 
#
# The idea is to create some of these configs for different backups. 
# E.g.: Daily backup, weekly backup and so on.
#
#
# sample_backup_1 = Name of the backup, will be the root folder.
# ./config/sample_cfg.cfg = Path to the actual config of the backup.
sample_backup_1 = ./config/sample_cfg.cfg
#
# Next config
# name_of_the_backup = full_or_relative_path_to_the_cfg/config_name.cfg
#
# .. and so on ...
```
* The 'project_config' contains the settings for the actual backup. It's easy to understand if you take a look at the 'project_sample_config.cfg'. <br><br>
**Sample 'project_sample_config.cfg':**
```
# Useable parameter:
# -f Copies a file, specified at [paths]
# -r Copies a directory recursively, specified at [paths] 
# -d Copies a directory not recursively, specified at [paths]
# -sql Creates a sqldump, DB-Name specified at [paths]
# 
# The parameter pairs in [operations] and [paths] belongs sequentially together.
# E.g.: op1 and path 1, op2 and path2
# You can set any name you want for opX and pathX. They are placeholder and only for you for better identification.
[operations] #Do not change this line! 
op1 = -f
op2 = -r
op3 = -d
#op4 = -sql

# All Path are relativ to "srcRootPath"!!!
# You don't need to set the first '/'
# E.g. path 1: /home/luensel/Entwicklung/PyBackupper/Testumgebung/toBackup/folder1/file1.txt
[paths] #Do not change this line!
path1 = /folder1/file1.txt
path2 = folder1
path3 = file1.txt
#path4 = localhost

[options] #Do not change this line!
# 
# dstBackupRootPath = Path were the Project be backuped. A subfolder with the project name will be created
dstBackupRootPath = ../../../Testumgebung/PyBackupTest/
#
# srcRootPath = Path to the root folder where your files for backup are.
srcRootPath = /home/luensel/Entwicklung/PyBackupper/Testumgebung/toBackup/
#
# zipProject = Compress the backup. NOT IMPLEMENTED YET!
# zipProject = no
#
# System links will be copied if is set to 'true'
copySysLinks = no
#
# You can set 2 different backup types here:
# owrite - Creates a copy of the files and overwrite them every time
# date - Creates a seperate directory with the actual date as the name and copies the files into it
backupType = owrite

# Optional parameters. You don't must set them. 
# They can be deleted if you don't want to backup a sql database.
dbUserName = test_user
dbUserPW = test_pw
dbName = test_db_name
dbCompress = yes

# Optional parameters.
#
# If 'whiteList' arguments are set, all files with this endings will be copied. 
# If you don't want to use a whielist, leaf it empty or delete this option.
# The whitelist has a higher weighting than the blacklist. If arguments are set, the 'blackList' will be ignored.
whiteList = .txt, .pdf, .zip 
#
# If 'blackList' arguments are set, all files with this endings will be ignored.  
# If you don't want to use a blackList, leaf it empty or delete this option.
blackList = 

```
