# -*- coding: utf-8 -*-
from ewitis.data.db import db
import pandas.io.sql as psql    
import pandas as pd
import time
from ewitis.data.DEF_DATA import *
from ewitis.data.dstore import dstore
import libs.timeutils.timeutils as timeutils
import ewitis.gui.TimesUtils as TimesUtils

#nešlo by to bez?
from ewitis.gui.tableUsers import tableUsers
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tabExportSettings import tabExportSettings

import libs.pandas.df_utils as df_utils
 


class TimesStore():
    '''
    tabulka startovních časů
        - Get()
        - Update() - volá se v TimesModel.Update()    
    '''
    #GET_ALL, ONLY_SMALLER, ONLY_BIGGER= range(0,3)
    #SOURCE_DF, SOURCE_FILTERED_DF = range(0,2)    
    def __init__(self):
        pass
        self.all = {}
        self.filtered = {}  
        self.joinedDf = pd.DataFrame()                                          
              
    def GetDefault(self):
        return {id:0, 'time_raw':0}
    
    def GetPrevious(self, dbTime, filter = None, df = None):        
        
        if(dbTime['user_id'] == 0) or (dbTime['user_id'] == None):            
            return None
        
        # user and previous filter
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw < dbTime['time_raw'])]             
        
        #filter        
        df =  df_utils.Filter(df, filter)                                       
        
        #group        
        try:            
            time = df[df.time_raw < dbTime['time_raw']].iloc[-1]                
            time = dict(time)                        
        except:                        
            time = None                    
                                   
        return time
        

                                                               
                    

    
    def IsFinishTime(self, dbTime): 
        
        if self.IsTimeToCalc(dbTime) == False:
            return False       
        
        eval_finish = dstore.GetItem("evaluation", ['finishtime'])
        
        if(dbTime['time1'] < TimesUtils.TimesUtils.timestring2time(eval_finish["time"], including_days = False)):
            return False
        
        if(dbTime['lap1'] < eval_finish["laps"]):
            return False
            
        return True

 
    
def GetStarttime(db, user_id):
    # STARTTIME    
    
    #user without number => no time        
    starttime = None          
    tabUser =  tableUsers.getTabUserParIdOrTagId(user_id)          
    if(tabUser['nr'] == 0):
        return None        

    if(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):
        #VIA CATEGORY => Xth starttime                                                                                                                
        start_nr = tableCategories.getTabRow(tabUser['category_id'])['start_nr'] #get category starttime                
        starttime = timesstore.Get(df, start_nr, filter = {'cell':1})                                                                                        
    elif(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
        #VIA USER => previous startime from the same user                                                
        starttime = timesstore.GetPrevious(joinTime, filter = {'cell':1}, df = df)
    else:
        print "E: Fatal Error: Starttime "
        return None
                            
    if starttime == None:
        return None
    
    
 
    


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
    
