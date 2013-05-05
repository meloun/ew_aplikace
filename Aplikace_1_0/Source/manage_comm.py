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
from ewitis.data.DEF_ENUM_STRINGS import * 
import libs.datastore.datastore as datastore
import ewitis.data.DEF_DATA as DEF_DATA
from threading import Thread

#COMM Shared Memory
DEFAULT_COMM_SHARED_MEMORY = { 
                              "enable" : False,
                              "port": "COM5",
                              "baudrate": 38400                              
}


class ManageComm(Thread):            
    def __init__(self, dstore):
        """ INIT VALUES """
        
        Thread.__init__(self)        
        self.datastore = dstore
        
        #set start download indexes
        self.index_runs = 0
        self.index_times = 0
        if(self.datastore.Get("download_from_last") == 2):      
            if(self.datastore.Get("count")['Runs'] - 1) > 0:          
                self.index_runs = self.datastore.Get("count")['Runs'] - 1
            if(self.datastore.Get("count")['Times'] - 1) > 0:
                self.index_times = self.datastore.Get("count")['Times'] - 1        
                                                                                      
                                                        
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
        
    def send_receive_frame(self, command_key, data="", length = None):
        """ ošetřená vysílací, přijímací metoda """
        
        command = DEF_COMMANDS.DEF_COMMANDS[command_key]['cmd']
        length = DEF_COMMANDS.DEF_COMMANDS[command_key]['length']
        
        #pack data (to string)
        if(length == 1):
            data = struct.pack('B', data)
        elif(length == 2):
            data = struct.pack('H', data)
        elif(length == 4):
            data = struct.pack('L', data)
                      
                      
        try:                                               
            return self.protokol.send_receive_frame(command, data)                                                                             
        except (serialprotocol.SendReceiveError) as (errno, strerror):
            print "E:SendReceiveError - {1}({0})".format(errno, strerror)
            return {"error":0xFF} 
            #continue
        except (serial.SerialException) as (strerror):
            print "E:SendReceiveError - {0}()".format(strerror)
            return {"error":0xFF} 
                                                            
    def run(self):  
        import pysqlite2      
        print "COMM: zakladam vlakno.."       
        
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
            
                                                                                    
        while(1):
                                  
            #wait 1 second, test if thread should be terminated
            for i in range(20): 
                
                #              
                time.sleep(0.01)
                
                #terminate thread?                                 
                if(self.datastore.Get("port_enable", "GET_SET") == False):
                    self.stop()                                       
                    return
                            
                                         
            #communication enabled?
            if(self.datastore.Get("communication_en", "GET_SET") == False):                
                continue
                
            """
            DATABASE PART
            
             - get new time
             - get new run
             - store new time to the databasae
             - store new run to the databasae
            """
            
            """ GET NEW TIME """                                                      
            aux_time = self.send_receive_frame("GET_TIME_PAR_INDEX", self.index_times)                                                
            
            """ GET NEW RUN """                                                                                   
            aux_run = self.send_receive_frame("GET_RUN_PAR_INDEX", self.index_runs)          
            
            
            
            """ STORE NEW TIME TO THE DATABASE """
            #print "aux_time['error']: ",aux_time['error'], type(aux_time['error'])
            if(aux_time['error'] == 0 or aux_run['error'] == 0):
                print"================="
                                                                             
            if(aux_time['error'] == 0):
                                    
                '''update CSV file'''                                
                aux_csv_string = str(aux_time['id']) + ";" + hex(aux_time['user_id'])+ ";" + str(aux_time['cell']) + ";" + str(aux_time['run_id']) + ";" + str(aux_time['time_raw']).replace(',', '.')
                                
                print "I: Comm: receive time:",self.index_times, ":", aux_csv_string
                #print struct.pack('<I', aux_time['user_id']).encode('hex')
                                
                '''save to database'''                                
                keys = ["state","id", "run_id", "user_id", "cell", "time_raw", "time"]
                values = [aux_time['state'], aux_time['id'],aux_time['run_id'], aux_time['user_id'], aux_time['cell'], aux_time['time_raw'], aux_time['time']]
                import pysqlite2 
                try: 
                    #self.tableTimes.insert_from_lists(keys, values)
                    self.db.insert_from_lists("times", keys, values)
#                except sqlite3.IntegrityError as err:                                
#                    print "I:DB: Time already exist", err
                except pysqlite2.dbapi2.IntegrityError:                                
                    print "I: DB: time already exists"
                                                                        
                
                '''all for this run has been successfully done, take next'''                   
                self.index_times += 1                                                                
                                                            
            else:
                pass
                #print "I:Comm: no new time"  
                
        
            """ STORE NEW RUN TO THE DATABASE """ 
            #print "error", aux_run              
            if(aux_run['error'] == 0):
                                    
                '''update CSV file'''                   
                aux_csv_string = str(aux_run['id']) + ";" + str(aux_run['name_id']) + ";"
                print "I: Comm: receive run: ", self.index_runs, ":", aux_csv_string               
                
                '''save to database'''
                keys = ["state","id", "starttime_id", "date", "name_id"]
                values = [aux_run['state'], aux_run['id'], aux_run['starttime_id'], aux_run['datetime'], aux_run['name_id']] 
                
                try:
                    #self.tableRuns.insert_from_lists(keys, values)
                    self.db.insert_from_lists("runs", keys, values)
