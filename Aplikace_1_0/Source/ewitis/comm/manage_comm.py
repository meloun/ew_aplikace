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
from ewitis.gui.tabCells import TabCells

#from ewitis.data.db import db
from ewitis.data.dstore import dstore

from ewitis.data.DEF_ENUM_STRINGS import * 
from threading import Thread

from ewitis.gui.multiprocessingManager import eventCalcNow


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
            if diagnostic:                
                dstore.AddDiagnostic(command, data, 'green', command_key)
            '''send and receive data'''            
            receivedata = self.protokol.send_receive_frame(command, data)                                                
            '''unpack data to dict structure'''
            data = callback.unpack_data(receivedata['cmd'], receivedata['data'], data)
            '''response diagnostic'''            
            if diagnostic:                                    
                dstore.AddDiagnostic(receivedata['cmd'], receivedata['data'], 'blue')                                                                              
        except (serialprotocol.SendReceiveError) as (errno, strerror):
            print "E:SendReceiveError - {1}({0})".format(errno, strerror)
            data = {"error":0xFF}
            #if(dstore.Get("diagnostic")["log_cyclic"] == 2) or (DEF_COMMANDS.IsCyclic(command_key)== False):
            if diagnostic:
                dstore.AddDiagnostic(command, "", 'red', command_key+": SendReceiveError")             
        except (serial.SerialException) as (strerror):            
            print "E:SendReceiveError - {0}()".format(strerror)
            data = {"error":0xFF}
            #if(dstore.Get("diagnostic")["log_cyclic"] == 2) or (DEF_COMMANDS.IsCyclic(command_key)== False):
            if diagnostic:
                dstore.AddDiagnostic(command, "", 'red', command_key+": SerialException")

 
        return data
    
    def run(self):       
        print "COMM: zakladam vlakno.."
        dstore.Set("com_init", 2)       
        
        ''' CONNECT TO EWITIS '''        
        try:
            self.protokol.open_port()
        except serial.SerialException:
            print "E: Cant open port"                                    
            dstore.SetItem("port", ["opened"], False)                        
            return            
        
        
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
                                                                                                        
        self.cell_nr = 0
            
        """slot tasking"""
        idx = idx_a = idx_b = idx_c = 0
        SLOT_A = [self.runGetCellOverview, self.runGetDeviceOverview, self.runGetTime, self.runGetTabSpecific, None]
        SLOT_B = [self.runGetRun, self.runGetCellInfo, None]
        SLOT_C = [self.runGetDeviceInfo, self.runGetRaceInfo, self.runGetDiagnostic]        
        LeastCommonMultiple = len(SLOT_A) * len(SLOT_B) * len(SLOT_C) 
        print "LCM:", LeastCommonMultiple
        
        while(1):
                                              
            #wait X millisecond, test if thread should be terminated
            ztime_first = time.clock()
                            
            #wait              
            #for i in range(10):                
            for i in range(2):
                #wait              
                time.sleep(0.01)
                               
            #terminate thread?                                                 
            if dstore.Get("port")["opened"] == False:
                self.stop()                                       
                return
                
            #print "I: Comm: waiting:",time.clock() - ztime_first,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            #ztime = time.clock()                            
                                         
            #communication enabled?
            if(dstore.Get("port")["enabled"] == False):                
                continue
                
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
                                
                #print "I: Comm: versions:",time.clock() - ztime,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                #ztime = time.clock()  
            """ end of hw-sw-version """
                        
            #print "I: Comm: each cycle: Actions: ",time.clock() - ztime,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            #ztime = time.clock()
                        
            
            """calling run functions"""
            
            '''each cycle'''
            self.runDeviceActions()
            self.runCellActions()
            self.runActions()
            self.runDiagnosticSendCommand()
                    
            '''slot A'''            
            if dstore.Get("development")["disabled_cyclic_commands"] == False:                                
                #print "-",idx,"-"
                idx_a = idx % len(SLOT_A)                                                
                if idx_a != len(SLOT_A)-1:                        
                    SLOT_A[idx_a]()            
                else:
                    '''slot B''' 
                    idx_b = (idx / len(SLOT_A)) % len(SLOT_B) 
                    if idx_b != len(SLOT_B)-1:                                                          
                        SLOT_B[idx_b]()
                    else:
                        '''slot C'''
                        idx_c = (idx / len(SLOT_A) / len(SLOT_B)) % len(SLOT_C)                                                   
                        SLOT_C[idx_c]()
         
                idx = idx + 1   
                if(idx == LeastCommonMultiple):
                    idx = 0                                                            
                                        
