# -*- coding: utf-8 -*-
from ewitis.data.db import db
import pandas.io.sql as psql    
import pandas as pd
from ewitis.data.DEF_DATA import *
from ewitis.data.dstore import dstore
import libs.timeutils.timeutils as timeutils
import ewitis.gui.TimesUtils as TimesUtils

#nešlo by to bez?
from ewitis.gui.tableUsers import tableUsers
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tabExportSettings import tabExportSettings


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
        self.joinedDf = pd.DataFrame()                                          
              
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
                    
                    if(k == "cell") and (v == "2"):
                        v="2$"                
                    v = v.replace("2|", "2$|") #cell=2|250
                    v = v.replace(" ", "") #mezery pryc
                    
                    # filter frame
                    df = df[df[k].notnull()]                                                                                                                                                                                                                                                                  
                    df = df[df[k].astype(int).astype(str).str.match(str(v))] #convert to int because of float type (3.0)
                           
                except (KeyError):
                    print "error: race settings: filter", k, v, filter
                    continue
        return df

    
    def GetPrevious(self, dbTime, filter = None, df = None):        
        
        if(dbTime['user_id'] == 0) or (dbTime['user_id'] == None):            
            return None
        
        # user and previous filter
        df = df[(df.user_id==dbTime['user_id'])  & (df.time_raw < dbTime['time_raw'])]             
        
        #filter        
        df =  self.FilterFrame(df, filter)                                       
        
        #group        
        try:            
            time = df[df.time_raw < dbTime['time_raw']].iloc[-1]                
            time = dict(time)                        
        except:                        
            time = None                    
                                   
        return time 
        
    '''
    
    '''
    def Get(self, df, nr, filter = None):
        time = {}
        
        #filter
        df = self.FilterFrame(df, filter)                      
               
        try:    
            time = df.iloc[nr-1]
        except IndexError:
            time = None
            
                    
        return time
    
    def GetFirst(self, filter = None):                    
        
        return self.Get(1, filter)        
                
    def Update(self, run_id, tabDf):
        '''
        najde všechny časy a uloží
        '''
        
        #table df
        #print "tabDf", tabDf
        self.tabDf = tabDf        
                
        #db df
        self.dbDf = psql.read_sql(\
                                "SELECT * FROM times" +\
                                " WHERE (times.run_id = "+ str(run_id ) +")"\
                                , db.getDb())
        self.dbDf.set_index('id',  drop=False, inplace = True)
        
        #replace nan with None
        self.dbDf = self.dbDf.where(pd.notnull(self.dbDf), None)
                        
        #update joinedDf
        columns =  self.tabDf.columns - self.dbDf.columns                              
        self.joinedDf = self.dbDf.join(self.tabDf[columns])        
        
        #user update
        self.userDf = psql.read_sql("SELECT * FROM users", db.getDb(), index_col = "id")        
        self.userDf = self.userDf[["year", "club", "sex", "o1", "o2", "o3", "o4"]]
        self.joinedDf =  pd.merge(self.joinedDf,  self.userDf, left_on='user_id', right_index=True, how="inner")
        self.joinedDf.sort("time_raw", inplace=True)                    
        
        #replace nan with None
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
        
        #update order df        
        self.orderDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS
        self.orderGroupbys = [None] * NUMBER_OF.THREECOLUMNS
        for i in range(0, NUMBER_OF.THREECOLUMNS):            
              
            #get order group
            group = dstore.GetItem('additional_info', ['order', i])
            
            if (group['checked'] == 0):
                continue
                                      
            #print group
            column1 = group['column1'].lower()  
            column2 = group['column2'].lower()
            asc1 = 1 if(group['order1'].lower() == "asc") else 0
            asc2 = 1 if(group['order2'].lower() == "asc") else 0
            
            #filter
            aux_df = self.joinedDf[(self.joinedDf[column1].notnull()) & (self.joinedDf['user_id']!=0)]
            #print "po", aux_df

            #sort
