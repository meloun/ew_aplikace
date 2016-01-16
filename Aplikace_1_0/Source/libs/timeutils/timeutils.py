'''
Created on 01.06.2011

@author: MELICHARL
'''
#-*- coding: utf-8 -*-  

import datetime
import time

def getCurrentTime():
    mytime = time.strftime("%H:%M:%S", time.localtime())    
    return mytime

def getCurrentDateTime():
    mytime = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())    
    return mytime


def getUnderlinedDatetime():
    datetime = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())    
    return datetime

def getUnderlinedDatetime2():
    aux_datetime = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")    
    return aux_datetime

def getUnderlinedDate():
    date = time.strftime("%Y_%m_%d", time.localtime())    
    return date

def getUnderlinedDate2():
    date = datetime.datetime.now().strftime("%Y_%m_%d")    
    return date

def getDuration(starttime, timeformat = '%Y-%m-%d %H:%M:%S'):
    time1 = datetime.datetime.strptime(starttime, timeformat)
    time2 = datetime.datetime.now()        
    return time2.replace(microsecond=0) - time1.replace(microsecond=0)
    
if __name__ == "__main__":
    print getUnderlinedDatetime()
    print getUnderlinedDatetime2()
    #print getUnderlinedDate()
    #print getUnderlinedDate2()
    
    print datetime.datetime.now().replace(microsecond=0)  
    print getDuration('2013-05-05 20:07:57')  

    