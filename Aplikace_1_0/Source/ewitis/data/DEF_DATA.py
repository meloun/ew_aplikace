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
    nr_tabs = 15
    runs_times, users, categories, cgroups, tags, alltags, race_info, race_settings,\
    export_settings, device, cells, diagnostic, communication, manual, about = range(0, nr_tabs)
    NAME =  {runs_times:"RunsTimes", users:"Users", categories:"Categories", cgroups:"CGroups", \
              tags:"Tags", alltags:"Alltags", race_info:"RaceInfo", \
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
    
    POINTSCOLUMNS = 5
    TIMESCOLUMNS = 4
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
        "com_init"           : {"GET_SET"  : { "value"   : False},},                       
        "port"               : {"name"     : "port",
                                "GET_SET"  : {"value": {
                                                        "opened": False,
                                                        "enabled": True,
                                                        "name": "COM7",
                                                        "baudrate": 38400
                                                        }
                                              }
                               },
        "systemcheck"        : {"GET_SET"  : {"value": {
                                                        "wdg_comm": 0
                                                        }
                                              }
                                },
        "gui"                : {"GET_SET"  : {"value": {
                                                        "active_tab": 0,
                                                        "active_row": 0,
                                                        "update_requests":{
                                                                         "tableUsers":False,
                                                                         "tableTimes":False 
                                                                        }
                                                        }
                                              }
                               },
        #tab TIMES
        "times"                : {"GET_SET"  : {"value": {
                                                          "auto_number": 0,
                                                          "auto_refresh": 0,
                                                          "auto_www_refresh": 0
                                                         }
                                                }
                                  },        
        #tab RACE SETTINGS
        "race_time"          : {"GET_SET"  : { "value"   : 0},},        
        "current_run"        : {"GET_SET"  : { "value"   : 0},},
                
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
                                                                            "minute_timeformat" : CheckboxValue.unchecked,
                                                                         }] * NUMBER_OF.TIMESCOLUMNS,                                                                                                                 
                                                        "lap"           : [{
                                                                            "checked"           : CheckboxValue.checked,
                                                                            "filter"            : "",
                                                                            "fromlaststart"     : CheckboxValue.unchecked,
                                                                                       
                                                                         }] * NUMBER_OF.TIMESCOLUMNS,                                    
                                                        "order"         : [
                                                                           {
                                                                            "checked"            : CheckboxValue.checked,
                                                                            "type"               : "Total",
                                                                            "row"                : "Last times",
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
                                                        "sorted": [{"order1":1, "order2":2, "order3":3, 
                                                                    "nr":4, 
                                                                    "ordercat1":5, "ordercat2":6, "ordercat3":7, 
                                                                    "name":8, "category":9, "year":10, "club":11, "sex":12,
                                                                    "o1":13,"o2":14,"o3":15, "o4":16, 
                                                                    "gap":17, 
                                                                    "time1":18,"lap1":19,"time2":20,"lap2":21,"time3":22,"lap3":23, "time4":24,"lap4":25,
                                                                    "points1":26,"points2":27,"points3":28,"points4":29,"points5":30,
                                                                    "un1":31,"un2":32,"un3":33,
                                                                    "us1":34,"status":35
                                                                   }] * NUMBER_OF.EXPORTS,
                                                        "names":  {                                                
                                                                "order1"            : u"Pořadí",
                                                                "order2"            : u"Pořadí",
                                                                "order3"            : u"Pořadí",
                                                                "nr"                : u"Číslo", 
                                                                "ordercat1"         : u"Pořadí/Kategorie",
                                                                "ordercat2"         : u"Pořadí/Kategorie",
                                                                "ordercat3"         : u"Pořadí/Kategorie",
                                                                "name"              : u"Jméno", 
                                                                "category"          : u"Kategorie", 
                                                                "year"              : u"Rok", 
                                                                "club"              : u"Klub", 
                                                                "sex"               : u"Pohlaví", 
                                                                "o1"                : u"Option 1",
                                                                "o2"                : u"Option 2",
                                                                "o3"                : u"Option 3",
                                                                "o4"                : u"Option 4",
                                                                "gap"               : u"Ztráta",                                                                                                 
                                                                "time1"             : u"Čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap1"              : u"Kolo",
                                                                "time2"             : u"Čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap2"              : u"Kolo",
                                                                "time3"             : u"Čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap3"              : u"Kolo",                                                                                                                                  
                                                                "time4"             : u"Čas",                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap4"              : u"Kolo",                                                                                                                                  
                                                                "points1"           : u"Body",
                                                                "points2"           : u"Body", 
                                                                "points3"           : u"Body",
                                                                "points4"           : u"Body",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "points5"           : u"Body",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "un1"               : u"Un 1",
                                                                "un2"               : u"Un 2", 
                                                                "un3"               : u"Un 3",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "us1"               : u"Us 1",                                                                                                                                                                                                                                                                                                                                                                         
                                                                "status"            : u"Status"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                },
                                                        "enabled_csv":  [True]* NUMBER_OF.EXPORTS,                                                        
                                                        "enabled_htm":  [False]* NUMBER_OF.EXPORTS,                                                        
                                                        "checked": [{                                                                
                                                                "order1"            : CheckboxValue.checked,
                                                                "order2"            : CheckboxValue.checked,
                                                                "order3"            : CheckboxValue.checked,
                                                                "nr"                : CheckboxValue.checked,
                                                                "ordercat1"         : CheckboxValue.unchecked,
                                                                "ordercat2"         : CheckboxValue.unchecked,
                                                                "ordercat3"         : CheckboxValue.unchecked, 
                                                                "name"              : CheckboxValue.checked, 
                                                                "category"          : CheckboxValue.checked, 
                                                                "year"              : CheckboxValue.unchecked, 
                                                                "club"              : CheckboxValue.checked, 
                                                                "sex"               : CheckboxValue.unchecked, 
                                                                "o1"                : CheckboxValue.unchecked,
                                                                "o2"                : CheckboxValue.unchecked,
                                                                "o3"                : CheckboxValue.unchecked,
                                                                "o4"                : CheckboxValue.unchecked,
                                                                "gap"               : CheckboxValue.unchecked,                                                                                                      
                                                                "time1"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap1"              : CheckboxValue.unchecked, 
                                                                "time2"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap2"              : CheckboxValue.unchecked, 
                                                                "time3"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap3"              : CheckboxValue.unchecked,                                                         
                                                                "time4"             : CheckboxValue.checked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "lap4"              : CheckboxValue.unchecked,                                                         
                                                                "points1"           : CheckboxValue.unchecked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "points2"           : CheckboxValue.unchecked,
                                                                "points3"           : CheckboxValue.unchecked,
                                                                "points4"           : CheckboxValue.unchecked,
                                                                "points5"           : CheckboxValue.unchecked,
                                                                "un1"               : CheckboxValue.unchecked,                                                                                                                                                                                                                                                                                                                                                                          
                                                                "un2"               : CheckboxValue.unchecked,
                                                                "un3"               : CheckboxValue.unchecked,
                                                                "us1"               : CheckboxValue.unchecked,                                                                
                                                                "status"            : CheckboxValue.unchecked                                                                                                                                
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
        "export_header"      : {"permanent": True,
                                "GET_SET"  : {"value": [{
                                                "racename"               : u"%race%",
                                                "categoryname"           : u"%category%",                                                                                                                                                                                                                                                                                                                           
                                                "description"            : u"%description%"                                                                                                                                                                                                                                                                                                                           
                                                }] * NUMBER_OF.EXPORTS,                                              
                                              "changed": True
                                              }  
                                },
        "export_filtersort"  : {"permanent": True,
                                "GET_SET"  : {"value": [{
                                                        "onerow"             : CheckboxValue.unchecked,
                                                        "type"               : "total",
                                                        "filter"             : "last times with time1",
                                                        "sort1"              : "order1", 
                                                        "sortorder1"         : "asc",                                                                                                                                                                                                                                                                                                                            
                                                        "sort2"              : "- - -", 
                                                        "sortorder2"         : "asc",                                                                                                                                                                                                                                                                                                                            
                                                        }] * NUMBER_OF.EXPORTS,                                              
                                              "changed": True
                                              }  
                               },
        "export_www"         : {"permanent": True,
                                "GET_SET"  : {"value": [{
                                                "css_filename"           : u"css/results.css",                                                                                                                                                                                                                                                                                                                       
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
                                                        "app": "v3.15b"},                                                                                                                    
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
                                                           "task": None,
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
