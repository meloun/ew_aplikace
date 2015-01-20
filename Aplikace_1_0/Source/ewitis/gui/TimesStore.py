# -*- coding: utf-8 -*-
from ewitis.data.db import db
import pandas.io.sql as psql    
import pandas as pd


class TimesStore():
    '''
    tabulka startovních časů
        - Get()
        - Update() - volá se v TimesModel.Update()    
    '''
    def __init__(self):
        pass                                            
              
    def GetDefault(self):
        return {id:0, 'time_raw':0}
    

    
    def GetPrevious(self, user_time = None, cells = None):       
        
        time = {} 
        user_id = user_time['user_id']
        time_raw = user_time['time_raw']
        
        if(user_id == 0) or (user_id == None):            
            return None
        
        
        # user filter
        if user_id != None:
            df = self.groups.get_group(user_id)            
        
        #cell filter
        if cells != None:            
            df = df[df['cell'].isin(cells)]                       
                
        
        #group        
        try:            
            time = df[df.time_raw < time_raw].iloc[-1]                
            time = dict(time)                        
        except:                        
            time = None
                                   
        return time 
        
    '''
    
    '''
    def Get(self, nr, user_id = None, cells = None):
        time = {}
         
        # user filter
        if user_id == None:
            df = self.df
        else:
            df = self.groups.get_group(user_id)
        
        #cell filter
        if cells != None:
            df = df[df['cell'].isin(cells)]
               
            
        time = df.iloc[nr-1]
                    
        return dict(time)
    
    def GetFirst(self, user_id = None, cells = None):                    
        
        return self.Get(1, user_id, cells)
        
    def Update(self, run_id):
        '''
        najde všechny časy a uloží
        '''        
        df = psql.read_sql(\
                                "SELECT * FROM times" +\
                                " WHERE (times.run_id = "+ str(run_id ) +")"\
                                , db.getDb())
        
        #assign to global list
        self.df = df        
        self.groups = self.df.groupby("user_id")

timesstore = TimesStore() 

if __name__ == "__main__": 
            
    times = Timesstore()
    times.Update(6)
    print times.df
    print "prvni:", times.GetFirst()
    print "prvni start:", times.GetFirst(cells=[1])
    print "prvni finish:", times.GetFirst(cells=[250])
    print "prvni start nebo finish:", times.GetFirst(cells=[1, 250])
    #print "prvni 1:", times.GetFirst(cells=[1])
    print times.Get(1, 1)    
    print times.Get(2, 1)    
    #print starts.Get(0, user_id = 1)    
    #print starts.Get(1, user_id = 1)            
    #print times.GetPrevious({'user_id': None, 'time_raw': 50932})            
    
