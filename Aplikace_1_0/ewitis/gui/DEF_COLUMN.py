'''

Created on 27.12.2011

@author: Meloun
'''

TIMES = {}
"""
COLUMN for TIMES
"""
        
TIMES['database'] = {
    """
    database column for times
    """
                            "state"     :     {"index": 0, "name": "state"},
                            "id"        :     {"index": 1, "name": "id"},
                            "run_id"    :     {"index": 2, "name": "run_id"},
                            "user_id"   :     {"index": 3, "name": "user_id"},
                            "cell"      :     {"index": 4, "name": "cell"},
                            "time_raw"  :     {"index": 5, "name": "time_raw"},
                            "time"      :     {"index": 6, "name": "time"},                                
                      }
TIMES['table_training'] = {
    """
    table collumn for times, mode training
    """
                           "id"         : {"index": 0,  "name": "id",        "width":35,    "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width":50,    "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width":50,    "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width":50,    "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width":50,    "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width":150,   "write":1},                                       
                         }                             

TIMES['table_race'] =   {
    """
    table collumn for times, mode race
    """
                           "id"         : {"index": 0,  "name": "id",        "width":35,    "col_nr_export": None,    "write":1},
                           "nr"         : {"index": 1,  "name": "nr",        "width":50,    "col_nr_export": 1,       "write":1},
                           "cell"       : {"index": 2,  "name": "cell",      "width":50,    "col_nr_export": None,    "write":1},
                           "time"       : {"index": 3,  "name": "time",      "width":100,   "col_nr_export": 5,       "write":1},
                           "name"       : {"index": 4,  "name": "name",      "width":150,   "col_nr_export": 2,       "write":1},
                           "category"   : {"index": 5,  "name": "category",  "width":100,   "col_nr_export": None,    "write":1},
                           "order"      : {"index": 6,  "name": "order",     "width":50,    "col_nr_export": None,    "write":1},      
                           "order_kat"  : {"index": 7,  "name": "order_kat", "width":50,    "col_nr_export": 0,       "write":1},      
                           "start_nr"   : {"index": 8,  "name": "start_nr",  "width":50,    "col_nr_export": None,    "write":1},
                           "lap"        : {"index": 9,  "name": "lap",       "width":50,    "col_nr_export": None,    "write":1},                                               
                        }  
TIMES['export'] =       {
    """
    export collumn for times
    """
                            "nr   "     :     {"index": 0, "name": "nr"},
                            "time"      :     {"index": 1, "name": "time"},
                            "name"      :     {"index": 2, "name": "name"},
                            "category"  :     {"index": 3, "name": "category"}                                                                                                                                            
                        }