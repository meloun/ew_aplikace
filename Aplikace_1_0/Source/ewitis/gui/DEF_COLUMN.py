# -*- coding: utf-8 -*-
'''

Created on 27.12.2011

@author: Meloun
'''

""" WIDTHS """
WIDTH_NUMBER_4DIGIT = 40

"""
RUNS
"""
RUNS = {}
        
""" database columns """
RUNS['database'] = {
                    "state"         :     {"name": "state",         "default": 161},
                    "id"            :     {"name": "id",            "default": 0},
                    "starttime_id"  :     {"name": "starttime_id",  "default": 0},
                    "date"          :     {"name": "date",          "default": "0.0. 2000 00:00:00"},
                    "name_id"       :     {"name": "name_id",       "default": 0},
                    "time_raw"      :     {"name": "time_raw",      "default": 0},
                    "description"   :     {"name": "description",   "default": ""}                                
                  }
""" table collumns """
RUNS['table'] = { 
                 "id"            :     {"index": 0,  "name": "id",          "default": 0,                       "width": WIDTH_NUMBER_4DIGIT,   "write": False},                                
                 "date"          :     {"index": 1,  "name": "date",        "default": "0.0. 2000 00:00:00",    "width": 100,                   "write": True},                                                 
                 "description"   :     {"index": 2,  "name": "description", "default": "",                      "width":10,                     "write": True}                                
                 }  

"""
TIMES
"""
TIMES = {}
        
""" database column for times """
TIMES['database'] = {
                            "state"     :     {"index": 0,  "name": "state",    "default": 161},
                            "id"        :     {"index": 1,  "name": "id",       "default": 0},
                            "run_id"    :     {"index": 2,  "name": "run_id",   "default": 0},
                            "user_id"   :     {"index": 3,  "name": "user_id",  "default": 0},
                            "cell"      :     {"index": 4,  "name": "cell",     "default": 250},
                            "time_raw"  :     {"index": 5,  "name": "time_raw", "default": 0},
                            #"time"      :     {"index": 6,  "name": "time",     "default": None},                                
                      }                            

