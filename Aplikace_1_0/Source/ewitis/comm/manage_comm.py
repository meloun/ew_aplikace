# -*- coding: utf-8 -*-
'''
Created on 10.06.2010
@author: Lubos Melichar
'''

import serial
import time
import datetime
import struct
import simplejson as json
import codecs
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
        self.index_times = 0
        #self.no_new_times = 0
        #self.no_new_runs = 0
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
        #cell versions
        print "COMM: Reset: cells_info"   
        
        dstore.SetItem("gui", ["update_requests", "tableCells_sync"], True)             
        print "STOP: nastavuju", dstore.GetItem("gui", ["update_requests", "tableCells_sync"]) 
        dstore.ResetToDefault("cells_info", "GET", False)
        dstore.ResetToDefault("cells_info", "SET", False)
                
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
        #except:
        #    print "E:SendReceiveError - probably other command requested"

        return data
    
    def run(self):       
        print "COMM: zakladam vlakno..", time.clock()
        dstore.Set("com_init", 30)
        
        ##Reset all HW settings
        #projit def_data a co neni permanent tak dat do default?
        
        #BB version
        print "COMM: Reset: versions"
        dstore.SetItem("versions", ["hw"], None)
        dstore.SetItem("versions", ["sw"], None)
        
        #cell versions
        print "COMM: Reset: cells_info"
        #dstore.ResetToDefault("cells_info", "GET")
        
        #timing settings
        
        #cell info
        
        #device info     
        
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

        self.CellIdx_ForCellInfo = 0
        self.CellIdx_ForVersions = 0
                        

        """slot tasking"""
        idx = idx_a = idx_b = idx_c = 0
        SLOT_A = [self.runGetCellOverview, self.runGetDeviceOverview, self.runGetTime, None]
        SLOT_B = [self.runGetCellInfo, self.runGetTabSpecific, None]
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
                try:
                    aux_diagnostics = self.runGetDiagnostic()
                    myjson = json.dumps(aux_diagnostics)
                    filename = 'log/'+time.strftime("%Y_%m_%d__%H_%M_", time.localtime())+'00_diagnostics.txt'
                    json.dump(aux_diagnostics, codecs.open(filename, 'w', 'utf-8'), ensure_ascii = False, indent = 4, sort_keys=True)
                    #f = open("Diagnostics.log","w")
                    #f.write( str(aux_diagnostics) )
                    #f.close()                    
                except:
                    print "E: Comm: Diagnostics.log"
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
                if(dstore.Get("com_init") == 0):
                    
                    """ Init Event """                    
                    #
                    print "init: nastavuju"                    
                    dstore.SetItem("gui", ["update_requests", "tableCells_sync"], True)
                    print "COMM: Initialized"
            
            
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
            self.runGetCellVersion()
        elif(aux_tab == TAB.cells1) or (aux_tab == TAB.cells2) or (aux_tab == TAB.cells3):
            self.runGetCellInfo()
        elif(aux_tab == TAB.diagnostic):
            self.runGetDiagnostic()
        else:
            self.runGetCellInfo()
            


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
                    if nr < NUMBER_OF.CELLS:
                        dstore.SetItem("cells_info", [nr, "ir_signal"], co["ir_signal"], "GET", permanent = False)
                        dstore.SetItem("cells_info", [nr, "synchronized_once"], co["synchronized_once"], "GET", permanent = False)
                        dstore.SetItem("cells_info", [nr, "synchronized"], co["synchronized"], "GET", permanent = False)
                        dstore.SetItem("cells_info", [nr, "missing_time_flag"], co["missing_time_flag"], "GET", permanent = False)
                        dstore.SetItem("cells_info", [nr, "insystem"], co["insystem"], "GET", permanent = False)
                        dstore.SetItem("cells_info", [nr, "active"], co["active"], "GET", permanent = False) 
                        #print "INFO: ", nr, dstore.Get("cells_info", "GET")[nr]                                               

    
    """
    runGetDeviceOverview()
     -   
    """
    def runGetDeviceOverview(self):
        
        """get device overview """            
        aux_device_overview = self.send_receive_frame("GET_DEVICE_OVERVIEW", diagnostic = dstore.Get("diagnostic")["log_cyclic"])
        #print "runGetDeviceOverview:", aux_device_overview
                
        """ store data to the datastore """         
        if not('error' in aux_device_overview): 
            if(dstore.IsReadyForRefresh("terminal_info")):
                dstore.SetItem("timing_settings", ["measurement_state"], aux_device_overview["measurement_state"], "GET", permanent = False)                
                dstore.SetItem("timing_settings", ["autoenable_cell"], aux_device_overview["autoenable_cell"], "GET", permanent = False)
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
    
    
    """
    GetCellInSystem()
    """
    def GetCellInSystem(self, start_idx):
        ''' get cell info '''                        
        ds_cells_info = dstore.Get("cells_info", "GET")
        
        ''' find next cell in system '''                  
        if ds_cells_info != None:            
            for i in range(0,  NUMBER_OF.CELLS):                
                aux_cell_nr = (start_idx + i) % NUMBER_OF.CELLS                                                 
                if(ds_cells_info[aux_cell_nr]["insystem"]) == True:                                        
                    break;
            else:
                ''' no cell found '''
                aux_cell_nr = None

            return aux_cell_nr 
    
    def runGetCellVersion(self):
        ''' find next cell in in system '''
        cell_idx = self.GetCellInSystem(self.CellIdx_ForVersions)
        #print "CV1:", self.CellIdx_ForVersions, cell_idx
        
        
        if(cell_idx != None):
            ''' send command '''
            aux_cells_version = self.send_receive_frame("GET_CELL_VERSION", cell_idx + 1, diagnostic = dstore.Get("diagnostic")["log_cyclic"])

            ''' store cell info to the datastore  '''
            if not('error' in aux_cells_version):
                #save to dstore                                           
                dstore.SetItem("versions", ["cells", cell_idx], aux_cells_version["cells"],  permanent = False)
                
            ''' update idx after last cell in sysem '''
            self.CellIdx_ForVersions = (cell_idx + 1) % NUMBER_OF.CELLS
        else:
            ''' increment idx to next cell '''
            self.CellIdx_ForVersions = (self.CellIdx_ForVersions + 1) % NUMBER_OF.CELLS   


    def runGetCellInfo(self):
        ''' find next cell in in system '''
        cell_idx = self.GetCellInSystem(self.CellIdx_ForCellInfo)

        if(cell_idx != None):
            
            ''' send command '''
            aux_cells_info = self.send_receive_frame("GET_CELL_INFO", cell_idx + 1, diagnostic = dstore.Get("diagnostic")["log_cyclic"])

            ''' store cell info to the datastore ''' 
            if not('error' in aux_cells_info):                    
                if(dstore.IsReadyForRefresh("cells_info")):
                    #copy insystem                    
                    aux_cells_info["insystem"] = dstore.Get("cells_info", "GET")[cell_idx]["insystem"]
                    
                    aux_cells_info["missing_time_flag"] = bool(aux_cells_info["missing_time_flag"])
                
                    #save to dstore                                           
                    dstore.SetItem("cells_info", [cell_idx], aux_cells_info, "GET", permanent = False)
                    
                    #synchro get a set, tzn. comboboxu s lineedit - po navazani komunikace
                    if dstore.Get("com_init"):                     
                        dstore.SetItem("cells_info", [cell_idx, "task"], aux_cells_info["task"], "SET", permanent = False, changed = False)
                        
                ''' update idx after last cell in sysem '''
                self.CellIdx_ForCellInfo = (cell_idx + 1) % NUMBER_OF.CELLS
            else:
                ''' increment idx to next cell '''
                self.CellIdx_ForVersions = (self.CellIdx_ForVersions + 1) % NUMBER_OF.CELLS

            
    def runGetCellInfo_OLD(self):        
                          
        """get cell info"""                        
        ds_cells_info = dstore.Get("cells_info", "GET")                
                  
        if ds_cells_info != None:            
            for i in range(0,  NUMBER_OF.CELLS):                
                aux_cell_nr = (self.CellIdx_ForCellInfo + i) % NUMBER_OF.CELLS                                                 
                if(ds_cells_info[aux_cell_nr]["insystem"]) == True:
                    #print "InSystem: ", aux_cell_nr, i
                    self.CellIdx_ForCellInfo = aux_cell_nr
                    break
                #else:
                #    print "NO InSystem: ", aux_cell_nr, i
                         
        aux_cells_info = self.send_receive_frame("GET_CELL_INFO", self.CellIdx_ForCellInfo + 1, diagnostic = dstore.Get("diagnostic")["log_cyclic"])
        #print "COMM CellInfo", self.cell_nr, "-", time.clock(), dstore.Get("com_init")   
        #print "COMM CellInfo", self.cell_nr, "-", aux_cells_info,  time.clock()                                                  
     
        """ store cell info to the datastore """ 
        if not('error' in aux_cells_info):                    
            if(dstore.IsReadyForRefresh("cells_info")):
                
                #copy insystem
                aux_cells_info["insystem"] = ds_cells_info[self.CellIdx_ForCellInfo]["insystem"]
                
                #save to dstore                                           
                dstore.SetItem("cells_info", [self.CellIdx_ForCellInfo], aux_cells_info, "GET", permanent = False)
                #synchro get a set, tzn. comboboxu s lineedit - po navazani komunikace
                if dstore.Get("com_init"):                     
                    dstore.SetItem("cells_info", [self.CellIdx_ForCellInfo, "task"], aux_cells_info["task"], "SET", permanent = False, changed = False)

                     
        self.CellIdx_ForCellInfo = self.CellIdx_ForCellInfo + 1;
        if (self.CellIdx_ForCellInfo  == NUMBER_OF.CELLS):
            self.CellIdx_ForCellInfo  = 0
                                 
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
            time.sleep(30)
            self.index_times = 0
            self.index_runs = 0
            dstore.ResetChangedFlag("clear_database")
            print "I: Comm: database should be empty now"
            
