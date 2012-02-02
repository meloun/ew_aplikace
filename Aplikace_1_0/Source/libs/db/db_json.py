# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import json

class Db(object):
    ''' classdocs '''
    def __init__(self, filename):
        self.filename = filename
        #self.data = ''
        
    def load_from_file(self):
        FILE2 = open(self.filename)
        text = FILE2.read()
        data = json.loads(text)
        #self.data = json.loads(text)
        return data
    
    def dump_to_file(self, data):
        FILE = open(self.filename, 'w')
        text = json.dumps(data)
        #text = json.dumps(self.data)
        FILE.write(text)
        FILE.close() 
        
if __name__ == '__main__':
    db_json = Db("testfile.txt")
    data =  [{u'klíč1':u"čeština1", u'klíč2':u"maďarština1", u'klíč3':u"francouština1"},
            {u'klíč1':u"čeština2", u'klíč3':u"maďarština2", u'klíč6':u"francouština2"}
            ]
    db_json.dump_to_file(data)
    data = db_json.load_from_file()
    print data
    for record in data:
        print record
    #print raw_input()
    
    
        