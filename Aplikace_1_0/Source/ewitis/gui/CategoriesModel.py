#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class CategoriesParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Categories"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.CATEGORIES['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.CATEGORIES['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.CategoriesProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.CategoriesFilterLineEdit
        self.gui['filterclear'] = source.ui.CategoriesFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.CategoriesAdd
        self.gui['remove'] =  source.ui.CategoriesRemove
        self.gui['export'] = source.ui.CategoriesExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.CategoriesImport 
        self.gui['delete'] = source.ui.CategoriesDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.CategoriesCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = CategoriesModel                              
        self.classProxyModel = CategoriesProxyModel
                

class CategoriesModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)

        self.update()                    

                
    def getDefaultTableRow(self): 
        category = myModel.myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        category['start_nr'] = 0
        return category 
                    
class CategoriesProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self)  
        

# view <- proxymodel <- model 
class Categories(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)        
    
        
    def getDbCategoryFirst(self):
        return self.params.db.getFirst("categories")
        
    def getDbCategoryParName(self, name):
                 
        dbCategory = self.params.db.getParX("categories", "name", name).fetchone()        
                        
        return dbCategory
    
    def getTabCategoryParName(self, name):

        print type(name)                 
        dbCategory = self.getDbCategoryParName(name)
        
        tabCategory = self.model.db2tableRow(dbCategory)           
                        
        return tabCategory        
                        

                            


        
       


        
        
            
            

        
        
    