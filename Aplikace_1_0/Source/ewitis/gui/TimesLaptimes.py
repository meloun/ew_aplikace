# -*- coding: utf-8 -*-
'''
Created on 14.07.2014

@author: Meloun
'''
from ewitis.data.DEF_DATA import *
from ewitis.data.db import db
from ewitis.data.dstore import dstore
from ewitis.data.db import db
import pandas.io.sql as psql    
import pandas as pd
import numpy as np



class TimesLaptime():
    '''
        - Get() - laptime, tzn. čas kola
        - GetBest() - nejlepší čas kola
    '''
    
    def __init__(self):                          
        pass
    
    def Get(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
#        if  dstore.Get("additional_info")['enabled'] == 0:
#            return None 
#        
#        if dstore.Get("additional_info")['laptime'] == 0:
#            return None                                       
        
        if(dbTime['time_raw'] == None):
            #print "laptime: neni time_raw", dbTime
            return None

        if(dbTime['cell'] == 1):
            #print "laptime: spatna cell", dbTime
            return None
                    
        if(dbTime['time_raw'] == 0):
            #print "laptime: zero time_raw", dbTime
            return None
        
        if(dbTime['user_id'] == 0):
            #print "laptime: neni user", dbTime
            return None
        
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (dbTime['cell'] != 250):
            return None 
        
        if(dbTime['laptime']) != None:
            return dbTime['laptime']                
        
        #  '''count of times - same race, same user, better time, exclude start time'''        
        laptimes = self.groups.get_group(dbTime['user_id']).sort(['time_raw'])
        try:    
            #laptimes = laptimes[laptimes.time_raw < dbTime['time_raw']]                                                      
            #laptime_time = laptimes.iloc[-1]['time_raw']            
            laptime_time = laptimes[laptimes.time_raw < dbTime['time_raw']].iloc[-1]['time_raw']
            laptime = dbTime['time_raw'] - laptime_time                               
        except IndexError:            
            laptime = dbTime['time']
            
        if laptime != None:
            laptime = int(laptime)

        #return laptime (int or none)                       
        return laptime    
        
    def GetBest(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
        
#        if dstore.Get("additional_info")['enabled'] == 0:
#            return None
#        
#        if dstore.Get("additional_info")['best_laptime'] == 0:
#            return None              
                               
        if(dbTime['time_raw'] == None):            
            return None;

        if(dbTime['cell'] == 1):            
            return None
                    
        if(dbTime['time_raw'] == 0):            
            return None
        
        if(dbTime['user_id'] == 0):            
            return None
        
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (dbTime['cell'] != 250):
            return None
        
        '''count of times - same race, same user, better time, exclude start time'''
        try:                
            laptime = self.groups.get_group(dbTime['user_id']).sort(['laptime']).iloc[0]['laptime']
            laptime = int(laptime)
        except:                    
            laptime = None                                    
            
        #return laptime (int or none)                    
        return laptime
    '''
    počty kol
        - Get(dbTime) - kolikáté kolo daného závodníka je tento čas
        - GetLaps() - počet kol daného závodníka
    '''
    def GetLap(self, dbTime, ):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
#        if  dstore.Get("additional_info")['enabled'] == 0:
#            return None         
#        if dstore.Get("additional_info")['lap'] == 0:
#            return None                                               
        if(dbTime['time_raw'] == None) or (dbTime['time_raw'] == 0):            
            return None
        if(dbTime['cell'] == 1):            
            return None                            
        if(dbTime['user_id'] == 0):          
            return None
               
        '''count of times - same race, same user, better time, exclude start time'''        
        try:
            lap_count = None      
            laptimes = self.groups.get_group(dbTime['user_id'])
            laptimes = laptimes[laptimes.time_raw < dbTime['time_raw']]
            if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME):        
                laptimes = laptimes[laptimes.cell == 250]
            else:
                laptimes = laptimes[laptimes.cell != 1]                                        
            lap_count = len(laptimes.index)+1
        except KeyError: #nenalezen spravny cas 
            lap_count = None            

        #return laptime (int or none)                       
        return lap_count
        
    def GetLaps(self, dbTime):
        '''
        celkový počet kol daného závodníka
        '''

        if(dbTime['cell'] == 1):            
            return None                            
        if(dbTime['user_id'] == 0):          
            return None
               
        '''count of times - same race, same user, better time, exclude start time'''
        #lap_count = None        
        try:
            laptimes = self.groups.get_group(dbTime['user_id'])            
            if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME):        
                laptimes = laptimes[laptimes.cell == 250]
            else:
                laptimes = laptimes[laptimes.cell != 1]
            lap_count = len(laptimes.index)                                        
        except: #nenalezen spravny cas             
            lap_count = None            
                
        return lap_count # int or none    
                         
    

    
    def Update(self, run_id):
        '''
        najde všechny časy potřebné pro laptime a uloží
        '''
        query = " SELECT * FROM times"+\
                " WHERE (times.run_id = "+ str(run_id) +")"
        
        #0:only finishtime, 1:all times
        if(dstore.Get("evaluation")['laptime']) == 0:
            query = query + " AND (times.cell == 250 )"        
            
            
        query = query + \
            " AND (times.run_id = "+ str(run_id) +")"+\
            " ORDER BY times.time ASC"                                  
        
        #get dataframe
        df = psql.read_frame(query, db.getDb())
        
        #assign to global variables
        #self.df = df        
        self.groups = df.groupby("user_id")        
    