'''
Created on 01.06.2011

@author: MELICHARL
'''
#-*- coding: utf-8 -*-  

import time

def getUnderlinedDatetime():
    datetime = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())    
    return datetime

def getUnderlinedDate():
    date = time.strftime("%Y_%m_%d", time.localtime())    
    return date
    
if __name__ == "__main__":
    print getUnderlinedDatetime()
    