# -*- coding: utf-8 -*-
from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.data.db import db
              
class AlltagsModel(myModel):
    def __init__(self, table):                        
        myModel.__init__(self, table)
                                                
class AlltagsProxyModel(myProxyModel):
    def __init__(self, table):                                        
        myProxyModel.__init__(self, table)  
        

# view <- proxymodel <- model 
class Alltags(myTable):
    def  __init__(self):                                                              
        myTable.__init__(self, "Alltags")
        
    def getDbTagParTagId(self, tag_id):                 
        dbTag = db.getParX("alltags", "tag_id", tag_id, limit = 1).fetchone()                                
        return dbTag   


tableAlltags = Alltags()
tabAlltags = MyTab(tables = [tableAlltags,])           
                        

                            


        
       


        
        
            
            

        
        
    