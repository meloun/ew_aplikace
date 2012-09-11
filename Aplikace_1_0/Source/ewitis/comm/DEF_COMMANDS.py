# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

""" Komandy rozdělené do dvou sekcí GET a SET """

DEF_COMMANDS = {
                
            #terminal => aplikace
            "GET_CELL_INFO"             : {'cmd':0x10, 'length':1},                                      
            "GET_TERMINAL_INFO"         : {'cmd':0x20, 'length':0},                                      
            "GET_TIMING_SETTINGS"       : {'cmd':0x22, 'length':0},                                      
            "GET_RUN_PAR_INDEX"         : {'cmd':0x30, 'length':1},                                      
            "GET_TIME_PAR_INDEX"        : {'cmd':0x32, 'length':1},
                                      
            #aplikace => terminal                                                  
            "SET_BACKLIGHT"             : {'cmd':0x10, 'length':1},                                      
            "SET_SPEAKER"               : {'cmd':0x11, 'length':3},                                      
            "SET_TIME"                  : {'cmd':0x12, 'length':7},                                      
            "SET_LANGUAGE"              : {'cmd':0x14, 'length':1},                                      
            "SET_TIMING_SETTINGS"       : {'cmd':0x23, 'length':6},                                      
            "ENABLE_START_CELL"         : {'cmd':0x41, 'length':0},
            "ENABLE_FINISH_CELL"        : {'cmd':0x42, 'length':0},
            "GENERATE_STARTTIME"    : {'cmd':0x43, 'length':4},
            "GENERATE_FINISHTIME"   : {'cmd':0x44, 'length':4}
                                                  
                                                  
            
}

        