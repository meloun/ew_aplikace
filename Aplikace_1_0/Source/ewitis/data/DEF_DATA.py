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
    CELLS = 14
    EXPORTS = 3
    
    POINTSCOLUMNS = 4
    THREECOLUMNS = 3
    OPTIONCOLUMNS = 4
    
def Assigments2Dict(assigment):                                            
        if assigment == "":            
            return None
        assigment = assigment.replace(" ", "") #mezery pryc
        
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
        #tab RACE SETTINGS
        "race_time"          : {"GET_SET"  : { "value"   : 0},},        
        #group timing setting: below
                                    
        #group timing setting: below
        "evaluation"         : {"permanent": True,
                                "GET_SET"  : {"value": {                                                         
                                                        "starttime": StarttimeEvaluation.VIA_USER, 
                                                        "finishtime": {"laps":0, "time":"00:00:00,00"}                                                                                                                                                                       
                                                        }
                                              }
                                },
            
        "racesettings-app"   : {"permanent": True,
                                "name": "race settings",
                                "GET_SET"  : {"value": {
                                                        "race_name"    :      u"Formula Student 2013",
                                                        "profile"      :      u"- - -",
                                                        "profile_desc" :      u"",
                                                        "remote"       :       CheckboxValue.unchecked,
                                                        "rfid"         :       CheckboxValue.unchecked,
                                                        "tag_filter"   :      CheckboxValue.unchecked,
                                                        },                                              
                                              "changed": True
                                      }
                                },
        "additional_info"    : {"name"     : "additinal info",
                                "permanent": True,
                                "GET_SET"  : {"value": {"status"        :{"checked"           : CheckboxValue.unchecked},
                                                        "time"          :[
                                                                          {                                                                     
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "rule"              : "time - starttime", 
                                                                            "filter"            : "cell=2|3|250",
                                                                         }] * NUMBER_OF.THREECOLUMNS,                                                                                                                 
                                                        "lap"           : [{
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "filter"            : "",           
                                                                         }] * NUMBER_OF.THREECOLUMNS,                                    
                                                        "order"         : [
                                                                           {
                                                                            "checked"            : CheckboxValue.checked,
                                                                            "type"               : "All",
                                                                            "row"                : "Lasttimes",
                                                                            "column1"            : "Time1",
                                                                            "order1"             : "Asc",                                                                                  
                                                                            "column2"            : " - - -",                                                                           
                                                                            "order2"             : "Asc"                                                                                  
                                                                          }] * NUMBER_OF.THREECOLUMNS,                                                                                                                                                                                                                                                                                                                           
                                                        "points"        :[
                                                                          {                                                                     
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "rule"              : "abs(time1 - %00:01:30,00%)", 
                                                                            "minimum"           : 0, 
                                                                            "maximum"           : 9999                                                                                                                                                                                                                                                                    
                                                                         }] * NUMBER_OF.POINTSCOLUMNS,
                                                        "un"            : [{"checked"           : CheckboxValue.checked}] * NUMBER_OF.THREECOLUMNS,
                                                        "us"            : [{"checked"           : CheckboxValue.checked}],                                                                                                                                                                
                                                        }
                                              }  
                               },
        "export"              : {"name"     : "export",
                                "permanent": True,                                
                                "GET_SET"  : {"value": {
                                                        "sorted": ["order1", "order2", "order3", "nr", "name", "category", "year", "club", "sex", "option1","option2","option3", "option4", "gap", "time1","lap1","time2","lap2","time3","lap3","points1","points2","points3","points4","un1","un2","un3","us1","status"],
                                                        "names":  {                                                
                                                                "order1"            : u"pořadí",
                                                                "order2"            : u"pořadí",
                                                                "order3"            : u"pořadí",
                                                                "nr"                : u"číslo", 
                                                                "name"              : u"jméno", 
                                                                "category"          : u"kategorie", 
                                                                "year"              : u"rok", 
                                                                "club"              : u"klub", 
                                                                "sex"               : u"pohlaví", 
                                                                "option1"           : u"option 1",
                                                                "option2"           : u"option 2",
                                                                "option3"           : u"option 3",
                                                                "option4"           : u"option 4",
                                                                "gap"               : u"ztráta",                                                                                                 
                                                                "time1"             : u"čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap1"              : u"kolo",
                                                                "time2"             : u"čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap2"              : u"kolo",
                                                                "time3"             : u"čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap3"              : u"kolo",                                                                                                                                  
                                                                "points1"           : u"body",
                                                                "points2"           : u"body", 
                                                                "points3"           : u"body",
                                                                "points4"           : u"body",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "un1"               : u"un 1",
                                                                "un2"               : u"un 2", 
                                                                "un3"               : u"un 3",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "us1"               : u"us 1",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "status"            : u"status",                                                                                                                                                                                                                                                                                                                                                                         
                                                                },
                                                        "enabled_csv":  [True]* NUMBER_OF.EXPORTS,                                                        
                                                        "enabled_htm":  [False]* NUMBER_OF.EXPORTS,                                                        
                                                        "checked": [{                                                                
                                                                "order1"            : CheckboxValue.checked,
                                                                "order2"            : CheckboxValue.checked,
                                                                "order3"            : CheckboxValue.checked,
                                                                "nr"                : CheckboxValue.checked, 
                                                                "name"              : CheckboxValue.checked, 
                                                                "category"          : CheckboxValue.checked, 
                                                                "year"              : CheckboxValue.unchecked, 
                                                                "club"              : CheckboxValue.checked, 
                                                                "sex"               : CheckboxValue.unchecked, 
                                                                "option1"           : CheckboxValue.unchecked,
                                                                "option2"           : CheckboxValue.unchecked,
                                                                "option3"           : CheckboxValue.unchecked,
                                                                "option4"           : CheckboxValue.unchecked,
                                                                "gap"               : CheckboxValue.unchecked,                                                                                                      
                                                                "time1"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap1"              : CheckboxValue.unchecked, 
                                                                "time2"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap2"              : CheckboxValue.unchecked, 
                                                                "time3"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap3"              : CheckboxValue.unchecked,                                                         
                                                                "points1"           : CheckboxValue.unchecked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "points2"           : CheckboxValue.unchecked,
                                                                "points3"           : CheckboxValue.unchecked,
                                                                "points4"           : CheckboxValue.unchecked,
                                                                "un1"               : CheckboxValue.unchecked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "un2"               : CheckboxValue.unchecked,
                                                                "un3"               : CheckboxValue.unchecked,
                                                                "us1"               : CheckboxValue.unchecked,                                                                
                                                                "status"            : CheckboxValue.unchecked,                                                                
                                                                }] * NUMBER_OF.EXPORTS
                                                        }
                                              }
                                },             
        "export_laps"        : {"name"     : "export_laps",
                                "permanent": True,
                                "GET_SET"  : {"value": {
                                                        "column"             : ExportLapsFormat.FORMAT_TIMES,                                                                                                                                                                                                                                                                                                                     
                                                        },                                              
                                              "changed": True
                                              }  
                               },
        "export_header"      : {"name"     : "export_filtersort",
                                "permanent": True,
                                "GET_SET"  : {"value": [{
                                                "racename"               : u"%race%",
                                                "categoryname"           : u"%category%",                                                                                                                                                                                                                                                                                                                           
                                                "description"            : u"%description%"                                                                                                                                                                                                                                                                                                                           
                                                }] * NUMBER_OF.EXPORTS,                                              
                                              "changed": True
                                              }  
                                },
        "export_filtersort"  : {"name"     : "export_filtersort",
                                "permanent": True,
                                "GET_SET"  : {"value": [{
                                                        "type"               : "total",
                                                        "filter"             : "last times",
                                                        "sort1"              : "order1", 
                                                        "sortorder1"         : "asc",                                                                                                                                                                                                                                                                                                                            
                                                        "sort2"              : "- - -", 
                                                        "sortorder2"         : "asc",                                                                                                                                                                                                                                                                                                                            
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
            
        # DATABASE"
        
        "count"              : {"GET_SET"  : {"value": {"Runs"          : 0,
                                                        "Times"         : 0},
                                              }
                                },  
        
        
        # TERMINAL DATA SET"              
        "synchronize_system" : {"SET"     : {"value": 0,
                                             "changed": False},
                               },
        "speaker"            : {"name"    : "speaker",                                                                 
                                "SET"     : {"value":{"keys": False, "timing": True, "system":True},
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
                                                        "app": "v3.05"},                                                                                                                    
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
                                "permanent": True, 
                                "GET"     : {"value": [                                                       
                                                       { #cell 1
                                                           "battery": None,
                                                           "ir_signal": None,
                                                           "active": None,
                                                           "synchronized_once": None,
                                                           "synchronized": None,
                                                           "address": index+1,
                                                           "task": 0,
                                                           "trigger": 0,
                                                           "diagnostic_long_ok":  0,
                                                           "diagnostic_long_ko":  0,
                                                           "diagnostic_short_ok": 0,
                                                           "diagnostic_short_ko": 0
                                                       } for index in range(NUMBER_OF.CELLS)                                              
                                                       ],
                                             "refresh_countdown": 0 ,
                                             },
                                "SET"     : {"value": [
                                                       {
                                                            "address": index+1,
                                                            "task": 0,
                                                            "trigger": 0,
                                                            "fu1": 0,
                                                            "fu2": 0,
                                                            "fu3": 0,
                                                            "fu4": 0
                                                       }for index in range(NUMBER_OF.CELLS)  ],
                                             "changed": False
                                             },
                               },
        "timing_settings"    : {"name"     : "timing_settings", 
                                "permanent": True,                                
                                "SET"      : {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 4,
                                                       "filter_tagtime": 5,
                                                       "filter_minlaptime": 60,
                                                       "filter_maxlapnumber": 0, 
                                                       "tags_reading_enable": None
                                                       },
                                              "changed": False
                                            },
                                "GET"      :  {"value": {"logic_mode": 1,
                                                       "measurement_state": MeasurementState.not_active,
                                                       "name_id": 04,
                                                       "filter_tagtime": None,
                                                       "filter_minlaptime": None,
                                                       "filter_maxlapnumber": None,
                                                       "tags_reading_enable": None
                                                       },
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
