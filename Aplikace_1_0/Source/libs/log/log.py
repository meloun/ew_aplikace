# -*- coding: utf-8 -*-
'''
Created on 12.3.2009
@author: krcka
'''
#import iqhouseccd.settings
import logging.handlers
import settings


class _Log:

    __my_logger = None
    
    def __init__(self):
        self.__my_logger = logging.getLogger('ewitis_logger')
        self.__my_logger.setLevel(logging.DEBUG)
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
               settings.LOG_FILENAME , maxBytes=3000, backupCount=5)
        ch = logging.StreamHandler()
        
        formatter = logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s")
        handler.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.__my_logger.addHandler(handler)
        self.__my_logger.addHandler(ch)
        
    def get_logger(self):
        return self.__my_logger

#
_log = _Log()

def Log(): 
    """
    Singleton
    """
    return _log.get_logger()


if __name__ == '__main__':
    #print settings.LOG_FILENAME    
    # "application" code
    Log().debug("debug message")
    Log().info("info message")
    Log().warn("warn message")
    Log().error("error message")
    Log().critical("critical message")


                
        