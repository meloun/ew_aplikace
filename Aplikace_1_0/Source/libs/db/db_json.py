# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
try: import simplejson as json
except ImportError: import json

class Db():
    ''' classdocs '''
    def __init__(self, filename, filename_restore):
        self.filename = filename
        self.filename_restore = filename_restore
        try:
            self.load()
        except IOError:
            print "E: DB: No file, restored from default-file"
            self.restore(filename_restore)            
        
    def load(self):
        return json.load(codecs.open(self.filename, 'r', 'utf-8'))
    
    def dump(self, data):
        json.dump(data, codecs.open(self.filename, 'w', 'utf-8'), ensure_ascii = False, indent = 4)
        
    def restore(self, filename_from = None):
        if filename_from == None:
            filename_from = self.filename_restore
        data = json.load(codecs.open(filename_from, 'r', 'utf-8'))
        self.dump(data)       
        
if __name__ == '__main__':
    import codecs, json
    
#    data =  {"a":{u'klíč1':u"čeština1", u'klíč2':u"maďarština1", u'klíč3':u"francouština1"},
#             "b":{u'klíč1':u"čeština2", u'klíč3':u"maďarština2", u'klíč6':u"francouština2"}
#            } 
    db_json = Db('filename.txt', 'file_in.txt')
    #db_json.restore('file_in.txt')
    #data = db_json.load()
    #print data
    #data['b'] = u"lubošekíšáýčříý"
    #db_json.dump(data)
       
#    data = json.load(codecs.open('file_in.txt', 'r', 'utf-8'))
#    json.dump(data, codecs.open('file_out.txt', 'w', 'utf-8'), ensure_ascii=False, indent=4)
    

    
    
        