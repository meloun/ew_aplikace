# -*- coding: utf-8 -*-
import libs.datastore.permanent_datastore as datastore
import time
import datetime


class Dstore(datastore.PermanentDatastore):
    
    def __init__(self, db = None, data = None):
        
        #init
        datastore.PermanentDatastore.__init__(self, db, data)
                            
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


if __name__ == "__main__":
    from ewitis.data.DEF_DATA import *        
    mydatastore = Dstore(DEF_DATA)
    print mydatastore.Get("versions")
    print mydatastore.IsTerminal()           
    print mydatastore.IsBlackbox()           