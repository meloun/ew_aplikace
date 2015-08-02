# -*- coding: utf-8 -*-
from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.data.db import db
import libs.sqlite.sqlite_utils as db_utils

    
class TagsModel(myModel):
    def __init__(self, table):                                        
        myModel.__init__(self, table)                
                    
class TagsProxyModel(myProxyModel):
    def __init__(self, table):                                        
        myProxyModel.__init__(self, table)  
        

# view <- proxymodel <- model 
class Tags(myTable):
    def  __init__(self):                                                              
        myTable.__init__(self, "Tags")
        
    def getDbTagParTagId(self, tag_id, db_con = None):
        if db_con == None:
            db_con = self.db_con
                 
        dbTag = db_utils.getParX(db_con, "tags", "tag_id", tag_id, limit = 1).fetchone() 
        #dbTag = db.getParX("tags", "tag_id", tag_id, limit = 1).fetchone()        
                        
        return dbTag   
    
    def getDbTagParUserNr(self, user_nr, db_con = None):
        if db_con == None:
            db_con = self.db_con
                 
        dbTag = db_utils.getParX(db_con, "tags", "user_nr", user_nr, limit = 1).fetchone()
        #dbTag = db.getParX("tags", "user_nr", user_nr, limit = 1).fetchone()        
                        
        return dbTag
    
    def getTabTagParUserNr(self, user_nr):
                 
        
        #dbTag = db.getParX("tags", "user_nr", user_nr).fetchone()
        dbTag = self.getDbTagParUserNr(user_nr)        
                     
        tabTag = self.model.db2tableRow(dbTag)   
                                
        return tabTag       

tableTags = Tags()
tabTags = MyTab(tables = [tableTags,])                          

                            


        
       


        
        
            
            

        
        
    