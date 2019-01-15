# -*- coding: utf-8 -*-

from ewitis.data.DEF_DATA import *
from ewitis.data.db import db
from ewitis.data.dstore import dstore


class ZeroRawTime_Error(Exception): pass
class NoneRawTime_Error(Exception): pass
class TimeFormat_Error(Exception): pass

class TimesUtils():
    def __init__(self):
        pass                        
    
    @staticmethod
    def time2timestring(time, including_days = False, including_hours = True):
        '''
        321561546 => 1293| 12:01:02,11
        '''
        
        if (time == None):
            return None        
        
        '''convert'''
        if(including_days):
            days = time / (24*100*60*60)        
            time = time % (24*100*60*60)
                                 
        hours = time / (100*60*60)        
        time = time % (100*60*60)
        
        minutes = time / (100*60)        
        time = time % (100*60)
        
        seconds = time / (100)
                
        milliseconds_x10 = time % (100)
        
        if(including_days):
            return '%02d| %02d:%02d:%02d,%02d' % (days, hours, minutes, seconds, milliseconds_x10)
        
        if(including_hours == False):
            return '%02d:%02d,%02d' % (minutes, seconds, milliseconds_x10)
        
        
        return '%02d:%02d:%02d,%02d' % (hours, minutes, seconds, milliseconds_x10)
        
        
    @staticmethod 
    def timemembers2time(days, hours, minutes, seconds, milliseconds_x10):
        '''
        12,01,02,11 => "12:01:02,11"
        '''
        if (minutes > 59) or (seconds > 59):
            raise TimeFormat_Error
        time = ((days*24*60*60)+(hours*60*60)+(minutes*60) + seconds)*100 + milliseconds_x10
        return time
    
    @staticmethod 
    def timestruct2time(timestruct):
        '''
        {12,01,02,11} => "12:01:02,11"
        '''        
        return TimesUtils.timenumbers2time(timestruct["hours"],timestruct["minutes"], timestruct["seconds"],timestruct["milliseconds_x10"])
    
    @staticmethod 
    def timestring2time(timestring, including_days = True):
        '''               
        "12:01:02,11" => 545464683
        '''        
        
        #get days
        if(including_days == True):
            try:
                time_days = timestring.split("|")
            except AttributeError:
                raise TimeFormat_Error
            if (len(time_days)) != 2 :
                raise TimeFormat_Error
            timestring = time_days[1]
            time_days = time_days[0]
        else:
            time_days = 0
                    
        #split to hours(01), minutes(02) and seconds(35,42)
        try:
            timestring = timestring.split(":")                                         
        except AttributeError:
            raise TimeFormat_Error
        
        if (len(timestring)) == 2 : #check: 2x splits?                
            timestring.insert(0, "00")
        elif (len(timestring)) != 3 : #check: 3x splits?
            raise TimeFormat_Error        

            
        
        #get seconds
        time_seconds = timestring[2].split(",")
        if (len(time_seconds)) != 2 : #check: 1x point?                 
            raise TimeFormat_Error
        
        try:
            days = int(time_days)  
            hours = int(timestring[0])
            minutes = int(timestring[1])
            seconds = int(time_seconds[0])
            milliseconds_x10 = int(time_seconds[1])
        except:
            raise TimeFormat_Error
        
        time = TimesUtils.timemembers2time(days, hours, minutes, seconds, milliseconds_x10)
                                   
        return time        
    
    @staticmethod 
    def times_difference(timestring1, timestring2):
        '''
        "00:01:03,15", "00:01:02,11" => "00:00:01,04"
        '''
        #print "timestring1",timestring1
        #print "timestring2",timestring2

        t1 = TimesUtils.timestring2time(timestring1, including_days = False)
        t2 = TimesUtils.timestring2time(timestring2, including_days = False)        
        timestring = TimesUtils.time2timestring(t1 - t2)
        #if(t1<t2)
        #    time_string = "-"+time_string
        return timestring
    

    
           
