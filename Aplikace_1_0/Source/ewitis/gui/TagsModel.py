#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class TagsParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Tags"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.TAGS['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.TAGS['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.TagsProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.TagsFilterLineEdit
        self.gui['filterclear'] = source.ui.TagsFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.TagsAdd
        self.gui['remove'] =  source.ui.TagsRemove
        self.gui['export'] = source.ui.TagsExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.TagsImport 
        self.gui['delete'] = source.ui.TagsDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.TagsCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = TagsModel                              
        self.classProxyModel = TagsProxyModel
                

class TagsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                            

                
    def getDefaultTableRow(self): 
        category = myModel.myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        category['start_nr'] = 0
        return category 
                    
class TagsProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class Tags(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
    def getDbTagParTagId(self, tag_id):
                 
        dbTag = self.params.db.getParX("tags", "tag_id", tag_id, limit = 1).fetchone()        
                        
        return dbTag   
    
    def getDbTagParUserNr(self, user_nr):
                 
        dbTag = self.params.db.getParX("tags", "user_nr", user_nr, limit = 1).fetchone()        
                        
        return dbTag
    
    def getTabTagParUserNr(self, user_nr):
                 
        
        #dbTag = self.params.db.getParX("tags", "user_nr", user_nr).fetchone()
        dbTag = self.getDbTagParUserNr(user_nr)        
                     
        tabTag = self.model.db2tableRow(dbTag)   
                                
        return tabTag       
                        

                            


        
       


        
        
            
            

        
        
    