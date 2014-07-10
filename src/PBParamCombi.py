'''
Created on 18.04.2014

@author: Dennis
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