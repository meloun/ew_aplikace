# -*- coding: utf-8 -*-

from ewitis.data.DEF_DATA import *


class ZeroRawTime_Error(Exception): pass
class NoneRawTime_Error(Exception): pass
class TimeFormat_Error(Exception): pass

class TimesUtils():
    def __init__(self):
        pass                        
    
    #time_raw => time
    @staticmethod
    def time2timestring(time):
        
        if (time == None):
            return None
        
        '''convert'''
        hours = time / (100*60*60)
        
        time = time % (100*60*60)
        minutes = time / (100*60)
        
        time = time % (100*60)
        seconds = time / (100)
        
        milliseconds = time % (100)
        
        return '%02d:%02d:%02d,%02d' %(hours, minutes, seconds, milliseconds)
        
        
  
    
    @staticmethod 
    def timestring2time(timestring):       
        
        #split to hours(01), minutes(02) and seconds(35,42)
        timestring = timestring.split(":")                                         
        if (len(timestring)) != 3 : #check: 2x colon?
            raise TimeFormat_Error
    
        #get seconds
        time_seconds = timestring[2].split(",")
        if (len(time_seconds)) != 2 : #check: 1x point?                 
            raise TimeFormat_Error
        
        try:
            hours = int(timestring[0])
            minutes = int(timestring[1])
            seconds = int(time_seconds[0])
            tens_ms = int(time_seconds[1])
        except:
            raise TimeFormat_Error
        
        if (hours > 59) or (minutes > 59) or (seconds > 59):
            raise TimeFormat_Error                 
        
        time = ((hours*60*60)+(minutes*60) + seconds)*100 + tens_ms
                                   
        return time
    
    
class TimesStarts():
    def __init__(self, db):                              
        self.db = db                        
        self.Update()                                             
              
    def GetDefault(self):
        return {id:0, 'time_raw':0}
    def GetFirst(self, run_id):
        return self.start_times[run_id][0]    
    def Get(self, run_id, nr):                     
        return self.start_times[run_id][nr-1]
    
                      
    
    #getStartTimer - return all start times of 
    def Update(self):
        
        #
        query = \
                " SELECT * FROM times" +\
                    " WHERE (times.cell = 1 )"+\
                    " ORDER BY times.run_id"                                                        
        #
        start_times={}
        
        #get all start times
        times = self.db.query(query)
                
        #convert to dicts                             
        times = self.db.cursor2dicts(times)
        
        #{3:[time, time, time], 4:[time, time]}
        for time in times:                        
            if ((time['run_id'] in start_times) == False):                                
                start_times[time['run_id']] = []
                
            start_times[time['run_id']].append(time)
        
        #assign to global list
        self.start_times = start_times
        