class TimesOrder():
    '''
    Pořadí závodníka v závodě/kategorii
        - IsLastTime()
        - IsBestTime()
        - IsResultTime()
        - Get()
    '''    
    IS_BEST_TIME, IS_WORST_TIME = range(0,2)
    
    def __init__(self):                          
        pass
    
    def IsUserTime(self, dbTime, mode):
        '''
        jde momentálně o poslední/nejlepší čas daného závodníka?
        '''
               
        if(dbTime['time1'] == None):
            return True
              
        if(dbTime['time1'] == 0):
            return True
            
        if(dbTime['cell'] == 1):            
            return True                                        

        if(dbTime['user_id'] == 0):
            return True  
                
                
        query = \
            " SELECT COUNT(times.id) FROM times" +\
                " WHERE "                    
                
                
        query = query + \
            " (times.user_id == " +str(dbTime['user_id'])+ ") AND "+\
            " (times.cell = 250)"
        
        
        if(mode == self.IS_WORST_TIME):
            query = query + \
            " AND (times.time_raw > " + str(dbTime['time_raw']) + ")"
        elif(mode == self.IS_BEST_TIME):
            query = query + \
            " AND (times.time_raw < " + str(dbTime['time_raw']) + ")"
                                                        
        res_cnt = db.query(query).fetchone()[0]                                                                                                                                 

        #print "isusertime:",res_cnt, query            
        if(res_cnt == 0):
            return True
                      
        return False
    
    def IsLastUsertime(self, dbTime):
        return self.IsUserTime(dbTime, self.IS_WORST_TIME)
        
    def IsBestUsertime(self, dbTime):
        return self.IsUserTime(dbTime, self.IS_BEST_TIME)
    
    def IsResultTime(self, dbTime):
        if(dstore.Get('evaluation')['order'] == OrderEvaluation.RACE \
           and self.IsLastUsertime(dbTime)):
            return True
        elif(dstore.Get('evaluation')['order'] == OrderEvaluation.SLALOM \
             and self.IsBestUsertime(dbTime)):
            return True
        return False
                 
    def Get(self, dbTime, lap, category_id = None):
        """
        vrací pořadí závodníka v závodě/kategorii
        """       
                    
        # zobrazovat pořadí? (kontrola checkboxů)        
