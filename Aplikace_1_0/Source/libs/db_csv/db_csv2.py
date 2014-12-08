# -*- coding: utf-8 -*-
'''
Created on 04.02.2014
@author: Lubos Melichar
'''

import csv

class Db_csv():    
    def __init__(self, filename):
        self.filename = filename
        
    def header(self, encode = 'utf8'):
        reader = csv.DictReader(open(self.filename, "rb"), delimiter = ";", skipinitialspace=True)                
        return reader.fieldnames
        
    def reader(self, encode = 'utf8'):       
        reader = csv.DictReader(open(self.filename, "rb"), delimiter = ";", skipinitialspace=True)        
        for row in reader:
            yield  dict([(unicode(key,'utf-8'), unicode(value, 'utf-8')) for key, value in row.iteritems()])


    def load(self, encode = 'utf8'):
        return list(self.reader(encode))     

    def utf_8_encoder(self, unicode_dicts):
        for row in unicode_dicts:
            yield  dict([(key.encode('utf-8'), value.encode('utf-8')) for key, value in row.iteritems()])
    
    def utf_8_encoder2(self, unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')
    
    '''save csv into file from lists'''
    def save2(self, rows, header = [], encode = 'utf8'):       
                
        if header == []:
            header = self.header()                                        
        
        writer = csv.DictWriter(open(self.filename, 'wb'), fieldnames = header, delimiter=';')                        
        writer.writeheader()
        writer.writerows(self.utf_8_encoder(rows))
            
    '''save csv into file from lists'''
    def save(self, rows, header = [], encode = 'utf8'):       
                
        if header == []:
            header = self.header()                                        
        
        writer = csv.writer(open(self.filename, 'wb'), delimiter=';')                        
        writer.writerow(header)
        print "RR",rows
        writer.writerows(self.utf_8_encoder2(rows))    
        
    
if __name__ == '__main__':
    
    db = Db_csv("Blizak_2010.csv")    
    db2 = Db_csv("ahoj6.csv")
    
    print db.load()
    
    #print db.header()
    

#            
#    print "======================="
#    for row in db.load() :
#        if(row["headerA"] == u'ředkvička'):
#            print row
#            
#    for row in db.load():
#        if(row["headerA"] == u'ředkvička'):
#            print row
#
#    db2.save(db.load(), db.header())
    

#     for i in listofnames:
#         for h in i: 
#             print h,";",
#         print "\n-------------"
#     
#     print len(listofnames)    
#         
           