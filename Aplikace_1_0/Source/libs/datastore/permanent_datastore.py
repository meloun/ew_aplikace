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
       
        #consistency check, if not consistent then update the datastore        
        self.consistency_check = self.UpdateConsistencyDict(self.data, default_data)
        print "I: Dstore: consistency check: ", self.consistency_check 
        if(self.consistency_check == False):
            self.db.dump(self.GetAllPermanents())
        
    def Update(self, update_dict):
        
        #update data
        datastore.Datastore.Update(self, update_dict)
        
        #update file with permanents datapoints
        self.db.dump(self.GetAllPermanents())
             
    #update consistency
    def UpdateConsistencyDict(self, destination, source):                            
        ret = True
        for k,v in source.iteritems():                         
            if isinstance(v, dict):
                #print "UCD----UCL", k, v                                                         
                if self.UpdateConsistencyDict(destination[k], v) == False:
                    ret = False
            elif isinstance(v, list):
                if self.UpdateConsistencyList(destination[k], v) == False:
                    ret = False            
            else:
                if k not in destination:
                    print "----NOT MATCH", k, v
                    destination[k] = v
                    ret = False                    
                #else:
                #    print "-MATCH", k, v
        return ret
    
    def UpdateConsistencyList(self, destination, source):
        ret = True
        for i in range(len(source)):
            if isinstance(source[i], dict):
                #print "UCL----UCD", source[i]                                                        
                if self.UpdateConsistencyDict(destination[i], source[i]) == False:
                    ret = False
            elif isinstance(source[i], list):
                #print "UCL----UCL", source[i]
                if self.UpdateConsistencyList(destination[i], source[i]) == False:
                    ret = False   
        return ret
                     

        
            
        
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
