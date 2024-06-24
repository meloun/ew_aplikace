# -*- coding: utf-8 -*-
'''
Created on 29.05.2015

@author: Lubos Melichar
'''

import sys, time
import pandas.io.sql as psql    
import pandas as pd
import numpy as np
import libs.sqlite.sqlite_utils as db_utils
import libs.pandas.df_utils as df_utils
from ewitis.data.DEF_DATA import *
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from ewitis.gui.multiprocessingManager import eventCalcNow, eventCalcReady
import ewitis.gui.TimesUtils as TimesUtils
import os

def getDf():
    myheader = ["name", "test2", "test3"]
    random_nr = int(round(time.clock() * 13))            
    myrow1 =   [ random_nr,  random_nr+400, 250]
    myrow2 =   [ random_nr+1,  random_nr+400, 250]
    df = pd.DataFrame([myrow1]*100 + [myrow2]*100, columns = myheader)
    return df

def xprint(*args):
    print( args )    

class ProcessDstore():
    def __init__(self, data):
        self.data = data
        
    def GetData(self):        
        return self.data
    def Get(self, name):        
        return self.data[name]
    
    def GetItem(self, name, keys):        
        item = self.data[name]
        
        for key in keys:                      
            if (key not in item) and not isinstance(key, int):
                return None
            item = item[key]                

        return item        



