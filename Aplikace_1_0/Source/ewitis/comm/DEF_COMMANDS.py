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
    "GET_HW_SW_VERSION"         : {'cmd':0x04,  'length-tx':0,  'length-rx':8,   'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "GET_DIAGNOSTIC"            : {'cmd':0x08,  'length-tx':2,  'length-rx':255, 'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "GET_CALIBRATION_DATA"      : {'cmd':0x0F,  'length-tx':0,  'length-rx':7,   'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "GET_TERMINAL_INFO"         : {'cmd':0x20,  'length-tx':0,  'length-rx':12,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                        
    "GET_CELL_INFO"             : {'cmd':0x21,  'length-tx':1,  'length-rx':17,  'Blackbox-IR': True,  'Blackbox-RFID': False  },                                      
    "GET_TIMING_SETTINGS"       : {'cmd':0x22,  'length-tx':0,  'length-rx':8,   'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "GET_CELL_OVERVIEW"         : {'cmd':0x29,  'length-tx':0,  'length-rx':24,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "GET_DEVICE_OVERVIEW"       : {'cmd':0x2A,  'length-tx':0,  'length-rx':16,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "GET_CELL_VERSION"          : {'cmd':0x2D,  'length-tx':1,  'length-rx':4,   'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "GET_RUN_PAR_INDEX"         : {'cmd':0x30,  'length-tx':2,  'length-rx':18,  'Blackbox-IR': True,  'Blackbox-RFID': True,  'cyclic': False},                                      
    "GET_TIME_PAR_INDEX"        : {'cmd':0x32,  'length-tx':2,  'length-rx':18,  'Blackbox-IR': True,  'Blackbox-RFID': True,  'cyclic': False},
    "GET_ACTUAL_RACE_TIME"      : {'cmd':0x46,  'length-tx':0,  'length-rx':4,   'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                                               
    "GET_CELL_LAST_TIME"        : {'cmd':0x47,  'length-tx':1,  'length-rx':0,   'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                                   
                                                         
    #aplikace => terminal : "actions"                                              
    "COMM_SYNCHRONIZATION"      : {'cmd':0x01,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "CLEAR_DIAGNOSTIC"          : {'cmd':0x09,  'length-tx':2,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "START_CALIBRATION_TIME"    : {'cmd':0x0C,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "END_CALIBRATION_TIME"      : {'cmd':0x0D,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "SET_CALIBRATION"           : {'cmd':0x0E,  'length-tx':4,  'length-rx':9,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                            
    "SET_SPEAKER"               : {'cmd':0x11,  'length-tx':3,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "SET_DATETIME"              : {'cmd':0x12,  'length-tx':7,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                
    "SET_TIMING_SETTINGS"       : {'cmd':0x23,  'length-tx':6,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "SYNCHRONIZE_SYSTEM"        : {'cmd':0x24,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                      
    "SET_CELL_INFO"             : {'cmd':0x25,  'length-tx':6,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },                                      
    "SET_CELL_DIAG_INFO"        : {'cmd':0x26,  'length-tx':7,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },                                      
    "PING_CELL"                 : {'cmd':0x27,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },                                      
    "RUN_CELL_DIAGNOSTIC"       : {'cmd':0x28,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },                                      
    "CLEAR_MISSING_TIMES"       : {'cmd':0x2C,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "CLEAR_DATABASE"            : {'cmd':0x34,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },            
    "QUIT_TIMING"               : {'cmd':0x40,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "ENABLE_START_CELL"         : {'cmd':0x41,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "ENABLE_CELL"               : {'cmd':0x41,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "DISABLE_CELL"              : {'cmd':0x42,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "GENERATE_STARTTIME"        : {'cmd':0x43,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "GENERATE_FINISHTIME"       : {'cmd':0x44,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                                    
    "SET_TAGS_READING"          : {'cmd':0x45,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': False, 'Blackbox-RFID': True   },                                                                                                    
    "GENERATE_CELLTIME"         : {'cmd':0x48,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "DIAGNOSTIC_COMMAND"        : {'cmd':0xFF,  'length-tx':5,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   }
                                                                                                       
}
DEF_COMMAND_GROUP = {
                     
    "diagnostic": {
                   "group_0_32"   : {'start':0x00 , 'count':0x20 },
                   "group_33_64"  : {'start':0x20 , 'count':0x20 },
                   "group_65_96"  : {'start':0x40 , 'count':0x20 },
                   "group_97_128" : {'start':0x60 , 'count':0x20 }
                   }                                       
}

DIAGNOSTICS_DESCRIPTION = [
    "Development error 0                                        ", 
    "Development error 1                                        ",
    "Development error 2                                        ",
    "Development error 3                                        ",
    "Development error 4                                        ",
    "Development error 5                                        ",
    "Development error 6                                        ",
    "Development error 7                                        ",
    "Development error 8                                        ",
    "Development error 9                                        ",
    "Development error 10                                       ",
    "Development error 11                                       ",
    "Development error 12                                       ",
    "Development error 13                                       ",
    "Development error 14                                       ",
    "Development error 15                                       ",
    "Kernel - too many processes                                ",
    "Kernel - CPU overload                                      ", 
    "Not used                                                   ", 
    "Not used                                                   ",
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",   
    "Calibration - Error top                                    ",
    "Calibration - Error bottom                                 ", 
    "Calibration - Data out of range                            ", 
    "Not used                                                   ",   
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",
    "UART0 buffer overflow                                      ", 
    "UART1 buffer overflow                                      ", 
    "UART2 buffer overflow                                      ",
    "UART3 buffer overflow                                      ",
    "UART0 response timeout                                     ", 
    "UART1 response timeout                                     ",
    "UART2 response timeout                                     ", 
    "UART3 response timeout                                     ",
    "UART0 continuity timeout                                   ", 
    "UART1 continuity timeout                                   ", 
    "UART2 continuity timeout                                   ",  
    "UART3 continuity timeout                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Application sends too many bytes                           ",
    "BB was not able to do command from APP in max given time   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",   
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "New time beep not executed due to too many requests        ",   
    "System beep not executed due to too many requests          ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Led flash not executed due to too many requests            ", 
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",   
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",   
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Not used                                                   ",
    "Not used                                                   ",
    "Missing time lost due to too many missing time of one cell ", 
    "Missing time index out of possible range                   ", 
    "Missing times lost due to reinit of missing times buffer   ",   
    "New time received, but set as confirmed by cell            ",
    "Missing time index was lost by cell                        ", 
    "Not used                                                   ", 
    "Not used                                                   ",   
    "Not used                                                   ",
    "Database buffer of operation full                          ", 
    "Database is full                                           ", 
    "New time lost                                              ",
    "Database not erased, request lost                          ", 
    "Time ID read out from EEPROM is suspicious                 ", 
    "Time ID read out from database is suspicious               ",
    "Not used                                                   ",
    "Not used                                                   ", 
    "WL buffers full                                            ", 
    "WL Tx data lost - no buffer free                           ",   
    "WL Rx data lost - no buffer free                           ",
    "WL some data lost - overwritten by new data                ", 
    "WL Rx data wrong checksum                                  ", 
    "WL no acknowledge on command                               ",   
    "Not used                                                   ",
    "Not used                                                   ", 
    "WL unkown command                                          ", 
    "WL ilegal command for BB received                          ",
    "WL unkown response                                         ",
    "WL ilegal response for BB received                         ", 
    "Not used                                                   ",
    "Not used                                                   ",
    "Not used                                                   ", 
    "Not used                                                   ", 
    "Getting from RTC failed                                    ",
    "Setting of RTC failed                                      ",
    "Not used                                                   ",                                            
]

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

def SetDiagnosticCommand(cmd = None, length = None):
    if(cmd != None):
        DEF_COMMANDS["DIAGNOSTIC_COMMAND"]["cmd"] = cmd    
    if(length != None):
        DEF_COMMANDS["DIAGNOSTIC_COMMAND"]["length"] = length
       
def GetSorted(key = 'cmd'):
    return sorted(DEF_COMMANDS.iteritems(), key = lambda (x, y): y['cmd'])
def Get(index):
    return GetSorted()[index]
def GetParCmd(cmd):
    for k,v in DEF_COMMANDS.iteritems():
        if v['cmd'] == cmd:
            return  (k, DEF_COMMANDS[k])
    return None 
        
        
if __name__ == "__main__":
    print GetParCmd(0x41) 
    print GetParCmd(0x41)[1]['length-tx'] 
    print Get(2)      
        