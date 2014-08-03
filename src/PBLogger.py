'''
@title           :PBLogger.py
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

import time

class Logger(object):
    '''
    classdocs
    '''
    
    PB_LOGGER_FATAL_ERROR = "FATAL_ERROR"
    PB_LOGGER_ERROR = "ERROR"
    PB_LOGGER_WARNING = "WARNING"
    PB_LOGGER_INFO = "INFO"
    
    
    def __getTimeStamp(self):
        t = time.localtime()        
        return  str(t.tm_year) + "-" \
                      + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2) \
                      + "_" + str(t.tm_hour).zfill(2) + ":" + str(t.tm_min).zfill(2) + ":" + str(t.tm_sec).zfill(2)
    
    def __init__(self):
        self.__fwriter = open("log.txt", "a")
        self.__fwriter.write("-------------- Log: " + self.__getTimeStamp() + "\n")
        
    def writeMsg(self, msg, type = PB_LOGGER_ERROR):
        wMsg = "<" + self.__getTimeStamp() + ">  <<" + type.center(11) + ">> " + str(msg)
        self.__fwriter.write(wMsg + "\n")   
        print(wMsg)
    
    def close(self):
        self.__fwriter.write("\n")
        self.__fwriter.close()
        