class ManageCalcProcess():            
    def __init__(self):         
        self.maxcalctime = 0
        self.commit_flag = False 
             
    def CommitRequest(self):
        self.commit_flag = True
    
    def Commit(self):
        if self.commit_flag:
            db_utils.commit(self.db) 
            self.commit_flag = False
            
    def run_fast(self, dstore, dfs, info, eventCalcNow, eventCalcReady):
        """ update joined DF"""
        #self.GetJoinedDf()
        pass
        
    def run(self, dstore, dfs, info, eventCalcNow, eventCalcReady):
        
        print "DEBUG: ", __debug__
        print "INFO: ", info
        #@print "I:P: CALC: zakladam process.." #, dstor
        self.dstore = ProcessDstore(dstore)    
        #@print "I:P: CALC: dstore.." #,  self.dstore.GetData()
                                    
        
        """ DATABASE """                
        try:           
            self.db = db_utils.connect("db/test_db.sqlite")
        except:                    
            print "E: Database"
            
        sys.stdout = sys.__stdout__
            
        complete_calc_flag = False
        
        '''casy ktere je nutné updatovat'''
        self.timesDfs = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
        self.lapsDfs = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]    
        self.orderDfs = [{'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}]
        
        while(1):                                               
            #=====================================================================
            #=====================================================================
            # NORMAL
            #=====================================================================
            #=====================================================================
           # if __debug__: print "P: C: START ------------------------"
            #delay            
            ztime = time.clock()
            
            #
            if(eventCalcReady.is_set() == False):
                complete_calc_flag = True 
            
            
            """ run fast """
            self.run_fast(dstore, dfs, info, eventCalcNow, eventCalcReady)
            
            """ update DFs """
           # if __debug__: ytime = time.clock() 
            self.ucDf = self.GetUserCategoryDf()
           # if __debug__: print "P1: C: GetUserCategoryDf()", (time.clock() - ytime)*1000,"ms"
            
            """ update joined DF"""
           # if __debug__: ytime = time.clock() 
            self.GetJoinedDf()
           # if __debug__: print "P2: C: GetJoinedDf() 1", (time.clock() - ytime)*1000,"ms"
            
            """ update times """
           # if __debug__: ytime = time.clock() 
            #update self.timesDfs[]
            self.GetTimesDfs() 
            #calc and update times in DB
            self.UpdateTimes(self.timesDfs)
            #print "#3", self.joinedDf
           # if __debug__: print "P3: C: UpdateTimes()", (time.clock() - ytime)*1000,"ms"

            #laps
           # if __debug__: ytime = time.clock()
            self.GetLapsDfs()
           # if __debug__: print "P4a: C: UpdateLaps()", (time.clock() - ytime)*1000,"ms"
            ret = self.UpdateLaps(self.lapsDfs)
           # if __debug__: print "P4b: C: UpdateLaps()", (time.clock() - ytime)*1000,"ms"
            if ret:
                self.GetJoinedDf()  
            #print "#4", self.joinedDf
           # if __debug__: print "P4: C: UpdateLaps()", (time.clock() - ytime)*1000,"ms"

            #orderX
            ytime = time.clock()                        
           # if __debug__: print "P5: C: UpdateOrder()", (time.clock() - ytime)*1000,"ms"
            #points                                                  
            ytime = time.clock()
            #!self.joinedDf = self.UpdatePoints(self.joinedDf)                
            self.UpdatePoints(self.joinedDf)
            #if (info["wdg_calc"] % 2 == 0) or (info["wdg_calc"]==0):
            #    self.joinedDf = self.UpdatePoints(self.joinedDf)                
            #else:
            #    self.joinedDf["points1"] = dfs["table"]["points1"]
            #    self.joinedDf["points2"] = dfs["table"]["points2"]
            #    self.joinedDf["points3"] = dfs["table"]["points3"]
            #    self.joinedDf["points4"] = dfs["table"]["points4"]
            #    self.joinedDf["points5"] = dfs["table"]["points5"]
            #    self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)             
           # if __debug__: print "P6: C: UpdatePoints()", (time.clock() - ytime)*1000,"ms"
            
            #orderX 
           # if __debug__: ytime = time.clock()
            self.GetOrderDfs()                
           # if __debug__: print "P7a: C: UpdateOrder()", (time.clock() - ytime)*1000,"ms"
            self.UpdateOrder()
            #if (info["wdg_calc"] % 2 == 1) or (info["wdg_calc"]==0):
            #    self.UpdateOrder()
            #else:
            #    self.joinedDf["order1"] = dfs["table"]["order1"]
            #    self.joinedDf["order2"] = dfs["table"]["order2"]
            #    self.joinedDf["order3"] = dfs["table"]["order3"]
            #    self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)             
           # if __debug__: print "P7: C: UpdateOrder()", (time.clock() - ytime)*1000,"ms"
            
            #update status                                                 
            #self.joinedDf = self.GetJoinedDf()
            
            #convert times to string format
           # if __debug__: ytime = time.clock()
            self.joinedDf = self.df2tableDf(self.joinedDf)
           # if __debug__: print "P8: C: Convert", (time.clock() - ytime)*1000,"ms"
            #print "#5", self.joinedDf
            
            #time.sleep(6)
            
            #sort and copy 
           # if __debug__: ytime = time.clock()
            columns = [item[0] for item in sorted(DEF_COLUMN.TIMES['table'].items(), key = lambda (k,v): (v["index"]))]                   
            if self.joinedDf.empty:
                dfs["table"] = pd.DataFrame(columns=columns)                            
            else:                              
                #self.joinedDf.loc[self.joinedDf.user_id == 0,  self.joinedDf.columns - ["id", "cell"]] = None             
                self.joinedDf.loc[self.joinedDf.user_id == 0, ["nr", "name", "category", "start_nr", "time1", "time2", "time3", "time4", "lap1", "lap2", "lap3", "lap4"]] = [0, "UNKNOWN unknown", "not def", 1, None, None, None, None, None, None, None, None]
                                
                #print "#6", self.joinedDf                                
                #self.joinedDf.loc[pd.isnull(self.joinedDf.nr) , ["nr", "name", "category", "start_nr", "time1", "time2", "time3", "lap1", "lap2", "lap3"]] = [0, "UNKNOWN user id: "+self.joinedDf[pd.isnull(self.joinedDf.nr)]["user_id"].astype(str), "not def", 1, None, None, None, None, None, None]
                self.joinedDf.loc[pd.isnull(self.joinedDf.nr) , ["nr", "name", "category", "start_nr", "time1", "time2", "time3", "time4", "lap1", "lap2", "lap3", "lap4"]] = [0, "UNKNOWN user", "not def", 1, None, None, None, None, None, None, None, None]
                
                #print "#7", self.joinedDf
                #umele pretypovani na long, defaultne float a 7.00
                self.joinedDf["nr"] = self.joinedDf["nr"].astype(long)
                                             
                dfs["table"] = self.joinedDf[columns].copy()
                #print  dfs["table"].sort_values("timeraw").tail(3)                
                
            
            """ commit the changes to db """
            self.Commit()
            
            if(complete_calc_flag):
                eventCalcReady.set()

           # if __debug__: print "P9: C: sort and copy", (time.clock() - ytime)*1000,"ms"
                        
           # if __debug__: print "Px: I: Calc: COMPLETE", (time.clock() - ztime)*1000,"ms"
            #print 'process id:', os.getpid()
            sys.stdout.write('.')
            
            info["wdg_calc"] = info["wdg_calc"] + 1
            info["lastcalctime"] = time.clock() - ztime
            if info["lastcalctime"] > self.maxcalctime:
                self.maxcalctime = info["lastcalctime"]
                print "MAX CALC-TIME:", self.maxcalctime

            sys.stdout.flush()
            #print "CalcNow: wait", time.clock()
            ret = eventCalcNow.wait(2)
            eventCalcNow.clear()
            #print "CalcNow: clear", ret, time.clock()
            
    def LastCalcTime(self):
        return self.calctime

    def GetUserCategoryDf(self):
        # USER df
        uDf = psql.read_sql("SELECT * FROM users", self.db, index_col = "id")                 
        uDf["name"] = uDf['name'].str.upper() +' '+uDf['first_name']        
        
        # CATEGORY df
        cDf = psql.read_sql("SELECT id, name, start_nr FROM categories", self.db, index_col = "id")
        cDf.columns = ['category', "start_nr"]                                  
        #uDf =  pd.merge(uDf,  cDf, left_on='category_id', right_on='index', how="left")       
        uDf =  uDf.merge(cDf, left_on='category_id', right_index = True, how="left")                
        
                       
        uDf = uDf[["nr", "status", "name", "category", "start_nr", "year", "club", "sex", "o1", "o2", "o3", "o4"]]
        
        #adding row for nr 0
        #uDf.loc[0] = [0, None, "UNKNOWN unknown", "not def", 1, None, None, None, None, None, None, None]        
        return uDf
                    
    """ GetJoinedDf
    """
    def GetJoinedDf(self):
            
        # DB df 
        #[u'state', u'id', u'run_id', u'user_id', u'cell', u'time_raw', u'time1', u'lap1', u'time2', u'lap2', u'time3', u'lap3', u'un1', u'un2', u'un3', u'us1']            
        self.joinedDf = psql.read_sql("SELECT * FROM times", self.db)
                          
        #set index = id
        self.joinedDf.set_index('id',  drop = False, inplace = True)
        
        #replace nan with None            
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
        #print "1111", self.joinedDf.loc[2237]                    

        #print  "left",  pd.merge(self.joinedDf, self.ucDf, left_on='user_id', right_index=True, how="left")
        #print  "right",  pd.merge(self.joinedDf, self.ucDf, left_on='user_id', right_index=True, how="right")
        self.joinedDf =  pd.merge(self.joinedDf, self.ucDf, left_on='user_id', right_index=True, how="left")
        #print "HUUU", self.joinedDf[["user_id", "nr", "name"]].head(2)
        
        self.joinedDf.sort_values(by="time_raw", inplace=True)
        
        #self.joinedDf["nr"].fillna(0, inplace = True)                     
        
        #replace nan with None        
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)        
                       
        return self.joinedDf
        
    def time2tableTime(self, row, i, including_hours):
        """
        convert time from db format to table forma
        e.g. 445 -> "00:00:04:45" 
        """
        #print row
        timeX = 'time'+str(i+1)
        if row[timeX] == None:
            return None 
        #elif(type(row[timeX]) == str):
        #    return row[timeX]
        elif(row["us1"] == "DNF"):
            timeX = "DNF"
        else:                  
            timeX = TimesUtils.TimesUtils.time2timestring(row[timeX], including_hours = including_hours)
        return timeX    
        
    def df2tableDf(self, df):
        
        '''NAME'''                       
        #tabTime['name'] = joinUser['name'].upper() +' '+joinUser['first_name']        
                                                                                    
        '''TIMERAW'''
        df['timeraw'] = df['time_raw'].apply(lambda row: TimesUtils.TimesUtils.time2timestring(row, including_days = True))                                                                                                                                        
        
        additional_info = self.dstore.Get("additional_info")        
        
        '''TIME 1-3'''
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            
            #TIME 1-3
            if additional_info['time'][i]:                                
                timeX = 'time'+str(i+1)
                if(df[timeX].empty == False):                                                                        
                    minute_timeformat = self.dstore.GetItem("additional_info", ["time", i, "minute_timeformat"])
                    #df_dnf = df.us1.str.match("DNF")                                       
                    #df[~df_dnf][timeX] = df[~df_dnf].apply(lambda row: self.time2tableTime(row, i, including_hours = not(minute_timeformat)), axis = 1)                                                                 
                    df[timeX] = df.apply(lambda row: self.time2tableTime(row, i, including_hours = not(minute_timeformat)), axis = 1)
                    #df[timeX] = df[timeX].apply(lambda row: TimesUtils.TimesUtils.time2timestring(row, including_hours = not(minute_timeformat)))                                                                 
            else: 
                df[timeX] = None            
                                                                                                                                                         
        return df                                     


    def GetTimesDfs(self):
        """
        contain times in which the time in UpdateTimes() will be updated        
        updated self.timesDfs[]
        
        inputs:
            - self.joinedDf¨
            - dstore.GetItem("additional_info", [ "time", i])['filter']
        """

        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            
            timeX = "time"+str(i+1)                
                         
            time_group = self.dstore.GetItem('additional_info', ['time', i])
            if(time_group['checked'] != 0):            
                
                #prepare filtered df for times                                                
                filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "time", i])['filter'])                
                tempDf = df_utils.Filter(self.joinedDf, filter_dict)
                tempDf = tempDf[(tempDf[timeX].isnull()) & (tempDf['user_id']!=0) ] #filter times with timeX or with no number                                         
                self.timesDfs[i] = tempDf

        return #self.timesDfs
                
                            
    """ update LAP df """
    def GetLapsDfs(self):
        """
        contain times in which the lap in UpdateLaps() will be updated        
        updated self.lapsDfs[i]
        
        inputs:
            - self.joinedDf
            - dstore.GetItem("additional_info", [ "time", i])['filter']
        """                             
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
                                    
            timeX = "time"+str(i+1)                
            lapX = "lap"+str(i+1)
                                                                                                                        
                 
            #prepare filtered df for lap
            lap_group = self.dstore.GetItem('additional_info', ['lap', i])                    
            if(lap_group['checked'] != 0):
                filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "time", i])['filter'])
                tempDf = df_utils.Filter(self.joinedDf, filter_dict)  
                filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "lap", i])['filter'])                        
                tempDf = df_utils.Filter(tempDf, filter_dict)
                lapDf =  tempDf[(tempDf[timeX].notnull()) & (tempDf[lapX].isnull()) & (tempDf['user_id']!=0) ] #filter times with timeX or with no number                                                                
            
                self.lapsDfs[i] = lapDf            
        return #self.lapsDfs
                        

    def GetOrderDfs(self):        
        """
        contain times in which the order in UpdateOrder() will be updated
        updated self.self.orderDfs[] -> {"total": df, "category": groubpy}
        
        inputs:
            - self.joinedDf¨
            - self.dstore.GetItem('additional_info', ['order', i])
        """                        
        for i in range(0, NUMBER_OF.THREECOLUMNS):            
              
            #get order group
            group = self.dstore.GetItem('additional_info', ['order', i])          
            if (group['checked'] == 0):
                continue
                                                  
            column1 = group['column1'].lower()  
            column2 = group['column2'].lower()
            asc1 = 1 if(group['order1'].lower() == "asc") else 0
            asc2 = 1 if(group['order2'].lower() == "asc") else 0
            
            #filter only times with (not null sort column1) AND number(user_id)            
            if not(column1 in self.joinedDf):
                continue
            aux_df = self.joinedDf[(self.joinedDf[column1].notnull()) & (self.joinedDf['user_id']!=0)]
                
            
            '''FILTER by row'''
            #1. sort Best times, Last times                            
            if group['row'] == u'Best times1':                      
                aux_df = aux_df.sort("time1", ascending = False )
            elif group['row'] == u'Best times2':                      
                aux_df = aux_df.sort("time2", ascending = False ) 
            elif group['row'] == u'Best times3':                      
                aux_df = aux_df.sort("time3", ascending = False )   
            elif group['row'] == u'Best times4':                           
                aux_df = aux_df.sort("time4", ascending = False )   
            elif group['row'] == u'Last times':                                 
                aux_df = aux_df.sort_values(by="time_raw")
            else:
                print "ERROR: no row specified!!!", group        
                            
            #2. take only last from each user                                                             
            aux_df = aux_df.groupby("user_id", as_index = False).last()
            aux_df = aux_df.where(pd.notnull(aux_df), None)                                        
            aux_df.set_index('id',  drop=False, inplace = True)                
            
            '''SORT by columns'''
            if(column2 in aux_df.columns):
                #print "nested sorting", column1, column2, asc1, asc2                
                try:                
                    aux_df = aux_df.sort_values(by=[column1, column2], ascending = [asc1, asc2])
                except IndexError:
                    aux_df = aux_df.sort_values(by=column1, ascending = asc1)
            else:                    
                aux_df = aux_df.sort_values(by=column1, ascending = asc1)            
            
            #category order            
            if(group['type'] == "Total"):
                self.orderDfs[i]['total'] = aux_df                    
            elif(group['type'] == "Category"):                                                
                self.orderDfs[i]['category'] = aux_df.groupby("category", as_index = False)                            
            elif(group['type'] == "Group#1"):
                print "ERROR: Group order NOT implemented"
            elif(group['type'] == "Group#2"):
                print "ERROR: Group order NOT implemented"
            elif(group['type'] == "Group#3"):
                print group
                print "ERROR: Group order NOT implemented"
            else:
                print "FATAL ERROR",group['type']
                       
        return #self.orderDfs           

    def UpdateTimes(self, timesDfs):
        """
        Calc and update times in DB
        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()
        
        inputs: self.timesDfs[i]
        output: call CalcAndUpdateTime[]
        ret: True: something updated  
        """
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            if self.timesDfs[i].empty:
                continue
            timesDfs[i].apply(lambda row: self.CalcAndUpdateTime(row, i), axis = 1)

        return True
    
    def UpdateLaps(self, lapsDfs):
        """
        Calc and update laps in DB

        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()
        u kol kde 'lapX'=None, dopočítá lap pomocí funkce calcLap()
        
        Ret: True: something updated   
        """
        ret = False     
                                
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
                if self.lapsDfs[i].empty:
                    continue                                  
                self.lapsDfs[i].apply(lambda row: self.CalcAndUpdateLap(row, i), axis = 1)                
                ret = True
        return ret
      
    def UpdateOrder(self):
        """        
        Calc and update order in DB        
        """
        

        
        
        
        if self.joinedDf.empty == False:
            for i in range(0, NUMBER_OF.THREECOLUMNS):
                #calc time                
                group = self.dstore.GetItem('additional_info', ["order", i])
                if(group["checked"] == 0):                    
                    self.joinedDf["order"+str(i+1)] = None
                    continue 
        
                if self.orderDfs[i] == None:
                    continue
                self.joinedDf["order"+str(i+1)] = self.joinedDf.apply(lambda row: self.CalcOrder(row, i), axis = 1)
                self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)        
        return #self.joinedDf
    
    def UpdatePoints(self, joinedDf):
        """
        Calc and update points in DB                 
        """
        if self.joinedDf.empty == False:
            for i in range(0, NUMBER_OF.POINTSCOLUMNS):
                group = self.dstore.GetItem('additional_info', ['points', i])          
                pointsX = "points"+str(i+1)                                  
                if (group['checked'] == 0):
                    self.joinedDf[pointsX] = None
                else:                                        
                    self.joinedDf[pointsX] = self.joinedDf.apply(lambda row: self.CalcPoints(row, i), axis = 1)
                    self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)                
        return #self.joinedDf
    
    def IsTimeToCalc(self, dbTime):        
        
        #remote mode => no calc values      
        if self.dstore.GetItem("racesettings-app", ['remote']) != 0:            
            return False                                                        

        #no user, no calc
        if(dbTime['user_id'] == 0):
            return False   
        
        if dbTime['time_raw'] == None:
            return False         
            
        return True
    
    def CalcTime(self, dbTime, index):
        return self.Calc(dbTime, index, 'time')

    def CalcAndUpdateTime(self, dbTime, index):        
        time = self.CalcTime(dbTime, index)                                                                                                                                                                              
        if time != None:                                                                                             
            db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], "time"+str(index+1):time}, commit_flag = False)
            self.CommitRequest()                                                                                                           
            return time
        return time
    
    def CalcPoints(self, tabTime, index):        
        points = self.Calc(tabTime, index, 'points')
        return points
    
    def CalcAndUpdatePoints(self, tabTime, index):
        points = self.CalcPoints(tabTime, index)
        if points != None:                                                                                 
            db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], lapX:lap}, commit_flag = False)
            return True
        return False

    def Calc(self, tabTime, index, key):
        '''
        společná funkce pro počítání time, points
        '''
                                    
        '''no time in some cases'''     
        if(self.IsTimeToCalc(tabTime) == False):   
            return None               
                  
        #calc time        
        group = self.dstore.GetItem('additional_info', [key, index])
        
        if(group["checked"] == 0):
            return None
        
        if(self.joinedDf.empty):
            return None
        
        #get join time, loc is faster than old solution                                                                             
        joinTime = self.joinedDf.loc[tabTime['id']]                

        #evalute rule
        #print "EVALUATING a", group                                       
                          
        ret_time = self.Evaluate(self.joinedDf, group, joinTime, tabTime)
         
        return ret_time
    
    def CalcLap(self, dbTime, index):
        '''
        pokud není čas spočítá čas,
        pokud je čas a není lap spočítá lap            
        '''                                                    
                     
