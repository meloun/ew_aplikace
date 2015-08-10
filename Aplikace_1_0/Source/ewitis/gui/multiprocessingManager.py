'''
Created on 8. 8. 2015

@author: Meloun
'''
import multiprocessing

class MultiprocessingManager():
    
    def __init__(self):
        pass  
    
    def Init(self, sharedDstore, sharedDfs, shareInfo):
        self.mgr = multiprocessing.Manager()
        self.dstore = self.mgr.dict(sharedDstore)
        self.dfs = self.mgr.dict(sharedDfs)
        self.info = self.mgr.dict(shareInfo)
    
    def GetDstore(self):        
        return self.dstore
    
    def GetDfs(self):
        return self.dfs
    
    def GetInfo(self):
        return self.info
    
eventCalcNow =  multiprocessing.Event()
#myevent2 =  multiprocessing.Event()       
mgr = MultiprocessingManager()