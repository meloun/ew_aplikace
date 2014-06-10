#!/usr/bin/env python

from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.data.db import db

class CategoriesModel(myModel):
    def __init__(self, table):                                        
        myModel.__init__(self, table)
                                                             
class CategoriesProxyModel(myProxyModel):
    def __init__(self, table):                                
        myProxyModel.__init__(self, table)  
        

# view <- proxymodel <- model 
class Categories(myTable):
    def  __init__(self):                                                              
        myTable.__init__(self, "Categories")        
            
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
           
                        

tableCategories = Categories()
tabCategories = MyTab(tables = [tableCategories,])                               


        
       


        
        
            
            

        
        
    