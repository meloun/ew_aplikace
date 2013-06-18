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
                    "state"         :     {"name": "state"},
                    "id"            :     {"name": "id"},
                    "starttime_id"  :     {"name": "starttime_id"},
                    "date"          :     {"name": "date"},
                    "name_id"       :     {"name": "name_id"},
                    "time_raw"      :     {"name": "time_raw"},
                    #"description"   :     {"name": "description"}                                
                  }
""" table collumns """
RUNS['table'] = { 
                 "id"            :     {"index": 0,  "name": "id",          "width": WIDTH_NUMBER_4DIGIT},                                
                 "date"          :     {"index": 1,  "name": "date",        "width": 130},
                 "name"          :     {"index": 2,  "name": "name",        "width": 100},                                
                 #"description"   :     {"index": 3,  "name": "description", "width":10}                                
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
                           "id"         : {"index": 0,  "name": "id",        "width": WIDTH_NUMBER_4DIGIT,    "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width": 50,    "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width": 50,    "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width": 50,    "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width": 50,    "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width": 150,   "write":1},                                       
                         }                             

""" table collumn for times, mode race """
TIMES['table_race'] =   {
                           "id"         : {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT,    "write":1  },
                           "nr"         : {"index": 1,  "name": "nr",           "width": WIDTH_NUMBER_4DIGIT,    "write":1  },
                           "cell"       : {"index": 2,  "name": "cell",         "width": 35,                     "write":1  },
                           "time"       : {"index": 3,  "name": "time",         "width": 80,                     "write":1  },
                           "name"       : {"index": 4,  "name": "name",         "width": 130,                    "write":1  },
                           "category"   : {"index": 5,  "name": "category",     "width": 100,                    "write":1  },
                           "order"      : {"index": 6,  "name": "order",        "width": 50,                     "write":1  },      
                           "order_cat"  : {"index": 7,  "name": "order_cat",    "width": 50,                     "write":1  },      
                           "start_nr"   : {"index": 8,  "name": "start_nr",     "width": 50,                     "write":1  },
                           "lap"        : {"index": 9,  "name": "lap",          "width": 50,                     "write":1  },                                                                          
                           "laptime"    : {"index": 10, "name": "laptime",      "width": 80,                     "write":1  },                                                                          
                           "best_laptime":{"index": 11, "name": "best_laptime", "width": 80,                     "write":1  },                                                                          
                           #!! nedavat 'time_raw' => stejne jmeno s tabulkou a kreje se
                           "timeraw"    : {"index": 12, "name": "timeraw",      "width": 100,                    "write":1  },                        
                        
                        }
"""
USERS
"""
USERS = {}


""" database columns """
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
                    "o1"            :     {"index": 12,     "name": "o1",     },
                    "o2"            :     {"index": 13,     "name": "o2",     },
                    "o3"            :     {"index": 14,     "name": "o3",     },    
                    "o4"            :     {"index": 15,     "name": "o4",     },                                                                                        
                  }

""" table collumns """
USERS['table'] = { "id"            :     {"index": 0,   "name": "id",          "width": WIDTH_NUMBER_4DIGIT,   },                   
                   "nr"            :     {"index": 1,   "name": "nr",          "width": WIDTH_NUMBER_4DIGIT,   },
                   "name"          :     {"index": 2,   "name": "name",        "width": 100,  },                
                   "first_name"    :     {"index": 3,   "name": "first_name",  "width": 100,  },
                   "category"      :     {"index": 4,   "name": "category",    "width": 100,  },                   
                   "club"          :     {"index": 5,   "name": "club",        "width": 200,  },
                   "birthday"      :     {"index": 6,   "name": "birthday",    "width": 70,   },
                   "sex"           :     {"index": 7,   "name": "sex",         "width": None, },
                   "email"         :     {"index": 8,   "name": "email",       "width": None, },
                   "symbol"        :     {"index": 9,   "name": "symbol",      "width": None, },
                   "paid"          :     {"index": 10,  "name": "paid",        "width": None, },
                   "note"          :     {"index": 11,  "name": "note",        "width": None, },
                   "o1"            :     {"index": 12,  "name": "o1",          "width": None, },
                   "o2"            :     {"index": 13,  "name": "o2",          "width": None, },
                   "o3"            :     {"index": 14,  "name": "o3",          "width": None, },    
                   "o4"            :     {"index": 15,  "name": "o4",          "width": 10,   },                                                                    
              }


"""
CATEGORIES
"""
CATEGORIES = {}


