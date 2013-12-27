#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import Ui
from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class CategoriesParameters(myModel.myParameters):
       
    def __init__(self):
                                
        #table and db table name
        self.name = "Categories"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.CATEGORIES['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.CATEGORIES['table']
                
        #create MODEL and his structure
        #myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = Ui().CategoriesProxyView        
        
        #FILTER
        self.gui['filter'] = Ui().CategoriesFilterLineEdit
        self.gui['filterclear'] = Ui().CategoriesFilterClear
        
        #GROUPBOX
        self.gui['add'] = Ui().CategoriesAdd
        self.gui['remove'] =  Ui().CategoriesRemove
        self.gui['export'] = Ui().CategoriesExport
        self.gui['export_www'] = None
        self.gui['import'] = Ui().CategoriesImport 
        self.gui['delete'] = Ui().CategoriesDelete
        
        #COUNTER
        self.gui['counter'] = Ui().CategoriesCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = CategoriesModel                              
        self.classProxyModel = CategoriesProxyModel
                

class CategoriesModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                         

                
    def getDefaultTableRow(self): 
        category = myModel.myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        category['start_nr'] = 1
        return category 
                    
class CategoriesProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class Categories(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)        
    
        
    def getDbCategoryFirst(self):        
        return db.getFirst("categories")
    def getTabCategoryFirst(self):                  
        dbCategory = self.getDbCategoryFirst()        
        tabCategory = self.model.db2tableRow(dbCategory)                                   
        return tabCategory  
        
    def getDbCategoryParName(self, name):
                 
        dbCategory = db.getParX("categories", "name", name).fetchone()        
                        
        return dbCategory
    
    def getTabCategoryParName(self, name):

        print type(name)                 
        dbCategory = self.getDbCategoryParName(name)
        
        tabCategory = self.model.db2tableRow(dbCategory)           
                        
        return tabCategory
    
    def getDbCategoriesParGroupLabel(self, group_label):
                 
        dbCategories = db.getParX("categories", group_label, "1")        
                        
        return dbCategories
    
    def getTabCategoryParName(self, name):

        #print type(name)                 
        dbCategory = self.getDbCategoryParName(name)
        
        tabCategory = self.model.db2tableRow(dbCategory)           
                        
        return tabCategory          
                        

                            


        
       


        
        
            
            

        
        
    