class TimesOrder():
    IS_BEST_TIME, IS_WORST_TIME = range(0,2)
    
    def __init__(self, db, datastore):        
                  
        self.db = db
        self.datastore = datastore   
    
    def IsLastUsertime_old(self, dbTime):
        '''
        jde momentálně o poslední čas daného závodníka?
        '''
               
        if(dbTime['time'] == None):
            return True
              
        if(dbTime['time'] == 0):
            return True
            
        if(dbTime['cell'] == 1):            
            return True                                        

        if(dbTime['user_id'] == 0):
            return True  
                
        query_order = \
        " SELECT COUNT(times.id) FROM times" +\
            " WHERE (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
            " AND (times.user_id == " +str(dbTime['user_id'])+ ")"+\
            " AND (times.time_raw > " + str(dbTime['time_raw']) + ")"            
        
        #print "islastusertime:", query_order
        res_cnt = self.db.query(query_order).fetchone()[0]                                                         

        if(res_cnt == 0):
            return True
                      
        return False
    

    
    def IsUserTime(self, dbTime, mode):
        '''
        jde momentálně o poslední čas daného závodníka?
        '''
               
        if(dbTime['time'] == None):
            return True
              
        if(dbTime['time'] == 0):
            return True
            
        if(dbTime['cell'] == 1):            
            return True                                        

        if(dbTime['user_id'] == 0):
            return True  
                
                
        query = \
            " SELECT COUNT(times.id) FROM times" +\
                " WHERE "
                    
        if(self.datastore.Get('show')['alltimes'] == 0):
            query = query + \
            " (times.run_id=\""+str(dbTime['run_id'])+"\") AND"
                
                
        query = query + \
            " (times.user_id == " +str(dbTime['user_id'])+ ") AND "\
            " (times.cell != 1)"
        
        
        if(mode == self.IS_WORST_TIME):
            query = query + \
            " AND (times.time_raw > " + str(dbTime['time_raw']) + ")"
        elif(mode == self.IS_BEST_TIME):
            query = query + \
            " AND (times.time_raw < " + str(dbTime['time_raw']) + ")"
                        
                
        res_cnt = self.db.query(query).fetchone()[0]                                                         

        #print "isusertime:",res_cnt, query            
        if(res_cnt == 0):
            return True
                      
        return False
    
    def IsLastUsertime(self, dbTime):
        return self.IsUserTime(dbTime, self.IS_WORST_TIME)
        
    def IsBestUsertime(self, dbTime):
        return self.IsUserTime(dbTime, self.IS_BEST_TIME)
    
    def IsToShow(self, dbTime):
        if(self.datastore.Get('order_evaluation') == OrderEvaluation.RACE \
           and self.IsLastUsertime(dbTime)):
            return True
        elif(self.datastore.Get('order_evaluation') == OrderEvaluation.SLALOM \
             and self.IsBestUsertime(dbTime)):
            return True
        return False
                 
    def Get(self, dbTime, lap, category_id = None):
        """
        """       
                    
        # zobrazovat pořadí? (kontrola checkboxů)        
        if (self.datastore.Get("additional_info")["enabled"] == 0):                 
            return None
        if (category_id == None) and (self.datastore.Get("additional_info")["order"] == 0):
            return None
        if (category_id != None) and (self.datastore.Get("additional_info")["order_in_cat"] == 0):
            return None
        
        # RACE:    pořadí jen u nejhorších/posledních časů
        # SLALOM:  pořadí jen u prvních/nejlepších časů
        if(self.IsToShow(dbTime) == False):
            return None
        
        if(dbTime['time'] == None):
            return None
              
        if(dbTime['time'] == 0):
            return None
            
        if(dbTime['cell'] == 1):            
            return None                                        

        if(dbTime['user_id'] == 0):
            return None            
        
        if category_id != None:     
            
            '''ORDER IN THE SAME CATEGORY'''        
            
            #shlukovat do skupin podle zavodníků
            query_order = \
            "SELECT COUNT(*) FROM("+\
                " SELECT user_id FROM times"

            """
            ir:    user_id == users.id
            rfid:  user_id == tag_id
            """                  
            if(self.datastore.Get('rfid') == 2):
                query_order = query_order + \
                " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                " INNER JOIN users ON tags.user_nr = users.nr "
            else:
                query_order = query_order + \
                " INNER JOIN users ON times.user_id = users.id"
                
            query_order = query_order + \
                    " WHERE (times.time < " + str(dbTime['time']) + ")"
            
            if(self.datastore.Get('show')['alltimes'] == 0):
                query_order = query_order + \
                        " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                                    
            #if(self.datastore.Get('onelap_race') == 0):
            query_order = query_order + \
                        " AND (times.user_id != " +str(dbTime['user_id'])+ ")"
            
            query_order = query_order + \
                        " AND (times.user_id != 0)"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " GROUP BY user_id"

            if(self.datastore.Get('order_evaluation') == OrderEvaluation.RACE):
                query_order = query_order + \
                        " HAVING count(*) == " + str(lap)                        
                    
            if(self.datastore.Get('onelap_race') == 0) and (self.datastore.Get('order_evaluation') != OrderEvaluation.SLALOM):
                
                #zohlednit závodníky s horším časem ale více koly
                
                query_order = query_order + \
                    " UNION "+\
                    " SELECT user_id FROM times"
                    
                if(self.datastore.Get('rfid') == 2):  
                    query_order = query_order + \
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "
                else:
                    query_order = query_order + \
                        " INNER JOIN users ON times.user_id = users.id"
                    
                query_order = query_order + \
                        " WHERE"
                        
                if(self.datastore.Get('show')['alltimes'] == 0):
                    query_order = query_order + \
                            "(times.run_id=\""+str(dbTime['run_id'])+"\") AND"
                            
                query_order = query_order + \
                            " (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                            " AND (times.user_id != 0 )"+\
                            " AND (times.time != 0 )"+\
                            " AND (times.cell != 1 )"+\
                            " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) > "+str(lap)
                        
            query_order = query_order + ")"                               
            
            #print "query_order_cat: ",self.datastore.Get('onelap_race') ,query_order                                 
                                                                                                                          
        else:                    
            '''ORDER IN ALL RUN'''            
            query_order = \
            "SELECT COUNT(*) FROM("+\
                "SELECT user_id FROM times"
            
            query_order = query_order + \
                    " WHERE (times.time < " + str(dbTime['time']) + ")"
                        
            if(self.datastore.Get('show')['alltimes'] == 0):
                query_order = query_order + \
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"

            #if(self.datastore.Get('onelap_race') == 0):
            query_order = query_order + \
                    " AND (times.user_id != " +str(dbTime['user_id'])+ ")"
                                
            query_order = query_order + \
                    " AND (times.user_id != 0)"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"
            
            query_order = query_order + \
                    " GROUP BY user_id"
                
            if(self.datastore.Get('order_evaluation') == OrderEvaluation.RACE):
                query_order = query_order + \
                    " HAVING count(*) == " + str(lap)
        
            if(self.datastore.Get('onelap_race') == 0) and (self.datastore.Get('order_evaluation') != OrderEvaluation.SLALOM):
                
                #zohlednit závodníky s horším časem ale více koly
                
                query_order = query_order + \
                " UNION "+\
                " SELECT user_id FROM times" +\
                    " WHERE"
                    
                if(self.datastore.Get('show')['alltimes'] == 0):
                    query_order = query_order + \
                    " (times.run_id=\""+str(dbTime['run_id'])+"\") AND"
                                     
                query_order = query_order +\
                    " (times.user_id != 0)"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " GROUP BY user_id"+\
                    " HAVING count(*) > "+str(lap)
                    
            query_order = query_order +\
            ")"
                                                                                        
            #print "order in run: ", query_order                                                   
                                                       
        try:
            #print query_order
            res_order = self.db.query(query_order).fetchone()[0]
            res_order = res_order + 1        
        except:
            res_order = None                            

        return res_order
     
    def Get_old(self, dbTime, lap, category_id = None):
        """
        RFID Race: 
            true: user_id v tabulce times obsahuje tag_id
            false: user_id prima relace do tabulky users 
        One Lap Race:
            true: závodník má jen jeden čas
            false: je nutno zohlednit závodníky s horšímy časy ale větším počtem kol
        1user 1order:
            true:
        """
        
        if (self.datastore.Get("additional_info")["enabled"] == 0):                 
            return None
        if (category_id == None) and (self.datastore.Get("additional_info")["order"] == 0):
            return None
        if (category_id != None) and (self.datastore.Get("additional_info")["order_in_cat"] == 0):
            return None
        
        if(dbTime['time'] == None):
            return None
              
        if(dbTime['time'] == 0):
            return None
            
        if(dbTime['cell'] == 1):            
            return None                                        

        if(dbTime['user_id'] == 0):
            return None            
        
        if category_id != None:     
            
            '''ORDER IN THE SAME CATEGORY'''        
                           
            if(self.datastore.Get('rfid') == 2):                
                query_order = \
                "SELECT COUNT(*) FROM("+\
                    " SELECT user_id FROM times" +\
                    " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                    " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " WHERE (times.time < " + str(dbTime['time']) + ")"+\
                        " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                        " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                        " AND (times.user_id != 0)"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " GROUP BY user_id"+\
                        " HAVING count(*) == "+str(lap)
                if(self.datastore.Get('onelap_race') == 0):
                    query_order = query_order + \
                        " UNION "+\
                        " SELECT user_id FROM times" +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                            " WHERE (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                            " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                            " AND (times.user_id != 0 )"+\
                            " AND (times.time != 0 )"+\
                            " AND (times.cell != 1 )"+\
                            " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) > "+str(lap)
                query_order = query_order + ")"                   
            else:                
                query_order = \
                "SELECT COUNT(*) FROM("+\
                    "SELECT user_id FROM times" +\
                    " INNER JOIN users ON times.user_id = users.id"+\
                        " WHERE (times.time < " + str(dbTime['time']) + ")"#+\
                        #" AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                if(self.datastore.Get('show')['alltimes'] == 0):
                    query_order = query_order + " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                query_order = query_order + \
                        " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                        " AND (times.user_id != 0)"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " GROUP BY user_id"+\
                        " HAVING count(*) == "+str(lap)
                if(self.datastore.Get('onelap_race') == 0):                    
                    query_order = query_order +\
                        " UNION "+\
                        " SELECT user_id FROM times" +\
                        " INNER JOIN users ON times.user_id = users.id"+\
                            " WHERE (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                            " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                            " AND (times.user_id != 0)"+\
                            " AND (times.time != 0 )"+\
                            " AND (times.cell != 1 )"+\
                            " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) > "+str(lap)
                query_order = query_order + ")"
            
            #print "query_order: ",self.datastore.Get('onelap_race') ,query_order                                 
                        
                                                                                          
        
        else:                    
            '''ORDER IN ALL RUN'''
            if(self.datastore.Get('rfid') == 2):  
                query_order = \
                    "SELECT COUNT(*) FROM("+\
                        "SELECT user_id FROM times" +\
                            " WHERE (times.time < " + str(dbTime['time']) + ")"#+\
                            #" AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                if(self.datastore.Get('show')['alltimes'] == 0):
                    query_order = query_order + " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                query_order = query_order + \
                            " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                            " AND (times.user_id != 0)"+\
                            " AND (times.time != 0 )"+\
                            " AND (times.cell != 1 )"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) == " + str(lap)
                if(self.datastore.Get('onelap_race') == 0):
                        query_order = query_order +\
                        " UNION "+\
                        " SELECT user_id FROM times" +\
                            " WHERE (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                            " AND (times.user_id != 0)"+\
                            " AND (times.time != 0 )"+\
                            " AND (times.cell != 1 )"+\
                            " GROUP BY user_id"+\
                            " HAVING count(*) > "+str(lap)
                query_order = query_order + ")"
            else:
                query_order = \
                    "SELECT COUNT(user_id) FROM times"+\
                        " WHERE (times.time < " + str(dbTime['time']) + ")"                            
                if(self.datastore.Get('show')['alltimes'] == 0):
                    query_order = query_order + " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                query_order = query_order + \
                        " AND (times.user_id != 0)"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"                                                            
            print "query_order: ",query_order                                             
                                                       
        try:
            print query_order
            res_order = self.db.query(query_order).fetchone()[0]
            #res_order_2 = self.db.query(query_order_2).fetchone()[0]
           
            #print "query_order2: ",query_order_2 
            #print str(res_order)+","+str(res_order_2)
            res_order = res_order + 1 #+ res_order_2        
        except:
            res_order = None                            

        return res_order 
