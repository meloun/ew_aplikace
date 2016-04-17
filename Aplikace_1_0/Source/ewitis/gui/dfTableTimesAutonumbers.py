# -*- coding: utf-8 -*-
'''
Created on 10. 4. 2016

@author: Meloun
'''
import time, os
import pandas as pd
import libs.pandas.df_utils as df_utils
from ewitis.data.dstore import dstore

def Update(df):    
    ret = []
    times = dstore.GetItem("gui", ["update_requests", "new_times"])    
    
    cells = dstore.GetItem("racesettings-app", ["autonumbers", "cells"])
    nr_cells = dstore.GetItem("racesettings-app", ["autonumbers", "nr_cells"])
    
    """for all new times"""        
    for time in times:
        """for one new time"""
        #print "time", time
        
        for number in dstore.GetItem("times", ["auto_number"]):            
            """test if this user should be taken"""
            #print "number", number    
            
            #number not set        
            if number == 0:
                continue
            
            #get position of new time (first from defined list)
            try:
                cell_position = cells.index(time["cell"])
                #print "tp:", time_position            
            except ValueError:
                continue
                      
            # get starttime 
            starttime = GetStartime(df, number)
            #print "starttime:", starttime
           
            #print "df columns:", df.columns
            
            if starttime != None:                                    
                sequence_times = df[(df.nr==number)  & (df.id >= starttime['id'])]
                sequence_cells = list(sequence_times.cell)
            else:
                sequence_cells = [] 

            if (
                    (time["cell"]) == 1 and (sequence_cells ==  cells[:nr_cells]) or
                    (sequence_cells ==  cells[:cell_position])
                ):
                
                print "I: auto number: MATCH nr.", number
                ret.append({"id":time["id"], "nr": number})                
                if cell_position == (nr_cells - 1):
                    print "I: auto number: run finished - shifting nr.", number
                    ShiftNumbers()
                return ret
            else:
                print "I: auto number: NO MATCH nr.", number, sequence_cells, cells[:cell_position]
                                                
    return ret
        
def GetStartime(df, nr):
    
    if df.empty:
        return None
    
    try:      
        starttime = df[(df.nr==nr) & (df.cell ==1)].iloc[-1]
        starttime = dict(starttime)
    except IndexError, AttributeError:
        starttime = None
    
    return starttime
    

def ShiftNumbers():        
    nrs = dstore.GetItem("times", ["auto_number"])
    nrs = nrs[1:]+[0]
    dstore.SetItem("times", ["auto_number"], nrs)
    
        