""" database columns """
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
""" table collumns """
CATEGORIES['table'] = {
                        "id"          :     {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT  },
                        "name"        :     {"index": 1,  "name": "name",         "width": 200                  },
                        "description" :     {"index": 2,  "name": "description",  "width": 350                  },                                                                
                        "start_nr"    :     {"index": 3,  "name": "start_nr",     "width": WIDTH_NUMBER_4DIGIT  },
                        "g1"          :     {"index": 4,  "name": "g1",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g2"          :     {"index": 5,  "name": "g2",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g3"          :     {"index": 6,  "name": "g3",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g4"          :     {"index": 7,  "name": "g4",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g5"          :     {"index": 8,  "name": "g5",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g6"          :     {"index": 9,  "name": "g6",           "width": WIDTH_NUMBER_4DIGIT  },
                        "g7"          :     {"index": 10,  "name": "g7",          "width": WIDTH_NUMBER_4DIGIT  },
                        "g8"          :     {"index": 11,  "name": "g8",          "width": WIDTH_NUMBER_4DIGIT  },
                        "g9"          :     {"index": 12,  "name": "g9",          "width": WIDTH_NUMBER_4DIGIT  },
                        "g10"         :     {"index": 13,  "name": "g10",         "width": WIDTH_NUMBER_4DIGIT  },
                        #"#"           :     {"index": 14,  "name": "#",           "width":0},
                      }  
"""
CATEGORY GROUPS
"""
CGROUPS = {}


""" database columns """
CGROUPS['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           },
                           "label"         :     {"index": 1,  "name": "label",         },                                                                 
                           "name"          :     {"index": 2,  "name": "name",         },                                                                 
                           "description"   :     {"index": 3,  "name": "description",  },                           
                         }
""" table collumns """
CGROUPS['table'] = {
                        "id"          :     {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT  },
                        "label"       :     {"index": 1,  "name": "label",        "width": 300                  },
                        "name"        :     {"index": 2,  "name": "name",         "width": 300                  },
                        "description" :     {"index": 3,  "name": "description",  "width": 300                  },                                                                                        
                      }  

"""
TAGS
"""
TAGS = {}


""" database columns """
TAGS['database'] = {
                           "id"          :     {"index": 0,  "name": "id",            },
                           "tag_id"      :     {"index": 1,  "name": "tag_id",        },                                                                 
                           "printed_nr"  :     {"index": 2,  "name": "printed_nr",    },
                           "user_nr"     :     {"index": 3,  "name": "user_nr",       },
                         }
""" table collumns """
TAGS['table'] = {
                        "id"         :     {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT   },
                        "tag_id"     :     {"index": 1,  "name": "tag_id",       "width": 160                   },                                                                
                        "printed_nr"  :    {"index": 2,  "name": "printed_nr",   "width": 80                    },
                        "user_nr"  :       {"index": 3,  "name": "user_nr",      "width": 80                    },
                        #"#1" :             {"index": 4,  "name": "",           "width":80},
                      } 

"""
ALLTAGS
"""
ALLTAGS = {}


""" database columns """
ALLTAGS['database'] = {
                       "id"          :     {"index": 0,  "name": "id",            },
                       "tag_id"      :     {"index": 1,  "name": "tag_id",        },                                                                 
                       "printed_nr"  :     {"index": 2,  "name": "printed_nr",    },                           
                       "description" :     {"index": 3,  "name": "description",   }                           
                       }
""" table collumns """
ALLTAGS['table'] =    {
                       "id"          :     {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT     },
                       "tag_id"      :     {"index": 1,  "name": "tag_id",       "width": 160                     },                                                                
                       "printed_nr"  :     {"index": 2,  "name": "printed_nr",   "width": 100                     },                                                
                       "description" :     {"index": 3,  "name": "description",  "width": 300                     }                                                
                       } 
"""
POINTS
"""
POINTS = {}

""" database columns """
POINTS['database'] = {
                      "id"          :    {"index": 0,  "name": "id",            },
                      "order"       :    {"index": 1,  "name": "order",         },                                                                 
                      "points"      :    {"index": 2,  "name": "points",        },
                      "description" :    {"index": 3,  "name": "description",   },
                      }
""" table collumns """
POINTS['table'] =    {
                      "id"          :    {"index": 0,  "name": "id",           "width": WIDTH_NUMBER_4DIGIT    },
                      "order"       :    {"index": 1,  "name": "order",        "width": WIDTH_NUMBER_4DIGIT    },                                                                
                      "points"      :    {"index": 2,  "name": "points",       "width": WIDTH_NUMBER_4DIGIT    },
                      "description" :    {"index": 3,  "name": "description",  "width": 160                    },                        
                      } 

"""
RACE INFO
"""
RACE_INFO = {}
""" database columns """
RACE_INFO['database'] = {
                      "id"          :    {"index": 0,  "name": "id",            },
                      "name"        :    {"index": 1,  "name": "id",            },                      
                      "start_list"  :    {"index": 2,  "name": "start_list",    },                                                                 
                      "dns"         :    {"index": 3,  "name": "dns"   ,        },
                      "dsq"         :    {"index": 4,  "name": "dsq",           },
                      "dnf"         :    {"index": 5,  "name": "dnf",           },
                      "finished"    :    {"index": 6,  "name": "finished",      },
                      "awaited"     :    {"index": 7,  "name": "awaited",       },
                      }
""" table collumns """
RACE_INFO['table'] =    {
                      "id"          :    {"index": 0,  "name": "id",            "width": WIDTH_NUMBER_4DIGIT},
                      "name"        :    {"index": 1,  "name": "id",            "width": 300},
                      "start_list"  :    {"index": 2,  "name": "start_list",    "width": 2*WIDTH_NUMBER_4DIGIT},                                                                 
                      "dns"         :    {"index": 3,  "name": "dns"   ,        "width": WIDTH_NUMBER_4DIGIT},
                      "dsq"         :    {"index": 4,  "name": "dsq",           "width": WIDTH_NUMBER_4DIGIT},
                      "dnf"         :    {"index": 5,  "name": "dnf",           "width": WIDTH_NUMBER_4DIGIT},
                      "finished"    :    {"index": 6,  "name": "finished",      "width": 2*WIDTH_NUMBER_4DIGIT},
                      "awaited"     :    {"index": 7,  "name": "awaited",       "width": WIDTH_NUMBER_4DIGIT},                       
                      } 

