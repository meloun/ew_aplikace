# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from PyQt4 import Qt, QtCore, QtGui

#MEASURE MODE
# MODE_TRAINING - simple version for customers 
# MODE_RACE - full version
MODE_TRAINING_BASIC, MODE_TRAINING, MODE_RACE = range(3)
MEASURE_MODE_STRINGS = {MODE_TRAINING_BASIC:"training_basic", MODE_TRAINING:"training", MODE_RACE:"race"}

#RACE & TRAINING SETTINGS
TRAINING_STANDART = {"name": u"standard",
                     "starts": [ {"nr_min":   0, "nr_max":  999, "nr_start": "END"},
                                ]
                }

DEFAULT_RACE = {"name": u"ewitis race",
                "starts": [ {"nr_min":   0, "nr_max":  999, "nr_start": 1},                                                        
                          ]
                }

BLIZAK_2011 = {"name": u"Blizak2011",
                "starts": [ {"nr_min":   0, "nr_max":  999, "nr_start": 1},                                                        
                          ]
                }

BC_KRALOVICE = {"name": u"Kralovický MTB Maraton",
                "starts": [ {"category" : "Kategorie A", "nr_min":   0, "nr_max":  49, "nr_start": 1},
                            {"category" : "Kategorie A", "nr_min":  50, "nr_max":  99, "nr_start": 2},
                            {"category" : "Kategorie A", "nr_min": 100, "nr_max": 149, "nr_start": 3},
                          ]
                }
STUPNO_2011_2 = { "name"   :   u"Stupno 2011, Author MTB Kriterium",
                "starts" :   [ {"category" : "A",      "nr_start": 1},
                               {"category" : "B",    "nr_start": 2},                               
                             ]              
             }
STUPNO_2011= { "name"   :   u"Stupno 2011, Author MTB Kriterium",
               "starts" :   [  {"category" : u"žáci nejmladší",      "nr_start": 1},
                               {"category" : u"žákyně nejmladší",    "nr_start": 2},
                               {"category" : u"žáci mladší",         "nr_start": 3},
                               {"category" : u"žákyně mladší",       "nr_start": 4},
                               
                               {"category" : u"kadeti",              "nr_start": 5},
                               {"category" : u"žáci starší",         "nr_start": 6},
                               {"category" : u"kadetky",             "nr_start": 7},                                                              
                               {"category" : u"žákyně starší",       "nr_start": 8},
                               
                               {"category" : u"kluci",               "nr_start": 9},
                               {"category" : u"holky",               "nr_start": 10},
                               {"category" : u"žáci nábor",          "nr_start": 11},
                               {"category" : u"žákyně nábor",        "nr_start": 12},
                               
                               {"category" : u"junioři",             "nr_start": 13},                               
                               {"category" : u"veteráni A",          "nr_start": 14},
                               {"category" : u"veteráni B",          "nr_start": 16},
                               {"category" : u"ženy",                "nr_start": 16},
                               
                               
                               {"category" : u"muži A",              "nr_start": 17},
                               {"category" : u"muži B",              "nr_start": 18},
                             ]              
             }
HORAZDOVICE_2011= { "name"   :   u"Horažďovické kolo 2011",
                    "starts" :   [ {"category" : u"kadeti",       "nr_start": 1},
                                   {"category" : u"kadetky",      "nr_start": 1},
                                   {"category" : u"junioři",      "nr_start": 1},
                                   {"category" : u"juniorky",     "nr_start": 1},
                                   {"category" : u"ženy",         "nr_start": 1},
                                   {"category" : u"veteráni I",   "nr_start": 1},
                                   {"category" : u"veteráni II",  "nr_start": 1},
                                   
                                   {"category" : u"muži I",       "nr_start": 2},
                                   {"category" : u"muži II",      "nr_start": 2},                                   
                                 ]              
                 }

KRALOVICE_2011= { "name"   :   u"Kralovický maraton MTB 2011",
                    "starts" :   [ 
                                   {"category" : u"DMEL",       "nr_start": 1},
                                   {"category" : u"DMH19",      "nr_start": 1},
                                   {"category" : u"DM30",       "nr_start": 1},
                                   {"category" : u"DM40",       "nr_start": 1},
                                   {"category" : u"DM50+",      "nr_start": 1},
                                   {"category" : u"DŽ19+",      "nr_start": 1},
                                   
                                   {"category" : u"KMH19",      "nr_start": 2},
                                   {"category" : u"KM30",       "nr_start": 2},
                                   {"category" : u"KM40",       "nr_start": 2},
                                   {"category" : u"KM50+",      "nr_start": 2},
                                   {"category" : u"KŽ19+",      "nr_start": 2},
                                   {"category" : u"KŽ16",       "nr_start": 2},
                                   {"category" : u"KM16",       "nr_start": 2},
                                   
                                   {"category" : u"MUŽI",       "nr_start": 3},
                                   {"category" : u"ŽENY",       "nr_start": 3}
                                                                                                         
                                 ]              
                 }

KRAPCUP_2011= { "name"   :   u"KřápKap 2011",
                    "starts" :   [ {"category" : u"KLASIK",          "nr_start": 1},
                                   {"category" : u"PITBIKE JUNIOR",  "nr_start": 1},
                                   {"category" : u"SPECIÁL",         "nr_start": 1},
                                   {"category" : u"PITBIKE OPEN",    "nr_start": 1},
                                   {"category" : u"VETERÁN",         "nr_start": 1}                                  
                                 ]              
                 }

#TABLE MODE
# EDIT - enable editing
# LOCK - disable editing
# REFRESH - automatic refreshing (disable editing)
MODE_EDIT, MODE_LOCK, MODE_REFRESH = range(3)

#USER ACTION
# ACTION_ENABLE - 
# ACTION_DISABLE - 
ACTIONS_ENABLE, ACTIONS_DISABLE = range(2)

#    
class GuiData():    
    def __init__(self):
        
        #MEASURE MODE
        #self.measure_mode = MODE_TRAINING_BASIC    
        self.measure_mode = MODE_RACE
        
        #measure_setting  => RACE & TRAINING SELECT
        if(self.measure_mode == MODE_RACE):
            #self.measure_setting = DEFAULT_RACE
            #self.measure_setting = BC_KRALOVICE
            #self.measure_setting = BLIZAK_2011
            #self.measure_setting = STUPNO_2011
            #self.measure_setting = HORAZDOVICE_2011
            #self.measure_setting = KRALOVICE_2011
            self.measure_setting = KRAPCUP_2011
            
        else:
            self.measure_setting = TRAINING_STANDART
        
        self.table_mode = MODE_EDIT
        self.user_actions = ACTIONS_ENABLE
        
    def getMesureModeString(self):
        return MEASURE_MODE_STRINGS[self.measure_mode]
    
    def getRaceName(self):          
        return self.measure_setting["name"]
    
    #get number of start according to user number
    def getStartNr(self, category):
        
        #TRAINING MODE
        if(self.measure_mode == MODE_TRAINING_BASIC) or (self.measure_mode == MODE_TRAINING):
            return 1
        
        #RACE MODE
        for start in self.measure_setting['starts']:        
            if(category == start['category']):                
                return start['nr_start']
        
        print "utikam", category,", ", start['category']
        return None
        
        
        