# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

""" Komandy rozdělené do dvou sekcí GET a SET 
první byte z HW + první byte ze FW
- "Terminal 1" => terminál optika
- "Blackbox 1" => blackbox rfid
- "Blackbox 2" => nový blackbox, optika V2
- "Blackbox 3" => nový blackbox, rfid
"""

DEF_COMMANDS = {
                
    #terminal => aplikace : "states"                                                
    "GET_HW_SW_VERSION"         : {'cmd':0x04,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                      
    "GET_DIAGNOSTIC"            : {'cmd':0x08,  'length':2,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},                                      
    "GET_CALIBRATION_DATA"      : {'cmd':0x0F,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},                                      
    "GET_TERMINAL_INFO"         : {'cmd':0x20,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                      
    "GET_CELL_INFO"             : {'cmd':0x21,  'length':1,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,   'terminal': True},                                      
    "GET_TIMING_SETTINGS"       : {'cmd':0x22,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                      
    "GET_RUN_PAR_INDEX"         : {'cmd':0x30,  'length':2,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True, 'cyclic': False},                                      
    "GET_TIME_PAR_INDEX"        : {'cmd':0x32,  'length':2,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True, 'cyclic': False},
                              
    #aplikace => terminal : "actions"                                                  
    "COMM_SYNCHRONIZATION"      : {'cmd':0x01,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},
    "CLEAR_DIAGNOSTIC"          : {'cmd':0x09,  'length':2,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},
    "START_CALIBRATION_TIME"    : {'cmd':0x0C,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},
    "END_CALIBRATION_TIME"      : {'cmd':0x0D,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},
    "SET_CALIBRATION"           : {'cmd':0x0E,  'length':4,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},                                                  
    "SET_BACKLIGHT"             : {'cmd':0x10,  'length':1,     'Blackbox 2': False, 'Blackbox 3': False, 'Blackbox 1': False,   'terminal': True},                                      
    "SET_SPEAKER"               : {'cmd':0x11,  'length':3,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                      
    "SET_TIME"                  : {'cmd':0x12,  'length':7,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                      
    "SET_LANGUAGE"              : {'cmd':0x14,  'length':1,     'Blackbox 2': False, 'Blackbox 3': False, 'Blackbox 1': False,   'terminal': True},                                      
    "SET_TIMING_SETTINGS"       : {'cmd':0x23,  'length':6,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,    'terminal': True},                                      
    "SET_CELL_INFO"             : {'cmd':0x25,  'length':6,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,   'terminal': False},                                      
    "CLEAR_DATABASE"            : {'cmd':0x34,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},            
    "QUIT_TIMING"               : {'cmd':0x40,  'length':0,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},
    "ENABLE_START_CELL"         : {'cmd':0x41,  'length':0,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,   'terminal': True},
    "ENABLE_CELL"               : {'cmd':0x41,  'length':1,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,   'terminal': True},
    "ENABLE_FINISH_CELL"        : {'cmd':0x42,  'length':0,     'Blackbox 2': True,  'Blackbox 3': False, 'Blackbox 1': True,   'terminal': True},
    "GENERATE_STARTTIME"        : {'cmd':0x43,  'length':4,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},
    "GENERATE_FINISHTIME"       : {'cmd':0x44,  'length':4,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                                                                                    
    "SET_TAGS_READING"          : {'cmd':0x45,  'length':1,     'Blackbox 2': False, 'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},                                                                                                    
    "GET_ACTUAL_RACE_TIME"      : {'cmd':0x46,  'length':4,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': False},                                                                                                               
    "GET_CELL_LAST_TIME"        : {'cmd':0x47,  'length':1,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True},                                                                                                   
    "GENERATE_CELLTIME"         : {'cmd':0x48,  'length':5,     'Blackbox 2': True,  'Blackbox 3': True,  'Blackbox 1': True,    'terminal': True}
                                                                                                       
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

def GetSorted(key='cmd'):
    return sorted(DEF_COMMANDS.iteritems(), key=lambda (x, y): y['cmd'])
def Get(index):
    return GetSorted()[index]     
        