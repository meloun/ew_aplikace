'''
Created on 4.1.2014

@author: Meloun
'''

from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import appWindow, Ui 
from ewitis.data.dstore import dstore 
from ewitis.gui.UiAccesories import MSGTYPE, uiAccesories
from ewitis.data.DEF_ENUM_STRINGS import * 
from ewitis.gui.barCellActions import barCellActions
import ewitis.gui.TimesUtils as TimesUtils

class Menus():
    
    def __init__(self):
        pass
            
    def init(self):
        pass
        
    def addSlots(self):
        pass
        
    def Update(self):
        pass
    
class Bars():
    
    def __init__(self):
        pass
    
           
    def Init(self):
        barCellActions.Init()
        self.createSlots()
        
    def createSlots(self):   
        barCellActions.createSlots()     
        QtCore.QObject.connect(Ui().aSetPort, QtCore.SIGNAL("triggered()"), self.sPortSet)        
        QtCore.QObject.connect(Ui().aConnectPort, QtCore.SIGNAL("triggered()"), self.sPortConnect)
        QtCore.QObject.connect(Ui().aEnableCommunication, QtCore.SIGNAL("triggered()"), lambda: uiAccesories.sGuiSetItem("port", ["enabled"], True))
        QtCore.QObject.connect(Ui().aDisableCommunication, QtCore.SIGNAL("triggered()"), lambda: uiAccesories.sGuiSetItem("port",["enabled"], False))
        
        #ping
        #enable cell
        #generate celltime
        #disable cell
        #clear database
                                                
        
    def Update(self):
        """ port name """
        Ui().aSetPort.setText(dstore.Get("port")["name"])                            
        Ui().aSetPort.setEnabled(not(dstore.Get("port")["opened"]))
        
        """ port conect """                                                                                                                                                        
        Ui().aConnectPort.setText(STRINGS.PORT_CONNECT[not dstore.Get("port")["opened"]])                                                                                                                            
                
        """ communicacation enabled/disabled """
        state = dstore.Get("port")['enabled']
        Ui().aEnableCommunication.setEnabled(not state)
        Ui().aDisableCommunication.setEnabled(state)
        
        # statusbar TIME <= race time
        time = dstore.Get("race_time")
        Ui().statusbar_time.setText(TimesUtils.TimesUtils.time2timestring(time))
        
        # statusbar measurement state
        timing_settings_get = dstore.Get("timing_settings", "GET")
        Ui().statusbar_msg.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])
        if timing_settings_get['measurement_state']== MeasurementState.not_active:
            Ui().statusbar_msg.setStyleSheet("background:red;")                    
        elif timing_settings_get['measurement_state']== MeasurementState.prepared:
            Ui().statusbar_msg.setStyleSheet("background:orange;")                    
        elif timing_settings_get['measurement_state']== MeasurementState.time_is_running:
            Ui().statusbar_msg.setStyleSheet("background:green;")
        elif timing_settings_get['measurement_state']== MeasurementState.finished:
            Ui().statusbar_msg.setStyleSheet("background:red;")
            
        barCellActions.Update()
            

        
        

    #########    
    # SLOTS
    #########
    def sPortSet(self):
        '''
        set the port
        ''' 
                
        import libs.comm.serial_utils as serial_utils         
            
        #dostupne porty
        ports = []        
        title = "Port Set"
        
        try:
            for p in serial_utils.enumerate_serial_ports():            
                ports.append(p)
        except:
            uiAccesories.showMessage(title, "No serial port available.")
            return   
    
        if (ports==[]):
            uiAccesories.showMessage(title, "No serial port available.")
            return    
                        
        ports = sorted(ports)                    

        item, ok = QtGui.QInputDialog.getItem(appWindow, "Serial Port",
                "Serial Port:", ports, 0, False)
        
        
        if (ok and item):                                  
            dstore.SetItem("port", ["name"], str(item))
            uiAccesories.showMessage(title, str(item), MSGTYPE.statusbar)
        
        self.Update()      
        
    def sPortConnect(self):
        '''
        connect/disconnect => create/kill communication thread
        '''

        import ewitis.comm.manage_comm as manage_comm
        
        title = "Port connect"
                                            
        #comm runs?        
        if(dstore.Get("port")["opened"] == True):                           
            
            # KILL COMMUNICATION - thread, etc..
            dstore.SetItem("port", ["opened"], False)                    
            uiAccesories.showMessage(title, dstore.Get("port")["name"]+" disconnected", MSGTYPE.statusbar)                       
        else:            
            uiAccesories.showMessage(title, dstore.Get("port")["name"]+" connected", MSGTYPE.statusbar)           
            # CREATE COMMUNICATION - thread, etc..                                    
                                 
            self.myManageComm = manage_comm.ManageComm(dstore)
            self.myManageComm.start()
            
            # wait to stable shared memory 
            time.sleep(0.2)            
            
            #already connected?                                
            #flag down => cant connect
            if(dstore.Get("port")["opened"] == False):            
                title = "Port connect"                                
                uiAccesories.showMessage(title, dstore.Get("port")["name"]+" cant connect")                
                                
        self.Update()   
    
bars = Bars()