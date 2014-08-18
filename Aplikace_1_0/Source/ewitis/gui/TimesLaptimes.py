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
    OF_THIS_TIME, OF_LAST_TIME= range(0,2)
    def __init__(self):                          
        pass
    
    def Get(self, tabTime, nr):
        if(tabTime['time_raw'] == None):
            print "1a"            
            return None

        if(tabTime['cell'] == 1):  
            print "1b"          
            return None
                    
        if(tabTime['time_raw'] == 0):
            print "1c"            
            return None
        
        if(tabTime['user_id'] == 0):
            print "1d"            
            return None
        
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (tabTime['cell'] != 250):
            print "2"
            return None 
               
        if tabTime['lap'] < nr:
            print "3"
            return None
        
        ''' count of times - same race, same user, better time '''  
        #print "XX",tabTime['nr']
        if self.tabGroups.groups == {}:        
            return None         
        #print self.tabGroups.groups 
        laptimes = self.tabGroups.get_group(u'3').sort(['timeraw'])
        laptimes = laptimes[laptimes.lap == str(nr)]               
        try:
            laptime = laptimes[laptimes.lap == str(nr)].iloc[-1]['laptime']                          
        except IndexError:
            print tabTime['id'],":IndexError:", laptimes
            laptime = None
            
        if laptime != None:
            try:
                laptime = int(laptime)
            except:
                pass
        
        print tabTime['id'],":", laptime                       
        return laptime # int or none  
        
        
        
                
    def Calc(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''        
        if(dbTime['time_raw'] == None):            
            return None

        if(dbTime['cell'] == 1):            
            return None
                    
        if(dbTime['time_raw'] == 0):            
            return None
        
        if(dbTime['user_id'] == 0):            
            return None
        
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (dbTime['cell'] != 250):
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
        
    def GetNrOfLap(self, dbTime, mode = OF_THIS_TIME):
        '''
        číslo kola
        '''
        if(dbTime['time_raw'] == None) or (dbTime['time_raw'] == 0):
            return None
        if(dbTime['cell'] == 1):            
            return None                            
        if(dbTime['user_id'] == 0):          
            return None
        #laptime evaluation: only finishtime AND thistime is not finishtime
        if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ONLY_FINISHTIME) and (dbTime['cell'] != 250):
            return None 
               
        '''count of times - same race, same user, better time, exclude start time'''
        #lap_count = None        
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
        
        #
        self.tabDf = tabDf
        self.tabGroups =  self.tabDf.groupby("nr")
        #print "tabDf", self.tabDf
        
        
        query = " SELECT * FROM times"+\
                " WHERE (times.run_id = "+ str(run_id) +")"+\
                " AND (times.cell != 1)"
        
        #0:only finishtime, 1:all times
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
    