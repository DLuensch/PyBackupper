'''
@title           :PBParamCombi.py
@description     :
@author          :Dennis Luensch
@date            :2014.04.18
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
'''

class ParamCombi(object):
    
    BACKUP_FILE = "-f"
    BACKUP_RECUSIVE = "-d"

    def __init__(self, operation, path):
        self.__operation = operation
        self.__path = path
        
    def getPath(self):
        return self.__path
    
    def getParam(self):
        return self.__operation