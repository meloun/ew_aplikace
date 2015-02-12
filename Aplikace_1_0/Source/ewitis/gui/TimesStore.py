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
    GET_ALL, ONLY_SMALLER, ONLY_BIGGER= range(0,3)
    SOURCE_DF, SOURCE_FILTERED_DF = range(0,2)
    def __init__(self):
        pass
        self.all = {}
        self.filtered = {}                                            
              
    def GetDefault(self):
        return {id:0, 'time_raw':0}
             
                        
    def FilterFrame(self, df, filter):
        '''
        filter the filtered frame        
        '''
        
                                      
        if filter != None:        
            for k,v in filter.iteritems():                
                try:
                    v = str(v)
                    if(v == "2"):
                        v="2$"                
                    v = v.replace("2|", "2$|") #cell=2|250                                                                                                                                                                                                                                                            
                    df = df[df[k].astype(str).str.match(str(v))]                                        
                except KeyError:
                    print "error: race settings: filter", filter               
        return df    
    

    
    def GetPrevious(self, user_time = None, filter = None):       
        
        time = {} 
        user_id = user_time['user_id']
        time_raw = user_time['time_raw']
        
        if(user_id == 0) or (user_id == None):            
            return None
        
        
        # user filter
        if user_id != None:
            df = self.groups.get_group(user_id)            
        
        #filter
        df =  self.FilterFrame(df, filter)                       
                
        
        #group        
        try:            
            time = df[df.time_raw < time_raw].iloc[-1]                
            time = dict(time)                        
        except:                        
            time = None
                                   
        return time 
        
    '''
    
    '''
    def Get(self, nr, user_id = None, filter = None):
        time = {}
         
        # user filter
        if user_id == None:
            df = self.df
        else:
            df = self.groups.get_group(user_id)
        
        #filter
        df = self.FilterFrame(df, filter)                      
               
            
        time = df.iloc[nr-1]
                    
        return dict(time)
    
    def GetFirst(self, user_id = None, filter = None):                    
        
        return self.Get(1, user_id, filter)
    
   
    def GetNrOf(self, df, column, dbTime, mode = GET_ALL, filter = None):
        '''
        počet
        '''        
        if(dbTime['time_raw'] == None) or (dbTime['time_raw'] == 0):      
            return None
        
        # one user filter
        if dbTime != None:
            df = df[df['user_id'] == dbTime['user_id']]            
                    
        #filter        
        #if filter != None:
        #    df =  self.FilterFrame(df, filter) 
        
        '''count of times - same race, same user, better time, exclude start time'''        
        if mode == TimesStore.ONLY_SMALLER:
            df = df[df[column] < dbTime[column]]           
                    
        try:                                                  
            lap_count = len(df[column])
        except KeyError:            
            lap_count = None  
        
        #print "po",lap_count, dbTime, df
        return lap_count # int or none    

    def Filter(self, run_id):
      
        self.groups = self.df.groupby("user_id")
                
    def Update(self, run_id):
        '''
        najde všechny časy a uloží
        '''        
        df = psql.read_sql(\
                                "SELECT * FROM times" +\
                                " WHERE (times.run_id = "+ str(run_id ) +")"\
                                , db.getDb())
        
        #assign to global list
        #self.all = {'df':df, groups: self.df.groupby("user_id")}
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
    
