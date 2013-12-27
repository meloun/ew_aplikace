#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import Ui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class AlltagsParameters(myModel.myParameters):
       
    def __init__(self):
                                
        #table and db table name
        self.name = "Alltags"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.ALLTAGS['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.ALLTAGS['table']
                
        #create MODEL and his structure
        #myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = Ui().AlltagsProxyView        
        
        #FILTER
        self.gui['filter'] = Ui().AlltagsFilterLineEdit
        self.gui['filterclear'] = Ui().AlltagsFilterClear
        
        #GROUPBOX
        self.gui['add'] = Ui().AlltagsAdd
        self.gui['remove'] =  Ui().AlltagsRemove
        self.gui['export'] = Ui().AlltagsExport
        self.gui['export_www'] = None
        self.gui['import'] = Ui().AlltagsImport 
        self.gui['delete'] = Ui().AlltagsDelete
        
        #COUNTER
        self.gui['counter'] = Ui().AlltagsCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = AlltagsModel                              
        self.classProxyModel = AlltagsProxyModel
                

class AlltagsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                            

                
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)                                    
        return row
                    
class AlltagsProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class Alltags(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
    def getDbTagParTagId(self, tag_id):
                 
        dbTag = db.getParX("alltags", "tag_id", tag_id, limit = 1).fetchone()        
                        
        return dbTag   
           
                        

                            


        
       


        
        
            
            

        
        
    