#    def Get_old(self, dbTime, category_id = None):
#        
#        if(self.datastore.Get("additinal_info") == False):            
#            return None
#        
#        if(dbTime['time'] == None):
#            return None
#              
#        if(dbTime['time'] == 0):
#            return None
#            
#        if(dbTime['cell'] == 1):            
#            return None                                        
#    
#        if category_id != None:     
#            
#            '''ORDER IN THE SAME CATEGORY'''        
#                           
#            if(self.datastore.Get('rfid') == True):                
#                query_order = \
#                    " SELECT COUNT(times.id) FROM times" +\
#                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
#                        " INNER JOIN users ON tags.user_nr = users.nr "+\
#                        " WHERE (times.time < " +str(dbTime['time'])+ ")"+\
#                        " AND (times.time != 0 )"+\
#                        " AND (times.cell != 1 )"+\
#                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
#                        " AND (times.run_id=" +str(dbTime['run_id'])+ ")"
#            else:
#                query_order = \
#                    "SELECT COUNT(*) FROM times" +\
#                        " INNER JOIN users ON times.user_id = users.id"+\
#                        " INNER JOIN categories ON users.category_id = categories.id "+\
#                        " WHERE (times.time < " +str(dbTime['time'])+ ")"+\
#                        " AND (times.time != 0 )"+\
#                        " AND (times.cell != 1 )"+\
#                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
#                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
#                        
#                        #" AND (categories.name=\"" +str(category)+ "\")"+\
#        
#        else:
#            
#            '''ORDER IN ALL RUN'''
#            
#            query_order = \
#                "SELECT COUNT(times.id) FROM times" +\
#                    " WHERE (times.time<" + str(dbTime['time']) + ")"+\
#                    " AND (times.time != 0 )"+\
#                    " AND (times.cell != 1 )"+\
#                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
#                               
#
#        #import time                     
#        
#        #print "..1", time.time()
#        res_order = self.db.query(query_order).fetchone()[0]+1
#        #print "..2", time.time() 
#               
#        #res_count = self.db.query(query_count).fetchone()[0]        
#        #return {"start":res_order, "end":res_order+res_count-1}              
#        return res_order
    
                

    
class TimesLap():
    def __init__(self, db, datastore):                          
        self.db = db
        self.datastore = datastore
        
    def Get(self, dbTime):
        '''
        spočítá kolikáté kolo daného závodníka je tento čas
        '''        
        
        if(self.datastore.Get("additional_info")['enabled'] == 0):            
            return None                               
        
        if(dbTime['time_raw'] == None):
            return None;

        if(dbTime['cell'] == 1):
            return None
                    
        if(dbTime['time_raw'] == 0):
            return None
        
        if(dbTime['user_id'] == 0):
            return None         

        '''v čase může být user_id pro které neexistuje uživatel => lap =0'''        
        #if(self.TimesModel.params.tabUser.getDbUserParIdOrTagId(time["user_id"]) == None):           
        #    return 0         
    
        '''count of times - same race, same user, better time, exclude start time'''
        query = \
                "SELECT COUNT(*) FROM times" +\
                    " WHERE "
                    
        if(self.datastore.Get('show')['alltimes'] == 0):
            query = query + \
                " (times.run_id=\""+str(dbTime['run_id'])+"\") AND"
                    
        query = query + \
                " (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"+\
                " AND (times.time_raw <" + str(dbTime['time_raw']) + ")"+\
                " AND (times.cell != 1)"
     
        #print "query lap: ", query          
        count = self.db.query(query).fetchone()[0]+1
        return count
    
    def GetLaps(self, dbTime):
        '''
        vrátí počet kol daného uživatele
        '''
                
                
        if(dbTime['cell'] == 1):
            return None                    
        
        if(dbTime['user_id'] == 0):
            return None         
    
        '''count of times - same race, same user, better time, exclude start time'''
        query = \
                "SELECT COUNT(*) FROM times" +\
                    " WHERE (times.run_id ==" + str(dbTime['run_id'])+ ")"+\
                    " AND (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"+\
                    " AND (times.cell != 1)"
     
        #print query          
        count = self.db.query(query).fetchone()[0]
        return count        
    
