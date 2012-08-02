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
import libs.html.htmltags as htmltags
import libs.html.html as html
import libs.utils.utils as utils
import libs.conf.conf as conf
import ewitis.comm.callback as callback
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS
import libs.datastore.datastore as datastore
import ewitis.data.DEF_DATA as DEF_DATA
from threading import Thread

#COMM Shared Memory
DEFAULT_COMM_SHARED_MEMORY = { 
                              "enable" : False,
                              "port": "COM5",
                              "baudrate": 38400                              
}

#CMD_SET_BACKLIGHT       =   0x10
#CMD_GET_RUN_PAR_INDEX   =   0x30
#CMD_GET_TIME_PAR_INDEX  =   0x32


class ManageComm(Thread):
    #def __init__(self, conf_file="ewitis.conf", ShaMem_comm = DEFAULT_COMM_SHARED_MEMORY):        
    def __init__(self, dstore):
        """ INIT VALUES """
        
        Thread.__init__(self)        
        self.datastore = dstore                
        self.index_runs = 0
        self.index_times = 0
        self.order = 0                 
                                                        
        ''' LOAD USER CONFIGURATION - port, baudrate '''            
        #USER_CONF = conf.load(self.conf_file, {"port": "COM8", "baudrate": 38400})
        
        
        ''' CONNECT TO EWITIS '''                
        self.protokol = serialprotocol.SerialProtocol( callback.callback, port=self.datastore.Get("port_name", "GET_SET"), baudrate=self.datastore.Get("port_baudrate", "GET_SET"))
        #print self.datastore.Get("port_name", "GET_SET")
        print "COMM: zakladam instanci.."                        
        
    def __del__(self):
        print "COMM: mazu instanci.."
        
    def stop(self):
        self.protokol.close_port()
        print "COMM: koncim vlakno.."
        
    def send_receive_frame(self, command, string_data=""):
        """ ošetřená vysílací, přijímací metoda """
        try:                                               
            return self.protokol.send_receive_frame(command, string_data)                                                                             
        except (serialprotocol.SendReceiveError) as (errno, strerror):
            print "E:SendReceiveError - {1}({0})".format(errno, strerror)
            return {"error":0xFF} 
            #continue
        except (serial.SerialException) as (strerror):
            print "E:SendReceiveError - {0}()".format(strerror)
            return {"error":0xFF} 
                                                            
    def run(self):  
        #import sqlite3
        import pysqlite2      
        print "COMM: zakladam vlakno.."
