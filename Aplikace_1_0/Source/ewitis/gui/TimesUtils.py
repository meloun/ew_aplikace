# -*- coding: utf-8 -*-

class ZeroRawTime_Error(Exception): pass
class NoneRawTime_Error(Exception): pass
class WrongCell_Error(Exception): pass
class TimeFormat_Error(Exception): pass


class TimesUtils():
    def __init__(self, TimesModel):
        self.TimesModel = TimesModel
        
        #predelat, tohle pres self.times.name atd.
        self.name = TimesModel.params.name
        self.db = TimesModel.params.db        
                
        #update start times
        self.updateStartTimes()                 
        
    #time_raw => time
    @staticmethod
    def timeraw2time(time):
        hours = time / (100*60*60)
        
        time = time % (100*60*60)
        minutes = time / (100*60)
        
        time = time % (100*60)
        seconds = time / (100)
        
        milliseconds = time % (100)
        
        return '%02d:%02d:%02d,%02d' %(hours, minutes, seconds, milliseconds)
    
    # time => time_raw
    # "01:02:35,42" => (01*60*60 + 02*60 +35)*100 + 42
    @staticmethod 
    def time2timeraw(time):        
        
        #split to hours(01), minutes(02) and seconds(35,42)
        time = time.split(":")                                         
        if (len(time)) != 3 : #check: 2x colon?
            raise TimeFormat_Error
    
        #get seconds
        time_seconds = time[2].split(",")
        if (len(time_seconds)) != 2 : #check: 1x point?                 
            raise TimeFormat_Error
        
        try:
            hours = int(time[0])
            minutes = int(time[1])
            seconds = int(time_seconds[0])
            tens_ms = int(time_seconds[1])
        except:
            raise TimeFormat_Error
        
        if (hours > 59) or (minutes > 59) or (seconds > 59):
            raise TimeFormat_Error                 
        
        time_raw = ((hours*60*60)+(minutes*60) + seconds)*100 + tens_ms       
        return time_raw
    
    #restrict time(+starttime), different starts    
    def tabtime2dbtime(self, run_id, tabTime):                
        
        dbtime = self.time2timeraw(tabTime['time'])
                       
        #get starttime number        
        if(tabTime['cell'] == 1): #start time?                           
            starttime_nr = 1 #decrement 1.starttime        
        else:
            category = self.TimesModel.params.tabCategories.getTabCategoryParName(tabTime['category'])
            starttime_nr = category['start_nr']                                                                
        try:
            start_times = self.start_times[run_id]
        
            #incement start time        
            if(starttime_nr):
                dbtime = dbtime + start_times[int(starttime_nr)-1]['time_raw']
        except:
            print "I: tabtime2dbtime: no increment start time"
        
        return dbtime 
        
        
    
    #restrict time(-starttime), different starts    
    def dbtime2tabtime(self, run_id, dbTime, start_nr): #timeraw, start_nr):                           
                  
        #get rawtime
        aux_rawtime = dbTime['time_raw']

        #get start times for this run
        try:                       
            start_times = self.start_times[run_id]
        except:                         
            print "E:neexistuje startime"
            return        

        #TRAINING MODE
        #toDo: rozlisit podle modu z datastore
        #if(self.guidata.measure_setting == GuiData.TRAINING_STANDART):                
