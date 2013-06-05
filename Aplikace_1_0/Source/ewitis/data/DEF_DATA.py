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

#class LOGIC_MODES:
#    basic, manual, single_mass, multiple_mass = range(1,5)  
#class MEASUREMENT_STATE:
class MeasurementState:
    not_active, prepared, time_is_running, finished = range(0,4) 
class Languages:
    CZECH, ENGLISH = range(0,2)    
class OrderEvaluation:
    RACE, SLALOM = range(0,2)    
    

DEF_DATA = {
               
        # LOKÁLNÍ DATA (neposílájí se do terminálu)        
        "port_enable"        : {"name"     : "Port enable",
                                "GET_SET"  : {"value": False}
                               },
        "port_name"          : {"name"     : "Port name",
                                "GET_SET"  : {"value": "COM5"}
                               },
        "port_baudrate"      : {"name"     : "Port baudrate",
                                "GET_SET"  : {"value": 38400}
                               },
        "communication_en"   : {"name"     : "Commucation Enabled",
                                "GET_SET"  : {"value": True}
                               },

        "active_tab"         : {"GET_SET"  : {"value":0}},
        "active_row"         : {"GET_SET"  : {"value":0}},
        
        
        #show flags for times table
        #"show_alltimes"      : {"GET_SET"  : {"value": 0}},        
        #"show_starttimes"    : {"GET_SET"  : {"value": 2}},     
        
            
        "race_name"          : {"name"     : "race_name",
                                "GET_SET"  : {
                                              "value":u"Fichtl Cup Dolce",
                                              "changed": True
                                              },
                                  
                               },        
        "run_time"           : {"GET_SET"  : {
                                              "value":0,
                                              "changed": True
                                              },                                  
                               },        
        "rfid"               : {"name"     : "rfid",
                                "GET_SET"  : {"value":2}  
                               },
        "tag_filter"         : {"GET_SET"  : {"value":2}},
        "order_evaluation"   : {"name"     : "order evaluation",
                                "GET_SET"  : {"value": OrderEvaluation.RACE}  
                               },
        "onelap_race"        : {"name"     : "onelap race",
                                "GET_SET"  : {"value": 0}  
                               },
        "download_from_last" : {"GET_SET"  : {"value": 0} },                   
        "times_view_limit"   : {"name"     : "times view limit",
                                "GET_SET"  : {"value": 0}  
                               },
        "show"               : {"GET_SET"  : {"value": {
                                                        "starttimes"       : 2, 
                                                        "times_with_order" : 0,                                                                                                      
                                                        "alltimes"         : 0
                                                        }
                                              }
                                },
        "additional_info"    : {"name"     : "additinal info",
                                "GET_SET"  : {"value": {"enabled"       : 0,
                                                        "order"         : 2,
                                                        "order_in_cat"  : 2,
                                                        "lap"           : 2,                                               
                                                        "laptime"       : 2,                                               
                                                        "best_laptime"  : 2,                                               
                                                        }
                                              }  
                               },
        "export"             : {"name"     : "export",
                                "GET_SET"  : {"value": {
                                                        "year"              : 2, 
                                                        "club"              : 2, 
                                                        "laps"              : 2, 
                                                        "best_laptime"      : 0,
                                                        "option_1"          : 0,
                                                        "option_2"          : 0,
                                                        "option_3"          : 0,
                                                        "option_4"          : 0,
                                                        "option_1_name"     : "o1",
                                                        "option_2_name"     : "o2",
                                                        "option_3_name"     : "o3",
                                                        "option_4_name"     : "o4",
                                                        "gap"               : 0,                                                                                                      
                                                        "points_race"            : 2,                                                                                                      
                                                        "points_categories" : 2,                                                                                                      
                                                        "points_groups"     : 2,                                                                                                                                                                                                                                                                    
                                                        },
                                              "changed": True
                                              }  
                               },         
        "user_actions"       : {"name"     : "user_actions",
                                "GET_SET"  : {"value": 0}  
                               },
        "directories"        : {"name"     : "directories",
                                "GET_SET"  : {"value": { 
                                                        "import"        :   u"import/",
                                                        "export"        :   u"export/",                                                        
                                                        "import_csv"    :   u"import/csv/",                                                
                                                        "export_csv"    :   u"export/csv/",                                               
                                                        "export_www"    :   u"export/www/"                                                
                                                        },
                                              },
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
        # DATABASE
        "count"              : {"GET_SET"  : {"value": {"Runs"          : 0,
                                                        "Times"         : 0                                                                                                       
                                                       }
                                              }
                                },  
        

        # TERMINAL DATA SET
        "backlight"          : {"name"    : "backlight",                                                                 
                                "SET"     : {"value": 0x01, 
                                             "changed": False,                                             
                                             },
                               },
                
        "speaker"            : {"name"    : "speaker",                                                                 
                                "SET"     : {"value":{"keys": False, "timing": True, "system":True},
                                             "changed": False,                                             
                                             },
                               },                                                                                                       
        "speaker2"           : {"name"    : "speaker",                                                                 
                                "SET"     : {"value": {"keys": False, "dict1a": {"dict2a":2, "dict2b":3}, "dict1b":3},
                                             "changed": False,                                             
                                             },
                               },                                                                                                       
        "datetime"           : {"name"    : "datetime",                                                                
                                "SET"     : {"value": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5},
                                             "changed": False},
                               },                                        
        "language"           : {"name"    : "language",                                
                                "SET"     : {"value": Languages.CZECH,
                                             "changed": False}, 
                               },
            
        # TERMINAL DATA GET
            
        "versions"           : {"name"    : "versions",                                                                 
                                "GET_SET" : {"value": { "hw" : None,
                                                        "fw" : None,
                                                        "app": "v1.14"
                                                       },                                                                                                                    
                                             },
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
                                "SET"     : {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 4,
                                                       "filter_tagtime": 5,
                                                       "filter_minlaptime": 60,
                                                       "filter_maxlapnumber": 0, 
                                                       "tags_reading_enable": None,                                                      
                                                       },
                                              "changed": False
                                            },
                                "GET"    :  {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 04,
                                                       "filter_tagtime": None,
                                                       "filter_minlaptime": None,
                                                       "filter_maxlapnumber": None,
                                                       "tags_reading_enable": None,                                                       
                                                       },
                                             "refresh_countdown": 0 
                                             },                                
                                },
        "remove_hw_time"      : { "SET"  : { "value": 0,        #0 or id for removing 
                                             "changed": False,                                             
                                           },
                                },  
        "enable_startcell"    : { "SET"  : { "value": False, 
                                              "changed": False,                                             
                                           },
                               },
        "enable_finishcell"   : { "SET"  : { "value": False, 
                                            "changed": False,                                             
                                           },
                               },
        "generate_starttime"  : {"name"  : "generate starttime",                                                                 
                                 "SET"   : { "value": False, 
                                              "changed": False,                                             
                                           },
                                },
        "generate_finishtime" : {"name"  : "generate finishtime",                                                                 
                                 "SET"   : { "value"   : False, 
                                              "changed": False,                                             
                                           },
                                },
        "quit_timing"         : {"name"  : "quit timing",                                                                 
                                 "SET"   : { "value"   : False, 
                                              "changed": False,                                             
                                           },
                                },
        "clear_database"      : {"name"  : "clear database",                                                                 
                                 "SET"   : { "value"   : False, 
                                             "changed" : False,                                             
                                           },
                                },
        "tags_reading"        : {"name"  : "disable scan tags",                                                                 
                                 "SET"   : { "value"  : False, 
                                              "changed": False,                                             
                                           },
                                },
        }