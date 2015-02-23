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
        filter dataframe according to pattern        
        '''
                                      
        if filter != None:        
            for k,v in filter.iteritems():                
                try:
                    #replace
                    v = str(v)
                    if(v == "2"):
                        v="2$"                
                    v = v.replace("2|", "2$|") #cell=2|250
                    
                    # filter frame                                                                                                                                                                                                                                                           
                    df = df[df[k].astype(str).str.match(str(v))]                                        
                except KeyError:
                    print "error: race settings: filter", filter               
        return df

    
    def GetPrevious(self, dbTime, filter = None, df = None):
        print "funguju A"
        
        if(dbTime['user_id'] == 0) or (dbTime['user_id'] == None):            
            return None
        
        # user and previous filter
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw < dbTime['time_raw'])]             
        
        #filter
        #print filter, type(filter)
        df =  self.FilterFrame(df, filter)                       
                
        
        #group        
        try:            
            time = df[df.time_raw < dbTime['time_raw']].iloc[-1]                
            time = dict(time)                        
        except:                        
            time = None
            
        print "funguju B"
                                   
        return time 
        
    '''
    
    '''
    def Get(self, df, nr, filter = None):
        time = {}
        
        #filter
        df = self.FilterFrame(df, filter)                      
               
            
        time = df.iloc[nr-1]
                    
        return dict(time)
    
    def GetFirst(self, filter = None):                    
        
        return self.Get(1, filter)
        

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
        df.set_index('id',  drop=False, inplace = True)
        
        #assign to global list
        #self.all = {'df':df, groups: self.df.groupby("user_id")}
        
        #self.df = df        
        #self.groups = self.df.groupby("user_id")
        
        return df

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
    
