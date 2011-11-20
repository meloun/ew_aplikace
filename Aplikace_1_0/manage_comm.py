# -*- coding: utf-8 -*-
'''
Created on 10.06.2010
@author: Lubos Melichar
'''

import serial
import time
import struct
import libs.dicts.dicts as dicts
import libs.file.file as file
import libs.db.db_json as db
import libs.comm.serialprotocol as serialprotocol
import libs.sqlite.sqlite as sqlite
import ewitis.sql_queries.sql_queries as sql_queries
import libs.html.htmltags as htmltags
import libs.html.html as html
import libs.utils.utils as utils
import libs.conf.conf as conf
import ewitis.comm.ew_comm as ew_comm
from threading import Thread


#COMM Shared Memory
DEFAULT_COMM_SHARED_MEMORY = { 
                              "enable" : False,
                              "port": "COM5",
                              "baudrate": 38400                              
}

class ManageComm(Thread):
    def __init__(self, conf_file="ewitis.conf", ShaMem_comm = DEFAULT_COMM_SHARED_MEMORY):
        #=======================================================================
        # INIT VALUES
        #=======================================================================
        Thread.__init__(self)
        self.ShaMem_comm = ShaMem_comm
        self.conf_file = conf_file
        self.index_runs = 0
        self.index_times = 0
        self.order = 0 
        print "COMM: ", self.ShaMem_comm               
                
                                    
        #===========================================================================
        # LOAD USER CONFIGURATION - port, baudrate
        #===========================================================================    
        #USER_CONF = conf.load(self.conf_file, {"port": "COM8", "baudrate": 38400})
        
        #===========================================================================
        # CONNECT TO EWITIS
        #===========================================================================
        #self.protokol = serialprotocol.SerialProtocol( ew_comm.callback, port=USER_CONF['port'], baudrate=USER_CONF['baudrate'])
        self.protokol = serialprotocol.SerialProtocol( ew_comm.callback, port=self.ShaMem_comm["port"], baudrate=self.ShaMem_comm["baudrate"])
        print "COMM: zakladam instanci.."                        
        
    def __del__(self):
        print "COMM: mazu instanci.."
        
    def stop(self):
        self.protokol.close_port()
        print "COMM: koncim vlakno.."
                                                            
    def run(self):  
        import sqlite3      
        print "COMM: zakladam vlakno.."
        if(self.ShaMem_comm["enable"] == False):
            print "COMM: okamzite koncim vlakno.."
            return
        
        #===========================================================================
        # CONNECT TO EWITIS
        #===========================================================================
        try:
            self.protokol.open_port()
        except serial.SerialException:
            print "E: Cant open port"
            self.ShaMem_comm["enable"] = False
            print self.ShaMem_comm
            return            
            #raise serial.SerialException
        
        #=======================================================================
        # DATABASE
        #=======================================================================
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")
            #self.tableTimes = sqlite.sqlite_table(self.db, "times")
            #self.tableRuns = sqlite.sqlite_table(self.db, "runs")
        
            '''connect to db'''  
            self.db.connect()
        except:
            print "E: Database"
            
        #query = sql_queries.get_query_times_par_id(152)
        #res = self.db.query(query)
        #for item in res:
        #    print item 
                                                                                           
        while(1):
                                  
            #wait 1 second, test if thread should be terminated
            for i in range(100): 
                
                #              
                time.sleep(0.01)
                
                #terminate thread?                 
                if(self.ShaMem_comm["enable"] == False):
                    self.stop()                    
                    return                
            
            #print "COMM: ",self.ShaMem_comm["enable"] 
                       
            #===================================================================
            # GET NEW TIME           
            #===================================================================
            try:                                               
                aux_time = self.protokol.send_receive_frame(ew_comm.CMD_GET_TIME_PAR_INDEX, struct.pack('h',self.index_times))
                aux_time['order'] = self.order                                                                 
            except (serialprotocol.SendReceiveError) as (errno, strerror):
                print "E:SendReceiveError - {1}({0})".format(errno, strerror) 
                continue
            except (serial.SerialException) as (strerror):
                print "E:SendReceiveError - {0}()".format(strerror)
            
            #===================================================================
            # GET NEW RUN       
            #===================================================================
            try:                                               
                aux_run = self.protokol.send_receive_frame(ew_comm.CMD_GET_RUN_PAR_INDEX, struct.pack('h',self.index_runs))
                #aux_run['order'] = self.order
                #print aux_run                                                 
            except (serialprotocol.SendReceiveError) as (errno, strerror):
                print "E:SendReceiveError - {1}({0})".format(errno, strerror) 
                continue
            except (serial.SerialException) as (strerror):
                print "E:SendReceiveError - {0}()".format(strerror)
                                    
            #===============================================================
            # NEW TIME                            
            #===============================================================                        
            if(aux_time['error'] == 0):
                                    
                '''update CSV file'''                                
                aux_csv_string = str(aux_time['id']) + ";" + str(aux_time['run_id']) + ";" + str(aux_time['time']).replace(',', '.')
                print "I: Comm: receive time: "+aux_csv_string
                                
                '''save to database'''
                keys = ["state","id", "run_id", "user_id", "cell", "time_raw", "time"]
                values = [aux_time['state'], aux_time['id'],aux_time['run_id'], aux_time['user_id'], aux_time['cell'], aux_time['time_raw'], aux_time['time']]
                
                try: 
                    #self.tableTimes.insert_from_lists(keys, values)
                    self.db.insert_from_lists("times", keys, values)
                except sqlite3.IntegrityError:
                    print "I: DB: Time already exist"                                                    
                
                '''all for this run has been successfully done, take next'''                   
                self.index_times += 1
                self.order += 1
                                                
                                                            
            else:
                print "I:Comm: no new time"  
                
        
            #===============================================================
            # NEW RUN                            
            #===============================================================                        
            if(aux_run['error'] == 0):
                                    
                '''update CSV file'''                   
                aux_csv_string = str(aux_run['id']) + ";" + str(aux_run['name_id']) + ";"
                print "I: Comm: receive run: " + aux_csv_string               
                
                '''save to database'''
                keys = ["state","id", "starttime_id", "date", "name_id"]
                values = [aux_run['state'], aux_run['id'], aux_run['starttime_id'], aux_run['datetime'], aux_run['name_id']] 
                
                try:
                    #self.tableRuns.insert_from_lists(keys, values)
                    self.db.insert_from_lists("runs", keys, values)
                except sqlite3.IntegrityError:
                    print "I: DB: run already exist"   
                                
                '''all for this run has been successfully done, take next'''   
                self.index_runs += 1
                self.order += 1
                                                
                                                            
            else:
                print "I:Comm: no new run"  
            
    def port_open(self):
        self.flags['port_open'] = 1
    def port_close(self):
        self.flags['port_open'] = 0
                
if __name__ == "__main__":    
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            