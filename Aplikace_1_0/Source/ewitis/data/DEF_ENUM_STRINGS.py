# -*- coding: utf-8 -*-
'''
Created on 28.2.2012

@author: Meloun
'''

from ewitis.data.DEF_DATA import *

'''čísla záložek v TAB widgetu'''
class TAB:
    nr_tabs = 16
    run_times, users, categories, cgroups, tags, alltags, points, race_info, race_settings, actions, device, diagnostic, cells, communication, manual, about = range(0, nr_tabs)

class UPDATE_MODE:
    all, tables, gui = range(0,3)

#class LOGIC_MODES:
#    basic, manual, single_mass, multiple_mass_6b, multiple_mass_6c  = range(1,6)  
#    STRINGS =  {basic:"Basic", manual:"Manual", single_mass:"Single Mass", multiple_mass_6b:"multiple mass 6B", multiple_mass_6b:"multiple mass 6C"} 
         
class STRINGS:
    MEASUREMENT_STATE =  {MeasurementState.not_active:"Not Active", MeasurementState.prepared:"Prepared, waiting for start", MeasurementState.time_is_running:"Time is running", MeasurementState.finished:"Finished"}      
    PORT_CONNECT =  {False: "Disconnect", True: "Connect"}
    LANGUAGES = {Languages.CZECH: "čeština", Languages.ENGLISH:"english"}
    ORDER_EVALUATION = {OrderEvaluation.RACE:"Race", OrderEvaluation.SLALOM:"Slalom"}
    
class COLORS:
    green = "#90EE90"
    red = "#FF6347"      