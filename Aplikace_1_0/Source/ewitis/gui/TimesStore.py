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
        
    def UpdateExportDf(self):
        """
        update dataframes for export
        
        0: take tabbDf as basis (because of time-format 00:00:01:16)
           join dbDf and extend of userDf         
        1: Filter: Last times: take last time from each user
                   Best timesX: take best timeX from each user
        2: Sort: basic or nested sorting
        3: Selection: take only column you need
        
        return: filtred, sorted and selected dataframe for total export
                (for category export has to be filtred) 
        """                
                                         
        #update joinedDf        
        columns =  self.dbDf.columns - self.tabDf.columns                              
        joinedTabDf = self.tabDf.join(self.dbDf[columns])         
         
        #user update
        #userDf = psql.read_sql("SELECT * FROM users", db.getDb(), index_col = "id")        
        userDf = self.userDf #[["year", "club", "sex", "o1", "o2", "o3", "o4"]]
        joinedTabDf =  pd.merge(joinedTabDf,  userDf, left_on='user_id', right_index=True, how="inner")
        joinedTabDf.sort("time_raw", inplace=True)                                      
         
        #replace nan with None
        self.joinedTabDf = joinedTabDf.where(pd.notnull(joinedTabDf), None)        
        
        #update export df
        self.exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):
                          
            if (tabExportSettings.IsEnabled(i) == False):
                continue            
            
            #get export group            
            checked_info = dstore.GetItem('export', ["checked", i])
            
            #get export group
            filtersort = dstore.GetItem('export_filtersort', [i])
                                      
            #print group
            filter = filtersort['filter']
            sort1 = filtersort['sort1'].lower()  
            sort2 = filtersort['sort2'].lower()
            sortorder1 = True if(filtersort['sortorder1'].lower() == "asc") else False
            sortorder2 = True if(filtersort['sortorder2'].lower() == "asc") else False
            
            aux_df = self.joinedTabDf
            #filter 
            filter_split_keys = filter.split(" ")
            filter_keys = []
            for key in filter_split_keys:
                if(key in aux_df.columns):
                    filter_keys.append(key)
                
            #print filter_keys, len(filter_keys)
            
            if(len(filter_keys) == 1):
                #print "====", filter_keys
                aux_df =  aux_df[aux_df[filter_keys[0]] != ""]
                aux_df =  aux_df[aux_df[filter_keys[0]].notnull()]
                #print aux_df[filter_keys[0]]
                
            elif(len(filter_keys) == 2):
                aux_df =  aux_df[(aux_df[filter_keys[0]] != "") | (aux_df[filter_keys[1]] != "")]
                aux_df =  aux_df[(aux_df[filter_keys[0]] != None) | (aux_df[filter_keys[1]] != None)]
            
            #aux_df = self.joinedDf[(aux_df[column1].notnull()) & (self.joinedDf['user_id']!=0)]
            #last time from each user                    
            aux_df = aux_df.sort("time_raw")                        
            if("last" in filter):                                                                
                aux_df = aux_df.groupby("user_id", as_index = False).last()
            aux_df = aux_df.where(pd.notnull(aux_df), None)                        
            aux_df.set_index('id',  drop=False, inplace = True)
            
            #sort again
            if(sort2 in aux_df.columns):
                #print "nested sorting", sort1, sort2, sortorder1, sortorder2
                #print aux_df
                aux_df = aux_df.sort([sort1, sort2], ascending = [sortorder1, sortorder2])
            else:
                #print "basic sorting"
                aux_df = aux_df.sort(sort1, ascending = sortorder1)
                        
            #filter to checked columns
            columns = tabExportSettings.exportgroups[i].GetCheckedColumns()            
            
            for oc in range(0, NUMBER_OF.EXPORTS):
                ordercatX = 'ordercat'+str(oc+1)
                orderX = 'order'+str(oc+1)                
                aux_df[ordercatX] = aux_df[orderX].astype(str)+"./"+aux_df.category                        
                                   
            self.exportDf[i] = aux_df[columns]                            

        #print str(i), self.exportDf[i]                     
        return self.joinedDf         
                                                               
                    

    
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
    
