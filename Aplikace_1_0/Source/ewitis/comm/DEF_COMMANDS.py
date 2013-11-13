# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

""" Komandy rozdělené do dvou sekcí GET a SET """

DEF_COMMANDS = {
                
    #terminal => aplikace : "states"                                                
    "GET_HW_SW_VERSION"         : {'cmd':0x04,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_DIAGNOSTIC"            : {'cmd':0x08,  'length':2,     'blackbox': True,    'terminal': False},                                      
    "GET_CALIBRATION_DATA"      : {'cmd':0x0F,  'length':0,     'blackbox': True,    'terminal': False},                                      
    "GET_TERMINAL_INFO"         : {'cmd':0x20,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_CELL_INFO"             : {'cmd':0x21,  'length':1,     'blackbox': True,    'terminal': True},                                      
    "GET_TIMING_SETTINGS"       : {'cmd':0x22,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_RUN_PAR_INDEX"         : {'cmd':0x30,  'length':2,     'blackbox': True,    'terminal': True, 'cyclic': False},                                      
    "GET_TIME_PAR_INDEX"        : {'cmd':0x32,  'length':2,     'blackbox': True,    'terminal': True, 'cyclic': False},
                              
    #aplikace => terminal : "actions"                                                  
    "COMM_SYNCHRONIZATION"      : {'cmd':0x01,  'length':0,     'blackbox': True,    'terminal': True},
    "CLEAR_DIAGNOSTIC"          : {'cmd':0x09,  'length':2,     'blackbox': True,    'terminal': False},
    "START_CALIBRATION_TIME"    : {'cmd':0x0C,  'length':0,     'blackbox': True,    'terminal': False},
    "END_CALIBRATION_TIME"      : {'cmd':0x0D,  'length':0,     'blackbox': True,    'terminal': False},
    "SET_CALIBRATION"           : {'cmd':0x0E,  'length':4,     'blackbox': True,    'terminal': False},                                                  
    "SET_BACKLIGHT"             : {'cmd':0x10,  'length':1,     'blackbox': False,   'terminal': True},                                      
    "SET_SPEAKER"               : {'cmd':0x11,  'length':3,     'blackbox': True,    'terminal': True},                                      
    "SET_TIME"                  : {'cmd':0x12,  'length':7,     'blackbox': True,    'terminal': True},                                      
    "SET_LANGUAGE"              : {'cmd':0x14,  'length':1,     'blackbox': False,   'terminal': True},                                      
    "SET_TIMING_SETTINGS"       : {'cmd':0x23,  'length':6,     'blackbox': True,    'terminal': True},                                      
    "CLEAR_DATABASE"            : {'cmd':0x34,  'length':0,     'blackbox': True,    'terminal': True},            
    "QUIT_TIMING"               : {'cmd':0x40,  'length':0,     'blackbox': True,    'terminal': True},
    "ENABLE_START_CELL"         : {'cmd':0x41,  'length':0,     'blackbox': False,   'terminal': True},
    "ENABLE_FINISH_CELL"        : {'cmd':0x42,  'length':0,     'blackbox': False,   'terminal': True},
    "GENERATE_STARTTIME"        : {'cmd':0x43,  'length':4,     'blackbox': True,    'terminal': True},
    "GENERATE_FINISHTIME"       : {'cmd':0x44,  'length':4,     'blackbox': True,    'terminal': True},                                                                                                    
    "SET_TAGS_READING"          : {'cmd':0x45,  'length':1,     'blackbox': True,    'terminal': False},                                                                                                    
    "GET_ACTUAL_RACE_TIME"      : {'cmd':0x46,  'length':4,     'blackbox': True,    'terminal': False}                                                                                                               
}
DEF_COMMAND_GROUP = {
                     
    "diagnostic": {
                   "development" : {'start':0 , 'count':10 },
                   "kernel"      : {'start':10, 'count':10 },
                   "uart"        : {'start':20, 'count':10 }
                   }                                       
}
DEF_ERRORS = {
                
    #terminal => aplikace
    "UNKNOWN_ERROR"             : 0x01,                                      
    "GENERAL_ERROR"             : 0x02,                                      
    "TIMING_COMMAND_NOT_VALID"  : 0x03,                                      
    "TIMING_COMMAND_NO_EFFECT"  : 0x04,                                      
    "CELL_NOT_ACTIVE"           : 0x05,
    "DATA_OUT_OF_RANGE"         : 0x06,
    "COMMAND_NOT_VALID"         : 0x07,
    "COMMAND_TIMEOUT"           : 0x08,
    "COMMAND_NO_EFFECT"         : 0x09,
    "RESPONSE_PENDING"          : 0x78        
}

def IsCyclic(key):
    if key == "GET_TIME_PAR_INDEX":
        return True
    elif key == "GET_RUN_PAR_INDEX":
        return True
    elif key == "GET_TIMING_SETTINGS":
        return True
    return False

def GetSorted(key='cmd'):
    return sorted(DEF_COMMANDS.iteritems(), key=lambda (x, y): y['cmd'])
def Get(index):
    return GetSorted()[index]     
        