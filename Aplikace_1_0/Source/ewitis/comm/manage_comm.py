# -*- coding: utf-8 -*-
'''
Created on 10.06.2010
@author: Lubos Melichar
'''

import serial
import time
import datetime
import struct
import libs.dicts.dicts as dicts
import libs.file.file as file
import libs.db.db_json as db
import libs.comm.serialprotocol as serialprotocol
import libs.sqlite.sqlite as sqlite
import libs.html.htmltags as htmltags
import libs.html.html as html
import libs.utils.utils as utils
import ewitis.comm.callback as callback
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS
from ewitis.data.DEF_ENUM_STRINGS import * 
from threading import Thread

class ManageComm(Thread):            
    def __init__(self, dstore):
        """ INIT VALUES """
        
        Thread.__init__(self)        
        self.datastore = dstore
        
        #set start download indexes
        self.index_runs = 0
        self.index_times = 0
        self.no_new_times = 0
        self.no_new_runs = 0
        if(self.datastore.Get("download_from_last") == 2):      
            if(self.datastore.Get("count")['Runs'] - 1) > 0:          
                self.index_runs = self.datastore.Get("count")['Runs'] - 1
            if(self.datastore.Get("count")['Times'] - 1) > 0:
                self.index_times = self.datastore.Get("count")['Times'] - 1        
                                                                                      
                                                        
        ''' LOAD USER CONFIGURATION - port, baudrate '''            
        #USER_CONF = conf.load(self.conf_file, {"port": "COM8", "baudrate": 38400})
        
        
        ''' CONNECT TO EWITIS '''
        aux_port = self.datastore.Get("port")                
        self.protokol = serialprotocol.SerialProtocol( port = aux_port["name"], baudrate = aux_port["baudrate"])        
        print "COMM: zakladam instanci.."                        
        
    def __del__(self):
        print "COMM: mazu instanci.."
        
    def stop(self):
        self.protokol.close_port()
        print "COMM: koncim vlakno.."
        
    def send_receive_frame(self, command_key, data="", length = None):
        """ ošetřená vysílací, přijímací metoda """                
        if command_key != "GET_HW_SW_VERSION":
            if not((DEF_COMMANDS.DEF_COMMANDS[command_key]['blackbox'] and self.datastore.IsBlackbox()) \
                   or (DEF_COMMANDS.DEF_COMMANDS[command_key]['terminal'] and self.datastore.IsTerminal())):
            
                #this command is not defined for this device
                print "E: command not defined for this device", command_key                                
                return {"error":0xFF}
            
        command = DEF_COMMANDS.DEF_COMMANDS[command_key]['cmd']                                             
                      
        try:
            '''pack data to the string'''
            data = callback.pack_data(command_key, data)            
            '''requet diagnostic'''            
            if(self.datastore.Get("diagnostic")["log_cyclic"] == 2):# or (DEF_COMMANDS.IsCyclic(command_key)== False):                
                self.datastore.AddDiagnostic(command, data, 'green', command_key)
            '''send and receive data'''            
            receivedata = self.protokol.send_receive_frame(command, data)                                                
            '''unpack data to dict structure'''
            data = callback.unpack_data(receivedata['cmd'], receivedata['data'], data)
            '''response diagnostic'''
            if(self.datastore.Get("diagnostic")["log_cyclic"] == 2): #or (DEF_COMMANDS.IsCyclic(command_key)== False):                                    
                self.datastore.AddDiagnostic(receivedata['cmd'], receivedata['data'], 'blue')                                                                              
        except (serialprotocol.SendReceiveError) as (errno, strerror):
            print "E:SendReceiveError - {1}({0})".format(errno, strerror)
            data = {"error":0xFF}
            if(self.datastore.Get("diagnostic")["log_cyclic"] == 2):# or (DEF_COMMANDS.IsCyclic(command_key)== False):
                self.datastore.AddDiagnostic(command, data, 'red', command_key+": SendReceiveError")             
        except (serial.SerialException) as (strerror):            
            print "E:SendReceiveError - {0}()".format(strerror)
            data = {"error":0xFF}
            if(self.datastore.Get("diagnostic")["log_cyclic"] == 2):# or (DEF_COMMANDS.IsCyclic(command_key)== False):
                self.datastore.AddDiagnostic(command, data, 'red', command_key+": SerialException")

 
        return data
                                                            
    def run(self):       
        print "COMM: zakladam vlakno.."       
        
        ''' CONNECT TO EWITIS '''        
        try:
            self.protokol.open_port()
        except serial.SerialException:
            print "E: Cant open port"
            #self.datastore.Set("port_enable", False)                        
            self.datastore.SetItem("port", ["opened"], False)                        
            return            
            #raise serial.SerialException
        
        
        """ DATABASE """        
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")
        
            '''connect to db'''  
            self.db.connect()
        except:
            #self.datastore.Set("port_enable", False)
            self.datastore.SetItem("port", ["opened"], False)
            print "E: Database"
        
        
        """communication established"""
        #self.datastore.Set("port_enable", True)
        self.datastore.SetItem("port", ["opened"], True)
            
                                                                                    
        while(1):
                                  
            #wait X millisecond, test if thread should be terminated
            ztime = time.clock()
            for i in range(10): 
                
                #wait              
                time.sleep(0.01)
                
                #wait longer(for terminal - no info yet)                    
                #time.sleep(0.01)
                
                #terminate thread?                                 
                #if(self.datastore.Get("port_enable", "GET_SET") == False):
                if self.datastore.Get("port")["opened"] == False:
                    self.stop()                                       
                    return
                
            #print "I: Comm: waiting:",time.clock() - ztime,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]                            
                                         
            #communication enabled?
            if(self.datastore.Get("port")["enabled"] == False):                
                continue
                
            """ 
            GET HW-SW-VERSION 
                only once (after start sw,hw = none)
            """            
            if(self.datastore.Get("versions")["hw"] == None) or (self.datastore.Get("versions")["fw"] == None):
                
                aux_version = self.send_receive_frame("GET_HW_SW_VERSION")
                print "version:", aux_version
                                
                if ('error' in aux_version): 
                    print "E: Comm: no Hw and Fw versions on device"                
                    continue #no other commands as long as no version
                
                self.datastore.SetItem("versions", ["hw"], aux_version["hw"])
                self.datastore.SetItem("versions", ["fw"], aux_version["fw"])
            """ end of hw-sw-version """
            
            """ 
            SEND COMMAND 
                diagnostic purpose
            """ 
            if(self.datastore.Get("diagnostic")["sendcommandkey"] != None):
                
                
                print "COMM: sendcommand:", self.datastore.Get("diagnostic")["sendcommandkey"], self.datastore.Get("diagnostic")["senddata"]
                aux_response = self.send_receive_frame(self.datastore.Get("diagnostic")["sendcommandkey"], str(self.datastore.Get("diagnostic")["senddata"]))
                print "COMM: sendcommand response:", aux_response
                                
                if ('error' in aux_version): 
                    print "COMM: sendcommand response: ERROR"                                     
                
                #smazat request
                self.datastore.SetItem("diagnostic", ["sendcommandkey"], None)
                                
                #set response (text to label)
                #self.datastore.SetItem("diagnostic", ["sendresponse"], aux_response)
                                
            
            
            """
            RUNS & TIMES & DATABASE PART
             - get new time
             - get new run
             - store new time to the databasae
             - store new run to the databasae
            """
                        
            """ GET NEW TIME """                                                                  
            aux_time = self.send_receive_frame("GET_TIME_PAR_INDEX", self.index_times)                                                
            
            """ GET NEW RUN """                                                                                   
            aux_run = self.send_receive_frame("GET_RUN_PAR_INDEX", self.index_runs)                      
            
                        
            if(aux_time['error'] == 0 or aux_run['error'] == 0):
                print"================="

            """ GET NEW RUN """           
            aux_diagnostic = self.datastore.Get("diagnostic")                
            if(aux_time['error'] != 0):
                self.datastore.SetItem("diagnostic", ["no_new_time_cnt"], aux_diagnostic["no_new_time_cnt"]+1)
                
            if(aux_run['error'] != 0):
                self.datastore.SetItem("diagnostic", ["no_new_run_cnt"], aux_diagnostic["no_new_run_cnt"]+1)                        
            
            #self.datastore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='red'>no new times (100)</font><br>")
            #self.datastore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='green'>no new times (100)</font><br>")
            #self.datastore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='blue'>no new times (100)</font><br>")
            
                                                                             
                                                                            
                    
            """ STORE NEW TIME TO THE DATABASE """
            if(aux_time['error'] == 0):
                self.AddTimeToDb(aux_time)                                                                                                                           
                self.index_times += 1 # done, take next                                                                             
            else:
                pass # no new time                  
        
            """ STORE NEW RUN TO THE DATABASE """
            if(aux_run['error'] == 0):                       
                self.AddRunToDb(aux_run)                                                                              
                self.index_runs += 1 # done, take next                                                                                                                            
            else:
                pass # no new run
            
            """ end of Run & Times & Database """
                            
                
            """
            ACTIONS            
             - enable/disable startcell
             - enable/disable finishcell
             - generate starttime
             - generate finishtime
             - quit timing                        
             - clear database                        
             - enable/disable tags reading
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
            
            """ end of ACTIONS """
            
            """
            tab RACE SETTINGS & tab ACTIONS & tab DEVICE            
             - set backlight
             - set speaker
             - set language
             - get terminal info
             - set timing settings                                                                          
            """                                                         
            if(self.datastore.Get("active_tab") == TAB.race_settings) or (self.datastore.Get("active_tab") == TAB.actions)\
                or (self.datastore.Get("active_tab") == TAB.device):                                
                
                """ set backlight """
                if(self.datastore.IsChanged("backlight")):                                
                    data = self.datastore.Get("backlight", "SET")                                    
                    ret = self.send_receive_frame("SET_BACKLIGHT", data)
                    self.datastore.ResetChangedFlag("backlight")                                   
                
                """ set speaker """
                if(self.datastore.IsChanged("speaker")):
                    print "NASTAVUJI"                                                                             
                    aux_speaker = self.datastore.Get("speaker", "SET")                                                                                                                              
                    ret = self.send_receive_frame("SET_SPEAKER", aux_speaker)
                    self.datastore.ResetChangedFlag("speaker")                
                                            
                """ set language """                                    
                if(self.datastore.IsChanged("language")):
                    data = self.datastore.Get("language", "SET")                                                                                                                                                                               
                    ret = self.send_receive_frame("SET_LANGUAGE", data)                    
                    self.datastore.ResetChangedFlag("language")                                   
                                
                                                                                    
                """ get terminal-info """                     
                aux_terminal_info = self.send_receive_frame("GET_TERMINAL_INFO")                         
                """ store terminal-info to the datastore """
                if not('error' in aux_terminal_info): 
                    if(self.datastore.IsReadyForRefresh("terminal_info")):           
                        self.datastore.Set("terminal_info", aux_terminal_info, "GET")
                    else:
                        print "I: COMM: terminal info: not ready for refresh", aux_terminal_info               
                
                """ set timing settings """
                if(self.datastore.IsChanged("timing_settings")):
                    aux_timing_settings = self.datastore.Get("timing_settings", "SET")                                                                                                         
                    ret = self.send_receive_frame("SET_TIMING_SETTINGS", aux_timing_settings)                
                    self.datastore.ResetChangedFlag("timing_settings")  
        
            
            """
            tab DIAGNOSTIC                        
             - get diagnostic                                    
            """
            if(self.datastore.Get("active_tab") == TAB.diagnostic):        
                """ get diagnostic """
                #for cmd_group in DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']:                                          
                cmd_group = DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']['development']
                aux_diagnostic = self.send_receive_frame("GET_DIAGNOSTIC", cmd_group)
                                
                #print "aux_diagnostic", aux_diagnostic
                            
                """ store terminal-states to the datastore """ 
                #if(self.datastore.IsReadyForRefresh("timing_settings")):           
                #    self.datastore.Set("timing_settings", aux_timing_setting, "GET")
                #else:
                #    print "not ready for refresh", aux_timing_setting     
            
            """
            ALL TABs            
             - get timing settings                                    
            """
                                    
            """ get timing-settings """            
            aux_timing_setting = self.send_receive_frame("GET_TIMING_SETTINGS")            
            aux_timing_setting["name_id"] = 4
            
            #print aux_timing_setting            
            """ store terminal-states to the datastore """ 
            if not('error' in aux_timing_setting):
                if(self.datastore.IsReadyForRefresh("timing_settings")):            
                    self.datastore.Set("timing_settings", aux_timing_setting, "GET")
                else:
                    print "I: COMM: aux_timing_setting: not ready for refresh",aux_timing_setting                    
                    
            """
            ALL SETs            
             - potom bude parametr refreh v datastore zbytecny                                    
            """
            
            
    def AddTimeToDb(self, time):                       
                                    
        '''console ouput'''                                
        aux_csv_string = str(time['id']) + ";" + hex(time['user_id'])+ ";" + str(time['cell']) + ";" + str(time['run_id']) + ";" + str(time['time_raw']).replace(',', '.')                                
        print "I: Comm: receive time:",self.index_times, ":", aux_csv_string
        #print struct.pack('<I', time['user_id']).encode('hex')
                        
        '''alltag filter - activ only when rfid race and tag filter checked'''
        if(self.datastore.Get("rfid") == 2) and (self.datastore.Get("tag_filter") == 2):                
            ''' check tag id from table alltags'''
            if(time['user_id'] != 0) and (time['user_id'] != 1):            
                dbTag = self.db.getParX("alltags", "tag_id", time['user_id'], limit = 1).fetchone()
                if(dbTag == None):                
                    print "I: DB: this tag is NOT in table Alltags", time['user_id']
                    return False #tag not found
                                        
        '''save to database'''        
        keys = ["state", "id", "run_id", "user_id", "cell", "time_raw", "time"]
        values = [time['state'], time['id'],time['run_id'], time['user_id'], time['cell'], time['time_raw'], time['time']]
        ret = self.db.insert_from_lists("times", keys, values)
        
        '''return'''
        if ret == False:            
            print "I: DB: time already exists"                                                                            
        return ret                         

    def AddRunToDb(self, run):                
                                                    
        '''console output'''                   
        aux_csv_string = str(run['id']) + ";" + str(run['name_id']) + ";"
        print "I: Comm: receive run: ", self.index_runs, ":", aux_csv_string               
        
        '''save to database'''        
        keys = ["state","id", "starttime_id", "date", "name_id"]
        values = [run['state'], run['id'], run['starttime_id'], run['datetime'], run['name_id']]             
        ret = self.db.insert_from_lists("runs", keys, values)        
        
        '''return'''
        if ret == False:            
            print "I: DB: time already exists"                                                                            
        return ret 
                        
        return ret
                
if __name__ == "__main__":    
    print "main manage_com()"
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            