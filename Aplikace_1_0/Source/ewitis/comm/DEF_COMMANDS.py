# -*- coding: utf-8 -*-

'''
Created on 1.2.2012

@author: Meloun
'''

""" Komandy rozdělené do dvou sekcí GET a SET """
DEF_COMMANDS = {
            
            "GET":{
                   "terminal_info"  : 0x10,                                      
                   "cell_info"      : 0x10,                                      
                   "measure_info"   : 0x10,
                                                         
                   "run_par_index"  : 0x30,
                   "time_par_index" : 0x32
                   },
            
            "SET":{
                   "backlight"      : 0x10,
                   "time"           : 0x12,
                   "language"       : 0x00,
                }            
            }

        