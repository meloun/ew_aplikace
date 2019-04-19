# -*- coding: utf-8 -*-
'''
Created on 28.12.2013

@author: Meloun
'''
class UPDATE_MODE:
    all, tables, gui = range(0,3)
    
class MyTab():
    """
    
    """
    def  __init__(self, tables = [], items = []):
        self.tables = tables
        self.items = items
        
    def Init(self):
        for table in self.tables:
            table.Init()
        for item in self.items:
            item.Init()
            
        
    def Update(self, mode = UPDATE_MODE.all):
        ret1 = True
        ret2 = True        
                
        #update tables
        for table in self.tables:
            ret1 = table.UpdateGui()
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
                ret1 = table.Update()                            
                            
                                                

        #update gui                
        if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.gui):
            for item in self.items:
                ret2 = item.Update()
                                
        return (ret1 and ret2)
                