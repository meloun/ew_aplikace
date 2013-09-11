# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import simplejson as json
import codecs

class Db():
    ''' classdocs '''
    def __init__(self, filename, data_restore = None, filename_restore = None):
        self.filename = filename
        self.filename_restore = filename_restore
        try:
            self.load()
        except IOError:
            try:
                print "E: DB: "+self.filename+" : No file, restoring from default-file.."
                self.restore(data_restore, filename_restore)
            except:
                print "E: DB: "+self.filename+" : No file for restoring.."
                        
        
    #read from the file
    def load(self):
        return json.load(codecs.open(self.filename, 'r', 'utf-8'))
    
    #dump data to the file
    def dump(self, data):
        json.dump(data, codecs.open(self.filename, 'w', 'utf-8'), ensure_ascii = False, indent = 4)
            
    #restore from data        
    def restore_from_data(self, data = None):
        if data == None:
            data = self.data_restore                                
        
        #dump to the file
        self.dump(data)
               
    #restore from file               
    def restore_from_file(self, filename_from = None):
        if filename_from == None:
            filename_from = self.filename_restore
            
        #read data from file
        data = json.load(codecs.open(filename_from, 'r', 'utf-8'))
        #dump to the file
        self.dump(data)       
    
    #restore from data or from file
    def restore(self, data = None, filename_from = None):
        try:
            print "restoring from data"
            self.restore_from_data(data)
        except:
            print "restoring from file"
            self.restore_from_file(filename_from)
                
            
if __name__ == '__main__':    
    
#    data =  {"a":{u'klíč1':u"čeština1", u'klíč2':u"maďarština1", u'klíč3':u"francouština1"},
#             "b":{u'klíč1':u"čeština2", u'klíč3':u"maďarština2", u'klíč6':u"francouština2"}
#            }
    from ewitis.data.DEF_DATA import *
 
 
    db_restore = Db('conf/conf_restore.json')
    db_restore.dump(DEF_DATA)

    #init work file 
    db_json = Db('conf/conf_work.json', 'conf/conf_restore.json')
    data = db_json.load()
    #print data["port_name"]                                       
    #self.datastore = dstore.Dstore(DEF_DATA)  

    
#    db = db_json.load()    
#    print db
#    db["show"] = "AHOJ"
#    print db    
#    print DEF_DATA
#    db_json.dump(DEF_DATA)
    #db_json.restore('file_in.txt')
    #data = db_json.load()
       

#    data = json.load(codecs.open('file_in.txt', 'r', 'utf-8'))
#    json.dump(data, codecs.open('file_out.txt', 'w', 'utf-8'), ensure_ascii=False, indent=4)
    

    
    
        