#             if(column2 in aux_df.columns):
#                 print "nested sorting", column1, column2, asc1, asc2
#                 aux_df = aux_df.sort([column1, column2], ascending = [asc1, asc2])
#             else:
#                 print "basic sorting"
#                 aux_df = aux_df.sort(column1, ascending = asc1)

            
            #last time from each user                    
            aux_df = aux_df.sort("time_raw")       
            #print "aa1", aux_df                                             
            aux_df = aux_df.groupby("user_id", as_index = False).last()
            aux_df = aux_df.where(pd.notnull(aux_df), None)
            #print "aa2", aux_df.columns                        
            aux_df.set_index('id',  drop=False, inplace = True)
            #print "aa3", aux_df
            
            #sort again
            if(column2 in aux_df.columns):
                print "nested sorting", column1, column2, asc1, asc2
                #print aux_df
                aux_df = aux_df.sort([column1, column2], ascending = [asc1, asc2])
            else:
                #print "basic sorting"
                aux_df = aux_df.sort(column1, ascending = asc1)            
            
            self.orderDf[i] = aux_df
            
            #category order            
            if(group['type'] == "All"):
                pass
            elif(group['type'] == "Category"):
                self.orderGroupbys[i] = aux_df.groupby("category", as_index = False)
                #print "groupsA:", i, self.orderGroupbys[i].groups                                
            elif(group['type'] == "Group#1"):                
                print "ERROR: Group order NOT implemented"
            elif(group['type'] == "Group#2"):
                print "ERROR: Group order NOT implemented"                
            elif(group['type'] == "Group#3"):
                print "ERROR: Group order NOT implemented"
            else:
                print "FATAL ERROR"            
                
            
            #print "odf",i, aux_df.dtypes
            #print "odf",i, aux_df[["id","order1", "points2"]]
            
        #update times df and lap df
        self.timesDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS 
        self.lapDf = [pd.DataFrame()] * NUMBER_OF.THREECOLUMNS
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            
            '''calc times'''
            time_group = dstore.GetItem('additional_info', ['time', i])
            if(time_group['checked'] != 0):
                                               
                #prepare filtered df for times                            
                filter_dict = Assigments2Dict(dstore.GetItem("additional_info", [ "time", i])['filter'])
                self.timesDf[i] = timesstore.FilterFrame(self.joinedDf, filter_dict)
                #print "KL", i, filter_dict, len(self.timesDf[i])
 
                
                #prepare filtered df for lap
                lap_group = dstore.GetItem('additional_info', ['lap', i])
                #print lap_group
                if(lap_group['checked'] != 0):
                    filter_dict = Assigments2Dict(dstore.GetItem("additional_info", [ "lap", i])['filter'])
                    self.lapDf[i] = timesstore.FilterFrame(self.timesDf[i], filter_dict)
                                        
             
        return self.joinedDf     
        
    def UpdateExportDf(self):
        """
        update dataframes for export
        
        0: take tabbDf as basis (because of time-format 00:00:01:16)
           join dbDf and extend of userDf         
        1: Filter: Last times: take last time from each user
                   Best times:
        2: Sort: basic or nested sorting
        3: Selection: take only column you need
        
        return: filtred, sorted and selected dataframe for total export
                (for category export has to be filtred) 
        """                
                                         
        #update joinedDf        
        columns =  self.dbDf.columns - self.tabDf.columns                              
        joinedTabDf = self.tabDf.join(self.dbDf[columns])         
         
        #user update
        userDf = psql.read_sql("SELECT * FROM users", db.getDb(), index_col = "id")        
        userDf = self.userDf[["year", "club", "sex", "o1", "o2", "o3", "o4"]]
        joinedTabDf =  pd.merge(joinedTabDf,  userDf, left_on='user_id', right_index=True, how="inner")
        joinedTabDf.sort("time_raw", inplace=True)                                      
         
        #replace nan with None
        self.joinedTabDf = joinedTabDf.where(pd.notnull(joinedTabDf), None)        
        
        #update order df
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
                aux_df =  aux_df[aux_df[filter_keys[0]] != ""]
            elif(len(filter_keys) == 2):
                aux_df =  aux_df[(aux_df[filter_keys[0]] != "") | (aux_df[filter_keys[1]] != "")]
            
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
            
            
            columns = tabExportSettings.exportgroups[i].GetCheckedColumns() 
            print aux_df.columns                       
            self.exportDf[i] = aux_df[columns]                            
                     
        return self.joinedDf         
                                                               
                    
    def IsTimeToCalc(self, dbTime):        
        
        #remote mode => no calc values      
        if dstore.GetItem("racesettings-app", ['remote']) != 0:            
            return False                                                        

        #no user, no calc
        if(dbTime['user_id'] == 0):
            return False   
        
        if dbTime['time_raw'] == None:
            return False         
            
        return True
    
    def IsFinishTime(self, dbTime): 
        
        if self.IsTimeToCalc(dbTime) == False:
            return False       
        
        eval_finish = dstore.GetItem("evaluation", ['finishtime'])
        
        if(dbTime['time1'] < TimesUtils.TimesUtils.timestring2time(eval_finish["time"], including_days = False)):
            return False
        
        if(dbTime['lap1'] < eval_finish["laps"]):
            return False
            
        return True

    def CalcOrder(self, dbTime, index):
        '''
        pokud není čas spočítá čas,
        pokud je čas a není lap spočítá lap                            
        '''                                                                                         
                         
        '''no order in some cases'''
        if(self.IsTimeToCalc(dbTime) == False):            
            return None          
        
        
        #get order group
        #group = dstore.GetItem('additional_info', ['order', index])                 
        #column1 = group['column1'].lower()                           
        
        #column is empty => no order
        #if(dbTime[column1] == None):            
        #    return None               
        
        #take order df
        group = dstore.GetItem('additional_info', ['order', index])                
        
        df = pd.DataFrame() 
        if(group['type'] == "All"):            
            df = self.orderDf[index]
        elif(group['type'] == "Category"):
            #df = self.orderDf[index]
            if(dbTime["category"] != None): 
                groupby = self.orderGroupbys[index]                                                          
                if (groupby != None) and (groupby.groups !={}): 
                    try:                                                            
                        df = groupby.get_group(dbTime["category"])
                    except KeyError: 
                        return None              
        elif(group['type'] == "Group#1"):                
            print "ERROR: Group order NOT implemented"
        elif(group['type'] == "Group#2"):
            print "ERROR: Group order NOT implemented"                
        elif(group['type'] == "Group#3"):
            print "ERROR: Group order NOT implemented"
        else:
            print "FATAL ERROR"                
        
        if df.empty:
            return None        
              
        #is this my last time?         
        if(not dbTime['id'] in df.id.values):                                
            return None
        
        # count only better times, df already sorted        
        aux_df = df.loc[:dbTime['id']]                               
                                         
        order = len(aux_df)               
        
        return order  
                
    def Calc(self, tabTime, index, key):
        '''
        společná funkce pro počítání time, lap
        '''                        
                                               
        '''no time in some cases'''     
        if(self.IsTimeToCalc(tabTime) == False):            
            return None               
                  
        #calc time        
        group = dstore.GetItem('additional_info', [key, index])
        
        if(group["checked"] == 0):
            return None
        
        if(self.joinedDf.empty):
            return None
        
        #get join time        
        joinTime = self.joinedDf[self.joinedDf.id == tabTime['id']]
        joinTime = joinTime.iloc[0]

        #evalute rule                                         
        time = timesstore.Evaluate(self.joinedDf, group, joinTime, tabTime)
             
        return time                                                     
    
    def CalcTime(self, dbTime, index):
        return self.Calc(dbTime, index, 'time')
    def CalcPoints(self, tabTime, index):
        points = self.Calc(tabTime, index, 'points')        
        return points
                    
    def CalcLap(self, dbTime, index):
        '''
        pokud není čas spočítá čas,
        pokud je čas a není lap spočítá lap            
        '''                                                    
                     
        '''no time in some cases'''
        if(self.IsTimeToCalc(dbTime) == False):
            return None                    

        ret_dict =  {}         
        timeX = "time"+str(index+1)
        lapX = "lap"+str(index+1)
        df = self.lapDf[index]     
            
        #calc lap        
        #if(pd.notnull(dbTime[timeX])) and (pd.isnull(dbTime[lapX])):
        #if(dbTime[timeX] != u"") and (dbTime[lapX] == u""):            
        if(dbTime[timeX] != None) and (dbTime[lapX] == None):            
            
            #same user
            aux_df = df[df['user_id'] == dbTime['user_id']]            
            
            #better times
            aux_df = aux_df[aux_df[timeX] < dbTime[timeX]]                                 
        
            lap = len(aux_df)
                        
            if (lap != None):
                lap = lap + 1                
           
        return lap
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
                        celltime = timesstore.GetPrevious(joinTime, {"cell":str(i)}, df) 
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
            tabUser =  tableUsers.getTabUserParIdOrTagId(joinTime["user_id"])          
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
    
