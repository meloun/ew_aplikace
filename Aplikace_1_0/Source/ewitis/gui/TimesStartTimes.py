# -*- coding: utf-8 -*-
from ewitis.data.db import db
import pandas.io.sql as psql    
import pandas as pd


class TimesStarts():
    '''
    tabulka startovních časů
        - Get()
        - Update() - volá se v TimesModel.Update()    
    '''
    def __init__(self):
        pass                                            
              
    def GetDefault(self):
        return {id:0, 'time_raw':0}
    
    def GetFirst(self):
        starttime = {}                 
        starttime = self.df.iloc[0]                    
        return dict(starttime)
    
    def GetLast(self, user_time = None):        
        
        starttime = {} 
        user_id = user_time['user_id']
        time_raw = user_time['time_raw']
        
        if(user_id == 0):
            return self.GetFirst()
        
        #print "AA", user_time
#        print self.df
#        print self.groups.get_group(user_id)
        #group        
        try:
            starttime_group = self.groups.get_group(user_id)
            if user_id == None:
                starttime = self.df.iloc[-1]
            else:
                starttime = starttime_group[starttime_group.time_raw < time_raw].iloc[-1]
                
            starttime = dict(starttime)            
        except:
            #starttime = pd.Series()
            starttime = None
                                   
        return starttime 
        
    def Get(self, nr, user_id = None):
        starttime = {} 
        if user_id == None:
            starttime = self.df.iloc[nr-1]
        else:
            starttime = self.groups.get_group(user_id).iloc[nr-1]
                    
        return dict(starttime)
        
    def Update(self, run_id):
        '''
        najde všechny startovací časy a uloží
        '''        
        #df = psql.read_frame(\
        df = psql.read_sql(\
                                "SELECT * FROM times" +\
                                " WHERE (times.cell = 1 )" +\
                                " AND (times.run_id = "+ str(run_id ) +")"\
                                " ORDER BY times.time"  
                                , db.getDb())
        
        #assign to global list
        self.df = df        
        self.groups = self.df.groupby("user_id")


if __name__ == "__main__": 
        
    starts = TimesStarts()
    starts.Update(6)
    print starts.df    
    #print starts.Get(0, user_id = 1)    
    #print starts.Get(1, user_id = 1)            
    print starts.GetLast({'user_id': 1, 'time_raw': 50933})            
    
