# -*- coding: utf-8 -*-
'''
Created on 28.2.2012

@author: Meloun
'''

'''čísla záložek v TAB widgetu'''
class TAB:
    run_times, users, categories, cgroups, tags, race_settings, actions, device = range(0,8)

class UPDATE_MODE:
    all, tables, gui = range(0,3)

#class LOGIC_MODES:
#    basic, manual, single_mass, multiple_mass_6b, multiple_mass_6c  = range(1,6)  
#    STRINGS =  {basic:"Basic", manual:"Manual", single_mass:"Single Mass", multiple_mass_6b:"multiple mass 6B", multiple_mass_6b:"multiple mass 6C"} 
class MEASUREMENT_STATE:
    not_active, prepared, time_is_running, finished = range(0,4)
    STRINGS =  {not_active:"Not Active", prepared:"Prepared, waiting for start", time_is_running:"Time is running", prepared:"Finished"}      
class LANGUAGES:
    czech, english = range(0,2)  
    STRINGS =  {czech:"čeština", english:"english"}
    
class STRINGS:
    MEASUREMENT_STATE =  {MEASUREMENT_STATE.not_active:"Not Active", MEASUREMENT_STATE.prepared:"Prepared, waiting for start", MEASUREMENT_STATE.time_is_running:"Time is running", MEASUREMENT_STATE.prepared:"Finished"}      
    PORT_CONNECT =  {False:"Disconnect", True: "Connect"}      