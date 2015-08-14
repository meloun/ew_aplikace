# -*- coding: utf-8 -*-
'''
Created on 28. 7. 2015

@author: Meloun
'''


class ListOfDicts():
    def __init__(self, rows): 
        self.rows = rows
    
    def Get(self, name, positive_filter = None, negative_filter = None):
        
        if positive_filter:
            list = [row[name] for row in self.rows if row[positive_filter[0]] == positive_filter[1]]
        elif negative_filter:
            list = [row[name] for row in self.rows if row[negative_filter[0]] != negative_filter[1]]
        else:
            list = [row[name] for row in self.rows]
        
    
        return list
    

if __name__ == "__main__":
    cmds = [                                                                
            {'cmd':0x02,  'length':0,     'blackbox': True,    'terminal': True},                                      
            {'cmd':0x08,  'length':2,     'blackbox': True,    'terminal': False},
            {'cmd':0x011, 'length':15,    'blackbox': True,    'terminal': False}
    ]
    
    mylists = ListOfDicts(cmds)
    
    print mylists.Get("cmd", ('cmd',2))
    print mylists.Get("length", ("length", 2))
