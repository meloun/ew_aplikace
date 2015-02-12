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

#'''čísla záložek v TAB widgetu'''
class TAB:
    nr_tabs = 16
    runs_times, users, categories, cgroups, tags, alltags, points, race_info, race_settings,\
    export_settings, device, cells, diagnostic, communication, manual, about = range(0, nr_tabs)
    NAME =  {runs_times:"RunsTimes", users:"Users", categories:"Categories", cgroups:"CGroups", \
              tags:"Tags", alltags:"Alltags", points:"Points", race_info:"RaceInfo", \
              race_settings:"RaceSettings",  export_settings:"ExportSettings", device:"Device", cells: "Cells",\
              diagnostic: "Diagnostic", communication: "Communication",  \
              manual: "Manual", about: "About",    \
            }
class MeasurementState:
    not_active, prepared, time_is_running, finished = range(0,4) 
class Languages:
    CZECH, ENGLISH = range(0,2)    
class OrderEvaluation:
    RACE, SLALOM = range(0,2)    
class StarttimeEvaluation:
    VIA_CATEGORY, VIA_USER = range(0,2) 
class LaptimeEvaluation:
    ONLY_FINISHTIME, ALL_TIMES = range(0,2) 
class ExportLapsFormat:
    FORMAT_TIMES, FORMAT_LAPTIMES, FORMAT_POINTS_1, FORMAT_POINTS_2, FORMAT_POINTS_3 = range(0,5) 
class PointsEvaluation:
    FROM_TABLE, FROM_FORMULA = range(0,2) 
class CheckboxValue:
    unchecked, undefined, checked = range(0,3) 
    
        
    

class NUMBER_OF:
    CELLS = 10
    EXPORTS = 3
    
    POINTSCOLUMNS = 3
    THREECOLUMNS = 3
    OPTIONCOLUMNS = 4
    
def Assigments2Dict(assigment):                                            
        if assigment == "":            
            return None
        
        try:
            assigment_dict = dict([item.split("=") for item in assigment.split(";")])            
        except ValueError:
            assigment_dict = None            
            
        return assigment_dict    


