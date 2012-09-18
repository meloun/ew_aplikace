# -*- coding: utf-8 -*-
'''
Created on 28.2.2012

@author: Meloun
'''

'''čísla záložek v TAB widgetu'''
class TAB:
    run_times, users, categories, cgroups, tags, device, timing_settings = range(0,7)

class UPDATE_MODE:
    all, tables, gui = range(0,3)

class LOGIC_MODES:
    basic, manual, single_mass, multiple_mass = range(1,5)  
    STRINGS =  {basic:"basic", manual:"manual", single_mass:"single_mass", multiple_mass:"multiple_mass"} 
class MEASUREMENT_STATE:
    not_active, prepared, time_is_running, finished = range(0,4)
    STRINGS =  {not_active:"Not Active", prepared:"Prepared, waiting for start", time_is_running:"Time is running", prepared:"Finished"}      
class LANGUAGES:
    czech, english = range(0,2)  
    STRINGS =  {czech:"čeština", english:"english"}