#            #find before-starttime
#            previous_starttime = self.get_previous_time(start_times, dbTime['id'])
#            #print aux_rawtime,"-",previous_starttime['time_raw']
#            aux_rawtime = aux_rawtime - previous_starttime['time_raw']
        #RACE MODE
        
        #else:
        #decrement start time (if exist start_nr)        
        if start_nr and start_times:
            try:                                               
                aux_rawtime = aux_rawtime - start_times[start_nr-1]['time_raw']
            except:
                print "e: dbtime2tabtime"
                return None

        #convert to table format                                          
        return self.timeraw2time(aux_rawtime)
    
    #get previous time (from times(list) => time['id'] < time_id ) 
    def get_previous_time(self, times, time_id):
        aux_time = {'id':0, 'time_raw': 0}
        
        for time in times:
            if (time['id'] < time_id) and (time['id'] > aux_time['id']):
                aux_time = time                
                
        return aux_time
                
    
    #getStartTimer - return all start times of 
    def updateStartTimes(self):
        
        #
        query = \
                " SELECT * FROM " + self.name +\
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
        
          
    def getFirstStartTime(self, run_id):
        return self.start_times[run_id][0]
    
    def getStartTime(self, run_id, nr):             
        return self.start_times[run_id][nr-1]
              
                                                                                                                                                  
        
        
    #getOrder - return order and count of same time !in run! (in category)
    #errors 
        # NoneRawTime_Error
        # ZeroRawTime_Error 
    def getOrder(self, time, incategory = False):
        
        if(time['time_raw'] == None):
            raise NoneRawTime_Error;
            
        if(time['time_raw'] == 0):
            raise ZeroRawTime_Error
            
        if(time['cell'] == 1):
            raise WrongCell_Error 
        
        #ORDER IN THE SAME CATEGORY
        #toDo: str(time['category']) chyba pri vygenerovani exe
        if incategory == True:     
                   

            if(self.TimesModel.params.datastore.Get('rfid')):                
                query_order = \
                    " SELECT COUNT(*) FROM " + self.name +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw < " +str(time['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +((time['category']))+ "\")"+\
                        " AND (times.run_id=\"" +str(time['run_id'])+ "\")"
                query_count = \
                    " SELECT COUNT(*) FROM " + self.name +\
                        " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                        " INNER JOIN users ON tags.user_nr = users.nr "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw = " +str(time['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +((time['category']))+ "\")"+\
                        " AND (times.run_id=\"" +str(time['run_id'])+ "\")"
            else:
                query_order = \
                    " SELECT COUNT(*) FROM " + self.name +\
                        " INNER JOIN users ON times.user_id = users.id"+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw < " +str(time['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +((time['category']))+ "\")"+\
                        " AND (times.run_id=\"" +str(time['run_id'])+ "\")"
                query_count = \
                    " SELECT COUNT(*) FROM " + self.name +\
                        " INNER JOIN users ON times.user_id = users.id "+\
                        " INNER JOIN categories ON users.category_id = categories.id "+\
                        " WHERE (times.time_raw = " +str(time['time_raw'])+ ")"+\
                        " AND (times.time_raw != 0 )"+\
                        " AND (times.cell != 1 )"+\
                        " AND (categories.name=\"" +((time['category']))+ "\")"+\
                        " AND (times.run_id=\"" +str(time['run_id'])+ "\")"

        #ORDER IN ALL RUN
        else:
            query_order = "\
                SELECT COUNT(*) FROM " + self.name +\
                    " WHERE (times.time_raw<" + str(time['time_raw']) + ")"+\
                    " AND (times.time_raw != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (times.run_id=\""+str(time['run_id'])+"\")"
            query_count = "\
                SELECT COUNT(*) FROM " + self.name +\
                    " WHERE (times.time_raw=" + str(time['time_raw']) + ")"+\
                    " AND (times.time_raw != 0 )"+\
                    " AND (times.cell != 1 )"+\
                    " AND (times.run_id=\""+str(time['run_id'])+"\")"
                               
                     
        res_order = self.db.query(query_order).fetchone()[0]+1        
        res_count = self.db.query(query_count).fetchone()[0]
                
        return {"start":res_order, "end":res_order+res_count-1}   
    
    #getOrder - return order and count of same time !in run! (in category)
    #errors 
        # NoneRawTime_Error
        # ZeroRawTime_Error 
    def getLap(self, time):
        
        if(time['time_raw'] == None):
            raise NoneRawTime_Error;
            
        if(time['time_raw'] == 0):
            raise ZeroRawTime_Error

        '''v čase může být user_id pro které neexistuje uživatel => lap =0'''        
        if(self.TimesModel.params.tabUser.getDbUserParIdOrTagId(time["user_id"]) == None):           
            return 0 
        
        '''count of times - same race, same user, better time, exclude start time'''
        query = "\
                SELECT COUNT(*) FROM " + self.name +\
                    " WHERE (times.run_id ==" + str(time['run_id'])+ ")"+\
                    " AND (times.user_id ==\"" + str(time['user_id'] )+"\")"+\
                    " AND (times.time_raw <" + str(time['time_raw']) + ")"+\
                    " AND (times.cell != 1)"
     
                    
        count = self.db.query(query).fetchone()[0]+1
        return count
                    
        
        
