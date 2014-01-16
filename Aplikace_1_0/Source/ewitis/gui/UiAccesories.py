# -*- coding: utf-8 -*-


from libs.myqt.mydialogs import *
from ewitis.data.dstore import dstore 
from ewitis.gui.Ui import Ui
 

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
   
    
class UiaDialogs(MyDialogs):
    def __init__(self):
        MyDialogs.__init__(self)                   
    def showMessage(self, title, message, msgtype = MSGTYPE.warning, *params):
        print "showMessage", title, message        
        #right statusbar
        if(msgtype == MSGTYPE.right_statusbar):            
            #all time update
            print "right status bar"
            self.update_right_statusbar(title, message)                 
            timing_settings_get = dstore.Get("timing_settings", "GET")
#            Ui().statusbar_msg.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])
#            if timing_settings_get['measurement_state']== MeasurementState.not_active:
#                Ui().statusbar_msg.setStyleSheet("background:red;")                    
#            elif timing_settings_get['measurement_state']== MeasurementState.prepared:
#                Ui().statusbar_msg.setStyleSheet("background:orange;")                    
#            elif timing_settings_get['measurement_state']== MeasurementState.time_is_running:
#                Ui().statusbar_msg.setStyleSheet("background:green;")
#            elif timing_settings_get['measurement_state']== MeasurementState.finished:
#                Ui().statusbar_msg.setStyleSheet("background:red;")
                                                
        #STATUSBAR        
        elif (msgtype == MSGTYPE.warning) or (msgtype == MSGTYPE.info) or (msgtype == MSGTYPE.statusbar):                                
            #timing_settings_get = dstore.Get("timing_settings", "GET")                       
            #Ui().statusbar_msg.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                                                                             
            Ui().statusbar.showMessage(title+" : " + message)
            print "NASTAVUJU", title, message        
        return MyDialogs.showMessage(self, title, message, msgtype, *params)
   
class UiAccesories(UiaDialogs):
    def __init__(self):                                                                        
        #init dialog   
        pass
    
    def Init(self):
        UiaDialogs.__init__(self)
        self.showMessage("Race", dstore.Get("race_name"), MSGTYPE.statusbar)
                                                                                                    
    def sGuiSet(self, name, value, tab = None, dialog = False):        
        if value == dstore.Get(name):
            return
                
        if(dialog == True):            
            name_string = dstore.GetName(name)            
            if (self.showMessage(name_string, "Are you sure you want to change \""+name_string+"\"? \n ", MSGTYPE.warning_dialog) != True):            
                return
                
        dstore.Set(name, value)
        #self.updateTab(tab)
        
        
    def sGuiSetItem(self, name, keys, value, callback = None, dialog = False):        
        if value == dstore.GetItem(name, keys):
            return
                
        if(dialog == True):            
            name_string = dstore.GetName(name)            
            if (self.showmessage(name_string, "Are you sure you want to change \""+name_string+"\"? \n ", MSGTYPE.warning_dialog) != True):            
                return
                
        dstore.SetItem(name, keys, value)
        if callback != None:        
            callback()

#instance
uiAccesories = UiAccesories()  
    
        
                           
        
           
