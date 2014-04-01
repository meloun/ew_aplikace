# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Lubos Melichar


'''
import csv

import libs.utils.utils as utils




class Db_csv():    
    def __init__(self, filename):
        self.filename = filename
        
    #load csv from file to lists
    def load(self, encode = 'utf8'):
                        
        reader = csv.reader(open(self.filename, "r"), delimiter = ";", skipinitialspace=True)
                
        list = []
        for row in reader:
            list.append([cell.decode(encode) for cell in row])                        
                    
#        for lt in list:
#            for item in lt:
#                print type(item), item 
                
        return list
    
    '''save csv into file from lists'''
    def save(self, lists, keys = None, encode = 'utf8'):       
                    
        my_string = ""    
        
        for list in lists:
            for item in list:                                                                                               
                my_string += str(item) + u';'
            my_string += "\n"            
                                        
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
        
           