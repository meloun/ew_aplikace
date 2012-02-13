# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

"""
definice DAT pro DATASTORE
 - přenos dat mezi gui a kommunikací
 - sekce:
     GET: data se pravidelně se obnovují z terminálu
          očekávané hodnoty:
              refresh_countdown - za jak dlouho se data obnoví z terminálu 
     SET: při změně se data nastavují do terminálu
          očekávané hodnoty:
              changed - hodnoty se změnili a čekají na odeslání do terminálu
     GET_SET: žádná akce mimo základní metody Datastore
"""
import sys
import time


eTIMING_LOGIC_MODE = ["basic", "manual"]

class LOGIC_MODES:
    basic, manual, single_mass, multiple_mass = range(1,5)  
    STRINGS =  {basic:"basic", manual:"manual"} 
class LANGUAGES:
    czech, english = range(0,2)  
    STRINGS =  {czech:"čeština", english:"english"}    
         

DEF_DATA = {
               
        # LOKÁLNÍ DATA (neposílájí se do terminálu)
        "port_enable"        : {"name"   : "Port enable",
                                "GET_SET"  : {"value": False}
                               },
        "port_name"          : {"name"   : "Port name",
                                "GET_SET"  : {"value": "COM3"}
                               },
        "port_baudrate"      : {"name"   : "Port baudrate",
                                "GET_SET"  : {"value": 38400}
                               },        

        # TERMINAL DATA
        "backlight"          : {"name"    : "backlight",                                                                 
                                "SET"     : {"value": 0x01, 
                                             "changed": True,                                             
                                             },
                               },
                
        "speaker"            : {"name"    : "speaker",                                                                 
                                "SET"     : {"value":{"keys": True, "timing": True, "system":True},
                                             "changed": True,                                             
                                             },
                               },                                                                                                       
        "datetime"           : {"name"    : "datetime",                                                                
                                "SET"     : {"value": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5},
                                             "changed": True},
                               },                                        
        "language"           : {"name"    : "language",                                
                                "SET"     : {"value": LANGUAGES.czech, "changed": False}, 
                               },                                               
        "terminal_info"      : {"name"    : "terminal info",
                                "GET"     : {"value": {"number_of_cells": None,
                                                       "battery": None,
                                                       "backlight":  None,
                                                       "speaker": {"keys": None, "timing": None, "system":None},
                                                       "language": None,
                                                       "datetime": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5}
                                                       },
                                             "refresh_countdown": 0                                              
                                             },
                               },
        "cell_info"          : {"name"    : "cell info", 
                                "GET"     : {"value": {"address": 10,
                                                       "baterry": 99,
                                                       "status":  {"new error": True,
                                                                   "cell on": True,
                                                                   "battery empty": True,
                                                                   "ping error": True,
                                                                   "ack error": True,
                                                                   "IR signal missinng": True},
                                                       },
                                             },
                               },
        "timing_settings"    : {"name"    : "timing info", 
                                "GET"     : {"value": {"logic mode": LOGIC_MODES.basic,
                                                       "baterry": 99,
                                                       "status":  {"new error": True,
                                                                   "cell on": True,
                                                                   "battery empty": True,
                                                                   "ping error": True,
                                                                   "ack error": True,
                                                                   "IR signal missinng": True},
                                                       },
                                             "refresh_countdown": 0 
                                             },                                
                                },                                                                                                
        }