#         '''no time in some cases'''
#         if(self.IsTimeToCalc(dbTime) == False):
#             return None                    
                
        timeX = "time"+str(index+1)
        lapX = "lap"+str(index+1)
        lap = None
            
        #calc lap           
        if(dbTime[timeX] != None) and (dbTime[lapX] == None):            
            
            
            # Filter #1: only better times                                                         
            aux_df = self.joinedDf[self.joinedDf["time_raw"] < dbTime["time_raw"]]  #aux_df = aux_df[aux_df[timeX] < dbTime[timeX]]                        
            
            # Filter #2: only after starttime
            fromlaststart = self.dstore.GetItem("additional_info", ["lap", index, "fromlaststart"])
            if(fromlaststart):            
                starttime = self.GetStarttime(dbTime, aux_df)                
                if(starttime == None):
                    return None                                    
                aux_df = aux_df[aux_df["time_raw"] > starttime["time_raw"]]
                                            
            # Filter #3: only times from the same user            
            aux_df = aux_df[aux_df['user_id'] == dbTime['user_id']]
        
            lap = len(aux_df[aux_df[timeX].notnull()])
                        
            if (lap != None):
                lap = lap + 1                
           
        return lap
    
    def CalcAndUpdateLap(self, dbTime, index):        
        lap = self.CalcLap(dbTime, index)                                                                                                                                                                              
        if lap != None:                                                                                             
            db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], "lap"+str(index+1):lap}, commit_flag = False)            
            self.CommitRequest()
            return True
        return False
    
    def CalcOrder(self, dbTime, index):
        '''
        pokud není čas spočítá čas,
        pokud je čas a není lap spočítá lap                           
        '''        
        df = self.orderDfs[index]
                         
        #'''no order in some cases'''
        #if(self.IsTimeToCalc(dbTime) == False):            
        #    return None          
        
        
        #get order group
        #group = dstore.GetItem('additional_info', ['order', index])                 
        #column1 = group['column1'].lower()                           
        
        #column is empty => no order
        #if(dbTime[column1] == None):            
        #    return None
        
        #get order group
        group = self.dstore.GetItem('additional_info', ['order', index])          
        if (group['checked'] == 0):
            return None
        
        aux_df = pd.DataFrame()
        #take order df
        group = self.dstore.GetItem('additional_info', ['order', index])
        
        if(group['type'] == "Total"):
            aux_df = df['total']
        elif(group['type'] == "Category"):
            aux_groupby = df['category']
            if(dbTime["category"] != None):
                if (aux_groupby) and (aux_groupby.groups !={}): 
                    try:
                    #print dbTime, type(dbTime)  
                    #print aux_groupby.groups
                        aux_df = aux_groupby.get_group(dbTime["category"])
                    except KeyError: 
                        return None
                else:
                    return None
            else:
                return None
        elif(group['type'] == "Group#1"):                
            print "ERROR: Group1 order NOT implemented", index, self.dstore.Get('additional_info')
        elif(group['type'] == "Group#2"):
            print "ERROR: Group2 order NOT implemented"                
        elif(group['type'] == "Group#3"):
            print "ERROR: Group3 order NOT implemented"
        else:
            print "FATAL ERROR1", group['type']                
       
        order = None
        if (aux_df.empty == False) and (dbTime['id'] in aux_df.id.values):
            # count only better times, df already sorted        
            aux_df = aux_df.loc[:dbTime['id']]
            order = len(aux_df)
        return order  
    
    def GetPrevious(self, dbTime, filter = None, df = None, nr = -1):        
        
        if(dbTime['user_id'] == 0) or (dbTime['user_id'] == None):                                    
            return None
        
        # user and previoustime filter                
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw < dbTime['time_raw'])]                     
        
        #filter        
        df =  df_utils.Filter(df, filter)                                       
        
        #group        
        try:            
            #time = df[df.time_raw < dbTime['time_raw']].iloc[nr]                
            time = df.iloc[nr]
            time = dict(time)                        
        except:                                    
            time = None                    
                                   
        return time
    
    def GetNext(self, dbTime, filter = None, df = None, nr = -1):        
        
        if(dbTime['user_id'] == 0) or (dbTime['user_id'] == None):                                    
            return None
        
        # user and previoustime filter                
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw > dbTime['time_raw'])]                     
        
        #filter        
        df =  df_utils.Filter(df, filter)                                       
        
        #group                
        try:            
            #time = df[df.time_raw < dbTime['time_raw']].iloc[nr]                
            time = df.iloc[nr]
            time = dict(time)                        
        except:                                    
            time = None                    
                                   
        return time
    
    
    
    
    def GetStarttime(self, time, df = None):        
        starttime = None                
        
        if(self.dstore.GetItem("racesettings-app", ["evaluation", "starttime"]) == StarttimeEvaluation.VIA_CATEGORY):
            #VIA CATEGORY => Xth starttime                                                                                                                            
            starttime = df_utils.Get(df, time["start_nr"] , filter = {'cell':1})                                                                                                            
        elif(self.dstore.GetItem("racesettings-app", ["evaluation", "starttime"])  == StarttimeEvaluation.VIA_USER):
            #VIA USER => previous startime from the same user                                                
            starttime = self.GetPrevious(time, filter = {'cell':1}, df = df)        
        return starttime 
    
    def GetStarttime_old(self, dbTime, df = None):
        filter = {'cell':1}
        starttime = None
                
        
        if(self.dstore.GetItem("racesettings-app", ["evaluation", "starttime"])  == StarttimeEvaluation.VIA_CATEGORY):
            #VIA CATEGORY => Xth starttime    
            dbUser =   self.tableUsers.getDbUserParIdOrTagId(dbTime["user_id"], self.db)          
            if(dbUser == None):
                return None                                                                                                             
            start_nr = self.tableCategories.getTabRow(dbUser['category_id'], self.db)['start_nr'] #get category starttime                
            starttime = df_utils.Get(df, start_nr, filter = {'cell':1})                                                                                                            
        elif(self.dstore.GetItem("racesettings-app", ["evaluation", "starttime"])  == StarttimeEvaluation.VIA_USER):
            #VIA USER => previous startime from the same user                                                
            starttime = self.GetPrevious(dbTime, filter = {'cell':1}, df = df)

            
        return starttime    
    
    
    
     
    """
    joinTime - z df, db i tab data(older) i user data
    tabTime - aktualizovaná data z tabulky, points, order atd.
    """
    def Evaluate(self, df, rule, joinTime, tabTime):
        points = None
                
        minimum =  rule['minimum'] if ('minimum' in rule) else None
        maximum = rule['maximum'] if ('maximum' in rule) else None
        
        #rule
        rule = rule['rule']
        rule = rule.lower()
                
        
        #check if data exist
        #nelze rusi mi celltime2
