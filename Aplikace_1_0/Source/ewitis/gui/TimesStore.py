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
                    v = v.replace(" ", "") #mezery pryc
                    
                    # filter frame
                    #print df                                                                                                                                                                                                                                                           
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
                
    def Update(self, run_id, tabDf):
        '''
        najde všechny časy a uloží
        '''
        
        #update table df
        self.tabDf = tabDf
        #print tabDf
                
        #update db df
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
        #replace nan with None
        self.joinedDf = self.joinedDf.where(pd.notnull(self.joinedDf), None)
        
        #update order df
        self.orderDf = [pd.DataFrame()] * NUMBER_OF.POINTSCOLUMNS
        self.orderGroupbys = [None] * NUMBER_OF.POINTSCOLUMNS
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            
              
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
            #print "jDf", self.joinedDf
            aux_df = self.joinedDf[(self.joinedDf[column1]!=None) &  (self.joinedDf['user_id']!=0)]

            #sort
#             if(column2 in aux_df.columns):
#                 print "nested sorting", column1, column2, asc1, asc2
#                 aux_df = aux_df.sort([column1, column2], ascending = [asc1, asc2])
#             else:
#                 print "basic sorting"
#                 aux_df = aux_df.sort(column1, ascending = asc1)

            
            #last time from each user                    
            aux_df = aux_df.sort("time_raw")                                                    
            aux_df = aux_df.groupby("user_id", as_index = False).last()                        
            aux_df.set_index('id',  drop=False, inplace = True)
            
            #sort again
            if(column2 in aux_df.columns):
                #print "nested sorting", column1, column2, asc1, asc2
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
                
                #prepare filtered df for lap
                lap_group = dstore.GetItem('additional_info', ['lap', i])
                if(lap_group['checked'] != 0):                        
                    filter_dict = Assigments2Dict(dstore.GetItem("additional_info", [ "lap", i])['filter'])
                    self.lapDf[i] = timesstore.FilterFrame(self.timesDf[i], filter_dict)
                                        
             
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
                    df = groupby.get_group(dbTime["category"])               
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
        
        # count only better times
        #aux_df = df[df[column1] < dbTime[column1]]
        aux_df = df.loc[:dbTime['id']]                               
                                         
        order = len(aux_df) 
        #print "nr",  nr_of_better       
        
        return order  
                
    def Calc(self, dbTime, index, key):
        '''
        společná funkce pro počítání time, lap
        '''                        
                                               
        '''no time in some cases'''        
        if(self.IsTimeToCalc(dbTime) == False):
            return None               
                  
        #calc time        
        group = dstore.GetItem('additional_info', [key, index])                                 
        time = timesstore.Evaluate(self.joinedDf, group, {}, dbTime)
             
        return time                                                     
    
    def CalcTime(self, dbTime, index):
        return self.Calc(dbTime, index, 'time')
    def CalcPoints(self, dbTime, index):
        points = self.Calc(dbTime, index, 'points')
        #print "points", points, type(points)
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
        df = self.joinedDf        
            
        #calc lap        
        #if(pd.notnull(dbTime[timeX])) and (pd.isnull(dbTime[lapX])):
        if(dbTime[timeX] != None) and (dbTime[lapX] == None):            
            #lap = timesstore.GetNrOf(df, dbTime, [['==', 'user_id'], ['<', timeX]])
            #aux_df = timesstore.SelectFrame(df, dbTime, [['==', 'user_id'], ['<', timeX]])
            
            #empty user
            aux_df = df[df['user_id'] == 0]
            
            #same user
            aux_df = df[df['user_id'] == dbTime['user_id']]            
            
            #better times
            aux_df = aux_df[aux_df[timeX] < dbTime[timeX]]            
                                 
        
            lap = len(aux_df)
                        
            if (lap != None):
                lap = lap + 1                
           
        return lap
    
    def Evaluate(self, df, rule, tabTime, dbTime):
        points = None
        
    #     if filter != None:        
    #         for k,v in filter.iteritems():                
    #             if not isinstance(v, list):                          
    #                 if
    #             else:
    #                 df = df[df[k].str.contains(v)]
                
        minimum =  rule['minimum'] if ('minimum' in rule) else None
        maximum = rule['maximum'] if ('maximum' in rule) else None
        
        #rule
        rule = rule['rule']
        rule = rule.lower()
        
        #check if data exist
    #     if ("time1" in rule) and (dbTime['time1'] == None):    
    #         return None
    #     if ("time2" in rule) and (dbTime['time2'] == None):        
    #         return None
    #     if ("time3" in rule) and (dbTime['time3'] == None):        
    #         return None
    
        
        
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
        #print expression_string
         
        #UN1-UN3
        try:
            if ("un1" in rule):
                expression_string = expression_string.replace("un1", str(dbTime['un1']))
            if ("un2" in rule):                                
                expression_string = expression_string.replace("un2", str(dbTime['un2']))
            if ("un3" in rule):                                
                expression_string = expression_string.replace("un3", str(dbTime['un3']))
        except KeyError:        
            return None
        
        # ORDER1-ORDER3       
        try:
            if ("order1" in rule):                                
                expression_string = expression_string.replace("order1", str(tabTime['order1']))
            if ("order2" in rule):                                
                expression_string = expression_string.replace("order2", str(tabTime['order2']))
            if ("order3" in rule):                                
                expression_string = expression_string.replace("order3", str(tabTime['order3']))
        except KeyError:        
            return None
        
        # POINTS1-POINTS3       
        try:
            if ("points1" in rule):                                
                expression_string = expression_string.replace("points1", str(tabTime['points1']))
            if ("points2" in rule):                                
                expression_string = expression_string.replace("points2", str(tabTime['points2']))
            if ("points3" in rule):                                
                expression_string = expression_string.replace("points3", str(tabTime['points3']))
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
                #print celltimeX, rule
                if (celltimeX in rule):
                    try:  
                        celltime = timesstore.GetPrevious(dbTime, {"cell":str(i)}, df) 
                        expression_string = expression_string.replace(celltimeX, str(celltime['time_raw']))                 
                    except TypeError:       
                        print "type error"         
                        return None
                
        # STARTTIME    
        #user without number => no time
        if ("starttime" in rule):
            starttime = None          
            tabUser =  tableUsers.getTabUserParIdOrTagId(dbTime["user_id"])          
            if(tabUser['nr'] == 0):
                return None        
        
            if(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):
                #VIA CATEGORY => Xth starttime                                                                                                                              
                start_nr = tableCategories.getTabRow(tabUser['category_id'])['start_nr'] #get category starttime                
                starttime = timesstore.Get(df, start_nr, filter = {'cell':1})                                                                                        
            elif(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
                #VIA USER => previous startime from the same user                                                
                starttime = timesstore.GetPrevious(dbTime, filter = {'cell':1}, df = df)
            else:
                print "E: Fatal Error: Starttime "
                return None
            
            if starttime != None:
                expression_string = rule.replace("starttime", str(starttime['time_raw']))
                        
                                           
               
        # TIME1-TIME3                                                        
        expression_string = expression_string.replace("time1", str(dbTime['time1']))       
        expression_string = expression_string.replace("time2", str(dbTime['time2']))       
        expression_string = expression_string.replace("time3", str(dbTime['time3']))
               
        # TIME
        expression_string = expression_string.replace("time", str(dbTime['time_raw']))
                
        ''' evaluate expresion '''
        #print "ES",expression_string 
        try:            
            points = eval(expression_string)        
        except (SyntaxError, TypeError, NameError):
            print "I: invalid string for evaluation", expression_string            
            return None        
        
        #restrict final value               
        if minimum and (points < minimum):
            points = minimum
        if maximum and (points > maximum):
            points = maximum                     
                
        #print points, rule
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
    
