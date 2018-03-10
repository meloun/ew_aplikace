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
    "CLEAR_DATABASE"            : {'cmd':0x34,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },            
    "QUIT_TIMING"               : {'cmd':0x40,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "ENABLE_START_CELL"         : {'cmd':0x41,  'length-tx':0,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "ENABLE_CELL"               : {'cmd':0x41,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "DISABLE_CELL"              : {'cmd':0x42,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': False  },
    "GENERATE_STARTTIME"        : {'cmd':0x43,  'length-tx':4,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "GENERATE_FINISHTIME"       : {'cmd':0x44,  'length-tx':4,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },                                                                                                    
    "SET_TAGS_READING"          : {'cmd':0x45,  'length-tx':1,  'length-rx':0,  'Blackbox-IR': False, 'Blackbox-RFID': True   },                                                                                                    
    "GENERATE_CELLTIME"         : {'cmd':0x48,  'length-tx':5,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   },
    "DIAGNOSTIC_COMMAND"        : {'cmd':0xFF,  'length-tx':5,  'length-rx':0,  'Blackbox-IR': True,  'Blackbox-RFID': True   }
                                                                                                       
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
        