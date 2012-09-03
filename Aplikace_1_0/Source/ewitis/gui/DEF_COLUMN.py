'''

Created on 27.12.2011

@author: Meloun
'''

"""
RUNS
"""
RUNS = {}
        
""" database column for times """
RUNS['database'] = {
                    "state"         :     {"name": "state"},
                    "id"            :     {"name": "id"},
                    "starttime_id"  :     {"name": "starttime_id"},
                    "date"          :     {"name": "date"},
                    "name_id"       :     {"name": "name_id"},
                    "time_raw"      :     {"name": "time_raw"},
                    "description"   :     {"name": "description"}                                
                  }
""" table collumn for times, mode training """
RUNS['table'] = { 
                 "id"            :     {"index": 0,  "name": "id",          "width":40},                                
                 "date"          :     {"index": 1,  "name": "date",        "width":120},
                 "name"          :     {"index": 2,  "name": "name",        "width":120},                                
                 "description"   :     {"index": 3,  "name": "description", "width":0}                                
                 }  

"""
TIMES
"""
TIMES = {}
        
""" database column for times """
TIMES['database'] = {
                            "state"     :     {"index": 0, "name": "state"},
                            "id"        :     {"index": 1, "name": "id"},
                            "run_id"    :     {"index": 2, "name": "run_id"},
                            "user_id"   :     {"index": 3, "name": "user_id"},
                            "cell"      :     {"index": 4, "name": "cell"},
                            "time_raw"  :     {"index": 5, "name": "time_raw"},
                            #"time"      :     {"index": 6, "name": "time"},                                
                      }
""" table collumn for times, mode training """
TIMES['table_training'] = {
                           "id"         : {"index": 0,  "name": "id",        "width":35,    "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width":50,    "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width":50,    "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width":50,    "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width":50,    "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width":150,   "write":1},                                       
                         }                             

""" table collumn for times, mode race """
TIMES['table_race'] =   {
                           "id"         : {"index": 0,  "name": "id",        "width":35,    "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width":50,    "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width":50,    "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width":100,   "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width":150,   "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width":100,   "write":1},
                           "order"      : {"index": 6,  "name": "order",     "width":50,    "write":1},      
                           "order_cat"  : {"index": 7,  "name": "order_cat", "width":50,    "write":1},      
                           "start_nr"   : {"index": 8,  "name": "start_nr",  "width":50,    "write":1},
                           "lap"        : {"index": 9,  "name": "lap",       "width":50,    "write":1},                                                                          
                           #!! nedavat 'time_raw' => stejne jmeno s tabulkou a kreje se
                           "timeraw"    : {"index": 10, "name": "timeraw",   "width":100,   "write":1},                        
                        
                        }
  
""" export collumn for times """
TIMES['export'] =       {
                            "nr   "     :     {"index": 0, "name": "nr"},
                            "time"      :     {"index": 1, "name": "time"},
                            "name"      :     {"index": 2, "name": "name"},
                            "category"  :     {"index": 3, "name": "category"}                                                                                                                                                                                                                
                        }
"""
USERS
"""
USERS = {}


""" database column for times """
USERS['database'] = { 
                    "id"            :     {"index": 0,      "name": "id",               },
                    "nr"            :     {"index": 1,      "name": "nr",               },
                    "name"          :     {"index": 2,      "name": "name",             },
                    "first_name"    :     {"index": 3,      "name": "first_name",       },
                    "category_id"   :     {"index": 4,      "name": "category",         },
                    "club"          :     {"index": 5,      "name": "club",             },
                    "birthday"      :     {"index": 6,      "name": "birthday",         },
                    "sex"           :     {"index": 7,      "name": "sex",              },
                    "email"         :     {"index": 8,      "name": "email",            },
                    "symbol"        :     {"index": 9,      "name": "symbol",           },
                    "paid"          :     {"index": 10,     "name": "paid",             },
                    "note"          :     {"index": 11,     "name": "note",             },
                    "user_field_1"  :     {"index": 12,     "name": "user_field_1",     },
                    "user_field_2"  :     {"index": 13,     "name": "user_field_2",     },
                    "user_field_3"  :     {"index": 14,     "name": "user_field_3",     },    
                    "user_field_4"  :     {"index": 15,     "name": "user_field_4",     },                                                                                        
                  }

