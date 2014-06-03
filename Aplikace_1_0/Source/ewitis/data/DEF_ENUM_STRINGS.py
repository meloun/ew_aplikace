# -*- coding: utf-8 -*-
'''
Created on 28.2.2012

@author: Meloun
'''

from ewitis.data.DEF_DATA import *

'''čísla záložek v TAB widgetu'''
#class TAB:
#    nr_tabs = 15
#    run_times, users, categories, cgroups, tags, alltags, points, race_info, race_settings, device, cells, diagnostic, communication, manual, about = range(0, nr_tabs)

class UPDATE_MODE:
    all, tables, gui = range(0,3)
 
         
class STRINGS:
    MEASUREMENT_STATE =  {MeasurementState.not_active:"Not Active", MeasurementState.prepared:"Prepared, waiting for start", MeasurementState.time_is_running:"Time is running", MeasurementState.finished:"Finished"}      
    PORT_CONNECT =  {False: "Disconnect", True: "Connect"}
    LANGUAGES = {Languages.CZECH: "čeština", Languages.ENGLISH:"english"}
    ORDER_EVALUATION = {OrderEvaluation.RACE:"Race", OrderEvaluation.SLALOM:"Slalom"}
    
class COLORS:
    green = "#90EE90"
    red = "#ff7f50" 
    orange = "#ffa500"
    none = ""
    
    @staticmethod
    def GetColor(key, enabled = True):                   
        
        if bool(enabled) == False:
            return COLORS.none
        
        if key == None:
            return COLORS.none

        #boolean
        if isinstance(key, bool):
            if key == True:
                return COLORS.green
            else:
                return COLORS.red
        
        return COLORS.none      