#        if(self.datastore.Get("port_enable", "GET_SET") == False):        
#            print "COMM: okamzite koncim vlakno.."
#            return
        
        
        ''' CONNECT TO EWITIS '''        
        try:
            self.protokol.open_port()
        except serial.SerialException:
            print "E: Cant open port"
            self.datastore.Set("port_enable", False)                        
            return            
            #raise serial.SerialException
        
        
        """ DATABASE """        
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")
        
            '''connect to db'''  
            self.db.connect()
        except:
            self.datastore.Set("port_enable", False)
            print "E: Database"
        
        
        """communication established"""
        self.datastore.Set("port_enable", True)
            
        #query = sql_queries.get_query_times_par_id(152)
        #res = self.db.query(query)
        #for item in res:
        #    print item 
        cnt = 0                                                                                   
        while(1):
                                  
            #wait 1 second, test if thread should be terminated
            for i in range(20): 
                
                #              
                time.sleep(0.01)
                
                #terminate thread?                                 
                if(self.datastore.Get("port_enable", "GET_SET") == False):
                    self.stop()                                       
                    return
            #print self.datastore.Get("port_enable", "GET_SET")                
            
            #print "COMM: ",self.ShaMem_comm["enable"]                                 
            
            """
            DATABASE PART
            
             - get new time
             - get new run
             - store new time to the databasae
             - store new run to the databasae
            """
            
            """ GET NEW TIME """                              
            aux_time = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["GET"]["time_par_index"], struct.pack('h',self.index_times))            
            #aux_time['order'] = self.order
                        
            
            """ GET NEW RUN """
            aux_run = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["GET"]["run_par_index"], struct.pack('h',self.index_runs))          
                                    
            
            """ STORE NEW TIME TO THE DATABASE """                                                            
            if(aux_time['error'] == 0):
                                    
                '''update CSV file'''                                
                aux_csv_string = str(aux_time['id']) + ";" + hex(aux_time['user_id']) + ";" + str(aux_time['run_id']) + ";" + str(aux_time['time']).replace(',', '.')
                                
                print "I:Comm: receive time: "+aux_csv_string
                #print struct.pack('<I', aux_time['user_id']).encode('hex')
                                
                '''save to database'''
                #keys = ["state","id", "run_id", "user_id", "cell", "time_raw", "time"]
                #values = [aux_time['state'], aux_time['id'],aux_time['run_id'], aux_time['user_id'], aux_time['cell'], aux_time['time_raw'], aux_time['time']]
                keys = ["state","id", "run_id", "user_id", "cell", "time_raw", "time"]
                values = [aux_time['state'], aux_time['id'],aux_time['run_id'], aux_time['user_id'], aux_time['cell'], aux_time['time_raw'], aux_time['time']]
                import pysqlite2 
                try: 
                    #self.tableTimes.insert_from_lists(keys, values)
                    self.db.insert_from_lists("times", keys, values)
#                except sqlite3.IntegrityError as err:                                
#                    print "I:DB: Time already exist", err
                except pysqlite2.dbapi2.IntegrityError:                                
                    print "I:DB: Time already exist"
                                                                        
                
                '''all for this run has been successfully done, take next'''                   
                self.index_times += 1
                #self.order += 1
                                                
                                                            
            else:
                pass
                #print "I:Comm: no new time"  
                
        
            """ STORE NEW RUN TO THE DATABASE """ 
            #print "error", aux_run              
            if(aux_run['error'] == 0):
                                    
                '''update CSV file'''                   
                aux_csv_string = str(aux_run['id']) + ";" + str(aux_run['name_id']) + ";"
                print "I:Comm: receive run: " + aux_csv_string               
                
                '''save to database'''
                keys = ["state","id", "starttime_id", "date", "name_id"]
                values = [aux_run['state'], aux_run['id'], aux_run['starttime_id'], aux_run['datetime'], aux_run['name_id']] 
                
                try:
                    #self.tableRuns.insert_from_lists(keys, values)
                    self.db.insert_from_lists("runs", keys, values)
