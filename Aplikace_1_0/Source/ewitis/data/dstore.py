# -*- coding: utf-8 -*-
import libs.datastore.datastore as datastore
from ewitis.data.DEF_DATA import *

class Dstore(datastore.Datastore):
    
    def __init__(self, db = None, data = None):
        self.db = db
        if self.db != None:
            datastore.Datastore.__init__(self, DEF_DATA)
        else:
            datastore.Datastore.__init__(self, data)
        
    def Set(self, name, value, section = "GET_SET"):
        datastore.Datastore.Set(self, name, value, section)
#        if self.db != None:
#            self.db.dump(self.data)
        #print "DSTORE:setItem:", self.data
        
    def SetItem(self, name, keys, value, section = "GET_SET"):
        datastore.Datastore.SetItem(self, name, keys, value, section)
#        if self.db != None:
#            self.db.dump(self.data)
        #print "DSTORE:setItem:", self.data
                    
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


if __name__ == "__main__":        
    mydatastore = Dstore(DEF_DATA)
    print mydatastore.Get("versions")
    print mydatastore.IsTerminal()           
    print mydatastore.IsBlackbox()           