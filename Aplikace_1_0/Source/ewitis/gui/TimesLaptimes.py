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
        - Get(self, dbTime, nr) - laptime, tzn. čas kola
        - Calc(self, dbTime)
        - GetBest(self, dbTime) - nejlepší čas kola
        - GetNrOfLap(self, dbTime, mode = OF_THIS_TIME) - číslo daného kola (nebo všech)        
    '''
    OF_THIS_TIME, OF_LAST_TIME= range(0,2)
    def __init__(self):                          
        pass
    
    def IsValid(self, dbTime):
                
        if(dbTime['time_raw'] == None) or (dbTime['time_raw'] == 0):      
            return False

        if(dbTime['cell'] == 1):       
            return False                    
        
        if(dbTime['user_id'] == 0):                        
            return False
        
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (dbTime['cell'] != 250):            
            return False
        
        #everything ok
        return True
    
    def Get(self, dbTime, nr):
        '''
        vyhledá daný laptime (vyhodnocení bodů, laptime1, ..)
        '''
        
        if(self.IsValid(dbTime) == False):
            return None 
               
        if dbTime['lap'] < nr:            
            return None
        
        ''' count of times - same race, same user, better time '''     
        laptimes = self.groups.get_group(dbTime['user_id']).sort(['time_raw'])                                    
        try:
            laptime = laptimes[laptimes.lap == nr].iloc[-1]['laptime']                          
            laptime = int(laptime)
        except:            
            laptime = None            
        
        #print dbTime['id'],":", laptime, type(laptime)                       
        return laptime # int or none                        
                
    def Calc(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
                
        if(self.IsValid(dbTime) == False):
            return None  
        
        if(dbTime['laptime']) != None:
            return dbTime['laptime']                
        
        ''' count of times - same race, same user, better time '''        
        laptimes = self.groups.get_group(dbTime['user_id']).sort(['time_raw'])
        try:
            laptime_time = laptimes[laptimes.time_raw < dbTime['time_raw']].iloc[-1]['time_raw']
            laptime = dbTime['time_raw'] - laptime_time                               
        except IndexError:            
            laptime = dbTime['time']
            
        if laptime != None:
            laptime = int(laptime)
                               
        return laptime # int or none    
        
    def GetBest(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''                                             
        if(self.IsValid(dbTime) == False):
            return None
        
        '''count of times - same race, same user, better time, exclude start time'''
        try:                
            laptime = self.groups.get_group(dbTime['user_id']).sort(['laptime']).iloc[0]['laptime']
            laptime = int(laptime)
        except:                    
            laptime = None                                    
            
        #return laptime (int or none)                    
        return laptime
        
    def GetNrOfLap(self, dbTime, mode = OF_THIS_TIME):
        '''
        číslo kola
        '''
        
        if(self.IsValid(dbTime) == False):
            return None 
               
        '''count of times - same race, same user, better time, exclude start time'''               
        try:
            laptimes = self.groups.get_group(dbTime['user_id'])
            if mode == self.OF_THIS_TIME:
                laptimes = laptimes[laptimes.time_raw <= dbTime['time_raw']]                                                    
            lap_count = len(laptimes.index)
        except KeyError: #nenalezen spravny cas             
            lap_count = None            
                
        return lap_count # int or none    
                         
    

    
    def Update(self, run_id, tabDf):
        '''
        najde všechny časy potřebné pro laptime a uloží
        '''                        
        
        query = " SELECT * FROM times"+\
                " WHERE (times.run_id = "+ str(run_id) +")"+\
                " AND (times.cell != 1)"
        
        #0:only finishtime, 2:all times
        if(dstore.Get("evaluation")['laptime']) == LaptimeEvaluation.ONLY_FINISHTIME:            
            query = query + " AND (times.cell == 250 )"        
            
            
        query = query + \
            " ORDER BY times.time ASC"                                  
        
        #get dataframe
        df = psql.read_frame(query, db.getDb())
        
        #assign to global variables
        #self.df = df        
        self.groups = df.groupby("user_id")
        
        
cLaptime = TimesLaptime()                 
    