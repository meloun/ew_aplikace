# -*- coding: utf-8 -*-
import libs.datastore.datastore as datastore
import libs.db.db_json as db_json

class PermanentDatastore(datastore.Datastore):
    
    def __init__(self, filename, default_data):
        
        #create datastore, default dictionary
        datastore.Datastore.__init__(self, default_data)        
        
        #create db, restore: permanents from default dict
        self.db = db_json.Db(filename, self.GetAllPermanents())
        
        #update datastore from db
        self.Update(self.db.load())
            
        
    def Set(self, name, value, section = "GET_SET"):        
        #set
        datastore.Datastore.Set(self, name, value, section)
        
        #store permanents to the file
        if self.IsPermanent(name):
            self.db.dump(self.GetAllPermanents())                
            #print "DSTORE: Set()", self.data[name]
        
    def SetItem(self, name, keys, value, section = "GET_SET", changed = True):        
        #set item
        datastore.Datastore.SetItem(self, name, keys, value, section, changed)
        
        #store permanents to the file
        if self.IsPermanent(name):
            self.db.dump(self.GetAllPermanents())
            #print "DSTORE: SetItem()", self.data[name]
                    

if __name__ == "__main__":        
    mydatastore = PermanentDatastore('conf/conf_work.json', {"a":1, "b":2})