#                except sqlite3.IntegrityError:
#                    print "I: DB: run already exist"
                except pysqlite2.dbapi2.IntegrityError:                                
                    print "I:DB: Time already exist"   
                                
                '''all for this run has been successfully done, take next'''   
                self.index_runs += 1
                self.order += 1
                                                
                                                            
            else:
                pass
                #print "I:Comm: no new run"
                
                
            """
            GET&STORE NEW VALUES FROM TERMINAL TO THE DATASTORE            
             - get&store new terminal states
             - get&store new cells states
             - get&store new measure states                        
            """
                        

                                         
            if(self.datastore.Get("active_tab") == 4) or (self.datastore.Get("active_tab") == 5):                                
                """
                SEND REQUESTED COMMANDS TO THE TERMINAL (FROM DATASTORE)            
                 - set new backlight state
                 - set new time
                 - set language                        
                """
                
                """ set backlight """
                if(self.datastore.IsChanged("backlight")):                                
                    data = self.datastore.Get("backlight", "SET")                
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["backlight"], struct.pack('B', data))
                    self.datastore.ResetChangedFlag("backlight")                                   
                
                """ set speaker """
                if(self.datastore.IsChanged("speaker")):
                    print "NASTAVUJI"                                                                             
                    aux_speaker = self.datastore.Get("speaker", "SET")                                
                    aux_data = struct.pack('BBB',int(aux_speaker["keys"]), int(aux_speaker["timing"]), int(aux_speaker["system"]))                                 
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["speaker"], aux_data)
                    self.datastore.ResetChangedFlag("speaker")                
                                            
                """ set language """                                    
                if(self.datastore.IsChanged("language")):
                    data = self.datastore.Get("language", "SET")
                    print "COMM", data                                                                                        
                                                    
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["language"], struct.pack('B', data))
                    self.datastore.ResetChangedFlag("language")                                   
                                
                                                                                    
                """ get terminal-info """                     
                aux_terminal_info = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["GET"]["terminal_info"])                         
                """ store terminal-info to the datastore """ 
                if(self.datastore.IsReadyForRefresh("terminal_info")):           
                    self.datastore.Set("terminal_info", aux_terminal_info, "GET")
                else:
                    print "not ready for refresh", aux_terminal_info               
                
                """ logic mode """
                if(self.datastore.IsChanged("timing_settings")):
                    aux_timing_settings = self.datastore.Get("timing_settings", "SET")                
                    aux_data = struct.pack('<BBBhB', aux_timing_settings['logic_mode'], aux_timing_settings['name_id'], aux_timing_settings['filter_tagtime'],\
                               aux_timing_settings['filter_minlaptime'], aux_timing_settings['filter_maxlapnumber'])                                 
                    #print "COMM2", aux_data.encode('hex')                                                                                        
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["timing_settings"], aux_data)                
                    self.datastore.ResetChangedFlag("timing_settings")  
    
    
                """ generate starttime """
                if(self.datastore.IsChanged("generate_starttime")):                                
                    data = self.datastore.Get("generate_starttime", "SET")                
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["generate_starttime"], struct.pack('B', data))
                    self.datastore.ResetChangedFlag("generate_starttime")
                """ generate finishtime """
                if(self.datastore.IsChanged("generate_finishtime")):                                
                    data = self.datastore.Get("generate_finishtime", "SET")                
                    ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["generate_finishtime"], struct.pack('B', data))
                    self.datastore.ResetChangedFlag("generate_finishtime")    
                                    
                """ get timing-settings """            
                aux_timing_setting = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["GET"]["timing_settings"])
                aux_timing_setting["name_id"] = 4
                
                #print aux_timing_setting            
                """ store terminal-states to the datastore """ 
                if(self.datastore.IsReadyForRefresh("timing_settings")):           
                    self.datastore.Set("timing_settings", aux_timing_setting, "GET")
                else:
                    print "not ready for refresh", aux_timing_setting   
                                                                          
                

            #print cnt, aux_terminal_states['speaker']['keys']            
                
            """ set time """
            #if(self.datastore.isRequested("time", "SET", "changed")):
            #    data = self.datastore.Get("time", "SET")
            # 53 11 12 0c 30 31 303130313031303135305 
            #print "AA",hex(0x010101010150), type(hex(0x010101010150))
#            aa = "313233".decode('hex')
#            print aa.encode('hex')
#            
#            print "d"
            #53 11 12 0e 30 78 31 303130313031303135304c6e
            
            
#            print "010101č01010113"
#            print str(01010101010113)
#            print hex(1010101010113)                  
#            ret = self.send_receive_frame(18, 01010101010113.decode('hex'))
#            print "R2:",ret
            
            
#                
#            """ set language """
#            if(self.datastore.isRequested("language", "SET", "changed")):
#                ret = self.send_receive_frame(COMMANDS["SET"]["language"], struct.pack('B', self.datastore.get("language", "SET")))


                
            
    def port_open(self):
        self.flags['port_open'] = 1
    def port_close(self):
        self.flags['port_open'] = 0
                
if __name__ == "__main__":    
    print "main manage_com()"
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            