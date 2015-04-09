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
        
        
    def Update(self, update_dict):
        
        #update data
        datastore.Datastore.Update(self, update_dict)
        
        #update file with permanents datapoints
        self.db.dump(self.GetAllPermanents()) 
        
            
        
    def Set(self, name, value, section = "GET_SET", permanent = True):
                

        
        #update data
        changed = datastore.Datastore.Set(self, name, value, section)
        
        #update file
        if changed and permanent and self.IsPermanent(name):
            #print "zapis", name, value
            self.db.dump(self.GetAllPermanents())
        
        
        
    def SetItem(self, name, keys, value, section = "GET_SET", permanent = True, changed = True):
                
        if(value == datastore.Datastore.GetItem(self, name, keys, section)):
            return                
        
        #set item  
        datastore.Datastore.SetItem(self, name, keys, value, section, changed)
        
        #store permanents to the file
        if permanent and self.IsPermanent(name):
            #print "zapis", name, keys, value, section
            self.db.dump(self.GetAllPermanents())            
                    

if __name__ == "__main__":        
    mydatastore = PermanentDatastore('conf/conf_work.json', {"a":1, "b":2})