""" table collumn for times, mode race """
TIMES['table'] =   {
                           "id"         : {"index": 0,  "name": "id",           "name_cz": u"id",               "default": 0,           "width": WIDTH_NUMBER_4DIGIT,    "write":False  },
                           "nr"         : {"index": 1,  "name": "nr",           "name_cz": u"Číslo",            "default": 0,           "width": WIDTH_NUMBER_4DIGIT,    "write":True  },
                           "cell"       : {"index": 2,  "name": "cell",         "name_cz": u"Buňka",            "default": 250,         "width": 35,                     "write":True  },
                           "status"     : {"index": 3,  "name": "status",       "name_cz": u"Status",           "default": "race",      "width": 60,                     "write":True  },                           
                           "time1"      : {"index": 4,  "name": "time1",         "name_cz": u"Čas1",            "default": "",          "width": 80,                     "write":False  },                           
                           "lap1"       : {"index": 5,  "name": "lap1",         "name_cz": u"Okruhy1",          "default": "",          "width": 50,                     "write":False  },
                           "time2"      : {"index": 6,  "name": "time2",        "name_cz": u"Čas2",             "default": "",          "width": 80,                     "write":False  },
                           "lap2"       : {"index": 7,  "name": "lap2",         "name_cz": u"Okruhy2",          "default": "",          "width": 50,                     "write":False  },
                           "time3"      : {"index": 8,  "name": "time3",        "name_cz": u"Čas3",             "default": "",          "width": 80,                     "write":False  },
                           "lap3"       : {"index": 9, "name": "lap3",         "name_cz": u"Okruhy3",           "default": "",          "width": 50,                     "write":False  },
                           "name"       : {"index": 10,  "name": "name",         "name_cz": u"Jméno",           "default": "unknow",    "width": 150,                    "write":False  },
                           "category"   : {"index": 11,  "name": "category",     "name_cz": u"Kategorie",       "default": "unknown",   "width": 100,                    "write":False  },
                           "order1"     : {"index": 12, "name": "order1",        "name_cz": u"Pořadí1",         "default": "",          "width": 50,                     "write":False  },                                 
                           "order2"     : {"index": 13, "name": "order2",        "name_cz": u"Pořadí2",         "default": "",          "width": 50,                     "write":False  },
                           "order3"     : {"index": 14, "name": "order3",        "name_cz": u"Pořadí3",         "default": "",          "width": 50,                     "write":False  },
                           "order_cat"  : {"index": 15, "name": "order_cat",    "name_cz": u"Pořadí",           "default": "",          "width": 50,                     "write":False  },      
                           "start_nr"   : {"index": 16, "name": "start_nr",     "name_cz": u"Start",            "default": 1,           "width": 50,                     "write":False  },
                           "lap"        : {"index": 17, "name": "lap",          "name_cz": u"Okruhy",           "default": "",          "width": 50,                     "write":False  },                                                                          
                           "laptime"    : {"index": 18, "name": "laptime",      "name_cz": u"Čas kola",         "default": "",          "width": 80,                     "write":False  },                                                                          
                           "best_laptime":{"index": 19, "name": "best_laptime", "name_cz": u"Top okruh",        "default": "",          "width": 80,                     "write":False  },                                                                          
                           "points1"    : {"index": 20, "name": "points1",      "name_cz": u"Body",             "default": "",          "width": 60,                     "write":False  },                                                                                                                                                                              
                           "points2"    : {"index": 21, "name": "points2",      "name_cz": u"Body",             "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           "points3"    : {"index": 22, "name": "points3",      "name_cz": u"Body",             "default": "",          "width": 60,                     "write":False  },                                                                                                     
                           #!! nedavat 'time_raw' => stejne jmeno s tabulkou a kreje se
                           "timeraw"    : {"index": 23, "name": "timeraw",      "name_cz": u"Čas Raw",          "default": 161,         "width": 100,                    "write":True  },                        
                        
                        }
"""
USERS
"""
USERS = {}


""" database columns """
USERS['database'] = { 
                    "id"            :     {"index": 0,      "name": "id",           "default": 0},
                    "nr"            :     {"index": 1,      "name": "nr",           "default": 0},
                    "status"        :     {"index": 2,      "name": "status",       "default": "race"},    
                    "name"          :     {"index": 3,      "name": "name",         "default": "unknown"},
                    "first_name"    :     {"index": 4,      "name": "first_name",   "default": "unknown"},
                    "category_id"   :     {"index": 5,      "name": "category",     "default": 1},
                    "club"          :     {"index": 6,      "name": "club",         "default": ""},
                    "birthday"      :     {"index": 7,      "name": "birthday",     "default": ""},
                    "sex"           :     {"index": 8,      "name": "sex",          "default": ""},
                    "email"         :     {"index": 9,      "name": "email",        "default": ""},
                    "symbol"        :     {"index": 10,     "name": "symbol",       "default": ""},
                    "paid"          :     {"index": 11,     "name": "paid",         "default": ""},
                    "note"          :     {"index": 12,     "name": "note",         "default": ""},
                    "o1"            :     {"index": 13,     "name": "o1",           "default": ""},
                    "o2"            :     {"index": 14,     "name": "o2",           "default": ""},
                    "o3"            :     {"index": 15,     "name": "o3",           "default": ""},    
                    "o4"            :     {"index": 16,     "name": "o4",           "default": ""},                                                                                                                                                                                                
                  }

""" table collumns """
USERS['table'] = { "id"            :     {"index": 0,   "name": "id",           "name_cz": u"id",        "default": 0,           "width": WIDTH_NUMBER_4DIGIT,   "write":False },                   
                   "nr"            :     {"index": 1,   "name": "nr",           "name_cz": u"Číslo",     "default": 0,           "width": WIDTH_NUMBER_4DIGIT,   "write":True },
                   "status"        :     {"index": 2,   "name": "status",       "name_cz": u"Status",    "default": "race",      "width": WIDTH_NUMBER_4DIGIT,   "write":True },
                   "name"          :     {"index": 3,   "name": "name",         "name_cz": u"Jméno",     "default": "unknown",   "width": 100,                   "write":True },                
                   "first_name"    :     {"index": 4,   "name": "first_name",   "name_cz": u"Nevím",     "default": "unknown",   "width": 100,                   "write":True },
                   "category"      :     {"index": 5,   "name": "category",     "name_cz": u"Kategorie", "default": "unknown",   "width": 100,                   "write":True },                   
                   "club"          :     {"index": 6,   "name": "club",         "name_cz": u"Klub",      "default": "",          "width": 200,                   "write":True },
                   "birthday"      :     {"index": 7,   "name": "birthday",     "name_cz":u"Ročník",     "default": "",          "width": 70,                    "write":True },
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


""" database columns """
CATEGORIES['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           "default": 0},
                           "name"          :     {"index": 1,  "name": "name",         "default": "unknown"},                                                                 
                           "description"   :     {"index": 2,  "name": "description",  "default": "0"},
                           "start_nr"      :     {"index": 3,  "name": "start_nr",     "default": 1},
                           "g1"            :     {"index": 4,  "name": "g1",           "default": 0},
                           "g2"            :     {"index": 5,  "name": "g2",           "default": 0},
                           "g3"            :     {"index": 6,  "name": "g3",           "default": 0},
                           "g4"            :     {"index": 7,  "name": "g4",           "default": 0},
                           "g5"            :     {"index": 8,  "name": "g5",           "default": 0},
                           "g6"            :     {"index": 9,  "name": "g6",           "default": 0},
                           "g7"            :     {"index": 10, "name": "g7",           "default": 0},
                           "g8"            :     {"index": 11, "name": "g8",           "default": 0},
                           "g9"            :     {"index": 12, "name": "g9",           "default": 0},
                           "g10"           :     {"index": 13, "name": "g10",          "default": 0},
                         }
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


""" database columns """
CGROUPS['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           "default": 0},
                           "label"         :     {"index": 1,  "name": "label",        "default": "gx"},                                                                 
                           "name"          :     {"index": 2,  "name": "name",         "default": ""},                                                                 
                           "description"   :     {"index": 3,  "name": "description",  "default": ""},                           
                         }
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


""" database columns """
TAGS['database'] = {
                           "id"          :     {"index": 0,  "name": "id",            "default": 0},
                           "tag_id"      :     {"index": 1,  "name": "tag_id",        "default": 0},                                                                 
                           "printed_nr"  :     {"index": 2,  "name": "printed_nr",    "default": 0},
                           "user_nr"     :     {"index": 3,  "name": "user_nr",       "default": 0},
                         }
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

""" database columns """
POINTS['database'] = {
                      "id"          :    {"index": 0,  "name": "id",            "default": 0},
                      "order_"      :    {"index": 1,  "name": "order",         "default": 0},                                                                 
                      "points"      :    {"index": 2,  "name": "points",        "default": 0},
                      "description" :    {"index": 3,  "name": "description",   "default": ""},
                      }
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
""" database columns """
RACEINFO['database'] = {
                      "id"          :    {"index": 0,  "name": "id",            "default": 0},
                      "name"        :    {"index": 1,  "name": "id",            "default":"unknown"},                      
                      "startlist"   :    {"index": 2,  "name": "startlist",     "default": 0},                                                                                       
                      "dns"         :    {"index": 3,  "name": "dns"   ,        "default": 0},                      
                      "finished"    :    {"index": 4,  "name": "finished",      "default": 0},
                      "dnf"         :    {"index": 5,  "name": "dnf",           "default": 0},
                      "dsq"         :    {"index": 6,  "name": "dsq",           "default": 0},
                      "race"        :    {"index": 7,  "name": "race",          "default": 0},
                      }
""" table collumns """
RACEINFO['table'] =    {
                      "id"          :    {"index": 0,  "name": "id",            "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "name"        :    {"index": 1,  "name": "id",            "default": "unknown", "width": 300,                         "write":False},
                      "startlist"   :    {"index": 2,  "name": "startlist",     "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},
                      "dns"         :    {"index": 3,  "name": "dns"   ,        "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "finished"    :    {"index": 4,  "name": "finished",      "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},                                                                                    
                      "dnf"         :    {"index": 5,  "name": "dnf",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "dsq"         :    {"index": 6,  "name": "dsq",           "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},
                      "race"        :    {"index": 7,  "name": "race",          "default": 0,         "width": 2*WIDTH_NUMBER_4DIGIT,       "write":False},               
                      "check"       :    {"index": 8,  "name": "check",         "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},                       
                      "-"           :    {"index": 9,  "name": "-",             "default": 0,         "width": WIDTH_NUMBER_4DIGIT,         "write":False},                       
                      } 

