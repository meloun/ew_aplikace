# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import csv




class Db_csv():    
    def __init__(self, filename):
        self.filename = filename
        
    #load csv from file to lists
    def load(self, encode = 'utf8'):
                        
        reader = csv.reader(open(self.filename, "r"), delimiter = ";", skipinitialspace=True)
        

        listofnames = []

        for name in reader:
            listofnames.append(name)
        
        #print listofnames
        return listofnames
    
    #save csv into file from lists
    def save(self, lists, keys = None, encode = None):       
                    
        my_string = ""
        
        #my_string += ";".join(str(x) for x in keys) + "\n"
        if(keys != None):            
            my_string += ";".join((x) for x in keys) + "\n"
        
        for list in lists:
            for item in list:    
                #print type(item), item
                
                if type(item) is int:
                    #print "retype"
                    item = str(item)                
                if type(item) is unicode:
                    item = (item).encode('utf-8')           
                my_string += item+';'
            my_string += "\n"
            #print my_string
                        
        #print my_string, type(my_string)
        if encode != None:
            my_string = my_string.encode(encode)    
        
        FILE = open(self.filename, 'w')
        FILE.write(my_string)
        FILE.close()                   
        
    
if __name__ == '__main__':
    
    db = Db_csv("Blizak_2010.csv")

    listofnames = db.load()  

    for i in listofnames:
        for h in i: 
            print h,";",
        print "\n-------------"
    
    print len(listofnames)    
        
           