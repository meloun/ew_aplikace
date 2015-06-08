# -*- coding: utf-8 -*-
'''
Created on 29.05.2015

@author: Lubos Melichar
'''

import threading
import time
import pandas.io.sql as psql    
import pandas as pd
import libs.sqlite.sqlite_utils as db_utils
import libs.pandas.df_utils as df_utils
from ewitis.data.DEF_DATA import *
from ewitis.gui.TimesStore import TimesStore, timesstore


class ManageCalc(threading.Thread):            
    def __init__(self, tableUsers, tableCategories, dstore):        
        self.tableUsers = tableUsers
        self.tableCategories = tableCategories
        self.dstore = dstore                
        self.joinedDfFreeze = pd.DataFrame()                                        
        threading.Thread.__init__(self)
                         
        
             
    def run(self):
        print "CALC: zakladam vlakno.."
        
        """ DATABASE """                
        try:           
            self.db = db_utils.connect("db/test_db.sqlite")                        
        except:                    
            print "E: Database"
            
            
        while(1):
            
            #delay
            ztime = time.clock()                                               
                                
            """ update DFs """
            
            #update times
            self.UpdateJoinedDf()
            self.UpdateTimeLapDf()            
            ko_nrs = self.UpdateTimes()                             
            if(ko_nrs != []):            
                print(" Update times error: Some times have no start times, ids: "+str(ko_nrs))            
                                                                                                                                                                                        
            #update laps
            self.UpdateJoinedDf()                        
            self.UpdateTimeLapDf()                         
            ko_nrs = self.UpdateLaps()                        
            if(ko_nrs != []):            
                print(" Update laps error: Some times have no start times, ids: "+str(ko_nrs))                                                                                                                                                                                    
            
            #update orderX 
            self.UpdateJoinedDf()
            self.UpdateOrderDf()               
            self.joinedDf["order1"] = 11
            self.joinedDf["order2"] = 22
            self.joinedDf["order3"] = 33                                                 
            
            #update points
            self.UpdateJoinedDf()            
            
            
            #update status
            self.UpdateJoinedDf()
            
            self.UpdateJoinedDf()                         
            self.joinedDfFreeze = self.joinedDf.copy()
            print "I: Calc: COMPLETE", time.clock() - ztime,"s"
            myevent.wait(2)
            myevent.clear()        
            
    def UpdateJoinedDf(self):
            run_id = dstore.Get("current_run")
                
            # DB df 
            #[u'state', u'id', u'run_id', u'user_id', u'cell', u'time_raw', u'time1', u'lap1', u'time2', u'lap2', u'time3', u'lap3', u'un1', u'un2', u'un3', u'us1']            
            self.dbDf = psql.read_sql(\
                                    "SELECT * FROM times" +\
                                    " WHERE (times.run_id = "+ str(run_id ) +")"\
                                    , self.db)            
            
            #set index = id
            self.dbDf.set_index('id',  drop=False, inplace = True)            
            
            #replace nan with None            
            self.dbDf = self.dbDf.where(pd.notnull(self.dbDf), None)            
            
            #update joinedDf
            ##@ columns =  self.tabDf.columns - self.dbDf.columns                                      
            ##@ self.joinedDf = self.dbDf.join(self.tabDf[columns])
            self.joinedDf = self.dbDf        
            
            # join USER df
            self.userDf = psql.read_sql("SELECT * FROM users", self.db, index_col = "id")        
            self.userDf = self.userDf[["category_id", "year", "club", "sex", "o1", "o2", "o3", "o4"]]
            self.joinedDf =  pd.merge(self.joinedDf,  self.userDf, left_on='user_id', right_index=True, how="left")
            self.joinedDf.sort("time_raw", inplace=True)            
            
            #replace nan with None
            self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)                                    
        
    """ update TIMES & LAP df """
    def UpdateTimeLapDf(self):
        
            self.timesDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS 
            self.lapDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS
            for i in range(0, NUMBER_OF.THREECOLUMNS):
                
                timeX = "time"+str(i+1)
                lapX = "lap"+str(i+1)
                             
                time_group = self.dstore.GetItem('additional_info', ['time', i])
                if(time_group['checked'] != 0):
                                                    
                    #prepare filtered df for times                                                
                    filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "time", i])['filter'])
                    tempDf = df_utils.Filter(self.joinedDf, filter_dict)                    
                    timesDf = tempDf[(tempDf[timeX].isnull()) & (tempDf['user_id']!=0) ] #filter times with timeX or with no number                          
                     
                    #prepare filtered df for lap
                    lap_group = self.dstore.GetItem('additional_info', ['lap', i])                    
                    if(lap_group['checked'] != 0):
                        filter_dict = Assigments2Dict(self.dstore.GetItem("additional_info", [ "lap", i])['filter'])                        
                        tempDf = df_utils.Filter(tempDf, filter_dict)
                        lapDf =  tempDf[(tempDf[timeX].notnull()) & (tempDf[lapX].isnull()) & (tempDf['user_id']!=0) ] #filter times with timeX or with no number                                            
                        
                self.timesDf[i] = timesDf
                self.lapDf[i] = lapDf
                        

    """ update ORDER df """
    def UpdateOrderDf(self):
                    
            self.orderDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS
            self.orderGroupbys = [None] * NUMBER_OF.THREECOLUMNS
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
                aux_df = self.joinedDf[(self.joinedDf[column1].notnull()) & (self.joinedDf['user_id']!=0)]
                    
                #FILTER only one time from each user, LAST or BEST                            
                if group['row'] == u'Best times1':
                    #print u'Best times1'                 
                    aux_df = aux_df.sort("time1", ascending = False )
                elif group['row'] == u'Best times2':
                    #print u'Best times2'                 
                    aux_df = aux_df.sort("time2", ascending = False ) 
                elif group['row'] == u'Best times3':
                    #print u'Best times3'                 
                    aux_df = aux_df.sort("time3", ascending = False )    
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
                    print "nested sorting", column1, column2, asc1, asc2                
                    aux_df = aux_df.sort([column1, column2], ascending = [asc1, asc2])
                else:                    
                    aux_df = aux_df.sort(column1, ascending = asc1)            
                
                
                #category order            
                if(group['type'] == "All"):
                    self.orderDf[i] = aux_df                    
                elif(group['type'] == "Category"):                    
                    self.orderGroupbys[i] = aux_df.groupby("category_id", as_index = False)                                                    
                elif(group['type'] == "Group#1"):                
                    print "ERROR: Group order NOT implemented"
                elif(group['type'] == "Group#2"):
                    print "ERROR: Group order NOT implemented"                
                elif(group['type'] == "Group#3"):
                    print "ERROR: Group order NOT implemented"
                else:
                    print "FATAL ERROR"
                    

                                                                                           
    def UpdateTimes(self):
        """
        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()        
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []        
                
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            timeX = "time"+str(i+1)                               
            commit_flag = False                               
                                             
            for index, dbTime in self.timesDf[i].iterrows():
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                #calc time                    
                dbTime = dbTime.to_dict()  #df to dict                                                                                                            
                time = self.CalcTime(dbTime, i)                                                                                                                                                         
                            
                #update db                
                if time != None:
                    try:             
                        commit_flag = True                                                                                                                                            
                        db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], timeX:time}, commit_flag = False) #commit na konci funkce
                    except IndexError: #potreba startime, ale nenalezen 
                        ret_ko_times.append(dbTime['id'])
            if commit_flag:                            
                db_utils.commit(self.db)                                                                     
                          
        return ret_ko_times
    
    def UpdateLaps(self):
        """
        u časů kde 'timeX'=None, dopočítá time z time_raw a startovacího časů pomocí funkce calcTime()
        u kol kde 'lapX'=None, dopočítá lap pomocí funkce calcLap()
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []        
                
        for i in range(0, NUMBER_OF.THREECOLUMNS):                        
            lapX = "lap"+str(i+1)                                          
            commit_flag = False            
                                                         
            for index, dbTime in self.lapDf[i].iterrows():
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                #calc lap                                                                                                                         
                dbTime = dbTime.to_dict()  #df to dict                                                                                                            
                lap = self.CalcLap(dbTime, i)                                                                                                                          
                            
                #update db                
                if lap != None:
                    try:             
                        commit_flag = True                                                                                                                                            
                        db_utils.update_from_dict(self.db, "times", {'id':dbTime['id'], lapX:lap}, commit_flag = False) #commit na konci funkce
                    except IndexError: #potreba startime, ale nenalezen 
                        ret_ko_times.append(dbTime['id'])
            if commit_flag:                            
                db_utils.commit(self.db)                                         
                                                      
        return ret_ko_times    
    
    
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
        #print "EVALUATING", group                                                 
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
        df = self.lapDf[index]
            
        #calc lap           
        if(dbTime[timeX] != None) and (dbTime[lapX] == None):            
            
            #same user
            aux_df = df[df['user_id'] == dbTime['user_id']]                        
            
            #better times
            aux_df = aux_df[aux_df[timeX] < dbTime[timeX]]                                 
        
            lap = len(aux_df)
                        
            if (lap != None):
                lap = lap + 1                
           
        return lap
    
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
                        print "type error celltime: ", rule         
                        return None
        # previoustime                
        if "previoustime" in rule:                              
            try:  
                time = timesstore.GetPrevious(joinTime, {}, df)
                if(time == None):
                    return None 
                expression_string = expression_string.replace("previoustime", str(time['time_raw']))                           
            except TypeError:       
                print "type error previoustime"         
                return None
                
        # STARTTIME    
        #user without number => no time
        if ("starttime" in rule):
            starttime = None          
            tabUser =   self.tableUsers.getTabUserParIdOrTagId(joinTime["user_id"], self.db)          
            if(tabUser['nr'] == 0):
                return None        
        
            if(self.dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):
                #VIA CATEGORY => Xth starttime                                                                                                                
                start_nr = self.tableCategories.getTabRow(tabUser['category_id'], self.db)['start_nr'] #get category starttime                
                starttime = df_utils.Get(df, start_nr, filter = {'cell':1})                                                                                        
            elif(self.dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
                #VIA USER => previous startime from the same user                                                
                starttime = timesstore.GetPrevious(joinTime, filter = {'cell':1}, df = df)
            else:
                print "E: Fatal Error: Starttime "
                return None
                                    
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
            print "I: invalid string for evaluation", expression_string, rule            
            return None        
        
        #restrict final value               
        if minimum and (points < minimum):
            points = minimum
        if maximum and (points > maximum):
            points = maximum                     
                                
        return points
    
from ewitis.gui.tableCategories import tabCategories
from ewitis.gui.tableUsers import tabUsers
from ewitis.data.dstore import dstore   
myevent =  threading.Event()
manage_calc = ManageCalc(tabUsers.tables[0], tabCategories.tables[0], dstore)
    
       
                                                                         
            
if __name__ == "__main__":    
    print "main manage_calc()"
    print "thread id", currentThread().ident
    my_calc = ManageCalc()         
    my_calc.start()
    while(1):
        pass            
