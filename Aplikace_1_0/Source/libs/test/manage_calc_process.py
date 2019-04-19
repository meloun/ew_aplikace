# -*- coding: utf-8 -*-
'''
Created on 29.05.2015

@author: Lubos Melichar
'''


import time
import pandas.io.sql as psql    
import pandas as pd
import libs.sqlite.sqlite_utils as db_utils
import libs.pandas.df_utils as df_utils
from ewitis.data.DEF_DATA import *
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from ewitis.gui.events import myevent, myevent2
import ewitis.gui.TimesUtils as TimesUtils
import os

def getDf():
    myheader = ["name", "test2", "test3"]
    random_nr = int(round(time.clock() * 13))            
    myrow1 =   [ random_nr,  random_nr+400, 250]
    myrow2 =   [ random_nr+1,  random_nr+400, 250]
    df = pd.DataFrame([myrow1]*100 + [myrow2]*100, columns = myheader)
    return df

class ProcessDstore():
    def __init__(self, data):
        self.data = data
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
        self.joinedDfFreeze = pd.DataFrame()  
        self.i = 0 
            
                        

    def mysleepstep(self):        
        return
        self.tick = self.tick + 1
        if(self.tick>50):            
            time.sleep(0.03)            
            self.tick = 0
                         
    def sRefresh(self):
        print "manage refresh"    
             
    def run(self, q, processdict):        
        print "I:P: CALC: zakladam process.."
        
        self.dstore = ProcessDstore(processdict)
        
        myevent2.set()                    
        
        """ DATABASE """                
        try:           
            self.db = db_utils.connect("db/test_db.sqlite")                        
        except:                    
            print "E: Database"
            
                
            
            
        while(1):
            #delay
            ztime = time.clock()
            
            self.timesDfs = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
            self.lapsDfs = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]    
            self.orderDfs = [{'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}]                                            
                                
            """ update DFs """
            ytime = time.clock() 
            self.ucDf = self.GetUserCategoryDf()
            #print "P: C: GetUserCategoryDf()", time.clock() - ytime,"s"
            
            
            
            """ update joined DF"""
            ytime = time.clock() 
            self.GetJoinedDf()
            #print "P: C: GetJoinedDf() 1", time.clock() - ytime,"s"             
            

            """ update times """                                            
            ytime = time.clock() 
            self.GetTimesDfs()                                                 
            self.UpdateTimes(self.timesDfs)                                                        
            self.GetJoinedDf()
            #print "P: C: UpdateTimes()", time.clock() - ytime,"s"
            #print "P: 2: ucDf", self.joinedDf             
                                                                                                                                                                                        
            #laps
            ytime = time.clock()
            self.GetLapsDfs()                                                                         
            self.UpdateLaps(self.lapsDfs)
            self.GetJoinedDf()                                                                                                                                                                                                                        
            #print "P: C: UpdateLaps()", time.clock() - ytime,"s"
                        
            #orderX 
            self.orderDfs = self.GetOrderDfs()                                                   
            ytime = time.clock()
            self.joinedDf = self.UpdateOrder()                        
            #print "P: C: UpdateOrder() 1", time.clock() - ytime,"s"                        
            
            #points                                                  
            ytime = time.clock()
            self.joinedDf = self.UpdatePoints(self.joinedDf)
            #print "P: C: UpdatePoints()", time.clock() - ytime,"s"                        
            
            #orderX 
            ytime = time.clock()
            self.GetOrderDfs()                                                                                       
            ytime = time.clock()
            self.UpdateOrder()                                    
            #print "P: C: UpdateOrder() 1", time.clock() - ytime,"s"                        
            
            #update status                                                 
            #self.joinedDf = self.GetJoinedDf()
            
            #convert times to string format
            self.joinedDf = self.df2tableDf(self.joinedDf)
            
            #sort and copy 
            ytime = time.clock()           
            if self.joinedDf.empty:
                self.joinedDfFreeze = pd.DataFrame()
                print "NIC"
            else:                              
                columns = [item[0] for item in sorted(DEF_COLUMN.TIMES['table'].items(), key = lambda (k,v): (v["index"]))]            
                self.joinedDfFreeze = self.joinedDf[columns].copy()                            
            #print "P: C: sort and copy", time.clock() - ytime,"s"                                 
            
            #print(".",end='')
            #print "P: I: Calc: COMPLETE", time.clock() - ztime,"s"
            #print "==============================================="
            #print 'process id:', os.getpid()
            
            self.joinedDfFreeze["name"].iloc[0] = self.i
            self.i =  self.i +1
            self.joinedDfFreeze = getDf()
            time.sleep(0.1)
            
            
                        
            q.put(self.joinedDfFreeze)
            print "P: name: ",self.joinedDfFreeze["name"].iloc[0], q.empty()
            sys.stdout.flush()
            #print "P: df", self.joinedDfFreeze              
            
#             sys.stdout.write('.')
#             self.calctime = time.clock() - ztime
#             if self.calctime > self.maxcalctime:
#                 self.maxcalctime = self.calctime
#                 print "MAX CALC-TIME:", self.maxcalctime
#                             
            time.sleep(2)
            #myevent.wait(2)
            #myevent.clear() 
            #myevent2.wait()   
            
    def LastCalcTime(self):
        return self.calctime

    def GetUserCategoryDf(self):
        # USER df
        uDf = psql.read_sql("SELECT * FROM users", self.db, index_col = "id")                 
        uDf["name"] = uDf['name'].str.upper() +' '+uDf['first_name']      
        
        # CATEGORY df
        cDf = psql.read_sql("SELECT id, name, start_nr FROM categories", self.db)
        cDf.columns = ['id', 'category', "start_nr"]                                  
        uDf =  pd.merge(uDf,  cDf, left_on='category_id', right_on='id', how="left")        
        
               
        #print "u", uDf.columns 
        uDf = uDf[["nr", "status", "name", "category", "start_nr", "year", "club", "sex", "o1", "o2", "o3", "o4"]]
        return uDf
                    
    def GetJoinedDf(self):
        run_id = 12332 #dstore.Get("current_run")
            
        # DB df 
        #[u'state', u'id', u'run_id', u'user_id', u'cell', u'time_raw', u'time1', u'lap1', u'time2', u'lap2', u'time3', u'lap3', u'un1', u'un2', u'un3', u'us1']            
        self.joinedDf = psql.read_sql(\
                                "SELECT * FROM times" +\
                                " WHERE (times.run_id = "+ str(run_id ) +")"\
                                , self.db)                  
        
        #set index = id
        self.joinedDf.set_index('id',  drop=False, inplace = True)            
        
        #replace nan with None            
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)                    

        
        if(self.dstore.GetItem("racesettings-app", ['rfid']) == 2):
            tDf = psql.read_sql("SELECT * FROM tags", self.db, index_col = "id")   
            tDf = tDf[["user_nr", "tag_id"]]
            self.joinedDf =  pd.merge(self.joinedDf,  tDf, left_on='user_id', right_on='tag_id', how="left")
            self.joinedDf =  pd.merge(self.joinedDf,  self.ucDf, left_on='user_nr', right_on='nr',  how="left")
            self.joinedDf.set_index('id',  drop=False, inplace = True) 
        else:
            self.joinedDf =  pd.merge(self.joinedDf,  self.ucDf, left_on='user_id', right_index=True, how="left")
        

        self.joinedDf.sort("time_raw", inplace=True)            
        
        #replace nan with None
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
                
        return self.joinedDf
    
    def df2tableDf(self, df):

        '''NAME'''                       
        #tabTime['name'] = joinUser['name'].upper() +' '+joinUser['first_name']        
                                                                                    
        '''TIMERAW'''
        df['timeraw'] = df['time_raw'].apply(lambda row: TimesUtils.TimesUtils.time2timestring(row, True))                                                                                                                                        
        
        additional_info = self.dstore.Get("additional_info")        
        
        '''TIME 1-3'''
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            
            #TIME 1-3
            if additional_info['time'][i]:                
                timeX = 'time'+str(i+1)
                if(df[timeX].empty == False):                                                                        
                    minute_timeformat = self.dstore.GetItem("additional_info", ["time", i, "minute_timeformat"])
                    df[timeX] = df[timeX].apply(lambda row: TimesUtils.TimesUtils.time2timestring(row, including_hours = not(minute_timeformat)))                                         
            else: 
                df[timeX] = None
                                                                                         
                                                                        
        return df                                     
        
    """ update TIMES df """
    def GetTimesDfs(self):
        
                     
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            
            timeX = "time"+str(i+1)                
                         
            time_group = self.dstore.GetItem('additional_info', ['time', i])
            if(time_group['checked'] != 0):            
                                                
                #prepare filtered df for times                                                
                filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "time", i])['filter'])
                tempDf = df_utils.Filter(self.joinedDf, filter_dict)                    
                tempDf = tempDf[(tempDf[timeX].isnull()) & (tempDf['user_id']!=0) ] #filter times with timeX or with no number                          
                                         
                self.timesDfs[i] = tempDf
        print "tDdfs 0",timesDfs[0]
        print "=================="
        print "tDdfs 1",timesDfs[1]
        print "=================="
        print "tDdfs 2",timesDfs[2]
        print "=================="
        print "=================="
        return self.timesDfs
                
                            
    """ update LAP df """
    def GetLapsDfs(self):
                             
        for i in range(0, NUMBER_OF.THREECOLUMNS):
                                    
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
        return self.lapsDfs
                        

    """ update ORDER df """
    def GetOrderDfs(self):
                    
        #orderDfs = [{'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}, {'total':pd.DataFrame(), "category":  None}]
        #self.orderGroupbys = [None] * NUMBER_OF.THREECOLUMNS
        for i in range(0, NUMBER_OF.THREECOLUMNS):            
              
            #get order group
            group = self.dstore.GetItem('additional_info', ['order', i])          
            if (group['checked'] == 0):
                continue
                                      
            #print group
            column1 = group['column1'].lower()  
            column2 = group['column2'].lower()
            asc1 = 1 if(group['order1'].lower() == "asc") else 0
            asc2 = 1 if(group['order2'].lower() == "asc") else 0
            
            #filter
            #print joinedDf.columns
            if not(column1 in self.joinedDf):
                continue
            aux_df = self.joinedDf[(self.joinedDf[column1].notnull()) & (self.joinedDf['user_id']!=0)]
                
            #FILTER only one time from each user, LAST or BEST                            
            if group['row'] == u'Best times1':                      
                aux_df = aux_df.sort("time1", ascending = False )
            elif group['row'] == u'Best times2':                      
                aux_df = aux_df.sort("time2", ascending = False ) 
            elif group['row'] == u'Best times3':                      
                aux_df = aux_df.sort("time3", ascending = False )
            elif group['row'] == u'Best times4':                        
                aux_df = aux_df.sort("time4", ascending = False )     
            elif group['row'] == u'Last times':
                #print u'Last times'                 
                aux_df = aux_df.sort("time_raw")
            else:
                print "ERROR: no row specified!!!", group        
                                                                         
            aux_df = aux_df.groupby("user_id", as_index = False).last()
            aux_df = aux_df.where(pd.notnull(aux_df), None)                                        
            aux_df.set_index('id',  drop=False, inplace = True)                
            
            #sort again
            if(column2 in aux_df.columns):
                #print "nested sorting", column1, column2, asc1, asc2                
                try:                
                    aux_df = aux_df.sort([column1, column2], ascending = [asc1, asc2])
                except IndexError:
                    aux_df = aux_df.sort(column1, ascending = asc1)
            else:                    
                aux_df = aux_df.sort(column1, ascending = asc1)            
            
            #category order            
            if(group['type'] == "Total"):
                self.orderDfs[i]['total'] = aux_df                    
            elif(group['type'] == "Category"):                    
                #self.orderGroupbys[i] = aux_df.groupby("category_id", as_index = False)                                                    
                self.orderDfs[i]['category'] = aux_df.groupby("category_id", as_index = False)                                                    
            elif(group['type'] == "Group#1"):
                print "ERROR: Group order NOT implemented"
            elif(group['type'] == "Group#2"):
                print "ERROR: Group order NOT implemented"                
            elif(group['type'] == "Group#3"):
                print group                
                print "ERROR: Group order NOT implemented"
            else:
                print "FATAL ERROR",group['type']
                
        #print "return", orderDfs[0]['total']
        return self.orderDfs
                    

                                                                                           
    def UpdateTimes(self, timesDfs):
        """
        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()        
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []                
                                       
        self.commit_flag = False
        for i in range(0, NUMBER_OF.THREECOLUMNS):                                               
            timesDfs[i].apply(lambda row: self.CalcAndUpdateTime(row, i), axis = 1)                                                                       
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        if self.commit_flag:                          
            db_utils.commit(self.db)                                                                     
                          
        return ret_ko_times
    
    def UpdateLaps(self, lapsDfs):
        """
        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()
        u kol kde 'lapX'=None, dopočítá lap pomocí funkce calcLap()
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []        
                        
        self.commit_flag = False
        for i in range(0, NUMBER_OF.THREECOLUMNS):                        
            self.lapsDfs[i].apply(lambda row: self.CalcAndUpdateLap(row, i), axis = 1)
                                                                                                    
        if self.commit_flag:
            db_utils.commit(self.db) 
            self.commit_flag = False                                        
                                                      
        return ret_ko_times
      
    def UpdateOrder(self):
        """        
        *Ret:*
            updated dataframe with all order   
        """
        if self.joinedDf.empty == False:
            for i in range(0, NUMBER_OF.THREECOLUMNS):                
                if self.orderDfs[i] == None:
                    continue                                                  
                self.joinedDf["order"+str(i+1)] = self.joinedDf.apply(lambda row: self.CalcOrder(row, i), axis = 1)
                self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
        
        return self.joinedDf
    
    def UpdatePoints(self, joinedDf):
        """        
        *Ret:*
            updated dataframe with all points   
        """
        if self.joinedDf.empty == False:
            for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
                pointsX = "points"+str(i+1)                                  
                self.joinedDf[pointsX] = self.joinedDf.apply(lambda row: self.CalcPoints(row, i), axis = 1)
                self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
        
        #print joinedDf
        return self.joinedDf
    
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
            self.commit_flag = True                                                                                                           
            return time
        return time
    
    def CalcPoints(self, tabTime, index):
        self.mysleepstep()       
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
        společná funkce pro počítání time, lap
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

        ret_dict =  {}         
        timeX = "time"+str(index+1)
        lapX = "lap"+str(index+1)
        lap = None     
        #df = self.lapsDfs[index]
            
        #calc lap           
        if(dbTime[timeX] != None) and (dbTime[lapX] == None):            
            
            #same user
            aux_df = self.joinedDf[self.joinedDf['user_id'] == dbTime['user_id']]
                        
            
            #get sarttime
            starttime = self.GetStarttime(dbTime, aux_df)
            #print "s", starttime, dbTime["time_raw"], aux_df
            if(starttime == None):
                return None
                                       
            
            
            #better times
            #aux_df = aux_df[aux_df[timeX] < dbTime[timeX]]                                             
            aux_df = aux_df[aux_df["time_raw"] < dbTime["time_raw"]]
            aux_df = aux_df[aux_df["time_raw"] > starttime["time_raw"]]
        
            lap = len(aux_df)
                        
            if (lap != None):
                lap = lap + 1                
           
        return lap
    
    def CalcAndUpdateLap(self, dbTime, index):        
        lap = self.CalcLap(dbTime, index)                                                                                                                                                                              
        if lap != None:                                                                                             
            db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], "lap"+str(index+1):lap}, commit_flag = False)
            self.commit_flag = True                                                                                                 
            return True
        return False
    
    def CalcOrder(self, dbTime, index):
        '''
        pokud není čas spočítá čas,
        pokud je čas a není lap spočítá lap                            
        '''    
        self.mysleepstep()        
        
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
            if(dbTime["category_id"] != None):                                                                                       
                if (aux_groupby) and (aux_groupby.groups !={}): 
                    try:         
                    #print dbTime, type(dbTime)  
                    #print aux_groupby.groups                                              
                        aux_df = aux_groupby.get_group(dbTime["category_id"])                                                                 
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
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw >= dbTime['time_raw'])]                     
        
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
    
    
    
    
    def GetStarttime(self, dbTime, df = None):
        filter = {'cell':1}
        starttime = None
                
        
        if(self.dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):
            #VIA CATEGORY => Xth starttime    
            dbUser =   self.tableUsers.getDbUserParIdOrTagId(dbTime["user_id"], self.db)          
            if(dbUser == None):
                return None                                                                                                             
            start_nr = self.tableCategories.getTabRow(dbUser['category_id'], self.db)['start_nr'] #get category starttime                
            starttime = df_utils.Get(df, start_nr, filter = {'cell':1})                                                                                                            
        elif(self.dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
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
        try:
            if ("order1" in rule):                                
                expression_string = expression_string.replace("order1", str(joinTime['order1']))
            if ("order2" in rule):                                
                expression_string = expression_string.replace("order2", str(joinTime['order2']))
            if ("order3" in rule):                                
                expression_string = expression_string.replace("order3", str(joinTime['order3']))
        except KeyError:        
            return None
        
        # POINTS1-POINTS3       
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
                        print "type error celltime: ", rule, joinTime         
                        return None

        # prevI-timeX
        for prev_i in range(1, 4):
            for i in range(1, NUMBER_OF.THREECOLUMNS + 1):                   
                previoustimeX = "prev"+str(prev_i)+"-time" + str(i)
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
        if ("previoustime" in rule) or ("prev-time" in rule):                              
            try:  
                time = self.GetPrevious(joinTime, {}, df)
                if(time == None):
                    return None                
                expression_string = expression_string.replace("previoustime", str(time['time_raw']))                           
            except TypeError:       
                print "type error previoustime"         
                return None
        # nexttime                
        if ("nextcas" in rule) or ("next-time" in rule):                              
            try:  
                print "nextcas"
                time = self.GetNext(joinTime, {}, df)
                if(time == None):
                    return None
                print "nahrazuji"                
                expression_string = expression_string.replace("nextcas", str(time['time_raw']))
                print "nahrazeno", expression_string                           
            except TypeError:       
                print "type error nexttime"         
                return None
                
        # STARTTIME    
        #user without number => no time
        if ("starttime" in rule):            
            starttime = self.GetStarttime(joinTime, df)            
                                    
            if starttime == None:
                return None
                        
            expression_string = rule.replace("starttime", str(starttime['time_raw']))                                                   
               
        # TIME1-TIME3                                                        
        expression_string = expression_string.replace("time1", str(joinTime['time1']))       
        expression_string = expression_string.replace("time2", str(joinTime['time2']))       
        expression_string = expression_string.replace("time3", str(joinTime['time3']))
               
        # TIME
        expression_string = expression_string.replace("time", str(joinTime['time_raw']))
                
        ''' evaluate expresion '''
        #print "ES",expression_string 
        if (expression_string == "") or ("None" in expression_string):
            return None
        
        try:            
            points = eval(expression_string)        
        except (SyntaxError, TypeError, NameError):
            #print "I: invalid string for evaluation", expression_string, rule            
            return None        
        
        #restrict final value               
        if minimum and (points < minimum):
            points = minimum
        if maximum and (points > maximum):
            points = maximum                     
                                
        return points
    
    
    
    def UpdateExportDf(self, tabDf, db):
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
                 
        columns =  self.joinedDf.columns - tabDf.columns  
        joinedTabDf = tabDf.join(self.joinedDf[columns])                           
         
        #replace nan with None
        self.joinedTabDf = joinedTabDf.where(pd.notnull(joinedTabDf), None)        
        
        #update export df
        self.exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):
                          
            if (tabExportSettings.IsEnabled(i) == False):
                continue            
            
            #get export group            
            checked_info = self.dstore.GetItem('export', ["checked", i])
            
            #get export group
            filtersort = self.dstore.GetItem('export_filtersort', [i])
                                      
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
                                   
            #print columns
            #print aux_df.columns
            self.exportDf[i] = aux_df[columns]                            

        #print str(i), self.exportDf[i]                     
        return self.joinedDf             
    

   

manage_calc_process = ManageCalcProcess()
    
       
                                                                         
            
if __name__ == "__main__":    
    print "main manage_calc()"
    print "thread id", currentThread().ident
    my_calc = ManageCalc()         
    my_calc.start()
    while(1):
        pass            