DEF_DATA = {
               
        
        # LOKÁLNÍ DATA (neposílájí se do terminálu)                       
        "port"               : {"name"     : "port",
                                "GET_SET"  : {"value": {
                                                        "opened": False,
                                                        "enabled": True,
                                                        "name": "COM8",
                                                        "baudrate": 38400
                                                        }
                                              }
                               },
        "gui"                : {"GET_SET"  : {"value": {
                                                        "active_tab": 0,
                                                        "active_row": 0
                                                        }
                                              }
                               },        
        #tab Race Info
        "race_info"          : {"GET_SET"  : {"value": {
                                                "limit_laps"      : 1, 
                                                "limit_time"      : {"hours"             :99,
                                                                     "minutes"           :59,
                                                                     "seconds"           :59,
                                                                     "milliseconds_x10"  :99
                                                                      }                                               
                                                }
                                      }
                        },
            
        #tab RACE SETTINGS
        "race_time"          : {"GET_SET"  : { "value"   : 0},},        
        #group timing setting: below
                                    
        #group timing setting: below
        "evaluation"         : {"permanent": True,
                                "GET_SET"  : {"value": {                                                         
                                                        "starttime": StarttimeEvaluation.VIA_CATEGORY,                                                                                                                                                                        
                                                        }
                                              }
                                },
            
        "racesettings-app"   : {"permanent": True,
                                "GET_SET"  : {"value": {
                                                        "race_name"  :      u"Formula Student 2013",
                                                        "remote"    :       CheckboxValue.unchecked,
                                                        "rfid"      :       CheckboxValue.unchecked,
                                                        "tag_filter" :      CheckboxValue.unchecked,
                                                        },
                                              "changed": True
                                      }
                                },
        "download_from_last" : {"GET_SET"  : {"value": 0} },                   
        "times_view_limit"   : {"name"     : "times view limit",
                                "GET_SET"  : {"value": 0}  
                               },
        "show"               : {"GET_SET"  : {"value": {                                                         
                                                        "times_with_order" : CheckboxValue.unchecked,                                                                                                      
                                                         #"alltimes"         : CheckboxValue.unchecked
                                                        }
                                              }
                                },
        "additional_info"    : {"name"     : "additinal info",
                                "permanent": True,
                                "GET_SET"  : {"value": {"time"          :[
                                                                          {                                                                     
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "rule"              : "time - starttime", 
                                                                            "filter"            : "cell250",
                                                                         }] * NUMBER_OF.THREECOLUMNS,                                                                                                                 
                                                        "lap"           : [{
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "filter"            : "",           
                                                                         }] * NUMBER_OF.THREECOLUMNS,                                    
                                                        "order"         : [
                                                                           {
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "column1"            : "Time1",
                                                                            "row1"               : "Last",
                                                                            "order1"             : "Asc",                                                                                  
                                                                            "column2"            : " - - -",
                                                                            "row2"               : "last",
                                                                            "order2"             : "Asc"                                                                                  
                                                                          }] * NUMBER_OF.THREECOLUMNS,                                                                                                                                                                                                                                                                                                                           
                                                        "points"        :[
                                                                          {                                                                     
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "rule"              : "abs(timeraw - %00:01:30,00%)", 
                                                                            "minimum"           : 0, 
                                                                            "maximum"           : 500                                                                                                                                                                                                                                                                    
                                                                         }] * NUMBER_OF.POINTSCOLUMNS,
                                                        "un"            : [{"checked"           : CheckboxValue.checked}] * NUMBER_OF.THREECOLUMNS,
                                                        "us"            : [{"checked"           : CheckboxValue.checked}],                                                                                                                                                                
                                                        }
                                              }  
                               },
        "export"             : {"name"     : "export",
                                "permanent": True,
                                "GET_SET"  : {"value": [{
                                                        "order"             : [CheckboxValue.checked] * NUMBER_OF.OPTIONCOLUMNS,
                                                        "number"            : CheckboxValue.checked, 
                                                        "name"              : CheckboxValue.checked, 
                                                        "category"          : CheckboxValue.checked, 
                                                        "year"              : CheckboxValue.unchecked, 
                                                        "club"              : CheckboxValue.checked, 
                                                        "sex"               : CheckboxValue.unchecked, 
                                                        "option"            : [CheckboxValue.unchecked] * NUMBER_OF.OPTIONCOLUMNS,
                                                        "optionname"        : ["optionname"] * NUMBER_OF.OPTIONCOLUMNS,
                                                        "gap"               : CheckboxValue.unchecked,                                                                                                      
                                                        "points"            : [CheckboxValue.unchecked] * NUMBER_OF.OPTIONCOLUMNS,                                                                                                                                                                                                                                                                                                                                                                          
                                                        "times"             : [CheckboxValue.checked] * NUMBER_OF.OPTIONCOLUMNS,                                                                                                                                                                                                                                                                                                                                                                          
                                                        "laps"              : CheckboxValue.unchecked                                                                                                                                                                                                                                                                                                                            
                                                        }] * NUMBER_OF.EXPORTS,
                                              "changed": True
                                              }  
                               },
        "diagnostic"         : {"GET_SET"  : {"value": {
                                                        "sendcommandkey": None,
                                                        "senddata": 0,
                                                        "sendresponse": "",
                                                        "communication": "",
                                                        "log_cyclic": 0,
                                                        "no_new_run_cnt": 0,
                                                        "no_new_time_cnt": 0,
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
#         "dir_import_csv"     : {"name"     : "dir_import_csv",
#                                 "GET_SET"  : {"value":  u"import/csv/"}  
#                                },
#         "dir_export_csv"     : {"name"     : "dir_export_csv",
#                                 "GET_SET"  : {"value":  u"export/csv/"}  
#                                },
#         "dir_export_www"     : {"name"     : "dir_export_www",
#                                 "GET_SET"  : {"value":  u"export/www/"}  
#                                },
            
        # DATABASE"
        
        "count"              : {"GET_SET"  : {"value": {"Runs"          : 0,
                                                        "Times"         : 0},
                                              }
                                },  
        
        
        # TERMINAL DATA SET"              
        "synchronize_system" : {"SET"     : {"value": 0,
                                             "changed": False},
                               },                                                                                                                                                                                                             
                                                                                 
        "datetime"           : {"name"    : "datetime",                                                                
                                "SET"     : {"value": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5},
                                             "changed": False},
                               },

            
        
        # TERMINAL DATA GET"
            
        "versions"           : {"name"    : "versions",                                                                 
                                "GET_SET" : {"value": { "hw" : None,
                                                        "fw" : None,
                                                        "app": "v3.00"},                                                                                                                    
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
        "cells_info"         : {"name"    : "cells info", 
                                "GET"     : {"value": [                                                       
                                                       { #cell 1
                                                           "battery": None,
                                                           "ir_signal": None,
                                                           "active": None,
                                                           "synchronized_once": None,
                                                           "synchronized": None,
                                                           "address": 1,
                                                           "task": 0,
                                                           "diagnostic_long_ok":  0,
                                                           "diagnostic_long_ko":  0,
                                                           "diagnostic_short_ok": 0,
                                                           "diagnostic_short_ko": 0
                                                       }                                              
                                                       ] * NUMBER_OF.CELLS,
                                             "refresh_countdown": 0 ,
                                             },
                                "SET"     : {"value": [
                                                       { #cell 1-2
                                                            "address": None,
                                                            "task": 0,
                                                            "fu1": None,
                                                            "fu2": None,
                                                            "fu3": None,
                                                            "fu4": None
                                                       }] * NUMBER_OF.CELLS,
                                             "changed": False
                                             },
                               },
        "timing_settings"    : {"name"    : "logic timing_settings",                                
                                "SET"     : {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 4,
                                                       "filter_tagtime": 5,
                                                       "filter_minlaptime": 60,
                                                       "filter_maxlapnumber": 0, 
                                                       "tags_reading_enable": None},
                                              "changed": False
                                            },
                                "GET"    :  {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 04,
                                                       "filter_tagtime": None,
                                                       "filter_minlaptime": None,
                                                       "filter_maxlapnumber": None,
                                                       "tags_reading_enable": None},
                                             "refresh_countdown": 0 
                                             },                                
                                },
        "remove_hw_time"      : { "SET"  : { "value": 0, 
                                             "changed": False},
                                 },  
        #address actions
        "set_cell_diag_info"  : { "SET"  : { "value": { "address": 0,
                                                        "diagnostic_long_ok":  0,
                                                        "diagnostic_long_ko":  0,
                                                        "diagnostic_short_ok": 0,
                                                        "diagnostic_short_ko": 0
                                                       },
                                             "changed": False}
                                 },
        "ping_cell"           : { "SET"  : { "value": 0, "changed": False}},
        "run_cell_diagnostic" : { "SET"  : { "value": 0, "changed": False}},
                                         
        #task actions
        "get_cell_last_times" : { "SET"  : { "value": 0, "changed": False}},                                
        "enable_cell"         : { "SET"  : { "value": 0, "changed": False}},
        "disable_cell"        : { "SET"  : { "value": 0, "changed": False}},
        "generate_celltime"  : { "SET"   : { "value": {'task':0, 'user_id':0}, 
                                             "changed": False},
                                },                        
        "quit_timing"         : {"name"  : "quit timing",                                                                 
                                 "SET"   : { "value"   : False, 
                                             "changed": False},
                                 },
        "clear_database"      : {"name"  : "clear database",                                                                 
                                 "SET"   : { "value"   : False, 
                                             "changed" : False},
                                 },
        "tags_reading"        : {"name"  : "disable scan tags",                                                                 
                                 "SET"   : { "value"  : False, 
                                             "changed": False},
                                 },
        }
