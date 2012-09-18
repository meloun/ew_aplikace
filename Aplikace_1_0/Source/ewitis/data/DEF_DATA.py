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
    STRINGS =  {basic:"basic", manual:"manual", single_mass:"single_mass", multiple_mass:"multiple_mass"} 
class MEASUREMENT_STATE:
    not_active, prepared, time_is_running, finished = range(0,4)
    STRINGS =  {not_active:"Not Active", prepared:"Prepared, waiting for start", time_is_running:"Time is running", prepared:"Finished"}      
class LANGUAGES:
    czech, english = range(0,2)  
    STRINGS =  {czech:"čeština", english:"english"}
    
         

DEF_DATA = {
               
        # LOKÁLNÍ DATA (neposílájí se do terminálu)
        "app_version"        : {"GET_SET"  : {"value":u"v0.61"}},
        "port_enable"        : {"name"     : "Port enable",
                                "GET_SET"  : {"value": False}
                               },
        "port_name"          : {"name"     : "Port name",
                                "GET_SET"  : {"value": "COM5"}
                               },
        "port_baudrate"      : {"name"     : "Port baudrate",
                                "GET_SET"  : {"value": 38400}
                               },

        "active_tab"         : {"GET_SET"  : {"value":0}},
        
        #show flags for times table
        "show_alltimes"      : {"GET_SET"  : {"value": False}},
        "show_zerotimes"     : {"GET_SET"  : {"value": True}},
        "show_starttimes"    : {"GET_SET"  : {"value": True}},     
        
            
        "race_name"          : {"name"     : "race_name",
                                "GET_SET"  : {"value":u"Křápkap"}  
                               },        
        "rfid"               : {"name"     : "rfid",
                                "GET_SET"  : {"value":True}  
                               },
        "onelap_race"        : {"name"     : "onelap race",
                                "GET_SET"  : {"value": False}  
                               },
        "additinal_info"     : {"name"     : "additinal info",
                                "GET_SET"  : {"value": True}  
                               },
        "user_actions"       : {"name"     : "user_actions",
                                "GET_SET"  : {"value": 0}  
                               },
        "dir_import_csv"     : {"name"     : "dir_import_csv",
                                "GET_SET"  : {"value":"import/csv/"}  
                               },
        "dir_export_csv"     : {"name"     : "dir_export_csv",
                                "GET_SET"  : {"value":u"export/csv/"}  
                               },
        "dir_export_www"     : {"name"     : "dir_export_www",
                                "GET_SET"  : {"value":u"export/www/"}  
                               },
            
        

        # TERMINAL DATA
        "backlight"          : {"name"    : "backlight",                                                                 
                                "SET"     : {"value": 0x01, 
                                             "changed": False,                                             
                                             },
                               },
                
        "speaker"            : {"name"    : "speaker",                                                                 
                                "SET"     : {"value":{"keys": True, "timing": True, "system":True},
                                             "changed": False,                                             
                                             },
                               },                                                                                                       
        "datetime"           : {"name"    : "datetime",                                                                
                                "SET"     : {"value": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5},
                                             "changed": False},
                               },                                        
        "language"           : {"name"    : "language",                                
                                "SET"     : {"value": LANGUAGES.czech,
                                             "changed": False}, 
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
        "timing_settings"    : {"name"    : "logic timing_settings",                                
                                "SET"     : {"value": {"logic_mode": LOGIC_MODES.multiple_mass,
                                                       "measurement_state": MEASUREMENT_STATE.not_active,
                                                       "name_id": 4,
                                                       "filter_tagtime": 5,
                                                       "filter_minlaptime": 60,
                                                       "filter_maxlapnumber": 0,                                                       
                                                       },
                                              "changed": False
                                            },
                                "GET"     : {"value": {"logic_mode": LOGIC_MODES.multiple_mass,
                                                       "measurement_state": None,
                                                       "name_id": 04,
                                                       "filter_tagtime": None,
                                                       "filter_minlaptime": None,
                                                       "filter_maxlapnumber": None,                                                       
                                                       },
                                             "refresh_countdown": 0 
                                             },                                
                                },
        "generate_starttime" :  {"name"    : "generate starttime",                                                                 
                                "SET"     : { "value": False, 
                                              "changed": False,                                             
                                            },
                                },
        "generate_finishtime" : {"name"  : "generate finishtime",                                                                 
                                  "SET"   : { "value": False, 
                                              "changed": False,                                             
                                            },
                                },
        "quit_timing" :         {"name"  : "quit timing",                                                                 
                                  "SET"   : { "value": False, 
                                              "changed": False,                                             
                                            },
                                },
        }