class TimesLaptime():
    def __init__(self, db, datastore):                          
        self.db = db
        self.datastore = datastore
    
    def Get(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
        if  self.datastore.Get("additional_info")['enabled'] == 0:
            return None 
        
        if self.datastore.Get("additional_info")['laptime'] == 0:
            return None        
        
        if(self.datastore.Get('show')['alltimes'] == 2):
            return None                         
        
        if(dbTime['time_raw'] == None):
            #print "laptime: neni time_raw", dbTime
            return None

        if(dbTime['cell'] == 1):
            #print "laptime: spatna cell", dbTime
            return None
                    
        if(dbTime['time_raw'] == 0):
            #print "laptime: zero time_raw", dbTime
            return None
        
        if(dbTime['user_id'] == 0):
            #print "laptime: neni user", dbTime
            return None
        
        '''count of times - same race, same user, better time, exclude start time'''
        query = \
                "SELECT time_raw FROM times" +\
                    " WHERE"
        if(self.datastore.Get('show')['alltimes'] == 0):
            query = query + \
                    "(times.run_id ==" + str(dbTime['run_id'])+ ") AND"
                    
        query = query + \
                    " (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"+\
                    " AND (times.time_raw <" + str(dbTime['time_raw']) + ")"+\
                    " AND (times.cell != 1)"+\
                    " ORDER BY time_raw DESC"+\
                    " LIMIT 1"

        #print "query laptime: ", query                      
        res = self.db.query(query).fetchone()
        if res == None:
            return None        
        return dbTime['time_raw'] - res['time_raw']    
        
    def GetBest(self, dbTime):
        '''
        vyhledá přechozí čas a spočítá laptime
        '''
        
        if self.datastore.Get("additional_info")['enabled'] == 0:
            return None
        
        if self.datastore.Get("additional_info")['best_laptime'] == 0:
            return None
        
        if(self.datastore.Get('show')['alltimes'] == 2):
            return None         
                               
        if(dbTime['time_raw'] == None):            
            return None;

        if(dbTime['cell'] == 1):            
            return None
                    
        if(dbTime['time_raw'] == 0):            
            return None
        
        if(dbTime['user_id'] == 0):            
            return None
        
        '''count of times - same race, same user, better time, exclude start time'''
        query = \
                "SELECT min(laptime) FROM times" +\
                    " WHERE (times.run_id ==" + str(dbTime['run_id'])+ ")"+\
                    " AND (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"
        res = self.db.query(query).fetchone()                
        if res == None:
            return None
        return res[0]
        
        
                    
        
        
