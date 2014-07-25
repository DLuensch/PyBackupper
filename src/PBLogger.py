'''
@title           :PBLogger.py
@description     :
@author          :Dennis Luensch
@date            :2014.04.18
@version         :1.0
@usage           :python pyscript.py
@notes           :
@python_version  :3.4
@license         :GPL v2
'''

import time

class Logger(object):
    '''
    classdocs
    '''
    
    def __getTimeStamp(self):
        t = time.localtime()        
        return  str(t.tm_year) + "." \
                      + str(t.tm_mon).zfill(2) + "." + str(t.tm_mday).zfill(2) \
                      + "_" + str(t.tm_hour).zfill(2) + ":" + str(t.tm_min).zfill(2) + ":" + str(t.tm_sec).zfill(2)
    
    def __init__(self):
        self.__fwriter = open("log.txt", "a")
        self.__fwriter.write("-------------- Log: " + self.__getTimeStamp() + "\n")
        
    def writeMsg(self, msg):
        wMsg = "<" + self.__getTimeStamp() + ">  " + str(msg)
        self.__fwriter.write(wMsg + "\n")   
        print(wMsg)
    
    def close(self):
        self.__fwriter.write("\n")
        self.__fwriter.close()
        