""" table collumn for times, mode race """ 
USERS['table'] = { "id"            :     {"index": 0,   "name": "id",          "width":30,   },                   
                   "nr"            :     {"index": 1,   "name": "nr",          "width":30,   },
                   "name"          :     {"index": 2,   "name": "name",        "width":100,  },                
                   "first_name"    :     {"index": 3,   "name": "first_name",  "width":100,  },
                   "category"      :     {"index": 4,   "name": "category",    "width":100,  },                   
                   "club"          :     {"index": 5,   "name": "club",        "width":200,  },
                   "birthday"      :     {"index": 6,   "name": "birthday",    "width":70,   },
                   "sex"           :     {"index": 7,   "name": "sex",         "width":None, },
                   "email"         :     {"index": 8,   "name": "email",       "width":None, },
                   "symbol"        :     {"index": 9,   "name": "symbol",      "width":None, },
                   "paid"          :     {"index": 10,  "name": "paid",        "width":None, },
                   "note"          :     {"index": 11,  "name": "note",        "width":None, },
                   "user_field_1"  :     {"index": 12,  "name": "#1",          "width":None, },
                   "user_field_2"  :     {"index": 13,  "name": "#2",          "width":None, },
                   "user_field_3"  :     {"index": 14,  "name": "#3",          "width":None, },    
                   "user_field_4"  :     {"index": 15,  "name": "#4",          "width":10,   },                                                                    
              }


"""
CATEGORIES
"""
CATEGORIES = {}


""" database column for times """
CATEGORIES['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           },
                           "name"          :     {"index": 1,  "name": "name",         },                                                                 
                           "description"   :     {"index": 2,  "name": "description",  },
                           "start_nr"      :     {"index": 3,  "name": "start_nr",     },
                           "g1"            :     {"index": 4,  "name": "g1",           },
                           "g2"            :     {"index": 5,  "name": "g2",           },
                           "g3"            :     {"index": 6,  "name": "g3",           },
                           "g4"            :     {"index": 7,  "name": "g4",           },
                           "g5"            :     {"index": 8,  "name": "g5",           },
                           "g6"            :     {"index": 9,  "name": "g6",           },
                           "g7"            :     {"index": 10, "name": "g7",           },
                           "g8"            :     {"index": 11, "name": "g8",           },
                           "g9"            :     {"index": 12, "name": "g9",           },
                           "g10"           :     {"index": 13, "name": "g10",          },
                         }
""" table collumn for times, mode race """
CATEGORIES['table'] = {
                        "id"          :     {"index": 0,  "name": "id",           "width":30},
                        "name"        :     {"index": 1,  "name": "name",         "width":220},
                        "description" :     {"index": 2,  "name": "description",  "width":400},                                                                
                        "start_nr"    :     {"index": 3,  "name": "start_nr",     "width":100},
                        "g1"          :     {"index": 4,  "name": "g1",           "width":30},
                        "g2"          :     {"index": 5,  "name": "g2",           "width":30},
                        "g3"          :     {"index": 6,  "name": "g3",           "width":30},
                        "g4"          :     {"index": 7,  "name": "g4",           "width":30},
                        "g5"          :     {"index": 8,  "name": "g5",           "width":30},
                        "g6"          :     {"index": 9,  "name": "g6",           "width":30},
                        "g7"          :     {"index": 10,  "name": "g7",          "width":30},
                        "g8"          :     {"index": 11,  "name": "g8",          "width":30},
                        "g9"          :     {"index": 12,  "name": "g9",          "width":30},
                        "g10"         :     {"index": 13,  "name": "g10",         "width":30},
                        #"#"           :     {"index": 14,  "name": "#",           "width":0},
                      }  
"""
CATEGORY GROUPS
"""
CGROUPS = {}


""" database column for times """
CGROUPS['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           },
                           "label"         :     {"index": 1,  "name": "label",         },                                                                 
                           "name"          :     {"index": 2,  "name": "name",         },                                                                 
                           "description"   :     {"index": 3,  "name": "description",  },                           
                         }
""" table collumn for times, mode race """
CGROUPS['table'] = {
                        "id"          :     {"index": 0,  "name": "id",           "width":30},
                        "label"       :     {"index": 1,  "name": "label",        "width":300},
                        "name"        :     {"index": 2,  "name": "name",         "width":300},
                        "description" :     {"index": 3,  "name": "description",  "width":300},                                                                                        
                      }  

"""
TAGS
"""
TAGS = {}


""" database column for times """
TAGS['database'] = {
                           "id"          :     {"index": 0,  "name": "id",            },
                           "tag_id"      :     {"index": 1,  "name": "tag_id",        },                                                                 
                           "printed_nr"  :     {"index": 2,  "name": "printed_nr",    },
                           "user_nr"     :     {"index": 3,  "name": "user_nr",       },
                         }
""" table collumn for times, mode race """
TAGS['table'] = {
                        "id"         :     {"index": 0,  "name": "id",           "width":30},
                        "tag_id"     :     {"index": 1,  "name": "tag_id",       "width":160},                                                                
                        "printed_nr"  :    {"index": 2,  "name": "printed_nr",   "width":80},
                        "user_nr"  :       {"index": 3,  "name": "user_nr",      "width":80},
                        #"#1" :             {"index": 4,  "name": "",           "width":80},
                      } 
