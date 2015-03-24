# -*- coding: utf-8 -*-
'''
Created on 10.06.2010
@author: Lubos Melichar
'''

import serial
import time
import datetime
import struct
import json
import libs.dicts.dicts as dicts
import libs.file.file as file
import libs.comm.serialprotocol as serialprotocol
import libs.sqlite.sqlite as sqlite
import libs.html.htmltags as htmltags
import libs.html.html as html
import libs.utils.utils as utils
import ewitis.comm.callback as callback
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS
from ewitis.data.DEF_DATA import TAB

#from ewitis.data.db import db
from ewitis.data.dstore import dstore

from ewitis.data.DEF_ENUM_STRINGS import * 
from threading import Thread


#prozatimni "define"
OPTIKA_V2 = True

class ManageComm(Thread):            
    def __init__(self, dstore):
        """ INIT VALUES """
        
        Thread.__init__(self)        
        
        #set start download indexes
        self.index_runs = 0
        self.index_times = 0
        self.no_new_times = 0
        self.no_new_runs = 0
#         if(dstore.Get("download_from_last") == 2):      
#             if(dstore.Get("count")['Runs'] - 1) > 0:          
#                 self.index_runs = dstore.Get("count")['Runs'] - 1
#             if(dstore.Get("count")['Times'] - 1) > 0:
#                 self.index_times = dstore.Get("count")['Times'] - 1        
                                                                                      
                                                        
        ''' LOAD USER CONFIGURATION - port, baudrate '''            
        #USER_CONF = conf.load(self.conf_file, {"port": "COM8", "baudrate": 38400})
        
        
        ''' CONNECT TO EWITIS '''
        aux_port = dstore.Get("port")                
        self.protokol = serialprotocol.SerialProtocol( port = aux_port["name"], baudrate = aux_port["baudrate"])        
        print "COMM: zakladam instanci.."                        
        
    def __del__(self):
        print "COMM: mazu instanci.."
        
    def stop(self):
        self.protokol.close_port()
        print "COMM: koncim vlakno.."
        
    def send_receive_frame(self, command_key, data="", length = None, diagnostic = True):
        """ ošetřená vysílací, přijímací metoda """                
        if command_key != "GET_HW_SW_VERSION":
            device = dstore.Get("versions")["device"]
            if(DEF_COMMANDS.DEF_COMMANDS[command_key][device] == False):
            
                #this command is not defined for this device
                #print "E: command not defined for this device", command_key                                
                return {"error":0xFF}
            
        command = DEF_COMMANDS.DEF_COMMANDS[command_key]['cmd']                                             
                      
        try:
            '''pack data to the string'''
            data = callback.pack_data(command_key, data)                        
            '''request diagnostic'''            
            if diagnostic == True:                
                dstore.AddDiagnostic(command, data, 'green', command_key)
            '''send and receive data'''            
            receivedata = self.protokol.send_receive_frame(command, data)                                                
            '''unpack data to dict structure'''
            data = callback.unpack_data(receivedata['cmd'], receivedata['data'], data)
            '''response diagnostic'''            
            if diagnostic == True:                                    
                dstore.AddDiagnostic(receivedata['cmd'], receivedata['data'], 'blue')                                                                              
        except (serialprotocol.SendReceiveError) as (errno, strerror):
            print "E:SendReceiveError - {1}({0})".format(errno, strerror)
            data = {"error":0xFF}
            #if(dstore.Get("diagnostic")["log_cyclic"] == 2) or (DEF_COMMANDS.IsCyclic(command_key)== False):
            if diagnostic == True:
                dstore.AddDiagnostic(command, "", 'red', command_key+": SendReceiveError")             
        except (serial.SerialException) as (strerror):            
            print "E:SendReceiveError - {0}()".format(strerror)
            data = {"error":0xFF}
            #if(dstore.Get("diagnostic")["log_cyclic"] == 2) or (DEF_COMMANDS.IsCyclic(command_key)== False):
            if diagnostic == True:
                dstore.AddDiagnostic(command, "", 'red', command_key+": SerialException")

 
        return data
                                                            
    def run(self):       
        print "COMM: zakladam vlakno.."       
        
        ''' CONNECT TO EWITIS '''        
        try:
            self.protokol.open_port()
        except serial.SerialException:
            print "E: Cant open port"
            #dstore.Set("port_enable", False)                        
            dstore.SetItem("port", ["opened"], False)                        
            return            
            #raise serial.SerialException
        
        
        """ DATABASE """        
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")
        
            '''connect to db'''  
            self.db.connect()
        except:
            #dstore.Set("port_enable", False)
            dstore.SetItem("port", ["opened"], False)
            print "E: Database"
        
        
        """communication established"""
        #dstore.Set("port_enable", True)
        dstore.SetItem("port", ["opened"], True)
            
                                                                                    
        while(1):
                                  
            #wait X millisecond, test if thread should be terminated
            ztime = time.clock()
            for i in range(10): 
                
                #wait              
                time.sleep(0.01)
                
                #wait longer(for terminal - no info yet)                    
                #time.sleep(0.01)
                
                #terminate thread?                                 
                #if(dstore.Get("port_enable", "GET_SET") == False):
                if dstore.Get("port")["opened"] == False:
                    self.stop()                                       
                    return
                
            #print "I: Comm: waiting:",time.clock() - ztime,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]                            
                                         
            #communication enabled?
            if(dstore.Get("port")["enabled"] == False):                
                continue
            
            #add diagnostic? 
            diagnostic = False
            if(dstore.Get("diagnostic")["log_cyclic"] == 2):                
                diagnostic = True  
                
            """ 
            GET HW-SW-VERSION 
                only once (after start sw,hw = none)
            """            
            if(dstore.Get("versions")["hw"] == None) or (dstore.Get("versions")["fw"] == None):
                
                aux_version = self.send_receive_frame("GET_HW_SW_VERSION")
                print "version:", aux_version
                                
                if ('error' in aux_version): 
                    print "E: Comm: no Hw and Fw versions on device"                
                    continue #no other commands as long as no version
                
                dstore.SetItem("versions", ["hw"], aux_version["hw"])
                dstore.SetItem("versions", ["fw"], aux_version["fw"])
                dstore.SetItem("versions", ["device"], aux_version["device"])
            """ end of hw-sw-version """
            
            """ 
            SEND COMMAND 
                diagnostic purpose
            """ 
            if(dstore.Get("diagnostic")["sendcommandkey"] != None):
                                
                #send command                
                aux_response = self.send_receive_frame(dstore.Get("diagnostic")["sendcommandkey"], (dstore.Get("diagnostic")["senddata"]).decode('hex'))                                
                                
                if ('error' in aux_response): 
                    print "COMM: sendcommand response: ERROR"                                     
                
                #smazat request
                dstore.SetItem("diagnostic", ["sendcommandkey"], None)
                                
                #set response (text to label)                
                dstore.SetItem("diagnostic", ["sendresponse"], json.dumps(aux_response, indent = 4))
                                
            
            
            """
            RUNS & TIMES & DATABASE PART
             - get new time
             - get new run
             - store new time to the databasae
             - store new run to the databasae
            """          
              
                        
            """ GET NEW TIME """                                                                  
            aux_time = self.send_receive_frame("GET_TIME_PAR_INDEX", self.index_times, diagnostic = diagnostic)                                                
            
            """ GET NEW RUN """                                                                                   
            aux_run = self.send_receive_frame("GET_RUN_PAR_INDEX", self.index_runs, diagnostic = diagnostic)                      
            
                        
            if(aux_time['error'] == 0 or aux_run['error'] == 0):
                print"================="

            """ GET NEW RUN """           
            aux_diagnostic = dstore.Get("diagnostic")                
            if(aux_time['error'] != 0):
                dstore.SetItem("diagnostic", ["no_new_time_cnt"], aux_diagnostic["no_new_time_cnt"]+1)
                
            if(aux_run['error'] != 0):
                dstore.SetItem("diagnostic", ["no_new_run_cnt"], aux_diagnostic["no_new_run_cnt"]+1)                        
            
            #dstore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='red'>no new times (100)</font><br>")
            #dstore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='green'>no new times (100)</font><br>")
            #dstore.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+"<font color='blue'>no new times (100)</font><br>")                                                                                                                                                                    
                    
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
            
            """ GET RACE TIME """                                                                                   
            aux_racetime = self.send_receive_frame("GET_ACTUAL_RACE_TIME", diagnostic = diagnostic)
            dstore.Set("race_time", aux_racetime['time'])              
                            
                
            """
            barCellActions            
             - enable/disable startcell
             - enable/disable finishcell
             - generate starttime
             - generate finishtime
             - quit timing                        
             - clear database                        
             - enable/disable tags reading
            """
            
            '''CELL ADDRESS ACTIONS, toolbar'''
            
            """ set cell diag info""" 
            set_cell_diagnostic = dstore.Get("set_cell_diag_info", "SET")                           
            if(set_cell_diagnostic['address'] != 0):                                
                ret = self.send_receive_frame("SET_CELL_DIAG_INFO", set_cell_diagnostic) 
                dstore.SetItem("set_cell_diag_info", ['address'],0, "SET")
                
            """ ping cell """ 
            address = dstore.Get("ping_cell", "SET")                           
            if(address != 0):                                
                ret = self.send_receive_frame("PING_CELL", address) 
                dstore.Set("ping_cell", 0, "SET")
                
            """ run cell diagnostic""" 
            address = dstore.Get("run_cell_diagnostic", "SET")                           
            if(address != 0):                                
                ret = self.send_receive_frame("RUN_CELL_DIAGNOSTIC", address) 
                dstore.Set("run_cell_diagnostic", 0, "SET")
                
            '''CELL TASK ACTIONS, tab cells'''
                
            """ get cell last times """ 
            task = dstore.Get("get_cell_last_times", "SET")                           
            if(task != 0):                                
                ret = self.send_receive_frame("GET_CELL_LAST_TIME", task) 
                dstore.Set("get_cell_last_times", 0, "SET")
                
            """ enable cell """ 
            task = dstore.Get("enable_cell", "SET")                           
            if(task != 0):                                
                ret = self.send_receive_frame("ENABLE_CELL", task) 
                dstore.Set("enable_cell", 0, "SET")
                                 
            """ disable cell """ 
            task = dstore.Get("disable_cell", "SET")                           
            if(task != 0):                                
                ret = self.send_receive_frame("DISABLE_CELL", task) 
                dstore.Set("disable_cell", 0, "SET")
                                 
            """ generate celltime """ 
            generate_celltime = dstore.Get("generate_celltime", "SET")                           
            if(generate_celltime['task'] != 0):                                
                ret = self.send_receive_frame("GENERATE_CELLTIME", generate_celltime) 
                dstore.Set("generate_celltime", {'task':0, 'user_id':0}, "SET")                 
                                                                    
                    
            """ quit timing """
            if(dstore.IsChanged("quit_timing")):                                                                                     
                ret = self.send_receive_frame("QUIT_TIMING")
                dstore.ResetChangedFlag("quit_timing")
                
            """ clear database """
            if(dstore.IsChanged("clear_database")):                                                                                     
                ret = self.send_receive_frame("CLEAR_DATABASE")
                print "I: Comm: clearing database, please wait.. "
                time.sleep(21)
                dstore.ResetChangedFlag("clear_database")
                print "I: Comm: database should be empty now"
                
            """ enable/disable tags reading """
            if(dstore.IsChanged("tags_reading")):         
                on_off = dstore.Get("tags_reading", "SET")                                                                                               
                ret = self.send_receive_frame("SET_TAGS_READING", on_off)
                dstore.ResetChangedFlag("tags_reading")
                if(on_off):
                    print "I: Comm: Enable tags reading"
                else:
                    print "I: Comm: Disable tags reading"
            
            """ end of ACTIONS """
            
            """
            tab RACE SETTINGS & tab DEVICE            
             - set speaker             
             - get terminal info
             - set timing settings                                                                          
            """                                                                   
            if(dstore.GetItem("gui", ["active_tab"]) == TAB.race_settings)\
                or (dstore.GetItem("gui", ["active_tab"]) == TAB.device):                                
                                                                  
                """ synchronize system """
                if(dstore.IsChanged("synchronize_system")):                                                                                     
                    ret = self.send_receive_frame("SYNCHRONIZE_SYSTEM")
                    print "I: Comm: synchronize system.. "
                    dstore.ResetChangedFlag("synchronize_system")                    
                
                
                """ set speaker """
                if(dstore.IsChanged("speaker")):                                                                                                
                    aux_speaker = dstore.Get("speaker", "SET")                                                                                                                              
                    ret = self.send_receive_frame("SET_SPEAKER", aux_speaker)
                    dstore.ResetChangedFlag("speaker")                                                                                            
                                
                                                                                    
                """ get terminal-info """                     
                aux_terminal_info = self.send_receive_frame("GET_TERMINAL_INFO")                         
                """ store terminal-info to the datastore """
                if not('error' in aux_terminal_info): 
                    if(dstore.IsReadyForRefresh("terminal_info")):           
                        dstore.Set("terminal_info", aux_terminal_info, "GET")
                    else:
                        print "I: COMM: terminal info: not ready for refresh", aux_terminal_info               
                
                """ set timing settings """                
                if(dstore.IsChanged("timing_settings")):                    
                    aux_timing_settings = dstore.Get("timing_settings", "SET")
                    #print  "TS", aux_timing_settings                                                                                                         
                    ret = self.send_receive_frame("SET_TIMING_SETTINGS", aux_timing_settings)                
                    dstore.ResetChangedFlag("timing_settings")  
        
            """
            tab CELLs
            - clear diag, run diag, buttons ping,                                                                        
            """ 
            if(dstore.GetItem("gui", ["active_tab"]) == TAB.cells):
                pass
            
            """
            tab DIAGNOSTIC                        
             - get diagnostic                                    
            """
            if(dstore.GetItem("gui", ["active_tab"]) == TAB.diagnostic):                    
                """ get diagnostic """
                #for cmd_group in DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']:                                          
                cmd_group = DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']['development']
                aux_diagnostic = self.send_receive_frame("GET_DIAGNOSTIC", cmd_group)
                                
                #print "aux_diagnostic", aux_diagnostic
                            
                """ store terminal-states to the datastore """ 
                #if(dstore.IsReadyForRefresh("timing_settings")):           
                #    dstore.Set("timing_settings", aux_timing_setting, "GET")
                #else:
                #    print "not ready for refresh", aux_timing_setting     
            
            """
            ALL TABs            
             - get timing settings                                    
            """
                                    
            """ get timing-settings """            
            aux_timing_setting = self.send_receive_frame("GET_TIMING_SETTINGS", diagnostic = diagnostic)            
            #aux_timing_setting["name_id"] = 4
                                    
            """ store terminal-states to the datastore """ 
            if not('error' in aux_timing_setting):
                if(dstore.IsReadyForRefresh("timing_settings")):            
                    dstore.Set("timing_settings", aux_timing_setting, "GET")
                #else:
                #   print "I: COMM: aux_timing_setting: not ready for refresh",aux_timing_setting
                    
            """ get cell info """
            if OPTIKA_V2:
                #SET CELL INFO
                nr_changed_cells = dstore.IsChanged("cells_info")
                if(nr_changed_cells):
                    for nr_changed_cell in nr_changed_cells:                                          
                        aux_cell_info = dstore.GetItem("cells_info", [nr_changed_cell], "SET")                                                                                                                                                                                                                                                   
                        #print "COMM: set cell info", nr_changed_cell, aux_cell_info
                        ret = self.send_receive_frame("SET_CELL_INFO", aux_cell_info)
                    dstore.ResetChangedFlag("cells_info")
                
                #GET CELL INFO                                
                aux_cells_info = [None] * NUMBER_OF.CELLS                
                for i in range(0,  NUMBER_OF.CELLS):                                       
                    aux_cells_info[i] = self.send_receive_frame("GET_CELL_INFO", i+1, diagnostic = diagnostic)                                                 
                
                    """ store terminal-states to the datastore """ 
                    if not('error' in aux_cells_info[i]):                    
                        if(dstore.IsReadyForRefresh("cells_info")):             
                            dstore.SetItem("cells_info", [i], aux_cells_info[i], "GET", permanent = False)
                            #print i, aux_cells_info[i]
                        #else:
                        #print "I: COMM: cell info: not ready for refresh", aux_cells_info[i]            
                                
                    
            """
            ALL SETs            
             - potom bude parametr refreh v datastore zbytecny                                    
            """
            
            
    def AddTimeToDb(self, time):                       
                                    
        '''console ouput''' 
        print time                               
        aux_csv_string = str(time['id']) + ";" + hex(time['user_id'])+ ";" + str(time['cell']) + ";" + str(time['run_id']) + ";" + str(time['time_raw']).replace(',', '.')                                
        print "I: Comm: receive time:",self.index_times, ":", aux_csv_string
        #print struct.pack('<I', time['user_id']).encode('hex')
                        
        '''alltag filter - activ only when rfid race and tag filter checked'''
        racesettings_app = dstore.Get("racesettings-app")
        if(racesettings_app["rfid"] == 2) and (racesettings_app["tag_filter"] == 2):                
            ''' check tag id from table alltags'''
            if(time['user_id'] != 0) and (time['user_id'] != 1):            
                dbTag = self.db.getParX("alltags", "tag_id", time['user_id'], limit = 1).fetchone()
                if(dbTag == None):                
                    print "I: DB: this tag is NOT in table Alltags", time['user_id']
                    return False #tag not found
                                        
        '''save to database'''        
        keys = ["state", "id", "run_id", "user_id", "cell", "time_raw"]#, "time"]
        values = [time['state'], time['id'],time['run_id'], time['user_id'], time['cell'], time['time_raw']] #, time['time']]
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
        keys = ["state","id", "starttime_id", "date", "name_id", "description"]
        values = [run['state'], run['id'], run['starttime_id'], run['datetime'], run['name_id'], u"race nr."+str(self.index_runs+1)]             
        ret = self.db.insert_from_lists("runs", keys, values)        
        
        '''return'''
        if ret == False:            
            print "I: DB: run already exists"                                                                            
        return ret 
                        
        return ret
                
if __name__ == "__main__":    
    print "main manage_com()"
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            