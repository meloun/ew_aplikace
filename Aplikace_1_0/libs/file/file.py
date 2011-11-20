# -*- coding: utf-8 -*-
'''
Created on 13.10.2009
@author: Lubos Melichar
'''
class File(object):
    def __init__(self, filename):
        self.filename = filename

    ''' '''        
    def read(self):
        FILE = open(self.filename)
        text = FILE.read()
        return text
    
    def write(self, text):
        FILE = open(self.filename, 'w')
        FILE.write(text)
        FILE.close()
        
    def add(self, text):
        FILE = open(self.filename, 'a')
        FILE.write(text)
        FILE.close()
        
if __name__ == '__main__':
    file = File("testfile.txt")
    text = "ahoj jak se máš"
    file.write(text)
    data = file.read()
    print data