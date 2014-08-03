'''
@title           :PBParamCombi.py
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

class ParamCombi(object):
    
    BACKUP_FILE = "-f"
    BACKUP_DIRECTORY = "-d" 
    BACKUP_RECUSIVE = "-r"
    BACKUP_MYSQLDB = "-sql"

    def __init__(self, operation, path):
        self.__operation = operation
        self.__path = path
        
    def getPath(self):
        return self.__path
    
    def getParam(self):
        return self.__operation