#        if (dstore.Get("additional_info")["enabled"] == 0):                 
#            return None
#        if (category_id == None) and (dstore.Get("additional_info")["order"] == 0):
#            return None
#        if (category_id != None) and (dstore.Get("additional_info")["order_in_cat"] == 0):
#            return None
        
        # RACE:    pořadí jen u nejhorších/posledních časů
        # SLALOM:  pořadí jen u prvních/nejlepších časů
        if(self.IsResultTime(dbTime) == False):
            return None
        
        if(dbTime['time1'] == None):
            return None
              
        if(dbTime['time1'] == 0):
            return None
            
        if(dbTime['cell'] == 1):            
            return None                                        

        if(dbTime['user_id'] == 0):
            return None            
        
        if category_id != None:     
            
            '''ORDER IN THE SAME CATEGORY'''        
            
            #do skupin podle zavodníků (group by)
            query_order = \
            "SELECT COUNT(*) FROM("+\
                " SELECT user_id FROM times"

            #ir:    bez tabulky tags  => user_id == users.id
            #rfid:  přes tabulku tags => user_id == tag_id
            if(dstore.GetItem("racesettings-app", ['rfid']) == 2):
                query_order = query_order + \
                " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                " INNER JOIN users ON tags.user_nr = users.nr "
            else:
                query_order = query_order + \
                " INNER JOIN users ON times.user_id = users.id"
                
            query_order = query_order + \
                    " WHERE (times.time < " + str(dbTime['time1']) + ")"            

            #if(dstore.Get('onelap_race') == 0):
            query_order = query_order + \
                        " AND (times.user_id != " +str(dbTime['user_id'])+ ")"

            query_order = query_order + \
                        " AND (times.user_id != 0)"+\
                        " AND (times.time != 0 )"

            if(dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ALL_TIMES):
                query_order = query_order + \
                    " AND (times.cell != 1 )"
            else:
                query_order = query_order + \
                        " AND (times.cell = 250 )"
                        
            query_order = query_order + \
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " GROUP BY user_id"

            if(dstore.Get('evaluation')['order'] == OrderEvaluation.RACE):
                query_order = query_order + \
                        " HAVING count(*) == " + str(lap)                        
                                
            if(dstore.Get('evaluation')['order'] != OrderEvaluation.SLALOM):
                
                #zohlednit závodníky s horším časem ale více koly
                
                query_order = query_order + \
                    " UNION "+\
                    " SELECT user_id FROM times"
                    
                if(dstore.GetItem("racesettings-app", ['rfid']) == 2):  
                    query_order = query_order + \
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "
                else:
                    query_order = query_order + \
                        " INNER JOIN users ON times.user_id = users.id"
                    
                query_order = query_order + \
                        " WHERE"
                            
                query_order = query_order + \
                            " (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                            " AND (times.user_id != 0 )"+\
                            " AND (times.time != 0 )"
                            
                if(dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ALL_TIMES):
                    query_order = query_order + \
                        " AND (times.cell != 1 )"
                else:
                    query_order = query_order + \
                        " AND (times.cell = 250 )"
                        
                query_order = query_order + \
                            " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) > "+str(lap)
                        
            query_order = query_order + ")"                               
            
            #print "query_order_cat: ",dstore.Get('onelap_race') ,query_order                                 
                                                                                                                          
        else:                    
            '''ORDER IN ALL RUN'''            
            query_order = \
            "SELECT COUNT(*) FROM("+\
                "SELECT user_id FROM times"
            
            query_order = query_order + \
                    " WHERE (times.time < " + str(dbTime['time1']) + ")"

            #if(dstore.Get('onelap_race') == 0):
            query_order = query_order + \
                    " AND (times.user_id != " +str(dbTime['user_id'])+ ")"

            query_order = query_order + \
                    " AND (times.user_id != 0)"+\
                    " AND (times.time != 0 )"

            if (dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ALL_TIMES):
                query_order = query_order + \
                    " AND (times.cell != 1 )"
            else:
                query_order = query_order + \
                    " AND (times.cell = 250 )"
            
            query_order = query_order + \
                    " GROUP BY user_id"
                
            if(dstore.Get('evaluation')['order'] == OrderEvaluation.RACE):
                query_order = query_order + \
                    " HAVING count(*) == " + str(lap)
                    
            if(dstore.Get('evaluation')['order'] != OrderEvaluation.SLALOM):
                
                #zohlednit závodníky s horším časem ale více koly
                
                query_order = query_order + \
                " UNION "+\
                " SELECT user_id FROM times" +\
                    " WHERE"                    
                                     
                query_order = query_order +\
                    " (times.user_id != 0)"+\
                    " AND (times.time != 0 )"

                if(dstore.Get("evaluation")['laptime'] == LaptimeEvaluation.ALL_TIMES):
                    query_order = query_order + \
                        " AND (times.cell != 1 )"
                else:
                    query_order = query_order + \
                        " AND (times.cell = 250 )"
                        
                query_order = query_order + \
                    " GROUP BY user_id"+\
                    " HAVING count(*) > "+str(lap)
                    
            query_order = query_order +\
            ")"
                                                                                        
            #print "order in run: ", query_order                                                   
                                                       
        try:
            #print query_order
            res_order = db.query(query_order).fetchone()[0]
            res_order = res_order + 1        
        except:
            res_order = None                            

        return res_order
    

    
       
    

        
        
                    
        
        