#         if ("time1" in rule) and (joinTime['time1'] == None):    
#             return None
#         if ("time2" in rule) and (joinTime['time2'] == None):        
#             return None
#         if ("time3" in rule) and (joinTime['time3'] == None):        
#             return None        
        
        '''REPLACE keywords'''
        
        # TIME CONSTANT: %00:00:01,66% => number(166)
        aux_split = rule.split('%')
        if(len(aux_split) == 3): # 3 parts => ruletime exist, on 2.position                
            try:
                ruletime = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
            except TimesUtils.TimeFormat_Error:            
                return None                                    
            rule = aux_split[0] + str(ruletime) + aux_split[2] #glue expression again
            
        if(len(aux_split) == 5): # 5 parts => ruletime exist, on 2.position and 4.position                
            try:
                ruletime1 = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
                ruletime2 = TimesUtils.TimesUtils.timestring2time(aux_split[3], including_days = False) #timestring=>time                        
            except TimesUtils.TimeFormat_Error:            
                return None                                    
            rule = aux_split[0] + str(ruletime1) + aux_split[2] + str(ruletime2) + aux_split[4]
            
        if(len(aux_split) == 7): # 5 parts                
            try:
                ruletime1 = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
                ruletime2 = TimesUtils.TimesUtils.timestring2time(aux_split[3], including_days = False) #timestring=>time                        
                ruletime3 = TimesUtils.TimesUtils.timestring2time(aux_split[5], including_days = False) #timestring=>time                        
            except TimesUtils.TimeFormat_Error:            
                return None                                    
            rule = aux_split[0] + str(ruletime1) + aux_split[2] + str(ruletime2) + aux_split[4] + str(ruletime3) + aux_split[6]
    
        
        if(len(aux_split) == 9): # 9 parts                
            try:
                ruletime1 = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
                ruletime2 = TimesUtils.TimesUtils.timestring2time(aux_split[3], including_days = False) #timestring=>time                        
                ruletime3 = TimesUtils.TimesUtils.timestring2time(aux_split[5], including_days = False) #timestring=>time                        
                ruletime4 = TimesUtils.TimesUtils.timestring2time(aux_split[7], including_days = False) #timestring=>time                        
            except TimesUtils.TimeFormat_Error:
                return None                                    
            rule = aux_split[0] + str(ruletime1) + aux_split[2] + str(ruletime2) + aux_split[4] + str(ruletime3) + aux_split[6] + str(ruletime4) + aux_split[8]
    
        
        expression_string = rule
        #print "es", expression_string
         
        #UN1-UN3
        try:
            if ("un1" in rule):
                expression_string = expression_string.replace("un1", str(joinTime['un1']))
            if ("un2" in rule):                                
                expression_string = expression_string.replace("un2", str(joinTime['un2']))
            if ("un3" in rule):                                
                expression_string = expression_string.replace("un3", str(joinTime['un3']))
        except KeyError:        
            return None
        
        # ORDER1-ORDER3
        if "order" in rule:        
            try:
                if ("order1" in rule):                                
                    expression_string = expression_string.replace("order1", str(joinTime['order1']))
                if ("order2" in rule):                                
                    expression_string = expression_string.replace("order2", str(joinTime['order2']))
                if ("order3" in rule):                                
                    expression_string = expression_string.replace("order3", str(joinTime['order3']))
            except KeyError:        
                return None
        #end of ORDER
        
        # POINTS1-POINTS3        
        if "points" in rule:       
            try:
                if ("points1" in rule):
                    #print rule, joinTime                                
                    expression_string = expression_string.replace("points1", str(tabTime['points1']))
                if ("points2" in rule):                                
                    expression_string = expression_string.replace("points2", str(tabTime['points2']))
                if ("points3" in rule):                                
                    expression_string = expression_string.replace("points3", str(tabTime['points3']))
                if ("points4" in rule):                                
                    expression_string = expression_string.replace("points4", str(tabTime['points4']))
                if ("points5" in rule):                                
                    expression_string = expression_string.replace("points5", str(tabTime['points5']))
            except KeyError:        
                return None
        #end of points
               
        # CELLTIME2 - CELLTIME250                
        if "celltime" in rule:
            for i in range(0,25):                
                
                #expression_string = es
                i = 25-i
                
                #replace index for finishtime
                if i == 25:
                    i = 250
                
                celltimeX = "celltime" + str(i)                
                if (celltimeX in rule):                    
                    try:                    
                        celltime = self.GetPrevious(joinTime, {"cell":str(i)}, df)
                        expression_string = expression_string.replace(celltimeX, str(celltime['time_raw']))                 
                    except TypeError:       
                        print "type error celltime: ", rule, "time id:", joinTime["id"]         
                        return None

        #PREV
        if "prev" in rule:
            # prevYtimeX
            for prev_i in range(1, 11):
                for i in range(1, NUMBER_OF.TIMESCOLUMNS + 1):                   
                    previoustimeX = "prev"+str(prev_i)+"time" + str(i)
                    if previoustimeX in rule:
                        try:  
                            time = self.GetPrevious(joinTime, {}, df, prev_i * -1)                        
                            if(time == None):
                                return None                     
                            expression_string = expression_string.replace(previoustimeX, str(time['time'+str(i)]))                           
                        except TypeError:       
                            print "type error", previoustimeX         
                            return None                    
        
            # previoustime                
            if ("prevtime" in rule) or ("prev1time" in rule):                              
                try:  
                    time = self.GetPrevious(joinTime, {}, df)
                    if(time == None):
                        return None                
                    expression_string = expression_string.replace("prev1time", str(time['time_raw']))                           
                    expression_string = expression_string.replace("prevtime", str(time['time_raw']))
                except TypeError:       
                    print "type error previoustime"         
                    return None
                    # prevI-timeX
                    
            # previous2time                        
            if ("prev2time" in rule):                              
                try:  
                    time = self.GetPrevious(joinTime, {}, df, -2)
                    if(time == None):
                        return None                                
                    expression_string = expression_string.replace("prev2time", str(time['time_raw']))                           
                except TypeError:       
                    print "type error previoustime"         
                    return None                
            # previous3time                        
            if ("prev3time" in rule):                              
                try:  
                    time = self.GetPrevious(joinTime, {}, df, -3)
                    if(time == None):
                        return None                                
                    expression_string = expression_string.replace("prev3time", str(time['time_raw']))                           
                except TypeError:       
                    print "type error previoustime"         
                    return None
        #end of PREV
        
        #NEXT
        '''
        zakomentovano, 
        kvuli formulim se pri zmene cisla mazou jen budouci casy
        if "next" in rule:                       
            # nextYtimeX        
            for next_i in range(1, 5):
                for i in range(1, NUMBER_OF.TIMESCOLUMNS + 1):                   
                    nexttimeX = "next"+str(prev_i)+"time" + str(i)
                    if nexttimeX in rule:                                        
                        try:  
                            time = self.Next(joinTime, {}, df, next_i * -1)                        
                            if(time == None):
                                return None                     
                            expression_string = expression_string.replace(nexttimeX, str(time['time'+str(i)]))                           
                        except TypeError:       
                            print "type error", nexttimeX         
                            return None 
            # nexttime                
            if ("nexttime" in rule) or ("next1time" in rule):                              
                try:                
                    time = self.GetNext(joinTime, {}, df, 0)                
                    if(time == None):                                                                            
                        return None                                    
                    expression_string = expression_string.replace("nexttime", str(time['time_raw']))                                       
                except TypeError:       
                    print "type error nexttime"         
                    return None
            # next2time                
            if ("next2time" in rule):                              
                try:                  
                    time = self.GetNext(joinTime, {}, df, 1)                
                    if(time == None):                                                                            
                        return None                                    
                    expression_string = expression_string.replace("next2time", str(time['time_raw']))                                       
                except TypeError:       
                    print "type error nexttime"         
                    return None
        #end of NEXT
        '''
                
        # STARTTIME    
        #user without number => no time
        if ("starttime" in rule):            
            starttime = self.GetStarttime(joinTime, df)            
                                    
            if starttime == None:
                return None
                        
            expression_string = expression_string.replace("starttime", str(starttime['time_raw']))                                                   
               
        
        # TIME1-TIME3
        if "time" in expression_string:                                                             
            expression_string = expression_string.replace("time1", str(joinTime['time1']))       
            expression_string = expression_string.replace("time2", str(joinTime['time2']))       
            expression_string = expression_string.replace("time3", str(joinTime['time3']))
            expression_string = expression_string.replace("time4", str(joinTime['time4']))
        
        # LAP1-LAP4
        if "lap" in expression_string:  
            expression_string = expression_string.replace("lap1", str(joinTime['lap1']))       
            expression_string = expression_string.replace("lap2", str(joinTime['lap2']))       
            expression_string = expression_string.replace("lap3", str(joinTime['lap3']))
            expression_string = expression_string.replace("lap4", str(joinTime['lap4']))
        
               
        # TIME
        expression_string = expression_string.replace("time", str(joinTime['time_raw']))
                
        ''' evaluate expresion '''
        #print "ES",expression_string 
        if (expression_string == "") or ("None" in expression_string):
            return None
        
        try:            
            points = eval(expression_string)        
        except (SyntaxError, TypeError, NameError):
            print "I: invalid string for evaluation", expression_string, rule            
            return None        
        
        #restrict final value               
        if minimum and (points < minimum):
            points = minimum
        if maximum and (points > maximum):
            points = maximum                     
                                
        return points
    
    
    