#         """ enable/disable tags reading """
#         if(dstore.IsChanged("tags_reading")):         
#             on_off = dstore.Get("tags_reading", "SET")                                                                                               
#             ret = self.send_receive_frame("SET_TAGS_READING", on_off)
#             dstore.ResetChangedFlag("tags_reading")
#             if(on_off):
#                 print "I: Comm: Enable tags reading"
#             else:
#                 print "I: Comm: Disable tags reading"                
                
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
                                            
        """ clear missing times """ 
        address = dstore.Get("clear_missing_times", "SET")                           
        if(address != 0):                                
            ret = self.send_receive_frame("CLEAR_MISSING_TIMES", address) 
            dstore.Set("clear_missing_times", 0, "SET")                                
            
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
                                                                                                                                                                                                            
        """ set datetime """
        if(dstore.IsChanged("datetime")):                                                                                                
            aux_datetime = dstore.Get("datetime", "SET")                                                                                                                              
            ret = self.send_receive_frame("SET_DATETIME", aux_datetime)
            dstore.ResetChangedFlag("datetime")                                                                                                                                                                                                

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
        ds_racesettings = dstore.Get("racesettings-app")
        
        if(aux_time['error'] == 0):
            aux_time['us1'] = ""
            aux_time['un1'] = 0
            
            #SPRINT: add us 'A'
            if(ds_racesettings["autonumbers"]["mode"] == AutonumbersMode.SPRINT):
                if(aux_time['cell'] == 1):
                    aux_time['us1'] = 'A'
                                
            self.AddTimeToDb(aux_time)            
            self.index_times += 1 # done, take next
            
            #SPRINT: duplicate the semaphore start time with us 'B'
            if(ds_racesettings["autonumbers"]["mode"] == AutonumbersMode.SPRINT):
                if(aux_time['cell'] == 1):
                    aux_time2 = aux_time.copy()
                    aux_time2['user_id'] = 0
                    aux_time2['us1'] = 'B'
                    aux_time2['id'] = aux_time2['id'] + 1000
                    self.AddTimeToDb(aux_time2) 
            eventCalcNow.set()
            #print "CalcNow: set", time.clock()
        else:
            pass # no new time                                         
    
    """
    runGetDiagnostic()
     - get diagnostic    
    """
    def runGetDiagnostic(self):
        """ get diagnostic """
        aux_diagnostic = {}
        for k, cmd_group in DEF_COMMANDS.DEF_COMMAND_GROUP['diagnostic'].iteritems():
            #print k, cmd_group
            aux_diagnostic[k] = self.send_receive_frame("GET_DIAGNOSTIC", cmd_group, diagnostic = dstore.Get("diagnostic")["log_cyclic"])
                    
        """ store terminal-states to the datastore """ 
        #if(dstore.IsReadyForRefresh("timing_settings")):           
        #    dstore.Set("timing_settings", aux_timing_setting, "GET")
        #else:
        #    print "not ready for refresh", aux_timing_setting
        return aux_diagnostic                                                                             
            
    def AddTimeToDb(self, time):                       
                                    
        '''console ouput''' 
        #print time                               
        aux_csv_string = str(time['id']) + ";" + hex(time['user_id'])+ ";" + str(time['cell']) + ";" + ";" + str(time['time_raw']).replace(',', '.')                                
        print "I: Comm: receive time:",self.index_times, ":", aux_csv_string
        
        #print struct.pack('<I', time['user_id']).encode('hex')
        
        DbTime = self.db.getParId("times", time['id'])

        if(DbTime == None):
            '''auto number, no logic'''
            ''' -> insert number(id) directly to the structure '''
            ds_times = dstore.Get("times")
            ds_racesettings = dstore.Get("racesettings-app")                       
            if(ds_racesettings["autonumbers"]["mode"] == AutonumbersMode.SINGLE):
                    auto_number = ds_times["auto_number"][0]
                    #print "NAHRAZUJI", time['user_id']
                    if(auto_number != 0) and (time['user_id'] == 0):
                        #print "NAHRAZUJI", time['user_id']
                        dbUser = self.db.getParX("users", "nr", auto_number, limit = 1).fetchone()
                        if dbUser != None:
                            #print "NAHRAZUJI", time['user_id'], dbUser['id']
                            time['user_id'] = dbUser['id']
            elif(ds_racesettings["autonumbers"]["mode"] == AutonumbersMode.SPRINT):
                '''
                cell 1 - semafor => generuje 2 casy, stejný raw time. (ten druhý je pouze v app, má ID +1000)
                cell 2,3 - ulitý start => generuje oboje jako cell 2,
                cell 4,5 - rychlost
                cell 6,7 - cíl => generuje oboje jako cell 250
                
                dráha A: 1,2,4,6 => 1,2,4,250 
                dráha B: 1,3,5,7 => 1,2,4,250
                '''
                #us1                
                time['un1'] = time['cell']   
                if time['cell'] == 1:                    
                    if time['us1'] == 'A':                        
                        auto_number = ds_times["auto_number"][0]
                    elif time['us1'] =='B':                        
                        auto_number = ds_times["auto_number"][1]
                    else:
                        pass          
                elif time['cell'] == 2:
                    time["us1"] = "A"
                    auto_number = ds_times["auto_number"][0]
                elif time['cell'] == 3:
                    time["us1"] = "B"
                    time["cell"] = 2
                    auto_number = ds_times["auto_number"][1]
                elif time['cell'] == 4:
                    time["us1"] = "A"
                    auto_number = ds_times["auto_number"][0]
                elif time['cell'] == 5:
                    time["us1"] = "B"
                    time["cell"] = 4
                    auto_number = ds_times["auto_number"][1]                                        
                elif time['cell'] == 6:
                    time["us1"] = "A"
                    time["cell"] = 250
                    auto_number = ds_times["auto_number"][0] 
                elif time['cell'] == 7:
                    time["us1"] = "B"
                    time["cell"] = 250
                    auto_number = ds_times["auto_number"][1] 
                else:
                    auto_number = 0;
                
                #replace the number in DB
                if(auto_number != 0) and (time['user_id'] == 0):
                    #print "NAHRAZUJI", time['user_id']
                    dbUser = self.db.getParX("users", "nr", auto_number, limit = 1).fetchone()
                    if dbUser != None:
                        #print "2-NAHRAZUJI", time['user_id'], dbUser['id']
                        time['user_id'] = dbUser['id']
            
             
            ''' auto cell logic'''                        
            ''' - inject the cell number
                - increment the index (ring buffer)
            '''
            if(ds_times["auto_cell_address"] == time['cell']):
                time['state'] = time['state']+str(time['cell'])                                
                time['cell'] = ds_times["auto_cell"][ds_times["auto_cell_index"]]
                if ((ds_times["auto_cell_index"]+1) < ds_racesettings["autocell"]["nr_cells"]):           
                    ds_times["auto_cell_index"] = ds_times["auto_cell_index"] + 1
                else:
                    ds_times["auto_cell_index"] = 0                                                   
                                            
            '''save to database'''        
            keys = ["state", "id", "user_id", "cell", "time_raw", "us1", "un1"]
            values = [time['state'], time['id'], time['user_id'], time['cell'], time['time_raw'], time['us1'], time['un1']]        
                    
            
            ret = self.db.insert_from_lists("times", keys, values)
            #print "prvni insert", ret
            #values[1] = values[1] + 1000 
            #ret |= self.db.insert_from_lists("times", keys, values)
            #print "druhy insert", ret
        else:
            ret = False
                
        '''return'''
        if ret == False:            
            print "I: DB: time already exists"
        else:
            #shift auto numbers
            aux_new_times = dstore.GetItem("gui", ["update_requests", "new_times"])            
            aux_new_times.append(time)              
            dstore.SetItem("gui", ["update_requests", "new_times"], aux_new_times)                                                                              
        return ret
                
if __name__ == "__main__":    
    print "main manage_com()"
    my_comm = ManageComm()         
    my_comm.start()
    while(1):
        pass
 
                    
            
