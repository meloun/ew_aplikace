# -*- coding: utf-8 -*-
class TimesUtils():
    def __init__(self, TimesModel):
        self.TimesModel = TimesModel
        
        #predelat, tohle pres self.times.name atd.
        self.name = TimesModel.params.name
        self.db = TimesModel.params.db                                       
        
    #time_raw => time
    @staticmethod
    def timeraw2timestring(timeraw, starttimeraw):
        
        if (timeraw == None) or (starttimeraw == None):
            return None
                
        '''decrement start-time'''
        time = timeraw - starttimeraw
        
        '''convert'''
        hours = time / (100*60*60)
        
        time = time % (100*60*60)
        minutes = time / (100*60)
        
        time = time % (100*60)
        seconds = time / (100)
        
        milliseconds = time % (100)
        
        return '%02d:%02d:%02d,%02d' %(hours, minutes, seconds, milliseconds)
        
        
    @staticmethod 
    def timestring2timeraw(timestring, starttimeraw):       
        
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
        
        '''increment starttime'''
        if starttimeraw:             
            timeraw = time + starttimeraw
        else:
            timeraw = time
                   
        return timeraw
    
    
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

    def Get(self, dbTime, category = None):
        if(dbTime['time_raw'] == None):
            return None
              
        if(dbTime['time_raw'] == 0):
            return None
            
        if(dbTime['cell'] == 1):            
            return None
        
        if category != None:     
            
            '''ORDER IN THE SAME CATEGORY'''        
                           
            if(self.datastore.Get('rfid') == True):                
                query_order = \
                    " SELECT COUNT(*) FROM times" +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw < " +str(dbTime['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +(category)+ "\")"+\
                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
                query_count = \
                    " SELECT COUNT(*) FROM times" +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw = " +str(dbTime['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +(category)+ "\")"+\
                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
            else:
                query_order = \
                    " SELECT COUNT(*) FROM times" +\
                        " INNER JOIN users ON times.user_id = users.id"+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw < " +str(dbTime['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +(category)+ "\")"+\
                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
                query_count = \
                    " SELECT COUNT(*) FROM times" +\
                        " INNER JOIN users ON times.user_id = users.id "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw = " +str(dbTime['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +(category)+ "\")"+\
                        " AND (times.run_id=\"" +str(dbTime['run_id'])+ "\")"
        
        else:
            
            '''ORDER IN ALL RUN'''
            
            query_order = "\
                SELECT COUNT(*) FROM times" +\
                    " WHERE (times.time_raw<" + str(dbTime['time_raw']) + ")"+\
                    " AND (times.time_raw != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
            query_count = "\
                SELECT COUNT(*) FROM times" +\
                    " WHERE (times.time_raw=" + str(dbTime['time_raw']) + ")"+\
                    " AND (times.time_raw != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (times.run_id=\""+str(dbTime['run_id'])+"\")"
                               
                     
        res_order = self.db.query(query_order).fetchone()[0]+1        
        res_count = self.db.query(query_count).fetchone()[0]
        
        #return {"start":res_order, "end":res_order+res_count-1}              
        return res_order                   

    
class TimesLap():
    def __init__(self, db):                          
        self.db = db
        
    def Get(self, dbTime):        
        
        if(dbTime['time_raw'] == None):
            return None;

        if(dbTime['cell'] == 1):
            return None
                    
        if(dbTime['time_raw'] == 0):
            return None

        '''v čase může být user_id pro které neexistuje uživatel => lap =0'''        
        #if(self.TimesModel.params.tabUser.getDbUserParIdOrTagId(time["user_id"]) == None):           
        #    return 0 
        
        '''count of times - same race, same user, better time, exclude start time'''
        query = "\
                SELECT COUNT(*) FROM times" +\
                    " WHERE (times.run_id ==" + str(dbTime['run_id'])+ ")"+\
                    " AND (times.user_id ==\"" + str(dbTime['user_id'] )+"\")"+\
                    " AND (times.time_raw <" + str(dbTime['time_raw']) + ")"+\
                    " AND (times.cell != 1)"
     
                    
        count = self.db.query(query).fetchone()[0]+1
        return count
    

                    
        
        
