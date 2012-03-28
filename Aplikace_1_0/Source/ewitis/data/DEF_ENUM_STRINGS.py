# -*- coding: utf-8 -*-
'''
Created on 28.2.2012

@author: Meloun
'''

'''čísla záložek v TAB widgetu'''
TABS = {"run_times":0, "users":1, "categories":2, "tags":3, "terminal_cells":4, "timing_settings":5}

class LOGIC_MODES:
    basic, manual, single_mass, multiple_mass = range(1,5)  
    STRINGS =  {basic:"basic", manual:"manual"} 

class LOGIC_MODES:
    basic, manual, single_mass, multiple_mass = range(1,5)  
    STRINGS =  {basic:"basic", manual:"manual"} 
class MEASUREMENT_STATE:
    not_active, prepared, time_is_running, finished = range(0,4)
    STRINGS =  {not_active:"Not Active", prepared:"Prepared, waiting for start", time_is_running:"Time is running", prepared:"Finished"}      
class LANGUAGES:
    czech, english = range(0,2)  
    STRINGS =  {czech:"čeština", english:"english"}