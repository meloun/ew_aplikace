# -*- coding: utf-8 -*-
'''

Created on 27.12.2011

@author: Meloun
'''

""" WIDTHS """
WIDTH_NUMBER_4DIGIT = 50
WIDTH_NUMBER_3DIGIT = 40

"""
RUNS
"""
RUNS = {}

""" table collumns """
RUNS['table'] = { 
                 "id"            :     {"index": 0,  "name": "id",          "default": 0,                       "width": WIDTH_NUMBER_4DIGIT,   "write": False},                                
                 #"date"          :     {"index": 1,  "name": "date",        "default": "0.0. 2000 00:00:00",    "width": 70,                    "write": True},                                                 
                 #"description"   :     {"index": 2,  "name": "description", "default": "",                      "width": 10,                    "write": True}                                
                 }  

"""
TIMES
"""
TIMES = {}
        
                         

""" table collumn for times, mode race """
TIMES['table'] =   {
                           "id"           : {"index": 0,  "name": "id",         "name_cz": u"id",       "type":"number",    "default": 0,           "width": WIDTH_NUMBER_4DIGIT,    "write":False  },                           
                           "nr"           : {"index": 1,  "name": "nr",         "name_cz": u"Číslo",    "type":"number",    "default": 0,           "width": WIDTH_NUMBER_4DIGIT,    "write":True  },
                           "cell"         : {"index": 2,  "name": "cell",       "name_cz": u"Buňka",                        "default": 250,         "width": 35,                     "write":True  },
                           "status"       : {"index": 3,  "name": "status",     "name_cz": u"Status",                       "default": "race",      "width": 60,                     "write":True  },                           
                           "time1"        : {"index": 4,  "name": "time1",      "name_cz": u"Čas1",                         "default": "",          "width": 80,                     "write":False  },                           
                           "lap1"         : {"index": 5,  "name": "lap1",       "name_cz": u"Okruhy1",                      "default": "",          "width": 50,                     "write":False  },
                           "time2"        : {"index": 6,  "name": "time2",      "name_cz": u"Čas2",                         "default": "",          "width": 80,                     "write":False  },
                           "lap2"         : {"index": 7,  "name": "lap2",       "name_cz": u"Okruhy2",                      "default": "",          "width": 50,                     "write":False  },
                           "time3"        : {"index": 8,  "name": "time3",      "name_cz": u"Čas3",                         "default": "",          "width": 80,                     "write":False  },
                           "lap3"         : {"index": 9,  "name": "lap3",       "name_cz": u"Okruhy3",                      "default": "",          "width": 50,                     "write":False  },
                           "time4"        : {"index": 10, "name": "time4",      "name_cz": u"Čas4",                         "default": "",          "width": 80,                     "write":False  },
                           "lap4"         : {"index": 11, "name": "lap4",       "name_cz": u"Okruhy4",                      "default": "",          "width": 50,                     "write":False  },
                           "name"         : {"index": 12, "name": "name",       "name_cz": u"Jméno",                        "default": "unknow",    "width": 200,                    "write":False  },
                           "category"     : {"index": 13, "name": "category",   "name_cz": u"Kategorie",                    "default": "unknown",   "width": 100,                    "write":False  },
                           "order1"       : {"index": 14, "name": "order1",     "name_cz": u"Pořadí1",  "type":"number",    "default": "",          "width": 60,                     "write":False  },                                 
                           "order2"       : {"index": 15, "name": "order2",     "name_cz": u"Pořadí2",  "type":"number",    "default": "",          "width": 60,                     "write":False  },
                           "order3"       : {"index": 16, "name": "order3",     "name_cz": u"Pořadí3",  "type":"number",    "default": "",          "width": 60,                     "write":False  },                                 
                           "start_nr"     : {"index": 17, "name": "start",      "name_cz": u"Start",                        "default": 1,           "width": 50,                     "write":False  },                                                                                                                                                                                                                                                                                                               
                           "points1"      : {"index": 18, "name": "points1",    "name_cz": u"Body",     "type":"number",    "default": "",          "width": 60,                     "write":False  },                                                                                                                                                                              
                           "points2"      : {"index": 19, "name": "points2",    "name_cz": u"Body",     "type":"number",    "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           "points3"      : {"index": 20, "name": "points3",    "name_cz": u"Body",     "type":"number",    "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           "points4"      : {"index": 21, "name": "points4",    "name_cz": u"Body",     "type":"number",    "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           "points5"      : {"index": 22, "name": "points5",    "name_cz": u"Body",     "type":"number",    "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           "un1"          : {"index": 23, "name": "un1",        "name_cz": u"un1",                          "default": "",          "width": WIDTH_NUMBER_3DIGIT,    "write":True  },                                                                                                     
                           "un2"          : {"index": 24, "name": "un2",        "name_cz": u"un2",                          "default": "",          "width": WIDTH_NUMBER_3DIGIT,    "write":True  },                                                                                                     
                           "un3"          : {"index": 25, "name": "un3",        "name_cz": u"un3",                          "default": "",          "width": WIDTH_NUMBER_3DIGIT,    "write":True  },                                                                                                     
                           "us1"          : {"index": 26, "name": "us1",        "name_cz": u"us1",                          "default": "",          "width": 80,                     "write":True  },                                                                                                     
                           "state"        : {"index": 27, "name": "state",      "name_cz": u"state",                        "default": "",          "width": 80,                     "write":False },
                           #!! nedavat 'time_raw' => stejne jmeno s tabulkou a kreje se
                           "timeraw"      : {"index": 28, "name": "timeraw",      "name_cz": u"Čas Raw",                    "default": 161,         "width": 120,                    "write":True  },                        
                        
                        }
"""
USERS
"""
USERS = {}


""" table collumns """
USERS['table'] = { "id"            :     {"index": 0,   "name": "id",           "name_cz": u"id",        "default": 0,           "width": WIDTH_NUMBER_4DIGIT,   "write":False },                   
                   "nr"            :     {"index": 1,   "name": "nr",           "name_cz": u"Číslo",     "default": 0,           "width": WIDTH_NUMBER_4DIGIT,   "write":True },
                   "status"        :     {"index": 2,   "name": "status",       "name_cz": u"Status",    "default": "race",      "width": WIDTH_NUMBER_4DIGIT,   "write":True },
                   "name"          :     {"index": 3,   "name": "name",         "name_cz": u"Jméno",     "default": "unknown",   "width": 100,                   "write":True },                
                   "first_name"    :     {"index": 4,   "name": "first_name",   "name_cz": u"Nevím",     "default": "unknown",   "width": 100,                   "write":True },
                   "category"      :     {"index": 5,   "name": "category",     "name_cz": u"Kategorie", "default": "unknown",   "width": 100,                   "write":True },                   
                   "club"          :     {"index": 6,   "name": "club",         "name_cz": u"Klub",      "default": "",          "width": 200,                   "write":True },
                   "year"          :     {"index": 7,   "name": "year",         "name_cz":u"Ročník",     "default": "",          "width": 70,                    "write":True },
                   "sex"           :     {"index": 8,   "name": "sex",          "name_cz":u"Pohlaví",    "default": "",           "width": None,                  "write":True },
                   "email"         :     {"index": 9,   "name": "email",        "name_cz": u"Email",     "default": "",          "width": None,                  "write":True },
                   "symbol"        :     {"index": 10,   "name": "symbol",      "name_cz": u"Nevím",     "default": "",           "width": None,                  "write":True },
                   "paid"          :     {"index": 11,  "name": "paid",         "name_cz": u"Nevím",     "default": "",          "width": None,                  "write":True },
                   "note"          :     {"index": 12,  "name": "note",         "name_cz": u"Nevím",     "default": "",          "width": None,                  "write":True },
                   "o1"            :     {"index": 13,  "name": "o1",           "name_cz":u"#1",         "default": "",          "width": None,                  "write":True },
                   "o2"            :     {"index": 14,  "name": "o2",           "name_cz":u"#2",         "default": "",          "width": None,                  "write":True },
                   "o3"            :     {"index": 15,  "name": "o3",           "name_cz":u"#3",         "default": "",          "width": None,                  "write":True },    
                   "o4"            :     {"index": 16,  "name": "o4",           "name_cz":u"#4",         "default": "",          "width": 10,                    "write":True },                                                                                                          
              }


"""
CATEGORIES
"""
CATEGORIES = {}


""" table collumns """
CATEGORIES['table'] = {
                        "id"          :     {"index": 0,   "name": "id",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":False  },
                        "name"        :     {"index": 1,   "name": "name",         "default": "unknown", "width": 200,                     "write":True  },
                        "description" :     {"index": 2,   "name": "description",  "default": "",        "width": 350,                     "write":True  },                                                                
                        "start_nr"    :     {"index": 3,   "name": "start_nr",     "default": 1,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g1"          :     {"index": 4,   "name": "g1",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g2"          :     {"index": 5,   "name": "g2",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g3"          :     {"index": 6,   "name": "g3",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g4"          :     {"index": 7,   "name": "g4",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g5"          :     {"index": 8,   "name": "g5",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g6"          :     {"index": 9,   "name": "g6",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g7"          :     {"index": 10,  "name": "g7",          "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g8"          :     {"index": 11,  "name": "g8",          "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g9"          :     {"index": 12,  "name": "g9",          "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        "g10"         :     {"index": 13,  "name": "g10",         "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True  },
                        #"#"           :     {"index": 14,  "name": "#",           "width":0},
                      }  
"""
CATEGORY GROUPS
"""
CGROUPS = {}


""" table collumns """
CGROUPS['table'] = {
                        "id"          :     {"index": 0,  "name": "id",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,      "write":False  },
                        "label"       :     {"index": 1,  "name": "label",        "default": "gx",      "width": 300,                      "write":True  },
                        "name"        :     {"index": 2,  "name": "name",         "default": "",        "width": 300,                      "write":True  },
                        "description" :     {"index": 3,  "name": "description",  "default": "",        "width": 300,                      "write":True  },                                                                                        
                      }  

"""
TAGS
"""
TAGS = {}


""" table collumns """
TAGS['table'] = {
                        "id"         :     {"index": 0,  "name": "id",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,        "write":False   },
                        "tag_id"     :     {"index": 1,  "name": "tag_id",       "default": 0,         "width": 160,                        "write":True   },                                                                
                        "printed_nr"  :    {"index": 2,  "name": "printed_nr",   "default": 0,         "width": 80,                         "write":True   },
                        "user_nr"  :       {"index": 3,  "name": "user_nr",      "default": 0,         "width": 80,                         "write":True   },
                        #"#1" :             {"index": 4,  "name": "",           "width":80},
                      } 

"""
ALLTAGS
"""
ALLTAGS = {}


""" database columns """
ALLTAGS['database'] = {
                       "id"          :     {"index": 0,  "name": "id",            "default": 0},
                       "tag_id"      :     {"index": 1,  "name": "tag_id",        "default": 0},                                                                 
                       "printed_nr"  :     {"index": 2,  "name": "printed_nr",    "default": 0},                           
                       "description" :     {"index": 3,  "name": "description",   "default": ""}                           
                       }
""" table collumns """
ALLTAGS['table'] =    {
                       "id"          :     {"index": 0,  "name": "id",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,    "write":False },
                       "tag_id"      :     {"index": 1,  "name": "tag_id",       "default": 0,         "width": 160,                    "write":True },                                                                
                       "printed_nr"  :     {"index": 2,  "name": "printed_nr",   "default": 0,         "width": 100,                    "write":True },                                                
                       "description" :     {"index": 3,  "name": "description",  "default": "",        "width": 300,                    "write":True }                                                
                       } 
"""
POINTS
"""
POINTS = {}

""" table collumns """
POINTS['table'] =    {
                      "id"          :    {"index": 0,  "name": "id",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":False},
                      "order_"      :    {"index": 1,  "name": "order",        "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True},                                                                
                      "points"      :    {"index": 2,  "name": "points",       "default": 0,         "width": WIDTH_NUMBER_4DIGIT,     "write":True},
                      "description" :    {"index": 3,  "name": "description",  "default": "",        "width": 160,                     "write":True},                        
                      } 

"""
RACE INFO
"""
RACEINFO = {}
""" table collumns """
RACEINFO['table'] =    {
                      "id"          :    {"index": 0,  "name": "id",            "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "name"        :    {"index": 1,  "name": "name",          "default": "unknown", "width": 300,                         "write":False},
                      "startlist"   :    {"index": 2,  "name": "startlist",     "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},
                      "dns"         :    {"index": 3,  "name": "dns"   ,        "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "finished"    :    {"index": 4,  "name": "finished",      "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},                                                                                    
                      "dnf"         :    {"index": 5,  "name": "dnf",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "dq"          :    {"index": 6,  "name": "dq",            "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "race"        :    {"index": 7,  "name": "race",          "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},               
                      "check"       :    {"index": 8,  "name": "check",         "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},                       
                      "-"           :    {"index": 9,  "name": "-",             "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},                       
                      } 

