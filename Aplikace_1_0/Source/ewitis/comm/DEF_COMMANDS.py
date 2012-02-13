# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

""" Komandy rozdělené do dvou sekcí GET a SET """
DEF_COMMANDS = {
            
            "GET":{
                   "cell_info"          : 0x10,                                      
                   "terminal_info"      : 0x20,                                      
                   "timing_settings"    : 0x22,
                                                         
                   "run_par_index"  : 0x30,
                   "time_par_index" : 0x32
                   },
            
            "SET":{
                   "backlight"      : 0x10,
                   "speaker"        : 0x11,
                   "time"           : 0x12,
                   "language"       : 0x00,
                }            
            }

        