#             print "I: Comm:",
#             if idx_a != len(SLOT_A)-1:
#                 print "slot A", idx_a,
#             elif idx_b != len(SLOT_B)-1:
#                 print "slot B", idx_b,
#             else:
#                 print "slot C", idx_c,
#             print "-", idx, time.clock() - ztime_first,"s", datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
#             #ztime = time.clock()
                                                                                      
            
            """
            """
            if dstore.Get("com_init") != 0:
                dstore.Set("com_init", dstore.Get("com_init") - 1)
            
            
            dstore.SetItem("systemcheck", ["wdg_comm"],  dstore.GetItem("systemcheck", ["wdg_comm"])+1)    
    
        
    """
    runGetCellOverview()
     -   
    """
    def runGetTabSpecific(self):
        
        aux_tab = dstore.GetItem("gui", ["active_tab"])
        if(aux_tab == TAB.race_settings):
            self.runGetRaceInfo()
        elif(aux_tab == TAB.device):
            self.runGetDeviceInfo()
        elif(aux_tab == TAB.cells1) or (aux_tab == TAB.cells2):            
            self.runGetCellInfo()
        elif(aux_tab == TAB.diagnostic):
            self.runGetDiagnostic()
        else:
            pass        
            
        
                    
    """
    runGetCellOverview()
     -   
    """
    def runGetCellOverview(self):
        
        """get cell overview """                  
        aux_cell_overview = self.send_receive_frame("GET_CELL_OVERVIEW", diagnostic = dstore.Get("diagnostic")["log_cyclic"])
        #print "runGetCellOverview:", aux_cell_overview
                
        """ store data to the datastore """                        
        if not('error' in aux_cell_overview):
            if(dstore.IsReadyForRefresh("cells_info")):             
                for nr, co in enumerate(aux_cell_overview):                                                                  
                    dstore.SetItem("cells_info", [nr, "ir_signal"], co["ir_signal"], "GET", permanent = False)
                    dstore.SetItem("cells_info", [nr, "synchronized_once"], co["synchronized_once"], "GET", permanent = False)
                    dstore.SetItem("cells_info", [nr, "synchronized"], co["synchronized"], "GET", permanent = False)
                    dstore.SetItem("cells_info", [nr, "active"], co["active"], "GET", permanent = False)               
                    
    
    """
    runGetDeviceOverview()
     -   
    """
    def runGetDeviceOverview(self):
        
        """get device overview """            
        aux_device_overview = self.send_receive_frame("GET_TERMINAL_OVERVIEW", diagnostic = dstore.Get("diagnostic")["log_cyclic"])
        #print "runGetDeviceOverview:", aux_device_overview
                
        """ store data to the datastore """         
        if not('error' in aux_device_overview): 
            if(dstore.IsReadyForRefresh("terminal_info")):
                dstore.SetItem("timing_settings", ["measurement_state"], aux_device_overview["measurement_state"], "GET", permanent = False)                
                dstore.SetItem("timing_settings", ["tags_reading_enable"], aux_device_overview["tags_reading_enable"], "GET", permanent = False)
                dstore.Set("race_time", aux_device_overview['race_time'])                
            else:
                print "I: COMM: terminal info: not ready for refresh", aux_device_overview  
        
                            
         
    """
    runGetRaceInfo()
     - get timing-settings
     - get cell info  
    """
    def runGetRaceInfo(self):                
                    
        """ get timing-settings """            
        aux_timing_setting = self.send_receive_frame("GET_TIMING_SETTINGS", diagnostic = dstore.Get("diagnostic")["log_cyclic"])                    
                                
        #store to the datastore 
        if not('error' in aux_timing_setting):
            if(dstore.IsReadyForRefresh("timing_settings")):            
                dstore.Set("timing_settings", aux_timing_setting, "GET")                
            #else:
            #   print "I: COMM: aux_timing_setting: not ready for refresh",aux_timing_setting
            
    def runGetCellInfo(self):
        
        aux_diagnostic = dstore.Get("diagnostic") 
         
        """get cell info"""                                
        aux_cells_info = [None] #* NUMBER_OF.CELLS                
        #for i in range(0,  NUMBER_OF.CELLS):                                       
        aux_cells_info = self.send_receive_frame("GET_CELL_INFO", self.cell_nr +1, diagnostic = aux_diagnostic["log_cyclic"])                                                    
    
        """ store terminal-states to the datastore """ 
        if not('error' in aux_cells_info):                    
            if(dstore.IsReadyForRefresh("cells_info")):            
                dstore.SetItem("cells_info", [self.cell_nr], aux_cells_info, "GET", permanent = False)
                if dstore.Get("com_init"): #synchro get a set, tzn. comboboxu s lineedit - po navazani komunikace
                    dstore.SetItem("cells_info", [self.cell_nr, "task"], aux_cells_info["task"], "SET", permanent = False, changed = False)
                    
        #return nr of next cell
        self.cell_nr = self.cell_nr  +1 
        if self.cell_nr  == NUMBER_OF.CELLS:
            self.cell_nr  = 0        
    """
    runActions()
     - quit timing
     - clear database            
     - enable/disable tags reading
     - set cells info
    """
    def runActions(self):
        """ quit timing """
        if(dstore.IsChanged("quit_timing")):                                                                                     
            ret = self.send_receive_frame("QUIT_TIMING")
            dstore.ResetChangedFlag("quit_timing")
            
        """ clear database """
        if(dstore.IsChanged("clear_database")):                                                                                     
            ret = self.send_receive_frame("CLEAR_DATABASE")
            print "I: Comm: clearing database, please wait.. "
            time.sleep(21)
            self.index_times = 0
            self.index_run = 0
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
                
        """set cells info"""
        nr_changed_cells = dstore.IsChanged("cells_info")
        if(nr_changed_cells):            
            for nr_changed_cell in nr_changed_cells:                                          
                aux_cell_info = dstore.GetItem("cells_info", [nr_changed_cell], "SET")                                                                                                                                                                                                                                                   
                #print "COMM: set cell info", nr_changed_cell, aux_cell_info
                ret = self.send_receive_frame("SET_CELL_INFO", aux_cell_info)            
            dstore.ResetChangedFlag("cells_info")            
                    
    """
    runCellActions()
     - set cell diagnostic 
     - run cell diagnostic            
     - ping cell
     - get cell lasttimes
     - enable cekk
     - disable cell
     - generate time
    """
    def runCellActions(self):            
            
        """ set cell diag info""" 
        set_cell_diagnostic = dstore.Get("set_cell_diag_info", "SET")                           
        if(set_cell_diagnostic['address'] != 0):                                
            ret = self.send_receive_frame("SET_CELL_DIAG_INFO", set_cell_diagnostic) 
            dstore.SetItem("set_cell_diag_info", ['address'], 0, "SET")
            
        """ run cell diagnostic""" 
        address = dstore.Get("run_cell_diagnostic", "SET")                           
        if(address != 0):                                
            ret = self.send_receive_frame("RUN_CELL_DIAGNOSTIC", address) 
            dstore.Set("run_cell_diagnostic", 0, "SET")
            
        """ ping cell """ 
        address = dstore.Get("ping_cell", "SET")                           
        if(address != 0):                                
            ret = self.send_receive_frame("PING_CELL", address) 
            dstore.Set("ping_cell", 0, "SET")                                
            
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
        #print "gc", time.clock()     
        generate_celltime = dstore.Get("generate_celltime", "SET")                                   
        if(generate_celltime['task'] != 0):                                             
            ret = self.send_receive_frame("GENERATE_CELLTIME", generate_celltime) 
            dstore.Set("generate_celltime", {'task':0, 'user_id':0}, "SET")
    
    """
    runDeviceGetInfo()
     - get terminal-info 
     - get race time
    """  
    def runGetDeviceInfo(self):
        
        aux_diagnostic = dstore.Get("diagnostic") 
        
        """ get terminal-info """                     
        aux_terminal_info = self.send_receive_frame("GET_TERMINAL_INFO", diagnostic = aux_diagnostic["log_cyclic"])                         
        #store terminal-info to the datastore """
        if not('error' in aux_terminal_info): 
            if(dstore.IsReadyForRefresh("terminal_info")):           
                dstore.Set("terminal_info", aux_terminal_info, "GET")
            else:
                print "I: COMM: terminal info: not ready for refresh", aux_terminal_info
                
    def runGetRaceTime(self):            
        """get race time"""   
        aux_diagnostic = dstore.Get("diagnostic")                                                                                
        aux_racetime = self.send_receive_frame("GET_ACTUAL_RACE_TIME", diagnostic = aux_diagnostic["log_cyclic"])
        dstore.Set("race_time", aux_racetime['time'])                          
        
    """
    runDeviceActions()    
     - synchronize system            
     - set speaker
     - set timing settings
    """        
    def runDeviceActions(self):
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

        """ set timing settings """                
        if(dstore.IsChanged("timing_settings")):                    
            aux_timing_settings = dstore.Get("timing_settings", "SET")
            #print  "TS", aux_timing_settings                                                                                                         
            ret = self.send_receive_frame("SET_TIMING_SETTINGS", aux_timing_settings)                
            dstore.ResetChangedFlag("timing_settings")
             
    def runDiagnosticSendCommand(self):
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
    runGetTime()
     - get new time
     - store new time to the database
    """
    def runGetTime(self):     
        
        aux_diagnostic = dstore.Get("diagnostic")    
                                            
        """ GET NEW TIME """                                                                  
        aux_time = self.send_receive_frame("GET_TIME_PAR_INDEX", self.index_times, diagnostic = aux_diagnostic["log_cyclic"])                                                                                    
                    
        if(aux_time['error'] == 0):
            print"================="
                                               
        if(aux_time['error'] != 0):
            dstore.SetItem("diagnostic", ["no_new_time_cnt"], aux_diagnostic["no_new_time_cnt"]+1)            
                                                                                                                                                                                
                
        """ STORE NEW TIME TO THE DATABASE """
        if(aux_time['error'] == 0):                 
            self.AddTimeToDb(aux_time)                                                                                                                           
            self.index_times += 1 # done, take next 
            eventCalcNow.set()                                                                            
        else:
            pass # no new time                  
    

    """
    runGetRun()
     - get new run
     - store new run to the databasae 
    """
    def runGetRun(self):        
        
        """ GET NEW RUN """                                                                                   
        aux_run = self.send_receive_frame("GET_RUN_PAR_INDEX", self.index_runs, diagnostic = dstore.Get("diagnostic")["log_cyclic"])
        if(aux_run['error'] == 0):
            print"================="
            
                    
        if(aux_run['error'] != 0):
            dstore.SetItem("diagnostic", ["no_new_run_cnt"], dstore.Get("diagnostic")["no_new_run_cnt"]+1)
        
        """ STORE NEW RUN TO THE DATABASE """
        if(aux_run['error'] == 0):                       
            self.AddRunToDb(aux_run)                                                                              
            self.index_runs += 1 # done, take next
            if dstore.Get("current_run") == 0:
                dstore.Set("current_run", aux_run["id"])                                                                                                        
        else:
            pass # no new run                        
    
    """
    runGetDiagnostic()
     - get diagnostic    
    """
    def runGetDiagnostic(self):
        """ get diagnostic """
        #for cmd_group in DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']:                                          
        cmd_group = DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic']['development']
        aux_diagnostic = self.send_receive_frame("GET_DIAGNOSTIC", cmd_group, diagnostic = dstore.Get("diagnostic")["log_cyclic"])
                        
        #print "aux_diagnostic", aux_diagnostic
                    
        """ store terminal-states to the datastore """ 
        #if(dstore.IsReadyForRefresh("timing_settings")):           
        #    dstore.Set("timing_settings", aux_timing_setting, "GET")
        #else:
        #    print "not ready for refresh", aux_timing_setting                                                                             
            
    def AddTimeToDb(self, time):                       
                                    
        '''console ouput''' 
        print time                               
        aux_csv_string = str(time['id']) + ";" + hex(time['user_id'])+ ";" + str(time['cell']) + ";" + str(time['run_id']) + ";" + str(time['time_raw']).replace(',', '.')                                
        print "I: Comm: receive time:",self.index_times, ":", aux_csv_string
        
        #print struct.pack('<I', time['user_id']).encode('hex')

        '''auto number'''
        ds_times = dstore.Get("times")
        if(ds_times["auto_number_enable"] and (ds_times["auto_number_logic"] == False)):
            auto_number = ds_times["auto_number"][0]
            if(auto_number != 0) and (time['user_id'] == 0) and (dstore.GetItem("racesettings-app", ['rfid']) == 0):
                dbUser = self.db.getParX("users", "nr", auto_number, limit = 1).fetchone()
                if dbUser != None:
                    time['user_id'] = dbUser['id']
        
        '''hack for car sprint'''
#         time['un1'] = time['cell']                    
#         if (time['cell'] == 2) or (time['cell']== 3):
#             time['cell'] = 1
#         elif (time['cell'] == 4) or (time['cell'] == 5):
#             time['cell'] = 250       
                                
        '''alltag filter - active only when rfid race and tag filter checked'''
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
        
        '''hack for car sprint'''
        #keys.append("un1")
        #values.append(time["un1"])
        ret = self.db.insert_from_lists("times", keys, values)
        
      
        
        '''return'''
        if ret == False:            
            print "I: DB: time already exists"
        else:
            #shift auto numbers
            aux_new_times = dstore.GetItem("gui", ["update_requests", "new_times"])
            aux_new_times.append(time)  
            dstore.SetItem("gui", ["update_requests", "new_times"], aux_new_times)                                                                              
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
 
                    
            
