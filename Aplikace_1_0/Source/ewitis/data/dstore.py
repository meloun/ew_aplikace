# -*- coding: utf-8 -*-
import libs.datastore.permanent_datastore as datastore


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


if __name__ == "__main__":
    from ewitis.data.DEF_DATA import *        
    mydatastore = Dstore(DEF_DATA)
    print mydatastore.Get("versions")
    print mydatastore.IsTerminal()           
    print mydatastore.IsBlackbox()           