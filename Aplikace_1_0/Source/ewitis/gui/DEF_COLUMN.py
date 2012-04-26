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
                           "id"         : {"index": 0,  "name": "id",        "width":35,    "col_nr_export": None,  "col_nr_export_raw": 0,     "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width":50,    "col_nr_export": 1,     "col_nr_export_raw": 1,     "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width":50,    "col_nr_export": None,  "col_nr_export_raw": 2,     "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width":100,   "col_nr_export": 5,     "col_nr_export_raw": 3,     "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width":150,   "col_nr_export": 2,     "col_nr_export_raw": None,  "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width":100,   "col_nr_export": None,  "col_nr_export_raw": None,  "write":1},
                           "order"      : {"index": 6,  "name": "order",     "width":50,    "col_nr_export": None,  "col_nr_export_raw": 4,     "write":1},      
                           "order_kat"  : {"index": 7,  "name": "order_kat", "width":50,    "col_nr_export": 0,     "col_nr_export_raw": 5,     "write":1},      
                           "start_nr"   : {"index": 8,  "name": "start_nr",  "width":50,    "col_nr_export": None,  "col_nr_export_raw": 6,     "write":1},
                           "lap"        : {"index": 9,  "name": "lap",       "width":50,    "col_nr_export": None,  "col_nr_export_raw": 7,     "write":1},                                               
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
USERS['table'] = { "id"            :     {"index": 0,   "name": "id",          "width":30,   "col_nr_export": None, "col_nr_export_raw": 8},                   
                   "nr"            :     {"index": 1,   "name": "nr",          "width":30,   "col_nr_export": None, "col_nr_export_raw": 9},
                   "name"          :     {"index": 2,   "name": "name",        "width":100,  "col_nr_export": None, "col_nr_export_raw": 10},                
                   "first_name"    :     {"index": 3,   "name": "first_name",  "width":100,  "col_nr_export": None, "col_nr_export_raw": 11},
                   "category"      :     {"index": 4,   "name": "category",    "width":100,  "col_nr_export": None, "col_nr_export_raw": 12},                   
                   "club"          :     {"index": 5,   "name": "club",        "width":200,  "col_nr_export": 3,    "col_nr_export_raw": 13},
                   "birthday"      :     {"index": 6,   "name": "birthday",    "width":70,   "col_nr_export": 4,    "col_nr_export_raw": 14},
                   "sex"           :     {"index": 7,   "name": "sex",         "width":None, "col_nr_export": None, "col_nr_export_raw": 15},
                   "email"         :     {"index": 8,   "name": "email",       "width":None, "col_nr_export": None, "col_nr_export_raw": 16},
                   "symbol"        :     {"index": 9,   "name": "symbol",      "width":None, "col_nr_export": None, "col_nr_export_raw": 17},
                   "paid"          :     {"index": 10,  "name": "paid",        "width":None, "col_nr_export": None, "col_nr_export_raw": 18},
                   "note"          :     {"index": 11,  "name": "note",        "width":None, "col_nr_export": None, "col_nr_export_raw": 19},
                   "user_field_1"  :     {"index": 12,  "name": "#1",          "width":None, "col_nr_export": None, "col_nr_export_raw": 20},
                   "user_field_2"  :     {"index": 13,  "name": "#2",          "width":None, "col_nr_export": None, "col_nr_export_raw": 21},
                   "user_field_3"  :     {"index": 14,  "name": "#3",          "width":None, "col_nr_export": None, "col_nr_export_raw": 22},    
                   "user_field_4"  :     {"index": 15,  "name": "#4",          "width":10,   "col_nr_export": None, "col_nr_export_raw": 23},                                                                    
              }


"""
CATEGORIES
"""
CATEGORIES = {}


""" database column for times """
CATEGORIES['database'] = {
                           "id"            :     {"index": 0,  "name": "id",           "col_nr_export": None},
                           "name"          :     {"index": 1,  "name": "name",         "col_nr_export": None},                                                                 
                           "start_nr"     :     {"index": 2,  "name": "start_nr",    "col_nr_export": None},
                         }
""" table collumn for times, mode race """
CATEGORIES['table'] = {
                        "id"         :     {"index": 0,  "name": "id",           "width":30},
                        "name"       :     {"index": 1,  "name": "name",         "width":300},                                                                
                        "start_nr"  :     {"index": 2,  "name": "start_nr",    "width":300},
                      }  

"""
TAGS
"""
TAGS = {}


""" database column for times """
TAGS['database'] = {
                           "id"          :     {"index": 0,  "name": "id",            "col_nr_export": None},
                           "tag_id"      :     {"index": 1,  "name": "tag_id",        "col_nr_export": None},                                                                 
                           "printed_nr"  :     {"index": 2,  "name": "printed_nr",    "col_nr_export": None},
                           "user_nr"     :     {"index": 3,  "name": "user_nr",       "col_nr_export": None},
                         }
""" table collumn for times, mode race """
TAGS['table'] = {
                        "id"         :     {"index": 0,  "name": "id",           "width":30},
                        "tag_id"     :     {"index": 1,  "name": "tag_id",       "width":160},                                                                
                        "printed_nr"  :    {"index": 2,  "name": "printed_nr",   "width":80},
                        "user_nr"  :       {"index": 3,  "name": "user_nr",      "width":80},
                        #"#1" :             {"index": 4,  "name": "",           "width":80},
                      } 
