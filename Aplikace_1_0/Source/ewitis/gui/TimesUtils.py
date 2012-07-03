# -*- coding: utf-8 -*-
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
    def __init__(self, db, datastore):        
                  
        self.db = db
        self.datastore = datastore        

    def Get_old(self, dbTime, category_id = None):
        
        if(self.datastore.Get("additinal_info") == False):            
            return None
        
        if(dbTime['time'] == None):
            return None
              
        if(dbTime['time'] == 0):
            return None
            
        if(dbTime['cell'] == 1):            
            return None                                        
    
        if category_id != None:     
            
            '''ORDER IN THE SAME CATEGORY'''        
                           
            if(self.datastore.Get('rfid') == True):                
                query_order = \
                    " SELECT COUNT(times.id) FROM times" +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " WHERE (times.time < " +str(dbTime['time'])+ ")"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " AND (times.run_id=" +str(dbTime['run_id'])+ ")"
            else:
                query_order = \
                    "SELECT COUNT(*) FROM times" +\
                        " INNER JOIN users ON times.user_id = users.id"+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time < " +str(dbTime['time'])+ ")"+\
                        " AND (times.time != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
                        
                        #" AND (categories.name=\"" +str(category)+ "\")"+\
        
        else:
            
            '''ORDER IN ALL RUN'''
            
            query_order = \
                "SELECT COUNT(times.id) FROM times" +\
                    " WHERE (times.time<" + str(dbTime['time']) + ")"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                               

        #import time                     
        
        #print "..1", time.time()
        res_order = self.db.query(query_order).fetchone()[0]+1
        #print "..2", time.time() 
               
        #res_count = self.db.query(query_count).fetchone()[0]        
        #return {"start":res_order, "end":res_order+res_count-1}              
        return res_order
    
    def Get(self, dbTime, lap, category_id = None):
        
        if(self.datastore.Get("additinal_info") == False):            
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
                           
            if(self.datastore.Get('rfid') == True):                
                query_order = \
                "SELECT count(*) FROM (" +\
                    " SELECT COUNT(times.id) FROM times" +\
                    " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                    " INNER JOIN users ON tags.user_nr = users.nr "+\
                    " WHERE (times.time < " + str(dbTime['time']) + ")"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                    " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                    " GROUP BY user_id"+\
                    " HAVING count(*) >= "+str(lap)+\
                ")"
                    
            else:
                query_order = \
                "SELECT count(*) FROM (" +\
                    " SELECT COUNT(times.id) FROM times" +\
                    " INNER JOIN users ON times.user_id = users.id"+\
                    " WHERE (times.time <= " + str(dbTime['time']) + ")"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                    " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (users.category_id=\"" +str(category_id)+ "\")"+\
                    " GROUP BY user_id"+\
                    " HAVING count(*) >= "+str(lap)+\
                ")"                   
                        
                                                                                          
        
        else:                    
            '''ORDER IN ALL RUN'''
            
            query_order = \
                "SELECT count(*) FROM (" +\
                    " SELECT COUNT(times.id) FROM times" +\
                    " WHERE (times.time <= " + str(dbTime['time']) + ")"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"+\
                    " AND (times.user_id != " +str(dbTime['user_id'])+ ")"+\
                    " AND (times.time != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " GROUP BY user_id"+\
                    " HAVING count(*) >= "+str(lap)+\
                ")"
                
        #print "new count:", query_order                     
                                                       
        try:
            res_order = self.db.query(query_order).fetchone()[0]
            res_order = res_order + 1        
        except:
            res_order = None                            

        return res_order                 

    
class TimesLap():
    def __init__(self, db, datastore):                          
        self.db = db
        self.datastore = datastore
        
    def Get(self, dbTime):        
        
        if(self.datastore.Get("additinal_info") == False):
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
                    " WHERE (times.run_id ==" + str(dbTime['run_id'])+ ")"+\
                    " AND (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"+\
                    " AND (times.time_raw <" + str(dbTime['time_raw']) + ")"+\
                    " AND (times.cell != 1)"
     
                    
        count = self.db.query(query).fetchone()[0]+1
        return count
    

                    
        
        
