# -*- coding: utf-8 -*-
from ewitis.data.DEF_DATA import *
import libs.datastore.permanent_datastore as datastore
import time
import datetime


class Dstore(datastore.PermanentDatastore):
    
    def __init__(self, db = None, data = None, process_dict = None):
        
        #init
        datastore.PermanentDatastore.__init__(self, db, data)
        
        self.ResetGetValues()
        self.process_dict = None
                
    
    def SetProcessDict(self, process_dict):
        print "share dict 2", id(process_dict)
        self.process_dict = process_dict
        print self.process_dict
        
    #
    def UpdateProcessDict(self, name):
        
        
        aux_dstore = {}
        
        if self.process_dict:           
            if name in self.process_dict["dstore"].keys():                
                for key in self.process_dict["dstore"].keys():   
                    aux_dstore[key] = self.Get(key)
                self.process_dict["dstore"] = aux_dstore            
                    
                print "nove hodnoty", name, self.process_dict                                                                                    

        
    #copy dict for calc-process
    def  Set(self, name, value, section = "GET_SET"):
        datastore.PermanentDatastore.Set(self, name, value, section)
        self.UpdateProcessDict(name)

        
    #copy dict for calc-process    
    def SetItem(self, name, keys, value, section = "GET_SET", changed = True):
        datastore.PermanentDatastore.SetItem(self, name, keys, value, section, changed)
        self.UpdateProcessDict(name)
        
         
        
    def ResetGetValues(self):
        
        #get cell task None         
        for idx in range(0, len(self.Get("cells_info", "GET"))):
            self.ResetValue("cells_info", [idx, "task"])
            
        #timing settings
        self.ResetValue("timing_settings", ["measurement_state"], MeasurementState.not_active)
        self.ResetValue("timing_settings", ["logic_mode"])        
                        
                            
    def IsTerminal(self):
        return self.IsDevice("Terminal")
    
    def IsBlackbox(self):
        return self.IsDevice("Blackbox")
        
    def IsDevice(self, name):
        hw_version = self.Get("versions")["hw"]
        if hw_version:
            if name in hw_version:
                return True
        return False
    
    
    def InitDiagnostic(self):
        self.SetItem("diagnostic", ["communication"], "")
        self.AddDiagnostic('Info', "Log cleared", 'black')
        
    def AddDiagnostic(self, cmd, data, color = "red", desc = None):
        
        #format        
        if type(cmd) is int:
            cmd = '%02x' % cmd
            data = ":".join(c.encode('hex') for c in data)        
        
        #prepare string
        mytime = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]        
        added_string = "<font color='grey' size='2'>"+ mytime +": </font>"          
        added_string += "<font color='" +color+ "'><b>"+cmd+"</b> " +data+ "</font>"
        if desc != None :
            added_string += "<font color='grey' size='2'>("+desc.lower()+")</font>"
        
            
        #write to datastore            
        aux_diagnostic = self.Get("diagnostic")
        self.SetItem("diagnostic", ["communication"], aux_diagnostic["communication"]+added_string+"<BR>")

#create datastore
print "I: Dstore init"
dstore = Dstore('conf/conf_work.json', DEF_DATA)
print "dstore id", id(dstore)
#a = multiprocessing.Manager().dict({"current_run":None, "racesettings-app":None, "additional_info": None})


#test
if __name__ == "__main__":
    from ewitis.data.DEF_DATA import *        
    mydatastore = Dstore(DEF_DATA)
    print mydatastore.Get("versions")
    print mydatastore.IsTerminal()           
    print mydatastore.IsBlackbox()           