#     def UpdateExportDf(self, tabDf, db):
#         """
#         update dataframes for export
#         
#         0: take tabbDf as basis (because of time-format 00:00:01:16)
#            join dbDf and extend of userDf         
#         1: Filter: Last times: take last time from each user
#                    Best timesX: take best timeX from each user
#         2: Sort: basic or nested sorting
#         3: Selection: take only column you need
#         
#         return: filtred, sorted and selected dataframe for total export
#                 (for category export has to be filtred) 
#         """
#                  
#         columns =  self.joinedDf.columns - tabDf.columns  
#         joinedTabDf = tabDf.join(self.joinedDf[columns])                           
#          
#         #replace nan with None
#         self.joinedTabDf = joinedTabDf.where(pd.notnull(joinedTabDf), None)        
#         
#         #update export df
#         self.exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS        
#         for i in range(0, NUMBER_OF.EXPORTS):
#                           
#             if (tabExportSettings.IsEnabled(i) == False):
#                 continue            
#             
#             #get export group            
#             checked_info = self.dstore.GetItem('export', ["checked", i])
#             
#             #get export group
#             filtersort = self.dstore.GetItem('export_filtersort', [i])
#                                       
#             #print group
#             filter = filtersort['filter']
#             sort1 = filtersort['sort1'].lower()  
#             sort2 = filtersort['sort2'].lower()
#             sortorder1 = True if(filtersort['sortorder1'].lower() == "asc") else False
#             sortorder2 = True if(filtersort['sortorder2'].lower() == "asc") else False
#             
#             aux_df = self.joinedTabDf
#             #filter 
#             filter_split_keys = filter.split(" ")
#             filter_keys = []
#             for key in filter_split_keys:
#                 if(key in aux_df.columns):
#                     filter_keys.append(key)
#                 
#             #print filter_keys, len(filter_keys)
#             
#             if(len(filter_keys) == 1):
#                 #print "====", filter_keys
#                 aux_df =  aux_df[aux_df[filter_keys[0]] != ""]
#                 aux_df =  aux_df[aux_df[filter_keys[0]].notnull()]
#                 #print aux_df[filter_keys[0]]
#                 
#             elif(len(filter_keys) == 2):
#                 aux_df =  aux_df[(aux_df[filter_keys[0]] != "") | (aux_df[filter_keys[1]] != "")]
#                 aux_df =  aux_df[(aux_df[filter_keys[0]] != None) | (aux_df[filter_keys[1]] != None)]
#             
#             #aux_df = self.joinedDf[(aux_df[column1].notnull()) & (self.joinedDf['user_id']!=0)]
#             #last time from each user                    
#             aux_df = aux_df.sort("time_raw")                        
#             if("last" in filter):                                                                
#                 aux_df = aux_df.groupby("user_id", as_index = False).last()
#             aux_df = aux_df.where(pd.notnull(aux_df), None)                        
#             aux_df.set_index('id',  drop=False, inplace = True)
#             
#             #sort again
#             if(sort2 in aux_df.columns):
#                 #print "nested sorting", sort1, sort2, sortorder1, sortorder2
#                 #print aux_df
#                 aux_df = aux_df.sort([sort1, sort2], ascending = [sortorder1, sortorder2])
#             else:
#                 #print "basic sorting"
#                 aux_df = aux_df.sort(sort1, ascending = sortorder1)
#                         
#             #filter to checked columns
#             columns = tabExportSettings.exportgroups[i].GetCheckedColumns()            
#             
#             for oc in range(0, NUMBER_OF.EXPORTS):
#                 ordercatX = 'ordercat'+str(oc+1)
#                 orderX = 'order'+str(oc+1)                
#                 aux_df[ordercatX] = aux_df[orderX].astype(str)+"./"+aux_df.category                        
#                                                            
#             self.exportDf[i] = aux_df[columns]                            
#                            
#         return self.joinedDf             
    

manage_calc = ManageCalcProcess()
    
       
                                                                         
            
if __name__ == "__main__":    
    print "main manage_calc()"
    print "thread id", currentThread().ident
    my_calc = ManageCalc()         
    my_calc.start()
    while(1):
        pass            
