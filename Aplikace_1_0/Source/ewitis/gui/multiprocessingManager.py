'''
Created on 8. 8. 2015

@author: Meloun
'''
import multiprocessing

class MultiprocessingManager():
    
    def __init__(self):
        pass
    
    def Init(self, mydict):
        self.mgr = multiprocessing.Manager()
        self.dict = self.mgr.dict(mydict)
    
    def Get(self):
        return self.dict
    
mgr = MultiprocessingManager()