#                except sqlite3.IntegrityError:
#                    print "I: DB: run already exist"
                except pysqlite2.dbapi2.IntegrityError:                                
                    print "I: DB: run already exists"   
                                
                '''all for this run has been successfully done, take next'''   
                self.index_runs += 1                                                                
                                                            
            else:
                pass
                #print "I:Comm: no new run"
                
                
            """
            GET&STORE NEW VALUES FROM TERMINAL TO THE DATASTORE            
             - get&store new terminal states
             - get&store new cells states
             - get&store new measure states                        
            """
            
            """ enable start-cell """                
            if(self.datastore.IsChanged("enable_startcell")):                                        
                user_id = self.datastore.Get("enable_startcell", "SET")                
                ret = self.send_receive_frame("ENABLE_START_CELL")
                self.datastore.ResetChangedFlag("enable_startcell")
                
            """ enable finish-cell """                
            if(self.datastore.IsChanged("enable_finishcell")):                        
                user_id = self.datastore.Get("enable_finishcell", "SET")                
                ret = self.send_receive_frame("ENABLE_FINISH_CELL")
                self.datastore.ResetChangedFlag("enable_finishcell")
                                    
            """ generate starttime """                
            if(self.datastore.IsChanged("generate_starttime")):                                        
                user_id = self.datastore.Get("generate_starttime", "SET")                
                ret = self.send_receive_frame("GENERATE_STARTTIME", user_id)
                self.datastore.ResetChangedFlag("generate_starttime")
                
            """ generate finishtime """
            if(self.datastore.IsChanged("generate_finishtime")):                                
                user_id = self.datastore.Get("generate_finishtime", "SET")                
                ret = self.send_receive_frame("GENERATE_FINISHTIME", user_id)
                self.datastore.ResetChangedFlag("generate_finishtime")
                    
            """ quit timing """
            if(self.datastore.IsChanged("quit_timing")):                                                                                     
                ret = self.send_receive_frame("QUIT_TIMING")
                self.datastore.ResetChangedFlag("quit_timing")
                
            """ clear database """
            if(self.datastore.IsChanged("clear_database")):                                                                                     
                ret = self.send_receive_frame("CLEAR_DATABASE")
                self.datastore.ResetChangedFlag("clear_database")
                print "I: Comm: clearing database, please wait.. "
                time.sleep(19)
                print "I: Comm: database should be empty now"
                
            """ enable/disable tags reading """
            if(self.datastore.IsChanged("tags_reading")):         
                on_off = self.datastore.Get("tags_reading", "SET")                                                                                               
                ret = self.send_receive_frame("SET_TAGS_READING", on_off)
                self.datastore.ResetChangedFlag("tags_reading")
                if(on_off):
                    print "I: Comm: Enable tags reading"
                else:
                    print "I: Comm: Disable tags reading"
                
                                                     
            if(self.datastore.Get("active_tab") == TAB.race_settings) or (self.datastore.Get("active_tab") == TAB.actions)\
                or (self.datastore.Get("active_tab") == TAB.device):                                
                """
                SEND REQUESTED COMMANDS TO THE TERMINAL (FROM DATASTORE)            
                 - set new backlight state
                 - set new time
                 - set language                        
                """
                
                """ set backlight """
                if(self.datastore.IsChanged("backlight")):                                
                    data = self.datastore.Get("backlight", "SET")                
                    #ret = self.send_receive_frame(DEF_COMMANDS.DEF_COMMANDS["SET"]["backlight"], struct.pack('B', data))
                    ret = self.send_receive_frame("SET_BACKLIGHT", data)
                    self.datastore.ResetChangedFlag("backlight")                                   
                
                """ set speaker """
                if(self.datastore.IsChanged("speaker")):
                    print "NASTAVUJI"                                                                             
                    aux_speaker = self.datastore.Get("speaker", "SET")                                
                    aux_data = struct.pack('BBB',int(aux_speaker["keys"]), int(aux_speaker["timing"]), int(aux_speaker["system"]))                                                     
                    ret = self.send_receive_frame("SET_SPEAKER", aux_data)
                    self.datastore.ResetChangedFlag("speaker")                
                                            
                """ set language """                                    
                if(self.datastore.IsChanged("language")):
                    data = self.datastore.Get("language", "SET")
                    print "COMM", data                                                                                        
                                                                        
                    ret = self.send_receive_frame("SET_LANGUAGE", data)                    
                    self.datastore.ResetChangedFlag("language")                                   
                                
                                                                                    
                """ get terminal-info """                     
                aux_terminal_info = self.send_receive_frame("GET_TERMINAL_INFO")                         
                """ store terminal-info to the datastore """
                if not('error' in aux_terminal_info): 
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
                    ret = self.send_receive_frame("SET_TIMING_SETTINGS", aux_data)                
                    self.datastore.ResetChangedFlag("timing_settings")  
        
                                    
            """ get timing-settings """            
            aux_timing_setting = self.send_receive_frame("GET_TIMING_SETTINGS")
            aux_timing_setting["name_id"] = 4
            
            #print aux_timing_setting            
            """ store terminal-states to the datastore """ 
            if not('error' in aux_timing_setting):
                if(self.datastore.IsReadyForRefresh("timing_settings")):            
                    self.datastore.Set("timing_settings", aux_timing_setting, "GET")
                else:
                    print "not ready for refresh", aux_timing_setting   
                                                                                  

                

                
if __name__ == "__main__":    
    print "main manage_com()"
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            