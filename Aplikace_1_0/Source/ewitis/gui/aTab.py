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
    def  __init__(self, tables = [], guiitems = []):
        self.tables = tables
        self.items = guiitems
        
    def Init(self):
        for table in self.tables:
            table.Init()
        for item in self.items:
            item.Init()
            
        
    def Update(self, mode = UPDATE_MODE.all):
        
        if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.gui):
            for table in self.tables:
                table.Update()
                
        if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
            for item in self.items:
                item.Update()