'''
Created on 15. 8. 2015

@author: Meloun
'''
import sys

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename
        self.log = None

    def write(self, message):
        self.log = open(self.filename, "a")
        self.terminal.write(message)
        self.log.write(message)  
        self.log.close()
        
    def flush(self):
        self.terminal.flush()  